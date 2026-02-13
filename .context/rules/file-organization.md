# File Organization Standards

> Directory structure and file naming conventions for Jerry.
> Derived from Jerry Design Canon.

**Authoritative Pattern Source**: `.context/patterns/PATTERN-CATALOG.md`

---

## Project Root Structure

```
jerry/
├── .context/                  # Canonical Source (version-controlled, distributable)
│   ├── rules/                 # Behavioral rules (this file)
│   ├── patterns/              # Pattern catalog
│   └── templates/             # Worktracker and design templates
│
├── .claude/                   # Claude Code Config (synced from .context/)
│   ├── rules/ → .context/rules/   # Symlinked
│   ├── patterns/ → .context/patterns/ # Symlinked
│   ├── agents/                # Agent definitions
│   └── settings.json          # Claude Code settings
│
├── .claude-plugin/            # Distribution Layer
│   └── manifest.json          # Plugin manifest
│
├── skills/                    # Interface Layer (Natural Language)
│   ├── worktracker/           # Work tracking skill
│   ├── architecture/          # Architecture guidance skill
│   └── problem-solving/       # Domain use case invocation
│
├── scripts/                   # Execution Layer (CLI Shims)
│   └── session_start.py       # Session initialization hook
│
├── hooks/                     # Git and IDE Hooks
│   └── user-prompt-submit.py  # User prompt hook
│
├── src/                       # Hexagonal Core (Python)
│   ├── domain/                # Pure Business Logic
│   ├── application/           # Use Cases (CQRS)
│   ├── infrastructure/        # Adapters
│   ├── interface/             # Primary Adapters
│   ├── shared_kernel/         # Cross-cutting concerns
│   ├── session_management/    # Bounded Context
│   ├── work_tracking/         # Bounded Context
│   └── bootstrap.py           # Composition Root
│
├── tests/                     # Test Suites
│   ├── unit/                  # Unit tests
│   ├── integration/           # Integration tests
│   ├── e2e/                   # End-to-end tests
│   ├── contract/              # Contract tests
│   ├── architecture/          # Architecture tests
│   └── conftest.py            # Shared fixtures
│
├── docs/                      # Knowledge Repository
│   ├── design/                # ADRs and design docs
│   ├── knowledge/             # Patterns and exemplars
│   ├── governance/            # Constitution and behavior tests
│   └── INSTALLATION.md        # Installation guide
│
├── projects/                  # Project Workspaces
│   ├── README.md              # Project registry
│   └── PROJ-{NNN}-{slug}/     # Individual project
│
├── CLAUDE.md                  # Root context for Claude Code
├── AGENTS.md                  # Agent registry
├── pyproject.toml             # Python project config
└── pytest.ini                 # Test configuration
```

---

## Source Code Structure

### Domain Layer (`src/domain/`)

```
src/domain/
├── __init__.py
├── aggregates/
│   ├── __init__.py
│   ├── work_item.py           # WorkItem aggregate root
│   └── task.py                # Task aggregate root
├── entities/
│   ├── __init__.py
│   └── project_info.py        # ProjectInfo entity
├── value_objects/
│   ├── __init__.py
│   ├── project_id.py          # ProjectId value object
│   ├── priority.py            # Priority value object
│   └── work_type.py           # WorkType value object
├── events/
│   ├── __init__.py
│   ├── work_item_events.py    # WorkItem domain events
│   └── task_events.py         # Task domain events
├── services/
│   ├── __init__.py
│   └── quality_validator.py   # Domain service
├── ports/
│   ├── __init__.py
│   └── repository.py          # IRepository port
└── exceptions.py              # Domain exceptions
```

### Application Layer (`src/application/`)

```
src/application/
├── __init__.py
├── commands/
│   ├── __init__.py
│   ├── create_task_command.py
│   └── complete_task_command.py
├── queries/
│   ├── __init__.py
│   ├── retrieve_project_context_query.py
│   ├── scan_projects_query.py
│   └── validate_project_query.py
├── handlers/
│   ├── __init__.py
│   ├── commands/
│   │   ├── __init__.py
│   │   ├── create_task_command_handler.py
│   │   └── complete_task_command_handler.py
│   └── queries/
│       ├── __init__.py
│       ├── retrieve_project_context_query_handler.py
│       ├── scan_projects_query_handler.py
│       └── validate_project_query_handler.py
├── ports/
│   ├── __init__.py
│   ├── primary/
│   │   ├── __init__.py
│   │   ├── iquerydispatcher.py
│   │   └── icommanddispatcher.py
│   └── secondary/
│       ├── __init__.py
│       ├── ieventstore.py
│       └── isnapshotstore.py
├── projections/
│   ├── __init__.py
│   └── project_context_projection.py
├── dispatchers/
│   ├── __init__.py
│   ├── query_dispatcher.py
│   └── command_dispatcher.py
└── dtos/
    ├── __init__.py
    └── project_context_dto.py
```

### Infrastructure Layer (`src/infrastructure/`)

```
src/infrastructure/
├── __init__.py
├── adapters/
│   ├── __init__.py
│   ├── persistence/
│   │   ├── __init__.py
│   │   ├── filesystem_project_adapter.py
│   │   └── json_file_repository.py
│   ├── messaging/
│   │   ├── __init__.py
│   │   └── inmemory_event_store.py
│   └── external/
│       ├── __init__.py
│       └── os_environment_adapter.py
├── read_models/
│   ├── __init__.py
│   └── project_list_read_model.py
└── internal/
    ├── __init__.py
    ├── file_store.py          # IFileStore implementation
    └── serializer.py          # ISerializer implementation
```

### Interface Layer (`src/interface/`)

```
src/interface/
├── __init__.py
├── cli/
│   ├── __init__.py
│   ├── main.py                # CLI entry point
│   ├── adapter.py             # CLIAdapter (Clean Architecture)
│   └── formatters/
│       ├── __init__.py
│       └── table_formatter.py
├── api/
│   ├── __init__.py
│   └── routes/
│       └── __init__.py
└── hooks/
    ├── __init__.py
    └── session_start.py       # Session hook
```

---

## Test Structure

```
tests/
├── conftest.py                # Shared fixtures
├── unit/
│   ├── domain/
│   │   ├── test_work_item.py
│   │   └── test_project_id.py
│   └── application/
│       └── test_handlers.py
├── integration/
│   ├── test_filesystem_adapter.py
│   └── test_event_store.py
├── e2e/
│   └── test_cli_workflow.py
├── contract/
│   └── test_hook_output.py
├── architecture/
│   ├── test_composition_root.py
│   └── test_layer_boundaries.py
└── shared_kernel/
    ├── test_vertex_id.py
    └── test_domain_event.py
```

### Test File Naming

| Type | Pattern | Example |
|------|---------|---------|
| Unit | `test_{module}.py` | `test_work_item.py` |
| Integration | `test_{adapter}.py` | `test_filesystem_adapter.py` |
| E2E | `test_{workflow}.py` | `test_cli_workflow.py` |
| Contract | `test_{contract}.py` | `test_hook_output.py` |
| Architecture | `test_{concern}.py` | `test_layer_boundaries.py` |

---

## Project Workspace Structure

```
projects/PROJ-{NNN}-{slug}/
├── PLAN.md                    # Implementation plan
├── WORKTRACKER.md             # Work tracking document
├── .jerry/
│   └── data/
│       └── items/             # Work item state
├── work/
│   ├── PHASE-01-*.md          # Phase documents
│   ├── PHASE-BUGS.md          # Bug tracking
│   ├── PHASE-TECHDEBT.md      # Tech debt tracking
│   └── PHASE-DISCOVERY.md     # Discoveries
├── research/
│   └── {project}-{id}-*.md    # Research artifacts
├── analysis/
│   └── {project}-{id}-*.md    # Analysis artifacts
├── synthesis/
│   └── {project}-{id}-*.md    # Synthesis documents
├── decisions/
│   └── ADR-*.md               # Architecture Decision Records
├── reports/
│   └── {project}-*.md         # Status reports
├── runbooks/
│   └── RUNBOOK-*.md           # Execution guides
└── reviews/
    └── {project}-*.md         # Review documents
```

---

## Naming Conventions

### File Names

| Type | Convention | Example |
|------|------------|---------|
| Python modules | snake_case | `work_item.py` |
| Test files | `test_` prefix | `test_work_item.py` |
| Markdown docs | UPPER_SNAKE or kebab | `WORKTRACKER.md`, `file-organization.md` |
| ADRs | ADR-{id}-{slug} | `ADR-001-hexagonal-architecture.md` |
| Research | {project}-{type}-{id}-*.md | `PROJ-001-e-011-design-canon.md` |

### Class Names

| Type | Convention | Example |
|------|------------|---------|
| Aggregates | PascalCase | `WorkItem` |
| Value Objects | PascalCase | `ProjectId` |
| Events | PascalCase (past tense) | `TaskCompleted` |
| Commands | PascalCase (verb + noun) | `CreateTaskCommand` |
| Queries | PascalCase (verb + noun) | `RetrieveProjectContextQuery` |
| Handlers | PascalCase + Handler | `CreateTaskCommandHandler` |
| Ports | I + PascalCase | `IRepository`, `IEventStore` |
| Adapters | PascalCase + Adapter | `FilesystemProjectAdapter` |

### Module `__init__.py` Exports

Each `__init__.py` should explicitly export public API:

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

---

## One Class Per File Rule

**MANDATORY**: Each Python file contains exactly ONE public class/protocol.

**Correct**:
```
src/application/ports/primary/
├── iquerydispatcher.py        # Contains IQueryDispatcher
└── icommanddispatcher.py      # Contains ICommandDispatcher
```

**Incorrect**:
```
src/application/ports/
└── dispatcher.py              # Contains both IQueryDispatcher AND ICommandDispatcher
```

**Exception**: Related small value objects may be grouped:
```python
# src/domain/value_objects/priority.py
# Contains Priority enum and related types
```

---

## References

- **Pattern Catalog**: `.claude/patterns/PATTERN-CATALOG.md`
- **Design Canon**: `projects/PROJ-001-plugin-cleanup/synthesis/PROJ-001-e-011-v1-jerry-design-canon.md`
- **Architecture Standards**: `.claude/rules/architecture-standards.md`
