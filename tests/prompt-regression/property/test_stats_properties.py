# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Victor Lau

"""Property-based tests for jerry.testing.stats using Hypothesis.

Tests statistical invariants that must hold for ALL valid inputs,
not just specific examples:
    - compare_versions symmetry: swapping A/B inverts effect direction
    - Score bounds: all output scores from statistical functions in [0, 1]
    - Wilson CI bounds: lower <= pass_rate <= upper
    - Bonferroni alpha: more metrics always produces smaller per-test alpha

All tests use Hypothesis strategies to generate arbitrary valid inputs.
No LLM calls performed.

References:
    - FR-014: N >= 20 enforcement
    - FR-015: Wilcoxon signed-rank (two-sided)
    - FR-016: Wilson score confidence intervals
    - FR-017: Bonferroni correction
    - H-20: 90% line coverage target
"""

from __future__ import annotations

from hypothesis import HealthCheck, assume, given, settings
from hypothesis import strategies as st

from jerry.testing.stats import (
    bonferroni_correction,
    compare_versions,
    wilson_score_intervals,
)
from jerry.testing.types import EvaluationMode, RegressionClass

# ---------------------------------------------------------------------------
# Strategy helpers
# ---------------------------------------------------------------------------


def _score_strategy(min_val: float = 0.0, max_val: float = 1.0) -> st.SearchStrategy[float]:
    """Return a Hypothesis strategy for a single score in [min_val, max_val]."""
    return st.floats(min_value=min_val, max_value=max_val, allow_nan=False, allow_infinity=False)


def _score_array_strategy(
    min_n: int = 20,
    max_n: int = 35,
) -> st.SearchStrategy[list[float]]:
    """Return a Hypothesis strategy for a valid score array with variation.

    Ensures the array has N >= 20 elements and contains variation
    (not all-identical) to satisfy Wilcoxon requirements.
    """
    return st.lists(
        _score_strategy(
            min_val=0.01, max_val=0.99
        ),  # Avoid exact 0/1 boundaries to ensure variation
        min_size=min_n,
        max_size=max_n,
    ).filter(lambda scores: len(set(scores)) > 1)  # Require at least 2 distinct values


# ---------------------------------------------------------------------------
# Symmetry property: swapping A/B inverts effect direction
# ---------------------------------------------------------------------------


@given(
    scores_a=_score_array_strategy(),
    scores_b=_score_array_strategy(),
)
@settings(
    max_examples=40,
    suppress_health_check=[HealthCheck.too_slow, HealthCheck.filter_too_much],
    deadline=None,
)
def test_compare_versions_symmetry(scores_a: list[float], scores_b: list[float]) -> None:
    """Swapping A and B should invert the mean_delta direction.

    If mean_b > mean_a in the original call, then mean_a > mean_b
    in the swapped call, and vice versa.  The magnitude of mean_delta
    should be the same in both calls.

    Skip degenerate cases where scores_a == scores_b element-wise:
    scipy.stats.wilcoxon returns NaN p-value when all differences are zero,
    and NaN arithmetic is not comparable.
    """
    # Skip if arrays are identical element-wise (Wilcoxon undefined on zero diffs)
    assume(scores_a != scores_b)
    # Also skip if the concatenated difference has no variation for Wilcoxon
    diffs = [b - a for a, b in zip(scores_a, scores_b, strict=False)]
    assume(any(d != 0.0 for d in diffs))

    result_ab = compare_versions(scores_a, scores_b, evaluation_mode=EvaluationMode.FULL)
    result_ba = compare_versions(scores_b, scores_a, evaluation_mode=EvaluationMode.FULL)

    # Skip NaN p-values (degenerate Wilcoxon inputs that scipy cannot handle)
    import math  # noqa: PLC0415

    assume(not math.isnan(result_ab.wilcoxon.p_value))
    assume(not math.isnan(result_ba.wilcoxon.p_value))

    # mean_delta(A→B) should equal -mean_delta(B→A)
    assert abs(result_ab.wilcoxon.mean_delta + result_ba.wilcoxon.mean_delta) < 1e-7

    # p-values should be identical (Wilcoxon is symmetric)
    assert abs(result_ab.wilcoxon.p_value - result_ba.wilcoxon.p_value) < 1e-7

    # Effect sizes should be identical in magnitude
    assert abs(result_ab.wilcoxon.cohens_r - result_ba.wilcoxon.cohens_r) < 1e-6


# ---------------------------------------------------------------------------
# Score bounds property: all output values in [0, 1]
# ---------------------------------------------------------------------------


@given(scores=_score_array_strategy())
@settings(max_examples=30, suppress_health_check=[HealthCheck.too_slow], deadline=None)
def test_compare_versions_score_bounds(scores: list[float]) -> None:
    """All output scores from compare_versions() must be in [0.0, 1.0].

    Cohen's r effect size and p-values must both be in the valid range.

    A floating-point tolerance of 1e-10 is applied to Wilson CI bounds because
    scipy's Wilson interval computation may produce ci_lower values like -1.39e-17
    when all scores fail (pass_rate==0.0), which is within machine epsilon of 0.
    """
    _EPS = 1e-10

    result = compare_versions(scores, scores[::-1], evaluation_mode=EvaluationMode.FULL)

    assert 0.0 - _EPS <= result.wilcoxon.cohens_r <= 1.0 + _EPS
    assert 0.0 - _EPS <= result.wilcoxon.p_value <= 1.0 + _EPS
    assert 0.0 - _EPS <= result.wilson_a.pass_rate <= 1.0 + _EPS
    assert 0.0 - _EPS <= result.wilson_b.pass_rate <= 1.0 + _EPS
    assert 0.0 - _EPS <= result.wilson_a.ci_lower <= result.wilson_a.ci_upper <= 1.0 + _EPS
    assert 0.0 - _EPS <= result.wilson_b.ci_lower <= result.wilson_b.ci_upper <= 1.0 + _EPS


# ---------------------------------------------------------------------------
# Wilson CI bounds property: lower <= pass_rate <= upper
# ---------------------------------------------------------------------------


@given(
    scores=st.lists(
        _score_strategy(min_val=0.0, max_val=1.0),
        min_size=5,
        max_size=50,
    )
)
@settings(max_examples=50, suppress_health_check=[HealthCheck.too_slow], deadline=None)
def test_wilson_ci_bounds(scores: list[float]) -> None:
    """Wilson CI must always satisfy: ci_lower <= pass_rate <= ci_upper.

    This must hold for any score array, including all-pass and all-fail arrays.

    A floating-point tolerance of 1e-10 is applied to the bounds check because
    scipy's Wilson interval computation may produce ci_lower values like 2.78e-17
    when all scores fail (pass_rate==0.0), which is within machine epsilon of 0.
    """
    _EPS = 1e-10  # Tolerance for Wilson CI floating-point boundary

    result = wilson_score_intervals(scores)

    assert result.ci_lower >= 0.0 - _EPS, f"ci_lower={result.ci_lower} < 0"
    assert result.ci_upper <= 1.0 + _EPS, f"ci_upper={result.ci_upper} > 1"
    assert result.ci_lower <= result.ci_upper + _EPS, (
        f"CI bounds inverted: [{result.ci_lower}, {result.ci_upper}]"
    )
    assert result.ci_lower - _EPS <= result.pass_rate <= result.ci_upper + _EPS, (
        f"pass_rate={result.pass_rate} outside CI [{result.ci_lower}, {result.ci_upper}]"
    )
    assert result.ci_width >= 0.0 - _EPS, f"ci_width={result.ci_width} is negative"


# ---------------------------------------------------------------------------
# Bonferroni alpha property: more metrics → smaller per-test alpha
# ---------------------------------------------------------------------------


@given(
    k_small=st.integers(min_value=1, max_value=10),
    k_large_delta=st.integers(min_value=1, max_value=10),
)
@settings(max_examples=30, deadline=None)
def test_bonferroni_alpha_decreases(k_small: int, k_large_delta: int) -> None:
    """Adding more metrics (larger k) must decrease the per-test alpha.

    This is a fundamental invariant of Bonferroni correction:
    alpha_per_test = alpha_family / k, so larger k means smaller alpha_per_test.
    """
    k_large = k_small + k_large_delta  # k_large > k_small

    bc_small = bonferroni_correction(k=k_small)
    bc_large = bonferroni_correction(k=k_large)

    assert bc_large.alpha_per_test < bc_small.alpha_per_test, (
        f"Expected alpha to decrease: k={k_small} gave {bc_small.alpha_per_test}, "
        f"k={k_large} gave {bc_large.alpha_per_test}"
    )


# ---------------------------------------------------------------------------
# Classification consistency: REGRESSION → BLOCK, NO_REGRESSION → ALLOW
# ---------------------------------------------------------------------------


@given(
    scores_a=_score_array_strategy(),
    scores_b=_score_array_strategy(),
)
@settings(
    max_examples=30,
    suppress_health_check=[HealthCheck.too_slow],
    deadline=None,
)
def test_merge_decision_consistent_with_classification(
    scores_a: list[float], scores_b: list[float]
) -> None:
    """The merge_decision must be consistent with the classification.

    REGRESSION → BLOCK
    QUALITY_FLOOR_BREACH → BLOCK
    STRUCTURAL_FAIL → BLOCK
    MARGINAL → ALLOW_WITH_WARNING
    IMPROVEMENT → ALLOW_WITH_WARNING
    NO_REGRESSION → ALLOW
    """
    from jerry.testing.types import MergeDecision

    result = compare_versions(scores_a, scores_b, evaluation_mode=EvaluationMode.FULL)

    blocking_classes = {
        RegressionClass.REGRESSION,
        RegressionClass.QUALITY_FLOOR_BREACH,
        RegressionClass.STRUCTURAL_FAIL,
    }
    warning_classes = {RegressionClass.MARGINAL, RegressionClass.IMPROVEMENT}
    allow_classes = {RegressionClass.NO_REGRESSION}

    cls = result.classification
    decision = result.merge_decision

    if cls in blocking_classes:
        assert decision == MergeDecision.BLOCK, (
            f"Classification {cls} should produce BLOCK but got {decision}"
        )
    elif cls in warning_classes:
        assert decision == MergeDecision.ALLOW_WITH_WARNING, (
            f"Classification {cls} should produce ALLOW_WITH_WARNING but got {decision}"
        )
    elif cls in allow_classes:
        assert decision == MergeDecision.ALLOW, (
            f"Classification {cls} should produce ALLOW but got {decision}"
        )


# ---------------------------------------------------------------------------
# Wilson CI width property: CI width decreases as N increases
# ---------------------------------------------------------------------------


@given(
    base_scores=st.lists(
        _score_strategy(min_val=0.85, max_val=0.99),
        min_size=20,
        max_size=20,
    ),
    extra_scores=st.lists(
        _score_strategy(min_val=0.85, max_val=0.99),
        min_size=10,
        max_size=30,
    ),
)
@settings(max_examples=30, deadline=None)
def test_wilson_ci_width_decreases_with_n(
    base_scores: list[float], extra_scores: list[float]
) -> None:
    """Larger N should produce a narrower Wilson CI (more precise estimate).

    This is a fundamental property of confidence intervals.
    Note: We compare N=20 vs N=20+extra; the larger sample should
    have a smaller or equal CI width.
    """
    small_result = wilson_score_intervals(base_scores)
    large_result = wilson_score_intervals(base_scores + extra_scores)

    # CI width must decrease (or remain equal within floating-point tolerance)
    # as N grows. An absolute tolerance of 0.02 accommodates edge cases where
    # the additional scores shift the pass_rate distribution slightly, while
    # being tight enough to detect meaningful CI-width regressions in the
    # statsmodels Wilson implementation.
    assert large_result.ci_width <= small_result.ci_width + 0.02, (
        f"Large N ({len(base_scores + extra_scores)}) CI width "
        f"{large_result.ci_width:.4f} exceeds small N ({len(base_scores)}) "
        f"CI width {small_result.ci_width:.4f} by more than 0.02"
    )
