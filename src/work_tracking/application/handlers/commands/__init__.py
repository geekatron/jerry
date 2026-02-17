# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
Work Tracking Command Handlers.

Handlers for work item command operations.
These handlers implement the CQRS command pattern.

Command Handlers:
    CreateWorkItemCommandHandler: Creates new work items
    StartWorkItemCommandHandler: Starts work on an item
    CompleteWorkItemCommandHandler: Completes a work item
    BlockWorkItemCommandHandler: Blocks a work item
    CancelWorkItemCommandHandler: Cancels a work item

References:
    - PHASE-45-ITEMS-COMMANDS.md: Implementation tracker
    - PAT-CQRS-001: Command Pattern
"""

from .block_work_item_command_handler import BlockWorkItemCommandHandler
from .cancel_work_item_command_handler import CancelWorkItemCommandHandler
from .complete_work_item_command_handler import CompleteWorkItemCommandHandler
from .create_work_item_command_handler import CreateWorkItemCommandHandler
from .start_work_item_command_handler import StartWorkItemCommandHandler

__all__ = [
    "CreateWorkItemCommandHandler",
    "StartWorkItemCommandHandler",
    "CompleteWorkItemCommandHandler",
    "BlockWorkItemCommandHandler",
    "CancelWorkItemCommandHandler",
]
