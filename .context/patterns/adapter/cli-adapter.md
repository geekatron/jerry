# PAT-ADP-001: CLI Adapter Pattern

> **Status**: MANDATORY
> **Category**: Adapter Pattern
> **Location**: `src/interface/cli/`

---

## Overview

The CLI Adapter is a primary adapter that translates command-line interactions into application operations. It drives the application via dispatcher ports, handling argument parsing, output formatting, and error translation.

---

## Industry Prior Art

| Source | Key Insight |
|--------|-------------|
| **Alistair Cockburn** | "Primary adapters drive the application" |
| **Robert C. Martin** | "The CLI is a delivery mechanism, not the application" |
| **Clean Architecture** | "Frameworks and drivers are the outermost circle" |

---

## Jerry Implementation

### CLI Adapter Structure

```python
# File: src/interface/cli/adapter.py
from __future__ import annotations

from typing import TYPE_CHECKING

from src.shared_kernel.exceptions import (
    DomainError,
    NotFoundError,
    ValidationError,
    InvalidStateError,
    ConcurrencyError,
)

if TYPE_CHECKING:
    from src.application.ports.primary.icommanddispatcher import ICommandDispatcher
    from src.application.ports.primary.iquerydispatcher import IQueryDispatcher


class CLIAdapter:
    """Primary adapter for CLI interface.

    Responsibilities:
    - Translate CLI arguments to commands/queries
    - Dispatch to application layer
    - Format output for display
    - Translate domain errors to exit codes

    Design Notes:
    - Receives dispatchers via constructor (DI)
    - No business logic - only translation
    - Uses domain exceptions, not CLI-specific
    """

    def __init__(
        self,
        command_dispatcher: ICommandDispatcher,
        query_dispatcher: IQueryDispatcher,
        output_formatter: OutputFormatter | None = None,
    ) -> None:
        """Initialize with dispatchers (dependency injection).

        Args:
            command_dispatcher: Dispatcher for write operations
            query_dispatcher: Dispatcher for read operations
            output_formatter: Optional output formatter
        """
        self._command_dispatcher = command_dispatcher
        self._query_dispatcher = query_dispatcher
        self._formatter = output_formatter or DefaultOutputFormatter()

    # =========================================================================
    # Command Operations (Write)
    # =========================================================================

    def create_task(
        self,
        title: str,
        priority: str = "medium",
        description: str = "",
    ) -> int:
        """Handle create-task command.

        Args:
            title: Task title
            priority: Task priority
            description: Optional description

        Returns:
            Exit code (0 = success, 1 = domain error, 2 = unexpected)
        """
        from src.application.commands.create_work_item_command import (
            CreateWorkItemCommand,
        )

        command = CreateWorkItemCommand(
            title=title,
            work_type="task",
            priority=priority,
            description=description,
        )

        return self._dispatch_command(command, "Task created: {work_item_id}")

    def complete_task(self, task_id: str) -> int:
        """Handle complete-task command.

        Args:
            task_id: ID of task to complete

        Returns:
            Exit code
        """
        from src.application.commands.complete_work_item_command import (
            CompleteWorkItemCommand,
        )

        command = CompleteWorkItemCommand(
            work_item_id=task_id,
            quality_passed=True,
        )

        return self._dispatch_command(command, f"Task {task_id} completed")

    def start_task(self, task_id: str) -> int:
        """Handle start-task command."""
        from src.application.commands.start_work_item_command import (
            StartWorkItemCommand,
        )

        command = StartWorkItemCommand(work_item_id=task_id)
        return self._dispatch_command(command, f"Task {task_id} started")

    # =========================================================================
    # Query Operations (Read)
    # =========================================================================

    def show_status(self, json_output: bool = False) -> int:
        """Handle status command.

        Args:
            json_output: If True, output JSON format

        Returns:
            Exit code
        """
        from src.application.queries.retrieve_project_context_query import (
            RetrieveProjectContextQuery,
        )

        query = RetrieveProjectContextQuery(base_path=self._get_projects_dir())
        return self._dispatch_query(query, json_output=json_output)

    def list_tasks(
        self,
        status: str | None = None,
        priority: str | None = None,
        json_output: bool = False,
    ) -> int:
        """Handle list-tasks command.

        Args:
            status: Optional status filter
            priority: Optional priority filter
            json_output: If True, output JSON format

        Returns:
            Exit code
        """
        from src.application.queries.list_work_items_query import ListWorkItemsQuery

        query = ListWorkItemsQuery(
            status=status,
            priority=priority,
        )
        return self._dispatch_query(query, json_output=json_output)

    def get_task(self, task_id: str, json_output: bool = False) -> int:
        """Handle get-task command."""
        from src.application.queries.get_work_item_query import GetWorkItemQuery

        query = GetWorkItemQuery(work_item_id=task_id)
        return self._dispatch_query(query, json_output=json_output)

    # =========================================================================
    # Internal Methods
    # =========================================================================

    def _dispatch_command(
        self,
        command,
        success_message: str,
    ) -> int:
        """Dispatch command and handle result.

        Args:
            command: Command to dispatch
            success_message: Message template for success

        Returns:
            Exit code
        """
        try:
            events = self._command_dispatcher.dispatch(command)

            # Format success message with event data
            if events:
                event = events[0]
                message = success_message.format(
                    work_item_id=getattr(event, 'work_item_id', ''),
                )
            else:
                message = success_message

            self._formatter.success(message)
            return 0

        except ValidationError as e:
            self._formatter.error(f"Validation error: {e.field}: {e.validation_message}")
            return 1

        except NotFoundError as e:
            self._formatter.error(f"{e.entity_type} '{e.entity_id}' not found")
            return 1

        except InvalidStateError as e:
            self._formatter.error(f"Invalid state: {e}")
            return 1

        except ConcurrencyError as e:
            self._formatter.error("Concurrent modification detected. Please retry.")
            return 1

        except DomainError as e:
            self._formatter.error(f"Error: {e}")
            return 1

        except Exception as e:
            self._formatter.error(f"Unexpected error: {e}")
            return 2

    def _dispatch_query(
        self,
        query,
        json_output: bool = False,
    ) -> int:
        """Dispatch query and format result.

        Args:
            query: Query to dispatch
            json_output: Whether to output JSON

        Returns:
            Exit code
        """
        try:
            result = self._query_dispatcher.dispatch(query)

            if json_output:
                self._formatter.json(result)
            else:
                self._formatter.display(result)

            return 0

        except NotFoundError as e:
            self._formatter.error(f"{e.entity_type} '{e.entity_id}' not found")
            return 1

        except DomainError as e:
            self._formatter.error(f"Error: {e}")
            return 1

        except Exception as e:
            self._formatter.error(f"Unexpected error: {e}")
            return 2

    def _get_projects_dir(self) -> str:
        """Get projects directory path."""
        import os
        return os.environ.get("JERRY_PROJECTS_DIR", "projects")
```

---

## Output Formatter

```python
# File: src/interface/cli/formatters/output_formatter.py
from __future__ import annotations

import json
import sys
from abc import ABC, abstractmethod
from typing import Any


class OutputFormatter(ABC):
    """Abstract formatter for CLI output."""

    @abstractmethod
    def success(self, message: str) -> None:
        """Output success message."""
        ...

    @abstractmethod
    def error(self, message: str) -> None:
        """Output error message."""
        ...

    @abstractmethod
    def display(self, data: Any) -> None:
        """Display data in human-readable format."""
        ...

    @abstractmethod
    def json(self, data: Any) -> None:
        """Output data as JSON."""
        ...


class DefaultOutputFormatter(OutputFormatter):
    """Default CLI output formatter."""

    def success(self, message: str) -> None:
        """Print success message to stdout."""
        print(f"✓ {message}")

    def error(self, message: str) -> None:
        """Print error message to stderr."""
        print(f"✗ {message}", file=sys.stderr)

    def display(self, data: Any) -> None:
        """Display data based on type."""
        if isinstance(data, dict):
            self._display_dict(data)
        elif hasattr(data, '__dataclass_fields__'):
            self._display_dataclass(data)
        else:
            print(data)

    def json(self, data: Any) -> None:
        """Output as formatted JSON."""
        if hasattr(data, 'to_dict'):
            data = data.to_dict()
        elif hasattr(data, '__dataclass_fields__'):
            from dataclasses import asdict
            data = asdict(data)
        print(json.dumps(data, indent=2, default=str))

    def _display_dict(self, data: dict) -> None:
        """Display dictionary as key-value pairs."""
        for key, value in data.items():
            print(f"  {key}: {value}")

    def _display_dataclass(self, obj) -> None:
        """Display dataclass fields."""
        for field in obj.__dataclass_fields__:
            value = getattr(obj, field)
            print(f"  {field}: {value}")
```

---

## CLI Entry Point

```python
# File: src/interface/cli/main.py
import argparse
import sys

from src.bootstrap import create_command_dispatcher, create_query_dispatcher
from src.interface.cli.adapter import CLIAdapter


def main() -> int:
    """CLI entry point."""
    parser = argparse.ArgumentParser(description="Jerry Work Tracker")
    subparsers = parser.add_subparsers(dest="command")

    # create-task subcommand
    create_parser = subparsers.add_parser("create-task", help="Create a new task")
    create_parser.add_argument("title", help="Task title")
    create_parser.add_argument("--priority", "-p", default="medium")
    create_parser.add_argument("--description", "-d", default="")

    # complete-task subcommand
    complete_parser = subparsers.add_parser("complete-task", help="Complete a task")
    complete_parser.add_argument("task_id", help="Task ID")

    # list-tasks subcommand
    list_parser = subparsers.add_parser("list-tasks", help="List tasks")
    list_parser.add_argument("--status", "-s", help="Filter by status")
    list_parser.add_argument("--json", action="store_true", help="JSON output")

    # Parse arguments
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    # Create adapter with dispatchers (composition root)
    adapter = CLIAdapter(
        command_dispatcher=create_command_dispatcher(),
        query_dispatcher=create_query_dispatcher(),
    )

    # Route to command
    if args.command == "create-task":
        return adapter.create_task(
            title=args.title,
            priority=args.priority,
            description=args.description,
        )
    elif args.command == "complete-task":
        return adapter.complete_task(args.task_id)
    elif args.command == "list-tasks":
        return adapter.list_tasks(
            status=args.status,
            json_output=args.json,
        )

    return 1


if __name__ == "__main__":
    sys.exit(main())
```

---

## Testing Pattern

```python
def test_cli_adapter_dispatches_create_command():
    """CLI adapter creates and dispatches command."""
    mock_cmd_dispatcher = Mock(spec=ICommandDispatcher)
    mock_cmd_dispatcher.dispatch.return_value = [
        WorkItemCreated(work_item_id="WORK-001", title="Test")
    ]

    adapter = CLIAdapter(
        command_dispatcher=mock_cmd_dispatcher,
        query_dispatcher=Mock(),
    )

    exit_code = adapter.create_task("Test Task", priority="high")

    assert exit_code == 0
    mock_cmd_dispatcher.dispatch.assert_called_once()
    cmd = mock_cmd_dispatcher.dispatch.call_args[0][0]
    assert isinstance(cmd, CreateWorkItemCommand)
    assert cmd.title == "Test Task"


def test_cli_adapter_handles_validation_error():
    """CLI adapter returns exit code 1 on validation error."""
    mock_dispatcher = Mock(spec=ICommandDispatcher)
    mock_dispatcher.dispatch.side_effect = ValidationError(
        field="title",
        message="cannot be empty",
    )

    adapter = CLIAdapter(
        command_dispatcher=mock_dispatcher,
        query_dispatcher=Mock(),
    )

    exit_code = adapter.create_task("")

    assert exit_code == 1


def test_cli_adapter_handles_not_found():
    """CLI adapter returns exit code 1 on not found."""
    mock_dispatcher = Mock(spec=IQueryDispatcher)
    mock_dispatcher.dispatch.side_effect = NotFoundError(
        entity_type="Task",
        entity_id="WORK-999",
    )

    adapter = CLIAdapter(
        command_dispatcher=Mock(),
        query_dispatcher=mock_dispatcher,
    )

    exit_code = adapter.get_task("WORK-999")

    assert exit_code == 1
```

---

## Exit Code Convention

| Exit Code | Meaning | Example |
|-----------|---------|---------|
| 0 | Success | Operation completed |
| 1 | Domain/Business Error | Validation, NotFound, InvalidState |
| 2 | Unexpected Error | Unhandled exception |

---

## Jerry-Specific Decisions

> **Jerry Decision**: CLI adapter receives dispatchers via constructor injection.

> **Jerry Decision**: Exit codes follow Unix convention (0=success, non-zero=error).

> **Jerry Decision**: Domain exceptions are translated to user-friendly messages.

---

## References

- **Clean Architecture**: Chapter 26 - The Main Component
- **Design Canon**: Section 7.1 - CLI Adapter
- **Related Patterns**: PAT-ARCH-002 (Ports and Adapters), PAT-CQRS-003 (Dispatcher)
