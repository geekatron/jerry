# TASK-001: Consolidate EN-301 task files

<!--
TEMPLATE: Task
VERSION: 0.1.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
-->

> **Type:** task
> **Status:** BACKLOG
> **Priority:** HIGH
> **Activity:** DEVELOPMENT
> **Created:** 2026-02-16
> **Parent:** EN-910

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Content](#content) | Description, acceptance criteria, implementation notes |
| [Evidence](#evidence) | Deliverables and verification |
| [History](#history) | Status changes and key events |

---

## Content

### Description

Merge EN-301 root-level task files into tasks/ subdirectory. Remove root-level duplicates. EN-301 currently has task files at both the enabler root level and within a tasks/ subdirectory. The tasks/ subdirectory is the authoritative location.

Steps:
1. Identify all TASK-*.md files at EN-301 root level
2. Compare with corresponding files in EN-301/tasks/
3. Merge any content differences (keep most complete version)
4. Remove root-level TASK-*.md files
5. Update any internal references to use tasks/ paths

### Acceptance Criteria

- [ ] No TASK-*.md files remain at EN-301 root level
- [ ] All task content preserved in tasks/ subdirectory
- [ ] No content lost during consolidation (diff verification)
- [ ] Internal references updated to tasks/ paths

### Implementation Notes

Use git diff to compare root-level and tasks/ versions before merging. If versions differ, merge manually keeping the most complete content. Preserve git history by using git mv where possible.

### Related Items

- Parent: [EN-910: Task File Consolidation](EN-910-task-file-consolidation.md)
- Related: TASK-002 through TASK-005 (other consolidation tasks), TASK-006 (verification)

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| Consolidated EN-301 task files | Code change | pending |

### Verification

- [ ] Acceptance criteria verified
- [ ] No root-level TASK-*.md files remain
- [ ] Reviewed by: --

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-16 | Created | Initial creation. Part of EN-910 task file consolidation. |
