# Quality Score Report: Stream 5C Test Suite — Iter 4

## L0 Executive Summary

**Score:** 0.9215/1.00 | **Verdict:** REVISE | **Weakest Dimension:** Actionability (0.89)
**One-line assessment:** The suite is technically sound and nearly complete, but falls 0.0185 below the 0.94 C4 threshold; the primary blocker is an overly permissive else-branch in `test_aggregate_dimension_driver_consistent_with_classification` that reduces the test's failure-signal value.

---

## Scoring Context

- **Deliverable:** 11 test files under `tests/prompt-regression/`
- **Deliverable Type:** Code (test suite — Four-Layer Composite Test Harness, Stream 5C)
- **Criticality Level:** C4
- **Scoring Strategy:** S-014 (LLM-as-Judge)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Threshold Applied:** 0.94 (C4 project-specific, per scoring context)
- **Iteration:** 4 (prior: iter1=0.876, iter2=0.922, iter3=0.9135)
- **Scored:** 2026-03-07T00:00:00Z

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.9215 |
| **Threshold** | 0.94 (C4) |
| **Verdict** | REVISE |
| **Strategy Findings Incorporated** | No |

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Completeness | 0.20 | 0.94 | 0.1880 | All public APIs covered; both iter4 fixes fully addressed; thin gap in direct `_validate_score_array` unit tests |
| Internal Consistency | 0.20 | 0.95 | 0.1900 | Zero contradictions across 11 files; iter4 assertions align with factory construction; behavioral contract cross-references consistent |
| Methodological Rigor | 0.20 | 0.92 | 0.1840 | Correct Hypothesis parameterization, `assume()` instead of early-return, mock injection, `dc_replace` for MARGINAL branch; one minor tight-tolerance concern in symmetry test |
| Evidence Quality | 0.15 | 0.90 | 0.1350 | FR traceability present throughout; behavioral-contracts.md section references in all relevant tests; minor: debiasing tests less FR-specific |
| Actionability | 0.15 | 0.89 | 0.1335 | All tests executable; precise error message assertions; iter4 fix 2 else-branch is too broad to flag non-regression dimension_driver errors reliably |
| Traceability | 0.10 | 0.91 | 0.0910 | FR-004/007/010/014-021, OWASP A03:2021, H-13, H-20 all cited; `H-20: 90% line coverage target` is a process reference not a behavioral spec |
| **TOTAL** | **1.00** | | **0.9215** | |

---

## Detailed Dimension Analysis

### Completeness (0.94/1.00)

**Evidence:**

`test_stats.py` covers every function exported from `stats.py`: `compare_versions()` (5 test classes, 17 methods), `compare_multiple_metrics()` (4 methods), `wilson_score_intervals()` (7 methods), `merge_decision_from_classification()` (6 methods mapping each `RegressionClass` value), `bonferroni_correction()` (5 methods), named constants (4 methods). Both custom exceptions (`InsufficientSamplesError`, `InvalidScoreArrayError`) validated as `ValueError` subclasses.

`test_types.py` covers all 12 exported types from `types.py`: `EvaluationMode` (5 methods), `RegressionClass` (7 methods), `RateClass` (2), `EffectSizeLabel` (4), `MergeDecision` (3), `BaselineRecord` (3), `WilcoxonResult` (2), `WilsonResult` (2), `BonferroniConfig` (2), `RegressionResult` (4), `MultiMetricResult` (7), `ScoreArray` (1).

`test_baselines.py` covers all 4 `BaselineStore` methods: `store()` (8 methods, including quality gate rejection, version key validation, N enforcement by mode), `retrieve()` (3), `audit()` (5), `invalidate()` (4).

`test_layer4_pipeline.py` covers 9 distinct behavioral surfaces: smoke mode (5 methods), full mode (6 methods), insufficient samples (3 methods), `run_single_metric()` (2 methods), `_exit_code()` (3 methods), `_aggregate_multi_metric()` (4 methods), lazy import path (1), `_persist_report()` (3 methods: JSON, Markdown, parent-dir creation), `_emit_gha_outputs()` (3 methods: dimension_driver branch, key=value format validation, OSError swallowing).

Both iter4 fixes are addressed: (1) `test_multi_metric_result_fields_present` now asserts `result.per_metric == {}`, `isinstance(result.bonferroni, BonferroniConfig)`, `result.dimension_driver == "completeness"`, `result.overall_classification == RegressionClass.NO_REGRESSION`, `result.merge_decision == MergeDecision.ALLOW` — all direct value assertions consistent with the factory. (2) `test_aggregate_dimension_driver_consistent_with_classification` replaces the previous incorrect test name and docstring with an invariant that correctly handles the statistical ambiguity of the inputs.

**Gaps:**

`_validate_score_array()` (the internal validation helper in `stats.py`) is tested only indirectly through `compare_versions()` and `wilson_score_intervals()` call sites. No dedicated test exercises the `require_variation=False` branch of this function (the Wilson path where all-identical arrays are permitted). The behavioral difference between the two `require_variation` modes is a meaningful contract.

**Improvement Path:**

Add a test in `test_stats.py`: `test_wilson_score_intervals_all_identical_accepted` — confirm that `wilson_score_intervals([0.95] * 20)` does not raise `InvalidScoreArrayError`, contrasting with `compare_versions()` which requires variation. This would close the explicit contract coverage for the `require_variation=False` path.

---

### Internal Consistency (0.95/1.00)

**Evidence:**

The iter4 fix to `test_multi_metric_result_fields_present` introduces five direct assertions that are fully consistent with the `_make_multi_metric_result(dimension_driver="completeness")` factory. The factory constructs: `per_metric={}`, `bonferroni=BonferroniConfig(k=13, ...)`, `dimension_driver="completeness"`, `overall_classification=RegressionClass.NO_REGRESSION`, `merge_decision=MergeDecision.ALLOW`. Each assertion matches exactly.

Cross-file FR consistency is maintained: FR-014's `N >= 20` threshold appears correctly as `MIN_STATISTICAL_SAMPLE_SIZE == 20` in `test_stats.py` and as `minimum_sample_size == 20` in `test_metamorphic_base.py`. FR-017's Bonferroni k=13 appears in both `test_stats.py` (`BONFERRONI_K_FULL_SUITE == 13`) and `test_metrics.py` (via `sample_criteria` fixture with 6 criteria summing to 1.0). The 0.92 threshold appears in `test_metrics.py` (`classify_composite`) and `test_stats.py` (`QUALITY_PASS_THRESHOLD == 0.92`), both consistent with `quality-enforcement.md` SSOT.

The `TestCompareVersionsRegression` class (`test_stats.py`) asserts that a regressed result has `merge_decision in (BLOCK, ALLOW_WITH_WARNING)` — this is consistent with the contract that a MARGINAL classification (when Wilcoxon is borderline) maps to `ALLOW_WITH_WARNING`. The multi-valued assertion is not a contradiction; it reflects the correct behavioral contract.

`test_aggregate_dimension_driver_consistent_with_classification` (iter4 fix 2): the `if REGRESSION: assert driver == "completeness"; else: assert driver is None or isinstance(driver, str)` structure is internally consistent with the pipeline's behavior under statistical ambiguity. No inconsistency relative to `Layer4Pipeline._aggregate_multi_metric()` source.

**Gaps:**

Minor: `test_compare_versions_improvement_allows_with_warning` in `test_stats.py` (line 209) asserts `merge_decision != BLOCK` for an IMPROVEMENT result. This is true, but IMPROVEMENT maps to `ALLOW_WITH_WARNING` per `merge_decision_from_classification()`, so a more precise assertion would be `== ALLOW_WITH_WARNING`. The test is not incorrect — it just understates the contract.

**Improvement Path:**

Tighten `test_compare_versions_improvement_allows_with_warning` to assert `result.merge_decision == MergeDecision.ALLOW_WITH_WARNING`. This would make the test falsifiable for the exact mapping, not merely for the negative.

---

### Methodological Rigor (0.92/1.00)

**Evidence:**

Hypothesis property-based testing is correctly structured throughout `test_stats_properties.py` and `test_mr_properties.py`:
- `_score_array_strategy()` filters with `len(set(scores)) > 1` to prevent all-identical inputs that defeat Wilcoxon (matching the `require_variation=True` path in stats.py).
- All property tests use `assume()` for filtering rather than `if ... return` inside the test body — this correctly signals to Hypothesis that filtered cases are excluded, not trivially passing. This is confirmed in the docstring of `test_mr001_evaluate_result_type` (line 159): "Use assume() instead of early-return so Hypothesis correctly tracks these as filtered examples, not test successes."
- `max_examples` values are calibrated to test execution cost: property tests use 20-50 examples, not 500+.
- `deadline=None` prevents false failures on slow CI runners.
- `HealthCheck.too_slow` and `HealthCheck.filter_too_much` are suppressed where the strategy is known to filter heavily.

Integration tests use proper mock injection (hexagonal ports): `Layer4Pipeline` receives `MagicMock` for both `BaselinePersistencePort` and `ReportOutputPort`. This allows testing orchestration logic without filesystem or LLM dependencies.

`TestAggregateMultiMetricMarginalDriver` uses `dataclasses.replace()` to manufacture a MARGINAL result deterministically, avoiding statistical fragility in branch coverage. The technique is documented in the class docstring.

`conftest.py` places sys.path manipulation at session scope, avoiding per-test module-level side effects.

**Gaps:**

`test_compare_versions_symmetry` (line 102): `assert abs(result_ab.wilcoxon.mean_delta + result_ba.wilcoxon.mean_delta) < 1e-9` — this tolerance assumes perfect arithmetic cancellation. In practice, `mean(a) - mean(b)` computed twice via `statistics.mean()` may have floating-point rounding that produces differences around 1e-16 to 1e-14, which is within 1e-9. However, the bound is tighter than necessary; `< 1e-9` could fail on edge cases with many tied ranks or unusual numerical configurations. The bound `< 1e-9` appears safe in practice but is borderline for a property test that runs against arbitrary Hypothesis-generated arrays.

`test_wilson_ci_width_decreases_with_n` uses `small_result.ci_width + 0.05` absolute tolerance. This permits the large-N CI to be up to 5 percentage points wider than the small-N CI. The tolerance is defensible for edge cases but means the test cannot catch a moderate CI-width regression in the statsmodels Wilson implementation.

**Improvement Path:**

1. Loosen `mean_delta` antisymmetry tolerance in `test_compare_versions_symmetry` to `< 1e-7` to provide a safety margin against floating-point accumulation across arbitrary Hypothesis inputs.
2. Consider tightening `test_wilson_ci_width_decreases_with_n` tolerance to `+ 0.02` after examining the actual variance in CI-width differences to verify 0.05 is not masking real regressions.

---

### Evidence Quality (0.90/1.00)

**Evidence:**

Every test module has a module-level docstring listing the behavioral contract being tested, with explicit FR references. Examples:
- `test_stats.py` line 14-20: `FR-014: N >= 20`, `FR-015: Wilcoxon`, `FR-016: Wilson`, `FR-017: Bonferroni`, `H-20: 90%`.
- `test_metamorphic_base.py` line 16-18: `FR-010: Five Universal MRs`, `behavioral-contracts.md Section C`.
- `test_metrics.py` line 13-16: `FR-007: G-Eval`, `quality-enforcement.md: S-014`, `H-20`.
- `test_debiasing.py` line 12-17: `FR-021: Debiasing`, `behavioral-contracts.md §B.5`.
- `test_version_keys.py` line 17-23: `FR-004 AC-1..AC-3`, `OWASP A03:2021`, `ASVS V5.1`.
- `test_layer4_pipeline.py` line 18-22: `FR-018: CI/CD exit codes`, `FR-019: one-way dependency`, `behavioral-contracts.md D.6`.

Individual test method docstrings carry FR citations: `test_store_full_mode_min_samples_rejection` cites `FULL mode` (FR-014 semantics). `test_bonferroni_correction_k13_alpha` cites `k=13 with alpha_family=0.05`. `test_emit_gha_outputs_writes_to_github_output_file` cites `FR-018: GitHub Actions requires strict key=value line format`.

The `test_score_composite_in_range` test (lines 218-237) embeds the complete arithmetic derivation as a docstring comment, making the expected value independently verifiable: `Expected: (0.75*0.20 + ... + 0.95*0.10) / 1.00 = 0.820`.

**Gaps:**

`test_debiasing.py` tests largely reference C-007 and §B.5 but do not cite explicit FR numbers for `shuffle_criteria()` and `randomize_candidate_positions()`. FR-021 is mentioned in the module docstring but individual test methods (e.g., `test_shuffle_criteria_changes_order`, `test_randomize_positions_never_swap_probability`) lack FR attribution in their docstrings.

`test_baselines.py` class `TestBaselineStoreStore` docstring does not explicitly cite FR-014 for the `test_store_full_mode_min_samples_rejection` test method body, though it references "FULL mode baseline with N < 30."

**Improvement Path:**

Add `FR-021` and `FR-021 AC-x` citations to individual test method docstrings in `test_debiasing.py`. Ensure `test_store_full_mode_min_samples_rejection` docstring references FR-014 explicitly.

---

### Actionability (0.89/1.00)

**Evidence:**

All 11 files are executable pytest tests with no `@pytest.mark.skip`, no `TODO` markers, and no unresolved import stubs. `conftest.py` ensures sys.path is set at session scope so `version_keys` can be imported from any working directory.

Error message assertions are precise and CI-diagnosable:
- `assert "19" in str(exc_info.value)` and `assert "Smoke mode" in str(exc_info.value)` (test_stats.py, lines 225-226) pin both the numeric value and the guidance text.
- `assert "invalidated" in str(exc_info.value).lower()` (test_baselines.py, line 238) pins the required word in the error message.
- `assert kv_pattern.match(line)` (test_layer4_pipeline.py, line 943) uses a compiled regex to validate GHA output format.

The `TestBuildVersionKeyMocked` class uses `monkeypatch.setattr` on `version_keys.get_file_last_commit_hash` and `version_keys.get_current_commit_hash` — this avoids subprocess calls while still exercising the version key construction logic. Any failure produces a precise error about which hash was not set correctly.

`test_persist_report_creates_parent_dirs` verifies that `output_json_path.parent.mkdir(parents=True, exist_ok=True)` is called, using `tmp_path / "nested" / "deep" / "report.json"`. If the pipeline fails to create parent dirs, `assert nested_json.exists()` fails immediately.

**Gap — Primary blocker:**

`test_aggregate_dimension_driver_consistent_with_classification` (iter4 fix 2, test_layer4_pipeline.py, lines 731-752):

```python
if multi.overall_classification == RegressionClass.REGRESSION:
    assert multi.dimension_driver == "completeness"
else:
    assert multi.dimension_driver is None or isinstance(multi.dimension_driver, str)
```

The else-branch (`assert multi.dimension_driver is None or isinstance(multi.dimension_driver, str)`) is vacuously true for any dimension_driver value: `None`, any string, and any subclass of `str` all satisfy it. If `_aggregate_multi_metric()` had a bug that returned `dimension_driver = "wrong_metric"` on a NO_REGRESSION outcome, this assertion would still pass. The test cannot catch incorrect dimension_driver values in the non-REGRESSION path.

The correct assertion for a NO_REGRESSION or IMPROVEMENT outcome from a single-metric result would be `assert multi.dimension_driver is None`, because the aggregate logic should only set a dimension_driver when there is an actionable regression to attribute.

**Improvement Path:**

Replace the else-branch with `assert multi.dimension_driver is None` to create a falsifiable assertion for the non-regression case. If the implementation can legitimately return a non-None driver in the NO_REGRESSION path (e.g., for MARGINAL), add separate test cases for each classification outcome rather than a single broad else.

---

### Traceability (0.91/1.00)

**Evidence:**

FR-to-test traceability is comprehensive across the suite:
- FR-004 (version key format): tested in `test_version_keys.py` via 6 test classes covering construction, hash validation, path traversal, from_string(), minimum runs, and validate_baseline_version_key().
- FR-007 (G-Eval): tested in `test_metrics.py` via DIMENSION_WEIGHTS, score_composite, classify_composite.
- FR-010 (metamorphic relations): tested in `test_metamorphic_base.py` and `test_mr_properties.py`.
- FR-014 (N >= 20): tested in `test_stats.py` (TestCompareVersionsInsufficientSamples, TestMergeDecisionFromClassification) and `test_layer4_pipeline.py` (TestPipelineInsufficientSamples).
- FR-015 (Wilcoxon): covered by `test_stats.py` (TestCompareVersionsNoRegression, TestCompareVersionsRegression, TestCompareVersionsImprovement) and `test_stats_properties.py` (symmetry, score bounds).
- FR-016 (Wilson CI): covered by `test_stats.py` (TestWilsonScoreIntervals) and `test_stats_properties.py` (CI bounds, CI width).
- FR-017 (Bonferroni): covered by `test_stats.py` (TestBonferroniCorrection, TestCompareMultipleMetrics) and `test_stats_properties.py` (alpha-decreases property).
- FR-018 (CI/CD exit codes): covered by `test_layer4_pipeline.py` (TestExitCodeMapping, TestPipelineFullMode exit code assertions, TestEmitGhaOutputs).
- FR-019 (one-way dependency): asserted structurally — `stats.py` imports only `types.py`, and `test_layer4_pipeline.py` documents this in its module docstring.
- FR-020 (baseline audit): covered by `test_baselines.py` (TestBaselineStoreAudit, 5 methods).
- FR-021 (debiasing): covered by `test_debiasing.py` (full class).

OWASP A03:2021 Injection and ASVS V5.1 Input Validation are cited in `test_version_keys.py` for path traversal and hash validation tests.

**Gaps:**

`test_stats.py` module docstring references `H-20: 90% line coverage target` — this is a process requirement (coverage gate), not a behavioral specification. The FR reference for minimum sample size should be the primary citation. This is a minor precision issue, not a missing trace.

FR-019 (one-way dependency rule) is documented textually in `test_layer4_pipeline.py` module docstring but there is no static import-check test that would fail at CI time if someone added an illegal import to `stats.py`. The traceability is asserted by documentation, not by an executable guard.

**Improvement Path:**

Add a test in `test_stats.py` that verifies `stats.py` does not import from `jerry.testing.evaluation`, `jerry.testing.metamorphic`, `jerry.testing.baselines`, or `jerry.testing.layer4_stats` (FR-019 one-way dependency). This could use `importlib` or `ast.parse()` to inspect the source file's imports without loading potentially circular modules.

---

## Improvement Recommendations (Priority Ordered)

| Priority | Dimension | Current | Target | Recommendation |
|----------|-----------|---------|--------|----------------|
| 1 | Actionability | 0.89 | 0.93 | Replace the else-branch in `test_aggregate_dimension_driver_consistent_with_classification` with `assert multi.dimension_driver is None` for non-REGRESSION classifications; add separate test cases for MARGINAL and IMPROVEMENT if needed |
| 2 | Internal Consistency | 0.95 | 0.96 | Tighten `test_compare_versions_improvement_allows_with_warning` to assert `== MergeDecision.ALLOW_WITH_WARNING` instead of `!= BLOCK` |
| 3 | Completeness | 0.94 | 0.96 | Add `test_wilson_score_intervals_all_identical_accepted` to explicitly cover the `require_variation=False` path in `_validate_score_array()` |
| 4 | Methodological Rigor | 0.92 | 0.94 | Loosen `mean_delta` antisymmetry tolerance from `1e-9` to `1e-7`; review `wilson_ci_width` 0.05 tolerance |
| 5 | Evidence Quality | 0.90 | 0.93 | Add FR-021 AC-x citations to individual test method docstrings in `test_debiasing.py` |
| 6 | Traceability | 0.91 | 0.94 | Add executable FR-019 import-guard test using `ast.parse()` on `stats.py` source to fail at CI time if one-way dependency is violated |

---

## Leniency Bias Check

- [x] Each dimension scored independently before computing weighted composite
- [x] Evidence documented for each score with specific line references and test names
- [x] Uncertain scores resolved downward: Actionability was borderline 0.89/0.90; chose 0.89 because the broad else-branch constitutes a real reduction in failure-signal coverage, not a marginal style issue
- [x] First-draft calibration not applicable (iteration 4); convergence trend noted (iter1=0.876, iter2=0.922, iter3=0.9135, iter4=0.9215 — marginal improvement confirming the iter4 fixes addressed the two highest-priority issues but did not resolve all gaps)
- [x] No dimension scored above 0.95 without documented justification (Internal Consistency at 0.95 is justified by zero contradictions across 11 files with 500+ test methods and full consistency of iter4 factory-to-assertion alignment)
- [x] Composite math verified: 0.1880 + 0.1900 + 0.1840 + 0.1350 + 0.1335 + 0.0910 = 0.9215

---

## Session Context Handoff

```yaml
verdict: REVISE
composite_score: 0.9215
threshold: 0.94
weakest_dimension: Actionability
weakest_score: 0.89
critical_findings_count: 0
iteration: 4
improvement_recommendations:
  - "Replace broad else-branch in test_aggregate_dimension_driver_consistent_with_classification with assert multi.dimension_driver is None for non-REGRESSION paths (test_layer4_pipeline.py lines 749-752)"
  - "Tighten test_compare_versions_improvement_allows_with_warning to assert == ALLOW_WITH_WARNING not != BLOCK (test_stats.py)"
  - "Add test_wilson_score_intervals_all_identical_accepted to cover require_variation=False path (test_stats.py)"
  - "Loosen symmetry tolerance from 1e-9 to 1e-7 in test_compare_versions_symmetry (test_stats_properties.py line 102)"
  - "Add FR-021 citations to individual test method docstrings in test_debiasing.py"
  - "Add AST-based FR-019 import-guard test for stats.py one-way dependency"
```
