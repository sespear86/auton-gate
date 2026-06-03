"""Bootstrap tests for auton-gate skeleton."""

import subprocess
import sys
from pathlib import Path

def test_cli_help():
    # Once installed in env or via python -m
    # For bootstrap, just import smoke
    from auton_gate import cli
    assert hasattr(cli, "app")

def test_stub_check_runs_without_crashing(tmp_path: Path):
    # Run the stub module directly
    res = subprocess.run(
        [sys.executable, "-m", "auton_gate.cli", "check", str(tmp_path)],
        capture_output=True, text=True
    )
    # Stub always exits 0 with banner
    assert "MECHANICAL GATE ONLY" in res.stdout
    assert res.returncode == 0
