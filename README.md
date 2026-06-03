# auton-gate

Mechanical Production Readiness Gate CLI for the `/autonomous` skill.

**AUTON_ID that identified this as first test:** `ee70444d` (Washington Linux, 2026-06-03)

**Status:** Bootstrapped skeleton from identification run. See `docs/PLAN.md`, `docs/DESIGN.md`, `docs/RESEARCH_SYNTHESIS.md` (copied from the run that selected `auton-gate`).

## What it is

`auton-gate check <path>` executes the *automatable* mechanical checks from `~/.grok/skills/autonomous/docs/PRODUCTION_CHECKLIST.md` (build, test, lint, secrets, lockfiles, CI presence, README heuristics, etc.), emits `GATE_REPORT.md` + JSON, and exits 0/1.

- **MECHANICAL_PASS only** — never substitutes for the full autonomous verifier subagent + 0-issue design review + security-auditor + human judgment on the full 12-section checklist.
- Designed to be called from autonomous Phase 6 before/during the verifier subagent.
- Dogfoods on itself.
- Supports `--auton-id` to link `~/.grok/auton-projects/<id>.json` (research/design paths, etc.).

## Quickstart (once implemented)

```bash
pip install -e .
auton-gate check .
# or with context from a prior autonomous run:
auton-gate check . --auton-id ee70444d
```

See `docs/INTEGRATION_AUTONOMOUS.md` (to be written in build) and the embedded `docs/DESIGN.md` for Phase 6.1–6.7 subroutine.

## Bootstrap note (from ee70444d)

This skeleton + the docs/ copies of synthesis/design/plan + .auton-starter.json were self-provisioned by the identification autonomous run so that a follow-on `/autonomous` (using the prompt in .auton-starter.json) has zero-ramp context and can focus thrust on implementation.

Target: after full build run, `pip install -e . && auton-gate check .` must exit 0 (mechanical) on the tree itself, with full `PRODUCTION_READY.md`.

## Next

Launch the real first test:

```
grok -p "/autonomous Build production-ready `auton-gate`: a Python CLI that implements the mechanical portions of ~/.grok/skills/autonomous/docs/PRODUCTION_CHECKLIST.md for an arbitrary project path, supports --auton-id linking to ~/.grok/auton-projects/<id>.json, emits GATE_REPORT.md + JSON + exit code, includes pytest fixtures, GitHub Actions CI, README with integration section for Phase 6 of the autonomous skill. New git repo at ~/auton-gate (not inside grok-hermes-symbiosis or grok-mempalace-integration). No paid hosting. Target: pip install -e . && auton-gate check . passes on self after implementation."
```

Or use the exact prompt from `~/.grok/auton-runs/ee70444d/` or the .auton-starter.json.

## Primes followed in identification

Bust a nut. 0 blue balls. Exact signatures in the run artifacts. Mirror later via Kumquat.

---

*Identified + bootstrapped by autonomous ee70444d. Production gate for this identification run to follow.*
