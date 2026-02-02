# FEAT-002: CLAUDE.md Optimization

<!--
TEMPLATE: Feature
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.4
CREATED: 2026-02-01 (Claude)
PURPOSE: Optimize CLAUDE.md from 914 lines to 60-80 lines for OSS release
-->

> **Type:** feature
> **Status:** pending
> **Priority:** critical
> **Impact:** critical
> **Created:** 2026-02-01T00:00:00Z
> **Due:** 2026-02-15T00:00:00Z
> **Completed:** -
> **Parent:** EPIC-001
> **Owner:** -
> **Target Sprint:** Sprint 1

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What this feature delivers - 91-93% reduction in CLAUDE.md size |
| [Benefit Hypothesis](#benefit-hypothesis) | Expected outcomes - improved LLM performance |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done - line count, functionality |
| [MVP Definition](#mvp-definition) | Scope boundaries - what's in vs out |
| [Children (Enablers)](#children-enablers) | Work breakdown - 5 enablers with dependencies |
| [Progress Summary](#progress-summary) | Current completion status |
| [Decomposition Strategy](#decomposition-strategy) | Tiered Hybrid Loading Strategy |
| [Feature-Level Discoveries](#feature-level-discoveries) | DISC-001 navigation tables |
| [Feature-Level Decisions](#feature-level-decisions) | DEC-001 navigation standard |

---

## Summary

Optimize Jerry's CLAUDE.md file from its current **914 lines (~10,000 tokens)** to a target of **60-80 lines (~3,300-3,500 tokens)** - a **91-93% reduction**. This optimization is essential for OSS release readiness, developer onboarding experience, and preventing context rot that degrades LLM performance.

**Value Proposition:**
- Reduces session start context overhead by 65-67%
- Improves OSS onboarding experience (less cognitive load)
- Implements progressive disclosure via tiered loading
- Addresses context rot research findings

---

## Benefit Hypothesis

**We believe that** reducing CLAUDE.md to 60-80 lines with a tiered hybrid loading strategy

**Will result in** improved LLM performance, faster developer onboarding, and better context management

**We will know we have succeeded when:**
- Session start tokens < 5,000 (vs ~10,000 before)
- All skills load correctly on invocation
- New contributor can start contributing within 10 minutes
- Typical workflows remain unchanged

---

## Acceptance Criteria

### Definition of Done

- [ ] CLAUDE.md reduced to 60-80 lines
- [ ] Session start tokens reduced by 65%+
- [ ] Worktracker fully functional via skill
- [ ] All existing workflows unchanged
- [ ] No broken references
- [ ] Documentation updated for contributors
- [ ] All Enablers completed

### Functional Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| AC-1 | CLAUDE.md is 60-80 lines | [ ] |
| AC-2 | Token count is ~3,300-3,500 | [ ] |
| AC-3 | All navigation pointers work | [ ] |
| AC-4 | No duplicated content from rules/ | [ ] |
| AC-5 | /worktracker skill loads all entity information | [ ] |
| AC-6 | No worktracker content remains in CLAUDE.md | [ ] |
| AC-7 | All template references work correctly | [ ] |

### Non-Functional Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| NFC-1 | Context utilization < 50% at session start | [ ] |
| NFC-2 | OSS contributor can understand structure in < 5 minutes | [ ] |

---

## MVP Definition

### In Scope (MVP)

- Worktracker content extraction to skill (371 lines)
- CLAUDE.md rewrite to 60-80 lines
- TODO section migration to worktracker skill
- Basic validation testing
- Essential documentation updates

### Out of Scope (Future)

- Automated token count monitoring
- Context utilization dashboard
- Progressive disclosure analytics
- Platform-specific testing (Linux, Windows)

---

## Children (Enablers)

### Enabler Inventory

| ID | Type | Title | Status | Priority | Effort |
|----|------|-------|--------|----------|--------|
| [EN-201](./EN-201-worktracker-skill-extraction/EN-201-worktracker-skill-extraction.md) | Enabler | Worktracker Skill Extraction | **complete** | critical | 8 |
| [EN-202](./EN-202-claude-md-rewrite/EN-202-claude-md-rewrite.md) | Enabler | CLAUDE.md Rewrite | **complete** | critical | 10 |
| [EN-203](./EN-203-todo-section-migration/EN-203-todo-section-migration.md) | Enabler | TODO Section Migration | **complete** | high | 3 |
| [EN-204](./EN-204-validation-testing/EN-204-validation-testing.md) | Enabler | Validation & Testing | pending | critical | 5 |
| [EN-205](./EN-205-documentation-update/EN-205-documentation-update.md) | Enabler | Documentation Update | pending | medium | 3 |
| [EN-206](./EN-206-context-distribution-strategy/EN-206-context-distribution-strategy.md) | Enabler | Context Distribution Strategy | **in_progress** | critical | 20 |

### Enabler Dependencies

```
EN-201 (Worktracker Extraction) [COMPLETE]
    |
    +---> EN-202 (CLAUDE.md Rewrite) [COMPLETE] ---> EN-204 (Validation)
    |                                                       |
    +---> EN-203 (TODO Migration) [COMPLETE] ---------------+
    |                                                       |
    +---> EN-206 (Context Distribution) [IN PROGRESS - 15%]
              |                                             |
              +---> SPIKE-001 (Research) [COMPLETE] --------+---> EN-205 (Documentation)
              +---> TASK-001 (Restructure) [PENDING]
              +---> TASK-002 (Sync Mechanism) [PENDING]
              +---> TASK-003 (Bootstrap Skill) [PENDING]
              +---> TASK-004 (User Docs) [PENDING]
              +---> TASK-005 (Integration Testing) [PENDING]
              +---> TASK-006 (Rollback Docs) [PENDING]
```

### Critical Path

EN-201 -> EN-202 -> EN-204 (Must complete in sequence)

---

## Progress Summary

### Status Overview

```
+------------------------------------------------------------------+
|                   FEATURE PROGRESS TRACKER (VERIFIED 2026-02-02)  |
+------------------------------------------------------------------+
| Enablers:  [##########..........] 50% (3/6 completed)            |
| Tasks:     [##########..........] 51% (20/39 completed)          |
+------------------------------------------------------------------+
| Overall:   [##########..........] 50%                            |
+------------------------------------------------------------------+
| EN-201:    [####################] COMPLETE (verified)            |
| EN-202:    [####################] COMPLETE (verified)            |
| EN-203:    [####################] COMPLETE (verified)            |
| EN-204:    [....................] PENDING                        |
| EN-205:    [....................] PENDING                        |
| EN-206:    [###.................] 15% IN PROGRESS                |
+------------------------------------------------------------------+
```

### Progress Metrics

| Metric | Value |
|--------|-------|
| **Total Enablers** | 6 |
| **Completed Enablers** | 3 (EN-201, EN-202, EN-203) |
| **Total Tasks** | 39 |
| **Completed Tasks** | 20 |
| **Total Effort (points)** | 49 |
| **Completed Effort** | 24 |
| **Completion %** | 50% |

---

## Decomposition Strategy

This Feature implements a **Tiered Hybrid Loading Strategy**:

| Tier | Content | Loading | Lines |
|------|---------|---------|-------|
| Tier 1 | CLAUDE.md root | Always loaded | ~60-80 |
| Tier 2 | `.claude/rules/` | Auto-loaded by Claude Code | ~500 |
| Tier 3 | Skills | On-demand via `/skill` | ~1,500+ |
| Tier 4 | Reference docs | Explicit file access | unlimited |

### Current vs Target

| Metric | Current | Target | Improvement |
|--------|---------|--------|-------------|
| CLAUDE.md Lines | 914 | 60-80 | 91-93% reduction |
| Token Footprint | ~10,000 | ~3,300-3,500 | 65-67% reduction |
| Session Start Load | All content | Tier 1 only | Progressive disclosure |
| Worktracker Lines | 371 (inline) | 0 (skill) | 100% extraction |

---

## Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Loss of critical information during extraction | Medium | High | Comprehensive mapping, backup original, test workflows |
| Users forget to invoke skills | Low | Medium | Clear documentation, auto-suggest based on context |
| Rules loading inconsistency | Low | High | Test on multiple platforms, fallback with @ imports |
| Contributor confusion | Medium | Medium | CLAUDE-MD-GUIDE.md, "How to Find Information" section |
| Backward compatibility issues | Low | High | Version changes, migration notes, semantic versioning |

---

## Related Items

### Hierarchy

- **Parent Epic:** [EPIC-001: Jerry OSS Release](../EPIC-001-oss-release.md)

### Related Features

- [FEAT-001: Research and Preparation](../FEAT-001-research-and-preparation/FEAT-001-research-and-preparation.md) - Provides research foundation

### Source Plan

- [PLAN-CLAUDE-MD-OPTIMIZATION.md](../FEAT-001-research-and-preparation/orchestration/oss-release-20260131-001/plans/PLAN-CLAUDE-MD-OPTIMIZATION.md)

### Related ADRs

- ADR-OSS-001: Decomposition Strategy
- ADR-OSS-003: Worktracker Extraction
- ADR-OSS-004: Multi-Persona Documentation

### Feature-Level Discoveries

| ID | Title | Status | Impact |
|----|-------|--------|--------|
| [FEAT-002:DISC-001](./FEAT-002--DISC-001-navigation-tables-for-llm-comprehension.md) | Navigation Tables Improve LLM Document Comprehension | VALIDATED | High |

### Feature-Level Decisions

| ID | Title | Status |
|----|-------|--------|
| [FEAT-002:DEC-001](./FEAT-002--DEC-001-navigation-table-standard.md) | Navigation Tables Required in Claude-Consumed Markdown | ACCEPTED |

### Rules Created

| Rule | Location | Description |
|------|----------|-------------|
| Navigation Standards | `.claude/rules/markdown-navigation-standards.md` | Mandates navigation tables for all Claude-consumed markdown |

### Verification Reports

| Report | Date | Summary |
|--------|------|---------|
| [Acceptance Criteria Verification](./acceptance-criteria-verification.md) | 2026-02-02 | Backward verification of all enablers. EN-203 confirmed complete. 3/6 enablers verified. |

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-01T00:00:00Z | Claude | pending | Feature created from PLAN-CLAUDE-MD-OPTIMIZATION.md |
| 2026-02-01T13:00:00Z | Claude | pending | Created EN-201 through EN-205 enablers |
| 2026-02-01T18:00:00Z | Claude | pending | Added FEAT-002:DISC-001, FEAT-002:DEC-001, navigation standards rule |
| 2026-02-01T18:15:00Z | Claude | pending | Added EN-202:TASK-000 for navigation table updates |
| 2026-02-01T18:30:00Z | Claude | pending | Added navigation table per FEAT-002:DEC-001 |
| 2026-02-02T10:00:00Z | Verification Agent | in_progress | Acceptance Criteria Verification completed. EN-203 verified as COMPLETE (work done during EN-202 gap closure). Updated progress: 3/6 enablers complete (50%). |

---

## System Mapping

| System | Mapping |
|--------|---------|
| **Azure DevOps** | Feature |
| **SAFe** | Feature (Program Backlog) |
| **JIRA** | Epic (or custom issue type) |
