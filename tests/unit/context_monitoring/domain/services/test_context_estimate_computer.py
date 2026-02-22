# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Tests for ContextEstimateComputer domain service."""

from __future__ import annotations

import pytest

from src.context_monitoring.domain.services.context_estimate_computer import (
    ContextEstimateComputer,
)
from src.context_monitoring.domain.value_objects.context_usage_input import (
    ContextUsageInput,
)
from src.context_monitoring.domain.value_objects.rotation_action import RotationAction
from src.context_monitoring.domain.value_objects.threshold_tier import ThresholdTier


def _make_usage(
    *,
    input_tokens: int = 8500,
    cache_creation: int = 5000,
    cache_read: int = 12000,
    window_size: int = 200000,
    session_id: str = "abc123",
    used_pct: float | None = None,
    remaining_pct: float | None = None,
) -> ContextUsageInput:
    """Helper to create ContextUsageInput with sensible defaults."""
    return ContextUsageInput(
        session_id=session_id,
        input_tokens=input_tokens,
        cache_creation_input_tokens=cache_creation,
        cache_read_input_tokens=cache_read,
        context_window_size=window_size,
        used_percentage=used_pct,
        remaining_percentage=remaining_pct,
    )


class TestCompute:
    """Test ContextEstimateComputer.compute()."""

    def test_basic_fill_computation(self) -> None:
        """Computes fill percentage from token counts and window size."""
        computer = ContextEstimateComputer()
        usage = _make_usage(
            input_tokens=50000,
            cache_creation=30000,
            cache_read=60000,
            window_size=200000,
        )
        estimate = computer.compute(usage)
        assert estimate.fill_percentage == pytest.approx(0.70)
        assert estimate.used_tokens == 140000
        assert estimate.window_size == 200000

    def test_token_breakdown_preserved(self) -> None:
        """Fresh, cached, and cache_creation tokens are broken out."""
        computer = ContextEstimateComputer()
        usage = _make_usage(
            input_tokens=8500,
            cache_creation=5000,
            cache_read=12000,
        )
        estimate = computer.compute(usage)
        assert estimate.fresh_tokens == 8500
        assert estimate.cached_tokens == 12000
        assert estimate.cache_creation_tokens == 5000

    def test_is_estimated_false_for_exact_data(self) -> None:
        """Exact Claude Code data sets is_estimated=False."""
        computer = ContextEstimateComputer()
        estimate = computer.compute(_make_usage())
        assert estimate.is_estimated is False

    def test_zero_tokens_uses_claude_code_percentage(self) -> None:
        """When all token counts are 0, falls back to used_percentage."""
        computer = ContextEstimateComputer()
        usage = _make_usage(
            input_tokens=0,
            cache_creation=0,
            cache_read=0,
            used_pct=73.0,
            remaining_pct=27.0,
        )
        estimate = computer.compute(usage)
        assert estimate.fill_percentage == pytest.approx(0.73)

    def test_zero_tokens_no_percentage_gives_zero(self) -> None:
        """When tokens are 0 and no percentage, fill is 0."""
        computer = ContextEstimateComputer()
        usage = _make_usage(
            input_tokens=0,
            cache_creation=0,
            cache_read=0,
        )
        estimate = computer.compute(usage)
        assert estimate.fill_percentage == 0.0

    def test_invalid_window_size_falls_back_to_200k(self) -> None:
        """Zero or negative window size defaults to 200K."""
        computer = ContextEstimateComputer()
        usage = _make_usage(
            window_size=0,
            input_tokens=100000,
            cache_creation=0,
            cache_read=0,
        )
        estimate = computer.compute(usage)
        assert estimate.window_size == 200000
        assert estimate.fill_percentage == pytest.approx(0.5)

    def test_fill_clamped_to_max_1(self) -> None:
        """Fill percentage is clamped to 1.0 maximum."""
        computer = ContextEstimateComputer()
        usage = _make_usage(
            input_tokens=150000,
            cache_creation=100000,
            cache_read=100000,
            window_size=200000,
        )
        estimate = computer.compute(usage)
        assert estimate.fill_percentage == 1.0

    def test_1m_context_window(self) -> None:
        """Supports 1M extended context window (D-015: never hardcode)."""
        computer = ContextEstimateComputer()
        usage = _make_usage(
            input_tokens=200000,
            cache_creation=100000,
            cache_read=200000,
            window_size=1000000,
        )
        estimate = computer.compute(usage)
        assert estimate.fill_percentage == pytest.approx(0.5)
        assert estimate.window_size == 1000000


class TestClassifyTier:
    """Test tier classification at all boundaries."""

    @pytest.mark.parametrize(
        ("fill_pct", "expected_tier"),
        [
            (0.0, ThresholdTier.NOMINAL),
            (0.30, ThresholdTier.NOMINAL),
            (0.54, ThresholdTier.NOMINAL),
            (0.55, ThresholdTier.LOW),
            (0.60, ThresholdTier.LOW),
            (0.69, ThresholdTier.LOW),
            (0.70, ThresholdTier.WARNING),
            (0.75, ThresholdTier.WARNING),
            (0.79, ThresholdTier.WARNING),
            (0.80, ThresholdTier.CRITICAL),
            (0.85, ThresholdTier.CRITICAL),
            (0.87, ThresholdTier.CRITICAL),
            (0.88, ThresholdTier.EMERGENCY),
            (0.95, ThresholdTier.EMERGENCY),
            (1.0, ThresholdTier.EMERGENCY),
        ],
    )
    def test_tier_boundaries(self, fill_pct: float, expected_tier: ThresholdTier) -> None:
        """Tier classification matches 5-tier system at all boundaries."""
        computer = ContextEstimateComputer()
        assert computer.classify_tier(fill_pct) == expected_tier

    def test_custom_thresholds(self) -> None:
        """Custom thresholds override defaults."""
        computer = ContextEstimateComputer(
            thresholds={"nominal": 0.40, "warning": 0.60, "critical": 0.75, "emergency": 0.90}
        )
        assert computer.classify_tier(0.45) == ThresholdTier.LOW
        assert computer.classify_tier(0.65) == ThresholdTier.WARNING
        assert computer.classify_tier(0.80) == ThresholdTier.CRITICAL
        assert computer.classify_tier(0.95) == ThresholdTier.EMERGENCY


class TestDetectCompaction:
    """Test compaction detection logic."""

    def test_no_prior_state(self) -> None:
        """First invocation -- no compaction detected."""
        computer = ContextEstimateComputer()
        result = computer.detect_compaction(
            current_tokens=50000,
            current_session_id="abc123",
            previous_tokens=None,
            previous_session_id=None,
        )
        assert result.detected is False
        assert result.session_id_changed is False

    def test_normal_growth(self) -> None:
        """Tokens growing normally -- no compaction."""
        computer = ContextEstimateComputer()
        result = computer.detect_compaction(
            current_tokens=160000,
            current_session_id="abc123",
            previous_tokens=150000,
            previous_session_id="abc123",
        )
        assert result.detected is False

    def test_compaction_detected_same_session(self) -> None:
        """Large token drop within same session = compaction."""
        computer = ContextEstimateComputer()
        result = computer.detect_compaction(
            current_tokens=46000,
            current_session_id="abc123",
            previous_tokens=180000,
            previous_session_id="abc123",
        )
        assert result.detected is True
        assert result.from_tokens == 180000
        assert result.to_tokens == 46000
        assert result.session_id_changed is False

    def test_session_id_change_is_clear_not_compaction(self) -> None:
        """Session ID change = /clear event, not compaction."""
        computer = ContextEstimateComputer()
        result = computer.detect_compaction(
            current_tokens=5000,
            current_session_id="def456",
            previous_tokens=180000,
            previous_session_id="abc123",
        )
        assert result.detected is False
        assert result.session_id_changed is True

    def test_small_fluctuation_not_compaction(self) -> None:
        """Small token decrease (< threshold) is not compaction."""
        computer = ContextEstimateComputer()
        result = computer.detect_compaction(
            current_tokens=148000,
            current_session_id="abc123",
            previous_tokens=150000,
            previous_session_id="abc123",
        )
        assert result.detected is False

    def test_compaction_threshold_exact_10k_drop_not_detected(self) -> None:
        """Token drop of exactly 10,000 does NOT trigger compaction (must be >10K)."""
        computer = ContextEstimateComputer()
        result = computer.detect_compaction(
            current_tokens=90000,
            current_session_id="abc123",
            previous_tokens=100000,
            previous_session_id="abc123",
        )
        assert result.detected is False

    def test_compaction_large_drop_but_still_above_80pct(self) -> None:
        """Drop > 10K but current >= 80% of previous is NOT compaction."""
        computer = ContextEstimateComputer()
        # 160000 is exactly 80% of 200000, so 160000 >= 200000 * 0.8 → not compaction
        result = computer.detect_compaction(
            current_tokens=160000,
            current_session_id="abc123",
            previous_tokens=200000,
            previous_session_id="abc123",
        )
        assert result.detected is False

    def test_compaction_just_above_both_thresholds(self) -> None:
        """Drop > 10K AND current < 80% of previous IS compaction."""
        computer = ContextEstimateComputer()
        # 159000 < 200000 * 0.8 (160000) AND drop = 41000 > 10000 → compaction
        result = computer.detect_compaction(
            current_tokens=159000,
            current_session_id="abc123",
            previous_tokens=200000,
            previous_session_id="abc123",
        )
        assert result.detected is True
        assert result.from_tokens == 200000
        assert result.to_tokens == 159000


class TestDetermineRotationAction:
    """Test rotation action mapping for all tier x aggressiveness combinations."""

    @pytest.mark.parametrize(
        ("tier", "aggressiveness", "expected_action"),
        [
            # Conservative
            (ThresholdTier.NOMINAL, "conservative", RotationAction.NONE),
            (ThresholdTier.LOW, "conservative", RotationAction.NONE),
            (ThresholdTier.WARNING, "conservative", RotationAction.LOG_WARNING),
            (ThresholdTier.CRITICAL, "conservative", RotationAction.LOG_WARNING),
            (ThresholdTier.EMERGENCY, "conservative", RotationAction.CHECKPOINT),
            # Moderate (default)
            (ThresholdTier.NOMINAL, "moderate", RotationAction.NONE),
            (ThresholdTier.LOW, "moderate", RotationAction.NONE),
            (ThresholdTier.WARNING, "moderate", RotationAction.LOG_WARNING),
            (ThresholdTier.CRITICAL, "moderate", RotationAction.CHECKPOINT),
            (ThresholdTier.EMERGENCY, "moderate", RotationAction.EMERGENCY_HANDOFF),
            # Aggressive
            (ThresholdTier.NOMINAL, "aggressive", RotationAction.NONE),
            (ThresholdTier.LOW, "aggressive", RotationAction.LOG_WARNING),
            (ThresholdTier.WARNING, "aggressive", RotationAction.CHECKPOINT),
            (ThresholdTier.CRITICAL, "aggressive", RotationAction.ROTATE),
            (ThresholdTier.EMERGENCY, "aggressive", RotationAction.EMERGENCY_HANDOFF),
        ],
    )
    def test_rotation_matrix(
        self,
        tier: ThresholdTier,
        aggressiveness: str,
        expected_action: RotationAction,
    ) -> None:
        """Graduated response table matches plan specification."""
        computer = ContextEstimateComputer(aggressiveness=aggressiveness)
        assert computer.determine_rotation_action(tier) == expected_action

    def test_unknown_aggressiveness_falls_back_to_none(self) -> None:
        """Unrecognized aggressiveness mode falls back to RotationAction.NONE."""
        computer = ContextEstimateComputer(aggressiveness="nonexistent")
        for tier in ThresholdTier:
            assert computer.determine_rotation_action(tier) == RotationAction.NONE


class TestNegativeTokenClamping:
    """C4 remediation: negative token values are clamped to [0.0, 1.0]."""

    def test_negative_fill_clamped_to_zero(self) -> None:
        """Negative input_tokens (anomaly) results in fill clamped to 0.0."""
        computer = ContextEstimateComputer()
        usage = _make_usage(
            input_tokens=-5000,
            cache_creation=0,
            cache_read=0,
            window_size=200000,
        )
        estimate = computer.compute(usage)
        assert estimate.fill_percentage == 0.0

    def test_negative_window_size_falls_back_to_200k(self) -> None:
        """Negative window_size defaults to 200K."""
        computer = ContextEstimateComputer()
        usage = _make_usage(
            window_size=-1,
            input_tokens=100000,
            cache_creation=0,
            cache_read=0,
        )
        estimate = computer.compute(usage)
        assert estimate.window_size == 200000


class TestThresholdsProperty:
    """Test thresholds property returns a defensive copy."""

    def test_returns_copy(self) -> None:
        """Modifying the returned dict does not affect the computer."""
        computer = ContextEstimateComputer()
        thresholds = computer.thresholds
        thresholds["nominal"] = 0.99
        assert computer.thresholds["nominal"] == 0.55
