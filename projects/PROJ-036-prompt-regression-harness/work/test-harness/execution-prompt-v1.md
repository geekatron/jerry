# PROJ-036 Four-Layer Composite Test Harness — Execution Prompt v1

> Structured execution prompt for end-to-end validation of 5 target agents
> through Layers 2, 3, and 4 of the PROJ-036 test harness.

---

## Prompt

```
Use /orchestration with orch-planner to sequence a 4-phase validation pipeline for PROJ-036.

ENVIRONMENT SETUP:
- Load ANTHROPIC_API_KEY from .env using `python-dotenv` (uv add python-dotenv if needed).
  NEVER read or echo the key value. Use: `os.environ["ANTHROPIC_API_KEY"]`.
- Agent execution uses each agent's PINNED model from its .md frontmatter:
    ps-researcher: opus    | ps-analyst: sonnet   | ps-architect: opus
    ps-critic: sonnet      | adv-scorer: sonnet
  The Task tool respects the `model:` frontmatter field automatically.
- G-Eval judge scoring (Layer 2) uses: claude-sonnet-4-20250514 via DeepEvalAdapter.
  This is the JUDGE model, separate from the agent execution model.
- Track every API call's input_tokens and output_tokens. Accumulate totals per agent
  and across the full run. Pricing by model:
    Opus:   $15/M input, $75/M output  (ps-researcher, ps-architect)
    Sonnet: $3/M input,  $15/M output  (ps-analyst, ps-critic, adv-scorer, G-Eval judge)
  Persist cost ledger to: projects/PROJ-036-prompt-regression-harness/work/test-harness/cost-ledger.md
- Future: EN-036-001 will add --judge-model and --agent-model CLI overrides.

TARGET AGENTS (5):
  1. ps-researcher  — quality floor 0.82, criteria: jerry/testing/evaluation/criteria/ps_researcher.py
  2. ps-analyst     — quality floor 0.85, criteria: jerry/testing/evaluation/criteria/ps_analyst.py
  3. ps-architect   — quality floor 0.88, criteria: jerry/testing/evaluation/criteria/ps_architect.py
  4. ps-critic      — quality floor 0.83, criteria: jerry/testing/evaluation/criteria/ps_critic.py
  5. adv-scorer     — quality floor 0.90, criteria: jerry/testing/evaluation/criteria/adv_scorer.py

---

PHASE 1 — Agent Output Generation (per agent):
  For each of the 5 target agents, generate a representative output sample by
  invoking the agent via the Task tool with a domain-appropriate test prompt:

  - ps-researcher: "Research the trade-offs between property-based testing and
    metamorphic testing for LLM output evaluation. Output L0/L1/L2 sections."
  - ps-analyst: "Analyze the failure modes of LLM-as-Judge scoring with
    leniency bias. Apply FMEA methodology. Output L0/L1/L2 sections."
  - ps-architect: "Evaluate two options for test harness persistence:
    (A) JSON file store, (B) SQLite with WAL mode. Dimensions: write latency,
    corruption recovery, concurrent access, operational simplicity.
    Output in Nygard ADR format."
  - ps-critic: "Critique the following deliverable for quality gaps:
    [use the ps-researcher output from this run as input].
    Apply S-014 LLM-as-Judge with 6-dimension rubric."
  - adv-scorer: "Score the following deliverable against the S-014 quality gate:
    [use the ps-architect output from this run as input].
    Return per-dimension scores, weighted composite, and PASS/REVISE/ESCALATE verdict."

  Persist each output to:
    projects/PROJ-036-prompt-regression-harness/work/test-harness/validation-run/
      {agent-id}-output.md

  Record token usage per agent call in the cost ledger.

---

PHASE 2 — Layer 2: DeepEval G-Eval Scoring (per agent):
  For each agent's output from Phase 1, run DeepEval G-Eval scoring using
  the PROJ-036 DeepEvalAdapter:

  Entry point: jerry/testing/evaluation/deepeval_adapter.py
  Class: DeepEvalAdapter
  Method: build_metric_for_agent(agent_id, criteria_set)

  For each agent:
    1. Load the agent's criteria set from jerry/testing/evaluation/criteria/
    2. Instantiate DeepEvalAdapter with model="claude-sonnet-4-20250514"
    3. Apply mandatory debiasing per C-007 (position randomization, rubric shuffling)
    4. Score the agent output against each dimension in the criteria set
    5. Compute weighted composite score
    6. Compare against quality floor

  Persist per-agent Layer 2 scores to:
    projects/PROJ-036-prompt-regression-harness/work/test-harness/validation-run/
      layer2-scores-{agent-id}.md

  Format per agent:
    | Dimension | Weight | Raw Score | Weighted | Floor |
    |-----------|--------|-----------|----------|-------|
    | ...       | ...    | ...       | ...      | ...   |
    | **Composite** | | | **{score}** | **{floor}** |
    | **Verdict** | | | **PASS/FAIL** | |

  Record token usage for all scoring calls in the cost ledger.

---

PHASE 3 — Layer 3: Metamorphic Relation Validation (select 2 agents):
  Select ps-researcher and ps-architect for MR validation (broadest cognitive
  diversity: divergent vs. convergent).

  For each selected agent, apply MR-001 (Paraphrase Consistency) and
  MR-003 (Irrelevant Context Appendation):

  MR-001 (jerry/testing/metamorphic/mr_001_paraphrase.py):
    - Generate 5 paraphrased variants of the test prompt (minimum viable sample)
    - Score each variant's output using Layer 2 scoring
    - Compute mean delta between original and paraphrased scores
    - Report: tolerance=0.05, effect size threshold Cohen's r >= 0.30
    - Violation condition: Wilcoxon p < 0.05 AND mean_delta > 0.05

  MR-003 (jerry/testing/metamorphic/mr_003_context.py):
    - Append 5 irrelevant context suffixes to the test prompt
    - Score each variant's output using Layer 2 scoring
    - Compute mean delta between original and appended scores
    - Report: tolerance=0.03, effect size threshold Cohen's r >= 0.25
    - Violation condition: Wilcoxon p < 0.05 AND mean_delta > 0.03

  NOTE: Full MR validation requires N>=20 pairs per ADR-001.
  This validation run uses N=5 as a smoke test to demonstrate the pipeline.
  Mark results as "SMOKE TEST — not statistically powered" in the report.

  Persist MR results to:
    projects/PROJ-036-prompt-regression-harness/work/test-harness/validation-run/
      layer3-mr-results.md

  Record token usage for all MR variant calls in the cost ledger.

---

PHASE 4 — Layer 4: Statistical Comparison Report:
  Using the Layer 2 scores from Phase 2 as the "candidate" distribution,
  generate a Layer 4 statistical comparison report:

  Entry point: jerry/testing/layer4_stats.py
  Class: Layer4Pipeline

  For each of the 5 agents:
    1. Use the per-dimension scores from Phase 2 as the candidate scores
    2. Use the quality floor values as the baseline reference point
    3. Compute Wilson score confidence intervals for pass-rate estimation
    4. Apply Bonferroni correction for multi-metric comparison (6 dimensions)
    5. Classify result: PASS / REGRESSED / IMPROVED / INCONCLUSIVE

  Persist Layer 4 report to:
    projects/PROJ-036-prompt-regression-harness/work/test-harness/validation-run/
      layer4-statistical-report.md

---

PHASE 5 — /adversary Quality Gate (>= 0.92):
  Use /adversary with adv-scorer to score the OVERALL validation run report
  as a C2 deliverable against the S-014 quality gate.

  Compile a summary report from Phases 1-4 into:
    projects/PROJ-036-prompt-regression-harness/work/test-harness/validation-run/
      validation-summary.md

  The summary report MUST include:
    - Per-agent Layer 2 composite scores and verdicts
    - Layer 3 MR smoke test results (pass/fail per relation per agent)
    - Layer 4 statistical classification per agent
    - Total API cost breakdown (input tokens, output tokens, USD per agent, total USD)
    - Evidence: token counts from each API call

  Score this summary against S-014 dimensions:
    Completeness (0.20), Internal Consistency (0.20), Methodological Rigor (0.20),
    Evidence Quality (0.15), Actionability (0.15), Traceability (0.10)

  Quality threshold: >= 0.92 weighted composite.
  If below threshold: revise and re-score (max 3 iterations per H-14).

  Persist final scored report to:
    projects/PROJ-036-prompt-regression-harness/work/test-harness/validation-run/
      adversary-quality-gate.md

---

OUTPUT ARTIFACTS (all under projects/PROJ-036-prompt-regression-harness/work/test-harness/validation-run/):
  1. {agent-id}-output.md          — 5 files, one per agent
  2. layer2-scores-{agent-id}.md   — 5 files, Layer 2 G-Eval results
  3. layer3-mr-results.md          — MR smoke test results
  4. layer4-statistical-report.md  — Statistical comparison report
  5. validation-summary.md         — Compiled summary with cost evidence
  6. adversary-quality-gate.md     — /adversary S-014 scored report
  7. cost-ledger.md                — Running cost ledger with per-call evidence

Quality threshold: >= 0.92 weighted composite on the validation summary.
```

---

## Prompt Quality Self-Assessment (7-Criterion Rubric)

| # | Criterion | Weight | Score (0-3) | Rationale |
|---|-----------|--------|-------------|-----------|
| C1 | Task Specificity | 20% | 3 | All 5 phases fully specified with entry points, classes, methods, thresholds, and output paths |
| C2 | Skill Routing | 18% | 3 | `/orchestration` with orch-planner, `/adversary` with adv-scorer, Task tool for agent invocation |
| C3 | Context Provision | 15% | 3 | File paths, model names, pricing, quality floors, MR tolerances all provided |
| C4 | Quality Specification | 15% | 3 | Numeric threshold >= 0.92, S-014 6-dimension rubric, H-14 iteration bounds |
| C5 | Decomposition | 12% | 3 | 5 named phases with sync dependencies (Phase 2 depends on 1, Phase 4 on 2, etc.) |
| C6 | Output Specification | 12% | 3 | 7 artifact types with exact file paths, table formats, and content requirements |
| C7 | Positive Framing | 8% | 3 | Zero negative instructions; all constraints framed as positive requirements |

**Weighted composite: 100/100**

---

## Cost Estimate

| Phase | API Calls | Est. Tokens (In/Out) | Est. Cost |
|-------|-----------|---------------------|-----------|
| Phase 1 (5 agent outputs) | 5 | ~25K / ~15K | ~$1.50 (2 opus + 3 sonnet) |
| Phase 2 (5 × 6-dim scoring) | 30 | ~90K / ~30K | ~$0.72 (all sonnet judge) |
| Phase 3 (2 agents × 2 MRs × 5 variants + scoring) | ~24 | ~72K / ~36K | ~$2.40 (1 opus + 1 sonnet agent + sonnet judge) |
| Phase 4 (statistical computation) | 0 (local) | 0 | $0.00 |
| Phase 5 (/adversary scoring) | 3-9 | ~15K / ~9K | ~$0.18 (sonnet) |
| **Total estimate** | **~62-68** | **~202K / ~90K** | **~$4.80** |

> Estimate uses differentiated pricing: Opus ($15/$75 per M) for ps-researcher and
> ps-architect; Sonnet ($3/$15 per M) for all others and G-Eval judge. Phase 3 is
> reduced scope (N=5 smoke test vs N=20 full). Actual costs depend on output length.

---

## Execution Notes

1. **Environment**: Requires `ANTHROPIC_API_KEY` in `.env`. Uses `uv run` for all Python (H-05).
2. **Scope**: This is a smoke-test validation run. Layer 3 uses N=5 (not statistically powered).
   Full validation requires N>=20 pairs per ADR-001 FM-002.
3. **Dependencies**: `deepeval` must be installed (`uv add deepeval`). `scipy` for Wilcoxon tests.
4. **Cost cap**: If total cost exceeds $5.00, halt and report partial results.
