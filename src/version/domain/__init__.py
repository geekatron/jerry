# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
Version Domain Layer.

Contains the core domain model: value objects and domain services.
This layer has NO external dependencies (stdlib only).
"""

from __future__ import annotations

from .value_objects.bump_type import BumpType
from .value_objects.conventional_commit import ConventionalCommit

__all__ = [
    "BumpType",
    "ConventionalCommit",
]
