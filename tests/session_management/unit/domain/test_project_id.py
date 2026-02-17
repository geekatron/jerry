# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Unit tests for ProjectId value object.

Test Categories:
    - VertexId Compliance: Inheritance and protocol implementation
    - Format Validation: PROJ-{nnn}-{slug} format rules
    - Backwards Compatibility: parse(), number, slug properties
    - Edge Cases: Boundary conditions and error handling

References:
    - ENFORCE-008d: Domain Refactoring
    - Canon PAT-001: VertexId Base Class
    - ADR-013: Shared Kernel Module
"""

from __future__ import annotations

import pytest

from src.session_management.domain.exceptions import InvalidProjectIdError
from src.session_management.domain.value_objects.project_id import ProjectId
from src.shared_kernel.vertex_id import VertexId

# =============================================================================
# VertexId Compliance Tests (I-008d.1.1)
# =============================================================================


class TestProjectIdVertexIdCompliance:
    """Tests for VertexId protocol compliance."""

    def test_project_id_extends_vertex_id(self) -> None:
        """ProjectId should inherit from VertexId base class."""
        project_id = ProjectId.parse("PROJ-001-test")
        assert isinstance(project_id, VertexId)

    def test_project_id_is_frozen_dataclass(self) -> None:
        """ProjectId should be immutable (frozen dataclass)."""
        project_id = ProjectId.parse("PROJ-001-test")
        with pytest.raises(Exception):  # FrozenInstanceError
            project_id.value = "changed"

    def test_project_id_has_value_property(self) -> None:
        """ProjectId should have value property from VertexId."""
        project_id = ProjectId.parse("PROJ-001-test")
        assert hasattr(project_id, "value")
        assert project_id.value == "PROJ-001-test"

    def test_project_id_implements_is_valid_format(self) -> None:
        """ProjectId should implement _is_valid_format classmethod."""
        assert hasattr(ProjectId, "_is_valid_format")
        assert callable(ProjectId._is_valid_format)

    def test_is_valid_format_accepts_valid_format(self) -> None:
        """_is_valid_format should return True for valid PROJ-{nnn}-{slug}."""
        assert ProjectId._is_valid_format("PROJ-001-test") is True
        assert ProjectId._is_valid_format("PROJ-999-my-project") is True
        assert ProjectId._is_valid_format("PROJ-042-a") is True

    def test_is_valid_format_rejects_invalid_format(self) -> None:
        """_is_valid_format should return False for invalid formats."""
        assert ProjectId._is_valid_format("PROJ-1-test") is False  # Not 3 digits
        assert ProjectId._is_valid_format("PROJ-000-test") is False  # Zero not allowed
        assert ProjectId._is_valid_format("TASK-001-test") is False  # Wrong prefix
        assert ProjectId._is_valid_format("proj-001-test") is False  # Lowercase prefix
        assert ProjectId._is_valid_format("PROJ-001-Test") is False  # Uppercase in slug

    def test_project_id_has_from_string_method(self) -> None:
        """ProjectId should have from_string classmethod from VertexId."""
        assert hasattr(ProjectId, "from_string")
        project_id = ProjectId.from_string("PROJ-001-test")
        assert project_id.value == "PROJ-001-test"

    def test_project_id_str_returns_value(self) -> None:
        """__str__ should return the value property."""
        project_id = ProjectId.parse("PROJ-001-test")
        assert str(project_id) == "PROJ-001-test"

    def test_project_id_hash_uses_value(self) -> None:
        """Hash should be based on value for set/dict usage."""
        id1 = ProjectId.parse("PROJ-001-test")
        id2 = ProjectId.parse("PROJ-001-test")
        assert hash(id1) == hash(id2)

    def test_project_id_equality_by_value(self) -> None:
        """Two ProjectIds with same value should be equal."""
        id1 = ProjectId.parse("PROJ-001-test")
        id2 = ProjectId.parse("PROJ-001-test")
        assert id1 == id2


# =============================================================================
# Backwards Compatibility Tests (I-008d.1.2)
# =============================================================================


class TestProjectIdBackwardsCompatibility:
    """Tests for backwards compatibility with existing API."""

    def test_parse_still_works(self) -> None:
        """parse() classmethod should still work."""
        project_id = ProjectId.parse("PROJ-001-plugin-cleanup")
        assert project_id.value == "PROJ-001-plugin-cleanup"

    def test_parse_returns_project_id_type(self) -> None:
        """parse() should return ProjectId (not just VertexId)."""
        project_id = ProjectId.parse("PROJ-001-test")
        assert type(project_id) is ProjectId

    def test_number_property_available(self) -> None:
        """number property should be extractable."""
        project_id = ProjectId.parse("PROJ-042-test")
        assert project_id.number == 42

    def test_slug_property_available(self) -> None:
        """slug property should be extractable."""
        project_id = ProjectId.parse("PROJ-001-my-cool-project")
        assert project_id.slug == "my-cool-project"

    def test_create_method_works(self) -> None:
        """create(number, slug) factory should still work."""
        project_id = ProjectId.create(number=5, slug="new-project")
        assert project_id.value == "PROJ-005-new-project"
        assert project_id.number == 5
        assert project_id.slug == "new-project"


# =============================================================================
# Format Validation Tests (I-008d.1.3)
# =============================================================================


class TestProjectIdFormatValidation:
    """Tests for format validation rules."""

    def test_valid_minimal_format(self) -> None:
        """Accept minimal valid format."""
        project_id = ProjectId.parse("PROJ-001-a")
        assert project_id.number == 1
        assert project_id.slug == "a"

    def test_valid_max_number(self) -> None:
        """Accept maximum number 999."""
        project_id = ProjectId.parse("PROJ-999-test")
        assert project_id.number == 999

    def test_valid_complex_slug(self) -> None:
        """Accept complex kebab-case slug."""
        project_id = ProjectId.parse("PROJ-001-my-complex-project-name")
        assert project_id.slug == "my-complex-project-name"

    def test_valid_slug_with_numbers(self) -> None:
        """Accept slug with numbers."""
        project_id = ProjectId.parse("PROJ-001-version2")
        assert project_id.slug == "version2"

    def test_reject_none_value(self) -> None:
        """Reject None input."""
        with pytest.raises(InvalidProjectIdError):
            ProjectId.parse(None)

    def test_reject_empty_value(self) -> None:
        """Reject empty string."""
        with pytest.raises(InvalidProjectIdError):
            ProjectId.parse("")

    def test_reject_zero_number(self) -> None:
        """Reject number 000."""
        with pytest.raises(InvalidProjectIdError):
            ProjectId.parse("PROJ-000-test")

    def test_reject_missing_slug(self) -> None:
        """Reject format without slug."""
        with pytest.raises(InvalidProjectIdError):
            ProjectId.parse("PROJ-001-")

    def test_reject_uppercase_in_slug(self) -> None:
        """Reject uppercase characters in slug."""
        with pytest.raises(InvalidProjectIdError):
            ProjectId.parse("PROJ-001-TestProject")

    def test_reject_underscore_in_slug(self) -> None:
        """Reject underscore in slug (must be kebab-case)."""
        with pytest.raises(InvalidProjectIdError):
            ProjectId.parse("PROJ-001-test_project")

    def test_reject_slug_starting_with_number(self) -> None:
        """Reject slug starting with number."""
        with pytest.raises(InvalidProjectIdError):
            ProjectId.parse("PROJ-001-1test")

    def test_reject_wrong_prefix(self) -> None:
        """Reject non-PROJ prefix."""
        with pytest.raises(InvalidProjectIdError):
            ProjectId.parse("TASK-001-test")


# =============================================================================
# Edge Cases Tests
# =============================================================================


class TestProjectIdEdgeCases:
    """Edge case and boundary tests."""

    def test_whitespace_is_stripped(self) -> None:
        """Leading/trailing whitespace should be handled."""
        project_id = ProjectId.parse("  PROJ-001-test  ")
        assert project_id.value == "PROJ-001-test"

    def test_single_char_slug(self) -> None:
        """Single character slug is valid."""
        project_id = ProjectId.parse("PROJ-001-x")
        assert project_id.slug == "x"

    def test_max_length_slug(self) -> None:
        """Maximum length slug (50 chars) should work."""
        long_slug = "a" * 50
        project_id = ProjectId.create(1, long_slug)
        assert len(project_id.slug) == 50

    def test_exceeds_max_slug_length(self) -> None:
        """Slug exceeding 50 chars should be rejected."""
        long_slug = "a" * 51
        with pytest.raises(InvalidProjectIdError):
            ProjectId.create(1, long_slug)

    def test_number_boundary_001(self) -> None:
        """Minimum valid number is 001."""
        project_id = ProjectId.parse("PROJ-001-test")
        assert project_id.number == 1

    def test_create_with_invalid_number_type(self) -> None:
        """create() with non-integer number should fail."""
        with pytest.raises(InvalidProjectIdError):
            ProjectId.create("five", "test")

    def test_create_with_negative_number(self) -> None:
        """create() with negative number should fail."""
        with pytest.raises(InvalidProjectIdError):
            ProjectId.create(-1, "test")

    def test_create_with_zero_number(self) -> None:
        """create() with zero should fail."""
        with pytest.raises(InvalidProjectIdError):
            ProjectId.create(0, "test")

    def test_create_with_number_over_999(self) -> None:
        """create() with number > 999 should fail."""
        with pytest.raises(InvalidProjectIdError):
            ProjectId.create(1000, "test")
