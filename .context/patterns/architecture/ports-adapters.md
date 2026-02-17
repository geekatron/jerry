# PAT-ARCH-002: Ports and Adapters Pattern

> **Status**: MANDATORY
> **Category**: Architecture Pattern
> **Location**: `src/*/ports/`, `src/infrastructure/adapters/`

---

## Overview

Ports and Adapters (part of Hexagonal Architecture) isolates the application core from external concerns. Ports define contracts (interfaces), while adapters implement them for specific technologies.

---

## Industry Prior Art

| Source | Key Insight |
|--------|-------------|
| **Alistair Cockburn** | "Allow an application to be equally driven by users, programs, automated tests, or batch scripts" |
| **Robert C. Martin** | "Plugin architecture where external details are pluggable" |
| **Vaughn Vernon** | "Ports express intentions, adapters fulfill them" |

---

## Port Types

### Primary Ports (Driving/Inbound)

Primary ports define how the application is **used**. They are interfaces implemented by the application core and called by external actors (UI, CLI, API).

```python
# File: src/application/ports/primary/iquerydispatcher.py
from typing import Any, Protocol


class IQueryDispatcher(Protocol):
    """Primary port for query dispatch.

    Defines the contract for how external actors
    request data from the application.
    """

    def dispatch(self, query: Any) -> Any:
        """Dispatch a query to its handler.

        Args:
            query: Query object to dispatch

        Returns:
            Query result (DTO)
        """
        ...


# File: src/application/ports/primary/icommanddispatcher.py
from typing import Any, Protocol

from src.shared_kernel.domain_event import DomainEvent


class ICommandDispatcher(Protocol):
    """Primary port for command dispatch.

    Defines the contract for how external actors
    request state changes in the application.
    """

    def dispatch(self, command: Any) -> list[DomainEvent]:
        """Dispatch a command to its handler.

        Args:
            command: Command object to dispatch

        Returns:
            List of domain events raised
        """
        ...
```

---

### Secondary Ports (Driven/Outbound)

Secondary ports define what the application **needs** from external systems. They are interfaces that the application depends on, implemented by infrastructure adapters.

```python
# File: src/work_tracking/domain/ports/work_item_repository.py
from typing import Protocol, Sequence

from src.work_tracking.domain.aggregates.work_item import WorkItem
from src.work_tracking.domain.value_objects.work_item_id import WorkItemId


class IWorkItemRepository(Protocol):
    """Secondary port for work item persistence.

    Defines the contract for aggregate persistence.
    Implemented by infrastructure adapters.
    """

    def get(self, id: WorkItemId) -> WorkItem | None:
        """Retrieve work item by ID."""
        ...

    def get_or_raise(self, id: WorkItemId) -> WorkItem:
        """Retrieve work item or raise if not found."""
        ...

    def save(self, work_item: WorkItem) -> None:
        """Persist work item."""
        ...

    def delete(self, id: WorkItemId) -> bool:
        """Delete work item."""
        ...


# File: src/application/ports/secondary/ieventstore.py
from typing import Protocol, Sequence

from src.shared_kernel.domain_event import DomainEvent


class IEventStore(Protocol):
    """Secondary port for event persistence."""

    def append(
        self,
        stream_id: str,
        events: Sequence[DomainEvent],
        expected_version: int,
    ) -> None:
        """Append events to stream."""
        ...

    def read(self, stream_id: str, from_version: int = 1) -> Sequence[DomainEvent]:
        """Read events from stream."""
        ...


# File: src/application/ports/secondary/ienvironment_provider.py
from typing import Protocol


class IEnvironmentProvider(Protocol):
    """Secondary port for environment access."""

    def get_env(self, key: str, default: str | None = None) -> str | None:
        """Get environment variable value."""
        ...
```

---

## Adapter Types

### Primary Adapters (Driving)

Primary adapters **drive** the application by calling primary ports.

```python
# File: src/interface/cli/adapter.py
from src.application.ports.primary.icommanddispatcher import ICommandDispatcher
from src.application.ports.primary.iquerydispatcher import IQueryDispatcher


class CLIAdapter:
    """CLI primary adapter.

    Translates CLI commands to application operations.
    Drives the application via dispatcher ports.
    """

    def __init__(
        self,
        command_dispatcher: ICommandDispatcher,
        query_dispatcher: IQueryDispatcher,
    ) -> None:
        """Initialize with dispatcher ports (injected)."""
        self._command_dispatcher = command_dispatcher
        self._query_dispatcher = query_dispatcher

    def create_task(self, title: str, priority: str = "medium") -> int:
        """Handle create-task CLI command."""
        from src.application.commands.create_work_item_command import (
            CreateWorkItemCommand,
        )

        command = CreateWorkItemCommand(
            title=title,
            work_type="task",
            priority=priority,
        )

        try:
            events = self._command_dispatcher.dispatch(command)
            print(f"Created: {events[0].work_item_id}")
            return 0
        except Exception as e:
            print(f"Error: {e}")
            return 1
```

---

### Secondary Adapters (Driven)

Secondary adapters are **driven** by the application. They implement secondary ports.

```python
# File: src/infrastructure/adapters/persistence/in_memory_event_store.py
from collections import defaultdict
from typing import Sequence

from src.application.ports.secondary.ieventstore import IEventStore
from src.shared_kernel.domain_event import DomainEvent


class InMemoryEventStore:
    """In-memory implementation of event store port.

    Secondary adapter for testing and development.
    """

    def __init__(self) -> None:
        self._streams: dict[str, list[DomainEvent]] = defaultdict(list)

    def append(
        self,
        stream_id: str,
        events: Sequence[DomainEvent],
        expected_version: int,
    ) -> None:
        """Append events to stream."""
        current_version = len(self._streams[stream_id])
        if current_version != expected_version:
            raise ConcurrencyError(stream_id, expected_version, current_version)

        self._streams[stream_id].extend(events)

    def read(
        self,
        stream_id: str,
        from_version: int = 1,
    ) -> Sequence[DomainEvent]:
        """Read events from stream."""
        events = self._streams.get(stream_id, [])
        return events[from_version - 1:]


# File: src/infrastructure/adapters/external/os_environment_adapter.py
import os

from src.application.ports.secondary.ienvironment_provider import IEnvironmentProvider


class OsEnvironmentAdapter:
    """OS environment implementation of environment port.

    Secondary adapter that reads from OS environment variables.
    """

    def get_env(self, key: str, default: str | None = None) -> str | None:
        """Get environment variable from OS."""
        return os.environ.get(key, default)
```

---

## Port/Adapter Flow

```
    External World            Application Core           External Systems
          │                        │                          │
          │    Primary Port        │    Secondary Port        │
          │    (IDispatcher)       │    (IRepository)         │
          │                        │                          │
    ┌─────┴─────┐            ┌─────┴─────┐            ┌───────┴───────┐
    │   CLI     │───────────►│  Handler  │───────────►│  Event Store  │
    │ (Adapter) │            │  (Core)   │            │   (Adapter)   │
    └───────────┘            └───────────┘            └───────────────┘

    Primary adapters          Application logic         Secondary adapters
    CALL primary ports        DEFINES ports             IMPLEMENT secondary ports
```

---

## Directory Structure

```
src/
├── application/
│   └── ports/
│       ├── primary/                    # Inbound ports
│       │   ├── iquerydispatcher.py
│       │   └── icommanddispatcher.py
│       └── secondary/                  # Outbound ports
│           ├── ieventstore.py
│           ├── isnapshotstore.py
│           └── ienvironment_provider.py
│
├── work_tracking/
│   └── domain/
│       └── ports/                      # Domain-specific ports
│           ├── work_item_repository.py
│           └── event_store.py
│
├── infrastructure/
│   └── adapters/
│       ├── persistence/                # Storage adapters
│       │   ├── in_memory_event_store.py
│       │   └── filesystem_repository.py
│       ├── messaging/                  # Event bus adapters
│       └── external/                   # External service adapters
│           └── os_environment_adapter.py
│
└── interface/                          # Primary adapters
    ├── cli/
    │   └── adapter.py
    └── api/
        └── routes/
```

---

## Naming Conventions

| Type | Location | Naming Pattern | Example |
|------|----------|----------------|---------|
| Primary Port | `application/ports/primary/` | `I{Verb}Dispatcher` | `IQueryDispatcher` |
| Secondary Port | `application/ports/secondary/` | `I{Noun}` | `IEventStore` |
| Domain Port | `domain/ports/` | `I{Noun}Repository` | `IWorkItemRepository` |
| Primary Adapter | `interface/{type}/` | `{Type}Adapter` | `CLIAdapter` |
| Secondary Adapter | `infrastructure/adapters/{type}/` | `{Tech}{Noun}Adapter` | `FilesystemProjectAdapter` |

---

## Testing Pattern

```python
def test_adapter_implements_port():
    """Adapter implements the port interface."""
    adapter = InMemoryEventStore()

    # Use Protocol.runtime_checkable for verification
    assert isinstance(adapter, IEventStore)


def test_handler_uses_port_not_adapter():
    """Handler depends on port, not concrete adapter."""
    # Can inject any adapter implementing the port
    mock_repo = Mock(spec=IWorkItemRepository)
    handler = CreateWorkItemCommandHandler(repository=mock_repo)

    # Handler works with mock
    handler.handle(CreateWorkItemCommand(title="Test"))
    mock_repo.save.assert_called_once()


def test_cli_adapter_drives_via_dispatcher():
    """CLI adapter uses dispatcher port."""
    mock_dispatcher = Mock(spec=ICommandDispatcher)
    mock_dispatcher.dispatch.return_value = [WorkItemCreated(...)]

    adapter = CLIAdapter(
        command_dispatcher=mock_dispatcher,
        query_dispatcher=Mock(),
    )

    adapter.create_task("New Task")

    mock_dispatcher.dispatch.assert_called_once()
```

---

## Jerry-Specific Decisions

> **Jerry Decision**: Ports are Python Protocols, not abstract base classes. This enables structural typing.

> **Jerry Decision**: One port per file. File name is lowercase interface name (e.g., `iquerydispatcher.py`).

> **Jerry Decision**: Secondary adapters in `infrastructure/adapters/`, primary adapters in `interface/`.

---

## Anti-Patterns

### 1. Direct Infrastructure Dependency

```python
# WRONG: Handler depends on concrete adapter
class CreateWorkItemHandler:
    def __init__(self):
        self._repo = FilesystemRepository()  # Concrete!

# CORRECT: Handler depends on port
class CreateWorkItemHandler:
    def __init__(self, repository: IWorkItemRepository):
        self._repo = repository
```

### 2. Port with Implementation Details

```python
# WRONG: Port exposes technology
class IEventStore(Protocol):
    def execute_sql(self, query: str): ...  # SQL detail!
    def get_connection(): ...  # Connection detail!

# CORRECT: Port is technology-agnostic
class IEventStore(Protocol):
    def append(self, stream_id: str, events: list): ...
    def read(self, stream_id: str): ...
```

---

## References

- **Alistair Cockburn**: [Hexagonal Architecture](https://alistair.cockburn.us/hexagonal-architecture/)
- **Robert C. Martin**: Clean Architecture (2017)
- **Design Canon**: Section 3.2 - Ports and Adapters
- **Related Patterns**: PAT-ARCH-001 (Composition Root), PAT-ARCH-003 (Bounded Contexts)
