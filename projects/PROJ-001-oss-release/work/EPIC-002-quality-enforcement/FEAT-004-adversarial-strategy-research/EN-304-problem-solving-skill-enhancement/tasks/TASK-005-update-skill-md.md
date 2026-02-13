# TASK-005: Update SKILL.md with Adversarial Capabilities

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
id: "TASK-005"
work_type: TASK
title: "Update SKILL.md with adversarial capabilities"
description: |
  Update the /problem-solving SKILL.md to document all adversarial capabilities added to the
  skill, including available modes, usage examples, mode selection guidance, and integration
  with automatic mode selection via the EN-303 decision tree.
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
  - SKILL.md documents all 10 adversarial modes with descriptions
  - Usage examples are provided for explicit mode selection
  - Automatic mode selection via decision tree is documented
  - Multi-mode pipeline usage examples are included
  - Documentation follows the Triple-Lens format (L0/L1/L2)
due_date: null
activity: DOCUMENTATION
original_estimate: null
remaining_work: null
time_spent: null
```

---

## Content

### Description

Update the /problem-solving SKILL.md to document all adversarial capabilities added to the skill. Include available adversarial modes, usage examples for each mode, guidance on mode selection, multi-mode pipeline examples, and integration with automatic mode selection via the EN-303 decision tree.

### Acceptance Criteria

- [ ] SKILL.md documents all 10 adversarial modes with descriptions
- [ ] Usage examples are provided for explicit mode selection
- [ ] Automatic mode selection via decision tree is documented
- [ ] Multi-mode pipeline usage examples are included
- [ ] Documentation follows the Triple-Lens format (L0/L1/L2)

### Implementation Notes

Can run in parallel with TASK-006 (PLAYBOOK.md). Depends on TASK-004 (agent spec updates). Uses ps-architect agent. Feeds into TASK-007 (code review).

### Related Items

- Parent: [EN-304](../EN-304-problem-solving-skill-enhancement.md)
- Depends on: [TASK-004](./TASK-004-implement-ps-critic-spec-updates.md)
- Feeds into: [TASK-007](./TASK-007-code-review.md)

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
