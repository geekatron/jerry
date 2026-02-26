# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
VendorOverrideSpec - Allowlist of valid vendor override keys.

Prevents governance field injection through per-agent vendor override files.
Each vendor has a defined set of keys that may be overridden; attempts to
override governance keys (constitution, guardrails, enforcement) are rejected.

References:
    - PROJ-012: Agent Configuration Extraction & Schema Enforcement
    - ADR-PROJ010-003: LLM Portability Architecture
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class VendorOverrideSpec:
    """Specification of allowed override keys for a vendor.

    Attributes:
        vendor: Vendor identifier (e.g., 'claude_code').
        allowed_keys: Frozenset of top-level keys that may appear in overrides.
    """

    vendor: str
    allowed_keys: frozenset[str]

    def validate(self, overrides: dict[str, object]) -> list[str]:
        """Validate override keys against the allowlist.

        Args:
            overrides: Dictionary of override key-value pairs.

        Returns:
            List of error messages for disallowed keys. Empty if all valid.
        """
        errors: list[str] = []
        for key in overrides:
            if key not in self.allowed_keys:
                errors.append(
                    f"Disallowed vendor override key: {key!r}. "
                    f"Allowed keys for {self.vendor}: "
                    f"{', '.join(sorted(self.allowed_keys))}"
                )
        return errors


CLAUDE_CODE_OVERRIDE_SPEC = VendorOverrideSpec(
    vendor="claude_code",
    allowed_keys=frozenset(
        {
            "permissionMode",
            "background",
            "maxTurns",
            "isolation",
            "skills",
            "hooks",
            "memory",
        }
    ),
)
