"""
Application Dispatchers Package.

Contains dispatcher implementations for CQRS pattern.

Exports:
    QueryDispatcher: Implementation of IQueryDispatcher
"""

from .query_dispatcher import QueryDispatcher

__all__ = [
    "QueryDispatcher",
]
