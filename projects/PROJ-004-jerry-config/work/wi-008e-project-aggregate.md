# WI-008e: Design JerryProject Aggregate

| Field | Value |
|-------|-------|
| **ID** | WI-008e |
| **Title** | Design JerryProject aggregate |
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

Design the JerryProject aggregate - represents a single project within the Jerry framework. Each project has its own configuration, work items, plan, and worktracker.

---

## Agent Invocation

### ps-architect Prompt

```
You are the ps-architect agent (v2.0.0).

## PS CONTEXT (REQUIRED)
- **PS ID:** PROJ-004
- **Entry ID:** e-009
- **Topic:** JerryProject Aggregate Design

## MANDATORY PERSISTENCE (P-002)
Create ADR at: projects/PROJ-004-jerry-config/decisions/ADR-PROJ004-002-jerry-project-aggregate.md

## DESIGN TASK

Design the JerryProject aggregate using Nygard ADR format.

### Context
A JerryProject represents a discrete unit of work within Jerry:
- Has unique ID following PROJ-NNN-slug pattern
- Lives in `projects/PROJ-NNN-slug/` directory
- Has its own `.jerry/` configuration
- Owns work items, plan, worktracker
- Can override framework configuration

### Design Requirements
1. Must have strongly-typed ProjectId value object
2. Must provide path accessors for project artifacts
3. Must support configuration with framework fallback
4. Must be navigable from JerryFramework
5. Parent reference: should it hold JerryFramework or just root_path?

### Questions to Answer
1. Is JerryProject a full aggregate or an entity within JerryFramework?
2. How to validate project structure integrity?
3. Should project config be loaded eagerly or lazily?
4. What invariants must JerryProject enforce?
5. What events does JerryProject emit?

### Key Paths to Provide
- WORKTRACKER.md path
- PLAN.md path
- .jerry/data/items/ path
- .jerry/config.toml path
- work/ directory path
- research/ directory path

### Inputs (from research)
- WI-008a findings on current project structure
- WI-008b findings on parent-child aggregate patterns

### Constraints
- Must follow hexagonal architecture
- ProjectId must be a value object with validation
- Domain layer has zero external dependencies

## ADR STRUCTURE
Use Nygard format with:
- Title, Status, Context
- Decision with code examples
- Consequences (positive, negative, neutral)
- L0/L1/L2 explanation levels
```

---

## Acceptance Criteria

- [ ] AC-008e.1: ADR created with Nygard format
- [ ] AC-008e.2: JerryProject class interface defined
- [ ] AC-008e.3: ProjectId value object designed
- [ ] AC-008e.4: Path accessors specified
- [ ] AC-008e.5: Configuration inheritance clarified
- [ ] AC-008e.6: Parent relationship decided
- [ ] AC-008e.7: Invariants documented

---

## Proposed Interface (Draft)

```python
@dataclass(frozen=True, slots=True)
class ProjectId:
    """Strongly-typed project identifier."""
    value: str  # "PROJ-001-plugin-cleanup"

    def __post_init__(self) -> None:
        if not re.match(r"^PROJ-\d{3}-[\w-]+$", self.value):
            raise ValidationError(field="project_id", message="Invalid format")

    @property
    def number(self) -> int:
        return int(self.value[5:8])

    @property
    def slug(self) -> str:
        return self.value[9:]


class JerryProject:
    """Project aggregate within Jerry framework."""

    def __init__(
        self,
        project_id: ProjectId,
        path: Path,
        framework: JerryFramework,
    ) -> None:
        ...

    @property
    def project_id(self) -> ProjectId: ...

    @property
    def path(self) -> Path: ...

    @property
    def name(self) -> str: ...

    @property
    def config(self) -> ProjectConfig: ...

    # Path accessors
    def get_worktracker_path(self) -> Path: ...
    def get_plan_path(self) -> Path: ...
    def get_work_items_path(self) -> Path: ...
    def get_work_path(self) -> Path: ...
    def get_research_path(self) -> Path: ...
    def get_config_path(self) -> Path: ...

    # Configuration with fallback
    def get_setting(self, key: str) -> Any | None:
        """Get setting with project → framework fallback."""
        ...
```

---

## Evidence

| Criterion | Evidence | Source |
|-----------|----------|--------|
| AC-008e.1 | - | - |
| AC-008e.2 | - | - |
| AC-008e.3 | - | - |
| AC-008e.4 | - | - |
| AC-008e.5 | - | - |
| AC-008e.6 | - | - |
| AC-008e.7 | - | - |

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
| Parallel With | WI-008d, WI-008f | Can design in parallel |
| Blocks | WI-008g | Session needs project |

---

## Related Artifacts

- **Output**: `decisions/ADR-PROJ004-002-jerry-project-aggregate.md`
- **Research Input**: `research/PROJ-004-e-005-*.md`, `research/PROJ-004-e-006-*.md`
