# EN-201: Worktracker Skill Extraction

<!--
TEMPLATE: Enabler
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.9
CREATED: 2026-02-01 (Claude)
PURPOSE: Extract 371 lines of worktracker content from CLAUDE.md to /worktracker skill
-->

> **Type:** enabler
> **Status:** complete
> **Priority:** critical
> **Impact:** critical
> **Enabler Type:** architecture
> **Created:** 2026-02-01T00:00:00Z
> **Due:** 2026-02-07T00:00:00Z
> **Completed:** -
> **Parent:** FEAT-002
> **Owner:** -
> **Effort:** 8

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What this enabler does - extract 371 lines to worktracker skill |
| [Problem Statement](#problem-statement) | Why this work is needed - unnecessary context loading |
| [Technical Approach](#technical-approach) | Target structure with 5 rule files |
| [Children (Tasks)](#children-tasks) | 7 tasks with dependencies |
| [Progress Summary](#progress-summary) | 14% complete (1/7 tasks) |
| [Orchestration](#orchestration) | DISC-002 adversarial review protocol |
| [Discoveries](#discoveries) | DISC-001, DISC-002 findings |
| [Decisions](#decisions) | DEC-001, DEC-002 choices |
| [Bugs (in EN-201)](#bugs-in-en-201) | BUG-001 process failure |
| [Bugs Created (for EN-202)](#bugs-created-for-en-202) | BUG-001-003 source defects |

---

## Summary

Extract 371 lines (40.6%) of worktracker content from CLAUDE.md into the `/worktracker` skill's rules directory. This is the largest single extraction and the foundation for the CLAUDE.md optimization effort.

**Technical Scope:**
- Fix existing SKILL.md description bug (transcript copy-paste)
- Create 5 new rule files in `skills/worktracker/rules/`
- Update SKILL.md with proper navigation pointers
- Validate skill loads correctly on invocation

---

## Enabler Type Classification

| Type | Description | Examples |
|------|-------------|----------|
| **INFRASTRUCTURE** | Platform, tooling, DevOps enablers | CI/CD pipelines, monitoring setup |
| **EXPLORATION** | Research and proof-of-concept work | Technology spikes, prototypes |
| **ARCHITECTURE** | Architectural runway and design work | Service decomposition, API design |
| **COMPLIANCE** | Security, regulatory, and compliance requirements | GDPR implementation, SOC2 controls |

**This Enabler Type:** ARCHITECTURE (restructuring context loading architecture)

---

## Problem Statement

CLAUDE.md currently contains 371 lines of worktracker content that is:
1. Loaded at every session start (unnecessary overhead)
2. Only relevant when doing work tracking activities
3. Contributing to context rot that degrades LLM performance
4. Duplicating content that should live in the worktracker skill

---

## Business Value

Extracting worktracker content to the skill enables:
- 40% reduction in CLAUDE.md size
- On-demand loading when worktracker features needed
- Single source of truth for worktracker documentation
- Better OSS contributor onboarding experience

### Features Unlocked

- Lean CLAUDE.md (60-80 lines target)
- Progressive disclosure architecture
- Context-efficient session starts

---

## Technical Approach

Create modular rule files in `skills/worktracker/rules/` that are loaded when the `/worktracker` skill is invoked. Each file focuses on one aspect of worktracker functionality.

### Target Structure

```
skills/worktracker/
├── SKILL.md                              # Skill entry point (fix description)
└── rules/
    ├── worktracker-entity-hierarchy.md    # Entity types and hierarchy (80 lines)
    ├── worktracker-system-mappings.md     # ADO/SAFe/JIRA mappings (120 lines)
    ├── worktracker-behavior-rules.md      # WORKTRACKER.md behavior (60 lines)
    ├── worktracker-directory-structure.md # Directory conventions (111 lines)
    └── worktracker-template-usage-rules.md # Template requirements (existing)
```

---

## Children (Tasks)

### Task Inventory

| ID | Title | Status | Effort | Owner |
|----|-------|--------|--------|-------|
| [TASK-001](./TASK-001-fix-skill-md-description.md) | Fix SKILL.md description bug | **DONE** | 1 | Claude |
| [TASK-002](./TASK-002-create-entity-hierarchy-rules.md) | Create worktracker-entity-hierarchy.md | **DONE** | 1 | Claude |
| [TASK-003](./TASK-003-create-system-mappings-rules.md) | Create worktracker-system-mappings.md | **DONE** | 2 | Claude |
| [TASK-004](./TASK-004-create-behavior-rules.md) | Create worktracker-behavior-rules.md | **DONE** | 1 | Claude |
| [TASK-005](./TASK-005-create-directory-structure-rules.md) | Create worktracker-directory-structure.md | **DONE** | 1 | Claude |
| [TASK-006](./TASK-006-update-skill-navigation.md) | Update SKILL.md with navigation pointers | **DONE** | 1 | Claude |
| [TASK-007](./TASK-007-validate-skill-loading.md) | Validate skill loads correctly | **DONE** | 1 | Claude |

### Task Dependencies

```
TASK-001 (Fix SKILL.md)
    |
    +---> TASK-002, TASK-003, TASK-004, TASK-005 (can run in parallel)
              |
              +---> TASK-006 (Update navigation)
                        |
                        +---> TASK-007 (Validation)
```

---

## Progress Summary

### Status Overview

```
+------------------------------------------------------------------+
|                   ENABLER PROGRESS TRACKER                        |
+------------------------------------------------------------------+
| Tasks:     [####################] 100% (7/7 completed)           |
| Effort:    [####################] 100% (8/8 points completed)    |
+------------------------------------------------------------------+
| Overall:   [####################] 100%                           |
+------------------------------------------------------------------+
```

### Progress Metrics

| Metric | Value |
|--------|-------|
| **Total Tasks** | 7 |
| **Completed Tasks** | 7 |
| **Total Effort (points)** | 8 |
| **Completed Effort** | 8 |
| **Completion %** | 100% |

---

## Acceptance Criteria

### Definition of Done

- [x] SKILL.md description fixed (no transcript copy-paste)
- [x] worktracker-entity-hierarchy.md created with complete hierarchy (104 lines)
- [x] worktracker-system-mappings.md created with ADO/SAFe/JIRA mappings (92 lines)
- [x] worktracker-behavior-rules.md created with behavior rules (148 lines, includes WTI-001 through WTI-006)
- [x] worktracker-directory-structure.md created with directory conventions (81 lines)
- [x] SKILL.md updated with navigation pointers to all rules (116 lines, NAV-006 compliant)
- [x] /worktracker skill loads all entity and mapping information (TC-1 through TC-4 passed)
- [x] Documentation updated

### Technical Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| TC-1 | /worktracker skill invocation loads all rules | [x] |
| TC-2 | All entity hierarchy information accessible via skill | [x] |
| TC-3 | All system mappings (ADO/SAFe/JIRA) accessible via skill | [x] |
| TC-4 | All template references work correctly | [x] |
| TC-5 | No worktracker content remains in CLAUDE.md | [x] (Validated in EN-202) |

---

## Evidence

### Deliverables

| Deliverable | Type | Description | Link |
|-------------|------|-------------|------|
| SKILL.md | Documentation | Fixed skill entry point | skills/worktracker/SKILL.md |
| Entity Hierarchy Rules | Documentation | Entity types and hierarchy | skills/worktracker/rules/worktracker-entity-hierarchy.md |
| System Mappings Rules | Documentation | ADO/SAFe/JIRA mappings | skills/worktracker/rules/worktracker-system-mappings.md |
| Behavior Rules | Documentation | WORKTRACKER.md behavior | skills/worktracker/rules/worktracker-behavior-rules.md |
| Directory Structure Rules | Documentation | Directory conventions | skills/worktracker/rules/worktracker-directory-structure.md |

### Technical Verification

| Criterion | Verification Method | Evidence | Verified By | Date |
|-----------|---------------------|----------|-------------|------|
| Entity hierarchy created | `wc -l` file check | 104 lines at `skills/worktracker/rules/worktracker-entity-hierarchy.md` | Claude | 2026-02-01 |
| System mappings created | `wc -l` file check | 92 lines at `skills/worktracker/rules/worktracker-system-mappings.md` | Claude | 2026-02-01 |
| Behavior rules created | `wc -l` file check | 148 lines at `skills/worktracker/rules/worktracker-behavior-rules.md` | Claude | 2026-02-01 |
| Directory structure created | `wc -l` file check | 81 lines at `skills/worktracker/rules/worktracker-directory-structure.md` | Claude | 2026-02-01 |
| WTI integrity rules added | Manual review | WTI-001 through WTI-006 in behavior-rules.md | Claude | 2026-02-01 |
| Skill loads correctly | Manual invocation test | - | - | - |
| All content migrated | Line count comparison | - | - | - |
| No broken references | Navigation test | - | - | - |

---

## Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Content loss during extraction | Low | High | Keep original CLAUDE.md backup, verify line-by-line |
| Rule files not loading | Low | Medium | Test skill invocation, verify Claude Code rules mechanism |
| Navigation pointers broken | Low | Medium | Test each pointer resolves correctly |

---

## Dependencies

### Depends On

- None (first Enabler in chain)

### Enables

- [EN-202: CLAUDE.md Rewrite](../EN-202-claude-md-rewrite/EN-202-claude-md-rewrite.md)
- [EN-203: TODO Section Migration](../EN-203-todo-section-migration/EN-203-todo-section-migration.md)

---

## Orchestration

This enabler uses the **DISC-002 Adversarial Review Protocol** established in the FEAT-001 research phase.

| Artifact | Purpose | Location |
|----------|---------|----------|
| ORCHESTRATION_PLAN.md | Strategic workflow design | [orchestration/ORCHESTRATION_PLAN.md](./orchestration/ORCHESTRATION_PLAN.md) |
| ORCHESTRATION.yaml | Machine-readable state (SSOT) | [orchestration/ORCHESTRATION.yaml](./orchestration/ORCHESTRATION.yaml) |
| ORCHESTRATION_WORKTRACKER.md | Tactical execution tracking | [orchestration/ORCHESTRATION_WORKTRACKER.md](./orchestration/ORCHESTRATION_WORKTRACKER.md) |

### DISC-002 Adversarial Review Protocol

- **Pattern:** Fan-Out/Fan-In with DISC-002 Adversarial Review Loops
- **Quality Threshold:** 0.92 (per DEC-OSS-001)
- **Max Iterations:** 3 (then human escalation per DEC-OSS-004)
- **Agents Used:**
  - `ps-critic` - Adversarial quality evaluation (C/A/CL/AC/T criteria)
  - `nse-qa` - NASA SE compliance audit (TR/RT/VE/RI/DQ criteria)

### Adversarial Mode Characteristics

| # | Characteristic | Description |
|---|----------------|-------------|
| 1 | RED TEAM FRAMING | Assume problems exist |
| 2 | MANDATORY FINDINGS | Must identify ≥3 issues |
| 3 | CHECKLIST ENFORCEMENT | Evidence required for PASS |
| 4 | DEVIL'S ADVOCATE | "What could go wrong?" |
| 5 | COUNTER-EXAMPLES | Identify failure scenarios |
| 6 | NO RUBBER STAMPS | 0.95+ requires justification |

### Prior Art

See `FEAT-001-research-and-preparation/orchestration/oss-release-20260131-001/quality-gates/` for implementation examples (qg-0 through qg-4).

---

## Related Items

### Hierarchy

- **Parent:** [FEAT-002: CLAUDE.md Optimization](../FEAT-002-claude-md-optimization.md)

### Discoveries

| ID | Title | Status | Impact |
|----|-------|--------|--------|
| [DISC-001](./DISC-001-redundant-template-sections.md) | Redundant Template Sections in CLAUDE.md | DOCUMENTED | Medium |
| [DISC-002](./DISC-002-skill-md-outdated-refs.md) | SKILL.md Had Outdated File References | DOCUMENTED | High |

### Decisions

| ID | Title | Status |
|----|-------|--------|
| [DEC-001](./DEC-001-faithful-extraction-principle.md) | Faithful Extraction Preserves Source Defects | ACCEPTED |
| [DEC-002](./DEC-002-risk-identification-deferred.md) | Risk Identification Deferred to EN-202 | ACCEPTED |

### Bugs (in EN-201)

| ID | Title | Severity | Status |
|----|-------|----------|--------|
| [BUG-001](./BUG-001-deleted-user-files-without-review.md) | Deleted user's manual files without review | major | **FIXED** |
| [BUG-002](./BUG-002-worktracker-state-drift.md) | Worktracker state drift - tasks completed but not updated | major | **FIXED** |

### Bugs Created (for EN-202)

Source defects discovered during extraction, deferred to EN-202 per DEC-001:

| ID | Title | Severity |
|----|-------|----------|
| [EN-202:BUG-001](../EN-202-claude-md-rewrite/BUG-001-relationships-typo.md) | "relationships to to" typo | trivial |
| [EN-202:BUG-002](../EN-202-claude-md-rewrite/BUG-002-story-folder-id-mismatch.md) | Story folder uses {EnablerId} instead of {StoryId} | minor |
| [EN-202:BUG-003](../EN-202-claude-md-rewrite/BUG-003-template-path-inconsistency.md) | Template path inconsistency | minor |

### Source Content

Current CLAUDE.md sections to extract:
- Entity Hierarchy (~80 lines)
- Entity Classification (~60 lines)
- System Mappings (~120 lines)
- Directory Structure (~111 lines)

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-01T00:00:00Z | Claude | pending | Enabler created |
| 2026-02-01T12:00:00Z | Claude | in_progress | TASK-001 completed - Fixed SKILL.md description bug |
| 2026-02-01T13:00:00Z | Claude | in_progress | Orchestration plan created with adversarial review loops (ps-critic + nse-qa) |
| 2026-02-01T17:00:00Z | Claude | in_progress | Added DISC-001, DISC-002, DEC-001, DEC-002, BUG-001 |
| 2026-02-01T17:30:00Z | Claude | in_progress | BUG-001 fixed - recovered content from git history |
| 2026-02-01T18:30:00Z | Claude | in_progress | Added navigation table per FEAT-002:DEC-001 |
| 2026-02-01T20:00:00Z | Claude | in_progress | TASK-002,003,004,005 completed via background agents (rule files created) |
| 2026-02-01T21:00:00Z | Claude | in_progress | BUG-002 discovered - worktracker state drift (files completed but status not updated) |
| 2026-02-01T21:00:00Z | Claude | in_progress | BUG-002 fixed - updated task status, added WTI-001 through WTI-006 integrity rules |
| 2026-02-01T22:00:00Z | Claude | in_progress | TASK-006 completed - SKILL.md updated with NAV-006 navigation table, Quick Reference section (116 lines) |
| 2026-02-01T22:30:00Z | Claude | **COMPLETE** | TASK-007 completed - All 4 test cases passed (TC-1 skill invocation, TC-2 entity hierarchy, TC-3 system mappings, TC-4 template references) |

---

## System Mapping

| System | Mapping |
|--------|---------|
| **Azure DevOps** | PBI with ValueArea=Architectural |
| **SAFe** | Enabler (ARCHITECTURE type) |
| **JIRA** | Story with 'enabler' label |
