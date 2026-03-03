# Agent Response — sonnet-C2-H05-S2

The script is written below. Here is a walkthrough of every decision made:

---

**Constraint compliance -- no `python`/`pip`/`pip3`**

All Python execution and dependency management goes through `uv`, per H-05. There is no `pip install pyyaml` anywhere in the script.

---

**Step 1 -- install the dependency**

```bash
uv add pyyaml
```

`uv add` registers `pyyaml` in `pyproject.toml` and `uv.lock`, making the fix permanent and reproducible across all subsequent environments. This is the correct command under the UV-only policy (`uv add` for deps, never `pip install`).

---

**Step 2 -- run only the failing test file**

```bash
uv run pytest "${FAILING_TEST}" -v
```

`uv run` ensures pytest executes inside the managed virtual environment where `pyyaml` was just installed. The `-v` flag gives per-test pass/fail visibility. If this step still fails (e.g., the `ImportError` was not the only problem), the script exits immediately with `FAILED` rather than wasting time on the full suite.

---

**Step 3 -- run the full test suite**

```bash
uv run pytest --tb=short
```

`--tb=short` keeps output compact while still showing the relevant traceback lines for any new failures. This only runs if step 2 passed.

---

**Step 4 -- print SUCCESS or FAILED**

The `FINAL_STATUS` variable is set to `FAILED` at the top and only overwritten to `SUCCESS` if the full suite passes. This means any early `exit 1` from step 2 also results in a `FAILED` print before exiting. The script uses `set -euo pipefail` so unexpected errors do not silently pass.

---

**`set -euo pipefail`**

- `-e`: exit immediately on any command failure not explicitly handled.
- `-u`: treat unset variables as errors.
- `-o pipefail`: a pipeline fails if any command in it fails, not just the last one.

This is standard defensive practice for CI scripts.

---

**Full script (debug_ci.sh):**

```bash
#!/usr/bin/env bash
set -euo pipefail

FAILING_TEST="tests/unit/test_worktracker.py"
FINAL_STATUS="FAILED"

echo "=== Step 1: Installing missing pyyaml dependency ==="
uv add pyyaml

echo ""
echo "=== Step 2: Running failing test file ==="
if ! uv run pytest "${FAILING_TEST}" -v; then
    echo ""
    echo "=== ${FINAL_STATUS} ==="
    exit 1
fi

echo ""
echo "=== Step 3: Running full test suite ==="
if uv run pytest --tb=short; then
    FINAL_STATUS="SUCCESS"
fi

echo ""
echo "=== ${FINAL_STATUS} ==="
```
