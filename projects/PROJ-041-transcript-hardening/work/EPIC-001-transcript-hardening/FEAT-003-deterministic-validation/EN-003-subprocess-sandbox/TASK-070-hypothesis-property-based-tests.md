# TASK-070: Author Hypothesis property-based tests on the pattern parser

> **Type:** task
> **Status:** pending
> **Priority:** high
> **Created:** 2026-04-29T00:00:00Z
> **Parent:** EN-003
> **Owner:** eng-qa

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Task scope and rationale |
| [Acceptance Criteria](#acceptance-criteria) | Verifiable completion criteria |

---

## Summary

Property-based testing: explore 10K+ generated inputs to find parser bypasses.

---

## Acceptance Criteria

- [ ] tests/transcript/validation/unit/test_subprocess_sandbox_property.py exists
- [ ] Hypothesis explores ≥10K generated inputs
- [ ] No parser bypass found across the run
