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
    jerry-session-start  # Via entry point (preferred)
    python -m src.interface.cli.session_start  # Via module

Environment Variables:
    JERRY_PROJECT: The project ID to use (optional)
    CLAUDE_PROJECT_DIR: The project root directory (set by Claude Code)
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

from src.session_management.application import GetProjectContextQuery
from src.session_management.infrastructure import FilesystemProjectAdapter, OsEnvironmentAdapter


def get_projects_directory() -> str:
    """Determine the projects directory path.

    Returns:
        Absolute path to the projects directory
    """
    # Try CLAUDE_PROJECT_DIR first (set by Claude Code)
    project_root = os.environ.get("CLAUDE_PROJECT_DIR")
    if project_root:
        return str(Path(project_root) / "projects")

    # Fallback: current working directory (assumes run from project root)
    return str(Path.cwd() / "projects")


def format_project_list(projects: list) -> str:
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


def output_project_active(context: dict) -> None:
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


def output_project_required(context: dict) -> None:
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


def output_project_error(context: dict) -> None:
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

    Returns:
        Exit code (always 0 - we want Claude to handle issues)
    """
    # Wire up dependencies
    repository = FilesystemProjectAdapter()
    environment = OsEnvironmentAdapter()
    projects_dir = get_projects_directory()

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

    # Determine output based on context
    jerry_project = context["jerry_project"]
    project_id = context["project_id"]
    validation = context["validation"]

    if jerry_project is None:
        # No project set - require selection
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
