# EN-304: /problem-solving Skill Enhancement

<!--
TEMPLATE: Enabler
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.9
CREATED: 2026-02-12 (Claude)
PURPOSE: Enhance the /problem-solving skill to integrate adversarial strategies into Jerry's agent architecture
-->

> **Type:** enabler
> **Status:** completed
> **Priority:** critical
> **Impact:** critical
> **Enabler Type:** architecture
> **Created:** 2026-02-12
> **Due:** —
> **Completed:** 2026-02-16
> **Parent:** FEAT-004
> **Owner:** —
> **Effort:** 10

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

Enhance the /problem-solving skill to integrate the 10 selected adversarial strategies into Jerry's agent architecture. This enabler covers: updating the ps-critic agent specification with adversarial mode definitions (one mode per strategy), defining the invocation protocol for selecting and applying strategies, updating SKILL.md with adversarial capabilities documentation, updating PLAYBOOK.md with adversarial workflow procedures, and creating any necessary agent extension definitions. The result is a fully operational adversarial review capability within Jerry's existing skill and agent framework, ready for use in all problem-solving workflows.

## Problem Statement

The research, selection, and mapping from EN-301 through EN-303 produce knowledge artifacts but do not change Jerry's operational capability. Without concrete modifications to the /problem-solving skill, the adversarial strategies remain theoretical. The ps-critic agent currently operates with a single undifferentiated review mode. To leverage the 10 selected strategies, the agent must support multiple adversarial modes, each with distinct prompting patterns, evaluation criteria, and output formats. The invocation protocol must enable both explicit strategy selection (user or orchestrator chooses a strategy) and automatic selection (using the EN-303 decision tree). All changes must be backward-compatible with existing /problem-solving workflows and documented in the skill's SKILL.md and PLAYBOOK.md files.

## Technical Approach

1. **Requirements Definition** -- Formalize requirements for the skill enhancement: what capabilities must the enhanced ps-critic support, what backward compatibility constraints exist, what the invocation protocol must handle, and what documentation updates are needed.
2. **Adversarial Mode Design** -- Design the adversarial mode architecture for ps-critic: each of the 10 strategies becomes a named mode with its own prompt template, evaluation criteria, output format, and applicability metadata (from EN-303). Define mode switching, composition (multiple modes in sequence), and fallback behavior.
3. **Invocation Protocol Design** -- Design the protocol for requesting adversarial review: explicit mode selection (e.g., `ps-critic --mode red-team`), automatic mode selection (context-based using EN-303 decision tree), multi-mode pipelines (e.g., Red Team then Blue Team), and integration with /orchestration for multi-phase adversarial workflows.
4. **Implementation** -- Update the ps-critic agent specification with mode definitions, prompt templates, and configuration. This is specification-level work (markdown agent definitions), not Python code changes.
5. **Documentation** -- Update SKILL.md to document adversarial capabilities, available modes, and usage examples. Update PLAYBOOK.md to include adversarial workflow procedures (when to invoke, how to interpret results, how to iterate).
6. **Review and Validation** -- Code review of all modifications, adversarial review using Red Team + Blue Team on the changes themselves, verification against requirements from step 1, and final validation.

## Children (Tasks)

| ID | Title | Status | Activity | Agents |
|----|-------|--------|----------|--------|
| TASK-001 | Define requirements for PS skill enhancements | pending | DESIGN | nse-requirements |
| TASK-002 | Design adversarial mode integration for ps-critic | pending | DESIGN | ps-architect |
| TASK-003 | Design invocation protocol for adversarial strategies | pending | DESIGN | ps-architect |
| TASK-004 | Implement ps-critic agent spec updates | pending | DEVELOPMENT | ps-architect |
| TASK-005 | Update SKILL.md with adversarial capabilities | pending | DOCUMENTATION | ps-architect |
| TASK-006 | Update PLAYBOOK.md with adversarial workflows | pending | DOCUMENTATION | ps-architect |
| TASK-007 | Code review of all modifications | pending | TESTING | ps-reviewer |
| TASK-008 | Adversarial review (Red Team + Blue Team) | pending | TESTING | ps-critic |
| TASK-009 | Verification against requirements | pending | TESTING | nse-verification |
| TASK-010 | Final validation | pending | TESTING | ps-validator |

### Task Dependencies

```
TASK-001 ──> TASK-002 ──> TASK-003 ──> TASK-004 ──┐
                                                    ├──> TASK-007 ──> TASK-008 ──> TASK-009 ──> TASK-010
                                       TASK-005 ──┤
                                       TASK-006 ──┘
```

## Acceptance Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| 1 | Requirements document defines all enhancement capabilities | [ ] |
| 2 | ps-critic agent spec supports all 10 adversarial modes | [ ] |
| 3 | Each mode has: name, prompt template, evaluation criteria, output format | [ ] |
| 4 | Invocation protocol supports explicit mode selection | [ ] |
| 5 | Invocation protocol supports automatic mode selection via decision tree | [ ] |
| 6 | Invocation protocol supports multi-mode pipelines | [ ] |
| 7 | SKILL.md documents all adversarial capabilities with usage examples | [ ] |
| 8 | PLAYBOOK.md includes adversarial workflow procedures | [ ] |
| 9 | All changes are backward-compatible with existing PS workflows | [ ] |
| 10 | Code review completed with no blocking issues | [ ] |
| 11 | Adversarial review (Red Team + Blue Team) completed | [ ] |
| 12 | Requirements verification confirms all requirements met | [ ] |
| 13 | Final validation confirms all criteria met | [ ] |

## Agent Assignments

| Agent | Skill | Role | Phase |
|-------|-------|------|-------|
| ps-architect | /problem-solving | Creator -- mode design, protocol design, implementation, documentation | TASK-002, TASK-003, TASK-004, TASK-005, TASK-006 |
| ps-critic | /problem-solving | Adversarial -- Red Team + Blue Team review of changes | TASK-008 |
| ps-reviewer | /problem-solving | Code review -- review all spec modifications | TASK-007 |
| nse-requirements | /nasa-se | Requirements engineering -- formal requirements definition | TASK-001 |
| nse-verification | /nasa-se | Verification & validation -- requirements traceability check | TASK-009 |
| ps-validator | /problem-solving | Validation -- final quality gate | TASK-010 |

## Related Items

### Hierarchy
- **Parent Feature:** [FEAT-004](../FEAT-004-adversarial-strategy-research.md)

### Dependencies
| Type | Item | Description |
|------|------|-------------|
| depends_on | EN-303 | Requires situational mapping and decision tree for automatic mode selection |
| depends_on | EN-302 | Requires the selected 10 strategies for mode definitions |
| depends_on | EN-301 | Requires strategy descriptions for prompt template authoring |

## Evidence

### Superseded By

This enabler was superseded by EPIC-003 FEAT-008 **EN-707** (PS Skill Adversarial Mode Enhancement). EN-707 added adversarial review sections to the ps-critic and ps-reviewer agent specifications, implementing the adversarial mode integration that EN-304 planned. The work was completed through the EPIC-003 quality framework implementation rather than through the FEAT-004 pipeline.

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-12 | Claude | pending | Enabler created with task decomposition. Terminal enabler in FEAT-004 pipeline. |
| 2026-02-16 | Claude | completed | Superseded by EPIC-003. EN-707 (PS Skill Adversarial Mode Enhancement). See Evidence section. |
