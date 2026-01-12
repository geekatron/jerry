---
id: wi-sao-053
title: "Enhance orchestrator Agent"
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
entry_id: sao-053
token_estimate: 600
---

# WI-SAO-053: Enhance orchestrator Agent

> **Status:** 📋 OPEN
> **Priority:** P0 (CRITICAL - Most used agent)
> **Pipeline Pattern:** Pattern 8 (Generator-Critic Loop)

---

## Description

Enhance the orchestrator agent definition using the Generator-Critic loop pattern. Apply context engineering best practices, improve persona activation, and ensure compliance with standards. Use the rubric to measure quality with circuit breaker (max 3 iterations, threshold ≥0.85).

---

## Target File

`.claude/agents/orchestrator.md`

---

## Acceptance Criteria

1. [ ] Baseline rubric score recorded
2. [ ] Rubric score ≥0.85 achieved OR 3 iterations completed
3. [ ] Context engineering improvements applied
4. [ ] Role-Goal-Backstory enhanced
5. [ ] Guardrails section complete
6. [ ] L0/L1/L2 lens coverage verified
7. [ ] Changes committed

---

## Tasks

### T-053.1: Baseline Assessment

- [ ] **T-053.1.1:** Read current orchestrator.md
- [ ] **T-053.1.2:** Score against rubric (record baseline)
- [ ] **T-053.1.3:** Identify specific enhancement opportunities
- [ ] **T-053.1.4:** Document baseline in work item

### T-053.2: Enhancement Iteration 1

- [ ] **T-053.2.1:** Apply context engineering improvements
  - Add/improve `<identity>` section
  - Add/improve `<capabilities>` section
  - Add/improve `<instructions>` section
  - Add/improve `<guardrails>` section
  - Add/improve `<output_format>` section
  - Add/improve `<examples>` section
- [ ] **T-053.2.2:** Enhance Role-Goal-Backstory
- [ ] **T-053.2.3:** Add/improve L0/L1/L2 lens coverage
- [ ] **T-053.2.4:** Add orchestration metadata (state_output_key, cognitive_mode)
- [ ] **T-053.2.5:** Critique against rubric - record score

### T-053.3: Enhancement Iteration 2-3 (if needed)

- [ ] **T-053.3.1:** Address critique feedback from iteration 1
- [ ] **T-053.3.2:** Re-evaluate against rubric
- [ ] **T-053.3.3:** Continue until threshold (0.85) or circuit breaker (3 iterations)

### T-053.4: Commit

- [ ] **T-053.4.1:** Record final rubric score
- [ ] **T-053.4.2:** Document changes summary
- [ ] **T-053.4.3:** Commit enhanced agent

---

## Generator-Critic Loop Configuration

```yaml
circuit_breaker:
  max_iterations: 3
  acceptance_threshold: 0.85
  improvement_threshold: 0.10  # Min improvement per iteration
  escalation: human_review     # After 3 fails
```

---

## Enhancement Checklist

### Structure

- [ ] Identity Section (role, expertise)
- [ ] Capabilities Section (tools, agents)
- [ ] Instructions Section (step-by-step)
- [ ] Guardrails Section (non-negotiables)
- [ ] Output Format Section (structure)
- [ ] Examples Section (demonstrations)

### Content

- [ ] L0 (ELI5) - Metaphor explaining what/why
- [ ] L1 (Engineer) - Technical how-to
- [ ] L2 (Architect) - Constraints, boundaries, anti-patterns
- [ ] State Output Key defined
- [ ] Cognitive Mode declared
- [ ] Next Hint (suggested next agent)

### Compliance

- [ ] P-003 compliant (no recursive subagents)
- [ ] Anthropic best practices followed
- [ ] XML/Markdown structure appropriate

---

## Iteration Log

| Iteration | Score | Notes | Action |
|-----------|-------|-------|--------|
| Baseline | TBD | Initial score | Identify gaps |
| 1 | TBD | First enhancement | Apply improvements |
| 2 | TBD | Second enhancement (if needed) | Address feedback |
| 3 | TBD | Final attempt (if needed) | Final refinement |

---

## Verification

| Evidence ID | Type | Description | Status |
|-------------|------|-------------|--------|
| E-053-001 | Score | Baseline rubric score | ⏳ Pending |
| E-053-002 | Score | Final rubric score | ⏳ Pending |
| E-053-003 | Artifact | Enhanced orchestrator.md | ⏳ Pending |
| E-053-004 | Commit | Changes committed | ⏳ Pending |

---

*Source: SAO-INIT-008 plan.md*
*Created: 2026-01-12*
