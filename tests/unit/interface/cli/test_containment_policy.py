# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Unit tests for the pure ``jerry ast`` containment policy (BUG-010 Option C).

Covers ``ContainmentRoot`` and ``resolve_allowed_roots()`` -- the pure,
zero-I/O decision core of path containment: given a resolved project root,
a sequence of resolved user-configured trusted roots, and an optional
resolved explicit ``--root``, compute the ordered allowed-roots set with
per-root trust classification (``project`` | ``configured`` | ``explicit``)
and broad-root flags.

Also covers ``_is_broad_containment_root()``, relocated here verbatim from
``project_root.py`` (BUG-010 Option C, Section 1.1 of
``eng-lead-option-c-plan.md``) so the pure policy module has a single
source of truth for broad-root detection without a circular import back to
the I/O-boundary module.

Zero env/filesystem/config access anywhere in this module, except the
pre-existing ``Path.home()`` monkeypatch pattern already used by the
relocated ``_is_broad_containment_root`` tests -- unchanged from the
original ``test_project_root.py::TestBroadRootWarning`` suite.
"""

from __future__ import annotations

import dataclasses
from pathlib import Path, PureWindowsPath

import pytest

from src.interface.cli.containment_policy import (
    ContainmentRoot,
    _is_broad_containment_root,
    resolve_allowed_roots,
)

# =============================================================================
# resolve_allowed_roots -- default (no explicit_root) branch
# =============================================================================


class TestResolveAllowedRootsDefault:
    """No explicit_root: project root + de-duplicated configured roots."""

    def test_resolve_allowed_roots_when_no_configured_and_no_explicit_then_returns_only_project_root(
        self, tmp_path: Path
    ) -> None:
        """With zero configured roots and no explicit root, only the project
        root is returned, classified 'project'."""
        # Arrange
        project_root = (tmp_path / "project").resolve()
        project_root.mkdir()

        # Act
        roots = resolve_allowed_roots(project_root, [], None)

        # Assert
        assert len(roots) == 1
        assert roots[0].path == project_root
        assert roots[0].classification == "project"

    def test_resolve_allowed_roots_when_configured_roots_given_then_appended_after_project_root_in_order(
        self, tmp_path: Path
    ) -> None:
        """Configured roots are appended after the project root, preserving
        the caller-supplied order, each classified 'configured'."""
        # Arrange
        project_root = (tmp_path / "project").resolve()
        project_root.mkdir()
        configured_1 = (tmp_path / "configured-1").resolve()
        configured_1.mkdir()
        configured_2 = (tmp_path / "configured-2").resolve()
        configured_2.mkdir()

        # Act
        roots = resolve_allowed_roots(project_root, [configured_1, configured_2], None)

        # Assert
        assert [r.path for r in roots] == [project_root, configured_1, configured_2]
        assert roots[0].classification == "project"
        assert roots[1].classification == "configured"
        assert roots[2].classification == "configured"

    def test_resolve_allowed_roots_when_configured_root_duplicates_project_root_then_deduped_keeping_project_classification(
        self, tmp_path: Path
    ) -> None:
        """A configured root identical to the project root is dropped from
        the configured entries, retaining the single 'project' entry."""
        # Arrange
        project_root = (tmp_path / "project").resolve()
        project_root.mkdir()

        # Act
        roots = resolve_allowed_roots(project_root, [project_root], None)

        # Assert
        assert len(roots) == 1
        assert roots[0].classification == "project"

    def test_resolve_allowed_roots_when_duplicate_configured_roots_given_then_deduped_preserving_first_order(
        self, tmp_path: Path
    ) -> None:
        """Duplicate configured roots are de-duplicated, keeping the first
        occurrence's position."""
        # Arrange
        project_root = (tmp_path / "project").resolve()
        project_root.mkdir()
        dup = (tmp_path / "dup").resolve()
        dup.mkdir()

        # Act
        roots = resolve_allowed_roots(project_root, [dup, dup], None)

        # Assert
        assert len(roots) == 2
        assert roots[1].path == dup
        assert roots[1].classification == "configured"

    def test_resolve_allowed_roots_when_configured_roots_empty_then_returns_project_root_only(
        self, tmp_path: Path
    ) -> None:
        """An explicitly empty configured_roots sequence behaves identically
        to the zero-configured-roots default case."""
        # Arrange
        project_root = (tmp_path / "project").resolve()
        project_root.mkdir()

        # Act
        roots = resolve_allowed_roots(project_root, [], None)

        # Assert
        assert len(roots) == 1
        assert roots[0].path == project_root


# =============================================================================
# resolve_allowed_roots -- explicit_root branch
# =============================================================================


class TestResolveAllowedRootsExplicit:
    """explicit_root given: exactly one entry, project/configured excluded."""

    def test_resolve_allowed_roots_when_explicit_root_given_then_returns_single_explicit_entry(
        self, tmp_path: Path
    ) -> None:
        """A supplied explicit_root produces exactly one entry, classified
        'explicit'."""
        # Arrange
        project_root = (tmp_path / "project").resolve()
        project_root.mkdir()
        explicit_root = (tmp_path / "explicit").resolve()
        explicit_root.mkdir()

        # Act
        roots = resolve_allowed_roots(project_root, [], explicit_root)

        # Assert
        assert len(roots) == 1
        assert roots[0].path == explicit_root
        assert roots[0].classification == "explicit"

    def test_resolve_allowed_roots_when_explicit_root_given_then_project_root_and_configured_roots_excluded(
        self, tmp_path: Path
    ) -> None:
        """When explicit_root is given, project_root and configured_roots
        are ignored entirely -- exclusive override semantics."""
        # Arrange
        project_root = (tmp_path / "project").resolve()
        project_root.mkdir()
        configured = (tmp_path / "configured").resolve()
        configured.mkdir()
        explicit_root = (tmp_path / "explicit").resolve()
        explicit_root.mkdir()

        # Act
        roots = resolve_allowed_roots(project_root, [configured], explicit_root)

        # Assert
        assert len(roots) == 1
        assert roots[0].path == explicit_root
        assert project_root not in [r.path for r in roots]
        assert configured not in [r.path for r in roots]


# =============================================================================
# resolve_allowed_roots -- is_broad flagging
# =============================================================================


class TestResolveAllowedRootsBroadFlagging:
    """Per-root is_broad flag via the relocated _is_broad_containment_root."""

    def test_resolve_allowed_roots_when_project_root_is_broad_then_flagged_is_broad_true(
        self,
    ) -> None:
        """A broad project root (filesystem root) is flagged is_broad=True."""
        # Act
        roots = resolve_allowed_roots(Path("/"), [], None)

        # Assert
        assert roots[0].is_broad is True

    def test_resolve_allowed_roots_when_configured_root_is_broad_then_flagged_is_broad_true(
        self, tmp_path: Path
    ) -> None:
        """A broad configured root is flagged is_broad=True, independent of
        the (ordinary) project root's own flag."""
        # Arrange
        project_root = (tmp_path / "project").resolve()
        project_root.mkdir()

        # Act
        roots = resolve_allowed_roots(project_root, [Path("/")], None)

        # Assert
        assert roots[0].is_broad is False
        assert roots[1].is_broad is True

    def test_resolve_allowed_roots_when_explicit_root_is_broad_then_flagged_is_broad_true(
        self,
    ) -> None:
        """A broad explicit root is flagged is_broad=True."""
        # Act
        roots = resolve_allowed_roots(Path("/some/ordinary/project"), [], Path("/"))

        # Assert
        assert roots[0].is_broad is True

    def test_resolve_allowed_roots_when_all_roots_ordinary_then_is_broad_false_for_every_entry(
        self, tmp_path: Path
    ) -> None:
        """Ordinary project + configured roots are all flagged is_broad=False."""
        # Arrange
        project_root = (tmp_path / "project").resolve()
        project_root.mkdir()
        configured = (tmp_path / "configured").resolve()
        configured.mkdir()

        # Act
        roots = resolve_allowed_roots(project_root, [configured], None)

        # Assert
        assert all(r.is_broad is False for r in roots)


# =============================================================================
# ContainmentRoot value object
# =============================================================================


class TestContainmentRoot:
    """H-10: exactly one public class per file; frozen, hashable value object."""

    def test_containment_root_when_constructed_then_is_frozen_and_hashable(
        self, tmp_path: Path
    ) -> None:
        """ContainmentRoot is a frozen, hashable dataclass -- mutation raises,
        and instances can be used as set/dict-key members."""
        # Arrange
        root = ContainmentRoot(path=tmp_path, classification="project", is_broad=False)

        # Act / Assert
        with pytest.raises(dataclasses.FrozenInstanceError):
            root.path = tmp_path  # type: ignore[misc]
        assert {root} == {root}


# =============================================================================
# _is_broad_containment_root -- relocated verbatim from test_project_root.py
# (TestBroadRootWarning, pure-predicate cases only; import path changed to
# containment_policy per BUG-010 Option C Section 5).
# =============================================================================


class TestIsBroadContainmentRoot:
    """R-3/DD-1 predicate: filesystem/drive root, $HOME, or ancestor of $HOME."""

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
        ancestor-of-home class as /home and /Users. Verified portably via a
        stubbed Path.home() returning a PureWindowsPath so this holds
        independent of the host OS actually running the test."""

        class _FakeWindowsHome:
            """Stand-in for Path.home() that resolves to a PureWindowsPath."""

            def resolve(self) -> PureWindowsPath:
                return PureWindowsPath("C:\\Users\\eng")

        monkeypatch.setattr(Path, "home", classmethod(lambda cls: _FakeWindowsHome()))

        assert _is_broad_containment_root(PureWindowsPath("C:\\Users")) is True

    def test_is_broad_containment_root_when_home_undeterminable_then_false(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        """When Path.home() raises (RuntimeError or OSError -- home
        directory cannot be determined on this system/environment), an
        ordinary resolvable path is NOT broad via the home-directory
        criterion (fails safe/closed toward "not broad", not toward
        false-positive broadness)."""

        def _raise_runtime_error(cls: type[Path]) -> Path:
            raise RuntimeError("home directory cannot be determined")

        monkeypatch.setattr(Path, "home", classmethod(_raise_runtime_error))
        ordinary = tmp_path / "some" / "project" / "dir"
        ordinary.mkdir(parents=True)

        assert _is_broad_containment_root(ordinary.resolve()) is False

    def test_is_broad_containment_root_when_descendant_of_home_then_false(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        """A subdirectory beneath $HOME (e.g. ~/projects/foo) is NOT
        broad -- only $HOME itself and its ancestors are. Prevents
        over-flagging ordinary project directories that merely happen to
        live under the user's home directory."""
        # Arrange
        fake_home = tmp_path / "home-dir"
        fake_home.mkdir()
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: fake_home))
        descendant = fake_home / "projects" / "foo"
        descendant.mkdir(parents=True)

        # Act / Assert
        assert _is_broad_containment_root(descendant.resolve()) is False
