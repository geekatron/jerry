# TASK-152: Implement discussions[] across extraction-report.json schema, anchor regex, output template, mindmap symbols

> **Type:** task
> **Status:** pending
> **Priority:** high
> **Created:** 2026-04-29T00:00:00Z
> **Parent:** STORY-015
> **Owner:** eng-backend

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Task scope and rationale |
| [Acceptance Criteria](#acceptance-criteria) | Verifiable completion criteria |

---

## Summary

Schema: optional 5th top-level array. Anchor regex `disc-\d{3,}` per BUG-004. Mindmap: `~` (mermaid), `[~]` (ascii). Output: H2 in topics file.

---

## Acceptance Criteria

- [ ] Schema v1.2 includes discussions[] (optional)
- [ ] Anchor regex registered as `^disc-\d{3,}$`
- [ ] Mindmap symbols registered for both renderers
- [ ] Output template adds `## Discussion Items` H2
