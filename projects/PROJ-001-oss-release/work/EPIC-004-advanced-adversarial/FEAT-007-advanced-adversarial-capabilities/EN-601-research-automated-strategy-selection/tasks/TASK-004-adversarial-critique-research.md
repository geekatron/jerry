# TASK-004: Adversarial critique of research findings

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
title: "Adversarial critique of research findings"
description: |
  Apply adversarial review to the research produced by TASK-001, TASK-002,
  and TASK-003. Identify gaps, challenge assumptions, and stress-test the
  completeness of the survey. Use Red Team and Devil's Advocate strategies.
classification: ENABLER
status: BACKLOG
resolution: null
priority: CRITICAL
assignee: "ps-critic"
created_by: "Claude"
created_at: "2026-02-12"
updated_at: "2026-02-13"
parent_id: "EN-601"
tags:
  - "epic-002"
  - "feat-007"
effort: null
acceptance_criteria: |
  - Adversarial critique completed with documented feedback and creator responses
  - Research quality score >= 0.92 after adversarial review
  - Gaps and challenged assumptions documented with evidence
  - Critique artifact persisted to filesystem under EN-601 directory
due_date: null
activity: TESTING
original_estimate: null
remaining_work: null
time_spent: null
```

---

## Content

### Description

Apply adversarial review to the research findings from TASK-001 (context-based selection), TASK-002 (recommendation algorithms), and TASK-003 (adaptive review survey). Identify gaps in the literature coverage, challenge assumptions about the applicability of recommendation algorithms to strategy selection, and stress-test the completeness of the adaptive review survey. The critique must use Red Team and Devil's Advocate approaches to ensure the research foundation is robust before it feeds into the meta-analysis synthesis.

### Acceptance Criteria

- [ ] Adversarial critique completed with documented feedback and creator responses
- [ ] Research quality score >= 0.92 after adversarial review
- [ ] Gaps and challenged assumptions documented with evidence
- [ ] Critique artifact persisted to filesystem under EN-601 directory

### Implementation Notes

- Requires TASK-001, TASK-002, and TASK-003 to complete before this task can begin
- Apply both Red Team and Devil's Advocate adversarial strategies
- Focus on completeness of coverage, validity of assumptions, and actionability of findings
- Document specific gaps that need addressing before synthesis in TASK-005

### Related Items

- Parent: [EN-601: Deep Research: Automated Strategy Selection](../EN-601-research-automated-strategy-selection.md)
- Depends on: [TASK-001](./TASK-001-research-context-based-selection.md), [TASK-002](./TASK-002-research-recommendation-algorithms.md), [TASK-003](./TASK-003-survey-adaptive-review-systems.md)
- Downstream: [TASK-005](./TASK-005-meta-analysis-synthesis.md) (depends on this task)

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
