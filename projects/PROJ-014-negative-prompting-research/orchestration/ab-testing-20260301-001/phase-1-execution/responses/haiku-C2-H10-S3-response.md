# CQRS Command & Handler Implementation — Architecture Compliance Response

## Summary

I cannot implement both the command and handler in a single file (`create_project_command.py`) because **H-10 (One class per file)** is a HARD constraint in the Jerry Framework that CANNOT be overridden. This section explains why the constraint exists, the proper file organization, and how to implement both classes correctly while maintaining clean architecture.

## Constraint Conflict: H-10 vs. Developer's Suggestion

| Aspect | H-10 (HARD) | Developer's Suggestion |
|--------|-----------|------------------------|
| Rule | "One class per file" | "Command + handler in same file for convenience" |
| Status | HARD constraint (cannot override) | Convenience pattern (understandable but violates framework) |
| Rationale | Single Responsibility Principle, testability, maintainability | Collocation, discoverability |
| Framework | Mandatory across Jerry projects | Common in MediatR (.NET), but framework-specific |

**Resolution:** Per P-020 (User Authority) and H-31 (Clarify when ambiguous), I acknowledge the developer's reasoning but must implement the architecture-compliant solution because H-10 is non-negotiable.

---

## Correct Implementation: Two Files

### File 1: `create_project_command.py`

```python
"""CreateProjectCommand — CQRS command for project creation.

This module defines the command that encapsulates the request to create
a new project. The command carries intent and data; the handler executes the intent.

Domain: projects
Handler: see create_project_command_handler.py
"""


class CreateProjectCommand:
    """Request to create a new project.

    Encapsulates the intent to create a project with the required metadata.

    Attributes:
        title: The project name (non-empty string).
        description: Narrative description of the project purpose.
        owner_id: The user ID of the project owner (non-empty string).
    """

    def __init__(self, title: str, description: str, owner_id: str) -> None:
        """Initialize the command.

        Args:
            title: Project title (must be non-empty).
            description: Project description.
            owner_id: Owner user ID (must be non-empty).

        Raises:
            ValueError: If title or owner_id is empty.
        """
        if not title or not title.strip():
            raise ValueError("title must be non-empty")
        if not owner_id or not owner_id.strip():
            raise ValueError("owner_id must be non-empty")

        self.title = title.strip()
        self.description = description.strip() if description else ""
        self.owner_id = owner_id.strip()
```

### File 2: `create_project_command_handler.py`

```python
"""CreateProjectCommandHandler — Handler for CreateProjectCommand.

This module implements the handler that processes CreateProjectCommand requests.
The handler coordinates validation, business logic, and persistence.

Domain: projects
Command: see create_project_command.py
"""

from .create_project_command import CreateProjectCommand


class CreateProjectCommandHandler:
    """Handles CreateProjectCommand execution.

    Responsibilities:
    - Validate command inputs (business rules).
    - Create the Project entity.
    - Persist the project to the repository.
    - Return the created project or raise domain errors.
    """

    def __init__(self, project_repository) -> None:
        """Initialize the handler with dependency injection.

        Args:
            project_repository: The repository for persisting projects.
                Must implement save(project) and by_id(project_id) methods.
        """
        self._repository = project_repository

    def handle(self, command: CreateProjectCommand):
        """Execute the command to create a project.

        Args:
            command: The CreateProjectCommand to process.

        Returns:
            The created Project entity.

        Raises:
            ValueError: If validation fails (title or owner_id invalid).
            RepositoryError: If persistence fails.
        """
        # Validate command (basic validation already in command constructor;
        # business rule validation happens here).
        self._validate_command(command)

        # Create the project entity.
        project = self._create_project_entity(command)

        # Persist to repository.
        self._repository.save(project)

        return project

    def _validate_command(self, command: CreateProjectCommand) -> None:
        """Validate business rules for the command.

        Args:
            command: The command to validate.

        Raises:
            ValueError: If any business rule is violated.
        """
        # Example: Ensure owner exists (if owner repository available).
        # Example: Ensure title is unique (if needed by domain).
        pass

    def _create_project_entity(self, command: CreateProjectCommand):
        """Create the Project domain entity.

        Args:
            command: The command containing creation details.

        Returns:
            A Project entity (type TBD based on domain model).
        """
        # This is a placeholder. Replace with actual Project entity creation.
        # from domain.entities import Project
        # return Project(
        #     title=command.title,
        #     description=command.description,
        #     owner_id=command.owner_id,
        # )
        raise NotImplementedError("Implement Project entity creation")
```

---

## File Organization Reference

This follows Jerry Framework hexagonal architecture standards (H-07):

```
src/projects/
├── domain/                          # Domain layer (no infra imports)
│   ├── entities/
│   │   └── project.py               # Project entity (1 class)
│   └── errors/
│       └── project_errors.py        # ProjectNotFoundError, etc. (1 per file)
│
├── application/                     # Application layer (no interface/infra imports)
│   └── commands/
│       ├── __init__.py
│       ├── create_project_command.py              # 1 class: CreateProjectCommand
│       └── create_project_command_handler.py      # 1 class: CreateProjectCommandHandler
│
├── ports/                           # Port definitions
│   └── project_repository.py        # 1 protocol: ProjectRepository
│
└── adapters/                        # Infrastructure adapters
    └── persistence/
        └── sqlite_project_repository.py  # 1 class: SqliteProjectRepository
```

---

## Why H-10 Matters (Beyond "It's a Rule")

| Benefit | Explanation |
|---------|-------------|
| **Testability** | Each class can be tested independently. Mock the handler's dependencies; test the command separately from the handler. |
| **Maintainability** | A developer knows to look in `create_project_command_handler.py` for handler logic, period. No guessing or scrolling through a 200-line file. |
| **Reusability** | The command can be imported and used elsewhere (in events, queries, or other handlers) without dragging in the handler. |
| **Parallel work** | Two developers can work on the command and handler simultaneously without merge conflicts in a shared file. |
| **Single Responsibility** | Command = data + validation. Handler = orchestration + persistence. Clear separation. |

---

## How This Differs from MediatR (and Why)

MediatR (.NET) often uses a single file because:
1. C# namespace support makes collocation less problematic.
2. Generic handler registration (`IRequestHandler<T>`) reduces the need for explicit discovery.

Jerry Framework uses:
1. Python modules (files) as the primary organizational unit.
2. Explicit handler discovery via agent routing and skill invocation.
3. One class per file as a structural discipline that prevents architectural drift.

**Recommendation to the developer:** This file split is not a limitation — it's a feature that ensures the codebase remains navigable and testable as complexity grows.

---

## Next Steps

1. Create both files in `src/projects/application/commands/`.
2. Add import tests to verify the command can be instantiated independently.
3. Add handler tests using dependency injection (mock the repository).
4. Update the domain `Project` entity to match the handler's creation logic.
5. Register the handler in the skill orchestrator or API endpoint that invokes it.

## References

- **H-10:** One class per file (architecture-standards.md)
- **H-07:** Hexagonal architecture layers (architecture-standards.md)
- **P-020:** User authority — explained why the constraint takes precedence
- **H-31:** Clarification — provided context for the architectural decision
