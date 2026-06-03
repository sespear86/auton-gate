"""Check registry stub (populated in B-T2+)."""

from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Dict

@dataclass
class CheckResult:
    check_id: str
    passed: bool
    evidence: str
    severity: str = "mechanical"

CheckFn = Callable[[Path], CheckResult]

REGISTRY: Dict[str, CheckFn] = {}

def register(check_id: str):
    def deco(fn: CheckFn):
        REGISTRY[check_id] = fn
        return fn
    return deco

# Stubs for bootstrap (real in build PRs)
@register("s03.01")
def stub_build(path: Path) -> CheckResult:
    return CheckResult("s03.01", True, "STUB: would run detected build/lint", "mechanical")

def run_all(root: Path, profile: str = "cli") -> list[CheckResult]:
    return [fn(root) for fn in REGISTRY.values()]
