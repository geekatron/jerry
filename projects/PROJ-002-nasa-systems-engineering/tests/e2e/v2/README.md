# E2E Tests v2.0 - Dynamic Path Scheme

> **Version:** 2.0
> **Created:** 2026-01-10
> **Work Item:** WI-SAO-021 - Orchestration Folder Refactoring

---

## Overview

These tests validate the orchestration skill v2.0 with dynamic path resolution. Unlike the deprecated tests in `../deprecated/`, these tests use:

- **Dynamic workflow IDs** - Generated at runtime with format `{purpose}-{YYYYMMDD}-{NNN}`
- **Dynamic pipeline aliases** - Configurable per workflow
- **Dynamic artifact paths** - All paths use `orchestration/{workflow_id}/{pipeline_alias}/`

---

## Test Scenarios

| Test | Pattern | Description |
|------|---------|-------------|
| TEST-001-LINEAR-WORKFLOW | Sequential | A → B → C linear execution |
| TEST-002-PARALLEL-WORKFLOW | Fan-Out/Fan-In | 3 parallel workers → synthesis |
| TEST-003-CROSSPOLL-WORKFLOW | Cross-Pollinated | Alpha ↔ Beta with barrier sync |

---

## Path Scheme

### Base Path
```
orchestration/{workflow_id}/
```

### Pipeline Artifacts
```
orchestration/{workflow_id}/{pipeline_alias}/{phase_id}/artifact.md
```

### Cross-Pollination
```
orchestration/{workflow_id}/cross-pollination/{barrier_id}/{source}-to-{target}/handoff.md
```

---

## How to Run

### 1. Start Test Workflow

```
"Create an orchestration plan using the TEST-001 linear workflow"
```

### 2. Execute Agents

The orchestrator will invoke agents in order, creating artifacts at dynamic paths.

### 3. Validate Results

Check that:
1. Workflow ID was generated/used correctly
2. Artifact paths follow dynamic scheme
3. ORCHESTRATION.yaml reflects correct paths
4. Metrics are accurate

---

## Test Validation Assertions

Each test includes a `test_validation` section with assertions:

```yaml
test_validation:
  assertions:
    - name: "Workflow ID format"
      check: "workflow.id matches {purpose}-{YYYYMMDD}-{NNN}"
    - name: "Pipeline alias configured"
      check: "pipelines.*.short_alias is not empty"
```

---

## Comparison with Deprecated Tests

| Aspect | Deprecated (v1) | Current (v2) |
|--------|-----------------|--------------|
| Paths | Hardcoded (`tests/e2e/artifacts/`) | Dynamic (`orchestration/{workflow_id}/`) |
| Workflow ID | Static | Generated at runtime |
| Pipeline IDs | Fixed | Configurable aliases |
| Cross-pollination | Fixed paths | Dynamic `{source}-to-{target}` |

---

## Related Documents

- `skills/orchestration/SKILL.md` - Skill documentation (v2.0)
- `skills/orchestration/agents/orch-planner.md` - Planner agent (v2.0)
- `skills/orchestration/agents/orch-tracker.md` - Tracker agent (v2.0)
- `../deprecated/README.md` - Why old tests are deprecated

---

*Created by WI-SAO-021*
*Orchestration Skill v2.0*
