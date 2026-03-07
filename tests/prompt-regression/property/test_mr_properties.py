# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Property-based tests for jerry.testing.metamorphic — MetamorphicRelation.

Tests invariants that must hold for ALL valid inputs to MR implementations:
    - transform() does not mutate original prompt (pure function)
    - evaluate() always returns MRResult (correct return type)
    - evaluate() result scores match the input sequences provided

All tests use Hypothesis strategies to generate arbitrary valid inputs.
No LLM calls performed.

References:
    - FR-010: Five Universal Metamorphic Relations
    - behavioral-contracts.md Section C
      (projects/PROJ-036-prompt-regression-harness/contracts/behavioral-contracts.md)
    - H-20: 90% line coverage target
"""

from __future__ import annotations

import pytest
from hypothesis import HealthCheck, assume, given, settings
from hypothesis import strategies as st

from jerry.testing.metamorphic.base import MRResult, MRViolationSeverity
from jerry.testing.metamorphic.mr_001_paraphrase import ParaphraseConsistency
from jerry.testing.metamorphic.mr_002_negation import NegationHandling
from jerry.testing.stats import InsufficientSamplesError

# ---------------------------------------------------------------------------
# Strategies
# ---------------------------------------------------------------------------


def _valid_prompt_strategy() -> st.SearchStrategy[str]:
    """Return a Hypothesis strategy for non-empty prompt strings."""
    return st.text(
        alphabet=st.characters(whitelist_categories=("Lu", "Ll", "Nd", "Zs")),
        min_size=1,
        max_size=200,
    ).filter(lambda s: s.strip())  # Ensure non-whitespace-only


def _mr_score_sequence_strategy(min_n: int = 20, max_n: int = 30) -> st.SearchStrategy[list[float]]:
    """Return a Hypothesis strategy for a valid MR score sequence."""
    return st.lists(
        st.floats(min_value=0.0, max_value=1.0, allow_nan=False, allow_infinity=False),
        min_size=min_n,
        max_size=max_n,
    )


def _mr_002_score_sequence_strategy() -> st.SearchStrategy[list[float]]:
    """MR-002 has a lower minimum of 15 samples."""
    return _mr_score_sequence_strategy(min_n=15, max_n=25)


# ---------------------------------------------------------------------------
# transform() does not mutate original prompt
# ---------------------------------------------------------------------------


@given(prompt=_valid_prompt_strategy())
@settings(max_examples=50, suppress_health_check=[HealthCheck.too_slow], deadline=None)
def test_mr001_transform_preserves_input(prompt: str) -> None:
    """MR-001 transform() must not mutate the original prompt string.

    Python strings are immutable, but we verify the transform() contract
    explicitly: the returned value is a new string, not the same object
    in a modified state.
    """
    mr = ParaphraseConsistency()
    original = str(prompt)  # Ensure we have a copy
    result = mr.transform(prompt)

    # The original should be unchanged
    assert prompt == original
    # The result should be a non-empty string
    assert isinstance(result, str)
    assert len(result) > 0


@given(prompt=_valid_prompt_strategy())
@settings(max_examples=50, suppress_health_check=[HealthCheck.too_slow], deadline=None)
def test_mr002_transform_preserves_input(prompt: str) -> None:
    """MR-002 transform() must not mutate the original prompt string."""
    mr = NegationHandling()
    original = str(prompt)
    result = mr.transform(prompt)

    # The original should be unchanged
    assert prompt == original
    # The result must be a non-empty string
    assert isinstance(result, str)
    assert len(result) > 0


# ---------------------------------------------------------------------------
# transform() actually transforms the input (not identity)
# ---------------------------------------------------------------------------


def test_mr001_transform_known_substitution() -> None:
    """MR-001 transform() must produce output distinct from input.

    'Research' is a known substitution trigger; the transform must
    produce a different string (not an identity function).

    Evidence quality: assert result differs from input.

    References:
        - FR-010: MR-001 Paraphrase Consistency
        - behavioral-contracts.md Section C
          (projects/PROJ-036-prompt-regression-harness/contracts/behavioral-contracts.md)
    """
    mr = ParaphraseConsistency()
    prompt = "Research the authentication patterns."
    result = mr.transform(prompt)

    # Transformation must have occurred — result must differ from input
    assert result != prompt, (
        f"transform() returned the input unchanged: {result!r}. "
        "MR-001 must apply a paraphrase substitution."
    )
    # The substitution should replace 'Research' with 'Survey'
    assert "Survey" in result or "research" not in result.lower()


# ---------------------------------------------------------------------------
# evaluate() always returns MRResult
# ---------------------------------------------------------------------------


@given(
    original_scores=_mr_score_sequence_strategy(),
    transformed_scores=_mr_score_sequence_strategy(),
)
@settings(
    max_examples=30,
    suppress_health_check=[HealthCheck.too_slow, HealthCheck.filter_too_much],
    deadline=None,
)
def test_mr001_evaluate_result_type(
    original_scores: list[float], transformed_scores: list[float]
) -> None:
    """MR-001 evaluate() must always return an MRResult instance.

    When given valid inputs (N >= 20, equal lengths, scores in [0, 1]),
    evaluate() must return an MRResult — never raise, never return None.
    """
    mr = ParaphraseConsistency()

    # Truncate to minimum length for equal-length requirement
    min_n = min(len(original_scores), len(transformed_scores))
    # Use assume() instead of early-return so Hypothesis correctly
    # tracks these as filtered examples, not test successes.
    assume(min_n >= 20)

    orig = original_scores[:min_n]
    trans = transformed_scores[:min_n]

    result = mr.evaluate(orig, trans)

    assert isinstance(result, MRResult)
    assert result.mr_id == "MR-001"
    assert result.mr_name == "Paraphrase Consistency"
    assert isinstance(result.passed, bool)
    assert isinstance(result.severity, MRViolationSeverity)
    assert isinstance(result.evidence, str)


@given(
    original_scores=_mr_002_score_sequence_strategy(),
    transformed_scores=_mr_002_score_sequence_strategy(),
)
@settings(
    max_examples=30,
    suppress_health_check=[HealthCheck.too_slow, HealthCheck.filter_too_much],
    deadline=None,
)
def test_mr002_evaluate_result_type(
    original_scores: list[float], transformed_scores: list[float]
) -> None:
    """MR-002 evaluate() must always return an MRResult instance.

    When given valid inputs (N >= 15, equal lengths, scores in [0, 1]),
    evaluate() must return an MRResult.
    """
    mr = NegationHandling()

    min_n = min(len(original_scores), len(transformed_scores))
    # Use assume() instead of early-return so Hypothesis correctly
    # tracks these as filtered examples, not test successes.
    assume(min_n >= 15)

    orig = original_scores[:min_n]
    trans = transformed_scores[:min_n]

    result = mr.evaluate(orig, trans)

    assert isinstance(result, MRResult)
    assert result.mr_id == "MR-002"
    assert isinstance(result.passed, bool)
    # p_value must be in valid probability range [0.0, 1.0]
    assert 0.0 <= result.p_value <= 1.0, (
        f"p_value={result.p_value} is outside valid probability range [0.0, 1.0]"
    )


# ---------------------------------------------------------------------------
# evaluate() result scores match inputs
# ---------------------------------------------------------------------------


@given(
    original_scores=_mr_score_sequence_strategy(min_n=20, max_n=25),
    transformed_scores=_mr_score_sequence_strategy(min_n=20, max_n=25),
)
@settings(
    max_examples=20,
    suppress_health_check=[HealthCheck.too_slow, HealthCheck.filter_too_much],
    deadline=None,
)
def test_mr001_evaluate_scores_match_inputs(
    original_scores: list[float], transformed_scores: list[float]
) -> None:
    """MR-001 MRResult must embed the exact score sequences provided as input.

    The original_scores and transformed_scores in MRResult should match
    the sequences passed to evaluate().
    """
    mr = ParaphraseConsistency()

    min_n = min(len(original_scores), len(transformed_scores))
    # Use assume() instead of early-return so Hypothesis correctly
    # tracks these as filtered examples, not test successes.
    assume(min_n >= 20)

    orig = original_scores[:min_n]
    trans = transformed_scores[:min_n]

    result = mr.evaluate(orig, trans)

    assert result.original_scores == tuple(orig)
    assert result.transformed_scores == tuple(trans)


# ---------------------------------------------------------------------------
# MRResult invariants
# ---------------------------------------------------------------------------


@given(
    original_scores=_mr_score_sequence_strategy(min_n=20, max_n=25),
    transformed_scores=_mr_score_sequence_strategy(min_n=20, max_n=25),
)
@settings(
    max_examples=20,
    suppress_health_check=[HealthCheck.too_slow, HealthCheck.filter_too_much],
    deadline=None,
)
def test_mr001_result_mean_delta_nonnegative(
    original_scores: list[float], transformed_scores: list[float]
) -> None:
    """MR-001 MRResult.mean_delta must always be non-negative (absolute difference)."""
    mr = ParaphraseConsistency()

    min_n = min(len(original_scores), len(transformed_scores))
    assume(min_n >= 20)

    orig = original_scores[:min_n]
    trans = transformed_scores[:min_n]

    result = mr.evaluate(orig, trans)

    assert result.mean_delta >= 0.0, (
        f"mean_delta={result.mean_delta} is negative (should be absolute value)"
    )


@given(
    original_scores=_mr_score_sequence_strategy(min_n=20, max_n=25),
    transformed_scores=_mr_score_sequence_strategy(min_n=20, max_n=25),
)
@settings(
    max_examples=20,
    suppress_health_check=[HealthCheck.too_slow, HealthCheck.filter_too_much],
    deadline=None,
)
def test_mr001_result_effect_size_bounded(
    original_scores: list[float], transformed_scores: list[float]
) -> None:
    """MR-001 MRResult.effect_size (Cohen's r) must be in [0.0, 1.0]."""
    mr = ParaphraseConsistency()

    min_n = min(len(original_scores), len(transformed_scores))
    assume(min_n >= 20)

    orig = original_scores[:min_n]
    trans = transformed_scores[:min_n]

    result = mr.evaluate(orig, trans)

    assert 0.0 <= result.effect_size <= 1.0, f"effect_size={result.effect_size} is outside [0, 1]"


@given(
    original_scores=_mr_score_sequence_strategy(min_n=20, max_n=25),
    transformed_scores=_mr_score_sequence_strategy(min_n=20, max_n=25),
)
@settings(
    max_examples=20,
    suppress_health_check=[HealthCheck.too_slow, HealthCheck.filter_too_much],
    deadline=None,
)
def test_mr001_result_p_value_bounded(
    original_scores: list[float], transformed_scores: list[float]
) -> None:
    """MR-001 MRResult.p_value must be in [0.0, 1.0]."""
    mr = ParaphraseConsistency()

    min_n = min(len(original_scores), len(transformed_scores))
    assume(min_n >= 20)

    orig = original_scores[:min_n]
    trans = transformed_scores[:min_n]

    result = mr.evaluate(orig, trans)

    assert 0.0 <= result.p_value <= 1.0, f"p_value={result.p_value} is outside [0, 1]"


# ---------------------------------------------------------------------------
# InsufficientSamplesError raised for too-small inputs
# ---------------------------------------------------------------------------


@given(
    n=st.integers(min_value=1, max_value=19),
)
@settings(max_examples=20, deadline=None)
def test_mr001_insufficient_samples_always_raises(n: int) -> None:
    """MR-001 evaluate() must always raise InsufficientSamplesError for N < 20."""
    mr = ParaphraseConsistency()
    scores = [0.90] * n

    with pytest.raises(InsufficientSamplesError):
        mr.evaluate(scores, scores)


@given(
    n=st.integers(min_value=1, max_value=14),
)
@settings(max_examples=20, deadline=None)
def test_mr002_insufficient_samples_always_raises(n: int) -> None:
    """MR-002 evaluate() must always raise InsufficientSamplesError for N < 15."""
    mr = NegationHandling()
    scores = [0.90] * n

    with pytest.raises(InsufficientSamplesError):
        mr.evaluate(scores, scores)
