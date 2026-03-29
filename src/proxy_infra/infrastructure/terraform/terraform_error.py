# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Base exception for terraform operation failures.

References:
    - TASK-023-102: Terraform runner + state parser
"""

from __future__ import annotations


class TerraformError(Exception):
    """Base exception for terraform operation failures."""
