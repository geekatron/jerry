"""Pytest configuration for Jerry Framework tests.

Note: Path manipulation removed - the editable install (`pip install -e .` or
`uv pip install -e .`) makes the `src` package available. No additional sys.path
manipulation is needed.

See: BUG-001 in projects/PROJ-003-agents-cleanup/WORKTRACKER.md
"""

from __future__ import annotations


def pytest_configure(config):  # noqa: ARG001
    """Configure pytest for Jerry Framework tests.

    Note: Previously manipulated sys.path here, but this conflicted with
    --import-mode=importlib. The editable install handles package resolution.

    Args:
        config: pytest Config object (unused, but required by pytest hook signature)
    """
    pass  # Placeholder for future configuration needs
