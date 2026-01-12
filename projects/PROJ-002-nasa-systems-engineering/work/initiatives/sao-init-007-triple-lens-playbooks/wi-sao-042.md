---
id: wi-sao-042
title: "Research & document Generator-Critic patterns"
status: OPEN
parent: "_index.md"
initiative: sao-init-007
children: []
depends_on: []
blocks:
  - wi-sao-043
  - wi-sao-045
created: "2026-01-12"
last_updated: "2026-01-12"
priority: P1
estimated_effort: "4h"
entry_id: sao-042
token_estimate: 600
---

# WI-SAO-042: Research & Document Generator-Critic Patterns

> **Status:** 📋 OPEN
> **Priority:** P1 (HIGH - Critical gap)
> **Blocks:** WI-SAO-043, WI-SAO-045

---

## Description

The problem-solving PLAYBOOK.md is missing documentation for the Generator-Critic pattern and ps-critic agent integration. This is a critical gap because:

1. ps-critic exists (v2.1.0) but is not documented in the playbook
2. Feedback loop patterns are referenced but not explained
3. Users don't know WHEN or HOW to use critic in conjunction with other agents

**Approach:** Use ps-* agents themselves to research and document this pattern (dogfooding).

---

## Acceptance Criteria

1. [ ] Generator-Critic pattern fully documented in problem-solving PLAYBOOK.md
2. [ ] ps-critic agent role and capabilities explained
3. [ ] Workflow diagrams (ASCII + Mermaid) showing critic integration
4. [ ] Decision guide: When to use critic vs other agents
5. [ ] At least 3 complete examples of generator-critic workflows
6. [ ] Anti-patterns documented (L2)

---

## Tasks

### T-042.1: Research Phase (ps-researcher)
- [ ] **T-042.1.1:** Invoke ps-researcher to gather information about generator-critic patterns
- [ ] **T-042.1.2:** Research industry best practices (Google ADK, LangChain, etc.)
- [ ] **T-042.1.3:** Document ps-critic agent capabilities from agent definition
- [ ] **T-042.1.4:** Create research artifact: `research/sao-042-generator-critic-research.md`

### T-042.2: Analysis Phase (ps-analyst)
- [ ] **T-042.2.1:** Invoke ps-analyst to analyze when generator-critic is appropriate
- [ ] **T-042.2.2:** Create decision matrix: critic vs validator vs reviewer
- [ ] **T-042.2.3:** Identify optimal workflow compositions
- [ ] **T-042.2.4:** Create analysis artifact: `analysis/sao-042-generator-critic-analysis.md`

### T-042.3: Critique Phase (ps-critic)
- [ ] **T-042.3.1:** Invoke ps-critic to review research and analysis
- [ ] **T-042.3.2:** Identify gaps or issues in proposed documentation
- [ ] **T-042.3.3:** Iterate until critique passes
- [ ] **T-042.3.4:** Document critique findings

### T-042.4: Documentation Phase
- [ ] **T-042.4.1:** Update problem-solving PLAYBOOK.md with L0 (ELI5) section
- [ ] **T-042.4.2:** Update problem-solving PLAYBOOK.md with L1 (Engineer) section
- [ ] **T-042.4.3:** Update problem-solving PLAYBOOK.md with L2 (Architect) section
- [ ] **T-042.4.4:** Add ASCII workflow diagrams
- [ ] **T-042.4.5:** Add Mermaid workflow diagrams
- [ ] **T-042.4.6:** Update ORCHESTRATION_PATTERNS.md Pattern 8 if needed

---

## Verification

| Evidence ID | Type | Description | Status |
|-------------|------|-------------|--------|
| E-042-001 | Research | ps-researcher artifact created | ⏳ |
| E-042-002 | Analysis | ps-analyst artifact created | ⏳ |
| E-042-003 | Critique | ps-critic passed | ⏳ |
| E-042-004 | Content | PLAYBOOK.md updated with generator-critic | ⏳ |
| E-042-005 | Diagram | ASCII + Mermaid workflows present | ⏳ |

---

## Research Questions

1. What distinguishes ps-critic from ps-validator and ps-reviewer?
2. When should a user choose generator-critic over sequential chain?
3. What are the circuit breaker conditions (max iterations, no improvement)?
4. How does the feedback loop integrate with state management?
5. What are common failure modes and how to avoid them?

---

## Context from ps-critic Agent Definition

```yaml
# From skills/problem-solving/agents/ps-critic.md
name: ps-critic
version: "2.1.0"
cognitive_mode: "convergent"
Output Key: critic_output

# Circuit Breaker Parameters (from agent definition)
- max_iterations: 5 (default)
- min_improvement_threshold: 0.1
- no_improvement_window: 2
```

---

*Source: DISCOVERY-012 (GAP-012-001, GAP-012-002)*
*Created: 2026-01-12*
