# Research: CLI Namespace Architecture - 5W1H Analysis

**ID**: PHASE4-R-001
**Date**: 2026-01-12
**Author**: Claude (Distinguished Systems Engineer)
**Status**: COMPLETE
**Branch**: cc/task-subtask

---

## Executive Summary

This document provides comprehensive 5W1H analysis for reorganizing Jerry's CLI commands into bounded-context-aligned namespaces. The goal is to transform the current flat CLI structure into a hierarchical namespace structure (`jerry session`, `jerry items`, `jerry projects`) that aligns with the hexagonal architecture and bounded contexts.

**Breaking Change**: This is a v0.1.0 breaking change with no backward compatibility required.

---

## 1. WHAT - What Are We Building?

### 1.1 Current CLI Structure (As-Is)

```
jerry init                      # Initialize project context
jerry projects list             # List all projects
jerry projects validate <id>    # Validate a project
```

**Implementation Details**:
- **Entry Point**: `src/interface/cli/main.py` (166 lines)
- **Adapter**: `src/interface/cli/adapter.py` (219 lines) - CLIAdapter class
- **Parser**: argparse with subparsers
- **Commands Available**: 3 (init, projects list, projects validate)
- **Output Formats**: Text (default), JSON (--json flag)

### 1.2 Target CLI Structure (To-Be)

```
jerry session start [--name] [--description]    # Start a new session
jerry session end [--summary]                   # End current session
jerry session status                            # Show session status
jerry session abandon [--reason]                # Abandon session

jerry items create <title> [--type] [--parent]  # Create work item
jerry items list [--status] [--type]            # List work items
jerry items show <id>                           # Show work item details
jerry items start <id>                          # Start work on item
jerry items complete <id>                       # Complete work item
jerry items block <id> [--reason]               # Block work item
jerry items cancel <id> [--reason]              # Cancel work item
jerry items assign <id> <assignee>              # Assign work item

jerry projects list                             # List projects
jerry projects validate <id>                    # Validate project
jerry projects context                          # Show current context (formerly 'init')
```

### 1.3 Bounded Context Alignment

| Namespace | Bounded Context | Domain Aggregate |
|-----------|-----------------|------------------|
| `session` | session_management | Session |
| `items` | work_tracking | WorkItem |
| `projects` | session_management | ProjectInfo |

### 1.4 Domain Operations Mapped to CLI

#### Session Operations (from `Session` aggregate)
| Aggregate Method | CLI Command | Status |
|------------------|-------------|--------|
| `Session.create()` | `jerry session start` | NEW |
| `Session.complete(summary)` | `jerry session end` | NEW |
| `Session.abandon(reason)` | `jerry session abandon` | NEW |
| `Session.link_project(project_id)` | (implicit in start) | NEW |
| Status query | `jerry session status` | NEW |

#### WorkItem Operations (from `WorkItem` aggregate)
| Aggregate Method | CLI Command | Status |
|------------------|-------------|--------|
| `WorkItem.create()` | `jerry items create` | NEW |
| `WorkItem.start_work()` | `jerry items start` | NEW |
| `WorkItem.complete()` | `jerry items complete` | NEW |
| `WorkItem.block(reason)` | `jerry items block` | NEW |
| `WorkItem.cancel(reason)` | `jerry items cancel` | NEW |
| `WorkItem.reopen()` | `jerry items reopen` | NEW |
| `WorkItem.assign(assignee)` | `jerry items assign` | NEW |
| `WorkItem.change_priority()` | `jerry items priority` | NEW |
| List query | `jerry items list` | NEW |
| Get query | `jerry items show` | NEW |

#### Project Operations (existing queries)
| Query | CLI Command | Status |
|-------|-------------|--------|
| `ScanProjectsQuery` | `jerry projects list` | EXISTS (move) |
| `ValidateProjectQuery` | `jerry projects validate` | EXISTS (move) |
| `RetrieveProjectContextQuery` | `jerry projects context` | EXISTS (rename from init) |

### 1.5 What We Are NOT Building (Scope Exclusions)

| Exclusion | Reason |
|-----------|--------|
| HTTP API | Out of scope for Phase 4 |
| gRPC interface | Out of scope |
| Backward compatibility aliases | Breaking change to v0.1.0 |
| Interactive mode | Not requested |
| Shell completion | Future enhancement |

---

## 2. WHY - Why Is This Needed?

### 2.1 Business Justification

| Driver | Rationale | Evidence |
|--------|-----------|----------|
| Hexagonal Architecture | CLI should be a thin adapter invoking application layer | ADR-003 |
| Bounded Context Isolation | Commands should be organized by domain | DDD principles |
| User Experience | Hierarchical commands are more discoverable | CLI UX best practices |
| Maintainability | Related commands in same namespace easier to maintain | Software engineering |
| Extensibility | New commands easily added to appropriate namespace | SOLID - OCP |

### 2.2 Technical Justification

| Pattern | Benefit | Reference |
|---------|---------|-----------|
| Command Groups | Logical organization, better help | Click/Typer patterns |
| Subparser Namespaces | argparse native support | Python stdlib |
| Thin Adapter | CLI only transforms input/output | Hexagonal Architecture |
| Dispatcher Injection | Testable, decoupled | Composition Root pattern |

### 2.3 Why Breaking Change?

| Option | Pros | Cons | Decision |
|--------|------|------|----------|
| A: Aliases | Backward compat | Code bloat, confusion | REJECTED |
| B: Breaking | Clean slate, v0.1.0 | Migration required | **SELECTED** |
| C: Deprecation | Gradual | Delays cleanup | REJECTED |

**Decision Rationale**: Jerry is pre-v1.0, no external users, and the current CLI is minimal. A clean breaking change to v0.1.0 is the pragmatic choice.

---

## 3. WHO - Who Is Affected?

### 3.1 Stakeholders

| Stakeholder | Impact | Mitigation |
|-------------|--------|------------|
| Claude Agents | Primary - use CLI commands | Update skill prompts |
| Human Users | Secondary - manual CLI use | Update documentation |
| CI/CD | Low - no CLI in CI yet | N/A |

### 3.2 Components Affected

| Component | Change Type | Risk |
|-----------|-------------|------|
| `src/interface/cli/main.py` | Major refactor | Medium |
| `src/interface/cli/adapter.py` | Major refactor | Medium |
| `scripts/session_start.py` | May need update | Low |
| `skills/worktracker/` | Update command references | Low |
| `CLAUDE.md` | Update CLI documentation | Low |

---

## 4. WHERE - Where In The Codebase?

### 4.1 Current Structure

```
src/interface/cli/
├── __init__.py
├── main.py                    # Entry point + argparse setup
├── adapter.py                 # CLIAdapter class
├── session_start.py           # Session hook
└── formatters/
    └── __init__.py
```

### 4.2 Target Structure

```
src/interface/cli/
├── __init__.py
├── main.py                    # Entry point (thin)
├── parser.py                  # NEW: argparse setup with namespaces
├── adapter.py                 # CLIAdapter with namespaced methods
├── commands/                  # NEW: Command group modules
│   ├── __init__.py
│   ├── session.py             # session namespace commands
│   ├── items.py               # items namespace commands
│   └── projects.py            # projects namespace commands
├── formatters/
│   ├── __init__.py
│   ├── text.py                # Human-readable output
│   └── json.py                # JSON output for AI
└── hooks/
    └── session_start.py       # Moved hook
```

### 4.3 Test Structure

```
tests/interface/cli/
├── __init__.py
├── unit/
│   ├── test_parser.py         # Parser tests
│   ├── test_adapter.py        # Adapter tests
│   └── commands/
│       ├── test_session.py    # Session command tests
│       ├── test_items.py      # Items command tests
│       └── test_projects.py   # Projects command tests
├── integration/
│   └── test_cli_workflow.py   # E2E CLI tests
└── contract/
    └── test_cli_output.py     # Output format contracts
```

---

## 5. WHEN - When Can We Start?

### 5.1 Prerequisites

| Prerequisite | Status | Evidence |
|--------------|--------|----------|
| Domain aggregates exist | COMPLETE | Session, WorkItem implemented |
| Queries exist | COMPLETE | RetrieveProjectContext, ScanProjects, ValidateProject |
| Commands exist | PARTIAL | No application commands yet |
| Research complete | COMPLETE | This document |

### 5.2 Dependencies

```
IMPL-005 (WorkItem Aggregate)  ──┐
                                 ├──►  Phase 4 CLI Namespaces
Session Aggregate              ──┘
```

### 5.3 Implementation Order

| Phase | Task | Est. Tests | Notes |
|-------|------|------------|-------|
| 4.1 | Create parser.py with namespaces | 10 | RED phase |
| 4.2 | Implement `projects` namespace | 8 | Migrate existing |
| 4.3 | Implement `session` namespace | 12 | New commands |
| 4.4 | Implement `items` namespace (queries) | 10 | List/show only |
| 4.5 | Implement `items` namespace (commands) | 15 | Create/complete/etc |
| 4.6 | Update adapter.py | 8 | Refactor |
| 4.7 | Integration tests | 10 | E2E workflows |
| 4.8 | Documentation update | 0 | CLAUDE.md, skills |
| **Total** | | **~73** | |

---

## 6. HOW - How Will We Implement?

### 6.1 Parser Architecture (argparse)

Based on research from Python stdlib documentation:

```python
# src/interface/cli/parser.py
import argparse

def create_parser() -> argparse.ArgumentParser:
    """Create the Jerry CLI argument parser with namespaced subcommands."""
    parser = argparse.ArgumentParser(
        prog="jerry",
        description="Jerry Framework CLI - Behavior and workflow guardrails",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output in JSON format",
    )
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 0.1.0",
    )

    subparsers = parser.add_subparsers(dest="namespace", help="Command namespaces")

    # Session namespace
    session_parser = subparsers.add_parser("session", help="Session management")
    session_subparsers = session_parser.add_subparsers(dest="command")

    session_start = session_subparsers.add_parser("start", help="Start a new session")
    session_start.add_argument("--name", help="Session name")
    session_start.add_argument("--description", help="Session description")

    session_end = session_subparsers.add_parser("end", help="End current session")
    session_end.add_argument("--summary", help="Session summary")

    session_subparsers.add_parser("status", help="Show session status")

    session_abandon = session_subparsers.add_parser("abandon", help="Abandon session")
    session_abandon.add_argument("--reason", help="Abandonment reason")

    # Items namespace
    items_parser = subparsers.add_parser("items", help="Work item management")
    items_subparsers = items_parser.add_subparsers(dest="command")

    items_create = items_subparsers.add_parser("create", help="Create work item")
    items_create.add_argument("title", help="Work item title")
    items_create.add_argument("--type", choices=["task", "bug", "story", "epic"], default="task")
    items_create.add_argument("--parent", help="Parent work item ID")

    items_list = items_subparsers.add_parser("list", help="List work items")
    items_list.add_argument("--status", choices=["pending", "in_progress", "blocked", "done"])
    items_list.add_argument("--type", choices=["task", "bug", "story", "epic"])

    items_show = items_subparsers.add_parser("show", help="Show work item details")
    items_show.add_argument("id", help="Work item ID")

    items_start = items_subparsers.add_parser("start", help="Start work on item")
    items_start.add_argument("id", help="Work item ID")

    items_complete = items_subparsers.add_parser("complete", help="Complete work item")
    items_complete.add_argument("id", help="Work item ID")

    items_block = items_subparsers.add_parser("block", help="Block work item")
    items_block.add_argument("id", help="Work item ID")
    items_block.add_argument("--reason", required=True, help="Block reason")

    items_cancel = items_subparsers.add_parser("cancel", help="Cancel work item")
    items_cancel.add_argument("id", help="Work item ID")
    items_cancel.add_argument("--reason", help="Cancellation reason")

    # Projects namespace
    projects_parser = subparsers.add_parser("projects", help="Project management")
    projects_subparsers = projects_parser.add_subparsers(dest="command")

    projects_subparsers.add_parser("list", help="List projects")
    projects_subparsers.add_parser("context", help="Show current project context")

    projects_validate = projects_subparsers.add_parser("validate", help="Validate project")
    projects_validate.add_argument("project_id", help="Project ID to validate")

    return parser
```

### 6.2 Adapter Pattern (Clean Architecture)

```python
# src/interface/cli/adapter.py
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.application.ports.primary.iquerydispatcher import IQueryDispatcher
    from src.application.ports.primary.icommanddispatcher import ICommandDispatcher


class CLIAdapter:
    """Primary adapter for CLI interface.

    Follows Clean Architecture - receives dispatchers via injection,
    translates CLI input to commands/queries, formats output.
    """

    def __init__(
        self,
        query_dispatcher: IQueryDispatcher,
        command_dispatcher: ICommandDispatcher | None = None,
        projects_dir: str | None = None,
    ) -> None:
        self._query_dispatcher = query_dispatcher
        self._command_dispatcher = command_dispatcher
        self._projects_dir = projects_dir

    # Session namespace
    def cmd_session_start(self, name: str | None, description: str | None, json_output: bool) -> int:
        """Handle: jerry session start"""
        ...

    def cmd_session_end(self, summary: str | None, json_output: bool) -> int:
        """Handle: jerry session end"""
        ...

    def cmd_session_status(self, json_output: bool) -> int:
        """Handle: jerry session status"""
        ...

    def cmd_session_abandon(self, reason: str | None, json_output: bool) -> int:
        """Handle: jerry session abandon"""
        ...

    # Items namespace
    def cmd_items_create(self, title: str, work_type: str, parent: str | None, json_output: bool) -> int:
        """Handle: jerry items create"""
        ...

    def cmd_items_list(self, status: str | None, work_type: str | None, json_output: bool) -> int:
        """Handle: jerry items list"""
        ...

    def cmd_items_show(self, item_id: str, json_output: bool) -> int:
        """Handle: jerry items show"""
        ...

    def cmd_items_start(self, item_id: str, json_output: bool) -> int:
        """Handle: jerry items start"""
        ...

    def cmd_items_complete(self, item_id: str, json_output: bool) -> int:
        """Handle: jerry items complete"""
        ...

    # Projects namespace (migrate existing)
    def cmd_projects_list(self, json_output: bool) -> int:
        """Handle: jerry projects list"""
        ...

    def cmd_projects_context(self, json_output: bool) -> int:
        """Handle: jerry projects context (formerly init)"""
        ...

    def cmd_projects_validate(self, project_id: str, json_output: bool) -> int:
        """Handle: jerry projects validate"""
        ...
```

### 6.3 Command Routing (main.py)

```python
# src/interface/cli/main.py
from __future__ import annotations

import sys

from src.bootstrap import create_query_dispatcher, create_command_dispatcher
from src.interface.cli.parser import create_parser
from src.interface.cli.adapter import CLIAdapter


def main() -> int:
    """Jerry CLI entry point."""
    parser = create_parser()
    args = parser.parse_args()

    if not args.namespace:
        parser.print_help()
        return 0

    # Create dispatchers via composition root
    query_dispatcher = create_query_dispatcher()
    command_dispatcher = create_command_dispatcher()

    # Create adapter with injected dependencies
    adapter = CLIAdapter(
        query_dispatcher=query_dispatcher,
        command_dispatcher=command_dispatcher,
    )

    json_output = getattr(args, "json", False)

    # Route to appropriate handler
    if args.namespace == "session":
        return _handle_session(adapter, args, json_output)
    elif args.namespace == "items":
        return _handle_items(adapter, args, json_output)
    elif args.namespace == "projects":
        return _handle_projects(adapter, args, json_output)

    parser.print_help()
    return 1


def _handle_session(adapter: CLIAdapter, args, json_output: bool) -> int:
    """Route session namespace commands."""
    if args.command == "start":
        return adapter.cmd_session_start(args.name, args.description, json_output)
    elif args.command == "end":
        return adapter.cmd_session_end(args.summary, json_output)
    elif args.command == "status":
        return adapter.cmd_session_status(json_output)
    elif args.command == "abandon":
        return adapter.cmd_session_abandon(args.reason, json_output)
    return 1


def _handle_items(adapter: CLIAdapter, args, json_output: bool) -> int:
    """Route items namespace commands."""
    if args.command == "create":
        return adapter.cmd_items_create(args.title, args.type, args.parent, json_output)
    elif args.command == "list":
        return adapter.cmd_items_list(args.status, args.type, json_output)
    elif args.command == "show":
        return adapter.cmd_items_show(args.id, json_output)
    elif args.command == "start":
        return adapter.cmd_items_start(args.id, json_output)
    elif args.command == "complete":
        return adapter.cmd_items_complete(args.id, json_output)
    # ... more commands
    return 1


def _handle_projects(adapter: CLIAdapter, args, json_output: bool) -> int:
    """Route projects namespace commands."""
    if args.command == "list":
        return adapter.cmd_projects_list(json_output)
    elif args.command == "context":
        return adapter.cmd_projects_context(json_output)
    elif args.command == "validate":
        return adapter.cmd_projects_validate(args.project_id, json_output)
    return 1


if __name__ == "__main__":
    sys.exit(main())
```

### 6.4 BDD Test Approach

```gherkin
# tests/features/cli/session_commands.feature
Feature: Session CLI Commands
  As a Jerry user
  I want to manage sessions via CLI
  So that I can track my work context

  Scenario: Start a new session
    Given no active session exists
    When I run "jerry session start --name 'Feature Work'"
    Then the exit code should be 0
    And the output should contain "Session started"
    And an active session should exist

  Scenario: End a session with summary
    Given an active session exists
    When I run "jerry session end --summary 'Completed feature X'"
    Then the exit code should be 0
    And the output should contain "Session ended"
    And no active session should exist

  Scenario: Get session status
    Given an active session exists with name "Test Session"
    When I run "jerry session status"
    Then the exit code should be 0
    And the output should contain "Test Session"
    And the output should contain "ACTIVE"

  Scenario: Get session status in JSON format
    Given an active session exists
    When I run "jerry --json session status"
    Then the exit code should be 0
    And the output should be valid JSON
    And the JSON should have key "status" with value "active"
```

### 6.5 Industry Pattern Comparison

| Framework | Pattern | Applicability to Jerry |
|-----------|---------|------------------------|
| argparse | `add_subparsers()` with nested parsers | **SELECTED** - stdlib, no deps |
| Click | `@click.group()` with `@cli.command()` | Alternative if deps allowed |
| Typer | `typer.Typer()` with `app.add_typer()` | Alternative if deps allowed |

**Decision**: Use argparse (stdlib) to maintain zero-dependency domain principle extending to interface layer where practical.

---

## 7. References & Citations

### Primary Sources

1. **Python Documentation**. [argparse - Parser for command-line options](https://docs.python.org/3/library/argparse.html). Python 3.11+.

2. **Click Documentation**. [Commands and Groups](https://click.palletsprojects.com/en/stable/commands/). Pallets Projects, 2025.

3. **Typer Documentation**. [Subcommands](https://typer.tiangolo.com/tutorial/subcommands/). FastAPI Team, 2025.

### Jerry Framework References

4. **ADR-003**: Hexagonal Architecture
5. **Design Canon**: Section 3.2 - Interface Layer
6. `.claude/rules/architecture-standards.md`: Primary Adapter patterns

### Industry Best Practices

7. **12 Factor CLI**: [clig.dev](https://clig.dev/) - CLI design guidelines
8. **GNU Standards**: [Command Line Interfaces](https://www.gnu.org/prep/standards/html_node/Command_002dLine-Interfaces.html)

---

## 8. Self-Critique & Risk Assessment

### What Could Go Wrong?

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Breaking existing scripts | Low | Medium | No external users pre-v1.0 |
| Missing command implementation | Medium | Medium | Track in WORKTRACKER |
| Parser complexity | Low | Low | Keep flat structure, avoid deep nesting |
| Test coverage gaps | Low | High | BDD-first approach |

### Assumptions Made

1. **argparse sufficient** - No need for Click/Typer dependencies
2. **JSON output required** - For AI agent consumption
3. **Commands will be added incrementally** - Not all at once
4. **Session and WorkItem aggregates complete** - Domain layer ready

### Open Questions (None Blocking)

1. Should we support TOON output format? → Future enhancement
2. Should we add shell completion? → Future enhancement (v0.2.0)

---

## 9. Gap Analysis: Current vs Target

### Commands to Migrate

| Current Command | Target Command | Change Type |
|-----------------|----------------|-------------|
| `jerry init` | `jerry projects context` | RENAME |
| `jerry projects list` | `jerry projects list` | MOVE (same) |
| `jerry projects validate <id>` | `jerry projects validate <id>` | MOVE (same) |

### Commands to Create (New)

| Command | Bounded Context | Priority |
|---------|-----------------|----------|
| `jerry session start` | session_management | HIGH |
| `jerry session end` | session_management | HIGH |
| `jerry session status` | session_management | HIGH |
| `jerry session abandon` | session_management | MEDIUM |
| `jerry items create` | work_tracking | HIGH |
| `jerry items list` | work_tracking | HIGH |
| `jerry items show` | work_tracking | HIGH |
| `jerry items start` | work_tracking | MEDIUM |
| `jerry items complete` | work_tracking | MEDIUM |
| `jerry items block` | work_tracking | MEDIUM |
| `jerry items cancel` | work_tracking | LOW |
| `jerry items assign` | work_tracking | LOW |

### Application Layer Gaps

| Required | Exists | Gap |
|----------|--------|-----|
| `CreateSessionCommand` | No | NEW |
| `EndSessionCommand` | No | NEW |
| `AbandonSessionCommand` | No | NEW |
| `GetSessionStatusQuery` | No | NEW |
| `CreateWorkItemCommand` | No | NEW |
| `StartWorkItemCommand` | No | NEW |
| `CompleteWorkItemCommand` | No | NEW |
| `ListWorkItemsQuery` | No | NEW |
| `GetWorkItemQuery` | No | NEW |

---

*Document Version: 1.0*
*Last Updated: 2026-01-12*
