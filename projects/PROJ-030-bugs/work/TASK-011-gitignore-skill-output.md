# TASK-011: Update .gitignore to prevent skills/*/output/ accumulation

> **Type:** task
> **Status:** pending
> **Priority:** medium
> **Created:** 2026-03-31
> **Parent:** BUG-006

---

## Summary

Add `skills/*/output/` pattern to `.gitignore` to prevent future accidental commits of skill-internal output directories.

## Acceptance Criteria

- [ ] `.gitignore` contains `skills/*/output/` pattern
- [ ] Pattern is documented with a comment explaining why
- [ ] `git check-ignore skills/eng-team/output/test.md` confirms the pattern works
