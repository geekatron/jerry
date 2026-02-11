# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
ToonSerializer - Token-Oriented Object Notation Serializer.

Implements ILlmContextSerializer using TOON format for token-efficient
serialization. Provides 30-60% token reduction compared to JSON while
maintaining equivalent or better LLM comprehension accuracy.

TOON Format Features:
- Indentation-based syntax (no braces)
- Tabular arrays for uniform objects (maximum efficiency)
- Minimal quoting for strings
- Human-readable, LLM-optimized

References:
    - impl-es-e-002-toon-serialization.md: Full specification
    - https://toonformat.dev/: Official TOON specification
    - DISC-012: TOON Format Required as Primary Output
"""

from __future__ import annotations

import json
from dataclasses import asdict, is_dataclass
from datetime import datetime
from typing import Any

from src.application.ports.secondary.illm_context_serializer import OutputFormat


class SerializationError(Exception):
    """Raised when serialization fails."""

    def __init__(self, message: str, data: Any = None) -> None:
        self.data = data
        super().__init__(message)


class DeserializationError(Exception):
    """Raised when deserialization fails."""

    def __init__(self, message: str, line: int | None = None) -> None:
        self.line = line
        super().__init__(f"{message} (line {line})" if line else message)


class ToonSerializer:
    """TOON serializer adapter for LLM context formatting.

    Optimized for:
    - Domain event arrays (audit logs)
    - Work item lists
    - Checkpoint summaries

    Example:
        >>> serializer = ToonSerializer()
        >>> data = [{"id": 1, "name": "Task"}, {"id": 2, "name": "Bug"}]
        >>> output = serializer.serialize(data)
        >>> # Returns: [2]{id,name}:\\n  1,Task\\n  2,Bug

    Attributes:
        _indent: Number of spaces for indentation (default: 2)
        _delimiter: Column delimiter for tabular arrays (default: ,)
    """

    def __init__(
        self,
        indent: int = 2,
        delimiter: str = ",",
    ) -> None:
        """Initialize the serializer.

        Args:
            indent: Spaces per indentation level
            delimiter: Column separator for tabular arrays
        """
        self._indent = indent
        self._delimiter = delimiter

    def serialize(
        self,
        data: Any,
        format: OutputFormat = OutputFormat.TOON,
    ) -> str:
        """Serialize data to the specified format.

        Args:
            data: Python data structure
            format: Target output format

        Returns:
            Serialized string

        Raises:
            SerializationError: If serialization fails
        """
        try:
            normalized = self._normalize(data)

            if format == OutputFormat.TOON:
                return self._encode_toon(normalized)
            elif format == OutputFormat.JSON:
                return json.dumps(normalized, indent=2, default=str)
            elif format == OutputFormat.HUMAN:
                return self._encode_human(normalized)
            else:
                raise SerializationError(f"Unknown format: {format}", data)
        except (TypeError, ValueError) as e:
            raise SerializationError(str(e), data) from e

    def deserialize(
        self,
        text: str,
        format: OutputFormat = OutputFormat.TOON,
    ) -> Any:
        """Deserialize text to Python data structure.

        Args:
            text: Serialized string
            format: Source format

        Returns:
            Deserialized Python data

        Raises:
            DeserializationError: If parsing fails
        """
        try:
            if format == OutputFormat.TOON:
                return self._decode_toon(text)
            elif format == OutputFormat.JSON:
                return json.loads(text)
            elif format == OutputFormat.HUMAN:
                # Human format is not reversible
                raise DeserializationError("Human format cannot be deserialized")
            else:
                raise DeserializationError(f"Unknown format: {format}")
        except json.JSONDecodeError as e:
            raise DeserializationError(str(e), e.lineno) from e

    def detect_format(self, text: str) -> OutputFormat:
        """Detect the format of serialized text.

        Args:
            text: Serialized string

        Returns:
            Detected OutputFormat
        """
        text = text.strip()

        # Check for JSON indicators
        if text.startswith("{") or text.startswith("["):
            try:
                json.loads(text)
                return OutputFormat.JSON
            except json.JSONDecodeError:
                pass

        # Check for TOON indicators
        if ":" in text and not text.startswith("{"):
            # Look for tabular array header pattern
            if "[" in text.splitlines()[0] and "]" in text.splitlines()[0]:
                return OutputFormat.TOON
            # Look for key: value pattern without braces
            if "\n" in text or "\r\n" in text:
                lines = text.splitlines()
                if any(":" in line and not line.strip().startswith("{") for line in lines):
                    return OutputFormat.TOON

        return OutputFormat.HUMAN

    def is_tabular_eligible(self, data: Any) -> bool:
        """Check if data can use TOON tabular format.

        Tabular format requires:
        - List of 2+ items
        - All items are dicts
        - All dicts have same keys
        - All values are primitives

        Args:
            data: Data to check

        Returns:
            True if tabular format can be used
        """
        if not isinstance(data, list) or len(data) < 2:
            return False

        if not all(isinstance(item, dict) for item in data):
            return False

        first_keys = set(data[0].keys())
        if not first_keys:
            return False

        for item in data:
            if set(item.keys()) != first_keys:
                return False
            if not all(isinstance(v, str | int | float | bool | type(None)) for v in item.values()):
                return False

        return True

    # =========================================================================
    # Private: Normalization
    # =========================================================================

    def _normalize(self, data: Any) -> Any:
        """Convert domain objects to serializable dicts."""
        if is_dataclass(data) and not isinstance(data, type):
            return asdict(data)
        to_dict_method = getattr(data, "to_dict", None)
        if to_dict_method is not None and callable(to_dict_method):
            return to_dict_method()
        if isinstance(data, datetime):
            return data.isoformat()
        if isinstance(data, list):
            return [self._normalize(item) for item in data]
        if isinstance(data, dict):
            return {k: self._normalize(v) for k, v in data.items()}
        # Enum support - use getattr for pyright compatibility
        value_attr = getattr(data, "value", None)
        if value_attr is not None:
            return value_attr
        return data

    # =========================================================================
    # Private: TOON Encoding
    # =========================================================================

    def _encode_toon(self, data: Any) -> str:
        """Encode data to TOON format."""
        if isinstance(data, list):
            return self._encode_array(data, depth=0)
        elif isinstance(data, dict):
            return self._encode_object(data, depth=0)
        else:
            return self._encode_value(data)

    def _encode_value(self, value: Any) -> str:
        """Encode a primitive value."""
        if value is None:
            return "null"
        if isinstance(value, bool):
            return "true" if value else "false"
        if isinstance(value, int | float):
            return str(value)
        if isinstance(value, str):
            return self._quote_if_needed(value)
        return str(value)

    def _encode_array(self, arr: list[Any], depth: int) -> str:
        """Encode an array, using tabular format when eligible."""
        if not arr:
            return "[0]:"

        # Check for tabular eligibility
        if self.is_tabular_eligible(arr):
            return self._encode_tabular_array(arr, depth)

        # Check for primitive array
        if all(isinstance(x, str | int | float | bool | type(None)) for x in arr):
            values = self._delimiter.join(self._encode_value(x) for x in arr)
            return f"[{len(arr)}]: {values}"

        # Fall back to list format
        return self._encode_list_array(arr, depth)

    def _encode_tabular_array(self, arr: list[dict[str, Any]], depth: int) -> str:
        """Encode as tabular array (TOON's main optimization)."""
        fields = list(arr[0].keys())
        header = f"[{len(arr)}]{{{self._delimiter.join(fields)}}}:"

        indent = " " * (self._indent * (depth + 1))
        rows = []
        for item in arr:
            row_values = [self._encode_value(item[f]) for f in fields]
            rows.append(indent + self._delimiter.join(row_values))

        return header + "\n" + "\n".join(rows)

    def _encode_list_array(self, arr: list[Any], depth: int) -> str:
        """Encode as list format (non-uniform arrays)."""
        lines = [f"[{len(arr)}]:"]
        indent = " " * (self._indent * (depth + 1))

        for item in arr:
            if isinstance(item, dict):
                obj_lines = self._encode_object(item, depth + 1).split("\n")
                lines.append(f"{indent}- {obj_lines[0]}")
                lines.extend(f"{indent}  {line}" for line in obj_lines[1:] if line)
            elif isinstance(item, list):
                arr_encoded = self._encode_array(item, depth + 1)
                lines.append(f"{indent}- {arr_encoded}")
            else:
                lines.append(f"{indent}- {self._encode_value(item)}")

        return "\n".join(lines)

    def _encode_object(self, obj: dict[str, Any], depth: int) -> str:
        """Encode object with proper indentation."""
        if not obj:
            return ""

        lines = []
        indent = " " * (self._indent * depth)

        for key, value in obj.items():
            if isinstance(value, dict) and value:
                lines.append(f"{indent}{key}:")
                nested = self._encode_object(value, depth + 1)
                if nested:
                    lines.append(nested)
            elif isinstance(value, list):
                arr_encoded = self._encode_array(value, depth)
                if "\n" in arr_encoded:
                    # Multi-line array
                    lines.append(f"{indent}{key}{arr_encoded}")
                else:
                    lines.append(f"{indent}{key}{arr_encoded}")
            else:
                lines.append(f"{indent}{key}: {self._encode_value(value)}")

        return "\n".join(lines)

    def _quote_if_needed(self, s: str) -> str:
        """Quote string if it contains special characters."""
        if not s:
            return '""'

        needs_quote = (
            s in ("true", "false", "null")
            or s.startswith(" ")
            or s.endswith(" ")
            or s == "-"
            or s.startswith("-")
            or any(c in s for c in ':"\\[]{}\n\t\r' + self._delimiter)
            or self._looks_numeric(s)
        )

        if needs_quote:
            escaped = s.replace("\\", "\\\\").replace('"', '\\"')
            escaped = escaped.replace("\n", "\\n").replace("\r", "\\r").replace("\t", "\\t")
            return f'"{escaped}"'

        return s

    def _looks_numeric(self, s: str) -> bool:
        """Check if string looks like a number."""
        try:
            float(s)
            return True
        except ValueError:
            return False

    # =========================================================================
    # Private: TOON Decoding
    # =========================================================================

    def _decode_toon(self, text: str) -> Any:
        """Decode TOON format to Python data."""
        stripped = text.strip()
        if not stripped:
            return {}
        lines = stripped.splitlines()

        # Check for tabular array
        first_line = lines[0].strip()
        if first_line.startswith("[") and "]{" in first_line:
            return self._decode_tabular_array(lines)

        # Check for simple array
        if first_line.startswith("[") and first_line.endswith(":"):
            return self._decode_list_array(lines)

        # Check for primitive array
        if first_line.startswith("[") and "]: " in first_line:
            return self._decode_primitive_array(first_line)

        # Object
        return self._decode_object(lines, 0)[0]

    def _decode_tabular_array(self, lines: list[str]) -> list[dict[str, Any]]:
        """Decode tabular array format."""
        header = lines[0].strip()
        # Parse [N]{field1,field2,...}:
        fields_start = header.index("{") + 1
        fields_end = header.index("}")

        fields = header[fields_start:fields_end].split(self._delimiter)

        result = []
        for line in lines[1:]:
            stripped = line.strip()
            if not stripped:
                continue
            values = stripped.split(self._delimiter)
            item = {}
            for i, field in enumerate(fields):
                if i < len(values):
                    item[field] = self._decode_value(values[i])
            result.append(item)

        return result

    def _decode_primitive_array(self, line: str) -> list[Any]:
        """Decode inline primitive array."""
        # Format: [N]: value1,value2,...
        parts = line.split("]: ", 1)
        if len(parts) != 2:
            return []
        values_str = parts[1]
        if not values_str:
            return []
        return [self._decode_value(v) for v in values_str.split(self._delimiter)]

    def _decode_list_array(self, lines: list[str]) -> list[Any]:
        """Decode list format array."""
        result = []
        i = 1
        while i < len(lines):
            line = lines[i]
            stripped = line.strip()
            if stripped.startswith("- "):
                value_str = stripped[2:]
                result.append(self._decode_value(value_str))
            i += 1
        return result

    def _decode_object(
        self,
        lines: list[str],
        start_index: int,
    ) -> tuple[dict[str, Any], int]:
        """Decode object from lines."""
        result = {}
        i = start_index

        while i < len(lines):
            line = lines[i]
            if not line.strip():
                i += 1
                continue

            # Find key: value
            if ": " in line:
                key, value_str = line.split(": ", 1)
                key = key.strip()
                result[key] = self._decode_value(value_str.strip())
            elif line.strip().endswith(":"):
                # Nested object or array - simplified handling
                key = line.strip()[:-1]
                result[key] = {}

            i += 1

        return result, i

    def _decode_value(self, s: str) -> Any:
        """Decode a TOON value to Python."""
        s = s.strip()

        if not s or s == "null":
            return None
        if s == "true":
            return True
        if s == "false":
            return False

        # Quoted string
        if s.startswith('"') and s.endswith('"'):
            inner = s[1:-1]
            return inner.replace("\\n", "\n").replace("\\t", "\t").replace('\\"', '"')

        # Try numeric
        try:
            if "." in s:
                return float(s)
            return int(s)
        except ValueError:
            pass

        return s

    # =========================================================================
    # Private: Human-readable Encoding
    # =========================================================================

    def _encode_human(self, data: Any, depth: int = 0) -> str:
        """Encode data to human-readable format."""
        indent = "  " * depth

        if isinstance(data, dict):
            if not data:
                return f"{indent}(empty)"
            lines = []
            for key, value in data.items():
                if isinstance(value, dict | list):
                    lines.append(f"{indent}{key}:")
                    lines.append(self._encode_human(value, depth + 1))
                else:
                    lines.append(f"{indent}{key}: {value}")
            return "\n".join(lines)

        elif isinstance(data, list):
            if not data:
                return f"{indent}(no items)"
            lines = []
            for i, item in enumerate(data, 1):
                if isinstance(item, dict):
                    lines.append(f"{indent}{i}.")
                    lines.append(self._encode_human(item, depth + 1))
                else:
                    lines.append(f"{indent}{i}. {item}")
            return "\n".join(lines)

        else:
            return f"{indent}{data}"
