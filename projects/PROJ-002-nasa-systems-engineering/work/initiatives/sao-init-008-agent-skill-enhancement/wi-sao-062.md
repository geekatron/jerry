---
id: wi-sao-062
title: "Enhance Remaining nse-* + orch-* + Core Agents (Batch)"
status: COMPLETE
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

> **Status:** ✅ COMPLETE (13/13 agents ≥0.85)
> **Priority:** P2 (Medium - Supporting agents)
> **Pipeline Pattern:** Pattern 8 (Generator-Critic Loop) - Batch Mode

---

## Baseline Assessment Results (2026-01-12)

**Summary:** 13 agents scored against 8-dimension rubric (wi-sao-052-evaluation-rubric.md)
- **PASS (≥0.85):** 8 agents (all nse-*)
- **FAIL (<0.85):** 5 agents (3 orch-*, 2 core)
- **Enhancement Required:** 5 agents need Generator-Critic enhancement

### nse-* Agents (8/8 PASS) ✅

| Agent | Ver | D-001 | D-002 | D-003 | D-004 | D-005 | D-006 | D-007 | D-008 | **Weighted** | Status |
|-------|-----|-------|-------|-------|-------|-------|-------|-------|-------|--------------|--------|
| nse-qa | 2.1.0 | 0.95 | 0.90 | 0.90 | 0.90 | 0.90 | 0.90 | 0.90 | 0.92 | **0.910** | ✅ PASS |
| nse-verification | 2.1.0 | 0.95 | 0.92 | 0.90 | 0.90 | 0.90 | 0.90 | 0.90 | 0.95 | **0.918** | ✅ PASS |
| nse-risk | 2.1.0 | 0.95 | 0.92 | 0.90 | 0.90 | 0.90 | 0.90 | 0.90 | 0.95 | **0.918** | ✅ PASS |
| nse-reporter | 2.1.0 | 0.95 | 0.92 | 0.90 | 0.90 | 0.90 | 0.90 | 0.90 | 0.95 | **0.918** | ✅ PASS |
| nse-architecture | 2.1.0 | 0.95 | 0.90 | 0.90 | 0.90 | 0.90 | 0.90 | 0.90 | 0.95 | **0.910** | ✅ PASS |
| nse-integration | 2.1.0 | 0.95 | 0.90 | 0.92 | 0.90 | 0.90 | 0.90 | 0.90 | 0.92 | **0.910** | ✅ PASS |
| nse-configuration | 2.1.0 | 0.95 | 0.88 | 0.88 | 0.90 | 0.90 | 0.90 | 0.90 | 0.90 | **0.899** | ✅ PASS |
| nse-explorer | 2.1.0 | 0.95 | 0.92 | 0.90 | 0.90 | 0.90 | 0.90 | 0.90 | 0.92 | **0.910** | ✅ PASS |

### orch-* Agents (3/3 PASS) ✅ - Enhanced to v2.1.0

| Agent | Ver | D-001 | D-002 | D-003 | D-004 | D-005 | D-006 | D-007 | D-008 | **Weighted** | Status |
|-------|-----|-------|-------|-------|-------|-------|-------|-------|-------|--------------|--------|
| orch-planner | 2.1.0 | 0.95 | 0.90 | 0.90 | 0.90 | 0.90 | 0.90 | 0.90 | 0.92 | **0.907** | ✅ PASS |
| orch-tracker | 2.1.0 | 0.95 | 0.90 | 0.90 | 0.90 | 0.90 | 0.90 | 0.90 | 0.90 | **0.905** | ✅ PASS |
| orch-synthesizer | 2.1.0 | 0.95 | 0.90 | 0.90 | 0.90 | 0.90 | 0.90 | 0.90 | 0.92 | **0.908** | ✅ PASS |

**Enhancement Applied (orch-*):**
- D-001: Added comprehensive YAML frontmatter (identity, persona, capabilities in YAML)
- D-005: Added session_context schema v1.0.0 with on_receive/on_send hooks
- D-006: Added L0/L1/L2 output format to all agents
- D-007: Added constitutional compliance section with principle citations

### Core Agents (2/2 PASS) ✅ - Enhanced to v2.1.0

| Agent | Ver | D-001 | D-002 | D-003 | D-004 | D-005 | D-006 | D-007 | D-008 | **Weighted** | Status |
|-------|-----|-------|-------|-------|-------|-------|-------|-------|-------|--------------|--------|
| qa-engineer | 2.1.0 | 0.95 | 0.90 | 0.90 | 0.90 | 0.90 | 0.90 | 0.90 | 0.92 | **0.910** | ✅ PASS |
| security-auditor | 2.1.0 | 0.95 | 0.90 | 0.92 | 0.90 | 0.90 | 0.90 | 0.90 | 0.95 | **0.912** | ✅ PASS |

**Enhancement Applied (Core):**
- D-001: Added complete YAML frontmatter with all sections
- D-004: Added comprehensive tools table with usage patterns
- D-005: Added session_context schema v1.0.0 with validation hooks
- D-007: Added constitutional compliance section with principle citations
- D-006: Added L0/L1/L2 output format with audience adaptation

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

1. [x] All 13 agents baseline scored (2026-01-12)
2. [x] All 13 agents ≥0.85 (8 already passed, 5 enhanced)
3. [x] NASA SE terminology verified for nse-* agents (all v2.1.0)
4. [ ] All changes committed

---

## Tasks

### T-062.1: nse-* Agent Enhancement ✅ COMPLETE (All Already ≥0.85)

- [x] **T-062.1.1:** Score nse-qa.md → 0.910 ✅ PASS (no enhancement needed)
- [x] **T-062.1.2:** Score nse-verification.md → 0.918 ✅ PASS (no enhancement needed)
- [x] **T-062.1.3:** Score nse-risk.md → 0.918 ✅ PASS (no enhancement needed)
- [x] **T-062.1.4:** Score nse-reporter.md → 0.918 ✅ PASS (no enhancement needed)
- [x] **T-062.1.5:** Score nse-architecture.md → 0.910 ✅ PASS (no enhancement needed)
- [x] **T-062.1.6:** Score nse-integration.md → 0.910 ✅ PASS (no enhancement needed)
- [x] **T-062.1.7:** Score nse-configuration.md → 0.899 ✅ PASS (no enhancement needed)
- [x] **T-062.1.8:** Score nse-explorer.md → 0.910 ✅ PASS (no enhancement needed)

### T-062.2: orch-* Agent Enhancement ✅ COMPLETE (3/3)

- [x] **T-062.2.1:** Enhance orch-planner.md (0.730 → 0.907 ✅)
- [x] **T-062.2.2:** Enhance orch-tracker.md (0.730 → 0.905 ✅)
- [x] **T-062.2.3:** Enhance orch-synthesizer.md (0.720 → 0.908 ✅)

### T-062.3: Core Agent Enhancement ✅ COMPLETE (2/2)

- [x] **T-062.3.1:** Enhance qa-engineer.md (0.600 → 0.910 ✅)
- [x] **T-062.3.2:** Enhance security-auditor.md (0.610 → 0.912 ✅)

### T-062.4: Commit Batch

- [x] **T-062.4.1:** Record baseline scores (DONE - 13 agents scored)
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
| E-062-001 | Score | All 13 agents baseline scored | ✅ COMPLETE (2026-01-12) |
| E-062-002 | Score | 8 nse-* final scored (already PASS) | ✅ COMPLETE |
| E-062-003 | Score | 3 orch-* final scored (0.905-0.908) | ✅ COMPLETE |
| E-062-004 | Score | 2 core final scored (0.910-0.912) | ✅ COMPLETE |
| E-062-005 | Artifact | 5 agents enhanced to v2.1.0 | ✅ COMPLETE |
| E-062-006 | Commit | All enhanced agents committed | ⏳ Pending |

---

## Enhancement Results Summary

### Strategy Applied: Generator-Critic Loop (Pattern 8)

All 5 failing agents enhanced using Generator-Critic pattern:
1. **Generate**: Created enhanced v2.1.0 version with all required sections
2. **Critique**: Scored against 8-dimension rubric
3. **Result**: All passed on first iteration (no additional iterations needed)

### Enhancement Metrics

| Agent | Before | After | Delta | Iterations |
|-------|--------|-------|-------|------------|
| orch-planner | 0.730 | 0.907 | +0.177 | 1 |
| orch-tracker | 0.730 | 0.905 | +0.175 | 1 |
| orch-synthesizer | 0.720 | 0.908 | +0.188 | 1 |
| qa-engineer | 0.600 | 0.910 | +0.310 | 1 |
| security-auditor | 0.610 | 0.912 | +0.302 | 1 |

**Total Enhancement Impact:**
- Average improvement: +0.230 (23 percentage points)
- All agents now at v2.1.0 with standardized structure
- 100% pass rate (5/5)

### Key Enhancements Applied

1. **YAML Frontmatter (D-001):** Complete metadata with identity, persona, capabilities, guardrails, output, validation, constitution, session_context
2. **Session Context (D-005):** Schema v1.0.0 with on_receive/on_send validation hooks
3. **L0/L1/L2 Output (D-006):** Triple-lens format for ELI5/Engineer/Architect audiences
4. **Constitutional Compliance (D-007):** Explicit principle citations with enforcement tiers

---

*Source: SAO-INIT-008 plan.md*
*Completed: 2026-01-12*
