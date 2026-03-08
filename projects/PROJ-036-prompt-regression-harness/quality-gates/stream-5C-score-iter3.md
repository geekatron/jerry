# Quality Score Report: Stream 5C Test Suite — Four-Layer Composite Test Harness (Iteration 3)

## L0 Executive Summary

**Score:** 0.9135/1.00 | **Verdict:** REVISE | **Weakest Dimension:** Evidence Quality (0.88)
**One-line assessment:** The suite is near-threshold with strong traceability and actionability, but the iter3 evidence-quality fix was incomplete — five `hasattr()` checks in `TestMultiMetricResult.test_multi_metric_result_fields_present` were not converted to value assertions, leaving a residual gap that holds the composite below the 0.94 C4 threshold.

---

## Scoring Context

- **Deliverable:** 11 test files under `tests/prompt-regression/` (conftest, 7 unit, 2 property, 1 integration)
- **Deliverable Type:** Code (test suite)
- **Criticality Level:** C4
- **Scoring Strategy:** S-014 (LLM-as-Judge)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Quality Threshold (user-specified):** 0.94 (C4 — above standard H-13 threshold of 0.92)
- **Prior Scores:** iter1=0.876, iter2=0.922
- **Scored:** 2026-03-07T00:00:00Z

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.9135 |
| **Threshold** | 0.94 (C4, user-specified) |
| **Verdict** | REVISE |
| **Strategy Findings Incorporated** | No (scored directly from deliverable files) |

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Completeness | 0.20 | 0.90 | 0.1800 | All 7 source modules covered; minor gap: 5 `hasattr()` presence checks in TestMultiMetricResult not converted to value assertions |
| Internal Consistency | 0.20 | 0.93 | 0.1860 | RegressionClass→MergeDecision mappings tested independently in unit, property, and integration layers with no contradictions |
| Methodological Rigor | 0.20 | 0.91 | 0.1820 | Hypothesis property tests use `assume()`, `deadline=None`, and `suppress_health_check` correctly; 0.05 absolute tolerance in width-decreases test is an improvement but still admits edge violations |
| Evidence Quality | 0.15 | 0.88 | 0.1320 | iter3 fixed WilcoxonResult, MRResult, and score_composite assertions; TestMultiMetricResult.test_multi_metric_result_fields_present retains 5 `hasattr()` checks — existence confirmed, values not asserted |
| Actionability | 0.15 | 0.93 | 0.1395 | conftest.py isolates sys.path; tmp_path fixtures in test_baselines.py; mock injection via hexagonal ports in test_layer4_pipeline.py; f-string diagnostics in all property test assertions |
| Traceability | 0.10 | 0.94 | 0.0940 | Repo-relative `behavioral-contracts.md` paths added in iter3 to test_metamorphic_base.py and test_debiasing.py; FR-004 through FR-021, OWASP, ASVS, S-014 all cited with section precision |
| **TOTAL** | **1.00** | | **0.9135** | |

---

## Detailed Dimension Analysis

### Completeness (0.90/1.00)

**Evidence:**

All seven source modules under `jerry.testing` have dedicated test files:
- `jerry.testing.stats` → `test_stats.py` (503 lines, 6 test classes covering compare_versions, compare_multiple_metrics, wilson_score_intervals, merge_decision_from_classification, bonferroni_correction, and named constants)
- `jerry.testing.types` → `test_types.py` (479 lines, covering all 14 imported types including WilcoxonResult, WilsonResult, BonferroniConfig, RegressionResult, MultiMetricResult)
- `jerry.testing.baselines.store` → `test_baselines.py` (405 lines, covering store/retrieve/audit/invalidate with edge cases)
- `jerry.testing.metamorphic.base` → `test_metamorphic_base.py` (383 lines, covering ABC, concrete MR-001, MR-002)
- `jerry.testing.evaluation.metrics` → `test_metrics.py` (316 lines, covering DIMENSION_WEIGHTS, classify_composite, score_composite, JerryGEvalMetric construction)
- `jerry.testing.evaluation.debiasing` → `test_debiasing.py` (285 lines, covering construction, shuffle_criteria, randomize_candidate_positions, reset_rng, build_debiased_prompt_section)
- `tests/prompt-regression/version_keys.py` → `test_version_keys.py` (478 lines, covering VersionKey, VersionKeyRegistry, BaselineVersionRecord, validate_baseline_version_key)
- Property tests: `test_stats_properties.py` and `test_mr_properties.py` cover invariants
- Integration: `test_layer4_pipeline.py` covers Layer4Pipeline end-to-end including smoke mode, full mode, error propagation, GHA output, file persistence, lazy import, and multi-metric aggregation including the MARGINAL branch

FR coverage: FR-004, FR-005, FR-007, FR-010, FR-014 through FR-021 all referenced.

**Gaps:**

`TestMultiMetricResult.test_multi_metric_result_fields_present` (test_types.py lines 432-436) uses five `hasattr()` checks (`per_metric`, `bonferroni`, `dimension_driver`, `overall_classification`, `merge_decision`) rather than asserting actual values. The iter3 fix description stated "hasattr() checks replaced with direct value assertions in TestWilcoxonResult and TestMRResult" — this was correctly applied to those two classes but NOT extended to TestMultiMetricResult, which retains the weaker assertion pattern.

No tests for FR-008 (scoring result schema validation), FR-009 (LLM evaluation pipeline), FR-011 through FR-013 (MR-003 through MR-005). These are not in scope for the 5C stream but represent known gaps if the stream expands.

**Improvement Path:**

Convert the five `hasattr()` checks in `test_multi_metric_result_fields_present` to direct value assertions using the `_make_multi_metric_result()` factory already present in the class. For example: `assert result.per_metric == {}`, `assert isinstance(result.bonferroni, BonferroniConfig)`, `assert result.dimension_driver == "completeness"`, etc.

---

### Internal Consistency (0.93/1.00)

**Evidence:**

The RegressionClass-to-MergeDecision mapping is tested at three independent layers, all consistent:
1. Unit: `TestMergeDecisionFromClassification` (test_stats.py lines 432-464) — each of the six classifications asserted individually with exact expected decisions.
2. Property: `test_merge_decision_consistent_with_classification` (test_stats_properties.py lines 218-255) — Hypothesis verifies the mapping holds for all valid input pairs (max_examples=30).
3. Integration: `TestExitCodeMapping` (test_layer4_pipeline.py lines 597-626) — BLOCK→1, ALLOW_WITH_WARNING→2, ALLOW→0 confirmed with static `_exit_code()` method.

The IMPROVEMENT-to-ALLOW_WITH_WARNING mapping is correctly handled: `test_merge_decision_improvement_warns` (unit) and `test_pipeline_full_mode_improvement_returns_allow_with_warning` (integration) both assert ALLOW_WITH_WARNING. The inline comment in the integration test (lines 343-363) explicitly explains why IMPROVEMENT produces exit code 2, preventing future confusion.

No contradictions found between the three enforcement layers.

**Gaps:**

`test_aggregate_dimension_driver_none_when_no_regression` (test_layer4_pipeline.py lines 731-757) uses a score pair `(self._SCORES_A_BASELINE, self._SCORES_B_REGRESSED)` that produces REGRESSION (not NO_REGRESSION), making the test name misleading. The test body accommodates both outcomes with an if-else, which is intentionally permissive and technically correct, but the test name creates a minor documentation inconsistency. This is not a behavioral contradiction.

**Improvement Path:**

Rename `test_aggregate_dimension_driver_none_when_no_regression` to `test_aggregate_dimension_driver_consistent_with_classification` to reflect its actual permissive assertion pattern, and consider using the `_SCORES_PASS` pair (which reliably produces NO_REGRESSION) to test the None case deterministically.

---

### Methodological Rigor (0.91/1.00)

**Evidence:**

The iter3 fix to `test_wilson_ci_width_decreases_with_n` replaces the `1.1x multiplier` with `small_result.ci_width + 0.05`. This is methodologically superior: the original 1.1x multiplier was a relative tolerance that could allow large absolute increases for small CI widths, while the absolute 0.05 tolerance is proportional to the score range [0,1] and is better-justified as "not meaningfully increasing."

Hypothesis configuration is consistently correct:
- `assume(scores_a != scores_b)` and `assume(any(d != 0.0 for d in diffs))` in the symmetry test correctly filter degenerate Wilcoxon inputs without silently passing them.
- `assume(min_n >= 20)` in the MR property tests is used correctly instead of early return (as noted in the inline comments at lines 159-161, 196-198, 239-241 of test_mr_properties.py).
- `suppress_health_check=[HealthCheck.too_slow, HealthCheck.filter_too_much]` and `deadline=None` prevent Hypothesis infrastructure failures.
- `max_examples` settings (20-50) are appropriately tiered by test complexity.

Integration test methodology is sound: mock injection of `BaselinePersistencePort` and `ReportOutputPort` via `MagicMock` correctly tests pipeline orchestration without filesystem or LLM dependencies. The `_make_comparison_report` and `_make_smoke_report` factories make test setup explicit.

`TestAggregateMultiMetric` uses `compare_versions()` to produce real `RegressionResult` objects rather than stub construction, which correctly exercises the real classification logic in the aggregation tests.

**Gaps:**

`test_wilson_ci_width_decreases_with_n`: the 0.05 tolerance is better than 1.1x but still permits cases where adding 10-30 extra scores (with pass_rates drawn from [0.85, 0.99] but potentially different from the base scores) produces a Wilson CI that is up to 0.05 wider. For example, if base_scores all pass (pass_rate=1.0, CI width ≈ 0 for N=20) and extra_scores include some below 0.92 (pass_rate drops, CI widens), the assertion would still pass within 0.05. This is a known limitation explicitly documented in the assertion message. It passes the spirit of the test while being aware of the edge case.

**Improvement Path:**

To make `test_wilson_ci_width_decreases_with_n` a strict monotone property, use `extra_scores` drawn from the same distribution as `base_scores` (not from a separate strategy). This would eliminate the pass-rate shift that drives edge-case CI widening. Alternatively, note the current design is acceptable if the 0.05 tolerance is team-accepted.

---

### Evidence Quality (0.88/1.00)

**Evidence:**

The iter3 fix applied `pytest.approx()` to:
- `TestWilcoxonResult.test_wilcoxon_result_fields` (test_types.py lines 265-273): all eight numeric fields now use `pytest.approx()` with exact expected values.
- `TestMRResult.test_mr_result_mean_delta_correct` (test_metamorphic_base.py lines 173-175): uses `pytest.approx(abs(result.mean_original - result.mean_transformed))`.
- `TestScoreComposite.test_score_composite_in_range` (test_metrics.py lines 215-237): now computes exact expected value `(0.75*0.20 + 0.90*0.20 + 0.85*0.20 + 0.80*0.15 + 0.70*0.15 + 0.95*0.10) / 1.00 = 0.820` and asserts `score == pytest.approx(expected)`.

Error message content assertions are specific and informative:
- `assert "19" in str(exc_info.value)` and `assert "Smoke mode" in str(exc_info.value)` in test_stats.py TestCompareVersionsInsufficientSamples.
- `assert "Wilcoxon requires N >= 20" in error_msg` and `assert "Smoke mode" in error_msg` for the format test.
- `assert "quality gate" in str(exc_info.value).lower() or "0.92" in str(exc_info.value)` in test_baselines.py.

**Gaps:**

`TestMultiMetricResult.test_multi_metric_result_fields_present` (test_types.py lines 429-436):
```python
assert hasattr(result, "per_metric")
assert hasattr(result, "bonferroni")
assert hasattr(result, "dimension_driver")
assert hasattr(result, "overall_classification")
assert hasattr(result, "merge_decision")
```
These five assertions confirm that the attributes exist on the type but do not confirm that the values match what was passed to `_make_multi_metric_result()`. Concretely: if `MultiMetricResult` were refactored to drop `per_metric` but add it as a property that returns an empty dict from a different internal field, all five `hasattr()` checks would pass while the structural contract is broken. The `_make_multi_metric_result()` factory provides concrete values (`per_metric={}`, `dimension_driver="completeness"`, etc.) that could be used for direct assertions.

This gap is all the more notable because iter3's stated objective was to fix exactly this class of issue (hasattr → value assertions) and it was fully applied to TestWilcoxonResult and TestMRResult but missed TestMultiMetricResult.

**Improvement Path:**

Replace the five `hasattr()` checks with:
```python
assert result.per_metric == {}
assert isinstance(result.bonferroni, BonferroniConfig)
assert result.dimension_driver == "completeness"  # per _make_multi_metric_result factory
assert result.overall_classification == RegressionClass.NO_REGRESSION
assert result.merge_decision == MergeDecision.ALLOW
```

---

### Actionability (0.93/1.00)

**Evidence:**

`conftest.py` correctly centralizes sys.path manipulation (iter2 fix, preserved in iter3):
```python
_PR_TEST_DIR = os.path.dirname(__file__)
if _PR_TEST_DIR not in sys.path:
    sys.path.insert(0, _PR_TEST_DIR)
```
The docstring references FR-004 and explains the rationale clearly.

Test isolation is strong throughout:
- `tmp_path` fixture used in `test_baselines.py` for every BaselineStore test (all 8 tests in TestBaselineStoreStore, TestBaselineStoreRetrieve, TestBaselineStoreAudit, TestBaselineStoreInvalidate).
- Mock injection in `test_layer4_pipeline.py` via `mock_store` and `mock_generator` fixtures prevents real I/O.
- `monkeypatch.setenv("GITHUB_OUTPUT", ...)` in TestEmitGhaOutputs correctly isolates env var manipulation.

Diagnostic messages in property tests include f-string context:
```
f"Large N ({len(base_scores + extra_scores)}) CI width {large_result.ci_width:.4f} exceeds small N ({len(base_scores)}) CI width {small_result.ci_width:.4f} by more than 0.05"
```

The `TestBuildVersionKeyMocked` class correctly uses `monkeypatch.setattr` on module-level functions rather than on instances, which is the correct approach for testing git subprocess calls without invoking git.

The `_ConcreteStubMR` in test_metamorphic_base.py provides a minimal but complete concrete ABC implementation that directly tests `_validate_inputs()`, `_mean()`, and `_std()` without requiring a full MR implementation.

**Gaps:**

`test_aggregate_dimension_driver_none_when_no_regression` (layer4 line 731) is difficult to run in isolation and understand without reading the comments — the test name suggests NO_REGRESSION but uses REGRESSED score pairs. This is a minor actionability issue for future maintainers.

**Improvement Path:**

Rename the test and use `_SCORES_PASS` pairs for the NO_REGRESSION branch to make the test self-explanatory.

---

### Traceability (0.94/1.00)

**Evidence:**

The iter3 fix added repo-relative `behavioral-contracts.md` paths:
- `test_metamorphic_base.py` lines 15-16: `behavioral-contracts.md Section C (projects/PROJ-036-prompt-regression-harness/contracts/behavioral-contracts.md)`
- `test_debiasing.py` lines 14-15: `behavioral-contracts.md §B.5: Score stability bounds (projects/PROJ-036-prompt-regression-harness/contracts/behavioral-contracts.md)`

FR references are precise and bidirectional across all 11 files:
- `test_stats.py`: FR-014 (N>=20), FR-015 (Wilcoxon), FR-016 (Wilson), FR-017 (Bonferroni k=13), H-20
- `test_types.py`: H-07, H-20
- `test_baselines.py`: FR-004, FR-014, FR-020 (with inline FR-020 acceptance criterion quote)
- `test_metamorphic_base.py`: FR-010, behavioral-contracts.md Section C
- `test_metrics.py`: FR-007, quality-enforcement.md S-014, H-20
- `test_debiasing.py`: FR-021, behavioral-contracts.md §B.5
- `test_version_keys.py`: FR-004 AC-1..AC-3, OWASP A03:2021, ASVS V5.1, H-20
- `test_stats_properties.py`: FR-014 through FR-017, H-20
- `test_mr_properties.py`: FR-010, behavioral-contracts.md Section C
- `test_layer4_pipeline.py`: FR-018, FR-019, behavioral-contracts.md Section D.6, H-20

Individual test docstrings cite specific FR numbers: `"""FR-018: BLOCK merge recommendation maps to exit code 1 (CI/CD gate failure)."""`

**Gaps:**

`conftest.py` references FR-004 in its docstring but does not link to `behavioral-contracts.md`. This is acceptable given conftest's narrow scope (sys.path setup).

The `test_layer4_pipeline.py::TestAggregateMultiMetric` class comment references "lines 373-378" and "lines 102-104" in layer4_stats.py — these are implementation line numbers that will drift as code changes, creating brittle traceability.

**Improvement Path:**

Replace implementation-file line number references in test comments with function/method names (e.g., "lazy import branch in `Layer4Pipeline.__init__`") which are stable across refactors.

---

## Improvement Recommendations (Priority Ordered)

| Priority | Dimension | Current | Target | Recommendation |
|----------|-----------|---------|--------|----------------|
| 1 | Evidence Quality | 0.88 | 0.93 | Convert 5 `hasattr()` checks in `TestMultiMetricResult.test_multi_metric_result_fields_present` (test_types.py lines 432-436) to direct value assertions using the `_make_multi_metric_result()` factory values (`per_metric=={}`, `overall_classification==RegressionClass.NO_REGRESSION`, `merge_decision==MergeDecision.ALLOW`, `dimension_driver=="completeness"`, `isinstance(bonferroni, BonferroniConfig)`) |
| 2 | Completeness | 0.90 | 0.93 | The Evidence Quality fix in P1 also closes this gap since the incomplete assertions reduce the effective completeness of TestMultiMetricResult's contract coverage |
| 3 | Internal Consistency | 0.93 | 0.95 | Rename `test_aggregate_dimension_driver_none_when_no_regression` and use `_SCORES_PASS` pairs to test the NO_REGRESSION→dimension_driver=None case deterministically, eliminating the if-else permissive assertion |
| 4 | Methodological Rigor | 0.91 | 0.93 | For `test_wilson_ci_width_decreases_with_n`, draw `extra_scores` from the same pass-rate distribution as `base_scores` to eliminate the pass-rate-shift edge case; or document explicitly in the test class that 0.05 is the team-accepted tolerance |
| 5 | Traceability | 0.94 | 0.96 | Replace implementation line number references (e.g., "lines 102-104 in layer4_stats.py") with stable function/method name references |

---

## Leniency Bias Check

- [x] Each dimension scored independently before computing composite
- [x] Evidence documented for each score with specific file/line references
- [x] Uncertain scores resolved downward: Evidence Quality held at 0.88 (not 0.90) because the 5 hasattr residuals are a direct failure of the stated iter3 fix; Methodological Rigor held at 0.91 (not 0.93) because the 0.05 tolerance is a real edge case even if improved
- [x] First-draft calibration not applicable (iter3 of a mature test suite); calibration anchors applied: 0.92 = "strong work with minor refinements"; 0.85 = "strong work with clear improvement areas"
- [x] No dimension scored above 0.95 without exceptional evidence (Traceability at 0.94 is the maximum and is supported by explicit FR citations and repo-relative contract paths across all 11 files)

---

## Session Context (Handoff Schema)

```yaml
verdict: REVISE
composite_score: 0.9135
threshold: 0.94
weakest_dimension: evidence_quality
weakest_score: 0.88
critical_findings_count: 0
iteration: 3
improvement_recommendations:
  - "Convert 5 hasattr() checks in TestMultiMetricResult.test_multi_metric_result_fields_present to value assertions (test_types.py lines 432-436)"
  - "Rename test_aggregate_dimension_driver_none_when_no_regression and use _SCORES_PASS for deterministic NO_REGRESSION assertion"
  - "Document or constrain test_wilson_ci_width_decreases_with_n extra_scores distribution"
  - "Replace implementation line number references with function name references in test_layer4_pipeline.py comments"
```

---

*Score Report Version: 1.0.0*
*Agent: adv-scorer*
*Strategy: S-014 (LLM-as-Judge)*
*SSOT: `.context/rules/quality-enforcement.md`*
*Scored: 2026-03-07*
