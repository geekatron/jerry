# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Unit tests for WorkItem domain events.

Test Categories:
    - Event Creation: Each event type creates correctly
    - Serialization: to_dict and from_dict work correctly
    - Payload: _payload returns event-specific data

References:
    - IMPL-005: WorkItem Aggregate (events are supporting components)
    - ADR-009: Event Storage Mechanism
"""

from __future__ import annotations

from datetime import datetime

import pytest

from src.work_tracking.domain.events.work_item_events import (
    AssigneeChanged,
    DependencyAdded,
    DependencyRemoved,
    PriorityChanged,
    QualityMetricsUpdated,
    StatusChanged,
    WorkItemCompleted,
    WorkItemCreated,
)

# =============================================================================
# WorkItemCreated Tests
# =============================================================================


class TestWorkItemCreated:
    """Tests for WorkItemCreated event."""

    def test_create_with_required_fields(self) -> None:
        """Create event with required fields."""
        event = WorkItemCreated(
            aggregate_id="12345",
            aggregate_type="WorkItem",
            title="Test Task",
            work_type="task",
            priority="medium",
        )
        assert event.aggregate_id == "12345"
        assert event.title == "Test Task"
        assert event.work_type == "task"

    def test_payload_includes_all_fields(self) -> None:
        """Payload includes all event-specific fields."""
        event = WorkItemCreated(
            aggregate_id="12345",
            aggregate_type="WorkItem",
            title="Test Task",
            work_type="task",
            priority="high",
            description="Details here",
            parent_id="99999",
        )
        payload = event._payload()

        assert payload["title"] == "Test Task"
        assert payload["work_type"] == "task"
        assert payload["priority"] == "high"
        assert payload["description"] == "Details here"
        assert payload["parent_id"] == "99999"

    def test_to_dict_includes_event_type(self) -> None:
        """to_dict includes event_type for deserialization."""
        event = WorkItemCreated(
            aggregate_id="12345",
            aggregate_type="WorkItem",
            title="Test",
        )
        data = event.to_dict()

        assert data["event_type"] == "WorkItemCreated"
        assert data["aggregate_id"] == "12345"

    def test_from_dict_restores_event(self) -> None:
        """from_dict restores event from dictionary."""
        original = WorkItemCreated(
            aggregate_id="12345",
            aggregate_type="WorkItem",
            title="Test Task",
            work_type="bug",
            priority="critical",
            description="Bug details",
        )
        data = original.to_dict()
        restored = WorkItemCreated.from_dict(data)

        assert restored.aggregate_id == original.aggregate_id
        assert restored.title == original.title
        assert restored.work_type == original.work_type
        assert restored.priority == original.priority
        assert restored.description == original.description

    def test_default_values(self) -> None:
        """Default values are set correctly."""
        event = WorkItemCreated(
            aggregate_id="12345",
            aggregate_type="WorkItem",
        )
        assert event.title == ""
        assert event.work_type == "task"
        assert event.priority == "medium"
        assert event.description == ""
        assert event.parent_id is None


# =============================================================================
# StatusChanged Tests
# =============================================================================


class TestStatusChanged:
    """Tests for StatusChanged event."""

    def test_create_with_statuses(self) -> None:
        """Create event with status transition."""
        event = StatusChanged(
            aggregate_id="12345",
            aggregate_type="WorkItem",
            old_status="pending",
            new_status="in_progress",
            reason="Starting work",
        )
        assert event.old_status == "pending"
        assert event.new_status == "in_progress"
        assert event.reason == "Starting work"

    def test_payload_includes_status_fields(self) -> None:
        """Payload includes status transition fields."""
        event = StatusChanged(
            aggregate_id="12345",
            aggregate_type="WorkItem",
            old_status="in_progress",
            new_status="done",
        )
        payload = event._payload()

        assert payload["old_status"] == "in_progress"
        assert payload["new_status"] == "done"
        assert payload["reason"] is None

    def test_from_dict_restores_event(self) -> None:
        """from_dict restores event correctly."""
        original = StatusChanged(
            aggregate_id="12345",
            aggregate_type="WorkItem",
            old_status="pending",
            new_status="in_progress",
            reason="Test reason",
        )
        data = original.to_dict()
        restored = StatusChanged.from_dict(data)

        assert restored.old_status == original.old_status
        assert restored.new_status == original.new_status
        assert restored.reason == original.reason


# =============================================================================
# WorkItemCompleted Tests
# =============================================================================


class TestWorkItemCompleted:
    """Tests for WorkItemCompleted event."""

    def test_create_with_completion_data(self) -> None:
        """Create event with completion data."""
        event = WorkItemCompleted(
            aggregate_id="12345",
            aggregate_type="WorkItem",
            final_status="done",
            duration_seconds=3600,
            completion_reason="All tests pass",
        )
        assert event.final_status == "done"
        assert event.duration_seconds == 3600
        assert event.completion_reason == "All tests pass"

    def test_payload_includes_completion_fields(self) -> None:
        """Payload includes completion fields."""
        event = WorkItemCompleted(
            aggregate_id="12345",
            aggregate_type="WorkItem",
            final_status="cancelled",
            duration_seconds=1800,
        )
        payload = event._payload()

        assert payload["final_status"] == "cancelled"
        assert payload["duration_seconds"] == 1800
        assert payload["completion_reason"] is None

    def test_from_dict_restores_event(self) -> None:
        """from_dict restores event correctly."""
        original = WorkItemCompleted(
            aggregate_id="12345",
            aggregate_type="WorkItem",
            final_status="done",
            duration_seconds=7200,
        )
        data = original.to_dict()
        restored = WorkItemCompleted.from_dict(data)

        assert restored.final_status == original.final_status
        assert restored.duration_seconds == original.duration_seconds


# =============================================================================
# PriorityChanged Tests
# =============================================================================


class TestPriorityChanged:
    """Tests for PriorityChanged event."""

    def test_create_with_priorities(self) -> None:
        """Create event with priority change."""
        event = PriorityChanged(
            aggregate_id="12345",
            aggregate_type="WorkItem",
            old_priority="medium",
            new_priority="critical",
            reason="Production issue",
        )
        assert event.old_priority == "medium"
        assert event.new_priority == "critical"
        assert event.reason == "Production issue"

    def test_payload_includes_priority_fields(self) -> None:
        """Payload includes priority fields."""
        event = PriorityChanged(
            aggregate_id="12345",
            aggregate_type="WorkItem",
            old_priority="low",
            new_priority="high",
        )
        payload = event._payload()

        assert payload["old_priority"] == "low"
        assert payload["new_priority"] == "high"

    def test_from_dict_restores_event(self) -> None:
        """from_dict restores event correctly."""
        original = PriorityChanged(
            aggregate_id="12345",
            aggregate_type="WorkItem",
            old_priority="medium",
            new_priority="high",
        )
        data = original.to_dict()
        restored = PriorityChanged.from_dict(data)

        assert restored.old_priority == original.old_priority
        assert restored.new_priority == original.new_priority


# =============================================================================
# QualityMetricsUpdated Tests
# =============================================================================


class TestQualityMetricsUpdated:
    """Tests for QualityMetricsUpdated event."""

    def test_create_with_metrics(self) -> None:
        """Create event with quality metrics."""
        event = QualityMetricsUpdated(
            aggregate_id="12345",
            aggregate_type="WorkItem",
            coverage_percent=85.5,
            positive_tests=10,
            negative_tests=5,
            edge_case_tests=3,
            gate_level="L2",
            gate_passed=True,
        )
        assert event.coverage_percent == 85.5
        assert event.positive_tests == 10
        assert event.gate_passed is True

    def test_payload_includes_metrics_fields(self) -> None:
        """Payload includes all metrics fields."""
        event = QualityMetricsUpdated(
            aggregate_id="12345",
            aggregate_type="WorkItem",
            coverage_percent=80.0,
            positive_tests=8,
            negative_tests=4,
            edge_case_tests=2,
            gate_level="L1",
            gate_passed=True,
            gate_failures=(),
        )
        payload = event._payload()

        assert payload["coverage_percent"] == 80.0
        assert payload["positive_tests"] == 8
        assert payload["negative_tests"] == 4
        assert payload["edge_case_tests"] == 2
        assert payload["gate_level"] == "L1"
        assert payload["gate_passed"] is True
        assert payload["gate_failures"] == []

    def test_gate_failures_as_list_in_payload(self) -> None:
        """gate_failures converted to list in payload."""
        event = QualityMetricsUpdated(
            aggregate_id="12345",
            aggregate_type="WorkItem",
            gate_failures=("Missing coverage", "No edge tests"),
        )
        payload = event._payload()

        assert payload["gate_failures"] == ["Missing coverage", "No edge tests"]

    def test_from_dict_restores_event(self) -> None:
        """from_dict restores event correctly."""
        original = QualityMetricsUpdated(
            aggregate_id="12345",
            aggregate_type="WorkItem",
            coverage_percent=90.0,
            positive_tests=15,
            negative_tests=7,
            edge_case_tests=5,
            gate_level="L2",
            gate_passed=True,
            gate_failures=(),
        )
        data = original.to_dict()
        restored = QualityMetricsUpdated.from_dict(data)

        assert restored.coverage_percent == original.coverage_percent
        assert restored.positive_tests == original.positive_tests
        assert restored.gate_passed == original.gate_passed

    def test_from_dict_converts_list_to_tuple(self) -> None:
        """from_dict converts gate_failures list to tuple."""
        data = {
            "aggregate_id": "12345",
            "aggregate_type": "WorkItem",
            "gate_failures": ["Error 1", "Error 2"],
        }
        event = QualityMetricsUpdated.from_dict(data)

        assert event.gate_failures == ("Error 1", "Error 2")


# =============================================================================
# DependencyAdded Tests
# =============================================================================


class TestDependencyAdded:
    """Tests for DependencyAdded event."""

    def test_create_with_dependency(self) -> None:
        """Create event with dependency data."""
        event = DependencyAdded(
            aggregate_id="12345",
            aggregate_type="WorkItem",
            dependency_id="67890",
            dependency_type="blocks",
        )
        assert event.dependency_id == "67890"
        assert event.dependency_type == "blocks"

    def test_payload_includes_dependency_fields(self) -> None:
        """Payload includes dependency fields."""
        event = DependencyAdded(
            aggregate_id="12345",
            aggregate_type="WorkItem",
            dependency_id="99999",
            dependency_type="related",
        )
        payload = event._payload()

        assert payload["dependency_id"] == "99999"
        assert payload["dependency_type"] == "related"

    def test_from_dict_restores_event(self) -> None:
        """from_dict restores event correctly."""
        original = DependencyAdded(
            aggregate_id="12345",
            aggregate_type="WorkItem",
            dependency_id="67890",
            dependency_type="blocks",
        )
        data = original.to_dict()
        restored = DependencyAdded.from_dict(data)

        assert restored.dependency_id == original.dependency_id
        assert restored.dependency_type == original.dependency_type


# =============================================================================
# DependencyRemoved Tests
# =============================================================================


class TestDependencyRemoved:
    """Tests for DependencyRemoved event."""

    def test_create_with_dependency(self) -> None:
        """Create event with dependency ID."""
        event = DependencyRemoved(
            aggregate_id="12345",
            aggregate_type="WorkItem",
            dependency_id="67890",
        )
        assert event.dependency_id == "67890"

    def test_payload_includes_dependency_id(self) -> None:
        """Payload includes dependency_id."""
        event = DependencyRemoved(
            aggregate_id="12345",
            aggregate_type="WorkItem",
            dependency_id="99999",
        )
        payload = event._payload()

        assert payload["dependency_id"] == "99999"

    def test_from_dict_restores_event(self) -> None:
        """from_dict restores event correctly."""
        original = DependencyRemoved(
            aggregate_id="12345",
            aggregate_type="WorkItem",
            dependency_id="67890",
        )
        data = original.to_dict()
        restored = DependencyRemoved.from_dict(data)

        assert restored.dependency_id == original.dependency_id


# =============================================================================
# AssigneeChanged Tests
# =============================================================================


class TestAssigneeChanged:
    """Tests for AssigneeChanged event."""

    def test_create_with_assignees(self) -> None:
        """Create event with assignee change."""
        event = AssigneeChanged(
            aggregate_id="12345",
            aggregate_type="WorkItem",
            old_assignee=None,
            new_assignee="agent:developer",
        )
        assert event.old_assignee is None
        assert event.new_assignee == "agent:developer"

    def test_payload_includes_assignee_fields(self) -> None:
        """Payload includes assignee fields."""
        event = AssigneeChanged(
            aggregate_id="12345",
            aggregate_type="WorkItem",
            old_assignee="user:john",
            new_assignee="user:jane",
        )
        payload = event._payload()

        assert payload["old_assignee"] == "user:john"
        assert payload["new_assignee"] == "user:jane"

    def test_from_dict_restores_event(self) -> None:
        """from_dict restores event correctly."""
        original = AssigneeChanged(
            aggregate_id="12345",
            aggregate_type="WorkItem",
            old_assignee="agent:qa",
            new_assignee=None,
        )
        data = original.to_dict()
        restored = AssigneeChanged.from_dict(data)

        assert restored.old_assignee == original.old_assignee
        assert restored.new_assignee == original.new_assignee

    def test_unassign_event(self) -> None:
        """Event for unassignment has None new_assignee."""
        event = AssigneeChanged(
            aggregate_id="12345",
            aggregate_type="WorkItem",
            old_assignee="user:john",
            new_assignee=None,
        )
        assert event.old_assignee == "user:john"
        assert event.new_assignee is None


# =============================================================================
# Event Base Class Integration Tests
# =============================================================================


class TestEventBaseIntegration:
    """Tests for DomainEvent base class integration."""

    def test_event_has_event_id(self) -> None:
        """All events have auto-generated event_id."""
        event = WorkItemCreated(
            aggregate_id="12345",
            aggregate_type="WorkItem",
        )
        assert event.event_id is not None
        assert len(event.event_id) > 0

    def test_event_has_timestamp(self) -> None:
        """All events have timestamp."""
        event = StatusChanged(
            aggregate_id="12345",
            aggregate_type="WorkItem",
            old_status="pending",
            new_status="in_progress",
        )
        assert event.timestamp is not None
        assert isinstance(event.timestamp, datetime)

    def test_event_has_version(self) -> None:
        """All events have version number."""
        event = PriorityChanged(
            aggregate_id="12345",
            aggregate_type="WorkItem",
            version=5,
        )
        assert event.version == 5

    def test_events_are_immutable(self) -> None:
        """Events are frozen dataclasses."""
        event = WorkItemCreated(
            aggregate_id="12345",
            aggregate_type="WorkItem",
            title="Test",
        )
        with pytest.raises(Exception):  # FrozenInstanceError
            event.title = "Changed"  # type: ignore

    def test_events_are_hashable(self) -> None:
        """Events can be used in sets."""
        event1 = WorkItemCreated(
            aggregate_id="12345",
            aggregate_type="WorkItem",
        )
        event2 = StatusChanged(
            aggregate_id="12345",
            aggregate_type="WorkItem",
        )
        event_set = {event1, event2}
        assert len(event_set) == 2
