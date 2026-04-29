# TASK-020: Grep across skills/transcript/ for token-cap references; verify no remaining unlabeled divergence

> **Type:** task
> **Status:** pending
> **Priority:** medium
> **Created:** 2026-04-29T00:00:00Z
> **Parent:** BUG-001
> **Owner:** ps-validator

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Task scope and rationale |
| [Acceptance Criteria](#acceptance-criteria) | Verifiable completion criteria |

---

## Summary

Search for 2K/5K and 5K/8K patterns; ensure every reference is either consistent OR explicitly labeled.

---

## Acceptance Criteria

- [ ] `grep -rE '(2,?000|5,?000|2K|5K|8K)' skills/transcript/` shows only consistent or labeled references
- [ ] Validation report persisted in BUG-001 directory
