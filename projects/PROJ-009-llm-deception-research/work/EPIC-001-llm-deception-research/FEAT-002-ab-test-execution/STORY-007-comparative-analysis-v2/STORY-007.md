# STORY-007: Comparative Analysis (v2)

> **Type:** story
> **Status:** completed
> **Priority:** critical
> **Impact:** medium
> **Created:** 2026-02-22T00:00:00Z
> **Due:** —
> **Completed:** 2026-02-22
> **Parent:** FEAT-002
> **Owner:** ps-analyst-002
> **Target Sprint:** —

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Description and scope |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done |
| [Delivery Evidence](#delivery-evidence) | Artifact references |
| [History](#history) | Status changes |

---

## Summary

7-dimension comparative analysis with Confident Inaccuracy Rate (CIR). SOURCE OF TRUTH for all numerical values in the v2 A/B test. Revealed Two-Leg pattern: Leg 1 (ITS: Agent A FA=0.850, CIR=0.070 -- internal knowledge is largely accurate but confident when wrong) and Leg 2 (PC: Agent B FA=0.870 -- tool-augmented answers degrade on well-known stable facts). Output via ps-analyst-002.

---

## Acceptance Criteria

- [x] 7-dimension comparison complete across all 15 questions
- [x] Confident Inaccuracy Rate (CIR) computed for both agents
- [x] Two-Leg pattern documented (Leg 1: ITS vulnerability, Leg 2: PC degradation)
- [x] Evidence of stale data problem documented (R-001)
- [x] Quantitative metrics provided with ground truth baselines
- [x] Findings persisted to repository as SSOT for numerical values

---

## Delivery Evidence

| Artifact | Path |
|----------|------|
| Primary output | `orchestration/llm-deception-20260222-002/ps/phase-2-ab-test/ps-analyst-002/ps-analyst-002-output.md` |
| Quality gate | `orchestration/llm-deception-20260222-002/quality-gates/qg-2/qg-2-report.md` |

**Key metrics:** Two-Leg pattern -- Leg 1 (ITS: FA=0.850, CIR=0.070), Leg 2 (PC: FA=0.070). Agent A vs Agent B comparative analysis across 7 dimensions.

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-22 | orch-planner | pending | Story created for v2 comparative analysis |
| 2026-02-22 | orchestrator | completed | Delivered via ps-analyst-002. 7-dimension comparison with CIR. Two-Leg pattern revealed. SSOT for all v2 numerical values. QG-2 PASS at 0.92 (R2). |
