# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
ThresholdTier - Context fill threshold tier enumeration.

Represents the five severity levels for context window fill monitoring.
Each tier corresponds to increasing urgency of action needed.

Tiers (in order of increasing severity):
    - NOMINAL: Context fill is healthy, no action needed
    - LOW: Context fill is growing but manageable
    - WARNING: Context fill is approaching concerning levels
    - CRITICAL: Context fill is high, action recommended
    - EMERGENCY: Context fill is dangerously high, immediate action required

References:
    - EN-003: Context Monitoring Bounded Context Foundation
    - FEAT-001: Context Detection
    - PROJ-004: Context Resilience
"""

from __future__ import annotations

from enum import Enum


class ThresholdTier(Enum):
    """Context fill threshold tier.

    Five levels of context window fill severity, ordered from
    least to most urgent.

    Attributes:
        NOMINAL: Healthy context fill level
        LOW: Growing but manageable
        WARNING: Approaching concerning levels
        CRITICAL: High fill, action recommended
        EMERGENCY: Dangerously high, immediate action required

    Example:
        >>> tier = ThresholdTier.WARNING
        >>> tier.value
        'warning'
    """

    NOMINAL = "nominal"
    LOW = "low"
    WARNING = "warning"
    CRITICAL = "critical"
    EMERGENCY = "emergency"

    def __str__(self) -> str:
        """Return the tier value as string."""
        return self.value

    def __repr__(self) -> str:
        """Return detailed representation for debugging."""
        return f"ThresholdTier.{self.name}"
