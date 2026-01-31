# FEAT-005:DEC-003: Background Execution for Parallel Tracks

<!--
TEMPLATE: Decision
VERSION: 1.0.0
SOURCE: worktracker.md (Decision File), ADR/MADR best practices
CREATED: 2026-01-31 (FEAT-005 Execution Mode Decision)
-->

> **Type:** decision
> **Status:** ACCEPTED
> **Priority:** HIGH
> **Created:** 2026-01-31T05:00:00Z
> **Parent:** FEAT-005
> **Owner:** Claude
> **Related:** FEAT-005:DEC-002

---

## Frontmatter

```yaml
id: "FEAT-005:DEC-003"
work_type: DECISION
title: "Background Execution for Parallel Tracks"
status: ACCEPTED
priority: HIGH
created_by: "Claude"
participants:
  - "User"
  - "Claude"
created_at: "2026-01-31T05:00:00Z"
updated_at: "2026-01-31T05:00:00Z"
decided_at: "2026-01-31T05:00:00Z"
parent_id: "FEAT-005"
tags: ["execution-mode", "parallelism", "background", "task-tool"]
superseded_by: null
supersedes: null
decision_count: 1
```

---

## Summary

**Decision:** Use background execution (`run_in_background: true`) for Track A and Track B agents to enable true parallelism. Phase 0 (TASK-419) uses foreground execution as a blocking gate.

**Key Insight:** Each Task agent gets its own context window. Background execution does NOT degrade quality because:
1. Agents don't share memory with the orchestrator
2. Cross-pollination happens via file artifacts, not shared context
3. Foreground execution would make parallel tracks impossible

---

## Context

### Background

The FEAT-005 orchestration plan v3.0 describes parallel execution of Track A and Track B after Phase 0 completes. The question arose: should agents run in the foreground (blocking) or background (non-blocking)?

### Initial (Incorrect) Analysis

Initially, Claude argued AGAINST background execution, citing:
- Cross-pollination dependencies
- Quality gate feedback loops
- State management race conditions

### User Challenge

The user correctly challenged this analysis:

> "The orchestration plan is supposed to hand the relevant artifacts from the upstream to the next agent. So why would they need to be in the foreground? Each agent gets its own context window doesn't it? How does running them in the foreground help when that means your context window gets more pressure? How would Track A and Track B even be able to run in parallel if they were in the foreground?"

### Corrected Understanding

Upon reconsideration, the key insights are:

1. **Agents have isolated context windows** - A spawned Task agent does NOT share the orchestrator's context. It gets a fresh context window.

2. **Cross-pollination uses files, not shared memory** - Agent A writes to `artifact.md`, Agent B reads from `artifact.md`. This works perfectly with background execution.

3. **Foreground blocks the orchestrator** - If the orchestrator runs EN-027 in foreground, it CANNOT simultaneously spawn TASK-420. The "parallel" tracks become sequential.

4. **State updates are serialized by orchestrator** - The orchestrator (not agents) updates ORCHESTRATION.yaml. Updates happen BETWEEN agent completions, so no race conditions.

---

## Decision

### Question

Should FEAT-005 orchestration use foreground or background execution for Task agents?

### Options Considered

| Option | Description | Pros | Cons |
|--------|-------------|------|------|
| **A** | All foreground | Simpler mental model | **Impossible parallelism** - defeats v3.0 design |
| **B** | All background | Maximum parallelism | Phase 0 is blocking anyway |
| **C** | Hybrid: Phase 0 foreground, Tracks background | True parallelism where needed, simplicity where appropriate | Slightly more complex |

### Decision

**We decided:** Option C - Hybrid execution mode.

| Component | Execution Mode | Rationale |
|-----------|---------------|-----------|
| Phase 0 (TASK-419) | **Foreground** | Blocking gate - nothing can start until PASS/FAIL known |
| Track A agents | **Background** | Enable parallelism with Track B |
| Track B agents | **Background** | Enable parallelism with Track A |
| ps-critic | **Foreground** | Quick evaluation, simpler iterative refinement |

---

## Rationale

### Why Foreground for Phase 0

```
TASK-419: Validate Task tool model parameter
    │
    ├── Result determines if EN-031 is viable
    ├── Result informs EN-027 agent definition design (CP-1)
    └── NOTHING can proceed until we know PASS/FAIL

Running in background provides zero benefit:
- We'd spawn it, then immediately poll/wait
- Same wall-clock time, extra complexity
- Foreground is simpler
```

### Why Background for Parallel Tracks

```
FOREGROUND (impossible parallelism):
═══════════════════════════════════════════════════════════
Orchestrator: Spawn EN-027 → BLOCKED → Wait 10h → Returns
              Now spawn TASK-420 → BLOCKED → Wait 8h → Returns
              Track B didn't start until Track A step 1 finished!
═══════════════════════════════════════════════════════════

BACKGROUND (true parallelism):
═══════════════════════════════════════════════════════════
Orchestrator: Spawn EN-027 (background) → output_file_A
              Spawn TASK-420 (background) → output_file_B
              Spawn TASK-421 (background) → output_file_C
              │
              ├── EN-027 running in context window A
              ├── TASK-420 running in context window B
              └── TASK-421 running in context window C

              ALL THREE progressing simultaneously!
═══════════════════════════════════════════════════════════
```

### Why Quality Gates Still Work

The iterative refinement loop is orchestrated by the ORCHESTRATOR, not inside agents:

```
Iteration 1:
1. EN-027 (background) completes → writes to file
2. Orchestrator reads output
3. ps-critic (foreground) evaluates → score 0.85
4. Score < 0.90 → REFINE needed

Iteration 2:
5. Orchestrator spawns refinement agent with findings → (background)
6. Refinement completes → writes updated file
7. ps-critic evaluates → score 0.92
8. Score >= 0.90 → PASS
```

Each individual agent is atomic. The iteration happens between agents, controlled by the orchestrator.

### Why No Race Conditions

```
YAML Update Sequence (serialized by orchestrator):
═══════════════════════════════════════════════════
1. EN-027 completes → Orchestrator updates YAML
2. TASK-420 completes → Orchestrator updates YAML
3. TASK-421 completes → Orchestrator updates YAML

Updates are NEVER concurrent. The orchestrator waits for
an agent to complete, THEN updates, THEN proceeds.
Agents don't update YAML directly.
═══════════════════════════════════════════════════
```

---

## Implications

### Positive

- **True parallelism achieved** - Track A and Track B progress simultaneously
- **Reduced wall-clock time** - 6 days instead of 12+ days sequential
- **Orchestrator context preserved** - Agent working output doesn't flood main context
- **Correct interpretation of v3.0 plan** - Plan said "parallel" and now it actually is

### Negative

- **Slightly more complex orchestration** - Must track output_file paths, poll for completion
- **Requires careful dependency management** - Must not spawn agent until dependencies are met

### Follow-up Required

- Update ORCHESTRATION_WORKTRACKER.md with execution mode section
- Ensure TASK-419 file includes instruction to use foreground
- Document polling/waiting strategy in RUNBOOK

---

## Execution Mode Specification

```yaml
execution:
  phase_0:
    mode: foreground
    tasks: [TASK-419]
    rationale: "Blocking gate - must know result before any parallel work"

  track_a:
    mode: background
    agents: [EN-027, EN-028, EN-029, EN-030]
    rationale: "Enable parallelism with Track B"

  track_b:
    mode: background
    agents: [TASK-420, TASK-421, TASK-422, TASK-423, TASK-424]
    rationale: "Enable parallelism with Track A"

  ps_critic:
    mode: foreground
    rationale: "Quick evaluation, simpler iterative refinement"

  orchestrator_protocol:
    spawn: "Use Task tool with run_in_background: true"
    track: "Store output_file paths for each agent"
    poll: "Use TaskOutput or Read to check completion"
    update: "Update YAML after each completion, before spawning dependents"
```

---

## Example: Day 1 Parallel Execution

```
09:00 - Phase 0 complete (G-PHASE0 PASS)
        │
        ▼
09:05 - Orchestrator spawns parallel:
        ├── Task(EN-027, run_in_background=true) → output_file_A
        ├── Task(TASK-420, run_in_background=true) → output_file_B
        └── Task(TASK-421, run_in_background=true) → output_file_C

09:10 - Orchestrator continues (not blocked!)
        ├── Can update status
        ├── Can respond to user
        └── Can check progress

14:00 - Poll: EN-027 complete
        ├── Read output_file_A
        ├── Update YAML: EN-027 COMPLETE
        ├── Spawn ps-critic for G-027 (foreground)
        └── G-027 PASS → TASK-422 now unblocked

14:30 - Spawn TASK-422 (background) - has CP-2 data from EN-027

15:00 - Poll: TASK-420 complete
        ├── Read output_file_B
        ├── Update YAML: TASK-420 COMPLETE
        └── CP-3 now available for EN-028

... and so on
```

---

## Related Artifacts

| Type | Path | Description |
|------|------|-------------|
| Parent | [FEAT-005](./FEAT-005-skill-compliance.md) | Parent feature |
| Related | [DEC-002](./FEAT-005--DEC-002-orchestration-v3-design-decisions.md) | v3.0 design decisions |
| Reference | [ORCHESTRATION.yaml](./orchestration/ORCHESTRATION.yaml) | Updated with execution section |

---

## Document History

| Date | Author | Change |
|------|--------|--------|
| 2026-01-31T05:00:00Z | Claude | Created decision based on user correction |

---

## Metadata

```yaml
id: "FEAT-005:DEC-003"
parent_id: "FEAT-005"
work_type: DECISION
title: "Background Execution for Parallel Tracks"
status: ACCEPTED
priority: HIGH
created_by: "Claude"
created_at: "2026-01-31T05:00:00Z"
updated_at: "2026-01-31T05:00:00Z"
decided_at: "2026-01-31T05:00:00Z"
participants: [User, Claude]
tags: [execution-mode, parallelism, background, task-tool]
decision_count: 1
superseded_by: null
supersedes: null
```
