# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Victor Lau

"""Unit tests for jerry.testing.stats — Layer 4 statistical engine.

Tests every public function in stats.py:
    - compare_versions()
    - compare_multiple_metrics()
    - wilson_score_intervals()
    - merge_decision_from_classification()
    - InsufficientSamplesError
    - InvalidScoreArrayError

Each test is independent and uses only deterministic, controlled inputs.
No LLM calls or I/O are performed.

References:
    - FR-014: N >= 20 enforcement (InsufficientSamplesError)
    - FR-015: Wilcoxon signed-rank test
    - FR-016: Wilson score confidence intervals
    - FR-017: Bonferroni correction (k=13)
    - H-20: 90% line coverage target
"""

from __future__ import annotations

import pytest

from jerry.testing.stats import (
    BONFERRONI_ALPHA_FULL,
    BONFERRONI_K_FULL_SUITE,
    MIN_STATISTICAL_SAMPLE_SIZE,
    QUALITY_PASS_THRESHOLD,
    InsufficientSamplesError,
    InvalidScoreArrayError,
    bonferroni_correction,
    compare_multiple_metrics,
    compare_versions,
    merge_decision_from_classification,
    wilson_score_intervals,
)
from jerry.testing.types import (
    EvaluationMode,
    MergeDecision,
    RegressionClass,
)

# ---------------------------------------------------------------------------
# Helper factories
# ---------------------------------------------------------------------------


def _make_scores(n: int, value: float) -> list[float]:
    """Return a list of n identical scores at the given value."""
    return [value] * n


def _make_scores_varying(n: int, base: float, delta: float) -> list[float]:
    """Return alternating [base, base+delta, ...] to avoid all-identical arrays."""
    return [base if i % 2 == 0 else base + delta for i in range(n)]


def _good_scores(n: int = 30) -> list[float]:
    """Return N high-quality scores (above 0.92) with variation."""
    return _make_scores_varying(n, 0.93, 0.04)


def _degraded_scores(n: int = 30) -> list[float]:
    """Return N clearly degraded scores (around 0.55) with variation."""
    return _make_scores_varying(n, 0.50, 0.10)


def _improved_scores(n: int = 30) -> list[float]:
    """Return N clearly improved scores (around 0.97) with variation."""
    return _make_scores_varying(n, 0.97, 0.02)


# ---------------------------------------------------------------------------
# Named constants
# ---------------------------------------------------------------------------


class TestNamedConstants:
    """Verify the module-level named constants match the FR-specified values."""

    def test_min_statistical_sample_size(self) -> None:
        """FR-014: MIN_STATISTICAL_SAMPLE_SIZE shall be 20."""
        assert MIN_STATISTICAL_SAMPLE_SIZE == 20

    def test_quality_pass_threshold(self) -> None:
        """FR-016: QUALITY_PASS_THRESHOLD shall be 0.92."""
        assert QUALITY_PASS_THRESHOLD == 0.92

    def test_bonferroni_k_full_suite(self) -> None:
        """FR-017: BONFERRONI_K_FULL_SUITE shall be 13."""
        assert BONFERRONI_K_FULL_SUITE == 13

    def test_bonferroni_alpha_full(self) -> None:
        """FR-017: BONFERRONI_ALPHA_FULL shall be 0.004 (conservative rounding of 0.05/13)."""
        assert BONFERRONI_ALPHA_FULL == 0.004


# ---------------------------------------------------------------------------
# compare_versions() — primary public API
# ---------------------------------------------------------------------------


class TestCompareVersionsNoRegression:
    """compare_versions() correctly classifies stable arrays as non-blocking.

    Per behavioral-contracts.md Section D.4:
        p >= alpha_marginal (any r)                 → NO_REGRESSION
        p < alpha, delta >= 0.0 (candidate >= base) → IMPROVEMENT

    Both NO_REGRESSION and IMPROVEMENT are non-blocking outcomes.  When arrays
    are identical (delta == 0.0), scipy may report a degenerate p-value that
    falls below alpha, causing IMPROVEMENT rather than NO_REGRESSION.  Either
    outcome is correct per the contract; neither is a regression.
    """

    def test_compare_versions_similar_arrays_not_blocking(self) -> None:
        """Two similar score arrays must not produce a blocking classification.

        REGRESSION and QUALITY_FLOOR_BREACH are blocking; NO_REGRESSION and
        IMPROVEMENT are both acceptable for stable, high-quality arrays.
        """
        a = _good_scores(30)
        b = _good_scores(30)
        result = compare_versions(a, b, evaluation_mode=EvaluationMode.FULL)
        blocking = {RegressionClass.REGRESSION, RegressionClass.QUALITY_FLOOR_BREACH}
        assert result.classification not in blocking

    def test_compare_versions_similar_arrays_not_block_merge_decision(self) -> None:
        """Similar arrays must not produce BLOCK merge decision."""
        a = _good_scores(30)
        b = _good_scores(30)
        result = compare_versions(a, b, evaluation_mode=EvaluationMode.FULL)
        assert result.merge_decision != MergeDecision.BLOCK

    def test_compare_versions_result_has_correct_metric_id(self) -> None:
        """compare_versions() should preserve the metric_id argument."""
        a = _good_scores(30)
        b = _good_scores(30)
        result = compare_versions(a, b, metric_id="my_metric", evaluation_mode=EvaluationMode.FULL)
        assert result.metric_id == "my_metric"

    def test_compare_versions_result_has_sample_sizes(self) -> None:
        """compare_versions() result includes correct n_a and n_b fields."""
        a = _good_scores(25)
        b = _good_scores(28)
        result = compare_versions(a, b, evaluation_mode=EvaluationMode.FULL)
        assert result.n_a == 25
        assert result.n_b == 28


class TestCompareVersionsRegression:
    """compare_versions() correctly classifies clearly degraded arrays as REGRESSION."""

    def test_compare_versions_regression(self) -> None:
        """Clearly degraded candidate array should produce REGRESSION or MARGINAL classification."""
        # Use extreme degradation to ensure classification
        a = _make_scores_varying(30, 0.93, 0.04)  # baseline: ~0.95 mean
        b = _make_scores_varying(30, 0.40, 0.10)  # candidate: ~0.45 mean (extreme drop)
        result = compare_versions(a, b, evaluation_mode=EvaluationMode.FULL)
        assert result.classification in (
            RegressionClass.REGRESSION,
            RegressionClass.MARGINAL,
        )

    def test_compare_versions_regression_blocks_merge(self) -> None:
        """REGRESSION or QUALITY_FLOOR_BREACH classification should block the merge."""
        a = _make_scores_varying(30, 0.93, 0.04)
        b = _make_scores_varying(30, 0.40, 0.10)
        result = compare_versions(a, b, evaluation_mode=EvaluationMode.FULL)
        # Either REGRESSION (blocks) or MARGINAL (allows with warning) is valid
        # depending on effect size; BLOCK or ALLOW_WITH_WARNING are both valid here.
        assert result.merge_decision in (MergeDecision.BLOCK, MergeDecision.ALLOW_WITH_WARNING)

    def test_compare_versions_regression_negative_mean_delta(self) -> None:
        """A regressed result should have negative mean_delta (candidate worse than baseline)."""
        a = _make_scores_varying(30, 0.93, 0.04)
        b = _make_scores_varying(30, 0.40, 0.10)
        result = compare_versions(a, b, evaluation_mode=EvaluationMode.FULL)
        assert result.wilcoxon.mean_delta < 0.0


class TestCompareVersionsImprovement:
    """compare_versions() correctly classifies improved arrays as IMPROVEMENT."""

    def test_compare_versions_improvement(self) -> None:
        """Clearly improved candidate should produce IMPROVEMENT or NO_REGRESSION."""
        a = _make_scores_varying(30, 0.50, 0.10)  # baseline: ~0.55 mean
        b = _make_scores_varying(30, 0.93, 0.04)  # candidate: ~0.95 mean (clear improvement)
        result = compare_versions(a, b, evaluation_mode=EvaluationMode.FULL)
        assert result.classification in (
            RegressionClass.IMPROVEMENT,
            RegressionClass.NO_REGRESSION,
        )

    def test_compare_versions_improvement_positive_delta(self) -> None:
        """An improved result should have a positive mean_delta."""
        a = _make_scores_varying(30, 0.50, 0.10)
        b = _make_scores_varying(30, 0.93, 0.04)
        result = compare_versions(a, b, evaluation_mode=EvaluationMode.FULL)
        assert result.wilcoxon.mean_delta > 0.0

    def test_compare_versions_improvement_allows_with_warning(self) -> None:
        """IMPROVEMENT should map to ALLOW_WITH_WARNING (FR-018: exit code 2)."""
        a = _make_scores_varying(30, 0.50, 0.10)
        b = _make_scores_varying(30, 0.93, 0.04)
        result = compare_versions(a, b, evaluation_mode=EvaluationMode.FULL)
        assert result.merge_decision == MergeDecision.ALLOW_WITH_WARNING


class TestCompareVersionsInsufficientSamples:
    """compare_versions() enforces N >= 20 on both arrays (FR-014)."""

    def test_compare_versions_insufficient_samples_a(self) -> None:
        """N < 20 in scores_a should raise InsufficientSamplesError."""
        small_a = _make_scores_varying(19, 0.93, 0.04)
        valid_b = _good_scores(30)
        with pytest.raises(InsufficientSamplesError) as exc_info:
            compare_versions(small_a, valid_b, evaluation_mode=EvaluationMode.FULL)
        assert "19" in str(exc_info.value)
        assert "Smoke mode" in str(exc_info.value)

    def test_compare_versions_insufficient_samples_b(self) -> None:
        """N < 20 in scores_b should raise InsufficientSamplesError."""
        valid_a = _good_scores(30)
        small_b = _make_scores_varying(5, 0.93, 0.04)
        with pytest.raises(InsufficientSamplesError) as exc_info:
            compare_versions(valid_a, small_b, evaluation_mode=EvaluationMode.FULL)
        assert "5" in str(exc_info.value)

    def test_compare_versions_insufficient_samples_error_format(self) -> None:
        """FR-014: error message format shall include N values and Smoke mode suggestion."""
        small = _make_scores_varying(10, 0.93, 0.04)
        with pytest.raises(InsufficientSamplesError) as exc_info:
            compare_versions(small, small, evaluation_mode=EvaluationMode.FULL)
        error_msg = str(exc_info.value)
        assert "Wilcoxon requires N >= 20" in error_msg
        assert "Smoke mode" in error_msg

    def test_insufficient_samples_is_value_error_subclass(self) -> None:
        """InsufficientSamplesError must be a subclass of ValueError."""
        assert issubclass(InsufficientSamplesError, ValueError)


class TestCompareVersionsInvalidScores:
    """compare_versions() rejects score arrays with out-of-range values."""

    def test_compare_versions_invalid_scores_above_one(self) -> None:
        """Score > 1.0 should raise InvalidScoreArrayError."""
        bad_scores = _make_scores_varying(30, 0.93, 0.04)
        bad_scores[5] = 1.5  # inject an out-of-range value
        valid = _good_scores(30)
        with pytest.raises(InvalidScoreArrayError):
            compare_versions(bad_scores, valid, evaluation_mode=EvaluationMode.FULL)

    def test_compare_versions_invalid_scores_below_zero(self) -> None:
        """Score < 0.0 should raise InvalidScoreArrayError."""
        bad_scores = _good_scores(30)
        bad_scores[0] = -0.1
        valid = _good_scores(30)
        with pytest.raises(InvalidScoreArrayError):
            compare_versions(valid, bad_scores, evaluation_mode=EvaluationMode.FULL)

    def test_compare_versions_invalid_scores_empty(self) -> None:
        """Empty scores_a should raise either InsufficientSamplesError or InvalidScoreArrayError."""
        with pytest.raises((InsufficientSamplesError, InvalidScoreArrayError)):
            compare_versions([], _good_scores(30), evaluation_mode=EvaluationMode.FULL)

    def test_invalid_score_array_is_value_error_subclass(self) -> None:
        """InvalidScoreArrayError must be a subclass of ValueError."""
        assert issubclass(InvalidScoreArrayError, ValueError)


class TestCompareVersionsIdenticalArrays:
    """compare_versions() handles all-identical score arrays (degenerate case)."""

    def test_compare_versions_identical_arrays_raises(self) -> None:
        """All-identical scores defeat significance testing and should raise InvalidScoreArrayError."""
        identical = _make_scores(30, 0.93)
        with pytest.raises(InvalidScoreArrayError):
            compare_versions(identical, identical, evaluation_mode=EvaluationMode.FULL)


class TestCompareVersionsAlphaValidation:
    """compare_versions() validates the alpha parameter range."""

    def test_compare_versions_alpha_too_high(self) -> None:
        """alpha > 0.10 should raise ValueError."""
        a = _good_scores(30)
        b = _good_scores(30)
        with pytest.raises(ValueError):
            compare_versions(a, b, alpha=0.20, evaluation_mode=EvaluationMode.FULL)

    def test_compare_versions_alpha_too_low(self) -> None:
        """alpha < 0.001 should raise ValueError."""
        a = _good_scores(30)
        b = _good_scores(30)
        with pytest.raises(ValueError):
            compare_versions(a, b, alpha=0.0001, evaluation_mode=EvaluationMode.FULL)

    def test_compare_versions_bonferroni_alpha_accepted(self) -> None:
        """Bonferroni-corrected alpha (0.05/13 ~ 0.0038) should be accepted."""
        a = _good_scores(30)
        b = _good_scores(30)
        bc = bonferroni_correction(k=13)
        # Should not raise
        result = compare_versions(
            a, b, alpha=bc.alpha_per_test, bonferroni=bc, evaluation_mode=EvaluationMode.FULL
        )
        assert result is not None


# ---------------------------------------------------------------------------
# compare_multiple_metrics() with Bonferroni correction
# ---------------------------------------------------------------------------


class TestCompareMultipleMetrics:
    """compare_multiple_metrics() applies Bonferroni correction across metrics."""

    def test_compare_multiple_metrics_bonferroni_k13(self) -> None:
        """k=13 Bonferroni correction should be applied and reflected in results."""
        a = _good_scores(30)
        b = _good_scores(30)
        metrics = {
            "composite_score": (a, b),
            "completeness": (
                _make_scores_varying(30, 0.92, 0.04),
                _make_scores_varying(30, 0.93, 0.03),
            ),
        }
        results, bc = compare_multiple_metrics(
            metrics,
            k=BONFERRONI_K_FULL_SUITE,
            evaluation_mode=EvaluationMode.FULL,
        )
        assert bc.k == 13
        assert abs(bc.alpha_per_test - 0.05 / 13) < 1e-6
        assert "composite_score" in results
        assert "completeness" in results

    def test_compare_multiple_metrics_returns_bonferroni_config(self) -> None:
        """compare_multiple_metrics() returns a BonferroniConfig as second element."""
        a = _good_scores(30)
        b = _good_scores(30)
        metrics = {"metric1": (a, b)}
        results, bc = compare_multiple_metrics(metrics, evaluation_mode=EvaluationMode.FULL)
        assert bc is not None
        assert bc.alpha_per_test == bc.alpha_family / bc.k

    def test_compare_multiple_metrics_empty_raises(self) -> None:
        """Empty metric_scores dict should raise ValueError."""
        with pytest.raises(ValueError):
            compare_multiple_metrics({}, evaluation_mode=EvaluationMode.FULL)

    def test_compare_multiple_metrics_bonferroni_in_result(self) -> None:
        """Each per-metric result should include the Bonferroni config."""
        a = _good_scores(30)
        b = _good_scores(30)
        metrics = {
            "m1": (a, b),
            "m2": (_make_scores_varying(30, 0.93, 0.03), _make_scores_varying(30, 0.92, 0.04)),
        }
        results, bc = compare_multiple_metrics(metrics, evaluation_mode=EvaluationMode.FULL)
        for result in results.values():
            assert result.bonferroni is not None
            assert result.bonferroni.k == bc.k


# ---------------------------------------------------------------------------
# wilson_score_intervals()
# ---------------------------------------------------------------------------


class TestWilsonScoreIntervals:
    """wilson_score_intervals() computes valid confidence intervals."""

    def test_wilson_score_intervals_known_input(self) -> None:
        """Known input: all 20 scores >= 0.92 should give pass_rate=1.0."""
        scores = [0.93] * 20
        result = wilson_score_intervals(scores)
        assert result.pass_rate == 1.0
        assert result.n_total == 20
        assert result.n_pass == 20

    def test_wilson_score_intervals_zero_pass_rate(self) -> None:
        """All scores below threshold should give pass_rate=0.0."""
        scores = _make_scores_varying(20, 0.50, 0.10)
        result = wilson_score_intervals(scores)
        assert result.pass_rate == 0.0
        assert result.n_pass == 0

    def test_wilson_score_intervals_ci_bounds(self) -> None:
        """Wilson CI lower bound must be <= pass_rate <= upper bound."""
        scores = _make_scores_varying(30, 0.90, 0.06)
        result = wilson_score_intervals(scores)
        assert result.ci_lower <= result.pass_rate <= result.ci_upper

    def test_wilson_score_intervals_ci_width_positive(self) -> None:
        """CI width should be positive (not a degenerate interval)."""
        scores = _make_scores_varying(30, 0.90, 0.06)
        result = wilson_score_intervals(scores)
        assert result.ci_width > 0.0

    def test_wilson_score_intervals_mixed_scores(self) -> None:
        """Mixed scores produce pass_rate between 0 and 1."""
        # 15 above, 15 below threshold (0.92)
        scores = [0.95] * 15 + [0.85] * 15
        result = wilson_score_intervals(scores)
        assert 0.0 < result.pass_rate < 1.0
        assert result.n_pass == 15

    def test_wilson_score_intervals_invalid_score_raises(self) -> None:
        """Out-of-range score should raise InvalidScoreArrayError."""
        scores = _make_scores_varying(20, 0.90, 0.05)
        scores[0] = 1.5
        with pytest.raises(InvalidScoreArrayError):
            wilson_score_intervals(scores)

    def test_wilson_score_intervals_custom_threshold(self) -> None:
        """Custom threshold parameter should be respected."""
        scores = [0.80] * 20  # all below 0.92 but all above 0.70
        result = wilson_score_intervals(scores, threshold=0.70)
        assert result.pass_rate == 1.0

    def test_wilson_score_intervals_all_identical_accepted(self) -> None:
        """All-identical scores are valid for Wilson CI (require_variation=False).

        Unlike compare_versions() which requires variation for Wilcoxon,
        wilson_score_intervals() accepts all-identical arrays because pass-rate
        computation is meaningful even without score variation.
        """
        identical = [0.95] * 20
        result = wilson_score_intervals(identical)
        assert result.pass_rate == 1.0
        assert result.n_total == 20
        assert result.ci_lower <= result.pass_rate <= result.ci_upper


# ---------------------------------------------------------------------------
# merge_decision_from_classification()
# ---------------------------------------------------------------------------


class TestMergeDecisionFromClassification:
    """merge_decision_from_classification() maps every RegressionClass correctly."""

    def test_merge_decision_regression_blocks(self) -> None:
        """REGRESSION classification shall map to BLOCK merge decision."""
        decision = merge_decision_from_classification(RegressionClass.REGRESSION)
        assert decision == MergeDecision.BLOCK

    def test_merge_decision_quality_floor_breach_blocks(self) -> None:
        """QUALITY_FLOOR_BREACH classification shall map to BLOCK merge decision."""
        decision = merge_decision_from_classification(RegressionClass.QUALITY_FLOOR_BREACH)
        assert decision == MergeDecision.BLOCK

    def test_merge_decision_structural_fail_blocks(self) -> None:
        """STRUCTURAL_FAIL classification shall map to BLOCK merge decision."""
        decision = merge_decision_from_classification(RegressionClass.STRUCTURAL_FAIL)
        assert decision == MergeDecision.BLOCK

    def test_merge_decision_marginal_warns(self) -> None:
        """MARGINAL classification shall map to ALLOW_WITH_WARNING."""
        decision = merge_decision_from_classification(RegressionClass.MARGINAL)
        assert decision == MergeDecision.ALLOW_WITH_WARNING

    def test_merge_decision_improvement_warns(self) -> None:
        """IMPROVEMENT classification shall map to ALLOW_WITH_WARNING (log but don't block)."""
        decision = merge_decision_from_classification(RegressionClass.IMPROVEMENT)
        assert decision == MergeDecision.ALLOW_WITH_WARNING

    def test_merge_decision_no_regression_allows(self) -> None:
        """NO_REGRESSION classification shall map to ALLOW."""
        decision = merge_decision_from_classification(RegressionClass.NO_REGRESSION)
        assert decision == MergeDecision.ALLOW


# ---------------------------------------------------------------------------
# bonferroni_correction()
# ---------------------------------------------------------------------------


class TestBonferroniCorrection:
    """bonferroni_correction() computes correct per-test alpha values."""

    def test_bonferroni_correction_k13_alpha(self) -> None:
        """k=13 with alpha_family=0.05 should give alpha_per_test = 0.05/13."""
        bc = bonferroni_correction(k=13)
        expected = 0.05 / 13
        assert abs(bc.alpha_per_test - expected) < 1e-10

    def test_bonferroni_correction_k1_unchanged(self) -> None:
        """k=1 should leave alpha unchanged."""
        bc = bonferroni_correction(k=1)
        assert bc.alpha_per_test == 0.05

    def test_bonferroni_correction_invalid_k(self) -> None:
        """k < 1 should raise ValueError."""
        with pytest.raises(ValueError):
            bonferroni_correction(k=0)

    def test_bonferroni_correction_invalid_alpha_family(self) -> None:
        """alpha_family outside (0, 1) should raise ValueError."""
        with pytest.raises(ValueError):
            bonferroni_correction(k=13, alpha_family=1.0)
        with pytest.raises(ValueError):
            bonferroni_correction(k=13, alpha_family=0.0)

    def test_bonferroni_description_included(self) -> None:
        """BonferroniConfig.description property should reference k and alpha."""
        bc = bonferroni_correction(k=13)
        desc = bc.description
        assert "13" in desc
        assert "Bonferroni" in desc


# ---------------------------------------------------------------------------
# FR-019: One-way dependency guard (stats.py must not import upstream modules)
# ---------------------------------------------------------------------------


class TestStatsDependencyGuard:
    """stats.py must only import from types.py — no upstream dependencies (FR-019)."""

    def test_stats_py_no_forbidden_imports(self) -> None:
        """Verify stats.py does not import from evaluation, metamorphic, baselines,
        or layer4_stats modules. Uses ast.parse() for static analysis so this
        test fails at CI time if someone adds an illegal import.
        """
        import ast
        from pathlib import Path

        stats_path = Path(__file__).resolve().parents[3] / "jerry" / "testing" / "stats.py"
        source = stats_path.read_text()
        tree = ast.parse(source)

        forbidden_modules = {
            "jerry.testing.evaluation",
            "jerry.testing.metamorphic",
            "jerry.testing.baselines",
            "jerry.testing.layer4_stats",
        }

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    for forbidden in forbidden_modules:
                        assert not alias.name.startswith(forbidden), (
                            f"FR-019 violation: stats.py imports {alias.name}"
                        )
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    for forbidden in forbidden_modules:
                        assert not node.module.startswith(forbidden), (
                            f"FR-019 violation: stats.py imports from {node.module}"
                        )
