"""
Jerry CLI - Primary Adapter for Command-Line Interface

This module provides the main entry point for the Jerry CLI tool.
It follows hexagonal architecture principles: thin adapter that translates
CLI protocol to use case calls.

Usage:
    jerry --help              # Show help
    jerry --version           # Show version
    jerry init                # Display project context
    jerry projects list       # List all projects
    jerry projects validate   # Validate a project

Exit Codes:
    0: Success
    1: Error (validation failure, project not found, etc.)
    2: Invalid usage (bad arguments)
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

# Application layer imports (use cases)
from src.session_management.application import (
    GetProjectContextQuery,
    ScanProjectsQuery,
    ValidateProjectQuery,
)

# Infrastructure layer imports (adapters)
from src.session_management.infrastructure import (
    FilesystemProjectAdapter,
    OsEnvironmentAdapter,
)

# Version from pyproject.toml (hardcoded for v0.0.1, will be dynamic later)
__version__ = "0.0.1"


def get_projects_directory() -> str:
    """Determine the projects directory path.

    Returns:
        Absolute path to the projects directory
    """
    import os

    # Try CLAUDE_PROJECT_DIR first (set by Claude Code)
    project_root = os.environ.get("CLAUDE_PROJECT_DIR")
    if project_root:
        return str(Path(project_root) / "projects")

    # Fallback: current working directory
    return str(Path.cwd() / "projects")


def create_parser() -> argparse.ArgumentParser:
    """Create the argument parser for the CLI.

    Returns:
        Configured ArgumentParser instance
    """
    parser = argparse.ArgumentParser(
        prog="jerry",
        description="Jerry Framework CLI - Project and workflow management",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    jerry init                           # Show current project context
    jerry projects list                  # List all available projects
    jerry projects validate PROJ-001     # Validate a specific project
    jerry --json projects list           # Output as JSON for scripting
        """,
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"jerry {__version__}",
    )

    parser.add_argument(
        "--json",
        action="store_true",
        help="Output in JSON format for scripting",
    )

    # Subparsers for command groups
    subparsers = parser.add_subparsers(
        title="commands",
        dest="command",
        metavar="<command>",
    )

    # init command
    subparsers.add_parser(
        "init",
        help="Display current project context",
        description="Show the current project context including JERRY_PROJECT setting.",
    )

    # projects command group
    projects_parser = subparsers.add_parser(
        "projects",
        help="Project management commands",
        description="Commands for listing and validating projects.",
    )

    projects_subparsers = projects_parser.add_subparsers(
        title="subcommands",
        dest="projects_command",
        metavar="<subcommand>",
    )

    projects_subparsers.add_parser(
        "list",
        help="List all available projects",
        description="Scan and display all valid projects in the projects/ directory.",
    )

    validate_parser = projects_subparsers.add_parser(
        "validate",
        help="Validate a specific project",
        description="Check that a project exists and has required configuration.",
    )
    validate_parser.add_argument(
        "project_id",
        help="Project ID to validate (e.g., PROJ-001-my-project)",
    )

    return parser


def format_project_table(projects: list) -> str:
    """Format projects as a readable table.

    Args:
        projects: List of ProjectInfo objects

    Returns:
        Formatted table string
    """
    if not projects:
        return "No projects found."

    lines = ["ID                              STATUS      PATH"]
    lines.append("-" * 60)

    for p in projects:
        status = p.status.name.lower()
        path = f"projects/{p.id}/"
        lines.append(f"{str(p.id):<32}{status:<12}{path}")

    return "\n".join(lines)


def cmd_init(args: argparse.Namespace) -> int:
    """Execute the init command.

    Args:
        args: Parsed command-line arguments

    Returns:
        Exit code (0 for success)
    """
    # Wire dependencies (composition root pattern)
    repository = FilesystemProjectAdapter()
    environment = OsEnvironmentAdapter()
    projects_dir = get_projects_directory()

    # Execute query
    query = GetProjectContextQuery(
        repository=repository,
        environment=environment,
        base_path=projects_dir,
    )

    try:
        context = query.execute()
    except Exception as e:
        if args.json:
            print(json.dumps({"error": str(e)}))
        else:
            print(f"Error: {e}", file=sys.stderr)
        return 1

    # Format output
    if args.json:
        output: dict[str, Any] = {
            "jerry_project": context["jerry_project"],
            "project_id": str(context["project_id"]) if context["project_id"] else None,
            "validation": {
                "is_valid": context["validation"].is_valid,
                "messages": context["validation"].messages,
            }
            if context["validation"]
            else None,
            "available_projects": [
                {"id": str(p.id), "status": p.status.name}
                for p in context["available_projects"]
            ],
            "next_number": context["next_number"],
        }
        print(json.dumps(output, indent=2))
    else:
        jerry_project = context["jerry_project"]
        project_id = context["project_id"]
        validation = context["validation"]

        if jerry_project is None:
            print("JERRY_PROJECT: (not set)")
            print("\nSet JERRY_PROJECT environment variable to activate a project.")
            print("\nAvailable projects:")
            print(format_project_table(context["available_projects"]))
        elif project_id and validation and validation.is_valid:
            print(f"JERRY_PROJECT: {jerry_project}")
            print(f"Project Path: projects/{project_id}/")
            print("Status: Valid")
            if validation.has_warnings:
                print(f"Warnings: {'; '.join(validation.messages)}")
        else:
            print(f"JERRY_PROJECT: {jerry_project}")
            print("Status: Invalid")
            if validation:
                print(f"Error: {validation.first_message}")

    return 0


def cmd_projects_list(args: argparse.Namespace) -> int:
    """Execute the projects list command.

    Args:
        args: Parsed command-line arguments

    Returns:
        Exit code (0 for success)
    """
    repository = FilesystemProjectAdapter()
    projects_dir = get_projects_directory()

    query = ScanProjectsQuery(
        repository=repository,
        base_path=projects_dir,
    )

    try:
        projects = query.execute()
    except Exception as e:
        if args.json:
            print(json.dumps({"error": str(e)}))
        else:
            print(f"Error: {e}", file=sys.stderr)
        return 1

    if args.json:
        output = {
            "projects": [
                {
                    "id": str(p.id),
                    "status": p.status.name,
                    "path": f"projects/{p.id}/",
                }
                for p in projects
            ],
            "count": len(projects),
        }
        print(json.dumps(output, indent=2))
    else:
        print(format_project_table(projects))
        print(f"\nTotal: {len(projects)} project(s)")

    return 0


def cmd_projects_validate(args: argparse.Namespace) -> int:
    """Execute the projects validate command.

    Args:
        args: Parsed command-line arguments

    Returns:
        Exit code (0 for valid, 1 for invalid)
    """
    repository = FilesystemProjectAdapter()
    projects_dir = get_projects_directory()

    query = ValidateProjectQuery(
        repository=repository,
        base_path=projects_dir,
        project_id_str=args.project_id,
    )

    try:
        project_id, validation = query.execute()
    except Exception as e:
        if args.json:
            print(json.dumps({"error": str(e)}))
        else:
            print(f"Error: {e}", file=sys.stderr)
        return 1

    if args.json:
        output = {
            "project_id": str(project_id) if project_id else None,
            "is_valid": validation.is_valid,
            "messages": validation.messages,
        }
        print(json.dumps(output, indent=2))
    else:
        if project_id is None:
            print(f"Invalid project ID format: {args.project_id}")
            print(f"Error: {validation.first_message}")
        elif validation.is_valid:
            print(f"Project: {project_id}")
            print("Status: Valid")
            if validation.has_warnings:
                print(f"Warnings: {'; '.join(validation.messages)}")
        else:
            print(f"Project: {project_id}")
            print("Status: Invalid")
            print(f"Error: {validation.first_message}")

    return 0 if validation.is_valid else 1


def main() -> int:
    """Main entry point for the Jerry CLI.

    Returns:
        Exit code
    """
    parser = create_parser()
    args = parser.parse_args()

    # No command specified - show help
    if args.command is None:
        parser.print_help()
        return 0

    # Route to command handler
    if args.command == "init":
        return cmd_init(args)
    elif args.command == "projects":
        if args.projects_command is None:
            # Show projects subcommand help
            # Re-parse with projects --help
            parser.parse_args(["projects", "--help"])
            return 0
        elif args.projects_command == "list":
            return cmd_projects_list(args)
        elif args.projects_command == "validate":
            return cmd_projects_validate(args)

    # Unknown command
    parser.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
