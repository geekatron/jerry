# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak
"""Teardown result data class for container lifecycle management."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class TeardownResult:
    """Result of tearing down clusters."""

    clusters_torn_down: list[str] = field(default_factory=list)
    volumes_removed: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    state_file_deleted: bool = False
