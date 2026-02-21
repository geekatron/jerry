# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
Integration tests for Event Sourcing wiring (TD-018 Phase 4).

Tests the complete chain:
- Bootstrap factories create correct instances
- CLI -> Handler -> Repository -> EventStore -> File

References:
    - TD-018: Event Sourcing for WorkItem Repository
    - Phase 4: Composition Root Wiring
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from src.work_tracking.domain.aggregates.work_item import WorkItem
from src.work_tracking.domain.value_objects import Priority, WorkItemId, WorkType


def create_work_item_id(internal_id: int) -> WorkItemId:
    """Helper to create a WorkItemId."""
    return WorkItemId.create(internal_id, 1)


def create_work_item(
    internal_id: int = 1,
    title: str = "Test Work Item",
    work_type: WorkType = WorkType.TASK,
    priority: Priority = Priority.MEDIUM,
) -> WorkItem:
    """Helper to create a WorkItem for testing."""
    return WorkItem.create(
        id=create_work_item_id(internal_id),
        title=title,
        work_type=work_type,
        priority=priority,
    )


class TestBootstrapFactories:
    """Tests for bootstrap factory functions."""

    def test_create_event_store_returns_in_memory_when_no_project(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Without project context, creates in-memory store."""
        from src.bootstrap import create_event_store
        from src.work_tracking.infrastructure.persistence.in_memory_event_store import (
            InMemoryEventStore,
        )

        # Clear JERRY_PROJECT env var to simulate no active project
        monkeypatch.delenv("JERRY_PROJECT", raising=False)

        store = create_event_store(project_path=None)

        assert isinstance(store, InMemoryEventStore)

    def test_create_event_store_returns_filesystem_with_project(self, tmp_path: Path) -> None:
        """With project path, creates filesystem store."""
        from src.bootstrap import create_event_store
        from src.work_tracking.infrastructure.persistence.filesystem_event_store import (
            FileSystemEventStore,
        )

        store = create_event_store(project_path=tmp_path)

        assert isinstance(store, FileSystemEventStore)

    def test_create_event_store_in_memory_flag(self) -> None:
        """use_in_memory=True forces in-memory store."""
        from src.bootstrap import create_event_store
        from src.work_tracking.infrastructure.persistence.in_memory_event_store import (
            InMemoryEventStore,
        )

        store = create_event_store(use_in_memory=True)

        assert isinstance(store, InMemoryEventStore)

    def test_create_work_item_repository_with_event_store(self, tmp_path: Path) -> None:
        """Creates EventSourcedWorkItemRepository with given store."""
        from src.bootstrap import create_event_store, create_work_item_repository
        from src.work_tracking.infrastructure.adapters.event_sourced_work_item_repository import (
            EventSourcedWorkItemRepository,
        )

        store = create_event_store(project_path=tmp_path)
        repo = create_work_item_repository(event_store=store)

        assert isinstance(repo, EventSourcedWorkItemRepository)

    def test_create_command_dispatcher_has_session_handlers(self) -> None:
        """CommandDispatcher is configured with session commands."""
        from src.bootstrap import create_command_dispatcher
        from src.session_management.application.commands import (
            AbandonSessionCommand,
            CreateSessionCommand,
            EndSessionCommand,
        )

        dispatcher = create_command_dispatcher()

        assert dispatcher.has_handler(CreateSessionCommand)
        assert dispatcher.has_handler(EndSessionCommand)
        assert dispatcher.has_handler(AbandonSessionCommand)

    def test_reset_singletons_clears_cached_instances(self) -> None:
        """reset_singletons() clears all cached instances."""
        from src.bootstrap import (
            get_event_store,
            get_session_repository,
            get_work_item_repository,
            reset_singletons,
        )

        # Access singletons to create them
        store1 = get_event_store()
        repo1 = get_work_item_repository()
        session1 = get_session_repository()

        # Reset
        reset_singletons()

        # Get new instances
        store2 = get_event_store()
        repo2 = get_work_item_repository()
        session2 = get_session_repository()

        # Should be different instances
        assert store1 is not store2
        assert repo1 is not repo2
        assert session1 is not session2


class TestEventSourcingPersistence:
    """Tests for event sourcing persistence chain."""

    def test_work_item_persists_to_filesystem(self, tmp_path: Path) -> None:
        """Work item events are persisted to filesystem."""
        from src.bootstrap import create_event_store, create_work_item_repository

        store = create_event_store(project_path=tmp_path)
        repo = create_work_item_repository(event_store=store)

        # Create and save a work item
        work_item = create_work_item(internal_id=1, title="Persistent Task")
        repo.save(work_item)

        # Verify event file exists
        events_dir = tmp_path / ".jerry" / "data" / "events"
        event_files = list(events_dir.glob("*.jsonl"))
        assert len(event_files) == 1

        # Verify content is JSON Lines
        content = event_files[0].read_text()
        lines = content.strip().split("\n")
        assert len(lines) == 1

        event_data = json.loads(lines[0])
        assert event_data["event_type"] == "WorkItemCreated"

    def test_work_item_survives_repository_recreation(self, tmp_path: Path) -> None:
        """Work item persists across repository instances (simulated restart)."""
        from src.bootstrap import create_event_store, create_work_item_repository

        # First "session" - create and save
        store1 = create_event_store(project_path=tmp_path)
        repo1 = create_work_item_repository(event_store=store1)

        work_item = create_work_item(internal_id=2, title="Survives Restart")
        work_item.start_work()
        repo1.save(work_item)

        # Simulate restart - create new instances
        del repo1, store1

        # Second "session" - load
        store2 = create_event_store(project_path=tmp_path)
        repo2 = create_work_item_repository(event_store=store2)

        loaded = repo2.get(work_item.id)

        assert loaded is not None
        assert loaded.title == "Survives Restart"
        assert loaded.status.name == "IN_PROGRESS"

    def test_multiple_work_items_isolated(self, tmp_path: Path) -> None:
        """Multiple work items have separate event streams."""
        from src.bootstrap import create_event_store, create_work_item_repository

        store = create_event_store(project_path=tmp_path)
        repo = create_work_item_repository(event_store=store)

        # Create multiple items
        item1 = create_work_item(internal_id=10, title="Item One")
        item2 = create_work_item(internal_id=11, title="Item Two")
        item3 = create_work_item(internal_id=12, title="Item Three")

        repo.save(item1)
        repo.save(item2)
        repo.save(item3)

        # Verify separate event files
        events_dir = tmp_path / ".jerry" / "data" / "events"
        event_files = list(events_dir.glob("*.jsonl"))
        assert len(event_files) == 3

        # Load and verify each
        loaded1 = repo.get(item1.id)
        loaded2 = repo.get(item2.id)
        loaded3 = repo.get(item3.id)

        assert loaded1 is not None
        assert loaded2 is not None
        assert loaded3 is not None
        assert loaded1.title == "Item One"
        assert loaded2.title == "Item Two"
        assert loaded3.title == "Item Three"


class TestCommandDispatcherIntegration:
    """Integration tests for CommandDispatcher with session commands."""

    def test_create_session_via_dispatcher(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """CreateSessionCommand works through dispatcher."""
        from src.bootstrap import create_command_dispatcher, reset_singletons
        from src.session_management.application.commands import CreateSessionCommand

        # Unset JERRY_PROJECT to use InMemoryEventStore (isolate from filesystem)
        monkeypatch.delenv("JERRY_PROJECT", raising=False)
        reset_singletons()
        dispatcher = create_command_dispatcher()

        command = CreateSessionCommand(name="Test Session", description="Integration test")
        events = dispatcher.dispatch(command)

        assert len(events) >= 1
        # Check first event is SessionCreated
        assert "SessionCreated" in type(events[0]).__name__

    def test_full_session_lifecycle_via_dispatcher(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Full session lifecycle (create -> end) via dispatcher."""
        from src.bootstrap import create_command_dispatcher, reset_singletons
        from src.session_management.application.commands import (
            CreateSessionCommand,
            EndSessionCommand,
        )

        # Unset JERRY_PROJECT to use InMemoryEventStore (isolate from filesystem)
        monkeypatch.delenv("JERRY_PROJECT", raising=False)
        reset_singletons()
        dispatcher = create_command_dispatcher()

        # Create session
        create_cmd = CreateSessionCommand(name="Lifecycle Test")
        create_events = dispatcher.dispatch(create_cmd)
        assert len(create_events) >= 1

        # End session
        end_cmd = EndSessionCommand(summary="Completed successfully")
        end_events = dispatcher.dispatch(end_cmd)
        assert len(end_events) >= 1

    def test_dispatcher_rejects_unregistered_command(self) -> None:
        """Dispatcher raises for unregistered command type."""
        from dataclasses import dataclass

        from src.application.ports import CommandHandlerNotFoundError
        from src.bootstrap import create_command_dispatcher

        @dataclass
        class UnknownCommand:
            value: str

        dispatcher = create_command_dispatcher()

        with pytest.raises(CommandHandlerNotFoundError):
            dispatcher.dispatch(UnknownCommand(value="test"))
