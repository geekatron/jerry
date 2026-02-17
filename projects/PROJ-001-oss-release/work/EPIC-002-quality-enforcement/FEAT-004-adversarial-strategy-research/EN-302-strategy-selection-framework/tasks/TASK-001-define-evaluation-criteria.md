# TASK-001: Define Evaluation Criteria and Weights

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
title: "Define evaluation criteria and weights"
description: |
  Define the evaluation dimensions and weighted criteria for scoring the 15 adversarial
  strategies from EN-301. Dimensions include effectiveness, applicability to LLM review
  contexts, complementarity, implementation complexity, cognitive load, and differentiation.
classification: ENABLER
status: COMPLETE
resolution: COMPLETED
priority: CRITICAL
assignee: "ps-analyst"
created_by: "Claude"
created_at: "2026-02-12"
updated_at: "2026-02-13"
parent_id: "EN-302"
tags:
  - "epic-002"
  - "feat-004"
effort: null
acceptance_criteria: |
  - At least 5 weighted evaluation criteria are defined
  - Each criterion has a clear definition, scoring rubric, and assigned weight
  - Weights reflect Jerry's priorities and sum to a consistent total
  - Criteria cover both effectiveness and practical applicability dimensions
  - Evaluation framework is documented and ready for use in TASK-004 scoring
due_date: null
activity: DESIGN
original_estimate: null
remaining_work: null
time_spent: null
```

---

## Content

### Description

Define the evaluation dimensions and weighted criteria for scoring the 15 adversarial strategies from EN-301. Dimensions include effectiveness (empirical evidence), applicability to LLM review contexts, complementarity with other strategies, implementation complexity, cognitive load on users, and differentiation from existing strategies. Assign weights reflecting Jerry's priorities for each dimension.

### Acceptance Criteria

- [x] At least 5 weighted evaluation criteria are defined
- [x] Each criterion has a clear definition, scoring rubric, and assigned weight
- [x] Weights reflect Jerry's priorities and sum to a consistent total
- [x] Criteria cover both effectiveness and practical applicability dimensions
- [x] Evaluation framework is documented and ready for use in TASK-004 scoring

### Implementation Notes

First of three parallel inputs to TASK-004 (scoring). Can run in parallel with TASK-002 (risk assessment) and TASK-003 (architecture trade study).

### Related Items

- Parent: [EN-302](../EN-302-strategy-selection-framework.md)
- Feeds into: [TASK-004](./TASK-004-score-and-select-top-10.md)

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
| Evaluation Criteria and Weighting Methodology | Framework Document | [deliverable-001-evaluation-criteria.md](../deliverable-001-evaluation-criteria.md) |

### Verification

- [ ] Acceptance criteria verified
- [ ] Reviewed by: --

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-12 | Created | Initial creation |
| 2026-02-13 | Complete | Evaluation framework created with 6 weighted dimensions, 1-5 rubrics, anchoring examples, Jerry-specific considerations, and sensitivity analysis guidance |
