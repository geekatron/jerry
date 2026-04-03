# BUG-003: scripts/tests/test_hooks.py Fails When Collected Alongside tests/

> **Type:** bug
> **Status:** completed
> **Priority:** high
> **Severity:** major
> **Impact:** medium
> **Created:** 2026-03-30T00:00:00Z
> **Due:**
> **Completed:**
> **Parent:** FEAT-001
> **Owner:**
> **Effort:** 2
> **GitHub Issue:** [#228](https://github.com/geekatron/jerry/issues/228)

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What's broken |
| [Root Cause](#root-cause) | Why it fails |
| [Acceptance Criteria](#acceptance-criteria) | Verification checklist |
| [Steps to Reproduce](#steps-to-reproduce) | How to trigger |
| [Dependencies](#dependencies) | Relationship to other work |
| [History](#history) | Status changes |

---

## Summary

`scripts/tests/test_hooks.py` (15 failures) cannot be collected alongside `tests/` via pytest testpaths. Different environment assumptions cause failures. Prevents expanding testpaths to include script-level tests.

---

## Root Cause

`scripts/tests/test_hooks.py` was designed for isolated execution. Tests assume a different import path structure and environment setup than the main `tests/` suite. When both are collected together, hook test fixtures conflict with the main test infrastructure.

---

## Steps to Reproduce

1. Add `scripts/tests` to `testpaths` in `pyproject.toml`
2. Run `uv run pytest` — observe 15 failures from `scripts/tests/test_hooks.py` due to fixture conflicts

---

## Acceptance Criteria

- [ ] `scripts/tests` can be added to pytest testpaths without breaking existing tests
- [ ] `test_hooks.py` passes when collected alongside `tests/`
- [ ] `test_validate_agent_frontmatter.py` (STORY-022) runs in CI via pytest collection (not just script invocation)
- [ ] Proper `conftest.py` or markers isolate script test environment

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
