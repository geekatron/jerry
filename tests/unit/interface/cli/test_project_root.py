# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Unit tests for the shared CLI project-root resolution helper (BUG-010, GH #337).

The helper anchors path-containment and configuration lookups to the USER'S
project root (``CLAUDE_PROJECT_DIR`` env var, else the current working
directory) — never to the Jerry installation's own directory tree.

Also covers the BUG-010 scope-widening follow-up (PR #341 owner review,
2026-08-07): ``get_containment_roots()`` widens the default allowed set to
include OS temp/scratchpad directories, and supports an exclusive
``--root`` override. Two owner-resolved stderr transparency behaviors are
covered here at the ``get_containment_roots`` level:
    - R-3: a one-line stderr WARNING when an explicit ``--root`` resolves
      to an unusually broad location (filesystem/drive root or home dir).
    - R-4: covered at the ``_check_path_containment`` level in
      ``test_ast_commands.py`` (requires knowledge of which specific root
      in the allowed set actually matched a given file).
"""

from __future__ import annotations

import tempfile
from pathlib import Path, PureWindowsPath

import pytest

import src.interface.cli.project_root as project_root_module
from src.interface.cli.project_root import (
    _is_broad_containment_root,
    get_containment_roots,
    get_project_root,
)


class TestGetProjectRoot:
    """Resolution order: CLAUDE_PROJECT_DIR env var, then cwd."""

    def test_get_project_root_when_claude_project_dir_set_then_returns_it(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        """CLAUDE_PROJECT_DIR takes precedence over the working directory."""
        # Arrange
        project_dir = tmp_path / "user-project"
        project_dir.mkdir()
        monkeypatch.setenv("CLAUDE_PROJECT_DIR", str(project_dir))

        # Act
        root = get_project_root()

        # Assert
        assert root == project_dir

    def test_get_project_root_when_env_absent_then_returns_cwd(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        """Without the env var, the current working directory is the root."""
        # Arrange
        monkeypatch.delenv("CLAUDE_PROJECT_DIR", raising=False)
        monkeypatch.chdir(tmp_path)

        # Act
        root = get_project_root()

        # Assert
        assert root == tmp_path

    def test_get_project_root_when_env_empty_string_then_returns_cwd(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        """An empty CLAUDE_PROJECT_DIR is treated as unset, not as a valid root."""
        # Arrange
        monkeypatch.setenv("CLAUDE_PROJECT_DIR", "")
        monkeypatch.chdir(tmp_path)

        # Act
        root = get_project_root()

        # Assert
        assert root == tmp_path

    def test_get_project_root_never_resolves_to_install_tree(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        """The resolver must not anchor to the Jerry source tree (the BUG-010 defect)."""
        # Arrange: simulate running from a user project unrelated to the install tree
        monkeypatch.delenv("CLAUDE_PROJECT_DIR", raising=False)
        monkeypatch.chdir(tmp_path)
        install_tree = Path(__file__).resolve().parents[4]

        # Act
        root = get_project_root()

        # Assert
        assert root != install_tree


# =============================================================================
# BUG-010 scope widening (PR #341 owner review, 2026-08-07): default
# containment roots extend to temp/scratchpad dirs; --root is an exclusive
# override. See eng-lead-implementation-plan.md T-1.
# =============================================================================


class TestGetContainmentRoots:
    """Default allowed set (project root + temp dirs) vs. exclusive --root."""

    def test_get_containment_roots_when_no_explicit_root_then_includes_resolved_project_root(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        """Default set always contains the resolved project root."""
        # Arrange
        project_dir = tmp_path / "user-project"
        project_dir.mkdir()
        monkeypatch.setenv("CLAUDE_PROJECT_DIR", str(project_dir))

        # Act
        roots = get_containment_roots()

        # Assert
        assert project_dir.resolve() in roots

    def test_get_containment_roots_when_no_explicit_root_then_includes_resolved_gettempdir(
        self,
    ) -> None:
        """Default set always contains the resolved system temp directory."""
        # Act
        roots = get_containment_roots()

        # Assert
        assert Path(tempfile.gettempdir()).resolve() in roots

    def test_get_containment_roots_when_hardcoded_tmp_exists_then_includes_it(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        """A monkeypatched, existing _HARDCODED_TMP is included in the default set."""
        # Arrange
        existing = tmp_path / "hardcoded-tmp"
        existing.mkdir()
        monkeypatch.setattr(project_root_module, "_HARDCODED_TMP", existing)

        # Act
        roots = get_containment_roots()

        # Assert
        assert existing.resolve() in roots

    def test_get_containment_roots_when_hardcoded_tmp_absent_then_excludes_it(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        """A monkeypatched, nonexistent _HARDCODED_TMP is excluded; set has exactly 2 entries."""
        # Arrange
        nonexistent = tmp_path / "does-not-exist"
        monkeypatch.setattr(project_root_module, "_HARDCODED_TMP", nonexistent)

        # Act
        roots = get_containment_roots()

        # Assert
        assert nonexistent.resolve() not in roots
        assert len(roots) == 2

    def test_get_containment_roots_when_gettempdir_equals_hardcoded_tmp_then_deduplicated(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        """When gettempdir() and _HARDCODED_TMP resolve to the same dir, no duplicate entries."""
        # Arrange
        shared_tmp = tmp_path / "shared-tmp"
        shared_tmp.mkdir()
        monkeypatch.setattr(project_root_module, "_HARDCODED_TMP", shared_tmp)
        monkeypatch.setattr(tempfile, "gettempdir", lambda: str(shared_tmp))

        # Act
        roots = get_containment_roots()

        # Assert
        assert len(roots) == len(set(roots))
        assert roots.count(shared_tmp.resolve()) == 1

    def test_get_containment_roots_when_explicit_root_given_then_returns_exactly_that_root(
        self, tmp_path: Path
    ) -> None:
        """An explicit_root produces a single-entry, exclusive allowed set."""
        # Arrange
        explicit_dir = tmp_path / "some-dir"
        explicit_dir.mkdir()

        # Act
        roots = get_containment_roots(str(explicit_dir))

        # Assert
        assert roots == [explicit_dir.resolve()]

    def test_get_containment_roots_when_explicit_root_given_then_excludes_project_root_and_tempdir(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        """explicit_root is exclusive -- project root and tempdir are NOT additive."""
        # Arrange
        project_dir = tmp_path / "user-project"
        project_dir.mkdir()
        monkeypatch.setenv("CLAUDE_PROJECT_DIR", str(project_dir))
        explicit_dir = tmp_path / "unrelated-dir"
        explicit_dir.mkdir()

        # Act
        roots = get_containment_roots(str(explicit_dir))

        # Assert
        assert project_dir.resolve() not in roots
        assert Path(tempfile.gettempdir()).resolve() not in roots

    def test_get_containment_roots_when_explicit_root_is_relative_then_resolved_against_cwd(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        """A relative explicit_root resolves the same way Path.resolve() would."""
        # Arrange
        monkeypatch.chdir(tmp_path)
        (tmp_path / "relative" / "dir").mkdir(parents=True)

        # Act
        roots = get_containment_roots("relative/dir")

        # Assert
        assert roots == [Path("relative/dir").resolve()]


# =============================================================================
# R-3 (owner-resolved): warn on stderr when an explicit --root resolves to
# an unusually broad location (filesystem/drive root or home directory).
# Cross-platform detection via Path.parts/Path.anchor (not hard-coded "/").
# =============================================================================


class TestBroadRootWarning:
    """R-3: stderr WARNING when --root is a filesystem/drive root or $HOME."""

    def test_is_broad_containment_root_when_posix_filesystem_root_then_true(self) -> None:
        """The POSIX filesystem root '/' is broad."""
        assert _is_broad_containment_root(Path("/")) is True

    def test_is_broad_containment_root_when_windows_drive_root_then_true(self) -> None:
        """A Windows-style drive root (e.g. C:\\) is broad -- portable detection
        via Path.parts/Path.anchor, verified directly against a PureWindowsPath
        so this assertion holds regardless of the host OS running the test."""
        assert _is_broad_containment_root(PureWindowsPath("C:\\")) is True

    def test_is_broad_containment_root_when_home_directory_then_true(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        """The user's home directory is broad."""
        # Arrange
        fake_home = tmp_path / "home-dir"
        fake_home.mkdir()
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: fake_home))

        # Act / Assert
        assert _is_broad_containment_root(fake_home.resolve()) is True

    def test_is_broad_containment_root_when_ordinary_subdirectory_then_false(
        self, tmp_path: Path
    ) -> None:
        """An ordinary project subdirectory is not broad."""
        ordinary = tmp_path / "some" / "project" / "dir"
        ordinary.mkdir(parents=True)
        assert _is_broad_containment_root(ordinary.resolve()) is False

    def test_get_containment_roots_when_explicit_root_is_broad_then_warns_on_stderr(
        self, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """--root '/' (portable: resolves to the drive root on Windows too)
        triggers a one-line stderr warning; stdout remains untouched."""
        # Act
        get_containment_roots("/")

        # Assert
        captured = capsys.readouterr()
        assert captured.out == ""
        assert "Warning" in captured.err
        assert captured.err.count("\n") == 1

    def test_get_containment_roots_when_explicit_root_is_home_then_warns_on_stderr(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """--root pointed at $HOME triggers the same stderr warning."""
        # Arrange
        fake_home = tmp_path / "home-dir"
        fake_home.mkdir()
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: fake_home))

        # Act
        get_containment_roots(str(fake_home))

        # Assert
        captured = capsys.readouterr()
        assert "Warning" in captured.err

    def test_get_containment_roots_when_explicit_root_is_ordinary_dir_then_no_warning(
        self, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """An ordinary --root directory does not trigger the broad-root warning."""
        # Arrange
        ordinary = tmp_path / "project" / "subdir"
        ordinary.mkdir(parents=True)

        # Act
        get_containment_roots(str(ordinary))

        # Assert
        captured = capsys.readouterr()
        assert captured.err == ""

    def test_get_containment_roots_when_no_explicit_root_then_no_warning_regardless_of_project_root(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """The default (non-exclusive) allowed set never triggers the R-3 warning,
        even when the project root itself happens to be broad -- R-3 is scoped
        to the explicit --root escape hatch only."""
        # Arrange
        monkeypatch.setenv("CLAUDE_PROJECT_DIR", str(Path("/")))

        # Act
        get_containment_roots()

        # Assert
        captured = capsys.readouterr()
        assert captured.err == ""

    # -------------------------------------------------------------------
    # H-02 (RED-BUG010 red-team remediation, CWE-1284-adjacent incomplete
    # allowlist): _is_broad_containment_root previously only flagged the
    # exact filesystem/drive root and the exact $HOME directory, missing
    # ancestors of $HOME (e.g. /home, /Users, C:\\Users, $HOME's parent)
    # that are functionally just as broad -- every user's home directory
    # lives underneath them. The remediation widens the check to flag any
    # ANCESTOR OF (or equal to) $HOME, detected portably via
    # PurePath.relative_to() so it works for PureWindowsPath too (folds
    # in the H-08 Windows coverage-gap caveat with the same fix).
    # -------------------------------------------------------------------

    @pytest.mark.parametrize(
        "home_relative,broad_relative",
        [
            (("home", "testuser"), ("home",)),
            (("Users", "testuser"), ("Users",)),
            (("Users", "testuser"), ()),
        ],
        ids=[
            "linux-home-multiuser-parent",
            "macos-users-multiuser-parent",
            "home-parent-generic",
        ],
    )
    def test_is_broad_containment_root_when_ancestor_of_home_then_true(
        self,
        monkeypatch: pytest.MonkeyPatch,
        tmp_path: Path,
        home_relative: tuple[str, ...],
        broad_relative: tuple[str, ...],
    ) -> None:
        """An ancestor of $HOME (e.g. /home, /Users, $HOME's parent) is
        broad, even though it is neither the exact filesystem root nor
        the exact $HOME directory -- every user's home directory lives
        underneath it, effectively disabling containment host-wide."""
        # Arrange
        fake_home = tmp_path.joinpath(*home_relative)
        fake_home.mkdir(parents=True)
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: fake_home))
        broad_root = tmp_path.joinpath(*broad_relative)

        # Act / Assert
        assert _is_broad_containment_root(broad_root.resolve()) is True

    def test_is_broad_containment_root_when_windows_users_ancestor_of_home_then_true(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """C:\\Users is an ancestor of a Windows-style $HOME -- the same
        ancestor-of-home class as /home and /Users (H-08 coverage gap,
        folded into the H-02 remediation). Verified portably via a
        stubbed Path.home() returning a PureWindowsPath so this holds
        independent of the host OS actually running the test (no live
        Windows host in RoE, per red-vuln's code-reasoning-only verdict)."""

        class _FakeWindowsHome:
            """Stand-in for Path.home() that resolves to a PureWindowsPath."""

            def resolve(self) -> PureWindowsPath:
                return PureWindowsPath("C:\\Users\\eng")

        monkeypatch.setattr(Path, "home", classmethod(lambda cls: _FakeWindowsHome()))

        assert _is_broad_containment_root(PureWindowsPath("C:\\Users")) is True

    def test_is_broad_containment_root_when_descendant_of_home_then_false(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        """A subdirectory beneath $HOME (e.g. ~/projects/foo) is NOT
        broad -- only $HOME itself and its ancestors are, per the H-02
        remediation. Prevents over-flagging ordinary project directories
        that merely happen to live under the user's home directory."""
        # Arrange
        fake_home = tmp_path / "home-dir"
        fake_home.mkdir()
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: fake_home))
        descendant = fake_home / "projects" / "foo"
        descendant.mkdir(parents=True)

        # Act / Assert
        assert _is_broad_containment_root(descendant.resolve()) is False

    def test_get_containment_roots_when_explicit_root_is_ancestor_of_home_then_warns_on_stderr(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """--root pointed at an ancestor of $HOME (e.g. /Users, /home)
        triggers the same R-3 stderr warning as the exact-filesystem-root
        and exact-$HOME cases, propagated end-to-end through
        get_containment_roots (H-02 remediation, RED-BUG010)."""
        # Arrange
        fake_home = tmp_path / "Users" / "testuser"
        fake_home.mkdir(parents=True)
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: fake_home))
        broad_root = tmp_path / "Users"

        # Act
        get_containment_roots(str(broad_root))

        # Assert
        captured = capsys.readouterr()
        assert "Warning" in captured.err
