"""§7 README (s07.01 core sections heuristic; others manual)."""


from ..config import ProjectContext
from .base import CheckResult, Status, make_result, register

CORE_HEADINGS = [
    "quickstart", "installation", "usage", "configuration", "examples",
    "testing", "development", "contributing", "license", "production",
]


@register("s07.01.readme_core_sections", section=7, bullet=1, automatable="partial")
def s07_01_readme(ctx: ProjectContext) -> CheckResult:
    root = ctx.project_path
    readme = None
    for cand in ["README.md", "README.rst", "readme.md", "Readme.md"]:
        p = root / cand
        if p.exists():
            readme = p
            break
    if not readme:
        return make_result(
            "s07.01.readme_core_sections",
            Status.FAIL,
            "No README.* found",
            {"present": False},
            "partial",
        )
    txt = readme.read_text(errors="ignore").lower()
    found = [h for h in CORE_HEADINGS if h in txt]
    # Require at least 3 core-ish for partial PASS heuristic
    status = Status.PASS if len(found) >= 3 else Status.MANUAL_REVIEW_REQUIRED
    return CheckResult(
        check_id="s07.01.readme_core_sections",
        section=7,
        bullet=1,
        status=status,
        automatable="partial",
        evidence={"readme": str(readme.name), "found_headings": found, "count": len(found)},
        message=f"README has {len(found)}/core headings (heuristic)",
    )
