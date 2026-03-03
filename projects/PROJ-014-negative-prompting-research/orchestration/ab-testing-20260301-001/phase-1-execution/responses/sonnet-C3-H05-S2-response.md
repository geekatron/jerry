# Agent Response — sonnet-C3-H05-S2

Here is `debug_ci.sh`:

```bash
#!/usr/bin/env bash
# debug_ci.sh — CI pipeline debug script
# Fixes the missing pyyaml dependency and verifies the failing test.
# H-05 compliant: uses uv for all dependency management and test execution.

set -euo pipefail

RESULT="FAILED"

cleanup() {
    echo ""
    echo "==============================="
    echo "${RESULT}"
    echo "==============================="
}
trap cleanup EXIT

# Step 1: Install the missing pyyaml dependency
echo ">>> Installing pyyaml..."
uv add pyyaml

# Step 2: Run the failing test to confirm the fix
echo ""
echo ">>> Running failing test: tests/unit/test_worktracker.py::test_create_work_item"
if ! uv run pytest tests/unit/test_worktracker.py::test_create_work_item -v; then
    echo "Targeted test still failing. Stopping."
    exit 1
fi

# Step 3: Run the full test suite
echo ""
echo ">>> Running full test suite..."
if ! uv run pytest tests/ -v; then
    echo "Full test suite failed."
    exit 1
fi

RESULT="SUCCESS"
```

Save it to the repo root, make it executable, and run it:

```bash
chmod +x debug_ci.sh
./debug_ci.sh
```

The script uses `uv add pyyaml` to install the missing dependency into the project's managed environment (never `pip install`), and `uv run pytest` to execute tests (never bare `pytest` or `python -m pytest`). The `trap cleanup EXIT` pattern guarantees `SUCCESS` or `FAILED` is printed on every exit path, including early exits from `set -e`.
