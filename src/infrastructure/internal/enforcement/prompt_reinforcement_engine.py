# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
Prompt Reinforcement Engine for L2 Per-Prompt Re-injection.

Implements the L2 enforcement layer by extracting critical quality rules
from all auto-loaded rule files and assembling a token-budgeted
reinforcement preamble that is injected into every user prompt via the
UserPromptSubmit hook.

The engine parses HTML comment markers with the ``L2-REINJECT`` tag from
all ``.md`` files in the ``.claude/rules/`` directory (or a single file
for backward compatibility), sorts them by rank, and assembles content
within an 850-token budget. It uses a conservative token estimation
formula (chars/4 * 0.83).

The engine is fail-open by design: any internal error results in an
empty reinforcement rather than blocking user interaction.

References:
    - EN-705: L2 Per-Prompt Reinforcement Hook
    - EN-002: HARD Rule Budget Enforcement Improvements (PROJ-007)
    - ADR-EPIC002-002: 5-layer enforcement architecture
    - All auto-loaded rule files: L2-REINJECT markers
"""

from __future__ import annotations

import re
from pathlib import Path

from src.infrastructure.internal.enforcement.reinforcement_content import (
    ReinforcementContent,
)

# Token budget for L2 reinforcement per prompt
# Updated from 600 to 850 to support markers from all auto-loaded rule files
# (EN-002: HARD Rule Budget Enforcement Improvements)
_DEFAULT_TOKEN_BUDGET = 850

# Calibration factor for token estimation: chars/4 * factor
_TOKEN_CALIBRATION_FACTOR = 0.83


class PromptReinforcementEngine:
    """Engine for generating L2 per-prompt quality reinforcement.

    Reads L2-REINJECT markers from all auto-loaded rule files, sorts by
    rank, and assembles a reinforcement preamble within the token budget.

    The engine is fail-open: if the rules path is missing, empty, or
    contains malformed markers, it returns an empty reinforcement rather
    than raising an error.

    Args:
        rules_path: Path to a rules file or directory. If a file, reads
            only that file (backward compatible). If a directory, reads
            all .md files in it. If None, auto-detected by searching for
            .claude/rules/ relative to the project root.
        token_budget: Maximum token budget for the reinforcement preamble.
            Defaults to 850.
    """

    def __init__(
        self,
        rules_path: Path | None = None,
        token_budget: int = _DEFAULT_TOKEN_BUDGET,
    ) -> None:
        """Initialize the prompt reinforcement engine.

        Args:
            rules_path: Path to a rules file or directory. If None,
                auto-detected to .claude/rules/ directory.
            token_budget: Maximum token budget for the reinforcement preamble.
        """
        self._rules_path = rules_path or self._find_rules_path()
        self._token_budget = token_budget

    def generate_reinforcement(self) -> ReinforcementContent:
        """Generate the reinforcement preamble from L2-REINJECT markers.

        Reads all auto-loaded rule files from the ``.claude/rules/``
        directory (or a single file for backward compatibility), extracts
        L2-REINJECT markers, sorts them by rank (ascending), and assembles
        content within the token budget.

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

    # Maximum allowed content length per marker (C-06: prevents budget exhaustion attacks)
    _MAX_MARKER_CONTENT_LENGTH = 500

    # Patterns that indicate injection attempts in marker content (C-06)
    _INJECTION_PATTERNS = re.compile(r"<!--|-->|<script|</script")

    @staticmethod
    def _parse_reinject_markers(content: str) -> list[dict[str, str | int]]:
        """Parse L2-REINJECT HTML comment markers from file content.

        Extracts markers matching either pattern:
            <!-- L2-REINJECT: rank=N, content="..." -->
            <!-- L2-REINJECT: rank=N, tokens=M, content="..." -->

        The ``tokens`` field is deprecated (EN-002 R4) and optional. When
        present it is parsed but ignored — the engine computes actual token
        counts at assembly time via ``_estimate_tokens``.

        Content is sanitized to prevent injection attacks (C-06):
        - Markers with content exceeding 500 characters are rejected
        - Markers containing HTML comment delimiters or script tags are rejected

        Note:
            The engine does NOT use declared token counts for budget decisions.
            computes its own estimate via ``_estimate_tokens()`` to ensure
            consistency regardless of marker metadata accuracy. The ``tokens``
            field is DEPRECATED and may be removed in a future version.

        Args:
            content: The combined text content of all rule files.

        Returns:
            List of dicts with keys: rank (int), content (str).
            Sorted by rank ascending. Malformed or suspicious markers are
            silently skipped.
        """
        pattern = (
            r"<!--\s*L2-REINJECT:\s*"
            r"rank=(\d+)\s*,\s*"
            r"(?:tokens=\d+\s*,\s*)?"
            r'content="([^"]*?)"\s*'
            r"-->"
        )

        markers: list[dict[str, str | int]] = []
        for match in re.finditer(pattern, content):
            try:
                marker_content = match.group(2)

                # C-06: Reject oversized content (prevents budget exhaustion)
                if len(marker_content) > PromptReinforcementEngine._MAX_MARKER_CONTENT_LENGTH:
                    continue

                # C-06: Reject content containing injection patterns
                if PromptReinforcementEngine._INJECTION_PATTERNS.search(marker_content):
                    continue

                markers.append(
                    {
                        "rank": int(match.group(1)),
                        "content": marker_content,
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
        """Read L2-REINJECT content from the rules path.

        If rules_path is a file, reads that single file.
        If rules_path is a directory, reads all .md files in it
        (sorted alphabetically for deterministic ordering).

        Returns:
            Combined file content as a string. Empty string if path
            not found, empty, or unreadable.
        """
        try:
            if not self._rules_path:
                return ""
            if self._rules_path.is_file():
                return self._rules_path.read_text(encoding="utf-8")
            if self._rules_path.is_dir():
                contents: list[str] = []
                for md_file in sorted(self._rules_path.glob("*.md")):
                    try:
                        contents.append(md_file.read_text(encoding="utf-8"))
                    except (OSError, UnicodeDecodeError):
                        continue
                return "\n".join(contents)
        except (OSError, UnicodeDecodeError):
            pass
        return ""

    def _find_rules_path(self) -> Path:
        """Find the rules directory by searching for the project root.

        Walks upward from CWD looking for CLAUDE.md, then returns the
        .claude/rules/ directory containing auto-loaded rule files.
        Falls back to the single quality-enforcement.md file if the
        directory does not exist.

        Returns:
            Path to .claude/rules/ directory or quality-enforcement.md
            (may not exist).
        """
        current = Path.cwd()
        for parent in [current, *current.parents]:
            if (parent / "CLAUDE.md").exists():
                rules_dir = parent / ".claude" / "rules"
                if rules_dir.is_dir():
                    return rules_dir
                return parent / ".context" / "rules" / "quality-enforcement.md"
        # Fallback to CWD-relative path
        return current / ".context" / "rules" / "quality-enforcement.md"
