"""CLI Parser with Namespace Structure.

This module provides the argument parser for the Jerry CLI with
bounded-context-aligned namespaces:
- session: Session management (session_management BC)
- items: Work item management (work_tracking BC)
- projects: Project management (session_management BC)

References:
    - ADR-CLI-002: CLI Namespace Implementation
    - PHASE4-R-001: 5W1H Research
"""

from __future__ import annotations

import argparse

# Version for v0.1.0 (breaking change from v0.0.1)
__version__ = "0.1.0"


def create_parser() -> argparse.ArgumentParser:
    """Create the argument parser for the Jerry CLI with namespaces.

    Structure:
        jerry [--json] [--version] <namespace> <command> [args]

        Namespaces:
        - session: start, end, status, abandon
        - items: create, list, show, start, complete, block, cancel
        - projects: list, validate, context

    Returns:
        Configured ArgumentParser instance with namespace subparsers.
    """
    parser = argparse.ArgumentParser(
        prog="jerry",
        description="Jerry Framework CLI - Behavior and workflow guardrails",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    jerry session start --name "Feature Work"
    jerry items list --status pending
    jerry items create "Implement feature X"
    jerry projects list
    jerry --json projects validate PROJ-001
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
        default=False,
        help="Output in JSON format for scripting/AI consumption",
    )

    # Top-level subparsers for namespaces
    subparsers = parser.add_subparsers(
        title="namespaces",
        dest="namespace",
        metavar="<namespace>",
    )

    # Session namespace
    _add_session_namespace(subparsers)

    # Items namespace
    _add_items_namespace(subparsers)

    # Projects namespace
    _add_projects_namespace(subparsers)

    return parser


def _add_session_namespace(subparsers: argparse._SubParsersAction) -> None:
    """Add session namespace commands.

    Commands:
        - start: Start a new session
        - end: End current session
        - status: Show session status
        - abandon: Abandon session (e.g., context compaction)
    """
    session_parser = subparsers.add_parser(
        "session",
        help="Session management commands",
        description="Manage agent sessions for context tracking.",
    )

    session_subparsers = session_parser.add_subparsers(
        title="commands",
        dest="command",
        metavar="<command>",
    )

    # session start
    start_parser = session_subparsers.add_parser(
        "start",
        help="Start a new session",
        description="Start a new agent session for context tracking.",
    )
    start_parser.add_argument(
        "--name",
        help="Session name (optional)",
    )
    start_parser.add_argument(
        "--description",
        help="Session description (optional)",
    )

    # session end
    end_parser = session_subparsers.add_parser(
        "end",
        help="End current session",
        description="End the current session with optional summary.",
    )
    end_parser.add_argument(
        "--summary",
        help="Session summary (optional)",
    )

    # session status
    session_subparsers.add_parser(
        "status",
        help="Show session status",
        description="Display the status of the current session.",
    )

    # session abandon
    abandon_parser = session_subparsers.add_parser(
        "abandon",
        help="Abandon session",
        description="Abandon the current session (e.g., due to context compaction).",
    )
    abandon_parser.add_argument(
        "--reason",
        help="Reason for abandonment (optional)",
    )


def _add_items_namespace(subparsers: argparse._SubParsersAction) -> None:
    """Add items namespace commands.

    Commands:
        - create: Create a new work item
        - list: List work items
        - show: Show work item details
        - start: Start work on item
        - complete: Complete work item
        - block: Block work item
        - cancel: Cancel work item
    """
    items_parser = subparsers.add_parser(
        "items",
        help="Work item management commands",
        description="Manage work items (tasks, bugs, stories, etc.).",
    )

    items_subparsers = items_parser.add_subparsers(
        title="commands",
        dest="command",
        metavar="<command>",
    )

    # items create
    create_parser = items_subparsers.add_parser(
        "create",
        help="Create a new work item",
        description="Create a new work item with specified title.",
    )
    create_parser.add_argument(
        "title",
        help="Work item title",
    )
    create_parser.add_argument(
        "--type",
        choices=["task", "bug", "story", "epic", "subtask", "spike"],
        default="task",
        help="Work item type (default: task)",
    )
    create_parser.add_argument(
        "--parent",
        help="Parent work item ID (optional)",
    )

    # items list
    list_parser = items_subparsers.add_parser(
        "list",
        help="List work items",
        description="List work items with optional filters.",
    )
    list_parser.add_argument(
        "--status",
        choices=["pending", "in_progress", "blocked", "done", "cancelled"],
        help="Filter by status",
    )
    list_parser.add_argument(
        "--type",
        choices=["task", "bug", "story", "epic", "subtask", "spike"],
        help="Filter by type",
    )

    # items show
    show_parser = items_subparsers.add_parser(
        "show",
        help="Show work item details",
        description="Display details of a specific work item.",
    )
    show_parser.add_argument(
        "id",
        help="Work item ID",
    )

    # items start
    start_parser = items_subparsers.add_parser(
        "start",
        help="Start work on item",
        description="Mark a work item as in progress.",
    )
    start_parser.add_argument(
        "id",
        help="Work item ID",
    )

    # items complete
    complete_parser = items_subparsers.add_parser(
        "complete",
        help="Complete work item",
        description="Mark a work item as done.",
    )
    complete_parser.add_argument(
        "id",
        help="Work item ID",
    )

    # items block
    block_parser = items_subparsers.add_parser(
        "block",
        help="Block work item",
        description="Mark a work item as blocked with reason.",
    )
    block_parser.add_argument(
        "id",
        help="Work item ID",
    )
    block_parser.add_argument(
        "--reason",
        required=True,
        help="Reason for blocking (required)",
    )

    # items cancel
    cancel_parser = items_subparsers.add_parser(
        "cancel",
        help="Cancel work item",
        description="Cancel a work item.",
    )
    cancel_parser.add_argument(
        "id",
        help="Work item ID",
    )
    cancel_parser.add_argument(
        "--reason",
        help="Reason for cancellation (optional)",
    )


def _add_projects_namespace(subparsers: argparse._SubParsersAction) -> None:
    """Add projects namespace commands.

    Commands:
        - list: List all projects
        - validate: Validate a project
        - context: Show current project context (formerly 'init')
    """
    projects_parser = subparsers.add_parser(
        "projects",
        help="Project management commands",
        description="Manage Jerry projects.",
    )

    projects_subparsers = projects_parser.add_subparsers(
        title="commands",
        dest="command",
        metavar="<command>",
    )

    # projects list
    projects_subparsers.add_parser(
        "list",
        help="List all projects",
        description="Scan and display all valid projects in the projects/ directory.",
    )

    # projects validate
    validate_parser = projects_subparsers.add_parser(
        "validate",
        help="Validate a project",
        description="Check that a project exists and has required configuration.",
    )
    validate_parser.add_argument(
        "project_id",
        help="Project ID to validate (e.g., PROJ-001-my-project)",
    )

    # projects context (formerly 'init')
    projects_subparsers.add_parser(
        "context",
        help="Show current project context",
        description="Display the current project context including JERRY_PROJECT setting.",
    )
