# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Victor Lau

"""Baseline persistence package for the Four-Layer Composite Test Harness.

Provides the BaselineStore adapter for storing and retrieving baseline score
records keyed by git commit hash and agent definition file path (FR-004,
FR-020), and the BaselinePersistencePort protocol for dependency inversion.

Public API:
    from jerry.testing.baselines import BaselineStore
    from jerry.testing.baselines import BaselinePersistencePort
"""

from jerry.testing.baselines.ports import BaselinePersistencePort
from jerry.testing.baselines.store import BaselineStore

__all__ = ["BaselineStore", "BaselinePersistencePort"]
