# RESEARCH_SYNTHESIS.md

**AUTON_ID:** `ee70444d`  
**Slug:** `identify-first-auton-test-project`  
**Date:** 2026-06-03 (PT)  
**Device:** Washington (Linux)  
**Artifact path:** `/tmp/grok-auton-artifacts-ee70444d/RESEARCH_SYNTHESIS.md`

---

## Executive Summary

**Recommended first `/autonomous` test project:** **`auton-gate`** (slug: `auton-gate`) — a **fresh, standalone Python CLI/library** that **mechanically executes** the autonomous skill’s **Production Readiness Gate** against any project workspace (and optionally an `AUTON_ID` state file), emitting a structured **`VERDICT: PASS|FAIL`** report with per-checklist-item evidence.

**Why it wins:** The autonomous orchestrator’s non-negotiable exit condition (Phase 6 / Phase 9) is a **verifier subagent + markdown checklist** (`PRODUCTION_CHECKLIST.md`, 133 lines, 12 sections). Today there is **no reusable executable gate**—only `micro-autonomous-test.py` (toy temp workspace, ~7 checks) and `/check-work` (session-scoped, different prompt). Building `auton-gate` **directly raises the probability that future autonomous runs on symbiosis, relay, toolbox, and greenfield repos actually reach honest PASS** with less LLM drift, fewer re-verify loops, and CI-enforceable evidence. It is **small–medium scope**, **self-dogfooding** (the project itself must pass its own gate once wired), **local-only deploy**, and **high leverage** for the “hand me an idea → wake when shipped” vision.

**Second choice:** **`auton-scaffold`** — CLI to bootstrap Phase 4 (repo skeleton, `pyproject.toml`/`package.json`, `.github/workflows/ci.yml`, `AGENTS.md`, `.env.example`) from a slug + stack hint. Pairs with `auton-gate` but does **not** solve verification reliability alone.

**Pre-research state alignment:** `~/.grok/auton-projects/ee70444d.json` already lists `recommended_project: auton-gate` (lines 25–26); this synthesis **confirms** that choice with evidence, alternatives, and risks.

---

## 1. Active Projects Map (Exclude List)

### 1.1 Git roots discovered (`find /home/Irikash -maxdepth 3 -name '.git'`)

| Path | Role / notes |
|------|----------------|
| `/home/Irikash/openclaw` | Personal AI assistant (large monorepo); **EXCLUDE** |
| `/home/Irikash/openclaw/gogcli` | Nested submodule/repo under openclaw |
| `/home/Irikash/.openclaw/workspace` | OpenClaw workspace |
| `/home/Irikash/grok-hermes-symbiosis` | Symbiosis coordination repo; **EXCLUDE** |
| `/home/Irikash/Synced/grok-mempalace-integration` | Mempalace + symbiosis-relay rich layer; **EXCLUDE** (includes `symbiosis-relay/`) |
| `/home/Irikash/AI_Projects/GrokForge/grokforge` | GrokForge main code; **EXCLUDE** |
| `/home/Irikash/AI_Projects/Santa_Claude` | Multi-agent experiments; **EXCLUDE** |
| `/home/Irikash/mission-control` | Next.js agent orchestration dashboard; **EXCLUDE** |
| `/home/Irikash/adhd-passive-site` | Static GH Pages site; **EXCLUDE** |
| `/home/Irikash/.hermes/hermes-agent` | Hermes agent source |

**Additional user-named assets (no separate top-level `.git` at depth 3 but in scope):**

| Path | Notes |
|------|--------|
| `/home/Irikash/GrokForge` | Small dir (`healing.log` only in listing); primary code under `AI_Projects/GrokForge/grokforge` |
| `~/.grok/toolbox` | Created via prior `/autonomous` (AUTON `6370a6d6`, `df604e5f`) — **extension of symbiosis/tooling, not a fresh test bed** |
| `~/.grok/skills/autonomous` | The skill under test — **not a deliverable project** |

### 1.2 Confirmed exclude set (for first test)

`openclaw`, `grok-hermes-symbiosis`, `GrokForge` (incl. `AI_Projects/GrokForge/grokforge`), `Santa_Claude`, `mission-control`, `adhd-passive-site`, `grok-mempalace-integration`, `symbiosis-relay` (under Synced tree), and **direct extensions** (e.g. `~/.grok/toolbox`, worktrees under `grok-hermes-symbiosis/.worktrees`).

### 1.3 Related ecosystem (context only)

- **Symbiosis README** (`grok-hermes-symbiosis/README.md:30`, `:225`): lists mission-control, openclaw, GrokForge, `.mempalace`.
- **Mempalace MCP search** (`mempalace_search`, wing `projects`): prior autonomous toolbox runs filed under `projects/grok-toolbox` — proves `/autonomous` works but is **not** the first-test greenfield target.

---

## 2. Autonomous Skill — Deep Analysis

### 2.1 Location and structure

| Artifact | Path |
|----------|------|
| Orchestrator spec | `~/.grok/skills/autonomous/SKILL.md` (255 lines) |
| Gate checklist | `~/.grok/skills/autonomous/docs/PRODUCTION_CHECKLIST.md` (136 lines) |
| Usage | `~/.grok/skills/autonomous/docs/USAGE.md` (87 lines) |
| Structure verifier | `scripts/verify-skill-structure.py` |
| Micro pipeline sim | `scripts/micro-autonomous-test.py` |
| Durable state | `~/.grok/auton-projects/<id>.json` (e.g. `ee70444d.json`) |
| Workspace artifacts | `/tmp/grok-auton-artifacts-<id>/` |

**Self-tests executed (this research):**

```text
verify-skill-structure.py → ALL BASIC STRUCTURE CHECKS PASSED
micro-autonomous-test.py  → VERDICT: PASS (temp hello-auton package)
```

### 2.2 Immutable pipeline (SKILL.md:39–55)

1. Setup & State  
2. Research & Synthesis  
3. Design & Full-Lifecycle Plan  
4. Bootstrap  
5. Execute Plan  
6. **Harden & Verify (Production Gate)** ← critical  
7. Deliver & Stack  
8. CI & Post-Delivery Babysit  
9. Production Activate & Persistent Handoff  
10. Memory Flush & Close  

**Exit contract (SKILL.md:57, :231):** production gate **PASS** or true external block only.

### 2.3 State & resume (SKILL.md:61–66, `ee70444d.json`)

- `AUTON_ID`: 8-char hex  
- `state_file`: `/tmp/grok-auton-${ID}.json` or `~/.grok/auton-projects/<id>.json`  
- Fields: `current_phase`, `research_path`, `design_doc_path`, `prod_gate_state`, `mempalace_drawer`, `artifacts`  
- **Friction:** schema is documented in SKILL but **not validated** by tooling; resume depends on orchestrator re-reading JSON.

### 2.4 Production gate today

| Mechanism | What it does | Gap |
|-----------|--------------|-----|
| `PRODUCTION_CHECKLIST.md` | 12 sections, 80+ checkboxes | **Human/LLM only**; verifier must re-run commands (lines 116–119) |
| Verifier subagent | Prompt-driven | **Non-deterministic**, costly, no artifact for CI |
| `/check-work` | `VERDICT: PASS/FAIL` on session work | **Different scope** than full prod checklist (`check-work/SKILL.md:56–287`) |
| `micro-autonomous-test.py` | pip/pytest/secret scan on **temp** toy | **Not** wired to real repos or checklist sections 1–12 |
| `verify-skill-structure.py` | SKILL.md frontmatter only | Skill meta only |

**Quoted gate requirement (PRODUCTION_CHECKLIST.md:127–131):**

> Never declare PASS if: Any critical test or build fails; Secrets in repo; No way for a new human or Hermes to pick up and run...

### 2.5 Orchestration friction (actionable for complementarity)

| Friction | Evidence | Complement project |
|----------|----------|-------------------|
| Gate is prompt + docs only | SKILL.md:47–51, PRODUCTION_CHECKLIST.md:116–127 | **auton-gate** |
| Bootstrap repeated per run | SKILL.md:45–46, Phase 4 | auton-scaffold (2nd) |
| State ad-hoc JSON | SKILL.md:170–186, `ee70444d.json` | auton-state-manager (lower priority) |
| Hermes kanban manual | SKILL.md:105–106, USAGE.md:54–57 | auton-kanban-setup (later) |
| Multi-AUTON observability weak | Only `~/.grok/auton-projects/*.json` | auton-runs-dashboard (later; overlaps bust-a-nut-dashboard) |
| Checklist tailoring undocumented mechanically | PRODUCTION_CHECKLIST.md:125–126 | auton-gate profiles (`cli`, `lib`, `service`) |

### 2.6 Integrations enforced

- Subagents, `todo_write`, worktrees, Composer (`SKILL.md:135–148`)  
- Hermes, Mempalace, cross-device Kumquat (`SKILL.md:145–148`, USAGE.md:53–57)  
- Related skills: design, implement, execute-plan, check-work, pr-babysit, best-of-n (`SKILL.md:242–243`)  
- **Toolbox** (`~/.grok/toolbox/TOOLBOX.md:66`): autonomous research should use toolbox; **vet-tool.sh** is a precedent for **S0–S12 protocol gates** (parallel to prod gate).

### 2.7 Prior autonomous proofs on this machine

| AUTON_ID | Deliverable | Mempalace |
|----------|-------------|-----------|
| `6370a6d6` | Grok toolbox registry + protocol | `projects/grok-toolbox` |
| `df604e5f` | Toolbox enhancements (vet --install, skill) | `projects/grok-toolbox-recommended-nexts` |
| `db7caad3` | Reboot prep (coordination only) | linux/windows-instructions |
| `ee70444d` | This research task | `projects/identify-first-auton-test-project` (planned) |

**Insight:** Toolbox run validated **orchestrator + gate in prose**; it did **not** add a **project-level** executable prod verifier for arbitrary repos.

---

## 3. Ecosystem Tool Patterns (Verifiers, Dashboards, Health Gates)

| Tool | Path | Pattern |
|------|------|---------|
| `check-primes.sh` | `~/bin/check-primes.sh` | Grep-based **self-test** across canonical files; exit 1 on fail |
| `mempalace-project-verify` | `~/bin/mempalace-project-verify` | Domain health (palace subdirs, tags) |
| `relay-health.sh` | `Synced/.../symbiosis-relay/tools/relay-health.sh` | **Fail-closed** system health + Bust-a-nut counters |
| `bust-a-nut-status` | `~/bin/bust-a-nut-status` | One-line status + relay-health excerpt |
| `bust-a-nut-dashboard` | `~/bin/bust-a-nut-dashboard` → rich `symbiosis-relay/tools/...` | Local HTTP dashboard (port 8765) |
| `symbiosis-dashboard` | `~/bin/symbiosis-dashboard` | (launcher; symbiosis ops) |
| `vet-tool.sh` | `~/.grok/toolbox/scripts/vet-tool.sh` | **Research protocol gate** before adding tools |
| `verify-skill-structure.py` | autonomous skill | Meta verification |
| `micro-autonomous-test.py` | autonomous skill | Minimal **prod-like** pipeline in `/tmp` |

**Pattern to reuse for `auton-gate`:** combine `check-primes`/`relay-health` **exit codes + structured sections** with `micro-autonomous-test` **command execution** and `PRODUCTION_CHECKLIST.md` **section IDs**.

---

## 4. Symbiosis Priorities & Roadmap Fit

### 4.1 Current operational focus (2026-06-03)

- **linux-instructions.md:7** / **windows-instructions.md:6–7:** Tier 1 off Bust-a-Nut survival; focus **Real Slack** (`slack_operator.py create-ingest-companion`), `PROJECT_FINISH_LINE.md`, `last_real_slack.md`.
- **Implication:** First `/autonomous` test should **not** compete with relay token work; **`auton-gate` is independent** (local CLI, no Pi/Slack deps).

### 4.2 OPEN_ITEMS.md (coordination/)

- Top priorities: Mempalace usage, Git/hybrid stability, hygiene (lines 20–29).
- Nice-to-haves: handoff scaffolding (#2), kanban over handoffs (#4) — **auton-scaffold** aligns with #2; **auton-gate** aligns with “production ready” symbiosis deliverables.

### 4.3 README roadmap (grok-hermes-symbiosis/README.md:188–195)

- Evaluation harness (pure Grok vs Hermes vs symbiotic) — **larger** than first test; defer.
- Kanban + Grok integration scripts — Phase 9; **later**.
- **Full Autonomy section (README.md:246–264):** documents `/autonomous`; explicitly needs **real idea test** — this research satisfies that meta-step by picking **`auton-gate`** as that idea.

### 4.4 “Hand me idea → wake when shipped”

Mechanical **PASS evidence** from `auton-gate` gives Hermes/gateway a **binary artifact** to trust without re-running a verifier subagent for every checklist line — **directly supports persistent ops** (SKILL.md Phase 9, PRODUCTION_CHECKLIST.md §12).

---

## 5. Selection Criteria (Defined)

1. **Small–medium scope:** Completable in one autonomous run (research → PASS) without multi-day runtime or paid cloud.
2. **High complementarity:** Improves Phase 6/9 PASS rate for **other** projects.
3. **Self-verifiable:** Own repo can satisfy the same gate it implements.
4. **Fresh greenfield repo:** Not inside excluded trees.
5. **Primes-aligned:** Self-provision, bust-a-nut nonstop, Mirrorability (scriptable, documentable for Oregon).
6. **Symbiosis leverage:** Supports long-horizon delegation + Mempalace/Hermes handoff.
7. **Testability:** Unit tests, GHA CI, README, no secrets; local/docker optional only.

---

## 6. Candidate Projects (5) — Evaluation

| Criterion | **1. auton-gate** | **2. auton-scaffold** | **3. auton-state-manager** | **4. auton-kanban-auto-setup** | **5. auton-eval-harness** |
|-----------|-------------------|----------------------|----------------------------|-------------------------------|---------------------------|
| Scope | M– (CLI + checks + report) | M (templates + CLI) | S–M | M (Hermes APIs + templates) | L |
| Complementarity | **Highest** (Phase 6) | High (Phase 4) | Medium (resume) | Medium (Phase 9) | High but indirect |
| Self-dogfood | **Yes** | Yes | Yes | Harder (needs live Hermes) | Heavy |
| Fresh repo | Yes | Yes | Yes | Yes | Yes |
| Paid hosting | No | No | No | No | Maybe |
| First-test risk | Low | Low | Low | **Hermes/slack coupling** | **Too large** |
| CI enforceable | **Yes** | Yes | Yes | Partial | Yes |

### 6.1 auton-gate (recommended)

**Elevator pitch:** `auton-gate check /path/to/project [--auton-id ee70444d] [--profile cli|lib|service]` → runs deterministic checks mapped 1:1 to `PRODUCTION_CHECKLIST.md` sections where automatable; outputs `GATE_REPORT.md` + exit code 0/1.

**Automatable examples (v1):**

- §3: run detected build/lint (`pyproject.toml` → `ruff`, `pytest`; `package.json` → `npm test`)  
- §4: tests exist + pass  
- §5: secret patterns, `.env` not committed  
- §6: `.github/workflows/*.yml` exists  
- §7: README sections heuristic (headings: Quickstart, Config)  
- §8: lockfile presence  
- §11: `git status` clean (optional flag)  
- §12: `PRODUCTION_READY.md` presence when `--auton-id` links to state  

**Non-automatable (v1):** design doc 0-issues, security-auditor sign-off → report as `MANUAL_REVIEW_REQUIRED` not FAIL if optional.

### 6.2 auton-scaffold

`auton-scaffold init my-slug --stack python-cli` → emits repo skeleton. **Does not** fix gate reliability alone.

### 6.3 auton-state-manager

CRUD/validate `~/.grok/auton-projects/*.json`, phase transitions. Useful; **does not** reduce verify loop count.

### 6.4 auton-kanban-auto-setup

Hermes MCP `messages_send` + board templates. **Blocked** on operator Hermes session semantics for first test; better as **second wave**.

### 6.5 auton-eval-harness (symbiosis README roadmap)

Compare Grok vs Hermes vs symbiotic on benchmark tasks. **High value, wrong size** for first `/autonomous` functional test.

### 6.6 Rejected: meta bust-a-nut-status web dashboard

`bust-a-nut-dashboard` already exists (`~/bin/bust-a-nut-dashboard` → rich relay tools). Duplicate scope; weak checklist mapping.

---

## 7. Winner & Runner-Up

### Winner: **auton-gate**

**Rationale (evidence chain):**

1. User constraint: complement **autonomous completion** of ongoing work → gate is the **documented bottleneck** (SKILL Phase 6, 12-section checklist).  
2. Existing scripts prove **executable verification culture** (`check-primes`, `relay-health`, `vet-tool`) but **none** apply to arbitrary project prod readiness.  
3. `micro-autonomous-test.py` proves the **concept** of automated gate (VERDICT PASS) but is **not production-grade** for real trees (temp dir, 7 checks).  
4. Prior toolbox autonomous runs show orchestrator works; **next marginal gain** is **deterministic gate**.  
5. Small-medium, local, testable, fresh repo, CI-friendly — meets all criteria §5.  
6. Aligns with `ee70444d.json` pre-recommendation (`artifacts.recommended_project`).

### Runner-up: **auton-scaffold**

Bootstrap friction is real (SKILL Phase 4) but **second** to verification; can be **follow-on** `/autonomous` run after `auton-gate` PASS.

---

## 8. Production-Ready Target for `auton-gate` (Design Phase Input)

### Stack (recommended)

- **Python 3.11+**, `pyproject.toml` + `src/auton_gate/`  
- CLI: `typer` or `argparse` (stdlib-only acceptable for v1)  
- Checks: modular `checks/*.py` registry keyed by checklist section IDs  
- Reporting: Markdown + JSON (`gate_report.json`) for Hermes/Mempalace ingest  
- Tests: `pytest` with fixture repos under `tests/fixtures/` (minimal good/bad repos)  
- CI: `.github/workflows/ci.yml` — lint + test on push  
- Docker: optional `Dockerfile` for reproducible CI local mirror (not required for PASS)  
- Deploy: **none** (CLI); optional `pip install` from GitHub releases  

### Key features (MVP)

1. `auton-gate check <path>` with exit code.  
2. `--checklist ~/.grok/skills/autonomous/docs/PRODUCTION_CHECKLIST.md` (default).  
3. `--auton-id` loads `~/.grok/auton-projects/<id>.json` for artifact paths (research, design, PRODUCTION_READY).  
4. `--profile` tailors skip/rules (documented in gate report per checklist line 125).  
5. `auton-gate explain <check-id>` for agent/human remediation hints.  
6. Integration hook doc: orchestrator Phase 6 runs gate **before** verifier subagent; subagent only adjudicates `MANUAL_*` items.

### Plug-in to autonomous phases

| Phase | Integration |
|-------|-------------|
| 6 | Run `auton-gate check`; loop fixes until exit 0; store report in `artifacts` + Mempalace |
| 9 | Attach `GATE_REPORT.md` to `PRODUCTION_READY.md` |
| 10 | File pattern learnings to `implement-memory` / drawer `projects/auton-gate` |

### Mempalace / Hermes hooks

- Drawer: `projects/auton-gate` with checklist version pin.  
- Hermes: kanban lane “auton-gate releases” optional post-MVP.  

### Mirrorability

- Document Oregon install: `pip install git+...` or synced repo under `C:\Synced\Projects\auton-gate`.  
- Same CLI invocations on Windows (Python cross-platform).

---

## 9. How This Complements Current Work (Not Competing)

| Ongoing work | Relationship |
|--------------|--------------|
| Real Slack / symbiosis-relay | **No dependency**; gate is local |
| grok-hermes-symbiosis coordination | After PASS, **one Kumquat** to mention `auton-gate` in linux/windows instructions optional |
| grok-mempalace-integration | Optional: run gate in CI for **that** repo later — not first test |
| ~/.grok/toolbox | Complementary: vet-tool gates **new tools**; auton-gate gates **projects** |
| `/autonomous` skill itself | **Extends** skill with recommended `auton-gate` invocation in Phase 6 (doc patch post-PASS) |

---

## 10. Risks, Assumptions, Decisions

### Risks

| Risk | Mitigation |
|------|------------|
| Over-automation declares false PASS | Mark ambiguous checks MANUAL; default strict on build/test/secrets |
| Checklist drift vs SKILL | Pin checklist hash; `auton-gate --version` reports checklist path |
| Scope creep (full Hermes/kanban) | MVP = check + report only |
| Oregon mirror lag | README + Syncthing path; no Pi required |

### Assumptions

- First test run uses **`/autonomous` with idea:** “Build auton-gate …” in new repo `~/auton-gate` (or `~/Projects/auton-gate`).  
- Python acceptable (consistent with micro-test, toolbox, relay tools).  
- User approves **new GitHub repo** under personal account (optional for PASS; local git sufficient).  

### KEY_DECISIONS.log

```
2026-06-03 | DECISION-001 | Winner = auton-gate | Rationale = Phase 6 gate is LLM-only; highest leverage for PASS reliability
2026-06-03 | DECISION-002 | Runner-up = auton-scaffold | Sequenced after auton-gate
2026-06-03 | DECISION-003 | Exclude all listed incumbent repos | User constraint
2026-06-03 | DECISION-004 | Defer auton-eval-harness | README roadmap item; too large for first test
2026-06-03 | DECISION-005 | MVP integrates with ~/.grok/auton-projects/<id>.json | State file already used by ee70444d
2026-06-03 | DECISION-006 | Confirm ee70444d.json pre-recommendation auton-gate | Validated by research
```

---

## 11. Suggested Next Phase Prompt (for orchestrator)

```text
/autonomous Build production-ready `auton-gate`: a Python CLI that implements the mechanical portions of ~/.grok/skills/autonomous/docs/PRODUCTION_CHECKLIST.md for an arbitrary project path, supports --auton-id linking to ~/.grok/auton-projects/<id>.json, emits GATE_REPORT.md + JSON + exit code, includes pytest fixtures, GitHub Actions CI, README with integration section for Phase 6 of the autonomous skill. New git repo at ~/auton-gate (not inside grok-hermes-symbiosis or grok-mempalace-integration). No paid hosting. Target: pip install -e . && auton-gate check . passes on self after implementation.
```

---

## 12. Sources Appendix

| # | Source | Use |
|---|--------|-----|
| S1 | `~/.grok/skills/autonomous/SKILL.md` | Pipeline, gate, state, integrations |
| S2 | `~/.grok/skills/autonomous/docs/PRODUCTION_CHECKLIST.md` | Gate definition |
| S3 | `~/.grok/skills/autonomous/docs/USAGE.md` | Invocation, gate strictness |
| S4 | `~/.grok/skills/autonomous/scripts/micro-autonomous-test.py` | Micro gate pattern |
| S5 | `~/.grok/skills/autonomous/scripts/verify-skill-structure.py` | Skill smoke |
| S6 | `~/.grok/skills/check-work/SKILL.md` | Contrast with check-work scope |
| S7 | `~/.grok/auton-projects/ee70444d.json` | State + pre-recommendation |
| S8 | `~/.grok/toolbox/TOOLBOX.md` | Prior autonomous deliverables |
| S9 | `grok-hermes-symbiosis/README.md` | Ecosystem, /autonomous section, roadmap |
| S10 | `grok-hermes-symbiosis/cross-device/coordination/OPEN_ITEMS.md` | Priorities |
| S11 | `grok-hermes-symbiosis/cross-device/coordination/linux-instructions.md` | Current focus Slack |
| S12 | `~/bin/check-primes.sh`, `mempalace-project-verify`, `bust-a-nut-status` | Verifier patterns |
| S13 | `Synced/.../symbiosis-relay/tools/relay-health.sh` | Health gate pattern |
| S14 | `find …/.git` (depth 3) | Repo map |
| S15 | `mempalace__mempalace_search` (wing projects) | Prior auton toolbox runs |
| S16 | Terminal: `verify-skill-structure.py`, `micro-autonomous-test.py` | Live PASS output |

---

**End of synthesis.** Handoff to Design phase: use §8 as initial architecture/constraints input.