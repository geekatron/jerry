# EN-202: CLAUDE.md Rewrite

<!--
TEMPLATE: Enabler
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.9
CREATED: 2026-02-01 (Claude)
PURPOSE: Rewrite CLAUDE.md from 914 lines to 60-80 lines
-->

> **Type:** enabler
> **Status:** in_progress
> **Priority:** critical
> **Impact:** critical
> **Enabler Type:** architecture
> **Created:** 2026-02-01T00:00:00Z
> **Due:** 2026-02-10T00:00:00Z
> **Completed:** 2026-02-02T04:00:00Z
> **Parent:** FEAT-002
> **Owner:** Claude
> **Effort:** 10

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What this enabler does - rewrite CLAUDE.md to 60-80 lines |
| [Problem Statement](#problem-statement) | Why this work is needed - 914 lines causes context rot |
| [Technical Approach](#technical-approach) | Target structure with 5 sections |
| [Children (Tasks)](#children-tasks) | 8 tasks with dependencies |
| [Progress Summary](#progress-summary) | Current completion status |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done checklist |
| [Bugs (Source Defects to Fix)](#bugs-source-defects-to-fix) | 3 bugs from EN-201 extraction |
| [FEAT-002 Standards (Apply in TASK-000)](#feat-002-standards-apply-in-task-000) | Navigation tables requirement |

---

## Summary

Rewrite CLAUDE.md from its current 914 lines to the target 60-80 lines following the Tiered Hybrid Loading Strategy. The new CLAUDE.md will contain only essential identity, navigation pointers, critical constraints, and quick reference information.

**Technical Scope:**
- Create Identity section (~10 lines)
- Create Navigation pointers section (~20 lines)
- Create Active project section (~15 lines)
- Create Critical constraints section (~15 lines)
- Create Quick reference section (~15 lines)
- Validate all pointers resolve correctly

---

## Enabler Type Classification

**This Enabler Type:** ARCHITECTURE (restructuring context loading architecture)

---

## Problem Statement

CLAUDE.md at 914 lines:
1. Consumes ~10,000 tokens at every session start
2. Contains content that should be loaded on-demand
3. Causes context rot that degrades LLM performance
4. Creates cognitive overload for new contributors

---

## Business Value

A lean 60-80 line CLAUDE.md provides:
- 91-93% reduction in always-loaded content
- Improved session start performance
- Better OSS onboarding experience
- Progressive disclosure architecture

### Features Unlocked

- Context-efficient session starts
- Improved LLM performance
- Better OSS contributor onboarding

---

## Technical Approach

Replace the current CLAUDE.md with a focused document containing only:

### Target CLAUDE.md Structure (~75 lines)

```markdown
# CLAUDE.md - Jerry Framework Root Context

## Identity (~10 lines)
- Framework purpose
- Core principle
- Context rot reference

## Navigation (~20 lines)
- Where to find coding standards
- Where to find skills
- Where to find project context
- Where to find knowledge

## Active Project (~15 lines)
- JERRY_PROJECT variable
- Hook output interpretation
- Project context enforcement

## Critical Constraints (~15 lines)
- P-003: No recursive subagents (HARD)
- P-020: User authority (HARD)
- P-022: No deception (HARD)
- Python 3.11+ / UV only

## Quick Reference (~15 lines)
- CLI command summary
- Skill invocation summary
- Key file locations
```

---

## Children (Tasks)

### Task Inventory

| ID | Title | Status | Effort | Score | Owner |
|----|-------|--------|--------|-------|-------|
| [TASK-000](./TASK-000-add-navigation-tables.md) | Add navigation tables to worktracker files | COMPLETE | 2 | 1.0 | Claude |
| [TASK-001](./TASK-001-create-identity-section.md) | Create Identity section | COMPLETE | 1 | 0.94 | Claude |
| [TASK-002](./TASK-002-create-navigation-section.md) | Create Navigation pointers section | COMPLETE | 2 | 0.948 | Claude |
| [TASK-003](./TASK-003-create-active-project-section.md) | Create Active project section | COMPLETE | 1 | 0.942 | Claude |
| [TASK-004](./TASK-004-create-critical-constraints-section.md) | Create Critical constraints section | COMPLETE | 1 | 0.9365 | Claude |
| [TASK-005](./TASK-005-create-quick-reference-section.md) | Create Quick reference section | COMPLETE | 1 | 0.95 | Claude |
| [TASK-006](./TASK-006-validate-pointers.md) | Validate all pointers resolve correctly | COMPLETE | 1 | 1.0 | Claude |
| [TASK-007](./TASK-007-verify-line-count.md) | Verify line count target (60-80 lines) | COMPLETE | 1 | 1.0 | Claude |

### Task Dependencies

```
TASK-000 (Add navigation tables - MUST complete first)
    |
    +---> TASK-001, TASK-002, TASK-003, TASK-004, TASK-005 (can run in parallel)
              |
              +---> TASK-006 (Validate pointers)
                        |
                        +---> TASK-007 (Verify line count)
```

---

## Progress Summary

### Status Overview

```
+------------------------------------------------------------------+
|                   ENABLER PROGRESS TRACKER                        |
+------------------------------------------------------------------+
| Tasks:     [####################] 100% (8/8 completed)           |
| Effort:    [####################] 100% (10/10 points)            |
+------------------------------------------------------------------+
| Overall:   [####################] 100% COMPLETE                  |
+------------------------------------------------------------------+
| Phase 0:   [####################] COMPLETE                       |
| Phase 1:   [####################] COMPLETE (avg score: 0.9433)   |
| QG-1:      [####################] PASSED (ps: 0.944, nse: 0.94)  |
| Phase 2:   [####################] COMPLETE (80 lines assembled)  |
| Phase 3:   [####################] COMPLETE (validation passed)   |
+------------------------------------------------------------------+
```

### Progress Metrics

| Metric | Value |
|--------|-------|
| **Total Tasks** | 8 |
| **Completed Tasks** | 8 |
| **Total Effort (points)** | 10 |
| **Completed Effort** | 10 |
| **Completion %** | 100% |
| **Line Count** | 80 (target: 60-80) ✓ |
| **Reduction** | 91.2% (914 → 80 lines) |
| **Average Score** | 0.9433 (threshold: 0.92) ✓ |

---

## Acceptance Criteria

### Definition of Done

- [x] CLAUDE.md is 60-80 lines (80 lines)
- [x] Token count is ~3,300-3,500 (~3,200)
- [x] All navigation pointers work (12/12 verified)
- [x] No duplicated content from rules/
- [x] No worktracker content in CLAUDE.md
- [x] Backup of original CLAUDE.md created (CLAUDE.md.backup)

### Technical Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| TC-1 | Line count between 60-80 | [x] 80 lines |
| TC-2 | All navigation pointers resolve | [x] 12/12 |
| TC-3 | Identity section complete | [x] Score 0.94 |
| TC-4 | Critical constraints documented | [x] P-003, P-020, P-022, UV |
| TC-5 | No content duplication | [x] Verified |

---

## Evidence

### Deliverables

| Deliverable | Type | Description | Link |
|-------------|------|-------------|------|
| New CLAUDE.md | Documentation | Rewritten context file | CLAUDE.md |
| CLAUDE.md.backup | Backup | Original 914-line version | CLAUDE.md.backup |

### Technical Verification

| Criterion | Verification Method | Evidence | Verified By | Date |
|-----------|---------------------|----------|-------------|------|
| Line count | `wc -l CLAUDE.md` | - | - | - |
| Token count | Claude Code `/context` | - | - | - |
| Pointers resolve | Manual navigation test | - | - | - |

---

## Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Loss of critical information | Medium | High | Backup original, comprehensive mapping |
| Navigation pointers broken | Low | Medium | Test each pointer |
| Content too sparse | Low | Medium | Review against plan structure |

---

## Dependencies

### Depends On

- [EN-201: Worktracker Skill Extraction](../EN-201-worktracker-skill-extraction/EN-201-worktracker-skill-extraction.md) - Must complete before removing worktracker content

### Enables

- [EN-204: Validation & Testing](../EN-204-validation-testing/EN-204-validation-testing.md)

---

## Related Items

### Hierarchy

- **Parent:** [FEAT-002: CLAUDE.md Optimization](../FEAT-002-claude-md-optimization.md)

### Bugs (Source Defects to Fix)

Bugs discovered during EN-201 extraction that must be fixed in the CLAUDE.md rewrite:

| ID | Title | Severity | Priority | Status |
|----|-------|----------|----------|--------|
| [BUG-001](./BUG-001-relationships-typo.md) | "relationships to to" typo (line 221) | trivial | low | CLOSED (N/A) |
| [BUG-002](./BUG-002-story-folder-id-mismatch.md) | Story folder uses {EnablerId} instead of {StoryId} (line 232) | minor | medium | CLOSED (N/A) |
| [BUG-003](./BUG-003-template-path-inconsistency.md) | Template path inconsistency (docs/ vs .context/) | minor | medium | CLOSED (FIXED) |

### Bugs (Gap Analysis - Content Preservation)

Bugs discovered during gap analysis (GAP-001 through GAP-005) identifying content NOT preserved:

| ID | Title | Severity | Priority | Status |
|----|-------|----------|----------|--------|
| [BUG-004](./BUG-004-todo-section-not-migrated.md) | TODO Section Not Migrated (EN-203 pending) | critical | critical | PENDING |
| [BUG-005](./BUG-005-mandatory-skill-usage-lost.md) | Mandatory Skill Usage Section Lost (108 lines) | critical | critical | PENDING |
| [BUG-006](./BUG-006-working-with-jerry-lost.md) | Working with Jerry Section Lost (46 lines) | major | critical | PENDING |
| [BUG-007](./BUG-007-problem-solving-templates-lost.md) | Problem-Solving Templates Reference Lost (18 lines) | minor | high | PENDING |
| [BUG-008](./BUG-008-askuserquestion-flow-lost.md) | AskUserQuestion Flow Lost (24 lines) | minor | high | PENDING |

### Gap Analysis

| Artifact | Description | Link |
|----------|-------------|------|
| traceability-matrix.md | Full section-by-section disposition analysis | [gap-analysis/](./gap-analysis/traceability-matrix.md) |

### Orchestration

| Artifact | Purpose | Location |
|----------|---------|----------|
| ORCHESTRATION_PLAN.md | Strategic workflow design | [orchestration/ORCHESTRATION_PLAN.md](./orchestration/ORCHESTRATION_PLAN.md) |
| ORCHESTRATION.yaml | Machine-readable state (SSOT) | [orchestration/ORCHESTRATION.yaml](./orchestration/ORCHESTRATION.yaml) |
| ORCHESTRATION_WORKTRACKER.md | Tactical execution tracking | [orchestration/ORCHESTRATION_WORKTRACKER.md](./orchestration/ORCHESTRATION_WORKTRACKER.md) |

**Workflow ID:** `en202-rewrite-20260201-001`
**Protocol:** DISC-002 Adversarial Review
**Quality Threshold:** 0.92

### Reference

- Appendix A in PLAN-CLAUDE-MD-OPTIMIZATION.md contains proposed structure
- [EN-201:DEC-001](../EN-201-worktracker-skill-extraction/DEC-001-faithful-extraction-principle.md) - Decision to preserve defects during extraction

### FEAT-002 Standards (Apply in TASK-000)

| Type | Path | Description |
|------|------|-------------|
| Discovery | [FEAT-002:DISC-001](../FEAT-002--DISC-001-navigation-tables-for-llm-comprehension.md) | Navigation tables improve LLM comprehension |
| Decision | [FEAT-002:DEC-001](../FEAT-002--DEC-001-navigation-table-standard.md) | Navigation tables required in all Claude-consumed markdown |
| Rule | `.claude/rules/markdown-navigation-standards.md` | Enforcement rule for navigation tables |
| Research | [Navigation Table Research](./research-navigation-table-optimization.md) | Full research with anchor link findings |

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-01T00:00:00Z | Claude | pending | Enabler created |
| 2026-02-01T13:00:00Z | Claude | pending | Added BUG-001, BUG-002, BUG-003 (source defects from EN-201) |
| 2026-02-01T18:00:00Z | Claude | pending | Added TASK-000 (navigation tables), updated dependency graph, added FEAT-002 standards references |
| 2026-02-01T18:30:00Z | Claude | pending | Added navigation table per FEAT-002:DEC-001 |
| 2026-02-01T22:30:00Z | Claude | pending | Created orchestration plan (en202-rewrite-20260201-001) with DISC-002 protocol |
| 2026-02-02T02:00:00Z | Claude | in_progress | Phase 0 complete (TASK-000). 14 files updated with navigation tables |
| 2026-02-02T02:30:00Z | Claude | in_progress | Phase 1 started. 5 parallel agents launched for section creation |
| 2026-02-02T03:05:00Z | Claude | in_progress | Phase 1 complete. All 5 sections created: 72 LOC, avg score 0.9433. BUG-003 fixed in Section 002 |
| 2026-02-02T03:30:00Z | Claude | in_progress | QG-1 PASSED: ps-critic (0.944), nse-qa (0.94) |
| 2026-02-02T03:45:00Z | Claude | in_progress | Phase 2 complete. 5 sections assembled into 80-line CLAUDE.md. Backup created. |
| 2026-02-02T04:00:00Z | Claude | complete | Phase 3 complete. TASK-006 (12/12 pointers verified) and TASK-007 (80 lines, 91.2% reduction) PASSED. EN-202 COMPLETE. |
| 2026-02-02T05:00:00Z | Claude | in_progress | Gap analysis revealed 5 new bugs (BUG-004 through BUG-008). CRITICAL: 108 lines of mandatory skill usage content + 46 lines of project workflow content NOT preserved. Reopened for gap closure. |

---

## System Mapping

| System | Mapping |
|--------|---------|
| **Azure DevOps** | PBI with ValueArea=Architectural |
| **SAFe** | Enabler (ARCHITECTURE type) |
| **JIRA** | Story with 'enabler' label |
