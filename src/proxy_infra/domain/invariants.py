# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Domain invariants for proxy infrastructure bounded context.

Defines and documents the proxy domain invariants PI-001 through PI-007.
These invariants are enforced by ProxyPoolService and PoolManifestStore.

References:
    - ADR-PROJ023-008: CLI Bounded Context Architecture for Proxy Infrastructure
    - EPIC-023-007: Proxy infrastructure automation
"""

from __future__ import annotations

# PI-001: Total nodes per engagement must not exceed max_nodes.
# Enforcement point: ProxyPoolService.provision() checks pool size before calling provisioner.
PI_001_MAX_NODES_PER_ENGAGEMENT = "PI-001"

# PI-002: All mutating operations require a valid engagement_id.
# Enforcement point: Every command handler validates engagement_id is non-empty before dispatch.
PI_002_ENGAGEMENT_ID_REQUIRED = "PI-002"

# PI-003: Burned nodes must not be reused; rotation creates a new node first.
# Enforcement point: ProxyPoolService.rotate() provisions replacement before destroying burned node.
PI_003_BURNED_NODE_NO_REUSE = "PI-003"

# PI-004: Pool manifest integrity hash must be verified on every read.
# Enforcement point: PoolManifestStore.load() computes and compares SHA-256 before returning manifest.
PI_004_MANIFEST_INTEGRITY_ON_READ = "PI-004"

# PI-005: SSH keys must be removed from provider on node destruction.
# Enforcement point: ProxyPoolService.destroy() sequence includes key removal via provisioner port.
PI_005_SSH_KEY_CLEANUP_ON_DESTROY = "PI-005"

# PI-006: Firewall rules must restrict SOCKS5 port to operator IP.
# Enforcement point: Default FirewallRule generation in provisioning config builder.
PI_006_SOCKS5_RESTRICTED_TO_OPERATOR_IP = "PI-006"

# PI-007: Audit log entry must be written for every mutating operation.
# Enforcement point: ProxyPoolService writes to AuditLogStore after every provision/destroy/rotate.
PI_007_AUDIT_LOG_ALL_MUTATIONS = "PI-007"


def describe_invariant(invariant_id: str) -> str:
    """Return a human-readable description of a domain invariant.

    Args:
        invariant_id: One of the PI-NNN constant strings defined in this module.

    Returns:
        A description string for the invariant.

    Raises:
        NotImplementedError: Always — not yet implemented (TASK-023-027).
    """
    raise NotImplementedError("TASK-023-027: not yet implemented")
