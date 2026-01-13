"""
CLIAdapter - Clean Architecture CLI Adapter.

This adapter receives a QueryDispatcher via constructor injection.
It does NOT instantiate any infrastructure adapters directly.

The adapter's responsibility is to:
1. Parse CLI arguments
2. Create query/command data objects
3. Dispatch queries through the injected dispatcher
4. Execute commands through injected handlers
5. Format and display results

NO infrastructure imports are allowed in this module.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import TYPE_CHECKING, Any

from src.application.ports.primary.icommanddispatcher import (
    ICommandDispatcher,
)
from src.application.ports.primary.iquerydispatcher import IQueryDispatcher
from src.application.queries import (
    RetrieveProjectContextQuery,
    ScanProjectsQuery,
    ValidateProjectQuery,
)
from src.session_management.application.commands import (
    AbandonSessionCommand,
    CreateSessionCommand,
    EndSessionCommand,
)
from src.session_management.application.queries import GetSessionStatusQuery
from src.shared_kernel.exceptions import InvalidStateTransitionError, ValidationError
from src.work_tracking.application.commands import (
    BlockWorkItemCommand,
    CancelWorkItemCommand,
    CompleteWorkItemCommand,
    CreateWorkItemCommand,
    StartWorkItemCommand,
)
from src.work_tracking.application.handlers.queries.get_work_item_query_handler import (
    WorkItemNotFoundError,
)
from src.work_tracking.application.queries import GetWorkItemQuery, ListWorkItemsQuery
from src.work_tracking.domain.ports.repository import AggregateNotFoundError

if TYPE_CHECKING:
    pass


class CLIAdapter:
    """Clean Architecture CLI Adapter.

    Receives dispatchers via constructor injection and routes
    all queries and commands through them.

    Attributes:
        _dispatcher: The query dispatcher for routing queries
        _command_dispatcher: The command dispatcher for routing commands
        _projects_dir: Path to projects directory
        _session_handlers: Optional dictionary of session command handlers
    """

    def __init__(
        self,
        dispatcher: IQueryDispatcher,
        projects_dir: str | None = None,
        session_handlers: dict[str, Any] | None = None,
        command_dispatcher: ICommandDispatcher | None = None,
    ) -> None:
        """Initialize the CLI adapter.

        Args:
            dispatcher: Query dispatcher for routing queries
            projects_dir: Optional projects directory override
            session_handlers: Optional dict of session command handlers
                Keys: "create", "end", "abandon"
            command_dispatcher: Optional command dispatcher for work item commands

        Raises:
            ValueError: If dispatcher is None
        """
        if dispatcher is None:
            raise ValueError("dispatcher cannot be None")

        self._dispatcher = dispatcher
        self._command_dispatcher = command_dispatcher
        self._session_handlers = session_handlers

        # Use bootstrap helper if not provided
        if projects_dir is None:
            from src.bootstrap import get_projects_directory

            projects_dir = get_projects_directory()

        self._projects_dir = projects_dir

    def cmd_init(self, json_output: bool = False) -> int:
        """Execute the init command (deprecated, use cmd_projects_context).

        Args:
            json_output: Whether to output as JSON

        Returns:
            Exit code (0 for success)
        """
        return self.cmd_projects_context(json_output=json_output)

    def cmd_projects_context(self, json_output: bool = False) -> int:
        """Display project context (replaces 'init' in v0.1.0).

        Args:
            json_output: Whether to output as JSON

        Returns:
            Exit code (0 for success)
        """
        query = RetrieveProjectContextQuery(base_path=self._projects_dir)
        context = self._dispatcher.dispatch(query)

        if json_output:
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
            self._format_init_output(context)

        return 0

    def _format_init_output(self, context: dict[str, Any]) -> None:
        """Format init command output for human consumption."""
        jerry_project = context["jerry_project"]
        project_id = context["project_id"]
        validation = context["validation"]

        if jerry_project is None:
            print("JERRY_PROJECT: (not set)")
            print("\nSet JERRY_PROJECT environment variable to activate a project.")
            print("\nAvailable projects:")
            print(self._format_project_table(context["available_projects"]))
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

    def cmd_projects_list(self, json_output: bool = False) -> int:
        """Execute the projects list command.

        Args:
            json_output: Whether to output as JSON

        Returns:
            Exit code (0 for success)
        """
        query = ScanProjectsQuery(base_path=self._projects_dir)
        projects = self._dispatcher.dispatch(query)

        if json_output:
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
            print(self._format_project_table(projects))
            print(f"\nTotal: {len(projects)} project(s)")

        return 0

    def cmd_projects_validate(
        self,
        project_id_str: str,
        json_output: bool = False,
    ) -> int:
        """Execute the projects validate command.

        Args:
            project_id_str: Project ID to validate
            json_output: Whether to output as JSON

        Returns:
            Exit code (0 for valid, 1 for invalid)
        """
        query = ValidateProjectQuery(
            base_path=self._projects_dir,
            project_id_str=project_id_str,
        )
        project_id, validation = self._dispatcher.dispatch(query)

        if json_output:
            output = {
                "project_id": str(project_id) if project_id else None,
                "is_valid": validation.is_valid,
                "messages": validation.messages,
            }
            print(json.dumps(output, indent=2))
        else:
            if project_id is None:
                print(f"Invalid project ID format: {project_id_str}")
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

    def _format_project_table(self, projects: list[Any]) -> str:
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

    # =========================================================================
    # Session Namespace Commands (Phase 4.3)
    # =========================================================================

    def cmd_session_start(
        self,
        name: str | None = None,
        description: str | None = None,
        json_output: bool = False,
    ) -> int:
        """Start a new session.

        Args:
            name: Optional session name
            description: Optional session description
            json_output: Whether to output as JSON

        Returns:
            Exit code (0 for success, 1 for error)
        """
        if self._session_handlers is None:
            if json_output:
                print(json.dumps({"error": "Session handlers not configured"}))
            else:
                print("Error: Session handlers not configured")
            return 1

        handler = self._session_handlers.get("create")
        if handler is None:
            if json_output:
                print(json.dumps({"error": "CreateSession handler not available"}))
            else:
                print("Error: CreateSession handler not available")
            return 1

        try:
            command = CreateSessionCommand(
                name=name,
                description=description,
            )
            events = handler.handle(command)

            # Get the created session ID from the first event (uses aggregate_id)
            session_id = events[0].aggregate_id if events else "unknown"

            if json_output:
                output = {
                    "success": True,
                    "session_id": session_id,
                    "message": "Session started",
                }
                print(json.dumps(output, indent=2))
            else:
                print(f"Session started: {session_id}")
                if description:
                    print(f"Description: {description}")

            return 0

        except Exception as e:
            error_msg = str(e)
            if json_output:
                print(json.dumps({"error": error_msg}))
            else:
                print(f"Error: {error_msg}")
            return 1

    def cmd_session_end(
        self,
        summary: str | None = None,
        json_output: bool = False,
    ) -> int:
        """End the current session.

        Args:
            summary: Optional session summary
            json_output: Whether to output as JSON

        Returns:
            Exit code (0 for success, 1 for error)
        """
        if self._session_handlers is None:
            if json_output:
                print(json.dumps({"error": "Session handlers not configured"}))
            else:
                print("Error: Session handlers not configured")
            return 1

        handler = self._session_handlers.get("end")
        if handler is None:
            if json_output:
                print(json.dumps({"error": "EndSession handler not available"}))
            else:
                print("Error: EndSession handler not available")
            return 1

        try:
            command = EndSessionCommand(summary=summary)
            events = handler.handle(command)

            # Get the session ID from the first event (uses aggregate_id)
            session_id = events[0].aggregate_id if events else "unknown"

            if json_output:
                output = {
                    "success": True,
                    "session_id": session_id,
                    "message": "Session ended",
                }
                print(json.dumps(output, indent=2))
            else:
                print(f"Session ended: {session_id}")
                if summary:
                    print(f"Summary: {summary}")

            return 0

        except Exception as e:
            error_msg = str(e)
            if json_output:
                print(json.dumps({"error": error_msg}))
            else:
                print(f"Error: {error_msg}")
            return 1

    def cmd_session_status(self, json_output: bool = False) -> int:
        """Show current session status.

        Args:
            json_output: Whether to output as JSON

        Returns:
            Exit code (0 for success)
        """
        query = GetSessionStatusQuery()
        status = self._dispatcher.dispatch(query)

        if json_output:
            output = {
                "has_active_session": status.has_active_session,
                "session_id": status.session_id,
                "status": status.status,
                "description": status.description,
                "project_id": status.project_id,
                "started_at": status.started_at.isoformat() if status.started_at else None,
            }
            print(json.dumps(output, indent=2))
        else:
            if not status.has_active_session:
                print("No active session.")
                print("\nUse 'jerry session start' to begin a new session.")
            else:
                print(f"Session ID: {status.session_id}")
                print(f"Status: {status.status}")
                if status.description:
                    print(f"Description: {status.description}")
                if status.project_id:
                    print(f"Project: {status.project_id}")
                if status.started_at:
                    print(f"Started: {status.started_at.strftime('%Y-%m-%d %H:%M:%S')}")

        return 0

    def cmd_session_abandon(
        self,
        reason: str | None = None,
        json_output: bool = False,
    ) -> int:
        """Abandon the current session.

        Args:
            reason: Optional reason for abandonment
            json_output: Whether to output as JSON

        Returns:
            Exit code (0 for success, 1 for error)
        """
        if self._session_handlers is None:
            if json_output:
                print(json.dumps({"error": "Session handlers not configured"}))
            else:
                print("Error: Session handlers not configured")
            return 1

        handler = self._session_handlers.get("abandon")
        if handler is None:
            if json_output:
                print(json.dumps({"error": "AbandonSession handler not available"}))
            else:
                print("Error: AbandonSession handler not available")
            return 1

        try:
            command = AbandonSessionCommand(reason=reason)
            events = handler.handle(command)

            # Get the session ID from the first event (uses aggregate_id)
            session_id = events[0].aggregate_id if events else "unknown"

            if json_output:
                output = {
                    "success": True,
                    "session_id": session_id,
                    "message": "Session abandoned",
                }
                print(json.dumps(output, indent=2))
            else:
                print(f"Session abandoned: {session_id}")
                if reason:
                    print(f"Reason: {reason}")

            return 0

        except Exception as e:
            error_msg = str(e)
            if json_output:
                print(json.dumps({"error": error_msg}))
            else:
                print(f"Error: {error_msg}")
            return 1

    # =========================================================================
    # Items Namespace Commands (Phase 4.4/4.5 - Stub implementations)
    # =========================================================================

    def cmd_items_list(
        self,
        status: str | None = None,
        work_type: str | None = None,
        limit: int | None = None,
        json_output: bool = False,
    ) -> int:
        """List work items.

        Args:
            status: Optional status filter (pending, in_progress, blocked, done, cancelled)
            work_type: Optional type filter (not yet implemented)
            limit: Maximum number of items to return
            json_output: Whether to output as JSON

        Returns:
            Exit code (0 for success)
        """
        # Note: work_type filter not yet implemented in query handler
        _ = work_type  # Suppress unused warning

        query = ListWorkItemsQuery(status=status, limit=limit)
        result = self._dispatcher.dispatch(query)

        if json_output:
            output = {
                "items": [
                    {
                        "id": item.id,
                        "title": item.title,
                        "status": item.status,
                        "priority": item.priority,
                        "work_type": item.work_type,
                        "assignee": item.assignee,
                    }
                    for item in result.items
                ],
                "total_count": result.total_count,
                "has_more": result.has_more,
            }
            print(json.dumps(output, indent=2))
        else:
            if not result.items:
                print("No work items found.")
                if status:
                    print(f"(filtered by status: {status})")
            else:
                self._format_items_table(result.items)
                print(f"\nShowing {len(result.items)} of {result.total_count} item(s)")
                if result.has_more:
                    print("(use --limit to see more)")

        return 0

    def _format_items_table(self, items: list[Any]) -> None:
        """Format work items as a readable table.

        Args:
            items: List of WorkItemDTO objects
        """
        print(f"{'ID':<12} {'TITLE':<30} {'STATUS':<12} {'PRIORITY':<10} {'TYPE':<8}")
        print("-" * 80)

        for item in items:
            title = item.title[:28] + ".." if len(item.title) > 30 else item.title
            print(
                f"{item.id:<12} {title:<30} {item.status:<12} {item.priority:<10} {item.work_type:<8}"
            )

    def cmd_items_show(
        self,
        item_id: str,
        json_output: bool = False,
    ) -> int:
        """Show work item details.

        Args:
            item_id: Work item ID to show
            json_output: Whether to output as JSON

        Returns:
            Exit code (0 for success, 1 for not found)
        """
        try:
            query = GetWorkItemQuery(work_item_id=item_id)
            item = self._dispatcher.dispatch(query)

            if json_output:
                output = {
                    "id": item.id,
                    "title": item.title,
                    "description": item.description,
                    "status": item.status,
                    "priority": item.priority,
                    "work_type": item.work_type,
                    "assignee": item.assignee,
                    "parent_id": item.parent_id,
                    "dependencies": item.dependencies,
                    "test_coverage": item.test_coverage,
                    "created_at": item.created_at.isoformat() if item.created_at else None,
                    "completed_at": item.completed_at.isoformat() if item.completed_at else None,
                }
                print(json.dumps(output, indent=2))
            else:
                print(f"Work Item: {item.id}")
                print(f"Title: {item.title}")
                print(f"Status: {item.status}")
                print(f"Priority: {item.priority}")
                print(f"Type: {item.work_type}")
                if item.description:
                    print(f"Description: {item.description}")
                if item.assignee:
                    print(f"Assignee: {item.assignee}")
                if item.parent_id:
                    print(f"Parent: {item.parent_id}")
                if item.dependencies:
                    print(f"Dependencies: {', '.join(item.dependencies)}")
                if item.test_coverage is not None:
                    print(f"Test Coverage: {item.test_coverage:.1f}%")
                if item.created_at:
                    print(f"Created: {item.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
                if item.completed_at:
                    print(f"Completed: {item.completed_at.strftime('%Y-%m-%d %H:%M:%S')}")

            return 0

        except WorkItemNotFoundError as e:
            if json_output:
                print(json.dumps({"error": str(e)}))
            else:
                print(f"Error: {e}")
            return 1

    def cmd_items_create(
        self,
        title: str,
        work_type: str = "task",
        priority: str = "medium",
        description: str = "",
        parent: str | None = None,
        json_output: bool = False,
    ) -> int:
        """Create a new work item.

        Args:
            title: Work item title
            work_type: Work item type (task, bug, story, spike)
            priority: Priority level (low, medium, high, critical)
            description: Optional description
            parent: Optional parent work item ID
            json_output: Whether to output as JSON

        Returns:
            Exit code (0 for success, 1 for error)
        """
        if self._command_dispatcher is None:
            if json_output:
                print(json.dumps({"error": "Command dispatcher not configured"}))
            else:
                print("Error: Command dispatcher not configured")
            return 1

        try:
            command = CreateWorkItemCommand(
                title=title,
                work_type=work_type,
                priority=priority,
                description=description,
                parent_id=parent,
            )
            events = self._command_dispatcher.dispatch(command)

            # Get the created work item ID from the first event
            work_item_id = events[0].aggregate_id if events else "unknown"

            if json_output:
                output = {
                    "success": True,
                    "work_item_id": work_item_id,
                    "title": title,
                    "work_type": work_type,
                    "priority": priority,
                    "message": "Work item created",
                }
                print(json.dumps(output, indent=2))
            else:
                print(f"Created work item: {work_item_id}")
                print(f"Title: {title}")
                print(f"Type: {work_type}")
                print(f"Priority: {priority}")

            return 0

        except ValidationError as e:
            if json_output:
                print(json.dumps({"error": str(e)}))
            else:
                print(f"Error: {e}")
            return 1

        except Exception as e:
            error_msg = str(e)
            if json_output:
                print(json.dumps({"error": error_msg}))
            else:
                print(f"Error: {error_msg}")
            return 1

    def cmd_items_start(
        self,
        item_id: str,
        reason: str | None = None,
        json_output: bool = False,
    ) -> int:
        """Start work on an item.

        Args:
            item_id: Work item ID to start
            reason: Optional reason for starting
            json_output: Whether to output as JSON

        Returns:
            Exit code (0 for success, 1 for error)
        """
        if self._command_dispatcher is None:
            if json_output:
                print(json.dumps({"error": "Command dispatcher not configured"}))
            else:
                print("Error: Command dispatcher not configured")
            return 1

        try:
            command = StartWorkItemCommand(
                work_item_id=item_id,
                reason=reason,
            )
            events = self._command_dispatcher.dispatch(command)

            # Get the work item ID from the first event
            work_item_id = events[0].aggregate_id if events else item_id

            if json_output:
                output = {
                    "success": True,
                    "work_item_id": work_item_id,
                    "status": "in_progress",
                    "message": "Work item started",
                }
                print(json.dumps(output, indent=2))
            else:
                print(f"Started work item: {work_item_id}")
                print("Status: in_progress")
                if reason:
                    print(f"Reason: {reason}")

            return 0

        except AggregateNotFoundError as e:
            if json_output:
                print(json.dumps({"error": str(e)}))
            else:
                print(f"Error: Work item '{item_id}' not found")
            return 1

        except InvalidStateTransitionError as e:
            if json_output:
                print(json.dumps({"error": str(e)}))
            else:
                print(f"Error: {e}")
            return 1

        except Exception as e:
            error_msg = str(e)
            if json_output:
                print(json.dumps({"error": error_msg}))
            else:
                print(f"Error: {error_msg}")
            return 1

    def cmd_items_complete(
        self,
        item_id: str,
        reason: str | None = None,
        json_output: bool = False,
    ) -> int:
        """Complete a work item.

        Args:
            item_id: Work item ID to complete
            reason: Optional reason for completion
            json_output: Whether to output as JSON

        Returns:
            Exit code (0 for success, 1 for error)
        """
        if self._command_dispatcher is None:
            if json_output:
                print(json.dumps({"error": "Command dispatcher not configured"}))
            else:
                print("Error: Command dispatcher not configured")
            return 1

        try:
            command = CompleteWorkItemCommand(
                work_item_id=item_id,
                reason=reason,
            )
            events = self._command_dispatcher.dispatch(command)

            # Get the work item ID from the first event
            work_item_id = events[0].aggregate_id if events else item_id

            if json_output:
                output = {
                    "success": True,
                    "work_item_id": work_item_id,
                    "status": "done",
                    "message": "Work item completed",
                }
                print(json.dumps(output, indent=2))
            else:
                print(f"Completed work item: {work_item_id}")
                print("Status: done")
                if reason:
                    print(f"Reason: {reason}")

            return 0

        except AggregateNotFoundError as e:
            if json_output:
                print(json.dumps({"error": str(e)}))
            else:
                print(f"Error: Work item '{item_id}' not found")
            return 1

        except InvalidStateTransitionError as e:
            if json_output:
                print(json.dumps({"error": str(e)}))
            else:
                print(f"Error: {e}")
            return 1

        except Exception as e:
            error_msg = str(e)
            if json_output:
                print(json.dumps({"error": error_msg}))
            else:
                print(f"Error: {error_msg}")
            return 1

    def cmd_items_block(
        self,
        item_id: str,
        reason: str,
        json_output: bool = False,
    ) -> int:
        """Block a work item.

        Args:
            item_id: Work item ID to block
            reason: Reason for blocking (required)
            json_output: Whether to output as JSON

        Returns:
            Exit code (0 for success, 1 for error)
        """
        if self._command_dispatcher is None:
            if json_output:
                print(json.dumps({"error": "Command dispatcher not configured"}))
            else:
                print("Error: Command dispatcher not configured")
            return 1

        try:
            command = BlockWorkItemCommand(
                work_item_id=item_id,
                reason=reason,
            )
            events = self._command_dispatcher.dispatch(command)

            # Get the work item ID from the first event
            work_item_id = events[0].aggregate_id if events else item_id

            if json_output:
                output = {
                    "success": True,
                    "work_item_id": work_item_id,
                    "status": "blocked",
                    "reason": reason,
                    "message": "Work item blocked",
                }
                print(json.dumps(output, indent=2))
            else:
                print(f"Blocked work item: {work_item_id}")
                print("Status: blocked")
                print(f"Reason: {reason}")

            return 0

        except AggregateNotFoundError as e:
            if json_output:
                print(json.dumps({"error": str(e)}))
            else:
                print(f"Error: Work item '{item_id}' not found")
            return 1

        except InvalidStateTransitionError as e:
            if json_output:
                print(json.dumps({"error": str(e)}))
            else:
                print(f"Error: {e}")
            return 1

        except Exception as e:
            error_msg = str(e)
            if json_output:
                print(json.dumps({"error": error_msg}))
            else:
                print(f"Error: {error_msg}")
            return 1

    def cmd_items_cancel(
        self,
        item_id: str,
        reason: str | None = None,
        json_output: bool = False,
    ) -> int:
        """Cancel a work item.

        Args:
            item_id: Work item ID to cancel
            reason: Optional reason for cancellation
            json_output: Whether to output as JSON

        Returns:
            Exit code (0 for success, 1 for error)
        """
        if self._command_dispatcher is None:
            if json_output:
                print(json.dumps({"error": "Command dispatcher not configured"}))
            else:
                print("Error: Command dispatcher not configured")
            return 1

        try:
            command = CancelWorkItemCommand(
                work_item_id=item_id,
                reason=reason,
            )
            events = self._command_dispatcher.dispatch(command)

            # Get the work item ID from the first event
            work_item_id = events[0].aggregate_id if events else item_id

            if json_output:
                output = {
                    "success": True,
                    "work_item_id": work_item_id,
                    "status": "cancelled",
                    "message": "Work item cancelled",
                }
                print(json.dumps(output, indent=2))
            else:
                print(f"Cancelled work item: {work_item_id}")
                print("Status: cancelled")
                if reason:
                    print(f"Reason: {reason}")

            return 0

        except AggregateNotFoundError as e:
            if json_output:
                print(json.dumps({"error": str(e)}))
            else:
                print(f"Error: Work item '{item_id}' not found")
            return 1

        except InvalidStateTransitionError as e:
            if json_output:
                print(json.dumps({"error": str(e)}))
            else:
                print(f"Error: {e}")
            return 1

        except Exception as e:
            error_msg = str(e)
            if json_output:
                print(json.dumps({"error": error_msg}))
            else:
                print(f"Error: {error_msg}")
            return 1

    # =========================================================================
    # Config Namespace Commands (WI-016)
    # =========================================================================

    def _get_project_root(self) -> Path:
        """Get the project root directory.

        Returns:
            Path to project root
        """
        project_dir = os.environ.get("CLAUDE_PROJECT_DIR")
        if project_dir:
            return Path(project_dir)
        return Path.cwd()

    def _create_config_adapter(self) -> Any:
        """Create a LayeredConfigAdapter for config commands.

        Note: This is a local import to avoid infrastructure imports at module level.

        Returns:
            LayeredConfigAdapter instance
        """
        from src.infrastructure.adapters.configuration.layered_config_adapter import (
            LayeredConfigAdapter,
        )

        root = self._get_project_root()
        jerry_project = os.environ.get("JERRY_PROJECT")

        project_config_path = None
        if jerry_project:
            project_config_path = root / "projects" / jerry_project / ".jerry" / "config.toml"

        return LayeredConfigAdapter(
            env_prefix="JERRY_",
            root_config_path=root / ".jerry" / "config.toml",
            project_config_path=project_config_path,
            defaults={
                "logging.level": "INFO",
                "work_tracking.auto_snapshot_interval": 10,
                "work_tracking.quality_gate_enabled": True,
                "session.auto_start": True,
                "session.max_duration_hours": 8,
            },
        )

    def cmd_config_show(
        self,
        show_source: bool = False,
        json_output: bool = False,
    ) -> int:
        """Show current configuration.

        Args:
            show_source: Whether to show the source of each value
            json_output: Whether to output as JSON

        Returns:
            Exit code (0 for success)

        References:
            - AC-016.1: jerry config show displays merged configuration
            - AC-016.2: jerry config show --json outputs JSON format
        """
        try:
            config = self._create_config_adapter()
            all_keys = config.all_keys()

            if json_output:
                output: dict[str, Any] = {}
                for key in sorted(all_keys):
                    value = config.get(key)
                    if show_source:
                        source = config.get_source(key)
                        output[key] = {"value": value, "source": source}
                    else:
                        output[key] = value
                print(json.dumps(output, indent=2))
            else:
                if not all_keys:
                    print("No configuration values found.")
                else:
                    if show_source:
                        print(f"{'KEY':<40} {'VALUE':<20} {'SOURCE':<10}")
                        print("-" * 70)
                        for key in sorted(all_keys):
                            value = config.get(key)
                            source = config.get_source(key)
                            value_str = str(value)[:18] if len(str(value)) > 20 else str(value)
                            print(f"{key:<40} {value_str:<20} {source:<10}")
                    else:
                        print(f"{'KEY':<40} {'VALUE':<30}")
                        print("-" * 70)
                        for key in sorted(all_keys):
                            value = config.get(key)
                            value_str = str(value)[:28] if len(str(value)) > 30 else str(value)
                            print(f"{key:<40} {value_str:<30}")

            return 0

        except Exception as e:
            if json_output:
                print(json.dumps({"error": str(e)}))
            else:
                print(f"Error: {e}")
            return 1

    def cmd_config_get(
        self,
        key: str,
        json_output: bool = False,
    ) -> int:
        """Get a configuration value.

        Args:
            key: Configuration key to retrieve
            json_output: Whether to output as JSON

        Returns:
            Exit code (0 for success, 1 for not found)

        References:
            - AC-016.3: jerry config get <key> retrieves specific value
        """
        try:
            config = self._create_config_adapter()
            value = config.get(key)

            if value is None:
                if json_output:
                    print(json.dumps({"error": f"Key '{key}' not found"}))
                else:
                    print(f"Error: Key '{key}' not found")
                return 1

            if json_output:
                source = config.get_source(key)
                print(json.dumps({"key": key, "value": value, "source": source}))
            else:
                print(value)

            return 0

        except Exception as e:
            if json_output:
                print(json.dumps({"error": str(e)}))
            else:
                print(f"Error: {e}")
            return 1

    def cmd_config_set(
        self,
        key: str,
        value: str,
        scope: str = "project",
        json_output: bool = False,
    ) -> int:
        """Set a configuration value.

        Args:
            key: Configuration key to set
            value: Value to set
            scope: Scope to write to (project, root, or local)
            json_output: Whether to output as JSON

        Returns:
            Exit code (0 for success, 1 for error)

        References:
            - AC-016.4: jerry config set <key> <value> --scope writes to appropriate file
        """
        try:
            import tomllib

            from src.infrastructure.adapters.persistence.atomic_file_adapter import (
                AtomicFileAdapter,
            )

            root = self._get_project_root()
            jerry_project = os.environ.get("JERRY_PROJECT")

            # Determine target file based on scope
            if scope == "project":
                if not jerry_project:
                    if json_output:
                        print(json.dumps({"error": "No active project. Set JERRY_PROJECT first."}))
                    else:
                        print("Error: No active project. Set JERRY_PROJECT first.")
                    return 1
                config_path = root / "projects" / jerry_project / ".jerry" / "config.toml"
            elif scope == "root":
                config_path = root / ".jerry" / "config.toml"
            elif scope == "local":
                config_path = root / ".jerry" / "local" / "context.toml"
            else:
                if json_output:
                    print(json.dumps({"error": f"Invalid scope: {scope}"}))
                else:
                    print(f"Error: Invalid scope: {scope}")
                return 1

            # Ensure parent directory exists
            config_path.parent.mkdir(parents=True, exist_ok=True)

            # Load existing config or start fresh
            file_adapter = AtomicFileAdapter()
            existing: dict[str, Any] = {}
            if config_path.exists():
                content = file_adapter.read_with_lock(config_path)
                if content.strip():
                    existing = tomllib.loads(content)

            # Parse key into nested structure
            parts = key.split(".")
            current = existing
            for part in parts[:-1]:
                if part not in current:
                    current[part] = {}
                current = current[part]

            # Coerce value type
            coerced_value: Any = value
            if value.lower() in ("true", "false"):
                coerced_value = value.lower() == "true"
            elif value.isdigit():
                coerced_value = int(value)
            else:
                try:
                    coerced_value = float(value)
                except ValueError:
                    pass

            current[parts[-1]] = coerced_value

            # Write back using TOML format
            def format_toml(d: dict[str, Any], prefix: str = "") -> str:
                """Simple TOML formatter for nested dicts."""
                lines: list[str] = []
                simple_items = []
                nested_items = []

                for k, v in d.items():
                    if isinstance(v, dict):
                        nested_items.append((k, v))
                    else:
                        simple_items.append((k, v))

                # Write simple key-value pairs first
                for k, v in simple_items:
                    if isinstance(v, bool):
                        lines.append(f"{k} = {str(v).lower()}")
                    elif isinstance(v, (int, float)):
                        lines.append(f"{k} = {v}")
                    else:
                        lines.append(f'{k} = "{v}"')

                # Write nested sections
                for k, v in nested_items:
                    section_key = f"{prefix}.{k}" if prefix else k
                    lines.append(f"\n[{section_key}]")
                    lines.append(format_toml(v, section_key))

                return "\n".join(lines)

            toml_content = format_toml(existing)
            file_adapter.write_atomic(config_path, toml_content + "\n")

            if json_output:
                print(
                    json.dumps(
                        {
                            "success": True,
                            "key": key,
                            "value": coerced_value,
                            "scope": scope,
                            "path": str(config_path),
                        }
                    )
                )
            else:
                print(f"Set {key} = {coerced_value}")
                print(f"Scope: {scope}")
                print(f"Path: {config_path}")

            return 0

        except Exception as e:
            if json_output:
                print(json.dumps({"error": str(e)}))
            else:
                print(f"Error: {e}")
            return 1

    def cmd_config_path(self, json_output: bool = False) -> int:
        """Show configuration file paths.

        Args:
            json_output: Whether to output as JSON

        Returns:
            Exit code (0 for success)

        References:
            - AC-016.5: jerry config path shows config file locations
        """
        root = self._get_project_root()
        jerry_project = os.environ.get("JERRY_PROJECT")

        paths = {
            "root": str(root / ".jerry" / "config.toml"),
            "local": str(root / ".jerry" / "local" / "context.toml"),
        }

        if jerry_project:
            paths["project"] = str(root / "projects" / jerry_project / ".jerry" / "config.toml")

        if json_output:
            output = {
                "paths": paths,
                "project_root": str(root),
                "active_project": jerry_project,
            }
            print(json.dumps(output, indent=2))
        else:
            print(f"Project Root: {root}")
            if jerry_project:
                print(f"Active Project: {jerry_project}")
            print()
            print("Configuration Files:")
            print(f"  Root:    {paths['root']}")
            if jerry_project:
                print(f"  Project: {paths['project']}")
            print(f"  Local:   {paths['local']}")

        return 0
