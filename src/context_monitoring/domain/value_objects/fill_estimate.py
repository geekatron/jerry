# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
FillEstimate - Context window fill estimation value object.

Immutable value object capturing the estimated fill level of the
LLM context window at a point in time.

Attributes:
    fill_percentage: Estimated fill as a fraction (0.0 to 1.0)
    tier: The ThresholdTier classification for this fill level
    token_count: Optional absolute token count estimate

References:
    - EN-003: Context Monitoring Bounded Context Foundation
    - FEAT-001: Context Detection
    - PROJ-004: Context Resilience
"""

from __future__ import annotations

from dataclasses import dataclass

from src.context_monitoring.domain.value_objects.threshold_tier import ThresholdTier


@dataclass(frozen=True)
class FillEstimate:
    """Estimated context window fill level.

    Immutable value object combining percentage fill, tier classification,
    and optional absolute token count.

    Attributes:
        fill_percentage: Fill as a fraction between 0.0 and 1.0
        tier: Classified ThresholdTier for this fill level
        token_count: Optional absolute token count, or None if unknown

    Example:
        >>> estimate = FillEstimate(
        ...     fill_percentage=0.72,
        ...     tier=ThresholdTier.WARNING,
        ...     token_count=144000,
        ... )
        >>> estimate.fill_percentage
        0.72
    """

    fill_percentage: float
    tier: ThresholdTier
    token_count: int | None = None
