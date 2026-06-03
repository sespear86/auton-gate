# PLAN — AUTON_ID `ee70444d` + `auton-gate` build

**Extracted from:** `DESIGN.md` (revised), PR Plan, validation gates V1–V6  
**Date:** 2026-06-03 (PT)

---

## Tracks

| Track | Owner | AUTON_ID | Outcome |
|-------|--------|----------|---------|
| **Meta** | Orchestrator / meta subagents | `ee70444d` | Identification docs PASS + handoff |
| **Build** | Next `/autonomous` run (new ID recommended) | TBD | `~/auton-gate` production-ready CLI |

---

## Validation gates

| Gate | Track | Verification command / criterion |
|------|-------|----------------------------------|
| **V1** | Meta | `test -f DESIGN.md && grep -q "Appendix A" DESIGN.md` |
| **V2** | Meta | `test -f PLAN.md` && PR DAG acyclic (this file) |
| **V3** | Meta | Verifier `GATE_REPORT.md` → production `VERDICT: PASS` with tailoring matrix |
| **V4** | Build | `cd ~/auton-gate && gh run list --limit 1` or local `ruff check && pytest` per PR |
| **V5** | Build | `pip install -e . && auton-gate check .`; exit 0 + mechanical banner |
| **V6** | Build | E-1 SKILL patch + Mempalace `projects/auton-gate` |

---

## Meta tasks (`ee70444d`)

| ID | Task | Owner | Deps | Verification |
|----|------|-------|------|--------------|
| M-T1 | Finalize DESIGN.md post-review | design-writer | Research | V1; `DESIGN_REVIEW.md` 0 open Med+ |
| M-T2 | Write PLAN.md (this file) | design-writer | M-T1 | V2 |
| M-T3 | Create `starter-auton-gate/.auton-starter.json` | orchestrator | M-T2 | `test -f starter-auton-gate/.auton-starter.json` |
| M-T4 | Meta Phase 6 verifier pass | verifier | M-T1, M-T2, M-T3 | V3; tailoring matrix in meta GATE_REPORT |
| M-T5 | Write `PRODUCTION_READY.md` (meta) | orchestrator | M-T4 | Resume + §11 prompt embedded |
| M-T6 | Mempalace drawer update (M-4) | orchestrator | M-T5 | `mempalace_search` or drawer lists artifact paths |
| M-T7 | Optional symbiosis blurb (M-5) | orchestrator | M-T5 | Diff in linux-instructions.md |

**State update after M-T2:** `current_phase` → `phase-4-bootstrap` or `phase-6-verify` per orchestrator; ensure `plan_path` points to this file.

**Meta Phase 6 commands (verifier):**

```bash
ls -la /tmp/grok-auton-artifacts-ee70444d/
python3 ~/.grok/skills/autonomous/scripts/verify-skill-structure.py
# Read DESIGN_REVIEW.md — confirm 0 open Medium/High
# Produce /tmp/grok-auton-artifacts-ee70444d/GATE_REPORT.md with tailoring matrix
```

---

## Build tasks (`auton-gate` — next `/autonomous`)

**Target repo:** `~/auton-gate`  
**Prompt:** `RESEARCH_SYNTHESIS.md` §11 (also in `starter-auton-gate/.auton-starter.json`)

| ID | PR | Task | Owner | Deps | Verification |
|----|-----|------|-------|------|--------------|
| B-T1 | 1 | Scaffold pyproject, `src/auton_gate`, CI skeleton, stub checks | implementer | — | `pip install -e .`; `pytest`; `ruff check` |
| B-T2 | 2 | Core: config, detector, registry, runner; **STUB** checks | implementer | B-T1 | `pytest tests/test_registry.py` |
| B-T3 | 3 | Checks §3–4 + `docs/CHECKLIST_MAPPING_v1.md` | implementer | B-T2 | Unit tests per module |
| B-T4 | 4 | Checks §5, §8 | implementer | B-T2 | Fixture `bad_secrets` fails s05.03 |
| B-T5 | 5 | Checks §6–7 | implementer | B-T2 | CI/README fixtures |
| B-T6 | 6 | Checks §11–12 + `--auton-id` | implementer | B-T2 | Integration test with temp auton json |
| B-T7 | 7 | Reporter + mechanical verdict banner | implementer | B-T3–B-T6 merged | Golden `GATE_REPORT.md` test |
| B-T8 | 8 | CLI `check`, `explain`, `version` (positional PATH only) | implementer | B-T7 | `auton-gate check tests/fixtures/good_cli_py` |
| B-T9 | 9 | Fixtures + README quickstart | implementer | B-T8 | README commands copy-paste |
| B-T10 | 10 | `docs/INTEGRATION_AUTONOMOUS.md` (Phase 6 steps 6.1–6.7) | implementer | B-T9 | Doc review |
| B-T11 | 11 | Harden: timeouts, path safety, `shell=False` | implementer | B-T8 | Security review vs micro-test |
| B-T12 | 12 | Dogfood + `PRODUCTION_READY.md` | orchestrator | B-T11 | V5: `auton-gate check .` exit 0 |
| B-T13 | E-1 | Patch `~/.grok/skills/autonomous/SKILL.md` Phase 6 | implementer | B-T12 | V6 |
| B-T14 | E-2 | Patch `USAGE.md` mechanical vs production | implementer | B-T13 | Grep link auton-gate |

**Merge strategy:** Serial merge PRs 3→6 on main (or integration branch) before B-T7; CI e2e `auton-gate check` only after B-T7 (see DESIGN PR Plan).

**Build Phase 6 commands:**

```bash
auton-gate check "$REPO_ROOT" --auton-id "$AUTON_ID" \
  --checklist ~/.grok/skills/autonomous/docs/PRODUCTION_CHECKLIST.md
# exit 0 => MECHANICAL_PASS only; then verifier subagent for production VERDICT: PASS
```

---

## Dependency graph (build)

```
B-T1 → B-T2 → B-T3 ─┐
              → B-T4 ─┼→ B-T7 → B-T8 → B-T9 → B-T10 → B-T11 → B-T12 → B-T13 → B-T14
              → B-T5 ─┤
              → B-T6 ─┘
```

---

## Ops / infra

| Task | Owner | When |
|------|-------|------|
| GHA `ci.yml` lint+test | implementer | B-T1 |
| Optional GHA `strict` job (`--strict`) | implementer | B-T11 (OQ-3: on in CI only) |
| pr-babysit first PR stack | orchestrator | After GitHub push |
| Mempalace `projects/auton-gate` | orchestrator | B-T12 |

---

## References

- `DESIGN.md` — architecture, Appendix A, Phase 6 subroutine
- `DESIGN_REVIEW.md` — review closure
- `~/.grok/skills/autonomous/docs/PRODUCTION_CHECKLIST.md`