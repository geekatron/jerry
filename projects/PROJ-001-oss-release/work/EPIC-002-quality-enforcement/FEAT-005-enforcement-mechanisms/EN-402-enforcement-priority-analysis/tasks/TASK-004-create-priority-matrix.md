# TASK-004: Create Priority Matrix and Score All Vectors

<!--
TEMPLATE: Task
VERSION: 0.1.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
-->

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Frontmatter](#frontmatter) | YAML metadata |
| [Content](#content) | Description and acceptance criteria |
| [Time Tracking](#time-tracking) | Effort estimates |
| [Evidence](#evidence) | Deliverables and verification |
| [History](#history) | Status changes |

---

## Frontmatter

```yaml
id: "TASK-004"
work_type: TASK
title: "Create priority matrix and score all vectors"
description: |
  Apply the evaluation criteria from TASK-001, risk assessment from TASK-002,
  and trade study findings from TASK-003 to score all enforcement vectors.
  Produce a ranked priority list with composite scores.
classification: ENABLER
status: BACKLOG
resolution: null
priority: CRITICAL
assignee: "ps-analyst"
created_by: "Claude"
created_at: "2026-02-12"
updated_at: "2026-02-13"
parent_id: "EN-402"
tags:
  - "epic-002"
  - "feat-005"
  - "enforcement"
effort: null
acceptance_criteria: |
  - All enforcement vectors scored against all evaluation criteria from TASK-001
  - Risk assessment findings from TASK-002 integrated into scoring
  - Trade study composition insights from TASK-003 factored into rankings
  - Ranked priority list produced with composite scores and clear ranking justification
  - Priority matrix artifact persisted to filesystem
due_date: null
activity: RESEARCH
original_estimate: null
remaining_work: null
time_spent: null
```

---

## Content

### Description

Apply the evaluation criteria from TASK-001, risk assessment from TASK-002, and trade study findings from TASK-003 to score all enforcement vectors. Produce a ranked priority list with composite scores that integrates effectiveness, cost, portability, maintainability, and risk dimensions.

### Acceptance Criteria

- [ ] All enforcement vectors scored against all evaluation criteria from TASK-001
- [ ] Risk assessment findings from TASK-002 integrated into scoring
- [ ] Trade study composition insights from TASK-003 factored into rankings
- [ ] Ranked priority list produced with composite scores and clear ranking justification
- [ ] Priority matrix artifact persisted to filesystem

### Implementation Notes

Depends on TASK-001, TASK-002, and TASK-003. This is the critical scoring step.

### Related Items

- Parent: [EN-402](../EN-402-enforcement-priority-analysis.md)
- Depends on: [TASK-001](./TASK-001-define-evaluation-criteria.md), [TASK-002](./TASK-002-risk-assessment-vectors.md), [TASK-003](./TASK-003-architecture-trade-study.md)
- Feeds into: [TASK-005](./TASK-005-create-formal-adr.md)

---

## Time Tracking

| Metric | Value |
|--------|-------|
| Original Estimate | -- |
| Remaining Work | -- |
| Time Spent | -- |

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| -- | -- | -- |

### Verification

- [ ] Acceptance criteria verified
- [ ] Reviewed by: --

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-12 | Created | Initial creation |
