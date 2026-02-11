# BUG-004: Transcript pipeline test finds no datasets

> **Type:** bug
> **Status:** pending
> **Priority:** medium
> **Impact:** medium
> **Severity:** major
> **Created:** 2026-02-10
> **Due:** —
> **Completed:** —
> **Parent:** EN-002
> **Owner:** —
> **Found In:** PR #6
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
| [Related Items](#related-items) | Hierarchy and related items |
| [History](#history) | Status changes |

---

## Summary

The transcript pipeline integration test `test_all_datasets_complete_under_30_seconds` fails with `AssertionError: Expected to process 6 datasets, only processed 0`. The test expects 6 test datasets to be available but finds none.

**Key Details:**
- **Symptom:** 0 of 6 expected datasets found
- **Frequency:** Every CI run (100%)
- **Workaround:** None — blocks CI

---

## Reproduction Steps

### Steps to Reproduce

1. Clone repository fresh
2. Run `uv run pytest tests/integration/transcript/test_pipeline.py::TestPythonPipeline::test_all_datasets_complete_under_30_seconds`

### Expected Result

Test finds 6 datasets and processes them.

### Actual Result

```
AssertionError: Expected to process 6 datasets, only processed 0
```

---

## Environment

| Attribute | Value |
|-----------|-------|
| **Operating System** | Ubuntu 24.04 (GitHub Actions) |
| **Runtime** | Python 3.11-3.14 (all versions) |
| **CI Job** | Test pip/uv (all variants) |

---

## Root Cause Analysis

### Investigation Summary

The test `test_all_datasets_complete_under_30_seconds` in `tests/integration/transcript/test_pipeline.py` is hardcoded to expect 6 VTT datasets in `skills/transcript/test_data/transcripts/golden/`:

- `meeting-001.vtt` through `meeting-005-roadmap-review.vtt` (5 files)
- `meeting-006-all-hands.vtt` (1 file)

The test asserts exactly 6 datasets processed with a 30-second time limit.

### Root Cause

**Test data not committed to git.** The `skills/transcript/test_data/transcripts/golden/` directory and its 6 VTT files do not exist in the repository. These files are either gitignored or were never committed. The test has hardcoded file references and no skip/discovery logic when files are missing.

### Fix Options

1. **Commit test data** — Add the 6 VTT test files to git (if they exist locally and are not too large)
2. **Skip when missing** — Add `pytest.mark.skipif` when golden dataset directory doesn't exist
3. **Dynamic discovery** — Change parametrize to discover available datasets, skip if none found
4. **Mock/fixtures** — Generate minimal test VTT files in test setup

### Files Involved

| File | Role | Change Needed |
|------|------|---------------|
| `tests/integration/transcript/test_pipeline.py` | Test file | Skip or discover datasets dynamically |
| `skills/transcript/test_data/transcripts/golden/` | Test data directory | Commit VTT files or skip tests |

---

## Acceptance Criteria

### Fix Verification

- [ ] Test finds and processes all expected datasets
- [ ] Or test is updated to work with available datasets / skip gracefully
- [ ] Fix works across Python 3.11-3.14

---

## Related Items

### Hierarchy

- **Parent:** [EN-002: Fix Test Infrastructure](./EN-002-fix-test-infrastructure.md)
- **Feature:** [FEAT-001: Fix CI Build Failures](../FEAT-001-fix-ci-build-failures.md)

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-10 | Claude | pending | Bug triaged from PR #6 CI failure |
| 2026-02-10 | Claude | pending | Root cause confirmed: 6 VTT test datasets in `skills/transcript/test_data/transcripts/golden/` not committed to git. Tests hardcoded to expect exactly 6 files. |
