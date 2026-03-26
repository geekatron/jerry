# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""InvalidNodeTransitionError domain exception for proxy infrastructure."""

from __future__ import annotations


class InvalidNodeTransitionError(Exception):
    """Raised when a node lifecycle transition is not permitted by the state machine.

    The proxy node state machine defines a directed acyclic graph of allowed
    transitions. Attempting an out-of-graph transition raises this error.
    """
