# TASK-012: Fix diataxis SKILL.md plural/singular naming inconsistencies

> **Type:** task
> **Status:** pending
> **Priority:** low
> **Created:** 2026-03-31
> **Parent:** BUG-006

---

## Summary

Resolve plural/singular naming inconsistencies between `skills/diataxis/SKILL.md` and the governance YAML files.

## Inconsistencies

| Agent | SKILL.md Says | Governance Says | Fix To |
|-------|---------------|-----------------|--------|
| diataxis-howto | `docs/howto/` | `docs/how-to/` | `docs/how-to/` (governance is canonical) |
| diataxis-explanation | `docs/explanations/` | `docs/explanation/` | `docs/explanation/` (governance is canonical) |

**Locations:** SKILL.md lines 120-123 and 224-227 (agent table and quick reference).

## Acceptance Criteria

- [ ] SKILL.md output paths match governance YAML `output.location` fields exactly
- [ ] No plural/singular mismatches between SKILL.md and governance files
