# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
ScanProjectsQuery - Query for scanning available projects.

This is a pure data object - no dependencies, no behavior.
Used by the dispatcher to route to the handler.

Attributes:
    base_path: The base path to the projects directory
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ScanProjectsQuery:
    """Query for scanning all available projects.

    Returns a sorted list of ProjectInfo objects.

    Attributes:
        base_path: Path to the projects directory
    """

    base_path: str
