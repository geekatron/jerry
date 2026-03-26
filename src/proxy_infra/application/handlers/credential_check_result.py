# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""CredentialCheckResult value object (H-10: one class per file)."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CredentialCheckResult:
    """Result of a credential existence check.

    The value is never exposed — only presence/absence is reported.

    Attributes:
        found: True if a credential exists for the provider.
        provider: Provider name that was checked.
        source: Which store had the credential ("keychain", "environment", or "none").
    """

    found: bool
    provider: str
    source: str = "none"
