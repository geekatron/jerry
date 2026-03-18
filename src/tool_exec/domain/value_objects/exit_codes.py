# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Exit code enumeration for tool execution.

Defines all exit codes used by the jerry tool exec CLI, matching the
behavioral contract from ADR-PROJ023-001.

References:
    - ADR-PROJ023-001: Error Handling (exit codes 0-6)
    - TASK-009: ExitCode enum
    - M-03: STRICT_MODE_VIOLATION added for --no-filter enforcement (T-06)
    - CV-008/CV-009: FIX-6 -- FAMILY_NOT_FOUND=7 and FAMILY_CONFIG_ERROR=8 added
"""

from __future__ import annotations

from enum import IntEnum


class ExitCode(IntEnum):
    """Exit codes for the jerry tool exec command.

    Values 0-10 are reserved for the core tool execution framework.
    Values 11 is the Zone 3 approval denial code.
    Values 12+ are reserved for family-specific extensions. Each family
    may define its own exit codes in the 12-19 range (rainbow), 20-29
    range (next family), etc.

    Attributes:
        SUCCESS: Tool executed successfully and output returned.
        UNKNOWN_TOOL: Tool command prefix not found in any resolution table.
        TOOL_ERROR: Tool executed but returned a non-zero exit code.
        CONTAINER_NOT_RUNNING: Container service not running and auto-start failed.
        CREDENTIAL_DETECTED: Credential detected in tool output; output quarantined.
        ENGAGEMENT_NOT_INIT: Required engagement directory not initialized.
        MODE_UNSET: Execution mode not set for a Zone 2/3 tool in strict mode.
        FAMILY_NOT_FOUND: Named family not found in the registry (CV-008, FIX-6).
        FAMILY_CONFIG_ERROR: Family registry config is malformed or missing required
            keys (CV-009, FIX-6).
        STRICT_MODE_VIOLATION: Forbidden flag used while JERRY_STRICT_MODE=true.
            M-03 (T-06, DREAD 34): --no-filter is FORBIDDEN when
            JERRY_STRICT_MODE=true. Exit code 9 signals that the command was
            rejected by the strict mode gate before any tool execution occurred.
            OWASP A01:2021 Broken Access Control.
        ZONE3_CONTAINER_REQUIRED: Zone 3 tool requested with --mode local, which
            violates the container_required policy (FM-002, FIX-3).
        ZONE3_APPROVAL_DENIED: Zone 3 per-operation approval gate denied --
            operator declined or non-TTY auto-deny fired (IN-015-R2, NEW-001).
            Distinct from ENGAGEMENT_NOT_INIT (5): 5 means the engagement was
            never initialized; 11 means it was initialized but the human approval
            gate rejected the specific operation.
    """

    SUCCESS = 0
    UNKNOWN_TOOL = 1
    TOOL_ERROR = 2
    CONTAINER_NOT_RUNNING = 3
    CREDENTIAL_DETECTED = 4
    ENGAGEMENT_NOT_INIT = 5
    MODE_UNSET = 6
    # CV-008 (FIX-6): Family not found in registry.
    FAMILY_NOT_FOUND = 7
    # CV-009 (FIX-6): Family registry config is malformed.
    FAMILY_CONFIG_ERROR = 8
    # M-03 (T-06, DREAD 34): Strict mode violation -- forbidden flag detected.
    STRICT_MODE_VIOLATION = 9
    # FM-002 (FIX-3): Zone 3 container enforcement -- local mode rejected.
    ZONE3_CONTAINER_REQUIRED = 10
    # IN-015-R2 / NEW-001: Zone 3 per-operation approval denied by operator.
    # Distinct from ENGAGEMENT_NOT_INIT (5): this signals that the approval gate
    # fired and the operator explicitly declined (or auto-denied in CI).
    ZONE3_APPROVAL_DENIED = 11
    # 12+ reserved for family-specific extensions:
    #   12-19: rainbow family
    #   20-29: reserved for future families
