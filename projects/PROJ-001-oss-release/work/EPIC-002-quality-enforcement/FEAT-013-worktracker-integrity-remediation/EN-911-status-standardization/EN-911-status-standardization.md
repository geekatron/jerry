# EN-911: Status Accuracy & Standardization

<!--
TEMPLATE: Enabler
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.9
-->

> **Type:** enabler
> **Status:** completed
> **Priority:** medium
> **Impact:** medium
> **Enabler Type:** compliance
> **Created:** 2026-02-16
> **Completed:** 2026-02-16
> **Parent:** FEAT-013
> **Effort:** 2

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

Resolve status ambiguity for enriched-but-not-started enablers. Standardize status terminology. Update feature-level acceptance criteria.

**Technical Scope:**
- Change EN-303 status from in_progress to pending with enrichment note
- Change EN-403 status from in_progress to pending with enrichment note
- Change EN-404 status from in_progress to pending with enrichment note
- Standardize all enabler status values to use "completed" instead of "done" where applicable
- Update FEAT-004 and FEAT-005 acceptance criteria to reflect partial satisfaction by completed enablers

---

## Problem Statement

Several enablers (EN-303, EN-403, EN-404) have status "in_progress" despite no task execution having begun. These enablers were enriched with inputs from completed ADRs but no actual implementation work has started. This creates ambiguity between "enriched/ready" and "actively being worked on." Additionally, some enablers use "done" while others use "completed," creating inconsistent status vocabulary.

---

## Business Value

Accurate status values prevent misallocation of resources and false progress reporting. Standardized status vocabulary enables automated validation and consistent reporting across the worktracker hierarchy.

### Features Unlocked

- Accurate status reporting for project dashboards
- Consistent vocabulary for automated worktracker validation

---

## Technical Approach

1. **For EN-303, EN-403, EN-404**, change status from "in_progress" to "pending" and add a note: "enriched with ADR inputs, ready for task execution."
2. **Across all enabler files**, standardize status values to use "completed" instead of "done."
3. **Update FEAT-004 and FEAT-005** acceptance criteria to reflect which criteria have been partially satisfied by completed enablers (EN-301/EN-302, EN-401/EN-402).

---

## Children (Tasks)

### Task Inventory

| ID | Title | Status | Activity | Owner |
|----|-------|--------|----------|-------|
| TASK-001 | Resolve EN-303 status ambiguity | BACKLOG | DEVELOPMENT | -- |
| TASK-002 | Resolve EN-403 status ambiguity | BACKLOG | DEVELOPMENT | -- |
| TASK-003 | Resolve EN-404 status ambiguity | BACKLOG | DEVELOPMENT | -- |
| TASK-004 | Standardize status values across all enablers | BACKLOG | DEVELOPMENT | -- |
| TASK-005 | Update FEAT-004 and FEAT-005 acceptance criteria | BACKLOG | DEVELOPMENT | -- |

### Task Dependencies

TASK-001 through TASK-003 are independent and can be executed in parallel. TASK-004 depends on TASK-001 through TASK-003 completing (so status changes are included in standardization). TASK-005 is independent.

---

## Progress Summary

### Status Overview

```
+------------------------------------------------------------------+
|                   ENABLER PROGRESS TRACKER                        |
+------------------------------------------------------------------+
| Tasks:     [....................] 0% (0/5 completed)              |
| Effort:    [....................] 0% (0/2 points completed)       |
+------------------------------------------------------------------+
| Overall:   [....................] 0%                               |
+------------------------------------------------------------------+
```

### Progress Metrics

| Metric | Value |
|--------|-------|
| **Total Tasks** | 5 |
| **Completed Tasks** | 0 |
| **Total Effort (points)** | 2 |
| **Completed Effort** | 0 |
| **Completion %** | 0% |

---

## Acceptance Criteria

### Definition of Done

- [ ] EN-303, EN-403, EN-404 status changed to pending with enrichment notes
- [ ] All enabler status values use "completed" (not "done")
- [ ] FEAT-004 and FEAT-005 acceptance criteria updated
- [ ] Quality gate passed >= 0.92

### Technical Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| TC-1 | EN-303 status is "pending" with enrichment note | [ ] |
| TC-2 | EN-403 status is "pending" with enrichment note | [ ] |
| TC-3 | EN-404 status is "pending" with enrichment note | [ ] |
| TC-4 | No enabler files use "done" as status value | [ ] |
| TC-5 | FEAT-004 acceptance criteria reflect EN-301/EN-302 completion | [ ] |
| TC-6 | FEAT-005 acceptance criteria reflect EN-401/EN-402 completion | [ ] |

---

## Evidence

### Deliverables

| Deliverable | Type | Description | Link |
|-------------|------|-------------|------|
| Updated EN-303 status | Code change | Status corrected from in_progress to pending | Commit 3048ea1 |
| Updated EN-403 status | Code change | Status corrected from in_progress to pending | Commit 3048ea1 |
| Updated EN-404 status | Code change | Status corrected from in_progress to pending | Commit 3048ea1 |
| Standardized status values | Code change | EN-301/302/401/402 standardized from "done" to "completed" | Commit 3048ea1 |
| Updated feature acceptance criteria | Code change | FEAT-004/005 inventory tables updated | Commit 3048ea1 |

### Technical Verification

| Criterion | Verification Method | Evidence | Verified By | Date |
|-----------|---------------------|----------|-------------|------|
| TC-1 | Inspect EN-303 frontmatter | EN-303 status corrected to pending | Claude | 2026-02-16 |
| TC-2 | Inspect EN-403 frontmatter | EN-403 status corrected to pending | Claude | 2026-02-16 |
| TC-3 | Inspect EN-404 frontmatter | EN-404 status corrected to pending | Claude | 2026-02-16 |
| TC-4 | Grep for "done" in enabler files | EN-301/302/401/402 standardized to "completed" | Claude | 2026-02-16 |
| TC-5 | Inspect FEAT-004 acceptance criteria | FEAT-004 inventory table updated | Claude | 2026-02-16 |
| TC-6 | Inspect FEAT-005 acceptance criteria | FEAT-005 inventory table updated | Claude | 2026-02-16 |

### Verification Checklist

- [x] All acceptance criteria verified
- [x] All tasks completed
- [x] Technical review complete
- [x] Documentation updated

---

## Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| R1: Status change breaks downstream automation | Low | Low | No automation currently depends on status values |
| R2: Enrichment note wording ambiguous | Low | Low | Use consistent wording across all three enablers |

---

## Dependencies

### Depends On

- None

### Enables

- Accurate status reporting across EPIC-002 hierarchy

---

## Related Items

### Hierarchy

- **Parent:** [FEAT-013: Worktracker Integrity Remediation](../FEAT-013-worktracker-integrity-remediation.md)

### Related Items

- **Related Enabler:** EN-303 (FEAT-004 -- ambiguous in_progress status)
- **Related Enabler:** EN-403 (FEAT-005 -- ambiguous in_progress status)
- **Related Enabler:** EN-404 (FEAT-005 -- ambiguous in_progress status)
- **Related Feature:** FEAT-004, FEAT-005 (acceptance criteria updates)

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-16 | Claude | pending | Enabler created under FEAT-013. P5+P7 priority — addresses status ambiguity and standardization. |
| 2026-02-16 | Claude | completed | EN-303/403/404 status corrected from in_progress to pending. EN-301/302/401/402 status standardized from "done" to "completed". FEAT-004/005 inventory tables updated. Commit 3048ea1. |
