"""CLI entry for auton-gate (stub for bootstrap)."""

import typer
from pathlib import Path

app = typer.Typer(help="Mechanical Production Readiness Gate for /autonomous (ee70444d selection)")

@app.command()
def check(
    path: Path = typer.Argument(..., exists=True, file_okay=False, dir_okay=True, help="Project root to gate"),
    auton_id: str = typer.Option(None, "--auton-id", help="Link to ~/.grok/auton-projects/<id>.json"),
    checklist: Path = typer.Option(None, "--checklist", help="Path to PRODUCTION_CHECKLIST.md (default canonical)"),
    profile: str = typer.Option("cli", "--profile", help="cli|lib|service (tailors skips)"),
    strict: bool = typer.Option(False, "--strict", help="Treat more items as blocking for this tree"),
):
    """Run mechanical checks. Exit 0 = MECHANICAL_PASS (see banner); full production requires autonomous verifier."""
    typer.echo(f"[STUB] auton-gate check {path} --auton-id={auton_id} --profile={profile}")
    typer.echo("MECHANICAL GATE ONLY — not a substitute for autonomous verifier VERDICT: PASS + 0-issue design review.")
    typer.echo("See docs/DESIGN.md and the full PRODUCTION_CHECKLIST.md.")
    # In real impl: return code 0 for mechanical clean, 1 for FAILs, 2 for errors.
    raise SystemExit(0)

@app.command()
def explain(check_id: str):
    """Explain a check id (e.g. s03.01) and remediation."""
    typer.echo(f"[STUB] explain {check_id}")

if __name__ == "__main__":
    app()
