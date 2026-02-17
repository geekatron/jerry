# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Unit tests for work_tracking.domain.value_objects.test_coverage module.

Test Categories:
    - Happy Path: Normal creation and operations
    - Edge Cases: Boundary conditions (0%, 100%)
    - Negative Cases: Validation errors

References:
    - PAT-005-e006: Quality Gate Value Objects
    - Constraint c-004: Code Coverage Requirements
"""

from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest

from src.work_tracking.domain.value_objects.coverage import Coverage


class TestCoverageCreation:
    """Tests for Coverage initialization."""

    def test_create_from_percent(self) -> None:
        """Coverage can be created from percentage value."""
        coverage = Coverage.from_percent(85.5)
        assert coverage.percent == 85.5

    def test_from_percent_rounds_to_two_decimals(self) -> None:
        """from_percent rounds to 2 decimal places."""
        coverage = Coverage.from_percent(85.567)
        assert coverage.percent == 85.57

    def test_create_from_fraction(self) -> None:
        """Coverage can be created from covered/total fraction."""
        coverage = Coverage.from_fraction(85, 100)
        assert coverage.percent == 85.0

    def test_from_fraction_calculates_percentage(self) -> None:
        """from_fraction correctly calculates percentage."""
        coverage = Coverage.from_fraction(7, 10)
        assert coverage.percent == 70.0

    def test_from_fraction_with_decimals(self) -> None:
        """from_fraction rounds to 2 decimal places."""
        coverage = Coverage.from_fraction(1, 3)
        assert coverage.percent == 33.33

    def test_direct_construction(self) -> None:
        """Coverage can be constructed directly."""
        coverage = Coverage(percent=50.0)
        assert coverage.percent == 50.0


class TestCoverageThreshold:
    """Tests for threshold checking methods."""

    def test_meets_threshold_when_above(self) -> None:
        """meets_threshold returns True when coverage exceeds threshold."""
        coverage = Coverage.from_percent(85.0)
        assert coverage.meets_threshold(80.0) is True

    def test_meets_threshold_when_equal(self) -> None:
        """meets_threshold returns True when coverage equals threshold."""
        coverage = Coverage.from_percent(80.0)
        assert coverage.meets_threshold(80.0) is True

    def test_meets_threshold_when_below(self) -> None:
        """meets_threshold returns False when coverage below threshold."""
        coverage = Coverage.from_percent(75.0)
        assert coverage.meets_threshold(80.0) is False

    def test_gap_to_threshold_when_below(self) -> None:
        """gap_to_threshold returns positive gap when below."""
        coverage = Coverage.from_percent(75.0)
        assert coverage.gap_to_threshold(90.0) == 15.0

    def test_gap_to_threshold_when_above(self) -> None:
        """gap_to_threshold returns 0 when at or above threshold."""
        coverage = Coverage.from_percent(95.0)
        assert coverage.gap_to_threshold(90.0) == 0.0

    def test_gap_to_threshold_when_equal(self) -> None:
        """gap_to_threshold returns 0 when exactly at threshold."""
        coverage = Coverage.from_percent(90.0)
        assert coverage.gap_to_threshold(90.0) == 0.0


class TestCoverageComparison:
    """Tests for comparison operations."""

    def test_less_than(self) -> None:
        """Coverage supports < comparison."""
        low = Coverage.from_percent(50.0)
        high = Coverage.from_percent(80.0)
        assert low < high
        assert not high < low

    def test_less_than_or_equal(self) -> None:
        """Coverage supports <= comparison."""
        a = Coverage.from_percent(50.0)
        b = Coverage.from_percent(50.0)
        c = Coverage.from_percent(80.0)
        assert a <= b
        assert a <= c
        assert not c <= a

    def test_greater_than(self) -> None:
        """Coverage supports > comparison."""
        low = Coverage.from_percent(50.0)
        high = Coverage.from_percent(80.0)
        assert high > low
        assert not low > high

    def test_greater_than_or_equal(self) -> None:
        """Coverage supports >= comparison."""
        a = Coverage.from_percent(50.0)
        b = Coverage.from_percent(50.0)
        c = Coverage.from_percent(80.0)
        assert b >= a
        assert c >= a
        assert not a >= c

    def test_equality(self) -> None:
        """Coverage supports equality comparison."""
        a = Coverage.from_percent(75.0)
        b = Coverage.from_percent(75.0)
        assert a == b

    def test_inequality(self) -> None:
        """Coverage supports inequality comparison."""
        a = Coverage.from_percent(75.0)
        b = Coverage.from_percent(80.0)
        assert a != b

    def test_comparison_with_non_coverage_returns_not_implemented(self) -> None:
        """Comparison with non-Coverage returns NotImplemented."""
        coverage = Coverage.from_percent(50.0)
        assert coverage.__lt__(50.0) is NotImplemented
        assert coverage.__le__(50.0) is NotImplemented
        assert coverage.__gt__(50.0) is NotImplemented
        assert coverage.__ge__(50.0) is NotImplemented


class TestCoverageStringRepresentation:
    """Tests for string representations."""

    def test_str_format(self) -> None:
        """str() returns percentage with one decimal."""
        coverage = Coverage.from_percent(85.5)
        assert str(coverage) == "85.5%"

    def test_str_format_whole_number(self) -> None:
        """str() shows .0 for whole numbers."""
        coverage = Coverage.from_percent(80.0)
        assert str(coverage) == "80.0%"

    def test_repr_format(self) -> None:
        """repr() shows constructor form."""
        coverage = Coverage.from_percent(85.5)
        assert repr(coverage) == "Coverage(percent=85.5)"


class TestCoverageEdgeCases:
    """Edge case tests for Coverage."""

    def test_zero_percent(self) -> None:
        """0% is a valid coverage value."""
        coverage = Coverage.from_percent(0.0)
        assert coverage.percent == 0.0

    def test_hundred_percent(self) -> None:
        """100% is a valid coverage value."""
        coverage = Coverage.from_percent(100.0)
        assert coverage.percent == 100.0

    def test_from_fraction_zero_covered(self) -> None:
        """from_fraction handles 0 covered lines."""
        coverage = Coverage.from_fraction(0, 100)
        assert coverage.percent == 0.0

    def test_from_fraction_all_covered(self) -> None:
        """from_fraction handles all lines covered."""
        coverage = Coverage.from_fraction(100, 100)
        assert coverage.percent == 100.0

    def test_from_fraction_zero_total(self) -> None:
        """from_fraction returns 0% for empty file."""
        coverage = Coverage.from_fraction(0, 0)
        assert coverage.percent == 0.0

    def test_immutability(self) -> None:
        """Coverage is immutable (frozen dataclass)."""
        coverage = Coverage.from_percent(50.0)
        with pytest.raises(FrozenInstanceError):
            coverage.percent = 100.0  # type: ignore

    def test_hashable(self) -> None:
        """Coverage can be used as dict key."""
        c1 = Coverage.from_percent(50.0)
        c2 = Coverage.from_percent(50.0)
        coverage_map = {c1: "low"}
        assert coverage_map[c2] == "low"


class TestCoverageValidation:
    """Negative tests for Coverage validation."""

    def test_negative_percent_rejected(self) -> None:
        """Negative percentage is rejected."""
        with pytest.raises(ValueError, match="between 0 and 100"):
            Coverage(percent=-1.0)

    def test_over_hundred_percent_rejected(self) -> None:
        """Percentage over 100 is rejected."""
        with pytest.raises(ValueError, match="between 0 and 100"):
            Coverage(percent=101.0)

    def test_from_percent_negative_rejected(self) -> None:
        """from_percent rejects negative values."""
        with pytest.raises(ValueError, match="between 0 and 100"):
            Coverage.from_percent(-5.0)

    def test_from_percent_over_hundred_rejected(self) -> None:
        """from_percent rejects values over 100."""
        with pytest.raises(ValueError, match="between 0 and 100"):
            Coverage.from_percent(105.0)

    def test_from_fraction_negative_covered_rejected(self) -> None:
        """from_fraction rejects negative covered count."""
        with pytest.raises(ValueError, match="non-negative"):
            Coverage.from_fraction(-1, 100)

    def test_from_fraction_negative_total_rejected(self) -> None:
        """from_fraction rejects negative total count."""
        with pytest.raises(ValueError, match="non-negative"):
            Coverage.from_fraction(50, -1)

    def test_from_fraction_covered_exceeds_total_rejected(self) -> None:
        """from_fraction rejects covered > total."""
        with pytest.raises(ValueError, match="cannot exceed"):
            Coverage.from_fraction(150, 100)

    def test_non_numeric_percent_rejected(self) -> None:
        """Non-numeric percent is rejected."""
        with pytest.raises(TypeError, match="must be a number"):
            Coverage(percent="50%")  # type: ignore

    def test_from_percent_non_numeric_rejected(self) -> None:
        """from_percent rejects non-numeric values."""
        with pytest.raises(TypeError, match="must be a number"):
            Coverage.from_percent("85%")  # type: ignore

    def test_int_percent_accepted(self) -> None:
        """Integer percent is accepted (int is subtype of number)."""
        coverage = Coverage(percent=50)
        assert coverage.percent == 50
