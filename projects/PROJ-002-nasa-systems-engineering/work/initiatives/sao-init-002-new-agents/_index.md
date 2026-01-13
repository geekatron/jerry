---
id: sao-init-002
title: "New Agent Development"
type: initiative_index
status: IN_PROGRESS
parent: "../../WORKTRACKER.md"
children:
  - wi-sao-004.md
  - wi-sao-007.md
  - wi-sao-008.md
related:
  - "../../wontdo/wi-sao-005.md"
  - "../../wontdo/wi-sao-006.md"
created: "2026-01-10"
last_updated: "2026-01-11"
work_items_total: 5
work_items_complete: 3
work_items_cancelled: 2
tasks_total: 22
tasks_complete: 18
token_estimate: 700
---

# SAO-INIT-002: New Agent Development

> **Status:** IN PROGRESS (3/5 work items complete, 2 cancelled)
> **Last Updated:** 2026-01-11

---

## Summary

New agent development initiative adding specialized agents to both ps-* and nse-* families:

| Work Item | Status | Description |
|-----------|--------|-------------|
| WI-SAO-004 | ✅ COMPLETE | nse-explorer (divergent mode) |
| WI-SAO-005 | ❌ CANCELLED | nse-orchestrator (DISCOVERY-001) |
| WI-SAO-006 | ❌ CANCELLED | ps-orchestrator (DISCOVERY-001) |
| WI-SAO-007 | ✅ COMPLETE | ps-critic (generator-critic loops) |
| WI-SAO-008 | ✅ COMPLETE | nse-qa (artifact validation) |

---

## Cancellation Note

WI-SAO-005 and WI-SAO-006 were cancelled due to **DISCOVERY-001**: Orchestrator agents are architecturally incompatible with Claude Code's P-003 constraint. The MAIN CONTEXT is the orchestrator; agents are workers. See `wontdo/wi-sao-005.md` and `wontdo/wi-sao-006.md` for details.

---

## Key Artifacts

| Agent | File | Lines | Belbin Role |
|-------|------|-------|-------------|
| nse-explorer | `skills/nasa-se/agents/nse-explorer.md` | 17/17 conformant | Plant + Resource Investigator |
| ps-critic | `skills/problem-solving/agents/ps-critic.md` | 528 | Monitor Evaluator |
| nse-qa | `skills/nasa-se/agents/nse-qa.md` | 664 | Monitor Evaluator |

---

## Agent Count Summary

- **Before:** 16 agents (8 ps-*, 8 nse-*)
- **After:** 19 agents (9 ps-*, 10 nse-*)
- **Conformance:** 19/19 pass

---

*Source: Extracted from WORKTRACKER.md lines 987-1139*
