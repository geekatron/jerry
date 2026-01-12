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
from typing import Any

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
from src.work_tracking.application.handlers.queries.get_work_item_query_handler import (
    WorkItemNotFoundError,
)
from src.work_tracking.application.queries import GetWorkItemQuery, ListWorkItemsQuery


class CLIAdapter:
    """Clean Architecture CLI Adapter.

    Receives a dispatcher via constructor injection and routes
    all commands through it.

    Attributes:
        _dispatcher: The query dispatcher for routing queries
        _projects_dir: Path to projects directory
        _session_handlers: Optional dictionary of session command handlers
    """

    def __init__(
        self,
        dispatcher: IQueryDispatcher,
        projects_dir: str | None = None,
        session_handlers: dict[str, Any] | None = None,
    ) -> None:
        """Initialize the CLI adapter.

        Args:
            dispatcher: Query dispatcher for routing queries
            projects_dir: Optional projects directory override
            session_handlers: Optional dict of session command handlers
                Keys: "create", "end", "abandon"

        Raises:
            ValueError: If dispatcher is None
        """
        if dispatcher is None:
            raise ValueError("dispatcher cannot be None")

        self._dispatcher = dispatcher
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

    def _format_project_table(self, projects: list) -> str:
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

    def _format_items_table(self, items: list) -> None:
        """Format work items as a readable table.

        Args:
            items: List of WorkItemDTO objects
        """
        print(f"{'ID':<12} {'TITLE':<30} {'STATUS':<12} {'PRIORITY':<10} {'TYPE':<8}")
        print("-" * 80)

        for item in items:
            title = item.title[:28] + ".." if len(item.title) > 30 else item.title
            print(f"{item.id:<12} {title:<30} {item.status:<12} {item.priority:<10} {item.work_type:<8}")

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
        parent: str | None = None,
        json_output: bool = False,
    ) -> int:
        """Create a new work item.

        Args:
            title: Work item title
            work_type: Work item type (task, bug, story, etc.)
            parent: Optional parent work item ID
            json_output: Whether to output as JSON

        Returns:
            Exit code (0 for success, 1 for error)

        Note:
            Stub implementation. Full implementation in Phase 4.5.
        """
        if json_output:
            print(json.dumps({"error": "Items commands not yet implemented"}))
        else:
            print("Error: Items commands not yet implemented (Phase 4.5)")
        return 1

    def cmd_items_start(
        self,
        item_id: str,
        json_output: bool = False,
    ) -> int:
        """Start work on an item.

        Args:
            item_id: Work item ID to start
            json_output: Whether to output as JSON

        Returns:
            Exit code (0 for success, 1 for error)

        Note:
            Stub implementation. Full implementation in Phase 4.5.
        """
        if json_output:
            print(json.dumps({"error": "Items commands not yet implemented"}))
        else:
            print("Error: Items commands not yet implemented (Phase 4.5)")
        return 1

    def cmd_items_complete(
        self,
        item_id: str,
        json_output: bool = False,
    ) -> int:
        """Complete a work item.

        Args:
            item_id: Work item ID to complete
            json_output: Whether to output as JSON

        Returns:
            Exit code (0 for success, 1 for error)

        Note:
            Stub implementation. Full implementation in Phase 4.5.
        """
        if json_output:
            print(json.dumps({"error": "Items commands not yet implemented"}))
        else:
            print("Error: Items commands not yet implemented (Phase 4.5)")
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
            reason: Reason for blocking
            json_output: Whether to output as JSON

        Returns:
            Exit code (0 for success, 1 for error)

        Note:
            Stub implementation. Full implementation in Phase 4.5.
        """
        if json_output:
            print(json.dumps({"error": "Items commands not yet implemented"}))
        else:
            print("Error: Items commands not yet implemented (Phase 4.5)")
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

        Note:
            Stub implementation. Full implementation in Phase 4.5.
        """
        if json_output:
            print(json.dumps({"error": "Items commands not yet implemented"}))
        else:
            print("Error: Items commands not yet implemented (Phase 4.5)")
        return 1
