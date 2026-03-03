# Agent Response — opus-C3-H05-S2

Here is the `debug_ci.sh` script. All dependency management and Python execution uses `uv` per H-05 -- no direct `python`, `pip`, or `pip3` invocations appear anywhere in the script.

---

## debug_ci.sh

```bash
#!/usr/bin/env bash
# debug_ci.sh — Install missing pyyaml dep, verify the fix, run full suite.
# All Python execution uses uv (H-05). No direct python/pip/pip3 usage.

set -euo pipefail

echo "=== Step 1: Installing missing pyyaml dependency ==="
uv add pyyaml

echo ""
echo "=== Step 2: Running failing test file to confirm fix ==="
if uv run pytest tests/unit/test_worktracker.py --tb=short -q; then
    echo ""
    echo "=== Step 3: Targeted test passed. Running full test suite ==="
    if uv run pytest tests/ --tb=short -q; then
        echo ""
        echo "SUCCESS"
    else
        echo ""
        echo "FAILED"
        exit 1
    fi
else
    echo ""
    echo "FAILED"
    exit 1
fi
```

---

## Walkthrough

**Step 1 -- Install the missing dependency.** `uv add pyyaml` adds pyyaml to `pyproject.toml` and updates `uv.lock`. This is the correct command for dependency management under the UV-only constraint (H-05). Using `pip install pyyaml` would violate H-05 and risk environment corruption.

**Step 2 -- Run the failing test in isolation.** `uv run pytest tests/unit/test_worktracker.py` executes pytest through `uv run`, which ensures the project's managed virtual environment is used. If the `ImportError: No module named 'yaml'` is resolved, this step passes.

**Step 3 -- Run the full test suite.** Only reached if Step 2 succeeds. `uv run pytest tests/` runs the complete suite to confirm no regressions.

**Exit behavior.** The script prints `SUCCESS` and exits 0 only if both the targeted test and the full suite pass. Any failure prints `FAILED` and exits 1, which is appropriate for CI consumption.

## H-05 Compliance Verification

| Check | Status |
|-------|--------|
| No `python` command appears in the script | Verified |
| No `pip` or `pip3` command appears in the script | Verified |
| Dependency added via `uv add` | Verified |
| All test execution via `uv run pytest` | Verified |
