# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""BDD unit tests for orchestration handlers.

Covers:
  - SidecarLifecycleHandler (TASK-023-011)
  - SidecarComposeGenerator (TASK-023-012)
  - AutoProvisionHandler (TASK-023-014)
  - RotationHandler (TASK-023-015)
  - SecretsDistributionHandler (TASK-023-021)

All external dependencies (CLM, provisioner, ports) are mocked. No real
Docker or subprocess calls are made.

Test pyramid: 60% happy path / 30% negative/edge / 10% edge cases
"""

from __future__ import annotations

import tempfile
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import MagicMock, call

import pytest

from src.proxy_infra.application.handlers.auto_provision_handler import AutoProvisionHandler
from src.proxy_infra.application.handlers.provision_result import ProvisionResult
from src.proxy_infra.application.handlers.rotation_handler import RotationHandler
from src.proxy_infra.application.handlers.rotation_result import RotationResult
from src.proxy_infra.application.handlers.secrets_distribution_handler import (
    SecretsDistributionHandler,
)
from src.proxy_infra.application.handlers.sidecar_action import SidecarAction
from src.proxy_infra.application.handlers.sidecar_lifecycle_handler import (
    SidecarLifecycleHandler,
)
from src.proxy_infra.application.handlers.sidecar_lifecycle_result import SidecarLifecycleResult
from src.proxy_infra.domain.value_objects.destroy_result import DestroyResult
from src.proxy_infra.domain.value_objects.node_status import NodeStatus
from src.proxy_infra.domain.value_objects.proxy_node import ProxyNode
from src.proxy_infra.domain.value_objects.proxy_role import ProxyRole
from src.proxy_infra.domain.value_objects.proxy_type import ProxyType
from src.proxy_infra.infrastructure.compose.sidecar_compose import SidecarComposeGenerator


# =============================================================================
# Shared helpers
# =============================================================================


def _make_node(
    node_id: str = "node-001",
    ip: str = "203.0.113.10",
    proxy_type: ProxyType = ProxyType.SSH_TUNNEL,
) -> ProxyNode:
    """Build a minimal ProxyNode for test use."""
    return ProxyNode(
        id=node_id,
        provider="digitalocean",
        ip=ip,
        region="nyc1",
        role=ProxyRole.ACTIVE,
        proxy_type=proxy_type,
        status=NodeStatus.READY,
        ssh_key_id="key-abc",
        created_at=datetime(2026, 3, 25, tzinfo=timezone.utc),
        engagement_id="ENG-2026-001",
        socks_port=1080,
    )


def _make_clm(
    *,
    start_ok: bool = True,
    stop_ok: bool = True,
    running: bool = True,
) -> MagicMock:
    """Build a mock ContainerLifecyclePort."""
    clm = MagicMock()
    clm.start_sidecar.return_value = start_ok
    clm.stop_sidecar.return_value = stop_ok
    clm.is_sidecar_running.return_value = running
    return clm


# =============================================================================
# SidecarLifecycleHandler Tests
# =============================================================================


class TestSidecarLifecycleHandlerStart:
    """Tests for SidecarLifecycleHandler.start()."""

    def test_start_calls_clm_with_socks_profile(self) -> None:
        """GIVEN CLM succeeds WHEN start THEN CLM.start_sidecar called with socks profile."""
        clm = _make_clm()
        handler = SidecarLifecycleHandler(clm)
        handler.start()
        clm.start_sidecar.assert_called_once_with(profile="socks")

    def test_start_success_returns_success_result(self) -> None:
        """GIVEN CLM start succeeds WHEN start THEN result.success is True."""
        clm = _make_clm(start_ok=True, running=True)
        handler = SidecarLifecycleHandler(clm)
        result = handler.start()
        assert result.success is True
        assert result.action == SidecarAction.START

    def test_start_success_result_running_true(self) -> None:
        """GIVEN CLM reports running after start WHEN start THEN result.running is True."""
        clm = _make_clm(start_ok=True, running=True)
        handler = SidecarLifecycleHandler(clm)
        result = handler.start()
        assert result.running is True

    def test_start_failure_returns_failure_result(self) -> None:
        """GIVEN CLM start fails WHEN start THEN result.success is False."""
        clm = _make_clm(start_ok=False, running=False)
        handler = SidecarLifecycleHandler(clm)
        result = handler.start()
        assert result.success is False
        assert "start_sidecar" in result.error

    def test_start_with_custom_profile(self) -> None:
        """GIVEN custom socks_profile WHEN start THEN CLM called with that profile."""
        clm = _make_clm()
        handler = SidecarLifecycleHandler(clm, socks_profile="socks-ha")
        handler.start()
        clm.start_sidecar.assert_called_once_with(profile="socks-ha")


class TestSidecarLifecycleHandlerStop:
    """Tests for SidecarLifecycleHandler.stop()."""

    def test_stop_calls_clm_stop_sidecar(self) -> None:
        """GIVEN CLM succeeds WHEN stop THEN CLM.stop_sidecar called."""
        clm = _make_clm(stop_ok=True, running=False)
        handler = SidecarLifecycleHandler(clm)
        handler.stop()
        clm.stop_sidecar.assert_called_once()

    def test_stop_success_returns_success_result(self) -> None:
        """GIVEN CLM stop succeeds WHEN stop THEN result.success is True."""
        clm = _make_clm(stop_ok=True, running=False)
        handler = SidecarLifecycleHandler(clm)
        result = handler.stop()
        assert result.success is True
        assert result.action == SidecarAction.STOP

    def test_stop_failure_returns_failure_result(self) -> None:
        """GIVEN CLM stop fails WHEN stop THEN result.success is False."""
        clm = _make_clm(stop_ok=False, running=True)
        handler = SidecarLifecycleHandler(clm)
        result = handler.stop()
        assert result.success is False


class TestSidecarLifecycleHandlerRestart:
    """Tests for SidecarLifecycleHandler.restart()."""

    def test_restart_calls_stop_then_start(self) -> None:
        """GIVEN CLM succeeds WHEN restart THEN both stop and start are called."""
        clm = _make_clm(start_ok=True, stop_ok=True, running=True)
        handler = SidecarLifecycleHandler(clm)
        handler.restart()
        clm.stop_sidecar.assert_called_once()
        clm.start_sidecar.assert_called_once()

    def test_restart_returns_restart_action(self) -> None:
        """GIVEN CLM succeeds WHEN restart THEN result action is RESTART."""
        clm = _make_clm()
        handler = SidecarLifecycleHandler(clm)
        result = handler.restart()
        assert result.action == SidecarAction.RESTART

    def test_restart_short_circuits_when_stop_fails(self) -> None:
        """GIVEN stop fails WHEN restart THEN start is not called."""
        clm = _make_clm(stop_ok=False, running=True)
        handler = SidecarLifecycleHandler(clm)
        result = handler.restart()
        assert result.success is False
        clm.start_sidecar.assert_not_called()


class TestSidecarLifecycleHandlerStatus:
    """Tests for SidecarLifecycleHandler.status()."""

    def test_status_returns_running_true_when_sidecar_alive(self) -> None:
        """GIVEN CLM reports running WHEN status THEN result.running is True."""
        clm = _make_clm(running=True)
        handler = SidecarLifecycleHandler(clm)
        result = handler.status()
        assert result.running is True
        assert result.action == SidecarAction.STATUS

    def test_status_returns_running_false_when_sidecar_stopped(self) -> None:
        """GIVEN CLM reports not running WHEN status THEN result.running is False."""
        clm = _make_clm(running=False)
        handler = SidecarLifecycleHandler(clm)
        result = handler.status()
        assert result.running is False


# =============================================================================
# SidecarComposeGenerator Tests
# =============================================================================


class TestSidecarComposeGenerator:
    """Tests for SidecarComposeGenerator."""

    def test_render_service_contains_socks_bridge_name(self) -> None:
        """GIVEN zone3 WHEN render_service THEN yaml contains socks-bridge service name."""
        gen = SidecarComposeGenerator(zone="zone3-exploit")
        yaml = gen.render_service()
        assert "socks-bridge" in yaml

    def test_render_service_contains_socks_profile(self) -> None:
        """GIVEN zone3 WHEN render_service THEN yaml contains socks profile."""
        gen = SidecarComposeGenerator(zone="zone3-exploit")
        yaml = gen.render_service()
        assert "socks" in yaml
        assert "profiles" in yaml

    def test_render_service_contains_zone_network(self) -> None:
        """GIVEN zone3-exploit WHEN render_service THEN zone network in yaml."""
        gen = SidecarComposeGenerator(zone="zone3-exploit")
        yaml = gen.render_service()
        assert "zone3-exploit" in yaml

    def test_render_service_contains_egress_network(self) -> None:
        """GIVEN zone3 WHEN render_service THEN egress network referenced."""
        gen = SidecarComposeGenerator(zone="zone3-exploit")
        yaml = gen.render_service()
        assert "zone3-exploit-egress" in yaml

    def test_render_service_injects_env_vars(self) -> None:
        """GIVEN any zone WHEN render_service THEN SOCKS env vars with default syntax."""
        gen = SidecarComposeGenerator(zone="zone3-exploit")
        yaml = gen.render_service()
        assert "SOCKS_PROXY_POOL" in yaml
        assert "SOCKS_LB_STRATEGY" in yaml
        assert "SOCKS_FAIL_CLOSED" in yaml

    def test_render_service_contains_healthcheck(self) -> None:
        """GIVEN any zone WHEN render_service THEN healthcheck block is present."""
        gen = SidecarComposeGenerator(zone="zone3-exploit")
        yaml = gen.render_service()
        assert "healthcheck" in yaml

    def test_render_service_does_not_expose_host_ports(self) -> None:
        """GIVEN any zone WHEN render_service THEN no ports: key exposed to host."""
        gen = SidecarComposeGenerator(zone="zone3-exploit")
        yaml = gen.render_service()
        assert "ports:" not in yaml

    def test_render_egress_network_contains_zone_name(self) -> None:
        """GIVEN zone3-exploit WHEN render_egress_network THEN network name in yaml."""
        gen = SidecarComposeGenerator(zone="zone3-exploit")
        yaml = gen.render_egress_network()
        assert "zone3-exploit-egress" in yaml

    def test_zone_accessor_returns_configured_zone(self) -> None:
        """GIVEN zone3-exploit WHEN zone() THEN returns exact zone string."""
        gen = SidecarComposeGenerator(zone="zone3-exploit")
        assert gen.zone() == "zone3-exploit"

    def test_sidecar_port_accessor_returns_configured_port(self) -> None:
        """GIVEN port 9090 WHEN sidecar_port() THEN returns 9090."""
        gen = SidecarComposeGenerator(zone="zone3-exploit", sidecar_port=9090)
        assert gen.sidecar_port() == 9090

    def test_empty_zone_raises_value_error(self) -> None:
        """GIVEN empty zone WHEN construct THEN raises ValueError."""
        with pytest.raises(ValueError):
            SidecarComposeGenerator(zone="")

    def test_whitespace_zone_raises_value_error(self) -> None:
        """GIVEN whitespace zone WHEN construct THEN raises ValueError."""
        with pytest.raises(ValueError):
            SidecarComposeGenerator(zone="   ")


# =============================================================================
# AutoProvisionHandler Tests
# =============================================================================


def _make_auto_provision_handler(
    provision_nodes: list[ProxyNode] | None = None,
    ssh_ready: bool = True,
    healthy: bool = True,
) -> tuple[AutoProvisionHandler, MagicMock, MagicMock, MagicMock, MagicMock]:
    """Build AutoProvisionHandler with mocked ports."""
    node = provision_nodes[0] if provision_nodes else _make_node()
    provisioner = MagicMock()
    provisioner.provision.return_value = provision_nodes if provision_nodes is not None else [node]
    ssh_readiness = MagicMock()
    ssh_readiness.wait_for_ssh.return_value = ssh_ready
    health_checker = MagicMock()
    health_checker.check.return_value = healthy
    manifest_writer = MagicMock()

    handler = AutoProvisionHandler(
        provisioner=provisioner,
        ssh_readiness=ssh_readiness,
        health_checker=health_checker,
        manifest_writer=manifest_writer,
        ssh_timeout_seconds=30,
    )
    return handler, provisioner, ssh_readiness, health_checker, manifest_writer


class TestAutoProvisionHandlerSuccess:
    """Happy path tests for AutoProvisionHandler.handle()."""

    def test_handle_calls_provisioner(self) -> None:
        """GIVEN all ports succeed WHEN handle THEN provisioner.provision called."""
        node = _make_node()
        handler, provisioner, _, _, _ = _make_auto_provision_handler([node])
        config = MagicMock()
        handler.handle(config)
        provisioner.provision.assert_called_once_with(config)

    def test_handle_calls_ssh_readiness_with_node_ip(self) -> None:
        """GIVEN provisioner returns node WHEN handle THEN ssh_readiness.wait_for_ssh called."""
        node = _make_node(ip="10.0.0.5")
        handler, _, ssh_readiness, _, _ = _make_auto_provision_handler([node])
        handler.handle(MagicMock())
        ssh_readiness.wait_for_ssh.assert_called_once_with("10.0.0.5", 30)

    def test_handle_calls_health_checker(self) -> None:
        """GIVEN SSH ready WHEN handle THEN health_checker.check called."""
        node = _make_node()
        handler, _, _, health_checker, _ = _make_auto_provision_handler([node])
        handler.handle(MagicMock())
        health_checker.check.assert_called_once_with(node)

    def test_handle_calls_manifest_writer(self) -> None:
        """GIVEN all stages pass WHEN handle THEN manifest_writer.write called."""
        node = _make_node()
        handler, _, _, _, manifest_writer = _make_auto_provision_handler([node])
        handler.handle(MagicMock())
        manifest_writer.write.assert_called_once_with(node)

    def test_handle_returns_success_result(self) -> None:
        """GIVEN all stages pass WHEN handle THEN result.success is True."""
        node = _make_node()
        handler, _, _, _, _ = _make_auto_provision_handler([node])
        result = handler.handle(MagicMock())
        assert result.success is True
        assert result.node is node

    def test_handle_success_result_has_no_stage_failed(self) -> None:
        """GIVEN all stages pass WHEN handle THEN stage_failed is None."""
        node = _make_node()
        handler, _, _, _, _ = _make_auto_provision_handler([node])
        result = handler.handle(MagicMock())
        assert result.stage_failed is None


class TestAutoProvisionHandlerFailures:
    """Failure path tests for AutoProvisionHandler.handle()."""

    def test_handle_fails_when_provisioner_returns_empty_list(self) -> None:
        """GIVEN provisioner returns [] WHEN handle THEN result.stage_failed == 'provision'."""
        handler, _, _, _, _ = _make_auto_provision_handler(provision_nodes=[])
        result = handler.handle(MagicMock())
        assert result.success is False
        assert result.stage_failed == "provision"
        assert result.node is None

    def test_handle_fails_when_ssh_not_ready(self) -> None:
        """GIVEN SSH timeout WHEN handle THEN result.stage_failed == 'ssh_wait'."""
        node = _make_node()
        handler, _, _, _, manifest_writer = _make_auto_provision_handler(
            [node], ssh_ready=False
        )
        result = handler.handle(MagicMock())
        assert result.success is False
        assert result.stage_failed == "ssh_wait"
        manifest_writer.write.assert_not_called()

    def test_handle_fails_when_health_check_fails(self) -> None:
        """GIVEN health check fails WHEN handle THEN result.stage_failed == 'health'."""
        node = _make_node()
        handler, _, _, _, manifest_writer = _make_auto_provision_handler(
            [node], ssh_ready=True, healthy=False
        )
        result = handler.handle(MagicMock())
        assert result.success is False
        assert result.stage_failed == "health"
        manifest_writer.write.assert_not_called()

    def test_handle_ssh_failure_includes_ip_in_error(self) -> None:
        """GIVEN SSH timeout WHEN handle THEN error message contains node IP."""
        node = _make_node(ip="198.51.100.1")
        handler, _, _, _, _ = _make_auto_provision_handler([node], ssh_ready=False)
        result = handler.handle(MagicMock())
        assert "198.51.100.1" in result.error


# =============================================================================
# RotationHandler Tests
# =============================================================================


def _make_rotation_handler(
    replacement_node: ProxyNode | None = None,
    provision_success: bool = True,
    destroy_ok: bool = True,
) -> tuple[RotationHandler, MagicMock, MagicMock, MagicMock]:
    """Build RotationHandler with mocked dependencies."""
    if replacement_node is None:
        replacement_node = _make_node(node_id="node-new", ip="10.0.0.99")

    auto_provision = MagicMock()
    auto_provision.handle.return_value = ProvisionResult(
        success=provision_success,
        node=replacement_node if provision_success else None,
        stage_failed=None if provision_success else "provision",
        error=None if provision_success else "mock failure",
    )

    provisioner = MagicMock()
    provisioner.destroy.return_value = DestroyResult(
        destroyed=[replacement_node.id] if destroy_ok else [],
        failed=[] if destroy_ok else ["node-old"],
    )

    manifest_writer = MagicMock()

    handler = RotationHandler(
        auto_provisioner=auto_provision,
        provisioner=provisioner,
        manifest_writer=manifest_writer,
    )
    return handler, auto_provision, provisioner, manifest_writer


class TestRotationHandlerSuccess:
    """Happy path tests for RotationHandler.handle()."""

    def test_handle_calls_auto_provision(self) -> None:
        """GIVEN all succeeds WHEN handle THEN auto_provisioner.handle called."""
        handler, auto_provision, _, _ = _make_rotation_handler()
        burned = _make_node(node_id="node-burned")
        config = MagicMock()
        handler.handle(burned, config, trigger="RT-07")
        auto_provision.handle.assert_called_once_with(config)

    def test_handle_destroys_burned_node(self) -> None:
        """GIVEN replacement provisioned WHEN handle THEN provisioner.destroy called for burned."""
        handler, _, provisioner, _ = _make_rotation_handler()
        burned = _make_node(node_id="node-burned")
        handler.handle(burned, MagicMock(), trigger="RT-01")
        provisioner.destroy.assert_called_once_with(["node-burned"])

    def test_handle_returns_success_result(self) -> None:
        """GIVEN full rotation succeeds WHEN handle THEN result.success is True."""
        replacement = _make_node(node_id="node-new")
        handler, _, _, _ = _make_rotation_handler(replacement_node=replacement)
        burned = _make_node(node_id="node-burned")
        result = handler.handle(burned, MagicMock(), trigger="RT-07")
        assert result.success is True
        assert result.burned_node_id == "node-burned"
        assert result.replacement_node is replacement

    def test_handle_records_trigger_in_result(self) -> None:
        """GIVEN trigger RT-02 WHEN handle THEN result.trigger == RT-02."""
        handler, _, _, _ = _make_rotation_handler()
        burned = _make_node(node_id="node-old")
        result = handler.handle(burned, MagicMock(), trigger="RT-02")
        assert result.trigger == "RT-02"


class TestRotationHandlerFailures:
    """Failure path tests for RotationHandler.handle()."""

    def test_handle_fails_when_replacement_provision_fails(self) -> None:
        """GIVEN auto_provisioner fails WHEN handle THEN result.success is False."""
        handler, _, provisioner, _ = _make_rotation_handler(provision_success=False)
        burned = _make_node(node_id="node-burned")
        result = handler.handle(burned, MagicMock())
        assert result.success is False
        provisioner.destroy.assert_not_called()

    def test_handle_does_not_destroy_when_provision_fails(self) -> None:
        """GIVEN provision fails WHEN handle THEN burned node NOT destroyed (PI-003)."""
        handler, _, provisioner, _ = _make_rotation_handler(provision_success=False)
        burned = _make_node(node_id="node-burned")
        handler.handle(burned, MagicMock())
        provisioner.destroy.assert_not_called()

    def test_handle_continues_when_destroy_fails(self) -> None:
        """GIVEN destroy fails WHEN handle THEN overall result is still success (logged warning)."""
        handler, _, _, _ = _make_rotation_handler(destroy_ok=False)
        burned = _make_node(node_id="node-burned")
        result = handler.handle(burned, MagicMock(), trigger="RT-01")
        # Rotation is considered complete even if destroy has issues
        assert result.success is True


# =============================================================================
# SecretsDistributionHandler Tests
# =============================================================================


class TestSecretsDistributionHandler:
    """Tests for SecretsDistributionHandler."""

    @pytest.fixture()
    def tmp_dir(self, tmp_path: Path) -> Path:
        """Temporary directory simulating the engagement credential dir."""
        return tmp_path

    @pytest.fixture()
    def handler(self, tmp_dir: Path) -> SecretsDistributionHandler:
        """SecretsDistributionHandler with a temporary generated_dir."""
        return SecretsDistributionHandler(generated_dir=tmp_dir)

    def test_init_raises_when_dir_does_not_exist(self, tmp_path: Path) -> None:
        """GIVEN nonexistent dir WHEN construct THEN raises NotADirectoryError."""
        nonexistent = tmp_path / "does_not_exist"
        with pytest.raises(NotADirectoryError):
            SecretsDistributionHandler(generated_dir=nonexistent)

    def test_distribute_ssh_key_writes_file_with_0600(
        self, handler: SecretsDistributionHandler, tmp_dir: Path
    ) -> None:
        """GIVEN valid pem WHEN distribute_ssh_key THEN file written with 0600."""
        result = handler.distribute_ssh_key("--- FAKE PEM ---", node_role="recon")
        assert result.success is True
        secret_file = tmp_dir / "eng_ssh_key_recon"
        assert secret_file.exists()
        assert oct(secret_file.stat().st_mode)[-3:] == "600"

    def test_distribute_ssh_key_content_matches(
        self, handler: SecretsDistributionHandler, tmp_dir: Path
    ) -> None:
        """GIVEN pem content WHEN distribute_ssh_key THEN file contains exact pem."""
        pem = "--- FAKE ED25519 KEY ---"
        handler.distribute_ssh_key(pem, node_role="recon")
        content = (tmp_dir / "eng_ssh_key_recon").read_text()
        assert content == pem

    def test_distribute_ssh_key_empty_pem_returns_failure(
        self, handler: SecretsDistributionHandler
    ) -> None:
        """GIVEN empty pem WHEN distribute_ssh_key THEN result.success is False."""
        result = handler.distribute_ssh_key("", node_role="recon")
        assert result.success is False

    def test_distribute_ssh_key_empty_role_returns_failure(
        self, handler: SecretsDistributionHandler
    ) -> None:
        """GIVEN empty role WHEN distribute_ssh_key THEN result.success is False."""
        result = handler.distribute_ssh_key("--- FAKE PEM ---", node_role="")
        assert result.success is False

    def test_distribute_socks5_credentials_writes_file(
        self, handler: SecretsDistributionHandler, tmp_dir: Path
    ) -> None:
        """GIVEN valid creds WHEN distribute_socks5_credentials THEN file written."""
        node = _make_node(node_id="node-001")
        result = handler.distribute_socks5_credentials(node, "jerry-abc", "p4ssword!")
        assert result.success is True
        creds_file = tmp_dir / "socks5_creds_node-001"
        assert creds_file.exists()

    def test_distribute_socks5_credentials_content_format(
        self, handler: SecretsDistributionHandler, tmp_dir: Path
    ) -> None:
        """GIVEN creds WHEN distribute_socks5_credentials THEN content is user:pass."""
        node = _make_node(node_id="node-002")
        handler.distribute_socks5_credentials(node, "jerry-x1y2", "s3cr3t!")
        content = (tmp_dir / "socks5_creds_node-002").read_text()
        assert content == "jerry-x1y2:s3cr3t!"

    def test_distribute_socks5_empty_username_returns_failure(
        self, handler: SecretsDistributionHandler
    ) -> None:
        """GIVEN empty username WHEN distribute_socks5_credentials THEN failure."""
        node = _make_node()
        result = handler.distribute_socks5_credentials(node, "", "pass")
        assert result.success is False

    def test_distribute_pool_manifest_writes_file(
        self, handler: SecretsDistributionHandler, tmp_dir: Path
    ) -> None:
        """GIVEN manifest json WHEN distribute_pool_manifest THEN file written."""
        manifest = '{"nodes": []}'
        result = handler.distribute_pool_manifest(manifest)
        assert result.success is True
        assert (tmp_dir / "pool_manifest").exists()

    def test_distribute_pool_manifest_empty_returns_failure(
        self, handler: SecretsDistributionHandler
    ) -> None:
        """GIVEN empty manifest WHEN distribute_pool_manifest THEN failure."""
        result = handler.distribute_pool_manifest("")
        assert result.success is False

    def test_shred_all_returns_count_of_shredded_files(
        self, handler: SecretsDistributionHandler
    ) -> None:
        """GIVEN 2 files written WHEN shred_all THEN returns count >= 2."""
        node = _make_node()
        handler.distribute_ssh_key("--- KEY ---", node_role="recon")
        handler.distribute_socks5_credentials(node, "jerry-ab", "pass123")
        count = handler.shred_all()
        assert count >= 2

    def test_shred_all_clears_written_list(
        self, handler: SecretsDistributionHandler
    ) -> None:
        """GIVEN files written WHEN shred_all THEN written_count drops to 0."""
        handler.distribute_ssh_key("--- KEY ---", node_role="recon")
        handler.shred_all()
        assert handler.written_count() == 0

    def test_written_count_tracks_each_write(
        self, handler: SecretsDistributionHandler
    ) -> None:
        """GIVEN multiple writes WHEN written_count THEN matches number of successful writes."""
        node = _make_node()
        handler.distribute_ssh_key("--- KEY ---", node_role="recon")
        handler.distribute_socks5_credentials(node, "jerry-cd", "pw456")
        assert handler.written_count() == 2
