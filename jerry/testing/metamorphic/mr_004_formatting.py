# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Victor Lau

"""MR-004: Formatting Perturbation metamorphic relation.

Definition (behavioral-contracts.md Section C.4):
    Changing the formatting of the prompt (converting markdown to plain text,
    changing list styles, removing code block delimiters, converting tables to
    prose) should not change output quality by more than the tolerance (0.05).

Tolerance: 0.05 (max |score_original - score_formatted|)
Violation condition: Wilcoxon p < 0.05 AND mean_delta > 0.05 (both required)
Effect size threshold: Cohen's r >= 0.30 (medium effect)
Minimum sample size: 20 pairs (ADR-001 FM-002)

The tolerance (0.05) matches MR-001 because formatting perturbation is a
comparable surface-level change to paraphrasing; however formatting changes
can subtly affect LLM tokenisation and attention patterns.

Statistical helper: uses ``_wilcoxon_p_and_effect`` from ``mr_001_paraphrase``;
changes to that function affect this module's evaluate() method.

Domain isolation: MUST NOT import DeepEval, promptfoo, or any adapter (H-07).
One class per file (H-10): FormattingVariant enum is in formatting_variant.py;
this file contains only FormattingPerturbation.
"""

from __future__ import annotations

import re
from collections.abc import Sequence

from jerry.testing.metamorphic.base import (
    MetamorphicRelation,
    MRResult,
    MRViolationSeverity,
)
from jerry.testing.metamorphic.formatting_variant import FormattingVariant
from jerry.testing.metamorphic.mr_001_paraphrase import _wilcoxon_p_and_effect


class FormattingPerturbation(MetamorphicRelation):
    """MR-004: Formatting Perturbation.

    Tests that reformatting the prompt (markdown to plain text, list style
    changes, code block removal, table to prose) does not change output
    quality by more than the tolerance threshold.

    A violation indicates the agent's output quality is over-fitted to a
    specific prompt format -- a generalisation deficiency.

    Per contracts Section C.4: the structural invariants from Section A
    (e.g., SI-ARCH-001 through SI-ARCH-010) must still pass regardless of
    input formatting.  Format perturbation tests output quality robustness;
    structural invariants test output format compliance.  Both are evaluated
    independently.

    Tolerance values (from behavioral-contracts.md C.4):
        max_delta        = 0.05  (absolute mean score delta)
        p_alpha          = 0.05  (Wilcoxon significance level)
        effect_r_min     = 0.30  (Cohen's r; medium effect)

    Violation condition (both must be true):
        1. Wilcoxon signed-rank p < 0.05
        2. Mean absolute delta > 0.05
    """

    mr_id: str = "MR-004"
    mr_name: str = "Formatting Perturbation"
    minimum_sample_size: int = 20

    # Contracts C.4 parameters
    TOLERANCE: float = 0.05
    P_ALPHA: float = 0.05
    EFFECT_R_THRESHOLD: float = 0.30

    def __init__(
        self,
        variant: FormattingVariant = FormattingVariant.MARKDOWN_TO_PLAIN,
    ) -> None:
        """Initialise with a specific formatting transformation variant.

        Args:
            variant: Which formatting transformation to apply.  Defaults to
                ``MARKDOWN_TO_PLAIN`` (the most comprehensive transformation
                and most commonly used in regression test suites).
        """
        self._variant = variant

    @property
    def variant(self) -> FormattingVariant:
        """The active formatting transformation variant."""
        return self._variant

    def transform(self, input_text: str) -> str:
        """Apply the configured formatting transformation to the input text.

        All transformations are deterministic and require no external services.
        The semantic content of the input is preserved; only surface formatting
        changes.

        Variant behaviours:
            MARKDOWN_TO_PLAIN:
                - Converts ``## Heading`` and ``# Heading`` to ``Heading:``
                - Converts ``**bold**`` and ``*italic*`` to plain text
                - Converts ``---`` horizontal rules to blank lines
                - Converts ``[link text](url)`` to ``link text (url)``
            BULLETS_TO_NUMBERED:
                - Converts ``- item`` and ``* item`` lists to ``1. item`` etc.
                - Preserves list structure and indentation depth
            REMOVE_CODE_BLOCKS:
                - Strips ``` fenced code block delimiters (keeps content)
                - Strips inline ``code`` backtick formatting
            TABLES_TO_PROSE:
                - Converts markdown ``|`` tables to prose descriptions
                - Each table row becomes a sentence

        Args:
            input_text: The original prompt or user message text.

        Returns:
            Formatted variant of the prompt with equivalent semantic content.

        Raises:
            ValueError: If ``input_text`` is empty.
        """
        if not input_text or not input_text.strip():
            raise ValueError(
                f"{self.mr_id}: input_text must be non-empty for formatting transform."
            )

        dispatch = {
            FormattingVariant.MARKDOWN_TO_PLAIN: _to_plain_text,
            FormattingVariant.BULLETS_TO_NUMBERED: _bullets_to_numbered,
            FormattingVariant.REMOVE_CODE_BLOCKS: _remove_code_blocks,
            FormattingVariant.TABLES_TO_PROSE: _tables_to_prose,
        }
        transform_fn = dispatch[self._variant]
        return transform_fn(input_text)

    def evaluate(
        self,
        original_scores: Sequence[float],
        transformed_scores: Sequence[float],
    ) -> MRResult:
        """Evaluate formatting robustness across paired score sequences.

        Applies the dual-condition violation check from contracts C.4:
        1. Wilcoxon signed-rank p < 0.05
        2. Mean absolute delta > TOLERANCE (0.05)

        Args:
            original_scores: Quality scores from N original-prompt runs.
            transformed_scores: Quality scores from N reformatted-prompt runs.

        Returns:
            ``MRResult`` with verdict, delta, effect size, p-value, and evidence.

        Raises:
            InsufficientSamplesError: If len(original_scores) < 20.
            ValueError: Mismatched lengths or out-of-range scores.
        """
        self._validate_inputs(original_scores, transformed_scores)

        n = len(original_scores)
        mean_orig = self._mean(original_scores)
        mean_trans = self._mean(transformed_scores)
        mean_delta = abs(mean_orig - mean_trans)

        p_value, effect_r = _wilcoxon_p_and_effect(
            list(original_scores), list(transformed_scores), n
        )

        statistically_significant = p_value < self.P_ALPHA
        practically_significant = mean_delta > self.TOLERANCE
        violated = statistically_significant and practically_significant

        if violated:
            severity = MRViolationSeverity.REGRESSION
            passed = False
            evidence = (
                f"MR-004 VIOLATED: formatting variant '{self._variant.value}' "
                f"changed quality by {mean_delta:.4f} "
                f"(tolerance {self.TOLERANCE}). "
                f"Agent output quality is over-fitted to a specific prompt format. "
                f"Wilcoxon p={p_value:.4f} (alpha {self.P_ALPHA}), "
                f"Cohen's r={effect_r:.3f} (threshold {self.EFFECT_R_THRESHOLD}). "
                f"mean_original={mean_orig:.4f}, mean_reformatted={mean_trans:.4f}, N={n}."
            )
        else:
            severity = MRViolationSeverity.PASS
            passed = True
            reason_parts: list[str] = []
            if not statistically_significant:
                reason_parts.append(
                    f"Wilcoxon p={p_value:.4f} >= alpha {self.P_ALPHA} (not significant)"
                )
            if not practically_significant:
                reason_parts.append(f"mean_delta={mean_delta:.4f} <= tolerance {self.TOLERANCE}")
            evidence = (
                f"MR-004 PASSED: formatting variant '{self._variant.value}' "
                "has no significant quality impact. " + "; ".join(reason_parts) + ". "
                f"Cohen's r={effect_r:.3f}, N={n}. "
                f"mean_original={mean_orig:.4f}, mean_reformatted={mean_trans:.4f}."
            )

        return MRResult(
            mr_id=self.mr_id,
            mr_name=self.mr_name,
            passed=passed,
            original_scores=tuple(original_scores),
            transformed_scores=tuple(transformed_scores),
            mean_original=mean_orig,
            mean_transformed=mean_trans,
            mean_delta=mean_delta,
            tolerance=self.TOLERANCE,
            effect_size=effect_r,
            p_value=p_value,
            severity=severity,
            evidence=evidence,
        )


# ---------------------------------------------------------------------------
# Formatting transformation functions (module-private)
# ---------------------------------------------------------------------------


def _to_plain_text(text: str) -> str:
    """Convert markdown formatting to plain text.

    Handles headings, bold/italic, horizontal rules, and hyperlinks.

    Args:
        text: Markdown-formatted input text.

    Returns:
        Plain text equivalent with semantic content preserved.
    """
    # Convert ATX headings (## Heading, # Heading) -> "Heading:"
    result = re.sub(r"^#{1,6}\s+(.+)$", r"\1:", text, flags=re.MULTILINE)
    # Remove bold/italic markers
    result = re.sub(r"\*{1,3}(.+?)\*{1,3}", r"\1", result)
    result = re.sub(r"_{1,3}(.+?)_{1,3}", r"\1", result)
    # Convert [link text](url) -> "link text (url)"
    result = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r"\1 (\2)", result)
    # Remove horizontal rules
    result = re.sub(r"^-{3,}$", "", result, flags=re.MULTILINE)
    result = re.sub(r"^\*{3,}$", "", result, flags=re.MULTILINE)
    # Collapse multiple blank lines to at most two
    result = re.sub(r"\n{3,}", "\n\n", result)
    return result.strip()


def _bullets_to_numbered(text: str) -> str:
    """Convert unordered list markers to ordered list numbers.

    Processes each line that starts with ``- `` or ``* `` and replaces the
    marker with a sequential number.  Nested list indentation is preserved;
    numbering restarts at 1 for each indentation level.

    Args:
        text: Text that may contain markdown unordered lists.

    Returns:
        Text with bullet markers replaced by sequential numbers.
    """
    lines = text.split("\n")
    counters: dict[int, int] = {}
    result_lines: list[str] = []

    for line in lines:
        match = re.match(r"^(\s*)([-*])\s+(.+)$", line)
        if match:
            indent_str = match.group(1)
            indent_level = len(indent_str) // 2
            item_text = match.group(3)
            counters[indent_level] = counters.get(indent_level, 0) + 1
            # Reset deeper levels when we step back up
            for deeper in list(counters.keys()):
                if deeper > indent_level:
                    del counters[deeper]
            number = counters[indent_level]
            result_lines.append(f"{indent_str}{number}. {item_text}")
        else:
            # Non-list line; reset all counters
            counters.clear()
            result_lines.append(line)

    return "\n".join(result_lines)


def _remove_code_blocks(text: str) -> str:
    """Remove fenced code block delimiters and inline code backticks.

    Preserves the code content while removing the markdown formatting syntax.
    The intent is to test whether the agent's output quality depends on
    seeing code formatted as code blocks versus plain text.

    Args:
        text: Text that may contain markdown code fences and inline code spans.

    Returns:
        Text with code delimiters removed; code content preserved.
    """
    # Remove fenced code blocks: ```language\ncontent\n``` -> content
    result = re.sub(
        r"```[^\n]*\n(.*?)\n```",
        r"\1",
        text,
        flags=re.DOTALL,
    )
    # Also handle triple-backtick without language tag
    result = re.sub(r"```(.*?)```", r"\1", result, flags=re.DOTALL)
    # Remove inline code backticks: `code` -> code
    result = re.sub(r"`([^`]+)`", r"\1", result)
    return result


def _tables_to_prose(text: str) -> str:
    """Convert markdown table blocks to prose descriptions.

    Parses each ``|``-delimited table block and emits a prose sentence per
    data row using the column headers as field names.

    Limitations: handles simple, single-header-row tables.  Multi-header or
    complex merged cell tables are passed through unchanged.

    Args:
        text: Text that may contain markdown tables.

    Returns:
        Text with markdown tables replaced by prose equivalents.
    """
    lines = text.split("\n")
    result_lines: list[str] = []
    i = 0

    while i < len(lines):
        line = lines[i]
        # Detect a table header row: starts and ends with |
        if re.match(r"^\|.+\|$", line.strip()):
            # Collect the full table block
            table_lines: list[str] = [line]
            j = i + 1
            while j < len(lines) and re.match(r"^\|", lines[j].strip()):
                table_lines.append(lines[j])
                j += 1

            prose = _table_block_to_prose(table_lines)
            result_lines.extend(prose.split("\n"))
            i = j
        else:
            result_lines.append(line)
            i += 1

    return "\n".join(result_lines)


def _table_block_to_prose(table_lines: list[str]) -> str:
    """Convert a list of table lines (header + separator + rows) to prose.

    Args:
        table_lines: Lines forming one complete markdown table.

    Returns:
        Prose description of the table data.
    """
    if len(table_lines) < 3:  # Must have header, separator, at least one row
        return "\n".join(table_lines)

    def _parse_row(row: str) -> list[str]:
        """Split a table row by ``|`` and strip cell content."""
        return [cell.strip() for cell in row.strip("|").split("|")]

    headers = _parse_row(table_lines[0])
    separator = table_lines[1]

    # Validate separator row (contains only |, -, :, and spaces)
    if not re.match(r"^[\|\-\:\s]+$", separator):
        return "\n".join(table_lines)

    data_rows = table_lines[2:]
    sentences: list[str] = []

    for row_line in data_rows:
        cells = _parse_row(row_line)
        if len(cells) != len(headers):
            continue
        pairs = [f"{h}: {c}" for h, c in zip(headers, cells, strict=False) if h and c]
        if pairs:
            sentences.append(". ".join(pairs) + ".")

    return " ".join(sentences) if sentences else "\n".join(table_lines)
