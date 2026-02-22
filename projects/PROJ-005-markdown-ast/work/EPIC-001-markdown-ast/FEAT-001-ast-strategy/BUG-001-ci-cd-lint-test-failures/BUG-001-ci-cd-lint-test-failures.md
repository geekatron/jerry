# BUG-001: CI/CD lint and test failures on PR #48

> **Type:** bug
> **Status:** pending
> **Priority:** high
> **Impact:** high
> **Severity:** major
> **Created:** 2026-02-21
> **Parent:** FEAT-001-ast-strategy
> **Owner:** Claude
> **Found In:** feat/proj-005-markdown-ast @ f6d5e4c

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Bug overview |
| [Steps to Reproduce](#steps-to-reproduce) | How to reproduce |
| [Environment](#environment) | CI environment details |
| [Root Cause Analysis](#root-cause-analysis) | Two distinct root causes |
| [Acceptance Criteria](#acceptance-criteria) | Fix verification conditions |
| [Tasks](#tasks) | Fix tasks |
| [Related Items](#related-items) | Links to PR, workflows |
| [History](#history) | Change log |

---

## Summary

All CI/CD jobs on PR #48 (`feat/proj-005-markdown-ast`) are failing. Two distinct root causes identified:

1. **Lint failures (32 ruff errors):** The `r01_poc.py` PoC spike file has 32 ruff violations (unsorted imports, `zip()` without `strict=`, f-strings without placeholders, etc.). CI runs `ruff check .` on the entire repo, but local pre-commit hooks only check staged files, so these were never caught during development.

2. **Test failures (2 PROJ-006 + 1 flaky):** Two pre-existing `PROJ-006-multi-instance` test failures (incomplete project directory structure — only `decisions/` exists, needs 3+ category dirs). Plus 1 flaky Windows-only perf test (`test_50_file_frontmatter_batch_under_200ms`).

**Key Details:**
- **Symptom:** CI "Lint & Format" job exits 1 (32 ruff errors). All 16 test matrix jobs exit 1 (2 PROJ-006 failures each).
- **Frequency:** Every push to `feat/proj-005-markdown-ast` since branch creation
- **Workaround:** None for CI — the "CI Success" gate job fails, blocking merge

---

## Steps to Reproduce

### Prerequisites

- Push any commit to `feat/proj-005-markdown-ast` branch

### Steps to Reproduce

1. Push commit to `feat/proj-005-markdown-ast`
2. Observe GitHub Actions run (e.g., run `22257033157`)
3. "Lint & Format" fails with 32 ruff errors in `r01_poc.py`
4. All test matrix jobs fail with 2 PROJ-006 assertion errors

### Expected Result

All CI jobs pass. "CI Success" gate job reports success.

### Actual Result

- Lint & Format: `Found 32 errors` (exit code 1)
- Test jobs: `2 failed, N passed` (PROJ-006-multi-instance assertions)
- CI Success: `fail` (gates on all other jobs)

---

## Environment

| Attribute | Value |
|-----------|-------|
| **CI Platform** | GitHub Actions |
| **Run ID** | 22257033157 |
| **Branch** | feat/proj-005-markdown-ast |
| **Commit** | f6d5e4c |
| **Ruff Version** | 0.14.11 |
| **Python Versions** | 3.11, 3.12, 3.13, 3.14 |
| **OS Matrix** | ubuntu-latest, macos-latest, windows-latest |

---

## Root Cause Analysis

### Root Cause 1: PoC file not excluded from CI lint

The `r01_poc.py` file at `projects/PROJ-005-markdown-ast/work/EPIC-001-markdown-ast/FEAT-001-ast-strategy/EN-001-r01-poc/r01_poc.py` is a one-off proof-of-concept script written during EN-001. It was never intended to meet production lint standards. CI runs `ruff check .` across the entire repo, catching all 32 violations. Local pre-commit hooks only lint staged files, so developers never see these errors.

**Fix options:**
- A) Add `r01_poc.py` path to ruff `exclude` in `pyproject.toml`
- B) Fix the 32 lint errors in `r01_poc.py`
- C) Delete `r01_poc.py` (PoC served its purpose)

### Root Cause 2: PROJ-006 incomplete directory structure

`projects/PROJ-006-multi-instance/` only has a `decisions/` directory. Two project validation tests require >= 3 category directories (`research`, `synthesis`, `analysis`, `decisions`, `reports`, `design`). This is a pre-existing issue unrelated to PROJ-005 changes, but it blocks CI on this branch.

**Fix options:**
- A) Create missing category directories for PROJ-006
- B) Mark PROJ-006 tests as `xfail` or skip until PROJ-006 is properly set up

---

## Acceptance Criteria

### Fix Verification

- [ ] CI "Lint & Format" job passes (0 ruff errors)
- [ ] CI test jobs pass (0 failures, excluding known xfail/skip)
- [ ] CI "CI Success" gate job passes
- [ ] PR #48 is mergeable

### Quality Checklist

- [ ] Existing tests still passing
- [ ] No new issues introduced
- [ ] Pre-commit hooks installed in worktree

---

## Tasks

| ID | Task | Status |
|----|------|--------|
| TASK-001 | Fix ruff lint errors — exclude PoC from ruff + fix 22 pre-existing errors | in_progress |
| TASK-002 | Fix project validation tests — spec-driven expectations from worktracker rules | in_progress |

---

## Related Items

### Hierarchy

- **Parent:** [FEAT-001-ast-strategy](../FEAT-001-ast-strategy.md)

### Related Items

- **PR:** #48 (feat/proj-005-markdown-ast)
- **CI Run:** GitHub Actions run 22257033157
- **Causing Change:** Accumulated across multiple PROJ-005 commits

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-21 | Claude | pending | Initial report. 32 lint errors + 2 PROJ-006 test failures blocking CI. |
