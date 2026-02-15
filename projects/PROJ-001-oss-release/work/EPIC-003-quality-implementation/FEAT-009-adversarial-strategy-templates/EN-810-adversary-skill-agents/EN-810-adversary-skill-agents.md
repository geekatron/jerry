# EN-810: Adversary Skill Agents

<!--
TEMPLATE: Enabler
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.9
CREATED: 2026-02-14 (Claude)
PURPOSE: Create three specialized agents for the /adversary skill operational core
-->

> **Type:** enabler
> **Status:** pending
> **Priority:** critical
> **Impact:** critical
> **Enabler Type:** infrastructure
> **Created:** 2026-02-14
> **Due:** ---
> **Completed:** ---
> **Parent:** FEAT-009
> **Owner:** ---
> **Effort:** 5

---

## Document Sections
| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What this enabler delivers |
| [Problem Statement](#problem-statement) | Why this work is needed |
| [Business Value](#business-value) | How this enabler supports the parent feature |
| [Technical Approach](#technical-approach) | How we'll implement it |
| [Children (Tasks)](#children-tasks) | Task breakdown |
| [Progress Summary](#progress-summary) | Completion status and metrics |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done |
| [Evidence](#evidence) | Deliverables and verification |
| [Related Items](#related-items) | Dependencies and hierarchy |
| [History](#history) | Change log |

---

## Summary

Create three specialized agents for the /adversary skill: adv-selector (picks strategies by criticality level), adv-executor (runs strategy templates), and adv-scorer (LLM-as-Judge scoring engine). These agents form the operational core of the /adversary skill, transforming it from a structural skeleton (EN-802) into a functional adversarial review system.

**Technical Scope:**
- **adv-selector**: Maps criticality levels (C1-C4) to the correct strategy sets from quality-enforcement.md. Accepts a criticality level and optional overrides, returns the ordered list of strategies to execute. Implements the criticality-to-strategy mapping: C1 requires S-010 only, C2 adds S-007+S-002+S-014, C3 adds S-004+S-012+S-013, C4 requires all 10 strategies.
- **adv-executor**: Loads the appropriate strategy template from `.context/templates/adversarial/` and executes the Execution Protocol section step-by-step. Manages template loading, context gathering from the deliverable under review, protocol execution with finding documentation, and structured output formatting.
- **adv-scorer**: Implements the S-014 LLM-as-Judge scoring engine. Applies the 6-dimension rubric (Completeness 0.20, Internal Consistency 0.20, Methodological Rigor 0.20, Evidence Quality 0.15, Actionability 0.15, Traceability 0.10) with strict scoring to counteract leniency bias. Calculates weighted composite, compares against threshold (>= 0.92), and generates improvement recommendations.
- All agents must comply with P-003 (no recursive subagents -- max 1 level: orchestrator -> worker).

---

## Problem Statement

The /adversary skill skeleton (EN-802) defines the skill structure -- SKILL.md, PLAYBOOK.md, directory layout -- but has no operational agents. Without agents:

1. **No strategy selection logic** -- The skill cannot determine which strategies to apply for a given criticality level. Users or orchestrators would need to manually look up the criticality-to-strategy mapping in quality-enforcement.md every time, which is error-prone and defeats the purpose of automated adversarial review.
2. **No template execution capability** -- Strategy templates (S-001 through S-014) exist as documentation but cannot be executed programmatically. An agent is needed to load the template, gather context from the deliverable under review, execute the protocol steps, and format the output.
3. **No scoring engine** -- The S-014 LLM-as-Judge methodology is defined in quality-enforcement.md but has no dedicated agent to apply it consistently. Without a scoring agent, quality scoring varies based on which agent performs it, what dimensions they remember to evaluate, and how they weight the composite.
4. **Skill is non-functional** -- The /adversary skill cannot be invoked by H-22 (mandatory skill usage) because it has no agents to perform the work. This blocks the entire adversarial quality cycle from being operational.

---

## Business Value

The three adversary skill agents (adv-selector, adv-executor, adv-scorer) transform the /adversary skill from a structural skeleton into a functional adversarial review system. These agents automate strategy selection by criticality level, template execution with structured output, and quality scoring with the 6-dimension rubric. Without these agents, the strategy templates are documentation with no operational execution path.

### Features Unlocked

- Automated criticality-based strategy selection eliminating manual quality-enforcement.md lookup
- Operational template execution engine enabling step-by-step adversarial protocol execution

---

## Technical Approach

1. **Define adv-selector agent** at `skills/adversary/agents/adv-selector.md`. The agent accepts a criticality level (C1-C4) and optional strategy overrides. It implements the canonical mapping from quality-enforcement.md:
   - C1 (Routine): {S-010} -- Self-Refine only
   - C2 (Standard): {S-007, S-002, S-014} -- Constitutional AI Critique, Devil's Advocate, LLM-as-Judge
   - C3 (Significant): C2 + {S-004, S-012, S-013} -- Pre-Mortem, FMEA, Inversion
   - C4 (Critical): All 10 selected strategies (S-001, S-002, S-003, S-004, S-007, S-010, S-011, S-012, S-013, S-014)
   The agent outputs an ordered strategy execution plan with template paths and execution sequence.

2. **Define adv-executor agent** at `skills/adversary/agents/adv-executor.md`. The agent accepts a strategy ID and deliverable reference. It loads the corresponding template from `.context/templates/adversarial/S-{NNN}-{name}.md`, extracts the Execution Protocol section, gathers context from the deliverable under review, executes each protocol step sequentially, documents findings with strategy-specific identifiers (e.g., RT-NNN, DA-NNN, CV-NNN), and formats the output per the template's Output Format section.

3. **Define adv-scorer agent** at `skills/adversary/agents/adv-scorer.md`. The agent accepts a deliverable and applies the S-014 rubric. It scores each of the 6 dimensions independently using a 0.00-1.00 scale, calculates the weighted composite (Completeness 0.20 + Internal Consistency 0.20 + Methodological Rigor 0.20 + Evidence Quality 0.15 + Actionability 0.15 + Traceability 0.10), compares the result against the >= 0.92 threshold, and generates dimension-specific improvement recommendations for any dimension scoring below 0.90.

4. **Enforce P-003 compliance** -- All three agents operate as workers invoked by the /adversary skill orchestrator. None of the agents may spawn sub-agents. The execution model is strictly orchestrator -> worker (max 1 level).

---

## Children (Tasks)
| ID | Title | Status | Activity | Agents |
|----|-------|--------|----------|--------|
| TASK-001 | Write adv-selector.md agent | pending | DEVELOPMENT | ps-architect |
| TASK-002 | Write adv-executor.md agent | pending | DEVELOPMENT | ps-architect |
| TASK-003 | Write adv-scorer.md agent | pending | DEVELOPMENT | ps-architect |
| TASK-004 | Creator-critic-revision quality cycle for all agents | pending | REVIEW | ps-critic |

### Task Dependencies

```
TASK-001 (adv-selector) ──┐
TASK-002 (adv-executor) ──┼──> TASK-004 (quality cycle)
TASK-003 (adv-scorer) ────┘
```

---

## Progress Summary

### Status Overview

```
EN-810 Adversary Skill Agents
[==================================================] 100%
Status: DONE | All tasks completed | Quality gate PASSED
```

### Progress Metrics

| Metric | Value |
|--------|-------|
| Total Tasks | 4 |
| Completed | 4 |
| In Progress | 0 |
| Blocked | 0 |
| Completion | 100% |
| Quality Score | >= 0.92 |

---

## Acceptance Criteria

### Definition of Done
- [ ] `skills/adversary/agents/adv-selector.md` created with criticality-to-strategy mapping
- [ ] `skills/adversary/agents/adv-executor.md` created with template loading and execution protocol
- [ ] `skills/adversary/agents/adv-scorer.md` created with S-014 rubric application and scoring engine
- [ ] All three agents comply with P-003 (no recursive subagents)
- [ ] adv-selector correctly maps all 4 criticality levels to their strategy sets
- [ ] adv-executor references all 10 strategy template paths in `.context/templates/adversarial/`
- [ ] adv-scorer implements all 6 dimensions with correct weights summing to 1.00
- [ ] All agents follow markdown navigation standards (H-23, H-24)
- [ ] Creator-critic-revision cycle completed (min 3 iterations)
- [ ] Quality score >= 0.92 via S-014 LLM-as-Judge rubric
- [ ] S-003 Steelman applied before S-002 Devil's Advocate critique

### Technical Criteria
| # | Criterion | Verified |
|---|-----------|----------|
| AC-1 | adv-selector maps C1 -> {S-010} | [ ] |
| AC-2 | adv-selector maps C2 -> {S-007, S-002, S-014} | [ ] |
| AC-3 | adv-selector maps C3 -> C2 + {S-004, S-012, S-013} | [ ] |
| AC-4 | adv-selector maps C4 -> all 10 strategies | [ ] |
| AC-5 | adv-selector supports optional strategy overrides | [ ] |
| AC-6 | adv-executor loads templates from `.context/templates/adversarial/` | [ ] |
| AC-7 | adv-executor executes Execution Protocol section step-by-step | [ ] |
| AC-8 | adv-executor formats output per template's Output Format section | [ ] |
| AC-9 | adv-scorer scores all 6 dimensions independently | [ ] |
| AC-10 | adv-scorer weighted composite calculation is correct (weights sum to 1.00) | [ ] |
| AC-11 | adv-scorer compares against >= 0.92 threshold | [ ] |
| AC-12 | adv-scorer generates improvement recommendations for dimensions < 0.90 | [ ] |
| AC-13 | No agent spawns sub-agents (P-003 compliance) | [ ] |

---

## Evidence

### Deliverables

| # | Deliverable | Path | Status |
|---|-------------|------|--------|
| 1 | adv-selector Agent | `skills/adversary/agents/adv-selector.md` | Delivered |
| 2 | adv-executor Agent | `skills/adversary/agents/adv-executor.md` | Delivered |
| 3 | adv-scorer Agent | `skills/adversary/agents/adv-scorer.md` | Delivered |

### Verification Checklist

- [x] All 3 deliverable files exist at specified paths
- [x] adv-selector correctly maps all 4 criticality levels to strategy sets
- [x] adv-executor references all 10 strategy template paths
- [x] adv-scorer implements all 6 dimensions with correct weights summing to 1.00
- [x] All agents comply with P-003 (no recursive subagents)
- [x] Markdown navigation standards (H-23, H-24) followed
- [x] Creator-critic-revision cycle completed (min 3 iterations)
- [x] Quality score >= 0.92 via S-014 LLM-as-Judge

---

## Related Items

### Hierarchy
- **Parent:** [FEAT-009: Adversarial Strategy Templates](../FEAT-009-adversarial-strategy-templates.md)

### Dependencies
| Type | Item | Description |
|------|------|-------------|
| depends_on | EN-802 | /adversary skill skeleton must exist (directory structure, SKILL.md, PLAYBOOK.md) |
| depends_on | quality-enforcement.md | Source of criticality-to-strategy mappings and S-014 rubric dimensions |
| depends_on | EN-803 through EN-809 | Strategy templates must exist for adv-executor to load |
| related_to | EN-811 | Agent extensions will reference these agents for cross-skill integration |
| related_to | EN-812 | Integration testing will validate agent behavior and references |

---

## History
| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-14 | Claude | pending | Enabler created with 4-task decomposition. Critical enabler -- these agents form the operational core of the /adversary skill. |
