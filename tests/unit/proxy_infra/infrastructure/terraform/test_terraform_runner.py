# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""RED phase tests for TASK-023-102: Terraform Runner (subprocess wrapper).

Tests verify:
1. Correct subprocess arguments for init/apply/destroy/output
2. No shell=True in any call
3. Typed error classes for each operation failure
4. Pre-flight check for terraform binary
5. Version validation

All tests MUST FAIL before implementation (H-20 RED phase).
"""

from __future__ import annotations

import subprocess
from pathlib import Path
from unittest.mock import patch

import pytest


class TestTerraformRunnerInit:
    """Tests for terraform init subprocess calls."""

    def test_init_subprocess_args_correct(self, tmp_path: Path) -> None:
        """terraform_init must call subprocess with ['terraform', 'init']."""
        from src.proxy_infra.infrastructure.terraform.terraform_runner import (
            TerraformRunner,
        )

        runner = TerraformRunner(terraform_binary="terraform")

        with patch("subprocess.run") as mock_run:
            mock_run.return_value = subprocess.CompletedProcess(
                args=["terraform", "init"], returncode=0, stdout="", stderr=""
            )
            runner.init(work_dir=tmp_path)

            mock_run.assert_called_once()
            call_args = mock_run.call_args
            cmd = call_args[0][0] if call_args[0] else call_args[1].get("args", [])
            assert cmd[0] == "terraform"
            assert cmd[1] == "init"
            # CRITICAL: verify no shell=True (T-009)
            assert call_args[1].get("shell", False) is False


class TestTerraformRunnerApply:
    """Tests for terraform apply subprocess calls."""

    def test_apply_subprocess_args_include_auto_approve(self, tmp_path: Path) -> None:
        """terraform apply must include -auto-approve flag."""
        from src.proxy_infra.infrastructure.terraform.terraform_runner import (
            TerraformRunner,
        )

        runner = TerraformRunner(terraform_binary="terraform")

        with patch("subprocess.run") as mock_run:
            mock_run.return_value = subprocess.CompletedProcess(
                args=["terraform", "apply"], returncode=0, stdout="", stderr=""
            )
            runner.apply(work_dir=tmp_path)

            call_args = mock_run.call_args
            cmd = call_args[0][0] if call_args[0] else call_args[1].get("args", [])
            assert "apply" in cmd
            assert "-auto-approve" in cmd


class TestTerraformRunnerDestroy:
    """Tests for terraform destroy subprocess calls."""

    def test_destroy_subprocess_args_include_auto_approve(self, tmp_path: Path) -> None:
        """terraform destroy must include -auto-approve flag."""
        from src.proxy_infra.infrastructure.terraform.terraform_runner import (
            TerraformRunner,
        )

        runner = TerraformRunner(terraform_binary="terraform")

        with patch("subprocess.run") as mock_run:
            mock_run.return_value = subprocess.CompletedProcess(
                args=["terraform", "destroy"], returncode=0, stdout="", stderr=""
            )
            runner.destroy(work_dir=tmp_path)

            call_args = mock_run.call_args
            cmd = call_args[0][0] if call_args[0] else call_args[1].get("args", [])
            assert "destroy" in cmd
            assert "-auto-approve" in cmd


class TestTerraformRunnerOutput:
    """Tests for terraform output subprocess calls."""

    def test_output_subprocess_args_include_json_flag(self, tmp_path: Path) -> None:
        """terraform output must include -json flag."""
        from src.proxy_infra.infrastructure.terraform.terraform_runner import (
            TerraformRunner,
        )

        runner = TerraformRunner(terraform_binary="terraform")

        with patch("subprocess.run") as mock_run:
            mock_run.return_value = subprocess.CompletedProcess(
                args=["terraform", "output"],
                returncode=0,
                stdout='{"droplet_ip": {"value": "1.2.3.4"}}',
                stderr="",
            )
            runner.output(work_dir=tmp_path)

            call_args = mock_run.call_args
            cmd = call_args[0][0] if call_args[0] else call_args[1].get("args", [])
            assert "output" in cmd
            assert "-json" in cmd


class TestTerraformRunnerErrors:
    """Tests for typed error handling."""

    def test_non_zero_exit_raises_typed_error_on_init(self, tmp_path: Path) -> None:
        """Non-zero exit code from init must raise TerraformInitError."""
        from src.proxy_infra.infrastructure.terraform.terraform_init_error import (
            TerraformInitError,
        )
        from src.proxy_infra.infrastructure.terraform.terraform_runner import (
            TerraformRunner,
        )

        runner = TerraformRunner(terraform_binary="terraform")

        with patch("subprocess.run") as mock_run:
            mock_run.return_value = subprocess.CompletedProcess(
                args=["terraform", "init"],
                returncode=1,
                stdout="",
                stderr="Error: plugin installation failed",
            )
            with pytest.raises(TerraformInitError):
                runner.init(work_dir=tmp_path)

    def test_non_zero_exit_raises_typed_error_on_apply(self, tmp_path: Path) -> None:
        """Non-zero exit code from apply must raise TerraformApplyError."""
        from src.proxy_infra.infrastructure.terraform.terraform_apply_error import (
            TerraformApplyError,
        )
        from src.proxy_infra.infrastructure.terraform.terraform_runner import (
            TerraformRunner,
        )

        runner = TerraformRunner(terraform_binary="terraform")

        with patch("subprocess.run") as mock_run:
            mock_run.return_value = subprocess.CompletedProcess(
                args=["terraform", "apply"],
                returncode=1,
                stdout="",
                stderr="Error: creating droplet",
            )
            with pytest.raises(TerraformApplyError):
                runner.apply(work_dir=tmp_path)

    def test_non_zero_exit_raises_typed_error_on_destroy(self, tmp_path: Path) -> None:
        """Non-zero exit code from destroy must raise TerraformDestroyError."""
        from src.proxy_infra.infrastructure.terraform.terraform_destroy_error import (
            TerraformDestroyError,
        )
        from src.proxy_infra.infrastructure.terraform.terraform_runner import (
            TerraformRunner,
        )

        runner = TerraformRunner(terraform_binary="terraform")

        with patch("subprocess.run") as mock_run:
            mock_run.return_value = subprocess.CompletedProcess(
                args=["terraform", "destroy"],
                returncode=1,
                stdout="",
                stderr="Error: destroying resource",
            )
            with pytest.raises(TerraformDestroyError):
                runner.destroy(work_dir=tmp_path)


class TestTerraformRunnerPreflight:
    """Tests for binary pre-flight and version checks."""

    def test_preflight_raises_if_terraform_not_in_path(self) -> None:
        """Pre-flight check must raise when terraform binary not found."""
        from src.proxy_infra.infrastructure.terraform.terraform_not_found_error import (
            TerraformNotFoundError,
        )
        from src.proxy_infra.infrastructure.terraform.terraform_runner import (
            TerraformRunner,
        )

        runner = TerraformRunner(terraform_binary="/nonexistent/path/terraform")

        with pytest.raises(TerraformNotFoundError):
            runner.preflight_check()

    def test_version_validation_raises_on_unsupported_version(self) -> None:
        """Version check must raise on terraform versions below minimum."""
        from src.proxy_infra.infrastructure.terraform.terraform_runner import (
            TerraformRunner,
        )
        from src.proxy_infra.infrastructure.terraform.terraform_version_error import (
            TerraformVersionError,
        )

        runner = TerraformRunner(terraform_binary="terraform")

        with patch("subprocess.run") as mock_run:
            mock_run.return_value = subprocess.CompletedProcess(
                args=["terraform", "version", "-json"],
                returncode=0,
                stdout='{"terraform_version": "0.12.0"}',
                stderr="",
            )
            with pytest.raises(TerraformVersionError):
                runner.preflight_check()
