# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
CheckpointData - Checkpoint state capture value object.

Immutable value object representing a complete checkpoint snapshot,
including context state, optional resumption data, and metadata.

A checkpoint is created before context compaction to preserve enough
state for the next session to resume work seamlessly.

Attributes:
    checkpoint_id: Unique sequential ID (e.g., cx-001, cx-002)
    context_state: Fill estimate at time of checkpoint
    resumption_state: Optional dict with orchestration/workflow state
    created_at: ISO 8601 timestamp of checkpoint creation

References:
    - EN-003: Context Monitoring Bounded Context Foundation
    - FEAT-002: Checkpoint Management
    - PROJ-004: Context Resilience
"""

from __future__ import annotations

from dataclasses import dataclass

from src.context_monitoring.domain.value_objects.fill_estimate import FillEstimate


@dataclass(frozen=True)
class CheckpointData:
    """Complete checkpoint state capture.

    Immutable value object containing all data needed to resume
    work after context compaction.

    Attributes:
        checkpoint_id: Sequential checkpoint ID (e.g., cx-001)
        context_state: FillEstimate at time of checkpoint
        resumption_state: Optional orchestration/workflow state dict
        created_at: ISO 8601 timestamp string

    Example:
        >>> from src.context_monitoring.domain.value_objects.fill_estimate import FillEstimate
        >>> from src.context_monitoring.domain.value_objects.threshold_tier import ThresholdTier
        >>> state = FillEstimate(fill_percentage=0.82, tier=ThresholdTier.CRITICAL)
        >>> cp = CheckpointData(
        ...     checkpoint_id="cx-001",
        ...     context_state=state,
        ...     created_at="2026-02-20T10:00:00+00:00",
        ... )
    """

    checkpoint_id: str
    context_state: FillEstimate
    created_at: str
    resumption_state: dict | None = None
