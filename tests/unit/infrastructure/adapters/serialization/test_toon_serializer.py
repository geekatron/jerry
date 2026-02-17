# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Unit tests for ToonSerializer.

Tests cover TOON format encoding/decoding, format detection,
tabular eligibility, and edge cases.

References:
    - impl-es-e-002-toon-serialization.md: TOON research
    - DISC-012: TOON Format Required as Primary Output
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime

import pytest

from src.application.ports.secondary.illm_context_serializer import OutputFormat
from src.infrastructure.adapters.serialization.toon_serializer import (
    DeserializationError,
    ToonSerializer,
)

# =============================================================================
# Test Fixtures
# =============================================================================


@pytest.fixture
def serializer() -> ToonSerializer:
    """Create a ToonSerializer instance."""
    return ToonSerializer()


@pytest.fixture
def tabular_data() -> list[dict]:
    """Sample data eligible for tabular format."""
    return [
        {"id": 1, "name": "Task A", "status": "pending"},
        {"id": 2, "name": "Task B", "status": "done"},
        {"id": 3, "name": "Task C", "status": "blocked"},
    ]


@pytest.fixture
def nested_data() -> dict:
    """Sample nested object data."""
    return {
        "project": "jerry",
        "version": "0.1.0",
        "config": {
            "debug": True,
            "timeout": 30,
        },
    }


# =============================================================================
# Tabular Eligibility Tests
# =============================================================================


class TestTabularEligibility:
    """Tests for is_tabular_eligible method."""

    def test_is_tabular_eligible_when_uniform_array_then_returns_true(
        self,
        serializer: ToonSerializer,
        tabular_data: list[dict],
    ) -> None:
        """Uniform dict arrays are tabular eligible."""
        assert serializer.is_tabular_eligible(tabular_data) is True

    def test_is_tabular_eligible_when_single_item_then_returns_false(
        self,
        serializer: ToonSerializer,
    ) -> None:
        """Single-item arrays are not tabular eligible."""
        data = [{"id": 1, "name": "Only one"}]
        assert serializer.is_tabular_eligible(data) is False

    def test_is_tabular_eligible_when_empty_array_then_returns_false(
        self,
        serializer: ToonSerializer,
    ) -> None:
        """Empty arrays are not tabular eligible."""
        assert serializer.is_tabular_eligible([]) is False

    def test_is_tabular_eligible_when_not_list_then_returns_false(
        self,
        serializer: ToonSerializer,
    ) -> None:
        """Non-list data is not tabular eligible."""
        assert serializer.is_tabular_eligible({"a": 1}) is False
        assert serializer.is_tabular_eligible("string") is False
        assert serializer.is_tabular_eligible(42) is False

    def test_is_tabular_eligible_when_different_keys_then_returns_false(
        self,
        serializer: ToonSerializer,
    ) -> None:
        """Arrays with different keys are not tabular eligible."""
        data = [
            {"id": 1, "name": "A"},
            {"id": 2, "title": "B"},  # Different key
        ]
        assert serializer.is_tabular_eligible(data) is False

    def test_is_tabular_eligible_when_nested_values_then_returns_false(
        self,
        serializer: ToonSerializer,
    ) -> None:
        """Arrays with nested values are not tabular eligible."""
        data = [
            {"id": 1, "config": {"nested": True}},
            {"id": 2, "config": {"nested": False}},
        ]
        assert serializer.is_tabular_eligible(data) is False

    def test_is_tabular_eligible_when_primitive_array_then_returns_false(
        self,
        serializer: ToonSerializer,
    ) -> None:
        """Primitive arrays are not tabular eligible (different format)."""
        data = [1, 2, 3, 4, 5]
        assert serializer.is_tabular_eligible(data) is False


# =============================================================================
# TOON Serialization Tests
# =============================================================================


class TestToonSerialization:
    """Tests for TOON format serialization."""

    def test_serialize_when_tabular_array_then_produces_tabular_format(
        self,
        serializer: ToonSerializer,
        tabular_data: list[dict],
    ) -> None:
        """Tabular arrays produce header + row format."""
        result = serializer.serialize(tabular_data, OutputFormat.TOON)

        # Should have header with count and fields
        assert result.startswith("[3]{id,name,status}:")
        # Should have rows
        assert "1,Task A,pending" in result
        assert "2,Task B,done" in result
        assert "3,Task C,blocked" in result

    def test_serialize_when_primitive_array_then_produces_inline_format(
        self,
        serializer: ToonSerializer,
    ) -> None:
        """Primitive arrays produce inline format."""
        data = [1, 2, 3, 4, 5]
        result = serializer.serialize(data, OutputFormat.TOON)

        assert result == "[5]: 1,2,3,4,5"

    def test_serialize_when_empty_array_then_produces_empty_marker(
        self,
        serializer: ToonSerializer,
    ) -> None:
        """Empty arrays produce [0]: marker."""
        result = serializer.serialize([], OutputFormat.TOON)
        assert result == "[0]:"

    def test_serialize_when_object_then_produces_key_value_format(
        self,
        serializer: ToonSerializer,
        nested_data: dict,
    ) -> None:
        """Objects produce key: value format."""
        result = serializer.serialize(nested_data, OutputFormat.TOON)

        assert "project: jerry" in result
        assert "version: 0.1.0" in result
        assert "config:" in result
        assert "debug: true" in result
        assert "timeout: 30" in result

    def test_serialize_when_null_values_then_produces_null_literal(
        self,
        serializer: ToonSerializer,
    ) -> None:
        """None values become 'null' literal."""
        data = {"name": "test", "value": None}
        result = serializer.serialize(data, OutputFormat.TOON)

        assert "value: null" in result

    def test_serialize_when_boolean_values_then_produces_lowercase(
        self,
        serializer: ToonSerializer,
    ) -> None:
        """Booleans become lowercase true/false."""
        data = {"enabled": True, "disabled": False}
        result = serializer.serialize(data, OutputFormat.TOON)

        assert "enabled: true" in result
        assert "disabled: false" in result

    def test_serialize_when_string_with_special_chars_then_quotes_string(
        self,
        serializer: ToonSerializer,
    ) -> None:
        """Strings with special characters are quoted."""
        data = {"message": "Hello, World!"}  # Contains comma
        result = serializer.serialize(data, OutputFormat.TOON)

        assert '"Hello, World!"' in result

    def test_serialize_when_string_looks_like_number_then_quotes_string(
        self,
        serializer: ToonSerializer,
    ) -> None:
        """Numeric-looking strings are quoted."""
        data = {"code": "123"}
        result = serializer.serialize(data, OutputFormat.TOON)

        assert '"123"' in result

    def test_serialize_when_empty_string_then_quotes_string(
        self,
        serializer: ToonSerializer,
    ) -> None:
        """Empty strings produce empty quotes."""
        data = {"empty": ""}
        result = serializer.serialize(data, OutputFormat.TOON)

        assert 'empty: ""' in result

    def test_serialize_when_dataclass_then_converts_to_dict(
        self,
        serializer: ToonSerializer,
    ) -> None:
        """Dataclasses are normalized to dicts."""

        @dataclass
        class Task:
            id: int
            name: str

        task = Task(id=1, name="Test")
        result = serializer.serialize(task, OutputFormat.TOON)

        assert "id: 1" in result
        assert "name: Test" in result

    def test_serialize_when_datetime_then_converts_to_iso_format(
        self,
        serializer: ToonSerializer,
    ) -> None:
        """Datetimes are normalized to ISO format."""
        dt = datetime(2024, 1, 15, 10, 30, 0, tzinfo=UTC)
        data = {"created_at": dt}
        result = serializer.serialize(data, OutputFormat.TOON)

        assert "2024-01-15T10:30:00" in result

    def test_serialize_when_mixed_array_then_uses_list_format(
        self,
        serializer: ToonSerializer,
    ) -> None:
        """Non-uniform arrays use list format with bullets."""
        data = [
            {"type": "task", "data": {"id": 1}},
            {"type": "event", "data": {"id": 2}},
        ]
        result = serializer.serialize(data, OutputFormat.TOON)

        assert "[2]:" in result
        assert "-" in result  # Has bullet markers
        assert "type: task" in result


# =============================================================================
# JSON Serialization Tests
# =============================================================================


class TestJsonSerialization:
    """Tests for JSON format serialization."""

    def test_serialize_when_json_format_then_produces_valid_json(
        self,
        serializer: ToonSerializer,
        tabular_data: list[dict],
    ) -> None:
        """JSON format produces valid JSON output."""
        import json

        result = serializer.serialize(tabular_data, OutputFormat.JSON)
        parsed = json.loads(result)

        assert len(parsed) == 3
        assert parsed[0]["id"] == 1

    def test_serialize_when_json_format_then_is_indented(
        self,
        serializer: ToonSerializer,
    ) -> None:
        """JSON output is indented for readability."""
        data = {"key": "value"}
        result = serializer.serialize(data, OutputFormat.JSON)

        assert "  " in result  # Has indentation


# =============================================================================
# Human Format Tests
# =============================================================================


class TestHumanSerialization:
    """Tests for human-readable format serialization."""

    def test_serialize_when_human_format_then_produces_readable_output(
        self,
        serializer: ToonSerializer,
    ) -> None:
        """Human format is readable with numbered lists."""
        data = [{"name": "Task 1"}, {"name": "Task 2"}]
        result = serializer.serialize(data, OutputFormat.HUMAN)

        assert "1." in result
        assert "2." in result
        assert "name: Task 1" in result

    def test_serialize_when_human_empty_dict_then_shows_empty_marker(
        self,
        serializer: ToonSerializer,
    ) -> None:
        """Empty dicts show (empty) marker."""
        result = serializer.serialize({}, OutputFormat.HUMAN)
        assert "(empty)" in result

    def test_serialize_when_human_empty_list_then_shows_no_items(
        self,
        serializer: ToonSerializer,
    ) -> None:
        """Empty lists show (no items) marker."""
        result = serializer.serialize([], OutputFormat.HUMAN)
        assert "(no items)" in result


# =============================================================================
# TOON Deserialization Tests
# =============================================================================


class TestToonDeserialization:
    """Tests for TOON format deserialization."""

    def test_deserialize_when_tabular_format_then_returns_list_of_dicts(
        self,
        serializer: ToonSerializer,
    ) -> None:
        """Tabular format deserializes to list of dicts."""
        text = "[2]{id,name}:\n  1,Alpha\n  2,Beta"
        result = serializer.deserialize(text, OutputFormat.TOON)

        assert len(result) == 2
        assert result[0]["id"] == 1
        assert result[0]["name"] == "Alpha"
        assert result[1]["id"] == 2
        assert result[1]["name"] == "Beta"

    def test_deserialize_when_primitive_array_then_returns_list(
        self,
        serializer: ToonSerializer,
    ) -> None:
        """Primitive array format deserializes to list."""
        text = "[3]: 10,20,30"
        result = serializer.deserialize(text, OutputFormat.TOON)

        assert result == [10, 20, 30]

    def test_deserialize_when_object_format_then_returns_dict(
        self,
        serializer: ToonSerializer,
    ) -> None:
        """Object format deserializes to dict."""
        text = "name: test\nvalue: 42"
        result = serializer.deserialize(text, OutputFormat.TOON)

        assert result["name"] == "test"
        assert result["value"] == 42

    def test_deserialize_when_empty_text_then_returns_empty_dict(
        self,
        serializer: ToonSerializer,
    ) -> None:
        """Empty text deserializes to empty dict."""
        result = serializer.deserialize("", OutputFormat.TOON)
        assert result == {}

    def test_deserialize_when_null_literal_then_returns_none(
        self,
        serializer: ToonSerializer,
    ) -> None:
        """'null' literal deserializes to None."""
        text = "value: null"
        result = serializer.deserialize(text, OutputFormat.TOON)
        assert result["value"] is None

    def test_deserialize_when_boolean_literals_then_returns_booleans(
        self,
        serializer: ToonSerializer,
    ) -> None:
        """'true'/'false' literals deserialize to booleans."""
        text = "enabled: true\ndisabled: false"
        result = serializer.deserialize(text, OutputFormat.TOON)

        assert result["enabled"] is True
        assert result["disabled"] is False

    def test_deserialize_when_quoted_string_then_unquotes(
        self,
        serializer: ToonSerializer,
    ) -> None:
        """Quoted strings are unquoted."""
        text = 'message: "Hello, World!"'
        result = serializer.deserialize(text, OutputFormat.TOON)

        assert result["message"] == "Hello, World!"


# =============================================================================
# JSON Deserialization Tests
# =============================================================================


class TestJsonDeserialization:
    """Tests for JSON format deserialization."""

    def test_deserialize_when_valid_json_then_returns_parsed(
        self,
        serializer: ToonSerializer,
    ) -> None:
        """Valid JSON deserializes correctly."""
        text = '{"name": "test", "value": 42}'
        result = serializer.deserialize(text, OutputFormat.JSON)

        assert result["name"] == "test"
        assert result["value"] == 42

    def test_deserialize_when_invalid_json_then_raises_error(
        self,
        serializer: ToonSerializer,
    ) -> None:
        """Invalid JSON raises DeserializationError."""
        with pytest.raises(DeserializationError):
            serializer.deserialize("{invalid}", OutputFormat.JSON)


# =============================================================================
# Human Format Deserialization Tests
# =============================================================================


class TestHumanDeserialization:
    """Tests for human format deserialization."""

    def test_deserialize_when_human_format_then_raises_error(
        self,
        serializer: ToonSerializer,
    ) -> None:
        """Human format is not deserializable."""
        with pytest.raises(DeserializationError) as exc_info:
            serializer.deserialize("some text", OutputFormat.HUMAN)

        assert "cannot be deserialized" in str(exc_info.value)


# =============================================================================
# Format Detection Tests
# =============================================================================


class TestFormatDetection:
    """Tests for detect_format method."""

    def test_detect_format_when_json_object_then_returns_json(
        self,
        serializer: ToonSerializer,
    ) -> None:
        """JSON objects are detected as JSON."""
        text = '{"key": "value"}'
        assert serializer.detect_format(text) == OutputFormat.JSON

    def test_detect_format_when_json_array_then_returns_json(
        self,
        serializer: ToonSerializer,
    ) -> None:
        """JSON arrays are detected as JSON."""
        text = "[1, 2, 3]"
        assert serializer.detect_format(text) == OutputFormat.JSON

    def test_detect_format_when_toon_tabular_then_returns_toon(
        self,
        serializer: ToonSerializer,
    ) -> None:
        """TOON tabular format is detected as TOON."""
        text = "[2]{id,name}:\n  1,Test"
        assert serializer.detect_format(text) == OutputFormat.TOON

    def test_detect_format_when_toon_object_then_returns_toon(
        self,
        serializer: ToonSerializer,
    ) -> None:
        """TOON object format is detected as TOON."""
        text = "name: test\nvalue: 42"
        assert serializer.detect_format(text) == OutputFormat.TOON

    def test_detect_format_when_plain_text_then_returns_human(
        self,
        serializer: ToonSerializer,
    ) -> None:
        """Plain text defaults to HUMAN format."""
        text = "Just some plain text"
        assert serializer.detect_format(text) == OutputFormat.HUMAN


# =============================================================================
# Roundtrip Tests
# =============================================================================


class TestRoundtrip:
    """Tests for serialize/deserialize roundtrip consistency."""

    def test_roundtrip_when_tabular_data_then_preserves_structure(
        self,
        serializer: ToonSerializer,
        tabular_data: list[dict],
    ) -> None:
        """Tabular data survives roundtrip."""
        serialized = serializer.serialize(tabular_data, OutputFormat.TOON)
        deserialized = serializer.deserialize(serialized, OutputFormat.TOON)

        assert len(deserialized) == len(tabular_data)
        for i, item in enumerate(tabular_data):
            assert deserialized[i]["id"] == item["id"]
            assert deserialized[i]["name"] == item["name"]
            assert deserialized[i]["status"] == item["status"]

    def test_roundtrip_when_primitive_array_then_preserves_values(
        self,
        serializer: ToonSerializer,
    ) -> None:
        """Primitive arrays survive roundtrip."""
        data = [1, 2, 3, 4, 5]
        serialized = serializer.serialize(data, OutputFormat.TOON)
        deserialized = serializer.deserialize(serialized, OutputFormat.TOON)

        assert deserialized == data

    def test_roundtrip_when_json_format_then_preserves_data(
        self,
        serializer: ToonSerializer,
        nested_data: dict,
    ) -> None:
        """JSON roundtrip preserves all data."""
        serialized = serializer.serialize(nested_data, OutputFormat.JSON)
        deserialized = serializer.deserialize(serialized, OutputFormat.JSON)

        assert deserialized == nested_data


# =============================================================================
# Edge Case Tests
# =============================================================================


class TestEdgeCases:
    """Tests for edge cases and boundary conditions."""

    def test_serialize_when_unicode_content_then_preserves_unicode(
        self,
        serializer: ToonSerializer,
    ) -> None:
        """Unicode characters are preserved."""
        data = {"name": "任务 🎯 Tâche"}
        result = serializer.serialize(data, OutputFormat.TOON)

        assert "任务" in result or '"任务' in result  # May or may not be quoted

    def test_serialize_when_newline_in_value_then_escapes_newline(
        self,
        serializer: ToonSerializer,
    ) -> None:
        """Newlines in values are escaped."""
        data = {"text": "line1\nline2"}
        result = serializer.serialize(data, OutputFormat.TOON)

        # Should be quoted and escaped
        assert "\\n" in result

    def test_serialize_when_custom_delimiter_then_uses_delimiter(
        self,
    ) -> None:
        """Custom delimiter is used in output."""
        serializer = ToonSerializer(delimiter="|")
        data = [{"a": 1, "b": 2}, {"a": 3, "b": 4}]
        result = serializer.serialize(data, OutputFormat.TOON)

        assert "{a|b}:" in result
        assert "1|2" in result

    def test_serialize_when_custom_indent_then_uses_indent(
        self,
    ) -> None:
        """Custom indent is used in output."""
        serializer = ToonSerializer(indent=4)
        data = {"outer": {"inner": "value"}}
        result = serializer.serialize(data, OutputFormat.TOON)

        # Check for 4-space indentation
        assert "    inner" in result

    def test_deserialize_when_empty_tabular_rows_then_skips_empty(
        self,
        serializer: ToonSerializer,
    ) -> None:
        """Empty rows in tabular format are skipped."""
        text = "[2]{id,name}:\n  1,First\n\n  2,Second\n"
        result = serializer.deserialize(text, OutputFormat.TOON)

        assert len(result) == 2
