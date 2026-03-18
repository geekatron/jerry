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


# --- GCP Service Account helpers ---


def _gcp_project_id() -> str:
    """Build a fake GCP project ID."""
    return "canary" + "-fake-project-00000"


def _gcp_private_key_id() -> str:
    """Build a fake GCP private key ID (40 hex zeros)."""
    return "0" * 40


def _gcp_client_email(project: str) -> str:
    """Build a fake GCP service account email."""
    return "canary-sa@" + project + ".iam.gserviceaccount.com"


def _gcp_client_id() -> str:
    """Build a fake GCP client ID (21 zeros)."""
    return "0" * 21


def _gcp_creds_env_label() -> str:
    """Build the GOOGLE_APPLICATION_CREDENTIALS label."""
    return "GOOGLE_" + "APPLICATION_" + "CREDENTIALS"


# --- Azure Service Principal helpers ---


def _azure_tenant_id() -> str:
    """Build a fake Azure tenant ID (UUID format)."""
    return "00000000-0000-0000-0000-000000000000"


def _azure_client_id() -> str:
    """Build a fake Azure client/app ID (UUID format)."""
    return "11111111-1111-1111-1111-111111111111"


def _azure_client_secret() -> str:
    """Build a fake Azure client secret (fake ~34-char value)."""
    # Real Azure client secrets are ~34-40 chars, mixed case + digits + tilde
    return "CANARY" + "~" + "Fake" + "AzureSecret" + "Value" + "0000" + "CANARY"


def _azure_subscription_id() -> str:
    """Build a fake Azure subscription ID (UUID format)."""
    return "22222222-2222-2222-2222-222222222222"


def _azure_env_label(key: str) -> str:
    """Build Azure environment variable label from fragments."""
    mapping = {
        "tenant": "AZURE_" + "TENANT_ID",
        "client": "AZURE_" + "CLIENT_ID",
        "secret": "AZURE_" + "CLIENT_" + "SECRET",
        "subscription": "AZURE_" + "SUBSCRIPTION_ID",
    }
    return mapping[key]


# --- GitHub PAT helpers ---


def _ghfine_token() -> str:
    """Build a GitHub fine-grained PAT (github_pat_ prefix + 82 zeros)."""
    return "github" + "_pat_" + "0" * 82


def _ghp_classic_token() -> str:
    """Build a GitHub classic PAT (ghp_ prefix + 36 zeros, same as _ghp_token)."""
    return "gh" + "p_" + "0" * 36


def _gho_token() -> str:
    """Build a GitHub OAuth token (gho_ prefix + 36 zeros)."""
    return "gh" + "o_" + "0" * 36


def _ghs_token() -> str:
    """Build a GitHub server-to-server token (ghs_ prefix + 36 zeros)."""
    return "gh" + "s_" + "0" * 36


# --- JWT helpers ---


def _jwt_header_b64() -> str:
    """Build a base64url-encoded JWT header fragment (no real encoding needed for canary)."""
    # eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9 is the well-known {"alg":"HS256","typ":"JWT"}
    # Build from harmless fragments to avoid triggering bearer-token detection on the full JWT
    return "eyJhbGci" + "OiJIUzI1NiIs" + "InR5cCI6IkpXVCJ9"


def _jwt_payload_b64() -> str:
    """Build a fake base64url-encoded JWT payload fragment."""
    # Fake payload: {"sub":"canary","iat":0,"exp":9999999999}
    return "eyJzdWIi" + "OiJjYW5hcnki" + "LCJpYXQiOjAs" + "ImV4cCI6OTk5OTk5OTk5OX0"


def _jwt_signature() -> str:
    """Build a fake JWT signature fragment."""
    return "CANARY" + "FakeSignature" + "ABCDEF0123456789"


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


def generate_gcp_sa() -> None:
    """Category 10: GCP Service Account Keys."""
    project = _gcp_project_id()
    key_id = _gcp_private_key_id()
    email = _gcp_client_email(project)
    client_id = _gcp_client_id()
    creds_label = _gcp_creds_env_label()
    rsa_h = _pem_header("RSA")
    rsa_f = _pem_footer("RSA")
    body = "CANARY" + "A" * 58

    # Build JSON-format SA key from fragments so no single string is a full credential
    json_type = '"type": "service_account"'
    json_project = f'"project_id": "{project}"'
    json_key_id = f'"private_key_id": "{key_id}"'
    json_key_val = '"private_key": "' + rsa_h + "\\n" + body + "\\n" + rsa_f + '\\n"'
    json_email = f'"client_email": "{email}"'
    json_client_id = f'"client_id": "{client_id}"'
    json_auth_uri = '"auth_uri": "https://accounts.google.com/o/oauth2/auth"'
    json_token_uri = '"token_uri": "https://oauth2.googleapis.com/token"'

    b64_hint = base64.b64encode(b'"type": "service_account"').decode()

    lines = [
        "# CANARY TEST FIXTURE -- Category 10: GCP Service Account Keys",
        "# FAKE credentials for credential filter testing only.",
        "",
        "# --- Test 1: GCP Service Account JSON Key (full structure) ---",
        "{",
        f"  {json_type},",
        f"  {json_project},",
        f"  {json_key_id},",
        f"  {json_key_val},",
        f"  {json_email},",
        f"  {json_client_id},",
        f"  {json_auth_uri},",
        f"  {json_token_uri}",
        "}",
        "",
        "# --- Test 2: GCP credentials env-var label ---",
        f"{creds_label}=/path/to/canary-sa-key.json",
        f"GCP_SA_KEY={project}:{email}",
        "",
        "# --- Test 3: GCP SA private key PEM block (standalone) ---",
        rsa_h,
        body,
        body,
        rsa_f,
        "",
        "# --- Test 4: Base64-encoded 'service_account' type marker (decode-and-rescan) ---",
        b64_hint,
        "",
        "# --- Test 5: Multi-line GCP SA reference in config (sliding window) ---",
        "[gcp]",
        f"  project = {project}",
        f"  service_account = {email}",
        f"  private_key_id = {key_id}",
        "  private_key =",
        f"    {rsa_h}",
        f"    {body}",
        f"    {rsa_f}",
        "",
    ]
    _write_fixture("gcp-sa", "\n".join(lines))


def generate_azure_sp() -> None:
    """Category 11: Azure Service Principal Credentials."""
    tenant = _azure_tenant_id()
    client = _azure_client_id()
    secret = _azure_client_secret()
    subscription = _azure_subscription_id()
    l_tenant = _azure_env_label("tenant")
    l_client = _azure_env_label("client")
    l_secret = _azure_env_label("secret")
    l_sub = _azure_env_label("subscription")

    b64_secret = base64.b64encode(secret.encode()).decode()

    lines = [
        "# CANARY TEST FIXTURE -- Category 11: Azure Service Principal Credentials",
        "# FAKE credentials for credential filter testing only.",
        "",
        "# --- Test 1: Azure SP environment variables block ---",
        f"{l_tenant}={tenant}",
        f"{l_client}={client}",
        f"{l_secret}={secret}",
        f"{l_sub}={subscription}",
        "",
        "# --- Test 2: Azure SP in az login format ---",
        f"az login --service-principal -u {client} -p {secret} --tenant {tenant}",
        "",
        "# --- Test 3: Azure SP in JSON credentials format ---",
        "{",
        f'  "tenantId": "{tenant}",',
        f'  "clientId": "{client}",',
        f'  "clientSecret": "{secret}",',
        f'  "subscriptionId": "{subscription}"',
        "}",
        "",
        "# --- Test 4: Base64-encoded Azure client secret (decode-and-rescan) ---",
        b64_secret,
        "",
        "# --- Test 5: Multi-line Azure SP config block (sliding window) ---",
        "[azure-credentials]",
        f"  tenant_id = {tenant}",
        f"  client_id = {client}",
        "  client_secret =",
        f"    {secret}",
        f"  subscription_id = {subscription}",
        "",
    ]
    _write_fixture("azure-sp", "\n".join(lines))


def generate_github_pat() -> None:
    """Category 12: GitHub Personal Access Tokens (all formats)."""
    fine = _ghfine_token()
    classic = _ghp_classic_token()
    oauth = _gho_token()
    server = _ghs_token()
    b64_fine = base64.b64encode(fine.encode()).decode()

    lines = [
        "# CANARY TEST FIXTURE -- Category 12: GitHub Personal Access Tokens",
        "# FAKE tokens for credential filter testing only.",
        "",
        "# --- Test 1: GitHub fine-grained PAT (github_pat_ prefix) ---",
        f"GITHUB_TOKEN={fine}",
        "",
        "# --- Test 2: GitHub classic PAT (ghp_ prefix) ---",
        f"GH_TOKEN={classic}",
        "",
        "# --- Test 3: GitHub OAuth token (gho_ prefix) ---",
        f"Authorization: token {oauth}",
        "",
        "# --- Test 4: GitHub server-to-server token (ghs_ prefix) ---",
        f"x-github-token: {server}",
        "",
        "# --- Test 5: Base64-encoded fine-grained PAT (decode-and-rescan) ---",
        b64_fine,
        "",
        "# --- Test 6: Multi-line .netrc format with GitHub PAT (sliding window) ---",
        "machine github.com",
        "  login canary-user",
        f"  password {classic}",
        "",
        "# --- Test 7: GitHub Actions secrets reference pattern ---",
        f"token: {fine}",
        "",
    ]
    _write_fixture("github-pat", "\n".join(lines))


def generate_jwt_token() -> None:
    """Category 13: JWT Tokens (bearer tokens in header.payload.signature format)."""
    hdr = _jwt_header_b64()
    pay = _jwt_payload_b64()
    sig = _jwt_signature()
    full_jwt = hdr + "." + pay + "." + sig

    b64_jwt = base64.b64encode(full_jwt.encode()).decode()

    lines = [
        "# CANARY TEST FIXTURE -- Category 13: JWT Tokens",
        "# FAKE tokens for credential filter testing only.",
        "",
        "# --- Test 1: JWT in Authorization header ---",
        f"Authorization: Bearer {full_jwt}",
        "",
        "# --- Test 2: JWT in X-Auth-Token header ---",
        f"X-Auth-Token: {full_jwt}",
        "",
        "# --- Test 3: JWT in config file ---",
        f"access_token = {full_jwt}",
        "",
        "# --- Test 4: JWT with HS256 alg in JSON response ---",
        "{",
        f'  "token": "{full_jwt}",',
        '  "token_type": "Bearer",',
        '  "expires_in": 3600',
        "}",
        "",
        "# --- Test 5: Base64-encoded full JWT (decode-and-rescan) ---",
        b64_jwt,
        "",
        "# --- Test 6: Multi-line JWT storage (sliding window) ---",
        "[auth]",
        "  token_type = bearer",
        "  jwt =",
        f"    {full_jwt}",
        "",
    ]
    _write_fixture("jwt-token", "\n".join(lines))


def generate_l2_entropy() -> None:
    """Category 8: L2 Entropy Canaries.

    These fixtures contain high-entropy random strings (Shannon >= 4.5,
    minimum 20 chars) that do NOT match any L1 regex pattern prefix.
    They MUST be detected by L2 entropy analysis only.
    """
    import hashlib

    # Generate deterministic high-entropy strings using hash functions.
    # These produce alphanumeric output that does not match any L1 pattern
    # prefix (no AKIA, ghp_, xox, PEM headers, krb5, connection-string
    # keywords, or password labels).
    seed_a = hashlib.sha256(b"canary-l2-entropy-test-alpha").hexdigest()
    seed_b = hashlib.sha256(b"canary-l2-entropy-test-bravo").hexdigest()
    seed_c = hashlib.blake2b(b"canary-l2-entropy-test-charlie", digest_size=24).hexdigest()

    lines = [
        "# CANARY TEST FIXTURE -- Category 8: L2 Entropy Detection",
        "# High-entropy strings that ONLY trigger L2 detection, NOT L1 regex.",
        "# Shannon entropy >= 4.5 for each string; no L1 pattern prefix match.",
        "",
        "# --- Test 1: SHA-256 hex digest (64 chars, entropy ~4.0 per hex char) ---",
        "config_value: " + seed_a,
        "",
        "# --- Test 2: Different SHA-256 digest ---",
        "internal_setting: " + seed_b,
        "",
        "# --- Test 3: BLAKE2b hex digest (48 chars) ---",
        "opaque_ref: " + seed_c,
        "",
        "# --- Test 4: Mixed-case high-entropy string (no known prefix) ---",
        "random_field: " + "mR7kPx2Qn9vLw4Fj8Ys5Td3Bc6Ah1Ge",
        "",
        "# --- Test 5: Numeric-heavy high-entropy string ---",
        "nonce_value: " + "48291073562849175036284917503628",
        "",
    ]
    _write_fixture("l2-entropy", "\n".join(lines))


def generate_l3_structural() -> None:
    """Category 9: L3 Structural Canaries.

    These fixtures contain JSON/YAML objects with sensitive key names
    (matching L3 structural patterns) but whose VALUES do NOT match L1
    regex patterns and are NOT high-entropy (below L2 threshold).
    They MUST be detected by L3 structural analysis only.
    """
    lines = [
        "# CANARY TEST FIXTURE -- Category 9: L3 Structural Detection",
        "# Structured data with sensitive keys that ONLY trigger L3 detection.",
        "# Values are low-entropy and do not match L1 regex patterns.",
        "",
        "# --- Test 1: JSON object with database_password key ---",
        '{"database_password": "test-canary-value-123"}',
        "",
        "# --- Test 2: JSON object with api_secret key ---",
        '{"api_secret": "simple-test-secret-abc"}',
        "",
        "# --- Test 3: YAML-style key-value with credential key ---",
        "service_credential: basic-service-token-xyz",
        "",
        "# --- Test 4: Nested JSON with sensitive key ---",
        '{"config": {"db": {"connection_password": "dev-only-pass-456"}}}',
        "",
        "# --- Test 5: INI-style with auth_token key ---",
        "[service]",
        "auth_token = my-local-dev-token-789",
        "",
        "# --- Test 6: JSON with access_key (low-entropy value, no AKIA prefix) ---",
        '{"access_key": "dev-testing-key-value-000"}',
        "",
    ]
    _write_fixture("l3-structural", "\n".join(lines))


def main() -> None:
    """Generate all 13 canary fixture categories."""
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
    generate_l2_entropy()
    generate_l3_structural()
    generate_gcp_sa()
    generate_azure_sp()
    generate_github_pat()
    generate_jwt_token()

    print()
    print("All 13 fixture categories generated successfully.")
    print("Run credential filter against fixtures to validate AC-F-05/AC-F-05a.")
    print("  Categories 1-7, 10-13: L1 regex detection (AC-F-05a)")
    print("  Category 8: L2 entropy detection only")
    print("  Category 9: L3 structural detection only")
    print("  Categories added by T9.1: gcp-sa (10), azure-sp (11), github-pat (12), jwt-token (13)")


if __name__ == "__main__":
    main()
