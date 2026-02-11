# BUG-006: Validation test CI regressions from EN-001/TASK-002

> **Type:** bug
> **Status:** done
> **Priority:** high
> **Impact:** high
> **Severity:** major
> **Created:** 2026-02-11
> **Due:** —
> **Completed:** 2026-02-11
> **Parent:** EN-003
> **Owner:** —
> **Found In:** CI Run #21893324775
> **Fix Version:** —

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Brief description and key details |
| [Reproduction Steps](#reproduction-steps) | Steps to reproduce the issue |
| [Environment](#environment) | Environment where bug occurs |
| [Root Cause Analysis](#root-cause-analysis) | Investigation and root cause |
| [Acceptance Criteria](#acceptance-criteria) | Conditions for bug to be fixed |
| [Children (Tasks)](#children-tasks) | Task breakdown |
| [Evidence](#evidence) | Deliverables and verification |
| [Related Items](#related-items) | Hierarchy and related items |
| [History](#history) | Status changes |

---

## Summary

Two CI regressions introduced by EN-001/TASK-002 (validation test creation) in `tests/contract/test_plugin_manifest_validation.py`:

1. **Lint failure:** `f"[PASS]"` on line 370 — extraneous f-prefix with no interpolation. Ruff rule F541 flags this.
2. **Test pip failure:** `TestValidationScriptIntegration` calls `subprocess.run(["uv", ...])` but pip CI jobs don't have `uv` installed, causing `FileNotFoundError`.

**Key Details:**
- **Symptom 1:** Lint & Format CI fails with `Found 1 error` (extraneous f-prefix)
- **Symptom 2:** Test pip (Python 3.11-3.14) fails with `FileNotFoundError: [Errno 2] No such file or directory: 'uv'`
- **Frequency:** Every CI run (100%)
- **Workaround:** None — blocks CI
- **Note:** Test uv jobs pass (uv is available). Only Test pip and Lint & Format fail.

---

## Reproduction Steps

### Steps to Reproduce

1. Push any commit to PR #6
2. CI triggers Lint & Format and Test pip jobs
3. Lint & Format runs ruff check
4. Test pip runs pytest without uv on PATH

### Expected Result

Lint & Format passes. Test pip tests either pass or gracefully skip uv-dependent tests.

### Actual Result

```
# Lint & Format
tests/contract/test_plugin_manifest_validation.py:370:20
  F541 f-string without any placeholders
Found 1 error.

# Test pip (all Python versions)
FAILED tests/contract/test_plugin_manifest_validation.py::TestValidationScriptIntegration::test_all_manifests_pass_validation - FileNotFoundError: [Errno 2] No such file or directory: 'uv'
FAILED tests/contract/test_plugin_manifest_validation.py::TestValidationScriptIntegration::test_validation_script_uses_uv_run - FileNotFoundError: [Errno 2] No such file or directory: 'uv'
```

---

## Environment

| Attribute | Value |
|-----------|-------|
| **Operating System** | Ubuntu 24.04 (GitHub Actions) |
| **Runtime** | Python 3.11-3.14 / pip (no uv) |
| **CI Job** | Lint & Format, Test pip |
| **Ruff Version** | 0.14.11 |

---

## Root Cause Analysis

### Root Cause

Two defects in `tests/contract/test_plugin_manifest_validation.py` introduced by EN-001/TASK-002:

1. **F541 lint violation (line 370):** `assert f"[PASS]"` uses f-string prefix but `"[PASS]"` contains no interpolation placeholders. Ruff correctly flags this as F541 (f-string without placeholders).

2. **Missing uv availability guard:** `TestValidationScriptIntegration.test_all_manifests_pass_validation` and `test_validation_script_uses_uv_run` both call `subprocess.run(["uv", "run", "python", ...])`. When `uv` is not on PATH (pip CI environments), Python raises `FileNotFoundError` before the subprocess even starts. The existing skip logic in `test_validation_script_uses_uv_run` (lines 398-399) checks `result.stderr` for "uv: command not found" — but the `FileNotFoundError` exception occurs before `result` is created, so the skip never triggers.

### Contributing Factors

- TASK-002 adversarial critique cycle focused on test logic correctness, not CI environment compatibility
- Ruff was not run locally against the test file before commit (would have caught F541)
- The `test_validation_script_uses_uv_run` already had a partial skip mechanism, but it was unreachable due to the exception type

---

## Acceptance Criteria

### Fix Verification

- [x] Extraneous f-string prefix removed from line 370 (TASK-001)
- [x] `TestValidationScriptIntegration` class skips when `uv` is not on PATH (TASK-002)
- [x] `uv run ruff check tests/contract/test_plugin_manifest_validation.py` passes
- [x] `uv run pytest tests/contract/test_plugin_manifest_validation.py -v` passes (11/11)
- [x] No regression in other tests

---

## Children (Tasks)

| ID | Title | Status | Priority |
|----|-------|--------|----------|
| [TASK-001](./TASK-001-remove-extraneous-fstring.md) | Remove extraneous f-string prefix (lint fix) | DONE | HIGH |
| [TASK-002](./TASK-002-skip-uv-tests-pip-ci.md) | Skip uv-dependent tests in pip CI environments | DONE | HIGH |

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| Updated test file | Code | `tests/contract/test_plugin_manifest_validation.py` |

### Verification Results

**Ruff lint check:**
```
$ uv run ruff check tests/contract/test_plugin_manifest_validation.py
All checks passed!
```

**Pytest execution:**
```
$ uv run pytest tests/contract/test_plugin_manifest_validation.py -v
11 passed in 0.54s
```

---

## Related Items

### Hierarchy

- **Parent:** [EN-003: Fix Validation Test Regressions](./EN-003-fix-validation-test-regressions.md)
- **Feature:** [FEAT-001: Fix CI Build Failures](../FEAT-001-fix-ci-build-failures.md)

### Regression Source

- **Introduced By:** [EN-001/TASK-002: Add validation tests](../EN-001-fix-plugin-validation/TASK-002-add-validation-tests.md)

### CI Reference

- **CI Run:** [GitHub Actions #21893324775](https://github.com/geekatron/jerry/actions/runs/21893324775)

### Files Involved

| File | Role | Change Needed |
|------|------|---------------|
| `tests/contract/test_plugin_manifest_validation.py` | Validation test file | **Fix: remove f-prefix, add skipif** |

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-11 | Claude | done | Bug triaged from CI run #21893324775. Both root causes identified, fixes applied, all verification passed. |
