# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak
"""Cluster state enumeration for container lifecycle management."""

from __future__ import annotations

from enum import Enum


class ClusterState(Enum):
    """State of a Docker Compose cluster."""

    UNKNOWN = "unknown"
    STOPPED = "stopped"
    STARTING = "starting"
    RUNNING = "running"
    UNHEALTHY = "unhealthy"
    ERROR = "error"
