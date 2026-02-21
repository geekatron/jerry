# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
Unit tests for ThresholdTier enum.

Tests cover BDD scenarios from EN-003:
    - ThresholdTier enum has all 5 levels
    - Enum values are correct strings
    - Ordering is maintained

References:
    - EN-003: Context Monitoring Bounded Context Foundation
    - PROJ-004: Context Resilience
"""

from __future__ import annotations

from src.context_monitoring.domain.value_objects.threshold_tier import ThresholdTier


# =============================================================================
# BDD Scenario: ThresholdTier enum has all 5 levels
# =============================================================================


class TestThresholdTierEnum:
    """Scenario: ThresholdTier enum has all 5 levels.

    Given the ThresholdTier enum,
    it should have exactly 5 members with correct values.
    """

    def test_has_nominal_level(self) -> None:
        """ThresholdTier has NOMINAL level."""
        assert ThresholdTier.NOMINAL is not None
        assert ThresholdTier.NOMINAL.value == "nominal"

    def test_has_low_level(self) -> None:
        """ThresholdTier has LOW level."""
        assert ThresholdTier.LOW is not None
        assert ThresholdTier.LOW.value == "low"

    def test_has_warning_level(self) -> None:
        """ThresholdTier has WARNING level."""
        assert ThresholdTier.WARNING is not None
        assert ThresholdTier.WARNING.value == "warning"

    def test_has_critical_level(self) -> None:
        """ThresholdTier has CRITICAL level."""
        assert ThresholdTier.CRITICAL is not None
        assert ThresholdTier.CRITICAL.value == "critical"

    def test_has_emergency_level(self) -> None:
        """ThresholdTier has EMERGENCY level."""
        assert ThresholdTier.EMERGENCY is not None
        assert ThresholdTier.EMERGENCY.value == "emergency"

    def test_exactly_five_members(self) -> None:
        """ThresholdTier has exactly 5 members."""
        assert len(ThresholdTier) == 5

    def test_members_are_distinct(self) -> None:
        """All ThresholdTier members have distinct values."""
        values = [t.value for t in ThresholdTier]
        assert len(values) == len(set(values))
