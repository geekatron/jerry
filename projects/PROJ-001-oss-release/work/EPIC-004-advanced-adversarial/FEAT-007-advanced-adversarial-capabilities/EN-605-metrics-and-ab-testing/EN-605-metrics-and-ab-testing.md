# EN-605: Effectiveness Metrics Dashboard & A/B Testing Framework

<!--
TEMPLATE: Enabler
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.9
CREATED: 2026-02-12 (Claude)
PURPOSE: Implement effectiveness metrics collection, visualization dashboard, and A/B testing framework
-->

> **Type:** enabler
> **Status:** pending
> **Priority:** high
> **Impact:** high
> **Enabler Type:** infrastructure
> **Created:** 2026-02-12
> **Due:** —
> **Completed:** —
> **Parent:** FEAT-007
> **Owner:** —
> **Effort:** 10

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What this enabler delivers |
| [Problem Statement](#problem-statement) | Why this work is needed |
| [Technical Approach](#technical-approach) | How we'll implement it |
| [Children (Tasks)](#children-tasks) | Task breakdown with agent assignments |
| [Task Dependencies](#task-dependencies) | Execution order and parallel opportunities |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done |
| [Agent Assignments](#agent-assignments) | Which agents are used and their roles |
| [Related Items](#related-items) | Dependencies and hierarchy |
| [History](#history) | Change log |

---

## Summary

Implement the effectiveness metrics collection, visualization dashboard, and A/B testing framework. Build per-strategy scoring, trend analysis, and controlled experiment infrastructure for comparing strategy combinations. This enabler translates the research findings from EN-602 into a working measurement and experimentation system.

**Value Proposition:**
- Provides quantitative evidence for adversarial strategy effectiveness, replacing subjective assessments
- Per-strategy scoring enables data-driven strategy selection optimization in EN-603
- Trend analysis reveals quality improvement patterns over time
- A/B testing framework enables empirical comparison of strategy combinations
- Dashboard visualization makes metrics accessible to all stakeholders, not just technical users
- Creates a feedback loop: metrics inform selection, selection drives better outcomes, outcomes improve metrics

**Technical Scope:**
- Metrics collection infrastructure (event capture, storage, aggregation)
- Per-strategy effectiveness scoring methodology (based on EN-602 research)
- Trend analysis and time-series tracking for quality improvement
- A/B testing framework with experiment definition, assignment, and analysis
- Statistical significance validation for experiment results
- Dashboard visualization (CLI-based reporting and structured output)

---

## Problem Statement

With adversarial strategies defined (FEAT-004), automated selection built (EN-603), and custom strategies enabled (EN-604), Jerry still lacks the ability to measure whether its adversarial review system is actually improving quality. Without metrics and experimentation:

1. **No feedback loop** -- The system cannot learn from its own outcomes to improve strategy recommendations.
2. **No evidence for optimization** -- Strategy selection (EN-603) cannot be tuned without empirical data on what works.
3. **No experiment capability** -- Claims about strategy A being better than strategy B cannot be validated without controlled comparison.
4. **No stakeholder visibility** -- Users and project leads have no way to see the impact of adversarial review on overall quality.
5. **No trend detection** -- Quality degradation or improvement patterns go unnoticed without longitudinal tracking.

This enabler must implement the measurement and experimentation infrastructure that closes the feedback loop between strategy selection, execution, and improvement.

---

## Technical Approach

1. **Metrics Collection Architecture** -- Design the metrics collection infrastructure following hexagonal architecture:
   - Domain events emitted by adversarial review processes (ReviewStarted, ReviewCompleted, DefectFound, etc.)
   - Metrics collector port (application layer) with filesystem adapter (infrastructure layer)
   - Event aggregation pipeline that computes per-strategy metrics from raw events
   - Storage format: JSON files in a metrics directory, one file per strategy per time period

2. **Effectiveness Scoring Methodology** -- Implement the scoring methodology based on EN-602 research:
   - Defect detection rate (defects found / total defects estimated)
   - Review thoroughness score (coverage of review dimensions)
   - False positive rate (invalid findings / total findings)
   - Composite effectiveness score (weighted combination of above metrics)
   - Confidence interval for each score based on sample size

3. **A/B Testing Framework** -- Build controlled experiment infrastructure:
   - Experiment definition (strategy A vs. strategy B, target metrics, duration)
   - Random assignment mechanism (deterministic hash-based for reproducibility)
   - Result collection and aggregation per experiment arm
   - Statistical significance testing (frequentist or Bayesian per EN-602 recommendations)
   - Experiment lifecycle management (create, start, stop, analyze)

4. **Quality Assurance** -- Comprehensive QA testing by nse-qa covering metrics accuracy, A/B testing correctness, and edge case handling.

5. **End-to-End Validation** -- Validate the complete metrics pipeline from event emission to dashboard display using realistic scenarios.

6. **Adversarial Critique** -- Apply adversarial review to the design and implementation, challenging metric validity, statistical assumptions, and dashboard utility.

---

## Children (Tasks)

| ID | Title | Status | Activity | Agents |
|----|-------|--------|----------|--------|
| TASK-001 | Design metrics collection architecture (events, collectors, storage) | pending | DEVELOPMENT | ps-architect |
| TASK-002 | Define effectiveness scoring methodology (formulas, weights, confidence) | pending | DEVELOPMENT | ps-analyst |
| TASK-003 | Implement A/B testing framework (experiments, assignment, analysis) | pending | DEVELOPMENT | ps-architect |
| TASK-004 | Quality assurance testing of metrics and A/B testing components | pending | TESTING | nse-qa |
| TASK-005 | End-to-end validation of complete metrics pipeline | pending | TESTING | ps-validator |
| TASK-006 | Adversarial critique of design, metrics validity, and statistical assumptions | pending | TESTING | ps-critic |

### Task Dependencies

```
TASK-001 (metrics architecture) ──┐
                                  ├──> TASK-004 (QA testing) ──> TASK-005 (end-to-end validation)
TASK-002 (scoring methodology) ───┤                                │
                                  │                                v
TASK-003 (A/B testing framework) ─┘                         TASK-006 (adversarial critique)
```

- TASK-001, TASK-002, and TASK-003 can execute in parallel (independent design/implementation tracks)
- TASK-004 requires all three implementation tasks to complete before QA testing
- TASK-005 requires TASK-004 QA to pass before end-to-end validation
- TASK-006 applies adversarial critique after end-to-end validation confirms correctness

---

## Acceptance Criteria

### Functional Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| AC-1 | Metrics collection captures ReviewStarted, ReviewCompleted, DefectFound events | [ ] |
| AC-2 | Per-strategy effectiveness score computed with defect detection rate, thoroughness, and false positive rate | [ ] |
| AC-3 | Composite effectiveness score calculated with configurable weights | [ ] |
| AC-4 | Confidence intervals computed for all scores based on sample size | [ ] |
| AC-5 | Trend analysis tracks effectiveness scores over time periods | [ ] |
| AC-6 | A/B testing: experiments can be defined with strategy pair, target metrics, and duration | [ ] |
| AC-7 | A/B testing: random assignment is deterministic and reproducible | [ ] |
| AC-8 | A/B testing: statistical significance validated for experiment results | [ ] |
| AC-9 | Dashboard output available in CLI format (structured text) and JSON | [ ] |
| AC-10 | End-to-end validation confirms metrics accuracy with known test data | [ ] |
| AC-11 | Adversarial critique completed with documented feedback | [ ] |

### Non-Functional Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| NFC-1 | Metrics storage is filesystem-based (JSON files, no database dependency) | [ ] |
| NFC-2 | Implementation follows hexagonal architecture (domain events, ports, adapters) | [ ] |
| NFC-3 | All code has type hints and docstrings per coding standards | [ ] |
| NFC-4 | Unit test coverage >= 90% for metrics and A/B testing components | [ ] |
| NFC-5 | No recursive subagent invocations (P-003 compliance) | [ ] |
| NFC-6 | Cross-platform compatibility (macOS, Windows, Linux) | [ ] |
| NFC-7 | Metrics collection adds < 100ms latency to review completion | [ ] |

---

## Agent Assignments

| Agent | Skill | Role | Phase |
|-------|-------|------|-------|
| ps-architect | /problem-solving | Creator -- metrics architecture and A/B testing framework design/implementation | TASK-001, TASK-003 |
| ps-analyst | /problem-solving | Analyst -- effectiveness scoring methodology definition | TASK-002 |
| nse-qa | /nasa-se | Quality assurance -- comprehensive QA testing of all components | TASK-004 |
| ps-validator | /problem-solving | Validator -- end-to-end validation of complete metrics pipeline | TASK-005 |
| ps-critic | /problem-solving | Adversarial -- critique design, metric validity, and statistical assumptions | TASK-006 |

---

## Related Items

### Hierarchy

- **Parent Feature:** [FEAT-007: Advanced Adversarial Capabilities](../FEAT-007-advanced-adversarial-capabilities.md)

### Dependencies

| Type | Item | Description |
|------|------|-------------|
| depends_on | EN-602 | Effectiveness measurement research provides scoring methodology and statistical methods |
| related | EN-601 | Strategy selection research informs which metrics matter per strategy type |
| related | EN-603 | Metrics feed back into strategy selector to improve recommendations over time |
| related | EN-604 | Custom strategies must be tracked by effectiveness metrics after registration |
| related | FEAT-004 | Metrics apply to the foundational strategy catalog strategies |

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-12 | Claude | pending | Enabler created with 6-task decomposition. Infrastructure enabler for effectiveness metrics and A/B testing. Depends on EN-602 research completion. |
