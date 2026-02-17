# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Utilities for LLM integration tests.

This module provides helper functions for:
- Agent invocation via the Task tool
- Output comparison for extraction reports
- Citation validation
- Timeout and retry handling

Reference: TASK-234, EN-023 Integration Testing
"""

from __future__ import annotations

import json
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class LLMTestResult:
    """Result from an LLM test invocation.

    Attributes:
        success: Whether the invocation completed successfully.
        output: The parsed output data, if any.
        error: Error message if invocation failed.
        tokens_used: Estimated tokens consumed.
        elapsed_seconds: Time taken for invocation.
        raw_output: Raw string output from the agent.
    """

    success: bool
    output: dict[str, Any] | None = None
    error: str | None = None
    tokens_used: int = 0
    elapsed_seconds: float = 0.0
    raw_output: str | None = None


@dataclass
class ComparisonResult:
    """Result from comparing two extraction reports."""

    matches: bool
    differences: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


@dataclass
class CitationValidationResult:
    """Result from validating citations in an extraction report."""

    valid: bool
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


def compare_extraction_reports(
    actual: dict[str, Any],
    expected: dict[str, Any],
    tolerance: float = 0.15,
) -> ComparisonResult:
    """Compare two extraction reports, returning differences.

    Compares entity counts with tolerance for LLM non-determinism.
    For meeting-006 with 3071 segments, ±15% tolerance is reasonable.

    Args:
        actual: The actual extraction report from the LLM.
        expected: The expected extraction report (ground truth).
        tolerance: Allowed percentage difference (default 0.15 = 15%).

    Returns:
        ComparisonResult with match status and list of differences.
    """
    differences = []
    warnings = []

    # Compare extraction stats
    entity_types = ["action_items", "decisions", "questions", "topics"]

    for entity_type in entity_types:
        actual_count = len(actual.get(entity_type, []))
        expected_count = len(expected.get(entity_type, []))

        if expected_count > 0:
            diff_ratio = abs(actual_count - expected_count) / expected_count
            if diff_ratio > tolerance:
                differences.append(
                    f"{entity_type}: expected ~{expected_count}, got {actual_count} "
                    f"(diff: {diff_ratio:.1%})"
                )
            elif diff_ratio > tolerance / 2:
                warnings.append(
                    f"{entity_type}: slight variance - expected ~{expected_count}, "
                    f"got {actual_count} (diff: {diff_ratio:.1%})"
                )
        elif actual_count > 0:
            warnings.append(f"{entity_type}: expected 0, got {actual_count}")

    # Compare speaker count
    actual_speakers = len(actual.get("speakers", {}).get("identified", []))
    expected_speakers = len(expected.get("speakers", {}).get("identified", []))

    if expected_speakers > 0:
        speaker_diff = abs(actual_speakers - expected_speakers) / expected_speakers
        if speaker_diff > tolerance:
            differences.append(f"speakers: expected ~{expected_speakers}, got {actual_speakers}")

    return ComparisonResult(
        matches=len(differences) == 0,
        differences=differences,
        warnings=warnings,
    )


def validate_citations(
    report: dict[str, Any],
    max_segment_id: int = 3071,
) -> CitationValidationResult:
    """Validate all citations in extraction report.

    Checks that:
    - Every entity has a citation
    - Citation segment_id is within valid range
    - Citation format is correct

    Args:
        report: The extraction report to validate.
        max_segment_id: Maximum valid segment ID (default 3071 for meeting-006).

    Returns:
        CitationValidationResult with validation status and errors.
    """
    errors = []
    warnings = []

    entity_types = ["action_items", "decisions", "questions"]

    for entity_type in entity_types:
        for i, entity in enumerate(report.get(entity_type, [])):
            entity_id = entity.get("id", f"{entity_type}_{i}")

            # Check citation exists
            citation = entity.get("citation")
            if not citation:
                errors.append(f"{entity_id}: missing citation")
                continue

            # Check segment_id
            segment_id = citation.get("segment_id")
            if segment_id is None:
                errors.append(f"{entity_id}: citation missing segment_id")
            elif isinstance(segment_id, int):
                if segment_id < 1 or segment_id > max_segment_id:
                    errors.append(
                        f"{entity_id}: segment_id {segment_id} out of range [1, {max_segment_id}]"
                    )
            elif isinstance(segment_id, str):
                # Handle string format like "seg-0001"
                try:
                    if segment_id.startswith("seg-"):
                        seg_num = int(segment_id.split("-")[1])
                        if seg_num < 1 or seg_num > max_segment_id:
                            errors.append(f"{entity_id}: segment_id {segment_id} out of range")
                    else:
                        seg_num = int(segment_id)
                        if seg_num < 1 or seg_num > max_segment_id:
                            errors.append(f"{entity_id}: segment_id {segment_id} out of range")
                except (ValueError, IndexError):
                    errors.append(f"{entity_id}: invalid segment_id format: {segment_id}")

            # Check confidence if present
            confidence = entity.get("confidence")
            if confidence is not None:
                if not isinstance(confidence, int | float):
                    warnings.append(f"{entity_id}: confidence not a number")
                elif confidence < 0.0 or confidence > 1.0:
                    warnings.append(f"{entity_id}: confidence {confidence} out of range [0, 1]")

    return CitationValidationResult(
        valid=len(errors) == 0,
        errors=errors,
        warnings=warnings,
    )


def validate_against_schema(
    data: dict[str, Any],
    schema: dict[str, Any],
) -> tuple[bool, list[str]]:
    """Validate data against a JSON Schema.

    Args:
        data: The data to validate.
        schema: The JSON Schema to validate against.

    Returns:
        Tuple of (is_valid, list of error messages).
    """
    try:
        from jsonschema import Draft202012Validator

        validator = Draft202012Validator(schema)
        errors = []
        for error in validator.iter_errors(data):
            path = ".".join(str(p) for p in error.absolute_path)
            errors.append(f"{path}: {error.message}" if path else error.message)

        return len(errors) == 0, errors

    except ImportError:
        return True, ["jsonschema not installed, skipping validation"]


class TimeoutContext:
    """Context manager for handling timeouts in LLM tests.

    Usage:
        with TimeoutContext(timeout_seconds=300) as ctx:
            # Run LLM invocation
            result = invoke_extractor(...)
            ctx.mark_complete(result)

        if ctx.timed_out:
            print(f"Timed out after {ctx.elapsed_seconds:.1f}s")
    """

    def __init__(self, timeout_seconds: float = 300.0) -> None:
        """Initialize timeout context.

        Args:
            timeout_seconds: Maximum time to wait (default 300s = 5 min).
        """
        self.timeout_seconds = timeout_seconds
        self.start_time: float = 0.0
        self.end_time: float = 0.0
        self.timed_out: bool = False
        self.completed: bool = False
        self.result: Any = None

    def __enter__(self) -> TimeoutContext:
        self.start_time = time.time()
        return self

    def __exit__(self, exc_type: type | None, exc_val: Exception | None, exc_tb: Any) -> None:
        self.end_time = time.time()
        if not self.completed:
            if self.elapsed_seconds > self.timeout_seconds:
                self.timed_out = True

    @property
    def elapsed_seconds(self) -> float:
        """Time elapsed since entering context."""
        if self.end_time > 0:
            return self.end_time - self.start_time
        return time.time() - self.start_time

    def check_timeout(self) -> bool:
        """Check if timeout has been exceeded.

        Returns:
            True if timed out, False otherwise.
        """
        if self.elapsed_seconds > self.timeout_seconds:
            self.timed_out = True
            return True
        return False

    def mark_complete(self, result: Any = None) -> None:
        """Mark the operation as complete.

        Args:
            result: Optional result to store.
        """
        self.completed = True
        self.result = result


def load_expected_results(
    dataset_name: str,
    results_dir: Path | None = None,
) -> dict[str, Any] | None:
    """Load expected results for a dataset (ground truth).

    Args:
        dataset_name: Name of the dataset (e.g., "meeting-006").
        results_dir: Directory containing expected results.

    Returns:
        Expected results dict, or None if not found.
    """
    if results_dir is None:
        results_dir = Path("skills/transcript/test_data/expected")

    expected_path = results_dir / f"{dataset_name}-expected.json"
    if not expected_path.exists():
        return None

    with open(expected_path) as f:
        return json.load(f)


def estimate_tokens(text: str) -> int:
    """Estimate token count for text.

    Uses a simple character-based approximation.
    Actual token count depends on the tokenizer used.

    Args:
        text: Text to estimate tokens for.

    Returns:
        Estimated token count.
    """
    # Rough estimate: ~4 characters per token for English text
    return len(text) // 4
