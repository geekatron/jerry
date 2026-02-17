# EN-603: Automated Strategy Selector Implementation

<!--
TEMPLATE: Enabler
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.9
CREATED: 2026-02-12 (Claude)
PURPOSE: Implement the automated strategy selector that maps task characteristics to optimal adversarial strategies
-->

> **Type:** enabler
> **Status:** pending
> **Priority:** high
> **Impact:** high
> **Enabler Type:** architecture
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

Implement the automated strategy selector that maps task characteristics to optimal adversarial strategies. Design and build the context analysis engine, strategy recommendation algorithm, and integration points with /problem-solving and /nasa-se skills. This enabler translates the research findings from EN-601 into a working component that eliminates manual strategy selection.

**Value Proposition:**
- Eliminates guesswork in adversarial strategy selection by automating context-to-strategy mapping
- Provides consistent, reproducible strategy recommendations across all review invocations
- Integrates seamlessly with existing /problem-solving and /nasa-se skill workflows
- Supports extensibility as new strategies are added via EN-604 custom tooling
- Adds less than 1 second of latency to workflow invocation (NFC-9 from FEAT-007)

**Technical Scope:**
- Context analysis engine that extracts task characteristics (type, complexity, domain, risk)
- Strategy recommendation algorithm based on EN-601 research findings
- Integration adapters for /problem-solving and /nasa-se skill invocation paths
- Configuration-driven mapping rules with override capability
- Fallback strategy selection for unrecognized task contexts

---

## Problem Statement

With the foundational strategy catalog (FEAT-004) and strategy selection research (EN-601) complete, Jerry needs a concrete implementation that automatically selects the right adversarial strategy for each task. Without this automation:

1. **Manual selection is error-prone** -- Users must understand all available strategies and their applicability, which becomes impractical as the catalog grows.
2. **Inconsistent application** -- Different users select different strategies for identical tasks, undermining review quality consistency.
3. **No integration path** -- Skills like /problem-solving and /nasa-se have no programmatic way to request "the best strategy for this task."
4. **Scalability barrier** -- Adding new strategies (via EN-604) without automated selection means more strategies just creates more confusion.

The strategy selector must be deterministic, explainable (users can understand why a strategy was selected), and fast (< 1s latency addition to workflow invocation).

---

## Technical Approach

1. **Architecture Design** -- Design the strategy selector as a domain service following hexagonal architecture principles. Define ports for context analysis input and strategy recommendation output. Ensure the selector is testable in isolation from skill infrastructure.

2. **Context Analyzer Implementation** -- Build the context analysis engine that extracts task characteristics from the invocation context:
   - Task type classification (research, implementation, review, design, testing)
   - Complexity estimation (lines of code, number of components, dependency depth)
   - Domain detection (security, performance, correctness, usability)
   - Risk level assessment (based on component criticality and change scope)

3. **Recommendation Engine Implementation** -- Implement the strategy recommendation algorithm based on EN-601 research findings:
   - Rule-based mapping from task characteristics to strategy scores
   - Weighted scoring model for strategy ranking
   - Configurable mapping rules stored in YAML/JSON configuration
   - Fallback strategy for unrecognized contexts (default to Red Team + Devil's Advocate)

4. **Skill Integration** -- Create integration adapters for /problem-solving and /nasa-se:
   - Hook into skill invocation paths to inject strategy selection
   - Provide strategy recommendation as structured output (strategy name, confidence, rationale)
   - Support manual override (user can reject recommendation and choose manually)

5. **Code Review** -- Comprehensive code review by ps-reviewer covering architecture compliance, code quality, and integration correctness.

6. **Verification Testing** -- Verification testing by nse-verification to validate that the selector produces correct recommendations for known task/strategy pairings.

---

## Children (Tasks)

| ID | Title | Status | Activity | Agents |
|----|-------|--------|----------|--------|
| TASK-001 | Design strategy selector architecture (ports, adapters, domain service) | pending | DEVELOPMENT | ps-architect |
| TASK-002 | Implement context analyzer (task type, complexity, domain, risk extraction) | pending | DEVELOPMENT | ps-architect |
| TASK-003 | Implement recommendation engine (scoring, ranking, fallback) | pending | DEVELOPMENT | ps-architect |
| TASK-004 | Code review of selector implementation | pending | TESTING | ps-reviewer |
| TASK-005 | Verification testing of strategy selection accuracy | pending | TESTING | nse-verification |
| TASK-006 | Adversarial critique of design and implementation | pending | TESTING | ps-critic |

### Task Dependencies

```
TASK-001 (architecture design) ──> TASK-002 (context analyzer) ──┐
                                                                  ├──> TASK-004 (code review) ──> TASK-005 (verification)
                                   TASK-003 (recommendation engine)┘                              │
                                                                                                   v
                                                                                            TASK-006 (adversarial critique)
```

- TASK-001 must complete before TASK-002 and TASK-003 can begin
- TASK-002 and TASK-003 can execute in parallel after TASK-001
- TASK-004 requires both TASK-002 and TASK-003 to complete
- TASK-005 requires TASK-004 code review to pass
- TASK-006 applies adversarial critique after verification testing

---

## Acceptance Criteria

### Functional Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| AC-1 | Context analyzer extracts task type, complexity, domain, and risk from invocation context | [ ] |
| AC-2 | Recommendation engine produces ranked list of strategies with confidence scores | [ ] |
| AC-3 | Mapping rules are configuration-driven (YAML/JSON) and modifiable without code changes | [ ] |
| AC-4 | Fallback strategy is defined and applied when context is unrecognized | [ ] |
| AC-5 | Integration with /problem-solving skill invocation path is functional | [ ] |
| AC-6 | Integration with /nasa-se skill invocation path is functional | [ ] |
| AC-7 | Manual override capability allows users to reject recommendation | [ ] |
| AC-8 | Strategy selection rationale is explainable (user can see why a strategy was chosen) | [ ] |
| AC-9 | Code review passes with no critical findings | [ ] |
| AC-10 | Verification testing confirms correct recommendations for at least 10 known task/strategy pairings | [ ] |

### Non-Functional Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| NFC-1 | Strategy selection adds < 1s latency to workflow invocation | [ ] |
| NFC-2 | Implementation follows hexagonal architecture (domain service with ports) | [ ] |
| NFC-3 | All code has type hints and docstrings per coding standards | [ ] |
| NFC-4 | Unit test coverage >= 90% for selector components | [ ] |
| NFC-5 | No recursive subagent invocations (P-003 compliance) | [ ] |
| NFC-6 | Cross-platform compatibility (macOS, Windows, Linux) | [ ] |

---

## Agent Assignments

| Agent | Skill | Role | Phase |
|-------|-------|------|-------|
| ps-architect | /problem-solving | Creator -- architecture design and implementation | TASK-001, TASK-002, TASK-003 |
| ps-reviewer | /problem-solving | Reviewer -- code review for architecture compliance and quality | TASK-004 |
| nse-verification | /nasa-se | Verification -- validate selector produces correct recommendations | TASK-005 |
| ps-critic | /problem-solving | Adversarial -- critique design decisions and implementation quality | TASK-006 |

---

## Related Items

### Hierarchy

- **Parent Feature:** [FEAT-007: Advanced Adversarial Capabilities](../FEAT-007-advanced-adversarial-capabilities.md)

### Dependencies

| Type | Item | Description |
|------|------|-------------|
| depends_on | EN-601 | Research findings provide the basis for mapping rules and recommendation algorithm |
| related | EN-604 | Custom strategy tooling must integrate with the selector's strategy registry |
| related | EN-605 | Effectiveness metrics track selector recommendation accuracy over time |
| related | FEAT-004 | Uses the foundational strategy catalog as the strategy pool |
| related | FEAT-005 | Enforcement mechanisms provide hooks for selector integration |

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-12 | Claude | pending | Enabler created with 6-task decomposition. Implementation enabler for automated strategy selection. Depends on EN-601 research completion. |
