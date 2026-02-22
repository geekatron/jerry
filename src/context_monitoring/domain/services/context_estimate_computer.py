# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
ContextEstimateComputer - Pure domain service for context fill computation.

Computes context fill percentage from exact Claude Code ``current_usage``
data, classifies into ThresholdTier, detects compaction from previous
state, and determines the appropriate rotation action.

This is a pure domain service with NO I/O. All data is passed in
as value objects.

References:
    - FEAT-002: Status Line / Context Monitoring Unification
    - EN-009: Domain VOs + ContextEstimateComputer Service
    - DEC-004 D-015: Never hardcode context window sizes
    - PROJ-004: Context Resilience
"""

from __future__ import annotations

from src.context_monitoring.domain.value_objects.compaction_result import (
    CompactionResult,
)
from src.context_monitoring.domain.value_objects.context_estimate import (
    ContextEstimate,
)
from src.context_monitoring.domain.value_objects.context_usage_input import (
    ContextUsageInput,
)
from src.context_monitoring.domain.value_objects.rotation_action import RotationAction
from src.context_monitoring.domain.value_objects.threshold_tier import ThresholdTier

# Default thresholds matching quality-enforcement.md SSOT
_DEFAULT_THRESHOLDS: dict[str, float] = {
    "nominal": 0.55,
    "warning": 0.70,
    "critical": 0.80,
    "emergency": 0.88,
}

# Rotation action mapping: (tier, aggressiveness) -> action
# Conservative: only act at EMERGENCY
# Moderate: act from WARNING onwards
# Aggressive: act from LOW onwards
_ROTATION_ACTIONS: dict[tuple[ThresholdTier, str], RotationAction] = {
    # Conservative
    (ThresholdTier.NOMINAL, "conservative"): RotationAction.NONE,
    (ThresholdTier.LOW, "conservative"): RotationAction.NONE,
    (ThresholdTier.WARNING, "conservative"): RotationAction.LOG_WARNING,
    (ThresholdTier.CRITICAL, "conservative"): RotationAction.LOG_WARNING,
    (ThresholdTier.EMERGENCY, "conservative"): RotationAction.CHECKPOINT,
    # Moderate (default)
    (ThresholdTier.NOMINAL, "moderate"): RotationAction.NONE,
    (ThresholdTier.LOW, "moderate"): RotationAction.NONE,
    (ThresholdTier.WARNING, "moderate"): RotationAction.LOG_WARNING,
    (ThresholdTier.CRITICAL, "moderate"): RotationAction.CHECKPOINT,
    (ThresholdTier.EMERGENCY, "moderate"): RotationAction.EMERGENCY_HANDOFF,
    # Aggressive
    (ThresholdTier.NOMINAL, "aggressive"): RotationAction.NONE,
    (ThresholdTier.LOW, "aggressive"): RotationAction.LOG_WARNING,
    (ThresholdTier.WARNING, "aggressive"): RotationAction.CHECKPOINT,
    (ThresholdTier.CRITICAL, "aggressive"): RotationAction.ROTATE,
    (ThresholdTier.EMERGENCY, "aggressive"): RotationAction.EMERGENCY_HANDOFF,
}


class ContextEstimateComputer:
    """Pure domain service for context fill computation.

    Computes fill percentage, tier classification, compaction detection,
    and rotation action from exact Claude Code data. No I/O.

    Attributes:
        _thresholds: Tier threshold configuration.
        _aggressiveness: Rotation aggressiveness mode.

    Example:
        >>> computer = ContextEstimateComputer()
        >>> estimate = computer.compute(usage_input)
        >>> estimate.tier
        ThresholdTier.WARNING
    """

    def __init__(
        self,
        thresholds: dict[str, float] | None = None,
        aggressiveness: str = "moderate",
    ) -> None:
        """Initialize the ContextEstimateComputer.

        Args:
            thresholds: Tier threshold values. Keys: "nominal", "warning",
                "critical", "emergency". Defaults to quality-enforcement.md SSOT.
            aggressiveness: Rotation mode. One of "conservative",
                "moderate", "aggressive". Defaults to "moderate".
        """
        self._thresholds = thresholds or _DEFAULT_THRESHOLDS.copy()
        self._aggressiveness = aggressiveness

    def compute(self, usage: ContextUsageInput) -> ContextEstimate:
        """Compute a context fill estimate from exact usage data.

        Uses the dynamic ``context_window_size`` from Claude Code
        (D-015: never hardcode). Falls back to Claude Code's
        ``used_percentage`` if token data suggests an anomaly.

        Args:
            usage: Parsed context usage input from Claude Code JSON.

        Returns:
            Computed ContextEstimate with fill, tier, and token breakdown.
        """
        window_size = usage.context_window_size
        if window_size <= 0:
            window_size = 200_000

        total_tokens = usage.total_context_tokens

        # Prefer Claude Code's pre-calculated percentage when available
        # and our token-based calculation would be zero (before first API call)
        if total_tokens == 0 and usage.used_percentage is not None:
            fill_pct = usage.used_percentage / 100.0
        else:
            fill_pct = total_tokens / window_size if window_size > 0 else 0.0

        # Clamp to [0.0, 1.0]
        fill_pct = max(0.0, min(1.0, fill_pct))

        tier = self.classify_tier(fill_pct)

        return ContextEstimate(
            fill_percentage=fill_pct,
            used_tokens=total_tokens,
            window_size=window_size,
            tier=tier,
            is_estimated=False,
            fresh_tokens=usage.input_tokens,
            cached_tokens=usage.cache_read_input_tokens,
            cache_creation_tokens=usage.cache_creation_input_tokens,
        )

    def classify_tier(self, fill_percentage: float) -> ThresholdTier:
        """Classify a fill percentage into a ThresholdTier.

        Uses the configured thresholds (SSOT from quality-enforcement.md).

        Args:
            fill_percentage: Fill as a fraction between 0.0 and 1.0.

        Returns:
            The corresponding ThresholdTier.

        Example:
            >>> computer = ContextEstimateComputer()
            >>> computer.classify_tier(0.85)
            ThresholdTier.CRITICAL
        """
        emergency = self._thresholds.get("emergency", 0.88)
        critical = self._thresholds.get("critical", 0.80)
        warning = self._thresholds.get("warning", 0.70)
        nominal = self._thresholds.get("nominal", 0.55)

        if fill_percentage >= emergency:
            return ThresholdTier.EMERGENCY
        if fill_percentage >= critical:
            return ThresholdTier.CRITICAL
        if fill_percentage >= warning:
            return ThresholdTier.WARNING
        if fill_percentage >= nominal:
            return ThresholdTier.LOW
        return ThresholdTier.NOMINAL

    def detect_compaction(
        self,
        current_tokens: int,
        current_session_id: str,
        previous_tokens: int | None,
        previous_session_id: str | None,
    ) -> CompactionResult:
        """Detect compaction or /clear from previous state.

        Compaction is a significant token drop within the same session_id.
        A session_id change indicates ``/clear`` (new session).

        Args:
            current_tokens: Current total context tokens.
            current_session_id: Current Claude Code session ID.
            previous_tokens: Previous invocation's token count.
                None if no prior state exists.
            previous_session_id: Previous invocation's session ID.
                None if no prior state exists.

        Returns:
            CompactionResult describing what was detected.

        Example:
            >>> result = computer.detect_compaction(46000, "abc", 180000, "abc")
            >>> result.detected
            True
        """
        # No prior state -- first invocation
        if previous_tokens is None or previous_session_id is None:
            return CompactionResult.no_compaction(current_tokens)

        # Session ID changed -- /clear event (new session)
        if current_session_id != previous_session_id:
            return CompactionResult.new_session(current_tokens)

        # Same session, check for token drop (compaction)
        # Compaction typically drops tokens by >50%. Use a threshold
        # to avoid false positives from normal fluctuation.
        token_drop = previous_tokens - current_tokens
        if token_drop > 10_000 and current_tokens < previous_tokens * 0.8:
            return CompactionResult(
                detected=True,
                from_tokens=previous_tokens,
                to_tokens=current_tokens,
                session_id_changed=False,
            )

        return CompactionResult.no_compaction(current_tokens)

    def determine_rotation_action(self, tier: ThresholdTier) -> RotationAction:
        """Determine the rotation action for a given tier.

        Uses the configured aggressiveness mode to select the
        appropriate graduated response.

        Args:
            tier: Current ThresholdTier classification.

        Returns:
            The recommended RotationAction.

        Example:
            >>> computer = ContextEstimateComputer(aggressiveness="moderate")
            >>> computer.determine_rotation_action(ThresholdTier.CRITICAL)
            RotationAction.CHECKPOINT
        """
        key = (tier, self._aggressiveness)
        return _ROTATION_ACTIONS.get(key, RotationAction.NONE)

    @property
    def thresholds(self) -> dict[str, float]:
        """Return a copy of the threshold configuration.

        Returns:
            Dict with keys: nominal, warning, critical, emergency.
        """
        return self._thresholds.copy()
