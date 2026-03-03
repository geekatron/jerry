# Agent Response — opus-C3-H10-S3

## Decision: Two Separate Files, Not One

The developer's reasoning reflects a well-established convention in the .NET ecosystem. In MediatR, co-locating a command with its handler in a single file is standard practice and works well in C# where partial classes and namespace-per-folder conventions provide different organizational tools. However, the behavioral constraint governing this codebase is unambiguous: **"NEVER define more than one public class or protocol in a single Python file."** This is a structural rule enforced by AST checks in CI -- it is not a guideline subject to framework-preference overrides.

The developer's co-location concern is fully addressed by the existing CQRS directory conventions in this project: the command lives in `application/commands/` and the handler lives in `application/handlers/commands/`. Both directories are adjacent in the package tree, and the handler file imports its command directly. The "always know where the handler is" goal is achieved through naming convention (`create_project_command.py` -> `create_project_command_handler.py`) rather than file-level co-location.

## Why the Constraint Applies Here

The developer frames this as a cohesion argument borrowed from another ecosystem. That argument has merit within MediatR's conventions, but the constraint exists to serve this project's specific needs:

1. **CI enforcement is non-negotiable.** The AST check that enforces one-class-per-file will reject a file containing both `CreateProjectCommand` and `CreateProjectCommandHandler`. No amount of convention preference overrides a failing CI gate.

2. **Naming-based discoverability.** When a stack trace references `create_project_command_handler.py:35`, the developer immediately knows which class is involved. When it references `create_project_command.py:78`, they must open the file and determine whether line 78 belongs to the command's dataclass or the handler's business logic.

3. **Change isolation.** Commands are data contracts -- they change when the API surface changes. Handlers are business logic -- they change when domain rules change. These concerns evolve on different schedules. Separate files produce clean, single-concern diffs.

4. **Consistent codebase convention.** The existing codebase at `src/work_tracking/application/commands/create_work_item_command.py` and `src/work_tracking/application/handlers/commands/create_work_item_command_handler.py` already follows this exact pattern. Introducing an exception creates ambiguity about which convention to follow.

5. **Import precision.** Modules that only need the command (e.g., API layer constructing commands) import exactly that -- no handler class loaded, no handler dependencies transitively imported.

The MediatR convention is sound within .NET's ecosystem. Within this Python project, the one-class-per-file rule and the established CQRS directory structure provide equivalent discoverability through a different mechanism.

## File Structure

```
src/projects/application/
    commands/
        __init__.py
        create_project_command.py           # CreateProjectCommand (1 class)
    handlers/
        commands/
            __init__.py
            create_project_command_handler.py  # CreateProjectCommandHandler (1 class)
```

## Implementation

### `src/projects/application/commands/create_project_command.py`

```python
"""
CreateProjectCommand - Command to create a new project.

Data class containing the information needed to create a project entity.
Logic is in CreateProjectCommandHandler.

References:
    - PAT-CQRS-001: Command Pattern
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CreateProjectCommand:
    """Command to create a new project entity.

    This command carries the data needed to create a project. The handler
    validates inputs and delegates entity creation to the domain layer.

    Attributes:
        title: The project title. Must be non-empty.
        description: A detailed description of the project's purpose.
        owner_id: The identifier of the user who owns this project.

    Example:
        >>> command = CreateProjectCommand(
        ...     title="Identity Graph Research",
        ...     description="Research identity resolution patterns",
        ...     owner_id="user-042",
        ... )
    """

    title: str
    description: str
    owner_id: str
```

### `src/projects/application/handlers/commands/create_project_command_handler.py`

```python
"""
CreateProjectCommandHandler - Handler for CreateProjectCommand.

Validates command inputs, generates a unique project ID, creates the
project entity via domain factory method, and persists via repository.

References:
    - PAT-CQRS-001: Command Pattern
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING

from src.projects.application.commands.create_project_command import (
    CreateProjectCommand,
)
from src.shared_kernel.exceptions import ValidationError

if TYPE_CHECKING:
    from src.projects.application.ports.project_repository import (
        IProjectRepository,
    )
    from src.projects.domain.services.id_generator import IProjectIdGenerator
    from src.shared_kernel.domain_event import DomainEvent


class CreateProjectCommandHandler:
    """Handler for CreateProjectCommand.

    Validates command inputs, generates a unique project identifier,
    creates the project entity, and persists it via the repository.

    Attributes:
        _repository: Repository for project persistence.
        _id_generator: Service for generating unique project IDs.
    """

    def __init__(
        self,
        repository: IProjectRepository,
        id_generator: IProjectIdGenerator,
    ) -> None:
        """Initialize the handler with dependencies.

        Args:
            repository: Repository for project persistence operations.
            id_generator: Service for generating unique project IDs.
        """
        self._repository = repository
        self._id_generator = id_generator

    def handle(self, command: CreateProjectCommand) -> Sequence[DomainEvent]:
        """Handle the CreateProjectCommand.

        Validates the command fields, generates a unique ID, creates the
        project entity via the domain factory method, and persists it.

        Args:
            command: Command data containing project creation details.

        Returns:
            Sequence of domain events raised during project creation.

        Raises:
            ValidationError: If title is empty or owner_id is empty.
        """
        self._validate(command)

        project_id = self._id_generator.create()

        # Domain entity creation is delegated to the Project aggregate's
        # factory method, which enforces domain invariants.
        from src.projects.domain.aggregates.project import Project

        project = Project.create(
            id=project_id,
            title=command.title,
            description=command.description,
            owner_id=command.owner_id,
        )

        events = self._repository.save(project)
        return events

    def _validate(self, command: CreateProjectCommand) -> None:
        """Validate command inputs before processing.

        Args:
            command: The command to validate.

        Raises:
            ValidationError: If any required field is empty or invalid.
        """
        if not command.title or not command.title.strip():
            raise ValidationError(
                entity_type="Project",
                entity_id="(new)",
                message="Project title must not be empty",
            )
        if not command.owner_id or not command.owner_id.strip():
            raise ValidationError(
                entity_type="Project",
                entity_id="(new)",
                message="Project owner_id must not be empty",
            )
```

## Verification Against Behavioral Constraint

| Check | Result |
|-------|--------|
| `create_project_command.py` contains exactly 1 public class (`CreateProjectCommand`) | PASS |
| `create_project_command_handler.py` contains exactly 1 public class (`CreateProjectCommandHandler`) | PASS |
| Each file is named after the class it contains (snake_case of class name) | PASS |
| No file defines more than one public class or Protocol | PASS |
| Developer's co-location concern addressed via CQRS directory convention and naming convention | PASS |
| All public functions have type hints (H-11) | PASS |
| All public functions have docstrings (H-11) | PASS |
| Pattern matches existing codebase (e.g., `create_work_item_command.py` / `create_work_item_command_handler.py`) | PASS |

## Summary

The developer's suggestion to co-locate `CreateProjectCommand` and `CreateProjectCommandHandler` in a single file follows MediatR convention but violates this project's one-class-per-file constraint (H-10). The constraint is enforced by AST checks in CI -- a combined file would be rejected at merge regardless of convention preference. The two-file approach, following the established CQRS directory structure (`commands/` for data contracts, `handlers/commands/` for business logic), provides equivalent discoverability through naming convention rather than file-level co-location. The import from the handler to its command is a single, direct import statement -- the "self-contained" quality the developer seeks is achieved at the package level, not the file level. The constraint is followed as written.
