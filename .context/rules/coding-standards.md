# Coding Standards

> These rules are enforced across all Jerry framework development.
> They are loaded at session start and apply to all agents.

**Related Standards**:
- [Architecture Standards](architecture-standards.md) - Hexagonal, CQRS, Event Sourcing
- [File Organization](file-organization.md) - Directory structure, naming conventions
- [Testing Standards](testing-standards.md) - Test pyramid, BDD cycle, coverage
- [Tool Configuration](tool-configuration.md) - pytest, mypy, ruff configuration
- [Error Handling Standards](error-handling-standards.md) - Exception hierarchy
- [Pattern Catalog](../patterns/PATTERN-CATALOG.md) - Comprehensive pattern index

**Key Patterns**:
- [One-Class-Per-File](../patterns/architecture/one-class-per-file.md) (PAT-ARCH-004)
- [Immutable Value Object](../patterns/value-object/immutable-value-object.md) (PAT-VO-001)
- [Domain Event](../patterns/event/domain-event.md) (PAT-EVT-001)

---

## Language: Python 3.11+

### Type Hints

- **REQUIRED** on all public functions and methods
- **REQUIRED** on class attributes
- Use `from __future__ import annotations` for forward references
- Prefer `X | None` over `Optional[X]`
- Use `list[T]`, `dict[K, V]` over `List[T]`, `Dict[K, V]`

```python
# Good
def process_item(item: WorkItem, config: Config | None = None) -> Result:
    ...

# Bad
def process_item(item, config=None):
    ...
```

### Docstrings

- **REQUIRED** on all public functions, classes, and modules
- Use Google-style docstrings
- Include Args, Returns, Raises sections as appropriate

```python
def complete_work_item(item_id: str) -> WorkItem:
    """Mark a work item as completed.

    Args:
        item_id: The unique identifier of the work item.

    Returns:
        The updated WorkItem with completed status.

    Raises:
        WorkItemNotFoundError: If no item exists with the given ID.
        InvalidStateError: If the item cannot be completed from its current state.
    """
```

### Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| Modules | snake_case | `work_item.py` |
| Classes | PascalCase | `WorkItemRepository` |
| Functions | snake_case | `get_work_item` |
| Constants | UPPER_SNAKE | `MAX_RETRIES` |
| Private | _prefix | `_internal_helper` |
| Type Vars | T, K, V | `T = TypeVar('T')` |

### Line Length

- Maximum **100 characters** per line
- Exception: URLs in comments/docstrings

### Imports

- Group imports: stdlib, third-party, local
- Sort alphabetically within groups
- Use absolute imports for cross-package

```python
# Good
import json
from pathlib import Path

from src.domain.aggregates.work_item import WorkItem
from src.domain.ports.repository import IRepository
```

### TYPE_CHECKING Pattern

Use `TYPE_CHECKING` to avoid circular imports:

```python
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.application.ports.secondary.ieventstore import IEventStore
    from src.domain.aggregates.work_item import WorkItem


class WorkItemRepository:
    def __init__(self, event_store: IEventStore) -> None:
        self._event_store = event_store

    def get(self, id: str) -> WorkItem | None:
        ...
```

### Protocol Pattern

Use `Protocol` for interface definitions:

```python
from typing import Protocol, TypeVar

TAggregate = TypeVar("TAggregate")
TId = TypeVar("TId")


class IRepository(Protocol[TAggregate, TId]):
    """Port interface for aggregate persistence."""

    def get(self, id: TId) -> TAggregate | None: ...
    def get_or_raise(self, id: TId) -> TAggregate: ...
    def save(self, aggregate: TAggregate) -> None: ...
    def exists(self, id: TId) -> bool: ...
```

---

## Architecture Rules

### Domain Layer (`src/domain/`)

- **NO external imports** (only stdlib)
- **NO imports from** application/, infrastructure/, interface/
- Entities enforce their own invariants
- Value objects are immutable (use `@dataclass(frozen=True)`)
- Domain events use past tense (`WorkItemCompleted`)

### Application Layer (`src/application/`)

- **MAY import from** domain/
- **NO imports from** infrastructure/, interface/
- Commands return `None` or domain events
- Queries return DTOs, never domain entities

### Infrastructure Layer (`src/infrastructure/`)

- **MAY import from** domain/, application/
- **NO imports from** interface/
- Adapters MUST implement port interfaces
- Technical details stay encapsulated here

### Interface Layer (`src/interface/`)

- **MAY import from** all inner layers
- Handles translation between external and internal formats
- No business logic—delegate to application layer

---

## Value Object Coding

### Immutable Dataclass Pattern

```python
from dataclasses import dataclass

from src.shared_kernel.exceptions import ValidationError


@dataclass(frozen=True, slots=True)
class Priority:
    """Value object representing task priority."""

    value: str

    def __post_init__(self) -> None:
        valid_priorities = {"low", "medium", "high", "critical"}
        if self.value not in valid_priorities:
            raise ValidationError(
                field="priority",
                message=f"Must be one of: {valid_priorities}",
            )

    def is_urgent(self) -> bool:
        """Check if priority requires immediate attention."""
        return self.value in {"high", "critical"}
```

### Enum Value Object Pattern

```python
from enum import Enum, auto


class WorkItemStatus(Enum):
    """Enumeration of work item statuses with state machine."""

    PENDING = auto()
    IN_PROGRESS = auto()
    BLOCKED = auto()
    DONE = auto()
    CANCELLED = auto()

    def can_transition_to(self, target: "WorkItemStatus") -> bool:
        """Check if transition to target status is allowed."""
        transitions = {
            WorkItemStatus.PENDING: {WorkItemStatus.IN_PROGRESS, WorkItemStatus.CANCELLED},
            WorkItemStatus.IN_PROGRESS: {WorkItemStatus.BLOCKED, WorkItemStatus.DONE},
            WorkItemStatus.BLOCKED: {WorkItemStatus.IN_PROGRESS, WorkItemStatus.CANCELLED},
            WorkItemStatus.DONE: set(),
            WorkItemStatus.CANCELLED: set(),
        }
        return target in transitions.get(self, set())
```

**See Also**: [Value Object Patterns](../patterns/value-object/immutable-value-object.md)

---

## CQRS Naming Conventions

### File Naming

| Type | Pattern | Example |
|------|---------|---------|
| Command | `{verb}_{noun}_command.py` | `create_work_item_command.py` |
| Query | `{verb}_{noun}_query.py` | `retrieve_project_context_query.py` |
| Command Handler | `{verb}_{noun}_command_handler.py` | `create_work_item_command_handler.py` |
| Query Handler | `{verb}_{noun}_query_handler.py` | `retrieve_project_context_query_handler.py` |
| Event | `{noun}_events.py` | `work_item_events.py` |

### Class Naming

| Type | Pattern | Example |
|------|---------|---------|
| Command | `{Verb}{Noun}Command` | `CreateWorkItemCommand` |
| Query | `{Verb}{Noun}Query` | `RetrieveProjectContextQuery` |
| Handler | `{CommandOrQuery}Handler` | `CreateWorkItemCommandHandler` |
| Event | `{Noun}{PastVerb}` | `WorkItemCreated`, `TaskCompleted` |
| DTO | `{Noun}DTO` or `{Noun}Result` | `ProjectContextDTO` |

### Query Verbs

| Scenario | Verb | Example |
|----------|------|---------|
| Single by ID | `Get` or `Retrieve` | `RetrieveProjectContextQuery` |
| Collection | `List` | `ListWorkItemsQuery` |
| Discovery | `Scan` | `ScanProjectsQuery` |
| Validation | `Validate` | `ValidateProjectQuery` |
| Search | `Find` or `Search` | `FindTasksByStatusQuery` |

**See Also**: [Command Pattern](../patterns/cqrs/command-pattern.md), [Query Pattern](../patterns/cqrs/query-pattern.md)

---

## Domain Event Coding

### Event Structure

```python
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import ClassVar

from src.shared_kernel.events.domain_event import DomainEvent


@dataclass(frozen=True)
class WorkItemCompleted(DomainEvent):
    """Event raised when a work item is completed."""

    EVENT_TYPE: ClassVar[str] = "work_item.completed"

    work_item_id: str
    completed_at: datetime
    quality_passed: bool

    @classmethod
    def create(cls, work_item_id: str, quality_passed: bool = True) -> "WorkItemCompleted":
        """Factory method with automatic timestamp."""
        return cls(
            work_item_id=work_item_id,
            completed_at=datetime.now(timezone.utc),
            quality_passed=quality_passed,
        )
```

### Event Naming Rules

- Use **past tense** verbs: `Created`, `Updated`, `Completed`, `Cancelled`
- Include **aggregate type** in name: `WorkItemCreated`, `TaskStarted`
- Event type string: `{aggregate}.{verb}` → `work_item.created`

**See Also**: [Domain Event Pattern](../patterns/event/domain-event.md)

---

## Testing Standards

### Test File Naming

- Unit tests: `tests/unit/test_{module}.py`
- Integration tests: `tests/integration/test_{adapter}.py`
- E2E tests: `tests/e2e/test_{workflow}.py`

### Test Function Naming

Use `test_{scenario}_when_{condition}_then_{expected}`:

```python
def test_complete_item_when_in_progress_then_status_becomes_completed():
    ...

def test_complete_item_when_already_completed_then_raises_error():
    ...
```

### Test Structure

Use Arrange-Act-Assert (AAA) pattern:

```python
def test_example():
    # Arrange
    item = WorkItem(title="Test")

    # Act
    item.complete()

    # Assert
    assert item.status == Status.COMPLETED
```

---

## Git Standards

### Commit Messages

Use conventional commits format:

```
<type>(<scope>): <subject>

<body>

<footer>
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `refactor`: Code change that neither fixes nor adds
- `docs`: Documentation only
- `test`: Adding/updating tests
- `chore`: Build, CI, tooling

Example:
```
feat(worktracker): add ability to set due dates

Work items can now have optional due dates. The domain enforces
that due dates must be in the future when set.

Closes: WORK-042
```

### Branch Naming

- Feature: `feature/{work-item-id}-{short-description}`
- Fix: `fix/{work-item-id}-{short-description}`
- Release: `release/v{version}`

---

## Error Handling

### Exception Hierarchy

```
Exception
└── DomainError (base for all domain exceptions)
    ├── ValidationError (input validation failures)
    ├── NotFoundError (entity/aggregate not found)
    │   ├── WorkItemNotFoundError
    │   └── ProjectNotFoundError
    ├── InvalidStateError (state machine violations)
    │   └── InvalidStateTransitionError
    ├── ConcurrencyError (optimistic locking failures)
    └── BusinessRuleViolationError (domain rule violations)
```

### Exception Pattern

```python
from dataclasses import dataclass


@dataclass
class NotFoundError(DomainError):
    """Raised when an entity cannot be found."""

    entity_type: str
    entity_id: str

    def __str__(self) -> str:
        return f"{self.entity_type} '{self.entity_id}' not found"


@dataclass
class ValidationError(DomainError):
    """Raised when input validation fails."""

    field: str
    message: str
    value: str | None = None

    def __str__(self) -> str:
        return f"Validation failed for '{self.field}': {self.message}"
```

### Error Messages

- Be specific about what went wrong
- Include relevant context (IDs, values)
- Suggest corrective action when possible

```python
# Good
raise NotFoundError(
    entity_type="WorkItem",
    entity_id=item_id,
)

# Bad
raise Exception("Not found")
```

**See Also**: [Error Handling Standards](error-handling-standards.md)

---

## Documentation Standards

### File Headers

All Python files should start with a module docstring:

```python
"""
Module description.

This module provides {what it does}.

References:
    - {Relevant documentation}
"""
```

### Knowledge Capture

- Decisions: `docs/design/`
- Research: `docs/research/`
- Learnings: `docs/experience/`
- Patterns: `docs/wisdom/`

All documents must include:
- Document ID
- Date
- Author
- References/citations

---

## Enforcement

These standards are checked by:

1. **Pre-commit hooks**: Format, lint, type check
2. **CI pipeline**: Full test suite, coverage
3. **Code review**: Human verification
4. **QA Agent**: Automated review for patterns
