# Credential Filter Canary Test Fixtures

> Test fixtures for validating the Rainbow credential filter pipeline (AC-F-05, AC-F-05a).

## Document Sections

| Section | Purpose |
|---------|---------|
| [Overview](#overview) | What these fixtures test |
| [Generation](#generation) | How to create the fixture files |
| [Categories](#categories) | The 13 fixture categories |
| [Acceptance Criteria](#acceptance-criteria) | Pass/fail requirements |

---

## Overview

This directory contains canary test fixtures -- files with obviously fake credential-format strings that the credential filter MUST detect. Each of the 13 credential categories has its own subdirectory with a `canary.txt` file.

**IMPORTANT:** The canary fixture files contain strings that match credential patterns by design. The development-time secret detection hook (pre-tool-use) will block direct creation of these files through Claude Code. This is correct behavior -- it demonstrates defense-in-depth working at the authoring layer.

Fixture files MUST be generated using the provided generator script, which assembles credential-format test strings programmatically from fragments that individually do not trigger detection.

---

## Generation

Generate all 13 canary fixture files:

```bash
uv run python skills/rainbow/tests/credential-fixtures/generate_canaries.py
```

This creates one `canary.txt` file in each category subdirectory.

After generation, verify all fixtures exist:

```bash
ls -la skills/rainbow/tests/credential-fixtures/*/canary.txt
```

---

## Categories

| # | Directory | Category | Min Entries | L1 Patterns Tested | Added |
|---|-----------|----------|-------------|-------------------|-------|
| 1 | `aws-key/` | AWS credentials | 3 | Access key ID, secret key, STS token | T0.8 |
| 2 | `api-token/` | API tokens and keys | 3 | GitHub PAT, Slack token, Bearer token | T0.8 |
| 3 | `ssh-key/` | SSH/TLS private keys | 3 | RSA key header, EC key header, encrypted key | T0.8 |
| 4 | `ntlm-hash/` | NTLM hashes | 3 | LM:NT pair, NT hash, SAM dump format | T0.8 |
| 5 | `kerberos/` | Kerberos material | 3 | krbtgt ref, ticket base64, Kerberoast hash | T0.8 |
| 6 | `connection-string/` | Connection strings | 3 | Generic DB, URI-format, JDBC | T0.8 |
| 7 | `plaintext-password/` | Plaintext passwords | 3 | Password label, Passwd label, Credential label | T0.8 |
| 8 | `l2-entropy/` | L2 entropy detection | 3 | High-entropy strings without L1 prefix (L2 only) | T0.8 |
| 9 | `l3-structural/` | L3 structural detection | 3 | Sensitive key names with low-entropy values (L3 only) | T0.8 |
| 10 | `gcp-sa/` | GCP service account keys | 3 | SA JSON key, GOOGLE_APPLICATION_CREDENTIALS, PEM block | **T9.1** |
| 11 | `azure-sp/` | Azure service principal | 3 | AZURE_CLIENT_SECRET, az login, JSON credentials block | **T9.1** |
| 12 | `github-pat/` | GitHub personal access tokens | 3 | fine-grained (github_pat_), classic (ghp_), OAuth (gho_), server (ghs_) | **T9.1** |
| 13 | `jwt-token/` | JWT tokens | 3 | Authorization Bearer, X-Auth-Token, config file, JSON response | **T9.1** |

Each fixture also includes:
- At least one base64-encoded variant (for L1 decode-and-rescan testing)
- At least one multi-line variant (for sliding window testing)

**Note on categories 1-9:** These were delivered as part of T0.8. Categories 10-13 (marked T9.1) were added to align with the original ORCHESTRATION.yaml planned categories (gcp-sa, azure-sp, github-pat, jwt-token).

---

## Acceptance Criteria

- **AC-F-05:** Credential filter detects 100% of canary fixtures across all 13 categories; fail-closed on crash
- **AC-F-05a:** L1 regex alone detects 100% of canary fixtures in categories 1-7 and 10-13 (fallback if L2/L3 deferred per IR-1)
- No fixture may be added to the entropy allowlist
- Detection must complete within 5 seconds per fixture file
- All canary values are obviously fake (zero-filled tokens, CANARY-prefixed values, AWS documentation example keys)
