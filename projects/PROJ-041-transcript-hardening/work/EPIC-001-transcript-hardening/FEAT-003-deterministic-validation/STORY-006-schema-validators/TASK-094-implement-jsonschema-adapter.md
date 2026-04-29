# TASK-094: Implement JsonSchemaAdapter (infrastructure layer)

> **Type:** task
> **Status:** pending
> **Priority:** high
> **Created:** 2026-04-29T00:00:00Z
> **Parent:** STORY-006
> **Owner:** eng-backend

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Task scope and rationale |
| [Acceptance Criteria](#acceptance-criteria) | Verifiable completion criteria |

---

## Summary

Adapter loads canonical schemas; rules read schemas via this adapter (not by direct file read).

---

## Acceptance Criteria

- [ ] JsonSchemaAdapter exists in infrastructure/json_schema_adapter.py
- [ ] Loads schemas from canonical locations (post-BUG-002/003/004 paths)
