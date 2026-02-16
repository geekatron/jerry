# TASK-002: Consolidate EN-302 task files and fix TASK-006 ID

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

Merge EN-302 root-level task files into tasks/ subdirectory. Fix duplicate TASK-006 ID (rename TASK-006-critique-iteration-2.md to TASK-009). EN-302 has two issues: duplicate task files at root and tasks/ levels, and a duplicate TASK-006 identifier where two different tasks share the same ID.

Steps:
1. Identify all TASK-*.md files at EN-302 root level
2. Compare with corresponding files in EN-302/tasks/
3. Merge any content differences (keep most complete version)
4. Rename TASK-006-critique-iteration-2.md to TASK-009-critique-iteration-2.md to resolve ID collision
5. Remove root-level TASK-*.md files
6. Update EN-302 task inventory table to reflect the TASK-009 rename
7. Update any internal references to use tasks/ paths

### Acceptance Criteria

- [ ] No TASK-*.md files remain at EN-302 root level
- [ ] No duplicate TASK-006 ID exists
- [ ] TASK-006-critique-iteration-2.md renamed to TASK-009
- [ ] EN-302 task inventory table updated with TASK-009
- [ ] All task content preserved in tasks/ subdirectory

### Implementation Notes

The TASK-006 duplicate is particularly important to resolve as it breaks unique identification. Ensure the renamed task file has its internal references updated (Parent, History, etc.).

### Related Items

- Parent: [EN-910: Task File Consolidation](EN-910-task-file-consolidation.md)
- Related: TASK-001, TASK-003 through TASK-005 (other consolidation tasks), TASK-006 (verification)

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| Consolidated EN-302 task files | Code change | pending |
| Renamed TASK-009 | Code change | pending |

### Verification

- [ ] Acceptance criteria verified
- [ ] No duplicate TASK-006 ID
- [ ] No root-level TASK-*.md files remain
- [ ] Reviewed by: --

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-16 | Created | Initial creation. Part of EN-910 task file consolidation. |
