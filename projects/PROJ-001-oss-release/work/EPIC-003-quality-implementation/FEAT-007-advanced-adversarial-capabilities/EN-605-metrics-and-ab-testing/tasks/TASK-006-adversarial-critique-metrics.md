# TASK-006: Adversarial critique of design, metrics validity, and statistical assumptions

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
id: "TASK-006"
work_type: TASK
title: "Adversarial critique of design, metrics validity, and statistical assumptions"
description: |
  Apply adversarial review to the metrics collection design, effectiveness
  scoring methodology, and A/B testing framework. Challenge metric validity,
  statistical assumptions, and dashboard utility.
classification: ENABLER
status: BACKLOG
resolution: null
priority: HIGH
assignee: "ps-critic"
created_by: "Claude"
created_at: "2026-02-12"
updated_at: "2026-02-13"
parent_id: "EN-605"
tags:
  - "epic-002"
  - "feat-007"
effort: null
acceptance_criteria: |
  - Adversarial critique completed with documented feedback
  - Metric validity challenged (do the metrics measure what they claim?)
  - Statistical assumptions in A/B testing reviewed and validated
  - Dashboard utility evaluated (is the output actionable for stakeholders?)
  - Critique findings persisted to filesystem under EN-605 directory
due_date: null
activity: TESTING
original_estimate: null
remaining_work: null
time_spent: null
```

---

## Content

### Description

Apply adversarial review to the metrics collection design, effectiveness scoring methodology, and A/B testing framework after end-to-end validation. Challenge metric validity (do the metrics actually measure what they claim?), review statistical assumptions in the A/B testing framework (are sample sizes adequate? is the randomization truly unbiased?), and evaluate dashboard utility (is the output actionable for stakeholders, or just noise?). The critique must ensure the measurement system is trustworthy and useful.

### Acceptance Criteria

- [ ] Adversarial critique completed with documented feedback
- [ ] Metric validity challenged (do the metrics measure what they claim?)
- [ ] Statistical assumptions in A/B testing reviewed and validated
- [ ] Dashboard utility evaluated (is the output actionable for stakeholders?)
- [ ] Critique findings persisted to filesystem under EN-605 directory

### Implementation Notes

- Requires TASK-005 end-to-end validation to complete before adversarial critique
- Apply Red Team and Devil's Advocate strategies
- Focus on Goodhart's Law risks identified in EN-602 research
- Challenge whether the dashboard output drives actual quality improvement

### Related Items

- Parent: [EN-605: Effectiveness Metrics Dashboard & A/B Testing Framework](../EN-605-metrics-and-ab-testing.md)
- Depends on: [TASK-005](./TASK-005-end-to-end-validation.md)

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
