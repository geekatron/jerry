# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
Unit tests for context monitoring domain events.

Tests cover BDD scenarios from EN-003:
    - ContextThresholdReached event construction and payload
    - CompactionDetected event construction and payload
    - CheckpointCreated event construction and payload
    - All events are immutable (frozen dataclass)

References:
    - EN-003: Context Monitoring Bounded Context Foundation
    - PROJ-004: Context Resilience
"""

from __future__ import annotations

import pytest

from src.context_monitoring.domain.events.checkpoint_created import CheckpointCreated
from src.context_monitoring.domain.events.compaction_detected import CompactionDetected
from src.context_monitoring.domain.events.context_threshold_reached import (
    ContextThresholdReached,
)


# =============================================================================
# BDD Scenario: ContextThresholdReached event
# =============================================================================


class TestContextThresholdReached:
    """Scenario: ContextThresholdReached domain event.

    Given a context fill threshold crossing,
    the event should capture the tier and fill_percentage.
    """

    def test_construction(self) -> None:
        """ContextThresholdReached can be constructed with all fields."""
        event = ContextThresholdReached(
            aggregate_id="session-001",
            aggregate_type="ContextMonitor",
            tier="warning",
            fill_percentage=0.72,
        )
        assert event.tier == "warning"
        assert event.fill_percentage == 0.72
        assert event.aggregate_type == "ContextMonitor"

    def test_payload(self) -> None:
        """ContextThresholdReached._payload returns tier and fill_percentage."""
        event = ContextThresholdReached(
            aggregate_id="session-001",
            aggregate_type="ContextMonitor",
            tier="critical",
            fill_percentage=0.82,
        )
        payload = event._payload()
        assert payload["tier"] == "critical"
        assert payload["fill_percentage"] == 0.82

    def test_to_dict_includes_event_type(self) -> None:
        """ContextThresholdReached.to_dict includes event_type."""
        event = ContextThresholdReached(
            aggregate_id="session-001",
            aggregate_type="ContextMonitor",
            tier="emergency",
            fill_percentage=0.90,
        )
        data = event.to_dict()
        assert data["event_type"] == "ContextThresholdReached"
        assert data["tier"] == "emergency"

    def test_is_immutable(self) -> None:
        """ContextThresholdReached is immutable."""
        event = ContextThresholdReached(
            aggregate_id="session-001",
            aggregate_type="ContextMonitor",
            tier="warning",
            fill_percentage=0.72,
        )
        with pytest.raises(AttributeError):
            event.tier = "critical"  # type: ignore[misc]


# =============================================================================
# BDD Scenario: CompactionDetected event
# =============================================================================


class TestCompactionDetected:
    """Scenario: CompactionDetected domain event.

    Given a compaction event detection,
    the event should capture the compaction details.
    """

    def test_construction(self) -> None:
        """CompactionDetected can be constructed with all fields."""
        event = CompactionDetected(
            aggregate_id="session-001",
            aggregate_type="ContextMonitor",
            previous_token_count=180000,
            current_token_count=80000,
            compaction_number=1,
        )
        assert event.previous_token_count == 180000
        assert event.current_token_count == 80000
        assert event.compaction_number == 1

    def test_payload(self) -> None:
        """CompactionDetected._payload returns compaction details."""
        event = CompactionDetected(
            aggregate_id="session-001",
            aggregate_type="ContextMonitor",
            previous_token_count=180000,
            current_token_count=80000,
            compaction_number=2,
        )
        payload = event._payload()
        assert payload["previous_token_count"] == 180000
        assert payload["current_token_count"] == 80000
        assert payload["compaction_number"] == 2

    def test_to_dict_includes_event_type(self) -> None:
        """CompactionDetected.to_dict includes event_type."""
        event = CompactionDetected(
            aggregate_id="session-001",
            aggregate_type="ContextMonitor",
            previous_token_count=180000,
            current_token_count=80000,
            compaction_number=1,
        )
        data = event.to_dict()
        assert data["event_type"] == "CompactionDetected"

    def test_is_immutable(self) -> None:
        """CompactionDetected is immutable."""
        event = CompactionDetected(
            aggregate_id="session-001",
            aggregate_type="ContextMonitor",
            previous_token_count=180000,
            current_token_count=80000,
            compaction_number=1,
        )
        with pytest.raises(AttributeError):
            event.compaction_number = 3  # type: ignore[misc]


# =============================================================================
# BDD Scenario: CheckpointCreated event
# =============================================================================


class TestCheckpointCreated:
    """Scenario: CheckpointCreated domain event.

    Given a checkpoint creation,
    the event should capture the checkpoint_id and trigger.
    """

    def test_construction(self) -> None:
        """CheckpointCreated can be constructed with all fields."""
        event = CheckpointCreated(
            aggregate_id="session-001",
            aggregate_type="ContextMonitor",
            checkpoint_id="cx-001",
            trigger="pre_compact",
        )
        assert event.checkpoint_id == "cx-001"
        assert event.trigger == "pre_compact"

    def test_payload(self) -> None:
        """CheckpointCreated._payload returns checkpoint details."""
        event = CheckpointCreated(
            aggregate_id="session-001",
            aggregate_type="ContextMonitor",
            checkpoint_id="cx-003",
            trigger="manual",
        )
        payload = event._payload()
        assert payload["checkpoint_id"] == "cx-003"
        assert payload["trigger"] == "manual"

    def test_to_dict_includes_event_type(self) -> None:
        """CheckpointCreated.to_dict includes event_type."""
        event = CheckpointCreated(
            aggregate_id="session-001",
            aggregate_type="ContextMonitor",
            checkpoint_id="cx-001",
            trigger="pre_compact",
        )
        data = event.to_dict()
        assert data["event_type"] == "CheckpointCreated"

    def test_is_immutable(self) -> None:
        """CheckpointCreated is immutable."""
        event = CheckpointCreated(
            aggregate_id="session-001",
            aggregate_type="ContextMonitor",
            checkpoint_id="cx-001",
            trigger="pre_compact",
        )
        with pytest.raises(AttributeError):
            event.checkpoint_id = "cx-999"  # type: ignore[misc]
