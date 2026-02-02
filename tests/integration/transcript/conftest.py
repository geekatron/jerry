"""Fixtures for transcript integration tests.

Integration tests may use the filesystem but do NOT invoke LLM agents.
They are fast enough for CI and validate Python-layer component interaction.
"""

from __future__ import annotations

from collections.abc import Generator
from pathlib import Path

import pytest


@pytest.fixture
def golden_vtt_path() -> Path:
    """Path to meeting-006 golden VTT file (~90K tokens, 3071 segments)."""
    path = Path("skills/transcript/test_data/transcripts/golden/meeting-006-all-hands.vtt")
    if not path.exists():
        pytest.skip(f"Golden dataset not found: {path}")
    return path


@pytest.fixture
def small_vtt_path() -> Path:
    """Path to meeting-001 small VTT file for quick tests."""
    path = Path("skills/transcript/test_data/transcripts/golden/meeting-001.vtt")
    if not path.exists():
        pytest.skip(f"Test dataset not found: {path}")
    return path


@pytest.fixture
def temp_output_dir(tmp_path: Path) -> Generator[Path, None, None]:
    """Temporary directory for test outputs.

    Creates a dedicated subdirectory and cleans up after test.
    """
    output = tmp_path / "transcript_output"
    output.mkdir(parents=True, exist_ok=True)
    yield output
    # Cleanup happens automatically via tmp_path fixture


@pytest.fixture
def temp_chunked_dir(tmp_path: Path) -> Path:
    """Temporary directory for chunked output."""
    chunked = tmp_path / "chunked"
    chunked.mkdir(parents=True, exist_ok=True)
    return chunked


@pytest.fixture
def golden_datasets_dir() -> Path:
    """Path to golden datasets directory."""
    path = Path("skills/transcript/test_data/transcripts/golden")
    if not path.exists():
        pytest.skip(f"Golden datasets directory not found: {path}")
    return path


@pytest.fixture
def schemas_dir() -> Path:
    """Path to JSON schemas directory."""
    path = Path("skills/transcript/test_data/schemas")
    if not path.exists():
        pytest.skip(f"Schemas directory not found: {path}")
    return path
