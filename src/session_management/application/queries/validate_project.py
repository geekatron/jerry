"""
ValidateProjectQuery - Query to validate a specific project.

Checks that the project exists and has the required configuration files.
Returns detailed validation results with warnings for missing optional files.
"""

from __future__ import annotations

from dataclasses import dataclass

from ...domain import InvalidProjectIdError, ProjectId, ValidationResult
from ..ports import IProjectRepository


@dataclass
class ValidateProjectQuery:
    """Query to validate a specific project."""

    repository: IProjectRepository
    base_path: str
    project_id_str: str

    def execute(self) -> tuple[ProjectId | None, ValidationResult]:
        """Execute the validate project query.

        Returns:
            Tuple of (ProjectId if valid format, ValidationResult)
            If the project ID format is invalid, returns (None, failure result)
        """
        # First, validate the project ID format
        try:
            project_id = ProjectId.parse(self.project_id_str)
        except InvalidProjectIdError as e:
            return None, ValidationResult.failure([e.message])

        # Then validate the project exists and is configured
        result = self.repository.validate_project(self.base_path, project_id)
        return project_id, result
