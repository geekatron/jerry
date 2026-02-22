# TASK-026: Update Ceiling to 25 with Two-Tier Model and Exception Mechanism

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
> **Source:** DEC-001 D-001/D-002, derivation R2 "Recommendation" and "Exception Mechanism" sections

---

## Summary

Update `quality-enforcement.md` to replace the unprincipled 35-slot ceiling with the derived 25-rule ceiling. Add a two-tier allocation table (Tier A: <=12, Tier B: <=13) and an exception mechanism for temporary ceiling expansion. Update the Tier Vocabulary table and HARD Rule Index to reflect the new model. This is the primary governance deliverable of EN-002.

---

## Scope

1. Update Tier Vocabulary table: replace `<= 35` with the two-tier model (Tier A: <=12, Tier B: <=13, Total: <=25).
2. Add exception mechanism section: temporary ceiling expansion (ceiling + N, N<=3, 3 months max, C4 ADR required).
3. Add permanent revision path: re-derive ceiling when architectural constraints change.
4. Update HARD Rule Index to show tier assignments and post-consolidation rule IDs.
5. Add provenance reference to the C4 derivation document.

---

## Acceptance Criteria

- [ ] Tier Vocabulary table ceiling reads `<= 25` (not `<= 35`)
- [ ] Two-tier allocation table present in `quality-enforcement.md` (Tier A <=12, Tier B <=13)
- [ ] Exception mechanism documented (ceiling + N, N<=3, 3-month max, C4 ADR required)
- [ ] HARD Rule Index rows show tier assignments for each rule
- [ ] Provenance reference to derivation document present
- [ ] All pre-commit hooks pass

---

## Dependencies

**Blocked by:** TASK-025 (Tier A/B classification must be finalized before the allocation table can be written).

**Blocks:** TASK-027 (L5 enforcement gate must enforce the correct ceiling value, which is set here).

---

## History

| Date | Author | Note |
|------|--------|------|
| 2026-02-21 | system | Created from EN-002 implementation plan (DEC-001 D-001/D-002, R2 recommendation) |
