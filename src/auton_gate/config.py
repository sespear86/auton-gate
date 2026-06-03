"""Configuration loader, profile rules, auton-id state integration."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

DEFAULT_CHECKLIST = Path("~/.grok/skills/autonomous/docs/PRODUCTION_CHECKLIST.md").expanduser()


@dataclass
class ProjectContext:
    """Context for a gate run against a project path."""
    project_path: Path
    profile: str = "cli"
    auton_id: str | None = None
    auton_state: dict[str, Any] = field(default_factory=dict)
    checklist_path: Path = DEFAULT_CHECKLIST
    checklist_sha256: str | None = None
    output_dir: Path = Path(".")
    strict: bool = False
    no_git_check: bool = False
    verbose: bool = False
    timeout: int = 600  # seconds per command


PROFILE_SKIP_RULES: dict[str, dict[str, str]] = {
    # section prefix -> rule: SKIP | MANUAL | run
    "cli": {
        "s01": "MANUAL",
        "s02": "MANUAL",
        "s09": "SKIP",
        "s10": "SKIP",  # except logging handled in checks
    },
    "lib": {
        "s01": "MANUAL",
        "s02": "MANUAL",
        "s09": "SKIP",
    },
    "service": {
        "s01": "MANUAL",
        "s02": "MANUAL",
        "s09": "MANUAL",
        "s10": "MANUAL",
    },
}


def resolve_path(p: str | Path | None) -> Path | None:
    if p is None:
        return None
    return Path(p).expanduser().resolve()


def load_auton_state(auton_id: str | None) -> dict[str, Any]:
    """Load ~/.grok/auton-projects/<id>.json if provided. Read-only for gate."""
    if not auton_id:
        return {}
    state_path = Path("~/.grok/auton-projects").expanduser() / f"{auton_id}.json"
    if not state_path.exists():
        # Do not fail hard; report will note missing
        return {"_error": f"auton state not found at {state_path}"}
    try:
        with state_path.open() as f:
            return json.load(f)
    except Exception as e:
        return {"_error": f"failed to load auton state: {e}"}


def compute_checklist_hash(path: Path) -> str | None:
    if not path.exists():
        return None
    import hashlib
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()[:16]


def load_config(
    project_path: Path | str,
    auton_id: str | None = None,
    checklist: Path | str | None = None,
    profile: str = "cli",
    output_dir: Path | str | None = None,
    strict: bool = False,
    no_git_check: bool = False,
    verbose: bool = False,
    timeout: int = 600,
) -> ProjectContext:
    """Build ProjectContext, merge auton state, resolve paths, pin checklist hash."""
    proj = resolve_path(project_path)
    if proj is None or not proj.exists() or not proj.is_dir():
        raise ValueError(f"Project path must be existing directory: {project_path}")

    cl_path = resolve_path(checklist) if checklist else DEFAULT_CHECKLIST
    if not cl_path.exists():
        # Allow running without canonical, but record
        cl_path = cl_path  # still use, reporter will note

    auton_state = load_auton_state(auton_id)
    cl_hash = compute_checklist_hash(cl_path) if cl_path.exists() else None

    out_dir = resolve_path(output_dir) if output_dir else Path.cwd()

    ctx = ProjectContext(
        project_path=proj,
        profile=profile.lower().strip(),
        auton_id=auton_id,
        auton_state=auton_state,
        checklist_path=cl_path,
        checklist_sha256=cl_hash,
        output_dir=out_dir,
        strict=strict,
        no_git_check=no_git_check,
        verbose=verbose,
        timeout=timeout,
    )
    return ctx


def should_skip(ctx: ProjectContext, section: int) -> tuple[bool, str]:
    """Return (skip, reason_or_status) per profile rules + cli tailoring."""
    prefix = f"s{section:02d}"
    rules = PROFILE_SKIP_RULES.get(ctx.profile, {})
    rule = rules.get(prefix)
    if rule in ("SKIP", "MANUAL"):
        return True, rule
    # cli specific for §10 etc handled in individual checks
    return False, "run"
