# TASK-112: Test suite: dry-run, scoped buckets, atomicity under concurrent simulation

> **Type:** task
> **Status:** pending
> **Priority:** high
> **Created:** 2026-04-29T00:00:00Z
> **Parent:** STORY-008
> **Owner:** eng-qa

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Task scope and rationale |
| [Acceptance Criteria](#acceptance-criteria) | Verifiable completion criteria |

---

## Summary

Comprehensive tests of all CLI flags and atomicity guarantees.

---

## Acceptance Criteria

- [ ] Tests cover --dry-run (no writes), --bucket (scoped), atomicity (concurrent)
- [ ] Coverage ≥90% on UpdateAnchorsService
