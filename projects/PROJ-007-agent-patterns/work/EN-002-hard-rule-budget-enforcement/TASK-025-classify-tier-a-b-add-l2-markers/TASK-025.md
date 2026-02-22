# TASK-025: Classify Rules into Tier A/B and Add Missing L2 Markers

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
> **Source:** DEC-001 D-002, derivation R2 "Draft Tier A/B Classification" section

---

## Summary

Classify all post-consolidation HARD rules into Tier A (constitutional, engine-processed L2) and Tier B (operational, structural L2 + L3/L5). Add L2-REINJECT markers for H-04 and H-22, which are currently missing from engine-processed L2 coverage despite being high-priority behavioral rules. Based on the draft classification in the derivation R2 document.

---

## Scope

1. Add L2-REINJECT marker for H-04 (active project required) in `quality-enforcement.md` (~50 tokens).
2. Add L2-REINJECT marker for H-22 (proactive skill invocation) in `quality-enforcement.md` (~50 tokens).
3. Document Tier A/B classification in `quality-enforcement.md` alongside the HARD Rule Index.
4. Verify L2 budget: current 415 + 100 new = 515 tokens (within 850 budget post-engine-expansion).

---

## Acceptance Criteria

- [ ] H-04 has engine-processed L2-REINJECT marker in `quality-enforcement.md`
- [ ] H-22 has engine-processed L2-REINJECT marker in `quality-enforcement.md`
- [ ] Tier A/B classification documented in `quality-enforcement.md` alongside the HARD Rule Index
- [ ] L2 token budget verified within limits (target <= 850 tokens post-expansion)

---

## Dependencies

**Blocked by:** TASK-022 (engine expansion — engine must read all rule files before adding new markers); TASK-023 and TASK-024 (consolidation determines the final rule set that gets classified).

**Blocks:** TASK-026 (two-tier ceiling model depends on Tier A/B assignments being finalized).

---

## History

| Date | Author | Note |
|------|--------|------|
| 2026-02-21 | system | Created from EN-002 implementation plan (DEC-001 D-002, R2 draft classification) |
