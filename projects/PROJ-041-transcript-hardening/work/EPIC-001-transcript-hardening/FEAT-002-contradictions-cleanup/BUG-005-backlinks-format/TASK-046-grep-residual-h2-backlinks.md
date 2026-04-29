# TASK-046: Grep across **/*.md for residual ## Backlinks headings; verify zero matches in canonical packet locations

> **Type:** task
> **Status:** pending
> **Priority:** medium
> **Created:** 2026-04-29T00:00:00Z
> **Parent:** BUG-005
> **Owner:** ps-validator

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Task scope and rationale |
| [Acceptance Criteria](#acceptance-criteria) | Verifiable completion criteria |

---

## Summary

Search for old H2 form; confirm cleanup.

---

## Acceptance Criteria

- [ ] `grep -r '^## Backlinks' test_data/ skills/transcript/` returns zero matches
- [ ] Audit report persisted
