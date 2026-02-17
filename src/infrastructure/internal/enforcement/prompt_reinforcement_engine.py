# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
Prompt Reinforcement Engine for L2 Per-Prompt Re-injection.

Implements the L2 enforcement layer by extracting critical quality rules
from quality-enforcement.md (the SSOT) and assembling a token-budgeted
reinforcement preamble that is injected into every user prompt via the
UserPromptSubmit hook.

The engine parses HTML comment markers with the ``L2-REINJECT`` tag,
sorts them by rank, and assembles content within a 600-token budget.
It uses a conservative token estimation formula (chars/4 * 0.83).

The engine is fail-open by design: any internal error results in an
empty reinforcement rather than blocking user interaction.

References:
    - EN-705: L2 Per-Prompt Reinforcement Hook
    - ADR-EPIC002-002: 5-layer enforcement architecture
    - quality-enforcement.md: L2-REINJECT markers
"""

from __future__ import annotations

import re
from pathlib import Path

from src.infrastructure.internal.enforcement.reinforcement_content import (
    ReinforcementContent,
)

# Token budget for L2 reinforcement per prompt
_DEFAULT_TOKEN_BUDGET = 600

# Calibration factor for token estimation: chars/4 * factor
_TOKEN_CALIBRATION_FACTOR = 0.83


class PromptReinforcementEngine:
    """Engine for generating L2 per-prompt quality reinforcement.

    Reads L2-REINJECT markers from quality-enforcement.md, sorts by rank,
    and assembles a reinforcement preamble within the token budget.

    The engine is fail-open: if the rules file is missing, empty, or
    contains malformed markers, it returns an empty reinforcement rather
    than raising an error.

    Args:
        rules_path: Path to quality-enforcement.md. If None, auto-detected
            by searching for .context/rules/quality-enforcement.md relative
            to the project root (found by searching for CLAUDE.md).
        token_budget: Maximum token budget for the reinforcement preamble.
            Defaults to 600.
    """

    def __init__(
        self,
        rules_path: Path | None = None,
        token_budget: int = _DEFAULT_TOKEN_BUDGET,
    ) -> None:
        """Initialize the prompt reinforcement engine.

        Args:
            rules_path: Path to quality-enforcement.md. If None, auto-detected.
            token_budget: Maximum token budget for the reinforcement preamble.
        """
        self._rules_path = rules_path or self._find_rules_path()
        self._token_budget = token_budget

    def generate_reinforcement(self) -> ReinforcementContent:
        """Generate the reinforcement preamble from L2-REINJECT markers.

        Reads the quality-enforcement.md file, extracts L2-REINJECT markers,
        sorts them by rank (ascending), and assembles content within the
        token budget.

        Returns:
            ReinforcementContent with the assembled preamble and metadata.
            On any error, returns an empty ReinforcementContent (fail-open).
        """
        try:
            content = self._read_rules_file()
            if not content:
                return ReinforcementContent(
                    preamble="",
                    token_estimate=0,
                    items_included=0,
                    items_total=0,
                )

            markers = self._parse_reinject_markers(content)
            if not markers:
                return ReinforcementContent(
                    preamble="",
                    token_estimate=0,
                    items_included=0,
                    items_total=0,
                )

            return self._assemble_preamble(markers)

        except Exception:
            # Fail-open: any error returns empty reinforcement
            return ReinforcementContent(
                preamble="",
                token_estimate=0,
                items_included=0,
                items_total=0,
            )

    @staticmethod
    def _parse_reinject_markers(content: str) -> list[dict[str, str | int]]:
        """Parse L2-REINJECT HTML comment markers from file content.

        Extracts markers matching the pattern:
            <!-- L2-REINJECT: rank=N, tokens=M, content="..." -->

        Note:
            The ``tokens`` metadata field is parsed for completeness and
            potential future use (e.g., pre-computed budgets), but the engine
            does NOT use it for budget decisions. Instead, the engine computes
            its own estimate via ``_estimate_tokens()`` to ensure consistency
            regardless of marker metadata accuracy.

        Args:
            content: The full text content of quality-enforcement.md.

        Returns:
            List of dicts with keys: rank (int), tokens (int), content (str).
            Sorted by rank ascending. Malformed markers are silently skipped.
        """
        pattern = (
            r"<!--\s*L2-REINJECT:\s*"
            r"rank=(\d+)\s*,\s*"
            r"tokens=(\d+)\s*,\s*"
            r'content="([^"]*?)"\s*'
            r"-->"
        )

        markers: list[dict[str, str | int]] = []
        for match in re.finditer(pattern, content):
            try:
                markers.append(
                    {
                        "rank": int(match.group(1)),
                        "tokens": int(match.group(2)),
                        "content": match.group(3),
                    }
                )
            except (ValueError, IndexError):
                # Skip malformed markers
                continue

        # Sort by rank ascending (lower rank = higher priority)
        markers.sort(key=lambda m: m["rank"])
        return markers

    @staticmethod
    def _estimate_tokens(text: str) -> int:
        """Estimate token count using calibrated character-based formula.

        Uses the formula: ceil(len(text) / 4 * 0.83) which provides a
        conservative estimate for English text with technical content.

        Args:
            text: The text to estimate tokens for.

        Returns:
            Estimated token count as an integer. Returns 0 for empty text.
        """
        if not text:
            return 0
        raw = len(text) / 4.0 * _TOKEN_CALIBRATION_FACTOR
        # Round up to be conservative
        return int(raw) + (1 if raw != int(raw) else 0)

    def _assemble_preamble(self, markers: list[dict[str, str | int]]) -> ReinforcementContent:
        """Assemble the reinforcement preamble within the token budget.

        Adds markers in rank order until the budget is exhausted.

        Args:
            markers: Sorted list of L2-REINJECT marker dicts.

        Returns:
            ReinforcementContent with the assembled preamble.
        """
        items: list[str] = []
        running_tokens = 0
        items_included = 0

        for marker in markers:
            marker_content = str(marker["content"])
            marker_tokens = self._estimate_tokens(marker_content)

            if running_tokens + marker_tokens > self._token_budget:
                # Budget exhausted; stop adding items
                break

            items.append(marker_content)
            running_tokens += marker_tokens
            items_included += 1

        preamble = " ".join(items) if items else ""
        actual_tokens = self._estimate_tokens(preamble)

        return ReinforcementContent(
            preamble=preamble,
            token_estimate=actual_tokens,
            items_included=items_included,
            items_total=len(markers),
        )

    def _read_rules_file(self) -> str:
        """Read the quality-enforcement.md file content.

        Returns:
            File content as a string. Empty string if file not found or
            unreadable.
        """
        try:
            if self._rules_path and self._rules_path.is_file():
                return self._rules_path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            pass
        return ""

    def _find_rules_path(self) -> Path:
        """Find quality-enforcement.md by searching for the project root.

        Walks upward from CWD looking for CLAUDE.md, then constructs the
        path to .context/rules/quality-enforcement.md.

        Returns:
            Path to quality-enforcement.md (may not exist).
        """
        current = Path.cwd()
        for parent in [current, *current.parents]:
            if (parent / "CLAUDE.md").exists():
                return parent / ".context" / "rules" / "quality-enforcement.md"
        # Fallback to CWD-relative path
        return current / ".context" / "rules" / "quality-enforcement.md"
