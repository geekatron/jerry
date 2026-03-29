# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Raised when a terraform state file is not found.

References:
    - TASK-023-103: State encryption with age
"""

from __future__ import annotations

from src.proxy_infra.infrastructure.terraform.terraform_error import TerraformError


class StateFileNotFoundError(TerraformError):
    """Raised when terraform.tfstate or terraform.tfstate.age is not found."""
