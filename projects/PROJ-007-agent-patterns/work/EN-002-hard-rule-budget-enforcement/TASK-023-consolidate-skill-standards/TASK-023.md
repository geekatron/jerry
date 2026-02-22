# TASK-023: Consolidate H-25..H-30 into 2 Compound Rules

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
> **Source:** DEC-001 D-002, derivation R2 Implementation Path step 1
> **Created:** 2026-02-21T23:50:00Z

---

## Summary

Consolidate 6 skill standard HARD rules (H-25 through H-30) into 2 compound rules, saving 4 HARD rule slots toward the 35-rule ceiling.

- **Compound rule A:** H-25 + H-26 + H-27 → "Skill naming and structure" (skill file must be `SKILL.md`, folder must use kebab-case, no `README.md` inside skill folder).
- **Compound rule B:** H-28 + H-29 + H-30 → "Skill description, paths, and registration" (description format `<1024 chars/no XML`, full repo-relative paths, register in `CLAUDE.md` + `AGENTS.md`).

These rules share enforcement layer (L1/L2/L4) and subject domain. No L3 AST gating exists for any of them, so consolidation carries no enforcement risk.

---

## Scope

1. In `skill-standards.md`: merge H-25, H-26, H-27 into a single compound HARD rule.
2. In `skill-standards.md`: merge H-28, H-29, H-30 into a single compound HARD rule.
3. Update `quality-enforcement.md` HARD Rule Index: replace 6 individual rows with 2 compound rows.
4. Search codebase for cross-references to H-25, H-26, H-27, H-28, H-29, H-30 and update all occurrences.
5. Verify no L3 AST enforcement exists for any of these rules before closing.

---

## Acceptance Criteria

- [ ] `skill-standards.md` contains 2 compound HARD rules instead of 6 individual rules
- [ ] `quality-enforcement.md` HARD Rule Index updated (6 rows → 2 rows)
- [ ] All cross-references updated (grep for H-25 through H-30)
- [ ] No L3 AST enforcement broken
- [ ] All pre-commit hooks pass

---

## Dependencies

**Blocked by:** None — can run in parallel with TASK-022 and TASK-024.

**Blocks:** TASK-026 (ceiling two-tier model update depends on final slot count after all consolidations).

---

## History

| Date | Author | Note |
|------|--------|------|
| 2026-02-21 | system | Created from EN-002 implementation plan (DEC-001 D-002, R2 step 1) |
