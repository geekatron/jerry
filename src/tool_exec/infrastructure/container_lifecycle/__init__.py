# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak
"""Container lifecycle management package for the /rainbow skill orchestrator.

Implements ADR-PROJ023-007 Option D (Hybrid: Zone 1 eager, Zone 2/3 lazy
with scope gate).
"""

from src.tool_exec.infrastructure.container_lifecycle.cluster_state import ClusterState
from src.tool_exec.infrastructure.container_lifecycle.cluster_status import ClusterStatus
from src.tool_exec.infrastructure.container_lifecycle.container_lifecycle_manager import (
    ContainerLifecycleManager,
)
from src.tool_exec.infrastructure.container_lifecycle.docker_compose_adapter import (
    DockerComposeAdapter,
)
from src.tool_exec.infrastructure.container_lifecycle.service_status import ServiceStatus
from src.tool_exec.infrastructure.container_lifecycle.session_state import SessionState
from src.tool_exec.infrastructure.container_lifecycle.teardown_result import TeardownResult
from src.tool_exec.infrastructure.container_lifecycle.worktree_isolation import (
    derive_compose_project_name,
    session_state_path,
)

__all__ = [
    "ClusterState",
    "ClusterStatus",
    "ContainerLifecycleManager",
    "DockerComposeAdapter",
    "ServiceStatus",
    "SessionState",
    "TeardownResult",
    "derive_compose_project_name",
    "session_state_path",
]
