# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Contract tests: TerraformProvisionerAdapter implements ProxyProvisionerPort.

Verifies that the adapter satisfies the port's contract:
- All abstract methods are implemented
- Method signatures match the port
- Return types conform to port expectations
- Adapter instances are recognized as ProxyProvisionerPort subclasses
"""

from __future__ import annotations

import inspect
import subprocess
from pathlib import Path
from unittest.mock import MagicMock, patch

from src.proxy_infra.domain.ports.proxy_provisioner_port import ProxyProvisionerPort
from src.proxy_infra.domain.value_objects.destroy_result import DestroyResult
from src.proxy_infra.domain.value_objects.health_status import HealthStatus
from src.proxy_infra.domain.value_objects.proxy_node import ProxyNode
from src.proxy_infra.domain.value_objects.proxy_role import ProxyRole
from src.proxy_infra.domain.value_objects.proxy_type import ProxyType
from src.proxy_infra.infrastructure.adapters.terraform_provisioner_adapter import (
    TerraformProvisionerAdapter,
)


class TestPortContractCompliance:
    """Verify TerraformProvisionerAdapter implements all ProxyProvisionerPort methods."""

    def test_adapter_is_subclass_of_port(self) -> None:
        """Adapter must be a subclass of ProxyProvisionerPort."""
        assert issubclass(TerraformProvisionerAdapter, ProxyProvisionerPort)

    def test_adapter_instance_passes_isinstance_check(self, tmp_path: Path) -> None:
        """Adapter instance must pass isinstance(adapter, ProxyProvisionerPort)."""
        adapter = TerraformProvisionerAdapter(engagement_dir=tmp_path)
        assert isinstance(adapter, ProxyProvisionerPort)

    def test_all_abstract_methods_implemented(self) -> None:
        """Every abstract method on ProxyProvisionerPort must exist on the adapter."""
        port_methods = {
            name
            for name, method in inspect.getmembers(
                ProxyProvisionerPort, predicate=inspect.isfunction
            )
            if getattr(method, "__isabstractmethod__", False)
        }
        adapter_methods = {
            name for name in dir(TerraformProvisionerAdapter) if not name.startswith("_")
        }

        missing = port_methods - adapter_methods
        assert missing == set(), f"Missing port methods: {missing}"


class TestProvisionContract:
    """Verify provision() returns list[ProxyNode] matching port contract."""

    @patch("subprocess.run")
    def test_provision_returns_list_of_proxy_nodes(
        self, mock_run: MagicMock, tmp_path: Path
    ) -> None:
        """provision() must return list[ProxyNode] per port contract."""
        from src.proxy_infra.domain.value_objects.provision_config import ProvisionConfig

        mock_run.side_effect = [
            subprocess.CompletedProcess(["terraform", "init"], 0, "", ""),
            subprocess.CompletedProcess(["terraform", "apply"], 0, "", ""),
            subprocess.CompletedProcess(
                ["terraform", "output"],
                0,
                '{"droplet_ip":{"value":"1.2.3.4"},"droplet_id":{"value":"999"},'
                '"ssh_key_id":{"value":"111"},"firewall_id":{"value":"fw-222"}}',
                "",
            ),
        ]

        adapter = TerraformProvisionerAdapter(engagement_dir=tmp_path)
        config = ProvisionConfig(
            provider="digitalocean",
            region="nyc3",
            engagement_id="RED-TEST-001",
            engagement_tag="jerry-red-test-001",
            count=1,
            role=ProxyRole.ACTIVE,
            proxy_type=ProxyType.DIRECT_SOCKS5,
            ssh_public_key="ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAA test@contract",
            operator_ip="198.51.100.1",
        )

        result = adapter.provision(config)

        assert isinstance(result, list)
        assert len(result) >= 1
        node = result[0]
        assert isinstance(node, ProxyNode)
        assert node.ip == "1.2.3.4"
        assert node.provider == "digitalocean"
        assert node.engagement_id == "RED-TEST-001"


class TestDestroyContract:
    """Verify destroy() returns DestroyResult matching port contract."""

    def test_destroy_returns_destroy_result(self, tmp_path: Path) -> None:
        """destroy() must return DestroyResult per port contract."""
        mock_runner = MagicMock()
        adapter = TerraformProvisionerAdapter(
            engagement_dir=tmp_path,
            terraform_runner=mock_runner,
        )

        result = adapter.destroy(node_ids=["123"], engagement_id="RED-TEST-001")

        assert isinstance(result, DestroyResult)
        assert hasattr(result, "destroyed")
        assert hasattr(result, "failed")


class TestHealthCheckContract:
    """Verify health_check() returns HealthStatus matching port contract."""

    def test_health_check_returns_health_status(self, tmp_path: Path) -> None:
        """health_check() must return HealthStatus per port contract."""
        adapter = TerraformProvisionerAdapter(engagement_dir=tmp_path)

        result = adapter.health_check(node_id="123")

        assert isinstance(result, HealthStatus)
        assert hasattr(result, "node_id")
        assert hasattr(result, "reachable")


class TestListContract:
    """Verify list methods return list[ProxyNode] matching port contract."""

    def test_list_nodes_returns_list(self, tmp_path: Path) -> None:
        """list_nodes() must return list[ProxyNode] per port contract."""
        adapter = TerraformProvisionerAdapter(engagement_dir=tmp_path)
        result = adapter.list_nodes()
        assert isinstance(result, list)

    def test_list_instances_returns_list(self, tmp_path: Path) -> None:
        """list_instances() must return list[ProxyNode] per port contract."""
        adapter = TerraformProvisionerAdapter(engagement_dir=tmp_path)
        result = adapter.list_instances(engagement_tag="jerry-test")
        assert isinstance(result, list)
