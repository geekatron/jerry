# PROJ-004-e-007: Jerry Skill/Agent Structure Analysis

> **PS ID:** PROJ-004
> **Entry ID:** e-007
> **Topic:** Jerry Skill/Agent Structure Analysis
> **Agent:** ps-researcher
> **Created:** 2026-01-12
> **Status:** COMPLETED

---

## L0: Executive Summary

Jerry skills are **framework-scoped capability modules** defined by SKILL.md files:
- **Location:** `skills/{skill-name}/SKILL.md`
- **Structure:** YAML frontmatter + Markdown body
- **Agents:** Defined in `skills/{skill-name}/agents/*.md`
- **Invocation:** Via `/skill-name` command or Skill tool
- **Output:** Project-relative paths (e.g., `projects/PROJ-NNN/research/`)

Skills need **configuration for output paths, agent preferences, and capability settings**.

---

## L1: Technical Implementation Details

### 1. SKILL.md Format

#### File Location
```
skills/
├── problem-solving/
│   ├── SKILL.md              # Skill definition
│   └── agents/
│       ├── ps-researcher.md
│       ├── ps-architect.md
│       └── ps-validator.md
├── worktracker/
│   └── SKILL.md
└── architecture/
    └── SKILL.md
```

#### Frontmatter Structure
```yaml
---
name: problem-solving
description: Structured problem-solving framework with specialized agents...
version: "2.0.0"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Task, WebSearch, WebFetch
activation-keywords:
  - "research"
  - "analyze"
  - "investigate"
  - "ADR"
  - "5 whys"
---
```

#### Frontmatter Fields

| Field | Type | Purpose |
|-------|------|---------|
| `name` | string | Skill identifier (matches directory name) |
| `description` | string | Human-readable description |
| `version` | string | Semantic version |
| `allowed-tools` | string (CSV) | Tools the skill can use |
| `activation-keywords` | list[string] | Keywords for auto-detection |

#### Markdown Body
The body describes:
- Purpose and capabilities
- When to use the skill
- Available agents table
- Invocation options
- Output locations
- Constitutional compliance

### 2. Agent Definitions

#### Agent File Location
```
skills/problem-solving/agents/
├── PS_AGENT_TEMPLATE.md      # Template for creating agents
├── ps-researcher.md          # Research specialist
├── ps-analyst.md             # Analysis specialist
├── ps-architect.md           # Architecture specialist
├── ps-validator.md           # Validation specialist
├── ps-synthesizer.md         # Synthesis specialist
├── ps-reviewer.md            # Review specialist
├── ps-investigator.md        # Investigation specialist
└── ps-reporter.md            # Reporting specialist
```

#### Agent Markdown Structure
```markdown
# ps-researcher

> Research Specialist Agent

## Role
Gathers information with citations and produces research artifacts.

## Output Format
- L0: Executive summary
- L1: Technical details
- L2: Strategic implications

## Output Location
`docs/research/{ps-id}-{entry-id}-{topic}.md`

## Invocation Prompt Template
```
You are the ps-researcher agent (v2.0.0).

## PS CONTEXT (REQUIRED)
- **PS ID:** {ps-id}
- **Entry ID:** {entry-id}
- **Topic:** {topic}

## MANDATORY PERSISTENCE (P-002)
Create file at: {output-path}

## RESEARCH TASK
{task-description}
```
```

#### Agent Properties Extracted

| Property | Example | Domain Model Mapping |
|----------|---------|---------------------|
| Name | `ps-researcher` | `AgentInfo.name` |
| Role | Research Specialist | `AgentInfo.description` |
| Output location | `docs/research/` | `AgentInfo.output_path` |
| Version | v2.0.0 | Inherited from skill |

### 3. Skill Discovery Mechanism

#### Current Implementation
Skills are discovered by the Skill tool in Claude Code:
1. User types `/problem-solving` or mentions activation keyword
2. Skill tool searches `skills/` directory for matching SKILL.md
3. SKILL.md frontmatter + body is loaded as context
4. Claude executes with skill instructions

#### Discovery Flow (Proposed for JerrySkill)
```python
class JerryFramework:
    def list_skills(self) -> list[SkillInfo]:
        """Discover available skills by scanning skills/ directory."""
        skills = []
        skills_dir = self._root_path / "skills"
        for skill_dir in skills_dir.iterdir():
            if skill_dir.is_dir() and (skill_dir / "SKILL.md").exists():
                skill_name = SkillName(skill_dir.name)
                skill_info = self._read_skill_info(skill_dir)
                skills.append(skill_info)
        return skills

    def get_skill(self, skill_name: SkillName) -> JerrySkill | None:
        """Load a specific skill by name."""
        skill_path = self._root_path / "skills" / skill_name.value
        if not (skill_path / "SKILL.md").exists():
            return None
        return JerrySkill(skill_name, skill_path, self)
```

### 4. Skill-Project Interaction

#### Active Project Context
Skills need to know the active project for:
- **Output paths**: Research artifacts go to `projects/PROJ-NNN/research/`
- **Project config**: Skill behavior may vary per project
- **Work item linking**: PS IDs reference project IDs

#### Current Pattern (from SKILL.md)
```markdown
## Output Structure

docs/                          # Root-relative (for framework docs)
├── research/
└── decisions/

projects/PROJ-NNN-slug/        # Project-relative (for project artifacts)
├── research/
├── analysis/
├── decisions/
└── synthesis/
```

#### Project-Relative Output Resolution
```python
class JerrySkill:
    def get_output_path(self, project: JerryProject | None = None) -> Path:
        """Get output path, relative to project if provided."""
        if project:
            # Project-relative: projects/PROJ-NNN/research/
            return project.path / self._default_output_subdir
        else:
            # Framework-relative: docs/research/
            return self._framework.root_path / "docs" / self._default_output_subdir

class JerrySession:
    def get_skill_output_path(self, skill: JerrySkill) -> Path:
        """Get output path using active project context."""
        return skill.get_output_path(self.active_project)
```

#### Project-Specific Skill Configuration (Proposed)
```toml
# projects/PROJ-004-jerry-config/config.toml

[skills.problem-solving]
# Override default output path for this project
output_subdir = "ps-output"

# Agent preferences
preferred_agents = ["ps-researcher", "ps-architect"]

[skills.worktracker]
# Worktracker-specific settings
auto_update_on_complete = true
```

### 5. Skill Configuration Needs

#### Framework-Level Configuration
```toml
# .jerry/config.toml

[skills]
# Global skill settings
auto_discover = true
skills_directory = "skills"

[skills.problem-solving]
version = "2.0.0"
enabled = true

[skills.worktracker]
enabled = true
```

#### Skill-Level Configuration (Proposed)
```toml
# skills/problem-solving/config.toml

[defaults]
output_subdir = "research"
agent_model = "opus"

[agents.ps-researcher]
output_prefix = "e-"
max_sources = 10

[agents.ps-architect]
adr_format = "nygard"
```

#### Configuration Requirements Summary

| Requirement | Scope | Example |
|-------------|-------|---------|
| Output directory | Per-skill | `research/` |
| Agent model preference | Per-agent | `opus`, `sonnet` |
| Enabled/disabled | Per-project | `skills.problem-solving.enabled = false` |
| Custom output prefix | Per-project | `output_subdir = "ps-output"` |
| Agent-specific settings | Per-agent | `max_sources = 10` |

---

## L2: Strategic Implications for Domain Model

### JerrySkill Aggregate Design

```python
@dataclass(frozen=True, slots=True)
class SkillName:
    """Strongly-typed skill identifier."""
    value: str  # "problem-solving", "worktracker"

    def __post_init__(self) -> None:
        if not re.match(r"^[a-z][a-z0-9]*(?:-[a-z0-9]+)*$", self.value):
            raise ValidationError(field="skill_name", message="Invalid format")


@dataclass(frozen=True)
class AgentInfo:
    """Information about an agent within a skill."""
    name: str                    # "ps-researcher"
    description: str             # "Research Specialist"
    output_subdir: str           # "research"
    file_path: Path              # skills/problem-solving/agents/ps-researcher.md


class JerrySkill:
    """Skill aggregate providing capabilities."""

    def __init__(
        self,
        skill_name: SkillName,
        path: Path,
        framework: JerryFramework,
    ) -> None:
        self._skill_name = skill_name
        self._path = path
        self._framework = framework
        self._metadata = self._parse_skill_md()
        self._agents = self._discover_agents()

    @property
    def skill_name(self) -> SkillName:
        return self._skill_name

    @property
    def version(self) -> str:
        return self._metadata.get("version", "0.0.0")

    @property
    def description(self) -> str:
        return self._metadata.get("description", "")

    def list_agents(self) -> list[AgentInfo]:
        """List all agents defined in this skill."""
        return list(self._agents.values())

    def get_agent(self, agent_name: str) -> AgentInfo | None:
        """Get a specific agent by name."""
        return self._agents.get(agent_name)

    def get_output_path(self, project: JerryProject | None = None) -> Path:
        """Get output path, relative to project if provided."""
        if project:
            return project.path / self._default_output_subdir
        return self._framework.root_path / "docs" / self._default_output_subdir
```

### Skill Discovery in JerryFramework

```python
class JerryFramework:
    def __init__(self, root_path: Path) -> None:
        self._root_path = root_path
        self._skills: dict[SkillName, JerrySkill] | None = None  # Lazy

    def list_skills(self) -> list[SkillInfo]:
        """List available skills (lazy discovery)."""
        if self._skills is None:
            self._skills = self._discover_skills()
        return [
            SkillInfo(name=s.skill_name, version=s.version, description=s.description)
            for s in self._skills.values()
        ]

    def get_skill(self, skill_name: SkillName) -> JerrySkill | None:
        """Get a specific skill."""
        if self._skills is None:
            self._skills = self._discover_skills()
        return self._skills.get(skill_name)

    def _discover_skills(self) -> dict[SkillName, JerrySkill]:
        skills = {}
        skills_dir = self._root_path / "skills"
        for skill_dir in skills_dir.iterdir():
            if skill_dir.is_dir() and (skill_dir / "SKILL.md").exists():
                try:
                    skill_name = SkillName(skill_dir.name)
                    skills[skill_name] = JerrySkill(skill_name, skill_dir, self)
                except ValidationError:
                    pass  # Skip invalid skill directories
        return skills
```

### Integration with JerrySession

```python
class JerrySession:
    def invoke_agent(self, skill_name: str, agent_name: str, task: str) -> Path:
        """Invoke an agent and return output path."""
        skill = self._framework.get_skill(SkillName(skill_name))
        if not skill:
            raise SkillNotFoundError(skill_name)

        agent = skill.get_agent(agent_name)
        if not agent:
            raise AgentNotFoundError(agent_name)

        output_path = skill.get_output_path(self.active_project)
        # Agent invocation happens via Task tool, path is for reference
        return output_path / f"{self._generate_entry_id()}-{task[:20]}.md"
```

---

## Evidence Summary

| Finding | Evidence Source |
|---------|-----------------|
| SKILL.md frontmatter format | `skills/problem-solving/SKILL.md:1-19` |
| Agent file structure | `skills/problem-solving/agents/*.md` |
| Output locations | SKILL.md "Output Structure" section |
| Activation keywords | SKILL.md frontmatter |
| Constitutional compliance | SKILL.md references P-002 |

---

## Recommendations

1. **Create SkillName value object** with kebab-case validation
2. **Parse SKILL.md frontmatter** in infrastructure adapter (YAML parsing)
3. **Lazy-load skill agents** only when skill is accessed
4. **Support skill-level config.toml** for agent preferences
5. **Use project-relative output paths** when active project exists
6. **Add skill configuration section** to project config.toml
