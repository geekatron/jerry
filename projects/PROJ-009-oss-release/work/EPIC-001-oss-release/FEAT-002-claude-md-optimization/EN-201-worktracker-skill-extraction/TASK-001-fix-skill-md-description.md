# TASK-001: Fix SKILL.md Description Bug

<!--
TEMPLATE: Task
SOURCE: ONTOLOGY-v1.md Section 3.4.6
VERSION: 1.0.0
-->

---

## Frontmatter

```yaml
id: "TASK-001"
work_type: TASK
title: "Fix SKILL.md Description Bug"
description: |
  The worktracker SKILL.md currently has a copy-paste bug from the transcript skill.
  Fix the description to accurately describe the worktracker skill functionality.

classification: ENABLER
status: BACKLOG
resolution: null
priority: HIGH
assignee: null
created_by: "Claude"
created_at: "2026-02-01T00:00:00Z"
updated_at: "2026-02-01T00:00:00Z"
parent_id: "EN-201"
tags:
  - enabler
  - bug-fix
  - worktracker

effort: 1
acceptance_criteria: |
  - SKILL.md description accurately describes worktracker functionality
  - No transcript skill content remains
  - Skill purpose is clear to users
due_date: null

activity: DOCUMENTATION
original_estimate: 1
remaining_work: 1
time_spent: null
```

---

## Content

### Description

The `skills/worktracker/SKILL.md` file currently contains copy-pasted content from the transcript skill. This needs to be fixed to accurately describe the worktracker skill's purpose and functionality.

### Acceptance Criteria

- [ ] Review current SKILL.md content for transcript references
- [ ] Write accurate description of worktracker skill purpose
- [ ] Update SKILL.md with correct description
- [ ] Verify no transcript skill content remains

### Implementation Notes

1. Read current `skills/worktracker/SKILL.md`
2. Identify all transcript-related content
3. Replace with worktracker-specific description
4. Include:
   - Purpose: Work tracking and task management
   - Entity types: Epic, Feature, Story, Task, etc.
   - Integration with WORKTRACKER.md files
   - Template usage guidance

### Related Items

- Parent: [EN-201: Worktracker Skill Extraction](./EN-201-worktracker-skill-extraction.md)
- Source: `skills/worktracker/SKILL.md`

---

## Time Tracking

| Metric | Value |
|---------|-------|
| Original Estimate | 1 hour |
| Remaining Work | 1 hour |
| Time Spent | 0 hours |

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| Fixed SKILL.md | Documentation | skills/worktracker/SKILL.md |

### Verification

- [ ] SKILL.md describes worktracker functionality
- [ ] No transcript references remain
- [ ] Reviewed by: -

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-01 | Created | Initial creation |
