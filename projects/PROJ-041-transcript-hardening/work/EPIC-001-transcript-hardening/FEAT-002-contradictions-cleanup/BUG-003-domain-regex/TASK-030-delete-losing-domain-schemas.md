# TASK-030: Delete or deprecate contexts/schemas/domain-schema.json and schemas/context-domain-schema.json

> **Type:** task
> **Status:** pending
> **Priority:** high
> **Created:** 2026-04-29T00:00:00Z
> **Parent:** BUG-003
> **Owner:** eng-lead

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Task scope and rationale |
| [Acceptance Criteria](#acceptance-criteria) | Verifiable completion criteria |

---

## Summary

Either delete the two regex-based domain schemas OR mark them deprecated with a pointer to the canonical schema.

---

## Acceptance Criteria

- [ ] Two losing schemas deleted (preferred) OR marked deprecated with pointer
- [ ] All references across codebase updated to point to DOMAIN-SCHEMA.json
