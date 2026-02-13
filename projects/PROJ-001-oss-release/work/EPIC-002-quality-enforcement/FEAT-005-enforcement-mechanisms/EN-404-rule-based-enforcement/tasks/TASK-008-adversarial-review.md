# TASK-008: Adversarial Review (Red Team + Strawman)

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
id: "TASK-008"
work_type: TASK
title: "Adversarial review (Red Team + Strawman)"
description: |
  Apply adversarial review patterns to all rule-based enforcement implementations.
  Use Red Team pattern to identify bypass vectors and weaknesses in rule file
  enforcement, then Strawman pattern to challenge the overall approach and identify
  fundamental design flaws.
classification: ENABLER
status: BACKLOG
resolution: null
priority: HIGH
assignee: "ps-critic"
created_by: "Claude"
created_at: "2026-02-12"
updated_at: "2026-02-13"
parent_id: "EN-404"
tags:
  - "epic-002"
  - "feat-005"
  - "enforcement"
effort: null
acceptance_criteria: |
  - Red Team analysis completed identifying bypass vectors in all rule files
  - Strawman analysis completed challenging the overall enforcement approach
  - Enforcement weaknesses documented with severity and exploitability assessment
  - Actionable remediation items identified for creator revision in TASK-009
  - Adversarial review artifact persisted to filesystem
due_date: null
activity: TESTING
original_estimate: null
remaining_work: null
time_spent: null
```

---

## Content

### Description

Apply adversarial review patterns to all rule-based enforcement implementations. Use Red Team pattern to identify bypass vectors and weaknesses in rule file enforcement, then Strawman pattern to challenge the overall approach and identify fundamental design flaws.

### Acceptance Criteria

- [ ] Red Team analysis completed identifying bypass vectors in all rule files
- [ ] Strawman analysis completed challenging the overall enforcement approach
- [ ] Enforcement weaknesses documented with severity and exploitability assessment
- [ ] Actionable remediation items identified for creator revision in TASK-009
- [ ] Adversarial review artifact persisted to filesystem

### Implementation Notes

Depends on TASK-005, TASK-006, TASK-007 (all implementation tasks complete).

### Related Items

- Parent: [EN-404](../EN-404-rule-based-enforcement.md)
- Depends on: [TASK-005](./TASK-005-enhance-mandatory-skill-usage.md), [TASK-006](./TASK-006-enhance-project-workflow.md), [TASK-007](./TASK-007-create-quality-enforcement-rule.md)
- Feeds into: [TASK-009](./TASK-009-creator-revision.md)

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
