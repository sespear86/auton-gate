"""Check registry: registers checks by check_id (sNN.MM.slug), runs them, supports stubs."""

from __future__ import annotations

import importlib
import pkgutil
from collections.abc import Callable
from dataclasses import dataclass, field
from enum import StrEnum

from .config import ProjectContext


class Status(StrEnum):
    PASS = "PASS"
    FAIL = "FAIL"
    SKIP = "SKIP"
    MANUAL_REVIEW_REQUIRED = "MANUAL_REVIEW_REQUIRED"


@dataclass
class CheckResult:
    check_id: str
    section: int
    bullet: int
    status: Status
    automatable: str = "partial"  # full | partial | manual | skip
    evidence: dict = field(default_factory=dict)
    duration_ms: int = 0
    message: str = ""


CheckFn = Callable[[ProjectContext], CheckResult]


class CheckRegistry:
    def __init__(self) -> None:
        self._checks: dict[str, CheckFn] = {}
        self._metadata: dict[str, dict] = {}  # check_id -> {section, bullet, automatable, ...}

    def register(
        self,
        check_id: str,
        section: int,
        bullet: int,
        automatable: str = "partial",
        fn: CheckFn | None = None,
    ) -> Callable[[CheckFn], CheckFn]:
        """Decorator or direct register."""
        def deco(fn: CheckFn) -> CheckFn:
            self._checks[check_id] = fn
            self._metadata[check_id] = {
                "section": section,
                "bullet": bullet,
                "automatable": automatable,
            }
            return fn
        if fn is not None:
            return deco(fn)
        return deco

    def get(self, check_id: str) -> CheckFn | None:
        return self._checks.get(check_id)

    def all_ids(self) -> list[str]:
        return sorted(self._checks.keys())

    def get_metadata(self, check_id: str) -> dict:
        return self._metadata.get(check_id, {})

    def load_builtin_checks(self) -> None:
        """Auto-discover checks in auton_gate.checks.* modules (import side effect registers)."""
        import auton_gate.checks  # noqa
        package = auton_gate.checks
        for _finder, name, _ispkg in pkgutil.iter_modules(package.__path__):
            if name.startswith("_"):
                continue
            importlib.import_module(f"{package.__name__}.{name}")


# Global default registry instance (populated at import of check modules)
REGISTRY = CheckRegistry()


def register(check_id: str, section: int, bullet: int, automatable: str = "partial"):
    """Module-level decorator using the global REGISTRY."""
    return REGISTRY.register(check_id, section, bullet, automatable)
