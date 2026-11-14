"""ProgramBench verifier for BenchFlow.

Downloads every active test branch's archive from Hugging Face first, before
any of the agent's code runs; then compiles the agent's submission, runs each
branch's pytest suite, parses JUnit XML results, and writes a partial-credit
reward.

The archives are the task's hidden tests, so a failed download is never the
submission's 0: verify.py then writes no reward and exits with
DOWNLOAD_FAILED_EXIT, and the run ends unscored. The task's [verifier]
allowlist names the hosts the download and each run.sh need.

A branch whose tests never report (its archive would not extract, or run.sh
stopped before pytest wrote eval/results.xml, say on a refused pip or apt
fetch) counts every expected test as failed, as ProgramBench's own eval does
(not_run): a silent branch never leaves the denominator.
"""

from __future__ import annotations

import argparse
import json
import os
import signal
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

#: Exit status when a hidden-test archive cannot be downloaded (no reward).
DOWNLOAD_FAILED_EXIT = 3
HF_DATASET = "programbench/ProgramBench-Tests"


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


def _stash_executable(workspace: Path, stash: Path) -> Path:
    """Move the compiled executable to a safe location."""
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
    # A process still running the previous copy keeps its own inode; writing
    # over a running binary fails with ETXTBSY.
    dest.unlink(missing_ok=True)
    shutil.copy2(str(stash), str(dest))
    dest.chmod(0o755)


def _stop_leftovers(pgid: int, workspace: Path, stash: Path) -> None:
    """Kill what a branch's tests left running (a watcher, a clock, a server):
    their process group, and any process still running the submission, which
    may have left the group."""
    try:
        os.killpg(pgid, signal.SIGKILL)
    except (ProcessLookupError, PermissionError):
        pass
    targets = {
        os.path.realpath(str(workspace / "executable")),
        os.path.realpath(str(stash)),
    }
    for entry in Path("/proc").iterdir():
        if not entry.name.isdigit() or int(entry.name) == os.getpid():
            continue
        try:
            exe = os.readlink(str(entry / "exe"))
        except OSError:
            continue
        if exe.endswith(" (deleted)"):
            exe = exe[: -len(" (deleted)")]
        if exe in targets:
            try:
                os.kill(int(entry.name), signal.SIGKILL)
            except OSError:
                pass


def _download_test_blob(instance_id: str, branch: str) -> Path:
    """Download a test branch archive from HuggingFace."""
    from huggingface_hub import hf_hub_download

    return Path(
        hf_hub_download(
            repo_id=HF_DATASET,
            filename=f"{instance_id}/tests/{branch}.tar.gz",
            repo_type="dataset",
        )
    )


def _download_all(instance_id: str, branches: list[str]) -> dict[str, Path]:
    """Every branch's archive, or exit DOWNLOAD_FAILED_EXIT with no reward.

    Runs before the agent's compile.sh or executable, so a failure here comes
    from the network or Hugging Face, never from the submission.
    """
    blobs: dict[str, Path] = {}
    for branch in branches:
        try:
            blobs[branch] = _download_test_blob(instance_id, branch)
        except Exception as exc:
            sys.stdout.flush()
            print(
                f"ERROR: hidden-test download failed: {instance_id} branch "
                f"{branch} from Hugging Face dataset {HF_DATASET}: "
                f"{type(exc).__name__}: {exc}",
                file=sys.stderr,
            )
            print(
                "ERROR: no reward written and the run is not scored: the "
                "hidden tests are unavailable, which says nothing about the "
                "submission. The verifier needs the Hugging Face hosts in the "
                "task's [verifier] allowed_hosts.",
                file=sys.stderr,
                flush=True,
            )
            sys.exit(DOWNLOAD_FAILED_EXIT)
    return blobs


def _run_test_branch(
    workspace: Path, branch: str, blob_path: Path, stash: Path, expected: int
) -> tuple[int, int]:
    """Run one test branch and return (passed, total).

    *expected* is the branch's test count in tests.json: the total when the
    branch reports no tests.
    """
    try:
        subprocess.run(
            ["tar", "xzf", str(blob_path), "-C", str(workspace)],
            check=True,
            timeout=120,
        )
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as exc:
        print(f"  WARNING: failed to extract archive for branch {branch}: {exc}")
        return 0, expected

    # Restore executable
    _restore_executable(stash, workspace)

    # Patch timeout method (same as ProgramBench eval)
    run_sh = workspace / "eval" / "run.sh"
    if run_sh.exists():
        content = run_sh.read_text()
        content = content.replace("--timeout-method=thread", "--timeout-method=signal")
        run_sh.write_text(content)
        run_sh.chmod(0o755)
        # Run tests in a session of their own, so what they leave running
        # can be stopped before the next branch copies the executable back.
        proc = subprocess.Popen(
            ["bash", str(run_sh)], cwd=str(workspace), start_new_session=True
        )
        try:
            proc.wait(timeout=3600)
        except subprocess.TimeoutExpired:
            print(f"  WARNING: test run timed out for branch {branch}")
        finally:
            _stop_leftovers(proc.pid, workspace, stash)
            proc.wait()

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
    if total == 0 and expected:
        print(
            f"  WARNING: branch {branch} reported no tests; its {expected} "
            "expected tests count as failed"
        )
        passed, total = 0, expected

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
    parser.add_argument("--tests-json", default="/tests/tests.json", type=Path)
    parser.add_argument(
        "--stash-path", default="/opt/benchflow-stashed-executable", type=Path
    )
    args = parser.parse_args()

    reward_file: Path = args.reward_file
    reward_file.parent.mkdir(parents=True, exist_ok=True)
    # Only this run's verdict may be read as the reward.
    reward_file.unlink(missing_ok=True)

    # Load tests.json from the tests/ directory (copied by BenchFlow)
    tests_json_path: Path = args.tests_json
    if not tests_json_path.exists():
        print(f"ERROR: {tests_json_path} not found")
        reward_file.write_text("0")
        sys.exit(0)

    tests_data = json.loads(tests_json_path.read_text())
    branches = tests_data.get("branches", {})
    clean_hashes: list[str] = json.loads(args.clean_hashes)
    active_branches = [
        name for name, info in branches.items() if not info.get("ignored")
    ]

    # Step 0: Download every hidden-test archive before any of the agent's
    # code runs; a failure exits DOWNLOAD_FAILED_EXIT with no reward.
    print("=== Step 0: Downloading hidden tests ===", flush=True)
    blobs = _download_all(args.instance_id, active_branches)

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
    stash = _stash_executable(args.workspace, args.stash_path)

    # Step 4: Run test branches
    print("=== Step 3: Running behavioral tests ===")
    total_passed = 0
    total_tests = 0

    for i, branch in enumerate(active_branches):
        print(f"  Branch {i + 1}/{len(active_branches)}: {branch}")
        passed, total = _run_test_branch(
            args.workspace,
            branch,
            blobs[branch],
            stash,
            len(branches[branch].get("tests") or []),
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
