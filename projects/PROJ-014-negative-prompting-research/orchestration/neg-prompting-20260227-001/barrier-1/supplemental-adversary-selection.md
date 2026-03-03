# Strategy Selection Plan — Supplemental Vendor Evidence Report

**Deliverable:** Supplemental Evidence Report: Vendor Self-Practice and Session Empirical Observations (Barrier 1, PROJ-014)
**File:** `projects/PROJ-014-negative-prompting-research/orchestration/neg-prompting-20260227-001/barrier-1/supplemental-vendor-evidence.md`
**Selection Date:** 2026-02-27

---

## Criticality Assessment

- **Requested Level:** C4 (Critical)
- **Deliverable Type:** Analysis (research synthesis supplemental evidence)
- **Auto-Escalation Applied:** No
  - AE-001 (constitution touch): Not triggered
  - AE-002 (rules/ touch): Not triggered
  - AE-003 (ADR creation): Not triggered
  - AE-004 (baselined ADR modification): Not triggered
  - AE-005 (security-relevant code): Not triggered
  - AE-006 (context fill): WARNING tier (78% usage) — log and continue per AE-006b
- **Final Level:** C4 (Critical)

**Rationale:** C4 criticality confirmed. This is a standalone evidence report supporting the PROJ-014 research hypothesis. The report documents four evidence categories (vendor self-practice, production system, session empirical observation, innovator's gap) and proposes a controlled A/B experimental design for Phase 2. The findings directly inform the project's core research question about negative prompting effectiveness. Irreversible research contribution at project governance level. Quality threshold set at >= 0.95 per project constraints (PLAN.md).

---

## Selected Strategies (Ordered)

**Criticality C4 requires all 10 selected strategies per quality-enforcement.md. No optional strategies.**

| Order | Strategy ID | Strategy Name | Template Path | Required/Optional | Group |
|-------|-------------|---------------|---------------|--------------------|-------|
| 1 | S-010 | Self-Refine | `.context/templates/adversarial/s-010-self-refine.md` | Required | Group A (Self-Review) |
| 2 | S-003 | Steelman Technique | `.context/templates/adversarial/s-003-steelman.md` | Required | Group B (Strengthen) |
| 3 | S-002 | Devil's Advocate | `.context/templates/adversarial/s-002-devils-advocate.md` | Required | Group C (Challenge) |
| 4 | S-004 | Pre-Mortem Analysis | `.context/templates/adversarial/s-004-pre-mortem.md` | Required | Group C (Challenge) |
| 5 | S-001 | Red Team Analysis | `.context/templates/adversarial/s-001-red-team.md` | Required | Group C (Challenge) |
| 6 | S-007 | Constitutional AI Critique | `.context/templates/adversarial/s-007-constitutional-ai.md` | Required | Group D (Verify) |
| 7 | S-011 | Chain-of-Verification | `.context/templates/adversarial/s-011-cove.md` | Required | Group D (Verify) |
| 8 | S-012 | FMEA | `.context/templates/adversarial/s-012-fmea.md` | Required | Group E (Decompose) |
| 9 | S-013 | Inversion Technique | `.context/templates/adversarial/s-013-inversion.md` | Required | Group E (Decompose) |
| 10 | S-014 | LLM-as-Judge | `.context/templates/adversarial/s-014-llm-as-judge.md` | Required | Group F (Score) |

---

## H-16 Compliance

**Steelman before Devil's Advocate Constraint (H-16 HARD):**

- S-003 (Steelman Technique) position: **2**
- S-002 (Devil's Advocate) position: **3**
- Constraint satisfied: **Yes** — S-003 (position 2) executed before S-002 (position 3) per H-16 ordering requirement

This ensures the deliverable's strengths are articulated and reinforced before adversarial challenge, preventing premature rejection of sound evidence and interpretive frameworks.

---

## Execution Context

**Quality Gate:**
- Threshold: >= 0.95 (C4 critical threshold, per project PLAN.md)
- Scoring mechanism: S-014 (LLM-as-Judge) with 6-dimension rubric from quality-enforcement.md
- Dimensions: Completeness (0.20), Internal Consistency (0.20), Methodological Rigor (0.20), Evidence Quality (0.15), Actionability (0.15), Traceability (0.10)

**Minimum iterations:** 3 per H-14 (creator-critic-revision cycle)
**Maximum iterations for C4:** 10 per agent-routing-standards.md RT-M-010

**Context Budget Status:**
- Current usage: ~78% of 200K token window
- Reserve applied: 5% minimum per CB-01 (agent-development-standards.md)
- Available for tournament execution: ~14K tokens

**Deliverable Scope:**
- 415 lines of analysis and evidence documentation
- 4 major evidence categories with source citations
- 12 consolidated findings across vendor, production system, empirical, and methodology categories
- 1 controlled A/B experimental design for Phase 2
- 3 hypothesis reframings for consideration

---

## Strategy Overrides Applied

**None.** All strategies are required per C4 criticality. No user overrides requested.

---

## P-003 Self-Check (No Recursion)

This selection plan operates at the worker level within an orchestrator context. The adv-selector agent itself does NOT invoke other agents. Execution will proceed via the adv-executor agent (also a worker), which loads and applies each strategy template sequentially. No recursive subagent spawning. P-003 compliant.

---

## Constitutional Compliance

| Principle | Adherence |
|-----------|-----------|
| P-003 (No recursive subagents) | Compliant — single-level orchestrator-to-worker topology |
| P-020 (User authority) | Compliant — selection respects requested C4 criticality and quality threshold |
| P-022 (No deception) | Compliant — all selected and excluded strategies transparently listed; no capability claims beyond scope |

---

## Pre-Persistence Self-Review (H-15, S-010)

Per H-15, verify before persistence:

1. ✓ All strategy IDs valid (S-001 through S-014, all 10 selected strategies present)
2. ✓ H-16 ordering satisfied (S-003 position 2 < S-002 position 3)
3. ✓ Auto-escalation rules checked (AE-001 through AE-006e, no escalation triggered)
4. ✓ User overrides reflected (none requested, all required strategies included)
5. ✓ Template paths correct (all paths follow `.context/templates/adversarial/s-{NNN}-{slug}.md` pattern)
6. ✓ Criticality justification documented (C4 irreversible research contribution)
7. ✓ Quality threshold specified (>= 0.95 per PLAN.md)
8. ✓ Execution context clear (10 strategies, 3-10 iteration bounds, tournament mode)

**Self-review result: PASS. Proceeding with persistence.**

---

*adv-selector | PROJ-014 | Barrier 1 Supplemental Strategy Selection | 2026-02-27*
*SSOT: `.context/rules/quality-enforcement.md` (Criticality Levels section)*
*Generated by: adv-selector agent*
*Compliance: H-15, H-16, P-003, P-020, P-022*
