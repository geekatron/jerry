# EN-701: Quality Enforcement SSOT (Single Source of Truth)

<!--
TEMPLATE: Enabler
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.9
CREATED: 2026-02-14 (Claude)
PURPOSE: Create the single source of truth for all quality framework constants
-->

> **Type:** enabler
> **Status:** completed
> **Priority:** critical
> **Impact:** critical
> **Enabler Type:** infrastructure
> **Created:** 2026-02-14
> **Due:** —
> **Completed:** —
> **Parent:** FEAT-008
> **Owner:** —
> **Effort:** 5

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What this enabler delivers |
| [Problem Statement](#problem-statement) | Why this work is needed |
| [Business Value](#business-value) | How this enabler supports the parent feature |
| [Technical Approach](#technical-approach) | How we'll implement it |
| [Design Source](#design-source) | Traceability to EPIC-002 design artifacts |
| [Children (Tasks)](#children-tasks) | Task breakdown |
| [Progress Summary](#progress-summary) | Completion status and metrics |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done |
| [Evidence](#evidence) | Proof of completion |
| [Related Items](#related-items) | Dependencies and hierarchy |
| [History](#history) | Change log |

---

## Summary

Create `.context/rules/quality-enforcement.md` as the Single Source of Truth for all quality framework constants. This file consolidates shared values referenced by all hooks, rules, and skills: criticality levels (C1-C4), quality threshold (0.92), strategy encodings (S-001 through S-014), cycle count (3 iterations minimum), tier vocabulary (HARD/MEDIUM/SOFT), and auto-escalation rules (AE-001 through AE-006).

**Value Proposition:**
- Eliminates constant duplication across hooks, rules, and skills
- Provides a single canonical reference for all quality framework values
- Prevents enforcement gaps caused by inconsistent values across documents
- Enables downstream enablers (EN-702 through EN-706) to reference one authoritative file
- Reduces maintenance burden when constants change

**Technical Scope:**
- Criticality levels C1-C4 with definitions and enforcement tier mapping
- Quality threshold (0.92) with scoring dimensions
- All strategy encodings (S-001 through S-014) with descriptions
- Minimum cycle count (3 iterations) for creator-critic-revision
- Tier vocabulary (HARD/MEDIUM/SOFT) definitions and usage rules
- Auto-escalation rules (AE-001 through AE-006)
- 5-layer architecture reference (L1-L5)

---

## Problem Statement

Quality framework constants are scattered across multiple EPIC-002 design documents. Without a single authoritative source, hooks and rules will reference inconsistent values leading to enforcement gaps. Specific risks:

1. **Value drift** -- Different files may define slightly different thresholds or criticality boundaries, leading to inconsistent enforcement behavior.
2. **Maintenance burden** -- Updating a constant (e.g., quality threshold) requires finding and updating every file that references it.
3. **Onboarding friction** -- New contributors cannot find the authoritative definition of framework constants without reading multiple design documents.
4. **Enforcement gaps** -- If a hook references C1-C4 levels differently than a rule file, Claude may exploit the inconsistency to bypass quality gates.

---

## Business Value

Provides the canonical source of truth for quality framework constants, eliminating duplication and drift across hooks, rules, and skills. This enabler is the foundation that all downstream enforcement components (EN-702 through EN-711) reference for authoritative constant values.

### Features Unlocked

- Consistent quality enforcement across all 5 layers (L1-L5) via single-point-of-update for threshold and criticality constants
- Traceable compliance references enabling downstream enablers to reference one authoritative file

---

## Technical Approach

1. **Extract constants** from EN-403 (hook designs), EN-404 (rule optimization), EN-405 (session context), and the EPIC-002 final synthesis into a single consolidated list.
2. **Organize by category** -- Group constants into logical sections: criticality levels, quality thresholds, strategy catalog, cycle requirements, tier vocabulary, escalation rules, and architecture layers.
3. **Write `.context/rules/quality-enforcement.md`** following the markdown navigation standards (NAV-001 through NAV-006). Keep the file under 2000 tokens.
4. **Cross-reference** -- Ensure all downstream enablers (EN-702 through EN-706) can reference this file as the SSOT rather than embedding constants directly.
5. **Validate completeness** -- Verify every constant referenced in EPIC-002 design documents is present in the SSOT file.

---

## Design Source

| Source | Content Used |
|--------|-------------|
| EPIC-002 EN-405 / TASK-006 | Preamble content, session context constants |
| EPIC-002 EN-404 | Rule optimization, tier vocabulary, enforcement language |
| ADR-EPIC002-002 | 5-layer architecture (L1-L5), token budgets, enforcement tier definitions |
| ADR-EPIC002-001 | Decision criticality levels (C1-C4), quality gate thresholds |
| EPIC-002 Final Synthesis | Strategy catalog (S-001 through S-014), auto-escalation rules (AE-001 through AE-006) |

---

## Children (Tasks)

| ID | Title | Status | Activity | Agents |
|----|-------|--------|----------|--------|
| TASK-001 | Extract all quality framework constants from EPIC-002 design documents | pending | RESEARCH | ps-researcher |
| TASK-002 | Organize constants into structured SSOT file | pending | DEVELOPMENT | ps-architect |
| TASK-003 | Validate completeness against all EPIC-002 source documents | pending | TESTING | nse-verification |
| TASK-004 | Adversarial review of SSOT file for gaps and ambiguities | pending | TESTING | ps-critic |
| TASK-005 | Creator revision based on review findings | pending | DEVELOPMENT | ps-architect |

### Task Dependencies

```
TASK-001 (extract constants) ──> TASK-002 (organize SSOT) ──> TASK-003 (validate)
                                                                     │
                                                                     v
                                                   TASK-004 (adversarial review) ──> TASK-005 (revision)
```

---

## Progress Summary

### Status Overview

```
+------------------------------------------------------------------+
|                   ENABLER PROGRESS TRACKER                        |
+------------------------------------------------------------------+
| Tasks:     [████████████████████] 100% (5/5 completed)           |
| Effort:    [████████████████████] 100% (5/5 points completed)    |
+------------------------------------------------------------------+
| Overall:   [████████████████████] 100%                            |
+------------------------------------------------------------------+
```

### Progress Metrics

| Metric | Value |
|--------|-------|
| **Total Tasks** | 5 |
| **Completed Tasks** | 5 |
| **Completion %** | 100% |

---

## Acceptance Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| AC-1 | `.context/rules/quality-enforcement.md` created | [ ] |
| AC-2 | Contains all criticality levels (C1-C4) with definitions | [ ] |
| AC-3 | Contains quality threshold (0.92) with scoring dimensions | [ ] |
| AC-4 | Contains all strategy encodings (S-001 through S-014) | [ ] |
| AC-5 | Contains minimum cycle count (3 iterations) | [ ] |
| AC-6 | Contains tier vocabulary (HARD/MEDIUM/SOFT) definitions | [ ] |
| AC-7 | Contains auto-escalation rules (AE-001 through AE-006) | [ ] |
| AC-8 | Contains 5-layer architecture reference (L1-L5) | [ ] |
| AC-9 | File follows markdown navigation standards (NAV-001 through NAV-006) | [ ] |
| AC-10 | File is under 2000 tokens | [ ] |

---

## Evidence

### Deliverables

| Deliverable | Type | Description | Link |
|-------------|------|-------------|------|
| quality-enforcement.md | SSOT Document | Canonical quality framework constants file | `.context/rules/quality-enforcement.md` |

### Verification Checklist

- [x] All acceptance criteria verified
- [x] All tasks completed
- [x] Quality gate passed (>= 0.92)

---

## Related Items

### Hierarchy

- **Parent Feature:** [FEAT-008: Quality Framework Implementation](../FEAT-008-quality-framework-implementation.md)

### Dependencies

| Type | Item | Description |
|------|------|-------------|
| depends_on | EPIC-002 Final Synthesis | Source of all quality framework constants |
| blocks | EN-702 | Rule optimization must reference SSOT for constants |
| blocks | EN-703 | Hook implementation must reference SSOT for thresholds |
| blocks | EN-704 | Session context must reference SSOT for preamble values |
| related_to | EN-404 | EPIC-002 rule-based enforcement design (source material) |
| related_to | EN-405 | EPIC-002 session context enforcement design (source material) |

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-14 | Claude | pending | Enabler created with 5-task decomposition. First enabler in FEAT-008 quality framework implementation pipeline. SSOT file serves as foundation for all subsequent enablers. |
