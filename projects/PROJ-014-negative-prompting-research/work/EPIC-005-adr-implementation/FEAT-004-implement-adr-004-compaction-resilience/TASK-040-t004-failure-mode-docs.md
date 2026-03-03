# TASK-040: Decision 3 — T-004 Failure Mode Documentation in Templates

> **Type:** task
> **Status:** completed
> **Priority:** medium
> **Created:** 2026-02-28
> **Parent:** FEAT-004
> **Owner:** —
> **Activity:** DOCUMENTATION

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

Add T-004 failure mode documentation sections to all constraint-bearing templates. Each section documents which constraints are vulnerable to context compaction, what fails if lost, what compensating controls exist, and how to detect constraint loss.

---

## Content

### Description

ADR-004 Decision 3 (unconditional). Addresses WT-GAP-005 from TASK-014. No entity template currently documents what happens when template constraints are lost during context compaction. Add a new section to constraint-bearing templates answering four questions: (1) which constraints are vulnerable to compaction, (2) what is the failure mode if lost, (3) what compensating controls exist (L2 markers, hooks, CI gates, skill enforcement), (4) what is the detection mechanism.

### Acceptance Criteria

- [x] All constraint-bearing templates identified (9 templates: EPIC, FEATURE, STORY, TASK, BUG, ENABLER, SPIKE, DISCOVERY, DECISION)
- [x] Failure mode documentation section added to each template
- [x] Each section answers the 4 required questions (constraint, failure mode, compensating control, detection)
- [x] Template format standardized across all affected templates

### Related Items

- Parent: [FEAT-004: Implement ADR-004](./FEAT-004-implement-adr-004-compaction-resilience.md)
- References: ADR-004 Decision 3
- References: TASK-014 WT-GAP-005

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| Updated constraint-bearing templates | Template modifications | `.context/templates/` |

### Verification

- [x] Acceptance criteria verified

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-28 | Created | Initial creation |
| 2026-02-28 | Completed | T-004 sections added to 9 templates. Commit: f5f892b2 |
