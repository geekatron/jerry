# EN-203: TODO Section Migration

<!--
TEMPLATE: Enabler
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.9
CREATED: 2026-02-01 (Claude)
PURPOSE: Migrate TODO section content from CLAUDE.md to worktracker skill
-->

> **Type:** enabler
> **Status:** complete
> **Priority:** high
> **Impact:** medium
> **Enabler Type:** architecture
> **Created:** 2026-02-01T00:00:00Z
> **Due:** 2026-02-10T00:00:00Z
> **Completed:** 2026-02-02T08:42:00Z
> **Parent:** FEAT-002
> **Owner:** Claude
> **Effort:** 3

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What this enabler delivers |
| [Enabler Type Classification](#enabler-type-classification) | ARCHITECTURE type classification |
| [Problem Statement](#problem-statement) | Why this migration is needed |
| [Business Value](#business-value) | Features unlocked |
| [Technical Approach](#technical-approach) | Target structure |
| [Children (Tasks)](#children-tasks) | Task inventory and dependencies |
| [Progress Summary](#progress-summary) | Completion status |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done |
| [Evidence](#evidence) | Deliverables and verification |
| [Risks and Mitigations](#risks-and-mitigations) | Risk management |
| [Dependencies](#dependencies) | What this depends on and enables |
| [Related Items](#related-items) | Hierarchy |
| [History](#history) | Change log |

---

## Summary

Migrate the TODO section (~80 lines) from CLAUDE.md to the worktracker skill's rules directory. This includes all META TODO requirements and TODO behavior rules.

**Technical Scope:**
- Create todo-integration.md rule file
- Move META TODO requirements to worktracker skill
- Add brief TODO mention in CLAUDE.md quick reference
- Update skill to load TODO rules on invocation

---

## Enabler Type Classification

**This Enabler Type:** ARCHITECTURE (restructuring context loading architecture)

---

## Problem Statement

The current CLAUDE.md contains ~80 lines of TODO behavior rules that:
1. Are only needed when using the TODO/task tracking features
2. Contribute to context overhead at session start
3. Should be loaded on-demand with worktracker skill

---

## Business Value

Migrating TODO content provides:
- Additional ~80 lines removed from CLAUDE.md
- On-demand loading when TODO features needed
- Consolidation of all worktracker-related content in one skill

### Features Unlocked

- Leaner CLAUDE.md
- Unified worktracker skill experience

---

## Technical Approach

Create a dedicated rule file for TODO integration at `skills/worktracker/rules/todo-integration.md` containing all META TODO requirements and behavior rules.

### Target Structure

```
skills/worktracker/
├── SKILL.md
└── rules/
    ├── ... (existing)
    └── todo-integration.md    # NEW: TODO behavior rules
```

---

## Children (Tasks)

### Task Inventory

| ID | Title | Status | Effort | Owner |
|----|-------|--------|--------|-------|
| [TASK-001](./TASK-001-create-todo-integration-rules.md) | Create todo-integration.md rule file | **DONE** | 1 | Claude |
| [TASK-002](./TASK-002-move-meta-todo-requirements.md) | Move META TODO requirements | **DONE** | 1 | Claude |
| [TASK-003](./TASK-003-add-brief-todo-mention.md) | Add brief TODO mention in CLAUDE.md | **DONE** | 0.5 | Claude |
| [TASK-004](./TASK-004-update-skill-todo-loading.md) | Update skill to load TODO rules | **DONE** | 0.5 | Claude |

### Task Dependencies

```
TASK-001 (Create rules file)
    |
    +---> TASK-002 (Move requirements)
              |
              +---> TASK-003, TASK-004 (can run in parallel)
```

---

## Progress Summary

### Status Overview

```
+------------------------------------------------------------------+
|                   ENABLER PROGRESS TRACKER                        |
+------------------------------------------------------------------+
| Tasks:     [####################] 100% (4/4 completed)           |
| Effort:    [####################] 100% (3/3 points completed)    |
+------------------------------------------------------------------+
| Overall:   [####################] 100% COMPLETE                  |
+------------------------------------------------------------------+
```

### Progress Metrics

| Metric | Value |
|--------|-------|
| **Total Tasks** | 4 |
| **Completed Tasks** | 4 |
| **Total Effort (points)** | 3 |
| **Completed Effort** | 3 |
| **Completion %** | 100% |

---

## Acceptance Criteria

### Definition of Done

- [x] todo-integration.md created in worktracker rules
- [x] All META TODO requirements migrated
- [x] Brief TODO pointer in CLAUDE.md quick reference
- [x] Worktracker skill loads TODO rules on invocation
- [x] No TODO section remains in CLAUDE.md

### Technical Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| TC-1 | todo-integration.md exists | [x] `skills/worktracker/rules/todo-integration-rules.md` (129 lines) |
| TC-2 | All META TODO items captured | [x] 15 META TODO items in lines 14-68 |
| TC-3 | CLAUDE.md has brief TODO mention only | [x] Only `/worktracker` skill pointer |
| TC-4 | /worktracker loads TODO content | [x] Referenced in SKILL.md line 117 |

---

## Evidence

### Deliverables

| Deliverable | Type | Description | Link |
|-------------|------|-------------|------|
| TODO Integration Rules | Documentation | TODO behavior rules | skills/worktracker/rules/todo-integration.md |

### Technical Verification

| Criterion | Verification Method | Evidence | Verified By | Date |
|-----------|---------------------|----------|-------------|------|
| Rules file exists | File check | - | - | - |
| Skill loads content | Manual test | - | - | - |

---

## Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Lost META TODO items | Low | Medium | Verify all items transferred |
| Users miss TODO guidance | Low | Low | Brief pointer in CLAUDE.md |

---

## Dependencies

### Depends On

- [EN-201: Worktracker Skill Extraction](../EN-201-worktracker-skill-extraction/EN-201-worktracker-skill-extraction.md) - Worktracker skill must be updated first

### Enables

- [EN-204: Validation & Testing](../EN-204-validation-testing/EN-204-validation-testing.md)

---

## Related Items

### Hierarchy

- **Parent:** [FEAT-002: CLAUDE.md Optimization](../FEAT-002-claude-md-optimization.md)

### Source Content

Current CLAUDE.md `<todo>` section contains:
- META TODO items (must always be on list)
- TODO behavior rules
- Worktracker sync requirements

---

## Evidence

### Deliverables

| Deliverable | Type | Description | Link |
|-------------|------|-------------|------|
| TODO Integration Rules | Documentation | TODO behavior rules (129 lines, 5,832 bytes) | `skills/worktracker/rules/todo-integration-rules.md` |

### Technical Verification

| Criterion | Verification Method | Evidence | Verified By | Date |
|-----------|---------------------|----------|-------------|------|
| Rules file exists | File check | 5,832 bytes | Verification Agent | 2026-02-02 |
| META TODO items complete | Manual review | 15 META items documented | Verification Agent | 2026-02-02 |
| SKILL.md reference | Manual review | Line 117 in SKILL.md | Verification Agent | 2026-02-02 |
| No TODO in CLAUDE.md | Grep check | Only skill pointer exists | Verification Agent | 2026-02-02 |

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-01T00:00:00Z | Claude | pending | Enabler created |
| 2026-02-02T08:42:00Z | Claude | complete | Work completed as part of EN-202 gap closure (BUG-004). Created `todo-integration-rules.md` with all META TODO items. |
| 2026-02-02T10:00:00Z | Verification Agent | complete | Backward verification confirmed all acceptance criteria met. Status updated from `pending` to `complete`. |

---

## System Mapping

| System | Mapping |
|--------|---------|
| **Azure DevOps** | PBI with ValueArea=Architectural |
| **SAFe** | Enabler (ARCHITECTURE type) |
| **JIRA** | Story with 'enabler' label |
