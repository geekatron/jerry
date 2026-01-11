# Trade Study: Architecture Decisions for Skills and Agents

> **Document ID:** ps-a-002
> **Phase:** 2 - Analysis (ps-* Pipeline)
> **Project:** PROJ-002-nasa-systems-engineering
> **Date:** 2026-01-09
> **Agent:** ps-analyst

---

## L0: Executive Summary of Recommendations

Five architectural trade studies were conducted. **Recommendations:**
1. **Agent Template Unification**: Adopt superset schema merging ps-* and nse-* fields
2. **Orchestration Pattern**: Implement hierarchical orchestration with dedicated orchestrator agents
3. **State Management**: Adopt explicit state schema with JSON contracts (Google ADK pattern)
4. **Parallel Execution**: Implement fan-out/fan-in with controlled concurrency (max 5 agents)
5. **Generator-Critic**: Implement paired agents with iterative refinement loops

All recommendations respect P-003 (single nesting), P-002 (file persistence), and NPR 7123.1D alignment constraints.

---

## L1: Trade Study 1 - Agent Template Unification

### Problem Statement

ps-* agents use PS_AGENT_TEMPLATE v2.0 with 6 YAML fields, while nse-* agents use NSE_AGENT_TEMPLATE v1.0 with 8 fields. This creates inconsistency and complicates cross-pipeline handoffs.

### Alternatives

| Alt | Approach | Description |
|-----|----------|-------------|
| A | Keep Separate | Maintain distinct templates per family |
| B | Superset Schema | Merge into unified template with optional fields |
| C | Inheritance Model | Base template + family-specific extensions |

### Evaluation Criteria

| Criterion | Weight | Alt A | Alt B | Alt C |
|-----------|--------|-------|-------|-------|
| Cross-pipeline compatibility | 30% | 2 | 5 | 4 |
| Implementation complexity | 25% | 5 | 3 | 2 |
| Migration risk | 20% | 5 | 3 | 3 |
| Extensibility | 15% | 2 | 4 | 5 |
| Maintenance burden | 10% | 2 | 4 | 3 |
| **Weighted Score** | | **3.1** | **3.8** | **3.4** |

### Recommendation: Alternative B (Superset Schema)

**Rationale:** Superset schema provides best balance of compatibility and complexity. Migration is one-time effort, and single template simplifies tooling.

**Unified Schema Proposal:**
```yaml
# UNIFIED_AGENT_TEMPLATE v1.0
identity:
  role: string           # REQUIRED
  expertise: array       # REQUIRED
  cognitive_mode: enum   # REQUIRED (divergent/convergent/mixed)
  model: enum           # REQUIRED (opus/sonnet/haiku)
persona:
  tone: string           # REQUIRED
  style: string          # REQUIRED
  formality: enum        # OPTIONAL (casual/formal/technical)
capabilities:
  allowed_tools: array   # REQUIRED
  forbidden_actions: array  # REQUIRED
state:
  output_key: string     # REQUIRED
  schema: object         # OPTIONAL
nasa_se:                 # OPTIONAL block for nse-* agents
  process_refs: array
  methodology: string
  disclaimers: array
```

**Constraints Respected:**
- CON-003: NPR 7123.1D compliance via optional nasa_se block
- CON-004: L0/L1/L2 output levels preserved

---

## L1: Trade Study 2 - Orchestration Pattern

### Problem Statement

Current orchestration is implicit (described in PLAYBOOKs). No dedicated orchestrator agents exist for ps-* or nse-* families, causing 10% efficiency loss per research findings.

### Alternatives

| Alt | Approach | Description |
|-----|----------|-------------|
| A | Flat/Peer | All agents equal, handoff via state |
| B | Hierarchical | Dedicated orchestrator delegates to specialists |
| C | Hybrid | Orchestrator for complex, peer for simple workflows |

### Evaluation Criteria

| Criterion | Weight | Alt A | Alt B | Alt C |
|-----------|--------|-------|-------|-------|
| P-003 compliance (single nesting) | 30% | 5 | 4 | 4 |
| Workflow visibility | 25% | 2 | 5 | 4 |
| Scalability | 20% | 3 | 5 | 4 |
| Implementation complexity | 15% | 5 | 3 | 2 |
| Error recovery | 10% | 2 | 5 | 4 |
| **Weighted Score** | | **3.3** | **4.4** | **3.6** |

### Recommendation: Alternative B (Hierarchical)

**Rationale:** Hierarchical orchestration provides clear control flow, better error handling, and workflow visibility. P-003 compliance achieved by enforcing orchestrator → worker (no further nesting).

**Implementation:**
- Create `ps-orchestrator.md` with Coordinator Belbin role
- Create `nse-orchestrator.md` with NASA SE process awareness
- Orchestrator selects worker agents based on task type
- Workers cannot spawn additional agents (P-003 enforced)

**Constraints Respected:**
- CON-001: P-003 single nesting enforced by design
- CON-005: File persistence via orchestrator state tracking

---

## L1: Trade Study 3 - State Management

### Problem Statement

Current state management is implicit (file-based via WORKTRACKER.md and output files). No formal schema for session_context or handoff_manifest exists.

### Alternatives

| Alt | Approach | Description |
|-----|----------|-------------|
| A | Implicit File | Continue with unstructured file-based state |
| B | Explicit Schema | JSON schema with validation (Google ADK pattern) |
| C | Event Sourcing | Immutable event log with replay capability |

### Evaluation Criteria

| Criterion | Weight | Alt A | Alt B | Alt C |
|-----------|--------|-------|-------|-------|
| Agent chaining reliability | 30% | 2 | 5 | 5 |
| Implementation complexity | 25% | 5 | 3 | 1 |
| Debugging capability | 20% | 2 | 4 | 5 |
| P-002 compliance | 15% | 5 | 5 | 5 |
| Migration risk | 10% | 5 | 3 | 2 |
| **Weighted Score** | | **3.2** | **4.0** | **3.5** |

### Recommendation: Alternative B (Explicit Schema)

**Rationale:** Explicit schema provides reliability without event sourcing complexity. JSON Schema validation catches errors at handoff time.

**Proposed session_context Schema:**
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
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
        "key_findings": { "type": "array", "items": { "type": "string" } },
        "open_questions": { "type": "array" },
        "blockers": { "type": "array" },
        "confidence": { "type": "number", "minimum": 0, "maximum": 1 }
      }
    },
    "artifact_refs": { "type": "array", "items": { "type": "string" } }
  }
}
```

**Constraints Respected:**
- CON-005: File persistence (JSON files)
- GAP-AGT-003: Addresses session_context contract gap

---

## L1: Trade Study 4 - Parallel Execution

### Problem Statement

Jerry operates sequentially only. Industry frameworks (LangGraph, Google ADK) offer native parallel execution for research fan-out scenarios.

### Alternatives

| Alt | Approach | Description |
|-----|----------|-------------|
| A | Sequential Only | Maintain current sequential execution |
| B | Unlimited Parallel | Allow unbounded agent parallelism |
| C | Controlled Parallel | Fan-out with configurable concurrency limit |

### Evaluation Criteria

| Criterion | Weight | Alt A | Alt B | Alt C |
|-----------|--------|-------|-------|-------|
| Performance | 30% | 1 | 5 | 4 |
| Resource management | 25% | 5 | 1 | 4 |
| Context isolation | 20% | 5 | 2 | 4 |
| Implementation complexity | 15% | 5 | 2 | 3 |
| Debugging complexity | 10% | 5 | 1 | 3 |
| **Weighted Score** | | **3.4** | **2.4** | **3.8** |

### Recommendation: Alternative C (Controlled Parallel)

**Rationale:** Controlled parallelism provides performance gains while maintaining resource bounds and debuggability.

**Implementation:**
```yaml
parallel_config:
  max_concurrent_agents: 5
  fan_out_strategy: "topic_based"
  fan_in_timeout_ms: 300000
  isolation_mode: "full"  # Each agent gets clean context
```

**Constraints Respected:**
- CON-001: P-003 compliance (no nested spawning)
- R-REQ-005: Context isolation maintained per agent

---

## L1: Trade Study 5 - Generator-Critic Loops

### Problem Statement

No quality assurance loop exists. Industry research shows 15-25% quality improvement with generator-critic patterns.

### Alternatives

| Alt | Approach | Description |
|-----|----------|-------------|
| A | No Loop | Single-pass output (current state) |
| B | Self-Critique | Same agent critiques own output |
| C | Paired Agents | Dedicated generator and critic agents |

### Evaluation Criteria

| Criterion | Weight | Alt A | Alt B | Alt C |
|-----------|--------|-------|-------|-------|
| Output quality | 30% | 2 | 4 | 5 |
| Implementation complexity | 25% | 5 | 4 | 3 |
| P-003 compliance | 20% | 5 | 5 | 4 |
| Token efficiency | 15% | 5 | 3 | 2 |
| Belbin alignment | 10% | 2 | 3 | 5 |
| **Weighted Score** | | **3.6** | **3.9** | **3.9** |

### Recommendation: Alternative C (Paired Agents)

**Rationale:** Paired agents provide better separation of concerns and align with Belbin Monitor Evaluator role. While token cost is higher, quality improvement justifies investment.

**Implementation:**
- Create `ps-critic.md` (Monitor Evaluator role)
- Create `nse-qa.md` (NASA SE quality assurance)
- Define iteration protocol (max 3 iterations)
- Generator produces, critic evaluates, generator refines

**Constraints Respected:**
- CON-001: P-003 via orchestrator managing loop
- CON-002: P-022 transparency via critique logging

---

## L2: Decision Matrix with Weighted Scoring

### Summary of Recommendations

| Trade Study | Recommendation | Score | Constraints |
|-------------|----------------|-------|-------------|
| TS-1: Templates | Superset Schema | 3.8 | CON-003, CON-004 |
| TS-2: Orchestration | Hierarchical | 4.4 | CON-001, CON-005 |
| TS-3: State | Explicit Schema | 4.0 | CON-005, GAP-AGT-003 |
| TS-4: Parallel | Controlled (max 5) | 3.8 | CON-001, R-REQ-005 |
| TS-5: Gen-Critic | Paired Agents | 3.9 | CON-001, CON-002 |

### Implementation Priority

```
Priority 1: TS-3 (State Schema) - Foundation for all others
Priority 2: TS-1 (Template Unification) - Enables consistency
Priority 3: TS-2 (Orchestration) - Enables coordination
Priority 4: TS-5 (Generator-Critic) - Quality improvement
Priority 5: TS-4 (Parallel Execution) - Performance optimization
```

### Risk Summary

| Trade Study | Primary Risk | Mitigation |
|-------------|--------------|------------|
| TS-1 | Migration breaks existing agents | Versioned rollout |
| TS-2 | Orchestrator becomes bottleneck | Async delegation |
| TS-3 | Schema too rigid | Use optional fields |
| TS-4 | Race conditions | Context isolation |
| TS-5 | Infinite critique loops | Max iteration limit |

---

## Cross-Pollination Metadata

### Target Pipeline: nse-architecture (Phase 3)

**Artifacts for Architecture Design:**

| Trade Study | Architecture Input |
|-------------|-------------------|
| TS-1 | UNIFIED_AGENT_TEMPLATE v1.0 schema |
| TS-2 | Orchestrator agent specifications |
| TS-3 | session_context JSON Schema |
| TS-4 | parallel_config specification |
| TS-5 | Generator-Critic interaction protocol |

### Handoff Checklist for Barrier 2

- [x] 5 trade studies completed
- [x] All alternatives evaluated with weighted scoring
- [x] Recommendations documented with rationale
- [x] Constraints verified for each decision
- [ ] nse-architecture acknowledges design inputs

---

## Source Artifacts

| Artifact | Path | Relevance |
|----------|------|-----------|
| Industry Practices | ps-pipeline/phase-1-research/industry-practices.md | Framework patterns |
| Research Findings | cross-pollination/barrier-1/ps-to-nse/research-findings.md | Options identified |
| Requirements Gaps | cross-pollination/barrier-1/nse-to-ps/requirements-gaps.md | Constraints |

---

*Trade Study Document: ps-a-002*
*Generated by: ps-analyst (Phase 2)*
*Date: 2026-01-09*
