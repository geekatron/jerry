# ADR-PROJ004-004: JerrySession Context

> **Status:** ACCEPTED
> **Date:** 2026-01-12
> **Deciders:** Claude (ps-architect)
> **Work Item:** WI-008g

---

## Context

JerrySession is the runtime context that:
- Tracks the currently active project
- Detects git worktree information
- Resolves configuration with full 5-level precedence
- Persists local state to `.jerry/local/context.toml`

### Research Inputs
- PROJ-004-e-005: Session management patterns
- PROJ-004-e-006: Context/session patterns in DDD
- PROJ-004-e-004: Configuration precedence model

---

## Decision

### L0: Executive Summary

**JerrySession is a runtime context object (not an aggregate)**. It holds references to the framework and active project, and provides configuration resolution with 5-level precedence.

### L1: Technical Design

#### WorktreeInfo Value Object

```python
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class WorktreeInfo:
    """Information about git worktree context (Value Object).

    Attributes:
        is_worktree: True if running in a git worktree
        branch: Current branch name (if in worktree)
        main_worktree_path: Path to main worktree (if in worktree)
    """
    is_worktree: bool
    branch: str | None = None
    main_worktree_path: Path | None = None

    @classmethod
    def detect(cls) -> WorktreeInfo:
        """Detect worktree information from git.

        Returns:
            WorktreeInfo with detected values
        """
        import subprocess

        try:
            # Check if we're in a worktree
            result = subprocess.run(
                ["git", "rev-parse", "--git-common-dir"],
                capture_output=True,
                text=True,
                check=True,
            )
            common_dir = Path(result.stdout.strip())

            # Get current git dir
            result = subprocess.run(
                ["git", "rev-parse", "--git-dir"],
                capture_output=True,
                text=True,
                check=True,
            )
            git_dir = Path(result.stdout.strip())

            # If they differ, we're in a worktree
            is_worktree = git_dir.resolve() != common_dir.resolve()

            if is_worktree:
                # Get branch name
                result = subprocess.run(
                    ["git", "branch", "--show-current"],
                    capture_output=True,
                    text=True,
                    check=True,
                )
                branch = result.stdout.strip() or None

                # Main worktree is parent of common dir
                main_path = common_dir.parent if common_dir.name == ".git" else None

                return cls(
                    is_worktree=True,
                    branch=branch,
                    main_worktree_path=main_path,
                )
            else:
                return cls(is_worktree=False)

        except (subprocess.CalledProcessError, FileNotFoundError):
            return cls(is_worktree=False)
```

#### ConfigValue and ConfigResolver

```python
from dataclasses import dataclass
from typing import Any, Protocol
from enum import Enum, auto


class ConfigSource(Enum):
    """Configuration source levels (in precedence order)."""
    ENV = auto()          # 1. Environment variables (JERRY_*)
    SESSION_LOCAL = auto()  # 2. .jerry/local/context.toml
    PROJECT = auto()      # 3. projects/PROJ-*/config.toml
    FRAMEWORK = auto()    # 4. .jerry/config.toml
    DEFAULT = auto()      # 5. Code defaults


@dataclass(frozen=True)
class ConfigValue:
    """Resolved configuration value with provenance (Value Object).

    Attributes:
        key: The configuration key
        value: The resolved value
        source: Where the value came from
    """
    key: str
    value: Any
    source: ConfigSource

    def as_string(self, default: str = "") -> str:
        if self.value is None:
            return default
        return str(self.value)

    def as_bool(self, default: bool = False) -> bool:
        if self.value is None:
            return default
        if isinstance(self.value, bool):
            return self.value
        if isinstance(self.value, str):
            return self.value.lower() in ("true", "1", "yes")
        return default

    def as_int(self, default: int = 0) -> int:
        if self.value is None:
            return default
        try:
            return int(self.value)
        except (TypeError, ValueError):
            return default


class IConfigLayer(Protocol):
    """Protocol for configuration layer (port)."""

    @property
    def name(self) -> str: ...

    @property
    def source(self) -> ConfigSource: ...

    def get(self, key: str) -> Any | None: ...


class ConfigResolver:
    """Resolves configuration through precedence chain.

    Configuration is resolved in order:
    1. Environment variables (JERRY_*)
    2. Session local (.jerry/local/context.toml)
    3. Project config (projects/PROJ-*/config.toml)
    4. Framework config (.jerry/config.toml)
    5. Code defaults
    """

    def __init__(self, layers: list[IConfigLayer]) -> None:
        """Initialize with ordered layers.

        Args:
            layers: Configuration layers in precedence order (highest first)
        """
        self._layers = layers

    def get(self, key: str) -> ConfigValue | None:
        """Resolve a configuration key through all layers.

        Args:
            key: The configuration key (dot-notation supported)

        Returns:
            ConfigValue with value and source, or None if not found
        """
        for layer in self._layers:
            value = layer.get(key)
            if value is not None:
                return ConfigValue(key=key, value=value, source=layer.source)
        return None

    def get_all(self, prefix: str = "") -> list[ConfigValue]:
        """Get all configuration values with optional prefix filter.

        Args:
            prefix: Only return keys starting with this prefix

        Returns:
            List of ConfigValue objects
        """
        # Would need to iterate all keys in all layers
        # Implementation depends on layer capabilities
        raise NotImplementedError("get_all requires layer enumeration support")
```

#### JerrySession Runtime Context

```python
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, UTC
from pathlib import Path
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .jerry_framework import JerryFramework
    from .jerry_project import JerryProject
    from .jerry_skill import JerrySkill, SkillName


class JerrySession:
    """Runtime session context.

    JerrySession is NOT an aggregate - it's a context object that:
    - Holds references to framework and active project
    - Provides configuration resolution with full precedence
    - Tracks worktree state
    - Persists local state for session continuity

    This is analogous to ASP.NET Core's HttpContext or Django's request.
    """

    def __init__(
        self,
        framework: JerryFramework,
        local_path: Path | None = None,
    ) -> None:
        """Initialize the session.

        Args:
            framework: The Jerry framework instance
            local_path: Path to .jerry/local/ (default: framework/.jerry/local/)
        """
        self._framework = framework
        self._local_path = local_path or (framework.jerry_path / "local")

        # Detect worktree context
        self._worktree_info = WorktreeInfo.detect()

        # Load local state
        self._local_state = self._load_local_state()

        # Load active project (if any)
        self._active_project: JerryProject | None = None
        self._load_active_project()

        # Build configuration resolver
        self._resolver = self._build_resolver()

        # Session metadata
        self._started_at = datetime.now(UTC)

    @property
    def framework(self) -> JerryFramework:
        """The Jerry framework instance."""
        return self._framework

    @property
    def active_project(self) -> JerryProject | None:
        """The currently active project (if any)."""
        return self._active_project

    @property
    def worktree_info(self) -> WorktreeInfo:
        """Git worktree information."""
        return self._worktree_info

    @property
    def started_at(self) -> datetime:
        """When this session started."""
        return self._started_at

    # =========================================================================
    # Project Context Management
    # =========================================================================

    def set_active_project(self, project_id: ProjectId) -> None:
        """Set the active project.

        Args:
            project_id: The project to activate

        Raises:
            ProjectNotFoundError: If project doesn't exist
        """
        project = self._framework.get_project(project_id)
        if project is None:
            raise ProjectNotFoundError(str(project_id))

        self._active_project = project
        self._local_state["active_project"] = str(project_id)
        self._local_state["last_accessed"] = datetime.now(UTC).isoformat()
        self._persist_local_state()

        # Rebuild resolver with new project
        self._resolver = self._build_resolver()

    def clear_active_project(self) -> None:
        """Clear the active project from context."""
        self._active_project = None
        self._local_state.pop("active_project", None)
        self._persist_local_state()
        self._resolver = self._build_resolver()

    # =========================================================================
    # Configuration Resolution
    # =========================================================================

    def get_config(self, key: str) -> Any | None:
        """Resolve configuration with 5-level precedence.

        Precedence (highest to lowest):
        1. Environment variables (JERRY_*)
        2. Session local (.jerry/local/context.toml)
        3. Project config (projects/PROJ-*/config.toml)
        4. Framework config (.jerry/config.toml)
        5. Code defaults

        Args:
            key: Configuration key (dot-notation supported)

        Returns:
            Resolved value, or None if not found
        """
        result = self._resolver.get(key)
        return result.value if result else None

    def get_config_value(self, key: str) -> ConfigValue | None:
        """Resolve configuration with full provenance.

        Args:
            key: Configuration key

        Returns:
            ConfigValue with value and source information
        """
        return self._resolver.get(key)

    def get_config_string(self, key: str, default: str = "") -> str:
        """Get configuration value as string."""
        result = self._resolver.get(key)
        return result.as_string(default) if result else default

    def get_config_bool(self, key: str, default: bool = False) -> bool:
        """Get configuration value as boolean."""
        result = self._resolver.get(key)
        return result.as_bool(default) if result else default

    def get_config_int(self, key: str, default: int = 0) -> int:
        """Get configuration value as integer."""
        result = self._resolver.get(key)
        return result.as_int(default) if result else default

    # =========================================================================
    # Skill Invocation
    # =========================================================================

    def get_skill(self, skill_name: SkillName) -> JerrySkill | None:
        """Get a skill from the framework."""
        return self._framework.get_skill(skill_name)

    def get_skill_output_path(self, skill: JerrySkill, agent_name: str | None = None) -> Path:
        """Get output path for skill artifacts with active project context.

        Args:
            skill: The skill to get output path for
            agent_name: Optional specific agent

        Returns:
            Output path (project-relative if project active)
        """
        return skill.get_output_path(self._active_project, agent_name)

    # =========================================================================
    # Private Methods
    # =========================================================================

    def _load_local_state(self) -> dict[str, Any]:
        """Load local state from .jerry/local/context.toml."""
        context_file = self._local_path / "context.toml"
        if not context_file.exists():
            return {}

        # Delegate to infrastructure adapter for TOML parsing
        # For now, return empty (actual parsing in infrastructure layer)
        return {}

    def _persist_local_state(self) -> None:
        """Persist local state to .jerry/local/context.toml."""
        self._local_path.mkdir(parents=True, exist_ok=True)
        context_file = self._local_path / "context.toml"

        # Delegate to infrastructure adapter for TOML writing
        # Ensure atomic write with tempfile + rename
        pass

    def _load_active_project(self) -> None:
        """Load active project from env var or local state."""
        import os

        # Try environment variable first
        project_str = os.environ.get("JERRY_PROJECT")
        if project_str:
            try:
                project_id = ProjectId.parse(project_str)
                self._active_project = self._framework.get_project(project_id)
            except ValidationError:
                pass
            return

        # Try local state
        project_str = self._local_state.get("active_project")
        if project_str:
            try:
                project_id = ProjectId.parse(project_str)
                self._active_project = self._framework.get_project(project_id)
            except ValidationError:
                pass

    def _build_resolver(self) -> ConfigResolver:
        """Build configuration resolver with current context."""
        from .config_layers import (
            EnvVarLayer,
            SessionLocalLayer,
            ProjectConfigLayer,
            FrameworkConfigLayer,
            DefaultsLayer,
        )

        layers: list[IConfigLayer] = [
            EnvVarLayer(),
            SessionLocalLayer(self._local_state),
        ]

        if self._active_project:
            layers.append(ProjectConfigLayer(self._active_project.config))

        layers.extend([
            FrameworkConfigLayer(self._framework.config),
            DefaultsLayer(),
        ])

        return ConfigResolver(layers)


# Exception for project not found
class ProjectNotFoundError(Exception):
    """Raised when a project is not found."""

    def __init__(self, project_id: str) -> None:
        self.project_id = project_id
        super().__init__(f"Project not found: {project_id}")
```

#### Local State Format

```toml
# .jerry/local/context.toml

[context]
active_project = "PROJ-004-jerry-config"
last_accessed = 2026-01-12T12:00:00Z

[session]
id = "session-abc123"
started_at = 2026-01-12T10:00:00Z

[overrides]
# Local configuration overrides
logging.level = "DEBUG"
```

### L2: Strategic Implications

#### Design Rationale

| Decision | Rationale |
|----------|-----------|
| Not an aggregate | No domain events, transient per invocation |
| ConfigResolver pattern | Chain of Responsibility for precedence |
| ConfigValue with source | Full provenance for debugging |
| WorktreeInfo detection | Support for git worktree isolation |
| Local state persistence | Session continuity across invocations |

#### Configuration Precedence

```
Precedence Flow (highest to lowest):
┌─────────────────────────────────────────────────┐
│  1. Environment Variables (JERRY_*)            │
│     Example: JERRY_LOGGING_LEVEL=DEBUG         │
└──────────────────┬──────────────────────────────┘
                   │ (not found)
                   ▼
┌─────────────────────────────────────────────────┐
│  2. Session Local (.jerry/local/context.toml)  │
│     Example: [overrides] logging.level = "INFO"│
└──────────────────┬──────────────────────────────┘
                   │ (not found)
                   ▼
┌─────────────────────────────────────────────────┐
│  3. Project Config (projects/PROJ-*/config.toml)│
│     Example: [logging] level = "WARNING"       │
└──────────────────┬──────────────────────────────┘
                   │ (not found)
                   ▼
┌─────────────────────────────────────────────────┐
│  4. Framework Config (.jerry/config.toml)      │
│     Example: [logging] level = "ERROR"         │
└──────────────────┬──────────────────────────────┘
                   │ (not found)
                   ▼
┌─────────────────────────────────────────────────┐
│  5. Code Defaults                              │
│     Example: DEFAULT_LOG_LEVEL = "INFO"        │
└─────────────────────────────────────────────────┘
```

#### Invariants

1. Session always has a framework reference
2. Active project must exist in framework
3. Local state is worktree-specific (gitignored)
4. Config resolution follows strict precedence

---

## Consequences

### Positive
- Clear 5-level configuration precedence
- Config provenance for debugging
- Worktree-safe local state
- Session continuity across invocations

### Negative
- Requires TOML parsing in infrastructure
- Local state file I/O on every change
- Resolver rebuild on project switch

### Neutral
- Not an aggregate (no event sourcing)
- Local path is gitignored

---

## Related

- **WI-008d**: JerryFramework (referenced)
- **WI-008e**: JerryProject (active project)
- **WI-008f**: JerrySkill (skill invocation)
- **PROJ-004-e-004**: Configuration precedence research
