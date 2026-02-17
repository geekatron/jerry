# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Fixtures for transcript unit tests.

Unit tests are fast (< 1s) and require no external I/O.
All fixtures provide in-memory test data only.
"""

from __future__ import annotations

import pytest


@pytest.fixture
def sample_vtt_content() -> str:
    """Sample VTT content for unit tests."""
    return """WEBVTT

00:00:00.000 --> 00:00:05.000
<v John>Hello, welcome to the meeting.

00:00:05.000 --> 00:00:10.000
<v Jane>Thanks for joining everyone.

00:00:10.000 --> 00:00:15.000
<v John>Let's start with the agenda.
"""


@pytest.fixture
def sample_srt_content() -> str:
    """Sample SRT content for unit tests."""
    return """1
00:00:00,000 --> 00:00:05,000
John: Hello, welcome to the meeting.

2
00:00:05,000 --> 00:00:10,000
Jane: Thanks for joining everyone.

3
00:00:10,000 --> 00:00:15,000
John: Let's start with the agenda.
"""


@pytest.fixture
def sample_plain_text_content() -> str:
    """Sample plain text content for unit tests."""
    return """John: Hello, welcome to the meeting.
Jane: Thanks for joining everyone.
John: Let's start with the agenda.
"""
