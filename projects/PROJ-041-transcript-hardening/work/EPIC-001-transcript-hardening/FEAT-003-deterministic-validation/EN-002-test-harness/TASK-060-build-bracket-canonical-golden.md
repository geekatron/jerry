# TASK-060: Build bracket-canonical golden (mindmap labels with [...])

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

Packet exercising FEAT-005 BUG-006 fix. Per ps-architect D-6.3, may need synthesis from PDD-0102 patterns if audit packet unshareable.

---

## Acceptance Criteria

- [ ] test_data/golden/bracket-canonical/ exists with bracketed canonical-form labels
- [ ] Reproduces the parse-error condition before BUG-006 fix
- [ ] After BUG-006 fix lands, packet renders cleanly via mmdc
