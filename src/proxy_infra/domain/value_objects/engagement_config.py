# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""EngagementConfig value object — operator-provided engagement parameters.

Captures the minimal set of operator inputs required to bootstrap a fully
hands-free proxy infrastructure pipeline.  Parsed from a YAML engagement
config file by ``EngagementConfigParser``.

Domain invariants:
    - engagement_id must be non-empty (PI-002)
    - provider must be non-empty
    - region must be non-empty
    - count must be 1..10 (RATELIMIT-006)
    - operator_ip must be non-empty (firewall allowlisting)
    - engagement_tag derived from engagement_id (ISOLATION-001)

References:
    - TASK-023-050: Engagement config YAML schema, parser, and validator
    - FEAT-023-004: Hands-Free Engagement Pipeline Automation
"""

from __future__ import annotations

from dataclasses import dataclass

#: Maximum number of proxy nodes per engagement (RATELIMIT-006).
_MAX_NODES_PER_ENGAGEMENT: int = 10


@dataclass(frozen=True)
class EngagementConfig:
    """Immutable engagement configuration parsed from operator YAML.

    Attributes:
        engagement_id: Unique engagement identifier (e.g., "ENG-001").
        provider: Cloud provider name (e.g., "digitalocean").
        region: Provider region identifier (e.g., "nyc1").
        count: Number of proxy nodes to provision (1..10).
        proxy_type: Transport type (e.g., "direct_socks5").
        socks_port: SOCKS5 listening port on each node.
        operator_ip: Operator egress IP for firewall allowlisting.
        image: Provider OS image (default: ubuntu-24-04-x64).
        size: Provider instance size (default: s-1vcpu-1gb).
        engagement_tag: Derived tag for resource isolation (ISOLATION-001).
    """

    engagement_id: str
    provider: str
    region: str
    count: int
    proxy_type: str
    socks_port: int
    operator_ip: str
    image: str = "ubuntu-24-04-x64"
    size: str = "s-1vcpu-1gb"

    @property
    def engagement_tag(self) -> str:
        """Derive the engagement tag from the engagement ID.

        Returns:
            Tag string for resource isolation (ISOLATION-001).
        """
        return f"jerry-{self.engagement_id.lower()}"

    def __post_init__(self) -> None:
        """Enforce domain invariants on construction.

        Raises:
            ValueError: If any required field is empty or count is out of range.
        """
        if not self.engagement_id or not self.engagement_id.strip():
            raise ValueError(
                "engagement_id must not be empty — PI-002: engagement scoping required"
            )
        if not self.provider or not self.provider.strip():
            raise ValueError(
                "provider must not be empty — cloud provider required for provisioning"
            )
        if not self.region or not self.region.strip():
            raise ValueError(
                "region must not be empty — provider region required for provisioning"
            )
        if self.count < 1:
            raise ValueError(
                f"count={self.count} must be at least 1"
            )
        if self.count > _MAX_NODES_PER_ENGAGEMENT:
            raise ValueError(
                f"count={self.count} exceeds maximum of {_MAX_NODES_PER_ENGAGEMENT} "
                f"nodes per engagement — RATELIMIT-006"
            )
        if not self.operator_ip or not self.operator_ip.strip():
            raise ValueError(
                "operator_ip must not be empty — required for firewall allowlisting"
            )
