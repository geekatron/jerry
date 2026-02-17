# TASK-006: Implement Enhanced project-workflow.md

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
title: "Implement enhanced project-workflow.md"
description: |
  Enhance the project-workflow.md rule file with quality gate checkpoints at each workflow
  phase (Before, During, After). Add HARD enforcement language for mandatory quality checks
  and integrate tiered enforcement from TASK-003 to ensure appropriate rigor based on task
  complexity.
classification: ENABLER
status: BACKLOG
resolution: null
priority: HIGH
assignee: "ps-architect"
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
  - project-workflow.md updated with quality gate checkpoints for each phase
  - HARD enforcement language applied to mandatory quality checks
  - Tiered enforcement integrated for simple vs complex task workflows
  - Quality gate verification steps defined for Before/During/After phases
  - Backward compatibility maintained with existing project workflow
due_date: null
activity: DEVELOPMENT
original_estimate: null
remaining_work: null
time_spent: null
```

---

## Content

### Description

Enhance the project-workflow.md rule file with quality gate checkpoints at each workflow phase (Before, During, After). Add HARD enforcement language for mandatory quality checks and integrate tiered enforcement from TASK-003 to ensure appropriate rigor based on task complexity.

### Acceptance Criteria

- [ ] project-workflow.md updated with quality gate checkpoints for each phase
- [ ] HARD enforcement language applied to mandatory quality checks
- [ ] Tiered enforcement integrated for simple vs complex task workflows
- [ ] Quality gate verification steps defined for Before/During/After phases
- [ ] Backward compatibility maintained with existing project workflow

### Implementation Notes

Depends on TASK-003 (tiered strategy) and TASK-004 (HARD patterns). Can be done in parallel with TASK-005 and TASK-007.

### Related Items

- Parent: [EN-404](../EN-404-rule-based-enforcement.md)
- Depends on: [TASK-003](./TASK-003-design-tiered-enforcement.md), [TASK-004](./TASK-004-design-hard-enforcement-language.md)
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
