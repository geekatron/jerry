# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
ContextState - Aggregate context monitoring state value object.

Immutable value object representing the overall state of context
monitoring, including fill percentage, tier, and compaction history.

Attributes:
    fill_percentage: Current fill as a fraction (0.0 to 1.0)
    tier: Current ThresholdTier classification
    compaction_count: Number of compactions detected this session

References:
    - EN-003: Context Monitoring Bounded Context Foundation
    - FEAT-001: Context Detection
    - PROJ-004: Context Resilience
"""

from __future__ import annotations

from dataclasses import dataclass

from src.context_monitoring.domain.value_objects.threshold_tier import ThresholdTier


@dataclass(frozen=True)
class ContextState:
    """Overall context monitoring state.

    Immutable value object tracking the current context fill level,
    its tier classification, and how many compactions have been
    detected in this session.

    Attributes:
        fill_percentage: Current fill as a fraction between 0.0 and 1.0
        tier: Classified ThresholdTier for this fill level
        compaction_count: Number of compactions detected (default 0)

    Example:
        >>> state = ContextState(
        ...     fill_percentage=0.65,
        ...     tier=ThresholdTier.LOW,
        ...     compaction_count=1,
        ... )
        >>> state.compaction_count
        1
    """

    fill_percentage: float
    tier: ThresholdTier
    compaction_count: int = 0
