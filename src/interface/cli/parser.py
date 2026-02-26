# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

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

try:
    from importlib.metadata import version

    __version__ = version("jerry")
except Exception:
    __version__ = "dev"


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

    parser.add_argument(
        "--saucer-boy",
        action="store_true",
        default=False,
        help=argparse.SUPPRESS,
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

    # Config namespace
    _add_config_namespace(subparsers)

    # Transcript namespace (TASK-251: TDD-FEAT-004 Section 11)
    _add_transcript_namespace(subparsers)

    # Context namespace (EN-012: jerry context estimate)
    _add_context_namespace(subparsers)

    # AST namespace (ST-004: jerry ast commands)
    _add_ast_namespace(subparsers)

    # Agents namespace (ADR-PROJ010-003: Canonical agent build pipeline)
    _add_agents_namespace(subparsers)

    # EE-008: Undocumented philosophy command
    subparsers.add_parser(
        "why",
        help=argparse.SUPPRESS,
    )

    # Hooks namespace (EN-006: Context monitoring hook events)
    _add_hooks_namespace(subparsers)

    return parser


def _add_session_namespace(subparsers: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
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


def _add_items_namespace(subparsers: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
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


def _add_projects_namespace(
    subparsers: argparse._SubParsersAction[argparse.ArgumentParser],
) -> None:
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


def _add_config_namespace(
    subparsers: argparse._SubParsersAction[argparse.ArgumentParser],
) -> None:
    """Add config namespace commands.

    Commands:
        - show: Display all configuration values
        - get: Get a specific configuration value
        - set: Set a configuration value
        - path: Show configuration file paths

    References:
        - WI-016: CLI Config Commands
    """
    config_parser = subparsers.add_parser(
        "config",
        help="Configuration management commands",
        description="View and manage Jerry configuration.",
    )

    config_subparsers = config_parser.add_subparsers(
        title="commands",
        dest="command",
        metavar="<command>",
    )

    # config show
    show_parser = config_subparsers.add_parser(
        "show",
        help="Show current configuration",
        description="Display all configuration values with their sources.",
    )
    show_parser.add_argument(
        "--source",
        action="store_true",
        help="Show the source of each value (env, project, root, default)",
    )

    # config get
    get_parser = config_subparsers.add_parser(
        "get",
        help="Get a configuration value",
        description="Get the value of a specific configuration key.",
    )
    get_parser.add_argument(
        "key",
        help="Configuration key (e.g., logging.level)",
    )

    # config set
    set_parser = config_subparsers.add_parser(
        "set",
        help="Set a configuration value",
        description="Set a configuration value in the specified scope.",
    )
    set_parser.add_argument(
        "key",
        help="Configuration key (e.g., logging.level)",
    )
    set_parser.add_argument(
        "value",
        help="Configuration value to set",
    )
    set_parser.add_argument(
        "--scope",
        choices=["project", "root", "local"],
        default="project",
        help="Scope to write to (default: project)",
    )

    # config path
    config_subparsers.add_parser(
        "path",
        help="Show configuration file paths",
        description="Display paths to all configuration files.",
    )


def _add_transcript_namespace(
    subparsers: argparse._SubParsersAction[argparse.ArgumentParser],
) -> None:
    """Add transcript namespace commands.

    Commands:
        - parse: Parse VTT/SRT transcript to canonical JSON

    References:
        - TDD-FEAT-004 Section 11: Jerry CLI Integration
        - TASK-251: Implement CLI Transcript Namespace
        - EN-020: Python Parser Implementation
    """
    transcript_parser = subparsers.add_parser(
        "transcript",
        help="Transcript skill commands",
        description="Manage transcript skill operations.",
    )

    transcript_subparsers = transcript_parser.add_subparsers(
        title="commands",
        dest="command",
        metavar="<command>",
    )

    # parse command
    parse_parser = transcript_subparsers.add_parser(
        "parse",
        help="Parse transcript file to canonical JSON",
        description="Parse VTT/SRT transcript file and produce canonical JSON output with optional chunking.",
    )
    parse_parser.add_argument(
        "path",
        help="Path to transcript file (VTT or SRT)",
    )
    parse_parser.add_argument(
        "--format",
        choices=["vtt", "srt", "auto"],
        default="auto",
        help="Input format (default: auto-detect from extension)",
    )
    parse_parser.add_argument(
        "--output-dir",
        dest="output_dir",
        default=None,
        help="Output directory for canonical JSON and chunks (default: same as input)",
    )
    parse_parser.add_argument(
        "--chunk-size",
        dest="chunk_size",
        type=int,
        default=500,
        help="Number of segments per chunk (deprecated, use --target-tokens)",
    )
    parse_parser.add_argument(
        "--target-tokens",
        dest="target_tokens",
        type=int,
        default=18000,
        help="Target tokens per chunk (default: 18000, recommended for Claude Code)",
    )
    parse_parser.add_argument(
        "--no-token-limit",
        dest="no_token_limit",
        action="store_true",
        default=False,
        help="Disable token-based chunking, use segment-based only (deprecated)",
    )
    parse_parser.add_argument(
        "--no-chunks",
        dest="no_chunks",
        action="store_true",
        default=False,
        help="Skip chunk generation, output canonical JSON only",
    )

    # Model selection parameters (TASK-420, TASK-423: EN-031 Model Selection Capability)
    # Profile selection (TASK-423: Predefined model profiles)
    parse_parser.add_argument(
        "--profile",
        choices=["economy", "balanced", "quality", "speed"],
        default=None,
        help=(
            "Model profile: economy (all haiku), balanced (default), "
            "quality (opus for critical), speed (all haiku). "
            "Individual --model-* flags override profile."
        ),
    )

    # Individual model overrides (take precedence over --profile)
    parse_parser.add_argument(
        "--model-parser",
        dest="model_parser",
        choices=["opus", "sonnet", "haiku"],
        default=None,
        help="Model for ts-parser agent (overrides --profile)",
    )
    parse_parser.add_argument(
        "--model-extractor",
        dest="model_extractor",
        choices=["opus", "sonnet", "haiku"],
        default=None,
        help="Model for ts-extractor agent (overrides --profile)",
    )
    parse_parser.add_argument(
        "--model-formatter",
        dest="model_formatter",
        choices=["opus", "sonnet", "haiku"],
        default=None,
        help="Model for ts-formatter agent (overrides --profile)",
    )
    parse_parser.add_argument(
        "--model-mindmap",
        dest="model_mindmap",
        choices=["opus", "sonnet", "haiku"],
        default=None,
        help="Model for ts-mindmap-* agents (overrides --profile)",
    )
    parse_parser.add_argument(
        "--model-critic",
        dest="model_critic",
        choices=["opus", "sonnet", "haiku"],
        default=None,
        help="Model for ps-critic agent (overrides --profile)",
    )


def _add_ast_namespace(
    subparsers: argparse._SubParsersAction[argparse.ArgumentParser],
) -> None:
    """Add ast namespace commands.

    Commands:
        - parse: Parse a markdown file and output the AST as JSON.
        - render: Roundtrip parse-render a markdown file through mdformat.
        - validate: Validate a markdown file against a schema.
        - query: Query AST nodes by type and output structured JSON.

    References:
        - ST-004: Add jerry ast CLI Commands
        - ST-001: JerryDocument Facade
    """
    ast_parser = subparsers.add_parser(
        "ast",
        help="Markdown AST operations",
        description="Parse, query, transform, and validate markdown AST structures.",
    )

    ast_subparsers = ast_parser.add_subparsers(
        title="commands",
        dest="command",
        metavar="<command>",
    )

    # ast parse
    parse_parser = ast_subparsers.add_parser(
        "parse",
        help="Parse markdown file to AST JSON",
        description="Parse a markdown file and output its AST as structured JSON.",
    )
    parse_parser.add_argument(
        "file",
        help="Path to markdown file",
    )

    # ast render
    render_parser = ast_subparsers.add_parser(
        "render",
        help="Roundtrip render markdown file via mdformat",
        description="Parse and re-render a markdown file through mdformat normalization.",
    )
    render_parser.add_argument(
        "file",
        help="Path to markdown file",
    )

    # ast validate
    validate_parser = ast_subparsers.add_parser(
        "validate",
        help="Validate markdown file",
        description="Validate a markdown file, optionally against a named schema.",
    )
    validate_parser.add_argument(
        "file",
        help="Path to markdown file",
    )
    validate_parser.add_argument(
        "--schema",
        default=None,
        help="Schema type to validate against (e.g., story, epic, task). Optional.",
    )
    validate_parser.add_argument(
        "--nav",
        action="store_true",
        default=False,
        help="Include detailed nav table entries in output.",
    )

    # ast query
    query_parser = ast_subparsers.add_parser(
        "query",
        help="Query AST nodes by type",
        description="Query all AST nodes matching the given node type selector.",
    )
    query_parser.add_argument(
        "file",
        help="Path to markdown file",
    )
    query_parser.add_argument(
        "selector",
        help="Node type to query (e.g., heading, blockquote, paragraph)",
    )

    # ast frontmatter
    frontmatter_parser = ast_subparsers.add_parser(
        "frontmatter",
        help="Extract blockquote frontmatter fields as JSON",
        description="Extract all blockquote frontmatter fields from a markdown file.",
    )
    frontmatter_parser.add_argument(
        "file",
        help="Path to markdown file",
    )

    # ast modify
    modify_parser = ast_subparsers.add_parser(
        "modify",
        help="Modify a frontmatter field",
        description="Modify a frontmatter field value and write back to file.",
    )
    modify_parser.add_argument(
        "file",
        help="Path to markdown file",
    )
    modify_parser.add_argument(
        "--key",
        required=True,
        help="Frontmatter field name to modify (case-sensitive).",
    )
    modify_parser.add_argument(
        "--value",
        required=True,
        help="New value for the field.",
    )

    # ast reinject
    reinject_parser = ast_subparsers.add_parser(
        "reinject",
        help="Extract L2-REINJECT directives as JSON",
        description="Extract all L2-REINJECT directives from a markdown file.",
    )
    reinject_parser.add_argument(
        "file",
        help="Path to markdown file",
    )

    # ast detect (RE-006: WI-017)
    detect_parser = ast_subparsers.add_parser(
        "detect",
        help="Detect document type of a markdown file",
        description="Detect the Jerry document type using path-first, structure-fallback detection.",
    )
    detect_parser.add_argument(
        "file",
        help="Path to markdown file",
    )

    # ast sections (RE-006: WI-017)
    sections_parser = ast_subparsers.add_parser(
        "sections",
        help="Extract XML-tagged sections as JSON",
        description="Extract XML-tagged sections (e.g., <identity>, <methodology>) from a markdown file.",
    )
    sections_parser.add_argument(
        "file",
        help="Path to markdown file",
    )

    # ast metadata (RE-006: WI-017)
    metadata_parser = ast_subparsers.add_parser(
        "metadata",
        help="Extract HTML comment metadata as JSON",
        description="Extract structured metadata from HTML comments (e.g., PS-ID, VERSION blocks).",
    )
    metadata_parser.add_argument(
        "file",
        help="Path to markdown file",
    )


def _add_agents_namespace(
    subparsers: argparse._SubParsersAction[argparse.ArgumentParser],
) -> None:
    """Add agents namespace commands.

    Commands:
        - build: Build vendor-specific agent files from canonical source
        - extract: Reverse-engineer canonical source from existing vendor files
        - validate: Validate all canonical agent definitions against schema
        - list: List agents with tier, skill, vendor status
        - diff: Show drift between canonical source and generated output

    References:
        - ADR-PROJ010-003: LLM Portability Architecture
    """
    agents_parser = subparsers.add_parser(
        "agents",
        help="Agent definition build pipeline",
        description="Build and manage vendor-agnostic canonical agent definitions.",
    )

    agents_subparsers = agents_parser.add_subparsers(
        title="commands",
        dest="command",
        metavar="<command>",
    )

    # agents build
    build_parser = agents_subparsers.add_parser(
        "build",
        help="Build vendor-specific agent files from canonical source",
        description="Generate vendor-specific agent files from canonical .agent.yaml + .prompt.md source.",
    )
    build_parser.add_argument(
        "--vendor",
        default="claude_code",
        help="Target vendor (default: claude_code)",
    )
    build_parser.add_argument(
        "--agent",
        default=None,
        help="Specific agent to build (default: all)",
    )
    build_parser.add_argument(
        "--dry-run",
        action="store_true",
        default=False,
        help="Show what would be generated without writing files",
    )

    # agents extract
    extract_parser = agents_subparsers.add_parser(
        "extract",
        help="Extract canonical source from existing vendor files",
        description="Reverse-engineer canonical .agent.yaml + .prompt.md from existing agent files.",
    )
    extract_parser.add_argument(
        "--agent",
        default=None,
        help="Specific agent to extract (default: all)",
    )
    extract_parser.add_argument(
        "--source-vendor",
        default="claude_code",
        help="Source vendor format (default: claude_code)",
    )

    # agents compose
    compose_parser = agents_subparsers.add_parser(
        "compose",
        help="Compose agent files with defaults for deployment",
        description="Generate composed agent files by merging canonical source with base defaults.",
    )
    compose_parser.add_argument(
        "--vendor",
        default="claude_code",
        help="Target vendor (default: claude_code)",
    )
    compose_parser.add_argument(
        "--agent",
        default=None,
        help="Specific agent to compose (default: all)",
    )
    compose_parser.add_argument(
        "--output-dir",
        default=None,
        help="Output directory (default: .claude/agents/)",
    )
    compose_parser.add_argument(
        "--clean",
        action="store_true",
        default=False,
        help="Remove existing .md files in output dir before writing",
    )
    compose_parser.add_argument(
        "--dry-run",
        action="store_true",
        default=False,
        help="Show what would be generated without writing files",
    )

    # agents validate
    validate_parser = agents_subparsers.add_parser(
        "validate",
        help="Validate canonical agent definitions",
        description="Validate all canonical agent definitions against JSON Schema and domain rules.",
    )
    validate_parser.add_argument(
        "--agent",
        default=None,
        help="Specific agent to validate (default: all)",
    )

    # agents list
    list_parser = agents_subparsers.add_parser(
        "list",
        help="List agents with metadata",
        description="List all canonical agents with tier, skill, and model information.",
    )
    list_parser.add_argument(
        "--skill",
        default=None,
        help="Filter by skill name",
    )

    # agents diff
    diff_parser = agents_subparsers.add_parser(
        "diff",
        help="Show drift between canonical and generated files",
        description="Compare canonical source against generated vendor files to detect drift.",
    )
    diff_parser.add_argument(
        "--agent",
        default=None,
        help="Specific agent to diff (default: all)",
    )
    diff_parser.add_argument(
        "--vendor",
        default="claude_code",
        help="Vendor to compare against (default: claude_code)",
    )


def _add_context_namespace(
    subparsers: argparse._SubParsersAction[argparse.ArgumentParser],
) -> None:
    """Add context namespace commands.

    Commands:
        - estimate: Compute context fill estimate from Claude Code stdin JSON

    References:
        - EN-012: jerry context estimate CLI Command
        - FEAT-002: Status Line / Context Monitoring Unification
    """
    context_parser = subparsers.add_parser(
        "context",
        help="Context monitoring commands",
        description="Context monitoring and fill estimation.",
    )

    context_subparsers = context_parser.add_subparsers(
        title="commands",
        dest="command",
        metavar="<command>",
    )

    context_subparsers.add_parser(
        "estimate",
        help="Compute context fill estimate",
        description="Read Claude Code JSON from stdin and compute context fill estimate.",
    )


def _add_hooks_namespace(
    subparsers: argparse._SubParsersAction[argparse.ArgumentParser],
) -> None:
    """Add hooks namespace commands.

    Commands:
        - prompt-submit: Handle UserPromptSubmit hook event
        - session-start: Handle SessionStart hook event
        - pre-compact: Handle PreCompact hook event
        - pre-tool-use: Handle PreToolUse hook event

    References:
        - EN-006: jerry hooks CLI Command Namespace
    """
    hooks_parser = subparsers.add_parser(
        "hooks",
        help="Claude Code hook event handlers",
        description="Handle Claude Code hook events via CLI.",
    )

    hooks_subparsers = hooks_parser.add_subparsers(
        title="commands",
        dest="hooks_command",
        metavar="<command>",
    )

    hooks_subparsers.add_parser(
        "prompt-submit",
        help="Handle UserPromptSubmit hook event",
    )

    hooks_subparsers.add_parser(
        "session-start",
        help="Handle SessionStart hook event",
    )

    hooks_subparsers.add_parser(
        "pre-compact",
        help="Handle PreCompact hook event",
    )

    hooks_subparsers.add_parser(
        "pre-tool-use",
        help="Handle PreToolUse hook event",
    )

    hooks_subparsers.add_parser(
        "stop",
        help="Handle Stop hook event (context stop gate)",
    )

    hooks_subparsers.add_parser(
        "subagent-stop",
        help="Handle SubagentStop hook event (lifecycle tracking)",
    )
