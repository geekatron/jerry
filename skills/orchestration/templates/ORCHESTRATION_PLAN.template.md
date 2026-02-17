# ORCHESTRATION_PLAN.md

> **Document ID:** {PROJECT_ID}-ORCH-PLAN
> **Project:** {PROJECT_ID}
> **Workflow ID:** `{WORKFLOW_ID}`
> **Status:** {ACTIVE|PAUSED|COMPLETE}
> **Version:** 2.0
> **Created:** {CREATED_DATE}
> **Last Updated:** {UPDATED_DATE}

---

## 1. Executive Summary

{Brief description of the workflow being orchestrated. What problem does it solve?
What is the expected outcome?}

**Current State:** {Current execution state summary}

**Orchestration Pattern:** {Pattern name from SKILL.md}

### 1.1 Workflow Identification

| Field | Value | Source |
|-------|-------|--------|
| Workflow ID | `{WORKFLOW_ID}` | {user \| auto} |
| ID Format | `{purpose}-{YYYYMMDD}-{NNN}` | semantic-date-seq |
| Base Path | `orchestration/{WORKFLOW_ID}/` | Dynamic |

**Artifact Output Locations:**
- Pipeline A: `orchestration/{WORKFLOW_ID}/{PIPELINE_A_ALIAS}/`
- Pipeline B: `orchestration/{WORKFLOW_ID}/{PIPELINE_B_ALIAS}/`
- Cross-pollination: `orchestration/{WORKFLOW_ID}/cross-pollination/`

---

## 2. Workflow Architecture

### 2.1 Pipeline Diagram

```
{ASCII diagram showing pipelines, phases, agents, and barriers}

Example for cross-pollinated pipeline:

    PIPELINE A                              PIPELINE B
    ==========                              ==========

┌─────────────────────┐                 ┌─────────────────────┐
│ PHASE 1: {NAME}     │                 │ PHASE 1: {NAME}     │
│ ─────────────────── │                 │ ─────────────────── │
│ • agent-a-001       │                 │ • agent-b-001       │
│ • agent-a-002       │                 │ • agent-b-002       │
│ STATUS: {STATUS}    │                 │ STATUS: {STATUS}    │
└──────────┬──────────┘                 └──────────┬──────────┘
           │                                       │
           ▼                                       ▼
    ╔═══════════════════════════════════════════════════════════╗
    ║                     SYNC BARRIER 1                         ║
    ║  ┌─────────────────────────────────────────────────────┐  ║
    ║  │ a→b: {artifact-name}.md                             │  ║
    ║  │ b→a: {artifact-name}.md                             │  ║
    ║  └─────────────────────────────────────────────────────┘  ║
    ║  STATUS: {STATUS}                                          ║
    ╚═══════════════════════════════════════════════════════════╝
           │                                       │
           ▼                                       ▼
┌─────────────────────┐                 ┌─────────────────────┐
│ PHASE 2: {NAME}     │                 │ PHASE 2: {NAME}     │
│ STATUS: {STATUS}    │                 │ STATUS: {STATUS}    │
└─────────────────────┘                 └─────────────────────┘
```

### 2.2 Orchestration Pattern Classification

| Pattern | Applied | Description |
|---------|---------|-------------|
| Sequential | {Yes/No} | Phases execute in order |
| Concurrent | {Yes/No} | Pipelines run in parallel |
| Barrier Sync | {Yes/No} | Cross-pollination at barriers |
| Hierarchical | {Yes/No} | Orchestrator delegates to agents |

---

## 3. Phase Definitions

### 3.1 Pipeline A Phases

| Phase | Name | Purpose | Agents | Status |
|-------|------|---------|--------|--------|
| 1 | {Name} | {Purpose} | {agent-ids} | {STATUS} |
| 2 | {Name} | {Purpose} | {agent-ids} | {STATUS} |

### 3.2 Pipeline B Phases

| Phase | Name | Purpose | Agents | Status |
|-------|------|---------|--------|--------|
| 1 | {Name} | {Purpose} | {agent-ids} | {STATUS} |
| 2 | {Name} | {Purpose} | {agent-ids} | {STATUS} |

---

## 4. Sync Barrier Protocol

### 4.1 Barrier Transition Rules

```
1. PRE-BARRIER CHECK
   □ All phase agents have completed execution
   □ All phase artifacts exist and are valid
   □ No blocking errors or unresolved issues

2. CROSS-POLLINATION EXECUTION
   □ Extract key findings from source pipeline
   □ Transform into cross-pollination artifact
   □ Validate artifact schema and content

3. POST-BARRIER VERIFICATION
   □ Target pipeline acknowledges receipt
   □ Inputs incorporated into next phase context
   □ Barrier status updated to COMPLETE
```

### 4.2 Barrier Definitions

| Barrier | After Phase | Artifacts | Status |
|---------|-------------|-----------|--------|
| barrier-1 | Phase 1 | {a→b}, {b→a} | {STATUS} |
| barrier-2 | Phase 2 | {a→b}, {b→a} | {STATUS} |

---

## 5. Agent Registry

### 5.1 Phase {N} Agents

| Agent ID | Pipeline | Role | Input Artifacts | Output Artifacts | Status |
|----------|----------|------|-----------------|------------------|--------|
| {id} | {pipeline} | {role} | {inputs} | {output} | {STATUS} |

---

## 6. State Management

### 6.1 State Files

| File | Purpose |
|------|---------|
| `ORCHESTRATION.yaml` | Machine-readable state (SSOT) |
| `ORCHESTRATION_WORKTRACKER.md` | Tactical execution documentation |
| `ORCHESTRATION_PLAN.md` | This file - strategic context |

### 6.2 Artifact Path Structure (WI-SAO-021)

All artifacts are stored under the workflow's base path using dynamic identifiers:

```
orchestration/{WORKFLOW_ID}/
├── {PIPELINE_A_ALIAS}/
│   ├── phase-1-{name}/
│   │   └── {artifact}.md
│   └── phase-2-{name}/
│       └── {artifact}.md
├── {PIPELINE_B_ALIAS}/
│   ├── phase-1-{name}/
│   │   └── {artifact}.md
│   └── phase-2-{name}/
│       └── {artifact}.md
└── cross-pollination/
    ├── barrier-1/
    │   ├── {PIPELINE_A_ALIAS}-to-{PIPELINE_B_ALIAS}/
    │   │   └── handoff.md
    │   └── {PIPELINE_B_ALIAS}-to-{PIPELINE_A_ALIAS}/
    │       └── handoff.md
    └── barrier-2/
        └── ...
```

**Pipeline Alias Resolution:**
1. Workflow YAML override (highest priority)
2. Skill registration default
3. Auto-derived from skill name (fallback)

### 6.3 Checkpoint Strategy

| Trigger | When | Purpose |
|---------|------|---------|
| PHASE_COMPLETE | After each phase | Phase-level rollback |
| BARRIER_COMPLETE | After each sync | Cross-pollination recovery |
| MANUAL | User-triggered | Debug and inspection |

---

## 7. Execution Constraints

### 7.1 Hard Constraints (Jerry Constitution)

| Constraint | ID | Enforcement |
|------------|----|----|
| Single agent nesting | P-003 | Orchestrator → Worker only |
| File persistence | P-002 | All state to filesystem |
| No deception | P-022 | Transparent reasoning |
| User authority | P-020 | User approves gates |

### 7.1.1 Worktracker Entity Templates

> **WTI-007:** Entity files (EPIC, FEATURE, ENABLER, TASK, etc.) created during orchestration MUST use canonical templates from `.context/templates/worktracker/`. Read the appropriate template first, then populate. Do not create entity files from memory or by copying other instance files.

### 7.2 Soft Constraints

| Constraint | Value | Rationale |
|------------|-------|-----------|
| Max concurrent agents | {N} | Resource management |
| Max barrier retries | {N} | Circuit breaker |
| Checkpoint frequency | {PHASE|BARRIER|AGENT} | Recovery granularity |

---

## 8. Success Criteria

### 8.1 Phase {N} Exit Criteria

| Criterion | Validation |
|-----------|------------|
| {Criterion 1} | {How to validate} |
| {Criterion 2} | {How to validate} |

### 8.2 Workflow Completion Criteria

| Criterion | Validation |
|-----------|------------|
| All phases complete | All phase status = COMPLETE |
| All barriers synced | All barrier status = COMPLETE |
| Final synthesis created | synthesis/{workflow-id}-final.md exists |

---

## 9. Risk Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| {Risk 1} | {L/M/H} | {L/M/H} | {Mitigation} |

---

## 10. Resumption Context

### 10.1 Current Execution State

```
WORKFLOW STATUS AS OF {DATE}
============================

Pipeline A:
  Phase 1: {STATUS}
  Phase 2: {STATUS}

Pipeline B:
  Phase 1: {STATUS}
  Phase 2: {STATUS}

Barriers:
  Barrier 1: {STATUS}
  Barrier 2: {STATUS}
```

### 10.2 Next Actions

1. {Next action 1}
2. {Next action 2}
3. {Next action 3}

---

*Document ID: {PROJECT_ID}-ORCH-PLAN*
*Workflow ID: {WORKFLOW_ID}*
*Version: 2.0*
*Cross-Session Portable: All paths are repository-relative*
