# TASK-057: Build drift-detected golden packet

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

Construct a packet where _anchors.json declared counts disagree with walked truth. Used to verify ANCHOR substrate-coupling rule catches drift.

---

## Acceptance Criteria

- [ ] test_data/golden/drift-detected/ exists
- [ ] expected.json declares which rule_ids should FAIL (specifically ANCHOR substrate-coupling)
- [ ] Manual verification: walked counts != declared counts in this packet
