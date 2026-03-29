# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Raised when the age encryption binary is not found.

References:
    - TASK-023-103: State encryption with age
"""

from __future__ import annotations

from src.proxy_infra.infrastructure.terraform.terraform_error import TerraformError


class AgeNotFoundError(TerraformError):
    """Raised when the age encryption binary is not found in PATH."""
