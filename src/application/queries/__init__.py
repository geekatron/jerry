# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
Query Definitions for Application Layer.

Queries are pure data objects that define what data to retrieve.
They contain no behavior - just the data needed for a query.

Following CQRS:
- Queries are for READ operations
- They are dispatched to query handlers
- They return DTOs, never domain entities

Naming Convention:
    {Verb}{Noun}Query - e.g., RetrieveProjectContextQuery
"""

from src.application.queries.agent_config_queries import (
    ListAgentConfigsQuery,
    ShowAgentConfigQuery,
    ValidateAgentConfigQuery,
)
from src.application.queries.retrieve_project_context_query import (
    RetrieveProjectContextQuery,
)
from src.application.queries.scan_projects_query import ScanProjectsQuery
from src.application.queries.validate_project_query import ValidateProjectQuery

__all__ = [
    "ListAgentConfigsQuery",
    "RetrieveProjectContextQuery",
    "ScanProjectsQuery",
    "ShowAgentConfigQuery",
    "ValidateAgentConfigQuery",
    "ValidateProjectQuery",
]
