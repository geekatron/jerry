# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
ResumptionContextGenerator - Application service for generating resumption XML.

This service generates a compact XML <resumption-context> block from a
CheckpointData instance. The block is designed to be injected into the
LLM context at the start of a new session to restore workflow state after
context compaction.

If the checkpoint has no resumption_state (None), an empty string is returned
and the block is omitted entirely. This keeps the output lean when there is
no state to resume.

Target output: ~760 token budget for the full block.

References:
    - EN-004: ContextFillEstimator and ResumptionContextGenerator
    - FEAT-002: Checkpoint Management
    - PROJ-004: Context Resilience
"""

from __future__ import annotations

import logging

from src.context_monitoring.domain.value_objects.checkpoint_data import CheckpointData

logger = logging.getLogger(__name__)


class ResumptionContextGenerator:
    """Application service for generating LLM resumption context XML.

    Converts a CheckpointData into a structured XML block suitable for
    injection into a Claude Code session context, providing the LLM with
    the information needed to resume interrupted work.

    The generated block targets a ~760 token budget and serialises the
    resumption_state dict as XML key-value pairs within a <recovery-state>
    section.

    Example:
        >>> generator = ResumptionContextGenerator()
        >>> xml = generator.generate(checkpoint)
        >>> # xml begins with <resumption-context> and ends with </resumption-context>
    """

    def generate(self, checkpoint: CheckpointData) -> str:
        """Generate a resumption context XML block from a checkpoint.

        If checkpoint.resumption_state is None, returns an empty string.
        Otherwise returns a compact XML block with checkpoint metadata
        and serialized recovery state.

        Args:
            checkpoint: The CheckpointData to render as resumption XML.

        Returns:
            XML string wrapped in <resumption-context> tags, or "" if
            checkpoint.resumption_state is None.

        Example:
            >>> xml = generator.generate(checkpoint)
            >>> xml.startswith("<resumption-context>")
            True
        """
        if checkpoint.resumption_state is None:
            return ""

        recovery_state_xml = self._serialize_recovery_state(checkpoint.resumption_state)
        fill_pct = checkpoint.context_state.fill_percentage
        tier_name = checkpoint.context_state.tier.name

        return (
            "<resumption-context>\n"
            f"  <checkpoint-id>{checkpoint.checkpoint_id}</checkpoint-id>\n"
            "  <context-state>\n"
            f"    <fill-percentage>{fill_pct:.4f}</fill-percentage>\n"
            f"    <tier>{tier_name}</tier>\n"
            "  </context-state>\n"
            "  <recovery-state>\n"
            f"{recovery_state_xml}"
            "  </recovery-state>\n"
            f"  <created-at>{checkpoint.created_at}</created-at>\n"
            "</resumption-context>"
        )

    def _serialize_recovery_state(self, state: dict) -> str:
        """Serialize a resumption state dict to indented XML key-value pairs.

        Each key-value pair in the dict is rendered as:
            <key>value</key>

        Nested structures are rendered using their str() representation.

        Args:
            state: The resumption state dictionary to serialize.

        Returns:
            XML lines as a single string, indented with 4 spaces.

        Example:
            >>> gen._serialize_recovery_state({"phase": "impl"})
            "    <phase>impl</phase>\\n"
        """
        lines: list[str] = []
        for key, value in state.items():
            safe_key = str(key).replace(" ", "_")
            lines.append(f"    <{safe_key}>{value}</{safe_key}>\n")
        return "".join(lines)
