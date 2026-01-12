"""
Integration tests for Items Commands (Phase 4.5).

Tests the complete chain:
- CLI -> CommandDispatcher -> Handler -> Repository -> EventStore
- Event persistence verification (filesystem)
- Full work item lifecycle (create -> start -> complete)

References:
    - PHASE-45-ITEMS-COMMANDS.md: Implementation tracker
    - TD-018: Event Sourcing infrastructure

Test Categories:
    - TestCommandDispatcherIntegration: CommandDispatcher with work item commands
    - TestEventPersistence: Work item events persisted to filesystem
    - TestWorkItemLifecycle: Full lifecycle through dispatcher
    - TestCLIAdapterIntegration: CLIAdapter -> CommandDispatcher E2E
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from src.bootstrap import (
    create_command_dispatcher,
    create_event_store,
    create_query_dispatcher,
    create_work_item_repository,
    reset_singletons,
)
from src.interface.cli.adapter import CLIAdapter
from src.work_tracking.application.commands import (
    BlockWorkItemCommand,
    CancelWorkItemCommand,
    CompleteWorkItemCommand,
    CreateWorkItemCommand,
    StartWorkItemCommand,
)
from src.work_tracking.domain.events import StatusChanged, WorkItemCreated
from src.work_tracking.domain.ports.repository import AggregateNotFoundError
from src.work_tracking.domain.value_objects import Coverage, TypeRatio

# =============================================================================
# Test Fixtures
# =============================================================================


@pytest.fixture(autouse=True)
def reset_bootstrap() -> None:
    """Reset bootstrap singletons before each test."""
    reset_singletons()
    yield
    reset_singletons()


# =============================================================================
# CommandDispatcher Integration Tests (Task 4.5.6.1)
# =============================================================================


class TestCommandDispatcherIntegration:
    """Integration tests for CommandDispatcher with work item commands."""

    def test_command_dispatcher_has_work_item_handlers(self) -> None:
        """CommandDispatcher is configured with all work item commands."""
        dispatcher = create_command_dispatcher()

        assert dispatcher.has_handler(CreateWorkItemCommand)
        assert dispatcher.has_handler(StartWorkItemCommand)
        assert dispatcher.has_handler(CompleteWorkItemCommand)
        assert dispatcher.has_handler(BlockWorkItemCommand)
        assert dispatcher.has_handler(CancelWorkItemCommand)

    def test_create_work_item_via_dispatcher(self) -> None:
        """CreateWorkItemCommand works through dispatcher."""
        dispatcher = create_command_dispatcher()

        command = CreateWorkItemCommand(
            title="Integration Test Task",
            work_type="task",
            priority="high",
            description="Created via dispatcher",
        )
        events = dispatcher.dispatch(command)

        assert len(events) >= 1
        assert isinstance(events[0], WorkItemCreated)
        assert events[0].title == "Integration Test Task"
        assert events[0].work_type == "task"
        assert events[0].priority == "high"

    def test_start_work_item_via_dispatcher(self) -> None:
        """StartWorkItemCommand works through dispatcher."""
        dispatcher = create_command_dispatcher()

        # First create a work item
        create_cmd = CreateWorkItemCommand(title="Start Test Task")
        create_events = dispatcher.dispatch(create_cmd)
        work_item_id = create_events[0].aggregate_id

        # Now start it
        start_cmd = StartWorkItemCommand(
            work_item_id=work_item_id,
            reason="Beginning work",
        )
        start_events = dispatcher.dispatch(start_cmd)

        assert len(start_events) >= 1
        assert isinstance(start_events[0], StatusChanged)
        assert start_events[0].old_status == "pending"
        assert start_events[0].new_status == "in_progress"

    def test_block_work_item_via_dispatcher(self) -> None:
        """BlockWorkItemCommand works through dispatcher."""
        dispatcher = create_command_dispatcher()

        # Create and start work item
        create_cmd = CreateWorkItemCommand(title="Block Test Task")
        create_events = dispatcher.dispatch(create_cmd)
        work_item_id = create_events[0].aggregate_id

        start_cmd = StartWorkItemCommand(work_item_id=work_item_id)
        dispatcher.dispatch(start_cmd)

        # Block it
        block_cmd = BlockWorkItemCommand(
            work_item_id=work_item_id,
            reason="Waiting for API access",
        )
        block_events = dispatcher.dispatch(block_cmd)

        assert len(block_events) >= 1
        assert isinstance(block_events[0], StatusChanged)
        assert block_events[0].new_status == "blocked"

    def test_cancel_work_item_via_dispatcher(self) -> None:
        """CancelWorkItemCommand works through dispatcher."""
        dispatcher = create_command_dispatcher()

        # Create a work item
        create_cmd = CreateWorkItemCommand(title="Cancel Test Task")
        create_events = dispatcher.dispatch(create_cmd)
        work_item_id = create_events[0].aggregate_id

        # Cancel it from pending state
        cancel_cmd = CancelWorkItemCommand(
            work_item_id=work_item_id,
            reason="No longer needed",
        )
        cancel_events = dispatcher.dispatch(cancel_cmd)

        assert len(cancel_events) >= 1
        assert isinstance(cancel_events[0], StatusChanged)
        assert cancel_events[0].new_status == "cancelled"

    def test_dispatcher_rejects_start_on_nonexistent_item(self) -> None:
        """StartWorkItemCommand fails for non-existent work item."""
        dispatcher = create_command_dispatcher()

        command = StartWorkItemCommand(work_item_id="WORK-99999-1")

        with pytest.raises(AggregateNotFoundError):
            dispatcher.dispatch(command)


# =============================================================================
# Event Persistence Tests (Task 4.5.6.2)
# =============================================================================


class TestEventPersistence:
    """Tests for event persistence to filesystem."""

    def test_create_work_item_persists_event_to_filesystem(self, tmp_path: Path) -> None:
        """CreateWorkItemCommand persists WorkItemCreated event to file."""
        store = create_event_store(project_path=tmp_path)
        repo = create_work_item_repository(event_store=store)

        # We need to use the repo directly to ensure we're using the tmp_path store
        from src.work_tracking.domain.aggregates.work_item import WorkItem
        from src.work_tracking.domain.services.id_generator import WorkItemIdGenerator
        from src.work_tracking.domain.value_objects import Priority, WorkType

        id_gen = WorkItemIdGenerator()
        work_item_id = id_gen.create()

        work_item = WorkItem.create(
            id=work_item_id,
            title="Persistent Task",
            work_type=WorkType.TASK,
            priority=Priority.HIGH,
        )
        repo.save(work_item)

        # Verify event file exists
        events_dir = tmp_path / ".jerry" / "data" / "events"
        event_files = list(events_dir.glob("*.jsonl"))
        assert len(event_files) == 1

        # Verify content
        content = event_files[0].read_text()
        lines = content.strip().split("\n")
        assert len(lines) >= 1

        event_data = json.loads(lines[0])
        assert event_data["event_type"] == "WorkItemCreated"
        # Event data is nested in "data" field
        assert event_data["data"]["title"] == "Persistent Task"

    def test_start_work_item_persists_status_change_event(self, tmp_path: Path) -> None:
        """StartWorkItemCommand persists StatusChanged event to file."""
        store = create_event_store(project_path=tmp_path)
        repo = create_work_item_repository(event_store=store)

        from src.work_tracking.domain.aggregates.work_item import WorkItem
        from src.work_tracking.domain.services.id_generator import WorkItemIdGenerator
        from src.work_tracking.domain.value_objects import Priority, WorkType

        id_gen = WorkItemIdGenerator()
        work_item_id = id_gen.create()

        # Create work item
        work_item = WorkItem.create(
            id=work_item_id,
            title="Start Persistence Test",
            work_type=WorkType.TASK,
            priority=Priority.MEDIUM,
        )
        repo.save(work_item)

        # Clear events and start work
        work_item.collect_events()
        work_item.start_work()
        repo.save(work_item)

        # Verify events file has both events
        events_dir = tmp_path / ".jerry" / "data" / "events"
        event_files = list(events_dir.glob("*.jsonl"))
        assert len(event_files) == 1

        content = event_files[0].read_text()
        lines = content.strip().split("\n")
        assert len(lines) == 2

        # First event should be WorkItemCreated
        event1 = json.loads(lines[0])
        assert event1["event_type"] == "WorkItemCreated"

        # Second event should be StatusChanged
        event2 = json.loads(lines[1])
        assert event2["event_type"] == "StatusChanged"
        # Event data is nested in "data" field
        assert event2["data"]["old_status"] == "pending"
        assert event2["data"]["new_status"] == "in_progress"

    def test_work_item_survives_repository_recreation(self, tmp_path: Path) -> None:
        """Work item survives repository recreation (simulates app restart)."""
        from src.work_tracking.domain.aggregates.work_item import WorkItem
        from src.work_tracking.domain.services.id_generator import WorkItemIdGenerator
        from src.work_tracking.domain.value_objects import Priority, WorkType

        id_gen = WorkItemIdGenerator()
        work_item_id = id_gen.create()

        # First "session" - create and start work item
        store1 = create_event_store(project_path=tmp_path)
        repo1 = create_work_item_repository(event_store=store1)

        work_item = WorkItem.create(
            id=work_item_id,
            title="Survives Restart",
            work_type=WorkType.BUG,
            priority=Priority.HIGH,
        )
        work_item.start_work()
        repo1.save(work_item)

        # "Restart" - create new repository
        del repo1, store1

        store2 = create_event_store(project_path=tmp_path)
        repo2 = create_work_item_repository(event_store=store2)

        # Load and verify (use string ID from the work_item)
        loaded = repo2.get(work_item.id)

        assert loaded is not None
        assert loaded.title == "Survives Restart"
        assert loaded.status.name == "IN_PROGRESS"
        assert loaded.work_type == WorkType.BUG
        assert loaded.priority == Priority.HIGH


# =============================================================================
# Full Work Item Lifecycle Tests (Task 4.5.6.3)
# =============================================================================


class TestWorkItemLifecycle:
    """Tests for full work item lifecycle through dispatcher."""

    def test_full_lifecycle_create_start_complete(self) -> None:
        """Full lifecycle: create -> start -> add quality -> complete."""
        dispatcher = create_command_dispatcher()

        # Step 1: Create
        create_cmd = CreateWorkItemCommand(
            title="Lifecycle Test Task",
            work_type="task",
            priority="high",
        )
        create_events = dispatcher.dispatch(create_cmd)
        work_item_id = create_events[0].aggregate_id

        assert isinstance(create_events[0], WorkItemCreated)

        # Step 2: Start
        start_cmd = StartWorkItemCommand(work_item_id=work_item_id)
        start_events = dispatcher.dispatch(start_cmd)

        assert isinstance(start_events[0], StatusChanged)
        assert start_events[0].new_status == "in_progress"

        # Step 3: Add quality metrics (required for completion)
        # We need to access the repository directly to update quality
        repo = create_work_item_repository()
        work_item = repo.get_or_raise(work_item_id)
        work_item.update_quality_metrics(
            coverage=Coverage(percent=85.0),
            ratio=TypeRatio(positive=10, negative=5, edge_case=3),
        )
        repo.save(work_item)

        # Step 4: Complete
        complete_cmd = CompleteWorkItemCommand(
            work_item_id=work_item_id,
            reason="All tests passing",
        )
        complete_events = dispatcher.dispatch(complete_cmd)

        # Verify completion events
        status_events = [e for e in complete_events if isinstance(e, StatusChanged)]
        assert len(status_events) >= 1
        assert status_events[0].new_status == "done"

    def test_lifecycle_create_start_block_cancel(self) -> None:
        """Lifecycle: create -> start -> block -> cancel."""
        dispatcher = create_command_dispatcher()

        # Create
        create_cmd = CreateWorkItemCommand(title="Block-Cancel Test")
        create_events = dispatcher.dispatch(create_cmd)
        work_item_id = create_events[0].aggregate_id

        # Start
        start_cmd = StartWorkItemCommand(work_item_id=work_item_id)
        dispatcher.dispatch(start_cmd)

        # Block
        block_cmd = BlockWorkItemCommand(
            work_item_id=work_item_id,
            reason="External dependency unavailable",
        )
        block_events = dispatcher.dispatch(block_cmd)
        assert block_events[0].new_status == "blocked"

        # Cancel from blocked state
        cancel_cmd = CancelWorkItemCommand(
            work_item_id=work_item_id,
            reason="Dependency will not be available",
        )
        cancel_events = dispatcher.dispatch(cancel_cmd)
        assert cancel_events[0].new_status == "cancelled"

    def test_lifecycle_with_filesystem_persistence(self, tmp_path: Path) -> None:
        """Full lifecycle persists all events to filesystem."""
        from src.work_tracking.domain.services.id_generator import WorkItemIdGenerator

        store = create_event_store(project_path=tmp_path)
        repo = create_work_item_repository(event_store=store)

        from src.work_tracking.domain.aggregates.work_item import WorkItem
        from src.work_tracking.domain.value_objects import Priority, WorkType

        id_gen = WorkItemIdGenerator()
        work_item_id = id_gen.create()

        # Create
        work_item = WorkItem.create(
            id=work_item_id,
            title="Persisted Lifecycle",
            work_type=WorkType.STORY,
            priority=Priority.HIGH,
        )
        repo.save(work_item)

        # Start
        work_item.collect_events()
        work_item.start_work()
        repo.save(work_item)

        # Add quality
        work_item.collect_events()
        work_item.update_quality_metrics(
            coverage=Coverage(percent=90.0),
            ratio=TypeRatio(positive=8, negative=4, edge_case=2),
        )
        repo.save(work_item)

        # Complete
        work_item.collect_events()
        work_item.complete()
        repo.save(work_item)

        # Verify all events are persisted
        events_dir = tmp_path / ".jerry" / "data" / "events"
        event_files = list(events_dir.glob("*.jsonl"))
        assert len(event_files) == 1

        content = event_files[0].read_text()
        lines = content.strip().split("\n")

        # Should have: WorkItemCreated, StatusChanged (start),
        # QualityMetricsUpdated, StatusChanged (complete), WorkItemCompleted
        assert len(lines) >= 4

        # Verify event types in order
        event_types = [json.loads(line)["event_type"] for line in lines]
        assert event_types[0] == "WorkItemCreated"
        assert event_types[1] == "StatusChanged"  # start
        assert event_types[2] == "QualityMetricsUpdated"
        assert "StatusChanged" in event_types[3:]  # complete

        # Reload from fresh repo to verify replay
        work_item_str_id = work_item.id  # Save before deleting
        del repo, store

        store2 = create_event_store(project_path=tmp_path)
        repo2 = create_work_item_repository(event_store=store2)
        loaded = repo2.get(work_item_str_id)

        assert loaded is not None
        assert loaded.status.name == "DONE"
        assert loaded.test_coverage is not None
        assert loaded.test_coverage.percent == 90.0


# =============================================================================
# CLI Adapter Integration Tests (E2E)
# =============================================================================


class TestCLIAdapterIntegration:
    """E2E tests for CLI Adapter with CommandDispatcher."""

    def test_cli_create_work_item(self, capsys: pytest.CaptureFixture) -> None:
        """CLIAdapter.cmd_items_create works end-to-end."""
        query_dispatcher = create_query_dispatcher()
        command_dispatcher = create_command_dispatcher()

        adapter = CLIAdapter(
            dispatcher=query_dispatcher,
            command_dispatcher=command_dispatcher,
        )

        exit_code = adapter.cmd_items_create(
            title="CLI Integration Test",
            work_type="task",
            priority="high",
            json_output=False,
        )

        assert exit_code == 0

        captured = capsys.readouterr()
        assert "Created work item:" in captured.out
        assert "CLI Integration Test" in captured.out

    def test_cli_create_work_item_json_output(self, capsys: pytest.CaptureFixture) -> None:
        """CLIAdapter.cmd_items_create returns valid JSON."""
        query_dispatcher = create_query_dispatcher()
        command_dispatcher = create_command_dispatcher()

        adapter = CLIAdapter(
            dispatcher=query_dispatcher,
            command_dispatcher=command_dispatcher,
        )

        exit_code = adapter.cmd_items_create(
            title="JSON Output Test",
            work_type="bug",
            priority="critical",
            json_output=True,
        )

        assert exit_code == 0

        captured = capsys.readouterr()
        output = json.loads(captured.out)

        assert output["success"] is True
        assert output["title"] == "JSON Output Test"
        assert output["work_type"] == "bug"
        assert output["priority"] == "critical"
        assert "work_item_id" in output

    def test_cli_start_work_item(self, capsys: pytest.CaptureFixture) -> None:
        """CLIAdapter.cmd_items_start works end-to-end."""
        query_dispatcher = create_query_dispatcher()
        command_dispatcher = create_command_dispatcher()

        adapter = CLIAdapter(
            dispatcher=query_dispatcher,
            command_dispatcher=command_dispatcher,
        )

        # Create item first
        adapter.cmd_items_create(
            title="Start CLI Test",
            json_output=True,
        )
        captured = capsys.readouterr()
        work_item_id = json.loads(captured.out)["work_item_id"]

        # Start it
        exit_code = adapter.cmd_items_start(
            item_id=work_item_id,
            json_output=False,
        )

        assert exit_code == 0

        captured = capsys.readouterr()
        assert "Started work item:" in captured.out
        assert "in_progress" in captured.out

    def test_cli_block_work_item(self, capsys: pytest.CaptureFixture) -> None:
        """CLIAdapter.cmd_items_block works end-to-end."""
        query_dispatcher = create_query_dispatcher()
        command_dispatcher = create_command_dispatcher()

        adapter = CLIAdapter(
            dispatcher=query_dispatcher,
            command_dispatcher=command_dispatcher,
        )

        # Create and start
        adapter.cmd_items_create(title="Block CLI Test", json_output=True)
        captured = capsys.readouterr()
        work_item_id = json.loads(captured.out)["work_item_id"]

        adapter.cmd_items_start(item_id=work_item_id, json_output=True)
        capsys.readouterr()

        # Block
        exit_code = adapter.cmd_items_block(
            item_id=work_item_id,
            reason="Waiting for review",
            json_output=True,
        )

        assert exit_code == 0

        captured = capsys.readouterr()
        output = json.loads(captured.out)
        assert output["status"] == "blocked"
        assert output["reason"] == "Waiting for review"

    def test_cli_cancel_work_item(self, capsys: pytest.CaptureFixture) -> None:
        """CLIAdapter.cmd_items_cancel works end-to-end."""
        query_dispatcher = create_query_dispatcher()
        command_dispatcher = create_command_dispatcher()

        adapter = CLIAdapter(
            dispatcher=query_dispatcher,
            command_dispatcher=command_dispatcher,
        )

        # Create
        adapter.cmd_items_create(title="Cancel CLI Test", json_output=True)
        captured = capsys.readouterr()
        work_item_id = json.loads(captured.out)["work_item_id"]

        # Cancel from pending
        exit_code = adapter.cmd_items_cancel(
            item_id=work_item_id,
            reason="Requirements changed",
            json_output=True,
        )

        assert exit_code == 0

        captured = capsys.readouterr()
        output = json.loads(captured.out)
        assert output["status"] == "cancelled"

    def test_cli_start_nonexistent_item_returns_error(self, capsys: pytest.CaptureFixture) -> None:
        """CLIAdapter.cmd_items_start returns error for non-existent item."""
        query_dispatcher = create_query_dispatcher()
        command_dispatcher = create_command_dispatcher()

        adapter = CLIAdapter(
            dispatcher=query_dispatcher,
            command_dispatcher=command_dispatcher,
        )

        exit_code = adapter.cmd_items_start(
            item_id="WORK-99999-1",
            json_output=True,
        )

        assert exit_code == 1

        captured = capsys.readouterr()
        output = json.loads(captured.out)
        assert "error" in output

    def test_cli_without_command_dispatcher_returns_error(
        self, capsys: pytest.CaptureFixture
    ) -> None:
        """CLIAdapter without command_dispatcher returns error for items commands."""
        query_dispatcher = create_query_dispatcher()

        adapter = CLIAdapter(
            dispatcher=query_dispatcher,
            command_dispatcher=None,  # No command dispatcher
        )

        exit_code = adapter.cmd_items_create(
            title="Should Fail",
            json_output=True,
        )

        assert exit_code == 1

        captured = capsys.readouterr()
        output = json.loads(captured.out)
        assert output["error"] == "Command dispatcher not configured"
