# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
ContextEstimate - Computed context fill estimate value object.

Immutable value object representing the domain-computed result of
context fill estimation from exact Claude Code data.

References:
    - FEAT-002: Status Line / Context Monitoring Unification
    - EN-009: Domain VOs + ContextEstimateComputer Service
    - PROJ-004: Context Resilience
"""

from __future__ import annotations

from dataclasses import dataclass

from src.context_monitoring.domain.value_objects.threshold_tier import ThresholdTier


@dataclass(frozen=True)
class ContextEstimate:
    """Domain-computed context fill estimate.

    Combines exact Claude Code data with Jerry's tier classification
    and broken-out token types for consumer use.

    Attributes:
        fill_percentage: Fill as a fraction between 0.0 and 1.0.
        used_tokens: Total tokens in context window.
        window_size: Dynamic context window size.
        tier: Classified ThresholdTier from Jerry's 5-tier system.
        is_estimated: False when computed from exact current_usage data.
            True when falling back to transcript-based estimation.
        fresh_tokens: Input tokens from last API call (non-cached).
        cached_tokens: Cache read tokens (previously cached content).
        cache_creation_tokens: Tokens used to create new cache entries.

    Example:
        >>> estimate = ContextEstimate(
        ...     fill_percentage=0.73,
        ...     used_tokens=146000,
        ...     window_size=200000,
        ...     tier=ThresholdTier.WARNING,
        ...     is_estimated=False,
        ...     fresh_tokens=8500,
        ...     cached_tokens=45200,
        ...     cache_creation_tokens=12000,
        ... )
    """

    fill_percentage: float
    used_tokens: int
    window_size: int
    tier: ThresholdTier
    is_estimated: bool
    fresh_tokens: int
    cached_tokens: int
    cache_creation_tokens: int
