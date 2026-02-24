# STORY-005: Agent A - Internal Knowledge Only (v2)

> **Type:** story
> **Status:** completed
> **Priority:** critical
> **Impact:** medium
> **Created:** 2026-02-22T00:00:00Z
> **Due:** —
> **Completed:** 2026-02-22
> **Parent:** FEAT-002
> **Owner:** ps-researcher-006
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

Agent A internal-only responses to 15 questions. No external tools (no WebSearch, no Context7). Completely isolated from Agent B. Results scored against ground truth baselines. ITS Factual Accuracy = 0.850, Confident Inaccuracy Rate = 0.070. Output via ps-researcher-006.

---

## Acceptance Criteria

- [x] All 15 questions answered using internal knowledge only
- [x] No external tool usage (no WebSearch, no Context7)
- [x] Output preserved as versioned artifacts
- [x] Responses scored against ground truth baselines

---

## Delivery Evidence

| Artifact | Path |
|----------|------|
| Primary output | `orchestration/llm-deception-20260222-002/ps/phase-2-ab-test/ps-researcher-005-agent-a/agent-a-responses.md` |
| Quality gate | `orchestration/llm-deception-20260222-002/quality-gates/qg-2/qg-2-report.md` |

**Key metrics:** ITS FA = 0.850, CIR = 0.070

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-22 | orch-planner | pending | Story created for v2 A/B test Agent A |
| 2026-02-22 | orchestrator | completed | Delivered via ps-researcher-006. Internal-only responses to 15 questions. ITS FA=0.850, CIR=0.070. QG-2 PASS at 0.92 (R2). |
