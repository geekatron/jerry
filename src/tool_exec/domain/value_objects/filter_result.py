# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""FilterResult value object.

Extracted from credential_filter.py to comply with H-10 (one class per file).

References:
    - ADR-PROJ023-001: Behavioral Contract BC-07 (Credential Filtering)
    - CC-001: H-10 one-class-per-file remediation
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.tool_exec.domain.value_objects.credential_match import CredentialMatch


@dataclass
class FilterResult:
    """Result of applying the credential filter to output.

    Attributes:
        detected: Whether any credential was detected.
        match: The first CredentialMatch, or None if no detection.
        filtered_output: The output after filtering (inline [CREDENTIAL-REDACTED]
            substitution on the affected line, or original output if not detected).
        raw_output: The original unfiltered output.
    """

    detected: bool
    match: CredentialMatch | None
    filtered_output: str
    raw_output: str
