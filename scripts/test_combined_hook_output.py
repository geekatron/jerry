#!/usr/bin/env python3
"""
TEST SCRIPT: Empirical test for combined systemMessage + hookSpecificOutput.

PURPOSE:
    Verify whether Claude Code SessionStart hooks can output BOTH:
    - systemMessage (shown to user in terminal)
    - hookSpecificOutput.additionalContext (sent to Claude's context)

HYPOTHESIS:
    Based on documentation, systemMessage is a "common field for ALL hooks",
    so it should work with SessionStart's hookSpecificOutput.additionalContext.

TEST METHOD:
    1. This script outputs JSON with both fields
    2. User runs new Claude Code session
    3. Observe:
       - Does systemMessage appear in terminal?
       - Does additionalContext reach Claude's context?

EXPECTED BEHAVIOR (if hypothesis is correct):
    - Terminal shows: "TEST: systemMessage field is working..."
    - Claude receives: "<test-context>...</test-context>"

DISCOVERY: To be documented in disc-005-combined-hook-output-test.md
"""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone


def main() -> int:
    """Output combined JSON for testing."""

    timestamp = datetime.now(timezone.utc).isoformat()
    project = os.environ.get("JERRY_PROJECT", "NOT_SET")

    # The systemMessage should appear in the user's terminal
    system_message = f"""TEST: systemMessage field is working!

Timestamp: {timestamp}
JERRY_PROJECT: {project}

If you see this in your terminal, systemMessage works with SessionStart hooks."""

    # The additionalContext should be sent to Claude
    additional_context = f"""TEST: additionalContext field is working!

<test-context>
TestTimestamp: {timestamp}
TestProject: {project}
TestPurpose: Verify combined systemMessage + hookSpecificOutput.additionalContext
</test-context>

If Claude can see this, additionalContext works alongside systemMessage."""

    # Combined output - testing both fields together
    output = {
        "systemMessage": system_message,
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": additional_context
        }
    }

    print(json.dumps(output, indent=2))
    return 0


if __name__ == "__main__":
    exit(main())
