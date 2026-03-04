# Kernel-Level AI Agent Security Competitive Analysis: Orchestration Plan

> **Document ID:** ORCH-PLAN-KERNEL-SECURITY
> **Workflow ID:** `kernel-security-analysis`
> **Date:** 2026-03-02
> **Status:** PLANNED
> **Augments:** `docs/pm-pmm/leash-analysis/` (strongDM Leash research portfolio)

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Workflow Overview](#l0-workflow-overview) | What this workflow does and why it matters |
| [L1: Technical Plan](#l1-technical-plan) | Workflow diagram, pipeline definitions, sync barriers |
| [L2: Implementation Details](#l2-implementation-details) | State schema, path configuration, recovery strategies |
| [Criticality Assessment](#criticality-assessment) | C1-C4 classification and adversarial strategy set |
| [Quality Gate Definitions](#quality-gate-definitions) | Per-barrier quality enforcement |
| [Prior Deliverable Cross-Reference Map](#prior-deliverable-cross-reference-map) | Which phases consume which existing artifacts |
| [Disclaimer](#disclaimer) | Agent-generated plan notice |

---

## L0: Workflow Overview

This workflow augments the strongDM Leash research portfolio with a focused investigation into kernel-level AI agent security -- the technology layer where Leash's syscall-level telemetry creates its most defensible competitive moat. The existing portfolio (PM-CA-001 competitive analysis, plus three planned deliverables) established Leash's market position, PMF, and financial model at a layer-agnostic level. This workflow goes one layer deeper: the operating system kernel.

The workflow answers four questions that the existing portfolio leaves open: (1) What kernel-level technologies exist and how do they compare to Leash's current syscall approach? (2) Who is building kernel-security products for AI agents, and how do they stack against Leash? (3) Where should Leash invest -- which kernel capabilities to build, partner for, or acquire? (4) How does kernel-level differentiation change the TAM and the competitive positioning statement?

The output is four research documents that slot directly into the existing `leash-analysis/` portfolio as a `kernel-security/` sub-portfolio. Phase 1 and Phase 2 run in parallel. Phase 3 synthesizes them. Phase 4 converts Phase 3 into investment and GTM decisions.

---

## L1: Technical Plan

### Workflow Diagram (ASCII)

```
PRIOR PORTFOLIO (read-only inputs)
  02-competitive-analysis.md (PM-CA-001)
  01-product-strategy-use-cases.md [planned]
  03-market-strategy-positioning.md [planned]
  04-business-analysis.md [planned]
          │
          │ (cross-reference at each phase)
          ▼

┌─────────────────────────────────┐   ┌─────────────────────────────────┐
│  PIPELINE A: Technology         │   │  PIPELINE B: Competitor          │
│  Landscape (Phase 1)            │   │  Deep-Dive (Phase 2)             │
│                                 │   │                                  │
│  Agent: pm-competitive-analyst  │   │  Agent: pm-competitive-analyst   │
│  Tool: WebSearch + WebFetch     │   │  Tool: WebSearch + WebFetch      │
│                                 │   │                                  │
│  eBPF, seccomp, LSMs,           │   │  Pure-play AI security,          │
│  gVisor, Kata Containers,       │   │  Container/runtime platforms,    │
│  Firecracker, ptrace            │   │  Cloud-native, OSS frameworks,   │
│                                 │   │  PAM vendors                     │
│  Out: 01-technology-landscape   │   │  Out: 02-competitor-deep-dive    │
└────────────────┬────────────────┘   └───────────────┬──────────────────┘
                 │                                    │
                 │ (parallel execution)               │
                 └──────────────────┬─────────────────┘
                                    │
                          ╔═════════╧════════════╗
                          ║  BARRIER 1           ║
                          ║  Phase 1 + Phase 2   ║
                          ║  BOTH complete       ║
                          ║  Quality Gate        ║
                          ║  adv-scorer >= 0.92  ║
                          ╚═════════╤════════════╝
                                    │
                                    ▼
               ┌────────────────────────────────────────┐
               │  PIPELINE C: Product Strategy (Phase 3) │
               │                                         │
               │  Agent: pm-product-strategist           │
               │  Tool: WebSearch + WebFetch             │
               │  Inputs: Phase 1 + Phase 2 outputs      │
               │                                         │
               │  Opportunity Solution Tree              │
               │  JTBD statements                        │
               │  Playing to Win cascade                 │
               │  RICE backlog                           │
               │                                         │
               │  Out: 03-product-strategy.md            │
               └────────────────────┬────────────────────┘
                                    │
                          ╔═════════╧════════════╗
                          ║  BARRIER 2           ║
                          ║  Phase 3 complete    ║
                          ║  Quality Gate        ║
                          ║  adv-scorer >= 0.92  ║
                          ╚═════════╤════════════╝
                                    │
                                    ▼
               ┌────────────────────────────────────────┐
               │  PIPELINE D: Business Viability &       │
               │  GTM (Phase 4)                         │
               │                                         │
               │  Primary Agent: pm-business-analyst     │
               │  Contributing: pm-market-strategist     │
               │  Tool: WebSearch + WebFetch             │
               │  Inputs: Phase 1 + Phase 2 + Phase 3   │
               │                                         │
               │  TAM/SAM/SOM delta                      │
               │  Build/partner/acquire analysis         │
               │  Investment sizing (T-shirt)            │
               │  Updated positioning statement          │
               │                                         │
               │  Out: 04-business-viability-gtm.md      │
               └────────────────────┬────────────────────┘
                                    │
                          ╔═════════╧════════════╗
                          ║  BARRIER 3           ║
                          ║  Phase 4 complete    ║
                          ║  Quality Gate        ║
                          ║  adv-scorer >= 0.92  ║
                          ║  WORKFLOW COMPLETE   ║
                          ╚══════════════════════╝
```

### Pipeline Definitions

| Pipeline | Phase | Agent | Inputs | Output Artifact | Parallel |
|----------|-------|-------|--------|-----------------|----------|
| A | 1 -- Technology Landscape | pm-competitive-analyst | WebSearch, WebFetch, PM-CA-001 (SWOT/value curve sections) | `kernel-security/01-technology-landscape.md` | Yes (with B) |
| B | 2 -- Competitor Deep-Dive | pm-competitive-analyst | WebSearch, WebFetch, PM-CA-001 (6-product matrix, battle cards) | `kernel-security/02-competitor-deep-dive.md` | Yes (with A) |
| C | 3 -- Product Strategy | pm-product-strategist | Phase 1 output, Phase 2 output, PM-PS-004 (use cases + RICE) | `kernel-security/03-product-strategy.md` | No (after Barrier 1) |
| D | 4 -- Business Viability & GTM | pm-business-analyst + pm-market-strategist | Phase 3 output, PM-BA-001 (TAM/SOM), PM-MS-001 (positioning) | `kernel-security/04-business-viability-gtm.md` | No (after Barrier 2) |

### Sync Barriers

| Barrier | ID | Trigger Condition | Blocks |
|---------|----|-------------------|--------|
| 1 | `barrier-1-technology-competitor` | Phase 1 AND Phase 2 both produce outputs at or above quality threshold | Phase 3 (Pipeline C) |
| 2 | `barrier-2-product-strategy` | Phase 3 produces output at or above quality threshold | Phase 4 (Pipeline D) |
| 3 | `barrier-3-workflow-complete` | Phase 4 produces output at or above quality threshold | N/A -- terminal |

### Agent Assignments

| Phase | Primary Agent | Contributing Agent | Role of Contributing Agent |
|-------|---------------|--------------------|-----------------------------|
| 1 | pm-competitive-analyst | -- | Technology landscape primary |
| 2 | pm-competitive-analyst | -- | Competitor profiling primary |
| 3 | pm-product-strategist | -- | Strategy synthesis primary |
| 4 | pm-business-analyst | pm-market-strategist | pm-market-strategist provides positioning update section; pm-business-analyst produces remainder and integrates |

---

## L2: Implementation Details

### State Schema (ORCHESTRATION.yaml)

```yaml
workflow:
  id: "kernel-security-analysis"
  name: "Kernel-Level AI Agent Security Competitive Analysis"
  status: "PLANNED"
  created: "2026-03-02"
  augments: "docs/pm-pmm/leash-analysis/"

paths:
  base: "orchestration/kernel-security-analysis/"
  pipeline_a: "orchestration/kernel-security-analysis/pipeline-a-technology/phase-1/"
  pipeline_b: "orchestration/kernel-security-analysis/pipeline-b-competitor/phase-2/"
  pipeline_c: "orchestration/kernel-security-analysis/pipeline-c-strategy/phase-3/"
  pipeline_d: "orchestration/kernel-security-analysis/pipeline-d-business/phase-4/"
  barrier_1: "orchestration/kernel-security-analysis/cross-pollination/barrier-1/"
  barrier_2: "orchestration/kernel-security-analysis/cross-pollination/barrier-2/"
  barrier_3: "orchestration/kernel-security-analysis/cross-pollination/barrier-3/"

prior_portfolio:
  competitive_analysis: "docs/pm-pmm/leash-analysis/02-competitive-analysis.md"
  product_strategy:     "docs/pm-pmm/leash-analysis/01-product-strategy-use-cases.md"
  market_positioning:   "docs/pm-pmm/leash-analysis/03-market-strategy-positioning.md"
  business_analysis:    "docs/pm-pmm/leash-analysis/04-business-analysis.md"

pipelines:
  - id: "pipeline-a"
    alias: "tech"
    phase: 1
    name: "Technology Landscape Research"
    agent: "pm-competitive-analyst"
    skill: "/pm-pmm"
    data_sources:
      - "WebSearch"
      - "WebFetch"
    status: "PLANNED"
    output: "docs/pm-pmm/leash-analysis/kernel-security/01-technology-landscape.md"
    success_criteria:
      - "All 7 kernel technologies documented: eBPF, seccomp, LSMs (SELinux/AppArmor/Landlock/Smack), gVisor, Kata Containers, Firecracker, ptrace"
      - "Each technology covers: mechanism, AI/ML adoption, performance benchmarks, security guarantees, container runtime compatibility"
      - "Cross-references to PM-CA-001 SWOT and value curve sections included"
      - "Leash syscall-level telemetry positioned within the technology landscape"

  - id: "pipeline-b"
    alias: "comp"
    phase: 2
    name: "Competitor Deep-Dive"
    agent: "pm-competitive-analyst"
    skill: "/pm-pmm"
    data_sources:
      - "WebSearch"
      - "WebFetch"
    status: "PLANNED"
    output: "docs/pm-pmm/leash-analysis/kernel-security/02-competitor-deep-dive.md"
    success_criteria:
      - "Top 5 competitors identified from: pure-play AI security, container/runtime platforms, cloud-native, OSS frameworks, PAM vendors"
      - "Each competitor profiled with: Porter's Five Forces, Blue Ocean value curve vs. Leash, battle card with talk tracks, competitive threat rating"
      - "Net-new vs. overlapping mapping against PM-CA-001 6-product matrix documented"
      - "Competitive threat ratings (Critical/High/Medium/Low) with rationale"

  - id: "pipeline-c"
    alias: "strat"
    phase: 3
    name: "Product Strategy"
    agent: "pm-product-strategist"
    skill: "/pm-pmm"
    data_sources:
      - "WebSearch"
      - "WebFetch"
      - "docs/pm-pmm/leash-analysis/kernel-security/01-technology-landscape.md"
      - "docs/pm-pmm/leash-analysis/kernel-security/02-competitor-deep-dive.md"
    status: "BLOCKED"
    blocked_by: "barrier-1-technology-competitor"
    output: "docs/pm-pmm/leash-analysis/kernel-security/03-product-strategy.md"
    success_criteria:
      - "Opportunity Solution Tree with kernel-security branch mapping outcomes to technology opportunities and Leash options"
      - "JTBD statements (functional, emotional, social) for platform engineering teams evaluating kernel-level sandboxing"
      - "Playing to Win strategy cascade: Where to Play (kernel mechanisms), How to Win (differentiation vs. Phase 2 competitors)"
      - "RICE-scored kernel feature backlog with minimum 5 scored opportunities"
      - "Mapping to existing 10 use cases from PM-PS-004: which are strengthened, which net-new"

  - id: "pipeline-d"
    alias: "biz"
    phase: 4
    name: "Business Viability and GTM"
    primary_agent: "pm-business-analyst"
    contributing_agent: "pm-market-strategist"
    skill: "/pm-pmm"
    data_sources:
      - "WebSearch"
      - "WebFetch"
      - "docs/pm-pmm/leash-analysis/kernel-security/03-product-strategy.md"
      - "docs/pm-pmm/leash-analysis/04-business-analysis.md"
      - "docs/pm-pmm/leash-analysis/03-market-strategy-positioning.md"
    status: "BLOCKED"
    blocked_by: "barrier-2-product-strategy"
    output: "docs/pm-pmm/leash-analysis/kernel-security/04-business-viability-gtm.md"
    success_criteria:
      - "TAM/SAM/SOM delta quantified vs. PM-BA-001 baseline with incremental addressable market sized"
      - "Build/partner/acquire recommendation per kernel technology from Phase 1 (eBPF, seccomp, gVisor, etc.)"
      - "T-shirt sizing (S/M/L/XL + engineering weeks) for top 3 RICE features from Phase 3"
      - "Updated Dunford positioning statement reflecting kernel-level security differentiation"
      - "Updated competitive alternative framing vs. Phase 2 top 5 competitors"

barriers:
  - id: "barrier-1-technology-competitor"
    name: "Technology + Competitor Complete"
    trigger: "pipeline-a COMPLETE AND pipeline-b COMPLETE"
    quality_threshold: 0.92
    unlocks: "pipeline-c"
    status: "PENDING"

  - id: "barrier-2-product-strategy"
    name: "Product Strategy Complete"
    trigger: "pipeline-c COMPLETE"
    quality_threshold: 0.92
    unlocks: "pipeline-d"
    status: "PENDING"

  - id: "barrier-3-workflow-complete"
    name: "Workflow Terminal"
    trigger: "pipeline-d COMPLETE"
    quality_threshold: 0.92
    unlocks: null
    status: "PENDING"

quality:
  threshold: 0.92
  criticality: "C2"
  scoring_mechanism: "S-014"
  scoring_agent: "adv-scorer"
  required_strategies:
    - "S-007"   # Constitutional AI Critique
    - "S-002"   # Devil's Advocate
    - "S-014"   # LLM-as-Judge
  optional_strategies:
    - "S-003"   # Steelman Technique
    - "S-010"   # Self-Refine
  phase_scores: {}
  barrier_scores: {}
  workflow_quality: {}

metrics:
  phases_total: 4
  agents_total: 4
  barriers_total: 3
  pipelines_parallel: 2
  pipelines_sequential: 2
```

### Dynamic Path Configuration

All artifact paths use the workflow ID as the base identifier. Paths resolve as follows:

| Path Type | Template | Example Resolution |
|-----------|----------|--------------------|
| Base | `orchestration/{workflow.id}/` | `orchestration/kernel-security-analysis/` |
| Pipeline | `orchestration/{workflow.id}/{pipeline.alias}/{phase}/` | `orchestration/kernel-security-analysis/tech/phase-1/` |
| Barrier | `orchestration/{workflow.id}/cross-pollination/{barrier.id}/` | `orchestration/kernel-security-analysis/cross-pollination/barrier-1/` |
| Output artifact | `docs/pm-pmm/leash-analysis/kernel-security/{filename}` | `docs/pm-pmm/leash-analysis/kernel-security/01-technology-landscape.md` |

No hardcoded pipeline names are used. Pipeline alias (`tech`, `comp`, `strat`, `biz`) derives from the abbreviated phase purpose.

### Execution Sequence

```
t=0   START
t=0   Spawn Pipeline A (Phase 1: Technology Landscape) -- pm-competitive-analyst
t=0   Spawn Pipeline B (Phase 2: Competitor Deep-Dive) -- pm-competitive-analyst
      [Pipeline A and Pipeline B run in parallel]
      ...
t=A+B Barrier 1: Verify Phase 1 AND Phase 2 outputs exist and score >= 0.92
t=A+B Spawn Pipeline C (Phase 3: Product Strategy) -- pm-product-strategist
      [Pipeline C runs sequential on Phase 1 + Phase 2 outputs]
      ...
t=C   Barrier 2: Verify Phase 3 output exists and scores >= 0.92
t=C   Spawn Pipeline D (Phase 4: Business Viability + GTM)
         -- pm-business-analyst (primary)
         -- pm-market-strategist (positioning section contribution)
      [Pipeline D runs sequential on Phase 1 + Phase 2 + Phase 3 outputs]
      ...
t=D   Barrier 3: Verify Phase 4 output exists and scores >= 0.92
t=D   WORKFLOW COMPLETE
```

### Recovery Strategies

| Failure Mode | Recovery Action |
|---|---|
| Phase 1 output does not meet quality gate | adv-scorer returns specific revision guidance; pm-competitive-analyst revises and re-submits; max 3 revision cycles per H-14 |
| Phase 2 output does not meet quality gate | Same as Phase 1 recovery; phases are independent so Phase 1 need not wait |
| Barrier 1 partially blocked (one pipeline fails, one passes) | The passing pipeline output is preserved; failing pipeline revises independently; Barrier 1 re-evaluates when both pass |
| Phase 3 cannot find prior deliverable cross-reference | If referenced file does not exist, agent documents the gap explicitly in the output with a `[PLANNED -- NOT YET AVAILABLE]` notation and continues with available data |
| Phase 4 pm-market-strategist contribution unavailable | pm-business-analyst produces the positioning section directly using PM-MS-001 as input; document the fallback in the output |
| WebSearch/WebFetch returns insufficient results for a specific technology | Agent documents "insufficient public data" for that technology, proceeds with best-available information, flags for manual research |
| Quality gate plateau (delta < 0.01 for 3 consecutive iterations) | Per RT-M-010: escalate to user with current best result and critic findings; do not continue revision cycles |

---

## Criticality Assessment

**Classification: C2 (Standard)**

| Factor | Assessment |
|--------|------------|
| Reversibility | Reversible within 1 day -- research documents, no production code changes |
| File scope | 4 new output files + cross-references to 4 existing files = 8 files in scope |
| Impact | Module-level: augments existing leash-analysis portfolio; no API changes; no governance file changes |
| Auto-escalation checks | Does not touch `.context/rules/` (no AE-002). Does not touch constitution (no AE-001). No new ADRs (no AE-003). No baselined ADR modification (no AE-004). No security code (no AE-005). |

**Result:** C2 applies. HARD + MEDIUM enforcement tiers active. Required strategies: S-007, S-002, S-014.

---

## Quality Gate Definitions

### Per-Phase Quality Gate

Each phase uses adv-scorer with the S-014 LLM-as-Judge rubric before the barrier is cleared.

| Dimension | Weight | Application to This Workflow |
|-----------|--------|------------------------------|
| Completeness | 0.20 | All required coverage dimensions documented per success criteria |
| Internal Consistency | 0.20 | Technology claims consistent across sections; competitor assessments aligned with prior portfolio |
| Methodological Rigor | 0.20 | Named frameworks applied correctly (Porter's, JTBD, OST, Playing to Win, RICE, Dunford) |
| Evidence Quality | 0.15 | WebSearch/WebFetch citations present; data gaps explicitly flagged |
| Actionability | 0.15 | Findings support concrete investment, positioning, and GTM decisions |
| Traceability | 0.10 | Cross-references to prior portfolio deliverables present and specific |

**Composite threshold:** >= 0.92 per H-13.

### Barrier-Level Enforcement

```
Phase N Output
      │
      ▼
adv-scorer (S-014)
  ├── Score >= 0.92 → PASS → unlock next phase
  ├── Score 0.85-0.91 (REVISE) → targeted revision → re-score (max 3 cycles)
  └── Score < 0.85 (REJECTED) → significant rework → re-score (max 3 cycles)
      │
      ▼
If 3 cycles reach plateau (delta < 0.01):
  → Escalate to user with best result + critic findings (RT-M-010)
```

### Required Adversarial Strategies (C2)

| Strategy | When Applied | Purpose |
|----------|-------------|---------|
| S-007 Constitutional AI Critique | Before each barrier | Verify research does not violate governance constraints |
| S-002 Devil's Advocate | At each quality scoring round | Challenge core competitive assessments and market sizing assumptions |
| S-014 LLM-as-Judge | At each barrier | Formal quality scoring against 6-dimension rubric |

### Optional Adversarial Strategies (C2)

| Strategy | When Applied | Purpose |
|----------|-------------|---------|
| S-003 Steelman Technique | Before Devil's Advocate (H-16 ordering) | Strengthen competitive claims before attacking them |
| S-010 Self-Refine | Before submitting to adv-scorer | Agent self-review per H-15 |

---

## Prior Deliverable Cross-Reference Map

This map defines which sections of the existing portfolio each phase MUST cross-reference. Phases execute autonomously after human approval of this plan; cross-references are non-optional.

| Phase | Prior Deliverable | Specific Sections to Cross-Reference | Cross-Reference Purpose |
|-------|-------------------|--------------------------------------|-------------------------|
| 1 | `02-competitive-analysis.md` (PM-CA-001) | SWOT Analysis (Leash) -- Strengths: Syscall-level telemetry; Blue Ocean Value Curve -- Leash position on Kernel-Level Enforcement axis | Position the 7 kernel technologies relative to Leash's existing syscall approach; identify which technologies are adjacent vs. differentiated |
| 2 | `02-competitive-analysis.md` (PM-CA-001) | Competitive Comparison Matrix (6 products); Battle Cards (Teleport, Lasso, E2B, Daytona, AWS Bedrock); Competitive Threat Assessment | Identify net-new competitors not in the original 6; update threat ratings for any overlapping competitors; extend battle cards |
| 2 | `01-product-strategy-use-cases.md` (PM-PS-004) [if available] | Competitive Positioning section (L2); RICE scores for existing use cases | Understand which use cases have kernel-security adjacency |
| 3 | `01-product-strategy-use-cases.md` (PM-PS-004) [if available] | 10 use cases; RICE scores | Map which existing use cases are strengthened by kernel-level differentiation; identify net-new use cases |
| 3 | Phase 1 output | Technology landscape section | Populate Opportunity Solution Tree technology opportunities from Phase 1 findings |
| 3 | Phase 2 output | Top 5 competitor profiles | Populate Playing to Win "How to Win" vs. identified competitors |
| 4 | `04-business-analysis.md` (PM-BA-001) [if available] | TAM/SAM/SOM baseline figures; Lean Canvas; SaaS metrics | Compute delta; identify which Lean Canvas assumptions change with kernel-level differentiation |
| 4 | `03-market-strategy-positioning.md` (PM-MS-001) [if available] | Dunford positioning statement; Crossing the Chasm segment; buyer personas | Draft updated positioning statement; assess which buyer persona benefits most from kernel-level security |
| 4 | Phase 3 output | RICE backlog (top 3 features); Playing to Win cascade | Scope investment sizing; align GTM positioning with strategy cascade |

**Note on unavailable files:** Files PM-PS-004, PM-MS-001, and PM-BA-001 reference planned deliverables not yet created at time of this orchestration plan. If they do not exist when their phase executes, agents MUST document the gap with `[PLANNED -- NOT YET AVAILABLE]` notation and proceed using PM-CA-001 (which exists) and WebSearch as fallback sources. This is a known limitation of the parallel portfolio development sequence.

---

## Disclaimer

This orchestration plan was generated by the orch-planner agent (v2.2.0) on 2026-03-02. Human review is required before execution begins. Once approved, all four phases execute autonomously -- individual phase outputs do not require human review. Quality gates are enforced at each barrier by adv-scorer at >= 0.92; the workflow self-corrects within the revision cycle bounds defined in this plan before escalating to the user.

Confidence in this plan: 0.87 (high). Gap: three of the four prior portfolio cross-references (01, 03, 04) reference planned but not-yet-created files. Recovery strategy for this gap is documented in the Recovery Strategies section and the Cross-Reference Map.
