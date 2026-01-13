# ADR-PROJ004-003: JerrySkill Aggregate

> **Status:** ACCEPTED
> **Date:** 2026-01-12
> **Deciders:** Claude (ps-architect)
> **Work Item:** WI-008f

---

## Context

JerrySkill represents a capability module within Jerry. Skills:
- Are defined by SKILL.md files in skills/ directory
- Contain agent definitions in agents/ subdirectory
- Are framework-scoped (not project-scoped)
- Need to resolve output paths relative to active project

### Research Inputs
- PROJ-004-e-007: Skill/agent structure analysis
- SKILL.md frontmatter format
- Agent markdown structure

---

## Decision

### L0: Executive Summary

**JerrySkill is a child aggregate** of JerryFramework that represents a capability module. It provides agent discovery and output path resolution relative to the active project.

### L1: Technical Design

#### SkillName Value Object

```python
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import ClassVar
from re import Pattern

from src.shared_kernel.exceptions import ValidationError


@dataclass(frozen=True, slots=True)
class SkillName:
    """Strongly-typed skill identifier.

    Format: lowercase kebab-case (e.g., "problem-solving", "worktracker")

    Attributes:
        value: The skill name string
    """
    value: str

    _PATTERN: ClassVar[Pattern[str]] = re.compile(r"^[a-z][a-z0-9]*(?:-[a-z0-9]+)*$")

    def __post_init__(self) -> None:
        if not self._PATTERN.match(self.value):
            raise ValidationError(
                field="skill_name",
                message="Must be lowercase kebab-case (e.g., 'problem-solving')",
            )

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return f"SkillName(value={self.value!r})"
```

#### AgentInfo Value Object

```python
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class AgentInfo:
    """Information about an agent within a skill (Value Object).

    Attributes:
        name: Agent name (e.g., "ps-researcher")
        description: Human-readable description
        output_subdir: Default output subdirectory (e.g., "research")
        file_path: Path to the agent definition file
    """
    name: str
    description: str
    output_subdir: str
    file_path: Path

    def __str__(self) -> str:
        return f"{self.name}: {self.description}"
```

#### SkillConfig Value Object

```python
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class SkillConfig:
    """Skill-level configuration snapshot (Value Object).

    Attributes:
        values: Configuration dictionary
        source_path: Path to config.toml if loaded
    """
    values: dict[str, Any]
    source_path: Path | None = None

    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value."""
        return self.values.get(key, default)

    def get_agent_config(self, agent_name: str) -> dict[str, Any]:
        """Get agent-specific configuration."""
        return self.values.get(f"agents.{agent_name}", {})
```

#### JerrySkill Aggregate

```python
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Any
import re

if TYPE_CHECKING:
    from .jerry_framework import JerryFramework
    from .jerry_project import JerryProject


class JerrySkill:
    """Skill aggregate providing capabilities.

    A skill is a capability module defined by SKILL.md that contains
    agent definitions for specialized tasks.

    Attributes:
        skill_name: Unique identifier
        path: Filesystem path to the skill directory
        version: Skill version from SKILL.md
        description: Human-readable description
        config: Skill-level configuration
    """

    def __init__(
        self,
        skill_name: SkillName,
        path: Path,
        framework: JerryFramework,
    ) -> None:
        """Initialize the skill.

        Args:
            skill_name: The skill identifier
            path: Path to the skill directory
            framework: Parent framework reference

        Raises:
            ValidationError: If path doesn't exist or SKILL.md missing
        """
        skill_md = path / "SKILL.md"
        if not skill_md.exists():
            raise ValidationError(
                field="path",
                message=f"SKILL.md not found in: {path}",
            )

        self._skill_name = skill_name
        self._path = path.resolve()
        self._framework = framework

        # Parse SKILL.md metadata
        self._metadata = self._parse_skill_md()
        self._config = self._load_config()

        # Lazy-loaded agent cache
        self._agents: dict[str, AgentInfo] | None = None

    @property
    def skill_name(self) -> SkillName:
        """The unique skill identifier."""
        return self._skill_name

    @property
    def path(self) -> Path:
        """Filesystem path to the skill directory."""
        return self._path

    @property
    def version(self) -> str:
        """Skill version from SKILL.md."""
        return self._metadata.get("version", "0.0.0")

    @property
    def description(self) -> str:
        """Human-readable skill description."""
        return self._metadata.get("description", "")

    @property
    def allowed_tools(self) -> list[str]:
        """List of tools the skill is allowed to use."""
        tools_str = self._metadata.get("allowed-tools", "")
        return [t.strip() for t in tools_str.split(",") if t.strip()]

    @property
    def activation_keywords(self) -> list[str]:
        """Keywords that trigger skill activation."""
        return self._metadata.get("activation-keywords", [])

    @property
    def config(self) -> SkillConfig:
        """Skill-level configuration."""
        return self._config

    @property
    def framework(self) -> JerryFramework:
        """Parent framework reference."""
        return self._framework

    # =========================================================================
    # Agent Navigation
    # =========================================================================

    def list_agents(self) -> list[AgentInfo]:
        """List all agents defined in this skill.

        Returns:
            List of AgentInfo objects
        """
        if self._agents is None:
            self._agents = self._discover_agents()
        return list(self._agents.values())

    def get_agent(self, agent_name: str) -> AgentInfo | None:
        """Get a specific agent by name.

        Args:
            agent_name: The agent name (e.g., "ps-researcher")

        Returns:
            AgentInfo if found, None otherwise
        """
        if self._agents is None:
            self._agents = self._discover_agents()
        return self._agents.get(agent_name)

    # =========================================================================
    # Output Path Resolution
    # =========================================================================

    def get_output_path(
        self,
        project: JerryProject | None = None,
        agent_name: str | None = None,
    ) -> Path:
        """Get output path for skill artifacts.

        Args:
            project: Active project (if any)
            agent_name: Specific agent (for agent-specific subdir)

        Returns:
            Output path - project-relative if project provided,
            otherwise framework-relative (docs/)
        """
        # Determine output subdirectory
        if agent_name:
            agent = self.get_agent(agent_name)
            subdir = agent.output_subdir if agent else "output"
        else:
            subdir = self._get_default_output_subdir()

        if project:
            # Project-relative: projects/PROJ-NNN/research/
            return project.path / subdir
        else:
            # Framework-relative: docs/research/
            return self._framework.root_path / "docs" / subdir

    def _get_default_output_subdir(self) -> str:
        """Get default output subdirectory for this skill."""
        # Could be configured in skill config or derived from name
        return self._config.get("output_subdir", "output")

    # =========================================================================
    # Private Methods
    # =========================================================================

    def _parse_skill_md(self) -> dict[str, Any]:
        """Parse SKILL.md frontmatter.

        Returns:
            Dictionary of frontmatter values
        """
        skill_md = self._path / "SKILL.md"
        content = skill_md.read_text(encoding="utf-8")

        # Extract YAML frontmatter between ---
        match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
        if not match:
            return {}

        frontmatter = match.group(1)
        metadata: dict[str, Any] = {}

        # Simple YAML parsing (could use pyyaml in infrastructure)
        for line in frontmatter.split("\n"):
            if ":" in line:
                key, value = line.split(":", 1)
                key = key.strip()
                value = value.strip().strip('"').strip("'")

                # Handle lists
                if key == "activation-keywords":
                    # Collect subsequent lines with - prefix
                    continue

                metadata[key] = value

        # Parse activation-keywords list
        if "activation-keywords:" in frontmatter:
            keywords = []
            in_keywords = False
            for line in frontmatter.split("\n"):
                if "activation-keywords:" in line:
                    in_keywords = True
                    continue
                if in_keywords:
                    if line.strip().startswith("-"):
                        keywords.append(line.strip()[1:].strip().strip('"'))
                    elif line.strip() and not line.startswith(" "):
                        break
            metadata["activation-keywords"] = keywords

        return metadata

    def _load_config(self) -> SkillConfig:
        """Load skill configuration from config.toml."""
        config_path = self._path / "config.toml"
        if not config_path.exists():
            return SkillConfig(values={}, source_path=None)

        # Delegate to infrastructure adapter
        return SkillConfig(values={}, source_path=config_path)

    def _discover_agents(self) -> dict[str, AgentInfo]:
        """Discover all agents in the agents/ directory."""
        agents = {}
        agents_dir = self._path / "agents"

        if not agents_dir.exists():
            return agents

        for agent_file in agents_dir.glob("*.md"):
            # Skip template files
            if agent_file.name.startswith("_") or "TEMPLATE" in agent_file.name:
                continue

            agent_name = agent_file.stem
            agent_info = self._parse_agent_md(agent_file)
            if agent_info:
                agents[agent_name] = agent_info

        return agents

    def _parse_agent_md(self, agent_file: Path) -> AgentInfo | None:
        """Parse agent markdown file to extract info.

        Args:
            agent_file: Path to agent.md file

        Returns:
            AgentInfo if parseable, None otherwise
        """
        content = agent_file.read_text(encoding="utf-8")

        # Extract agent name from first heading
        name = agent_file.stem

        # Extract description from "Role" or first paragraph
        description = ""
        lines = content.split("\n")
        for i, line in enumerate(lines):
            if line.strip().lower() in ("## role", "## description"):
                if i + 1 < len(lines):
                    description = lines[i + 1].strip()
                break

        if not description:
            # Use first non-heading, non-empty line
            for line in lines:
                if line.strip() and not line.startswith("#") and not line.startswith(">"):
                    description = line.strip()
                    break

        # Determine output subdirectory from agent name or content
        output_subdir = self._infer_output_subdir(name, content)

        return AgentInfo(
            name=name,
            description=description[:100],  # Truncate
            output_subdir=output_subdir,
            file_path=agent_file,
        )

    def _infer_output_subdir(self, agent_name: str, content: str) -> str:
        """Infer output subdirectory from agent name or content."""
        # Common mappings
        subdir_map = {
            "researcher": "research",
            "analyst": "analysis",
            "architect": "decisions",
            "validator": "analysis",
            "synthesizer": "synthesis",
            "reviewer": "reviews",
            "investigator": "investigations",
            "reporter": "reports",
        }

        for keyword, subdir in subdir_map.items():
            if keyword in agent_name.lower():
                return subdir

        # Look for Output Location in content
        match = re.search(r"Output Location[:\s]+[`\"]?([a-z/]+)", content, re.IGNORECASE)
        if match:
            return match.group(1).strip("`/")

        return "output"

    # =========================================================================
    # String Representation
    # =========================================================================

    def __str__(self) -> str:
        return f"{self._skill_name} v{self.version}"

    def __repr__(self) -> str:
        return (
            f"JerrySkill("
            f"skill_name={self._skill_name!r}, "
            f"version={self.version!r}, "
            f"agents={len(self.list_agents())})"
        )
```

### L2: Strategic Implications

#### Design Rationale

| Decision | Rationale |
|----------|-----------|
| SkillName as value object | Type-safe skill identification |
| AgentInfo as value object | Immutable agent metadata |
| Framework-scoped skills | Skills are reusable across projects |
| Output path resolution | Project-relative when project active |
| Lazy agent discovery | Only load agents on first access |

#### Invariants

1. `skill_name` must be lowercase kebab-case
2. SKILL.md must exist in skill directory
3. Agent names are unique within a skill
4. Output paths are always valid directories

#### Skill Directory Structure

```
skills/{skill-name}/
├── SKILL.md                   # Required: Skill definition
├── config.toml                # Optional: Skill configuration
└── agents/
    ├── ps-researcher.md       # Agent definitions
    ├── ps-architect.md
    └── ps-validator.md
```

---

## Consequences

### Positive
- Type-safe skill identification
- Agent discovery with lazy loading
- Output path resolution handles project context
- Parses SKILL.md frontmatter

### Negative
- Simple YAML parsing (may need library for complex cases)
- Agent info inferred from markdown (may be imprecise)

### Neutral
- Skills are framework-scoped, not project-scoped
- Skill config separate from project skill config

---

## Related

- **WI-008d**: JerryFramework (parent aggregate)
- **WI-008g**: JerrySession (resolves skill output paths)
- **PROJ-004-e-007**: Skill/agent structure analysis
