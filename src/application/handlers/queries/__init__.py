# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
Query Handlers for Application Layer.

Query handlers implement the business logic for read operations.
They receive queries and return DTOs.

Following CQRS:
- Query handlers are for READ operations
- They receive dependencies via constructor injection
- They return DTOs, never domain entities

Naming Convention:
    {Verb}{Noun}QueryHandler - e.g., RetrieveProjectContextQueryHandler
"""

from src.application.handlers.queries.agent_config_query_handlers import (
    ComposeAgentConfigQueryHandler,
    ListAgentConfigsQueryHandler,
    ShowAgentConfigQueryHandler,
    ValidateAgentConfigQueryHandler,
)
from src.application.handlers.queries.retrieve_project_context_query_handler import (
    RetrieveProjectContextQueryHandler,
)
from src.application.handlers.queries.scan_projects_query_handler import (
    ScanProjectsQueryHandler,
)
from src.application.handlers.queries.validate_project_query_handler import (
    ValidateProjectQueryHandler,
)

__all__ = [
    "ComposeAgentConfigQueryHandler",
    "ListAgentConfigsQueryHandler",
    "RetrieveProjectContextQueryHandler",
    "ScanProjectsQueryHandler",
    "ShowAgentConfigQueryHandler",
    "ValidateAgentConfigQueryHandler",
    "ValidateProjectQueryHandler",
]
