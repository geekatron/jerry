# TASK-004: Implement ps-critic Agent Spec Updates

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
title: "Implement ps-critic agent spec updates"
description: |
  Update the ps-critic agent specification with adversarial mode definitions, prompt templates,
  and configuration for all 10 selected strategies. This is specification-level work (markdown
  agent definitions), not Python code changes.
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
  - ps-critic agent spec is updated with all 10 adversarial mode definitions
  - Each mode has a complete prompt template ready for use
  - Evaluation criteria and output format are specified per mode
  - Applicability metadata from EN-303 is embedded in each mode definition
  - Agent spec changes are backward-compatible with existing ps-critic behavior
due_date: null
activity: DEVELOPMENT
original_estimate: null
remaining_work: null
time_spent: null
```

---

## Content

### Description

Update the ps-critic agent specification with adversarial mode definitions, prompt templates, and configuration for all 10 selected strategies. This is specification-level work (markdown agent definitions), not Python code changes. Each mode definition includes the strategy name, prompt template, evaluation criteria, output format, and applicability metadata.

### Acceptance Criteria

- [ ] ps-critic agent spec is updated with all 10 adversarial mode definitions
- [ ] Each mode has a complete prompt template ready for use
- [ ] Evaluation criteria and output format are specified per mode
- [ ] Applicability metadata from EN-303 is embedded in each mode definition
- [ ] Agent spec changes are backward-compatible with existing ps-critic behavior

### Implementation Notes

Depends on TASK-003 (invocation protocol). Uses ps-architect agent. Core implementation task. Feeds into TASK-005, TASK-006, and TASK-007 (documentation and review).

### Related Items

- Parent: [EN-304](../EN-304-problem-solving-skill-enhancement.md)
- Depends on: [TASK-003](./TASK-003-design-invocation-protocol.md)
- Feeds into: [TASK-005](./TASK-005-update-skill-md.md), [TASK-006](./TASK-006-update-playbook-md.md), [TASK-007](./TASK-007-code-review.md)

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
