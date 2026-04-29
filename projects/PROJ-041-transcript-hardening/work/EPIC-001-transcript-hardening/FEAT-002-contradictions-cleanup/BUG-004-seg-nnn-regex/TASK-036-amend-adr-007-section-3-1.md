# TASK-036: Amend ADR-007 §3.1 segment-anchor regex \d{3} → \d{3,}

> **Type:** task
> **Status:** pending
> **Priority:** high
> **Created:** 2026-04-29T00:00:00Z
> **Parent:** BUG-004
> **Owner:** ps-architect

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Task scope and rationale |
| [Acceptance Criteria](#acceptance-criteria) | Verifiable completion criteria |

---

## Summary

Edit ADR-007 §3.1 to loosen the segment-anchor regex, matching schemas. Add History entry with date, author, rationale.

---

## Acceptance Criteria

- [ ] ADR-007 §3.1 regex updated to `^seg-\d{3,}$`
- [ ] ADR-007 History records the amendment with rationale
