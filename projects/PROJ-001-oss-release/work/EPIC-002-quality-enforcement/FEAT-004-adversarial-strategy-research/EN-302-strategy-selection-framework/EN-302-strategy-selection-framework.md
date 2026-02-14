# EN-302: Strategy Selection & Decision Framework

<!--
TEMPLATE: Enabler
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.9
CREATED: 2026-02-12 (Claude)
PURPOSE: Create weighted decision framework to score and select the best 10 adversarial strategies from the 15-strategy catalog
-->

> **Type:** enabler
> **Status:** done
> **Resolution:** completed (conditional — pending user ratification of ADR-EPIC002-001)
> **Priority:** critical
> **Impact:** critical
> **Enabler Type:** architecture
> **Created:** 2026-02-12
> **Due:** —
> **Completed:** 2026-02-14
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

Create a weighted decision framework to evaluate all 15 adversarial strategies from EN-301, score them against defined criteria, and select the best 10 for integration into Jerry. The framework must produce an evidence-based rationale for each selection and document rejected strategies with clear exclusion reasons. The output includes a formal Architecture Decision Record (ADR) capturing the selection rationale, risk assessment, and trade-off analysis. This enabler transforms the raw research catalog into an actionable, justified subset ready for situational mapping and skill integration.

## Problem Statement

Having 15 researched strategies does not mean all 15 should be implemented. Some strategies may be redundant when combined, impractical for LLM-based review contexts, too specialized for general use, or insufficiently differentiated to justify the complexity overhead. Without a rigorous, transparent selection process, the choice of which strategies to keep becomes subjective and difficult to defend. A formal decision framework ensures: (a) selection criteria are explicit and weighted, (b) every strategy receives consistent evaluation, (c) rejected strategies have documented rationale, and (d) the final set is optimized for coverage, diversity, and practical applicability within Jerry's agent architecture.

## Technical Approach

1. **Criteria Definition** -- Define evaluation dimensions: effectiveness (empirical evidence), applicability to LLM review contexts, complementarity with other strategies, implementation complexity, cognitive load on users, and differentiation from existing strategies. Assign weights reflecting Jerry's priorities.
2. **Risk Assessment** -- Perform risk analysis on adopting each strategy: What could go wrong? What is the cost of a false positive/negative from each strategy? How does each strategy interact with Jerry's constraint system?
3. **Architecture Trade Study** -- Evaluate strategy adoption from an architectural perspective: How does each strategy map to Jerry's agent model? What are the integration costs? Which strategies compose well together?
4. **Scoring and Selection** -- Apply the weighted framework to score all 15 strategies. Rank by composite score. Select top 10 with sensitivity analysis (how robust is the selection to weight changes?).
5. **Decision Record** -- Create a formal ADR documenting: criteria, weights, scores, selection rationale, rejected strategies with exclusion reasons, and conditions under which rejected strategies might be reconsidered.
6. **Adversarial Review** -- Apply Steelman (strengthen the case for rejected strategies) and Strawman (weaken the case for selected strategies) to stress-test the decision.

## Children (Tasks)

| ID | Title | Status | Activity | Agents |
|----|-------|--------|----------|--------|
| TASK-001 | Define evaluation criteria and weights | done | DESIGN | ps-analyst |
| TASK-002 | Risk assessment of strategy adoption | done | RESEARCH | nse-risk |
| TASK-003 | Architecture trade study for strategy selection | done | DESIGN | nse-architecture |
| TASK-004 | Score all 15 strategies and select top 10 | done | RESEARCH | ps-analyst |
| TASK-005 | Create formal decision record (ADR) | done | DOCUMENTATION | ps-architect |
| TASK-006 | Adversarial review (2 iterations: 0.79→0.935) | done | TESTING | ps-critic |
| TASK-007 | Creator revision based on critic feedback | done | DEVELOPMENT | ps-analyst |
| TASK-008 | Final validation (CONDITIONAL PASS, 9/9 ACs) | done | TESTING | ps-validator |

### Task Dependencies

```
TASK-001 ──┐
TASK-002 ──┼──> TASK-004 ──> TASK-005 ──> TASK-006 ──> TASK-007 ──> TASK-008
TASK-003 ──┘
```

## Acceptance Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| 1 | Evaluation framework defines at least 5 weighted criteria | [x] (6 dimensions defined) |
| 2 | All 15 strategies from EN-301 are scored against every criterion | [x] (90 scores verified) |
| 3 | Exactly 10 strategies are selected with composite score justification | [x] |
| 4 | Each rejected strategy has a documented exclusion rationale | [x] (5 exclusions with reconsideration) |
| 5 | Sensitivity analysis demonstrates selection robustness to weight variation | [x] (3/3 thresholds pass, 9/10 stable) |
| 6 | Risk assessment covers adoption risk for each selected strategy | [x] (105 risk entries) |
| 7 | Formal ADR is created and stored in decisions/ directory | [x] (ADR-EPIC002-001, file location caveat) |
| 8 | Adversarial review (Steelman + Strawman) completed with documented feedback | [x] (2 iterations: 0.79→0.935) |
| 9 | Final validation confirms all criteria met | [x] (CONDITIONAL PASS) |

## Agent Assignments

| Agent | Skill | Role | Phase |
|-------|-------|------|-------|
| ps-analyst | /problem-solving | Creator -- criteria definition, scoring, revision | TASK-001, TASK-004, TASK-007 |
| ps-critic | /problem-solving | Adversarial -- Steelman + Strawman review | TASK-006 |
| nse-risk | /nasa-se | Risk assessment -- strategy adoption risks | TASK-002 |
| nse-architecture | /nasa-se | Trade study -- architectural fit analysis | TASK-003 |
| ps-architect | /problem-solving | ADR author -- formal decision documentation | TASK-005 |
| ps-validator | /problem-solving | Validation -- final quality gate | TASK-008 |

## Related Items

### Hierarchy
- **Parent Feature:** [FEAT-004](../FEAT-004-adversarial-strategy-research.md)

### Dependencies
| Type | Item | Description |
|------|------|-------------|
| depends_on | EN-301 | Requires complete 15-strategy catalog as input |
| blocks | EN-303 | Situational mapping depends on the selected 10 strategies |
| blocks | EN-304 | Skill enhancement depends on finalized strategy selection |

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-12 | Claude | pending | Enabler created with task decomposition. Depends on EN-301 catalog completion. |
| 2026-02-14 | Claude | done | All 8 tasks complete. Quality scores: iter1 0.79, iter2 0.935 (PASS). Top 10 selected: S-014(4.40), S-003(4.30), S-013(4.25), S-007(4.15), S-002(4.10), S-004(4.05), S-010(4.00), S-012(3.75), S-011(3.35), S-001(3.35). 5 excluded: S-008, S-006, S-005, S-009, S-015. ADR-EPIC002-001 created (PROPOSED, pending user ratification). 9/9 ACs pass. Conditional on user ratification per P-020. |
