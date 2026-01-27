# BUG-001: EN-009 ID Conflict - Duplicate Enabler IDs

<!--
TEMPLATE: Bug
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.8
-->

> **Type:** bug
> **Status:** RESOLVED
> **Priority:** critical
> **Severity:** high
> **Created:** 2026-01-26T21:00:00Z
> **Resolved:** 2026-01-26T22:00:00Z
> **Found In:** FEAT-002-implementation
> **Parent:** FEAT-002
> **Owner:** Claude
> **Resolution:** FIXED - EN-009-ts-formatter renumbered to EN-016

---

## Summary

Two enablers share the same ID `EN-009`, causing confusion and potential traceability issues:

| Enabler | Location | Tasks | Purpose |
|---------|----------|-------|---------|
| EN-009-mindmap-generator | `EN-009-mindmap-generator/` | TASK-046..049 | Mind Map Generator (Mermaid + ASCII) |
| EN-009-ts-formatter | `EN-009-ts-formatter/` | TASK-113..119 | ts-formatter Agent Implementation |

**Evidence:** Task number sequences indicate EN-009-mindmap-generator (TASK-046+) was created BEFORE EN-009-ts-formatter (TASK-113+).

---

## Impact Analysis

### L0: Executive Summary (ELI5)
Two work items have the same ID number, like having two students with the same ID in a class. When we reference "EN-009", we don't know which one we're talking about.

### L1: Engineer Impact
- **Traceability broken:** Cannot uniquely identify enablers in dependency graphs
- **Task confusion:** TASK-046-049 vs TASK-113-119 both claim EN-009 parent
- **Documentation inconsistency:** FEAT-002 references only ts-formatter as EN-009

### L2: Architectural Impact
- **Ontology violation:** Enabler IDs must be unique per ONTOLOGY-v1.md Section 3.4.5
- **Orchestration ambiguity:** ORCHESTRATION.yaml cannot correctly track two EN-009s
- **Audit trail compromised:** Historical records ambiguous about which EN-009

---

## Root Cause Analysis

### Timeline Reconstruction

1. **Initial creation:** EN-009-mindmap-generator created with TASK-046..049
2. **DISC-001 restructuring (2026-01-26):** FEAT-002 was restructured per DISC-001
3. **During restructuring:** EN-009-ts-formatter created with TASK-113..119
4. **Oversight:** Original EN-009-mindmap-generator was not renumbered or deprecated

### Why This Happened

- During DISC-001 analysis, the TDD-ts-formatter.md design was mapped to EN-009
- The existing EN-009-mindmap-generator was not checked before ID assignment
- No validation mechanism exists to prevent duplicate enabler IDs

---

## Resolution Plan

### Recommended Resolution: Renumber ts-formatter to EN-016

**Rationale:**
1. EN-009-mindmap-generator has priority by creation timestamp (lower task numbers)
2. User confirmed EN-009 is "hard requirement for mermaid and ascii art mind maps"
3. EN-016 is the next available enabler ID (after EN-015)
4. Minimal impact - ts-formatter was recently created during DISC-001

### Changes Required

| Item | Current | Change To |
|------|---------|-----------|
| Folder | `EN-009-ts-formatter/` | `EN-016-ts-formatter/` |
| File | `EN-009-ts-formatter.md` | `EN-016-ts-formatter.md` |
| ID in YAML frontmatter | `EN-009` | `EN-016` |
| Task parent references | `EN-009` | `EN-016` |
| FEAT-002 enabler table | Row shows EN-009 | Row shows EN-016 |
| EN-011 dependency | EN-010 | EN-016 |
| EN-012 dependency | EN-010 | EN-016 |

### Gate Reassignment

| Enabler | Current Gate | New Gate | Notes |
|---------|--------------|----------|-------|
| EN-009 (mindmap) | GATE-6 | GATE-5 | Core visualization, pre-validation |
| EN-016 (ts-formatter) | GATE-5 | GATE-5 | Unchanged |

---

## Acceptance Criteria

- [x] EN-009-ts-formatter folder renamed to EN-016-ts-formatter
- [x] EN-016-ts-formatter.md file renamed and ID updated
- [x] All TASK-113..119 files updated with EN-016 parent
- [x] FEAT-002-implementation.md updated with EN-016
- [x] EN-009-mindmap-generator added to FEAT-002 enabler inventory
- [x] EN-011 dependencies updated (EN-010 -> EN-016)
- [x] EN-012 dependencies updated (EN-010 -> EN-016)
- [x] ORCHESTRATION.yaml updated (N/A - no ORCHESTRATION.yaml exists at FEAT-002 level)
- [x] No duplicate EN-009 references remain (verified via grep)

---

## Related Items

- **DISC-001:** [FEAT-002--DISC-001-enabler-alignment-analysis.md](./FEAT-002--DISC-001-enabler-alignment-analysis.md) - Restructuring that introduced conflict
- **EN-009-mindmap-generator:** [EN-009-mindmap-generator.md](./EN-009-mindmap-generator/EN-009-mindmap-generator.md) - Original EN-009 (retained)
- **EN-016-ts-formatter:** [EN-016-ts-formatter.md](./EN-016-ts-formatter/EN-016-ts-formatter.md) - Renumbered from EN-009
- **EN-010:** [EN-010-artifact-packaging.md](./EN-010-artifact-packaging/EN-010-artifact-packaging.md) - DEPRECATED, absorbed into EN-016
- **EN-011:** [EN-011-worktracker-integration.md](./EN-011-worktracker-integration/EN-011-worktracker-integration.md) - Dependencies fixed (EN-010 → EN-016)
- **EN-012:** [EN-012-skill-interface.md](./EN-012-skill-interface/EN-012-skill-interface.md) - Dependencies fixed (EN-010 → EN-016)

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-01-26 | Claude | OPEN | Bug identified during task file creation |
| 2026-01-26 | Claude | IN_PROGRESS | Resolution plan created |
| 2026-01-26 | Claude | RESOLVED | EN-009-ts-formatter renumbered to EN-016, all dependencies fixed, verified via grep |

---

## System Mapping

| System | Mapping |
|--------|---------|
| **Azure DevOps** | Bug |
| **SAFe** | Defect |
| **JIRA** | Bug |
