"""
Pytest configuration and shared fixtures for PROJ-001 tests.

Test Pyramid Coverage:
- Unit: Path validation logic
- Integration: File system resolution
- System: Full grep validation
- E2E: Document traceability chain
- Contract: Document schema compliance
- Architecture: Path convention enforcement
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest


@pytest.fixture
def project_root() -> Path:
    """Return the Jerry framework root directory."""
    # Navigate from tests/ to project root
    current = Path(__file__).parent
    while current.name != "jerry" and current.parent != current:
        current = current.parent
    return current


@pytest.fixture
def proj_001_root(project_root: Path) -> Path:
    """Return the PROJ-001-plugin-cleanup directory."""
    return project_root / "projects" / "PROJ-001-plugin-cleanup"


@pytest.fixture
def phase7_artifacts(proj_001_root: Path) -> dict[str, Path]:
    """Return paths to all Phase 7 artifacts."""
    return {
        "e-006": proj_001_root / "synthesis" / "PROJ-001-e-006-unified-architecture-canon.md",
        "e-007": proj_001_root / "analysis" / "PROJ-001-e-007-implementation-gap-analysis.md",
        "e-009": proj_001_root / "analysis" / "PROJ-001-e-009-alignment-validation.md",
        "e-010": proj_001_root / "reports" / "PROJ-001-e-010-synthesis-status-report.md",
    }


@pytest.fixture
def old_path_pattern() -> re.Pattern:
    """Regex pattern that matches old (incorrect) path format."""
    return re.compile(r"docs/(research|synthesis|analysis|decisions)/PROJ-001")


@pytest.fixture
def new_path_pattern() -> re.Pattern:
    """Regex pattern that matches new (correct) path format."""
    return re.compile(
        r"projects/PROJ-001-plugin-cleanup/(research|synthesis|analysis|decisions|reports)/PROJ-001"
    )


@pytest.fixture
def markdown_link_pattern() -> re.Pattern:
    """Regex pattern to extract markdown file references."""
    return re.compile(r"`([^`]+\.md)`")
