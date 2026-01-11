"""
SessionId - Value Object representing a valid session identifier.

Format: SESS-{uuid8}
Where:
    - uuid8: 8 hexadecimal characters (lowercase)

This is an immutable value object that extends VertexId from shared_kernel.

References:
    - ENFORCE-008d.3: New Domain Objects
    - Canon PAT-001: VertexId Base Class
    - ADR-013: Shared Kernel Module
"""

from __future__ import annotations

import re
import uuid
from dataclasses import dataclass
from typing import ClassVar, Pattern

from src.shared_kernel.vertex_id import VertexId


@dataclass(frozen=True)
class SessionId(VertexId):
    """Immutable value object representing a valid session identifier.

    Extends VertexId from shared_kernel for graph-ready identity.
    Format: SESS-{uuid8} where uuid8 is 8 lowercase hex characters.

    Attributes:
        value: The full session ID string (inherited from VertexId)

    Example:
        >>> session_id = SessionId.generate()
        >>> session_id.value
        'SESS-a1b2c3d4'
    """

    # Regex pattern for valid session IDs
    _PATTERN: ClassVar[Pattern[str]] = re.compile(r"^SESS-[a-f0-9]{8}$")

    @classmethod
    def _is_valid_format(cls, value: str) -> bool:
        """Validate session ID format.

        Args:
            value: The string to validate

        Returns:
            True if format is valid SESS-{uuid8}
        """
        return bool(cls._PATTERN.match(value))

    @classmethod
    def generate(cls) -> SessionId:
        """Generate a new SessionId with a random UUID.

        Returns:
            A new SessionId instance with format SESS-{uuid8}
        """
        return cls(f"SESS-{uuid.uuid4().hex[:8]}")

    @classmethod
    def from_string(cls, value: str) -> SessionId:
        """Parse ID from string representation.

        This is the VertexId-compatible factory method.

        Args:
            value: The session ID string to parse

        Returns:
            A validated SessionId instance

        Raises:
            ValueError: If the format is invalid (via VertexId.__post_init__)
        """
        return cls(value)

    def __repr__(self) -> str:
        """Return a detailed representation."""
        return f"SessionId(value={self.value!r})"
