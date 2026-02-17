# BUG-001: PR #13 CI Pipeline Failures

> **Type:** bug
> **Status:** in_progress
> **Priority:** critical
> **Impact:** high
> **Severity:** major
> **Created:** 2026-02-16T23:00:00Z
> **Due:** 2026-02-17
> **Completed:** —
> **Parent:** EPIC-003
> **Owner:** Claude
> **Found In:** feature/PROJ-001-oss-release-feat003 (commit f9b3e88)
> **Fix Version:** —

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Brief description and key details |
| [Reproduction Steps](#reproduction-steps) | Steps to reproduce the CI failures |
| [Environment](#environment) | CI environment details |
| [Root Cause Analysis](#root-cause-analysis) | Three root causes identified |
| [Fix Description](#fix-description) | Planned fixes |
| [Acceptance Criteria](#acceptance-criteria) | Conditions for resolution |
| [Children (Tasks)](#children-tasks) | 8 tasks across 3 groups |
| [Related Items](#related-items) | PR and epic references |
| [History](#history) | Status changes |

---

## Summary

PR #13 (EPIC-003 Quality Framework Implementation) has 14 failing CI jobs out of 24 total. The failures stem from 3 root causes: (A) 11 tests calling `uv run` in pip-only CI jobs where `uv` is not installed, (B) Windows PowerShell syntax errors from bash-style `\` line continuations in ci.yml, and (C/D) cascading gate/coverage failures from A+B.

**Key Details:**
- **Symptom:** 14 of 24 CI jobs failing on PR #13
- **Frequency:** Every push to the branch
- **Workaround:** None — PR cannot merge until CI is green

---

## Reproduction Steps

### Prerequisites

- Push any commit to `feature/PROJ-001-oss-release-feat003` branch

### Steps to Reproduce

1. Push commit to `feature/PROJ-001-oss-release-feat003`
2. Observe GitHub Actions CI workflow run
3. Check job results: 14 jobs fail

### Expected Result

All 24 CI jobs pass (lint, type check, security, test-pip, test-uv, CI gate, coverage report).

### Actual Result

10 jobs fail directly, `ci-success` gate fails, `coverage-report` is skipped:
- **8 test-pip jobs:** `FileNotFoundError: No such file or directory: 'uv'` — tests call `uv run` but pip-only jobs don't have `uv`
- **2 test-uv Windows jobs:** `ParserError` on line 7 of multi-line pytest command — PowerShell can't parse bash `\` continuations
- **ci-success:** Fails because upstream jobs failed
- **coverage-report:** Skipped because test-pip failed

---

## Environment

| Attribute | Value |
|-----------|-------|
| **Operating System** | ubuntu-latest, windows-latest, macos-latest |
| **Runtime** | Python 3.11, 3.12, 3.13, 3.14 |
| **Application Version** | feature/PROJ-001-oss-release-feat003 (commit f9b3e88) |
| **Configuration** | GitHub Actions CI (.github/workflows/ci.yml) |
| **Deployment** | GitHub Actions |

---

## Root Cause Analysis

### Root Cause A: uv-dependent tests in pip-only CI jobs (11 tests)

Tests in 3 files call `uv run` via subprocess but are NOT marked with `@pytest.mark.subprocess`. The `test-pip` CI job runs `pytest -m "not subprocess and not llm"` — these unmarked tests execute and fail with `FileNotFoundError: No such file or directory: 'uv'`.

**Affected files:**
- `tests/e2e/test_adversary_templates_e2e.py` — 2 tests
- `tests/e2e/test_quality_framework_e2e.py` — 8 tests
- `tests/integration/test_session_start_hook_integration.py` — 1 test

### Root Cause B: Windows PowerShell syntax errors (2 jobs)

The `test-uv` job in ci.yml uses bash-style `\` line continuations in the multi-line pytest command. Windows runners default to PowerShell, which cannot parse this syntax, causing `ParserError`.

**Affected jobs:** `Test uv (Python 3.13, windows-latest)`, `Test uv (Python 3.14, windows-latest)`

### Root Cause C/D: Cascading failures (2 jobs)

- `ci-success` gate job requires all upstream jobs to pass — fails because A+B fail
- `coverage-report` job depends on `test-pip` — skipped because test-pip fails

---

## Fix Description

### Solution Approach

**Group A fix:** Add `@pytest.mark.subprocess` to all 11 tests that invoke `uv` via subprocess. This ensures they are excluded from pip-only CI runs.

**Group B fix:** Add `shell: bash` to the test-uv job steps that use multi-line commands with `\` continuations. This ensures bash is used on all platforms including Windows.

**Group C/D fix:** No direct fix needed — cascading failures resolve automatically when A+B are fixed.

### Changes Planned

| File | Change Description |
|------|-------------------|
| `tests/e2e/test_adversary_templates_e2e.py` | Add `@pytest.mark.subprocess` to 2 tests |
| `tests/e2e/test_quality_framework_e2e.py` | Add `@pytest.mark.subprocess` to 8 tests |
| `tests/integration/test_session_start_hook_integration.py` | Add `@pytest.mark.subprocess` to 1 test |
| `.github/workflows/ci.yml` | Add `shell: bash` to test-uv steps with multi-line commands |

---

## Acceptance Criteria

### Fix Verification

- [ ] All 11 uv-dependent tests marked with `@pytest.mark.subprocess`
- [ ] pip-only CI jobs exclude subprocess-marked tests (verified by job output)
- [ ] Windows CI jobs pass (no PowerShell syntax errors)
- [ ] All 24 CI jobs pass on PR #13
- [ ] Coverage report posts to PR

### Quality Checklist

- [ ] No new issues introduced
- [ ] Existing tests still passing locally (`uv run pytest`)

---

## Children (Tasks)

| ID | Title | Status | Priority | Group |
|----|-------|--------|----------|-------|
| [TASK-001](./TASK-001-mark-adversary-tests-subprocess.md) | Mark adversary template E2E tests with subprocess marker | BACKLOG | critical | A |
| [TASK-002](./TASK-002-mark-quality-framework-tests-subprocess.md) | Mark quality framework E2E tests with subprocess marker | BACKLOG | critical | A |
| [TASK-003](./TASK-003-mark-session-hook-test-subprocess.md) | Mark session start hook integration test with subprocess marker | BACKLOG | critical | A |
| [TASK-004](./TASK-004-verify-pip-jobs-exclude-subprocess.md) | Verify pip jobs exclude subprocess-marked tests | BACKLOG | high | A |
| [TASK-005](./TASK-005-fix-ci-yml-windows-shell.md) | Fix ci.yml test-uv Windows shell syntax | BACKLOG | high | B |
| [TASK-006](./TASK-006-verify-windows-ci-pass.md) | Verify Windows CI jobs pass | BACKLOG | high | B |
| [TASK-007](./TASK-007-push-and-verify-ci-green.md) | Push fixes and verify all 24 CI jobs pass | BACKLOG | medium | C |
| [TASK-008](./TASK-008-verify-coverage-report.md) | Verify coverage report posts to PR | BACKLOG | medium | C |

---

## Related Items

### Hierarchy

- **Parent:** [EPIC-003 Quality Framework Implementation](../EPIC-003-quality-implementation.md)

### Related Items

- **PR:** [PR #13](https://github.com/geekatron/jerry/pull/13) — EPIC-003 Quality Framework Implementation
- **Branch:** `feature/PROJ-001-oss-release-feat003`

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-16 | Claude | in_progress | Initial report. 3 root causes, 8 tasks created. |

---
