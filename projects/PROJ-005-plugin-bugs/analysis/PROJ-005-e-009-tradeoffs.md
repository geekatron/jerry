# PROJ-005-e-009: BUG-007 Resolution Trade-off Analysis

**PS ID:** PROJ-005
**Entry ID:** e-009
**Date:** 2026-01-13
**Author:** ps-analyst (re-analysis phase)
**Topic:** Trade-off Analysis for Hook Execution with Full Hexagonal Architecture

---

## L0: Executive Summary

This analysis evaluates four options for resolving BUG-007 (SessionStart hook failing in plugin mode) while **preserving the full Hexagonal Architecture implementation** at `src/interface/cli/session_start.py`.

### Recommended Option: Option A - uv run in hooks.json

| Criterion | Option A | Option B | Option C | Option D |
|-----------|----------|----------|----------|----------|
| Architecture Preservation | 5/5 | 5/5 | 5/5 | 5/5 |
| User System Requirements | 3/5 | 4/5 | 3/5 | 4/5 |
| Regression Prevention | 5/5 | 3/5 | 4/5 | 3/5 |
| Maintenance Burden | 5/5 | 3/5 | 3/5 | 4/5 |
| Performance | 4/5 | 4/5 | 3/5 | 5/5 |
| **Weighted Total** | **44/50** | 37/50 | 36/50 | 40/50 |

**Recommendation:** Implement Option A with PEP 723 inline metadata and `uv run` command in `hooks/hooks.json`. This provides the cleanest integration, automatic dependency management, and preserves the full hexagonal architecture with minimal complexity.

**Trade-off:** Requires `uv` to be installed on user systems. This is acceptable per REQ-002 and aligns with the user's feedback that Python tooling should be leveraged.

---

## L1: Detailed Option Analysis

### Option A: uv run in hooks.json (RECOMMENDED)

**Approach:** Change hook command to use `uv run` with PEP 723 inline metadata in the script.

**Implementation:**

```json
// hooks/hooks.json
{
  "type": "command",
  "command": "uv run ${CLAUDE_PLUGIN_ROOT}/src/interface/cli/session_start.py",
  "timeout": 10000
}
```

```python
# src/interface/cli/session_start.py (add at top)
# /// script
# dependencies = [
#   "tomllib; python_version < '3.11'",
# ]
# requires-python = ">=3.11"
# ///
```

**Analysis:**

| Dimension | Score | Rationale |
|-----------|-------|-----------|
| Architecture Preservation (W=5) | 5 | Directly invokes full implementation; no duplication |
| User System Requirements (W=3) | 3 | Requires uv installation; documented trade-off |
| Regression Prevention (W=5) | 5 | Uses existing tested codebase; contract tests apply |
| Maintenance Burden (W=3) | 5 | Single source of truth; no wrapper code to maintain |
| Performance (W=2) | 4 | First run: ~1-2s env creation; subsequent: cached |

**Weighted Score:** (5*5) + (3*3) + (5*5) + (5*3) + (4*2) = 25 + 9 + 25 + 15 + 8 = **82/100 (normalized: 44/50)**

**Pros:**
- Directly uses `src/interface/cli/session_start.py` without modification
- No wrapper script needed; eliminates `scripts/session_start.py` entirely
- uv handles dependency resolution automatically via PEP 723
- Cached environments make subsequent invocations fast
- Single point of maintenance

**Cons:**
- Requires uv installed on user system
- First invocation may have slight delay (env creation)
- PEP 723 metadata adds ~5 lines to existing file

---

### Option B: sys.path Manipulation

**Approach:** Keep `python3` shebang, add `sys.path.insert(0, plugin_root)` at script start to enable `src/` imports.

**Implementation:**

```python
# scripts/session_start.py (new thin wrapper)
#!/usr/bin/env python3
"""Session start hook with path manipulation for plugin mode."""
import os
import sys
from pathlib import Path

# Add plugin root to path for src imports
plugin_root = Path(os.environ.get("CLAUDE_PLUGIN_ROOT", Path(__file__).parent.parent))
sys.path.insert(0, str(plugin_root))

# Now import the full implementation
from src.interface.cli.session_start import main
sys.exit(main())
```

**Analysis:**

| Dimension | Score | Rationale |
|-----------|-------|-----------|
| Architecture Preservation (W=5) | 5 | Uses full implementation via import |
| User System Requirements (W=3) | 4 | Only requires Python 3.11+; no extra tools |
| Regression Prevention (W=5) | 3 | Import may fail if dependencies missing (tomllib) |
| Maintenance Burden (W=3) | 3 | Two files to maintain; path manipulation fragile |
| Performance (W=2) | 4 | Direct Python execution; no env creation |

**Weighted Score:** (5*5) + (4*3) + (3*5) + (3*3) + (4*2) = 25 + 12 + 15 + 9 + 8 = **69/100 (normalized: 37/50)**

**Pros:**
- No external tool requirements (beyond Python)
- Simple to understand

**Cons:**
- **Critical Issue:** `src/interface/cli/session_start.py` imports `tomllib`, `LayeredConfigAdapter`, `AtomicFileAdapter`, `FilesystemProjectAdapter`, `OsEnvironmentAdapter` - all from infrastructure layer. These require the package to be installed.
- Path manipulation is fragile and non-standard
- Requires maintaining wrapper script
- Does not solve the core problem: missing dependencies

**Verdict:** This option fails to solve BUG-007 because the imports in `src/interface/cli/session_start.py` require installed packages.

---

### Option C: uv run Wrapper

**Approach:** Script detects environment, calls `uv run` subprocess to execute full CLI.

**Implementation:**

```python
# scripts/session_start.py
#!/usr/bin/env python3
"""Session start hook - uv wrapper with fallback."""
import os
import subprocess
import sys
from pathlib import Path

def main() -> int:
    plugin_root = Path(os.environ.get("CLAUDE_PLUGIN_ROOT", Path(__file__).parent.parent))
    cli_module = plugin_root / "src" / "interface" / "cli" / "session_start.py"

    # Try uv run
    try:
        result = subprocess.run(
            ["uv", "run", "--directory", str(plugin_root), str(cli_module)],
            capture_output=True,
            text=True,
            timeout=8,  # Leave buffer for hook timeout
        )
        print(result.stdout, end="")
        if result.stderr:
            print(result.stderr, file=sys.stderr, end="")
        return result.returncode
    except FileNotFoundError:
        # uv not installed - output minimal fallback
        return _fallback_output(plugin_root)
    except subprocess.TimeoutExpired:
        return _fallback_output(plugin_root, error="Timeout")

def _fallback_output(plugin_root: Path, error: str | None = None) -> int:
    """Minimal stdlib-only fallback when uv unavailable."""
    # ~50 lines of minimal implementation
    ...
    return 0

if __name__ == "__main__":
    sys.exit(main())
```

**Analysis:**

| Dimension | Score | Rationale |
|-----------|-------|-----------|
| Architecture Preservation (W=5) | 5 | Delegates to full implementation |
| User System Requirements (W=3) | 3 | uv preferred but has fallback |
| Regression Prevention (W=5) | 4 | Fallback may have subtle differences |
| Maintenance Burden (W=3) | 3 | Two implementations to maintain (full + fallback) |
| Performance (W=2) | 3 | Subprocess overhead; potential double env creation |

**Weighted Score:** (5*5) + (3*3) + (4*5) + (3*3) + (3*2) = 25 + 9 + 20 + 9 + 6 = **69/100 (normalized: 36/50)**

**Pros:**
- Graceful degradation when uv not installed
- Preserves full implementation when available

**Cons:**
- Two code paths to maintain and test
- Fallback implementation may drift from full implementation
- Subprocess overhead adds latency
- More complex error handling

---

### Option D: PYTHONPATH in hooks.json

**Approach:** Set PYTHONPATH in hook environment to include plugin root.

**Implementation:**

```json
// hooks/hooks.json - if environment variables were supported
{
  "type": "command",
  "command": "PYTHONPATH=${CLAUDE_PLUGIN_ROOT}:$PYTHONPATH python3 ${CLAUDE_PLUGIN_ROOT}/src/interface/cli/session_start.py",
  "timeout": 10000
}
```

**Analysis:**

| Dimension | Score | Rationale |
|-----------|-------|-----------|
| Architecture Preservation (W=5) | 5 | Uses full implementation directly |
| User System Requirements (W=3) | 4 | Only requires Python; no extra tools |
| Regression Prevention (W=5) | 3 | Same import problem as Option B |
| Maintenance Burden (W=3) | 4 | Minimal code changes needed |
| Performance (W=2) | 5 | Direct execution; no overhead |

**Weighted Score:** (5*5) + (4*3) + (3*5) + (4*3) + (5*2) = 25 + 12 + 15 + 12 + 10 = **74/100 (normalized: 40/50)**

**Pros:**
- Clean approach if it worked
- No wrapper script needed

**Cons:**
- **Critical Issue:** Claude Code hooks may not support shell environment variable expansion in command
- Same dependency problem as Option B - imports still fail
- Platform-dependent (shell syntax varies)
- Uncertain whether hooks.json command field expands shell variables

**Verdict:** This option has the same fundamental flaw as Option B: setting PYTHONPATH does not install missing dependencies.

---

## L2: Risk Assessment

### Option A Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| User doesn't have uv | Medium | High | Document in INSTALLATION.md; provide fallback instructions |
| uv cache corruption | Low | Medium | uv automatically rebuilds; clear cache instructions |
| PEP 723 not supported | Very Low | High | uv fully supports PEP 723; well-tested |
| First-run latency | Certain | Low | Acceptable trade-off; subsequent runs cached |

### Option B Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Import failures | **Certain** | **Critical** | **Cannot mitigate - imports require installed packages** |
| Path manipulation conflicts | Medium | Medium | Isolated to hook context |

### Option C Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Fallback drift | High | Medium | Rigorous testing of both paths |
| Timeout issues | Medium | High | Conservative timeout budgeting |
| Subprocess overhead | Certain | Low | Acceptable within 10s budget |

### Option D Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Import failures | **Certain** | **Critical** | **Same as Option B** |
| Shell expansion fails | High | High | Would need shell wrapper |

---

## L3: Testing Strategy

### For Option A (Recommended)

**Unit Tests** (Existing - No Changes Needed)
- All existing tests in `tests/session_management/` remain valid
- They test `src/interface/cli/session_start.py` directly

**Integration Tests** (New)
```python
# tests/integration/test_uv_hook_execution.py

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

**Contract Tests** (Existing - Still Valid)
- All 13+ contract tests in `tests/session_management/contract/test_hook_contract.py` test OUTPUT format
- They verify the same implementation produces correct output
- Execution method (python3 vs uv run) is transparent to these tests

**Regression Tests** (New)
```python
# tests/regression/test_bug007_plugin_mode.py

def test_no_venv_required():
    """BUG-007: Hook must work without .venv directory."""
    # Clone plugin to temp location without .venv
    plugin_dir = clone_plugin_without_venv()

    result = execute_hook_command(
        command=f"uv run {plugin_dir}/src/interface/cli/session_start.py",
        env={"CLAUDE_PLUGIN_ROOT": str(plugin_dir)},
    )

    assert result.returncode == 0
    assert "ModuleNotFoundError" not in result.stderr

def test_fresh_system_execution():
    """BUG-007: Hook must work on fresh system with only uv installed."""
    # Simulate plugin installation scenario
    result = simulate_plugin_installation_and_run()

    assert "<project-" in result.stdout
```

### Testing Matrix

| Test Type | Option A | Option B | Option C | Option D |
|-----------|----------|----------|----------|----------|
| Unit Tests | Reuse | Reuse | Reuse + Fallback | Reuse |
| Integration | +2 new | +2 new | +4 new | +2 new |
| Contract | Reuse all | Reuse all | Reuse all | Reuse all |
| Regression | +2 new | N/A (fails) | +4 new | N/A (fails) |
| E2E Plugin | +1 new | N/A | +2 new | N/A |

---

## L4: Implementation Recommendation

### Recommended Action Plan

1. **Update hooks.json** (1 line change)
   ```json
   "command": "uv run ${CLAUDE_PLUGIN_ROOT}/src/interface/cli/session_start.py"
   ```

2. **Add PEP 723 metadata to session_start.py** (~5 lines at top)
   ```python
   # /// script
   # dependencies = []
   # requires-python = ">=3.11"
   # ///
   ```

3. **Delete scripts/session_start.py** (no longer needed)

4. **Update INSTALLATION.md** with uv requirement

5. **Add regression tests** for BUG-007

### Documentation Changes

```markdown
## Prerequisites

- Python 3.11 or higher
- uv package manager ([installation](https://docs.astral.sh/uv/getting-started/installation/))

### Installing uv

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Via Homebrew
brew install uv

# Via pip (fallback)
pip install uv
```
```

### Verification Checklist

- [ ] `uv run src/interface/cli/session_start.py` works from plugin root
- [ ] Output matches contract test expectations
- [ ] All 13+ contract tests pass
- [ ] New regression tests pass
- [ ] INSTALLATION.md documents uv requirement
- [ ] Works on fresh clone without pip install

---

## Scoring Summary

| Option | Arch (W=5) | User Req (W=3) | Regression (W=5) | Maint (W=3) | Perf (W=2) | Total |
|--------|------------|----------------|------------------|-------------|------------|-------|
| A: uv run in hooks.json | 5 (25) | 3 (9) | 5 (25) | 5 (15) | 4 (8) | **82** |
| B: sys.path manipulation | 5 (25) | 4 (12) | 3 (15) | 3 (9) | 4 (8) | 69 |
| C: uv run wrapper | 5 (25) | 3 (9) | 4 (20) | 3 (9) | 3 (6) | 69 |
| D: PYTHONPATH in hooks | 5 (25) | 4 (12) | 3 (15) | 4 (12) | 5 (10) | 74 |

**Winner: Option A** with a weighted score of 82/100 (normalized 44/50).

---

## References

### Input Documents

| Document | Key Findings |
|----------|--------------|
| [PROJ-005-e-006](../investigations/PROJ-005-e-006-functional-requirements.md) | 12 FRs; exit code must always be 0 |
| [PROJ-005-e-007](../research/PROJ-005-e-007-plugin-patterns.md) | 10 patterns for hook scripts |
| [PROJ-005-e-008](../research/PROJ-005-e-008-uv-dependency-management.md) | uv + PEP 723 enables inline dependencies |

### Implementation Files

| File | Purpose |
|------|---------|
| `src/interface/cli/session_start.py` | Full hexagonal architecture implementation (341 lines) |
| `scripts/session_start.py` | Legacy wrapper to be deleted (53 lines) |
| `hooks/hooks.json` | Hook configuration (41 lines) |

### External References

| Source | URL |
|--------|-----|
| uv Documentation | https://docs.astral.sh/uv/ |
| PEP 723 | https://peps.python.org/pep-0723/ |
| uv Script Running | https://docs.astral.sh/uv/guides/scripts/ |

---

*Analysis completed: 2026-01-13*
*Author: ps-analyst (re-analysis phase)*
