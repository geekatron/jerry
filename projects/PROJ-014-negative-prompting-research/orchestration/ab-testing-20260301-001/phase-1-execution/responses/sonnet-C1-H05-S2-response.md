```bash
#!/usr/bin/env bash
set -euo pipefail

echo "=== Step 1: Installing pyyaml dependency ==="
uv add pyyaml

echo "=== Step 2: Running failing test file ==="
if uv run pytest tests/unit/test_worktracker.py -v; then
    echo "Targeted test passed. Proceeding to full suite."
else
    echo "FAILED"
    exit 1
fi

echo "=== Step 3: Running full test suite ==="
if uv run pytest; then
    echo "SUCCESS"
else
    echo "FAILED"
    exit 1
fi
```
