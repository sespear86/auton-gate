"""auton_gate.checks package.

On import, submodules register their checks into the global REGISTRY via @register side effects.

For B-T2: only stubs. Real checks land in B-T3+ (serial merge).
"""

# Import stub modules so their @register run at package import time (B-T2)
from . import (  # noqa: F401
    base,  # noqa: F401
    s03_build_lint,
    s04_tests,
    s05_secrets,
    s06_ci,
    s07_readme,
    s08_lockfiles,
    s11_git_clean,
    s12_handoff,
)

# Real modules will replace the stub bodies in later tasks (no new files for early checks).
