# PAT-CQRS-002: Query Pattern

> **Status**: MANDATORY
> **Category**: CQRS Pattern
> **Location**: `src/application/queries/`

---

## Overview

Queries represent requests for information. They are immutable DTOs that specify what data is needed. Queries are handled by query handlers which return DTOs, never domain entities.

---

## Industry Prior Art

| Source | Key Insight |
|--------|-------------|
| **Martin Fowler** | "Queries return data without modifying state" |
| **Greg Young** | "Read side and write side can have different models optimized for their purpose" |
| **Udi Dahan** | "Query-side can be denormalized for optimal read performance" |

---

## Jerry Implementation

### Query Structure

```python
# File: src/application/queries/retrieve_project_context_query.py
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RetrieveProjectContextQuery:
    """Query to retrieve project context.

    Queries are:
    - Immutable (frozen dataclass)
    - Named as {Verb}{Noun}Query
    - Pure data (no behavior)
    - Return DTOs, not domain entities

    File naming: {verb}_{noun}_query.py
    """

    base_path: str


@dataclass(frozen=True)
class ListWorkItemsQuery:
    """Query to list work items with optional filters."""

    status: str | None = None
    priority: str | None = None
    limit: int = 50
    offset: int = 0


@dataclass(frozen=True)
class GetWorkItemByIdQuery:
    """Query to get a single work item by ID."""

    work_item_id: str
```

---

## Query Handler

```python
# File: src/application/handlers/queries/retrieve_project_context_query_handler.py
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from src.application.queries.retrieve_project_context_query import (
    RetrieveProjectContextQuery,
)

if TYPE_CHECKING:
    from src.session_management.application.ports.project_repository import (
        IProjectRepository,
    )
    from src.session_management.application.ports.environment_provider import (
        IEnvironmentProvider,
    )


class RetrieveProjectContextQueryHandler:
    """Handler for RetrieveProjectContextQuery.

    Responsibilities:
    - Execute query logic
    - Return DTO (not domain entity)
    - No side effects

    Returns:
        Dictionary or DTO with query results
    """

    def __init__(
        self,
        repository: IProjectRepository,
        environment: IEnvironmentProvider,
    ) -> None:
        self._repository = repository
        self._environment = environment

    def handle(self, query: RetrieveProjectContextQuery) -> dict[str, Any]:
        """Execute the query.

        Returns:
            Project context as dictionary DTO
        """
        # Get active project from environment
        project_id = self._environment.get_env("JERRY_PROJECT")

        if not project_id:
            return {
                "project_active": False,
                "available_projects": self._list_projects(query.base_path),
            }

        # Get project details
        project = self._repository.get_project(query.base_path, project_id)

        if not project:
            return {
                "project_active": False,
                "error": f"Project {project_id} not found",
            }

        return {
            "project_active": True,
            "project_id": project_id,
            "project_path": project.path,
            "status": project.status,
        }

    def _list_projects(self, base_path: str) -> list[dict[str, str]]:
        """List available projects."""
        projects = self._repository.scan_projects(base_path)
        return [
            {"id": p.id, "status": p.status}
            for p in projects
        ]
```

---

## Query Verb Guidelines

| Verb | Usage | Example |
|------|-------|---------|
| Get | Single by ID | `GetWorkItemByIdQuery` |
| Retrieve | Single with context | `RetrieveProjectContextQuery` |
| List | Collection/paginated | `ListWorkItemsQuery` |
| Scan | Discovery/exploration | `ScanProjectsQuery` |
| Find | Search by criteria | `FindWorkItemsByStatusQuery` |
| Search | Full-text search | `SearchWorkItemsQuery` |
| Validate | Check validity | `ValidateProjectQuery` |
| Count | Aggregate count | `CountWorkItemsByStatusQuery` |

### Decision Matrix

```
                        ┌─────────────────────────────────────┐
                        │            Need full data?          │
                        │         Yes              No         │
      ┌─────────────────┼───────────────────┬─────────────────┤
      │ Single item     │  Get/Retrieve     │   Exists        │
      │                 │                   │                 │
      │ Collection      │  List/Find        │   Count         │
      │                 │                   │                 │
      │ Discovery       │  Scan/Search      │   Validate      │
      └─────────────────┴───────────────────┴─────────────────┘
```

---

## File Organization

```
src/application/
├── queries/
│   ├── __init__.py
│   ├── retrieve_project_context_query.py
│   ├── scan_projects_query.py
│   ├── validate_project_query.py
│   └── list_work_items_query.py
│
├── handlers/
│   └── queries/
│       ├── __init__.py
│       ├── retrieve_project_context_query_handler.py
│       ├── scan_projects_query_handler.py
│       ├── validate_project_query_handler.py
│       └── list_work_items_query_handler.py
│
└── dtos/
    ├── __init__.py
    ├── project_context_dto.py
    └── work_item_dto.py
```

---

## DTOs (Data Transfer Objects)

```python
# File: src/application/dtos/work_item_dto.py
from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class WorkItemDTO:
    """Read-only view of a work item.

    DTOs are optimized for reading and serialization.
    They may combine data from multiple aggregates.
    """

    id: str
    title: str
    status: str
    priority: str
    work_type: str
    created_at: datetime
    updated_at: datetime

    # Computed/denormalized fields
    days_since_created: int = 0
    subtask_count: int = 0
    completion_percentage: float = 0.0


@dataclass(frozen=True)
class WorkItemListDTO:
    """Paginated list of work items."""

    items: list[WorkItemDTO]
    total: int
    limit: int
    offset: int

    @property
    def has_more(self) -> bool:
        return self.offset + len(self.items) < self.total
```

---

## Query Dispatcher Integration

```python
# In bootstrap.py
def create_query_dispatcher() -> QueryDispatcher:
    repository = get_project_repository()
    environment = get_environment_provider()

    handlers = {
        RetrieveProjectContextQuery: RetrieveProjectContextQueryHandler(
            repository, environment
        ).handle,
        ScanProjectsQuery: ScanProjectsQueryHandler(repository).handle,
        ValidateProjectQuery: ValidateProjectQueryHandler(repository).handle,
    }

    return QueryDispatcher(handlers)

# Usage in CLI adapter
class CLIAdapter:
    def __init__(self, query_dispatcher: IQueryDispatcher) -> None:
        self._query_dispatcher = query_dispatcher

    def show_status(self) -> int:
        query = RetrieveProjectContextQuery(base_path=get_projects_dir())
        context = self._query_dispatcher.dispatch(query)

        if context["project_active"]:
            print(f"Active project: {context['project_id']}")
        else:
            print("No project active")

        return 0
```

---

## Testing Pattern

```python
def test_query_is_immutable():
    """Queries are frozen dataclasses."""
    query = RetrieveProjectContextQuery(base_path="/projects")

    with pytest.raises(FrozenInstanceError):
        query.base_path = "/other"


def test_handler_returns_dto_not_entity():
    """Handler returns DTO, not domain entity."""
    repository = InMemoryProjectRepository()
    repository.add_project(Project(id="PROJ-001", status="ACTIVE"))

    handler = RetrieveProjectContextQueryHandler(
        repository=repository,
        environment=MockEnvironment({"JERRY_PROJECT": "PROJ-001"}),
    )

    result = handler.handle(RetrieveProjectContextQuery(base_path="/projects"))

    # Result is a dict/DTO, not a Project entity
    assert isinstance(result, dict)
    assert result["project_id"] == "PROJ-001"


def test_list_query_returns_paginated_results():
    """List queries support pagination."""
    handler = ListWorkItemsQueryHandler(repository=mock_repo)

    query = ListWorkItemsQuery(limit=10, offset=20)
    result = handler.handle(query)

    assert isinstance(result, WorkItemListDTO)
    assert result.limit == 10
    assert result.offset == 20
```

---

## Anti-Patterns

### 1. Returning Domain Entities

```python
# WRONG: Returns domain entity
class GetTaskQueryHandler:
    def handle(self, query: GetTaskQuery) -> Task:  # Domain entity!
        return self._repository.get(query.task_id)

# CORRECT: Returns DTO
class GetTaskQueryHandler:
    def handle(self, query: GetTaskQuery) -> TaskDTO:
        task = self._repository.get(query.task_id)
        return TaskDTO(
            id=task.id,
            title=task.title,
            status=task.status.value,
        )
```

### 2. Query with Side Effects

```python
# WRONG: Query modifies state
class GetTaskQueryHandler:
    def handle(self, query: GetTaskQuery) -> TaskDTO:
        self._analytics.record_view(query.task_id)  # Side effect!
        return self._to_dto(task)

# CORRECT: Query is pure read
class GetTaskQueryHandler:
    def handle(self, query: GetTaskQuery) -> TaskDTO:
        return self._to_dto(self._repository.get(query.task_id))
```

### 3. Generic Find Query

```python
# WRONG: SQL-like generic query
FindQuery(table="tasks", where={"status": "done"}, select=["id", "title"])

# CORRECT: Domain-specific query
FindCompletedTasksQuery(since=datetime(2026, 1, 1))
```

---

## Jerry-Specific Decisions

> **Jerry Decision**: Query handlers return dictionaries or DTOs, never domain entities. This prevents domain objects from leaking to the interface layer.

> **Jerry Decision**: Query file naming is `{verb}_{noun}_query.py`. Handler is `{verb}_{noun}_query_handler.py`.

> **Jerry Decision**: Use `Retrieve` for single items with context, `Get` for simple lookup by ID, `List` for collections, `Scan` for discovery.

---

## References

- **Martin Fowler**: [CQRS](https://martinfowler.com/bliki/CQRS.html)
- **Greg Young**: [CQRS Documents](https://cqrs.files.wordpress.com/2010/11/cqrs_documents.pdf)
- **Design Canon**: Section 6.2 - Query Pattern
- **Related Patterns**: PAT-CQRS-003 (Dispatcher), PAT-CQRS-004 (Projection)
