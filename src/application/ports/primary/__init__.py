"""
Primary Ports - Inbound Interfaces for Application Layer.

Primary ports define the contracts for inbound operations.
These are implemented by the application layer and called by
interface adapters (CLI, API, etc.).

Ports:
    IQueryDispatcher: Dispatches read queries to appropriate handlers
    ICommandDispatcher: Dispatches write commands to appropriate handlers

Per Clean Architecture:
    - Primary ports are CALLED by external layers (interface)
    - They are IMPLEMENTED in the application layer
"""

from src.application.ports.primary.icommanddispatcher import (
    CommandHandlerNotFoundError,
    DuplicateHandlerError,
    ICommandDispatcher,
)
from src.application.ports.primary.iquerydispatcher import (
    IQueryDispatcher,
    QueryHandlerNotFoundError,
)

__all__ = [
    "CommandHandlerNotFoundError",
    "DuplicateHandlerError",
    "ICommandDispatcher",
    "IQueryDispatcher",
    "QueryHandlerNotFoundError",
]
