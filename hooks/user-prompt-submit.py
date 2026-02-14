#!/usr/bin/env -S uv run python
"""
UserPromptSubmit hook for L2 Per-Prompt Quality Reinforcement.

This hook runs on every user prompt submission and injects critical
quality rules as additionalContext. It reads L2-REINJECT markers from
quality-enforcement.md and assembles a token-budgeted preamble.

The hook is fail-open by design: on ANY error, it returns a valid
empty JSON response and logs the error to stderr. User work is
NEVER blocked.

Claude Code Hook Protocol:
    - Reads JSON from stdin (contains prompt info)
    - Writes JSON to stdout with hookSpecificOutput.additionalContext
    - Exit code 0 always (fail-open)

References:
    - EN-705: L2 Per-Prompt Reinforcement Hook
    - ADR-EPIC002-002: 5-layer enforcement architecture
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


def main() -> int:
    """Main hook entry point.

    Reads stdin, generates reinforcement content, writes JSON to stdout.
    On any error, outputs an empty passthrough response.

    Returns:
        Exit code (always 0 for fail-open behavior).
    """
    try:
        # Read hook input from stdin (Claude Code protocol)
        # We don't need the input data, but must consume stdin
        sys.stdin.read()

        # Add project root to path for src imports
        project_root = Path(__file__).resolve().parent.parent
        if str(project_root) not in sys.path:
            sys.path.insert(0, str(project_root))

        from src.infrastructure.internal.enforcement.prompt_reinforcement_engine import (
            PromptReinforcementEngine,
        )

        engine = PromptReinforcementEngine()
        result = engine.generate_reinforcement()

        if result.preamble:
            output = {
                "hookSpecificOutput": {
                    "additionalContext": (
                        f"<quality-reinforcement>\n{result.preamble}\n</quality-reinforcement>"
                    ),
                },
            }
            print(
                f"L2 reinforce: {result.items_included}/{result.items_total} items, "
                f"~{result.token_estimate} tokens",
                file=sys.stderr,
            )
        else:
            # No reinforcement content available; passthrough
            output = {}

        print(json.dumps(output))
        return 0

    except Exception as e:
        # Fail-open: log error to stderr, return empty response
        print(
            json.dumps({"warning": f"L2 reinforcement error: {e}"}),
            file=sys.stderr,
        )
        print(json.dumps({}))
        return 0


if __name__ == "__main__":
    sys.exit(main())
