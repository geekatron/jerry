# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Unit tests for jerry.testing.metamorphic.base — MetamorphicRelation ABC.

Tests the shared base class and its concrete behaviors:
    - _validate_inputs(): insufficient samples, length mismatch, out-of-range scores
    - MRResult frozen dataclass immutability
    - MRViolationSeverity enum members

Also tests the concrete MR implementations (MR-001 and MR-002) for their
transform() and evaluate() behaviors.

No LLM calls performed. All test inputs are deterministic.

References:
    - FR-010: Five Universal Metamorphic Relations
    - behavioral-contracts.md Section C
      (projects/PROJ-036-prompt-regression-harness/contracts/behavioral-contracts.md)
    - H-20: 90% line coverage target
"""

from __future__ import annotations

import dataclasses
from collections.abc import Sequence

import pytest

from jerry.testing.metamorphic.base import (
    MetamorphicRelation,
    MRResult,
    MRViolationSeverity,
)
from jerry.testing.metamorphic.mr_001_paraphrase import ParaphraseConsistency
from jerry.testing.metamorphic.mr_002_negation import NegationHandling
from jerry.testing.stats import InsufficientSamplesError

# ---------------------------------------------------------------------------
# Concrete stub for testing the ABC
# ---------------------------------------------------------------------------


class _ConcreteStubMR(MetamorphicRelation):
    """Minimal concrete implementation of MetamorphicRelation for ABC testing."""

    mr_id: str = "MR-TEST"
    mr_name: str = "Stub MR for testing"
    minimum_sample_size: int = 20

    def transform(self, input_text: str) -> str:
        """Return input unchanged (passthrough transform for testing)."""
        if not input_text:
            raise ValueError("Empty input not permitted.")
        return input_text

    def evaluate(
        self,
        original_scores: Sequence[float],
        transformed_scores: Sequence[float],
    ) -> MRResult:
        """Return a PASS MRResult for any valid input."""
        self._validate_inputs(original_scores, transformed_scores)
        mean_o = self._mean(original_scores)
        mean_t = self._mean(transformed_scores)
        return MRResult(
            mr_id=self.mr_id,
            mr_name=self.mr_name,
            passed=True,
            original_scores=tuple(original_scores),
            transformed_scores=tuple(transformed_scores),
            mean_original=mean_o,
            mean_transformed=mean_t,
            mean_delta=abs(mean_o - mean_t),
            tolerance=0.05,
            effect_size=0.0,
            p_value=1.0,
            severity=MRViolationSeverity.PASS,
            evidence="Stub pass.",
        )


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def stub_mr() -> _ConcreteStubMR:
    """Return a concrete stub MetamorphicRelation for testing the ABC."""
    return _ConcreteStubMR()


def _valid_scores(n: int = 25, base: float = 0.93) -> list[float]:
    """Return N alternating scores with variation above 0.0."""
    return [base if i % 2 == 0 else base + 0.04 for i in range(n)]


# ---------------------------------------------------------------------------
# MRViolationSeverity
# ---------------------------------------------------------------------------


class TestMRViolationSeverity:
    """Verify MRViolationSeverity enum members."""

    def test_pass_member(self) -> None:
        """PASS must be present with value 'PASS'."""
        assert MRViolationSeverity.PASS.value == "PASS"

    def test_informational_member(self) -> None:
        """INFORMATIONAL must be present."""
        assert MRViolationSeverity.INFORMATIONAL.value == "INFORMATIONAL"

    def test_warning_member(self) -> None:
        """WARNING must be present."""
        assert MRViolationSeverity.WARNING.value == "WARNING"

    def test_regression_member(self) -> None:
        """REGRESSION must be present."""
        assert MRViolationSeverity.REGRESSION.value == "REGRESSION"

    def test_critical_member(self) -> None:
        """CRITICAL must be present."""
        assert MRViolationSeverity.CRITICAL.value == "CRITICAL"


# ---------------------------------------------------------------------------
# MRResult frozen dataclass
# ---------------------------------------------------------------------------


class TestMRResult:
    """MRResult is a frozen dataclass."""

    def _make_result(self) -> MRResult:
        scores = _valid_scores(25)
        return MRResult(
            mr_id="MR-001",
            mr_name="Paraphrase Consistency",
            passed=True,
            original_scores=tuple(scores),
            transformed_scores=tuple(scores),
            mean_original=0.93,
            mean_transformed=0.93,
            mean_delta=0.0,
            tolerance=0.05,
            effect_size=0.0,
            p_value=1.0,
            severity=MRViolationSeverity.PASS,
            evidence="MR-001 PASSED.",
        )

    def test_mr_result_frozen(self) -> None:
        """MRResult should be immutable (frozen=True)."""
        result = self._make_result()
        with pytest.raises((dataclasses.FrozenInstanceError, AttributeError)):
            result.passed = False  # type: ignore[misc]

    def test_mr_result_fields_present(self) -> None:
        """MRResult must expose all required fields with correct values."""
        result = self._make_result()
        assert result.mr_id == "MR-001"
        assert result.mr_name == "Paraphrase Consistency"
        assert result.passed is True
        assert len(result.original_scores) == 25
        assert len(result.transformed_scores) == 25
        assert result.severity == MRViolationSeverity.PASS
        assert result.evidence == "MR-001 PASSED."

    def test_mr_result_mean_delta_correct(self) -> None:
        """mean_delta should match |mean_original - mean_transformed|."""
        result = self._make_result()
        assert result.mean_delta == pytest.approx(
            abs(result.mean_original - result.mean_transformed)
        )


# ---------------------------------------------------------------------------
# MetamorphicRelation._validate_inputs()
# ---------------------------------------------------------------------------


class TestValidateInputsInsufficientSamples:
    """_validate_inputs() raises InsufficientSamplesError when N < minimum_sample_size."""

    def test_insufficient_samples_raises(self, stub_mr: _ConcreteStubMR) -> None:
        """N < 20 should raise InsufficientSamplesError."""
        small = [0.93] * 10
        with pytest.raises(InsufficientSamplesError) as exc_info:
            stub_mr._validate_inputs(small, small)
        assert "MR-TEST" in str(exc_info.value)
        assert "20" in str(exc_info.value)

    def test_exactly_minimum_does_not_raise(self, stub_mr: _ConcreteStubMR) -> None:
        """N == 20 (minimum_sample_size) should not raise."""
        scores = _valid_scores(20)
        # Should not raise
        stub_mr._validate_inputs(scores, scores)

    def test_insufficient_error_message_format(self, stub_mr: _ConcreteStubMR) -> None:
        """Error message should include MR ID and minimum sample size."""
        small = [0.90] * 5
        with pytest.raises(InsufficientSamplesError) as exc_info:
            stub_mr._validate_inputs(small, small)
        msg = str(exc_info.value)
        assert "MR-TEST" in msg
        assert "20" in msg


class TestValidateInputsLengthMismatch:
    """_validate_inputs() raises ValueError when sequence lengths differ."""

    def test_length_mismatch_raises(self, stub_mr: _ConcreteStubMR) -> None:
        """Mismatched sequence lengths should raise ValueError."""
        original = _valid_scores(25)
        transformed = _valid_scores(20)
        with pytest.raises(ValueError) as exc_info:
            stub_mr._validate_inputs(original, transformed)
        assert "length" in str(exc_info.value).lower() or "MR-TEST" in str(exc_info.value)

    def test_equal_lengths_do_not_raise(self, stub_mr: _ConcreteStubMR) -> None:
        """Equal lengths should pass validation."""
        scores = _valid_scores(25)
        stub_mr._validate_inputs(scores, scores)  # Should not raise


class TestValidateInputsOutOfRange:
    """_validate_inputs() raises ValueError for scores outside [0.0, 1.0]."""

    def test_score_above_one_raises(self, stub_mr: _ConcreteStubMR) -> None:
        """Score > 1.0 should raise ValueError."""
        scores = _valid_scores(25)
        bad = list(scores)
        bad[0] = 1.01
        with pytest.raises(ValueError):
            stub_mr._validate_inputs(bad, scores)

    def test_score_below_zero_raises(self, stub_mr: _ConcreteStubMR) -> None:
        """Score < 0.0 should raise ValueError."""
        scores = _valid_scores(25)
        bad = list(scores)
        bad[3] = -0.01
        with pytest.raises(ValueError):
            stub_mr._validate_inputs(scores, bad)

    def test_boundary_values_accepted(self, stub_mr: _ConcreteStubMR) -> None:
        """Exactly 0.0 and 1.0 should be accepted as valid boundary values."""
        # Alternating 0.0 and 1.0 to avoid all-identical issues
        boundary_scores = [0.0 if i % 2 == 0 else 1.0 for i in range(25)]
        stub_mr._validate_inputs(boundary_scores, boundary_scores)  # Should not raise


# ---------------------------------------------------------------------------
# MetamorphicRelation._mean() and _std() helpers
# ---------------------------------------------------------------------------


class TestStatisticalHelpers:
    """Test the shared statistical helper methods."""

    def test_mean_helper(self, stub_mr: _ConcreteStubMR) -> None:
        """_mean() should return correct arithmetic mean."""
        scores = [0.90, 0.92, 0.94]
        assert stub_mr._mean(scores) == pytest.approx(0.92)

    def test_std_helper_single_value(self, stub_mr: _ConcreteStubMR) -> None:
        """_std() with a single value should return 0.0."""
        assert stub_mr._std([0.93]) == 0.0

    def test_std_helper_multiple_values(self, stub_mr: _ConcreteStubMR) -> None:
        """_std() with multiple values should return a non-negative number."""
        scores = [0.90, 0.92, 0.94, 0.88, 0.96]
        std = stub_mr._std(scores)
        assert std >= 0.0


# ---------------------------------------------------------------------------
# ParaphraseConsistency (MR-001) — concrete behavior
# ---------------------------------------------------------------------------


class TestParaphraseConsistency:
    """Tests for MR-001 ParaphraseConsistency transform and evaluate."""

    @pytest.fixture
    def mr(self) -> ParaphraseConsistency:
        """Return a ParaphraseConsistency instance."""
        return ParaphraseConsistency()

    def test_transform_non_empty_input(self, mr: ParaphraseConsistency) -> None:
        """transform() should return a non-empty string."""
        result = mr.transform("Research the topic carefully.")
        assert isinstance(result, str)
        assert len(result) > 0

    def test_transform_empty_raises(self, mr: ParaphraseConsistency) -> None:
        """transform() with empty input should raise ValueError."""
        with pytest.raises(ValueError):
            mr.transform("")

    def test_transform_whitespace_only_raises(self, mr: ParaphraseConsistency) -> None:
        """transform() with whitespace-only input should raise ValueError."""
        with pytest.raises(ValueError):
            mr.transform("   ")

    def test_transform_known_substitution(self, mr: ParaphraseConsistency) -> None:
        """'Research' should be substituted to 'Survey'."""
        result = mr.transform("Research the authentication patterns.")
        assert "Survey" in result or "research" not in result.lower()

    def test_transform_is_deterministic(self, mr: ParaphraseConsistency) -> None:
        """transform() on the same input should always return the same output."""
        text = "Research the topic carefully."
        result_a = mr.transform(text)
        result_b = mr.transform(text)
        assert result_a == result_b

    def test_evaluate_insufficient_samples(self, mr: ParaphraseConsistency) -> None:
        """evaluate() with N < 20 should raise InsufficientSamplesError."""
        small = [0.93] * 10
        with pytest.raises(InsufficientSamplesError):
            mr.evaluate(small, small)

    def test_mr_id_and_name(self, mr: ParaphraseConsistency) -> None:
        """MR-001 should have correct mr_id and mr_name."""
        assert mr.mr_id == "MR-001"
        assert mr.mr_name == "Paraphrase Consistency"

    def test_minimum_sample_size(self, mr: ParaphraseConsistency) -> None:
        """MR-001 minimum_sample_size should be 20."""
        assert mr.minimum_sample_size == 20


# ---------------------------------------------------------------------------
# NegationHandling (MR-002) — concrete behavior
# ---------------------------------------------------------------------------


class TestNegationHandling:
    """Tests for MR-002 NegationHandling transform and evaluate."""

    @pytest.fixture
    def mr(self) -> NegationHandling:
        """Return a NegationHandling instance."""
        return NegationHandling()

    def test_transform_non_empty_input(self, mr: NegationHandling) -> None:
        """transform() should return a non-empty string."""
        result = mr.transform("The agent must include L0/L1/L2 sections.")
        assert isinstance(result, str)
        assert len(result) > 0

    def test_transform_empty_raises(self, mr: NegationHandling) -> None:
        """transform() with empty input should raise ValueError."""
        with pytest.raises(ValueError):
            mr.transform("")

    def test_transform_known_negation(self, mr: NegationHandling) -> None:
        """'must include' should be transformed to 'must NOT include'."""
        result = mr.transform("The output must include citations.")
        assert "NOT" in result or "not" in result

    def test_transform_fallback_prefix(self, mr: NegationHandling) -> None:
        """Input with no matching pattern should receive fallback negation prefix."""
        result = mr.transform("Do the task in a thoughtful manner.")
        # Fallback adds a prefix instruction
        assert len(result) > len("Do the task in a thoughtful manner.")

    def test_evaluate_insufficient_samples(self, mr: NegationHandling) -> None:
        """evaluate() with N < 15 should raise InsufficientSamplesError."""
        small = [0.93] * 10
        with pytest.raises(InsufficientSamplesError):
            mr.evaluate(small, small)

    def test_mr_id_and_name(self, mr: NegationHandling) -> None:
        """MR-002 should have correct mr_id and mr_name."""
        assert mr.mr_id == "MR-002"
        assert mr.mr_name == "Negation Handling"

    def test_minimum_sample_size_reduced(self, mr: NegationHandling) -> None:
        """MR-002 minimum_sample_size should be 15 (reduced from default 20)."""
        assert mr.minimum_sample_size == 15
