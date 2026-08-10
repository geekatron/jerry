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
        (jerry_dir / "config.toml").write_text(
            f'[ast]\ntrusted_roots = ["{trusted_dir}"]\n', encoding="utf-8"
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
        monkeypatch.setenv("JERRY_AST__TRUSTED_ROOTS", f'["{trusted_dir}"]')

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

    def test_get_containment_roots_when_no_explicit_root_then_no_warning_regardless_of_project_root(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """The default (non-exclusive) allowed set never triggers the R-3 warning
        for the PROJECT root specifically, even when the project root itself
        happens to be broad -- R-3/DD-1 fires for 'explicit' and 'configured'
        classifications only, never for 'project'."""
        # Arrange
        monkeypatch.setenv("CLAUDE_PROJECT_DIR", str(Path("/")))
        monkeypatch.setattr(project_root_module, "_load_trusted_roots", lambda: [])

        # Act
        get_containment_roots()

        # Assert
        captured = capsys.readouterr()
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
