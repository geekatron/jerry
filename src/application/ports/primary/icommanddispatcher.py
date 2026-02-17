# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
ICommandDispatcher - Protocol for Command Dispatchers.

Defines the contract (port) that command dispatcher implementations must satisfy.
This is an inbound/primary port from the Hexagonal Architecture perspective.

Following Clean Architecture:
- No imports from infrastructure/ or interface/
- Only imports from domain/ or stdlib

Protocol:
    ICommandDispatcher: Dispatches write commands to appropriate handlers

Exceptions:
    DuplicateHandlerError: Raised when registering duplicate handler
"""

from __future__ import annotations

from typing import Any, Protocol, runtime_checkable


class DuplicateHandlerError(Exception):
    """Raised when attempting to register a duplicate handler.

    Attributes:
        handler_type: The type that already has a handler registered
        message: Human-readable error message
    """

    def __init__(self, handler_type: type, message: str | None = None) -> None:
        """Initialize the exception.

        Args:
            handler_type: The type that already has a handler
            message: Optional custom message
        """
        self.handler_type = handler_type
        if message is None:
            message = f"Handler already registered for type: {handler_type.__name__}"
        super().__init__(message)


class CommandHandlerNotFoundError(Exception):
    """Raised when no handler is registered for a command type.

    Attributes:
        command_type: The type of command that had no handler
        message: Human-readable error message
    """

    def __init__(self, command_type: type, message: str | None = None) -> None:
        """Initialize the exception.

        Args:
            command_type: The type of command that had no handler
            message: Optional custom message
        """
        self.command_type = command_type
        if message is None:
            message = f"No handler registered for command type: {command_type.__name__}"
        super().__init__(message)


@runtime_checkable
class ICommandDispatcher(Protocol):
    """Protocol for command dispatchers.

    A command dispatcher routes write commands to their appropriate handlers.
    Commands may return events or None.

    Example:
        >>> class CreateUserCommand:
        ...     name: str
        ...     email: str
        ...
        >>> dispatcher: ICommandDispatcher = CommandDispatcher(handlers)
        >>> events = dispatcher.dispatch(CreateUserCommand(name="John", email="j@e.com"))
    """

    def dispatch(self, command: Any) -> Any:
        """Dispatch a command to its registered handler.

        Args:
            command: The command object to dispatch

        Returns:
            Domain events or None

        Raises:
            CommandHandlerNotFoundError: If no handler is registered for the command type
        """
        ...
