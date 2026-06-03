# Changelog

## 0.1.0 (2026-06-03)

- Initial production-ready release of `auton-gate` (first `/autonomous` functional test project, AUTONs ee70444d identification + 021dbe8d build).
- `auton-gate check <path>` : mechanical execution of automatable PRODUCTION_CHECKLIST.md items (s03 build/lint, s04 tests, s05 secrets, s06 CI, s07 README, s08 lock/gitignore, s11 git, s12 handoff).
- `--auton-id` integration with `~/.grok/auton-projects/<id>.json`.
- Full reporter: `GATE_REPORT.md` (with mandatory MECHANICAL banner) + `gate_report.json` (schema 1.0).
- Exit codes + mechanical verdict semantics (FAIL on strict s03/s04/s05.03; MECHANICAL_PASS otherwise).
- `explain <check-id>`, `version`.
- pytest + fixtures (good_cli_py exits 0; bad vectors for secrets via temp).
- GitHub Actions CI (lint + test + smoke).
- Self-dogfood: `pip install -e . && auton-gate check .` exits 0.
- Docs: README quickstart, `docs/INTEGRATION_AUTONOMOUS.md` (Phase 6.1-6.7), `docs/CHECKLIST_MAPPING_v1.md`, `docs/DESIGN.md`/`PLAN.md` (embedded).
- Hardening: shell=False everywhere, path resolve, timeouts, no committed secrets.
- Mempalace projects/auton-gate drawer + state update.
- Patches to autonomous SKILL.md Phase 6 + USAGE.md (mechanical vs production).

See `PRODUCTION_READY.md`, `docs/PLAN.md`, `AGENTS.md`.
