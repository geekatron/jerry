# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
Unit tests for ContextState value object.

Tests cover BDD scenarios from EN-003:
    - ContextState construction with required fields
    - ContextState construction with optional compaction_count
    - ContextState is immutable

References:
    - EN-003: Context Monitoring Bounded Context Foundation
    - PROJ-004: Context Resilience
"""

from __future__ import annotations

import pytest

from src.context_monitoring.domain.value_objects.context_state import ContextState
from src.context_monitoring.domain.value_objects.threshold_tier import ThresholdTier


# =============================================================================
# BDD Scenario: ContextState construction
# =============================================================================


class TestContextStateConstruction:
    """Scenario: ContextState construction.

    Given valid parameters,
    ContextState should store fill_percentage, tier, and compaction_count.
    """

    def test_construction_with_required_fields(self) -> None:
        """ContextState can be constructed with required fields only."""
        state = ContextState(fill_percentage=0.6, tier=ThresholdTier.LOW)
        assert state.fill_percentage == 0.6
        assert state.tier == ThresholdTier.LOW
        assert state.compaction_count == 0

    def test_construction_with_compaction_count(self) -> None:
        """ContextState stores compaction_count."""
        state = ContextState(
            fill_percentage=0.85,
            tier=ThresholdTier.CRITICAL,
            compaction_count=2,
        )
        assert state.compaction_count == 2

    def test_compaction_count_default_zero(self) -> None:
        """ContextState compaction_count defaults to 0."""
        state = ContextState(fill_percentage=0.3, tier=ThresholdTier.NOMINAL)
        assert state.compaction_count == 0


# =============================================================================
# BDD Scenario: ContextState is immutable
# =============================================================================


class TestContextStateImmutability:
    """Scenario: ContextState is immutable.

    Given a ContextState value object,
    it should be a frozen dataclass that cannot be mutated.
    """

    def test_cannot_mutate_fill_percentage(self) -> None:
        """ContextState.fill_percentage cannot be changed."""
        state = ContextState(fill_percentage=0.5, tier=ThresholdTier.NOMINAL)
        with pytest.raises(AttributeError):
            state.fill_percentage = 0.9  # type: ignore[misc]

    def test_cannot_mutate_tier(self) -> None:
        """ContextState.tier cannot be changed."""
        state = ContextState(fill_percentage=0.5, tier=ThresholdTier.NOMINAL)
        with pytest.raises(AttributeError):
            state.tier = ThresholdTier.EMERGENCY  # type: ignore[misc]

    def test_cannot_mutate_compaction_count(self) -> None:
        """ContextState.compaction_count cannot be changed."""
        state = ContextState(fill_percentage=0.5, tier=ThresholdTier.NOMINAL)
        with pytest.raises(AttributeError):
            state.compaction_count = 5  # type: ignore[misc]

    def test_equality(self) -> None:
        """Two ContextState instances with same values are equal."""
        a = ContextState(fill_percentage=0.5, tier=ThresholdTier.NOMINAL, compaction_count=1)
        b = ContextState(fill_percentage=0.5, tier=ThresholdTier.NOMINAL, compaction_count=1)
        assert a == b
