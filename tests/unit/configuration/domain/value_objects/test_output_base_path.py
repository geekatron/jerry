# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
Unit tests for OutputBasePath value object.

Tests cover:
    - GH #192 / REQ-OBP-003c: OutputBasePath value object specification
    - Construction with valid paths (relative, absolute, with trailing slash)
    - Empty string acceptance (triggers fallback in OutputResolver)
    - Null byte rejection (ValueError per REQ-OBP-003h)
    - Whitespace-only path acceptance (EC-025)
    - Immutability (frozen dataclass)
    - __str__ returns the raw path value

Test Categories:
    - Happy path: Valid path construction and string conversion
    - Negative: Null byte rejection
    - Edge cases: Empty string, whitespace-only, absolute paths
"""

from __future__ import annotations

import pytest

from src.configuration.domain.value_objects.output_base_path import OutputBasePath


class TestOutputBasePathCreation:
    """Tests for OutputBasePath instantiation."""

    def test_create_with_relative_path(self) -> None:
        """Relative path is valid."""
        path = OutputBasePath("work/")
        assert path.value == "work/"

    def test_create_with_relative_path_no_trailing_slash(self) -> None:
        """Relative path without trailing slash is valid (resolver adds slash)."""
        path = OutputBasePath("custom/output")
        assert path.value == "custom/output"

    def test_create_with_absolute_path(self) -> None:
        """Absolute path is valid per ADR-PROJ021-001 INV-3."""
        path = OutputBasePath("/absolute/path/")
        assert path.value == "/absolute/path/"

    def test_create_with_nested_path(self) -> None:
        """Deeply nested path is valid."""
        path = OutputBasePath("projects/PROJ-001/output/artifacts/")
        assert path.value == "projects/PROJ-001/output/artifacts/"

    def test_create_with_empty_string(self) -> None:
        """Empty string is valid (triggers fallback in OutputResolver)."""
        path = OutputBasePath("")
        assert path.value == ""

    def test_create_with_whitespace_only(self) -> None:
        """Whitespace-only path is valid per EC-025."""
        path = OutputBasePath("   ")
        assert path.value == "   "

    def test_create_with_dot_path(self) -> None:
        """Current directory reference is valid."""
        path = OutputBasePath("./")
        assert path.value == "./"

    def test_create_with_parent_reference(self) -> None:
        """Parent directory reference is valid."""
        path = OutputBasePath("../output/")
        assert path.value == "../output/"


class TestOutputBasePathNullByteRejection:
    """Tests for null byte validation."""

    def test_rejects_null_byte_at_start(self) -> None:
        """Null byte at start of path raises ValueError."""
        with pytest.raises(ValueError, match="null bytes"):
            OutputBasePath("\x00work/")

    def test_rejects_null_byte_in_middle(self) -> None:
        """Null byte in middle of path raises ValueError."""
        with pytest.raises(ValueError, match="null bytes"):
            OutputBasePath("work/\x00output/")

    def test_rejects_null_byte_at_end(self) -> None:
        """Null byte at end of path raises ValueError."""
        with pytest.raises(ValueError, match="null bytes"):
            OutputBasePath("work/\x00")

    def test_rejects_only_null_byte(self) -> None:
        """Single null byte raises ValueError."""
        with pytest.raises(ValueError, match="null bytes"):
            OutputBasePath("\x00")

    def test_rejects_multiple_null_bytes(self) -> None:
        """Multiple null bytes raises ValueError."""
        with pytest.raises(ValueError, match="null bytes"):
            OutputBasePath("\x00\x00\x00")


class TestOutputBasePathImmutability:
    """Tests for frozen dataclass behavior."""

    def test_cannot_modify_value(self) -> None:
        """Frozen dataclass prevents attribute mutation."""
        path = OutputBasePath("work/")
        with pytest.raises(AttributeError):
            path.value = "other/"  # type: ignore[misc]


class TestOutputBasePathStringConversion:
    """Tests for __str__ behavior."""

    def test_str_returns_value(self) -> None:
        """__str__ returns the raw path value."""
        path = OutputBasePath("work/output/")
        assert str(path) == "work/output/"

    def test_str_returns_empty_for_empty(self) -> None:
        """__str__ returns empty string for empty path."""
        path = OutputBasePath("")
        assert str(path) == ""

    def test_str_returns_absolute_path(self) -> None:
        """__str__ returns absolute path as-is."""
        path = OutputBasePath("/usr/local/output/")
        assert str(path) == "/usr/local/output/"


class TestOutputBasePathEquality:
    """Tests for dataclass equality."""

    def test_equal_paths_are_equal(self) -> None:
        """Same value produces equal instances."""
        assert OutputBasePath("work/") == OutputBasePath("work/")

    def test_different_paths_are_not_equal(self) -> None:
        """Different values produce unequal instances."""
        assert OutputBasePath("work/") != OutputBasePath("output/")

    def test_hashable(self) -> None:
        """Frozen dataclass is hashable (usable in sets/dicts)."""
        paths = {OutputBasePath("a/"), OutputBasePath("b/"), OutputBasePath("a/")}
        assert len(paths) == 2
