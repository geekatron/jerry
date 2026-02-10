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
# ROOT DETECTION
# =============================================================================

# Marker files that indicate the Jerry framework root directory
_ROOT_MARKERS = ("pyproject.toml", "CLAUDE.md")


def _find_project_root(start: Path) -> Path:
    """
    Find the Jerry framework root directory by looking for marker files.

    This function walks up from the starting directory until it finds a directory
    containing one of the marker files (pyproject.toml or CLAUDE.md). This approach
    works regardless of what the repository directory is named (jerry, jerry-agent-cleanup,
    my-fork, etc.).

    Args:
        start: The starting directory to search from.

    Returns:
        Path to the Jerry framework root directory.

    Raises:
        RuntimeError: If no root directory can be found.

    References:
        - TD-001: Project validation tests use incorrect absolute paths
        - https://docs.python.org/3/library/pathlib.html
    """
    current = start.resolve()

    while current != current.parent:
        for marker in _ROOT_MARKERS:
            if (current / marker).exists():
                return current
        current = current.parent

    # If we reach here, we've hit the filesystem root without finding a marker
    raise RuntimeError(
        f"Could not find Jerry framework root directory. "
        f"Searched from {start} looking for: {_ROOT_MARKERS}. "
        f"Ensure you are running tests from within the Jerry repository."
    )


# =============================================================================
# CORE FIXTURES
# =============================================================================


@pytest.fixture(scope="session")
def project_root() -> Path:
    """
    Return the Jerry framework root directory.

    Uses marker file detection (pyproject.toml, CLAUDE.md) to find the root,
    making the fixture work regardless of the repository directory name.

    See TD-001 for details on why this approach is used.
    """
    return _find_project_root(Path(__file__).parent)


@pytest.fixture(scope="session")
def all_projects(project_root: Path) -> list[Path]:
    """Return all discovered project directories."""
    return discover_projects(project_root)


# Module-level discovery for fixture parameterization.
# Computed at test collection time, before fixtures are instantiated.
# pytest constraint: @pytest.fixture(params=...) cannot reference other fixtures.
_DISCOVERED_PROJECT_IDS: list[str] = []
_SENTINEL_NO_PROJECTS = "__NO_PROJECTS__"

try:
    _test_root = _find_project_root(Path(__file__).parent)
    _discovered_paths = discover_projects(_test_root)
    _DISCOVERED_PROJECT_IDS = sorted([p.name for p in _discovered_paths])
except (RuntimeError, OSError, PermissionError):
    # Root detection or directory traversal failed; tests will skip gracefully.
    pass


@pytest.fixture(
    params=_DISCOVERED_PROJECT_IDS if _DISCOVERED_PROJECT_IDS else [_SENTINEL_NO_PROJECTS]
)
def project_id(request: pytest.FixtureRequest) -> str:
    """Parameterized fixture that discovers all PROJ-* directories at collection time."""
    if request.param == _SENTINEL_NO_PROJECTS:
        pytest.skip("No PROJ-* directories found in repository")
    return request.param


@pytest.fixture
def proj_root(project_root: Path, project_id: str) -> Path:
    """Return the root directory for the current project under test.

    Skips if the project directory is missing or lacks required project
    files (e.g., in CI where the projects/ directory is gitignored).
    """
    path = project_root / "projects" / project_id
    has_plan = (path / "PLAN.md").exists()
    has_tracker = (path / "WORKTRACKER.md").exists()
    if not path.is_dir() or not (has_plan or has_tracker):
        pytest.skip(f"Project directory not available: {project_id}")
    return path


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
        "orchestration",  # Orchestration skill workflow state (per SKILL.md)
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
