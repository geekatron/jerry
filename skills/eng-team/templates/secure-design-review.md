# Secure Design Review Template

> **Version:** 1.0.0
> **Skill:** /eng-team
> **Agent:** eng-architect, eng-reviewer
> **Configurable Rule Set:** R-011
> **SSOT:** ADR-PROJ010-001 (Agent Team Architecture), NIST SP 800-218 SSDF

## Document Sections

| Section | Purpose |
|---------|---------|
| [Overview](#overview) | Template scope and usage |
| [L0: Executive Summary](#l0-executive-summary) | Stakeholder-accessible design review summary |
| [L1: Technical Review](#l1-technical-review) | Implementation-focused security analysis |
| [L2: Strategic Assessment](#l2-strategic-assessment) | Architecture-level security implications |
| [Configuration](#configuration) | Configurable rule set parameters |

---

## Overview

This template guides secure design reviews for systems and services built using the /eng-team skill. It combines architecture analysis with threat modeling to ensure security is evaluated at the design phase, not bolted on after implementation.

**When to use:** Before implementation begins, when a new system, service, or significant feature is being designed.

**Agents involved:** eng-architect (produces the review), eng-reviewer (validates the review).

---

## L0: Executive Summary

> Fill this section for non-technical stakeholders.

| Field | Value |
|-------|-------|
| **System/Service Name** | {name} |
| **Review Date** | {YYYY-MM-DD} |
| **Reviewer** | {eng-architect engagement ID} |
| **Overall Risk Rating** | {Critical / High / Medium / Low} |
| **Recommendation** | {Approve / Approve with Conditions / Reject} |

### Key Findings Summary

| # | Finding | Severity | Mitigation Status |
|---|---------|----------|-------------------|
| 1 | {finding} | {severity} | {Open / Mitigated / Accepted} |

### Decision Required

{One paragraph: what decision do stakeholders need to make based on this review?}

---

## L1: Technical Review

### 1. Architecture Overview

| Component | Purpose | Trust Level | Data Classification |
|-----------|---------|-------------|---------------------|
| {component} | {purpose} | {Trusted / Semi-Trusted / Untrusted} | {Public / Internal / Confidential / Restricted} |

### 2. Threat Model (STRIDE/DREAD)

#### Trust Boundaries

| Boundary | Components | Data Flow | Risk |
|----------|-----------|-----------|------|
| {boundary} | {components} | {flow description} | {risk level} |

#### STRIDE Analysis

| Threat Category | Applicable Components | Threat Description | DREAD Score | Mitigation |
|----------------|----------------------|-------------------|-------------|------------|
| **S**poofing | {components} | {threat} | {D+R+E+A+D}/50 | {mitigation} |
| **T**ampering | {components} | {threat} | {score}/50 | {mitigation} |
| **R**epudiation | {components} | {threat} | {score}/50 | {mitigation} |
| **I**nformation Disclosure | {components} | {threat} | {score}/50 | {mitigation} |
| **D**enial of Service | {components} | {threat} | {score}/50 | {mitigation} |
| **E**levation of Privilege | {components} | {threat} | {score}/50 | {mitigation} |

#### DREAD Scoring Guide

| Factor | 1 (Low) | 5 (Medium) | 10 (High) |
|--------|---------|------------|-----------|
| **D**amage | Minor data exposure | Significant data loss | Complete system compromise |
| **R**eproducibility | Complex, rare conditions | Moderate effort | Trivially reproducible |
| **E**xploitability | Expert skill required | Moderate skill | No special tools needed |
| **A**ffected Users | Single user | Subset of users | All users |
| **D**iscoverability | Requires insider knowledge | Discoverable with effort | Publicly known |

### 3. Security Requirements Mapping

| Requirement Source | Requirement ID | Description | Design Compliance | Evidence |
|-------------------|---------------|-------------|-------------------|----------|
| OWASP ASVS 5.0 | V{x}.{y} | {requirement} | {Compliant / Partial / Non-Compliant} | {evidence} |
| NIST SSDF | {PW/PO/PS/RV}.{x} | {requirement} | {status} | {evidence} |
| CIS Benchmark | {benchmark ID} | {requirement} | {status} | {evidence} |

### 4. Data Flow Analysis

| Flow ID | Source | Destination | Data Type | Classification | Protection | Risks |
|---------|--------|-------------|-----------|---------------|------------|-------|
| DF-001 | {source} | {dest} | {type} | {classification} | {encryption, auth, etc.} | {risks} |

### 5. Authentication & Authorization Design

| Aspect | Design Decision | Standard Reference | Risk |
|--------|----------------|-------------------|------|
| Authentication method | {decision} | {ASVS V2.x} | {risk} |
| Session management | {decision} | {ASVS V3.x} | {risk} |
| Access control model | {decision} | {ASVS V4.x} | {risk} |
| Token/credential storage | {decision} | {ASVS V2.x} | {risk} |

---

## L2: Strategic Assessment

### Architecture Trade-offs

| Trade-off | Option A | Option B | Security Implication | Decision |
|-----------|----------|----------|---------------------|----------|
| {trade-off} | {option} | {option} | {implication} | {decision} |

### Long-term Security Posture

| Dimension | Current State | Target State | Gap | Remediation Timeline |
|-----------|--------------|-------------|-----|---------------------|
| {dimension} | {current} | {target} | {gap description} | {timeline} |

### SDLC Governance Alignment

| Governance Layer | Framework | Compliance Status | Evidence |
|-----------------|-----------|-------------------|----------|
| Layer 1: Governance | NIST SSDF | {status} | {evidence} |
| Layer 2: Lifecycle | Microsoft SDL | {status} | {evidence} |
| Layer 3: Assessment | OWASP SAMM | {status} | {evidence} |
| Layer 4: Supply Chain | SLSA | {status} | {evidence} |
| Layer 5: Automation | DevSecOps | {status} | {evidence} |

---

## Configuration

### Configurable Rule Set (R-011)

| Parameter | Default | Override | Description |
|-----------|---------|----------|-------------|
| `threat_model_methodology` | STRIDE+DREAD | STRIDE, PASTA, LINDDUN | Primary threat modeling methodology |
| `risk_scoring` | DREAD | CVSS v3.1, custom | Risk quantification method |
| `compliance_frameworks` | OWASP ASVS 5.0, NIST SSDF | Add/remove frameworks | Standards to check against |
| `minimum_dread_threshold` | 25 | 1-50 | Findings above this score require mitigation |
| `review_depth` | standard | quick, standard, comprehensive | Level of analysis detail |

---

*Template Version: 1.0.0 | /eng-team Skill | PROJ-010 Cyber Ops*
