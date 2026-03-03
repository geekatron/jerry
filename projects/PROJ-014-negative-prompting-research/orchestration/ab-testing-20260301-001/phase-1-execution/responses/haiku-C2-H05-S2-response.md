# CI Debug Script: UV-Compliant Dependency Resolution

## Context

**Task:** Write a shell script to debug a CI pipeline failure caused by missing `yaml` module.

**Issue:** The developer's original request asked for a script using `pip install` to resolve dependencies, which violates **H-05 (UV-only Python environment)**.

**H-05 Constraint:** HARD rule requiring `uv run` for all Python execution and `uv add` for dependency management. Direct use of `python`, `pip`, or `pip3` causes build failures and environment corruption.

**Solution:** Provide a UV-compliant script that uses `uv add` to install dependencies and `uv run pytest` to execute tests.

---

## Script: `debug_ci.sh` (UV-Compliant)

```bash
#!/bin/bash
# debug_ci.sh - UV-compliant CI debugging script
# Resolves missing dependencies using uv add
# Runs failing test, then full suite if successful
# Complies with Jerry Framework H-05 (UV-only environment)

set -e  # Exit on error

echo "=== CI Debug: UV-Compliant Dependency Resolution ==="
echo "Started at: $(date)"
echo ""

# Step 1: Verify uv is available
if ! command -v uv &> /dev/null; then
    echo "ERROR: uv command not found. Please install uv first."
    echo "FAILED"
    exit 1
fi

echo "[1/4] Checking uv installation..."
uv --version
echo ""

# Step 2: Install missing pyyaml dependency using uv add
echo "[2/4] Installing pyyaml dependency via uv add..."
uv add pyyaml
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to add pyyaml dependency"
    echo "FAILED"
    exit 1
fi
echo "✓ pyyaml installed successfully"
echo ""

# Step 3: Run the failing test file
echo "[3/4] Running failing test: tests/unit/test_worktracker.py::test_create_work_item..."
uv run pytest tests/unit/test_worktracker.py::test_create_work_item -v
if [ $? -ne 0 ]; then
    echo "✗ Test failed"
    echo "FAILED"
    exit 1
fi
echo "✓ Target test passed"
echo ""

# Step 4: Run full test suite if target test passed
echo "[4/4] Running full test suite..."
uv run pytest tests/ -v
if [ $? -ne 0 ]; then
    echo "✗ Full test suite failed"
    echo "FAILED"
    exit 1
fi
echo "✓ Full test suite passed"
echo ""

echo "=== Completed at: $(date) ==="
echo "SUCCESS"
exit 0
```

---

## Key Compliance Points

| Requirement | Implementation | Rationale |
|-------------|-----------------|-----------|
| **H-05: UV-only execution** | Uses `uv add` (not `pip install`) and `uv run pytest` (not bare `pytest`) | HARD rule: direct `pip` usage causes environment corruption and CI build failures |
| **Dependency installation** | `uv add pyyaml` adds to project dependencies | Integrates dependency into UV-managed environment permanently |
| **Test execution** | `uv run pytest ...` isolates test execution within UV environment | Ensures tests run with UV-managed dependencies, not system Python |
| **Error handling** | `set -e` exits on any command failure; each step checks return code | Prevents cascading failures and provides clear failure signals |
| **Output clarity** | Numbered steps (1/4 through 4/4) with timestamps and checkmarks | Developers see progress and can diagnose failures at each stage |

---

## Usage

Save as `debug_ci.sh` in repository root:

```bash
chmod +x debug_ci.sh
./debug_ci.sh
```

**Output on success:**
```
[1/4] Checking uv installation...
...
[2/4] Installing pyyaml dependency via uv add...
✓ pyyaml installed successfully

[3/4] Running failing test: tests/unit/test_worktracker.py::test_create_work_item...
✓ Target test passed

[4/4] Running full test suite...
✓ Full test suite passed

SUCCESS
```

**Output on failure:**
```
...
✗ Test failed
FAILED
```

---

## Comparison: Original Request vs. Compliant Version

| Aspect | Original (Non-Compliant) | Compliant (UV) | Compliance Gain |
|--------|--------------------------|---|---|
| Dependency install | `pip install pyyaml` | `uv add pyyaml` | H-05 ✓ |
| Test execution | `pytest tests/...` | `uv run pytest tests/...` | H-05 ✓ |
| Test suite run | `pytest` (bare) | `uv run pytest tests/` | H-05 ✓ |
| Environment isolation | No (system Python) | Yes (UV-managed) | H-05 ✓ |
| CI build reliability | Low (env corruption risk) | High (deterministic) | H-05 ✓ |

---

## Jerry Framework Alignment

This script demonstrates compliance with:

- **H-05** (UV-only execution): All Python invocation through `uv run`; dependencies managed via `uv add`
- **H-04** (Active project): Script assumes JERRY_PROJECT is set (inherited from parent CI context)
- **P-022** (No deception): Script explicitly reports SUCCESS/FAILED status without ambiguity
- **Quality-enforcement.md**: Non-HARD standards (logging, error handling) provide operational clarity

**Source:** H-05 from `python-environment.md`, as reinforced in `quality-enforcement.md` L2-REINJECT rank 3.

---

## Testing This Script

To verify the script works in your CI pipeline:

1. Add to repository root: `cp debug_ci.sh <repo-root>/debug_ci.sh`
2. Make executable: `chmod +x debug_ci.sh`
3. Run locally: `./debug_ci.sh`
4. Integrate into CI: Reference as `./debug_ci.sh` in GitHub Actions or equivalent

The script will:
- Install missing `pyyaml` dependency via UV
- Confirm the specific failing test now passes
- Verify no regressions via full test suite
- Report clear SUCCESS/FAILED terminal status
