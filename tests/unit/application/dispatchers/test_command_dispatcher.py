"""
Unit tests for CommandDispatcher implementation.

Follows Red/Green/Refactor testing methodology.

Test Distribution:
- Happy Path (60%): Dispatch returns events, correct handler invoked, multiple handlers
- Negative (30%): None command, unregistered command, duplicate handler
- Edge (10%): Handler returns None, subclass command routing, has_handler

References:
    - PAT-CQRS-002: Dispatcher Pattern
    - TD-018: Event Sourcing for WorkItem Repository
    - DISC-018: CommandDispatcher Not Implemented
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import pytest

from src.application.ports import (
    CommandHandlerNotFoundError,
    DuplicateHandlerError,
    ICommandDispatcher,
)


# === Test Fixtures ===


@dataclass
class SampleCommand:
    """Sample command for testing."""

    title: str


@dataclass
class OtherCommand:
    """Another command type for testing multiple handlers."""

    value: int


@dataclass
class UnregisteredCommand:
    """Command type with no registered handler."""

    data: str


@dataclass
class ChildCommand(SampleCommand):
    """Subclass of SampleCommand for inheritance testing."""

    extra: str = "default"


@dataclass(frozen=True)
class SampleEvent:
    """Sample domain event for testing."""

    command_title: str


class SampleHandler:
    """Handler for SampleCommand."""

    def __init__(self) -> None:
        self.called_with: list[SampleCommand] = []

    def handle(self, command: SampleCommand) -> list[SampleEvent]:
        """Handle the command and return events."""
        self.called_with.append(command)
        return [SampleEvent(command_title=command.title)]


class OtherHandler:
    """Handler for OtherCommand."""

    def handle(self, command: OtherCommand) -> list[SampleEvent]:
        """Handle the command and return events."""
        return [SampleEvent(command_title=f"value_{command.value}")]


class NoneHandler:
    """Handler that returns None (no events)."""

    def handle(self, command: Any) -> None:
        """Return None (no events to publish)."""
        return None


class MultiEventHandler:
    """Handler that returns multiple events."""

    def handle(self, command: SampleCommand) -> list[SampleEvent]:
        """Return multiple events."""
        return [
            SampleEvent(command_title=f"{command.title}_created"),
            SampleEvent(command_title=f"{command.title}_validated"),
        ]


# === Happy Path Tests (60%) ===


class TestCommandDispatcherHappyPath:
    """Happy path tests for CommandDispatcher."""

    def test_dispatch_routes_to_handler(self) -> None:
        """CommandDispatcher routes command to registered handler."""
        from src.application.dispatchers.command_dispatcher import CommandDispatcher

        handler = SampleHandler()
        dispatcher = CommandDispatcher()
        dispatcher.register(SampleCommand, handler.handle)

        command = SampleCommand(title="test")
        events = dispatcher.dispatch(command)

        assert len(events) == 1
        assert events[0].command_title == "test"
        assert len(handler.called_with) == 1
        assert handler.called_with[0] is command

    def test_dispatch_returns_handler_events(self) -> None:
        """CommandDispatcher returns the exact events from handler."""
        from src.application.dispatchers.command_dispatcher import CommandDispatcher

        handler = OtherHandler()
        dispatcher = CommandDispatcher()
        dispatcher.register(OtherCommand, handler.handle)

        events = dispatcher.dispatch(OtherCommand(value=42))

        assert len(events) == 1
        assert events[0].command_title == "value_42"

    def test_dispatch_returns_multiple_events(self) -> None:
        """CommandDispatcher returns multiple events from handler."""
        from src.application.dispatchers.command_dispatcher import CommandDispatcher

        handler = MultiEventHandler()
        dispatcher = CommandDispatcher()
        dispatcher.register(SampleCommand, handler.handle)

        events = dispatcher.dispatch(SampleCommand(title="multi"))

        assert len(events) == 2
        assert events[0].command_title == "multi_created"
        assert events[1].command_title == "multi_validated"

    def test_dispatcher_handles_multiple_command_types(self) -> None:
        """CommandDispatcher can handle multiple different command types."""
        from src.application.dispatchers.command_dispatcher import CommandDispatcher

        sample_handler = SampleHandler()
        other_handler = OtherHandler()

        dispatcher = CommandDispatcher()
        dispatcher.register(SampleCommand, sample_handler.handle)
        dispatcher.register(OtherCommand, other_handler.handle)

        events1 = dispatcher.dispatch(SampleCommand(title="hello"))
        events2 = dispatcher.dispatch(OtherCommand(value=3))

        assert events1[0].command_title == "hello"
        assert events2[0].command_title == "value_3"

    def test_dispatcher_satisfies_protocol(self) -> None:
        """CommandDispatcher satisfies ICommandDispatcher protocol."""
        from src.application.dispatchers.command_dispatcher import CommandDispatcher

        dispatcher = CommandDispatcher()
        assert isinstance(dispatcher, ICommandDispatcher)

    def test_register_returns_dispatcher_for_chaining(self) -> None:
        """register() returns self to allow method chaining."""
        from src.application.dispatchers.command_dispatcher import CommandDispatcher

        dispatcher = CommandDispatcher()
        result = dispatcher.register(SampleCommand, SampleHandler().handle)

        assert result is dispatcher

    def test_constructor_accepts_initial_handlers(self) -> None:
        """CommandDispatcher can be initialized with handler dict."""
        from src.application.dispatchers.command_dispatcher import CommandDispatcher

        handler = SampleHandler()
        dispatcher = CommandDispatcher(handlers={SampleCommand: handler.handle})

        events = dispatcher.dispatch(SampleCommand(title="init"))
        assert events[0].command_title == "init"


# === Negative Tests (30%) ===


class TestCommandDispatcherNegative:
    """Negative tests for CommandDispatcher."""

    def test_dispatch_none_command_raises(self) -> None:
        """Dispatching None raises TypeError."""
        from src.application.dispatchers.command_dispatcher import CommandDispatcher

        dispatcher = CommandDispatcher()

        with pytest.raises(TypeError) as exc_info:
            dispatcher.dispatch(None)

        assert "None" in str(exc_info.value) or "command" in str(exc_info.value).lower()

    def test_dispatch_unregistered_command_raises(self) -> None:
        """Dispatching unregistered command type raises CommandHandlerNotFoundError."""
        from src.application.dispatchers.command_dispatcher import CommandDispatcher

        dispatcher = CommandDispatcher()

        with pytest.raises(CommandHandlerNotFoundError) as exc_info:
            dispatcher.dispatch(UnregisteredCommand(data="test"))

        assert exc_info.value.command_type is UnregisteredCommand
        assert "UnregisteredCommand" in str(exc_info.value)

    def test_register_duplicate_handler_raises(self) -> None:
        """Registering duplicate handler raises DuplicateHandlerError."""
        from src.application.dispatchers.command_dispatcher import CommandDispatcher

        dispatcher = CommandDispatcher()
        dispatcher.register(SampleCommand, SampleHandler().handle)

        with pytest.raises(DuplicateHandlerError) as exc_info:
            dispatcher.register(SampleCommand, SampleHandler().handle)

        assert exc_info.value.handler_type is SampleCommand


# === Edge Case Tests (10%) ===


class TestCommandDispatcherEdgeCases:
    """Edge case tests for CommandDispatcher."""

    def test_handler_returns_none(self) -> None:
        """Handler can legitimately return None (no events)."""
        from src.application.dispatchers.command_dispatcher import CommandDispatcher

        handler = NoneHandler()
        dispatcher = CommandDispatcher()
        dispatcher.register(SampleCommand, handler.handle)

        result = dispatcher.dispatch(SampleCommand(title="test"))

        assert result is None

    def test_subclass_command_not_routed_to_parent_handler(self) -> None:
        """Subclass commands don't automatically route to parent handler.

        If ChildCommand (subclass of SampleCommand) is dispatched but only
        SampleCommand has a handler registered, it should raise
        CommandHandlerNotFoundError - exact type matching, not inheritance.
        """
        from src.application.dispatchers.command_dispatcher import CommandDispatcher

        handler = SampleHandler()
        dispatcher = CommandDispatcher()
        dispatcher.register(SampleCommand, handler.handle)

        with pytest.raises(CommandHandlerNotFoundError):
            dispatcher.dispatch(ChildCommand(title="child", extra="more"))

    def test_has_handler_returns_true_for_registered(self) -> None:
        """has_handler() returns True for registered command type."""
        from src.application.dispatchers.command_dispatcher import CommandDispatcher

        dispatcher = CommandDispatcher()
        dispatcher.register(SampleCommand, SampleHandler().handle)

        assert dispatcher.has_handler(SampleCommand) is True

    def test_has_handler_returns_false_for_unregistered(self) -> None:
        """has_handler() returns False for unregistered command type."""
        from src.application.dispatchers.command_dispatcher import CommandDispatcher

        dispatcher = CommandDispatcher()

        assert dispatcher.has_handler(UnregisteredCommand) is False

    def test_registered_types_returns_frozenset(self) -> None:
        """registered_types returns immutable frozenset of types."""
        from src.application.dispatchers.command_dispatcher import CommandDispatcher

        dispatcher = CommandDispatcher()
        dispatcher.register(SampleCommand, SampleHandler().handle)
        dispatcher.register(OtherCommand, OtherHandler().handle)

        types = dispatcher.registered_types

        assert isinstance(types, frozenset)
        assert SampleCommand in types
        assert OtherCommand in types
        assert len(types) == 2

    def test_register_chain_multiple_handlers(self) -> None:
        """Method chaining works for multiple registrations."""
        from src.application.dispatchers.command_dispatcher import CommandDispatcher

        dispatcher = (
            CommandDispatcher()
            .register(SampleCommand, SampleHandler().handle)
            .register(OtherCommand, OtherHandler().handle)
        )

        assert dispatcher.has_handler(SampleCommand)
        assert dispatcher.has_handler(OtherCommand)
