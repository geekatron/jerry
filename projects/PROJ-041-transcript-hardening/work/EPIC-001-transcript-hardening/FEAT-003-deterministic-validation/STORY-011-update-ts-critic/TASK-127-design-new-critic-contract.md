# TASK-127: Design new contract: critic invokes verify --json first; failures are findings without re-judging

> **Type:** task
> **Status:** pending
> **Priority:** high
> **Created:** 2026-04-29T00:00:00Z
> **Parent:** STORY-011
> **Owner:** ps-architect

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Task scope and rationale |
| [Acceptance Criteria](#acceptance-criteria) | Verifiable completion criteria |

---

## Summary

Architect the integration where deterministic validator output becomes pre-LLM signal.

---

## Acceptance Criteria

- [ ] Contract design persisted in STORY-011 directory
- [ ] Contract specifies: verify --json first, failures = findings, LLM cycles for content quality only
