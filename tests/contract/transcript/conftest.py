"""Fixtures for transcript contract tests.

Contract tests validate JSON schema compliance between components.
They ensure the parser output matches the chunker input schema, etc.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest


@pytest.fixture
def canonical_transcript_schema() -> dict[str, Any]:
    """Load canonical-transcript.json schema."""
    schema_path = Path("skills/transcript/test_data/schemas/canonical-transcript.json")
    if not schema_path.exists():
        pytest.skip(f"Schema not found: {schema_path}")
    with open(schema_path) as f:
        return json.load(f)


@pytest.fixture
def index_schema() -> dict[str, Any]:
    """Load index.json schema."""
    schema_path = Path("skills/transcript/test_data/schemas/index.json")
    if not schema_path.exists():
        pytest.skip(f"Schema not found: {schema_path}")
    with open(schema_path) as f:
        return json.load(f)


@pytest.fixture
def chunk_schema() -> dict[str, Any]:
    """Load chunk.json schema."""
    schema_path = Path("skills/transcript/test_data/schemas/chunk.json")
    if not schema_path.exists():
        pytest.skip(f"Schema not found: {schema_path}")
    with open(schema_path) as f:
        return json.load(f)


@pytest.fixture
def extraction_report_schema() -> dict[str, Any]:
    """Load extraction-report.json schema."""
    schema_path = Path("skills/transcript/test_data/schemas/extraction-report.json")
    if not schema_path.exists():
        pytest.skip(f"Schema not found: {schema_path}")
    with open(schema_path) as f:
        return json.load(f)


@pytest.fixture
def schemas_dir() -> Path:
    """Path to all schemas directory."""
    path = Path("skills/transcript/test_data/schemas")
    if not path.exists():
        pytest.skip(f"Schemas directory not found: {path}")
    return path
