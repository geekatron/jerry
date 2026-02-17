# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Unit tests for work_tracking.domain.value_objects.work_item_id module.

These tests verify the WorkItemId value object which provides hybrid
identity combining Snowflake internal IDs with human-readable display IDs.

References:
    - ADR-007: ID Generation Strategy
    - PHASE-IMPL-DOMAIN: IMPL-003 specification
"""

from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest

# Import will fail until implemented - RED phase
from src.work_tracking.domain.value_objects.work_item_id import WorkItemId


class TestWorkItemIdCreation:
    """Tests for WorkItemId initialization."""

    def test_create_valid_work_item_id(self) -> None:
        """WorkItemId can be created with valid internal and display IDs."""
        work_id = WorkItemId.create(
            internal_id=1767053847123456789,
            display_number=42,
        )
        assert work_id.internal_id == 1767053847123456789
        assert work_id.display_id == "WORK-042"

    def test_display_id_formats_with_leading_zeros(self) -> None:
        """Display ID pads single digits with leading zeros."""
        work_id = WorkItemId.create(internal_id=123456789, display_number=1)
        assert work_id.display_id == "WORK-001"

    def test_display_id_formats_double_digits(self) -> None:
        """Display ID pads double digits correctly."""
        work_id = WorkItemId.create(internal_id=123456789, display_number=12)
        assert work_id.display_id == "WORK-012"

    def test_display_id_formats_triple_digits(self) -> None:
        """Display ID handles triple digits without padding."""
        work_id = WorkItemId.create(internal_id=123456789, display_number=999)
        assert work_id.display_id == "WORK-999"

    def test_display_id_handles_large_numbers(self) -> None:
        """Display ID handles numbers beyond 3 digits."""
        work_id = WorkItemId.create(internal_id=123456789, display_number=10000)
        assert work_id.display_id == "WORK-10000"


class TestWorkItemIdProperties:
    """Tests for WorkItemId computed properties."""

    def test_display_number_extraction(self) -> None:
        """display_number property returns the numeric portion."""
        work_id = WorkItemId.create(internal_id=123456789, display_number=42)
        assert work_id.display_number == 42

    def test_internal_hex_representation(self) -> None:
        """internal_hex property returns hex string."""
        work_id = WorkItemId.create(internal_id=255, display_number=1)
        assert work_id.internal_hex == "0xff"

    def test_internal_hex_large_value(self) -> None:
        """internal_hex handles large Snowflake values."""
        work_id = WorkItemId.create(
            internal_id=1767053847123456789,
            display_number=1,
        )
        # Verify it's a valid hex string
        assert work_id.internal_hex.startswith("0x")
        int(work_id.internal_hex, 16)  # Should not raise


class TestWorkItemIdEquality:
    """Tests for WorkItemId equality and hashing."""

    def test_equality_by_internal_id(self) -> None:
        """Two WorkItemIds with same internal_id are equal."""
        id1 = WorkItemId.create(internal_id=12345, display_number=1)
        id2 = WorkItemId.create(internal_id=12345, display_number=1)
        assert id1 == id2

    def test_inequality_different_internal_id(self) -> None:
        """WorkItemIds with different internal_ids are not equal."""
        id1 = WorkItemId.create(internal_id=12345, display_number=1)
        id2 = WorkItemId.create(internal_id=12346, display_number=2)
        assert id1 != id2

    def test_hash_by_internal_id(self) -> None:
        """WorkItemIds with same internal_id have same hash."""
        id1 = WorkItemId.create(internal_id=12345, display_number=1)
        id2 = WorkItemId.create(internal_id=12345, display_number=1)
        assert hash(id1) == hash(id2)

    def test_usable_in_set(self) -> None:
        """WorkItemId can be used in sets and as dict keys."""
        id1 = WorkItemId.create(internal_id=12345, display_number=1)
        id2 = WorkItemId.create(internal_id=12346, display_number=2)
        id_set = {id1, id2}
        assert len(id_set) == 2

    def test_str_returns_display_id(self) -> None:
        """String representation returns display_id."""
        work_id = WorkItemId.create(internal_id=12345, display_number=42)
        assert str(work_id) == "WORK-042"

    def test_repr_includes_both_ids(self) -> None:
        """repr includes both internal and display IDs."""
        work_id = WorkItemId.create(internal_id=12345, display_number=42)
        repr_str = repr(work_id)
        assert "12345" in repr_str
        assert "WORK-042" in repr_str


class TestWorkItemIdValidation:
    """Negative tests for WorkItemId validation."""

    def test_negative_internal_id_rejected(self) -> None:
        """Negative internal_id is rejected."""
        with pytest.raises(ValueError, match="internal_id.*non-negative|negative"):
            WorkItemId.create(internal_id=-1, display_number=1)

    def test_zero_display_number_rejected(self) -> None:
        """Zero display_number is rejected."""
        with pytest.raises(ValueError, match="display_number.*positive"):
            WorkItemId.create(internal_id=12345, display_number=0)

    def test_negative_display_number_rejected(self) -> None:
        """Negative display_number is rejected."""
        with pytest.raises(ValueError, match="display_number.*positive"):
            WorkItemId.create(internal_id=12345, display_number=-1)


class TestWorkItemIdEdgeCases:
    """Edge case tests for WorkItemId."""

    def test_zero_internal_id_accepted(self) -> None:
        """Zero is a valid internal_id (edge case)."""
        work_id = WorkItemId.create(internal_id=0, display_number=1)
        assert work_id.internal_id == 0

    def test_max_64_bit_internal_id(self) -> None:
        """Maximum 64-bit value is accepted."""
        max_int64 = (2**63) - 1
        work_id = WorkItemId.create(internal_id=max_int64, display_number=1)
        assert work_id.internal_id == max_int64

    def test_immutability(self) -> None:
        """WorkItemId is immutable (frozen dataclass)."""
        work_id = WorkItemId.create(internal_id=12345, display_number=1)
        with pytest.raises(FrozenInstanceError):
            work_id.internal_id = 99999  # type: ignore


class TestWorkItemIdFromDisplayId:
    """Tests for parsing display_id strings."""

    def test_parse_valid_display_id(self) -> None:
        """from_display_id parses valid WORK-nnn format."""
        # This is for parsing existing display IDs, not for creating new ones
        work_id = WorkItemId.from_display_id("WORK-042", internal_id=12345)
        assert work_id.display_number == 42
        assert work_id.internal_id == 12345

    def test_parse_display_id_no_padding(self) -> None:
        """from_display_id handles non-padded numbers."""
        work_id = WorkItemId.from_display_id("WORK-999", internal_id=12345)
        assert work_id.display_number == 999

    def test_invalid_display_id_format_rejected(self) -> None:
        """Invalid display_id format is rejected."""
        with pytest.raises(ValueError, match="Invalid.*format|WORK-"):
            WorkItemId.from_display_id("INVALID-001", internal_id=12345)

    def test_empty_display_id_rejected(self) -> None:
        """Empty display_id is rejected."""
        with pytest.raises(ValueError, match="Invalid|empty|format"):
            WorkItemId.from_display_id("", internal_id=12345)

    def test_display_id_wrong_prefix_rejected(self) -> None:
        """Wrong prefix in display_id is rejected."""
        with pytest.raises(ValueError, match="Invalid|WORK-"):
            WorkItemId.from_display_id("TASK-001", internal_id=12345)
