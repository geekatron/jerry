# EN-003: Fix Validation Test Regressions

> **Type:** enabler
> **Status:** done
> **Priority:** high
> **Impact:** high
> **Enabler Type:** infrastructure
> **Created:** 2026-02-11
> **Due:** —
> **Completed:** 2026-02-11
> **Parent:** FEAT-001
> **Owner:** —
> **Effort:** XS

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Brief description and technical scope |
| [Problem Statement](#problem-statement) | Why this enabler is needed |
| [Business Value](#business-value) | How enabler supports feature delivery |
| [Technical Approach](#technical-approach) | High-level technical approach |
| [Bugs](#bugs) | Bugs addressed by this enabler |
| [Tasks](#tasks) | Task inventory |
| [Progress Summary](#progress-summary) | Overall enabler progress |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done |
| [Evidence](#evidence) | Deliverables and verification |
| [Related Items](#related-items) | Hierarchy and related work |
| [History](#history) | Status changes and key events |

---

## Summary

Fix two CI regressions introduced by EN-001/TASK-002 (validation test creation). The validation test file `tests/contract/test_plugin_manifest_validation.py` has (1) an extraneous f-string prefix that fails Lint & Format CI, and (2) integration tests that assume `uv` is on PATH, which fails in all Test pip CI jobs.

**Technical Scope:**
- Remove extraneous f-string prefix in test assertion (lint fix)
- Add `pytest.mark.skipif` to skip uv-dependent tests when uv is not available

---

## Problem Statement

EN-001 fixed the Plugin Validation CI check but introduced two regressions in the test file created by TASK-002:

1. **Lint & Format** CI job now fails due to `f"[PASS]"` (extraneous f-prefix, no interpolation)
2. **Test pip (Python 3.11-3.14)** all fail with `FileNotFoundError: [Errno 2] No such file or directory: 'uv'`

These regressions mean the overall CI pipeline is still red despite EN-001's schema fix being correct.

---

## Business Value

Unblocks two of the remaining failing CI categories:
- Lint & Format (was previously passing, now regressed)
- Test pip (Python 3.11-3.14) (2 tests fail per version)

### Features Unlocked

- Restores Lint & Format CI to passing state
- Restores Test pip CI to passing state (for validation-related tests)
- Contributes to FEAT-001 goal of green CI pipeline

---

## Technical Approach

1. **TASK-001 (lint fix):** Remove extraneous `f` prefix from `f"[PASS]"` on line 370 — no interpolation needed
2. **TASK-002 (pip compatibility):** Add `@pytest.mark.skipif(shutil.which("uv") is None, ...)` to `TestValidationScriptIntegration` class so uv-dependent integration tests are skipped when uv is not installed

---

## Bugs

| ID | Title | Status | Priority |
|----|-------|--------|----------|
| [BUG-006](./BUG-006-validation-test-ci-regressions.md) | Validation test CI regressions from EN-001/TASK-002 | done | high |

---

## Tasks

| ID | Title | Status | Priority | Parent | Owner |
|----|-------|--------|----------|--------|-------|
| [TASK-001](./TASK-001-remove-extraneous-fstring.md) | Remove extraneous f-string prefix (lint fix) | DONE | HIGH | BUG-006 | — |
| [TASK-002](./TASK-002-skip-uv-tests-pip-ci.md) | Skip uv-dependent tests in pip CI environments | DONE | HIGH | BUG-006 | — |

---

## Progress Summary

### Status Overview

```
+------------------------------------------------------------------+
|                   ENABLER PROGRESS TRACKER                        |
+------------------------------------------------------------------+
| Tasks:     [####################] 100% (2/2 completed)            |
+------------------------------------------------------------------+
| Overall:   [####################] 100%                             |
+------------------------------------------------------------------+
```

### Progress Metrics

| Metric | Value |
|--------|-------|
| **Total Tasks** | 2 |
| **Completed Tasks** | 2 |
| **Completion %** | 100% |

---

## Acceptance Criteria

### Definition of Done

- [x] Extraneous f-string prefix removed (TASK-001)
- [x] uv-dependent tests skip when uv unavailable (TASK-002)
- [x] `uv run ruff check tests/contract/test_plugin_manifest_validation.py` passes
- [x] `uv run pytest tests/contract/test_plugin_manifest_validation.py` passes (11/11)
- [x] No regressions in existing test suite

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| Updated test file | Code | `tests/contract/test_plugin_manifest_validation.py` |

### Verification

- [x] `uv run ruff check` passes — `All checks passed!`
- [x] `uv run pytest tests/contract/test_plugin_manifest_validation.py -v` — `11 passed in 0.54s`
- [x] No regressions in validation tests

---

## Related Items

### Hierarchy

- **Parent:** [FEAT-001: Fix CI Build Failures](../FEAT-001-fix-ci-build-failures.md)

### Regression Source

- **Introduced By:** [EN-001/TASK-002: Add validation tests](../EN-001-fix-plugin-validation/TASK-002-add-validation-tests.md)

### CI Reference

- **CI Run:** [GitHub Actions #21893324775](https://github.com/geekatron/jerry/actions/runs/21893324775)

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-11 | Claude | done | Enabler created, both bugs fixed, all tasks complete. Regressions from EN-001/TASK-002 resolved. |
