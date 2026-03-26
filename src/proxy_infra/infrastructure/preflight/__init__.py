# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Pre-flight API key validation package for proxy infrastructure.

Exports:
    ApiKeyPreflightChecker: Validates API keys before mutating operations.
    PreflightResult: Immutable result value object.
    PreflightStatus: Enum of possible pre-flight outcomes.
    get_current_egress_ip: Helper to detect operator's current egress IP.

References:
    - TASK-023-048: API Key Pre-Flight Health Check
    - APIKEY-006: Pre-flight catches expired or revoked API keys
    - FM-009: Vultr IP ACL mismatch detection
"""

from src.proxy_infra.infrastructure.preflight.api_key_preflight import (
    ApiKeyPreflightChecker,
    get_current_egress_ip,
)
from src.proxy_infra.infrastructure.preflight.preflight_result import PreflightResult
from src.proxy_infra.infrastructure.preflight.preflight_status import PreflightStatus

__all__ = [
    "ApiKeyPreflightChecker",
    "PreflightResult",
    "PreflightStatus",
    "get_current_egress_ip",
]
