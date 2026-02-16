# TASK-002: Implement context analyzer (task type, complexity, domain, risk extraction)

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
title: "Implement context analyzer (task type, complexity, domain, risk extraction)"
description: |
  Build the context analysis engine that extracts task characteristics
  from the invocation context. Implement task type classification,
  complexity estimation, domain detection, and risk level assessment.
classification: ENABLER
status: BACKLOG
resolution: null
priority: HIGH
assignee: "ps-architect"
created_by: "Claude"
created_at: "2026-02-12"
updated_at: "2026-02-13"
parent_id: "EN-603"
tags:
  - "epic-002"
  - "feat-007"
effort: null
acceptance_criteria: |
  - Context analyzer extracts task type, complexity, domain, and risk from invocation context
  - Task type classification covers research, implementation, review, design, and testing categories
  - Complexity estimation accounts for multiple factors (LOC, components, dependency depth)
  - All code has type hints and docstrings per coding standards
  - Unit test coverage >= 90% for context analyzer components
due_date: null
activity: DEVELOPMENT
original_estimate: null
remaining_work: null
time_spent: null
```

---

## Content

### Description

Build the context analysis engine that extracts task characteristics from the invocation context. Implement task type classification (research, implementation, review, design, testing), complexity estimation (lines of code, number of components, dependency depth), domain detection (security, performance, correctness, usability), and risk level assessment (based on component criticality and change scope). The analyzer must produce a structured context object consumable by the recommendation engine.

### Acceptance Criteria

- [ ] Context analyzer extracts task type, complexity, domain, and risk from invocation context
- [ ] Task type classification covers research, implementation, review, design, and testing categories
- [ ] Complexity estimation accounts for multiple factors (LOC, components, dependency depth)
- [ ] All code has type hints and docstrings per coding standards
- [ ] Unit test coverage >= 90% for context analyzer components

### Implementation Notes

- Depends on TASK-001 architecture design for port/adapter interfaces
- Can execute in parallel with TASK-003 (recommendation engine) after TASK-001 completes
- Produce a structured context object (value object or DTO) as output
- Follow coding standards from `.claude/rules/coding-standards.md`

### Related Items

- Parent: [EN-603: Automated Strategy Selector Implementation](../EN-603-automated-strategy-selector.md)
- Depends on: [TASK-001](./TASK-001-design-selector-architecture.md)
- Parallel: [TASK-003](./TASK-003-implement-recommendation-engine.md)
- Downstream: [TASK-004](./TASK-004-code-review-selector.md) (depends on this task)

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
