# TASK-006: Update PLAYBOOK.md with Adversarial Workflows

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
title: "Update PLAYBOOK.md with adversarial workflows"
description: |
  Update the /problem-solving PLAYBOOK.md to include adversarial workflow procedures.
  Document when to invoke adversarial review, how to interpret results, how to iterate
  on creator-critic cycles, and how to escalate unresolved findings.
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
  - PLAYBOOK.md includes adversarial workflow procedures for common scenarios
  - Step-by-step guidance covers when to invoke, interpret, and iterate
  - Creator-critic cycle workflow is documented with entry/exit criteria
  - Escalation path for unresolved findings is defined
  - Playbook procedures are consistent with SKILL.md documentation
due_date: null
activity: DOCUMENTATION
original_estimate: null
remaining_work: null
time_spent: null
```

---

## Content

### Description

Update the /problem-solving PLAYBOOK.md to include adversarial workflow procedures. Document when to invoke adversarial review, how to interpret results from each strategy mode, how to iterate on creator-critic cycles, and how to escalate unresolved adversarial findings. Include step-by-step workflow guidance for common adversarial scenarios.

### Acceptance Criteria

- [ ] PLAYBOOK.md includes adversarial workflow procedures for common scenarios
- [ ] Step-by-step guidance covers when to invoke, interpret, and iterate
- [ ] Creator-critic cycle workflow is documented with entry/exit criteria
- [ ] Escalation path for unresolved findings is defined
- [ ] Playbook procedures are consistent with SKILL.md documentation

### Implementation Notes

Can run in parallel with TASK-005 (SKILL.md). Depends on TASK-004 (agent spec updates). Uses ps-architect agent. Feeds into TASK-007 (code review).

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
