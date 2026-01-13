# PROJ-005-e-008: uv and Python Dependency Management for Plugin Hooks

**PS ID:** PROJ-005
**Entry ID:** e-008
**Date:** 2026-01-13
**Author:** ps-researcher (re-analysis phase)
**Topic:** uv Package Manager and Plugin Dependency Management Alternatives

---

## L0: Executive Summary

This research analyzes alternatives for managing Python dependencies in Claude Code plugin hooks. The original BUG-007 analysis incorrectly assumed plugins must be stdlib-only. This research corrects that assumption and evaluates options for using the full Hexagonal Architecture CLI implementation.

**Key Finding:** Claude Code plugins CAN have Python dependencies. The `uv` package manager with PEP 723 inline metadata provides an elegant solution for self-contained, dependency-enabled scripts.

### Recommended Approach

| Option | Viability | Pros | Cons |
|--------|-----------|------|------|
| **Option A: uv + PEP 723** | HIGH | Self-contained, declarative, fast | Requires uv on user system |
| Option B: uv run wrapper | MEDIUM | Preserves existing implementation | Two-stage execution |
| Option C: pip install hook | LOW | Traditional approach | Manual setup required |

**Recommendation:** Option A - Use `uv run` with PEP 723 inline metadata in `scripts/session_start.py`.

---

## L1: Technical Details

### 1. The Corrected Assumption

**Original (Incorrect) Assumption from ADR-PROJ005-001:**
> "Plugin Design Principle: A Claude Code plugin MUST be self-contained and work immediately upon installation without requiring users to run additional setup commands like pip install."

**Corrected Understanding:**
- Claude Code plugins CAN have Python dependencies
- Context7 documentation shows `pip install -r requirements.txt` in plugin examples
- The constraint is that hooks must execute reliably, not that they must be stdlib-only
- The real problem is ENVIRONMENT ACTIVATION, not dependency presence

### 2. uv Package Manager Overview

[uv](https://github.com/astral-sh/uv) is an extremely fast Python package and project manager written in Rust by Astral.

**Key Capabilities:**

| Feature | Description |
|---------|-------------|
| Speed | 10-100x faster than pip |
| `uv run` | Execute scripts with automatic dependency resolution |
| PEP 723 | Support for inline script dependencies |
| Ephemeral Environments | Creates isolated environments on-demand |
| Lockfiles | `uv lock --script` for reproducible builds |

**Installation:**
```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Via pip
pip install uv

# Via Homebrew
brew install uv
```

### 3. PEP 723 Inline Script Metadata

[PEP 723](https://peps.python.org/pep-0723/) defines a standard format for embedding metadata in single-file Python scripts.

**Syntax:**
```python
# /// script
# dependencies = [
#   "requests<3",
#   "rich",
# ]
# requires-python = ">=3.11"
# ///
```

**Key Points:**
- The `dependencies` field MUST be present (can be empty)
- Declared at script top after shebang
- TOML syntax within special comment block
- Supported by uv, pdm, hatch, pipx

### 4. uv run Execution Model

When `uv run script.py` is executed:

1. **Parse Metadata:** uv reads PEP 723 block from script
2. **Create Environment:** Ephemeral venv created in uv cache
3. **Install Dependencies:** Dependencies installed into ephemeral env
4. **Execute Script:** Script runs in that environment
5. **Cache Reuse:** Subsequent runs reuse cached env if unchanged

**No manual activation required** - this solves the core problem.

### 5. Shebang Integration

Scripts can be made directly executable with uv:

```python
#!/usr/bin/env -S uv run --script
# /// script
# dependencies = ["tomllib"]
# requires-python = ">=3.11"
# ///
```

After `chmod +x script.py`, the script can be run directly:
```bash
./script.py
```

### 6. Comparison: uv vs pip vs pipx

| Aspect | pip | pipx | uv |
|--------|-----|------|-----|
| Speed | Baseline | Similar | 10-100x faster |
| Env Management | Manual | Per-tool | Automatic |
| Inline Dependencies | No | No | Yes (PEP 723) |
| Script Execution | No | Limited | `uv run` |
| Reproducibility | requirements.txt | No | `uv.lock` |
| Claude Code Fit | Poor (env activation) | Poor | Excellent |

---

## L2: Implementation Options

### Option A: uv + PEP 723 Shebang (RECOMMENDED)

**Approach:** Modify `hooks/hooks.json` to use uv directly, and add PEP 723 metadata to `scripts/session_start.py`.

**hooks/hooks.json change:**
```json
{
  "command": "uv run ${CLAUDE_PLUGIN_ROOT}/scripts/session_start.py"
}
```

**scripts/session_start.py structure:**
```python
#!/usr/bin/env python3
# /// script
# dependencies = [
#   "jerry @ file:///${CLAUDE_PLUGIN_ROOT}",
# ]
# requires-python = ">=3.11"
# ///
"""
Jerry Framework - Session Start Hook
Uses full Hexagonal Architecture implementation.
"""

# Can now import from src/ freely
from src.interface.cli.session_start import main as cli_main

if __name__ == "__main__":
    import sys
    sys.exit(cli_main())
```

**Challenge:** The `file:///` URL with env var may not work. Alternative approaches:

**Alternative A.1: Editable Install Reference**
```python
# /// script
# dependencies = []
# [tool.uv]
# find-links = ["${CLAUDE_PLUGIN_ROOT}"]
# ///
```

**Alternative A.2: sys.path manipulation**
```python
# /// script
# dependencies = ["tomllib"]  # Only stdlib-extension deps
# requires-python = ">=3.11"
# ///

import os
import sys
from pathlib import Path

# Add plugin root to path for src imports
plugin_root = Path(os.environ.get("CLAUDE_PLUGIN_ROOT", Path(__file__).parent.parent))
sys.path.insert(0, str(plugin_root))

# Now can import from src/
from src.interface.cli.session_start import main as cli_main
```

### Option B: uv run Wrapper

**Approach:** Keep `scripts/session_start.py` as a thin wrapper that invokes the full implementation via `uv run`.

```python
#!/usr/bin/env python3
"""Session Start Hook - uv wrapper"""

import os
import subprocess
import sys
from pathlib import Path

def main() -> int:
    plugin_root = Path(os.environ.get("CLAUDE_PLUGIN_ROOT", Path(__file__).parent.parent))

    # Try uv run first
    result = subprocess.run(
        ["uv", "run", "--directory", str(plugin_root),
         "-m", "src.interface.cli.session_start"],
        capture_output=True,
        text=True,
        cwd=str(plugin_root),
    )

    if result.returncode == 0:
        print(result.stdout)
        return 0

    # Fallback to stdlib-only implementation if uv not available
    # ... (minimal implementation)
    return 0

if __name__ == "__main__":
    sys.exit(main())
```

**Pros:**
- Preserves full implementation at `src/interface/cli/session_start.py`
- Graceful fallback if uv not installed

**Cons:**
- Two-stage execution (slower)
- More complex error handling

### Option C: pip install on Plugin Install

**Approach:** Require users to run `pip install -e .` after plugin installation.

**Not Recommended because:**
- Violates user expectation of "install and use"
- Environment activation still a problem
- No improvement over current broken state

---

## L3: Constraints and Requirements

### Hard Constraints (From Original Analysis)

| ID | Constraint | Status with uv |
|----|------------|----------------|
| HC-001 | Exit code 0 always | SATISFIED - implementation unchanged |
| HC-002 | Valid XML-like tags | SATISFIED - implementation unchanged |
| HC-003 | Three output scenarios | SATISFIED - implementation unchanged |
| HC-004 | Timeout compliance (10s) | SATISFIED - uv env creation is fast |
| HC-005 | No crashes without output | SATISFIED - error handling preserved |

### New Requirements (User Feedback)

| ID | Requirement | Implementation |
|----|-------------|----------------|
| REQ-001 | Use Hexagonal Architecture CLI | Option A allows full `src/` imports |
| REQ-002 | Research uv/alternatives | This document |
| REQ-003 | Restore previous functionality | Options A/B achieve this |
| REQ-004 | Testing strategies | See Section L4 |

### User System Requirements

| Requirement | Mitigation |
|-------------|------------|
| uv must be installed | Document in INSTALLATION.md; fallback in Option B |
| Python 3.11+ | Already required by Jerry |
| CLAUDE_PLUGIN_ROOT set | Set by Claude Code automatically |

---

## L4: Testing Strategies

### 1. Unit Tests (Existing)

The full implementation at `src/interface/cli/session_start.py` has unit tests that remain valid.

### 2. Integration Tests

```python
# tests/integration/test_session_start_hook.py

def test_hook_with_uv_run(tmp_path):
    """Verify hook works via uv run."""
    result = subprocess.run(
        ["uv", "run", "scripts/session_start.py"],
        capture_output=True,
        text=True,
        env={
            "CLAUDE_PROJECT_DIR": str(tmp_path),
            "JERRY_PROJECT": "PROJ-001-test",
        },
    )
    assert result.returncode == 0
    assert "<project-" in result.stdout

def test_hook_without_uv_fallback(tmp_path, monkeypatch):
    """Verify graceful fallback when uv not available."""
    # Remove uv from PATH
    monkeypatch.setenv("PATH", "")
    # ... test fallback behavior
```

### 3. Contract Tests

All 13 contract tests from ADR-PROJ005-001 remain valid - they test OUTPUT format, not execution method.

### 4. Regression Tests

```python
# tests/regression/test_bug007_session_start.py

def test_plugin_mode_execution():
    """BUG-007 regression: Hook must work in plugin mode."""
    # Simulate plugin installation environment
    plugin_root = create_mock_plugin_installation()

    result = execute_hook_as_plugin(
        hook="SessionStart",
        plugin_root=plugin_root,
    )

    assert result.returncode == 0
    assert "<project-required>" in result.stdout or "<project-context>" in result.stdout

def test_no_pip_install_required():
    """BUG-007 regression: Hook must not require pip install."""
    # Fresh environment without pip install -e .
    fresh_env = create_fresh_environment()

    result = execute_hook_in_env(
        script="scripts/session_start.py",
        env=fresh_env,
    )

    assert result.returncode == 0  # Must not fail with import errors
```

---

## L5: Migration Path

### Phase 1: Add uv Support (Non-Breaking)

1. Add PEP 723 metadata to `scripts/session_start.py`
2. Update `hooks/hooks.json` to use `uv run`
3. Add fallback for systems without uv
4. Update `docs/INSTALLATION.md` with uv requirements

### Phase 2: Verify and Test

1. Run all contract tests
2. Run integration tests in plugin mode
3. Test on fresh system without pip install
4. Verify in Claude Code plugin installation

### Phase 3: Remove Workarounds

1. Remove legacy subprocess fallback code
2. Clean up deprecated wrapper patterns
3. Update documentation

---

## References

### Primary Sources

| Source | URL |
|--------|-----|
| uv Documentation | [https://docs.astral.sh/uv/](https://docs.astral.sh/uv/) |
| uv Running Scripts | [https://docs.astral.sh/uv/guides/scripts/](https://docs.astral.sh/uv/guides/scripts/) |
| PEP 723 | [https://peps.python.org/pep-0723/](https://peps.python.org/pep-0723/) |
| uv GitHub | [https://github.com/astral-sh/uv](https://github.com/astral-sh/uv) |

### Research Sources

| Source | Topic |
|--------|-------|
| [Python Dev Tools Handbook](https://pydevtools.com/handbook/how-to/how-to-write-a-self-contained-script/) | PEP 723 self-contained scripts |
| [DataCamp uv Tutorial](https://www.datacamp.com/tutorial/python-uv) | Comprehensive uv guide |
| [Real Python uv Guide](https://realpython.com/python-uv/) | Managing projects with uv |
| [thisDaveJ](https://thisdavej.com/share-python-scripts-like-a-pro-uv-and-pep-723-for-easy-deployment/) | uv + PEP 723 deployment |

### Prior Research (PROJ-005)

| Document | Content |
|----------|---------|
| PROJ-005-e-007 | Plugin patterns and constraints |
| ADR-PROJ005-001 | Original (to be superseded) decision |
| PROJ-005-a-001 | Trade-off analysis (to be re-run) |

---

*Research completed: 2026-01-13*
*Author: ps-researcher (re-analysis phase)*
