# PROJ-005-e-010: ADR - uv-Based Session Start Hook

**ADR ID:** PROJ-005-e-010
**Status:** Accepted
**Date:** 2026-01-13
**Author:** ps-architect
**Deciders:** Project PROJ-005 team
**Bug Reference:** BUG-007 (session_start.py requires pip installation)
**Supersedes:** ADR-PROJ005-001 (Standalone Session Start Hook Implementation)

---

## Context

### Problem Statement

The `scripts/session_start.py` hook fails in Claude Code plugin mode because:

1. It attempts to delegate to the full Hexagonal Architecture implementation via subprocess
2. The subprocess requires a Python virtual environment (`.venv/`) with jerry package installed
3. When the plugin is installed via Claude Code's plugin system, no virtual environment exists

The original ADR-PROJ005-001 proposed a stdlib-only reimplementation that would:
- Duplicate logic between `scripts/session_start.py` and `src/interface/cli/session_start.py`
- Defer 2 of 12 functional requirements (local context, layered configuration)
- Create ongoing maintenance burden to keep two implementations in sync

**User feedback rejected this approach**, stating:
> "The ADR is wrong. [...] A Claude Code plugin CAN have Python dependencies."

### Corrected Understanding

Research (PROJ-005-e-008) established:

1. **Claude Code plugins CAN have dependencies** - The constraint is reliable execution, not stdlib-only
2. **uv package manager** - Provides automatic dependency resolution via PEP 723 inline metadata
3. **The real problem is environment activation** - Not dependency presence

### Architecture Requirement

**REQ-001: The hook MUST use the Hexagonal Architecture CLI implementation.**

The full implementation at `src/interface/cli/session_start.py`:
- Provides all 12 functional requirements
- Uses proper layered configuration (LayeredConfigAdapter)
- Supports local context loading (`.jerry/local/context.toml`)
- Has existing unit and contract test coverage
- Follows Jerry framework architectural patterns

### Options Evaluated

From PROJ-005-e-009 Trade-off Analysis:

| Option | Score | Verdict |
|--------|-------|---------|
| **A: uv run in hooks.json** | **44/50** | **RECOMMENDED** |
| B: sys.path manipulation | 37/50 | FAILS - imports require installed packages |
| C: uv run wrapper | 36/50 | Lower score due to maintenance burden |
| D: PYTHONPATH in hooks.json | 40/50 | FAILS - same issue as Option B |

Options B and D fail because `src/interface/cli/session_start.py` imports:
- `tomllib` (stdlib in Python 3.11+)
- `LayeredConfigAdapter` (from `src.infrastructure.adapters.configuration`)
- `AtomicFileAdapter` (from `src.infrastructure.adapters.persistence`)
- `FilesystemProjectAdapter`, `OsEnvironmentAdapter` (from `src.session_management.infrastructure`)

These imports require the package structure to be importable, which `sys.path` manipulation alone cannot provide without proper package installation.

---

## Decision

**Implement Option A: uv run in hooks.json with PEP 723 inline metadata.**

This approach:
1. Changes `hooks/hooks.json` to invoke `src/interface/cli/session_start.py` via `uv run`
2. Adds PEP 723 inline metadata to the script for dependency declaration
3. Eliminates `scripts/session_start.py` (no longer needed)
4. Requires `uv` to be installed on user systems (acceptable per REQ-002)

### Why uv?

[uv](https://github.com/astral-sh/uv) is a Rust-based Python package manager by Astral that:

| Feature | Benefit for BUG-007 |
|---------|---------------------|
| `uv run` | Executes scripts with automatic dependency resolution |
| PEP 723 | Inline script metadata - no separate requirements.txt |
| Ephemeral environments | Creates isolated envs on-demand in uv cache |
| Caching | Subsequent runs reuse cached environment (fast) |
| No activation | **Solves the core problem** - no manual env activation needed |

### PEP 723 Inline Metadata

[PEP 723](https://peps.python.org/pep-0723/) defines a standard format for embedding metadata in single-file Python scripts:

```python
# /// script
# dependencies = []
# requires-python = ">=3.11"
# ///
```

For `src/interface/cli/session_start.py`, all dependencies are:
- In the stdlib (`tomllib` in Python 3.11+)
- Within the jerry package structure

Therefore, the `dependencies` array is empty - uv only needs to ensure the project is importable.

---

## Consequences

### Positive

1. **Single Source of Truth**: Uses existing `src/interface/cli/session_start.py` without duplication
2. **Full Functionality**: All 12 functional requirements preserved
3. **Minimal Code Changes**: ~5 lines added to script, 1 line changed in hooks.json
4. **Leverages uv Cache**: First run creates env, subsequent runs are fast
5. **No Wrapper Maintenance**: Eliminates `scripts/session_start.py` entirely
6. **Existing Tests Remain Valid**: Contract tests verify output format, not execution method

### Negative

1. **uv Dependency**: Requires users to have uv installed
2. **First-Run Latency**: Initial invocation may take 1-2 seconds for env creation
3. **User System Requirement**: Must document uv installation in INSTALLATION.md

### Risk Mitigation

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| User doesn't have uv | Medium | High | Document in INSTALLATION.md; provide installation commands |
| uv cache corruption | Low | Medium | uv auto-rebuilds; document cache clear instructions |
| First-run latency | Certain | Low | Acceptable within 10s hook timeout; cached after first run |
| PEP 723 not supported | Very Low | High | uv fully supports PEP 723; well-tested standard |

---

## Implementation

### 1. Update hooks/hooks.json

Change the SessionStart hook command:

**Before:**
```json
{
  "type": "command",
  "command": "python3 ${CLAUDE_PLUGIN_ROOT}/scripts/session_start.py",
  "timeout": 10000
}
```

**After:**
```json
{
  "type": "command",
  "command": "uv run ${CLAUDE_PLUGIN_ROOT}/src/interface/cli/session_start.py",
  "timeout": 10000
}
```

### 2. Add PEP 723 Metadata to src/interface/cli/session_start.py

Insert after the module docstring, before imports:

```python
"""
Jerry Framework - Session Start Hook
...existing docstring...
"""

# /// script
# dependencies = []
# requires-python = ">=3.11"
# ///

from __future__ import annotations
...
```

**Note:** The `dependencies` array is empty because:
- `tomllib` is stdlib in Python 3.11+
- All other imports are from the jerry package itself
- uv will resolve the package structure via `--directory`

### 3. Delete scripts/session_start.py

The legacy wrapper at `scripts/session_start.py` is no longer needed:

```bash
rm scripts/session_start.py
```

### 4. Update docs/INSTALLATION.md

Add uv as a prerequisite:

```markdown
## Prerequisites

- Python 3.11 or higher
- uv package manager ([installation guide](https://docs.astral.sh/uv/getting-started/installation/))

### Installing uv

#### macOS/Linux (Recommended)

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

#### Via Homebrew

```bash
brew install uv
```

#### Via pip (Fallback)

```bash
pip install uv
```

### Verify Installation

```bash
uv --version
```

Expected output: `uv 0.5.x` or higher
```

### 5. Implementation Checklist

- [ ] Update `hooks/hooks.json` SessionStart command to use `uv run`
- [ ] Add PEP 723 metadata block to `src/interface/cli/session_start.py`
- [ ] Delete `scripts/session_start.py`
- [ ] Update `docs/INSTALLATION.md` with uv requirement
- [ ] Add regression tests for BUG-007
- [ ] Verify all contract tests pass
- [ ] Test on fresh clone without pip install

---

## Testing Strategy

### Existing Tests (No Changes Required)

All existing tests remain valid because they test the output format and behavior of `src/interface/cli/session_start.py`, not the execution method:

| Test Suite | Location | Status |
|------------|----------|--------|
| Contract Tests | `tests/session_management/contract/test_hook_contract.py` | Valid |
| Unit Tests | `tests/session_management/` | Valid |

### New Integration Tests

```python
# tests/integration/test_uv_hook_execution.py

import subprocess
from pathlib import Path

def test_hook_executes_via_uv_run(tmp_path, monkeypatch):
    """Verify hook works via uv run command."""
    # Setup minimal project structure
    projects_dir = tmp_path / "projects" / "PROJ-001-test"
    projects_dir.mkdir(parents=True)
    (projects_dir / "PLAN.md").write_text("# Test Plan")
    (projects_dir / "WORKTRACKER.md").write_text("# Test Tracker")

    monkeypatch.setenv("CLAUDE_PLUGIN_ROOT", str(tmp_path))
    monkeypatch.setenv("CLAUDE_PROJECT_DIR", str(tmp_path))
    monkeypatch.setenv("JERRY_PROJECT", "PROJ-001-test")

    result = subprocess.run(
        ["uv", "run", str(tmp_path / "src/interface/cli/session_start.py")],
        capture_output=True,
        text=True,
        cwd=str(tmp_path),
    )

    assert result.returncode == 0
    assert "<project-context>" in result.stdout
    assert "ProjectActive: PROJ-001-test" in result.stdout


def test_hook_exits_zero_on_missing_project(tmp_path, monkeypatch):
    """Hook must exit 0 even when project not found."""
    monkeypatch.setenv("CLAUDE_PLUGIN_ROOT", str(tmp_path))
    monkeypatch.setenv("JERRY_PROJECT", "PROJ-999-nonexistent")

    result = subprocess.run(
        ["uv", "run", str(tmp_path / "src/interface/cli/session_start.py")],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0  # Must always be 0
    assert "<project-error>" in result.stdout
```

### New Regression Tests

```python
# tests/regression/test_bug007_plugin_mode.py

import subprocess
import shutil
from pathlib import Path

def test_no_venv_required(tmp_path):
    """BUG-007: Hook must work without .venv directory."""
    # Clone plugin structure to temp location (simulating fresh install)
    plugin_src = Path(__file__).parent.parent.parent
    plugin_dst = tmp_path / "jerry-plugin"

    # Copy only essential files (no .venv)
    for item in ["src", "hooks", "projects", "pyproject.toml"]:
        src_path = plugin_src / item
        if src_path.exists():
            if src_path.is_dir():
                shutil.copytree(src_path, plugin_dst / item)
            else:
                shutil.copy2(src_path, plugin_dst / item)

    # Ensure no .venv exists
    assert not (plugin_dst / ".venv").exists()

    # Execute hook via uv run
    result = subprocess.run(
        ["uv", "run", str(plugin_dst / "src/interface/cli/session_start.py")],
        capture_output=True,
        text=True,
        cwd=str(plugin_dst),
        env={
            "CLAUDE_PLUGIN_ROOT": str(plugin_dst),
            "CLAUDE_PROJECT_DIR": str(plugin_dst),
        },
    )

    assert result.returncode == 0
    assert "ModuleNotFoundError" not in result.stderr
    assert "<project-" in result.stdout


def test_fresh_system_execution(tmp_path):
    """BUG-007: Hook must work on fresh system with only uv installed."""
    # Verify uv is available
    uv_check = subprocess.run(["uv", "--version"], capture_output=True)
    assert uv_check.returncode == 0, "uv must be installed to run this test"

    # Setup minimal plugin structure
    plugin_dir = tmp_path / "jerry-plugin"
    plugin_dir.mkdir()

    # Create minimal pyproject.toml
    (plugin_dir / "pyproject.toml").write_text("""
[project]
name = "jerry"
version = "0.1.0"
requires-python = ">=3.11"

[build-system]
requires = ["setuptools>=68", "wheel"]
build-backend = "setuptools.build_meta"

[tool.setuptools.packages.find]
where = ["."]
""")

    # Create src structure with minimal session_start.py
    src_dir = plugin_dir / "src" / "interface" / "cli"
    src_dir.mkdir(parents=True)
    (plugin_dir / "src" / "__init__.py").write_text("")
    (plugin_dir / "src" / "interface" / "__init__.py").write_text("")
    (src_dir / "__init__.py").write_text("")
    (src_dir / "session_start.py").write_text('''
# /// script
# dependencies = []
# requires-python = ">=3.11"
# ///
"""Minimal session start for testing."""
import sys
def main() -> int:
    print("Jerry Framework initialized.")
    print("<project-required>")
    print("ProjectRequired: true")
    print("AvailableProjects:")
    print("NextProjectNumber: 001")
    print("ProjectsJson: []")
    print("</project-required>")
    return 0

if __name__ == "__main__":
    sys.exit(main())
''')

    # Execute via uv run
    result = subprocess.run(
        ["uv", "run", str(src_dir / "session_start.py")],
        capture_output=True,
        text=True,
        cwd=str(plugin_dir),
    )

    assert result.returncode == 0
    assert "<project-required>" in result.stdout
```

### Testing Matrix

| Test Type | Tests | Purpose |
|-----------|-------|---------|
| Contract | 13+ existing | Verify output format compliance |
| Unit | Existing | Verify internal function behavior |
| Integration | 2 new | Verify uv run execution path |
| Regression | 2 new | Verify BUG-007 is resolved |
| E2E | 1 new | Verify plugin installation scenario |

---

## Verification Checklist

Before marking BUG-007 as resolved:

- [ ] `uv run src/interface/cli/session_start.py` works from repository root
- [ ] Output matches contract test expectations (all 13 tests pass)
- [ ] Works on fresh clone without `pip install -e .`
- [ ] Works without `.venv/` directory present
- [ ] INSTALLATION.md documents uv requirement
- [ ] `scripts/session_start.py` is deleted
- [ ] hooks.json updated to use uv run
- [ ] PEP 723 metadata present in `src/interface/cli/session_start.py`

---

## References

### Input Documents

| Document | Key Findings |
|----------|--------------|
| [PROJ-005-e-008](../research/PROJ-005-e-008-uv-dependency-management.md) | uv + PEP 723 enables inline dependencies; plugins CAN have dependencies |
| [PROJ-005-e-009](../analysis/PROJ-005-e-009-tradeoffs.md) | Option A recommended with score 44/50; Options B/D fail due to import requirements |
| [PROJ-005-e-006](../investigations/PROJ-005-e-006-functional-requirements.md) | 12 functional requirements; exit code must always be 0 |
| [PROJ-005-e-007](../research/PROJ-005-e-007-plugin-patterns.md) | 10 patterns for hook scripts |

### Superseded Documents

| Document | Reason for Supersession |
|----------|-------------------------|
| [ADR-PROJ005-001](ADR-PROJ005-001-standalone-session-start.md) | User rejected stdlib-only approach; requires uv-based solution |

### Implementation Files

| File | Action |
|------|--------|
| `src/interface/cli/session_start.py` | Add PEP 723 metadata block (~5 lines) |
| `hooks/hooks.json` | Change command to use `uv run` (1 line) |
| `scripts/session_start.py` | DELETE (legacy wrapper no longer needed) |
| `docs/INSTALLATION.md` | Add uv prerequisite documentation |

### External References

| Source | URL |
|--------|-----|
| uv Documentation | https://docs.astral.sh/uv/ |
| uv Running Scripts | https://docs.astral.sh/uv/guides/scripts/ |
| PEP 723 | https://peps.python.org/pep-0723/ |
| uv GitHub | https://github.com/astral-sh/uv |

---

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-01-13 | ps-architect | Initial acceptance; supersedes ADR-PROJ005-001 |

---

*ADR created: 2026-01-13*
*Status: Accepted*
