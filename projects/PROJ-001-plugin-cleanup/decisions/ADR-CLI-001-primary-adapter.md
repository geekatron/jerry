# ADR-CLI-001: Jerry CLI Primary Adapter Architecture

> **Status:** PROPOSED
> **Date:** 2026-01-12
> **Decision Makers:** Claude, User
> **Related:** TD-014, DISC-006, DISC-007

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

**Use factory pattern for dependency wiring:**

```python
# src/interface/cli/main.py

def create_project_context_query(base_path: str) -> GetProjectContextQuery:
    """Factory for GetProjectContextQuery with dependencies."""
    return GetProjectContextQuery(
        repository=FilesystemProjectAdapter(),
        environment=OsEnvironmentAdapter(),
        base_path=base_path,
    )
```

**Rationale:** Follows the pattern established in `session_start.py`. Centralizes dependency creation and enables testing via dependency injection.

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

**Support two output modes:**

| Mode | Flag | Purpose |
|------|------|---------|
| Human | (default) | Readable terminal output |
| Machine | `--json` | JSON for scripting/automation |

**Rationale:** Human mode for interactive use; JSON mode for integration with other tools and scripts.

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
