#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak
"""SubagentStop lifecycle hook wrapper. Delegates to jerry hooks subagent-stop.

Records sub-agent completion for context monitoring.
Timeout budget: wrapper subprocess=4s < hooks.json=5s (1s buffer).
"""

import os
import subprocess
import sys
from pathlib import Path

root = os.environ.get("CLAUDE_PLUGIN_ROOT", str(Path(__file__).resolve().parent.parent))
try:
    result = subprocess.run(
        ["uv", "run", "--directory", root, "jerry", "--json", "hooks", "subagent-stop"],
        input=sys.stdin.buffer.read(),
        capture_output=True,
        timeout=4,
    )
    sys.stdout.buffer.write(result.stdout)
    if result.stderr:
        sys.stderr.buffer.write(result.stderr)
except Exception:
    # Fail-open: approve on any error
    print('{"decision": "approve"}')
sys.exit(0)
