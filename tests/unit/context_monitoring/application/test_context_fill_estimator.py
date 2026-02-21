# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
Unit tests for ContextFillEstimator.

Tests cover BDD scenarios from EN-004:
    - Tier classification across all 5 threshold boundaries
    - Fail-open on FileNotFoundError
    - Fail-open on ValueError
    - Fail-open on generic Exception
    - XML tag generation for each tier
    - XML tag token count within bounds (40-200 tokens)
    - Monitoring disabled returns NOMINAL

References:
    - EN-004: ContextFillEstimator and ResumptionContextGenerator
    - PROJ-004: Context Resilience
"""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from src.context_monitoring.application.ports.transcript_reader import ITranscriptReader
from src.context_monitoring.application.services.context_fill_estimator import (
    ContextFillEstimator,
)
from src.context_monitoring.domain.value_objects.fill_estimate import FillEstimate
from src.context_monitoring.domain.value_objects.threshold_tier import ThresholdTier


# =============================================================================
# Helpers / Fakes
# =============================================================================


class FakeThresholdConfiguration:
    """Fake IThresholdConfiguration with default thresholds."""

    def __init__(self, *, enabled: bool = True) -> None:
        """Initialize with optional enabled flag."""
        self._enabled = enabled
        self._thresholds = {
            "nominal": 0.55,
            "warning": 0.70,
            "critical": 0.80,
            "emergency": 0.88,
        }

    def get_threshold(self, tier: str) -> float:
        """Return threshold for the given tier."""
        return self._thresholds[tier.lower()]

    def is_enabled(self) -> bool:
        """Return whether monitoring is enabled."""
        return self._enabled

    def get_compaction_detection_threshold(self) -> int:
        """Return compaction detection threshold."""
        return 10000

    def get_all_thresholds(self) -> dict[str, float]:
        """Return all thresholds."""
        return dict(self._thresholds)


class FakeTranscriptReader:
    """Fake ITranscriptReader that returns a fixed token count."""

    def __init__(self, token_count: int) -> None:
        """Initialize with a fixed token count to return."""
        self._token_count = token_count

    def read_latest_tokens(self, transcript_path: str) -> int:
        """Return the fixed token count."""
        return self._token_count


class FailingTranscriptReader:
    """Fake ITranscriptReader that raises on read."""

    def __init__(self, exc: Exception) -> None:
        """Initialize with the exception to raise."""
        self._exc = exc

    def read_latest_tokens(self, transcript_path: str) -> int:
        """Raise the configured exception."""
        raise self._exc


# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture()
def config() -> FakeThresholdConfiguration:
    """Return a default FakeThresholdConfiguration (enabled)."""
    return FakeThresholdConfiguration()


@pytest.fixture()
def disabled_config() -> FakeThresholdConfiguration:
    """Return a FakeThresholdConfiguration with monitoring disabled."""
    return FakeThresholdConfiguration(enabled=False)


# =============================================================================
# BDD Scenario: Tier classification across all 5 boundaries
# =============================================================================


class TestTierClassification:
    """Scenario: ContextFillEstimator classifies fill percentage into correct tier.

    Given a token count that maps to a specific fill percentage,
    the estimator should return the correct ThresholdTier.
    """

    @pytest.mark.parametrize(
        ("token_count", "context_window", "expected_tier"),
        [
            # NOMINAL: fill < 0.55
            (100_000, 200_000, ThresholdTier.NOMINAL),   # 0.50 < 0.55
            (10_000, 200_000, ThresholdTier.NOMINAL),    # 0.05 < 0.55
            # LOW: 0.55 <= fill < 0.70
            (110_000, 200_000, ThresholdTier.LOW),       # 0.55 exactly
            (130_000, 200_000, ThresholdTier.LOW),       # 0.65
            # WARNING: 0.70 <= fill < 0.80
            (140_000, 200_000, ThresholdTier.WARNING),   # 0.70 exactly
            (150_000, 200_000, ThresholdTier.WARNING),   # 0.75
            # CRITICAL: 0.80 <= fill < 0.88
            (160_000, 200_000, ThresholdTier.CRITICAL),  # 0.80 exactly
            (170_000, 200_000, ThresholdTier.CRITICAL),  # 0.85
            # EMERGENCY: fill >= 0.88
            (176_000, 200_000, ThresholdTier.EMERGENCY), # 0.88 exactly
            (190_000, 200_000, ThresholdTier.EMERGENCY), # 0.95
        ],
    )
    def test_tier_from_token_count(
        self,
        token_count: int,
        context_window: int,
        expected_tier: ThresholdTier,
        config: FakeThresholdConfiguration,
    ) -> None:
        """Estimator classifies token count into expected tier."""
        reader = FakeTranscriptReader(token_count=token_count)
        estimator = ContextFillEstimator(reader=reader, threshold_config=config)
        result = estimator.estimate(
            transcript_path="/fake/transcript.jsonl",
            context_window=context_window,
        )
        assert result.tier == expected_tier

    def test_estimate_returns_fill_estimate(
        self, config: FakeThresholdConfiguration
    ) -> None:
        """estimate() returns a FillEstimate instance."""
        reader = FakeTranscriptReader(token_count=100_000)
        estimator = ContextFillEstimator(reader=reader, threshold_config=config)
        result = estimator.estimate("/fake/path.jsonl")
        assert isinstance(result, FillEstimate)

    def test_estimate_sets_token_count(
        self, config: FakeThresholdConfiguration
    ) -> None:
        """estimate() includes token_count in the result."""
        reader = FakeTranscriptReader(token_count=144_000)
        estimator = ContextFillEstimator(reader=reader, threshold_config=config)
        result = estimator.estimate("/fake/path.jsonl", context_window=200_000)
        assert result.token_count == 144_000

    def test_estimate_sets_fill_percentage(
        self, config: FakeThresholdConfiguration
    ) -> None:
        """estimate() correctly computes fill_percentage."""
        reader = FakeTranscriptReader(token_count=100_000)
        estimator = ContextFillEstimator(reader=reader, threshold_config=config)
        result = estimator.estimate("/fake/path.jsonl", context_window=200_000)
        assert abs(result.fill_percentage - 0.5) < 1e-9


# =============================================================================
# BDD Scenario: Fail-open on exceptions from ITranscriptReader
# =============================================================================


class TestFailOpen:
    """Scenario: ContextFillEstimator is fail-open on reader exceptions.

    Given a reader that raises any exception,
    the estimator should return NOMINAL FillEstimate without propagating.
    """

    def test_fail_open_on_file_not_found(
        self, config: FakeThresholdConfiguration
    ) -> None:
        """Returns NOMINAL FillEstimate when reader raises FileNotFoundError."""
        reader = FailingTranscriptReader(FileNotFoundError("no file"))
        estimator = ContextFillEstimator(reader=reader, threshold_config=config)
        result = estimator.estimate("/fake/missing.jsonl")
        assert result.tier == ThresholdTier.NOMINAL
        assert result.fill_percentage == 0.0
        assert result.token_count is None

    def test_fail_open_on_value_error(
        self, config: FakeThresholdConfiguration
    ) -> None:
        """Returns NOMINAL FillEstimate when reader raises ValueError."""
        reader = FailingTranscriptReader(ValueError("empty file"))
        estimator = ContextFillEstimator(reader=reader, threshold_config=config)
        result = estimator.estimate("/fake/empty.jsonl")
        assert result.tier == ThresholdTier.NOMINAL
        assert result.fill_percentage == 0.0
        assert result.token_count is None

    def test_fail_open_on_generic_exception(
        self, config: FakeThresholdConfiguration
    ) -> None:
        """Returns NOMINAL FillEstimate when reader raises a generic Exception."""
        reader = FailingTranscriptReader(RuntimeError("unexpected error"))
        estimator = ContextFillEstimator(reader=reader, threshold_config=config)
        result = estimator.estimate("/fake/broken.jsonl")
        assert result.tier == ThresholdTier.NOMINAL
        assert result.fill_percentage == 0.0
        assert result.token_count is None

    def test_fail_open_does_not_propagate_exception(
        self, config: FakeThresholdConfiguration
    ) -> None:
        """No exception propagates from estimate() on reader failure."""
        reader = FailingTranscriptReader(OSError("disk error"))
        estimator = ContextFillEstimator(reader=reader, threshold_config=config)
        # Should not raise
        result = estimator.estimate("/fake/path.jsonl")
        assert result is not None


# =============================================================================
# BDD Scenario: Monitoring disabled returns NOMINAL
# =============================================================================


class TestMonitoringDisabled:
    """Scenario: When monitoring is disabled, estimate always returns NOMINAL."""

    def test_disabled_returns_nominal(
        self, disabled_config: FakeThresholdConfiguration
    ) -> None:
        """When is_enabled() returns False, result is NOMINAL fill=0.0."""
        reader = FakeTranscriptReader(token_count=190_000)
        estimator = ContextFillEstimator(reader=reader, threshold_config=disabled_config)
        result = estimator.estimate("/fake/path.jsonl", context_window=200_000)
        assert result.tier == ThresholdTier.NOMINAL
        assert result.fill_percentage == 0.0
        assert result.token_count is None

    def test_disabled_reader_never_called(
        self, disabled_config: FakeThresholdConfiguration
    ) -> None:
        """When disabled, the reader is not invoked."""
        mock_reader = MagicMock(spec=ITranscriptReader)
        estimator = ContextFillEstimator(
            reader=mock_reader, threshold_config=disabled_config
        )
        estimator.estimate("/fake/path.jsonl")
        mock_reader.read_latest_tokens.assert_not_called()


# =============================================================================
# BDD Scenario: XML context monitor tag generation
# =============================================================================


class TestGenerateContextMonitorTag:
    """Scenario: generate_context_monitor_tag produces valid XML per tier.

    Given a FillEstimate, the estimator generates an XML <context-monitor> tag
    with appropriate action text for the tier.
    """

    @pytest.mark.parametrize(
        ("tier", "expected_action_fragment"),
        [
            (ThresholdTier.NOMINAL, "No action needed"),
            (ThresholdTier.LOW, "Monitor usage"),
            (ThresholdTier.WARNING, "Consider checkpointing"),
            (ThresholdTier.CRITICAL, "Checkpoint recommended"),
            (ThresholdTier.EMERGENCY, "Immediate checkpoint required"),
        ],
    )
    def test_action_text_per_tier(
        self,
        tier: ThresholdTier,
        expected_action_fragment: str,
        config: FakeThresholdConfiguration,
    ) -> None:
        """Action text contains tier-appropriate phrasing."""
        reader = FakeTranscriptReader(token_count=100_000)
        estimator = ContextFillEstimator(reader=reader, threshold_config=config)
        estimate = FillEstimate(
            fill_percentage=0.5, tier=tier, token_count=100_000
        )
        tag = estimator.generate_context_monitor_tag(estimate)
        assert expected_action_fragment in tag

    def test_tag_contains_fill_percentage(
        self, config: FakeThresholdConfiguration
    ) -> None:
        """Generated tag includes fill-percentage element."""
        reader = FakeTranscriptReader(token_count=144_000)
        estimator = ContextFillEstimator(reader=reader, threshold_config=config)
        estimate = FillEstimate(
            fill_percentage=0.72, tier=ThresholdTier.WARNING, token_count=144_000
        )
        tag = estimator.generate_context_monitor_tag(estimate)
        assert "<fill-percentage>" in tag
        assert "0.72" in tag

    def test_tag_contains_tier(
        self, config: FakeThresholdConfiguration
    ) -> None:
        """Generated tag includes tier element."""
        reader = FakeTranscriptReader(token_count=144_000)
        estimator = ContextFillEstimator(reader=reader, threshold_config=config)
        estimate = FillEstimate(
            fill_percentage=0.72, tier=ThresholdTier.WARNING, token_count=144_000
        )
        tag = estimator.generate_context_monitor_tag(estimate)
        assert "<tier>" in tag
        assert "WARNING" in tag

    def test_tag_contains_token_count(
        self, config: FakeThresholdConfiguration
    ) -> None:
        """Generated tag includes token-count element when token_count is set."""
        reader = FakeTranscriptReader(token_count=144_000)
        estimator = ContextFillEstimator(reader=reader, threshold_config=config)
        estimate = FillEstimate(
            fill_percentage=0.72, tier=ThresholdTier.WARNING, token_count=144_000
        )
        tag = estimator.generate_context_monitor_tag(estimate)
        assert "<token-count>" in tag
        assert "144000" in tag

    def test_tag_within_token_budget(
        self, config: FakeThresholdConfiguration
    ) -> None:
        """Generated tag is between 40 and 200 tokens (approx via len/4)."""
        reader = FakeTranscriptReader(token_count=144_000)
        estimator = ContextFillEstimator(reader=reader, threshold_config=config)
        estimate = FillEstimate(
            fill_percentage=0.72, tier=ThresholdTier.WARNING, token_count=144_000
        )
        tag = estimator.generate_context_monitor_tag(estimate)
        approx_tokens = len(tag) / 4
        assert 40 <= approx_tokens <= 200

    def test_tag_is_valid_xml_structure(
        self, config: FakeThresholdConfiguration
    ) -> None:
        """Generated tag starts with <context-monitor> and ends with closing tag."""
        reader = FakeTranscriptReader(token_count=100_000)
        estimator = ContextFillEstimator(reader=reader, threshold_config=config)
        estimate = FillEstimate(
            fill_percentage=0.5, tier=ThresholdTier.NOMINAL, token_count=100_000
        )
        tag = estimator.generate_context_monitor_tag(estimate)
        assert tag.strip().startswith("<context-monitor>")
        assert tag.strip().endswith("</context-monitor>")

    def test_tag_with_none_token_count(
        self, config: FakeThresholdConfiguration
    ) -> None:
        """Tag handles None token_count gracefully."""
        reader = FakeTranscriptReader(token_count=100_000)
        estimator = ContextFillEstimator(reader=reader, threshold_config=config)
        estimate = FillEstimate(
            fill_percentage=0.5, tier=ThresholdTier.NOMINAL, token_count=None
        )
        tag = estimator.generate_context_monitor_tag(estimate)
        assert "<context-monitor>" in tag
        # Should not raise
