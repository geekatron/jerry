# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
ContextEstimateHandler - CLI handler for ``jerry context estimate``.

Reads Claude Code status line JSON from stdin, extracts
``context_window.current_usage`` data, runs the domain estimation
pipeline, and outputs structured JSON to stdout.

Fail-open design (DEC-004 D-007): any parsing or domain error
produces degraded JSON output with safe defaults rather than
crashing. Always exits 0.

Output JSON structure:
    - ``context``: Domain-computed fill estimate (Jerry adds value)
    - ``compaction``: Compaction detection result
    - ``thresholds``: 5-tier threshold configuration
    - ``action``: Recommended rotation action
    - ``session``: Full passthrough of Claude Code's stdin JSON

References:
    - FEAT-002: Status Line / Context Monitoring Unification
    - EN-012: ``jerry context estimate`` CLI Command
    - DEC-004 D-007: Fail-open design
    - DEC-004 D-013: Full passthrough of Claude Code JSON
    - PROJ-004: Context Resilience
"""

from __future__ import annotations

import json
import logging
from typing import Any

from src.context_monitoring.application.ports.sub_agent_reader import ISubAgentReader
from src.context_monitoring.application.services.context_estimate_service import (
    ContextEstimateService,
)
from src.context_monitoring.application.services.estimate_result import EstimateResult
from src.context_monitoring.domain.value_objects.context_usage_input import (
    ContextUsageInput,
)
from src.context_monitoring.domain.value_objects.sub_agent_info import SubAgentInfo

logger = logging.getLogger(__name__)


class ContextEstimateHandler:
    """CLI handler for the ``jerry context estimate`` command.

    Reads Claude Code's status line JSON from stdin, runs the
    domain estimation pipeline, and outputs structured JSON.

    Fail-open: parsing errors produce degraded output with
    NOMINAL tier and safe defaults.

    Attributes:
        _service: Application service for context estimation.
        _sub_agent_reader: Optional reader for sub-agent data.

    Example:
        >>> handler = ContextEstimateHandler(service)
        >>> exit_code = handler.handle(stdin_json)
        >>> assert exit_code == 0
    """

    def __init__(
        self,
        service: ContextEstimateService,
        sub_agent_reader: ISubAgentReader | None = None,
    ) -> None:
        """Initialize with the estimation service.

        Args:
            service: Application service for context estimation.
            sub_agent_reader: Optional reader for sub-agent lifecycle
                and context usage data (EN-018).
        """
        self._service = service
        self._sub_agent_reader = sub_agent_reader

    def handle(self, stdin_json: str) -> int:
        """Handle the context estimate command.

        Parses stdin JSON, runs estimation pipeline, outputs JSON.
        Always returns 0 (fail-open).

        Args:
            stdin_json: Raw JSON string from Claude Code on stdin.

        Returns:
            Always 0.
        """
        raw_data = self._parse_stdin(stdin_json)
        if raw_data is None:
            result = self._service.estimate_degraded()
            self._output(result, session_passthrough={}, context_window_size=200_000)
            return 0

        usage = self._extract_usage(raw_data)
        context_window = raw_data.get("context_window", {})
        window_size = (
            int(context_window.get("context_window_size", 200_000))
            if isinstance(context_window, dict)
            else 200_000
        )

        if usage is None:
            result = self._service.estimate_degraded()
            self._output(result, session_passthrough=raw_data, context_window_size=window_size)
            return 0

        result = self._service.estimate(usage)
        self._output(result, session_passthrough=raw_data, context_window_size=window_size)
        return 0

    def _parse_stdin(self, stdin_json: str) -> dict[str, Any] | None:
        """Parse raw stdin JSON string.

        Args:
            stdin_json: Raw JSON from stdin.

        Returns:
            Parsed dict or None on failure.
        """
        if not stdin_json or not stdin_json.strip():
            logger.debug("Empty stdin — producing degraded estimate")
            return None
        try:
            data = json.loads(stdin_json)
            if not isinstance(data, dict):
                logger.warning("Stdin JSON is not a dict — degraded")
                return None
            return data
        except json.JSONDecodeError as exc:
            logger.warning("Invalid JSON on stdin: %s", exc)
            return None

    def _extract_usage(self, data: dict[str, Any]) -> ContextUsageInput | None:
        """Extract ContextUsageInput from Claude Code's JSON structure.

        Claude Code sends ``context_window.current_usage`` with token
        counts. The ``session_id`` is at the top level.

        Handles null ``current_usage`` (before first API call) by
        falling back to ``used_percentage`` if available.

        Args:
            data: Parsed Claude Code JSON dict.

        Returns:
            ContextUsageInput or None if extraction fails.
        """
        try:
            session_id = data.get("session_id", "")
            context_window = data.get("context_window", {})
            if not isinstance(context_window, dict):
                context_window = {}

            window_size = context_window.get("context_window_size", 200_000)
            current_usage = context_window.get("current_usage")

            # Pre-calculated percentages (can be null before first API call)
            used_pct = context_window.get("used_percentage")
            remaining_pct = context_window.get("remaining_percentage")

            if current_usage is None or not isinstance(current_usage, dict):
                # Before first API call — no token data yet
                return ContextUsageInput(
                    session_id=session_id,
                    input_tokens=0,
                    cache_creation_input_tokens=0,
                    cache_read_input_tokens=0,
                    context_window_size=int(window_size),
                    used_percentage=float(used_pct) if used_pct is not None else None,
                    remaining_percentage=(
                        float(remaining_pct) if remaining_pct is not None else None
                    ),
                )

            return ContextUsageInput(
                session_id=session_id,
                input_tokens=int(current_usage.get("input_tokens", 0)),
                cache_creation_input_tokens=int(
                    current_usage.get("cache_creation_input_tokens", 0)
                ),
                cache_read_input_tokens=int(current_usage.get("cache_read_input_tokens", 0)),
                context_window_size=int(window_size),
                used_percentage=float(used_pct) if used_pct is not None else None,
                remaining_percentage=(float(remaining_pct) if remaining_pct is not None else None),
            )
        except (TypeError, ValueError) as exc:
            logger.warning("Failed to extract usage from stdin: %s", exc)
            return None

    def _output(
        self,
        result: EstimateResult,
        session_passthrough: dict[str, Any],
        context_window_size: int,
    ) -> None:
        """Output structured JSON to stdout.

        Args:
            result: Estimation pipeline result.
            session_passthrough: Full Claude Code JSON for session block.
            context_window_size: Window size for sub-agent fill calculation.
        """
        output: dict[str, Any] = {
            "context": {
                "fill_percentage": result.estimate.fill_percentage,
                "tier": result.estimate.tier.value,
                "used_tokens": result.estimate.used_tokens,
                "window_size": result.estimate.window_size,
                "is_estimated": result.estimate.is_estimated,
                "fresh_tokens": result.estimate.fresh_tokens,
                "cached_tokens": result.estimate.cached_tokens,
                "cache_creation_tokens": result.estimate.cache_creation_tokens,
            },
            "compaction": {
                "detected": result.compaction.detected,
                "from_tokens": result.compaction.from_tokens,
                "to_tokens": result.compaction.to_tokens,
                "session_id_changed": result.compaction.session_id_changed,
            },
            "thresholds": result.thresholds,
            "action": result.action.value,
            "sub_agents": self._read_sub_agents(context_window_size),
            "session": session_passthrough,
        }
        print(json.dumps(output))

    def _read_sub_agents(self, context_window_size: int) -> dict[str, Any]:
        """Read sub-agent data from lifecycle file and transcripts.

        Fail-open: returns empty data on any error.

        Args:
            context_window_size: Window size for fill percentage calculation.

        Returns:
            Dict with sub-agent summary and per-agent details.
        """
        if self._sub_agent_reader is None:
            return self._empty_sub_agents()

        try:
            agents = self._sub_agent_reader.read_sub_agents(context_window_size)
        except Exception as exc:  # noqa: BLE001
            logger.warning("Sub-agent reader failed: %s", exc)
            return self._empty_sub_agents()

        active = [a for a in agents if a.status == "active"]
        completed = [a for a in agents if a.status != "active"]

        return {
            "active_count": len(active),
            "completed_count": len(completed),
            "total_count": len(agents),
            "aggregate": {
                "total_context_tokens": sum(a.context_tokens for a in agents),
                "total_output_tokens": sum(a.output_tokens for a in agents),
            },
            "agents": [self._agent_to_dict(a) for a in agents],
        }

    @staticmethod
    def _agent_to_dict(agent: SubAgentInfo) -> dict[str, Any]:
        """Convert a SubAgentInfo to a JSON-serializable dict.

        Args:
            agent: Sub-agent info value object.

        Returns:
            Dict representation for JSON output.
        """
        return {
            "agent_id": agent.agent_id,
            "agent_type": agent.agent_type,
            "model": agent.model,
            "status": agent.status,
            "context_tokens": agent.context_tokens,
            "context_fill_pct": agent.context_fill_pct,
            "output_tokens": agent.output_tokens,
        }

    @staticmethod
    def _empty_sub_agents() -> dict[str, Any]:
        """Return empty sub-agent data structure.

        Returns:
            Dict with zero counts and empty agents list.
        """
        return {
            "active_count": 0,
            "completed_count": 0,
            "total_count": 0,
            "aggregate": {
                "total_context_tokens": 0,
                "total_output_tokens": 0,
            },
            "agents": [],
        }
