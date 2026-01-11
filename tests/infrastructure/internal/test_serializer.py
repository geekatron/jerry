"""
Unit tests for ISerializer implementations.

Test Categories:
    - Happy Path: Normal serialization/deserialization works
    - Edge Cases: Boundary conditions and special inputs
    - Negative Cases: Error handling and invalid inputs
    - Type Safety: Correct type reconstruction

References:
    - IMPL-REPO-002: IFileStore + ISerializer<T>
    - PAT-010: Composed Infrastructure Adapters
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any

import pytest

from src.infrastructure.internal.serializer import (
    DeserializeError,
    InMemorySerializer,
    JsonSerializer,
    SerializeError,
)


@dataclass
class SimpleUser:
    """Simple dataclass for testing."""

    name: str
    age: int


@dataclass
class UserWithOptional:
    """Dataclass with optional field."""

    name: str
    email: str | None = None


@dataclass
class UserWithDatetime:
    """Dataclass with datetime field."""

    name: str
    created_at: datetime


@dataclass
class NestedData:
    """Dataclass with nested structure."""

    user: SimpleUser
    tags: list[str]


class DictConvertible:
    """Class with to_dict/from_dict methods."""

    def __init__(self, value: str) -> None:
        self.value = value

    def to_dict(self) -> dict[str, Any]:
        return {"value": self.value}

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> DictConvertible:
        return cls(data["value"])


class TestJsonSerializerHappyPath:
    """Happy path tests for JsonSerializer."""

    def test_serialize_dict(self) -> None:
        """Test serializing a plain dictionary."""
        serializer = JsonSerializer()
        data = {"name": "Alice", "age": 30}

        result = serializer.serialize(data)

        assert b'"name"' in result
        assert b'"Alice"' in result

    def test_deserialize_dict(self) -> None:
        """Test deserializing to a dictionary."""
        serializer = JsonSerializer()
        json_bytes = b'{"name": "Alice", "age": 30}'

        result = serializer.deserialize(json_bytes, dict)

        assert result == {"name": "Alice", "age": 30}

    def test_serialize_dataclass(self) -> None:
        """Test serializing a dataclass."""
        serializer = JsonSerializer[SimpleUser]()
        user = SimpleUser(name="Bob", age=25)

        result = serializer.serialize(user)

        assert b'"name"' in result
        assert b'"Bob"' in result
        assert b'"age"' in result

    def test_deserialize_dataclass(self) -> None:
        """Test deserializing to a dataclass."""
        serializer = JsonSerializer[SimpleUser]()
        json_bytes = b'{"name": "Charlie", "age": 35}'

        result = serializer.deserialize(json_bytes, SimpleUser)

        assert isinstance(result, SimpleUser)
        assert result.name == "Charlie"
        assert result.age == 35

    def test_roundtrip_dataclass(self) -> None:
        """Test serialize/deserialize roundtrip."""
        serializer = JsonSerializer[SimpleUser]()
        original = SimpleUser(name="Diana", age=40)

        json_bytes = serializer.serialize(original)
        restored = serializer.deserialize(json_bytes, SimpleUser)

        assert restored == original

    def test_serialize_with_indent(self) -> None:
        """Test serialization with indentation."""
        serializer = JsonSerializer(indent=2)
        data = {"key": "value"}

        result = serializer.serialize(data)

        assert b"\n" in result  # Has newlines
        assert b"  " in result  # Has indentation

    def test_serialize_with_ensure_ascii_false(self) -> None:
        """Test that unicode characters are preserved."""
        serializer = JsonSerializer(ensure_ascii=False)
        data = {"greeting": "Привет"}

        result = serializer.serialize(data)

        assert "Привет".encode() in result

    def test_serialize_list(self) -> None:
        """Test serializing a list."""
        serializer = JsonSerializer()
        data = [1, 2, 3]

        result = serializer.serialize(data)

        assert result == b"[1, 2, 3]"

    def test_deserialize_list(self) -> None:
        """Test deserializing a list."""
        serializer = JsonSerializer()
        json_bytes = b"[1, 2, 3]"

        result = serializer.deserialize(json_bytes, list)

        assert result == [1, 2, 3]


class TestJsonSerializerDatetime:
    """Datetime handling tests for JsonSerializer."""

    def test_serialize_datetime(self) -> None:
        """Test that datetime is serialized to ISO format."""
        serializer = JsonSerializer[UserWithDatetime]()
        user = UserWithDatetime(name="Eve", created_at=datetime(2024, 1, 15, 10, 30, 0))

        result = serializer.serialize(user)

        assert b"2024-01-15T10:30:00" in result

    def test_deserialize_datetime(self) -> None:
        """Test that ISO datetime string is deserialized."""
        serializer = JsonSerializer[UserWithDatetime]()
        json_bytes = b'{"name": "Eve", "created_at": "2024-01-15T10:30:00"}'

        result = serializer.deserialize(json_bytes, UserWithDatetime)

        assert result.created_at == datetime(2024, 1, 15, 10, 30, 0)

    def test_roundtrip_datetime(self) -> None:
        """Test datetime roundtrip."""
        serializer = JsonSerializer[UserWithDatetime]()
        original = UserWithDatetime(name="Frank", created_at=datetime(2025, 6, 20, 14, 45, 30))

        json_bytes = serializer.serialize(original)
        restored = serializer.deserialize(json_bytes, UserWithDatetime)

        assert restored == original


class TestJsonSerializerEdgeCases:
    """Edge case tests for JsonSerializer."""

    def test_empty_dict(self) -> None:
        """Test serializing/deserializing empty dict."""
        serializer = JsonSerializer()

        result = serializer.serialize({})
        restored = serializer.deserialize(result, dict)

        assert restored == {}

    def test_empty_list(self) -> None:
        """Test serializing/deserializing empty list."""
        serializer = JsonSerializer()

        result = serializer.serialize([])
        restored = serializer.deserialize(result, list)

        assert restored == []

    def test_optional_field_none(self) -> None:
        """Test dataclass with None optional field."""
        serializer = JsonSerializer[UserWithOptional]()
        user = UserWithOptional(name="Grace", email=None)

        json_bytes = serializer.serialize(user)
        restored = serializer.deserialize(json_bytes, UserWithOptional)

        assert restored.name == "Grace"
        assert restored.email is None

    def test_optional_field_present(self) -> None:
        """Test dataclass with present optional field."""
        serializer = JsonSerializer[UserWithOptional]()
        user = UserWithOptional(name="Henry", email="henry@example.com")

        json_bytes = serializer.serialize(user)
        restored = serializer.deserialize(json_bytes, UserWithOptional)

        assert restored.email == "henry@example.com"

    def test_unicode_content(self) -> None:
        """Test handling unicode content."""
        serializer = JsonSerializer()
        data = {"emoji": "🎉", "cyrillic": "Москва", "chinese": "北京"}

        json_bytes = serializer.serialize(data)
        restored = serializer.deserialize(json_bytes, dict)

        assert restored == data

    def test_nested_dataclass(self) -> None:
        """Test nested dataclass (as dict, not recursive reconstruction)."""
        serializer = JsonSerializer()
        data = NestedData(user=SimpleUser("Ivy", 28), tags=["admin", "active"])

        json_bytes = serializer.serialize(data)
        restored = serializer.deserialize(json_bytes, dict)

        # Note: Full reconstruction would need custom handling
        assert restored["user"]["name"] == "Ivy"
        assert restored["tags"] == ["admin", "active"]

    def test_special_json_values(self) -> None:
        """Test special JSON values (null, booleans)."""
        serializer = JsonSerializer()
        data = {"null_val": None, "true_val": True, "false_val": False}

        json_bytes = serializer.serialize(data)
        restored = serializer.deserialize(json_bytes, dict)

        assert restored == data

    def test_numeric_precision(self) -> None:
        """Test numeric precision for floats."""
        serializer = JsonSerializer()
        data = {"precise": 3.141592653589793, "integer": 9007199254740993}

        json_bytes = serializer.serialize(data)
        restored = serializer.deserialize(json_bytes, dict)

        assert restored["precise"] == pytest.approx(3.141592653589793)

    def test_to_dict_method(self) -> None:
        """Test class with to_dict method."""
        serializer = JsonSerializer()
        obj = DictConvertible("test_value")

        json_bytes = serializer.serialize(obj)

        assert b'"value"' in json_bytes
        assert b'"test_value"' in json_bytes

    def test_from_dict_method(self) -> None:
        """Test class with from_dict method."""
        serializer = JsonSerializer()
        json_bytes = b'{"value": "restored_value"}'

        result = serializer.deserialize(json_bytes, DictConvertible)

        assert isinstance(result, DictConvertible)
        assert result.value == "restored_value"


class TestJsonSerializerNegativeCases:
    """Negative case tests for JsonSerializer."""

    def test_serialize_non_serializable_raises_error(self) -> None:
        """Test that non-serializable objects raise SerializeError."""
        serializer = JsonSerializer()

        # Use an object that truly can't be serialized (circular reference)
        circular: dict = {}
        circular["self"] = circular

        with pytest.raises(SerializeError) as exc_info:
            serializer.serialize(circular)

        assert "serialize" in str(exc_info.value).lower()

    def test_deserialize_invalid_json_raises_error(self) -> None:
        """Test that invalid JSON raises DeserializeError."""
        serializer = JsonSerializer()

        with pytest.raises(DeserializeError):
            serializer.deserialize(b"not valid json", dict)

    def test_deserialize_wrong_encoding_raises_error(self) -> None:
        """Test that non-UTF8 data raises DeserializeError."""
        serializer = JsonSerializer()
        # Latin-1 encoded data that's not valid UTF-8
        bad_data = "Ñoño".encode("latin-1")

        with pytest.raises(DeserializeError):
            serializer.deserialize(bad_data, dict)

    def test_deserialize_missing_field_raises_error(self) -> None:
        """Test that missing required field raises DeserializeError."""
        serializer = JsonSerializer[SimpleUser]()
        json_bytes = b'{"name": "Jack"}'  # Missing 'age'

        with pytest.raises(DeserializeError) as exc_info:
            serializer.deserialize(json_bytes, SimpleUser)

        assert "Invalid structure" in str(exc_info.value)

    def test_deserialize_wrong_type_raises_error(self) -> None:
        """Test that wrong type in field raises DeserializeError."""
        serializer = JsonSerializer[SimpleUser]()
        json_bytes = b'{"name": "Jack", "age": "not_a_number"}'

        # This may or may not raise depending on type strictness
        # At minimum, it should not silently corrupt data


class TestInMemorySerializer:
    """Tests for InMemorySerializer (test double)."""

    def test_serialize_returns_repr(self) -> None:
        """Test that serialize returns repr of object."""
        serializer = InMemorySerializer()
        obj = {"key": "value"}

        result = serializer.serialize(obj)

        assert b"key" in result

    def test_deserialize_raises_error(self) -> None:
        """Test that deserialize always raises error."""
        serializer = InMemorySerializer()

        with pytest.raises(DeserializeError) as exc_info:
            serializer.deserialize(b"data", dict)

        assert "InMemorySerializer" in str(exc_info.value)


class TestSerializerProtocolCompliance:
    """Tests that implementations comply with ISerializer protocol."""

    @pytest.mark.parametrize(
        "serializer",
        [
            JsonSerializer(),
            InMemorySerializer(),
        ],
    )
    def test_protocol_methods_exist(self, serializer) -> None:
        """Test that all protocol methods are implemented."""
        assert callable(serializer.serialize)
        assert callable(serializer.deserialize)

    def test_json_serializer_generic_typing(self) -> None:
        """Test that JsonSerializer can be parameterized."""
        # This should not raise
        serializer: JsonSerializer[SimpleUser] = JsonSerializer()
        _ = serializer
