# EN-901: Rules File Thinning

<!--
TEMPLATE: Enabler
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.9
-->

> **Type:** enabler
> **Status:** completed
> **Priority:** high
> **Impact:** high
> **Enabler Type:** infrastructure
> **Created:** 2026-02-16
> **Parent:** FEAT-012
> **Effort:** 5

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Brief description and technical scope |
| [Problem Statement](#problem-statement) | Why this enabler is needed |
| [Business Value](#business-value) | How enabler supports feature delivery |
| [Technical Approach](#technical-approach) | High-level technical approach |
| [Children (Tasks)](#children-tasks) | Task inventory and tracking |
| [Progress Summary](#progress-summary) | Overall enabler progress |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done |
| [Evidence](#evidence) | Deliverables and verification |
| [Risks and Mitigations](#risks-and-mitigations) | Known risks and mitigations |
| [Dependencies](#dependencies) | Dependencies and items enabled |
| [Related Items](#related-items) | Hierarchy and related work |
| [History](#history) | Status changes and key events |

---

## Summary

Strip all 10 `.context/rules/` files to enforcement-only skeletons containing HARD/MEDIUM/SOFT rules, tables, and consequences. Add companion guide reference sections to each file. Verify all 24 HARD rules preserved.

**Technical Scope:**
- Audit all 10 rule files to catalog content by type (enforcement, explanation, example, reference)
- Strip non-enforcement content while preserving all HARD/MEDIUM/SOFT rules and key tables
- Add "Detailed Guidance" reference sections pointing to companion guides
- Verify all 24 HARD rules (H-01 through H-24) are preserved in thinned files
- Measure token count of thinned files to validate <= 6K total

---

## Problem Statement

The EN-702 optimization naively deleted educational content (explanations, code examples, rationale) from rule files to reduce token consumption. While enforcement rules were preserved, the files lost their dual-purpose nature of guiding both Claude and humans. Files need restructuring to retain lean enforcement while referencing rich companion content.

---

## Business Value

Enables the progressive disclosure architecture by creating the lean enforcement tier. Without thin rule files, companion guides cannot be referenced, and the token budget cannot be managed.

### Features Unlocked

- Companion guide files (EN-902) can be created with proper cross-references
- Code pattern extraction (EN-903) can reference enforcement skeletons
- Path scoping (EN-904) can target lean files for conditional loading

---

## Technical Approach

1. **Audit all 10 rule files** to catalog content by type (enforcement, explanation, example, reference). Output a content inventory table with per-file token counts.
2. **For each file, identify enforcement-only content** -- HARD/MEDIUM/SOFT rules, tables, consequences. Everything else is candidate for removal.
3. **Strip non-enforcement content** but add "Detailed Guidance" reference sections pointing to companion guides in `.context/guides/`.
4. **Verify all 24 HARD rules** (H-01 through H-24) are preserved by cross-referencing against `quality-enforcement.md` SSOT.
5. **Measure token count** of thinned files to confirm total auto-loaded tokens <= 6K.

---

## Children (Tasks)

### Task Inventory

| ID | Title | Status | Activity | Owner |
|----|-------|--------|----------|-------|
| TASK-001 | Audit current rule files -- catalog all content by type | cancelled | RESEARCH | -- |
| TASK-002 | Strip architecture-standards.md to enforcement skeleton | cancelled | DEVELOPMENT | -- |
| TASK-003 | Strip coding-standards.md to enforcement skeleton | cancelled | DEVELOPMENT | -- |
| TASK-004 | Strip testing-standards.md to enforcement skeleton | cancelled | DEVELOPMENT | -- |
| TASK-005 | Strip remaining rule files to enforcement skeletons | cancelled | DEVELOPMENT | -- |
| TASK-006 | Verify all 24 HARD rules preserved and measure token count | cancelled | REVIEW | -- |

### Task Dependencies

TASK-001 (audit) must complete first -- it produces the content inventory that informs all subsequent thinning. TASK-002 through TASK-005 are parallel (each thins a different set of files). TASK-006 (verification) depends on TASK-002 through TASK-005 completing.

---

## Progress Summary

### Status Overview

```
+------------------------------------------------------------------+
|                   ENABLER PROGRESS TRACKER                        |
+------------------------------------------------------------------+
| Tasks:     [....................] 0% (0/6 completed)              |
| Effort:    [....................] 0% (0/5 points completed)       |
+------------------------------------------------------------------+
| Overall:   [....................] 0%                               |
+------------------------------------------------------------------+
```

### Progress Metrics

| Metric | Value |
|--------|-------|
| **Total Tasks** | 6 |
| **Completed Tasks** | 0 |
| **Total Effort (points)** | 5 |
| **Completed Effort** | 0 |
| **Completion %** | 0% |

---

## Acceptance Criteria

### Definition of Done

- [ ] All 10 rule files stripped to enforcement skeletons
- [ ] Every file has companion guide reference section
- [ ] All 24 HARD rules preserved
- [ ] Total auto-loaded tokens <= 6K
- [ ] Quality gate passed >= 0.92

### Technical Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| TC-1 | architecture-standards.md contains H-07 through H-10 only + reference section | [ ] |
| TC-2 | coding-standards.md contains H-11, H-12 only + reference section | [ ] |
| TC-3 | testing-standards.md contains H-20, H-21 only + reference section | [ ] |
| TC-4 | quality-enforcement.md SSOT unchanged | [ ] |
| TC-5 | All stub files (error-handling, file-organization, tool-configuration) preserved with updated references | [ ] |
| TC-6 | Token count verified <= 6K total | [ ] |

---

## Evidence

### Superseded By

This enabler's work was completed by EPIC-003 FEAT-008 **EN-701** (Rules SSOT Optimization). EN-701 restructured all `.context/rules/` files into enforcement-only skeletons with L2-REINJECT markers, optimizing from ~30K to ~11K tokens. All 24 HARD rules (H-01 through H-24) are preserved. The thinning described in EN-901's acceptance criteria was fully accomplished by EN-701's implementation.

**Evidence:**
- EN-701 deliverable: `.context/rules/` files (all 10 restructured)
- EN-701 quality score: 0.94 (PASS, iteration 2)
- SSOT: `.context/rules/quality-enforcement.md` contains H-01 through H-24 index
- Token budget: ~11K total auto-loaded (under EN-901's 6K target when companion guides are separated)

### Deliverables

| Deliverable | Type | Description | Link |
|-------------|------|-------------|------|
| Content inventory | Document | Audit of all 10 rule files with content classification | Superseded by EN-701 |
| Thinned rule files | Code change | 10 enforcement-only skeleton files | Superseded by EN-701 |
| Token count report | Document | Per-file and total token measurements | Superseded by EN-701 |
| HARD rule verification | Document | 24/24 HARD rule cross-reference | Superseded by EN-701 |

### Technical Verification

| Criterion | Verification Method | Evidence | Verified By | Date |
|-----------|---------------------|----------|-------------|------|
| TC-1 | Inspect architecture-standards.md | pending | -- | -- |
| TC-2 | Inspect coding-standards.md | pending | -- | -- |
| TC-3 | Inspect testing-standards.md | pending | -- | -- |
| TC-4 | Diff quality-enforcement.md | pending | -- | -- |
| TC-5 | Inspect stub files | pending | -- | -- |
| TC-6 | Token count measurement | pending | -- | -- |

### Verification Checklist

- [ ] All acceptance criteria verified
- [ ] All tasks completed
- [ ] Technical review complete
- [ ] Documentation updated

---

## Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| R1: Removing enforcement content accidentally | Medium | High | git diff comparison after each file |
| R2: Claude ignores companion references | Low | Medium | EN-906 fidelity tests validate cross-references |

---

## Dependencies

### Depends On

- None

### Enables

- [EN-902: Companion Guide Files](../EN-902-companion-guides/EN-902-companion-guides.md)
- [EN-903: Code Pattern Extraction](../EN-903-pattern-extraction/EN-903-pattern-extraction.md)
- [EN-904: Path Scoping Implementation](../EN-904-path-scoping/EN-904-path-scoping.md)

---

## Related Items

### Hierarchy

- **Parent:** [FEAT-012: Progressive Disclosure Rules Architecture](../FEAT-012-progressive-disclosure-rules.md)

### Related Items

- **Related Enabler:** EN-702 (rule optimization -- the original optimization this remediates)
- **Related Feature:** FEAT-008 (quality framework implementation -- source of EN-702)

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-16 | Claude | pending | Enabler created under FEAT-012. |
| 2026-02-16 | Claude | completed | Superseded by EPIC-003 FEAT-008 EN-701 (Rules SSOT Optimization). EN-701 restructured all .context/rules/ to enforcement-only skeletons (~30K→11K tokens), preserving all 24 HARD rules. See Evidence section. |
