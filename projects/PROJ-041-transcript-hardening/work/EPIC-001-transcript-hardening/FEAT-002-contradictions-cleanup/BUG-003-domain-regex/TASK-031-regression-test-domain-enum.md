# TASK-031: Regression: 6 registered domain values pass; out-of-list value rejected

> **Type:** task
> **Status:** pending
> **Priority:** high
> **Created:** 2026-04-29T00:00:00Z
> **Parent:** BUG-003
> **Owner:** eng-qa

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Task scope and rationale |
| [Acceptance Criteria](#acceptance-criteria) | Verifiable completion criteria |

---

## Summary

Validate against the canonical schema with each of the 6 registered domains (must pass) and a synthetic out-of-list value (must reject).

---

## Acceptance Criteria

- [ ] 6 registered domain values all validate
- [ ] Out-of-list value rejected with clear error
- [ ] Regression test added to suite
