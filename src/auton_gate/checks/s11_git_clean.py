"""§11 Git hygiene (s11.01 partial: clean tree or clear status)."""

import subprocess

from ..config import ProjectContext
from .base import CheckResult, Status, make_result, register


@register("s11.01.commits_clear", section=11, bullet=1, automatable="partial")
def s11_01_git(ctx: ProjectContext) -> CheckResult:
    if ctx.no_git_check:
        return make_result(
            "s11.01.commits_clear",
            Status.SKIP,
            "skipped via --no-git-check",
            {"skipped": True},
            "partial",
        )
    root = ctx.project_path
    if not (root / ".git").exists():
        return make_result(
            "s11.01.commits_clear",
            Status.MANUAL_REVIEW_REQUIRED,
            "no .git dir; cannot verify commits",
            {"has_git": False},
            "partial",
        )
    try:
        res = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=root, capture_output=True, text=True, timeout=min(30, ctx.timeout), shell=False
        )
        dirty = res.stdout.strip()
        if res.returncode != 0:
            return make_result("s11.01.commits_clear", Status.MANUAL_REVIEW_REQUIRED, "git status failed", {"rc": res.returncode}, "partial")
        if not dirty:
            status = Status.PASS
            msg = "working tree clean"
        else:
            status = Status.FAIL
            msg = "dirty tree (uncommitted changes)"
        return CheckResult(
            check_id="s11.01.commits_clear",
            section=11,
            bullet=1,
            status=status,
            automatable="partial",
            evidence={"porcelain": dirty[:500], "lines": len(dirty.splitlines()) if dirty else 0},
            message=msg,
        )
    except Exception as e:
        return make_result("s11.01.commits_clear", Status.MANUAL_REVIEW_REQUIRED, f"git check error: {e}", {}, "partial")
