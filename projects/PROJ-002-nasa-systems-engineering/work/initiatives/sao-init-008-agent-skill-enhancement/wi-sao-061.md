---
id: wi-sao-061
title: "Enhance Remaining ps-* Agents (Batch)"
status: OPEN
parent: "_index.md"
initiative: sao-init-008
children: []
depends_on:
  - wi-sao-056
blocks:
  - wi-sao-066
created: "2026-01-12"
last_updated: "2026-01-12"
priority: P2
estimated_effort: "8-12h"
entry_id: sao-061
token_estimate: 700
---

# WI-SAO-061: Enhance Remaining ps-* Agents (Batch)

> **Status:** 📋 OPEN
> **Priority:** P2 (Medium - Supporting agents)
> **Pipeline Pattern:** Pattern 8 (Generator-Critic Loop) - Batch Mode

---

## Description

Batch enhancement of remaining ps-* agents using the same Generator-Critic methodology. These are supporting agents that complete the problem-solving pipeline.

---

## Target Files

1. `skills/problem-solving/agents/ps-validator.md`
2. `skills/problem-solving/agents/ps-reviewer.md`
3. `skills/problem-solving/agents/ps-reporter.md`
4. `skills/problem-solving/agents/ps-investigator.md`

---

## Acceptance Criteria

1. [ ] All 4 agents baseline scored
2. [ ] All 4 agents enhanced (≥0.85 or 3 iterations)
3. [ ] All changes committed

---

## Tasks

### T-061.1: ps-validator Enhancement

- [ ] **T-061.1.1:** Baseline assessment
- [ ] **T-061.1.2:** Apply enhancement template
- [ ] **T-061.1.3:** Add orchestration metadata
  - state_output_key: "validation_output"
  - cognitive_mode: "convergent"
  - next_hint: "ps-synthesizer"
- [ ] **T-061.1.4:** Score and iterate

### T-061.2: ps-reviewer Enhancement

- [ ] **T-061.2.1:** Baseline assessment
- [ ] **T-061.2.2:** Apply enhancement template
- [ ] **T-061.2.3:** Add orchestration metadata
  - state_output_key: "review_output"
  - cognitive_mode: "convergent"
  - next_hint: "(conditional)"
- [ ] **T-061.2.4:** Score and iterate

### T-061.3: ps-reporter Enhancement

- [ ] **T-061.3.1:** Baseline assessment
- [ ] **T-061.3.2:** Apply enhancement template
- [ ] **T-061.3.3:** Add orchestration metadata
  - state_output_key: "report_output"
  - cognitive_mode: "convergent"
  - next_hint: "(terminal)"
- [ ] **T-061.3.4:** Score and iterate

### T-061.4: ps-investigator Enhancement

- [ ] **T-061.4.1:** Baseline assessment
- [ ] **T-061.4.2:** Apply enhancement template
- [ ] **T-061.4.3:** Add orchestration metadata
  - state_output_key: "investigation_output"
  - cognitive_mode: "divergent"
  - next_hint: "ps-analyst"
- [ ] **T-061.4.4:** Score and iterate

### T-061.5: Commit Batch

- [ ] **T-061.5.1:** Record final scores
- [ ] **T-061.5.2:** Commit all enhanced agents

---

## Verification

| Evidence ID | Type | Description | Status |
|-------------|------|-------------|--------|
| E-061-001 | Score | All 4 agents baseline scored | ⏳ Pending |
| E-061-002 | Score | All 4 agents final scored | ⏳ Pending |
| E-061-003 | Artifact | All 4 agents enhanced | ⏳ Pending |

---

*Source: SAO-INIT-008 plan.md*
