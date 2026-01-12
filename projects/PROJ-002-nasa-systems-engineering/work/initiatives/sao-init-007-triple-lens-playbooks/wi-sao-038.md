---
id: wi-sao-038
title: "Document 8 orchestration patterns in template"
status: COMPLETE
parent: "_index.md"
initiative: sao-init-007
children: []
depends_on: []
blocks:
  - wi-sao-033
  - wi-sao-041
created: "2026-01-12"
last_updated: "2026-01-12"
completed: "2026-01-12"
priority: P1
estimated_effort: "3h"
actual_effort: "1h"
entry_id: sao-038
token_estimate: 700
---

# WI-SAO-038: Document 8 orchestration patterns in template

> **Status:** ✅ COMPLETE
> **Priority:** P1 (HIGH)
> **Completed:** 2026-01-12
> **Blocks:** WI-SAO-033 (template), WI-SAO-041 (decision tree)

---

## Description

Ensure all 8 orchestration patterns identified in DISCOVERY-008 are fully documented with ASCII diagrams, use cases, agent mappings, and cognitive modes.

---

## 8 Patterns Documented

1. ✅ **Single Agent** - Direct invocation, no orchestration overhead
2. ✅ **Sequential Chain** - Order-dependent state passing
3. ✅ **Fan-Out** - Parallel independent execution
4. ✅ **Fan-In** - Output aggregation with sync barrier
5. ✅ **Cross-Pollinated Pipeline** - Bidirectional barriers for multi-track
6. ✅ **Divergent-Convergent (Diamond)** - Explore then converge
7. ✅ **Review Gate** - Quality checkpoint (SRR, PDR, CDR)
8. ✅ **Generator-Critic Loop** - Iterative refinement (max 3, threshold 0.85)

---

## Acceptance Criteria

1. [x] Each pattern has ASCII topology diagram
2. [x] Each pattern has "USE WHEN" section
3. [x] Each pattern has agent mapping examples
4. [x] Each pattern has cognitive mode declaration
5. [x] Generator-Critic has circuit breaker parameters documented
6. [x] Cross-Pollinated has barrier semantics documented

---

## Tasks

- [x] **T-038.1:** Create skills/shared/ directory structure (already exists)
- [x] **T-038.2:** Create ORCHESTRATION_PATTERNS.md reference document
- [x] **T-038.3:** Extract 8 patterns with ASCII diagrams
- [x] **T-038.4:** Document circuit breaker (max_iterations: 3, threshold: 0.85)
- [x] **T-038.5:** Document cross-skill handoff matrix

---

## Verification

| Evidence ID | Type | Description | Status |
|-------------|------|-------------|--------|
| E-038-001 | Artifact | `skills/shared/ORCHESTRATION_PATTERNS.md` created | ✅ Complete |
| E-038-002 | Content | 8 patterns with ASCII diagrams | ✅ Complete |
| E-038-003 | Content | Circuit breaker: max_iterations=3, threshold=0.85 | ✅ Complete |
| E-038-004 | Content | Cross-skill handoff matrix (ps↔nse) | ✅ Complete |
| E-038-005 | Content | Pattern selection decision tree | ✅ Complete |
| E-038-006 | Content | Session context schema v1.0.0 | ✅ Complete |
| E-038-007 | Content | Agent state output keys (19 agents) | ✅ Complete |

---

## Output Artifact

**File:** `skills/shared/ORCHESTRATION_PATTERNS.md`

**Contents:**
- Pattern Overview (8 patterns visual)
- Each pattern with L0/L1/L2 sections
- Pattern Selection Decision Tree
- Agent State Output Keys table
- Cross-Skill Handoff Matrix
- Session Context Schema v1.0.0

**Size:** ~15KB (comprehensive reference document)

---

*Source: SAO-INIT-007 plan.md Pattern Catalog section*
*Completed: 2026-01-12*
