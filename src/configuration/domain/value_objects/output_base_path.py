# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
OutputBasePath - Immutable value object for output base path configuration.

Wraps a single string path value with minimal domain validation.
Rejects null bytes (path-traversal attack vector). Permits empty strings
(triggers fallback in OutputResolver).

References:
    - GitHub Issue #192: Configurable output base path for skill agents
    - REQ-OBP-003c: OutputBasePath value object specification
    - ADR-PROJ021-001: Output path resolution architecture

Exports:
    OutputBasePath: Immutable output base path value object
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class OutputBasePath:
    """Immutable value object wrapping an output base path string.

    Attributes:
        value: The path string. May be relative or absolute.
            Empty string is permitted (triggers fallback in resolver).

    Invariants:
        - Path must not contain null bytes (\\x00)

    Examples:
        >>> OutputBasePath("work/")
        OutputBasePath(value='work/')
        >>> OutputBasePath("")
        OutputBasePath(value='')
        >>> OutputBasePath("/absolute/path/")
        OutputBasePath(value='/absolute/path/')
    """

    value: str

    def __post_init__(self) -> None:
        """Validate path after initialization."""
        if "\x00" in self.value:
            raise ValueError(f"Output base path must not contain null bytes: {self.value!r}")

    def __str__(self) -> str:
        """Return the path value for display."""
        return self.value
