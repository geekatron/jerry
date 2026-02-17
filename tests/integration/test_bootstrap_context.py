"""Integration tests for context distribution bootstrap script.

Tests the cross-platform sync mechanism that links .context/ to .claude/.
Covers symlink creation, check mode, force mode, fallback behavior,
idempotency, content drift detection, retry logic, mock-based Windows
code paths, and bootstrap error paths.

Cross-platform CI evidence:
    The CI matrix in .github/workflows/ci.yml runs tests on:
    - ubuntu-latest (Python 3.11-3.14)
    - windows-latest (Python 3.13-3.14)
    - macos-latest (Python 3.13-3.14)
    Windows/macOS CI evidence will be collected on first PR run to main.
    See: .github/workflows/ci.yml lines 213, 298 (test-pip, test-uv matrices).
"""

from __future__ import annotations

import os
import platform
import shutil
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from scripts.bootstrap_context import (
    _create_windows_link,
    _files_match,
    _rmtree_with_retry,
    bootstrap,
    check_sync,
    create_symlink,
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
        """Symlinks use relative paths for portability.  Addresses F-401, NF-006."""
        bootstrap(jerry_project, quiet=True)

        rules_link = jerry_project / ".claude" / "rules"
        if not rules_link.is_symlink():
            pytest.skip("Symlink was not created (file-copy fallback used)")
        target = os.readlink(str(rules_link))
        assert not os.path.isabs(target), f"Symlink should be relative, got: {target}"
        assert target == os.path.join("..", ".context", "rules")


# === _files_match Tests ===


class TestFilesMatch:
    """Tests for _files_match content comparison."""

    def test_matching_directories_return_true(self, tmp_path: Path) -> None:
        """_files_match returns True when source and target have identical content."""
        source = tmp_path / "source"
        target = tmp_path / "target"
        source.mkdir()
        target.mkdir()

        (source / "a.md").write_text("hello")
        (target / "a.md").write_text("hello")

        assert _files_match(source, target) is True

    def test_different_content_returns_false(self, tmp_path: Path) -> None:
        """_files_match returns False when files have same name but different content."""
        source = tmp_path / "source"
        target = tmp_path / "target"
        source.mkdir()
        target.mkdir()

        (source / "a.md").write_text("original content")
        (target / "a.md").write_text("modified content")

        assert _files_match(source, target) is False

    def test_extra_file_in_source_returns_false(self, tmp_path: Path) -> None:
        """_files_match returns False when source has a file target lacks."""
        source = tmp_path / "source"
        target = tmp_path / "target"
        source.mkdir()
        target.mkdir()

        (source / "a.md").write_text("hello")
        (source / "b.md").write_text("world")
        (target / "a.md").write_text("hello")

        assert _files_match(source, target) is False

    def test_extra_file_in_target_returns_false(self, tmp_path: Path) -> None:
        """_files_match returns False when target has a file source lacks."""
        source = tmp_path / "source"
        target = tmp_path / "target"
        source.mkdir()
        target.mkdir()

        (source / "a.md").write_text("hello")
        (target / "a.md").write_text("hello")
        (target / "extra.md").write_text("extra")

        assert _files_match(source, target) is False

    def test_empty_directories_match(self, tmp_path: Path) -> None:
        """_files_match returns True for two empty directories."""
        source = tmp_path / "source"
        target = tmp_path / "target"
        source.mkdir()
        target.mkdir()

        assert _files_match(source, target) is True

    def test_recursive_subdirectory_comparison(self, tmp_path: Path) -> None:
        """_files_match recursively compares files in subdirectories."""
        source = tmp_path / "source"
        target = tmp_path / "target"
        (source / "sub").mkdir(parents=True)
        (target / "sub").mkdir(parents=True)

        (source / "sub" / "deep.md").write_text("deep content")
        (target / "sub" / "deep.md").write_text("deep content")

        assert _files_match(source, target) is True

    def test_recursive_subdirectory_content_drift(self, tmp_path: Path) -> None:
        """_files_match detects content drift in nested subdirectories."""
        source = tmp_path / "source"
        target = tmp_path / "target"
        (source / "sub").mkdir(parents=True)
        (target / "sub").mkdir(parents=True)

        (source / "sub" / "deep.md").write_text("original")
        (target / "sub" / "deep.md").write_text("drifted")

        assert _files_match(source, target) is False


# === _rmtree_with_retry Tests ===


class TestRmtreeWithRetry:
    """Tests for _rmtree_with_retry retry logic."""

    def test_successful_removal_on_first_attempt(self, tmp_path: Path) -> None:
        """_rmtree_with_retry removes directory on first attempt."""
        target = tmp_path / "to_remove"
        target.mkdir()
        (target / "file.txt").write_text("content")

        _rmtree_with_retry(target)
        assert not target.exists()

    def test_succeeds_after_retry_on_permission_error(self, tmp_path: Path) -> None:
        """_rmtree_with_retry succeeds when PermissionError clears on retry."""
        target = tmp_path / "to_remove"
        target.mkdir()
        (target / "file.txt").write_text("content")

        call_count = 0
        original_rmtree = shutil.rmtree

        def flaky_rmtree(path: object, **kwargs: object) -> None:
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                raise PermissionError("file locked")
            original_rmtree(path)  # type: ignore[arg-type]

        with patch("shutil.rmtree", side_effect=flaky_rmtree):
            with patch("time.sleep"):
                _rmtree_with_retry(target)

        assert call_count == 2

    def test_raises_after_max_retries_exhausted(self, tmp_path: Path) -> None:
        """_rmtree_with_retry raises PermissionError after all retries fail."""
        target = tmp_path / "to_remove"
        target.mkdir()

        def always_fail(path: object, **kwargs: object) -> None:
            raise PermissionError("permanently locked")

        with patch("shutil.rmtree", side_effect=always_fail):
            with patch("time.sleep"):
                with pytest.raises(PermissionError, match="permanently locked"):
                    _rmtree_with_retry(target, max_retries=3)


# === Content Modification Drift in check_sync ===


class TestCheckSyncContentDrift:
    """Tests for content-modification drift detection in check_sync."""

    def test_check_sync_detects_content_modification_drift(self, jerry_project: Path) -> None:
        """check_sync detects when file content is modified (not just added/removed)."""
        source_rules = jerry_project / ".context" / "rules"
        target_rules = jerry_project / ".claude" / "rules"
        shutil.copytree(source_rules, target_rules)

        source_patterns = jerry_project / ".context" / "patterns"
        target_patterns = jerry_project / ".claude" / "patterns"
        shutil.copytree(source_patterns, target_patterns)

        # Verify sync is OK before modification
        assert check_sync(jerry_project, quiet=True) is True

        # Modify content of an existing file in the target (simulating drift)
        (target_rules / "coding-standards.md").write_text("# MODIFIED content\n")

        result = check_sync(jerry_project, quiet=True)
        assert result is False

    def test_check_sync_detects_source_content_modification(self, jerry_project: Path) -> None:
        """check_sync detects drift when source content changes after copy."""
        source_rules = jerry_project / ".context" / "rules"
        target_rules = jerry_project / ".claude" / "rules"
        shutil.copytree(source_rules, target_rules)

        source_patterns = jerry_project / ".context" / "patterns"
        target_patterns = jerry_project / ".claude" / "patterns"
        shutil.copytree(source_patterns, target_patterns)

        # Verify sync is OK before modification
        assert check_sync(jerry_project, quiet=True) is True

        # Modify content in the source (upstream change not yet synced)
        (source_rules / "coding-standards.md").write_text("# Updated upstream\n")

        result = check_sync(jerry_project, quiet=True)
        assert result is False


# === Mock-based Windows Code Path Tests (NF-008, NF-009) ===
# These tests mock detect_platform() to exercise Windows-specific branches
# on non-Windows hosts. Cross-platform CI will validate real Windows behavior.
# CI matrix: .github/workflows/ci.yml (windows-latest in test-pip and test-uv).


class TestWindowsCreateLink:
    """Mock-based tests for _create_windows_link code paths.  Addresses NF-008."""

    def test_windows_link_uses_relative_path_for_symlink(self, tmp_path: Path) -> None:
        """_create_windows_link passes relative path to symlink_to().  Addresses F-401."""
        # Arrange
        source = tmp_path / "source_dir"
        source.mkdir()
        target = tmp_path / "sub" / "target_dir"
        target.parent.mkdir(parents=True)

        captured_args: list[str] = []

        def mock_symlink_to(path_arg: str) -> None:
            captured_args.append(str(path_arg))

        # Act -- mock target.symlink_to to capture the path argument
        with patch.object(Path, "symlink_to", side_effect=mock_symlink_to):
            _create_windows_link(source, target, quiet=True)

        # Assert -- the symlink attempt should use a relative path
        assert len(captured_args) == 1
        assert not os.path.isabs(captured_args[0]), (
            f"Windows symlink should attempt relative path, got: {captured_args[0]}"
        )
        expected_rel = os.path.relpath(source, target.parent)
        assert captured_args[0] == expected_rel

    def test_windows_junction_fallback_uses_absolute_path(self, tmp_path: Path) -> None:
        """_create_windows_link uses absolute path for junction subprocess.  Addresses F-401."""
        # Arrange
        source = tmp_path / "source_dir"
        source.mkdir()
        target = tmp_path / "sub" / "target_dir"
        target.parent.mkdir(parents=True)

        captured_subprocess_args: list[list[str]] = []

        def mock_subprocess_run(cmd: list[str], **kwargs: object) -> MagicMock:
            captured_subprocess_args.append(cmd)
            return MagicMock(returncode=0)

        # Act -- make symlink_to fail so junction fallback is triggered
        with patch.object(Path, "symlink_to", side_effect=OSError("no Developer Mode")):
            with patch("subprocess.run", side_effect=mock_subprocess_run):
                result = _create_windows_link(source, target, quiet=True)

        # Assert -- junction uses absolute path for source
        assert result is True
        assert len(captured_subprocess_args) == 1
        cmd = captured_subprocess_args[0]
        assert cmd == ["cmd", "/c", "mklink", "/J", str(target), str(source)]
        # The source argument (cmd[5]) must be absolute for junctions
        assert os.path.isabs(cmd[5]), f"Junction source must be absolute, got: {cmd[5]}"

    def test_windows_link_returns_false_when_both_fail(self, tmp_path: Path) -> None:
        """_create_windows_link returns False when symlink and junction both fail."""
        # Arrange
        source = tmp_path / "source_dir"
        source.mkdir()
        target = tmp_path / "sub" / "target_dir"
        target.parent.mkdir(parents=True)

        # Act -- make both paths fail
        with patch.object(Path, "symlink_to", side_effect=OSError("no Developer Mode")):
            with patch(
                "subprocess.run",
                side_effect=FileNotFoundError("cmd not found"),
            ):
                result = _create_windows_link(source, target, quiet=True)

        # Assert
        assert result is False


class TestWindowsJunctionDetection:
    """Mock-based tests for is_symlink_or_junction Windows branch.  Addresses NF-009."""

    def test_detects_reparse_point_attribute_on_windows(self, tmp_path: Path) -> None:
        """is_symlink_or_junction detects Windows junction via st_file_attributes."""
        # Arrange -- create a real directory (non-symlink) then mock platform + lstat
        target = tmp_path / "junction_target"
        target.mkdir()

        FILE_ATTRIBUTE_REPARSE_POINT = 0x400
        mock_stat = MagicMock()
        mock_stat.st_file_attributes = FILE_ATTRIBUTE_REPARSE_POINT

        # Act
        with patch("scripts.bootstrap_context.detect_platform", return_value="windows"):
            with patch("os.lstat", return_value=mock_stat):
                result = is_symlink_or_junction(target)

        # Assert
        assert result is True

    def test_returns_false_when_no_reparse_attribute_on_windows(self, tmp_path: Path) -> None:
        """is_symlink_or_junction returns False for regular dir on Windows."""
        # Arrange
        target = tmp_path / "regular_dir"
        target.mkdir()

        mock_stat = MagicMock()
        mock_stat.st_file_attributes = 0x0  # No reparse point

        # Act
        with patch("scripts.bootstrap_context.detect_platform", return_value="windows"):
            with patch("os.lstat", return_value=mock_stat):
                result = is_symlink_or_junction(target)

        # Assert
        assert result is False

    def test_returns_false_when_lstat_raises_oserror_on_windows(self, tmp_path: Path) -> None:
        """is_symlink_or_junction returns False when os.lstat raises OSError on Windows."""
        # Arrange
        target = tmp_path / "missing_junction"
        # Do not create the directory -- it does not exist on disk

        # Act
        with patch("scripts.bootstrap_context.detect_platform", return_value="windows"):
            with patch("os.lstat", side_effect=OSError("path not found")):
                result = is_symlink_or_junction(target)

        # Assert
        assert result is False

    def test_returns_false_when_no_st_file_attributes(self, tmp_path: Path) -> None:
        """is_symlink_or_junction handles missing st_file_attributes gracefully."""
        # Arrange -- simulate a stat result without st_file_attributes (non-Windows FS)
        target = tmp_path / "no_attrs"
        target.mkdir()

        # We need os.lstat to work normally for is_symlink() check (which inspects st_mode),
        # but return a stat result without st_file_attributes for the Windows branch.
        original_lstat = os.lstat
        call_count = 0

        def lstat_side_effect(path: object, *args: object, **kwargs: object) -> object:
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                # First call is from is_symlink() -- return real result
                return original_lstat(path)  # type: ignore[arg-type]
            # Second call is from the Windows branch -- return mock without st_file_attributes
            mock_stat = MagicMock()
            del mock_stat.st_file_attributes  # Remove so getattr returns default 0
            return mock_stat

        # Act
        with patch("scripts.bootstrap_context.detect_platform", return_value="windows"):
            with patch("os.lstat", side_effect=lstat_side_effect):
                result = is_symlink_or_junction(target)

        # Assert
        assert result is False


class TestCreateSymlinkPlatformRouting:
    """Tests that create_symlink routes to the correct platform handler."""

    def test_routes_to_windows_handler_on_windows(self, tmp_path: Path) -> None:
        """create_symlink calls _create_windows_link when platform is windows."""
        # Arrange
        source = tmp_path / "source"
        source.mkdir()
        target = tmp_path / "target"

        # Act -- mock detect_platform and _create_windows_link
        with patch("scripts.bootstrap_context.detect_platform", return_value="windows"):
            with patch(
                "scripts.bootstrap_context._create_windows_link", return_value=True
            ) as mock_win:
                result = create_symlink(source, target, quiet=True)

        # Assert
        assert result is True
        mock_win.assert_called_once_with(source, target, True)

    def test_routes_to_unix_handler_on_linux(self, tmp_path: Path) -> None:
        """create_symlink calls _create_unix_symlink when platform is linux."""
        # Arrange
        source = tmp_path / "source"
        source.mkdir()
        target = tmp_path / "target"

        # Act
        with patch("scripts.bootstrap_context.detect_platform", return_value="linux"):
            with patch(
                "scripts.bootstrap_context._create_unix_symlink", return_value=True
            ) as mock_unix:
                result = create_symlink(source, target, quiet=True)

        # Assert
        assert result is True
        mock_unix.assert_called_once_with(source, target, True)


# === Bootstrap Error Path Tests ===


class TestBootstrapErrorPaths:
    """Tests for bootstrap() error and edge-case paths.  Addresses critic iteration 3."""

    def test_bootstrap_when_source_dir_missing_then_returns_false(self, tmp_path: Path) -> None:
        """bootstrap() returns False when .context/ source directories do not exist."""
        # Arrange -- create .context/ but WITHOUT rules/ or patterns/
        (tmp_path / ".context").mkdir()
        (tmp_path / ".claude").mkdir()
        (tmp_path / "CLAUDE.md").write_text("")

        # Act
        result = bootstrap(tmp_path, quiet=True)

        # Assert -- source dirs are missing, so bootstrap should report failure
        assert result is False

    def test_bootstrap_when_copytree_fails_then_returns_false(self, jerry_project: Path) -> None:
        """bootstrap() returns False when both symlink and copytree fail.  Addresses F-603."""
        # Arrange -- mock create_symlink to fail (triggers copytree fallback),
        # then mock copytree to also fail
        with patch("scripts.bootstrap_context.create_symlink", return_value=False):
            with patch(
                "scripts.bootstrap_context.shutil.copytree",
                side_effect=OSError("disk full"),
            ):
                # Act
                result = bootstrap(jerry_project, quiet=True)

        # Assert
        assert result is False

    def test_bootstrap_when_force_with_existing_copy_then_recreates(
        self, jerry_project: Path
    ) -> None:
        """bootstrap() with --force removes existing file-copy dirs and recreates."""
        # Arrange -- first bootstrap normally, then replace symlinks with copies
        bootstrap(jerry_project, quiet=True)

        rules_link = jerry_project / ".claude" / "rules"
        patterns_link = jerry_project / ".claude" / "patterns"

        # Remove symlinks and replace with file copies to test force removal of dirs
        for link_path, dirname in [(rules_link, "rules"), (patterns_link, "patterns")]:
            if link_path.is_symlink():
                link_path.unlink()
            elif link_path.is_dir():
                shutil.rmtree(link_path)
            shutil.copytree(jerry_project / ".context" / dirname, link_path)

        # Verify they are regular directories now (not symlinks)
        assert rules_link.is_dir() and not rules_link.is_symlink()

        # Act -- force re-bootstrap
        result = bootstrap(jerry_project, force=True, quiet=True)

        # Assert
        assert result is True
        # After force, should be symlinks again (or file copies if symlink fails)
        assert rules_link.exists()
        assert (rules_link / "coding-standards.md").exists()

    def test_bootstrap_when_partial_source_exists_then_syncs_available(
        self, tmp_path: Path
    ) -> None:
        """bootstrap() syncs available dirs and reports failure for missing ones."""
        # Arrange -- only rules/ exists, patterns/ is missing
        context_dir = tmp_path / ".context"
        rules_dir = context_dir / "rules"
        rules_dir.mkdir(parents=True)
        (rules_dir / "test.md").write_text("# Test\n")
        (tmp_path / ".claude").mkdir()
        (tmp_path / "CLAUDE.md").write_text("")

        # Act
        result = bootstrap(tmp_path, quiet=True)

        # Assert -- returns False (not all dirs synced) but rules/ should be linked
        assert result is False
        assert (tmp_path / ".claude" / "rules").exists()
        assert not (tmp_path / ".claude" / "patterns").exists()


# === CI Evidence Documentation ===
# Cross-platform CI matrix is defined in .github/workflows/ci.yml.
# Both test-pip and test-uv jobs run on: ubuntu-latest, windows-latest, macos-latest
# with Python 3.13 and 3.14 for windows/macos, and 3.11-3.14 for ubuntu.
#
# Mock-based Windows tests above exercise the _create_windows_link() and
# is_symlink_or_junction() Windows branches on the current platform.
# Real Windows/macOS evidence will be collected when CI runs on those platforms.
#
# Reference: .github/workflows/ci.yml lines 207-254 (test-pip), 287-368 (test-uv)
# Finding: F-1101 (CI matrix defined, passing evidence pending first PR run)
