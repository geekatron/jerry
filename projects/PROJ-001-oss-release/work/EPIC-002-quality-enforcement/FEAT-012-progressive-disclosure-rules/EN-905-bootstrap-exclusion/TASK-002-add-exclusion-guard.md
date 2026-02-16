# TASK-002: Add explicit exclusion guard in bootstrap_context.py

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

Add an explicit exclusion guard in `scripts/bootstrap_context.py` to prevent `.context/guides/` from being symlinked. This should include:

1. Add a comment explaining WHY guides are excluded (progressive disclosure -- guides are on-demand only)
2. Add an explicit check that skips `.context/guides/` if it exists
3. Ensure the guard is in the main symlink creation loop/logic
4. Verify the script still correctly symlinks `.context/rules/` and `.context/patterns/`

### Acceptance Criteria

- [ ] Script has explicit guard preventing `.context/guides/` symlink
- [ ] Comment explains rationale (progressive disclosure, on-demand only)
- [ ] Existing symlinks for `.context/rules/` and `.context/patterns/` unaffected
- [ ] Script passes `--check` mode

### Implementation Notes

This task modifies `scripts/bootstrap_context.py` to add a defensive guard. Even if guides are not currently symlinked, an explicit exclusion with rationale protects against future regressions where someone might add guides to the symlink list without understanding the progressive disclosure architecture.

### Related Items

- Parent: [EN-905: Bootstrap Exclusion & Validation](EN-905-bootstrap-exclusion.md)
- Blocks: TASK-004 (E2E test depends on this guard being in place)
- Related: TASK-001 (depends on TASK-001 audit findings)

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| Modified bootstrap_context.py with exclusion guard | Code | pending |

### Verification

- [ ] Acceptance criteria verified
- [ ] Exclusion guard tested manually
- [ ] Reviewed by: --

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-16 | Created | Initial creation. Part of EN-905 bootstrap exclusion implementation phase. |
