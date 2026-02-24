# Threat Model Template (STRIDE/DREAD)

> **Version:** 1.0.0
> **Skill:** /eng-team
> **Agent:** eng-architect
> **Configurable Rule Set:** R-011
> **SSOT:** ADR-PROJ010-001 Section 9 (Threat Modeling Escalation), Architecture Decision B-004

## Document Sections

| Section | Purpose |
|---------|---------|
| [Overview](#overview) | Template scope, usage, and criticality escalation |
| [L0: Threat Summary](#l0-threat-summary) | Stakeholder-accessible threat overview |
| [L1: Threat Analysis](#l1-threat-analysis) | Detailed STRIDE analysis with DREAD scoring |
| [L2: Attack Tree Analysis](#l2-attack-tree-analysis) | Strategic attack path modeling (C3+) |
| [Configuration](#configuration) | Configurable rule set parameters |

---

## Overview

This template guides threat modeling following the criticality-based escalation defined in ADR-PROJ010-001:

| Criticality | Methodology |
|-------------|-------------|
| C1 (Routine) | STRIDE only |
| C2 (Standard) | STRIDE + DREAD scoring |
| C3 (Significant) | STRIDE + DREAD + Attack Trees |
| C4 (Critical) | STRIDE + DREAD + Attack Trees + PASTA stages 4-7 |
| PII involvement | Add LINDDUN to any level |

**When to use:** During Step 1 (eng-architect) of the /eng-team workflow, as part of system design.

---

## L0: Threat Summary

| Field | Value |
|-------|-------|
| **System Name** | {name} |
| **Criticality Level** | {C1 / C2 / C3 / C4} |
| **Methodology Applied** | {STRIDE / STRIDE+DREAD / STRIDE+DREAD+Attack Trees / Full PASTA} |
| **Date** | {YYYY-MM-DD} |
| **Total Threats Identified** | {count} |
| **Critical/High Threats** | {count} |
| **Residual Risk** | {Acceptable / Requires Mitigation / Unacceptable} |

### Threat Landscape Summary

{2-3 paragraph summary of the threat landscape, key risks, and recommended actions for stakeholders.}

---

## L1: Threat Analysis

### System Context

| Attribute | Value |
|-----------|-------|
| **System Type** | {Web App / API / Microservice / Infrastructure / Mobile} |
| **Data Classification** | {Public / Internal / Confidential / Restricted} |
| **User Base** | {Internal / External / Both} |
| **Authentication** | {method} |
| **Network Position** | {Internet-facing / Internal / Hybrid} |

### Trust Boundaries

| ID | Boundary | Inside | Outside | Data Crossing |
|----|----------|--------|---------|---------------|
| TB-001 | {boundary name} | {components} | {components} | {data types} |

### STRIDE Threat Catalog

#### Spoofing (Identity)

| ID | Threat | Target Component | Attack Vector | Likelihood | Impact |
|----|--------|-----------------|---------------|------------|--------|
| S-001 | {threat description} | {component} | {vector} | {H/M/L} | {H/M/L} |

**Mitigations:**

| Threat ID | Mitigation | Standard Reference | Status |
|-----------|-----------|-------------------|--------|
| S-001 | {mitigation} | {ASVS V2.x / CWE-xxx} | {Implemented / Planned / Accepted} |

#### Tampering (Integrity)

| ID | Threat | Target Component | Attack Vector | Likelihood | Impact |
|----|--------|-----------------|---------------|------------|--------|
| T-001 | {threat} | {component} | {vector} | {L} | {L} |

#### Repudiation (Non-repudiation)

| ID | Threat | Target Component | Attack Vector | Likelihood | Impact |
|----|--------|-----------------|---------------|------------|--------|
| R-001 | {threat} | {component} | {vector} | {L} | {L} |

#### Information Disclosure (Confidentiality)

| ID | Threat | Target Component | Attack Vector | Likelihood | Impact |
|----|--------|-----------------|---------------|------------|--------|
| I-001 | {threat} | {component} | {vector} | {L} | {L} |

#### Denial of Service (Availability)

| ID | Threat | Target Component | Attack Vector | Likelihood | Impact |
|----|--------|-----------------|---------------|------------|--------|
| D-001 | {threat} | {component} | {vector} | {L} | {L} |

#### Elevation of Privilege (Authorization)

| ID | Threat | Target Component | Attack Vector | Likelihood | Impact |
|----|--------|-----------------|---------------|------------|--------|
| E-001 | {threat} | {component} | {vector} | {L} | {L} |

### DREAD Risk Scores (C2+)

| Threat ID | Damage | Reproducibility | Exploitability | Affected Users | Discoverability | Total (/50) | Risk Level |
|-----------|--------|----------------|----------------|----------------|-----------------|-------------|-----------|
| S-001 | {1-10} | {1-10} | {1-10} | {1-10} | {1-10} | {sum} | {Critical/High/Medium/Low} |

**Risk Level Thresholds:**

| Score Range | Risk Level | Action Required |
|-------------|-----------|-----------------|
| 40-50 | Critical | Immediate mitigation required |
| 25-39 | High | Mitigation before release |
| 12-24 | Medium | Mitigation planned |
| 1-11 | Low | Risk accepted or deferred |

---

## L2: Attack Tree Analysis (C3+)

> Include this section only for C3 (Significant) or C4 (Critical) threat models.

### Attack Goal: {Primary Attack Objective}

```
[Attack Goal: {objective}]
├── [AND/OR] Attack Path 1: {path}
│   ├── [AND] Precondition: {precondition}
│   ├── [AND] Action: {action}
│   └── [OR] Alternative: {alternative}
├── [OR] Attack Path 2: {path}
│   ├── [AND] Precondition: {precondition}
│   └── [AND] Action: {action}
└── [OR] Attack Path 3: {path}
    └── [AND] Action: {action}
```

### Attack Path Risk Assessment

| Path ID | Feasibility | Impact | Overall Risk | Mitigation Priority |
|---------|------------|--------|-------------|---------------------|
| Path 1 | {H/M/L} | {H/M/L} | {H/M/L} | {1-N} |

### PASTA Stages 4-7 (C4 Only)

> Include this section only for C4 (Critical) threat models.

| PASTA Stage | Activity | Output |
|-------------|----------|--------|
| Stage 4: Threat Analysis | {adversary profiling, threat intelligence} | {threat agent catalog} |
| Stage 5: Vulnerability Analysis | {vulnerability mapping to threats} | {vulnerability-threat matrix} |
| Stage 6: Attack Modeling | {attack tree enumeration, simulation} | {attack scenarios} |
| Stage 7: Risk & Impact Analysis | {business impact, risk quantification} | {risk-ordered mitigation plan} |

### LINDDUN Analysis (PII Systems)

> Include this section when system processes personally identifiable information.

| LINDDUN Category | Threat | Affected Data | Mitigation |
|-----------------|--------|---------------|------------|
| **L**inkability | {threat} | {data} | {mitigation} |
| **I**dentifiability | {threat} | {data} | {mitigation} |
| **N**on-repudiation (unwanted) | {threat} | {data} | {mitigation} |
| **D**etectability | {threat} | {data} | {mitigation} |
| **D**isclosure of information | {threat} | {data} | {mitigation} |
| **U**nawareness | {threat} | {data} | {mitigation} |
| **N**on-compliance | {threat} | {data} | {mitigation} |

---

## Configuration

### Configurable Rule Set (R-011)

| Parameter | Default | Override | Description |
|-----------|---------|----------|-------------|
| `methodology` | STRIDE+DREAD | STRIDE, PASTA, LINDDUN | Primary methodology |
| `auto_escalate_pii` | true | false | Auto-add LINDDUN for PII systems |
| `dread_threshold_critical` | 40 | 1-50 | Score above = Critical |
| `dread_threshold_high` | 25 | 1-50 | Score above = High |
| `attack_tree_depth` | 3 | 1-5 | Max attack tree depth for C3+ |
| `include_pasta` | auto (C4 only) | always, never, auto | PASTA stage inclusion |

---

*Template Version: 1.0.0 | /eng-team Skill | PROJ-010 Cyber Ops*
