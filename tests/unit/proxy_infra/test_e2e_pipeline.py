# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""BDD test suite for end-to-end pipeline orchestration.

STORY-023-009: End-to-End Pipeline Orchestration & Verification
Tasks covered:
  - TASK-023-057: BDD tests for E2E pipeline orchestration (RED)
  - TASK-023-058: Extend AutoProvisionHandler with credential injection stage
  - TASK-023-059: Pool manifest → BPF bypass map + Docker Compose generation
  - TASK-023-060: E2E integration test

Covers:
  - AutoProvisionHandler 5-stage pipeline (provision → ssh → inject → health → manifest)
  - Backward compatibility (injection port optional)
  - EngagePipelineOrchestrator: full engage_command → inject → BPF → compose chain
  - Docker Compose sidecar generation from pool manifest
  - E2E chain: config → provision → inject → compose output

Test pyramid: 60% happy path / 30% negative / 10% edge cases
Naming convention: test_{scenario}_when_{condition}_then_{expected}
"""

from __future__ import annotations

import os
import stat
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import MagicMock, patch, PropertyMock

import pytest
import yaml

from src.proxy_infra.application.handlers.auto_provision_handler import AutoProvisionHandler
from src.proxy_infra.application.handlers.provision_result import ProvisionResult
from src.proxy_infra.domain.value_objects.node_status import NodeStatus
from src.proxy_infra.domain.value_objects.proxy_node import ProxyNode
from src.proxy_infra.domain.value_objects.proxy_role import ProxyRole
from src.proxy_infra.domain.value_objects.proxy_type import ProxyType
from src.proxy_infra.domain.value_objects.provision_config import ProvisionConfig


# =============================================================================
# Shared fixtures
# =============================================================================


def _make_config() -> ProvisionConfig:
    """Create a test ProvisionConfig."""
    return ProvisionConfig(
        provider="digitalocean",
        region="nyc1",
        engagement_id="ENG-001",
        engagement_tag="jerry-eng-001",
        count=1,
        role=ProxyRole.ACTIVE,
        proxy_type=ProxyType.DIRECT_SOCKS5,
        ssh_public_key="ssh-ed25519 AAAA... test@jerry",
        operator_ip="174.7.155.69",
        socks_port=1080,
    )


def _make_node(
    node_id: str = "do-12345",
    ip: str = "159.203.44.10",
) -> ProxyNode:
    """Create a test ProxyNode."""
    return ProxyNode(
        id=node_id,
        provider="digitalocean",
        ip=ip,
        region="nyc1",
        role=ProxyRole.ACTIVE,
        proxy_type=ProxyType.DIRECT_SOCKS5,
        status=NodeStatus.CONFIGURING,
        ssh_key_id="key-123",
        created_at=datetime.now(timezone.utc),
        engagement_id="ENG-001",
        socks_port=1080,
    )


# =============================================================================
# AutoProvisionHandler with injection stage (TASK-023-058)
# =============================================================================


class TestAutoProvisionHandlerInjectionStage:
    """Tests for extending AutoProvisionHandler with credential injection."""

    def test_handle_when_injection_port_provided_then_5_stages_execute(self) -> None:
        """Full 5-stage pipeline: provision → ssh → inject → health → manifest."""
        provisioner = MagicMock()
        node = _make_node()
        provisioner.provision.return_value = [node]

        ssh_readiness = MagicMock()
        ssh_readiness.wait_for_ssh.return_value = True

        injection_handler = MagicMock()
        injection_result = MagicMock(success=True, username="u", password="p")
        injection_handler.inject.return_value = injection_result

        health_checker = MagicMock()
        health_checker.check.return_value = True

        manifest_writer = MagicMock()

        handler = AutoProvisionHandler(
            provisioner=provisioner,
            ssh_readiness=ssh_readiness,
            health_checker=health_checker,
            manifest_writer=manifest_writer,
            credential_injector=injection_handler,
        )

        result = handler.handle(_make_config())
        assert result.success is True
        injection_handler.inject.assert_called_once()

    def test_handle_when_no_injection_port_then_backward_compatible_4_stages(self) -> None:
        """Without injection port, original 4-stage pipeline runs (backward compat)."""
        provisioner = MagicMock()
        node = _make_node()
        provisioner.provision.return_value = [node]

        ssh_readiness = MagicMock()
        ssh_readiness.wait_for_ssh.return_value = True

        health_checker = MagicMock()
        health_checker.check.return_value = True

        manifest_writer = MagicMock()

        handler = AutoProvisionHandler(
            provisioner=provisioner,
            ssh_readiness=ssh_readiness,
            health_checker=health_checker,
            manifest_writer=manifest_writer,
        )

        result = handler.handle(_make_config())
        assert result.success is True

    def test_handle_when_injection_fails_then_returns_failure_at_inject_stage(self) -> None:
        """Injection failure should halt pipeline before health check."""
        provisioner = MagicMock()
        node = _make_node()
        provisioner.provision.return_value = [node]

        ssh_readiness = MagicMock()
        ssh_readiness.wait_for_ssh.return_value = True

        injection_handler = MagicMock()
        injection_handler.inject.return_value = MagicMock(
            success=False, stage_failed="credential_generation"
        )

        health_checker = MagicMock()
        manifest_writer = MagicMock()

        handler = AutoProvisionHandler(
            provisioner=provisioner,
            ssh_readiness=ssh_readiness,
            health_checker=health_checker,
            manifest_writer=manifest_writer,
            credential_injector=injection_handler,
        )

        result = handler.handle(_make_config())
        assert result.success is False
        assert result.stage_failed == "credential_inject"
        health_checker.check.assert_not_called()

    def test_handle_when_injection_port_then_inject_called_after_ssh_wait(self) -> None:
        """Injection must happen AFTER SSH wait, BEFORE health check."""
        call_order = []

        provisioner = MagicMock()
        provisioner.provision.return_value = [_make_node()]

        ssh_readiness = MagicMock()
        ssh_readiness.wait_for_ssh.side_effect = lambda *a, **k: (call_order.append("ssh"), True)[1]

        injection_handler = MagicMock()
        injection_handler.inject.side_effect = lambda *a, **k: (
            call_order.append("inject"),
            MagicMock(success=True),
        )[1]

        health_checker = MagicMock()
        health_checker.check.side_effect = lambda *a, **k: (call_order.append("health"), True)[1]

        manifest_writer = MagicMock()

        handler = AutoProvisionHandler(
            provisioner=provisioner,
            ssh_readiness=ssh_readiness,
            health_checker=health_checker,
            manifest_writer=manifest_writer,
            credential_injector=injection_handler,
        )
        handler.handle(_make_config())

        assert call_order == ["ssh", "inject", "health"]


# =============================================================================
# EngagePipelineOrchestrator tests (TASK-023-059 / TASK-023-060)
# =============================================================================


class TestEngagePipelineOrchestrator:
    """Tests for the full engage pipeline: config → provision → inject → BPF → compose."""

    def test_orchestrate_when_valid_config_then_produces_compose_file(
        self, tmp_path: Path,
    ) -> None:
        """Full pipeline produces a Docker Compose sidecar file."""
        from src.proxy_infra.application.handlers.engage_pipeline_orchestrator import (
            EngagePipelineOrchestrator,
        )

        provisioner = MagicMock()
        nodes = [_make_node("n1", "1.2.3.4"), _make_node("n2", "5.6.7.8")]
        provisioner.provision.return_value = nodes

        ssh_readiness = MagicMock()
        ssh_readiness.wait_for_ssh.return_value = True

        injection_handler = MagicMock()
        injection_handler.inject.return_value = MagicMock(
            success=True, username="u", password="p"
        )

        health_checker = MagicMock()
        health_checker.check.return_value = True

        manifest_writer = MagicMock()
        bpf_port = MagicMock()

        orchestrator = EngagePipelineOrchestrator(
            provisioner=provisioner,
            ssh_readiness=ssh_readiness,
            credential_injector=injection_handler,
            health_checker=health_checker,
            manifest_writer=manifest_writer,
            bpf_port=bpf_port,
            engagement_dir=tmp_path,
        )

        config = _make_config()
        result = orchestrator.orchestrate(config, private_key_path=Path("/tmp/key"))

        assert result.success is True
        compose_file = tmp_path / "docker-compose.socks.yaml"
        assert compose_file.exists()

    def test_orchestrate_when_valid_then_bpf_bypass_updated_with_node_ips(
        self, tmp_path: Path,
    ) -> None:
        """BPF bypass map should contain all proxy node IPs."""
        from src.proxy_infra.application.handlers.engage_pipeline_orchestrator import (
            EngagePipelineOrchestrator,
        )

        provisioner = MagicMock()
        nodes = [_make_node("n1", "1.2.3.4"), _make_node("n2", "5.6.7.8")]
        provisioner.provision.return_value = nodes

        ssh_readiness = MagicMock()
        ssh_readiness.wait_for_ssh.return_value = True

        injection_handler = MagicMock()
        injection_handler.inject.return_value = MagicMock(
            success=True, username="u", password="p"
        )

        health_checker = MagicMock()
        health_checker.check.return_value = True

        bpf_port = MagicMock()
        manifest_writer = MagicMock()

        orchestrator = EngagePipelineOrchestrator(
            provisioner=provisioner,
            ssh_readiness=ssh_readiness,
            credential_injector=injection_handler,
            health_checker=health_checker,
            manifest_writer=manifest_writer,
            bpf_port=bpf_port,
            engagement_dir=tmp_path,
        )

        orchestrator.orchestrate(_make_config(), private_key_path=Path("/tmp/key"))

        bpf_port.update_bypass_ips.assert_called_once()
        bypass_ips = bpf_port.update_bypass_ips.call_args[0][0]
        assert "1.2.3.4" in bypass_ips
        assert "5.6.7.8" in bypass_ips

    def test_orchestrate_when_provision_fails_then_no_compose_generated(
        self, tmp_path: Path,
    ) -> None:
        """Failed provisioning should not produce a compose file."""
        from src.proxy_infra.application.handlers.engage_pipeline_orchestrator import (
            EngagePipelineOrchestrator,
        )

        provisioner = MagicMock()
        provisioner.provision.return_value = []

        orchestrator = EngagePipelineOrchestrator(
            provisioner=provisioner,
            ssh_readiness=MagicMock(),
            credential_injector=MagicMock(),
            health_checker=MagicMock(),
            manifest_writer=MagicMock(),
            bpf_port=MagicMock(),
            engagement_dir=tmp_path,
        )

        result = orchestrator.orchestrate(_make_config(), private_key_path=Path("/tmp/key"))
        assert result.success is False
        assert not (tmp_path / "docker-compose.socks.yaml").exists()

    def test_orchestrate_writes_credential_return_files(
        self, tmp_path: Path,
    ) -> None:
        """Credential return files should be written for each injected node."""
        from src.proxy_infra.application.handlers.engage_pipeline_orchestrator import (
            EngagePipelineOrchestrator,
        )

        provisioner = MagicMock()
        nodes = [_make_node("n1", "1.2.3.4")]
        provisioner.provision.return_value = nodes

        ssh_readiness = MagicMock()
        ssh_readiness.wait_for_ssh.return_value = True

        injection_handler = MagicMock()
        injection_handler.inject.return_value = MagicMock(
            success=True, username="jerry-aaa", password="secretpass"
        )

        health_checker = MagicMock()
        health_checker.check.return_value = True

        orchestrator = EngagePipelineOrchestrator(
            provisioner=provisioner,
            ssh_readiness=ssh_readiness,
            credential_injector=injection_handler,
            health_checker=health_checker,
            manifest_writer=MagicMock(),
            bpf_port=MagicMock(),
            engagement_dir=tmp_path,
        )

        orchestrator.orchestrate(_make_config(), private_key_path=Path("/tmp/key"))

        cred_file = tmp_path / "credentials" / "socks5_creds_n1"
        assert cred_file.exists()
        assert cred_file.read_text() == "jerry-aaa:secretpass"

    def test_orchestrate_compose_contains_socks_proxy_host(
        self, tmp_path: Path,
    ) -> None:
        """Generated compose file should reference proxy node addresses."""
        from src.proxy_infra.application.handlers.engage_pipeline_orchestrator import (
            EngagePipelineOrchestrator,
        )

        provisioner = MagicMock()
        nodes = [_make_node("n1", "1.2.3.4")]
        provisioner.provision.return_value = nodes

        ssh_readiness = MagicMock()
        ssh_readiness.wait_for_ssh.return_value = True

        injection_handler = MagicMock()
        injection_handler.inject.return_value = MagicMock(
            success=True, username="u", password="p"
        )

        health_checker = MagicMock()
        health_checker.check.return_value = True

        orchestrator = EngagePipelineOrchestrator(
            provisioner=provisioner,
            ssh_readiness=ssh_readiness,
            credential_injector=injection_handler,
            health_checker=health_checker,
            manifest_writer=MagicMock(),
            bpf_port=MagicMock(),
            engagement_dir=tmp_path,
        )

        orchestrator.orchestrate(_make_config(), private_key_path=Path("/tmp/key"))

        compose_content = (tmp_path / "docker-compose.socks.yaml").read_text()
        assert "1.2.3.4" in compose_content
