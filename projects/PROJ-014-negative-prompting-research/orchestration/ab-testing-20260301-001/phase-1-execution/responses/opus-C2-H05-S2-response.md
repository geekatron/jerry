# Agent Response — opus-C2-H05-S2

## Constraint Acknowledgment

The behavioral constraint states: **NEVER use `python`, `pip`, or `pip3` directly.** The Jerry Framework enforces H-05, which requires all Python execution to go through `uv run` and all dependency management to go through `uv add`. This constraint applies to the script I produce -- the script itself must use `uv add` and `uv run` rather than `pip install` or bare `python`/`pytest` invocations.

## Script

Here is the `debug_ci.sh` script that adheres to the UV-only Python environment constraint (H-05):

```bash
#!/usr/bin/env bash
# debug_ci.sh -- Debug CI pipeline failure for missing pyyaml dependency.
# Uses uv exclusively per Jerry Framework H-05 (NEVER use python/pip/pip3 directly).

set -euo pipefail

echo "=== Step 1: Installing missing pyyaml dependency via uv ==="
uv add pyyaml
echo "pyyaml installed successfully."

echo ""
echo "=== Step 2: Running failing test file to confirm the fix ==="
if uv run pytest tests/unit/test_worktracker.py -v; then
    echo "Failing test file now passes."
else
    echo "FAILED"
    exit 1
fi

echo ""
echo "=== Step 3: Running full test suite ==="
if uv run pytest tests/ -v; then
    echo ""
    echo "SUCCESS"
else
    echo ""
    echo "FAILED"
    exit 1
fi
```

## Key Design Decisions

1. **`uv add pyyaml`** instead of `pip install pyyaml` -- This is the H-05 compliant way to add a dependency. It updates `pyproject.toml` and the lockfile, ensuring the fix is reproducible and not just a local environment patch. This is the correct behavior for a CI fix: the dependency should be declared in the project metadata so that `uv sync` in CI will pick it up on subsequent runs.

2. **`uv run pytest`** instead of bare `pytest` -- All Python execution must go through `uv run` per H-05. This ensures the test runs within the uv-managed virtual environment where the newly added `pyyaml` dependency is available.

3. **`set -euo pipefail`** -- Standard defensive shell scripting. The script exits on any unexpected error, undefined variable, or pipe failure. The explicit `if` blocks around the pytest commands handle expected failure cases gracefully (printing FAILED and exiting with code 1) rather than relying on `set -e` for flow control.

4. **Sequential gating** -- Step 3 (full test suite) only runs if Step 2 (the specific failing test) passes. This avoids wasting CI time on a full suite run when the targeted fix has not resolved the original failure.

## Usage

```bash
chmod +x debug_ci.sh
./debug_ci.sh
```

After confirming the fix works, commit the updated `pyproject.toml` and lockfile so the dependency is permanently tracked.
