# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""System tests: engage pipeline with TerraformProvisionerAdapter.

Tests the full engage_command → TerraformProvisionerAdapter →
EngagePipelineOrchestrator composition with real code wiring but
mocked subprocess calls. This validates that the Terraform adapter
integrates correctly with the existing pipeline.

Test pyramid level: System (component interaction).
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from unittest.mock import MagicMock, patch

from src.proxy_infra.domain.value_objects.proxy_role import ProxyRole
from src.proxy_infra.domain.value_objects.proxy_type import ProxyType


def _terraform_output_json() -> str:
    """Return a mock terraform output -json payload."""
    return json.dumps(
        {
            "droplet_ip": {"value": "104.131.99.99", "type": "string"},
            "droplet_id": {"value": "999888777", "type": "string"},
            "ssh_key_id": {"value": "55555", "type": "string"},
            "firewall_id": {"value": "fw-system-test", "type": "string"},
        }
    )


class TestEngagePipelineWithTerraformOrchestrator:
    """System test: EngagePipelineOrchestrator composes with TerraformProvisionerAdapter."""

    @patch("subprocess.run")
    def test_orchestrator_full_pipeline_with_terraform_adapter(
        self, mock_run: MagicMock, tmp_path: Path
    ) -> None:
        """Full pipeline: provision → SSH wait → inject → health → compose."""
        from src.proxy_infra.application.handlers.engage_pipeline_orchestrator import (
            EngagePipelineOrchestrator,
        )
        from src.proxy_infra.domain.value_objects.provision_config import ProvisionConfig
        from src.proxy_infra.infrastructure.adapters.terraform_provisioner_adapter import (
            TerraformProvisionerAdapter,
        )

        # Mock terraform calls
        mock_run.side_effect = [
            subprocess.CompletedProcess(["terraform", "init"], 0, "", ""),
            subprocess.CompletedProcess(["terraform", "apply"], 0, "", ""),
            subprocess.CompletedProcess(["terraform", "output"], 0, _terraform_output_json(), ""),
        ]

        adapter = TerraformProvisionerAdapter(engagement_dir=tmp_path)

        # Mock pipeline ports
        mock_ssh = MagicMock()
        mock_ssh.wait_for_ssh.return_value = True

        mock_injector = MagicMock()
        mock_injector.inject.return_value = MagicMock(
            success=True, username="proxyuser", password="proxypass"
        )

        mock_health = MagicMock()
        mock_health.check.return_value = True

        mock_manifest = MagicMock()
        mock_bpf = MagicMock()

        orchestrator = EngagePipelineOrchestrator(
            provisioner=adapter,
            ssh_readiness=mock_ssh,
            credential_injector=mock_injector,
            health_checker=mock_health,
            manifest_writer=mock_manifest,
            bpf_port=mock_bpf,
            engagement_dir=tmp_path,
        )

        config = ProvisionConfig(
            provider="digitalocean",
            region="nyc3",
            engagement_id="RED-SYS-001",
            engagement_tag="jerry-red-sys-001",
            count=1,
            role=ProxyRole.ACTIVE,
            proxy_type=ProxyType.DIRECT_SOCKS5,
            ssh_public_key="ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIFake test",
            operator_ip="198.51.100.1",
        )

        result = orchestrator.orchestrate(
            config=config,
            private_key_path=tmp_path / "id_ed25519",
        )

        assert result.success is True
        assert result.nodes is not None
        assert len(result.nodes) == 1
        assert result.nodes[0].ip == "104.131.99.99"
        assert result.compose_path is not None

        # Verify all pipeline stages fired
        mock_ssh.wait_for_ssh.assert_called_once()
        mock_injector.inject.assert_called_once()
        mock_health.check.assert_called_once()
        mock_manifest.write.assert_called_once()
        mock_bpf.update_bypass_ips.assert_called_once_with(["104.131.99.99"])

        # Verify Docker Compose generated
        compose = Path(result.compose_path)
        assert compose.exists()
        compose_content = compose.read_text()
        assert "104.131.99.99" in compose_content
        assert "socks-bridge" in compose_content

    @patch("subprocess.run")
    def test_orchestrator_skips_node_when_ssh_timeout(
        self, mock_run: MagicMock, tmp_path: Path
    ) -> None:
        """Node skipped when SSH readiness times out — pipeline returns failure."""
        from src.proxy_infra.application.handlers.engage_pipeline_orchestrator import (
            EngagePipelineOrchestrator,
        )
        from src.proxy_infra.domain.value_objects.provision_config import ProvisionConfig
        from src.proxy_infra.infrastructure.adapters.terraform_provisioner_adapter import (
            TerraformProvisionerAdapter,
        )

        mock_run.side_effect = [
            subprocess.CompletedProcess(["terraform", "init"], 0, "", ""),
            subprocess.CompletedProcess(["terraform", "apply"], 0, "", ""),
            subprocess.CompletedProcess(["terraform", "output"], 0, _terraform_output_json(), ""),
        ]

        adapter = TerraformProvisionerAdapter(engagement_dir=tmp_path)

        mock_ssh = MagicMock()
        mock_ssh.wait_for_ssh.return_value = False  # SSH timeout

        orchestrator = EngagePipelineOrchestrator(
            provisioner=adapter,
            ssh_readiness=mock_ssh,
            credential_injector=MagicMock(),
            health_checker=MagicMock(),
            manifest_writer=MagicMock(),
            bpf_port=MagicMock(),
            engagement_dir=tmp_path,
        )

        config = ProvisionConfig(
            provider="digitalocean",
            region="nyc3",
            engagement_id="RED-SYS-002",
            engagement_tag="jerry-red-sys-002",
            count=1,
            role=ProxyRole.ACTIVE,
            proxy_type=ProxyType.DIRECT_SOCKS5,
            ssh_public_key="ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIFake test",
            operator_ip="198.51.100.1",
        )

        result = orchestrator.orchestrate(
            config=config,
            private_key_path=tmp_path / "id_ed25519",
        )

        assert result.success is False
        assert "No nodes successfully injected" in result.error

    @patch("subprocess.run")
    def test_adapter_factory_routes_to_terraform_in_pipeline(
        self, mock_run: MagicMock, tmp_path: Path, monkeypatch: MagicMock
    ) -> None:
        """Factory creates TerraformProvisionerAdapter which integrates with orchestrator."""
        from src.proxy_infra.infrastructure.adapters.provisioner_adapter_factory import (
            create_provisioner_adapter,
        )
        from src.proxy_infra.infrastructure.adapters.terraform_provisioner_adapter import (
            TerraformProvisionerAdapter,
        )

        monkeypatch.delenv("JERRY_PROVISIONER_BACKEND", raising=False)

        adapter = create_provisioner_adapter(
            provider="digitalocean",
            engagement_dir=tmp_path,
        )

        assert isinstance(adapter, TerraformProvisionerAdapter)

        # Verify it can be used in the orchestrator constructor
        from src.proxy_infra.application.handlers.engage_pipeline_orchestrator import (
            EngagePipelineOrchestrator,
        )

        orchestrator = EngagePipelineOrchestrator(
            provisioner=adapter,
            ssh_readiness=MagicMock(),
            credential_injector=MagicMock(),
            health_checker=MagicMock(),
            manifest_writer=MagicMock(),
            bpf_port=MagicMock(),
            engagement_dir=tmp_path,
        )

        assert orchestrator is not None
