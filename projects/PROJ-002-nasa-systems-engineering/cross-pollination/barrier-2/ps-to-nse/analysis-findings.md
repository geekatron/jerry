# Barrier 2: ps-* Analysis Findings for nse-* Pipeline

> **Document ID:** BARRIER-2-PS-TO-NSE
> **Date:** 2026-01-09
> **Source Pipeline:** ps-* (Problem-Solving Analysis)
> **Target Pipeline:** nse-* (NASA SE Architecture)
> **Phase Transition:** Analysis → Design

---

## Executive Summary

The ps-* pipeline completed Phase 2 analysis with 2 agents performing gap analysis and trade studies. This document extracts key findings for the nse-* architecture phase to formalize into architectural decisions and specifications.

---

## 1. Gap Analysis Summary (From ps-a-001)

### Critical/High Gaps Requiring Architecture

| Gap ID | Description | Severity | Architecture Need |
|--------|-------------|----------|-------------------|
| GAP-AGT-003 | No formal session_context contract | Critical | Define JSON schema |
| GAP-006 | All nse-* agents convergent | Critical | Design nse-explorer |
| GAP-COORD | No pipeline orchestrators | Critical | Design orchestrators |
| GAP-SKL-001 | No acceptance test criteria | High | Define BDD framework |
| GAP-SKL-002 | No interface contracts | High | Define OpenAPI contracts |
| GAP-002 | No parallel execution | High | Design ParallelAgent |
| GAP-008 | No checkpointing | High | Design checkpoint system |

### Gap Closure Roadmap

| Phase | Gaps | Estimated Effort |
|-------|------|------------------|
| 1 - Quick Wins | GAP-001, GAP-005, GAP-010 | 5 hours |
| 2 - Foundation | GAP-AGT-003, GAP-AGT-004, GAP-SKL-002 | 14 hours |
| 3 - New Agents | GAP-006, GAP-COORD | 24 hours |
| 4 - Infrastructure | GAP-002, GAP-008 | 32 hours |

---

## 2. Trade Study Decisions (From ps-a-002)

### Decision Summary

| Trade Study | Recommendation | Score | Priority |
|-------------|----------------|-------|----------|
| TS-1: Templates | Superset Schema | 3.8/5 | P2 |
| TS-2: Orchestration | Hierarchical | 4.4/5 | P3 |
| TS-3: State Mgmt | Explicit Schema | 4.0/5 | P1 |
| TS-4: Parallel | Controlled (max 5) | 3.8/5 | P5 |
| TS-5: Gen-Critic | Paired Agents | 3.9/5 | P4 |

### Architecture Artifacts from Trade Studies

#### TS-1: Unified Agent Template Schema

```yaml
# UNIFIED_AGENT_TEMPLATE v1.0
identity:
  role: string           # REQUIRED
  expertise: array       # REQUIRED
  cognitive_mode: enum   # REQUIRED
  model: enum           # REQUIRED
persona:
  tone: string
  style: string
  formality: enum       # OPTIONAL
capabilities:
  allowed_tools: array
  forbidden_actions: array
state:
  output_key: string
  schema: object
nasa_se:                # OPTIONAL block
  process_refs: array
  methodology: string
  disclaimers: array
```

#### TS-3: session_context JSON Schema

```json
{
  "type": "object",
  "required": ["session_id", "source_agent", "target_agent", "payload"],
  "properties": {
    "session_id": { "type": "string", "format": "uuid" },
    "source_agent": { "type": "string" },
    "target_agent": { "type": "string" },
    "cognitive_mode": { "enum": ["divergent", "convergent", "mixed"] },
    "payload": {
      "type": "object",
      "properties": {
        "key_findings": { "type": "array" },
        "open_questions": { "type": "array" },
        "blockers": { "type": "array" },
        "confidence": { "type": "number", "minimum": 0, "maximum": 1 }
      }
    },
    "artifact_refs": { "type": "array" }
  }
}
```

#### TS-4: Parallel Execution Config

```yaml
parallel_config:
  max_concurrent_agents: 5
  fan_out_strategy: "topic_based"
  fan_in_timeout_ms: 300000
  isolation_mode: "full"
```

#### TS-5: Generator-Critic Protocol

```yaml
generator_critic:
  max_iterations: 3
  improvement_threshold: 0.10
  circuit_breaker:
    consecutive_failures: 2
    reset_timeout_ms: 60000
```

---

## 3. Constraints for nse-* Architecture

### Hard Constraints (Must Not Violate)

| Constraint | Source | Architecture Impact |
|------------|--------|---------------------|
| P-003: Single nesting | JERRY_CONSTITUTION | Orchestrator → Worker only |
| P-002: File persistence | JERRY_CONSTITUTION | All state to filesystem |
| P-022: No deception | JERRY_CONSTITUTION | Transparent critique logs |
| CON-003: NPR 7123.1D | NASA SE | 17 process alignment |
| CON-004: L0/L1/L2 | Output standard | All outputs tiered |

### Soft Constraints (Should Consider)

| Constraint | Source | Flexibility |
|------------|--------|-------------|
| Max 5 parallel agents | Trade study TS-4 | Adjustable based on resources |
| Max 3 critic iterations | Trade study TS-5 | Adjustable for quality needs |
| JSON for state | Trade study TS-3 | Could use msgpack if needed |

---

## 4. Architectural Requirements for nse-*

### From Gap Analysis

| REQ ID | Requirement | Priority | Rationale |
|--------|-------------|----------|-----------|
| ARCH-REQ-001 | Architecture SHALL define session_context schema | P1 | GAP-AGT-003 |
| ARCH-REQ-002 | Architecture SHALL include nse-explorer agent | P1 | GAP-006 |
| ARCH-REQ-003 | Architecture SHALL include nse-orchestrator agent | P1 | GAP-COORD |
| ARCH-REQ-004 | Architecture SHALL define skill interface contracts | P2 | GAP-SKL-002 |
| ARCH-REQ-005 | Architecture SHALL support parallel execution | P3 | GAP-002 |

### From Trade Studies

| REQ ID | Requirement | Priority | Source |
|--------|-------------|----------|--------|
| ARCH-REQ-006 | Architecture SHALL adopt superset template schema | P2 | TS-1 |
| ARCH-REQ-007 | Architecture SHALL implement hierarchical orchestration | P2 | TS-2 |
| ARCH-REQ-008 | Architecture SHALL support generator-critic loops | P3 | TS-5 |
| ARCH-REQ-009 | Architecture SHALL implement state checkpointing | P3 | TS-4 |

---

## 5. Recommended New Agent Specifications

### nse-explorer Agent

| Attribute | Specification |
|-----------|---------------|
| Role | Trade study exploration, concept investigation |
| Belbin | Plant + Resource Investigator |
| Cognitive Mode | Divergent |
| Process Refs | NPR 7123.1D Process 17 (Decision Analysis) |
| Output | `exploration/` directory |

### nse-orchestrator Agent

| Attribute | Specification |
|-----------|---------------|
| Role | Pipeline coordination, task delegation |
| Belbin | Coordinator |
| Cognitive Mode | Mixed |
| Process Refs | NPR 7123.1D Process 10 (Technical Planning) |
| Output | Delegation manifests |

### ps-critic Agent

| Attribute | Specification |
|-----------|---------------|
| Role | Quality evaluation, improvement feedback |
| Belbin | Monitor Evaluator |
| Cognitive Mode | Convergent |
| Pairing | With ps-architect, ps-researcher |
| Output | Critique reports |

---

## Cross-Pollination Validation

This artifact is ready for nse-* architecture consumption when:
- [x] Gap analysis summary extracted
- [x] Trade study decisions documented
- [x] Architectural requirements defined
- [x] Agent specifications proposed
- [ ] nse-architecture acknowledges inputs

---

## Source Artifacts

| Artifact | Path | Agent |
|----------|------|-------|
| Gap Analysis | `ps-pipeline/phase-2-analysis/gap-analysis.md` | ps-a-001 |
| Trade Study | `ps-pipeline/phase-2-analysis/trade-study.md` | ps-a-002 |

---

*Cross-pollination artifact generated at Sync Barrier 2*
*Date: 2026-01-09*
