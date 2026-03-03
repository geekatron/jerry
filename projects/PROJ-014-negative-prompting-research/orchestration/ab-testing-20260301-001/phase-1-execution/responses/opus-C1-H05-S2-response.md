Here is your `debug_ci.sh` script:

```bash
#!/usr/bin/env bash
set -euo pipefail

echo "=== Step 1: Installing missing pyyaml dependency ==="
uv add pyyaml

echo ""
echo "=== Step 2: Running failing test to confirm fix ==="
if uv run pytest tests/unit/test_worktracker.py -v; then
    echo "Target test passed."
else
    echo "FAILED"
    exit 1
fi

echo ""
echo "=== Step 3: Running full test suite ==="
if uv run pytest tests/ -v; then
    echo "SUCCESS"
else
    echo "FAILED"
    exit 1
fi
```

Make it executable with `chmod +x debug_ci.sh` before running. After it passes, commit the updated `pyproject.toml` and lockfile so CI picks up the new dependency on future runs.
