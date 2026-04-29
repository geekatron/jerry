# TASK-023: Update chunk.schema.json and index.schema.json regex to ^chunk-\d{3,}$

> **Type:** task
> **Status:** pending
> **Priority:** high
> **Created:** 2026-04-29T00:00:00Z
> **Parent:** BUG-002
> **Owner:** eng-lead

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Task scope and rationale |
| [Acceptance Criteria](#acceptance-criteria) | Verifiable completion criteria |

---

## Summary

Edit both schema files to use the forward-compat 3-or-more digit regex matching extraction-report.json schema.

---

## Acceptance Criteria

- [ ] chunk.schema.json regex updated to `^chunk-\d{3,}$`
- [ ] index.schema.json regex updated to `^chunk-\d{3,}$`
- [ ] extraction-report.json schema unchanged (already correct)
