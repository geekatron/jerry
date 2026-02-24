# STORY-003: Unified Research Synthesis v2

> **Type:** story
> **Status:** completed
> **Priority:** critical
> **Impact:** medium
> **Created:** 2026-02-22T00:00:00Z
> **Due:** —
> **Completed:** 2026-02-22
> **Parent:** FEAT-003
> **Owner:** ps-synthesizer-002
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

Unified synthesis v2 establishing Two-Leg Thesis. Leg 1: LLMs confidently wrong within training data (ITS FA=0.850, CIR=0.070). Leg 2: LLMs decline/hallucinate beyond training data (PC FA=0.070). 30+ numerical errors corrected during QG-3 revision. Output via ps-synthesizer-002.

---

## Acceptance Criteria

- [x] Two-Leg Thesis established with quantitative evidence
- [x] All deception patterns mapped to multi-source evidence
- [x] Full citation chain maintained per R-004
- [x] 30+ numerical errors from v1 corrected
- [x] Findings persisted to repository

---

## Delivery Evidence

| Artifact | Path |
|----------|------|
| Primary output | `orchestration/llm-deception-20260222-002/ps/phase-3-synthesis/ps-synthesizer-002/ps-synthesizer-002-output.md` |
| Quality gate R1 | `orchestration/llm-deception-20260222-002/quality-gates/qg-3/qg-3-r1-report.md` |
| Quality gate R2 | `orchestration/llm-deception-20260222-002/quality-gates/qg-3/qg-3-r2-report.md` |

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-22 | orch-planner | pending | Story created for workflow-002 v2 synthesis |
| 2026-02-22 | orchestrator | completed | Delivered via ps-synthesizer-002. Two-Leg Thesis with corrected values. QG-3 R1=0.82 REJECTED, 30+ values corrected. QG-3 R2=0.92 PASS. |
