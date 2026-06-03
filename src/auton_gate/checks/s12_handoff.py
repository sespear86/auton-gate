"""§12 Handoff (s12.01 PRODUCTION_READY.md + auton state; s12.02 partial)."""


from ..config import ProjectContext
from .base import CheckResult, Status, make_result, register


@register("s12.01.production_ready_md", section=12, bullet=1, automatable="full")
def s12_01_prod_ready(ctx: ProjectContext) -> CheckResult:
    root = ctx.project_path
    prod_md = root / "PRODUCTION_READY.md"
    has_md = prod_md.exists()
    # If auton_id, also require state loaded without _error
    auton_ok = True
    if ctx.auton_id:
        st = ctx.auton_state or {}
        auton_ok = "_error" not in st and bool(st.get("auton_id"))
    status = Status.PASS if (has_md and auton_ok) else (Status.MANUAL_REVIEW_REQUIRED if has_md else Status.FAIL)
    ev = {
        "production_ready_md": has_md,
        "auton_id": ctx.auton_id,
        "auton_state_ok": auton_ok,
        "auton_state_keys": list((ctx.auton_state or {}).keys())[:5] if ctx.auton_id else [],
    }
    msg = "PRODUCTION_READY.md present" + (" + auton state linked" if ctx.auton_id and auton_ok else "")
    if not has_md:
        msg = "PRODUCTION_READY.md missing"
    elif ctx.auton_id and not auton_ok:
        msg = "PRODUCTION_READY.md present but auton state load failed or missing"
    return CheckResult(
        check_id="s12.01.production_ready_md",
        section=12,
        bullet=1,
        status=status,
        automatable="full",
        evidence=ev,
        message=msg,
    )


@register("s12.02.mempalace_indexed", section=12, bullet=2, automatable="partial")
def s12_02_mempalace(ctx: ProjectContext) -> CheckResult:
    st = ctx.auton_state or {}
    has_drawer = bool(st.get("mempalace_drawer"))
    status = Status.PASS if has_drawer else Status.MANUAL_REVIEW_REQUIRED
    return make_result(
        "s12.02.mempalace_indexed",
        status,
        "mempalace_drawer in auton state" if has_drawer else "no mempalace_drawer (check state or run with --auton-id)",
        {"drawer": st.get("mempalace_drawer")},
        "partial",
    )
