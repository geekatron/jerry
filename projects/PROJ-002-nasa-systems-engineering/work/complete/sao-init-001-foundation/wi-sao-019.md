---
id: wi-sao-019
title: "Agent Architecture Research (5W1H + NASA SE)"
status: COMPLETE
parent: "_index.md"
initiative: sao-init-001
children: []
depends_on: []
blocks: []
created: "2026-01-10"
started: "2026-01-10"
completed: "2026-01-10"
priority: "P0"
estimated_effort: "4h"
entry_id: "sao-019"
source: "User clarification request on agent architecture claim"
token_estimate: 1200
---

# WI-SAO-019: Agent Architecture Research (5W1H + NASA SE)

> **Status:** ✅ COMPLETE
> **Started:** 2026-01-10
> **Completed:** 2026-01-10
> **Priority:** CRITICAL (P0)

---

## Trigger Statement

"Jerry agents are NOT Claude Code subagents in the formal sense"

---

## Description

Comprehensive research to establish common understanding of Claude Code subagent mechanics, Task tool patterns, and Jerry agent architecture. Must produce evidence-based explanation at ELI5, Engineer, and Architect levels.

---

## Research Framework

5W1H + NASA SE Handbook (NPR 7123.1D Process 17: Decision Analysis)

---

## Research Questions

1. **WHAT** are Claude Code subagents (formal definition)?
2. **WHAT** is the Task tool and how does it spawn agents?
3. **WHY** are there agents in `.claude/agents/` vs `skills/*/agents/`?
4. **HOW** do industry multi-agent frameworks handle this?
5. **WHO** are the authoritative sources on this topic?
6. **WHEN** should each agent type be used?

---

## Acceptance Criteria

1. ✅ Claude Code documentation researched and cited (Context7 + claude.ai/docs)
2. ✅ Task tool mechanics documented with evidence
3. ✅ `.claude/agents/` vs `skills/*/agents/` differences explained
4. ✅ Industry best practices cited (45+ authoritative sources)
5. ✅ 3-level explanation produced (ELI5, Engineer, Architect)
6. ✅ Research artifact persisted to `projects/PROJ-002.../research/`

---

## Key Findings

- Claude Code subagents are isolated Claude instances spawned via Task tool
- Jerry agents ARE Claude Code subagents when invoked via Task tool
- AgentDefinition type: `{ description, tools?, prompt, model? }`
- Built-in subagent types: Explore, Plan, general-purpose, claude-code-guide
- P-003 constraint: max 1 level nesting (orchestrator → worker)
- Token economics: agent = 4×, multi-agent = 15× vs chat

---

## Output Artifact

`research/agent-architecture-5w1h-analysis.md` (~700 lines)

---

## Tasks

- [x] **R-019.1:** Research Claude Code subagent mechanics (Context7 + docs)
- [x] **R-019.2:** Research Task tool spawn patterns
- [x] **R-019.3:** Analyze `.claude/agents/` vs `skills/*/agents/` in this repo
- [x] **R-019.4:** Research industry multi-agent patterns (min 5 sources)
- [x] **R-019.5:** Synthesize findings + produce 3-level explanation

---

*Source: Extracted from WORKTRACKER.md lines 889-927*
