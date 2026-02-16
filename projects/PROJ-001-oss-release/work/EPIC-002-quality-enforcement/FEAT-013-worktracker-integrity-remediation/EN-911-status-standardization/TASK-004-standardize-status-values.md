# TASK-004: Standardize status values across all enablers

<!--
TEMPLATE: Task
VERSION: 0.1.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
-->

> **Type:** task
> **Status:** BACKLOG
> **Priority:** MEDIUM
> **Activity:** DEVELOPMENT
> **Created:** 2026-02-16
> **Parent:** EN-911

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

Standardize all enabler status values to use "completed" instead of "done" where applicable. Some enabler files use "done" while others use "completed" as the status value for finished work. This inconsistency complicates automated validation and reporting.

Steps:
1. Grep all enabler files for status values containing "done"
2. Replace "done" with "completed" in frontmatter Status field
3. Update corresponding History entries if they reference "done" status
4. Verify no other status values are non-standard

Standard status values: pending, in_progress, completed, blocked, cancelled

### Acceptance Criteria

- [ ] No enabler files use "done" as status value
- [ ] All completed enablers use "completed" status
- [ ] Standard status vocabulary documented (pending, in_progress, completed, blocked, cancelled)
- [ ] History entries updated to reflect standardized terminology

### Implementation Notes

Search across all enabler files in FEAT-004, FEAT-005, and FEAT-006 directories. Only change the status value, not other content. The standard vocabulary should align with the worktracker ontology.

### Related Items

- Parent: [EN-911: Status Accuracy & Standardization](EN-911-status-standardization.md)
- Depends on: TASK-001 through TASK-003 (status corrections should be included in standardization sweep)

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| Standardized enabler status values | Code change | pending |

### Verification

- [ ] Acceptance criteria verified
- [ ] Grep confirms no "done" status values remain
- [ ] Reviewed by: --

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-16 | Created | Initial creation. Part of EN-911 status accuracy & standardization. |
