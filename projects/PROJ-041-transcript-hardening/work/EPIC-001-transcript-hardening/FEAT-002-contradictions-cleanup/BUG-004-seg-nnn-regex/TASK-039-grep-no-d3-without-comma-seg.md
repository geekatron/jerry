# TASK-039: Grep across codebase for any remaining \d{3}$ (non-comma form) on seg-NNN

> **Type:** task
> **Status:** pending
> **Priority:** medium
> **Created:** 2026-04-29T00:00:00Z
> **Parent:** BUG-004
> **Owner:** ps-validator

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Task scope and rationale |
| [Acceptance Criteria](#acceptance-criteria) | Verifiable completion criteria |

---

## Summary

Search for old `\d{3}$` pattern; verify no remaining matches.

---

## Acceptance Criteria

- [ ] `grep -rE 'seg.*\d.\{3\}\$'` returns zero matches
- [ ] Audit report persisted
