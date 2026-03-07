# Quality Score Report: Stream 5C — Test Suite Development (PROJ-036)

## L0 Executive Summary

**Score:** 0.876/1.00 | **Verdict:** REVISE | **Weakest Dimension:** Methodological Rigor (0.86)

**One-line assessment:** The test suite is structurally sound with strong FR traceability and good fixture design, but falls short of the C4 threshold (0.94) due to property-test methodology gaps (early-return vs. `assume()`), a test naming inconsistency that misrepresents IMPROVEMENT exit-code semantics, and a small number of loose assertions that weaken falsifiability; targeted fixes to these three areas are sufficient to reach threshold.

---

## Scoring Context

- **Deliverable:** 10 test files comprising the Stream 5C unified test suite
  - `tests/prompt-regression/unit/test_stats.py`
  - `tests/prompt-regression/unit/test_types.py`
  - `tests/prompt-regression/unit/test_baselines.py`
  - `tests/prompt-regression/unit/test_metamorphic_base.py`
  - `tests/prompt-regression/unit/test_metrics.py`
  - `tests/prompt-regression/unit/test_debiasing.py`
  - `tests/prompt-regression/unit/test_version_keys.py`
  - `tests/prompt-regression/property/test_stats_properties.py`
  - `tests/prompt-regression/property/test_mr_properties.py`
  - `tests/prompt-regression/integration/test_layer4_pipeline.py`
- **Deliverable Type:** Code (Test Suite)
- **Criticality Level:** C4
- **Scoring Strategy:** S-014 (LLM-as-Judge)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Elevated Threshold:** 0.94 (C4 criticality; standard threshold 0.92)
- **Scored:** 2026-03-07T00:00:00Z
- **Iteration:** 1 (first score)

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.876 |
| **Standard Threshold** | 0.92 (H-13) |
| **C4 Elevated Threshold** | 0.94 |
| **Verdict** | REVISE |
| **Strategy Findings Incorporated** | No (standalone scoring) |

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Completeness | 0.20 | 0.87 | 0.174 | All major public APIs tested; `MultiMetricResult` not exercised in test_types.py; git integration functions excluded by documented design |
| Internal Consistency | 0.20 | 0.88 | 0.176 | Consistent patterns across all 10 files; one test name (`test_pipeline_full_mode_improvement_returns_zero`) contradicts its assertion (`exit_code == 2`) |
| Methodological Rigor | 0.20 | 0.86 | 0.172 | Good BDD structure and fixtures throughout; property tests in test_mr_properties.py use early-return instead of `assume()`, violating Hypothesis idiom; loose "or" disjunctions weaken some unit test falsifiability |
| Evidence Quality | 0.15 | 0.88 | 0.132 | Most tests use specific expected values and concrete comparisons; `test_mr001_transform_known_substitution` accepts either original or substitution form, weakening evidence; `test_aggregate_dimension_driver_none_when_no_regression` assertion is underspecified |
| Actionability | 0.15 | 0.90 | 0.135 | Tests are well-structured, independent, and runnable; clear pass/fail semantics; fixtures isolate dependencies cleanly throughout |
| Traceability | 0.10 | 0.87 | 0.087 | FR citations present in module docstrings for all unit/property files; integration test file lacks FR citations in individual test docstrings; some unit tests in test_layer4_pipeline.py lack FR cross-references |
| **TOTAL** | **1.00** | | **0.876** | |

**Arithmetic verification:**
- Completeness: 0.87 × 0.20 = 0.174
- Internal Consistency: 0.88 × 0.20 = 0.176
- Methodological Rigor: 0.86 × 0.20 = 0.172
- Evidence Quality: 0.88 × 0.15 = 0.132
- Actionability: 0.90 × 0.15 = 0.135
- Traceability: 0.87 × 0.10 = 0.087
- **Sum: 0.174 + 0.176 + 0.172 + 0.132 + 0.135 + 0.087 = 0.876**

---

## Detailed Dimension Analysis

### Completeness (0.87/1.00)

**Evidence:**

The suite covers 8 production modules with good breadth. Specific coverage confirmed:

- `test_stats.py` (503 lines): Exercises all 5 public functions (`compare_versions`, `compare_multiple_metrics`, `wilson_score_intervals`, `merge_decision_from_classification`, `bonferroni_correction`) plus all 4 exported constants (`MIN_STATISTICAL_SAMPLE_SIZE`, `QUALITY_PASS_THRESHOLD`, `BONFERRONI_K_FULL_SUITE`, `BONFERRONI_ALPHA_FULL`) and both exception types (`InsufficientSamplesError`, `InvalidScoreArrayError`).
- `test_types.py`: Covers `EvaluationMode`, `RegressionClass`, `RateClass`, `EffectSizeLabel`, `MergeDecision`, `BaselineRecord`, `WilcoxonResult`, `WilsonResult`, `BonferroniConfig`, `RegressionResult`, `ScoreArray` with field presence and immutability tests.
- `test_baselines.py`: Covers `BaselineStore` round-trip persistence, quality gate rejection (mean < 0.92), N < 30 FULL mode rejection, version key validation, double-invalidation idempotency, and directory creation.
- `test_metamorphic_base.py`: Covers `MetamorphicRelation` ABC via `_ConcreteStubMR` plus concrete MR-001 and MR-002 implementations.
- `test_metrics.py`: Covers `JerryGEvalMetric` including `DIMENSION_WEIGHTS` constants (weights sum verified), `score_composite()`, `classify_composite()`, and construction validation.
- `test_debiasing.py`: Covers `DebiasingStrategy` construction, `shuffle_criteria()`, `randomize_candidate_positions()`, `reset_rng()`, and `build_debiased_prompt_section()`.
- `test_version_keys.py`: Covers `VersionKey`, `VersionKeyRegistry`, `BaselineVersionRecord`, `validate_baseline_version_key()`, and private validators.
- `test_layer4_pipeline.py`: Covers `Layer4Pipeline` smoke mode (exit 0/1), full mode (single and multi-metric), Bonferroni routing, `InsufficientSamplesError` propagation, `_exit_code()`, `_aggregate_multi_metric()` including MARGINAL branch, `_persist_report()`, `_emit_gha_outputs()`.

**Gaps:**

1. **`MultiMetricResult` not tested in test_types.py.** The `types.py` module exports `MultiMetricResult` (a non-frozen dataclass with `results: list[RegressionResult]`, `bonferroni: BonferroniConfig`, `dimension_driver: str | None`). No test in `test_types.py` instantiates or verifies `MultiMetricResult` field presence, mutability, or the `dimension_driver` optional field. `MultiMetricResult` is only indirectly exercised through integration tests.
2. **Git integration functions excluded by design.** `version_keys.py` exports `get_current_commit_hash()`, `get_file_last_commit_hash()`, `build_version_key()`, and `compute_prompt_content_hash()`. None are tested. The module's docstring states these require live git subprocess calls, which is a reasonable documented design decision, but there is no stub/mock-based test for the non-git logic paths in `build_version_key()` or error handling in `get_current_commit_hash()`.
3. **`wilcoxon_signed_rank()` not directly tested.** The internal helper is only exercised indirectly through `compare_versions()` in test_stats.py. This is a minor gap because it is an internal function, but it contains the FR-015 implementation.
4. **`_classify_regression()` internal function.** Not directly tested; exercised only through `compare_versions()` output. All classification branches (REGRESSION, QUALITY_FLOOR_BREACH, IMPROVEMENT, MARGINAL, NO_REGRESSION, STRUCTURAL_FAIL) are exercised via integration paths but not isolated.

**Improvement Path:**

Add a `TestMultiMetricResult` class to `test_types.py` covering field presence, mutability, and `dimension_driver` optional handling. Add mock-based tests for the non-git paths in `build_version_key()` (e.g., injecting pre-validated hashes). These two additions would raise Completeness to approximately 0.91.

---

### Internal Consistency (0.88/1.00)

**Evidence:**

The suite maintains consistent patterns across all 10 files:
- Consistent use of `@pytest.mark.parametrize` for multi-case unit tests throughout
- Consistent `_make_scores()`, `_make_scores_varying()`, `_good_scores()`, `_degraded_scores()`, `_improved_scores()` factory patterns in test_stats.py reused coherently
- Consistent `tmp_path` isolation in test_baselines.py
- Consistent `seed=42` determinism pattern in test_debiasing.py
- FR reference format (`FR-0NN`) is consistent across all docstrings that carry such references
- `@settings(deadline=None)` used consistently across all Hypothesis tests to suppress timing issues
- `MagicMock` adapter pattern is consistent throughout test_layer4_pipeline.py

**Inconsistencies:**

1. **Test name contradicts assertion semantics.** `test_pipeline_full_mode_improvement_returns_zero` (line ~342 in test_layer4_pipeline.py) asserts `assert result.exit_code == 2`. An IMPROVEMENT classification produces exit code 2 (ALLOW_WITH_WARNING), not 0 (ALLOW). The test name says "returns_zero" but the implementation correctly asserts exit_code == 2. This is a documentation inconsistency that misrepresents the behavioral contract to any reader parsing test names as executable specifications.

2. **MR-002 minimum sample inconsistency.** `test_mr_properties.py` uses `_mr_002_score_sequence_strategy()` with `min_n=15`, while `test_mr002_insufficient_samples_always_raises` uses `st.integers(min_value=1, max_value=14)`. Cross-referencing against `baselines/store.py` (`MIN_FULL_SAMPLES=30`) and `metamorphic/base.py` suggests MR-002 uses a minimum of 15, which is lower than the FR-014 minimum of 20. This is intentional (MR-002 has a different minimum) but the relationship is not stated explicitly in any test docstring, creating a latent confusion risk.

3. **EvaluationMode defined in two files.** `version_keys.py` defines its own local `EvaluationMode` enum (SMOKE, STANDARD, FULL) that must mirror `jerry.testing.types.EvaluationMode`. `TestEvaluationModeVersionKeys` in `test_version_keys.py` verifies the local copy's values but does not assert that the local enum is structurally equal to the canonical one. A future divergence would not be caught.

**Improvement Path:**

Rename `test_pipeline_full_mode_improvement_returns_zero` to `test_pipeline_full_mode_improvement_returns_allow_with_warning` (exit code 2). Add an assertion in test_version_keys.py that `version_keys.EvaluationMode` member names and values exactly match `jerry.testing.types.EvaluationMode`. These fixes raise Internal Consistency to approximately 0.93.

---

### Methodological Rigor (0.86/1.00)

**Evidence:**

The suite follows a coherent testing methodology:
- BDD-style descriptive test names and docstrings throughout
- H-07 hexagonal architecture respected: integration tests use mock adapters for ports, not real filesystem operations
- Hypothesis property tests in `test_stats_properties.py` correctly use `assume()` to skip degenerate cases (all-zero differences, NaN p-values)
- `_score_array_strategy()` correctly enforces `len(set(scores)) > 1` filter for Wilcoxon variation requirement
- `tmp_path` fixture ensures filesystem isolation in test_baselines.py
- `monkeypatch` used correctly for environment variable injection in test_layer4_pipeline.py
- Exception message content tested (e.g., "19" in str(exc)) rather than just exception type

**Gaps:**

1. **Early-return anti-pattern in property tests.** In `test_mr_properties.py`, several tests use:
   ```python
   if min_n < 20:
       return
   ```
   rather than `assume(min_n >= 20)`. The Hypothesis `assume()` function properly informs the engine to discard and regenerate examples, maintaining statistical coverage distribution. Early return silently passes without testing, making the test vacuously true for a subset of generated inputs without Hypothesis registering the skip. This degrades property coverage in ways that Hypothesis's shrinking and example database mechanisms cannot compensate for.

2. **`_mr_score_sequence_strategy()` sets `min_n=20`** but the test function then checks `if min_n < 20: return`. If the strategy already enforces `min_size=min_n` with `min_n=20`, the early-return branch can never be triggered with the default strategy, making it dead code. For `test_mr001_evaluate_result_type`, the strategy is called with default `min_n=20`, so the guard is unreachable. This is a latent testing gap: the guard suggests the test author is uncertain whether inputs below the minimum can arrive, but they cannot with the current strategy parameters.

3. **Loose disjunction in `test_mr001_transform_known_substitution`.** The test asserts:
   ```python
   assert "You can say that" in result or "Rephrasing:" in result or original in result
   ```
   This is a three-way disjunction where the last branch (`original in result`) accepts the transform returning the unchanged input. If the transform implementation regresses to identity (always returning the original), this test would still pass. A stricter test would assert the result is different from the input when variation is expected.

4. **`dc_replace` MARGINAL branch test coverage.** `test_aggregate_dimension_driver_none_when_no_regression` in test_layer4_pipeline.py uses `dc_replace` to synthesize a MARGINAL classification result. The test asserts `result.dimension_driver is None` but does not verify the aggregated pass counts or the multi-metric structure fully. This is the only test exercising the MARGINAL aggregation branch, and it is underspecified.

**Improvement Path:**

Replace all early-return patterns in `test_mr_properties.py` with `assume()` calls. Strengthen `test_mr001_transform_known_substitution` to assert the result differs from the original in the positive transform case. Add a secondary assertion to the MARGINAL aggregation test covering `len(result.results)`. These changes raise Methodological Rigor to approximately 0.91.

---

### Evidence Quality (0.88/1.00)

**Evidence:**

Most tests use specific, deterministic expected values:
- `test_compare_versions_returns_regression` asserts specific `RegressionClass.REGRESSION`, `MergeDecision.BLOCK`
- `test_wilson_ci_basic_pass_rate` asserts `result.pass_rate == pytest.approx(0.8, abs=0.01)`
- `test_bonferroni_full_suite_constants` asserts exact constant values (`BONFERRONI_K_FULL_SUITE == 13`, `BONFERRONI_ALPHA_FULL == pytest.approx(0.05 / 13)`)
- `test_version_key_from_string_round_trip` verifies exact field equality after round-trip
- Hypothesis property tests verify mathematical invariants (symmetry, bounds) rather than specific output values, which is appropriate for property-based testing
- `test_wilson_ci_bounds` verifies the `ci_lower <= pass_rate <= ci_upper` ordering invariant with `_EPS=1e-10` tolerance, correctly handling scipy floating-point edge cases

**Gaps:**

1. **Loose disjunction weakens falsifiability.** As noted in Methodological Rigor, `test_mr001_transform_known_substitution`'s three-way disjunction including `original in result` means the test cannot detect identity-function regression in the transform.

2. **`test_aggregate_dimension_driver_none_when_no_regression` lacks full evidence chain.** The test verifies `result.dimension_driver is None` for MARGINAL but does not assert the multi-metric result's `results` list structure, making it impossible to verify from the test alone that aggregation was correctly performed.

3. **`test_mr002_evaluate_result_type` asserts only `result.p_value >= 0.0`** (lower bound only). The upper bound (`result.p_value <= 1.0`) is not asserted in this test (it is covered by the property test in `test_stats_properties.py`, but not in the unit test itself). This creates a gap where the unit test alone is insufficient to verify p_value bounds.

4. **`test_debiasing_shuffle_criteria_changes_order`** uses seed=42 and asserts the shuffled list is not equal to the original. This is technically correct but depends on the specific seed producing a different order for the 5-element test list. If the seed happened to produce an identity permutation for this specific list, the test would fail spuriously. The current seed is safe, but the approach is brittle to future list changes.

**Improvement Path:**

Strengthen `test_mr001_transform_known_substitution` to assert `result != prompt` when a substitution is expected. Add upper bound to `test_mr002_evaluate_result_type`'s p_value assertion. Add a `len(result.results)` assertion to the MARGINAL aggregation test. These changes raise Evidence Quality to approximately 0.91.

---

### Actionability (0.90/1.00)

**Evidence:**

The test suite's structure enables clear action on failures:
- Each test file has a well-defined scope matching a single module under test (good modular decomposition)
- `tmp_path` fixture provides automatic cleanup; tests leave no side effects
- `seed=42` in test_debiasing.py ensures deterministic failures that can be reproduced without additional information
- `MagicMock` adapters in test_layer4_pipeline.py allow running integration tests without a real baseline store or report output sink
- `suppress_health_check` and `deadline=None` in all Hypothesis tests prevent flaky CI failures from timing variability
- Exception message assertions (`"19" in str(exc)`) make failures immediately actionable: the developer knows which value was rejected and why
- Pytest class organization groups related tests, making it easy to run subsets with `-k TestClassName`
- No external network calls or I/O dependencies outside of `tmp_path`

**Gaps:**

1. **The `sys.path.insert()` import hack in `test_version_keys.py`** makes the test harder to run in isolation and fragile to directory structure changes. If the test is run from a different working directory, the relative `os.pardir` navigation may fail. A `conftest.py` or package `__init__.py` in the test directory would be more robust and self-documenting.

2. **`test_pipeline_emission_gha_outputs`** tests environment variable setting via `monkeypatch.setenv("GITHUB_OUTPUT", str(tmp_path / "gha_output.txt"))` but does not verify that `_emit_gha_outputs()` produces the correct output format expected by GitHub Actions. The test only verifies that the function runs without exception, not that the emitted format matches the `key=value` GHA output protocol.

**Improvement Path:**

Move the `sys.path.insert()` logic to a `conftest.py` fixture in `tests/prompt-regression/`. Add an assertion in `test_pipeline_emission_gha_outputs` that verifies the emitted file contains the expected `key=value` lines. These changes raise Actionability to approximately 0.93.

---

### Traceability (0.87/1.00)

**Evidence:**

Module-level docstrings in all 10 test files include FR references:
- `test_stats.py`: FR-014, FR-015, FR-016, FR-017, H-20
- `test_types.py`: H-20
- `test_baselines.py`: FR-004, FR-016, FR-020 (inferred from quality gate logic)
- `test_metamorphic_base.py`: FR-010, C-007 (debiasing strategy reference)
- `test_metrics.py`: FR-011, FR-012 (GEval dimensions)
- `test_debiasing.py`: C-007, FR-012
- `test_version_keys.py`: FR-004, OWASP A03:2021, ASVS V5.1
- `test_stats_properties.py`: FR-014, FR-015, FR-016, FR-017, H-20
- `test_mr_properties.py`: FR-010, C
- `test_layer4_pipeline.py`: FR-018 (exit codes), FR-014, FR-015

**Gaps:**

1. **Individual test docstrings in `test_layer4_pipeline.py` do not cite specific FRs.** The module-level docstring cites FR-018 and FR-014, but individual test functions like `test_pipeline_smoke_mode_no_regression`, `test_pipeline_full_mode_single_metric_regression`, etc. do not reference which requirement they validate. At C4 criticality, per-test traceability to requirements provides stronger V&V evidence than module-level citation alone.

2. **`test_baselines.py` individual tests do not cite FRs.** The module docstring is absent; individual tests reference behavior (e.g., "FULL mode requires run_count >= 30") but do not cite FR-020 (baseline quality gate) explicitly. Cross-referencing against `baselines/store.py` shows `QUALITY_PASS_THRESHOLD = 0.92` and `MIN_FULL_SAMPLES = 30` are the governing constants, but no FR reference appears in the test file.

3. **`test_mr_properties.py` module docstring references "behavioral-contracts.md Section C"** but does not provide a repository-relative path. This trace is incomplete: a reader cannot locate the contract document without additional search.

4. **No explicit traceability to ADR-PROJ036-XXX.** For a C4 deliverable, the test suite should ideally trace back not just to FRs but to the architectural decisions (ADRs) that shaped the design. None of the test files reference design decisions.

**Improvement Path:**

Add FR citations to individual test docstrings in `test_layer4_pipeline.py` (FR-018 for exit code tests, FR-014 for InsufficientSamplesError tests). Add a module docstring to `test_baselines.py` citing FR-020. Provide a full repository-relative path for `behavioral-contracts.md` in `test_mr_properties.py`. These changes raise Traceability to approximately 0.91.

---

## Improvement Recommendations (Priority Ordered)

| Priority | Dimension | Current | Target | Recommendation |
|----------|-----------|---------|--------|----------------|
| 1 | Methodological Rigor | 0.86 | 0.91 | Replace all early-return patterns in `test_mr_properties.py` with `assume()` calls. Replace `if min_n < 20: return` with `assume(len(original_scores[:min_n]) >= 20)` in the 3 affected test functions. Strengthen `test_mr001_transform_known_substitution` to assert `result != prompt`. |
| 2 | Internal Consistency | 0.88 | 0.93 | Rename `test_pipeline_full_mode_improvement_returns_zero` to `test_pipeline_full_mode_improvement_returns_allow_with_warning`. Add an assertion in `test_version_keys.py` that verifies the local `EvaluationMode` enum members and values exactly match `jerry.testing.types.EvaluationMode`. |
| 3 | Completeness | 0.87 | 0.91 | Add `TestMultiMetricResult` class to `test_types.py` covering instantiation, field presence (`results`, `bonferroni`, `dimension_driver`), mutability (not frozen), and `dimension_driver=None` default. Add mock-based test for `build_version_key()` injecting pre-validated hash strings to test non-git paths. |
| 4 | Traceability | 0.87 | 0.91 | Add per-test FR citations in `test_layer4_pipeline.py` docstrings (FR-018 for exit code tests, FR-014 for InsufficientSamplesError tests). Add module docstring to `test_baselines.py` citing FR-020. Provide full repo-relative path for `behavioral-contracts.md` reference in `test_mr_properties.py`. |
| 5 | Evidence Quality | 0.88 | 0.91 | Strengthen `test_mr001_transform_known_substitution`: assert result differs from input. Add upper bound assertion to `test_mr002_evaluate_result_type` for p_value. Add `len(result.results)` assertion to MARGINAL aggregation test. |
| 6 | Actionability | 0.90 | 0.93 | Move `sys.path.insert()` in `test_version_keys.py` to a shared `conftest.py`. Add file content assertions to `test_pipeline_emission_gha_outputs` verifying the `key=value` format expected by GitHub Actions. |

---

## Leniency Bias Check

- [x] Each dimension scored independently before computing weighted composite
- [x] Evidence documented for each score with specific file/line references
- [x] Uncertain scores resolved downward (Methodological Rigor at 0.86 despite generally sound approach, due to early-return pattern being a meaningful methodology gap; Traceability at 0.87 despite FR references being present at module level, because per-test traceability is absent in the integration test file)
- [x] First-draft calibration considered: this is Iteration 1; score of 0.876 is consistent with the 0.70-0.84 "significant gaps" band but sits at the upper end reflecting a strong foundation with specific fixable issues
- [x] No dimension scored above 0.92; Actionability (0.90) is the highest and is justified by the fixture isolation, seed determinism, and MagicMock adapter patterns
- [x] Weighted composite verified by independent arithmetic: 0.174 + 0.176 + 0.172 + 0.132 + 0.135 + 0.087 = 0.876

---

## Session Context Handoff

```yaml
verdict: REVISE
composite_score: 0.876
threshold: 0.94
weakest_dimension: Methodological Rigor
weakest_score: 0.86
critical_findings_count: 0
iteration: 1
improvement_recommendations:
  - "Replace early-return patterns in test_mr_properties.py with assume() calls (Methodological Rigor)"
  - "Rename test_pipeline_full_mode_improvement_returns_zero to match actual behavior (Internal Consistency)"
  - "Add TestMultiMetricResult class to test_types.py (Completeness)"
  - "Add per-test FR citations to test_layer4_pipeline.py docstrings (Traceability)"
  - "Strengthen test_mr001_transform_known_substitution assertion chain (Evidence Quality)"
  - "Move sys.path.insert() to conftest.py; add GHA output format assertions (Actionability)"
```
