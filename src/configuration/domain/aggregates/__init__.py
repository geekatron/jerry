# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
Configuration Domain Aggregates.

Aggregate roots for the configuration bounded context.

Exports:
    Configuration: Aggregate root for configuration management
"""

from __future__ import annotations

from src.configuration.domain.aggregates.configuration import Configuration

__all__ = [
    "Configuration",
]
