# ADR-CLI-001: Jerry CLI Primary Adapter Architecture

> **Status:** SUPERSEDED (D2 REJECTED - See Amendment 2026-01-12)
> **Date:** 2026-01-12
> **Decision Makers:** Claude, User
> **Related:** TD-014, DISC-006, DISC-007, BUG-006

---

## Amendment (2026-01-12)

**D2 (Factory Composition Root) is REJECTED.** The original decision used "Poor Man's DI" pattern where the adapter wires dependencies directly. This is NOT acceptable per user requirements.

**Required Changes:**
- Adapters MUST NOT instantiate infrastructure adapters
- Adapters MUST receive pre-wired dispatcher via injection
- Composition root MUST be external to adapters (e.g., `src/bootstrap.py`)
- See `docs/design/PYTHON-ARCHITECTURE-STANDARDS.md` for correct patterns

**Related:** BUG-006 (CLI Adapter Bypasses Application Layer) confirms this violation.

---

## Context

The Jerry framework defines a CLI entry point in `pyproject.toml` that references a non-existent file:

```toml
[project.scripts]
jerry = "src.interface.cli.main:main"  # DOES NOT EXIST
```

This blocks package installation and prevents Jerry from being used as intended. We need to implement a CLI that:

1. Fixes the broken entry point (DISC-006)
2. Follows hexagonal architecture principles
3. Provides a minimal viable interface for v0.0.1
4. Is extensible for future commands

### Research Summary

| Source | Key Finding |
|--------|-------------|
| TD-014.R1 | 4 Queries exist, 0 Commands - limited to project management |
| TD-014.R2 | Domain has 2 aggregates (WorkItem, Session) but no app layer commands |
| TD-014.R3 | Factory composition pattern validated; session_start.py is reference |

---

## Decision

### D1: Minimal CLI for v0.0.1

**Implement 5 commands for v0.0.1:**

| Command | Implementation |
|---------|----------------|
| `jerry --help` | argparse built-in |
| `jerry --version` | Version from pyproject.toml |
| `jerry init` | Calls `GetProjectContextQuery` |
| `jerry projects list` | Calls `ScanProjectsQuery` |
| `jerry projects validate <id>` | Calls `ValidateProjectQuery` |

**Rationale:** Only these commands have corresponding use cases in the application layer. Work tracking commands are deferred to v0.0.2.

### D2: Factory Composition Root

> **⚠️ REJECTED (2026-01-12)** - This decision is superseded. The pattern below is NOT acceptable.

~~**Use factory pattern for dependency wiring:**~~

```python
# WRONG - "Poor Man's DI" pattern (REJECTED)
# src/interface/cli/main.py

def create_project_context_query(base_path: str) -> GetProjectContextQuery:
    """Factory for GetProjectContextQuery with dependencies."""
    return GetProjectContextQuery(
        repository=FilesystemProjectAdapter(),  # VIOLATION: Adapter wires dependencies
        environment=OsEnvironmentAdapter(),      # VIOLATION: Direct instantiation
        base_path=base_path,
    )
```

~~**Rationale:** Follows the pattern established in `session_start.py`. Centralizes dependency creation and enables testing via dependency injection.~~

### D2-AMENDED: Dispatcher Pattern with External Composition Root

**Use Dispatcher pattern with dependency injection:**

```python
# CORRECT - External composition root (src/bootstrap.py)
def create_application() -> CLIAdapter:
    """Wire all dependencies at application startup."""
    repository = FilesystemProjectAdapter()
    environment = OsEnvironmentAdapter()

    handlers = {
        GetProjectContextQuery: GetProjectContextHandler(repository, environment),
        ScanProjectsQuery: ScanProjectsHandler(repository),
    }

    dispatcher = QueryDispatcher(handlers)
    return CLIAdapter(dispatcher)


# CORRECT - Adapter receives dispatcher (src/interface/cli/main.py)
class CLIAdapter:
    def __init__(self, dispatcher: IQueryDispatcher) -> None:
        self._dispatcher = dispatcher

    def cmd_init(self, args: argparse.Namespace) -> int:
        query = GetProjectContextQuery(base_path=get_projects_directory())
        context = self._dispatcher.dispatch(query)  # Via dispatcher, not direct
        return format_output(args, context)
```

**Rationale:** Clean Architecture requires adapters to be thin and receive dependencies via injection. The composition root is external to all adapters.

### D3: Zero-Dependency Core

**Use only Python stdlib in CLI:**

| Allowed | Not Allowed |
|---------|-------------|
| `argparse` | `click`, `typer` |
| `sys`, `os` | `rich`, `colorama` |
| `pathlib` | External formatters |

**Rationale:** Aligns with Jerry's zero-dependency core principle. CLI is a primary adapter that should be thin and simple.

### D4: Command Routing Architecture

**Use subcommand pattern with argparse:**

```
jerry
├── init                    # Direct command
└── projects                # Command group
    ├── list
    └── validate <id>
```

**Rationale:** Hierarchical structure allows future expansion (session, items) without breaking existing commands.

### D5: Output Format

> **⚠️ AMENDED (2026-01-12)** - Added TOON as primary format for LLM consumption.

**Support three output modes:**

| Mode | Flag | Purpose | Priority |
|------|------|---------|----------|
| TOON | `--toon` (default) | Token-efficient for LLM consumption | PRIMARY |
| JSON | `--json` | Machine-readable structured data | SECONDARY |
| Human | `--human` | Readable terminal output | TERTIARY |

**Rationale:** Token efficiency is paramount. TOON reduces token usage by 30-60% for tabular data. See `projects/archive/research/TOON_FORMAT_ANALYSIS.md` for benchmarks.

**Implementation:**
```bash
jerry projects list              # Default: TOON output
jerry --toon projects list       # Explicit TOON
jerry --json projects list       # JSON output
jerry --human projects list      # Human-readable tables
```

### D6: CLI Namespaces per Bounded Context (NEW)

**Each bounded context gets its own CLI subcommand namespace:**

```bash
jerry session <command>          # Session Management bounded context
jerry worktracker <command>      # Work Tracker bounded context
jerry projects <command>         # Project Management bounded context
```

**Rationale:** This mirrors:
- **Bounded Contexts**: Each namespace maps to a distinct domain
- **Authorization Scopes**: Security boundaries align with namespaces
- **Threat Models**: Attack surface isolation per bounded context
- **Use Case Ports**: Each namespace routes to a distinct application service

**Architecture:**
```
CLI Command → Use Case (Application Service) → Domain
     │
     ├── jerry session → ISessionManagementPort
     ├── jerry worktracker → IWorkTrackerPort
     └── jerry projects → IProjectManagementPort
```

**Rules:**
1. CLI is a Primary Adapter - translates user intent to use case invocation
2. CLI NEVER contains business logic
3. CLI NEVER knows infrastructure details
4. Routing is pure orchestration, not logic
5. CLI structure reflects actor intent, not domain structure

---

## Consequences

### Positive

1. **Package installable:** `pip install -e .` will work
2. **Regression-free:** No changes to existing behavior
3. **Extensible:** Command groups allow future expansion
4. **Testable:** Factory pattern enables dependency injection
5. **Compliant:** Follows hexagonal architecture principles

### Negative

1. **Limited v0.0.1 scope:** Only project commands available
2. **No work tracking:** Must wait for application layer commands
3. **Plain output:** No rich formatting (no external deps)

### Neutral

1. **Learning curve:** Users may expect more commands
2. **Documentation needed:** Must explain what's available

---

## Implementation Plan

### Phase 1: Core Infrastructure

1. Create `src/interface/cli/main.py` with:
   - `main()` entry point
   - Argument parser setup
   - Command routing

2. Create `src/interface/cli/commands/` with:
   - `__init__.py` (command registry)
   - `init.py` (init command)
   - `projects.py` (projects subcommand)

### Phase 2: Command Implementation

1. `jerry init`:
   - Call `GetProjectContextQuery`
   - Format output (human/json)
   - Return exit code

2. `jerry projects list`:
   - Call `ScanProjectsQuery`
   - Format as table/json
   - Return exit code

3. `jerry projects validate`:
   - Parse project ID argument
   - Call `ValidateProjectQuery`
   - Format validation result
   - Return exit code (0=valid, 1=invalid)

### Phase 3: Testing

| Test Type | Focus |
|-----------|-------|
| Unit | Command handlers, argument parsing |
| Integration | Factory composition, query execution |
| Architecture | Layer boundary compliance |

---

## Alternatives Considered

### A1: Use Click/Typer Library

**Rejected.** Violates zero-dependency core principle. Would add external dependency to interface layer.

### A2: Implement All Commands Now

**Rejected.** Application layer lacks commands for WorkItem and Session. Would require implementing entire CQRS command infrastructure.

### A3: Defer CLI to v0.0.2

**Rejected.** Broken entry point blocks package installation. Must fix for v0.0.1.

---

## Validation Criteria

| Criterion | Test |
|-----------|------|
| Entry point works | `pip install -e . && jerry --help` |
| Init command works | `jerry init` shows project context |
| Projects list works | `jerry projects list` shows available projects |
| Projects validate works | `jerry projects validate PROJ-001-plugin-cleanup` |
| JSON output works | `jerry --json projects list` |
| Exit codes correct | `jerry projects validate invalid-id; echo $?` returns 1 |

---

## References

- TD-014.R1: `research/td-014-e-011-use-case-inventory.md`
- TD-014.R2: `research/td-014-e-012-domain-capabilities.md`
- TD-014.R3: `research/td-014-e-013-knowledge-base-patterns.md`
- TD-014.A1: `analysis/td-014-a-001-cli-gap-analysis.md`
- DISC-006: Broken CLI entry point
- DISC-007: Distribution model clarification
- Teaching Edition: `docs/knowledge/exemplars/architecture/work_tracker_architecture_hexagonal_ddd_cqrs_layered_teaching_edition.md`

---

## Approval

| Role | Name | Date | Status |
|------|------|------|--------|
| Author | Claude | 2026-01-12 | PROPOSED |
| Reviewer | User | - | PENDING |
