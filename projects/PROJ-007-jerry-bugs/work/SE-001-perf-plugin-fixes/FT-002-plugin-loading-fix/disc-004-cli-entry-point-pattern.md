# disc-004: CLI Entry Point Pattern

> **Discovery ID:** disc-004
> **Feature:** FT-002-plugin-loading-fix
> **Project:** PROJ-007-jerry-bugs
> **Status:** DOCUMENTED
> **Severity:** Important (Architectural Pattern)
> **Discovered:** 2026-01-14
> **Discovered By:** Claude (during FT-002 implementation)

---

## Summary

When using `uv` to run Python scripts that depend on project packages, **always prefer registered entry points** over directly running module files.

---

## Discovery Context

During FT-002 implementation, we initially used:
```bash
# WRONG: Direct module execution with PYTHONPATH hack
PYTHONPATH="${CLAUDE_PLUGIN_ROOT}" uv run ${CLAUDE_PLUGIN_ROOT}/src/interface/cli/session_start.py
```

This approach:
1. Required PYTHONPATH manipulation (hack)
2. Was fragile and environment-dependent
3. Conflicted with PEP 723 inline metadata behavior

---

## Correct Pattern

Register entry points in `pyproject.toml`:

```toml
[project.scripts]
jerry = "src.interface.cli.main:main"              # User CLI: jerry session start
jerry-session-start = "src.interface.cli.session_start:main"  # Hook entry point
```

Then invoke via entry point:
```bash
# CORRECT: Entry point invocation (uv-native)
uv run --directory ${CLAUDE_PLUGIN_ROOT} jerry-session-start
```

---

## Why This Works

1. **uv builds/installs the project** when using entry points
2. **Package is on PYTHONPATH** automatically via installation
3. **No environment hacks** required
4. **`--directory` flag** tells uv where the project root is

---

## Entry Point Types in Jerry

| Entry Point | Purpose | Invocation Context |
|-------------|---------|-------------------|
| `jerry` | User CLI (all commands) | Interactive terminal |
| `jerry-session-start` | SessionStart hook only | Claude plugin system |

**Important Distinction:**
- `jerry session start` → User command via main CLI
- `jerry-session-start` → Hook entry point (separate binary)

These are **different entry points** for different purposes:
- User CLI: Namespace-based subcommands (`jerry session start`, `jerry items list`)
- Hook: Direct single-purpose binary for plugin hook execution

---

## Evidence

| ID | Source | Description |
|----|--------|-------------|
| E-001 | `pyproject.toml:47-49` | Entry point definitions |
| E-002 | `hooks/hooks.json:10` | Updated hook command (uv-native) |
| E-003 | `/tmp` test | Verified hook works from arbitrary directory |

---

## Implications

### For Hooks
- All hooks using Jerry code should use entry points
- Current TD-003 (Hooks Inconsistency) tracks that PreToolUse/Stop hooks still use `python3 scripts/*.py`
- Future work: Consider entry points for all hooks (if they need project dependencies)

### For CI
- CI scripts should also prefer entry points over `uv run <module.py>`
- This ensures consistent behavior between CI and runtime

### For Developers
- When adding new CLI functionality, register it as an entry point
- Prefer `uv run <entry-point>` over `uv run <script.py>` for anything requiring project imports

---

## Related Artifacts

| Type | Reference |
|------|-----------|
| Feature | FT-002-plugin-loading-fix |
| Technical Debt | TD-003 (hooks inconsistency) |
| ADR | ADR-PROJ007-002 (documents Option 4) |
| Prior Art | PROJ-005-e-010-adr-uv-session-start.md |

---

## Change Log

| Date | Change | Author |
|------|--------|--------|
| 2026-01-14 | Discovery documented | Claude |
