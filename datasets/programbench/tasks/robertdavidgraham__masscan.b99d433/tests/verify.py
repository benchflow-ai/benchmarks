"""ProgramBench verifier for BenchFlow.

Step 0, before any of the agent's code runs: download every active test
branch's archive from Hugging Face, check that each one opens and holds
eval/run.sh, and install the pip requirements the run.sh files name. Then
compile the agent's submission, run each branch's pytest suite, parse the
JUnit XML results, and write a partial-credit reward.

The archives are the task's hidden tests, so a missing test is never the
submission's 0. When Step 0 cannot make the tests ready (a failed download, an
unusable archive, PyPI unreachable), verify.py writes no reward and exits with
DOWNLOAD_FAILED_EXIT. When a branch's tests report no results (pytest never
ran or never finished), it writes no reward and exits with
TESTS_DID_NOT_REPORT_EXIT. Either way the run ends unscored, never with a
silent 0 or a partial score. The task's [verifier] allowlist names the hosts
Step 0 and run.sh need.
"""

from __future__ import annotations

import argparse
import errno
import gzip
import json
import os
import re
import shlex
import signal
import subprocess
import sys
import tarfile
import tempfile
import xml.etree.ElementTree as ET
import zlib
from pathlib import Path

#: Exit status when Step 0 cannot make the hidden tests ready (no reward).
DOWNLOAD_FAILED_EXIT = 3
#: Exit status when a branch's tests report no results (no reward).
TESTS_DID_NOT_REPORT_EXIT = 5
HF_DATASET = "programbench/ProgramBench-Tests"

# A failure on this machine (a full or read-only disk), not on the network.
_LOCAL_ERRNOS = {errno.ENOSPC, errno.EDQUOT, errno.EROFS}
_LOCAL_TEXT = (
    "No space left on device",
    "os error 28",
    "Disk quota exceeded",
    "Read-only file system",
)
# pip output that says the package index could not be reached or answered.
_PIP_NETWORK = re.compile(
    r"Max retries exceeded|NewConnectionError|ConnectionError|ConnectTimeout"
    r"|ReadTimeout|Read timed out|timed out|Temporary failure in name resolution"
    r"|Name or service not known|Failed to establish a new connection"
    r"|Connection refused|Connection reset|ProxyError|Tunnel connection failed"
    r"|Cannot connect to proxy|SSLError|CERTIFICATE_VERIFY_FAILED"
    r"|HTTP error \d{3}|\b(?:403|404|429|5\d\d) (?:Client|Server) Error"
    r"|from versions: none",
    re.IGNORECASE,
)
_PIP_CMD = re.compile(
    r"^(?:sudo\s+(?:-\S+\s+)*)?(?:[\w./-]*python[\d.]*\s+-m\s+)?pip[\d.]*\s+"
    r"(?P<opts>(?:-\S+\s+)*)install\b(?P<args>.*)$"
)
_REDIRECT = re.compile(r"^(?:\d*>>?|&>>?|\d*<)")
_OPTION_WITH_VALUE = (
    "-i", "--index-url", "--extra-index-url", "-c", "--constraint",
    "-t", "--target", "--timeout", "--retries",
)


def _fail(lines: list[str], code: int) -> None:
    """Print the reasons on stderr and exit *code*, with no reward written."""
    sys.stdout.flush()
    for line in lines:
        print(line, file=sys.stderr)
    sys.stderr.flush()
    sys.exit(code)


def _local_cause(exc: BaseException | None) -> str | None:
    """The local reason (a full or read-only disk) behind *exc*, else None."""
    seen = set()
    while exc is not None and id(exc) not in seen:
        seen.add(id(exc))
        if isinstance(exc, OSError) and exc.errno in _LOCAL_ERRNOS:
            return os.strerror(exc.errno)
        text = str(exc)
        for marker in _LOCAL_TEXT:
            if marker in text:
                return marker
        exc = exc.__cause__ or exc.__context__
    return None


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


def _remove_hashed_files(roots: list[Path], hashes: list[str]) -> None:
    """Remove files whose SHA-256 matches any of the given hashes, in the
    workspace and in the other places the agent could write (a copy moved to
    /tmp is removed too).

    Prevents trivial solutions that just copy the original binary.
    """
    if not hashes:
        return
    hash_set = set(hashes)
    existing = [str(r) for r in roots if r.is_dir()]
    if not existing:
        return
    result = subprocess.run(
        ["find", *existing, "-xdev", "-type", "f", "-exec", "sha256sum", "{}", "+"],
        capture_output=True,
        text=True,
        timeout=600,
    )
    for line in result.stdout.strip().splitlines():
        parts = line.split("  ", 1)
        if len(parts) == 2 and parts[0] in hash_set:
            path = Path(parts[1])
            print(f"Removing hash-matched file: {path}")
            path.unlink(missing_ok=True)


def _stash_executable(workspace: Path, stash: Path) -> Path:
    """Copy the compiled executable's bytes to a safe location and remove it
    from the workspace. The stash is a regular file even when executable is
    a symlink, so nothing below acts on the symlink's target."""
    exe = workspace / "executable"
    if exe.exists():
        import shutil
        stash.unlink(missing_ok=True)
        shutil.copyfile(str(exe), str(stash))
        stash.chmod(0o755)
        exe.unlink()
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
    their process group, and any process still running one of the two copies
    of the submission, which may have left the group. The copies are matched
    by their own paths, never by what a path resolves to."""
    try:
        os.killpg(pgid, signal.SIGKILL)
    except (ProcessLookupError, PermissionError):
        pass
    targets = {
        os.path.join(os.path.realpath(str(workspace)), "executable"),
        os.path.join(os.path.realpath(str(stash.parent)), stash.name),
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
    """Every branch's archive, or exit DOWNLOAD_FAILED_EXIT with no reward."""
    blobs: dict[str, Path] = {}
    for branch in branches:
        try:
            blobs[branch] = _download_test_blob(instance_id, branch)
        except Exception as exc:
            what = (
                f"{instance_id} branch {branch} from Hugging Face dataset "
                f"{HF_DATASET}: {type(exc).__name__}: {exc}"
            )
            local = _local_cause(exc)
            if local:
                _fail(
                    [
                        f"ERROR: hidden-test download failed on this machine "
                        f"({local}), not on the network: {what}",
                        "ERROR: no reward written and the run is not scored.",
                    ],
                    DOWNLOAD_FAILED_EXIT,
                )
            _fail(
                [
                    f"ERROR: hidden-test download failed: {what}",
                    "ERROR: no reward written and the run is not scored: the "
                    "hidden tests are unavailable, which says nothing about the "
                    "submission. The verifier needs the Hugging Face hosts in "
                    "the task's [verifier] allowed_hosts.",
                ],
                DOWNLOAD_FAILED_EXIT,
            )
    return blobs


def _archive_contents(blob: Path) -> tuple[str, dict[str, str]]:
    """eval/run.sh's text and any requirements*.txt files in the archive.

    Reads the archive to its end first (gzip checks its length and CRC there),
    then lists it. Raises ValueError when the archive is unusable.
    """
    try:
        with gzip.open(str(blob), "rb") as stream:
            while stream.read(1 << 20):
                pass
        run_sh = None
        requirements: dict[str, str] = {}
        with tarfile.open(str(blob), "r:gz") as tar:
            for member in tar:
                name = member.name[2:] if member.name.startswith("./") else member.name
                if not member.isfile():
                    continue
                wanted = name == "eval/run.sh" or (
                    name.rsplit("/", 1)[-1].startswith("requirements")
                    and name.endswith(".txt")
                    and member.size < (1 << 20)
                )
                if not wanted:
                    continue
                data = tar.extractfile(member)
                text = data.read().decode("utf-8", "replace") if data else ""
                if name == "eval/run.sh":
                    run_sh = text
                else:
                    requirements[name] = text
    except (OSError, EOFError, tarfile.TarError, zlib.error) as exc:
        raise ValueError(f"unreadable archive: {type(exc).__name__}: {exc}") from exc
    if run_sh is None:
        raise ValueError("the archive has no eval/run.sh")
    return run_sh, requirements


def _pip_requirements(run_sh: str) -> tuple[bool, list[str], list[str]]:
    """(upgrade pip, packages, requirement files) that run.sh's pip lines install."""
    upgrade, packages, files = False, [], []
    for raw in run_sh.replace("\\\n", " ").splitlines():
        line = raw.strip()
        if line.startswith("#"):
            continue
        for segment in re.split(r"&&|\|\||;|\|", line):
            m = _PIP_CMD.match(segment.strip())
            if not m:
                continue
            try:
                tokens = shlex.split(m.group("args"), comments=True)
            except ValueError:
                tokens = m.group("args").split()
            wants_upgrade = any(o in ("-U", "--upgrade") for o in m.group("opts").split())
            skip_next = take_file = False
            for tok in tokens:
                if skip_next:
                    skip_next = False
                elif take_file:
                    files.append(tok)
                    take_file = False
                elif tok in ("-r", "--requirement"):
                    take_file = True
                elif tok in ("-U", "--upgrade"):
                    wants_upgrade = True
                elif _REDIRECT.match(tok):
                    skip_next = tok in (">", ">>", "1>", "2>", "2>>", "&>", "<")
                elif tok.startswith("-"):
                    skip_next = tok in _OPTION_WITH_VALUE
                elif tok.lower() == "pip":
                    upgrade = upgrade or wants_upgrade
                else:
                    packages.append(tok)
    return upgrade, packages, files


def _pip(args: list[str], timeout: int) -> tuple[bool, str]:
    """``python3 -m pip install`` *args*, retried with --break-system-packages
    where the image's Python is externally managed: (ok, output)."""
    out = ""
    for extra in ([], ["--break-system-packages"]):
        cmd = ["python3", "-m", "pip", "install", "-q", "--disable-pip-version-check"]
        try:
            result = subprocess.run(
                cmd + args + extra, capture_output=True, text=True, timeout=timeout
            )
        except subprocess.TimeoutExpired:
            return False, f"pip timed out after {timeout}s"
        out = (result.stdout or "") + (result.stderr or "")
        if result.returncode == 0:
            return True, out
        if "externally-managed-environment" not in out:
            return False, out
    return False, out


def _preinstall(archives: dict[str, tuple[str, dict[str, str]]], timeout: int) -> None:
    """Install what the run.sh files pip-install, before any agent code runs.

    Exits DOWNLOAD_FAILED_EXIT when pip cannot reach the package index (the
    run.sh files would fail the same way later). A package that fails to build
    with the index reachable is left to run.sh, as upstream runs it.
    """
    upgrade = False
    groups: list[list[str]] = []
    with tempfile.TemporaryDirectory(prefix="programbench-req-") as tmp:
        for branch, (run_sh, requirement_files) in archives.items():
            up, packages, files = _pip_requirements(run_sh)
            upgrade = upgrade or up
            group = list(packages)
            for name in files:
                found = [
                    text
                    for path, text in sorted(requirement_files.items())
                    if path == name or path.endswith("/" + name)
                ]
                if found:
                    local = Path(tmp) / f"{branch}-{len(groups)}.txt"
                    local.write_text(found[0])
                    group += ["-r", str(local)]
            if group and group not in groups:
                groups.append(group)
        steps = ([["--upgrade", "pip"]] if upgrade else []) + groups
        for args in steps:
            print(f"  pip install {' '.join(args)}", flush=True)
            ok, out = _pip(args, timeout)
            if ok:
                continue
            tail = " | ".join(out.strip().splitlines()[-3:])
            if out.startswith("pip timed out") or _PIP_NETWORK.search(out):
                _fail(
                    [
                        "ERROR: the hidden tests' pip requirements could not be "
                        f"installed from PyPI: pip install {' '.join(args)}: {tail}",
                        "ERROR: no reward written and the run is not scored: the "
                        "tests cannot run without them, which says nothing about "
                        "the submission. The verifier needs pypi.org and "
                        "files.pythonhosted.org in the task's [verifier] "
                        "allowed_hosts.",
                    ],
                    DOWNLOAD_FAILED_EXIT,
                )
            print(
                f"  WARNING: pip install {' '.join(args)} failed with the index "
                f"reachable; left to run.sh: {tail}",
                flush=True,
            )


def _pin_installed(directory: str) -> Path | None:
    """A pip constraints file pinning every distribution installed now, after
    Step 0. run.sh gets it as PIP_CONSTRAINT: it can install what's missing
    but can't upgrade what's there, so a later PyPI release (a new pytest
    that an installed plugin can't load) can't break the tests."""
    result = subprocess.run(
        ["python3", "-m", "pip", "list", "--format=freeze", "--disable-pip-version-check", "--exclude", "pip"],
        capture_output=True,
        text=True,
        timeout=120,
    )
    pins = [
        line.strip()
        for line in (result.stdout or "").splitlines()
        if re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*==\S+", line.strip())
    ]
    if result.returncode != 0 or not pins:
        return None
    path = Path(directory) / "constraints.txt"
    path.write_text("\n".join(pins) + "\n")
    return path


def _load_excluded(path: Path) -> dict[str, set[str]]:
    """Branch -> test cases not counted (they need hosts the verifier refuses).
    "*" marks a branch whose run.sh itself can't run without them (an apt or
    wget fetch under set -e): the branch isn't run or counted."""
    if not path.exists():
        return {}
    data = json.loads(path.read_text())
    return {branch: set(names) for branch, names in data.items()}


def _run_test_branch(
    workspace: Path,
    branch: str,
    blob_path: Path,
    stash: Path,
    excluded: set[str],
    constraints: Path | None,
) -> tuple[int, int] | None:
    """Run one test branch: (passed, total) over its counted test cases, or
    None when its tests reported no results."""
    try:
        subprocess.run(
            ["tar", "xzf", str(blob_path), "-C", str(workspace)],
            check=True,
            timeout=120,
        )
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as exc:
        print(f"  WARNING: failed to extract archive for branch {branch}: {exc}")
        return None

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
        env = dict(os.environ)
        if constraints is not None:
            env["PIP_CONSTRAINT"] = str(constraints)
        proc = subprocess.Popen(
            ["bash", str(run_sh)], cwd=str(workspace), start_new_session=True, env=env
        )
        try:
            proc.wait(timeout=3600)
        except subprocess.TimeoutExpired:
            print(f"  WARNING: test run timed out for branch {branch}")
        finally:
            _stop_leftovers(proc.pid, workspace, stash)
            proc.wait()

    # Parse results
    reported = 0
    passed = 0
    total = 0
    results_xml = workspace / "eval" / "results.xml"
    if results_xml.exists():
        try:
            raw = results_xml.read_text()
            root = ET.fromstring(raw)
            for tc in root.iter("testcase"):
                reported += 1
                name = tc.get("name", "")
                classname = tc.get("classname", "")
                if (f"{classname}.{name}" if classname else name) in excluded:
                    continue
                total += 1
                has_fail = any(
                    c.tag in ("failure", "error") for c in tc
                )
                if not has_fail:
                    passed += 1
        except ET.ParseError as exc:
            print(f"  WARNING: failed to parse results.xml: {exc}")
            reported = 0

    # Clean up test artifacts for next branch
    eval_dir = workspace / "eval"
    if eval_dir.exists():
        import shutil
        shutil.rmtree(eval_dir, ignore_errors=True)

    if reported == 0:
        return None
    return passed, total


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--instance-id", required=True)
    parser.add_argument("--workspace", required=True, type=Path)
    parser.add_argument("--clean-hashes", default="[]")
    parser.add_argument("--reward-file", required=True, type=Path)
    parser.add_argument("--tests-json", default="/tests/tests.json", type=Path)
    parser.add_argument(
        "--excluded-tests", default="/tests/excluded_tests.json", type=Path
    )
    parser.add_argument(
        "--stash-path", default="/opt/benchflow-stashed-executable", type=Path
    )
    parser.add_argument("--pip-timeout", default=900, type=int)
    parser.add_argument(
        "--scan-dirs",
        default="/tmp,/var/tmp,/dev/shm,/home",
        help="Where else the original binary is looked for (comma-separated)",
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
    excluded = _load_excluded(args.excluded_tests)
    active_branches = [
        name for name, info in branches.items() if not info.get("ignored")
    ]

    # Step 0: make the hidden tests ready before any of the agent's code runs.
    # A failure exits DOWNLOAD_FAILED_EXIT with no reward.
    print("=== Step 0: Downloading hidden tests ===", flush=True)
    blobs = _download_all(args.instance_id, active_branches)
    archives: dict[str, tuple[str, dict[str, str]]] = {}
    for branch in active_branches:
        try:
            archives[branch] = _archive_contents(blobs[branch])
        except ValueError as exc:
            local = _local_cause(exc)
            where = f"on this machine ({local})" if local else "as downloaded"
            _fail(
                [
                    f"ERROR: hidden-test archive for {args.instance_id} branch "
                    f"{branch} is unusable {where}: {exc}",
                    "ERROR: no reward written and the run is not scored: the "
                    "hidden tests are unavailable, which says nothing about the "
                    "submission.",
                ],
                DOWNLOAD_FAILED_EXIT,
            )
    _preinstall(archives, args.pip_timeout)
    constraints = _pin_installed(tempfile.mkdtemp(prefix="programbench-pins-"))

    # Step 1: Remove hash-matched files from submission (anti-cheat).
    # Must happen BEFORE compile — matches ProgramBench's eval order.
    # The hashes identify the original pre-compiled binary; removing them
    # before compile prevents trivial copies while allowing a legitimate
    # rebuild that happens to produce a byte-identical executable.
    print("=== Step 1: Checking for copied binaries ===")
    scan = [args.workspace] + [Path(d) for d in args.scan_dirs.split(",") if d]
    _remove_hashed_files(scan, clean_hashes)

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
        if "*" in excluded.get(branch, set()):
            print("    not run: its run.sh needs hosts the verifier refuses")
            continue
        result = _run_test_branch(
            args.workspace,
            branch,
            blobs[branch],
            stash,
            excluded.get(branch, set()),
            constraints,
        )
        if result is None and not branches[branch].get("tests"):
            # tests.json expects nothing from this branch: nothing to count.
            print("    the branch has no expected tests")
            continue
        if result is None:
            _fail(
                [
                    f"ERROR: branch {branch}'s tests reported no results: pytest "
                    "never ran or never finished (see the run.sh output above).",
                    "ERROR: no reward written and the run is not scored.",
                ],
                TESTS_DID_NOT_REPORT_EXIT,
            )
        passed, total = result
        total_passed += passed
        total_tests += total
        print(f"    {passed}/{total} tests passed")

    # Step 5: Compute reward
    reward = total_passed / total_tests if total_tests > 0 else 0.0
    reward_file.write_text(f"{reward:.6f}")
    print(f"\n=== Result: {total_passed}/{total_tests} = {reward:.4f} ===")


if __name__ == "__main__":
    main()
