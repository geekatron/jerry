# TASK-059: Build large-packet golden (1000+ chunks/segments)

> **Type:** task
> **Status:** pending
> **Priority:** high
> **Created:** 2026-04-29T00:00:00Z
> **Parent:** EN-002
> **Owner:** eng-qa

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Task scope and rationale |
| [Acceptance Criteria](#acceptance-criteria) | Verifiable completion criteria |

---

## Summary

Packet exercising forward-compat regex from BUG-002 and BUG-004.

---

## Acceptance Criteria

- [ ] test_data/golden/large-packet/ exists with 1000+ chunks AND 1000+ segments
- [ ] All schema and anchor rules pass against this packet
- [ ] Validates forward-compat regex resolution
