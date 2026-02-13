# FEAT-004: Adversarial Strategy Research & Skill Enhancement

<!--
TEMPLATE: Feature
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.4
CREATED: 2026-02-12 (Claude)
PURPOSE: Research 15 adversarial strategies, select best 10, enhance skills
-->

> **Type:** feature
> **Status:** in_progress
> **Priority:** critical
> **Impact:** critical
> **Created:** 2026-02-12
> **Due:** —
> **Completed:** —
> **Parent:** EPIC-002
> **Owner:** —
> **Target Sprint:** Sprint 2

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What this feature delivers |
| [Benefit Hypothesis](#benefit-hypothesis) | Expected outcomes |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done |
| [MVP Definition](#mvp-definition) | Scope boundaries |
| [Children (Stories/Enablers)](#children-storiesenablers) | Work breakdown |
| [Progress Summary](#progress-summary) | Current completion status |
| [Related Items](#related-items) | Dependencies and hierarchy |
| [History](#history) | Change log |

---

## Summary

Deep research into adversarial critic/review strategies from authoritative industry sources. Identify 15 strategies, evaluate and select the best 10, define situational applicability for each, and enhance the `/problem-solving`, `/nasa-se`, AND `/orchestration` skills to integrate these strategies. The /orchestration skill must bake in adversarial feedback loops so that creator→critic→revision cycles are automatic rather than requiring user prompting.

**Value Proposition:**
- Evidence-based selection of adversarial review strategies with citations
- Clear guidance on when to use each strategy (situational mapping)
- Enhanced skills that can invoke adversarial patterns as part of quality workflows
- /orchestration skill updated to automatically embed adversarial review cycles in workflow plans
- Platform-portable implementation (macOS, Windows, Linux)
- Full utilization of all 22 available agents across problem-solving (9), nasa-se (10), and orchestration (3) skills

---

## Benefit Hypothesis

**We believe that** researching and integrating 10 proven adversarial review strategies into Jerry's skills

**Will result in** consistently higher quality outputs through structured adversarial feedback that catches blind spots, challenges assumptions, and strengthens arguments

**We will know we have succeeded when:**
- 15 strategies are researched with authoritative citations
- Best 10 are selected with evidence-based rationale
- Each strategy has defined situational applicability
- /problem-solving and /nasa-se skills are enhanced with adversarial capabilities
- /orchestration skill updated to bake in adversarial feedback loops automatically
- All research passes adversarial quality review (>=0.92)
- Decisions captured as DEC entities, discoveries as DISC entities throughout
- All 22 available agents leveraged per their expertise areas

---

## Acceptance Criteria

### Definition of Done

- [ ] Deep research identifies 15 adversarial strategies from authoritative sources
- [ ] All research includes citations, references, and sources from industry experts/leaders/innovators
- [ ] 10 best strategies selected with evidence-based decision rationale
- [ ] Each strategy has documented situational applicability (when to use, when not to use)
- [ ] /problem-solving skill enhanced with adversarial strategy integration
- [ ] /nasa-se skill enhanced with adversarial strategy integration
- [ ] /orchestration skill updated to bake in adversarial feedback loops automatically
- [ ] All creator outputs pass adversarial quality review (>=0.92 quality score)
- [ ] Minimum 3 creator→critic→revision iterations per deliverable
- [ ] Orchestration plan exists at Feature level
- [ ] Platform portability considered (macOS, Windows, Linux)
- [ ] All 22 agents leveraged per their expertise (ps-*, nse-*, orch-*)
- [ ] Decisions captured as DEC entities in worktracker during work
- [ ] Discoveries captured as DISC entities in worktracker during work
- [ ] Detailed enabler .md files with task decomposition for all enablers
- [ ] Task .md files created and tracked for each work unit

### Functional Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| AC-1 | 15 adversarial strategies researched with authoritative citations | [ ] |
| AC-2 | Decision matrix with weighted criteria for strategy selection | [ ] |
| AC-3 | 10 strategies selected with evidence-based rationale | [ ] |
| AC-4 | Situational mapping: strategy → context → when to use/avoid | [ ] |
| AC-5 | ps-critic agent spec updated with adversarial modes | [ ] |
| AC-6 | nasa-se verification agents (nse-verification, nse-reviewer, nse-qa) updated with adversarial modes | [ ] |
| AC-7 | Integration tests for adversarial strategy invocation | [ ] |
| AC-8 | Orchestration plan created for this Feature | [ ] |
| AC-9 | /orchestration skill (orch-planner, orch-tracker, orch-synthesizer) updated to automatically embed adversarial review cycles | [ ] |
| AC-10 | All 9 ps-* agents utilized per their expertise during research/analysis | [ ] |
| AC-11 | All 10 nse-* agents utilized per their expertise during design/V&V | [ ] |
| AC-12 | All 3 orch-* agents utilized for workflow management | [ ] |
| AC-13 | Decisions (DEC) entities created and tracked throughout work | [ ] |
| AC-14 | Discoveries (DISC) entities created and tracked throughout work | [ ] |
| AC-15 | ps-synthesizer produces meta-analysis synthesis of all research | [ ] |
| AC-16 | nse-requirements defines shall-statement requirements for skill enhancements | [ ] |
| AC-17 | nse-risk produces risk assessment for adversarial strategy integration | [ ] |
| AC-18 | ps-reviewer performs code/design review of skill modifications | [ ] |

### Non-Functional Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| NFC-1 | All research artifacts persisted to filesystem (P-002) | [ ] |
| NFC-2 | All agent interactions follow P-003 (no recursive subagents) | [ ] |
| NFC-3 | All quality scores documented with calculation breakdown | [ ] |
| NFC-4 | Cross-platform compatibility verified (macOS, Windows, Linux) | [ ] |
| NFC-5 | Enabler .md files exist for all EN-301 through EN-307 | [ ] |
| NFC-6 | Task .md files exist for all work units under each enabler | [ ] |
| NFC-7 | nse-configuration tracks configuration baselines for skill modifications | [ ] |
| NFC-8 | ps-reporter generates status reports at enabler completion | [ ] |

---

## MVP Definition

### In Scope (MVP)

- Research 15 adversarial strategies with citations (using ps-researcher, nse-explorer)
- Select 10 with evidence-based decision (using ps-analyst, nse-architecture, nse-risk)
- Define situational applicability for each (using ps-architect, nse-requirements)
- Enhance ps-critic agent with adversarial modes (using ps-architect, ps-reviewer)
- Enhance nasa-se verification agents with adversarial modes (using nse-architecture, nse-reviewer)
- Update /orchestration skill to bake in adversarial feedback loops (using ps-architect, orch-planner)
- Creator→critic→revision cycles with >=0.92 target
- Track all decisions (DEC entities) and discoveries (DISC entities)
- Detailed enabler and task entities for all work items

### Out of Scope (Future)

- Automated adversarial strategy selection based on context
- Custom strategy creation tooling
- Strategy effectiveness metrics dashboard
- A/B testing of strategy combinations

---

## Children (Stories/Enablers)

### Enabler Inventory

| ID | Type | Title | Status | Priority | Effort | Agents |
|----|------|-------|--------|----------|--------|--------|
| [EN-301](./EN-301-deep-research-adversarial-strategies/EN-301-deep-research-adversarial-strategies.md) | Enabler | Deep Research: 15 Adversarial Strategies | **done** | critical | 13 | ps-researcher, ps-critic, ps-synthesizer, nse-explorer |
| [EN-302](./EN-302-strategy-selection-framework/EN-302-strategy-selection-framework.md) | Enabler | Strategy Selection & Decision Framework | pending | critical | 8 | ps-analyst, ps-critic, nse-architecture, nse-risk |
| [EN-303](./EN-303-situational-applicability-mapping/EN-303-situational-applicability-mapping.md) | Enabler | Situational Applicability Mapping | pending | high | 5 | ps-architect, ps-critic, nse-requirements |
| [EN-304](./EN-304-problem-solving-skill-enhancement/EN-304-problem-solving-skill-enhancement.md) | Enabler | /problem-solving Skill Enhancement | pending | critical | 10 | ps-architect, ps-critic, ps-reviewer, nse-verification |
| [EN-305](./EN-305-nasa-se-skill-enhancement/EN-305-nasa-se-skill-enhancement.md) | Enabler | /nasa-se Skill Enhancement | pending | high | 8 | nse-architecture, ps-critic, nse-reviewer, nse-verification |
| [EN-306](./EN-306-integration-testing-validation/EN-306-integration-testing-validation.md) | Enabler | Integration Testing & Validation | pending | high | 5 | ps-validator, nse-qa, nse-verification, ps-reporter |
| [EN-307](./EN-307-orchestration-skill-enhancement/EN-307-orchestration-skill-enhancement.md) | Enabler | /orchestration Skill Enhancement (Adversarial Loops) | pending | critical | 8 | ps-architect, ps-critic, orch-planner, nse-reviewer |

### Enabler Dependencies

```
EN-301 (Research)
    |
    +---> EN-302 (Selection) ---> EN-303 (Mapping)
                                       |
                         +-------------+-------------+
                         |             |             |
                         v             v             v
                    EN-304 (PS)   EN-305 (NSE)  EN-307 (ORCH)
                         |             |             |
                         +-------------+-------------+
                                       |
                                       v
                                  EN-306 (Testing)
                          [depends on EN-304, EN-305, EN-307]
```

---

## Progress Summary

### Status Overview

```
+------------------------------------------------------------------+
|                   FEATURE PROGRESS TRACKER                        |
+------------------------------------------------------------------+
| Enablers:  [###.................] 14% (1/7 completed)             |
| Tasks:     [########............] 40% (8/20 EN-301 tasks done)   |
+------------------------------------------------------------------+
| Overall:   [###.................] ~14%                             |
+------------------------------------------------------------------+
```

### Progress Metrics

| Metric | Value |
|--------|-------|
| **Total Enablers** | 7 |
| **Completed Enablers** | 1 (EN-301) |
| **Total Effort (points)** | 57 |
| **Completed Effort** | 13 |
| **Completion %** | 23% (by effort) |

---

## Related Items

### Hierarchy

- **Parent Epic:** [EPIC-002: Quality Framework Enforcement](../EPIC-002-quality-enforcement.md)

### Related Features

- [FEAT-005: Enforcement Mechanisms](../FEAT-005-enforcement-mechanisms/FEAT-005-enforcement-mechanisms.md) - Enforcement depends on adversarial strategies being defined
- [FEAT-006: EPIC-001 Retroactive Review](../FEAT-006-epic001-retroactive-review/FEAT-006-epic001-retroactive-review.md) - Retroactive review uses the adversarial strategies defined here

### Dependencies

| Dependency Type | Item | Description |
|----------------|------|-------------|
| Blocks | FEAT-005 | Enforcement mechanisms need adversarial strategies defined |
| Blocks | FEAT-006 | Retroactive review needs adversarial strategies to apply |

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-12 | Claude | pending | Feature created under EPIC-002. 6 enablers defined (EN-301 through EN-306). |
| 2026-02-12 | Claude | in_progress | Added EN-307 (/orchestration skill enhancement). Updated ACs to 18 functional + 8 non-functional criteria. Added requirements for full agent utilization (22 agents), DEC/DISC entity tracking, and detailed enabler/task decomposition. |
| 2026-02-13 | Claude | in_progress | EN-301 completed: 15-strategy catalog with 2 adversarial review iterations (0.89→0.936), final validation PASS 8/8. User ratified EN-301-DEV-001 (Blue Team→R-6). EN-302 now unblocked. |

---

## System Mapping

| System | Mapping |
|--------|---------|
| **Azure DevOps** | Feature |
| **SAFe** | Feature (Program Backlog) |
| **JIRA** | Epic (or custom issue type) |
