"""Integration tests for Infrastructure Layer Adapters.

Test Categories:
    - OsEnvironmentAdapter: Environment variable handling
    - FilesystemProjectAdapter: Edge cases with real filesystem

References:
    - ENFORCE-010: Infrastructure Tests
    - Hexagonal Architecture: Adapter testing
"""
from __future__ import annotations

import os
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

from src.session_management.infrastructure.adapters.os_environment_adapter import (
    OsEnvironmentAdapter,
)
from src.session_management.infrastructure.adapters.filesystem_project_adapter import (
    FilesystemProjectAdapter,
)
from src.session_management.domain.value_objects.project_status import ProjectStatus


# =============================================================================
# OsEnvironmentAdapter Tests (ENFORCE-010.1)
# =============================================================================


class TestOsEnvironmentAdapterHappyPath:
    """Happy path tests for OsEnvironmentAdapter."""

    def test_get_env_reads_jerry_project(self) -> None:
        """get_env should read JERRY_PROJECT from environment."""
        adapter = OsEnvironmentAdapter()

        with patch.dict(os.environ, {"JERRY_PROJECT": "PROJ-001-test"}):
            result = adapter.get_env("JERRY_PROJECT")

        assert result == "PROJ-001-test"

    def test_get_env_returns_none_when_unset(self) -> None:
        """get_env should return None when variable is not set."""
        adapter = OsEnvironmentAdapter()

        # Ensure the variable is not set
        env = os.environ.copy()
        env.pop("TEST_UNSET_VAR", None)

        with patch.dict(os.environ, env, clear=True):
            result = adapter.get_env("TEST_UNSET_VAR")

        assert result is None

    def test_get_env_or_default_returns_value(self) -> None:
        """get_env_or_default should return value when set."""
        adapter = OsEnvironmentAdapter()

        with patch.dict(os.environ, {"MY_VAR": "my_value"}):
            result = adapter.get_env_or_default("MY_VAR", "default")

        assert result == "my_value"

    def test_get_env_or_default_returns_default(self) -> None:
        """get_env_or_default should return default when unset."""
        adapter = OsEnvironmentAdapter()

        env = os.environ.copy()
        env.pop("MY_UNSET_VAR", None)

        with patch.dict(os.environ, env, clear=True):
            result = adapter.get_env_or_default("MY_UNSET_VAR", "fallback")

        assert result == "fallback"


class TestOsEnvironmentAdapterEdgeCases:
    """Edge case tests for OsEnvironmentAdapter."""

    def test_get_env_with_empty_string_returns_none(self) -> None:
        """get_env should return None for empty string value."""
        adapter = OsEnvironmentAdapter()

        with patch.dict(os.environ, {"EMPTY_VAR": ""}):
            result = adapter.get_env("EMPTY_VAR")

        assert result is None

    def test_get_env_with_whitespace_only_returns_none(self) -> None:
        """get_env should return None for whitespace-only value."""
        adapter = OsEnvironmentAdapter()

        with patch.dict(os.environ, {"WHITESPACE_VAR": "   "}):
            result = adapter.get_env("WHITESPACE_VAR")

        assert result is None

    def test_get_env_strips_whitespace(self) -> None:
        """get_env should strip leading/trailing whitespace."""
        adapter = OsEnvironmentAdapter()

        with patch.dict(os.environ, {"PADDED_VAR": "  value  "}):
            result = adapter.get_env("PADDED_VAR")

        assert result == "value"

    def test_get_env_with_newline(self) -> None:
        """get_env should handle values with embedded newlines."""
        adapter = OsEnvironmentAdapter()

        with patch.dict(os.environ, {"NEWLINE_VAR": "value\nwith\nnewlines"}):
            result = adapter.get_env("NEWLINE_VAR")

        assert result == "value\nwith\nnewlines"

    def test_get_env_with_special_characters(self) -> None:
        """get_env should handle values with special characters."""
        adapter = OsEnvironmentAdapter()

        with patch.dict(os.environ, {"SPECIAL_VAR": "path/to/file:with=special&chars"}):
            result = adapter.get_env("SPECIAL_VAR")

        assert result == "path/to/file:with=special&chars"


class TestOsEnvironmentAdapterNegativeCases:
    """Negative test cases for OsEnvironmentAdapter."""

    def test_get_env_with_none_name_raises(self) -> None:
        """get_env with None name should raise TypeError."""
        adapter = OsEnvironmentAdapter()

        with pytest.raises(TypeError):
            adapter.get_env(None)  # type: ignore

    def test_get_env_with_empty_name(self) -> None:
        """get_env with empty name should return None (no such var)."""
        adapter = OsEnvironmentAdapter()

        result = adapter.get_env("")

        assert result is None


# =============================================================================
# FilesystemProjectAdapter Edge Cases (ENFORCE-010.2)
# =============================================================================


@pytest.fixture
def temp_projects_dir():
    """Create a temporary projects directory for testing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


class TestFilesystemAdapterEdgeCases:
    """Edge case tests for FilesystemProjectAdapter."""

    def test_adapter_with_empty_directory(self, temp_projects_dir: str) -> None:
        """Adapter should return empty list for empty directory."""
        adapter = FilesystemProjectAdapter()

        result = adapter.scan_projects(temp_projects_dir)

        assert result == []

    def test_adapter_with_only_archive_directory(
        self, temp_projects_dir: str
    ) -> None:
        """Adapter should ignore archive directory."""
        Path(temp_projects_dir, "archive").mkdir()

        adapter = FilesystemProjectAdapter()
        result = adapter.scan_projects(temp_projects_dir)

        assert result == []

    def test_adapter_with_mixed_valid_invalid_dirs(
        self, temp_projects_dir: str
    ) -> None:
        """Adapter should return only valid project directories."""
        base = Path(temp_projects_dir)
        # Valid project
        (base / "PROJ-001-valid").mkdir()
        # Invalid directories
        (base / "invalid").mkdir()
        (base / "random-folder").mkdir()
        (base / ".hidden").mkdir()

        adapter = FilesystemProjectAdapter()
        result = adapter.scan_projects(temp_projects_dir)

        assert len(result) == 1
        assert result[0].id.slug == "valid"

    def test_adapter_with_unicode_in_slug(self, temp_projects_dir: str) -> None:
        """Adapter should handle unicode in directory names gracefully."""
        base = Path(temp_projects_dir)
        # Unicode characters in slug - these won't match the pattern
        # but shouldn't crash
        (base / "PROJ-001-tëst").mkdir()

        adapter = FilesystemProjectAdapter()
        result = adapter.scan_projects(temp_projects_dir)

        # The pattern requires lowercase ASCII, so unicode won't match
        assert len(result) == 0

    def test_adapter_with_spaces_in_path(self) -> None:
        """Adapter should handle paths with spaces."""
        with tempfile.TemporaryDirectory() as parent:
            spaced_dir = Path(parent) / "my projects"
            spaced_dir.mkdir()
            (spaced_dir / "PROJ-001-test").mkdir()

            adapter = FilesystemProjectAdapter()
            result = adapter.scan_projects(str(spaced_dir))

            assert len(result) == 1
            assert result[0].id.slug == "test"

    def test_adapter_with_deeply_nested_structure(
        self, temp_projects_dir: str
    ) -> None:
        """Adapter should only scan top-level directories."""
        base = Path(temp_projects_dir)
        # Create nested structure
        (base / "PROJ-001-outer").mkdir()
        (base / "PROJ-001-outer" / "PROJ-002-inner").mkdir()

        adapter = FilesystemProjectAdapter()
        result = adapter.scan_projects(temp_projects_dir)

        # Should only find top-level project
        assert len(result) == 1
        assert result[0].id.slug == "outer"


class TestFilesystemAdapterFailureScenarios:
    """Failure scenario tests for FilesystemProjectAdapter."""

    def test_adapter_handles_corrupt_worktracker(
        self, temp_projects_dir: str
    ) -> None:
        """Adapter should handle corrupt/binary WORKTRACKER.md gracefully."""
        base = Path(temp_projects_dir)
        proj = base / "PROJ-001-corrupt"
        proj.mkdir()
        # Write binary data as WORKTRACKER
        (proj / "WORKTRACKER.md").write_bytes(b"\x00\x01\x02\xff\xfe")
        (proj / "PLAN.md").write_text("# Plan")

        adapter = FilesystemProjectAdapter()
        result = adapter.scan_projects(temp_projects_dir)

        # Should still find the project, status will be UNKNOWN
        assert len(result) == 1
        assert result[0].status == ProjectStatus.UNKNOWN

    def test_adapter_handles_extremely_large_worktracker(
        self, temp_projects_dir: str
    ) -> None:
        """Adapter should handle very large WORKTRACKER.md without issues."""
        base = Path(temp_projects_dir)
        proj = base / "PROJ-001-large"
        proj.mkdir()
        # Create a large file (10KB of repeated text)
        large_content = "IN_PROGRESS\n" + ("x" * 10000)
        (proj / "WORKTRACKER.md").write_text(large_content)
        (proj / "PLAN.md").write_text("# Plan")

        adapter = FilesystemProjectAdapter()
        result = adapter.scan_projects(temp_projects_dir)

        assert len(result) == 1
        # Should still detect status from first 2KB
        assert result[0].status == ProjectStatus.IN_PROGRESS

    def test_adapter_handles_empty_worktracker(
        self, temp_projects_dir: str
    ) -> None:
        """Adapter should handle empty WORKTRACKER.md."""
        base = Path(temp_projects_dir)
        proj = base / "PROJ-001-empty"
        proj.mkdir()
        (proj / "WORKTRACKER.md").write_text("")
        (proj / "PLAN.md").write_text("# Plan")

        adapter = FilesystemProjectAdapter()
        result = adapter.scan_projects(temp_projects_dir)

        assert len(result) == 1
        assert result[0].status == ProjectStatus.UNKNOWN

    def test_adapter_handles_file_with_bom(
        self, temp_projects_dir: str
    ) -> None:
        """Adapter should handle files with UTF-8 BOM."""
        base = Path(temp_projects_dir)
        proj = base / "PROJ-001-bom"
        proj.mkdir()
        # Write with UTF-8 BOM
        (proj / "WORKTRACKER.md").write_bytes(
            b"\xef\xbb\xbf# Tracker\nIN_PROGRESS"
        )
        (proj / "PLAN.md").write_text("# Plan")

        adapter = FilesystemProjectAdapter()
        result = adapter.scan_projects(temp_projects_dir)

        assert len(result) == 1
        assert result[0].status == ProjectStatus.IN_PROGRESS


# =============================================================================
# Symlink Tests (Platform Dependent)
# =============================================================================


@pytest.mark.skipif(
    os.name == "nt", reason="Symlinks may require admin on Windows"
)
class TestFilesystemAdapterSymlinks:
    """Symlink tests for FilesystemProjectAdapter (Unix-like systems)."""

    def test_adapter_follows_symlinked_project(
        self, temp_projects_dir: str
    ) -> None:
        """Adapter should follow symlinks to project directories."""
        base = Path(temp_projects_dir)
        # Create actual project in a different location
        actual_proj = base / "actual-projects" / "PROJ-001-real"
        actual_proj.mkdir(parents=True)
        (actual_proj / "PLAN.md").write_text("# Plan")
        (actual_proj / "WORKTRACKER.md").write_text("# Tracker\nIN_PROGRESS")

        # Create symlink
        symlink = base / "PROJ-001-linked"
        symlink.symlink_to(actual_proj)

        adapter = FilesystemProjectAdapter()
        result = adapter.scan_projects(temp_projects_dir)

        # Should find the symlinked project
        assert len(result) == 1
        assert result[0].id.slug == "linked"
        assert result[0].status == ProjectStatus.IN_PROGRESS
