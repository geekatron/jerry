"""
Unit tests for ConfigPath value object.

Tests cover:
    - AC-009.3: ConfigPath wraps Path with validation
    - AC-009.5: Immutability (frozen dataclass)
    - File type detection (TOML, JSON, YAML)

Test Categories:
    - Happy path: Valid path creation, property access
    - Negative: Invalid paths, None values
    - Edge cases: Relative paths, file type detection
"""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

import pytest

from src.configuration.domain.value_objects.config_path import ConfigPath
from src.shared_kernel.exceptions import ValidationError


class TestConfigPathCreation:
    """Tests for ConfigPath instantiation."""

    def test_create_from_absolute_path(self) -> None:
        """Absolute path is accepted."""
        path = ConfigPath(Path("/home/user/config.toml"))
        assert path.path.is_absolute()

    def test_create_from_relative_path_resolves_to_absolute(self) -> None:
        """Relative path is resolved to absolute."""
        path = ConfigPath(Path("config.toml"))
        assert path.path.is_absolute()

    def test_create_from_string(self) -> None:
        """from_string factory creates ConfigPath."""
        path = ConfigPath.from_string("/home/user/config.toml")
        assert path.name == "config.toml"

    def test_from_string_strips_whitespace(self) -> None:
        """from_string strips leading/trailing whitespace."""
        path = ConfigPath.from_string("  /home/user/config.toml  ")
        assert path.name == "config.toml"


class TestConfigPathValidation:
    """Tests for ConfigPath validation errors."""

    def test_none_path_raises_validation_error(self) -> None:
        """None path raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            ConfigPath(None)  # type: ignore[arg-type]
        assert exc_info.value.field == "path"
        assert "cannot be None" in str(exc_info.value)

    def test_from_string_empty_raises_validation_error(self) -> None:
        """Empty string raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            ConfigPath.from_string("")
        assert exc_info.value.field == "path"
        assert "cannot be empty" in str(exc_info.value)

    def test_from_string_whitespace_only_raises(self) -> None:
        """Whitespace-only string raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            ConfigPath.from_string("   ")
        assert "cannot be empty" in str(exc_info.value)


class TestConfigPathProperties:
    """Tests for ConfigPath property accessors."""

    def test_name_returns_filename(self) -> None:
        """name returns the file name."""
        path = ConfigPath(Path("/home/user/config.toml"))
        assert path.name == "config.toml"

    def test_stem_returns_name_without_extension(self) -> None:
        """stem returns name without extension."""
        path = ConfigPath(Path("/home/user/config.toml"))
        assert path.stem == "config"

    def test_extension_returns_suffix(self) -> None:
        """extension returns the file suffix."""
        path = ConfigPath(Path("/home/user/config.toml"))
        assert path.extension == ".toml"

    def test_extension_empty_for_no_extension(self) -> None:
        """extension is empty for files without extension."""
        path = ConfigPath(Path("/home/user/Makefile"))
        assert path.extension == ""

    def test_parent_returns_config_path(self) -> None:
        """parent returns ConfigPath of parent directory."""
        path = ConfigPath(Path("/home/user/config.toml"))
        parent = path.parent
        assert isinstance(parent, ConfigPath)
        assert parent.name == "user"


class TestConfigPathFileTypeDetection:
    """Tests for file type detection properties."""

    def test_is_toml_true_for_toml_extension(self) -> None:
        """is_toml returns True for .toml files."""
        path = ConfigPath(Path("config.toml"))
        assert path.is_toml is True

    def test_is_toml_case_insensitive(self) -> None:
        """is_toml is case-insensitive."""
        path = ConfigPath(Path("config.TOML"))
        assert path.is_toml is True

    def test_is_toml_false_for_other_extensions(self) -> None:
        """is_toml returns False for non-TOML files."""
        path = ConfigPath(Path("config.json"))
        assert path.is_toml is False

    def test_is_json_true_for_json_extension(self) -> None:
        """is_json returns True for .json files."""
        path = ConfigPath(Path("config.json"))
        assert path.is_json is True

    def test_is_json_case_insensitive(self) -> None:
        """is_json is case-insensitive."""
        path = ConfigPath(Path("config.JSON"))
        assert path.is_json is True

    def test_is_json_false_for_other_extensions(self) -> None:
        """is_json returns False for non-JSON files."""
        path = ConfigPath(Path("config.toml"))
        assert path.is_json is False

    def test_is_yaml_true_for_yaml_extension(self) -> None:
        """is_yaml returns True for .yaml files."""
        path = ConfigPath(Path("config.yaml"))
        assert path.is_yaml is True

    def test_is_yaml_true_for_yml_extension(self) -> None:
        """is_yaml returns True for .yml files."""
        path = ConfigPath(Path("config.yml"))
        assert path.is_yaml is True

    def test_is_yaml_case_insensitive(self) -> None:
        """is_yaml is case-insensitive."""
        path = ConfigPath(Path("config.YML"))
        assert path.is_yaml is True

    def test_is_yaml_false_for_other_extensions(self) -> None:
        """is_yaml returns False for non-YAML files."""
        path = ConfigPath(Path("config.toml"))
        assert path.is_yaml is False


class TestConfigPathNavigation:
    """Tests for path navigation methods."""

    def test_child_appends_segment(self) -> None:
        """child() appends a path segment."""
        path = ConfigPath(Path("/home/user"))
        child = path.child("config.toml")
        assert child.name == "config.toml"

    def test_child_chaining(self) -> None:
        """Multiple child calls build nested path."""
        path = ConfigPath(Path("/home"))
        nested = path.child("user").child(".jerry").child("config.toml")
        assert "user" in str(nested.path)
        assert ".jerry" in str(nested.path)
        assert nested.name == "config.toml"

    def test_truediv_operator(self) -> None:
        """/ operator creates child path."""
        path = ConfigPath(Path("/home"))
        child = path / "user" / "config.toml"
        assert child.name == "config.toml"

    def test_relative_to_base(self) -> None:
        """relative_to returns relative path."""
        base = ConfigPath(Path("/home/user"))
        full = ConfigPath(Path("/home/user/.jerry/config.toml"))
        relative = full.relative_to(base)
        assert str(relative) == ".jerry/config.toml"

    def test_relative_to_with_path(self, tmp_path: Path) -> None:
        """relative_to accepts Path object."""
        base = tmp_path
        full = ConfigPath(tmp_path / ".jerry" / "config.toml")
        relative = full.relative_to(base)
        assert str(relative) == ".jerry/config.toml"


class TestConfigPathFilesystemOperations:
    """Tests for filesystem operation methods."""

    def test_exists_returns_false_for_nonexistent(self, tmp_path: Path) -> None:
        """exists() returns False for non-existent path."""
        path = ConfigPath(tmp_path / "nonexistent.toml")
        assert path.exists() is False

    def test_exists_returns_true_for_existing(self, tmp_path: Path) -> None:
        """exists() returns True for existing path."""
        file_path = tmp_path / "config.toml"
        file_path.write_text("[config]")
        path = ConfigPath(file_path)
        assert path.exists() is True

    def test_is_file_returns_true_for_file(self, tmp_path: Path) -> None:
        """is_file() returns True for existing file."""
        file_path = tmp_path / "config.toml"
        file_path.write_text("[config]")
        path = ConfigPath(file_path)
        assert path.is_file() is True

    def test_is_file_returns_false_for_directory(self, tmp_path: Path) -> None:
        """is_file() returns False for directory."""
        path = ConfigPath(tmp_path)
        assert path.is_file() is False

    def test_is_directory_returns_true_for_directory(self, tmp_path: Path) -> None:
        """is_directory() returns True for existing directory."""
        path = ConfigPath(tmp_path)
        assert path.is_directory() is True

    def test_is_directory_returns_false_for_file(self, tmp_path: Path) -> None:
        """is_directory() returns False for file."""
        file_path = tmp_path / "config.toml"
        file_path.write_text("[config]")
        path = ConfigPath(file_path)
        assert path.is_directory() is False

    def test_is_readable_returns_true_for_readable_file(self, tmp_path: Path) -> None:
        """is_readable() returns True for readable file."""
        file_path = tmp_path / "config.toml"
        file_path.write_text("[config]")
        path = ConfigPath(file_path)
        assert path.is_readable() is True

    def test_is_readable_returns_false_for_nonexistent(self, tmp_path: Path) -> None:
        """is_readable() returns False for non-existent file."""
        path = ConfigPath(tmp_path / "nonexistent.toml")
        assert path.is_readable() is False

    def test_is_writable_for_existing_directory(self, tmp_path: Path) -> None:
        """is_writable() checks write permission."""
        path = ConfigPath(tmp_path)
        # tmp_path should be writable
        assert path.is_writable() is True

    def test_ensure_parent_exists_creates_directories(self, tmp_path: Path) -> None:
        """ensure_parent_exists() creates parent directories."""
        nested_path = tmp_path / "a" / "b" / "c" / "config.toml"
        path = ConfigPath(nested_path)
        path.ensure_parent_exists()
        assert path.parent.exists() is True


class TestConfigPathImmutability:
    """Tests for immutability (AC-009.5)."""

    def test_frozen_cannot_modify_path(self) -> None:
        """Frozen dataclass prevents attribute modification."""
        path = ConfigPath(Path("/home/user/config.toml"))
        with pytest.raises(AttributeError):
            path.path = Path("/other/path")  # type: ignore[misc]

    def test_equality_by_resolved_path(self) -> None:
        """Two ConfigPaths with same resolved path are equal."""
        path1 = ConfigPath(Path("/home/user/config.toml"))
        path2 = ConfigPath(Path("/home/user/config.toml"))
        assert path1 == path2

    def test_hash_consistency(self) -> None:
        """ConfigPaths can be used in sets/dicts."""
        path1 = ConfigPath(Path("/home/user/config.toml"))
        path2 = ConfigPath(Path("/home/user/config.toml"))
        path_set = {path1, path2}
        assert len(path_set) == 1


class TestConfigPathStringRepresentation:
    """Tests for string representations."""

    def test_str_returns_path_string(self) -> None:
        """str() returns the path as string."""
        path = ConfigPath(Path("/home/user/config.toml"))
        result = str(path)
        assert "config.toml" in result
        assert "/home/user" in result or "home/user" in result

    def test_repr_includes_class_name(self) -> None:
        """repr() includes class name for debugging."""
        path = ConfigPath(Path("/home/user/config.toml"))
        assert "ConfigPath" in repr(path)

    def test_fspath_protocol(self) -> None:
        """ConfigPath supports os.fspath() protocol."""
        import os
        path = ConfigPath(Path("/home/user/config.toml"))
        fspath = os.fspath(path)
        assert isinstance(fspath, str)
        assert "config.toml" in fspath
