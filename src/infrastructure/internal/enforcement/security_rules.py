# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Static security rule definitions for pre-tool-use enforcement.

Defines blocked paths, sensitive file patterns, and dangerous commands
as immutable frozen data. Injectable for testing.

References:
    - #150: pre_tool_use.py consolidation
    - ADR-150-001: Pre-Tool Enforcement Pipeline Consolidation
    - scripts/pre_tool_use.py: Original rule definitions
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SecurityRules:
    """Static security rule definitions.

    All fields are immutable tuples. Injectable for testing with
    custom rule sets. Default values match the production rules
    from scripts/pre_tool_use.py.

    Attributes:
        blocked_write_paths: Absolute path prefixes that must never be written.
        sensitive_file_patterns: Filename patterns (case-insensitive) for
            credential/secret files.
        dangerous_commands: Exact substrings that trigger a block in Bash.
        cd_patterns: Patterns that detect cd commands in Bash.
        dangerous_rm_patterns: Regex patterns for destructive rm commands.
        force_push_branches: Branch names where force push is blocked.
        current_platform: OS platform string for path expansion.
    """

    blocked_write_paths: tuple[str, ...] = (
        "~/.ssh",
        "~/.gnupg",
        "~/.aws",
        "~/.config/gcloud",
        "/etc",
        "/var",
        "/usr",
        "/bin",
        "/sbin",
    )

    sensitive_file_patterns: tuple[str, ...] = (
        ".env",
        ".env.",
        "credentials.json",
        "secrets.yaml",
        "secrets.yml",
        ".pem",
        ".key",
        "id_rsa",
        "id_ed25519",
    )

    sensitive_file_exceptions: tuple[str, ...] = (
        ".env.example",
        ".env.template",
        ".env.sample",
    )

    dangerous_commands: tuple[str, ...] = (
        "chmod 777",
        "chmod 0777",
        "> /dev/sda",
        "mkfs",
        "dd if=",
        "find / -delete",  # BV-03: non-rm destructive deletion
        "find / -exec rm",  # BV-03: find with rm action
    )
    # Note: curl/wget download-execute patterns are handled by regex in
    # SecurityEnforcementEngine._check_dangerous_commands, not by
    # substring matching. This catches: curl URL && bash, wget URL | sh, etc.

    cd_patterns: tuple[str, ...] = (
        r"(?<!\w)cd\s",  # bare cd + whitespace, word-boundary (not "argocd")
        r"&&\s*cd\b",  # && cd
        r";\s*cd\b",  # ; cd
        r"\$\(\s*cd\b",  # $(cd
        r"\|\s*cd\b",  # | cd
        r"\(\s*cd\b",  # BV-01: subshell (cd
        r"\bpushd\b",  # BV-01: pushd builtin
        r"\benv\s+-[Cc]\b",  # BV-01: env -C / env -c
        r"\benv\s+--chdir\b",  # BV-01: env --chdir
    )

    force_push_branches: tuple[str, ...] = (
        "main",
        "master",
    )

    # Note: Windows-specific path enforcement (normcase, %SystemRoot%) from
    # scripts/pre_tool_use.py is not ported. Jerry Framework targets macOS/Linux
    # CI runners. If Windows support is needed, add platform-aware checks in a
    # future PR rather than carrying dead config fields.

    @classmethod
    def default(cls) -> SecurityRules:
        """Create default production rules."""
        return cls()
