"""Base types and helpers for check implementations. Shared across s*.py modules."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from ..registry import CheckResult, Status, register  # re-export for check modules


def make_result(
    check_id: str,
    status: Status,
    message: str = "",
    evidence: dict[str, Any] | None = None,
    automatable: str = "partial",
) -> CheckResult:
    """Helper to build CheckResult; parse section/bullet from check_id sNN.MM.name"""
    parts = check_id.split(".")
    section = int(parts[0][1:]) if parts and parts[0].startswith("s") else 0
    bullet = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 0
    return CheckResult(
        check_id=check_id,
        section=section,
        bullet=bullet,
        status=status,
        automatable=automatable,
        message=message,
        evidence=evidence or {},
    )


def file_exists(root: Path, *names: str) -> bool:
    return any((root / n).exists() for n in names)


def count_files(root: Path, pattern: str) -> int:
    return len(list(root.rglob(pattern)))


# Re-export register for convenience in check modules: from .base import register
register = register
Status = Status
CheckResult = CheckResult
