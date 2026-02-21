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

    def __init__(
        self,
        *,
        enabled: bool = True,
        context_window_tokens: int = 200_000,
        context_window_source: str = "default",
    ) -> None:
        """Initialize with optional enabled flag and context window."""
        self._enabled = enabled
        self._context_window_tokens = context_window_tokens
        self._context_window_source = context_window_source
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

    def get_context_window_tokens(self) -> int:
        """Return context window size in tokens."""
        return self._context_window_tokens

    def get_context_window_source(self) -> str:
        """Return context window source."""
        return self._context_window_source


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
        ("token_count", "expected_tier"),
        [
            # NOMINAL: fill < 0.55  (200K default window)
            (100_000, ThresholdTier.NOMINAL),  # 0.50 < 0.55
            (10_000, ThresholdTier.NOMINAL),  # 0.05 < 0.55
            # LOW: 0.55 <= fill < 0.70
            (110_000, ThresholdTier.LOW),  # 0.55 exactly
            (130_000, ThresholdTier.LOW),  # 0.65
            # WARNING: 0.70 <= fill < 0.80
            (140_000, ThresholdTier.WARNING),  # 0.70 exactly
            (150_000, ThresholdTier.WARNING),  # 0.75
            # CRITICAL: 0.80 <= fill < 0.88
            (160_000, ThresholdTier.CRITICAL),  # 0.80 exactly
            (170_000, ThresholdTier.CRITICAL),  # 0.85
            # EMERGENCY: fill >= 0.88
            (176_000, ThresholdTier.EMERGENCY),  # 0.88 exactly
            (190_000, ThresholdTier.EMERGENCY),  # 0.95
        ],
    )
    def test_tier_from_token_count(
        self,
        token_count: int,
        expected_tier: ThresholdTier,
        config: FakeThresholdConfiguration,
    ) -> None:
        """Estimator classifies token count into expected tier."""
        reader = FakeTranscriptReader(token_count=token_count)
        estimator = ContextFillEstimator(reader=reader, threshold_config=config)
        result = estimator.estimate(transcript_path="/fake/transcript.jsonl")
        assert result.tier == expected_tier

    def test_estimate_returns_fill_estimate(self, config: FakeThresholdConfiguration) -> None:
        """estimate() returns a FillEstimate instance."""
        reader = FakeTranscriptReader(token_count=100_000)
        estimator = ContextFillEstimator(reader=reader, threshold_config=config)
        result = estimator.estimate("/fake/path.jsonl")
        assert isinstance(result, FillEstimate)

    def test_estimate_sets_token_count(self, config: FakeThresholdConfiguration) -> None:
        """estimate() includes token_count in the result."""
        reader = FakeTranscriptReader(token_count=144_000)
        estimator = ContextFillEstimator(reader=reader, threshold_config=config)
        result = estimator.estimate("/fake/path.jsonl")
        assert result.token_count == 144_000

    def test_estimate_sets_fill_percentage(self, config: FakeThresholdConfiguration) -> None:
        """estimate() correctly computes fill_percentage."""
        reader = FakeTranscriptReader(token_count=100_000)
        estimator = ContextFillEstimator(reader=reader, threshold_config=config)
        result = estimator.estimate("/fake/path.jsonl")
        assert abs(result.fill_percentage - 0.5) < 1e-9


# =============================================================================
# BDD Scenario: Fail-open on exceptions from ITranscriptReader
# =============================================================================


class TestFailOpen:
    """Scenario: ContextFillEstimator is fail-open on reader exceptions.

    Given a reader that raises any exception,
    the estimator should return NOMINAL FillEstimate without propagating.
    """

    def test_fail_open_on_file_not_found(self, config: FakeThresholdConfiguration) -> None:
        """Returns NOMINAL FillEstimate when reader raises FileNotFoundError."""
        reader = FailingTranscriptReader(FileNotFoundError("no file"))
        estimator = ContextFillEstimator(reader=reader, threshold_config=config)
        result = estimator.estimate("/fake/missing.jsonl")
        assert result.tier == ThresholdTier.NOMINAL
        assert result.fill_percentage == 0.0
        assert result.token_count is None

    def test_fail_open_on_value_error(self, config: FakeThresholdConfiguration) -> None:
        """Returns NOMINAL FillEstimate when reader raises ValueError."""
        reader = FailingTranscriptReader(ValueError("empty file"))
        estimator = ContextFillEstimator(reader=reader, threshold_config=config)
        result = estimator.estimate("/fake/empty.jsonl")
        assert result.tier == ThresholdTier.NOMINAL
        assert result.fill_percentage == 0.0
        assert result.token_count is None

    def test_fail_open_on_generic_exception(self, config: FakeThresholdConfiguration) -> None:
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

    def test_disabled_returns_nominal(self, disabled_config: FakeThresholdConfiguration) -> None:
        """When is_enabled() returns False, result is NOMINAL fill=0.0."""
        reader = FakeTranscriptReader(token_count=190_000)
        estimator = ContextFillEstimator(reader=reader, threshold_config=disabled_config)
        result = estimator.estimate("/fake/path.jsonl")
        assert result.tier == ThresholdTier.NOMINAL
        assert result.fill_percentage == 0.0
        assert result.token_count is None

    def test_disabled_reader_never_called(
        self, disabled_config: FakeThresholdConfiguration
    ) -> None:
        """When disabled, the reader is not invoked."""
        mock_reader = MagicMock(spec=ITranscriptReader)
        estimator = ContextFillEstimator(reader=mock_reader, threshold_config=disabled_config)
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
        estimate = FillEstimate(fill_percentage=0.5, tier=tier, token_count=100_000)
        tag = estimator.generate_context_monitor_tag(estimate)
        assert expected_action_fragment in tag

    def test_tag_contains_fill_percentage(self, config: FakeThresholdConfiguration) -> None:
        """Generated tag includes fill-percentage element."""
        reader = FakeTranscriptReader(token_count=144_000)
        estimator = ContextFillEstimator(reader=reader, threshold_config=config)
        estimate = FillEstimate(
            fill_percentage=0.72, tier=ThresholdTier.WARNING, token_count=144_000
        )
        tag = estimator.generate_context_monitor_tag(estimate)
        assert "<fill-percentage>" in tag
        assert "0.72" in tag

    def test_tag_contains_tier(self, config: FakeThresholdConfiguration) -> None:
        """Generated tag includes tier element."""
        reader = FakeTranscriptReader(token_count=144_000)
        estimator = ContextFillEstimator(reader=reader, threshold_config=config)
        estimate = FillEstimate(
            fill_percentage=0.72, tier=ThresholdTier.WARNING, token_count=144_000
        )
        tag = estimator.generate_context_monitor_tag(estimate)
        assert "<tier>" in tag
        assert "WARNING" in tag

    def test_tag_contains_token_count(self, config: FakeThresholdConfiguration) -> None:
        """Generated tag includes token-count element when token_count is set."""
        reader = FakeTranscriptReader(token_count=144_000)
        estimator = ContextFillEstimator(reader=reader, threshold_config=config)
        estimate = FillEstimate(
            fill_percentage=0.72, tier=ThresholdTier.WARNING, token_count=144_000
        )
        tag = estimator.generate_context_monitor_tag(estimate)
        assert "<token-count>" in tag
        assert "144000" in tag

    def test_tag_within_token_budget(self, config: FakeThresholdConfiguration) -> None:
        """Generated tag is between 40 and 200 tokens (approx via len/4)."""
        reader = FakeTranscriptReader(token_count=144_000)
        estimator = ContextFillEstimator(reader=reader, threshold_config=config)
        estimate = FillEstimate(
            fill_percentage=0.72, tier=ThresholdTier.WARNING, token_count=144_000
        )
        tag = estimator.generate_context_monitor_tag(estimate)
        approx_tokens = len(tag) / 4
        assert 40 <= approx_tokens <= 200

    def test_tag_is_valid_xml_structure(self, config: FakeThresholdConfiguration) -> None:
        """Generated tag starts with <context-monitor> and ends with closing tag."""
        reader = FakeTranscriptReader(token_count=100_000)
        estimator = ContextFillEstimator(reader=reader, threshold_config=config)
        estimate = FillEstimate(
            fill_percentage=0.5, tier=ThresholdTier.NOMINAL, token_count=100_000
        )
        tag = estimator.generate_context_monitor_tag(estimate)
        assert tag.strip().startswith("<context-monitor>")
        assert tag.strip().endswith("</context-monitor>")

    def test_tag_with_none_token_count(self, config: FakeThresholdConfiguration) -> None:
        """Tag handles None token_count gracefully."""
        reader = FakeTranscriptReader(token_count=100_000)
        estimator = ContextFillEstimator(reader=reader, threshold_config=config)
        estimate = FillEstimate(fill_percentage=0.5, tier=ThresholdTier.NOMINAL, token_count=None)
        tag = estimator.generate_context_monitor_tag(estimate)
        assert "<context-monitor>" in tag
        # Should not raise


# =============================================================================
# BDD Scenario: Estimator uses config context window (TASK-006)
# =============================================================================


class TestEstimatorUsesConfigContextWindow:
    """Scenario: ContextFillEstimator reads context window from IThresholdConfiguration.

    Given a threshold config returning 500_000 for get_context_window_tokens(),
    the estimator should compute fill_percentage = token_count / 500_000.
    This verifies the TASK-006 fix: estimator no longer hardcodes 200K.
    """

    def test_uses_500k_config_window(self) -> None:
        """Estimator uses 500K context window from config, not hardcoded 200K."""
        config = FakeThresholdConfiguration(context_window_tokens=500_000)
        reader = FakeTranscriptReader(token_count=160_000)
        estimator = ContextFillEstimator(reader=reader, threshold_config=config)
        result = estimator.estimate("/fake/path.jsonl")
        # 160K / 500K = 0.32 -> NOMINAL (< 0.55)
        assert abs(result.fill_percentage - 0.32) < 1e-9
        assert result.tier == ThresholdTier.NOMINAL

    def test_uses_1m_config_window(self) -> None:
        """Estimator uses 1M context window from config."""
        config = FakeThresholdConfiguration(context_window_tokens=1_000_000)
        reader = FakeTranscriptReader(token_count=160_000)
        estimator = ContextFillEstimator(reader=reader, threshold_config=config)
        result = estimator.estimate("/fake/path.jsonl")
        # 160K / 1M = 0.16 -> NOMINAL (< 0.55)
        assert abs(result.fill_percentage - 0.16) < 1e-9
        assert result.tier == ThresholdTier.NOMINAL

    def test_200k_hardcoded_would_give_wrong_tier(self) -> None:
        """Proves the bug: 160K/200K = 0.80 CRITICAL, but 160K/500K = 0.32 NOMINAL."""
        config = FakeThresholdConfiguration(context_window_tokens=500_000)
        reader = FakeTranscriptReader(token_count=160_000)
        estimator = ContextFillEstimator(reader=reader, threshold_config=config)
        result = estimator.estimate("/fake/path.jsonl")
        # With config window (500K): NOMINAL (correct for Enterprise)
        assert result.tier == ThresholdTier.NOMINAL
        # If hardcoded 200K was used: 160K/200K = 0.80 would be CRITICAL (wrong)
        assert result.fill_percentage != pytest.approx(0.80)

    def test_fill_estimate_includes_context_window(self) -> None:
        """FillEstimate includes context_window field."""
        config = FakeThresholdConfiguration(
            context_window_tokens=500_000,
            context_window_source="config",
        )
        reader = FakeTranscriptReader(token_count=160_000)
        estimator = ContextFillEstimator(reader=reader, threshold_config=config)
        result = estimator.estimate("/fake/path.jsonl")
        assert result.context_window == 500_000

    def test_fill_estimate_includes_context_window_source(self) -> None:
        """FillEstimate includes context_window_source field."""
        config = FakeThresholdConfiguration(
            context_window_tokens=1_000_000,
            context_window_source="env-1m-detection",
        )
        reader = FakeTranscriptReader(token_count=160_000)
        estimator = ContextFillEstimator(reader=reader, threshold_config=config)
        result = estimator.estimate("/fake/path.jsonl")
        assert result.context_window_source == "env-1m-detection"


# =============================================================================
# BDD Scenario: Zero/negative context window guard (TASK-006, FM-003/FM-004)
# =============================================================================


class TestEstimatorContextWindowGuard:
    """Scenario: Estimator guards against zero/negative context window.

    Given a threshold config returning zero or negative context_window_tokens,
    the estimator should fall back to 200K default to prevent ZeroDivisionError.
    """

    def test_zero_context_window_falls_back(self) -> None:
        """Zero context window falls back to 200K (FM-003)."""
        config = FakeThresholdConfiguration(context_window_tokens=0)
        reader = FakeTranscriptReader(token_count=100_000)
        estimator = ContextFillEstimator(reader=reader, threshold_config=config)
        result = estimator.estimate("/fake/path.jsonl")
        # Should NOT raise ZeroDivisionError
        assert result.context_window == 200_000
        assert result.context_window_source == "default"
        assert result.fill_percentage == pytest.approx(0.5)

    def test_negative_context_window_falls_back(self) -> None:
        """Negative context window falls back to 200K (FM-004)."""
        config = FakeThresholdConfiguration(context_window_tokens=-100_000)
        reader = FakeTranscriptReader(token_count=100_000)
        estimator = ContextFillEstimator(reader=reader, threshold_config=config)
        result = estimator.estimate("/fake/path.jsonl")
        assert result.context_window == 200_000
        assert result.context_window_source == "default"

    def test_exceeds_max_context_window_falls_back(self) -> None:
        """Context window exceeding 2M falls back to 200K (AV-002)."""
        config = FakeThresholdConfiguration(context_window_tokens=5_000_000)
        reader = FakeTranscriptReader(token_count=100_000)
        estimator = ContextFillEstimator(reader=reader, threshold_config=config)
        result = estimator.estimate("/fake/path.jsonl")
        assert result.context_window == 200_000
        assert result.context_window_source == "default"

    def test_threshold_config_exception_fails_open(self) -> None:
        """Exception from get_context_window_tokens() returns NOMINAL (FM-009)."""
        config = FakeThresholdConfiguration()
        # Monkey-patch to simulate an exception from the threshold config
        config.get_context_window_tokens = lambda: (_ for _ in ()).throw(  # type: ignore[assignment]
            RuntimeError("config error")
        )
        reader = FakeTranscriptReader(token_count=100_000)
        estimator = ContextFillEstimator(reader=reader, threshold_config=config)
        result = estimator.estimate("/fake/path.jsonl")
        assert result.tier == ThresholdTier.NOMINAL
        assert result.fill_percentage == 0.0
        assert result.token_count is None


# =============================================================================
# BDD Scenario: XML tag includes context-window fields (TASK-006)
# =============================================================================


class TestXmlContextWindowFields:
    """Scenario: XML <context-monitor> tag includes context-window information.

    Given a FillEstimate with context_window and context_window_source,
    generate_context_monitor_tag should include these fields.
    """

    def test_tag_contains_context_window(self, config: FakeThresholdConfiguration) -> None:
        """Generated tag includes <context-window> element."""
        reader = FakeTranscriptReader(token_count=144_000)
        estimator = ContextFillEstimator(reader=reader, threshold_config=config)
        estimate = FillEstimate(
            fill_percentage=0.72,
            tier=ThresholdTier.WARNING,
            token_count=144_000,
            context_window=200_000,
            context_window_source="default",
        )
        tag = estimator.generate_context_monitor_tag(estimate)
        assert "<context-window>200000</context-window>" in tag

    def test_tag_contains_context_window_source_default(
        self, config: FakeThresholdConfiguration
    ) -> None:
        """Generated tag includes <context-window-source>default</context-window-source>."""
        reader = FakeTranscriptReader(token_count=144_000)
        estimator = ContextFillEstimator(reader=reader, threshold_config=config)
        estimate = FillEstimate(
            fill_percentage=0.72,
            tier=ThresholdTier.WARNING,
            token_count=144_000,
            context_window=200_000,
            context_window_source="default",
        )
        tag = estimator.generate_context_monitor_tag(estimate)
        assert "<context-window-source>default</context-window-source>" in tag

    def test_tag_contains_context_window_source_config(
        self, config: FakeThresholdConfiguration
    ) -> None:
        """Generated tag includes <context-window-source>config</context-window-source>."""
        reader = FakeTranscriptReader(token_count=160_000)
        estimator = ContextFillEstimator(reader=reader, threshold_config=config)
        estimate = FillEstimate(
            fill_percentage=0.32,
            tier=ThresholdTier.NOMINAL,
            token_count=160_000,
            context_window=500_000,
            context_window_source="config",
        )
        tag = estimator.generate_context_monitor_tag(estimate)
        assert "<context-window>500000</context-window>" in tag
        assert "<context-window-source>config</context-window-source>" in tag

    def test_tag_contains_context_window_source_1m_detection(
        self, config: FakeThresholdConfiguration
    ) -> None:
        """Generated tag includes <context-window-source>env-1m-detection</context-window-source>."""
        reader = FakeTranscriptReader(token_count=160_000)
        estimator = ContextFillEstimator(reader=reader, threshold_config=config)
        estimate = FillEstimate(
            fill_percentage=0.16,
            tier=ThresholdTier.NOMINAL,
            token_count=160_000,
            context_window=1_000_000,
            context_window_source="env-1m-detection",
        )
        tag = estimator.generate_context_monitor_tag(estimate)
        assert "<context-window>1000000</context-window>" in tag
        assert "<context-window-source>env-1m-detection</context-window-source>" in tag


# =============================================================================
# BDD Scenario: monitoring_ok field distinguishes genuine from fail-open (TASK-007)
# =============================================================================


class TestMonitoringOk:
    """Scenario: monitoring_ok field on FillEstimate distinguishes genuine from fail-open.

    Genuine estimates have monitoring_ok=True. Fail-open and disabled estimates
    have monitoring_ok=False. XML output includes <monitoring-ok> element.
    """

    def test_genuine_estimate_has_monitoring_ok_true(
        self, config: FakeThresholdConfiguration
    ) -> None:
        """Successful estimate() returns monitoring_ok=True."""
        reader = FakeTranscriptReader(token_count=100_000)
        estimator = ContextFillEstimator(reader=reader, threshold_config=config)
        result = estimator.estimate("/fake/path.jsonl")
        assert result.monitoring_ok is True

    def test_fail_open_has_monitoring_ok_false(self, config: FakeThresholdConfiguration) -> None:
        """Fail-open estimate (reader exception) returns monitoring_ok=False."""
        reader = FailingTranscriptReader(RuntimeError("fail"))
        estimator = ContextFillEstimator(reader=reader, threshold_config=config)
        result = estimator.estimate("/fake/path.jsonl")
        assert result.monitoring_ok is False
        assert result.tier == ThresholdTier.NOMINAL

    def test_disabled_has_monitoring_ok_false(
        self, disabled_config: FakeThresholdConfiguration
    ) -> None:
        """Disabled monitoring returns monitoring_ok=False."""
        reader = FakeTranscriptReader(token_count=190_000)
        estimator = ContextFillEstimator(reader=reader, threshold_config=disabled_config)
        result = estimator.estimate("/fake/path.jsonl")
        assert result.monitoring_ok is False
        assert result.tier == ThresholdTier.NOMINAL

    def test_xml_tag_includes_monitoring_ok_true(self, config: FakeThresholdConfiguration) -> None:
        """XML tag includes <monitoring-ok>true</monitoring-ok> for genuine estimates."""
        reader = FakeTranscriptReader(token_count=100_000)
        estimator = ContextFillEstimator(reader=reader, threshold_config=config)
        estimate = FillEstimate(
            fill_percentage=0.5,
            tier=ThresholdTier.NOMINAL,
            token_count=100_000,
            monitoring_ok=True,
        )
        tag = estimator.generate_context_monitor_tag(estimate)
        assert "<monitoring-ok>true</monitoring-ok>" in tag

    def test_xml_tag_includes_monitoring_ok_false(self, config: FakeThresholdConfiguration) -> None:
        """XML tag includes <monitoring-ok>false</monitoring-ok> for fail-open."""
        reader = FakeTranscriptReader(token_count=100_000)
        estimator = ContextFillEstimator(reader=reader, threshold_config=config)
        estimate = FillEstimate(
            fill_percentage=0.0,
            tier=ThresholdTier.NOMINAL,
            token_count=None,
            monitoring_ok=False,
        )
        tag = estimator.generate_context_monitor_tag(estimate)
        assert "<monitoring-ok>false</monitoring-ok>" in tag
