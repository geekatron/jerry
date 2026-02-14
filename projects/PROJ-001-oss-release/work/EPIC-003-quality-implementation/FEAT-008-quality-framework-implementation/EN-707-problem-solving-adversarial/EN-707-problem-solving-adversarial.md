# EN-707: Problem-Solving Adversarial Mode

<!--
TEMPLATE: Enabler
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.9
CREATED: 2026-02-14 (Claude)
PURPOSE: Enhance /problem-solving skill with adversarial mode integration
-->

> **Type:** enabler
> **Status:** pending
> **Priority:** high
> **Impact:** high
> **Enabler Type:** architecture
> **Created:** 2026-02-14
> **Due:** —
> **Completed:** —
> **Parent:** FEAT-008
> **Owner:** —
> **Effort:** 8

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What this enabler delivers |
| [Problem Statement](#problem-statement) | Why this work is needed |
| [Technical Approach](#technical-approach) | How we'll implement it |
| [Design Source](#design-source) | Traceability to EPIC-002 design artifacts |
| [Children (Tasks)](#children-tasks) | Task breakdown |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done |
| [Related Items](#related-items) | Dependencies and hierarchy |
| [History](#history) | Change log |

---

## Summary

Enhance the `/problem-solving` skill with adversarial mode integration. Update `skills/problem-solving/SKILL.md`, `skills/problem-solving/PLAYBOOK.md`, and relevant agent files to incorporate the 10 selected adversarial strategies, creator-critic-revision cycles, and quality scoring with LLM-as-Judge (S-014).

**Value Proposition:**
- Elevates problem-solving output quality through structured adversarial review
- Integrates creator-critic-revision cycles into research, analysis, and synthesis workflows
- Provides strategy selection guidance tailored to problem-solving domain contexts
- Enforces quality scoring (>= 0.92 threshold) before accepting deliverables
- Aligns PS skill with the quality framework designed in EPIC-002

**Technical Scope:**
- SKILL.md updates with adversarial mode section and strategy catalog reference
- PLAYBOOK.md updates with creator-critic-revision cycle integration
- Agent file updates with strategy-specific guidance per agent role
- Quality scoring integration using LLM-as-Judge (S-014) methodology
- Strategy selection guidance mapping PS contexts to optimal strategies

---

## Problem Statement

The `/problem-solving` skill currently lacks built-in adversarial quality controls. Research, analysis, and synthesis outputs are produced without structured critical review, meaning quality depends entirely on the initial generation. Specific risks:

1. **Confirmation bias** -- Research agents may selectively gather evidence supporting initial hypotheses without adversarial challenge.
2. **Shallow analysis** -- Without critic cycles, analysis may miss edge cases, alternative explanations, or hidden assumptions.
3. **Synthesis gaps** -- Synthesized findings may lack coherence or completeness without adversarial review for logical consistency.
4. **Inconsistent quality** -- Output quality varies unpredictably without a standardized scoring threshold.

---

## Technical Approach

1. **Update SKILL.md** -- Add adversarial mode section documenting strategy availability, activation triggers, and quality threshold requirements. Reference the SSOT (EN-701) for constants.
2. **Update PLAYBOOK.md** -- Integrate creator-critic-revision cycles into each workflow phase (research, analysis, synthesis). Define when adversarial review is mandatory vs. optional based on criticality level (C1-C4).
3. **Update agent files** -- Add strategy-specific guidance to relevant agents (ps-researcher, ps-analyst, ps-synthesizer, ps-reviewer). Map each agent role to its most applicable strategies.
4. **Integrate quality scoring** -- Add LLM-as-Judge (S-014) scoring rubric for PS deliverables with dimensions: completeness, accuracy, evidence quality, logical coherence, actionability.
5. **Define strategy selection guidance** -- Create decision matrix mapping PS domain contexts (research, root cause, architecture review) to recommended adversarial strategies.

---

## Design Source

| Source | Content Used |
|--------|-------------|
| EPIC-002 EN-304 | Problem-solving skill enhancement design, agent-strategy mappings |
| EPIC-002 EN-303 | Decision tree for situational strategy selection |
| ADR-EPIC002-001 | Strategy selection framework, 10 selected strategies |
| EPIC-002 Final Synthesis | Quality scoring methodology, S-014 LLM-as-Judge integration |

---

## Children (Tasks)

| ID | Title | Status | Activity | Agents |
|----|-------|--------|----------|--------|
| TASK-001 | Update skills/problem-solving/SKILL.md with adversarial mode section | pending | DEVELOPMENT | ps-architect |
| TASK-002 | Update skills/problem-solving/PLAYBOOK.md with creator-critic-revision cycles | pending | DEVELOPMENT | ps-architect |
| TASK-003 | Update relevant agent files with strategy-specific guidance | pending | DEVELOPMENT | ps-architect |
| TASK-004 | Integrate quality scoring rubric (S-014 LLM-as-Judge) | pending | DEVELOPMENT | ps-architect |
| TASK-005 | Create strategy selection guidance for PS domain contexts | pending | DEVELOPMENT | ps-analyst |
| TASK-006 | Adversarial review of all changes | pending | TESTING | ps-critic |
| TASK-007 | Creator revision based on review findings | pending | DEVELOPMENT | ps-architect |

### Task Dependencies

```
TASK-001 (SKILL.md) ──┐
TASK-002 (PLAYBOOK.md) ├──> TASK-006 (adversarial review) ──> TASK-007 (revision)
TASK-003 (agents) ─────┤
TASK-004 (scoring) ────┤
TASK-005 (selection) ──┘
```

---

## Acceptance Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| AC-1 | skills/problem-solving/SKILL.md updated with adversarial mode | [ ] |
| AC-2 | skills/problem-solving/PLAYBOOK.md updated with adversarial cycle | [ ] |
| AC-3 | Relevant agent files updated with strategy-specific guidance | [ ] |
| AC-4 | Creator-critic-revision cycle documented with entry/exit criteria | [ ] |
| AC-5 | Quality scoring (>= 0.92) integrated with LLM-as-Judge (S-014) | [ ] |
| AC-6 | Strategy selection guidance for PS domain contexts defined | [ ] |
| AC-7 | All changes follow markdown navigation standards (NAV-001 through NAV-006) | [ ] |

---

## Related Items

### Hierarchy

- **Parent Feature:** [FEAT-008: Quality Framework Implementation](../FEAT-008-quality-framework-implementation.md)

### Dependencies

| Type | Item | Description |
|------|------|-------------|
| depends_on | EN-701 | SSOT must exist for strategy encodings and quality threshold constants |
| depends_on | EPIC-002 EN-304 | PS skill enhancement design (source material) |
| related_to | EN-708 | NASA-SE adversarial mode (parallel skill enhancement) |
| related_to | EN-709 | Orchestration adversarial mode (parallel skill enhancement) |
| related_to | EPIC-002 EN-303 | Decision tree for strategy selection |

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-14 | Claude | pending | Enabler created with 7-task decomposition. Enhances /problem-solving skill with adversarial mode per EPIC-002 design. |
