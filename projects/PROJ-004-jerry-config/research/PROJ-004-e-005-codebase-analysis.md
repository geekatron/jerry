# PROJ-004-e-005: Jerry Codebase Analysis

> **PS ID:** PROJ-004
> **Entry ID:** e-005
> **Topic:** Jerry Codebase Analysis
> **Agent:** ps-researcher
> **Created:** 2026-01-12
> **Status:** COMPLETED

---

## L0: Executive Summary

Jerry already has a well-structured hexagonal architecture with:
- **ProjectId** value object with PROJ-NNN-slug validation
- **ProjectInfo** entity for project metadata
- **IProjectRepository** port with FilesystemProjectAdapter
- **IEnvironmentProvider** port for env var access
- **Event sourcing** infrastructure (DomainEvent, EventRegistry, FileSystemEventStore)
- **CQRS** pattern with QueryDispatcher and CommandDispatcher
- **Composition Root** in bootstrap.py

**Key Gap:** No configuration hierarchy - currently flat key-value via env vars only.

---

## L1: Technical Implementation Details

### 1. Project Structure

#### Discovery Mechanism
Projects are discovered via `FilesystemProjectAdapter.scan_projects()`:

```python
# src/session_management/infrastructure/adapters/filesystem_project_adapter.py:33
def scan_projects(self, base_path: str) -> list[ProjectInfo]:
    """Scan the base path for available projects."""
    projects_dir = Path(base_path)
    for item in projects_dir.iterdir():
        if PROJECT_DIR_PATTERN.match(item.name):
            project_id = ProjectId.parse(item.name)
            project_info = self._read_project_info(item, project_id)
            projects.append(project_info)
```

#### Valid Project Pattern
```python
# src/session_management/infrastructure/adapters/filesystem_project_adapter.py:23
PROJECT_DIR_PATTERN = re.compile(r"^PROJ-\d{3}-[a-z][a-z0-9]*(?:-[a-z0-9]+)*$")
```

#### ProjectId Value Object
```python
# src/session_management/domain/value_objects/project_id.py:36
@dataclass(frozen=True)
class ProjectId(VertexId):
    """Format: PROJ-{nnn}-{slug} where nnn is 001-999 and slug is kebab-case."""
    _PATTERN: ClassVar[Pattern[str]] = re.compile(r"^PROJ-(\d{3})-([a-z][a-z0-9]*(?:-[a-z0-9]+)*)$")

    @property
    def number(self) -> int:
        return int(self._PATTERN.match(self.value).group(1))

    @property
    def slug(self) -> str:
        return self._PATTERN.match(self.value).group(2)
```

#### Project Configuration
- **Current:** No project-level config.toml
- **Status read from:** WORKTRACKER.md header (first 2KB scanned for keywords)
- **Location:** `projects/PROJ-NNN-slug/WORKTRACKER.md`

#### Active Project Determination
```python
# src/interface/cli/session_start.py:37
def get_projects_directory() -> str:
    project_root = os.environ.get("CLAUDE_PROJECT_DIR")
    if project_root:
        return str(Path(project_root) / "projects")
    return str(Path.cwd() / "projects")
```

Active project set via `JERRY_PROJECT` environment variable.

### 2. Session/Context Management

#### IEnvironmentProvider Port
```python
# src/session_management/application/ports/environment.py:13
class IEnvironmentProvider(Protocol):
    def get_env(self, name: str) -> str | None: ...
    def get_env_or_default(self, name: str, default: str) -> str: ...
```

#### OsEnvironmentAdapter
```python
# src/session_management/infrastructure/adapters/os_environment_adapter.py
class OsEnvironmentAdapter:
    def get_env(self, name: str) -> str | None:
        value = os.environ.get(name)
        return value if value else None
```

#### Session Aggregate
```python
# src/session_management/domain/aggregates/session.py
class Session(AggregateRoot):
    """Session aggregate tracking CLI session state."""
    # Events: SessionCreated, SessionEnded, SessionAbandoned
```

#### ProjectInfo Entity
```python
# src/session_management/domain/entities/project_info.py:33
@dataclass(frozen=True, slots=True)
class ProjectInfo:
    id: ProjectId
    status: ProjectStatus = ProjectStatus.UNKNOWN
    has_plan: bool = False
    has_tracker: bool = False
    path: str | None = None
    session_id: str | None = None
```

### 3. Current Configuration Handling

#### Environment Variables Used
| Variable | Purpose | Source |
|----------|---------|--------|
| `JERRY_PROJECT` | Active project ID | User-set |
| `CLAUDE_PROJECT_DIR` | Project root path | Claude Code |

#### Configuration Sources
1. Environment variables (only source currently)
2. Hard-coded defaults in code

#### No TOML/JSON Config Files
- No `.jerry/config.toml` at framework level
- No `projects/PROJ-*/config.toml` at project level
- Configuration is flat, not hierarchical

### 4. Event Sourcing Patterns

#### DomainEvent Base Class
```python
# src/shared_kernel/domain_event.py:39
@dataclass(frozen=True)
class DomainEvent:
    aggregate_id: str
    aggregate_type: str
    event_id: str = field(default_factory=_generate_event_id)
    timestamp: datetime = field(default_factory=_current_timestamp)
    version: int = 1

    def to_dict(self) -> dict[str, Any]: ...
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> DomainEvent: ...
```

#### EventRegistry for Polymorphic Deserialization
```python
# src/shared_kernel/domain_event.py:164
class EventRegistry:
    def register(self, event_class: type[DomainEvent]) -> type[DomainEvent]: ...
    def deserialize(self, data: dict[str, Any]) -> DomainEvent: ...
```

#### WorkItem Aggregate (Example)
```python
# src/work_tracking/domain/aggregates/work_item.py:81
class WorkItem(AggregateRoot):
    @classmethod
    def create(cls, id: WorkItemId, title: str, ...) -> WorkItem:
        item = cls.__new__(cls)
        item._initialize(str(id.internal_id))
        event = WorkItemCreated(...)
        item._raise_event(event)
        return item

    @classmethod
    def load_from_history(cls, events: Sequence[DomainEvent]) -> WorkItem:
        """Reconstruct by replaying events."""
        item = cls.__new__(cls)
        for event in events:
            item._apply(event)
        return item
```

#### FileSystemEventStore
```python
# src/work_tracking/infrastructure/persistence/filesystem_event_store.py
class FileSystemEventStore:
    """Stores events in JSONL files per aggregate stream."""
    # Location: projects/PROJ-NNN-slug/.jerry/data/events/
```

### 5. Composition Root (bootstrap.py)

Key patterns:
```python
# src/bootstrap.py:302
def create_query_dispatcher() -> QueryDispatcher:
    # Create infrastructure adapters
    project_repository = FilesystemProjectAdapter()
    environment = OsEnvironmentAdapter()

    # Create handlers with injected dependencies
    handler = RetrieveProjectContextQueryHandler(
        repository=project_repository,
        environment=environment,
    )

    # Configure dispatcher
    dispatcher = QueryDispatcher()
    dispatcher.register(RetrieveProjectContextQuery, handler.handle)
    return dispatcher
```

---

## L2: Strategic Implications for Domain Model

### Existing Patterns to Preserve

| Pattern | Location | Implication for PROJ-004 |
|---------|----------|--------------------------|
| ProjectId value object | `domain/value_objects/` | Use as SkillName, ConfigKey template |
| IRepository port | `domain/ports/` | Define IConfigurationRepository |
| FilesystemAdapter | `infrastructure/adapters/` | Create TomlConfigAdapter |
| Composition Root | `bootstrap.py` | Wire JerrySession here |
| EventRegistry | `shared_kernel/` | Consider ConfigChanged events |

### Gaps Requiring New Design

| Gap | Current State | Required |
|-----|---------------|----------|
| Framework Aggregate | None | JerryFramework as root aggregate |
| Project Aggregate | ProjectInfo (entity) | JerryProject (aggregate with config) |
| Skill Aggregate | SKILL.md files only | JerrySkill with agent navigation |
| Session Context | Session (limited) | JerrySession with config resolution |
| Config Hierarchy | Flat env vars | 5-level precedence |
| Config Files | None | TOML at framework/project levels |

### File Locations Identified

| Entity | Config Location | Runtime Location |
|--------|-----------------|------------------|
| Framework | `.jerry/config.toml` | Loaded at bootstrap |
| Project | `projects/PROJ-*/config.toml` | Loaded on activation |
| Session | `.jerry/local/context.toml` | Persistent per worktree |
| Skill | `skills/*/config.toml` | Loaded on invocation |

---

## Evidence Summary

| Finding | Evidence Source |
|---------|-----------------|
| ProjectId validation regex | `project_id.py:58` |
| Project discovery via glob | `filesystem_project_adapter.py:58` |
| Env var access port | `environment.py:13` |
| Event sourcing pattern | `domain_event.py`, `work_item.py:685` |
| Composition root pattern | `bootstrap.py:302` |
| No config files | Grep for `.toml` returns no domain config |

---

## Recommendations

1. **Extend ProjectInfo → JerryProject aggregate** with configuration
2. **Create JerryFramework aggregate** as entry point
3. **Use IEnvironmentProvider** for env var layer in config resolution
4. **Follow FilesystemProjectAdapter pattern** for TomlConfigAdapter
5. **Extend bootstrap.py** to create JerrySession at startup
