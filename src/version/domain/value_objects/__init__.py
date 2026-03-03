# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Version domain value objects."""

from __future__ import annotations

from .bump_type import BumpType
from .conventional_commit import ConventionalCommit

__all__ = [
    "BumpType",
    "ConventionalCommit",
]
