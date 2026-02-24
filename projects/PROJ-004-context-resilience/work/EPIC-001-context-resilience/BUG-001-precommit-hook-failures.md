# BUG-001: Pre-commit hooks failing — 10 test failures, SPDX violations, pyright errors

> **Type:** bug
> **Status:** completed
> **Priority:** high
> **Impact:** high
> **Severity:** major
> **Created:** 2026-02-21
> **Due:** --
> **Completed:** 2026-02-21
> **Parent:** EPIC-001
> **Owner:** --
> **Found In:** 0.5.0
> **Fix Version:** --

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Brief description and key details |
| [Steps to Reproduce](#steps-to-reproduce) | Steps to reproduce the issue |
| [Environment](#environment) | Environment where bug occurs |
| [Evidence](#evidence) | Bug documentation |
| [Acceptance Criteria](#acceptance-criteria) | Conditions for bug to be fixed |
| [Related Items](#related-items) | Hierarchy and related work items |
| [History](#history) | Status changes and key events |

---

## Summary

Three pre-commit hook categories are failing, requiring `SKIP=spdx-license-headers,pyright,pytest` to commit. This bypasses CI/CD quality gates and risks introducing regressions undetected.

**Key Details:**
- **Symptom:** `git commit` fails unless 3 hooks are skipped via SKIP env var
- **Frequency:** Every commit
- **Workaround:** `SKIP=spdx-license-headers,pyright,pytest git commit`

---

## Steps to Reproduce

### Prerequisites

- jerry-wt repo on `feat/proj-004-context-resilience` branch at commit `8750cc5`
- `uv sync` completed, pre-commit hooks installed

### Steps to Reproduce

1. Stage any file: `git add <file>`
2. Commit: `git commit -m "test: any message"`
3. Observe 3 hook failures

### Expected Result

All pre-commit hooks pass. Commit succeeds.

### Actual Result

3 hooks fail:

**1. spdx-license-headers (4 files):**
- `hooks/pre-compact.py` — missing SPDX + copyright headers
- `hooks/pre-tool-use.py` — missing SPDX + copyright headers
- `hooks/session-start.py` — missing SPDX + copyright headers
- `hooks/user-prompt-submit.py` — missing SPDX + copyright headers

**2. pyright (3+ type errors):**
- `src/bootstrap.py:634` — `str` not assignable to `Path` parameter
- `src/interface/cli/hooks/hooks_session_start_handler.py:124` — `Path` not assignable to `str` parameter
- Additional errors in hooks infrastructure

**3. pytest (10 failures):**
- `tests/contract/test_plugin_manifest_validation.py` — 2 failures (validation script integration)
- `tests/project_validation/architecture/test_path_conventions.py` — 2 failures (PROJ-006 missing structure, PROJ-004 cross-project ref)
- `tests/project_validation/integration/test_file_resolution.py` — 1 failure (PROJ-006 missing dirs)
- `tests/unit/orchestration/test_resumption_schema.py` — 1 failure (template missing recovery_state sub-section)
- `tests/unit/session_management/infrastructure/test_event_sourced_session_repository.py` — 4 failures (description/project_id not preserved through event replay)

---

## Environment

| Attribute | Value |
|-----------|-------|
| **Operating System** | macOS Darwin 24.6.0 |
| **Runtime** | Python 3.13 via UV |
| **Application Version** | jerry 0.5.0 |
| **Branch** | feat/proj-004-context-resilience |
| **Commit** | 8750cc5 |

---

## Evidence

### Bug Documentation

| Evidence | Type | Description | Date |
|----------|------|-------------|------|
| Pre-commit output | Log | Full hook output showing 3 categories of failures | 2026-02-21 |
| SKIP workaround | Workaround | `SKIP=spdx-license-headers,pyright,pytest` used for commit 8750cc5 | 2026-02-21 |

---

## Acceptance Criteria

### Fix Verification

- [x] `git commit` succeeds without any SKIP flags on a clean staging of changed files
- [x] All 4 hook wrapper scripts have SPDX + copyright headers
- [x] pyright passes on `src/` with zero errors
- [x] All 10 failing tests pass or are properly skipped with documented justification
- [x] No new test failures introduced

### Quality Checklist

- [x] Existing tests still passing
- [x] No new issues introduced
- [x] Pre-commit hooks run clean end-to-end

---

## Related Items

### Hierarchy

- **Parent:** [EPIC-001 Context Resilience](./EPIC-001-context-resilience.md)

### Related Items

- **Causing Change:** EN-006 (jerry hooks CLI), EN-007 (hook wrapper scripts) — introduced hook files without SPDX headers
- **Causing Change:** EN-001 (EventSourcedSessionRepository) — event replay may have introduced session description bug
- **Related:** PROJ-006-multi-instance — bootstrapped without full directory structure
- **GitHub Issue:** [#51](https://github.com/geekatron/jerry/issues/51)

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-21 | Claude | pending | Initial report. Discovered during commit of test suite (8750cc5). 3 hook categories failing. |
| 2026-02-21 | Claude | completed | All pre-commit hook failures resolved. Tests passing, SPDX compliant, pyright clean. |
