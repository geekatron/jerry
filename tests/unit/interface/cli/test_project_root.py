# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Unit tests for the shared CLI project-root and containment I/O boundary
(BUG-010 Option C, GH #337).

``get_project_root()`` anchors path-containment and configuration lookups
to the USER'S project root (``CLAUDE_PROJECT_DIR`` env var, else the
current working directory) -- never to the Jerry installation's own
directory tree.

``get_containment_roots()`` is the I/O boundary around the pure
``containment_policy.resolve_allowed_roots()`` decision core (BUG-010
Option C): containment defaults to the project root plus zero-or-more
**user-declared** ``ast.trusted_roots`` entries read through the shared
``LayeredConfigAdapter`` (via ``build_layered_config_adapter()``). No
directory is trusted unless the project owns it or the user explicitly
configured it -- OS temp/scratchpad directories are never auto-trusted.

Two owner-resolved stderr transparency behaviors are covered here at the
``get_containment_roots`` level:
    - R-3: a one-line stderr WARNING when an explicit ``--root`` (or,
      DD-1, a ``configured`` root) resolves to an unusually broad location
      (filesystem/drive root or home dir).
    - R-4: covered at the ``_check_path_containment`` level in
      ``test_ast_commands.py`` (requires knowledge of which specific root
      in the allowed set actually matched a given file).

Pure predicate coverage for ``_is_broad_containment_root`` lives in
``test_containment_policy.py`` (relocated, BUG-010 Option C Section 5).
"""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

import pytest

import src.interface.cli.project_root as project_root_module
from src.interface.cli.project_root import (
    _load_trusted_roots,
    build_layered_config_adapter,
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
# BUG-010 Option C: default containment roots are the project root plus
# zero-or-more user-declared ast.trusted_roots entries; --root is an
# exclusive override. See eng-lead-option-c-plan.md Section 1.2.
# =============================================================================


class TestGetContainmentRoots:
    """Default allowed set (project root + configured trusted roots) vs. --root."""

    def _no_configured_roots(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Force _load_trusted_roots() to return an empty list for this test."""
        monkeypatch.setattr(project_root_module, "_load_trusted_roots", lambda: [])

    def test_get_containment_roots_when_no_explicit_root_and_no_config_then_returns_only_project_root(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        """With no --root and no configured trusted roots, the allowed set
        contains exactly the project root."""
        # Arrange
        project_dir = tmp_path / "user-project"
        project_dir.mkdir()
        monkeypatch.setenv("CLAUDE_PROJECT_DIR", str(project_dir))
        self._no_configured_roots(monkeypatch)

        # Act
        roots = get_containment_roots()

        # Assert
        assert len(roots) == 1
        assert roots[0].path == project_dir.resolve()
        assert roots[0].classification == "project"

    def test_get_containment_roots_when_no_explicit_root_then_never_includes_tempfile_gettempdir(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        """Negative regression: the default set NEVER auto-trusts
        tempfile.gettempdir() -- the always-widen behavior is removed."""
        # Arrange
        project_dir = tmp_path / "user-project"
        project_dir.mkdir()
        monkeypatch.setenv("CLAUDE_PROJECT_DIR", str(project_dir))
        self._no_configured_roots(monkeypatch)

        # Act
        roots = get_containment_roots()

        # Assert
        assert Path(tempfile.gettempdir()).resolve() not in [r.path for r in roots]

    @pytest.mark.skipif(not Path("/tmp").exists(), reason="/tmp does not exist on this system")
    def test_get_containment_roots_when_no_explicit_root_then_never_includes_slash_tmp(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        """Negative regression: the default set NEVER auto-trusts /tmp."""
        # Arrange
        project_dir = tmp_path / "user-project"
        project_dir.mkdir()
        monkeypatch.setenv("CLAUDE_PROJECT_DIR", str(project_dir))
        self._no_configured_roots(monkeypatch)

        # Act
        roots = get_containment_roots()

        # Assert
        assert Path("/tmp").resolve() not in [r.path for r in roots]

    def test_get_containment_roots_when_trusted_roots_configured_in_toml_then_included_after_project_root(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        """A trusted root declared in .jerry/config.toml is included after
        the project root, classified 'configured'."""
        # Arrange
        project_dir = tmp_path / "user-project"
        project_dir.mkdir()
        trusted_dir = tmp_path / "scratchpad"
        trusted_dir.mkdir()
        jerry_dir = project_dir / ".jerry"
        jerry_dir.mkdir()
        # Forward-slash form (Path.as_posix()) keeps this a valid TOML basic
        # string on Windows too -- a raw "C:\Users\..." path would embed
        # invalid TOML escapes (e.g. "\U", "\s") and fail to parse.
        (jerry_dir / "config.toml").write_text(
            f'[ast]\ntrusted_roots = ["{trusted_dir.as_posix()}"]\n', encoding="utf-8"
        )
        monkeypatch.setenv("CLAUDE_PROJECT_DIR", str(project_dir))
        monkeypatch.delenv("JERRY_AST__TRUSTED_ROOTS", raising=False)

        # Act
        roots = get_containment_roots()

        # Assert
        assert [r.path for r in roots] == [project_dir.resolve(), trusted_dir.resolve()]
        assert roots[1].classification == "configured"

    def test_get_containment_roots_when_trusted_roots_configured_via_env_then_included(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        """A trusted root declared via JERRY_AST__TRUSTED_ROOTS is included."""
        # Arrange
        project_dir = tmp_path / "user-project"
        project_dir.mkdir()
        trusted_dir = tmp_path / "scratchpad"
        trusted_dir.mkdir()
        monkeypatch.setenv("CLAUDE_PROJECT_DIR", str(project_dir))
        # json.dumps escapes backslashes correctly, so a raw Windows path
        # (e.g. "C:\Users\...") round-trips through JSON parsing intact --
        # an f-string interpolation would embed invalid JSON escapes.
        monkeypatch.setenv("JERRY_AST__TRUSTED_ROOTS", json.dumps([str(trusted_dir)]))

        # Act
        roots = get_containment_roots()

        # Assert
        assert trusted_dir.resolve() in [r.path for r in roots]
        matched = next(r for r in roots if r.path == trusted_dir.resolve())
        assert matched.classification == "configured"

    def test_get_containment_roots_when_explicit_root_given_then_configured_trusted_roots_ignored(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        """--root is exclusive: configured trusted roots are ignored when
        an explicit root is supplied."""
        # Arrange
        project_dir = tmp_path / "user-project"
        project_dir.mkdir()
        monkeypatch.setenv("CLAUDE_PROJECT_DIR", str(project_dir))
        monkeypatch.setenv("JERRY_AST__TRUSTED_ROOTS", str(tmp_path / "scratchpad"))
        explicit_dir = tmp_path / "explicit"
        explicit_dir.mkdir()

        # Act
        roots = get_containment_roots(str(explicit_dir))

        # Assert
        assert len(roots) == 1
        assert roots[0].path == explicit_dir.resolve()
        assert roots[0].classification == "explicit"

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

    def test_get_containment_roots_when_configured_root_is_broad_then_warns_on_stderr(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """DD-1 symmetry: a broad configured trusted root triggers the same
        class of stderr warning as a broad --root."""
        # Arrange
        project_dir = tmp_path / "user-project"
        project_dir.mkdir()
        monkeypatch.setenv("CLAUDE_PROJECT_DIR", str(project_dir))
        monkeypatch.setattr(project_root_module, "_load_trusted_roots", lambda: ["/"])

        # Act
        get_containment_roots()

        # Assert
        captured = capsys.readouterr()
        assert captured.out == ""
        assert "Warning" in captured.err

    def test_get_containment_roots_when_quiet_true_then_suppresses_broad_root_warning(
        self, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """C6: quiet=True suppresses the R-3 broad-root warning entirely."""
        # Act
        get_containment_roots("/", quiet=True)

        # Assert
        captured = capsys.readouterr()
        assert captured.out == ""
        assert captured.err == ""

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

    def test_get_containment_roots_when_broad_project_root_then_warns_on_stderr(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """A-2 (BUG-010 C4 tournament, RT-002/FM-005): a broad PROJECT root
        (e.g. CLAUDE_PROJECT_DIR='/') now emits the same class of stderr
        warning as a broad 'explicit' or 'configured' root -- silently
        granting whole-filesystem trust via the project root is no longer
        unwarned. stdout stays untouched."""
        # Arrange
        monkeypatch.setenv("CLAUDE_PROJECT_DIR", str(Path("/")))
        monkeypatch.setattr(project_root_module, "_load_trusted_roots", lambda: [])

        # Act
        get_containment_roots()

        # Assert
        captured = capsys.readouterr()
        assert captured.out == ""
        assert "Warning" in captured.err

    def test_get_containment_roots_when_ordinary_project_root_then_no_warning(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """An ordinary (non-broad) project root never triggers the A-2
        warning -- only unusually broad project roots do."""
        # Arrange
        project_dir = tmp_path / "user-project"
        project_dir.mkdir()
        monkeypatch.setenv("CLAUDE_PROJECT_DIR", str(project_dir))
        monkeypatch.setattr(project_root_module, "_load_trusted_roots", lambda: [])

        # Act
        get_containment_roots()

        # Assert
        captured = capsys.readouterr()
        assert captured.err == ""

    def test_get_containment_roots_when_broad_project_root_and_quiet_then_warning_suppressed(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """C6: quiet=True suppresses the A-2 broad-project-root warning too."""
        # Arrange
        monkeypatch.setenv("CLAUDE_PROJECT_DIR", str(Path("/")))
        monkeypatch.setattr(project_root_module, "_load_trusted_roots", lambda: [])

        # Act
        get_containment_roots(quiet=True)

        # Assert
        captured = capsys.readouterr()
        assert captured.out == ""
        assert captured.err == ""

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
        assert [r.path for r in roots] == [Path("relative/dir").resolve()]

    # -------------------------------------------------------------------
    # RED-BUG010 AC-11 (MEDIUM): a blank/whitespace ast.trusted_roots
    # entry must never silently widen the allowed set to cwd.
    # -------------------------------------------------------------------

    def test_get_containment_roots_when_trusted_roots_env_blank_and_cwd_outside_project_then_cwd_not_trusted(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        """Regression for AC-11 (end-to-end style, mirrors the report's CLI
        PoC): a blank JERRY_AST__TRUSTED_ROOTS combined with a cwd that
        differs from the project root must never cause cwd to enter the
        allowed containment set."""
        # Arrange
        project_dir = tmp_path / "user-project"
        project_dir.mkdir()
        outside_dir = tmp_path / "cwd-outside-project"
        outside_dir.mkdir()
        monkeypatch.setenv("CLAUDE_PROJECT_DIR", str(project_dir))
        monkeypatch.setenv("JERRY_AST__TRUSTED_ROOTS", "")
        monkeypatch.chdir(outside_dir)

        # Act
        roots = get_containment_roots()

        # Assert
        assert len(roots) == 1
        assert roots[0].path == project_dir.resolve()
        assert outside_dir.resolve() not in [r.path for r in roots]

    # -------------------------------------------------------------------
    # RED-BUG010 AC-10 (LOW): relative ast.trusted_roots entries are
    # honored (owner decision: warn-and-honor) but must emit a one-line
    # stderr warning naming the resolved cwd-relative path.
    # -------------------------------------------------------------------

    def test_get_containment_roots_when_trusted_root_relative_then_still_trusted_and_warns(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """A relative entry is still honored, but a stderr warning naming
        the resolved cwd-relative path must fire; stdout stays untouched."""
        # Arrange
        project_dir = tmp_path / "user-project"
        project_dir.mkdir()
        cwd_dir = tmp_path / "invocation-cwd"
        scratch_dir = cwd_dir / "scratch"
        scratch_dir.mkdir(parents=True)
        monkeypatch.setenv("CLAUDE_PROJECT_DIR", str(project_dir))
        monkeypatch.chdir(cwd_dir)
        monkeypatch.setattr(project_root_module, "_load_trusted_roots", lambda: ["scratch"])

        # Act
        roots = get_containment_roots()

        # Assert
        assert scratch_dir.resolve() in [r.path for r in roots]
        captured = capsys.readouterr()
        assert captured.out == ""
        assert "Warning" in captured.err
        assert str(scratch_dir.resolve()) in captured.err

    def test_get_containment_roots_when_trusted_root_relative_and_quiet_then_warning_suppressed(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """C6 symmetry: quiet=True suppresses the relative-trusted-root
        warning too, while the trust decision itself is unaffected."""
        # Arrange
        project_dir = tmp_path / "user-project"
        project_dir.mkdir()
        cwd_dir = tmp_path / "invocation-cwd"
        scratch_dir = cwd_dir / "scratch"
        scratch_dir.mkdir(parents=True)
        monkeypatch.setenv("CLAUDE_PROJECT_DIR", str(project_dir))
        monkeypatch.chdir(cwd_dir)
        monkeypatch.setattr(project_root_module, "_load_trusted_roots", lambda: ["scratch"])

        # Act
        roots = get_containment_roots(quiet=True)

        # Assert
        assert scratch_dir.resolve() in [r.path for r in roots]
        captured = capsys.readouterr()
        assert captured.out == ""
        assert captured.err == ""

    def test_get_containment_roots_when_trusted_root_absolute_then_no_relative_warning(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """An absolute trusted root never triggers the relative-path warning."""
        # Arrange
        project_dir = tmp_path / "user-project"
        project_dir.mkdir()
        trusted_dir = tmp_path / "scratchpad"
        trusted_dir.mkdir()
        monkeypatch.setenv("CLAUDE_PROJECT_DIR", str(project_dir))
        monkeypatch.setattr(project_root_module, "_load_trusted_roots", lambda: [str(trusted_dir)])

        # Act
        get_containment_roots()

        # Assert
        captured = capsys.readouterr()
        assert captured.err == ""


# =============================================================================
# _load_trusted_roots -- I/O adapter reading ast.trusted_roots via the
# shared LayeredConfigAdapter (build_layered_config_adapter()).
# =============================================================================


class TestLoadTrustedRootsConfig:
    """_load_trusted_roots(): config precedence for ast.trusted_roots."""

    def test_load_trusted_roots_when_no_config_present_then_returns_empty_list(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        """With no TOML files and no env var, the default [] is returned."""
        # Arrange
        project_dir = tmp_path / "user-project"
        project_dir.mkdir()
        monkeypatch.setenv("CLAUDE_PROJECT_DIR", str(project_dir))
        monkeypatch.delenv("JERRY_AST__TRUSTED_ROOTS", raising=False)
        monkeypatch.delenv("JERRY_PROJECT", raising=False)

        # Act
        result = _load_trusted_roots()

        # Assert
        assert result == []

    def test_load_trusted_roots_when_root_config_toml_has_ast_trusted_roots_then_returns_list(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        """A root-level .jerry/config.toml [ast] trusted_roots entry is read."""
        # Arrange
        project_dir = tmp_path / "user-project"
        jerry_dir = project_dir / ".jerry"
        jerry_dir.mkdir(parents=True)
        (jerry_dir / "config.toml").write_text(
            '[ast]\ntrusted_roots = ["/some/trusted/dir"]\n', encoding="utf-8"
        )
        monkeypatch.setenv("CLAUDE_PROJECT_DIR", str(project_dir))
        monkeypatch.delenv("JERRY_AST__TRUSTED_ROOTS", raising=False)
        monkeypatch.delenv("JERRY_PROJECT", raising=False)

        # Act
        result = _load_trusted_roots()

        # Assert
        assert result == ["/some/trusted/dir"]

    def test_load_trusted_roots_when_project_config_overrides_root_config_then_project_value_used(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        """A projects/{JERRY_PROJECT}/.jerry/config.toml entry overrides the
        root-level .jerry/config.toml entry (LayeredConfigAdapter precedence)."""
        # Arrange
        project_dir = tmp_path / "user-project"
        root_jerry_dir = project_dir / ".jerry"
        root_jerry_dir.mkdir(parents=True)
        (root_jerry_dir / "config.toml").write_text(
            '[ast]\ntrusted_roots = ["/root/level/dir"]\n', encoding="utf-8"
        )
        proj_jerry_dir = project_dir / "projects" / "PROJ-999" / ".jerry"
        proj_jerry_dir.mkdir(parents=True)
        (proj_jerry_dir / "config.toml").write_text(
            '[ast]\ntrusted_roots = ["/project/level/dir"]\n', encoding="utf-8"
        )
        monkeypatch.setenv("CLAUDE_PROJECT_DIR", str(project_dir))
        monkeypatch.setenv("JERRY_PROJECT", "PROJ-999")
        monkeypatch.delenv("JERRY_AST__TRUSTED_ROOTS", raising=False)

        # Act
        result = _load_trusted_roots()

        # Assert
        assert result == ["/project/level/dir"]

    def test_load_trusted_roots_when_env_var_set_then_env_value_overrides_all_file_config(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        """JERRY_AST__TRUSTED_ROOTS (double underscore) overrides file config."""
        # Arrange
        project_dir = tmp_path / "user-project"
        jerry_dir = project_dir / ".jerry"
        jerry_dir.mkdir(parents=True)
        (jerry_dir / "config.toml").write_text(
            '[ast]\ntrusted_roots = ["/file/level/dir"]\n', encoding="utf-8"
        )
        monkeypatch.setenv("CLAUDE_PROJECT_DIR", str(project_dir))
        monkeypatch.setenv("JERRY_AST__TRUSTED_ROOTS", '["/env/level/dir"]')
        monkeypatch.delenv("JERRY_PROJECT", raising=False)

        # Act
        result = _load_trusted_roots()

        # Assert
        assert result == ["/env/level/dir"]

    # -------------------------------------------------------------------
    # RED-BUG010 AC-11 (MEDIUM): empty/whitespace/CSV-trailing-comma
    # entries must be dropped before they can resolve to cwd.
    # -------------------------------------------------------------------

    def test_load_trusted_roots_when_env_var_is_empty_string_then_returns_empty_list(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        """An empty JERRY_AST__TRUSTED_ROOTS must never surface as a
        degenerate entry that later resolves to cwd."""
        # Arrange
        project_dir = tmp_path / "user-project"
        project_dir.mkdir()
        monkeypatch.setenv("CLAUDE_PROJECT_DIR", str(project_dir))
        monkeypatch.setenv("JERRY_AST__TRUSTED_ROOTS", "")
        monkeypatch.delenv("JERRY_PROJECT", raising=False)

        # Act
        result = _load_trusted_roots()

        # Assert
        assert result == []

    def test_load_trusted_roots_when_env_var_is_whitespace_only_then_returns_empty_list(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        """A whitespace-only entry is dropped, not treated as a declared root."""
        # Arrange
        project_dir = tmp_path / "user-project"
        project_dir.mkdir()
        monkeypatch.setenv("CLAUDE_PROJECT_DIR", str(project_dir))
        monkeypatch.setenv("JERRY_AST__TRUSTED_ROOTS", "   ")
        monkeypatch.delenv("JERRY_PROJECT", raising=False)

        # Act
        result = _load_trusted_roots()

        # Assert
        assert result == []

    def test_load_trusted_roots_when_csv_trailing_comma_then_only_nonempty_entries_returned(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        """A CSV trailing comma ("/a,") is parsed upstream to ["/a", ""];
        the stray empty element must be filtered before it can resolve
        to cwd."""
        # Arrange
        project_dir = tmp_path / "user-project"
        project_dir.mkdir()
        monkeypatch.setenv("CLAUDE_PROJECT_DIR", str(project_dir))
        monkeypatch.setenv("JERRY_AST__TRUSTED_ROOTS", "/a,")
        monkeypatch.delenv("JERRY_PROJECT", raising=False)

        # Act
        result = _load_trusted_roots()

        # Assert
        assert result == ["/a"]

    def test_load_trusted_roots_when_entry_has_leading_and_trailing_whitespace_then_stripped(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        """A-3 (BUG-010 C4 tournament, SR-002): a trusted-root entry with
        leading/trailing whitespace (e.g. "  /abs/path  ") must be
        returned STRIPPED, not raw. The blank-entry filter already tests
        ``str(entry).strip()`` truthiness but previously returned the
        unstripped raw value, so a leading-space entry like " /abs" would
        later fail ``Path(" /abs").is_absolute()`` and be silently
        (mis)treated as a cwd-relative path -- this is a distinct defect
        from the AC-11 blank-entry filter (which drops purely-blank
        entries) and from AC-10 (which warns on genuinely relative
        entries)."""
        # Arrange
        project_dir = tmp_path / "user-project"
        project_dir.mkdir()
        monkeypatch.setenv("CLAUDE_PROJECT_DIR", str(project_dir))
        monkeypatch.setenv("JERRY_AST__TRUSTED_ROOTS", '["  /abs/path  "]')
        monkeypatch.delenv("JERRY_PROJECT", raising=False)

        # Act
        result = _load_trusted_roots()

        # Assert
        assert result == ["/abs/path"]

    def test_get_containment_roots_when_trusted_root_has_whitespace_then_treated_as_absolute_no_warning(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """A-3 end-to-end (real ``_load_trusted_roots``, not mocked): a
        whitespace-padded absolute trusted root declared via
        ``JERRY_AST__TRUSTED_ROOTS`` must resolve to the absolute path
        itself (not a cwd-relative reinterpretation) and must NOT
        trigger the AC-10 relative-path warning, since after stripping
        it is genuinely absolute."""
        # Arrange
        project_dir = tmp_path / "user-project"
        project_dir.mkdir()
        trusted_dir = tmp_path / "scratchpad"
        trusted_dir.mkdir()
        monkeypatch.setenv("CLAUDE_PROJECT_DIR", str(project_dir))
        # json.dumps escapes backslashes correctly (portable on Windows);
        # the surrounding two-space padding is preserved inside the JSON
        # string value to exercise the whitespace-stripping behavior.
        monkeypatch.setenv("JERRY_AST__TRUSTED_ROOTS", json.dumps([f"  {trusted_dir}  "]))
        monkeypatch.delenv("JERRY_PROJECT", raising=False)

        # Act
        roots = get_containment_roots()

        # Assert
        assert trusted_dir.resolve() in [r.path for r in roots]
        captured = capsys.readouterr()
        assert "relative" not in captured.err.lower()


# =============================================================================
# build_layered_config_adapter -- shared factory (DD-4)
# =============================================================================


class TestBuildLayeredConfigAdapter:
    """build_layered_config_adapter(): shared LayeredConfigAdapter factory."""

    def test_build_layered_config_adapter_when_called_then_applies_supplied_defaults(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        """The factory applies caller-supplied defaults through the
        resulting adapter's .get()."""
        # Arrange
        project_dir = tmp_path / "user-project"
        project_dir.mkdir()
        monkeypatch.setenv("CLAUDE_PROJECT_DIR", str(project_dir))
        monkeypatch.delenv("JERRY_PROJECT", raising=False)

        # Act
        adapter = build_layered_config_adapter({"ast.trusted_roots": []})

        # Assert
        assert adapter.get("ast.trusted_roots") == []


# =============================================================================
# RED-BUG010 AC-18 (MEDIUM): a '..'-laden JERRY_PROJECT value must not
# steer the project-config file read outside the projects/ tree.
# =============================================================================


class TestBuildLayeredConfigAdapterProjectTraversal:
    """JERRY_PROJECT traversal must not widen which config.toml is read."""

    def test_load_trusted_roots_when_jerry_project_traverses_outside_projects_tree_then_project_layer_ignored(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        """A '..'-laden JERRY_PROJECT value must not cause an outside
        config.toml to be read as the project-config layer, even when a
        real projects/ directory is present (the realistic case)."""
        # Arrange
        project_dir = tmp_path / "user-project"
        (project_dir / "projects").mkdir(parents=True)
        outside_jerry_dir = tmp_path / "elsewhere" / ".jerry"
        outside_jerry_dir.mkdir(parents=True)
        (outside_jerry_dir / "config.toml").write_text(
            '[ast]\ntrusted_roots = ["/tmp/attacker-planted"]\n', encoding="utf-8"
        )
        monkeypatch.setenv("CLAUDE_PROJECT_DIR", str(project_dir))
        monkeypatch.setenv("JERRY_PROJECT", "../../elsewhere")
        monkeypatch.delenv("JERRY_AST__TRUSTED_ROOTS", raising=False)

        # Act
        result = _load_trusted_roots()

        # Assert
        assert result == []

    def test_load_trusted_roots_when_jerry_project_is_normal_value_then_project_config_still_loads(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        """No regression: a well-formed JERRY_PROJECT value still resolves
        its project-level config.toml correctly."""
        # Arrange
        project_dir = tmp_path / "user-project"
        proj_jerry_dir = project_dir / "projects" / "PROJ-024-tactical-work" / ".jerry"
        proj_jerry_dir.mkdir(parents=True)
        (proj_jerry_dir / "config.toml").write_text(
            '[ast]\ntrusted_roots = ["/project/level/dir"]\n', encoding="utf-8"
        )
        monkeypatch.setenv("CLAUDE_PROJECT_DIR", str(project_dir))
        monkeypatch.setenv("JERRY_PROJECT", "PROJ-024-tactical-work")
        monkeypatch.delenv("JERRY_AST__TRUSTED_ROOTS", raising=False)

        # Act
        result = _load_trusted_roots()

        # Assert
        assert result == ["/project/level/dir"]
