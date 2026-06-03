# CHECKLIST_MAPPING_v1.md

**Source:** DESIGN.md Appendix A (normative for v1)  
**auton-gate version:** 0.1+  
**Purpose:** Stable `check_id` to `PRODUCTION_CHECKLIST.md` §N bullet mapping for reports, explain, Mempalace ingest. Unlisted bullets default to `MANUAL_REVIEW_REQUIRED`.

Normative `check_id` = `s{section:02d}.{bullet:02d}.{slug}`. Bullets match order in canonical `PRODUCTION_CHECKLIST.md`.

| § | Bul | check_id | Automatable | MVP module | Notes |
|---|-----|----------|-------------|------------|-------|
| 1 | 1–4 | s01.01–s01.04 | manual | — | Requirements/research |
| 2 | 1–4 | s02.01–s02.04 | manual | — | Design/planning |
| 3 | 3 | s03.03.build_clean | full | s03_build_lint | build command exit 0 |
| 3 | 4 | s03.04.linters_pass | full | s03_build_lint | ruff / eslint / clippy etc |
| 3 | 1–2,5–6 | s03.01–s03.02, s03.05–s03.06 | manual | — | 0-issues review, goldplating, conventions |
| 4 | 5 | s04.05.test_suite | full | s04_tests | runs detected; summary parse |
| 4 | 1–4,6–7 | s04.01–s04.04, s04.06–s04.07 | partial/manual | s04_tests (heuristics) | unit/integration/e2e presence + maintainability |
| 5 | 3 | s05.03.no_secrets_in_repo | full | s05_secrets | patterns + committed .env check |
| 5 | 1–2,4–7 | s05.01–s05.02, s05.04–s05.07 | manual | — | security-auditor |
| 6 | 1 | s06.01.ci_config_present | full | s06_ci | .github/workflows or equiv |
| 6 | 2–5 | s06.02–s06.05 | partial/manual | s06_ci | exercised, pr descs, babysit |
| 7 | 1 | s07.01.readme_core_sections | partial | s07_readme | headings heuristic |
| 7 | 2–5 | s07.02–s07.05 | manual/partial | s07_readme | examples, changelog, publish |
| 8 | 1 | s08.01.lockfiles | full | s08_lockfiles | committed lock |
| 8 | 4 | s08.04.gitignore | full | s08_lockfiles | .gitignore present + sensible |
| 8 | 2–3,5 | s08.02–s08.03, s08.05 | partial/manual | — | reproducible, versioning, multiplat |
| 9 | 1–7 | s09.* | SKIP cli/lib; manual service | v2 | infra/deploy |
| 10 | 1–7 | s10.* | SKIP cli except logging; manual | v2 | obs |
| 11 | 1 | s11.01.commits_clear | partial | s11_git_clean | git status or log |
| 11 | 2–6 | s11.02–s11.06 | manual | — | PR stack, no force etc |
| 12 | 1 | s12.01.production_ready_md | full (with --auton-id) | s12_handoff | looks for PRODUCTION_READY.md + auton json |
| 12 | 2 | s12.02.mempalace_indexed | partial | s12_handoff | state has drawer |
| 12 | 3–5 | s12.03–s12.05 | manual | verifier | hermes, cross-dev, schedulers |

**Implementation note:** Registered checks (via @register) are the source of truth for what is attempted; mapping doc is for humans/verifier subagent. Add new check_ids only with corresponding checklist update + version bump.

See DESIGN.md § Appendix A and `auton-gate explain <check-id>`.
