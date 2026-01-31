# EN-018: FEAT-002 Task Renumbering

<!--
TEMPLATE: Enabler
VERSION: 1.0.0
SOURCE: User feedback on task ID conventions
CREATED: 2026-01-27
PURPOSE: Tech debt enabler to fix global task numbering to enabler-scoped
-->

> **Type:** enabler
> **Status:** pending
> **Priority:** low
> **Impact:** low
> **Enabler Type:** compliance
> **Created:** 2026-01-27T00:00:00Z
> **Due:** TBD
> **Completed:**
> **Parent:** FEAT-003
> **Owner:** Claude
> **Effort:** 5

---

## Summary

Refactor **task numbering** across FEAT-002 enablers from **global numbering** (TASK-101, TASK-107, TASK-131, etc.) to **enabler-scoped numbering** (TASK-001, TASK-002, TASK-003 within each enabler).

**Tech Debt Origin:** User feedback during TASK-107 execution (2026-01-27)

---

## Problem Statement

### Current State (Incorrect)

The current task numbering in FEAT-002 uses a global sequence:
- EN-007: TASK-101, TASK-102, TASK-103, TASK-104, TASK-105, TASK-105A, TASK-106, TASK-107
- EN-008: TASK-107, TASK-108, TASK-109, TASK-110
- EN-015: TASK-131, TASK-132, TASK-133, TASK-134

This causes:
1. **ID Collision:** EN-007:TASK-107 and EN-008:TASK-107 both exist
2. **Worktracker Violation:** Per worktracker conventions, tasks should restart within each enabler (aggregate root)
3. **Confusion:** Global numbering implies cross-enabler dependencies that don't exist

### Expected State (Correct)

Per worktracker conventions, tasks should be enabler-scoped:
- EN-007: TASK-001, TASK-002, TASK-003, TASK-004, TASK-005, TASK-005A, TASK-006, TASK-007
- EN-008: TASK-001, TASK-002, TASK-003, TASK-004
- EN-015: TASK-001, TASK-002, TASK-003, TASK-004

---

## Business Value

| Benefit | Value |
|---------|-------|
| **Consistency** | Aligns with worktracker conventions |
| **Clarity** | No more ID collisions across enablers |
| **Maintainability** | Easier to navigate per-enabler task lists |
| **Standards Compliance** | Worktracker defines enabler as aggregate root |

---

## Technical Approach

### L0: Simple Analogy

Like renaming house numbers from "123 Main Street, Apt 1-50" to "Apt 1, Apt 2, Apt 3" within each building.

### L1: Technical Implementation

1. **Inventory Phase:**
   - Enumerate all task files in FEAT-002 enablers
   - Map old ID → new ID for each enabler
   - Document cross-references that need updating

2. **Rename Phase (per enabler):**
   - Rename task files: `TASK-101-*.md` → `TASK-001-*.md`
   - Update task file internal IDs
   - Update parent enabler task tables
   - Update any cross-references

3. **Verification Phase:**
   - Verify all links still resolve
   - Run link checker on FEAT-002
   - Update any external references (e.g., ps-critic reviews)

### L2: Architectural Considerations

- **Risk:** Many files affected (~37 tasks across 10 enablers)
- **Mitigation:** Batch processing with verification step
- **Rollback:** Git provides full rollback capability

---

## Scope

### Enablers to Update

| Enabler | Current Tasks | New Tasks |
|---------|---------------|-----------|
| EN-007 | TASK-101..TASK-107 | TASK-001..TASK-007 |
| EN-008 | TASK-107..TASK-110 | TASK-001..TASK-004 |
| EN-009 | TASK-111..TASK-116 | TASK-001..TASK-006 |
| EN-013 | TASK-117..TASK-122 | TASK-001..TASK-006 |
| EN-014 | TASK-123..TASK-125 | TASK-001..TASK-003 |
| EN-015 | TASK-131..TASK-138 | TASK-001..TASK-008 |
| EN-016 | TASK-139..TASK-145 | TASK-001..TASK-007 |

**Note:** Exact task counts may vary; inventory phase will confirm.

---

## Acceptance Criteria

### Definition of Done

- [ ] All FEAT-002 task files renamed to enabler-scoped IDs
- [ ] All enabler task tables updated with new IDs
- [ ] All internal cross-references updated
- [ ] All external references (reviews, discoveries) updated
- [ ] Link verification passes with no broken links
- [ ] No ID collisions exist

---

## Children (Tasks)

| ID | Title | Status | Effort |
|----|-------|--------|--------|
| TASK-001 | Create task ID mapping inventory | pending | 1 |
| TASK-002 | Rename EN-007 tasks | pending | 1 |
| TASK-003 | Rename EN-008 tasks | pending | 1 |
| TASK-004 | Rename remaining enabler tasks | pending | 1 |
| TASK-005 | Update cross-references | pending | 1 |

**NOTE:** Tasks use enabler-scoped numbering (TASK-001, TASK-002, etc.) per worktracker conventions.

---

## Related Items

| Type | Item | Description |
|------|------|-------------|
| Reference | [worktracker.md](../../../../../.context/templates/worktracker/README.md) | Worktracker conventions defining enabler as aggregate root |
| Affects | [FEAT-002](../../FEAT-002-implementation/FEAT-002-implementation.md) | Feature containing tasks to be renumbered |
| Origin | EN-007:TASK-107 discovery | Collision discovered during encoding fallback task |

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-01-27 | Claude | pending | Enabler created per user feedback on task ID conventions |
