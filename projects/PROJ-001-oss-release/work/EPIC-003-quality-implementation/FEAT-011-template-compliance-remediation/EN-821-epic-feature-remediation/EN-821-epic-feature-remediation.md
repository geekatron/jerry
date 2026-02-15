# EN-821: Remediate EPIC & FEATURE Entity Files

<!--
TEMPLATE: Enabler
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.9
-->

> **Type:** enabler
> **Status:** DONE
> **Completed:** 2026-02-15
> **Priority:** high
> **Impact:** high
> **Enabler Type:** infrastructure
> **Created:** 2026-02-15
> **Parent:** FEAT-011
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

Add missing REQUIRED and RECOMMENDED sections to the EPIC-003 epic file and all 3 feature files (FEAT-008, FEAT-009, FEAT-010). Guided by EPIC.md and FEATURE.md template REFERENCE sections.

**Technical Scope:**
- Add Milestone Tracking to EPIC-003, fix stale progress data
- Add Sprint Tracking to all 3 feature files (FEAT-008, FEAT-009, FEAT-010)
- Add Functional/Non-Functional AC to FEAT-008
- Fix naming inconsistencies in Children tables across all files

---

## Problem Statement

EPIC-003 is missing 6 sections including a stale Progress Summary that does not reflect actual completion state. All 3 feature files (FEAT-008, FEAT-009, FEAT-010) are missing the Sprint Tracking subsection which is RECOMMENDED by the FEATURE template. Additionally, FEAT-008 lacks Functional and Non-Functional Acceptance Criteria tables, and Children tables across files use inconsistent naming (varying column headers and section titles).

These gaps prevent accurate progress reporting, formal feature closure, and consistent navigability across the worktracker hierarchy.

---

## Business Value

Enables accurate progress tracking across the EPIC-003 hierarchy, formal feature closure with Sprint Tracking data, and complete acceptance criteria for FEAT-008.

### Features Unlocked

- Proper progress reporting with accurate data across EPIC and FEATURE levels
- Feature closure readiness with Sprint Tracking for all 3 features

---

## Technical Approach

1. **Remediate EPIC-003** -- Add Milestone Tracking section, fix stale Progress Summary data to reflect actual enabler completion state, normalize Children table to use "Enabler Inventory" naming with correct columns.
2. **Remediate FEAT-008** -- Add Sprint Tracking subsection, add Functional Criteria and Non-Functional Criteria tables to Acceptance Criteria, normalize Children table.
3. **Remediate FEAT-009** -- Add Sprint Tracking subsection, normalize Children table.
4. **Remediate FEAT-010** -- Add Sprint Tracking subsection, normalize Children table.

---

## Children (Tasks)

### Task Inventory

| ID | Title | Status | Activity | Agents |
|----|-------|--------|----------|--------|
| TASK-001 | Remediate EPIC-003 entity file | DONE | DEVELOPMENT | ps-architect |
| TASK-002 | Remediate FEAT-008 entity file | DONE | DEVELOPMENT | ps-architect |
| TASK-003 | Remediate FEAT-009 entity file | DONE | DEVELOPMENT | ps-architect |
| TASK-004 | Remediate FEAT-010 entity file | DONE | DEVELOPMENT | ps-architect |

### Task Dependencies

All 4 tasks are independent and can be executed in parallel. Each task targets a single entity file. No ordering constraints exist between them.

---

## Progress Summary

### Status Overview

```
+------------------------------------------------------------------+
|                   ENABLER PROGRESS TRACKER                        |
+------------------------------------------------------------------+
| Tasks:     [████████████████████] 100% (4/4 completed)           |
| Effort:    [████████████████████] 100% (5/5 points completed)    |
+------------------------------------------------------------------+
| Overall:   [████████████████████] 100%                            |
+------------------------------------------------------------------+
```

### Progress Metrics

| Metric | Value |
|--------|-------|
| **Total Tasks** | 4 |
| **Completed Tasks** | 4 |
| **Total Effort (points)** | 5 |
| **Completed Effort** | 5 |
| **Completion %** | 100% |

---

## Acceptance Criteria

### Definition of Done

- [x] EPIC-003 has Milestone Tracking and accurate progress data
- [x] All 3 features have Sprint Tracking subsection
- [x] FEAT-008 has Functional and Non-Functional Criteria tables
- [x] Children tables use consistent naming ("Enabler Inventory" with correct columns)
- [x] Creator-critic-revision cycle completed (min 3 iterations, >= 0.92)

### Technical Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| TC-1 | EPIC-003 has Milestone Tracking and accurate progress data | [x] |
| TC-2 | All 3 features have Sprint Tracking subsection | [x] |
| TC-3 | FEAT-008 has Functional and Non-Functional Criteria tables | [x] |
| TC-4 | Children tables use consistent naming ("Enabler Inventory" with correct columns) | [x] |

---

## Evidence

### Deliverables

| Deliverable | Type | Description | Link |
|-------------|------|-------------|------|
| EPIC-003 remediated | Entity file | Milestone Tracking + progress fix | `EPIC-003-quality-implementation.md` |
| FEAT-008 remediated | Entity file | Sprint Tracking + AC tables | `FEAT-008-quality-framework-implementation.md` |
| FEAT-009 remediated | Entity file | Sprint Tracking + Children normalization | `FEAT-009-adversarial-strategy-templates.md` |
| FEAT-010 remediated | Entity file | Sprint Tracking + Children normalization | `FEAT-010-tournament-remediation.md` |

### Technical Verification

| Criterion | Verification Method | Evidence | Verified By | Date |
|-----------|---------------------|----------|-------------|------|
| TC-1 | Inspect EPIC-003.md Milestone Tracking section | -- | -- | -- |
| TC-2 | Inspect Sprint Tracking in FEAT-008, FEAT-009, FEAT-010 | -- | -- | -- |
| TC-3 | Inspect FEAT-008 Acceptance Criteria tables | -- | -- | -- |
| TC-4 | Inspect Children table headers across all 4 files | -- | -- | -- |

### Verification Checklist

- [x] All acceptance criteria verified
- [x] All tasks completed
- [x] Technical review complete
- [x] Documentation updated

---

## Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Stale progress data in EPIC-003 requires manual audit of all enablers | Medium | Low | Cross-reference enabler status from individual enabler files |
| Sprint Tracking data unavailable for completed features | Medium | Low | Use best-effort estimates from History sections and commit timestamps |
| Children table normalization breaks existing cross-references | Low | Medium | Verify no automated tooling parses current column headers before changing |

---

## Dependencies

### Depends On

- EN-820 (behavioral root cause fix must come first to prevent future non-compliance)

### Enables

- Accurate EPIC-003 progress reporting
- Feature closure readiness for FEAT-008, FEAT-009, FEAT-010

---

## Related Items

### Hierarchy

- **Parent:** FEAT-011

### Related Items

- **Blocked By:** EN-820 (behavioral fix must precede remediation)
- **Related Discovery:** DISC-001 (audit findings for EPIC and FEATURE files)

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-15 | Claude | pending | Enabler created. Source: DISC-001 audit findings for EPIC-003, FEAT-008, FEAT-009, FEAT-010. |
| 2026-02-15 | Claude | DONE | All 4 entity files remediated. Commit: 4a7cc56. |
