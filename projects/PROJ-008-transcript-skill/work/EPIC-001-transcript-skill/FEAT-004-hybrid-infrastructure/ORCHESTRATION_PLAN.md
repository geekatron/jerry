# ORCHESTRATION_PLAN.md

> **Document ID:** FEAT-004-ORCH-PLAN
> **Project:** PROJ-008-transcript-skill
> **Workflow ID:** `feat004-tdd-20260129-001`
> **Status:** ACTIVE
> **Version:** 2.0
> **Created:** 2026-01-29
> **Last Updated:** 2026-01-29

---

## 1. Executive Summary

This orchestration plan coordinates the creation of **TDD-FEAT-004 Hybrid Infrastructure Technical Design** using the `/jerry:problem-solving` skill agents. The workflow addresses the operational findings from DISC-009 (99.8% data loss, ad-hoc workaround) by designing a comprehensive hybrid architecture for the transcript skill.

**Current State:** Phase 1 pending (Research)

**Orchestration Pattern:** Sequential with Feedback Loops

### 1.1 Workflow Identification

| Field | Value | Source |
|-------|-------|--------|
| Workflow ID | `feat004-tdd-20260129-001` | auto |
| ID Format | `{purpose}-{YYYYMMDD}-{NNN}` | semantic-date-seq |
| Base Path | `FEAT-004-hybrid-infrastructure/docs/` | Dynamic |

**Artifact Output Locations:**
- Research: `FEAT-004-hybrid-infrastructure/docs/research/`
- Analysis: `FEAT-004-hybrid-infrastructure/docs/analysis/`
- Design: `FEAT-004-hybrid-infrastructure/docs/design/`
- Critiques: `FEAT-004-hybrid-infrastructure/docs/critiques/`

---

## 2. Workflow Architecture

### 2.1 Pipeline Diagram

```
FEAT-004 TDD CREATION WORKFLOW (Sequential with Feedback Loops)
================================================================

                    ┌─────────────────────────────────────────────────────────┐
                    │                   USER DECISION                          │
                    │              (DEC-011: ts-parser Hybrid Role)            │
                    └──────────────────────────┬──────────────────────────────┘
                                               │
                                               ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│ PHASE 1: RESEARCH (ps-researcher)                                    TASK-240  │
├─────────────────────────────────────────────────────────────────────────────────┤
│ • Hybrid architecture patterns (Strategy Pattern, Orchestrator)                 │
│ • Python parsing libraries (webvtt-py, pysrt, chardet)                         │
│ • Chunking strategies (LangChain, semantic splitting)                          │
│ • RED/GREEN/REFACTOR TDD best practices                                        │
│ • Industry evidence with citations                                             │
│                                                                                 │
│ OUTPUT: FEAT-004-e-240-hybrid-architecture-research.md                         │
│ STATUS: PENDING                                                                │
└─────────────────────────────────────────────────────────────────────────────────┘
                                               │
                                               ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│ PHASE 2: ANALYSIS (ps-analyst)                                       TASK-241  │
├─────────────────────────────────────────────────────────────────────────────────┤
│ • Blast radius assessment (ts-parser, ts-extractor, SKILL.md)                  │
│ • Gap mapping (DISC-009 → Implementation requirements)                         │
│ • 5W2H analysis for hybrid transformation                                      │
│ • FMEA risk assessment for architecture change                                 │
│ • Enabler dependency analysis (EN-020, EN-021, EN-022, EN-023)                │
│                                                                                 │
│ INPUT: Phase 1 research                                                        │
│ OUTPUT: FEAT-004-e-241-blast-radius-analysis.md                                │
│ STATUS: BLOCKED (awaiting Phase 1)                                             │
│                                                                                 │
│ FEEDBACK LOOP: If analysis reveals research gaps → revise Phase 1              │
└─────────────────────────────────────────────────────────────────────────────────┘
                                               │
                                               ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│ PHASE 3: ARCHITECTURE (ps-architect)                                 TASK-242  │
├─────────────────────────────────────────────────────────────────────────────────┤
│ Create TDD-FEAT-004-hybrid-infrastructure.md with:                             │
│ • Section 1: Problem Statement (DISC-009 operational findings)                 │
│ • Section 2: Hybrid Architecture Design (Strategy Pattern)                     │
│ • Section 3: ts-parser.md Transformation (Orchestrator/Delegator/Fallback)     │
│ • Section 4: Python Parser Implementation (EN-020 specs)                       │
│ • Section 5: Chunking Strategy (EN-021 specs)                                  │
│ • Section 6: ts-extractor.md Adaptation (EN-022 specs)                         │
│ • Section 7: Integration Testing (EN-023 specs)                                │
│ • Section 8: Testing Strategy (RED/GREEN/REFACTOR)                             │
│ • Section 9: Implementation Roadmap (Work Item specifications)                 │
│ • Section 10: Migration Strategy (Incremental adoption)                        │
│                                                                                 │
│ INPUT: Phase 1 research + Phase 2 analysis                                     │
│ OUTPUT: TDD-FEAT-004-hybrid-infrastructure.md                                  │
│ STATUS: BLOCKED (awaiting Phase 2)                                             │
│                                                                                 │
│ FEEDBACK LOOP: If design reveals analysis gaps → revise Phase 2                │
└─────────────────────────────────────────────────────────────────────────────────┘
                                               │
                                               ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│ PHASE 4: VALIDATION (ps-critic)                                      TASK-243  │
├─────────────────────────────────────────────────────────────────────────────────┤
│ • Quality score evaluation (threshold: 0.95)                                   │
│ • DISC-009 requirements traceability                                           │
│ • DEC-011 alignment verification                                               │
│ • Completeness assessment (all enablers addressed)                             │
│ • Actionability check (work items can be created from TDD)                     │
│                                                                                 │
│ INPUT: TDD-FEAT-004-hybrid-infrastructure.md                                   │
│ OUTPUT: FEAT-004-e-243-tdd-validation-critique.md                              │
│ STATUS: BLOCKED (awaiting Phase 3)                                             │
│                                                                                 │
│ FEEDBACK LOOP: If score < 0.95 → revise Phase 3 with specific issues           │
└─────────────────────────────────────────────────────────────────────────────────┘
                                               │
                                               ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│ GATE-5: HUMAN APPROVAL                                               TASK-244  │
├─────────────────────────────────────────────────────────────────────────────────┤
│ • Human review of TDD-FEAT-004                                                 │
│ • Approval to proceed with EN-020..023 implementation                          │
│ • Approval to update enabler files with TDD specifications                     │
│                                                                                 │
│ STATUS: BLOCKED (awaiting Phase 4)                                             │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### 2.2 Orchestration Pattern Classification

| Pattern | Applied | Description |
|---------|---------|-------------|
| Sequential | Yes | Phases execute in order (Research → Analysis → Architecture → Validation) |
| Concurrent | No | Single pipeline |
| Feedback Loops | **Yes** | Downstream phases can request upstream revision |
| Hierarchical | Yes | Orchestrator delegates to ps-* agents |

### 2.3 Feedback Loop Protocol

```
FEEDBACK LOOP MECHANISM
=======================

When downstream phase identifies gaps:

1. DETECTION
   - Agent identifies missing research, analysis, or design element
   - Gap documented with specific requirements

2. ESCALATION
   - Feedback artifact created: FEAT-004-e-{NNN}-{phase}-feedback.md
   - Previous phase status changed to IN_PROGRESS (revision)
   - Quality score reset

3. REVISION
   - Upstream agent revises artifact addressing feedback
   - New version number (v2, v3, etc.)

4. CONTINUATION
   - Downstream phase resumes with revised input
   - Feedback artifact marked as ADDRESSED

EXAMPLE:
  ps-analyst discovers missing webvtt-py performance data
  → Creates feedback artifact
  → ps-researcher revises research with performance benchmarks
  → ps-analyst continues with enriched research
```

---

## 3. Phase Definitions

### 3.1 Phase Summary

| Phase | Name | Agent | Purpose | TASK ID | Status |
|-------|------|-------|---------|---------|--------|
| 1 | Research | ps-researcher | Industry patterns, evidence gathering | TASK-240 | PENDING |
| 2 | Analysis | ps-analyst | Blast radius, gap mapping, FMEA | TASK-241 | BLOCKED |
| 3 | Architecture | ps-architect | TDD document creation | TASK-242 | BLOCKED |
| 4 | Validation | ps-critic | Quality review (0.95 threshold) | TASK-243 | BLOCKED |
| GATE | Human Approval | Human | Review and approve TDD | TASK-244 | BLOCKED |

### 3.2 Phase Dependencies

```
TASK-240 (Research)
    │
    └──► TASK-241 (Analysis) ◄──┐
            │                    │
            └──► TASK-242 (Architecture) ◄──┐
                    │                        │
                    └──► TASK-243 (Validation)
                            │
                            └──► TASK-244 (Human Gate)

FEEDBACK LOOPS:
  TASK-241 ───feedback───► TASK-240
  TASK-242 ───feedback───► TASK-241
  TASK-243 ───feedback───► TASK-242
```

---

## 4. Research Scope (Phase 1)

### 4.1 Research Questions

| RQ | Question | Source |
|----|----------|--------|
| RQ-1 | What patterns exist for LLM orchestrators with Python delegation? | Context7, WebSearch |
| RQ-2 | How do production systems implement format-specific routing? | Industry examples |
| RQ-3 | What are webvtt-py performance characteristics for large files? | Benchmarks, testing |
| RQ-4 | What chunking strategies minimize "Lost-in-the-Middle" degradation? | Stanford research |
| RQ-5 | What are RED/GREEN/REFACTOR best practices for hybrid architectures? | Kent Beck, TDD literature |
| RQ-6 | How do Python parsers for SRT/plain text compare to LLM parsing? | Library comparison |

### 4.2 Required Evidence

| Evidence | Type | Purpose |
|----------|------|---------|
| Strategy Pattern reference | Citation | ts-parser orchestrator design |
| webvtt-py documentation | Library docs | VTT parser specifications |
| pysrt documentation | Library docs | SRT parser specifications |
| LangChain chunking | Framework docs | Chunking strategy patterns |
| Stanford Lost-in-the-Middle | Research paper | Chunking justification |
| TDD best practices | Industry guidance | Testing strategy |

---

## 5. Analysis Scope (Phase 2)

### 5.1 Blast Radius Assessment

| Component | Change Type | Impact | Complexity |
|-----------|-------------|--------|------------|
| ts-parser.md | **MAJOR** | Transformed to orchestrator | HIGH |
| SKILL.md | MODERATE | Pipeline flow update | MEDIUM |
| ts-extractor.md | MODERATE | Chunked input support | MEDIUM |
| EN-020 (Python Parser) | NEW | Python VTT implementation | HIGH |
| EN-021 (Chunking) | NEW | Index + chunk strategy | MEDIUM |
| EN-022 (Extractor) | UPDATE | Interface adaptation | LOW |
| EN-023 (Testing) | UPDATE | Integration test specs | MEDIUM |
| Test specifications | EXTEND | New contract tests | MEDIUM |

### 5.2 5W2H Analysis Framework

| Question | Application |
|----------|-------------|
| **What** | Transform ts-parser.md from direct parser to orchestrator |
| **Why** | DISC-009: 99.8% data loss, ad-hoc workaround, scalability |
| **Who** | Claude (implementation), User (approval) |
| **When** | After TDD approval (GATE-5) |
| **Where** | skills/transcript/agents/, skills/transcript/src/ |
| **How** | Strategy Pattern with Python delegation and LLM fallback |
| **How Much** | 4 enablers (EN-020..023), ~25 tasks |

---

## 6. TDD Scope (Phase 3)

### 6.1 TDD Section Requirements

| Section | Title | Content Requirements |
|---------|-------|---------------------|
| 1 | Problem Statement | DISC-009 findings, 99.8% data loss, operational impact |
| 2 | Architecture Overview | Hybrid model diagram, component relationships |
| 3 | ts-parser.md Transformation | Orchestrator/Delegator/Fallback/Validator roles |
| 4 | Python Parser (EN-020) | webvtt-py integration, interface contracts |
| 5 | Chunking Strategy (EN-021) | Index schema, chunk schema, navigation |
| 6 | Extractor Adaptation (EN-022) | Chunked input handling, citation preservation |
| 7 | Integration Testing (EN-023) | Contract tests, E2E validation |
| 8 | Testing Strategy | RED/GREEN/REFACTOR cycle, coverage targets |
| 9 | Implementation Roadmap | Work item specifications, dependencies |
| 10 | Migration Strategy | Incremental adoption, backward compatibility |

### 6.2 TDD Quality Criteria

| Criterion | Requirement |
|-----------|-------------|
| Completeness | All enablers (EN-020..023) fully specified |
| Actionability | Work items can be created directly from TDD |
| Traceability | DISC-009 requirements mapped to specifications |
| Evidence-based | All claims supported by citations |
| L0/L1/L2 | Three-persona documentation |

---

## 7. State Management

### 7.1 State Files

| File | Purpose |
|------|---------|
| `ORCHESTRATION.yaml` | Machine-readable state (SSOT) |
| `ORCHESTRATION_PLAN.md` | This file - strategic context |

### 7.2 Artifact Path Structure

```
FEAT-004-hybrid-infrastructure/
├── docs/
│   ├── research/
│   │   └── FEAT-004-e-240-hybrid-architecture-research.md
│   ├── analysis/
│   │   └── FEAT-004-e-241-blast-radius-analysis.md
│   ├── design/
│   │   └── TDD-FEAT-004-hybrid-infrastructure.md
│   └── critiques/
│       └── FEAT-004-e-243-tdd-validation-critique.md
├── ORCHESTRATION_PLAN.md
├── ORCHESTRATION.yaml
├── FEAT-004--DEC-011-ts-parser-hybrid-role.md
└── [Enabler folders]
```

---

## 8. Success Criteria

### 8.1 Phase Exit Criteria

| Phase | Exit Criteria |
|-------|---------------|
| Phase 1 | Research document created with all RQ answered, citations provided |
| Phase 2 | Blast radius assessment complete, FMEA documented, gaps mapped |
| Phase 3 | TDD created with all 10 sections, ps-critic score >= 0.95 |
| Phase 4 | Quality validation passed, no blocking issues |
| GATE-5 | Human approval received |

### 8.2 Workflow Completion Criteria

| Criterion | Validation |
|-----------|------------|
| TDD created | TDD-FEAT-004-hybrid-infrastructure.md exists |
| Quality passed | ps-critic score >= 0.95 |
| Human approved | TASK-244 marked DONE |
| Enablers updated | EN-020..023 reference TDD |

---

## 9. Risk Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Research scope creep | Medium | Medium | RQ-bounded research, time-box |
| Analysis paralysis | Low | High | 5W2H framework constraints |
| TDD too abstract | Medium | High | Work item creation test |
| Feedback loop infinite | Low | Medium | Max 2 iterations per loop |
| Quality threshold too high | Low | Low | User can override 0.95 |

---

## 10. Resumption Context

### 10.1 Current Execution State

```
WORKFLOW STATUS AS OF 2026-01-29
================================

Phase 1 (Research):     PENDING
Phase 2 (Analysis):     BLOCKED (awaiting Phase 1)
Phase 3 (Architecture): BLOCKED (awaiting Phase 2)
Phase 4 (Validation):   BLOCKED (awaiting Phase 3)
GATE-5 (Human):         BLOCKED (awaiting Phase 4)

Feedback Loops:         None active
```

### 10.2 Next Actions

1. Create TASK-240 through TASK-244 files
2. Invoke ps-researcher for Phase 1 (TASK-240)
3. Update ORCHESTRATION.yaml with agent completion
4. Continue to Phase 2 after Phase 1 complete

---

*Document ID: FEAT-004-ORCH-PLAN*
*Workflow ID: feat004-tdd-20260129-001*
*Version: 2.0*
*Cross-Session Portable: All paths are repository-relative*
