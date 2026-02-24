# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Tests for ContextUsageInput value object."""

from __future__ import annotations

import pytest

from src.context_monitoring.domain.value_objects.context_usage_input import (
    ContextUsageInput,
)


class TestContextUsageInput:
    """Test ContextUsageInput creation and computed properties."""

    def test_total_context_tokens_sums_all_inputs(self) -> None:
        """Total context tokens = input + cache_creation + cache_read."""
        usage = ContextUsageInput(
            session_id="abc123",
            input_tokens=8500,
            cache_creation_input_tokens=5000,
            cache_read_input_tokens=12000,
            context_window_size=200000,
        )
        assert usage.total_context_tokens == 25500

    def test_total_context_tokens_zero_when_all_zero(self) -> None:
        """Total is zero before first API call."""
        usage = ContextUsageInput(
            session_id="abc123",
            input_tokens=0,
            cache_creation_input_tokens=0,
            cache_read_input_tokens=0,
            context_window_size=200000,
        )
        assert usage.total_context_tokens == 0

    def test_frozen_immutability(self) -> None:
        """ContextUsageInput is frozen/immutable."""
        usage = ContextUsageInput(
            session_id="abc123",
            input_tokens=100,
            cache_creation_input_tokens=0,
            cache_read_input_tokens=0,
            context_window_size=200000,
        )
        with pytest.raises(AttributeError):
            usage.input_tokens = 999  # type: ignore[misc]

    def test_optional_percentages_default_none(self) -> None:
        """used_percentage and remaining_percentage default to None."""
        usage = ContextUsageInput(
            session_id="abc123",
            input_tokens=100,
            cache_creation_input_tokens=0,
            cache_read_input_tokens=0,
            context_window_size=200000,
        )
        assert usage.used_percentage is None
        assert usage.remaining_percentage is None

    def test_percentages_when_provided(self) -> None:
        """Explicit percentages are preserved."""
        usage = ContextUsageInput(
            session_id="abc123",
            input_tokens=100,
            cache_creation_input_tokens=0,
            cache_read_input_tokens=0,
            context_window_size=200000,
            used_percentage=73.0,
            remaining_percentage=27.0,
        )
        assert usage.used_percentage == 73.0
        assert usage.remaining_percentage == 27.0

    def test_large_context_window_1m(self) -> None:
        """Supports 1M extended context window."""
        usage = ContextUsageInput(
            session_id="abc123",
            input_tokens=500000,
            cache_creation_input_tokens=100000,
            cache_read_input_tokens=200000,
            context_window_size=1000000,
        )
        assert usage.total_context_tokens == 800000
        assert usage.context_window_size == 1000000
