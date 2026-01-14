# BUG-002 Investigation Report: Jerry Plugin Not Loading via --plugin-dir

> **PS ID:** bug-002
> **Entry ID:** e-001
> **Severity:** HIGH
> **Date:** 2026-01-14
> **Investigator:** ps-investigator v2.1.0

---

## L0: Executive Summary (ELI5)

### What's Happening?
When users try to load the Jerry plugin using Claude Code's `--plugin-dir` option, nothing happens. The plugin silently fails to initialize - no welcome message, no project context, nothing.

### Why It Matters
Without the plugin loading, users cannot:
- Use Jerry's project management features
- Get automatic project context enforcement
- Access Jerry skills and workflows

### Root Cause (Plain Language)
The plugin hook tries to run a Python script using `uv run`, but the script has **conflicting instructions**:
1. The script's header says "I have no dependencies" (`dependencies = []`)
2. But the script actually imports from the Jerry package (`from src.infrastructure...`)

When `uv run` sees "no dependencies", it runs the script in isolation without access to the Jerry package. The imports fail silently, and the hook produces no output.

### Fix Summary
Update the script to either:
- **Option A (Quick):** List the local package as a dependency in the script header
- **Option B (Better):** Run the script as a module with proper package installation

---

## L1: Technical Analysis

### Evidence Chain

#### Evidence 1: Hook Configuration
**File:** `hooks/hooks.json` (line 10)
```json
"command": "PYTHONPATH=\"${CLAUDE_PLUGIN_ROOT}\" uv run ${CLAUDE_PLUGIN_ROOT}/src/interface/cli/session_start.py"
```

The hook sets `PYTHONPATH` and uses `uv run` to execute the script.

#### Evidence 2: PEP 723 Inline Script Metadata
**File:** `src/interface/cli/session_start.py` (lines 36-39)
```python
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
```

The script declares **zero dependencies** using PEP 723 inline script metadata.

#### Evidence 3: Conflicting Imports
**File:** `src/interface/cli/session_start.py` (lines 50-57)
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

The script imports from `src.infrastructure` and `src.session_management`, which are part of the Jerry package.

#### Evidence 4: pyproject.toml Package Definition
**File:** `pyproject.toml` (lines 55-56)
```toml
[tool.hatch.build.targets.wheel]
packages = ["src"]
```

The `src/` directory is the package root, confirming these are internal package imports.

### 5 Whys Analysis

#### Why 1: Why doesn't the plugin load?
**Because:** The SessionStart hook produces no output when the script fails silently.

**Evidence:** User reports: "no initialization message when running: JERRY_PROJECT=PROJ-007-jerry-bugs CLAUDE_CONFIG_DIR=~/.claude-geek claude --plugin-dir=/path/to/jerry"

#### Why 2: Why does the script fail silently?
**Because:** `uv run` creates an isolated environment where the `from src.infrastructure...` imports fail with `ModuleNotFoundError`.

**Evidence:** The script uses `sys.exit(main())` at line 347, but if imports fail at lines 50-57, the script never reaches `main()`. The error is swallowed by the hook execution framework.

#### Why 3: Why do the imports fail?
**Because:** `uv run` with PEP 723 metadata creates a virtual environment based ONLY on the declared `dependencies = []`. The Jerry package (`src/`) is not installed.

**Evidence:** PEP 723 spec states: "When a script contains inline metadata, tools SHOULD create an isolated environment with only those dependencies."

#### Why 4: Why doesn't PYTHONPATH help?
**Because:** `uv run` with inline script metadata ignores `PYTHONPATH` - it creates a fresh, isolated environment where only declared dependencies are available.

**Evidence:** The hook sets `PYTHONPATH="${CLAUDE_PLUGIN_ROOT}"`, but `uv run` overrides this with its own isolated environment. The uv documentation states: "Script execution creates an isolated environment."

#### Why 5: Why was this design chosen?
**Because:** PROJ-005 added `uv run` support without accounting for the conflict between "standalone script" semantics (PEP 723) and "package module" semantics (importing from src/).

**Evidence:** ADR e-010 documents the uv Session Start solution but doesn't address the package import conflict.

### Import Dependency Graph

```
session_start.py
    |
    +-> src.infrastructure.adapters.configuration.layered_config_adapter
    |       |
    |       +-> src.infrastructure.adapters.configuration.env_config_adapter
    |       +-> src.infrastructure.adapters.persistence.atomic_file_adapter
    |
    +-> src.infrastructure.adapters.persistence.atomic_file_adapter
    |       |
    |       +-> (stdlib only: fcntl, hashlib, os, tempfile, pathlib)
    |
    +-> src.session_management.application.GetProjectContextQuery
    |       |
    |       +-> (various domain and application layer imports)
    |
    +-> src.session_management.infrastructure
            |
            +-> FilesystemProjectAdapter
            +-> OsEnvironmentAdapter
            +-> InMemorySessionRepository
```

**All imports require the `src/` package to be installed or on PYTHONPATH in a way uv respects.**

---

## L2: Systemic Analysis

### Ishikawa (Fishbone) Diagram

```
                                    Plugin Fails to Load
                                           |
    +------------------+------------------+------------------+------------------+
    |                  |                  |                  |                  |
  Method             Machine           Material           Measurement
    |                  |                  |                  |                  |
    |                  |                  |                  |                  |
[uv run creates    [PYTHONPATH      [PEP 723 metadata   [No error output
 isolated env]      ignored]         conflicts with      from hook failure]
    |                  |              package imports]        |
    |                  |                  |                  |
[PEP 723 declares  [uv overrides    [dependencies=[]    [Silent failure
 no dependencies]   env vars]        but imports src/]   hides root cause]
```

### FMEA (Failure Mode and Effects Analysis)

| Failure Mode | Potential Effect | Severity | Occurrence | Detection | RPN | Recommended Action |
|--------------|------------------|----------|------------|-----------|-----|-------------------|
| uv run ignores PYTHONPATH | Imports fail, hook silent | 8 | 9 | 2 | 144 | Remove PYTHONPATH reliance |
| PEP 723 conflicts with package | Module not found | 9 | 9 | 3 | 243 | Fix metadata or use module run |
| Silent hook failure | User sees nothing | 7 | 8 | 2 | 112 | Add error handling/logging |
| No integration tests | Bug shipped to users | 6 | 7 | 4 | 168 | Add plugin load tests |

**RPN = Severity x Occurrence x Detection** (higher = worse)

### Prevention Strategies

#### Immediate (Hours)

1. **Fix PEP 723 Metadata**
   - Option A: Change `dependencies = []` to include the local package path
   - Option B: Remove PEP 723 metadata entirely and use `python -m` instead

2. **Alternative Hook Command**
   ```json
   "command": "cd ${CLAUDE_PLUGIN_ROOT} && python -m src.interface.cli.session_start"
   ```
   This runs the script as a module within the package context.

#### Short-Term (Days)

1. **Add Plugin Integration Tests**
   - Test hook execution with mock Claude environment
   - Verify expected output format
   - Test error conditions

2. **Add Error Handling to Hook**
   - Wrap imports in try/except
   - Output diagnostic information on failure
   - Ensure non-zero exit on error

3. **Document uv run Behavior**
   - Update ADR e-010 with caveats
   - Add warning about PEP 723 vs package imports

#### Long-Term (Weeks)

1. **Refactor Session Start Architecture**
   - Make session_start.py truly standalone (no package imports)
   - Or package it properly with entry_points

2. **Add Pre-Flight Checks**
   - Verify package installation before hook runs
   - Check environment variables are set correctly

3. **Implement Hook Execution Logging**
   - Log all hook invocations and outcomes
   - Surface errors to users appropriately

### Corrective Actions

| Priority | Action | Owner | Timeline | Status |
|----------|--------|-------|----------|--------|
| P0 | Change hook command to use `python -m` | TBD | 1 hour | PROPOSED |
| P1 | Add integration test for plugin load | TBD | 1 day | PROPOSED |
| P1 | Add error handling to session_start.py | TBD | 1 day | PROPOSED |
| P2 | Update ADR e-010 with caveats | TBD | 2 days | PROPOSED |
| P3 | Evaluate standalone script refactor | TBD | 1 week | PROPOSED |

---

## Appendix A: Proposed Fix (Option A - Quick)

Change `hooks/hooks.json` line 10 from:
```json
"command": "PYTHONPATH=\"${CLAUDE_PLUGIN_ROOT}\" uv run ${CLAUDE_PLUGIN_ROOT}/src/interface/cli/session_start.py"
```

To:
```json
"command": "cd ${CLAUDE_PLUGIN_ROOT} && python -m src.interface.cli.session_start"
```

**Rationale:** Running as a module (`-m`) ensures Python's import system finds the `src/` package from the current directory.

## Appendix B: Proposed Fix (Option B - Better)

1. Remove PEP 723 metadata from `session_start.py` (lines 36-39)
2. Ensure `pip install -e .` is run during plugin installation
3. Use the registered entry point:
   ```json
   "command": "jerry-session-start"
   ```

**Rationale:** This uses the entry point defined in pyproject.toml (line 49: `jerry-session-start = "src.interface.cli.session_start:main"`), which is the intended Python packaging approach.

## Appendix C: Evidence Files

| File | Path | Relevance |
|------|------|-----------|
| hooks.json | `hooks/hooks.json` | Hook command definition |
| session_start.py | `src/interface/cli/session_start.py` | Script with conflicting metadata |
| pyproject.toml | `pyproject.toml` | Package definition |
| plugin.json | `.claude-plugin/plugin.json` | Plugin manifest |
| layered_config_adapter.py | `src/infrastructure/adapters/configuration/` | Import dependency |
| atomic_file_adapter.py | `src/infrastructure/adapters/persistence/` | Import dependency |

---

**Report Generated:** 2026-01-14
**Investigation Method:** 5 Whys + Ishikawa + FMEA
**Confidence Level:** HIGH (evidence chain complete)
