# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
CommandDispatcher - Concrete implementation of ICommandDispatcher.

Routes commands to their registered handlers based on command type.
Implements exact type matching - subclasses don't inherit parent handlers.

This is an application layer component that:
- Routes commands to handlers (no business logic)
- Maintains handler registry
- Enforces single handler per command type
- Returns domain events from command execution

Example:
    >>> dispatcher = CommandDispatcher()
    >>> dispatcher.register(CreateWorkItemCommand, create_handler.handle)
    >>> events = dispatcher.dispatch(CreateWorkItemCommand(title="Test"))

References:
    - PAT-CQRS-002: Dispatcher Pattern
    - DISC-018: CommandDispatcher Not Implemented
    - TD-018: Event Sourcing for WorkItem Repository
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from src.application.ports.primary.icommanddispatcher import (
    CommandHandlerNotFoundError,
    DuplicateHandlerError,
)


class CommandDispatcher:
    """Dispatches commands to registered handlers.

    Uses exact type matching - a handler registered for ParentCommand
    will NOT handle ChildCommand instances.

    Command handlers typically return domain events (list[DomainEvent])
    or None for commands that don't produce events.

    Thread Safety:
        The dispatcher is NOT thread-safe. Registration should happen
        at startup (composition root) before concurrent dispatching.

    Attributes:
        _handlers: Dictionary mapping command types to handler callables
    """

    def __init__(
        self,
        handlers: dict[type, Callable[[Any], Any]] | None = None,
    ) -> None:
        """Initialize the dispatcher.

        Args:
            handlers: Optional initial handler mappings
        """
        self._handlers: dict[type, Callable[[Any], Any]] = handlers.copy() if handlers else {}

    def register(
        self,
        command_type: type,
        handler: Callable[[Any], Any],
    ) -> CommandDispatcher:
        """Register a handler for a command type.

        Args:
            command_type: The type of command this handler processes
            handler: Callable that takes a command and returns events or None

        Returns:
            Self for method chaining

        Raises:
            DuplicateHandlerError: If a handler is already registered for this type

        Example:
            >>> dispatcher = CommandDispatcher()
            >>> dispatcher.register(CreateCommand, create_handler.handle)
            >>> dispatcher.register(UpdateCommand, update_handler.handle)
        """
        if command_type in self._handlers:
            raise DuplicateHandlerError(command_type)

        self._handlers[command_type] = handler
        return self

    def dispatch(self, command: Any) -> Any:
        """Dispatch a command to its registered handler.

        Uses exact type matching - subclass commands won't match
        parent class handlers.

        Args:
            command: The command object to dispatch

        Returns:
            Domain events (list[DomainEvent]) or None from the handler

        Raises:
            TypeError: If command is None
            CommandHandlerNotFoundError: If no handler registered for command type

        Example:
            >>> events = dispatcher.dispatch(CreateWorkItemCommand(title="Test"))
            >>> if events:
            ...     for event in events:
            ...         print(event.event_type)
        """
        if command is None:
            raise TypeError("Cannot dispatch None command")

        command_type = type(command)

        if command_type not in self._handlers:
            raise CommandHandlerNotFoundError(command_type)

        handler = self._handlers[command_type]
        return handler(command)

    def has_handler(self, command_type: type) -> bool:
        """Check if a handler is registered for a command type.

        Args:
            command_type: The type to check

        Returns:
            True if a handler is registered, False otherwise
        """
        return command_type in self._handlers

    @property
    def registered_types(self) -> frozenset[type]:
        """Get all registered command types.

        Returns:
            Immutable set of registered command types
        """
        return frozenset(self._handlers.keys())
