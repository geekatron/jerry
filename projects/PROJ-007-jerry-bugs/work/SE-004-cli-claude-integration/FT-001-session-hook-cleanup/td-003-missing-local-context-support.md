# TD-003: cli/main.py Missing Local Context Support

> **Type:** Technical Debt
> **Feature:** [FT-001](./FEATURE-WORKTRACKER.md) Session Hook Cleanup
> **Solution Epic:** [SE-004](../SOLUTION-WORKTRACKER.md) CLI and Claude Code Integration
> **Project:** PROJ-007-jerry-bugs
> **Status:** DOCUMENTED
> **Severity:** MEDIUM
> **Created:** 2026-01-15
> **Last Updated:** 2026-01-15

---

## Description

The main CLI (`cli/main.py`) does not support reading project context from local worktree configuration (`.jerry/local/context.toml`). This functionality was implemented only in `cli/session_start.py`.

## Evidence

**`cli/session_start.py` has (lines 128-164):**
```python
def load_local_context() -> dict[str, Any]:
    """Load worktree-local context from .jerry/local/context.toml."""
    path = get_local_context_path()
    if not path.exists():
        return {}
    file_adapter = AtomicFileAdapter()
    content = file_adapter.read_with_lock(path)
    return tomllib.loads(content)

def get_active_project_from_local_context() -> str | None:
    """Get the active project ID from local context."""
    context = load_local_context()
    return context.get("context", {}).get("active_project")
```

**`cli/main.py` does NOT have this functionality.**

## Impact

1. **Feature Gap** - Main CLI cannot use worktree-specific project selection
2. **Inconsistent Behavior** - Different project resolution between entry points
3. **User Experience** - Users must set `JERRY_PROJECT` env var manually

## Configuration Precedence (from WI-015)

The intended precedence is:
1. `JERRY_PROJECT` environment variable (highest)
2. `.jerry/local/context.toml` (worktree-specific)
3. Project discovery (prompts user)

Only `cli/session_start.py` implements levels 2 and 3.

## Resolution

1. Add local context reading to `CLIAdapter` or bootstrap
2. Implement configuration precedence in `RetrieveProjectContextQuery`
3. Ensure `cli/main.py` respects the precedence chain

## Related Artifacts

| Type | Location | Description |
|------|----------|-------------|
| Reference | WI-015 | Configuration precedence spec |
| Reference | ADR-PROJ004-004 | JerrySession Context (5-level precedence) |
| Missing In | `src/interface/cli/main.py` | Main CLI |
| Implemented In | `src/interface/cli/session_start.py` | Rogue CLI |

---

## Change Log

| Date | Change | Author |
|------|--------|--------|
| 2026-01-15 | Technical debt documented | Claude |
