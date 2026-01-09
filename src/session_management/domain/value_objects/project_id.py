"""
ProjectId - Value Object representing a valid project identifier.

Format: PROJ-{nnn}-{slug}
Where:
    - nnn: Three-digit zero-padded number (001-999)
    - slug: Kebab-case alphanumeric string (1-50 chars)

This is an immutable value object that validates on construction.
"""

from __future__ import annotations
import re
from dataclasses import dataclass

from ..exceptions import InvalidProjectIdError


# Validation constants
MIN_NUMBER = 1
MAX_NUMBER = 999
MIN_SLUG_LENGTH = 1
MAX_SLUG_LENGTH = 50

# Regex pattern for valid project IDs
# PROJ-{3 digits}-{kebab-case slug}
PROJECT_ID_PATTERN = re.compile(
    r"^PROJ-(\d{3})-([a-z][a-z0-9]*(?:-[a-z0-9]+)*)$"
)


@dataclass(frozen=True, slots=True)
class ProjectId:
    """Immutable value object representing a valid project identifier.

    Attributes:
        value: The full project ID string (e.g., "PROJ-001-plugin-cleanup")
        number: The numeric portion extracted from the ID (e.g., 1)
        slug: The slug portion extracted from the ID (e.g., "plugin-cleanup")
    """

    value: str
    number: int
    slug: str

    def __post_init__(self) -> None:
        """Validate the project ID components after initialization."""
        # Validate number range
        if not (MIN_NUMBER <= self.number <= MAX_NUMBER):
            raise InvalidProjectIdError(
                self.value,
                f"Number must be between {MIN_NUMBER} and {MAX_NUMBER}"
            )

        # Validate slug length
        if not (MIN_SLUG_LENGTH <= len(self.slug) <= MAX_SLUG_LENGTH):
            raise InvalidProjectIdError(
                self.value,
                f"Slug must be between {MIN_SLUG_LENGTH} and {MAX_SLUG_LENGTH} characters"
            )

    @classmethod
    def parse(cls, value: str | None) -> ProjectId:
        """Parse a string into a validated ProjectId.

        Args:
            value: The project ID string to parse

        Returns:
            A validated ProjectId instance

        Raises:
            InvalidProjectIdError: If the value is None, empty, or doesn't match the pattern
        """
        if value is None:
            raise InvalidProjectIdError("None", "Project ID cannot be None")

        if not value:
            raise InvalidProjectIdError("", "Project ID cannot be empty")

        value = value.strip()

        match = PROJECT_ID_PATTERN.match(value)
        if not match:
            raise InvalidProjectIdError(
                value,
                "Must match format PROJ-{nnn}-{slug} where nnn is 001-999 "
                "and slug is lowercase kebab-case"
            )

        number_str, slug = match.groups()
        number = int(number_str)

        # Validate number is not 000
        if number == 0:
            raise InvalidProjectIdError(value, "Number cannot be 000")

        return cls(value=value, number=number, slug=slug)

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
        # Validate number
        if not isinstance(number, int):
            raise InvalidProjectIdError(
                f"PROJ-???-{slug}",
                f"Number must be an integer, got {type(number).__name__}"
            )

        if not (MIN_NUMBER <= number <= MAX_NUMBER):
            raise InvalidProjectIdError(
                f"PROJ-{number:03d}-{slug}",
                f"Number must be between {MIN_NUMBER} and {MAX_NUMBER}"
            )

        # Validate slug
        if not slug:
            raise InvalidProjectIdError(
                f"PROJ-{number:03d}-",
                "Slug cannot be empty"
            )

        # Check slug format (lowercase kebab-case)
        if not re.match(r"^[a-z][a-z0-9]*(?:-[a-z0-9]+)*$", slug):
            raise InvalidProjectIdError(
                f"PROJ-{number:03d}-{slug}",
                "Slug must be lowercase kebab-case starting with a letter"
            )

        if len(slug) > MAX_SLUG_LENGTH:
            raise InvalidProjectIdError(
                f"PROJ-{number:03d}-{slug}",
                f"Slug exceeds maximum length of {MAX_SLUG_LENGTH} characters"
            )

        value = f"PROJ-{number:03d}-{slug}"
        return cls(value=value, number=number, slug=slug)

    def __str__(self) -> str:
        """Return the full project ID string."""
        return self.value

    def __repr__(self) -> str:
        """Return a detailed representation."""
        return f"ProjectId(value={self.value!r}, number={self.number}, slug={self.slug!r})"
