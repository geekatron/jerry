"""Unit tests for Work Item Commands.

Test Categories:
    - CreateWorkItemCommand: Create new work items
    - StartWorkItemCommand: Start work on items
    - CompleteWorkItemCommand: Complete work items
    - BlockWorkItemCommand: Block work items
    - CancelWorkItemCommand: Cancel work items

References:
    - PHASE-45-ITEMS-COMMANDS.md: Implementation tracker
    - PAT-CQRS-001: Command Pattern

Test Matrix:
    Happy Path:
        - Commands are frozen dataclasses
        - Commands have expected default values
        - Commands accept all required parameters
    Negative:
        - Commands reject type mismatches (via type checker)
    Edge:
        - Commands with empty strings
        - Commands with None for optional fields
"""

from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest

from src.work_tracking.application.commands import (
    BlockWorkItemCommand,
    CancelWorkItemCommand,
    CompleteWorkItemCommand,
    CreateWorkItemCommand,
    StartWorkItemCommand,
)

# =============================================================================
# CreateWorkItemCommand Tests
# =============================================================================


class TestCreateWorkItemCommand:
    """Tests for CreateWorkItemCommand."""

    def test_create_with_title_only(self) -> None:
        """Create command with minimal required field."""
        command = CreateWorkItemCommand(title="Test task")

        assert command.title == "Test task"
        assert command.work_type == "task"
        assert command.priority == "medium"
        assert command.description == ""
        assert command.parent_id is None

    def test_create_with_all_fields(self) -> None:
        """Create command with all fields specified."""
        command = CreateWorkItemCommand(
            title="Bug fix",
            work_type="bug",
            priority="high",
            description="Fix the login issue",
            parent_id="WORK-001",
        )

        assert command.title == "Bug fix"
        assert command.work_type == "bug"
        assert command.priority == "high"
        assert command.description == "Fix the login issue"
        assert command.parent_id == "WORK-001"

    def test_command_is_frozen(self) -> None:
        """Command should be immutable."""
        command = CreateWorkItemCommand(title="Test")

        with pytest.raises(FrozenInstanceError):
            command.title = "Modified"  # type: ignore[misc]

    def test_command_with_empty_title(self) -> None:
        """Command accepts empty title (validation happens in handler)."""
        command = CreateWorkItemCommand(title="")
        assert command.title == ""


# =============================================================================
# StartWorkItemCommand Tests
# =============================================================================


class TestStartWorkItemCommand:
    """Tests for StartWorkItemCommand."""

    def test_create_with_id_only(self) -> None:
        """Create command with minimal required field."""
        command = StartWorkItemCommand(work_item_id="WORK-001")

        assert command.work_item_id == "WORK-001"
        assert command.reason is None

    def test_create_with_reason(self) -> None:
        """Create command with optional reason."""
        command = StartWorkItemCommand(
            work_item_id="WORK-001",
            reason="Starting implementation",
        )

        assert command.work_item_id == "WORK-001"
        assert command.reason == "Starting implementation"

    def test_command_is_frozen(self) -> None:
        """Command should be immutable."""
        command = StartWorkItemCommand(work_item_id="WORK-001")

        with pytest.raises(FrozenInstanceError):
            command.work_item_id = "WORK-002"  # type: ignore[misc]


# =============================================================================
# CompleteWorkItemCommand Tests
# =============================================================================


class TestCompleteWorkItemCommand:
    """Tests for CompleteWorkItemCommand."""

    def test_create_with_id_only(self) -> None:
        """Create command with minimal required field."""
        command = CompleteWorkItemCommand(work_item_id="WORK-001")

        assert command.work_item_id == "WORK-001"
        assert command.reason is None

    def test_create_with_reason(self) -> None:
        """Create command with optional reason."""
        command = CompleteWorkItemCommand(
            work_item_id="WORK-001",
            reason="Implementation done, tests passing",
        )

        assert command.work_item_id == "WORK-001"
        assert command.reason == "Implementation done, tests passing"

    def test_command_is_frozen(self) -> None:
        """Command should be immutable."""
        command = CompleteWorkItemCommand(work_item_id="WORK-001")

        with pytest.raises(FrozenInstanceError):
            command.work_item_id = "WORK-002"  # type: ignore[misc]


# =============================================================================
# BlockWorkItemCommand Tests
# =============================================================================


class TestBlockWorkItemCommand:
    """Tests for BlockWorkItemCommand."""

    def test_create_requires_reason(self) -> None:
        """Create command requires reason (not optional)."""
        command = BlockWorkItemCommand(
            work_item_id="WORK-001",
            reason="Waiting for API specification",
        )

        assert command.work_item_id == "WORK-001"
        assert command.reason == "Waiting for API specification"

    def test_command_is_frozen(self) -> None:
        """Command should be immutable."""
        command = BlockWorkItemCommand(
            work_item_id="WORK-001",
            reason="Blocked",
        )

        with pytest.raises(FrozenInstanceError):
            command.reason = "Different reason"  # type: ignore[misc]


# =============================================================================
# CancelWorkItemCommand Tests
# =============================================================================


class TestCancelWorkItemCommand:
    """Tests for CancelWorkItemCommand."""

    def test_create_with_id_only(self) -> None:
        """Create command with minimal required field."""
        command = CancelWorkItemCommand(work_item_id="WORK-001")

        assert command.work_item_id == "WORK-001"
        assert command.reason is None

    def test_create_with_reason(self) -> None:
        """Create command with optional reason."""
        command = CancelWorkItemCommand(
            work_item_id="WORK-001",
            reason="Requirements changed",
        )

        assert command.work_item_id == "WORK-001"
        assert command.reason == "Requirements changed"

    def test_command_is_frozen(self) -> None:
        """Command should be immutable."""
        command = CancelWorkItemCommand(work_item_id="WORK-001")

        with pytest.raises(FrozenInstanceError):
            command.work_item_id = "WORK-002"  # type: ignore[misc]
