# TD-017-E-005: CQRS and Event Sourcing Naming Conventions

**Document ID**: td-017-e-005
**Date**: 2026-01-11
**Author**: Claude Agent (ps-researcher)
**Topic**: CQRS and Event Sourcing Naming Conventions
**Status**: Complete

---

## Executive Summary

This research document synthesizes authoritative industry guidance on naming conventions for Command Query Responsibility Segregation (CQRS) and Event Sourcing patterns. It establishes conventions for Commands, Queries, Events, Handlers, and file naming that align with industry standards while preserving Jerry's established patterns.

**Key Finding**: Jerry's existing conventions align well with industry best practices, requiring only minor standardization around query verb prefixes.

---

## 1. Industry Standard Conventions

### 1.1 Authoritative Sources Consulted

| Source | Authority | Focus Area |
|--------|-----------|------------|
| [Martin Fowler - CQRS](https://www.martinfowler.com/bliki/CQRS.html) | Foundational | Pattern definition |
| [Greg Young - Event Sourcing](https://leanpub.com/eventsourcing) | Original Author | Event naming, ES patterns |
| [Microsoft Azure Architecture](https://learn.microsoft.com/en-us/azure/architecture/patterns/cqrs) | Enterprise | CQRS implementation patterns |
| [MediatR](https://github.com/jbogard/mediatr) | De facto .NET | Handler patterns |
| [Jimmy Bogard - Message Naming](https://www.jimmybogard.com/message-naming-conventions/) | MediatR Author | Naming conventions |
| [Cosmic Python - CQRS](https://www.cosmicpython.com/book/chapter_12_cqrs.html) | Python-specific | Python CQRS patterns |
| [Event-Driven.io](https://event-driven.io/en/cqrs_facts_and_myths_explained/) | Community | Modern CQRS practices |

### 1.2 Industry Consensus Summary

The industry has converged on the following naming principles:

1. **Commands**: Imperative mood verbs (`Create`, `Update`, `Delete`, `Complete`)
2. **Queries**: Retrieval verbs (`Get`, `Retrieve`, `List`, `Find`, `Search`)
3. **Events**: Past tense verbs indicating completed actions (`Created`, `Completed`, `Updated`)
4. **Handlers**: Append `Handler` suffix to the message type name

---

## 2. Command Naming Guidelines

### 2.1 Standard Pattern

```
{Verb}{Noun}Command
```

**Examples**:
- `CreateTaskCommand`
- `CompleteTaskCommand`
- `UpdateProjectCommand`
- `DeleteWorkItemCommand`

### 2.2 Verb Categories

| Category | Verbs | Use Case |
|----------|-------|----------|
| Creation | `Create`, `Add`, `Register` | New entity creation |
| Modification | `Update`, `Set`, `Modify`, `Change` | Entity updates |
| State Changes | `Complete`, `Cancel`, `Approve`, `Reject`, `Enable`, `Disable` | State transitions |
| Deletion | `Delete`, `Remove`, `Archive` | Entity removal |
| Domain Actions | `Book`, `Transfer`, `Allocate`, `Assign` | Business operations |

### 2.3 Anti-Patterns to Avoid

**CRUDy Commands** (Technical focus instead of business intent):

| Anti-Pattern | Preferred |
|--------------|-----------|
| `SetReservationStatusToReserved` | `BookHotelRoom` |
| `UpdateUserEmail` | `ChangeEmailAddress` |
| `InsertOrder` | `PlaceOrder` |

**Source**: [Microsoft Azure - CQRS Pattern](https://learn.microsoft.com/en-us/azure/architecture/patterns/cqrs)

> "Commands should represent specific business tasks instead of low-level data updates."

### 2.4 Command Structure (Python)

```python
@dataclass(frozen=True)
class CreateTaskCommand:
    """Command to create a new task.

    Attributes:
        title: The task title (required)
        description: Optional task description
        parent_id: Optional parent task reference
    """
    title: str
    description: str | None = None
    parent_id: TaskId | None = None
```

---

## 3. Query Naming Guidelines

### 3.1 Standard Pattern

```
{Verb}{Noun}Query
```

**Verb Conventions**:

| Verb | Use Case | Returns |
|------|----------|---------|
| `Retrieve` | Single entity by identifier | Entity or None |
| `Get` | Single entity (alias for Retrieve) | Entity or None |
| `List` | Collection of entities | List/Collection |
| `Scan` | Discovery/enumeration | List/Collection |
| `Find` | Search with criteria | List/Collection |
| `Search` | Full-text or complex search | List/Collection |

### 3.2 Examples

| Query Name | Purpose |
|------------|---------|
| `RetrieveProjectContextQuery` | Get single project context |
| `GetOrderByIdQuery` | Get order by identifier |
| `ListTasksQuery` | List all tasks (paginated) |
| `ScanProjectsQuery` | Discover available projects |
| `FindTasksByStatusQuery` | Find tasks matching criteria |
| `SearchProductsQuery` | Full-text product search |

### 3.3 Verb Selection Guidelines

**Source**: [Jimmy Bogard - Message Naming Conventions](https://www.jimmybogard.com/message-naming-conventions/)

| Scenario | Recommended Verb |
|----------|------------------|
| Fetch by ID | `Get` or `Retrieve` |
| Fetch all (paginated) | `List` |
| Discovery/enumeration | `Scan` |
| Criteria-based | `Find` |
| Text/complex search | `Search` |

### 3.4 Query Structure (Python)

```python
@dataclass(frozen=True)
class RetrieveProjectContextQuery:
    """Query to retrieve project context.

    Attributes:
        base_path: Path to the projects directory
    """
    base_path: str


@dataclass(frozen=True)
class ListTasksQuery:
    """Query to list tasks with optional filtering.

    Attributes:
        project_id: Filter by project (optional)
        status: Filter by status (optional)
        page: Page number (1-indexed)
        page_size: Items per page
    """
    project_id: str | None = None
    status: str | None = None
    page: int = 1
    page_size: int = 20
```

---

## 4. Event Naming Guidelines

### 4.1 Standard Pattern

```
{Noun}{Verb}ed  or  {Noun}{PastTenseVerb}
```

**Source**: [Greg Young's Event Sourcing teachings](https://cqrs.files.wordpress.com/2010/11/cqrs_documents.pdf)

> "All events should be represented as verbs in the past tense such as CustomerRelocated, CargoShipped, or InventoryLossageRecorded."

### 4.2 Examples

| Event | Meaning |
|-------|---------|
| `TaskCreated` | A task was created |
| `TaskCompleted` | A task was marked complete |
| `OrderPlaced` | An order was placed |
| `PaymentReceived` | A payment was received |
| `UserRegistered` | A user registered |
| `InventoryAdjusted` | Inventory was adjusted |

### 4.3 Event vs Command Naming

| Command (Imperative) | Event (Past Tense) |
|---------------------|-------------------|
| `CreateTask` | `TaskCreated` |
| `CompleteTask` | `TaskCompleted` |
| `PlaceOrder` | `OrderPlaced` |
| `ApproveInvoice` | `InvoiceApproved` |

**Source**: [CodeOpinion - Event Sourcing 101](https://codeopinion.com/event-sourcing-101-terminology/)

### 4.4 Avoid "Was" Prefix

**Preferred**: `TaskCreated`, `TaskCompleted`
**Avoid**: `TaskWasCreated`, `TaskWasCompleted`

The past tense verb inherently implies the action occurred; "was" is redundant.

### 4.5 Event Structure (Python)

```python
@dataclass(frozen=True)
class TaskCreated(DomainEvent):
    """Event raised when a task is created.

    Attributes:
        task_id: Unique identifier of the created task
        title: Title of the task
        created_at: Timestamp of creation
    """
    task_id: TaskId
    title: str
    created_at: datetime


@dataclass(frozen=True)
class TaskCompleted(DomainEvent):
    """Event raised when a task is completed.

    Attributes:
        task_id: Unique identifier of the completed task
        completed_at: Timestamp of completion
    """
    task_id: TaskId
    completed_at: datetime
```

---

## 5. Handler Naming Guidelines

### 5.1 Standard Pattern

```
{CommandOrQueryName}Handler
```

**Examples**:
- `CreateTaskCommandHandler`
- `RetrieveProjectContextQueryHandler`
- `ListTasksQueryHandler`

### 5.2 Handler Method Naming

| Library/Framework | Method Name |
|-------------------|-------------|
| MediatR (.NET) | `Handle()` |
| Cosmic Python | `handle()` |
| Jerry (Python) | `handle()` |

**Rationale**: Using a consistent `handle()` method allows for protocol/interface-based dispatching.

### 5.3 Handler Structure (Python)

```python
class CreateTaskCommandHandler:
    """Handler for CreateTaskCommand.

    Attributes:
        _repository: Repository for task persistence
    """

    def __init__(self, repository: ITaskRepository) -> None:
        """Initialize handler with dependencies.

        Args:
            repository: Repository for task operations
        """
        self._repository = repository

    def handle(self, command: CreateTaskCommand) -> list[DomainEvent]:
        """Handle the CreateTaskCommand.

        Args:
            command: Command containing task creation data

        Returns:
            List of domain events raised during handling
        """
        task = Task.create(title=command.title, description=command.description)
        self._repository.save(task)
        return task.collect_events()
```

---

## 6. File and Directory Naming Standards

### 6.1 Python File Naming (snake_case)

**Source**: [PEP 8 - Style Guide for Python Code](https://peps.python.org/pep-0008/)

| Type | Pattern | Example |
|------|---------|---------|
| Command | `{verb}_{noun}_command.py` | `create_task_command.py` |
| Query | `{verb}_{noun}_query.py` | `retrieve_project_context_query.py` |
| Command Handler | `{verb}_{noun}_command_handler.py` | `create_task_command_handler.py` |
| Query Handler | `{verb}_{noun}_query_handler.py` | `retrieve_project_context_query_handler.py` |
| Event | `{noun}_events.py` (grouped) | `task_events.py` |
| Port | `i{noun}.py` or `{noun}_port.py` | `irepository.py`, `event_store_port.py` |
| Adapter | `{tech}_{entity}_adapter.py` | `filesystem_project_adapter.py` |

### 6.2 Directory Structure

```
application/
├── commands/
│   ├── __init__.py
│   ├── create_task_command.py
│   └── complete_task_command.py
├── queries/
│   ├── __init__.py
│   ├── retrieve_project_context_query.py
│   ├── list_tasks_query.py
│   └── scan_projects_query.py
├── handlers/
│   ├── __init__.py
│   ├── commands/
│   │   ├── __init__.py
│   │   ├── create_task_command_handler.py
│   │   └── complete_task_command_handler.py
│   └── queries/
│       ├── __init__.py
│       ├── retrieve_project_context_query_handler.py
│       ├── list_tasks_query_handler.py
│       └── scan_projects_query_handler.py
├── ports/
│   ├── __init__.py
│   ├── primary/
│   │   ├── __init__.py
│   │   ├── icommanddispatcher.py
│   │   └── iquerydispatcher.py
│   └── secondary/
│       ├── __init__.py
│       ├── ieventstore.py
│       └── irepository.py
├── dispatchers/
│   ├── __init__.py
│   ├── command_dispatcher.py
│   └── query_dispatcher.py
└── dtos/
    ├── __init__.py
    └── project_context_dto.py
```

### 6.3 One Class Per File Rule

**Enforced**: Each Python file contains exactly ONE public class/protocol.

This enables:
- Easy file discovery by class name
- Clear import paths
- Reduced merge conflicts
- Better IDE navigation

---

## 7. Jerry-Specific Conventions

### 7.1 Preserved Jerry Patterns

The following patterns are already established in Jerry and align with industry standards:

| Category | Jerry Convention | Industry Standard | Status |
|----------|------------------|-------------------|--------|
| Commands | `CreateTaskCommand` | `CreateTaskCommand` | Aligned |
| Queries | `RetrieveProjectContextQuery` | `RetrieveProjectContextQuery` | Aligned |
| Events | `TaskCreated`, `TaskCompleted` | `TaskCreated`, `TaskCompleted` | Aligned |
| Handlers | `CreateTaskCommandHandler` | `CreateTaskCommandHandler` | Aligned |
| File naming | `create_task_command.py` | `create_task_command.py` | Aligned |

### 7.2 Query Verb Preferences

Jerry uses a mix of query verbs. Recommended standardization:

| Current | Standardized | Reasoning |
|---------|--------------|-----------|
| `RetrieveProjectContextQuery` | Keep | Single entity by context |
| `ScanProjectsQuery` | Keep | Discovery/enumeration |
| `ValidateProjectQuery` | Keep | Validation operation |
| `GetNextNumberQuery` | Keep | Simple getter |

### 7.3 Query Verb Decision Matrix

| Need | Verb | Example |
|------|------|---------|
| Get by ID | `Get` or `Retrieve` | `GetTaskByIdQuery` |
| Get all | `List` | `ListTasksQuery` |
| Discover/scan | `Scan` | `ScanProjectsQuery` |
| Validate | `Validate` | `ValidateProjectQuery` |
| Search | `Search` or `Find` | `SearchTasksQuery` |

### 7.4 Event Naming Convention

Jerry uses `{Noun}{PastVerb}` without "Was":
- `TaskCreated` (correct)
- `TaskCompleted` (correct)
- `ProjectValidated` (correct)

### 7.5 Domain Events File Organization

Group related events in single files:
- `task_events.py` contains `TaskCreated`, `TaskCompleted`, `TaskUpdated`
- `project_events.py` contains `ProjectCreated`, `ProjectArchived`

This is an exception to the one-class-per-file rule for closely related event types.

---

## 8. Summary Table

| Element | Pattern | File Pattern | Example |
|---------|---------|--------------|---------|
| Command | `{Verb}{Noun}Command` | `{verb}_{noun}_command.py` | `CreateTaskCommand` / `create_task_command.py` |
| Query | `{Verb}{Noun}Query` | `{verb}_{noun}_query.py` | `RetrieveProjectContextQuery` / `retrieve_project_context_query.py` |
| Event | `{Noun}{PastVerb}` | `{noun}_events.py` | `TaskCreated` / `task_events.py` |
| Command Handler | `{Verb}{Noun}CommandHandler` | `{verb}_{noun}_command_handler.py` | `CreateTaskCommandHandler` / `create_task_command_handler.py` |
| Query Handler | `{Verb}{Noun}QueryHandler` | `{verb}_{noun}_query_handler.py` | `RetrieveProjectContextQueryHandler` / `retrieve_project_context_query_handler.py` |

---

## 9. References

### Primary Sources

1. Fowler, Martin. "CQRS." martinfowler.com. https://www.martinfowler.com/bliki/CQRS.html
2. Young, Greg. "CQRS Documents." 2010. https://cqrs.files.wordpress.com/2010/11/cqrs_documents.pdf
3. Young, Greg. "Event Sourcing." Leanpub. https://leanpub.com/eventsourcing

### Implementation References

4. Bogard, Jimmy. "Message Naming Conventions." https://www.jimmybogard.com/message-naming-conventions/
5. Bogard, Jimmy. "MediatR." GitHub. https://github.com/jbogard/mediatr
6. Microsoft. "CQRS Pattern." Azure Architecture Center. https://learn.microsoft.com/en-us/azure/architecture/patterns/cqrs

### Python-Specific

7. Percival, Harry & Gregory, Bob. "Architecture Patterns with Python." O'Reilly. https://www.cosmicpython.com/book/chapter_12_cqrs.html
8. PEP 8. "Style Guide for Python Code." https://peps.python.org/pep-0008/

### Community Resources

9. Dudycz, Oskar. "CQRS facts and myths explained." Event-Driven.io. https://event-driven.io/en/cqrs_facts_and_myths_explained/
10. CodeOpinion. "Event Sourcing 101: Terminology." https://codeopinion.com/event-sourcing-101-terminology/
11. Choubey, Ankush. "Best Practices Command Naming Event Sourcing." https://www.ankushchoubey.com/software-blog/best-practices-command-naming-event-sourcing/

---

## Appendix A: Naming Quick Reference Card

```
COMMANDS (Imperative - What to do)
---------------------------------
Pattern:     {Verb}{Noun}Command
File:        {verb}_{noun}_command.py
Handler:     {Verb}{Noun}CommandHandler
Handler File: {verb}_{noun}_command_handler.py

Verbs: Create, Update, Delete, Complete, Cancel, Approve, Enable, Disable

QUERIES (Retrieval - What to get)
---------------------------------
Pattern:     {Verb}{Noun}Query
File:        {verb}_{noun}_query.py
Handler:     {Verb}{Noun}QueryHandler
Handler File: {verb}_{noun}_query_handler.py

Verbs: Get, Retrieve, List, Scan, Find, Search

EVENTS (Past Tense - What happened)
-----------------------------------
Pattern:     {Noun}{PastVerb}
File:        {noun}_events.py (grouped)
Base Class:  DomainEvent

Examples: TaskCreated, TaskCompleted, OrderPlaced, PaymentReceived
```

---

*End of Document*
