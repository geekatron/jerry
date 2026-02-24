#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak
"""Stop hook gate wrapper. Delegates to jerry hooks stop.

Blocks Claude from stopping at EMERGENCY tier to force checkpoint.
Timeout budget: wrapper subprocess=4s < hooks.json=5s (1s buffer).
"""

import os
import subprocess
import sys
from pathlib import Path

root = os.environ.get("CLAUDE_PLUGIN_ROOT", str(Path(__file__).resolve().parent.parent))
try:
    result = subprocess.run(
        ["uv", "run", "--directory", root, "jerry", "--json", "hooks", "stop"],
        input=sys.stdin.buffer.read(),
        capture_output=True,
        timeout=4,
    )
    sys.stdout.buffer.write(result.stdout)
    if result.stderr:
        sys.stderr.buffer.write(result.stderr)
except Exception:
    # Fail-open: allow stop on any error
    print('{"decision": "approve"}')
sys.exit(0)
