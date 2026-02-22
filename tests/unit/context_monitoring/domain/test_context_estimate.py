# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Tests for ContextEstimate value object."""

from __future__ import annotations

import pytest

from src.context_monitoring.domain.value_objects.context_estimate import (
    ContextEstimate,
)
from src.context_monitoring.domain.value_objects.threshold_tier import ThresholdTier


class TestContextEstimate:
    """Test ContextEstimate value object."""

    def test_creation_with_all_fields(self) -> None:
        """ContextEstimate stores all domain-computed fields."""
        estimate = ContextEstimate(
            fill_percentage=0.73,
            used_tokens=146000,
            window_size=200000,
            tier=ThresholdTier.WARNING,
            is_estimated=False,
            fresh_tokens=8500,
            cached_tokens=45200,
            cache_creation_tokens=12000,
        )
        assert estimate.fill_percentage == 0.73
        assert estimate.used_tokens == 146000
        assert estimate.window_size == 200000
        assert estimate.tier == ThresholdTier.WARNING
        assert estimate.is_estimated is False
        assert estimate.fresh_tokens == 8500
        assert estimate.cached_tokens == 45200
        assert estimate.cache_creation_tokens == 12000

    def test_frozen_immutability(self) -> None:
        """ContextEstimate is frozen/immutable."""
        estimate = ContextEstimate(
            fill_percentage=0.5,
            used_tokens=100000,
            window_size=200000,
            tier=ThresholdTier.NOMINAL,
            is_estimated=False,
            fresh_tokens=5000,
            cached_tokens=0,
            cache_creation_tokens=0,
        )
        with pytest.raises(AttributeError):
            estimate.fill_percentage = 0.99  # type: ignore[misc]

    def test_estimated_flag_true_for_transcript_fallback(self) -> None:
        """is_estimated=True when using transcript-based estimation."""
        estimate = ContextEstimate(
            fill_percentage=0.5,
            used_tokens=100000,
            window_size=200000,
            tier=ThresholdTier.NOMINAL,
            is_estimated=True,
            fresh_tokens=0,
            cached_tokens=0,
            cache_creation_tokens=0,
        )
        assert estimate.is_estimated is True
