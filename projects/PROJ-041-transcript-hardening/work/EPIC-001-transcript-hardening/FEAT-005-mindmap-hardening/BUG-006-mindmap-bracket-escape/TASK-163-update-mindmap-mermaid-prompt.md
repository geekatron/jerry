# TASK-163: Update ts-mindmap-mermaid.md agent prompt: HTML-escape brackets at write time

> **Type:** task
> **Status:** pending
> **Priority:** high
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

When emitting node labels containing `[` or `]`, HTML-escape as `&#91;` and `&#93;`. Defensively also escape `(`, `)`, `{`, `}`.

---

## Acceptance Criteria

- [ ] Agent prompt updated with escape rule
- [ ] Defensive escaping covers all Mermaid-reserved characters
