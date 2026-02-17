# TASK-001: Verify bootstrap script does NOT symlink .context/guides/

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
> **Parent:** EN-905

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

Read `scripts/bootstrap_context.py` and verify it only symlinks `.context/rules/` and `.context/patterns/`. Confirm `.context/guides/` is not handled.

Specific verification steps:
1. Read the full content of `scripts/bootstrap_context.py`
2. Identify all symlink creation calls and their targets
3. Confirm that only `.context/rules/` and `.context/patterns/` are symlinked to `.claude/`
4. Confirm `.context/guides/` is NOT referenced in any symlink creation
5. Document current behavior for TASK-002 to build upon

### Acceptance Criteria

- [ ] Script behavior documented
- [ ] Confirmed guides not symlinked
- [ ] Current symlink targets cataloged
- [ ] Current behavior verified and documented

### Implementation Notes

This is a review/audit task. Read the script, trace the symlink logic, and document findings. If the script already handles guides (unexpected), escalate immediately as this would be a pre-existing defect.

### Related Items

- Parent: [EN-905: Bootstrap Exclusion & Validation](EN-905-bootstrap-exclusion.md)
- Blocks: TASK-002 (must verify current state before modifying)

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| Bootstrap behavior audit | Document | pending |

### Verification

- [ ] Acceptance criteria verified
- [ ] Script fully reviewed
- [ ] Reviewed by: --

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-16 | Created | Initial creation. Part of EN-905 bootstrap exclusion audit phase. |
