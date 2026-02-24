# Code Review Security Checklist

> **Version:** 1.0.0
> **Skill:** /eng-team
> **Agent:** eng-security, eng-reviewer
> **Configurable Rule Set:** R-011
> **SSOT:** CWE Top 25 (2025), OWASP ASVS 5.0, NIST SP 800-218 SSDF PW.7

## Document Sections

| Section | Purpose |
|---------|---------|
| [Overview](#overview) | Template scope and usage |
| [L0: Review Summary](#l0-review-summary) | Stakeholder-accessible findings summary |
| [L1: Security Checklist](#l1-security-checklist) | Implementation-focused review items |
| [L2: Strategic Findings](#l2-strategic-findings) | Architecture-level security concerns |
| [Configuration](#configuration) | Configurable rule set parameters |

---

## Overview

This checklist guides manual secure code review per SSDF PW.7 (Review and/or analyze human-readable code to identify vulnerabilities and verify compliance with security requirements). It covers the CWE Top 25 most dangerous software weaknesses and OWASP ASVS verification requirements.

**When to use:** During Step 6 (eng-security manual review) of the /eng-team workflow, after automated scans (Step 4) and testing (Step 5).

**Agents involved:** eng-security (performs the review), eng-reviewer (validates completeness).

---

## L0: Review Summary

| Field | Value |
|-------|-------|
| **Component Under Review** | {component name/path} |
| **Review Date** | {YYYY-MM-DD} |
| **Reviewer** | {eng-security engagement ID} |
| **Lines of Code Reviewed** | {count} |
| **Findings** | {Critical: N, High: N, Medium: N, Low: N, Info: N} |
| **Recommendation** | {Pass / Pass with Findings / Fail} |

---

## L1: Security Checklist

### CWE Top 25 Coverage

| Rank | CWE ID | Name | Checked | Finding | Severity |
|------|--------|------|---------|---------|----------|
| 1 | CWE-787 | Out-of-bounds Write | [ ] | {finding or N/A} | {severity} |
| 2 | CWE-79 | Cross-site Scripting (XSS) | [ ] | | |
| 3 | CWE-89 | SQL Injection | [ ] | | |
| 4 | CWE-416 | Use After Free | [ ] | | |
| 5 | CWE-78 | OS Command Injection | [ ] | | |
| 6 | CWE-20 | Improper Input Validation | [ ] | | |
| 7 | CWE-125 | Out-of-bounds Read | [ ] | | |
| 8 | CWE-22 | Path Traversal | [ ] | | |
| 9 | CWE-352 | Cross-Site Request Forgery (CSRF) | [ ] | | |
| 10 | CWE-434 | Unrestricted Upload of File with Dangerous Type | [ ] | | |
| 11 | CWE-862 | Missing Authorization | [ ] | | |
| 12 | CWE-476 | NULL Pointer Dereference | [ ] | | |
| 13 | CWE-287 | Improper Authentication | [ ] | | |
| 14 | CWE-190 | Integer Overflow or Wraparound | [ ] | | |
| 15 | CWE-502 | Deserialization of Untrusted Data | [ ] | | |
| 16 | CWE-77 | Command Injection | [ ] | | |
| 17 | CWE-119 | Improper Restriction of Operations within Memory Buffer | [ ] | | |
| 18 | CWE-798 | Use of Hard-coded Credentials | [ ] | | |
| 19 | CWE-918 | Server-Side Request Forgery (SSRF) | [ ] | | |
| 20 | CWE-306 | Missing Authentication for Critical Function | [ ] | | |
| 21 | CWE-362 | Race Condition | [ ] | | |
| 22 | CWE-269 | Improper Privilege Management | [ ] | | |
| 23 | CWE-94 | Code Injection | [ ] | | |
| 24 | CWE-863 | Incorrect Authorization | [ ] | | |
| 25 | CWE-276 | Incorrect Default Permissions | [ ] | | |

### OWASP ASVS Verification Areas

| ASVS Chapter | Area | Items Checked | Findings |
|--------------|------|---------------|----------|
| V1 | Architecture & Threat Modeling | {count} | {findings} |
| V2 | Authentication | {count} | {findings} |
| V3 | Session Management | {count} | {findings} |
| V4 | Access Control | {count} | {findings} |
| V5 | Validation, Sanitization, Encoding | {count} | {findings} |
| V6 | Stored Cryptography | {count} | {findings} |
| V7 | Error Handling & Logging | {count} | {findings} |
| V8 | Data Protection | {count} | {findings} |
| V9 | Communication | {count} | {findings} |
| V10 | Malicious Code | {count} | {findings} |
| V11 | Business Logic | {count} | {findings} |
| V12 | Files & Resources | {count} | {findings} |
| V13 | API & Web Service | {count} | {findings} |
| V14 | Configuration | {count} | {findings} |

### Additional Security Checks

| Category | Check | Status | Notes |
|----------|-------|--------|-------|
| Secrets | No hardcoded credentials, API keys, or tokens | [ ] | |
| Secrets | Secrets loaded from environment/vault only | [ ] | |
| Logging | No sensitive data in log output | [ ] | |
| Logging | Security events logged with sufficient context | [ ] | |
| Error Handling | No stack traces or internal details in error responses | [ ] | |
| Error Handling | Consistent error response format | [ ] | |
| Dependencies | No known vulnerable dependencies (CVE check) | [ ] | |
| Dependencies | Dependencies pinned to specific versions | [ ] | |
| Crypto | Industry-standard algorithms only (no custom crypto) | [ ] | |
| Crypto | Proper key management and rotation | [ ] | |

---

## L2: Strategic Findings

### Systemic Issues

| Issue | Affected Components | Root Cause | Recommended Fix | Priority |
|-------|--------------------|-----------|-----------------|----------|
| {issue} | {components} | {root cause} | {fix} | {priority} |

### Security Debt Assessment

| Category | Current Debt | Trend | Recommended Action |
|----------|-------------|-------|-------------------|
| {category} | {description} | {Increasing / Stable / Decreasing} | {action} |

---

## Configuration

### Configurable Rule Set (R-011)

| Parameter | Default | Override | Description |
|-----------|---------|----------|-------------|
| `cwe_checklist` | CWE Top 25 (2025) | Custom CWE list | Which CWEs to check |
| `asvs_level` | Level 2 | Level 1, Level 2, Level 3 | ASVS verification level depth |
| `language_specific_checks` | auto-detect | python, javascript, go, rust, java | Language-specific vulnerability patterns |
| `minimum_severity_threshold` | Medium | Low, Medium, High, Critical | Minimum severity to report |
| `review_scope` | full | targeted, full, comprehensive | Scope of code review |

---

*Template Version: 1.0.0 | /eng-team Skill | PROJ-010 Cyber Ops*
