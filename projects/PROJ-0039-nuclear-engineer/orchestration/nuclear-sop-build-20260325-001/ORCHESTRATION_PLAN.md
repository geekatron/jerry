# Nuclear SOP Build Pipeline: Orchestration Plan

> **Document ID:** PROJ-0039-ORCH-BUILD-PLAN
> **Project:** PROJ-0039-nuclear-engineer
> **Workflow ID:** `nuclear-sop-build-20260325-001`
> **Date:** 2026-03-25
> **Status:** PLANNED
> **Version:** 2.2.0
> **Pattern:** Cross-Pollinated Pipeline (Pattern 5) — eng-team + red-team + nasa-se pipelines with three bidirectional sync barriers

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Workflow Overview](#l0-workflow-overview) | Stakeholder-facing summary |
| [L1: Technical Plan](#l1-technical-plan) | Full workflow diagram, pipeline definitions, phase assignments, barriers |
| [L2: Implementation Details](#l2-implementation-details) | State schema, path configuration, recovery strategies |
| [Execution Constraints](#execution-constraints) | Constitutional constraints and hard limits |
| [Success Criteria](#success-criteria) | Phase and barrier exit criteria |
| [Risk Mitigations](#risk-mitigations) | Risk register with likelihood, impact, mitigations |
| [Resumption Context](#resumption-context) | Cross-session execution state and next actions |
| [Revision History](#revision-history) | Version history with change summaries |
| [Disclaimer](#disclaimer) | Required output disclaimer |

---

## L0: Workflow Overview

The research is done. Now we build — and this time, we build to a higher standard.

The prior workflow (`nuclear-sop-research-20260319-001`) produced a complete specification for the `/nuclear-sop` skill: four agents (sop-brief, sop-executor, sop-verifier, sop-capture), their templates, their behavioral rules, and an ADR validating the architecture. Subsequent integration research (`skill-integration-analysis.md`) identified how the skill fits into the ecosystem, established the routing keyword table, and designed the GAP-09 behavioral baseline monitoring capability. Four of five upstream artifacts have quality-gated scores (0.922, 0.933, 0.914, 0.920); the integration analysis was produced under a separate workflow at 0.91 (iteration 2, PASSED at threshold 0.90). The specification defines exactly what 16 files need to exist and what they need to do.

This workflow builds those files, attacks them, verifies them formally, and registers them.

Three pipelines run in parallel and cross-inform each other. The engineering pipeline (eng-team) designs, implements, tests, reviews, and registers the skill. The red-team pipeline maps the attack surface, finds vulnerabilities, and develops exploitation methodology. The V&V pipeline (nasa-se) traces requirements, creates a formal verification plan, and conducts a CDR-equivalent technical review as the final gate before workflow completion. All three pipelines meet at three synchronization barriers.

The test harness is itself a consumer of the skill being built — a self-referential validation that proves the skill's fitness by using it to guide the construction of the tool that tests it. ENG Phase 4 extends this with seven quantitative performance metrics (STAR catch rate, false positive rate, OE schema completeness, prerequisite detection, quality gate convergence, GAP-09 behavioral baseline recording, and composition pattern validation).

Quality enforcement is upgraded to C3 at the 0.93 threshold. Every phase exit runs the full six-strategy C3 required set with S-003 Steelman applied before S-002 Devil's Advocate at every critique cycle. Barriers use tournament-style multi-strategy review. Maximum iterations increase to five per gate.

**Why this matters:** A skill that governs procedure execution but has never been red-teamed is governance theater. A skill that has never been formally verified against its own requirements specification is a claim without evidence. The three-pipeline architecture converts a specification-compliant implementation into a hardened, independently verified deliverable with a formal requirements trace and a registration in the ecosystem routing table.

**Current State:** PLANNED — awaiting Barrier 0 (pre-conditions verification) then parallel pipeline execution.

**Orchestration Pattern:** Cross-Pollinated (Pattern 5) — three pipelines with bidirectional communication at three sync barriers.

### Workflow Identification

| Field | Value | Source |
|-------|-------|--------|
| Workflow ID | `nuclear-sop-build-20260325-001` | user-specified |
| ID Format | `{purpose}-{YYYYMMDD}-{NNN}` | semantic-date-seq |
| Base Path | `orchestration/nuclear-sop-build-20260325-001/` | Dynamic |

### Upstream Dependencies (COMPLETE)

| Artifact | Workflow | Status |
|----------|----------|--------|
| Phase 4 synthesis spec | `nuclear-sop-research-20260319-001/ps/phase-4/ps-synthesizer-001/skill-specification-synthesis.md` | COMPLETE (0.922) |
| ADR-001 architecture | `nuclear-sop-research-20260319-001/ps/phase-3/ps-architect-001/ADR-001-nuclear-sop-skill-architecture.md` | COMPLETE (0.933) |
| Pattern extraction | `nuclear-sop-research-20260319-001/ps/phase-2/ps-analyst-001/sop-pattern-extraction.md` | COMPLETE (0.914) |
| Nuclear survey | `nuclear-sop-research-20260319-001/ps/phase-1/ps-researcher-001/nuclear-sop-survey.md` | COMPLETE (0.920) |
| Integration analysis | `research/skill-integration-analysis.md` | COMPLETE (0.91, iteration 2 PASS at 0.90 threshold; below 0.93 build threshold — ACCEPTED-RISK, see Risk Register) |

---

## L1: Technical Plan

### Workflow Diagram (ASCII)

```
PIPELINE A: ENGINEERING (alias: eng)     PIPELINE B: RED TEAM (alias: red)     PIPELINE C: V&V (alias: vv)
=====================================    =====================================  ===========================

┌────────────────────────────────────────────────────────────────────────┐
│  PRE-CONDITIONS (Barrier 0)                                            │
│  Verify all upstream artifacts exist; confirm synthesis spec complete  │
│  Confirm skills/nuclear-sop/ does not exist                           │
└──────────────────────────┬─────────────────────────────────────────────┘
                           │ VERIFIED
          ┌────────────────┴────────────────┐
          │                                 │
          ▼                                 ▼

┌────────────────────┐             ┌────────────────────┐
│ ENG Phase 1        │             │ RED Phase 1         │
│ Architecture &     │             │ Engagement Scope    │
│ Threat Model       │             │ (Rules of           │
│ Agent: eng-arch    │             │  Engagement)        │
│ STRIDE threat      │             │ Agent: red-lead     │
│ model for skill    │             │ Scope, targets,     │
│ attack surface     │             │ attack vectors      │
│ QG: full C3 set    │             │ No quality gate     │
│ S-003 -> S-002     │             │                     │
└────────┬───────────┘             └──────────┬──────────┘
         │                                    │
         ▼                                    │
┌────────────────────┐                        │
│ ENG Phase 2        │                        │
│ Implementation     │                        │
│ Planning &         │                        │
│ Standards          │                        │
│ Agent: eng-lead    │                        │
│ File mapping,      │                        │
│ H-34/H-35 plan,   │                        │
│ test harness plan  │                        │
│ QG: full C3 set    │                        │
│ S-003 -> S-002     │                        │
└────────┬───────────┘                        │
         │                                    │
         ▼                                    │
┌──────────────────────────────────────────┬──┘
│ ENG Phase 3: Implementation (Fan-Out)    │
│ 4 parallel eng-backend agents            │
│                                          │
│  ┌─────────────┐  ┌─────────────┐        │
│  │ eng-back-001│  │ eng-back-002│        │
│  │ SKILL.md    │  │ sop-brief   │        │
│  │ +rules.md   │  │ + PRE_JOB   │        │
│  │ QG: C3 full │  │ .template   │        │
│  │ S-003->S-002│  │ QG: C3 full │        │
│  └─────────────┘  └─────────────┘        │
│                                          │
│  ┌─────────────┐  ┌─────────────┐        │
│  │ eng-back-003│  │ eng-back-004a         │
│  │ sop-executor│  │ sop-verifier│        │
│  │ + templates │  │ QG: C3 full │        │
│  │ QG: C3 full │  │ S-003->S-002│        │
│  │ S-003->S-002│  └─────────────┘        │
│  └─────────────┘  ┌─────────────┐        │
│                   │ eng-back-004b         │
│                   │ sop-capture │        │
│                   │ + POST_JOB  │        │
│                   │ .template   │        │
│                   │ QG: C3 full │        │
│                   │ S-003->S-002│        │
│                   └─────────────┘        │
└─────────────────────────┬────────────────┘
                          │
      ┌───────────────────┘
      │ Skill files built
      │
      ▼
╔══════════════════════════════════════════════════════════════════════╗
║  BARRIER 1: ENG Phase 3 Fan-In + RED Phase 1                        ║
║  ──────────────────────────────────────────────────────────────────  ║
║  ENG → RED: Built skill files shared for attack surface mapping      ║
║  RED → ENG: Attack surface findings inform test harness design (E4)  ║
║  ENG → V&V: Built skill files + synthesis spec shared for req trace  ║
║  Quality Gate: >= 0.93; tournament-style 6-strategy review           ║
║  Sync: eng-phase-3 COMPLETE AND red-phase-1 COMPLETE                 ║
╚════════════╤═══════════════════════╤═══════════════════╤═════════════╝
             │                       │                   │
             ▼                       ▼                   ▼

┌──────────────────────┐  ┌──────────────────────┐  ┌──────────────────────┐
│ ENG Phase 4          │  │ RED Phase 2           │  │ V&V Phase 1          │
│ Test Harness & QA    │  │ Reconnaissance &      │  │ Requirements         │
│ Agent: eng-qa        │  │ Attack Surface        │  │ Traceability         │
│ STAR trap suite (3+) │  │ Agent: red-recon      │  │ Agent: nse-req       │
│ 7 performance metrics│  │ Input vectors, trust  │  │ Map 14 nuclear       │
│ GAP-09 baselines     │  │ boundaries, flows,    │  │ patterns to agents,  │
│ Apply /nuclear-sop   │  │ OE injection points   │  │ templates, tests     │
│ to build harness     │  │ QG: full C3 set       │  │ Req trace matrix     │
│ QG: full C3 set      │  │ S-003 -> S-002        │  │ QG: full C3 set      │
└──────────┬───────────┘  └──────────┬────────────┘  └──────────┬───────────┘
           │                         ▼                           │
           │              ┌──────────────────────┐               │
           │              │ RED Phase 3           │               │
           │              │ Vulnerability         │               │
           │              │ Analysis              │               │
           │              │ Agent: red-vuln       │               │
           │              │ Prompt injection,     │               │
           │              │ STAR bypass, hold pt  │               │
           │              │ evasion, OE poisoning │               │
           │              │ PROC_STATE manip.     │               │
           │              │ QG: full C3 set       │               │
           │              │ S-003 -> S-002        │               │
           │              └──────────┬────────────┘               │
           │                         │                            │
           ▼                         │                            │
┌──────────────────────┐             │                            │
│ ENG Phase 5          │             │                            │
│ Security Code Review │             │                            │
│ Agent: eng-security  │             │                            │
│ Prompt injection     │             │                            │
│ vectors, hold point  │             │                            │
│ bypass, tool tier    │             │                            │
│ violations, STAR     │             │                            │
│ evasion patterns     │             │                            │
│ QG: full C3 set      │             │                            │
│ S-003 -> S-002       │             │                            │
└──────────┬───────────┘             │                            │
           │                         │                            │
           └──────────┬──────────────┘                            │
                      │ Both reach barrier                        │
                      ▼                                           │
╔══════════════════════════════════════════════════════════╗       │
║  BARRIER 2: ENG Phase 5 + RED Phase 3                   ║       │
║  ─────────────────────────────────────────────────────  ║       │
║  ENG → RED: Security findings inform exploitation       ║       │
║  RED → ENG: Vulnerability findings inform final review  ║       │
║  Quality Gate: >= 0.93; tournament-style 6-strategy     ║       │
║  Sync: eng-phase-5 COMPLETE AND red-phase-3 COMPLETE    ║       │
╚════════════╤═══════════════════════╤════════════════════╝       │
             │                       │                            │
             ▼                       ▼                            │
┌──────────────────────┐  ┌──────────────────────┐               │
│ ENG Phase 6          │  │ RED Phase 4           │               │
│ Final Review Gate    │  │ Exploitation          │               │
│ + Registration       │  │ Methodology           │               │
│ Agent: eng-reviewer  │  │ Agent: red-exploit    │               │
│ Compliance matrix    │  │ PoC methodology for  │               │
│ H-34/H-35 schema     │  │ top vulnerabilities  │               │
│ All ACs from spec    │  │ Impact assessment,   │               │
│ Registration updates │  │ mitigation proposals  │               │
│ QG: full C3 set      │  │ No quality gate      │               │
└──────────┬───────────┘  └──────────┬────────────┘               │
           │                          │                            │
           │              V&V Phase 2 (starts after E4 complete)   │
           │              ┌──────────────────────────────────┐     │
           │              │ V&V Phase 2                      │     │
           │              │ V&V Plan                         │<────┘
           │              │ Agent: nse-verifier              │
           │              │ Req verification, design         │
           │              │ verification, behavioral         │
           │              │ validation, integration test     │
           │              │ QG: full C3 set                  │
           │              └──────────┬───────────────────────┘
           │                         │
           └──────────┬──────────────┘
                      │ ENG Phase 6 + V&V Phase 2 both reach barrier
                      ▼
╔════════════════════════════════════════════════════════════════════╗
║  BARRIER 3: ENG Phase 6 + RED Phase 4 + V&V Phase 2               ║
║  ────────────────────────────────────────────────────────────────  ║
║  V&V Phase 3 entrance gate: all 16 skill files exist,             ║
║  all prior QGs passed, test harness complete, registration done    ║
║  Quality Gate: >= 0.93; tournament-style 6-strategy               ║
║  Sync: eng-phase-6 COMPLETE AND red-phase-4 COMPLETE              ║
║        AND vv-phase-2 COMPLETE                                     ║
╚════════════════════════════╤═══════════════════════════════════════╝
                             │
                             ▼
              ┌──────────────────────────────────┐
              │ V&V Phase 3                       │
              │ Formal Technical Review (CDR)     │
              │ Agent: nse-reviewer               │
              │ Full requirements trace,          │
              │ verification methods executed,    │
              │ all open items dispositioned      │
              │ QG: full C3 set                   │
              └──────────────┬────────────────────┘
                             │
                             ▼
                   ╔══════════════════════╗
                   ║  WORKFLOW COMPLETE   ║
                   ║  /nuclear-sop        ║
                   ║  BUILT, HARDENED,    ║
                   ║  VERIFIED &          ║
                   ║  REGISTERED          ║
                   ╚══════════════════════╝
```

### Pipeline Definitions

| Pipeline | Alias | Skill Source | Phases | Pattern |
|----------|-------|--------------|--------|---------|
| Engineering | eng | eng-team | 6 phases (incl. 1 fan-out) + 8 quality gates | Sequential with Fan-Out in Phase 3 (5 sub-agents: 001, 002, 003, 004a, 004b) |
| Red Team | red | red-team | 4 phases + 2 quality gates | Sequential |
| V&V | vv | nasa-se | 3 phases + 3 quality gates | Sequential |

**Pipeline Alias Resolution:**
- `eng` — auto-derived from `eng-team` skill prefix (no user override; no skill default; abbreviated form)
- `red` — auto-derived from `red-team` skill prefix (no user override; no skill default; abbreviated form)
- `vv` — auto-derived from `nasa-se` skill prefix (no user override; no skill default; abbreviated to V&V function)

### Phase Definitions — Pipeline A (Engineering)

| Phase | Name | Agent(s) | Input | Output Artifact(s) | Quality Gate |
|-------|------|----------|-------|--------------------|--------------|
| E1 | Architecture & Threat Model | eng-architect-001 | Synthesis spec, ADR-001 | `secure-architecture-design.md` | Full C3 set (S-007 + S-002 + S-014 + S-004 + S-012 + S-013); S-003 before S-002; >= 0.93 |
| E2 | Implementation Planning | eng-lead-001 | E1 output, synthesis spec | `implementation-plan.md` | Full C3 set; S-003 before S-002; >= 0.93 |
| E3a | SKILL.md + rules (fan-out) | eng-backend-001 | E2 output, synthesis spec | `SKILL.md`, `nuclear-sop-behavior-rules.md` | Full C3 set; S-003 before S-002; >= 0.93 |
| E3b | sop-brief agent (fan-out) | eng-backend-002 | E2 output, synthesis spec | `sop-brief.md`, `sop-brief.governance.yaml`, `PRE_JOB_BRIEF.template.md` | Full C3 set; S-003 before S-002; >= 0.93 |
| E3c | sop-executor agent (fan-out) | eng-backend-003 | E2 output, synthesis spec | `sop-executor.md`, `sop-executor.governance.yaml`, `WORKFLOW_DEFINITION.template.md`, `PROCEDURE_STATE.template.yaml`, `HOLD_POINT_LOG.template.md` | Full C3 set; S-003 before S-002; >= 0.93 |
| E3d-a | sop-verifier agent (fan-out) | eng-backend-004a | E2 output, synthesis spec | `sop-verifier.md`, `sop-verifier.governance.yaml` | Full C3 set; S-003 before S-002; >= 0.93 |
| E3d-b | sop-capture agent + POST_JOB_BRIEF template (fan-out) | eng-backend-004b | E2 output, synthesis spec | `sop-capture.md`, `sop-capture.governance.yaml`, `POST_JOB_BRIEF.template.md` | Full C3 set; S-003 before S-002; >= 0.93 |
| BARRIER-1 | Cross-Pollination Sync | — | E3 all complete + R1 complete | Barrier handoff docs | >= 0.93 all directions; tournament-style |
| E4 | Test Harness & QA (incl. Performance Metrics + GAP-09) | eng-qa-001 | Skill files (post-B1), synthesis spec, integration analysis | `test-strategy.md` + test harness files + `behavioral-baselines/` | Full C3 set; S-003 before S-002; >= 0.93 |
| E5 | Security Code Review | eng-security-001 | Skill files, E1 threat model | `security-review.md` | Full C3 set; S-003 before S-002; >= 0.93 |
| BARRIER-2 | Cross-Pollination Sync | — | E5 complete + R3 complete | Barrier handoff docs | >= 0.93 both directions; tournament-style |
| E6 | Final Review Gate + Registration | eng-reviewer-001 | All built files, all reviews, test results | `compliance-verification.md` + routing registration updates | Full C3 set; S-003 before S-002; >= 0.93 |

### Phase Definitions — Pipeline B (Red Team)

| Phase | Name | Agent(s) | Input | Output Artifact(s) | Quality Gate |
|-------|------|----------|-------|--------------------|--------------|
| R1 | Engagement Scope | red-lead-001 | Synthesis spec, ADR-001 | `engagement-scope.md` | None (scoping doc) |
| R2 | Reconnaissance & Attack Surface | red-recon-001 | Skill files (post-B1), R1 output | `attack-surface-map.md` | Full C3 set; S-003 before S-002; >= 0.93 |
| R3 | Vulnerability Analysis | red-vuln-001 | R2 output, skill files | `vulnerability-report.md` | Full C3 set; S-003 before S-002; >= 0.93 |
| R4 | Exploitation Methodology | red-exploit-001 | R3 output, E5 output (post-B2) | `exploitation-methodology.md` | None (final report) |

### Phase Definitions — Pipeline C (V&V)

| Phase | Name | Agent(s) | Input | Output Artifact(s) | Quality Gate |
|-------|------|----------|-------|--------------------|--------------|
| V1 | Requirements Traceability | nse-requirements-001 | Synthesis spec, skill files (post-B1), pattern extraction | `requirements-traceability-matrix.md` | Full C3 set; S-003 before S-002; >= 0.93 |
| V2 | V&V Plan | nse-verification-001 | V1 output, test harness (post-E4) | `vv-plan.md` | Full C3 set; S-003 before S-002; >= 0.93 |
| V3 | Formal Technical Review (CDR) | nse-reviewer-001 | All skill files, all phase outputs, V1+V2 outputs (post-B3) | `formal-technical-review.md` | Full C3 set; S-003 before S-002; >= 0.93 |

### Sync Barrier Specifications

#### Barrier 1: After ENG Phase 3 Fan-In + RED Phase 1

| Field | Value |
|-------|-------|
| ID | BARRIER-1 |
| Sync Condition | ALL of: eng-backend-001, eng-backend-002, eng-backend-003, eng-backend-004a, eng-backend-004b COMPLETE AND red-lead-001 COMPLETE |
| Direction 1 | ENG → RED: All 16 built skill files shared for attack surface mapping |
| Direction 2 | RED → ENG: Engagement scope and initial attack vector hypotheses shared to inform test harness design |
| Direction 3 | ENG → V&V: All 16 built skill files + synthesis spec shared for requirements traceability |
| Quality Gate | >= 0.93 all directions; tournament-style review: 7 strategies applied (6 C3 required + S-003 per H-16) against each handoff document; adv-executor-barrier-1 assigned (see Execution Queue Groups 7a/7b) |
| Artifact Path (ENG→RED) | `cross-pollination/barrier-1/eng-to-red/barrier-handoff.md` |
| Artifact Path (RED→ENG) | `cross-pollination/barrier-1/red-to-eng/barrier-handoff.md` |
| Artifact Path (ENG→VV) | `cross-pollination/barrier-1/eng-to-vv/barrier-handoff.md` |
| Unblock | RED Phase 2 + ENG Phase 4 + V&V Phase 1 |

#### Barrier 2: After ENG Phase 5 + RED Phase 3

| Field | Value |
|-------|-------|
| ID | BARRIER-2 |
| Sync Condition | eng-security-001 COMPLETE AND red-vuln-001 COMPLETE |
| Direction 1 | ENG → RED: Security review findings and identified prompt injection vectors shared for exploitation methodology |
| Direction 2 | RED → ENG: Vulnerability report shared; findings inform final review compliance checks |
| Quality Gate | >= 0.93 both directions; tournament-style review: 7 strategies applied (6 C3 required + S-003 per H-16); adv-executor-barrier-2 assigned (see Execution Queue Groups 16a/16b) |
| Artifact Path (ENG→RED) | `cross-pollination/barrier-2/eng-to-red/barrier-handoff.md` |
| Artifact Path (RED→ENG) | `cross-pollination/barrier-2/red-to-eng/barrier-handoff.md` |
| Unblock | RED Phase 4 + ENG Phase 6 |

#### Barrier 3: After ENG Phase 6 + RED Phase 4 + V&V Phase 2

| Field | Value |
|-------|-------|
| ID | BARRIER-3 |
| Sync Condition | eng-reviewer-001 COMPLETE AND red-exploit-001 COMPLETE AND nse-verification-001 COMPLETE |
| Direction 1 | All pipelines → V&V Phase 3: All 16 skill files, compliance matrix, exploitation methodology, V1+V2 outputs provided as CDR entrance package |
| Quality Gate | >= 0.93; tournament-style review: 7 strategies applied (6 C3 required + S-003 per H-16) against CDR entrance package; adv-executor-barrier-3 assigned (see Execution Queue Groups 19a/19b) |
| Artifact Path (All→V3) | `cross-pollination/barrier-3/all-to-vv/barrier-handoff.md` |
| Entrance Criteria | (a) All 16 skill files exist; (b) all prior QGs passed at >= 0.93; (c) test harness complete with all 7 metrics documented; (d) registration updates written; (e) no unresolved CRITICAL vulnerabilities |
| Unblock | V&V Phase 3 (Formal Technical Review) |

### Quality Gate Specifications

> **Global policy for v2.1.0:** All quality gates use the FULL C3 required strategy set. Every critique cycle applies S-003 (Steelman) before S-002 (Devil's Advocate) per H-16. **Total strategies per gate: 7** (6 C3 required: S-007, S-002, S-014, S-004, S-012, S-013; plus S-003 per H-16). Maximum iterations: 5 per gate (RT-M-010 C3 ceiling); **minimum iterations: 3 per gate (H-14)**. Threshold: >= 0.93.

#### Quality Gate E1 — Secure Architecture Review (ENG Phase 1 Exit)

| Field | Value |
|-------|-------|
| Criticality | C3 |
| Threshold | >= 0.93 |
| Required Strategies | S-003 (Steelman), S-007 (Constitutional AI Critique), S-002 (Devil's Advocate), S-014 (LLM-as-Judge), S-004 (Pre-Mortem), S-012 (FMEA), S-013 (Inversion) |
| Strategy Order | S-003 MUST precede S-002 (H-16 enforcement) |
| Max Iterations | 5 |
| Creator | eng-architect-001 |
| Critic | adv-executor-001 |
| Validation Criteria | (a) STRIDE threat model covers all four attack surfaces (prompt injection, hold point bypass, STAR evasion, OE poisoning); (b) Secure design decisions trace to specific threats; (c) Architecture respects P-003/P-020/P-022; (d) No over-engineering relative to synthesis spec; (e) FMEA: failure modes for each attack surface enumerated with RPN scores; (f) Inversion: what does a perfectly insecure implementation look like? Does the design address it? |
| Failure Action | Return to eng-architect-001 with critique; revise and re-submit |

#### Quality Gate E2 — Implementation Plan Review (ENG Phase 2 Exit)

| Field | Value |
|-------|-------|
| Criticality | C3 |
| Threshold | >= 0.93 |
| Required Strategies | S-003, S-007, S-002, S-014, S-004, S-012, S-013 |
| Strategy Order | S-003 before S-002 |
| Max Iterations | 5 |
| Creator | eng-lead-001 |
| Critic | adv-scorer-001 |
| Validation Criteria | (a) All 16 files from synthesis spec are accounted for; (b) H-34/H-35 compliance plan is concrete and actionable; (c) Test harness plan identifies all 7 performance metrics to measure; (d) File assignments are correct (right agent gets right files); (e) Pre-mortem: what fails if Phase 3 fan-out runs with this plan? |
| Failure Action | Return to eng-lead-001 with scoring breakdown; targeted revision |

#### Quality Gate E3 — Implementation Review (ENG Phase 3 Sub-Agents, per sub-agent)

| Field | Value |
|-------|-------|
| Criticality | C3 |
| Threshold | >= 0.93 |
| Required Strategies | S-003, S-007, S-002, S-014, S-004, S-012, S-013 |
| Strategy Order | S-003 before S-002 |
| Max Iterations | 5 per sub-agent |
| Creator | eng-backend-001, eng-backend-002, eng-backend-003, eng-backend-004a, eng-backend-004b (each independently) |
| Critic | adv-executor per sub-agent (002 through 005a/005b) |
| Validation Criteria | (a) Files pass H-34 JSON Schema validation; (b) Constitutional triplet (P-003/P-020/P-022) present; (c) File content matches synthesis spec for this agent's scope; (d) No hardcoded pipeline names or paths; (e) Inversion: does the agent definition prevent the behaviors it is supposed to prevent? |
| Failure Action | Return to responsible eng-backend with critique; revise and re-submit |

#### Quality Gate E4 — Test Harness Review (ENG Phase 4 Exit)

| Field | Value |
|-------|-------|
| Criticality | C3 |
| Threshold | >= 0.93 |
| Required Strategies | S-003, S-007, S-002, S-014, S-004, S-012, S-013 |
| Strategy Order | S-003 before S-002 |
| Max Iterations | 5 |
| Creator | eng-qa-001 |
| Critic | adv-executor-006 |
| Validation Criteria | (a) STAR trap suite contains >= 3 deliberate traps; (b) A/B comparison framework is implemented; (c) Hold point compliance tests are deterministic; (d) OE schema validation tests exercise schema boundaries; (e) /nuclear-sop applied to test harness construction (self-referential); (f) Pre-mortem: what fails if agents execute STAR steps undeterministically; (g) All 7 performance metrics are present with instrumentation; (h) >= 3 GAP-09 behavioral baseline scenarios recorded in `skills/nuclear-sop/behavioral-baselines/`; (i) At least 1 composition pattern (nuclear-sop wrapping another skill) demonstrated in worked example |
| Failure Action | Return to eng-qa-001 with critique; revise and re-submit |

#### Quality Gate E5 — Security Review (ENG Phase 5 Exit)

| Field | Value |
|-------|-------|
| Criticality | C3 |
| Threshold | >= 0.93 |
| Required Strategies | S-003, S-007, S-002, S-014, S-004, S-012, S-013 |
| Strategy Order | S-003 before S-002 |
| Max Iterations | 5 |
| Creator | eng-security-001 |
| Critic | adv-executor-007 |
| Validation Criteria | (a) All prompt injection vectors from threat model are addressed; (b) Hold point bypass paths are eliminated or documented as accepted risks; (c) Tool tier violations are enumerated; (d) STAR evasion patterns are covered by behavioral rules; (e) FMEA residual risk table populated |
| Failure Action | Return to eng-security-001 with critique; revise and re-submit |

#### Quality Gate E6 — Final Compliance Review (ENG Phase 6 Exit)

| Field | Value |
|-------|-------|
| Criticality | C3 |
| Threshold | >= 0.93 |
| Required Strategies | S-003, S-007, S-002, S-014, S-004, S-012, S-013 |
| Strategy Order | S-003 before S-002 |
| Max Iterations | 5 |
| Creator | eng-reviewer-001 |
| Critic | adv-executor-008 |
| Validation Criteria | (a) All acceptance criteria from synthesis spec Section 3 are met; (b) H-34/H-35 schema compliance verified for all 4 agent definition pairs; (c) Compliance evidence matrix complete and traceable; (d) Red-team vulnerability findings resolved or risk-accepted with documented rationale; (e) Registration deliverables present: trigger map row, CLAUDE.md entry, AGENTS.md entries |
| Failure Action | Return to eng-reviewer-001 with scoring breakdown; targeted revision |

#### Quality Gate R2 — Attack Surface Review (RED Phase 2 Exit)

| Field | Value |
|-------|-------|
| Criticality | C3 |
| Threshold | >= 0.93 |
| Required Strategies | S-003, S-007, S-002, S-014, S-004, S-012, S-013 |
| Strategy Order | S-003 before S-002 |
| Max Iterations | 5 |
| Creator | red-recon-001 |
| Critic | adv-executor-009 |
| Validation Criteria | (a) All input vectors to each agent are documented; (b) Trust boundaries between agents are mapped; (c) PROCEDURE_STATE.yaml data flow is traced end-to-end; (d) OE entry injection points are enumerated |
| Failure Action | Return to red-recon-001 with critique; revise and re-submit |

#### Quality Gate R3 — Vulnerability Report Review (RED Phase 3 Exit)

| Field | Value |
|-------|-------|
| Criticality | C3 |
| Threshold | >= 0.93 |
| Required Strategies | S-003, S-007, S-002, S-014, S-004, S-012, S-013 |
| Strategy Order | S-003 before S-002 |
| Max Iterations | 5 |
| Creator | red-vuln-001 |
| Critic | adv-executor-010 |
| Validation Criteria | (a) Each vulnerability has an attack scenario; (b) Severity is rated with justification; (c) Inversion: what would a perfectly secure implementation look like? Does the diff reveal gaps?; (d) No vulnerability category from the engagement scope is unaddressed |
| Failure Action | Return to red-vuln-001 with critique; revise and re-submit |

#### Quality Gate V1 — Requirements Traceability Review (V&V Phase 1 Exit)

| Field | Value |
|-------|-------|
| Criticality | C3 |
| Threshold | >= 0.93 |
| Required Strategies | S-003, S-007, S-002, S-014, S-004, S-012, S-013 |
| Strategy Order | S-003 before S-002 |
| Max Iterations | 5 |
| Creator | nse-requirements-001 |
| Critic | adv-executor-011 |
| Validation Criteria | (a) All 14 directly implemented nuclear patterns traced from pattern-extraction to agent definition; (b) All 4 approximated patterns have explicit transparency notes; (c) All 4 impossible patterns have acknowledged rationale; (d) Each trace entry links: nuclear pattern → gap analysis finding → synthesis spec section → agent/template file → test case ID; (e) Matrix is complete — no pattern without a trace row |
| Failure Action | Return to nse-requirements-001 with critique; revise and re-submit |

#### Quality Gate V2 — V&V Plan Review (V&V Phase 2 Exit)

| Field | Value |
|-------|-------|
| Criticality | C3 |
| Threshold | >= 0.93 |
| Required Strategies | S-003, S-007, S-002, S-014, S-004, S-012, S-013 |
| Strategy Order | S-003 before S-002 |
| Max Iterations | 5 |
| Creator | nse-verification-001 |
| Critic | adv-executor-012 |
| Validation Criteria | (a) Requirements verification section: does each agent definition satisfy its nuclear pattern requirements? Verification method defined for each using the LLM behavioral verification vocabulary defined in criterion (c); (b) Design verification section: does the 4-agent architecture satisfy ADR-001 design decisions? Each ADR decision has a verification method; (c) Behavioral validation section: does STAR actually catch errors per Section 1.5a of synthesis spec? Test method references eng-qa-001 performance metrics. For LLM-behavioral verification claims, acceptable verification methods are: BEHAVIORAL-SAMPLE (adversarial test scenario with documented STAR output), TRACE-INSPECTION (review of PROCEDURE_STATE.yaml execution log for correct field population), METRIC-REFERENCE (cite PM-01 through PM-07 metric results from QG-E4), or STRUCTURAL-ANALYSIS (review agent definition for correct behavioral rule encoding). Each behavioral requirement MUST be linked to one of these four methods; (d) Integration validation section: do agents compose correctly in 3-hop and 4-hop sequences? Test cases reference test harness composition pattern (PM-07); (e) Open items section with disposition plan |
| Failure Action | Return to nse-verification-001 with critique; revise and re-submit |

#### Quality Gate V3 — Formal Technical Review (V&V Phase 3 Exit)

| Field | Value |
|-------|-------|
| Criticality | C3 |
| Threshold | >= 0.93 |
| Required Strategies | S-003, S-007, S-002, S-014, S-004, S-012, S-013 |
| Strategy Order | S-003 before S-002 |
| Max Iterations | 5 |
| Creator | nse-reviewer-001 |
| Critic | adv-executor-013 |
| Validation Criteria | (a) All requirements in traceability matrix have been verified (pass/fail recorded); (b) All verification methods in V&V plan have been executed; (c) All open items dispositioned using the mandatory taxonomy — RESOLVED (requirement now satisfied with evidence), ACCEPTED-RISK (risk accepted with documented rationale and risk owner), WAIVED (requirement acknowledged as inapplicable to LLM-based implementation with documented rationale), ESCALATED (unresolvable by reviewer; escalated to user per H-31 with full context for user decision). No open item may remain in status OPEN at V&V Phase 3 exit; (d) CDR exit criteria met: skill ready for production use; (e) No unresolved items blocking production use |
| Failure Action | Return to nse-reviewer-001 with critique; revise and re-submit. If open items remain OPEN after 5 iterations: escalate to user per H-31 with full open item report including recommended disposition for each. |

### Execution Queue

| Group | Mode | Agent(s) | Dependency | Status |
|-------|------|----------|------------|--------|
| 0 | SEQUENTIAL | Pre-conditions check | None | READY |
| 1 | PARALLEL | eng-architect-001, red-lead-001 | Group 0 PASS | BLOCKED |
| 2 | SEQUENTIAL | adv-executor-001 | eng-architect-001 complete | BLOCKED |
| 3 | SEQUENTIAL | eng-lead-001 | QG-E1 PASS | BLOCKED |
| 4 | SEQUENTIAL | adv-scorer-001 | eng-lead-001 complete | BLOCKED |
| 5 | PARALLEL (Fan-Out) | eng-backend-001, eng-backend-002, eng-backend-003, eng-backend-004a, eng-backend-004b | QG-E2 PASS AND user approval checkpoint | BLOCKED |
| 6 | PARALLEL | adv-executor-002, adv-executor-003, adv-executor-004, adv-executor-005a, adv-executor-005b | Each eng-backend complete (per sub-agent) | BLOCKED |
| 7a | BARRIER | BARRIER-1 handoff document creation (3 directions: eng→red, red→eng, eng→vv) | ALL of Group 6 QGs PASS AND red-lead-001 complete | BLOCKED |
| 7b | SEQUENTIAL | adv-executor-barrier-1 (tournament review: 7 strategies, S-003 before S-002 per H-16, against each of the 3 handoff docs in sequence) | Group 7a complete (all 3 handoff docs exist) | BLOCKED |
| 8 | PARALLEL | eng-qa-001, red-recon-001, nse-requirements-001 | BARRIER-1 PASS (adv-executor-barrier-1 scores all 3 directions >= 0.93) | BLOCKED |
| 9 | PARALLEL | adv-executor-006, adv-executor-009, adv-executor-011 | Each of Group 8 complete (per agent) | BLOCKED |
| 10 | SEQUENTIAL | red-vuln-001 | QG-R2 PASS | BLOCKED |
| 11 | SEQUENTIAL | adv-executor-010 | red-vuln-001 complete | BLOCKED |
| 12 | SEQUENTIAL | eng-security-001 | **QG-E4 PASS only** (does NOT wait for QG-V1) | BLOCKED |
| 13 | SEQUENTIAL | adv-executor-007 | eng-security-001 complete | BLOCKED |
| 14 | SEQUENTIAL | nse-verification-001 | QG-E4 PASS AND QG-V1 PASS | BLOCKED |
| 15 | SEQUENTIAL | adv-executor-012 | nse-verification-001 complete | BLOCKED |
| 16a | BARRIER | BARRIER-2 handoff document creation (2 directions: eng→red, red→eng) | QG-E5 PASS AND QG-R3 PASS AND no-CRITICAL-vulns | BLOCKED |
| 16b | SEQUENTIAL | adv-executor-barrier-2 (tournament review: 7 strategies, S-003 before S-002 per H-16, against each of the 2 handoff docs in sequence) | Group 16a complete (both handoff docs exist) | BLOCKED |
| 17 | PARALLEL | eng-reviewer-001, red-exploit-001 | BARRIER-2 PASS (adv-executor-barrier-2 scores both directions >= 0.93) | BLOCKED |
| 18 | SEQUENTIAL | adv-executor-008 | eng-reviewer-001 complete | BLOCKED |
| 19a | BARRIER | BARRIER-3 handoff document creation (1 direction: all→vv CDR entrance package) | QG-E6 PASS AND red-exploit-001 complete AND QG-V2 PASS AND all 5 entrance criteria verified | BLOCKED |
| 19b | SEQUENTIAL | adv-executor-barrier-3 (tournament review: 7 strategies, S-003 before S-002 per H-16, against CDR entrance package handoff doc) | Group 19a complete (barrier-handoff.md exists) | BLOCKED |
| 20 | SEQUENTIAL | nse-reviewer-001 | BARRIER-3 PASS (adv-executor-barrier-3 scores CDR entrance package >= 0.93) | BLOCKED |
| 21 | SEQUENTIAL | adv-executor-013 | nse-reviewer-001 complete | BLOCKED |
| 22 | SEQUENTIAL | Workflow completion verification | QG-V3 PASS | BLOCKED |

---

## L2: Implementation Details

### State Schema (ORCHESTRATION.yaml Preview)

The machine-readable state file at `ORCHESTRATION.yaml` (sibling to this file) defines:

- `workflow.id`: `nuclear-sop-build-20260325-001`
- `workflow.status`: `PLANNED`
- `pipelines.eng.phases`: 6 phases with sub-agent isolation paths
- `pipelines.red.phases`: 4 phases
- `pipelines.vv.phases`: 3 phases (NEW)
- `barriers`: BARRIER-1, BARRIER-2, BARRIER-3 with bidirectional/tridirectional handoff paths
- `quality.criticality`: `C3`
- `quality.threshold`: `0.93` (all gates — upgraded from 0.92)
- `quality.required_strategies`: full C3 set at every gate
- `checkpoints`: CP-001 through CP-012 trigger points

### Dynamic Path Configuration

All artifact paths are dynamically constructed. No hardcoded pipeline names.

```
Base:        projects/PROJ-0039-nuclear-engineer/orchestration/nuclear-sop-build-20260325-001/
Pipeline:    {base}{pipeline_alias}/{phase_id}/{agent_id}/
Barrier:     {base}cross-pollination/{barrier_id}/{direction}/
```

**Resolved artifact paths (all relative to `projects/PROJ-0039-nuclear-engineer/`):**

| Agent | Artifact Path |
|-------|---------------|
| eng-architect-001 | `orchestration/nuclear-sop-build-20260325-001/eng/phase-1/eng-architect-001/secure-architecture-design.md` |
| adv-executor-001 | `orchestration/nuclear-sop-build-20260325-001/eng/phase-1/adv-executor-001/architecture-threat-review.md` |
| eng-lead-001 | `orchestration/nuclear-sop-build-20260325-001/eng/phase-2/eng-lead-001/implementation-plan.md` |
| adv-scorer-001 | `orchestration/nuclear-sop-build-20260325-001/eng/phase-2/adv-scorer-001/implementation-plan-score.md` |
| eng-backend-001 | `orchestration/nuclear-sop-build-20260325-001/eng/phase-3/eng-backend-001/implementation-review.md` (review output; skill files at `skills/nuclear-sop/`) |
| eng-backend-002 | `orchestration/nuclear-sop-build-20260325-001/eng/phase-3/eng-backend-002/implementation-review.md` |
| eng-backend-003 | `orchestration/nuclear-sop-build-20260325-001/eng/phase-3/eng-backend-003/implementation-review.md` |
| eng-backend-004a | `orchestration/nuclear-sop-build-20260325-001/eng/phase-3/eng-backend-004a/implementation-review.md` |
| eng-backend-004b | `orchestration/nuclear-sop-build-20260325-001/eng/phase-3/eng-backend-004b/implementation-review.md` |
| adv-executor-002 | `orchestration/nuclear-sop-build-20260325-001/eng/phase-3/adv-executor-002/backend-001-review.md` |
| adv-executor-003 | `orchestration/nuclear-sop-build-20260325-001/eng/phase-3/adv-executor-003/backend-002-review.md` |
| adv-executor-004 | `orchestration/nuclear-sop-build-20260325-001/eng/phase-3/adv-executor-004/backend-003-review.md` |
| adv-executor-005a | `orchestration/nuclear-sop-build-20260325-001/eng/phase-3/adv-executor-005a/backend-004a-review.md` |
| adv-executor-005b | `orchestration/nuclear-sop-build-20260325-001/eng/phase-3/adv-executor-005b/backend-004b-review.md` |
| BARRIER-1 (eng→red) | `orchestration/nuclear-sop-build-20260325-001/cross-pollination/barrier-1/eng-to-red/barrier-handoff.md` |
| BARRIER-1 (red→eng) | `orchestration/nuclear-sop-build-20260325-001/cross-pollination/barrier-1/red-to-eng/barrier-handoff.md` |
| BARRIER-1 (eng→vv) | `orchestration/nuclear-sop-build-20260325-001/cross-pollination/barrier-1/eng-to-vv/barrier-handoff.md` |
| eng-qa-001 | `orchestration/nuclear-sop-build-20260325-001/eng/phase-4/eng-qa-001/test-strategy.md` |
| adv-executor-006 | `orchestration/nuclear-sop-build-20260325-001/eng/phase-4/adv-executor-006/test-harness-review.md` |
| red-lead-001 | `orchestration/nuclear-sop-build-20260325-001/red/phase-1/red-lead-001/engagement-scope.md` |
| red-recon-001 | `orchestration/nuclear-sop-build-20260325-001/red/phase-2/red-recon-001/attack-surface-map.md` |
| adv-executor-009 | `orchestration/nuclear-sop-build-20260325-001/red/phase-2/adv-executor-009/recon-review.md` |
| red-vuln-001 | `orchestration/nuclear-sop-build-20260325-001/red/phase-3/red-vuln-001/vulnerability-report.md` |
| adv-executor-010 | `orchestration/nuclear-sop-build-20260325-001/red/phase-3/adv-executor-010/vuln-review.md` |
| eng-security-001 | `orchestration/nuclear-sop-build-20260325-001/eng/phase-5/eng-security-001/security-review.md` |
| adv-executor-007 | `orchestration/nuclear-sop-build-20260325-001/eng/phase-5/adv-executor-007/security-review-critique.md` |
| BARRIER-2 (eng→red) | `orchestration/nuclear-sop-build-20260325-001/cross-pollination/barrier-2/eng-to-red/barrier-handoff.md` |
| BARRIER-2 (red→eng) | `orchestration/nuclear-sop-build-20260325-001/cross-pollination/barrier-2/red-to-eng/barrier-handoff.md` |
| red-exploit-001 | `orchestration/nuclear-sop-build-20260325-001/red/phase-4/red-exploit-001/exploitation-methodology.md` |
| eng-reviewer-001 | `orchestration/nuclear-sop-build-20260325-001/eng/phase-6/eng-reviewer-001/compliance-verification.md` |
| adv-executor-008 | `orchestration/nuclear-sop-build-20260325-001/eng/phase-6/adv-executor-008/final-review-critique.md` |
| nse-requirements-001 | `orchestration/nuclear-sop-build-20260325-001/vv/phase-1/nse-requirements-001/requirements-traceability-matrix.md` |
| adv-executor-011 | `orchestration/nuclear-sop-build-20260325-001/vv/phase-1/adv-executor-011/req-trace-review.md` |
| nse-verification-001 | `orchestration/nuclear-sop-build-20260325-001/vv/phase-2/nse-verification-001/vv-plan.md` |
| adv-executor-012 | `orchestration/nuclear-sop-build-20260325-001/vv/phase-2/adv-executor-012/vv-plan-review.md` |
| BARRIER-3 (all→vv) | `orchestration/nuclear-sop-build-20260325-001/cross-pollination/barrier-3/all-to-vv/barrier-handoff.md` |
| adv-executor-barrier-1 | `orchestration/nuclear-sop-build-20260325-001/cross-pollination/barrier-1/quality-review/barrier-1-tournament-review.md` |
| adv-executor-barrier-2 | `orchestration/nuclear-sop-build-20260325-001/cross-pollination/barrier-2/quality-review/barrier-2-tournament-review.md` |
| adv-executor-barrier-3 | `orchestration/nuclear-sop-build-20260325-001/cross-pollination/barrier-3/quality-review/barrier-3-tournament-review.md` |
| nse-reviewer-001 | `orchestration/nuclear-sop-build-20260325-001/vv/phase-3/nse-reviewer-001/formal-technical-review.md` |
| adv-executor-013 | `orchestration/nuclear-sop-build-20260325-001/vv/phase-3/adv-executor-013/cdr-review-critique.md` |

**Skill output files (built by Phase 3 agents, NOT orchestration artifacts):**

| File | Agent | Location |
|------|-------|----------|
| `SKILL.md` | eng-backend-001 | `skills/nuclear-sop/SKILL.md` |
| `nuclear-sop-behavior-rules.md` | eng-backend-001 | `skills/nuclear-sop/rules/nuclear-sop-behavior-rules.md` |
| `sop-brief.md` | eng-backend-002 | `skills/nuclear-sop/agents/sop-brief.md` |
| `sop-brief.governance.yaml` | eng-backend-002 | `skills/nuclear-sop/agents/sop-brief.governance.yaml` |
| `PRE_JOB_BRIEF.template.md` | eng-backend-002 | `skills/nuclear-sop/templates/PRE_JOB_BRIEF.template.md` |
| `sop-executor.md` | eng-backend-003 | `skills/nuclear-sop/agents/sop-executor.md` |
| `sop-executor.governance.yaml` | eng-backend-003 | `skills/nuclear-sop/agents/sop-executor.governance.yaml` |
| `WORKFLOW_DEFINITION.template.md` | eng-backend-003 | `skills/nuclear-sop/templates/WORKFLOW_DEFINITION.template.md` |
| `PROCEDURE_STATE.template.yaml` | eng-backend-003 | `skills/nuclear-sop/templates/PROCEDURE_STATE.template.yaml` |
| `HOLD_POINT_LOG.template.md` | eng-backend-003 | `skills/nuclear-sop/templates/HOLD_POINT_LOG.template.md` |
| `sop-verifier.md` | eng-backend-004a | `skills/nuclear-sop/agents/sop-verifier.md` |
| `sop-verifier.governance.yaml` | eng-backend-004a | `skills/nuclear-sop/agents/sop-verifier.governance.yaml` |
| `sop-capture.md` | eng-backend-004b | `skills/nuclear-sop/agents/sop-capture.md` |
| `sop-capture.governance.yaml` | eng-backend-004b | `skills/nuclear-sop/agents/sop-capture.governance.yaml` |
| `POST_JOB_BRIEF.template.md` | eng-backend-004b | `skills/nuclear-sop/templates/POST_JOB_BRIEF.template.md` |

### Performance Metrics Framework (ENG Phase 4 Specification)

eng-qa-001 MUST instrument the test harness to measure all seven metrics. Each metric has a measurement method and an acceptance threshold that must be validated by adv-executor-006 as part of QG-E4.

| Metric ID | Metric Name | Measurement Method | Acceptance Threshold |
|-----------|-------------|-------------------|---------------------|
| PM-01 | STAR catch rate | Count STOP-WORK records in STAR REVIEW log for planted error-trap steps / total planted trap steps across all test runs | 100% for planted traps |
| PM-02 | STAR false positive rate | Count STOP-WORK on non-trap steps / total non-trap steps executed in test runs | <= 10% |
| PM-03 | OE entry schema completeness | Count mandatory fields present in each OE entry / total mandatory fields per OE schema across all OE entries generated during test | 100% (write blocked if missing field) |
| PM-04 | Prerequisite pass/fail detection | Count sop-brief STOP gates triggered on deliberately missing prerequisites / total deliberate missing-prerequisite test cases | 100% detection rate |
| PM-05 | QG-HOLD convergence | Record iteration count for each QG-HOLD to reach >= 0.93 pass across all test runs | <= 3 iterations for C2 workflows; <= 5 iterations for C3 workflows |
| PM-06 | GAP-09 behavioral baseline recording | Count canonical scenario baselines recorded in `skills/nuclear-sop/behavioral-baselines/` with baseline score | >= 3 scenario baselines recorded |
| PM-07 | Composition pattern validation | Count composition patterns (nuclear-sop wrapping another skill) demonstrated with correct hop accounting | >= 1 pattern validated in worked example |

**Measurement instrumentation requirements:**
- STAR catch rate (PM-01) and false positive rate (PM-02) require a test fixture that plants deliberate errors at known steps and records whether STAR REVIEW produces STOP-WORK at those steps.
- OE schema completeness (PM-03) requires a schema validator that checks each OE entry against the mandatory field list before write.
- PM-04 requires test cases with explicitly missing prerequisites and assertion that sop-brief halts.
- PM-05 requires a QG-HOLD harness that runs the adversarial cycle and records iteration count at each hold point.
- PM-06 and PM-07 require the GAP-09 baseline recording and composition example to be executed during Phase 4 as live test cases, not just documented.

### GAP-09 Behavioral Baseline Recording (ENG Phase 4 Specification)

The first STAR validation runs are canonical behavioral scenarios for GAP-09 (Behavioral Drift Monitoring). eng-qa-001 MUST:

1. Execute at least 3 distinct test scenarios through the full sop-executor STAR loop
2. Record each scenario definition in `skills/nuclear-sop/behavioral-baselines/{scenario-id}.md` with the fields: scenario name, workflow definition reference, step under test, expected STAR output, actual STAR output, baseline score (S-014), date recorded
3. These baselines become the reference corpus for GAP-09 periodic drift checking via `/adversary` (S-014 LLM-as-Judge) and `/schedule` (periodic trigger)

**Minimum scenario set:**

| Scenario | Description | Expected STAR Outcome |
|----------|-------------|----------------------|
| BS-001 | Nominal step with no error condition | PROCEED — no STOP-WORK |
| BS-002 | Step with planted classification error (wrong procedure use tag) | STOP-WORK — classification mismatch detected |
| BS-003 | Hold point activation at IV-HOLD with missing verification criteria | STOP-WORK — cannot verify; human escalation |

### Routing Registration Deliverables (ENG Phase 6 Specification)

eng-reviewer-001 MUST produce the following registration artifacts as part of ENG Phase 6 output. These are required deliverables for QG-E6 compliance.

| Deliverable | File | Content |
|-------------|------|---------|
| Trigger map row | Inline in `compliance-verification.md` Section: Registration | Full 5-column trigger map row per integration analysis `skill-integration-analysis.md` activation keywords table: detected keywords, negative keywords, priority 12, compound triggers, `/nuclear-sop` |
| CLAUDE.md update | Inline in `compliance-verification.md` Section: Registration | New row for Quick Reference skill table: `nuclear-sop` skill entry |
| AGENTS.md entries | Inline in `compliance-verification.md` Section: Registration | 4 new agent entries: sop-brief, sop-executor, sop-verifier, sop-capture with role and skill source |

**Implementation note:** The registration deliverables are written into `compliance-verification.md` as copy-ready content. Actual file edits to `mandatory-skill-usage.md`, `CLAUDE.md`, and `AGENTS.md` are performed by the user after QG-E6 PASS, not by eng-reviewer-001 during automated execution. This respects P-020 (user authority over framework configuration changes) while ensuring the content is validated by the quality gate before application.

### Self-Referential Test Harness Application

The /nuclear-sop skill is applied to its own test harness construction in ENG Phase 4. This is a key validation:

1. eng-qa-001 invokes /nuclear-sop skill to guide the test harness build
2. A WORKFLOW_DEFINITION is created for "Build Nuclear SOP Test Harness"
3. sop-brief generates the pre-job brief for the test harness construction procedure
4. sop-executor tracks execution of the test harness build steps
5. Hold points are placed at: test harness skeleton creation, STAR trap integration, A/B framework creation, behavioral bounds definition, PM instrumentation
6. sop-verifier validates at each hold point that the correct test harness component was built
7. sop-capture records OE from the test harness construction for the post-job brief
8. Evidence: execution logs show that /nuclear-sop agents behaved within defined bounds while guiding their own test harness construction; STAR catch rate and false positive rate (PM-01, PM-02) are measured during this self-referential run

This is not circular — the test harness tests whether agents behave deterministically; the skill guides the construction of that harness using the same procedural discipline the harness will verify.

### Checkpoint Strategy

| Checkpoint | Trigger | Recovery Point | Contents |
|------------|---------|----------------|----------|
| CP-001 | Pre-conditions verified | Start Group 1 (parallel pipelines) | Upstream artifact inventory |
| CP-002 | ENG Phase 1 + QG-E1 PASS | Start ENG Phase 2 | secure-architecture-design.md |
| CP-003 | ENG Phase 2 + QG-E2 PASS | Start ENG Phase 3 fan-out | implementation-plan.md |
| CP-004 | ENG Phase 3 ALL + all sub-QGs PASS + RED Phase 1 COMPLETE | BARRIER-1 sync | All 16 skill files + engagement-scope.md |
| CP-005 | BARRIER-1 PASS (all three directions) | Start ENG Phase 4 + RED Phase 2 + V&V Phase 1 in parallel | All barrier handoff docs |
| CP-006a | QG-E4 PASS | Start ENG Phase 5 (eng-security-001) — QG-E4 PASS is the ONLY condition required for ENG Phase 5; does NOT wait for QG-V1 | test-strategy.md |
| CP-006b | QG-E4 PASS AND QG-V1 PASS | Start V&V Phase 2 (nse-verification-001) — both QGs must pass | test-strategy.md + requirements-traceability-matrix.md |
| CP-007 | ENG Phase 5 QG-E5 PASS AND RED Phase 3 QG-R3 PASS | BARRIER-2 sync | security-review.md + vulnerability-report.md |
| CP-008 | BARRIER-2 PASS (both directions) | Start ENG Phase 6 + RED Phase 4 in parallel | Both barrier handoff docs |
| CP-009 | QG-V2 PASS | V&V Phase 2 complete; ready for BARRIER-3 | vv-plan.md |
| CP-010 | ENG Phase 6 QG-E6 PASS AND RED Phase 4 complete AND QG-V2 PASS | BARRIER-3 sync | compliance-verification.md + exploitation-methodology.md + vv-plan.md |
| CP-011 | BARRIER-3 PASS | Start V&V Phase 3 (CDR) | CDR entrance package handoff doc |
| CP-012 | QG-V3 PASS | Workflow complete | formal-technical-review.md |

### Criticality Assessment

| Factor | Assessment | Justification |
|--------|-----------|---------------|
| Reversibility | > 1 day | New skill architecture creates 16+ files; significant rework if wrong |
| File scope | 16+ files | Agent defs, governance YAML, templates, rules, skill root — all new |
| Impact | API/cross-module | New skill exposes public API; affects all future procedure-based work; routing registration modifies framework configuration files |
| **Overall** | **C3 (Significant)** | All three factors point to C3; no AE-001 (no constitution touch); AE-003 applies |
| AE triggers | AE-002 watch | If nuclear-sop-behavior-rules.md is placed in `.context/rules/` — would trigger auto-C3; MUST place in skills/nuclear-sop/rules/ instead |
| Auto-escalation check | AE-003 confirmed | ADR-001 was a new ADR in prior workflow; this workflow implements it |

### Adversarial Strategy Set (C3 — Full Set at Every Gate)

Per `quality-enforcement.md` criticality levels, ALL quality gates in this workflow run the FULL C3 required set:

| Tier | Strategies |
|------|-----------|
| Required (C2 baseline) | S-007 (Constitutional AI Critique), S-002 (Devil's Advocate), S-014 (LLM-as-Judge) |
| Required (C3 additions) | S-004 (Pre-Mortem Analysis), S-012 (FMEA), S-013 (Inversion Technique) |
| H-16 enforcement | S-003 (Steelman) MUST be applied before S-002 (Devil's Advocate) at every critique cycle |
| Optional (C3) | S-001 (Red Team Analysis), S-010 (Self-Refine), S-011 (Chain-of-Verification) |

**Barrier tournament review:** At BARRIER-1, BARRIER-2, and BARRIER-3, all 7 strategies are applied against each handoff document. This is tournament-style execution: each strategy produces a critique, the critiques are synthesized, and the handoff document is revised until the combined score reaches >= 0.93. Strategy count clarification: the C3 REQUIRED set is 6 strategies (S-007, S-002, S-014, S-004, S-012, S-013). S-003 (Steelman) is applied in addition per H-16 ordering rule — S-003 MUST precede S-002 at every critique cycle. Total strategies applied at every gate: **7** (6 C3 required + S-003 per H-16). When this document states "6-strategy review" it refers to the 6 C3 required strategies; the operational total is 7 because S-003 is always prepended per H-16.

### Recovery Strategies

| Failure Mode | Recovery Action |
|---|---|
| Upstream artifact missing (synthesis spec, ADR-001) | Halt; report to user; do not proceed without all pre-condition artifacts |
| QG-E1 fails after 5 iterations | Escalate to user with best-effort threat model; document gaps explicitly |
| QG-E3 sub-agent fails for H-34 schema validation | Return specific schema violations to eng-backend; fix and re-submit |
| BARRIER-1 fails (quality < 0.93) | Revise handoff document; retry with full C3 strategy tournament; max 5 retries per direction |
| ENG Phase 4 PM instrumentation incomplete | Document which metrics could not be instrumented; complete harness with available metrics; flag gap in QG-E4 failure report |
| ENG Phase 4 test harness cannot apply /nuclear-sop to itself | Document failure mode; complete harness without self-referential validation; flag as partial |
| GAP-09 baseline recording fails (< 3 scenarios) | Execute additional test scenarios until 3 baselines recorded; if still failing after 5 attempts, document as a known gap with roadmap item |
| QG-R3 finds severity-critical vulnerability | Halt BARRIER-2; return vulnerability to eng-security for immediate remediation before proceeding |
| BARRIER-2 fails | Same as BARRIER-1 recovery |
| V&V Phase 1 trace matrix has unresolvable gaps | Escalate to user; nse-requirements-001 documents which patterns cannot be traced and why; proceed only with user approval |
| V&V Phase 2 cannot define verification method for a requirement | Flag as open item; document proposed disposition; nse-reviewer-001 must disposition in V&V Phase 3 |
| BARRIER-3 entrance criteria not met | Identify blocking criterion; resolve in the responsible phase; re-run affected QG; re-trigger BARRIER-3 sync |
| QG-V3 finds undispositioned open items | Attempt disposition in nse-reviewer-001 iteration; if open items remain after 5 iterations, escalate to user with full open item report |
| Context window fills mid-phase | AE-006 graduated escalation; checkpoint to file; resume next session |
| Quality gate ceiling reached (5 iterations, no PASS) | Halt; present best-effort output with explicit gap documentation to user |
| H-34/H-35 schema validation fails in Phase 6 | Return to responsible eng-backend; fix specific violations; targeted re-validation |
| Registration deliverables fail QG-E6 | Return to eng-reviewer-001; revise routing registration content until trigger map row, CLAUDE.md entry, and AGENTS.md entries are complete and accurate |

---

## Execution Constraints

### Hard Constraints (Jerry Constitution)

| Constraint | ID | Enforcement |
|---|---|---|
| Single agent nesting | P-003 | Orchestrator to worker only; no recursive subagents from any eng, red, or vv agent |
| File persistence | P-002 | All state to filesystem at defined paths; ORCHESTRATION.yaml updated after every phase |
| No deception | P-022 | Transparent reasoning; accurate confidence scores; no suppressed findings |
| User authority | P-020 | User approves any destructive operations; halt on severity-critical vulnerabilities; user applies registration edits after QG-E6 |
| **User approval checkpoint before Phase 3 fan-out** | **P-020** | **Before ENG Phase 3 fan-out execution (Group 5): user MUST confirm that the implementation plan (E2 output) is acceptable and authorize the creation of 16 new skill files in `skills/nuclear-sop/`. This approval gate is placed between QG-E2 PASS and Group 5 execution. See Group 5 dependency in Execution Queue.** |
| UV-only Python | H-05 | Any test harness code uses uv run; never python/pip |

### HARD Rule Scope for Skill Files

All agent definitions created in ENG Phase 3 MUST comply with H-34 and H-35:

- H-34: Dual-file architecture (`.md` + `.governance.yaml`); only official Claude Code fields in frontmatter; governance schema validated against `docs/schemas/agent-governance-v1.schema.json`
- H-35: Constitutional triplet (P-003, P-020, P-022) in `constitution.principles_applied`; minimum 3 `forbidden_actions`; worker agents MUST NOT include `Task` in tools
- **AE-002 file placement constraint:** `nuclear-sop-behavior-rules.md` MUST be placed at `skills/nuclear-sop/rules/nuclear-sop-behavior-rules.md`, NOT at `.context/rules/`. Placement in `.context/rules/` would trigger AE-002 auto-C3 escalation on all subsequent sessions. Verify placement before BARRIER-1 sync.

### Soft Constraints

| Constraint | Value | Rationale |
|------------|-------|-----------|
| Max quality gate iterations | 5 per gate | RT-M-010 C3 ceiling (upgraded from 3 in v1.0) |
| Min quality gate iterations | 3 per gate | H-14: minimum 3 creator-critic-revision cycles REQUIRED before acceptance, even if threshold passed in fewer |
| Quality threshold (all gates) | >= 0.93 | C3 criticality at elevated threshold (upgraded from 0.92 in v1.0) |
| Full C3 strategy set at every gate | S-003, S-007, S-002, S-014, S-004, S-012, S-013 | Requirement 3: full strategy set at every phase exit |
| H-16 enforcement | S-003 before S-002 at every critique cycle | Steelman before Devil's Advocate; non-negotiable per H-16 |
| Max routing hops | 3 | H-36 circuit breaker |
| Fan-out sub-agents | 5 | ENG Phase 3 only (001, 002, 003, 004a, 004b); all others sequential |
| Barrier quality threshold | >= 0.93 all directions | Cross-pollination integrity; tournament-style review |

---

## Success Criteria

### Pre-Conditions (Barrier 0 — must be PASS before starting)

| Criterion | Validation |
|-----------|------------|
| Phase 4 synthesis spec exists | File present at defined path; QG4 score 0.922 recorded |
| ADR-001 exists | File present at defined path; QG3 score 0.933 recorded |
| Pattern extraction exists | File present at defined path; QG2 score 0.914 recorded |
| Nuclear survey exists | File present at defined path; QG1 score 0.920 recorded |
| Integration analysis exists | File present at research/skill-integration-analysis.md; quality score 0.91 (iteration 2 PASS at 0.90 threshold) recorded |
| Upstream quality scores reviewed | Confirm all recorded quality gate scores match Upstream Dependencies table. Integration analysis (0.91) is below the build threshold (0.93) — explicitly ACCEPTED-RISK: the integration analysis informs routing registration content but does not define agent behavior; any routing decisions derived from it are validated independently at QG-E6. |
| `skills/nuclear-sop/` directory does not exist | Clean build target confirmed |

### ENG Phase 3 Exit Criteria (All sub-agents required)

| Criterion | Validation |
|-----------|------------|
| All 16 skill files created | File inventory check against synthesis spec Section 1.2 file structure |
| All agent defs pass H-34 schema | `docs/schemas/agent-governance-v1.schema.json` validation PASS for all 4 agent pairs |
| Constitutional triplet present in all governance.yaml | P-003, P-020, P-022 in all `constitution.principles_applied` |
| No hardcoded pipeline names | Grep `skills/nuclear-sop/` for hardcoded pipeline names — zero matches |
| All sub-agent QGs PASS | adv-executor-002 through adv-executor-005 all score >= 0.93 |

### Barrier 1 Exit Criteria

| Criterion | Validation |
|-----------|------------|
| ENG → RED handoff complete | `barrier-1/eng-to-red/barrier-handoff.md` exists; all 16 skill file paths listed |
| RED → ENG handoff complete | `barrier-1/red-to-eng/barrier-handoff.md` exists; attack hypotheses documented |
| ENG → V&V handoff complete | `barrier-1/eng-to-vv/barrier-handoff.md` exists; synthesis spec + skill file paths listed |
| All directions score >= 0.93 | Tournament-style 7-strategy scoring applied to each handoff document by adv-executor-barrier-1 (Groups 7a/7b in Execution Queue) |
| RED Phase 2 unblocked | red-recon-001 has access to built skill files |
| ENG Phase 4 informed | eng-qa-001 has attack surface hypotheses for test trap design |
| V&V Phase 1 unblocked | nse-requirements-001 has built skill files for traceability analysis |

### Barrier 2 Exit Criteria

| Criterion | Validation |
|-----------|------------|
| ENG → RED handoff complete | `barrier-2/eng-to-red/barrier-handoff.md` exists; security findings enumerated |
| RED → ENG handoff complete | `barrier-2/red-to-eng/barrier-handoff.md` exists; vulnerability report paths listed |
| Both directions score >= 0.93 | Tournament-style 7-strategy scoring applied to both handoff documents by adv-executor-barrier-2 (Groups 16a/16b in Execution Queue) |
| Severity-critical vulnerabilities resolved before proceeding | None of the red-vuln-001 findings are severity-critical and unresolved |

### Barrier 3 Exit Criteria

| Criterion | Validation |
|-----------|------------|
| All-to-V&V CDR entrance package complete | `barrier-3/all-to-vv/barrier-handoff.md` exists; all 16 skill files listed; all QG scores recorded |
| Package scores >= 0.93 | Tournament-style 7-strategy scoring applied to CDR entrance package by adv-executor-barrier-3 (Groups 19a/19b in Execution Queue) |
| Entrance criteria verified | All 5 entrance criteria met (16 files exist, all QGs passed, test harness complete, registration written, no CRITICAL vulns) |
| V&V Phase 3 unblocked | nse-reviewer-001 has complete CDR entrance package |

### Workflow Completion Criteria

| Criterion | Validation |
|-----------|------------|
| All 16 skill files exist and pass schema validation | File inventory + H-34 schema check |
| ENG Phase 6 compliance matrix complete | All synthesis spec Section 3 ACs are mapped to pass/fail evidence |
| Red team exploitation methodology complete | `exploitation-methodology.md` exists; all priority vulnerabilities addressed |
| Test harness applied self-referentially | /nuclear-sop application logs present in Phase 4 output |
| All 7 performance metrics measured | PM-01 through PM-07 recorded in test-strategy.md with pass/fail against thresholds |
| >= 3 GAP-09 behavioral baselines recorded | Scenario files exist in `skills/nuclear-sop/behavioral-baselines/` |
| Requirements traceability complete | All 14 nuclear patterns traced in requirements-traceability-matrix.md |
| V&V plan executed | All verification methods executed and pass/fail recorded in formal-technical-review.md |
| Formal technical review complete | `formal-technical-review.md` exists; all open items dispositioned |
| Registration deliverables written | Trigger map row, CLAUDE.md entry, AGENTS.md entries in compliance-verification.md |
| CP-012 checkpoint created | Workflow complete state persisted to ORCHESTRATION.yaml |

---

## Risk Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| H-34 schema validation fails for agent defs | MEDIUM | HIGH | eng-lead-001 plans schema compliance in Phase 2; eng-backend agents validate against schema before QG submission |
| Phase 3 fan-out produces inconsistent agent styles | MEDIUM | MEDIUM | Implementation plan (Phase 2) defines style standards; QG-E3 reviews consistency |
| BARRIER-1 handoff lacks sufficient detail for red-team | MEDIUM | HIGH | Handoff template specifies all 16 file paths + role descriptions; tournament-style scoring targets completeness dimension |
| BARRIER-1 handoff lacks sufficient detail for V&V | MEDIUM | HIGH | eng-to-vv direction requires synthesis spec reference + all skill file paths; nse-requirements-001 inputs defined explicitly |
| Red-team finds severity-critical vulnerabilities | LOW | CRITICAL | Recovery strategy halts BARRIER-2 until resolution; eng-security must address before proceeding |
| Self-referential test harness application fails | MEDIUM | MEDIUM | Fallback: complete harness without self-referential validation; document as gap; flag to user |
| Performance metrics PM-01 or PM-02 cannot be instrumented | MEDIUM | HIGH | eng-lead-001 Phase 2 plans metric instrumentation; if instrumentation not feasible, flag in Phase 2 before fan-out begins |
| GAP-09 baseline recording produces < 3 scenarios | LOW | MEDIUM | Phase 4 plan allocates time for at least 5 scenario runs; 3 is the minimum acceptable |
| Context window fills during Phase 3 fan-out | HIGH | MEDIUM | Each sub-agent runs in isolated context (Task tool); AE-006 monitoring per sub-agent |
| Synthesis spec ambiguity on file content | MEDIUM | HIGH | eng-lead-001 Phase 2 resolves ambiguities before fan-out; create file content specs for each eng-backend |
| V&V Phase 1 traceability has gaps (patterns not traceable) | MEDIUM | HIGH | nse-requirements-001 documents gaps; user approves disposition before proceeding; gaps become formal open items in V&V Phase 2 |
| V&V Phase 3 CDR finds blocking open items | LOW | HIGH | V&V Phase 2 pre-dispositions open items where possible; BARRIER-3 entrance criteria include open item review; QG-V3 has 5 iterations |
| Upgraded threshold (0.93 vs 0.92) causes iteration ceiling exhaustion | MEDIUM | MEDIUM | Max iterations increased to 5 (from 3) for all gates; pre-mortem analysis in QG-E1 identifies likely problem areas early |
| Routing registration content conflicts with existing trigger map | LOW | HIGH | integration analysis already defines the trigger map row; nse-reviewer-001 validates no collisions in V&V Phase 3 |
| Barrier quality gate fails for all directions | LOW | HIGH | Max 5 iterations; tournament-style review provides more granular critique to guide revision; if still failing, escalate to user |
| sop-verifier and sop-capture scope overload (previously eng-backend-004) | LOW | MEDIUM | MITIGATED in v2.1.0: split into eng-backend-004a (sop-verifier + governance yaml) and eng-backend-004b (sop-capture + governance yaml + POST_JOB_BRIEF template). Both run in parallel within Phase 3 fan-out; each has its own adv-executor critic. Scope overload risk reduced to LOW by structural split. |
| QG-E5 security review finds prompt injection in sop-executor | MEDIUM | HIGH | STRIDE threat model (Phase 1) flags this vector; eng-security specifically targeted at sop-executor prompt boundaries |

---

## Resumption Context

### Current Execution State (as of 2026-03-25)

```
WORKFLOW STATUS AS OF 2026-03-25 (v2.0 — Three-Pipeline Architecture)
=======================================================================

Plan version upgraded from 1.0 to 2.0. No execution has begun.
All phases reflect the expanded scope.

Pre-conditions (Barrier 0): READY (all upstream artifacts confirmed; integration analysis confirmed)

PIPELINE: eng (Engineering)
  Phase 1 (Architecture & Threat Model):   PENDING
  Phase 2 (Implementation Planning):       BLOCKED (pending QG-E1 PASS)
  Phase 3 (Implementation Fan-Out):        BLOCKED (pending QG-E2 PASS)
  Phase 4 (Test Harness & QA + Metrics):   BLOCKED (pending BARRIER-1 PASS)
  Phase 5 (Security Code Review):          BLOCKED (pending QG-E4 PASS only — does NOT depend on QG-V1)
  Phase 6 (Final Review Gate + Reg.):      BLOCKED (pending BARRIER-2 PASS)

PIPELINE: red (Red Team)
  Phase 1 (Engagement Scope):              PENDING
  Phase 2 (Reconnaissance):               BLOCKED (pending BARRIER-1 PASS)
  Phase 3 (Vulnerability Analysis):        BLOCKED (pending QG-R2 PASS)
  Phase 4 (Exploitation Methodology):      BLOCKED (pending BARRIER-2 PASS)

PIPELINE: vv (V&V — NEW)
  Phase 1 (Requirements Traceability):     BLOCKED (pending BARRIER-1 PASS)
  Phase 2 (V&V Plan):                      BLOCKED (pending QG-E4 PASS + QG-V1 PASS)
  Phase 3 (Formal Technical Review / CDR): BLOCKED (pending BARRIER-3 PASS)

Quality Gates:
  QG-E1 (Architecture Threat Review):        PENDING  [threshold: 0.93, max: 5 iters]
  QG-E2 (Implementation Plan Review):        PENDING  [threshold: 0.93, max: 5 iters]
  QG-E3a through QG-E3d (Implementation):    PENDING  [threshold: 0.93, max: 5 iters each]
  QG-E4 (Test Harness + Metrics Review):     PENDING  [threshold: 0.93, max: 5 iters]
  QG-E5 (Security Review):                   PENDING  [threshold: 0.93, max: 5 iters]
  QG-E6 (Final Compliance + Registration):   PENDING  [threshold: 0.93, max: 5 iters]
  QG-R2 (Attack Surface Review):             PENDING  [threshold: 0.93, max: 5 iters]
  QG-R3 (Vulnerability Report Review):       PENDING  [threshold: 0.93, max: 5 iters]
  QG-V1 (Requirements Traceability Review):  PENDING  [threshold: 0.93, max: 5 iters]
  QG-V2 (V&V Plan Review):                   PENDING  [threshold: 0.93, max: 5 iters]
  QG-V3 (Formal Technical Review):           PENDING  [threshold: 0.93, max: 5 iters]

Sync Barriers:
  BARRIER-1 (After ENG-P3 + RED-P1):  PENDING  [3 directions; threshold: 0.93; adv-executor-barrier-1 assigned (Group 7b)]
  BARRIER-2 (After ENG-P5 + RED-P3):  PENDING  [2 directions; threshold: 0.93; adv-executor-barrier-2 assigned (Group 16b)]
  BARRIER-3 (After E6 + R4 + V2):     PENDING  [1 direction (all→vv); threshold: 0.93; adv-executor-barrier-3 assigned (Group 19b)]

Checkpoints:
  CP-001 through CP-012: NOT YET CREATED

Overall Progress: 0%
```

### Next Actions

1. Update ORCHESTRATION.yaml to reflect v2.0 three-pipeline architecture (V&V pipeline added, thresholds upgraded to 0.93, max iterations set to 5, BARRIER-3 added, CP-009 through CP-012 added).
2. Verify pre-conditions: confirm all five upstream research artifacts exist at their defined paths. Confirm `skills/nuclear-sop/` does not exist.
3. Execute ENG Phase 1 (eng-architect-001) and RED Phase 1 (red-lead-001) in parallel. These have no dependencies on each other and no dependency on V&V.
4. Execute adv-executor-001 against eng-architect-001 output. Apply full C3 strategy set with S-003 before S-002. Threshold >= 0.93.
5. If QG-E1 PASS: create CP-002. Proceed to ENG Phase 2 (eng-lead-001). ENG Phase 2 implementation plan MUST include all 7 PM instrumentation requirements.
6. RED Phase 1 has no quality gate. Once red-lead-001 produces engagement-scope.md, RED Phase 1 is COMPLETE.
7. After QG-E2 PASS (CP-003): execute ENG Phase 3 fan-out — all four eng-backend agents in parallel.
8. Once all Phase 3 QGs pass AND RED Phase 1 is complete: execute BARRIER-1 sync (three directions: eng→red, red→eng, eng→vv). Create CP-004.
9. After BARRIER-1 PASS (CP-005): execute ENG Phase 4, RED Phase 2, and V&V Phase 1 in parallel.
10. After QG-E4 PASS (CP-006 partial): execute ENG Phase 5 (eng-security-001) immediately — ENG Phase 5 depends only on QG-E4 PASS and does NOT wait for QG-V1. After QG-E4 PASS AND QG-V1 PASS (CP-006 full): execute V&V Phase 2 (nse-verification-001). These two events may trigger at different times. ENG Phase 5 and V&V Phase 2 run independently once each starts; neither blocks the other.
11. After BARRIER-2 PASS (CP-008): execute ENG Phase 6 and RED Phase 4 in parallel. V&V Phase 2 continues independently.
12. After QG-E6, RED Phase 4 complete, and QG-V2 PASS (CP-010): execute BARRIER-3 sync.
13. After BARRIER-3 PASS (CP-011): execute V&V Phase 3 (nse-reviewer-001).
14. If QG-V3 PASS (CP-012): workflow complete. Present registration deliverables to user for manual application.

---

## Revision History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 2.0 | 2026-03-25 | orch-planner v2.2.0 | Initial three-pipeline architecture; V&V pipeline added; threshold upgraded to 0.93; 7 performance metrics; GAP-09 baselines; routing registration deliverables |
| 2.1.0 | 2026-03-25 | orch-planner | RR-01 through RR-07 applied per C3 critique (0.836). Barrier executors assigned, Phase 5 dependency fixed, strategy count reconciled, CDR taxonomy added, V&V vocabulary defined, eng-backend-004 split, constitutional gates surfaced. |
| 2.2.0 | 2026-03-26 | manual | RF-01 through RF-03 applied per iteration 2 rescore (0.902). L0 upstream quality claims corrected to distinguish gated vs. non-gated artifacts. Barrier 0 pre-conditions now verify upstream quality scores with explicit ACCEPTED-RISK for integration analysis. P-043 unverifiable label removed from disclaimer. |
| 2.1.0 | 2026-03-25 | orch-planner v2.2.0 | Revised per ps-critic C3 critique (0.836 → target >= 0.93). RR-01 through RR-07 addressed: (RR-01) added adv-executor-barrier-1/2/3 to Execution Queue Groups 7b/16b/19b; (RR-02) fixed ENG Phase 5 start condition — depends on QG-E4 PASS only, not QG-V1; (RR-03) reconciled 6/7 strategy count — 7 total (6 C3 required + S-003 per H-16); (RR-04) added CDR disposition taxonomy to QG-V3 (RESOLVED/ACCEPTED-RISK/WAIVED/ESCALATED); (RR-05) added LLM behavioral verification method vocabulary to QG-V2 (BEHAVIORAL-SAMPLE/TRACE-INSPECTION/METRIC-REFERENCE/STRUCTURAL-ANALYSIS); (RR-06) split eng-backend-004 into 004a (sop-verifier) and 004b (sop-capture + POST_JOB_BRIEF); (RR-07) added user approval gate (P-020) before Phase 3 fan-out, H-14 minimum iteration count to Soft Constraints, AE-002 constraint to HARD Rule Scope. |

---

## Disclaimer

This orchestration plan was generated by the orch-planner agent (v2.2.0) on 2026-03-25. Version 2.0 of this plan expands the original two-pipeline architecture to three pipelines by adding Pipeline C (V&V via /nasa-se), upgrades all quality gates to C3 at the 0.93 threshold with the full six-strategy required set, adds a seven-metric performance framework to ENG Phase 4, adds GAP-09 behavioral baseline recording, adds three sync barriers (BARRIER-3), and adds routing registration deliverables to ENG Phase 6.

Human review is recommended before execution begins, particularly to verify: (a) the V&V phase assignments and CDR entrance criteria are appropriate; (b) the seven performance metrics are measurable with the planned test harness; (c) the registration deliverables content matches the intended routing behavior; and (d) the upgraded 0.93 threshold is appropriate given the project timeline.

This plan does not constitute official guidance on nuclear engineering practices, security testing methodology, NASA systems engineering methodology, or software engineering standards. All implementation decisions derive from the prior research workflow (`nuclear-sop-research-20260319-001`) and integration analysis (`research/skill-integration-analysis.md`). Execution of this plan will create files in `skills/nuclear-sop/` and (upon user application of registration deliverables) modify `mandatory-skill-usage.md`, `CLAUDE.md`, and `AGENTS.md` in the Jerry framework.

*Disclaimer: This document was produced by the orch-planner agent as part of an automated orchestration planning process. It is NOT official NASA guidance, nuclear industry standards, or safety-critical procedure documentation. All references to nuclear engineering patterns are analytical abstractions derived from open literature for software framework design purposes only.*
