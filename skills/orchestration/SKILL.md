---
name: orchestration
description: Multi-agent workflow orchestration with state tracking, checkpointing, and cross-pollinated pipelines. Use when coordinating parallel agent pipelines, managing sync barriers, or tracking complex workflow execution state across sessions.
version: "1.0.0"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Task, WebSearch, WebFetch
activation-keywords:
  - "orchestration"
  - "multi-agent workflow"
  - "pipeline"
  - "cross-pollinated"
  - "sync barrier"
  - "checkpoint"
  - "workflow state"
  - "parallel agents"
  - "agent coordination"
  - "execution tracking"
---

# Orchestration Skill

> **Version:** 1.0.0
> **Framework:** Jerry Orchestration (ORCH)
> **Constitutional Compliance:** Jerry Constitution v1.0
> **Industry References:** [Anthropic Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills), [Microsoft AI Agent Patterns](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns), [LangGraph](https://langchain-ai.github.io/langgraph/), [CrewAI Flows](https://docs.crewai.com/concepts/flows)

---

## Purpose

The Orchestration skill provides a structured framework for managing **multi-agent workflows** that require:

- **Parallel Pipeline Execution** - Multiple agent pipelines running concurrently
- **Sync Barriers** - Cross-pollination points between pipelines
- **State Tracking** - Persistent execution state across sessions
- **Checkpointing** - Recovery points for long-running workflows
- **Progress Visibility** - Clear dashboards and metrics

### Key Capabilities

- **Cross-Pollinated Pipelines** - Bidirectional agent pipelines with barrier synchronization
- **State Management** - YAML-based machine-readable state (SSOT)
- **Checkpoint Recovery** - Resume workflows from any checkpoint
- **Execution Queues** - Priority-ordered agent execution with dependencies
- **Metrics Tracking** - Progress percentages, success rates, timing

---

## When to Use This Skill

Activate when:

- Coordinating **3+ agents** in a structured workflow
- Running **parallel pipelines** that need synchronization
- Workflow spans **multiple sessions** and needs state persistence
- Need **checkpointing** for long-running processes
- Require **visibility** into complex workflow progress

**Do NOT use when:**
- Single agent task (use problem-solving skill instead)
- Simple sequential flow (use direct agent invocation)
- No cross-session state needed

---

## Core Artifacts

Every orchestrated workflow creates three artifacts:

| Artifact | Format | Purpose | Audience |
|----------|--------|---------|----------|
| `ORCHESTRATION_PLAN.md` | Markdown | Strategic context, workflow diagram | Humans |
| `ORCHESTRATION_WORKTRACKER.md` | Markdown | Tactical execution documentation | Humans |
| `ORCHESTRATION.yaml` | YAML | Machine-readable state (SSOT) | Claude/Automation |

**Location:** `projects/{project_id}/`

---

## Available Agents

| Agent | Role | Output |
|-------|------|--------|
| `orch-planner` | Creates orchestration plan with workflow diagram | `ORCHESTRATION_PLAN.md` |
| `orch-tracker` | Updates execution state after agent completion | `ORCHESTRATION.yaml`, `ORCHESTRATION_WORKTRACKER.md` |
| `orch-synthesizer` | Creates final workflow synthesis | `synthesis/workflow-synthesis.md` |

### Important: P-003 Compliance

These agents are **workers invoked by the main context**. They do NOT spawn other agents.

```
MAIN CONTEXT (Claude) ← Orchestrator
    │
    ├──► orch-planner      (creates plan)
    ├──► ps-d-001          (Phase work)
    ├──► nse-f-001         (Phase work)
    ├──► orch-tracker      (updates state)
    └──► orch-synthesizer  (final synthesis)

Each is a WORKER. None spawn other agents.
```

---

## Workflow Patterns

### Pattern 1: Cross-Pollinated Pipeline

Two or more pipelines running in parallel with synchronization barriers.

```
Pipeline A                    Pipeline B
    │                              │
    ▼                              ▼
┌─────────┐                  ┌─────────┐
│ Phase 1 │                  │ Phase 1 │
└────┬────┘                  └────┬────┘
     │                            │
     └──────────┬─────────────────┘
                ▼
        ╔═══════════════╗
        ║   BARRIER 1   ║  ← Cross-pollination
        ╚═══════════════╝
                │
     ┌──────────┴─────────────────┐
     │                            │
     ▼                            ▼
┌─────────┐                  ┌─────────┐
│ Phase 2 │                  │ Phase 2 │
└─────────┘                  └─────────┘
```

### Pattern 2: Sequential with Checkpoints

Single pipeline with checkpoints for recovery.

```
┌─────────┐     ┌─────────┐     ┌─────────┐
│ Phase 1 │────►│ Phase 2 │────►│ Phase 3 │
└─────────┘     └─────────┘     └─────────┘
     │               │               │
     ▼               ▼               ▼
   CP-001          CP-002          CP-003
```

### Pattern 3: Fan-Out/Fan-In

Parallel execution with synthesis.

```
              ┌─────────┐
              │  Start  │
              └────┬────┘
        ┌──────────┼──────────┐
        ▼          ▼          ▼
   ┌────────┐ ┌────────┐ ┌────────┐
   │Agent A │ │Agent B │ │Agent C │
   └────┬───┘ └────┬───┘ └────┬───┘
        └──────────┼──────────┘
                   ▼
            ┌────────────┐
            │ Synthesize │
            └────────────┘
```

---

## Quick Start

### Step 1: Create Orchestration Artifacts

```
# Copy templates to your project
cp skills/orchestration/templates/ORCHESTRATION_PLAN.template.md \
   projects/{PROJECT}/ORCHESTRATION_PLAN.md

cp skills/orchestration/templates/ORCHESTRATION_WORKTRACKER.template.md \
   projects/{PROJECT}/ORCHESTRATION_WORKTRACKER.md

cp skills/orchestration/templates/ORCHESTRATION.template.yaml \
   projects/{PROJECT}/ORCHESTRATION.yaml
```

Or use the `orch-planner` agent:

```
"Create an orchestration plan for a cross-pollinated pipeline
 with ps-* and nse-* phases"
```

### Step 2: Update State After Each Agent

After each agent completes, update the state:

```
"Update ORCHESTRATION.yaml: ps-d-001 complete,
 artifact at ps-pipeline/phase-3-design/agent-design-specs.md"
```

### Step 3: Track Progress

Check workflow status:

```
"Show orchestration status for PROJ-002"
```

---

## State Schema

### ORCHESTRATION.yaml Structure

```yaml
workflow:
  id: string                    # Unique workflow identifier
  name: string                  # Human-readable name
  project_id: string            # Project identifier
  status: ACTIVE|PAUSED|COMPLETE|FAILED

pipelines:
  {pipeline_id}:
    current_phase: number
    phases:
      - id: number
        name: string
        status: PENDING|IN_PROGRESS|COMPLETE|BLOCKED
        agents:
          - id: string
            status: PENDING|IN_PROGRESS|COMPLETE|FAILED
            artifact: string    # Path to output artifact

barriers:
  - id: string
    status: PENDING|COMPLETE
    artifacts:
      ps_to_nse: {path, status}
      nse_to_ps: {path, status}

execution_queue:
  current_group: number
  groups:
    - id: number
      execution_mode: PARALLEL|SEQUENTIAL
      agents: [agent_ids]

checkpoints:
  latest_id: string
  entries:
    - id: string
      timestamp: ISO-8601
      trigger: PHASE_COMPLETE|BARRIER_COMPLETE|MANUAL
      recovery_point: string

metrics:
  phases_complete: number
  phases_total: number
  agents_executed: number
  agents_total: number
```

See `docs/STATE_SCHEMA.md` for complete schema documentation.

---

## Constitutional Compliance

| Principle | Requirement | Implementation |
|-----------|-------------|----------------|
| P-002 | File Persistence | All state persisted to ORCHESTRATION.yaml |
| P-003 | No Recursive Subagents | Main context invokes workers only |
| P-010 | Task Tracking | ORCHESTRATION_WORKTRACKER.md updated |
| P-022 | No Deception | Honest status and progress reporting |

---

## Templates

| Template | Purpose |
|----------|---------|
| `templates/ORCHESTRATION_PLAN.template.md` | Strategic context with ASCII diagram |
| `templates/ORCHESTRATION_WORKTRACKER.template.md` | Tactical execution tracking |
| `templates/ORCHESTRATION.template.yaml` | Machine-readable state skeleton |

---

## Agent Details

For detailed agent specifications, see:

- `skills/orchestration/agents/orch-planner.md`
- `skills/orchestration/agents/orch-tracker.md`
- `skills/orchestration/agents/orch-synthesizer.md`

---

## Playbook

For workflow examples and step-by-step guides, see:

- `skills/orchestration/PLAYBOOK.md`

---

## References

1. Anthropic. (2025). *Equipping agents for the real world with Agent Skills*. https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills
2. Microsoft. (2025). *AI Agent Orchestration Patterns*. https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns
3. LangChain. (2025). *LangGraph Documentation*. https://langchain-ai.github.io/langgraph/
4. CrewAI. (2025). *Flows Documentation*. https://docs.crewai.com/concepts/flows

---

*Skill Version: 1.0.0*
*Constitutional Compliance: Jerry Constitution v1.0*
*Created: 2026-01-10*
