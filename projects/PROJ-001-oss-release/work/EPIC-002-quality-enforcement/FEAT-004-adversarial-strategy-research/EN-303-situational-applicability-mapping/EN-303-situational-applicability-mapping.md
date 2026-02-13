# EN-303: Situational Applicability Mapping

<!--
TEMPLATE: Enabler
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.9
CREATED: 2026-02-12 (Claude)
PURPOSE: Map each selected adversarial strategy to specific contexts with use/avoid guidance and a decision tree
-->

> **Type:** enabler
> **Status:** pending
> **Priority:** high
> **Impact:** high
> **Enabler Type:** architecture
> **Created:** 2026-02-12
> **Due:** —
> **Completed:** —
> **Parent:** FEAT-004
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

Map each of the 10 selected adversarial strategies (from EN-302) to specific usage contexts within Jerry. For each strategy, define: when to use it, when to avoid it, complementary strategy pairings, preconditions that must hold, and expected outcomes. The deliverable includes per-strategy applicability profiles and a strategy selection decision tree that guides agents and users to the right strategy for a given situation. This mapping transforms abstract strategy knowledge into actionable, context-aware guidance that can be directly consumed by Jerry's agent architecture.

## Problem Statement

Knowing which 10 strategies to support is necessary but insufficient. Without situational guidance, agents and users face a paradox of choice: given a review task, which adversarial strategy should be applied? The wrong choice wastes effort (e.g., applying Red Team to a well-established design that needs refinement, not fundamental challenge) or misses critical issues (e.g., applying Blue Team when foundational assumptions need challenging). Furthermore, some strategies are complementary (Red Team followed by Blue Team) while others are redundant or counterproductive when combined. A formal applicability mapping with a decision tree eliminates guesswork and enables automated or semi-automated strategy selection.

## Technical Approach

1. **Context Taxonomy** -- Define the dimensions that determine strategy applicability: review target type (code, architecture, requirements, research), review phase (early exploration, design, implementation, validation), risk level (critical, high, medium, low), artifact maturity (draft, reviewed, approved), and team composition (single agent, multi-agent, human-in-loop).
2. **Requirements Engineering** -- Define formal requirements for what the situational mapping must cover, ensuring completeness and traceability back to FEAT-004 objectives.
3. **Per-Strategy Mapping** -- For each of the 10 selected strategies, create an applicability profile: recommended contexts (when to use), contraindicated contexts (when to avoid), complementary pairings (strategies that work well together), preconditions (what must be true before applying), and expected outcomes (what the strategy produces).
4. **Decision Tree Construction** -- Build a decision tree that takes context inputs (target type, phase, risk level, maturity) and recommends one or more strategies. The tree must handle multi-strategy recommendations and fallback paths.
5. **Adversarial Review** -- Apply Blue Team strategy to stress-test the decision tree for gaps, ambiguities, and edge cases.

## Children (Tasks)

| ID | Title | Status | Activity | Agents |
|----|-------|--------|----------|--------|
| TASK-001 | Define applicability dimensions and context taxonomy | pending | DESIGN | ps-architect |
| TASK-002 | Define requirements for situational mapping | pending | DESIGN | nse-requirements |
| TASK-003 | Map each strategy to contexts with use/avoid guidance | pending | DESIGN | ps-architect |
| TASK-004 | Create strategy selection decision tree | pending | DESIGN | ps-architect |
| TASK-005 | Adversarial review (Blue Team) | pending | TESTING | ps-critic |
| TASK-006 | Creator revision and final validation | pending | DEVELOPMENT | ps-architect, ps-validator |

### Task Dependencies

```
TASK-001 ──┐
            ├──> TASK-003 ──> TASK-004 ──> TASK-005 ──> TASK-006
TASK-002 ──┘
```

## Acceptance Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| 1 | Context taxonomy defines at least 4 applicability dimensions | [ ] |
| 2 | All 10 selected strategies have complete applicability profiles | [ ] |
| 3 | Each profile includes: when to use, when to avoid, pairings, preconditions, outcomes | [ ] |
| 4 | Strategy selection decision tree is complete and covers all context combinations | [ ] |
| 5 | Decision tree handles multi-strategy recommendations | [ ] |
| 6 | Decision tree has fallback paths for ambiguous contexts | [ ] |
| 7 | Blue Team adversarial review completed with documented feedback | [ ] |
| 8 | Requirements traceability to FEAT-004 objectives confirmed | [ ] |
| 9 | Final validation confirms all criteria met | [ ] |

## Agent Assignments

| Agent | Skill | Role | Phase |
|-------|-------|------|-------|
| ps-architect | /problem-solving | Creator -- taxonomy, mapping, decision tree, revision | TASK-001, TASK-003, TASK-004, TASK-006 |
| ps-critic | /problem-solving | Adversarial -- Blue Team review of decision tree | TASK-005 |
| nse-requirements | /nasa-se | Requirements engineering -- formal requirements definition | TASK-002 |
| ps-validator | /problem-solving | Validation -- final quality gate | TASK-006 |

## Related Items

### Hierarchy
- **Parent Feature:** [FEAT-004](../FEAT-004-adversarial-strategy-research.md)

### Dependencies
| Type | Item | Description |
|------|------|-------------|
| depends_on | EN-302 | Requires the selected 10 strategies as input |
| blocks | EN-304 | Skill enhancement depends on situational mapping and decision tree |

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-12 | Claude | pending | Enabler created with task decomposition. Depends on EN-302 strategy selection. |
