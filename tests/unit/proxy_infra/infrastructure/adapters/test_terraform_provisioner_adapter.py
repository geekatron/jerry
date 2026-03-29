# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""RED phase tests for TASK-023-100: TerraformProvisionerAdapter Core.

Tests verify:
1. Adapter construction requires engagement_dir
2. provision() orchestrates HCL gen -> init -> apply -> output -> ProxyNode list
3. destroy() orchestrates terraform destroy -> cleanup
4. Error handling on non-zero terraform exit codes
5. No shell=True anywhere in subprocess calls

All tests MUST FAIL before implementation (H-20 RED phase).
"""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock

import pytest


def _mock_terraform_output() -> dict:
    """Return a mock terraform output -json response."""
    return {
        "droplet_ip": {"value": "104.131.1.1", "type": "string"},
        "droplet_id": {"value": "123456", "type": "string"},
        "ssh_key_id": {"value": "42424242", "type": "string"},
        "firewall_id": {"value": "fw-abcdef", "type": "string"},
    }


def _valid_config() -> dict:
    """Return a valid engagement config dict."""
    return {
        "engagement_id": "RED-TEST-001",
        "region": "nyc3",
        "size": "s-1vcpu-1gb",
        "image": "ubuntu-24-04-x64",
        "ssh_public_key": "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAA test@poc",
        "operator_ip": "198.51.100.1",
        "socks_port": 1080,
    }


class TestTerraformProvisionerAdapterConstruction:
    """Tests for adapter construction."""

    def test_adapter_construction_requires_engagement_dir(self) -> None:
        """Adapter must raise if engagement_dir is not a valid directory."""
        from src.proxy_infra.infrastructure.adapters.terraform_provisioner_adapter import (
            TerraformProvisionerAdapter,
        )

        with pytest.raises((ValueError, TypeError)):
            TerraformProvisionerAdapter(engagement_dir=None)  # type: ignore[arg-type]


class TestTerraformProvisionerAdapterProvision:
    """Tests for provision() method."""

    def test_provision_calls_generate_hcl(self, tmp_path: Path) -> None:
        """provision() must call HclGenerator.generate() with engagement config."""
        from src.proxy_infra.infrastructure.adapters.terraform_provisioner_adapter import (
            TerraformProvisionerAdapter,
        )

        mock_hcl = MagicMock()
        mock_hcl.generate.return_value = tmp_path / "main.tf"
        (tmp_path / "main.tf").write_text("# mock")

        mock_runner = MagicMock()
        mock_runner.output.return_value = _mock_terraform_output()

        adapter = TerraformProvisionerAdapter(
            engagement_dir=tmp_path,
            hcl_generator=mock_hcl,
            terraform_runner=mock_runner,
            state_parser=MagicMock(),
        )

        adapter.provision(_valid_config())

        mock_hcl.generate.assert_called_once()

    def test_provision_calls_terraform_init(self, tmp_path: Path) -> None:
        """provision() must call terraform init."""
        from src.proxy_infra.infrastructure.adapters.terraform_provisioner_adapter import (
            TerraformProvisionerAdapter,
        )

        mock_runner = MagicMock()
        mock_runner.output.return_value = _mock_terraform_output()

        mock_parser = MagicMock()
        mock_parser.parse_output.return_value = {
            "droplet_ip": "104.131.1.1",
            "droplet_id": "123456",
            "ssh_key_id": "42424242",
            "firewall_id": "fw-abcdef",
        }

        adapter = TerraformProvisionerAdapter(
            engagement_dir=tmp_path,
            hcl_generator=MagicMock(generate=MagicMock(return_value=tmp_path / "main.tf")),
            terraform_runner=mock_runner,
            state_parser=mock_parser,
        )

        adapter.provision(_valid_config())

        mock_runner.init.assert_called_once()

    def test_provision_calls_terraform_apply_with_auto_approve(self, tmp_path: Path) -> None:
        """provision() must call terraform apply (auto-approve via runner)."""
        from src.proxy_infra.infrastructure.adapters.terraform_provisioner_adapter import (
            TerraformProvisionerAdapter,
        )

        mock_runner = MagicMock()
        mock_runner.output.return_value = _mock_terraform_output()

        adapter = TerraformProvisionerAdapter(
            engagement_dir=tmp_path,
            hcl_generator=MagicMock(generate=MagicMock(return_value=tmp_path / "main.tf")),
            terraform_runner=mock_runner,
            state_parser=MagicMock(),
        )

        adapter.provision(_valid_config())

        mock_runner.apply.assert_called_once()

    def test_provision_calls_terraform_output_json(self, tmp_path: Path) -> None:
        """provision() must call terraform output -json after apply."""
        from src.proxy_infra.infrastructure.adapters.terraform_provisioner_adapter import (
            TerraformProvisionerAdapter,
        )

        mock_runner = MagicMock()
        mock_runner.output.return_value = _mock_terraform_output()

        adapter = TerraformProvisionerAdapter(
            engagement_dir=tmp_path,
            hcl_generator=MagicMock(generate=MagicMock(return_value=tmp_path / "main.tf")),
            terraform_runner=mock_runner,
            state_parser=MagicMock(),
        )

        adapter.provision(_valid_config())

        mock_runner.output.assert_called_once()

    def test_provision_returns_proxy_node_list(self, tmp_path: Path) -> None:
        """provision() must return list[ProxyNode] from parsed terraform output."""
        from src.proxy_infra.domain.value_objects.proxy_node import ProxyNode
        from src.proxy_infra.infrastructure.adapters.terraform_provisioner_adapter import (
            TerraformProvisionerAdapter,
        )

        mock_runner = MagicMock()
        mock_runner.output.return_value = _mock_terraform_output()

        mock_node = MagicMock(spec=ProxyNode)
        mock_parser = MagicMock()
        mock_parser.to_proxy_node.return_value = mock_node

        adapter = TerraformProvisionerAdapter(
            engagement_dir=tmp_path,
            hcl_generator=MagicMock(generate=MagicMock(return_value=tmp_path / "main.tf")),
            terraform_runner=mock_runner,
            state_parser=mock_parser,
        )

        result = adapter.provision(_valid_config())

        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0] is mock_node


class TestTerraformProvisionerAdapterDestroy:
    """Tests for destroy() method."""

    def test_destroy_calls_terraform_destroy_with_auto_approve(self, tmp_path: Path) -> None:
        """destroy() must call terraform destroy (auto-approve via runner)."""
        from src.proxy_infra.infrastructure.adapters.terraform_provisioner_adapter import (
            TerraformProvisionerAdapter,
        )

        mock_runner = MagicMock()

        adapter = TerraformProvisionerAdapter(
            engagement_dir=tmp_path,
            hcl_generator=MagicMock(),
            terraform_runner=mock_runner,
            state_parser=MagicMock(),
        )

        adapter.destroy(node_ids=["123456"], engagement_id="RED-TEST-001")

        mock_runner.destroy.assert_called_once()


class TestTerraformProvisionerAdapterErrors:
    """Tests for error handling."""

    def test_provision_raises_on_terraform_apply_failure(self, tmp_path: Path) -> None:
        """Non-zero exit code from apply must raise ProvisionError."""
        from src.proxy_infra.domain.exceptions.provision_error import ProvisionError
        from src.proxy_infra.infrastructure.adapters.terraform_provisioner_adapter import (
            TerraformProvisionerAdapter,
        )
        from src.proxy_infra.infrastructure.terraform.terraform_apply_error import (
            TerraformApplyError,
        )

        mock_runner = MagicMock()
        mock_runner.apply.side_effect = TerraformApplyError("apply failed")

        adapter = TerraformProvisionerAdapter(
            engagement_dir=tmp_path,
            hcl_generator=MagicMock(generate=MagicMock(return_value=tmp_path / "main.tf")),
            terraform_runner=mock_runner,
            state_parser=MagicMock(),
        )

        with pytest.raises(ProvisionError):
            adapter.provision(_valid_config())

    def test_destroy_raises_on_terraform_destroy_failure(self, tmp_path: Path) -> None:
        """Non-zero exit code from destroy must raise with details."""
        from src.proxy_infra.infrastructure.adapters.terraform_provisioner_adapter import (
            TerraformProvisionerAdapter,
        )
        from src.proxy_infra.infrastructure.terraform.terraform_destroy_error import (
            TerraformDestroyError,
        )

        mock_runner = MagicMock()
        mock_runner.destroy.side_effect = TerraformDestroyError("destroy failed")

        adapter = TerraformProvisionerAdapter(
            engagement_dir=tmp_path,
            hcl_generator=MagicMock(),
            terraform_runner=mock_runner,
            state_parser=MagicMock(),
        )

        result = adapter.destroy(node_ids=["123456"], engagement_id="RED-TEST-001")

        assert "123456" in result.failed


class TestTerraformProvisionerAdapterArchitecture:
    """Architecture tests for security invariants."""

    def test_no_shell_true_anywhere_in_subprocess_calls(self) -> None:
        """Architecture test: no subprocess.run call in terraform modules uses shell=True."""
        import ast
        from pathlib import Path

        terraform_dir = Path("src/proxy_infra/infrastructure/terraform")
        violations = []

        for py_file in terraform_dir.glob("*.py"):
            tree = ast.parse(py_file.read_text())
            for node in ast.walk(tree):
                if isinstance(node, ast.Call):
                    func = node.func
                    is_subprocess_run = False
                    if isinstance(func, ast.Attribute) and func.attr == "run":
                        is_subprocess_run = True
                    if is_subprocess_run:
                        for kw in node.keywords:
                            if kw.arg == "shell" and isinstance(kw.value, ast.Constant):
                                if kw.value.value is True:
                                    violations.append(f"{py_file.name}:{node.lineno}")

        assert violations == [], f"T-009 STRIDE violation: shell=True found in: {violations}"
