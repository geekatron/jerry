# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
IThresholdConfiguration - Port for Context Monitoring Threshold Access.

This port defines the contract for reading context monitoring threshold
configuration values. Implementations bridge to the underlying configuration
system (e.g., LayeredConfigAdapter).

The port is intentionally thin: it provides typed access to the six
context monitoring configuration keys with sensible defaults.

Configuration Keys (context_monitor.* namespace):
    - nominal_threshold: Float (0.55) - context fill below this is nominal
    - warning_threshold: Float (0.70) - context fill triggers warning
    - critical_threshold: Float (0.80) - context fill triggers critical alert
    - emergency_threshold: Float (0.88) - context fill triggers emergency
    - compaction_detection_threshold: Int (10000) - token delta for compaction detection
    - enabled: Bool (True) - whether context monitoring is active

References:
    - EN-002: ConfigThresholdAdapter + IThresholdConfiguration Port
    - FEAT-001: Context Detection
    - PROJ-004: Context Resilience
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable


@runtime_checkable
class IThresholdConfiguration(Protocol):
    """Port for reading context monitoring threshold configuration.

    This protocol defines the contract for accessing context monitoring
    thresholds. Implementations delegate to the underlying configuration
    system and provide defaults when keys are not explicitly set.

    Thread Safety:
        Implementations SHOULD ensure thread-safe read access.

    Example:
        >>> config: IThresholdConfiguration = ConfigThresholdAdapter(layered_config)
        >>> if config.is_enabled():
        ...     threshold = config.get_threshold("warning")
        ...     print(f"Warning at {threshold:.0%} context fill")
    """

    def get_threshold(self, tier: str) -> float:
        """Get the threshold value for a context monitoring tier.

        Supported tiers: "nominal", "warning", "critical", "emergency".

        Args:
            tier: The threshold tier name (case-insensitive).

        Returns:
            The threshold value as a float between 0.0 and 1.0.

        Raises:
            ValueError: If the tier name is not recognized.

        Example:
            >>> config.get_threshold("warning")
            0.70
            >>> config.get_threshold("critical")
            0.80
        """
        ...

    def is_enabled(self) -> bool:
        """Check whether context monitoring is enabled.

        Returns:
            True if context monitoring is active, False otherwise.

        Example:
            >>> config.is_enabled()
            True
        """
        ...

    def get_compaction_detection_threshold(self) -> int:
        """Get the compaction detection threshold in tokens.

        This value represents the minimum token delta between consecutive
        context measurements that signals a compaction event has occurred.

        Returns:
            The compaction detection threshold in tokens.

        Example:
            >>> config.get_compaction_detection_threshold()
            10000
        """
        ...

    def get_all_thresholds(self) -> dict[str, float]:
        """Get all threshold tiers and their values.

        Returns:
            Dictionary mapping tier names to threshold values.

        Example:
            >>> config.get_all_thresholds()
            {'nominal': 0.55, 'warning': 0.70, 'critical': 0.80, 'emergency': 0.88}
        """
        ...
