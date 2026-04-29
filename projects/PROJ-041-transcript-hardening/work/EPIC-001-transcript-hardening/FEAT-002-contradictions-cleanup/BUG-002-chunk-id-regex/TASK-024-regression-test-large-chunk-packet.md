# TASK-024: Regression test: synthetic 1000+ chunk packet validates against all 3 schemas

> **Type:** task
> **Status:** pending
> **Priority:** high
> **Created:** 2026-04-29T00:00:00Z
> **Parent:** BUG-002
> **Owner:** eng-qa

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Task scope and rationale |
| [Acceptance Criteria](#acceptance-criteria) | Verifiable completion criteria |

---

## Summary

Construct a synthetic packet with chunk-001 through chunk-1500 identifiers and validate against all three schemas.

---

## Acceptance Criteria

- [ ] Synthetic 1500-chunk packet exists in test_data/
- [ ] All three schemas pass validation against the synthetic packet
- [ ] Regression test added to test suite
