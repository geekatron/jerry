# BUG-001: Context Monitoring Tests Fail on 1M Context Window

> **Type:** bug
> **Status:** completed
> **Priority:** critical
> **Severity:** critical
> **Impact:** critical
> **Created:** 2026-03-30T00:00:00Z
> **Completed:** 2026-03-30T00:00:00Z
> **Parent:** FEAT-001
> **Owner:**
> **Effort:** 3
> **GitHub Issue:** [#226](https://github.com/geekatron/jerry/issues/226)

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What's broken |
| [Steps to Reproduce](#steps-to-reproduce) | How to observe the failure |
| [Root Cause](#root-cause) | Why it's broken |
| [Affected Tests](#affected-tests) | Which tests fail |
| [Acceptance Criteria](#acceptance-criteria) | Verification checklist |
| [Dependencies](#dependencies) | Relationship to other work |
| [History](#history) | Status changes |

---

## Summary

20 context monitoring tests hardcode expectations for a 200K context window. The runtime now uses 1M (Opus 4.6). This blocks all commits via the pre-commit pytest hook. Confirmed pre-existing on clean branch.

---

## Steps to Reproduce

1. Check out a clean branch at the time of discovery (2026-03-30, pre-fix).
2. Run `uv run pytest tests/integration/test_context_monitoring_integration.py tests/integration/test_context_exhaustion_e2e.py tests/system/test_context_monitoring_system.py tests/e2e/test_context_monitoring_e2e.py`.
3. Observe 20 failures: assertions expect a 200K context window while `ConfigThresholdAdapter.get_context_window_tokens()` returns 1,000,000, producing wrong tier classifications.
4. Attempt any `git commit` — the pre-commit pytest hook fails on the same tests.

---

## Root Cause

`ConfigThresholdAdapter.get_context_window_tokens()` returns 1,000,000 (1M) but tests assert `== 200_000`. Downstream tests set token counts relative to 200K, producing wrong tier classifications (NOMINAL instead of WARNING/EMERGENCY).

---

## Affected Tests

| File | Failures | Pattern |
|------|----------|---------|
| `tests/integration/test_context_monitoring_integration.py` | 10 | Tier boundary expectations at 200K |
| `tests/integration/test_context_exhaustion_e2e.py` | 4 | Checkpoint/resume at 200K boundaries |
| `tests/system/test_context_monitoring_system.py` | 4 | Pipeline tier progression at 200K |
| `tests/e2e/test_context_monitoring_e2e.py` | 1 | XML tag tier output |
| `tests/project_validation/architecture/test_path_conventions.py` | 1 | Cross-project reference |

---

## Acceptance Criteria

- [ ] All 20 currently-failing context monitoring tests pass
- [ ] Tests use actual context window size (1M) or parameterize for multiple sizes
- [ ] No new test failures introduced
- [ ] Pre-commit pytest hook passes without `--no-verify`
- [ ] `ConfigThresholdAdapter` correctly reports the active model's context window

---

## Dependencies

| Type | Item | Description |
|------|------|-------------|
| Blocks | BUG-002 | Both must pass for clean CI; fix order: BUG-001 first (most failures) |
| Blocks | BUG-003 | testpaths expansion depends on hook tests not interfering |
| Related | STORY-022 | P-003 CI check discovered these failures |

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-03-30 | adam.nowak | pending | Created from PROJ-024 session. 20 failures confirmed pre-existing on clean branch. |
