"""
Application Ports Package.

Contains port (interface) definitions for the application layer.
These are the contracts that adapters must implement.

Structure:
    primary/ - Inbound ports (IQueryDispatcher, ICommandDispatcher)
    secondary/ - Outbound ports (IEventStore, IReadModelStore)

Exports:
    IQueryDispatcher: Protocol for query dispatchers
    ICommandDispatcher: Protocol for command dispatchers
    QueryHandlerNotFoundError: Exception for missing query handlers
    DuplicateHandlerError: Exception for duplicate handlers
"""

from src.application.ports.primary import (
    DuplicateHandlerError,
    ICommandDispatcher,
    IQueryDispatcher,
    QueryHandlerNotFoundError,
)

__all__ = [
    "DuplicateHandlerError",
    "ICommandDispatcher",
    "IQueryDispatcher",
    "QueryHandlerNotFoundError",
]
