# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Tests for the switch that decides whether the archive tests run.

The archive tests build, list and read real archives. They are on by default on
Linux and off elsewhere. ``JERRY_RELEASE_ARCHIVE_TESTS=1`` forces them on and
``JERRY_RELEASE_ARCHIVE_TESTS=0`` forces them off, without a code change. The
reason is part of the skip message, so ``pytest -rs`` says why a test was
skipped.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))

from release_test_support import ARCHIVE_SWITCH, archive_tests_state  # noqa: E402

pytestmark = pytest.mark.unit


def test_the_archive_tests_are_on_by_default_on_linux(monkeypatch: pytest.MonkeyPatch) -> None:
    """On Linux, with no switch set, the archive tests run and the reason says so."""
    monkeypatch.delenv(ARCHIVE_SWITCH, raising=False)
    monkeypatch.setattr(sys, "platform", "linux")
    assert archive_tests_state() == (True, False, "archive tests run by default on Linux")


@pytest.mark.parametrize("platform", ["darwin", "win32", "freebsd14"])
def test_the_archive_tests_are_off_by_default_elsewhere_and_the_reason_names_the_switch(
    platform: str, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Off Linux the archive tests skip by default, and the skip reason names the switch."""
    monkeypatch.delenv(ARCHIVE_SWITCH, raising=False)
    monkeypatch.setattr(sys, "platform", platform)
    enabled, forced, reason = archive_tests_state()
    assert (enabled, forced) == (False, False)
    assert "archive tests run only on Linux unless JERRY_RELEASE_ARCHIVE_TESTS=1" in reason
    assert platform in reason


@pytest.mark.parametrize("platform", ["linux", "darwin"])
def test_the_switch_set_to_one_forces_the_archive_tests_on(
    platform: str, monkeypatch: pytest.MonkeyPatch
) -> None:
    """JERRY_RELEASE_ARCHIVE_TESTS=1 turns the archive tests on, whatever the platform."""
    monkeypatch.setenv(ARCHIVE_SWITCH, "1")
    monkeypatch.setattr(sys, "platform", platform)
    enabled, forced, reason = archive_tests_state()
    assert (enabled, forced) == (True, True)
    assert "JERRY_RELEASE_ARCHIVE_TESTS=1" in reason


@pytest.mark.parametrize("platform", ["linux", "darwin"])
def test_the_switch_set_to_zero_forces_the_archive_tests_off(
    platform: str, monkeypatch: pytest.MonkeyPatch
) -> None:
    """JERRY_RELEASE_ARCHIVE_TESTS=0 turns the archive tests off, even on Linux."""
    monkeypatch.setenv(ARCHIVE_SWITCH, "0")
    monkeypatch.setattr(sys, "platform", platform)
    enabled, forced, reason = archive_tests_state()
    assert (enabled, forced) == (False, True)
    assert "JERRY_RELEASE_ARCHIVE_TESTS=0" in reason


@pytest.mark.parametrize("value", ["", " ", "yes", "true", "2"])
def test_any_other_value_of_the_switch_leaves_the_default_in_place(
    value: str, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A switch value other than 0 or 1 is ignored, and the platform default applies."""
    monkeypatch.setenv(ARCHIVE_SWITCH, value)
    monkeypatch.setattr(sys, "platform", "darwin")
    assert archive_tests_state()[:2] == (False, False)
    monkeypatch.setattr(sys, "platform", "linux")
    assert archive_tests_state()[:2] == (True, False)
