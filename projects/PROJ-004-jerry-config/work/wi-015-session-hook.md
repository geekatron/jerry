# WI-015: Update session_start.py Hook

| Field | Value |
|-------|-------|
| **ID** | WI-015 |
| **Title** | Update session_start.py Hook |
| **Type** | Task |
| **Status** | PENDING |
| **Priority** | HIGH |
| **Phase** | PHASE-05 |
| **Assignee** | WT-CLI |
| **Created** | 2026-01-12 |
| **Completed** | - |

---

## Description

Update the `scripts/session_start.py` hook to use the new configuration system. The hook should load configuration with proper precedence and detect the active project from config before falling back to user prompts.

---

## Acceptance Criteria

- [ ] AC-015.1: Uses `LayeredConfigAdapter` to load configuration
- [ ] AC-015.2: Reads `JERRY_PROJECT` from env or `context.active_project` from local config
- [ ] AC-015.3: Falls back to project discovery if no active project configured
- [ ] AC-015.4: Updates local context when project is selected
- [ ] AC-015.5: Backward compatible with existing env var workflow
- [ ] AC-015.6: Contract tests verify output format unchanged

---

## Sub-tasks

- [ ] ST-015.1: Refactor `scripts/session_start.py` to use new config
- [ ] ST-015.2: Load local context from `.jerry/local/context.toml`
- [ ] ST-015.3: Update local context on project selection
- [ ] ST-015.4: Write contract tests for hook output format
- [ ] ST-015.5: Test backward compatibility with `JERRY_PROJECT`

---

## Evidence

| Criterion | Evidence | Source |
|-----------|----------|--------|
| AC-015.1 | - | - |
| AC-015.2 | - | - |
| AC-015.3 | - | - |
| AC-015.4 | - | - |
| AC-015.5 | - | - |
| AC-015.6 | - | - |

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
