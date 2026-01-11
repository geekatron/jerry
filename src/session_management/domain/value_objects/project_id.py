"""
ProjectId - Value Object representing a valid project identifier.

Format: PROJ-{nnn}-{slug}
Where:
    - nnn: Three-digit zero-padded number (001-999)
    - slug: Kebab-case alphanumeric string (1-50 chars)

This is an immutable value object that extends VertexId from shared_kernel.

References:
    - ENFORCE-008d: Domain Refactoring
    - Canon PAT-001: VertexId Base Class
    - ADR-013: Shared Kernel Module
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from re import Pattern
from typing import ClassVar

from src.shared_kernel.vertex_id import VertexId

from ..exceptions import InvalidProjectIdError

# Validation constants
MIN_NUMBER = 1
MAX_NUMBER = 999
MIN_SLUG_LENGTH = 1
MAX_SLUG_LENGTH = 50


@dataclass(frozen=True)
class ProjectId(VertexId):
    """Immutable value object representing a valid project identifier.

    Extends VertexId from shared_kernel for graph-ready identity.
    Format: PROJ-{nnn}-{slug} where nnn is 001-999 and slug is kebab-case.

    Attributes:
        value: The full project ID string (inherited from VertexId)

    Properties:
        number: The numeric portion extracted from the ID (e.g., 1)
        slug: The slug portion extracted from the ID (e.g., "plugin-cleanup")

    Example:
        >>> project_id = ProjectId.parse("PROJ-001-plugin-cleanup")
        >>> project_id.number
        1
        >>> project_id.slug
        'plugin-cleanup'
    """

    # Regex pattern for valid project IDs
    _PATTERN: ClassVar[Pattern[str]] = re.compile(r"^PROJ-(\d{3})-([a-z][a-z0-9]*(?:-[a-z0-9]+)*)$")

    @classmethod
    def _is_valid_format(cls, value: str) -> bool:
        """Validate project ID format.

        Args:
            value: The string to validate

        Returns:
            True if format is valid PROJ-{nnn}-{slug}
        """
        match = cls._PATTERN.match(value)
        if not match:
            return False

        number_str, slug = match.groups()
        number = int(number_str)

        # Number must be 001-999
        if not (MIN_NUMBER <= number <= MAX_NUMBER):
            return False

        # Slug must be within length limits
        if not (MIN_SLUG_LENGTH <= len(slug) <= MAX_SLUG_LENGTH):
            return False

        return True

    @classmethod
    def generate(cls) -> ProjectId:
        """Generate a new ProjectId.

        Note: ProjectId requires a number and slug, so generate() is not
        directly supported. Use create(number, slug) instead.

        Raises:
            NotImplementedError: Always, as ProjectId requires components
        """
        raise NotImplementedError("ProjectId requires number and slug; use create(number, slug)")

    @classmethod
    def from_string(cls, value: str) -> ProjectId:
        """Parse ID from string representation.

        This is the VertexId-compatible factory method.

        Args:
            value: The project ID string to parse

        Returns:
            A validated ProjectId instance

        Raises:
            ValueError: If the format is invalid (via VertexId.__post_init__)
        """
        return cls(value)

    @classmethod
    def parse(cls, value: str | None) -> ProjectId:
        """Parse a string into a validated ProjectId.

        Backwards-compatible factory method.

        Args:
            value: The project ID string to parse

        Returns:
            A validated ProjectId instance

        Raises:
            InvalidProjectIdError: If the value is None, empty, or invalid format
        """
        if value is None:
            raise InvalidProjectIdError("None", "Project ID cannot be None")

        if not value:
            raise InvalidProjectIdError("", "Project ID cannot be empty")

        value = value.strip()

        if not cls._is_valid_format(value):
            raise InvalidProjectIdError(
                value,
                "Must match format PROJ-{nnn}-{slug} where nnn is 001-999 "
                "and slug is lowercase kebab-case",
            )

        return cls(value)

    @classmethod
    def create(cls, number: int, slug: str) -> ProjectId:
        """Create a new ProjectId from components.

        Args:
            number: The project number (1-999)
            slug: The project slug (kebab-case)

        Returns:
            A validated ProjectId instance

        Raises:
            InvalidProjectIdError: If components are invalid
        """
        # Validate number type
        if not isinstance(number, int):
            raise InvalidProjectIdError(
                f"PROJ-???-{slug}", f"Number must be an integer, got {type(number).__name__}"
            )

        # Validate number range
        if not (MIN_NUMBER <= number <= MAX_NUMBER):
            raise InvalidProjectIdError(
                f"PROJ-{number:03d}-{slug}" if number >= 0 else f"PROJ-{number}-{slug}",
                f"Number must be between {MIN_NUMBER} and {MAX_NUMBER}",
            )

        # Validate slug exists
        if not slug:
            raise InvalidProjectIdError(f"PROJ-{number:03d}-", "Slug cannot be empty")

        # Check slug format (lowercase kebab-case)
        if not re.match(r"^[a-z][a-z0-9]*(?:-[a-z0-9]+)*$", slug):
            raise InvalidProjectIdError(
                f"PROJ-{number:03d}-{slug}",
                "Slug must be lowercase kebab-case starting with a letter",
            )

        # Check slug length
        if len(slug) > MAX_SLUG_LENGTH:
            raise InvalidProjectIdError(
                f"PROJ-{number:03d}-{slug}",
                f"Slug exceeds maximum length of {MAX_SLUG_LENGTH} characters",
            )

        value = f"PROJ-{number:03d}-{slug}"
        return cls(value)

    @property
    def number(self) -> int:
        """Extract the numeric portion from the project ID.

        Returns:
            The project number (1-999)
        """
        match = self._PATTERN.match(self.value)
        if match:
            return int(match.group(1))
        # This shouldn't happen for a valid ProjectId
        return 0

    @property
    def slug(self) -> str:
        """Extract the slug portion from the project ID.

        Returns:
            The project slug (kebab-case string)
        """
        match = self._PATTERN.match(self.value)
        if match:
            return match.group(2)
        # This shouldn't happen for a valid ProjectId
        return ""

    def __repr__(self) -> str:
        """Return a detailed representation."""
        return f"ProjectId(value={self.value!r}, number={self.number}, slug={self.slug!r})"
