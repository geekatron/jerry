# PAT-SVC-002: Application Service Pattern

> **Status**: MANDATORY
> **Category**: Application Service Pattern
> **Location**: `src/application/handlers/`

---

## Overview

Application Services (implemented as Command/Query Handlers in Jerry) orchestrate use cases by coordinating domain objects, repositories, and infrastructure. They define the application's boundary and transaction scope.

---

## Industry Prior Art

| Source | Key Insight |
|--------|-------------|
| **Eric Evans** | "Application Services coordinate tasks and delegate work to domain objects" |
| **Vaughn Vernon** | "Application Services are the direct clients of the domain model" |
| **Robert C. Martin** | "Use Cases are application-specific business rules" |

---

## Jerry Implementation

In Jerry, Application Services are implemented as **Command Handlers** and **Query Handlers** following the CQRS pattern.

### Command Handler (Write Operation)

```python
# File: src/application/handlers/commands/complete_work_item_command_handler.py
from __future__ import annotations

from typing import TYPE_CHECKING

from src.application.commands.complete_work_item_command import CompleteWorkItemCommand
from src.shared_kernel.exceptions import AggregateNotFoundError, QualityGateError
from src.work_tracking.domain.services.quality_validator import QualityValidator
from src.work_tracking.domain.value_objects.work_item_id import WorkItemId

if TYPE_CHECKING:
    from src.shared_kernel.domain_event import DomainEvent
    from src.work_tracking.domain.ports.work_item_repository import IWorkItemRepository


class CompleteWorkItemCommandHandler:
    """Application service for completing work items.

    Orchestrates the complete-work-item use case:
    1. Load aggregate from repository
    2. Validate quality gate (domain service)
    3. Execute domain operation
    4. Persist changes
    5. Return domain events

    Design Notes:
    - Coordinates between domain objects and infrastructure
    - Defines transaction boundary (load-modify-save)
    - Dependencies injected via constructor
    - Returns events for publishing
    """

    def __init__(
        self,
        repository: IWorkItemRepository,
        quality_validator: QualityValidator | None = None,
    ) -> None:
        """Initialize with dependencies.

        Args:
            repository: Work item repository
            quality_validator: Optional quality gate validator
        """
        self._repository = repository
        self._quality_validator = quality_validator or QualityValidator()

    def handle(self, command: CompleteWorkItemCommand) -> list[DomainEvent]:
        """Execute the complete work item use case.

        Args:
            command: Complete work item command

        Returns:
            List of domain events raised

        Raises:
            AggregateNotFoundError: If work item doesn't exist
            QualityGateError: If quality gate fails
            InvalidStateError: If work item cannot be completed
        """
        # 1. Load aggregate
        work_item_id = WorkItemId(command.work_item_id)
        work_item = self._repository.get_or_raise(work_item_id)

        # 2. Validate quality gate (if metrics provided)
        if command.quality_metrics:
            self._quality_validator.validate_for_completion(
                work_item,
                command.quality_metrics,
            )

        # 3. Execute domain operation (may raise InvalidStateError)
        work_item.complete(quality_passed=command.quality_passed)

        # 4. Collect events before save
        events = work_item.collect_events()

        # 5. Persist
        self._repository.save(work_item)

        return list(events)
```

---

### Query Handler (Read Operation)

```python
# File: src/application/handlers/queries/get_work_item_query_handler.py
from __future__ import annotations

from typing import TYPE_CHECKING

from src.application.dtos.work_item_dto import WorkItemDTO
from src.application.queries.get_work_item_query import GetWorkItemQuery
from src.shared_kernel.exceptions import AggregateNotFoundError
from src.work_tracking.domain.value_objects.work_item_id import WorkItemId

if TYPE_CHECKING:
    from src.work_tracking.domain.ports.work_item_repository import IWorkItemRepository


class GetWorkItemQueryHandler:
    """Application service for retrieving work item details.

    Handles read operation:
    1. Load aggregate from repository
    2. Transform to DTO
    3. Return DTO (never domain entity)

    Design Notes:
    - Read-only, no side effects
    - Returns DTO, not domain aggregate
    - May use read models for optimization
    """

    def __init__(self, repository: IWorkItemRepository) -> None:
        """Initialize with repository.

        Args:
            repository: Work item repository
        """
        self._repository = repository

    def handle(self, query: GetWorkItemQuery) -> WorkItemDTO:
        """Execute the get work item query.

        Args:
            query: Get work item query

        Returns:
            Work item DTO

        Raises:
            AggregateNotFoundError: If work item doesn't exist
        """
        # 1. Load aggregate
        work_item_id = WorkItemId(query.work_item_id)
        work_item = self._repository.get_or_raise(work_item_id)

        # 2. Transform to DTO (never expose domain entity)
        return self._to_dto(work_item)

    def _to_dto(self, work_item) -> WorkItemDTO:
        """Convert domain aggregate to DTO."""
        return WorkItemDTO(
            id=work_item.id,
            title=work_item.title,
            description=work_item.description,
            status=work_item.status.value,
            priority=work_item.priority.value,
            work_type=work_item.work_type.value,
            created_at=work_item.created_at,
            updated_at=work_item.updated_at,
            parent_id=work_item.parent_id,
            subtask_ids=list(work_item.subtask_ids),
            dependency_ids=list(work_item.dependency_ids),
        )
```

---

### Complex Use Case Handler

```python
# File: src/application/handlers/commands/create_work_item_with_subtasks_handler.py
from __future__ import annotations

from typing import TYPE_CHECKING

from src.application.commands.create_work_item_with_subtasks_command import (
    CreateWorkItemWithSubtasksCommand,
)
from src.work_tracking.domain.aggregates.work_item import WorkItem
from src.work_tracking.domain.value_objects.work_item_id import WorkItemId

if TYPE_CHECKING:
    from src.shared_kernel.domain_event import DomainEvent
    from src.work_tracking.domain.ports.work_item_repository import IWorkItemRepository


class CreateWorkItemWithSubtasksHandler:
    """Application service for creating work items with subtasks.

    Complex use case that:
    1. Creates parent work item
    2. Creates child subtasks
    3. Links them together
    4. Persists all in correct order

    Demonstrates:
    - Multi-aggregate coordination
    - Transaction boundary management
    - Event collection across aggregates
    """

    def __init__(
        self,
        repository: IWorkItemRepository,
        id_generator: Callable[[], str] | None = None,
    ) -> None:
        self._repository = repository
        self._id_generator = id_generator or WorkItemId.generate

    def handle(
        self,
        command: CreateWorkItemWithSubtasksCommand,
    ) -> list[DomainEvent]:
        """Execute the create with subtasks use case.

        Args:
            command: Command with parent and subtask data

        Returns:
            All domain events from the operation
        """
        all_events = []

        # 1. Create parent work item
        parent_id = self._id_generator()
        parent = WorkItem.create(
            id=parent_id,
            title=command.title,
            work_type=command.work_type,
            priority=command.priority,
            description=command.description,
        )
        all_events.extend(parent.collect_events())
        self._repository.save(parent)

        # 2. Create subtasks
        for subtask_data in command.subtasks:
            subtask_id = self._id_generator()
            subtask = WorkItem.create(
                id=subtask_id,
                title=subtask_data.title,
                work_type="subtask",
                priority=command.priority,
                parent_id=parent_id,
            )
            all_events.extend(subtask.collect_events())
            self._repository.save(subtask)

            # Link to parent
            parent = self._repository.get_or_raise(WorkItemId(parent_id))
            parent.add_subtask(subtask_id)
            all_events.extend(parent.collect_events())
            self._repository.save(parent)

        return all_events
```

---

## Application Service Responsibilities

| Responsibility | Example |
|---------------|---------|
| Load aggregates | `repository.get_or_raise(id)` |
| Coordinate domain services | `quality_validator.validate(...)` |
| Execute domain operations | `work_item.complete()` |
| Persist changes | `repository.save(aggregate)` |
| Collect/return events | `aggregate.collect_events()` |
| Transform to DTOs | `_to_dto(aggregate)` |

---

## Application Service vs Domain Service

| Aspect | Application Service | Domain Service |
|--------|---------------------|----------------|
| Layer | Application | Domain |
| Dependencies | Repository, Infrastructure | Domain objects only |
| State Changes | Coordinates persistence | No persistence |
| Transaction | Defines boundary | Part of transaction |
| Returns | Events or DTOs | Validation results |

---

## Testing Pattern

```python
def test_handler_completes_work_item():
    """Handler completes work item and returns events."""
    repository = InMemoryRepository()
    work_item = create_work_item(status=WorkItemStatus.IN_PROGRESS)
    repository.save(work_item)

    handler = CompleteWorkItemCommandHandler(
        repository=repository,
        quality_validator=QualityValidator(),
    )

    command = CompleteWorkItemCommand(
        work_item_id=work_item.id,
        quality_passed=True,
    )

    events = handler.handle(command)

    assert len(events) == 1
    assert isinstance(events[0], WorkItemCompleted)

    # Verify persisted
    loaded = repository.get(WorkItemId(work_item.id))
    assert loaded.status == WorkItemStatus.DONE


def test_handler_raises_when_quality_gate_fails():
    """Handler raises when quality gate fails."""
    repository = InMemoryRepository()
    work_item = create_work_item(status=WorkItemStatus.IN_PROGRESS)
    repository.save(work_item)

    handler = CompleteWorkItemCommandHandler(
        repository=repository,
        quality_validator=QualityValidator(coverage_threshold=0.9),
    )

    command = CompleteWorkItemCommand(
        work_item_id=work_item.id,
        quality_metrics=QualityMetrics(
            test_coverage=0.5,  # Below threshold
            documentation_complete=True,
            code_reviewed=True,
            acceptance_criteria_met=True,
        ),
    )

    with pytest.raises(QualityGateError):
        handler.handle(command)


def test_query_handler_returns_dto_not_entity():
    """Query handler returns DTO, not domain entity."""
    repository = InMemoryRepository()
    work_item = create_work_item()
    repository.save(work_item)

    handler = GetWorkItemQueryHandler(repository)
    query = GetWorkItemQuery(work_item_id=work_item.id)

    result = handler.handle(query)

    assert isinstance(result, WorkItemDTO)
    assert result.id == work_item.id
```

---

## Jerry-Specific Decisions

> **Jerry Decision**: Application services are Command/Query Handlers. No separate "service" class.

> **Jerry Decision**: Command handlers return `list[DomainEvent]`. Query handlers return DTOs.

> **Jerry Decision**: All dependencies are injected via constructor. No service locator pattern.

---

## Anti-Patterns

### 1. Domain Logic in Application Service

```python
# WRONG: Business logic in handler
class CompleteWorkItemHandler:
    def handle(self, command):
        work_item = self._repo.get(command.id)
        if work_item.status != "in_progress":  # Business logic!
            raise InvalidStateError()
        work_item._status = "done"  # Direct mutation!

# CORRECT: Delegate to domain
class CompleteWorkItemHandler:
    def handle(self, command):
        work_item = self._repo.get(command.id)
        work_item.complete()  # Domain encapsulates logic
```

### 2. Returning Domain Entities

```python
# WRONG: Exposing domain entity
class GetWorkItemHandler:
    def handle(self, query) -> WorkItem:  # Domain entity!
        return self._repo.get(query.id)

# CORRECT: Return DTO
class GetWorkItemHandler:
    def handle(self, query) -> WorkItemDTO:
        work_item = self._repo.get(query.id)
        return self._to_dto(work_item)
```

---

## References

- **Eric Evans**: Domain-Driven Design (2003), Chapter 4 - Isolating the Domain
- **Robert C. Martin**: Clean Architecture (2017), Chapter 20 - Use Cases
- **Design Canon**: Section 6.4 - Application Services
- **Related Patterns**: PAT-CQRS-001 (Command), PAT-CQRS-002 (Query), PAT-SVC-001 (Domain Service)
