#!/usr/bin/env python3
"""SessionStart hook wrapper. Delegates to jerry hooks session-start.

Timeout budget: wrapper subprocess=9s < hooks.json=10s (1s buffer for wrapper overhead).
"""
import os, subprocess, sys  # noqa: E401
from pathlib import Path
root = os.environ.get("CLAUDE_PLUGIN_ROOT", str(Path(__file__).resolve().parent.parent))
try:
    result = subprocess.run(
        ["uv", "run", "--directory", root, "jerry", "--json", "hooks", "session-start"],
        input=sys.stdin.buffer.read(), capture_output=True, timeout=9,
    )
    sys.stdout.buffer.write(result.stdout)
    if result.stderr:
        sys.stderr.buffer.write(result.stderr)
except Exception:
    pass
sys.exit(0)
