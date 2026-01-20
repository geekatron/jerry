# TD-002: Duplicate CLI Entry Points

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

There are two separate CLI entry points defined in `pyproject.toml`, creating maintenance burden and architectural inconsistency.

## Evidence

**pyproject.toml (lines 47-49):**
```toml
[project.scripts]
jerry = "src.interface.cli.main:main"
jerry-session-start = "src.interface.cli.session_start:main"
```

## Impact

1. **Maintenance Burden** - Two files to maintain for CLI functionality
2. **Inconsistent Behavior** - Different output formats between entry points
3. **Test Duplication** - Separate test suites for overlapping functionality
4. **Confusion** - Unclear which entry point to use for what purpose

## Root Cause

A previous Claude Code session needed to:
1. Output JSON format for hook integration
2. Read local worktree context
3. Output structured XML-like tags

Instead of extending `cli/main.py`, a separate `cli/session_start.py` was created.

## Target State

**Single entry point with command support:**
```toml
[project.scripts]
jerry = "src.interface.cli.main:main"
```

**Hook wrapper calls:**
```bash
# From session_start_hook.py
uv run jerry projects context --format hook
```

## Resolution

1. Add `--format hook` option to `jerry projects context`
2. Implement hook output format in `CLIAdapter`
3. Update `session_start_hook.py` to call `jerry` instead of `jerry-session-start`
4. Remove `jerry-session-start` entry point from pyproject.toml
5. Delete `cli/session_start.py`

## Related Artifacts

| Type | Location | Description |
|------|----------|-------------|
| Technical Debt | [td-001-session-start-violates-hexagonal.md](./td-001-session-start-violates-hexagonal.md) | Architecture violation |
| pyproject.toml | `pyproject.toml` | Entry point definitions |
| Main CLI | `src/interface/cli/main.py` | Proper entry point |
| Rogue CLI | `src/interface/cli/session_start.py` | Duplicate entry point |

---

## Change Log

| Date | Change | Author |
|------|--------|--------|
| 2026-01-15 | Technical debt documented | Claude |
