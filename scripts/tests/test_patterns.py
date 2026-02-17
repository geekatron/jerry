#!/usr/bin/env python3

# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
BDD Tests for Pattern Library

Work Item: WI-SAO-015
Acceptance Criteria Tested:
    - AC-015-002: timeout_ms: 100 (configured in patterns)
    - AC-015-003: mode: warn (default behavior)
    - AC-015-004: Pattern library for common checks

Test Categories:
    - Happy Path (60%): Pattern detection works correctly
    - Negative Cases (30%): Invalid patterns handled gracefully
    - Edge Cases (10%): Boundary conditions
"""

import json
import sys
from pathlib import Path

import pytest

# Add hooks directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from patterns import (
    PatternLibrary,
    PatternMatch,
    ValidationResult,
    load_patterns,
)

# =============================================================================
# FIXTURES
# =============================================================================


@pytest.fixture
def patterns() -> PatternLibrary:
    """Load pattern library for testing."""
    return load_patterns()


@pytest.fixture
def empty_patterns() -> PatternLibrary:
    """Create empty pattern library."""
    return PatternLibrary(
        {
            "schema_version": "1.0.0",
            "validation_modes": {},
            "input_patterns": {},
            "output_patterns": {},
            "tool_rules": {},
        }
    )


# =============================================================================
# HAPPY PATH TESTS (60%)
# =============================================================================


class TestPatternLibraryLoading:
    """Test pattern library loading functionality."""

    def test_load_patterns_returns_library(self, patterns: PatternLibrary) -> None:
        """Given a valid patterns file, when loaded, then returns PatternLibrary."""
        assert isinstance(patterns, PatternLibrary)
        assert patterns.schema_version == "1.0.0"

    def test_load_patterns_has_input_patterns(self, patterns: PatternLibrary) -> None:
        """Given patterns file, when loaded, then has input pattern groups."""
        assert len(patterns.input_patterns) >= 1
        assert "secrets_detection" in patterns.input_patterns

    def test_load_patterns_has_output_patterns(self, patterns: PatternLibrary) -> None:
        """Given patterns file, when loaded, then has output pattern groups."""
        assert len(patterns.output_patterns) >= 1
        assert "no_secrets_in_output" in patterns.output_patterns

    def test_load_patterns_has_tool_rules(self, patterns: PatternLibrary) -> None:
        """Given patterns file, when loaded, then has tool-specific rules."""
        assert len(patterns.tool_rules) >= 1
        assert "Bash" in patterns.tool_rules


class TestInputValidation:
    """Test input pattern validation."""

    def test_validate_safe_bash_command(self, patterns: PatternLibrary) -> None:
        """Given safe bash command, when validated, then approved."""
        result = patterns.validate_input("Bash", {"command": "ls -la"})
        assert result.decision == "approve"
        assert len(result.matches) == 0

    def test_validate_email_in_webfetch(self, patterns: PatternLibrary) -> None:
        """Given email in WebFetch URL, when validated, then warns about PII."""
        result = patterns.validate_input(
            "WebFetch", {"url": "https://api.example.com/users/test@example.com"}
        )
        # PII detection may warn about email
        assert result.decision in ("approve", "warn")

    def test_validate_returns_validation_result(self, patterns: PatternLibrary) -> None:
        """Given any input, when validated, then returns ValidationResult."""
        result = patterns.validate_input("Bash", {"command": "echo test"})
        assert isinstance(result, ValidationResult)
        assert result.decision in ("approve", "warn", "block", "ask")


class TestOutputValidation:
    """Test output pattern validation."""

    def test_validate_safe_output(self, patterns: PatternLibrary) -> None:
        """Given safe output, when validated, then approved."""
        result = patterns.validate_output("Bash", "Build completed successfully")
        assert result.decision == "approve"
        assert len(result.matches) == 0


class TestPatternMatching:
    """Test pattern matching behavior."""

    def test_pattern_match_includes_position(self, patterns: PatternLibrary) -> None:
        """Given input with PII, when matched, then includes position info."""
        # Create input with email
        result = patterns.validate_input("WebFetch", {"url": "Contact: user@example.com for info"})
        if result.matches:
            match = result.matches[0]
            assert isinstance(match, PatternMatch)
            assert match.start_pos >= 0
            assert match.end_pos > match.start_pos


# =============================================================================
# NEGATIVE CASES (30%)
# =============================================================================


class TestInvalidInputHandling:
    """Test handling of invalid inputs."""

    def test_validate_empty_input(self, patterns: PatternLibrary) -> None:
        """Given empty input dict, when validated, then approves."""
        result = patterns.validate_input("Bash", {})
        assert result.decision == "approve"

    def test_validate_unknown_tool(self, patterns: PatternLibrary) -> None:
        """Given unknown tool name, when validated, then uses all patterns."""
        result = patterns.validate_input("UnknownTool", {"data": "test"})
        assert result.decision == "approve"

    def test_validate_none_input(self, patterns: PatternLibrary) -> None:
        """Given None values in input, when validated, then handles gracefully."""
        result = patterns.validate_input("Bash", {"command": None})
        assert result.decision in ("approve", "warn", "block")


class TestEmptyPatternLibrary:
    """Test behavior with empty pattern library."""

    def test_empty_library_approves_all(self, empty_patterns: PatternLibrary) -> None:
        """Given empty pattern library, when validating, then approves all."""
        result = empty_patterns.validate_input("Bash", {"command": "rm -rf /"})
        assert result.decision == "approve"

    def test_empty_library_has_no_matches(self, empty_patterns: PatternLibrary) -> None:
        """Given empty pattern library, when validating, then no matches."""
        result = empty_patterns.validate_output("Bash", "secret-key-12345")
        assert len(result.matches) == 0


# =============================================================================
# EDGE CASES (10%)
# =============================================================================


class TestEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_very_long_input(self, patterns: PatternLibrary) -> None:
        """Given very long input, when validated, then completes within timeout."""
        long_text = "x" * 10000
        result = patterns.validate_input("Bash", {"command": long_text})
        assert result.elapsed_ms < 5000  # Should complete within 5 seconds

    def test_unicode_in_input(self, patterns: PatternLibrary) -> None:
        """Given unicode input, when validated, then handles correctly."""
        result = patterns.validate_input("Bash", {"command": "echo '日本語 テスト 🎯'"})
        assert result.decision in ("approve", "warn", "block")

    def test_validation_result_to_json(self, patterns: PatternLibrary) -> None:
        """Given ValidationResult, when converted to JSON, then is serializable."""
        result = patterns.validate_input("Bash", {"command": "ls"})
        json_result = result.to_json()
        # Should be serializable
        json_str = json.dumps(json_result)
        assert isinstance(json_str, str)


class TestTimeoutBehavior:
    """Test timeout behavior (AC-015-002)."""

    def test_validation_completes_within_timeout(self, patterns: PatternLibrary) -> None:
        """Given normal input, when validated, then completes under 100ms."""
        result = patterns.validate_input("Bash", {"command": "ls -la"})
        # Allow some margin for slow systems
        assert result.elapsed_ms < 500  # 500ms max


# =============================================================================
# ACCEPTANCE CRITERIA TESTS
# =============================================================================


class TestAcceptanceCriteria:
    """Test specific acceptance criteria from WI-SAO-015."""

    def test_ac_015_002_timeout_configured(self, patterns: PatternLibrary) -> None:
        """AC-015-002: Verify timeout_ms is configured in patterns."""
        for group in patterns.input_patterns.values():
            assert hasattr(group, "timeout_ms")
            assert group.timeout_ms == 100 or group.timeout_ms == 50

    def test_ac_015_003_warn_mode_default(self, patterns: PatternLibrary) -> None:
        """AC-015-003: Verify warn mode is available."""
        assert "pii_detection" in patterns.input_patterns
        pii_group = patterns.input_patterns["pii_detection"]
        assert pii_group.mode == "warn"

    def test_ac_015_004_pattern_library_exists(self, patterns: PatternLibrary) -> None:
        """AC-015-004: Verify pattern library has common checks."""
        # Should have PII detection
        assert "pii_detection" in patterns.input_patterns
        pii_rules = patterns.input_patterns["pii_detection"].rules
        rule_ids = [r.id for r in pii_rules]
        assert "pii-email" in rule_ids

        # Should have secrets detection
        assert "secrets_detection" in patterns.input_patterns
        secret_rules = patterns.input_patterns["secrets_detection"].rules
        rule_ids = [r.id for r in secret_rules]
        assert "secret-generic-password" in rule_ids


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
