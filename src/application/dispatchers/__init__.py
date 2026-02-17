# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
Application Dispatchers Package.

Contains dispatcher implementations for CQRS pattern.

Exports:
    CommandDispatcher: Implementation of ICommandDispatcher
    QueryDispatcher: Implementation of IQueryDispatcher
"""

from .command_dispatcher import CommandDispatcher
from .query_dispatcher import QueryDispatcher

__all__ = [
    "CommandDispatcher",
    "QueryDispatcher",
]
