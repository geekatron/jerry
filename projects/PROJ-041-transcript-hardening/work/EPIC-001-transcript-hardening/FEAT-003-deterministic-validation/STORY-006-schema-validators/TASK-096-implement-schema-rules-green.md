# TASK-096: Implement SCHEMA-001..008 (Green); rules read schemas, don't hardcode shapes

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

Per ADR-007 §4 SCHEMA rule definitions. Rules consume schemas via JsonSchemaAdapter so FEAT-004 schema additions extend coverage automatically.

---

## Acceptance Criteria

- [ ] SCHEMA-001..008 ValidationRule classes pass tests
- [ ] Rules use post-FEAT-002 schemas (converged chunk_id, canonical DOMAIN-SCHEMA, loosened seg-NNN)
- [ ] Adding a schema field automatically extends rule coverage
