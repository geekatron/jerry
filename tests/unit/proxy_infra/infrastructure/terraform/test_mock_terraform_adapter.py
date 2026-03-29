# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Unit tests for MockTerraformProvisionerAdapter (EN-023-006 CI-safe mode).

RED phase: these tests define the mock adapter contract before implementation.

References:
    - EN-023-006: CI-Safe Terraform Mode
    - FEAT-023-014: Real E2E Engagement Lifecycle
"""

from __future__ import annotations

import pytest

from src.proxy_infra.domain.value_objects.node_status import NodeStatus
from src.proxy_infra.domain.value_objects.provision_config import ProvisionConfig
from src.proxy_infra.domain.value_objects.proxy_role import ProxyRole
from src.proxy_infra.domain.value_objects.proxy_type import ProxyType
from src.proxy_infra.infrastructure.adapters.mock_terraform_provisioner_adapter import (
    MockTerraformProvisionerAdapter,
)


@pytest.fixture()
def mock_adapter() -> MockTerraformProvisionerAdapter:
    """Create a MockTerraformProvisionerAdapter instance."""
    return MockTerraformProvisionerAdapter()


@pytest.fixture()
def provision_config() -> ProvisionConfig:
    """Create a standard provision config for testing."""
    return ProvisionConfig(
        provider="digitalocean",
        region="nyc1",
        engagement_id="E2E-RAINBOW-001",
        engagement_tag="jerry-e2e-E2E-RAINBOW-001",
        count=1,
        role=ProxyRole.ACTIVE,
        proxy_type=ProxyType.DIRECT_SOCKS5,
        ssh_public_key="ssh-ed25519 AAAA... test@e2e",
        operator_ip="127.0.0.1",
    )


class TestMockProvision:
    """Mock adapter provision returns deterministic localhost nodes."""

    def test_provision_returns_one_node(
        self,
        mock_adapter: MockTerraformProvisionerAdapter,
        provision_config: ProvisionConfig,
    ) -> None:
        """Provision returns exactly count=1 ProxyNode."""
        nodes = mock_adapter.provision(provision_config)
        assert len(nodes) == 1

    def test_provision_node_uses_localhost(
        self,
        mock_adapter: MockTerraformProvisionerAdapter,
        provision_config: ProvisionConfig,
    ) -> None:
        """Mock node IP is 127.0.0.1 for local E2E testing."""
        nodes = mock_adapter.provision(provision_config)
        assert nodes[0].ip == "127.0.0.1"

    def test_provision_node_has_socks_port(
        self,
        mock_adapter: MockTerraformProvisionerAdapter,
        provision_config: ProvisionConfig,
    ) -> None:
        """Mock node uses the configured SOCKS port."""
        nodes = mock_adapter.provision(provision_config)
        assert nodes[0].socks_port == 1080

    def test_provision_node_is_ready(
        self,
        mock_adapter: MockTerraformProvisionerAdapter,
        provision_config: ProvisionConfig,
    ) -> None:
        """Mock node status is READY immediately (no real provisioning delay)."""
        nodes = mock_adapter.provision(provision_config)
        assert nodes[0].status == NodeStatus.READY

    def test_provision_node_has_engagement_id(
        self,
        mock_adapter: MockTerraformProvisionerAdapter,
        provision_config: ProvisionConfig,
    ) -> None:
        """Mock node carries the engagement ID from config."""
        nodes = mock_adapter.provision(provision_config)
        assert nodes[0].engagement_id == "E2E-RAINBOW-001"

    def test_provision_multiple_nodes(
        self,
        mock_adapter: MockTerraformProvisionerAdapter,
    ) -> None:
        """Provision with count=2 returns 2 nodes with distinct IDs."""
        config = ProvisionConfig(
            provider="digitalocean",
            region="nyc1",
            engagement_id="E2E-RAINBOW-001",
            engagement_tag="jerry-e2e-E2E-RAINBOW-001",
            count=2,
            role=ProxyRole.ACTIVE,
            proxy_type=ProxyType.DIRECT_SOCKS5,
            ssh_public_key="ssh-ed25519 AAAA... test@e2e",
            operator_ip="127.0.0.1",
        )
        nodes = mock_adapter.provision(config)
        assert len(nodes) == 2
        assert nodes[0].id != nodes[1].id

    def test_provision_cost_guardrail_rejects_over_two(
        self,
        mock_adapter: MockTerraformProvisionerAdapter,
    ) -> None:
        """Cost guardrail: mock adapter also enforces max 2 nodes per engagement."""
        config = ProvisionConfig(
            provider="digitalocean",
            region="nyc1",
            engagement_id="E2E-RAINBOW-001",
            engagement_tag="jerry-e2e-E2E-RAINBOW-001",
            count=3,
            role=ProxyRole.ACTIVE,
            proxy_type=ProxyType.DIRECT_SOCKS5,
            ssh_public_key="ssh-ed25519 AAAA... test@e2e",
            operator_ip="127.0.0.1",
        )
        with pytest.raises(ValueError, match="[Cc]ost guardrail|max 2"):
            mock_adapter.provision(config)


class TestMockDestroy:
    """Mock adapter destroy is a no-op that reports success."""

    def test_destroy_returns_all_successful(
        self,
        mock_adapter: MockTerraformProvisionerAdapter,
    ) -> None:
        """Destroy reports all requested node IDs as destroyed."""
        result = mock_adapter.destroy(["mock-node-0", "mock-node-1"])
        assert result.destroyed == ["mock-node-0", "mock-node-1"]
        assert result.failed == []
        assert result.is_all_successful


class TestMockHealthCheck:
    """Mock adapter health check always returns healthy."""

    def test_health_check_returns_healthy(
        self,
        mock_adapter: MockTerraformProvisionerAdapter,
    ) -> None:
        """Mock health check always returns healthy for any node ID."""
        status = mock_adapter.health_check("mock-node-0")
        assert status.is_healthy
        assert status.reachable
        assert status.socks_port_open


class TestMockListNodes:
    """Mock adapter tracks provisioned nodes."""

    def test_list_nodes_after_provision(
        self,
        mock_adapter: MockTerraformProvisionerAdapter,
        provision_config: ProvisionConfig,
    ) -> None:
        """list_nodes returns nodes that were provisioned."""
        mock_adapter.provision(provision_config)
        nodes = mock_adapter.list_nodes()
        assert len(nodes) == 1

    def test_list_nodes_empty_before_provision(
        self,
        mock_adapter: MockTerraformProvisionerAdapter,
    ) -> None:
        """list_nodes returns empty list before any provisioning."""
        assert mock_adapter.list_nodes() == []


class TestModeSelection:
    """Mode selection logic: mock vs real adapter routing."""

    def test_mode_mock_when_env_var_set(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """JERRY_E2E_TERRAFORM_MODE=mock selects mock adapter."""
        monkeypatch.setenv("JERRY_E2E_TERRAFORM_MODE", "mock")
        monkeypatch.delenv("DIGITALOCEAN_TOKEN", raising=False)

        from src.proxy_infra.infrastructure.adapters.mock_terraform_provisioner_adapter import (
            select_provisioner_mode,
        )

        assert select_provisioner_mode() == "mock"

    def test_mode_mock_when_no_token(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Auto-detect: mock mode when DIGITALOCEAN_TOKEN is absent."""
        monkeypatch.delenv("JERRY_E2E_TERRAFORM_MODE", raising=False)
        monkeypatch.delenv("DIGITALOCEAN_TOKEN", raising=False)

        from src.proxy_infra.infrastructure.adapters.mock_terraform_provisioner_adapter import (
            select_provisioner_mode,
        )

        assert select_provisioner_mode() == "mock"

    def test_mode_real_when_token_present(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Auto-detect: real mode when DIGITALOCEAN_TOKEN is present."""
        monkeypatch.delenv("JERRY_E2E_TERRAFORM_MODE", raising=False)
        monkeypatch.setenv("DIGITALOCEAN_TOKEN", "test-token-value")

        from src.proxy_infra.infrastructure.adapters.mock_terraform_provisioner_adapter import (
            select_provisioner_mode,
        )

        assert select_provisioner_mode() == "real"

    def test_mode_real_explicit_without_token_raises(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """JERRY_E2E_TERRAFORM_MODE=real without token raises ValueError."""
        monkeypatch.setenv("JERRY_E2E_TERRAFORM_MODE", "real")
        monkeypatch.delenv("DIGITALOCEAN_TOKEN", raising=False)

        from src.proxy_infra.infrastructure.adapters.mock_terraform_provisioner_adapter import (
            select_provisioner_mode,
        )

        with pytest.raises(ValueError, match="DIGITALOCEAN_TOKEN"):
            select_provisioner_mode()
