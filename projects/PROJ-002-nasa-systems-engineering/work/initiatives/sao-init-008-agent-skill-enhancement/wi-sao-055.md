---
id: wi-sao-055
title: "Enhance ps-analyst Agent"
status: OPEN
parent: "_index.md"
initiative: sao-init-008
children: []
depends_on:
  - wi-sao-052
blocks:
  - wi-sao-066
created: "2026-01-12"
last_updated: "2026-01-12"
priority: P0
estimated_effort: "4-6h"
entry_id: sao-055
token_estimate: 600
---

# WI-SAO-055: Enhance ps-analyst Agent

> **Status:** 📋 OPEN
> **Priority:** P0 (CRITICAL - Core analysis capability)
> **Pipeline Pattern:** Pattern 8 (Generator-Critic Loop)

---

## Description

Enhance the ps-analyst agent definition using the Generator-Critic loop pattern. The analyst is responsible for converting research into actionable insights - quality here drives decision-making.

---

## Target File

`skills/problem-solving/agents/ps-analyst.md`

---

## Acceptance Criteria

1. [ ] Baseline rubric score recorded
2. [ ] Rubric score ≥0.85 achieved OR 3 iterations completed
3. [ ] Context engineering improvements applied
4. [ ] Role-Goal-Backstory enhanced (analysis specialist persona)
5. [ ] Analysis methodology guidance added/improved
6. [ ] L0/L1/L2 lens coverage verified
7. [ ] Changes committed

---

## Tasks

### T-055.1: Baseline Assessment

- [ ] **T-055.1.1:** Read current ps-analyst.md
- [ ] **T-055.1.2:** Score against rubric (record baseline)
- [ ] **T-055.1.3:** Identify specific enhancement opportunities
- [ ] **T-055.1.4:** Document baseline in work item

### T-055.2: Enhancement Iteration 1

- [ ] **T-055.2.1:** Apply context engineering improvements
- [ ] **T-055.2.2:** Enhance persona (analysis specialist)
- [ ] **T-055.2.3:** Add analysis methodology guidance (5 Whys, Fishbone, etc.)
- [ ] **T-055.2.4:** Add structured output format for findings
- [ ] **T-055.2.5:** Add L0/L1/L2 lens if missing
- [ ] **T-055.2.6:** Add orchestration metadata
  - state_output_key: "analysis_output"
  - cognitive_mode: "convergent"
  - next_hint: "ps-architect"
- [ ] **T-055.2.7:** Critique against rubric - record score

### T-055.3: Enhancement Iteration 2-3 (if needed)

- [ ] **T-055.3.1:** Address critique feedback
- [ ] **T-055.3.2:** Re-evaluate against rubric
- [ ] **T-055.3.3:** Continue until threshold or circuit breaker

### T-055.4: Commit

- [ ] **T-055.4.1:** Record final rubric score
- [ ] **T-055.4.2:** Document changes summary
- [ ] **T-055.4.3:** Commit enhanced agent

---

## Analysis-Specific Enhancements

### Analysis Methodology Section

- Root cause analysis techniques
- Trade-off analysis frameworks
- Gap analysis patterns
- Comparative analysis methods

### Output Structure

- Structured findings format
- Evidence-based conclusions
- Confidence levels
- Recommendations

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
| E-055-001 | Score | Baseline rubric score | ⏳ Pending |
| E-055-002 | Score | Final rubric score | ⏳ Pending |
| E-055-003 | Artifact | Enhanced ps-analyst.md | ⏳ Pending |
| E-055-004 | Commit | Changes committed | ⏳ Pending |

---

*Source: SAO-INIT-008 plan.md*
*Created: 2026-01-12*
