# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Pytest configuration for Jerry Framework tests.

Note: Path manipulation removed - the editable install (`pip install -e .` or
`uv pip install -e .`) makes the `src` package available. No additional sys.path
manipulation is needed.

See: BUG-001 in projects/PROJ-003-agents-cleanup/WORKTRACKER.md
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest


def pytest_configure(config):  # noqa: ARG001
    """Configure pytest for Jerry Framework tests.

    Note: Previously manipulated sys.path here, but this conflicted with
    --import-mode=importlib. The editable install handles package resolution.

    Args:
        config: pytest Config object (unused, but required by pytest hook signature)
    """
    pass  # Placeholder for future configuration needs


@pytest.fixture()
def create_transcript():
    """Factory fixture for creating minimal JSONL transcript files.

    Returns a callable that creates a JSONL file with a single assistant
    entry containing the specified token count. Supports optional cache fields.

    References:
        - FEAT-001: Context Detection
        - PROJ-004: Context Resilience
    """

    def _create(
        path: Path,
        token_count: int,
        cache_creation: int = 0,
        cache_read: int = 0,
    ) -> Path:
        entry = {
            "type": "assistant",
            "message": {
                "role": "assistant",
                "usage": {
                    "input_tokens": token_count,
                    "cache_creation_input_tokens": cache_creation,
                    "cache_read_input_tokens": cache_read,
                },
            },
        }
        path.write_text(json.dumps(entry) + "\n")
        return path

    return _create
