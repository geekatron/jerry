# TASK-004: E2E test: verify guides not in .claude/ after bootstrap

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

Create an E2E test in `tests/e2e/` that verifies `.claude/guides/` does NOT exist after running the bootstrap script. Test should:

1. Run `bootstrap_context.py` (or simulate its behavior)
2. Assert `.claude/guides/` does NOT exist as a symlink or directory
3. Assert `.claude/rules/` DOES exist (positive control)
4. Assert `.claude/patterns/` DOES exist (positive control)
5. Clean up any test artifacts

### Acceptance Criteria

- [ ] E2E test passes
- [ ] Covers negative case: `.claude/guides/` does not exist after bootstrap
- [ ] Covers positive cases: `.claude/rules/` and `.claude/patterns/` exist after bootstrap
- [ ] Test artifacts cleaned up after execution

### Implementation Notes

Test location: `tests/e2e/test_bootstrap_guides_exclusion.py`

This test validates the exclusion guard added in TASK-002. It should run the actual bootstrap script (or its core logic) against a temporary directory structure and verify the resulting symlink state. Use `tmp_path` pytest fixture for isolation and automatic cleanup.

### Related Items

- Parent: [EN-905: Bootstrap Exclusion & Validation](EN-905-bootstrap-exclusion.md)
- Depends on: TASK-002 (tests the guard that was added)

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| tests/e2e/test_bootstrap_guides_exclusion.py | Test | pending |

### Verification

- [ ] Acceptance criteria verified
- [ ] E2E test passes in CI
- [ ] Reviewed by: --

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-16 | Created | Initial creation. Part of EN-905 bootstrap exclusion validation phase. |
