"""
CLI Interface - Command Line Adapters

This package contains command-line interface adapters for Jerry Framework.
These are primary adapters that drive the application.

Modules:
    - main: Main CLI entry point (jerry command)
    - session_start: Hook for Claude Code session initialization
"""

from src.interface.cli.main import main
from src.interface.cli.session_start import main as session_start_main

__all__ = ["main", "session_start_main"]
