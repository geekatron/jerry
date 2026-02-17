# TASK-003: Design Invocation Protocol for Adversarial Strategies

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
id: "TASK-003"
work_type: TASK
title: "Design invocation protocol for adversarial strategies"
description: |
  Design the protocol for requesting adversarial review within the /problem-solving skill.
  Support explicit mode selection, automatic mode selection via the EN-303 decision tree,
  multi-mode pipelines, and integration with /orchestration.
classification: ENABLER
status: BACKLOG
resolution: null
priority: CRITICAL
assignee: "ps-architect"
created_by: "Claude"
created_at: "2026-02-12"
updated_at: "2026-02-13"
parent_id: "EN-304"
tags:
  - "epic-002"
  - "feat-004"
effort: null
acceptance_criteria: |
  - Explicit mode selection protocol is defined with clear syntax
  - Automatic mode selection integrates with the EN-303 decision tree
  - Multi-mode pipeline protocol supports sequential strategy application
  - Integration points with /orchestration are identified and documented
  - Protocol is backward-compatible with existing ps-critic invocations
due_date: null
activity: DESIGN
original_estimate: null
remaining_work: null
time_spent: null
```

---

## Content

### Description

Design the protocol for requesting adversarial review within the /problem-solving skill. Support explicit mode selection (e.g., `ps-critic --mode red-team`), automatic mode selection (context-based using the EN-303 decision tree), multi-mode pipelines (e.g., Red Team then Blue Team), and integration with /orchestration for multi-phase adversarial workflows.

### Acceptance Criteria

- [ ] Explicit mode selection protocol is defined with clear syntax
- [ ] Automatic mode selection integrates with the EN-303 decision tree
- [ ] Multi-mode pipeline protocol supports sequential strategy application
- [ ] Integration points with /orchestration are identified and documented
- [ ] Protocol is backward-compatible with existing ps-critic invocations

### Implementation Notes

Depends on TASK-002 (mode design). Uses ps-architect agent. Defines how users and orchestrators invoke adversarial modes. Feeds into TASK-004 (implementation).

### Related Items

- Parent: [EN-304](../EN-304-problem-solving-skill-enhancement.md)
- Depends on: [TASK-002](./TASK-002-design-adversarial-mode-integration.md)
- Feeds into: [TASK-004](./TASK-004-implement-ps-critic-spec-updates.md)

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
