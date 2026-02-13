# TASK-007: Code Review of All Modifications

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
id: "TASK-007"
work_type: TASK
title: "Code review of all modifications"
description: |
  Perform a comprehensive code review of all ps-critic agent spec modifications, SKILL.md
  updates, and PLAYBOOK.md updates. Verify consistency across all modified files and confirm
  backward compatibility.
classification: ENABLER
status: BACKLOG
resolution: null
priority: CRITICAL
assignee: "ps-reviewer"
created_by: "Claude"
created_at: "2026-02-12"
updated_at: "2026-02-13"
parent_id: "EN-304"
tags:
  - "epic-002"
  - "feat-004"
effort: null
acceptance_criteria: |
  - All modified files (agent spec, SKILL.md, PLAYBOOK.md) are reviewed
  - Mode definitions are consistent across agent spec and documentation
  - Backward compatibility with existing workflows is confirmed
  - No blocking issues identified (or all blocking issues resolved)
  - Review findings are documented with severity classifications
due_date: null
activity: TESTING
original_estimate: null
remaining_work: null
time_spent: null
```

---

## Content

### Description

Perform a comprehensive code review of all ps-critic agent spec modifications, SKILL.md updates, and PLAYBOOK.md updates. Verify consistency across all modified files, check for completeness of mode definitions, and confirm backward compatibility with existing /problem-solving workflows.

### Acceptance Criteria

- [ ] All modified files (agent spec, SKILL.md, PLAYBOOK.md) are reviewed
- [ ] Mode definitions are consistent across agent spec and documentation
- [ ] Backward compatibility with existing workflows is confirmed
- [ ] No blocking issues identified (or all blocking issues resolved)
- [ ] Review findings are documented with severity classifications

### Implementation Notes

Depends on TASK-004 (agent spec), TASK-005 (SKILL.md), and TASK-006 (PLAYBOOK.md). Uses ps-reviewer agent. Feeds into TASK-008 (adversarial review).

### Related Items

- Parent: [EN-304](../EN-304-problem-solving-skill-enhancement.md)
- Depends on: [TASK-004](./TASK-004-implement-ps-critic-spec-updates.md), [TASK-005](./TASK-005-update-skill-md.md), [TASK-006](./TASK-006-update-playbook-md.md)
- Feeds into: [TASK-008](./TASK-008-adversarial-review.md)

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
