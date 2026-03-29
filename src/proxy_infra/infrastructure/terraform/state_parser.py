# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Terraform state parser for proxy infrastructure.

Extracts resource attributes from terraform output -json and constructs
ProxyNode domain objects. Enforces chmod 600 on state files after write.

References:
    - TASK-023-102: Terraform runner + state parser
    - ADR-EN023-003: Infrastructure provisioning (Option C: Hybrid)
"""

from __future__ import annotations

import os
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from src.proxy_infra.domain.value_objects.node_status import NodeStatus
from src.proxy_infra.domain.value_objects.proxy_node import ProxyNode
from src.proxy_infra.domain.value_objects.proxy_role import ProxyRole
from src.proxy_infra.domain.value_objects.proxy_type import ProxyType


class StateParser:
    """Parses terraform output -json and constructs ProxyNode domain objects.

    Enforces chmod 600 on state files to prevent unauthorised reads of
    engagement infrastructure data (R-CHMOD-STATE OPSEC control).
    """

    def parse_output(self, output_json: dict[str, Any]) -> dict[str, str]:
        """Extract key resource attributes from terraform output -json.

        Args:
            output_json: Parsed JSON dict from ``terraform output -json``.
                Expected keys: droplet_ip, droplet_id, ssh_key_id, firewall_id.
                Each value is a dict with a "value" key.

        Returns:
            Dict with keys: droplet_ip, droplet_id, ssh_key_id, firewall_id.
        """
        return {
            "droplet_ip": str(output_json.get("droplet_ip", {}).get("value", "")),
            "droplet_id": str(output_json.get("droplet_id", {}).get("value", "")),
            "ssh_key_id": str(output_json.get("ssh_key_id", {}).get("value", "")),
            "firewall_id": str(output_json.get("firewall_id", {}).get("value", "")),
        }

    def to_proxy_node(
        self,
        output_json: dict[str, Any],
        engagement_id: str,
        region: str,
        socks_port: int = 1080,
    ) -> ProxyNode:
        """Construct a ProxyNode from terraform output.

        Args:
            output_json: Parsed JSON dict from ``terraform output -json``.
            engagement_id: Owning engagement identifier.
            region: Provider region identifier.
            socks_port: SOCKS5 listening port on the node.

        Returns:
            ProxyNode domain object.
        """
        parsed = self.parse_output(output_json)
        return ProxyNode(
            id=parsed["droplet_id"],
            provider="digitalocean",
            ip=parsed["droplet_ip"],
            region=region,
            role=ProxyRole.ACTIVE,
            proxy_type=ProxyType.DIRECT_SOCKS5,
            status=NodeStatus.CONFIGURING,
            ssh_key_id=parsed["ssh_key_id"],
            created_at=datetime.now(UTC),
            engagement_id=engagement_id,
            socks_port=socks_port,
        )

    @staticmethod
    def write_state(state_file: Path, content: str) -> None:
        """Write state content to file with chmod 600 enforcement.

        Args:
            state_file: Path to write the state file to.
            content: State file content (typically JSON).
        """
        state_file.write_text(content)
        os.chmod(state_file, 0o600)
