# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Unit tests for Priority value object.

Test Categories:
    - Enum Values: Correct values and ordering
    - Parsing: from_string and from_int factory methods
    - Properties: is_high_priority, is_low_priority

References:
    - IMPL-005: WorkItem Aggregate (Priority is a supporting VO)
    - impl-es-e-006-workitem-schema: Priority specification
"""

from __future__ import annotations

import pytest

from src.work_tracking.domain.value_objects import Priority

# =============================================================================
# Enum Value Tests
# =============================================================================


class TestPriorityValues:
    """Tests for Priority enum values."""

    def test_critical_value(self) -> None:
        """CRITICAL has value 1."""
        assert Priority.CRITICAL.value == 1

    def test_high_value(self) -> None:
        """HIGH has value 2."""
        assert Priority.HIGH.value == 2

    def test_medium_value(self) -> None:
        """MEDIUM has value 3."""
        assert Priority.MEDIUM.value == 3

    def test_low_value(self) -> None:
        """LOW has value 4."""
        assert Priority.LOW.value == 4

    def test_has_four_priorities(self) -> None:
        """There are exactly 4 priority levels."""
        assert len(Priority) == 4


# =============================================================================
# Ordering Tests
# =============================================================================


class TestPriorityOrdering:
    """Tests for Priority ordering (IntEnum behavior)."""

    def test_critical_less_than_high(self) -> None:
        """CRITICAL < HIGH (higher priority = lower value)."""
        assert Priority.CRITICAL < Priority.HIGH

    def test_high_less_than_medium(self) -> None:
        """HIGH < MEDIUM."""
        assert Priority.HIGH < Priority.MEDIUM

    def test_medium_less_than_low(self) -> None:
        """MEDIUM < LOW."""
        assert Priority.MEDIUM < Priority.LOW

    def test_sorting(self) -> None:
        """Priorities sort correctly."""
        priorities = [Priority.LOW, Priority.CRITICAL, Priority.MEDIUM, Priority.HIGH]
        sorted_priorities = sorted(priorities)
        assert sorted_priorities == [
            Priority.CRITICAL,
            Priority.HIGH,
            Priority.MEDIUM,
            Priority.LOW,
        ]


# =============================================================================
# Parsing Tests - from_string
# =============================================================================


class TestPriorityFromString:
    """Tests for Priority.from_string() factory method."""

    def test_parse_critical(self) -> None:
        """Parse 'critical' string."""
        assert Priority.from_string("critical") == Priority.CRITICAL

    def test_parse_high(self) -> None:
        """Parse 'high' string."""
        assert Priority.from_string("high") == Priority.HIGH

    def test_parse_medium(self) -> None:
        """Parse 'medium' string."""
        assert Priority.from_string("medium") == Priority.MEDIUM

    def test_parse_low(self) -> None:
        """Parse 'low' string."""
        assert Priority.from_string("low") == Priority.LOW

    def test_parse_uppercase(self) -> None:
        """Parse uppercase strings."""
        assert Priority.from_string("CRITICAL") == Priority.CRITICAL
        assert Priority.from_string("HIGH") == Priority.HIGH

    def test_parse_mixed_case(self) -> None:
        """Parse mixed case strings."""
        assert Priority.from_string("Critical") == Priority.CRITICAL
        assert Priority.from_string("HiGh") == Priority.HIGH

    def test_parse_with_whitespace(self) -> None:
        """Parse strings with whitespace."""
        assert Priority.from_string("  high  ") == Priority.HIGH

    def test_unknown_returns_medium(self) -> None:
        """Unknown string returns MEDIUM as default."""
        assert Priority.from_string("unknown") == Priority.MEDIUM
        assert Priority.from_string("urgent") == Priority.MEDIUM
        assert Priority.from_string("") == Priority.MEDIUM


# =============================================================================
# Parsing Tests - from_int
# =============================================================================


class TestPriorityFromInt:
    """Tests for Priority.from_int() factory method."""

    def test_from_int_1(self) -> None:
        """Integer 1 maps to CRITICAL."""
        assert Priority.from_int(1) == Priority.CRITICAL

    def test_from_int_2(self) -> None:
        """Integer 2 maps to HIGH."""
        assert Priority.from_int(2) == Priority.HIGH

    def test_from_int_3(self) -> None:
        """Integer 3 maps to MEDIUM."""
        assert Priority.from_int(3) == Priority.MEDIUM

    def test_from_int_4(self) -> None:
        """Integer 4 maps to LOW."""
        assert Priority.from_int(4) == Priority.LOW

    def test_invalid_int_raises(self) -> None:
        """Invalid integer raises ValueError."""
        with pytest.raises(ValueError, match="Invalid priority value"):
            Priority.from_int(0)

    def test_out_of_range_raises(self) -> None:
        """Out of range integer raises ValueError."""
        with pytest.raises(ValueError, match="Invalid priority value: 5"):
            Priority.from_int(5)

    def test_negative_raises(self) -> None:
        """Negative integer raises ValueError."""
        with pytest.raises(ValueError):
            Priority.from_int(-1)


# =============================================================================
# Property Tests
# =============================================================================


class TestPriorityProperties:
    """Tests for Priority properties."""

    def test_critical_is_high_priority(self) -> None:
        """CRITICAL is high priority."""
        assert Priority.CRITICAL.is_high_priority is True

    def test_high_is_high_priority(self) -> None:
        """HIGH is high priority."""
        assert Priority.HIGH.is_high_priority is True

    def test_medium_is_not_high_priority(self) -> None:
        """MEDIUM is not high priority."""
        assert Priority.MEDIUM.is_high_priority is False

    def test_low_is_not_high_priority(self) -> None:
        """LOW is not high priority."""
        assert Priority.LOW.is_high_priority is False

    def test_low_is_low_priority(self) -> None:
        """LOW is low priority."""
        assert Priority.LOW.is_low_priority is True

    def test_medium_is_not_low_priority(self) -> None:
        """MEDIUM is not low priority."""
        assert Priority.MEDIUM.is_low_priority is False

    def test_high_is_not_low_priority(self) -> None:
        """HIGH is not low priority."""
        assert Priority.HIGH.is_low_priority is False

    def test_critical_is_not_low_priority(self) -> None:
        """CRITICAL is not low priority."""
        assert Priority.CRITICAL.is_low_priority is False


# =============================================================================
# String Representation Tests
# =============================================================================


class TestPriorityStringRepresentation:
    """Tests for Priority string representations."""

    def test_str_critical(self) -> None:
        """str(CRITICAL) returns 'critical'."""
        assert str(Priority.CRITICAL) == "critical"

    def test_str_high(self) -> None:
        """str(HIGH) returns 'high'."""
        assert str(Priority.HIGH) == "high"

    def test_str_medium(self) -> None:
        """str(MEDIUM) returns 'medium'."""
        assert str(Priority.MEDIUM) == "medium"

    def test_str_low(self) -> None:
        """str(LOW) returns 'low'."""
        assert str(Priority.LOW) == "low"

    def test_repr(self) -> None:
        """repr includes class name."""
        assert repr(Priority.HIGH) == "Priority.HIGH"


# =============================================================================
# Edge Case Tests
# =============================================================================


class TestPriorityEdgeCases:
    """Edge case tests for Priority."""

    def test_equality(self) -> None:
        """Same priority values are equal."""
        assert Priority.HIGH == Priority.HIGH

    def test_inequality(self) -> None:
        """Different priority values are not equal."""
        assert Priority.HIGH != Priority.LOW

    def test_hashable(self) -> None:
        """Priority values can be used in sets."""
        priority_set = {Priority.HIGH, Priority.LOW, Priority.HIGH}
        assert len(priority_set) == 2

    def test_comparable_to_int(self) -> None:
        """Priority values can be compared to integers."""
        assert Priority.HIGH == 2
        assert Priority.CRITICAL < 2
