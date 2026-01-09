"""
Unit Tests - Domain Layer

Pure unit tests for domain models. No I/O, no mocks needed.
These tests verify that domain objects enforce their invariants correctly.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

# Add project root to path for imports from src/
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from src.session_management.domain import (
    ProjectId,
    ProjectStatus,
    ProjectInfo,
    ValidationResult,
    InvalidProjectIdError,
    DomainError,
    ProjectNotFoundError,
    ProjectValidationError,
)


# =============================================================================
# ProjectId Tests
# =============================================================================

class TestProjectIdHappyPath:
    """Happy path tests for ProjectId value object."""

    def test_project_id_creation_with_valid_format_succeeds(self):
        """Valid project ID should parse successfully."""
        project_id = ProjectId.parse("PROJ-001-plugin-cleanup")
        assert project_id.value == "PROJ-001-plugin-cleanup"

    def test_project_id_extracts_number_correctly(self):
        """Number should be extracted and converted to int."""
        project_id = ProjectId.parse("PROJ-042-my-project")
        assert project_id.number == 42

    def test_project_id_extracts_slug_correctly(self):
        """Slug should be extracted correctly."""
        project_id = ProjectId.parse("PROJ-001-my-awesome-project")
        assert project_id.slug == "my-awesome-project"

    def test_project_id_create_with_components_succeeds(self):
        """Creating from components should work."""
        project_id = ProjectId.create(number=5, slug="test-project")
        assert project_id.value == "PROJ-005-test-project"
        assert project_id.number == 5
        assert project_id.slug == "test-project"

    def test_project_id_str_returns_value(self):
        """String representation should return the full ID."""
        project_id = ProjectId.parse("PROJ-001-test")
        assert str(project_id) == "PROJ-001-test"


class TestProjectIdEdgeCases:
    """Edge case tests for ProjectId value object."""

    def test_project_id_with_leading_zeros_preserved(self):
        """Leading zeros in the value string should be preserved."""
        project_id = ProjectId.parse("PROJ-001-test")
        assert project_id.value == "PROJ-001-test"
        assert project_id.number == 1

    def test_project_id_with_single_digit_number_fails(self):
        """Single digit numbers (not zero-padded) should fail."""
        with pytest.raises(InvalidProjectIdError) as exc_info:
            ProjectId.parse("PROJ-1-test")
        assert "Must match format" in str(exc_info.value)

    def test_project_id_with_four_digit_number_fails(self):
        """Four digit numbers should fail."""
        with pytest.raises(InvalidProjectIdError) as exc_info:
            ProjectId.parse("PROJ-1000-test")
        assert "Must match format" in str(exc_info.value)

    def test_project_id_with_empty_slug_fails(self):
        """Empty slug should fail."""
        with pytest.raises(InvalidProjectIdError) as exc_info:
            ProjectId.create(number=1, slug="")
        assert "empty" in str(exc_info.value).lower()

    def test_project_id_with_underscore_slug_fails(self):
        """Underscores in slug should fail (must be kebab-case)."""
        with pytest.raises(InvalidProjectIdError) as exc_info:
            ProjectId.parse("PROJ-001-test_project")
        assert "Must match format" in str(exc_info.value)

    def test_project_id_with_uppercase_slug_fails(self):
        """Uppercase in slug should fail."""
        with pytest.raises(InvalidProjectIdError) as exc_info:
            ProjectId.parse("PROJ-001-TestProject")
        assert "Must match format" in str(exc_info.value)

    def test_project_id_slug_with_special_chars_fails(self):
        """Special characters in slug should fail."""
        with pytest.raises(InvalidProjectIdError) as exc_info:
            ProjectId.parse("PROJ-001-test@project")
        assert "Must match format" in str(exc_info.value)

    def test_project_id_slug_with_spaces_fails(self):
        """Spaces in slug should fail."""
        with pytest.raises(InvalidProjectIdError) as exc_info:
            ProjectId.parse("PROJ-001-test project")
        assert "Must match format" in str(exc_info.value)

    def test_project_id_slug_starting_with_number_fails(self):
        """Slug starting with number should fail."""
        with pytest.raises(InvalidProjectIdError) as exc_info:
            ProjectId.parse("PROJ-001-123test")
        assert "Must match format" in str(exc_info.value)


class TestProjectIdNegative:
    """Negative tests for ProjectId value object."""

    def test_project_id_with_null_raises_error(self):
        """None value should raise error."""
        with pytest.raises(InvalidProjectIdError) as exc_info:
            ProjectId.parse(None)
        assert "None" in str(exc_info.value)

    def test_project_id_with_empty_string_raises_error(self):
        """Empty string should raise error."""
        with pytest.raises(InvalidProjectIdError) as exc_info:
            ProjectId.parse("")
        assert "empty" in str(exc_info.value).lower()

    def test_project_id_without_proj_prefix_raises_error(self):
        """Missing PROJ prefix should raise error."""
        with pytest.raises(InvalidProjectIdError) as exc_info:
            ProjectId.parse("001-test")
        assert "Must match format" in str(exc_info.value)

    def test_project_id_without_number_raises_error(self):
        """Missing number should raise error."""
        with pytest.raises(InvalidProjectIdError) as exc_info:
            ProjectId.parse("PROJ--test")
        assert "Must match format" in str(exc_info.value)

    def test_project_id_without_slug_raises_error(self):
        """Missing slug should raise error."""
        with pytest.raises(InvalidProjectIdError) as exc_info:
            ProjectId.parse("PROJ-001-")
        assert "Must match format" in str(exc_info.value)

    def test_project_id_with_wrong_delimiter_raises_error(self):
        """Wrong delimiter should raise error."""
        with pytest.raises(InvalidProjectIdError) as exc_info:
            ProjectId.parse("PROJ_001_test")
        assert "Must match format" in str(exc_info.value)

    def test_project_id_with_lowercase_prefix_raises_error(self):
        """Lowercase PROJ prefix should raise error."""
        with pytest.raises(InvalidProjectIdError) as exc_info:
            ProjectId.parse("proj-001-test")
        assert "Must match format" in str(exc_info.value)

    def test_project_id_with_negative_number_raises_error(self):
        """Negative number should raise error when using create()."""
        with pytest.raises(InvalidProjectIdError) as exc_info:
            ProjectId.create(number=-1, slug="test")
        assert "must be between" in str(exc_info.value).lower()


class TestProjectIdBoundary:
    """Boundary tests for ProjectId value object."""

    def test_project_id_number_000_is_invalid(self):
        """Number 000 should be invalid."""
        with pytest.raises(InvalidProjectIdError) as exc_info:
            ProjectId.parse("PROJ-000-test")
        assert "000" in str(exc_info.value) or "cannot be" in str(exc_info.value).lower()

    def test_project_id_number_001_is_valid(self):
        """Number 001 (minimum) should be valid."""
        project_id = ProjectId.parse("PROJ-001-test")
        assert project_id.number == 1

    def test_project_id_number_999_is_valid(self):
        """Number 999 (maximum) should be valid."""
        project_id = ProjectId.parse("PROJ-999-test")
        assert project_id.number == 999

    def test_project_id_slug_min_length_1_char_valid(self):
        """Single character slug should be valid."""
        project_id = ProjectId.parse("PROJ-001-a")
        assert project_id.slug == "a"

    def test_project_id_slug_max_length_50_chars_valid(self):
        """50 character slug should be valid."""
        slug = "a" + "-b" * 24 + "-c"  # Creates a 50-char slug
        # Actually let's create a proper 50-char kebab-case slug
        slug = "a" * 50  # Simple 50 a's
        project_id = ProjectId.create(number=1, slug=slug)
        assert len(project_id.slug) == 50

    def test_project_id_slug_exceeds_max_length_fails(self):
        """51+ character slug should fail."""
        slug = "a" * 51
        with pytest.raises(InvalidProjectIdError) as exc_info:
            ProjectId.create(number=1, slug=slug)
        assert "maximum length" in str(exc_info.value).lower() or "50" in str(exc_info.value)


# =============================================================================
# ProjectStatus Tests
# =============================================================================

class TestProjectStatus:
    """Tests for ProjectStatus enum."""

    def test_project_status_from_string_in_progress(self):
        """IN_PROGRESS string should parse correctly."""
        status = ProjectStatus.from_string("IN_PROGRESS")
        assert status == ProjectStatus.IN_PROGRESS

    def test_project_status_from_string_case_insensitive(self):
        """Parsing should be case insensitive."""
        status = ProjectStatus.from_string("in_progress")
        assert status == ProjectStatus.IN_PROGRESS

    def test_project_status_from_string_with_spaces(self):
        """Spaces should be normalized to underscores."""
        status = ProjectStatus.from_string("IN PROGRESS")
        assert status == ProjectStatus.IN_PROGRESS

    def test_project_status_from_string_unknown_returns_unknown(self):
        """Unknown string should return UNKNOWN status."""
        status = ProjectStatus.from_string("INVALID_STATUS")
        assert status == ProjectStatus.UNKNOWN

    def test_project_status_str_representation(self):
        """String representation should be human readable."""
        status = ProjectStatus.IN_PROGRESS
        assert str(status) == "In Progress"


# =============================================================================
# ValidationResult Tests
# =============================================================================

class TestValidationResult:
    """Tests for ValidationResult value object."""

    def test_validation_result_success_is_valid(self):
        """Success result should be valid."""
        result = ValidationResult.success()
        assert result.is_valid is True
        assert bool(result) is True

    def test_validation_result_success_with_warnings(self):
        """Success can have warnings."""
        result = ValidationResult.success(warnings=["Missing optional file"])
        assert result.is_valid is True
        assert result.has_warnings is True
        assert len(result.messages) == 1

    def test_validation_result_failure_contains_message(self):
        """Failure result should contain error messages."""
        result = ValidationResult.failure(["Error 1", "Error 2"])
        assert result.is_valid is False
        assert result.has_errors is True
        assert len(result.messages) == 2

    def test_validation_result_failure_requires_message(self):
        """Failure without messages should raise error."""
        with pytest.raises(ValueError) as exc_info:
            ValidationResult.failure([])
        assert "at least one error" in str(exc_info.value).lower()

    def test_validation_result_first_message(self):
        """First message should be accessible."""
        result = ValidationResult.failure(["First error", "Second error"])
        assert result.first_message == "First error"

    def test_validation_result_first_message_when_empty(self):
        """First message should be None when no messages."""
        result = ValidationResult.success()
        assert result.first_message is None

    def test_validation_result_bool_false_when_invalid(self):
        """Boolean context should return False for invalid."""
        result = ValidationResult.failure(["Error"])
        assert bool(result) is False


# =============================================================================
# ProjectInfo Tests
# =============================================================================

class TestProjectInfo:
    """Tests for ProjectInfo entity."""

    def test_project_info_creation_with_all_fields_succeeds(self):
        """Creating with all fields should work."""
        project_id = ProjectId.parse("PROJ-001-test")
        info = ProjectInfo(
            id=project_id,
            status=ProjectStatus.IN_PROGRESS,
            has_plan=True,
            has_tracker=True,
            path="/path/to/project",
        )
        assert info.id == project_id
        assert info.status == ProjectStatus.IN_PROGRESS
        assert info.has_plan is True
        assert info.has_tracker is True
        assert info.path == "/path/to/project"

    def test_project_info_create_from_string_id(self):
        """Create factory should accept string ID."""
        info = ProjectInfo.create(
            project_id="PROJ-001-test",
            status="IN_PROGRESS",
            has_plan=True,
            has_tracker=True,
        )
        assert info.id.value == "PROJ-001-test"
        assert info.status == ProjectStatus.IN_PROGRESS

    def test_project_info_with_none_status_defaults_to_unknown(self):
        """Default status should be UNKNOWN."""
        project_id = ProjectId.parse("PROJ-001-test")
        info = ProjectInfo(id=project_id)
        assert info.status == ProjectStatus.UNKNOWN

    def test_project_info_with_invalid_id_raises_error(self):
        """Creating with invalid string ID should raise error."""
        with pytest.raises(InvalidProjectIdError):
            ProjectInfo.create(project_id="invalid-id")

    def test_project_info_is_complete_when_has_both_files(self):
        """is_complete should be True when both files exist."""
        info = ProjectInfo.create(
            project_id="PROJ-001-test",
            has_plan=True,
            has_tracker=True,
        )
        assert info.is_complete is True

    def test_project_info_is_not_complete_when_missing_plan(self):
        """is_complete should be False when PLAN.md missing."""
        info = ProjectInfo.create(
            project_id="PROJ-001-test",
            has_plan=False,
            has_tracker=True,
        )
        assert info.is_complete is False

    def test_project_info_is_active_for_in_progress(self):
        """is_active should be True for IN_PROGRESS."""
        info = ProjectInfo.create(
            project_id="PROJ-001-test",
            status="IN_PROGRESS",
        )
        assert info.is_active is True

    def test_project_info_is_not_active_for_archived(self):
        """is_active should be False for ARCHIVED."""
        info = ProjectInfo.create(
            project_id="PROJ-001-test",
            status="ARCHIVED",
        )
        assert info.is_active is False

    def test_project_info_warnings_lists_missing_files(self):
        """warnings should list missing files."""
        info = ProjectInfo.create(
            project_id="PROJ-001-test",
            has_plan=False,
            has_tracker=False,
        )
        warnings = info.warnings
        assert len(warnings) == 2
        assert any("PLAN" in w for w in warnings)
        assert any("WORKTRACKER" in w for w in warnings)


# =============================================================================
# DomainError Tests
# =============================================================================

class TestDomainErrors:
    """Tests for domain error hierarchy."""

    def test_domain_error_is_exception(self):
        """DomainError should be an Exception."""
        error = DomainError("Test error")
        assert isinstance(error, Exception)
        assert str(error) == "Test error"

    def test_domain_error_has_message_attribute(self):
        """DomainError should have message attribute."""
        error = DomainError("Test message")
        assert error.message == "Test message"

    def test_invalid_project_id_error_includes_value_and_reason(self):
        """InvalidProjectIdError should include both value and reason."""
        error = InvalidProjectIdError("bad-id", "Invalid format")
        assert error.value == "bad-id"
        assert error.reason == "Invalid format"
        assert "bad-id" in str(error)
        assert "Invalid format" in str(error)

    def test_invalid_project_id_error_inherits_from_domain_error(self):
        """InvalidProjectIdError should inherit from DomainError."""
        error = InvalidProjectIdError("bad-id", "reason")
        assert isinstance(error, DomainError)

    def test_project_not_found_error_with_id_only(self):
        """ProjectNotFoundError should work with just project ID."""
        error = ProjectNotFoundError("PROJ-001-test")
        assert error.project_id == "PROJ-001-test"
        assert error.path is None
        assert "PROJ-001-test" in str(error)
        assert "not found" in str(error).lower()

    def test_project_not_found_error_with_path(self):
        """ProjectNotFoundError should include path when provided."""
        error = ProjectNotFoundError("PROJ-001-test", path="/path/to/project")
        assert error.project_id == "PROJ-001-test"
        assert error.path == "/path/to/project"
        assert "/path/to/project" in str(error)

    def test_project_validation_error_with_issues(self):
        """ProjectValidationError should list all issues."""
        error = ProjectValidationError("PROJ-001-test", ["Missing PLAN.md", "Invalid status"])
        assert error.project_id == "PROJ-001-test"
        assert len(error.issues) == 2
        assert "Missing PLAN.md" in str(error)
        assert "Invalid status" in str(error)

    def test_project_validation_error_inherits_from_domain_error(self):
        """ProjectValidationError should inherit from DomainError."""
        error = ProjectValidationError("PROJ-001-test", ["Issue"])
        assert isinstance(error, DomainError)
