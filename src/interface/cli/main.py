# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

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

from src.bootstrap import (
    create_command_dispatcher,
    create_hooks_handlers,
    create_query_dispatcher,
    create_session_command_handlers,
    get_projects_directory,
)
from src.interface.cli.adapter import CLIAdapter
from src.interface.cli.model_profiles import resolve_model_config
from src.interface.cli.parser import create_parser

if TYPE_CHECKING:
    pass


def create_cli_adapter() -> CLIAdapter:
    """Create a fully configured CLIAdapter.

    This is the composition root for the CLI interface.
    All dependencies are wired here via the bootstrap module.

    Returns:
        CLIAdapter with injected dispatcher, session handlers, and configuration

    References:
        - TDD-FEAT-004 Section 11.4: Bootstrap Wiring
        - TASK-251: Added command_dispatcher for transcript commands
    """
    query_dispatcher = create_query_dispatcher()
    command_dispatcher = create_command_dispatcher()
    projects_dir = get_projects_directory()
    session_handlers = create_session_command_handlers()
    hooks_handlers = create_hooks_handlers()
    return CLIAdapter(
        dispatcher=query_dispatcher,
        projects_dir=projects_dir,
        session_handlers=session_handlers,
        command_dispatcher=command_dispatcher,
        hooks_handlers=hooks_handlers,
    )


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

    json_output = getattr(args, "json", False)

    # EE-008: jerry why (works without project configuration)
    if args.namespace == "why":
        return _handle_why()

    # Create adapter with all dependencies wired
    adapter = create_cli_adapter()

    # Route to namespace handler
    if args.namespace == "session":
        return _handle_session(adapter, args, json_output)
    elif args.namespace == "items":
        return _handle_items(adapter, args, json_output)
    elif args.namespace == "projects":
        return _handle_projects(adapter, args, json_output)
    elif args.namespace == "config":
        return _handle_config(adapter, args, json_output)
    elif args.namespace == "transcript":
        return _handle_transcript(adapter, args, json_output)
    elif args.namespace == "context":
        return _handle_context(args)
    elif args.namespace == "ast":
        return _handle_ast(args, json_output)
    elif args.namespace == "hooks":
        return _handle_hooks(adapter, args)
    elif args.namespace == "agents":
        return _handle_agents(adapter, args)

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
        print("No session command specified. Use 'jerry session --help'.")
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

    print(f"Unknown session command: {args.command}")
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
        print("No items command specified. Use 'jerry items --help'.")
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

    print(f"Unknown items command: {args.command}")
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
        print("No projects command specified. Use 'jerry projects --help'.")
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

    print(f"Unknown projects command: {args.command}")
    return 1


def _handle_config(adapter: CLIAdapter, args: Any, json_output: bool) -> int:
    """Route config namespace commands.

    Args:
        adapter: CLI adapter instance
        args: Parsed arguments
        json_output: Whether to output JSON

    Returns:
        Exit code

    References:
        - WI-016: CLI Config Commands
    """
    if args.command is None:
        print("No config command specified. Use 'jerry config --help'.")
        return 1

    if args.command == "show":
        return adapter.cmd_config_show(
            show_source=getattr(args, "source", False),
            json_output=json_output,
        )
    elif args.command == "get":
        return adapter.cmd_config_get(
            key=args.key,
            json_output=json_output,
        )
    elif args.command == "set":
        return adapter.cmd_config_set(
            key=args.key,
            value=args.value,
            scope=getattr(args, "scope", "project"),
            json_output=json_output,
        )
    elif args.command == "path":
        return adapter.cmd_config_path(json_output=json_output)

    print(f"Unknown config command: {args.command}")
    return 1


def _handle_transcript(adapter: CLIAdapter, args: Any, json_output: bool) -> int:
    """Route transcript namespace commands.

    Args:
        adapter: CLI adapter instance
        args: Parsed arguments
        json_output: Whether to output JSON

    Returns:
        Exit code

    References:
        - TDD-FEAT-004 Section 11.2: Main Routing
        - TASK-251: Implement CLI Transcript Namespace
    """
    if args.command is None:
        print("No transcript command specified. Use 'jerry transcript --help'.")
        return 1

    if args.command == "parse":
        # EN-026: Support both token-based and segment-based chunking
        # --no-token-limit disables token-based chunking (deprecated)
        target_tokens: int | None = getattr(args, "target_tokens", 18000)
        if getattr(args, "no_token_limit", False):
            target_tokens = None

        # TASK-423: Resolve model configuration from profile and individual overrides
        model_config = resolve_model_config(
            profile=getattr(args, "profile", None),
            model_parser=getattr(args, "model_parser", None),
            model_extractor=getattr(args, "model_extractor", None),
            model_formatter=getattr(args, "model_formatter", None),
            model_mindmap=getattr(args, "model_mindmap", None),
            model_critic=getattr(args, "model_critic", None),
        )

        return adapter.cmd_transcript_parse(
            path=args.path,
            format=getattr(args, "format", "auto"),
            output_dir=getattr(args, "output_dir", None),
            chunk_size=getattr(args, "chunk_size", 500),
            target_tokens=target_tokens,
            generate_chunks=not getattr(args, "no_chunks", False),
            model_parser=model_config["parser"],
            model_extractor=model_config["extractor"],
            model_formatter=model_config["formatter"],
            model_mindmap=model_config["mindmap"],
            model_critic=model_config["critic"],
            json_output=json_output,
        )

    print(f"Unknown transcript command: {args.command}")
    return 1


def _handle_context(args: Any) -> int:
    """Route context namespace commands.

    Reads stdin JSON and delegates to the context estimate handler.
    Does not require the CLIAdapter — uses its own bootstrap wiring.

    Args:
        args: Parsed arguments with .command.

    Returns:
        Exit code (always 0 for fail-open).

    References:
        - EN-012: jerry context estimate CLI Command
    """
    if args.command is None:
        print("No context command specified. Use 'jerry context --help'.")
        return 1

    if args.command == "estimate":
        from src.bootstrap import create_context_estimate_handler

        handler = create_context_estimate_handler()

        # Read stdin
        stdin_json = ""
        if not sys.stdin.isatty():
            stdin_json = sys.stdin.read()

        return handler.handle(stdin_json)

    print(f"Unknown context command: {args.command}")
    return 1


def _handle_ast(args: Any, json_output: bool) -> int:
    """Route ast namespace commands.

    Does not require the CLIAdapter; calls the domain layer directly via
    ast_commands functions.

    Args:
        args: Parsed arguments with .command, .file, and optional .selector/.schema.
        json_output: Whether JSON output was requested (passed through to commands).

    Returns:
        Exit code: 0 (success), 1 (validation failure), 2 (parse error).

    References:
        - ST-004: Add jerry ast CLI Commands
    """
    from src.interface.cli.ast_commands import (
        ast_detect,
        ast_frontmatter,
        ast_metadata,
        ast_modify,
        ast_parse,
        ast_query,
        ast_reinject,
        ast_render,
        ast_sections,
        ast_validate,
    )

    if args.command is None:
        print("No ast command specified. Use 'jerry ast --help'.")
        return 1

    if args.command == "parse":
        return ast_parse(args.file, json_output)
    elif args.command == "render":
        return ast_render(args.file)
    elif args.command == "validate":
        return ast_validate(
            args.file,
            getattr(args, "schema", None),
            nav=getattr(args, "nav", False),
        )
    elif args.command == "query":
        return ast_query(args.file, args.selector, json_output)
    elif args.command == "frontmatter":
        return ast_frontmatter(args.file)
    elif args.command == "modify":
        return ast_modify(args.file, args.key, args.value)
    elif args.command == "reinject":
        return ast_reinject(args.file)
    elif args.command == "detect":
        return ast_detect(args.file)
    elif args.command == "sections":
        return ast_sections(args.file)
    elif args.command == "metadata":
        return ast_metadata(args.file)

    print(f"Unknown ast command: {args.command}")
    return 1


def _handle_agents(adapter: CLIAdapter, args: Any) -> int:
    """Route agents namespace commands.

    Args:
        adapter: CLI adapter instance
        args: Parsed arguments

    Returns:
        Exit code

    References:
        - PROJ-012: Agent Configuration Extraction & Schema Enforcement
    """
    if args.command is None:
        print("No agents command specified. Use 'jerry agents --help'.")
        return 1

    json_output = getattr(args, "json", False)

    if args.command == "list":
        return adapter.cmd_agents_list(
            skill_filter=getattr(args, "skill", None),
        )
    elif args.command == "validate":
        return adapter.cmd_agents_validate(
            agent_name=getattr(args, "agent_name", None),
        )
    elif args.command == "show":
        return adapter.cmd_agents_show(
            agent_name=args.agent_name,
            raw=getattr(args, "raw", False),
        )
    elif args.command == "compose":
        return adapter.cmd_agents_compose(
            target=args.target,
            output_dir=getattr(args, "output_dir", None),
            clean=getattr(args, "clean", False),
            json_output=json_output,
        )

    print(f"Unknown agents command: {args.command}")
    return 1


def _handle_why() -> int:
    """Handle the 'why' command (EE-008).

    Returns:
        Exit code (always 0)
    """
    print(
        "Why does Jerry exist?\n"
        "\n"
        "Joy and excellence are not trade-offs. They're multipliers.\n"
        "\n"
        "The quality gates are non-negotiable. The voice is non-negotiable too.\n"
        "Both serve the same purpose: making the work worth doing.\n"
        "\n"
        '"Whether it was steep, extreme descent or new freestyle,\n'
        "what we were doing was freeskiing, free to ski our own style\n"
        'on our own terms." \u2014 Shane McConkey\n'
        "\n"
        "That's why."
    )
    return 0


def _handle_hooks(adapter: CLIAdapter, args: Any) -> int:
    """Route hooks namespace commands.

    Reads stdin JSON and delegates to the adapter's hooks handler.

    Args:
        adapter: CLI adapter instance
        args: Parsed arguments

    Returns:
        Exit code

    References:
        - EN-006: jerry hooks CLI Command Namespace
    """
    hooks_command = getattr(args, "hooks_command", None)
    if hooks_command is None:
        print("Error: No hooks command specified. Use 'jerry hooks --help'")
        return 1

    # Read hook input from stdin
    stdin_json = ""
    if not sys.stdin.isatty():
        stdin_json = sys.stdin.read()

    return adapter.cmd_hooks(hooks_command, stdin_json)


if __name__ == "__main__":
    sys.exit(main())
