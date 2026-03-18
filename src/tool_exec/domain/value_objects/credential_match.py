# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""CredentialMatch value object.

Extracted from credential_filter.py to comply with H-10 (one class per file).

References:
    - ADR-PROJ023-001: Behavioral Contract BC-07 (Credential Filtering)
    - CC-001: H-10 one-class-per-file remediation
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CredentialMatch:
    """Result of a credential detection match.

    Attributes:
        pattern: The regex pattern that matched.
        line_number: 1-based line number where the match occurred.
        case_sensitive: Whether the match was case-sensitive.
    """

    pattern: str
    line_number: int
    case_sensitive: bool
