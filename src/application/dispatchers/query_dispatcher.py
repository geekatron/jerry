"""
QueryDispatcher - Concrete implementation of IQueryDispatcher.

Routes queries to their registered handlers based on query type.
Implements exact type matching - subclasses don't inherit parent handlers.

This is an application layer component that:
- Routes queries to handlers (no business logic)
- Maintains handler registry
- Enforces single handler per query type

Example:
    >>> dispatcher = QueryDispatcher()
    >>> dispatcher.register(GetUserQuery, get_user_handler.handle)
    >>> result = dispatcher.dispatch(GetUserQuery(user_id="123"))
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from src.application.ports.primary.icommanddispatcher import DuplicateHandlerError
from src.application.ports.primary.iquerydispatcher import QueryHandlerNotFoundError


class QueryDispatcher:
    """Dispatches queries to registered handlers.

    Uses exact type matching - a handler registered for ParentQuery
    will NOT handle ChildQuery instances.

    Attributes:
        _handlers: Dictionary mapping query types to handler callables
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
        query_type: type,
        handler: Callable[[Any], Any],
    ) -> QueryDispatcher:
        """Register a handler for a query type.

        Args:
            query_type: The type of query this handler processes
            handler: Callable that takes a query and returns a result

        Returns:
            Self for method chaining

        Raises:
            DuplicateHandlerError: If a handler is already registered for this type
        """
        if query_type in self._handlers:
            raise DuplicateHandlerError(query_type)

        self._handlers[query_type] = handler
        return self

    def dispatch(self, query: Any) -> Any:
        """Dispatch a query to its registered handler.

        Uses exact type matching - subclass queries won't match
        parent class handlers.

        Args:
            query: The query object to dispatch

        Returns:
            The result from the handler

        Raises:
            TypeError: If query is None
            QueryHandlerNotFoundError: If no handler registered for query type
        """
        if query is None:
            raise TypeError("Cannot dispatch None query")

        query_type = type(query)

        if query_type not in self._handlers:
            raise QueryHandlerNotFoundError(query_type)

        handler = self._handlers[query_type]
        return handler(query)
