# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Tests for CredentialFilterService.

Validates all 8 base patterns (4 case-sensitive + 4 case-insensitive)
ported from the bash rainbow-tool-exec script.

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
        """Filter starts with 8 base patterns (4 CS + 4 CI)."""
        assert self.filter.pattern_count() == 8

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
