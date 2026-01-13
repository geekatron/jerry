# WI-008d: Design JerryFramework Aggregate

| Field | Value |
|-------|-------|
| **ID** | WI-008d |
| **Title** | Design JerryFramework aggregate |
| **Type** | Design |
| **Status** | PENDING |
| **Priority** | CRITICAL |
| **Phase** | PHASE-02 |
| **Parent** | WI-008 |
| **Agent** | ps-architect |
| **Assignee** | WT-Main |
| **Created** | 2026-01-12 |
| **Completed** | - |

---

## Description

Design the JerryFramework aggregate root - the top-level entity representing the Jerry framework installation. This aggregate owns projects, skills, and global configuration.

---

## Agent Invocation

### ps-architect Prompt

```
You are the ps-architect agent (v2.0.0).

## PS CONTEXT (REQUIRED)
- **PS ID:** PROJ-004
- **Entry ID:** e-008
- **Topic:** JerryFramework Aggregate Design

## MANDATORY PERSISTENCE (P-002)
Create ADR at: projects/PROJ-004-jerry-config/decisions/ADR-PROJ004-001-jerry-framework-aggregate.md

## DESIGN TASK

Design the JerryFramework aggregate root using Nygard ADR format.

### Context
Jerry needs a root aggregate that:
- Represents the framework installation (repository root)
- Owns global configuration
- Can discover and navigate to projects
- Can discover and navigate to skills
- Provides configuration resolution starting point

### Design Requirements
1. Aggregate must be the entry point for all Jerry operations
2. Must support project discovery via `list_projects()`
3. Must support skill discovery via `list_skills()`
4. Must own framework-level configuration
5. Must be constructible from repository root path

### Questions to Answer
1. Should JerryFramework lazy-load projects/skills or eager-load?
2. How to handle invalid/corrupted project directories?
3. Should framework config be mutable or immutable?
4. What invariants must JerryFramework enforce?
5. What events does JerryFramework emit?

### Inputs (from research)
- WI-008a findings on current codebase patterns
- WI-008b findings on DDD hierarchical patterns

### Constraints
- Must follow hexagonal architecture
- Domain layer has zero external dependencies
- Must be testable without filesystem

## ADR STRUCTURE
Use Nygard format with:
- Title, Status, Context
- Decision with code examples
- Consequences (positive, negative, neutral)
- L0/L1/L2 explanation levels
```

---

## Acceptance Criteria

- [ ] AC-008d.1: ADR created with Nygard format
- [ ] AC-008d.2: JerryFramework class interface defined
- [ ] AC-008d.3: Project navigation methods specified
- [ ] AC-008d.4: Skill navigation methods specified
- [ ] AC-008d.5: Configuration ownership clarified
- [ ] AC-008d.6: Invariants documented
- [ ] AC-008d.7: Events defined (if any)

---

## Proposed Interface (Draft)

```python
class JerryFramework:
    """Root aggregate for Jerry framework."""

    def __init__(self, root_path: Path) -> None:
        """Initialize from repository root."""
        ...

    @property
    def root_path(self) -> Path:
        """Repository root path."""
        ...

    @property
    def config(self) -> FrameworkConfig:
        """Framework-level configuration."""
        ...

    @property
    def version(self) -> str:
        """Framework version."""
        ...

    # Project navigation
    def list_projects(self) -> list[ProjectInfo]:
        """Discover all valid projects."""
        ...

    def get_project(self, project_id: ProjectId) -> JerryProject | None:
        """Get project by ID, or None if not found."""
        ...

    def create_project(self, slug: str, name: str) -> JerryProject:
        """Create a new project."""
        ...

    # Skill navigation
    def list_skills(self) -> list[SkillInfo]:
        """Discover all available skills."""
        ...

    def get_skill(self, skill_name: SkillName) -> JerrySkill | None:
        """Get skill by name, or None if not found."""
        ...
```

---

## Evidence

| Criterion | Evidence | Source |
|-----------|----------|--------|
| AC-008d.1 | - | - |
| AC-008d.2 | - | - |
| AC-008d.3 | - | - |
| AC-008d.4 | - | - |
| AC-008d.5 | - | - |
| AC-008d.6 | - | - |
| AC-008d.7 | - | - |

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
| Depends On | WI-008a, WI-008b | Research must complete |
| Parallel With | WI-008e, WI-008f | Can design in parallel |
| Blocks | WI-008g | Session needs framework |

---

## Related Artifacts

- **Output**: `decisions/ADR-PROJ004-001-jerry-framework-aggregate.md`
- **Research Input**: `research/PROJ-004-e-005-*.md`, `research/PROJ-004-e-006-*.md`
