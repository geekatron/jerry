# EN-404: Rule-Based Enforcement Enhancement

<!--
TEMPLATE: Enabler
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.9
CREATED: 2026-02-12 (Claude)
PURPOSE: Enhance .claude/rules/ files with HARD enforcement language and tiered enforcement strategy
-->

> **Type:** enabler
> **Status:** pending
> **Priority:** high
> **Impact:** high
> **Enabler Type:** infrastructure
> **Created:** 2026-02-12
> **Due:** —
> **Completed:** —
> **Parent:** FEAT-005
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
| [Agent Assignments](#agent-assignments) | Which agents are used |
| [Related Items](#related-items) | Dependencies |
| [History](#history) | Change log |

---

## Summary

Enhance .claude/rules/ files with HARD enforcement language that prevents Claude from bypassing quality framework. Implement tiered enforcement based on task complexity. Add explicit quality gate requirements to rule files.

## Problem Statement

Current .claude/rules/ files provide guidance but lack HARD enforcement language that prevents Claude from bypassing quality requirements. Without explicit enforcement tiers and quality gate requirements embedded in rule files, Claude may skip mandatory quality steps during complex tasks. The rules need to distinguish between simple tasks (where lightweight enforcement suffices) and complex tasks (where full quality framework engagement is mandatory).

## Technical Approach

1. Audit existing .claude/rules/ files to identify enforcement gaps where Claude could bypass quality requirements.
2. Define a tiered enforcement strategy that distinguishes simple vs complex tasks.
3. Design HARD enforcement language patterns that are unambiguous and non-overridable.
4. Enhance mandatory-skill-usage.md with stronger enforcement directives.
5. Enhance project-workflow.md with quality gate checkpoints.
6. Create a new quality-enforcement.md rule file that codifies the enforcement framework.
7. Subject all changes to adversarial review (Red Team + Strawman) to identify bypass vectors.
8. Revise based on adversarial findings and verify against requirements.

## Children (Tasks)

| ID | Title | Status | Activity | Agents |
|----|-------|--------|----------|--------|
| TASK-001 | Define requirements for rule-based enforcement | pending | DESIGN | nse-requirements |
| TASK-002 | Audit existing .claude/rules/ files for enforcement gaps | pending | RESEARCH | ps-investigator |
| TASK-003 | Design tiered enforcement strategy (simple vs complex tasks) | pending | DESIGN | ps-architect |
| TASK-004 | Design HARD enforcement language patterns | pending | DESIGN | ps-architect |
| TASK-005 | Implement enhanced mandatory-skill-usage.md | pending | DEVELOPMENT | ps-architect |
| TASK-006 | Implement enhanced project-workflow.md | pending | DEVELOPMENT | ps-architect |
| TASK-007 | Create new quality-enforcement.md rule file | pending | DEVELOPMENT | ps-architect |
| TASK-008 | Adversarial review (ps-critic with Red Team + Strawman) | pending | TESTING | ps-critic |
| TASK-009 | Creator revision | pending | DEVELOPMENT | ps-architect |
| TASK-010 | Verification against requirements | pending | TESTING | nse-verification |

### Task Dependencies

```
TASK-001 ──► TASK-002 ──► TASK-003 ──► TASK-004
                                          │
                                          ▼
                              ┌─── TASK-005
                              ├─── TASK-006
                              └─── TASK-007
                                      │
                                      ▼
                                  TASK-008 ──► TASK-009 ──► TASK-010
```

## Acceptance Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| 1 | All .claude/rules/ files audited for enforcement gaps with findings documented | [ ] |
| 2 | Tiered enforcement strategy defined (simple vs complex task thresholds) | [ ] |
| 3 | HARD enforcement language patterns documented and applied consistently | [ ] |
| 4 | mandatory-skill-usage.md enhanced with enforcement directives | [ ] |
| 5 | project-workflow.md enhanced with quality gate checkpoints | [ ] |
| 6 | New quality-enforcement.md rule file created and integrated | [ ] |
| 7 | Adversarial review completed with no unmitigated bypass vectors | [ ] |
| 8 | All changes verified against defined requirements | [ ] |

## Agent Assignments

| Agent | Skill | Role | Phase |
|-------|-------|------|-------|
| ps-architect | problem-solving | Creator - designs and implements enforcement enhancements | DESIGN, DEVELOPMENT |
| ps-critic | problem-solving | Adversarial reviewer - Red Team + Strawman analysis | TESTING |
| ps-investigator | problem-solving | Gap auditor - audits existing rules for enforcement weaknesses | RESEARCH |
| nse-requirements | nasa-se | Requirements engineer - defines enforcement requirements | DESIGN |
| nse-verification | nasa-se | Verification engineer - validates against requirements | TESTING |

## Related Items

### Hierarchy
- **Parent Feature:** [FEAT-005](../FEAT-005-enforcement-mechanisms.md)

### Dependencies
| Type | Item | Description |
|------|------|-------------|
| depends_on | EN-402 | Enforcement priority analysis must be completed to inform rule enhancement strategy |

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-12 | Claude | pending | Enabler created with task decomposition. |
