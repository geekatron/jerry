# PAT-CQRS-004: Dispatcher Pattern

> **Status**: MANDATORY
> **Category**: CQRS
> **Also Known As**: Mediator, Message Router

---

## Intent

Route commands/queries to registered handlers without direct coupling, enabling centralized cross-cutting concerns and loose coupling between senders and receivers.

---

## Problem

Without a dispatcher:
- Calling code must know about handler implementations
- Cross-cutting concerns (logging, validation, authorization) must be duplicated
- Testing requires mocking concrete handlers
- Adding new handlers requires modifying calling code

---

## Solution

Create a central dispatcher that routes messages to registered handlers.

### Structure

```python
# Port Definition (Application Layer)
@runtime_checkable
class IQueryDispatcher(Protocol):
    """Inbound/primary port - query routing contract."""

    def dispatch(self, query: Any) -> Any:
        """Dispatch a query to its registered handler."""
        ...

@runtime_checkable
class ICommandDispatcher(Protocol):
    """Inbound/primary port - command routing contract."""

    def dispatch(self, command: Any) -> list[DomainEvent]:
        """Dispatch a command to its registered handler."""
        ...
```

### Implementation

```python
# Dispatcher Implementation (Application Layer)
class QueryDispatcher:
    """Concrete dispatcher that routes queries to handlers."""

    def __init__(self) -> None:
        self._handlers: dict[type, Callable[[Any], Any]] = {}

    def register(self, query_type: type, handler: Callable[[Any], Any]) -> None:
        """Register a handler for a query type.

        Args:
            query_type: The type of query to handle
            handler: Callable that handles the query
        """
        self._handlers[query_type] = handler

    def dispatch(self, query: Any) -> Any:
        """Route query to registered handler.

        Args:
            query: Query object to dispatch

        Returns:
            Handler result

        Raises:
            UnregisteredQueryError: If no handler registered
        """
        handler = self._handlers.get(type(query))
        if handler is None:
            raise UnregisteredQueryError(
                f"No handler registered for {type(query).__name__}"
            )
        return handler(query)
```

---

## Registration Pattern

Handlers are registered in the composition root:

```python
# src/bootstrap.py

def create_query_dispatcher() -> QueryDispatcher:
    """Create and configure query dispatcher."""
    # Create infrastructure adapters
    repository = FilesystemProjectAdapter()
    environment = OsEnvironmentAdapter()

    # Create handlers with injected dependencies
    retrieve_handler = RetrieveProjectContextQueryHandler(
        repository=repository,
        environment=environment,
    )
    scan_handler = ScanProjectsQueryHandler(repository=repository)
    validate_handler = ValidateProjectQueryHandler(repository=repository)

    # Configure dispatcher with all handlers
    dispatcher = QueryDispatcher()
    dispatcher.register(RetrieveProjectContextQuery, retrieve_handler.handle)
    dispatcher.register(ScanProjectsQuery, scan_handler.handle)
    dispatcher.register(ValidateProjectQuery, validate_handler.handle)

    return dispatcher
```

---

## Usage Pattern

### In CLI Adapter

```python
class CLIAdapter:
    """Clean Architecture CLI Adapter."""

    def __init__(self, dispatcher: IQueryDispatcher) -> None:
        """Initialize with dispatcher (dependency injection)."""
        self._dispatcher = dispatcher

    def cmd_init(self, json_output: bool = False) -> int:
        """Handle init command."""
        query = RetrieveProjectContextQuery(base_path=self._projects_dir)
        context = self._dispatcher.dispatch(query)
        # Format and display results
        return 0
```

### In Tests

```python
def test_cmd_init_dispatches_query():
    """Verify init command dispatches correct query."""
    # Arrange
    mock_dispatcher = Mock(spec=IQueryDispatcher)
    mock_dispatcher.dispatch.return_value = create_test_context()
    adapter = CLIAdapter(dispatcher=mock_dispatcher)

    # Act
    adapter.cmd_init()

    # Assert
    mock_dispatcher.dispatch.assert_called_once()
    query = mock_dispatcher.dispatch.call_args[0][0]
    assert isinstance(query, RetrieveProjectContextQuery)
```

---

## Jerry Implementation

### File Locations

| Type | Location |
|------|----------|
| Query Dispatcher Port | `src/application/ports/primary/iquerydispatcher.py` |
| Command Dispatcher Port | `src/application/ports/primary/icommanddispatcher.py` |
| Query Dispatcher Impl | `src/application/dispatchers/query_dispatcher.py` |
| Command Dispatcher Impl | `src/application/dispatchers/command_dispatcher.py` |

### Current Implementation

```python
# src/application/ports/primary/iquerydispatcher.py
"""Query dispatcher port (primary/inbound)."""
from __future__ import annotations

from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class IQueryDispatcher(Protocol):
    """Inbound port for query dispatching."""

    def dispatch(self, query: Any) -> Any:
        """Dispatch a query to its registered handler."""
        ...


# src/application/dispatchers/query_dispatcher.py
"""Query dispatcher implementation."""
from __future__ import annotations

from typing import Any, Callable


class UnregisteredQueryError(Exception):
    """Raised when no handler is registered for a query type."""


class QueryDispatcher:
    """Routes queries to registered handlers."""

    def __init__(self) -> None:
        self._handlers: dict[type, Callable[[Any], Any]] = {}

    def register(self, query_type: type, handler: Callable[[Any], Any]) -> None:
        """Register a handler for a query type."""
        self._handlers[query_type] = handler

    def dispatch(self, query: Any) -> Any:
        """Route query to registered handler."""
        handler = self._handlers.get(type(query))
        if handler is None:
            raise UnregisteredQueryError(
                f"No handler registered for {type(query).__name__}"
            )
        return handler(query)
```

---

## Benefits

| Benefit | Description |
|---------|-------------|
| **Loose Coupling** | Senders don't know about receivers |
| **Testability** | Easy to mock dispatcher in tests |
| **Single Responsibility** | Each handler does one thing |
| **Open/Closed** | Add handlers without modifying calling code |
| **Cross-Cutting Concerns** | Centralized logging, validation, authorization |

---

## Cross-Cutting Concerns

The dispatcher can wrap handlers with decorators:

```python
class LoggingQueryDispatcher:
    """Decorator that adds logging to dispatch."""

    def __init__(self, inner: IQueryDispatcher) -> None:
        self._inner = inner

    def dispatch(self, query: Any) -> Any:
        logger.info(f"Dispatching {type(query).__name__}")
        try:
            result = self._inner.dispatch(query)
            logger.info(f"Query succeeded")
            return result
        except Exception as e:
            logger.error(f"Query failed: {e}")
            raise
```

---

## Industry Prior Art

| Source | Description |
|--------|-------------|
| [MediatR](https://github.com/jbogard/mediatr) | .NET mediator pattern library by Jimmy Bogard |
| [Cosmic Python](https://www.cosmicpython.com/book/chapter_12_cqrs.html) | Python CQRS patterns |
| [CQRS Pattern](https://martinfowler.com/bliki/CQRS.html) | Martin Fowler's CQRS description |

---

## Related Patterns

- [PAT-CQRS-001: Command Pattern](./command-pattern.md)
- [PAT-CQRS-002: Query Pattern](./query-pattern.md)
- [PAT-ARCH-005: Composition Root](../architecture/composition-root.md)

---

## TD-015 Reference

Implemented as part of TD-015 (CLI Architecture Remediation).

---

*Pattern documented by Claude (Opus 4.5) as part of TD-017*
