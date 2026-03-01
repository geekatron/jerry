---
name: orchestration
description: Multi-agent workflow orchestration with state tracking, checkpointing, and cross-pollinated pipelines. Use when coordinating parallel agent pipelines, managing sync barriers, or tracking complex workflow execution state across sessions.
version: "2.2.0"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Task, WebSearch, WebFetch, mcp__memory-keeper__store, mcp__memory-keeper__retrieve, mcp__memory-keeper__search
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

> **Version:** 2.2.0
> **Framework:** Jerry Orchestration (ORCH)
> **Constitutional Compliance:** Jerry Constitution v1.0
> **Industry References:** [Anthropic Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills), [Microsoft AI Agent Patterns](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns), [LangGraph](https://langchain-ai.github.io/langgraph/), [CrewAI Flows](https://docs.crewai.com/concepts/flows)

---

## Document Audience (Triple-Lens)

This SKILL.md serves multiple audiences:

| Level | Audience | Sections to Focus On |
|-------|----------|---------------------|
| **L0 (ELI5)** | Project stakeholders, new users | Purpose, When to Use, [Routing Disambiguation](#routing-disambiguation), Core Artifacts |
| **L1 (Engineer)** | Developers executing workflows | Quick Start, State Schema |
| **L2 (Architect)** | Workflow designers | Workflow Patterns, Adversarial Quality Mode, Constitutional Compliance |

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

See [Routing Disambiguation](#routing-disambiguation) for full exclusion conditions with consequences.

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

## Adversarial Quality Mode

> Adversarial quality enforcement is embedded by default into every orchestrated workflow.
> Constants referenced from `.context/rules/quality-enforcement.md` (SSOT).

### Phase Gate Definitions

Every phase transition in an orchestrated workflow passes through a quality gate. The gate enforces a minimum quality threshold before work proceeds to the next phase.

| Gate Element | Value | Source |
|-------------|-------|--------|
| Quality threshold | >= 0.92 weighted composite | H-13 (quality-enforcement SSOT) |
| Minimum iterations | 3 (creator -> critic -> revision) | H-14 (quality-enforcement SSOT) |
| Scoring mechanism | S-014 (LLM-as-Judge) with dimension rubrics | quality-enforcement SSOT |
| Self-review | REQUIRED before presenting any deliverable | H-15 (quality-enforcement SSOT) |

**Scoring Dimensions** (per quality-enforcement SSOT):

| Dimension | Weight |
|-----------|--------|
| Completeness | 0.20 |
| Internal Consistency | 0.20 |
| Methodological Rigor | 0.20 |
| Evidence Quality | 0.15 |
| Actionability | 0.15 |
| Traceability | 0.10 |

**Gate Outcomes:**
- **PASS** (>= 0.92): Phase proceeds to next stage or barrier
- **REVISE** (< 0.92): Creator receives critic feedback, revision cycle continues
- **ESCALATE**: After 3 failed iterations, escalate to human review (per AE-006)

### Creator-Critic-Revision Cycle at Sync Barriers

At every sync barrier, the orchestrator enforces a creator-critic-revision cycle on cross-pollination artifacts before they flow to the next phase.

```
Phase N Output (Creator)
     │
     ▼
┌─────────────────────────────┐
│  BARRIER QUALITY GATE       │
│                             │
│  1. Creator produces        │
│     deliverable             │
│                             │
│  2. Critic scores with      │
│     S-014 (LLM-as-Judge)    │
│     + S-002 (Devil's        │
│     Advocate) + S-007       │
│     (Constitutional)        │
│                             │
│  3. If score < 0.92:        │
│     → Revision with S-003   │
│       (Steelman) + feedback │
│     → Return to step 2      │
│                             │
│  4. If score >= 0.92:       │
│     → PASS gate             │
│     → Cross-pollinate       │
│                             │
│  5. Circuit breaker:        │
│     max 3 iterations        │
│     → Escalate if all fail  │
└─────────────────────────────┘
     │
     ▼
Phase N+1 Input
```

### Cross-Pollination with Adversarial Critique

Cross-pollination artifacts exchanged at barriers are subject to adversarial review before delivery to the receiving pipeline. This prevents low-quality or assumption-laden findings from propagating across pipelines.

| Direction | Strategy Applied | Purpose |
|-----------|-----------------|---------|
| A-to-B handoff | S-003 (Steelman) + S-002 (Devil's Advocate) | Strengthen claims before sharing; challenge hidden assumptions |
| B-to-A handoff | S-003 (Steelman) + S-002 (Devil's Advocate) | Same adversarial rigor in reverse direction |
| Both directions | S-007 (Constitutional AI Critique) | Verify compliance with Jerry Constitution and rules |

### Quality Gates in Non-Barrier Patterns

Quality gates are not limited to cross-pollinated pipelines with sync barriers. They apply at every phase transition regardless of workflow pattern.

| Pattern | Quality Gate Location | Trigger |
|---------|----------------------|---------|
| Sequential Chain | Between each phase | Phase N output reviewed before Phase N+1 starts |
| Fan-Out | At fan-out origin | Source deliverable reviewed before parallel dispatch |
| Fan-In | At convergence point | Each incoming deliverable reviewed before synthesis |
| Cross-Pollinated | At sync barriers | Both directions reviewed before cross-pollination |
| Divergent-Convergent | At convergence (diamond merge) | All divergent outputs reviewed before merge |
| Review Gate | The gate itself IS the quality gate | Formal review (SRR/PDR/CDR) constitutes the gate |
| Generator-Critic | Each iteration IS a quality cycle | Loop exit requires score >= 0.92 |

For patterns without explicit barriers, the orchestrator enforces the creator-critic-revision cycle at phase boundaries. The same threshold (>= 0.92, H-13) and minimum iterations (3, H-14) apply.

### Strategy Selection for Orchestration Contexts

The orchestrator selects adversarial strategies based on criticality level (per quality-enforcement SSOT). The orch-planner MUST embed the appropriate strategy set when generating workflow plans.

| Criticality | Quality Layer | Strategies (REQUIRED) | Strategies (OPTIONAL) |
|-------------|--------------|----------------------|----------------------|
| C1 (Routine) | L0-L1 | S-010 (Self-Refine) | S-003, S-014 |
| C2 (Standard) | L2 | S-007, S-002, S-014 | S-003, S-010 |
| C3 (Significant) | L3 | C2 + S-004, S-012, S-013 | S-001, S-003, S-010, S-011 |
| C4 (Critical) | L4 | All 10 selected strategies | None -- all required |

**Auto-Escalation** (per quality-enforcement SSOT AE rules):
- Artifacts touching `.context/rules/` = auto-C3 minimum (AE-002)
- Artifacts touching `docs/governance/JERRY_CONSTITUTION.md` = auto-C4 (AE-001)
- Modifying baselined ADRs = auto-C4 (AE-004)
- Security-relevant code changes = auto-C3 minimum (AE-005)
- Token exhaustion at C3+ criticality = human escalation required (AE-006)

### Quality Score Tracking in ORCHESTRATION.yaml

Quality scores are tracked per phase and per barrier in the ORCHESTRATION.yaml state file.

```yaml
# Extension to ORCHESTRATION.yaml schema
quality:
  threshold: 0.92                    # From quality-enforcement SSOT (H-13)
  criticality: "C2"                  # Determined by orch-planner (C1-C4)
  scoring_mechanism: "S-014"         # LLM-as-Judge

  phase_scores:
    phase-1:
      pipeline_a:
        score: 0.94
        iterations: 2
        status: PASS
      pipeline_b:
        score: 0.93
        iterations: 3
        status: PASS

  barrier_scores:
    barrier-1:
      a_to_b:
        score: 0.95
        iterations: 1
        status: PASS
      b_to_a:
        score: 0.92
        iterations: 3
        status: PASS

  workflow_quality:
    average_score: 0.935
    lowest_score: 0.92
    total_iterations: 9
    gates_passed: 4
    gates_failed: 0
```

---

## Constitutional Compliance

| Principle | Requirement | Implementation |
|-----------|-------------|----------------|
| P-002 | File Persistence | All state persisted to ORCHESTRATION.yaml |
| P-003 | No Recursive Subagents | Main context invokes workers only |
| P-010 | Task Tracking | ORCHESTRATION_WORKTRACKER.md updated |
| P-022 | No Deception | Honest status and progress reporting |
| H-13 | Quality threshold >= 0.92 | Phase gates enforce weighted composite scoring |
| H-14 | Creator-critic-revision (3 min) | Adversarial cycle at every sync barrier |
| H-15 | Self-review before presenting | S-010 applied before gate submission |
| WTI-007 | Mandatory Template Usage | Entity files created during orchestration MUST use canonical templates from `.context/templates/worktracker/` |

---

## Templates

| Template | Purpose |
|----------|---------|
| `templates/ORCHESTRATION_PLAN.template.md` | Strategic context with ASCII diagram |
| `templates/ORCHESTRATION_WORKTRACKER.template.md` | Tactical execution tracking |
| `templates/ORCHESTRATION.template.yaml` | Machine-readable state skeleton |

---

## Routing Disambiguation

> When this skill is the wrong choice and what happens if misrouted.

| Condition | Use Instead | Consequence of Misrouting |
|-----------|-------------|--------------------------|
| Single-agent task with no cross-session state | `/problem-solving` | Multi-phase coordination overhead (barrier sync, quality gates, ORCHESTRATION.yaml state tracking) applied to single-step task wastes significant context budget on unnecessary coordination infrastructure |
| Simple sequential flow without parallel pipelines | Direct agent invocation | Orchestration creates three artifacts (ORCHESTRATION_PLAN.md, ORCHESTRATION_WORKTRACKER.md, ORCHESTRATION.yaml) for a workflow that needs none; artifact overhead exceeds task complexity |
| Research, analysis, or root cause investigation | `/problem-solving` | Orchestration agents (orch-planner, orch-tracker, orch-synthesizer) coordinate workflows but have no research or analytical methodology |
| Requirements engineering or V&V activities | `/nasa-se` | Orchestration manages workflow state, not requirements traceability; NPR-compliant artifacts not generated |
| Adversarial quality review or scoring | `/adversary` | Orchestration has no quality scoring rubric or adversarial strategy templates; orch-synthesizer produces workflow synthesis, not quality assessment |
| Transcript parsing or meeting note extraction | `/transcript` | Orchestration has no VTT/SRT parser; transcript-specific agents not available |

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

*Skill Version: 2.2.0*
*Constitutional Compliance: Jerry Constitution v1.0*
*Enhancement: EN-709 Adversarial Quality Mode integration (phase gates, creator-critic-revision, quality scoring)*
*Created: 2026-01-10*
*Last Updated: 2026-02-14*
