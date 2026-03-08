# PROJ-036 Test Harness Validation Pipeline: Orchestration Plan

> **Document ID:** PROJ-036-ORCH-PLAN
> **Workflow ID:** validation-run-20260307-001
> **Date:** 2026-03-07
> **Status:** PLANNED
> **Criticality:** C2 (Standard)
> **Pattern:** Pattern 2 — Sequential Pipeline with Fan-Out / Fan-In sub-patterns

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Workflow Overview](#l0-workflow-overview) | Stakeholder summary |
| [L1: Technical Plan](#l1-technical-plan) | Diagram, phases, agents, barriers |
| [L2: Implementation Details](#l2-implementation-details) | State schema, paths, recovery, quality gates |
| [Disclaimer](#disclaimer) | Mandatory orch-planner disclaimer |

---

## L0: Workflow Overview

This workflow validates that PROJ-036's four-layer prompt regression test harness produces correct, measurable outputs before it is used as a gating mechanism in CI/CD. Five Jerry agents (ps-researcher, ps-analyst, ps-architect, ps-critic, adv-scorer) each generate a representative output sample, which is then scored through three complementary lenses — DeepEval G-Eval semantic scoring (Layer 2), Metamorphic Relation consistency checks (Layer 3), and statistical significance analysis (Layer 4). A final adversarial quality gate aggregates the evidence and decides pass or fail.

If the pipeline completes with an S-014 composite score >= 0.92, the harness is confirmed fit for purpose. If it fails, the quality gate's critique findings identify which layer and which agent require remediation before the harness is promoted to CI. A cross-cutting cost ledger tracks every API call so the team can see exactly what the validation run cost.

---

## L1: Technical Plan

### Workflow Diagram (ASCII)

```
VALIDATION-RUN-20260307-001
Sequential Pipeline (Pattern 2) with Fan-Out / Fan-In sub-patterns

PHASE 1 — Agent Output Generation
  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐
  │ ps-researcher│  │  ps-analyst  │  │  ps-architect    │
  │  (divergent) │  │ (convergent) │  │   (convergent)   │
  └──────┬───────┘  └──────┬───────┘  └────────┬─────────┘
         │  (parallel wave 1 — no dependencies)  │
         │                                       │
         ▼                                       │
  ┌──────────────┐                               ▼
  │   ps-critic  │                    ┌──────────────────┐
  │ depends on   │                    │   adv-scorer     │
  │ ps-researcher│                    │ depends on       │
  │   output     │                    │ ps-architect     │
  └──────┬───────┘                    └────────┬─────────┘
         │         (parallel wave 2)           │
         └─────────────────┬───────────────────┘
                           ▼
                  ╔════════════════╗
                  ║  CP-001        ║
                  ║  Checkpoint    ║
                  ║  5/5 outputs   ║
                  ╚════════════════╝
                           │
                           ▼

PHASE 2 — Layer 2 G-Eval Scoring
  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐
  │ score-   │ │ score-   │ │ score-   │ │ score-   │ │ score-   │
  │ research │ │ analyst  │ │ architect│ │  critic  │ │  adv-    │
  │ >=0.82   │ │ >=0.85   │ │ >=0.88   │ │ >=0.83   │ │ scorer   │
  │          │ │          │ │          │ │          │ │ >=0.90   │
  └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘
       │             │             │             │             │
       └─────────────┴─────────────┴─────────────┴─────────────┘
                                   ▼
                  ╔════════════════════════╗
                  ║  CP-002                ║
                  ║  Checkpoint            ║
                  ║  Quality Gate          ║
                  ║  All 5 floor scores    ║
                  ║  met or documented     ║
                  ╚════════════════════════╝
                           │
             ┌─────────────┴─────────────┐
             ▼                           ▼

PHASE 3 (parallel)           PHASE 4 (parallel)
Layer 3 Metamorphic          Layer 4 Statistical
Relation Validation          Comparison Report
  ps-researcher +              Layer4Pipeline
  ps-architect                 Wilson CIs +
  MR-001, MR-003               Bonferroni k=6
  N=5 smoke                    per-dimension
  ┌──────────────┐             ┌──────────────┐
  │  layer3-mr-  │             │  layer4-     │
  │  results.md  │             │  statistical-│
  │              │             │  report.md   │
  └──────┬───────┘             └──────┬───────┘
         │                            │
         ▼                            ▼
  ╔══════════════╗           ╔════════════════╗
  ║  CP-003      ║           ║  CP-004        ║
  ║  Checkpoint  ║           ║  Checkpoint    ║
  ╚══════════════╝           ╚════════════════╝
         │                            │
         └─────────────┬──────────────┘
                       ▼

PHASE 5 — Adversary Quality Gate
  ┌─────────────────────────────────────┐
  │  Compile validation-summary.md      │
  │  Score against S-014 >= 0.92        │
  │  Include cost ledger evidence       │
  │  Max 3 iterations (H-14)            │
  └─────────────────┬───────────────────┘
                    ▼
         ╔══════════════════════╗
         ║  QUALITY GATE        ║
         ║  S-014 Composite     ║
         ║  >= 0.92 required    ║
         ║  Criticality: C2     ║
         ╚══════════════════════╝
                    │
         ┌──────────┴──────────┐
         │                     │
         ▼                     ▼
      PASS                  FAIL
  Harness fit           Revise per
  for purpose           critic findings
                        max 3 iter
```

```
CROSS-CUTTING: Cost Ledger
  Every API call → cost-ledger.md
  input_tokens × $3/M + output_tokens × $15/M
  Accumulated per-agent and total
  Path: work/test-harness/cost-ledger.md
```

### Pipeline Definitions

| Pipeline | Alias | Pattern | Phases | Agents |
|----------|-------|---------|--------|--------|
| validation-pipeline | vp | Sequential with Fan-Out/Fan-In | 5 | 7 |

### Phase Definitions

| Phase | ID | Name | Execution | Agents | Output Artifacts | Checkpoint |
|-------|----|------|-----------|--------|-----------------|------------|
| 1 | PH-001 | Agent Output Generation | Wave 1: parallel (3), Wave 2: parallel (2) | ps-researcher, ps-analyst, ps-architect, ps-critic, adv-scorer | 5x `{agent-id}-output.md` | CP-001 |
| 2 | PH-002 | Layer 2 G-Eval Scoring | Parallel (5 scoring tasks) | DeepEvalAdapter × 5 | 5x `layer2-scores-{agent-id}.md` | CP-002 |
| 3 | PH-003 | Layer 3 Metamorphic Validation | Sequential | MR-001 + MR-003 runners | `layer3-mr-results.md` | CP-003 |
| 4 | PH-004 | Layer 4 Statistical Report | Sequential | Layer4Pipeline | `layer4-statistical-report.md` | CP-004 |
| 5 | PH-005 | Adversary Quality Gate | Sequential (max 3 iter) | adv-scorer (S-014) | `adversary-quality-gate.md` | — |

### Phase 1 Wave Structure

| Wave | Agents | Dependency |
|------|--------|------------|
| Wave 1 | ps-researcher, ps-analyst, ps-architect | None (start in parallel) |
| Wave 2 | ps-critic (needs ps-researcher output), adv-scorer (needs ps-architect output) | Wave 1 complete |

### Quality Floors (Phase 2)

| Agent | Quality Floor | G-Eval Criteria File |
|-------|--------------|----------------------|
| ps-researcher | 0.82 | `jerry/testing/evaluation/criteria/ps_researcher.py` |
| ps-analyst | 0.85 | `jerry/testing/evaluation/criteria/ps_analyst.py` |
| ps-architect | 0.88 | `jerry/testing/evaluation/criteria/ps_architect.py` |
| ps-critic | 0.83 | `jerry/testing/evaluation/criteria/ps_critic.py` |
| adv-scorer | 0.90 | `jerry/testing/evaluation/criteria/adv_scorer.py` |

### Phase 3 Metamorphic Relations

| Relation | ID | Agents Under Test | N | Status |
|----------|----|-------------------|---|--------|
| Paraphrase Consistency | MR-001 | ps-researcher, ps-architect | 5 | Smoke test (not statistically powered) |
| Irrelevant Context Appendation | MR-003 | ps-researcher, ps-architect | 5 | Smoke test (not statistically powered) |

> **ADR-001 note:** N=5 is a smoke test only. ADR-001 requires N>=20 for statistical power. Phase 3 results are informational; they do not gate pipeline progression.

### Phase 4 Statistical Parameters

| Parameter | Value |
|-----------|-------|
| Module | `jerry/testing/layer4_stats.py` (Layer4Pipeline) |
| Candidate distribution | Per-dimension scores from Phase 2 |
| Baseline reference | Quality floor values |
| Confidence intervals | Wilson score CIs |
| Multiple comparisons | Bonferroni correction (k=6 dimensions) |

### Sync Checkpoints

| ID | Trigger | Gate Condition | On Fail |
|----|---------|---------------|---------|
| CP-001 | All 5 Phase 1 agent outputs exist | 5/5 files present at `work/test-harness/validation-run/{agent-id}-output.md` | Halt; report which agents failed to produce output |
| CP-002 | All 5 Phase 2 G-Eval scores computed | 5/5 score files present; floor violations documented (not blocking unless > 2 violations) | Warn on individual floor violations; halt if 3+ agents below floor |
| CP-003 | Phase 3 MR results file exists | `layer3-mr-results.md` present | Halt; report MR execution error |
| CP-004 | Phase 4 statistical report exists | `layer4-statistical-report.md` present | Halt; report Layer4Pipeline error |

---

## L2: Implementation Details

### State Schema (ORCHESTRATION.yaml)

See `ORCHESTRATION.yaml` in this directory for the machine-readable state file.

### Dynamic Path Configuration

All artifact paths use the workflow ID as the dynamic root. No hardcoded pipeline names appear in paths.

| Path Token | Value | Derivation |
|------------|-------|------------|
| `{workflow_id}` | `validation-run-20260307-001` | User-specified |
| `{base}` | `orchestration/validation-run-20260307-001/` | `orchestration/{workflow_id}/` |
| `{run_artifacts}` | `work/test-harness/validation-run/` | Fixed work output path |
| `{agent_output}` | `{run_artifacts}{agent-id}-output.md` | Per-agent output |
| `{layer2_score}` | `{run_artifacts}layer2-scores-{agent-id}.md` | Per-agent G-Eval score |
| `{cost_ledger}` | `work/test-harness/cost-ledger.md` | Cross-cutting cost tracking |

### Pre-Requisite Gap: Dependency Installation

> **GAP-001 (Blocking):** The pipeline requires `anthropic`, `python-dotenv`, `deepeval`, and `scipy` to be installed before execution. The ORCHESTRATION.yaml documents this as a pre-flight check. Executor must run `uv sync` or `uv add anthropic python-dotenv deepeval scipy` before invoking any phase. If dependencies are absent, Phase 1 wave invocations will fail at import time with no useful error message.

**Pre-flight check command:**
```
uv run python -c "import anthropic, dotenv, deepeval, scipy; print('deps OK')"
```

**Environment variable check:**
- `ANTHROPIC_API_KEY` must be set (loaded from `.env` via `python-dotenv`)
- Template: copy `.env.example` to `.env` and populate before execution

### Quality Gate Specification

| Gate | Location | Mechanism | Threshold | Criticality | Max Iterations |
|------|----------|-----------|-----------|-------------|----------------|
| QG-1 (floor check) | Phase 2 → CP-002 | G-Eval per-agent floor comparison | Agent-specific (0.82–0.90) | C2 | N/A (single-pass scoring) |
| QG-2 (final gate) | Phase 5 | S-014 LLM-as-Judge, 6-dimension composite | >= 0.92 | C2 | 3 (H-14) |

**S-014 Scoring Dimensions (Phase 5):**

| Dimension | Weight |
|-----------|--------|
| Completeness | 0.20 |
| Internal Consistency | 0.20 |
| Methodological Rigor | 0.20 |
| Evidence Quality | 0.15 |
| Actionability | 0.15 |
| Traceability | 0.10 |

### Required Adversarial Strategies (C2)

Per `quality-enforcement.md` Criticality Levels table, C2 requires:

| Strategy | ID | Applied At |
|----------|----|------------|
| Constitutional AI Critique | S-007 | Phase 5 quality gate |
| Devil's Advocate | S-002 | Phase 5 quality gate |
| LLM-as-Judge | S-014 | Phase 5 quality gate (primary scoring mechanism) |

### Cost Ledger Specification

| Field | Type | Description |
|-------|------|-------------|
| `agent_id` | string | Which agent made the call |
| `phase` | string | Phase ID (PH-001 through PH-005) |
| `call_type` | string | `generation`, `scoring`, `mr-validation`, `stats`, `quality-gate` |
| `input_tokens` | int | Tokens in the prompt |
| `output_tokens` | int | Tokens in the completion |
| `input_cost_usd` | float | `input_tokens / 1_000_000 * 3.00` |
| `output_cost_usd` | float | `output_tokens / 1_000_000 * 15.00` |
| `call_cost_usd` | float | `input_cost_usd + output_cost_usd` |
| `cumulative_usd` | float | Running total |

Pricing: $3.00/M input tokens, $15.00/M output tokens (claude-sonnet-4-20250514).

### Recovery Strategies

| Failure Mode | Detection | Recovery |
|--------------|-----------|----------|
| Single agent fails in Phase 1 Wave 1 | CP-001: missing output file | Retry agent invocation once; if second failure, halt and report |
| Wave 2 dependency unavailable | Wave 2 agent checks for Wave 1 output | Halt wave 2 agent; mark as blocked in ORCHESTRATION.yaml |
| G-Eval floor violation (1-2 agents) | CP-002: score below floor | Log violation, document in summary, continue to Phase 3/4 |
| G-Eval floor violation (3+ agents) | CP-002: >= 3 violations | Halt pipeline; surface violations in cost-ledger and ORCHESTRATION.yaml |
| MR execution error | CP-003: missing results file | Log error with stack trace; Phase 5 notes MR gap but continues |
| Layer4Pipeline error | CP-004: missing report file | Log error; Phase 5 notes statistical gap but continues |
| Phase 5 below threshold | S-014 score < 0.92 | Revision cycle up to 3 iterations; escalate to user on 3rd failure |
| `ANTHROPIC_API_KEY` missing | Pre-flight check | Halt before Phase 1; display actionable error message |
| Missing dependencies | Pre-flight check | Halt before Phase 1; display `uv add` remediation command |

---

## Disclaimer

This orchestration plan was generated by orch-planner agent (v2.2.0). Human review is recommended before execution. This plan is scoped to PROJ-036-prompt-regression-harness only and does not constitute official framework governance.

> **P-043 Mandatory Disclaimer:** This document is an AI-generated orchestration artifact. It has not been reviewed by NASA, any standards body, or official governance authority. It is internal project planning documentation only.
