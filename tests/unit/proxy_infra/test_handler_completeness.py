# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""BDD unit tests for RotateHandler, AddProviderHandler, and HealthCheckHandler.

Closes H-20 violation identified during C4 quality gate (PROJ-023-EPIC-007-ITER3):
three handlers had zero test coverage.

Also verifies the OPSEC fix for RotateHandler (operator_ip must not be wildcard).

Test pyramid: 60% happy path / 30% negative / 10% edge cases.

References:
    - ADR-PROJ023-008: Application handler design
    - EPIC-023-007: Proxy infrastructure automation
"""

from __future__ import annotations

import os
from datetime import datetime, timezone
from unittest.mock import MagicMock, call

import pytest

from src.proxy_infra.application.commands.add_provider_command import AddProviderCommand
from src.proxy_infra.application.commands.rotate_node_command import RotateNodeCommand
from src.proxy_infra.application.handlers.add_provider_handler import AddProviderHandler
from src.proxy_infra.application.handlers.health_check_handler import HealthCheckHandler
from src.proxy_infra.application.handlers.rotate_handler import RotateHandler
from src.proxy_infra.application.queries.health_check_query import HealthCheckQuery
from src.proxy_infra.domain.exceptions.credential_not_found_error import CredentialNotFoundError
from src.proxy_infra.domain.exceptions.invalid_engagement_id_error import InvalidEngagementIdError
from src.proxy_infra.domain.value_objects.health_status import HealthStatus
from src.proxy_infra.domain.value_objects.node_status import NodeStatus
from src.proxy_infra.domain.value_objects.proxy_node import ProxyNode
from src.proxy_infra.domain.value_objects.proxy_role import ProxyRole
from src.proxy_infra.domain.value_objects.proxy_type import ProxyType


# =============================================================================
# Shared helpers
# =============================================================================

_OPERATOR_IP = "203.0.113.5"
_SSH_PUBLIC_KEY = "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAITest operator@host"


def _make_node(
    node_id: str = "node-001",
    ip: str = "192.0.2.10",
    status: NodeStatus = NodeStatus.READY,
    engagement_id: str = "ENG-2026-001",
) -> ProxyNode:
    """Build a minimal ProxyNode for test use."""
    return ProxyNode(
        id=node_id,
        provider="digitalocean",
        ip=ip,
        region="nyc1",
        role=ProxyRole.ACTIVE,
        proxy_type=ProxyType.SSH_TUNNEL,
        status=status,
        ssh_key_id="key-abc",
        created_at=datetime(2026, 3, 25, tzinfo=timezone.utc),
        engagement_id=engagement_id,
        socks_port=1080,
    )


def _make_health_status(
    node_id: str = "node-001",
    reachable: bool = True,
    socks_port_open: bool = True,
    ssh_accessible: bool = True,
) -> HealthStatus:
    """Build a HealthStatus for test use."""
    return HealthStatus(
        node_id=node_id,
        reachable=reachable,
        socks_port_open=socks_port_open,
        ssh_accessible=ssh_accessible,
        checked_at=datetime(2026, 3, 25, tzinfo=timezone.utc),
    )


def _make_pool_service(
    nodes: list[ProxyNode] | None = None,
    replacement_node: ProxyNode | None = None,
) -> MagicMock:
    """Build a mock ProxyPoolService with a mock provisioner attached."""
    if nodes is None:
        nodes = [_make_node()]
    if replacement_node is None:
        replacement_node = _make_node(node_id="node-new", ip="192.0.2.99")

    provisioner = MagicMock()
    provisioner.list_instances.return_value = nodes
    provisioner.provision.return_value = [replacement_node]

    pool_service = MagicMock()
    pool_service._provisioner = provisioner
    # validate_engagement_id raises on empty string — match real behavior
    pool_service.validate_engagement_id.side_effect = lambda eid: (
        (_ for _ in ()).throw(InvalidEngagementIdError("engagement_id required"))
        if not eid or not eid.strip()
        else None
    )
    return pool_service


def _make_rotate_handler(
    nodes: list[ProxyNode] | None = None,
    replacement_node: ProxyNode | None = None,
    operator_ip: str = _OPERATOR_IP,
    ssh_public_key: str = _SSH_PUBLIC_KEY,
) -> tuple[RotateHandler, MagicMock]:
    """Build RotateHandler with mocked pool service. Returns (handler, pool_service)."""
    pool_service = _make_pool_service(nodes=nodes, replacement_node=replacement_node)
    handler = RotateHandler(
        pool_service=pool_service,
        operator_ip=operator_ip,
        ssh_public_key=ssh_public_key,
    )
    return handler, pool_service


# =============================================================================
# RotateHandler tests
# =============================================================================


class TestRotateHandlerHappyPath:
    """Happy path tests for RotateHandler.handle() — 60% of suite weight."""

    def test_rotate_when_valid_node_then_marks_burned_and_provisions_replacement(
        self,
    ) -> None:
        """GIVEN a valid engagement and existing node WHEN handle THEN provisioner.provision called."""
        node = _make_node(node_id="node-001")
        handler, pool_service = _make_rotate_handler(nodes=[node])
        command = RotateNodeCommand(
            engagement_id="ENG-2026-001",
            node_id="node-001",
        )
        handler.handle(command)
        pool_service._provisioner.provision.assert_called_once()

    def test_rotate_returns_rotation_result_with_replacement_node(self) -> None:
        """GIVEN valid rotation WHEN handle THEN returns the replacement ProxyNode."""
        node = _make_node(node_id="node-001")
        replacement = _make_node(node_id="node-new", ip="192.0.2.99")
        handler, _ = _make_rotate_handler(nodes=[node], replacement_node=replacement)
        command = RotateNodeCommand(
            engagement_id="ENG-2026-001",
            node_id="node-001",
        )
        result = handler.handle(command)
        assert result is replacement

    def test_rotate_calls_validate_engagement_id(self) -> None:
        """GIVEN valid command WHEN handle THEN pool_service.validate_engagement_id called."""
        node = _make_node()
        handler, pool_service = _make_rotate_handler(nodes=[node])
        command = RotateNodeCommand(engagement_id="ENG-2026-001", node_id="node-001")
        handler.handle(command)
        pool_service.validate_engagement_id.assert_called_once_with("ENG-2026-001")

    def test_rotate_calls_list_instances_with_engagement_id(self) -> None:
        """GIVEN valid command WHEN handle THEN provisioner.list_instances called with engagement_id."""
        node = _make_node()
        handler, pool_service = _make_rotate_handler(nodes=[node])
        command = RotateNodeCommand(engagement_id="ENG-2026-001", node_id="node-001")
        handler.handle(command)
        pool_service._provisioner.list_instances.assert_called_once_with("ENG-2026-001")

    def test_rotate_passes_operator_ip_to_provision_config(self) -> None:
        """GIVEN custom operator_ip WHEN handle THEN ProvisionConfig.operator_ip matches."""
        node = _make_node(node_id="node-001")
        custom_ip = "198.51.100.42"
        handler, pool_service = _make_rotate_handler(nodes=[node], operator_ip=custom_ip)
        command = RotateNodeCommand(engagement_id="ENG-2026-001", node_id="node-001")
        handler.handle(command)
        call_args = pool_service._provisioner.provision.call_args
        provision_config = call_args[0][0]
        assert provision_config.operator_ip == custom_ip

    def test_rotate_passes_ssh_public_key_to_provision_config(self) -> None:
        """GIVEN custom ssh_public_key WHEN handle THEN ProvisionConfig.ssh_public_key matches."""
        node = _make_node(node_id="node-001")
        key = "ssh-rsa AAAA... recon@jerry"
        handler, pool_service = _make_rotate_handler(nodes=[node], ssh_public_key=key)
        command = RotateNodeCommand(engagement_id="ENG-2026-001", node_id="node-001")
        handler.handle(command)
        call_args = pool_service._provisioner.provision.call_args
        provision_config = call_args[0][0]
        assert provision_config.ssh_public_key == key


class TestRotateHandlerNegativeCases:
    """Negative / error path tests for RotateHandler.handle() — 30% of suite weight."""

    def test_rotate_when_node_not_found_then_raises_value_error(self) -> None:
        """GIVEN no node with matching node_id WHEN handle THEN raises ValueError."""
        node = _make_node(node_id="node-001")
        handler, _ = _make_rotate_handler(nodes=[node])
        command = RotateNodeCommand(
            engagement_id="ENG-2026-001",
            node_id="node-NONEXISTENT",
        )
        with pytest.raises(ValueError, match="node-NONEXISTENT"):
            handler.handle(command)

    def test_rotate_when_empty_engagement_id_then_raises(self) -> None:
        """GIVEN empty engagement_id WHEN handle THEN raises InvalidEngagementIdError."""
        handler, _ = _make_rotate_handler()
        command = RotateNodeCommand(engagement_id="", node_id="node-001")
        with pytest.raises(InvalidEngagementIdError):
            handler.handle(command)

    def test_rotate_when_whitespace_engagement_id_then_raises(self) -> None:
        """GIVEN whitespace-only engagement_id WHEN handle THEN raises InvalidEngagementIdError."""
        handler, _ = _make_rotate_handler()
        command = RotateNodeCommand(engagement_id="   ", node_id="node-001")
        with pytest.raises(InvalidEngagementIdError):
            handler.handle(command)

    def test_rotate_when_pool_empty_then_raises_value_error(self) -> None:
        """GIVEN empty node pool WHEN handle THEN raises ValueError for missing node."""
        handler, _ = _make_rotate_handler(nodes=[])
        command = RotateNodeCommand(engagement_id="ENG-2026-001", node_id="node-001")
        with pytest.raises(ValueError):
            handler.handle(command)

    def test_rotate_when_node_not_found_provision_not_called(self) -> None:
        """GIVEN node_id not in pool WHEN handle raises THEN provisioner.provision NOT called."""
        node = _make_node(node_id="node-001")
        handler, pool_service = _make_rotate_handler(nodes=[node])
        command = RotateNodeCommand(engagement_id="ENG-2026-001", node_id="node-MISSING")
        with pytest.raises(ValueError):
            handler.handle(command)
        pool_service._provisioner.provision.assert_not_called()


class TestRotateHandlerOpsecInvariant:
    """OPSEC invariant test — verifies wildcard operator_ip is never used in ProvisionConfig."""

    def test_rotate_operator_ip_is_not_wildcard(self) -> None:
        """GIVEN handler configured with specific operator_ip WHEN handle THEN 0.0.0.0 never passed.

        OPSEC: PI-006 requires firewall allowlist be scoped to operator IP.
        A wildcard 0.0.0.0 creates world-accessible replacement proxies,
        exposing the engagement infrastructure to the public internet.
        """
        node = _make_node(node_id="node-001")
        handler, pool_service = _make_rotate_handler(
            nodes=[node],
            operator_ip="203.0.113.5",
        )
        command = RotateNodeCommand(engagement_id="ENG-2026-001", node_id="node-001")
        handler.handle(command)

        call_args = pool_service._provisioner.provision.call_args
        provision_config = call_args[0][0]
        assert provision_config.operator_ip != "0.0.0.0", (
            "OPSEC VIOLATION: operator_ip must not be 0.0.0.0 — "
            "this would make the replacement proxy world-accessible (PI-006)."
        )


# =============================================================================
# AddProviderHandler tests
# =============================================================================


class TestAddProviderHandlerHappyPath:
    """Happy path tests for AddProviderHandler.handle() — 60% of suite weight."""

    def test_add_provider_when_env_var_set_then_stores_credential(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """GIVEN env var set WHEN handle THEN credential_store.store_credential called."""
        monkeypatch.setenv("DO_API_KEY", "test-api-key-abc123")
        credential_store = MagicMock()
        handler = AddProviderHandler(credential_store=credential_store)
        command = AddProviderCommand(name="digitalocean", api_key_env="DO_API_KEY")
        handler.handle(command)
        credential_store.store_credential.assert_called_once_with("digitalocean", "test-api-key-abc123")

    def test_add_provider_returns_success_result(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """GIVEN env var set WHEN handle THEN returns None (no exception)."""
        monkeypatch.setenv("DO_API_KEY", "token-xyz")
        credential_store = MagicMock()
        handler = AddProviderHandler(credential_store=credential_store)
        command = AddProviderCommand(name="digitalocean", api_key_env="DO_API_KEY")
        result = handler.handle(command)
        # handler returns None on success (fire-and-forget command)
        assert result is None

    def test_add_provider_passes_provider_name_to_store(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """GIVEN env var set WHEN handle THEN store called with correct provider name."""
        monkeypatch.setenv("VULTR_API_KEY", "vultr-token-001")
        credential_store = MagicMock()
        handler = AddProviderHandler(credential_store=credential_store)
        command = AddProviderCommand(name="vultr", api_key_env="VULTR_API_KEY")
        handler.handle(command)
        name_arg = credential_store.store_credential.call_args[0][0]
        assert name_arg == "vultr"

    def test_add_provider_reads_api_key_from_named_env_var(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """GIVEN CUSTOM_ENV_VAR set WHEN handle THEN key value passed to store."""
        monkeypatch.setenv("CUSTOM_ENV_VAR", "super-secret-key")
        credential_store = MagicMock()
        handler = AddProviderHandler(credential_store=credential_store)
        command = AddProviderCommand(name="provider-x", api_key_env="CUSTOM_ENV_VAR")
        handler.handle(command)
        key_arg = credential_store.store_credential.call_args[0][1]
        assert key_arg == "super-secret-key"


class TestAddProviderHandlerNegativeCases:
    """Negative / error path tests for AddProviderHandler.handle() — 30% of suite weight."""

    def test_add_provider_when_env_var_missing_then_raises_credential_not_found(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """GIVEN env var not set WHEN handle THEN raises CredentialNotFoundError."""
        monkeypatch.delenv("DO_API_KEY", raising=False)
        credential_store = MagicMock()
        handler = AddProviderHandler(credential_store=credential_store)
        command = AddProviderCommand(name="digitalocean", api_key_env="DO_API_KEY")
        with pytest.raises(CredentialNotFoundError):
            handler.handle(command)

    def test_add_provider_when_env_var_missing_then_store_not_called(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """GIVEN env var not set WHEN handle raises THEN store_credential NOT called."""
        monkeypatch.delenv("MISSING_KEY", raising=False)
        credential_store = MagicMock()
        handler = AddProviderHandler(credential_store=credential_store)
        command = AddProviderCommand(name="digitalocean", api_key_env="MISSING_KEY")
        with pytest.raises(CredentialNotFoundError):
            handler.handle(command)
        credential_store.store_credential.assert_not_called()

    def test_add_provider_when_env_var_empty_string_then_raises(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """GIVEN env var set to empty string WHEN handle THEN raises CredentialNotFoundError."""
        monkeypatch.setenv("DO_API_KEY", "")
        credential_store = MagicMock()
        handler = AddProviderHandler(credential_store=credential_store)
        command = AddProviderCommand(name="digitalocean", api_key_env="DO_API_KEY")
        with pytest.raises(CredentialNotFoundError):
            handler.handle(command)

    def test_add_provider_error_message_includes_env_var_name(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """GIVEN missing env var WHEN handle raises THEN error message contains var name."""
        monkeypatch.delenv("DO_API_KEY", raising=False)
        credential_store = MagicMock()
        handler = AddProviderHandler(credential_store=credential_store)
        command = AddProviderCommand(name="digitalocean", api_key_env="DO_API_KEY")
        with pytest.raises(CredentialNotFoundError, match="DO_API_KEY"):
            handler.handle(command)


# =============================================================================
# HealthCheckHandler tests
# =============================================================================


class TestHealthCheckHandlerHappyPath:
    """Happy path tests for HealthCheckHandler.handle() — 60% of suite weight."""

    def test_health_check_delegates_to_health_service(self) -> None:
        """GIVEN valid query WHEN handle THEN health_service.check_pool called."""
        health_service = MagicMock()
        health_service.check_pool.return_value = []
        handler = HealthCheckHandler(health_service=health_service)
        query = HealthCheckQuery(engagement_id="ENG-2026-001")
        handler.handle(query)
        health_service.check_pool.assert_called_once()

    def test_health_check_when_pool_healthy_then_returns_all_healthy(self) -> None:
        """GIVEN two healthy nodes WHEN handle THEN all returned statuses are healthy."""
        status_a = _make_health_status(node_id="node-001")
        status_b = _make_health_status(node_id="node-002")
        health_service = MagicMock()
        health_service.check_pool.return_value = [status_a, status_b]
        handler = HealthCheckHandler(health_service=health_service)
        query = HealthCheckQuery(engagement_id="ENG-2026-001")
        results = handler.handle(query)
        assert len(results) == 2
        assert all(s.is_healthy for s in results)

    def test_health_check_returns_list_of_health_statuses(self) -> None:
        """GIVEN service returns statuses WHEN handle THEN result type is list[HealthStatus]."""
        status = _make_health_status()
        health_service = MagicMock()
        health_service.check_pool.return_value = [status]
        handler = HealthCheckHandler(health_service=health_service)
        query = HealthCheckQuery(engagement_id="ENG-2026-001")
        results = handler.handle(query)
        assert isinstance(results, list)
        assert isinstance(results[0], HealthStatus)

    def test_health_check_passes_pool_with_query_engagement_id(self) -> None:
        """GIVEN query with engagement_id WHEN handle THEN pool passed to service has same engagement_id."""
        health_service = MagicMock()
        health_service.check_pool.return_value = []
        handler = HealthCheckHandler(health_service=health_service)
        query = HealthCheckQuery(engagement_id="ENG-2026-001")
        handler.handle(query)
        pool_arg = health_service.check_pool.call_args[0][0]
        assert pool_arg.engagement_id == "ENG-2026-001"

    def test_health_check_empty_pool_returns_empty_list(self) -> None:
        """GIVEN pool with no nodes WHEN handle THEN returns empty list."""
        health_service = MagicMock()
        health_service.check_pool.return_value = []
        handler = HealthCheckHandler(health_service=health_service)
        query = HealthCheckQuery(engagement_id="ENG-2026-001")
        results = handler.handle(query)
        assert results == []


class TestHealthCheckHandlerNegativeCases:
    """Negative / mixed-status path tests for HealthCheckHandler — 30% of suite weight."""

    def test_health_check_when_node_unhealthy_then_returns_mixed_status(self) -> None:
        """GIVEN one healthy and one unhealthy node WHEN handle THEN mixed statuses returned."""
        healthy = _make_health_status(node_id="node-001")
        unhealthy = _make_health_status(
            node_id="node-002",
            reachable=False,
            socks_port_open=False,
            ssh_accessible=False,
        )
        health_service = MagicMock()
        health_service.check_pool.return_value = [healthy, unhealthy]
        handler = HealthCheckHandler(health_service=health_service)
        query = HealthCheckQuery(engagement_id="ENG-2026-001")
        results = handler.handle(query)
        assert len(results) == 2
        healthy_results = [s for s in results if s.is_healthy]
        unhealthy_results = [s for s in results if not s.is_healthy]
        assert len(healthy_results) == 1
        assert len(unhealthy_results) == 1

    def test_health_check_propagates_service_exception(self) -> None:
        """GIVEN health_service raises WHEN handle THEN exception propagates to caller."""
        health_service = MagicMock()
        health_service.check_pool.side_effect = RuntimeError("network unreachable")
        handler = HealthCheckHandler(health_service=health_service)
        query = HealthCheckQuery(engagement_id="ENG-2026-001")
        with pytest.raises(RuntimeError, match="network unreachable"):
            handler.handle(query)

    def test_health_check_all_nodes_unreachable_all_unhealthy(self) -> None:
        """GIVEN all nodes unreachable WHEN handle THEN no healthy results."""
        unhealthy_a = _make_health_status(
            node_id="node-001",
            reachable=False,
            socks_port_open=False,
            ssh_accessible=False,
        )
        unhealthy_b = _make_health_status(
            node_id="node-002",
            reachable=False,
            socks_port_open=False,
            ssh_accessible=False,
        )
        health_service = MagicMock()
        health_service.check_pool.return_value = [unhealthy_a, unhealthy_b]
        handler = HealthCheckHandler(health_service=health_service)
        query = HealthCheckQuery()
        results = handler.handle(query)
        assert not any(s.is_healthy for s in results)


class TestHealthCheckHandlerEdgeCases:
    """Edge case tests for HealthCheckHandler — 10% of suite weight."""

    def test_health_check_with_blank_engagement_id_passes_to_service(self) -> None:
        """GIVEN blank engagement_id WHEN handle THEN service still called (all-engagements check)."""
        health_service = MagicMock()
        health_service.check_pool.return_value = []
        handler = HealthCheckHandler(health_service=health_service)
        query = HealthCheckQuery(engagement_id="")
        handler.handle(query)
        health_service.check_pool.assert_called_once()
