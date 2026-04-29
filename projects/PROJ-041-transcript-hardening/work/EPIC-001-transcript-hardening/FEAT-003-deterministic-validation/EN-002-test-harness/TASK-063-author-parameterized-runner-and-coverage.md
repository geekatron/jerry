# TASK-063: Author parameterized test runner; configure coverage gate

> **Type:** task
> **Status:** pending
> **Priority:** high
> **Created:** 2026-04-29T00:00:00Z
> **Parent:** EN-002
> **Owner:** eng-qa

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Task scope and rationale |
| [Acceptance Criteria](#acceptance-criteria) | Verifiable completion criteria |

---

## Summary

Pytest harness parametrizes over test_data/golden/*/. Coverage gate ≥90% on validation/ module (≥95% on subprocess sandbox).

---

## Acceptance Criteria

- [ ] tests/transcript/validation/golden/test_packet_validation.py exists
- [ ] Coverage gate configured in pyproject.toml
- [ ] Initial Red phase: all 17 rule tests fail (implementations don't exist yet)
