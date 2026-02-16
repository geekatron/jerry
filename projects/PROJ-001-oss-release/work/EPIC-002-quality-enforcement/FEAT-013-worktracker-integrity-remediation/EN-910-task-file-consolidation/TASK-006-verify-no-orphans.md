# TASK-006: Verify no orphan task files remain

<!--
TEMPLATE: Task
VERSION: 0.1.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
-->

> **Type:** task
> **Status:** BACKLOG
> **Priority:** HIGH
> **Activity:** REVIEW
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

Verify no orphan task files remain after consolidation. Run glob check to confirm all TASK-*.md files are located within tasks/ subdirectories (not at enabler root level) across all affected enablers (EN-301, EN-302, EN-401, EN-402, EN-403, EN-404).

Verification steps:
1. Run glob pattern `**/EN-*/TASK-*.md` across FEAT-004 and FEAT-005 work directories
2. Confirm zero matches (all task files should be in `**/EN-*/tasks/TASK-*.md`)
3. Run glob pattern `**/EN-*/tasks/TASK-*.md` to confirm all task files are in authoritative location
4. Cross-reference task file count against enabler task inventory tables

### Acceptance Criteria

- [ ] Glob `**/EN-*/TASK-*.md` returns zero matches in FEAT-004/FEAT-005
- [ ] Glob `**/EN-*/tasks/TASK-*.md` returns expected task file count
- [ ] Task file count matches enabler task inventory tables
- [ ] Verification report persisted as deliverable

### Implementation Notes

This is a verification task that depends on TASK-001 through TASK-005 completing. The glob patterns should be run from the FEAT-004 and FEAT-005 work directories to scope the search appropriately.

### Related Items

- Parent: [EN-910: Task File Consolidation](EN-910-task-file-consolidation.md)
- Depends on: TASK-001 through TASK-005 (consolidation must complete before verification)

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| Orphan verification report | Document | pending |

### Verification

- [ ] Acceptance criteria verified
- [ ] Glob check confirms no orphan task files
- [ ] Reviewed by: --

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-16 | Created | Initial creation. Part of EN-910 task file consolidation. |
