# Cross-Pollination Architecture: ps-* and nse-* Agent Integration

> **Document ID:** proj-002-e-010
> **Date:** 2026-01-09
> **Author:** Claude Opus 4.5 (Orchestrator)
> **Status:** ARCHITECTURE DESIGN
> **Classification:** Analysis Document

---

## Executive Summary

This document defines the architecture for orchestrating two parallel agent pipelines (ps-* and nse-*) with synchronized cross-pollination points. The design addresses the fundamental challenge of combining **divergent exploration** (ps-*) with **convergent formalization** (nse-*) while respecting Claude Code's architectural constraints.

### Key Design Decisions

1. **Parallel Pipelines**: ps-* and nse-* run concurrently in phases
2. **Sync Barriers**: Explicit synchronization points for artifact exchange
3. **File-Based Handoff**: Artifacts stored in `cross-pollination/` directory
4. **Orchestrator-Managed**: Lead agent (Opus 4.5) coordinates all handoffs
5. **P-003 Compliant**: No recursive subagent spawning

---

## 1. Agent Family Analysis

### 1.1 ps-* (Problem-Solving) Family

| Agent | Cognitive Mode | Primary Output | Best For |
|-------|---------------|----------------|----------|
| `ps-researcher` | Divergent | Research findings, options | Information gathering, exploration |
| `ps-analyst` | Mixed | Gap analysis, trade studies | Evaluation, comparison |
| `ps-architect` | Convergent | ADRs, design decisions | Architectural choices |
| `ps-synthesizer` | Convergent | Unified recommendations | Integration, summary |

**Characteristic**: Exploratory, options-focused, flexible output formats

### 1.2 nse-* (NASA SE) Family

| Agent | Cognitive Mode | Primary Output | Best For |
|-------|---------------|----------------|----------|
| `nse-requirements` | Convergent | Formal "shall" statements, VCRM | Requirements formalization |
| `nse-risk` | Mixed | Risk registers, 5x5 matrices | Risk identification/tracking |
| `nse-architecture` | Convergent | TSR, ICD, technical specs | Formal architecture docs |
| `nse-reviewer` | Convergent | Review reports, gate assessments | Quality gates |
| `nse-verification` | Convergent | Verification matrices, test plans | V&V activities |
| `nse-reporter` | Convergent | Status reports, dashboards | Aggregation, reporting |

**Characteristic**: Formal, standards-compliant, structured output formats

### 1.3 Synergy Analysis

```
┌─────────────────────────────────────────────────────────────────┐
│                    COGNITIVE MODE SPECTRUM                       │
│                                                                  │
│  DIVERGENT ◄──────────────────────────────────────► CONVERGENT  │
│  (Explore)                                            (Formalize)│
│                                                                  │
│  ps-researcher ─────┐                                            │
│                     │                                            │
│  ps-analyst ────────┼──────────────────┐                         │
│                     │                  │                         │
│                     │    ps-architect ─┼───────────┐             │
│                     │                  │           │             │
│                     │   ps-synthesizer ┼───────────┼─────┐       │
│                     │                  │           │     │       │
│                     │                  │  nse-risk ┼─────┼───┐   │
│                     │                  │           │     │   │   │
│                     │     nse-requirements ────────┼─────┼───┼─┐ │
│                     │                              │     │   │ │ │
│                     │              nse-architecture┼─────┼───┼─┼─┤
│                     │                              │     │   │ │ │
│                     │                  nse-reviewer┼─────┼───┼─┼─┤
│                     │                              │     │   │ │ │
│                     │             nse-verification─┼─────┼───┼─┼─┤
│                     │                              │     │   │ │ │
│                     │                 nse-reporter─┼─────┼───┼─┼─┘
│                     │                              │     │   │ │
└─────────────────────┴──────────────────────────────┴─────┴───┴─┘
```

---

## 2. Cross-Pollination Value Matrix

### 2.1 ps-* → nse-* Handoffs

| Source Agent | Target Agent | Artifact Type | Value Created |
|--------------|--------------|---------------|---------------|
| ps-researcher | nse-requirements | Research findings | Options → formal requirements |
| ps-researcher | nse-risk | Technology options | Options → risk factors |
| ps-analyst | nse-risk | Gap analysis | Gaps → tracked risks |
| ps-analyst | nse-requirements | Trade study | Decisions → requirement updates |
| ps-architect | nse-architecture | ADR decisions | Decisions → TSR/ICD specs |
| ps-architect | nse-verification | Design rationale | Rationale → verification criteria |
| ps-synthesizer | nse-reporter | Unified findings | Synthesis → status reports |

### 2.2 nse-* → ps-* Handoffs

| Source Agent | Target Agent | Artifact Type | Value Created |
|--------------|--------------|---------------|---------------|
| nse-requirements | ps-researcher | Requirement gaps | Gaps → research targets |
| nse-requirements | ps-analyst | Formal requirements | Requirements → analysis scope |
| nse-risk | ps-analyst | Risk patterns | Risks → analysis priorities |
| nse-risk | ps-synthesizer | Risk register | Risks → synthesis considerations |
| nse-reviewer | ps-analyst | Review findings | Findings → gap analysis input |
| nse-architecture | ps-architect | Spec constraints | Constraints → design decisions |
| nse-verification | ps-analyst | V&V gaps | Gaps → analysis targets |

### 2.3 Handoff Value Scoring

| Handoff | Frequency | Impact | Priority |
|---------|-----------|--------|----------|
| ps-researcher → nse-requirements | High | High | P1 |
| ps-analyst → nse-risk | High | High | P1 |
| ps-architect → nse-architecture | Medium | High | P1 |
| nse-risk → ps-synthesizer | Medium | High | P2 |
| nse-requirements → ps-researcher | Medium | Medium | P2 |
| nse-reviewer → ps-analyst | Low | Medium | P3 |

---

## 3. Sync Barrier Architecture

### 3.1 Barrier Design Principles

1. **Atomic Phases**: Each pipeline phase completes before barrier
2. **Bidirectional Exchange**: Both pipelines contribute and receive
3. **Artifact Extraction**: Orchestrator extracts key information
4. **Context Injection**: Summarized context injected into next phase
5. **File Persistence**: All artifacts persisted for audit trail

### 3.2 Barrier Implementation Pattern

```
┌──────────────────────────────────────────────────────────────────┐
│                      SYNC BARRIER N                               │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│  STEP 1: COMPLETION WAIT                                          │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │ Orchestrator waits for all Phase N agents to complete       │ │
│  │ • Check TaskOutput for all agent IDs                        │ │
│  │ • Verify artifact files exist                               │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                              │                                    │
│                              ▼                                    │
│  STEP 2: ARTIFACT COLLECTION                                      │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │ Read all output artifacts from Phase N                      │ │
│  │ • ps-* outputs: research/*.md, analysis/*.md                │ │
│  │ • nse-* outputs: requirements/*.md, risks/*.md              │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                              │                                    │
│                              ▼                                    │
│  STEP 3: EXTRACTION                                               │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │ Extract cross-pollination artifacts                         │ │
│  │ • ps-to-nse: Key findings, options, decisions               │ │
│  │ • nse-to-ps: Gaps, constraints, formal requirements         │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                              │                                    │
│                              ▼                                    │
│  STEP 4: PERSISTENCE                                              │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │ Write cross-pollination artifacts                           │ │
│  │ • cross-pollination/barrier-N/ps-to-nse/*.md                │ │
│  │ • cross-pollination/barrier-N/nse-to-ps/*.md                │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                              │                                    │
│                              ▼                                    │
│  STEP 5: CONTEXT PREPARATION                                      │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │ Prepare injected context for Phase N+1                      │ │
│  │ • Summarize ps-to-nse for nse-* agents                      │ │
│  │ • Summarize nse-to-ps for ps-* agents                       │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                              │                                    │
│                              ▼                                    │
│  STEP 6: LAUNCH PHASE N+1                                         │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │ Launch next phase with cross-pollinated context             │ │
│  │ • ps-* agents receive nse-* context                         │ │
│  │ • nse-* agents receive ps-* context                         │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                                                                   │
└──────────────────────────────────────────────────────────────────┘
```

### 3.3 Barrier Schedule

| Barrier | After Phase | ps-* State | nse-* State | Exchange Type |
|---------|-------------|------------|-------------|---------------|
| 1 | Research/Scope | Research complete | Requirements scoped | Options ↔ Gaps |
| 2 | Analysis/Risk | Gaps analyzed | Risks identified | Gaps ↔ Risks |
| 3 | Design/Formal | ADRs decided | Specs drafted | Decisions ↔ Constraints |
| Final | Synthesis/Review | Synthesis ready | Review complete | Merge outputs |

---

## 4. Directory Structure

```
projects/PROJ-002-nasa-systems-engineering/
├── cross-pollination/
│   ├── barrier-1/
│   │   ├── ps-to-nse/
│   │   │   ├── research-summary.md
│   │   │   └── options-identified.md
│   │   └── nse-to-ps/
│   │       ├── requirements-gaps.md
│   │       └── scope-constraints.md
│   ├── barrier-2/
│   │   ├── ps-to-nse/
│   │   │   ├── gap-analysis-summary.md
│   │   │   └── trade-study-decisions.md
│   │   └── nse-to-ps/
│   │       ├── risk-patterns.md
│   │       └── formal-requirements.md
│   ├── barrier-3/
│   │   ├── ps-to-nse/
│   │   │   ├── adr-decisions.md
│   │   │   └── architecture-rationale.md
│   │   └── nse-to-ps/
│   │       ├── spec-constraints.md
│   │       └── verification-criteria.md
│   └── final/
│       ├── unified-synthesis.md
│       └── cross-pollination-report.md
├── ps-pipeline/
│   ├── phase-1-research/
│   ├── phase-2-analysis/
│   ├── phase-3-design/
│   └── phase-4-synthesis/
└── nse-pipeline/
    ├── phase-1-scope/
    ├── phase-2-risk/
    ├── phase-3-formal/
    └── phase-4-review/
```

---

## 5. Orchestration Sequence Diagram

```
Time
 │
 │  ┌─────────────┐     ┌─────────────┐
 │  │ ps-research │     │nse-requirem │
 │  │  (3 agents) │     │  (2 agents) │
 │  └──────┬──────┘     └──────┬──────┘
 │         │ artifacts         │ artifacts
 │         ▼                   ▼
 │  ╔══════════════════════════════════╗
 │  ║        SYNC BARRIER 1            ║
 │  ║  Orchestrator extracts/injects   ║
 │  ╚══════════════════════════════════╝
 │         │                   │
 │         │ +nse context      │ +ps context
 │         ▼                   ▼
 │  ┌─────────────┐     ┌─────────────┐
 │  │ ps-analyst  │     │  nse-risk   │
 │  │  (2 agents) │     │  (2 agents) │
 │  └──────┬──────┘     └──────┬──────┘
 │         │ artifacts         │ artifacts
 │         ▼                   ▼
 │  ╔══════════════════════════════════╗
 │  ║        SYNC BARRIER 2            ║
 │  ║  Orchestrator extracts/injects   ║
 │  ╚══════════════════════════════════╝
 │         │                   │
 │         │ +nse context      │ +ps context
 │         ▼                   ▼
 │  ┌─────────────┐     ┌─────────────┐
 │  │ ps-architect│     │nse-architect│
 │  │  (1 agent)  │     │  (1 agent)  │
 │  └──────┬──────┘     └──────┬──────┘
 │         │ artifacts         │ artifacts
 │         ▼                   ▼
 │  ╔══════════════════════════════════╗
 │  ║        SYNC BARRIER 3            ║
 │  ║  Orchestrator extracts/injects   ║
 │  ╚══════════════════════════════════╝
 │         │                   │
 │         │ +nse context      │ +ps context
 │         ▼                   ▼
 │  ┌─────────────┐     ┌─────────────┐
 │  │ps-synthesiz │     │ nse-review  │
 │  │  (1 agent)  │     │  (2 agents) │
 │  └──────┬──────┘     └──────┬──────┘
 │         │ artifacts         │ artifacts
 │         ▼                   ▼
 │  ╔══════════════════════════════════╗
 │  ║        FINAL BARRIER             ║
 │  ║  Merge into unified deliverable  ║
 │  ╚══════════════════════════════════╝
 │                   │
 │                   ▼
 │         ┌─────────────────┐
 │         │ UNIFIED OUTPUT  │
 │         └─────────────────┘
 ▼
```

---

## 6. Constraint Compliance

### 6.1 P-003 Compliance (No Recursive Subagents)

```
✓ COMPLIANT: Orchestrator spawns all agents directly
✗ VIOLATION: Subagent spawning another subagent

Correct Pattern:
  Orchestrator ──► ps-researcher (OK)
  Orchestrator ──► nse-requirements (OK)
  Orchestrator ──► ps-analyst (OK)

Violation Pattern:
  ps-researcher ──► ps-analyst (FORBIDDEN)
```

### 6.2 Parallel Execution Limits

- Maximum 10 concurrent subagents
- Batch if total agents > 10
- Phase-based batching naturally limits concurrency

### 6.3 Context Isolation

- Each subagent has fresh 200K context window
- Orchestrator manages cross-pollination context injection
- File-based artifacts prevent context pollution

---

## 7. Implementation Checklist

### Phase 1 Prerequisites
- [ ] Create directory structure
- [ ] Define artifact schemas
- [ ] Prepare agent prompts with handoff instructions

### Barrier 1 Implementation
- [ ] Wait for Phase 1 completion
- [ ] Read ps-* research outputs
- [ ] Read nse-* requirements outputs
- [ ] Extract key options (ps → nse)
- [ ] Extract requirement gaps (nse → ps)
- [ ] Write cross-pollination artifacts
- [ ] Prepare Phase 2 context injections

### Barrier 2 Implementation
- [ ] Wait for Phase 2 completion
- [ ] Read ps-* analysis outputs
- [ ] Read nse-* risk outputs
- [ ] Extract gap analysis (ps → nse)
- [ ] Extract risk patterns (nse → ps)
- [ ] Write cross-pollination artifacts
- [ ] Prepare Phase 3 context injections

### Barrier 3 Implementation
- [ ] Wait for Phase 3 completion
- [ ] Read ps-* architecture outputs
- [ ] Read nse-* formal outputs
- [ ] Extract ADR decisions (ps → nse)
- [ ] Extract spec constraints (nse → ps)
- [ ] Write cross-pollination artifacts
- [ ] Prepare Phase 4 context injections

### Final Barrier Implementation
- [ ] Wait for Phase 4 completion
- [ ] Read ps-* synthesis outputs
- [ ] Read nse-* review outputs
- [ ] Merge into unified deliverable
- [ ] Generate cross-pollination report

---

## 8. Risk Considerations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Agent timeout during phase | Medium | Retry with extended timeout |
| Context extraction misses key info | High | Structured extraction templates |
| Circular dependency in phases | High | DAG-based phase ordering |
| Artifact schema mismatch | Medium | Standardized L0/L1/L2 levels |
| Orchestrator context overflow | Medium | Summarize before injection |

---

## References

1. `agent-research-001-claude-code-mechanics.md` - Task tool constraints
2. `agent-research-002-multi-agent-patterns.md` - Orchestration patterns
3. `proj-002-e-009-integration-trade-study.md` - Integration value analysis
4. `proj-002-integration-synthesis.md` - Integration recommendations

---

*Architecture design by Claude Opus 4.5*
*Document created: 2026-01-09*
