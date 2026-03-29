# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Raised when age encryption or decryption fails.

References:
    - TASK-023-103: State encryption with age
"""

from __future__ import annotations

from src.proxy_infra.infrastructure.terraform.terraform_error import TerraformError


class EncryptionError(TerraformError):
    """Raised when age encryption or decryption fails."""
