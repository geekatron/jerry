# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak
"""Cluster status data class for container lifecycle management."""

from __future__ import annotations

from dataclasses import dataclass, field

from src.tool_exec.infrastructure.container_lifecycle.cluster_state import ClusterState
from src.tool_exec.infrastructure.container_lifecycle.service_status import ServiceStatus


@dataclass
class ClusterStatus:
    """Aggregate status of a Docker Compose cluster."""

    cluster_name: str
    compose_file: str
    state: ClusterState
    services: list[ServiceStatus] = field(default_factory=list)
    error: str | None = None
