#!/usr/bin/env python3
"""
Pre-Tool Use Hook - Security Guardrails

This hook runs BEFORE Claude executes any tool, providing security checks
and guardrails to prevent dangerous operations.

Reference: https://docs.anthropic.com/en/docs/claude-code/hooks

Work Item: WI-SAO-015 (Guardrail Validation Hooks)
Acceptance Criteria:
    - AC-015-001: Async validation via subprocess model
    - AC-015-002: timeout_ms: 100
    - AC-015-003: mode: warn (log but don't block)
    - AC-015-004: Pattern library for common checks

Exit Codes:
    0 - Allow the tool use (with optional decision in JSON)
    1 - Block the tool use (with reason)
    2 - Error in hook execution
"""

import json
import os
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
# PATTERN LIBRARY (AC-015-004)
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
            pass  # Fall back to rule-based checks only
    return _patterns


# =============================================================================
# CONFIGURATION
# =============================================================================

# Paths that should NEVER be written to (security-critical)
BLOCKED_WRITE_PATHS = [
    "~/.ssh",
    "~/.gnupg",
    "~/.aws",
    "~/.config/gcloud",
    "/etc",
    "/var",
    "/usr",
    "/bin",
    "/sbin",
]

# File patterns that should never be committed
SENSITIVE_FILE_PATTERNS = [
    ".env",
    ".env.local",
    ".env.production",
    "credentials.json",
    "secrets.yaml",
    "*.pem",
    "*.key",
    "id_rsa",
    "id_ed25519",
]

# Commands that require extra scrutiny
DANGEROUS_COMMANDS = [
    "rm -rf /",
    "rm -rf ~",
    "chmod 777",
    "curl | bash",
    "wget | bash",
    "eval",
    "> /dev/sda",
    "mkfs",
    "dd if=",
]


# =============================================================================
# HOOK LOGIC
# =============================================================================


def check_file_write(tool_input: dict[str, Any]) -> tuple[bool, str]:
    """Check if a file write operation is safe."""
    file_path = tool_input.get("file_path", "")

    # Expand home directory
    expanded_path = os.path.expanduser(file_path)

    # Check against blocked paths
    for blocked in BLOCKED_WRITE_PATHS:
        blocked_expanded = os.path.expanduser(blocked)
        if expanded_path.startswith(blocked_expanded):
            return False, f"Writing to {blocked} is blocked for security"

    # Check for sensitive files
    basename = os.path.basename(file_path)
    for pattern in SENSITIVE_FILE_PATTERNS:
        if pattern.startswith("*"):
            if basename.endswith(pattern[1:]):
                return False, f"Writing to sensitive file pattern {pattern} is blocked"
        elif basename == pattern:
            return False, f"Writing to sensitive file {pattern} is blocked"

    return True, ""


def check_bash_command(tool_input: dict[str, Any]) -> tuple[bool, str]:
    """Check if a bash command is safe."""
    command = tool_input.get("command", "")

    # Block cd commands - maintain working directory using absolute paths
    # This prevents scripts from having incorrect path assumptions
    cmd_stripped = command.strip()
    if (
        cmd_stripped.startswith("cd ")
        or cmd_stripped == "cd"
        or " && cd " in command
        or "; cd " in command
        or "$(cd " in command
    ):
        return False, "cd command blocked: Use absolute paths instead of changing directories"

    # Check for dangerous commands
    for dangerous in DANGEROUS_COMMANDS:
        if dangerous in command:
            return False, f"Command contains dangerous pattern: {dangerous}"

    # Warn about shell=True equivalent patterns
    if "| sh" in command or "| bash" in command:
        # Allow but log warning
        print(
            json.dumps({"warning": "Piping to shell detected - ensure source is trusted"}),
            file=sys.stderr,
        )

    return True, ""


def check_git_operation(tool_input: dict[str, Any]) -> tuple[bool, str]:
    """Check if a git operation is safe."""
    command = tool_input.get("command", "")

    # Block force pushes to main/master
    if "push" in command and "--force" in command:
        if "main" in command or "master" in command:
            return False, "Force push to main/master is blocked"

    # Block hard resets
    if "reset --hard" in command:
        # Allow but warn
        print(
            json.dumps({"warning": "git reset --hard will lose uncommitted changes"}),
            file=sys.stderr,
        )

    return True, ""


def check_patterns(tool_name: str, tool_input: dict[str, Any]) -> tuple[str, str, list[dict]]:
    """
    Check tool input against pattern library.

    Implements:
        - AC-015-001: Async validation (subprocess model - inherent)
        - AC-015-002: timeout_ms: 100 (configured in patterns)
        - AC-015-003: mode: warn (default behavior)
        - AC-015-004: Pattern library for common checks

    Args:
        tool_name: Name of the tool being called
        tool_input: Tool input parameters

    Returns:
        Tuple of (decision, reason, matches) where:
        - decision: "approve", "warn", "block", or "ask"
        - reason: Human-readable explanation
        - matches: List of pattern matches for logging
    """
    patterns = get_patterns()
    if patterns is None:
        return "approve", "", []

    try:
        result = patterns.validate_input(tool_name, tool_input)
        matches = [
            {
                "rule_id": m.rule_id,
                "severity": m.severity,
                "description": m.description,
            }
            for m in result.matches
        ]
        return result.decision, result.reason, matches
    except Exception as e:
        # Pattern validation failure should not block operations
        # Log error and approve (AC-015-003: warn mode)
        print(
            json.dumps({"warning": f"Pattern validation error: {e}", "fallback": "approve"}),
            file=sys.stderr,
        )
        return "approve", "", []


def main() -> int:
    """Main hook entry point."""
    try:
        # Read hook input from stdin
        input_data = json.loads(sys.stdin.read())

        tool_name = input_data.get("tool_name", "")
        tool_input = input_data.get("tool_input", {})

        # =================================================================
        # PHASE 1: Rule-based security checks (existing behavior)
        # =================================================================
        allowed = True
        reason = ""

        if tool_name in ("Write", "Edit", "MultiEdit"):
            allowed, reason = check_file_write(tool_input)

        elif tool_name == "Bash":
            allowed, reason = check_bash_command(tool_input)
            if allowed and "git" in tool_input.get("command", ""):
                allowed, reason = check_git_operation(tool_input)

        # If rule-based check blocks, return immediately
        if not allowed:
            print(json.dumps({"decision": "block", "reason": reason}))
            return 0

        # =================================================================
        # PHASE 2: Pattern-based validation (AC-015-004)
        # =================================================================
        pattern_decision, pattern_reason, pattern_matches = check_patterns(tool_name, tool_input)

        # Handle pattern validation result
        if pattern_decision == "block":
            print(
                json.dumps(
                    {"decision": "block", "reason": pattern_reason, "matches": pattern_matches}
                )
            )
            return 0

        if pattern_decision == "warn":
            # Log warning to stderr, but approve (AC-015-003)
            print(
                json.dumps({"warning": pattern_reason, "matches": pattern_matches}), file=sys.stderr
            )
            # Continue to approve below

        if pattern_decision == "ask":
            # Ask user for confirmation
            print(
                json.dumps(
                    {"decision": "ask", "reason": pattern_reason, "matches": pattern_matches}
                )
            )
            return 0

        # =================================================================
        # PHASE 3: Approve if all checks pass
        # =================================================================
        print(json.dumps({"decision": "approve"}))
        return 0

    except json.JSONDecodeError as e:
        print(json.dumps({"decision": "block", "reason": f"Hook error: Invalid JSON input - {e}"}))
        return 2
    except Exception as e:
        print(json.dumps({"decision": "block", "reason": f"Hook error: {e}"}))
        return 2


if __name__ == "__main__":
    sys.exit(main())
