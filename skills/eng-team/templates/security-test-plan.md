# Security Test Plan Template

> **Version:** 1.0.0
> **Skill:** /eng-team
> **Agent:** eng-qa, eng-devsecops
> **Configurable Rule Set:** R-011
> **SSOT:** OWASP Testing Guide, NIST SP 800-218 SSDF PW.7/PW.8

## Document Sections

| Section | Purpose |
|---------|---------|
| [Overview](#overview) | Template scope and usage |
| [L0: Test Summary](#l0-test-summary) | Stakeholder-accessible test status |
| [L1: Test Strategy](#l1-test-strategy) | Implementation-focused test planning |
| [L2: Coverage Analysis](#l2-coverage-analysis) | Strategic test coverage assessment |
| [Configuration](#configuration) | Configurable rule set parameters |

---

## Overview

This template guides security test planning per SSDF PW.8 (Test executable code to identify vulnerabilities and verify compliance with security requirements). It covers automated scanning (SAST/DAST), manual testing, fuzzing, and property-based testing.

**When to use:** During Steps 4-5 (eng-devsecops + eng-qa) of the /eng-team workflow.

**Agents involved:** eng-devsecops (automated scans), eng-qa (testing strategy and execution).

---

## L0: Test Summary

| Field | Value |
|-------|-------|
| **System Under Test** | {name} |
| **Test Date** | {YYYY-MM-DD} |
| **Test Lead** | {eng-qa engagement ID} |
| **Total Test Cases** | {count} |
| **Pass / Fail / Blocked** | {pass} / {fail} / {blocked} |
| **Code Coverage** | {line%} / {branch%} |
| **Security Findings** | {Critical: N, High: N, Medium: N, Low: N} |
| **Overall Status** | {Pass / Fail / Conditional Pass} |

---

## L1: Test Strategy

### Automated Security Scanning (Step 4: eng-devsecops)

| Scan Type | Tool | Target | Schedule | Status |
|-----------|------|--------|----------|--------|
| SAST | {tool, e.g. Semgrep, CodeQL} | {source code path} | {CI/every commit} | {Configured / Pending} |
| DAST | {tool, e.g. OWASP ZAP, Burp} | {running application URL} | {nightly / per release} | {status} |
| SCA/Dependency | {tool, e.g. Snyk, Trivy} | {dependency manifest} | {CI/every commit} | {status} |
| Secrets Scanning | {tool, e.g. Gitleaks, TruffleHog} | {repository} | {pre-commit + CI} | {status} |
| Container Scanning | {tool, e.g. Trivy, Grype} | {container images} | {CI/on build} | {status} |
| IaC Scanning | {tool, e.g. Checkov, tfsec} | {IaC templates} | {CI/on change} | {status} |

### Security Test Cases (Step 5: eng-qa)

#### Authentication Testing

| TC ID | Test Case | ASVS Ref | Priority | Status | Result |
|-------|-----------|----------|----------|--------|--------|
| AUTH-001 | Verify password complexity enforcement | V2.1.1 | High | {status} | {result} |
| AUTH-002 | Verify account lockout after failed attempts | V2.1.6 | High | | |
| AUTH-003 | Verify MFA enforcement for sensitive operations | V2.8.1 | High | | |
| AUTH-004 | Verify credential storage uses approved algorithms | V2.4.1 | Critical | | |

#### Authorization Testing

| TC ID | Test Case | ASVS Ref | Priority | Status | Result |
|-------|-----------|----------|----------|--------|--------|
| AUTHZ-001 | Verify IDOR protection on all endpoints | V4.1.2 | Critical | | |
| AUTHZ-002 | Verify role-based access control enforcement | V4.1.1 | High | | |
| AUTHZ-003 | Verify horizontal privilege escalation prevention | V4.2.1 | Critical | | |

#### Input Validation Testing

| TC ID | Test Case | ASVS Ref | Priority | Status | Result |
|-------|-----------|----------|----------|--------|--------|
| INPUT-001 | Verify SQL injection prevention | V5.3.4 | Critical | | |
| INPUT-002 | Verify XSS prevention (reflected, stored, DOM) | V5.3.3 | Critical | | |
| INPUT-003 | Verify command injection prevention | V5.3.8 | Critical | | |
| INPUT-004 | Verify path traversal prevention | V5.3.7 | High | | |

#### Fuzzing Campaign

| Target | Fuzzing Type | Input Space | Duration | Findings |
|--------|-------------|-------------|----------|----------|
| {API endpoint} | {mutation / generation / grammar} | {input description} | {hours} | {count} |

#### Property-Based Testing

| Property | Generator | Assertions | Status |
|----------|-----------|------------|--------|
| {invariant property} | {input generator description} | {assertion} | {status} |

---

## L2: Coverage Analysis

### OWASP Testing Guide Coverage

| Testing Category | Total Checks | Completed | Coverage % | Findings |
|-----------------|-------------|-----------|------------|----------|
| Information Gathering | {total} | {done} | {%} | {count} |
| Configuration Management | {total} | {done} | {%} | {count} |
| Identity Management | {total} | {done} | {%} | {count} |
| Authentication | {total} | {done} | {%} | {count} |
| Authorization | {total} | {done} | {%} | {count} |
| Session Management | {total} | {done} | {%} | {count} |
| Input Validation | {total} | {done} | {%} | {count} |
| Error Handling | {total} | {done} | {%} | {count} |
| Cryptography | {total} | {done} | {%} | {count} |
| Business Logic | {total} | {done} | {%} | {count} |
| Client-Side | {total} | {done} | {%} | {count} |

### Security Coverage Gap Analysis

| Gap | Risk | Recommended Action | Priority |
|-----|------|--------------------|----------|
| {gap description} | {risk} | {action} | {priority} |

---

## Configuration

### Configurable Rule Set (R-011)

| Parameter | Default | Override | Description |
|-----------|---------|----------|-------------|
| `sast_tools` | auto-detect | semgrep, codeql, bandit | SAST tool selection |
| `dast_tools` | OWASP ZAP | burp, zap, nuclei | DAST tool selection |
| `minimum_code_coverage` | 90% | 0-100% | Line coverage threshold (H-21) |
| `fuzzing_duration_hours` | 4 | 1-48 | Minimum fuzzing campaign duration |
| `asvs_verification_level` | Level 2 | Level 1-3 | ASVS depth |
| `scan_frequency` | per-commit | nightly, per-commit, manual | Automated scan schedule |

---

*Template Version: 1.0.0 | /eng-team Skill | PROJ-010 Cyber Ops*
