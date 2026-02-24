# TASK-024: Consolidate H-07..H-09 into 1 Compound Rule

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
> **Source:** DEC-001 D-002, derivation R2 Implementation Path step 2
> **Created:** 2026-02-21T23:50:00Z

---

## Summary

Consolidate 3 architecture layer HARD rules (H-07, H-08, H-09) into 1 compound rule covering "Architecture layer isolation", saving 2 HARD rule slots toward the 35-rule ceiling.

- H-07: Domain layer — no external imports
- H-08: Application layer — no infra/interface imports
- H-09: Composition root exclusivity

All three rules are co-located in `architecture-standards.md`, share the same enforcement layers (L1/L2/L4), and form a single coherent constraint: hexagonal layer isolation. No L3 AST gating currently exists for any of them. If L3 import enforcement is added in the future, these should be un-consolidated back to individual rules to allow per-rule gating.

---

## Scope

1. In `architecture-standards.md`: merge H-07, H-08, H-09 into a single compound HARD rule.
2. Update `quality-enforcement.md` HARD Rule Index: replace 3 individual rows with 1 compound row.
3. Search codebase for cross-references to H-07, H-08, H-09 and update all occurrences.
4. Verify no L3 AST enforcement exists for any of these rules before closing.
5. Add inline note to the compound rule: if L3 AST import gating is added later, un-consolidate to individual rules.

---

## Acceptance Criteria

- [ ] `architecture-standards.md` contains 1 compound HARD rule instead of 3
- [ ] `quality-enforcement.md` HARD Rule Index updated (3 rows → 1 row)
- [ ] All cross-references updated (grep for H-07, H-08, H-09)
- [ ] No L3 AST enforcement broken
- [ ] All pre-commit hooks pass

---

## Dependencies

**Blocked by:** None — can run in parallel with TASK-022 and TASK-023.

**Blocks:** TASK-026 (ceiling two-tier model update depends on final slot count after all consolidations).

---

## History

| Date | Author | Note |
|------|--------|------|
| 2026-02-21 | system | Created from EN-002 implementation plan (DEC-001 D-002, R2 step 2) |
