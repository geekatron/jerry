# EN-202: CLAUDE.md Rewrite

<!--
TEMPLATE: Enabler
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.9
CREATED: 2026-02-01 (Claude)
PURPOSE: Rewrite CLAUDE.md from 914 lines to 60-80 lines
-->

> **Type:** enabler
> **Status:** pending
> **Priority:** critical
> **Impact:** critical
> **Enabler Type:** architecture
> **Created:** 2026-02-01T00:00:00Z
> **Due:** 2026-02-10T00:00:00Z
> **Completed:** -
> **Parent:** FEAT-002
> **Owner:** -
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

| ID | Title | Status | Effort | Owner |
|----|-------|--------|--------|-------|
| [TASK-000](./TASK-000-add-navigation-tables.md) | Add navigation tables to worktracker files | pending | 2 | - |
| [TASK-001](./TASK-001-create-identity-section.md) | Create Identity section | pending | 1 | - |
| [TASK-002](./TASK-002-create-navigation-section.md) | Create Navigation pointers section | pending | 2 | - |
| [TASK-003](./TASK-003-create-active-project-section.md) | Create Active project section | pending | 1 | - |
| [TASK-004](./TASK-004-create-critical-constraints-section.md) | Create Critical constraints section | pending | 1 | - |
| [TASK-005](./TASK-005-create-quick-reference-section.md) | Create Quick reference section | pending | 1 | - |
| [TASK-006](./TASK-006-validate-pointers.md) | Validate all pointers resolve correctly | pending | 1 | - |
| [TASK-007](./TASK-007-verify-line-count.md) | Verify line count target (60-80 lines) | pending | 1 | - |

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
| Tasks:     [....................] 0% (0/8 completed)             |
| Effort:    [....................] 0% (0/10 points completed)     |
+------------------------------------------------------------------+
| Overall:   [....................] 0%                             |
+------------------------------------------------------------------+
```

### Progress Metrics

| Metric | Value |
|--------|-------|
| **Total Tasks** | 8 |
| **Completed Tasks** | 0 |
| **Total Effort (points)** | 10 |
| **Completed Effort** | 0 |
| **Completion %** | 0% |

---

## Acceptance Criteria

### Definition of Done

- [ ] CLAUDE.md is 60-80 lines
- [ ] Token count is ~3,300-3,500
- [ ] All navigation pointers work
- [ ] No duplicated content from rules/
- [ ] No worktracker content in CLAUDE.md
- [ ] Backup of original CLAUDE.md created

### Technical Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| TC-1 | Line count between 60-80 | [ ] |
| TC-2 | All navigation pointers resolve | [ ] |
| TC-3 | Identity section complete | [ ] |
| TC-4 | Critical constraints documented | [ ] |
| TC-5 | No content duplication | [ ] |

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

| ID | Title | Severity | Priority |
|----|-------|----------|----------|
| [BUG-001](./BUG-001-relationships-typo.md) | "relationships to to" typo (line 221) | trivial | low |
| [BUG-002](./BUG-002-story-folder-id-mismatch.md) | Story folder uses {EnablerId} instead of {StoryId} (line 232) | minor | medium |
| [BUG-003](./BUG-003-template-path-inconsistency.md) | Template path inconsistency (docs/ vs .context/) | minor | medium |

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

---

## System Mapping

| System | Mapping |
|--------|---------|
| **Azure DevOps** | PBI with ValueArea=Architectural |
| **SAFe** | Enabler (ARCHITECTURE type) |
| **JIRA** | Story with 'enabler' label |
