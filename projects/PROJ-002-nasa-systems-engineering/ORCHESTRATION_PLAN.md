# ORCHESTRATION_PLAN.md

> **Document ID:** PROJ-002-ORCH-PLAN
> **Project:** PROJ-002-nasa-systems-engineering
> **Status:** ACTIVE - PHASE 3 PENDING
> **Version:** 1.0
> **Created:** 2026-01-10
> **Last Updated:** 2026-01-10

---

## 1. Executive Summary

This document captures the **strategic context** for orchestrating multi-agent workflows within PROJ-002. It defines the cross-pollinated pipeline architecture, phase dependencies, sync barriers, and agent coordination patterns.

**Current State:** Phases 1-2 complete for both pipelines. Phases 3-4 are pending execution.

**Orchestration Pattern:** Cross-Pollinated Bidirectional Pipeline (Sequential + Barrier Sync)

---

## 2. Workflow Architecture

### 2.1 Cross-Pollinated Pipeline Diagram

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                    CROSS-POLLINATED PIPELINE ARCHITECTURE                        │
│                        (ps-* ↔ nse-* Bidirectional)                              │
└─────────────────────────────────────────────────────────────────────────────────┘

    ps-* PIPELINE                                           nse-* PIPELINE
    (Problem-Solving)                                       (NASA SE Formalization)
    ═══════════════                                         ═══════════════════════

┌─────────────────────┐                                 ┌─────────────────────┐
│ PHASE 1: RESEARCH   │                                 │ PHASE 1: SCOPE      │
│ ─────────────────── │                                 │ ─────────────────── │
│ • ps-r-001: Skills  │                                 │ • nse-r-001: Skills │
│ • ps-r-002: Agent   │                                 │   Requirements      │
│   Design            │                                 │ • nse-r-002: Agent  │
│ • ps-r-003: Industry│                                 │   Requirements      │
│   Practices         │                                 │                     │
│ STATUS: ✅ COMPLETE │                                 │ STATUS: ✅ COMPLETE │
└──────────┬──────────┘                                 └──────────┬──────────┘
           │                                                       │
           ▼                                                       ▼
    ╔═══════════════════════════════════════════════════════════════════════╗
    ║                        SYNC BARRIER 1                                  ║
    ║  ┌─────────────────────────────────────────────────────────────────┐  ║
    ║  │ ps→nse: research-findings.md (8 options, 8 practices, 10 gaps) │  ║
    ║  │ nse→ps: requirements-gaps.md (85 requirements, 10 research gaps)│  ║
    ║  └─────────────────────────────────────────────────────────────────┘  ║
    ║  STATUS: ✅ COMPLETE                                                   ║
    ╚═══════════════════════════════════════════════════════════════════════╝
           │                                                       │
           ▼                                                       ▼
┌─────────────────────┐                                 ┌─────────────────────┐
│ PHASE 2: ANALYSIS   │                                 │ PHASE 2: RISK       │
│ ─────────────────── │                                 │ ─────────────────── │
│ • ps-a-001: Gap     │                                 │ • nse-k-001: Impl   │
│   Analysis          │                                 │   Risks (14)        │
│ • ps-a-002: Trade   │                                 │ • nse-k-002: Tech   │
│   Study             │                                 │   Risks (16)        │
│ STATUS: ✅ COMPLETE │                                 │ STATUS: ✅ COMPLETE │
└──────────┬──────────┘                                 └──────────┬──────────┘
           │                                                       │
           ▼                                                       ▼
    ╔═══════════════════════════════════════════════════════════════════════╗
    ║                        SYNC BARRIER 2                                  ║
    ║  ┌─────────────────────────────────────────────────────────────────┐  ║
    ║  │ ps→nse: analysis-findings.md (gap roadmap, trade decisions)     │  ║
    ║  │ nse→ps: risk-findings.md (risk register, go/no-go matrix)       │  ║
    ║  └─────────────────────────────────────────────────────────────────┘  ║
    ║  STATUS: ✅ COMPLETE                                                   ║
    ╚═══════════════════════════════════════════════════════════════════════╝
           │                                                       │
           ▼                                                       ▼
┌─────────────────────┐                                 ┌─────────────────────┐
│ PHASE 3: DESIGN     │                                 │ PHASE 3: FORMAL     │
│ ─────────────────── │                                 │ ─────────────────── │
│ • ps-d-001: Agent   │                                 │ • nse-f-001: Formal │
│   Design Specs      │                                 │   Requirements      │
│ • ps-d-002: Schema  │                                 │ • nse-f-002: Formal │
│   Contracts         │                                 │   Risk Mitigations  │
│ • ps-d-003: Arch    │                                 │ • nse-f-003: Verif  │
│   Blueprints        │                                 │   Matrices          │
│ STATUS: ⏳ PENDING  │                                 │ STATUS: ⏳ PENDING  │
└──────────┬──────────┘                                 └──────────┬──────────┘
           │                                                       │
           ▼                                                       ▼
    ╔═══════════════════════════════════════════════════════════════════════╗
    ║                        SYNC BARRIER 3                                  ║
    ║  ┌─────────────────────────────────────────────────────────────────┐  ║
    ║  │ ps→nse: design-specs.md (agent designs, schemas, blueprints)    │  ║
    ║  │ nse→ps: formal-artifacts.md (NASA-format reqs, mitigations)     │  ║
    ║  └─────────────────────────────────────────────────────────────────┘  ║
    ║  STATUS: ⏳ PENDING                                                    ║
    ╚═══════════════════════════════════════════════════════════════════════╝
           │                                                       │
           ▼                                                       ▼
┌─────────────────────┐                                 ┌─────────────────────┐
│ PHASE 4: SYNTHESIS  │                                 │ PHASE 4: REVIEW     │
│ ─────────────────── │                                 │ ─────────────────── │
│ • ps-s-001: Final   │                                 │ • nse-v-001: Tech   │
│   Synthesis         │                                 │   Review Findings   │
│ • ps-s-002: Impl    │                                 │ • nse-v-002: Go/No  │
│   Roadmap           │                                 │   Go Decision       │
│                     │                                 │ • nse-v-003: QA     │
│                     │                                 │   Sign-off          │
│ STATUS: ⏳ PENDING  │                                 │ STATUS: ⏳ PENDING  │
└──────────┬──────────┘                                 └──────────┬──────────┘
           │                                                       │
           ▼                                                       ▼
    ╔═══════════════════════════════════════════════════════════════════════╗
    ║                        SYNC BARRIER 4                                  ║
    ║  ┌─────────────────────────────────────────────────────────────────┐  ║
    ║  │ ps→nse: synthesis-complete.md (final recommendations)           │  ║
    ║  │ nse→ps: review-complete.md (approval, sign-off)                 │  ║
    ║  └─────────────────────────────────────────────────────────────────┘  ║
    ║  STATUS: ⏳ PENDING                                                    ║
    ╚═══════════════════════════════════════════════════════════════════════╝
           │                                                       │
           └───────────────────────┬───────────────────────────────┘
                                   ▼
                    ┌─────────────────────────────┐
                    │     FINAL INTEGRATION       │
                    │ ─────────────────────────── │
                    │ synthesis/final-synthesis.md│
                    │ STATUS: ⏳ PENDING          │
                    └─────────────────────────────┘
```

### 2.2 Orchestration Pattern Classification

Per [Microsoft AI Agent Orchestration Patterns](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns):

| Pattern | Applied | Description |
|---------|---------|-------------|
| **Sequential** | ✅ Yes | Phases execute in order within each pipeline |
| **Concurrent** | ✅ Yes | ps-* and nse-* pipelines run in parallel |
| **Barrier Sync** | ✅ Yes | Cross-pollination at sync barriers |
| **Hierarchical** | ✅ Yes | Orchestrator delegates to phase agents |
| **State Machine** | ✅ Yes | Explicit phase states and transitions |

---

## 3. Phase Definitions

### 3.1 ps-* Pipeline Phases

| Phase | Name | Purpose | Agents | Artifacts |
|-------|------|---------|--------|-----------|
| 1 | Research | Gather domain knowledge | ps-r-001, ps-r-002, ps-r-003 | skills-optimization.md, agent-design.md, industry-practices.md |
| 2 | Analysis | Analyze gaps and trade-offs | ps-a-001, ps-a-002 | gap-analysis.md, trade-study.md |
| 3 | Design | Create formal designs | ps-d-001, ps-d-002, ps-d-003 | agent-design-specs.md, schema-contracts.md, arch-blueprints.md |
| 4 | Synthesis | Final recommendations | ps-s-001, ps-s-002 | final-synthesis.md, impl-roadmap.md |

### 3.2 nse-* Pipeline Phases

| Phase | Name | Purpose | Agents | Artifacts |
|-------|------|---------|--------|-----------|
| 1 | Scope | Define requirements | nse-r-001, nse-r-002 | skills-requirements.md, agent-requirements.md |
| 2 | Risk | Assess risks | nse-k-001, nse-k-002 | implementation-risks.md, technical-risks.md |
| 3 | Formal | NASA-format specs | nse-f-001, nse-f-002, nse-f-003 | formal-requirements.md, formal-mitigations.md, verification-matrices.md |
| 4 | Review | Technical review | nse-v-001, nse-v-002, nse-v-003 | tech-review-findings.md, go-nogo-decision.md, qa-signoff.md |

---

## 4. Sync Barrier Protocol

Per [LangGraph State Management](https://langchain-ai.github.io/langgraph/) and NASA NPR 7123.1D Technical Review Gates:

### 4.1 Barrier Transition Rules

```
BARRIER TRANSITION PROTOCOL
===========================

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

### 4.2 Barrier Artifact Schema

```yaml
# Cross-pollination artifact schema
barrier_artifact:
  document_id: string          # BARRIER-{n}-{direction}
  date: ISO-8601               # Creation timestamp
  source_pipeline: string      # ps-* or nse-*
  target_pipeline: string      # nse-* or ps-*
  phase_transition: string     # e.g., "Research → Scope"
  key_findings:
    - id: string
      description: string
      priority: HIGH|MEDIUM|LOW
      source_artifact: string
  open_questions: array
  blockers: array
  confidence: float            # 0.0 - 1.0
  validation_checklist:
    - item: string
      status: PASS|FAIL|PENDING
```

---

## 5. Agent Registry

### 5.1 Phase 3 Agents (To Be Executed)

| Agent ID | Pipeline | Role | Cognitive Mode | Input Artifacts | Output Artifacts |
|----------|----------|------|----------------|-----------------|------------------|
| ps-d-001 | ps-* | Agent Design Specialist | Convergent | gap-analysis.md, trade-study.md | agent-design-specs.md |
| ps-d-002 | ps-* | Schema Contract Designer | Convergent | trade-study.md, risk-findings.md | schema-contracts.md |
| ps-d-003 | ps-* | Architecture Blueprint | Convergent | All Phase 2 artifacts | arch-blueprints.md |
| nse-f-001 | nse-* | Formal Requirements Engineer | Convergent | requirements-gaps.md, analysis-findings.md | formal-requirements.md |
| nse-f-002 | nse-* | Risk Mitigation Specialist | Convergent | implementation-risks.md, technical-risks.md | formal-mitigations.md |
| nse-f-003 | nse-* | Verification Matrix Engineer | Convergent | All Phase 2 artifacts | verification-matrices.md |

### 5.2 Phase 4 Agents (To Be Executed)

| Agent ID | Pipeline | Role | Cognitive Mode | Input Artifacts | Output Artifacts |
|----------|----------|------|----------------|-----------------|------------------|
| ps-s-001 | ps-* | Synthesis Specialist | Mixed | All ps-* artifacts + nse-* cross-pollination | final-synthesis.md |
| ps-s-002 | ps-* | Implementation Planner | Convergent | final-synthesis.md | impl-roadmap.md |
| nse-v-001 | nse-* | Technical Reviewer | Convergent | All nse-* artifacts | tech-review-findings.md |
| nse-v-002 | nse-* | Decision Gate Officer | Convergent | tech-review-findings.md, risk-findings.md | go-nogo-decision.md |
| nse-v-003 | nse-* | QA Sign-off Authority | Convergent | All artifacts | qa-signoff.md |

---

## 6. State Management

Per [CrewAI Flow State Management](https://docs.crewai.com/concepts/flows) and [LangGraph Checkpointing](https://langchain-ai.github.io/langgraph/):

### 6.1 Orchestration State Schema

```yaml
orchestration_state:
  workflow_id: string                    # Unique workflow identifier
  project_id: string                     # PROJ-002
  created_at: ISO-8601
  updated_at: ISO-8601

  pipelines:
    ps:
      current_phase: 1|2|3|4
      phase_status: PENDING|IN_PROGRESS|COMPLETE|BLOCKED
      agents_completed: array
      artifacts_produced: array
      blockers: array
    nse:
      current_phase: 1|2|3|4
      phase_status: PENDING|IN_PROGRESS|COMPLETE|BLOCKED
      agents_completed: array
      artifacts_produced: array
      blockers: array

  barriers:
    barrier_1: PENDING|IN_PROGRESS|COMPLETE
    barrier_2: PENDING|IN_PROGRESS|COMPLETE
    barrier_3: PENDING|IN_PROGRESS|COMPLETE
    barrier_4: PENDING|IN_PROGRESS|COMPLETE

  checkpoints:
    - checkpoint_id: string
      timestamp: ISO-8601
      state_snapshot: object
      trigger: PHASE_COMPLETE|BARRIER_COMPLETE|MANUAL
```

### 6.2 Checkpoint Strategy

| Checkpoint Trigger | Location | Purpose |
|--------------------|----------|---------|
| Phase Complete | After each phase | Enable phase-level rollback |
| Barrier Complete | After each sync | Enable cross-pollination recovery |
| Agent Complete | After each agent | Enable fine-grained recovery |
| Manual | User-triggered | Debug and inspection |

---

## 7. Execution Constraints

### 7.1 Hard Constraints (From Jerry Constitution)

| Constraint | ID | Enforcement |
|------------|----|----|
| Single agent nesting | P-003 | Orchestrator → Worker only |
| File persistence | P-002 | All state to filesystem |
| No deception | P-022 | Transparent reasoning |
| User authority | P-020 | User approves all gates |

### 7.2 Soft Constraints (From Research)

| Constraint | Source | Value |
|------------|--------|-------|
| Max concurrent agents | Microsoft Patterns | 3-5 agents |
| Max barrier retries | LangGraph | 3 attempts |
| Context window limit | Anthropic | Summarize at barriers |
| Checkpoint frequency | CrewAI Best Practice | Every phase transition |

---

## 8. Success Criteria

### 8.1 Phase 3 Exit Criteria

| Criterion | Pipeline | Validation |
|-----------|----------|------------|
| All design specs created | ps-* | Files exist in phase-3-design/ |
| Schema contracts defined | ps-* | JSON Schema valid |
| Architecture blueprints complete | ps-* | All components addressed |
| Formal requirements NASA-format | nse-* | NPR 7123.1D compliant |
| Risk mitigations documented | nse-* | All RED risks addressed |
| Verification matrices complete | nse-* | Bidirectional traceability |
| Barrier 3 cross-pollination done | Both | Artifacts exchanged |

### 8.2 Phase 4 Exit Criteria

| Criterion | Pipeline | Validation |
|-----------|----------|------------|
| Final synthesis complete | ps-* | Recommendations actionable |
| Implementation roadmap defined | ps-* | Phases, effort, dependencies |
| Technical review passed | nse-* | No blocking findings |
| Go/No-Go decision made | nse-* | GREEN status |
| QA sign-off obtained | nse-* | User approval |
| Barrier 4 complete | Both | Artifacts exchanged |
| Final integration done | Both | synthesis/final-synthesis.md |

---

## 9. Risk Mitigations

### 9.1 Orchestration Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Task tool connection errors | Medium | High | Direct artifact creation fallback |
| Context window exhaustion | Medium | Medium | Summarize at barriers |
| Infinite agent loops | Low | High | Max iterations = 3 |
| Cross-pollination data loss | Low | High | Checkpoint before barriers |
| Pipeline desynchronization | Medium | Medium | Barrier validation checks |

### 9.2 Circuit Breaker Configuration

```yaml
circuit_breaker:
  max_agent_retries: 3
  max_barrier_retries: 2
  timeout_per_agent_ms: 300000      # 5 minutes
  timeout_per_phase_ms: 1800000     # 30 minutes
  fallback_strategy: DIRECT_CREATION # Create artifacts directly
```

---

## 10. References

### 10.1 Industry Sources

| Source | URL | Key Insight |
|--------|-----|-------------|
| Microsoft AI Agent Patterns | [learn.microsoft.com](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns) | Orchestration pattern taxonomy |
| LangGraph Documentation | [langchain-ai.github.io](https://langchain-ai.github.io/langgraph/) | State checkpointing |
| CrewAI Flows | [docs.crewai.com](https://docs.crewai.com/concepts/flows) | Flow state management |
| NASA NPR 7123.1D | [nodis3.gsfc.nasa.gov](https://nodis3.gsfc.nasa.gov/displayDir.cfm?Internal_ID=N_PR_7123_001D_) | SE Engine, Technical Reviews |

### 10.2 Project Artifacts

| Artifact | Path | Purpose |
|----------|------|---------|
| Project Plan | PLAN.md | Project-level strategy |
| Work Tracker | WORKTRACKER.md | Project-level tasks |
| Orchestration Tracker | ORCHESTRATION_WORKTRACKER.md | Pipeline execution state |
| Final Synthesis | synthesis/skills-agents-optimization-synthesis.md | Current synthesis (to be updated) |

---

## 11. Resumption Context

### 11.1 Current Execution State

```
PIPELINE STATUS AS OF 2026-01-10
================================

ps-* Pipeline:
  Phase 1 (Research):   ✅ COMPLETE (3 agents, 3 artifacts)
  Phase 2 (Analysis):   ✅ COMPLETE (2 agents, 2 artifacts)
  Phase 3 (Design):     ⏳ PENDING (0 agents, 0 artifacts)
  Phase 4 (Synthesis):  ⏳ PENDING (0 agents, 0 artifacts)

nse-* Pipeline:
  Phase 1 (Scope):      ✅ COMPLETE (2 agents, 2 artifacts)
  Phase 2 (Risk):       ✅ COMPLETE (2 agents, 2 artifacts)
  Phase 3 (Formal):     ⏳ PENDING (0 agents, 0 artifacts)
  Phase 4 (Review):     ⏳ PENDING (0 agents, 0 artifacts)

Sync Barriers:
  Barrier 1: ✅ COMPLETE
  Barrier 2: ✅ COMPLETE
  Barrier 3: ⏳ PENDING
  Barrier 4: ⏳ PENDING
```

### 11.2 Next Actions

1. Execute ps-* Phase 3 agents (ps-d-001, ps-d-002, ps-d-003)
2. Execute nse-* Phase 3 agents (nse-f-001, nse-f-002, nse-f-003)
3. Complete Sync Barrier 3 cross-pollination
4. Execute ps-* Phase 4 agents (ps-s-001, ps-s-002)
5. Execute nse-* Phase 4 agents (nse-v-001, nse-v-002, nse-v-003)
6. Complete Sync Barrier 4 cross-pollination
7. Create final integration synthesis

---

*Document ID: PROJ-002-ORCH-PLAN*
*Version: 1.0*
*Status: ACTIVE*
*Cross-Session Portable: All paths are repository-relative*
