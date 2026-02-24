# TASK-022: Expand L2 Prompt Reinforcement Engine

## Document Sections

| Section | Purpose |
|---------|---------|
| [Metadata](#metadata) | Type, status, priority, parent |
| [Summary](#summary) | What and why |
| [Scope](#scope) | Implementation steps |
| [Acceptance Criteria](#acceptance-criteria) | Done conditions |
| [Dependencies](#dependencies) | Blocks and blocked-by |
| [History](#history) | Change log |

---

## Metadata

> **Type:** task
> **Status:** pending
> **Priority:** high
> **Criticality:** C3 (AE-002 — touches `.context/rules/`)
> **Parent:** EN-002
> **Source:** DISC-002, DEC-001 D-001
> **Created:** 2026-02-21T23:50:00Z

---

## Summary

Expand `prompt_reinforcement_engine.py` to read L2-REINJECT markers from all auto-loaded rule files. Currently the engine hardcodes `quality-enforcement.md` as its only source, covering roughly 10 of 27 HARD rules in L2. Fixing this is the highest-value, lowest-effort item in EN-002 — it nearly triples L2 coverage without any rule changes or budget restructuring.

---

## Scope

1. Modify `_find_rules_path` method (line 243) to glob all `.claude/rules/` symlinked files instead of hardcoding `quality-enforcement.md`.
2. Update L2 budget from 600 to 850 tokens in `ADR-EPIC002-002` and the enforcement architecture table in `quality-enforcement.md`.
3. Audit all 8 non-engine L2-REINJECT markers across rule files for consistency and quality.
4. Add unit tests for multi-file marker extraction.

---

## Acceptance Criteria

- [ ] Engine reads L2-REINJECT markers from all 9 auto-loaded rule files
- [ ] L2 budget updated in documentation (600 → 850 tokens)
- [ ] All existing tests pass
- [ ] New tests cover multi-file marker extraction

---

## Dependencies

**Blocked by:** None — can start immediately.

**Blocks:** TASK-025 (Tier A/B classification benefits from expanded engine coverage before new markers are added).

---

## History

| Date | Author | Note |
|------|--------|------|
| 2026-02-21 | system | Created from EN-002 implementation plan (DEC-001 D-001) |
