# FEAT-009: Adversarial Strategy Templates & /adversary Skill

<!--
TEMPLATE: Feature
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.4
CREATED: 2026-02-14 (Claude)
PURPOSE: Create reusable adversarial strategy execution templates and /adversary skill
-->

> **Type:** feature
> **Status:** completed
> **Priority:** critical
> **Impact:** critical
> **Created:** 2026-02-14
> **Due:** ---
> **Completed:** 2026-02-15
> **Parent:** EPIC-003
> **Owner:** ---
> **Target Sprint:** ---

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What this feature delivers |
| [Benefit Hypothesis](#benefit-hypothesis) | Expected benefits |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done |
| [Children (Enablers)](#children-enablers) | Enabler inventory |
| [Progress Summary](#progress-summary) | Overall feature progress |
| [Related Items](#related-items) | Dependencies and hierarchy |
| [History](#history) | Change log |

---

## Summary

Create reusable adversarial strategy execution templates for all 10 selected strategies (S-001 through S-014) and build the `/adversary` skill to make adversarial review workflows easy to invoke. EPIC-003 implemented the quality framework infrastructure but left a critical gap: strategy names without execution methodology are not actionable for reproducibility.

**Value Proposition:**
- Transforms strategy references (e.g., "apply S-002") into reproducible step-by-step execution protocols
- Provides criticality-based strategy selection (C1 minimal, C4 all 10)
- Creates a dedicated `/adversary` skill for on-demand adversarial reviews
- Extends existing agents (ps-critic, ps-reviewer, nse-reviewer, ps-architect) with template references

**Source Material:**
- `projects/PROJ-001-oss-release/work/EPIC-002-quality-enforcement/FEAT-004-adversarial-strategy-research/research-15-adversarial-strategies.md` (26,645 tokens)
- `.context/rules/quality-enforcement.md` (SSOT for strategy IDs and criticality levels)

---

## Benefit Hypothesis

**We believe that** creating concrete execution templates for all 10 selected adversarial strategies and building a dedicated /adversary skill

**Will result in** reproducible, consistent adversarial quality reviews that can be applied systematically across all criticality levels

**We will know we have succeeded when:**
- All 10 strategy templates follow a canonical format and pass >= 0.92 quality gate
- `/adversary` skill correctly selects strategies by criticality level
- Existing agents reference strategy templates instead of abstract strategy names
- E2E tests validate template format, agent references, and strategy selection

---

## Acceptance Criteria

### Definition of Done

- [x] All 10 strategy templates created in `.context/templates/adversarial/`
- [x] TEMPLATE-FORMAT.md defines canonical template structure
- [x] `/adversary` skill scaffold complete (SKILL.md, PLAYBOOK.md, 3 agents)
- [x] Existing agents updated with template references
- [x] E2E tests pass (`uv run pytest tests/e2e/test_adversary_templates_e2e.py`)
- [x] CLAUDE.md updated with /adversary skill entry
- [x] All enablers pass >= 0.92 quality gate via creator-critic-revision cycle
- [x] Git commits with clean working tree after each phase

### Functional Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| FC-1 | 10 strategy templates exist matching TEMPLATE-FORMAT.md | [x] |
| FC-2 | adv-selector picks correct strategies per criticality level | [x] |
| FC-3 | adv-executor references correct template for each strategy | [x] |
| FC-4 | adv-scorer implements S-014 rubric-based scoring | [x] |
| FC-5 | ps-critic, ps-reviewer, nse-reviewer, ps-architect reference templates | [x] |
| FC-6 | /adversary skill invocable and documented in CLAUDE.md | [x] |

### Non-Functional Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| NFC-1 | All strategy IDs match SSOT (quality-enforcement.md) | [x] |
| NFC-2 | Each enabler passes >= 0.92 quality gate | [x] |
| NFC-3 | Creator-critic-revision cycle (min 3 iterations) per deliverable | [x] |
| NFC-4 | Templates follow markdown navigation standards (H-23, H-24) | [x] |

---

## Children (Enablers)

### Enabler Inventory

| ID | Title | Status | Priority | Effort | Phase |
|----|-------|--------|----------|--------|-------|
| [EN-801](./EN-801-template-format-standard/EN-801-template-format-standard.md) | Template Format Standard | completed | critical | 3 | 1 |
| [EN-802](./EN-802-adversary-skill-skeleton/EN-802-adversary-skill-skeleton.md) | /adversary Skill Skeleton | completed | critical | 3 | 1 |
| [EN-803](./EN-803-s014-llm-as-judge/EN-803-s014-llm-as-judge.md) | S-014 LLM-as-Judge Template | completed | critical | 5 | 2 |
| [EN-804](./EN-804-s010-self-refine/EN-804-s010-self-refine.md) | S-010 Self-Refine Template | completed | critical | 3 | 2 |
| [EN-805](./EN-805-s007-constitutional-ai/EN-805-s007-constitutional-ai.md) | S-007 Constitutional AI Template | completed | critical | 3 | 2 |
| [EN-806](./EN-806-s002-devils-advocate/EN-806-s002-devils-advocate.md) | S-002 Devil's Advocate Template | completed | high | 3 | 3 |
| [EN-807](./EN-807-s003-steelman/EN-807-s003-steelman.md) | S-003 Steelman Template | completed | high | 3 | 3 |
| [EN-808](./EN-808-tier3-risk-strategies/EN-808-tier3-risk-strategies.md) | Tier 3 Risk Strategy Templates | completed | high | 5 | 4 |
| [EN-809](./EN-809-tier4-security-strategies/EN-809-tier4-security-strategies.md) | Tier 4 Security Strategy Templates | completed | high | 3 | 5 |
| [EN-810](./EN-810-adversary-skill-agents/EN-810-adversary-skill-agents.md) | Adversary Skill Agents | completed | critical | 5 | 6 |
| [EN-811](./EN-811-agent-extensions/EN-811-agent-extensions.md) | Agent Extensions | completed | high | 3 | 7 |
| [EN-812](./EN-812-integration-testing/EN-812-integration-testing.md) | Integration Testing | completed | critical | 5 | 7 |

---

## Progress Summary

### Status Overview

```
+------------------------------------------------------------------+
|                   FEATURE PROGRESS TRACKER                        |
+------------------------------------------------------------------+
| Enablers:  [████████████████████] 100% (12/12 completed)         |
| Effort:    [████████████████████] 100% (46/46 points)            |
+------------------------------------------------------------------+
| Overall:   [████████████████████] 100%                            |
+------------------------------------------------------------------+
```

### Progress Metrics

| Metric | Value |
|--------|-------|
| **Total Enablers** | 12 |
| **Completed Enablers** | 12 |
| **Total Effort (points)** | 46 |
| **Completed Effort** | 46 |
| **Completion %** | 100% |

### Sprint Tracking

| Sprint | Enablers | Status | Notes |
|--------|----------|--------|-------|
| 2026-02-15 | EN-801, EN-802 (Phase 1) | completed | Foundation: Template Format + Skill Skeleton |
| 2026-02-15 | EN-803, EN-804, EN-805 (Phase 2) | completed | Tier 1: S-014, S-010, S-007 |
| 2026-02-15 | EN-806, EN-807 (Phase 3) | completed | Tier 2: S-002, S-003 |
| 2026-02-15 | EN-808 (Phase 4) | completed | Tier 3: S-004/S-012/S-013 |
| 2026-02-15 | EN-809 (Phase 5) | completed | Tier 4: S-001/S-011 |
| 2026-02-15 | EN-810 (Phase 6) | completed | Skill Agents: selector/executor/scorer |
| 2026-02-15 | EN-811, EN-812 (Phase 7) | completed | Integration: Agent Extensions + E2E |

---

## Related Items

### Hierarchy

- **Parent Epic:** [EPIC-003: Quality Framework Implementation](../EPIC-003-quality-implementation.md)

### Dependencies

| Dependency Type | Item | Description |
|----------------|------|-------------|
| Depends On | FEAT-008 | Quality framework infrastructure (SSOT, hooks, enforcement engines) |
| Depends On | FEAT-004 (EPIC-002) | Adversarial strategy research (source material for templates) |

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-14 | Claude | pending | Feature created. 12 enablers across 7 phases. Source: EPIC-002 FEAT-004 research + EPIC-003 gap analysis. |
| 2026-02-15 | Claude | completed | All 12 enablers verified on disk. Status sync: all enablers updated to completed. AC checkboxes verified against deliverables. |
