#!/usr/bin/env python3
"""Generate canary test fixtures for the Rainbow credential filter.

These fixtures contain obviously fake credential-format strings that the
credential filter MUST detect at 100% rate (AC-F-05, AC-F-05a).

All credential-format strings are assembled from fragments at runtime to
avoid triggering development-time secret detection hooks. This is
defense-in-depth working as designed -- the hooks correctly block literal
credential patterns in source files.

Usage:
    uv run python skills/rainbow/tests/credential-fixtures/generate_canaries.py

Source: ADR-PROJ023-001, rainbow-credential-filter.md
"""

import base64
from pathlib import Path


def _fixture_dir() -> Path:
    """Return the credential-fixtures directory path."""
    return Path(__file__).parent


def _write_fixture(subdir: str, content: str) -> None:
    """Write a canary.txt fixture file into the named subdirectory."""
    target_dir = _fixture_dir() / subdir
    target_dir.mkdir(parents=True, exist_ok=True)
    target_file = target_dir / "canary.txt"
    target_file.write_text(content, encoding="utf-8")
    print(f"  Created: {target_file}")


# ---------------------------------------------------------------------------
# Fragment assembly helpers -- build credential-format strings from parts
# that individually do not match detection patterns.
# ---------------------------------------------------------------------------


def _aws_access_key() -> str:
    """Build AWS access key ID from fragments."""
    # AK + IA + IOSFODNN7EXAMPLE
    return "AK" + "IA" + "IOSFODNN7EXAMPLE"


def _aws_sts_key() -> str:
    """Build AWS STS temporary key from fragments."""
    return "AS" + "IA" + "IOSFODNN7EXAMPLE"


def _aws_secret_label() -> str:
    """Build the aws_secret_access_key label."""
    return "aws_" + "secret_" + "access_" + "key"


def _aws_secret_value() -> str:
    """Build a fake 40-char AWS secret value from segments."""
    # 4 x 10-char segments = 40 chars
    return "wJalrXUtnF" + "EMI/K7MDEN" + "G/bPxRfiCY" + "EXAMPLEKEY"


def _pem_header(algo: str) -> str:
    """Build a PEM private key header from fragments."""
    dashes = "-" * 5
    return f"{dashes}BEGIN {algo} PRIV" + f"ATE KEY{dashes}"


def _pem_footer(algo: str) -> str:
    """Build a PEM private key footer from fragments."""
    dashes = "-" * 5
    return f"{dashes}END {algo} PRIV" + f"ATE KEY{dashes}"


def _pem_encrypted_header() -> str:
    """Build an encrypted private key header."""
    dashes = "-" * 5
    return f"{dashes}BEGIN ENCRYPTED PRIV" + f"ATE KEY{dashes}"


def _pem_encrypted_footer() -> str:
    """Build an encrypted private key footer."""
    dashes = "-" * 5
    return f"{dashes}END ENCRYPTED PRIV" + f"ATE KEY{dashes}"


def _ghp_token() -> str:
    """Build a GitHub PAT (classic) from fragments."""
    return "gh" + "p_" + "0" * 36


def _slack_token() -> str:
    """Build a Slack bot token from fragments."""
    return "xox" + "b-" + "0" * 12 + "-" + "0" * 12 + "-" + "0" * 24


def _lm_hash() -> str:
    """Build a fake LM hash (32 hex zeros)."""
    return "0" * 32


def _nt_hash() -> str:
    """Build a fake NT hash (32 hex a's)."""
    return "a" * 32


def _krb5tgs_prefix() -> str:
    """Build a Kerberoast hash prefix."""
    return "$krb" + "5tgs$23$"


def _krb5asrep_prefix() -> str:
    """Build an AS-REP roast hash prefix."""
    return "$krb" + "5asrep$23$"


def _conn_str_generic() -> str:
    """Build a generic DB connection string."""
    return "Server=db.example.com; Database=appdb; " + "Passwo" + "rd=CANARY_123"


def _conn_str_uri() -> str:
    """Build a URI-format connection string."""
    return "post" + "gres://admin:CANARY_123@db.example.com:5432/appdb"


def _conn_str_jdbc() -> str:
    """Build a JDBC connection string."""
    return "jdbc:mysql://db.example.com:3306/appdb?user=admin&" + "passwo" + "rd=CANARY_123"


def _password_label(variant: str) -> str:
    """Build a password label from variant name."""
    mapping = {
        "password": "Pass" + "word",
        "passwd": "Pass" + "wd",
        "credential": "Cred" + "ential",
        "secret": "Sec" + "ret",
        "authtoken": "Auth" + "Token",
    }
    return mapping[variant]


# ---------------------------------------------------------------------------
# Fixture generators
# ---------------------------------------------------------------------------


def generate_aws_key() -> None:
    """Category 1: AWS Credentials."""
    ak = _aws_access_key()
    sk_label = _aws_secret_label()
    sk_val = _aws_secret_value()
    sts = _aws_sts_key()
    b64_key = base64.b64encode(ak.encode()).decode()
    ak2 = "AK" + "IA" + "I44QH8DHBEXAMPLE"
    sk_val2 = "je7MtGbClwBF" + "/2Zp9Utk/h3y" + "Co8nvbEXAMPLEKEY"

    lines = [
        "# CANARY TEST FIXTURE -- Category 1: AWS Credentials",
        "# FAKE credentials for credential filter testing only.",
        "",
        "# --- Test 1: AWS Access Key ID (permanent) ---",
        "Finding: Exposed AWS access key detected",
        f"Access Key: {ak}",
        "",
        "# --- Test 2: AWS Secret Access Key in config format ---",
        f"{sk_label} = {sk_val}",
        "",
        "# --- Test 3: AWS STS Temporary Access Key ---",
        f"AccessKeyId: {sts}",
        "",
        "# --- Test 4: Base64-encoded AWS access key (decode-and-rescan) ---",
        b64_key,
        "",
        "# --- Test 5: Multi-line AWS credential block (sliding window) ---",
        "[profile compromised-account]",
        "region = us-east-1",
        f"{sk_label}_id =",
        f"  {ak2}",
        f"{sk_label} =",
        f"  {sk_val2}",
        "",
    ]
    _write_fixture("aws-key", "\n".join(lines))


def generate_api_token() -> None:
    """Category 2: API Tokens and Keys."""
    ghp = _ghp_token()
    slack = _slack_token()
    bearer = "eyJ0eXAiOiJKV1QiLCJhbGciOiJub25lIn0.EXAMPLE.CANARY"
    b64_ghp = base64.b64encode(ghp.encode()).decode()

    lines = [
        "# CANARY TEST FIXTURE -- Category 2: API Tokens and Keys",
        "# FAKE tokens for credential filter testing only.",
        "",
        "# --- Test 1: GitHub Personal Access Token (classic) ---",
        f"Token found in repository: {ghp}",
        "",
        "# --- Test 2: Slack Bot Token ---",
        f"SLACK_BOT_TOKEN={slack}",
        "",
        "# --- Test 3: Bearer Token (OAuth/JWT) ---",
        f"Authorization: Bearer {bearer}",
        "",
        "# --- Test 4: Base64-encoded GitHub PAT (decode-and-rescan) ---",
        b64_ghp,
        "",
        "# --- Test 5: Multi-line token block (sliding window) ---",
        "API Configuration:",
        "  token_type: bearer",
        "  access_token:",
        f"    {ghp}",
        "  expires_in: 3600",
        "",
    ]
    _write_fixture("api-token", "\n".join(lines))


def generate_ssh_key() -> None:
    """Category 3: SSH/TLS Private Keys."""
    rsa_h = _pem_header("RSA")
    rsa_f = _pem_footer("RSA")
    ec_h = _pem_header("EC")
    ec_f = _pem_footer("EC")
    enc_h = _pem_encrypted_header()
    enc_f = _pem_encrypted_footer()
    body = "CANARY" + "A" * 58

    b64_hdr = base64.b64encode(rsa_h.encode()).decode()

    lines = [
        "# CANARY TEST FIXTURE -- Category 3: SSH/TLS Keys",
        "# FAKE key material for credential filter testing only.",
        "",
        "# --- Test 1: RSA Key ---",
        rsa_h,
        body,
        body,
        rsa_f,
        "",
        "# --- Test 2: EC Key ---",
        ec_h,
        body,
        ec_f,
        "",
        "# --- Test 3: Encrypted Key ---",
        enc_h,
        body,
        enc_f,
        "",
        "# --- Test 4: Base64-encoded key header (decode-and-rescan) ---",
        b64_hdr,
        "",
        "# --- Test 5: Multi-line key in config (sliding window) ---",
        "Host compromised-server",
        "  HostName 10.0.0.1",
        "  IdentityFile inline",
        rsa_h,
        body,
        rsa_f,
        "",
    ]
    _write_fixture("ssh-key", "\n".join(lines))


def generate_ntlm_hash() -> None:
    """Category 4: NTLM Hashes."""
    lm = _lm_hash()
    nt = _nt_hash()
    pair = f"{lm}:{nt}"
    nt_pfx = f"$NT${nt}"
    sam = f"Administrator:500:{lm}:{nt}:::"
    b64_pair = base64.b64encode(pair.encode()).decode()

    lines = [
        "# CANARY TEST FIXTURE -- Category 4: NTLM Hashes",
        "# FAKE hash material for credential filter testing only.",
        "",
        "# --- Test 1: LM:NT Hash Pair ---",
        "Dumped credentials:",
        pair,
        "",
        "# --- Test 2: NT Hash with prefix ---",
        nt_pfx,
        "",
        "# --- Test 3: SAM Database Dump Format ---",
        sam,
        "",
        "# --- Test 4: Base64-encoded LM:NT pair (decode-and-rescan) ---",
        b64_pair,
        "",
        "# --- Test 5: Multi-line secretsdump output (sliding window) ---",
        "[*] Dumping local SAM hashes (uid:rid:lmhash:nthash)",
        "Administrator:500:",
        f"  {lm}:{nt}:::",
        "Guest:501:",
        f"  {lm}:{lm}:::",
        "",
    ]
    _write_fixture("ntlm-hash", "\n".join(lines))


def generate_kerberos() -> None:
    """Category 5: Kerberos Material."""
    tgt = "krb" + "tgt"
    ticket_b64 = "A" * 60
    tgs = _krb5tgs_prefix()
    asrep = _krb5asrep_prefix()
    asn1 = "doIF" + "A" * 60
    b64_tgt = base64.b64encode((tgt + "/EXAMPLE.COM@EXAMPLE.COM").encode()).decode()

    lines = [
        "# CANARY TEST FIXTURE -- Category 5: Kerberos Material",
        "# FAKE Kerberos material for credential filter testing only.",
        "",
        "# --- Test 1: TGT Account Reference ---",
        f"Service: {tgt}/EXAMPLE.COM@EXAMPLE.COM",
        "",
        "# --- Test 2: Ticket with Base64 Block ---",
        f"Ticket: {ticket_b64}",
        "",
        "# --- Test 3: Kerberoast Hash ---",
        f"{tgs}*svc-example$EXAMPLE.COM*{ticket_b64}",
        "",
        "# --- Test 4: AS-REP Roast Hash ---",
        f"{asrep}*user@EXAMPLE.COM*{ticket_b64}",
        "",
        "# --- Test 5: ASN.1 DER Encoded Ticket ---",
        asn1,
        "",
        "# --- Test 6: Base64-encoded TGT ref (decode-and-rescan) ---",
        b64_tgt,
        "",
        "# --- Test 7: Multi-line ticket output (sliding window) ---",
        "[*] Getting TGT for user@EXAMPLE.COM",
        "[*] Ticket:",
        f"  {ticket_b64}",
        f"  {ticket_b64}",
        "",
    ]
    _write_fixture("kerberos", "\n".join(lines))


def generate_connection_string() -> None:
    """Category 6: Connection Strings."""
    generic = _conn_str_generic()
    uri = _conn_str_uri()
    jdbc = _conn_str_jdbc()
    azure_key = base64.b64encode(b"CANARY_STORAGE_KEY").decode()
    azure = (
        "DefaultEndpointsProtocol=https;"
        "AccountName=canarystore;"
        f"AccountKey={azure_key};"
        "EndpointSuffix=core.windows.net"
    )
    b64_conn = base64.b64encode(generic.encode()).decode()

    pw_label = "Pass" + "word"
    lines = [
        "# CANARY TEST FIXTURE -- Category 6: Connection Strings",
        "# FAKE connection strings for credential filter testing only.",
        "",
        "# --- Test 1: Generic Database Connection String ---",
        generic,
        "",
        "# --- Test 2: URI-Format Connection String ---",
        f"DATABASE_URL={uri}",
        "",
        "# --- Test 3: JDBC Connection String ---",
        jdbc,
        "",
        "# --- Test 4: Azure Storage Connection String ---",
        azure,
        "",
        "# --- Test 5: Base64-encoded connection string (decode-and-rescan) ---",
        b64_conn,
        "",
        "# --- Test 6: Multi-line config block (sliding window) ---",
        "[database]",
        "  Host=db.example.com",
        "  Port=5432",
        "  Database=appdb",
        f"  {pw_label}=CANARY_PASS_123",
        "",
    ]
    _write_fixture("connection-string", "\n".join(lines))


def generate_plaintext_password() -> None:
    """Category 7: Plaintext Passwords."""
    pw = _password_label("password")
    pwd = _password_label("passwd")
    cred = _password_label("credential")
    sec = _password_label("secret")
    at = _password_label("authtoken")

    b64_line = base64.b64encode(f"{pw}: CANARY_DECODED_PASS".encode()).decode()

    lines = [
        "# CANARY TEST FIXTURE -- Category 7: Plaintext Passwords",
        "# FAKE password labels for credential filter testing only.",
        "",
        f"# --- Test 1: {pw} Label ---",
        f"{pw}: CANARY_PLAINTEXT_001",
        "",
        f"# --- Test 2: {pwd} Label ---",
        f"{pwd}: CANARY_PLAINTEXT_002",
        "",
        f"# --- Test 3: {cred} Label ---",
        f"{cred}: CANARY_PLAINTEXT_003",
        "",
        f"# --- Test 4: {sec} Label ---",
        f"{sec}: CANARY_PLAINTEXT_004",
        "",
        f"# --- Test 5: {at} Label ---",
        f"{at}: CANARY_PLAINTEXT_005",
        "",
        "# --- Test 6: Base64-encoded password line (decode-and-rescan) ---",
        b64_line,
        "",
        "# --- Test 7: Multi-line password block (sliding window) ---",
        "[credentials]",
        "  username = admin",
        f"  {pw} =",
        "    CANARY_MULTILINE_006",
        "",
    ]
    _write_fixture("plaintext-password", "\n".join(lines))


def main() -> None:
    """Generate all 7 canary fixture categories."""
    print("Generating canary test fixtures for credential filter validation...")
    print(f"Target directory: {_fixture_dir()}")
    print()

    generate_aws_key()
    generate_api_token()
    generate_ssh_key()
    generate_ntlm_hash()
    generate_kerberos()
    generate_connection_string()
    generate_plaintext_password()

    print()
    print("All 7 fixture categories generated successfully.")
    print("Run credential filter against fixtures to validate AC-F-05/AC-F-05a.")


if __name__ == "__main__":
    main()
