# PAT-ARCH-004: One-Class-Per-File (Flat Structure)

> **Status**: MANDATORY
> **Category**: Architecture
> **Also Known As**: Flat Structure, File-Per-Class

---

## Intent

Each Python file contains exactly one public class/protocol, enabling predictable file-to-class mapping for LLM navigation and reduced merge conflicts.

---

## Problem

Traditional Python favors "one idea per file" where related classes are grouped. This creates challenges for:
- **LLM Navigation**: AI agents can't predict file locations from class names
- **Merge Conflicts**: Parallel edits to different classes in the same file conflict
- **IDE Navigation**: "Go to definition" is less predictable
- **CQRS Alignment**: Commands, queries, and handlers naturally want separate files

---

## Solution

Enforce one public class per file with predictable naming conventions.

### File Naming Convention

| Type | File Name Pattern | Class Name |
|------|-------------------|------------|
| Aggregate | `work_item.py` | `WorkItem` |
| Value Object | `project_id.py` | `ProjectId` |
| Command | `create_task_command.py` | `CreateTaskCommand` |
| Query | `retrieve_project_query.py` | `RetrieveProjectQuery` |
| Command Handler | `create_task_command_handler.py` | `CreateTaskCommandHandler` |
| Query Handler | `retrieve_project_query_handler.py` | `RetrieveProjectQueryHandler` |
| Port (Interface) | `iquerydispatcher.py` | `IQueryDispatcher` |
| Adapter | `filesystem_project_adapter.py` | `FilesystemProjectAdapter` |

**Rule**: File name is snake_case version of class name.

---

## Rationale

### 1. LLM Navigation Optimization

```python
# Given class name "CreateTaskCommandHandler"
# LLM can predict: src/application/handlers/commands/create_task_command_handler.py

# This is deterministic and works for AI agents like Claude Code
```

### 2. Reduced Merge Conflicts

```
# Developer A edits CreateTaskCommand
# Developer B edits UpdateTaskCommand

# With one-class-per-file: No conflict (different files)
# With grouped files: Potential conflict in commands.py
```

### 3. Test File Mapping

```
src/application/commands/create_task_command.py
  ↓ maps to ↓
tests/unit/application/commands/test_create_task_command.py
```

### 4. CQRS Alignment

Each CQRS element naturally gets its own file:
- Command definition → `create_task_command.py`
- Command handler → `create_task_command_handler.py`
- Query definition → `retrieve_task_query.py`
- Query handler → `retrieve_task_query_handler.py`

---

## Jerry Implementation

### Directory Structure

```
src/application/handlers/
├── __init__.py              # Exports public API
├── commands/
│   ├── __init__.py
│   ├── create_task_command_handler.py
│   └── complete_task_command_handler.py
└── queries/
    ├── __init__.py
    ├── retrieve_project_context_query_handler.py
    ├── scan_projects_query_handler.py
    └── validate_project_query_handler.py
```

### Package `__init__.py` Pattern

Each `__init__.py` explicitly exports the public API:

```python
# src/application/handlers/__init__.py
from src.application.handlers.commands.create_task_command_handler import (
    CreateTaskCommandHandler,
)
from src.application.handlers.queries.retrieve_project_context_query_handler import (
    RetrieveProjectContextQueryHandler,
)

__all__ = [
    "CreateTaskCommandHandler",
    "RetrieveProjectContextQueryHandler",
]
```

**Benefit**: External consumers can import from the package level:
```python
from src.application.handlers import CreateTaskCommandHandler
```

---

## Exceptions Policy

### When Grouping is Acceptable

| Exception | Rationale | Example |
|-----------|-----------|---------|
| **Related Small Value Objects** | Cohesive concept, always used together | `Priority` enum + `PriorityLevel` type alias |
| **Domain Events for Same Aggregate** | Logically coupled, share context | `TaskCreated`, `TaskCompleted` in `task_events.py` |
| **Exception Hierarchy** | All exceptions for a domain | `DomainError`, `WorkItemNotFoundError` in `exceptions.py` |
| **Type Aliases** | Supporting types for main class | Type definitions alongside primary class |

### Decision Criteria

Apply these questions to determine if grouping is appropriate:

1. **Are the classes always used together?** If yes, group is acceptable.
2. **Would separating cause import chains?** If yes, group is acceptable.
3. **Is the total file under 200 lines?** If no, split required.
4. **Do the classes represent a single concept?** If yes, group is acceptable.
5. **Would an LLM naturally look for them together?** If yes, group is acceptable.

### Anti-Patterns (Always Avoid)

| Anti-Pattern | Why Problematic |
|--------------|-----------------|
| Multiple aggregates in one file | Each aggregate is a consistency boundary |
| Port + Adapter in same file | Violates dependency inversion |
| Command + Handler in same file | Different lifecycle and testing needs |
| Multiple unrelated protocols | No cohesive concept |

---

## Jerry Opinion

> **Jerry Decision**: We intentionally deviate from Python's "one idea per file" tradition because one-class-per-file optimizes for LLM agent navigation. This is a deliberate architectural choice, not ignorance of Python conventions.

Python's traditional approach groups related functionality into modules:
```python
# Traditional Python: decimal.py contains multiple classes
# - Decimal, Context, DecimalException (and subclasses)
# All revolve around the "decimal" topic
```

Jerry's approach prioritizes:
- Predictable file locations for AI agents
- Multi-agent development (reduced conflicts)
- Clean Architecture alignment

---

## Industry Comparison

| Framework | Pattern | Notes |
|-----------|---------|-------|
| **Django** | One idea per file | `models.py`, `views.py` can have many classes |
| **FastAPI** | Module-based | Routers, models, schemas grouped by domain |
| **Java** | One public class per file | Compiler-enforced |
| **C#** | One class per file | Strong convention |
| **Hexagonal Python** | Often flat structure | AWS recommends separate files for ports/adapters |

---

## Industry Prior Art

| Source | Description |
|--------|-------------|
| [Java Language Specification](https://docs.oracle.com/javase/specs/) | Public class naming rules |
| [AWS Hexagonal Architecture](https://docs.aws.amazon.com/prescriptive-guidance/latest/patterns/structure-a-python-project-in-hexagonal-architecture-using-aws-lambda.html) | Recommends separate files for adapters |
| [Wemake Python Styleguide](https://wemake-python-styleguide.readthedocs.io/) | WPS202: max-module-members limit |

---

## Enforcement

Architecture tests validate one-class-per-file:

```python
# tests/architecture/test_layer_boundaries.py

def test_one_class_per_file():
    """Each Python file should contain at most one public class."""
    for file in Path("src").rglob("*.py"):
        if file.name == "__init__.py":
            continue
        public_classes = count_public_classes(file)
        assert public_classes <= 1, f"{file} has {public_classes} public classes"
```

---

## Related Patterns

- [PAT-ARCH-001: Hexagonal Architecture](./hexagonal-architecture.md)
- [PAT-CQRS-001: Command Pattern](../cqrs/command-pattern.md)
- [PAT-CQRS-002: Query Pattern](../cqrs/query-pattern.md)

---

## Research Reference

Full research in `projects/PROJ-001-plugin-cleanup/research/td-017-e-003-flat-structure-patterns.md`

---

*Pattern documented by Claude (Opus 4.5) as part of TD-017*
