# TASK-001: Define Evaluation Criteria and Weighting Methodology

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
id: "TASK-001"
work_type: TASK
title: "Define evaluation criteria and weighting methodology"
description: |
  Establish weighted evaluation criteria for scoring enforcement vectors across
  four dimensions: effectiveness, implementation cost, platform portability, and
  maintainability. Define a clear scoring methodology with justification for
  weight assignments that will be used in the priority matrix.
classification: ENABLER
status: DONE
resolution: completed
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
  - Evaluation criteria defined for effectiveness, implementation cost, platform portability, and maintainability
  - Weighting methodology established with clear justification for each weight
  - Scoring scale defined with rubric for each criterion
  - Methodology documented in a reusable format
  - Criteria reviewed for completeness and absence of bias
due_date: null
activity: DESIGN
original_estimate: null
remaining_work: null
time_spent: null
```

---

## Content

### Description

Establish weighted evaluation criteria for scoring enforcement vectors across four dimensions: effectiveness, implementation cost, platform portability, and maintainability. Define a clear scoring methodology with justification for weight assignments that will be used in the priority matrix.

### Acceptance Criteria

- [x] Evaluation criteria defined for effectiveness, implementation cost, platform portability, and maintainability (expanded to 7 dimensions: +CRR, +TOK, +BYP)
- [x] Weighting methodology established with clear justification for each weight (CRR 25%, EFF 20%, PORT 18%, TOK 13%, BYP 10%, COST 8%, MAINT 6%)
- [x] Scoring scale defined (1-5) with rubric for each criterion including anchoring examples
- [x] Methodology documented in a reusable format for consistent application across all vectors
- [x] Criteria reviewed for completeness and absence of bias (5 design principles, sensitivity analysis guidance)

### Implementation Notes

First task in EN-402. No dependencies within this enabler. Requires EN-401 research catalog as input.

### Related Items

- Parent: [EN-402](../EN-402-enforcement-priority-analysis.md)
- Feeds into: [TASK-002](./TASK-002-risk-assessment-vectors.md), [TASK-004](./TASK-004-create-priority-matrix.md)

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
| Evaluation Criteria and Weighting Methodology | Analysis Artifact | [deliverable-001-evaluation-criteria.md](../deliverable-001-evaluation-criteria.md) |

### Verification

- [ ] Acceptance criteria verified
- [ ] Reviewed by: --

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-12 | Created | Initial creation |
| 2026-02-13 | DONE | Completed by ps-analyst. 7-dimension framework with weighted composite scoring, rubrics, worked examples, and consumer guidance for TASK-002/003/004. |
