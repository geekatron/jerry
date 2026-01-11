"""
CLI Interface - Command Line Adapters

This package contains command-line interface adapters for Jerry Framework.
These are primary adapters that drive the application.

Modules:
    - session_start: Hook for Claude Code session initialization
    - main: Main CLI entry point (placeholder)
"""

from src.interface.cli.session_start import main as session_start_main

__all__ = ["session_start_main"]
