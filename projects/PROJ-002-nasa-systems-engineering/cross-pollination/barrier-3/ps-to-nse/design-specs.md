# Barrier 3: ps-* Design Artifacts for nse-* Pipeline

> **Barrier ID:** BARRIER-3-PS-TO-NSE
> **Source:** ps-* Pipeline Phase 3 (Design)
> **Target:** nse-* Pipeline Phase 4 (Review)
> **Date:** 2026-01-10
> **Status:** Complete

---

## Executive Summary

This document summarizes the design artifacts produced by the ps-* pipeline in Phase 3 for consumption by the nse-* pipeline in Phase 4 (Review). Three major design documents were produced:

| Document | ID | Focus | Key Contributions |
|----------|-----|-------|-------------------|
| Agent Design Specs | PS-D-001 | New agent specifications | 5 new agents, session context schema, delegation manifests |
| Schema Contracts | ps-d-002 | JSON Schema contracts | Session context v1.1.0, 16 agent output schemas, workflow state |
| Architecture Blueprints | ps-d-003 | Infrastructure patterns | Parallel execution, checkpointing, Generator-Critic loops |

---

## 1. Agent Design Specifications (PS-D-001)

### 1.1 New Agents Designed

| Agent ID | Pipeline | Role | Cognitive Mode | Gap Addressed |
|----------|----------|------|----------------|---------------|
| NSE-EXP-001 | nse-* | nse-explorer | Divergent | GAP-NEW-005, GAP-NEW-006 |
| NSE-ORC-001 | nse-* | nse-orchestrator | Mixed | GAP-AGT-004 |
| NSE-QA-001 | nse-* | nse-qa | Convergent | RGAP-009, GAP-SKL-001 |
| PS-ORC-001 | ps-* | ps-orchestrator | Mixed | GAP-AGT-004 |
| PS-CRT-001 | ps-* | ps-critic | Convergent | RGAP-009 |

### 1.2 Key Design Decisions

1. **UNIFIED_AGENT_TEMPLATE v1.0** - All agents use consistent template structure
2. **Hierarchical orchestration** - P-003 enforcement (max 1 level nesting)
3. **Explicit session_context schema** - Typed handoffs between agents
4. **Generator-Critic loops** - Circuit breaker at max 3 iterations

### 1.3 Risk Mitigations Incorporated

- **M-001:** Context isolation for parallel execution
- **M-002:** Circuit breaker (max 3 iterations) for Generator-Critic
- **M-003:** Schema validation at agent boundaries

---

## 2. JSON Schema Contracts (ps-d-002)

### 2.1 Schema Architecture

```
docs/schemas/
├── session_context.json          # Master envelope schema (v1.1.0)
├── common/
│   ├── types.json                # Shared type definitions
│   ├── findings.json             # Finding/question/blocker types
│   └── artifacts.json            # Artifact reference types
├── agents/
│   ├── ps/                       # 8 ps-* agent output schemas
│   └── nse/                      # 8 nse-* agent output schemas
└── workflows/
    └── cross_pollination.json    # Cross-family handoff extensions
```

### 2.2 Session Context v1.1.0 Extensions

- **`payload_schema_ref`** - URI reference to agent-specific output schema
- **`workflow_state`** - Cross-pollination tracking with:
  - `workflow_id`: Pattern `WF-[A-Z]{3}-\d{3}`
  - `phase`: enum [research, analysis, design, synthesis, validation]
  - `cross_family_handoff`: boolean
  - `sync_barrier`: { barrier_id, agents_expected, agents_completed }

### 2.3 Version Strategy

| Version | Breaking? | Description |
|---------|-----------|-------------|
| 1.0.0 | N/A | Initial release |
| 1.1.0 | No | Add payload_schema_ref for agent-specific validation |
| 1.2.0 | No | Add workflow_state for cross-pollination tracking |
| 2.0.0 | Yes | Reserved for major restructure |

---

## 3. Architecture Blueprints (ps-d-003)

### 3.1 Parallel Execution Architecture

```
                         PARALLEL EXECUTION ARCHITECTURE
    +-----------------------------------------------------------------+
    |  +-------------------+                                          |
    |  |   ORCHESTRATOR    |  (Opus 4.5 - Coordinator Role)           |
    |  +--------+----------+                                          |
    |           | spawn (respects P-003)                              |
    |  +--------+---------+                                           |
    |  |  PARALLEL ROUTER | (max 5 concurrent)                        |
    |  +--------+---------+                                           |
    |  +--------+--------+--------+--------+--------+                 |
    |  v        v        v        v        v        v                 |
    | [W1]     [W2]     [W3]     [W4]     [W5]    [Queue]             |
    |  +--------+--------+--------+--------+                          |
    |           v                                                     |
    |  +------------------+                                           |
    |  |  BARRIER SYNC    | (Timeout: 5min, Partial mode)             |
    |  +--------+---------+                                           |
    |           v                                                     |
    |  +------------------+                                           |
    |  |   AGGREGATOR     | (Merge, Conflict res, Quality check)      |
    |  +------------------+                                           |
    +-----------------------------------------------------------------+
```

### 3.2 Context Isolation Model

- **Shared (Read-Only):** Input artifacts, Configuration, Schema defs, Skill prompts
- **Isolated (Read-Write):** Per-worker directories with session_context.json, output/, scratch/
- **Enforcement:** No shared file handles, Namespace prefix `{workflow_id}/{agent_id}/`

### 3.3 State Checkpointing

```yaml
checkpoint:
  write_ahead_log: true        # M-004 atomicity
  recovery_point: "last_valid"
  storage: "filesystem"        # P-002 compliance
  retention: "3_checkpoints"
```

### 3.4 Generator-Critic Loop Pattern

```yaml
generator_critic:
  max_iterations: 3            # M-002 circuit breaker
  improvement_threshold: 0.10
  early_termination: true
  convergence_metric: "quality_score"
```

---

## 4. Implications for nse-* Phase 4 Review

### 4.1 Review Focus Areas

1. **Agent Specifications:** Verify NSE-EXP-001, NSE-ORC-001, NSE-QA-001 meet nse-* standards
2. **Schema Contracts:** Validate session_context v1.1.0 supports NPR 7123.1D traceability
3. **Architecture Blueprints:** Assess parallel execution alignment with nse-* quality gates

### 4.2 Cross-Reference to nse-* Formal Requirements

| ps-* Design Element | nse-* Requirement | Alignment Status |
|---------------------|-------------------|------------------|
| UNIFIED_AGENT_TEMPLATE | REQ-SAO-AGT-001 | Aligned |
| P-003 enforcement | REQ-SAO-L1-003 | Aligned |
| Session context schema | REQ-SAO-AGT-ORCH-001 | Aligned |
| 5 parallel agents max | REQ-SAO-L1-009 | Partially Aligned (spec says 10) |
| Circuit breaker (3 iter) | REQ-SAO-L1-011 | Aligned |

### 4.3 Open Items for Phase 4

1. Reconcile max concurrent agents: ps-* design says 5, nse-* formal says 10
2. Review NPR 7123.1D process mapping for new nse-* agents
3. Validate risk mitigations M-001 through M-004 coverage

---

## References

- PS-D-001-AGENT-SPECS: `ps-pipeline/phase-3-design/agent-design-specs.md`
- ps-d-002: `ps-pipeline/phase-3-design/schema-contracts.md`
- ps-d-003: `ps-pipeline/phase-3-design/arch-blueprints.md`

---

*Generated: 2026-01-10*
*Barrier: BARRIER-3-PS-TO-NSE*
