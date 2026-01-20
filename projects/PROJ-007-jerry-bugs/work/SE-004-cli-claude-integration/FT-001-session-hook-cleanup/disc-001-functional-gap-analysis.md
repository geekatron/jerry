# DISC-001: Functional Gap Between cli/main.py and cli/session_start.py

> **Type:** Discovery
> **Feature:** [FT-001](./FEATURE-WORKTRACKER.md) Session Hook Cleanup
> **Solution Epic:** [SE-004](../SOLUTION-WORKTRACKER.md) CLI and Claude Code Integration
> **Project:** PROJ-007-jerry-bugs
> **Status:** DOCUMENTED
> **Created:** 2026-01-15
> **Last Updated:** 2026-01-15

---

## Discovery Summary

Root Cause Analysis revealed that `cli/session_start.py` contains functionality that does not exist in `cli/main.py`. This functionality must be migrated before the rogue file can be deleted.

## Functional Gap Matrix

| Functionality | `cli/main.py` | `cli/session_start.py` | Migration Required |
|--------------|---------------|------------------------|-------------------|
| Project context query | Yes | Yes | No |
| JSON output format | Yes (`--json`) | Yes (`OutputCollector`) | Partial |
| Hook-specific JSON format | **NO** | Yes | **YES** |
| Local context reading | **NO** | Yes | **YES** |
| Status icons in list | **NO** | Yes | **YES** |
| XML-like structured tags | **NO** | Yes | **YES** |
| `<project-context>` output | **NO** | Yes | **YES** |
| `<project-required>` output | **NO** | Yes | **YES** |
| `<project-error>` output | **NO** | Yes | **YES** |
| ACTION REQUIRED messages | **NO** | Yes | **YES** |
| ProjectsJson field | **NO** | Yes | **YES** |

## Unique Components in cli/session_start.py

### 1. OutputCollector Class (lines 63-92)
```python
class OutputCollector:
    """Collects output lines for JSON formatting."""
    def to_json(self) -> str:
        return json.dumps({
            "hookSpecificOutput": {
                "hookEventName": "SessionStart",
                "additionalContext": content
            }
        })
```

### 2. Local Context Functions (lines 128-164)
```python
def load_local_context() -> dict[str, Any]: ...
def get_active_project_from_local_context() -> str | None: ...
```

### 3. Structured Output Functions (lines 216-296)
```python
def output_project_active(context, out): ...
def output_project_required(context, out): ...
def output_project_error(context, out): ...
```

### 4. Project List Formatter (lines 191-213)
```python
def format_project_list(projects) -> str:
    # Includes status icons: [ACTIVE], [DONE], [DRAFT], etc.
```

## Migration Strategy

1. **Phase 1**: Add `--format hook` option to CLI
2. **Phase 2**: Move structured output functions to `CLIAdapter`
3. **Phase 3**: Add local context support to project queries
4. **Phase 4**: Update hook wrapper to use main CLI
5. **Phase 5**: Delete `cli/session_start.py`

## Related Artifacts

| Type | Location | Description |
|------|----------|-------------|
| Technical Debt | [td-001](./td-001-session-start-violates-hexagonal.md) | Architecture violation |
| Technical Debt | [td-002](./td-002-duplicate-entry-points.md) | Duplicate entry points |
| Technical Debt | [td-003](./td-003-missing-local-context-support.md) | Missing local context |
| Main CLI | `src/interface/cli/main.py` | Target for migration |
| Rogue CLI | `src/interface/cli/session_start.py` | Source of functionality |

---

## Change Log

| Date | Change | Author |
|------|--------|--------|
| 2026-01-15 | Discovery documented from RCA | Claude |
