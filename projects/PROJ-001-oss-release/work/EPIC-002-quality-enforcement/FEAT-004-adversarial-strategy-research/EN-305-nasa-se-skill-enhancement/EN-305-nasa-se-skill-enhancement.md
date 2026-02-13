# EN-305: /nasa-se Skill Enhancement

<!--
TEMPLATE: Enabler
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.9
CREATED: 2026-02-12 (Claude)
PURPOSE: Enhance /nasa-se skill with adversarial strategy integration for SE review gates
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

Enhance the /nasa-se skill to integrate adversarial strategies. Update nse-verification, nse-reviewer, and nse-qa agents with adversarial modes. Map strategies to SE review types (SRR, PDR, CDR, TRR, FRR). Define V&V integration so that adversarial techniques become a first-class part of NASA Systems Engineering review processes within Jerry.

## Problem Statement

The /nasa-se skill currently performs systems engineering reviews (SRR, PDR, CDR, TRR, FRR) without leveraging adversarial strategies. This means reviews may miss critical issues that techniques like Devil's Advocate, Red Team/Blue Team, or Pre-Mortem Analysis would surface. Without adversarial integration, the SE review gates lack the rigor needed to catch subtle design flaws, unstated assumptions, and hidden risks. Each SE review type has different concerns (requirements completeness at SRR, design integrity at PDR/CDR, test coverage at TRR, readiness at FRR) and needs strategies mapped specifically to those concerns.

## Technical Approach

1. **Requirements Definition** -- Define what adversarial capabilities each NSE agent needs, mapped to specific review gates.
2. **Agent Enhancement Design** -- Design adversarial integration for nse-verification (V&V with adversarial challenge) and nse-reviewer (reviews with adversarial critique).
3. **Review Gate Mapping** -- Map the 10 adversarial strategies to the 5 SE review gates (SRR, PDR, CDR, TRR, FRR), identifying which strategies are most effective at each gate.
4. **Implementation** -- Update agent spec files for nse-verification and nse-reviewer with adversarial modes, prompts, and workflows.
5. **Documentation** -- Update the NSE SKILL.md to document adversarial capabilities and usage.
6. **Validation** -- Adversarial review of the modifications themselves, technical review, and final validation.

## Children (Tasks)

| ID | Title | Status | Activity | Agents |
|----|-------|--------|----------|--------|
| TASK-001 | Define requirements for NSE skill enhancements | pending | DESIGN | nse-requirements |
| TASK-002 | Design adversarial integration for nse-verification | pending | DESIGN | nse-architecture |
| TASK-003 | Design adversarial integration for nse-reviewer | pending | DESIGN | nse-architecture |
| TASK-004 | Map strategies to SE review gates (SRR, PDR, CDR, TRR, FRR) | pending | DESIGN | nse-architecture |
| TASK-005 | Implement nse-verification agent spec updates | pending | DEVELOPMENT | nse-architecture |
| TASK-006 | Implement nse-reviewer agent spec updates | pending | DEVELOPMENT | nse-architecture |
| TASK-007 | Update NSE SKILL.md with adversarial capabilities | pending | DOCUMENTATION | nse-architecture |
| TASK-008 | Adversarial review (ps-critic with Devil's Advocate + Steelman) | pending | TESTING | ps-critic |
| TASK-009 | Technical review of modifications (nse-reviewer) | pending | TESTING | nse-reviewer |
| TASK-010 | Final validation (ps-validator) | pending | TESTING | ps-validator |

### Task Dependencies

```
TASK-001 (requirements)
  |
  +---> TASK-002 (design nse-verification)
  |       |
  +---> TASK-003 (design nse-reviewer)
  |       |
  +---> TASK-004 (map to review gates)
          |
          +---> TASK-005 (implement nse-verification)
          |
          +---> TASK-006 (implement nse-reviewer)
          |
          +---> TASK-007 (update SKILL.md)
                  |
                  +---> TASK-008 (adversarial review)
                  |
                  +---> TASK-009 (technical review)
                          |
                          +---> TASK-010 (final validation)
```

## Acceptance Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| 1 | Requirements for NSE adversarial enhancements are defined and reviewed | [ ] |
| 2 | nse-verification agent spec includes adversarial challenge modes | [ ] |
| 3 | nse-reviewer agent spec includes adversarial critique modes | [ ] |
| 4 | All 10 strategies are mapped to appropriate SE review gates (SRR, PDR, CDR, TRR, FRR) | [ ] |
| 5 | NSE SKILL.md documents adversarial capabilities and usage | [ ] |
| 6 | Adversarial review (Devil's Advocate + Steelman) passes with no critical findings | [ ] |
| 7 | Technical review by nse-reviewer confirms architectural consistency | [ ] |
| 8 | Final validation by ps-validator confirms all criteria met | [ ] |

## Agent Assignments

| Agent | Skill | Role | Phase |
|-------|-------|------|-------|
| nse-architecture | /nasa-se | Creator -- designs and implements NSE enhancements | DESIGN, DEVELOPMENT |
| ps-critic | /problem-solving | Adversarial -- Devil's Advocate + Steelman review | TESTING |
| nse-reviewer | /nasa-se | Technical review -- validates SE consistency | TESTING |
| nse-requirements | /nasa-se | Requirements -- defines enhancement requirements | DESIGN |
| nse-verification | /nasa-se | V&V -- verification and validation integration | DEVELOPMENT |
| ps-validator | /problem-solving | Validation -- final acceptance validation | TESTING |

## Related Items

### Hierarchy
- **Parent Feature:** [FEAT-004](../FEAT-004-adversarial-strategy-research.md)

### Dependencies
| Type | Item | Description |
|------|------|-------------|
| depends_on | EN-303 | Situational Applicability Mapping -- strategy-to-context mappings needed for SE review gate mapping |

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-12 | Claude | pending | Enabler created with task decomposition. |
