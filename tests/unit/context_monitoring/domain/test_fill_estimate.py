# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
Unit tests for FillEstimate value object.

Tests cover BDD scenarios from EN-003:
    - FillEstimate is immutable (frozen dataclass)
    - Construction with required fields
    - Optional token_count field

References:
    - EN-003: Context Monitoring Bounded Context Foundation
    - PROJ-004: Context Resilience
"""

from __future__ import annotations

import pytest

from src.context_monitoring.domain.value_objects.fill_estimate import FillEstimate
from src.context_monitoring.domain.value_objects.threshold_tier import ThresholdTier


# =============================================================================
# BDD Scenario: FillEstimate is immutable
# =============================================================================


class TestFillEstimateImmutability:
    """Scenario: FillEstimate is immutable.

    Given a FillEstimate value object,
    it should be a frozen dataclass that cannot be mutated.
    """

    def test_cannot_mutate_fill_percentage(self) -> None:
        """FillEstimate.fill_percentage cannot be changed after creation."""
        estimate = FillEstimate(fill_percentage=0.5, tier=ThresholdTier.NOMINAL)
        with pytest.raises(AttributeError):
            estimate.fill_percentage = 0.9  # type: ignore[misc]

    def test_cannot_mutate_tier(self) -> None:
        """FillEstimate.tier cannot be changed after creation."""
        estimate = FillEstimate(fill_percentage=0.5, tier=ThresholdTier.NOMINAL)
        with pytest.raises(AttributeError):
            estimate.tier = ThresholdTier.CRITICAL  # type: ignore[misc]

    def test_cannot_mutate_token_count(self) -> None:
        """FillEstimate.token_count cannot be changed after creation."""
        estimate = FillEstimate(
            fill_percentage=0.5, tier=ThresholdTier.NOMINAL, token_count=50000
        )
        with pytest.raises(AttributeError):
            estimate.token_count = 100000  # type: ignore[misc]


# =============================================================================
# BDD Scenario: FillEstimate construction
# =============================================================================


class TestFillEstimateConstruction:
    """Scenario: FillEstimate construction with required and optional fields.

    Given valid parameters,
    FillEstimate should be constructed with correct values.
    """

    def test_construction_with_required_fields(self) -> None:
        """FillEstimate can be constructed with required fields only."""
        estimate = FillEstimate(fill_percentage=0.65, tier=ThresholdTier.WARNING)
        assert estimate.fill_percentage == 0.65
        assert estimate.tier == ThresholdTier.WARNING
        assert estimate.token_count is None

    def test_construction_with_token_count(self) -> None:
        """FillEstimate can be constructed with optional token_count."""
        estimate = FillEstimate(
            fill_percentage=0.85,
            tier=ThresholdTier.CRITICAL,
            token_count=170000,
        )
        assert estimate.fill_percentage == 0.85
        assert estimate.tier == ThresholdTier.CRITICAL
        assert estimate.token_count == 170000

    def test_equality(self) -> None:
        """Two FillEstimate instances with same values are equal."""
        a = FillEstimate(fill_percentage=0.5, tier=ThresholdTier.NOMINAL, token_count=100000)
        b = FillEstimate(fill_percentage=0.5, tier=ThresholdTier.NOMINAL, token_count=100000)
        assert a == b

    def test_inequality(self) -> None:
        """Two FillEstimate instances with different values are not equal."""
        a = FillEstimate(fill_percentage=0.5, tier=ThresholdTier.NOMINAL)
        b = FillEstimate(fill_percentage=0.8, tier=ThresholdTier.CRITICAL)
        assert a != b
