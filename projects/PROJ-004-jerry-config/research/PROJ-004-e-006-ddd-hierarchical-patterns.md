# PROJ-004-e-006: DDD Hierarchical Configuration Patterns

> **PS ID:** PROJ-004
> **Entry ID:** e-006
> **Topic:** DDD Hierarchical Configuration Patterns
> **Agent:** ps-researcher
> **Created:** 2026-01-12
> **Status:** COMPLETED

---

## L0: Executive Summary

For Jerry's hierarchical configuration needs:
- **Use separate aggregates** for Framework, Project, and Skill (each has its own lifecycle)
- **Child holds parent reference** for navigation (JerryProject → JerryFramework)
- **Configuration is a Value Object** (immutable snapshot), not an entity
- **JerrySession is a runtime context** (like HttpContext), not an aggregate
- **Use Chain of Responsibility** for layered configuration resolution

---

## L1: Technical Implementation Details

### 1. Aggregate Relationships

#### Pattern: Parent Reference vs ID-Only

**Option A: Direct Parent Reference**
```python
class JerryProject:
    def __init__(self, project_id: ProjectId, path: Path, framework: JerryFramework):
        self._project_id = project_id
        self._path = path
        self._framework = framework  # Direct reference

    def get_config(self, key: str) -> Any:
        # Can navigate to parent
        return self._config.get(key) or self._framework.config.get(key)
```

**Option B: ID-Only with Repository Lookup**
```python
class JerryProject:
    def __init__(self, project_id: ProjectId, path: Path, framework_path: Path):
        self._framework_path = framework_path  # ID/path only

    def get_framework_config(self, repository: IFrameworkRepository) -> FrameworkConfig:
        # Requires repository for navigation
        return repository.get_framework(self._framework_path).config
```

**Recommendation: Option A (Direct Parent Reference)**
- Jerry is a single-process CLI tool, not distributed
- Aggregates are loaded together at session start
- Navigation convenience outweighs loose coupling concerns
- Similar to how Git's Repository holds references to Index and WorkTree

#### When to Separate Aggregates

| Criterion | Separate Aggregate | Part of Parent |
|-----------|-------------------|----------------|
| Independent lifecycle | Yes | No |
| Own transactional boundary | Yes | No |
| Can exist without parent | Maybe | No |
| Own persistence stream | Yes | No |

**Jerry Analysis:**
- **JerryProject**: Separate (own config, own work items, own lifecycle)
- **JerrySkill**: Separate (framework-scoped, reusable across projects)
- **ProjectConfig**: Part of JerryProject (no independent lifecycle)

### 2. Configuration in DDD

#### Configuration as Value Object

```python
@dataclass(frozen=True)
class ConfigValue:
    """Immutable configuration value."""
    key: str
    value: Any
    source: str  # "env", "session", "project", "framework", "default"

@dataclass(frozen=True)
class FrameworkConfig:
    """Framework-level configuration snapshot."""
    values: tuple[ConfigValue, ...]

    def get(self, key: str) -> Any | None:
        for cv in self.values:
            if cv.key == key:
                return cv.value
        return None
```

**Why Value Object?**
- Configuration is a snapshot, not an entity with identity
- Immutable - changes create new snapshots
- Equality by value, not reference
- Simpler reasoning about config state

#### Layered Configuration Pattern

**Chain of Responsibility:**
```python
class ConfigResolver:
    """Resolves configuration through precedence chain."""

    def __init__(self, layers: list[ConfigLayer]):
        self._layers = layers  # Ordered by precedence

    def get(self, key: str) -> ConfigValue | None:
        for layer in self._layers:
            value = layer.get(key)
            if value is not None:
                return ConfigValue(key=key, value=value, source=layer.name)
        return None

# Usage in JerrySession
class JerrySession:
    def __init__(self, ...):
        self._resolver = ConfigResolver([
            EnvVarLayer(),           # 1. Highest precedence
            SessionLocalLayer(),      # 2. .jerry/local/
            ProjectConfigLayer(),     # 3. projects/PROJ-*/config.toml
            FrameworkConfigLayer(),   # 4. .jerry/config.toml
            DefaultsLayer(),          # 5. Code defaults
        ])

    def get_config(self, key: str) -> Any | None:
        result = self._resolver.get(key)
        return result.value if result else None
```

#### Configuration vs Infrastructure

| Concern | Layer | Reason |
|---------|-------|--------|
| Config key resolution | Domain | Business logic |
| Precedence rules | Domain | Business invariant |
| TOML parsing | Infrastructure | Technical detail |
| File I/O | Infrastructure | External dependency |

### 3. Context/Session Patterns

#### JerrySession as Runtime Context

**Not an Aggregate because:**
- No domain events
- No persistence of session entity itself
- Transient per CLI invocation
- Holds references to aggregates

**Pattern: Context Object**
```python
class JerrySession:
    """Runtime context for a Jerry CLI session."""

    def __init__(
        self,
        framework: JerryFramework,
        active_project: JerryProject | None,
        worktree_info: WorktreeInfo,
        local_state_path: Path,
    ):
        self._framework = framework
        self._active_project = active_project
        self._worktree_info = worktree_info
        self._local_state = self._load_local_state(local_state_path)
        self._resolver = self._build_resolver()

    @property
    def active_project(self) -> JerryProject | None:
        return self._active_project

    def set_active_project(self, project_id: ProjectId) -> None:
        """Switch active project and persist to local state."""
        self._active_project = self._framework.get_project(project_id)
        self._persist_local_state()
        self._resolver = self._build_resolver()  # Rebuild with new project
```

#### Comparison with ASP.NET Core HttpContext

| ASP.NET Core | Jerry |
|--------------|-------|
| `HttpContext` | `JerrySession` |
| `HttpContext.Request` | `JerrySession.active_project` |
| `HttpContext.User` | `JerrySession.worktree_info` |
| `IConfiguration` | `JerrySession.get_config()` |
| Request-scoped | CLI invocation-scoped |

### 4. Bounded Context Patterns

#### Jerry Context Map

```
┌─────────────────────────────────────────────────────────────────┐
│                        Jerry Framework                          │
├─────────────────────────────────────────────────────────────────┤
│  ┌───────────────────┐         ┌───────────────────┐           │
│  │ session_management│◄───────►│ configuration     │           │
│  │ (existing)        │   SK    │ (new BC)          │           │
│  └─────────┬─────────┘         └─────────┬─────────┘           │
│            │                             │                      │
│            │ SK                          │ SK                   │
│            ▼                             ▼                      │
│  ┌─────────────────────────────────────────────────┐           │
│  │               shared_kernel                      │           │
│  │  - ProjectId, SkillName, ConfigKey              │           │
│  │  - DomainEvent, AggregateRoot                   │           │
│  └─────────────────────────────────────────────────┘           │
└─────────────────────────────────────────────────────────────────┘
```

**Shared Kernel Contents:**
- `ProjectId` value object (already exists)
- `SkillName` value object (new)
- `ConfigKey` value object (new)
- Base classes: `DomainEvent`, `AggregateRoot`, `VertexId`

### 5. Industry Examples

#### Git: Repository → Worktree → Index

| Git Concept | Jerry Equivalent | Relationship |
|-------------|------------------|--------------|
| Repository | JerryFramework | Root aggregate |
| Worktree | JerrySession | Runtime context per worktree |
| Index | Active Project | Current working context |
| Config precedence | Config resolver | local → global → system |

**Git Config Precedence:**
1. `--local` (repo-specific)
2. `--global` (user-specific)
3. `--system` (system-wide)

**Jerry Config Precedence (mapped):**
1. Env vars (session-specific)
2. Local state (worktree-specific)
3. Project config (project-specific)
4. Framework config (repo-specific)
5. Defaults (system-wide)

#### Terraform: Workspace Isolation

| Terraform | Jerry |
|-----------|-------|
| Workspace | Project |
| Module | Skill |
| State file | `.jerry/data/` |
| Backend | FileSystemEventStore |

**Terraform Pattern Applied:**
- Each workspace (project) has isolated state
- Workspaces share module (skill) definitions
- Backend (infrastructure) is configurable per workspace

---

## L2: Strategic Implications

### Recommended Aggregate Structure

```
JerryFramework (Root Aggregate)
├── config: FrameworkConfig (Value Object)
├── projects: list[JerryProject] (Child Aggregates, lazy-loaded)
└── skills: list[JerrySkill] (Child Aggregates, lazy-loaded)

JerryProject (Aggregate)
├── project_id: ProjectId (Value Object)
├── config: ProjectConfig (Value Object)
└── framework: JerryFramework (Parent Reference)

JerrySkill (Aggregate)
├── skill_name: SkillName (Value Object)
├── config: SkillConfig (Value Object)
├── agents: list[AgentInfo] (Value Objects)
└── framework: JerryFramework (Parent Reference)

JerrySession (Runtime Context - NOT Aggregate)
├── framework: JerryFramework
├── active_project: JerryProject | None
├── worktree_info: WorktreeInfo
└── _resolver: ConfigResolver
```

### Configuration Resolution Flow

```
get_config("logging.level")
    │
    ▼
┌─────────────────┐
│  Env: JERRY_    │ ──► JERRY_LOGGING_LEVEL=DEBUG → "DEBUG"
│  LOGGING_LEVEL  │
└────────┬────────┘
         │ (not set)
         ▼
┌─────────────────┐
│ Session Local   │ ──► .jerry/local/context.toml → None
│                 │
└────────┬────────┘
         │ (not set)
         ▼
┌─────────────────┐
│ Project Config  │ ──► projects/PROJ-004/config.toml → "INFO"
│                 │
└────────┬────────┘
         │
         ▼
    Return "INFO" with source="project"
```

### Trade-off Analysis

| Decision | Trade-off | Recommendation |
|----------|-----------|----------------|
| Parent reference vs ID | Convenience vs coupling | Parent reference (CLI is single-process) |
| Config as VO vs Entity | Simplicity vs mutability | Value Object (immutable snapshots) |
| Session as Aggregate | Event sourcing vs simplicity | Runtime Context (no persistence needed) |
| Eager vs lazy loading | Memory vs latency | Lazy loading (scan only on first access) |

---

## Evidence Summary

| Pattern | Source | Applicability |
|---------|--------|---------------|
| Parent reference | Vernon IDDD Ch. 10 | High - single-process |
| Config as Value Object | Evans DDD Ch. 5 | High - immutable state |
| Chain of Responsibility | GoF Design Patterns | High - layered config |
| Context Object | Fowler P of EAA | High - request scope |
| Git config precedence | Git documentation | Direct mapping |

---

## References

1. Evans, Eric. "Domain-Driven Design." Addison-Wesley, 2004. Ch. 5-6 (Aggregates, Value Objects)
2. Vernon, Vaughn. "Implementing Domain-Driven Design." Addison-Wesley, 2013. Ch. 10 (Aggregates)
3. Fowler, Martin. "Patterns of Enterprise Application Architecture." Addison-Wesley, 2002. (Context Object)
4. Git Documentation. "git-config" man page. (Precedence model)
5. Terraform Documentation. "Workspaces" guide. (Isolation pattern)
