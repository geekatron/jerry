# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Exit code enumeration for tool execution.

Defines all exit codes used by the jerry tool exec CLI, matching the
behavioral contract from ADR-PROJ023-001.

References:
    - ADR-PROJ023-001: Error Handling (exit codes 0-6)
    - TASK-009: ExitCode enum
    - M-03: STRICT_MODE_VIOLATION added for --no-filter enforcement (T-06)
"""

from __future__ import annotations

from enum import IntEnum


class ExitCode(IntEnum):
    """Exit codes for the jerry tool exec command.

    Values 0-9 are reserved for the core tool execution framework.
    Values 10+ are reserved for family-specific extensions. Each family
    may define its own exit codes in the 10-19 range (rainbow), 20-29
    range (next family), etc.

    Attributes:
        SUCCESS: Tool executed successfully and output returned.
        UNKNOWN_TOOL: Tool command prefix not found in any resolution table.
        TOOL_ERROR: Tool executed but returned a non-zero exit code.
        CONTAINER_NOT_RUNNING: Container service not running and auto-start failed.
        CREDENTIAL_DETECTED: Credential detected in tool output; output quarantined.
        ENGAGEMENT_NOT_INIT: Required engagement directory not initialized.
        MODE_UNSET: Execution mode not set for a Zone 2/3 tool in strict mode.
        STRICT_MODE_VIOLATION: Forbidden flag used while JERRY_STRICT_MODE=true.
    """

    SUCCESS = 0
    UNKNOWN_TOOL = 1
    TOOL_ERROR = 2
    CONTAINER_NOT_RUNNING = 3
    CREDENTIAL_DETECTED = 4
    ENGAGEMENT_NOT_INIT = 5
    MODE_UNSET = 6
    # M-03 (T-06, DREAD 34): --no-filter is FORBIDDEN when JERRY_STRICT_MODE=true.
    # Exit code 7 signals that the command was rejected by the strict mode gate
    # before any tool execution occurred. OWASP A01:2021 Broken Access Control.
    STRICT_MODE_VIOLATION = 7
    # 10+ reserved for family-specific extensions:
    #   10-19: rainbow family
    #   20-29: reserved for future families
