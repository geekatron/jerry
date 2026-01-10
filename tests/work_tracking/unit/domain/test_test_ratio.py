"""Unit tests for work_tracking.domain.value_objects.test_ratio module.

Test Categories:
    - Happy Path: Normal creation and operations
    - Edge Cases: Boundary conditions
    - Negative Cases: Validation errors
    - Quality Level: QualityLevel enum and integration

References:
    - PAT-005-e006: Quality Gate Value Objects
    - Constraint c-006: Test Distribution Requirements
"""
from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest

from src.work_tracking.domain.value_objects.test_ratio import QualityLevel, TestRatio


class TestQualityLevel:
    """Tests for QualityLevel enum."""

    def test_l0_value(self) -> None:
        """QualityLevel.L0 has value 'L0'."""
        assert QualityLevel.L0.value == "L0"

    def test_l1_value(self) -> None:
        """QualityLevel.L1 has value 'L1'."""
        assert QualityLevel.L1.value == "L1"

    def test_l2_value(self) -> None:
        """QualityLevel.L2 has value 'L2'."""
        assert QualityLevel.L2.value == "L2"

    def test_can_construct_from_string(self) -> None:
        """QualityLevel can be constructed from string value."""
        assert QualityLevel("L1") == QualityLevel.L1

    def test_invalid_level_raises_error(self) -> None:
        """Invalid level string raises ValueError."""
        with pytest.raises(ValueError):
            QualityLevel("L3")


class TestTestRatioCreation:
    """Tests for TestRatio initialization."""

    def test_create_with_all_types(self) -> None:
        """TestRatio can be created with all test types."""
        ratio = TestRatio(positive=5, negative=3, edge_case=2)
        assert ratio.positive == 5
        assert ratio.negative == 3
        assert ratio.edge_case == 2

    def test_create_positive_only(self) -> None:
        """TestRatio can be created with only positive tests."""
        ratio = TestRatio(positive=10, negative=0, edge_case=0)
        assert ratio.positive == 10

    def test_create_balanced(self) -> None:
        """TestRatio can be created with balanced distribution."""
        ratio = TestRatio(positive=10, negative=10, edge_case=10)
        assert ratio.total == 30


class TestTestRatioProperties:
    """Tests for TestRatio computed properties."""

    def test_total_count(self) -> None:
        """total returns sum of all test types."""
        ratio = TestRatio(positive=5, negative=3, edge_case=2)
        assert ratio.total == 10

    def test_positive_percent(self) -> None:
        """positive_percent calculates correctly."""
        ratio = TestRatio(positive=5, negative=3, edge_case=2)
        assert ratio.positive_percent == 50.0

    def test_negative_percent(self) -> None:
        """negative_percent calculates correctly."""
        ratio = TestRatio(positive=5, negative=3, edge_case=2)
        assert ratio.negative_percent == 30.0

    def test_edge_case_percent(self) -> None:
        """edge_case_percent calculates correctly."""
        ratio = TestRatio(positive=5, negative=3, edge_case=2)
        assert ratio.edge_case_percent == 20.0

    def test_percentages_sum_to_hundred(self) -> None:
        """All percentages sum to approximately 100."""
        ratio = TestRatio(positive=5, negative=3, edge_case=2)
        total_percent = (
            ratio.positive_percent
            + ratio.negative_percent
            + ratio.edge_case_percent
        )
        assert total_percent == pytest.approx(100.0)

    def test_percentage_rounding(self) -> None:
        """Percentages are rounded to 2 decimal places."""
        ratio = TestRatio(positive=1, negative=1, edge_case=1)
        # 1/3 = 33.333... -> 33.33
        assert ratio.positive_percent == 33.33


class TestTestRatioQualityLevels:
    """Tests for quality level checking."""

    def test_meets_l0_with_positive_only(self) -> None:
        """L0 requires only positive tests."""
        ratio = TestRatio(positive=5, negative=0, edge_case=0)
        assert ratio.meets_level(QualityLevel.L0) is True

    def test_meets_l1_requires_positive_and_negative(self) -> None:
        """L1 requires positive AND negative tests."""
        ratio = TestRatio(positive=5, negative=3, edge_case=0)
        assert ratio.meets_level(QualityLevel.L1) is True

    def test_fails_l1_without_negative(self) -> None:
        """L1 fails without negative tests."""
        ratio = TestRatio(positive=5, negative=0, edge_case=2)
        assert ratio.meets_level(QualityLevel.L1) is False

    def test_meets_l2_requires_all_types(self) -> None:
        """L2 requires positive, negative, AND edge case tests."""
        ratio = TestRatio(positive=5, negative=3, edge_case=2)
        assert ratio.meets_level(QualityLevel.L2) is True

    def test_fails_l2_without_edge_cases(self) -> None:
        """L2 fails without edge case tests."""
        ratio = TestRatio(positive=5, negative=3, edge_case=0)
        assert ratio.meets_level(QualityLevel.L2) is False

    def test_meets_level_accepts_string(self) -> None:
        """meets_level accepts string level name."""
        ratio = TestRatio(positive=5, negative=3, edge_case=2)
        assert ratio.meets_level("L2") is True

    def test_meets_level_invalid_string_raises(self) -> None:
        """meets_level raises for invalid string level."""
        ratio = TestRatio(positive=5, negative=3, edge_case=2)
        with pytest.raises(ValueError, match="Unknown quality level"):
            ratio.meets_level("L99")


class TestTestRatioHighestLevel:
    """Tests for highest_met_level method."""

    def test_highest_level_l0(self) -> None:
        """highest_met_level returns L0 for positive only."""
        ratio = TestRatio(positive=5, negative=0, edge_case=0)
        assert ratio.highest_met_level() == QualityLevel.L0

    def test_highest_level_l1(self) -> None:
        """highest_met_level returns L1 for positive+negative."""
        ratio = TestRatio(positive=5, negative=3, edge_case=0)
        assert ratio.highest_met_level() == QualityLevel.L1

    def test_highest_level_l2(self) -> None:
        """highest_met_level returns L2 for all types."""
        ratio = TestRatio(positive=5, negative=3, edge_case=2)
        assert ratio.highest_met_level() == QualityLevel.L2


class TestTestRatioStringRepresentation:
    """Tests for string representations."""

    def test_str_format(self) -> None:
        """str() returns compact P:N:E format."""
        ratio = TestRatio(positive=5, negative=3, edge_case=2)
        assert str(ratio) == "P:5/N:3/E:2"

    def test_repr_format(self) -> None:
        """repr() shows constructor form."""
        ratio = TestRatio(positive=5, negative=3, edge_case=2)
        expected = "TestRatio(positive=5, negative=3, edge_case=2)"
        assert repr(ratio) == expected


class TestTestRatioEdgeCases:
    """Edge case tests for TestRatio."""

    def test_minimum_valid_ratio(self) -> None:
        """Minimum valid ratio has exactly one test."""
        ratio = TestRatio(positive=1, negative=0, edge_case=0)
        assert ratio.total == 1

    def test_large_counts(self) -> None:
        """Large test counts are accepted."""
        ratio = TestRatio(positive=1000, negative=500, edge_case=250)
        assert ratio.total == 1750

    def test_immutability(self) -> None:
        """TestRatio is immutable (frozen dataclass)."""
        ratio = TestRatio(positive=5, negative=3, edge_case=2)
        with pytest.raises(FrozenInstanceError):
            ratio.positive = 10  # type: ignore

    def test_hashable(self) -> None:
        """TestRatio can be used as dict key."""
        r1 = TestRatio(positive=5, negative=3, edge_case=2)
        r2 = TestRatio(positive=5, negative=3, edge_case=2)
        ratio_map = {r1: "good"}
        assert ratio_map[r2] == "good"

    def test_equality(self) -> None:
        """TestRatios with same values are equal."""
        r1 = TestRatio(positive=5, negative=3, edge_case=2)
        r2 = TestRatio(positive=5, negative=3, edge_case=2)
        assert r1 == r2

    def test_inequality(self) -> None:
        """TestRatios with different values are not equal."""
        r1 = TestRatio(positive=5, negative=3, edge_case=2)
        r2 = TestRatio(positive=5, negative=4, edge_case=2)
        assert r1 != r2


class TestTestRatioValidation:
    """Negative tests for TestRatio validation."""

    def test_all_zeros_rejected(self) -> None:
        """At least one test is required."""
        with pytest.raises(ValueError, match="At least one test"):
            TestRatio(positive=0, negative=0, edge_case=0)

    def test_negative_positive_rejected(self) -> None:
        """Negative positive count is rejected."""
        with pytest.raises(ValueError, match="non-negative"):
            TestRatio(positive=-1, negative=3, edge_case=2)

    def test_negative_negative_rejected(self) -> None:
        """Negative negative count is rejected."""
        with pytest.raises(ValueError, match="non-negative"):
            TestRatio(positive=5, negative=-1, edge_case=2)

    def test_negative_edge_case_rejected(self) -> None:
        """Negative edge_case count is rejected."""
        with pytest.raises(ValueError, match="non-negative"):
            TestRatio(positive=5, negative=3, edge_case=-1)

    def test_non_integer_positive_rejected(self) -> None:
        """Non-integer positive count is rejected."""
        with pytest.raises(TypeError, match="must be an integer"):
            TestRatio(positive=5.5, negative=3, edge_case=2)  # type: ignore

    def test_non_integer_negative_rejected(self) -> None:
        """Non-integer negative count is rejected."""
        with pytest.raises(TypeError, match="must be an integer"):
            TestRatio(positive=5, negative=3.5, edge_case=2)  # type: ignore

    def test_non_integer_edge_case_rejected(self) -> None:
        """Non-integer edge_case count is rejected."""
        with pytest.raises(TypeError, match="must be an integer"):
            TestRatio(positive=5, negative=3, edge_case=2.5)  # type: ignore

    def test_string_count_rejected(self) -> None:
        """String count is rejected."""
        with pytest.raises(TypeError, match="must be an integer"):
            TestRatio(positive="5", negative=3, edge_case=2)  # type: ignore
