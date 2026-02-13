#!/usr/bin/env -S uv run python
"""
SessionStart hook wrapper for Jerry Framework.

This script handles uv environment setup and invokes the main Jerry CLI,
transforming the output to Claude Code's Advanced JSON format for hooks.

This wrapper is invoked directly by Claude's hook system and does NOT
require uv to run - it bootstraps the uv environment itself.

EN-001: Refactored to call 'jerry --json projects context' instead of
the deprecated 'jerry-session-start' entry point (TD-005).
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from datetime import UTC
from pathlib import Path


def output_json(system_message: str, additional_context: str) -> None:
    """Output combined format with BOTH systemMessage AND additionalContext.

    Per DISC-005 and AC-002/AC-003:
    - systemMessage: Shown to user in terminal at session start
    - additionalContext: Added to Claude's context window

    Both fields MUST be present for proper user and Claude visibility.
    """
    print(
        json.dumps(
            {
                "systemMessage": system_message,
                "hookSpecificOutput": {
                    "hookEventName": "SessionStart",
                    "additionalContext": additional_context,
                },
            }
        )
    )


def output_error(message: str, log_file: Path | None = None) -> None:
    """Output an error as valid SessionStart hook JSON with both fields."""
    # User-visible system message (concise)
    system_msg = f"Jerry Framework: Error - {message[:80]}"
    if log_file:
        system_msg += f" (see {log_file.name})"

    # Claude context (detailed with XML tags)
    additional_context = f"Jerry Framework hook error.\n<hook-error>\n{message}\n</hook-error>"
    if log_file:
        additional_context += f"\n\nCheck {log_file} for details."

    output_json(system_msg, additional_context)


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
            from datetime import datetime

            timestamp = datetime.now(UTC).isoformat()
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
            result = subprocess.run([candidate, "--version"], capture_output=True, timeout=5)
            if result.returncode == 0:
                return candidate
        except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
            continue

    return None


def check_precommit_hooks(plugin_root: Path) -> str | None:
    """Check if pre-commit hooks are installed.

    Returns warning message if hooks are missing, None if installed.
    """
    # Find the git hooks directory (handles worktrees)
    git_path = plugin_root / ".git"

    if git_path.is_file():
        # This is a worktree - .git is a file pointing to main repo
        try:
            content = git_path.read_text().strip()
            if content.startswith("gitdir:"):
                # Extract main .git path and find hooks
                gitdir = content.split(":", 1)[1].strip()
                # Go up from worktrees/<name> to .git/hooks
                main_git = Path(gitdir).parent.parent
                hooks_dir = main_git / "hooks"
            else:
                return None  # Can't determine hooks location
        except (OSError, IndexError):
            return None
    elif git_path.is_dir():
        hooks_dir = git_path / "hooks"
    else:
        return None  # Not a git repo

    # Check if pre-commit hook exists and is not a sample
    precommit_hook = hooks_dir / "pre-commit"
    if not precommit_hook.exists() or precommit_hook.name.endswith(".sample"):
        return (
            "Pre-commit hooks are NOT installed. Tests will not run before commits.\n"
            "Run 'make setup' to install dependencies and hooks.\n"
            "(Windows: uv sync && uv run pre-commit install)"
        )

    # Check for stale Python path in hook (common after worktree creation or venv rebuild)
    try:
        hook_content = precommit_hook.read_text(encoding="utf-8")
        for line in hook_content.splitlines():
            if line.startswith("INSTALL_PYTHON="):
                # Extract the path between quotes
                python_path = line.split("=", 1)[1].strip().strip("'\"")
                if python_path and not Path(python_path).exists():
                    return (
                        "Pre-commit hook has a stale Python path "
                        f"({python_path}).\n"
                        "This happens after creating a worktree or "
                        "rebuilding the venv.\n"
                        "Fix: uv sync && uv run pre-commit install"
                    )
                break
    except OSError:
        pass  # If we can't read the hook, don't block the session

    return None


def format_hook_output(cli_data: dict, precommit_warning: str | None = None) -> tuple[str, str]:
    """Transform CLI JSON output to (systemMessage, additionalContext) tuple.

    Per DISC-005 and AC-002/AC-003:
    - systemMessage: Concise message shown to user in terminal
    - additionalContext: Detailed XML-tagged context for Claude

    Returns:
        tuple[str, str]: (system_message, additional_context)
    """
    project_id = cli_data.get("jerry_project") or cli_data.get("project_id")
    project_path = cli_data.get("project_path", "")
    validation = cli_data.get("validation", {})
    available = cli_data.get("available_projects", [])

    # Build warning section if pre-commit hooks missing
    warning_section = ""
    if precommit_warning:
        warning_section = (
            f"\n<dev-environment-warning>\n{precommit_warning}\n</dev-environment-warning>\n"
        )

    # Case 1: Active project with valid configuration
    if project_id and validation and validation.get("is_valid"):
        system_msg = f"Jerry Framework: Project {project_id} active"
        additional = (
            f"Jerry Framework initialized. See CLAUDE.md for context.\n"
            f"<project-context>\n"
            f"ProjectActive: {project_id}\n"
            f"ProjectPath: {project_path}\n"
            f"ValidationMessage: Project is properly configured\n"
            f"</project-context>"
            f"{warning_section}"
        )
        return (system_msg, additional)

    # Case 2: Project set but invalid
    if project_id and validation and not validation.get("is_valid"):
        messages = validation.get("messages", ["Unknown validation error"])
        error_msg = messages[0] if messages else "Invalid project"
        system_msg = f"Jerry Framework: ERROR - {project_id} invalid ({error_msg[:40]})"
        additional = (
            f"Jerry Framework initialized with ERROR.\n"
            f"<project-error>\n"
            f"InvalidProject: {project_id}\n"
            f"Error: {error_msg}\n"
            f"AvailableProjects:\n"
            + "\n".join(f"  - {p['id']}" for p in available[:5])
            + "\n</project-error>\n\n"
            "ACTION REQUIRED: The specified project is invalid.\n"
            "Use AskUserQuestion to help the user select a valid project."
            f"{warning_section}"
        )
        return (system_msg, additional)

    # Case 3: No project set - prompt user selection
    projects_json = json.dumps(
        [{"id": p["id"], "status": p.get("status", "UNKNOWN")} for p in available[:10]]
    )
    next_num = cli_data.get("next_number", 1)
    project_count = len(available)
    system_msg = f"Jerry Framework: No project set ({project_count} available)"
    additional = (
        "Jerry Framework initialized.\n"
        "<project-required>\n"
        "ProjectRequired: true\n"
        "AvailableProjects:\n"
        + "\n".join(f"  - {p['id']} [{p.get('status', 'UNKNOWN')}]" for p in available[:5])
        + f"\nNextProjectNumber: {next_num:03d}\n"
        f"ProjectsJson: {projects_json}\n"
        f"</project-required>\n\n"
        f"ACTION REQUIRED: No JERRY_PROJECT environment variable set.\n"
        f"Claude MUST use AskUserQuestion to help the user select an existing project or create a new one.\n"
        f"DO NOT proceed with any work until a project is selected."
        f"{warning_section}"
    )
    return (system_msg, additional)


def main() -> int:
    """Main entry point for the hook wrapper."""
    # Resolve plugin root from script location
    script_dir = Path(__file__).resolve().parent
    plugin_root = script_dir.parent

    log_file = get_log_file(plugin_root)
    log_file.parent.mkdir(parents=True, exist_ok=True)

    # Debug: Log startup
    log_error(log_file, "DEBUG: Hook started")

    # Find uv
    uv_path = find_uv()
    if not uv_path:
        log_error(log_file, "ERROR: uv not found in PATH or common locations")
        output_error("uv package manager not found", log_file)
        return 0  # Exit 0 so Claude continues

    log_error(log_file, f"DEBUG: Found uv at {uv_path}")

    # Change to plugin directory for uv to find pyproject.toml
    original_cwd = os.getcwd()
    try:
        os.chdir(plugin_root)
    except OSError as e:
        log_error(log_file, f"ERROR: Failed to cd to plugin directory: {e}")
        output_error(f"Failed to cd to plugin directory: {plugin_root}", log_file)
        return 0

    log_error(log_file, f"DEBUG: Changed to {plugin_root}, original cwd: {original_cwd}")

    try:
        # Sync dependencies (quiet mode)
        log_error(log_file, "DEBUG: Starting uv sync...")
        sync_result = subprocess.run([uv_path, "sync", "--quiet"], capture_output=True, timeout=30)
        log_error(log_file, f"DEBUG: uv sync completed with rc={sync_result.returncode}")
        if sync_result.returncode != 0:
            stderr = sync_result.stderr.decode("utf-8", errors="replace")
            log_error(log_file, f"WARNING: uv sync failed: {stderr}")
            # Continue anyway - deps might already be installed

        # EN-001: Call main CLI instead of deprecated jerry-session-start
        log_error(log_file, "DEBUG: Starting jerry projects context...")
        result = subprocess.run(
            [uv_path, "run", "jerry", "--json", "projects", "context"],
            capture_output=True,
            timeout=30,
        )
        log_error(log_file, f"DEBUG: jerry CLI completed with rc={result.returncode}")

        stdout = result.stdout.decode("utf-8", errors="replace")

        if result.returncode != 0 or not stdout.strip():
            # CLI failed - output error in hook format
            stderr = result.stderr.decode("utf-8", errors="replace")
            log_error(
                log_file, f"ERROR: jerry CLI failed. rc={result.returncode}, stderr: {stderr}"
            )
            output_error(f"jerry CLI failed: {stderr or 'no output'}", log_file)
            return 0

        # Parse CLI JSON output
        try:
            cli_data = json.loads(stdout)
        except json.JSONDecodeError as e:
            log_error(log_file, f"ERROR: Invalid JSON from CLI: {e}")
            output_error(f"Invalid JSON from jerry CLI: {e}", log_file)
            return 0

        # Only check for pre-commit hooks if user is working IN the Jerry repository
        # This prevents the "run make setup" warning from appearing in other repos
        precommit_warning = None
        user_cwd = Path(original_cwd).resolve()
        jerry_root = plugin_root.resolve()
        if user_cwd == jerry_root or jerry_root in user_cwd.parents:
            precommit_warning = check_precommit_hooks(plugin_root)

        # Transform to hook format with BOTH systemMessage and additionalContext
        system_message, additional_context = format_hook_output(cli_data, precommit_warning)
        output_json(system_message, additional_context)

        # Log any stderr
        stderr = result.stderr.decode("utf-8", errors="replace")
        if stderr.strip():
            log_error(log_file, f"jerry CLI stderr: {stderr}")

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
