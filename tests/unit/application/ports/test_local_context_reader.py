"""
Unit tests for ILocalContextReader port.

Tests the LocalContextReader port contract and adapter implementation.
These tests are part of EN-001 Phase 1 (RED) - they should FAIL until
the port and adapter are implemented.

Test Distribution:
- Happy Path (60%): 3 tests - Read valid TOML, get active project, nested structure
- Negative (30%): 2 tests - Missing file, invalid TOML
- Edge (10%): 1 test - Empty file

References:
    - EN-001: Session Start Hook TDD Cleanup
    - DEC-001: Local Context Test Strategy
    - TD-003: Missing local context support in main CLI
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from src.application.ports.secondary.ilocal_context_reader import ILocalContextReader


# === Port Contract Tests ===


class TestLocalContextReaderPortContract:
    """Tests for ILocalContextReader port contract."""

    def test_port_interface_exists(self) -> None:
        """ILocalContextReader port interface can be imported."""
        from src.application.ports.secondary.ilocal_context_reader import (
            ILocalContextReader,
        )

        assert ILocalContextReader is not None

    def test_port_has_read_method(self) -> None:
        """ILocalContextReader defines read() method."""
        from src.application.ports.secondary.ilocal_context_reader import (
            ILocalContextReader,
        )

        # Protocol should have read method
        assert hasattr(ILocalContextReader, "read")

    def test_port_has_get_active_project_method(self) -> None:
        """ILocalContextReader defines get_active_project() method."""
        from src.application.ports.secondary.ilocal_context_reader import (
            ILocalContextReader,
        )

        # Protocol should have get_active_project method
        assert hasattr(ILocalContextReader, "get_active_project")


# === Happy Path Tests (60%) ===


class TestLocalContextReaderHappyPath:
    """Happy path tests for LocalContextReader."""

    def test_read_returns_dict_when_file_exists(self, tmp_path: Path) -> None:
        """read() returns parsed dict when context.toml exists."""
        from src.infrastructure.adapters.persistence.filesystem_local_context_adapter import (
            FilesystemLocalContextAdapter,
        )

        # Arrange - create valid context.toml
        local_dir = tmp_path / ".jerry" / "local"
        local_dir.mkdir(parents=True)
        context_file = local_dir / "context.toml"
        context_file.write_text('[context]\nactive_project = "PROJ-001-test"\n')

        adapter = FilesystemLocalContextAdapter(base_path=tmp_path)

        # Act
        result = adapter.read()

        # Assert
        assert isinstance(result, dict)
        assert "context" in result
        assert result["context"]["active_project"] == "PROJ-001-test"

    def test_get_active_project_returns_project_id(self, tmp_path: Path) -> None:
        """get_active_project() returns project ID when set in context."""
        from src.infrastructure.adapters.persistence.filesystem_local_context_adapter import (
            FilesystemLocalContextAdapter,
        )

        # Arrange
        local_dir = tmp_path / ".jerry" / "local"
        local_dir.mkdir(parents=True)
        context_file = local_dir / "context.toml"
        context_file.write_text('[context]\nactive_project = "PROJ-007-jerry-bugs"\n')

        adapter = FilesystemLocalContextAdapter(base_path=tmp_path)

        # Act
        result = adapter.get_active_project()

        # Assert
        assert result == "PROJ-007-jerry-bugs"

    def test_read_handles_nested_structure(self, tmp_path: Path) -> None:
        """read() correctly parses nested TOML structure."""
        from src.infrastructure.adapters.persistence.filesystem_local_context_adapter import (
            FilesystemLocalContextAdapter,
        )

        # Arrange - create TOML with nested structure
        local_dir = tmp_path / ".jerry" / "local"
        local_dir.mkdir(parents=True)
        context_file = local_dir / "context.toml"
        context_file.write_text(
            '[context]\n'
            'active_project = "PROJ-001-test"\n'
            '\n'
            '[preferences]\n'
            'auto_save = true\n'
            'theme = "dark"\n'
        )

        adapter = FilesystemLocalContextAdapter(base_path=tmp_path)

        # Act
        result = adapter.read()

        # Assert
        assert result["context"]["active_project"] == "PROJ-001-test"
        assert result["preferences"]["auto_save"] is True
        assert result["preferences"]["theme"] == "dark"


# === Negative Tests (30%) ===


class TestLocalContextReaderNegative:
    """Negative tests for LocalContextReader."""

    def test_read_returns_empty_dict_when_file_missing(self, tmp_path: Path) -> None:
        """read() returns empty dict when context.toml doesn't exist."""
        from src.infrastructure.adapters.persistence.filesystem_local_context_adapter import (
            FilesystemLocalContextAdapter,
        )

        # Arrange - no context.toml file
        adapter = FilesystemLocalContextAdapter(base_path=tmp_path)

        # Act
        result = adapter.read()

        # Assert
        assert result == {}

    def test_read_returns_empty_dict_when_toml_invalid(self, tmp_path: Path) -> None:
        """read() returns empty dict when TOML is malformed."""
        from src.infrastructure.adapters.persistence.filesystem_local_context_adapter import (
            FilesystemLocalContextAdapter,
        )

        # Arrange - create invalid TOML
        local_dir = tmp_path / ".jerry" / "local"
        local_dir.mkdir(parents=True)
        context_file = local_dir / "context.toml"
        context_file.write_text("invalid toml [[[")

        adapter = FilesystemLocalContextAdapter(base_path=tmp_path)

        # Act
        result = adapter.read()

        # Assert
        assert result == {}

    def test_get_active_project_returns_none_when_not_set(
        self, tmp_path: Path
    ) -> None:
        """get_active_project() returns None when active_project not in context."""
        from src.infrastructure.adapters.persistence.filesystem_local_context_adapter import (
            FilesystemLocalContextAdapter,
        )

        # Arrange - context file without active_project
        local_dir = tmp_path / ".jerry" / "local"
        local_dir.mkdir(parents=True)
        context_file = local_dir / "context.toml"
        context_file.write_text('[preferences]\ntheme = "light"\n')

        adapter = FilesystemLocalContextAdapter(base_path=tmp_path)

        # Act
        result = adapter.get_active_project()

        # Assert
        assert result is None


# === Edge Case Tests (10%) ===


class TestLocalContextReaderEdgeCases:
    """Edge case tests for LocalContextReader."""

    def test_read_returns_empty_dict_when_file_empty(self, tmp_path: Path) -> None:
        """read() returns empty dict when context.toml is empty."""
        from src.infrastructure.adapters.persistence.filesystem_local_context_adapter import (
            FilesystemLocalContextAdapter,
        )

        # Arrange - create empty file
        local_dir = tmp_path / ".jerry" / "local"
        local_dir.mkdir(parents=True)
        context_file = local_dir / "context.toml"
        context_file.write_text("")

        adapter = FilesystemLocalContextAdapter(base_path=tmp_path)

        # Act
        result = adapter.read()

        # Assert
        assert result == {}

    def test_get_active_project_returns_none_when_file_missing(
        self, tmp_path: Path
    ) -> None:
        """get_active_project() returns None when file doesn't exist."""
        from src.infrastructure.adapters.persistence.filesystem_local_context_adapter import (
            FilesystemLocalContextAdapter,
        )

        # Arrange - no file
        adapter = FilesystemLocalContextAdapter(base_path=tmp_path)

        # Act
        result = adapter.get_active_project()

        # Assert
        assert result is None
