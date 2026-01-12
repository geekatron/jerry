"""
Pytest configuration and shared fixtures for project validation tests.

These fixtures support dynamic project discovery, allowing tests to run
against any PROJ-* directory in the repository.

Migration History:
    Originally: projects/PROJ-001-plugin-cleanup/tests/conftest.py
    Migrated: 2026-01-10 (TD-005)
    Purpose: BUG-001 regression prevention + ADR-003 enforcement
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass  # Reserved for future type imports

import pytest

# =============================================================================
# PROJECT DISCOVERY
# =============================================================================


def discover_projects(root: Path) -> list[Path]:
    """
    Discover all PROJ-* directories in the repository.

    Returns:
        List of paths to project directories matching PROJ-{NNN}-{slug} pattern.
    """
    projects_dir = root / "projects"
    if not projects_dir.exists():
        return []

    pattern = re.compile(r"PROJ-\d{3}-[a-z0-9-]+")
    return [p for p in projects_dir.iterdir() if p.is_dir() and pattern.match(p.name)]


# =============================================================================
# CORE FIXTURES
# =============================================================================


@pytest.fixture(scope="session")
def project_root() -> Path:
    """Return the Jerry framework root directory."""
    current = Path(__file__).parent
    while current.name != "jerry" and current.parent != current:
        current = current.parent
    return current


@pytest.fixture(scope="session")
def all_projects(project_root: Path) -> list[Path]:
    """Return all discovered project directories."""
    return discover_projects(project_root)


@pytest.fixture(params=["PROJ-001-plugin-cleanup"])  # Can be expanded dynamically
def project_id(request: pytest.FixtureRequest) -> str:
    """Parameterized fixture for project IDs."""
    return request.param


@pytest.fixture
def proj_root(project_root: Path, project_id: str) -> Path:
    """Return the root directory for the current project under test."""
    return project_root / "projects" / project_id


# =============================================================================
# PATTERN FIXTURES
# =============================================================================


@pytest.fixture
def old_path_pattern() -> re.Pattern[str]:
    """Regex pattern that matches old (incorrect) docs/ path format."""
    return re.compile(r"docs/(research|synthesis|analysis|decisions)/PROJ-\d{3}")


@pytest.fixture
def project_path_pattern() -> re.Pattern[str]:
    """Regex pattern that matches correct project-centric path format."""
    return re.compile(
        r"projects/PROJ-\d{3}-[a-z0-9-]+/(research|synthesis|analysis|decisions|reports|investigations|reviews)/"
    )


@pytest.fixture
def deprecated_patterns() -> list[tuple[str, str]]:
    """List of deprecated patterns with explanatory messages."""
    return [
        (r"docs/research/PROJ-", "Research should be in projects/{PROJ-ID}/research/"),
        (r"docs/synthesis/PROJ-", "Synthesis should be in projects/{PROJ-ID}/synthesis/"),
        (r"docs/analysis/PROJ-", "Analysis should be in projects/{PROJ-ID}/analysis/"),
        (r"docs/decisions/PROJ-", "Decisions should be in projects/{PROJ-ID}/decisions/"),
    ]


# =============================================================================
# CATEGORY FIXTURES
# =============================================================================


@pytest.fixture
def valid_categories() -> set[str]:
    """
    Valid category directories per ADR-003.

    These are the allowed subdirectories within a project workspace.
    """
    return {
        "research",
        "synthesis",
        "analysis",
        "decisions",
        "reports",
        "design",
        "investigations",
        "reviews",
        "work",  # Work tracking files
        "runbooks",  # Execution guides
    }


@pytest.fixture
def artifact_categories() -> set[str]:
    """
    Categories that contain document artifacts (for path validation).

    Subset of valid_categories that contain markdown documents.
    """
    return {
        "research",
        "synthesis",
        "analysis",
        "decisions",
        "reports",
        "investigations",
        "reviews",
    }


# =============================================================================
# UTILITY FIXTURES
# =============================================================================


@pytest.fixture
def markdown_link_pattern() -> re.Pattern[str]:
    """Regex pattern to extract markdown file references from backticks."""
    return re.compile(r"`([^`]+\.md)`")


def extract_project_references(content: str, project_id: str) -> set[str]:
    """
    Extract all document references for a specific project from content.

    Args:
        content: Markdown content to search
        project_id: Project ID (e.g., "PROJ-001-plugin-cleanup")

    Returns:
        Set of referenced file paths
    """
    pattern = rf"`(projects/{re.escape(project_id)}/[^`]+\.md)`"
    return set(re.findall(pattern, content))
