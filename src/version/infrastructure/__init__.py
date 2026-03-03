# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
Version Infrastructure Layer.

Exports adapters for commit log reading.
"""

from __future__ import annotations

from .adapters.git_commit_log_reader import GitCommitLogReader
from .adapters.stdin_commit_reader import StdinCommitReader

__all__ = [
    "GitCommitLogReader",
    "StdinCommitReader",
]
