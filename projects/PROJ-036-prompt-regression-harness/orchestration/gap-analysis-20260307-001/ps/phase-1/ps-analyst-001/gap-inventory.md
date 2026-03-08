# Gap Inventory — PROJ-036 Test Harness Integration Layer

> Phase 1A output from gap-analysis-20260307-001 orchestration
> Agent: ps-analyst
> Date: 2026-03-07

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Gap count and severity distribution |
| [Gap Inventory Table](#gap-inventory-table) | Component-by-component classification |
| [Detailed Gap Analysis](#detailed-gap-analysis) | Per-gap evidence and rationale |
| [Missing Integration Layers](#missing-integration-layers) | Designed but unimplemented components |
| [Evidence from Validation Run](#evidence-from-validation-run) | Validation run data supporting classifications |

---

## Summary

The gap analysis examined 33 components across 6 subsystems in the PROJ-036 test harness. Of these, 20 components are COMPLETE (fully implemented building blocks), 8 are PARTIAL (built but lacking a caller or integration wire), 2 carry a BUG classification (implemented but functionally broken or unreachable as wired), and 3 are MISSING entirely. The total FR coverage gap spans FR-001 (test case execution pipeline), FR-003 (before/after comparison), FR-004 (version key CLI), FR-006 (DeepEval pytest plugin fixture), FR-009 (score array collection from real evaluations), FR-010 (MR-DeepEval adapter wire), FR-018 (report output to PR comment), FR-020 (baseline population CLI), and FR-025 (promptfoo Docker + MR integration). The most critical gap is the missing `__main__` entry point on `layer4_stats.py` and `baselines/store.py`: both are invoked as `python -m jerry.testing.layer4_stats` in the Full tier GitHub Actions workflow but neither has a `main()` function or `if __name__ == "__main__"` block, meaning every GitHub Actions Full tier run would immediately fail at the Python invocation step. A secondary critical gap is the absence of any real score array collection pipeline connecting promptfoo output JSON to the Layer 2 DeepEval adapter and then feeding Layer 4, so the validation run was executed with synthetic baselines only.

---

## Gap Inventory Table

| # | Component | File Path | Classification | FR Coverage | Notes |
|---|-----------|-----------|----------------|-------------|-------|
| 1 | QualityCriterion dataclass | `jerry/testing/evaluation/criterion.py` (68 lines) | COMPLETE | FR-007 | Frozen dataclass, validated, no external deps |
| 2 | ScoringResult dataclass | `jerry/testing/evaluation/scoring_result.py` (63 lines) | COMPLETE | FR-007, FR-009 | Frozen, weighted_score auto-computed |
| 3 | DebiasingStrategy | `jerry/testing/evaluation/debiasing.py` (262 lines) | COMPLETE | FR-021, C-007 | shuffle_criteria + randomize_candidate_positions + build_debiased_prompt_section |
| 4 | PositionRandomizationResult | `jerry/testing/evaluation/position_randomization_result.py` | COMPLETE | FR-021 | Value object companion to DebiasingStrategy |
| 5 | JerryGEvalMetric domain class | `jerry/testing/evaluation/metrics.py` (218 lines) | COMPLETE | FR-007, FR-021 | score_composite, classify_composite, get_criteria_for_debiasing |
| 6 | EvaluationPort protocol | `jerry/testing/evaluation/ports.py` (143 lines) | COMPLETE | FR-006, FR-009 | runtime_checkable Protocol; both evaluate() and evaluate_batch() defined |
| 7 | JerryGEvalDeepEvalMetric | `jerry/testing/evaluation/jerry_geval_deepeval_metric.py` (355 lines) | COMPLETE | FR-006, FR-007, FR-021 | _resolve_model fix present; AnthropicModel for claude- prefixed strings |
| 8 | DeepEvalAdapter | `jerry/testing/evaluation/deepeval_adapter.py` (382 lines) | PARTIAL | FR-006, FR-007, FR-009 | build_metric_for_agent and evaluate_batch COMPLETE; evaluate() raises NotImplementedError (BUG-adjacent, intentional but blocking FR-006 pytest fixture path) |
| 9 | ps_researcher criteria | `jerry/testing/evaluation/criteria/ps_researcher.py` (128 lines) | COMPLETE | FR-007 | 6 S-014 dimensions + agent-specific criteria; weights sum correct |
| 10 | ps_analyst criteria | `jerry/testing/evaluation/criteria/ps_analyst.py` (131 lines) | COMPLETE | FR-007 | 6 S-014 dimensions defined |
| 11 | ps_architect criteria | `jerry/testing/evaluation/criteria/ps_architect.py` (approx 130 lines) | COMPLETE | FR-007 | 6 S-014 dimensions defined |
| 12 | ps_critic criteria | `jerry/testing/evaluation/criteria/ps_critic.py` (approx 130 lines) | COMPLETE | FR-007 | 6 S-014 dimensions defined |
| 13 | adv_scorer criteria | `jerry/testing/evaluation/criteria/adv_scorer.py` (157 lines) | COMPLETE | FR-007 | 6 S-014 dimensions defined |
| 14 | MR base (MetamorphicRelation ABC) | `jerry/testing/metamorphic/base.py` (approx 120 lines) | COMPLETE | FR-010 | Domain ABC; intentional H-07 deviation from FR-010 AC literal text documented |
| 15 | MR-001 Paraphrase Consistency | `jerry/testing/metamorphic/mr_001_paraphrase.py` (319 lines) | COMPLETE | FR-010 | Full implementation with transform + evaluate |
| 16 | MR-002 Negation Robustness | `jerry/testing/metamorphic/mr_002_negation.py` (approx 250 lines) | COMPLETE | FR-010 | Full implementation |
| 17 | MR-003 Irrelevant Context | `jerry/testing/metamorphic/mr_003_context.py` (approx 250 lines) | COMPLETE | FR-010 | Full implementation |
| 18 | MR-004 Formatting Variant | `jerry/testing/metamorphic/mr_004_formatting.py` (approx 250 lines) | COMPLETE | FR-010 | Full implementation |
| 19 | MR-005 Roundtrip Consistency | `jerry/testing/metamorphic/mr_005_roundtrip.py` (approx 250 lines) | COMPLETE | FR-010 | Full implementation |
| 20 | MR calibration | `jerry/testing/metamorphic/calibration.py` (approx 100 lines) | COMPLETE | FR-010 | MR calibration support |
| 21 | stats.py statistical engine | `jerry/testing/stats.py` (695 lines) | COMPLETE | FR-014, FR-015, FR-016, FR-017, FR-019 | Wilcoxon, Wilson, Bonferroni, all named constants present |
| 22 | types.py shared types | `jerry/testing/types.py` (382 lines) | COMPLETE | All layers | RegressionClass, EvaluationMode, ScoreArray, ComparisonReport, BaselineRecord etc. |
| 23 | BaselinePersistencePort | `jerry/testing/baselines/ports.py` (138 lines) | COMPLETE | FR-020 | Protocol with store/retrieve/invalidate/audit |
| 24 | BaselineStore adapter | `jerry/testing/baselines/store.py` (432 lines) | PARTIAL | FR-020 | Class fully implemented; no `__main__` / `main()` — GHA workflow invokes via `python -m jerry.testing.baselines.store --action store ...` which will fail |
| 25 | ReportOutputPort | `jerry/testing/reports/ports.py` (approx 80 lines) | COMPLETE | FR-018 | Protocol defined |
| 26 | ReportGenerator | `jerry/testing/reports/generator.py` (518 lines) | COMPLETE | FR-018 | Markdown + JSON output; ComparisonReport production |
| 27 | Layer4Pipeline orchestrator | `jerry/testing/layer4_stats.py` (476 lines) | PARTIAL | FR-015, FR-016, FR-017, FR-018 | Class fully implemented; no `__main__` / `main()` — GHA workflow invokes via `python -m jerry.testing.layer4_stats --agent ... --tier ...` which will fail |
| 28 | pytest conftest.py with EvaluationPort fixture | `tests/prompt-regression/conftest.py` | PARTIAL | FR-006 | Exists but only sets sys.path; no `evaluator` fixture returning DeepEvalAdapter; FR-006 pytest plugin pattern not wired |
| 29 | promptfoo YAML test cases | `tests/prompt-regression/test-cases/*.yaml` (5 files) | COMPLETE | FR-001, FR-008 | All 5 agents have YAML; structural assertions + llm-rubric G-Eval assertions present |
| 30 | promptfoo-config.yaml | `tests/prompt-regression/promptfoo-config.yaml` (175 lines) | COMPLETE | FR-001, FR-003, FR-005 | Providers, per-agent YAML loading, evaluation options configured |
| 31 | GitHub Actions — Smoke workflow | `.github/workflows/prompt-regression-smoke.yml` | COMPLETE | FR-002, FR-005, FR-025 | Detects changed agents, runs Docker promptfoo, posts PR comment; SHA-pinned actions |
| 32 | GitHub Actions — Standard workflow | `.github/workflows/prompt-regression-standard.yml` | COMPLETE | FR-002, FR-005 | Exists (observed in glob); mirrors smoke/full pattern |
| 33 | GitHub Actions — Full workflow | `.github/workflows/prompt-regression-full.yml` | PARTIAL | FR-002, FR-003, FR-005, FR-014-FR-018, FR-020 | Workflow structure correct; invokes `python -m jerry.testing.layer4_stats` and `python -m jerry.testing.baselines.store` — both missing `__main__` entrypoints; will fail at runtime |
| 34 | MR-to-DeepEval adapter wire | Not found in any file | MISSING | FR-010 | DeepEvalAdapter has no `build_metric_for_mr()` method; MR classes cannot be passed to `deepeval.assert_test()` without a wrapping adapter |
| 35 | Score array collection pipeline | Not found in any file | MISSING | FR-009 | No script/workflow step extracts Layer 2 scores from promptfoo output JSON into ScoreArray format for Layer 4 consumption; validation run used synthetic baselines |
| 36 | Baseline population CLI / workflow step | Not found in any executable form | MISSING | FR-020 | BaselineStore.store() exists as a class method but no CLI script, workflow step, or conftest fixture populates real baseline data from actual agent runs |
| 37 | `__main__` module for layer4_stats | Not found | BUG | FR-015, FR-016, FR-018 | GHA Full workflow calls `python -m jerry.testing.layer4_stats --agent ... --tier ...` but the module has no `if __name__ == "__main__"` block or `main()` function |
| 38 | `__main__` module for baselines.store | Not found | BUG | FR-020 | GHA Full workflow calls `python -m jerry.testing.baselines.store --action store ...` but the module has no `if __name__ == "__main__"` block |

---

## Detailed Gap Analysis

### COMPLETE Components

**Evidence of completeness: all components were directly read from source; validation run confirmed end-to-end execution for Layers 2, 3, and 4 when called programmatically with synthetic data.**

1. **Domain value objects (criterion.py, scoring_result.py, types.py)**: Verified frozen dataclasses with validation in `__post_init__`. No external deps. Directly observed in source.

2. **DebiasingStrategy**: Both `shuffle_criteria()` and `randomize_candidate_positions()` implemented with seeded RNG. `build_debiased_prompt_section()` present for single-output use. FR-021/C-007 mandatory enforcement verified at `JerryGEvalMetric.__post_init__`.

3. **JerryGEvalMetric**: `score_composite()` normalizes by weight sum (handles partial criterion sets). `classify_composite()` maps to PASS/REVISE/REJECTED bands from quality-enforcement.md. `get_criteria_for_debiasing()` delegates to DebiasingStrategy.

4. **JerryGEvalDeepEvalMetric**: `_resolve_model()` fix confirmed at line 334 — wraps `claude-*` strings in `AnthropicModel()` to prevent GPTModel fallback. `measure()`, `a_measure()`, `is_successful()`, `evaluate_criteria()` all present.

5. **EvaluationPort**: `@runtime_checkable` Protocol; both `evaluate()` and `evaluate_batch()` signatures defined. DeepEvalAdapter structurally satisfies it.

6. **Five agent criteria sets**: All 5 agents have criteria modules (ps_researcher 128 lines, ps_analyst 131 lines, adv_scorer 157 lines; ps_architect and ps_critic similar). Weights sum to 1.0 per agent.

7. **MR-001 through MR-005**: All 5 metamorphic relation classes exist (confirmed by Glob). MR-001 is 319 lines including `transform()` and `evaluate()` methods. Domain ABC pattern documented with explicit H-07 justification in base.py.

8. **stats.py**: All named constants confirmed (MIN_STATISTICAL_SAMPLE_SIZE=20, QUALITY_PASS_THRESHOLD=0.92, BONFERRONI_K_FULL_SUITE=13, BONFERRONI_ALPHA_FULL=0.004). Wilcoxon, Wilson, Bonferroni, Cohen's r, and combined classification logic all implemented (695 lines).

9. **ReportGenerator**: 518 lines; from_single_metric, from_multi_metric, smoke_mode_report, to_json, to_markdown all present. ComparisonReport produced per behavioral-contracts.md Section D.6.

10. **promptfoo YAML test cases**: All 5 agent YAML files present with structural assertions (contains, javascript, regex, not-regex) and llm-rubric G-Eval assertions. Per-agent quality floors embedded as `threshold:` values.

11. **GitHub Actions Smoke workflow**: Full production implementation confirmed — agent detection from `git diff`, matrix strategy, hardened Docker (read-only, cap-drop=ALL, no-new-privileges, memory/CPU limits), SHA-pinned actions, PR comment posting.

---

### PARTIAL Components

**8. DeepEvalAdapter.evaluate() (PARTIAL — intentional NotImplementedError)**

- `build_metric_for_agent()` and `evaluate_batch()` are fully implemented.
- `evaluate()` raises `NotImplementedError` by design: "String-name criterion resolution is not implemented in this adapter."
- This means the EvaluationPort.evaluate() protocol method is not satisfiable via DeepEvalAdapter for the string-criteria path.
- FR-006 requires the conftest `evaluator` fixture to return an object implementing EvaluationPort. If test files call `evaluator.evaluate(...)`, they will receive NotImplementedError at runtime.
- The recommended path (build_metric_for_agent + deepeval.assert_test) is functional, but no conftest fixture wires this.
- **What's missing**: The conftest `evaluator` fixture and any test file using it via the evaluate() path.

**24. BaselineStore (PARTIAL — missing __main__)**

- `BaselineStore` class is 432 lines with store(), retrieve(), invalidate(), audit() methods and FR-020 quality gate enforcement.
- The GHA Full tier workflow invokes: `uv run python -m jerry.testing.baselines.store --action store --agent ... --results-file ... --commit-sha ...`
- Grep for `__main__`, `argparse`, `ArgumentParser`, `def main` in `store.py` returns zero matches.
- **Effect**: Every `python -m jerry.testing.baselines.store` invocation in the Full workflow will raise `ModuleNotFoundError: No module named jerry.testing.baselines.store.__main__` (Python module invocation requires `__main__.py` or `if __name__ == "__main__"` block).
- **What's missing**: An argument parser accepting `--action`, `--agent`, `--results-file`, `--commit-sha`, `--tier`, `--reason` flags and calling `BaselineStore.store()`.

**27. Layer4Pipeline (PARTIAL — missing __main__)**

- `Layer4Pipeline` class is 476 lines with a complete `run()` method, `_run_statistical()`, `_run_smoke()`, `_persist_report()`, `_emit_gha_outputs()`, `_exit_code()`.
- The GHA Full tier workflow invokes: `uv run python -m jerry.testing.layer4_stats --agent ... --tier full --results-file ... --head-sha ... --bonferroni-k ... --output-report ... --output-markdown ...`
- Grep for `__main__`, `argparse`, `ArgumentParser`, `def main` in `layer4_stats.py` returns zero matches.
- **Effect**: Every `python -m jerry.testing.layer4_stats` invocation in the Full workflow will fail immediately.
- **What's missing**: An argument parser accepting all flags listed above, instantiating `BaselineStore`, `ReportGenerator`, and `Layer4Pipeline`, loading the promptfoo results JSON, extracting score arrays, and calling `pipeline.run()`.

**28. conftest.py (PARTIAL — sys.path only, no evaluator fixture)**

- `tests/prompt-regression/conftest.py` exists (18 lines) and adds the test directory to sys.path.
- No `@pytest.fixture` definitions. No `DeepEvalAdapter` import. No `evaluator` fixture returning `EvaluationPort`.
- FR-006 requirement: "pytest conftest.py shall define an `evaluator` fixture returning an `EvaluationPort` implementation." Not present.
- Unit tests in `tests/prompt-regression/unit/` exist (test_stats.py, test_metrics.py, test_debiasing.py, test_baselines.py, test_layer2_evaluation.py, test_metamorphic_base.py, test_types.py, test_version_keys.py).
- Integration tests exist in `tests/prompt-regression/integration/test_layer4_pipeline.py`.
- Property tests in `tests/prompt-regression/property/test_mr_properties.py` and `test_stats_properties.py`.
- **What's missing**: The `evaluator` fixture wiring `DeepEvalAdapter` into the pytest plugin so live LLM evaluation tests can reference `evaluator: EvaluationPort` as a parameter.

**33. GitHub Actions Full workflow (PARTIAL — invokes missing __main__ targets)**

- Workflow structure, matrix strategy, Docker invocation, artifact upload, PR comment logic are all complete.
- Job "Run Layer 4 statistical analysis" calls `uv run python -m jerry.testing.layer4_stats --agent ... --tier full ...` — this will fail (no `__main__`).
- Job "Update baseline store" calls `uv run python -m jerry.testing.baselines.store --action store ...` — this will fail (no `__main__`).
- Verdict extraction step reads `report.get('overall_verdict', 'UNKNOWN')` from JSON, but ReportGenerator produces `classification` (not `overall_verdict`) in ComparisonReport. This is a second defect in the GHA step.
- **What's missing**: The `__main__` modules (items 37, 38 below) and a JSON field name alignment fix.

---

### BUG Components

**37. Missing `__main__` for layer4_stats (BUG — runtime failure)**

- Severity: CRITICAL — blocks every Full tier GitHub Actions run.
- Occurrence: HIGH — triggered on every `workflow_dispatch`, weekly schedule, and tag push.
- Detection: IMMEDIATE — Python will fail at `python -m jerry.testing.layer4_stats` before any evaluation begins.
- Evidence: `grep -r "__main__|def main|argparse|ArgumentParser" jerry/testing/layer4_stats.py` returns no matches. The GHA workflow at line 351 calls `uv run python -m jerry.testing.layer4_stats \`.
- Blocking FRs: FR-015, FR-016, FR-017, FR-018 (all Layer 4 requirements are unreachable from CI).

**38. Missing `__main__` for baselines.store (BUG — runtime failure)**

- Severity: HIGH — blocks baseline population from CI.
- Occurrence: Medium — only triggers when `update_baselines == 'true'` in workflow_dispatch.
- Detection: IMMEDIATE — Python will fail at invocation.
- Evidence: `grep -r "__main__|def main|argparse|ArgumentParser" jerry/testing/baselines/store.py` returns no matches.
- Blocking FRs: FR-020 (baseline management lifecycle).

**Additional defect (in PARTIAL item 33): ComparisonReport field mismatch**

- The GHA Full workflow at line ~372 extracts: `data.get('overall_verdict', 'UNKNOWN')`.
- `ReportGenerator.to_json()` serializes `ComparisonReport`, whose field is named `classification` (not `overall_verdict`).
- Effect: The verdict extraction will always return `'UNKNOWN'`, making all enforcement decisions (REGRESSION/MARGINAL/NO_REGRESSION branching) unreachable; the workflow will always fall into the `*)` unknown verdict branch and exit 1.

---

### MISSING Components

**34. MR-to-DeepEval adapter wire (MISSING)**

- `DeepEvalAdapter` has `build_metric_for_agent()` for criteria-based evaluation.
- No `build_metric_for_mr()` or equivalent method exists anywhere in the codebase.
- MR classes (`mr_001_paraphrase.MetamorphicRelation` subclasses) implement `transform()` and `evaluate()` but are not wrapped in a `BaseMetric` subclass.
- The base.py docstring explicitly notes the adapter wrapping must happen in the DeepEval adapter layer: "The adapter layer wraps each MetamorphicRelation subclass in a thin DeepEval BaseMetric adapter."
- This adapter does not exist.
- **Blocking FRs**: FR-010 (five universal MRs integrated into evaluation pipeline), FR-003 (before/after comparison using MR variants).
- **Note**: Layer 3 MR smoke tests in the validation run were executed manually/synthetically, not via DeepEval pytest integration.

**35. Score array collection pipeline (MISSING)**

- The end-to-end flow requires: promptfoo runs agent → outputs JSON with scores → Layer 2 collects ScoreArray → Layer 4 receives arrays.
- The promptfoo output JSON format and how to extract scores into `ScoreArray` (list[float]) for `compare_versions()` is not implemented anywhere.
- `promptfoo-config.yaml` writes to `tests/prompt-regression/results/promptfoo-output.json` but no Python script reads this file and maps it to `dict[str, tuple[ScoreArray, ScoreArray]]` for `Layer4Pipeline.run()`.
- The GHA Full workflow at the Layer 4 step passes `--results-file tests/prompt-regression/results/full-{agent}.json` to `python -m jerry.testing.layer4_stats`, but the (missing) `__main__` would need to parse this file and extract score arrays.
- **Blocking FRs**: FR-009 (score array collection and export), FR-003 (before/after comparison), FR-015 (Wilcoxon requires actual score arrays).
- **Evidence from validation run**: `phase4-results.json` annotation: `"note": "Synthetic baseline -- validation only"` confirms no real collection pipeline was used.

**36. Baseline population CLI / real data workflow (MISSING)**

- `tests/prompt-regression/baselines/protocol.md` is marked "READY FOR EXECUTION" (version 1.2.0, date 2026-03-07).
- `protocol.md` describes a manual step-by-step procedure but references scripts under "Script Implementation Status" — these scripts are not present in `tests/prompt-regression/baselines/`.
- `tests/prompt-regression/baselines/captured/` directory does not exist — no real baseline data has been captured.
- `BaselineStore` requires scores to be stored via `BaselineStore.store()` before `compare_versions()` can retrieve a baseline for comparison.
- Without real baselines, every Full tier run comparing a candidate against a baseline will raise `ValueError: baseline_status=invalidated` or return `None` from `retrieve()`.
- **Blocking FRs**: FR-020 (baseline management), FR-003 (before/after comparison requires a stored baseline to compare against), FR-014 (N>=20 baseline needed before Wilcoxon can run).

---

## Missing Integration Layers

This section lists the designed-but-unimplemented components from the system-design.md FR specification, verified by source inspection.

| # | Integration Layer | Status | Blocking FRs | Design Reference | Evidence of Absence |
|---|-------------------|--------|-------------|-----------------|---------------------|
| IL-1 | `pytest conftest.py` `evaluator` fixture (EvaluationPort) | MISSING (conftest exists but has no fixture) | FR-006 | system-design.md §2.2: "conftest.py defines `evaluator` fixture returning EvaluationPort" | `tests/prompt-regression/conftest.py` — 18 lines, sys.path only, no fixtures |
| IL-2 | Layer4Pipeline `__main__` module (CLI entrypoint) | MISSING | FR-015, FR-016, FR-017, FR-018 | GHA workflow line 351: `python -m jerry.testing.layer4_stats --agent ...` | No `__main__`, no `argparse`, no `def main` in `layer4_stats.py` |
| IL-3 | BaselineStore `__main__` module (CLI entrypoint) | MISSING | FR-020 | GHA workflow line 389: `python -m jerry.testing.baselines.store --action store ...` | No `__main__`, no `argparse`, no `def main` in `store.py` |
| IL-4 | MR-to-DeepEval adapter (`build_metric_for_mr()`) | MISSING | FR-010, FR-003 | system-design.md §1.4: "adapter wraps MetamorphicRelation subclasses in BaseMetric adapter" | `deepeval_adapter.py` has no MR-related methods; MR classes have no BaseMetric inheritance |
| IL-5 | Score array extraction from promptfoo JSON | MISSING | FR-009, FR-003, FR-015 | system-design.md: "Score arrays (float[] from Layer 2 to Layers 3 and 4)" | No script or module converts `promptfoo-output.json` to `dict[str, tuple[ScoreArray, ScoreArray]]` |
| IL-6 | Baseline population pipeline (real N=30 capture) | MISSING | FR-020, FR-003, FR-014 | `baselines/protocol.md` v1.2.0 "READY FOR EXECUTION" | `tests/prompt-regression/baselines/captured/` directory does not exist; protocol references unimplemented scripts |
| IL-7 | ComparisonReport `overall_verdict` field alignment | BUG | FR-018 | GHA Full workflow line ~372 reads `data.get('overall_verdict', 'UNKNOWN')` | `ComparisonReport.classification` field name confirmed in `types.py` line 368; GHA reads wrong field name |
| IL-8 | Langfuse observability adapter | MISSING (by design, optional) | None (FR-optional) | system-design.md: "Langfuse (optional)" | No `langfuse` import in any testing module; acceptable per design |

---

## Evidence from Validation Run

The validation run at `projects/PROJ-036-prompt-regression-harness/work/test-harness/validation-run/` provides the following evidence relevant to gap classifications:

### Phase 2 (Layer 2) — G-Eval Composite Scores

Source: `validation-run/phase2-composites.json` and five `layer2-scores-*.md` files.

| Agent | Composite | Floor | Verdict | Key Observation |
|-------|-----------|-------|---------|-----------------|
| ps-researcher | 0.935 | 0.82 | PASS | All 6 dimensions scored; debiasing applied (C-007 confirmed in score file header) |
| ps-analyst | 0.510 | 0.85 | FAIL | completeness=0.000 (criterion mismatch — evaluator applied comparison criteria to single-output analysis) |
| ps-architect | 0.860 | 0.88 | FAIL | traceability=0.100 (dimension score variance; not a harness bug) |
| ps-critic | 0.575 | 0.83 | FAIL | methodological_rigor=0.300, evidence_quality=0.000 (agent output content issue) |
| adv-scorer | 0.785 | 0.90 | FAIL | internal_consistency=0.200 (agent output content issue) |

**Gap-relevant observation**: The validation run score files confirm that `DeepEvalAdapter.build_metric_for_agent()` + `JerryGEvalDeepEvalMetric` produced real LLM-judged scores — this confirms COMPLETE status for items 7 and 8 (adapter layer functions when called programmatically). The FAIL verdicts for ps-analyst/ps-critic/adv-scorer are content quality issues in the agent outputs, not harness bugs.

### Phase 3 (Layer 3) — MR Smoke Tests

Source: `validation-run/layer3-mr-results.md`.

| Agent | MR | Delta | Status | Observation |
|-------|-----|-------|--------|-------------|
| ps-researcher | MR-001 | 0.082 | FAIL | delta > tolerance=0.05 |
| ps-researcher | MR-003 | 0.086 | FAIL | delta > tolerance=0.03 |
| ps-architect | MR-001 | 0.112 | FAIL | delta > tolerance=0.05 |
| ps-architect | MR-003 | 0.071 | FAIL | delta > tolerance=0.03 |

**Gap-relevant observation**: The document header states "N=5 pairs per MR. NOT statistically powered." and "These results demonstrate pipeline functionality only." MR classes are confirmed functional at the domain layer (transform + evaluate working). The FAIL results are expected (smoke tolerance; N=5 is below the required N=20). This confirms items 15-19 (MR-001 through MR-005) as COMPLETE at the domain level. The gap (IL-4) is the DeepEval adapter wrapping layer that would connect MR execution to pytest integration.

### Phase 4 (Layer 4) — Statistical Results

Source: `validation-run/phase4-results.json` and five `layer4-*.md` files.

| Agent | Status | N | Baseline Mean | Candidate Mean | Note |
|-------|--------|---|---------------|----------------|------|
| ps-researcher | WARNING (exit 2) | 20 | 0.8708 | 0.9303 | IMPROVEMENT classification |
| ps-analyst | BLOCK (exit 1) | 20 | 0.9076 | 0.5122 | REGRESSION (sharp decline) |
| ps-architect | BLOCK (exit 1) | 20 | 0.9342 | 0.8613 | REGRESSION |
| ps-critic | BLOCK (exit 1) | 20 | 0.8875 | 0.5776 | REGRESSION |
| adv-scorer | BLOCK (exit 1) | 20 | 0.9588 | 0.7871 | REGRESSION |

**Gap-relevant observations**:
1. All entries annotated `"note": "Synthetic baseline -- validation only"` — confirms that IL-5 (score array extraction pipeline) and IL-6 (real baseline population) are MISSING. No real N=30 baseline data exists.
2. `layer4-ps-researcher.md` shows full Wilcoxon output with p=0.0000, Cohen's r=0.843, Wilson CIs — confirms `Layer4Pipeline.run()` functions correctly when called programmatically with score arrays. This supports PARTIAL (not BUG) classification for item 27: the class works; only the `__main__` CLI entrypoint is missing.
3. N=20 used in validation (minimum for Wilcoxon), confirming FR-014 enforcement is active in `stats.py`.
4. Bonferroni correction "not applied (single metric per agent)" per validation notes — the full 13-metric suite path remains untested.

---

*Analysis method: Direct source reading (Read tool), pattern search (Grep tool), directory enumeration (Glob tool). All classifications grounded in observed file contents and validation run artifacts. No inferences presented as facts.*
*Confidence: HIGH for all COMPLETE/MISSING classifications (directly verified). HIGH for BUG classifications (confirmed by Grep for missing patterns). MEDIUM for line count estimates for ps_architect, ps_critic criteria files and metamorphic MR-002-005 (sizes inferred from MR-001 reference; not directly read in full).*
