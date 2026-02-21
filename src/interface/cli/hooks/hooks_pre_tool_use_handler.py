# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
HooksPreToolUseHandler - CLI handler for the PreToolUse hook.

Reads Claude Code ``PreToolUse`` JSON from stdin, invokes the
PreToolEnforcementEngine for architecture validation, and the
StalenessDetector for ORCHESTRATION.yaml staleness checks.

Returns a JSON response with the enforcement decision. If the decision
is "block", the response includes ``decision: "block"`` and the reason.
If it is "warn", a warning is added. All other cases approve passthrough.

Design Principles:
    - **Fail-open everywhere**: Each step is wrapped in try/except.
      Step failures log to stderr, but processing continues.
    - **Exit 0 always**: The handler always exits 0 even on partial failure.
    - **Valid JSON always**: The response is always valid JSON.

References:
    - EN-006: jerry hooks CLI Command Namespace
    - EN-703: PreToolUse Enforcement Engine
    - EN-005: PreToolUse Staleness Detection
    - PROJ-004: Context Resilience
"""

from __future__ import annotations

import json
import logging
import sys
from datetime import datetime, timezone
from typing import Any

from src.context_monitoring.infrastructure.adapters.staleness_detector import (
    StalenessDetector,
)
from src.infrastructure.internal.enforcement.enforcement_decision import (
    EnforcementDecision,
)
from src.infrastructure.internal.enforcement.pre_tool_enforcement_engine import (
    PreToolEnforcementEngine,
)

logger = logging.getLogger(__name__)

# Tool names that trigger write enforcement
_WRITE_TOOLS = frozenset({"Write", "MultiEdit", "NotebookEdit"})

# Tool names that trigger edit enforcement
_EDIT_TOOLS = frozenset({"Edit"})

# Tool names that have a file_path we can check for staleness
_FILE_TARGET_TOOLS = frozenset({"Write", "Edit", "Read", "NotebookEdit"})


class HooksPreToolUseHandler:
    """CLI handler for the Claude Code PreToolUse hook.

    Evaluates tool use requests against architectural constraints via the
    PreToolEnforcementEngine and checks ORCHESTRATION.yaml staleness via
    the StalenessDetector.

    Each processing step is fail-open: failures log to stderr and
    processing continues. The final response always contains valid JSON.

    Attributes:
        _enforcement_engine: Engine for AST-based architecture validation.
        _staleness_detector: Detector for ORCHESTRATION.yaml staleness.

    Example:
        >>> handler = HooksPreToolUseHandler(
        ...     enforcement_engine=engine,
        ...     staleness_detector=detector,
        ... )
        >>> exit_code = handler.handle(stdin_json)
    """

    def __init__(
        self,
        enforcement_engine: PreToolEnforcementEngine,
        staleness_detector: StalenessDetector,
    ) -> None:
        """Initialize the handler with required services.

        Args:
            enforcement_engine: AST-based architecture enforcement engine.
            staleness_detector: ORCHESTRATION.yaml staleness detector.
        """
        self._enforcement_engine = enforcement_engine
        self._staleness_detector = staleness_detector

    def handle(self, stdin_json: str) -> int:
        """Handle a PreToolUse hook event.

        Extracts tool_name and tool_input from hook input, runs enforcement
        and staleness checks (both fail-open), and prints the response JSON.

        The response format follows Claude Code hook protocol:
        - For block decisions: ``{"decision": "block", "reason": "..."}``
        - For warn decisions: ``{"decision": "warn", "reason": "..."}``
        - For approve decisions: ``{}`` (empty, passthrough)

        Args:
            stdin_json: The JSON payload from the Claude Code hook.

        Returns:
            Exit code (always 0).
        """
        response: dict[str, Any] = {}

        # Step 1: Parse hook input (fail-open)
        hook_data: dict[str, Any] = {}
        try:
            hook_data = json.loads(stdin_json)
        except (json.JSONDecodeError, ValueError) as exc:
            print(f"[hooks/pre-tool-use] Failed to parse hook input: {exc}", file=sys.stderr)

        tool_name: str = hook_data.get("tool_name", "")
        tool_input: dict[str, Any] = hook_data.get("tool_input", {})
        file_path: str = tool_input.get("file_path", "")

        # Step 2: Architecture enforcement (fail-open)
        try:
            decision = self._run_enforcement(tool_name, tool_input)
            if decision is not None:
                if decision.action == "block":
                    response["decision"] = "block"
                    response["reason"] = decision.reason
                    if decision.violations:
                        response["violations"] = decision.violations
                    if decision.criticality_escalation:
                        response["criticality_escalation"] = decision.criticality_escalation
                elif decision.action == "warn":
                    response["decision"] = "warn"
                    response["reason"] = decision.reason
                    if decision.criticality_escalation:
                        response["criticality_escalation"] = decision.criticality_escalation
        except Exception as exc:  # noqa: BLE001
            print(
                f"[hooks/pre-tool-use] Enforcement engine failed: {exc}",
                file=sys.stderr,
            )

        # Step 3: Staleness detection (fail-open) - only if we have a file path
        if file_path and "decision" not in response:
            try:
                reference_time = datetime.now(timezone.utc)
                staleness = self._staleness_detector.check_staleness(
                    tool_target_path=file_path,
                    reference_time=reference_time,
                )
                if staleness.is_stale and staleness.warning_message:
                    # Add staleness warning to response
                    existing_reason = response.get("reason", "")
                    staleness_suffix = f"Staleness warning: {staleness.warning_message}"
                    response["staleness_warning"] = staleness.warning_message
                    if not existing_reason:
                        response["reason"] = staleness_suffix
            except Exception as exc:  # noqa: BLE001
                print(
                    f"[hooks/pre-tool-use] Staleness detection failed: {exc}",
                    file=sys.stderr,
                )

        # Emit response (always valid JSON)
        print(json.dumps(response))
        return 0

    def _run_enforcement(
        self,
        tool_name: str,
        tool_input: dict[str, Any],
    ) -> EnforcementDecision | None:
        """Run enforcement checks based on tool name.

        For Write/NotebookEdit tools: calls evaluate_write.
        For Edit tools: calls evaluate_edit.
        All others: no enforcement, returns None.

        Args:
            tool_name: The name of the Claude Code tool being invoked.
            tool_input: The tool input parameters dict.

        Returns:
            EnforcementDecision or None if no enforcement applies.
        """
        file_path: str = tool_input.get("file_path", "")

        if tool_name in _WRITE_TOOLS:
            content: str = tool_input.get("content", "")
            return self._enforcement_engine.evaluate_write(file_path, content)

        if tool_name in _EDIT_TOOLS:
            old_string: str = tool_input.get("old_string", "")
            new_string: str = tool_input.get("new_string", "")
            return self._enforcement_engine.evaluate_edit(file_path, old_string, new_string)

        return None
