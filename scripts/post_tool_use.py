#!/usr/bin/env python3
"""
Post-Tool Use Hook - Output Filtering

This hook runs AFTER Claude executes a tool, providing output filtering
and redaction of sensitive information.

Reference: https://docs.anthropic.com/en/docs/claude-code/hooks

Work Item: WI-SAO-015 (Guardrail Validation Hooks)
Acceptance Criteria:
    - AC-015-001: Async validation via subprocess model
    - AC-015-002: timeout_ms: 100
    - AC-015-003: mode: warn (log but don't block)
    - AC-015-004: Pattern library for common checks

Exit Codes:
    0 - Success (output may be modified)
    2 - Error in hook execution
"""

import json
import re
import sys
from pathlib import Path
from typing import Any

# Import pattern library (relative import from same directory)
try:
    from patterns import PatternLibrary, load_patterns

    PATTERNS_AVAILABLE = True
except ImportError:
    # Fallback: try absolute import
    try:
        sys.path.insert(0, str(Path(__file__).parent))
        from patterns import PatternLibrary, load_patterns

        PATTERNS_AVAILABLE = True
    except ImportError:
        PATTERNS_AVAILABLE = False
        PatternLibrary = None  # type: ignore


# =============================================================================
# PATTERN LIBRARY
# =============================================================================

# Load patterns once at module level for performance
_patterns: PatternLibrary | None = None


def get_patterns() -> PatternLibrary | None:
    """Get cached pattern library instance."""
    global _patterns
    if _patterns is None and PATTERNS_AVAILABLE:
        try:
            _patterns = load_patterns()
        except Exception:
            pass  # Fall back to no output filtering
    return _patterns


# =============================================================================
# OUTPUT FILTERING
# =============================================================================


def redact_output(
    tool_name: str,
    tool_output: str,
) -> tuple[str, list[dict]]:
    """
    Filter tool output by redacting sensitive patterns.

    Args:
        tool_name: Name of the tool that produced output
        tool_output: The raw tool output

    Returns:
        Tuple of (filtered_output, redactions) where:
        - filtered_output: Output with sensitive data redacted
        - redactions: List of redaction actions taken
    """
    patterns = get_patterns()
    if patterns is None:
        return tool_output, []

    try:
        result = patterns.validate_output(tool_name, tool_output)

        if not result.matches:
            return tool_output, []

        # Apply redactions
        filtered = tool_output
        redactions = []

        # Sort matches by position (reverse) to maintain positions during replacement
        sorted_matches = sorted(result.matches, key=lambda m: m.start_pos, reverse=True)

        for match in sorted_matches:
            # Get replacement from pattern group
            group = patterns.output_patterns.get(match.pattern_group)
            replacement = "[REDACTED]"
            if group and group.replacement:
                replacement = group.replacement

            # Replace the matched text
            filtered = filtered[: match.start_pos] + replacement + filtered[match.end_pos :]

            redactions.append(
                {
                    "rule_id": match.rule_id,
                    "description": match.description,
                    "severity": match.severity,
                    "original_length": len(match.matched_text),
                }
            )

        return filtered, redactions

    except Exception as e:
        # Output filtering failure should not block output
        # Log error and return original output (AC-015-003: warn mode)
        print(
            json.dumps({"warning": f"Output filtering error: {e}", "fallback": "pass_through"}),
            file=sys.stderr,
        )
        return tool_output, []


# =============================================================================
# INLINE REDACTION PATTERNS (Fallback)
# =============================================================================

# These patterns are applied directly without the pattern library
# as a safety net for environments where patterns don't load

INLINE_REDACTION_PATTERNS = [
    # Bearer tokens
    (re.compile(r"Bearer\s+[A-Za-z0-9-_.]+", re.IGNORECASE), "[BEARER_TOKEN_REDACTED]"),
    # API keys in common formats
    (re.compile(r"sk-[a-zA-Z0-9]{20,}"), "[API_KEY_REDACTED]"),
    (re.compile(r"ghp_[a-zA-Z0-9]{36}"), "[GITHUB_TOKEN_REDACTED]"),
    (re.compile(r"AKIA[0-9A-Z]{16}"), "[AWS_KEY_REDACTED]"),
]


def apply_inline_redactions(text: str) -> tuple[str, int]:
    """Apply inline redaction patterns as a safety net."""
    redaction_count = 0
    for pattern, replacement in INLINE_REDACTION_PATTERNS:
        text, count = pattern.subn(replacement, text)
        redaction_count += count
    return text, redaction_count


# =============================================================================
# MAIN HOOK LOGIC
# =============================================================================


def main() -> int:
    """Main hook entry point."""
    try:
        # Read hook input from stdin
        input_data = json.loads(sys.stdin.read())

        tool_name = input_data.get("tool_name", "")
        tool_output = input_data.get("tool_output", "")

        # If output is not a string, convert it
        if not isinstance(tool_output, str):
            tool_output = json.dumps(tool_output, default=str)

        # =================================================================
        # PHASE 1: Pattern-based redaction
        # =================================================================
        filtered_output, redactions = redact_output(tool_name, tool_output)

        # =================================================================
        # PHASE 2: Inline safety net redaction
        # =================================================================
        filtered_output, inline_count = apply_inline_redactions(filtered_output)
        if inline_count > 0:
            redactions.append(
                {
                    "rule_id": "inline-safety-net",
                    "description": f"Inline redaction applied {inline_count} times",
                    "severity": "high",
                }
            )

        # =================================================================
        # PHASE 3: Output result
        # =================================================================
        result: dict[str, Any] = {}

        if redactions:
            # Log redactions to stderr for visibility
            print(
                json.dumps(
                    {
                        "info": "Output redacted",
                        "redactions": len(redactions),
                        "details": redactions,
                    }
                ),
                file=sys.stderr,
            )
            # Return modified output
            result["output"] = filtered_output
        else:
            # No modifications needed
            result["output"] = tool_output

        print(json.dumps(result))
        return 0

    except json.JSONDecodeError as e:
        print(json.dumps({"error": f"Hook error: Invalid JSON input - {e}"}))
        return 2
    except Exception as e:
        print(json.dumps({"error": f"Hook error: {e}"}))
        return 2


if __name__ == "__main__":
    sys.exit(main())
