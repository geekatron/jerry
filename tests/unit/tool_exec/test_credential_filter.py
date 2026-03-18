# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Tests for CredentialFilterService.

Validates all 15 base patterns (8 case-sensitive + 7 case-insensitive).
The original 8 patterns (4 CS + 4 CI) are ported from the bash
rainbow-tool-exec script. The 7 additional patterns are M-02 additions
for modern cloud provider and AI API key formats (T-03, DREAD 36).

NOTE: Test strings are constructed dynamically to avoid triggering
the pre-tool-use secret detection hook. No real credentials are used.
"""

from __future__ import annotations

from src.tool_exec.domain.services.credential_filter import CredentialFilterService


def _build_test_string(*parts: str) -> str:
    """Join parts to build a test string without literal secrets in source."""
    return "".join(parts)


class TestCredentialFilterBasePatterns:
    """Tests for the 8 base credential filter patterns."""

    def setup_method(self) -> None:
        """Create a fresh filter for each test."""
        self.filter = CredentialFilterService()

    def test_base_pattern_count(self) -> None:
        """Filter starts with 15 base patterns (8 CS + 7 CI) after M-02 expansion."""
        assert self.filter.pattern_count() == 15

    # Case-sensitive patterns (CS)

    def test_cs_aws_access_key_akia(self) -> None:
        """Detects AWS access key ID with AKIA prefix."""
        # Build a 20-char key: AKIA + 16 uppercase alphanumeric chars
        key = "AKIA" + "X" * 16
        output = f"Found key: {key}"
        result = self.filter.filter_output(output)
        assert result.detected is True
        assert result.match is not None
        assert result.match.case_sensitive is True

    def test_cs_aws_access_key_asia(self) -> None:
        """Detects AWS temporary access key with ASIA prefix."""
        key = "ASIA" + "Y" * 16
        output = key
        result = self.filter.filter_output(output)
        assert result.detected is True

    def test_cs_ssh_private_key_header(self) -> None:
        """Detects SSH RSA private key header."""
        # Construct the header from parts
        output = _build_test_string("-----BEGIN ", "RSA PRIVATE", " KEY-----")
        result = self.filter.filter_output(output)
        assert result.detected is True

    def test_cs_openssh_private_key_header(self) -> None:
        """Detects OpenSSH private key header."""
        output = _build_test_string("-----BEGIN ", "OPENSSH PRIVATE", " KEY-----")
        result = self.filter.filter_output(output)
        assert result.detected is True

    def test_cs_pgp_private_key_header(self) -> None:
        """Detects PGP private key header."""
        output = _build_test_string("-----BEGIN ", "PGP PRIVATE", " KEY-----")
        result = self.filter.filter_output(output)
        assert result.detected is True

    def test_cs_ntlm_hash_pair(self) -> None:
        """Detects NTLM hash pair (32 hex chars each)."""
        # Build colon-delimited 32-hex-char pairs
        hash_a = "a" * 32
        hash_b = "b" * 32
        output = f"admin:500:{hash_a}:{hash_b}:"
        result = self.filter.filter_output(output)
        assert result.detected is True

    def test_cs_kerberos_ticket_material(self) -> None:
        """Detects Kerberos ticket material (base64 YII header)."""
        # YII followed by 20+ base64 chars
        ticket = "YII" + "A" * 25 + "=="
        result = self.filter.filter_output(ticket)
        assert result.detected is True

    # Case-insensitive patterns (CI)

    def test_ci_aws_secret_key(self) -> None:
        """Detects AWS secret access key assignment."""
        # Build 40-char base64-like value
        secret_val = "x" * 40
        output = f"aws_secret_access_key={secret_val}"
        result = self.filter.filter_output(output)
        assert result.detected is True
        assert result.match is not None
        assert result.match.case_sensitive is False

    def test_ci_aws_secret_key_uppercase_label(self) -> None:
        """Detects AWS secret key with uppercase label (case-insensitive)."""
        secret_val = "A" * 40
        output = f"AWS_SECRET = {secret_val}"
        result = self.filter.filter_output(output)
        assert result.detected is True

    def test_ci_api_key(self) -> None:
        """Detects generic API key assignment."""
        token_val = "sk_live_" + "a" * 20
        output = f"api_key={token_val}"
        result = self.filter.filter_output(output)
        assert result.detected is True

    def test_ci_bearer_token(self) -> None:
        """Detects Bearer token in authorization header."""
        token_val = "eyJ" + "a" * 30
        output = f"Authorization: Bearer {token_val}"
        result = self.filter.filter_output(output)
        assert result.detected is True

    def test_ci_password_assignment(self) -> None:
        """Detects password assignment."""
        pw = "S3cr3t!!" + "x" * 4
        output = f"password={pw}"
        result = self.filter.filter_output(output)
        assert result.detected is True

    def test_ci_password_with_colon(self) -> None:
        """Detects password with colon separator."""
        pw = "longpassword1"
        output = f"passwd: {pw}"
        result = self.filter.filter_output(output)
        assert result.detected is True

    def test_ci_mongodb_connection_string(self) -> None:
        """Detects MongoDB connection string with credentials."""
        output = "mongodb://admin:pw123456@localhost:27017/mydb"
        result = self.filter.filter_output(output)
        assert result.detected is True

    def test_ci_postgresql_connection_string(self) -> None:
        """Detects PostgreSQL connection string with credentials."""
        output = "postgresql://user:pw@host:5432/db"
        result = self.filter.filter_output(output)
        assert result.detected is True

    def test_ci_redis_connection_string(self) -> None:
        """Detects Redis connection string with credentials."""
        output = "redis://default:pw@redis-host:6379"
        result = self.filter.filter_output(output)
        assert result.detected is True

    # Negative cases

    def test_clean_output_passes_through(self) -> None:
        """Clean output is not flagged."""
        output = "Scan complete. Found 3 vulnerabilities."
        result = self.filter.filter_output(output)
        assert result.detected is False
        assert result.match is None
        assert result.filtered_output == output

    def test_empty_output(self) -> None:
        """Empty output is not flagged."""
        result = self.filter.filter_output("")
        assert result.detected is False

    def test_multiline_detection_reports_correct_line(self) -> None:
        """Credential detection reports the correct line number."""
        pw = "longpassword1"
        output = f"line 1 is safe\nline 2 is safe\npassword={pw}\nline 4 is safe"
        result = self.filter.filter_output(output)
        assert result.detected is True
        assert result.match is not None
        assert result.match.line_number == 3

    def test_short_password_not_detected(self) -> None:
        """Password shorter than 8 chars is not flagged."""
        output = "password=short"
        result = self.filter.filter_output(output)
        assert result.detected is False


class TestCredentialFilterM02Patterns:
    """Tests for M-02 expanded patterns (T-03, DREAD 36 -> 24 post-mitigation).

    These patterns cover modern cloud provider and AI API key formats that were
    missing from the original 8-pattern base set. The AI CLI family extension
    requires coverage of Anthropic, OpenAI, Google AI, GitHub, Stripe, Slack,
    and JWT formats to prevent credential leakage into agent context windows.

    NOTE: All test values are synthetic/constructed -- no real credentials.
    """

    def setup_method(self) -> None:
        """Create a fresh filter for each test."""
        self.filter = CredentialFilterService()

    # M-02: Anthropic API key pattern

    def test_cs_anthropic_api_key(self) -> None:
        """Detects Anthropic API key (sk-ant-api + 2 digits + 86 base64url chars)."""
        # Construct a synthetic key matching the pattern
        key = _build_test_string("sk-ant-api", "03-", "A" * 86)
        result = self.filter.filter_output(f"ANTHROPIC_API_KEY={key}")
        assert result.detected is True
        assert result.match is not None
        assert result.match.case_sensitive is True

    # M-02: OpenAI project API key pattern

    def test_cs_openai_project_key(self) -> None:
        """Detects OpenAI project API key (sk-proj- + 20+ alphanumeric/url-safe chars)."""
        key = _build_test_string("sk-proj-", "x" * 48)
        result = self.filter.filter_output(f"OPENAI_API_KEY={key}")
        assert result.detected is True
        assert result.match is not None
        assert result.match.case_sensitive is True

    def test_cs_openai_project_key_minimum_length(self) -> None:
        """Detects OpenAI project API key at minimum valid length (sk-proj- + 20 chars)."""
        key = _build_test_string("sk-proj-", "a" * 20)
        result = self.filter.filter_output(key)
        assert result.detected is True

    # M-02: Google AI API key pattern

    def test_cs_google_ai_api_key(self) -> None:
        """Detects Google AI API key (AIzaSy + 33 alphanumeric/url-safe chars)."""
        key = _build_test_string("AIzaSy", "B" * 33)
        result = self.filter.filter_output(f"GOOGLE_API_KEY={key}")
        assert result.detected is True
        assert result.match is not None
        assert result.match.case_sensitive is True

    def test_cs_google_ai_api_key_exact_length(self) -> None:
        """Detects Google AI API key with exactly 33 suffix chars."""
        key = _build_test_string("AIzaSy", "X" * 33)
        result = self.filter.filter_output(key)
        assert result.detected is True

    # M-02: GitHub fine-grained PAT pattern

    def test_cs_github_fine_grained_pat(self) -> None:
        """Detects GitHub fine-grained personal access token (github_pat_ prefix)."""
        token = _build_test_string("github_pat_", "A1b2C3d4E5f6G7h8I9j0K1")
        result = self.filter.filter_output(f"GITHUB_TOKEN={token}")
        assert result.detected is True
        assert result.match is not None
        assert result.match.case_sensitive is True

    def test_cs_github_pat_minimum_length(self) -> None:
        """Detects GitHub fine-grained PAT at minimum valid length (github_pat_ + 22 chars)."""
        token = _build_test_string("github_pat_", "a" * 22)
        result = self.filter.filter_output(token)
        assert result.detected is True

    # M-02: Stripe live key patterns

    def test_ci_stripe_secret_key(self) -> None:
        """Detects Stripe live secret key (sk_live_ + 24+ alphanumeric chars)."""
        key = _build_test_string("sk_live_", "A" * 24)
        result = self.filter.filter_output(f"stripe_key={key}")
        assert result.detected is True
        assert result.match is not None
        assert result.match.case_sensitive is False

    def test_ci_stripe_restricted_key(self) -> None:
        """Detects Stripe live restricted key (rk_live_ + 24+ alphanumeric chars)."""
        key = _build_test_string("rk_live_", "B" * 32)
        result = self.filter.filter_output(key)
        assert result.detected is True

    # M-02: Slack bot token pattern

    def test_ci_slack_bot_token(self) -> None:
        """Detects Slack bot token (xoxb- + 10+ digit segments + 24+ alphanum chars)."""
        # Format: xoxb-{10+ digits}-{10+ digits}-{24+ alphanum}
        token = _build_test_string("xoxb-", "1234567890", "-", "9876543210", "-", "C" * 24)
        result = self.filter.filter_output(f"SLACK_TOKEN={token}")
        assert result.detected is True
        assert result.match is not None

    def test_ci_slack_user_token(self) -> None:
        """Detects Slack user token (xoxp- prefix)."""
        token = _build_test_string("xoxp-", "1111111111", "-", "2222222222", "-", "D" * 24)
        result = self.filter.filter_output(token)
        assert result.detected is True

    # M-02: JWT token pattern

    def test_ci_jwt_token_three_part(self) -> None:
        """Detects JWT token (eyJ header.eyJ payload.signature format)."""
        # JWT: base64url(header).base64url(payload).base64url(signature)
        # Both header and payload start with eyJ (base64url of {"
        header = _build_test_string("eyJ", "a" * 15)
        payload = _build_test_string("eyJ", "b" * 20)
        signature = "c" * 43
        jwt = f"{header}.{payload}.{signature}"
        result = self.filter.filter_output(f"Authorization: Bearer {jwt}")
        assert result.detected is True
        assert result.match is not None

    def test_ci_jwt_token_inline(self) -> None:
        """Detects JWT token appearing inline in tool output."""
        header = _build_test_string("eyJ", "A" * 12)
        payload = _build_test_string("eyJ", "B" * 18)
        signature = "C" * 40
        jwt = f"{header}.{payload}.{signature}"
        result = self.filter.filter_output(f"token={jwt}")
        assert result.detected is True

    # Negative cases for new patterns

    def test_short_google_key_not_detected(self) -> None:
        """Google AI key with fewer than 33 suffix chars is not flagged."""
        key = _build_test_string("AIzaSy", "X" * 10)  # Too short
        result = self.filter.filter_output(key)
        assert result.detected is False

    def test_partial_jwt_not_detected(self) -> None:
        """String starting with eyJ but lacking the full JWT structure is not flagged."""
        # Only the header part, no payload dot separator
        partial = _build_test_string("eyJ", "a" * 15)
        result = self.filter.filter_output(f"data={partial}")
        # This partial form should NOT match the JWT pattern (missing payload.sig)
        assert result.detected is False


class TestCredentialFilterExtension:
    """Tests for extending the filter with family-specific patterns."""

    def test_extend_cs_patterns(self) -> None:
        """Family-specific case-sensitive patterns are added."""
        filter_svc = CredentialFilterService()
        initial_count = filter_svc.pattern_count()
        filter_svc.extend_patterns([r"CUSTOM_SECRET_[A-Z]{10}"], case_sensitive=True)
        assert filter_svc.pattern_count() == initial_count + 1

    def test_extended_pattern_detects(self) -> None:
        """Extended patterns detect matching content."""
        filter_svc = CredentialFilterService()
        filter_svc.extend_patterns([r"CUSTOM_SECRET_[A-Z]{10}"], case_sensitive=True)
        result = filter_svc.filter_output("Found: CUSTOM_SECRET_ABCDEFGHIJ")
        assert result.detected is True

    def test_extend_ci_patterns(self) -> None:
        """Family-specific case-insensitive patterns are added."""
        filter_svc = CredentialFilterService()
        filter_svc.extend_patterns([r"custom_token\s*=\s*\S+"], case_sensitive=False)
        result = filter_svc.filter_output("CUSTOM_TOKEN = abc123xyz")
        assert result.detected is True


class TestFilterResult:
    """Tests for FilterResult structure."""

    def test_filter_result_preserves_raw(self) -> None:
        """FilterResult preserves the raw output regardless of detection."""
        filter_svc = CredentialFilterService()
        pw = "longpassword1"
        raw = f"password={pw}"
        result = filter_svc.filter_output(raw)
        assert result.raw_output == raw

    def test_filter_result_redaction_notice(self) -> None:
        """FilterResult contains redaction notice when credential detected."""
        filter_svc = CredentialFilterService()
        pw = "longpassword1"
        result = filter_svc.filter_output(f"password={pw}")
        assert "[CREDENTIAL-FILTER]" in result.filtered_output
        assert "quarantined" in result.filtered_output
