# TASK-141: Add golden packet with populated editorial_conventions block; FEAT-003 SCHEMA-* validators pick up new field

> **Type:** task
> **Status:** pending
> **Priority:** medium
> **Created:** 2026-04-29T00:00:00Z
> **Parent:** STORY-013
> **Owner:** eng-qa

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Task scope and rationale |
| [Acceptance Criteria](#acceptance-criteria) | Verifiable completion criteria |

---

## Summary

Demonstrates the field works through validators automatically (since FEAT-003 STORY-006 reads schemas, not hardcodes).

---

## Acceptance Criteria

- [ ] test_data/golden/with-editorial-conventions/ exists
- [ ] FEAT-003 SCHEMA-* validators pass against this packet
