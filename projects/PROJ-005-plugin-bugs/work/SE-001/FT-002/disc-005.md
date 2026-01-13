# DISC-005: PYTHONPATH Required for uv run

> **Discovery ID:** DISC-005
> **Type:** Technical Discovery
> **Status:** RESOLVED
> **Parent:** [FT-002](./FEATURE-WORKTRACKER.md)
> **Related:** EN-003 (BUG-007)
> **Created:** 2026-01-13

---

## Discovery

The `uv run` command alone is not sufficient for running Python scripts that import from local packages. The script must have access to the source directory via PYTHONPATH.

### Evidence

**Test 1: uv run alone (FAILS)**
```bash
$ uv run src/interface/cli/session_start.py
ModuleNotFoundError: No module named 'src'
```

**Test 2: uv run with PYTHONPATH (WORKS)**
```bash
$ PYTHONPATH="." uv run src/interface/cli/session_start.py
Jerry Framework initialized...
<project-context>...</project-context>
```

### Root Cause

The PEP 723 `dependencies` list declares external packages from PyPI, not local source directories. When `uv run` creates an ephemeral environment, it doesn't automatically include the current directory in PYTHONPATH.

### Resolution

Updated `hooks/hooks.json` to include PYTHONPATH:
```json
"command": "PYTHONPATH=\"${CLAUDE_PLUGIN_ROOT}\" uv run ${CLAUDE_PLUGIN_ROOT}/src/interface/cli/session_start.py"
```

### Correction to Prior Analysis

The trade-off analysis (e-009) stated:
> "Options B (sys.path) and D (PYTHONPATH) FAIL because imports require installed packages, not just path manipulation."

This was **incorrect**. The imports work correctly with PYTHONPATH - the packages do NOT require pip installation. The import statements like `from src.infrastructure...` work when `src/` is in PYTHONPATH because Python can find the modules directly.

---

## References

| Source | Location |
|--------|----------|
| hooks.json | `hooks/hooks.json` line 10 |
| uv documentation | https://docs.astral.sh/uv/guides/scripts/ |
| PEP 723 | https://peps.python.org/pep-0723/ |
