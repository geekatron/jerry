"""
Application Ports Package.

Contains port (interface) definitions for the application layer.
These are the contracts that adapters must implement.

Exports:
    IQueryDispatcher: Protocol for query dispatchers
    ICommandDispatcher: Protocol for command dispatchers
    QueryHandlerNotFoundError: Exception for missing handlers
    DuplicateHandlerError: Exception for duplicate handlers
"""

from .dispatcher import (
    DuplicateHandlerError,
    ICommandDispatcher,
    IQueryDispatcher,
    QueryHandlerNotFoundError,
)

__all__ = [
    "IQueryDispatcher",
    "ICommandDispatcher",
    "QueryHandlerNotFoundError",
    "DuplicateHandlerError",
]
