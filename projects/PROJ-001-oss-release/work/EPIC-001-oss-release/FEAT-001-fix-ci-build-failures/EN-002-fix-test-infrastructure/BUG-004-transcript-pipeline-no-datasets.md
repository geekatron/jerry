# BUG-004: Transcript pipeline test finds no datasets

> **Type:** bug
> **Status:** in_progress
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

**Test data not committed to git.** The entire `skills/transcript/test_data/transcripts/` directory (34 files, 606 KB) was never committed to the repository. The `.gitignore` does NOT exclude these files -- they were simply omitted. Other test_data/ subdirectories (contexts/, expected/, schemas/, expected_output/, validation/) were committed correctly.

See [research-transcript-data-migration-gap.md](./research-transcript-data-migration-gap.md) for full 5W2H investigation.

### Fix (Corrected)

**Add the 34 missing test data files to the repository.** Data is 606 KB total (git-friendly).

Previous options (skip guard, dynamic discovery, mock/fixtures) are **workarounds** that hide the data gap. The correct fix is to add the data.

### Files Involved

| File | Role | Change Needed |
|------|------|---------------|
| `tests/integration/transcript/test_pipeline.py` | Test file | Skip or discover datasets dynamically |
| `skills/transcript/test_data/transcripts/golden/` | Test data directory | Commit VTT files or skip tests |

---

## Children (Tasks)

| ID | Title | Status | Priority |
|----|-------|--------|----------|
| [TASK-001](./BUG-004--TASK-001-skip-pipeline-test-missing-datasets.md) | Restore missing transcript test data files | done | high |

---

## Acceptance Criteria

### Fix Verification

- [x] Test finds and processes all expected datasets (33 files added to repository)
- [x] Or test is updated to work with available datasets / skip gracefully
- [ ] Fix works across Python 3.11-3.14 (pending CI verification)

---

## Related Items

### Hierarchy

- **Parent:** [EN-002: Fix Test Infrastructure](./EN-002-fix-test-infrastructure.md)
- **Feature:** [FEAT-001: Fix CI Build Failures](../FEAT-001-fix-ci-build-failures.md)

### Children

- [TASK-001: Skip transcript pipeline combined test when golden datasets missing](./BUG-004--TASK-001-skip-pipeline-test-missing-datasets.md)

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-10 | Claude | pending | Bug triaged from PR #6 CI failure |
| 2026-02-10 | Claude | pending | Root cause confirmed: 6 VTT test datasets in `skills/transcript/test_data/transcripts/golden/` not committed to git. Tests hardcoded to expect exactly 6 files. |
| 2026-02-11 | Claude | pending | TASK-001 created (originally: skip guard). ps-investigator research revealed test data was never committed to git. TASK-001 reframed to "restore missing test data". Root cause updated. Research artifact: research-transcript-data-migration-gap.md |
| 2026-02-11 | Claude | done | TASK-001 completed. 33 test data files added to repository. All 56 transcript integration tests pass locally. Committed in `4789625`. |
| 2026-02-11 | Claude | in_progress | Reopened: unnecessary test data directories still contained PII (surname leak in mindmap, local paths with username in canonical JSON). Directories removed. References in parser-tests.yaml, index.schema.json, and research doc cleaned. |
