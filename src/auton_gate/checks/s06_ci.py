"""§6 CI (s06.01 presence; partial for others)."""


from ..config import ProjectContext
from .base import CheckResult, Status, register


@register("s06.01.ci_config_present", section=6, bullet=1, automatable="full")
def s06_01_ci(ctx: ProjectContext) -> CheckResult:
    root = ctx.project_path
    ci_files = []
    # GitHub
    gh = root / ".github" / "workflows"
    if gh.exists():
        ci_files.extend([str(p.relative_to(root)) for p in gh.glob("*.yml")] + [str(p.relative_to(root)) for p in gh.glob("*.yaml")])
    # Others
    for cand in [".circleci/config.yml", ".gitlab-ci.yml", "Jenkinsfile", "azure-pipelines.yml", ".travis.yml"]:
        p = root / cand
        if p.exists():
            ci_files.append(cand)
    status = Status.PASS if ci_files else Status.FAIL
    return CheckResult(
        check_id="s06.01.ci_config_present",
        section=6,
        bullet=1,
        status=status,
        automatable="full",
        evidence={"ci_files": ci_files, "count": len(ci_files)},
        message=f"CI config present: {len(ci_files)} files" if ci_files else "No CI config found",
    )
