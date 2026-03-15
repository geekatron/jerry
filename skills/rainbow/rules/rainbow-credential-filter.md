# Rainbow Credential Filter Specification

> Mandatory pre-processing gate on ALL tool output before context window entry. Shared infrastructure across all `/rainbow` and `/blue-team` agents. Primary mitigation for RPN 280 credential cascade risk.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Purpose](#purpose) | Why the credential filter exists |
| [Execution Position](#execution-position) | Where the filter sits in the processing chain |
| [3-Layer Architecture](#3-layer-architecture) | Defense-in-depth filter pipeline |
| [L1: Regex Pattern Matching](#l1-regex-pattern-matching) | Deterministic pattern detection across 7 categories |
| [L2: Entropy-Based Detection](#l2-entropy-based-detection) | Shannon entropy analysis for novel credential formats |
| [L3: Structural Analysis](#l3-structural-analysis) | JSON/YAML key-name semantic matching |
| [Fail-Closed Behavior](#fail-closed-behavior) | What happens when detection triggers or the filter fails |
| [FMEA Decomposition](#fmea-decomposition) | Failure mode analysis with RPN scores |
| [Canary Testing Requirements](#canary-testing-requirements) | Per-tool credential fixture validation |
| [Update Cadence](#update-cadence) | When and how patterns are reviewed |
| [Configuration Files](#configuration-files) | Machine-parseable companion files |

---

## Purpose

The credential filter pipeline prevents credential material from entering the LLM context window. Any credential that reaches the context window is effectively exfiltrated -- it becomes part of the model's reasoning context and may appear in output, logs, or downstream artifacts. This is an irreversible exposure.

The filter is a **shared infrastructure component**, not owned by any single sub-skill. It applies to ALL tool output regardless of which sub-skill, agent, or security zone invoked the tool.

**Applicability:** Every agent in `/rainbow` (all 5 sub-skills) and `/blue-team` MUST route tool output through this filter before context window entry. No exceptions. No bypass mechanism exists by design.

---

## Execution Position

The credential filter operates at the adapter layer, between raw tool output and context window ingestion.

```
Tool CLI execution
        |
        v
  Raw stdout/stderr capture
        |
        v
  +---------------------------+
  | CREDENTIAL FILTER         |
  | L1: Regex patterns        |
  | L2: Entropy detection     |
  | L3: Structural analysis   |
  +---------------------------+
        |
        v
  Sanitized output
        |
        v
  Context window entry
```

**No tool output enters the context window without passing through the filter.** This is a post-tool-output, pre-context-window position enforced at the adapter layer.

---

## 3-Layer Architecture

The filter uses defense-in-depth with three complementary layers. Each layer catches what the previous layer misses.

| Layer | Mechanism | Coverage | Failure Mode | Processing Order |
|-------|-----------|----------|-------------|-----------------|
| L1 | Regex pattern matching | Known credential formats (high recall for cataloged patterns) | Misses novel or obfuscated formats | First (fastest, deterministic) |
| L2 | Entropy-based detection | Novel formats, base64-encoded secrets, binary-encoded material | False positives on legitimate high-entropy output (hashes, UUIDs) | Second (catches L1 misses) |
| L3 | Structural analysis | Structured output with semantic key names | Misses non-standard key names | Third (catches structured leaks) |

**Pipeline behavior:** All three layers execute sequentially on every tool output block. A detection at ANY layer triggers the fail-closed response. Layers do not short-circuit -- all three run to completion to maximize detection surface and to populate quarantine metadata with the detecting layer for forensic analysis.

---

## L1: Regex Pattern Matching

L1 applies deterministic regex patterns against known credential formats. Patterns are organized into 7 categories. The authoritative, machine-parseable pattern definitions are in `skills/rainbow/rules/credential-regex-patterns.yaml`.

**NOTE:** Literal credential-format examples are intentionally excluded from this markdown file to avoid triggering secret-detection hooks. All patterns, with test examples, are defined exclusively in the YAML configuration file.

### Category Summary

| # | Category | Description | Confidence | Tools Producing |
|---|----------|-------------|-----------|----------------|
| 1 | AWS credentials | Access key IDs (starting with known prefixes), secret access keys, session tokens | High | Prowler, Checkov, cloud audit tools |
| 2 | API tokens and keys | Bearer tokens, GitHub PATs (multiple generations), OpenAI keys, Slack tokens, GitLab PATs, Atlassian tokens | High-Medium | Reconnaissance tools, API enumeration |
| 3 | SSH/TLS private keys | PEM-format private key headers (RSA, EC, OPENSSH, DSA, PGP), encrypted keys, certificates | High | Impacket, reconnaissance output |
| 4 | NTLM hashes | LM:NT hash pairs, NT hash standalone, SAM database dump format | High | Impacket secretsdump, Mimikatz |
| 5 | Kerberos material | TGT references, ticket-followed-by-base64 blocks, Kerberoast/AS-REP hash formats | High-Medium | Impacket, BloodHound, Rubeus |
| 6 | Connection strings | Database connection strings with embedded passwords (generic, URI-format, JDBC, Azure, Redis) | High | Cloud audit tools, config scanners |
| 7 | Plaintext passwords | Context-dependent labels (Password/Passwd/Cred/Secret/AuthToken) followed by values | Medium | Metasploit, Empire, credential dump tools |

### L1 Supplemental: Base64 Decode-and-Rescan

For strings matching the base64 candidate pattern (20+ characters of alphanumeric plus `+/=`), L1 performs:

1. Attempt base64 decode
2. If decode succeeds, rescan the decoded content against all L1 patterns
3. If rescan detects a credential, flag the original base64 string

This mechanism addresses the highest residual FMEA risk (base64-encoded credentials, RPN 200).

### L1 Multi-Line Sliding Window

Credentials may be split across output lines (e.g., private keys, multi-line connection strings). L1 applies a sliding window of 5 lines to catch multi-line credential patterns. The window advances line-by-line through the output, concatenating window contents before pattern matching.

---

## L2: Entropy-Based Detection

L2 detects high-entropy strings that evade L1 regex patterns. Configuration is in `skills/rainbow/rules/credential-entropy-config.yaml`.

### Parameters

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| Shannon entropy threshold | > 4.5 | Balances detection sensitivity against false positive rate on legitimate tool output |
| Minimum string length | 16 characters | Strings shorter than 16 chars have insufficient entropy signal |
| Base64 rescan | Enabled | Decode base64 candidates and re-evaluate entropy of decoded content |

### Shannon Entropy Calculation

For a string S of length n with character frequencies f(c):

```
H(S) = -sum( f(c) * log2(f(c)) ) for each unique character c
```

Where f(c) = count(c) / n.

**Interpretation:**
- Entropy < 3.0: Likely natural language or repetitive content
- Entropy 3.0-4.5: Mixed content, unlikely to be random secret material
- Entropy > 4.5: High randomness, consistent with API keys, tokens, encoded secrets

### Allowlist (False Positive Suppression)

Certain high-entropy strings are legitimate tool output. The allowlist prevents false positive quarantine:

| Type | Description | Reason |
|------|-------------|--------|
| SHA-256 hash | 64-character lowercase hex string | Legitimate hash output from integrity checks |
| SHA-1 hash | 40-character lowercase hex string | Git commit hashes, file integrity checks |
| MD5 hash | 32-character lowercase hex string (when not in LM:NT context) | File integrity checks |
| UUID | Standard 8-4-4-4-12 hex-and-hyphen format | Standard UUID format |
| Hex dump | Space-separated hex byte pairs (8+ bytes) | Hex dump output from binary analysis tools |

**Allowlist precedence:** If a string matches an allowlist pattern, L2 does NOT flag it, even if its entropy exceeds 4.5. L1 regex patterns take precedence over the allowlist -- if L1 flags a string, the allowlist does not override that detection.

---

## L3: Structural Analysis

L3 analyzes structured output (JSON, YAML, XML, INI/config) for sensitive key-value pairs. Configuration is in `skills/rainbow/rules/credential-structural-rules.yaml`.

### Sensitive Key Patterns

L3 flags any key-value pair where the key matches a sensitive pattern and the value is non-empty:

| Key Pattern | Case Sensitive | Exclude Contexts |
|-------------|---------------|-----------------|
| `password` | No | -- |
| `secret` | No | -- |
| `token` | No | -- |
| `key` | No | `public_key`, `key_name`, `key_id`, `primary_key`, `foreign_key`, `sort_key`, `partition_key` |
| `credential` | No | -- |
| `auth` | No | `author`, `authority`, `authorization_url`, `auth_type`, `auth_method` |
| `private` | No | `private_ip`, `private_subnet`, `private_dns` |
| `apikey` | No | -- |
| `api_key` | No | -- |
| `access_key` | No | -- |
| `secret_key` | No | -- |
| `connection_string` | No | -- |

### Structural Detection Process

1. **Format detection:** Identify output format (JSON, YAML, XML, INI/config, or plaintext key-value)
2. **Key extraction:** Parse all key names from the structured output
3. **Pattern matching:** Match keys against sensitive key patterns
4. **Context exclusion:** Check matched keys against exclude contexts
5. **Value assessment:** For matched keys with non-excluded contexts, flag the key-value pair if value is non-empty and not a placeholder (e.g., `***`, `REDACTED`, `<masked>`)

### Nested Key Handling

For nested structures (e.g., `{"database": {"connection": {"password": "value"}}}`), L3 evaluates BOTH the leaf key name AND the full dot-path. A match at any level triggers detection.

---

## Fail-Closed Behavior

The credential filter operates in fail-closed mode. Every failure path results in credential protection.

### Detection Trigger (L1, L2, or L3 positive)

1. The output block containing the flagged content is **quarantined**
2. Quarantine location: `work/.credential-quarantine/{timestamp}-{tool}-{uuid}.txt`
3. Quarantine file includes: raw output, detecting layer (L1/L2/L3), matched pattern or rule, confidence level
4. A placeholder replaces the block in the context window:
   ```
   [QUARANTINED: potential credential detected by {layer} -- human review required at work/.credential-quarantine/{filename}]
   ```
5. The user is notified per P-020 (user authority)

### Filter Crash or Timeout

1. If the credential filter process fails (exception, timeout > 5 seconds), the **entire tool output block is rejected**
2. A placeholder is inserted:
   ```
   [TOOL OUTPUT REJECTED: credential filter failure -- raw output saved to quarantine]
   ```
3. The raw output is saved to quarantine for manual review
4. The failure is logged with stack trace for debugging

### Binary/Non-Text Output

1. Binary output from tools (e.g., Ghidra decompilation artifacts, mitmproxy captures) **bypasses context window entry entirely**
2. Only structured text summaries produced by the agent are permitted
3. Binary detection heuristic: presence of null bytes in the first 8192 bytes of output

### Quarantine Directory Structure

```
work/.credential-quarantine/
  20260314T143022Z-nmap-a1b2c3d4.txt
  20260314T143055Z-impacket-e5f6g7h8.txt
  ...
```

**Quarantine file format:**

```
--- Credential Filter Quarantine Record ---
Timestamp: {ISO 8601}
Tool: {tool name}
Agent: {invoking agent}
Detecting Layer: {L1|L2|L3}
Pattern/Rule: {matched pattern or rule name}
Confidence: {high|medium|low}
Quarantine Reason: {detection|crash|timeout|binary}
--- Raw Output Below ---
{full raw tool output}
```

---

## FMEA Decomposition

Failure mode analysis for the credential filter (from ADR-PROJ023-001).

| Failure Mode | S | O | D | RPN | Mitigation |
|-------------|---|---|---|-----|-----------|
| L1 regex miss on novel credential format | 9 | 5 | 4 | 180 | L2 entropy detection as fallback; quarterly pattern review |
| L2 false positive quarantines legitimate output | 3 | 6 | 2 | 36 | Entropy threshold tuning; per-tool allowlists for known high-entropy legitimate output |
| Filter crash on malformed tool output | 7 | 3 | 2 | 42 | Fail-closed design; timeout enforcement; structured error handling |
| Credential split across multiple output lines | 8 | 4 | 6 | 192 | L3 structural analysis operates on full output blocks; L1 sliding window |
| Base64-encoded credential blob | 8 | 5 | 5 | 200 | L1 base64 decode-and-rescan for strings matching base64 pattern |

**Total credential filter RPN:** 650 (reduced from 1,250 pre-mitigation, 48% reduction).

**Highest residual risk:** Base64-encoded credentials (RPN 200), addressed by L1 decode-and-rescan mechanism.

---

## Canary Testing Requirements

Each tool adapter MUST include credential test fixtures. The credential filter MUST demonstrate 100% detection on these fixtures before the tool is approved for production use.

### Fixture Location

```
skills/rainbow/tests/credential-fixtures/
  aws-key/canary.txt
  api-token/canary.txt
  ssh-key/canary.txt
  ntlm-hash/canary.txt
  kerberos/canary.txt
  connection-string/canary.txt
  plaintext-password/canary.txt
```

### Fixture Requirements

1. Each fixture contains at minimum 3 known credential formats from its category
2. All values MUST be obviously fake/canary values (documented as test data)
3. Each fixture MUST include at least one base64-encoded variant for L1 decode-and-rescan testing
4. Each fixture MUST include at least one multi-line variant for sliding window testing

### Acceptance Criteria

- **AC-F-05:** Credential filter detects 100% of canary fixtures across all 7 categories; fail-closed on crash
- **AC-F-05a:** L1 regex alone detects 100% of canary fixtures (fallback if L2/L3 deferred per IR-1)
- No fixture may be added to the allowlist
- Detection must complete within 5 seconds per fixture file

---

## Update Cadence

Credential filter patterns are reviewed when:

1. **New tool added:** Any new tool added to any sub-skill triggers pattern review for that tool's output format
2. **Format change detected:** When a tool's output format changes (version upgrade, new output fields), patterns are reviewed
3. **Quarterly review:** Scheduled quarterly review as part of security hygiene
4. **Incident-driven:** Any credential quarantine event that reveals a novel format triggers immediate pattern addition

Pattern additions follow the same PR review process as agent definition changes. Pattern removals require C3 minimum review (AE-005 security-relevant).

---

## Configuration Files

The credential filter specification is split across four files for separation of concerns:

| File | Purpose | Format |
|------|---------|--------|
| `rainbow-credential-filter.md` | This file. Human-readable specification, architecture, and procedures | Markdown |
| `credential-regex-patterns.yaml` | Machine-parseable L1 regex patterns organized by category | YAML |
| `credential-entropy-config.yaml` | L2 entropy detection parameters and allowlist | YAML |
| `credential-structural-rules.yaml` | L3 structural analysis key patterns and exclusions | YAML |

All four files are maintained in `skills/rainbow/rules/`. All four files are subject to the update cadence defined above.

---

*Source: ADR-PROJ023-001 Credential Filter Architecture section. Criticality: C4 (security infrastructure per AE-005).*
*FMEA data: ADR-PROJ023-001 S x O x D decomposition table.*
