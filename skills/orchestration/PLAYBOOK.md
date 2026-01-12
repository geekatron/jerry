# Orchestration Playbook

> **Version:** 2.0.0
> **Skill:** orchestration
> **Purpose:** Step-by-step guide for multi-agent workflow orchestration
> **Updated:** 2026-01-10 - Dynamic path scheme

---

## Quick Start

### 1. Initialize Orchestration Artifacts

When starting a new multi-agent workflow:

```
"Initialize orchestration for PROJ-XXX with a cross-pollinated pipeline
 using problem-solving and nasa-systems-engineering skills"
```

This creates:
- `ORCHESTRATION_PLAN.md` - Strategic context
- `ORCHESTRATION_WORKTRACKER.md` - Tactical tracking
- `ORCHESTRATION.yaml` - Machine-readable state

The planner will generate a workflow ID (e.g., `sao-crosspoll-20260110-001`) and
configure pipeline aliases based on skill defaults or user overrides.

### 2. Execute Agents

After planning, execute agents in priority order:

```
"Execute agent-a-001 for Phase 1 research"
```

### 3. Update State

After each agent completes, reference the dynamic path:

```
"Update orchestration: agent-a-001 complete,
 artifact at orchestration/{workflow_id}/{pipeline_alias}/phase-1/research.md"
```

The tracker will resolve placeholders using values from ORCHESTRATION.yaml.

### 4. Check Progress

```
"Show orchestration status"
```

### 5. Final Synthesis

When all phases complete:

```
"Create final orchestration synthesis"
```

---

## Workflow: Cross-Pollinated Pipeline

### Phase 1: Plan the Workflow

**Goal:** Create comprehensive orchestration plan with workflow diagram.

**Steps:**

1. Define pipelines and their purposes
2. Identify phases within each pipeline
3. Assign agents to phases
4. Define sync barriers and cross-pollination artifacts
5. Create ASCII workflow diagram

**Artifacts Created:**
- `ORCHESTRATION_PLAN.md`
- `ORCHESTRATION.yaml`
- `ORCHESTRATION_WORKTRACKER.md`

### Phase 2: Execute Pipeline Phases

**Goal:** Run agents according to execution queue.

**For each execution group:**

1. Check group status in ORCHESTRATION.yaml
2. If READY, execute agents (parallel or sequential)
3. After each agent completes:
   - Update agent status in ORCHESTRATION.yaml
   - Register artifact path
   - Update metrics
4. When all agents in group complete, create checkpoint

**State Updates:**

```yaml
# Configuration (from workflow)
workflow:
  id: "sao-crosspoll-20260110-001"
pipelines:
  pipeline_a:
    short_alias: "ps"

# Before agent execution
agents:
  - id: "agent-a-001"
    status: "PENDING"
    artifact: null

# After agent execution (resolved path with agent-level isolation - AC-012-004)
agents:
  - id: "agent-a-001"
    status: "COMPLETE"
    artifact: "orchestration/sao-crosspoll-20260110-001/ps/phase-1/agent-a-001/research.md"
```

### Phase 3: Cross Barriers

**Goal:** Exchange findings between pipelines at sync barriers.

**For each barrier:**

1. Verify all prerequisite phases are COMPLETE
2. Extract key findings from pipeline A
3. Create cross-pollination artifact (a→b)
4. Extract key findings from pipeline B
5. Create cross-pollination artifact (b→a)
6. Mark barrier as COMPLETE
7. Create checkpoint

**Barrier Artifact Format:**

```markdown
# Barrier N: {Direction} Cross-Pollination

> **Source Pipeline:** {pipeline}
> **Target Pipeline:** {pipeline}
> **Phase Transition:** {from_phase} → {to_phase}

## Key Findings
{extracted findings}

## For Target Pipeline
{how to use these findings}
```

### Phase 4: Final Synthesis

**Goal:** Create consolidated synthesis of all workflow findings.

**Steps:**

1. Verify all phases COMPLETE
2. Verify all barriers COMPLETE
3. Read all phase artifacts
4. Read all barrier artifacts
5. Extract cross-cutting patterns
6. Create synthesis with L0/L1/L2
7. Mark workflow as COMPLETE

---

## Common Scenarios

### Scenario: Agent Fails

```yaml
# In ORCHESTRATION.yaml
agents:
  - id: "agent-a-001"
    status: "FAILED"
    artifact: null

blockers:
  active:
    - id: "BLK-001"
      description: "agent-a-001 failed: Task tool connection error"
      blocking: ["barrier-1"]
      severity: "HIGH"
```

**Resolution Options:**

1. **Retry:** Re-execute the agent
2. **Manual:** Create artifact manually
3. **Skip:** Mark as COMPLETE with justification

### Scenario: Resume from Checkpoint

```
"Resume orchestration from checkpoint CP-003"
```

**Steps:**
1. Read checkpoint recovery_point
2. Reset agents after checkpoint to PENDING
3. Continue execution from recovery point

### Scenario: Add Agent Mid-Workflow

1. Update ORCHESTRATION.yaml phases.agents
2. Add to appropriate execution_queue group
3. Update metrics.agents_total
4. Continue execution

---

## Best Practices

### 1. Update State Immediately

After every agent completion, update ORCHESTRATION.yaml immediately.
Don't batch updates.

### 2. Create Checkpoints Frequently

At minimum, create checkpoints:
- After each phase completes
- After each barrier is crossed
- Before any risky operation

### 3. Keep Artifacts Small

Cross-pollination artifacts should be summaries, not full copies.
Reference original artifacts rather than duplicating content.

### 4. Use Parallel Execution Wisely

Only parallelize truly independent work.
If agents share inputs, run sequentially to avoid race conditions.

### 5. Monitor Metrics

Check progress regularly:
- agents_executed vs agents_total
- phases_complete vs phases_total
- agent_success_rate

---

## Troubleshooting

### Problem: ORCHESTRATION.yaml Out of Sync

**Symptoms:** Markdown documents don't match YAML state

**Fix:**
1. YAML is SSOT - trust it over markdown
2. Regenerate markdown from YAML
3. Or manually reconcile and update both

### Problem: Barrier Stuck

**Symptoms:** Barrier status stays PENDING despite phases complete

**Check:**
1. All prerequisite phases are truly COMPLETE
2. No FAILED agents in prerequisite phases
3. No active blockers preventing barrier

### Problem: Context Window Issues

**Symptoms:** Claude loses track of workflow state

**Fix:**
1. Read ORCHESTRATION.yaml (it's the SSOT)
2. Check latest checkpoint for recovery
3. Use resumption.files_to_read list

---

## Templates Reference

| Template | Location | Purpose |
|----------|----------|---------|
| ORCHESTRATION_PLAN.template.md | `skills/orchestration/templates/` | Strategic context |
| ORCHESTRATION_WORKTRACKER.template.md | `skills/orchestration/templates/` | Tactical tracking |
| ORCHESTRATION.template.yaml | `skills/orchestration/templates/` | State skeleton |

---

*Playbook Version: 2.0.0*
*Skill: orchestration*
*Updated: 2026-01-10 - Dynamic path scheme*
