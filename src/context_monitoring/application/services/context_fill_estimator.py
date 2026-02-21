# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
ContextFillEstimator - Application service for estimating context window fill.

This service reads the latest token count from a transcript file via the
ITranscriptReader port, computes the fill percentage relative to the
configured context window size, and classifies the fill level into the
appropriate ThresholdTier.

Fail-open design: Any exception from the ITranscriptReader results in a
NOMINAL FillEstimate (fill=0.0, token_count=None) rather than propagating
the exception. This ensures context monitoring never disrupts the main workflow.

When monitoring is disabled (IThresholdConfiguration.is_enabled() returns False),
the service returns NOMINAL immediately without reading the transcript.

References:
    - EN-004: ContextFillEstimator and ResumptionContextGenerator
    - FEAT-001: Context Detection
    - PROJ-004: Context Resilience
"""

from __future__ import annotations

import logging

from src.context_monitoring.application.ports.threshold_configuration import (
    IThresholdConfiguration,
)
from src.context_monitoring.application.ports.transcript_reader import ITranscriptReader
from src.context_monitoring.domain.value_objects.fill_estimate import FillEstimate
from src.context_monitoring.domain.value_objects.threshold_tier import ThresholdTier

logger = logging.getLogger(__name__)

# Action text mapped to ThresholdTier
_TIER_ACTION_TEXT: dict[ThresholdTier, str] = {
    ThresholdTier.NOMINAL: "Context healthy. No action needed.",
    ThresholdTier.LOW: "Context growing. Monitor usage.",
    ThresholdTier.WARNING: (
        "Consider checkpointing critical state. "
        "Context fill approaching critical levels."
    ),
    ThresholdTier.CRITICAL: (
        "Checkpoint recommended. Prepare for possible context compaction."
    ),
    ThresholdTier.EMERGENCY: (
        "Immediate checkpoint required. "
        "Context exhaustion imminent. Save all critical state NOW."
    ),
}

# Fail-open sentinel returned on any reader error or when monitoring is disabled.
# TODO(TASK-007): Add monitoring_ok: bool field to FillEstimate to distinguish
# genuine NOMINAL from fail-open/disabled states. Currently these are
# indistinguishable, which could suppress checkpoint behavior in production.
_FAIL_OPEN_ESTIMATE = FillEstimate(
    fill_percentage=0.0,
    tier=ThresholdTier.NOMINAL,
    token_count=None,
)


class ContextFillEstimator:
    """Application service for estimating context window fill level.

    Combines token count reading, fill percentage computation, and
    tier classification into a single estimate() operation.

    Attributes:
        _reader: Port for reading token counts from transcript files.
        _threshold_config: Port for accessing threshold configuration.

    Example:
        >>> estimator = ContextFillEstimator(
        ...     reader=transcript_reader,
        ...     threshold_config=threshold_config,
        ... )
        >>> estimate = estimator.estimate("/path/to/transcript.jsonl")
        >>> print(estimate.tier)
        ThresholdTier.WARNING
    """

    def __init__(
        self,
        reader: ITranscriptReader,
        threshold_config: IThresholdConfiguration,
    ) -> None:
        """Initialize the ContextFillEstimator.

        Args:
            reader: Port for reading token counts from JSONL transcript files.
            threshold_config: Port for accessing context monitoring thresholds.
        """
        self._reader = reader
        self._threshold_config = threshold_config

    def estimate(
        self,
        transcript_path: str,
    ) -> FillEstimate:
        """Estimate the current context window fill level.

        Reads the latest token count from the transcript file, computes the
        fill percentage relative to the configured context window size, and
        classifies it into a ThresholdTier based on the configured thresholds.

        The context window size is read from IThresholdConfiguration, which
        follows the canonical detection priority: explicit user config >
        ANTHROPIC_MODEL [1m] suffix > default 200K.

        Fail-open: Any exception from the reader results in a NOMINAL
        FillEstimate (fill=0.0, token_count=None).

        If monitoring is disabled (is_enabled() returns False), returns
        NOMINAL immediately without reading the transcript.

        Args:
            transcript_path: Path to the JSONL transcript file.

        Returns:
            FillEstimate with fill_percentage, tier, token_count,
            context_window, and context_window_source.
            On error or disabled, returns NOMINAL FillEstimate.

        Example:
            >>> estimate = estimator.estimate("/path/transcript.jsonl")
            >>> estimate.tier
            ThresholdTier.WARNING
        """
        if not self._threshold_config.is_enabled():
            logger.debug("Context monitoring disabled; returning NOMINAL.")
            return _FAIL_OPEN_ESTIMATE

        try:
            token_count = self._reader.read_latest_tokens(transcript_path)

            context_window = self._threshold_config.get_context_window_tokens()
            context_window_source = self._threshold_config.get_context_window_source()

            # Guard against invalid context window values (FM-003/FM-004/AV-002)
            if context_window <= 0 or context_window > 2_000_000:
                logger.warning(
                    "Invalid context window %d; falling back to 200K default.",
                    context_window,
                )
                context_window = 200_000
                context_window_source = "default"

            fill_percentage = token_count / context_window
            tier = self._classify_tier(fill_percentage)

            return FillEstimate(
                fill_percentage=fill_percentage,
                tier=tier,
                token_count=token_count,
                context_window=context_window,
                context_window_source=context_window_source,
            )
        except Exception as exc:  # noqa: BLE001
            logger.warning(
                "Context estimation failed for %s: %s (fail-open -> NOMINAL)",
                transcript_path,
                exc,
            )
            return _FAIL_OPEN_ESTIMATE

    def generate_context_monitor_tag(self, estimate: FillEstimate) -> str:
        """Generate an XML <context-monitor> tag from a FillEstimate.

        Produces a compact XML block summarising the current context fill
        state with an action recommendation appropriate for the tier.

        Output is between 40 and 200 tokens (approximately len/4 characters).

        Args:
            estimate: The FillEstimate to render as XML.

        Returns:
            An XML string wrapped in <context-monitor> tags.

        Example:
            >>> tag = estimator.generate_context_monitor_tag(estimate)
            >>> print(tag)
            <context-monitor>
              <fill-percentage>0.72</fill-percentage>
              <tier>WARNING</tier>
              <token-count>144000</token-count>
              <action>Consider checkpointing...</action>
            </context-monitor>
        """
        action = _TIER_ACTION_TEXT.get(estimate.tier, "Monitor context usage.")
        token_count_str = str(estimate.token_count) if estimate.token_count is not None else "N/A"

        return (
            "<context-monitor>\n"
            f"  <fill-percentage>{estimate.fill_percentage:.4f}</fill-percentage>\n"
            f"  <tier>{estimate.tier.name}</tier>\n"
            f"  <token-count>{token_count_str}</token-count>\n"
            f"  <context-window>{estimate.context_window}</context-window>\n"
            f"  <context-window-source>{estimate.context_window_source}</context-window-source>\n"
            f"  <action>{action}</action>\n"
            "</context-monitor>"
        )

    def _classify_tier(self, fill_percentage: float) -> ThresholdTier:
        """Classify a fill percentage into a ThresholdTier.

        Tiers are determined by the configured thresholds:
            - NOMINAL: fill < nominal_threshold
            - LOW: nominal_threshold <= fill < warning_threshold
            - WARNING: warning_threshold <= fill < critical_threshold
            - CRITICAL: critical_threshold <= fill < emergency_threshold
            - EMERGENCY: fill >= emergency_threshold

        Args:
            fill_percentage: Fill as a fraction between 0.0 and 1.0.

        Returns:
            The corresponding ThresholdTier.
        """
        nominal = self._threshold_config.get_threshold("nominal")
        warning = self._threshold_config.get_threshold("warning")
        critical = self._threshold_config.get_threshold("critical")
        emergency = self._threshold_config.get_threshold("emergency")

        if fill_percentage >= emergency:
            return ThresholdTier.EMERGENCY
        if fill_percentage >= critical:
            return ThresholdTier.CRITICAL
        if fill_percentage >= warning:
            return ThresholdTier.WARNING
        if fill_percentage >= nominal:
            return ThresholdTier.LOW
        return ThresholdTier.NOMINAL
