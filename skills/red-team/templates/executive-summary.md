# Executive Summary Template

> **Version:** 1.0.0
> **Skill:** /red-team
> **Agent:** red-reporter
> **Configurable Rule Set:** R-011
> **SSOT:** FEAT-040 L0 Output Spec

## Document Sections

| Section | Purpose |
|---------|---------|
| [Overview](#overview) | Template scope and usage |
| [L0: Executive Summary](#l0-executive-summary) | Non-technical stakeholder communication |
| [L1: Findings Overview](#l1-findings-overview) | Technical summary for security leadership |
| [L2: Strategic Recommendations](#l2-strategic-recommendations) | Long-term security posture guidance |
| [Configuration](#configuration) | Configurable rule set parameters |

---

## Overview

This template produces the executive summary section of the engagement report per FEAT-040 L0 output specification. It translates technical findings into business risk language for stakeholders.

**When to use:** At engagement conclusion, by red-reporter when compiling the final engagement report.

**Agent:** red-reporter (mandatory last for reporting).

---

## L0: Executive Summary

### Engagement Overview

| Field | Value |
|-------|-------|
| **Engagement ID** | RED-{NNNN} |
| **Engagement Type** | {type} |
| **Target** | {organization/system} |
| **Duration** | {start} to {end} |
| **Methodology** | {PTES / OSSTMM / NIST SP 800-115} |
| **Overall Risk Rating** | {Critical / High / Medium / Low} |

### Key Metrics

| Metric | Value |
|--------|-------|
| Total Findings | {count} |
| Critical Findings | {count} |
| High Findings | {count} |
| Medium Findings | {count} |
| Low/Info Findings | {count} |
| Unique Attack Paths | {count} |
| ATT&CK Tactics Exercised | {count}/14 |

### Finding Severity Distribution

| Severity | Count | % of Total |
|----------|-------|-----------|
| Critical | {n} | {%} |
| High | {n} | {%} |
| Medium | {n} | {%} |
| Low | {n} | {%} |
| Informational | {n} | {%} |

### Top Findings

| # | Finding | Severity | Business Impact |
|---|---------|----------|----------------|
| 1 | {finding title} | {severity} | {business impact in plain language} |
| 2 | {finding} | {severity} | {impact} |
| 3 | {finding} | {severity} | {impact} |

### Overall Assessment

{3-5 paragraph narrative assessment for executive stakeholders. Covers:
- What was tested and why
- Overall security posture assessment
- Most significant risks identified
- Key strengths observed
- Recommended priority actions}

---

## L1: Findings Overview

### Kill Chain Progress

| Kill Chain Phase | Status | Findings | Key Result |
|-----------------|--------|----------|------------|
| Reconnaissance | {Completed / Partial / Not Attempted} | {count} | {summary} |
| Initial Access | {Achieved / Not Achieved} | {count} | {summary} |
| Execution | {Achieved / Not Achieved} | {count} | {summary} |
| Persistence | {Achieved / Not Attempted / Not Authorized} | {count} | {summary} |
| Privilege Escalation | {Achieved / Not Achieved} | {count} | {summary} |
| Defense Evasion | {Tested / Not Tested} | {count} | {summary} |
| Credential Access | {Achieved / Not Achieved} | {count} | {summary} |
| Discovery | {Completed / Partial} | {count} | {summary} |
| Lateral Movement | {Achieved / Not Achieved} | {count} | {summary} |
| Collection | {Achieved / Not Attempted / Not Authorized} | {count} | {summary} |
| Exfiltration | {Achieved / Not Attempted / Not Authorized} | {count} | {summary} |
| Impact | {Demonstrated / Not Attempted / Not Authorized} | {count} | {summary} |

### Findings by Category

| Category | Critical | High | Medium | Low | Total |
|----------|----------|------|--------|-----|-------|
| Authentication | {n} | {n} | {n} | {n} | {n} |
| Authorization | {n} | {n} | {n} | {n} | {n} |
| Input Validation | {n} | {n} | {n} | {n} | {n} |
| Configuration | {n} | {n} | {n} | {n} | {n} |
| Cryptography | {n} | {n} | {n} | {n} | {n} |
| Network | {n} | {n} | {n} | {n} | {n} |
| Other | {n} | {n} | {n} | {n} | {n} |

---

## L2: Strategic Recommendations

### Priority Remediation Roadmap

| Priority | Timeframe | Action | Findings Addressed | Effort |
|----------|-----------|--------|-------------------|--------|
| P1 (Immediate) | 0-7 days | {action} | {finding IDs} | {effort} |
| P2 (Short-term) | 1-4 weeks | {action} | {finding IDs} | {effort} |
| P3 (Medium-term) | 1-3 months | {action} | {finding IDs} | {effort} |
| P4 (Long-term) | 3-6 months | {action} | {finding IDs} | {effort} |

### Security Posture Improvement

| Area | Current State | Target State | Gap | Recommended Investment |
|------|--------------|-------------|-----|----------------------|
| {area} | {current} | {target} | {gap} | {investment} |

### Comparison with Industry Standards

| Standard | Current Alignment | Target | Gap |
|----------|------------------|--------|-----|
| OWASP ASVS | {Level 0/1/2/3} | {target level} | {gap} |
| NIST CSF | {tier} | {target tier} | {gap} |
| CIS Controls | {IG level} | {target level} | {gap} |

---

## Configuration

### Configurable Rule Set (R-011)

| Parameter | Default | Override | Description |
|-----------|---------|----------|-------------|
| `audience` | executive | technical, executive, board | Target audience level |
| `include_kill_chain` | true | false | Include kill chain progress section |
| `include_standards_comparison` | true | false | Compare against industry standards |
| `finding_detail_level` | summary | summary, detailed | Finding detail in executive summary |
| `recommendation_timeframes` | standard | custom | Remediation timeline structure |

---

*Template Version: 1.0.0 | /red-team Skill | PROJ-010 Cyber Ops*
