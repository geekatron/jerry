# ADR-PROJ004-001: JerryFramework Aggregate

> **Status:** ACCEPTED
> **Date:** 2026-01-12
> **Deciders:** Claude (ps-architect)
> **Work Item:** WI-008d

---

## Context

Jerry needs a root aggregate representing the entire framework installation. This aggregate must:
- Provide discovery of projects and skills
- Hold framework-level configuration
- Serve as the entry point for navigation

### Research Inputs
- PROJ-004-e-005: Existing FilesystemProjectAdapter patterns
- PROJ-004-e-006: DDD aggregate relationship patterns
- PROJ-004-e-007: Skill discovery mechanism

---

## Decision

### L0: Executive Summary

**JerryFramework is the root aggregate** for the Jerry configuration system. It holds the `root_path` and provides lazy discovery of projects and skills.

### L1: Technical Design

#### Core Interface

```python
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .jerry_project import JerryProject
    from .jerry_skill import JerrySkill

from src.shared_kernel.exceptions import ValidationError


@dataclass(frozen=True)
class FrameworkConfig:
    """Framework-level configuration snapshot (Value Object)."""
    values: dict[str, Any]
    source_path: Path | None = None

    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value."""
        return self.values.get(key, default)

    def get_string(self, key: str, default: str = "") -> str:
        value = self.values.get(key, default)
        return str(value) if value is not None else default


class JerryFramework:
    """Root aggregate for the Jerry framework.

    Provides discovery and navigation for projects and skills.
    This is the entry point for the Jerry configuration system.

    Attributes:
        root_path: The root directory of the Jerry installation
        config: Framework-level configuration
    """

    def __init__(self, root_path: Path) -> None:
        """Initialize the framework.

        Args:
            root_path: Path to the Jerry installation root

        Raises:
            ValidationError: If root_path is not a valid Jerry installation
        """
        if not root_path.exists():
            raise ValidationError(
                field="root_path",
                message=f"Directory does not exist: {root_path}",
            )

        self._root_path = root_path.resolve()
        self._config = self._load_config()

        # Lazy-loaded collections
        self._projects: dict[ProjectId, JerryProject] | None = None
        self._skills: dict[SkillName, JerrySkill] | None = None

    @property
    def root_path(self) -> Path:
        """The root directory of the Jerry installation."""
        return self._root_path

    @property
    def config(self) -> FrameworkConfig:
        """Framework-level configuration."""
        return self._config

    @property
    def projects_path(self) -> Path:
        """Path to the projects directory."""
        return self._root_path / "projects"

    @property
    def skills_path(self) -> Path:
        """Path to the skills directory."""
        return self._root_path / "skills"

    @property
    def jerry_path(self) -> Path:
        """Path to the .jerry directory."""
        return self._root_path / ".jerry"

    # =========================================================================
    # Project Navigation
    # =========================================================================

    def list_projects(self) -> list[ProjectInfo]:
        """List all available projects.

        Returns:
            List of ProjectInfo objects, sorted by project number
        """
        if self._projects is None:
            self._projects = self._discover_projects()
        return [
            ProjectInfo(
                id=p.project_id,
                path=p.path,
                has_plan=(p.path / "PLAN.md").exists(),
                has_tracker=(p.path / "WORKTRACKER.md").exists(),
            )
            for p in self._projects.values()
        ]

    def get_project(self, project_id: ProjectId) -> JerryProject | None:
        """Get a specific project by ID.

        Args:
            project_id: The project identifier

        Returns:
            JerryProject if found, None otherwise
        """
        if self._projects is None:
            self._projects = self._discover_projects()
        return self._projects.get(project_id)

    def create_project(self, slug: str, name: str | None = None) -> JerryProject:
        """Create a new project.

        Args:
            slug: The project slug (kebab-case)
            name: Optional display name

        Returns:
            The newly created JerryProject

        Raises:
            ValidationError: If slug is invalid
        """
        # Get next project number
        if self._projects is None:
            self._projects = self._discover_projects()

        next_number = 1
        if self._projects:
            max_number = max(p.project_id.number for p in self._projects.values())
            next_number = max_number + 1

        project_id = ProjectId.create(next_number, slug)
        project_path = self.projects_path / str(project_id)

        # Create project directory structure
        project_path.mkdir(parents=True, exist_ok=False)
        (project_path / ".jerry" / "data" / "items").mkdir(parents=True)

        # Create minimal files
        (project_path / "PLAN.md").write_text(
            f"# PLAN: {name or slug}\n\n> Status: DRAFT\n"
        )
        (project_path / "WORKTRACKER.md").write_text(
            f"# WORKTRACKER: {str(project_id)}\n\n> Status: DRAFT\n"
        )

        # Add to cache
        project = JerryProject(project_id, project_path, self)
        self._projects[project_id] = project

        return project

    # =========================================================================
    # Skill Navigation
    # =========================================================================

    def list_skills(self) -> list[SkillInfo]:
        """List all available skills.

        Returns:
            List of SkillInfo objects
        """
        if self._skills is None:
            self._skills = self._discover_skills()
        return [
            SkillInfo(
                name=s.skill_name,
                version=s.version,
                description=s.description,
            )
            for s in self._skills.values()
        ]

    def get_skill(self, skill_name: SkillName) -> JerrySkill | None:
        """Get a specific skill by name.

        Args:
            skill_name: The skill identifier

        Returns:
            JerrySkill if found, None otherwise
        """
        if self._skills is None:
            self._skills = self._discover_skills()
        return self._skills.get(skill_name)

    # =========================================================================
    # Private Methods
    # =========================================================================

    def _load_config(self) -> FrameworkConfig:
        """Load framework configuration from .jerry/config.toml."""
        config_path = self.jerry_path / "config.toml"
        if not config_path.exists():
            return FrameworkConfig(values={}, source_path=None)

        # Delegate to infrastructure adapter
        # (actual TOML parsing happens in infrastructure layer)
        return FrameworkConfig(values={}, source_path=config_path)

    def _discover_projects(self) -> dict[ProjectId, JerryProject]:
        """Discover all projects in the projects directory."""
        from .jerry_project import JerryProject

        projects = {}
        if not self.projects_path.exists():
            return projects

        for project_dir in self.projects_path.iterdir():
            if not project_dir.is_dir():
                continue
            if project_dir.name.startswith("."):
                continue
            if project_dir.name.lower() == "archive":
                continue

            try:
                project_id = ProjectId.parse(project_dir.name)
                projects[project_id] = JerryProject(project_id, project_dir, self)
            except ValidationError:
                pass  # Skip invalid project directories

        return projects

    def _discover_skills(self) -> dict[SkillName, JerrySkill]:
        """Discover all skills in the skills directory."""
        from .jerry_skill import JerrySkill

        skills = {}
        if not self.skills_path.exists():
            return skills

        for skill_dir in self.skills_path.iterdir():
            if not skill_dir.is_dir():
                continue
            if not (skill_dir / "SKILL.md").exists():
                continue

            try:
                skill_name = SkillName(skill_dir.name)
                skills[skill_name] = JerrySkill(skill_name, skill_dir, self)
            except ValidationError:
                pass  # Skip invalid skill directories

        return skills


# Supporting Value Objects

@dataclass(frozen=True)
class ProjectInfo:
    """Lightweight project information (Value Object)."""
    id: ProjectId
    path: Path
    has_plan: bool = False
    has_tracker: bool = False


@dataclass(frozen=True)
class SkillInfo:
    """Lightweight skill information (Value Object)."""
    name: SkillName
    version: str
    description: str
```

### L2: Strategic Implications

#### Design Rationale

| Decision | Rationale |
|----------|-----------|
| Lazy loading | Projects/skills discovered on first access, not at init |
| Direct child references | Children hold `framework` reference for navigation |
| FrameworkConfig as VO | Configuration is immutable snapshot |
| ProjectInfo/SkillInfo VOs | Lightweight DTOs for listing without full load |

#### Invariants

1. `root_path` must exist and be a directory
2. Projects are uniquely identified by `ProjectId`
3. Skills are uniquely identified by `SkillName`
4. Framework config loads from `.jerry/config.toml`

#### Port Interfaces

```python
# Primary Port (used by interface layer)
class IJerryContext(Protocol):
    """Primary port for framework access."""

    @property
    def framework(self) -> JerryFramework: ...

    def get_project(self, project_id: ProjectId) -> JerryProject | None: ...
    def get_skill(self, skill_name: SkillName) -> JerrySkill | None: ...

# Secondary Port (used by framework)
class IConfigurationLoader(Protocol):
    """Secondary port for loading configuration files."""

    def load_toml(self, path: Path) -> dict[str, Any]: ...
```

---

## Consequences

### Positive
- Single entry point for framework access
- Lazy loading reduces startup time
- Clear navigation from framework to projects/skills
- Value objects for lightweight listing

### Negative
- Caching may become stale if files change externally
- Must handle project/skill discovery errors gracefully

### Neutral
- Projects and skills are separate aggregates (own lifecycle)
- Configuration parsing delegated to infrastructure

---

## Related

- **WI-008e**: JerryProject aggregate (child)
- **WI-008f**: JerrySkill aggregate (child)
- **WI-008g**: JerrySession (uses framework)
- **PROJ-004-e-005**: Codebase analysis (existing patterns)
