#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak
"""PreToolUse hook wrapper. Delegates to jerry hooks pre-tool-use.

Timeout budget: wrapper subprocess=4s < hooks.json=5s (1s buffer for wrapper overhead).
"""

import os
import subprocess
import sys
from pathlib import Path

root = os.environ.get("CLAUDE_PLUGIN_ROOT", str(Path(__file__).resolve().parent.parent))
try:
    result = subprocess.run(
        ["uv", "run", "--directory", root, "jerry", "--json", "hooks", "pre-tool-use"],
        input=sys.stdin.buffer.read(),
        capture_output=True,
        timeout=4,
    )
    sys.stdout.buffer.write(result.stdout)
    if result.stderr:
        sys.stderr.buffer.write(result.stderr)
except Exception:
    pass
sys.exit(0)
