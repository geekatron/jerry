# WI-015: Update session_start.py Hook

| Field | Value |
|-------|-------|
| **ID** | WI-015 |
| **Title** | Update session_start.py Hook |
| **Type** | Task |
| **Status** | COMPLETED |
| **Priority** | HIGH |
| **Phase** | PHASE-05 |
| **Assignee** | WT-CLI |
| **Created** | 2026-01-12 |
| **Completed** | 2026-01-12 |

---

## Description

Update the `scripts/session_start.py` hook to use the new configuration system. The hook should load configuration with proper precedence and detect the active project from config before falling back to user prompts.

---

## Acceptance Criteria

- [x] AC-015.1: Uses `LayeredConfigAdapter` to load configuration
- [x] AC-015.2: Reads `JERRY_PROJECT` from env or `context.active_project` from local config
- [x] AC-015.3: Falls back to project discovery if no active project configured
- [ ] AC-015.4: Updates local context when project is selected (DEFERRED to WI-016)
- [x] AC-015.5: Backward compatible with existing env var workflow
- [x] AC-015.6: Contract tests verify output format unchanged

---

## Sub-tasks

- [x] ST-015.1: Refactor `src/interface/cli/session_start.py` to use new config
- [x] ST-015.2: Load local context from `.jerry/local/context.toml`
- [ ] ST-015.3: Update local context on project selection (DEFERRED to WI-016)
- [x] ST-015.4: Write unit tests for local context functionality
- [x] ST-015.5: Test backward compatibility with `JERRY_PROJECT`

---

## Evidence

| Criterion | Evidence | Source |
|-----------|----------|--------|
| AC-015.1 | `create_config_provider()` creates LayeredConfigAdapter | `src/interface/cli/session_start.py:126-147` |
| AC-015.2 | `get_active_project_from_local_context()` reads from TOML | `src/interface/cli/session_start.py:113-123` |
| AC-015.3 | Falls back to `output_project_required()` when no project | `src/interface/cli/session_start.py:327-329` |
| AC-015.4 | DEFERRED to WI-016 (CLI commands) | - |
| AC-015.5 | 23 existing e2e tests pass, 15 new unit tests | `tests/session_management/e2e/test_session_start.py` |
| AC-015.6 | 23/23 contract tests pass unchanged | `tests/session_management/e2e/test_session_start.py` |

### Test Results

| Test Suite | Count | Status |
|------------|-------|--------|
| E2E session_start tests | 23 | PASSED |
| Unit local context tests | 15 | PASSED |
| Total session tests | 296 | PASSED |

---

## Implementation Notes

```python
# scripts/session_start.py (updated)
from src.infrastructure.adapters.configuration.layered_config_adapter import LayeredConfigAdapter
from src.infrastructure.adapters.persistence.atomic_file_adapter import AtomicFileAdapter


def main() -> int:
    # Load configuration with precedence
    config = LayeredConfigAdapter(
        root_config_path=Path(".jerry/config.toml"),
        defaults=DEFAULTS,
    )

    # Priority 1: Environment variable (via config)
    project_id = config.get_string("project.id")

    # Priority 2: Local context (worktree-specific)
    if not project_id:
        local_context = load_local_context()
        project_id = local_context.get("context", {}).get("active_project")

    # Priority 3: Project discovery (prompt user)
    if not project_id:
        available_projects = discover_projects()
        print_project_required_message(available_projects)
        return 1

    # Validate project
    if not validate_project(project_id):
        print_project_error_message(project_id)
        return 1

    # Success - print project context
    print_project_context_message(project_id)
    return 0


def load_local_context() -> dict:
    """Load worktree-local context from .jerry/local/context.toml."""
    path = Path(".jerry/local/context.toml")
    if not path.exists():
        return {}
    with open(path, "rb") as f:
        return tomllib.load(f)
```

---

## Progress Log

| Timestamp | Update | Actor |
|-----------|--------|-------|
| 2026-01-12T11:00:00Z | Work item created | Claude |
| 2026-01-12T20:00:00Z | Started WI-015 implementation | Claude |
| 2026-01-12T20:15:00Z | Added LayeredConfigAdapter import to session_start.py | Claude |
| 2026-01-12T20:20:00Z | Implemented `load_local_context()` function | Claude |
| 2026-01-12T20:25:00Z | Implemented `get_active_project_from_local_context()` function | Claude |
| 2026-01-12T20:30:00Z | Implemented `create_config_provider()` function | Claude |
| 2026-01-12T20:35:00Z | Updated `main()` to use local context as fallback | Claude |
| 2026-01-12T20:40:00Z | Verified 23 existing e2e tests still pass | Claude |
| 2026-01-12T20:45:00Z | Created 15 new unit tests for local context | Claude |
| 2026-01-12T20:50:00Z | All 296 session tests pass | Claude |
| 2026-01-12T20:55:00Z | Updated evidence table and marked COMPLETED | Claude |

---

## Dependencies

| Type | Work Item | Relationship |
|------|-----------|--------------|
| Depends On | WI-009, WI-010, WI-011 | Domain layer must be complete |
| Depends On | WI-012, WI-013, WI-014 | Infrastructure adapters must be complete |
| Blocks | WI-017 | Architecture tests need working hook |

---

## Related Artifacts

- **Plan Reference**: [PLAN.md, Phase 3](../PLAN.md)
- **Contract Tests**: `tests/contract/test_hook_output.py`
