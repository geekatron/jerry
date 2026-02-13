# EN-307: /orchestration Skill Enhancement (Adversarial Loops)

<!--
TEMPLATE: Enabler
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.9
CREATED: 2026-02-12 (Claude)
PURPOSE: Update /orchestration skill to automatically embed adversarial feedback loops in workflow plans
-->

> **Type:** enabler
> **Status:** pending
> **Priority:** critical
> **Impact:** critical
> **Enabler Type:** architecture
> **Created:** 2026-02-12
> **Due:** —
> **Completed:** —
> **Parent:** FEAT-004
> **Owner:** —
> **Effort:** 8

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

Update the /orchestration skill to automatically bake in adversarial feedback loops. The orch-planner should automatically generate creator->critic->revision cycles when creating orchestration plans. Update SKILL.md, PLAYBOOK.md, agent specs, and templates to embed adversarial review as a default workflow pattern rather than requiring user prompting. This makes adversarial quality enforcement a structural guarantee of every orchestrated workflow, not an optional add-on.

## Problem Statement

Currently, adversarial review in orchestrated workflows only happens when a user explicitly requests it. This means most workflows skip adversarial feedback entirely, producing deliverables that have not been stress-tested for hidden assumptions, logical flaws, or missed risks. The /orchestration skill is the natural enforcement point because it controls workflow structure -- if orch-planner automatically embeds creator->critic->revision cycles into every plan, adversarial quality becomes a default rather than an exception. Without this, the adversarial strategies researched in EN-301 and mapped in EN-303 remain theoretical rather than operationally embedded.

## Technical Approach

1. **Requirements Definition** -- Define what the orchestration skill enhancement needs to deliver, including automatic adversarial cycle generation, quality score tracking, and adversarial synthesis.
2. **Planner Design** -- Design how orch-planner will automatically detect which phases need adversarial cycles and inject creator->critic->revision patterns into generated plans.
3. **Quality Gate Design** -- Design how orch-tracker will track adversarial quality scores and enforce quality gates at sync barriers.
4. **Agent Spec Updates** -- Update orch-planner, orch-tracker, and orch-synthesizer agent specs with adversarial capabilities.
5. **Skill Documentation** -- Update orchestration SKILL.md and PLAYBOOK.md with adversarial patterns and workflows.
6. **Template Updates** -- Update orchestration templates (ORCHESTRATION_PLAN.md, ORCHESTRATION.yaml, ORCHESTRATION_WORKTRACKER.md) to include adversarial sections by default.
7. **Multi-Layer Review** -- Code review, adversarial review (Red Team + Blue Team), technical review, and final validation.

## Children (Tasks)

| ID | Title | Status | Activity | Agents |
|----|-------|--------|----------|--------|
| TASK-001 | Define requirements for orchestration skill enhancement | pending | DESIGN | nse-requirements |
| TASK-002 | Design adversarial loop integration for orch-planner | pending | DESIGN | ps-architect |
| TASK-003 | Design quality gate integration for orch-tracker | pending | DESIGN | ps-architect |
| TASK-004 | Update orch-planner agent spec to auto-embed adversarial cycles | pending | DEVELOPMENT | ps-architect |
| TASK-005 | Update orch-tracker agent spec for quality score tracking | pending | DEVELOPMENT | ps-architect |
| TASK-006 | Update orch-synthesizer to include adversarial synthesis | pending | DEVELOPMENT | ps-architect |
| TASK-007 | Update orchestration SKILL.md with adversarial patterns | pending | DOCUMENTATION | ps-architect |
| TASK-008 | Update orchestration PLAYBOOK.md with adversarial workflows | pending | DOCUMENTATION | ps-architect |
| TASK-009 | Update orchestration templates to include adversarial sections | pending | DEVELOPMENT | ps-architect |
| TASK-010 | Code review of all modifications | pending | TESTING | ps-reviewer |
| TASK-011 | Adversarial review (ps-critic with Red Team + Blue Team) | pending | TESTING | ps-critic |
| TASK-012 | Technical review of orchestration changes | pending | TESTING | nse-reviewer |
| TASK-013 | Final validation | pending | TESTING | ps-validator |

### Task Dependencies

```
TASK-001 (requirements)
  |
  +---> TASK-002 (design orch-planner adversarial loops)
  |       |
  +---> TASK-003 (design orch-tracker quality gates)
          |
          +---> TASK-004 (implement orch-planner spec)
          |
          +---> TASK-005 (implement orch-tracker spec)
          |
          +---> TASK-006 (implement orch-synthesizer spec)
                  |
                  +---> TASK-007 (update SKILL.md)
                  |
                  +---> TASK-008 (update PLAYBOOK.md)
                  |
                  +---> TASK-009 (update templates)
                          |
                          +---> TASK-010 (code review)
                          |
                          +---> TASK-011 (adversarial review)
                          |
                          +---> TASK-012 (technical review)
                                  |
                                  +---> TASK-013 (final validation)
```

## Acceptance Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| 1 | Requirements for orchestration adversarial enhancement are defined and reviewed | [ ] |
| 2 | orch-planner automatically generates creator->critic->revision cycles in plans | [ ] |
| 3 | orch-tracker tracks adversarial quality scores at sync barriers | [ ] |
| 4 | orch-synthesizer includes adversarial synthesis in final outputs | [ ] |
| 5 | Orchestration SKILL.md documents adversarial loop patterns | [ ] |
| 6 | Orchestration PLAYBOOK.md includes adversarial workflow guidance | [ ] |
| 7 | Orchestration templates include adversarial sections by default | [ ] |
| 8 | Code review passes with no critical findings | [ ] |
| 9 | Adversarial review (Red Team + Blue Team) passes with no critical findings | [ ] |
| 10 | Technical review by nse-reviewer confirms architectural consistency | [ ] |
| 11 | Final validation by ps-validator confirms all criteria met | [ ] |

## Agent Assignments

| Agent | Skill | Role | Phase |
|-------|-------|------|-------|
| ps-architect | /problem-solving | Creator -- designs and implements orchestration enhancements | DESIGN, DEVELOPMENT, DOCUMENTATION |
| ps-critic | /problem-solving | Adversarial -- Red Team + Blue Team review | TESTING |
| orch-planner | /orchestration | Orchestration design -- informs planner enhancement design | DESIGN |
| ps-reviewer | /problem-solving | Code review -- reviews all modifications | TESTING |
| nse-reviewer | /nasa-se | Technical review -- validates SE consistency | TESTING |
| nse-requirements | /nasa-se | Requirements -- defines enhancement requirements | DESIGN |
| ps-validator | /problem-solving | Validation -- final acceptance validation | TESTING |

## Related Items

### Hierarchy
- **Parent Feature:** [FEAT-004](../FEAT-004-adversarial-strategy-research.md)

### Dependencies
| Type | Item | Description |
|------|------|-------------|
| depends_on | EN-303 | Situational Applicability Mapping -- strategy-to-context mappings needed for orchestration loop design |

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-12 | Claude | pending | Enabler created with task decomposition. |
