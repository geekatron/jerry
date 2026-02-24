# STORY-006: Agent B - External Research Only (v2)

> **Type:** story
> **Status:** completed
> **Priority:** critical
> **Impact:** medium
> **Created:** 2026-02-22T00:00:00Z
> **Due:** —
> **Completed:** 2026-02-22
> **Parent:** FEAT-002
> **Owner:** ps-researcher-007
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

Agent B tool-augmented responses to 15 questions using Context7 + WebSearch only. Completely isolated from Agent A. Results scored against ground truth baselines. ITS Factual Accuracy = 0.930, PC (Positive Control) Factual Accuracy = 0.870. Output via ps-researcher-007.

---

## Acceptance Criteria

- [x] All 15 questions answered using Context7/WebSearch only
- [x] All sources cited with URLs
- [x] Output preserved as versioned artifacts
- [x] Responses scored against ground truth baselines

---

## Delivery Evidence

| Artifact | Path |
|----------|------|
| Primary output | `orchestration/llm-deception-20260222-002/ps/phase-2-ab-test/ps-researcher-006-agent-b/agent-b-responses.md` |
| Quality gate | `orchestration/llm-deception-20260222-002/quality-gates/qg-2/qg-2-report.md` |

**Key metrics:** ITS FA = 0.930, PC FA = 0.870

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-22 | orch-planner | pending | Story created for v2 A/B test Agent B |
| 2026-02-22 | orchestrator | completed | Delivered via ps-researcher-007. Tool-augmented responses to 15 questions. ITS FA=0.930, PC FA=0.870. QG-2 PASS at 0.92 (R2). |
