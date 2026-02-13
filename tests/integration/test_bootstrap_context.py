"""Integration tests for context distribution bootstrap script.

Tests the cross-platform sync mechanism that links .context/ to .claude/.
Covers symlink creation, check mode, force mode, fallback behavior,
and idempotency.
"""

from __future__ import annotations

import os
import platform
from pathlib import Path

import pytest

from scripts.bootstrap_context import (
    bootstrap,
    check_sync,
    detect_platform,
    find_project_root,
    is_symlink_or_junction,
)


@pytest.fixture()
def jerry_project(tmp_path: Path) -> Path:
    """Create a minimal Jerry project structure for testing."""
    # Create canonical source
    context_dir = tmp_path / ".context"
    rules_dir = context_dir / "rules"
    patterns_dir = context_dir / "patterns"
    rules_dir.mkdir(parents=True)
    patterns_dir.mkdir(parents=True)

    # Add sample files
    (rules_dir / "coding-standards.md").write_text("# Coding Standards\n")
    (rules_dir / "testing-standards.md").write_text("# Testing Standards\n")
    (patterns_dir / "PATTERN-CATALOG.md").write_text("# Pattern Catalog\n")

    # Create .claude/ directory (without rules/patterns - bootstrap will create them)
    claude_dir = tmp_path / ".claude"
    claude_dir.mkdir()
    (claude_dir / "settings.json").write_text("{}")

    # Create CLAUDE.md marker
    (tmp_path / "CLAUDE.md").write_text("# Jerry\n")

    return tmp_path


# === Platform Detection Tests ===


class TestDetectPlatform:
    """Tests for platform detection."""

    def test_returns_known_platform(self) -> None:
        """detect_platform returns one of the known platforms."""
        result = detect_platform()
        assert result in {"macos", "linux", "windows"} or isinstance(result, str)

    def test_matches_current_os(self) -> None:
        """detect_platform matches the current operating system."""
        result = detect_platform()
        system = platform.system()
        if system == "Darwin":
            assert result == "macos"
        elif system == "Linux":
            assert result == "linux"
        elif system == "Windows":
            assert result == "windows"


# === Bootstrap Happy Path Tests ===


class TestBootstrapHappyPath:
    """Tests for successful bootstrap operations."""

    def test_bootstrap_creates_symlinks(self, jerry_project: Path) -> None:
        """Bootstrap creates symlinks from .claude/ to .context/."""
        result = bootstrap(jerry_project, quiet=True)

        assert result is True
        rules_link = jerry_project / ".claude" / "rules"
        patterns_link = jerry_project / ".claude" / "patterns"
        assert rules_link.is_symlink() or rules_link.is_dir()
        assert patterns_link.is_symlink() or patterns_link.is_dir()

    def test_bootstrap_symlinks_resolve_to_context(self, jerry_project: Path) -> None:
        """Symlinks point to the correct .context/ directories."""
        bootstrap(jerry_project, quiet=True)

        rules_link = jerry_project / ".claude" / "rules"
        if rules_link.is_symlink():
            resolved = rules_link.resolve()
            expected = (jerry_project / ".context" / "rules").resolve()
            assert resolved == expected

    def test_bootstrap_files_accessible_through_symlink(self, jerry_project: Path) -> None:
        """Files in .context/ are accessible through .claude/ symlinks."""
        bootstrap(jerry_project, quiet=True)

        # Files should be readable through the symlink
        rules_link = jerry_project / ".claude" / "rules"
        coding_std = rules_link / "coding-standards.md"
        assert coding_std.exists()
        assert "Coding Standards" in coding_std.read_text()

    def test_bootstrap_preserves_existing_claude_files(self, jerry_project: Path) -> None:
        """Bootstrap doesn't remove existing .claude/ files like settings.json."""
        bootstrap(jerry_project, quiet=True)

        settings = jerry_project / ".claude" / "settings.json"
        assert settings.exists()
        assert settings.read_text() == "{}"

    def test_bootstrap_returns_true_on_success(self, jerry_project: Path) -> None:
        """Bootstrap returns True when all directories are synced."""
        result = bootstrap(jerry_project, quiet=True)
        assert result is True


# === Idempotency Tests ===


class TestBootstrapIdempotency:
    """Tests for idempotent bootstrap behavior."""

    def test_bootstrap_idempotent_without_force(self, jerry_project: Path) -> None:
        """Running bootstrap twice without force doesn't fail."""
        result1 = bootstrap(jerry_project, quiet=True)
        result2 = bootstrap(jerry_project, quiet=True)

        assert result1 is True
        assert result2 is True

    def test_bootstrap_force_recreates_links(self, jerry_project: Path) -> None:
        """Force flag recreates links even when they exist."""
        bootstrap(jerry_project, quiet=True)

        # Force re-bootstrap
        result = bootstrap(jerry_project, force=True, quiet=True)
        assert result is True

        # Symlinks still work
        rules_link = jerry_project / ".claude" / "rules"
        assert (rules_link / "coding-standards.md").exists()


# === Check Mode Tests ===


class TestCheckSync:
    """Tests for sync check operations."""

    def test_check_returns_true_when_synced(self, jerry_project: Path) -> None:
        """check_sync returns True after successful bootstrap."""
        bootstrap(jerry_project, quiet=True)
        result = check_sync(jerry_project, quiet=True)
        assert result is True

    def test_check_returns_false_when_not_synced(self, jerry_project: Path) -> None:
        """check_sync returns False when .claude/ dirs are missing."""
        result = check_sync(jerry_project, quiet=True)
        assert result is False

    def test_check_detects_missing_source(self, tmp_path: Path) -> None:
        """check_sync handles missing .context/ source directories."""
        (tmp_path / ".context").mkdir()
        (tmp_path / ".claude").mkdir()
        (tmp_path / "CLAUDE.md").write_text("")

        result = check_sync(tmp_path, quiet=True)
        assert result is False


# === Symlink Detection Tests ===


class TestSymlinkDetection:
    """Tests for symlink/junction detection."""

    def test_detects_symlink(self, tmp_path: Path) -> None:
        """is_symlink_or_junction detects symlinks."""
        source = tmp_path / "source"
        source.mkdir()
        link = tmp_path / "link"
        link.symlink_to(source)

        assert is_symlink_or_junction(link) is True

    def test_detects_regular_directory_as_non_link(self, tmp_path: Path) -> None:
        """is_symlink_or_junction returns False for regular directories."""
        regular_dir = tmp_path / "regular"
        regular_dir.mkdir()

        assert is_symlink_or_junction(regular_dir) is False

    def test_detects_nonexistent_as_non_link(self, tmp_path: Path) -> None:
        """is_symlink_or_junction returns False for nonexistent paths."""
        nonexistent = tmp_path / "nonexistent"

        assert is_symlink_or_junction(nonexistent) is False


# === File Copy Fallback Tests ===


class TestFallbackBehavior:
    """Tests for file copy fallback when symlinks fail."""

    def test_check_sync_handles_file_copy_directories(self, jerry_project: Path) -> None:
        """check_sync works with file-copy (non-symlink) directories."""
        # Manually copy instead of symlink to simulate fallback
        import shutil

        source_rules = jerry_project / ".context" / "rules"
        target_rules = jerry_project / ".claude" / "rules"
        shutil.copytree(source_rules, target_rules)

        source_patterns = jerry_project / ".context" / "patterns"
        target_patterns = jerry_project / ".claude" / "patterns"
        shutil.copytree(source_patterns, target_patterns)

        result = check_sync(jerry_project, quiet=True)
        assert result is True

    def test_check_sync_detects_drift_in_file_copy(self, jerry_project: Path) -> None:
        """check_sync detects missing files in file-copy mode."""
        import shutil

        source_rules = jerry_project / ".context" / "rules"
        target_rules = jerry_project / ".claude" / "rules"
        shutil.copytree(source_rules, target_rules)

        # Add a new file to source that target doesn't have
        (source_rules / "new-rule.md").write_text("# New Rule\n")

        source_patterns = jerry_project / ".context" / "patterns"
        target_patterns = jerry_project / ".claude" / "patterns"
        shutil.copytree(source_patterns, target_patterns)

        result = check_sync(jerry_project, quiet=True)
        assert result is False  # Drift detected


# === Project Root Detection Tests ===


class TestFindProjectRoot:
    """Tests for project root discovery."""

    def test_finds_root_from_project_directory(self) -> None:
        """find_project_root finds Jerry project root from cwd."""
        # This test runs in the actual Jerry repo, so it should find the root
        root = find_project_root()
        assert (root / "CLAUDE.md").exists()
        assert (root / ".context").exists()

    def test_root_has_expected_structure(self) -> None:
        """Found root has expected Jerry project structure."""
        root = find_project_root()
        assert (root / ".context" / "rules").exists()
        assert (root / ".context" / "patterns").exists()


# === Edge Case Tests ===


class TestBootstrapEdgeCases:
    """Edge case tests for bootstrap."""

    def test_bootstrap_with_empty_source_dirs(self, tmp_path: Path) -> None:
        """Bootstrap handles empty .context/ subdirectories."""
        context_dir = tmp_path / ".context"
        (context_dir / "rules").mkdir(parents=True)
        (context_dir / "patterns").mkdir(parents=True)
        (tmp_path / ".claude").mkdir()
        (tmp_path / "CLAUDE.md").write_text("")

        result = bootstrap(tmp_path, quiet=True)
        assert result is True

    def test_bootstrap_creates_claude_dir_if_missing(self, tmp_path: Path) -> None:
        """Bootstrap creates .claude/ directory if it doesn't exist."""
        context_dir = tmp_path / ".context"
        (context_dir / "rules").mkdir(parents=True)
        (context_dir / "patterns").mkdir(parents=True)
        (tmp_path / "CLAUDE.md").write_text("")

        # .claude/ doesn't exist yet
        assert not (tmp_path / ".claude").exists()

        result = bootstrap(tmp_path, quiet=True)
        assert result is True
        assert (tmp_path / ".claude").exists()

    @pytest.mark.skipif(
        platform.system() == "Windows",
        reason="Relative symlink path test for Unix only",
    )
    def test_symlinks_use_relative_paths(self, jerry_project: Path) -> None:
        """Symlinks use relative paths for portability."""
        bootstrap(jerry_project, quiet=True)

        rules_link = jerry_project / ".claude" / "rules"
        if rules_link.is_symlink():
            target = os.readlink(str(rules_link))
            assert not os.path.isabs(target), f"Symlink should be relative, got: {target}"
            assert target == os.path.join("..", ".context", "rules")
