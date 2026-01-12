---
id: wi-sao-035
title: "Refactor problem-solving PLAYBOOK.md"
status: COMPLETE
parent: "_index.md"
initiative: sao-init-007
children: []
depends_on:
  - wi-sao-033
blocks:
  - wi-sao-037
created: "2026-01-12"
last_updated: "2026-01-12"
completed: "2026-01-12"
priority: P1
estimated_effort: "6h"
actual_effort: "1.5h"
entry_id: sao-035
token_estimate: 500
---

# WI-SAO-035: Refactor problem-solving PLAYBOOK.md

> **Status:** ✅ COMPLETE
> **Priority:** P1 (HIGH)
> **Completed:** 2026-01-12
> **Depends On:** WI-SAO-033 (template)
> **Blocks:** WI-SAO-037 (validation)

---

## Description

Apply PLAYBOOK_TEMPLATE.md to refactor `skills/problem-solving/PLAYBOOK.md` with L0/L1/L2 sections using the Detective Agency metaphor.

---

## Acceptance Criteria

1. [x] L0 section added with Detective Agency metaphor and ASCII diagram
2. [x] L1 section with all 8 ps-* agent invocations documented
3. [x] L2 section with ≥3 anti-patterns (Agent Soup, Orphan Outputs, etc.)
4. [x] Agent selection guide table present
5. [x] ASCII diagrams in each section
6. [x] No placeholders remain

---

## Tasks

- [x] **T-035.1:** Read existing problem-solving/PLAYBOOK.md
- [x] **T-035.2:** Apply template structure
- [x] **T-035.3:** Write L0 section (Detective Agency)
- [x] **T-035.4:** Enhance L1 with 8 agents
- [x] **T-035.5:** Write L2 section (anti-patterns)
- [x] **T-035.6:** Version bump v2.0.0 -> v3.0.0

---

## Verification

| Evidence ID | Type | Description | Status |
|-------------|------|-------------|--------|
| E-035-001 | Content | L0 section with Detective Agency metaphor | ✅ Complete |
| E-035-002 | Content | L1 section with 8 agent commands | ✅ Complete |
| E-035-003 | Content | L2 section with 4 anti-patterns | ✅ Complete |
| E-035-004 | Version | v2.0.0 -> v3.0.0 | ✅ Complete |

---

## Output Summary

**File:** `skills/problem-solving/PLAYBOOK.md` (v3.0.0)

**L0 (ELI5) Section:**
- Detective Agency metaphor with boxed ASCII case intake diagram
- Detective Roster diagram (8 agents with metaphors)
- Agent selection guide flowchart
- Activation keywords table
- L0/L1/L2 output format explanation diagram

**L1 (Engineer) Section:**
- 30-second quick start
- 3 invocation methods
- 8 agents reference table with keywords and output locations
- 5 orchestration patterns with ASCII topologies
- 5 practical examples
- Output directory tree
- Tips and best practices
- Troubleshooting guide

**L2 (Architect) Section:**
- 4 Anti-patterns with boxed ASCII diagrams:
  - AP-001: Agent Soup
  - AP-002: Orphan Outputs
  - AP-003: Analysis Paralysis
  - AP-004: Context Amnesia
- Hard constraints table (5 constraints)
- Soft constraints table (3 constraints)
- Invariants checklist (5 invariants)
- Agent selection matrix with cognitive modes
- Session context schema
- Cross-skill handoff table
- Design rationale (3 decisions)

**Size:** ~25KB (comprehensive refactoring)

---

*Source: SAO-INIT-007 plan.md Phase 2*
*Completed: 2026-01-12*
