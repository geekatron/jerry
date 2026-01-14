"""
Jerry Framework - Session Start Hook

This module is executed by the SessionStart hook to validate project context
and produce structured output for Claude to consume.

Exit Codes:
    0: Success (always - we want Claude to handle any issues)

Output Format:
    Structured XML-like tags that Claude parses to determine action:
    - <project-context>: When JERRY_PROJECT is set and valid
    - <project-required>: When project selection is needed
    - <project-error>: When JERRY_PROJECT is set but invalid

Usage:
    uv run src/interface/cli/session_start.py  # Via uv run (preferred)
    python -m src.interface.cli.session_start  # Via module (requires pip install -e .)

Environment Variables:
    JERRY_PROJECT: The project ID to use (optional)
    CLAUDE_PROJECT_DIR: The project root directory (set by Claude Code)

Configuration Precedence (WI-015):
    1. JERRY_PROJECT environment variable (highest priority)
    2. Local context: .jerry/local/context.toml (worktree-specific)
    3. Project discovery (prompts user)

References:
    - WI-015: Update session_start.py Hook
    - ADR-PROJ004-004: JerrySession Context (5-level precedence)
    - PROJ-004-e-004: Configuration Precedence research
    - ADR e-010: uv Session Start solution
"""

# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///

from __future__ import annotations

import json
import os
import sys
import tomllib
from pathlib import Path
from typing import Any

from src.infrastructure.adapters.configuration.layered_config_adapter import (
    LayeredConfigAdapter,
)
from src.infrastructure.adapters.persistence.atomic_file_adapter import (
    AtomicFileAdapter,
)
from src.session_management.application import GetProjectContextQuery
from src.session_management.infrastructure import FilesystemProjectAdapter, OsEnvironmentAdapter


def get_project_root() -> Path:
    """Determine the project root directory.

    Returns:
        Path to the project root directory
    """
    # Try CLAUDE_PROJECT_DIR first (set by Claude Code)
    project_root = os.environ.get("CLAUDE_PROJECT_DIR")
    if project_root:
        return Path(project_root)

    # Fallback: current working directory (assumes run from project root)
    return Path.cwd()


def get_projects_directory() -> str:
    """Determine the projects directory path.

    Returns:
        Absolute path to the projects directory
    """
    return str(get_project_root() / "projects")


def get_local_context_path() -> Path:
    """Get the path to the worktree-local context file.

    Returns:
        Path to .jerry/local/context.toml
    """
    return get_project_root() / ".jerry" / "local" / "context.toml"


def load_local_context() -> dict[str, Any]:
    """Load worktree-local context from .jerry/local/context.toml.

    Uses AtomicFileAdapter for safe concurrent access.

    Returns:
        Parsed context dict, or empty dict if file missing/invalid

    References:
        - AC-015.2: Reads context.active_project from local config
        - ADR-PROJ004-004: WorktreeInfo and local context
    """
    path = get_local_context_path()
    if not path.exists():
        return {}

    try:
        file_adapter = AtomicFileAdapter()
        content = file_adapter.read_with_lock(path)
        if not content.strip():
            return {}
        return tomllib.loads(content)
    except (tomllib.TOMLDecodeError, OSError):
        return {}


def get_active_project_from_local_context() -> str | None:
    """Get the active project ID from local context.

    Returns:
        Project ID if set in local context, None otherwise

    References:
        - AC-015.2: Reads context.active_project from local config
    """
    context = load_local_context()
    return context.get("context", {}).get("active_project")


def create_config_provider() -> LayeredConfigAdapter:
    """Create a configuration provider with proper precedence.

    Returns:
        LayeredConfigAdapter configured with root and project paths

    References:
        - AC-015.1: Uses LayeredConfigAdapter to load configuration
        - ADR-PROJ004-004: 5-level configuration precedence
    """
    root = get_project_root()
    return LayeredConfigAdapter(
        env_prefix="JERRY_",
        root_config_path=root / ".jerry" / "config.toml",
        defaults={
            "logging.level": "INFO",
            "work_tracking.auto_snapshot_interval": 10,
            "work_tracking.quality_gate_enabled": True,
            "session.auto_start": True,
            "session.max_duration_hours": 8,
        },
    )


def format_project_list(projects: list[Any]) -> str:
    """Format projects as a readable list for output.

    Args:
        projects: List of ProjectInfo objects

    Returns:
        Formatted string with one project per line
    """
    if not projects:
        return "  (no projects found)"

    lines = []
    for p in projects:
        status_icon = {
            "IN_PROGRESS": "[ACTIVE]",
            "COMPLETED": "[DONE]",
            "DRAFT": "[DRAFT]",
            "ARCHIVED": "[ARCHIVED]",
            "UNKNOWN": "[?]",
        }.get(p.status.name, "[?]")
        lines.append(f"  - {p.id} {status_icon}")
    return "\n".join(lines)


def output_project_active(context: dict[str, Any]) -> None:
    """Output structured message for active project.

    Args:
        context: Project context dictionary
    """
    project_id = context["project_id"]
    validation = context["validation"]

    print("Jerry Framework initialized. See CLAUDE.md for context.")
    print("<project-context>")
    print(f"ProjectActive: {project_id}")
    print(f"ProjectPath: projects/{project_id}/")

    if validation and validation.is_valid:
        if validation.has_warnings:
            print(f"ValidationWarnings: {'; '.join(validation.messages)}")
        else:
            print("ValidationMessage: Project is properly configured")
    print("</project-context>")


def output_project_required(context: dict[str, Any]) -> None:
    """Output structured message when project selection is required.

    Args:
        context: Project context dictionary
    """
    projects = context["available_projects"]
    next_num = context["next_number"]

    # Create JSON representation for parsing
    projects_json = json.dumps([{"id": str(p.id), "status": p.status.name} for p in projects])

    print("Jerry Framework initialized.")
    print("<project-required>")
    print("ProjectRequired: true")
    print("AvailableProjects:")
    print(format_project_list(projects))
    print(f"NextProjectNumber: {next_num:03d}")
    print(f"ProjectsJson: {projects_json}")
    print("</project-required>")
    print()
    print("ACTION REQUIRED: No JERRY_PROJECT environment variable set.")
    print(
        "Claude MUST use AskUserQuestion to help the user select an existing project or create a new one."
    )
    print("DO NOT proceed with any work until a project is selected.")


def output_project_error(context: dict[str, Any]) -> None:
    """Output structured message for invalid project.

    Args:
        context: Project context dictionary
    """
    jerry_project = context["jerry_project"]
    validation = context["validation"]
    projects = context["available_projects"]
    next_num = context["next_number"]

    print("Jerry Framework initialized with ERROR.")
    print("<project-error>")
    print(f"InvalidProject: {jerry_project}")

    if validation:
        print(f"Error: {validation.first_message or 'Unknown validation error'}")
    else:
        print("Error: Project validation failed")

    print("AvailableProjects:")
    print(format_project_list(projects))
    print(f"NextProjectNumber: {next_num:03d}")
    print("</project-error>")
    print()
    print("ACTION REQUIRED: The specified JERRY_PROJECT is invalid.")
    print("Claude MUST use AskUserQuestion to help the user select or create a valid project.")


def main() -> int:
    """Main entry point for the session start hook.

    Configuration Precedence (WI-015):
        1. JERRY_PROJECT environment variable (highest priority)
        2. Local context: .jerry/local/context.toml (worktree-specific)
        3. Project discovery (prompts user)

    Returns:
        Exit code (always 0 - we want Claude to handle issues)

    References:
        - AC-015.1: Uses LayeredConfigAdapter to load configuration
        - AC-015.2: Reads JERRY_PROJECT from env or context.active_project
        - AC-015.3: Falls back to project discovery if no active project
        - AC-015.5: Backward compatible with existing env var workflow
    """
    # Wire up dependencies
    repository = FilesystemProjectAdapter()
    projects_dir = get_projects_directory()

    # Priority 1: Check JERRY_PROJECT environment variable (AC-015.5: backward compatible)
    jerry_project_env = os.environ.get("JERRY_PROJECT")

    # Priority 2: Check local context if env var not set (AC-015.2)
    effective_jerry_project = jerry_project_env
    project_source = "environment"

    if not effective_jerry_project:
        local_project = get_active_project_from_local_context()
        if local_project:
            effective_jerry_project = local_project
            project_source = "local_context"

    # Create environment adapter that respects our precedence
    # If we found project in local context, temporarily set it in env for the query
    if effective_jerry_project and project_source == "local_context":
        os.environ["JERRY_PROJECT"] = effective_jerry_project

    environment = OsEnvironmentAdapter()

    # Execute the query
    query = GetProjectContextQuery(
        repository=repository,
        environment=environment,
        base_path=projects_dir,
    )

    try:
        context = query.execute()
    except Exception as e:
        # If we can't even execute the query, output minimal info
        print("Jerry Framework initialized with ERROR.")
        print("<project-error>")
        print(f"Error: Failed to scan projects: {e}")
        print("</project-error>")
        print()
        print("ACTION REQUIRED: Could not access projects directory.")
        print("Check that the projects/ directory exists and is accessible.")
        return 0
    finally:
        # Clean up: restore original env if we modified it
        if project_source == "local_context":
            if jerry_project_env is None:
                os.environ.pop("JERRY_PROJECT", None)
            else:
                os.environ["JERRY_PROJECT"] = jerry_project_env

    # Determine output based on context
    jerry_project = context["jerry_project"]
    project_id = context["project_id"]
    validation = context["validation"]

    if jerry_project is None:
        # No project set - require selection (AC-015.3)
        output_project_required(context)
    elif project_id is not None and validation is not None and validation.is_valid:
        # Valid project set
        output_project_active(context)
    else:
        # Invalid project set
        output_project_error(context)

    return 0


if __name__ == "__main__":
    sys.exit(main())
