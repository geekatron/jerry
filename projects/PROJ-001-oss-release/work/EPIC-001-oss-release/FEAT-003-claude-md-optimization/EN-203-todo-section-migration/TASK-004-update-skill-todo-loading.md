# TASK-004: Update Skill to Load TODO Rules

<!--
TEMPLATE: Task
SOURCE: ONTOLOGY-v1.md Section 3.4.6
VERSION: 1.0.0
-->

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Frontmatter](#frontmatter) | Task metadata |
| [Content](#content) | Description, updates required, acceptance criteria |
| [Time Tracking](#time-tracking) | Effort metrics |
| [History](#history) | Change log |

---

## Frontmatter

```yaml
id: "TASK-004"
work_type: TASK
title: "Update Skill to Load TODO Rules"
description: |
  Update the worktracker SKILL.md to include todo-integration.md in its
  navigation and ensure it loads on skill invocation.

classification: ENABLER
status: BACKLOG
resolution: null
priority: MEDIUM
assignee: null
created_by: "Claude"
created_at: "2026-02-01T00:00:00Z"
updated_at: "2026-02-01T00:00:00Z"
parent_id: "EN-203"
tags:
  - enabler
  - todo
  - skill

effort: 0.5
acceptance_criteria: |
  - SKILL.md navigation includes todo-integration.md
  - TODO rules load when skill invoked
  - Navigation description is clear
due_date: null

activity: DOCUMENTATION
original_estimate: 0.5
remaining_work: 0.5
time_spent: null
```

---

## Content

### Description

Update the worktracker SKILL.md to include the todo-integration.md rule file in its navigation table, ensuring TODO behavior rules are available when the skill is invoked.

### Update Required

Add to SKILL.md navigation table:

```markdown
| TODO behavior | rules/todo-integration.md |
```

### Acceptance Criteria

- [ ] Navigation table updated
- [ ] TODO rules referenced
- [ ] Skill loads TODO content on invocation
- [ ] Test invocation confirms content available

### Related Items

- Parent: [EN-203: TODO Section Migration](./EN-203-todo-section-migration.md)
- Target: skills/worktracker/SKILL.md

---

## Time Tracking

| Metric | Value |
|---------|-------|
| Original Estimate | 0.5 hours |
| Remaining Work | 0.5 hours |
| Time Spent | 0 hours |

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-01 | Created | Initial creation |
