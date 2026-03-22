# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak
"""Service status data class for container lifecycle management."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ServiceStatus:
    """Status of a single Docker Compose service."""

    name: str
    state: str  # Docker's reported state (e.g., "running", "exited")
    health: str  # "healthy", "unhealthy", "starting", "none"
