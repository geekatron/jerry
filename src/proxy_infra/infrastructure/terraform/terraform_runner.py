# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Terraform subprocess runner for proxy infrastructure provisioning.

Wraps terraform CLI commands (init, apply, destroy, output) via subprocess
with list args. NEVER uses shell=True (T-009: STRIDE command injection).

References:
    - TASK-023-102: Terraform runner + state parser
    - ADR-EN023-003: Infrastructure provisioning (Option C: Hybrid)
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any

from src.proxy_infra.infrastructure.terraform.terraform_apply_error import (
    TerraformApplyError,
)
from src.proxy_infra.infrastructure.terraform.terraform_destroy_error import (
    TerraformDestroyError,
)
from src.proxy_infra.infrastructure.terraform.terraform_init_error import (
    TerraformInitError,
)
from src.proxy_infra.infrastructure.terraform.terraform_not_found_error import (
    TerraformNotFoundError,
)
from src.proxy_infra.infrastructure.terraform.terraform_output_error import (
    TerraformOutputError,
)
from src.proxy_infra.infrastructure.terraform.terraform_version_error import (
    TerraformVersionError,
)

#: Minimum supported terraform version.
_MIN_TERRAFORM_VERSION = (1, 0, 0)


class TerraformRunner:
    """Wraps terraform CLI commands via subprocess with list args.

    All subprocess calls use list arguments (never shell=True) to prevent
    command injection (T-009 STRIDE threat model).

    Attributes:
        terraform_binary: Path or name of the terraform binary.
    """

    def __init__(self, terraform_binary: str = "terraform") -> None:
        """Initialise the runner with a terraform binary path.

        Args:
            terraform_binary: Path or name of the terraform binary.
                Defaults to "terraform" (resolved via PATH).
        """
        self._binary = terraform_binary

    def preflight_check(self) -> None:
        """Verify terraform binary exists and meets minimum version.

        Raises:
            TerraformNotFoundError: If the terraform binary is not found.
            TerraformVersionError: If the version is below minimum.
        """
        try:
            result = subprocess.run(
                [self._binary, "version", "-json"],
                capture_output=True,
                text=True,
                check=False,
            )
        except FileNotFoundError as exc:
            raise TerraformNotFoundError(
                f"terraform binary not found at '{self._binary}' — "
                f"install terraform >= "
                f"{'.'.join(str(v) for v in _MIN_TERRAFORM_VERSION)} "
                f"and ensure it is in PATH"
            ) from exc

        if result.returncode != 0:
            raise TerraformNotFoundError(f"terraform version check failed: {result.stderr}")

        version_info = json.loads(result.stdout)
        version_str = version_info.get("terraform_version", "0.0.0")
        version_parts = tuple(int(p) for p in version_str.split(".")[:3])

        if version_parts < _MIN_TERRAFORM_VERSION:
            raise TerraformVersionError(
                f"terraform version {version_str} is below minimum "
                f"{'.'.join(str(v) for v in _MIN_TERRAFORM_VERSION)}"
            )

    def init(self, work_dir: Path) -> subprocess.CompletedProcess[str]:
        """Run terraform init in the work directory.

        Args:
            work_dir: Directory containing the .tf files.

        Returns:
            Completed subprocess result.

        Raises:
            TerraformInitError: If init fails (non-zero exit code).
        """
        result = subprocess.run(
            [self._binary, "init"],
            cwd=str(work_dir),
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode != 0:
            raise TerraformInitError(
                f"terraform init failed (exit {result.returncode}): {result.stderr}"
            )
        return result

    def apply(self, work_dir: Path) -> subprocess.CompletedProcess[str]:
        """Run terraform apply -auto-approve in the work directory.

        Args:
            work_dir: Directory containing the .tf files and state.

        Returns:
            Completed subprocess result.

        Raises:
            TerraformApplyError: If apply fails (non-zero exit code).
        """
        result = subprocess.run(
            [self._binary, "apply", "-auto-approve"],
            cwd=str(work_dir),
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode != 0:
            raise TerraformApplyError(
                f"terraform apply failed (exit {result.returncode}): {result.stderr}"
            )
        return result

    def destroy(self, work_dir: Path) -> subprocess.CompletedProcess[str]:
        """Run terraform destroy -auto-approve in the work directory.

        Args:
            work_dir: Directory containing the .tf files and state.

        Returns:
            Completed subprocess result.

        Raises:
            TerraformDestroyError: If destroy fails (non-zero exit code).
        """
        result = subprocess.run(
            [self._binary, "destroy", "-auto-approve"],
            cwd=str(work_dir),
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode != 0:
            raise TerraformDestroyError(
                f"terraform destroy failed (exit {result.returncode}): {result.stderr}"
            )
        return result

    def output(self, work_dir: Path) -> dict[str, Any]:
        """Run terraform output -json and return parsed dict.

        Args:
            work_dir: Directory containing the .tf files and state.

        Returns:
            Parsed JSON dict of terraform outputs.

        Raises:
            TerraformOutputError: If output command fails.
        """
        result = subprocess.run(
            [self._binary, "output", "-json"],
            cwd=str(work_dir),
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode != 0:
            raise TerraformOutputError(
                f"terraform output failed (exit {result.returncode}): {result.stderr}"
            )
        return json.loads(result.stdout)
