# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
ISerializer - Serialization Abstraction.

Internal abstraction for serialization used by repository adapters.
Provides serialize/deserialize operations with type safety.

References:
    - PAT-005: TOON for LLM Context Serialization
    - PAT-010: Composed Infrastructure Adapters
"""

from __future__ import annotations

import json
from dataclasses import asdict, is_dataclass
from datetime import datetime
from typing import Any, Generic, Protocol, TypeVar, get_type_hints, runtime_checkable

T = TypeVar("T")
T_co = TypeVar("T_co", covariant=True)


@runtime_checkable
class HasToDict(Protocol):
    """Protocol for objects with to_dict method.

    Enables pyright to narrow types after isinstance() check.
    This is necessary because hasattr() is a runtime check that
    type checkers cannot use for narrowing.
    """

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary representation."""
        ...


class SerializerError(Exception):
    """Base exception for serialization operations."""


class SerializeError(SerializerError):
    """Failed to serialize object."""

    def __init__(self, obj_type: type, reason: str) -> None:
        super().__init__(f"Failed to serialize {obj_type.__name__}: {reason}")
        self.obj_type = obj_type
        self.reason = reason


class DeserializeError(SerializerError):
    """Failed to deserialize data."""

    def __init__(self, target_type: type, reason: str) -> None:
        super().__init__(f"Failed to deserialize to {target_type.__name__}: {reason}")
        self.target_type = target_type
        self.reason = reason


class ISerializer(Protocol[T_co]):
    """Protocol for serialization.

    This is an internal abstraction used by repository adapters.
    It provides type-safe serialization and deserialization.

    Type Parameters:
        T_co: The type being serialized/deserialized (covariant)

    Implementations:
        - JsonSerializer: JSON format (default)
        - ToonSerializer: TOON format (for LLM context)

    Example:
        >>> serializer = JsonSerializer[User]()
        >>> data = serializer.serialize(user)
        >>> user_copy = serializer.deserialize(data, User)
    """

    def serialize(self, obj: Any) -> bytes:
        """Serialize object to bytes.

        Args:
            obj: Object to serialize

        Returns:
            Serialized bytes

        Raises:
            SerializeError: If serialization fails
        """
        ...

    def deserialize(self, data: bytes, target_type: type[T]) -> T:
        """Deserialize bytes to object.

        Args:
            data: Bytes to deserialize
            target_type: Type to deserialize into

        Returns:
            Deserialized object of target_type

        Raises:
            DeserializeError: If deserialization fails
        """
        ...


class JsonSerializer(Generic[T]):
    """JSON implementation of ISerializer.

    Handles dataclasses, dicts, and basic types.
    Supports datetime serialization in ISO format.

    Attributes:
        indent: JSON indentation (None for compact, 2 for pretty)
        ensure_ascii: Whether to escape non-ASCII characters

    Example:
        >>> from dataclasses import dataclass
        >>> @dataclass
        ... class User:
        ...     name: str
        ...     age: int
        >>> serializer = JsonSerializer[User](indent=2)
        >>> data = serializer.serialize(User("Alice", 30))
        >>> serializer.deserialize(data, User)
        User(name='Alice', age=30)
    """

    def __init__(
        self,
        *,
        indent: int | None = None,
        ensure_ascii: bool = False,
    ) -> None:
        """Initialize JsonSerializer.

        Args:
            indent: JSON indentation (None for compact)
            ensure_ascii: Whether to escape non-ASCII (default False)
        """
        self._indent = indent
        self._ensure_ascii = ensure_ascii

    def serialize(self, obj: Any) -> bytes:
        """Serialize object to JSON bytes."""
        try:
            if is_dataclass(obj) and not isinstance(obj, type):
                data = asdict(obj)
            elif isinstance(obj, HasToDict):
                data = obj.to_dict()
            else:
                data = obj

            json_str = json.dumps(
                data,
                indent=self._indent,
                ensure_ascii=self._ensure_ascii,
                default=self._json_default,
            )
            return json_str.encode("utf-8")

        except (TypeError, ValueError) as e:
            raise SerializeError(type(obj), str(e)) from e

    def deserialize(self, data: bytes, target_type: type[T]) -> T:
        """Deserialize JSON bytes to object."""
        try:
            json_data = json.loads(data.decode("utf-8"))

            if is_dataclass(target_type):
                return self._from_dict(json_data, target_type)
            elif hasattr(target_type, "from_dict"):
                return target_type.from_dict(json_data)  # type: ignore[attr-defined, no-any-return]
            else:
                return json_data  # type: ignore[no-any-return]

        except (json.JSONDecodeError, UnicodeDecodeError) as e:
            raise DeserializeError(target_type, str(e)) from e
        except (TypeError, KeyError) as e:
            raise DeserializeError(target_type, f"Invalid structure: {e}") from e

    def _json_default(self, obj: Any) -> Any:
        """Default JSON encoder for custom types."""
        if isinstance(obj, datetime):
            return obj.isoformat()
        if is_dataclass(obj) and not isinstance(obj, type):
            return asdict(obj)
        if isinstance(obj, HasToDict):
            return obj.to_dict()
        if hasattr(obj, "__dict__"):
            return obj.__dict__
        raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")

    def _from_dict(self, data: dict[str, Any], target_type: type[T]) -> T:
        """Reconstruct dataclass from dictionary."""
        if not is_dataclass(target_type):
            raise DeserializeError(target_type, "Target must be a dataclass")

        # Get type hints for datetime conversion
        hints = get_type_hints(target_type)

        # Convert datetime strings back to datetime objects
        converted = {}
        for key, value in data.items():
            if key in hints:
                hint = hints[key]
                if hint is datetime and isinstance(value, str):
                    converted[key] = datetime.fromisoformat(value)
                else:
                    converted[key] = value
            else:
                converted[key] = value

        return target_type(**converted)


class InMemorySerializer(Generic[T]):
    """In-memory serializer for testing.

    Simply stores objects as-is (no actual serialization).
    Useful for unit tests where serialization overhead should be avoided.
    """

    def serialize(self, obj: Any) -> bytes:
        """Return object repr as bytes (for testing)."""
        return repr(obj).encode("utf-8")

    def deserialize(self, data: bytes, target_type: type[T]) -> T:
        """This is a test double - raises if actually called with real data."""
        _ = data  # Unused, but required by protocol
        raise DeserializeError(target_type, "InMemorySerializer cannot deserialize real data")
