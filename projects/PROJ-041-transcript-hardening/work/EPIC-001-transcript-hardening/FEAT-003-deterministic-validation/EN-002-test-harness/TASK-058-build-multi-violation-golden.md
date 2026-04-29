# TASK-058: Build multi-violation golden packet

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

Packet where multiple rules fail simultaneously. Used to verify validator report aggregation.

---

## Acceptance Criteria

- [ ] test_data/golden/multi-violation/ exists
- [ ] expected.json declares ≥3 rule_ids as FAIL
- [ ] Manual verification confirms violations are independent
