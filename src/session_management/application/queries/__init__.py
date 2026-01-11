"""
Queries - Read-Only Use Cases (CQRS Pattern)

Queries encapsulate read operations and return data without side effects.
Each query is a single-responsibility class that orchestrates port calls
and domain logic to fulfill a specific use case.
"""

from .get_next_number import GetNextProjectNumberQuery
from .get_project_context import GetProjectContextQuery
from .scan_projects import ScanProjectsQuery
from .validate_project import ValidateProjectQuery

__all__ = [
    "ScanProjectsQuery",
    "ValidateProjectQuery",
    "GetNextProjectNumberQuery",
    "GetProjectContextQuery",
]
