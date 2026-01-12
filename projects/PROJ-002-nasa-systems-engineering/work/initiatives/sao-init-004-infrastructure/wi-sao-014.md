---
id: wi-sao-014
title: "Implement Generator-Critic Loops"
status: OPEN
parent: "_index.md"
initiative: sao-init-004
children: []
depends_on:
  - "../sao-init-002-new-agents/wi-sao-007.md"
blocks: []
created: "2026-01-10"
priority: "P1"
estimated_effort: "8h"
entry_id: "sao-014"
source: "OPT-002, Trade Study TS-5"
risk_mitigation: "M-002 (circuit breaker)"
token_estimate: 500
---

# WI-SAO-014: Implement Generator-Critic Loops

> **Status:** OPEN
> **Priority:** HIGH (P1)

---

## Description

Implement paired agent generator-critic iteration with circuit breaker.

---

## Acceptance Criteria

1. max_iterations: 3
2. improvement_threshold: 0.10
3. circuit_breaker: consecutive_failures: 2
4. Logging of all iterations

---

## Tasks

- [ ] **T-014.1:** Design generator-critic protocol
- [ ] **T-014.2:** Implement iteration controller
- [ ] **T-014.3:** Implement improvement measurement
- [ ] **T-014.4:** Add circuit breaker logic
- [ ] **T-014.5:** Create BDD tests for quality loops

---

*Source: Extracted from WORKTRACKER.md lines 1622-1641*
