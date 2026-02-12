# TASK-004: Test Navigation Pointers Resolve

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
| [Content](#content) | Description, checklist, issues |
| [Time Tracking](#time-tracking) | Effort metrics |
| [History](#history) | Change log |

---

## Frontmatter

```yaml
id: "TASK-004"
work_type: TASK
title: "Test Navigation Pointers Resolve"
description: |
  Test that all navigation pointers in the new CLAUDE.md resolve
  to existing targets.

classification: ENABLER
status: BACKLOG
resolution: null
priority: HIGH
assignee: null
created_by: "Claude"
created_at: "2026-02-01T00:00:00Z"
updated_at: "2026-02-01T00:00:00Z"
parent_id: "EN-204"
tags:
  - enabler
  - validation
  - navigation

effort: 1
acceptance_criteria: |
  - All file/directory pointers resolve
  - All skill references work
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

Systematically verify that every pointer in the new CLAUDE.md resolves to an actual target file, directory, or skill.

### Navigation Pointer Checklist

#### File/Directory Pointers

| Pointer | Target | Verification | Pass |
|---------|--------|--------------|------|
| `.claude/rules/` | Directory | `ls -la .claude/rules/` | [ ] |
| `.context/templates/` | Directory | `ls -la .context/templates/` | [ ] |
| `docs/knowledge/` | Directory | `ls -la docs/knowledge/` | [ ] |
| `docs/governance/JERRY_CONSTITUTION.md` | File | `ls docs/governance/` | [ ] |

#### Skill References

| Skill | Verification | Pass |
|-------|--------------|------|
| `/worktracker` | Invoke skill | [ ] |
| `/problem-solving` | Invoke skill | [ ] |
| `/nasa-se` | Invoke skill | [ ] |
| `/orchestration` | Invoke skill | [ ] |
| `/architecture` | Invoke skill | [ ] |

#### External Links

| Link | Verification | Pass |
|------|--------------|------|
| Chroma Research | Open in browser | [ ] |

### Acceptance Criteria

- [ ] All directories exist
- [ ] All files exist
- [ ] All skills invoke
- [ ] External links work (or marked as external)

### Issues Found

| Issue | Severity | Resolution |
|-------|----------|------------|
| - | - | - |

### Related Items

- Parent: [EN-204: Validation & Testing](./EN-204-validation-testing.md)

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
