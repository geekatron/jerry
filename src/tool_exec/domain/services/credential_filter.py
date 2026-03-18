# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Credential filter service for redacting sensitive data from tool output.

Ports all 15 patterns from the bash rainbow-tool-exec script (BC-07),
organized into case-sensitive and case-insensitive groups. Supports
family-specific pattern extensions via SecurityPolicy.

References:
    - ADR-PROJ023-001: Behavioral Contract BC-07 (Credential Filtering)
    - rainbow-tool-exec lines 322-348: Original bash patterns
    - TASK-006: CredentialFilterService
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass


@dataclass(frozen=True)
class CredentialMatch:
    """Result of a credential detection match.

    Attributes:
        pattern: The regex pattern that matched.
        line_number: 1-based line number where the match occurred.
        case_sensitive: Whether the match was case-sensitive.
    """

    pattern: str
    line_number: int
    case_sensitive: bool


@dataclass
class FilterResult:
    """Result of applying the credential filter to output.

    Attributes:
        detected: Whether any credential was detected.
        match: The first CredentialMatch, or None if no detection.
        filtered_output: The output after filtering (redacted or original).
        raw_output: The original unfiltered output.
    """

    detected: bool
    match: CredentialMatch | None
    filtered_output: str
    raw_output: str


class CredentialFilterService:
    """Filters credential material from tool output using regex patterns.

    Implements the L1 regex layer of the credential filter pipeline (BC-07).
    Patterns are split into case-sensitive and case-insensitive groups,
    matching the bash implementation's ERE patterns.

    The 15 base patterns (8 case-sensitive + 7 case-insensitive) cover:
    - AWS access key IDs (AKIA/AGPA/AROA/etc.)
    - SSH/PGP private key headers
    - NTLM hash pairs
    - Kerberos ticket material (base64 krb5)
    - Anthropic API keys (sk-ant-api)
    - OpenAI project API keys (sk-proj-)
    - Google AI API keys (AIzaSy)
    - GitHub fine-grained PATs (github_pat_)
    - Stripe live secret/restricted keys (sk_live_, rk_live_)
    - Slack bot tokens (xoxb-)
    - JWT tokens (eyJ...eyJ...sig)
    - AWS secret keys
    - API tokens and Bearer tokens
    - Password assignments
    - Database connection strings with credentials

    Family-specific patterns can be added via extend_patterns().

    Security: M-02 mitigation for T-03 (DREAD 36 -> 24 post-mitigation).
    The AI CLI family extension requires cloud AI API key coverage.
    """

    REDACTION_MARKER = "[CREDENTIAL-REDACTED]"

    # Case-sensitive patterns (matched against original line).
    # Ported from rainbow-tool-exec CREDENTIAL_FILTER_PATTERNS_CS plus
    # M-02 additions for modern cloud provider and AI API key formats.
    _BASE_CS_PATTERNS: list[str] = [
        # AWS access key ID (uppercase, fixed prefix families)
        r"(A3T[A-Z0-9]|AKIA|AGPA|AROA|AIPA|ANPA|ANVA|ASIA)[A-Z0-9]{16}",
        # SSH / PGP private key header
        r"-----BEGIN (RSA|DSA|EC|OPENSSH|PGP) PRIVATE KEY",
        # NTLM hash pair (32 hex chars each, colon-delimited)
        r":[0-9a-fA-F]{32}:[0-9a-fA-F]{32}:",
        # Kerberos ticket material -- base64-encoded krb5 ASN.1 (YAIB/YII header)
        r"YII[A-Za-z0-9+/]{20,}={0,2}",
        # M-02: Anthropic API key (sk-ant-api + 2 digits + base64url 86 chars)
        r"sk-ant-api[0-9]{2}-[A-Za-z0-9_-]{86}",
        # M-02: OpenAI project API key (sk-proj- + 20+ alphanumeric/url-safe chars)
        r"sk-proj-[A-Za-z0-9_-]{20,}",
        # M-02: Google AI API key (AIzaSy + 33 alphanumeric/url-safe chars)
        r"AIzaSy[A-Za-z0-9_-]{33}",
        # M-02: GitHub fine-grained personal access token
        r"github_pat_[A-Za-z0-9_]{22,}",
    ]

    # Case-insensitive patterns (matched against lowercased line).
    # Ported from rainbow-tool-exec CREDENTIAL_FILTER_PATTERNS_CI plus
    # M-02 additions for Stripe, Slack, and JWT formats.
    _BASE_CI_PATTERNS: list[str] = [
        # AWS secret key (heuristic -- base64-like 40 chars after key=)
        r"(aws_secret_access_key|aws_secret)\s*[=:]\s*[A-Za-z0-9/+=]{40}",
        # Generic API token / Bearer patterns
        r"(api[_\-]?key|api[_\-]?token|access[_\-]?token|bearer)\s*[=: ]\s*[A-Za-z0-9_.\:/\-]{20,}",
        # Generic password assignment
        r"(password|passwd|pwd)\s*[=:]\s*\S{8,}",
        # Connection strings with embedded credentials
        r"(mongodb|postgresql|mysql|redis|amqp)(\+srv)?://[^:]+:[^@]+@",
        # M-02: Stripe live secret key and restricted key
        r"(sk_live_|rk_live_)[A-Za-z0-9]{24,}",
        # M-02: Slack bot/user/app token (xoxb-, xoxp-, xoxa-)
        r"xox[bpa]-[0-9]{10,}-[0-9]{10,}-[A-Za-z0-9]{24,}",
        # M-02: JWT token (base64url header.payload.signature with eyJ prefix)
        r"eyJ[A-Za-z0-9_-]{10,}\.eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}",
    ]

    def __init__(self) -> None:
        """Initialize the credential filter with base patterns."""
        self._cs_patterns: list[re.Pattern[str]] = [re.compile(p) for p in self._BASE_CS_PATTERNS]
        self._ci_patterns: list[re.Pattern[str]] = [
            re.compile(p, re.IGNORECASE) for p in self._BASE_CI_PATTERNS
        ]
        self._cs_raw: list[str] = list(self._BASE_CS_PATTERNS)
        self._ci_raw: list[str] = list(self._BASE_CI_PATTERNS)

    def extend_patterns(
        self,
        patterns: list[str],
        case_sensitive: bool = True,
    ) -> None:
        """Add family-specific credential filter patterns.

        Args:
            patterns: List of regex pattern strings to add.
            case_sensitive: If True, patterns are added to the case-sensitive
                group. If False, they are added to the case-insensitive group.

        Raises:
            re.error: If any pattern is not a valid regex.
        """
        for pattern_str in patterns:
            compiled = (
                re.compile(pattern_str)
                if case_sensitive
                else re.compile(pattern_str, re.IGNORECASE)
            )
            if case_sensitive:
                self._cs_patterns.append(compiled)
                self._cs_raw.append(pattern_str)
            else:
                self._ci_patterns.append(compiled)
                self._ci_raw.append(pattern_str)

    def filter_output(self, raw_output: str) -> FilterResult:
        """Apply the credential filter to tool output.

        Uses a sliding-window approach: scans each line individually, then
        scans adjacent line pairs to catch credentials split across line
        boundaries (VF-001 mitigation). On first match, returns a FilterResult
        with detected=True and the matching details.

        Args:
            raw_output: The raw tool output to filter.

        Returns:
            FilterResult with detection status and filtered output.
        """
        lines = raw_output.split("\n")

        # Pass 1: Single-line scan (fast path for most detections)
        for line_idx, line in enumerate(lines):
            match = self._scan_text(line, line_idx + 1)
            if match is not None:
                return FilterResult(
                    detected=True,
                    match=match,
                    filtered_output=self._build_redaction_notice(match.line_number),
                    raw_output=raw_output,
                )

        # Pass 2: Sliding-window scan over adjacent line pairs (VF-001 fix).
        # Catches credentials whose distinctive prefix is split across a line
        # boundary (e.g., "AK\nIA1234567890ABCDEF"). Joins adjacent lines
        # with no separator to reconstruct the split credential.
        for line_idx in range(len(lines) - 1):
            joined = lines[line_idx] + lines[line_idx + 1]
            match = self._scan_text(joined, line_idx + 1)
            if match is not None:
                return FilterResult(
                    detected=True,
                    match=CredentialMatch(
                        pattern=match.pattern,
                        line_number=match.line_number,
                        case_sensitive=match.case_sensitive,
                    ),
                    filtered_output=self._build_redaction_notice(match.line_number),
                    raw_output=raw_output,
                )

        # No credential detected
        return FilterResult(
            detected=False,
            match=None,
            filtered_output=raw_output,
            raw_output=raw_output,
        )

    def _scan_text(self, text: str, line_number: int) -> CredentialMatch | None:
        """Scan a text string against all patterns.

        Args:
            text: The text to scan (single line or joined adjacent lines).
            line_number: 1-based line number for reporting.

        Returns:
            CredentialMatch if a pattern matched, None otherwise.
        """
        for pattern_idx, pattern in enumerate(self._cs_patterns):
            if pattern.search(text):
                return CredentialMatch(
                    pattern=self._cs_raw[pattern_idx],
                    line_number=line_number,
                    case_sensitive=True,
                )

        for pattern_idx, pattern in enumerate(self._ci_patterns):
            if pattern.search(text):
                return CredentialMatch(
                    pattern=self._ci_raw[pattern_idx],
                    line_number=line_number,
                    case_sensitive=False,
                )

        return None

    def pattern_count(self) -> int:
        """Return the total number of active patterns.

        Returns:
            Count of case-sensitive plus case-insensitive patterns.
        """
        return len(self._cs_patterns) + len(self._ci_patterns)

    def _build_redaction_notice(self, line_number: int) -> str:
        """Build the redaction notice for quarantined output.

        Args:
            line_number: 1-based line number where the credential was detected.

        Returns:
            Redaction notice string.
        """
        return (
            f"[CREDENTIAL-FILTER] Output quarantined. "
            f"Detecting layer: L1-regex. "
            f"Pattern matched at line {line_number}.\n"
            f"[CREDENTIAL-FILTER] Do NOT attempt to retrieve "
            f"quarantined content without operator review."
        )
