# TD-001: cli/session_start.py Violates Hexagonal Architecture

> **Type:** Technical Debt
> **Feature:** [FT-001](./FEATURE-WORKTRACKER.md) Session Hook Cleanup
> **Solution Epic:** [SE-004](../SOLUTION-WORKTRACKER.md) CLI and Claude Code Integration
> **Project:** PROJ-007-jerry-bugs
> **Status:** DOCUMENTED
> **Severity:** HIGH
> **Created:** 2026-01-15
> **Last Updated:** 2026-01-15

---

## Description

The file `src/interface/cli/session_start.py` contains direct infrastructure imports, violating the hexagonal architecture principle that interface adapters should not depend on infrastructure.

## Evidence

**Direct Infrastructure Imports (lines 53-60):**
```python
from src.infrastructure.adapters.configuration.layered_config_adapter import (
    LayeredConfigAdapter,
)
from src.infrastructure.adapters.persistence.atomic_file_adapter import (
    AtomicFileAdapter,
)
from src.session_management.application import GetProjectContextQuery
from src.session_management.infrastructure import FilesystemProjectAdapter, OsEnvironmentAdapter
```

## Impact

1. **Testability** - Cannot unit test without infrastructure dependencies
2. **Maintainability** - Changes to infrastructure require changes to interface layer
3. **Architecture Erosion** - Sets bad precedent for other developers
4. **Coupling** - Tight coupling between interface and infrastructure layers

## Proper Architecture

The interface layer should:
1. Depend ONLY on application layer (queries, commands, DTOs)
2. Receive infrastructure adapters via dependency injection
3. Use the dispatcher pattern for routing

**Correct Pattern (from `cli/main.py`):**
```python
from src.bootstrap import create_query_dispatcher
from src.interface.cli.adapter import CLIAdapter

def main() -> int:
    adapter = create_cli_adapter()  # Composition root handles wiring
    # ... route commands through adapter
```

## Resolution

1. Move business logic to `CLIAdapter`
2. Add hook-specific output format support to adapter
3. Remove direct infrastructure imports
4. Delete `cli/session_start.py` after migration

## Related Artifacts

| Type | Location | Description |
|------|----------|-------------|
| Enabler | [en-001-session-hook-tdd.md](./en-001-session-hook-tdd.md) | TDD cleanup work |
| Source | `src/interface/cli/session_start.py` | Violating file |
| Proper Pattern | `src/interface/cli/main.py` | Correct architecture |
| Architecture Rules | `.claude/rules/architecture-standards.md` | Layer boundary rules |

---

## Change Log

| Date | Change | Author |
|------|--------|--------|
| 2026-01-15 | Technical debt documented | Claude |
