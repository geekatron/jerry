"""Unit tests for shared_kernel.vertex_id module."""

from __future__ import annotations

import pytest

from src.shared_kernel.vertex_id import (
    ActorId,
    EdgeId,
    EventId,
    KnowledgeId,
    PhaseId,
    PlanId,
    SubtaskId,
    TaskId,
)


class TestTaskId:
    """Tests for TaskId."""

    def test_generate_creates_valid_id(self) -> None:
        """TaskId.generate() creates valid format."""
        task_id = TaskId.generate()
        assert task_id.value.startswith("TASK-")
        assert len(task_id.value) == 13  # TASK- + 8 hex chars

    def test_from_string_valid(self) -> None:
        """TaskId.from_string() accepts valid format."""
        task_id = TaskId.from_string("TASK-a1b2c3d4")
        assert task_id.value == "TASK-a1b2c3d4"

    def test_from_string_invalid_raises(self) -> None:
        """TaskId.from_string() rejects invalid format."""
        with pytest.raises(ValueError, match="Invalid TaskId format"):
            TaskId.from_string("INVALID")

    def test_equality(self) -> None:
        """TaskIds with same value are equal."""
        id1 = TaskId("TASK-a1b2c3d4")
        id2 = TaskId("TASK-a1b2c3d4")
        assert id1 == id2

    def test_hash(self) -> None:
        """TaskIds with same value have same hash."""
        id1 = TaskId("TASK-a1b2c3d4")
        id2 = TaskId("TASK-a1b2c3d4")
        assert hash(id1) == hash(id2)

    def test_str(self) -> None:
        """str(TaskId) returns value."""
        task_id = TaskId("TASK-a1b2c3d4")
        assert str(task_id) == "TASK-a1b2c3d4"

    def test_invalid_uppercase_hex_rejected(self) -> None:
        """TaskId rejects uppercase hex characters."""
        with pytest.raises(ValueError):
            TaskId("TASK-A1B2C3D4")


class TestPhaseId:
    """Tests for PhaseId."""

    def test_generate_creates_valid_id(self) -> None:
        """PhaseId.generate() creates valid format."""
        phase_id = PhaseId.generate()
        assert phase_id.value.startswith("PHASE-")
        assert len(phase_id.value) == 14  # PHASE- + 8 hex chars

    def test_from_string_valid(self) -> None:
        """PhaseId.from_string() accepts valid format."""
        phase_id = PhaseId.from_string("PHASE-e5f6a7b8")
        assert phase_id.value == "PHASE-e5f6a7b8"


class TestPlanId:
    """Tests for PlanId."""

    def test_generate_creates_valid_id(self) -> None:
        """PlanId.generate() creates valid format."""
        plan_id = PlanId.generate()
        assert plan_id.value.startswith("PLAN-")
        assert len(plan_id.value) == 13  # PLAN- + 8 hex chars


class TestSubtaskId:
    """Tests for SubtaskId."""

    def test_from_parent_creates_valid_id(self) -> None:
        """SubtaskId.from_parent() creates valid format."""
        parent = TaskId("TASK-a1b2c3d4")
        subtask_id = SubtaskId.from_parent(parent, sequence=1)
        assert subtask_id.value == "TASK-a1b2c3d4.1"

    def test_parent_id_extraction(self) -> None:
        """SubtaskId.parent_id extracts correct TaskId."""
        subtask_id = SubtaskId("TASK-a1b2c3d4.5")
        assert subtask_id.parent_id.value == "TASK-a1b2c3d4"

    def test_sequence_extraction(self) -> None:
        """SubtaskId.sequence extracts correct number."""
        subtask_id = SubtaskId("TASK-a1b2c3d4.5")
        assert subtask_id.sequence == 5

    def test_generate_raises(self) -> None:
        """SubtaskId.generate() raises NotImplementedError."""
        with pytest.raises(NotImplementedError):
            SubtaskId.generate()

    def test_sequence_must_be_positive(self) -> None:
        """SubtaskId rejects sequence < 1."""
        parent = TaskId("TASK-a1b2c3d4")
        with pytest.raises(ValueError, match="sequence must be >= 1"):
            SubtaskId.from_parent(parent, sequence=0)


class TestKnowledgeId:
    """Tests for KnowledgeId."""

    def test_generate_creates_valid_id(self) -> None:
        """KnowledgeId.generate() creates valid format."""
        know_id = KnowledgeId.generate()
        assert know_id.value.startswith("KNOW-")
        assert len(know_id.value) == 13


class TestActorId:
    """Tests for ActorId."""

    def test_for_type_creates_valid_id(self) -> None:
        """ActorId.for_type() creates valid format."""
        actor_id = ActorId.for_type("HUMAN", "user123")
        assert actor_id.value == "ACTOR-HUMAN-user123"

    def test_claude_creates_valid_id(self) -> None:
        """ActorId.claude() creates Claude actor."""
        actor_id = ActorId.claude()
        assert actor_id.value == "ACTOR-CLAUDE-main"

    def test_claude_with_instance(self) -> None:
        """ActorId.claude() accepts instance name."""
        actor_id = ActorId.claude("worker1")
        assert actor_id.value == "ACTOR-CLAUDE-worker1"

    def test_system_creates_valid_id(self) -> None:
        """ActorId.system() creates system actor."""
        actor_id = ActorId.system()
        assert actor_id.value == "ACTOR-SYSTEM-internal"

    def test_type_must_be_uppercase(self) -> None:
        """ActorId rejects lowercase type."""
        with pytest.raises(ValueError, match="uppercase"):
            ActorId.for_type("human", "user123")

    def test_generate_raises(self) -> None:
        """ActorId.generate() raises NotImplementedError."""
        with pytest.raises(NotImplementedError):
            ActorId.generate()


class TestEventId:
    """Tests for EventId."""

    def test_generate_creates_valid_id(self) -> None:
        """EventId.generate() creates valid UUID format."""
        event_id = EventId.generate()
        assert event_id.value.startswith("EVT-")
        # UUID format: EVT-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
        assert len(event_id.value) == 40


class TestEdgeId:
    """Tests for EdgeId."""

    def test_edge_id_value(self) -> None:
        """EdgeId.value combines source, label, target."""
        source = PhaseId("PHASE-e5f6a7b8")
        target = TaskId("TASK-a1b2c3d4")
        edge = EdgeId(source, target, "CONTAINS")
        assert edge.value == "PHASE-e5f6a7b8--CONTAINS-->TASK-a1b2c3d4"

    def test_edge_str(self) -> None:
        """str(EdgeId) returns value."""
        source = PhaseId("PHASE-e5f6a7b8")
        target = TaskId("TASK-a1b2c3d4")
        edge = EdgeId(source, target, "CONTAINS")
        assert str(edge) == "PHASE-e5f6a7b8--CONTAINS-->TASK-a1b2c3d4"

    def test_label_must_be_uppercase(self) -> None:
        """EdgeId rejects lowercase label."""
        source = PhaseId("PHASE-e5f6a7b8")
        target = TaskId("TASK-a1b2c3d4")
        with pytest.raises(ValueError, match="uppercase"):
            EdgeId(source, target, "contains")

    def test_label_cannot_be_empty(self) -> None:
        """EdgeId rejects empty label."""
        source = PhaseId("PHASE-e5f6a7b8")
        target = TaskId("TASK-a1b2c3d4")
        with pytest.raises(ValueError, match="empty"):
            EdgeId(source, target, "")

    def test_edge_hash(self) -> None:
        """EdgeIds with same components have same hash."""
        source = PhaseId("PHASE-e5f6a7b8")
        target = TaskId("TASK-a1b2c3d4")
        edge1 = EdgeId(source, target, "CONTAINS")
        edge2 = EdgeId(source, target, "CONTAINS")
        assert hash(edge1) == hash(edge2)
