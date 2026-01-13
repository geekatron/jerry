# ORCHESTRATION.yaml State Schema

> **Version:** 1.0.0
> **Skill:** orchestration
> **Format:** YAML 1.2

---

## Overview

The ORCHESTRATION.yaml file is the **Single Source of Truth (SSOT)** for workflow execution state. This document defines the complete schema specification.

---

## Schema Definition

### Root Structure

```yaml
workflow:         # Workflow metadata and configuration
pipelines:        # Pipeline definitions with phases and agents
barriers:         # Sync barrier definitions
execution_queue:  # Priority-ordered execution groups
checkpoints:      # Recovery checkpoint log
metrics:          # Execution and quality metrics
blockers:         # Active and resolved issues
next_actions:     # Immediate and subsequent actions
resumption:       # Cross-session resumption context
```

---

## Workflow Section

```yaml
workflow:
  id: string                    # REQUIRED. Unique workflow identifier
  name: string                  # REQUIRED. Human-readable name
  project_id: string            # REQUIRED. Project this workflow belongs to
  version: string               # Workflow version (semver)
  created_at: ISO-8601          # When workflow was created
  updated_at: ISO-8601          # Last modification timestamp
  status: enum                  # ACTIVE | PAUSED | COMPLETE | FAILED | CANCELLED

  patterns:                     # List of orchestration patterns used
    - enum                      # SEQUENTIAL | CONCURRENT | BARRIER_SYNC | HIERARCHICAL | FAN_OUT

  constraints:                  # Execution constraints
    max_agent_nesting: integer  # P-003: Must be 1
    file_persistence: boolean   # P-002: Must be true
    user_authority: boolean     # P-020: Must be true
    max_concurrent_agents: integer  # Soft limit (default: 5)
    max_barrier_retries: integer    # Circuit breaker (default: 2)
    checkpoint_frequency: enum  # AGENT | PHASE | BARRIER
```

---

## Pipelines Section

```yaml
pipelines:
  {pipeline_id}:                # Pipeline identifier (e.g., "ps", "nse")
    id: string                  # REQUIRED. Same as key
    name: string                # REQUIRED. Human-readable name
    description: string         # Pipeline purpose
    status: enum                # PHASE_N_PENDING | PHASE_N_IN_PROGRESS | COMPLETE
    current_phase: integer      # Currently active phase number
    total_phases: integer       # Total phases in pipeline
    progress_percent: integer   # 0-100

    phases:                     # List of phase definitions
      - id: integer             # REQUIRED. Phase number (1-indexed)
        name: string            # REQUIRED. Phase name
        status: enum            # PENDING | IN_PROGRESS | COMPLETE | BLOCKED
        blocked_by: string      # If BLOCKED, what is blocking (barrier/phase)
        started_at: ISO-8601    # When phase started (null if not started)
        completed_at: ISO-8601  # When phase completed (null if not complete)

        agents:                 # List of agents in this phase
          - id: string          # REQUIRED. Agent identifier
            name: string        # Human-readable agent name
            status: enum        # PENDING | IN_PROGRESS | COMPLETE | FAILED | BLOCKED
            artifact: string    # Path to output artifact (null if not created)
            inputs:             # List of input artifact paths
              - string

        artifacts:              # List of artifact paths created by this phase
          - string
```

---

## Barriers Section

```yaml
barriers:
  - id: string                  # REQUIRED. Barrier identifier (e.g., "barrier-1")
    name: string                # Human-readable name
    status: enum                # PENDING | IN_PROGRESS | COMPLETE
    completed_at: ISO-8601      # When barrier was crossed (null if not complete)

    depends_on:                 # What must complete before barrier can start
      - string                  # Format: "{pipeline_id}.phase.{phase_number}"

    artifacts:                  # Cross-pollination artifacts
      {direction}:              # e.g., "a_to_b", "b_to_a"
        path: string            # Path to artifact
        status: enum            # PENDING | IN_PROGRESS | COMPLETE
        key_content: string     # Summary of artifact content (null if not created)
```

---

## Execution Queue Section

```yaml
execution_queue:
  current_group: integer        # Currently executing group number

  groups:                       # Ordered list of execution groups
    - id: integer               # REQUIRED. Group number (1-indexed)
      name: string              # Human-readable group name
      execution_mode: enum      # PARALLEL | SEQUENTIAL
      status: enum              # READY | IN_PROGRESS | COMPLETE | BLOCKED
      blocked_by: string        # If BLOCKED, what is blocking

      agents:                   # List of agent IDs in this group (for agent groups)
        - string

      tasks:                    # List of task names (for non-agent groups like barriers)
        - string
```

---

## Checkpoints Section

```yaml
checkpoints:
  latest_id: string             # ID of most recent checkpoint (null if none)

  entries:                      # List of checkpoints
    - id: string                # REQUIRED. Checkpoint ID (e.g., "CP-001")
      timestamp: ISO-8601       # REQUIRED. When checkpoint was created
      trigger: enum             # PHASE_COMPLETE | BARRIER_COMPLETE | MANUAL
      description: string       # Human-readable description
      recovery_point: string    # What step to resume from if recovering
```

---

## Metrics Section

```yaml
metrics:
  execution:                    # Execution progress metrics
    phases_complete: integer
    phases_total: integer
    phases_percent: integer     # Calculated: (complete/total) * 100
    barriers_complete: integer
    barriers_total: integer
    barriers_percent: integer
    agents_executed: integer
    agents_total: integer
    agents_percent: integer
    artifacts_created: integer
    artifacts_total: integer
    artifacts_percent: integer

  quality:                      # Quality metrics
    agent_success_rate: integer # Percentage of agents that completed successfully
    barrier_validation_pass_rate: integer
    checkpoint_recovery_tested: boolean

  timing:                       # Timing metrics
    workflow_started: ISO-8601
    last_activity: ISO-8601
    estimated_completion: ISO-8601  # null if unknown
```

---

## Blockers Section

```yaml
blockers:
  active:                       # Currently blocking issues
    - id: string                # Issue ID (e.g., "BLK-001")
      description: string       # What is blocking
      blocking:                 # What is blocked
        - string                # Agent/phase IDs
      severity: enum            # LOW | MEDIUM | HIGH
      created_at: ISO-8601

issues:
  resolved:                     # Previously resolved issues
    - id: string
      description: string
      resolution: string        # How it was resolved
      resolved_at: ISO-8601
```

---

## Next Actions Section

```yaml
next_actions:
  immediate:                    # Actions to take now
    - action: string            # Description of action
      agents: [string]          # Agent IDs involved (if applicable)
      execution_mode: enum      # PARALLEL | SEQUENTIAL

  subsequent:                   # Actions after immediate ones
    - action: string
      depends_on: string        # What must complete first
```

---

## Resumption Section

```yaml
resumption:
  last_checkpoint: string       # ID of last checkpoint (null if none)
  current_state: string         # Human-readable current state description
  next_step: string             # What to do next

  files_to_read:                # Files to read when resuming
    - string                    # Relative paths

  cross_session_portable: boolean  # Should always be true
  ephemeral_references: boolean    # Should always be false
```

---

## Status Enums

### Workflow Status

| Value | Description |
|-------|-------------|
| ACTIVE | Workflow is running |
| PAUSED | Workflow is paused by user |
| COMPLETE | Workflow finished successfully |
| FAILED | Workflow failed |
| CANCELLED | Workflow cancelled by user |

### Phase/Agent Status

| Value | Description |
|-------|-------------|
| PENDING | Not yet started |
| IN_PROGRESS | Currently executing |
| COMPLETE | Finished successfully |
| FAILED | Failed during execution |
| BLOCKED | Waiting for dependency |

### Checkpoint Trigger

| Value | Description |
|-------|-------------|
| PHASE_COMPLETE | Triggered when a phase completes |
| BARRIER_COMPLETE | Triggered when a barrier is crossed |
| MANUAL | Triggered by user request |

---

## Validation Rules

1. **workflow.constraints.max_agent_nesting** MUST be 1 (P-003)
2. **workflow.constraints.file_persistence** MUST be true (P-002)
3. **resumption.cross_session_portable** MUST be true
4. **resumption.ephemeral_references** MUST be false
5. All paths MUST be repository-relative (no absolute paths)
6. ISO-8601 timestamps MUST include timezone

---

*Schema Version: 1.0.0*
*Skill: orchestration*
