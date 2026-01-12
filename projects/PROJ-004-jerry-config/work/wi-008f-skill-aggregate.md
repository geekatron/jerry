# WI-008f: Design JerrySkill Aggregate

| Field | Value |
|-------|-------|
| **ID** | WI-008f |
| **Title** | Design JerrySkill aggregate |
| **Type** | Design |
| **Status** | PENDING |
| **Priority** | HIGH |
| **Phase** | PHASE-02 |
| **Parent** | WI-008 |
| **Agent** | ps-architect |
| **Assignee** | WT-Main |
| **Created** | 2026-01-12 |
| **Completed** | - |

---

## Description

Design the JerrySkill aggregate - represents a skill that provides capabilities to Jerry. Skills contain agents and have their own configuration.

---

## Agent Invocation

### ps-architect Prompt

```
You are the ps-architect agent (v2.0.0).

## PS CONTEXT (REQUIRED)
- **PS ID:** PROJ-004
- **Entry ID:** e-010
- **Topic:** JerrySkill Aggregate Design

## MANDATORY PERSISTENCE (P-002)
Create ADR at: projects/PROJ-004-jerry-config/decisions/ADR-PROJ004-003-jerry-skill-aggregate.md

## DESIGN TASK

Design the JerrySkill aggregate using Nygard ADR format.

### Context
A JerrySkill represents a capability module:
- Lives in `skills/{skill-name}/` directory
- Defined by SKILL.md with metadata
- Contains agent definitions in `agents/` subdirectory
- May have skill-specific configuration
- Framework-level (not project-specific)

### Design Requirements
1. Must have strongly-typed SkillName value object
2. Must provide agent discovery via `list_agents()`
3. Must load skill metadata from SKILL.md
4. Must support optional skill configuration
5. Skills are framework-scoped, not project-scoped

### Questions to Answer
1. Should JerrySkill be an aggregate or entity?
2. How to parse SKILL.md metadata?
3. How to represent agent definitions?
4. Should skill output paths be project-relative?
5. What is the relationship between skill and project context?

### Key Concerns
- Skill discovery (list available skills)
- Agent discovery within skill
- Skill invocation context (which project?)
- Output path resolution (skill vs project directory)

### Inputs (from research)
- WI-008c findings on skill/agent structure
- WI-008b findings on DDD patterns

### Constraints
- Must follow hexagonal architecture
- SkillName must be a value object
- Skills exist independently of projects

## ADR STRUCTURE
Use Nygard format with:
- Title, Status, Context
- Decision with code examples
- Consequences (positive, negative, neutral)
- L0/L1/L2 explanation levels
```

---

## Acceptance Criteria

- [ ] AC-008f.1: ADR created with Nygard format
- [ ] AC-008f.2: JerrySkill class interface defined
- [ ] AC-008f.3: SkillName value object designed
- [ ] AC-008f.4: Agent discovery mechanism defined
- [ ] AC-008f.5: Skill metadata model specified
- [ ] AC-008f.6: Project context interaction clarified
- [ ] AC-008f.7: Output path resolution documented

---

## Proposed Interface (Draft)

```python
@dataclass(frozen=True, slots=True)
class SkillName:
    """Strongly-typed skill identifier."""
    value: str  # "problem-solving", "worktracker"

    def __post_init__(self) -> None:
        if not re.match(r"^[\w-]+$", self.value):
            raise ValidationError(field="skill_name", message="Invalid format")


@dataclass(frozen=True)
class AgentInfo:
    """Information about an agent within a skill."""
    name: str
    description: str
    file_path: Path


class JerrySkill:
    """Skill aggregate providing capabilities."""

    def __init__(self, skill_name: SkillName, path: Path) -> None:
        ...

    @property
    def skill_name(self) -> SkillName: ...

    @property
    def path(self) -> Path: ...

    @property
    def version(self) -> str: ...

    @property
    def description(self) -> str: ...

    @property
    def config(self) -> SkillConfig | None: ...

    # Agent navigation
    def list_agents(self) -> list[AgentInfo]: ...

    def get_agent(self, agent_name: str) -> AgentDefinition | None: ...

    # Output path (context-dependent)
    def get_output_path(self, project: JerryProject | None = None) -> Path:
        """Get output path, relative to project if provided."""
        if project:
            return project.path / self._output_subdir
        return self.path / "output"
```

---

## Evidence

| Criterion | Evidence | Source |
|-----------|----------|--------|
| AC-008f.1 | - | - |
| AC-008f.2 | - | - |
| AC-008f.3 | - | - |
| AC-008f.4 | - | - |
| AC-008f.5 | - | - |
| AC-008f.6 | - | - |
| AC-008f.7 | - | - |

---

## Progress Log

| Timestamp | Update | Actor |
|-----------|--------|-------|
| 2026-01-12T12:00:00Z | Work item created | Claude |

---

## Dependencies

| Type | Work Item | Relationship |
|------|-----------|--------------|
| Part Of | WI-008 | Parent work item |
| Depends On | WI-008b, WI-008c | Research must complete |
| Parallel With | WI-008d, WI-008e | Can design in parallel |
| Blocks | WI-008g | Session may use skills |

---

## Related Artifacts

- **Output**: `decisions/ADR-PROJ004-003-jerry-skill-aggregate.md`
- **Research Input**: `research/PROJ-004-e-006-*.md`, `research/PROJ-004-e-007-*.md`
