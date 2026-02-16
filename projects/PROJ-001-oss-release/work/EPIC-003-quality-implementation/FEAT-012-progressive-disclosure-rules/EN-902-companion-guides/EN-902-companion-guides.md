# EN-902: Companion Guide Files

<!--
TEMPLATE: Enabler
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.9
-->

> **Type:** enabler
> **Status:** pending
> **Priority:** high
> **Impact:** high
> **Enabler Type:** infrastructure
> **Created:** 2026-02-16
> **Parent:** FEAT-012
> **Effort:** 8

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

Restore deleted content from git history (pre-EN-702 optimization) and create focused companion guide files in `.context/guides/`. Each guide provides rich context (explanations, rationale, decision trees, examples) for a specific topic. All guides have navigation tables per H-23/H-24.

**Technical Scope:**
- Recover original rule file content from git history (~314993a^)
- Create focused companion guide files in `.context/guides/`
- One guide per topic (architecture layers, architecture patterns, coding practices, testing practices, error handling)
- Navigation tables in every guide (H-23/H-24)
- Content restoration plus additive improvements

---

## Problem Statement

The EN-702 optimization deleted explanatory prose, rationale, code examples, and decision trees from rule files. This content served both Claude (few-shot learning, edge case guidance) and humans (understanding why rules exist). The content needs to be restored into on-demand companion files that Claude reads when doing relevant work.

---

## Business Value

Restores the educational layer that makes rules understandable and actionable. Without guides, rules are bare imperatives that Claude follows mechanically without understanding edge cases, and humans cannot learn the reasoning behind constraints.

### Features Unlocked

- On-demand rich context for Claude when working on relevant topics
- Human-readable rationale for every rule and constraint
- Few-shot learning examples for edge cases

---

## Technical Approach

1. **Recover original rule file content from git history** (commit before EN-702, ~314993a^)
2. **Create focused companion guide files in `.context/guides/`**
3. **Use focused file approach** (one guide per topic) rather than monolithic companion files
4. **Ensure every guide has a navigation table** (H-23/H-24)
5. **Add content beyond what was deleted** where gaps exist
6. **Cross-reference guides from enforcement rule files** (EN-901 adds reference sections)

---

## Children (Tasks)

### Task Inventory

| ID | Title | Status | Activity | Agents |
|----|-------|--------|----------|--------|
| TASK-001 | Restore original rule file content from git history | BACKLOG | RESEARCH | -- |
| TASK-002 | Create architecture-layers.md guide | BACKLOG | DEVELOPMENT | -- |
| TASK-003 | Create architecture-patterns.md guide | BACKLOG | DEVELOPMENT | -- |
| TASK-004 | Create coding-practices.md guide | BACKLOG | DEVELOPMENT | -- |
| TASK-005 | Create testing-practices.md guide | BACKLOG | DEVELOPMENT | -- |
| TASK-006 | Create error-handling.md guide | BACKLOG | DEVELOPMENT | -- |
| TASK-007 | Verify all original content exists in guide files | BACKLOG | REVIEW | -- |

### Task Dependencies

TASK-001 must complete first (provides source content). TASK-002 through TASK-006 are parallel (each creates one guide file). TASK-007 depends on all of TASK-002 through TASK-006 (verification requires all guides to exist).

---

## Progress Summary

### Status Overview

```
[                    ] 0% (0/7 tasks)
```

### Progress Metrics

| Metric | Value |
|--------|-------|
| Total Tasks | 7 |
| Completed | 0 |
| In Progress | 0 |
| Pending | 7 |
| Blocked | 0 |
| Completion | 0% |

---

## Acceptance Criteria

### Definition of Done

- [ ] All companion guide files created in `.context/guides/`
- [ ] Navigation tables in every guide (H-23/H-24)
- [ ] Content restored from git history with no regression
- [ ] Every explanation/example from original rules exists in a guide
- [ ] Quality gate passed (>= 0.92)

### Technical Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| TC-1 | `.context/guides/` directory created with >= 5 guide files | [ ] |
| TC-2 | All guides have navigation tables per H-23/H-24 | [ ] |
| TC-3 | git diff comparison confirms all original content present | [ ] |
| TC-4 | No guide file is empty or stub-only | [ ] |
| TC-5 | Guide content exceeds original (additive, not just restoration) | [ ] |

---

## Evidence

### Deliverables

| # | Deliverable | Path | Status |
|---|-------------|------|--------|
| 1 | -- | -- | Pending |

### Verification Checklist

- [ ] All acceptance criteria verified
- [ ] All technical criteria verified
- [ ] Quality gate score >= 0.92
- [ ] Creator-critic-revision cycle completed (minimum 3 iterations)
- [ ] No regressions introduced

---

## Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| R1: Content regression -- some deleted content not recovered | Medium | High | git show comparison for each original file |
| R2: Guides become too large for single reads | Low | Medium | Focused file approach keeps each guide < 5K tokens |

---

## Dependencies

### Depends On

- EN-901 (needs reference sections to link to)

### Enables

- EN-906

---

## Related Items

### Hierarchy

- **Parent Feature:** [FEAT-012: Progressive Disclosure Rules](../FEAT-012-progressive-disclosure-rules.md)

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-16 | Claude | pending | Enabler created under FEAT-012. |
