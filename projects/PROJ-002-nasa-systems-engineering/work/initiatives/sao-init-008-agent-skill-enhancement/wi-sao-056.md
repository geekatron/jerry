---
id: wi-sao-056
title: "Enhance ps-critic Agent"
status: OPEN
parent: "_index.md"
initiative: sao-init-008
children: []
depends_on:
  - wi-sao-052
blocks:
  - wi-sao-061
  - wi-sao-066
created: "2026-01-12"
last_updated: "2026-01-12"
priority: P0
estimated_effort: "4-6h"
entry_id: sao-056
token_estimate: 600
---

# WI-SAO-056: Enhance ps-critic Agent

> **Status:** 📋 OPEN
> **Priority:** P0 (CRITICAL - Quality gatekeeper for Generator-Critic)
> **Pipeline Pattern:** Pattern 8 (Generator-Critic Loop)

---

## Description

Enhance the ps-critic agent definition using the Generator-Critic loop pattern. The critic is essential for Pattern 8 (Generator-Critic Loop) - it evaluates generator output and provides actionable feedback for refinement.

---

## Target File

`skills/problem-solving/agents/ps-critic.md`

---

## Acceptance Criteria

1. [ ] Baseline rubric score recorded
2. [ ] Rubric score ≥0.85 achieved OR 3 iterations completed
3. [ ] Context engineering improvements applied
4. [ ] Role-Goal-Backstory enhanced (critical evaluator persona)
5. [ ] Scoring methodology documented
6. [ ] Circuit breaker awareness added
7. [ ] L0/L1/L2 lens coverage verified
8. [ ] Changes committed

---

## Tasks

### T-056.1: Baseline Assessment

- [ ] **T-056.1.1:** Read current ps-critic.md
- [ ] **T-056.1.2:** Score against rubric (record baseline)
- [ ] **T-056.1.3:** Identify specific enhancement opportunities
- [ ] **T-056.1.4:** Document baseline in work item

### T-056.2: Enhancement Iteration 1

- [ ] **T-056.2.1:** Apply context engineering improvements
- [ ] **T-056.2.2:** Enhance persona (critical evaluator, not adversarial)
- [ ] **T-056.2.3:** Add scoring methodology (0.0-1.0 scale)
- [ ] **T-056.2.4:** Add feedback structure (specific, actionable)
- [ ] **T-056.2.5:** Add circuit breaker awareness
- [ ] **T-056.2.6:** Add L0/L1/L2 lens if missing
- [ ] **T-056.2.7:** Add orchestration metadata
  - state_output_key: "critique_output"
  - cognitive_mode: "convergent"
  - next_hint: "(generator)" - returns to generator
- [ ] **T-056.2.8:** Critique against rubric - record score

### T-056.3: Enhancement Iteration 2-3 (if needed)

- [ ] **T-056.3.1:** Address critique feedback
- [ ] **T-056.3.2:** Re-evaluate against rubric
- [ ] **T-056.3.3:** Continue until threshold or circuit breaker

### T-056.4: Commit

- [ ] **T-056.4.1:** Record final rubric score
- [ ] **T-056.4.2:** Document changes summary
- [ ] **T-056.4.3:** Commit enhanced agent

---

## Critic-Specific Enhancements

### Scoring Methodology Section

```yaml
output_format:
  score: 0.0-1.0  # Overall quality score
  dimensions:
    - name: "Completeness"
      score: 0.0-1.0
      feedback: "..."
    - name: "Accuracy"
      score: 0.0-1.0
      feedback: "..."
    - name: "Clarity"
      score: 0.0-1.0
      feedback: "..."
  recommendations:
    - priority: HIGH
      action: "..."
    - priority: MEDIUM
      action: "..."
  iteration_guidance: "..."  # For generator to improve
```

### Circuit Breaker Awareness

- Recognize iteration count context
- Provide diminishing returns signal
- Know when to recommend escalation

---

## Iteration Log

| Iteration | Score | Notes | Action |
|-----------|-------|-------|--------|
| Baseline | TBD | Initial score | Identify gaps |
| 1 | TBD | First enhancement | Apply improvements |
| 2 | TBD | If needed | Address feedback |
| 3 | TBD | If needed | Final refinement |

---

## Verification

| Evidence ID | Type | Description | Status |
|-------------|------|-------------|--------|
| E-056-001 | Score | Baseline rubric score | ⏳ Pending |
| E-056-002 | Score | Final rubric score | ⏳ Pending |
| E-056-003 | Artifact | Enhanced ps-critic.md | ⏳ Pending |
| E-056-004 | Commit | Changes committed | ⏳ Pending |

---

*Source: SAO-INIT-008 plan.md*
*Created: 2026-01-12*
