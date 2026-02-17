# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
RetrieveProjectContextQuery - Query for getting project context.

This is a pure data object - no dependencies, no behavior.
Used by the dispatcher to route to the handler.

Attributes:
    base_path: The base path to the projects directory
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RetrieveProjectContextQuery:
    """Query for retrieving full project context.

    The context includes:
    - Current JERRY_PROJECT environment variable
    - Parsed and validated project ID
    - List of available projects
    - Next available project number

    Attributes:
        base_path: Path to the projects directory
    """

    base_path: str
