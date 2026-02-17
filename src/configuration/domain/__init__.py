# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
Configuration Domain Layer.

Pure domain logic for configuration management. This layer has no external
dependencies beyond the standard library and shared_kernel.

Components:
    - value_objects/: ConfigKey, ConfigPath, ConfigValue, ConfigSource
    - aggregates/: Configuration aggregate root
    - events/: Configuration domain events

Invariants:
    - No external imports (only stdlib and shared_kernel)
    - All value objects are immutable
    - All state changes emit domain events
"""

from __future__ import annotations
