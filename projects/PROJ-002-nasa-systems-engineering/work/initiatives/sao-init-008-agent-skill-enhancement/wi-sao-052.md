---
id: wi-sao-052
title: "Create Enhancement Evaluation Rubric"
status: OPEN
parent: "_index.md"
initiative: sao-init-008
children: []
depends_on:
  - wi-sao-051
blocks:
  - wi-sao-053
  - wi-sao-054
  - wi-sao-055
  - wi-sao-056
  - wi-sao-057
  - wi-sao-058
  - wi-sao-059
  - wi-sao-060
  - wi-sao-061
  - wi-sao-062
  - wi-sao-063
  - wi-sao-064
  - wi-sao-065
created: "2026-01-12"
last_updated: "2026-01-12"
priority: P1
estimated_effort: "2-3h"
entry_id: sao-052
token_estimate: 500
---

# WI-SAO-052: Create Enhancement Evaluation Rubric

> **Status:** 📋 OPEN
> **Priority:** P1 (Phase 2 Analysis)
> **Pipeline Pattern:** Pattern 7 (Review Gate) - Gate Criteria Definition

---

## Description

Design the evaluation rubric that will be used to assess agent/skill quality during the Generator-Critic enhancement loop (Phase 3). The rubric defines dimensions, scoring scale, weights, and acceptance threshold (≥0.85).

---

## Acceptance Criteria

1. [ ] Rubric defined with ≥5 evaluation dimensions
2. [ ] Scoring scale defined (0.0-1.0)
3. [ ] Dimension weights defined
4. [ ] Scoring guide created with examples
5. [ ] Baseline scores recorded for 3 sample agents
6. [ ] Rubric validated to discriminate quality levels

---

## Tasks

### T-052.1: Rubric Design

- [ ] **T-052.1.1:** Define evaluation dimensions:
  - L0/L1/L2 Coverage
  - Persona Activation (Role-Goal-Backstory)
  - Context Engineering (Structure, Guardrails)
  - Orchestration Support (state_output_key, cognitive_mode)
  - Documentation Quality (Examples, Anti-patterns)
- [ ] **T-052.1.2:** Define scoring scale (0.0-1.0 per dimension)
- [ ] **T-052.1.3:** Define weighting per dimension
- [ ] **T-052.1.4:** Define acceptance threshold (≥0.85 weighted average)

### T-052.2: Rubric Documentation

- [ ] **T-052.2.1:** Create rubric template for evaluators
- [ ] **T-052.2.2:** Create scoring guide with examples per dimension
- [ ] **T-052.2.3:** Create calculator for weighted score
- [ ] **T-052.2.4:** Document in `analysis/sao-052-rubric.md`

### T-052.3: Baseline Scoring

- [ ] **T-052.3.1:** Score ps-researcher.md using rubric (baseline)
- [ ] **T-052.3.2:** Score nse-requirements.md using rubric (baseline)
- [ ] **T-052.3.3:** Score orchestrator.md using rubric (baseline)
- [ ] **T-052.3.4:** Document baseline scores
- [ ] **T-052.3.5:** Validate rubric discriminates quality levels

---

## Proposed Rubric Dimensions

| Dimension | Weight | Description |
|-----------|--------|-------------|
| L0/L1/L2 Coverage | 20% | Does agent have all three lens levels? |
| Persona Activation | 20% | Role, Goal, Backstory quality |
| Context Engineering | 25% | Structure, Guardrails, Examples |
| Orchestration Support | 15% | state_output_key, cognitive_mode, next_hint |
| Documentation Quality | 20% | Clarity, completeness, anti-patterns |

### Scoring Guide (per dimension)

| Score | Description |
|-------|-------------|
| 0.0-0.2 | Missing or severely deficient |
| 0.3-0.4 | Present but incomplete |
| 0.5-0.6 | Adequate but room for improvement |
| 0.7-0.8 | Good quality, minor gaps |
| 0.9-1.0 | Excellent, exemplary quality |

### Acceptance Threshold

```
weighted_score = sum(dimension_score * weight) / sum(weights)

IF weighted_score >= 0.85:
    ACCEPT
ELSE:
    ITERATE (max 3 times)
```

---

## Expected Outputs

| Artifact | Location | Description |
|----------|----------|-------------|
| Rubric definition | `analysis/sao-052-rubric.md` | Dimensions, weights, scale |
| Scoring template | `analysis/sao-052-scoring-template.md` | Evaluator template |
| Baseline scores | `analysis/sao-052-baseline-scores.md` | 3 sample agent scores |

---

## Verification

| Evidence ID | Type | Description | Status |
|-------------|------|-------------|--------|
| E-052-001 | Design | ≥5 dimensions defined | ⏳ Pending |
| E-052-002 | Design | Scoring guide created | ⏳ Pending |
| E-052-003 | Test | Baseline scores recorded | ⏳ Pending |
| E-052-004 | Test | Rubric discriminates quality | ⏳ Pending |

---

*Source: SAO-INIT-008 plan.md*
*Created: 2026-01-12*
