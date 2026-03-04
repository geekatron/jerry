# Leash Kernel-Level Security Research: Orchestration Plan

> **Workflow ID:** `leash-kernel-security-20260303-001`
> **Date:** 2026-03-03
> **Status:** ACTIVE
> **Project:** PROJ-0036-LEASH-COMP
> **Criticality:** C2 (Standard)

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Workflow Overview](#l0-workflow-overview) | What this workflow does and why |
| [L1: Technical Plan](#l1-technical-plan) | Workflow diagram, phase definitions, sync barriers |
| [L2: Implementation Details](#l2-implementation-details) | Agent mapping, data sources, quality gates |
| [Constraints](#constraints) | Research integrity and source requirements |
| [Quality Gate Definitions](#quality-gate-definitions) | Per-phase quality enforcement |

---

## L0: Workflow Overview

This workflow conducts a 5-phase research investigation into strongDM Leash and the kernel-level security ecosystem. It produces five deliverables:

1. **Leash Product Analysis** -- What Leash is, what it solves, how it works
2. **Kernel Security Landscape** -- The full technology landscape Leash operates within
3. **Competitive Analysis (Top 5)** -- The most innovative competitors, with strategic frameworks
4. **Strategic Synthesis** -- Where Leash fits, what to build/partner/acquire, top risks
5. **TAM Research and Market Sizing** -- Total Addressable Market analysis with TAM/SAM/SOM sizing

Phases 1 and 2 run in parallel (no dependency). Phase 3 requires both. Phase 4 requires Phase 3. Phase 5 requires Phase 4. Human review is required after each quality gate passes.

---

## L1: Technical Plan

### Workflow Diagram

```
PHASE 1: Leash Product Analysis     PHASE 2: Kernel Security Landscape
  Agent: ps-researcher                Agent: ps-researcher
  Sources: GitHub, WebSearch,         Sources: WebSearch, Context7
           Context7 (Cedar)                    (eBPF, seccomp, gVisor, etc.)
  Output: 01-leash-product-           Output: 02-kernel-security-
          analysis.md                          landscape.md
       |                                    |
       |     (parallel execution)           |
       +----------------+------------------+
                         |
               +=========+==========+
               ||   BARRIER 1      ||
               ||   Phase 1 + 2    ||
               ||   Quality Gate   ||
               ||   >= 0.92        ||
               ||   Human Review   ||
               +=========+==========+
                         |
                         v
         PHASE 3: Top 5 Competitive Analysis
           Agent: ps-researcher + ps-analyst
           Sources: WebSearch, WebFetch
           Inputs: Phase 1 + Phase 2 outputs
           Output: 03-competitive-analysis-top5.md
                         |
               +=========+==========+
               ||   BARRIER 2      ||
               ||   Phase 3        ||
               ||   Quality Gate   ||
               ||   >= 0.92        ||
               ||   Human Review   ||
               +=========+==========+
                         |
                         v
         PHASE 4: Synthesis + Strategy
           Agent: ps-synthesizer
           Sources: Phase 1, 2, 3 outputs
           Output: 04-strategic-synthesis.md
                         |
               +=========+==========+
               ||   BARRIER 3      ||
               ||   Phase 4        ||
               ||   Quality Gate   ||
               ||   >= 0.92        ||
               ||   Human Review   ||
               +=========+==========+
                         |
                         v
         PHASE 5: TAM Research + Market Sizing
           Agent: ps-researcher + ps-analyst
           Sources: WebSearch (analyst reports, market data)
           Inputs: Phase 1, 2, 3, 4 outputs
           Output: 05-tam-market-sizing.md
                         |
               +=========+==========+
               ||   BARRIER 4      ||
               ||   Phase 5        ||
               ||   Quality Gate   ||
               ||   >= 0.92        ||
               ||   Human Review   ||
               +=========+==========+
                         |
                         v
                    WORKFLOW COMPLETE
```

### Phase Definitions

| Phase | Title | Agent | Parallel | Depends On | Output |
|-------|-------|-------|----------|------------|--------|
| 1 | Leash Product Analysis | ps-researcher | Yes (with Phase 2) | -- | `01-leash-product-analysis.md` |
| 2 | Kernel Security Landscape | ps-researcher | Yes (with Phase 1) | -- | `02-kernel-security-landscape.md` |
| 3 | Top 5 Competitive Analysis | ps-researcher + ps-analyst | No | Phase 1, Phase 2 | `03-competitive-analysis-top5.md` |
| 4 | Strategic Synthesis | ps-synthesizer | No | Phase 3 | `04-strategic-synthesis.md` |
| 5 | TAM Research + Market Sizing | ps-researcher + ps-analyst | No | Phase 4 | `05-tam-market-sizing.md` |

### Sync Barriers

| Barrier | Trigger | Quality Threshold | Unlocks | Human Review |
|---------|---------|-------------------|---------|--------------|
| Barrier 1 | Phase 1 COMPLETE AND Phase 2 COMPLETE | >= 0.92 | Phase 3 | Required |
| Barrier 2 | Phase 3 COMPLETE | >= 0.92 | Phase 4 | Required |
| Barrier 3 | Phase 4 COMPLETE | >= 0.92 | Phase 5 | Required |
| Barrier 4 | Phase 5 COMPLETE | >= 0.92 | Workflow Complete | Required |

---

## L2: Implementation Details

### Agent Mapping

The user's prompt references PM-specific agent roles. These map to available Jerry agents:

| User Role | Jerry Agent | Rationale |
|-----------|-------------|-----------|
| pm-product-strategist | ps-researcher (divergent) | Product analysis is a research task |
| ps-researcher | ps-researcher (divergent) | Direct mapping |
| pm-competitive-analyst | ps-researcher + ps-analyst | Research + structured analysis |
| ps-synthesizer | ps-synthesizer (integrative) | Direct mapping |
| pm-market-analyst | ps-researcher + ps-analyst | TAM research + quantitative analysis |

### Data Sources Per Phase

| Phase | WebSearch | WebFetch | Context7 | File Refs |
|-------|-----------|----------|----------|-----------|
| 1 | Leash announcements, blogs | GitHub repo, docs | Cedar policy language | -- |
| 2 | eBPF, seccomp, gVisor state-of-art | Vendor docs | eBPF, seccomp, gVisor, Kata, Wasmtime | -- |
| 3 | Product launches, funding rounds | Vendor product pages | -- | Phase 1, Phase 2 outputs |
| 4 | -- | -- | -- | Phase 1, 2, 3 outputs |
| 5 | Market size reports, analyst forecasts | Analyst report pages | -- | Phase 1, 2, 3, 4 outputs |

### Output Paths

All paths relative to repository root: `docs/pm-pmm/leash-analysis/`

| Artifact | Path |
|----------|------|
| Phase 1 output | `docs/pm-pmm/leash-analysis/01-leash-product-analysis.md` |
| Phase 2 output | `docs/pm-pmm/leash-analysis/02-kernel-security-landscape.md` |
| Phase 3 output | `docs/pm-pmm/leash-analysis/03-competitive-analysis-top5.md` |
| Phase 4 output | `docs/pm-pmm/leash-analysis/04-strategic-synthesis.md` |
| Phase 5 output | `docs/pm-pmm/leash-analysis/05-tam-market-sizing.md` |
| Orchestration Plan | `docs/pm-pmm/leash-analysis/ORCHESTRATION_PLAN.md` |
| Orchestration State | `docs/pm-pmm/leash-analysis/ORCHESTRATION.yaml` |

---

## Constraints

| Constraint | Rule |
|------------|------|
| No LLM training data | Do NOT rely on training data for market research, product analysis, or competitive intelligence |
| Source requirement | Use WebSearch and WebFetch for all external claims |
| Context7 | Use for any named library/framework documentation |
| Citation requirement | All claims MUST cite sources with URLs |
| Unsourced claims | MUST be marked as `[HYPOTHESIS -- confidence: low]` |

---

## Quality Gate Definitions

| Gate | Phase | Threshold | Scoring | Strategies (C2) | Max Iterations |
|------|-------|-----------|---------|-----------------|----------------|
| QG-1 | Phase 1 | >= 0.92 | S-014 (LLM-as-Judge) | S-007, S-002, S-014 | 5 |
| QG-2 | Phase 2 | >= 0.92 | S-014 (LLM-as-Judge) | S-007, S-002, S-014 | 5 |
| QG-3 | Phase 3 | >= 0.92 | S-014 (LLM-as-Judge) | S-007, S-002, S-014 | 5 |
| QG-4 | Phase 4 | >= 0.92 | S-014 (LLM-as-Judge) | S-007, S-002, S-014 | 5 |
| QG-5 | Phase 5 | >= 0.92 | S-014 (LLM-as-Judge) | S-007, S-002, S-014 | 5 |

**Gate behavior:** Quality gate failure triggers revision cycle. After 5 iterations without passing, escalate to human review. Human review is required AFTER each quality gate passes (not before).
