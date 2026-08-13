# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Unit tests for ``CLIAdapter._create_config_adapter`` (BUG-010 Option C, DD-4).

Covers:
    - The ``ast.trusted_roots`` default key (``[]``) is registered in the
      defaults dict, making it discoverable via ``jerry config show`` /
      ``jerry config get ast.trusted_roots``.
    - DD-4 (non-blocking refactor): ``_create_config_adapter`` is built
      via the shared ``project_root.build_layered_config_adapter()``
      factory rather than duplicating ``LayeredConfigAdapter``
      construction, so ``jerry ast`` and ``jerry config`` never drift on
      precedence/path resolution.
"""

from __future__ import annotations

from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from src.interface.cli.adapter import CLIAdapter


class TestCreateConfigAdapterAstTrustedRoots:
    """ast.trusted_roots default registration (mandate requirement)."""

    def test_create_config_adapter_when_called_then_ast_trusted_roots_defaults_to_empty_list(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        """The defaults dict includes ast.trusted_roots: [] so it is
        discoverable via jerry config show/get."""
        # Arrange
        monkeypatch.setenv("CLAUDE_PROJECT_DIR", str(tmp_path))
        monkeypatch.delenv("JERRY_PROJECT", raising=False)
        monkeypatch.delenv("JERRY_AST__TRUSTED_ROOTS", raising=False)
        adapter = CLIAdapter(dispatcher=Mock(), projects_dir=str(tmp_path))

        # Act
        config = adapter._create_config_adapter()

        # Assert
        assert config.get("ast.trusted_roots") == []
        assert config.get_source("ast.trusted_roots") == "default"


class TestCreateConfigAdapterSharedFactory:
    """DD-4: _create_config_adapter delegates to the shared factory."""

    def test_create_config_adapter_when_called_then_delegates_to_build_layered_config_adapter(
        self, tmp_path: Path
    ) -> None:
        """_create_config_adapter calls the shared
        project_root.build_layered_config_adapter() factory rather than
        constructing LayeredConfigAdapter independently -- closing the
        duplication gap between adapter.py and project_root.py."""
        # Arrange
        adapter = CLIAdapter(dispatcher=Mock(), projects_dir=str(tmp_path))

        # Act / Assert
        with patch("src.interface.cli.project_root.build_layered_config_adapter") as mock_factory:
            mock_factory.return_value = Mock()
            adapter._create_config_adapter()

        mock_factory.assert_called_once()
        # The defaults dict passed to the factory must include the new key.
        called_defaults = mock_factory.call_args.args[0]
        assert "ast.trusted_roots" in called_defaults
        assert called_defaults["ast.trusted_roots"] == []
