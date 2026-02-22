# GitHub Issue Draft: EN-002 HARD Rule Budget Enforcement

> **Deliverable Type:** GitHub Issue (Feature Request / Implementation Record)
> **Worktracker Entity:** EN-002
> **Criticality:** C3 (auto-escalated: touches .context/rules/)

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Title](#title) | Issue title |
| [Labels](#labels) | GitHub labels |
| [Body](#body) | Full issue description |

---

## Title

Implement principled HARD rule budget enforcement (EN-002)

## Labels

`enhancement`, `proj-007`, `enforcement`, `governance`

## Body

### Problem

Two critical gaps threaten the Jerry Framework's enforcement quality:

1. **Unprincipled ceiling (DISC-001):** The 35-slot HARD rule ceiling was set retroactively with no derivation. A principled upper boundary derived from three independent constraint families (cognitive load @ 7+/-2, enforcement coverage @ token budget, governance burden @ review cost) is **25 rules**.

2. **L2 engine coverage gap (DISC-002):** The prompt reinforcement engine reads only `quality-enforcement.md`, providing per-prompt L2 protection for 10 of 31 H-rules (32%). The remaining 21 rules are vulnerable to context rot — the core problem Jerry exists to solve.

Without this fix, adding H-32..H-35 from PROJ-007 Agent Patterns would push the rule count to 35/35 (100% utilization of an unprincipled ceiling), degrading enforcement quality for all rules.

### Solution

EN-002 implements 5 decisions from DEC-001:

| Decision | Change | Impact |
|----------|--------|--------|
| D-001 | Expand L2 engine to read all 9 auto-loaded rule files | Engine reads all rule files (was: 1 file). Combined with D-002 consolidation, achieves 84% L2 coverage (21/25 H-rules). |
| D-002 | Consolidate H-25..H-30 (6->2) and H-07..H-09 (3->1) | Count: 31 -> 25 rules. Consolidation reduces denominator; engine expansion increases numerator. |
| D-003 | Defer TASK-016 until consolidation creates headroom | Unblocks EN-001 H-32..H-35 integration via exception mechanism |
| D-004 | Add L5 CI enforcement gate | Prevents silent ceiling breaches (pre-commit + GitHub Actions) |
| D-005 | Measure enforcement effectiveness (structural) | Pre/post comparison baseline. Behavioral measurement deferred to TASK-029. |

### Key Metrics

| Metric | Before | After |
|--------|--------|-------|
| HARD rule count | 31 | 25 (-6) |
| L2 H-rule coverage | 10/31 (32%) | 21/25 (84%) |
| Context rot exposure | 21 rules unprotected | 4 rules (Tier B with compensating controls) |
| L5 enforcement | None | Active (pre-commit + CI) |
| L2 token budget | 415/600 (69%) | 559/850 (66%) |
| Ceiling headroom | 4 slots (unprincipled) | 0 slots (principled, exception mechanism available) |

### Two-Tier Enforcement Model

- **Tier A (21 rules):** L2 engine-protected. Re-injected into every prompt via L2-REINJECT markers. Context-rot immune.
- **Tier B (4 rules):** Compensating controls only. Not L2-protected due to rule characteristics:
  - **H-04** (active project required): Enforced by SessionStart hook (L1) — session-scoped, not per-prompt
  - **H-16** (steelman before critique): Enforced by skill workflow logic — workflow-scoped ordering constraint
  - **H-17** (quality scoring required): Enforced by quality gate infrastructure — output-gated, not per-prompt
  - **H-18** (constitutional compliance check): Enforced by S-007 strategy execution — triggered by criticality level

### Quality Assurance

- **C4 adversary tournament:** All 10 strategies applied (S-001 through S-014)
- **S-014 LLM-as-Judge scoring:** 0.620 (R1) -> 0.868 (R2) -> 0.924 (R3) -> **0.953 (R4) PASS** at >= 0.95 elevated threshold
- **Tests:** 3,382 passed, 66 skipped, 0 failed
- **Pre-commit hooks:** 19/19 PASS
- **L5 gate:** 25/25 PASS, headroom 0

### Acceptance Criteria

- [x] L2 engine reads all auto-loaded rule files (not just quality-enforcement.md)
- [x] H-25..H-30 consolidated into 2 compound rules
- [x] H-07..H-09 consolidated into 1 compound rule
- [x] HARD rule count <= 25 (post-consolidation: 25)
- [x] quality-enforcement.md updated with 25-rule ceiling, two-tier table, exception mechanism
- [x] All rules classified as Tier A or Tier B
- [x] L5 CI gate enforces HARD rule ceiling (pre-commit + GitHub Actions CI)
- [x] All pre-commit hooks pass (19/19)
- [x] All tests pass (pytest: 3,382 pass, 66 skipped)
- [x] Enforcement effectiveness measured (pre/post comparison)

### Worktracker Traceability

| Entity | Type | Status | Path |
|--------|------|--------|------|
| EN-002 | Enabler | DONE | `projects/PROJ-007-agent-patterns/work/EN-002-hard-rule-budget-enforcement/EN-002.md` |
| DISC-001 | Discovery | VALIDATED | `work/EN-002-.../DISC-001-hard-rule-budget-no-derivation/DISC-001.md` |
| DISC-002 | Discovery | VALIDATED | `work/EN-002-.../DISC-002-l2-engine-coverage-gap/DISC-002.md` |
| DEC-001 | Decision | ACCEPTED | `work/EN-002-.../DEC-001-hard-rule-budget-implementation-plan/DEC-001.md` |
| TASK-022..028 | Tasks | DONE (7/7) | `work/EN-002-.../TASK-022..028-*/TASK-0{22..28}.md` |
| TASK-029 | Task | PENDING | `work/EN-002-.../TASK-029-empirical-behavioral-measurement/TASK-029.md` |

**Enables:** EN-001:TASK-016 (H-32..H-35 integration from PROJ-007 Agent Patterns)

### Files Changed

**62 files** changed, **8,965 insertions**, **111 deletions**

| Category | Files | Key Changes |
|----------|-------|-------------|
| Engine | `src/.../prompt_reinforcement_engine.py` | Directory globbing, `tokens` field deprecated, budget 600->850 |
| CI Gate | `scripts/check_hard_rule_ceiling.py` (new) | L5 ceiling enforcement with absolute max 28 |
| Governance | `quality-enforcement.md` (v1.3.0->1.5.0) + 8 rule files + `CLAUDE.md` | Ceiling 35->25, two-tier model, `tokens` removed from all 17 markers |
| Tests | 3 test files (41 + 12 + 51 = 104 targeted tests) | Multi-file reading, ceiling gate, e2e assertions |
| CI/CD | `.pre-commit-config.yaml`, `.github/workflows/ci.yml` | Hard rule ceiling hook + CI job |
| Worktracker | 30+ entity files | EN-001, EN-002, discoveries, decisions, tasks, tournament artifacts |

### Related Artifacts

| Artifact | Path |
|----------|------|
| Implementation Summary | `work/EN-002-.../en-002-implementation-summary.md` |
| Enforcement Effectiveness Report | `work/EN-002-.../TASK-028-.../enforcement-effectiveness-report.md` |
| C4 Tournament Score (R4 Final) | `work/EN-002-.../c4-tournament/s014-score-r4.md` |
| C4 Tournament Revision Logs | `work/EN-002-.../c4-tournament/r{2,3,4}-revision-log.md` |
| Upper Boundary Derivation | `orchestration/.../adversary/hard-rule-budget/hard-rule-budget-upper-boundary-derivation-r2.md` |
| ADR Supersession Note | Documented in `en-002-implementation-summary.md` — ADR-EPIC002-002 L2 budget (600) superseded by SSOT (850) |
