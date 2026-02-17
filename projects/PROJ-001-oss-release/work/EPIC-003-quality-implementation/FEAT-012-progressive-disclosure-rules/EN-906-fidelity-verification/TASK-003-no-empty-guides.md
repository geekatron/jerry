# TASK-003: E2E test: no guide file is empty or stub-only

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

Create an E2E test that verifies no guide file in `.context/guides/` is empty or contains only stub content. Test should:

1. Scan all `.md` files in `.context/guides/`
2. Assert each file has > 100 lines of content (not a stub)
3. Assert each file has at least 3 major sections (## headings)
4. Assert no file contains placeholder text like "TODO", "TBD", "PLACEHOLDER"

### Acceptance Criteria

- [ ] All guide files have substantial content
- [ ] No stubs detected
- [ ] No placeholder text found

### Implementation Notes

Test location: `tests/e2e/test_guide_completeness.py`

Use `pathlib.Path` to enumerate guide files. Count lines excluding blank lines for the 100-line threshold. Use regex to find `##` headings (level-2 markdown headings) for section counting. Placeholder detection should be case-insensitive and match whole words to avoid false positives (e.g., "TODO" but not "todolist"). Consider using `pytest.mark.e2e` marker.

### Related Items

- Parent: [EN-906: Fidelity Verification & Cross-Reference Testing](EN-906-fidelity-verification.md)
- Validates: EN-902 (companion guides completeness)

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| `tests/e2e/test_guide_completeness.py` | Test | pending |

### Verification

- [ ] Acceptance criteria verified
- [ ] Tests pass
- [ ] Reviewed by: --

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-16 | Created | Initial creation. Part of EN-906 fidelity verification suite. |
