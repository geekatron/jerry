# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Security enforcement engine for pre-tool-use validation.

Evaluates tool inputs against security rules: blocked paths, dangerous
commands, sensitive files, git safety, and pattern-based detection.

Fail-open by design: any internal error results in approval.

References:
    - #150: pre_tool_use.py consolidation
    - #234: Fix _check_cd false-positive substring matching
    - ADR-150-001: Pre-Tool Enforcement Pipeline Consolidation
    - T-04: Path traversal prevention via normpath/expanduser
    - T-06: Never log matched text, only rule IDs
"""

from __future__ import annotations

import os
import re
from typing import Any

from src.infrastructure.internal.enforcement.enforcement_decision import (
    EnforcementDecision,
)
from src.infrastructure.internal.enforcement.security_rules import SecurityRules

# Tools that trigger file path checks
_WRITE_TOOLS = frozenset({"Write", "Edit", "MultiEdit", "NotebookEdit"})

# Tools that trigger bash command checks
_BASH_TOOLS = frozenset({"Bash"})

# Approve decision (singleton-like for readability)
_APPROVE = EnforcementDecision(action="approve", reason="")


class SecurityEnforcementEngine:
    """Security enforcement engine for pre-tool-use validation.

    Evaluates tool inputs against security rules: blocked paths,
    dangerous commands, sensitive files, git safety.

    Fail-open by design: any internal error results in approval.

    Args:
        security_rules: Injectable security rules configuration.
            If None, uses default production rules.
        pattern_library: Injectable pattern library for PII/secrets
            detection. If None, pattern checks are skipped.
    """

    def __init__(
        self,
        security_rules: SecurityRules | None = None,
        pattern_library: Any | None = None,
    ) -> None:
        self._rules = security_rules or SecurityRules.default()
        self._pattern_library = pattern_library

    def evaluate(
        self,
        tool_name: str,
        tool_input: dict[str, Any],
    ) -> EnforcementDecision:
        """Evaluate a tool use request against security rules.

        Runs applicable checks based on tool_name. Returns the
        highest-severity result across all checks.

        Args:
            tool_name: Claude Code tool name.
            tool_input: Tool input parameters.

        Returns:
            EnforcementDecision with action, reason, violations.
        """
        try:
            return self._evaluate_internal(tool_name, tool_input)
        except Exception:
            return _APPROVE  # fail-open

    def _evaluate_internal(
        self,
        tool_name: str,
        tool_input: dict[str, Any],
    ) -> EnforcementDecision:
        """Internal evaluation — exceptions propagate to evaluate()."""
        # File write checks (Write, Edit, MultiEdit, NotebookEdit)
        if tool_name in _WRITE_TOOLS:
            file_path = tool_input.get("file_path", "")
            # BV-10: Type guard — non-string file_path is fail-open
            if not isinstance(file_path, str) or not file_path:
                return _APPROVE

            # BV-11: Null byte injection — block immediately
            if "\x00" in file_path:
                return EnforcementDecision(
                    action="block",
                    reason="Null byte in file path (path injection attempt)",
                    violations=["Null byte injection in file_path"],
                )

            decision = self._check_file_write(file_path)
            if decision.action == "block":
                return decision

        # Bash command checks
        if tool_name in _BASH_TOOLS:
            command = tool_input.get("command", "")
            # BV-10: Type guard for command
            if not isinstance(command, str) or not command:
                return _APPROVE

            # BV-11: Null byte in command
            if "\x00" in command:
                return EnforcementDecision(
                    action="block",
                    reason="Null byte in command (injection attempt)",
                    violations=["Null byte injection in command"],
                )

            decision = self._check_bash_command(command)
            if decision.action == "block":
                return decision

        # Pattern-based validation (if library available)
        if self._pattern_library is not None:
            decision = self._check_patterns(tool_name, tool_input)
            if decision.action == "block":
                return decision

        return _APPROVE

    # ------------------------------------------------------------------
    # File write checks (C-001, C-002)
    # ------------------------------------------------------------------

    def _check_file_write(self, file_path: str) -> EnforcementDecision:
        """Check file path against blocked paths and sensitive patterns.

        Uses os.path.normpath(os.path.expanduser()) to canonicalize
        the path before comparison, preventing traversal bypasses (T-04).
        """
        # Canonicalize path to prevent traversal (T-04)
        canonical = os.path.normpath(os.path.expanduser(file_path))

        # C-001: Blocked system paths
        for blocked in self._rules.blocked_write_paths:
            blocked_expanded = os.path.normpath(os.path.expanduser(blocked))

            if canonical.startswith(blocked_expanded):
                return EnforcementDecision(
                    action="block",
                    reason=f"Writing to {blocked} is blocked for security",
                    violations=[f"Blocked path: {blocked}"],
                )

            # For home-relative rules (~/.ssh), also match the dotdir as a
            # path component in any user's home directory.
            # BV-06: Use path component check, not substring, to avoid
            # false positives on paths like /project/my-ssh-tool/config.py
            if blocked.startswith("~/"):
                dotdir = blocked[2:]  # .ssh, .gnupg, .aws
                # Check if dotdir appears as an exact directory component.
                # Use [/\\] to handle both Unix and Windows path separators
                # since os.path.normpath uses backslashes on Windows.
                if re.search(r"(?<=[/\\])" + re.escape(dotdir) + r"([/\\]|$)", canonical):
                    return EnforcementDecision(
                        action="block",
                        reason=f"Writing to {blocked} is blocked for security",
                        violations=[f"Blocked path: {blocked}"],
                    )

        # C-002: Sensitive file patterns
        basename = os.path.basename(canonical).lower()

        # Check exceptions first (.env.example is allowed)
        for exception in self._rules.sensitive_file_exceptions:
            if basename == exception.lower():
                return _APPROVE

        # Check sensitive patterns
        for pattern in self._rules.sensitive_file_patterns:
            pattern_lower = pattern.lower()
            if basename == pattern_lower or basename.startswith(pattern_lower):
                return EnforcementDecision(
                    action="block",
                    reason=(
                        f"Writing to sensitive file ({pattern}) is blocked. "
                        f"File: {os.path.basename(file_path)}"
                    ),
                    violations=[f"Sensitive file pattern: {pattern}"],
                )
            # Also check extension match (.pem, .key)
            if pattern_lower.startswith(".") and basename.endswith(pattern_lower):
                return EnforcementDecision(
                    action="block",
                    reason=(
                        f"Writing to sensitive file ({pattern}) is blocked. "
                        f"File: {os.path.basename(file_path)}"
                    ),
                    violations=[f"Sensitive file pattern: {pattern}"],
                )

        return _APPROVE

    # ------------------------------------------------------------------
    # Bash command checks (C-003, C-004, C-005, C-007)
    # ------------------------------------------------------------------

    def _check_bash_command(self, command: str) -> EnforcementDecision:
        """Check bash command against dangerous patterns."""
        # C-003: cd command blocking
        decision = self._check_cd(command)
        if decision.action == "block":
            return decision

        # C-004: Dangerous rm patterns
        decision = self._check_dangerous_rm(command)
        if decision.action == "block":
            return decision

        # C-005: Dangerous commands
        decision = self._check_dangerous_commands(command)
        if decision.action == "block":
            return decision

        # C-007: Git force push to main/master
        decision = self._check_git_force_push(command)
        if decision.action == "block":
            return decision

        return _APPROVE

    def _check_cd(self, command: str) -> EnforcementDecision:
        """C-003: Block cd commands to preserve working directory."""
        cmd_lower = command.lower().strip()

        # Exact "cd" command
        if cmd_lower == "cd" or cmd_lower.startswith("cd ") or cmd_lower.startswith("cd\t"):
            return EnforcementDecision(
                action="block",
                reason=(
                    "cd commands are blocked to preserve working directory. "
                    "Use absolute paths instead."
                ),
                violations=["cd command detected"],
            )

        # cd after command separators (regex word-boundary matching, issue #234)
        for pattern in self._rules.cd_patterns:
            if re.search(pattern, command, re.IGNORECASE):
                return EnforcementDecision(
                    action="block",
                    reason=(
                        "cd commands are blocked to preserve working directory. "
                        "Use absolute paths instead."
                    ),
                    violations=[f"cd command detected (pattern: {pattern})"],
                )

        return _APPROVE

    def _check_dangerous_rm(self, command: str) -> EnforcementDecision:
        """C-004: Block destructive rm commands.

        Detects rm -rf /, rm -r -f /, rm --recursive --force /,
        and flag order variations.
        """
        # Match rm with -r and -f flags (in any order) targeting / or ~
        rm_pattern = re.compile(
            r"\brm\s+"
            r"(?=.*(?:-[a-zA-Z]*r[a-zA-Z]*|--recursive))"
            r"(?=.*(?:-[a-zA-Z]*f[a-zA-Z]*|--force))"
            r".*\s+[/~]",
        )
        if rm_pattern.search(command):
            return EnforcementDecision(
                action="block",
                reason="Destructive rm command detected targeting / or ~",
                violations=["Dangerous rm pattern"],
            )

        return _APPROVE

    def _check_dangerous_commands(self, command: str) -> EnforcementDecision:
        """C-005: Block known dangerous commands."""
        cmd_lower = command.lower()

        # BV-04: Download-then-execute pattern — catches pipe, &&, ;, >
        # curl/wget followed by bash/sh in the same command, any separator
        if re.search(r"\b(curl|wget)\b.*\b(bash|sh)\b", cmd_lower):
            return EnforcementDecision(
                action="block",
                reason="Download followed by shell execution is blocked",
                violations=["Download-execute pattern detected"],
            )

        # F-003: eval as a bash command (word-boundary to avoid matching
        # "evaluate", "evaluation", etc.)
        if re.search(r"\beval\b", cmd_lower):
            return EnforcementDecision(
                action="block",
                reason="eval command is blocked (arbitrary code execution)",
                violations=["eval command detected"],
            )

        # Check exact substring patterns
        for dangerous in self._rules.dangerous_commands:
            if dangerous.lower() in cmd_lower:
                return EnforcementDecision(
                    action="block",
                    reason=f"Dangerous command pattern detected: {dangerous}",
                    violations=[f"Dangerous command: {dangerous}"],
                )

        return _APPROVE

    def _check_git_force_push(self, command: str) -> EnforcementDecision:
        """C-007: Block force push to protected branches."""
        cmd_lower = command.lower()

        is_force = "--force" in cmd_lower or "-f " in cmd_lower or cmd_lower.endswith("-f")
        # BV-05: Use regex to handle multiple spaces between git and push
        is_push = bool(re.search(r"\bgit\s+push\b", cmd_lower))

        if is_force and is_push:
            for branch in self._rules.force_push_branches:
                if branch in cmd_lower:
                    return EnforcementDecision(
                        action="block",
                        reason=(
                            f"Force push to {branch} is blocked. Use a feature branch instead."
                        ),
                        violations=[f"Force push to {branch}"],
                    )

        return _APPROVE

    # ------------------------------------------------------------------
    # Pattern-based validation (C-012..C-017)
    # ------------------------------------------------------------------

    def _check_patterns(self, tool_name: str, tool_input: dict[str, Any]) -> EnforcementDecision:
        """Check tool input against pattern library (PII, secrets)."""
        try:
            library = self._pattern_library
            if library is None:
                return _APPROVE
            result = library.validate_tool_input(tool_name, tool_input)
            if result.decision == "block":
                return EnforcementDecision(
                    action="block",
                    reason=result.reason,
                    violations=[
                        # T-06: Log rule_id only, never matched text
                        f"Pattern match: {m.rule_id}"
                        for m in result.matches
                    ],
                )
        except Exception:
            pass  # fail-open on pattern library errors

        return _APPROVE
