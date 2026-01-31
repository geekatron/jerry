"""Fixtures for transcript LLM validation tests.

WARNING: These tests invoke LLM agents and are:
- SLOW (minutes per test)
- EXPENSIVE (token costs)
- EXCLUDED FROM CI (use pytest -m llm to run)

Run manually with: pytest -m llm tests/llm/transcript/
"""

from __future__ import annotations

import json
from collections.abc import Generator
from pathlib import Path
from typing import Any

import pytest


@pytest.fixture(scope="module")
def llm_test_config() -> dict[str, Any]:
    """Configuration for LLM tests.

    Provides default settings that can be overridden via environment variables.
    """
    return {
        "timeout_seconds": 300,  # 5 minutes default
        "max_retries": 1,
        "model": "sonnet",  # Default model for testing
    }


@pytest.fixture
def golden_vtt_path() -> Path:
    """Path to meeting-006 golden VTT file (~90K tokens, 3071 segments)."""
    path = Path("skills/transcript/test_data/transcripts/golden/meeting-006-all-hands.vtt")
    if not path.exists():
        pytest.skip(f"Golden dataset not found: {path}")
    return path


@pytest.fixture
def chunked_input_path(temp_output_dir: Path) -> Generator[Path, None, None]:
    """Generate chunked input from meeting-006 for LLM tests.

    This fixture:
    1. Parses the golden VTT file
    2. Chunks it using TranscriptChunker
    3. Returns the path to index.json

    Note: Requires VTTParser and TranscriptChunker to be implemented.
    """
    # Import here to avoid issues if modules not yet implemented
    try:
        from src.transcript.application.services.chunker import TranscriptChunker
        from src.transcript.infrastructure.adapters.vtt_parser import VTTParser
    except ImportError:
        pytest.skip("VTTParser or TranscriptChunker not yet implemented")

    vtt_path = Path("skills/transcript/test_data/transcripts/golden/meeting-006-all-hands.vtt")
    if not vtt_path.exists():
        pytest.skip(f"Golden dataset not found: {vtt_path}")

    parser = VTTParser()
    chunker = TranscriptChunker()

    # Parse VTT file - returns ParseResult with segments
    parse_result = parser.parse(str(vtt_path))
    # Chunk the segments into index.json + chunks/
    index_path = chunker.chunk(parse_result.segments, str(temp_output_dir))

    yield Path(index_path)


@pytest.fixture
def extraction_report_schema() -> dict[str, Any]:
    """Load extraction-report.json schema for validation."""
    schema_path = Path("skills/transcript/test_data/schemas/extraction-report.json")
    if not schema_path.exists():
        pytest.skip(f"Schema not found: {schema_path}")
    with open(schema_path) as f:
        return json.load(f)


@pytest.fixture
def temp_output_dir(tmp_path: Path) -> Generator[Path, None, None]:
    """Temporary directory for LLM test outputs.

    Creates a dedicated subdirectory for each test.
    """
    output = tmp_path / "llm_test_output"
    output.mkdir(parents=True, exist_ok=True)
    yield output
