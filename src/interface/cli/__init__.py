# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
CLI Interface - Command Line Adapters

This package contains command-line interface adapters for Jerry Framework.
These are primary adapters that drive the application.

Modules:
    - main: Main CLI entry point (jerry command)

EN-001: Removed session_start module (TD-004). Session hook now calls main CLI.
"""

from src.interface.cli.main import main

__all__ = ["main"]
