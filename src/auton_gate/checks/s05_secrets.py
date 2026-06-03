"""§5 Secrets (s05.03: no secrets in repo + .env not committed)."""

from __future__ import annotations

import re

from ..config import ProjectContext
from .base import CheckResult, Status, register

# High-signal secret patterns (case-insensitive where sensible). Keep conservative to avoid FPs.
SECRET_PATTERNS = [
    re.compile(r"(?i)(aws_?secret|aws_?access|secret_?key)\s*=\s*['\"]?[A-Za-z0-9/+=]{16,}"),
    re.compile(r"(?i)sk-[a-z0-9]{16,}"),  # openai etc
    re.compile(r"-----BEGIN (RSA |EC |)PRIVATE KEY-----"),
    re.compile(r"(?i)api_?key\s*[:=]\s*['\"]?[A-Za-z0-9_\-]{20,}"),
    re.compile(r"(?i)password\s*[:=]\s*['\"]?[^'\"\s]{8,}"),  # loose but in source files
    re.compile(r"ghp_[A-Za-z0-9]{20,}"),  # github pat
]

EXCLUDE_DIRS = {".git", ".venv", "node_modules", "__pycache__", "dist", "build", ".ruff_cache", ".pytest_cache", "tests"}
# Skip tests/ entirely for secret scan (our test vectors use temp dirs; committed code must never have secrets)
SECRET_EXCLUDE_SUBSTR = ["tests/"]


def _looks_like_secret(text: str) -> bool:
    for pat in SECRET_PATTERNS:
        if pat.search(text):
            return True
    return False


@register("s05.03.no_secrets_in_repo", section=5, bullet=3, automatable="full")
def s05_03_no_secrets(ctx: ProjectContext) -> CheckResult:
    root = ctx.project_path
    leaks: list[str] = []
    env_committed = False

    # Check for committed .env (bad; .env.example / .env.template ok)
    git_dir = root / ".git"
    if git_dir.exists():
        # Use git ls-files to see committed (fast, accurate)
        try:
            import subprocess
            res = subprocess.run(
                ["git", "ls-files", ".env", "*.env", ".*.env"],
                cwd=root, capture_output=True, text=True, timeout=10, shell=False
            )
            committed_envs = [line.strip() for line in res.stdout.splitlines() if line.strip()]
            for e in committed_envs:
                if not any(x in e.lower() for x in ["example", "template", "sample"]):
                    env_committed = True
                    leaks.append(f"committed .env-like: {e}")
        except Exception:
            pass  # fall to rglob
    if not git_dir.exists() or env_committed:
        # Fallback scan
        for p in root.rglob(".env*"):
            if any(part in EXCLUDE_DIRS for part in p.parts):
                continue
            name = p.name.lower()
            if name == ".env" or (name.startswith(".env.") and "example" not in name and "template" not in name):
                # If .git exists we already checked ls-files; here just flag presence if no .git or as extra
                if not (root / ".git").exists():
                    leaks.append(f".env file present (no git): {p.relative_to(root)}")

    # Scan source files for patterns
    for p in root.rglob("*"):
        if not p.is_file():
            continue
        pstr = str(p)
        if any(part in EXCLUDE_DIRS for part in p.parts):
            continue
        if any(sub in pstr for sub in SECRET_EXCLUDE_SUBSTR):
            continue
        if p.suffix.lower() not in {".py", ".js", ".ts", ".json", ".toml", ".yaml", ".yml", ".md", ".txt", ".sh", ".ini", ".cfg"}:
            continue
        try:
            txt = p.read_text(errors="ignore")
            if _looks_like_secret(txt):
                leaks.append(str(p.relative_to(root)))
        except Exception:
            pass

    if leaks:
        status = Status.FAIL
        msg = "Secrets or committed .env detected"
    else:
        status = Status.PASS
        msg = "No high-signal secrets or committed .env found"

    return CheckResult(
        check_id="s05.03.no_secrets_in_repo",
        section=5,
        bullet=3,
        status=status,
        automatable="full",
        evidence={"leaks": leaks[:10], "count": len(leaks), "env_committed": env_committed},
        message=msg,
    )
