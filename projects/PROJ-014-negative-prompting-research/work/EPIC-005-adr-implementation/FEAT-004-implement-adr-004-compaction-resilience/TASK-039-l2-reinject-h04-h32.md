# TASK-039: Decision 2 — Add L2-REINJECT Markers for H-04 and H-32

> **Type:** task
> **Status:** completed
> **Priority:** high
> **Created:** 2026-02-28
> **Parent:** FEAT-004
> **Owner:** —
> **Activity:** IMPLEMENTATION

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Brief description |
| [Content](#content) | Description and acceptance criteria |
| [Evidence](#evidence) | Deliverables and verification |
| [History](#history) | Status changes |

---

## Summary

Add L2-REINJECT markers for H-04 (active project REQUIRED) and H-32 (GitHub Issue parity) to close the widest-failure-window Tier B enforcement gaps. Verify total L2 token budget stays within 850-token limit.

---

## Content

### Description

ADR-004 Decision 2 (timing conditional — framing-independent but token budget verification required). H-04 and H-32 are Tier B HARD rules with the widest failure windows: if their compensating controls (SessionStart hook for H-04, /worktracker + CI for H-32) fail, no subsequent enforcement trigger exists for the entire session. Adding L2-REINJECT markers provides compaction-immune per-prompt re-injection.

Before implementation, resolve the 559 vs. 670 token discrepancy (documented in TASK-012) by performing an exact token count of all current L2-REINJECT marker content. Estimated additions: H-04 (~35 tokens), H-32 (~40 tokens). Worst-case total: ~745/850 tokens (87.6% utilization).

### Acceptance Criteria

- [x] Exact token count of current L2-REINJECT markers performed
- [x] H-04 L2-REINJECT marker added to project-workflow.md (rank=8)
- [x] H-32 L2-REINJECT marker added to project-workflow.md (rank=9)
- [x] Total L2 token consumption verified within 850-token budget (~619/850 = 72.8%)
- [x] quality-enforcement.md Two-Tier Enforcement Model updated (H-04/H-32 moved to Tier A, 22 Tier A / 3 Tier B)

### Related Items

- Parent: [FEAT-004: Implement ADR-004](./FEAT-004-implement-adr-004-compaction-resilience.md)
- References: ADR-004 Decision 2
- References: `quality-enforcement.md` Two-Tier Enforcement Model

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| Updated rule files with L2-REINJECT markers | Rule file modification | `.context/rules/` |
| Updated quality-enforcement.md | Rule file modification | `.context/rules/quality-enforcement.md` |

### Verification

- [x] Acceptance criteria verified

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-28 | Created | Initial creation |
| 2026-02-28 | Completed | L2-REINJECT markers added; Tier A/B updated. Commit: f5f892b2 |
