# ADR-PROJ004-002: JerryProject Aggregate

> **Status:** ACCEPTED
> **Date:** 2026-01-12
> **Deciders:** Claude (ps-architect)
> **Work Item:** WI-008e

---

## Context

JerryProject represents a discrete unit of work within the Jerry framework. Each project has:
- Its own PLAN.md and WORKTRACKER.md
- Its own configuration (projects/PROJ-*/config.toml)
- Its own work items and event store

### Research Inputs
- PROJ-004-e-005: Existing ProjectId value object pattern
- PROJ-004-e-006: Parent-child aggregate relationships
- Existing ProjectInfo entity (to be extended)

---

## Decision

### L0: Executive Summary

**JerryProject is a child aggregate** that extends the existing ProjectInfo pattern. It holds parent reference to JerryFramework and provides path accessors for project artifacts.

### L1: Technical Design

#### ProjectId Value Object (Existing - Enhanced)

```python
# src/session_management/domain/value_objects/project_id.py (existing)
# Already implements PROJ-NNN-slug validation
# Extends VertexId from shared_kernel

@dataclass(frozen=True)
class ProjectId(VertexId):
    """Format: PROJ-{nnn}-{slug} where nnn is 001-999."""

    @property
    def number(self) -> int: ...

    @property
    def slug(self) -> str: ...

    @classmethod
    def create(cls, number: int, slug: str) -> ProjectId: ...

    @classmethod
    def parse(cls, value: str) -> ProjectId: ...
```

#### JerryProject Aggregate

```python
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .jerry_framework import JerryFramework

from src.session_management.domain.value_objects import ProjectId
from src.shared_kernel.exceptions import ValidationError


@dataclass(frozen=True)
class ProjectConfig:
    """Project-level configuration snapshot (Value Object).

    Configuration values specific to this project.
    Falls back to framework config for missing keys.
    """
    values: dict[str, Any]
    source_path: Path | None = None

    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value."""
        return self.values.get(key, default)

    def get_string(self, key: str, default: str = "") -> str:
        value = self.values.get(key, default)
        return str(value) if value is not None else default

    def get_bool(self, key: str, default: bool = False) -> bool:
        value = self.values.get(key, default)
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            return value.lower() in ("true", "1", "yes")
        return default


class JerryProject:
    """Project aggregate within the Jerry framework.

    Represents a discrete unit of work with its own configuration,
    work items, and artifacts.

    Attributes:
        project_id: Unique identifier (PROJ-NNN-slug format)
        path: Filesystem path to the project directory
        config: Project-level configuration
        framework: Parent framework reference
    """

    def __init__(
        self,
        project_id: ProjectId,
        path: Path,
        framework: JerryFramework,
    ) -> None:
        """Initialize the project.

        Args:
            project_id: The project identifier
            path: Path to the project directory
            framework: Parent framework reference

        Raises:
            ValidationError: If path doesn't exist or is invalid
        """
        if not path.exists():
            raise ValidationError(
                field="path",
                message=f"Project directory does not exist: {path}",
            )

        self._project_id = project_id
        self._path = path.resolve()
        self._framework = framework
        self._config = self._load_config()

    @property
    def project_id(self) -> ProjectId:
        """The unique project identifier."""
        return self._project_id

    @property
    def path(self) -> Path:
        """Filesystem path to the project directory."""
        return self._path

    @property
    def config(self) -> ProjectConfig:
        """Project-level configuration."""
        return self._config

    @property
    def framework(self) -> JerryFramework:
        """Parent framework reference."""
        return self._framework

    @property
    def name(self) -> str:
        """Human-readable project name (from ID slug)."""
        return self._project_id.slug.replace("-", " ").title()

    # =========================================================================
    # Path Accessors
    # =========================================================================

    def get_worktracker_path(self) -> Path:
        """Path to WORKTRACKER.md."""
        return self._path / "WORKTRACKER.md"

    def get_plan_path(self) -> Path:
        """Path to PLAN.md."""
        return self._path / "PLAN.md"

    def get_jerry_path(self) -> Path:
        """Path to .jerry/ directory within project."""
        return self._path / ".jerry"

    def get_data_path(self) -> Path:
        """Path to .jerry/data/ for operational state."""
        return self.get_jerry_path() / "data"

    def get_work_items_path(self) -> Path:
        """Path to work items event store."""
        return self.get_data_path() / "items"

    def get_events_path(self) -> Path:
        """Path to event store directory."""
        return self.get_data_path() / "events"

    def get_config_path(self) -> Path:
        """Path to project config.toml."""
        return self._path / "config.toml"

    def get_work_path(self) -> Path:
        """Path to work/ directory for work item files."""
        return self._path / "work"

    def get_research_path(self) -> Path:
        """Path to research/ directory."""
        return self._path / "research"

    def get_decisions_path(self) -> Path:
        """Path to decisions/ directory for ADRs."""
        return self._path / "decisions"

    def get_analysis_path(self) -> Path:
        """Path to analysis/ directory."""
        return self._path / "analysis"

    def get_synthesis_path(self) -> Path:
        """Path to synthesis/ directory."""
        return self._path / "synthesis"

    # =========================================================================
    # Configuration Access
    # =========================================================================

    def get_setting(self, key: str, default: Any = None) -> Any:
        """Get setting with project -> framework fallback.

        Args:
            key: The configuration key (dot-notation supported)
            default: Default value if not found

        Returns:
            Configuration value from project or framework config
        """
        # Try project config first
        value = self._config.get(key)
        if value is not None:
            return value

        # Fall back to framework config
        return self._framework.config.get(key, default)

    def get_skill_config(self, skill_name: str) -> dict[str, Any]:
        """Get skill-specific configuration for this project.

        Args:
            skill_name: The skill name

        Returns:
            Skill configuration dictionary
        """
        return self._config.get(f"skills.{skill_name}", {})

    # =========================================================================
    # Validation
    # =========================================================================

    def is_complete(self) -> bool:
        """Check if project has all required files."""
        return (
            self.get_plan_path().exists() and
            self.get_worktracker_path().exists()
        )

    def get_warnings(self) -> list[str]:
        """Get list of warning messages for incomplete configuration."""
        warnings = []
        if not self.get_plan_path().exists():
            warnings.append("Missing PLAN.md")
        if not self.get_worktracker_path().exists():
            warnings.append("Missing WORKTRACKER.md")
        if not self.get_data_path().exists():
            warnings.append("Missing .jerry/data/ directory")
        return warnings

    # =========================================================================
    # Private Methods
    # =========================================================================

    def _load_config(self) -> ProjectConfig:
        """Load project configuration from config.toml."""
        config_path = self.get_config_path()
        if not config_path.exists():
            return ProjectConfig(values={}, source_path=None)

        # Delegate to infrastructure adapter
        return ProjectConfig(values={}, source_path=config_path)

    # =========================================================================
    # String Representation
    # =========================================================================

    def __str__(self) -> str:
        """Human-readable representation."""
        status = "complete" if self.is_complete() else "incomplete"
        return f"{self._project_id} [{status}]"

    def __repr__(self) -> str:
        """Detailed representation."""
        return (
            f"JerryProject("
            f"project_id={self._project_id!r}, "
            f"path={self._path}, "
            f"complete={self.is_complete()})"
        )
```

### L2: Strategic Implications

#### Design Rationale

| Decision | Rationale |
|----------|-----------|
| Holds framework reference | Enables navigation and config fallback |
| Separate ProjectConfig VO | Immutable configuration snapshot |
| Path accessor methods | Encapsulates project directory structure |
| get_setting() with fallback | Implements project -> framework precedence |

#### Invariants

1. `project_id` must be valid (PROJ-NNN-slug format)
2. `path` must exist and be a directory
3. Project ID string matches directory name
4. Config fallback always to framework if not found

#### Directory Structure

```
projects/PROJ-NNN-slug/
├── PLAN.md                    # Required
├── WORKTRACKER.md             # Required
├── config.toml                # Optional (project config)
├── .jerry/
│   └── data/
│       ├── items/             # Work item state
│       └── events/            # Event streams
├── work/                      # Work item files
├── research/                  # Research artifacts
├── decisions/                 # ADRs
├── analysis/                  # Analysis artifacts
└── synthesis/                 # Synthesis artifacts
```

---

## Consequences

### Positive
- Clear path accessors for all project artifacts
- Configuration fallback to framework
- Validation for completeness
- Extends existing ProjectId pattern

### Negative
- Holds parent reference (coupling)
- Must ensure parent reference is valid

### Neutral
- Lazy config loading (not at init)
- Path methods don't check existence

---

## Related

- **WI-008d**: JerryFramework (parent aggregate)
- **WI-008g**: JerrySession (uses project)
- **Existing**: ProjectId value object
- **Existing**: ProjectInfo entity
