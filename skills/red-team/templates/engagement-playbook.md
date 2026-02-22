# /red-team Engagement Playbook

> **Version:** 1.0.0
> **Skill:** /red-team
> **Configurable Rule Set:** R-011
> **SSOT:** ADR-PROJ010-001 (Agent Team Architecture), ADR-PROJ010-006 (Authorization)

## Document Sections

| Section | Purpose |
|---------|---------|
| [Overview](#overview) | Playbook scope and when to use |
| [Non-Linear Kill Chain Workflow](#non-linear-kill-chain-workflow) | Complete engagement lifecycle |
| [Mandatory Authorization](#mandatory-authorization) | Scope establishment requirements |
| [Phase Descriptions](#phase-descriptions) | Each engagement phase in detail |
| [Circuit Breaker Protocol](#circuit-breaker-protocol) | Safety checks at agent transitions |
| [Common Engagement Patterns](#common-engagement-patterns) | Typical engagement workflows |
| [Cross-Skill Integration](#cross-skill-integration) | Purple team integration points |
| [Configuration](#configuration) | Configurable parameters |

---

## Overview

This playbook codifies the /red-team's non-linear kill chain workflow into a repeatable engagement process. Unlike the /eng-team's sequential 8-step workflow, the /red-team follows an iterative engagement model where agents can be invoked in any order after scope establishment, with phase cycling explicitly supported.

**When to use:** At the start of any /red-team engagement to establish the workflow, review the authorization requirements, and plan the engagement approach.

---

## Non-Linear Kill Chain Workflow

### Mandatory Entry Point

Every engagement MUST begin with red-lead establishing scope. No operational agent can execute without an active scope document.

### Post-Scope Agent Availability

After scope establishment, agents are available based on the scope document's `agent_authorizations` and RoE settings:

| Agent | Availability | Condition |
|-------|-------------|-----------|
| red-recon | Available after scope | Standard authorization |
| red-vuln | Available after scope | Standard authorization |
| red-exploit | Available after scope | Standard authorization |
| red-privesc | Available after scope | Standard authorization |
| red-lateral | Available after scope | Standard authorization |
| red-persist | RoE-gated | `persistence_authorized: true` required |
| red-exfil | RoE-gated | `exfiltration_authorized: true` required |
| red-social | RoE-gated | `social_engineering_authorized: true` required |
| red-infra | Available after scope | Standard authorization |
| red-reporter | Always available | Can generate reports from existing findings |

### Phase Cycling

Real engagements are iterative. Common cycling patterns:

| Discovery | Triggers Return To | Reason |
|-----------|-------------------|--------|
| red-exploit finds new network segment | red-recon | New reconnaissance target discovered |
| red-privesc finds new service accounts | red-vuln | New credentials need vulnerability assessment |
| red-lateral reaches new subnet | red-recon | Expanded attack surface |
| red-recon finds new application | red-vuln + red-exploit | New attack vector |
| Any agent encounters scope ambiguity | red-lead | Scope review required |

---

## Mandatory Authorization

### Scope Establishment Checklist

1. [ ] User requests engagement (natural language or explicit)
2. [ ] red-lead creates scope document using [Pentest Engagement Template](pentest-engagement.md)
3. [ ] Targets defined with explicit in-scope/out-of-scope boundaries
4. [ ] Rules of Engagement documented (esp. RoE-gated agents)
5. [ ] Time window established
6. [ ] Technique allowlist reviewed
7. [ ] Agent authorizations confirmed
8. [ ] Evidence handling plan established
9. [ ] User provides authorization signature
10. [ ] Scope document persisted to `skills/red-team/output/{engagement-id}/`

### What Happens Without Authorization

Any agent invoked without scope immediately halts and returns:
```
AUTHORIZATION REQUIRED: No active scope document found for this engagement.
red-lead must establish scope before any operational agent can proceed.
```

---

## Phase Descriptions

### Phase 1: Scope & Authorization (red-lead)

| Attribute | Value |
|-----------|-------|
| **Agent** | red-lead |
| **MANDATORY** | Yes -- always first |
| **Output** | Scope document, engagement plan |
| **Template** | [Pentest Engagement](pentest-engagement.md) |
| **Criticality** | C4 (always -- irreversible authorization) |

### Phase 2: Reconnaissance (red-recon)

| Attribute | Value |
|-----------|-------|
| **Agent** | red-recon |
| **ATT&CK Tactics** | TA0043 (Reconnaissance) |
| **Output** | Attack surface map, OSINT findings, service enumeration |
| **Feeds Into** | red-vuln (vulnerabilities), red-exploit (targets), eng-architect (threat intelligence) |

### Phase 3: Vulnerability Analysis (red-vuln)

| Attribute | Value |
|-----------|-------|
| **Agent** | red-vuln |
| **ATT&CK Tactics** | Analysis support |
| **Output** | Vulnerability inventory, risk scores, exploit availability |
| **Template** | [Vulnerability Report](vulnerability-report.md) |
| **Feeds Into** | red-exploit (exploitation targets), eng-infra/eng-devsecops (validation) |

### Phase 4: Exploitation (red-exploit)

| Attribute | Value |
|-----------|-------|
| **Agent** | red-exploit |
| **ATT&CK Tactics** | TA0001 (Initial Access), TA0002 (Execution), TA0040 (Impact) |
| **Output** | Exploitation methodology, PoC guidance, initial access documentation |
| **Feeds Into** | red-privesc (post-exploitation), eng-security/eng-backend/eng-frontend (secure code validation) |

### Phase 5: Privilege Escalation (red-privesc)

| Attribute | Value |
|-----------|-------|
| **Agent** | red-privesc |
| **ATT&CK Tactics** | TA0004 (Privilege Escalation), TA0006 (Credential Access) |
| **Output** | Escalation paths, credential findings, token analysis |
| **Feeds Into** | red-lateral (movement), red-persist (elevated persistence) |

### Phase 6: Lateral Movement (red-lateral)

| Attribute | Value |
|-----------|-------|
| **Agent** | red-lateral |
| **ATT&CK Tactics** | TA0008 (Lateral Movement), TA0007 (Discovery) |
| **Output** | Network map, pivot methodology, discovery findings |
| **Triggers** | Phase cycling back to red-recon for newly discovered segments |

### Phase 7: Post-Exploitation (red-persist, red-exfil) -- RoE-GATED

| Attribute | Value |
|-----------|-------|
| **Agents** | red-persist (RoE-gated), red-exfil (RoE-gated) |
| **ATT&CK Tactics** | TA0003, TA0005 (persist), TA0009, TA0010 (exfil) |
| **Output** | Persistence methodology, exfiltration channel analysis |
| **Feeds Into** | eng-incident (IR validation) |

### Phase 8: Reporting (red-reporter)

| Attribute | Value |
|-----------|-------|
| **Agent** | red-reporter |
| **MANDATORY** | Yes -- engagement not complete without report |
| **Output** | Final engagement report, executive summary, remediation guidance |
| **Templates** | [Executive Summary](executive-summary.md), [Remediation Tracking](remediation-tracking.md) |

### Supporting: Infrastructure (red-infra)

| Attribute | Value |
|-----------|-------|
| **Agent** | red-infra |
| **ATT&CK Tactics** | TA0042, TA0011, TA0005 |
| **Invocable** | Any time after scope -- not phase-dependent |
| **Output** | C2 infrastructure methodology, payload guidance, redirector setup |

### Supporting: Social Engineering (red-social) -- RoE-GATED

| Attribute | Value |
|-----------|-------|
| **Agent** | red-social |
| **ATT&CK Tactics** | TA0043, TA0001 |
| **RoE-Gated** | `social_engineering_authorized: true` required |
| **Output** | Social engineering campaign methodology |

---

## Circuit Breaker Protocol

At every agent transition, the orchestrator performs:

1. **Scope revalidation:** Target still within authorized scope?
2. **Time window check:** Engagement still within authorized time?
3. **Technique check:** Next agent's techniques in allowlist?
4. **Agent authorization:** Next agent in agent_authorizations?
5. **RoE gate:** If RoE-gated, explicitly authorized?
6. **Cascading failure detection:** Any prior agent anomalies?

**If ANY check fails:** HALT and route to red-lead for scope review.

---

## Common Engagement Patterns

| Pattern | Agents Used | When |
|---------|------------|------|
| Full pentest | All (per RoE) | Comprehensive assessment |
| External pentest | red-lead, red-recon, red-vuln, red-exploit, red-reporter | External attack surface |
| Web app assessment | red-lead, red-recon, red-vuln, red-exploit, red-reporter | Application-focused |
| Red team exercise | All including RoE-gated | Adversary simulation |
| Vulnerability assessment | red-lead, red-recon, red-vuln, red-reporter | Assessment without exploitation |
| Purple team validation | red-* + eng-* integration points | Adversarial-collaborative |
| Social engineering | red-lead, red-social, red-reporter | Phishing/pretexting assessment |
| Post-incident | red-lead, red-recon, red-vuln, red-reporter | Assess impact of known breach |

---

## Cross-Skill Integration

Four purple team integration points with /eng-team:

| Integration Point | red-team Source | eng-team Target | Data |
|-------------------|----------------|-----------------|------|
| Threat-Informed Architecture | red-recon | eng-architect | Adversary TTPs, threat landscape |
| Attack Surface Validation | red-recon, red-vuln | eng-infra, eng-devsecops | Validation results |
| Secure Code vs. Exploitation | red-exploit, red-privesc | eng-security, eng-backend, eng-frontend | Exploitation results |
| IR Validation | red-persist, red-lateral, red-exfil | eng-incident | Exercise results, detection gaps |

---

## Configuration

### Configurable Rule Set (R-011)

| Parameter | Default | Override | Description |
|-----------|---------|----------|-------------|
| `engagement_type` | external-pentest | internal, webapp, red-team, vuln-assessment | Default engagement pattern |
| `circuit_breaker` | enabled | disabled (not recommended) | Agent transition safety checks |
| `phase_cycling` | enabled | disabled | Allow iterative phase cycling |
| `reporting_frequency` | end-of-engagement | interim-weekly, end-of-engagement | When red-reporter generates reports |
| `evidence_classification` | standard | minimal, standard, comprehensive | Evidence collection depth |
| `purple_team_integration` | disabled | enabled | Activate cross-skill integration points |

---

*Template Version: 1.0.0 | /red-team Skill | PROJ-010 Cyber Ops*
