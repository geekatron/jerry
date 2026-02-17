# TASK-001: E2E test: every HARD rule has corresponding guide section

<!--
TEMPLATE: Task
VERSION: 0.1.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
-->

> **Type:** task
> **Status:** BACKLOG
> **Priority:** CRITICAL
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

Create an E2E test in `tests/e2e/` that verifies every one of the 24 HARD rules (H-01 through H-24) defined in `.context/rules/quality-enforcement.md` has a corresponding explanation in one of the companion guide files in `.context/guides/`. Test should:

1. Parse quality-enforcement.md to extract all H-XX rule IDs
2. Scan all files in `.context/guides/` for references to each H-XX rule ID
3. Assert 100% coverage (every HARD rule has at least one guide section explaining it)
4. Report which rules are covered and which are missing as test output

### Acceptance Criteria

- [ ] Test passes
- [ ] 24/24 HARD rules have guide coverage
- [ ] Test output shows coverage matrix

### Implementation Notes

Test location: `tests/e2e/test_rule_guide_coverage.py`

Use `pathlib.Path` for file traversal. The HARD rule IDs follow a consistent `H-XX` pattern where XX is zero-padded two digits. The test should be resilient to formatting variations (e.g., `H-01`, `H-1`, `H01`). Consider using `pytest.mark.e2e` marker.

### Related Items

- Parent: [EN-906: Fidelity Verification & Cross-Reference Testing](EN-906-fidelity-verification.md)
- Validates: EN-901 (thinned rules), EN-902 (companion guides)

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| `tests/e2e/test_rule_guide_coverage.py` | Test | pending |

### Verification

- [ ] Acceptance criteria verified
- [ ] Tests pass
- [ ] Reviewed by: --

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-16 | Created | Initial creation. Part of EN-906 fidelity verification suite. |
