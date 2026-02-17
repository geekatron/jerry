# ORCHESTRATION_PLAN.md

> **Document ID:** PROJ-001-ORCH-PLAN
> **Project:** PROJ-001-oss-release
> **Workflow ID:** `epic002-crosspoll-20260213-001`
> **Status:** ACTIVE
> **Version:** 2.0
> **Created:** 2026-02-13
> **Last Updated:** 2026-02-13

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Executive Summary](#executive-summary) | Workflow overview and orchestration pattern |
| [Workflow Architecture](#workflow-architecture) | Pipeline diagram and pattern classification |
| [Phase Definitions](#phase-definitions) | Detailed phase breakdown for both pipelines |
| [Adversarial Feedback Protocol](#adversarial-feedback-protocol) | Creator→Critic→Revision cycle enforcement |
| [Sync Barrier Protocol](#sync-barrier-protocol) | Cross-pollination rules and artifacts |
| [Agent Registry](#agent-registry) | Complete agent assignments with roles |
| [State Management](#state-management) | Files, paths, and checkpoint strategy |
| [Execution Constraints](#execution-constraints) | Hard and soft constraints |
| [Success Criteria](#success-criteria) | Exit criteria per phase and workflow |
| [Risk Mitigations](#risk-mitigations) | Risk register and mitigations |
| [Resumption Context](#resumption-context) | Current state and next actions |

---

## 1. Executive Summary

This orchestration plan coordinates the completion of **EPIC-002: Quality Framework Enforcement & Course Correction**, managing two parallel pipelines (FEAT-004 and FEAT-005) with strategic cross-pollination to ensure coherent integration of adversarial strategies and enforcement mechanisms.

**Problem Statement:**
Having completed foundational research (EN-301: 15 adversarial strategies, EN-401: 62 enforcement vectors), Jerry now faces the challenge of transforming raw catalogs into actionable, integrated capabilities. This requires rigorous selection frameworks, situational mapping, skill enhancements across /problem-solving, /nasa-se, and /orchestration, and robust enforcement implementations. The work is complex, interdependent, and requires adversarial validation at every stage to meet Jerry's >= 0.92 quality gate threshold.

**Solution:**
A cross-pollinated dual-pipeline orchestration where:
- **Pipeline A (adv)** refines adversarial strategies through selection, mapping, and skill integration
- **Pipeline B (enf)** refines enforcement mechanisms through prioritization and implementation
- **Strategic barriers** synchronize the pipelines, allowing decisions in one to inform the other

**Current State:** Workflow initialized. Both pipelines in PHASE_1_PENDING. All agents ready for execution.

**Orchestration Pattern:** Concurrent Cross-Pollinated Pipeline with Adversarial Feedback Loops

### 1.1 Workflow Identification

| Field | Value | Source |
|-------|-------|--------|
| Workflow ID | `epic002-crosspoll-20260213-001` | auto |
| ID Format | `epic002-crosspoll-YYYYMMDD-NNN` | semantic-date-seq |
| Base Path | `orchestration/epic002-crosspoll-20260213-001/` | Dynamic |

**Artifact Output Locations:**
- Pipeline A (adv): `orchestration/epic002-crosspoll-20260213-001/adv/`
- Pipeline B (enf): `orchestration/epic002-crosspoll-20260213-001/enf/`
- Cross-pollination: `orchestration/epic002-crosspoll-20260213-001/cross-pollination/`

---

## 2. Workflow Architecture

### 2.1 Pipeline Diagram

```
PIPELINE A (adv): Adversarial Strategy Research      PIPELINE B (enf): Enforcement Mechanisms
============================================          =========================================

┌────────────────────────────────────────┐          ┌────────────────────────────────────────┐
│ PHASE 1: Strategy Selection            │          │ PHASE 1: Enforcement Priority Analysis │
│ ────────────────────────────────────   │          │ ────────────────────────────────────   │
│ EN-302: Selection Framework (8 tasks)  │          │ EN-402: Priority Analysis (9 tasks)    │
│                                        │          │                                        │
│ Agents:                                │          │ Agents:                                │
│  • ps-analyst (criteria, scoring)      │          │  • ps-analyst (criteria, priority)     │
│  • nse-risk (risk assessment)          │          │  • nse-risk (vector risk)              │
│  • nse-architecture (trade study)      │          │  • nse-architecture (vector trades)    │
│  • ps-architect (ADR)                  │          │  • ps-architect (ADR, plans)           │
│  • ps-critic (adversarial review)      │          │  • ps-critic (adversarial review)      │
│  • ps-validator (validation)           │          │  • ps-validator (validation)           │
│                                        │          │                                        │
│ Deliverables:                          │          │ Deliverables:                          │
│  - 10 selected strategies              │          │  - Priority matrix (all vectors)       │
│  - Selection ADR                       │          │  - Enforcement ADR                     │
│  - Risk analysis                       │          │  - Execution plans (top 3)             │
│                                        │          │                                        │
│ STATUS: PENDING                        │          │ STATUS: PENDING                        │
└────────────┬───────────────────────────┘          └────────────┬───────────────────────────┘
             │                                                    │
             ▼                                                    ▼
    ╔════════════════════════════════════════════════════════════════════════╗
    ║                          SYNC BARRIER 1                                 ║
    ║  ┌──────────────────────────────────────────────────────────────────┐  ║
    ║  │ adv→enf: Selected strategies inform enforcement implementations  │  ║
    ║  │ enf→adv: Enforcement capabilities inform strategy feasibility    │  ║
    ║  │                                                                   │  ║
    ║  │ Cross-Pollination Artifacts:                                     │  ║
    ║  │  - barrier-1-adv-to-enf-handoff.md (10 strategies + use cases)   │  ║
    ║  │  - barrier-1-enf-to-adv-handoff.md (constraints + capabilities)  │  ║
    ║  └──────────────────────────────────────────────────────────────────┘  ║
    ║  STATUS: PENDING                                                        ║
    ╚════════════════════════════════════════════════════════════════════════╝
             │                                                    │
             ▼                                                    ▼
┌────────────────────────────────────────┐          ┌────────────────────────────────────────┐
│ PHASE 2: Situational Mapping           │          │ PHASE 2: Implementation (Hooks/Rules)  │
│ ────────────────────────────────────   │          │ ────────────────────────────────────   │
│ EN-303: Applicability Mapping (6 tks)  │          │ EN-403: Hook-Based (12 tasks)          │
│                                        │          │ EN-404: Rule-Based (10 tasks)          │
│ Agents:                                │          │                                        │
│  • ps-analyst (taxonomy, mapping)      │          │ Agents:                                │
│  • ps-architect (decision tree)        │          │  • ps-architect (requirements, design) │
│  • ps-critic (adversarial review)      │          │  • ps-implementer (implementation)     │
│  • ps-validator (validation)           │          │  • ps-critic (adversarial review)      │
│                                        │          │  • ps-validator (verification)         │
│ Deliverables:                          │          │                                        │
│  - Context taxonomy                    │          │ Deliverables:                          │
│  - Per-strategy situational map        │          │  - Hook implementations                │
│  - Decision tree                       │          │  - HARD rule language                  │
│                                        │          │  - Rule implementations                │
│ STATUS: BLOCKED (barrier-1)            │          │ STATUS: BLOCKED (barrier-1)            │
└────────────┬───────────────────────────┘          └────────────┬───────────────────────────┘
             │                                                    │
             ▼                                                    ▼
    ╔════════════════════════════════════════════════════════════════════════╗
    ║                          SYNC BARRIER 2                                 ║
    ║  ┌──────────────────────────────────────────────────────────────────┐  ║
    ║  │ adv→enf: Situational maps inform enforcement implementation      │  ║
    ║  │ enf→adv: Enforcement mechanisms inform strategy applicability    │  ║
    ║  │                                                                   │  ║
    ║  │ Cross-Pollination Artifacts:                                     │  ║
    ║  │  - barrier-2-adv-to-enf-handoff.md (context mappings)            │  ║
    ║  │  - barrier-2-enf-to-adv-handoff.md (enforcement patterns)        │  ║
    ║  └──────────────────────────────────────────────────────────────────┘  ║
    ║  STATUS: BLOCKED (phase-2)                                              ║
    ╚════════════════════════════════════════════════════════════════════════╝
             │                                                    │
             ▼                                                    ▼
┌────────────────────────────────────────┐          ┌────────────────────────────────────────┐
│ PHASE 3: Skill Enhancements            │          │ PHASE 3: Session Context Enforcement   │
│ ────────────────────────────────────   │          │ ────────────────────────────────────   │
│ EN-304: /problem-solving (10 tasks)    │          │ EN-405: Session Context (11 tasks)     │
│ EN-305: /nasa-se (10 tasks)            │          │                                        │
│ EN-307: /orchestration (13 tasks)      │          │ Agents:                                │
│                                        │          │  • ps-architect (requirements, design) │
│ Agents:                                │          │  • ps-implementer (preamble, hooks)    │
│  • ps-architect (requirements, design) │          │  • ps-critic (adversarial review)      │
│  • ps-implementer (adversarial modes)  │          │  • ps-validator (testing, validation)  │
│  • ps-critic (adversarial review)      │          │                                        │
│  • ps-validator (validation)           │          │ Deliverables:                          │
│                                        │          │  - Session preamble design             │
│ Deliverables:                          │          │  - Hook integrations                   │
│  - Adversarial invocation protocols    │          │  - Testing suite                       │
│  - Agent enhancements (PS, NSE, ORCH)  │          │                                        │
│  - Documentation updates               │          │ STATUS: BLOCKED (barrier-2)            │
│                                        │          │                                        │
│ STATUS: BLOCKED (barrier-2)            │          │                                        │
└────────────┬───────────────────────────┘          └────────────┬───────────────────────────┘
             │                                                    │
             ▼                                                    ▼
┌────────────────────────────────────────┐          ┌────────────────────────────────────────┐
│ PHASE 4: Integration Testing           │          │ PHASE 4: Integration Testing           │
│ ────────────────────────────────────   │          │ ────────────────────────────────────   │
│ EN-306: Integration Tests (8 tasks)    │          │ EN-406: Integration Tests (13 tasks)   │
│                                        │          │                                        │
│ Agents:                                │          │ Agents:                                │
│  • ps-validator (test plan, execution) │          │  • ps-validator (test plan, execution) │
│  • ps-critic (QA audit)                │          │  • ps-critic (QA audit)                │
│                                        │          │                                        │
│ Deliverables:                          │          │ Deliverables:                          │
│  - Integration test suite              │          │  - Integration test suite              │
│  - Cross-platform validation           │          │  - Cross-platform validation           │
│  - QA audit report                     │          │  - Performance tests                   │
│                                        │          │  - QA audit report                     │
│ STATUS: BLOCKED (phase-3)              │          │ STATUS: BLOCKED (phase-3)              │
└────────────┬───────────────────────────┘          └────────────┬───────────────────────────┘
             │                                                    │
             ▼                                                    ▼
    ╔════════════════════════════════════════════════════════════════════════╗
    ║                      FINAL SYNTHESIS BARRIER                            ║
    ║  ┌──────────────────────────────────────────────────────────────────┐  ║
    ║  │ Integration findings cross-pollinate for final quality assurance │  ║
    ║  │                                                                   │  ║
    ║  │ Final Artifacts:                                                 │  ║
    ║  │  - epic002-final-synthesis.md (comprehensive summary)            │  ║
    ║  │  - epic002-integration-report.md (combined test results)         │  ║
    ║  │  - epic002-lessons-learned.md (process insights)                 │  ║
    ║  └──────────────────────────────────────────────────────────────────┘  ║
    ║  STATUS: BLOCKED (phase-4)                                              ║
    ╚════════════════════════════════════════════════════════════════════════╝
             │
             ▼
        EPIC-002 COMPLETE
```

### 2.2 Orchestration Pattern Classification

| Pattern | Applied | Description |
|---------|---------|-------------|
| Sequential | Yes | Phases execute in order within each pipeline |
| Concurrent | Yes | Both pipelines run in parallel between barriers |
| Barrier Sync | Yes | Cross-pollination at 2 major + 1 final barrier |
| Hierarchical | Yes | Orchestrator delegates to worker agents (P-003 compliant) |
| Adversarial Feedback | Yes | Every deliverable goes through creator→critic→revision cycles |

---

## 3. Phase Definitions

### 3.1 Pipeline A (adv) Phases

| Phase | Name | Purpose | Enablers | Agents | Status |
|-------|------|---------|----------|--------|--------|
| 1 | Strategy Selection | Select best 10 from 15 strategies via weighted decision framework | EN-302 | ps-analyst, nse-risk, nse-architecture, ps-architect, ps-critic, ps-validator | PENDING |
| 2 | Situational Mapping | Map selected strategies to situational contexts and create decision tree | EN-303 | ps-analyst, ps-architect, ps-critic, ps-validator | BLOCKED (barrier-1) |
| 3 | Skill Enhancements | Integrate adversarial modes into PS, NSE, ORCH skills | EN-304, EN-305, EN-307 | ps-architect, ps-implementer, ps-critic, ps-validator | BLOCKED (barrier-2) |
| 4 | Integration Testing | Validate skill enhancements across contexts and platforms | EN-306 | ps-validator, ps-critic | BLOCKED (phase-3) |

### 3.2 Pipeline B (enf) Phases

| Phase | Name | Purpose | Enablers | Agents | Status |
|-------|------|---------|----------|--------|--------|
| 1 | Enforcement Priority | Prioritize enforcement vectors via weighted analysis and create ADR | EN-402 | ps-analyst, nse-risk, nse-architecture, ps-architect, ps-critic, ps-validator | PENDING |
| 2 | Implementation (Hooks/Rules) | Implement hook-based and rule-based enforcement mechanisms | EN-403, EN-404 | ps-architect, ps-implementer, ps-critic, ps-validator | BLOCKED (barrier-1) |
| 3 | Session Context | Implement session preamble and context enforcement | EN-405 | ps-architect, ps-implementer, ps-critic, ps-validator | BLOCKED (barrier-2) |
| 4 | Integration Testing | Validate enforcement mechanisms across scenarios and platforms | EN-406 | ps-validator, ps-critic | BLOCKED (phase-3) |

---

## 4. Adversarial Feedback Protocol

### 4.1 Mandatory Feedback Loop Structure

**Every enabler's deliverables MUST go through:**

```
ITERATION 1:
  1. CREATOR produces artifact (ps-analyst, ps-architect, nse-architecture, etc.)
  2. CRITIC applies adversarial strategy and produces critique (ps-critic)
  3. CREATOR revises based on critique
  4. SCORE artifact (LLM-as-Judge pattern from S-014)

ITERATION 2:
  5. CRITIC applies different adversarial strategy
  6. CREATOR revises
  7. SCORE artifact

ITERATION 3:
  8. CRITIC applies third adversarial strategy
  9. CREATOR revises
  10. SCORE artifact

VALIDATION:
  11. If score >= 0.92, proceed to next phase
  12. If score < 0.92, repeat with focused critique on weak areas
```

**Minimum Requirements:**
- **3 iterations** of creator→critic→revision per enabler
- **Quality score >= 0.92** required to pass
- **Different adversarial strategies** applied across iterations (from EN-301 catalog)

### 4.2 Adversarial Strategy Mapping

#### EN-302 (Strategy Selection Framework)
| Iteration | Adversarial Strategy | Rationale |
|-----------|---------------------|-----------|
| 1 | S-002 Devil's Advocate | Challenge decision criteria and weighting choices |
| 2 | S-005 Dialectical Inquiry | Create antithesis to selection rationale |
| 3 | S-014 LLM-as-Judge | Score with structured rubric (effectiveness, completeness, clarity) |

#### EN-303 (Situational Applicability Mapping)
| Iteration | Adversarial Strategy | Rationale |
|-----------|---------------------|-----------|
| 1 | S-003 Steelman | Strengthen weak contextual mappings before critique |
| 2 | S-006 ACH | Test alternative hypotheses for situational triggers |
| 3 | S-014 LLM-as-Judge | Score mapping completeness and decision tree robustness |

#### EN-304, EN-305, EN-307 (Skill Enhancements)
| Iteration | Adversarial Strategy | Rationale |
|-----------|---------------------|-----------|
| 1 | S-001 Red Team | Attack implementation for security and correctness |
| 2 | S-004 Pre-Mortem | Identify failure modes before deployment |
| 3 | S-014 LLM-as-Judge | Score implementation quality, documentation, testability |

#### EN-306 (Integration Testing - Pipeline A)
| Iteration | Adversarial Strategy | Rationale |
|-----------|---------------------|-----------|
| 1 | S-012 FMEA | Identify failure modes in test coverage |
| 2 | S-001 Red Team | Attack test assumptions and edge cases |
| 3 | S-014 LLM-as-Judge | Score test suite completeness and rigor |

#### EN-402 (Enforcement Priority Analysis)
| Iteration | Adversarial Strategy | Rationale |
|-----------|---------------------|-----------|
| 1 | S-002 Devil's Advocate | Challenge priority criteria and assumptions |
| 2 | S-012 FMEA | Identify enforcement failure modes |
| 3 | S-014 LLM-as-Judge | Score analysis rigor and ADR quality |

#### EN-403, EN-404, EN-405 (Enforcement Implementations)
| Iteration | Adversarial Strategy | Rationale |
|-----------|---------------------|-----------|
| 1 | S-001 Red Team | Attack implementation for circumvention and edge cases |
| 2 | S-012 FMEA | Failure mode analysis for enforcement mechanisms |
| 3 | S-014 LLM-as-Judge | Score implementation correctness, portability, robustness |

#### EN-406 (Integration Testing - Pipeline B)
| Iteration | Adversarial Strategy | Rationale |
|-----------|---------------------|-----------|
| 1 | S-012 FMEA | Failure mode coverage in test plan |
| 2 | S-001 Red Team | Attack test suite for gaps and false positives |
| 3 | S-014 LLM-as-Judge | Score test coverage, cross-platform validation, reporting |

### 4.3 Scoring Rubric (S-014 LLM-as-Judge)

All artifacts scored on 1-10 scale across dimensions:

| Dimension | Weight | Description |
|-----------|--------|-------------|
| **Completeness** | 30% | All requirements addressed, no missing elements |
| **Rigor** | 25% | Evidence-based reasoning, justified decisions |
| **Clarity** | 20% | Clear documentation, reproducible processes |
| **Robustness** | 15% | Edge cases considered, failure modes addressed |
| **Maintainability** | 10% | Sustainable implementation, clear rationale for future changes |

**Composite Score:** (Completeness × 0.30) + (Rigor × 0.25) + (Clarity × 0.20) + (Robustness × 0.15) + (Maintainability × 0.10)

**Pass Threshold:** >= 9.2 / 10 (equivalent to 0.92)

---

## 5. Sync Barrier Protocol

### 5.1 Barrier Transition Rules

```
PRE-BARRIER CHECK (Both pipelines must satisfy):
  □ All phase agents have completed execution
  □ All phase artifacts exist and pass validation (>= 0.92 quality score)
  □ All adversarial feedback loops completed (minimum 3 iterations)
  □ No blocking errors or unresolved issues
  □ Agent status = COMPLETE for all phase agents

CROSS-POLLINATION EXECUTION:
  □ Extract key findings from source pipeline
  □ Transform into cross-pollination artifact
  □ Validate artifact schema and content
  □ Store in cross-pollination/{barrier-id}/{direction}/ directory

POST-BARRIER VERIFICATION:
  □ Target pipeline acknowledges receipt
  □ Inputs incorporated into next phase context
  □ Barrier status updated to COMPLETE
  □ Both pipelines unblocked for next phase
```

### 5.2 Barrier Definitions

#### Barrier 1: Selection/Prioritization Complete

**Triggered After:** Phase 1 complete in both pipelines
**Status:** PENDING

**Cross-Pollination Artifacts:**

| Direction | Artifact | Content |
|-----------|----------|---------|
| adv → enf | `barrier-1-adv-to-enf-handoff.md` | 10 selected adversarial strategies with: selection rationale, use case descriptions, integration requirements, expected enforcement touchpoints |
| enf → adv | `barrier-1-enf-to-adv-handoff.md` | Priority matrix results with: top 3 enforcement vectors, platform constraints, implementation capabilities, limitations that constrain strategy feasibility |

**Why Cross-Pollinate:**
- Enforcement knows which adversarial strategies to support (informs implementation design)
- Strategy selection knows enforcement capabilities and constraints (informs feasibility assessment)

#### Barrier 2: Mapping/Implementation Complete

**Triggered After:** Phase 2 complete in both pipelines
**Status:** BLOCKED (barrier-1)

**Cross-Pollination Artifacts:**

| Direction | Artifact | Content |
|-----------|----------|---------|
| adv → enf | `barrier-2-adv-to-enf-handoff.md` | Situational context mappings with: context taxonomy, per-strategy triggers, decision tree for strategy selection, situational examples |
| enf → adv | `barrier-2-enf-to-adv-handoff.md` | Enforcement patterns with: hook invocation points, rule enforcement patterns, session context requirements, integration examples |

**Why Cross-Pollinate:**
- Enforcement implementations align with situational triggers (enables context-aware enforcement)
- Strategy situational mapping accounts for enforcement mechanisms (ensures practical applicability)

#### Final Barrier: Integration Complete

**Triggered After:** Phase 4 complete in both pipelines
**Status:** BLOCKED (phase-4)

**Final Synthesis Artifacts:**

| Artifact | Content |
|----------|---------|
| `epic002-final-synthesis.md` | Comprehensive summary of EPIC-002 outcomes: strategies selected, enforcement implemented, integration validated, lessons learned |
| `epic002-integration-report.md` | Combined test results: skill enhancement tests, enforcement tests, cross-platform validation, performance benchmarks |
| `epic002-lessons-learned.md` | Process insights: adversarial feedback effectiveness, cross-pollination value, challenges encountered, recommendations for future orchestrations |

---

## 6. Agent Registry

### 6.1 Phase 1 Agents (Both Pipelines)

| Agent ID | Pipeline | Skill | Role | Input Artifacts | Output Artifacts | Status |
|----------|----------|-------|------|-----------------|------------------|--------|
| ps-analyst-302 | adv | problem-solving | Creator (criteria, scoring, revision) | EN-301 catalog | Evaluation framework, scoring matrix, revision docs | PENDING |
| nse-risk-302 | adv | nasa-se | Risk assessor | EN-301 catalog | Risk assessment per strategy | PENDING |
| nse-architecture-302 | adv | nasa-se | Trade study | EN-301 catalog | Architecture trade study | PENDING |
| ps-architect-302 | adv | problem-solving | ADR author | Scoring matrix, risk, trade study | Selection ADR | PENDING |
| ps-critic-302 | adv | problem-solving | Adversarial reviewer | All phase 1 artifacts | Critique reports (3 iterations) | PENDING |
| ps-validator-302 | adv | problem-solving | Validator | Final artifacts + critiques | Validation report | PENDING |
| ps-analyst-402 | enf | problem-solving | Creator (criteria, priority, revision) | EN-401 catalog | Evaluation framework, priority matrix, revision docs | PENDING |
| nse-risk-402 | enf | nasa-se | Risk assessor | EN-401 catalog | Vector risk assessment | PENDING |
| nse-architecture-402 | enf | nasa-se | Trade study | EN-401 catalog | Vector trade study | PENDING |
| ps-architect-402 | enf | problem-solving | ADR/plan author | Priority matrix, risk, trade study | Enforcement ADR, execution plans | PENDING |
| ps-critic-402 | enf | problem-solving | Adversarial reviewer | All phase 1 artifacts | Critique reports (3 iterations) | PENDING |
| ps-validator-402 | enf | problem-solving | Validator | Final artifacts + critiques | Validation report | PENDING |

### 6.2 Phase 2 Agents

| Agent ID | Pipeline | Skill | Role | Input Artifacts | Output Artifacts | Status |
|----------|----------|-------|------|-----------------|------------------|--------|
| ps-analyst-303 | adv | problem-solving | Creator (taxonomy, mapping) | Selected 10 strategies, barrier-1 enf→adv handoff | Context taxonomy, situational mappings | BLOCKED |
| ps-architect-303 | adv | problem-solving | Decision tree author | Situational mappings | Decision tree | BLOCKED |
| ps-critic-303 | adv | problem-solving | Adversarial reviewer | All phase 2 artifacts | Critique reports (3 iterations) | BLOCKED |
| ps-validator-303 | adv | problem-solving | Validator | Final artifacts + critiques | Validation report | BLOCKED |
| ps-architect-403 | enf | problem-solving | Requirements/design | Priority matrix, barrier-1 adv→enf handoff | Hook requirements, hook designs | BLOCKED |
| ps-implementer-403 | enf | problem-solving | Implementation | Hook designs | Hook implementations | BLOCKED |
| ps-architect-404 | enf | problem-solving | Requirements/design | Priority matrix | Rule requirements, HARD language spec | BLOCKED |
| ps-implementer-404 | enf | problem-solving | Implementation | Rule designs | Rule implementations | BLOCKED |
| ps-critic-403-404 | enf | problem-solving | Adversarial reviewer | All EN-403, EN-404 artifacts | Critique reports (3 iterations) | BLOCKED |
| ps-validator-403-404 | enf | problem-solving | Verifier | Implementations + critiques | Verification report | BLOCKED |

### 6.3 Phase 3 Agents

| Agent ID | Pipeline | Skill | Role | Input Artifacts | Output Artifacts | Status |
|----------|----------|-------|------|-----------------|------------------|--------|
| ps-architect-304 | adv | problem-solving | Requirements/design | Situational mappings, barrier-2 enf→adv handoff | PS skill requirements, adversarial mode design | BLOCKED |
| ps-implementer-304 | adv | problem-solving | Implementation | PS requirements | Adversarial invocation protocol, implementation | BLOCKED |
| ps-architect-305 | adv | problem-solving | Requirements/design | Situational mappings | NSE skill requirements, agent designs | BLOCKED |
| ps-implementer-305 | adv | problem-solving | Implementation | NSE requirements | NSE agent enhancements | BLOCKED |
| ps-architect-307 | adv | problem-solving | Requirements/design | Situational mappings | ORCH skill requirements, planner/gate designs | BLOCKED |
| ps-implementer-307 | adv | problem-solving | Implementation | ORCH requirements | ORCH skill enhancements | BLOCKED |
| ps-critic-304-305-307 | adv | problem-solving | Adversarial reviewer | All skill enhancement artifacts | Critique reports (3 iterations) | BLOCKED |
| ps-validator-304-305-307 | adv | problem-solving | Validator | Implementations + critiques | Validation report | BLOCKED |
| ps-architect-405 | enf | problem-solving | Requirements/design | Enforcement patterns, barrier-2 adv→enf handoff | Session preamble requirements, hook design | BLOCKED |
| ps-implementer-405 | enf | problem-solving | Implementation | Session requirements | Preamble implementation, hook integration | BLOCKED |
| ps-critic-405 | enf | problem-solving | Adversarial reviewer | All EN-405 artifacts | Critique reports (3 iterations) | BLOCKED |
| ps-validator-405 | enf | problem-solving | Validator | Implementation + critiques | Testing suite, validation report | BLOCKED |

### 6.4 Phase 4 Agents

| Agent ID | Pipeline | Skill | Role | Input Artifacts | Output Artifacts | Status |
|----------|----------|-------|------|-----------------|------------------|--------|
| ps-validator-306 | adv | problem-solving | Test plan/execution | All skill enhancements | Test plan, test results (PS/NSE/ORCH) | BLOCKED |
| ps-critic-306 | adv | problem-solving | QA auditor | Test results | QA audit report | BLOCKED |
| ps-validator-406 | enf | problem-solving | Test plan/execution | All enforcement implementations | Test plan, test results (hooks/rules/session) | BLOCKED |
| ps-critic-406 | enf | problem-solving | QA auditor | Test results, performance tests | QA audit report | BLOCKED |

---

## 7. State Management

### 7.1 State Files

| File | Purpose |
|------|---------|
| `ORCHESTRATION.yaml` | Machine-readable state (SSOT) |
| `ORCHESTRATION_WORKTRACKER.md` | Tactical execution documentation |
| `ORCHESTRATION_PLAN.md` | This file - strategic context |

### 7.2 Artifact Path Structure (WI-SAO-021)

All artifacts are stored under the workflow's base path using dynamic identifiers:

```
orchestration/epic002-crosspoll-20260213-001/
├── adv/                                    # Pipeline A (Adversarial Strategies)
│   ├── phase-1-selection/
│   │   ├── ps-analyst-302/
│   │   │   ├── evaluation-framework.md
│   │   │   ├── scoring-matrix.md
│   │   │   └── revision-log.md
│   │   ├── nse-risk-302/
│   │   │   └── risk-assessment.md
│   │   ├── nse-architecture-302/
│   │   │   └── trade-study.md
│   │   ├── ps-architect-302/
│   │   │   └── ADR-strategy-selection.md
│   │   ├── ps-critic-302/
│   │   │   ├── critique-iteration-1.md
│   │   │   ├── critique-iteration-2.md
│   │   │   └── critique-iteration-3.md
│   │   └── ps-validator-302/
│   │       └── validation-report.md
│   ├── phase-2-mapping/
│   │   └── (similar structure for EN-303)
│   ├── phase-3-skills/
│   │   └── (similar structure for EN-304, EN-305, EN-307)
│   └── phase-4-testing/
│       └── (similar structure for EN-306)
├── enf/                                    # Pipeline B (Enforcement Mechanisms)
│   ├── phase-1-priority/
│   │   └── (similar structure for EN-402)
│   ├── phase-2-implementation/
│   │   └── (similar structure for EN-403, EN-404)
│   ├── phase-3-session/
│   │   └── (similar structure for EN-405)
│   └── phase-4-testing/
│       └── (similar structure for EN-406)
└── cross-pollination/
    ├── barrier-1/
    │   ├── adv-to-enf/
    │   │   └── barrier-1-adv-to-enf-handoff.md
    │   └── enf-to-adv/
    │       └── barrier-1-enf-to-adv-handoff.md
    ├── barrier-2/
    │   ├── adv-to-enf/
    │   │   └── barrier-2-adv-to-enf-handoff.md
    │   └── enf-to-adv/
    │       └── barrier-2-enf-to-adv-handoff.md
    └── final-synthesis/
        ├── epic002-final-synthesis.md
        ├── epic002-integration-report.md
        └── epic002-lessons-learned.md
```

**Pipeline Alias Resolution:**
1. Workflow YAML override (highest priority)
2. Skill registration default
3. Auto-derived from skill name (fallback)

### 7.3 Checkpoint Strategy

| Trigger | When | Purpose |
|---------|------|---------|
| PHASE_COMPLETE | After each phase in each pipeline | Phase-level rollback |
| BARRIER_COMPLETE | After each sync barrier | Cross-pollination recovery |
| ADVERSARIAL_ITERATION | After each critic→revision cycle | Granular progress tracking |
| MANUAL | User-triggered | Debug and inspection |

**Checkpoint Naming:** `CP-{PIPELINE}-P{PHASE}-{TIMESTAMP}`
- Example: `CP-adv-P1-20260213T1430Z`

---

## 8. Execution Constraints

### 8.1 Hard Constraints (Jerry Constitution)

| Constraint | ID | Enforcement |
|------------|----|----|
| Single agent nesting | P-003 | Orchestrator → Worker only (no recursive subagents) |
| File persistence | P-002 | All state to filesystem, no ephemeral memory |
| No deception | P-022 | Transparent reasoning in all artifacts |
| User authority | P-020 | User approves quality gates and phase transitions |
| Adversarial validation | P-043 | Minimum 3 creator→critic→revision iterations per enabler |

### 8.2 Soft Constraints

| Constraint | Value | Rationale |
|------------|-------|-----------|
| Max concurrent agents | 6 | Resource management (2 per pipeline max) |
| Max barrier retries | 2 | Circuit breaker for cross-pollination failures |
| Checkpoint frequency | PHASE | Recovery granularity balances overhead vs. precision |
| Quality gate threshold | 0.92 | Jerry standard for production artifacts |
| Adversarial iteration min | 3 | Evidence-based minimum for quality improvement |

---

## 9. Success Criteria

### 9.1 Phase Exit Criteria

#### Phase 1 (Both Pipelines)

| Criterion | Validation |
|-----------|------------|
| Selection/prioritization framework complete | Framework documented with weighted criteria |
| Risk assessment complete | All strategies/vectors assessed with FMEA-style analysis |
| Trade study complete | Architecture analysis complete with justified recommendations |
| ADR created | Formal decision record stored in decisions/ directory |
| Quality score >= 0.92 | LLM-as-Judge scoring confirms threshold |
| Adversarial feedback (3+ iterations) | ps-critic reports show 3+ distinct adversarial strategies applied |

#### Phase 2 (Both Pipelines)

| Criterion | Validation |
|-----------|------------|
| Mapping/implementation complete | adv: Situational mappings for all 10 strategies; enf: Hook and rule implementations |
| Decision tree/patterns created | adv: Decision tree for strategy selection; enf: Enforcement patterns documented |
| Cross-pollination received | Both pipelines acknowledge barrier-2 handoff artifacts |
| Quality score >= 0.92 | LLM-as-Judge scoring confirms threshold |
| Adversarial feedback (3+ iterations) | ps-critic reports show 3+ distinct adversarial strategies applied |

#### Phase 3 (Both Pipelines)

| Criterion | Validation |
|-----------|------------|
| Skill enhancements complete | adv: PS, NSE, ORCH skills enhanced with adversarial modes; enf: Session context implemented |
| Documentation updated | All README, SKILL.md, and integration guides updated |
| Implementation tested | Unit tests pass for all new code |
| Quality score >= 0.92 | LLM-as-Judge scoring confirms threshold |
| Adversarial feedback (3+ iterations) | ps-critic reports show 3+ distinct adversarial strategies applied |

#### Phase 4 (Both Pipelines)

| Criterion | Validation |
|-----------|------------|
| Integration tests pass | All test suites pass (100% pass rate) |
| Cross-platform validated | Tests pass on macOS, Linux, Windows |
| QA audit complete | ps-critic QA audit report produced with no critical findings |
| Quality score >= 0.92 | LLM-as-Judge scoring confirms threshold |

### 9.2 Workflow Completion Criteria

| Criterion | Validation |
|-----------|------------|
| All phases complete | All phase status = COMPLETE in ORCHESTRATION.yaml |
| All barriers synced | All barrier status = COMPLETE in ORCHESTRATION.yaml |
| Final synthesis created | epic002-final-synthesis.md exists and passes review |
| Integration report created | epic002-integration-report.md consolidates all test results |
| Lessons learned captured | epic002-lessons-learned.md documents process insights |
| Overall quality >= 0.92 | Final synthesis scores >= 0.92 on composite rubric |

---

## 10. Risk Mitigations

| Risk ID | Risk | Likelihood | Impact | Mitigation |
|---------|------|------------|--------|------------|
| R-001 | Adversarial feedback degrades quality instead of improving | Medium | High | Use diverse strategies (Steelman, Devil's Advocate, Red Team) to balance strengthening and challenging. Monitor scores across iterations. |
| R-002 | Cross-pollination artifacts misaligned or incomplete | Medium | High | Define explicit schema for handoff artifacts. ps-validator checks barrier artifacts before transition. |
| R-003 | Quality gate threshold too high, causing delays | Medium | Medium | Allow 1-2 focused revisions if score >= 0.88 but < 0.92. Document exception rationale. |
| R-004 | Agent count exceeds concurrency limit | Low | Low | Soft limit of 6 concurrent. Serialize within phases if needed. |
| R-005 | Barrier synchronization deadlock | Low | High | Timeout mechanism: if barrier pending > 48h, escalate to user for manual resolution. |
| R-006 | Skill enhancement breaks existing functionality | Medium | High | Require backward compatibility tests in EN-306/EN-406. Regression test suite mandatory. |
| R-007 | Enforcement implementations not portable across platforms | Medium | High | Cross-platform testing required in EN-406. Use platform-agnostic patterns (no fcntl, use filelock, etc.). |
| R-008 | LLM-as-Judge scoring inconsistent | Medium | Medium | Use structured rubric with explicit criteria. Multiple judge passes for critical artifacts. Calibrate with human review samples. |
| R-009 | Workflow abandoned mid-execution | Low | Medium | Checkpoint at every phase. ORCHESTRATION.yaml resumption context enables restart. |

---

## 11. Resumption Context

### 11.1 Current Execution State

```
WORKFLOW STATUS AS OF 2026-02-13
==================================

Pipeline A (adv): Adversarial Strategy Research
  Phase 1 (EN-302): PENDING
  Phase 2 (EN-303): BLOCKED (barrier-1)
  Phase 3 (EN-304, EN-305, EN-307): BLOCKED (barrier-2)
  Phase 4 (EN-306): BLOCKED (phase-3)

Pipeline B (enf): Enforcement Mechanisms
  Phase 1 (EN-402): PENDING
  Phase 2 (EN-403, EN-404): BLOCKED (barrier-1)
  Phase 3 (EN-405): BLOCKED (barrier-2)
  Phase 4 (EN-406): BLOCKED (phase-3)

Barriers:
  Barrier 1 (Selection/Priority): PENDING
  Barrier 2 (Mapping/Implementation): BLOCKED (barrier-1)
  Final Barrier (Synthesis): BLOCKED (phase-4)
```

### 11.2 Next Actions

#### Immediate (Group 1)

1. **Execute Phase 1 Agents in Parallel:**
   - Pipeline A (adv): ps-analyst-302, nse-risk-302, nse-architecture-302, ps-architect-302
   - Pipeline B (enf): ps-analyst-402, nse-risk-402, nse-architecture-402, ps-architect-402

2. **Adversarial Feedback Loops:**
   - ps-critic-302 (adv) applies S-002, S-005, S-014 across 3 iterations
   - ps-critic-402 (enf) applies S-002, S-012, S-014 across 3 iterations

3. **Validation:**
   - ps-validator-302 (adv) validates EN-302 outputs
   - ps-validator-402 (enf) validates EN-402 outputs

#### Subsequent (After Group 1)

4. **Execute Barrier 1 Cross-Pollination:**
   - Create barrier-1-adv-to-enf-handoff.md (10 selected strategies)
   - Create barrier-1-enf-to-adv-handoff.md (enforcement constraints)
   - Validate handoff artifacts

5. **Unblock Phase 2 and Execute:**
   - Pipeline A: EN-303 agents (ps-analyst-303, ps-architect-303, ps-critic-303, ps-validator-303)
   - Pipeline B: EN-403, EN-404 agents (ps-architect-403/404, ps-implementer-403/404, ps-critic-403-404, ps-validator-403-404)

---

## 12. Constitutional Compliance Disclaimer (P-043)

> **CRITICAL:** This orchestration plan is a PROPOSAL for coordinated multi-agent execution. The orch-planner agent created this plan, but the orch-planner MUST NOT execute the work itself.
>
> **P-003 Compliance:** All work MUST be delegated to worker agents. No recursive orchestrator-to-orchestrator delegation is permitted. The execution model is:
>
> ```
> User → orch-tracker (reads plan) → Delegates to worker agents → Workers execute and report
> ```
>
> **User Authority (P-020):** Execution of this plan requires user approval. The user may:
> - Approve the plan as-is
> - Request modifications before execution
> - Reject the plan
>
> **Transparency (P-022):** This plan documents the proposed workflow. Any deviations during execution MUST be documented in ORCHESTRATION_WORKTRACKER.md with rationale.

---

*Document ID: PROJ-001-ORCH-PLAN*
*Workflow ID: epic002-crosspoll-20260213-001*
*Version: 2.0*
*Cross-Session Portable: All paths are repository-relative*
