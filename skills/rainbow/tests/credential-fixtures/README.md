# Credential Filter Canary Test Fixtures

> Test fixtures for validating the Rainbow credential filter pipeline (AC-F-05, AC-F-05a).

## Document Sections

| Section | Purpose |
|---------|---------|
| [Overview](#overview) | What these fixtures test |
| [Generation](#generation) | How to create the fixture files |
| [Categories](#categories) | The 7 fixture categories |
| [Acceptance Criteria](#acceptance-criteria) | Pass/fail requirements |

---

## Overview

This directory contains canary test fixtures -- files with obviously fake credential-format strings that the credential filter MUST detect. Each of the 7 credential categories has its own subdirectory with a `canary.txt` file.

**IMPORTANT:** The canary fixture files contain strings that match credential patterns by design. The development-time secret detection hook (pre-tool-use) will block direct creation of these files through Claude Code. This is correct behavior -- it demonstrates defense-in-depth working at the authoring layer.

Fixture files MUST be generated using the provided generator script, which assembles credential-format test strings programmatically.

---

## Generation

Generate all 7 canary fixture files:

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

| # | Directory | Category | Min Entries | L1 Patterns Tested |
|---|-----------|----------|-------------|-------------------|
| 1 | `aws-key/` | AWS credentials | 3 | Access key ID, secret key, STS token |
| 2 | `api-token/` | API tokens and keys | 3 | GitHub PAT, Slack token, Bearer token |
| 3 | `ssh-key/` | SSH/TLS private keys | 3 | RSA key header, EC key header, encrypted key |
| 4 | `ntlm-hash/` | NTLM hashes | 3 | LM:NT pair, NT hash, SAM dump format |
| 5 | `kerberos/` | Kerberos material | 3 | krbtgt ref, ticket base64, Kerberoast hash |
| 6 | `connection-string/` | Connection strings | 3 | Generic DB, URI-format, JDBC |
| 7 | `plaintext-password/` | Plaintext passwords | 3 | Password label, Passwd label, Credential label |

Each fixture also includes:
- At least one base64-encoded variant (for L1 decode-and-rescan testing)
- At least one multi-line variant (for sliding window testing)

---

## Acceptance Criteria

- **AC-F-05:** Credential filter detects 100% of canary fixtures across all 7 categories; fail-closed on crash
- **AC-F-05a:** L1 regex alone detects 100% of canary fixtures (fallback if L2/L3 deferred per IR-1)
- No fixture may be added to the entropy allowlist
- Detection must complete within 5 seconds per fixture file
- All canary values are obviously fake (use AWS documentation example keys, zero-filled tokens, etc.)
