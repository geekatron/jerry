# TASK-002: E2E test: every referenced pattern file exists

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

Create an E2E test that verifies every code pattern file referenced from `.context/rules/` or `.context/guides/` actually exists in `.context/patterns/`. Test should:

1. Scan all `.context/rules/*.md` and `.context/guides/*.md` files for pattern references
2. Extract referenced pattern file paths (e.g., `.context/patterns/command-handler.py`)
3. Assert every referenced pattern file exists on disk
4. Report orphaned patterns (exist but not referenced) as warnings

### Acceptance Criteria

- [ ] All referenced patterns exist
- [ ] No broken references
- [ ] Orphan report generated

### Implementation Notes

Test location: `tests/e2e/test_pattern_references.py`

Pattern references may appear as relative paths (e.g., `../patterns/command-handler.py`) or as descriptive references (e.g., "See `.context/patterns/` for reference"). The test should handle both explicit file paths and directory-level references. Use `pytest.mark.e2e` marker. Consider using regex to capture references in formats like backtick-wrapped paths, markdown links, and prose mentions.

### Related Items

- Parent: [EN-906: Fidelity Verification & Cross-Reference Testing](EN-906-fidelity-verification.md)
- Validates: EN-903 (pattern extraction), EN-901 (thinned rules), EN-902 (companion guides)

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| `tests/e2e/test_pattern_references.py` | Test | pending |

### Verification

- [ ] Acceptance criteria verified
- [ ] Tests pass
- [ ] Reviewed by: --

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-16 | Created | Initial creation. Part of EN-906 fidelity verification suite. |
