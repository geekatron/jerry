"""
Unit Tests: Path Validation Logic

Tests the core validation logic for document path references.
These tests are pure functions with no I/O dependencies.

Test Categories:
- Happy Path: Valid project-centric paths
- Edge Cases: Boundary conditions and variations
- Negative: Invalid/old path formats

Migration History:
    Originally: projects/PROJ-001-plugin-cleanup/tests/unit/test_path_validation.py
    Migrated: 2026-01-10 (TD-005)
    Commit: a911859 (original creation for BUG-001)
"""
from __future__ import annotations

import re

import pytest


# =============================================================================
# Path Validation Functions (Under Test)
# =============================================================================


def is_valid_project_path(path: str) -> bool:
    """
    Validate that a path follows the project-centric convention.

    Valid format: projects/PROJ-{NNN}-{slug}/{category}/...
    """
    pattern = r"^projects/PROJ-\d{3}-[a-z0-9-]+/(research|synthesis|analysis|decisions|reports|investigations|reviews)/"
    return bool(re.match(pattern, path))


def is_old_docs_path(path: str) -> bool:
    """
    Detect if a path uses the deprecated docs/ convention.

    Old format: docs/{category}/PROJ-{NNN}-...
    """
    pattern = r"^docs/(research|synthesis|analysis|decisions)/"
    return bool(re.match(pattern, path))


def extract_category_from_path(path: str) -> str | None:
    """Extract the category (research, synthesis, etc.) from a path."""
    match = re.search(r"/(research|synthesis|analysis|decisions|reports|investigations|reviews)/", path)
    return match.group(1) if match else None


def normalize_path_to_project_centric(old_path: str, project_id: str) -> str:
    """
    Convert an old docs/ path to project-centric format.

    Example:
        docs/research/PROJ-001-e-001.md
        -> projects/{project_id}/research/PROJ-001-e-001.md
    """
    if not is_old_docs_path(old_path):
        return old_path  # Already normalized or different format

    # Extract category and filename
    match = re.match(r"docs/(research|synthesis|analysis|decisions)/(.+)", old_path)
    if not match:
        return old_path

    category, filename = match.groups()
    return f"projects/{project_id}/{category}/{filename}"


# =============================================================================
# HAPPY PATH TESTS
# =============================================================================


class TestValidProjectPaths:
    """Tests for valid project-centric path formats."""

    def test_valid_research_path(self) -> None:
        """Research paths should be recognized as valid."""
        path = "projects/PROJ-001-plugin-cleanup/research/PROJ-001-e-001-worktracker-proposal-extraction.md"
        assert is_valid_project_path(path) is True

    def test_valid_synthesis_path(self) -> None:
        """Synthesis paths should be recognized as valid."""
        path = "projects/PROJ-001-plugin-cleanup/synthesis/PROJ-001-e-006-unified-architecture-canon.md"
        assert is_valid_project_path(path) is True

    def test_valid_analysis_path(self) -> None:
        """Analysis paths should be recognized as valid."""
        path = "projects/PROJ-001-plugin-cleanup/analysis/PROJ-001-e-007-implementation-gap-analysis.md"
        assert is_valid_project_path(path) is True

    def test_valid_decisions_path(self) -> None:
        """Decisions paths should be recognized as valid."""
        path = "projects/PROJ-001-plugin-cleanup/decisions/ADR-IMPL-001-unified-alignment.md"
        assert is_valid_project_path(path) is True

    def test_valid_reports_path(self) -> None:
        """Reports paths should be recognized as valid."""
        path = "projects/PROJ-001-plugin-cleanup/reports/PROJ-001-e-010-synthesis-status-report.md"
        assert is_valid_project_path(path) is True

    def test_valid_investigations_path(self) -> None:
        """Investigations paths should be recognized as valid."""
        path = "projects/PROJ-002-example/investigations/INV-001-root-cause.md"
        assert is_valid_project_path(path) is True

    def test_valid_reviews_path(self) -> None:
        """Reviews paths should be recognized as valid."""
        path = "projects/PROJ-003-test/reviews/REV-001-design-review.md"
        assert is_valid_project_path(path) is True

    def test_category_extraction_research(self) -> None:
        """Should extract 'research' category from path."""
        path = "projects/PROJ-001-plugin-cleanup/research/file.md"
        assert extract_category_from_path(path) == "research"

    def test_category_extraction_synthesis(self) -> None:
        """Should extract 'synthesis' category from path."""
        path = "projects/PROJ-001-plugin-cleanup/synthesis/file.md"
        assert extract_category_from_path(path) == "synthesis"


# =============================================================================
# EDGE CASE TESTS
# =============================================================================


class TestEdgeCases:
    """Tests for boundary conditions and edge cases."""

    def test_path_with_three_digit_project_number(self) -> None:
        """Project numbers can be 001-999."""
        path = "projects/PROJ-999-max-number/research/file.md"
        assert is_valid_project_path(path) is True

    def test_path_with_single_char_slug(self) -> None:
        """Slug can be a single character."""
        path = "projects/PROJ-001-x/research/file.md"
        assert is_valid_project_path(path) is True

    def test_path_with_numeric_slug(self) -> None:
        """Slug can contain numbers."""
        path = "projects/PROJ-001-v2-update/research/file.md"
        assert is_valid_project_path(path) is True

    def test_path_with_long_slug(self) -> None:
        """Slug can be long."""
        path = "projects/PROJ-001-this-is-a-very-long-project-slug-name/research/file.md"
        assert is_valid_project_path(path) is True

    def test_deeply_nested_file(self) -> None:
        """Files can be nested within category."""
        path = "projects/PROJ-001-plugin-cleanup/research/subcategory/nested/file.md"
        assert is_valid_project_path(path) is True

    def test_category_extraction_with_nested_path(self) -> None:
        """Category should be extracted even with nested paths."""
        path = "projects/PROJ-001-plugin-cleanup/analysis/subdir/file.md"
        assert extract_category_from_path(path) == "analysis"


# =============================================================================
# NEGATIVE TESTS
# =============================================================================


class TestOldPathDetection:
    """Tests for detecting deprecated docs/ paths."""

    def test_old_docs_research_path_detected(self) -> None:
        """Old docs/research/ paths should be detected."""
        path = "docs/research/PROJ-001-e-001-worktracker-proposal-extraction.md"
        assert is_old_docs_path(path) is True

    def test_old_docs_synthesis_path_detected(self) -> None:
        """Old docs/synthesis/ paths should be detected."""
        path = "docs/synthesis/PROJ-001-e-006-unified-architecture-canon.md"
        assert is_old_docs_path(path) is True

    def test_old_docs_analysis_path_detected(self) -> None:
        """Old docs/analysis/ paths should be detected."""
        path = "docs/analysis/PROJ-001-e-007-implementation-gap-analysis.md"
        assert is_old_docs_path(path) is True

    def test_old_docs_decisions_path_detected(self) -> None:
        """Old docs/decisions/ paths should be detected."""
        path = "docs/decisions/ADR-IMPL-001-unified-alignment.md"
        assert is_old_docs_path(path) is True

    def test_project_path_not_detected_as_old(self) -> None:
        """Project-centric paths should NOT be detected as old."""
        path = "projects/PROJ-001-plugin-cleanup/research/file.md"
        assert is_old_docs_path(path) is False

    def test_old_path_invalid_as_project_path(self) -> None:
        """Old docs/ paths should NOT be valid project paths."""
        path = "docs/research/PROJ-001-e-001.md"
        assert is_valid_project_path(path) is False


class TestInvalidPaths:
    """Tests for paths that should be rejected."""

    def test_missing_proj_prefix(self) -> None:
        """Paths without PROJ- prefix should be invalid."""
        path = "projects/001-plugin-cleanup/research/file.md"
        assert is_valid_project_path(path) is False

    def test_wrong_project_number_format(self) -> None:
        """Project numbers must be exactly 3 digits."""
        path = "projects/PROJ-01-plugin-cleanup/research/file.md"
        assert is_valid_project_path(path) is False

    def test_uppercase_slug(self) -> None:
        """Slugs must be lowercase."""
        path = "projects/PROJ-001-Plugin-Cleanup/research/file.md"
        assert is_valid_project_path(path) is False

    def test_underscore_in_slug(self) -> None:
        """Slugs should use hyphens, not underscores."""
        path = "projects/PROJ-001-plugin_cleanup/research/file.md"
        assert is_valid_project_path(path) is False

    def test_invalid_category(self) -> None:
        """Invalid categories should be rejected."""
        path = "projects/PROJ-001-plugin-cleanup/invalid/file.md"
        assert is_valid_project_path(path) is False

    def test_no_category_in_path(self) -> None:
        """Category extraction should return None for paths without category."""
        path = "some/random/path/file.md"
        assert extract_category_from_path(path) is None


# =============================================================================
# PATH NORMALIZATION TESTS
# =============================================================================


class TestPathNormalization:
    """Tests for converting old paths to new format."""

    @pytest.fixture
    def default_project_id(self) -> str:
        """Default project ID for normalization tests."""
        return "PROJ-001-plugin-cleanup"

    def test_normalize_research_path(self, default_project_id: str) -> None:
        """Should normalize docs/research/ to projects/.../research/."""
        old = "docs/research/PROJ-001-e-001-worktracker-proposal-extraction.md"
        expected = f"projects/{default_project_id}/research/PROJ-001-e-001-worktracker-proposal-extraction.md"
        assert normalize_path_to_project_centric(old, default_project_id) == expected

    def test_normalize_synthesis_path(self, default_project_id: str) -> None:
        """Should normalize docs/synthesis/ to projects/.../synthesis/."""
        old = "docs/synthesis/PROJ-001-e-006-unified-architecture-canon.md"
        expected = f"projects/{default_project_id}/synthesis/PROJ-001-e-006-unified-architecture-canon.md"
        assert normalize_path_to_project_centric(old, default_project_id) == expected

    def test_normalize_analysis_path(self, default_project_id: str) -> None:
        """Should normalize docs/analysis/ to projects/.../analysis/."""
        old = "docs/analysis/PROJ-001-e-007-implementation-gap-analysis.md"
        expected = f"projects/{default_project_id}/analysis/PROJ-001-e-007-implementation-gap-analysis.md"
        assert normalize_path_to_project_centric(old, default_project_id) == expected

    def test_normalize_decisions_path(self, default_project_id: str) -> None:
        """Should normalize docs/decisions/ to projects/.../decisions/."""
        old = "docs/decisions/ADR-IMPL-001-unified-alignment.md"
        expected = f"projects/{default_project_id}/decisions/ADR-IMPL-001-unified-alignment.md"
        assert normalize_path_to_project_centric(old, default_project_id) == expected

    def test_already_normalized_path_unchanged(self, default_project_id: str) -> None:
        """Already normalized paths should be returned unchanged."""
        path = f"projects/{default_project_id}/research/file.md"
        assert normalize_path_to_project_centric(path, default_project_id) == path

    def test_normalize_with_custom_project_id(self) -> None:
        """Should support custom project ID."""
        old = "docs/research/file.md"
        expected = "projects/PROJ-002-other-project/research/file.md"
        assert normalize_path_to_project_centric(old, "PROJ-002-other-project") == expected


# =============================================================================
# BOUNDARY TESTS
# =============================================================================


class TestBoundaryConditions:
    """Tests for boundary conditions."""

    def test_empty_string(self) -> None:
        """Empty string should be invalid."""
        assert is_valid_project_path("") is False
        assert is_old_docs_path("") is False

    def test_project_number_000(self) -> None:
        """Project number 000 should technically be valid format-wise."""
        path = "projects/PROJ-000-test/research/file.md"
        # Format is valid even if semantically 000 might not be used
        assert is_valid_project_path(path) is True

    def test_whitespace_in_path(self) -> None:
        """Paths with whitespace should be invalid."""
        path = "projects/PROJ-001-plugin cleanup/research/file.md"
        assert is_valid_project_path(path) is False
