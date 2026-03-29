# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Integration tests for TerraformProvisionerAdapter — full stack mocked.

Tests exercise the complete provision/destroy flow with subprocess mocked,
verifying that HCL generation, terraform calls, and state parsing integrate
correctly as a stack.

These complement the unit tests in TASK-023-100 by testing the real
composition rather than individual mocks.

References:
    - TASK-023-105: Test migration (pydo -> subprocess mocks)
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest


def _terraform_output_json() -> str:
    """Return a realistic terraform output -json payload."""
    return json.dumps(
        {
            "droplet_ip": {"value": "104.131.1.1", "type": "string"},
            "droplet_id": {"value": "561544479", "type": "string"},
            "ssh_key_id": {"value": "42424242", "type": "string"},
            "firewall_id": {"value": "fw-abcdef12", "type": "string"},
        }
    )


def _ok_result(args: list[str], stdout: str = "") -> subprocess.CompletedProcess[str]:
    """Create a successful CompletedProcess."""
    return subprocess.CompletedProcess(args=args, returncode=0, stdout=stdout, stderr="")


class TestTerraformAdapterProvisionIntegration:
    """Integration tests for the full provision() flow."""

    @patch("subprocess.run")
    def test_provision_end_to_end_mocked(self, mock_run: MagicMock, tmp_path: Path) -> None:
        """Full provision() call with subprocess mocked: HCL written, calls made, ProxyNode returned."""
        from src.proxy_infra.infrastructure.adapters.terraform_provisioner_adapter import (
            TerraformProvisionerAdapter,
        )

        mock_run.side_effect = [
            _ok_result(["terraform", "init"]),
            _ok_result(["terraform", "apply", "-auto-approve"]),
            _ok_result(
                ["terraform", "output", "-json"],
                stdout=_terraform_output_json(),
            ),
        ]

        adapter = TerraformProvisionerAdapter(engagement_dir=tmp_path)

        config = {
            "engagement_id": "RED-TEST-001",
            "region": "nyc3",
            "size": "s-1vcpu-1gb",
            "image": "ubuntu-24-04-x64",
            "ssh_public_key": "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAA test@poc",
            "operator_ip": "198.51.100.1",
            "socks_port": 1080,
        }

        nodes = adapter.provision(config)

        assert len(nodes) == 1
        assert nodes[0].ip == "104.131.1.1"
        assert nodes[0].id == "561544479"
        assert nodes[0].provider == "digitalocean"
        assert nodes[0].region == "nyc3"
        assert nodes[0].engagement_id == "RED-TEST-001"

        # Verify HCL file was generated
        main_tf = tmp_path / "terraform" / "main.tf"
        assert main_tf.exists()
        hcl_content = main_tf.read_text()
        assert "digitalocean_droplet" in hcl_content
        assert "RED-TEST-001" in hcl_content

        # Verify subprocess calls made in correct order
        assert mock_run.call_count == 3
        calls = mock_run.call_args_list
        assert calls[0][0][0] == ["terraform", "init"]
        assert calls[1][0][0] == ["terraform", "apply", "-auto-approve"]
        assert calls[2][0][0] == ["terraform", "output", "-json"]

    @patch("subprocess.run")
    def test_provision_raises_on_apply_failure(self, mock_run: MagicMock, tmp_path: Path) -> None:
        """Non-zero exit from terraform apply must raise ProvisionError."""
        from src.proxy_infra.domain.exceptions.provision_error import ProvisionError
        from src.proxy_infra.infrastructure.adapters.terraform_provisioner_adapter import (
            TerraformProvisionerAdapter,
        )

        mock_run.side_effect = [
            _ok_result(["terraform", "init"]),
            subprocess.CompletedProcess(
                args=["terraform", "apply"],
                returncode=1,
                stdout="",
                stderr="Error: creating digitalocean_droplet: 422 Unprocessable Entity",
            ),
        ]

        adapter = TerraformProvisionerAdapter(engagement_dir=tmp_path)

        with pytest.raises(ProvisionError):
            adapter.provision(
                {
                    "engagement_id": "RED-TEST-001",
                    "region": "nyc3",
                    "size": "s-1vcpu-1gb",
                    "image": "ubuntu-24-04-x64",
                    "ssh_public_key": "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAA test@poc",
                    "operator_ip": "198.51.100.1",
                    "socks_port": 1080,
                }
            )


class TestTerraformAdapterDestroyIntegration:
    """Integration tests for the full destroy() flow."""

    @patch("subprocess.run")
    def test_destroy_end_to_end_mocked(self, mock_run: MagicMock, tmp_path: Path) -> None:
        """Full destroy() call with subprocess mocked."""
        from src.proxy_infra.infrastructure.adapters.terraform_provisioner_adapter import (
            TerraformProvisionerAdapter,
        )

        mock_run.return_value = _ok_result(["terraform", "destroy", "-auto-approve"])

        work_dir = tmp_path / "terraform"
        work_dir.mkdir(parents=True)

        adapter = TerraformProvisionerAdapter(engagement_dir=tmp_path)

        result = adapter.destroy(node_ids=["561544479"], engagement_id="RED-TEST-001")

        assert result.is_all_successful
        assert "561544479" in result.destroyed
        assert result.failed == []

    @patch("subprocess.run")
    def test_destroy_captures_failure_in_result(self, mock_run: MagicMock, tmp_path: Path) -> None:
        """Failed terraform destroy captures node IDs in failed list."""
        from src.proxy_infra.infrastructure.adapters.terraform_provisioner_adapter import (
            TerraformProvisionerAdapter,
        )

        mock_run.return_value = subprocess.CompletedProcess(
            args=["terraform", "destroy"],
            returncode=1,
            stdout="",
            stderr="Error: resource still in use",
        )

        adapter = TerraformProvisionerAdapter(engagement_dir=tmp_path)

        result = adapter.destroy(node_ids=["561544479"], engagement_id="RED-TEST-001")

        assert not result.is_all_successful
        assert "561544479" in result.failed


class TestAdapterFactoryIntegration:
    """Integration tests for adapter factory routing."""

    def test_factory_returns_terraform_adapter_by_default(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Factory default for digitalocean is TerraformProvisionerAdapter."""
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
