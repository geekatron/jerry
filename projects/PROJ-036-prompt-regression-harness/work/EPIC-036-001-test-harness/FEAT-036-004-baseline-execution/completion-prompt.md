# FEAT-036-004 Completion Prompt: Baseline Collection with LLM I/O Visibility

> Multi-skill orchestration prompt for executing FEAT-036-004 baseline collection
> and validation across ps-researcher and ps-architect (narrowed from 5 agents).
> Built via `/prompt-engineering` pe-builder 5-element anatomy.
> Criticality: C3 (>10 files, API costs, multi-phase pipeline)

## Document Sections

| Section | Purpose |
|---------|---------|
| [Scope Narrowing Rationale](#scope-narrowing-rationale) | Why 2 agents instead of 5 |
| [Five-Element Anatomy](#five-element-anatomy) | Structural summary of the prompt |
| [NPT-013 Constraints](#npt-013-constraints) | Security and quality constraints |
| [L0: Quick-Start Prompt](#l0-quick-start-prompt) | Compact version for experienced users |
| [L1: Full Orchestration Prompt](#l1-full-orchestration-prompt) | Complete prompt with all phases |
| [Self-Review Score](#self-review-score) | 7-criterion rubric self-assessment |

---

## Scope Narrowing Rationale

The original FEAT-036-004 design targets 5 agents (ps-researcher, ps-analyst, ps-architect,
ps-critic, adv-scorer). This prompt narrows to **2 agents** for the following reasons:

| Factor | Rationale |
|--------|-----------|
| **Cognitive mode coverage** | ps-researcher (divergent) and ps-architect (convergent) cover the two primary cognitive modes under test |
| **MR testing targets** | MR-001 and MR-003 are already designed for ps-researcher and ps-architect specifically |
| **Cost reduction** | ~$15-20 estimated (down from $30 for 5 agents) |
| **Representative coverage** | These 2 agents use different model tiers (both Opus), different prompt structures, and different G-Eval criteria sets |
| **Expansion path** | Once the pipeline is validated with 2 agents, expanding to the remaining 3 is a mechanical repetition |

---

## Five-Element Anatomy

| # | Element | Value |
|---|---------|-------|
| 1 | **SKILL ROUTING** | `/orchestration` (orch-planner), `/eng-team` (eng-backend, eng-qa), `/red-team` (red-vuln), `/adversary` (adv-scorer with S-014) |
| 2 | **SCOPE** | Domain: PROJ-036 prompt regression harness baseline execution. Agents: ps-researcher, ps-architect. Infrastructure: `jerry/testing/` (evaluation, metamorphic, stats, baselines). Date: 2026-03-08. |
| 3 | **DATA SOURCE** | Codebase: `jerry/testing/evaluation/deepeval_adapter.py`, `jerry/testing/metamorphic/mr_001_paraphrase.py`, `jerry/testing/metamorphic/mr_003_context.py`, `jerry/testing/metamorphic/calibration.py`, `jerry/testing/stats.py`, `jerry/testing/layer4_stats.py`, `jerry/testing/baselines/store.py`. Prompts: `tests/prompt-regression/baselines/prompts/ps-researcher-prompts.yaml`, `tests/prompt-regression/baselines/prompts/ps-architect-prompts.yaml`. Agent defs: `skills/problem-solving/agents/ps-researcher.md`, `skills/problem-solving/agents/ps-architect.md`. |
| 4 | **QUALITY GATE** | `/adversary` adv-scorer (S-014 LLM-as-Judge) after each phase. Threshold: >= 0.94 per phase. C3 criticality. |
| 5 | **OUTPUT PATH** | Orchestration plan: `projects/PROJ-036-prompt-regression-harness/orchestration/baseline-execution-20260308-001/ORCHESTRATION_PLAN.md`. Phase outputs under same orchestration directory. |

---

## NPT-013 Constraints

<forbidden_actions>
<constraint format="NPT-013">
NEVER store API keys, tokens, or credentials in output artifacts or log files -- Consequence: credential exposure in git history is irreversible and compromises all API access. Instead: read keys exclusively from environment variables (ANTHROPIC_API_KEY) and redact any key-like strings from captured I/O logs before persistence.
</constraint>

<constraint format="NPT-013">
NEVER execute agent prompts without capturing the full LLM request payload and response text to disk -- Consequence: scores without I/O artifacts are unauditable and cannot be manually inspected for scoring accuracy. Instead: wrap every LLM call with an I/O capture layer that persists the exact prompt sent and exact response received as JSON files alongside the computed scores.
</constraint>

<constraint format="NPT-013">
NEVER run MR tests at N < 20 and report the results as statistically valid -- Consequence: underpowered tests produce unreliable p-values that mask real regressions or flag false positives. Instead: enforce N >= 20 minimum sample size per ADR-001 FM-002 and use CalibrationRunner for empirical threshold calibration.
</constraint>

<constraint format="NPT-013">
NEVER use synthetic or random baselines in Layer 4 statistical comparison and present them as real -- Consequence: synthetic baselines produce meaningless PASS/BLOCK verdicts that provide false confidence in regression detection capability. Instead: use only real API-generated baseline scores stored via BaselineStore.store() with actual agent outputs.
</constraint>

<constraint format="NPT-013">
NEVER skip the security review of I/O capture artifacts for prompt injection content -- Consequence: captured LLM responses may contain adversarial payloads that, if ingested by downstream tooling, could execute unintended actions. Instead: sanitize all captured I/O through the existing _sanitize_input() function from deepeval_adapter.py before persistence.
</constraint>
</forbidden_actions>

---

## L0: Quick-Start Prompt

> Compact version. Use this if you are familiar with the PROJ-036 infrastructure and
> want the essential instructions without full context.

```
Use /worktracker to update FEAT-036-004 status to in_progress.

Use /orchestration with orch-planner to sequence a 5-phase pipeline for PROJ-036
baseline collection and validation, narrowed to ps-researcher and ps-architect only.

Use /eng-team with eng-backend to implement LLM I/O capture (exact prompt sent +
exact response received, persisted as JSON) in the execution scripts. Use eng-qa
for test validation and coverage verification.

Use /red-team with red-vuln to review API key handling and prompt injection surface
in the I/O capture mechanism.

Phase 1: Execute test prompts from ps-researcher-prompts.yaml and ps-architect-prompts.yaml
against real agents, capturing full I/O traces.
Phase 2: Run DeepEvalAdapter.evaluate_batch() with G-Eval scoring trace capture.
Phase 3: MR-001 + MR-003 at N>=20 with CalibrationRunner, capturing variant I/O.
Phase 4: Layer4Pipeline with real baselines, produce statistical verdicts.
Phase 5: Verify CI/CD workflows consume real baseline data.

Include /adversary adv-scorer (S-014) review after each phase. Threshold: >= 0.94.
Quality gate: C3 criticality with >= 0.94 weighted composite per section.

Output orchestration plan:
projects/PROJ-036-prompt-regression-harness/orchestration/baseline-execution-20260308-001/ORCHESTRATION_PLAN.md
```

---

## L1: Full Orchestration Prompt

> Complete prompt with all phase details, file paths, acceptance criteria, and
> quality specifications. Copy this into a fresh Jerry session.

```
Use /worktracker to update FEAT-036-004 status to in_progress under PROJ-036.

Use /orchestration with orch-planner to sequence the following 5-phase pipeline
for PROJ-036 FEAT-036-004: Baseline Collection and Validation Execution.
Narrowed scope: ps-researcher and ps-architect only (2 of 5 agents).

Output orchestration plan:
projects/PROJ-036-prompt-regression-harness/orchestration/baseline-execution-20260308-001/ORCHESTRATION_PLAN.md

---

Phase 1 — Agent Output Generation with LLM I/O Capture (eng-backend + eng-qa)

Use /eng-team with eng-backend to implement I/O capture modifications and execute
agent output generation for ps-researcher and ps-architect.

1A — Implement I/O Capture Layer:
  Modify or extend the execution infrastructure so that every LLM call captures:
  (a) The exact prompt/system-prompt sent to the LLM (full request payload)
  (b) The exact raw response text received from the LLM
  (c) Timestamp, model identifier, and token usage metadata
  (d) Agent name, prompt ID, and run number

  Persist each capture as a JSON file:
    orchestration/baseline-execution-20260308-001/io-traces/{agent}/{prompt_id}/run-{NNN}-io.json

  The JSON schema for each I/O trace file:
  {
    "agent": "ps-researcher",
    "prompt_id": "P-PSR-001",
    "run_number": 1,
    "timestamp": "2026-03-08T...",
    "model": "claude-opus-4-20250514",
    "system_prompt": "<full system prompt text>",
    "user_prompt": "<full user prompt text>",
    "raw_response": "<full LLM response text>",
    "token_usage": { "input_tokens": N, "output_tokens": N },
    "latency_ms": N
  }

  Security requirement: Redact any environment variable values (API keys) that
  appear in captured payloads before writing to disk. Use the existing
  _sanitize_input() pattern from jerry/testing/evaluation/deepeval_adapter.py.

  Existing infrastructure to leverage:
  - jerry/testing/evaluation/deepeval_adapter.py (DeepEvalAdapter class)
  - jerry/testing/evaluation/criterion.py (QualityCriterion)
  - jerry/testing/evaluation/debiasing.py (DebiasingStrategy)

1B — Execute Test Prompts:
  For ps-researcher: execute all 5 prompts from
    tests/prompt-regression/baselines/prompts/ps-researcher-prompts.yaml
  For ps-architect: execute all 4 prompts from
    tests/prompt-regression/baselines/prompts/ps-architect-prompts.yaml

  Each prompt is executed against the real agent definition:
  - ps-researcher: skills/problem-solving/agents/ps-researcher.md
  - ps-architect: skills/problem-solving/agents/ps-architect.md

  Persist agent outputs as markdown files:
    orchestration/baseline-execution-20260308-001/outputs/{agent}/{prompt_id}/output.md

  I/O traces are persisted alongside (per 1A schema).

1C — Verification:
  Use /eng-team with eng-qa to verify:
  - All 9 prompts (5 + 4) produced non-empty output files
  - All 9 prompts have corresponding I/O trace JSON files
  - I/O trace files contain all required fields
  - No API keys or credentials appear in any persisted file

  Output: orchestration/baseline-execution-20260308-001/phase1-verification.md

Phase 1 acceptance criteria:
  - 9 output files exist with substantive content (>500 characters each)
  - 9 I/O trace JSON files exist with all schema fields populated
  - Zero credentials in any persisted artifact
  - Cost ledger entry for Phase 1 API spend

Use /adversary with adv-scorer to score Phase 1 deliverables against S-014 rubric.
Quality threshold: >= 0.94. C3 criticality.
Output: orchestration/baseline-execution-20260308-001/reviews/adv-phase1-score.md

---

Phase 2 — G-Eval Scoring with Score Transparency (eng-backend + eng-qa)

Use /eng-team with eng-backend to run G-Eval scoring with full judge I/O capture.

2A — Execute G-Eval Scoring:
  For each of the 9 agent outputs from Phase 1:
  - Load the agent's G-Eval criteria from the YAML prompt file (g_eval_criteria section)
  - Construct DeepEvalAdapter with model_name from JERRY_JUDGE_MODEL env var
    (default: claude-sonnet-4-20250514)
  - Run evaluate_batch() or equivalent scoring through JerryGEvalDeepEvalMetric

  Capture and persist for each scoring run:
  (a) The G-Eval prompt sent to the judge model (the criteria + agent output payload)
  (b) The judge model's raw scoring response
  (c) Per-dimension scores (completeness, internal_consistency, methodological_rigor,
      evidence_quality, actionability, traceability)
  (d) Composite score with weights applied

  Persist scoring traces:
    orchestration/baseline-execution-20260308-001/scoring-traces/{agent}/{prompt_id}/scoring-trace.json

  The scoring trace JSON schema:
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
      ...
    },
    "composite_score": 0.87,
    "debiasing_applied": true,
    "criteria_order": ["list", "of", "shuffled", "criteria"]
  }

2B — Aggregate Composites:
  Produce a summary JSON file:
    orchestration/baseline-execution-20260308-001/phase2-composites.json

  Schema:
  {
    "agents": {
      "ps-researcher": {
        "prompts": {
          "P-PSR-001": { "composite": 0.87, "dimensions": {...} },
          ...
        },
        "mean_composite": 0.86,
        "quality_floor": 0.82
      },
      "ps-architect": { ... }
    },
    "total_api_cost_usd": 0.00,
    "timestamp": "2026-03-08T..."
  }

2C — Verification:
  Use /eng-team with eng-qa to verify:
  - All 9 prompts have scoring trace JSON files
  - Scoring traces contain judge_prompt and judge_raw_response fields (I/O visibility)
  - Composite scores are arithmetically consistent with dimension scores and weights
  - Debiasing was applied to all runs (debiasing_applied: true)
  - ps-researcher mean composite >= 0.82 (quality_floor)
  - ps-architect mean composite >= 0.88 (quality_floor)

  Output: orchestration/baseline-execution-20260308-001/phase2-verification.md

Phase 2 acceptance criteria:
  - 9 scoring trace files with complete judge I/O
  - phase2-composites.json with all agent summaries
  - All quality floors met or documented with explanation
  - Cost ledger entry for Phase 2 API spend (judge model calls)

Use /adversary with adv-scorer to score Phase 2 deliverables. Threshold: >= 0.94.
Output: orchestration/baseline-execution-20260308-001/reviews/adv-phase2-score.md

---

Phase 3 — MR Testing at N>=20 with Variant I/O Capture (eng-backend + eng-qa)

Use /eng-team with eng-backend to execute metamorphic relation testing.

3A — MR-001 Paraphrase Consistency (N>=20):
  For ps-researcher and ps-architect:
  - Use ParaphraseConsistency from jerry/testing/metamorphic/mr_001_paraphrase.py
  - Execute transform() to generate paraphrased variants of each test prompt
  - Run each variant through the agent, capturing I/O traces for both original and variant
  - Run evaluate() with paired score arrays (original scores from Phase 2 + variant scores)
  - Target: N >= 20 paired observations per agent
  - Tolerance threshold: delta <= 0.05 (max |score_original - score_paraphrased|)

  Persist variant I/O traces:
    orchestration/baseline-execution-20260308-001/mr-traces/{agent}/mr-001/{variant_id}-io.json

3B — MR-003 Irrelevant Context Appendation (N>=20):
  For ps-researcher and ps-architect:
  - Use IrrelevantContextAppendation from jerry/testing/metamorphic/mr_003_context.py
  - Execute transform() to append irrelevant context to each test prompt
  - Run each variant through the agent, capturing I/O traces
  - Run evaluate() with paired score arrays
  - Target: N >= 20 paired observations per agent
  - Tolerance threshold: delta <= 0.03

  Persist variant I/O traces:
    orchestration/baseline-execution-20260308-001/mr-traces/{agent}/mr-003/{variant_id}-io.json

3C — Calibration:
  Use CalibrationRunner from jerry/testing/metamorphic/calibration.py to run
  empirical threshold calibration with the real score distributions from 3A and 3B.
  Persist calibration results:
    orchestration/baseline-execution-20260308-001/mr-calibration-results.json

3D — Baseline Population:
  Store N=30 baseline records per agent (accumulating Phase 2 scores + MR variant
  scores) via BaselineStore.store() from jerry/testing/baselines/store.py.
  Verify stored records:
    tests/prompt-regression/baselines/data/{agent}/{metric_id}/*.json

3E — Verification:
  Use /eng-team with eng-qa to verify:
  - N >= 20 paired observations per agent per MR
  - MR-001 delta <= 0.05 for both agents (or documented explanation if violated)
  - MR-003 delta <= 0.03 for both agents (or documented explanation if violated)
  - MR variant I/O traces exist and contain full prompt + response
  - BaselineStore contains N >= 30 records per agent
  - CalibrationRunner produced calibration results

  Output: orchestration/baseline-execution-20260308-001/phase3-verification.md

Phase 3 acceptance criteria:
  - MR-001 and MR-003 results at N>=20 for both agents
  - Variant I/O traces persisted for manual inspection
  - CalibrationRunner calibration results persisted
  - BaselineStore populated with N>=30 per agent
  - Cost ledger entry for Phase 3 API spend

Use /adversary with adv-scorer to score Phase 3 deliverables. Threshold: >= 0.94.
Output: orchestration/baseline-execution-20260308-001/reviews/adv-phase3-score.md

---

Phase 4 — Statistical Comparison with Real Baselines (eng-backend + eng-qa)

Use /eng-team with eng-backend to run the Layer 4 statistical pipeline.

4A — Layer4Pipeline Execution:
  Use Layer4Pipeline from jerry/testing/layer4_stats.py to:
  - Load real baseline scores from BaselineStore (populated in Phase 3D)
  - Load candidate scores (latest Phase 2 composites)
  - Run Wilcoxon signed-rank test for each quality dimension
  - Apply Bonferroni correction (k=6 dimensions)
  - Compute Wilson score confidence intervals for pass rates
  - Classify: NO_REGRESSION / MARGINAL / REGRESSION per dimension
  - Produce overall merge decision: PASS / BLOCK / WARNING

  Persist Layer 4 report:
    orchestration/baseline-execution-20260308-001/phase4-statistical-report.md

  Persist raw statistical data:
    orchestration/baseline-execution-20260308-001/phase4-stats.json

  The stats JSON includes:
  {
    "agents": {
      "ps-researcher": {
        "baseline_n": 30,
        "candidate_n": N,
        "dimensions": {
          "completeness": {
            "wilcoxon_p": 0.XX,
            "bonferroni_adjusted_p": 0.XX,
            "mean_delta": 0.XX,
            "wilson_ci_lower": 0.XX,
            "wilson_ci_upper": 0.XX,
            "classification": "NO_REGRESSION"
          },
          ...
        },
        "overall_classification": "NO_REGRESSION",
        "merge_decision": "PASS"
      },
      "ps-architect": { ... }
    }
  }

4B — Verification:
  Use /eng-team with eng-qa to verify:
  - Wilcoxon test used real baselines (not synthetic random.Random(42))
  - Bonferroni correction applied with k=6
  - Wilson CIs computed for all dimensions
  - PASS/BLOCK/WARNING verdict is consistent with p-values and classifications
  - Statistical report is human-readable with interpretation guidance

  Output: orchestration/baseline-execution-20260308-001/phase4-verification.md

Phase 4 acceptance criteria:
  - Layer 4 report with Wilcoxon p-values, Wilson CIs, and verdicts
  - phase4-stats.json with all statistical data
  - Verdicts derived from real baselines
  - Report includes interpretation guidance for non-statisticians

Use /adversary with adv-scorer to score Phase 4 deliverables. Threshold: >= 0.94.
Output: orchestration/baseline-execution-20260308-001/reviews/adv-phase4-score.md

---

Phase 5 — CI/CD Integration Verification (eng-qa + red-vuln)

Use /eng-team with eng-qa to verify CI/CD workflow integration.

5A — Workflow Consumption Test:
  Verify that the existing GitHub Actions workflows can consume real baseline data:
  - .github/workflows/prompt-regression-smoke.yml
  - .github/workflows/prompt-regression-standard.yml
  - .github/workflows/prompt-regression-full.yml

  Confirm:
  - Workflows reference the correct baseline data paths
  - BLOCK verdict causes workflow failure (non-zero exit code)
  - WARNING verdict produces annotations without failing
  - PASS verdict passes cleanly

5B — Security Review:
  Use /red-team with red-vuln to review:
  - API key handling in all execution scripts (ANTHROPIC_API_KEY env var only)
  - Prompt injection surface in I/O capture artifacts (captured responses could
    contain adversarial content that downstream consumers might execute)
  - File path traversal risk in I/O trace storage paths
  - Credential leakage in GitHub Actions logs

  Output: orchestration/baseline-execution-20260308-001/red-vuln-security-review.md

5C — Final Integration Report:
  Produce a synthesis report covering:
  - Cost ledger: total API spend across all phases for both agents
  - Quality summary: all phase scores and verdicts
  - I/O visibility confirmation: count of captured traces, sample inspection results
  - Expansion guidance: steps to add the remaining 3 agents (ps-analyst, ps-critic,
    adv-scorer) using the same pipeline

  Output: orchestration/baseline-execution-20260308-001/final-integration-report.md

Phase 5 acceptance criteria:
  - CI/CD workflows verified against real baseline data
  - Security review completed with no unmitigated critical findings
  - Cost ledger populated with actual API token costs
  - Expansion guidance documented

Use /adversary with adv-scorer to score Phase 5 deliverables. Threshold: >= 0.94.
Output: orchestration/baseline-execution-20260308-001/reviews/adv-phase5-score.md

---

Cross-Cutting Requirements:

Cost Tracking:
  Maintain a running cost ledger at:
    orchestration/baseline-execution-20260308-001/cost-ledger.md
  Track per-phase: number of API calls, input/output tokens, estimated USD cost.
  Budget ceiling: $20 for 2 agents. Halt and escalate if projected cost exceeds budget.

I/O Visibility:
  Every LLM call (agent execution, G-Eval judge, MR variant execution) produces
  a persisted I/O trace file. The user can inspect the exact prompt and response
  for any individual run by reading the corresponding JSON file.

Quality Gates:
  C3 criticality level. >= 0.94 weighted composite (S-014 dimensions) per phase.
  Minimum 3 creator-critic iterations per H-14 before phase advancement.
  Circuit breaker: if any phase fails quality gate after 5 iterations, halt and
  escalate to user with current best result and critic findings.

All output paths are relative to projects/PROJ-036-prompt-regression-harness/.
```

---

## Self-Review Score

Self-assessment against the 7-criterion prompt quality rubric (H-15, S-010).

| # | Criterion | Weight | Raw (0-3) | Weighted | Rationale |
|---|-----------|--------|-----------|----------|-----------|
| C1 | Task Specificity | 20% | 3 | 20.0 | All terms defined. No trailing fragments. Specific file paths, agent names, JSON schemas, thresholds, and acceptance criteria per phase. |
| C2 | Skill Routing | 18% | 3 | 18.0 | Five skills invoked with `/skill` syntax: `/orchestration`, `/eng-team` (eng-backend, eng-qa), `/red-team` (red-vuln), `/adversary` (adv-scorer), `/worktracker`. All agent names specified. |
| C3 | Context Provision | 15% | 3 | 15.0 | All data sources named with exact file paths. Existing infrastructure referenced by module path. No redundant inline content -- files referenced by path. |
| C4 | Quality Specification | 15% | 3 | 15.0 | Numeric threshold (>= 0.94) with named mechanism (S-014 LLM-as-Judge via adv-scorer). C3 criticality. H-14 iteration minimum. Circuit breaker specified. |
| C5 | Decomposition | 12% | 3 | 12.0 | 5 named phases with sync barriers. Sub-phases (1A-1C, 2A-2C, etc.) with explicit dependencies. Per-phase acceptance criteria. |
| C6 | Output Specification | 12% | 3 | 12.0 | Every phase has explicit output file path, format (JSON schema or markdown), and verification criteria. Orchestration plan path specified. |
| C7 | Positive Framing | 8% | 3 | 8.0 | All instructions are positive directives. NPT-013 constraints are in a separate section with constructive alternatives. No prohibitions in the main prompt body. |
| | **Total** | | | **100.0** | **Tier: Exemplary** |

**Scoring formula applied:** `sum((raw_N / 3) * weight_N * 100) = 100.0`

**Pre-Submission Checklist:**

```
SPECIFICITY
[x] Are all clauses grammatically and semantically complete?
[x] Are all vague descriptors replaced with concrete referents?

SKILL ROUTING
[x] Does each needed skill appear with /slash-command syntax?
[x] Is the specific agent named when a multi-agent workflow is intended?

CONTEXT
[x] Is the data source named? (exact file paths for all referenced modules)
[x] Is the domain scope specified? (PROJ-036, 2 agents, specific prompts)
[x] Is any time range relevant? If yes, is it stated? (2026-03-08)

QUALITY
[x] Is a numeric quality threshold present? (>= 0.94)
[x] Is adversarial critique explicitly requested? (adv-scorer after each phase)

OUTPUT
[x] Is the output file path, format, and structure specified? (per-phase paths + JSON schemas)
```
