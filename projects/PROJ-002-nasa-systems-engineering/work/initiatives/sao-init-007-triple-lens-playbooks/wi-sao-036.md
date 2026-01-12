---
id: wi-sao-036
title: "Refactor nasa-se PLAYBOOK.md"
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
actual_effort: "2h"
entry_id: sao-036
token_estimate: 500
---

# WI-SAO-036: Refactor nasa-se PLAYBOOK.md

> **Status:** ✅ COMPLETE
> **Priority:** P1 (HIGH)
> **Completed:** 2026-01-12
> **Depends On:** WI-SAO-033 (template)
> **Blocks:** WI-SAO-037 (validation)

---

## Description

Apply PLAYBOOK_TEMPLATE.md to refactor `skills/nasa-se/PLAYBOOK.md` with L0/L1/L2 sections using the Mission Control metaphor.

---

## Acceptance Criteria

1. [x] L0 section added with Mission Control metaphor and launch countdown ASCII
2. [x] L1 section with all 8 nse-* agent invocations documented
3. [x] L2 section with NASA-specific anti-patterns (AI as Authority, Skipping Reviews)
4. [x] Technical review sequence documented (SRR→PDR→CDR→TRR→FRR)
5. [x] P-043 disclaimer placement guidance
6. [x] ASCII diagrams in each section

---

## Tasks

- [x] **T-036.1:** Read existing nasa-se/PLAYBOOK.md
- [x] **T-036.2:** Apply template structure
- [x] **T-036.3:** Write L0 section (Mission Control)
- [x] **T-036.4:** Enhance L1 with 8 agents and review gates
- [x] **T-036.5:** Write L2 section (NASA anti-patterns)
- [x] **T-036.6:** Version bump v1.0.0 -> v2.0.0

---

## Verification

| Evidence ID | Type | Description | Status |
|-------------|------|-------------|--------|
| E-036-001 | Content | L0 section with Mission Control metaphor | ✅ Complete |
| E-036-002 | Content | L1 section with 8 agent commands | ✅ Complete |
| E-036-003 | Content | L2 section with 4 NASA anti-patterns | ✅ Complete |
| E-036-004 | Content | P-043 disclaimer guidance present | ✅ Complete |

---

## Output Summary

**File:** `skills/nasa-se/PLAYBOOK.md` (v2.0.0)

**L0 (ELI5) Section:**
- Mission Control metaphor with launch countdown ASCII diagram
- Review sequence diagram (SRR → PDR → CDR → TRR → FRR)
- Mission Control Roster (8 specialists with metaphors)
- Specialist selection guide flowchart
- Activation keywords table

**L1 (Engineer) Section:**
- 30-second quick start
- 3 invocation methods
- 8 agents reference table with keywords and output locations
- 5 practical workflows with ASCII topologies
- Review preparation guide with checklist
- Output directory tree
- Tips and best practices
- Troubleshooting guide

**L2 (Architect) Section:**
- 4 Anti-patterns with boxed ASCII diagrams:
  - AP-001: AI as Authority
  - AP-002: Skipping Review Gates
  - AP-003: Orphan Requirements
  - AP-004: Risk Blindness
- Hard constraints table (5 constraints)
- Soft constraints table (3 constraints)
- Invariants checklist (5 invariants)
- P-043 Disclaimer placement guide
- Cross-skill handoff table
- Design rationale (3 decisions)

**Size:** ~30KB (comprehensive refactoring)

---

*Source: SAO-INIT-007 plan.md Phase 3*
*Completed: 2026-01-12*
