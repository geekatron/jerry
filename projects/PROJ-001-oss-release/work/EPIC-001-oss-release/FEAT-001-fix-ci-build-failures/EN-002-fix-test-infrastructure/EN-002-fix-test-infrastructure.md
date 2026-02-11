# EN-002: Fix Test Infrastructure

> **Type:** enabler
> **Status:** in_progress
> **Priority:** medium
> **Impact:** medium
> **Enabler Type:** infrastructure
> **Created:** 2026-02-10
> **Due:** —
> **Completed:** —
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
| [BUG-004](./BUG-004-transcript-pipeline-no-datasets.md) | Transcript pipeline test finds no datasets | pending | medium | TASK-001 |
| [BUG-005](./BUG-005-project-validation-missing-artifacts.md) | Project validation tests reference non-existent PROJ-001-plugin-cleanup | pending | medium | TASK-001, TASK-002 |

### Tasks

| ID | Title | Parent | Status | Priority |
|----|-------|--------|--------|----------|
| [BUG-004/TASK-001](./BUG-004--TASK-001-skip-pipeline-test-missing-datasets.md) | Restore missing transcript test data from jerry-core | BUG-004 | pending | high |
| [BUG-005/TASK-001](./BUG-005--TASK-001-wire-dynamic-project-discovery.md) | Wire dynamic project discovery into fixture | BUG-005 | pending | medium |
| [BUG-005/TASK-002](./BUG-005--TASK-002-create-category-directories.md) | Create category directories in PROJ-001-oss-release | BUG-005 | pending | medium |

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
| Bugs:      [....................] 0% (0/2 resolved)               |
| Tasks:     [....................] 0% (0/3 completed)              |
+------------------------------------------------------------------+
| Overall:   [....................] 0%                               |
+------------------------------------------------------------------+
```

### Progress Metrics

| Metric | Value |
|--------|-------|
| **Total Bugs** | 2 |
| **Resolved Bugs** | 0 |
| **Total Tasks** | 3 |
| **Completed Tasks** | 0 |
| **Completion %** | 0% |

---

## Acceptance Criteria

### Definition of Done

- [ ] Transcript pipeline tests pass or skip gracefully in CI (BUG-004)
- [ ] Project validation tests discover projects dynamically (BUG-005)
- [ ] All Test pip/uv CI jobs pass across Python 3.11-3.14
- [ ] No hardcoded stale references in test fixtures

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| Updated test pipeline | Code | `tests/integration/transcript/test_pipeline.py` (BUG-004) |
| Updated conftest.py | Code | `tests/project_validation/conftest.py` (BUG-005) |

### Verification

- [ ] `uv run pytest tests/integration/transcript/` passes or skips gracefully
- [ ] `uv run pytest tests/project_validation/` passes with dynamic discovery
- [ ] All Test pip/uv CI jobs pass

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
