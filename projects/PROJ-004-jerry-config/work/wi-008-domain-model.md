# WI-008: Domain Model Design

| Field | Value |
|-------|-------|
| **ID** | WI-008 |
| **Title** | Design hierarchical configuration domain model |
| **Type** | Design |
| **Status** | IN_PROGRESS |
| **Priority** | CRITICAL |
| **Phase** | PHASE-02 |
| **Assignee** | WT-Main |
| **Created** | 2026-01-12 |
| **Updated** | 2026-01-12 |
| **Completed** | - |

---

## Description

Design the domain model for Jerry's hierarchical configuration system. The model must represent:

1. **JerryFramework** - Root aggregate (repository-level)
2. **JerryProject** - Project aggregate (project-level)
3. **JerrySkill** - Skill aggregate (skill-level)
4. **JerrySession** - Runtime context (worktree-local)

This is a **critical path** item that blocks all implementation work. The design must be validated before proceeding.

---

## Problem Statement

The original flat `IConfigurationProvider` design is **insufficient** because:

| Problem | Impact |
|---------|--------|
| P1: Too Flat | Cannot model framework → project → skill hierarchy |
| P2: No Entities | Just key-value strings, no domain objects |
| P3: No Navigation | Cannot discover/list projects or skills |
| P4: No Context | Doesn't know "which project am I in?" |
| P5: No Validation | Cannot validate project/skill structure |
| P6: No Relationships | Skills don't know their project context |

---

## Acceptance Criteria

### Research Phase (WI-008a, WI-008b, WI-008c)

- [ ] AC-008.R1: Existing Jerry codebase patterns documented
- [ ] AC-008.R2: DDD patterns for hierarchical config researched
- [ ] AC-008.R3: Skill/agent structure analyzed

### Design Phase (WI-008d, WI-008e, WI-008f, WI-008g)

- [ ] AC-008.D1: JerryFramework aggregate designed with ADR
- [ ] AC-008.D2: JerryProject aggregate designed with ADR
- [ ] AC-008.D3: JerrySkill aggregate designed with ADR
- [ ] AC-008.D4: JerrySession context designed with ADR
- [ ] AC-008.D5: Value objects defined (ProjectId, SkillName, etc.)
- [ ] AC-008.D6: Port interfaces defined (IJerryContext, IConfigurationProvider)
- [ ] AC-008.D7: Configuration resolution order documented

### Validation Phase (WI-008h)

- [ ] AC-008.V1: Design validated against use cases
- [ ] AC-008.V2: Design validated against existing patterns
- [ ] AC-008.V3: Design reviewed for extensibility

---

## Sub-Work Items

This work item is decomposed into sub-items for parallel execution:

| Sub-WI | Title | Type | Agent | Status |
|--------|-------|------|-------|--------|
| [WI-008a](wi-008a-codebase-analysis.md) | Analyze existing Jerry codebase | Research | ps-researcher | PENDING |
| [WI-008b](wi-008b-ddd-patterns.md) | Research DDD hierarchical patterns | Research | ps-researcher | PENDING |
| [WI-008c](wi-008c-skill-structure.md) | Analyze skill/agent structure | Research | ps-researcher | PENDING |
| [WI-008d](wi-008d-framework-aggregate.md) | Design JerryFramework aggregate | Design | ps-architect | PENDING |
| [WI-008e](wi-008e-project-aggregate.md) | Design JerryProject aggregate | Design | ps-architect | PENDING |
| [WI-008f](wi-008f-skill-aggregate.md) | Design JerrySkill aggregate | Design | ps-architect | PENDING |
| [WI-008g](wi-008g-session-context.md) | Design JerrySession context | Design | ps-architect | PENDING |
| [WI-008h](wi-008h-design-validation.md) | Validate domain design | Validation | ps-validator | PENDING |

---

## Entity Hierarchy

```
┌─────────────────────────────────────────────────────────────────────┐
│                        JerryFramework                                │
│  Location: / (repo root)                                            │
│  Config: .jerry/config.toml                                         │
│  Owns: Projects[], Skills[], GlobalSettings                         │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌───────────────────────────┐    ┌───────────────────────────┐   │
│  │      JerryProject         │    │       JerrySkill          │   │
│  │  Location: projects/PROJ-*│    │  Location: skills/*       │   │
│  │  Config: .jerry/config    │    │  Config: SKILL.md/config  │   │
│  │  Owns: WorkItems, Plan,   │    │  Owns: Agents[], Templates│   │
│  │        Worktracker        │    │                           │   │
│  └───────────────────────────┘    └───────────────────────────┘   │
│                                                                     │
│  ┌───────────────────────────┐                                     │
│  │      JerrySession         │  (Runtime, gitignored)              │
│  │  Location: .jerry/local/  │                                     │
│  │  Tracks: ActiveProject,   │                                     │
│  │          WorktreeContext  │                                     │
│  └───────────────────────────┘                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Proposed Domain Model

### Aggregates

```python
# JerryFramework - Root aggregate
class JerryFramework:
    root_path: Path
    config: FrameworkConfig

    def list_projects(self) -> list[ProjectInfo]: ...
    def get_project(self, project_id: ProjectId) -> JerryProject | None: ...
    def list_skills(self) -> list[SkillInfo]: ...
    def get_skill(self, skill_name: SkillName) -> JerrySkill | None: ...

# JerryProject - Project aggregate
class JerryProject:
    project_id: ProjectId
    path: Path
    config: ProjectConfig
    framework: JerryFramework  # Parent reference

    def get_worktracker_path(self) -> Path: ...
    def get_plan_path(self) -> Path: ...
    def get_work_items_path(self) -> Path: ...

# JerrySkill - Skill aggregate
class JerrySkill:
    skill_name: SkillName
    path: Path
    config: SkillConfig

    def list_agents(self) -> list[AgentInfo]: ...
    def get_output_path(self, project: JerryProject | None) -> Path: ...

# JerrySession - Runtime context
class JerrySession:
    framework: JerryFramework
    active_project: JerryProject | None
    worktree_info: WorktreeInfo | None

    def get_config(self, key: str) -> Any | None: ...  # Full resolution
```

### Value Objects

```python
@dataclass(frozen=True, slots=True)
class ProjectId:
    value: str  # "PROJ-001-plugin-cleanup"

    @property
    def number(self) -> int: ...

    @property
    def slug(self) -> str: ...

@dataclass(frozen=True, slots=True)
class SkillName:
    value: str  # "worktracker", "problem-solving"

@dataclass(frozen=True, slots=True)
class ConfigKey:
    value: str  # "logging.level"

    def to_env_key(self, prefix: str = "JERRY_") -> str: ...
```

### Port Interfaces

```python
# Primary port - Main entry point
class IJerryContext(Protocol):
    @property
    def framework(self) -> JerryFramework: ...

    @property
    def session(self) -> JerrySession: ...

    @property
    def active_project(self) -> JerryProject | None: ...

    def list_projects(self) -> list[ProjectInfo]: ...
    def list_skills(self) -> list[SkillInfo]: ...

    def get_config(self, key: str) -> Any | None: ...

# Secondary port - Raw config access (internal use)
class IConfigurationLoader(Protocol):
    def load(self, path: Path) -> dict[str, Any]: ...
    def save(self, path: Path, data: dict[str, Any]) -> None: ...
```

---

## Configuration Resolution Order

```
┌─────────────────────────────────────────────────────────────────┐
│                    Configuration Resolution                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Priority 1: Environment Variables (JERRY_*)                   │
│       ↓                                                         │
│  Priority 2: Session Local (.jerry/local/context.toml)         │
│       ↓                                                         │
│  Priority 3: Project Config (projects/PROJ-*/.jerry/config)    │
│       ↓                                                         │
│  Priority 4: Framework Config (.jerry/config.toml)             │
│       ↓                                                         │
│  Priority 5: Code Defaults                                      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Use Cases to Validate

| Use Case | Current Gap | Solution |
|----------|-------------|----------|
| Session Start | Can't list projects | `framework.list_projects()` |
| Skill Invocation | No project context | `session.active_project` |
| Work Tracker | Ambiguous path resolution | `project.get_work_items_path()` |
| Multi-Worktree | No worktree awareness | `session.worktree_info` |
| Config Override | No hierarchy | 5-layer resolution |

---

## Agent Usage Plan

### Phase 1: Research (Parallel)

```
┌────────────────┐  ┌────────────────┐  ┌────────────────┐
│ ps-researcher  │  │ ps-researcher  │  │ ps-researcher  │
│ WI-008a        │  │ WI-008b        │  │ WI-008c        │
│ Codebase       │  │ DDD Patterns   │  │ Skill/Agent    │
│ Analysis       │  │ Research       │  │ Structure      │
└────────────────┘  └────────────────┘  └────────────────┘
        │                   │                   │
        └───────────────────┼───────────────────┘
                            │
                            ▼
                    ┌──────────────┐
                    │ ps-synthesizer│
                    │ Combine       │
                    │ Findings      │
                    └──────────────┘
```

### Phase 2: Design (Sequential with dependencies)

```
                    Research Synthesis
                            │
            ┌───────────────┼───────────────┐
            │               │               │
            ▼               ▼               ▼
    ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
    │ ps-architect │ │ ps-architect │ │ ps-architect │
    │ WI-008d      │ │ WI-008e      │ │ WI-008f      │
    │ Framework    │ │ Project      │ │ Skill        │
    │ ADR          │ │ ADR          │ │ ADR          │
    └──────────────┘ └──────────────┘ └──────────────┘
            │               │               │
            └───────────────┼───────────────┘
                            │
                            ▼
                    ┌──────────────┐
                    │ ps-architect │
                    │ WI-008g      │
                    │ Session ADR  │
                    └──────────────┘
```

### Phase 3: Validation

```
                    All ADRs Complete
                            │
                            ▼
                    ┌──────────────┐
                    │ ps-validator │
                    │ WI-008h      │
                    │ Validate     │
                    │ Against Use  │
                    │ Cases        │
                    └──────────────┘
```

---

## Blocking Reason

This work item **BLOCKS** all implementation work:

- WI-009, WI-010, WI-011 → Need entity definitions
- WI-012, WI-013, WI-014 → Need port interfaces
- WI-015, WI-016 → Need context model

---

## Progress Log

| Timestamp | Update | Actor |
|-----------|--------|-------|
| 2026-01-12T11:00:00Z | Work item created (flat design) | Claude |
| 2026-01-12T12:00:00Z | Redesigned for hierarchical model | Claude |
| 2026-01-12T12:00:00Z | Decomposed into 8 sub-work items | Claude |

---

## Dependencies

| Type | Work Item | Relationship |
|------|-----------|--------------|
| Depends On | WI-007 | Plan must exist |
| Contains | WI-008a through WI-008h | Sub-work items |
| Blocks | WI-009 through WI-018 | All implementation |

---

## Related Artifacts

- **Plan Reference**: [PLAN.md](../PLAN.md) (needs update after design)
- **Architecture Standards**: [.claude/rules/architecture-standards.md](../../../../.claude/rules/architecture-standards.md)
- **Problem-Solving Skill**: [skills/problem-solving/SKILL.md](../../../../skills/problem-solving/SKILL.md)
