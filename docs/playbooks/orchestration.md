# Orchestration Playbook

> **Skill:** orchestration
> **SKILL.md:** [orchestration/SKILL.md](../../skills/orchestration/SKILL.md)
> **Trigger keywords:** orchestration, pipeline, workflow, multi-agent, phases, gates

## Document Sections

| Section | Purpose |
|---------|---------|
| [When to Use](#when-to-use) | Activation criteria and exclusions |
| [Prerequisites](#prerequisites) | What must be in place before invoking |
| [Workflow Patterns](#workflow-patterns) | The 3 structural patterns with diagrams |
| [Core Artifacts](#core-artifacts) | The 3 artifacts every orchestration creates |
| [Available Agents](#available-agents) | orch-planner, orch-tracker, orch-synthesizer |
| [P-003 Compliance](#p-003-compliance) | No recursive subagents — practical implication |
| [Step-by-Step](#step-by-step) | Primary invocation path |
| [Examples](#examples) | Concrete invocation examples |
| [Troubleshooting](#troubleshooting) | Common failure modes |
| [Related Resources](#related-resources) | Cross-references to SKILL.md and other playbooks |

---

## When to Use

### Use this skill when:

- You need **orchestration** of 3 or more agents in a structured workflow — include the keyword `orchestration` in your request to signal this skill.
- You are designing a multi-step **pipeline** — references to pipeline coordination signal this skill.
- Your task requires a **workflow** spanning multiple Claude Code sessions and needs persistent state tracking.
- You need to coordinate **multi-agent** work, especially parallel agents that produce artifacts consumed by each other.
- Your work is organized into **phases** with gates between them — each phase requires completion before the next begins.
- You need to define quality **gates** between work phases, enforcing a minimum quality threshold (>= 0.92) before proceeding.
- You are running parallel agent pipelines that need synchronization (cross-pollination) at defined barrier points.
- You need checkpoint recovery — the ability to resume a long-running workflow from a known-good state if a session ends before completion.
- You require visibility into complex workflow progress with metrics (phases complete, agents executed, success rates).

### Do NOT use this skill when:

- The task involves only a **single agent** — use the problem-solving skill instead. Orchestration adds overhead that is unnecessary for single-agent work.
- The work follows a **simple sequential flow** with no parallel pipelines and no need for state persistence across sessions — use direct agent invocation in sequence.
- **No cross-session state** is needed — if the entire task completes within one Claude Code session with no need to resume, orchestration's persistent state tracking provides no benefit.

---

## Prerequisites

- `JERRY_PROJECT` environment variable is set to the active project ID (required by H-04 before any work proceeds).
- An active Jerry session is running (`jerry session start` completed).
- You have identified 3 or more agents that will participate in the workflow — orchestration is not warranted below this threshold.
- You have a rough understanding of the workflow structure: whether work is sequential, parallel, or a combination.
- The project directory `projects/{JERRY_PROJECT}/` exists with a `PLAN.md` describing the project scope (orch-planner reads this to understand workflow context).
- If continuing an existing workflow: the `ORCHESTRATION.yaml` state file must exist in `projects/{JERRY_PROJECT}/orchestration/{workflow_id}/`.

---

## Workflow Patterns

The orchestration skill supports three structural patterns. Every orchestrated workflow uses one of these patterns or a hybrid. orch-planner selects and documents the pattern in `ORCHESTRATION_PLAN.md`.

### Pattern 1: Cross-Pollinated Pipeline

Two or more pipelines run in parallel. At synchronization barriers, each pipeline shares its findings with the other (cross-pollination). Work after the barrier incorporates insights from both pipelines.

**Use when:** Two independent analytical paths (e.g., problem-solving + systems-engineering) must each inform the other's next phase. Neither pipeline's Phase 2 can begin until both pipelines complete Phase 1.

```
Pipeline A                    Pipeline B
    |                              |
    v                              v
+----------+                 +----------+
| Phase 1  |                 | Phase 1  |
+----+-----+                 +-----+----+
     |                             |
     +------------+----------------+
                  v
          +=================+
          |    BARRIER 1    |  <- Cross-pollination
          +=================+
                  |
     +------------+----------------+
     |                             |
     v                             v
+----------+                 +----------+
| Phase 2  |                 | Phase 2  |
+----------+                 +----------+
```

Artifacts exchanged at each barrier are subject to adversarial quality review (S-003 Steelman + S-002 Devil's Advocate + S-007 Constitutional check) before crossing to the receiving pipeline.

### Pattern 2: Sequential with Checkpoints

A single pipeline of phases executed in order. Each phase transition creates a checkpoint — a recovery point that allows the workflow to resume from that phase if the session ends before completion.

**Use when:** Work is inherently sequential (each phase builds directly on the previous), but the total work spans multiple sessions or is too long to complete reliably in one run.

```
+----------+     +----------+     +----------+
| Phase 1  |---->| Phase 2  |---->| Phase 3  |
+----------+     +----------+     +----------+
     |                |                |
     v                v                v
   CP-001           CP-002           CP-003
```

Each checkpoint (`CP-NNN`) is recorded in `ORCHESTRATION.yaml` with a timestamp and recovery point reference. If a session ends at Phase 2, the next session reads the YAML, finds `CP-002`, and resumes from Phase 3.

### Pattern 3: Fan-Out / Fan-In

Work dispatched to multiple parallel agents, then collected and synthesized into a single output. Agents in the fan-out phase operate independently; the fan-in phase cannot begin until all fan-out agents have completed.

**Use when:** A task can be decomposed into independent parallel workstreams (e.g., 3 agents each analyze a different risk domain) that must be integrated by a synthesizer agent.

```
              +----------+
              |  Start   |
              +----+-----+
        +----------+-----------+
        v          v           v
   +--------+  +--------+  +--------+
   |Agent A |  |Agent B |  |Agent C |
   +----+---+  +----+---+  +----+---+
        +----------+-----------+
                   v
            +-------------+
            |  Synthesize  |
            +-------------+
```

Each fan-out agent writes to its own isolated subdirectory (`orchestration/{workflow_id}/{pipeline_alias}/phase-{N}/{agent_id}/`) to prevent file collisions. The fan-in synthesizer reads all agent outputs and produces a unified synthesis artifact.

---

## Core Artifacts

Every orchestrated workflow creates exactly three artifacts. These artifacts are created by orch-planner at workflow start and updated by orch-tracker after each agent completes. They serve different audiences and purposes.

| Artifact | Format | Purpose | Audience |
|----------|--------|---------|----------|
| `ORCHESTRATION_PLAN.md` | Markdown | Strategic context: workflow ID, chosen pattern, ASCII diagram, agent list, phase definitions, quality gate configuration | Humans — project managers, reviewers, human escalation points |
| `ORCHESTRATION_WORKTRACKER.md` | Markdown | Tactical execution documentation: per-agent status narrative, decisions made, blockers encountered, artifacts produced | Humans — developers running the workflow, post-workflow review |
| `ORCHESTRATION.yaml` | YAML | Machine-readable state (single source of truth): current phase, agent statuses, checkpoint history, quality scores, execution queue | Claude/Automation — orch-tracker reads and updates this file; it is the state that enables cross-session resumption |

**Location:** All three artifacts are placed at `projects/{JERRY_PROJECT}/orchestration/{workflow_id}/`.

**Why all three are required:**

- `ORCHESTRATION_PLAN.md` captures the intent and design — without it, a human reviewer cannot understand why the workflow was structured the way it was.
- `ORCHESTRATION_WORKTRACKER.md` captures the execution narrative — without it, a human resuming a paused workflow has no context about what decisions were made mid-execution.
- `ORCHESTRATION.yaml` is the machine state — without it, cross-session resumption is impossible. It is the only artifact that orch-tracker can reliably update programmatically.

Discarding any one of the three in favor of in-memory state violates [P-002](../governance/JERRY_CONSTITUTION.md#p-002-file-persistence) (file persistence requirement).

---

## Available Agents

The orchestration skill provides three specialized agents. Each is invoked by the main Claude Code context (never by each other — see P-003 Compliance below).

| Agent | Role | Primary Output |
|-------|------|----------------|
| `orch-planner` | Reads project context, determines workflow pattern, generates workflow ID, creates all three core artifacts with the workflow diagram and initial state | `ORCHESTRATION_PLAN.md`, initial `ORCHESTRATION.yaml`, initial `ORCHESTRATION_WORKTRACKER.md` |
| `orch-tracker` | Reads `ORCHESTRATION.yaml`, updates agent statuses after completion, records checkpoint entries, updates quality scores, reconciles artifact paths | Updated `ORCHESTRATION.yaml`, updated `ORCHESTRATION_WORKTRACKER.md` |
| `orch-synthesizer` | Reads all pipeline outputs and barrier artifacts, extracts patterns and decisions, produces the final workflow synthesis document | `orchestration/{workflow_id}/synthesis/workflow-synthesis.md` |

Agent specifications: [`orch-planner.md`](../../skills/orchestration/agents/orch-planner.md), [`orch-tracker.md`](../../skills/orchestration/agents/orch-tracker.md), [`orch-synthesizer.md`](../../skills/orchestration/agents/orch-synthesizer.md).

---

## P-003 Compliance

**P-003 (No Recursive Subagents):** Agents invoked by the orchestration skill are workers. They do NOT spawn other agents. The main Claude Code context is the sole orchestrator.

```
MAIN CONTEXT (Claude)  <-- Orchestrator
    |
    +---> orch-planner       (creates plan and initial state)
    +---> ps-agent-001       (Phase 1 work, Pipeline A)
    +---> nse-agent-001      (Phase 1 work, Pipeline B)
    +---> orch-tracker       (updates state after each agent)
    +---> orch-synthesizer   (final synthesis)

Each is a WORKER. None spawn other agents.
```

**Practical implication for users:** When you invoke the orchestration skill, you are asking the main Claude Code context to act as the orchestrator — it calls orch-planner, then dispatches work agents, then calls orch-tracker, and finally calls orch-synthesizer. You should NOT ask orch-planner to "orchestrate the workflow" or "spawn the work agents" — orch-planner only creates the plan document. The main context drives execution, not orch-planner.

**Violation pattern to avoid:** Do NOT structure a request as "use orch-planner to coordinate all the agents." orch-planner is a plan-creation worker. The correct structure is: "create an orchestration plan using orch-planner, then I will run the phases, and we will use orch-tracker to update state after each phase."

---

## Step-by-Step

### Primary Path: New cross-pollinated or sequential workflow

> **Note on keyword detection:** Skill activation via keywords is probabilistic — the LLM interprets your intent from context, not via exact string matching. If keyword detection does not activate the orchestration skill, use explicit invocation: `/orchestration` or name the agent directly (e.g., "Use orch-planner to create a workflow plan").

1. **Confirm prerequisites.** Verify `JERRY_PROJECT` is set and an active session exists. Identify the 3+ agents and the workflow pattern (cross-pollinated, sequential with checkpoints, or fan-out/fan-in).

2. **Invoke orch-planner.** Ask Claude to create an orchestration plan. Provide the workflow description, the skills/agents involved, and any alias preferences. Example: "Create an orchestration plan for a cross-pollinated pipeline using problem-solving (alias: ps) and nasa-se (alias: nse)."

3. **Review the generated artifacts.** orch-planner creates `ORCHESTRATION_PLAN.md`, `ORCHESTRATION_WORKTRACKER.md`, and `ORCHESTRATION.yaml` at `projects/{JERRY_PROJECT}/orchestration/{workflow_id}/`. Verify the workflow diagram in `ORCHESTRATION_PLAN.md` matches your intent before proceeding.

4. **Execute Phase 1 agents.** Invoke the Phase 1 work agents as specified in the plan. For parallel pipelines, dispatch both pipelines' Phase 1 agents. Each agent writes its output to its assigned subdirectory under `orchestration/{workflow_id}/{pipeline_alias}/phase-1/{agent_id}/`.

5. **Update state after each agent.** After each agent completes, invoke orch-tracker to update `ORCHESTRATION.yaml` and `ORCHESTRATION_WORKTRACKER.md`. Provide the agent ID, completion status, and artifact path. orch-tracker also records quality scores if the phase gate has been evaluated.

6. **Evaluate quality gate before advancing.** At each phase boundary (or barrier for cross-pollinated pipelines), the phase output must score >= 0.92 on the [S-014 quality rubric](../../.context/rules/quality-enforcement.md) before the next phase begins. If below threshold, a revision cycle is required before proceeding.

7. **Cross-pollinate at barriers (cross-pollinated pattern only).** When both Pipeline A and Pipeline B complete a phase, exchange barrier artifacts. Each pipeline's findings are delivered to the other pipeline as input for the next phase. orch-tracker records barrier completion in `ORCHESTRATION.yaml`.

8. **Repeat for subsequent phases.** Continue executing phase agents, updating state, and evaluating quality gates until all phases are complete.

9. **Invoke orch-synthesizer.** When all phases are complete, invoke orch-synthesizer to produce `synthesis/workflow-synthesis.md`. The synthesizer reads all pipeline outputs and barrier artifacts and extracts cross-cutting patterns, decisions, and recommendations.

10. **Verify final state.** Check `ORCHESTRATION.yaml` — `workflow.status` should be `COMPLETE`. Review `ORCHESTRATION_WORKTRACKER.md` for the execution narrative. The synthesis document is the primary human-consumable output.

---

## Examples

### Example 1: Cross-pollinated research and engineering pipeline

**User request:** "I need to orchestrate a multi-phase workflow that cross-pollinates a problem-solving research pipeline with a systems-engineering requirements pipeline. The workflow will run over multiple sessions."

**System behavior:** Claude recognizes keywords `orchestrate`, `multi-phase`, `workflow`, `cross-pollinates`, and `multiple sessions` — the orchestration skill is activated automatically. Claude invokes `orch-planner`, which reads `PLAN.md` from the active project, generates a workflow ID (e.g., `sao-crosspoll-20260218-001`), selects Pattern 1 (Cross-Pollinated Pipeline), creates the workflow diagram, and writes all three core artifacts to `projects/{JERRY_PROJECT}/orchestration/sao-crosspoll-20260218-001/`. Claude presents the workflow diagram from `ORCHESTRATION_PLAN.md` for review. Subsequent execution proceeds phase by phase with orch-tracker updates and quality gate evaluation at each barrier.

### Example 2: Fan-out analysis across parallel agents

**User request:** "Set up an orchestration pipeline with three agents analyzing different risk domains in parallel, then synthesize their findings into one report."

**System behavior:** Claude activates the orchestration skill on keywords `orchestration`, `pipeline`, `parallel`. Claude invokes `orch-planner` with the fan-out/fan-in pattern. orch-planner generates a workflow ID, creates `ORCHESTRATION_PLAN.md` with Pattern 3 (Fan-Out/Fan-In) diagram, and initializes `ORCHESTRATION.yaml` with three parallel agents in Phase 1 and one synthesizer agent in Phase 2. After the user approves the plan, Claude dispatches the three Phase 1 agents (each writes to its own isolated agent subdirectory). After all three complete, orch-tracker records their completion, the quality gate is evaluated at the fan-in point, and orch-synthesizer is invoked to produce the unified synthesis document.

### Example 3: Resuming a workflow after session interruption

**User request:** "Resume the orchestration workflow — we completed Phase 1 and Phase 2 last session, and we need to continue from Phase 3."

**System behavior:** Claude reads `ORCHESTRATION.yaml` (the state SSOT) from the active project's orchestration directory. The YAML shows `workflow.status: ACTIVE`, `current_phase: 3`, and the two completed checkpoints (`CP-001`, `CP-002`). Claude reads `ORCHESTRATION_WORKTRACKER.md` for the execution narrative, identifies which agents are pending in Phase 3 from the execution queue, and resumes exactly where the previous session left off. No artifacts are recreated; state is restored from the persisted YAML.

---

## Troubleshooting

| Symptom | Cause | Resolution |
|---------|-------|------------|
| orch-planner writes artifacts to the wrong directory | `JERRY_PROJECT` environment variable not set or set to wrong value | Verify `JERRY_PROJECT` matches the intended project ID: `echo $JERRY_PROJECT`. Set it explicitly before invoking the skill. |
| `ORCHESTRATION.yaml` not found when resuming a workflow | The YAML was never created (plan-only invocation), or the workflow ID changed between sessions | Check `projects/{JERRY_PROJECT}/orchestration/` for existing workflow directories. If the YAML is missing, re-run orch-planner to recreate the artifact using the same workflow ID. |
| orch-tracker shows stale agent statuses after a phase completes | orch-tracker was not invoked after the agent completed — state was only updated in-memory | Always invoke orch-tracker explicitly after each agent completes. Provide the agent ID, status (COMPLETE/FAILED), and artifact path. In-memory-only state violates [P-002](../governance/JERRY_CONSTITUTION.md#p-002-file-persistence) and is lost at session end. |
| Quality gate is never evaluated — workflow advances phases without scoring | The creator-critic-revision cycle was skipped between phases | Quality gates are not automatic — the orchestrator (main Claude context) must evaluate phase output against the S-014 rubric before invoking orch-tracker to advance the phase. If a phase is advanced without a gate check, the YAML's quality section will show no score for that phase. |
| orch-planner spawns other agents instead of just creating the plan | User asked orch-planner to "coordinate the workflow" or "run all the agents" — violates P-003 | Correct the request: orch-planner creates the plan document only. The main Claude context drives execution. Rephrase as: "use orch-planner to create the orchestration plan, then we will execute the phases together." |
| Two parallel agents write to the same artifact path, overwriting each other | Agent-level directory isolation was not used — agents shared a directory without unique filenames | Each agent must write to its own subdirectory: `orchestration/{workflow_id}/{pipeline_alias}/phase-{N}/{agent_id}/`. Verify the paths in `ORCHESTRATION.yaml` for each agent include the agent ID as a path component. |
| Barrier cross-pollination artifacts are not reviewed before delivery | The adversarial quality cycle at the barrier was skipped | Before delivering barrier artifacts to the receiving pipeline, apply S-003 (Steelman) + S-002 (Devil's Advocate) + S-007 (Constitutional check) to the artifacts. Only artifacts that pass the quality gate (>= 0.92) should cross-pollinate to the next phase. |
| Agent fails mid-execution during a phase (partial artifact or no output) | Agent encountered an error, token budget exhaustion, or session interruption | **1. Identify:** Check `ORCHESTRATION.yaml` — the failed agent's status will show `IN_PROGRESS` with no artifact path. Check the agent's output directory for partial files. **2. Salvage:** If a partial artifact exists, it can be used as input for re-invocation. **3. Recover:** Use checkpoint recovery — read the latest checkpoint from `ORCHESTRATION.yaml`, re-invoke the failed agent targeting its assigned output path, then call orch-tracker to update the state. The workflow resumes from the checkpoint without re-executing completed agents. |

---

## Related Resources

- [SKILL.md](../../skills/orchestration/SKILL.md) — Authoritative technical reference for the orchestration skill, including complete state schema, workflow configuration options, pipeline alias resolution, and adversarial quality mode details
- [Quality Enforcement Standards](../../.context/rules/quality-enforcement.md) — SSOT for quality gate thresholds, criticality levels (C1–C4), strategy catalog (S-001–S-014), and auto-escalation rules (AE-001–AE-006)
- [problem-solving.md](./problem-solving.md) — Problem-solving skill playbook; the problem-solving skill is frequently used as a pipeline within orchestrated workflows (ps-pipeline is the conventional Pipeline A in cross-pollinated patterns)
- [transcript.md](./transcript.md) — Transcript skill playbook; transcript parsing produces structured data that can serve as input to orchestrated analysis workflows
