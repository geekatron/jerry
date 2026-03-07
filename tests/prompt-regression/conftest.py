# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Victor Lau

"""Shared pytest configuration for tests/prompt-regression/.

Adds the tests/prompt-regression directory to sys.path so that the
standalone version_keys.py module (which does not reside in the jerry
package) can be imported by test files without per-file path manipulation.

Moved from test_version_keys.py per eng-qa iter2 fix: Actionability (0.90
→ 0.93+) — sys.path manipulation belongs in conftest.py, not individual
test files.

References:
    - FR-004: Version key composite format {commit_hash}:{file_path}
    - tests/prompt-regression/version_keys.py
"""

from __future__ import annotations

import os
import sys

# Ensure the tests/prompt-regression directory is on sys.path so that
# `from version_keys import ...` works in unit test files.
_PR_TEST_DIR = os.path.dirname(__file__)
if _PR_TEST_DIR not in sys.path:
    sys.path.insert(0, _PR_TEST_DIR)
