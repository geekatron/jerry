# TASK-171: Regression: agent on BUG-006 audit packet — correctly identifies failure (Option A) or doesn't make false claim (Option B)

> **Type:** task
> **Status:** pending
> **Priority:** high
> **Created:** 2026-04-29T00:00:00Z
> **Parent:** BUG-007
> **Owner:** eng-qa

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Task scope and rationale |
| [Acceptance Criteria](#acceptance-criteria) | Verifiable completion criteria |

---

## Summary

Behavior test against the original failure surface.

---

## Acceptance Criteria

- [ ] If Option A: agent correctly reports render failure on bracket-canonical golden
- [ ] If Option B: agent does not make false syntax-validity claim
- [ ] Test integrated into ts-mindmap-mermaid golden tests
