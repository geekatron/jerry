# EN-708: NASA-SE Adversarial Mode

<!--
TEMPLATE: Enabler
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.9
CREATED: 2026-02-14 (Claude)
PURPOSE: Enhance /nasa-se skill with adversarial mode integration
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

Enhance the `/nasa-se` skill with adversarial mode integration. Update `skills/nasa-se/SKILL.md`, `skills/nasa-se/PLAYBOOK.md`, and relevant agent files to incorporate adversarial strategies, V&V with creator-critic cycles, and risk-based quality gates.

**Value Proposition:**
- Integrates adversarial review into NASA systems engineering processes (NPR 7123.1D)
- Enhances V&V workflows with structured creator-critic-revision cycles
- Adds risk-based quality gates that scale enforcement with mission criticality
- Ensures requirements, design, and verification artifacts undergo adversarial challenge
- Aligns NSE skill with the quality framework designed in EPIC-002

**Technical Scope:**
- SKILL.md updates with adversarial mode section and V&V enhancement
- PLAYBOOK.md updates with creator-critic cycles at review gates
- Agent file updates with strategy-specific guidance per SE role
- Risk-based quality gates mapping criticality levels (C1-C4) to review intensity
- Strategy selection guidance for systems engineering domain contexts

---

## Problem Statement

The `/nasa-se` skill provides NASA-grade systems engineering processes but currently lacks adversarial quality controls in its review and V&V workflows. Technical reviews and verifications rely on single-pass generation without structured challenge. Specific risks:

1. **Requirements gaps** -- Requirements may be incomplete or ambiguous without adversarial challenge from an independent reviewer perspective.
2. **V&V weakness** -- Verification and validation activities may miss failure modes without structured adversarial testing of assumptions.
3. **Review theater** -- Technical reviews may become superficial without a defined critic role challenging the creator's work product.
4. **Risk blind spots** -- Risk assessments may underestimate severity without adversarial stress-testing of mitigation strategies.

---

## Technical Approach

1. **Update SKILL.md** -- Add adversarial mode section documenting V&V enhancement, review gate integration, and risk-based quality thresholds. Reference the SSOT (EN-701) for constants.
2. **Update PLAYBOOK.md** -- Integrate creator-critic-revision cycles into SE review gates (SRR, PDR, CDR equivalents). Define adversarial review requirements per criticality level.
3. **Update agent files** -- Add strategy-specific guidance to SE agents (nse-requirements, nse-verification, nse-validation, nse-risk). Map each agent role to applicable adversarial strategies.
4. **Integrate risk-based quality gates** -- Map criticality levels (C1-C4) to review intensity: C1/C2 require full adversarial cycles, C3/C4 allow abbreviated review.
5. **Define strategy selection guidance** -- Create decision matrix mapping NSE contexts (requirements review, design verification, risk assessment) to recommended adversarial strategies.

---

## Design Source

| Source | Content Used |
|--------|-------------|
| EPIC-002 EN-305 | NASA-SE skill enhancement design, agent-strategy mappings |
| EPIC-002 EN-303 | Decision tree for situational strategy selection |
| ADR-EPIC002-001 | Strategy selection framework, criticality-based review intensity |
| EPIC-002 Final Synthesis | Quality scoring methodology, V&V integration patterns |

---

## Children (Tasks)

| ID | Title | Status | Activity | Agents |
|----|-------|--------|----------|--------|
| TASK-001 | Update skills/nasa-se/SKILL.md with adversarial mode section | pending | DEVELOPMENT | ps-architect |
| TASK-002 | Update skills/nasa-se/PLAYBOOK.md with creator-critic-revision cycles | pending | DEVELOPMENT | ps-architect |
| TASK-003 | Update relevant agent files with strategy-specific guidance | pending | DEVELOPMENT | ps-architect |
| TASK-004 | Integrate risk-based quality gates (C1-C4 mapping) | pending | DEVELOPMENT | nse-risk |
| TASK-005 | Create strategy selection guidance for NSE domain contexts | pending | DEVELOPMENT | ps-analyst |
| TASK-006 | Adversarial review of all changes | pending | TESTING | ps-critic |
| TASK-007 | Creator revision based on review findings | pending | DEVELOPMENT | ps-architect |

### Task Dependencies

```
TASK-001 (SKILL.md) ──┐
TASK-002 (PLAYBOOK.md) ├──> TASK-006 (adversarial review) ──> TASK-007 (revision)
TASK-003 (agents) ─────┤
TASK-004 (risk gates) ─┤
TASK-005 (selection) ──┘
```

---

## Acceptance Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| AC-1 | skills/nasa-se/SKILL.md updated with adversarial mode | [ ] |
| AC-2 | skills/nasa-se/PLAYBOOK.md updated with adversarial cycle | [ ] |
| AC-3 | Relevant agent files updated with strategy-specific guidance | [ ] |
| AC-4 | V&V integration with adversarial review documented | [ ] |
| AC-5 | Risk-based quality gates integrated (C1-C4 mapping) | [ ] |
| AC-6 | Strategy selection guidance for NSE domain contexts defined | [ ] |

---

## Related Items

### Hierarchy

- **Parent Feature:** [FEAT-008: Quality Framework Implementation](../FEAT-008-quality-framework-implementation.md)

### Dependencies

| Type | Item | Description |
|------|------|-------------|
| depends_on | EN-701 | SSOT must exist for criticality levels and quality threshold constants |
| depends_on | EPIC-002 EN-305 | NSE skill enhancement design (source material) |
| related_to | EN-707 | Problem-solving adversarial mode (parallel skill enhancement) |
| related_to | EN-709 | Orchestration adversarial mode (parallel skill enhancement) |
| related_to | EPIC-002 EN-303 | Decision tree for strategy selection |

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-14 | Claude | pending | Enabler created with 7-task decomposition. Enhances /nasa-se skill with adversarial mode per EPIC-002 design. |
