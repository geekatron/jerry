# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
Unit tests for CheckpointData value object.

Tests cover BDD scenarios from EN-003:
    - CheckpointData captures resumption state
    - CheckpointData is immutable (frozen dataclass)
    - Construction with required and optional fields

References:
    - EN-003: Context Monitoring Bounded Context Foundation
    - PROJ-004: Context Resilience
"""

from __future__ import annotations

import pytest

from src.context_monitoring.domain.value_objects.checkpoint_data import CheckpointData
from src.context_monitoring.domain.value_objects.fill_estimate import FillEstimate
from src.context_monitoring.domain.value_objects.threshold_tier import ThresholdTier


# =============================================================================
# BDD Scenario: CheckpointData captures resumption state
# =============================================================================


class TestCheckpointDataCapture:
    """Scenario: CheckpointData captures resumption state.

    Given a checkpoint creation request,
    CheckpointData should store all relevant resumption information.
    """

    def test_captures_checkpoint_id(self) -> None:
        """CheckpointData stores checkpoint_id."""
        context_state = FillEstimate(fill_percentage=0.7, tier=ThresholdTier.WARNING)
        cp = CheckpointData(
            checkpoint_id="cx-001",
            context_state=context_state,
            created_at="2026-02-20T10:00:00+00:00",
        )
        assert cp.checkpoint_id == "cx-001"

    def test_captures_context_state(self) -> None:
        """CheckpointData stores context_state as FillEstimate."""
        context_state = FillEstimate(fill_percentage=0.85, tier=ThresholdTier.CRITICAL)
        cp = CheckpointData(
            checkpoint_id="cx-002",
            context_state=context_state,
            created_at="2026-02-20T10:00:00+00:00",
        )
        assert cp.context_state.fill_percentage == 0.85
        assert cp.context_state.tier == ThresholdTier.CRITICAL

    def test_captures_resumption_state(self) -> None:
        """CheckpointData stores optional resumption_state dict."""
        context_state = FillEstimate(fill_percentage=0.7, tier=ThresholdTier.WARNING)
        resumption = {"current_phase": "implementation", "entity_id": "EN-003"}
        cp = CheckpointData(
            checkpoint_id="cx-003",
            context_state=context_state,
            resumption_state=resumption,
            created_at="2026-02-20T10:00:00+00:00",
        )
        assert cp.resumption_state == resumption

    def test_resumption_state_defaults_to_none(self) -> None:
        """CheckpointData resumption_state defaults to None."""
        context_state = FillEstimate(fill_percentage=0.5, tier=ThresholdTier.NOMINAL)
        cp = CheckpointData(
            checkpoint_id="cx-004",
            context_state=context_state,
            created_at="2026-02-20T10:00:00+00:00",
        )
        assert cp.resumption_state is None

    def test_captures_created_at_iso(self) -> None:
        """CheckpointData stores created_at as ISO 8601 string."""
        context_state = FillEstimate(fill_percentage=0.5, tier=ThresholdTier.NOMINAL)
        timestamp = "2026-02-20T10:30:00+00:00"
        cp = CheckpointData(
            checkpoint_id="cx-005",
            context_state=context_state,
            created_at=timestamp,
        )
        assert cp.created_at == timestamp


# =============================================================================
# BDD Scenario: CheckpointData is immutable
# =============================================================================


class TestCheckpointDataImmutability:
    """Scenario: CheckpointData is immutable.

    Given a CheckpointData value object,
    it should not allow mutation of any field.
    """

    def test_cannot_mutate_checkpoint_id(self) -> None:
        """CheckpointData.checkpoint_id cannot be changed after creation."""
        context_state = FillEstimate(fill_percentage=0.5, tier=ThresholdTier.NOMINAL)
        cp = CheckpointData(
            checkpoint_id="cx-001",
            context_state=context_state,
            created_at="2026-02-20T10:00:00+00:00",
        )
        with pytest.raises(AttributeError):
            cp.checkpoint_id = "cx-999"  # type: ignore[misc]

    def test_cannot_mutate_context_state(self) -> None:
        """CheckpointData.context_state cannot be changed after creation."""
        context_state = FillEstimate(fill_percentage=0.5, tier=ThresholdTier.NOMINAL)
        cp = CheckpointData(
            checkpoint_id="cx-001",
            context_state=context_state,
            created_at="2026-02-20T10:00:00+00:00",
        )
        new_state = FillEstimate(fill_percentage=0.9, tier=ThresholdTier.EMERGENCY)
        with pytest.raises(AttributeError):
            cp.context_state = new_state  # type: ignore[misc]

    def test_cannot_mutate_created_at(self) -> None:
        """CheckpointData.created_at cannot be changed after creation."""
        context_state = FillEstimate(fill_percentage=0.5, tier=ThresholdTier.NOMINAL)
        cp = CheckpointData(
            checkpoint_id="cx-001",
            context_state=context_state,
            created_at="2026-02-20T10:00:00+00:00",
        )
        with pytest.raises(AttributeError):
            cp.created_at = "2026-12-31T23:59:59+00:00"  # type: ignore[misc]
