# TASK-002: Define effectiveness scoring methodology (formulas, weights, confidence)

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
id: "TASK-002"
work_type: TASK
title: "Define effectiveness scoring methodology (formulas, weights, confidence)"
description: |
  Implement the effectiveness scoring methodology based on EN-602 research
  findings. Define defect detection rate, review thoroughness score, false
  positive rate, composite effectiveness score, and confidence intervals.
classification: ENABLER
status: BACKLOG
resolution: null
priority: HIGH
assignee: "ps-analyst"
created_by: "Claude"
created_at: "2026-02-12"
updated_at: "2026-02-13"
parent_id: "EN-605"
tags:
  - "epic-002"
  - "feat-007"
effort: null
acceptance_criteria: |
  - Per-strategy effectiveness score computed with defect detection rate, thoroughness, and false positive rate
  - Composite effectiveness score calculated with configurable weights
  - Confidence intervals computed for all scores based on sample size
  - Trend analysis tracks effectiveness scores over time periods
  - All code has type hints and docstrings per coding standards
due_date: null
activity: DEVELOPMENT
original_estimate: null
remaining_work: null
time_spent: null
```

---

## Content

### Description

Implement the effectiveness scoring methodology based on EN-602 research findings. Define and implement defect detection rate (defects found / total defects estimated), review thoroughness score (coverage of review dimensions), false positive rate (invalid findings / total findings), and a composite effectiveness score as a weighted combination of the above metrics. Compute confidence intervals for each score based on sample size. The scoring methodology must support configurable weights for the composite score.

### Acceptance Criteria

- [ ] Per-strategy effectiveness score computed with defect detection rate, thoroughness, and false positive rate
- [ ] Composite effectiveness score calculated with configurable weights
- [ ] Confidence intervals computed for all scores based on sample size
- [ ] Trend analysis tracks effectiveness scores over time periods
- [ ] All code has type hints and docstrings per coding standards

### Implementation Notes

- Based on EN-602 research findings for scoring methodology
- Can execute in parallel with TASK-001 and TASK-003
- Scoring formulas should be configurable (weights as parameters)
- Follow coding standards from `.claude/rules/coding-standards.md`

### Related Items

- Parent: [EN-605: Effectiveness Metrics Dashboard & A/B Testing Framework](../EN-605-metrics-and-ab-testing.md)
- Parallel: [TASK-001](./TASK-001-design-metrics-collection-architecture.md), [TASK-003](./TASK-003-implement-ab-testing-framework.md)
- Downstream: [TASK-004](./TASK-004-qa-testing-metrics-ab.md) (depends on this task)

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
