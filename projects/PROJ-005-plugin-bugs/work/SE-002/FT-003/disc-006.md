# DISC-006: Duplicate tests/ Folders Investigation

> **Discovery ID:** DISC-006
> **Type:** Discovery
> **Status:** DOCUMENTED
> **Feature:** [FT-003](./FEATURE-WORKTRACKER.md)
> **Discovered:** 2026-01-13
> **Last Updated:** 2026-01-13

---

## Summary

Investigation revealed two `tests/` folders exist in the repository with different purposes and pytest only discovers one of them.

---

## Findings

### 1. Root `tests/` Folder

**Location:** `/tests/`
**Purpose:** Comprehensive test suite for `src/` codebase
**Test Count:** ~100+ test files
**Structure:**
- `tests/architecture/` - Architecture boundary tests
- `tests/e2e/` - End-to-end tests
- `tests/hooks/` - Hook tests
- `tests/infrastructure/` - Infrastructure adapter tests
- `tests/integration/` - Integration tests
- `tests/interface/cli/` - CLI tests
- `tests/project_validation/` - Project validation tests
- `tests/session_management/` - Session management tests (includes session_start.py tests)
- `tests/shared_kernel/` - Shared kernel tests
- `tests/unit/` - Unit tests
- `tests/work_tracking/` - Work tracking tests

**pytest Configuration:** Discovered automatically via `testpaths = ["tests"]`

### 2. `scripts/tests/` Folder

**Location:** `/scripts/tests/`
**Purpose:** Tests specifically for `scripts/` directory modules
**Test Count:** 2 test files
**Files:**
- `test_hooks.py` (11KB) - Tests for `scripts/pre_tool_use.py`, `scripts/post_tool_use.py`
- `test_patterns.py` (9KB) - Tests for `scripts/patterns.py`

**pytest Configuration:** **NOT discovered** - Not in `testpaths`

### 3. pytest Configuration

```ini
# pytest.ini
[pytest]
testpaths = tests

# pyproject.toml
[tool.pytest.ini_options]
testpaths = ["tests"]
```

**Implication:** `scripts/tests/` tests are NOT run automatically with `pytest`.

---

## Analysis

### Why Two Folders Exist

The `scripts/tests/` folder was likely created for isolation:
- Scripts in `scripts/` are meant to be standalone (no pip install)
- Testing them separately ensures they don't accidentally depend on `src/`
- Different execution context (shell scripts vs Python modules)

### Current Risk

| Risk | Severity | Mitigation |
|------|----------|------------|
| `scripts/tests/` not run in CI | HIGH | Add to pytest config or create separate CI job |
| Test rot in `scripts/tests/` | MEDIUM | Include in regular test runs |
| Confusion about test locations | LOW | Document in README |

---

## Recommendations

### Option A: Consolidate (Recommended)

Move `scripts/tests/` into `tests/scripts/`:
```
tests/scripts/
├── test_hooks.py
└── test_patterns.py
```

**Pros:**
- Single test suite
- Automatic pytest discovery
- Consistent structure

**Cons:**
- May break relative imports in test files
- Requires test file updates

### Option B: Update pytest Config

Add `scripts/tests` to testpaths:
```ini
testpaths = ["tests", "scripts/tests"]
```

**Pros:**
- No file moves needed
- Quick fix

**Cons:**
- Two test locations remain confusing
- Different conventions in different folders

### Option C: Separate CI Job

Keep as-is but add dedicated CI job for `scripts/tests/`:
```yaml
- name: Test scripts
  run: pytest scripts/tests/
```

**Pros:**
- Maintains isolation intent
- Clear separation of concerns

**Cons:**
- Two test runs
- Easy to forget

---

## Decision

**Deferred** - This is out of scope for SE-002. Recommend creating a separate tech debt item to address.

---

## Related Artifacts

| Type | Location | Description |
|------|----------|-------------|
| pytest.ini | `/pytest.ini` | Current pytest config |
| pyproject.toml | `/pyproject.toml` | Python project config |
| scripts/tests/ | `/scripts/tests/` | Scripts test folder |

---

## Change Log

| Date | Change | Author |
|------|--------|--------|
| 2026-01-13 | Created DISC-006 during FT-003 investigation | Claude |
