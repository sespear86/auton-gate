"""§8 Packaging/lockfiles (s08.01, s08.04)."""


from ..config import ProjectContext
from .base import CheckResult, Status, make_result, register

LOCKFILE_NAMES = [
    "poetry.lock", "pdm.lock", "uv.lock", "Pipfile.lock",
    "package-lock.json", "yarn.lock", "pnpm-lock.yaml",
    "Cargo.lock", "Gemfile.lock", "go.sum",
]


@register("s08.01.lockfiles", section=8, bullet=1, automatable="full")
def s08_01_lock(ctx: ProjectContext) -> CheckResult:
    root = ctx.project_path
    found = [lf for lf in LOCKFILE_NAMES if (root / lf).exists()]
    # Also check for requirements*.txt as weak lock for pure pip (but prefer real locks)
    reqs = list(root.glob("requirements*.txt")) + list(root.glob("requirements/*.txt"))
    has_any = bool(found) or bool(reqs)
    # For python projects with pyproject, prefer modern lock; but any lock or reqs counts for v1
    status = Status.PASS if has_any else Status.FAIL
    msg = f"lockfiles present: {found or 'none'}{' + reqs' if reqs else ''}"
    return CheckResult(
        check_id="s08.01.lockfiles",
        section=8,
        bullet=1,
        status=status,
        automatable="full",
        evidence={"found_locks": found, "reqs_count": len(reqs)},
        message=msg,
    )


@register("s08.04.gitignore", section=8, bullet=4, automatable="full")
def s08_04_gitignore(ctx: ProjectContext) -> CheckResult:
    gi = ctx.project_path / ".gitignore"
    if not gi.exists():
        return make_result(
            "s08.04.gitignore",
            Status.FAIL,
            ".gitignore missing",
            {"present": False},
            "full",
        )
    txt = gi.read_text(errors="ignore").lower()
    required_hints = ["__pycache__", ".env", "*.egg-info", "node_modules", ".venv", "dist", "build"]
    missing = [h for h in required_hints if h not in txt]
    status = Status.PASS if not missing else Status.FAIL
    return CheckResult(
        check_id="s08.04.gitignore",
        section=8,
        bullet=4,
        status=status,
        automatable="full",
        evidence={"present": True, "missing_hints": missing, "size": len(txt)},
        message=".gitignore present" + (f" (missing hints: {missing})" if missing else ""),
    )
