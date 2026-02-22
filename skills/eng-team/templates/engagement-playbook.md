# /eng-team Engagement Playbook

> **Version:** 1.0.0
> **Skill:** /eng-team
> **Configurable Rule Set:** R-011
> **SSOT:** ADR-PROJ010-001 (Agent Team Architecture), ADR-PROJ010-002 (Skill Routing)

## Document Sections

| Section | Purpose |
|---------|---------|
| [Overview](#overview) | Playbook scope and when to use |
| [8-Step Workflow](#8-step-workflow) | Complete engagement lifecycle |
| [Phase Gates](#phase-gates) | Quality checkpoints between steps |
| [Engagement Setup](#engagement-setup) | How to start a new engagement |
| [Common Patterns](#common-patterns) | Typical engagement workflows |
| [Escalation Procedures](#escalation-procedures) | When and how to escalate |
| [Configuration](#configuration) | Configurable parameters |

---

## Overview

This playbook codifies the /eng-team's 8-step sequential phase-gate workflow into a repeatable engagement process. It guides practitioners from initial design through post-deployment incident response.

**When to use:** At the start of any /eng-team engagement to establish the workflow, define scope, and set quality expectations.

---

## 8-Step Workflow

### Step 1: Architecture & Threat Modeling (eng-architect)

| Attribute | Value |
|-----------|-------|
| **Agent** | eng-architect |
| **Input** | System requirements, scope definition |
| **Output** | Architecture decision records, threat model (STRIDE/DREAD minimum) |
| **Quality Gate** | Threat model completeness, trust boundary coverage |
| **Templates** | [Secure Design Review](secure-design-review.md), [Threat Model](threat-model.md) |

**Actions:**
1. Define system architecture with component diagram
2. Identify trust boundaries and data flows
3. Perform STRIDE analysis on each trust boundary
4. Score threats using DREAD methodology
5. Document architecture decision records (ADRs)
6. Map security requirements to components

### Step 2: Implementation Planning (eng-lead)

| Attribute | Value |
|-----------|-------|
| **Agent** | eng-lead |
| **Input** | Architecture output, threat model |
| **Output** | Implementation plan, coding standards, dependency governance |
| **Quality Gate** | Standards mapping completeness, dependency risk assessment |

**Actions:**
1. Translate architecture into implementation plan
2. Define coding standards with security requirements
3. Assess dependencies for known vulnerabilities
4. Map SSDF practices to implementation tasks
5. Assess OWASP SAMM maturity level

### Step 3: Parallel Implementation (eng-backend / eng-frontend / eng-infra)

| Attribute | Value |
|-----------|-------|
| **Agents** | eng-backend, eng-frontend, eng-infra (parallel) |
| **Input** | Implementation plan, security standards from eng-lead |
| **Output** | Secure implementation artifacts per domain |
| **Quality Gate** | Standards compliance, input validation, output encoding |

**Actions (per agent):**
- **eng-backend:** Server-side implementation with OWASP Top 10 compliance, API security, input validation
- **eng-frontend:** Client-side implementation with XSS prevention, CSP configuration, CORS hardening
- **eng-infra:** IaC security, container hardening, SBOM generation, SLSA compliance

### Step 4: Automated Security Scanning (eng-devsecops)

| Attribute | Value |
|-----------|-------|
| **Agent** | eng-devsecops |
| **Input** | Implementation artifacts from Step 3 |
| **Output** | Scan results, pipeline configurations, remediation guidance |
| **Quality Gate** | No critical/high findings unresolved |
| **Templates** | [Security Test Plan](security-test-plan.md) (automated section) |

**Actions:**
1. Configure SAST scanning
2. Configure DAST scanning
3. Run secrets scanning
4. Run dependency/SCA analysis
5. Run container scanning
6. Generate remediation guidance for findings

### Step 5: Security Testing (eng-qa)

| Attribute | Value |
|-----------|-------|
| **Agent** | eng-qa |
| **Input** | Implementation artifacts, scan results from Step 4 |
| **Output** | Test results, coverage reports, fuzzing findings |
| **Quality Gate** | >= 90% line coverage (H-20), all critical test cases pass |
| **Templates** | [Security Test Plan](security-test-plan.md) (testing section) |

**Actions:**
1. Execute security test cases (auth, authz, input validation)
2. Run fuzzing campaigns against critical endpoints
3. Execute property-based tests for security invariants
4. Measure and report code coverage
5. Document findings with reproduction steps

### Step 6: Manual Security Review (eng-security)

| Attribute | Value |
|-----------|-------|
| **Agent** | eng-security |
| **Input** | All prior artifacts |
| **Output** | Code review findings with CWE classifications, ASVS verification |
| **Quality Gate** | CWE Top 25 coverage, ASVS verification completeness |
| **Templates** | [Code Review Security Checklist](code-review-security-checklist.md) |

**Actions:**
1. Review code against CWE Top 25
2. Verify OWASP ASVS requirements
3. Check for business logic vulnerabilities
4. Assess cryptographic implementation
5. Document findings with severity and remediation guidance

### Step 7: Final Quality Gate (eng-reviewer)

| Attribute | Value |
|-----------|-------|
| **Agent** | eng-reviewer |
| **Input** | All prior artifacts |
| **Output** | Quality scores, compliance status, go/no-go decision |
| **Quality Gate** | >= 0.95 quality score for C2+ deliverables (via /adversary) |

**Actions:**
1. Review all artifacts for architecture compliance
2. Verify security standards compliance across all phases
3. Validate test coverage meets thresholds
4. For C2+ deliverables: invoke /adversary for adversarial quality review
5. Issue go/no-go decision

### Step 8: Incident Response Planning (eng-incident)

| Attribute | Value |
|-----------|-------|
| **Agent** | eng-incident |
| **Input** | All prior artifacts (esp. threat model, test findings) |
| **Output** | IR plans, runbooks, monitoring configuration |
| **Quality Gate** | Runbook coverage of identified threat scenarios |

**Actions:**
1. Create incident response plans based on threat model
2. Develop runbooks for each critical threat scenario
3. Define monitoring and alerting configuration
4. Establish vulnerability lifecycle management process
5. Document escalation procedures

---

## Phase Gates

| Gate | Between Steps | Pass Criteria | Fail Action |
|------|--------------|---------------|-------------|
| PG-1 | 1 → 2 | Threat model complete, all trust boundaries identified | Return to eng-architect |
| PG-2 | 2 → 3 | Implementation plan approved, standards defined | Return to eng-lead |
| PG-3 | 3 → 4 | Implementation artifacts produced, self-review passed | Return to respective agent |
| PG-4 | 4 → 5 | No unresolved critical/high scan findings | Return to eng-devsecops |
| PG-5 | 5 → 6 | Coverage >= 90%, critical tests pass | Return to eng-qa |
| PG-6 | 6 → 7 | CWE Top 25 reviewed, ASVS verified | Return to eng-security |
| PG-7 | 7 → 8 | Quality score >= 0.95 (C2+), compliance confirmed | Return to eng-reviewer |

---

## Engagement Setup

### New Engagement Checklist

1. [ ] Define engagement scope and system boundaries
2. [ ] Assign engagement ID (ENG-NNNN format)
3. [ ] Determine criticality level (C1-C4) per quality-enforcement.md
4. [ ] Select applicable compliance frameworks
5. [ ] Configure rule set parameters (R-011)
6. [ ] Create output directory: `skills/eng-team/output/{engagement-id}/`
7. [ ] Begin with Step 1 (eng-architect)

### Engagement ID Format

```
ENG-{NNNN}
Example: ENG-0042
```

---

## Common Patterns

| Pattern | Steps Used | When |
|---------|-----------|------|
| Full SDLC engagement | 1-8 | New system or major feature |
| Security review only | 6-7 | Existing code needing review |
| Architecture assessment | 1-2 | Design phase only |
| DevSecOps setup | 4-5 | CI/CD pipeline configuration |
| Incident response planning | 8 | Post-deployment preparation |
| Quick security check | 4, 6 | Rapid assessment of changes |

---

## Escalation Procedures

| Condition | Escalation |
|-----------|------------|
| Critical vulnerability found | Immediate notification to eng-lead and eng-reviewer |
| Quality gate fails twice | Escalate to eng-architect for design review |
| Compliance gap identified | Document in findings, escalate to eng-reviewer |
| Scope change required | Return to eng-architect for revised threat model |
| /adversary score < 0.92 | Mandatory revision cycle per H-14 |

---

## Configuration

### Configurable Rule Set (R-011)

| Parameter | Default | Override | Description |
|-----------|---------|----------|-------------|
| `workflow_steps` | 1-8 (all) | Any subset | Which steps to execute |
| `parallel_implementation` | true | false | Run Step 3 agents in parallel |
| `quality_threshold` | 0.95 | 0.92-1.0 | Minimum quality score for pass |
| `compliance_frameworks` | OWASP ASVS, NIST SSDF | Add/remove | Active compliance frameworks |
| `criticality_level` | C2 | C1-C4 | Default criticality |
| `auto_escalate_findings` | true | false | Auto-escalate critical findings |

---

*Template Version: 1.0.0 | /eng-team Skill | PROJ-010 Cyber Ops*
