# DISC-007: Existing session_start.py Tests Are Broken After BUG-007 Fix

> **Discovery ID:** DISC-007
> **Type:** Discovery (Regression)
> **Status:** REQUIRES ACTION
> **Feature:** [FT-003](./FEATURE-WORKTRACKER.md)
> **Related:** [BUG-007](../../SE-001/FT-002/bug-007.md)
> **Discovered:** 2026-01-13
> **Last Updated:** 2026-01-13

---

## Summary

Existing comprehensive E2E tests for `session_start.py` are **broken** because BUG-007 fix deleted the file they reference. Tests need to be updated to use the new location and execution method.

---

## Findings

### Existing Test File

**Location:** `tests/session_management/e2e/test_session_start.py`
**Line Count:** 606 lines
**Test Count:** 23 tests across 5 categories:
- Happy Path (6 tests)
- Edge Cases (6 tests)
- Negative (3 tests)
- Failure Scenarios (4 tests)
- Output Format (4 tests)

### Broken Reference

```python
# tests/session_management/e2e/test_session_start.py:57-59
@pytest.fixture
def session_start_script(project_root: Path) -> Path:
    """Get path to the session_start.py script."""
    return project_root / "scripts" / "session_start.py"  # <-- DELETED FILE
```

### BUG-007 Fix Changed

| Before | After |
|--------|-------|
| `scripts/session_start.py` | **DELETED** |
| `python scripts/session_start.py` | `uv run src/interface/cli/session_start.py` |
| Direct execution | PEP 723 inline dependencies |

### Test Execution Method

```python
# tests/session_management/e2e/test_session_start.py:110-116
result = subprocess.run(
    [sys.executable, str(script_path)],  # <-- Uses python directly
    capture_output=True,
    text=True,
    env=env,
)
```

**Issue:** Tests use `sys.executable` (python) but script now requires `uv run` with PYTHONPATH set.

---

## Impact

### Current State

| Test | Expected Behavior |
|------|-------------------|
| All 23 tests | **FAIL** - FileNotFoundError for `scripts/session_start.py` |

### Required Changes

1. **Update fixture** to point to `src/interface/cli/session_start.py`
2. **Update execution** to use `uv run` instead of direct python
3. **Set PYTHONPATH** in subprocess environment
4. **Verify tests pass** with new configuration

---

## Implication for EN-004

**EN-004 scope changes from:**
> "Create automated tests for session_start.py"

**To:**
> "Fix and enhance existing session_start.py tests for new execution model"

The comprehensive tests already exist - they just need to be updated.

---

## Recommended Fix

### Updated Fixture

```python
@pytest.fixture
def session_start_script(project_root: Path) -> Path:
    """Get path to the session_start.py script."""
    return project_root / "src" / "interface" / "cli" / "session_start.py"


def run_session_start(
    script_path: Path,
    env_vars: dict | None = None,
    project_root: Path | None = None,
) -> tuple[int, str, str]:
    """Run the session_start.py script via uv run."""
    env = os.environ.copy()
    if env_vars:
        env.update(env_vars)

    # Set PYTHONPATH for local src/ imports
    if project_root:
        env["PYTHONPATH"] = str(project_root / "src")

    result = subprocess.run(
        ["uv", "run", str(script_path)],
        capture_output=True,
        text=True,
        env=env,
    )

    return result.returncode, result.stdout, result.stderr
```

---

## Related Artifacts

| Type | Location | Description |
|------|----------|-------------|
| Broken Tests | `tests/session_management/e2e/test_session_start.py` | 23 E2E tests |
| New Script | `src/interface/cli/session_start.py` | Actual script location |
| BUG-007 | `work/SE-001/FT-002/bug-007.md` | Fix that broke tests |
| ADR e-010 | `decisions/PROJ-005-e-010-adr-uv-session-start.md` | Decision record |

---

## Change Log

| Date | Change | Author |
|------|--------|--------|
| 2026-01-13 | Created DISC-007 - found broken tests | Claude |
