---
name: orchestration
description: Multi-agent workflow orchestration with state tracking, checkpointing, and cross-pollinated pipelines. Use when coordinating parallel agent pipelines, managing sync barriers, or tracking complex workflow execution state across sessions.
version: "2.1.0"
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

> **Version:** 2.1.0
> **Framework:** Jerry Orchestration (ORCH)
> **Constitutional Compliance:** Jerry Constitution v1.0
> **Industry References:** [Anthropic Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills), [Microsoft AI Agent Patterns](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns), [LangGraph](https://langchain-ai.github.io/langgraph/), [CrewAI Flows](https://docs.crewai.com/concepts/flows)

---

## Document Audience (Triple-Lens)

This SKILL.md serves multiple audiences:

| Level | Audience | Sections to Focus On |
|-------|----------|---------------------|
| **L0 (ELI5)** | Project stakeholders, new users | Purpose, When to Use, Core Artifacts |
| **L1 (Engineer)** | Developers executing workflows | Quick Start, State Schema |
| **L2 (Architect)** | Workflow designers | Workflow Patterns, Constitutional Compliance |

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
 using problem-solving and nasa-systems-engineering skills"
```

The planner will automatically:
1. Generate a workflow ID (or use your specified ID)
2. Resolve pipeline aliases from skill defaults
3. Create dynamic path structure

### Step 2: Update State After Each Agent

After each agent completes, update the state. Reference artifacts using the dynamic path scheme:

```
"Update ORCHESTRATION.yaml: agent-a-001 complete,
 artifact at orchestration/{workflow_id}/{pipeline_alias}/phase-1/research.md"
```

The orch-tracker agent will resolve placeholders to actual paths.

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
      a_to_b: {path, status}   # {pipeline_a_alias}-to-{pipeline_b_alias}
      b_to_a: {path, status}   # {pipeline_b_alias}-to-{pipeline_a_alias}

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

## Workflow Configuration

### Workflow Identification

Every orchestration workflow requires a unique identifier for:
- Artifact organization under `orchestration/{workflow_id}/`
- Cross-session resumption
- State file correlation

**Workflow ID Strategies:**

| Strategy | Format | Example | When to Use |
|----------|--------|---------|-------------|
| User-Specified | Any valid identifier | `my-custom-workflow` | User has specific naming convention |
| Auto-Generated | `{purpose}-{YYYYMMDD}-{NNN}` | `sao-crosspoll-20260110-001` | Default when no user preference |

**Configuration in ORCHESTRATION.yaml:**

```yaml
workflow:
  id: "sao-crosspoll-20260110-001"
  id_source: "auto"        # "user" | "auto"
  id_format: "semantic-date-seq"
```

**ID Generation Rules:**
1. User-specified IDs take priority when provided
2. Auto-generated IDs use semantic-date-sequence format
3. IDs must be valid filesystem path components (no spaces, special characters)
4. IDs are immutable once workflow is created

### Pipeline Alias Configuration

Each pipeline in a workflow has a **short alias** used in artifact paths. This provides flexibility while maintaining human-readable paths.

**Alias Resolution Priority:**

| Priority | Source | Example | Description |
|----------|--------|---------|-------------|
| 1 (Highest) | Workflow Override | `alpha` | Explicit override in ORCHESTRATION.yaml |
| 2 | Skill Default | `ps` | Registered default from skill definition |
| 3 (Fallback) | Auto-Derived | `problem-solving` | Derived from skill name |

**Configuration in ORCHESTRATION.yaml:**

```yaml
pipelines:
  pipeline_a:
    short_alias: "ps"                    # Used in paths
    skill_source: "problem-solving"       # Originating skill

  pipeline_b:
    short_alias: "nse"
    skill_source: "nasa-systems-engineering"
```

**Skill Default Registration:**

Skills can register a default pipeline alias. When creating new workflows, check if the skill provides a default:

```yaml
# In skill definition (future capability)
skill:
  name: "problem-solving"
  default_pipeline_alias: "ps"
```

**User Override:**

Users can override aliases when creating a workflow:

```
"Create an orchestration plan using problem-solving (alias: alpha)
 and nasa-se (alias: beta) pipelines"
```

### Dynamic Path Scheme

All artifact paths are dynamically constructed using workflow and pipeline identifiers. **No hardcoded pipeline names** (like `ps-pipeline` or `nse-pipeline`) should appear in templates or agents.

**Path Templates:**

| Component | Path Pattern |
|-----------|--------------|
| Base Path | `orchestration/{workflow_id}/` |
| Pipeline Artifacts | `orchestration/{workflow_id}/{pipeline_alias}/{phase_id}/{agent_id}/` |
| Cross-Pollination | `orchestration/{workflow_id}/cross-pollination/{barrier_id}/{source}-to-{target}/` |

**Agent-Level Isolation (AC-012-004):**

Each agent writes to its own subdirectory to prevent file collisions during parallel (fan-out) execution:

```
orchestration/{workflow_id}/{pipeline_alias}/phase-{N}/{agent_id}/
```

**Defense in Depth - Unique Filenames:**

For mission-critical workflows, artifacts SHOULD use unique filenames that include the agent ID, providing two layers of protection:

```
orchestration/{workflow_id}/{pipeline_alias}/phase-{N}/{agent_id}/{agent_id}-{artifact_type}.md
```

This ensures:
- **Primary protection:** Directory isolation (each agent has own directory)
- **Secondary protection:** Unique filenames (safe even if flattened)
- **Full provenance:** Agent ID in both path AND filename
- **Safe synthesis:** Can merge to single directory without collision

**Example Path Resolution:**

Given:
- `workflow_id`: `sao-crosspoll-20260110-001`
- `pipeline_a.short_alias`: `ps`
- `pipeline_b.short_alias`: `nse`
- `agent_id`: `agent-a-001`

Resolved paths (with defense in depth):
```
orchestration/sao-crosspoll-20260110-001/ps/phase-1/agent-a-001/agent-a-001-research.md
orchestration/sao-crosspoll-20260110-001/nse/phase-1/agent-b-001/agent-b-001-analysis.md
orchestration/sao-crosspoll-20260110-001/cross-pollination/barrier-1/ps-to-nse/handoff.md
```

**Important:** Templates use placeholders like `{WORKFLOW_ID}`, `{PIPELINE_A_ALIAS}`, etc. Agents MUST resolve these at runtime using the workflow configuration.

---

## Tool Invocation Examples

Each orchestration workflow uses tools for state management. Here are concrete examples:

### Workflow Planning (orch-planner)

```
1. Find existing orchestration artifacts:
   Glob(pattern="projects/${JERRY_PROJECT}/orchestration/**/*.yaml")
   → Returns list of existing workflow state files

2. Read project context for workflow design:
   Read(file_path="projects/${JERRY_PROJECT}/PLAN.md")
   → Load project plan to understand workflow scope

3. Create orchestration plan (MANDATORY per P-002):
   Write(
       file_path="projects/${JERRY_PROJECT}/orchestration/sao-crosspoll-20260112-001/ORCHESTRATION_PLAN.md",
       content="# Orchestration Plan: Cross-Pollinated Pipeline\n\n## Workflow Diagram\n```\nPipeline A             Pipeline B\n..."
   )
   → Persist strategic plan - transient planning VIOLATES P-002
```

### State Tracking (orch-tracker)

```
1. Read current workflow state (SSOT):
   Read(file_path="projects/${JERRY_PROJECT}/orchestration/sao-crosspoll-20260112-001/ORCHESTRATION.yaml")
   → Load machine-readable state as single source of truth

2. Search for agent completion artifacts:
   Glob(pattern="projects/${JERRY_PROJECT}/orchestration/**/phase-*/**/*.md")
   → Find all agent output artifacts for status reconciliation

3. Update workflow state (MANDATORY per P-002):
   Write(
       file_path="projects/${JERRY_PROJECT}/orchestration/sao-crosspoll-20260112-001/ORCHESTRATION.yaml",
       content="workflow:\n  id: 'sao-crosspoll-20260112-001'\n  status: ACTIVE\n..."
   )
   → Persist state changes - in-memory-only state VIOLATES P-002
```

### Workflow Synthesis (orch-synthesizer)

```
1. Find all barrier artifacts:
   Glob(pattern="projects/${JERRY_PROJECT}/orchestration/**/barriers/*.md")
   → Collect cross-pollination artifacts for synthesis

2. Read pipeline outputs:
   Read(file_path="projects/${JERRY_PROJECT}/orchestration/sao-crosspoll-20260112-001/ps/phase-2/agent-a-002/analysis.md")
   → Load agent outputs for pattern extraction

3. Create final synthesis (MANDATORY per P-002):
   Write(
       file_path="projects/${JERRY_PROJECT}/orchestration/sao-crosspoll-20260112-001/synthesis/final-synthesis.md",
       content="# Workflow Synthesis\n\n## L0: Executive Summary\n..."
   )
   → Persist synthesis - transient findings VIOLATES P-002
```

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

*Skill Version: 2.1.0*
*Constitutional Compliance: Jerry Constitution v1.0*
*Enhancement: WI-SAO-064 tool examples and L0/L1/L2 structure (0.830→0.870)*
*Created: 2026-01-10*
*Last Updated: 2026-01-12*
