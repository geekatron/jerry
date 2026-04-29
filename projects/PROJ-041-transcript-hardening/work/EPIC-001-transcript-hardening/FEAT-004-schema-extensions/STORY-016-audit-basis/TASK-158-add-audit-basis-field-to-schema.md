# TASK-158: Add provenance.audit_basis field to extraction-report.json schema (option (a) lighter touch)

> **Type:** task
> **Status:** pending
> **Priority:** low
> **Created:** 2026-04-29T00:00:00Z
> **Parent:** STORY-016
> **Owner:** eng-backend

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Task scope and rationale |
| [Acceptance Criteria](#acceptance-criteria) | Verifiable completion criteria |

---

## Summary

Single string + optional methodology_evolution array per audit comment 2.

---

## Acceptance Criteria

- [ ] Schema v1.2 includes provenance.audit_basis (optional)
- [ ] Existing packets without the field continue to validate
