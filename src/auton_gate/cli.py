"""CLI entry for auton-gate (full per DESIGN/PLAN)."""

from __future__ import annotations

from pathlib import Path

import typer

from . import __version__
from .config import DEFAULT_CHECKLIST, load_config
from .registry import REGISTRY
from .reporter import ReportBuilder
from .runner import CheckRunner

app = typer.Typer(
    help="Mechanical Production Readiness Gate for /autonomous (ee70444d first test project)",
    add_completion=False,
)


def _load_registry_once() -> None:
    REGISTRY.load_builtin_checks()


@app.command()
def check(
    path: Path = typer.Argument(
        ..., exists=True, file_okay=False, dir_okay=True,
        help="Project root to gate (positional only)"
    ),
    auton_id: str | None = typer.Option(None, "--auton-id", help="Link to ~/.grok/auton-projects/<id>.json"),
    checklist: Path | None = typer.Option(None, "--checklist", help="Path to PRODUCTION_CHECKLIST.md"),
    profile: str = typer.Option("cli", "--profile", help="cli|lib|service (tailors skips)"),
    output_dir: Path | None = typer.Option(None, "--output-dir", help="Dir for GATE_REPORT.md + gate_report.json"),
    strict: bool = typer.Option(False, "--strict", help="Exit 1 if any MANUAL_REVIEW_REQUIRED remain"),
    no_git_check: bool = typer.Option(False, "--no-git-check", help="Skip §11 git status"),
    verbose: bool = typer.Option(False, "-v", "--verbose", help="More logs"),
    timeout: int = typer.Option(600, "--timeout", help="Per-command timeout seconds"),
    _format: str = typer.Option("both", "--format", help="md,json,both (ignored; always writes both)"),
):
    """Run mechanical checks against PATH. Emits GATE_REPORT.md + gate_report.json + exit code.

    Exit:
      0: MECHANICAL_PASS (no strict FAIL; --strict may still 1 on manuals)
      1: FAIL (strict section fail) or --strict + manuals
      2: usage / config error
    """
    _load_registry_once()
    try:
        ctx = load_config(
            project_path=path,
            auton_id=auton_id,
            checklist=checklist,
            profile=profile,
            output_dir=output_dir,
            strict=strict,
            no_git_check=no_git_check,
            verbose=verbose,
            timeout=timeout,
        )
    except Exception as e:
        typer.secho(f"Config error: {e}", fg=typer.colors.RED, err=True)
        raise SystemExit(2)

    runner = CheckRunner(ctx)
    results = runner.run_all()
    rb = ReportBuilder(ctx, results)
    md_path, json_path = rb.write()
    typer.echo(f"Wrote {md_path}")
    typer.echo(f"Wrote {json_path}")
    # Print verdict banner to stdout for CI/logs
    typer.echo("")
    typer.echo("---")
    typer.echo(f"**Mechanical verdict:** VERDICT: {rb.verdict}")
    if rb.verdict == "FAIL":
        typer.secho("Strict checks failed. See GATE_REPORT.md for details.", fg=typer.colors.RED, err=True)
    elif strict and any(r.status == "MANUAL_REVIEW_REQUIRED" for r in results):  # type: ignore
        typer.secho("MANUAL items present + --strict.", fg=typer.colors.YELLOW, err=True)
    raise SystemExit(rb.exit_code)


@app.command()
def explain(check_id: str):
    """Explain a check_id (e.g. s03.03.build_clean) and suggested remediation."""
    _load_registry_once()
    meta = REGISTRY.get_metadata(check_id) or {}
    hints = {
        "s03.03.build_clean": "Ensure your detected build/lint cmd (ruff check, make, npm run, cargo check) exits 0. Run it locally.",
        "s03.04.linters_pass": "Run the linter command shown in evidence until clean. Add to pre-commit if missing.",
        "s04.05.test_suite": "Make `pytest -q` (or equiv) exit 0. Add tests for new paths. Use real objects over heavy mocks.",
        "s05.03.no_secrets_in_repo": "Remove the leaked strings/keys. Use .env + .gitignore. Never commit real creds.",
        "s06.01.ci_config_present": "Add .github/workflows/ci.yml (or equiv) with at least lint+test job.",
        "s07.01.readme_core_sections": "Add the missing core headings (Quickstart, Config, Testing, etc).",
        "s08.01.lockfiles": "Commit your lockfile (poetry.lock / package-lock.json etc).",
        "s08.04.gitignore": "Add common ignores: __pycache__, .env, *.egg-info, node_modules, .venv, dist/.",
        "s11.01.commits_clear": "git commit or stash; use --no-git-check only for special cases.",
        "s12.01.production_ready_md": "Write PRODUCTION_READY.md (see autonomous skill) + pass --auton-id for full handoff checks.",
    }
    hint = hints.get(check_id, "See docs/CHECKLIST_MAPPING_v1.md and the full PRODUCTION_CHECKLIST.md for the bullet.")
    typer.echo(f"check_id: {check_id}")
    typer.echo(f"section: {meta.get('section')} bullet: {meta.get('bullet')} automatable: {meta.get('automatable')}")
    typer.echo(f"Remediation hint: {hint}")
    typer.echo("Full mapping + Phase 6: docs/INTEGRATION_AUTONOMOUS.md")


@app.command()
def version():
    """Version, pinned checklist, git sha if available."""
    _load_registry_once()
    import subprocess
    sha = ""
    try:
        res = subprocess.run(["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True, shell=False, timeout=5)
        if res.returncode == 0:
            sha = res.stdout.strip()
    except Exception:
        pass
    typer.echo(f"auton-gate {__version__}")
    typer.echo(f"default-checklist: {DEFAULT_CHECKLIST}")
    if sha:
        typer.echo(f"git: {sha}")
    typer.echo("See --help and docs/ for integration with /autonomous Phase 6.")


if __name__ == "__main__":
    app()
