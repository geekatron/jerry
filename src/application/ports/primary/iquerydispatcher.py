"""
IQueryDispatcher - Protocol for Query Dispatchers.

Defines the contract (port) that query dispatcher implementations must satisfy.
This is an inbound/primary port from the Hexagonal Architecture perspective.

Following Clean Architecture:
- No imports from infrastructure/ or interface/
- Only imports from domain/ or stdlib

Protocol:
    IQueryDispatcher: Dispatches read queries to appropriate handlers

Exceptions:
    QueryHandlerNotFoundError: Raised when no handler registered for query type
"""

from __future__ import annotations

from typing import Any, Protocol, runtime_checkable


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


@runtime_checkable
class IQueryDispatcher(Protocol):
    """Protocol for query dispatchers.

    A query dispatcher routes read queries to their appropriate handlers.
    It does NOT execute business logic - it only routes.

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
