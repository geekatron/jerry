---
id: wi-sao-062
title: "Enhance Remaining nse-* + orch-* + Core Agents (Batch)"
status: OPEN
parent: "_index.md"
initiative: sao-init-008
children: []
depends_on:
  - wi-sao-060
blocks:
  - wi-sao-066
created: "2026-01-12"
last_updated: "2026-01-12"
priority: P2
estimated_effort: "12-16h"
entry_id: sao-062
token_estimate: 800
---

# WI-SAO-062: Enhance Remaining nse-* + orch-* + Core Agents (Batch)

> **Status:** 📋 OPEN
> **Priority:** P2 (Medium - Supporting agents)
> **Pipeline Pattern:** Pattern 8 (Generator-Critic Loop) - Batch Mode

---

## Description

Batch enhancement of remaining nse-* agents, orch-* agents, and core agents (.claude/agents/). These complete the agent ecosystem.

---

## Target Files

### nse-* Agents (8)

1. `skills/nasa-se/agents/nse-qa.md`
2. `skills/nasa-se/agents/nse-verification.md`
3. `skills/nasa-se/agents/nse-risk.md`
4. `skills/nasa-se/agents/nse-reporter.md`
5. `skills/nasa-se/agents/nse-architecture.md`
6. `skills/nasa-se/agents/nse-integration.md`
7. `skills/nasa-se/agents/nse-configuration.md`
8. `skills/nasa-se/agents/nse-explorer.md`

### orch-* Agents (3)

9. `skills/orchestration/agents/orch-planner.md`
10. `skills/orchestration/agents/orch-tracker.md`
11. `skills/orchestration/agents/orch-synthesizer.md`

### Core Agents (2)

12. `.claude/agents/qa-engineer.md`
13. `.claude/agents/security-auditor.md`

---

## Acceptance Criteria

1. [ ] All 13 agents baseline scored
2. [ ] All 13 agents enhanced (≥0.85 or 3 iterations)
3. [ ] NASA SE terminology verified for nse-* agents
4. [ ] All changes committed

---

## Tasks

### T-062.1: nse-* Agent Enhancement

- [ ] **T-062.1.1:** Enhance nse-qa.md
- [ ] **T-062.1.2:** Enhance nse-verification.md
- [ ] **T-062.1.3:** Enhance nse-risk.md
- [ ] **T-062.1.4:** Enhance nse-reporter.md
- [ ] **T-062.1.5:** Enhance nse-architecture.md
- [ ] **T-062.1.6:** Enhance nse-integration.md
- [ ] **T-062.1.7:** Enhance nse-configuration.md
- [ ] **T-062.1.8:** Enhance nse-explorer.md

### T-062.2: orch-* Agent Enhancement

- [ ] **T-062.2.1:** Enhance orch-planner.md
- [ ] **T-062.2.2:** Enhance orch-tracker.md
- [ ] **T-062.2.3:** Enhance orch-synthesizer.md

### T-062.3: Core Agent Enhancement

- [ ] **T-062.3.1:** Enhance qa-engineer.md
- [ ] **T-062.3.2:** Enhance security-auditor.md

### T-062.4: Commit Batch

- [ ] **T-062.4.1:** Record final scores
- [ ] **T-062.4.2:** Commit all enhanced agents

---

## nse-* Orchestration Metadata Reference

| Agent | state_output_key | cognitive_mode | next_hint |
|-------|------------------|----------------|-----------|
| nse-qa | qa_output | convergent | nse-reporter |
| nse-verification | verification_output | convergent | nse-reviewer |
| nse-risk | risk_output | convergent | nse-reviewer |
| nse-reporter | report_output | convergent | (terminal) |
| nse-architecture | architecture_output | divergent | nse-integration |
| nse-integration | integration_output | convergent | nse-verification |
| nse-configuration | configuration_output | convergent | nse-qa |
| nse-explorer | exploration_output | divergent | (context-dependent) |

---

## Verification

| Evidence ID | Type | Description | Status |
|-------------|------|-------------|--------|
| E-062-001 | Score | All 13 agents baseline scored | ⏳ Pending |
| E-062-002 | Score | All 13 agents final scored | ⏳ Pending |
| E-062-003 | Artifact | All 13 agents enhanced | ⏳ Pending |

---

*Source: SAO-INIT-008 plan.md*
