# TASK-005: Regression test: compare guide content against git history baseline

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

Create a regression test that compares the content in `.context/guides/` against the original pre-optimization content recovered from git history (~314993a^). Test should:

1. Extract original rule file content from git history (the commit before EN-702 optimization)
2. Catalog all explanatory/educational content that was in the original files
3. Verify that every piece of educational content exists somewhere in the new `.context/guides/` files
4. Generate a content coverage metric (percentage of original content preserved)
5. Assert coverage >= 95% (allowing for minor formatting changes)

### Acceptance Criteria

- [ ] Coverage metric calculated
- [ ] >= 95% content preserved
- [ ] Regression report generated

### Implementation Notes

Test location: `tests/e2e/test_content_regression.py`

This test verifies the fidelity claim of the restructuring. The git commit for pre-optimization content needs to be identified precisely. The test should compare semantic content, not exact strings (allow reformatting). Consider using `subprocess` to invoke `git show` for historical content retrieval. Normalize whitespace and formatting before comparison. A line-by-line or paragraph-by-paragraph approach may work better than whole-file diff. The coverage metric should weight substantive content (explanations, examples, rationale) more heavily than structural elements (headers, separators, metadata). Consider using `pytest.mark.e2e` marker.

### Related Items

- Parent: [EN-906: Fidelity Verification & Cross-Reference Testing](EN-906-fidelity-verification.md)
- Validates: EN-901 (thinned rules), EN-902 (companion guides), overall restructuring fidelity

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| `tests/e2e/test_content_regression.py` | Test | pending |

### Verification

- [ ] Acceptance criteria verified
- [ ] Tests pass
- [ ] Reviewed by: --

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-16 | Created | Initial creation. Part of EN-906 fidelity verification suite. |
