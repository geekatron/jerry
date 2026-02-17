# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
Configuration Value Objects.

Immutable value objects for the configuration domain.

Exports:
    ConfigKey: Configuration key with dot-notation support
    ConfigPath: Validated filesystem path wrapper
    ConfigValue: Type-coercing configuration value wrapper
    ConfigSource: Enum for configuration source precedence levels
"""

from __future__ import annotations

from src.configuration.domain.value_objects.config_key import ConfigKey
from src.configuration.domain.value_objects.config_path import ConfigPath
from src.configuration.domain.value_objects.config_source import ConfigSource
from src.configuration.domain.value_objects.config_value import ConfigValue

__all__ = [
    "ConfigKey",
    "ConfigPath",
    "ConfigSource",
    "ConfigValue",
]
