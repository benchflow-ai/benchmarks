"""ProgramBench verifier for BenchFlow.

Compiles the agent's submission, downloads test branch archives from
HuggingFace, runs each branch's pytest suite, parses JUnit XML results,
and writes a partial-credit reward.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


def _compile(workspace: Path) -> bool:
    """Run compile.sh and return True on success."""
    compile_sh = workspace / "compile.sh"
    if not compile_sh.exists():
        print("ERROR: No compile.sh found in workspace")
        return False
    compile_sh.chmod(0o755)
    result = subprocess.run(
        ["bash", str(compile_sh)],
        cwd=str(workspace),
        timeout=900,
        capture_output=False,
    )
    if result.returncode != 0:
        print(f"ERROR: compile.sh exited with code {result.returncode}")
        return False
    if not (workspace / "executable").exists():
        print("ERROR: compile.sh did not produce ./executable")
        return False
    return True


def _remove_hashed_files(workspace: Path, hashes: list[str]) -> None:
    """Remove files whose SHA-256 matches any of the given hashes.

    Prevents trivial solutions that just copy the original binary.
    """
    if not hashes:
        return
    hash_set = set(hashes)
    result = subprocess.run(
        ["find", str(workspace), "-type", "f", "-exec", "sha256sum", "{}", "+"],
        capture_output=True,
        text=True,
        timeout=120,
    )
    for line in result.stdout.strip().splitlines():
        parts = line.split("  ", 1)
        if len(parts) == 2 and parts[0] in hash_set:
            path = Path(parts[1])
            print(f"Removing hash-matched file: {path}")
            path.unlink(missing_ok=True)


def _stash_executable(workspace: Path) -> Path:
    """Move the compiled executable to a safe location."""
    stash = Path("/opt/benchflow-stashed-executable")
    exe = workspace / "executable"
    if exe.exists():
        import shutil
        shutil.move(str(exe), str(stash))
        stash.chmod(0o755)
    return stash


def _restore_executable(stash: Path, workspace: Path) -> None:
    """Copy the stashed executable back into workspace."""
    import shutil
    dest = workspace / "executable"
    shutil.copy2(str(stash), str(dest))
    dest.chmod(0o755)


def _download_test_blob(instance_id: str, branch: str) -> Path:
    """Download a test branch archive from HuggingFace."""
    from huggingface_hub import hf_hub_download

    return Path(
        hf_hub_download(
            repo_id="programbench/ProgramBench-Tests",
            filename=f"{instance_id}/tests/{branch}.tar.gz",
            repo_type="dataset",
        )
    )


def _run_test_branch(
    workspace: Path, instance_id: str, branch: str, stash: Path
) -> tuple[int, int]:
    """Run one test branch and return (passed, total)."""
    # Download and extract test archive
    try:
        blob_path = _download_test_blob(instance_id, branch)
    except Exception as exc:
        print(f"  WARNING: failed to download blob for branch {branch}: {exc}")
        return 0, 0

    try:
        subprocess.run(
            ["tar", "xzf", str(blob_path), "-C", str(workspace)],
            check=True,
            timeout=120,
        )
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as exc:
        print(f"  WARNING: failed to extract archive for branch {branch}: {exc}")
        return 0, 0

    # Restore executable
    _restore_executable(stash, workspace)

    # Patch timeout method (same as ProgramBench eval)
    run_sh = workspace / "eval" / "run.sh"
    if run_sh.exists():
        content = run_sh.read_text()
        content = content.replace("--timeout-method=thread", "--timeout-method=signal")
        run_sh.write_text(content)
        run_sh.chmod(0o755)
        # Run tests
        try:
            subprocess.run(
                ["bash", str(run_sh)],
                cwd=str(workspace),
                timeout=3600,
                capture_output=False,
            )
        except subprocess.TimeoutExpired:
            print(f"  WARNING: test run timed out for branch {branch}")

    # Parse results
    passed = 0
    total = 0
    results_xml = workspace / "eval" / "results.xml"
    if results_xml.exists():
        try:
            raw = results_xml.read_text()
            root = ET.fromstring(raw)
            for tc in root.iter("testcase"):
                total += 1
                has_fail = any(
                    c.tag in ("failure", "error") for c in tc
                )
                if not has_fail:
                    passed += 1
        except ET.ParseError as exc:
            print(f"  WARNING: failed to parse results.xml: {exc}")

    # Clean up test artifacts for next branch
    eval_dir = workspace / "eval"
    if eval_dir.exists():
        import shutil
        shutil.rmtree(eval_dir, ignore_errors=True)

    return passed, total


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--instance-id", required=True)
    parser.add_argument("--workspace", required=True, type=Path)
    parser.add_argument("--clean-hashes", default="[]")
    parser.add_argument("--reward-file", required=True, type=Path)
    args = parser.parse_args()

    reward_file: Path = args.reward_file
    reward_file.parent.mkdir(parents=True, exist_ok=True)

    # Load tests.json from the tests/ directory (copied by BenchFlow)
    tests_json_path = Path("/tests/tests.json")
    if not tests_json_path.exists():
        print("ERROR: /tests/tests.json not found")
        reward_file.write_text("0")
        sys.exit(0)

    tests_data = json.loads(tests_json_path.read_text())
    branches = tests_data.get("branches", {})
    clean_hashes: list[str] = json.loads(args.clean_hashes)

    # Step 1: Remove hash-matched files from submission (anti-cheat).
    # Must happen BEFORE compile — matches ProgramBench's eval order.
    # The hashes identify the original pre-compiled binary; removing them
    # before compile prevents trivial copies while allowing a legitimate
    # rebuild that happens to produce a byte-identical executable.
    print("=== Step 1: Checking for copied binaries ===")
    _remove_hashed_files(args.workspace, clean_hashes)

    # Step 2: Compile
    print("=== Step 2: Compiling submission ===")
    if not _compile(args.workspace):
        reward_file.write_text("0")
        sys.exit(0)

    # Step 3: Stash executable
    stash = _stash_executable(args.workspace)

    # Step 4: Run test branches
    print("=== Step 3: Running behavioral tests ===")
    total_passed = 0
    total_tests = 0
    active_branches = [
        name for name, info in branches.items() if not info.get("ignored")
    ]

    for i, branch in enumerate(active_branches):
        print(f"  Branch {i + 1}/{len(active_branches)}: {branch}")
        passed, total = _run_test_branch(
            args.workspace, args.instance_id, branch, stash
        )
        total_passed += passed
        total_tests += total
        print(f"    {passed}/{total} tests passed")

    # Step 5: Compute reward
    reward = total_passed / total_tests if total_tests > 0 else 0.0
    reward_file.write_text(f"{reward:.6f}")
    print(f"\n=== Result: {total_passed}/{total_tests} = {reward:.4f} ===")


if __name__ == "__main__":
    main()
