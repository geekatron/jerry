# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Unit tests for SessionId value object.

Test Categories:
    - VertexId Compliance: Inheritance and protocol implementation
    - Format Validation: SESS-{uuid8} format rules
    - Generation: generate() produces valid IDs
    - Edge Cases: Boundary conditions and error handling

References:
    - ENFORCE-008d.3: New Domain Objects
    - Canon PAT-001: VertexId Base Class
    - ADR-013: Shared Kernel Module
"""

from __future__ import annotations

import re

import pytest

from src.session_management.domain.value_objects.session_id import SessionId
from src.shared_kernel.vertex_id import VertexId

# =============================================================================
# VertexId Compliance Tests (I-008d.3.1)
# =============================================================================


class TestSessionIdVertexIdCompliance:
    """Tests for VertexId protocol compliance."""

    def test_session_id_extends_vertex_id(self) -> None:
        """SessionId should inherit from VertexId base class."""
        session_id = SessionId.generate()
        assert isinstance(session_id, VertexId)

    def test_session_id_is_frozen_dataclass(self) -> None:
        """SessionId should be immutable (frozen dataclass)."""
        session_id = SessionId.generate()
        with pytest.raises(Exception):  # FrozenInstanceError
            session_id.value = "changed"

    def test_session_id_has_value_property(self) -> None:
        """SessionId should have value property from VertexId."""
        session_id = SessionId.generate()
        assert hasattr(session_id, "value")
        assert session_id.value.startswith("SESS-")

    def test_session_id_implements_is_valid_format(self) -> None:
        """SessionId should implement _is_valid_format classmethod."""
        assert hasattr(SessionId, "_is_valid_format")
        assert callable(SessionId._is_valid_format)

    def test_session_id_str_returns_value(self) -> None:
        """__str__ should return the value property."""
        session_id = SessionId.generate()
        assert str(session_id) == session_id.value

    def test_session_id_hash_uses_value(self) -> None:
        """Hash should be based on value for set/dict usage."""
        id1 = SessionId.from_string("SESS-a1b2c3d4")
        id2 = SessionId.from_string("SESS-a1b2c3d4")
        assert hash(id1) == hash(id2)

    def test_session_id_equality_by_value(self) -> None:
        """Two SessionIds with same value should be equal."""
        id1 = SessionId.from_string("SESS-a1b2c3d4")
        id2 = SessionId.from_string("SESS-a1b2c3d4")
        assert id1 == id2


# =============================================================================
# Format Validation Tests
# =============================================================================


class TestSessionIdFormatValidation:
    """Tests for format validation rules."""

    def test_valid_format_accepted(self) -> None:
        """Accept valid SESS-{uuid8} format."""
        assert SessionId._is_valid_format("SESS-a1b2c3d4") is True
        assert SessionId._is_valid_format("SESS-00000000") is True
        assert SessionId._is_valid_format("SESS-ffffffff") is True

    def test_reject_wrong_prefix(self) -> None:
        """Reject non-SESS prefix."""
        assert SessionId._is_valid_format("TASK-a1b2c3d4") is False
        assert SessionId._is_valid_format("sess-a1b2c3d4") is False
        assert SessionId._is_valid_format("SESSION-a1b2") is False

    def test_reject_wrong_length(self) -> None:
        """Reject incorrect hex length (must be 8 chars)."""
        assert SessionId._is_valid_format("SESS-a1b2c3") is False  # 6 chars
        assert SessionId._is_valid_format("SESS-a1b2c3d4e5") is False  # 10 chars

    def test_reject_non_hex_characters(self) -> None:
        """Reject non-hexadecimal characters."""
        assert SessionId._is_valid_format("SESS-g1h2i3j4") is False  # g,h,i,j not hex
        assert SessionId._is_valid_format("SESS-A1B2C3D4") is False  # uppercase hex

    def test_from_string_valid(self) -> None:
        """from_string should parse valid format."""
        session_id = SessionId.from_string("SESS-a1b2c3d4")
        assert session_id.value == "SESS-a1b2c3d4"

    def test_from_string_invalid_raises(self) -> None:
        """from_string should raise ValueError for invalid format."""
        with pytest.raises(ValueError):
            SessionId.from_string("INVALID")


# =============================================================================
# Generation Tests
# =============================================================================


class TestSessionIdGeneration:
    """Tests for ID generation."""

    def test_generate_produces_valid_format(self) -> None:
        """generate() should produce valid SESS-{uuid8} format."""
        session_id = SessionId.generate()
        assert SessionId._is_valid_format(session_id.value)

    def test_generate_produces_unique_ids(self) -> None:
        """generate() should produce unique IDs."""
        ids = [SessionId.generate() for _ in range(100)]
        unique_values = {id.value for id in ids}
        assert len(unique_values) == 100

    def test_generated_id_matches_pattern(self) -> None:
        """Generated ID should match SESS-{8 hex chars} pattern."""
        session_id = SessionId.generate()
        pattern = re.compile(r"^SESS-[a-f0-9]{8}$")
        assert pattern.match(session_id.value) is not None


# =============================================================================
# Edge Cases Tests
# =============================================================================


class TestSessionIdEdgeCases:
    """Edge case and boundary tests."""

    def test_equality_different_instances_same_value(self) -> None:
        """Different instances with same value should be equal."""
        id1 = SessionId.from_string("SESS-12345678")
        id2 = SessionId.from_string("SESS-12345678")
        assert id1 == id2
        assert id1 is not id2

    def test_inequality_different_values(self) -> None:
        """Different values should not be equal."""
        id1 = SessionId.from_string("SESS-11111111")
        id2 = SessionId.from_string("SESS-22222222")
        assert id1 != id2

    def test_can_use_in_set(self) -> None:
        """SessionId should work in sets."""
        id1 = SessionId.from_string("SESS-a1b2c3d4")
        id2 = SessionId.from_string("SESS-a1b2c3d4")
        id3 = SessionId.from_string("SESS-11111111")

        id_set = {id1, id2, id3}
        assert len(id_set) == 2  # id1 and id2 are equal

    def test_can_use_as_dict_key(self) -> None:
        """SessionId should work as dictionary key."""
        id1 = SessionId.from_string("SESS-a1b2c3d4")
        id2 = SessionId.from_string("SESS-a1b2c3d4")

        data = {id1: "value1"}
        assert data[id2] == "value1"  # id2 should find same entry
