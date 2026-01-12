"""
Jerry CLI - Primary Adapter for Command-Line Interface v0.1.0.

This module provides the main entry point for the Jerry CLI tool.
It follows hexagonal architecture principles:
- Bootstrap module creates and wires all dependencies
- CLIAdapter translates CLI protocol to use case calls via dispatcher
- main.py is a thin shell that routes to the adapter

v0.1.0 Breaking Changes:
- CLI restructured into namespaces: session, items, projects
- 'jerry init' replaced by 'jerry projects context'
- New namespaces for work tracking and session management

Usage:
    jerry --help                           # Show help
    jerry --version                        # Show version
    jerry projects context                 # Display project context (was 'init')
    jerry projects list                    # List all projects
    jerry projects validate <id>           # Validate a project
    jerry session start/end/status         # Session management
    jerry items list/show/create           # Work item management

Exit Codes:
    0: Success
    1: Error (validation failure, not found, etc.)
    2: Invalid usage (bad arguments)

References:
    - ADR-CLI-002: CLI Namespace Implementation
    - PHASE4-R-001: 5W1H Research
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING, Any

from src.bootstrap import create_query_dispatcher, get_projects_directory
from src.interface.cli.adapter import CLIAdapter
from src.interface.cli.parser import __version__, create_parser

if TYPE_CHECKING:
    import argparse


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
        Exit code (0=success, 1=error, 2=invalid usage)
    """
    parser = create_parser()
    args = parser.parse_args()

    # No namespace specified - show help
    if args.namespace is None:
        parser.print_help()
        return 0

    # Create adapter with all dependencies wired
    adapter = create_cli_adapter()

    json_output = getattr(args, "json", False)

    # Route to namespace handler
    if args.namespace == "session":
        return _handle_session(adapter, args, json_output)
    elif args.namespace == "items":
        return _handle_items(adapter, args, json_output)
    elif args.namespace == "projects":
        return _handle_projects(adapter, args, json_output)

    # Unknown namespace (shouldn't happen with argparse)
    parser.print_help()
    return 2


def _handle_session(adapter: CLIAdapter, args: Any, json_output: bool) -> int:
    """Route session namespace commands.

    Args:
        adapter: CLI adapter instance
        args: Parsed arguments
        json_output: Whether to output JSON

    Returns:
        Exit code
    """
    if args.command is None:
        print("Error: No session command specified. Use 'jerry session --help'")
        return 1

    if args.command == "start":
        return adapter.cmd_session_start(
            name=getattr(args, "name", None),
            description=getattr(args, "description", None),
            json_output=json_output,
        )
    elif args.command == "end":
        return adapter.cmd_session_end(
            summary=getattr(args, "summary", None),
            json_output=json_output,
        )
    elif args.command == "status":
        return adapter.cmd_session_status(json_output=json_output)
    elif args.command == "abandon":
        return adapter.cmd_session_abandon(
            reason=getattr(args, "reason", None),
            json_output=json_output,
        )

    print(f"Error: Unknown session command '{args.command}'")
    return 1


def _handle_items(adapter: CLIAdapter, args: Any, json_output: bool) -> int:
    """Route items namespace commands.

    Args:
        adapter: CLI adapter instance
        args: Parsed arguments
        json_output: Whether to output JSON

    Returns:
        Exit code
    """
    if args.command is None:
        print("Error: No items command specified. Use 'jerry items --help'")
        return 1

    if args.command == "list":
        return adapter.cmd_items_list(
            status=getattr(args, "status", None),
            work_type=getattr(args, "type", None),
            json_output=json_output,
        )
    elif args.command == "show":
        return adapter.cmd_items_show(
            item_id=args.id,
            json_output=json_output,
        )
    elif args.command == "create":
        return adapter.cmd_items_create(
            title=args.title,
            work_type=getattr(args, "type", "task"),
            parent=getattr(args, "parent", None),
            json_output=json_output,
        )
    elif args.command == "start":
        return adapter.cmd_items_start(
            item_id=args.id,
            json_output=json_output,
        )
    elif args.command == "complete":
        return adapter.cmd_items_complete(
            item_id=args.id,
            json_output=json_output,
        )
    elif args.command == "block":
        return adapter.cmd_items_block(
            item_id=args.id,
            reason=args.reason,
            json_output=json_output,
        )
    elif args.command == "cancel":
        return adapter.cmd_items_cancel(
            item_id=args.id,
            reason=getattr(args, "reason", None),
            json_output=json_output,
        )

    print(f"Error: Unknown items command '{args.command}'")
    return 1


def _handle_projects(adapter: CLIAdapter, args: Any, json_output: bool) -> int:
    """Route projects namespace commands.

    Args:
        adapter: CLI adapter instance
        args: Parsed arguments
        json_output: Whether to output JSON

    Returns:
        Exit code
    """
    if args.command is None:
        print("Error: No projects command specified. Use 'jerry projects --help'")
        return 1

    if args.command == "context":
        return adapter.cmd_projects_context(json_output=json_output)
    elif args.command == "list":
        return adapter.cmd_projects_list(json_output=json_output)
    elif args.command == "validate":
        return adapter.cmd_projects_validate(
            project_id_str=args.project_id,
            json_output=json_output,
        )

    print(f"Error: Unknown projects command '{args.command}'")
    return 1


if __name__ == "__main__":
    sys.exit(main())
