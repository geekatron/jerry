# FEAT-035-001 Test Harness Research: Orchestration Plan

> **Document ID:** PROJ-035-ORCH-PLAN
> **Workflow ID:** test-harness-research-20260306-001
> **Feature:** FEAT-035-001 — Test Harness for LLM Prompt Evaluation and Safe Refactoring
> **Date:** 2026-03-06
> **Status:** PLANNED
> **Criticality:** C2 (Standard — reversible in 1 day, 3-10 files)
> **Quality Threshold:** >= 0.92 weighted composite (S-014 LLM-as-Judge)

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Workflow Overview](#l0-workflow-overview) | Summary for stakeholders |
| [L1: Technical Plan](#l1-technical-plan) | Workflow diagram, phase definitions, agents, barriers |
| [L2: Implementation Details](#l2-implementation-details) | State schema, path configuration, recovery strategies |
| [Quality Gate Definitions](#quality-gate-definitions) | Criticality, strategies, thresholds per barrier |
| [Constraints](#constraints) | NPT-013 execution constraints |
| [Disclaimer](#disclaimer) | P-043 mandatory disclaimer |

---

## L0: Workflow Overview

This workflow researches the landscape of LLM prompt testing methodologies, frameworks, and architectures to produce a grounded Architecture Decision Record (ADR) for the Jerry framework test harness (FEAT-035-001). The research runs four parallel streams simultaneously — historical methods, industry frameworks, agent SDKs, and innovation patterns — then cross-pollinates their findings into a synthesis, evaluates the best combination via structured analysis, and culminates in a formal ADR with a dual quality gate.

The outcome is a defensible, evidence-based architecture recommendation that tells the Jerry team which tools and approaches to adopt for safe LLM prompt refactoring and regression testing. Every claim in the final ADR traces back to externally verified sources. No tool is recommended without a verified OSI-approved open-source license. The human reviews and accepts the ADR only after both the automated quality scorer and the NASA SE technical reviewer pass it.

---

## L1: Technical Plan

### Workflow Diagram (ASCII)

```
PROJ-035 / FEAT-035-001: Test Harness Research Pipeline
Workflow ID: test-harness-research-20260306-001
Pattern: Fan-Out (Phase 1) -> Sequential with Quality Gates -> Fan-In (Phase 3) -> Sequential
===================================================================================

    ┌─────────────────────────────────────────────────────────────────────┐
    │                   PHASE 1: PARALLEL RESEARCH (Fan-Out)              │
    │                    Execution Group 1 — CONCURRENT                   │
    │                                                                      │
    │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
    │  │  STREAM 1A   │  │  STREAM 1B   │  │  STREAM 1C   │  │  STREAM 1D   │ │
    │  │ps-researcher │  │ps-researcher │  │ps-researcher │  │ps-researcher │ │
    │  │              │  │              │  │              │  │              │ │
    │  │ Historical   │  │ Industry     │  │ Agent SDK    │  │ Innovation   │ │
    │  │ Testing      │  │ Frameworks   │  │ Evaluation   │  │ Frameworks   │ │
    │  │ Methodologies│  │ Survey       │  │              │  │ (AI/LLM)     │ │
    │  │              │  │ (min 10:     │  │ (min 6 SDKs) │  │              │ │
    │  │ (min 8       │  │  5 trad +    │  │              │  │ (min 8       │ │
    │  │  distinct)   │  │  5 LLM/AI)   │  │              │  │  areas)      │ │
    │  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘ │
    └─────────┼─────────────────┼─────────────────┼─────────────────┼──────────┘
              │                 │                 │                 │
              │   historical-   │  industry-      │  agent-sdk-     │  innovation-
              │   testing-      │  frameworks-    │  evaluation.md  │  frameworks.md
              │   methodologies.│  survey.md      │                 │
              │   md            │                 │                 │
              └─────────────────┴────────┬────────┴─────────────────┘
                                         │ (all 4 outputs ready)
                                         ▼
                             ╔══════════════════════════╗
                             ║   BARRIER 1 / PHASE 2    ║
                             ║   Quality Gate 1         ║
                             ║   Agent: adv-scorer      ║
                             ║   Scores each of 4       ║
                             ║   research outputs       ║
                             ║   S-014 >= 0.92          ║
                             ║   Max 3 iterations each  ║
                             ╚══════════════╤═══════════╝
                                            │ (all 4 PASS)
                                            ▼
                             ┌──────────────────────────┐
                             │   PHASE 3: SYNTHESIS     │
                             │   (Fan-In)               │
                             │   Agent: ps-synthesizer  │
                             │                          │
                             │   Cross-pollinate all 4  │
                             │   research streams:      │
                             │   - Method mapping       │
                             │   - Framework matrix     │
                             │   - SDK gap analysis     │
                             │   - Innovation readiness │
                             │   - Convergence patterns │
                             │   - Optimal combination  │
                             └──────────────┬───────────┘
                                            │
                                            ▼
                             ╔══════════════════════════╗
                             ║   BARRIER 2 / PHASE 4    ║
                             ║   Quality Gate 2         ║
                             ║   Agent: adv-scorer      ║
                             ║   S-014 >= 0.92          ║
                             ║   Max 3 iterations       ║
                             ╚══════════════╤═══════════╝
                                            │ (PASS)
                                            ▼
                             ┌──────────────────────────┐
                             │   PHASE 5: ANALYSIS      │
                             │   Agent: ps-analyst      │
                             │                          │
                             │   6-dimension evaluation │
                             │   + FMEA risk analysis   │
                             │   of best combination    │
                             │   for LLM prompt harness │
                             └──────────────┬───────────┘
                                            │
                                            ▼
                             ╔══════════════════════════╗
                             ║   BARRIER 3 / PHASE 6    ║
                             ║   Quality Gate 3         ║
                             ║   Agent: adv-scorer      ║
                             ║   S-014 >= 0.92          ║
                             ║   Max 3 iterations       ║
                             ╚══════════════╤═══════════╝
                                            │ (PASS)
                                            ▼
                             ┌──────────────────────────┐
                             │   PHASE 7: ADR           │
                             │   Agent: ps-architect    │
                             │                          │
                             │   3 options derived from │
                             │   research evidence      │
                             │   (no predetermined      │
                             │    options)              │
                             │   Nygard ADR format      │
                             │   L0/L1/L2 sections      │
                             └──────────────┬───────────┘
                                            │
                                            ▼
                             ╔══════════════════════════╗
                             ║   BARRIER 4 / PHASE 8    ║
                             ║   DUAL Quality Gate      ║
                             ║                          ║
                             ║  Gate A: adv-scorer      ║
                             ║  S-014 >= 0.92           ║
                             ║  Max 3 iterations        ║
                             ║                          ║
                             ║  Gate B: nse-reviewer    ║
                             ║  NPR 7123.1D App. G      ║
                             ║  (both MUST pass)        ║
                             ╚══════════════╤═══════════╝
                                            │ (both gates PASS)
                                            ▼
                             ┌──────────────────────────┐
                             │   HUMAN REVIEW (P-020)   │
                             │   Present full pipeline  │
                             │   results + ADR-001 for  │
                             │   acceptance decision    │
                             └──────────────────────────┘
```

### Pipeline Definition

| Phase | Name | Pattern | Execution Group | Agents | Trigger |
|-------|------|---------|-----------------|--------|---------|
| 1 | Parallel Research | Fan-Out (4 concurrent) | 1 — PARALLEL | ps-researcher (x4) | Workflow start |
| 2 | Quality Gate 1 | Sequential scoring | 2 — SEQUENTIAL | adv-scorer | All Phase 1 outputs complete |
| 3 | Cross-Pollination Synthesis | Fan-In | 3 — SEQUENTIAL | ps-synthesizer | All Phase 2 scores >= 0.92 |
| 4 | Quality Gate 2 | Sequential scoring | 4 — SEQUENTIAL | adv-scorer | Phase 3 output complete |
| 5 | Analytical Evaluation | Sequential | 5 — SEQUENTIAL | ps-analyst | Phase 4 score >= 0.92 |
| 6 | Quality Gate 3 | Sequential scoring | 6 — SEQUENTIAL | adv-scorer | Phase 5 output complete |
| 7 | Architecture Decision | Sequential | 7 — SEQUENTIAL | ps-architect | Phase 6 score >= 0.92 |
| 8 | Final Quality Gate + Review | Dual gate | 8 — SEQUENTIAL | adv-scorer + nse-reviewer | Phase 7 output complete |

### Phase 1 — Parallel Research Streams

#### Stream 1A: Historical Testing Methodologies

| Field | Value |
|-------|-------|
| Agent | jerry:ps-researcher |
| Data Sources | WebSearch (academic papers, conference proceedings, historical surveys), WebFetch (cited sources) |
| Minimum Coverage | 8 distinct methodologies |
| Search Terms | "history of software testing methodologies", "evolution of testing practices", "software testing taxonomy", "testing strategy classification" |
| Per-Methodology Fields | Origin, core mechanism, effectiveness evidence, limitations, LLM prompt testing applicability |
| Completeness Check | If fewer than 8, broaden search terms before completing |
| Output | `projects/PROJ-035-skill-optimization/research/historical-testing-methodologies.md` (L0/L1/L2) |

#### Stream 1B: Industry Top Frameworks

| Field | Value |
|-------|-------|
| Agent | jerry:ps-researcher |
| Data Sources | WebSearch + Context7 (resolve each framework) |
| Minimum Coverage | 10 total (5 traditional code testing + 5 LLM/AI-specific testing) |
| Traditional Search | "most popular testing frameworks 2025 2026", "best testing frameworks by language" |
| LLM/AI Search | "LLM evaluation frameworks", "prompt testing tools", "AI testing frameworks comparison" |
| Per-Framework Fields | Architecture, key capabilities, CI/CD integration, community adoption evidence, suitability for LLM prompt regression testing |
| License Constraint | OSI-approved open-source only; exclude frameworks without verified license |
| Output | `projects/PROJ-035-skill-optimization/research/industry-frameworks-survey.md` (L0/L1/L2) |

#### Stream 1C: Agent SDK Evaluation

| Field | Value |
|-------|-------|
| Agent | jerry:ps-researcher |
| Data Sources | WebSearch + Context7 (resolve each SDK) |
| Minimum Coverage | 6 Agent SDKs |
| Search Terms | "AI agent frameworks 2025 2026", "agent SDK comparison", "multi-agent framework testing capabilities" |
| Per-SDK Fields | Testing API surface, mocking/stubbing support, determinism controls, CI/CD patterns, evaluation framework integration points, gaps for prompt regression testing |
| License Constraint | OSI-approved open-source only |
| Output | `projects/PROJ-035-skill-optimization/research/agent-sdk-evaluation.md` (L0/L1/L2) |

#### Stream 1D: Innovation Frameworks

| Field | Value |
|-------|-------|
| Agent | jerry:ps-researcher |
| Data Sources | WebSearch (including arxiv), WebFetch (cited papers) |
| Minimum Coverage | 8 distinct innovation areas |
| Search Terms | "LLM evaluation methodology 2025 2026", "AI code quality measurement", "novel approaches to LLM testing", "statistical methods for LLM evaluation", "arxiv LLM evaluation framework" |
| Per-Area Fields | Maturity level, adoption evidence, statistical rigor, integration feasibility for Jerry |
| Output | `projects/PROJ-035-skill-optimization/research/innovation-frameworks.md` (L0/L1/L2) |

### Phase 3 — Cross-Pollination Synthesis Tasks

| Task | Description |
|------|-------------|
| 1 | Map historical testing methodologies to LLM testing equivalents |
| 2 | Framework capability matrix (all 10+ frameworks side-by-side) |
| 3 | SDK testing gap analysis (what each SDK lacks for prompt regression) |
| 4 | Innovation readiness assessment (maturity vs. integration cost) |
| 5 | Convergence patterns across 3+ research streams |
| 6 | Optimal combination recommendation for LLM prompt test harness |

### Phase 5 — Analytical Evaluation Dimensions

| Dimension | Description |
|-----------|-------------|
| Refactoring safety | How well the approach guards against accidental regression during prompt edits |
| Migration confidence | Statistical confidence in safe migration across model versions/providers |
| Determinism coverage | Degree to which non-deterministic LLM outputs can be evaluated reliably |
| Statistical rigor | Quality of evaluation metrics, sample sizes, confidence intervals |
| Integration feasibility | Cost and complexity of integrating with Jerry's existing architecture |
| Evidence basis | Strength of real-world adoption evidence supporting the approach |

Prior art to incorporate: PROJ-017 ADR-002 (promptfoo extension architecture recommendation).

### Phase 7 — Architecture Decision Requirements

| Requirement | Detail |
|-------------|--------|
| Options count | 3 (derived from Phase 5 analysis — NOT predetermined) |
| Format | Nygard ADR with L0/L1/L2 sections |
| Evaluation dimensions | refactoring safety, migration confidence, determinism coverage, statistical rigor, integration feasibility, time to first value |
| Prior art | Reference PROJ-017 ADR-002 promptfoo extension architecture |
| Inputs | All Phase 1 research + Phase 3 synthesis + Phase 5 analysis |

### Phase 8 — Dual Quality Gate Requirements

| Gate | Agent | Standard | Checks |
|------|-------|----------|--------|
| Gate A | adv-scorer | S-014 >= 0.92 | 6-dimension scoring; max 3 iterations |
| Gate B | nse-reviewer | NPR 7123.1D Appendix G | Requirements traceability, evidence basis, risk coverage, implementation feasibility |
| Combined | Both | Both MUST pass | Neither gate is optional; pass order is Gate A then Gate B |

### Sync Barriers

| Barrier | ID | Trigger Condition | Gate Agent | Threshold | Failure Action |
|---------|-----|------------------|-----------|-----------|----------------|
| Barrier 1 | QG-1 | All 4 Phase 1 outputs complete | adv-scorer | >= 0.92 each | Return to ps-researcher; max 3 iterations per deliverable |
| Barrier 2 | QG-2 | Phase 3 synthesis complete | adv-scorer | >= 0.92 | Return to ps-synthesizer; max 3 iterations |
| Barrier 3 | QG-3 | Phase 5 analysis complete | adv-scorer | >= 0.92 | Return to ps-analyst; max 3 iterations |
| Barrier 4 | QG-4 | Phase 7 ADR complete | adv-scorer + nse-reviewer | >= 0.92 (both) | Return to ps-architect; max 3 iterations; escalate on 3rd failure |

---

## L2: Implementation Details

### State Schema (ORCHESTRATION.yaml)

See `ORCHESTRATION.yaml` co-located with this plan.

### Dynamic Path Configuration

All artifact paths use the workflow ID as the dynamic root segment. No hardcoded pipeline names.

| Path Type | Pattern | Example |
|-----------|---------|---------|
| Base | `orchestration/{workflow.id}/` | `orchestration/test-harness-research-20260306-001/` |
| Research outputs | `projects/PROJ-035-skill-optimization/research/{artifact}.md` | `research/historical-testing-methodologies.md` |
| Analysis outputs | `projects/PROJ-035-skill-optimization/analysis/{artifact}.md` | `analysis/cross-pollination-synthesis.md` |
| Decision outputs | `projects/PROJ-035-skill-optimization/decisions/{artifact}.md` | `decisions/ADR-001-test-harness-architecture.md` |
| Quality gate scores | `projects/PROJ-035-skill-optimization/work/test-harness/adv/{gate-dir}/` | `work/test-harness/adv/phase-1-scores/` |
| Orchestration state | `orchestration/{workflow.id}/ORCHESTRATION.yaml` | `orchestration/test-harness-research-20260306-001/ORCHESTRATION.yaml` |

### Execution Group Summary

| Group | Mode | Agents | Inputs | Outputs |
|-------|------|--------|--------|---------|
| 1 | PARALLEL | ps-researcher (1A, 1B, 1C, 1D) | WebSearch, WebFetch, Context7 | 4 research markdown files |
| 2 | SEQUENTIAL | adv-scorer | 4 research markdown files | 4 score reports in phase-1-scores/ |
| 3 | SEQUENTIAL | ps-synthesizer | 4 research markdown files | cross-pollination-synthesis.md |
| 4 | SEQUENTIAL | adv-scorer | cross-pollination-synthesis.md | phase-3-score.md |
| 5 | SEQUENTIAL | ps-analyst | synthesis + all Phase 1 research | test-harness-evaluation.md |
| 6 | SEQUENTIAL | adv-scorer | test-harness-evaluation.md | phase-5-score.md |
| 7 | SEQUENTIAL | ps-architect | all Phase 1 + Phase 3 + Phase 5 outputs | ADR-001-test-harness-architecture.md |
| 8 | SEQUENTIAL | adv-scorer + nse-reviewer | ADR-001-test-harness-architecture.md | 2 score/review reports in phase-7-scores/ |

### Recovery Strategies

| Scenario | Recovery Action |
|----------|----------------|
| Phase 1 stream returns fewer than minimum items | Broaden search terms; retry within same stream session |
| Phase 1 stream score < 0.92 after 3 iterations | Log blocker in ORCHESTRATION_WORKTRACKER.md; escalate to human |
| Phase 3 synthesis score < 0.92 after 3 iterations | Log blocker; escalate to human; do not proceed to Phase 5 |
| Phase 5 analysis score < 0.92 after 3 iterations | Log blocker; escalate to human; do not proceed to Phase 7 |
| Phase 7 ADR fails Gate A (adv-scorer) 3 iterations | Log blocker; escalate to human; do not run Gate B |
| Phase 7 ADR fails Gate B (nse-reviewer) | Return to ps-architect with nse-reviewer findings; max 3 combined Gate A+B iterations |
| Context7 returns no results for a library | Fall back to WebSearch; note "Context7 no coverage" in research output |
| Framework lacks verified OSI license | Exclude from research; note exclusion in output with search evidence |

### Artifact Registry

| Artifact ID | Path | Producing Phase | Consuming Phases |
|-------------|------|----------------|-----------------|
| ART-1A | `research/historical-testing-methodologies.md` | Phase 1 (1A) | Phase 2, Phase 3 |
| ART-1B | `research/industry-frameworks-survey.md` | Phase 1 (1B) | Phase 2, Phase 3 |
| ART-1C | `research/agent-sdk-evaluation.md` | Phase 1 (1C) | Phase 2, Phase 3 |
| ART-1D | `research/innovation-frameworks.md` | Phase 1 (1D) | Phase 2, Phase 3 |
| ART-QG1 | `work/test-harness/adv/phase-1-scores/` | Phase 2 | — |
| ART-3 | `analysis/cross-pollination-synthesis.md` | Phase 3 | Phase 4, Phase 5 |
| ART-QG2 | `work/test-harness/adv/phase-3-score.md` | Phase 4 | — |
| ART-5 | `analysis/test-harness-evaluation.md` | Phase 5 | Phase 6, Phase 7 |
| ART-QG3 | `work/test-harness/adv/phase-5-score.md` | Phase 6 | — |
| ART-7 | `decisions/ADR-001-test-harness-architecture.md` | Phase 7 | Phase 8 |
| ART-QG4 | `work/test-harness/adv/phase-7-scores/` | Phase 8 | Human review |

All paths are relative to `projects/PROJ-035-skill-optimization/`.

---

## Quality Gate Definitions

### Criticality Assessment

**Workflow criticality: C2 (Standard)**

| Factor | Assessment | Determination |
|--------|-----------|---------------|
| Reversibility | Research + ADR artifact; reversible within 1 day by deleting and re-running | Supports C2 |
| File scope | ~10 output files (4 research + 2 analysis + 1 ADR + score reports) | At C2 upper boundary |
| Impact | ADR informs architecture decision for FEAT-035-001; no public/governance impact | Supports C2 |
| Auto-escalation check | Does not touch `docs/governance/`, `.context/rules/`, or baselined ADRs | No AE rule triggers |

**C2 required strategies (per quality-enforcement.md):** S-007 (Constitutional AI Critique), S-002 (Devil's Advocate), S-014 (LLM-as-Judge)

**C2 optional strategies:** S-003 (Steelman Technique), S-010 (Self-Refine)

### Quality Gate Parameters Per Barrier

| Barrier | Gate | Criticality | Required Strategies | Threshold | Max Iterations |
|---------|------|-------------|---------------------|-----------|----------------|
| Barrier 1 | QG-1 (x4 outputs) | C2 | S-014, S-007, S-002 | >= 0.92 | 3 per deliverable |
| Barrier 2 | QG-2 | C2 | S-014, S-007, S-002 | >= 0.92 | 3 |
| Barrier 3 | QG-3 | C2 | S-014, S-007, S-002 | >= 0.92 | 3 |
| Barrier 4 | QG-4 (dual) | C2 | S-014, S-007, S-002, NPR 7123.1D | >= 0.92 | 3 (combined) |

### S-014 Scoring Dimensions

| Dimension | Weight | Description |
|-----------|--------|-------------|
| Completeness | 0.20 | All required items present (min counts met, all fields populated) |
| Internal Consistency | 0.20 | Claims do not contradict each other; methodology applied uniformly |
| Methodological Rigor | 0.20 | Appropriate method applied; steps followed correctly |
| Evidence Quality | 0.15 | Claims sourced to external evidence; no training-data-only citations |
| Actionability | 0.15 | Findings can be used to make concrete decisions |
| Traceability | 0.10 | Each claim traces back to a named source or search query |

### Creator-Critic Agent Assignments

| Phase | Creator | Critic | Revision |
|-------|---------|--------|---------|
| Phase 1 streams | ps-researcher | adv-scorer (Phase 2) | ps-researcher revision |
| Phase 3 | ps-synthesizer | adv-scorer (Phase 4) | ps-synthesizer revision |
| Phase 5 | ps-analyst | adv-scorer (Phase 6) | ps-analyst revision |
| Phase 7 | ps-architect | adv-scorer + nse-reviewer (Phase 8) | ps-architect revision |

---

## Constraints

> NPT-013 format — constraints governing all agent execution in this workflow.

| ID | Constraint |
|----|-----------|
| C-001 | NEVER use the general-purpose or Explore subagent_type. All agents must be named skill agents (ps-researcher, ps-synthesizer, ps-analyst, ps-architect, adv-scorer, nse-reviewer). |
| C-002 | NEVER cite LLM training knowledge as a source for research claims. Every factual claim must be attributed to a named external source accessed via WebSearch, WebFetch, or Context7. |
| C-003 | NEVER proceed past a quality gate with a score below 0.92. The workflow halts and returns to the producing agent for revision. |
| C-004 | NEVER present the final ADR to the human without passing both adv-scorer Gate A AND nse-reviewer Gate B in Phase 8. |
| C-005 | NEVER include any framework, SDK, or tool recommendation that lacks a verified OSI-approved open-source license. Exclude and document exclusions with evidence. |
| C-006 | NEVER pre-populate research with specific tool or methodology names from LLM training data. Research outputs must be driven by search results. |
| C-007 | NEVER allow Phase 7 to predetermine the 3 ADR options. Options must be derived from Phase 5 analysis findings. |

---

## Disclaimer

This orchestration plan was generated by the orch-planner agent for PROJ-035-skill-optimization / FEAT-035-001. It represents a planned workflow; execution sequences, agent assignments, and artifact paths are subject to revision during execution. Human review is recommended before execution begins. This plan does not constitute official NASA guidance.

> **P-043 Notice:** This document was generated by an AI orchestration planner. All architecture decisions produced by this workflow require human review and acceptance per P-020 (user authority). Quality gate scores produced by adv-scorer are advisory inputs to human judgment, not binding approvals.
