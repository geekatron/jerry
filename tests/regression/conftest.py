# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Conftest for regression tests — shared fixtures and CLI options."""

from __future__ import annotations

from typing import Any

import pytest


def pytest_addoption(parser: Any) -> None:
    """Add --update-golden CLI option to pytest."""
    parser.addoption(
        "--update-golden",
        action="store_true",
        default=False,
        help="Update golden files with current compose output",
    )


@pytest.fixture
def update_golden(request: pytest.FixtureRequest) -> bool:
    """Whether to update golden files instead of comparing."""
    return bool(request.config.getoption("--update-golden", default=False))
