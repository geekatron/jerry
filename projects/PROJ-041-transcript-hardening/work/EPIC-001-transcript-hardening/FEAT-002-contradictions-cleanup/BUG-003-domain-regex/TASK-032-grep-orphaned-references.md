# TASK-032: Grep for orphaned references to losing schemas; verify zero matches

> **Type:** task
> **Status:** pending
> **Priority:** medium
> **Created:** 2026-04-29T00:00:00Z
> **Parent:** BUG-003
> **Owner:** ps-validator

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Task scope and rationale |
| [Acceptance Criteria](#acceptance-criteria) | Verifiable completion criteria |

---

## Summary

Search across the codebase for any references to the deleted/deprecated schemas.

---

## Acceptance Criteria

- [ ] `grep -r 'context-domain-schema\|domain-schema'` shows only canonical references
- [ ] Audit report persisted
