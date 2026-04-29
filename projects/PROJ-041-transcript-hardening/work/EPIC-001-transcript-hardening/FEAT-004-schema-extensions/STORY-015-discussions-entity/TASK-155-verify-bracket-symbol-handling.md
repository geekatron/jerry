# TASK-155: Coordinate with FEAT-005 BUG-006: confirm `[~]` ascii symbol never escapes into Mermaid output unescaped

> **Type:** task
> **Status:** pending
> **Priority:** medium
> **Created:** 2026-04-29T00:00:00Z
> **Parent:** STORY-015
> **Owner:** eng-qa

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Task scope and rationale |
| [Acceptance Criteria](#acceptance-criteria) | Verifiable completion criteria |

---

## Summary

Per ps-architect D-6.2 ascii AC: ascii rendering of `[~]` validates without bracket escape; Mermaid path applies escape.

---

## Acceptance Criteria

- [ ] ascii output uses `[~]` literal (no escape)
- [ ] Mermaid output uses `~` (no brackets)
- [ ] Test confirms cross-renderer correctness
