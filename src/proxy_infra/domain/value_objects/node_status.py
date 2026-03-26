# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""NodeStatus enum for proxy node lifecycle states.

References:
    - ADR-PROJ023-008: CLI Bounded Context Architecture for Proxy Infrastructure
    - EPIC-023-007: Proxy infrastructure automation
"""

from __future__ import annotations

from enum import Enum


class NodeStatus(str, Enum):
    """Lifecycle states for a proxy node."""

    PROVISIONING = "provisioning"
    CONFIGURING = "configuring"  # SSH key uploaded, firewall pending
    READY = "ready"              # Healthy and routable
    UNHEALTHY = "unhealthy"      # Failed health check
    BURNED = "burned"            # Detected/blocked, must rotate
    ROTATING = "rotating"        # Replacement in progress
    DESTROYING = "destroying"
    DESTROYED = "destroyed"
