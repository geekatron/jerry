"""
Unit tests for QueryDispatcher implementation.

Follows Red/Green/Refactor - these tests fail initially (RED).

Test Distribution per impl-es-e-003:
- Happy Path (60%): 6 tests - Dispatch returns result, correct handler invoked, multiple handlers
- Negative (30%): 3 tests - None query, unregistered query, handler exception
- Edge (10%): 2 tests - Handler returns None, subclass query routing
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import pytest

from src.application.ports.dispatcher import (
    DuplicateHandlerError,
    IQueryDispatcher,
    QueryHandlerNotFoundError,
)


# === Test Fixtures ===


@dataclass
class SampleQuery:
    """Sample query for testing."""

    value: str


@dataclass
class OtherQuery:
    """Another query type for testing multiple handlers."""

    number: int


@dataclass
class UnregisteredQuery:
    """Query type with no registered handler."""

    data: str


@dataclass
class ChildQuery(SampleQuery):
    """Subclass of SampleQuery for inheritance testing."""

    extra: str = "default"


class SampleHandler:
    """Handler for SampleQuery."""

    def __init__(self) -> None:
        self.called_with: list[SampleQuery] = []

    def handle(self, query: SampleQuery) -> str:
        """Handle the query and return result."""
        self.called_with.append(query)
        return f"Result: {query.value}"


class OtherHandler:
    """Handler for OtherQuery."""

    def handle(self, query: OtherQuery) -> int:
        """Handle the query and return result."""
        return query.number * 2


class ExceptionHandler:
    """Handler that raises an exception."""

    def handle(self, query: Any) -> None:
        """Raise an exception."""
        raise ValueError("Handler error")


class NoneHandler:
    """Handler that returns None."""

    def handle(self, query: Any) -> None:
        """Return None."""
        return None


# === Happy Path Tests (60%) ===


class TestQueryDispatcherHappyPath:
    """Happy path tests for QueryDispatcher."""

    def test_dispatch_routes_to_handler(self) -> None:
        """QueryDispatcher routes query to registered handler."""
        from src.application.dispatchers.query_dispatcher import QueryDispatcher

        handler = SampleHandler()
        dispatcher = QueryDispatcher()
        dispatcher.register(SampleQuery, handler.handle)

        query = SampleQuery(value="test")
        result = dispatcher.dispatch(query)

        assert result == "Result: test"
        assert len(handler.called_with) == 1
        assert handler.called_with[0] is query

    def test_dispatch_returns_handler_result(self) -> None:
        """QueryDispatcher returns the exact result from handler."""
        from src.application.dispatchers.query_dispatcher import QueryDispatcher

        handler = OtherHandler()
        dispatcher = QueryDispatcher()
        dispatcher.register(OtherQuery, handler.handle)

        result = dispatcher.dispatch(OtherQuery(number=5))

        assert result == 10  # 5 * 2

    def test_dispatcher_handles_multiple_query_types(self) -> None:
        """QueryDispatcher can handle multiple different query types."""
        from src.application.dispatchers.query_dispatcher import QueryDispatcher

        sample_handler = SampleHandler()
        other_handler = OtherHandler()

        dispatcher = QueryDispatcher()
        dispatcher.register(SampleQuery, sample_handler.handle)
        dispatcher.register(OtherQuery, other_handler.handle)

        result1 = dispatcher.dispatch(SampleQuery(value="hello"))
        result2 = dispatcher.dispatch(OtherQuery(number=3))

        assert result1 == "Result: hello"
        assert result2 == 6

    def test_dispatcher_satisfies_protocol(self) -> None:
        """QueryDispatcher satisfies IQueryDispatcher protocol."""
        from src.application.dispatchers.query_dispatcher import QueryDispatcher

        dispatcher = QueryDispatcher()
        assert isinstance(dispatcher, IQueryDispatcher)

    def test_register_returns_dispatcher_for_chaining(self) -> None:
        """register() returns self to allow method chaining."""
        from src.application.dispatchers.query_dispatcher import QueryDispatcher

        dispatcher = QueryDispatcher()
        result = dispatcher.register(SampleQuery, SampleHandler().handle)

        assert result is dispatcher

    def test_constructor_accepts_initial_handlers(self) -> None:
        """QueryDispatcher can be initialized with handler dict."""
        from src.application.dispatchers.query_dispatcher import QueryDispatcher

        handler = SampleHandler()
        dispatcher = QueryDispatcher(handlers={SampleQuery: handler.handle})

        result = dispatcher.dispatch(SampleQuery(value="init"))
        assert result == "Result: init"


# === Negative Tests (30%) ===


class TestQueryDispatcherNegative:
    """Negative tests for QueryDispatcher."""

    def test_dispatch_none_query_raises(self) -> None:
        """Dispatching None raises TypeError."""
        from src.application.dispatchers.query_dispatcher import QueryDispatcher

        dispatcher = QueryDispatcher()

        with pytest.raises(TypeError) as exc_info:
            dispatcher.dispatch(None)

        assert "None" in str(exc_info.value) or "query" in str(exc_info.value).lower()

    def test_dispatch_unregistered_query_raises(self) -> None:
        """Dispatching unregistered query type raises QueryHandlerNotFoundError."""
        from src.application.dispatchers.query_dispatcher import QueryDispatcher

        dispatcher = QueryDispatcher()

        with pytest.raises(QueryHandlerNotFoundError) as exc_info:
            dispatcher.dispatch(UnregisteredQuery(data="test"))

        assert exc_info.value.query_type is UnregisteredQuery
        assert "UnregisteredQuery" in str(exc_info.value)

    def test_register_duplicate_handler_raises(self) -> None:
        """Registering duplicate handler raises DuplicateHandlerError."""
        from src.application.dispatchers.query_dispatcher import QueryDispatcher

        dispatcher = QueryDispatcher()
        dispatcher.register(SampleQuery, SampleHandler().handle)

        with pytest.raises(DuplicateHandlerError) as exc_info:
            dispatcher.register(SampleQuery, SampleHandler().handle)

        assert exc_info.value.query_type is SampleQuery


# === Edge Case Tests (10%) ===


class TestQueryDispatcherEdgeCases:
    """Edge case tests for QueryDispatcher."""

    def test_handler_returns_none(self) -> None:
        """Handler can legitimately return None."""
        from src.application.dispatchers.query_dispatcher import QueryDispatcher

        handler = NoneHandler()
        dispatcher = QueryDispatcher()
        dispatcher.register(SampleQuery, handler.handle)

        result = dispatcher.dispatch(SampleQuery(value="test"))

        assert result is None

    def test_subclass_query_not_routed_to_parent_handler(self) -> None:
        """Subclass queries don't automatically route to parent handler.

        If ChildQuery (subclass of SampleQuery) is dispatched but only
        SampleQuery has a handler registered, it should raise
        QueryHandlerNotFoundError - exact type matching, not inheritance.
        """
        from src.application.dispatchers.query_dispatcher import QueryDispatcher

        handler = SampleHandler()
        dispatcher = QueryDispatcher()
        dispatcher.register(SampleQuery, handler.handle)

        with pytest.raises(QueryHandlerNotFoundError):
            dispatcher.dispatch(ChildQuery(value="child", extra="more"))
