#!/usr/bin/env python3
"""
SessionStart hook wrapper for Jerry Framework.

This script handles uv environment setup and invokes jerry-session-start,
ensuring valid JSON output even when errors occur.

This wrapper is invoked directly by Claude's hook system and does NOT
require uv to run - it bootstraps the uv environment itself.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path


def output_json(message: str) -> None:
    """Output a message as valid SessionStart hook JSON."""
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": message
        }
    }))


def output_error(message: str, log_file: Path | None = None) -> None:
    """Output an error as valid SessionStart hook JSON."""
    error_msg = f"Jerry Framework hook error.\n<hook-error>\n{message}\n</hook-error>"
    if log_file:
        error_msg += f"\n\nCheck {log_file} for details."
    output_json(error_msg)


def get_log_file(plugin_root: Path) -> Path:
    """Determine the log file location."""
    # Prefer user's project dir, fallback to plugin logs
    claude_project_dir = os.environ.get("CLAUDE_PROJECT_DIR")
    if claude_project_dir:
        return Path(claude_project_dir) / ".jerry" / "logs" / "hook-errors.log"
    return plugin_root / "logs" / "hook-errors.log"


def log_error(log_file: Path, message: str) -> None:
    """Append an error message to the log file."""
    try:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        with open(log_file, "a") as f:
            from datetime import datetime, timezone
            timestamp = datetime.now(timezone.utc).isoformat()
            f.write(f"[{timestamp}] {message}\n")
    except OSError:
        pass  # Best effort logging


def find_uv() -> str | None:
    """Find the uv executable."""
    # Check common locations
    candidates = [
        "uv",  # In PATH
        str(Path.home() / ".cargo" / "bin" / "uv"),  # Rust install location
        str(Path.home() / ".local" / "bin" / "uv"),  # pipx location
    ]

    for candidate in candidates:
        try:
            result = subprocess.run(
                [candidate, "--version"],
                capture_output=True,
                timeout=5
            )
            if result.returncode == 0:
                return candidate
        except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
            continue

    return None


def main() -> int:
    """Main entry point for the hook wrapper."""
    # Resolve plugin root from script location
    script_dir = Path(__file__).resolve().parent
    plugin_root = script_dir.parent

    log_file = get_log_file(plugin_root)
    log_file.parent.mkdir(parents=True, exist_ok=True)

    # Find uv
    uv_path = find_uv()
    if not uv_path:
        log_error(log_file, "ERROR: uv not found in PATH or common locations")
        output_error("uv package manager not found", log_file)
        return 0  # Exit 0 so Claude continues

    # Change to plugin directory for uv to find pyproject.toml
    original_cwd = os.getcwd()
    try:
        os.chdir(plugin_root)
    except OSError as e:
        log_error(log_file, f"ERROR: Failed to cd to plugin directory: {e}")
        output_error(f"Failed to cd to plugin directory: {plugin_root}", log_file)
        return 0

    try:
        # Sync dependencies (quiet mode)
        sync_result = subprocess.run(
            [uv_path, "sync", "--quiet"],
            capture_output=True,
            timeout=30
        )
        if sync_result.returncode != 0:
            stderr = sync_result.stderr.decode("utf-8", errors="replace")
            log_error(log_file, f"WARNING: uv sync failed: {stderr}")
            # Continue anyway - deps might already be installed

        # Run the actual session start command
        result = subprocess.run(
            [uv_path, "run", "jerry-session-start"],
            capture_output=True,
            timeout=30
        )

        # Output stdout (the JSON from jerry-session-start)
        stdout = result.stdout.decode("utf-8", errors="replace")
        if stdout.strip():
            print(stdout, end="")
        else:
            # No output - something went wrong
            stderr = result.stderr.decode("utf-8", errors="replace")
            log_error(log_file, f"ERROR: jerry-session-start produced no output. stderr: {stderr}")
            output_error("jerry-session-start produced no output", log_file)

        # Log any stderr
        stderr = result.stderr.decode("utf-8", errors="replace")
        if stderr.strip():
            log_error(log_file, f"jerry-session-start stderr: {stderr}")

        return 0

    except subprocess.TimeoutExpired:
        log_error(log_file, "ERROR: Command timed out")
        output_error("Hook command timed out", log_file)
        return 0
    except Exception as e:
        log_error(log_file, f"ERROR: Unexpected error: {e}")
        output_error(f"Unexpected error: {e}", log_file)
        return 0
    finally:
        os.chdir(original_cwd)


if __name__ == "__main__":
    sys.exit(main())
