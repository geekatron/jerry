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
    monitoring_ok: Whether the reading came from active monitoring (True)
        or from a fail-open/disabled fallback (False)

References:
    - EN-003: Context Monitoring Bounded Context Foundation
    - TASK-007: Add monitoring_ok Field to FillEstimate
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
        context_window: Context window size used for this estimate
        context_window_source: How the context window was determined
        monitoring_ok: True if this reading came from active, functioning
            monitoring. False if from fail-open fallback or disabled state.
            Consumers can use this to distinguish genuine NOMINAL from
            fail-open NOMINAL. Default True for backward compatibility.

    Example:
        >>> estimate = FillEstimate(
        ...     fill_percentage=0.72,
        ...     tier=ThresholdTier.WARNING,
        ...     token_count=144000,
        ...     context_window=200000,
        ...     context_window_source="default",
        ... )
        >>> estimate.fill_percentage
        0.72
        >>> estimate.monitoring_ok
        True
    """

    fill_percentage: float
    tier: ThresholdTier
    token_count: int | None = None
    context_window: int = 200_000
    context_window_source: str = "default"
    monitoring_ok: bool = True
