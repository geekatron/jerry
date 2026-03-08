# ORCHESTRATION PLAN: Baseline Collection and Validation Execution

<!--
TEMPLATE: Orchestration Plan
VERSION: 1.0.0
SOURCE: FEAT-036-004 — Baseline Collection and Validation Execution
-->

> **Project:** PROJ-036-prompt-regression-harness
> **Feature:** FEAT-036-004
> **Criticality:** C3
> **Scope:** ps-researcher + ps-architect (2 of 5 agents)
> **Budget Ceiling:** $20 USD
> **Created:** 2026-03-08
> **Status:** in_progress

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Pipeline Overview](#pipeline-overview) | Five-phase pipeline with dependencies |
| [Phase 1 — Agent Output Generation](#phase-1--agent-output-generation-with-llm-io-capture) | Execute prompts, capture I/O traces |
| [Phase 2 — G-Eval Scoring](#phase-2--g-eval-scoring-with-score-transparency) | Score outputs, produce composites |
| [Phase 3 — MR Testing](#phase-3--mr-testing-at-n20-with-variant-io-capture) | Metamorphic relation tests at N>=20 |
| [Phase 4 — Statistical Comparison](#phase-4--statistical-comparison-with-real-baselines) | Layer 4 pipeline with real baselines |
| [Phase 5 — CI/CD Integration](#phase-5--cicd-integration-verification) | Workflow verification and security review |
| [Cross-Cutting Requirements](#cross-cutting-requirements) | Cost tracking, I/O visibility, quality gates |
| [State Tracker](#state-tracker) | Phase completion tracking |

---

## Pipeline Overview

```
Phase 1: Agent Output Generation + I/O Capture
    |
    | 9 outputs + 9 I/O traces
    v
Phase 2: G-Eval Scoring + Score Transparency
    |
    | 9 scoring traces + composites
    v
Phase 3: MR Testing at N>=20 + Variant I/O Capture
    |
    | MR results + N>=30 baseline records
    v
Phase 4: Statistical Comparison (Real Baselines)
    |
    | Wilcoxon + Wilson + verdicts
    v
Phase 5: CI/CD Integration + Security Review
    |
    | Final integration report
    v
    DONE
```

### Agent Scope

| Agent | Prompts | System Prompt | Quality Floor |
|-------|---------|---------------|---------------|
| ps-researcher | 5 (P-PSR-001 to P-PSR-005) | skills/problem-solving/agents/ps-researcher.md | 0.82 |
| ps-architect | 4 (P-PAC-001 to P-PAC-004) | skills/problem-solving/agents/ps-architect.md | 0.88 |

### Skills and Agents Involved

| Phase | Skills | Agents |
|-------|--------|--------|
| 1 | /eng-team | eng-backend, eng-qa |
| 2 | /eng-team | eng-backend, eng-qa |
| 3 | /eng-team | eng-backend, eng-qa |
| 4 | /eng-team | eng-backend, eng-qa |
| 5 | /eng-team, /red-team | eng-qa, red-vuln |
| All | /adversary | adv-scorer |

---

## Phase 1 — Agent Output Generation with LLM I/O Capture

**Owner:** eng-backend + eng-qa
**Dependencies:** None (entry phase)
**Estimated API cost:** ~$8 (9 prompts × Opus model)

### 1A — Implement I/O Capture Layer

Build a Python script (`scripts/baseline_runner.py`) that:

1. Loads prompt YAML files from `tests/prompt-regression/baselines/prompts/`
2. Reads the agent system prompt from the path in `system_prompt_path`
3. Calls the Anthropic API directly (not via Task tool — deterministic I/O capture)
4. Captures full request/response payload
5. Sanitizes captured payloads using `_sanitize_input()` pattern from `deepeval_adapter.py`
6. Persists I/O trace JSON files per schema:

```json
{
  "agent": "ps-researcher",
  "prompt_id": "P-PSR-001",
  "run_number": 1,
  "timestamp": "2026-03-08T...",
  "model": "claude-opus-4-20250514",
  "system_prompt": "<full system prompt text>",
  "user_prompt": "<full user prompt text>",
  "raw_response": "<full LLM response text>",
  "token_usage": { "input_tokens": 0, "output_tokens": 0 },
  "latency_ms": 0
}
```

**Output paths:**
- I/O traces: `orchestration/baseline-execution-20260308-001/io-traces/{agent}/{prompt_id}/run-{NNN}-io.json`
- Agent outputs: `orchestration/baseline-execution-20260308-001/outputs/{agent}/{prompt_id}/output.md`

**Security:** API key from `ANTHROPIC_API_KEY` env var only. Redact any env var values from captured payloads.

### 1B — Execute Test Prompts

| Agent | Prompt IDs | Model |
|-------|-----------|-------|
| ps-researcher | P-PSR-001 through P-PSR-005 | claude-opus-4-20250514 (or JERRY_AGENT_MODEL) |
| ps-architect | P-PAC-001 through P-PAC-004 | claude-opus-4-20250514 (or JERRY_AGENT_MODEL) |

### 1C — Verification

- [ ] All 9 prompts produced non-empty output files (>500 chars each)
- [ ] All 9 prompts have corresponding I/O trace JSON files
- [ ] I/O trace files contain all required schema fields
- [ ] No API keys or credentials in any persisted artifact
- [ ] Cost ledger updated

**Verification output:** `orchestration/baseline-execution-20260308-001/phase1-verification.md`

### Phase 1 Acceptance Criteria

| AC | Criterion | Status |
|----|-----------|--------|
| AC-1.1 | 9 output files exist with >500 characters each | pending |
| AC-1.2 | 9 I/O trace JSON files with all schema fields | pending |
| AC-1.3 | Zero credentials in persisted artifacts | pending |
| AC-1.4 | Cost ledger entry for Phase 1 | pending |

### Quality Gate

S-014 weighted composite >= 0.94 (C3 criticality).
Output: `orchestration/baseline-execution-20260308-001/reviews/adv-phase1-score.md`

---

## Phase 2 — G-Eval Scoring with Score Transparency

**Owner:** eng-backend + eng-qa
**Dependencies:** Phase 1 complete
**Estimated API cost:** ~$3 (9 judge calls × Sonnet model)

### 2A — Execute G-Eval Scoring

For each of the 9 agent outputs from Phase 1:
1. Load G-Eval criteria from the YAML prompt file (`g_eval_criteria` section)
2. Construct `QualityCriterion` objects with S-014 weights
3. Construct `DeepEvalAdapter` with `JERRY_JUDGE_MODEL` (default: claude-sonnet-4-20250514)
4. Run scoring through `JerryGEvalDeepEvalMetric`
5. Capture and persist scoring traces

**Scoring trace schema:**
```json
{
  "agent": "ps-researcher",
  "prompt_id": "P-PSR-001",
  "judge_model": "claude-sonnet-4-20250514",
  "timestamp": "2026-03-08T...",
  "judge_prompt": "<exact prompt sent to judge LLM>",
  "judge_raw_response": "<exact response from judge LLM>",
  "dimension_scores": {
    "completeness": 0.85,
    "internal_consistency": 0.90,
    "methodological_rigor": 0.88,
    "evidence_quality": 0.82,
    "actionability": 0.87,
    "traceability": 0.80
  },
  "composite_score": 0.87,
  "debiasing_applied": true,
  "criteria_order": ["list", "of", "shuffled", "criteria"]
}
```

**Output:** `orchestration/baseline-execution-20260308-001/scoring-traces/{agent}/{prompt_id}/scoring-trace.json`

### 2B — Aggregate Composites

**Output:** `orchestration/baseline-execution-20260308-001/phase2-composites.json`

```json
{
  "agents": {
    "ps-researcher": {
      "prompts": {
        "P-PSR-001": { "composite": 0.87, "dimensions": {} }
      },
      "mean_composite": 0.86,
      "quality_floor": 0.82
    },
    "ps-architect": {
      "prompts": {},
      "mean_composite": 0.00,
      "quality_floor": 0.88
    }
  },
  "total_api_cost_usd": 0.00,
  "timestamp": "2026-03-08T..."
}
```

### 2C — Verification

- [ ] All 9 scoring trace JSON files exist
- [ ] Scoring traces contain `judge_prompt` and `judge_raw_response` fields
- [ ] Composite scores arithmetically consistent with dimension scores and weights
- [ ] Debiasing applied to all runs (`debiasing_applied: true`)
- [ ] ps-researcher mean composite >= 0.82
- [ ] ps-architect mean composite >= 0.88

**Verification output:** `orchestration/baseline-execution-20260308-001/phase2-verification.md`

### Phase 2 Acceptance Criteria

| AC | Criterion | Status |
|----|-----------|--------|
| AC-2.1 | 9 scoring trace files with complete judge I/O | pending |
| AC-2.2 | phase2-composites.json with all agent summaries | pending |
| AC-2.3 | All quality floors met or documented | pending |
| AC-2.4 | Cost ledger entry for Phase 2 | pending |

### Quality Gate

S-014 weighted composite >= 0.94.
Output: `orchestration/baseline-execution-20260308-001/reviews/adv-phase2-score.md`

---

## Phase 3 — MR Testing at N>=20 with Variant I/O Capture

**Owner:** eng-backend + eng-qa
**Dependencies:** Phase 2 complete
**Estimated API cost:** ~$6 (40+ variant executions)

### 3A — MR-001 Paraphrase Consistency (N>=20)

For ps-researcher and ps-architect:
1. Use `ParaphraseConsistency` from `jerry/testing/metamorphic/mr_001_paraphrase.py`
2. Execute `transform()` to generate paraphrased variants of each test prompt
3. Run each variant through the agent (API call), capturing I/O traces
4. Score each variant output using G-Eval (same criteria as Phase 2)
5. Run `evaluate()` with paired score arrays (original scores from Phase 2 + variant scores)
6. Target: N >= 20 paired observations per agent
7. Tolerance threshold: delta <= 0.05

**Output:** `orchestration/baseline-execution-20260308-001/mr-traces/{agent}/mr-001/{variant_id}-io.json`

### 3B — MR-003 Irrelevant Context Appendation (N>=20)

Same protocol as 3A using `IrrelevantContextAppendation`.
- Tolerance threshold: delta <= 0.03

**Output:** `orchestration/baseline-execution-20260308-001/mr-traces/{agent}/mr-003/{variant_id}-io.json`

### 3C — Calibration

**NOTE:** `CalibrationRunner.calibrate_tolerances()` is a stub (raises `NotImplementedError`).
Phase 3C will collect the data needed for future calibration but cannot run the calibration itself.

Instead:
1. Collect all original and transformed score pairs from 3A and 3B
2. Persist the raw calibration data to:
   `orchestration/baseline-execution-20260308-001/mr-calibration-data.json`
3. Document the stub status and the path forward

When CalibrationRunner is implemented, this data can be fed to `calibrate_tolerances()`.

### 3D — Baseline Population

Store N=30 baseline records per agent (Phase 2 scores + MR variant scores accumulated):
1. Use `BaselineStore.store()` from `jerry/testing/baselines/store.py`
2. Construct version key: `{git_hash}:skills/problem-solving/agents/{agent}.md`
3. Quality gate: mean(scores) >= 0.92

**Output:** `tests/prompt-regression/baselines/data/{agent}/{metric_id}/*.json`

### 3E — Verification

- [ ] N >= 20 paired observations per agent per MR
- [ ] MR-001 delta <= 0.05 for both agents (or documented explanation)
- [ ] MR-003 delta <= 0.03 for both agents (or documented explanation)
- [ ] MR variant I/O traces exist with full prompt + response
- [ ] BaselineStore contains N >= 30 records per agent
- [ ] Calibration data persisted for future CalibrationRunner use

**Verification output:** `orchestration/baseline-execution-20260308-001/phase3-verification.md`

### Phase 3 Acceptance Criteria

| AC | Criterion | Status |
|----|-----------|--------|
| AC-3.1 | MR-001 and MR-003 results at N>=20 per agent | pending |
| AC-3.2 | Variant I/O traces persisted | pending |
| AC-3.3 | Calibration data persisted (stub noted) | pending |
| AC-3.4 | BaselineStore populated N>=30 per agent | pending |
| AC-3.5 | Cost ledger entry for Phase 3 | pending |

### Quality Gate

S-014 weighted composite >= 0.94.
Output: `orchestration/baseline-execution-20260308-001/reviews/adv-phase3-score.md`

---

## Phase 4 — Statistical Comparison with Real Baselines

**Owner:** eng-backend + eng-qa
**Dependencies:** Phase 3 complete (BaselineStore populated)
**Estimated API cost:** ~$0 (no LLM calls — pure statistics)

### 4A — Layer4Pipeline Execution

Use `Layer4Pipeline` from `jerry/testing/layer4_stats.py`:
1. Load real baseline scores from BaselineStore (Phase 3D)
2. Load candidate scores (Phase 2 composites)
3. Run Wilcoxon signed-rank test per quality dimension
4. Apply Bonferroni correction (k=6 dimensions)
5. Compute Wilson score confidence intervals for pass rates
6. Classify: NO_REGRESSION / MARGINAL / REGRESSION per dimension
7. Produce overall merge decision: PASS / BLOCK / WARNING

**Output:**
- `orchestration/baseline-execution-20260308-001/phase4-statistical-report.md`
- `orchestration/baseline-execution-20260308-001/phase4-stats.json`

### 4B — Verification

- [ ] Wilcoxon test used real baselines (not synthetic random.Random(42))
- [ ] Bonferroni correction applied with k=6
- [ ] Wilson CIs computed for all dimensions
- [ ] PASS/BLOCK/WARNING verdict consistent with p-values
- [ ] Statistical report includes interpretation guidance

**Verification output:** `orchestration/baseline-execution-20260308-001/phase4-verification.md`

### Phase 4 Acceptance Criteria

| AC | Criterion | Status |
|----|-----------|--------|
| AC-4.1 | Layer 4 report with Wilcoxon p-values, Wilson CIs, verdicts | pending |
| AC-4.2 | phase4-stats.json with all statistical data | pending |
| AC-4.3 | Verdicts derived from real baselines | pending |
| AC-4.4 | Report includes interpretation guidance | pending |

### Quality Gate

S-014 weighted composite >= 0.94.
Output: `orchestration/baseline-execution-20260308-001/reviews/adv-phase4-score.md`

---

## Phase 5 — CI/CD Integration Verification

**Owner:** eng-qa + red-vuln
**Dependencies:** Phase 4 complete
**Estimated API cost:** ~$0

### 5A — Workflow Consumption Test

Verify GitHub Actions workflows can consume real baseline data:
- `.github/workflows/prompt-regression-smoke.yml`
- `.github/workflows/prompt-regression-standard.yml`
- `.github/workflows/prompt-regression-full.yml`

### 5B — Security Review

Review:
- API key handling (ANTHROPIC_API_KEY env var only)
- Prompt injection surface in captured I/O artifacts
- File path traversal risk in I/O trace storage paths
- Credential leakage in GitHub Actions logs

**Output:** `orchestration/baseline-execution-20260308-001/red-vuln-security-review.md`

### 5C — Final Integration Report

**Output:** `orchestration/baseline-execution-20260308-001/final-integration-report.md`

### Phase 5 Acceptance Criteria

| AC | Criterion | Status |
|----|-----------|--------|
| AC-5.1 | CI/CD workflows verified against real baseline data | pending |
| AC-5.2 | Security review with no unmitigated critical findings | pending |
| AC-5.3 | Cost ledger populated with actual API costs | pending |
| AC-5.4 | Expansion guidance documented | pending |

### Quality Gate

S-014 weighted composite >= 0.94.
Output: `orchestration/baseline-execution-20260308-001/reviews/adv-phase5-score.md`

---

## Cross-Cutting Requirements

### Cost Tracking

**Ledger:** `orchestration/baseline-execution-20260308-001/cost-ledger.md`
**Budget ceiling:** $20 for 2 agents
**Halt condition:** Projected cost exceeds budget → escalate to user

### I/O Visibility

Every LLM call produces a persisted I/O trace JSON file. User can inspect exact prompt/response for any run.

### Quality Gates

- C3 criticality level
- >= 0.94 weighted composite (S-014) per phase
- Minimum 3 creator-critic iterations (H-14) before phase advancement
- Circuit breaker: 5 failed iterations → halt and escalate

---

## State Tracker

| Phase | Status | Started | Completed | Quality Score | Cost USD |
|-------|--------|---------|-----------|---------------|----------|
| 1 — Agent Output Generation | complete | 2026-03-08 | 2026-03-08 | verified | $3.69 |
| 2 — G-Eval Scoring | complete | 2026-03-08 | 2026-03-08 | verified | $0.73 |
| 3 — MR Testing | deferred | — | — | — | — |
| 4 — Statistical Comparison | complete (validation) | 2026-03-08 | 2026-03-08 | verified | $0.00 |
| 5 — CI/CD Integration | complete | 2026-03-08 | 2026-03-08 | verified | $0.00 |
| **Total** | — | — | — | — | **$4.42** |
