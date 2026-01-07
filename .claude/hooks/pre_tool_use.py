#!/usr/bin/env python3
"""
Pre-Tool Use Hook - Security Guardrails

This hook runs BEFORE Claude executes any tool, providing security checks
and guardrails to prevent dangerous operations.

Reference: https://docs.anthropic.com/en/docs/claude-code/hooks

Exit Codes:
    0 - Allow the tool use
    1 - Block the tool use (with reason)
    2 - Error in hook execution
"""

import json
import os
import sys
from typing import Any


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

    # Check for dangerous commands
    for dangerous in DANGEROUS_COMMANDS:
        if dangerous in command:
            return False, f"Command contains dangerous pattern: {dangerous}"

    # Warn about shell=True equivalent patterns
    if "| sh" in command or "| bash" in command:
        # Allow but log warning
        print(
            json.dumps({
                "warning": "Piping to shell detected - ensure source is trusted"
            }),
            file=sys.stderr
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
            json.dumps({
                "warning": "git reset --hard will lose uncommitted changes"
            }),
            file=sys.stderr
        )

    return True, ""


def main() -> int:
    """Main hook entry point."""
    try:
        # Read hook input from stdin
        input_data = json.loads(sys.stdin.read())

        tool_name = input_data.get("tool_name", "")
        tool_input = input_data.get("tool_input", {})

        # Route to appropriate checker
        allowed = True
        reason = ""

        if tool_name in ("Write", "Edit", "MultiEdit"):
            allowed, reason = check_file_write(tool_input)

        elif tool_name == "Bash":
            allowed, reason = check_bash_command(tool_input)
            if allowed and "git" in tool_input.get("command", ""):
                allowed, reason = check_git_operation(tool_input)

        # Output result
        if not allowed:
            print(json.dumps({
                "decision": "block",
                "reason": reason
            }))
            return 0

        # Allow by default
        print(json.dumps({"decision": "allow"}))
        return 0

    except json.JSONDecodeError as e:
        print(json.dumps({
            "decision": "block",
            "reason": f"Hook error: Invalid JSON input - {e}"
        }))
        return 2
    except Exception as e:
        print(json.dumps({
            "decision": "block",
            "reason": f"Hook error: {e}"
        }))
        return 2


if __name__ == "__main__":
    sys.exit(main())
