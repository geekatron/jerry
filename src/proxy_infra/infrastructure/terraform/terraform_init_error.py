# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Raised when terraform init fails.

References:
    - TASK-023-102: Terraform runner + state parser
"""

from __future__ import annotations

from src.proxy_infra.infrastructure.terraform.terraform_error import TerraformError


class TerraformInitError(TerraformError):
    """Raised when terraform init fails."""
