# TASK-005: Adversarial Review Iteration 1 (Red Team + Devil's Advocate)

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
id: "TASK-005"
work_type: TASK
title: "Adversarial review iteration 1 (Red Team + Devil's Advocate)"
description: |
  First adversarial review of the unified 15-strategy catalog using Red Team and Devil's
  Advocate critique patterns. Evaluate completeness, accuracy, citation quality,
  differentiation between strategies, and actionability. Quality target: >=0.92.
classification: ENABLER
status: BACKLOG
resolution: null
priority: CRITICAL
assignee: "ps-critic"
created_by: "Claude"
created_at: "2026-02-12"
updated_at: "2026-02-13"
parent_id: "EN-301"
tags:
  - "epic-002"
  - "feat-004"
effort: null
acceptance_criteria: |
  - Quality score calculated with weighted criteria breakdown
  - At least 3 improvement areas identified with specific recommendations
  - Red Team perspective: "What would a determined adversary exploit?"
  - Devil's Advocate perspective: "What assumptions are unexamined?"
  - Critique artifact persisted to filesystem (P-002)
due_date: null
activity: TESTING
original_estimate: null
remaining_work: null
time_spent: null
```

---

## Content

### Description

First adversarial review of the unified 15-strategy catalog using Red Team and Devil's Advocate critique patterns. Evaluate completeness, accuracy, citation quality, differentiation between strategies, and actionability. Quality target: >=0.92.

### Acceptance Criteria

- [ ] Quality score calculated with weighted criteria breakdown
- [ ] At least 3 improvement areas identified with specific recommendations
- [ ] Red Team perspective: "What would a determined adversary exploit?"
- [ ] Devil's Advocate perspective: "What assumptions are unexamined?"
- [ ] Critique artifact persisted to filesystem (P-002)

### Implementation Notes

Depends on TASK-004 (synthesis). Evaluation dimensions: Completeness (0.25), Accuracy (0.25), Differentiation (0.20), Actionability (0.15), Citation Quality (0.15). Feeds findings into TASK-006 for creator revision.

### Related Items

- Parent: [EN-301](../EN-301-deep-research-adversarial-strategies.md)
- Depends on: [TASK-004](./TASK-004-synthesis-unified-catalog.md)
- Feeds into: [TASK-006](./TASK-006-creator-revision.md)

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
| 2026-02-12 | Created | Initial creation. Blocked by TASK-004 (synthesis). |
