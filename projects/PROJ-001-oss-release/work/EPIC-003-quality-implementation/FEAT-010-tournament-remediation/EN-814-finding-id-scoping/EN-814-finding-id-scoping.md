# EN-814: Finding ID Scoping & Uniqueness

<!--
TEMPLATE: Enabler
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.9
CREATED: 2026-02-15 (Claude)
PURPOSE: Prevent finding ID collisions across multi-strategy tournaments
-->

> **Type:** enabler
> **Status:** pending
> **Priority:** critical
> **Impact:** critical
> **Enabler Type:** infrastructure
> **Created:** 2026-02-15
> **Due:** —
> **Completed:** —
> **Parent:** FEAT-010
> **Owner:** —
> **Effort:** 3

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What this enabler delivers |
| [Problem Statement](#problem-statement) | Why this work is needed |
| [Technical Approach](#technical-approach) | How we'll implement it |
| [Children (Tasks)](#children-tasks) | Task breakdown |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done |
| [Related Items](#related-items) | Dependencies and hierarchy |
| [History](#history) | Change log |

---

## Summary

Add execution-scoped finding ID prefix format to TEMPLATE-FORMAT.md and update all 10 strategy templates to use scoped finding IDs (e.g., FM-001-{execution_id}), preventing finding ID collisions when multiple strategies execute in the same tournament.

---

## Problem Statement

Current templates use simple finding ID formats (e.g., FM-001, DA-001) that collide when multiple strategies execute in the same tournament. The C4 tournament synthesis had to manually deduplicate findings due to ID overlap.

---

## Technical Approach

1. Add execution-scoped finding ID prefix format to TEMPLATE-FORMAT.md (e.g., FM-001-{execution_id})
2. Update all 10 strategy templates with scoped finding ID format in their Output Format sections
3. Add E2E test for finding prefix uniqueness across all templates

---

## Children (Tasks)

| ID | Title | Status | Activity | Agents |
|----|-------|--------|----------|--------|
| TASK-001 | Add execution-scoped finding ID prefix format to TEMPLATE-FORMAT.md | pending | DEVELOPMENT | ps-architect |
| TASK-002 | Update all 10 strategy templates with scoped finding ID format | pending | DEVELOPMENT | ps-architect |
| TASK-003 | Add E2E test for finding prefix uniqueness across all templates | pending | DEVELOPMENT | ps-architect |

---

## Acceptance Criteria

### Definition of Done

- [ ] TEMPLATE-FORMAT.md updated with execution-scoped finding ID format specification
- [ ] All 10 strategy templates updated with scoped finding ID format
- [ ] E2E test validates unique STRATEGY_PREFIX values across all templates
- [ ] All task acceptance criteria met
- [ ] Quality gate passed (>= 0.92)

### Technical Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| 1 | TEMPLATE-FORMAT.md defines execution-scoped finding ID format | ☐ |
| 2 | Format documented with examples | ☐ |
| 3 | All 10 templates updated (S-001, S-002, S-003, S-004, S-007, S-010, S-011, S-012, S-013, S-014) | ☐ |
| 4 | Each template defines unique STRATEGY_PREFIX | ☐ |
| 5 | E2E test validates unique prefixes across all templates | ☐ |
| 6 | E2E test validates finding ID format compliance | ☐ |
| 7 | E2E test passes with `uv run pytest` | ☐ |

---

## Related Items

### Hierarchy
- **Parent Feature:** [FEAT-010: Tournament Remediation](../FEAT-010-tournament-remediation.md)

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-15 | Claude | pending | Enabler created from FEAT-009 C4 Tournament findings. |
