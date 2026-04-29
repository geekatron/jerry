# TASK-025: Grep verifies no remaining \d{3}$ (without comma) for chunk_id

> **Type:** task
> **Status:** pending
> **Priority:** medium
> **Created:** 2026-04-29T00:00:00Z
> **Parent:** BUG-002
> **Owner:** ps-validator

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Task scope and rationale |
| [Acceptance Criteria](#acceptance-criteria) | Verifiable completion criteria |

---

## Summary

Search across all schema files for chunk_id regex patterns and confirm convergence.

---

## Acceptance Criteria

- [ ] `grep -r 'chunk-' --include='*.schema.json'` shows all uses match `\d{3,}` form
- [ ] Audit report persisted in BUG-002 directory
