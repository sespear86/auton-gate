"""Tests for CLI entry (updated post-stub)."""

import subprocess
import sys
from pathlib import Path


def test_cli_help():
    # Once installed in env or via python -m
    from auton_gate import cli
    assert hasattr(cli, "app")


def test_check_runs_and_emits_verdict(tmp_path: Path):
    """Real CLI check runs (B-T7+), emits report files or stdout verdict. Accepts 0/1 for clean/strict cases."""
    # Make a minimal "good enough" tree to avoid hard FAILs on strict checks
    (tmp_path / "pyproject.toml").write_text('[project]\nname = "t"\n')
    (tmp_path / ".gitignore").write_text("__pycache__/\n.env\n*.egg-info/\n.venv/\n")
    gh = tmp_path / ".github" / "workflows"
    gh.mkdir(parents=True)
    (gh / "ci.yml").write_text("name: CI\non: [push]\njobs:\n  test:\n    runs-on: ubuntu-latest\n")
    (tmp_path / "README.md").write_text("# t\n\n## Quickstart\n## Usage\n## Testing\n## Production\n")
    (tmp_path / "tests").mkdir()
    (tmp_path / "tests" / "test_t.py").write_text("def test_ok(): assert 1+1==2\n")
    res = subprocess.run(
        [sys.executable, "-m", "auton_gate.cli", "check", str(tmp_path)],
        capture_output=True, text=True, cwd=tmp_path
    )
    out = (res.stdout or "") + (res.stderr or "")
    assert "Mechanical verdict" in out or "VERDICT:" in out
    assert res.returncode in (0, 1)  # 0 mechanical pass or 1 on manuals/strict
    # Also check report was written next to cwd or default
    assert (tmp_path / "GATE_REPORT.md").exists() or "Wrote" in out
