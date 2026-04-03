# BUG-004: Fix Cross-Project Reference in ADR-STORY015-001 (Pre-Existing Test Failure)

> **Type:** bug
> **Status:** completed
> **Priority:** high
> **Impact:** medium
> **Created:** 2026-03-30T00:00:00Z
> **Due:**
> **Completed:** 2026-03-30T09:00:00Z
> **Severity:** minor
> **Parent:** FEAT-001
> **Owner:** adam.nowak
> **Effort:** 1

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What's broken |
| [Steps to Reproduce](#steps-to-reproduce) | How to observe the bug |
| [Acceptance Criteria](#acceptance-criteria) | Verification checklist |
| [Dependencies](#dependencies) | Relationship to other work |
| [History](#history) | Change log |

---

## Steps to Reproduce

1. Run `uv run pytest tests/architecture/test_path_conventions.py -k cross_project`
2. Test `test_no_cross_project_references[PROJ-024-tactical-work]` fails
3. ADR-STORY015-001 contains reference to `projects/PROJ-018`

---

## Summary

ADR-STORY015-001-tier-model-renumbering.md references `projects/PROJ-018` which violates project isolation. Causes 1 test failure in test_path_conventions.py. Fix: remove or replace the cross-project reference.

---

## Acceptance Criteria

- [x] test_no_cross_project_references[PROJ-024-tactical-work] passes
- [x] No cross-project references in PROJ-024 files
- [x] Full test suite passes with zero failures

---

## Dependencies

| Type | Item | Description |
|------|------|-------------|
| Blocks | BUG-005 | Clean test suite baseline needed before hook test fixes |
| Blocks | STORY-025 | Clean test suite needed for CLI integration |

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-03-30 | adam.nowak | pending | Created. Internal finding from test suite -- no GitHub Issue. |
| 2026-03-30 | adam.nowak | completed | Commit `85a168e0`. Cross-project reference removed. Test passes. |
