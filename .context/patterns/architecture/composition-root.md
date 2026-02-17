# PAT-ARCH-005: Composition Root Pattern

> **Status**: MANDATORY
> **Category**: Architecture
> **Also Known As**: Dependency Injection Container, Factory Root

---

## Intent

Single location (`bootstrap.py`) where all dependencies are wired, isolating dependency resolution from business logic.

---

## Problem

When adapters instantiate their own dependencies:
- Testing becomes difficult (can't inject mocks)
- Implementation details leak into business code
- Changing implementations requires modifying multiple files
- No single place to understand the wiring

### Anti-Pattern Example

```python
# WRONG - Adapter instantiates its own dependencies
class CLIAdapter:
    def cmd_init(self, args):
        # Direct infrastructure instantiation in adapter
        repository = FilesystemProjectAdapter()  # VIOLATION!
        environment = OsEnvironmentAdapter()     # VIOLATION!
        query = GetProjectContextQuery(repository=repository, environment=environment)
        return query.execute()
```

---

## Solution

Create a single factory function that wires all dependencies at application startup.

### Structure

```python
# src/bootstrap.py - Composition Root

def create_query_dispatcher() -> QueryDispatcher:
    """Factory function that wires all dependencies.

    This is the ONLY place infrastructure adapters are instantiated.
    """
    # 1. Create infrastructure adapters (driven/secondary)
    repository = FilesystemProjectAdapter()
    environment = OsEnvironmentAdapter()

    # 2. Create handlers with injected dependencies
    handler = RetrieveProjectContextQueryHandler(
        repository=repository,
        environment=environment,
    )

    # 3. Configure dispatcher with handlers
    dispatcher = QueryDispatcher()
    dispatcher.register(RetrieveProjectContextQuery, handler.handle)

    return dispatcher


def create_cli_adapter() -> CLIAdapter:
    """Create fully-wired CLI adapter."""
    dispatcher = create_query_dispatcher()
    return CLIAdapter(dispatcher=dispatcher)
```

---

## Key Principles

### 1. Single Point of Wiring

All adapter instantiation happens ONLY in `bootstrap.py`.

```python
# Good - Bootstrap creates adapters
def create_query_dispatcher():
    repository = FilesystemProjectAdapter()  # Created here
    ...

# Bad - Handler creates its own adapter
class SomeHandler:
    def __init__(self):
        self._repo = FilesystemProjectAdapter()  # VIOLATION!
```

### 2. No Self-Instantiation

Adapters NEVER create their own dependencies.

```python
# Good - Dependencies received via constructor
class RetrieveProjectContextQueryHandler:
    def __init__(self, repository: IProjectRepository, environment: IEnvironment):
        self._repository = repository
        self._environment = environment

# Bad - Self-instantiation
class RetrieveProjectContextQueryHandler:
    def __init__(self):
        self._repository = FilesystemProjectAdapter()  # VIOLATION!
```

### 3. Constructor Injection

All dependencies passed via constructors, never via method parameters.

```python
# Good - Constructor injection
adapter = CLIAdapter(dispatcher=dispatcher)

# Bad - Method injection for recurring dependency
adapter = CLIAdapter()
adapter.handle_command(command, dispatcher=dispatcher)  # Confusing!
```

### 4. Runtime Selection

Implementation selection happens at startup, not scattered through code.

```python
def create_repository() -> IProjectRepository:
    if os.getenv("TEST_MODE"):
        return InMemoryProjectRepository()
    else:
        return FilesystemProjectAdapter()
```

---

## Jerry Implementation

### File Location

`src/bootstrap.py`

### Current Implementation

```python
"""
Composition root for Jerry framework.

This module is the ONLY place where infrastructure adapters are instantiated
and wired to their ports. All other modules receive dependencies via
constructor injection.

References:
    - PAT-ARCH-005 (Composition Root)
    - PAT-ARCH-001 (Hexagonal Architecture)
"""
from src.application.dispatchers.query_dispatcher import QueryDispatcher
from src.application.handlers.queries.retrieve_project_context_query_handler import (
    RetrieveProjectContextQueryHandler,
)
from src.application.queries.retrieve_project_context_query import (
    RetrieveProjectContextQuery,
)
from src.infrastructure.adapters.persistence.filesystem_project_adapter import (
    FilesystemProjectAdapter,
)
from src.infrastructure.adapters.external.os_environment_adapter import (
    OsEnvironmentAdapter,
)
from src.interface.cli.adapter import CLIAdapter


def create_query_dispatcher() -> QueryDispatcher:
    """Create a fully-wired query dispatcher."""
    repository = FilesystemProjectAdapter()
    environment = OsEnvironmentAdapter()

    handler = RetrieveProjectContextQueryHandler(
        repository=repository,
        environment=environment,
    )

    dispatcher = QueryDispatcher()
    dispatcher.register(RetrieveProjectContextQuery, handler.handle)

    return dispatcher


def create_cli_adapter() -> CLIAdapter:
    """Create a fully-wired CLI adapter."""
    dispatcher = create_query_dispatcher()
    return CLIAdapter(dispatcher=dispatcher)
```

---

## Enforcement

Architecture tests validate composition root isolation:

```python
# tests/architecture/test_composition_root.py

def test_cli_adapter_has_no_infrastructure_imports():
    """CLIAdapter must not import infrastructure directly."""
    adapter_path = Path("src/interface/cli/adapter.py")
    imports = get_imports_from_file(adapter_path)
    assert not has_infrastructure_import(imports)

def test_bootstrap_imports_infrastructure():
    """Bootstrap SHOULD import infrastructure adapters."""
    bootstrap_path = Path("src/bootstrap.py")
    imports = get_imports_from_file(bootstrap_path)
    assert has_infrastructure_import(imports)

def test_handlers_do_not_import_infrastructure():
    """Handlers must not import infrastructure directly."""
    handler_files = Path("src/application/handlers").rglob("*.py")
    for file in handler_files:
        if file.name == "__init__.py":
            continue
        imports = get_imports_from_file(file)
        assert not has_infrastructure_import(imports), f"{file} violates boundary"
```

---

## Industry Prior Art

| Source | Author | Description |
|--------|--------|-------------|
| [Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html) | Robert C. Martin | "Details like the database don't matter to the business rules" |
| [Hexagonal Architecture in Python](https://blog.szymonmiks.pl/p/hexagonal-architecture-in-python/) | Szymon Miks | Python-specific implementation guide |
| [Dependency Injection Principles](https://martinfowler.com/articles/injection.html) | Martin Fowler | Foundational DI concepts |

---

## Factory vs Container

| Approach | Pros | Cons | When to Use |
|----------|------|------|-------------|
| **Factory Functions** | Simple, explicit, no dependencies | Manual wiring | Small to medium apps (Jerry) |
| **DI Container** | Automatic resolution, less boilerplate | Added complexity | Large apps with many dependencies |

**Jerry Decision**: We use factory functions for simplicity and explicitness.

---

## Related Patterns

- [PAT-ARCH-001: Hexagonal Architecture](./hexagonal-architecture.md)
- [PAT-CQRS-004: Dispatcher Pattern](../cqrs/dispatcher-pattern.md)
- [PAT-ARCH-002: Primary/Secondary Ports](./ports-adapters.md)

---

## TD-015 Reference

This pattern was implemented as part of TD-015 (CLI Architecture Remediation).

Commits:
- `e791dc6`: Implement CLIAdapter with dispatcher injection
- `32b4906`: Implement dispatcher pattern and composition root

---

*Pattern documented by Claude (Opus 4.5) as part of TD-017*
