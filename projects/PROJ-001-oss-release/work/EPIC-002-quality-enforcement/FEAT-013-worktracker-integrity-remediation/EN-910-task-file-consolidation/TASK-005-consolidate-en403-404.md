# TASK-005: Consolidate EN-403 and EN-404 task files

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

Merge EN-403 and EN-404 root-level task files into tasks/ subdirectories. Remove root-level duplicates. Both EN-403 and EN-404 currently have task files at both the enabler root level and within tasks/ subdirectories. The tasks/ subdirectory is the authoritative location.

Steps for each enabler (EN-403, EN-404):
1. Identify all TASK-*.md files at enabler root level
2. Compare with corresponding files in tasks/ subdirectory
3. Merge any content differences (keep most complete version)
4. Remove root-level TASK-*.md files
5. Update any internal references to use tasks/ paths

### Acceptance Criteria

- [ ] No TASK-*.md files remain at EN-403 root level
- [ ] No TASK-*.md files remain at EN-404 root level
- [ ] All task content preserved in tasks/ subdirectories
- [ ] No content lost during consolidation (diff verification)
- [ ] Internal references updated to tasks/ paths

### Implementation Notes

Handle EN-403 and EN-404 together as they are both in-progress enablers from FEAT-005 with similar consolidation needs. Use git diff to compare versions before merging.

### Related Items

- Parent: [EN-910: Task File Consolidation](EN-910-task-file-consolidation.md)
- Related: TASK-001 through TASK-004 (other consolidation tasks), TASK-006 (verification)

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| Consolidated EN-403 task files | Code change | pending |
| Consolidated EN-404 task files | Code change | pending |

### Verification

- [ ] Acceptance criteria verified
- [ ] No root-level TASK-*.md files remain in EN-403 or EN-404
- [ ] Reviewed by: --

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-16 | Created | Initial creation. Part of EN-910 task file consolidation. |
