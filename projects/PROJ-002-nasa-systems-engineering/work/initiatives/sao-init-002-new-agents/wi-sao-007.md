---
id: wi-sao-007
title: "Create ps-critic Agent"
status: COMPLETE
parent: "_index.md"
initiative: sao-init-002
children: []
depends_on: []
blocks:
  - wi-sao-014
created: "2026-01-11"
completed: "2026-01-11"
priority: "P1"
estimated_effort: "6h"
actual_effort: "4h"
entry_id: "sao-007"
source: "OPT-002"
belbin_role: "Monitor Evaluator"
risk_mitigation: "M-002 (circuit breaker)"
token_estimate: 800
---

# WI-SAO-007: Create ps-critic Agent

> **Status:** ✅ COMPLETE
> **Completed:** 2026-01-11
> **Priority:** HIGH (P1)

---

## Description

Create critic agent for quality evaluation and improvement feedback with circuit breaker.

---

## Acceptance Criteria

1. ✅ Agent definition follows PS_AGENT_TEMPLATE v2.0
2. ✅ Cognitive mode: convergent
3. ✅ Pairing with: ps-architect, ps-researcher (documented as orchestration guidance)
4. ✅ Output: Critique reports with improvement recommendations
5. ✅ max_iterations: 3, improvement_threshold: 0.10 (circuit breaker in orchestration_guidance)

---

## Artifacts Created

- `skills/problem-solving/agents/ps-critic.md` - 528 lines
- `skills/problem-solving/templates/critique.md` - Critique report template
- `skills/problem-solving/tests/BEHAVIOR_TESTS.md` - 11 BDD tests for ps-critic and generator-critic patterns

---

## Key Decisions

- Circuit breaker logic is orchestration guidance (MAIN CONTEXT manages loop)
- ps-critic does NOT self-manage iteration loops (P-003 compliant)
- Clear distinction from ps-reviewer: score-based vs. severity-based

---

## Tasks

- [x] **T-007.1:** Draft ps-critic.md agent definition
- [x] **T-007.2:** Define critique evaluation criteria (5 default + custom support)
- [x] **T-007.3:** Implement circuit breaker logic in orchestration_guidance section
- [x] **T-007.4:** Create BDD tests for generator-critic loops (11 tests)

---

*Source: Extracted from WORKTRACKER.md lines 1083-1113*
