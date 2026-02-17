# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
ValidateProjectQueryHandler - Handler for ValidateProjectQuery.

This handler validates a specific project:
- Parses and validates the project ID format
- Checks that the project exists and has required configuration

Dependencies are injected via constructor, query data via handle().
"""

from __future__ import annotations

from src.application.queries.validate_project_query import ValidateProjectQuery
from src.session_management.application.ports import IProjectRepository
from src.session_management.domain import (
    InvalidProjectIdError,
    ProjectId,
    ValidationResult,
)


class ValidateProjectQueryHandler:
    """Handler for ValidateProjectQuery.

    Validates a project by ID and returns the validation result.

    Attributes:
        _repository: Repository for project operations
    """

    def __init__(self, repository: IProjectRepository) -> None:
        """Initialize the handler with dependencies.

        Args:
            repository: Repository for project operations
        """
        self._repository = repository

    def handle(self, query: ValidateProjectQuery) -> tuple[ProjectId | None, ValidationResult]:
        """Handle the ValidateProjectQuery.

        Args:
            query: Query data containing base_path and project_id_str

        Returns:
            Tuple of (ProjectId if valid format, ValidationResult)
            If the project ID format is invalid, returns (None, failure result)
        """
        # First, validate the project ID format
        try:
            project_id = ProjectId.parse(query.project_id_str)
        except InvalidProjectIdError as e:
            return None, ValidationResult.failure([e.message])

        # Then validate the project exists and is configured
        result = self._repository.validate_project(query.base_path, project_id)
        return project_id, result
