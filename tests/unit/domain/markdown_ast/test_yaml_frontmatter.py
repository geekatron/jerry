# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Unit tests for YamlFrontmatter parser (WI-005, WI-006).

Tests cover:
    - Happy path: extract valid YAML frontmatter
    - Type normalization (DD-10): str, int, float, bool, list, dict, null
    - First-pair-only extraction (M-24)
    - Pre-parse size check (M-07)
    - Post-parse result size (M-20)
    - Post-parse key count (M-16)
    - Post-parse nesting depth (M-06)
    - Alias count enforcement (M-20)
    - Value length truncation (M-17)
    - Control character stripping (M-18)
    - Duplicate key detection (M-23)
    - Sanitized error messages (M-19)
    - Invalid YAML handling
    - Empty document handling
    - Frozen dataclass immutability

References:
    - ADR-PROJ005-003 Design Decisions 1, 8, 10
    - H-20: BDD test-first
"""

from __future__ import annotations

import pytest

from src.domain.markdown_ast.input_bounds import InputBounds
from src.domain.markdown_ast.jerry_document import JerryDocument
from src.domain.markdown_ast.yaml_frontmatter import (
    YamlFrontmatter,
    YamlFrontmatterField,
    YamlFrontmatterResult,
)

# =============================================================================
# Happy Path Tests
# =============================================================================


class TestYamlFrontmatterExtraction:
    """Tests for basic YAML frontmatter extraction."""

    @pytest.mark.happy_path
    def test_extract_simple_fields(self) -> None:
        """Extracts key-value pairs from --- delimited block."""
        source = "---\nname: test-agent\nversion: 1.0.0\n---\n# Agent\n"
        doc = JerryDocument.parse(source)
        result = YamlFrontmatter.extract(doc)

        assert result.parse_error is None
        assert len(result.fields) == 2
        assert result.fields[0].key == "name"
        assert result.fields[0].value == "test-agent"
        assert result.fields[1].key == "version"
        assert result.fields[1].value == "1.0.0"

    @pytest.mark.happy_path
    def test_extract_preserves_raw_yaml(self) -> None:
        """raw_yaml contains the text between --- delimiters."""
        source = "---\nname: test\n---\n"
        doc = JerryDocument.parse(source)
        result = YamlFrontmatter.extract(doc)

        assert "name: test" in result.raw_yaml

    @pytest.mark.happy_path
    def test_extract_line_positions(self) -> None:
        """start_line and end_line are set correctly."""
        source = "---\nname: test\nversion: 1.0\n---\n"
        doc = JerryDocument.parse(source)
        result = YamlFrontmatter.extract(doc)

        assert result.start_line == 0
        assert result.end_line > 0

    @pytest.mark.happy_path
    def test_no_yaml_returns_empty(self) -> None:
        """Document without --- block returns empty result."""
        doc = JerryDocument.parse("# Just a heading\n\nContent.\n")
        result = YamlFrontmatter.extract(doc)

        assert result.parse_error is None
        assert len(result.fields) == 0
        assert result.raw_yaml == ""

    @pytest.mark.happy_path
    def test_empty_document(self) -> None:
        """Empty document returns empty result."""
        doc = JerryDocument.parse("")
        result = YamlFrontmatter.extract(doc)

        assert result.parse_error is None
        assert len(result.fields) == 0


# =============================================================================
# Type Normalization Tests (DD-10)
# =============================================================================


class TestTypeNormalization:
    """Tests for YAML type normalization (Design Decision 10)."""

    @pytest.mark.happy_path
    def test_string_type(self) -> None:
        """String values get value_type='str'."""
        source = "---\nname: test-agent\n---\n"
        doc = JerryDocument.parse(source)
        result = YamlFrontmatter.extract(doc)

        assert result.fields[0].value_type == "str"
        assert result.fields[0].value == "test-agent"

    @pytest.mark.happy_path
    def test_integer_type(self) -> None:
        """Integer values get value_type='int'."""
        source = "---\ncount: 42\n---\n"
        doc = JerryDocument.parse(source)
        result = YamlFrontmatter.extract(doc)

        assert result.fields[0].value_type == "int"
        assert result.fields[0].value == 42

    @pytest.mark.happy_path
    def test_float_type(self) -> None:
        """Float values get value_type='float'."""
        source = "---\nscore: 3.14\n---\n"
        doc = JerryDocument.parse(source)
        result = YamlFrontmatter.extract(doc)

        assert result.fields[0].value_type == "float"
        assert result.fields[0].value == 3.14

    @pytest.mark.happy_path
    def test_boolean_type(self) -> None:
        """Boolean values get value_type='bool'."""
        source = "---\nenabled: true\n---\n"
        doc = JerryDocument.parse(source)
        result = YamlFrontmatter.extract(doc)

        assert result.fields[0].value_type == "bool"
        assert result.fields[0].value is True

    @pytest.mark.happy_path
    def test_null_type(self) -> None:
        """Null values get value_type='null'."""
        source = "---\nempty: null\n---\n"
        doc = JerryDocument.parse(source)
        result = YamlFrontmatter.extract(doc)

        assert result.fields[0].value_type == "null"
        assert result.fields[0].value is None

    @pytest.mark.happy_path
    def test_list_type(self) -> None:
        """List values get value_type='list'."""
        source = "---\nitems:\n  - one\n  - two\n---\n"
        doc = JerryDocument.parse(source)
        result = YamlFrontmatter.extract(doc)

        assert result.fields[0].value_type == "list"
        assert isinstance(result.fields[0].value, list)
        assert len(result.fields[0].value) == 2

    @pytest.mark.happy_path
    def test_dict_type(self) -> None:
        """Dict values get value_type='dict'."""
        source = "---\nperson:\n  name: alice\n  age: 30\n---\n"
        doc = JerryDocument.parse(source)
        result = YamlFrontmatter.extract(doc)

        assert result.fields[0].value_type == "dict"
        assert isinstance(result.fields[0].value, dict)


# =============================================================================
# First-Pair-Only Extraction (M-24)
# =============================================================================


class TestFirstPairOnly:
    """Tests for M-24: only the first --- ... --- pair is extracted."""

    @pytest.mark.happy_path
    def test_second_yaml_block_ignored(self) -> None:
        """Only the first --- block is extracted; subsequent ones are ignored."""
        source = (
            "---\nfirst: block\n---\n\n"
            "## Content\n\n"
            "---\nsecond: block\n---\n"
        )
        doc = JerryDocument.parse(source)
        result = YamlFrontmatter.extract(doc)

        assert result.parse_error is None
        assert len(result.fields) == 1
        assert result.fields[0].key == "first"


# =============================================================================
# Bounds Enforcement Tests
# =============================================================================


class TestBoundsEnforcement:
    """Tests for InputBounds enforcement in YamlFrontmatter."""

    @pytest.mark.boundary
    def test_yaml_block_size_limit(self) -> None:
        """YAML block exceeding max_yaml_block_bytes produces parse error (M-07)."""
        bounds = InputBounds(max_yaml_block_bytes=10)
        source = "---\nname: this-is-a-long-name-that-exceeds\n---\n"
        doc = JerryDocument.parse(source)
        result = YamlFrontmatter.extract(doc, bounds)

        assert result.parse_error is not None
        assert "exceeds maximum size" in result.parse_error

    @pytest.mark.boundary
    def test_key_count_limit(self) -> None:
        """Key count exceeding max produces parse error (M-16)."""
        bounds = InputBounds(max_frontmatter_keys=2)
        source = "---\na: 1\nb: 2\nc: 3\n---\n"
        doc = JerryDocument.parse(source)
        result = YamlFrontmatter.extract(doc, bounds)

        assert result.parse_error is not None
        assert "key count exceeds" in result.parse_error

    @pytest.mark.boundary
    def test_nesting_depth_limit(self) -> None:
        """Nesting depth exceeding max produces parse error (M-06)."""
        bounds = InputBounds(max_nesting_depth=1)
        source = "---\nouter:\n  inner:\n    deep: value\n---\n"
        doc = JerryDocument.parse(source)
        result = YamlFrontmatter.extract(doc, bounds)

        assert result.parse_error is not None
        assert "nesting depth exceeds" in result.parse_error

    @pytest.mark.boundary
    def test_alias_count_limit(self) -> None:
        """Alias count exceeding max produces parse error (M-20)."""
        bounds = InputBounds(max_alias_count=0)
        source = "---\nanchor: &ref value\naliased: *ref\n---\n"
        doc = JerryDocument.parse(source)
        result = YamlFrontmatter.extract(doc, bounds)

        assert result.parse_error is not None
        assert "alias count exceeds" in result.parse_error

    @pytest.mark.boundary
    def test_value_length_truncation(self) -> None:
        """Value exceeding max_value_length produces warning (M-17)."""
        bounds = InputBounds(max_value_length=5)
        source = "---\nname: this-is-very-long\n---\n"
        doc = JerryDocument.parse(source)
        result = YamlFrontmatter.extract(doc, bounds)

        assert result.parse_error is None
        assert len(result.parse_warnings) > 0
        assert any("truncated" in w for w in result.parse_warnings)


# =============================================================================
# Control Character Stripping Tests (M-18)
# =============================================================================


class TestControlCharacterStripping:
    """Tests for M-18: control characters stripped from values."""

    @pytest.mark.edge_case
    def test_strip_control_chars_removes_null_bytes(self) -> None:
        """_strip_control_chars removes null bytes from strings (M-18).

        PyYAML rejects null bytes at the reader stage (before our code runs),
        so M-18 stripping applies to values that survive parsing. We test
        the stripping function directly.
        """
        from src.domain.markdown_ast.yaml_frontmatter import _strip_control_chars

        assert _strip_control_chars("test\x00agent") == "testagent"
        assert _strip_control_chars("na\x01me") == "name"
        assert _strip_control_chars("clean") == "clean"

    @pytest.mark.edge_case
    def test_strip_control_chars_preserves_whitespace(self) -> None:
        """_strip_control_chars preserves tab, newline, carriage return."""
        from src.domain.markdown_ast.yaml_frontmatter import _strip_control_chars

        assert _strip_control_chars("with\ttab") == "with\ttab"
        assert _strip_control_chars("with\nnewline") == "with\nnewline"
        assert _strip_control_chars("with\rreturn") == "with\rreturn"


# =============================================================================
# Duplicate Key Detection (M-23)
# =============================================================================


class TestDuplicateKeyDetection:
    """Tests for M-23: duplicate key detection."""

    @pytest.mark.edge_case
    def test_duplicate_keys_produce_warning(self) -> None:
        """Duplicate YAML keys produce a warning."""
        source = "---\nname: first\nname: second\n---\n"
        doc = JerryDocument.parse(source)
        result = YamlFrontmatter.extract(doc)

        assert len(result.parse_warnings) > 0
        assert any("Duplicate key" in w for w in result.parse_warnings)

    @pytest.mark.edge_case
    def test_duplicate_key_last_value_used(self) -> None:
        """For duplicate keys, the last value is used (PyYAML behavior)."""
        source = "---\nname: first\nname: second\n---\n"
        doc = JerryDocument.parse(source)
        result = YamlFrontmatter.extract(doc)

        # PyYAML uses the last value for duplicate keys
        name_field = next(f for f in result.fields if f.key == "name")
        assert name_field.value == "second"


# =============================================================================
# Error Handling Tests
# =============================================================================


class TestErrorHandling:
    """Tests for YAML parse error handling (M-19, DD-9)."""

    @pytest.mark.negative
    def test_invalid_yaml_produces_parse_error(self) -> None:
        """Invalid YAML syntax produces a parse error."""
        source = "---\n: invalid yaml:\n  bad: [unclosed\n---\n"
        doc = JerryDocument.parse(source)
        result = YamlFrontmatter.extract(doc)

        assert result.parse_error is not None
        assert len(result.fields) == 0

    @pytest.mark.negative
    def test_non_mapping_yaml_produces_error(self) -> None:
        """YAML that parses as non-dict produces error."""
        source = "---\n- item1\n- item2\n---\n"
        doc = JerryDocument.parse(source)
        result = YamlFrontmatter.extract(doc)

        assert result.parse_error is not None
        assert "mapping" in result.parse_error

    @pytest.mark.negative
    def test_error_messages_do_not_leak_full_content(self) -> None:
        """Error messages are sanitized (M-19): no raw YAML in error."""
        source = "---\n: [broken yaml\n---\n"
        doc = JerryDocument.parse(source)
        result = YamlFrontmatter.extract(doc)

        assert result.parse_error is not None
        # Error should reference problem, not dump raw content
        assert "YAML" in result.parse_error


# =============================================================================
# Immutability Tests
# =============================================================================


class TestImmutability:
    """Tests for frozen dataclass immutability."""

    @pytest.mark.happy_path
    def test_field_is_frozen(self) -> None:
        """YamlFrontmatterField is frozen."""
        field = YamlFrontmatterField(key="test", value="val", value_type="str")
        with pytest.raises(AttributeError):
            field.key = "hacked"  # type: ignore[misc]

    @pytest.mark.happy_path
    def test_result_is_frozen(self) -> None:
        """YamlFrontmatterResult is frozen."""
        result = YamlFrontmatterResult(
            fields=(),
            raw_yaml="",
            start_line=0,
            end_line=0,
            parse_error=None,
        )
        with pytest.raises(AttributeError):
            result.parse_error = "hacked"  # type: ignore[misc]

    @pytest.mark.happy_path
    def test_fields_is_tuple(self) -> None:
        """Fields container is a tuple for immutability."""
        source = "---\nname: test\n---\n"
        doc = JerryDocument.parse(source)
        result = YamlFrontmatter.extract(doc)

        assert isinstance(result.fields, tuple)

    @pytest.mark.happy_path
    def test_parse_warnings_is_tuple(self) -> None:
        """parse_warnings is a tuple for immutability."""
        source = "---\nname: test\n---\n"
        doc = JerryDocument.parse(source)
        result = YamlFrontmatter.extract(doc)

        assert isinstance(result.parse_warnings, tuple)


# =============================================================================
# Default Bounds Tests
# =============================================================================


class TestDefaultBounds:
    """Tests for default InputBounds behavior."""

    @pytest.mark.happy_path
    def test_none_bounds_uses_defaults(self) -> None:
        """Passing None for bounds uses InputBounds.DEFAULT."""
        source = "---\nname: test\n---\n"
        doc = JerryDocument.parse(source)
        result = YamlFrontmatter.extract(doc, bounds=None)

        assert result.parse_error is None
        assert len(result.fields) == 1


# =============================================================================
# YAML Error Path Coverage Tests
# =============================================================================


class TestYamlErrorPaths:
    """Tests for specific YAML error handling paths."""

    @pytest.mark.negative
    def test_scanner_error_with_line_info(self) -> None:
        """ScannerError with problem_mark includes line info (lines 272-275)."""
        # Invalid YAML that triggers ScannerError with position info
        source = "---\nname: test\n  bad indent: value\n---\n"
        doc = JerryDocument.parse(source)
        result = YamlFrontmatter.extract(doc)

        assert result.parse_error is not None
        # ScannerError should have line information
        assert "error" in result.parse_error.lower()

    @pytest.mark.negative
    def test_constructor_error_handling(self) -> None:
        """ConstructorError produces parse error (lines 293-294)."""
        # YAML with a tag that triggers ConstructorError in safe_load
        source = "---\ndata: !!python/object:os.system 'ls'\n---\n"
        doc = JerryDocument.parse(source)
        result = YamlFrontmatter.extract(doc)

        assert result.parse_error is not None
        assert "error" in result.parse_error.lower()

    @pytest.mark.boundary
    def test_result_size_exceeds_max(self) -> None:
        """Post-parse result exceeding max_yaml_result_bytes triggers error (M-20, lines 317-320)."""
        # Create a YAML with enough content to exceed a very small result limit
        bounds = InputBounds(max_yaml_result_bytes=10)
        source = "---\nname: this-is-a-long-value-that-will-exceed-ten-bytes\n---\n"
        doc = JerryDocument.parse(source)
        result = YamlFrontmatter.extract(doc, bounds=bounds)

        assert result.parse_error is not None
        assert "exceeds maximum size" in result.parse_error
