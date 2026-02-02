"""
ILlmContextSerializer - LLM Context Serialization Port.

Defines the contract for serializing data structures for LLM consumption.
Supports multiple formats optimized for different use cases:
- TOON: Token-optimized (30-60% reduction)
- JSON: Standard format (interoperability)
- Human: Human-readable text format

This is a secondary port (driven) used by interface adapters
to format output for LLM context windows.

References:
    - impl-es-e-002-toon-serialization.md: TOON research
    - DISC-012: TOON Format Required as Primary Output
"""

from __future__ import annotations

from enum import Enum, auto
from typing import Any, Protocol, runtime_checkable


class OutputFormat(Enum):
    """Supported output formats for LLM context."""

    TOON = auto()  # Token-Oriented Object Notation (default)
    JSON = auto()  # Standard JSON
    HUMAN = auto()  # Human-readable text


@runtime_checkable
class ILlmContextSerializer(Protocol):
    """Protocol for LLM context serialization.

    Serializers convert Python data structures into string formats
    optimized for LLM context windows. The primary format (TOON)
    provides 30-60% token reduction compared to JSON.

    Example:
        >>> serializer = ToonSerializer()
        >>> data = [{"id": 1, "name": "Task 1"}, {"id": 2, "name": "Task 2"}]
        >>> output = serializer.serialize(data)
        >>> # Returns TOON tabular format

    Usage Guidelines:
        - Use TOON for: Work item arrays, event audit trails, checkpoint summaries
        - Use JSON for: Complex nested objects, external API payloads
        - Use Human for: Direct user-facing output, reports
    """

    def serialize(self, data: Any, format: OutputFormat = OutputFormat.TOON) -> str:
        """Serialize data to the specified format.

        Args:
            data: Python data structure (dict, list, or dataclass)
            format: Target output format (default: TOON)

        Returns:
            Serialized string in the requested format

        Raises:
            SerializationError: If data cannot be serialized
        """
        ...

    def deserialize(self, text: str, format: OutputFormat = OutputFormat.TOON) -> Any:
        """Deserialize text back to Python data structure.

        Args:
            text: Serialized string in the specified format
            format: Source format of the text (default: TOON)

        Returns:
            Deserialized Python data structure

        Raises:
            DeserializationError: If text cannot be parsed
        """
        ...

    def detect_format(self, text: str) -> OutputFormat:
        """Detect the format of serialized text.

        Args:
            text: Serialized string to analyze

        Returns:
            Detected OutputFormat
        """
        ...

    def is_tabular_eligible(self, data: Any) -> bool:
        """Check if data is eligible for TOON tabular format.

        Tabular format provides maximum token efficiency for
        uniform object arrays.

        Args:
            data: Data to check

        Returns:
            True if data can use tabular format, False otherwise
        """
        ...
