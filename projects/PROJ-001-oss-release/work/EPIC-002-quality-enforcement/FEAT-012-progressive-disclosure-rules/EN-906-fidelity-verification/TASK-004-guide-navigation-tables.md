# TASK-004: E2E test: all guide files have navigation tables

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
> **Parent:** EN-906

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

Create an E2E test that verifies all companion guide files in `.context/guides/` have proper navigation tables per H-23/H-24. Test should:

1. Scan all `.md` files in `.context/guides/`
2. Assert each file has a "Document Sections" table (or equivalent navigation table)
3. Assert navigation table entries use anchor links (H-24 compliance)
4. Assert anchor links resolve to actual headings in the same file

### Acceptance Criteria

- [ ] All guides have navigation tables
- [ ] All anchor links valid
- [ ] H-23/H-24 compliance verified

### Implementation Notes

Test location: `tests/e2e/test_guide_navigation.py`

Use regex to detect the navigation table pattern. The table header typically follows `| Section | Purpose |` with a separator line `|---------|---------|`. Anchor links follow the pattern `\[.+\]\(#.+\)`. For anchor link validation, extract the anchor target (e.g., `#some-section`) and verify a corresponding heading exists in the file by converting headings to their anchor form (lowercase, spaces to hyphens, remove special characters). Be flexible about exact column names but strict about anchor link presence. Consider using `pytest.mark.e2e` marker.

### Related Items

- Parent: [EN-906: Fidelity Verification & Cross-Reference Testing](EN-906-fidelity-verification.md)
- Validates: EN-902 (companion guides), H-23/H-24 compliance

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| `tests/e2e/test_guide_navigation.py` | Test | pending |

### Verification

- [ ] Acceptance criteria verified
- [ ] Tests pass
- [ ] Reviewed by: --

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-16 | Created | Initial creation. Part of EN-906 fidelity verification suite. |
