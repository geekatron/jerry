# BUG-003: scripts/tests/test_hooks.py Fails When Collected Alongside tests/

> **Type:** bug
> **Status:** completed
> **Priority:** high
> **Severity:** minor
> **Impact:** medium
> **Created:** 2026-03-30T00:00:00Z
> **Completed:** 2026-03-30T00:00:00Z
> **Parent:** FEAT-001
> **Owner:**
> **Effort:** 2
> **GitHub Issue:** [#228](https://github.com/geekatron/jerry/issues/228)

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What's broken |
| [Steps to Reproduce](#steps-to-reproduce) | How to observe the failure |
| [Root Cause](#root-cause) | Why it fails |
| [Acceptance Criteria](#acceptance-criteria) | Verification checklist |
| [Dependencies](#dependencies) | Relationship to other work |
| [History](#history) | Status changes |

---

## Summary

`scripts/tests/test_hooks.py` (15 failures) cannot be collected alongside `tests/` via pytest testpaths. Different environment assumptions cause failures. Prevents expanding testpaths to include script-level tests.

---

## Steps to Reproduce

1. At the 2026-03-30 pre-fix state, add `scripts/tests` to the `testpaths` list in `pyproject.toml`.
2. Run `uv run pytest` (collecting `tests/` and `scripts/tests` together).
3. Observe 15 failures in `scripts/tests/test_hooks.py` — fixtures conflict with the main test infrastructure due to different import-path and environment assumptions.
4. Run `uv run pytest scripts/tests/test_hooks.py` in isolation — all tests pass, confirming the collection conflict.

---

## Root Cause

`scripts/tests/test_hooks.py` was designed for isolated execution. Tests assume a different import path structure and environment setup than the main `tests/` suite. When both are collected together, hook test fixtures conflict with the main test infrastructure.

---

## Acceptance Criteria

- [x] `scripts/tests` can be added to pytest testpaths without breaking existing tests
- [x] `test_hooks.py` passes when collected alongside `tests/`
- [x] `test_validate_agent_frontmatter.py` (STORY-022) runs in CI via pytest collection (not just script invocation)
- [x] Proper `conftest.py` or markers isolate script test environment

> AC boxes backfilled 2026-08-05 (audit W-004c): work verified complete at closure 2026-03-30 — GitHub issue [#228](https://github.com/geekatron/jerry/issues/228) closed; the full suite including script tests passes in CI and pre-commit today.

---

## Dependencies

| Type | Item | Description |
|------|------|-------------|
| Blocked By | BUG-001 | Context monitoring fixes must land first (they cause more failures) |
| Blocked By | BUG-002 | CVE fix must land first (blocks push) |
| Related | STORY-022 | P-003 tests currently run via CI workflow step due to this limitation |

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-03-30 | adam.nowak | pending | Created from PROJ-024 session. Discovered when STORY-022 tried adding scripts/tests to testpaths. |
| 2026-03-30 | adam.nowak | completed | Fixed and closed — GH #228 closed; script tests isolated and collected cleanly alongside tests/. (History row backfilled 2026-08-05 per audit W-004c.) |
