# TASK-003: Add Brief TODO Mention in CLAUDE.md

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
| [Content](#content) | Description, target content, acceptance criteria |
| [Time Tracking](#time-tracking) | Effort metrics |
| [History](#history) | Change log |

---

## Frontmatter

```yaml
id: "TASK-003"
work_type: TASK
title: "Add Brief TODO Mention in CLAUDE.md"
description: |
  Add a brief mention of TODO/task tracking in the new CLAUDE.md quick
  reference section, pointing to the worktracker skill.

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
  - claude-md

effort: 0.5
acceptance_criteria: |
  - Brief TODO mention in CLAUDE.md
  - Points to worktracker skill for details
  - Does not add significant line count
due_date: null

activity: DOCUMENTATION
original_estimate: 0.5
remaining_work: 0.5
time_spent: null
```

---

## Content

### Description

Add a brief mention of TODO/task tracking capabilities in the new CLAUDE.md, directing users to the worktracker skill for detailed requirements.

### Target Content

Add to Quick Reference or Navigation section:

```markdown
**Task Tracking**: Use TaskCreate/TaskUpdate tools. See `/worktracker` for META TODO requirements.
```

### Acceptance Criteria

- [ ] Brief TODO mention added to CLAUDE.md
- [ ] Points to /worktracker skill
- [ ] Minimal line count impact (1-2 lines max)
- [ ] Clear and actionable

### Related Items

- Parent: [EN-203: TODO Section Migration](./EN-203-todo-section-migration.md)
- Target: CLAUDE.md (Quick Reference or Navigation section)

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
