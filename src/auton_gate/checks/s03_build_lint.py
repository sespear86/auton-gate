"""§3 Code Quality checks (§3.03 build, §3.04 linters)."""

from __future__ import annotations

from ..config import ProjectContext
from ..detector import detect_stack, get_default_check_cmd
from ..runner import safe_run_cmd
from .base import CheckResult, Status, make_result, register


def _truncate(text: str, max_len: int = 2000) -> str:
    if len(text) <= max_len:
        return text
    return text[:max_len] + "\n... [truncated]"


def _run_check_cmd(ctx: ProjectContext, kind: str, check_id: str, section: int, bullet: int) -> CheckResult:
    ds = detect_stack(ctx.project_path)
    cmd = get_default_check_cmd(ds, kind)
    if not cmd:
        return make_result(
            check_id,
            Status.MANUAL_REVIEW_REQUIRED,
            f"No {kind} command detected for stack={ds.primary} (manifest={ds.manifest})",
            {"detected_stack": ds.primary, "manifest": ds.manifest},
            "full",
        )
    proc = safe_run_cmd(cmd, ctx.project_path, ctx.timeout)
    status = Status.PASS if proc.returncode == 0 else Status.FAIL
    evidence = {
        "command": cmd,
        "exit_code": proc.returncode,
        "stdout": _truncate(proc.stdout or ""),
        "stderr": _truncate(proc.stderr or ""),
        "stack": ds.primary,
    }
    msg = f"{kind} {'passed' if status == Status.PASS else 'failed'} (exit={proc.returncode})"
    return CheckResult(
        check_id=check_id,
        section=section,
        bullet=bullet,
        status=status,
        automatable="full",
        evidence=evidence,
        message=msg,
    )


@register("s03.03.build_clean", section=3, bullet=3, automatable="full")
def s03_03_build_clean(ctx: ProjectContext) -> CheckResult:
    return _run_check_cmd(ctx, "build", "s03.03.build_clean", 3, 3)


@register("s03.04.linters_pass", section=3, bullet=4, automatable="full")
def s03_04_linters(ctx: ProjectContext) -> CheckResult:
    return _run_check_cmd(ctx, "lint", "s03.04.linters_pass", 3, 4)
