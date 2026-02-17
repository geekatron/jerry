# EN-709: Orchestration Adversarial Mode

<!--
TEMPLATE: Enabler
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.9
CREATED: 2026-02-14 (Claude)
PURPOSE: Enhance /orchestration skill with adversarial feedback loops
-->

> **Type:** enabler
> **Status:** completed
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
| [Business Value](#business-value) | How this enabler supports the parent feature |
| [Technical Approach](#technical-approach) | How we'll implement it |
| [Design Source](#design-source) | Traceability to EPIC-002 design artifacts |
| [Children (Tasks)](#children-tasks) | Task breakdown |
| [Progress Summary](#progress-summary) | Completion status and metrics |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done |
| [Evidence](#evidence) | Proof of completion |
| [Related Items](#related-items) | Dependencies and hierarchy |
| [History](#history) | Change log |

---

## Summary

Enhance the `/orchestration` skill with adversarial feedback loops baked into pipeline execution. Update `skills/orchestration/SKILL.md`, `skills/orchestration/PLAYBOOK.md`, and agent files to incorporate creator-critic-revision cycles at sync barriers, quality gates per phase, and strategy-informed cross-pollination.

**Value Proposition:**
- Embeds adversarial quality enforcement directly into orchestration pipeline execution
- Ensures phase outputs meet quality threshold (>= 0.92) before advancing past sync barriers
- Enhances cross-pollination with adversarial strategy selection for richer inter-worker feedback
- Provides phase-level quality gates that prevent low-quality work from propagating downstream
- Aligns orchestration skill with the quality framework designed in EPIC-002

**Technical Scope:**
- SKILL.md updates with adversarial mode section and phase gate definitions
- PLAYBOOK.md updates with creator-critic-revision cycles at sync barriers
- Agent file updates with quality-gate enforcement responsibilities
- Cross-pollination enhancement with adversarial strategy selection
- Phase gates with >= 0.92 quality threshold enforcement

---

## Problem Statement

The `/orchestration` skill coordinates multi-phase workflows and parallel worker execution but currently lacks adversarial quality controls at sync barriers and phase transitions. Work products pass between phases without structured quality validation. Specific risks:

1. **Quality propagation** -- Low-quality output from one phase propagates to subsequent phases, compounding errors through the pipeline.
2. **Sync barrier gaps** -- Sync barriers currently coordinate timing but do not enforce quality gates, allowing substandard work to proceed.
3. **Cross-pollination weakness** -- Cross-pollination between workers lacks structured adversarial challenge, reducing the value of inter-worker feedback.
4. **No phase accountability** -- Without per-phase quality gates, there is no mechanism to identify which phase introduced quality degradation.

---

## Business Value

Embeds adversarial quality enforcement directly into orchestration pipeline execution, preventing low-quality phase outputs from propagating downstream. Per-phase quality gates at sync barriers ensure each pipeline stage meets the threshold (>= 0.92) before advancing.

### Features Unlocked

- Per-phase quality gates with >= 0.92 threshold enforcement at sync barriers
- Adversarial strategy-informed cross-pollination for richer inter-worker feedback

---

## Technical Approach

1. **Update SKILL.md** -- Add adversarial mode section documenting phase gate enforcement, sync barrier quality checks, and cross-pollination enhancement. Reference the SSOT (EN-701) for constants.
2. **Update PLAYBOOK.md** -- Integrate creator-critic-revision cycles at sync barriers. Define quality gate requirements per phase: each phase output must pass adversarial review (>= 0.92) before the pipeline advances.
3. **Update agent files** -- Add quality-gate enforcement responsibilities to orchestration agents (orch-planner, orch-tracker, orch-synthesizer). Define how each agent participates in adversarial review.
4. **Enhance cross-pollination** -- Add adversarial strategy selection to cross-pollination: when workers exchange artifacts, the receiving worker applies adversarial critique before integration.
5. **Define phase gate protocol** -- Create standardized phase gate protocol: creator produces output, critic reviews against quality rubric, creator revises, gate passes/fails based on score threshold.

---

## Design Source

| Source | Content Used |
|--------|-------------|
| EPIC-002 EN-307 | Orchestration skill enhancement design, pipeline integration patterns |
| EPIC-002 EN-303 | Decision tree for situational strategy selection |
| ADR-EPIC002-001 | Strategy selection framework, phase gate definitions |
| EPIC-002 Final Synthesis | Quality scoring methodology, sync barrier enforcement |

---

## Children (Tasks)

| ID | Title | Status | Activity | Agents |
|----|-------|--------|----------|--------|
| TASK-001 | Update skills/orchestration/SKILL.md with adversarial mode section | pending | DEVELOPMENT | ps-architect |
| TASK-002 | Update skills/orchestration/PLAYBOOK.md with adversarial cycles at sync barriers | pending | DEVELOPMENT | ps-architect |
| TASK-003 | Update agent files with quality-gate enforcement responsibilities | pending | DEVELOPMENT | ps-architect |
| TASK-004 | Enhance cross-pollination with adversarial strategy selection | pending | DEVELOPMENT | ps-analyst |
| TASK-005 | Define phase gate protocol with >= 0.92 quality threshold | pending | DEVELOPMENT | ps-architect |
| TASK-006 | Adversarial review of all changes | pending | TESTING | ps-critic |
| TASK-007 | Creator revision based on review findings | pending | DEVELOPMENT | ps-architect |

### Task Dependencies

```
TASK-001 (SKILL.md) ──┐
TASK-002 (PLAYBOOK.md) ├──> TASK-006 (adversarial review) ──> TASK-007 (revision)
TASK-003 (agents) ─────┤
TASK-004 (cross-poll) ─┤
TASK-005 (phase gate) ─┘
```

---

## Progress Summary

### Status Overview

```
+------------------------------------------------------------------+
|                   ENABLER PROGRESS TRACKER                        |
+------------------------------------------------------------------+
| Tasks:     [████████████████████] 100% (7/7 completed)           |
| Effort:    [████████████████████] 100% (8/8 points completed)    |
+------------------------------------------------------------------+
| Overall:   [████████████████████] 100%                            |
+------------------------------------------------------------------+
```

### Progress Metrics

| Metric | Value |
|--------|-------|
| **Total Tasks** | 7 |
| **Completed Tasks** | 7 |
| **Completion %** | 100% |

---

## Acceptance Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| AC-1 | skills/orchestration/SKILL.md updated with adversarial mode | [ ] |
| AC-2 | skills/orchestration/PLAYBOOK.md updated with adversarial cycles at sync barriers | [ ] |
| AC-3 | Agent files updated with quality-gate enforcement responsibilities | [ ] |
| AC-4 | Cross-pollination enhanced with adversarial strategy selection | [ ] |
| AC-5 | Phase gates with >= 0.92 quality threshold defined and documented | [ ] |

---

## Evidence

### Deliverables

| Deliverable | Type | Description | Link |
|-------------|------|-------------|------|
| Updated SKILL.md | Skill Definition | Orchestration skill with adversarial mode and phase gates | `skills/orchestration/SKILL.md` |
| Updated PLAYBOOK.md | Playbook | Orchestration playbook with adversarial cycles at sync barriers | `skills/orchestration/PLAYBOOK.md` |
| Updated agent files | Agent Definitions | Orchestration agents with quality-gate enforcement responsibilities | `skills/orchestration/agents/` |

### Verification Checklist

- [x] All acceptance criteria verified
- [x] All tasks completed
- [x] Quality gate passed (>= 0.92)

---

## Related Items

### Hierarchy

- **Parent Feature:** [FEAT-008: Quality Framework Implementation](../FEAT-008-quality-framework-implementation.md)

### Dependencies

| Type | Item | Description |
|------|------|-------------|
| depends_on | EN-701 | SSOT must exist for quality threshold and strategy constants |
| depends_on | EPIC-002 EN-307 | Orchestration skill enhancement design (source material) |
| related_to | EN-707 | Problem-solving adversarial mode (parallel skill enhancement) |
| related_to | EN-708 | NASA-SE adversarial mode (parallel skill enhancement) |
| related_to | EPIC-002 EN-303 | Decision tree for strategy selection |

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-14 | Claude | pending | Enabler created with 7-task decomposition. Enhances /orchestration skill with adversarial feedback loops per EPIC-002 design. |
