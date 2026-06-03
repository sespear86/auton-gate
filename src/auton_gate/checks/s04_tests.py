"""§4 Testing checks (s04.05 full; partial heuristics for others)."""

from __future__ import annotations

from ..config import ProjectContext
from ..detector import detect_stack, get_default_check_cmd
from ..runner import safe_run_cmd
from .base import CheckResult, Status, make_result, register


def _truncate(text: str, max_len: int = 2000) -> str:
    if len(text) <= max_len:
        return text
    return text[:max_len] + "\n... [truncated]"


@register("s04.05.test_suite", section=4, bullet=5, automatable="full")
def s04_05_test_suite(ctx: ProjectContext) -> CheckResult:
    ds = detect_stack(ctx.project_path)
    cmd = get_default_check_cmd(ds, "test")
    if not cmd:
        return make_result(
            "s04.05.test_suite",
            Status.MANUAL_REVIEW_REQUIRED,
            f"No test command for stack={ds.primary}",
            {"detected_stack": ds.primary},
            "full",
        )
    proc = safe_run_cmd(cmd, ctx.project_path, ctx.timeout)
    status = Status.PASS if proc.returncode == 0 else Status.FAIL
    # naive summary parse
    summary = ""
    for line in (proc.stdout or "").splitlines() + (proc.stderr or "").splitlines():
        if "passed" in line.lower() or "failed" in line.lower() or "error" in line.lower():
            summary = line.strip()
            break
    evidence = {
        "command": cmd,
        "exit_code": proc.returncode,
        "stdout": _truncate(proc.stdout or ""),
        "stderr": _truncate(proc.stderr or ""),
        "summary": summary or "no summary line",
        "stack": ds.primary,
    }
    msg = f"test_suite {'passed' if status == Status.PASS else 'failed'}"
    return CheckResult(
        check_id="s04.05.test_suite",
        section=4,
        bullet=5,
        status=status,
        automatable="full",
        evidence=evidence,
        message=msg,
    )


# Partial heuristics for other §4 bullets (per Appendix A: partial/manual)
@register("s04.01.unit_tests", section=4, bullet=1, automatable="partial")
def s04_01_unit(ctx: ProjectContext) -> CheckResult:
    has_test_dir = (ctx.project_path / "tests").is_dir() or (ctx.project_path / "test").is_dir()
    has_test_files = len(list(ctx.project_path.rglob("test_*.py"))) + len(list(ctx.project_path.rglob("*_test.py"))) > 0
    if has_test_dir or has_test_files:
        return make_result(
            "s04.01.unit_tests",
            Status.MANUAL_REVIEW_REQUIRED,
            "Test files/dirs present; manual review for coverage of happy/error/boundary per checklist",
            {"has_tests_dir": has_test_dir, "test_file_count": has_test_files},
            "partial",
        )
    return make_result(
        "s04.01.unit_tests",
        Status.MANUAL_REVIEW_REQUIRED,
        "No obvious test files; verify unit tests exist",
        {},
        "partial",
    )
