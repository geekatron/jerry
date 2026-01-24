# DISC-008: Bootstrap Missing LocalContextReader Wiring

> **Discovery:** Bootstrap.py does not wire LocalContextReader to handler
> **Feature:** [FT-001](./FEATURE-WORKTRACKER.md) Session Hook Cleanup
> **Enabler:** [EN-001](./en-001-session-hook-tdd.md) Session Start Hook TDD Cleanup
> **Status:** DOCUMENTED
> **Type:** Integration Gap
> **Created:** 2026-01-21
> **Discovered During:** EN-001 Phase 2 exploration

---

## Summary

The `RetrieveProjectContextQueryHandler` was updated in Phase 1 to accept an optional `local_context_reader` dependency, but `bootstrap.py` was never updated to wire the `FilesystemLocalContextAdapter`. This means the local context feature (reading `.jerry/local/context.toml`) is implemented but **not connected** in production.

---

## Evidence

### Handler Updated (Phase 1)

`src/application/handlers/queries/retrieve_project_context_query_handler.py`:

```python
def __init__(
    self,
    repository: IProjectRepository,
    environment: IEnvironmentProvider,
    local_context_reader: ILocalContextReader | None = None,  # ← Added in Phase 1
) -> None:
```

### Bootstrap.py NOT Updated

`src/bootstrap.py` lines 317-320:

```python
retrieve_project_context_handler = RetrieveProjectContextQueryHandler(
    repository=project_repository,
    environment=environment,
    # local_context_reader NOT injected! ← THE GAP
)
```

### Missing Import

`bootstrap.py` does not import:
- `FilesystemLocalContextAdapter` from `src.infrastructure.adapters.persistence`

---

## Impact

- CLI command `jerry projects context` works but does NOT read from `.jerry/local/context.toml`
- Handler falls through to project discovery when env var not set (expected: local context first)
- Phase 1 unit tests pass because they mock the dependency
- Integration/E2E tests pass because they don't test local context reading

---

## Resolution

**Phase 2 tasks** (EN-001):
1. T-014: Write integration test expecting local context to be read
2. T-015: Write integration test expecting JSON output to include source field
3. T-018: Update `bootstrap.py` to wire `FilesystemLocalContextAdapter`

### Required Changes to bootstrap.py

```python
# Add import
from src.infrastructure.adapters.persistence.filesystem_local_context_adapter import (
    FilesystemLocalContextAdapter,
)

# In create_query_dispatcher():
local_context_reader = FilesystemLocalContextAdapter(
    base_path=Path(get_projects_directory()).parent
)

retrieve_project_context_handler = RetrieveProjectContextQueryHandler(
    repository=project_repository,
    environment=environment,
    local_context_reader=local_context_reader,  # Now wired!
)
```

---

## Related Artifacts

- [EN-001](./en-001-session-hook-tdd.md): Parent enabler
- [TD-003](./td-003-missing-local-context-support.md): Original tech debt documenting the gap
- [DEC-001](./dec-001-local-context-test-strategy.md): Decision on test strategy

---

## Change Log

| Date | Change | Author |
|------|--------|--------|
| 2026-01-21 | Discovery documented during Phase 2 exploration | Claude |
