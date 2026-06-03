"""Language / stack / build command detector for project root.

Order of precedence (per DESIGN):
1. pyproject.toml -> python (ruff/pytest or make)
2. package.json -> node
3. Cargo.toml -> rust
4. Makefile -> generic make
5. Fallback: MANUAL_REVIEW_REQUIRED for build/test sections
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass
class DetectedStack:
    primary: str  # "python", "node", "rust", "unknown"
    manifest: str | None = None
    build_cmds: list[str] = None
    test_cmds: list[str] = None
    lint_cmds: list[str] = None
    has_lockfile: bool = False
    package_name: str | None = None


def _read_toml(path: Path) -> dict:
    try:
        # stdlib tomllib in 3.11+
        import tomllib
        with path.open("rb") as f:
            return tomllib.load(f)
    except Exception:
        return {}


def _read_json(path: Path) -> dict:
    try:
        import json
        return json.loads(path.read_text())
    except Exception:
        return {}


def detect_stack(root: Path) -> DetectedStack:
    root = root.resolve()
    ds = DetectedStack(primary="unknown", build_cmds=[], test_cmds=[], lint_cmds=[])

    pyproj = root / "pyproject.toml"
    if pyproj.exists():
        ds.primary = "python"
        ds.manifest = "pyproject.toml"
        data = _read_toml(pyproj)
        proj = data.get("project", {})
        ds.package_name = proj.get("name")
        # Prefer explicit scripts or make; default ruff + pytest for our stack
        if (root / "Makefile").exists():
            ds.build_cmds = ["make build"] if _has_make_target(root / "Makefile", "build") else []
            ds.test_cmds = ["make test"] if _has_make_target(root / "Makefile", "test") else ["make test"]
            ds.lint_cmds = ["make lint"] if _has_make_target(root / "Makefile", "lint") else ["make lint"]
        else:
            # Safe syntax "build" check for pure python (py_compile doesn't take dir well)
            ds.build_cmds = [
                "python -c \"import ast,pathlib;[ast.parse(p.read_text(errors='ignore')) for p in pathlib.Path('.').rglob('*.py') if '.venv' not in str(p) and 'site-packages' not in str(p)]\""
            ]
            ds.test_cmds = ["pytest -q"]
            ds.lint_cmds = ["ruff check ."]
        # lockfiles
        ds.has_lockfile = any((root / lf).exists() for lf in ["poetry.lock", "pdm.lock", "uv.lock", "requirements*.txt"])
        return ds

    pkgjson = root / "package.json"
    if pkgjson.exists():
        ds.primary = "node"
        ds.manifest = "package.json"
        data = _read_json(pkgjson)
        ds.package_name = data.get("name")
        scripts = data.get("scripts", {})
        if "build" in scripts:
            ds.build_cmds.append("npm run build")
        if "test" in scripts:
            ds.test_cmds.append("npm test")
        if "lint" in scripts:
            ds.lint_cmds.append("npm run lint")
        else:
            ds.lint_cmds.append("npx eslint . || true")
        ds.has_lockfile = (root / "package-lock.json").exists() or (root / "yarn.lock").exists() or (root / "pnpm-lock.yaml").exists()
        return ds

    cargo = root / "Cargo.toml"
    if cargo.exists():
        ds.primary = "rust"
        ds.manifest = "Cargo.toml"
        ds.build_cmds = ["cargo check"]
        ds.test_cmds = ["cargo test"]
        ds.lint_cmds = ["cargo clippy -- -D warnings || cargo clippy"]
        ds.has_lockfile = (root / "Cargo.lock").exists()
        return ds

    mk = root / "Makefile"
    if mk.exists():
        ds.primary = "make"
        ds.manifest = "Makefile"
        if _has_make_target(mk, "build"):
            ds.build_cmds.append("make build")
        if _has_make_target(mk, "test"):
            ds.test_cmds.append("make test")
        if _has_make_target(mk, "lint"):
            ds.lint_cmds.append("make lint")
        return ds

    # Fallback
    ds.primary = "unknown"
    return ds


def _has_make_target(makefile: Path, target: str) -> bool:
    try:
        txt = makefile.read_text(errors="ignore")
        return f"{target}:" in txt or f".PHONY: {target}" in txt
    except Exception:
        return False


def get_default_check_cmd(ds: DetectedStack, kind: str = "test") -> str | None:
    cmds = {
        "test": ds.test_cmds,
        "lint": ds.lint_cmds,
        "build": ds.build_cmds,
    }.get(kind, [])
    return cmds[0] if cmds else None
