# AGENTS.md — auton-gate

This project was selected as the **first real test case for the `/autonomous` skill** (AUTON_ID `ee70444d`, research + design 2026-06-03).

## Core rules for any agent (human or LLM) working here

- Follow the autonomous production readiness contract: never claim PASS without the full gate (mechanical + verifier subagent 0 issues on design review + security + full checklist).
- Use the embedded `docs/PLAN.md` + `docs/DESIGN.md` as the source of truth for implementation order (B-T* tasks, merge strategy: serial for early checks).
- All code changes must be reviewable units. Prefer small PRs or worktree-isolated impl + mandatory reviewer to 0 issues.
- Self-dogfood: after CLI + reporter exist, every change must survive `auton-gate check .` (mechanical) before claiming progress.
- No secrets in tree. `shell=False` (list argv) for all subprocess in checks (contrast with legacy micro-autonomous-test.py).
- Python 3.11+, modern packaging, ruff + pytest.
- When in doubt during autonomous execution: re-read `docs/RESEARCH_SYNTHESIS.md` §5 criteria and §8 target, and the Phase 6 integration in DESIGN.

## For the build autonomous run

The prompt is in `.auton-starter.json` (or `docs/PLAN.md`).

Use worktrees for parallelizable B-T3–B-T6 after foundation.

After B-T12 (dogfood), the tree + this AGENTS must satisfy the gate for the build AUTON's Phase 6.

## References (local)

- `docs/RESEARCH_SYNTHESIS.md` — why auton-gate, evidence, excluded projects
- `docs/DESIGN.md` — full arch, API, integration, PR DAG
- `docs/PLAN.md` — tasks, gates V1–V6, verification commands
- `~/.grok/skills/autonomous/docs/PRODUCTION_CHECKLIST.md` — the source of truth this tool partially automates
- `~/.grok/auton-projects/ee70444d.json` — the identification run state

## Mirror / cross-device

After significant work or Kumquat: update the brother (Oregon) via the standard handoff + Mempalace + this repo sync. The CLI is pure Python + stdlib-adjacent; Windows parity should be trivial.

Bust a nut. Keep er goinnnn. Exact signature per prime when closing waves.
