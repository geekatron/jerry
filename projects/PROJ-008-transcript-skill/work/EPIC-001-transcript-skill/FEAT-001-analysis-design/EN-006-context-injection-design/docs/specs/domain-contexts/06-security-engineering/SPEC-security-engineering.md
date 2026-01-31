# Domain Specification: Security Engineering

<!--
DOCUMENT: SPEC-security-engineering.md
VERSION: 1.0.0
DOMAIN: security-engineering
TASK: TASK-038 (Phase 3)
STATUS: COMPLETE
-->

---

> **DISCLAIMER:** This guidance is AI-generated based on NASA Systems Engineering
> standards. It is advisory only and does not constitute official NASA guidance.
> All SE decisions require human review and professional engineering judgment.

---

## Document Control

| Attribute | Value |
|-----------|-------|
| **Domain ID** | security-engineering |
| **Version** | 1.0.0 |
| **Status** | DESIGN COMPLETE |
| **Created** | 2026-01-27 |
| **Task** | TASK-038 (Phase 3) |

---

## L0: Overview (ELI5)

This domain helps analyze **security-focused meetings** like:
- Security audits ("We found a SQL injection in the login form...")
- Threat modeling ("An attacker could exploit...")
- Compliance reviews ("We're not meeting SOC2 requirement X...")

It extracts **key information** like:
- Vulnerabilities with CVE references
- Threats using STRIDE methodology
- Mitigations and security controls
- Compliance gaps and remediation plans

---

## L1: Domain Details (Software Engineer)

### Target Users

| Role | Use Case |
|------|----------|
| Security Engineers | Track vulnerabilities |
| Security Architects | Document threat models |
| AppSec Engineers | Code review findings |
| Compliance Officers | Track compliance gaps |

### Supported Transcript Types

| Type | Description | Typical Duration |
|------|-------------|------------------|
| Security Audit | Vulnerability review | 1-2 hours |
| Threat Modeling | STRIDE/DREAD analysis | 1-2 hours |
| Compliance Review | SOC2/PCI/HIPAA audit | 1-2 hours |
| Vulnerability Triage | CVE prioritization | 30-60 min |
| Security Architecture | Design review | 1-2 hours |

### STRIDE Threat Categories

| Category | Description |
|----------|-------------|
| **S**poofing | Pretending to be someone else |
| **T**ampering | Modifying data or code |
| **R**epudiation | Denying actions taken |
| **I**nformation Disclosure | Exposing private data |
| **D**enial of Service | Making system unavailable |
| **E**levation of Privilege | Gaining unauthorized access |

### CVSS v3.1 Severity

| Score | Rating | Description |
|-------|--------|-------------|
| 9.0-10.0 | Critical | Immediate remediation |
| 7.0-8.9 | High | High priority fix |
| 4.0-6.9 | Medium | Scheduled fix |
| 0.1-3.9 | Low | Best effort |

---

## L2: Technical Specification (Principal Architect)

### Entity Model

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    SECURITY ENGINEERING ENTITY MODEL                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌─────────────────┐       exploits       ┌─────────────────┐              │
│  │    Threat       │──────────────────────►│  Vulnerability  │              │
│  │                 │                       │                 │              │
│  │ - threat_id     │◄─ STRIDE             │ - title         │              │
│  │ - description   │                       │ - cve           │              │
│  │ - threat_actor  │                       │ - severity      │◄─ CVSS      │
│  │ - attack_vector │                       │ - cvss_score    │              │
│  │ - likelihood    │                       │ - status        │              │
│  │ - impact        │                       └────────┬────────┘              │
│  └────────┬────────┘                                │                       │
│           │                                         │                       │
│           │ mitigated_by                            │ remediated_by         │
│           ▼                                         ▼                       │
│  ┌─────────────────┐                       ┌─────────────────┐              │
│  │   Mitigation    │                       │    Security     │              │
│  │                 │                       │    Decision     │              │
│  │ - title         │                       │                 │              │
│  │ - type          │◄─ prevent/detect/fix  │ - topic         │              │
│  │ - implementation│                       │ - decision      │              │
│  │ - effectiveness │                       │ - risk_accepted │              │
│  │ - status        │                       │ - rationale     │              │
│  └─────────────────┘                       │ - approver      │              │
│                                            └─────────────────┘              │
│                                                                              │
│  ┌─────────────────┐                                                        │
│  │ Compliance Gap  │                                                        │
│  │                 │                                                        │
│  │ - framework     │◄─ SOC2/PCI/HIPAA/GDPR                                  │
│  │ - requirement   │                                                        │
│  │ - current_state │                                                        │
│  │ - gap           │                                                        │
│  │ - remediation   │                                                        │
│  └─────────────────┘                                                        │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Entity Definitions

See [entities/entity-definitions.yaml](./entities/entity-definitions.yaml) for the complete schema.

| Entity | Purpose | Key Attributes |
|--------|---------|----------------|
| `vulnerability` | Security weakness | title, cve, severity, cvss_score, affected_systems, status |
| `threat` | Threat model finding | threat_id, description, threat_actor, attack_vector, likelihood, impact |
| `mitigation` | Security control | title, type, implementation, effectiveness, status |
| `compliance_gap` | Compliance issue | framework, requirement, current_state, gap, remediation |
| `security_decision` | Risk decision | topic, decision, risk_accepted, rationale, approver |

---

## Validation Criteria

| ID | Criterion | Status |
|----|-----------|--------|
| SEC-AC-001 | Entity definitions cover 5 types | ✅ |
| SEC-AC-002 | Severity aligns with CVSS v3.1 | ✅ |
| SEC-AC-003 | Supports STRIDE methodology | ✅ |
| SEC-AC-004 | Covers major compliance frameworks | ✅ |
| SEC-AC-005 | Handles CVE extraction | ✅ |
| SEC-AC-006 | Captures risk acceptance | ✅ |
| SEC-AC-007 | Output supports vuln tracking | ✅ |
| SEC-AC-008 | Validation criteria defined | ✅ |

---

*Document ID: SPEC-SEC-001*
*Domain: security-engineering*
*Task: TASK-038*
*Status: DESIGN COMPLETE*
