# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
Configuration Domain Events.

Domain events for configuration lifecycle tracking.
All events are immutable and extend the DomainEvent base class.

Exports:
    ConfigurationLoaded: Emitted when configuration is successfully loaded
    ConfigurationValueChanged: Emitted when a configuration value is updated
    ConfigurationError: Emitted when configuration loading/parsing fails
"""

from __future__ import annotations

from src.configuration.domain.events.configuration_events import (
    ConfigurationError,
    ConfigurationLoaded,
    ConfigurationValueChanged,
)

__all__ = [
    "ConfigurationLoaded",
    "ConfigurationValueChanged",
    "ConfigurationError",
]
