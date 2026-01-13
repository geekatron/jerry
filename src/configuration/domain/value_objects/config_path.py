"""
ConfigPath - Immutable filesystem path wrapper with validation.

Wraps pathlib.Path with validation and domain-specific operations
for configuration file paths.

References:
    - WI-009: Configuration Value Objects
    - AC-009.3: ConfigPath value object wraps Path with validation
    - PAT-VO-001: Immutable Value Object pattern

Exports:
    ConfigPath: Immutable path value object for configuration files
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from src.shared_kernel.exceptions import ValidationError


@dataclass(frozen=True, slots=True)
class ConfigPath:
    """
    Immutable filesystem path for configuration files.

    Wraps pathlib.Path with validation and convenience methods
    specific to configuration file handling.

    Attributes:
        path: The underlying Path object

    Invariants:
        - Path cannot be None
        - Path is always resolved to absolute form

    Examples:
        >>> config_path = ConfigPath(Path("/home/user/.jerry/config.toml"))
        >>> config_path.exists()
        False
        >>> config_path.extension
        '.toml'
        >>> config_path.is_toml
        True

    Note:
        Existence is NOT validated at construction time. This allows
        referencing paths that may be created later.
    """

    path: Path

    def __post_init__(self) -> None:
        """Validate and normalize path after initialization."""
        if self.path is None:
            raise ValidationError(
                field="path",
                message="Configuration path cannot be None",
            )

        # Resolve to absolute path using object.__setattr__ since frozen
        resolved = self.path.resolve()
        object.__setattr__(self, "path", resolved)

    @classmethod
    def from_string(cls, path_str: str) -> ConfigPath:
        """
        Create ConfigPath from string.

        Args:
            path_str: Path as string

        Returns:
            ConfigPath wrapping the path

        Raises:
            ValidationError: If path_str is empty

        Example:
            >>> ConfigPath.from_string("/home/user/config.toml")
            ConfigPath(path=PosixPath('/home/user/config.toml'))
        """
        if not path_str or not path_str.strip():
            raise ValidationError(
                field="path",
                message="Configuration path cannot be empty",
            )
        return cls(Path(path_str.strip()))

    @property
    def name(self) -> str:
        """
        Get the file name.

        Returns:
            File name including extension

        Example:
            >>> ConfigPath(Path("/home/user/config.toml")).name
            'config.toml'
        """
        return self.path.name

    @property
    def stem(self) -> str:
        """
        Get the file name without extension.

        Returns:
            File name without extension

        Example:
            >>> ConfigPath(Path("/home/user/config.toml")).stem
            'config'
        """
        return self.path.stem

    @property
    def extension(self) -> str:
        """
        Get the file extension.

        Returns:
            File extension including dot

        Example:
            >>> ConfigPath(Path("/home/user/config.toml")).extension
            '.toml'
        """
        return self.path.suffix

    @property
    def parent(self) -> ConfigPath:
        """
        Get the parent directory as ConfigPath.

        Returns:
            ConfigPath of parent directory

        Example:
            >>> ConfigPath(Path("/home/user/config.toml")).parent
            ConfigPath(path=PosixPath('/home/user'))
        """
        return ConfigPath(self.path.parent)

    @property
    def is_toml(self) -> bool:
        """
        Check if this is a TOML configuration file.

        Returns:
            True if extension is .toml

        Example:
            >>> ConfigPath(Path("config.toml")).is_toml
            True
        """
        return self.extension.lower() == ".toml"

    @property
    def is_json(self) -> bool:
        """
        Check if this is a JSON configuration file.

        Returns:
            True if extension is .json

        Example:
            >>> ConfigPath(Path("config.json")).is_json
            True
        """
        return self.extension.lower() == ".json"

    @property
    def is_yaml(self) -> bool:
        """
        Check if this is a YAML configuration file.

        Returns:
            True if extension is .yaml or .yml

        Example:
            >>> ConfigPath(Path("config.yaml")).is_yaml
            True
        """
        return self.extension.lower() in (".yaml", ".yml")

    def exists(self) -> bool:
        """
        Check if the path exists on the filesystem.

        Returns:
            True if path exists

        Example:
            >>> ConfigPath(Path("/etc/passwd")).exists()
            True
        """
        return self.path.exists()

    def is_file(self) -> bool:
        """
        Check if the path is an existing file.

        Returns:
            True if path exists and is a file
        """
        return self.path.is_file()

    def is_directory(self) -> bool:
        """
        Check if the path is an existing directory.

        Returns:
            True if path exists and is a directory
        """
        return self.path.is_dir()

    def is_readable(self) -> bool:
        """
        Check if the file exists and is readable.

        Returns:
            True if file exists and can be read

        Note:
            This checks actual filesystem permissions.
        """
        if not self.path.exists():
            return False
        try:
            # Try to open for reading
            with self.path.open("r"):
                return True
        except (PermissionError, OSError):
            return False

    def is_writable(self) -> bool:
        """
        Check if the file/directory is writable.

        Returns:
            True if file exists and can be written, or
            directory exists and new files can be created
        """
        import os
        return os.access(self.path, os.W_OK)

    def child(self, name: str) -> ConfigPath:
        """
        Create a child path.

        Args:
            name: Child name or relative path

        Returns:
            New ConfigPath for the child

        Example:
            >>> ConfigPath(Path("/home/user")).child("config.toml")
            ConfigPath(path=PosixPath('/home/user/config.toml'))
        """
        return ConfigPath(self.path / name)

    def relative_to(self, base: ConfigPath | Path) -> Path:
        """
        Get path relative to a base.

        Args:
            base: Base path to compute relative path from

        Returns:
            Relative path

        Raises:
            ValueError: If this path is not relative to base
        """
        base_path = base.path if isinstance(base, ConfigPath) else base
        return self.path.relative_to(base_path)

    def ensure_parent_exists(self) -> None:
        """
        Create parent directories if they don't exist.

        Creates all parent directories with default permissions.
        """
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def __truediv__(self, other: str) -> ConfigPath:
        """
        Support / operator for path joining.

        Args:
            other: Path segment to join

        Returns:
            New ConfigPath with joined segment

        Example:
            >>> ConfigPath(Path("/home")) / "user" / "config.toml"
            ConfigPath(path=PosixPath('/home/user/config.toml'))
        """
        return self.child(other)

    def __str__(self) -> str:
        """Return path as string for display."""
        return str(self.path)

    def __repr__(self) -> str:
        """Return detailed representation for debugging."""
        return f"ConfigPath(path={self.path!r})"

    def __fspath__(self) -> str:
        """Support os.fspath() protocol."""
        return str(self.path)
