# WI-008g: Design JerrySession Context

| Field | Value |
|-------|-------|
| **ID** | WI-008g |
| **Title** | Design JerrySession context |
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

Design the JerrySession context - the runtime context that tracks the active project, worktree state, and provides configuration resolution with full precedence.

---

## Agent Invocation

### ps-architect Prompt

```
You are the ps-architect agent (v2.0.0).

## PS CONTEXT (REQUIRED)
- **PS ID:** PROJ-004
- **Entry ID:** e-011
- **Topic:** JerrySession Context Design

## MANDATORY PERSISTENCE (P-002)
Create ADR at: projects/PROJ-004-jerry-config/decisions/ADR-PROJ004-004-jerry-session-context.md

## DESIGN TASK

Design the JerrySession context using Nygard ADR format.

### Context
JerrySession is the runtime context that:
- Tracks the currently active project
- Tracks worktree information (if in a worktree)
- Provides configuration resolution with full precedence
- Persists to `.jerry/local/context.toml` (gitignored)
- Is worktree-specific (each worktree has its own session)

### Design Requirements
1. Must track active project (mutable)
2. Must detect git worktree context
3. Must resolve configuration with 5-level precedence
4. Must persist local state atomically
5. Must be reconstructible from local state

### Configuration Precedence
1. Environment Variables (JERRY_*)
2. Session Local (.jerry/local/context.toml)
3. Project Config (projects/PROJ-*/.jerry/config.toml)
4. Framework Config (.jerry/config.toml)
5. Code Defaults

### Questions to Answer
1. Is JerrySession an aggregate, entity, or service?
2. How to detect git worktree context?
3. What state should be persisted vs transient?
4. How to handle missing/corrupted local state?
5. Should session emit events for state changes?

### Key Use Cases
- Session start: Load context, determine active project
- Project switch: Update context, persist
- Config get: Resolve with full precedence
- Worktree detection: Identify worktree branch/path

### Inputs (from research)
- WI-008a findings on current context handling
- WI-008b findings on session patterns
- WI-008d, WI-008e, WI-008f for entity references

### Constraints
- Must follow hexagonal architecture
- Local state is gitignored
- Must support atomic updates

## ADR STRUCTURE
Use Nygard format with:
- Title, Status, Context
- Decision with code examples
- Consequences (positive, negative, neutral)
- L0/L1/L2 explanation levels
```

---

## Acceptance Criteria

- [ ] AC-008g.1: ADR created with Nygard format
- [ ] AC-008g.2: JerrySession class interface defined
- [ ] AC-008g.3: Active project tracking specified
- [ ] AC-008g.4: Worktree detection mechanism defined
- [ ] AC-008g.5: Configuration resolution documented
- [ ] AC-008g.6: Local state persistence designed
- [ ] AC-008g.7: State reconstruction logic specified

---

## Proposed Interface (Draft)

```python
@dataclass(frozen=True)
class WorktreeInfo:
    """Information about git worktree context."""
    is_worktree: bool
    branch: str | None
    main_worktree_path: Path | None


class JerrySession:
    """Runtime session context."""

    def __init__(
        self,
        framework: JerryFramework,
        local_path: Path,
    ) -> None:
        ...

    @property
    def framework(self) -> JerryFramework: ...

    @property
    def active_project(self) -> JerryProject | None: ...

    @property
    def worktree_info(self) -> WorktreeInfo: ...

    # Project context management
    def set_active_project(self, project_id: ProjectId) -> None:
        """Set active project and persist to local state."""
        ...

    def clear_active_project(self) -> None:
        """Clear active project from context."""
        ...

    # Configuration resolution (full precedence)
    def get_config(self, key: str) -> Any | None:
        """
        Resolve configuration with 5-level precedence:
        1. Env vars (JERRY_*)
        2. Local context
        3. Project config
        4. Framework config
        5. Defaults
        """
        ...

    def get_config_string(self, key: str, default: str = "") -> str: ...
    def get_config_bool(self, key: str, default: bool = False) -> bool: ...
    def get_config_int(self, key: str, default: int = 0) -> int: ...

    # Persistence
    def _load_local_state(self) -> dict[str, Any]: ...
    def _save_local_state(self) -> None: ...
```

---

## Local State Format

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

---

## Evidence

| Criterion | Evidence | Source |
|-----------|----------|--------|
| AC-008g.1 | - | - |
| AC-008g.2 | - | - |
| AC-008g.3 | - | - |
| AC-008g.4 | - | - |
| AC-008g.5 | - | - |
| AC-008g.6 | - | - |
| AC-008g.7 | - | - |

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
| Depends On | WI-008d, WI-008e, WI-008f | Entity designs must complete |
| Blocks | WI-008h | Validation needs session |

---

## Related Artifacts

- **Output**: `decisions/ADR-PROJ004-004-jerry-session-context.md`
- **Research Input**: All research artifacts
