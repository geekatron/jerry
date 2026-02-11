# EN-002: Fix Test Infrastructure

> **Type:** enabler
> **Status:** done
> **Priority:** medium
> **Impact:** medium
> **Enabler Type:** infrastructure
> **Created:** 2026-02-10
> **Due:** —
> **Completed:** 2026-02-11
> **Parent:** FEAT-001
> **Owner:** —
> **Effort:** —

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Brief description and technical scope |
| [Problem Statement](#problem-statement) | Why this enabler is needed |
| [Business Value](#business-value) | How enabler supports feature delivery |
| [Technical Approach](#technical-approach) | High-level technical approach |
| [Bugs](#bugs) | Bugs addressed by this enabler |
| [Progress Summary](#progress-summary) | Overall enabler progress |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done |
| [Related Items](#related-items) | Hierarchy and related work |
| [History](#history) | Status changes and key events |

---

## Summary

Fix two test infrastructure issues that cause CI failures: transcript pipeline tests expect test data that isn't committed to git, and project validation tests reference a stale project ID that doesn't exist.

**Technical Scope:**
- Fix transcript pipeline test data availability (BUG-004)
- Fix project validation test parameterization (BUG-005)

---

## Problem Statement

Two categories of CI test failures stem from test infrastructure issues, not application bugs:

1. **Transcript pipeline** (`test_all_datasets_complete_under_30_seconds`): Hardcoded to expect 6 VTT datasets in `skills/transcript/test_data/transcripts/golden/` which don't exist in the repository.
2. **Project validation** (4 tests): `project_id` fixture in `conftest.py` is hardcoded to `PROJ-001-plugin-cleanup` which doesn't exist. A dynamic `discover_projects()` function exists but isn't wired into the fixture.

Both block PR #6 merge across Python 3.11-3.14 on both pip and uv.

---

## Business Value

Resolves 2 of the 3 remaining CI failure categories, contributing to FEAT-001 completion and unblocking the OSS release.

### Features Unlocked

- PR #6 merge to main (contributes to FEAT-001 completion)
- Robust test suite that doesn't break on fresh clones

---

## Technical Approach

### BUG-004: Transcript Pipeline
Options under consideration:
1. **Skip when missing** — Add `pytest.mark.skipif` when golden dataset directory doesn't exist
2. **Dynamic discovery** — Change parametrize to discover available datasets, skip if none found
3. **Commit test data** — Add the 6 VTT test files to git (if not too large)

### BUG-005: Project Validation
Recommended approach:
1. **Use dynamic discovery** — Wire existing `discover_projects()` function into the `project_id` fixture
2. Ensure `PROJ-001-oss-release` has the required category directories (research, analysis, etc.)

---

## Bugs

| ID | Title | Status | Priority | Children |
|----|-------|--------|----------|----------|
| [BUG-004](./BUG-004-transcript-pipeline-no-datasets.md) | Transcript pipeline test finds no datasets | done | medium | TASK-001 |
| [BUG-005](./BUG-005-project-validation-missing-artifacts.md) | Project validation tests reference non-existent PROJ-001-plugin-cleanup | done | medium | TASK-001, TASK-002 |

### Tasks

| ID | Title | Parent | Status | Priority |
|----|-------|--------|--------|----------|
| [BUG-004/TASK-001](./BUG-004--TASK-001-skip-pipeline-test-missing-datasets.md) | Restore missing transcript test data from source-repository | BUG-004 | done | high |
| [BUG-005/TASK-001](./BUG-005--TASK-001-wire-dynamic-project-discovery.md) | Wire dynamic project discovery into fixture | BUG-005 | done | medium |
| [BUG-005/TASK-002](./BUG-005--TASK-002-create-category-directories.md) | Create category directories in PROJ-001-oss-release | BUG-005 | done | medium |

### Dependency Chain

```
BUG-004 ── TASK-001 (restore test data)        [independent - do first]

BUG-005 ── TASK-001 (dynamic discovery)  ──┐
                                            ├── Both needed for tests to pass
BUG-005 ── TASK-002 (category dirs)     ──┘
```

BUG-004/TASK-001 is fully independent and should be done first (data copy). BUG-005/TASK-001 and BUG-005/TASK-002 are co-dependent (both needed, but implementable in parallel).

**Research:** [Transcript Data Migration Gap](./research-transcript-data-migration-gap.md) — ps-investigator 5W2H analysis confirming BUG-004 root cause is data migration gap, not missing test infrastructure.

---

## Progress Summary

### Status Overview

```
+------------------------------------------------------------------+
|                   ENABLER PROGRESS TRACKER                        |
+------------------------------------------------------------------+
| Bugs:      [####################] 100% (2/2 resolved)             |
| Tasks:     [####################] 100% (3/3 completed)            |
+------------------------------------------------------------------+
| Overall:   [####################] 100%                             |
+------------------------------------------------------------------+
```

### Progress Metrics

| Metric | Value |
|--------|-------|
| **Total Bugs** | 2 |
| **Resolved Bugs** | 2 |
| **Total Tasks** | 3 |
| **Completed Tasks** | 3 |
| **Completion %** | 100% |

---

## Acceptance Criteria

### Definition of Done

- [x] Transcript pipeline tests pass or skip gracefully in CI (BUG-004) — 33 files restored, 56 tests pass
- [x] Project validation tests discover projects dynamically (BUG-005) — module-level discovery, 68 tests pass
- [ ] All Test pip/uv CI jobs pass across Python 3.11-3.14 (pending CI verification)
- [x] No hardcoded stale references in test fixtures

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| Updated test pipeline | Code | `tests/integration/transcript/test_pipeline.py` (BUG-004) |
| Updated conftest.py | Code | `tests/project_validation/conftest.py` (BUG-005) |

### Verification

- [x] `uv run pytest tests/integration/transcript/` passes — 56 passed
- [x] `uv run pytest tests/project_validation/` passes with dynamic discovery — 68 passed, 1 skipped
- [ ] All Test pip/uv CI jobs pass (pending CI verification)

---

## Related Items

### Hierarchy

- **Parent:** [FEAT-001: Fix CI Build Failures](../FEAT-001-fix-ci-build-failures.md)

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-10 | Claude | pending | Enabler created from FEAT-001 restructure. Groups BUG-004 and BUG-005. |
| 2026-02-11 | Claude | in_progress | 3 tasks created: BUG-004/TASK-001 (skip guard), BUG-005/TASK-001 (dynamic discovery), BUG-005/TASK-002 (category dirs). Dependency chain established. |
| 2026-02-11 | Claude | done | All 3 tasks completed with adversarial critic feedback loops. BUG-004: 33 test data files restored from source-repository. BUG-005: Dynamic discovery with sentinel pattern + synthesis/analysis/decisions dirs + orchestration in valid_categories. Full test suite: 2510 passed, 34 skipped. Committed in `4789625`, pushed to origin. |
