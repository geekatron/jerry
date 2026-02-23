# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""ReDoS safety test suite for schema value_pattern regexes (WI-023).

Validates that all ``value_pattern`` regexes in registered schemas are safe
from catastrophic backtracking (CWE-1333). Tests adversarial inputs against
each pattern with a timeout.

Security constraint: M-12 (ReDoS-safe regex patterns).

References:
    - ADR-PROJ005-003 Threat Model: T-SV-03 (CWE-1333)
    - H-20: BDD test-first
"""

from __future__ import annotations

import re
import signal
import sys
import time

import pytest

from src.domain.markdown_ast.schema_definitions import DEFAULT_REGISTRY


def _timeout_handler(signum: int, frame: object) -> None:
    """Signal handler for ReDoS timeout detection."""
    raise TimeoutError("Regex took too long -- possible ReDoS")


def _run_pattern_with_timeout(
    pattern: str, adversarial_input: str, timeout_seconds: float = 2.0
) -> float:
    """Run a regex pattern against input with a timeout.

    Args:
        pattern: The regex pattern string.
        adversarial_input: Input designed to trigger backtracking.
        timeout_seconds: Maximum allowed time.

    Returns:
        Elapsed time in seconds.

    Raises:
        TimeoutError: If pattern execution exceeds timeout.
    """
    compiled = re.compile(pattern)

    if sys.platform != "win32":
        old_handler = signal.signal(signal.SIGALRM, _timeout_handler)
        signal.alarm(int(timeout_seconds) + 1)
        try:
            start = time.monotonic()
            compiled.search(adversarial_input)
            elapsed = time.monotonic() - start
            return elapsed
        finally:
            signal.alarm(0)
            signal.signal(signal.SIGALRM, old_handler)
    else:
        # Windows fallback: just time it
        start = time.monotonic()
        compiled.search(adversarial_input)
        elapsed = time.monotonic() - start
        if elapsed > timeout_seconds:
            raise TimeoutError(f"Regex took {elapsed:.2f}s -- possible ReDoS")
        return elapsed


# =============================================================================
# Adversarial Input Generators
# =============================================================================

ADVERSARIAL_INPUTS = [
    "a" * 10_000,                    # Repeated single char
    "ab" * 5_000,                    # Repeated pair
    " " * 10_000,                    # Whitespace flood
    "a" * 5_000 + "!" + "a" * 5_000, # Char in middle
    "a-b-c-" * 2_000,               # Repeated with separators
    "1.2.3." * 2_000,               # Repeated version-like
    "aaa" + "." * 10_000 + "bbb",   # Long alternation trigger
]


# =============================================================================
# Collected Pattern Tests
# =============================================================================


class TestValuePatternReDoSSafety:
    """Verify all value_pattern regexes complete quickly on adversarial input."""

    @pytest.mark.security
    def test_all_patterns_collected(self) -> None:
        """At least some schemas have value_pattern regexes."""
        patterns: list[tuple[str, str, str]] = []
        for schema_name in DEFAULT_REGISTRY.list_types():
            schema = DEFAULT_REGISTRY.get(schema_name)
            for rule in schema.field_rules:
                if rule.value_pattern:
                    patterns.append(
                        (schema_name, rule.key, rule.value_pattern)
                    )
        assert len(patterns) > 0, "Expected at least some value_pattern regexes"

    @pytest.mark.security
    @pytest.mark.parametrize("adversarial_input", ADVERSARIAL_INPUTS[:4])
    def test_patterns_complete_under_threshold(
        self, adversarial_input: str
    ) -> None:
        """All value_pattern regexes complete in < 2 seconds on adversarial input."""
        for schema_name in DEFAULT_REGISTRY.list_types():
            schema = DEFAULT_REGISTRY.get(schema_name)
            for rule in schema.field_rules:
                if rule.value_pattern:
                    elapsed = _run_pattern_with_timeout(
                        rule.value_pattern,
                        adversarial_input,
                        timeout_seconds=2.0,
                    )
                    assert elapsed < 2.0, (
                        f"ReDoS risk: pattern {rule.value_pattern!r} "
                        f"for {schema_name}.{rule.key} took "
                        f"{elapsed:.2f}s on input of length "
                        f"{len(adversarial_input)}"
                    )


class TestInternalPatternSafety:
    """Verify internal regex patterns used by parsers are ReDoS-safe."""

    @pytest.mark.security
    def test_xml_section_pattern_safe(self) -> None:
        """XmlSectionParser's section pattern is safe on adversarial input."""
        from src.domain.markdown_ast.xml_section import _build_section_pattern, XmlSectionParser

        pattern = _build_section_pattern(XmlSectionParser.ALLOWED_TAGS)
        # Adversarial: many lines of near-matches
        adversarial = ("<identity>\n" + "x\n" * 5_000 + "</identity>\n")
        start = time.monotonic()
        list(pattern.finditer(adversarial))
        elapsed = time.monotonic() - start
        assert elapsed < 2.0, f"XML section pattern took {elapsed:.2f}s"

    @pytest.mark.security
    def test_html_comment_pattern_safe(self) -> None:
        """HtmlCommentMetadata's comment pattern is safe on adversarial input."""
        from src.domain.markdown_ast.html_comment import _METADATA_COMMENT_PATTERN

        adversarial = "<!-- " + "KEY: value | " * 2_000 + " -->\n"
        start = time.monotonic()
        list(_METADATA_COMMENT_PATTERN.finditer(adversarial))
        elapsed = time.monotonic() - start
        assert elapsed < 2.0, f"HTML comment pattern took {elapsed:.2f}s"

    @pytest.mark.security
    def test_control_char_pattern_safe(self) -> None:
        """Control character stripping pattern is safe on large input."""
        from src.domain.markdown_ast.xml_section import _CONTROL_CHAR_RE

        adversarial = "\x00" * 10_000 + "normal text" + "\x01" * 10_000
        start = time.monotonic()
        _CONTROL_CHAR_RE.sub("", adversarial)
        elapsed = time.monotonic() - start
        assert elapsed < 1.0, f"Control char pattern took {elapsed:.2f}s"
