# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
Jerry CLI Hooks Package.

Handlers for Claude Code hook events dispatched via the ``jerry hooks``
CLI subcommand group.

Hook handlers:
    - HooksPromptSubmitHandler: Handles UserPromptSubmit events
    - HooksSessionStartHandler: Handles SessionStart events
    - HooksPreCompactHandler: Handles PreCompact events
    - HooksPreToolUseHandler: Handles PreToolUse events

References:
    - EN-006: jerry hooks CLI Command Namespace
    - PROJ-004: Context Resilience
"""
