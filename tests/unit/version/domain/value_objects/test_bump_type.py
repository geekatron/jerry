# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Unit tests for BumpType value object.

References:
    - BUG-002: Version bump regex rejects uppercase scopes
"""

from __future__ import annotations

import pytest

from src.version.domain.value_objects.bump_type import BumpType


class TestBumpTypeOrdering:
    """Tests for BumpType severity ordering."""

    @pytest.mark.happy_path
    def test_major_is_greater_than_minor(self) -> None:
        assert BumpType.MAJOR > BumpType.MINOR

    @pytest.mark.happy_path
    def test_minor_is_greater_than_patch(self) -> None:
        assert BumpType.MINOR > BumpType.PATCH

    @pytest.mark.happy_path
    def test_patch_is_greater_than_none(self) -> None:
        assert BumpType.PATCH > BumpType.NONE

    @pytest.mark.happy_path
    def test_major_is_greatest(self) -> None:
        assert BumpType.MAJOR > BumpType.NONE
        assert BumpType.MAJOR > BumpType.PATCH
        assert BumpType.MAJOR > BumpType.MINOR

    @pytest.mark.happy_path
    def test_none_is_least(self) -> None:
        assert BumpType.NONE < BumpType.PATCH
        assert BumpType.NONE < BumpType.MINOR
        assert BumpType.NONE < BumpType.MAJOR

    @pytest.mark.happy_path
    def test_equality(self) -> None:
        assert BumpType.MAJOR == BumpType.MAJOR
        assert BumpType.NONE == BumpType.NONE

    @pytest.mark.happy_path
    def test_max_selects_highest(self) -> None:
        result = max(BumpType.NONE, BumpType.PATCH, BumpType.MINOR, BumpType.MAJOR)
        assert result == BumpType.MAJOR

    @pytest.mark.happy_path
    def test_max_with_only_none_and_patch(self) -> None:
        result = max(BumpType.NONE, BumpType.PATCH)
        assert result == BumpType.PATCH

    @pytest.mark.happy_path
    def test_ge_comparison(self) -> None:
        assert BumpType.MAJOR >= BumpType.MAJOR
        assert BumpType.MAJOR >= BumpType.MINOR

    @pytest.mark.happy_path
    def test_le_comparison(self) -> None:
        assert BumpType.NONE <= BumpType.NONE
        assert BumpType.NONE <= BumpType.PATCH

    @pytest.mark.negative
    def test_gt_with_non_bump_type_returns_not_implemented(self) -> None:
        result = BumpType.MAJOR.__gt__(42)
        assert result is NotImplemented

    @pytest.mark.negative
    def test_lt_with_non_bump_type_returns_not_implemented(self) -> None:
        result = BumpType.MAJOR.__lt__("not_a_bump_type")
        assert result is NotImplemented

    @pytest.mark.negative
    def test_ge_with_non_bump_type_returns_not_implemented(self) -> None:
        result = BumpType.MAJOR.__ge__(None)
        assert result is NotImplemented

    @pytest.mark.negative
    def test_le_with_non_bump_type_returns_not_implemented(self) -> None:
        result = BumpType.MAJOR.__le__(3.14)
        assert result is NotImplemented


class TestBumpTypeLabel:
    """Tests for BumpType.label property."""

    @pytest.mark.happy_path
    def test_major_label(self) -> None:
        assert BumpType.MAJOR.label == "major"

    @pytest.mark.happy_path
    def test_minor_label(self) -> None:
        assert BumpType.MINOR.label == "minor"

    @pytest.mark.happy_path
    def test_patch_label(self) -> None:
        assert BumpType.PATCH.label == "patch"

    @pytest.mark.happy_path
    def test_none_label(self) -> None:
        assert BumpType.NONE.label == "none"


class TestBumpTypeValues:
    """Tests for BumpType enum values."""

    @pytest.mark.edge_case
    def test_enum_has_four_members(self) -> None:
        assert len(BumpType) == 4

    @pytest.mark.happy_path
    def test_values_are_monotonically_increasing(self) -> None:
        assert BumpType.NONE.value < BumpType.PATCH.value
        assert BumpType.PATCH.value < BumpType.MINOR.value
        assert BumpType.MINOR.value < BumpType.MAJOR.value
