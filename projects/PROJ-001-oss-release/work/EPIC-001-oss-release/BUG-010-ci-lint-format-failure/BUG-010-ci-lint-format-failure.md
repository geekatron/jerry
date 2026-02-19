# BUG-010: CI Lint & Format Failure — Unformatted E2E Test File

> **Type:** bug
> **Status:** done
> **Priority:** high
> **Impact:** high
> **Severity:** major
> **Created:** 2026-02-19
> **Due:** --
> **Completed:** 2026-02-19
> **Parent:** EPIC-001
> **Owner:** --
> **Found In:** 0.2.3
> **Fix Version:** --

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Brief description and key details |
| [Reproduction Steps](#reproduction-steps) | Steps to reproduce the issue |
| [Environment](#environment) | Environment where bug occurs |
| [Root Cause Analysis](#root-cause-analysis) | Investigation and root cause details |
| [Children (Tasks)](#children-tasks) | Task breakdown for fix |
| [Acceptance Criteria](#acceptance-criteria) | Conditions for bug to be fixed |
| [Related Items](#related-items) | Hierarchy and related work items |
| [History](#history) | Status changes and key events |

---

## Summary

The CI pipeline on PR #36 fails at the **Lint & Format** job because `tests/e2e/test_mkdocs_research_validation.py` does not conform to `ruff format` output style. The **CI Success** gate job fails downstream because it requires all jobs to pass. All other CI jobs (test-pip, test-uv, cli-integration, security, license, plugin validation, template validation) pass.

**Key Details:**
- **Symptom:** `ruff format --check` reports `1 file would be reformatted` — `tests/e2e/test_mkdocs_research_validation.py`
- **Frequency:** Every CI run on this branch
- **Workaround:** None — PR cannot be merged until CI is green

---

## Reproduction Steps

### Prerequisites

- Branch: `feat/proj-001-oss-documentation`
- PR #36 open against `main`

### Steps to Reproduce

1. Push any commit to `feat/proj-001-oss-documentation`
2. Observe CI run — Lint & Format job fails
3. CI Success gate job also fails (lint: failure)

### Expected Result

- `ruff format --check` passes with 0 files needing reformatting
- CI Success gate passes

### Actual Result

- `ruff format --check` reports: `Would reformat: tests/e2e/test_mkdocs_research_validation.py`
- 3 reformatting diffs: parenthesized assert messages that ruff wants to inline
- CI Success gate fails: `lint: failure`

---

## Environment

| Attribute | Value |
|-----------|-------|
| **Operating System** | ubuntu-latest (GitHub Actions) |
| **Runtime** | Python 3.14.2, ruff (CI-installed) |
| **Application Version** | Jerry 0.2.3 |
| **Configuration** | `pyproject.toml` ruff config, `.github/workflows/ci.yml` Lint & Format job |
| **Deployment** | GitHub Actions CI on PR #36 |

---

## Root Cause Analysis

### Investigation Summary

Ran `uv run ruff format --check tests/e2e/test_mkdocs_research_validation.py --diff` locally. Identified 3 locations where ruff wants to unwrap parenthesized assert messages into single-line or differently-wrapped format:

1. **Line 45-47**: `assert result.returncode == 0, (f"mkdocs build...")` — ruff wants single-line
2. **Line 96-99**: `assert not failures, ("Links with...")` — ruff wants different wrapping
3. **Line 120-123**: `assert not failures, ("Broken same-page...")` — ruff wants single-line

### Root Cause

The file was written with manually-wrapped assert message strings using explicit parenthesization. Ruff's formatter prefers to inline these when they fit within the line length limit, or wrap differently when they don't. The file was never run through `ruff format` before committing.

### Contributing Factors

- Pre-commit hooks are NOT installed in this worktree (dev-environment-warning at session start)
- BUG-009 had 4 commits across the adversary review cycle — none ran ruff format
- The CI pipeline catches this as a blocking failure, which is correct behavior

---

## Children (Tasks)

| ID | Title | Status | Effort |
|----|-------|--------|--------|
| TASK-001 | Run `ruff format` on the e2e test file | pending | 1 |

---

## Acceptance Criteria

### Fix Verification

- [x] AC-1: `uv run ruff format --check .` passes with 0 files needing reformatting
- [ ] AC-2: CI Lint & Format job passes on PR #36
- [ ] AC-3: CI Success gate job passes (all jobs green)

### Quality Checklist

- [x] Existing tests still passing
- [x] No new issues introduced

---

## Related Items

### Hierarchy

- **Parent:** [EPIC-001: OSS Release Preparation](../EPIC-001-oss-release.md)

### Related Items

- **Causing Change:** BUG-009 fix commits — introduced the unformatted test file
- **Related Bug:** [BUG-009](../BUG-009-research-section-broken-navigation/BUG-009-research-section-broken-navigation.md) — the bug fix that introduced this file
- **CI Run:** [PR #36 CI](https://github.com/geekatron/jerry/pull/36) — failing Lint & Format job

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-19 | Claude | pending | Created. CI Lint & Format fails on `tests/e2e/test_mkdocs_research_validation.py` — 3 parenthesized assert messages need ruff formatting. Blocks PR #36 merge. |
| 2026-02-19 | Claude | done | Fixed. Ran `uv run ruff format`, verified `ruff format --check .` (414 files clean), `ruff check` (0 errors), 3/3 e2e tests pass, 3171/3171 full suite pass. AC-2/AC-3 pending CI run. |

---
