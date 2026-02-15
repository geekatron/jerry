# EN-813: Template Context Optimization

<!--
TEMPLATE: Enabler
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.9
CREATED: 2026-02-15 (Claude)
PURPOSE: Reduce context consumption during strategy execution via lazy loading
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
> **Effort:** 5

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

Implement section-boundary parsing in adv-executor to load only the Execution Protocol section during strategy execution, reducing context consumption to <= 10,000 tokens for C4 tournaments. Currently, full template loading causes excessive context consumption.

---

## Problem Statement

Full template loading during strategy execution wastes context budget. A C4 tournament using all 10 strategies loads ~50K+ tokens of template content when only the Execution Protocol sections (~10K total) are needed for actual execution.

---

## Technical Approach

1. Implement section-boundary parsing in adv-executor to identify Execution Protocol boundaries via markdown heading detection
2. Update adv-executor.md to use lazy loading — only Execution Protocol section loaded during execution, other sections loaded on-demand
3. Measure and validate context consumption <= 10,000 tokens for C4 tournament
4. Update PLAYBOOK.md with lazy loading operational guidance

---

## Children (Tasks)

| ID | Title | Status | Activity | Agents |
|----|-------|--------|----------|--------|
| TASK-001 | Implement section-boundary parsing in adv-executor | pending | DEVELOPMENT | ps-architect |
| TASK-002 | Update adv-executor.md to load only Execution Protocol section | pending | DEVELOPMENT | ps-architect |
| TASK-003 | Measure and validate context consumption <= 10,000 tokens | pending | REVIEW | ps-critic |
| TASK-004 | Update PLAYBOOK.md with lazy loading operational guidance | pending | DEVELOPMENT | ps-architect |

---

## Acceptance Criteria

### Definition of Done

- [ ] Section-boundary parsing implemented in adv-executor
- [ ] adv-executor.md updated with lazy loading specification
- [ ] Context consumption measured and validated <= 10,000 tokens for C4 tournament
- [ ] PLAYBOOK.md updated with lazy loading operational guidance
- [ ] All task acceptance criteria met
- [ ] Quality gate passed (>= 0.92)

### Technical Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| 1 | Section parser correctly identifies Execution Protocol boundaries in all 10 templates | ☐ |
| 2 | Parser handles edge cases (missing section, empty section) | ☐ |
| 3 | adv-executor spec updated with lazy loading instructions | ☐ |
| 4 | Backward compatible with existing invocation patterns | ☐ |
| 5 | Context consumption <= 10,000 tokens for C4 tournament | ☐ |
| 6 | Before/after measurement comparison documented | ☐ |
| 7 | PLAYBOOK.md includes lazy loading operational guidance | ☐ |

---

## Related Items

### Hierarchy
- **Parent Feature:** [FEAT-010: Tournament Remediation](../FEAT-010-tournament-remediation.md)

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-15 | Claude | pending | Enabler created from FEAT-009 C4 Tournament findings. |
