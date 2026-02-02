# PAT-CQRS-001: Command Pattern

> **Status**: MANDATORY
> **Category**: CQRS Pattern
> **Location**: `src/application/commands/`

---

## Overview

Commands represent intentions to change system state. They are immutable DTOs that carry data needed for a write operation. Commands are handled by command handlers which execute the business logic.

---

## Industry Prior Art

| Source | Key Insight |
|--------|-------------|
| **Bertrand Meyer** | "Command-Query Separation: methods should either change state or return data, not both" |
| **Martin Fowler** | "CQRS separates read and write operations into distinct models" |
| **Greg Young** | "Commands express intent; events express facts" |
| **Jimmy Bogard** | "MediatR: Commands are requests that change state" |

---

## Jerry Implementation

### Command Structure

```python
# File: src/application/commands/create_work_item_command.py
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CreateWorkItemCommand:
    """Command to create a new work item.

    Commands are:
    - Immutable (frozen dataclass)
    - Named as {Verb}{Noun}Command
    - Data transfer objects (no behavior)
    - Validated in handler, not in command

    File naming: {verb}_{noun}_command.py
    """

    title: str
    work_type: str = "task"
    priority: str = "medium"
    description: str = ""
    parent_id: str | None = None


@dataclass(frozen=True)
class CompleteWorkItemCommand:
    """Command to complete a work item."""

    work_item_id: str
    quality_passed: bool = True


@dataclass(frozen=True)
class UpdateWorkItemPriorityCommand:
    """Command to update work item priority."""

    work_item_id: str
    new_priority: str
```

---

## Command Handler

```python
# File: src/application/handlers/commands/create_work_item_command_handler.py
from __future__ import annotations

from typing import TYPE_CHECKING

from src.application.commands.create_work_item_command import CreateWorkItemCommand
from src.work_tracking.domain.aggregates.work_item import WorkItem
from src.work_tracking.domain.value_objects.work_item_id import WorkItemId

if TYPE_CHECKING:
    from src.shared_kernel.domain_event import DomainEvent
    from src.work_tracking.domain.ports.work_item_repository import IWorkItemRepository


class CreateWorkItemCommandHandler:
    """Handler for CreateWorkItemCommand.

    Responsibilities:
    - Validate command data
    - Execute domain logic
    - Persist aggregate
    - Return domain events

    Dependencies injected via constructor (DI).
    """

    def __init__(self, repository: IWorkItemRepository) -> None:
        self._repository = repository

    def handle(self, command: CreateWorkItemCommand) -> list[DomainEvent]:
        """Execute the command.

        Returns:
            List of domain events raised by the operation
        """
        # Generate ID
        work_item_id = WorkItemId.generate()

        # Create aggregate (validates invariants)
        work_item = WorkItem.create(
            id=work_item_id.value,
            title=command.title,
            work_type=command.work_type,
            priority=command.priority,
            description=command.description,
            parent_id=command.parent_id,
        )

        # Collect events before save
        events = work_item.collect_events()

        # Persist
        self._repository.save(work_item)

        return list(events)
```

---

## Command Naming Convention

| Verb | Usage | Example |
|------|-------|---------|
| Create | New entity | `CreateTaskCommand` |
| Add | Add to collection | `AddSubtaskCommand` |
| Register | Enroll/activate | `RegisterUserCommand` |
| Update | Modify attributes | `UpdateTitleCommand` |
| Set | Single attribute | `SetPriorityCommand` |
| Modify | Complex changes | `ModifySettingsCommand` |
| Complete | Finish/close | `CompleteTaskCommand` |
| Cancel | Abort/terminate | `CancelOrderCommand` |
| Approve | Accept/confirm | `ApproveRequestCommand` |
| Delete | Remove | `DeleteTaskCommand` |
| Remove | Remove from collection | `RemoveDependencyCommand` |
| Archive | Soft delete/hide | `ArchiveProjectCommand` |

---

## File Organization

```
src/application/
├── commands/
│   ├── __init__.py
│   ├── create_work_item_command.py      # CreateWorkItemCommand
│   ├── complete_work_item_command.py    # CompleteWorkItemCommand
│   └── update_priority_command.py       # UpdatePriorityCommand
│
├── handlers/
│   └── commands/
│       ├── __init__.py
│       ├── create_work_item_command_handler.py
│       ├── complete_work_item_command_handler.py
│       └── update_priority_command_handler.py
```

---

## Command Dispatcher Integration

```python
# In bootstrap.py
def create_command_dispatcher() -> CommandDispatcher:
    repository = get_work_item_repository()

    handlers = {
        CreateWorkItemCommand: CreateWorkItemCommandHandler(repository).handle,
        CompleteWorkItemCommand: CompleteWorkItemCommandHandler(repository).handle,
        UpdatePriorityCommand: UpdatePriorityCommandHandler(repository).handle,
    }

    return CommandDispatcher(handlers)

# Usage in CLI adapter
class CLIAdapter:
    def __init__(self, command_dispatcher: ICommandDispatcher) -> None:
        self._command_dispatcher = command_dispatcher

    def create_task(self, title: str, priority: str) -> int:
        command = CreateWorkItemCommand(
            title=title,
            priority=priority,
        )
        events = self._command_dispatcher.dispatch(command)
        print(f"Created work item with {len(events)} events")
        return 0
```

---

## Testing Pattern

```python
def test_create_work_item_command_is_immutable():
    """Commands are frozen dataclasses."""
    command = CreateWorkItemCommand(title="Test")

    with pytest.raises(FrozenInstanceError):
        command.title = "Changed"


def test_handler_creates_work_item():
    """Handler creates aggregate and returns events."""
    repository = InMemoryWorkItemRepository()
    handler = CreateWorkItemCommandHandler(repository)

    command = CreateWorkItemCommand(
        title="New Task",
        priority="high",
    )

    events = handler.handle(command)

    assert len(events) == 1
    assert isinstance(events[0], WorkItemCreated)
    assert events[0].title == "New Task"


def test_handler_persists_aggregate():
    """Handler saves aggregate to repository."""
    repository = InMemoryWorkItemRepository()
    handler = CreateWorkItemCommandHandler(repository)

    command = CreateWorkItemCommand(title="Test Task")
    events = handler.handle(command)

    # Verify persisted
    work_item_id = events[0].aggregate_id
    saved = repository.get(WorkItemId(work_item_id))
    assert saved is not None
    assert saved.title == "Test Task"
```

---

## Anti-Patterns

### 1. Commands with Business Logic

```python
# WRONG: Command contains logic
@dataclass(frozen=True)
class CreateTaskCommand:
    title: str

    def validate(self) -> None:
        if not self.title:
            raise ValueError()  # Logic in command!

# CORRECT: Handler validates
class CreateTaskCommandHandler:
    def handle(self, command: CreateTaskCommand):
        if not command.title.strip():
            raise ValidationError("title", "cannot be empty")
```

### 2. Commands Returning Data

```python
# WRONG: Command returns data (violates CQS)
class CreateTaskCommand:
    def execute(self) -> Task:  # Returns data!
        return Task(...)

# CORRECT: Command returns events, query reads data
events = handler.handle(CreateTaskCommand(...))
task = query_dispatcher.dispatch(GetTaskQuery(task_id))
```

### 3. CRUD-y Commands

```python
# WRONG: Generic CRUD
SetFieldCommand(entity_id="...", field="status", value="done")

# CORRECT: Intent-revealing command
CompleteTaskCommand(task_id="...")
```

---

## Jerry-Specific Decisions

> **Jerry Decision**: Commands return `list[DomainEvent]`, not aggregates. Events are collected before save and returned for publishing.

> **Jerry Decision**: Command file naming is `{verb}_{noun}_command.py` with snake_case. Handler is `{verb}_{noun}_command_handler.py`.

> **Jerry Decision**: Validation happens in handler, not in command. Commands are pure data transfer objects.

---

## References

- **Bertrand Meyer**: Object-Oriented Software Construction - CQS
- **Martin Fowler**: [CQRS](https://martinfowler.com/bliki/CQRS.html)
- **Greg Young**: [CQRS and Event Sourcing](https://cqrs.files.wordpress.com/2010/11/cqrs_documents.pdf)
- **Jimmy Bogard**: [MediatR](https://github.com/jbogard/mediatr)
- **Design Canon**: Section 6.1 - Command Pattern
- **Related Patterns**: PAT-CQRS-003 (Dispatcher), PAT-EVT-001 (DomainEvent)
