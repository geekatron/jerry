"""
CLIAdapter - Clean Architecture CLI Adapter.

This adapter receives a QueryDispatcher via constructor injection.
It does NOT instantiate any infrastructure adapters directly.

The adapter's responsibility is to:
1. Parse CLI arguments
2. Create query data objects
3. Dispatch queries through the injected dispatcher
4. Format and display results

NO infrastructure imports are allowed in this module.
"""

from __future__ import annotations

import json
import sys
from typing import Any

from src.application.handlers import (
    GetProjectContextQueryData,
    ScanProjectsQueryData,
    ValidateProjectQueryData,
)
from src.application.ports.dispatcher import IQueryDispatcher


class CLIAdapter:
    """Clean Architecture CLI Adapter.

    Receives a dispatcher via constructor injection and routes
    all commands through it.

    Attributes:
        _dispatcher: The query dispatcher for routing queries
        _projects_dir: Path to projects directory
    """

    def __init__(
        self,
        dispatcher: IQueryDispatcher,
        projects_dir: str | None = None,
    ) -> None:
        """Initialize the CLI adapter.

        Args:
            dispatcher: Query dispatcher for routing queries
            projects_dir: Optional projects directory override

        Raises:
            ValueError: If dispatcher is None
        """
        if dispatcher is None:
            raise ValueError("dispatcher cannot be None")

        self._dispatcher = dispatcher

        # Use bootstrap helper if not provided
        if projects_dir is None:
            from src.bootstrap import get_projects_directory

            projects_dir = get_projects_directory()

        self._projects_dir = projects_dir

    def cmd_init(self, json_output: bool = False) -> int:
        """Execute the init command.

        Args:
            json_output: Whether to output as JSON

        Returns:
            Exit code (0 for success)
        """
        query = GetProjectContextQueryData(base_path=self._projects_dir)
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
        query = ScanProjectsQueryData(base_path=self._projects_dir)
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
        query = ValidateProjectQueryData(
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
