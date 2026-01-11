#!/usr/bin/env python3
"""
Jerry Framework - Session Start Hook (Legacy Wrapper)

DEPRECATED: This script is a legacy wrapper. The actual implementation
has been moved to src/interface/cli/session_start.py.

Preferred usage:
    jerry-session-start              # Via installed entry point
    python -m src.interface.cli.session_start  # Via module

This wrapper exists for backwards compatibility and will be removed
in a future version. Update your hooks to use the entry point instead.

See: .claude/settings.json for hook configuration
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def main() -> int:
    """Run the session start hook via the installed entry point or module."""
    project_root = Path(__file__).parent.parent

    # Try installed entry point first (preferred)
    venv_entry_point = project_root / ".venv" / "bin" / "jerry-session-start"
    if venv_entry_point.exists():
        result = subprocess.run([str(venv_entry_point)], cwd=str(project_root))
        return result.returncode

    # Fallback: try running as module with venv python
    venv_python = project_root / ".venv" / "bin" / "python"
    if venv_python.exists():
        result = subprocess.run(
            [str(venv_python), "-m", "src.interface.cli.session_start"],
            cwd=str(project_root),
        )
        return result.returncode

    # Last resort: try system python with module (requires pip install -e .)
    result = subprocess.run(
        [sys.executable, "-m", "src.interface.cli.session_start"],
        cwd=str(project_root),
    )
    return result.returncode


if __name__ == "__main__":
    sys.exit(main())
