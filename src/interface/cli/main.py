"""
Jerry CLI - Primary Adapter for Command-Line Interface.

This module provides the main entry point for the Jerry CLI tool.
It follows hexagonal architecture principles:
- Bootstrap module creates and wires all dependencies
- CLIAdapter translates CLI protocol to use case calls via dispatcher
- main.py is a thin shell that routes to the adapter

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
import sys

from src.bootstrap import create_query_dispatcher, get_projects_directory
from src.interface.cli.adapter import CLIAdapter

# Version from pyproject.toml (hardcoded for v0.0.1, will be dynamic later)
__version__ = "0.0.1"


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


def create_cli_adapter() -> CLIAdapter:
    """Create a fully configured CLIAdapter.

    This is the composition root for the CLI interface.
    All dependencies are wired here via the bootstrap module.

    Returns:
        CLIAdapter with injected dispatcher and configuration
    """
    dispatcher = create_query_dispatcher()
    projects_dir = get_projects_directory()
    return CLIAdapter(dispatcher=dispatcher, projects_dir=projects_dir)


def main() -> int:
    """Main entry point for the Jerry CLI.

    Returns:
        Exit code
    """
    parser = create_parser()
    args = parser.parse_args()

    # Create adapter with all dependencies wired
    adapter = create_cli_adapter()

    # No command specified - show help
    if args.command is None:
        parser.print_help()
        return 0

    # Route to adapter methods
    if args.command == "init":
        return adapter.cmd_init(json_output=args.json)
    elif args.command == "projects":
        if args.projects_command is None:
            # Show projects subcommand help
            parser.parse_args(["projects", "--help"])
            return 0
        elif args.projects_command == "list":
            return adapter.cmd_projects_list(json_output=args.json)
        elif args.projects_command == "validate":
            return adapter.cmd_projects_validate(
                project_id_str=args.project_id,
                json_output=args.json,
            )

    # Unknown command
    parser.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
