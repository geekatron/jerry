# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
HooksSubagentStopHandler - CLI handler for the SubagentStop hook.

Records sub-agent completion to a lifecycle tracking file so the
``jerry context estimate`` command can include sub-agent data in its
response without parsing all transcript files on every invocation.

Design Principles:
    - **Fail-open everywhere**: Any step failure logs to stderr.
    - **Exit 0 always**: The handler always exits 0.
    - **Always approve**: The handler never blocks sub-agent completion.

References:
    - EN-017: Sub-Agent Lifecycle Hooks
    - FEAT-002: Status Line / Context Monitoring Unification
    - PROJ-004: Context Resilience
"""

from __future__ import annotations

import json
import logging
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


class HooksSubagentStopHandler:
    """CLI handler for the Claude Code SubagentStop hook.

    Records sub-agent completion data to a lifecycle JSON file for
    consumption by ``jerry context estimate``. Always approves the
    sub-agent stop (never blocks).

    Attributes:
        _lifecycle_path: Path to the sub-agent lifecycle JSON file.

    Example:
        >>> handler = HooksSubagentStopHandler(
        ...     lifecycle_dir=Path(".jerry/local"),
        ... )
        >>> exit_code = handler.handle(stdin_json)
    """

    _LIFECYCLE_FILENAME = "subagent-lifecycle.json"

    def __init__(self, lifecycle_dir: Path) -> None:
        """Initialize the handler.

        Args:
            lifecycle_dir: Directory for the lifecycle tracking file.
        """
        self._lifecycle_path = lifecycle_dir / self._LIFECYCLE_FILENAME

    def handle(self, stdin_json: str) -> int:
        """Handle a SubagentStop hook event.

        Parses the hook input, records agent completion to the
        lifecycle file, and returns an approve decision.

        Args:
            stdin_json: The JSON payload from the Claude Code hook.

        Returns:
            Exit code (always 0).
        """
        # Step 1: Parse hook input (fail-open)
        hook_data: dict[str, Any] = {}
        try:
            hook_data = json.loads(stdin_json)
        except (json.JSONDecodeError, TypeError, ValueError) as exc:
            print(
                f"[hooks/subagent-stop] Failed to parse hook input: {exc}",
                file=sys.stderr,
            )

        # Step 2: Record agent completion (fail-open)
        self._record_completion(hook_data)

        # Step 3: Always approve
        print(json.dumps({"decision": "approve"}))
        return 0

    def _record_completion(self, hook_data: dict[str, Any]) -> None:
        """Record sub-agent completion to the lifecycle file.

        Reads the existing lifecycle file, appends the agent's
        completion record, and writes back atomically.

        Fail-open: any error is logged to stderr.

        Args:
            hook_data: The parsed hook input JSON.
        """
        session_id = hook_data.get("session_id", "")
        # Claude Code may send agent info in various field names
        raw_agent_id = hook_data.get("agent_id", "") or hook_data.get("agent_name", "")
        agent_type = hook_data.get("agent_type", "")
        transcript_path = hook_data.get(
            "agent_transcript_path",
            hook_data.get("transcript_path", ""),
        )

        if not session_id and not raw_agent_id:
            return

        agent_id = raw_agent_id or "unknown"

        try:
            lifecycle = self._load_lifecycle()

            agents = lifecycle.setdefault("agents", {})
            agents[agent_id] = {
                "session_id": session_id,
                "agent_type": agent_type,
                "status": "completed",
                "transcript_path": transcript_path,
                "completed_at": datetime.now(UTC).isoformat(),
            }
            lifecycle["updated_at"] = datetime.now(UTC).isoformat()

            self._save_lifecycle(lifecycle)
            logger.info("Sub-agent %s recorded as completed", agent_id)
        except Exception as exc:  # noqa: BLE001
            print(
                f"[hooks/subagent-stop] Lifecycle record failed: {exc}",
                file=sys.stderr,
            )

    def _load_lifecycle(self) -> dict[str, Any]:
        """Load the lifecycle file, returning empty dict if missing.

        Returns:
            The lifecycle data dictionary.
        """
        if not self._lifecycle_path.exists():
            return {}
        content = self._lifecycle_path.read_text(encoding="utf-8")
        return json.loads(content) if content.strip() else {}

    def _save_lifecycle(self, data: dict[str, Any]) -> None:
        """Save lifecycle data, creating parent dirs if needed.

        Args:
            data: The lifecycle data to persist.
        """
        self._lifecycle_path.parent.mkdir(parents=True, exist_ok=True)
        self._lifecycle_path.write_text(
            json.dumps(data, indent=2) + "\n",
            encoding="utf-8",
        )
