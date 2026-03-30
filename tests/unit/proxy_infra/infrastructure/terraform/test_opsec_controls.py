# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""RED phase tests for TASK-023-106: OPSEC Controls.

Tests verify the 7 mandatory OPSEC controls from ADR-EN023-003:
1. R-GITIGNORE: .gitignore contains terraform patterns
2. R-CHMOD-STATE: state files get chmod 600
3. R-CHMOD-DIR: engagement dirs get chmod 700
4. R-PROVIDER-PIN: HCL template pins exact provider version
5. R-NO-TLS-PRIVATE-KEY: No tls_private_key in HCL
6. R-NO-SHELL: No shell=True in subprocess calls
7. R-PRE-COMMIT: Pre-commit hook for tfstate detection

All tests MUST FAIL before implementation (H-20 RED phase).
"""

from __future__ import annotations

import ast
from pathlib import Path


class TestGitignoreOpsec:
    """Tests for .gitignore terraform patterns (R-GITIGNORE)."""

    def test_gitignore_contains_tfstate_pattern(self) -> None:
        """R-GITIGNORE: .gitignore must contain *.tfstate."""
        gitignore = Path(".gitignore")
        assert gitignore.exists(), ".gitignore must exist"
        content = gitignore.read_text()
        assert "*.tfstate" in content

    def test_gitignore_contains_tfstate_backup_pattern(self) -> None:
        """R-GITIGNORE: .gitignore must contain *.tfstate.*."""
        content = Path(".gitignore").read_text()
        assert "*.tfstate.*" in content

    def test_gitignore_contains_tfstate_age_pattern(self) -> None:
        """R-GITIGNORE: .gitignore must contain *.tfstate.age."""
        content = Path(".gitignore").read_text()
        assert "*.tfstate.age" in content

    def test_gitignore_contains_terraform_directory(self) -> None:
        """R-GITIGNORE: .gitignore must contain **/.terraform/."""
        content = Path(".gitignore").read_text()
        assert "**/.terraform/" in content or ".terraform/" in content


class TestHclTemplateOpsec:
    """Tests for HCL template security controls."""

    def test_hcl_template_pins_exact_provider_version(self) -> None:
        """R-PROVIDER-PIN: Template must use = version constraint, not ~>."""
        template = Path("infra/terraform/modules/digitalocean-proxy/main.tf.j2")
        assert template.exists(), "main.tf.j2 must exist"
        content = template.read_text()
        # Must have exact pin (= "X.Y.Z") not approximate (~> X.Y)
        assert '= "' in content, 'Provider version must use exact pin (= "X.Y.Z")'
        assert "~>" not in content, "Provider version must NOT use ~> constraint"

    def test_hcl_template_has_no_tls_private_key_resource(self) -> None:
        """R-NO-TLS-PRIVATE-KEY: Template must not declare tls_private_key."""
        template = Path("infra/terraform/modules/digitalocean-proxy/main.tf.j2")
        content = template.read_text()
        assert "tls_private_key" not in content, (
            "HCL template must not contain tls_private_key resource — "
            "SSH keys are pre-generated outside terraform"
        )


class TestSubprocessOpsec:
    """Tests for subprocess security controls (R-NO-SHELL)."""

    def test_no_shell_true_in_subprocess_calls(self) -> None:
        """R-NO-SHELL: All terraform module files must not use shell=True."""
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


class TestChmodOpsec:
    """Tests for filesystem permission controls."""

    def test_state_file_chmod_600_after_write(self, tmp_path: Path) -> None:
        """R-CHMOD-STATE: State files must get chmod 600 after write."""
        from src.proxy_infra.infrastructure.terraform.state_parser import (
            StateParser,
        )

        state_file = tmp_path / "terraform.tfstate"
        parser = StateParser()
        parser.write_state(state_file, '{"version": 4}')

        file_mode = oct(state_file.stat().st_mode)[-3:]
        assert file_mode == "600", f"Expected chmod 600, got {file_mode}"

    def test_engagement_dir_chmod_700_on_creation(self, tmp_path: Path) -> None:
        """R-CHMOD-DIR: Engagement terraform dirs must get chmod 700 on creation."""
        from unittest.mock import MagicMock

        from src.proxy_infra.infrastructure.adapters.terraform_provisioner_adapter import (
            TerraformProvisionerAdapter,
        )

        mock_hcl = MagicMock()
        mock_hcl.generate.return_value = tmp_path / "terraform" / "main.tf"

        mock_runner = MagicMock()
        mock_runner.output.return_value = {
            "droplet_ip": {"value": "1.2.3.4"},
            "droplet_id": {"value": "123"},
            "ssh_key_id": {"value": "456"},
            "firewall_id": {"value": "789"},
        }

        adapter = TerraformProvisionerAdapter(
            engagement_dir=tmp_path,
            hcl_generator=mock_hcl,
            terraform_runner=mock_runner,
            state_parser=MagicMock(),
        )

        config = {
            "engagement_id": "RED-TEST-001",
            "region": "nyc3",
            "size": "s-1vcpu-1gb",
            "image": "ubuntu-24-04-x64",
            "ssh_public_key": "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAA test",
            "operator_ip": "198.51.100.1",
            "socks_port": 1080,
        }
        adapter.provision(config)

        terraform_dir = tmp_path / "terraform"
        dir_mode = oct(terraform_dir.stat().st_mode)[-3:]
        assert dir_mode == "700", f"Expected chmod 700, got {dir_mode}"
