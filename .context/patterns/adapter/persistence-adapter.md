# PAT-ADP-002: Persistence Adapter Pattern

> **Status**: MANDATORY
> **Category**: Adapter Pattern
> **Location**: `src/infrastructure/adapters/persistence/`

---

## Overview

Persistence Adapters are secondary adapters that implement repository ports for specific storage technologies. They translate between domain objects and storage formats.

---

## Industry Prior Art

| Source | Key Insight |
|--------|-------------|
| **Alistair Cockburn** | "Secondary adapters are driven by the application" |
| **Martin Fowler** | "Data Mapper translates between objects and data" |
| **Eric Evans** | "Repository implementation is an infrastructure concern" |

---

## Jerry Implementation

### Filesystem Adapter

```python
# File: src/infrastructure/adapters/persistence/filesystem_project_adapter.py
from __future__ import annotations

import json
from pathlib import Path
from typing import TYPE_CHECKING, Sequence

from src.session_management.domain.entities.project_info import ProjectInfo
from src.session_management.domain.value_objects.project_id import ProjectId

if TYPE_CHECKING:
    from src.session_management.domain.ports.project_repository import (
        IProjectRepository,
    )


class FilesystemProjectAdapter:
    """Filesystem implementation of project repository.

    Secondary adapter that persists projects as directory structures.
    Each project is a directory with configuration files.

    Storage Format:
        projects/
        └── PROJ-001-example/
            ├── PLAN.md
            ├── WORKTRACKER.md
            └── .jerry/
                └── config.json

    Design Notes:
    - Implements IProjectRepository port
    - Translates domain objects to filesystem structure
    - Uses JSON for structured data
    """

    PROJECTS_DIR = "projects"
    CONFIG_FILE = ".jerry/config.json"

    def __init__(self, base_path: Path | str | None = None) -> None:
        """Initialize with optional base path.

        Args:
            base_path: Base directory for projects (default: cwd)
        """
        self._base = Path(base_path) if base_path else Path.cwd()

    def get(self, project_id: ProjectId) -> ProjectInfo | None:
        """Load project from filesystem.

        Args:
            project_id: Project identifier

        Returns:
            ProjectInfo or None if not found
        """
        project_path = self._project_path(project_id)

        if not project_path.exists():
            return None

        config = self._load_config(project_path)

        return ProjectInfo(
            id=project_id.value,
            path=str(project_path),
            status=config.get("status", "ACTIVE"),
            description=config.get("description", ""),
        )

    def save(self, project: ProjectInfo) -> None:
        """Persist project to filesystem.

        Creates directory structure and config file.

        Args:
            project: Project to persist
        """
        project_path = self._project_path(ProjectId(project.id))

        # Create directory structure
        project_path.mkdir(parents=True, exist_ok=True)
        (project_path / ".jerry").mkdir(exist_ok=True)
        (project_path / ".jerry/data/items").mkdir(parents=True, exist_ok=True)

        # Create required files
        self._create_if_missing(project_path / "PLAN.md", self._plan_template())
        self._create_if_missing(
            project_path / "WORKTRACKER.md",
            self._worktracker_template(),
        )

        # Save config
        config = {
            "id": project.id,
            "status": project.status,
            "description": project.description,
        }
        self._save_config(project_path, config)

    def delete(self, project_id: ProjectId) -> bool:
        """Delete project from filesystem.

        Note: This is a soft delete - archives the directory.

        Args:
            project_id: Project to delete

        Returns:
            True if deleted, False if not found
        """
        project_path = self._project_path(project_id)

        if not project_path.exists():
            return False

        # Soft delete: rename to .archived-{name}
        archived_path = project_path.parent / f".archived-{project_path.name}"
        project_path.rename(archived_path)
        return True

    def exists(self, project_id: ProjectId) -> bool:
        """Check if project directory exists."""
        return self._project_path(project_id).exists()

    def scan_projects(self) -> Sequence[ProjectInfo]:
        """Scan for all projects in base directory.

        Returns:
            List of discovered projects
        """
        projects_dir = self._base / self.PROJECTS_DIR
        if not projects_dir.exists():
            return []

        projects = []
        for path in projects_dir.iterdir():
            if path.is_dir() and not path.name.startswith("."):
                project_id = ProjectId(path.name)
                project = self.get(project_id)
                if project:
                    projects.append(project)

        return projects

    # =========================================================================
    # Internal Methods
    # =========================================================================

    def _project_path(self, project_id: ProjectId) -> Path:
        """Get filesystem path for project."""
        return self._base / self.PROJECTS_DIR / project_id.value

    def _load_config(self, project_path: Path) -> dict:
        """Load project configuration."""
        config_path = project_path / self.CONFIG_FILE

        if not config_path.exists():
            return {}

        return json.loads(config_path.read_text())

    def _save_config(self, project_path: Path, config: dict) -> None:
        """Save project configuration."""
        config_path = project_path / self.CONFIG_FILE
        config_path.write_text(json.dumps(config, indent=2))

    def _create_if_missing(self, path: Path, content: str) -> None:
        """Create file with content if it doesn't exist."""
        if not path.exists():
            path.write_text(content)

    def _plan_template(self) -> str:
        """Generate PLAN.md template."""
        return """# Project Plan

## Overview

[Describe the project goals and scope]

## Phases

### Phase 1: [Name]

[Phase description]

## Success Criteria

- [ ] Criterion 1
- [ ] Criterion 2
"""

    def _worktracker_template(self) -> str:
        """Generate WORKTRACKER.md template."""
        return """# Work Tracker

## Current Sprint

| ID | Task | Status | Priority |
|----|------|--------|----------|
|    |      |        |          |

## Backlog

| ID | Task | Priority |
|----|------|----------|
|    |      |          |
"""
```

---

### In-Memory Adapter (Testing)

```python
# File: src/infrastructure/adapters/persistence/in_memory_repository.py
from __future__ import annotations

from typing import Generic, TypeVar

from src.shared_kernel.exceptions import AggregateNotFoundError

TAggregate = TypeVar("TAggregate")
TId = TypeVar("TId")


class InMemoryRepository(Generic[TAggregate, TId]):
    """In-memory repository for testing.

    Generic implementation that stores aggregates in a dictionary.
    Useful for unit tests that don't need persistence.
    """

    def __init__(self) -> None:
        self._storage: dict[str, TAggregate] = {}

    def get(self, id: TId) -> TAggregate | None:
        """Get aggregate by ID."""
        key = self._key(id)
        return self._storage.get(key)

    def get_or_raise(self, id: TId) -> TAggregate:
        """Get aggregate or raise if not found."""
        aggregate = self.get(id)
        if aggregate is None:
            raise AggregateNotFoundError(
                entity_type=self._aggregate_type(),
                entity_id=str(id),
            )
        return aggregate

    def save(self, aggregate: TAggregate) -> None:
        """Save aggregate to memory."""
        key = self._key(self._get_id(aggregate))
        self._storage[key] = aggregate

    def delete(self, id: TId) -> bool:
        """Delete aggregate from memory."""
        key = self._key(id)
        if key in self._storage:
            del self._storage[key]
            return True
        return False

    def exists(self, id: TId) -> bool:
        """Check if aggregate exists."""
        return self._key(id) in self._storage

    def all(self) -> list[TAggregate]:
        """Get all stored aggregates."""
        return list(self._storage.values())

    def clear(self) -> None:
        """Clear all stored aggregates."""
        self._storage.clear()

    def _key(self, id: TId) -> str:
        """Convert ID to storage key."""
        if hasattr(id, 'value'):
            return str(id.value)
        return str(id)

    def _get_id(self, aggregate: TAggregate) -> TId:
        """Extract ID from aggregate."""
        return aggregate.id

    def _aggregate_type(self) -> str:
        """Get aggregate type name."""
        return "Aggregate"
```

---

### JSON File Repository

```python
# File: src/infrastructure/adapters/persistence/json_file_repository.py
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Callable, TypeVar

TAggregate = TypeVar("TAggregate")
TId = TypeVar("TId")


class JsonFileRepository:
    """JSON file-based repository for development.

    Stores each aggregate as a separate JSON file.
    Useful for development and debugging.

    Storage Format:
        .jerry/data/{type}/{id}.json
    """

    def __init__(
        self,
        base_path: Path,
        aggregate_type: str,
        serializer: Callable[[TAggregate], dict[str, Any]],
        deserializer: Callable[[dict[str, Any]], TAggregate],
    ) -> None:
        """Initialize with serialization functions.

        Args:
            base_path: Base directory for storage
            aggregate_type: Type name for directory
            serializer: Function to convert aggregate to dict
            deserializer: Function to convert dict to aggregate
        """
        self._base = base_path / ".jerry/data" / aggregate_type
        self._serialize = serializer
        self._deserialize = deserializer

    def get(self, id: TId) -> TAggregate | None:
        """Load aggregate from JSON file."""
        file_path = self._file_path(id)

        if not file_path.exists():
            return None

        data = json.loads(file_path.read_text())
        return self._deserialize(data)

    def save(self, aggregate: TAggregate) -> None:
        """Save aggregate to JSON file."""
        self._base.mkdir(parents=True, exist_ok=True)

        file_path = self._file_path(aggregate.id)
        data = self._serialize(aggregate)
        file_path.write_text(json.dumps(data, indent=2, default=str))

    def delete(self, id: TId) -> bool:
        """Delete JSON file."""
        file_path = self._file_path(id)

        if file_path.exists():
            file_path.unlink()
            return True
        return False

    def exists(self, id: TId) -> bool:
        """Check if JSON file exists."""
        return self._file_path(id).exists()

    def _file_path(self, id: TId) -> Path:
        """Get file path for aggregate."""
        id_str = id.value if hasattr(id, 'value') else str(id)
        return self._base / f"{id_str}.json"
```

---

## Testing Pattern

```python
def test_filesystem_adapter_saves_and_loads():
    """Adapter persists project to filesystem."""
    with tempfile.TemporaryDirectory() as tmpdir:
        adapter = FilesystemProjectAdapter(base_path=tmpdir)

        project = ProjectInfo(
            id="PROJ-001-test",
            path="",
            status="ACTIVE",
            description="Test project",
        )

        adapter.save(project)
        loaded = adapter.get(ProjectId("PROJ-001-test"))

        assert loaded is not None
        assert loaded.id == "PROJ-001-test"
        assert loaded.status == "ACTIVE"


def test_in_memory_adapter_provides_isolation():
    """In-memory adapter isolates tests."""
    repo = InMemoryRepository()

    work_item = WorkItem.create(id="WORK-001", title="Test")
    repo.save(work_item)

    loaded = repo.get(WorkItemId("WORK-001"))
    assert loaded.title == "Test"

    # Clear for next test
    repo.clear()
    assert repo.get(WorkItemId("WORK-001")) is None


def test_adapter_implements_port():
    """Adapter satisfies port contract."""
    adapter = FilesystemProjectAdapter()

    # Protocol check (if using runtime_checkable)
    assert isinstance(adapter, IProjectRepository)
```

---

## Adapter Selection

| Environment | Repository | Event Store |
|-------------|------------|-------------|
| Unit Tests | InMemoryRepository | InMemoryEventStore |
| Development | JsonFileRepository | JsonFileEventStore |
| Production | DatabaseRepository | EventStoreDB |

---

## Jerry-Specific Decisions

> **Jerry Decision**: Projects stored as directory structures with JSON config.

> **Jerry Decision**: In-memory adapters for unit tests, file-based for development.

> **Jerry Decision**: All adapters implement the same port interface for interchangeability.

---

## References

- **Martin Fowler**: [Data Mapper](https://martinfowler.com/eaaCatalog/dataMapper.html)
- **Design Canon**: Section 7.2 - Persistence Adapters
- **Related Patterns**: PAT-REPO-001 (Generic Repository), PAT-ARCH-002 (Ports and Adapters)
