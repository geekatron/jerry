# Orchestration Skill Access Architecture Analysis

> **Document ID:** PROJ-002-e-037-skill-access-analysis
> **Date:** 2026-01-10
> **Author:** Claude (Opus 4.5)
> **Status:** ANALYSIS COMPLETE
> **Method:** 5W1H Framework + Industry Research

---

## Executive Summary

**Critical Finding:** Sub-agents in Jerry do NOT automatically have access to the orchestration skill. The current design has an architectural gap where:

1. **Main Claude thread** is the ONLY entity that should interact with the orchestration skill
2. **Sub-agents** (ps-*, nse-*) should NOT directly interact with the skill
3. **State is shared via filesystem**, not skill injection
4. **The orchestration skill is a control plane tool**, not a data plane tool

---

## 5W1H Analysis

### 1. WHO should interact with the orchestration skill?

| Actor | Should Interact? | Reason |
|-------|------------------|--------|
| Main Claude Thread | **YES - Primary** | Orchestrator role, coordinates all agents |
| ps-* agents | **NO** | Workers, not orchestrators |
| nse-* agents | **NO** | Workers, not orchestrators |
| orch-* agents | **YES - Secondary** | Specialized skill workers for specific tasks |
| User | **YES** | Ultimate authority (P-020) |

**Evidence from Research:**

> "Subagents do not automatically inherit Skills from the main conversation. To give a custom subagent access to specific Skills, list them in the subagent's `skills` field."
> — [Claude Code Subagents Documentation](https://code.claude.com/docs/en/sub-agents)

> "The hierarchical agent team is typically organized into at least two levels: a supervisor and a team of worker agents."
> — [LangGraph Hierarchical Teams](https://langchain-ai.github.io/langgraph/tutorials/multi_agent/hierarchical_agent_teams/)

**Conclusion:** The main Claude thread acts as the supervisor/orchestrator. Sub-agents are workers that should NOT need orchestration access.

---

### 2. WHAT is the orchestration skill's role?

| Component | Description |
|-----------|-------------|
| **Control Plane** | Workflow state, execution tracking, checkpoints |
| **State Management** | ORCHESTRATION.yaml as SSOT |
| **Coordination** | Barrier synchronization, execution ordering |
| **Recovery** | Checkpoint-based resumption |

The orchestration skill is a **control plane tool** - it manages the workflow, not the work itself.

**Analogy:**
- **Orchestration Skill** = Air Traffic Control
- **ps-*/nse-* Agents** = Airplanes
- **State Files** = Flight plans and radar data

Air Traffic Control doesn't fly planes; it coordinates them. Similarly, the orchestration skill doesn't do the work - it coordinates the agents that do.

---

### 3. WHEN does state synchronization occur?

| Event | Who Updates State | How |
|-------|-------------------|-----|
| Agent starts | Main thread OR orch-tracker | Updates ORCHESTRATION.yaml |
| Agent completes | Main thread OR orch-tracker | Updates status, registers artifact |
| Barrier crossed | Main thread OR orch-tracker | Creates cross-pollination artifacts |
| Checkpoint needed | Main thread OR orch-tracker | Adds checkpoint entry |
| Workflow complete | Main thread OR orch-synthesizer | Final synthesis |

**Pattern from CrewAI:**

> "Flows allow you to create structured, event-driven workflows that manage state and control execution."
> — [CrewAI Flows Documentation](https://docs.crewai.com/concepts/flows)

> "CrewAI passes the complete, unmodified output of each previous task directly into the planner's context through its context parameter system."
> — [CrewAI Context Sharing](https://www.firecrawl.dev/blog/crewai-multi-agent-systems-tutorial)

**Conclusion:** State updates happen AFTER agent completion, not DURING. The main thread (or orch-tracker) updates state between agent invocations.

---

### 4. WHERE does state live?

| State Type | Location | Access Pattern |
|------------|----------|----------------|
| Workflow State | `ORCHESTRATION.yaml` | Read/Write by main thread |
| Agent Artifacts | `{pipeline}/phase-{n}/` | Write by agents, Read by all |
| Barrier Artifacts | `barriers/` | Write by orch-tracker |
| Checkpoints | `ORCHESTRATION.yaml` | Append-only log |

**Industry Pattern (Shared State):**

> "In shared memory architectures, all agents access the same state store for consistent context and result sharing."
> — [Multi-Agent Orchestration Guide](https://www.kore.ai/blog/what-is-multi-agent-orchestration)

> "A shared memory or state object is typically used so agents can remain loosely coupled but coordinated. This allows agents to asynchronously read, write, and react without needing direct communication."
> — [AI Agent Orchestration Frameworks](https://blog.n8n.io/ai-agent-orchestration-frameworks/)

**Conclusion:** The filesystem (ORCHESTRATION.yaml + artifact files) IS the shared state. Sub-agents don't need skill access because they write artifacts to agreed-upon paths.

---

### 5. WHY don't sub-agents need skill access?

| Reason | Explanation |
|--------|-------------|
| **P-003 Compliance** | Sub-agents can't spawn other agents, so they can't orchestrate |
| **Separation of Concerns** | Workers do work; orchestrator coordinates |
| **Context Efficiency** | Injecting skill content bloats agent context |
| **State via Files** | Agents write to known paths; main thread reads |
| **Single Nesting** | Jerry allows only 1 level of nesting |

**Critical Insight:**

Jerry's architecture follows the **Hierarchical Delegation** pattern:

```
MAIN CLAUDE THREAD (Orchestrator)
    │
    │   Has access to:
    │   - orchestration skill
    │   - problem-solving skill
    │   - nasa-se skill
    │   - worktracker skill
    │
    ├──► ps-researcher (Worker)
    │    └── Writes to: research/file.md
    │
    ├──► nse-requirements (Worker)
    │    └── Writes to: requirements/file.md
    │
    ├──► orch-tracker (Specialized Worker)
    │    └── Updates: ORCHESTRATION.yaml
    │
    └──► orch-synthesizer (Specialized Worker)
         └── Creates: synthesis/file.md
```

The main thread:
1. **Reads** ORCHESTRATION.yaml to know current state
2. **Invokes** appropriate agent with Task tool
3. **After completion**, updates state (directly or via orch-tracker)
4. **Repeats** until workflow complete

---

### 6. HOW should the orchestration workflow function?

#### Pattern A: Main Thread Direct Orchestration (RECOMMENDED)

```
1. Main thread reads ORCHESTRATION.yaml
2. Main thread determines next action
3. Main thread invokes worker agent (ps-*, nse-*)
4. Worker agent writes artifact to designated path
5. Main thread updates ORCHESTRATION.yaml
6. Repeat until complete
```

**Pros:**
- Simplest implementation
- No skill injection needed
- Main thread has full visibility
- P-003 compliant

**Cons:**
- Main thread context grows

#### Pattern B: Delegated State Updates (via orch-tracker)

```
1. Main thread reads ORCHESTRATION.yaml
2. Main thread invokes worker agent
3. Worker writes artifact
4. Main thread invokes orch-tracker to update state
5. Repeat
```

**Pros:**
- Separates work from bookkeeping
- State update logic centralized
- Cleaner separation

**Cons:**
- Extra agent invocation per step
- Slightly more complex

#### Pattern C: Worker Self-Registration (NOT RECOMMENDED)

```
1. Worker reads ORCHESTRATION.yaml (needs to know path)
2. Worker does work
3. Worker updates own status in ORCHESTRATION.yaml
```

**Cons:**
- Workers need orchestration knowledge
- Violates separation of concerns
- Race conditions possible
- Context bloat in workers

---

## Recommendations

### R1: Main Thread as Sole Orchestrator (CONFIRMED)

The orchestration skill should ONLY be used by the main Claude thread (or orch-* specialized agents invoked by main thread).

**Sub-agents (ps-*, nse-*) should NOT:**
- Read ORCHESTRATION.yaml
- Write to ORCHESTRATION.yaml
- Have the orchestration skill injected

**Sub-agents SHOULD:**
- Write artifacts to designated paths
- Return completion status to main thread
- Focus on their specialized work

### R2: Filesystem as Shared State Layer

Use the filesystem (not skill injection) for state sharing:

| State | File |
|-------|------|
| Workflow state | `ORCHESTRATION.yaml` |
| Agent outputs | `{pipeline}/phase-{n}/artifact.md` |
| Barrier artifacts | `barriers/barrier-{n}-{direction}.md` |

### R3: No Modification to Existing Agents

The ps-* and nse-* agents do NOT need modification. They already:
- Write to designated paths
- Return completion summaries
- Are P-003 compliant

### R4: Orchestration Skill is Complete As-Is

The current orchestration skill design is architecturally correct:
- Main thread uses SKILL.md for guidance
- orch-* agents are specialized helpers
- State tracked via ORCHESTRATION.yaml

---

## Evidence Summary

| Source | Key Finding | URL |
|--------|-------------|-----|
| Claude Code Docs | Sub-agents don't inherit skills | https://code.claude.com/docs/en/sub-agents |
| LangGraph | Hierarchical teams with supervisor/worker | https://langchain-ai.github.io/langgraph/tutorials/multi_agent/hierarchical_agent_teams/ |
| CrewAI | Flows for state management, Crews for agents | https://docs.crewai.com/concepts/flows |
| Kore.ai | Shared context via state store | https://www.kore.ai/blog/what-is-multi-agent-orchestration |
| n8n | Shared memory/state object for coordination | https://blog.n8n.io/ai-agent-orchestration-frameworks/ |
| Microsoft | MCP for shared context interface | https://techcommunity.microsoft.com/blog/azuredevcommunityblog/orchestrating-multi-agent-intelligence-mcp-driven-patterns-in-agent-framework/4462150 |

---

## Conclusion

**The orchestration skill does NOT need to be accessible to sub-agents.**

The design is correct:
1. Main thread orchestrates using the skill
2. Sub-agents do specialized work
3. State is shared via filesystem (ORCHESTRATION.yaml)
4. This follows industry patterns (LangGraph, CrewAI, Microsoft MCP)

**No changes required to existing ps-* or nse-* agents.**

---

*Analysis Version: 1.0.0*
*Method: 5W1H Framework*
*Industry Sources: 6*
*Compliance: Jerry Constitution v1.0*
