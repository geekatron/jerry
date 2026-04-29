# TASK-166: Add validator (extends FEAT-003 SCHEMA-* or CONTENT-*) detecting unescaped brackets in Mermaid output

> **Type:** task
> **Status:** pending
> **Priority:** medium
> **Created:** 2026-04-29T00:00:00Z
> **Parent:** BUG-006
> **Owner:** eng-backend

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Task scope and rationale |
| [Acceptance Criteria](#acceptance-criteria) | Verifiable completion criteria |

---

## Summary

Defensive guard against future regression.

---

## Acceptance Criteria

- [ ] Validator detects unescaped `[` or `]` in `*.mmd` files
- [ ] Validator integrated with existing rule families
