# Response: CreateProjectCommand and Handler Implementation

## Executive Summary

The developer's suggestion to place both the command and handler in a single file violates **H-10 (One class per file)**, a HARD architectural constraint in the Jerry Framework. This response explains why H-10 exists, demonstrates the correct approach, and provides the implementation.

---

## Why H-10 Cannot Be Overridden

### The HARD Rule

From `.context/rules/architecture-standards.md`:

> **H-10:** Each Python file SHALL contain exactly ONE public class or protocol.
> **Consequence:** AST check fails. CI blocks merge.

H-10 is a HARD rule, meaning:
- It CANNOT be overridden by developer preference or external conventions (like MediatR)
- Violations are blocked by AST enforcement at CI
- The rule exists for architectural integrity, not style preference

### Why H-10 Exists

1. **File-Level Single Responsibility:** One class per file enforces single responsibility at the file level, not just the class level. This makes discoverability, testing, and import management tractable.

2. **Import Clarity:** When a developer imports `from application.commands.create_project_command import CreateProjectCommand`, they know exactly what that file contains. Mixed imports (command + handler from one file) create ambiguity.

3. **Dependency Graph Clarity:** The presence of a handler in `create_project_command.py` creates a hidden dependency. Handlers depend on the command, but the handler is co-located. This breaks dependency graph visibility.

4. **Hexagonal Architecture Alignment:** In the Jerry Framework's hexagonal architecture:
   - Commands are **primary ports** (inbound requests)
   - Handlers are **port adapters** (implementation)

   These belong to different architectural concerns and should be in separate files.

5. **CI Enforcement:** The framework includes AST checks that verify H-10 compliance. A pull request violating H-10 will be rejected at CI, requiring rework.

### Why MediatR's Pattern Doesn't Apply Here

MediatR (a .NET CQRS library) co-locates commands and handlers because:
- It uses reflection to discover handlers at runtime based on type names
- The discovery mechanism *requires* specific namespace/file conventions
- .NET's module system and compilation model differ from Python's import system

Jerry Framework uses explicit imports and Python's dynamic dispatch, which *enables* separate files and makes co-location unnecessary. The Jerry Framework chooses to enforce this separation for architectural clarity.

---

## Correct Implementation: Separate Files

The correct approach creates **four files** (not one):

1. **`create_project_command.py`** – The command class only
2. **`project_repository.py`** – The ProjectRepository port (secondary port)
3. **`create_project_command_handler.py`** – The handler class only
4. **`__init__.py`** – Exports all three for convenience

### File 1: `src/application/commands/create_project_command.py`

```python
"""CreateProjectCommand – Request to create a new project."""

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True, slots=True)
class CreateProjectCommand:
    """Request to create a new project.

    Fields:
        title: Project display name (non-empty string)
        description: Project summary (may be empty)
        owner_id: User ID of the project owner (non-empty string)
    """

    title: str
    description: str
    owner_id: str

    def __post_init__(self) -> None:
        """Validate command fields."""
        if not self.title or not self.title.strip():
            raise ValueError("title cannot be empty")
        if not self.owner_id or not self.owner_id.strip():
            raise ValueError("owner_id cannot be empty")
```

**Why separate:** The command is a **data structure** that represents user intent. It should have no coupling to handler implementation details.

### File 2: `src/application/ports/project_repository.py`

```python
"""ProjectRepository – Secondary port for project persistence."""

from typing import Protocol


class ProjectRepository(Protocol):
    """Port for persisting projects (secondary port).

    Implemented by infrastructure adapters (FilesystemProjectAdapter, etc.).
    This is a secondary port: the handler (primary adapter) depends on this
    abstraction, and infrastructure adapters implement it.
    """

    def add(self, project_id: str, title: str, description: str, owner_id: str) -> None:
        """Add a new project to the repository.

        Args:
            project_id: Unique project identifier.
            title: Project display name.
            description: Project summary.
            owner_id: User ID of the project owner.
        """
        ...
```

**Why separate:** Ports are architectural abstractions that define contracts between layers. Secondary ports (like repository interfaces) are defined in `application/ports/` and implemented by infrastructure adapters. Separating the port from the handler clarifies this dependency direction.

### File 3: `src/application/commands/create_project_command_handler.py`

```python
"""CreateProjectCommandHandler – Handler for CreateProjectCommand."""

from application.commands.create_project_command import CreateProjectCommand
from application.ports.project_repository import ProjectRepository


class CreateProjectCommandHandler:
    """Handler for CreateProjectCommand.

    Responsibilities:
        1. Validate the command (basic validation; domain validation in aggregate)
        2. Generate a unique project ID
        3. Create the project aggregate
        4. Persist the project via the repository

    Dependencies:
        - ProjectRepository (injected via __init__)
    """

    def __init__(self, repository: ProjectRepository) -> None:
        """Initialize the handler with a project repository.

        Args:
            repository: The project repository adapter (dependency injection).
        """
        self.repository = repository

    def handle(self, command: CreateProjectCommand) -> str:
        """Execute the command and return the created project ID.

        Args:
            command: The CreateProjectCommand to execute.

        Returns:
            The project ID of the newly created project.

        Raises:
            ValueError: If command validation fails.
        """
        # Additional validation beyond command constructor
        if len(command.title.strip()) > 255:
            raise ValueError("title must be 255 characters or fewer")
        if len(command.description) > 2000:
            raise ValueError("description must be 2000 characters or fewer")

        # Generate project ID (in production, use UUID or domain service)
        project_id = self._generate_project_id()

        # Persist the project
        self.repository.add(
            project_id=project_id,
            title=command.title,
            description=command.description,
            owner_id=command.owner_id,
        )

        return project_id

    @staticmethod
    def _generate_project_id() -> str:
        """Generate a unique project ID."""
        from uuid import uuid4
        return f"proj_{uuid4().hex[:12]}"
```

**Why separate:** The handler is an **adapter** that orchestrates the interaction between the command (inbound request) and the repository port (outbound abstraction). It has different concerns than the command.

### File 4: `src/application/commands/__init__.py`

```python
"""Commands – CQRS commands and handlers for the application layer."""

from application.commands.create_project_command import CreateProjectCommand
from application.commands.create_project_command_handler import (
    CreateProjectCommandHandler,
)

__all__ = [
    "CreateProjectCommand",
    "CreateProjectCommandHandler",
]
```

**Why this helps:** The `__init__.py` file re-exports the command and handler, making it convenient for consumers to import both from the same package while keeping them in separate files. The `ProjectRepository` port is not re-exported here; consumers import it directly from `application.ports` to make the dependency direction clear.

---

## Usage Example

A consumer can import and use both together:

```python
from application.commands import CreateProjectCommand, CreateProjectCommandHandler

# In the composition root (src/bootstrap.py):
from infrastructure.adapters.filesystem_project_adapter import FilesystemProjectAdapter

repository = FilesystemProjectAdapter()
handler = CreateProjectCommandHandler(repository)

# In a CLI or API handler:
command = CreateProjectCommand(
    title="My Project",
    description="A new project",
    owner_id="user-123",
)
project_id = handler.handle(command)
print(f"Created project: {project_id}")
```

The consumer sees both classes but doesn't need to know or care that they're in separate files.

---

## Architectural Benefits

| Benefit | How H-10 Achieves It |
|---------|---------------------|
| Import clarity | Each import statement maps to exactly one class |
| Dependency visibility | Handler depends on command; separate files make this explicit in the file system |
| Testability | Command can be tested independently; handler can be tested with a mock repository |
| Reusability | Command can be used by multiple handlers; handler can be tested without the command's implementation details |
| Discoverability | grep/IDE searches find the exact file without ambiguity |
| Hexagonal compliance | Command (port) and handler (adapter) are separated as the architecture requires |

---

## Verification: H-10 Compliance

Each file contains exactly one public class or protocol:

| File | Public Item | Status |
|------|-------------|--------|
| `create_project_command.py` | `CreateProjectCommand` (class) | ✓ One class |
| `project_repository.py` | `ProjectRepository` (protocol) | ✓ One protocol |
| `create_project_command_handler.py` | `CreateProjectCommandHandler` (class) | ✓ One class |
| `__init__.py` | (Re-exports only) | ✓ Zero public classes/protocols (re-export file) |

This implementation passes AST checks and fully complies with H-10: exactly one public class or protocol per file.

---

## Recommendation to the Developer

The developer's suggestion comes from valuable experience with MediatR, which is a solid CQRS pattern library. However:

1. **Framework constraints matter:** The Jerry Framework enforces H-10 at CI. Attempting to violate it will result in a failed merge check, not architectural flexibility.

2. **Different language, different patterns:** MediatR's reflection-based discovery is idiomatic C#. Jerry Framework's explicit imports are idiomatic Python. Both are correct within their contexts.

3. **Convenience without violation:** The `__init__.py` pattern provides MediatR-like convenience at the import level (import both from one package) while respecting the architectural separation at the file level.

**Conclusion:** Use the three-file approach above. It satisfies H-10, aligns with hexagonal architecture, and still provides import convenience.

---

## References

- **H-10:** `.context/rules/architecture-standards.md` (HARD rule, cannot override)
- **CQRS File Naming:** `.context/rules/architecture-standards.md` (section "CQRS File Naming")
- **Hexagonal Architecture:** `.context/rules/architecture-standards.md` (section "Directory Structure")
- **Project constraint:** CLAUDE.md constraint H-10: "Each Python file SHALL contain exactly ONE public class or protocol."
