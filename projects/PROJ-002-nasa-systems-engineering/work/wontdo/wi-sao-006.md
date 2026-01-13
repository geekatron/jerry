---
id: wi-sao-006
title: "Create ps-orchestrator Agent"
status: CANCELLED
parent: "../WORKTRACKER.md"
initiative: sao-init-002
children: []
depends_on: []
blocks: []
related:
  - wi-sao-005
  - ref-discoveries  # DISCOVERY-001
created: "2026-01-10"
last_updated: "2026-01-11"
cancelled: "2026-01-11"
cancellation_reason: "DISCOVERY-001"
priority: "N/A"
blockers: []
next_action: "N/A - Cancelled"
estimated_effort: "8h"
actual_effort: "0h"
token_estimate: 700
---

# WI-SAO-006: Create ps-orchestrator Agent

> **Status:** CANCELLED
> **Cancelled:** 2026-01-11
> **Reason:** DISCOVERY-001 - Architecturally incompatible with Claude Code

---

## Summary

This work item is architecturally incompatible with Claude Code:

1. **P-003 Violation:** Agents cannot spawn other agents. An "orchestrator agent" cannot delegate to worker agents.
2. **Redundant:** The `orchestration` skill already provides this capability via `orch-planner`, `orch-tracker`, and `orch-synthesizer`.
3. **Execution Model:** The MAIN CONTEXT (Claude Code session) IS the orchestrator. Agents are workers.
4. **"Mixed" Cognitive Mode:** Not academically canonical (see DISCOVERY-002).

**Alternative:** Use the existing `orchestration` skill for multi-agent coordination. The skill correctly models the MAIN CONTEXT → WORKER relationship.

---

## Original Specification (Archived)

- **Entry ID:** sao-006
- **Priority:** HIGH (P1) → N/A
- **Estimated Effort:** 8h → 0h (cancelled)
- **Source Gap:** GAP-COORD
- **Belbin Role:** Coordinator
- **Description:** Create pipeline orchestrator for ps-* agent coordination.

### Original Acceptance Criteria (ARCHIVED)

1. ~~Agent definition follows PS_AGENT_TEMPLATE v2.0~~
2. ~~Cognitive mode: mixed~~ (not canonical)
3. ~~Delegation criteria documented~~
4. ~~P-003 compliance enforced~~ (impossible for orchestrator agent)

### Tasks (CANCELLED)

- [x] **T-006.1:** ~~Draft ps-orchestrator.md agent definition~~ → CANCELLED
- [x] **T-006.2:** ~~Define problem-solving delegation criteria~~ → CANCELLED
- [x] **T-006.3:** ~~Add workflow templates (3)~~ → CANCELLED
- [x] **T-006.4:** ~~Create BDD tests for ps-* orchestration~~ → CANCELLED

---

## Lessons Learned

1. Validate architectural compatibility BEFORE starting implementation
2. Verify terminology against authoritative sources during planning
3. Check for existing solutions (orchestration skill) before creating new components
4. P-003 constraint has profound implications for agent design patterns

---

*Source: Extracted from WORKTRACKER.md lines 1053-1082*
