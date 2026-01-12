---
id: wi-sao-038
title: "Document 8 orchestration patterns in template"
status: OPEN
parent: "_index.md"
initiative: sao-init-007
children: []
depends_on: []
blocks:
  - wi-sao-033
  - wi-sao-041
created: "2026-01-12"
last_updated: "2026-01-12"
priority: P1
estimated_effort: "3h"
entry_id: sao-038
token_estimate: 600
---

# WI-SAO-038: Document 8 orchestration patterns in template

> **Status:** 📋 OPEN
> **Priority:** P1 (HIGH)
> **Blocks:** WI-SAO-033 (template), WI-SAO-041 (decision tree)

---

## Description

Ensure all 8 orchestration patterns identified in DISCOVERY-008 are fully documented with ASCII diagrams, use cases, agent mappings, and cognitive modes.

---

## 8 Patterns to Document

1. **Single Agent** - Direct invocation, no orchestration overhead
2. **Sequential Chain** - Order-dependent state passing
3. **Fan-Out** - Parallel independent execution
4. **Fan-In** - Output aggregation with sync barrier
5. **Cross-Pollinated Pipeline** - Bidirectional barriers for multi-track
6. **Divergent-Convergent (Diamond)** - Explore then converge
7. **Review Gate** - Quality checkpoint (SRR, PDR, CDR)
8. **Generator-Critic Loop** - Iterative refinement (max 3, threshold 0.85)

---

## Acceptance Criteria

1. [ ] Each pattern has ASCII topology diagram
2. [ ] Each pattern has "USE WHEN" section
3. [ ] Each pattern has agent mapping examples
4. [ ] Each pattern has cognitive mode declaration
5. [ ] Generator-Critic has circuit breaker parameters documented
6. [ ] Cross-Pollinated has barrier semantics documented

---

## Tasks

- [ ] **T-038.1:** Verify plan.md pattern catalog completeness
- [ ] **T-038.2:** Add missing details to any incomplete patterns
- [ ] **T-038.3:** Ensure ASCII diagrams are correct and readable
- [ ] **T-038.4:** Document circuit breaker (max_iterations: 3, threshold: 0.85)
- [ ] **T-038.5:** Document cross-skill handoff matrix

---

## Verification

| Evidence ID | Type | Description | Status |
|-------------|------|-------------|--------|
| E-038-001 | Content | 8 patterns in plan.md | ✅ Complete |
| E-038-002 | Content | ASCII diagrams for each | ✅ Complete |
| E-038-003 | Content | Circuit breaker documented | ✅ Complete |
| E-038-004 | Content | Cross-skill handoffs documented | ✅ Complete |

---

## Notes

Pattern documentation already exists in plan.md (DISCOVERY-008). This work item validates completeness and ensures integration into template.

---

*Source: SAO-INIT-007 plan.md Pattern Catalog section*
