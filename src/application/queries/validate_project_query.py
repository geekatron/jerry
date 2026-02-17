# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
ValidateProjectQuery - Query for validating a specific project.

This is a pure data object - no dependencies, no behavior.
Used by the dispatcher to route to the handler.

Attributes:
    base_path: The base path to the projects directory
    project_id_str: The project ID string to validate
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ValidateProjectQuery:
    """Query for validating a specific project.

    Validates:
    - Project ID format is valid
    - Project directory exists
    - Project has required configuration

    Attributes:
        base_path: Path to the projects directory
        project_id_str: Project ID string to validate (e.g., "PROJ-001-example")
    """

    base_path: str
    project_id_str: str
