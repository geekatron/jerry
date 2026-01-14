# ADR-PROJ007-002: Plugin Session Start Execution Strategy

**ADR ID:** ADR-PROJ007-002
**Status:** Proposed
**Date:** 2026-01-14
**Author:** ps-architect
**Deciders:** Project PROJ-007 team
**Bug Reference:** BUG-002 (Jerry Plugin Not Loading via --plugin-dir)

---

## Context

### Problem Statement

When users load the Jerry plugin using Claude Code's `--plugin-dir` option, the plugin silently fails to initialize. Users see no welcome message, no project context, and Jerry's features are unavailable.

### Current Behavior (Broken)

The `SessionStart` hook in `hooks/hooks.json` is configured as:

```json
"command": "PYTHONPATH=\"${CLAUDE_PLUGIN_ROOT}\" uv run ${CLAUDE_PLUGIN_ROOT}/src/interface/cli/session_start.py"
```

The script `src/interface/cli/session_start.py` contains PEP 723 inline script metadata:

```python
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
```

But the script imports from the Jerry package:

```python
from src.infrastructure.adapters.configuration.layered_config_adapter import (
    LayeredConfigAdapter,
)
from src.session_management.application import GetProjectContextQuery
# ... more package imports
```

### Root Cause Analysis

The failure chain is:

1. Hook sets `PYTHONPATH="${CLAUDE_PLUGIN_ROOT}"` and invokes `uv run`
2. `uv run` detects PEP 723 metadata with `dependencies = []`
3. Per PEP 723 spec, `uv run` creates an **isolated environment** with only declared dependencies
4. The isolated environment ignores `PYTHONPATH` entirely
5. The `from src.infrastructure...` imports fail with `ModuleNotFoundError`
6. The script terminates before reaching `main()`, producing no output
7. Claude Code receives no output and the plugin appears not to load

### Impact

Without the plugin loading:
- No project context enforcement
- No JERRY_PROJECT validation
- No session initialization
- Jerry framework is effectively non-functional

---

## Decision Drivers

| Priority | Driver | Rationale |
|----------|--------|-----------|
| P0 | Works without pip install | Plugin must be self-contained |
| P0 | Works with Claude Code plugin architecture | Must integrate correctly with hook system |
| P1 | Maintainable | Solution should not require parallel codebases |
| P1 | Error visibility | Failures should produce diagnostic output |
| P2 | Performance | Should complete well under 10s timeout |

---

## Considered Options

### Option 1: Use `python -m` Instead of `uv run`

**Description:** Change the hook command to run the script as a Python module rather than using `uv run`.

**Hook Command:**
```json
"command": "cd ${CLAUDE_PLUGIN_ROOT} && python -m src.interface.cli.session_start"
```

**Pros:**
- Minimal change (single line in hooks.json)
- Uses Python's standard module import system
- `cd` ensures `src/` is discoverable on `sys.path`
- No external tool dependencies (`python` is guaranteed present)
- Maintains full feature parity with current implementation

**Cons:**
- Relies on `cd` being available (standard on all platforms)
- Requires current directory to be plugin root for imports to work
- Does not leverage uv's dependency isolation benefits

**Code Changes Required:**
1. `hooks/hooks.json` line 10 only

### Option 2: Remove PEP 723 and Use Entry Point

**Description:** Remove the PEP 723 metadata from `session_start.py` and use the registered entry point from `pyproject.toml`.

**Hook Command:**
```json
"command": "jerry-session-start"
```

**Pros:**
- Clean, idiomatic Python packaging approach
- Entry point defined in pyproject.toml (line 49)
- Leverages proper package installation

**Cons:**
- **Requires `pip install -e .`** to be run before plugin can work
- Breaks the self-contained plugin requirement
- Adds installation friction for users
- Entry point only exists after package installation

**Code Changes Required:**
1. `hooks/hooks.json` line 10
2. Remove lines 36-39 from `session_start.py`
3. Require package installation in documentation

### Option 3: Make Script Truly Standalone (No Package Imports)

**Description:** Rewrite `session_start.py` to have zero dependencies on the `src/` package, using only Python stdlib.

**Hook Command:**
```json
"command": "uv run ${CLAUDE_PLUGIN_ROOT}/src/interface/cli/session_start.py"
```

**Pros:**
- Script becomes genuinely self-contained
- Works with uv run's isolation model
- Consistent with PEP 723 semantics
- Could be extended with external dependencies via PEP 723

**Cons:**
- **Requires reimplementing functionality from:**
  - `LayeredConfigAdapter` (config loading)
  - `AtomicFileAdapter` (file operations)
  - `FilesystemProjectAdapter` (project discovery)
  - `OsEnvironmentAdapter` (environment handling)
  - `GetProjectContextQuery` (context assembly)
- Creates code duplication
- Maintenance burden of keeping two implementations in sync
- Estimated 200+ lines of code to rewrite
- Risk of feature drift between implementations

**Code Changes Required:**
1. Major rewrite of `session_start.py` (~400 lines)
2. Removal of all `src.*` imports
3. Inline implementation of all required functionality

---

## Decision Outcome

**Selected Option: Option 1 - Use `python -m` Instead of `uv run`**

### Rationale

| Criterion | Option 1 | Option 2 | Option 3 |
|-----------|----------|----------|----------|
| Works without pip install | YES | NO | YES |
| Change scope | 1 line | 3+ files | 400+ lines |
| Maintains feature parity | YES | YES | YES (but duplicated) |
| Maintenance burden | None | Low | High |
| Risk level | Low | Medium | High |

Option 1 is selected because:

1. **Minimal change** - Single line modification to `hooks.json`
2. **Immediate fix** - Can be implemented and tested in minutes
3. **No code duplication** - Keeps single source of truth for session logic
4. **Guaranteed Python availability** - `python` is always present where Claude Code runs
5. **No installation friction** - Plugin remains self-contained

### Why Other Options Were Rejected

**Option 2 (Entry Point)** was rejected because:
- Violates the "works without pip install" driver
- Adds installation friction for end users
- Plugin should be usable immediately after cloning

**Option 3 (Standalone Rewrite)** was rejected because:
- Disproportionate effort (~400 lines) for the problem being solved
- Creates maintenance burden with code duplication
- Risk of feature drift between implementations
- The existing implementation is correct; only the invocation method is broken

---

## Consequences

### Positive

1. **Immediate resolution** - Plugin will load correctly with one-line fix
2. **No feature regression** - All existing functionality preserved
3. **Low risk** - Minimal change surface area
4. **Testable** - Easy to verify fix works

### Negative

1. **Directory dependency** - Relies on `cd` to set correct working directory
2. **Not leveraging uv** - Loses uv's reproducible environment benefits for this script

### Neutral

1. **PEP 723 metadata becomes documentation** - The metadata stays but is ignored by the new invocation method
2. **Other hooks already use python3** - This aligns with `PreToolUse` and `Stop` hooks

---

## Implementation Plan

### Step 1: Update hooks.json (Required)

**File:** `hooks/hooks.json`

**Before (line 10):**
```json
"command": "PYTHONPATH=\"${CLAUDE_PLUGIN_ROOT}\" uv run ${CLAUDE_PLUGIN_ROOT}/src/interface/cli/session_start.py"
```

**After (line 10):**
```json
"command": "cd ${CLAUDE_PLUGIN_ROOT} && python -m src.interface.cli.session_start"
```

### Step 2: Add Error Handling Wrapper (Recommended)

To prevent silent failures in the future, add a try/except wrapper in `session_start.py`:

**File:** `src/interface/cli/session_start.py`

**Add at the end of imports (after line 57):**

```python
# Import validation - fail early with diagnostic
_IMPORT_VALIDATION_PASSED = True

def _emit_import_error(error: Exception) -> None:
    """Emit diagnostic output when imports fail."""
    print("Jerry Framework initialization ERROR.")
    print("<project-error>")
    print(f"InvalidProject: NONE")
    print(f"Error: Import failed - {type(error).__name__}: {error}")
    print("AvailableProjects:")
    print("NextProjectNumber: 001")
    print("</project-error>")
    print()
    print("ACTION REQUIRED: Jerry plugin failed to initialize.")
    print("Ensure you are running from the jerry repository root.")
    print(f"Technical: {error}", file=sys.stderr)
```

**Modify the entry point at the bottom of the file:**

```python
if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        _emit_import_error(e)
        sys.exit(0)  # Always exit 0 per hook contract
```

### Step 3: Consider Removing PEP 723 Metadata (Optional)

The PEP 723 metadata is now unused and potentially misleading. Consider removing it:

**File:** `src/interface/cli/session_start.py`

**Remove lines 36-39:**
```python
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
```

**Or update to clarify:**
```python
# /// script
# NOTE: This script is invoked as a module, not standalone.
# The PEP 723 metadata below is for documentation only.
# requires-python = ">=3.11"
# dependencies = ["jerry"]  # Requires local package
# ///
```

### Testing Strategy

#### Manual Verification

```bash
# 1. Navigate to Jerry repository root
cd /path/to/jerry

# 2. Test the new command directly
cd . && python -m src.interface.cli.session_start
# Expected: <project-required> or <project-context> output

# 3. Test with JERRY_PROJECT set
export JERRY_PROJECT=PROJ-007-jerry-bugs
cd . && python -m src.interface.cli.session_start
# Expected: <project-context> with project details

# 4. Test via Claude Code
JERRY_PROJECT=PROJ-007-jerry-bugs claude --plugin-dir=/path/to/jerry
# Expected: Jerry Framework initialization message
```

#### Automated Test (Integration)

```python
# tests/integration/test_plugin_loading.py

import subprocess
from pathlib import Path

def test_session_start_via_module(tmp_path):
    """Session start works when invoked as module."""
    # Create minimal project structure
    projects_dir = tmp_path / "projects"
    project_dir = projects_dir / "PROJ-001-test"
    project_dir.mkdir(parents=True)
    (project_dir / "PLAN.md").write_text("# Test")
    (project_dir / "WORKTRACKER.md").write_text("Status: IN_PROGRESS")

    # Get jerry root (parent of tests)
    jerry_root = Path(__file__).parent.parent.parent

    # Execute as the hook would
    result = subprocess.run(
        ["python", "-m", "src.interface.cli.session_start"],
        capture_output=True,
        text=True,
        cwd=str(jerry_root),
        env={
            "CLAUDE_PROJECT_DIR": str(jerry_root),
            "JERRY_PROJECT": "PROJ-001-test",
        },
    )

    assert result.returncode == 0
    assert "<project-" in result.stdout  # Has structured output
    assert "ModuleNotFoundError" not in result.stderr
```

### Rollout Plan

| Phase | Action | Timeline |
|-------|--------|----------|
| 1 | Apply hooks.json change | Immediate |
| 2 | Test locally with `--plugin-dir` | 5 minutes |
| 3 | Add error handling (Step 2) | 30 minutes |
| 4 | Add integration test | 30 minutes |
| 5 | Commit and document | 10 minutes |

---

## Copy-Paste Ready Changes

### Change 1: hooks.json (REQUIRED)

```diff
--- a/hooks/hooks.json
+++ b/hooks/hooks.json
@@ -7,7 +7,7 @@
         "hooks": [
           {
             "type": "command",
-            "command": "PYTHONPATH=\"${CLAUDE_PLUGIN_ROOT}\" uv run ${CLAUDE_PLUGIN_ROOT}/src/interface/cli/session_start.py",
+            "command": "cd ${CLAUDE_PLUGIN_ROOT} && python -m src.interface.cli.session_start",
             "timeout": 10000
           }
         ]
```

### Change 2: session_start.py Error Handling (RECOMMENDED)

At the end of the file, replace:

```python
if __name__ == "__main__":
    sys.exit(main())
```

With:

```python
def _emit_initialization_error(error: Exception) -> None:
    """Emit diagnostic output when initialization fails.

    This ensures users see meaningful error messages rather than
    silent failure when the plugin cannot load.
    """
    print("Jerry Framework initialization ERROR.")
    print("<project-error>")
    print("InvalidProject: NONE")
    print(f"Error: {type(error).__name__}: {error}")
    print("AvailableProjects:")
    print("NextProjectNumber: 001")
    print("</project-error>")
    print()
    print("ACTION REQUIRED: Jerry plugin failed to initialize.")
    print("Technical details logged to stderr.")
    print(f"[session_start.py] {type(error).__name__}: {error}", file=sys.stderr)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        _emit_initialization_error(e)
        sys.exit(0)  # Always exit 0 per hook contract
```

---

## Compliance

### Decision Drivers Verification

| Driver | Met? | Evidence |
|--------|------|----------|
| Works without pip install | YES | `python -m` uses in-tree source |
| Works with Claude Code plugin | YES | Standard hook invocation |
| Maintainable | YES | Single source of truth preserved |
| Error visibility | YES | (with Step 2 implementation) |
| Performance | YES | No additional overhead |

### Pattern Compliance

| Pattern ID | Description | Compliance |
|------------|-------------|------------|
| P-002 | File Persistence | N/A (hook output) |
| P-007 | Error Handling | YES (with Step 2) |
| CT-001 | Exit code always 0 | YES |
| CT-002 | Exactly one tag type | YES |

---

## References

### Investigation Report

- `projects/PROJ-007-jerry-bugs/investigations/bug-002-e-001-investigation.md`

### Related ADRs

- ADR-PROJ005-001: Standalone Session Start Hook Implementation
- ADR e-010: uv Session Start solution (referenced in investigation)

### Source Files

| File | Purpose |
|------|---------|
| hooks/hooks.json | Hook command definition (line 10) |
| src/interface/cli/session_start.py | Script with conflicting metadata |
| pyproject.toml | Package definition (line 49, 55-56) |

### External References

| Source | URL |
|--------|-----|
| PEP 723 | https://peps.python.org/pep-0723/ |
| Claude Code Hooks | https://docs.anthropic.com/en/docs/claude-code/hooks |
| uv Script Dependencies | https://docs.astral.sh/uv/guides/scripts/#declaring-script-dependencies |

---

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-01-14 | ps-architect | Initial proposal |

---

*ADR created: 2026-01-14*
*Status: Proposed*
