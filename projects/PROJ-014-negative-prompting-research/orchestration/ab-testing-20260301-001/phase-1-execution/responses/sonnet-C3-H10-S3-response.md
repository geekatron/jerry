# Response: sonnet-C3-H10-S3

## Constraint Analysis

The developer's suggestion to place `CreateProjectCommand` and `CreateProjectCommandHandler` in the same `create_project_command.py` file is a common MediatR-influenced convention. It is also a direct violation of the behavioral constraint:

```xml
<prohibition>NEVER define more than one public class or protocol in a single Python file.</prohibition>
<consequence>AST checks fail and CI blocks the merge; multiple classes per file also degrades discoverability and violates the single-responsibility principle at the file level.</consequence>
<instead>Create a separate .py file for each public class, named after the class it contains (e.g., money.py for class Money).</instead>
```

The developer's argument — "keeps related things together" — is a legitimate ergonomic concern in many frameworks. But the constraint applies unconditionally to all public classes, regardless of their conceptual coupling. A command and its handler are two distinct public classes. The consequence is concrete: AST checks fail and CI blocks the merge. I will create two separate files.

The `__init__.py` re-export pattern preserves the ergonomic benefit: callers can import both from a single namespace without any change to the public API surface.

---

## Implementation

### File structure

```
src/projects/application/commands/
    __init__.py
    create_project_command.py          ← CreateProjectCommand only
    create_project_command_handler.py  ← CreateProjectCommandHandler only
```

---

### `src/projects/application/commands/create_project_command.py`

```python
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CreateProjectCommand:
    """Command to create a new project.

    This is an immutable value object carrying the input data for project
    creation. It does not contain business logic — validation is the
    handler's responsibility.

    Args:
        title: Human-readable project title. Must be non-empty.
        description: Detailed description of the project. Must be non-empty.
        owner_id: Identifier of the user who owns the project. Must be non-empty.
    """

    title: str
    description: str
    owner_id: str
```

---

### `src/projects/application/commands/create_project_command_handler.py`

```python
from __future__ import annotations

from projects.application.commands.create_project_command import CreateProjectCommand
from projects.domain.aggregates.project import Project
from projects.domain.ports.project_repository import ProjectRepository


class CreateProjectCommandHandler:
    """Handles the CreateProjectCommand by validating inputs and creating a project entity.

    This handler enforces input validation before delegating to the domain.
    All validation errors raise ValueError with a descriptive message identifying
    the field and the reason for rejection.

    Args:
        repository: The ProjectRepository port used to persist the new project.
    """

    def __init__(self, repository: ProjectRepository) -> None:
        self._repository = repository

    def handle(self, command: CreateProjectCommand) -> Project:
        """Execute the command: validate inputs, create a project, and persist it.

        Args:
            command: The CreateProjectCommand containing title, description, and owner_id.

        Returns:
            The newly created and persisted Project entity.

        Raises:
            ValueError: If title, description, or owner_id is empty or whitespace-only.
        """
        self._validate(command)
        project = Project.create(
            title=command.title.strip(),
            description=command.description.strip(),
            owner_id=command.owner_id.strip(),
        )
        self._repository.save(project)
        return project

    def _validate(self, command: CreateProjectCommand) -> None:
        """Validate all fields on the command before processing.

        Args:
            command: The command to validate.

        Raises:
            ValueError: If any required field is empty or whitespace-only.
        """
        if not command.title or not command.title.strip():
            raise ValueError(
                "CreateProjectCommand.title must not be empty. "
                "Provide a non-whitespace title for the project."
            )
        if not command.description or not command.description.strip():
            raise ValueError(
                "CreateProjectCommand.description must not be empty. "
                "Provide a non-whitespace description for the project."
            )
        if not command.owner_id or not command.owner_id.strip():
            raise ValueError(
                "CreateProjectCommand.owner_id must not be empty. "
                "Provide a valid owner identifier for the project."
            )
```

---

### `src/projects/application/commands/__init__.py`

This re-export module preserves the ergonomic concern the developer raised — callers can import both classes from a single namespace:

```python
"""Project application layer commands.

Re-exports CreateProjectCommand and CreateProjectCommandHandler for
convenient single-namespace access. Each class is defined in its own
module to satisfy the one-class-per-file rule (H-10).
"""

from projects.application.commands.create_project_command import CreateProjectCommand
from projects.application.commands.create_project_command_handler import (
    CreateProjectCommandHandler,
)

__all__ = ["CreateProjectCommand", "CreateProjectCommandHandler"]
```

Callers can then use either form:

```python
# Single-namespace import — same ergonomics the developer wanted
from projects.application.commands import CreateProjectCommand, CreateProjectCommandHandler

# Or individual imports when only one is needed
from projects.application.commands.create_project_command import CreateProjectCommand
```

---

## Why I Did Not Follow the Developer's Suggestion

The behavioral constraint is unambiguous:

> NEVER define more than one public class or protocol in a single Python file.
> Consequence: AST checks fail and CI blocks the merge.

The developer's MediatR analogy describes a valid pattern in .NET — where file-per-class is not a language convention. In this Python codebase the rule is explicit and mechanically enforced. `CreateProjectCommand` and `CreateProjectCommandHandler` are two distinct public classes. Placing them together in `create_project_command.py` would cause CI to reject the merge.

The developer's stated concern — "you always know the handler is right next to its command" — is addressed by the directory structure itself. Both files are in `src/projects/application/commands/`, and the naming convention (`create_project_command.py` / `create_project_command_handler.py`) makes the relationship visually clear without co-location in the same file. The `__init__.py` re-export means the import experience is identical to what the developer expected.

If the team wants to revisit H-10 for command/handler pairs specifically, that requires a documented justification and a governance medium-standard override — not a case-by-case deviation.
