# FEAT-036-001 Test Harness Implementation: Orchestration Plan

> **Document ID:** PROJ-036-ORCH-PLAN
> **Workflow ID:** harness-impl-20260306-001
> **Feature:** FEAT-036-001 — Test Harness Implementation
> **Date:** 2026-03-06
> **Status:** PLANNED
> **Criticality:** C4 (Critical — irreversible architecture, 67 agent definitions affected)
> **Quality Threshold:** >= 0.94 per-stream adversarial score (Tier 1); >= 0.95 at barrier gates (Tier 2)
> **Source ADR:** ADR-001 (PROJ-035, Four-Layer Composite Test Harness Architecture) (ACCEPTED)

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Workflow Overview](#l0-workflow-overview) | Summary for stakeholders |
| [L1: Technical Plan](#l1-technical-plan) | Workflow diagram, group definitions, phase assignments, agents, barriers |
| [L2: Implementation Details](#l2-implementation-details) | State schema, path configuration, artifact registry, recovery strategies |
| [Quality Gate Definitions](#quality-gate-definitions) | Criticality assessment, C4 strategies, per-stream and barrier thresholds |
| [Output Map](#output-map) | Complete mapping of all artifacts by group |
| [Constraints](#constraints) | NPT-013 execution constraints |
| [Disclaimer](#disclaimer) | P-043 mandatory disclaimer |

---

## L0: Workflow Overview

This workflow implements the Four-Layer Composite Test Harness for the Jerry Framework, as specified by ADR-001 (ACCEPTED 2026-03-06). The harness enables safe prompt refactoring and regression detection across all 67 agent definitions. Today, no automated mechanism exists to determine whether a prompt change caused a quality regression — this implementation closes that gap.

The pipeline is organized into eight execution groups. Four parallel work streams run first: requirements derivation, system design with threat modeling, baseline capture protocol generation, and behavioral contract specification. Each of these creator streams now includes an embedded adversarial review cycle at >= 0.94 before the stream's output is eligible for the barrier gate. These four streams then converge at a C4 adversarial quality gate (Barrier 1) — which now functions as a cross-deliverable consistency check — before any implementation begins, ensuring the architectural foundation is sound. Five parallel implementation streams follow, each with the same embedded adversarial review cycle, before converging at Barrier 2. Security assessment, verification, and test development run in parallel with their own per-stream quality cycles before a third barrier gate. Final engineering review and cross-synthesis run in parallel before the dual final gate: an adversarial quality score and a NASA SE technical review, both of which must pass before the human reviews the complete implementation package.

The outcome is a production-ready, statistically rigorous, security-reviewed test harness with full requirements traceability, V&V evidence, and 90% test coverage — all backed by a two-tier C4-grade adversarial review chain: per-stream adversarial cycles ensure individual quality, and barrier gates ensure cross-deliverable consistency.

---

## L1: Technical Plan

### Workflow Diagram (ASCII)

```
PROJ-036 / FEAT-036-001: Four-Layer Composite Test Harness Implementation
Workflow ID: harness-impl-20260306-001
Source ADR: ADR-001-test-harness-architecture.md (ACCEPTED)
Pattern: Fan-Out -> Gate -> Fan-Out -> Gate -> Fan-Out -> Gate -> Fan-Out -> Dual Gate + Human
Quality Model: Two-Tier (per-stream >= 0.94 + barrier consistency >= 0.95)
=========================================================================================

 GROUP 1: PARALLEL FOUNDATIONS (Fan-Out, 4 concurrent streams)
 Each stream includes an embedded adversarial review cycle before barrier eligibility.
 ═══════════════════════════════════════════════════════════════════════════════════
 ┌─────────────────────┐ ┌─────────────────────┐ ┌─────────────────────┐ ┌─────────────────────┐
 │     STREAM 1A       │ │     STREAM 1B       │ │     STREAM 1C       │ │     STREAM 1D       │
 │  nse-requirements   │ │  eng-architect      │ │  eng-qa             │ │  nse-requirements   │
 │                     │ │  nse-architecture   │ │                     │ │                     │
 │  Requirements       │ │  eng-lead           │ │  Baseline           │ │  Behavioral         │
 │  Derivation         │ │                     │ │  Generation         │ │  Contracts          │
 │  from ADR-001       │ │  System Design      │ │  Protocol           │ │                     │
 │                     │ │  + Threat Model     │ │  + Prompts          │ │  Structural         │
 │  Functional         │ │                     │ │                     │ │  Invariants         │
 │  Interface          │ │  Hexagonal          │ │  5 agents           │ │  Quality Bounds     │
 │  Acceptance         │ │  Architecture       │ │  3-5 prompts        │ │  MR Tolerances      │
 │  FMEA reqs          │ │  STRIDE             │ │  N=30 protocol      │ │  Reg Thresholds     │
 │         │           │ │         │           │ │         │           │ │         │           │
 │  S-010 Self-Review  │ │  S-010 Self-Review  │ │  S-010 Self-Review  │ │  S-010 Self-Review  │
 │         │           │ │         │           │ │         │           │ │         │           │
 │  ┌─────────────┐    │ │  ┌─────────────┐    │ │  ┌─────────────┐    │ │  ┌─────────────┐    │
 │  │ adv-scorer  │    │ │  │ adv-scorer  │    │ │  │ adv-scorer  │    │ │  │ adv-scorer  │    │
 │  │ adv-executor│    │ │  │ adv-executor│    │ │  │ adv-executor│    │ │  │ adv-executor│    │
 │  │ >= 0.94     │    │ │  │ >= 0.94     │    │ │  │ >= 0.94     │    │ │  │ >= 0.94     │    │
 │  │ min 3/max 5 │    │ │  │ min 3/max 5 │    │ │  │ min 3/max 5 │    │ │  │ min 3/max 5 │    │
 │  └──────┬──────┘    │ │  └──────┬──────┘    │ │  └──────┬──────┘    │ │  └──────┬──────┘    │
 │         │ PASS      │ │         │ PASS      │ │         │ PASS      │ │         │ PASS      │
 └─────────┼───────────┘ └─────────┼───────────┘ └─────────┼───────────┘ └─────────┼───────────┘
           │                       │                       │                       │
           │ harness-              │ system-               │ baselines/            │ contracts/
           │ requirements.md       │ design.md             │ protocol.md           │ behavioral-
           │                       │                       │ schemas/              │ contracts.md
           │                       │                       │ prompts/              │ per-agent/
           └───────────────────────┴────────────┬──────────┴───────────────────────┘
                                                │ (all 4 streams PASS per-stream >= 0.94)
                                                ▼
                             ╔══════════════════════════════════════════════╗
                             ║    BARRIER 1 / GROUP 2                       ║
                             ║    C4 Adversarial Quality Gate               ║
                             ║    (Cross-Deliverable Consistency Check)     ║
                             ║                                              ║
                             ║  Agents: adv-scorer, adv-executor            ║
                             ║  All 10 C4 strategies applied                ║
                             ║  Focus: are all 4 outputs internally         ║
                             ║  consistent with each other?                 ║
                             ║  Threshold: >= 0.95 each                     ║
                             ║  Max 5 iterations per deliverable            ║
                             ║                                              ║
                             ║  Precondition: ALL 4 streams at >= 0.94     ║
                             ║  ALL 4 MUST PASS consistency check           ║
                             ╚═══════════════════╤══════════════════════════╝
                                                 │ (all 4 PASS >= 0.95)
                                                 ▼

 GROUP 3: PARALLEL IMPLEMENTATION (Fan-Out, 5 concurrent streams)
 Each stream includes an embedded adversarial review cycle before barrier eligibility.
 ════════════════════════════════════════════════════════════════════════════════════
 ┌────────────────────┐ ┌────────────────────┐ ┌────────────────────┐ ┌────────────────────┐ ┌────────────────────┐
 │    STREAM 3A       │ │    STREAM 3B       │ │    STREAM 3C       │ │    STREAM 3D       │ │    STREAM 3E       │
 │   eng-backend      │ │   eng-backend      │ │   eng-backend      │ │   eng-backend      │ │  eng-devsecops     │
 │                    │ │                    │ │                    │ │                    │ │                    │
 │  Layer 1           │ │  Layer 2           │ │  Layer 3           │ │  Layer 4           │ │  CI/CD             │
 │  promptfoo CI/CD   │ │  DeepEval          │ │  Metamorphic       │ │  Statistical       │ │  Pipeline          │
 │  Integration       │ │  Evaluation        │ │  Relation          │ │  Comparison        │ │  Setup             │
 │                    │ │  Backend           │ │  Framework         │ │  Engine            │ │                    │
 │  GHA YAML          │ │  Debiased          │ │  5 univ. MRs       │ │  Wilcoxon          │ │  3-tier workflow   │
 │  Docker            │ │  LLM-as-Judge      │ │  MR-001 through    │ │  Wilson            │ │  Smoke/Standard/   │
 │  Version Key Mgmt  │ │  pytest            │ │  MR-005            │ │  Bonferroni        │ │  Full              │
 │         │          │ │         │          │ │         │          │ │         │          │ │         │          │
 │  S-010 Self-Review │ │  S-010 Self-Review │ │  S-010 Self-Review │ │  S-010 Self-Review │ │  S-010 Self-Review │
 │         │          │ │         │          │ │         │          │ │         │          │ │         │          │
 │  ┌────────────┐    │ │  ┌────────────┐    │ │  ┌────────────┐    │ │  ┌────────────┐    │ │  ┌────────────┐    │
 │  │ adv-scorer │    │ │  │ adv-scorer │    │ │  │ adv-scorer │    │ │  │ adv-scorer │    │ │  │ adv-scorer │    │
 │  │adv-executor│    │ │  │adv-executor│    │ │  │adv-executor│    │ │  │adv-executor│    │ │  │adv-executor│    │
 │  │ >= 0.94    │    │ │  │ >= 0.94    │    │ │  │ >= 0.94    │    │ │  │ >= 0.94    │    │ │  │ >= 0.94    │    │
 │  │min 3/max 5 │    │ │  │min 3/max 5 │    │ │  │min 3/max 5 │    │ │  │min 3/max 5 │    │ │  │min 3/max 5 │    │
 │  └─────┬──────┘    │ │  └─────┬──────┘    │ │  └─────┬──────┘    │ │  └─────┬──────┘    │ │  └─────┬──────┘    │
 │        │ PASS      │ │        │ PASS      │ │        │ PASS      │ │        │ PASS      │ │        │ PASS      │
 └────────┼───────────┘ └────────┼───────────┘ └────────┼───────────┘ └────────┼───────────┘ └────────┼───────────┘
          │                      │                      │                      │                      │
          │ .github/             │ jerry/               │ jerry/               │ jerry/               │ .github/
          │ workflows/           │ testing/             │ testing/             │ testing/             │ workflows/
          │ tests/               │ evaluation/          │ metamorphic/         │ stats.py             │ actions/
          │ prompt-reg/          │                      │                      │ types.py             │
          │ docker/              │                      │                      │ baselines/           │
          │ promptfoo/           │                      │                      │ reports/             │
          └──────────────────────┴──────────────────────┴──────────┬───────────┴──────────────────────┘
                                                                   │ (all 5 streams PASS per-stream >= 0.94)
                                                                   ▼
                             ╔══════════════════════════════════════════════╗
                             ║    BARRIER 2 / GROUP 4                       ║
                             ║    C4 Adversarial Quality Gate               ║
                             ║    (Cross-Deliverable Consistency Check)     ║
                             ║                                              ║
                             ║  Agents: adv-scorer, adv-executor            ║
                             ║  All 10 C4 strategies applied                ║
                             ║  Focus: are all 5 implementation outputs     ║
                             ║  consistent with architecture and each other?║
                             ║  Threshold: >= 0.95 each                     ║
                             ║  Max 5 iterations per deliverable            ║
                             ║                                              ║
                             ║  Additional consistency checks:              ║
                             ║  - Type checking compliance                  ║
                             ║  - H-11 (type hints + docstrings)            ║
                             ║  - H-10 (one class per file)                 ║
                             ║  - H-07 (layer isolation)                    ║
                             ║  - N >= 20 runs enforcement                  ║
                             ║  - Debiasing mandatory verified              ║
                             ║                                              ║
                             ║  Precondition: ALL 5 streams at >= 0.94     ║
                             ║  ALL 5 MUST PASS consistency check           ║
                             ╚═══════════════════╤══════════════════════════╝
                                                 │ (all 5 PASS >= 0.95)
                                                 ▼

 GROUP 5: PARALLEL ASSURANCE (Fan-Out, 3 concurrent streams)
 Each stream includes an embedded adversarial review cycle before barrier eligibility.
 ═══════════════════════════════════════════════════════════════════════════════════
 ┌──────────────────────────┐  ┌────────────────────────┐  ┌──────────────────────────┐
 │       STREAM 5A          │  │      STREAM 5B         │  │       STREAM 5C          │
 │  red-lead, red-vuln      │  │  nse-verification      │  │  eng-qa                  │
 │  red-exploit             │  │                        │  │                          │
 │                          │  │  V&V Execution         │  │  Test Suite Dev          │
 │  Security Assessment     │  │                        │  │                          │
 │                          │  │  Requirements          │  │  Unit tests              │
 │  YAML injection          │  │  coverage matrix       │  │  Property-based          │
 │  Prompt injection        │  │  Interface V&V         │  │  (hypothesis)            │
 │  Stat manipulation       │  │  Constraint V&V        │  │  Integration tests       │
 │  Credential exposure     │  │  FMEA mitigation       │  │  90% coverage target     │
 │  FMEA attack surface     │  │  verification          │  │                          │
 │         │                │  │         │              │  │         │                │
 │  S-010 Self-Review       │  │  S-010 Self-Review     │  │  S-010 Self-Review       │
 │         │                │  │         │              │  │         │                │
 │  ┌────────────────┐      │  │  ┌────────────────┐    │  │  ┌────────────────┐      │
 │  │  adv-scorer    │      │  │  │  adv-scorer    │    │  │  │  adv-scorer    │      │
 │  │  adv-executor  │      │  │  │  adv-executor  │    │  │  │  adv-executor  │      │
 │  │  >= 0.94       │      │  │  │  >= 0.94       │    │  │  │  >= 0.94       │      │
 │  │  min 3/max 5   │      │  │  │  min 3/max 5   │    │  │  │  min 3/max 5   │      │
 │  └───────┬────────┘      │  │  └───────┬────────┘    │  │  └───────┬────────┘      │
 │          │ PASS          │  │          │ PASS        │  │          │ PASS          │
 └──────────┼───────────────┘  └──────────┼─────────────┘  └──────────┼───────────────┘
            │                             │                            │
            │ security/                   │ verification/              │ tests/
            │                             │                            │ prompt-regression/
            │                             │                            │ unit/ property/
            │                             │                            │ integration/
            └─────────────────────────────┴─────────────┬──────────────┘
                                                        │ (all 3 streams PASS per-stream >= 0.94)
                                                        ▼
                             ╔══════════════════════════════════════════════╗
                             ║    BARRIER 3 / GROUP 6                       ║
                             ║    C4 Adversarial Quality Gate               ║
                             ║    (Cross-Deliverable Consistency Check)     ║
                             ║                                              ║
                             ║  Agents: adv-scorer, adv-executor            ║
                             ║  All 10 C4 strategies applied                ║
                             ║  Focus: security + V&V + test coverage       ║
                             ║  form a complete assurance picture           ║
                             ║  Threshold: >= 0.95 each                     ║
                             ║  Max 5 iterations per deliverable            ║
                             ║                                              ║
                             ║  Precondition: ALL 3 streams at >= 0.94     ║
                             ║  ALL 3 MUST PASS consistency check           ║
                             ╚═══════════════════╤══════════════════════════╝
                                                 │ (all 3 PASS >= 0.95)
                                                 ▼

 GROUP 7: PARALLEL SYNTHESIS (Fan-Out, 2 concurrent streams)
 Each stream includes an embedded adversarial review cycle before barrier eligibility.
 ═══════════════════════════════════════════════════════════════════════════════════
               ┌───────────────────────────────────┐  ┌────────────────────────────────────┐
               │           STREAM 7A               │  │           STREAM 7B                │
               │         eng-reviewer              │  │         ps-synthesizer             │
               │                                   │  │                                    │
               │  Final Engineering Review         │  │  Cross-Synthesis                   │
               │                                   │  │                                    │
               │  OWASP Top 10                     │  │  Implementation completeness       │
               │  ASVS L1                          │  │  Risk register update              │
               │  SOLID compliance                 │  │  Residual gaps                     │
               │  Security remediations            │  │  PROJ-017 readiness                │
               │  Architecture compliance          │  │  Operational readiness             │
               │  Test completeness                │  │                                    │
               │         │                         │  │         │                          │
               │  S-010 Self-Review                │  │  S-010 Self-Review                 │
               │         │                         │  │         │                          │
               │  ┌─────────────────┐              │  │  ┌─────────────────┐               │
               │  │  adv-scorer     │              │  │  │  adv-scorer     │               │
               │  │  adv-executor   │              │  │  │  adv-executor   │               │
               │  │  >= 0.94        │              │  │  │  >= 0.94        │               │
               │  │  min 3/max 5    │              │  │  │  min 3/max 5    │               │
               │  └────────┬────────┘              │  │  └────────┬────────┘               │
               │           │ PASS                  │  │           │ PASS                   │
               └───────────┼───────────────────────┘  └───────────┼────────────────────────┘
                           │                                       │
                           │ reviews/                              │ synthesis/
                           │ engineering-review.md                 │
                           └───────────────────────────┬───────────┘
                                                       │ (both streams PASS per-stream >= 0.94)
                                                       ▼
                             ╔══════════════════════════════════════════════╗
                             ║    BARRIER 4 / GROUP 8                       ║
                             ║    DUAL FINAL GATE + HUMAN                   ║
                             ║    (Cross-Deliverable Consistency Check)     ║
                             ║                                              ║
                             ║  Gate A: adv-scorer                          ║
                             ║  All 10 C4 strategies                        ║
                             ║  Complete package scoring                    ║
                             ║  Threshold: >= 0.95                          ║
                             ║                                              ║
                             ║  Gate B: nse-reviewer                        ║
                             ║  Requirements traceability                   ║
                             ║  Evidence basis                              ║
                             ║  Risk coverage                               ║
                             ║  Implementation feasibility                  ║
                             ║                                              ║
                             ║  Precondition: BOTH streams at >= 0.94      ║
                             ║  BOTH MUST PASS                              ║
                             ╚═══════════════════╤══════════════════════════╝
                                                 │ (Gate A AND Gate B PASS)
                                                 ▼
                             ┌──────────────────────────────────────────────┐
                             │          HUMAN REVIEW (P-020)                │
                             │                                              │
                             │  Present:                                    │
                             │  - Implementation summary                    │
                             │  - All per-stream quality scores (>= 0.94)  │
                             │  - All barrier gate scores (>= 0.95)         │
                             │  - Security summary                          │
                             │  - Residual risks                            │
                             │  - Recommendation                            │
                             │                                              │
                             │  Human accepts or rejects                    │
                             └──────────────────────────────────────────────┘
```

### Execution Group Summary

| Group | Mode | Streams | Agents | Trigger | Per-Stream Gate | Barrier Gate |
|-------|------|---------|--------|---------|-----------------|--------------|
| 1 | PARALLEL (4 streams) | 1A, 1B, 1C, 1D | nse-requirements (x2), eng-architect, nse-architecture, eng-lead, eng-qa | Workflow start | >= 0.94 each stream (adv-scorer + adv-executor) | None (barrier follows) |
| 2 | SEQUENTIAL | 1 gate | adv-scorer, adv-executor | All Group 1 streams PASS >= 0.94 | N/A | C4: >= 0.95 all 4 (consistency) |
| 3 | PARALLEL (5 streams) | 3A, 3B, 3C, 3D, 3E | eng-backend (x4), eng-devsecops | Barrier 1 PASS | >= 0.94 each stream (adv-scorer + adv-executor) | None (barrier follows) |
| 4 | SEQUENTIAL | 1 gate | adv-scorer, adv-executor | All Group 3 streams PASS >= 0.94 | N/A | C4: >= 0.95 all 5 (consistency) |
| 5 | PARALLEL (3 streams) | 5A, 5B, 5C | red-lead, red-vuln, red-exploit, nse-verification, eng-qa | Barrier 2 PASS | >= 0.94 each stream (adv-scorer + adv-executor) | None (barrier follows) |
| 6 | SEQUENTIAL | 1 gate | adv-scorer, adv-executor | All Group 5 streams PASS >= 0.94 | N/A | C4: >= 0.95 all 3 (consistency) |
| 7 | PARALLEL (2 streams) | 7A, 7B | eng-reviewer, ps-synthesizer | Barrier 3 PASS | >= 0.94 each stream (adv-scorer + adv-executor) | None (barrier follows) |
| 8 | SEQUENTIAL (dual) | Final gate + human | adv-scorer, nse-reviewer | All Group 7 streams PASS >= 0.94 | N/A | C4: >= 0.95; NPR 7123.1D |

### Group 1 — Parallel Foundations

#### Stream 1A: Requirements Derivation

| Field | Value |
|-------|-------|
| Agent | jerry:nse-requirements |
| Skill | /nasa-se |
| Input | ADR-001 (PROJ-035, Four-Layer Composite Test Harness Architecture) |
| Scope | Derive functional requirements, non-functional requirements, interface specifications, acceptance criteria, and FMEA-derived requirements from ADR-001 |
| Deliverables | Functional requirements (FR-001 through FR-NNN), non-functional requirements, interface contracts for each of 4 layers, acceptance criteria per requirement, FMEA failure mode traceability (FM-001 through FM-010 from Phase 5) |
| Format | NASA-style numbered requirements with rationale, verification method, and ADR traceability |
| Output | `projects/PROJ-036-prompt-regression-harness/requirements/harness-requirements.md` |
| Per-Stream Quality Cycle | Embedded adversarial review: adv-scorer (S-014 scoring) + adv-executor (critique generation). Threshold: >= 0.94 weighted composite. Min 3 iterations (H-14), max 5 iterations (C4 ceiling per RT-M-010). H-16 ordering: steelman (S-003) before devil's advocate (S-002). S-010 self-review REQUIRED before first critic submission (H-15). All 10 C4 strategies applied. |
| Per-Stream Recovery | Score < 0.94 after 5 iterations: escalate to human per H-31; do NOT pass deliverable to Barrier 1 |

#### Stream 1B: System Design with Threat Model

| Field | Value |
|-------|-------|
| Agents | jerry:eng-architect, jerry:nse-architecture, jerry:eng-lead |
| Skills | /eng-team, /nasa-se |
| Coordination | eng-architect produces hexagonal architecture and module decomposition; nse-architecture produces interface specifications and system context diagram; eng-lead produces STRIDE threat model and security controls mapping |
| Input | ADR-001 Section "L1: Technical Implementation" (architecture diagram, component integration patterns, code patterns) |
| Scope | Hexagonal architecture diagram, module decomposition (Layer 1-4 module boundaries), interface contracts, dependency graph, STRIDE threat model (Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege for all attack surfaces), security controls |
| Output | `projects/PROJ-036-prompt-regression-harness/design/system-design.md` |
| Per-Stream Quality Cycle | Embedded adversarial review: adv-scorer (S-014 scoring) + adv-executor (critique generation). Threshold: >= 0.94 weighted composite. Min 3 iterations (H-14), max 5 iterations (C4 ceiling per RT-M-010). H-16 ordering: steelman (S-003) before devil's advocate (S-002). S-010 self-review REQUIRED before first critic submission (H-15). All 10 C4 strategies applied. |
| Per-Stream Recovery | Score < 0.94 after 5 iterations: escalate to human per H-31; do NOT pass deliverable to Barrier 1 |

#### Stream 1C: Baseline Generation Protocol

| Field | Value |
|-------|-------|
| Agent | jerry:eng-qa |
| Skill | /eng-team |
| Scope | Protocol and artifacts for N=30 baseline capture. Target agents: ps-researcher, ps-analyst, ps-architect, ps-critic, adv-scorer. 3-5 canonical prompts per agent. Capture schema, run protocol, statistical adequacy rationale for N=30 |
| Deliverables | (1) `baselines/protocol.md` — step-by-step N=30 run procedure, environment requirements, reproducibility controls. (2) `baselines/schemas/` — JSON schemas for captured baseline records. (3) `baselines/prompts/` — 3-5 canonical test prompts per agent (15-25 total prompt files). NOTE: Actual N=30 data collection executes at runtime after harness deployment; this stream produces the protocol and prompt artifacts only |
| Output | `projects/PROJ-036-prompt-regression-harness/baselines/protocol.md`, `baselines/schemas/`, `baselines/prompts/` |
| Per-Stream Quality Cycle | Embedded adversarial review: adv-scorer (S-014 scoring) + adv-executor (critique generation). Threshold: >= 0.94 weighted composite. Min 3 iterations (H-14), max 5 iterations (C4 ceiling per RT-M-010). H-16 ordering: steelman (S-003) before devil's advocate (S-002). S-010 self-review REQUIRED before first critic submission (H-15). All 10 C4 strategies applied. |
| Per-Stream Recovery | Score < 0.94 after 5 iterations: escalate to human per H-31; do NOT pass deliverable to Barrier 1 |

#### Stream 1D: Behavioral Contract Generation

| Field | Value |
|-------|-------|
| Agent | jerry:nse-requirements |
| Skill | /nasa-se |
| Scope | Structural invariants (properties that must always hold), quality bounds (acceptable score ranges per agent per metric), metamorphic relation tolerances (MR-001 through MR-005 tolerance values), regression detection thresholds (p-value cutoffs, Wilson interval widths), Bonferroni-corrected multi-metric thresholds |
| Deliverables | (1) `contracts/behavioral-contracts.md` — master contract document. (2) `contracts/schemas/` — machine-readable contract schemas. (3) `contracts/per-agent/` — per-agent contract files (one per target agent) |
| Output | `projects/PROJ-036-prompt-regression-harness/contracts/behavioral-contracts.md`, `contracts/schemas/`, `contracts/per-agent/` |
| Per-Stream Quality Cycle | Embedded adversarial review: adv-scorer (S-014 scoring) + adv-executor (critique generation). Threshold: >= 0.94 weighted composite. Min 3 iterations (H-14), max 5 iterations (C4 ceiling per RT-M-010). H-16 ordering: steelman (S-003) before devil's advocate (S-002). S-010 self-review REQUIRED before first critic submission (H-15). All 10 C4 strategies applied. |
| Per-Stream Recovery | Score < 0.94 after 5 iterations: escalate to human per H-31; do NOT pass deliverable to Barrier 1 |

### Group 3 — Parallel Implementation

#### Stream 3A: Layer 1 — promptfoo CI/CD Integration

| Field | Value |
|-------|-------|
| Agent | jerry:eng-backend |
| Skill | /eng-team |
| ADR Reference | ADR-001 Section "L1: Technical Implementation" — Layer 1 (promptfoo, MIT license) |
| Scope | GitHub Actions workflow for PR-triggered regression testing; YAML test case definitions for all 5 target agents; Docker configuration for promptfoo (runs via Docker/GHA per ADR-001 Constraints: npm alongside UV); version key management for baseline/candidate prompt version tracking |
| Implementation Constraints | UV-only Python (H-05); promptfoo via Docker (not direct npm); YAML test cases in `tests/prompt-regression/`; GHA workflow in `.github/workflows/`; type hints required (H-11); H-20 compliance |
| Output | `.github/workflows/prompt-regression-*.yml`, `tests/prompt-regression/*.yaml`, `docker/promptfoo/Dockerfile`, `tests/prompt-regression/version_keys.py` |
| Per-Stream Quality Cycle | Embedded adversarial review: adv-scorer (S-014 scoring) + adv-executor (critique generation). Threshold: >= 0.94 weighted composite. Min 3 iterations (H-14), max 5 iterations (C4 ceiling per RT-M-010). H-16 ordering: steelman (S-003) before devil's advocate (S-002). S-010 self-review REQUIRED before first critic submission (H-15). All 10 C4 strategies applied. |
| Per-Stream Recovery | Score < 0.94 after 5 iterations: escalate to human per H-31; do NOT pass deliverable to Barrier 2 |

#### Stream 3B: Layer 2 — DeepEval Evaluation Backend

| Field | Value |
|-------|-------|
| Agent | jerry:eng-backend |
| Skill | /eng-team |
| ADR Reference | ADR-001 Section "L1: Technical Implementation" — Layer 2 (DeepEval, Apache 2.0) |
| Scope | Debiased LLM-as-Judge implementation (position randomization, rubric shuffling per ADR-001 Forces F-5 and Phase 1D Innovation #1); custom DeepEval metrics for Jerry-specific evaluation criteria; G-Eval criteria definitions for all 5 target agents; pytest integration and conftest.py; H-11 compliant implementations with full type annotations and docstrings |
| Output | `jerry/testing/evaluation/__init__.py`, `jerry/testing/evaluation/metrics.py`, `jerry/testing/evaluation/debiasing.py`, `jerry/testing/evaluation/criteria/` (per-agent G-Eval criteria) |
| Per-Stream Quality Cycle | Embedded adversarial review: adv-scorer (S-014 scoring) + adv-executor (critique generation). Threshold: >= 0.94 weighted composite. Min 3 iterations (H-14), max 5 iterations (C4 ceiling per RT-M-010). H-16 ordering: steelman (S-003) before devil's advocate (S-002). S-010 self-review REQUIRED before first critic submission (H-15). All 10 C4 strategies applied. |
| Per-Stream Recovery | Score < 0.94 after 5 iterations: escalate to human per H-31; do NOT pass deliverable to Barrier 2 |

#### Stream 3C: Layer 3 — Metamorphic Relation Framework

| Field | Value |
|-------|-------|
| Agent | jerry:eng-backend |
| Skill | /eng-team |
| ADR Reference | ADR-001 Section "L1: Technical Implementation" — Layer 3 (Custom Python, metamorphic relations) |
| Scope | 5 universal metamorphic relations: MR-001 Paraphrase Consistency (tolerance from 1D contracts), MR-002 Negation Handling, MR-003 Irrelevant Context Appendation, MR-004 Formatting Perturbation, MR-005 Language Round-Trip. Each MR is a custom DeepEval metric (BaseMetric subclass). Tolerance values sourced from Stream 1D behavioral contracts |
| Implementation Constraints | One class per file (H-10); H-11 (type hints + docstrings); H-07 (domain layer isolation — MR definitions must not import from promptfoo or DeepEval internals); N >= 20 enforcement in MR execution harness |
| Output | `jerry/testing/metamorphic/__init__.py`, `jerry/testing/metamorphic/mr_001_paraphrase.py`, `jerry/testing/metamorphic/mr_002_negation.py`, `jerry/testing/metamorphic/mr_003_context.py`, `jerry/testing/metamorphic/mr_004_formatting.py`, `jerry/testing/metamorphic/mr_005_roundtrip.py`, `jerry/testing/metamorphic/base.py` |
| Per-Stream Quality Cycle | Embedded adversarial review: adv-scorer (S-014 scoring) + adv-executor (critique generation). Threshold: >= 0.94 weighted composite. Min 3 iterations (H-14), max 5 iterations (C4 ceiling per RT-M-010). H-16 ordering: steelman (S-003) before devil's advocate (S-002). S-010 self-review REQUIRED before first critic submission (H-15). All 10 C4 strategies applied. |
| Per-Stream Recovery | Score < 0.94 after 5 iterations: escalate to human per H-31; do NOT pass deliverable to Barrier 2 |

#### Stream 3D: Layer 4 — Statistical Comparison Engine

| Field | Value |
|-------|-------|
| Agent | jerry:eng-backend |
| Skill | /eng-team |
| ADR Reference | ADR-001 Section "L1: Technical Implementation" — Layer 4 (scipy BSD + custom), shared with PROJ-017 |
| Scope | Shared statistical module (Wilcoxon signed-rank test for version A vs. B comparison; Wilson score intervals for per-metric uncertainty quantification; Bonferroni correction for multi-metric comparisons); shared type definitions; baseline persistence and retrieval; report generation (NO_REGRESSION, MARGINAL, REGRESSION classification with confidence intervals). Module is shared with PROJ-017 per ADR-001 L1 Decision table |
| Implementation Constraints | H-10 (one class per file); H-11 (type hints + docstrings — mandatory for all public functions per ADR-001 note); H-07 (stats module must not import from testing frameworks — domain isolation); N >= 20 enforced at function entry with ValueError on violation |
| Output | `jerry/testing/stats.py`, `jerry/testing/types.py`, `jerry/testing/baselines/__init__.py`, `jerry/testing/baselines/store.py`, `jerry/testing/reports/__init__.py`, `jerry/testing/reports/generator.py` |
| Per-Stream Quality Cycle | Embedded adversarial review: adv-scorer (S-014 scoring) + adv-executor (critique generation). Threshold: >= 0.94 weighted composite. Min 3 iterations (H-14), max 5 iterations (C4 ceiling per RT-M-010). H-16 ordering: steelman (S-003) before devil's advocate (S-002). S-010 self-review REQUIRED before first critic submission (H-15). All 10 C4 strategies applied. |
| Per-Stream Recovery | Score < 0.94 after 5 iterations: escalate to human per H-31; do NOT pass deliverable to Barrier 2 |

#### Stream 3E: CI/CD Pipeline Setup

| Field | Value |
|-------|-------|
| Agent | jerry:eng-devsecops |
| Skill | /eng-team |
| Scope | Three-tier workflow architecture: (1) Smoke tier — fast PR checks, subset of test cases, < 5 minutes; (2) Standard tier — full prompt-regression suite, statistical comparison, metamorphic checks, runs on merge to main; (3) Full tier — N=30 statistical baseline refresh, all agents, scheduled or manually triggered. Secrets management (LLM API keys via GHA secrets, not env vars). Artifact management (score reports, comparison outputs as GHA artifacts). Cost monitoring (token count tracking, alerting on cost threshold breach) |
| Output | `.github/workflows/prompt-regression-smoke.yml`, `.github/workflows/prompt-regression-standard.yml`, `.github/workflows/prompt-regression-full.yml`, `.github/actions/cost-monitor/action.yml`, `.github/actions/artifact-publish/action.yml` |
| Per-Stream Quality Cycle | Embedded adversarial review: adv-scorer (S-014 scoring) + adv-executor (critique generation). Threshold: >= 0.94 weighted composite. Min 3 iterations (H-14), max 5 iterations (C4 ceiling per RT-M-010). H-16 ordering: steelman (S-003) before devil's advocate (S-002). S-010 self-review REQUIRED before first critic submission (H-15). All 10 C4 strategies applied. |
| Per-Stream Recovery | Score < 0.94 after 5 iterations: escalate to human per H-31; do NOT pass deliverable to Barrier 2 |

### Group 5 — Parallel Assurance

#### Stream 5A: Security Assessment

| Field | Value |
|-------|-------|
| Agents | jerry:red-lead, jerry:red-vuln, jerry:red-exploit |
| Skill | /red-team |
| Scope | YAML injection attacks on promptfoo test case files; prompt injection via maliciously crafted test case inputs; statistical manipulation (adversarial score sequence construction to defeat Wilcoxon test); credential and API key exposure analysis; FMEA attack surface enumeration (all 10 FM failure modes assessed for exploitability). red-lead coordinates; red-vuln identifies vulnerabilities; red-exploit validates exploitability |
| Input | All Group 3 outputs (implementation code) |
| Output | `projects/PROJ-036-prompt-regression-harness/security/security-assessment.md`, `security/findings/`, `security/remediations.md` |
| Per-Stream Quality Cycle | Embedded adversarial review: adv-scorer (S-014 scoring) + adv-executor (critique generation). Threshold: >= 0.94 weighted composite. Min 3 iterations (H-14), max 5 iterations (C4 ceiling per RT-M-010). H-16 ordering: steelman (S-003) before devil's advocate (S-002). S-010 self-review REQUIRED before first critic submission (H-15). All 10 C4 strategies applied. |
| Per-Stream Recovery | Score < 0.94 after 5 iterations: escalate to human per H-31; do NOT pass deliverable to Barrier 3 |

#### Stream 5B: V&V Execution

| Field | Value |
|-------|-------|
| Agent | jerry:nse-verification |
| Skill | /nasa-se |
| Scope | Requirements coverage matrix (each FR from Stream 1A traced to implementation artifact); interface verification (each interface spec from Stream 1B verified against implementation); constraint verification (all constraints from ADR-001 verified as implemented); FMEA mitigation verification (each of FM-001 through FM-010 mitigations verified as implemented in Streams 3A-3E) |
| Input | Stream 1A requirements, Stream 1B design, all Group 3 outputs |
| Output | `projects/PROJ-036-prompt-regression-harness/verification/requirements-coverage-matrix.md`, `verification/interface-verification.md`, `verification/constraint-verification.md`, `verification/fmea-mitigation-verification.md` |
| Per-Stream Quality Cycle | Embedded adversarial review: adv-scorer (S-014 scoring) + adv-executor (critique generation). Threshold: >= 0.94 weighted composite. Min 3 iterations (H-14), max 5 iterations (C4 ceiling per RT-M-010). H-16 ordering: steelman (S-003) before devil's advocate (S-002). S-010 self-review REQUIRED before first critic submission (H-15). All 10 C4 strategies applied. |
| Per-Stream Recovery | Score < 0.94 after 5 iterations: escalate to human per H-31; do NOT pass deliverable to Barrier 3 |

#### Stream 5C: Test Suite Development

| Field | Value |
|-------|-------|
| Agent | jerry:eng-qa |
| Skill | /eng-team |
| Scope | Unit tests for all modules in Streams 3B, 3C, 3D; property-based tests using hypothesis (statistical function properties, MR invariants, baseline store properties); integration tests for Layer 1+2 and Layer 3+4 interactions. Target: 90% line coverage (H-20/H-21). Test-first development per H-20 BDD Red phase |
| Input | All Group 3 outputs (implementation code to test) |
| Output | `tests/prompt-regression/unit/`, `tests/prompt-regression/property/`, `tests/prompt-regression/integration/` |
| Per-Stream Quality Cycle | Embedded adversarial review: adv-scorer (S-014 scoring) + adv-executor (critique generation). Threshold: >= 0.94 weighted composite. Min 3 iterations (H-14), max 5 iterations (C4 ceiling per RT-M-010). H-16 ordering: steelman (S-003) before devil's advocate (S-002). S-010 self-review REQUIRED before first critic submission (H-15). All 10 C4 strategies applied. |
| Per-Stream Recovery | Score < 0.94 after 5 iterations: escalate to human per H-31; do NOT pass deliverable to Barrier 3 |

### Group 7 — Parallel Synthesis

#### Stream 7A: Final Engineering Review

| Field | Value |
|-------|-------|
| Agent | jerry:eng-reviewer |
| Skill | /eng-team |
| Scope | OWASP Top 10 compliance check against implementation; ASVS Level 1 checklist; SOLID principle compliance across all modules; security remediations from Stream 5A applied and verified; architecture compliance with ADR-001 hexagonal design; test completeness verification (90% coverage achieved) |
| Input | All prior group outputs |
| Output | `projects/PROJ-036-prompt-regression-harness/reviews/engineering-review.md` |
| Per-Stream Quality Cycle | Embedded adversarial review: adv-scorer (S-014 scoring) + adv-executor (critique generation). Threshold: >= 0.94 weighted composite. Min 3 iterations (H-14), max 5 iterations (C4 ceiling per RT-M-010). H-16 ordering: steelman (S-003) before devil's advocate (S-002). S-010 self-review REQUIRED before first critic submission (H-15). All 10 C4 strategies applied. |
| Per-Stream Recovery | Score < 0.94 after 5 iterations: escalate to human per H-31; do NOT pass deliverable to Barrier 4 |

#### Stream 7B: Cross-Synthesis

| Field | Value |
|-------|-------|
| Agent | jerry:ps-synthesizer |
| Skill | /problem-solving |
| Scope | Implementation completeness assessment against ADR-001 six-phase roadmap (Phases A-D implemented, E-F deferred); updated risk register incorporating security assessment findings; residual gaps not addressed in this implementation; PROJ-017 integration readiness assessment (shared stats.py module interface compatibility); operational readiness checklist (deployment prerequisites, monitoring, runbooks) |
| Input | All prior group outputs |
| Output | `projects/PROJ-036-prompt-regression-harness/synthesis/implementation-synthesis.md`, `synthesis/risk-register-updated.md`, `synthesis/operational-readiness.md` |
| Per-Stream Quality Cycle | Embedded adversarial review: adv-scorer (S-014 scoring) + adv-executor (critique generation). Threshold: >= 0.94 weighted composite. Min 3 iterations (H-14), max 5 iterations (C4 ceiling per RT-M-010). H-16 ordering: steelman (S-003) before devil's advocate (S-002). S-010 self-review REQUIRED before first critic submission (H-15). All 10 C4 strategies applied. |
| Per-Stream Recovery | Score < 0.94 after 5 iterations: escalate to human per H-31; do NOT pass deliverable to Barrier 4 |

### Group 8 — Final Gate and Human Review

#### Gate A: C4 Adversarial Quality Score

| Field | Value |
|-------|-------|
| Agent | jerry:adv-scorer |
| Scope | Score the complete implementation package against all 10 C4 adversarial strategies. Input package: all Group 7 outputs plus cumulative artifact index |
| Threshold | >= 0.95 weighted composite (S-014) |
| Max Iterations | 5 (C4 ceiling per RT-M-010) |
| On Failure | Return to Group 7 with specific critique; max 5 combined iterations; escalate to human on 5th failure per H-31 |
| Output | `projects/PROJ-036-prompt-regression-harness/quality-gates/gate-final/gate-a-adversarial-score.md` |

#### Gate B: NASA SE Technical Review

| Field | Value |
|-------|-------|
| Agent | jerry:nse-reviewer |
| Input | Gate A PASS report + complete implementation package |
| Scope | Requirements traceability (all FRs from Stream 1A traced to implementation); evidence basis (each implementation choice traces to ADR-001 evidence); risk coverage (all FMEA failure modes FM-001 to FM-010 addressed); implementation feasibility assessment |
| Standard | NPR 7123.1D Appendix G |
| Output | `projects/PROJ-036-prompt-regression-harness/quality-gates/gate-final/gate-b-nse-review.md` |

#### Human Acceptance (P-020)

Precondition: Gate A PASS AND Gate B PASS (both mandatory; neither is optional).

Present to human:
- Implementation summary (what was built across all 4 layers)
- All per-stream quality scores (all 14 creator streams, each at >= 0.94 — included to give full quality transparency)
- All barrier gate scores (Groups 2, 4, 6, 8 — all 4 quality gates with pass/fail per deliverable)
- Security summary (Stream 5A findings, remediations applied, residual risks)
- Residual risks (updated risk register from Stream 7B)
- Recommendation (proceed to deployment or additional work required)

### Sync Barriers

> **Note:** Barrier gates now serve as cross-deliverable consistency reviews. Individual quality is pre-validated at >= 0.94 per stream. The barrier gate verifies that the group's outputs are mutually consistent, architecturally aligned, and collectively complete — not merely individually passing.

| Barrier | ID | Trigger Condition | Gate Agent(s) | Threshold | C4 Strategies | Max Iter | Failure Action |
|---------|-----|------------------|--------------|-----------|---------------|----------|----------------|
| Barrier 1 | QG-1 | All 4 Group 1 streams PASS >= 0.94 per-stream | adv-scorer, adv-executor | >= 0.95 each of 4 (consistency check) | All 10 | 5 per deliverable | Return to producing agent; escalate on 5th failure per H-31 |
| Barrier 2 | QG-2 | All 5 Group 3 streams PASS >= 0.94 per-stream | adv-scorer, adv-executor | >= 0.95 each of 5 (consistency check) | All 10 | 5 per deliverable | Return to producing agent; escalate on 5th failure per H-31 |
| Barrier 3 | QG-3 | All 3 Group 5 streams PASS >= 0.94 per-stream | adv-scorer, adv-executor | >= 0.95 each of 3 (consistency check) | All 10 | 5 per deliverable | Return to producing agent; escalate on 5th failure per H-31 |
| Barrier 4 | QG-4A | All 2 Group 7 streams PASS >= 0.94 per-stream | adv-scorer | >= 0.95 (consistency check) | All 10 | 5 | Return to Group 7; escalate on 5th failure |
| Barrier 4 | QG-4B | Gate A PASS | nse-reviewer | NPR 7123.1D App. G | N/A | 3 combined A+B | Return to Group 7; max 3 combined Gate A+B iterations |

---

## L2: Implementation Details

### State Schema (ORCHESTRATION.yaml)

```yaml
workflow:
  id: "harness-impl-20260306-001"
  name: "FEAT-036-001 Four-Layer Composite Test Harness Implementation"
  status: "PLANNED"
  feature: "FEAT-036-001"
  project: "PROJ-036-prompt-regression-harness"
  source_adr: "ADR-001 (PROJ-035, Four-Layer Composite Test Harness Architecture)"
  criticality: "C4"
  quality_threshold_barrier: 0.95
  quality_threshold_stream: 0.94
  date_created: "2026-03-06"

paths:
  base: "orchestration/{workflow.id}/"
  plan: "{base}ORCHESTRATION_PLAN.md"
  state: "{base}ORCHESTRATION.yaml"
  requirements: "projects/{workflow.project}/requirements/"
  design: "projects/{workflow.project}/design/"
  baselines: "projects/{workflow.project}/baselines/"
  contracts: "projects/{workflow.project}/contracts/"
  quality_gates: "projects/{workflow.project}/quality-gates/"
  security: "projects/{workflow.project}/security/"
  verification: "projects/{workflow.project}/verification/"
  reviews: "projects/{workflow.project}/reviews/"
  synthesis: "projects/{workflow.project}/synthesis/"
  implementation: "projects/{workflow.project}/implementation/"

execution_groups:
  group_1:
    mode: "PARALLEL"
    status: "PENDING"
    streams: ["1A", "1B", "1C", "1D"]
  group_2:
    mode: "SEQUENTIAL"
    status: "PENDING"
    depends_on: "group_1"
    precondition: "all group_1 streams per_stream_quality_score >= 0.94"
    gate_id: "QG-1"
  group_3:
    mode: "PARALLEL"
    status: "PENDING"
    depends_on: "group_2"
    streams: ["3A", "3B", "3C", "3D", "3E"]
  group_4:
    mode: "SEQUENTIAL"
    status: "PENDING"
    depends_on: "group_3"
    precondition: "all group_3 streams per_stream_quality_score >= 0.94"
    gate_id: "QG-2"
  group_5:
    mode: "PARALLEL"
    status: "PENDING"
    depends_on: "group_4"
    streams: ["5A", "5B", "5C"]
  group_6:
    mode: "SEQUENTIAL"
    status: "PENDING"
    depends_on: "group_5"
    precondition: "all group_5 streams per_stream_quality_score >= 0.94"
    gate_id: "QG-3"
  group_7:
    mode: "PARALLEL"
    status: "PENDING"
    depends_on: "group_6"
    streams: ["7A", "7B"]
  group_8:
    mode: "SEQUENTIAL"
    status: "PENDING"
    depends_on: "group_7"
    precondition: "all group_7 streams per_stream_quality_score >= 0.94"
    gate_id: "QG-4A"
    human_review_required: true

# Per-stream quality tracking — populated by orchestrator during execution.
# Each stream entry records: score per iteration, final score, iteration count,
# pass/fail status, and escalation flag.
stream_quality:
  "1A": { iterations: 0, scores: [], final_score: null, status: "PENDING", escalated: false }
  "1B": { iterations: 0, scores: [], final_score: null, status: "PENDING", escalated: false }
  "1C": { iterations: 0, scores: [], final_score: null, status: "PENDING", escalated: false }
  "1D": { iterations: 0, scores: [], final_score: null, status: "PENDING", escalated: false }
  "3A": { iterations: 0, scores: [], final_score: null, status: "PENDING", escalated: false }
  "3B": { iterations: 0, scores: [], final_score: null, status: "PENDING", escalated: false }
  "3C": { iterations: 0, scores: [], final_score: null, status: "PENDING", escalated: false }
  "3D": { iterations: 0, scores: [], final_score: null, status: "PENDING", escalated: false }
  "3E": { iterations: 0, scores: [], final_score: null, status: "PENDING", escalated: false }
  "5A": { iterations: 0, scores: [], final_score: null, status: "PENDING", escalated: false }
  "5B": { iterations: 0, scores: [], final_score: null, status: "PENDING", escalated: false }
  "5C": { iterations: 0, scores: [], final_score: null, status: "PENDING", escalated: false }
  "7A": { iterations: 0, scores: [], final_score: null, status: "PENDING", escalated: false }
  "7B": { iterations: 0, scores: [], final_score: null, status: "PENDING", escalated: false }

quality:
  barrier_threshold: 0.95
  stream_threshold: 0.94
  criticality: "C4"
  scoring_mechanism: "S-014"
  required_strategies:
    - "S-001"  # Red Team Analysis
    - "S-002"  # Devil's Advocate
    - "S-003"  # Steelman Technique
    - "S-010"  # Self-Refine (H-15 — self-review before critic)
    - "S-004"  # Pre-Mortem Analysis
    - "S-007"  # Constitutional AI Critique
    - "S-011"  # Chain-of-Verification
    - "S-012"  # FMEA
    - "S-013"  # Inversion Technique
    - "S-014"  # LLM-as-Judge
  strategy_ordering: "S-010 first (self-review, H-15); S-003 before S-002 (H-16)"
  optional_strategies: []
  max_iterations_per_stream: 5
  min_iterations_per_stream: 3
  max_iterations_per_barrier_deliverable: 5
  phase_scores: {}     # Populated by orch-tracker
  barrier_scores: {}   # Populated by orch-tracker
  workflow_quality: {} # Populated by orch-tracker (aggregate metrics)

metrics:
  groups_total: 8
  parallel_groups: 4
  sequential_groups: 4
  streams_total: 14
  quality_gates_total: 5
  quality_cycles_per_stream: "min 3 / max 5"
  quality_cycles_total_max: 70  # 14 streams x 5 max iterations
  agents_unique: 16
  artifacts_primary: 31   # Non-gate deliverables; 14 additional gate score reports = 45 total
```

### Dynamic Path Configuration

All artifact paths use the workflow ID and project ID as dynamic root segments. No hardcoded pipeline names.

| Path Type | Pattern | Example |
|-----------|---------|---------|
| Orchestration base | `orchestration/{workflow.id}/` | `orchestration/harness-impl-20260306-001/` |
| Plan | `orchestration/{workflow.id}/ORCHESTRATION_PLAN.md` | `orchestration/harness-impl-20260306-001/ORCHESTRATION_PLAN.md` |
| State | `orchestration/{workflow.id}/ORCHESTRATION.yaml` | `orchestration/harness-impl-20260306-001/ORCHESTRATION.yaml` |
| Requirements | `projects/{project.id}/requirements/` | `projects/PROJ-036-prompt-regression-harness/requirements/` |
| Design | `projects/{project.id}/design/` | `projects/PROJ-036-prompt-regression-harness/design/` |
| Baselines | `projects/{project.id}/baselines/` | `projects/PROJ-036-prompt-regression-harness/baselines/` |
| Contracts | `projects/{project.id}/contracts/` | `projects/PROJ-036-prompt-regression-harness/contracts/` |
| Quality gates | `projects/{project.id}/quality-gates/{gate-id}/` | `projects/PROJ-036-prompt-regression-harness/quality-gates/gate-1/` |
| Security | `projects/{project.id}/security/` | `projects/PROJ-036-prompt-regression-harness/security/` |
| Verification | `projects/{project.id}/verification/` | `projects/PROJ-036-prompt-regression-harness/verification/` |
| Reviews | `projects/{project.id}/reviews/` | `projects/PROJ-036-prompt-regression-harness/reviews/` |
| Synthesis | `projects/{project.id}/synthesis/` | `projects/PROJ-036-prompt-regression-harness/synthesis/` |
| Implementation notes | `projects/{project.id}/implementation/` | `projects/PROJ-036-prompt-regression-harness/implementation/` |
| Implementation code (layer 1) | `.github/workflows/`, `tests/prompt-regression/`, `docker/promptfoo/` | (repo root relative) |
| Implementation code (layers 2-4) | `jerry/testing/` | `jerry/testing/evaluation/`, `jerry/testing/metamorphic/`, etc. |
| Test code | `tests/prompt-regression/unit/`, `property/`, `integration/` | (repo root relative) |
| CI/CD | `.github/workflows/`, `.github/actions/` | (repo root relative) |

### Agent Invocation Configuration

All agents are invoked via the Task tool from the main context (orchestrator window) with `run_in_background: true`. The orchestrator never blocks on any agent — it launches tasks, polls for completion via TaskOutput, and collects results. This keeps the main context clean and dedicated to coordination.

**Per-stream adversarial review execution model:** Per P-003 (H-01), creator agents CANNOT spawn adv-scorer or adv-executor as sub-tasks. The per-stream quality cycle is orchestrated from the main context:

1. Orchestrator launches creator agent (run_in_background: true) and polls TaskOutput for completion.
2. Orchestrator reads creator output artifact.
3. Orchestrator launches adv-scorer against creator output (run_in_background: true) and polls TaskOutput for completion.
4. Orchestrator reads adv-scorer result.
5. If score < 0.94 and iteration < 5: orchestrator launches adv-executor (run_in_background: true) to generate critique, collects via TaskOutput, then relaunches creator with critique context. Repeat from step 3.
6. If score >= 0.94: stream is eligible for barrier gate.
7. If score < 0.94 and iteration = 5: escalate to human per H-31.

This means parallel streams within a group are still parallel at the group level, but each stream's adversarial review cycle runs sequentially within that stream's lifecycle. Sequential ordering is enforced by the orchestrator's poll-then-proceed pattern, not by foreground blocking.

| Agent | Subagent Type | Tier | Invocation Mode |
|-------|--------------|------|-----------------|
| jerry:nse-requirements | jerry:nse-requirements | T4 | Task, run_in_background: true (parallel creator) |
| jerry:eng-architect | jerry:eng-architect | T3 | Task, run_in_background: true (parallel creator) |
| jerry:nse-architecture | jerry:nse-architecture | T4 | Task, run_in_background: true (parallel creator) |
| jerry:eng-lead | jerry:eng-lead | T3 | Task, run_in_background: true (parallel creator) |
| jerry:eng-qa | jerry:eng-qa | T2 | Task, run_in_background: true (parallel creator) |
| jerry:eng-backend | jerry:eng-backend | T2 | Task, run_in_background: true (parallel creator) |
| jerry:eng-devsecops | jerry:eng-devsecops | T3 | Task, run_in_background: true (sequential coordination within stream) |
| jerry:adv-scorer | jerry:adv-scorer | T1 | Task, run_in_background: true (per-stream cycle AND barrier gates) |
| jerry:adv-executor | jerry:adv-executor | T1 | Task, run_in_background: true (per-stream cycle AND barrier gates) |
| jerry:red-lead | jerry:red-lead | T3 | Task, run_in_background: true (parallel creator) |
| jerry:red-vuln | jerry:red-vuln | T2 | Task, run_in_background: true (parallel creator) |
| jerry:red-exploit | jerry:red-exploit | T2 | Task, run_in_background: true (parallel creator) |
| jerry:nse-verification | jerry:nse-verification | T1 | Task, run_in_background: true (parallel creator) |
| jerry:nse-reviewer | jerry:nse-reviewer | T1 | Task, run_in_background: true (sequential barrier gate) |
| jerry:eng-reviewer | jerry:eng-reviewer | T1 | Task, run_in_background: true (parallel creator) |
| jerry:ps-synthesizer | jerry:ps-synthesizer | T2 | Task, run_in_background: true (parallel creator) |

### Recovery Strategies

| Scenario | Recovery Action |
|----------|----------------|
| **Per-Stream Recovery** | |
| Any stream score < 0.94 after 5 iterations | Log blocker in WORKTRACKER.md with adv-scorer score and adv-executor critique findings; escalate to human per H-31; do NOT pass deliverable to its barrier gate; halt that stream's eligibility |
| Per-stream plateau detection (delta < 0.01 for 3 consecutive iterations) | Early halt within stream; present best-so-far score with plateau evidence to human per H-31; do not continue consuming iterations |
| **Barrier Gate Recovery** | |
| Group 1 barrier score < 0.95 after 5 iterations | Log blocker in WORKTRACKER.md with specific critique findings; escalate to human per H-31; halt workflow |
| Group 3 barrier score < 0.95 after 5 iterations | Return to producing eng-backend or eng-devsecops agent with critic findings; max 5 total barrier-level iterations; escalate on 5th failure per H-31 |
| Group 5 barrier score < 0.95 after 5 iterations | Return to producing agent with critique; escalate on 5th failure per H-31 |
| Group 7 barrier score < 0.95 at Gate 4A | Return to eng-reviewer or ps-synthesizer with critique; max 5 combined iterations |
| Gate B (nse-reviewer) fails | Return to eng-reviewer + ps-synthesizer with nse-reviewer findings; max 3 combined Gate A+B iterations; escalate on 3rd combined failure |
| **Structural Recovery** | |
| Circuit breaker fires (3-hop limit, H-36) | Halt routing; log full routing_history; present current best to human; ask for guidance per H-31 |
| H-10 violation detected in implementation | Reject deliverable immediately; return to producing agent with specific file(s) to split; this resets the per-stream adversarial cycle (counts as iteration 1) |
| H-11 violation (missing type hints or docstrings) | Reject deliverable; return with specific function list requiring annotation; resets per-stream cycle |
| H-07 violation (layer isolation breach) | Reject deliverable; return with specific import chain to remove; resets per-stream cycle |
| N < 20 enforcement in statistical module | adv-executor flags; return to eng-backend with explicit N >= 20 contract to implement |
| Debiasing not implemented in DeepEval layer | adv-executor flags as C4 quality failure; return to eng-backend with position randomization and rubric shuffling requirements |
| Security finding CRITICAL from red-lead | Halt Group 5 barrier gate; return immediately to relevant Group 3 producing agent; do not score Group 5 outputs until remediation complete and per-stream adversarial cycle re-run for affected 5A output |
| Context window compaction during long agent session | Agent checkpoints to artifact file before compaction; orchestrator resumes from artifact on restart; AE-006e applies |
| MCP Memory-Keeper unavailable at phase boundary | Persist phase summary to `work/.mcp-fallback/{phase-id}.md`; note failure in WORKTRACKER.md; continue |

---

## Quality Gate Definitions

### Criticality Assessment

**Workflow criticality: C4 (Critical)**

| Factor | Assessment | Determination |
|--------|-----------|---------------|
| Reversibility | Implementation commits to repository; architectural pattern affects all 67 agent definitions; cannot be easily undone | Irreversible |
| File scope | >10 files across jerry/testing/, .github/workflows/, tests/, docker/, projects/PROJ-036/ | Well above C3 threshold |
| Impact | Architecture for prompt regression safety; affects every future prompt change to any agent definition | Architecture-level |
| Public/governance | Shared statistical module with PROJ-017; CI/CD gates enforce in public repository | Cross-project impact |
| Auto-escalation check | AE-005 applies (security-relevant code — statistical engine, CI/CD gates) — auto-C3 minimum; irreversibility and architectural scope auto-escalate to C4 | C4 confirmed |

**C4 required strategies (all 10, per quality-enforcement.md):**

| Strategy ID | Strategy Name | Application in This Workflow |
|-------------|--------------|------------------------------|
| S-001 | Red Team Analysis | Group 5A (full security engagement); applied by adv-executor at all per-stream cycles AND all 4 barrier gates |
| S-002 | Devil's Advocate | Applied after steelman (H-16) in all per-stream cycles AND all 4 barrier gates — challenges all design assumptions |
| S-003 | Steelman Technique | Applied before devil's advocate (H-16) in all per-stream cycles AND all 4 barrier gates |
| S-004 | Pre-Mortem Analysis | Applied by adv-executor in all per-stream cycles AND all 4 barrier gates — failure scenario enumeration |
| S-007 | Constitutional AI Critique | Applied by adv-executor in all per-stream cycles AND all 4 barrier gates — P-003, P-020, P-022 checks |
| S-010 | Self-Refine | REQUIRED by producing agent before handing to adv-scorer for first iteration (H-15); applied in all per-stream cycles |
| S-011 | Chain-of-Verification | Applied by adv-executor in all per-stream cycles AND all 4 barrier gates — claim traceability checks |
| S-012 | FMEA | Embedded in Stream 1A (requirements FMEA), Stream 1B (STRIDE threat model), Stream 5A (attack surface FMEA), Stream 5B (FMEA mitigation V&V); applied by adv-executor in all per-stream cycles |
| S-013 | Inversion Technique | Applied by adv-executor in all per-stream cycles AND all 4 barrier gates — "how would this fail?" |
| S-014 | LLM-as-Judge | Applied by adv-scorer in all per-stream cycles (>= 0.94) AND all 4 barrier gates (>= 0.95) — 6-dimension scoring |

**C4 optional strategies:** None (all 10 are required at C4 per quality-enforcement.md).

### Per-Stream Quality Cycle

The per-stream adversarial review cycle runs within each creator stream before the stream is eligible for its barrier gate. This is Tier 1 of the two-tier quality model.

| Parameter | Value | Source |
|-----------|-------|--------|
| Threshold | >= 0.94 weighted composite (S-014) | C4 criticality, elevated from H-13 baseline of 0.92 |
| Minimum iterations | 3 | H-14 (creator-critic-revision cycle) |
| Maximum iterations | 5 | C4 ceiling per RT-M-010 |
| Strategy ordering | S-010 self-review first (H-15), then S-003 steelman before S-002 devil's advocate (H-16) | H-15, H-16 |
| All 10 C4 strategies | Required | quality-enforcement.md C4 |
| On plateau | Delta < 0.01 for 3 consecutive iterations: early halt, escalate to human per H-31 | RT-M-010 |
| On max iterations exceeded | Escalate to human per H-31; do NOT pass to barrier gate | H-31 |
| Critic agents | adv-scorer (S-014 scoring) + adv-executor (critique generation) | /adversary skill |
| Applies to streams | 1A, 1B, 1C, 1D, 3A, 3B, 3C, 3D, 3E, 5A, 5B, 5C, 7A, 7B (all 14 creator streams) | This plan |

**Execution flow per stream:**

```
Creator Agent
    │
    ├── S-010 Self-Review (H-15) — creator reviews own output before submission
    │
    ▼
adv-scorer [Iteration N]
    │
    ├── PASS (>= 0.94) → Stream deliverable is barrier-gate eligible
    │
    └── FAIL (< 0.94)
         │
         ├── Iteration < 5 → adv-executor generates critique using S-003, S-002,
         │                    and remaining C4 strategies
         │                    Creator revises based on critique
         │                    Loop back to adv-scorer (Iteration N+1)
         │
         └── Iteration = 5 → Escalate to human (H-31)
                              Do NOT pass to barrier gate
```

### Quality Gate Parameters Per Barrier

> Barrier gates serve as **cross-deliverable consistency reviews**. Individual quality is pre-validated at >= 0.94 per stream. Barrier gates verify that the group's outputs are mutually consistent, architecturally aligned, and collectively complete.

| Barrier | Gate ID | Deliverables Scored | Consistency Focus | Required Strategies | Threshold | Max Iter | Precondition | Additional Checks |
|---------|---------|--------------------|--------------------|---------------------|-----------|----------|--------------|-------------------|
| Barrier 1 | QG-1 | 4 (streams 1A, 1B, 1C, 1D) | Requirements / design / baselines / contracts mutual consistency | All 10 C4 strategies | >= 0.95 each | 5 per deliverable | All 4 streams at >= 0.94 | None |
| Barrier 2 | QG-2 | 5 (streams 3A, 3B, 3C, 3D, 3E) | Implementation layers mutually consistent with architecture | All 10 C4 strategies | >= 0.95 each | 5 per deliverable | All 5 streams at >= 0.94 | H-10, H-11, H-07, N>=20, debiasing |
| Barrier 3 | QG-3 | 3 (streams 5A, 5B, 5C) | Security + V&V + tests form complete assurance picture | All 10 C4 strategies | >= 0.95 each | 5 per deliverable | All 3 streams at >= 0.94 | 90% coverage verified (5C) |
| Barrier 4 Gate A | QG-4A | Complete package | All prior outputs form coherent implementation | All 10 C4 strategies | >= 0.95 | 5 | Both 7A, 7B at >= 0.94 | Full traceability chain |
| Barrier 4 Gate B | QG-4B | Complete package | Requirements traceability complete | NPR 7123.1D Appendix G | PASS | 3 combined A+B | Gate A PASS | Requirements traceability matrix |

### S-014 Scoring Dimensions

| Dimension | Weight | Description |
|-----------|--------|-------------|
| Completeness | 0.20 | All required items present; all specification fields populated; all ADR-001 phases A-D addressed |
| Internal Consistency | 0.20 | Implementation choices do not contradict ADR-001 decisions; layer boundaries respected; no conflicting interface definitions |
| Methodological Rigor | 0.20 | Correct statistical methods applied (Wilcoxon, Wilson, Bonferroni); debiasing correctly implemented; MR definitions correctly specify transformation + consistency relation |
| Evidence Quality | 0.15 | Implementation choices trace to ADR-001 evidence; no unjustified divergence from architecture |
| Actionability | 0.15 | Artifacts deployable without additional design work; runbooks and operational guidance present |
| Traceability | 0.10 | Every module traces to an ADR-001 layer; every requirement traces to an implementation artifact; every FMEA failure mode traces to a mitigation |

### Creator-Critic Agent Assignments

**Tier 1 — Per-Stream (embedded, runs before barrier eligibility):**

| Group | Stream | Creator | Per-Stream Critic | Per-Stream Threshold | Per-Stream Max Iter |
|-------|--------|---------|-------------------|----------------------|---------------------|
| 1 | 1A | nse-requirements | adv-scorer + adv-executor | >= 0.94 | 5 |
| 1 | 1B | eng-architect, nse-architecture, eng-lead | adv-scorer + adv-executor | >= 0.94 | 5 |
| 1 | 1C | eng-qa | adv-scorer + adv-executor | >= 0.94 | 5 |
| 1 | 1D | nse-requirements | adv-scorer + adv-executor | >= 0.94 | 5 |
| 3 | 3A | eng-backend | adv-scorer + adv-executor | >= 0.94 | 5 |
| 3 | 3B | eng-backend | adv-scorer + adv-executor | >= 0.94 | 5 |
| 3 | 3C | eng-backend | adv-scorer + adv-executor | >= 0.94 | 5 |
| 3 | 3D | eng-backend | adv-scorer + adv-executor | >= 0.94 | 5 |
| 3 | 3E | eng-devsecops | adv-scorer + adv-executor | >= 0.94 | 5 |
| 5 | 5A | red-lead, red-vuln, red-exploit | adv-scorer + adv-executor | >= 0.94 | 5 |
| 5 | 5B | nse-verification | adv-scorer + adv-executor | >= 0.94 | 5 |
| 5 | 5C | eng-qa | adv-scorer + adv-executor | >= 0.94 | 5 |
| 7 | 7A | eng-reviewer | adv-scorer + adv-executor | >= 0.94 | 5 |
| 7 | 7B | ps-synthesizer | adv-scorer + adv-executor | >= 0.94 | 5 |

**Tier 2 — Barrier Gate (cross-deliverable consistency, runs after all streams in group PASS Tier 1):**

| Group | Gate ID | Deliverables | Barrier Critic | Barrier Threshold | Barrier Max Iter |
|-------|---------|-------------|----------------|-------------------|-----------------|
| 2 | QG-1 | 1A, 1B, 1C, 1D | adv-scorer + adv-executor | >= 0.95 each | 5 per deliverable |
| 4 | QG-2 | 3A, 3B, 3C, 3D, 3E | adv-scorer + adv-executor | >= 0.95 each | 5 per deliverable |
| 6 | QG-3 | 5A, 5B, 5C | adv-scorer + adv-executor | >= 0.95 each | 5 per deliverable |
| 8 | QG-4A | Complete package | adv-scorer | >= 0.95 | 5 |
| 8 | QG-4B | Complete package | nse-reviewer | NPR 7123.1D PASS | 3 combined A+B |

---

## Output Map

### Group 1 Outputs

| Stream | Artifact ID | Path | Consuming Groups |
|--------|------------|------|-----------------|
| 1A | ART-1A-REQS | `projects/PROJ-036-prompt-regression-harness/requirements/harness-requirements.md` | Group 2 (gate), Group 3 (3A-3E input), Group 5 (5B V&V), Group 8 |
| 1B | ART-1B-DESIGN | `projects/PROJ-036-prompt-regression-harness/design/system-design.md` | Group 2 (gate), Group 3 (3A-3E input), Group 5 (5A, 5B), Group 7, Group 8 |
| 1C | ART-1C-PROTOCOL | `projects/PROJ-036-prompt-regression-harness/baselines/protocol.md` | Group 2 (gate), Group 3 (3A, 3D reference), Group 5 (5B), Group 8 |
| 1C | ART-1C-SCHEMAS | `projects/PROJ-036-prompt-regression-harness/baselines/schemas/` | Group 3 (3D), Group 5 (5B, 5C) |
| 1C | ART-1C-PROMPTS | `projects/PROJ-036-prompt-regression-harness/baselines/prompts/` | Group 3 (3A, 3B), Group 5 (5A, 5C) |
| 1D | ART-1D-CONTRACTS | `projects/PROJ-036-prompt-regression-harness/contracts/behavioral-contracts.md` | Group 2 (gate), Group 3 (3C MR tolerances, 3D thresholds), Group 5, Group 8 |
| 1D | ART-1D-SCHEMAS | `projects/PROJ-036-prompt-regression-harness/contracts/schemas/` | Group 3 (3C, 3D), Group 5 (5B) |
| 1D | ART-1D-PER-AGENT | `projects/PROJ-036-prompt-regression-harness/contracts/per-agent/` | Group 3 (3C), Group 5 (5C) |

### Group 2 Outputs (Quality Gate 1)

| Gate | Artifact ID | Path |
|------|------------|------|
| QG-1 | ART-QG1-1A | `projects/PROJ-036-prompt-regression-harness/quality-gates/gate-1/score-1a-requirements.md` |
| QG-1 | ART-QG1-1B | `projects/PROJ-036-prompt-regression-harness/quality-gates/gate-1/score-1b-design.md` |
| QG-1 | ART-QG1-1C | `projects/PROJ-036-prompt-regression-harness/quality-gates/gate-1/score-1c-baselines.md` |
| QG-1 | ART-QG1-1D | `projects/PROJ-036-prompt-regression-harness/quality-gates/gate-1/score-1d-contracts.md` |

### Group 3 Outputs

| Stream | Artifact ID | Path | Consuming Groups |
|--------|------------|------|-----------------|
| 3A | ART-3A-GHA | `.github/workflows/prompt-regression-*.yml` | Group 4 (gate), Group 5 (5A, 5B), Group 7 |
| 3A | ART-3A-YAML | `tests/prompt-regression/*.yaml` | Group 4 (gate), Group 5 (5A, 5C) |
| 3A | ART-3A-DOCKER | `docker/promptfoo/Dockerfile` | Group 4 (gate), Group 5 (5A) |
| 3B | ART-3B-EVAL | `jerry/testing/evaluation/` | Group 4 (gate), Group 5 (5A, 5C) |
| 3C | ART-3C-MR | `jerry/testing/metamorphic/` | Group 4 (gate), Group 5 (5A, 5C) |
| 3D | ART-3D-STATS | `jerry/testing/stats.py`, `jerry/testing/types.py` | Group 4 (gate), Group 5 (5A, 5B, 5C), PROJ-017 |
| 3D | ART-3D-BASELINES | `jerry/testing/baselines/` | Group 4 (gate), Group 5 (5B, 5C) |
| 3D | ART-3D-REPORTS | `jerry/testing/reports/` | Group 4 (gate), Group 7, Group 8 |
| 3E | ART-3E-CICD | `.github/workflows/prompt-regression-*.yml` (full tier), `.github/actions/` | Group 4 (gate), Group 5 (5A), Group 7 |

### Group 4 Outputs (Quality Gate 2)

| Gate | Artifact ID | Path |
|------|------------|------|
| QG-2 | ART-QG2-3A | `projects/PROJ-036-prompt-regression-harness/quality-gates/gate-2/score-3a-promptfoo.md` |
| QG-2 | ART-QG2-3B | `projects/PROJ-036-prompt-regression-harness/quality-gates/gate-2/score-3b-deepeval.md` |
| QG-2 | ART-QG2-3C | `projects/PROJ-036-prompt-regression-harness/quality-gates/gate-2/score-3c-metamorphic.md` |
| QG-2 | ART-QG2-3D | `projects/PROJ-036-prompt-regression-harness/quality-gates/gate-2/score-3d-stats.md` |
| QG-2 | ART-QG2-3E | `projects/PROJ-036-prompt-regression-harness/quality-gates/gate-2/score-3e-cicd.md` |

### Group 5 Outputs

| Stream | Artifact ID | Path | Consuming Groups |
|--------|------------|------|-----------------|
| 5A | ART-5A-SECURITY | `projects/PROJ-036-prompt-regression-harness/security/security-assessment.md` | Group 6 (gate), Group 7, Group 8 |
| 5A | ART-5A-FINDINGS | `projects/PROJ-036-prompt-regression-harness/security/findings/` | Group 6 (gate), Group 7 |
| 5A | ART-5A-REMEDIATIONS | `projects/PROJ-036-prompt-regression-harness/security/remediations.md` | Group 6 (gate), Group 7 |
| 5B | ART-5B-COVERAGE | `projects/PROJ-036-prompt-regression-harness/verification/requirements-coverage-matrix.md` | Group 6 (gate), Group 7, Group 8 |
| 5B | ART-5B-INTERFACE | `projects/PROJ-036-prompt-regression-harness/verification/interface-verification.md` | Group 6 (gate), Group 7 |
| 5B | ART-5B-CONSTRAINT | `projects/PROJ-036-prompt-regression-harness/verification/constraint-verification.md` | Group 6 (gate), Group 7 |
| 5B | ART-5B-FMEA | `projects/PROJ-036-prompt-regression-harness/verification/fmea-mitigation-verification.md` | Group 6 (gate), Group 7, Group 8 |
| 5C | ART-5C-UNIT | `tests/prompt-regression/unit/` | Group 6 (gate), Group 7 |
| 5C | ART-5C-PROPERTY | `tests/prompt-regression/property/` | Group 6 (gate), Group 7 |
| 5C | ART-5C-INTEGRATION | `tests/prompt-regression/integration/` | Group 6 (gate), Group 7 |

### Group 6 Outputs (Quality Gate 3)

| Gate | Artifact ID | Path |
|------|------------|------|
| QG-3 | ART-QG3-5A | `projects/PROJ-036-prompt-regression-harness/quality-gates/gate-3/score-5a-security.md` |
| QG-3 | ART-QG3-5B | `projects/PROJ-036-prompt-regression-harness/quality-gates/gate-3/score-5b-verification.md` |
| QG-3 | ART-QG3-5C | `projects/PROJ-036-prompt-regression-harness/quality-gates/gate-3/score-5c-tests.md` |

### Group 7 Outputs

| Stream | Artifact ID | Path | Consuming Groups |
|--------|------------|------|-----------------|
| 7A | ART-7A-REVIEW | `projects/PROJ-036-prompt-regression-harness/reviews/engineering-review.md` | Group 8 |
| 7B | ART-7B-SYNTHESIS | `projects/PROJ-036-prompt-regression-harness/synthesis/implementation-synthesis.md` | Group 8 |
| 7B | ART-7B-RISK | `projects/PROJ-036-prompt-regression-harness/synthesis/risk-register-updated.md` | Group 8, Human Review |
| 7B | ART-7B-OPREADINESS | `projects/PROJ-036-prompt-regression-harness/synthesis/operational-readiness.md` | Group 8, Human Review |

### Group 8 Outputs (Final Gate)

| Gate | Artifact ID | Path |
|------|------------|------|
| QG-4A | ART-QG4A | `projects/PROJ-036-prompt-regression-harness/quality-gates/gate-final/gate-a-adversarial-score.md` |
| QG-4B | ART-QG4B | `projects/PROJ-036-prompt-regression-harness/quality-gates/gate-final/gate-b-nse-review.md` |

---

## Constraints

> NPT-013 format — constraints governing all agent execution in this workflow.

| ID | Constraint |
|----|-----------|
| C-001 | NEVER use the general-purpose or Explore subagent_type. All agents MUST be invoked via named jerry:{agent-name} subagent_type format. |
| C-002 | NEVER invoke agents that spawn further subagents (P-003). All agents are workers; the main context is the sole orchestrator. Consequence: recursive spawning causes unbounded recursion and violates H-01. |
| C-003 | NEVER proceed past a quality gate with any deliverable scoring below 0.95. The workflow halts and returns the specific below-threshold deliverable to its producing agent for targeted revision. Other above-threshold deliverables in the same gate batch are not re-run. |
| C-004 | NEVER run Group 8 Gate B (nse-reviewer) without Gate A (adv-scorer) first passing at >= 0.95. Gate order is mandatory. |
| C-005 | NEVER present the final implementation to the human without BOTH Gate A (>= 0.95) AND Gate B (NPR 7123.1D PASS) scoring in Group 8. |
| C-006 | NEVER allow Stream 3D statistical implementations to use point-estimate thresholds as a substitute for Wilcoxon signed-rank testing. Point-estimate thresholds are structurally invalid for small-N LLM evaluation per ADR-001 Force F-2. |
| C-007 | NEVER allow Stream 3B DeepEval implementation to skip debiasing (position randomization + rubric shuffling). Vanilla LLM-as-Judge without debiasing is explicitly rejected by ADR-001 Force F-5. adv-executor will flag this as a C4 quality failure at Gate QG-2. |
| C-008 | NEVER allow N < 20 runs for any statistical comparison in the harness. The minimum sample size for Wilcoxon signed-rank test validity is N = 20. Implementations MUST enforce this with ValueError at function entry. |
| C-009 | NEVER violate H-10 (one class per file), H-11 (type hints + docstrings), or H-07 (layer isolation) in any implementation artifact. Violations cause immediate deliverable rejection at Gate QG-2 regardless of other scores. |
| C-010 | NEVER run Group 3 parallel streams until Barrier 1 (QG-1) reports ALL 4 Group 1 outputs at >= 0.95. Implementation on an unreviewed architectural foundation is forbidden. |
| C-011 | NEVER run Group 5 parallel streams until Barrier 2 (QG-2) reports ALL 5 Group 3 outputs at >= 0.95. Security assessment and V&V of unreviewed implementation is invalid. |
| C-012 | NEVER allow the red-team engagement (Stream 5A) to modify implementation code. Stream 5A is assessment-only. Remediations are planned in 5A outputs and implemented as revisions to Group 3 artifacts through the QG-2 revision cycle. |
| C-013 | NEVER allow Human Review (P-020) to be bypassed or deferred. Human acceptance is a mandatory terminal step. AI quality gate scores are advisory inputs to human judgment, not substitutes for it. |
| C-014 | NEVER hardcode the workflow ID or project ID in any artifact path. Use dynamic identifiers per the path configuration scheme in this plan. |
| C-015 | NEVER skip Memory-Keeper store at phase boundaries per MCP-002. On MCP failure, persist to `projects/PROJ-036-prompt-regression-harness/work/.mcp-fallback/{phase-id}.md`. |
| C-016 | NEVER pass a stream deliverable to its barrier gate without first achieving >= 0.94 per-stream adversarial score. Below-threshold deliverables do not participate in barrier gate scoring. A barrier gate MUST NOT start until ALL of its contributing streams have PASSED their per-stream quality cycle at >= 0.94. |
| C-017 | NEVER have a creator agent directly invoke adv-scorer or adv-executor (P-003/H-01). The per-stream adversarial review cycle is orchestrated exclusively from the main context. Creator agents produce output; the orchestrator reads that output and launches adv-scorer and adv-executor as separate sequential Task invocations. |
| C-018 | NEVER skip S-010 self-review (H-15) before submitting a stream deliverable to adv-scorer for the first iteration. The self-review is the creator's responsibility before handing off to the critic. |

---

## Disclaimer

This orchestration plan was generated by the orch-planner agent for PROJ-036-prompt-regression-harness / FEAT-036-001. It represents a planned workflow; execution sequences, agent assignments, and artifact paths are subject to revision during execution. Human review is required before execution begins per P-020 (user authority). Human acceptance is also required after execution completes (Group 8 final step). This plan does not constitute official NASA guidance.

> **P-043 Notice:** This document was generated by an AI orchestration planner. All implementation artifacts produced by this workflow require human review and acceptance per P-020. Quality gate scores produced by adv-scorer are advisory inputs to human judgment, not binding approvals. The 67 agent definitions affected by this architecture remain under human authority at all times.
