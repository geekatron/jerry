"""
Dispatcher Port Interfaces for CQRS.

Defines the contracts (ports) that dispatcher implementations must satisfy.
These are inbound ports from the Hexagonal Architecture perspective.

Following Clean Architecture:
- No imports from infrastructure/ or interface/
- Only imports from domain/ or stdlib

Protocols:
    IQueryDispatcher: Dispatches read queries to appropriate handlers
    ICommandDispatcher: Dispatches write commands to appropriate handlers

Exceptions:
    QueryHandlerNotFoundError: Raised when no handler registered for query type
    DuplicateHandlerError: Raised when registering duplicate handler
"""

from __future__ import annotations

from typing import Any, Protocol, TypeVar, runtime_checkable

# Generic type variables for queries, commands, and results
TQuery = TypeVar("TQuery")
TResult = TypeVar("TResult", covariant=True)
TCommand = TypeVar("TCommand")


class QueryHandlerNotFoundError(Exception):
    """Raised when no handler is registered for a query type.

    Attributes:
        query_type: The type of query that had no handler
        message: Human-readable error message
    """

    def __init__(self, query_type: type, message: str | None = None) -> None:
        """Initialize the exception.

        Args:
            query_type: The type of query that had no handler
            message: Optional custom message
        """
        self.query_type = query_type
        if message is None:
            message = f"No handler registered for query type: {query_type.__name__}"
        super().__init__(message)


class DuplicateHandlerError(Exception):
    """Raised when attempting to register a duplicate handler.

    Attributes:
        query_type: The type that already has a handler registered
        message: Human-readable error message
    """

    def __init__(self, query_type: type, message: str | None = None) -> None:
        """Initialize the exception.

        Args:
            query_type: The type that already has a handler
            message: Optional custom message
        """
        self.query_type = query_type
        if message is None:
            message = f"Handler already registered for type: {query_type.__name__}"
        super().__init__(message)


@runtime_checkable
class IQueryDispatcher(Protocol):
    """Protocol for query dispatchers.

    A query dispatcher routes read queries to their appropriate handlers.
    It does NOT execute business logic - it only routes.

    Type Parameters:
        TQuery: The query type (input)
        TResult: The result type (output)

    Example:
        >>> class GetUserByIdQuery:
        ...     user_id: str
        ...
        >>> dispatcher: IQueryDispatcher = QueryDispatcher(handlers)
        >>> result = dispatcher.dispatch(GetUserByIdQuery(user_id="123"))
    """

    def dispatch(self, query: Any) -> Any:
        """Dispatch a query to its registered handler.

        Args:
            query: The query object to dispatch

        Returns:
            The result from the handler

        Raises:
            QueryHandlerNotFoundError: If no handler is registered for the query type
        """
        ...


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
            QueryHandlerNotFoundError: If no handler is registered for the command type
        """
        ...
