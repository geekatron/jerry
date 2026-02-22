# ORCHESTRATION_PLAN.md

> **Document ID:** PROJ-010-ORCH-PLAN
> **Project:** PROJ-010
> **Workflow ID:** `cyber-ops-20260222-001`
> **Status:** ACTIVE
> **Version:** 2.0
> **Criticality:** C4 (Mission Critical)
> **Quality Threshold:** >= 0.95
> **Created:** 2026-02-22
> **Last Updated:** 2026-02-22

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [1. Executive Summary](#1-executive-summary) | Workflow purpose, current state, pattern classification |
| [2. Workflow Architecture](#2-workflow-architecture) | Pipeline diagram, pattern classification, artifact locations |
| [3. Phase Definitions](#3-phase-definitions) | All 6 phases with agents, tasks, and execution groups |
| [4. Sync Barrier Protocol](#4-sync-barrier-protocol) | 6 barriers with transition rules and artifact flows |
| [5. Quality Gates](#5-quality-gates) | C4 tournament gates between all phases |
| [6. Agent Registry](#6-agent-registry) | All agents with phase assignments |
| [7. State Management](#7-state-management) | State files, artifact paths, checkpoint strategy |
| [8. Execution Constraints](#8-execution-constraints) | Hard and soft constraints |
| [9. Success Criteria](#9-success-criteria) | Phase exit criteria and workflow completion |
| [10. Risk Mitigations](#10-risk-mitigations) | Identified risks and mitigations |
| [11. Resumption Context](#11-resumption-context) | Current state and next actions |

---

## 1. Executive Summary

Build two elite Jerry skills -- `/eng-team` (secure-by-design software engineering) and `/red-team` (offensive security operations) -- through a 6-phase orchestrated workflow with C4 quality enforcement at every gate. The two skills operate as adversaries: `/eng-team` builds, `/red-team` breaks, and the gap between them drives hardening.

This workflow produces 2 fully operational skills, 17 agent definitions, 6 architecture decision records, and a purple team validation demonstrating adversarial resilience. All 24 requirements (R-001 through R-024) are fulfilled through evidence-driven research, architecturally pure design, and mission-critical quality enforcement.

**Current State:** Phase 1 not yet started. Orchestration plan complete. Ready for execution.

**Orchestration Pattern:** Divergent-Convergent with Cross-Pollination

### 1.1 Workflow Identification

| Field | Value | Source |
|-------|-------|--------|
| Workflow ID | `cyber-ops-20260222-001` | user |
| ID Format | `{purpose}-{YYYYMMDD}-{NNN}` | semantic-date-seq |
| Base Path | `orchestration/cyber-ops-20260222-001/` | Dynamic |

**Artifact Output Locations:**
- Pipeline A (research): `orchestration/cyber-ops-20260222-001/research/`
- Pipeline B (eng-team): `orchestration/cyber-ops-20260222-001/eng-team/`
- Pipeline C (red-team): `orchestration/cyber-ops-20260222-001/red-team/`
- Pipeline D (validation): `orchestration/cyber-ops-20260222-001/validation/`
- Cross-pollination: `orchestration/cyber-ops-20260222-001/cross-pollination/`

---

## 2. Workflow Architecture

### 2.1 Pipeline Diagram

```
    PIPELINE A (research) -- Shared Foundation
    ============================================

┌──────────────────────────────────────────────────────────────────┐
│ PHASE 1: Research & Analysis                                     │
│ ──────────────────────────────────────────────────────────────── │
│                                                                  │
│  Group 1 (15 tasks parallel):                                    │
│  • A-001, A-002, A-003      (Role Completeness)                  │
│  • B-001, B-002, B-003, B-004 (Methodology)                     │
│  • C-001, C-002, C-003      (Tool Integration)                   │
│  • D-001, D-002, D-003      (Prior Art)                          │
│  • E-001, E-002             (LLM Portability)                    │
│                                                                  │
│  Group 2 (2 tasks, depends on Group 1):                          │
│  • A-004                    (Role Gap Synthesis)                  │
│  • E-003                    (Portability Synthesis)               │
│                                                                  │
│  ╔═══════════════════════════════════════════════════════════╗    │
│  ║ BARRIER 1: C4 /adversary on all stream outputs >= 0.95  ║    │
│  ╚═══════════════════════════════════════════════════════════╝    │
│                                                                  │
│  Group 3 (3 tasks parallel):                                     │
│  • F-001, F-002, F-003      (Secure SDLC)                       │
│                                                                  │
│  Group 4 (3 tasks sequential):                                   │
│  • S-001 → S-002 → S-003   (Synthesis)                          │
│                                                                  │
│  ╔═══════════════════════════════════════════════════════════╗    │
│  ║ BARRIER 2: C4 /adversary on research compendium >= 0.95 ║    │
│  ╚═══════════════════════════════════════════════════════════╝    │
│                                                                  │
│  Agents: ps-researcher, ps-synthesizer, ps-architect,            │
│          nse-explorer, orch-planner, orch-tracker                │
│  STATUS: PENDING                                                 │
└──────────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌──────────────────────────────────────────────────────────────────┐
│ PHASE 2: Architecture & Design                                   │
│ ──────────────────────────────────────────────────────────────── │
│  6 ADRs (sequential, each with C4 review):                       │
│  • ADR-001: Agent Team Architecture                              │
│  • ADR-002: Skill Routing                                        │
│  • ADR-003: LLM Portability                                      │
│  • ADR-004: Configurable Rule Sets                               │
│  • ADR-005: Tool Adapters                                        │
│  • ADR-006: Authorization Architecture                           │
│                                                                  │
│  Agents: ps-architect, nse-architecture, nse-requirements,       │
│          ps-researcher, ps-critic                                │
│  STATUS: PENDING                                                 │
└──────────────────────────────────────────────────────────────────┘
                               │
    ╔══════════════════════════════════════════════════════════════╗
    ║ BARRIER 3: Architecture approved before parallel build       ║
    ║ All 6 ADRs pass C4 /adversary >= 0.95                       ║
    ╚══════════════════════════════════════════════════════════════╝
                               │
              ┌────────────────┴────────────────┐
              ▼                                 ▼

    PIPELINE B (eng-team)              PIPELINE C (red-team)
    =====================              =====================

┌─────────────────────────┐   ┌─────────────────────────┐
│ PHASE 3: /eng-team Build│   │ PHASE 4: /red-team Build│
│ ─────────────────────── │   │ ─────────────────────── │
│ FEAT-020 through        │   │ FEAT-030 through        │
│ FEAT-025                │   │ FEAT-037                 │
│                         │   │                         │
│ Agents:                 │   │ Agents:                 │
│ • ps-architect (design) │   │ • ps-architect (design) │
│ • ps-reviewer (review)  │   │ • ps-reviewer (review)  │
│ • ps-critic (quality)   │   │ • ps-critic (quality)   │
│ • adv-executor (C4)     │   │ • adv-executor (C4)     │
│ STATUS: PENDING         │   │ STATUS: PENDING         │
└────────────┬────────────┘   └────────────┬────────────┘
             │                             │
    ╔════════╧═════════════════════════════╧═════════════╗
    ║ BARRIER 4: Both skills complete before validation  ║
    ║ Phase 3 + Phase 4 pass C4 /adversary >= 0.95      ║
    ╚════════════════════════════════════════════════════╝
                               │
                               ▼

    PIPELINE D (validation)
    =======================

┌──────────────────────────────────────────────────────────────────┐
│ PHASE 5: Purple Team Validation                                  │
│ ──────────────────────────────────────────────────────────────── │
│  /red-team attacks /eng-team outputs                             │
│  FEAT-040 through FEAT-044                                       │
│                                                                  │
│  Agents: ps-investigator, ps-validator,                          │
│          ps-synthesizer, adv-scorer                              │
│  STATUS: PENDING                                                 │
└──────────────────────────────────────────────────────────────────┘
                               │
    ╔══════════════════════════════════════════════════════════════╗
    ║ BARRIER 5: Validation passes before documentation           ║
    ║ Phase 5 passes C4 /adversary >= 0.95                        ║
    ╚══════════════════════════════════════════════════════════════╝
                               │
                               ▼
┌──────────────────────────────────────────────────────────────────┐
│ PHASE 6: Documentation & Registration                            │
│ ──────────────────────────────────────────────────────────────── │
│  FEAT-050 through FEAT-054                                       │
│                                                                  │
│  Agents: ps-reporter, ps-reviewer, adv-scorer                   │
│  STATUS: PENDING                                                 │
└──────────────────────────────────────────────────────────────────┘
                               │
    ╔══════════════════════════════════════════════════════════════╗
    ║ BARRIER 6: Final quality gate                                ║
    ║ Phase 6 passes C4 /adversary >= 0.95                        ║
    ╚══════════════════════════════════════════════════════════════╝
                               │
                               ▼
                           COMPLETE
```

### 2.2 Orchestration Pattern Classification

| Pattern | Applied | Description |
|---------|---------|-------------|
| Sequential | Yes | Phases 1 -> 2 (shared foundation), Phase 5 -> 6 (validation to docs) |
| Concurrent | Yes | Phase 3 (eng-team) and Phase 4 (red-team) run in parallel |
| Barrier Sync | Yes | 6 sync barriers enforce phase gate transitions |
| Hierarchical | Yes | Orchestrator delegates to skill-specific agent teams |
| Fan-Out / Fan-In | Yes | Phase 1 fans out to 6 research streams, fans in through synthesis |
| Cross-Pollination | Yes | Phase 5 converges eng-team and red-team outputs via purple team |
| Divergent-Convergent | Yes | Phases 3/4 diverge from shared foundation, converge at Phase 5 |

### 2.3 Pipeline Definitions

| Pipeline | ID | Phases | Purpose |
|----------|----|--------|---------|
| Pipeline A | research | 1, 2 | Shared research and architecture foundation |
| Pipeline B | eng-team | 3 | Engineering team skill build |
| Pipeline C | red-team | 4 | Red team skill build |
| Pipeline D | validation | 5, 6 | Purple team validation and documentation |

---

## 3. Phase Definitions

### 3.1 Phase 1: Research & Analysis

| Field | Value |
|-------|-------|
| Pipeline | A (research) |
| Purpose | Comprehensive research across 6 streams plus synthesis |
| Primary Agents | ps-researcher, ps-synthesizer, ps-architect, nse-explorer |
| Support Agents | orch-planner (plan), orch-tracker (state) |
| Status | PENDING |
| Quality Gate | C4 /adversary >= 0.95 (2 internal barriers) |

#### Research Streams

| Stream | ID | Focus |
|--------|----|-------|
| A | Role Completeness | Agent roster validation for both skills against industry team structures |
| B | Methodology | Offensive/defensive methodology standards (MITRE ATT&CK, PTES, OSSTMM, OWASP) |
| C | Tool Integration | External tooling landscape, adapter patterns, integration architecture |
| D | Prior Art | Existing agentic security tools, LLM-based security research, competitive analysis |
| E | LLM Portability | Cross-provider agent patterns, universal prompt engineering, portability testing |
| F | Secure SDLC | NIST, CIS, SANS secure development lifecycle mapping |

#### Execution Groups

**Group 1 -- Parallel Research (15 tasks):**

| Task | Stream | Description |
|------|--------|-------------|
| A-001 | A | /eng-team role completeness -- industry engineering team structures |
| A-002 | A | /red-team role completeness -- offensive security team structures |
| A-003 | A | Gap analysis -- missing roles against industry benchmarks |
| B-001 | B | MITRE ATT&CK mapping for /red-team methodology |
| B-002 | B | PTES/OSSTMM framework analysis for engagement methodology |
| B-003 | B | OWASP integration points for /eng-team secure development |
| B-004 | B | Defensive methodology synthesis (NIST CSF, CIS Controls) |
| C-001 | C | Offensive tool landscape (Metasploit, Burp, Nmap, etc.) |
| C-002 | C | Defensive/SAST/DAST tool landscape |
| C-003 | C | Adapter pattern research for pluggable tool integration |
| D-001 | D | Existing agentic security tools survey |
| D-002 | D | LLM-based security research state of art |
| D-003 | D | Competitive analysis of AI security tooling |
| E-001 | E | Cross-provider prompt engineering patterns |
| E-002 | E | Provider-specific feature dependency audit |

**Group 2 -- Dependent Synthesis (2 tasks, requires Group 1):**

| Task | Stream | Description | Depends On |
|------|--------|-------------|------------|
| A-004 | A | Role gap synthesis -- final roster recommendations | A-001, A-002, A-003 |
| E-003 | E | Portability validation strategy | E-001, E-002 |

**Barrier 1:** C4 /adversary review on all stream A-E outputs. Threshold >= 0.95. All 10 strategies (C4 tournament). Max 5 iterations.

**Group 3 -- Secure SDLC Research (3 tasks parallel, after Barrier 1):**

| Task | Stream | Description |
|------|--------|-------------|
| F-001 | F | NIST secure SDLC mapping for /eng-team workflow |
| F-002 | F | CIS/SANS coding standards integration points |
| F-003 | F | Secure SDLC verification and compliance patterns |

**Group 4 -- Final Synthesis (3 tasks sequential):**

| Task | Stream | Description | Depends On |
|------|--------|-------------|------------|
| S-001 | Synthesis | Cross-stream findings consolidation | All research streams |
| S-002 | Synthesis | Research compendium assembly | S-001 |
| S-003 | Synthesis | Architecture input preparation | S-002 |

**Barrier 2:** C4 /adversary review on research compendium. Threshold >= 0.95. All 10 strategies (C4 tournament). Max 5 iterations.

### 3.2 Phase 2: Architecture & Design

| Field | Value |
|-------|-------|
| Pipeline | A (research) |
| Purpose | 6 Architecture Decision Records based on Phase 1 research |
| Primary Agents | ps-architect, nse-architecture, nse-requirements |
| Support Agents | ps-researcher (follow-up), ps-critic (review) |
| Status | PENDING |
| Quality Gate | C4 /adversary on each ADR >= 0.95 |

#### Architecture Decision Records

| ADR | Title | Scope | Key Inputs |
|-----|-------|-------|------------|
| ADR-001 | Agent Team Architecture | Agent roster, team structure, interaction patterns | Stream A research, Stream D prior art |
| ADR-002 | Skill Routing | Skill invocation, agent routing, workflow orchestration | Stream B methodology, existing routing-standards |
| ADR-003 | LLM Portability | Cross-provider agent design, universal prompting | Stream E portability research |
| ADR-004 | Configurable Rule Sets | User-provided rule overrides, standards customization | Stream B methodology, Stream F secure SDLC |
| ADR-005 | Tool Adapters | Pluggable adapter architecture for external tools | Stream C tool integration research |
| ADR-006 | Authorization Architecture | Scope verification, rules of engagement, out-of-scope protection | Stream B methodology, R-020 authorization |

Each ADR follows the sequential workflow: ps-architect drafts -> ps-critic reviews -> ps-architect revises -> C4 /adversary tournament scoring. Max 5 iterations per ADR.

### 3.3 Phase 3: /eng-team Build

| Field | Value |
|-------|-------|
| Pipeline | B (eng-team) |
| Purpose | Build the engineering team skill |
| Primary Agents | ps-architect (design), ps-reviewer (review) |
| Support Agents | ps-critic (quality), adv-executor (C4) |
| Status | PENDING |
| Quality Gate | C4 /adversary >= 0.95 |

#### Features

| Feature | Title | Description |
|---------|-------|-------------|
| FEAT-020 | /eng-team SKILL.md | Skill definition, routing, triggers, description |
| FEAT-021 | /eng-team Agent Definitions | 8 agent definitions (eng-architect through eng-reviewer) |
| FEAT-022 | /eng-team Templates | Workflow templates, output templates, review checklists |
| FEAT-023 | /eng-team /adversary Integration | C4 quality enforcement wiring for all deliverables |
| FEAT-024 | /eng-team Configurable Rules | User-overridable rule set architecture |
| FEAT-025 | /eng-team Tool Adapters | Pluggable adapter stubs for SAST/DAST/IaC tools |

### 3.4 Phase 4: /red-team Build

| Field | Value |
|-------|-------|
| Pipeline | C (red-team) |
| Purpose | Build the red team skill |
| Primary Agents | ps-architect (design), ps-reviewer (review) |
| Support Agents | ps-critic (quality), adv-executor (C4) |
| Status | PENDING |
| Quality Gate | C4 /adversary >= 0.95 |

#### Features

| Feature | Title | Description |
|---------|-------|-------------|
| FEAT-030 | /red-team SKILL.md | Skill definition, routing, triggers, description |
| FEAT-031 | /red-team Agent Definitions | 9 agent definitions (red-recon through red-lead) |
| FEAT-032 | /red-team Templates | Engagement templates, finding templates, report templates |
| FEAT-033 | /red-team Methodology Framework | MITRE ATT&CK mapping, PTES/OSSTMM integration |
| FEAT-034 | /red-team Authorization Controls | Scope verification, rules of engagement enforcement |
| FEAT-035 | /red-team /adversary Integration | C4 quality enforcement for findings and reports |
| FEAT-036 | /red-team Configurable Rules | User-overridable methodology and standards |
| FEAT-037 | /red-team Tool Adapters | Pluggable adapter stubs for Metasploit, Burp, Nmap, etc. |

### 3.5 Phase 5: Purple Team Validation

| Field | Value |
|-------|-------|
| Pipeline | D (validation) |
| Purpose | /red-team attacks /eng-team outputs; cross-pollination convergence |
| Primary Agents | ps-investigator (gap analysis), ps-validator (validation) |
| Support Agents | ps-synthesizer (synthesis), adv-scorer (scoring) |
| Status | PENDING |
| Quality Gate | C4 /adversary >= 0.95 |

#### Features

| Feature | Title | Description |
|---------|-------|-------------|
| FEAT-040 | Purple Team Engagement Plan | Scope, methodology, success criteria for /red-team vs /eng-team |
| FEAT-041 | Attack Surface Analysis | /red-team analyzes /eng-team outputs for weaknesses |
| FEAT-042 | Gap Analysis Report | Identified gaps between offensive findings and defensive posture |
| FEAT-043 | Hardening Recommendations | Specific improvements driven by purple team findings |
| FEAT-044 | Portability Validation | Cross-LLM provider testing of both skills |

### 3.6 Phase 6: Documentation & Registration

| Field | Value |
|-------|-------|
| Pipeline | D (validation) |
| Purpose | Skill documentation, usage guides, framework registration |
| Primary Agents | ps-reporter (docs) |
| Support Agents | ps-reviewer (review), adv-scorer (scoring) |
| Status | PENDING |
| Quality Gate | C4 /adversary >= 0.95 |

#### Features

| Feature | Title | Description |
|---------|-------|-------------|
| FEAT-050 | /eng-team Usage Guide | Complete usage documentation with examples |
| FEAT-051 | /red-team Usage Guide | Engagement guide with methodology walkthroughs |
| FEAT-052 | Rule Set Customization Guide | How to override default standards and rules |
| FEAT-053 | Tool Integration Guide | How to connect external tools via adapters |
| FEAT-054 | Framework Registration | CLAUDE.md, AGENTS.md, mandatory-skill-usage.md updates |

---

## 4. Sync Barrier Protocol

### 4.1 Barrier Transition Rules

```
1. PRE-BARRIER CHECK
   [ ] All phase agents have completed execution
   [ ] All phase artifacts exist and are valid
   [ ] No blocking errors or unresolved issues

2. QUALITY GATE EXECUTION
   [ ] C4 /adversary tournament with all 10 strategies
   [ ] Weighted composite score >= 0.95
   [ ] Max 5 creator-critic-revision iterations
   [ ] Below threshold = REJECTED, revision required

3. POST-BARRIER VERIFICATION
   [ ] Quality gate score recorded
   [ ] Artifacts promoted to next phase input
   [ ] Barrier status updated to COMPLETE
   [ ] Memory-Keeper state persisted
```

### 4.2 Barrier Definitions

| Barrier | Location | Condition | Artifacts | Status |
|---------|----------|-----------|-----------|--------|
| Barrier 1 | Phase 1 internal | After research streams A-E complete | Stream outputs -> C4 review | PENDING |
| Barrier 2 | Phase 1 -> 2 | Research compendium passes C4 | Research compendium -> architecture inputs | PENDING |
| Barrier 3 | Phase 2 -> 3/4 | All 6 ADRs approved | ADR set -> parallel build inputs | PENDING |
| Barrier 4 | Phase 3+4 -> 5 | Both skills complete | /eng-team + /red-team -> purple team inputs | PENDING |
| Barrier 5 | Phase 5 -> 6 | Validation passes | Validation report -> documentation inputs | PENDING |
| Barrier 6 | Phase 6 -> Done | Final quality gate | Documentation set -> project complete | PENDING |

### 4.3 Barrier Detail: Cross-Pipeline Synchronization

**Barrier 4** is the critical cross-pipeline synchronization point where Pipelines B and C converge into Pipeline D:

```
Pipeline B (eng-team)     Pipeline C (red-team)
       │                         │
       ▼                         ▼
╔══════════════════════════════════════════════════╗
║ BARRIER 4: Cross-Pipeline Convergence            ║
║                                                  ║
║ Required:                                        ║
║ • Phase 3 COMPLETE with >= 0.95 quality score    ║
║ • Phase 4 COMPLETE with >= 0.95 quality score    ║
║                                                  ║
║ Artifacts:                                       ║
║ • eng-team -> validation: skill definition,      ║
║   agent definitions, templates, adapters         ║
║ • red-team -> validation: skill definition,      ║
║   agent definitions, methodology, templates      ║
║                                                  ║
║ STATUS: PENDING                                  ║
╚══════════════════════════════════════════════════╝
                    │
                    ▼
           Pipeline D (validation)
```

---

## 5. Quality Gates

> All quality gates use C4 tournament mode: all 10 selected strategies from the strategy catalog. Quality threshold elevated to >= 0.95 per R-013.

| Gate | Transition | Threshold | Strategies | Max Iterations | Status |
|------|------------|-----------|------------|----------------|--------|
| QG-1 | Phase 1 -> 2 | >= 0.95 | All 10 (C4 tournament) | 5 | PENDING |
| QG-2 | Phase 2 -> 3/4 | >= 0.95 | All 10 (C4 tournament) | 5 | PENDING |
| QG-3 | Phase 3 -> 5 | >= 0.95 | All 10 (C4 tournament) | 5 | PENDING |
| QG-4 | Phase 4 -> 5 | >= 0.95 | All 10 (C4 tournament) | 5 | PENDING |
| QG-5 | Phase 5 -> 6 | >= 0.95 | All 10 (C4 tournament) | 5 | PENDING |
| QG-6 | Phase 6 -> Done | >= 0.95 | All 10 (C4 tournament) | 5 | PENDING |

### C4 Tournament Strategy Set

All 10 selected strategies applied at every gate:

| ID | Strategy | Family | Weight in Scoring |
|----|----------|--------|-------------------|
| S-014 | LLM-as-Judge | Iterative Self-Correction | Scoring mechanism |
| S-003 | Steelman Technique | Dialectical Synthesis | Applied before S-002 (H-16) |
| S-013 | Inversion Technique | Structured Decomposition | Applied |
| S-007 | Constitutional AI Critique | Iterative Self-Correction | Applied |
| S-002 | Devil's Advocate | Role-Based Adversarialism | Applied after S-003 (H-16) |
| S-004 | Pre-Mortem Analysis | Role-Based Adversarialism | Applied |
| S-010 | Self-Refine | Iterative Self-Correction | Applied |
| S-012 | FMEA | Structured Decomposition | Applied |
| S-011 | Chain-of-Verification | Structured Decomposition | Applied |
| S-001 | Red Team Analysis | Role-Based Adversarialism | Applied |

### S-014 Scoring Dimensions

| Dimension | Weight | Description |
|-----------|--------|-------------|
| Completeness | 0.20 | All requirements addressed, no gaps |
| Internal Consistency | 0.20 | No contradictions, coherent design |
| Methodological Rigor | 0.20 | Sound approach, evidence-based reasoning |
| Evidence Quality | 0.15 | Authoritative sources, current intelligence |
| Actionability | 0.15 | Executable outputs, clear next steps |
| Traceability | 0.10 | Requirements to implementation traceability |

---

## 6. Agent Registry

### 6.1 Orchestration Agents

| Agent ID | Skill | Role | Phases | Responsibilities |
|----------|-------|------|--------|------------------|
| orch-planner | /orchestration | Workflow Planner | 1 | Phase planning, task decomposition, agent assignment |
| orch-tracker | /orchestration | State Tracker | 1-6 | State persistence, checkpoint management, progress tracking |
| orch-synthesizer | /orchestration | Cross-Pipeline Synthesizer | 5 | Cross-pipeline context retrieval, convergence synthesis |

### 6.2 Problem-Solving Agents

| Agent ID | Skill | Role | Phases | Responsibilities |
|----------|-------|------|--------|------------------|
| ps-researcher | /problem-solving | Researcher | 1 | Primary research across all 6 streams (A-F) |
| ps-synthesizer | /problem-solving | Synthesizer | 1, 5 | Cross-stream synthesis (Phase 1), purple team synthesis (Phase 5) |
| ps-architect | /problem-solving | Architect | 1, 2, 3, 4 | Architecture research (Phase 1), ADR authoring (Phase 2), skill design (Phases 3-4) |
| ps-critic | /problem-solving | Critic | 2, 3, 4 | ADR review (Phase 2), quality review (Phases 3-4) |
| ps-reviewer | /problem-solving | Reviewer | 3, 4, 6 | Skill artifact review (Phases 3-4), documentation review (Phase 6) |
| ps-investigator | /problem-solving | Investigator | 5 | Gap analysis during purple team validation |
| ps-validator | /problem-solving | Validator | 5 | Validation of skill outputs against requirements |
| ps-reporter | /problem-solving | Reporter | 6 | Documentation authoring |

### 6.3 Adversary Agents

| Agent ID | Skill | Role | Phases | Responsibilities |
|----------|-------|------|--------|------------------|
| adv-selector | /adversary | Strategy Selector | 1-6 | Maps C4 criticality to full strategy set at every gate |
| adv-executor | /adversary | Strategy Executor | 1-6 | Executes all 10 strategies against deliverables at gates |
| adv-scorer | /adversary | Quality Scorer | 1-6 | S-014 LLM-as-Judge scoring with 6-dimension rubric |

### 6.4 NASA-SE Agents

| Agent ID | Skill | Role | Phases | Responsibilities |
|----------|-------|------|--------|------------------|
| nse-explorer | /nasa-se | Trade Study Explorer | 1 | Research trade studies for tool integration, methodology selection |
| nse-architecture | /nasa-se | Architecture Reviewer | 2 | Architecture standards review for ADRs |
| nse-requirements | /nasa-se | Requirements Engineer | 2 | Requirements formalization, V&V criteria definition |

### 6.5 Agent-Phase Matrix

| Agent | Ph1 | Ph2 | Ph3 | Ph4 | Ph5 | Ph6 |
|-------|-----|-----|-----|-----|-----|-----|
| orch-planner | P | | | | | |
| orch-tracker | S | S | S | S | S | S |
| orch-synthesizer | | | | | S | |
| ps-researcher | P | S | | | | |
| ps-synthesizer | P | | | | S | |
| ps-architect | P | P | P | P | | |
| ps-critic | | S | S | S | | |
| ps-reviewer | | | P | P | | S |
| ps-investigator | | | | | P | |
| ps-validator | | | | | P | |
| ps-reporter | | | | | | P |
| adv-selector | G | G | G | G | G | G |
| adv-executor | G | G | G | G | G | G |
| adv-scorer | G | G | G | G | G | G |
| nse-explorer | P | | | | | |
| nse-architecture | | P | | | | |
| nse-requirements | | P | | | | |

**Legend:** P = Primary, S = Support, G = Quality Gate

---

## 7. State Management

### 7.1 State Files

| File | Purpose | Update Frequency |
|------|---------|------------------|
| `ORCHESTRATION.yaml` | Machine-readable state (SSOT) | Every state transition |
| `ORCHESTRATION_PLAN.md` | This file -- strategic context | Phase boundaries, major decisions |
| `ORCHESTRATION_WORKTRACKER.md` | Tactical execution documentation | Created when execution begins |

### 7.2 Artifact Path Structure

```
orchestration/cyber-ops-20260222-001/
├── research/
│   ├── phase-1-research/
│   │   ├── stream-a-role-completeness/
│   │   │   ├── A-001-eng-team-roles.md
│   │   │   ├── A-002-red-team-roles.md
│   │   │   ├── A-003-gap-analysis.md
│   │   │   └── A-004-role-synthesis.md
│   │   ├── stream-b-methodology/
│   │   │   ├── B-001-mitre-attack.md
│   │   │   ├── B-002-ptes-osstmm.md
│   │   │   ├── B-003-owasp.md
│   │   │   └── B-004-defensive-methodology.md
│   │   ├── stream-c-tool-integration/
│   │   │   ├── C-001-offensive-tools.md
│   │   │   ├── C-002-defensive-tools.md
│   │   │   └── C-003-adapter-patterns.md
│   │   ├── stream-d-prior-art/
│   │   │   ├── D-001-agentic-security-tools.md
│   │   │   ├── D-002-llm-security-research.md
│   │   │   └── D-003-competitive-analysis.md
│   │   ├── stream-e-portability/
│   │   │   ├── E-001-cross-provider-patterns.md
│   │   │   ├── E-002-dependency-audit.md
│   │   │   └── E-003-portability-strategy.md
│   │   ├── stream-f-secure-sdlc/
│   │   │   ├── F-001-nist-sdlc.md
│   │   │   ├── F-002-cis-sans-standards.md
│   │   │   └── F-003-verification-patterns.md
│   │   └── synthesis/
│   │       ├── S-001-cross-stream-consolidation.md
│   │       ├── S-002-research-compendium.md
│   │       └── S-003-architecture-inputs.md
│   └── phase-2-architecture/
│       ├── ADR-001-agent-team-architecture.md
│       ├── ADR-002-skill-routing.md
│       ├── ADR-003-llm-portability.md
│       ├── ADR-004-configurable-rule-sets.md
│       ├── ADR-005-tool-adapters.md
│       └── ADR-006-authorization-architecture.md
├── eng-team/
│   └── phase-3-build/
│       ├── FEAT-020-skill-definition/
│       ├── FEAT-021-agent-definitions/
│       ├── FEAT-022-templates/
│       ├── FEAT-023-adversary-integration/
│       ├── FEAT-024-configurable-rules/
│       └── FEAT-025-tool-adapters/
├── red-team/
│   └── phase-4-build/
│       ├── FEAT-030-skill-definition/
│       ├── FEAT-031-agent-definitions/
│       ├── FEAT-032-templates/
│       ├── FEAT-033-methodology-framework/
│       ├── FEAT-034-authorization-controls/
│       ├── FEAT-035-adversary-integration/
│       ├── FEAT-036-configurable-rules/
│       └── FEAT-037-tool-adapters/
├── validation/
│   ├── phase-5-purple-team/
│   │   ├── FEAT-040-engagement-plan/
│   │   ├── FEAT-041-attack-surface/
│   │   ├── FEAT-042-gap-analysis/
│   │   ├── FEAT-043-hardening/
│   │   └── FEAT-044-portability-validation/
│   └── phase-6-documentation/
│       ├── FEAT-050-eng-team-guide/
│       ├── FEAT-051-red-team-guide/
│       ├── FEAT-052-rule-customization/
│       ├── FEAT-053-tool-integration/
│       └── FEAT-054-framework-registration/
├── cross-pollination/
│   ├── barrier-1/
│   │   └── stream-review-results/
│   ├── barrier-2/
│   │   └── compendium-review-results/
│   ├── barrier-3/
│   │   └── adr-review-results/
│   ├── barrier-4/
│   │   ├── eng-team-to-validation/
│   │   └── red-team-to-validation/
│   ├── barrier-5/
│   │   └── validation-review-results/
│   └── barrier-6/
│       └── final-review-results/
└── quality-gates/
    ├── QG-1-research-to-architecture.md
    ├── QG-2-architecture-to-build.md
    ├── QG-3-eng-team-to-validation.md
    ├── QG-4-red-team-to-validation.md
    ├── QG-5-validation-to-docs.md
    └── QG-6-final.md
```

### 7.3 Checkpoint Strategy

| Trigger | When | Purpose |
|---------|------|---------|
| PHASE_COMPLETE | After each phase | Phase-level rollback point |
| BARRIER_COMPLETE | After each sync barrier | Quality gate recovery |
| GROUP_COMPLETE | After each execution group (Phase 1) | Research group recovery |
| MANUAL | User-triggered | Debug and inspection |

### 7.4 Memory-Keeper Integration

| Event | Key Pattern | Action |
|-------|-------------|--------|
| Phase complete | `jerry/PROJ-010/phase-boundary/phase-{N}-complete` | Store phase summary + score |
| Phase start | `jerry/PROJ-010/orchestration/phase-{N}-start` | Retrieve prior phase context |
| Research finding | `jerry/PROJ-010/research/{stream}-{task}` | Store research artifact |
| ADR complete | `jerry/PROJ-010/decision/ADR-{NNN}` | Store architecture decision |
| Quality gate | `jerry/PROJ-010/phase-boundary/QG-{N}-results` | Store gate score + feedback |

---

## 8. Execution Constraints

### 8.1 Hard Constraints (Jerry Constitution)

| Constraint | ID | Enforcement |
|------------|----|----|
| Single agent nesting | P-003 | Orchestrator -> Worker only. No recursive subagents. |
| File persistence | P-002 | All state to filesystem. No outputs exist only in context. |
| No deception | P-022 | Transparent reasoning. Honest about capabilities and confidence. |
| User authority | P-020 | User approves gates. Never override user intent. |

### 8.1.1 Worktracker Entity Templates

> **WTI-007:** Entity files (EPIC, FEATURE, ENABLER, TASK, etc.) created during orchestration MUST use canonical templates from `.context/templates/worktracker/`. Read the appropriate template first, then populate. Do not create entity files from memory or by copying other instance files.

### 8.2 Soft Constraints

| Constraint | Value | Rationale |
|------------|-------|-----------|
| Max concurrent agents | 4 | Resource management within single session |
| Max barrier retries | 5 | Circuit breaker per R-013 (5 creator-critic iterations) |
| Checkpoint frequency | PHASE + BARRIER + GROUP | Fine-grained recovery for C4 workflow |
| Max parallel research tasks | 15 | Phase 1 Group 1 fan-out limit |

### 8.3 Requirement Traceability

| Requirement | Enforced In |
|-------------|-------------|
| R-001 (Secure by Design) | Phase 2 ADR-006, Phase 3 all features, Phase 5 validation |
| R-002 (Architecturally Pure) | Phase 2 all ADRs, Phase 3-4 skill design |
| R-003 (No Slop Code) | All phases via C4 /adversary |
| R-004 (No Shortcuts) | Barrier protocol -- no phase skipping |
| R-005 (Grounded in Reality) | Phase 1 evidence-based research, Phase 5 validation |
| R-006 (Evidence-Driven) | Phase 1 research streams, Phase 2 ADR citations |
| R-007 (Persistent Research) | Phase 1 artifact persistence to `work/research/` |
| R-008 (Role Completeness) | Phase 1 Stream A (A-001 through A-004) |
| R-009 (Current Intelligence) | Phase 1 Context7 + WebSearch usage |
| R-010 (LLM Portability) | Phase 1 Stream E, Phase 2 ADR-003, Phase 5 FEAT-044 |
| R-011 (Configurable Rules) | Phase 2 ADR-004, Phase 3 FEAT-024, Phase 4 FEAT-036 |
| R-012 (Tool Integration) | Phase 1 Stream C, Phase 2 ADR-005, Phase 3 FEAT-025, Phase 4 FEAT-037 |
| R-013 (C4 Every Phase) | All 6 quality gates |
| R-014 (Full Orchestration) | This plan + ORCHESTRATION.yaml |
| R-015 (Detailed Worktracker) | ORCHESTRATION_WORKTRACKER.md (created at execution) |
| R-016 (Challenge Weak Specs) | H-31 enforcement throughout |
| R-017 (Industry Leader) | >= 0.95 threshold, C4 tournament, all 10 strategies |
| R-018 (Real Techniques) | Phase 1 Stream B, Phase 4 FEAT-033 |
| R-019 (Secure SDLC) | Phase 1 Stream F, Phase 3 all features |
| R-020 (Authorization) | Phase 2 ADR-006, Phase 4 FEAT-034 |
| R-021 (Remediation Guidance) | Phase 4 FEAT-032 (finding templates) |
| R-022 (Agent Standards) | Phase 3 FEAT-020/021, Phase 4 FEAT-030/031 |
| R-023 (Persist Outputs) | P-002 enforcement + artifact path structure |
| R-024 (Adversary Integration) | Phase 3 FEAT-023, Phase 4 FEAT-035 |

---

## 9. Success Criteria

### 9.1 Phase Exit Criteria

**Phase 1 Exit:**

| Criterion | Validation |
|-----------|------------|
| All 23 research tasks complete | Task artifacts exist in `stream-*/` directories |
| Research compendium assembled | `S-002-research-compendium.md` exists and is complete |
| Architecture inputs prepared | `S-003-architecture-inputs.md` exists |
| Barrier 2 passed | C4 /adversary score >= 0.95 on compendium |

**Phase 2 Exit:**

| Criterion | Validation |
|-----------|------------|
| All 6 ADRs authored and reviewed | ADR files exist in `phase-2-architecture/` |
| Each ADR passes C4 review | Individual ADR scores >= 0.95 |
| Barrier 3 passed | C4 /adversary score >= 0.95 on ADR set |

**Phase 3 Exit:**

| Criterion | Validation |
|-----------|------------|
| All 6 /eng-team features complete | FEAT-020 through FEAT-025 artifacts exist |
| /eng-team skill is structurally valid | SKILL.md, agents/, templates/ all present |
| Barrier QG-3 passed | C4 /adversary score >= 0.95 |

**Phase 4 Exit:**

| Criterion | Validation |
|-----------|------------|
| All 8 /red-team features complete | FEAT-030 through FEAT-037 artifacts exist |
| /red-team skill is structurally valid | SKILL.md, agents/, templates/ all present |
| Authorization controls implemented | FEAT-034 complete with scope verification |
| Barrier QG-4 passed | C4 /adversary score >= 0.95 |

**Phase 5 Exit:**

| Criterion | Validation |
|-----------|------------|
| Purple team engagement complete | All 5 validation features complete |
| Gap analysis documented | FEAT-042 gap analysis report exists |
| Hardening recommendations issued | FEAT-043 recommendations exist |
| Portability validated | FEAT-044 cross-LLM test results exist |
| Barrier QG-5 passed | C4 /adversary score >= 0.95 |

**Phase 6 Exit:**

| Criterion | Validation |
|-----------|------------|
| All 5 documentation features complete | FEAT-050 through FEAT-054 artifacts exist |
| Framework registration complete | CLAUDE.md and AGENTS.md updated |
| Barrier QG-6 passed | C4 /adversary score >= 0.95 |

### 9.2 Workflow Completion Criteria

| Criterion | Validation |
|-----------|------------|
| All 24 requirements fulfilled | Requirement traceability matrix fully satisfied |
| All 6 phases complete | All phase status = COMPLETE |
| All 6 barriers synced | All barrier status = COMPLETE |
| All 6 quality gates passed | All QG scores >= 0.95 |
| 2 new skills operational | `/eng-team` and `/red-team` skills registered and invocable |
| 17 agent definitions | 8 eng-team + 9 red-team agents defined per standards |
| 6 ADRs baselined | All architecture decisions documented with evidence |
| Purple team validated | Adversarial resilience demonstrated (Phase 5) |
| LLM portability confirmed | Cross-provider testing passed (FEAT-044) |
| All outputs persisted | No research or artifacts exist only in conversation context |

---

## 10. Risk Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Context window exhaustion during Phase 1 (23 research tasks) | H | H | AE-006 graduated escalation; checkpoint after each execution group; Memory-Keeper persistence |
| Quality gate score plateau below 0.95 | M | H | Max 5 iterations per gate; escalate to user at iteration 4 with specific feedback |
| Research streams produce contradictory findings | M | M | Synthesis phase (S-001 through S-003) explicitly reconciles contradictions; ps-synthesizer primary agent |
| LLM portability constraints limit agent design | M | H | ADR-003 addresses early; portability validated in Phase 5 before documentation |
| Phase 3/4 parallel divergence | L | M | Barrier 4 cross-pipeline sync; shared architecture from Phase 2 ADRs constrains divergence |
| Authorization architecture insufficient for real-world use | M | H | ADR-006 dedicated to authorization; Phase 5 purple team tests authorization controls |
| Scope creep from 24 requirements | M | M | Requirements frozen after Phase 1 research validates them; changes require C4 review |
| Compaction event during critical phase | M | H | AE-006e mandatory checkpoint; session restart; Memory-Keeper retrieval of prior context |

---

## 11. Resumption Context

### 11.1 Current Execution State

```
WORKFLOW STATUS AS OF 2026-02-22
================================

Pipeline A (research):
  Phase 1: PENDING
  Phase 2: PENDING

Pipeline B (eng-team):
  Phase 3: PENDING

Pipeline C (red-team):
  Phase 4: PENDING

Pipeline D (validation):
  Phase 5: PENDING
  Phase 6: PENDING

Barriers:
  Barrier 1 (Phase 1 internal): PENDING
  Barrier 2 (Phase 1 -> 2):     PENDING
  Barrier 3 (Phase 2 -> 3/4):   PENDING
  Barrier 4 (Phase 3+4 -> 5):   PENDING
  Barrier 5 (Phase 5 -> 6):     PENDING
  Barrier 6 (Phase 6 -> Done):  PENDING

Quality Gates:
  QG-1: PENDING
  QG-2: PENDING
  QG-3: PENDING
  QG-4: PENDING
  QG-5: PENDING
  QG-6: PENDING
```

### 11.2 Next Actions

1. Create `ORCHESTRATION.yaml` with machine-readable initial state
2. Execute Phase 1, Group 1: Launch 15 parallel research tasks across streams A-E
3. Persist all research artifacts to `work/research/` and orchestration artifact paths
4. After Group 1 completes, execute Group 2 (A-004, E-003) dependent synthesis tasks
5. Apply Barrier 1: C4 /adversary tournament on all stream outputs

---

> **P-043 Disclaimer:** This orchestration plan was generated by an AI assistant operating within the Jerry Framework governance constraints. All phase outputs, quality gate scores, and agent assessments are subject to the framework's quality enforcement architecture (L1-L5) and require human review at gate transitions per P-020 (User Authority). The plan reflects the best available analysis at time of creation and should be validated against current project requirements before execution.

---

*Document ID: PROJ-010-ORCH-PLAN*
*Workflow ID: cyber-ops-20260222-001*
*Version: 2.0*
*Cross-Session Portable: All paths are repository-relative*
