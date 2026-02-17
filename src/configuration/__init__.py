# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
Configuration - Bounded context for Jerry configuration management.

This bounded context provides the domain model for managing hierarchical
configuration across the Jerry framework, including environment variables,
project-level settings, and framework defaults.

Key Components:
    - Value Objects: ConfigKey, ConfigPath, ConfigValue, ConfigSource
    - Aggregates: Configuration
    - Domain Events: ConfigurationLoaded, ConfigurationValueChanged, ConfigurationError

References:
    - ADR-PROJ004-001: JerryFramework Aggregate
    - ADR-PROJ004-004: JerrySession Context
    - WI-009, WI-010, WI-011: Domain Implementation
"""

from __future__ import annotations
