# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Pre-flight check outcome enum (H-10: one class per file)."""

from enum import Enum


class PreflightStatus(str, Enum):
    """Possible outcomes of an API key pre-flight check.

    Attributes:
        PASS: Key is valid and properly scoped.
        WARNING: Check timed out; key validity cannot be confirmed but
            provisioning may proceed (network issues should not block ops).
        FAIL: Key is invalid, expired, or lacks required scope.
    """

    PASS = "PASS"
    WARNING = "WARNING"
    FAIL = "FAIL"
