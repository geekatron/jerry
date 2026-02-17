# Coding Practices Guide

> Educational companion to [coding-standards.md](../rules/coding-standards.md).
> Explains type hint rationale, docstring format guidance, import organization, and error handling decision trees.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Type Hints Rationale](#type-hints-rationale) | Why type hints matter and how to use them |
| [Docstring Best Practices](#docstring-best-practices) | Google-style format guidance with examples |
| [Import Organization](#import-organization) | Grouping, sorting, and avoiding circular imports |
| [Error Handling Decision Trees](#error-handling-decision-trees) | Quick reference (full guide in error-handling.md) |
| [Value Object Patterns](#value-object-patterns) | Immutable dataclass patterns |
| [Protocol vs ABC](#protocol-vs-abc) | When to use Protocol vs Abstract Base Class |
| [TYPE_CHECKING Pattern](#type_checking-pattern) | Avoiding circular imports |
| [Evidence](#evidence) | Verified codebase file paths and code quotes |

---

## Type Hints Rationale

### Why Type Hints Are Required (H-11)

**Rule**: All public functions and methods MUST have type annotations.

**Rationale**:

#### 1. Catch Bugs Before Runtime

```python
# (Hypothetical -- illustrative pattern)
# Without type hints
def get_work_item(id):
    return repository.get(id)

# Bug: Passing integer instead of string
item = get_work_item(123)  # Runtime error later

# With type hints
def get_work_item(id: str) -> WorkItem | None:
    return repository.get(id)

# Bug caught by mypy
item = get_work_item(123)  # ❌ mypy error: Expected str, got int
```

---

#### 2. Self-Documenting Code

```python
# Without type hints - unclear
def process(data, options=None):
    ...

# With type hints - clear
def process(data: list[WorkItem], options: ProcessOptions | None = None) -> ProcessResult:
    ...
```

**Reading the second signature**, you immediately know:
- `data` is a list of `WorkItem` objects
- `options` is optional, type `ProcessOptions` or `None`
- Returns `ProcessResult`

---

#### 3. Better IDE Support

**Type hints enable**:
- Autocomplete
- Inline documentation
- Refactoring tools
- Jump to definition

```python
def complete_work_item(item_id: str, dispatcher: ICommandDispatcher) -> None:
    command = CreateWorkItemCommand(title="Test")
    #         ^--- IDE suggests CreateWorkItemCommand fields
    dispatcher.dispatch(command)
    #          ^--- IDE shows dispatch() signature
```

---

### Type Hint Best Practices

#### Use Modern Syntax (Python 3.10+)

```python
# ✅ GOOD: Modern syntax
def get_item(id: str) -> WorkItem | None:
    ...

def process(items: list[WorkItem]) -> dict[str, int]:
    ...

# ❌ OLD: Deprecated syntax (avoid)
from typing import Optional, List, Dict

def get_item(id: str) -> Optional[WorkItem]:
    ...

def process(items: List[WorkItem]) -> Dict[str, int]:
    ...
```

**Why prefer modern syntax?**
- Shorter, more readable
- Python 3.10+ built-in support
- Recommended by PEP 604, PEP 585

---

#### Use `from __future__ import annotations` for Forward References

```python
from __future__ import annotations

class WorkItem:
    def add_subtask(self, subtask: WorkItem) -> None:  # ✅ Forward reference works
        self._subtasks.append(subtask)
```

**Without `from __future__`**:
```python
class WorkItem:
    def add_subtask(self, subtask: "WorkItem") -> None:  # ❌ Requires string quote
        ...
```

**Why use `from __future__`?**
- Cleaner (no string quotes)
- Forward references work automatically
- Deferred annotation evaluation (faster imports)

---

#### Annotate Return Types, Even for `None`

```python
# ✅ GOOD: Explicit None return
def save_work_item(item: WorkItem) -> None:
    repository.save(item)

# ❌ BAD: Missing return type
def save_work_item(item: WorkItem):
    repository.save(item)
```

**Why annotate `None`?**
- Makes it clear the function doesn't return a value
- mypy can verify you're not accidentally returning something
- Consistency

---

#### Use Generic Types for Containers

```python
# ✅ GOOD: Specific element type
def filter_items(items: list[WorkItem], status: Status) -> list[WorkItem]:
    return [i for i in items if i.status == status]

# ❌ BAD: Untyped list
def filter_items(items: list, status: Status) -> list:
    return [i for i in items if i.status == status]
```

**Why specify element type?**
- mypy can verify operations on elements
- IDE autocomplete knows element type
- Documents what the list contains

---

### Common Type Hint Patterns

#### Optional Parameters

```python
def create_task(
    title: str,
    description: str | None = None,  # Optional, defaults to None
    parent_id: str | None = None,
) -> Task:
    ...
```

---

#### Union Types

```python
def load_config(source: str | Path) -> Config:
    """Load config from file path (string or Path object)."""
    ...
```

---

#### Callable Types

```python
from typing import Callable

def register_handler(
    event_type: type[DomainEvent],
    handler: Callable[[DomainEvent], None],
) -> None:
    ...
```

---

#### Generic Protocols

```python
# (Hypothetical -- illustrative pattern)
from typing import Protocol, TypeVar

TAggregate = TypeVar("TAggregate")
TId = TypeVar("TId")

class IRepository(Protocol[TAggregate, TId]):
    def get(self, id: TId) -> TAggregate | None: ...
    def save(self, aggregate: TAggregate) -> None: ...
```

---

## Docstring Best Practices

### Why Docstrings Are Required (H-12)

**Rule**: All public functions, classes, and modules MUST have docstrings.

**Rationale**:

1. **Self-documenting code**: Explains **why**, not just **what**
2. **IDE support**: Inline help when hovering over functions
3. **Generated documentation**: Tools like Sphinx extract docstrings
4. **Onboarding**: New developers understand code faster

---

### Google-Style Format

**Jerry standard**: Google-style docstrings with Args, Returns, Raises sections.

#### Function Docstring

```python
def complete_work_item(item_id: str, quality_passed: bool = True) -> WorkItem:
    """Mark a work item as completed.

    Transitions the work item to COMPLETED status if it's currently IN_PROGRESS.
    Emits a WorkItemCompleted domain event.

    Args:
        item_id: The unique identifier of the work item.
        quality_passed: Whether the work item passed quality checks. Defaults to True.

    Returns:
        The updated WorkItem with COMPLETED status.

    Raises:
        WorkItemNotFoundError: If no item exists with the given ID.
        InvalidStateError: If the item is not IN_PROGRESS.
        QualityGateFailedError: If quality_passed is False and quality gate is enforced.

    Example:
        >>> item = complete_work_item("WORK-123")
        >>> assert item.status == Status.COMPLETED
    """
    item = repository.get_or_raise(item_id)
    if item.status != Status.IN_PROGRESS:
        raise InvalidStateError(...)
    item.complete(quality_passed=quality_passed)
    repository.save(item)
    return item
```

**Sections**:
1. **Summary** (first line): One-sentence description
2. **Extended description** (optional): Details, algorithm, rationale
3. **Args**: Parameter descriptions
4. **Returns**: Return value description
5. **Raises**: Exceptions that may be raised
6. **Example** (optional): Usage example

---

#### Class Docstring

```python
class WorkItemRepository:
    """Repository for persisting and retrieving work items.

    Implements event sourcing pattern. Work items are reconstructed from
    their event history stored in the event store.

    Attributes:
        _event_store: Event store adapter for persistence.
        _snapshot_store: Optional snapshot store for optimization.
    """

    def __init__(self, event_store: IEventStore) -> None:
        """Initialize the repository.

        Args:
            event_store: Event store adapter for event persistence.
        """
        self._event_store = event_store
```

---

#### Module Docstring

```python
"""Work item domain model.

This module contains the WorkItem aggregate root and related value objects.
WorkItem represents a unit of work with lifecycle, subtasks, and quality tracking.

Classes:
    WorkItem: Aggregate root representing a unit of work.
    WorkItemId: Value object for work item identity.
    WorkItemStatus: Enum for work item status.

References:
    - docs/design/work-tracking-design.md
    - .context/patterns/entity/aggregate-root.md
"""
```

---

### Docstring Best Practices

#### 1. First Line Is Summary

```python
# ✅ GOOD: Concise summary
def validate_quality(item: WorkItem) -> bool:
    """Check if work item meets quality criteria."""
    ...

# ❌ BAD: Too verbose for first line
def validate_quality(item: WorkItem) -> bool:
    """This function validates whether a given work item meets the quality criteria
    defined by the quality gate configuration and returns a boolean indicating success."""
    ...
```

**Rule**: First line should fit on one line (< 80 chars).

---

#### 2. Explain "Why", Not Just "What"

```python
# ❌ BAD: Repeats the function signature
def save_snapshot(item: WorkItem, version: int) -> None:
    """Save snapshot of work item at version."""
    ...

# ✅ GOOD: Explains rationale
def save_snapshot(item: WorkItem, version: int) -> None:
    """Save snapshot of work item to optimize event replay.

    Snapshots are saved every 10 events to avoid replaying large event streams.
    This significantly improves performance for long-lived aggregates.
    """
    ...
```

---

#### 3. Document Business Logic

```python
def can_complete(self) -> bool:
    """Check if work item can be completed.

    Work items can only be completed if:
    1. Current status is IN_PROGRESS
    2. All subtasks are completed (if any exist)
    3. Quality gate passed (if enforced)

    Returns:
        True if work item can be completed, False otherwise.
    """
    ...
```

---

## Import Organization

### Import Grouping Standard

**Rule**: Group imports into three sections, separated by blank lines.

```python
# Standard library imports
import json
from datetime import datetime, timezone
from pathlib import Path

# Third-party imports
import click
from pydantic import BaseModel

# Local application imports
from src.domain.aggregates.work_item import WorkItem
from src.domain.ports.repository import IRepository
from src.shared_kernel.identity.vertex_id import VertexId
```

**Order**:
1. **Standard library** (built-in Python modules)
2. **Third-party** (installed packages)
3. **Local** (your application code)

**Within each group**: Sort alphabetically.

---

### Absolute vs Relative Imports

```python
# ✅ GOOD: Absolute imports for cross-package
from src.domain.aggregates.work_item import WorkItem
from src.application.commands.create_work_item_command import CreateWorkItemCommand

# ❌ BAD: Relative imports for cross-package
from ...domain.aggregates.work_item import WorkItem  # Hard to follow
```

**When to use relative imports?**
- Within the same package (optional, not required)
- Example: `from .value_objects import Priority` (within domain package)

**Jerry preference**: Absolute imports for clarity.

---

### Avoiding Circular Imports with TYPE_CHECKING

See [TYPE_CHECKING Pattern](#type_checking-pattern) section below.

---

## Error Handling Decision Trees

> **Full error handling guide**: See [Error Handling Guide](error-handling.md) for the complete exception hierarchy, detailed decision tree, usage examples, error message best practices, and layer-appropriate exception handling patterns.

This section provides a brief summary. For the authoritative decision tree and examples, refer to the dedicated guide.

### Quick Reference: "Which Exception Should I Raise?"

| Situation | Exception | Example |
|-----------|-----------|---------|
| Invalid input (before processing) | `ValidationError(field, message)` | Empty title, out-of-range value |
| Entity not found | `NotFoundError(entity_type, entity_id)` | WorkItem not in repository |
| Wrong state for operation | `InvalidStateError(current_state, attempted_action)` | Complete when not IN_PROGRESS |
| State transition not allowed | `InvalidStateTransitionError(from_state, to_state)` | PENDING to COMPLETED directly |
| Business rule violated | `InvariantViolationError(invariant, details)` | Percentages don't sum to 100% |
| Concurrent modification | `ConcurrencyError(expected_version, actual_version)` | Event store version mismatch |

### Ambiguous Cases

| Question | Guidance |
|----------|----------|
| Input is valid format but entity doesn't exist? | `NotFoundError`, not `ValidationError`. Validation passed; the entity is simply missing. |
| Multiple validations fail at once? | Raise `ValidationError` for the **first** failing field. Future: consider collecting all errors. |
| Domain rule vs input validation? | If the check requires loading domain state (e.g., checking uniqueness), use `InvariantViolationError`. If it can be checked from the input alone, use `ValidationError`. |
| Infrastructure error (file I/O, JSON parse)? | Convert to domain exception at layer boundary. See [Error Handling Guide -- Domain vs Infrastructure](error-handling.md#domain-vs-infrastructure-exceptions). |
| Unsure whether InvalidStateError or InvalidStateTransitionError? | If there is an explicit state machine with defined transitions, use `InvalidStateTransitionError`. Otherwise, use `InvalidStateError`. |

### Exception Propagation

**Rule**: Use `from e` when re-raising to preserve exception context.

```python
# (Hypothetical -- illustrative pattern)
try:
    data = json.loads(file_content)
except json.JSONDecodeError as e:
    raise ValidationError(
        field="config",
        message=f"Invalid JSON in config file: {e}",
    ) from e
```

**Why `from e`?**
- Preserves full stack trace
- Shows both original and new exception
- Easier to debug

---

## Value Object Patterns

### Immutable Dataclass Pattern

**Rule**: All value objects MUST be immutable.

```python
from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class Priority:
    """Value object representing task priority."""
    value: str

    def __post_init__(self) -> None:
        # Validation happens here
        valid = {"low", "medium", "high", "critical"}
        if self.value not in valid:
            raise ValidationError(field="priority", message=f"Invalid: {self.value}")

    def is_urgent(self) -> bool:
        """Business logic on value object."""
        return self.value in {"high", "critical"}
```

**Why `frozen=True`?**
- Prevents modification after creation
- Enables use as dict keys
- Thread-safe

**Why `slots=True`?**
- Reduces memory usage
- Slightly faster attribute access
- Prevents dynamic attribute addition

---

### Enum Value Object Pattern

**When**: Fixed set of values with behavior.

```python
from enum import Enum, auto

class WorkItemStatus(Enum):
    """Work item status with state machine."""

    PENDING = auto()
    IN_PROGRESS = auto()
    BLOCKED = auto()
    DONE = auto()
    CANCELLED = auto()

    def can_transition_to(self, target: "WorkItemStatus") -> bool:
        """Check if transition to target is allowed."""
        transitions = {
            WorkItemStatus.PENDING: {WorkItemStatus.IN_PROGRESS, WorkItemStatus.CANCELLED},
            WorkItemStatus.IN_PROGRESS: {WorkItemStatus.BLOCKED, WorkItemStatus.DONE},
            WorkItemStatus.BLOCKED: {WorkItemStatus.IN_PROGRESS, WorkItemStatus.CANCELLED},
            WorkItemStatus.DONE: set(),
            WorkItemStatus.CANCELLED: set(),
        }
        return target in transitions.get(self, set())

    def is_terminal(self) -> bool:
        """Check if this is a terminal state."""
        return self in {WorkItemStatus.DONE, WorkItemStatus.CANCELLED}
```

---

### Composite Value Object Pattern

**When**: Multiple related values form a concept.

```python
@dataclass(frozen=True, slots=True)
class DateRange:
    """Value object representing a date range."""
    start: datetime
    end: datetime

    def __post_init__(self) -> None:
        if self.start > self.end:
            raise ValidationError(
                field="date_range",
                message="Start date must be before end date",
            )

    def contains(self, date: datetime) -> bool:
        """Check if date falls within range."""
        return self.start <= date <= self.end

    def duration(self) -> timedelta:
        """Calculate duration of range."""
        return self.end - self.start
```

---

## Protocol vs ABC

### When to Use Protocol

**Use Protocol for**:
- Structural subtyping (duck typing)
- Interfaces defined by behavior, not inheritance
- Avoiding inheritance coupling

```python
from typing import Protocol

class IRepository(Protocol):
    """Port interface (structural subtyping)."""

    def save(self, item: WorkItem) -> None: ...
    def get(self, id: str) -> WorkItem | None: ...

# Any class with these methods implements IRepository
class FilesystemAdapter:
    def save(self, item: WorkItem) -> None:
        # Implementation
        ...

    def get(self, id: str) -> WorkItem | None:
        # Implementation
        ...

# No inheritance needed! FilesystemAdapter "implements" IRepository
repository: IRepository = FilesystemAdapter()  # ✅ Type-safe
```

**Advantages**:
- No inheritance required
- Works with existing classes
- More flexible

---

### When to Use ABC

**Use ABC for**:
- Enforcing interface implementation
- Shared base behavior
- Template method pattern

```python
from abc import ABC, abstractmethod

class AggregateRoot(ABC):
    """Base class for all aggregate roots."""

    def __init__(self) -> None:
        self._events: list[DomainEvent] = []
        self._version: int = 0

    @abstractmethod
    def _apply(self, event: DomainEvent) -> None:
        """Apply event to aggregate state. Must be implemented by subclasses."""
        ...

    def apply_event(self, event: DomainEvent) -> None:
        """Template method: common behavior for all aggregates."""
        self._apply(event)  # Calls subclass implementation
        self._events.append(event)
        self._version += 1

# Subclass must implement _apply
class WorkItem(AggregateRoot):
    def _apply(self, event: DomainEvent) -> None:
        if isinstance(event, WorkItemCreated):
            self.title = event.title
        # ...
```

**Advantages**:
- Enforces implementation (raises error if not implemented)
- Shared base behavior (template method)
- Inheritance-based type checking

---

### Decision Tree: Protocol vs ABC

```
Question: Does the interface need shared implementation?

├─ YES (shared behavior across implementations)
│  └─ Use ABC
│     Examples:
│     - AggregateRoot (apply_event, collect_events)
│     - DomainEvent (timestamp, event_type)
│
└─ NO (pure interface, no shared behavior)
   └─ Use Protocol
      Examples:
      - IRepository (just method signatures)
      - IEventStore (just method signatures)
      - ICommandHandler (just method signatures)
```

---

## TYPE_CHECKING Pattern

### Problem: Circular Imports

```python
# src/domain/aggregates/work_item.py
from src.domain.ports.repository import IRepository  # Imports repository

class WorkItem:
    def save_to(self, repository: IRepository) -> None:
        repository.save(self)

# src/domain/ports/repository.py
from src.domain.aggregates.work_item import WorkItem  # Imports work_item

class IRepository(Protocol):
    def save(self, item: WorkItem) -> None: ...

# ❌ Circular import: work_item → repository → work_item
```

---

### Solution: TYPE_CHECKING

```python
# src/domain/aggregates/work_item.py
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.domain.ports.repository import IRepository  # Only imported for type checking

class WorkItem:
    def save_to(self, repository: IRepository) -> None:  # ✅ Type hint works
        repository.save(self)

# src/domain/ports/repository.py
from __future__ import annotations
from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from src.domain.aggregates.work_item import WorkItem  # Only imported for type checking

class IRepository(Protocol):
    def save(self, item: WorkItem) -> None: ...  # ✅ Type hint works
```

**How it works**:
1. `TYPE_CHECKING` is `True` during type checking (mypy)
2. `TYPE_CHECKING` is `False` at runtime
3. Imports inside `if TYPE_CHECKING:` only happen during type checking
4. No circular import at runtime!

**When to use**:
- Circular imports for type hints
- Expensive imports only needed for type hints
- Forward references

---

## Evidence

> Verified references to actual Jerry codebase files demonstrating the patterns in this guide.

### Type Hints (H-11) -- Real Examples

**`src/bootstrap.py`** -- All public functions have type annotations:
```python
# (From: src/bootstrap.py, lines 126-139)
def get_session_repository() -> InMemorySessionRepository:
    """Get the shared session repository instance.

    Returns:
        InMemorySessionRepository singleton instance
    """
    global _session_repository
    if _session_repository is None:
        _session_repository = InMemorySessionRepository()
    return _session_repository
```

**`src/shared_kernel/vertex_id.py`** -- `from __future__ import annotations` with forward references:
```python
# (From: src/shared_kernel/vertex_id.py, lines 19-26)
from __future__ import annotations

import re
import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass
from re import Pattern
from typing import ClassVar
```

### Docstrings (H-12) -- Real Examples

**`src/session_management/domain/aggregates/session.py`** -- Google-style class and method docstrings:
```python
# (From: src/session_management/domain/aggregates/session.py, lines 56-88)
class Session(AggregateRoot):
    """Event-sourced aggregate for work session tracking.

    A Session represents a work context for an agent. It tracks which project
    is being worked on and the lifecycle of the session.

    ...

    Attributes:
        id: Unique identifier (SessionId value)
        status: Current lifecycle status
        ...
    """
```

### Import Organization -- Real Examples

**`src/session_management/domain/aggregates/session.py`** -- Correct import grouping (stdlib, then local):
```python
# (From: src/session_management/domain/aggregates/session.py, lines 23-39)
# stdlib
from collections.abc import Sequence
from datetime import datetime
from enum import Enum

# local (shared_kernel)
from src.shared_kernel.domain_event import DomainEvent
from src.work_tracking.domain.aggregates.base import AggregateRoot

# local (relative)
from ..events.session_events import (
    SessionAbandoned,
    SessionCompleted,
    SessionCreated,
    SessionProjectLinked,
)
```

### Exception Hierarchy -- Real Files

| Exception | File |
|-----------|------|
| `DomainError` | `src/shared_kernel/exceptions.py` |
| `ValidationError` | `src/shared_kernel/exceptions.py` |
| `NotFoundError` | `src/shared_kernel/exceptions.py` |
| `InvalidStateError` | `src/shared_kernel/exceptions.py` |
| `InvalidStateTransitionError` | `src/shared_kernel/exceptions.py` |
| `InvariantViolationError` | `src/shared_kernel/exceptions.py` |
| `ConcurrencyError` | `src/shared_kernel/exceptions.py` |
| `InvalidProjectIdError` | `src/session_management/domain/exceptions.py` |
| `ProjectNotFoundError` | `src/session_management/domain/exceptions.py` |

### Protocol Usage -- Real Examples

**`src/application/ports/primary/iquerydispatcher.py`** -- `@runtime_checkable` Protocol:
```python
# (From: src/application/ports/primary/iquerydispatcher.py, lines 44-71)
@runtime_checkable
class IQueryDispatcher(Protocol):
    """Protocol for query dispatchers."""

    def dispatch(self, query: Any) -> Any:
        """Dispatch a query to its registered handler."""
        ...
```

### Tool Configuration -- pyproject.toml

| Tool | Setting | Source |
|------|---------|--------|
| mypy | `strict = true`, `disallow_untyped_defs = true` | `pyproject.toml` lines 74-79 |
| ruff | `target-version = "py311"`, `line-length = 100` | `pyproject.toml` lines 81-83 |
| ruff lint | Selects: E, W, F, I, B, C4, UP | `pyproject.toml` lines 86-94 |

---

## References

### Related Documents

- [Coding Standards](../rules/coding-standards.md) - Enforcement rules (H-11, H-12)
- [Architecture Layers Guide](architecture-layers.md) - Layer import rules
- [Error Handling Guide](error-handling.md) - Exception hierarchy details

### External References

- [PEP 484](https://peps.python.org/pep-0484/) - Type Hints
- [PEP 604](https://peps.python.org/pep-0604/) - Union Syntax (`X | Y`)
- [PEP 585](https://peps.python.org/pep-0585/) - Generic Syntax (`list[T]`)
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html) - Docstring format
- [mypy Documentation](https://mypy.readthedocs.io/) - Type checker
