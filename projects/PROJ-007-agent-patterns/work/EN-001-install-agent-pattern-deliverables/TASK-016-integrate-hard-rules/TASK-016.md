# TASK-016: Integrate H-32..H-35 into quality-enforcement.md

> **Type:** task
> **Status:** pending
> **Priority:** high
> **Impact:** high
> **Criticality:** C3 (AE-002)
> **Created:** 2026-02-21T23:59:00Z
> **Parent:** EN-001
> **Owner:** --
> **Effort:** 2
> **Activity:** documentation

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Description](#description) | What this task requires |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done |
| [Implementation Notes](#implementation-notes) | Technical approach and constraints |
| [Related Items](#related-items) | Parent and related work |
| [History](#history) | Status changes |

---

## Description

Add H-32 (JSON Schema validation), H-33 (constitutional compliance), H-34 (circuit breaker / max 3 routing hops), and H-35 (keyword-first routing) to the HARD Rule Index in `.context/rules/quality-enforcement.md`. Update the HARD rule budget comment from 31 to 35. Verify no orphan references — every rule in the index must have a corresponding source rule file.

**AE-002 applies:** This task touches `.context/rules/` — auto-C3 minimum criticality. `quality-enforcement.md` is the SSOT for the quality framework and is auto-loaded at session start.

### New Rules to Add

| ID | Rule | Source |
|----|------|--------|
| H-32 | JSON Schema validation REQUIRED for agent definitions | agent-development-standards |
| H-33 | Constitutional compliance check REQUIRED for agent definitions | agent-development-standards |
| H-34 | Circuit breaker: max 3 routing hops before human escalation | agent-routing-standards |
| H-35 | Keyword-first routing: MUST use keyword matching before LLM inference | agent-routing-standards |

### Steps

1. Read current `quality-enforcement.md` HARD Rule Index
2. Append H-32..H-35 rows to the index table
3. Update the Tier Vocabulary table comment: `<= 35` (was `<= 31` or similar)
4. Verify source rule files for H-32/H-33 (agent-development-standards.md) and H-34/H-35 (agent-routing-standards.md) are installed (TASK-012 and TASK-013)
5. Verify no orphan references — every H-rule in the index has a source file

---

## Acceptance Criteria

- [ ] AC-1: H-32 appears in HARD Rule Index with correct rule text and source
- [ ] AC-2: H-33 appears in HARD Rule Index with correct rule text and source
- [ ] AC-3: H-34 appears in HARD Rule Index with correct rule text and source
- [ ] AC-4: H-35 appears in HARD Rule Index with correct rule text and source
- [ ] AC-5: HARD rule budget updated to reflect 35 rules (max count <= 35)
- [ ] AC-6: All rules in the index are traceable to an existing source rule file (no orphans)

---

## Implementation Notes

### Files to Modify

| File | Change |
|------|--------|
| `.context/rules/quality-enforcement.md` | Add H-32..H-35 to HARD Rule Index; update budget |

### Dependencies

TASK-012 (install agent-development-standards) and TASK-013 (install agent-routing-standards) must complete first, or must complete concurrently, so that H-32/H-33 and H-34/H-35 have valid source files in `.context/rules/`.

### Orphan Check

After adding rules, scan the HARD Rule Index and confirm each `Source` column value maps to an existing `.context/rules/` file or an existing CLAUDE.md section reference.

### AE-002 Note

Touching `.context/rules/quality-enforcement.md` is auto-C3. Self-review (S-010) and constitutional compliance check (S-007) required before marking done.

---

## Related Items

- **Parent:** [EN-001](../EN-001.md)
- **AE-002:** Touches `.context/rules/quality-enforcement.md` — auto-C3 minimum
- **Depends on:** TASK-012 (H-32/H-33 source), TASK-013 (H-34/H-35 source)
- **Source rules:** `agent-development-standards.md` (H-32, H-33), `agent-routing-standards.md` (H-34, H-35)

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-21 | pending | Created — awaiting installation of rule files from TASK-012 and TASK-013 |
