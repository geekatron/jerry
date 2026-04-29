# TASK-075: Implement FILE-001..003 as ValidationRule entities (Green)

> **Type:** task
> **Status:** pending
> **Priority:** high
> **Created:** 2026-04-29T00:00:00Z
> **Parent:** STORY-003
> **Owner:** eng-backend

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Task scope and rationale |
| [Acceptance Criteria](#acceptance-criteria) | Verifiable completion criteria |

---

## Summary

Per ADR-007 §4 FILE rule definitions, implement under src/jerry/transcript/validation/domain/rules/file/.

---

## Acceptance Criteria

- [ ] FILE-001..003 ValidationRule classes exist and pass tests
- [ ] Each rule returns (rule_id, severity, pass|fail, evidence) tuple
- [ ] All 3 rules pass against clean-packet golden
