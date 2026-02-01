# TASK-006: Validate All Pointers Resolve Correctly

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
| [Content](#content) | Description, dependencies, validation checklist |
| [Time Tracking](#time-tracking) | Effort metrics |
| [Evidence](#evidence) | Deliverables and verification |
| [History](#history) | Change log |

---

## Frontmatter

```yaml
id: "TASK-006"
work_type: TASK
title: "Validate All Pointers Resolve Correctly"
description: |
  Validate that all navigation pointers in the new CLAUDE.md resolve to
  existing files, directories, and skills.

classification: ENABLER
status: BACKLOG
resolution: null
priority: HIGH
assignee: null
created_by: "Claude"
created_at: "2026-02-01T00:00:00Z"
updated_at: "2026-02-01T00:00:00Z"
parent_id: "EN-202"
tags:
  - enabler
  - claude-md
  - validation

effort: 1
acceptance_criteria: |
  - All file/directory pointers resolve
  - All skill references valid
  - No 404s or missing targets
due_date: null

activity: TESTING
original_estimate: 1
remaining_work: 1
time_spent: null
```

---

## Content

### Description

After creating all sections, validate that every pointer in the new CLAUDE.md resolves to an actual target.

### Dependencies

This task depends on completion of:
- TASK-001: Create Identity section
- TASK-002: Create Navigation pointers section
- TASK-003: Create Active project section
- TASK-004: Create Critical constraints section
- TASK-005: Create Quick reference section

### Validation Checklist

#### File/Directory Pointers

| Pointer | Target | Exists |
|---------|--------|--------|
| `.claude/rules/` | Directory | [ ] |
| `.context/templates/` | Directory | [ ] |
| `docs/knowledge/` | Directory | [ ] |
| `docs/governance/JERRY_CONSTITUTION.md` | File | [ ] |
| `scripts/session_start_hook.py` | File | [ ] |

#### Skill References

| Skill | Exists | Loads |
|-------|--------|-------|
| `/worktracker` | [ ] | [ ] |
| `/problem-solving` | [ ] | [ ] |
| `/nasa-se` | [ ] | [ ] |
| `/orchestration` | [ ] | [ ] |
| `/architecture` | [ ] | [ ] |

#### External Links

| Link | Purpose | Works |
|------|---------|-------|
| Chroma Research | Context rot reference | [ ] |

### Acceptance Criteria

- [ ] All file pointers resolve to existing files
- [ ] All directory pointers resolve to existing directories
- [ ] All skill references are valid
- [ ] External links work (or marked as external)

### Related Items

- Parent: [EN-202: CLAUDE.md Rewrite](./EN-202-claude-md-rewrite.md)
- Dependencies: TASK-001 through TASK-005

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
| Validation Results | Documentation | (inline in this file) |

### Verification

- [ ] All pointers validated
- [ ] No missing targets
- [ ] Reviewed by: -

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-01 | Created | Initial creation |
