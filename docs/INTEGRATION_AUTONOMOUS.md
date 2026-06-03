# Integration with /autonomous Phase 6 (Harden & Verify)

**auton-gate** provides the *mechanical* half of the Production Readiness Gate. It is **not** a replacement for the verifier subagent or 0-issue design/security review.

## Phase 6 Subroutine (normative, from DESIGN.md)

After code changes + reviews land (and CI green):

1. **6.1** Run the gate (orchestrator):
   ```bash
   auton-gate check "$REPO_ROOT" \
     --auton-id "$AUTON_ID" \
     --checklist ~/.grok/skills/autonomous/docs/PRODUCTION_CHECKLIST.md \
     --profile <cli|lib|service>
   ```
   - Use `--strict` in CI contexts if desired (OQ-3).
   - `--no-git-check` only for special snapshot runs.

2. **6.2** If exit **1** (FAIL or strict+manuals): loop fixes (implementer subagent or human) → re-run 6.1 until mechanical exit **0**.

3. **6.3** Persist artifacts (orchestrator):
   - Update `~/.grok/auton-projects/<id>.json` under `artifacts`:
     ```json
     "gate_report_md": "/abs/path/GATE_REPORT.md",
     "gate_report_json": "/abs/path/gate_report.json",
     "gate_mechanical_verdict": "MECHANICAL_PASS",
     "gate_checklist_sha256": "..."
     ```

4. **6.4** Optional: `/check-work` for session gaps (does **not** replace checklist).

5. **6.5** security-auditor persona for §5 MANUAL items (or full §5 on high-risk).

6. **6.6** Verifier subagent:
   - Read full state + synthesis + DESIGN + PLAN + both gate reports + git/CI.
   - Re-execute build/test/lint commands yourself (trust-but-verify).
   - Mark every applicable checklist item with evidence.
   - Output production gate report containing **`VERDICT: PASS`** (or FAIL + precise list).

7. **6.7** If verifier FAIL: fix loop → return to 6.1.

**Never** advance to Phase 7 or declare "production ready" on `auton-gate` exit 0 alone. The mechanical gate only clears the automatable strict items (build, tests, secrets) and surfaces the rest.

## Tailoring & Profiles

- `cli` (default): §9/10 largely SKIP or minimal; §1/2/11/12 partial.
- `lib`: emphasize packaging/README/lockfiles.
- `service`: more MANUAL on deploy/ops (v1).

Always document tailoring in the final verifier gate report (per PRODUCTION_CHECKLIST.md:125).

## Report Semantics

- `GATE_REPORT.md` top banner **always** reminds it is mechanical only.
- `VERDICT: MECHANICAL_PASS` in report + exit 0 = ready for verifier.
- `VERDICT: FAIL` + exit 1 = strict section (s03/s04/s05.03) broken; must fix before verifier.
- Unregistered / manual bullets surface as `MANUAL_REVIEW_REQUIRED` (verifier adjudicates).

## Self-dogfood

After B-T12:
```bash
pip install -e .
auton-gate check .
```
Must exit 0 (mechanical) on the `auton-gate` tree itself. The full production gate (verifier + 0 issues) happens in the autonomous run's Phase 6.

## Post-PASS Ecosystem (E-1 / E-2)

- Patch `~/.grok/skills/autonomous/SKILL.md` (Phase 6 text) to reference steps 6.1–6.7 and `auton-gate`.
- Patch `USAGE.md` to distinguish mechanical vs production `VERDICT: PASS`.
- Optional: one-line in symbiosis cross-device instructions.

## References

- `docs/DESIGN.md` (architecture, verdict table, Phase 6 subroutine)
- `docs/PLAN.md` (B-T* tasks, V5 dogfood target)
- `docs/CHECKLIST_MAPPING_v1.md` (check_id → bullet)
- `~/.grok/skills/autonomous/docs/PRODUCTION_CHECKLIST.md` (canonical 12 sections)
- `~/.grok/skills/autonomous/SKILL.md` (orchestrator contract)

Use `auton-gate explain <check-id>` during fix loops for hints.

**Exact prime**: only declare production ready on full verifier `VERDICT: PASS` + 0 open issues.
