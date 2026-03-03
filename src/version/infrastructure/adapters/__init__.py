# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Version infrastructure adapters."""

from __future__ import annotations

from .git_commit_log_reader import GitCommitLogReader
from .stdin_commit_reader import StdinCommitReader

__all__ = [
    "GitCommitLogReader",
    "StdinCommitReader",
]
