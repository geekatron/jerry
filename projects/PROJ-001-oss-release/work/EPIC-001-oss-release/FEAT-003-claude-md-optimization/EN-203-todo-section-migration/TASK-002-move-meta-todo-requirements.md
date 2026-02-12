# TASK-002: Move META TODO Requirements

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
| [Content](#content) | Description, dependencies, source content |
| [Time Tracking](#time-tracking) | Effort metrics |
| [History](#history) | Change log |

---

## Frontmatter

```yaml
id: "TASK-002"
work_type: TASK
title: "Move META TODO Requirements"
description: |
  Extract and migrate all META TODO requirements from CLAUDE.md to the
  todo-integration.md rule file.

classification: ENABLER
status: BACKLOG
resolution: null
priority: HIGH
assignee: null
created_by: "Claude"
created_at: "2026-02-01T00:00:00Z"
updated_at: "2026-02-01T00:00:00Z"
parent_id: "EN-203"
tags:
  - enabler
  - todo
  - migration

effort: 1
acceptance_criteria: |
  - All META TODO items extracted from CLAUDE.md
  - All items added to todo-integration.md
  - No META TODO items lost
due_date: null

activity: DOCUMENTATION
original_estimate: 1
remaining_work: 1
time_spent: null
```

---

## Content

### Description

Extract all META TODO requirements from the current CLAUDE.md `<todo>` section and add them to the todo-integration.md rule file.

### Dependencies

- TASK-001: Create todo-integration.md rule file

### Source Content (from CLAUDE.md `<todo>` section)

All items marked as "MUST ALWAYS BE ON LIST":
1. Project ID reminder
2. Update worktracker files reminder
3. Capture decisions reminder
4. Update files with progress reminder
5. Document bugs/discoveries/impediments reminder
6. Keep TODO up to date reminder
7. Keep TODO in sync with worktracker reminder
8. Keep work tracker entities up to date reminder
9. Keep orchestration artifacts up to date reminder
10. No shortcuts/hacks reminder
11. Ask questions reminder
12. Be truthful/accurate reminder
13. Document for three personas reminder
14. Research/analysis framework reminder
15. Context7/internet research reminder
16. Data+evidence driven decisions reminder
17. Persist analysis/findings reminder
18. Evidence-based decisions reminder
19. ASCII art/mermaid diagrams reminder

### Acceptance Criteria

- [ ] All 19+ META TODO items captured
- [ ] Items organized logically
- [ ] Clear formatting in rule file
- [ ] No content lost from CLAUDE.md

### Related Items

- Parent: [EN-203: TODO Section Migration](./EN-203-todo-section-migration.md)
- Source: CLAUDE.md `<todo>` section
- Target: skills/worktracker/rules/todo-integration.md

---

## Time Tracking

| Metric | Value |
|---------|-------|
| Original Estimate | 1 hour |
| Remaining Work | 1 hour |
| Time Spent | 0 hours |

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-01 | Created | Initial creation |
