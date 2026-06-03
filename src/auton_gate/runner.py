"""CheckRunner: executes registered checks (sequentially for v1, with timeout, safe subprocess)."""

from __future__ import annotations

import subprocess
import time
from pathlib import Path

from .config import ProjectContext
from .registry import REGISTRY, CheckResult, Status


def safe_run_cmd(cmd: str, cwd: Path, timeout: int) -> subprocess.CompletedProcess:
    """Run with shell=False (argv list) only. Public helper for checks."""
    import shlex
    argv = shlex.split(cmd)
    try:
        return subprocess.run(
            argv,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=timeout,
            shell=False,
        )
    except subprocess.TimeoutExpired as e:
        return subprocess.CompletedProcess(argv, 124, stdout=e.stdout or "", stderr=(e.stderr or "") + "\nTIMEOUT")
    except FileNotFoundError:
        return subprocess.CompletedProcess(argv, 127, "", f"command not found: {argv[0]}")


class CheckRunner:
    def __init__(self, ctx: ProjectContext):
        self.ctx = ctx
        self.results: list[CheckResult] = []

    def run_check(self, check_id: str) -> CheckResult:
        fn = REGISTRY.get(check_id)
        if fn is None:
            # Unknown -> manual
            res = CheckResult(
                check_id=check_id,
                section=int(check_id.split(".")[0][1:]) if check_id.startswith("s") else 0,
                bullet=int(check_id.split(".")[1]) if "." in check_id else 0,
                status=Status.MANUAL_REVIEW_REQUIRED,
                automatable="manual",
                message="check not implemented in this version",
            )
            self.results.append(res)
            return res

        start = time.time()
        try:
            res = fn(self.ctx)
        except Exception as e:
            res = CheckResult(
                check_id=check_id,
                section=0,
                bullet=0,
                status=Status.FAIL,
                message=f"check crashed: {e}",
                evidence={"exception": str(e)},
            )
        res.duration_ms = int((time.time() - start) * 1000)
        self.results.append(res)
        return res

    def run_all(self, check_ids: list[str] | None = None) -> list[CheckResult]:
        ids = check_ids or REGISTRY.all_ids()
        for cid in ids:
            self.run_check(cid)
        return self.results

    def has_strict_fail(self) -> bool:
        strict_prefixes = ("s03.", "s04.", "s05.03")  # build, tests, no_secrets per PLAN/DESIGN
        for r in self.results:
            if r.status == Status.FAIL and any(r.check_id.startswith(p) for p in strict_prefixes):
                return True
        return False
