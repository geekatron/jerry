---
name: eng-team
description: >
  Secure engineering team skill providing methodology guidance for building
  security-hardened software. Invoked when users request system design,
  implementation, code review, testing, CI/CD security, or incident response
  with security considerations. Routes to 10 specialized agents covering
  architecture through post-deployment. Integrates NIST SSDF governance,
  Microsoft SDL phases, OWASP ASVS verification, SLSA supply chain integrity,
  and DevSecOps automation patterns.
version: "1.0.0"
agents:
  - eng-architect
  - eng-lead
  - eng-backend
  - eng-frontend
  - eng-infra
  - eng-devsecops
  - eng-qa
  - eng-security
  - eng-reviewer
  - eng-incident
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, WebSearch, WebFetch, mcp__context7__resolve-library-id, mcp__context7__query-docs
activation-keywords:
  - "secure design"
  - "threat model"
  - "secure architecture"
  - "STRIDE"
  - "DREAD"
  - "secure implementation"
  - "code review for security"
  - "SAST"
  - "DAST"
  - "supply chain security"
  - "incident response"
  - "DevSecOps"
  - "OWASP"
  - "ASVS"
  - "CWE"
  - "CIS benchmark"
  - "SSDF"
  - "SLSA"
  - "build a secure"
  - "security requirements"
---

# Eng-Team Skill

> **Version:** 1.0.0
> **Framework:** Jerry Eng-Team
> **Constitutional Compliance:** Jerry Constitution v1.0
> **SSOT References:** ADR-PROJ010-001 (Agent Team Architecture), ADR-PROJ010-002 (Skill Routing & Invocation), ADR-PROJ010-003 (LLM Portability)
> **Project:** PROJ-010 Cyber Ops | EPIC-003 (/eng-team Skill Build) | FEAT-020 through FEAT-025

## Document Sections

| Section | Purpose |
|---------|---------|
| [Document Audience](#document-audience-triple-lens) | Triple-Lens audience guide |
| [Purpose](#purpose) | Skill overview and key capabilities |
| [When to Use This Skill](#when-to-use-this-skill) | Activation triggers |
| [Available Agents](#available-agents) | 10-agent roster with roles and output locations |
| [Invoking an Agent](#invoking-an-agent) | Three invocation methods with examples |
| [Orchestration Flow](#orchestration-flow) | 8-step sequential phase-gate workflow |
| [State Passing Between Agents](#state-passing-between-agents) | Output keys and handoff data |
| [Mandatory Persistence](#mandatory-persistence-p-002) | P-002 file persistence requirements |
| [Layered SDLC Governance](#layered-sdlc-governance) | 5-layer governance model (AD-008) |
| [Adversarial Quality Mode](#adversarial-quality-mode) | /adversary integration and criticality escalation |
| [Constitutional Compliance](#constitutional-compliance) | Governing principles |
| [Quick Reference](#quick-reference) | Common workflows and agent selection hints |
| [Agent Details](#agent-details) | Agent file paths |
| [References and Traceability](#references-and-traceability) | ADR baseline, architecture decisions, research provenance |

## Document Audience (Triple-Lens)

This SKILL.md serves multiple audiences:

| Level | Audience | Sections to Focus On |
|-------|----------|---------------------|
| **L0 (ELI5)** | New users, stakeholders | [Purpose](#purpose), [When to Use This Skill](#when-to-use-this-skill), [Quick Reference](#quick-reference) |
| **L1 (Engineer)** | Developers invoking agents | [Invoking an Agent](#invoking-an-agent), [Agent Details](#agent-details), [Adversarial Quality Mode](#adversarial-quality-mode) |
| **L2 (Architect)** | Workflow designers | [Orchestration Flow](#orchestration-flow), [State Passing Between Agents](#state-passing-between-agents), [Layered SDLC Governance](#layered-sdlc-governance) |

---

## Purpose

The Eng-Team skill provides a structured secure software engineering framework through 10 specialized agents. Each agent produces **persistent artifacts** that survive context compaction, enforce security standards at every phase, and build a cumulative knowledge base of security-hardened engineering decisions.

### Key Capabilities

- **Secure Architecture** -- System design with threat modeling (STRIDE/DREAD/PASTA) and architecture decision records
- **Implementation Planning** -- Standards enforcement, dependency governance, and SAMM maturity assessment
- **Secure Backend Engineering** -- Server-side implementation with OWASP Top 10 and ASVS verification
- **Secure Frontend Engineering** -- Client-side implementation with XSS prevention, CSP, and CORS hardening
- **Secure Infrastructure** -- IaC security, container hardening, SBOM generation, and SLSA supply chain integrity
- **DevSecOps Automation** -- SAST/DAST pipeline integration, secrets scanning, dependency analysis
- **Security QA** -- Test strategy, fuzzing, property-based testing, and coverage enforcement
- **Manual Security Review** -- Secure code review against CWE Top 25 and ASVS requirements
- **Final Quality Gate** -- Architecture compliance with /adversary integration for C2+ deliverables
- **Incident Response** -- Post-deployment IR runbooks, vulnerability lifecycle, and remediation tracking

---

## When to Use This Skill

Activate when:

- Designing a new system or service that requires security hardening
- Performing threat modeling on an architecture
- Implementing backend or frontend components with security requirements
- Setting up secure CI/CD pipelines and DevSecOps automation
- Writing security-focused test cases or fuzzing campaigns
- Conducting manual secure code review
- Creating incident response plans or runbooks
- Reviewing deliverables against security standards (OWASP, NIST, CIS, SLSA)
- Planning infrastructure with container security and supply chain integrity

---

## Available Agents

| Agent | Role | Output Location |
|-------|------|-----------------|
| `eng-architect` | Solution Architect and Threat Modeler | `skills/eng-team/output/{engagement-id}/eng-architect-{topic-slug}.md` |
| `eng-lead` | Engineering Lead and Standards Enforcer | `skills/eng-team/output/{engagement-id}/eng-lead-{topic-slug}.md` |
| `eng-backend` | Secure Backend Engineer | `skills/eng-team/output/{engagement-id}/eng-backend-{topic-slug}.md` |
| `eng-frontend` | Secure Frontend Engineer | `skills/eng-team/output/{engagement-id}/eng-frontend-{topic-slug}.md` |
| `eng-infra` | Secure Infrastructure Engineer | `skills/eng-team/output/{engagement-id}/eng-infra-{topic-slug}.md` |
| `eng-devsecops` | DevSecOps Pipeline Engineer | `skills/eng-team/output/{engagement-id}/eng-devsecops-{topic-slug}.md` |
| `eng-qa` | Security QA Engineer | `skills/eng-team/output/{engagement-id}/eng-qa-{topic-slug}.md` |
| `eng-security` | Security Code Review Specialist | `skills/eng-team/output/{engagement-id}/eng-security-{topic-slug}.md` |
| `eng-reviewer` | Final Review Gate and Quality Enforcer | `skills/eng-team/output/{engagement-id}/eng-reviewer-{topic-slug}.md` |
| `eng-incident` | Incident Response Specialist | `skills/eng-team/output/{engagement-id}/eng-incident-{topic-slug}.md` |

All agents produce output at three levels:
- **L0 (Executive Summary):** Accessible summary for non-technical stakeholders. Answers "What does this mean for the project?"
- **L1 (Technical Detail):** Implementation-focused content with specifics, code examples, and configuration guidance.
- **L2 (Strategic Implications):** Trade-offs, long-term risks, alignment with security posture, and architectural evolution.

---

## Invoking an Agent

### Option 1: Natural Language Request

Simply describe what you need:

```
"Design a secure microservice architecture with threat model"
"Review this API implementation for OWASP Top 10 vulnerabilities"
"Set up a DevSecOps pipeline with SAST and container scanning"
"Create an incident response runbook for credential compromise"
"Test this authentication flow with fuzzing and boundary testing"
```

The orchestrator selects the appropriate agent based on keywords and context.

### Option 2: Explicit Agent Request

Request a specific agent:

```
"Use eng-architect to create a threat model for the payment service"
"Have eng-devsecops design the CI/CD security pipeline"
"I need eng-security to review the authentication module"
```

### Option 3: Native Agent Invocation

Agents are registered via `plugin.json` and discovered by Claude Code automatically. The orchestrator invokes them as named subagents:

```python
Task(
    description="eng-architect: Threat model for payment service",
    subagent_type="eng-architect",
    prompt="""
## ENG CONTEXT (REQUIRED)
- **Engagement ID:** ENG-0042
- **Topic:** Payment Service Threat Model

## TASK
Produce a threat model for the payment service using STRIDE analysis
with DREAD risk scoring. Include architecture diagrams, trust boundaries,
data flow analysis, and prioritized threat matrix.
"""
)
```

Claude Code enforces the agent's `tools` frontmatter — eng-architect only has access to Read, Write, Edit, Glob, Grep, Bash, WebSearch, WebFetch and the Context7 MCP server.

---

## Orchestration Flow

### 8-Step Sequential Phase-Gate Workflow

The /eng-team skill follows an 8-step sequential workflow with phase gates. Each step must complete before the next begins, except Step 3 where three agents execute in parallel.

```
Step 1: eng-architect (Design + Threat Model)
    |
Step 2: eng-lead (Implementation Plan + Security Standards)
    |
Step 3: eng-backend / eng-frontend / eng-infra (Parallel Implementation)
    |
Step 4: eng-devsecops (Automated Security Scans)
    |
Step 5: eng-qa (Testing + Fuzzing)
    |
Step 6: eng-security (Manual Security Review)
    |
Step 7: eng-reviewer (Final Gate + /adversary for C2+)
    |
Step 8: eng-incident (IR Plan + Runbooks, Post-Deployment)
```

**Step 1 -- eng-architect:** Produces the system design, architecture decision records, and threat model (STRIDE/DREAD at minimum). All subsequent agents consume this as their security context.

**Step 2 -- eng-lead:** Receives the architecture and threat model. Produces the implementation plan, coding standards, dependency governance decisions, and security standards mapping.

**Step 3 -- eng-backend / eng-frontend / eng-infra (parallel):** Three agents execute in parallel. Each receives the implementation plan and security standards from eng-lead. Backend handles server-side, frontend handles client-side, infra handles IaC and containers.

**Step 4 -- eng-devsecops:** Receives implementation artifacts. Configures and runs automated security scans: SAST, DAST, secrets scanning, container scanning, dependency analysis. Produces scan results and remediation guidance.

**Step 5 -- eng-qa:** Receives implementation artifacts and scan results. Produces security test cases, fuzzing campaigns, property-based tests, and coverage reports.

**Step 6 -- eng-security:** Receives all prior artifacts. Performs manual secure code review against CWE Top 25 and OWASP ASVS. Produces findings with severity ratings and remediation guidance.

**Step 7 -- eng-reviewer:** Mandatory final gate. Reviews all artifacts for architecture compliance, security standards compliance, and test coverage. Invokes /adversary for C2+ deliverables per R-013 at >= 0.95 quality threshold.

**Step 8 -- eng-incident:** Post-deployment phase. Produces incident response plans, runbooks, monitoring configuration, and vulnerability lifecycle management. Activates independently of the build workflow.

---

## State Passing Between Agents

Agents reference each other's output using state keys:

| Agent | Output Key | Provides |
|-------|------------|----------|
| eng-architect | `architect_output` | System design, threat model, ADRs, trust boundaries |
| eng-lead | `lead_output` | Implementation plan, standards mapping, dependency decisions |
| eng-backend | `backend_output` | Server-side implementation, API security artifacts |
| eng-frontend | `frontend_output` | Client-side implementation, CSP/CORS configuration |
| eng-infra | `infra_output` | IaC templates, container configs, SBOM |
| eng-devsecops | `devsecops_output` | Scan results, pipeline configs, remediation list |
| eng-qa | `qa_output` | Test results, coverage reports, fuzzing findings |
| eng-security | `security_output` | Code review findings, ASVS verification results |
| eng-reviewer | `reviewer_output` | Final gate decision, quality scores, compliance status |
| eng-incident | `incident_output` | IR plans, runbooks, monitoring configuration |

---

## Mandatory Persistence (P-002)

All agents MUST persist their output to files. This ensures:

1. **Context Rot Resistance** -- Findings survive session compaction
2. **Knowledge Accumulation** -- Artifacts build project security knowledge base
3. **Auditability** -- Security decisions can be traced and reviewed
4. **Compliance Evidence** -- Persisted artifacts serve as compliance documentation

### Output Structure

```
skills/eng-team/output/
└── {engagement-id}/
    ├── eng-architect-{topic-slug}.md
    ├── eng-lead-{topic-slug}.md
    ├── eng-backend-{topic-slug}.md
    ├── eng-frontend-{topic-slug}.md
    ├── eng-infra-{topic-slug}.md
    ├── eng-devsecops-{topic-slug}.md
    ├── eng-qa-{topic-slug}.md
    ├── eng-security-{topic-slug}.md
    ├── eng-reviewer-{topic-slug}.md
    └── eng-incident-{topic-slug}.md
```

---

## Layered SDLC Governance

The /eng-team skill references a 5-layer governance model. Every agent maps to one or more layers:

| Layer | Framework | Purpose | Agents |
|-------|-----------|---------|--------|
| 1. Governance | NIST SP 800-218 SSDF (4 practice groups, 19 practices, 43 tasks) | Organizational security practices | eng-architect, eng-lead, eng-reviewer |
| 2. Lifecycle | Microsoft SDL (5 phases: Requirements, Design, Implementation, Verification, Release) | Phase-gated secure development | All agents |
| 3. Assessment | OWASP SAMM (3 maturity levels across 15 practices) | Maturity measurement | eng-lead, eng-security |
| 4. Supply Chain | Google SLSA (4 build levels) | Build integrity and provenance | eng-infra, eng-devsecops |
| 5. Automation | DevSecOps patterns (CI/CD security gates) | Automated enforcement | eng-devsecops, eng-qa |

Every security activity includes SSDF practice references (e.g., PW.7 for code review, PS.1 for secrets management).

---

## Adversarial Quality Mode

> **SSOT Reference:** `.context/rules/quality-enforcement.md` -- all thresholds, strategy IDs, and criticality levels are defined there. NEVER hardcode values; always reference the SSOT.

The /eng-team skill integrates the adversarial quality framework defined in EPIC-002. Security-critical deliverables receive elevated scrutiny.

### Criticality-Based Activation

Strategy activation follows the SSOT criticality levels (C1-C4). See `.context/rules/quality-enforcement.md` (Criticality Levels section) for the authoritative mapping.

| Level | Eng-Team Context | Required Strategies | Typical Scenario |
|-------|-----------------|---------------------|------------------|
| **C1 (Routine)** | Minor config changes, documentation | S-010 (Self-Refine) | Updating a CSP header |
| **C2 (Standard)** | Feature implementation, test suites | S-007, S-002, S-014 | New API endpoint with auth |
| **C3 (Significant)** | Architecture decisions, IaC changes | C2 + S-004, S-012, S-013 | New service architecture |
| **C4 (Critical)** | Security architecture, auth systems | All 10 selected strategies | Authentication redesign |

### Threat Modeling Escalation

eng-architect applies threat modeling depth based on criticality:

| Level | Threat Modeling Approach |
|-------|------------------------|
| C1 | STRIDE only |
| C2 | STRIDE + DREAD scoring |
| C3 | STRIDE + DREAD + Attack Trees |
| C4 | STRIDE + DREAD + Attack Trees + PASTA stages 4-7 |
| PII involvement | Add LINDDUN to any level |

### eng-reviewer Quality Gate

eng-reviewer invokes /adversary for C2+ deliverables per R-013 at >= 0.95 quality threshold. Below threshold means the deliverable is rejected and returned for revision. No exceptions.

### Mandatory Self-Review (H-15)

Per H-15 (HARD rule), all /eng-team agents MUST perform self-review using S-010 (Self-Refine) before presenting any deliverable.

Per H-16 (HARD rule), agents MUST apply S-003 (Steelman Technique) before critiquing -- strengthen the argument first, then challenge it.

---

## Constitutional Compliance

All agents adhere to the **Jerry Constitution v1.0**:

| Principle | Requirement |
|-----------|-------------|
| P-001: Truth and Accuracy | Findings based on evidence, sources cited |
| P-002: File Persistence | All outputs persisted to files |
| P-003: No Recursive Subagents | Agents cannot spawn nested agents |
| P-004: Explicit Provenance | Reasoning and sources documented |
| P-011: Evidence-Based | Recommendations tied to evidence |
| P-020: User Authority | Never override user decisions |
| P-022: No Deception | Limitations and gaps disclosed |

---

## Quick Reference

### Common Workflows

| Need | Agent | Command Example |
|------|-------|-----------------|
| Threat model | eng-architect | "Create a STRIDE threat model for the auth service" |
| Implementation plan | eng-lead | "Plan the implementation for the new API gateway" |
| Secure backend code | eng-backend | "Implement the user registration endpoint with input validation" |
| Secure frontend code | eng-frontend | "Add CSP headers and XSS protection to the dashboard" |
| Infrastructure setup | eng-infra | "Design the container security configuration with SBOM" |
| CI/CD security | eng-devsecops | "Set up SAST/DAST scanning in the CI pipeline" |
| Security testing | eng-qa | "Write security test cases with fuzzing for the auth flow" |
| Code security review | eng-security | "Review the payment module for CWE Top 25 vulnerabilities" |
| Final review gate | eng-reviewer | "Final review of the release candidate against all standards" |
| Incident response | eng-incident | "Create an IR runbook for credential compromise scenarios" |

### Agent Selection Hints

| Keywords | Likely Agent |
|----------|--------------|
| design, architecture, threat model, STRIDE, DREAD, ADR, trust boundary | eng-architect |
| plan, standards, dependencies, code standards, lead, SAMM | eng-lead |
| backend, API, server, auth, database, input validation, OWASP Top 10 | eng-backend |
| frontend, XSS, CSP, CORS, client, browser, output encoding | eng-frontend |
| infrastructure, IaC, container, secrets, SBOM, SLSA, supply chain | eng-infra |
| pipeline, SAST, DAST, CI/CD, scanning, DevSecOps, automation | eng-devsecops |
| test, QA, fuzzing, coverage, boundary testing, property-based | eng-qa |
| code review, CWE, ASVS, manual review, vulnerability, security review | eng-security |
| final review, quality gate, compliance, release, /adversary | eng-reviewer |
| incident, runbook, response, monitoring, post-deployment, remediation | eng-incident |

---

## Agent Details

For detailed agent specifications, see:

- `skills/eng-team/agents/eng-architect.md`
- `skills/eng-team/agents/eng-lead.md`
- `skills/eng-team/agents/eng-backend.md`
- `skills/eng-team/agents/eng-frontend.md`
- `skills/eng-team/agents/eng-infra.md`
- `skills/eng-team/agents/eng-devsecops.md`
- `skills/eng-team/agents/eng-qa.md`
- `skills/eng-team/agents/eng-security.md`
- `skills/eng-team/agents/eng-reviewer.md`
- `skills/eng-team/agents/eng-incident.md`

---

## References and Traceability

### Architecture Decision Records

| ADR | Title | Relevance |
|-----|-------|-----------|
| [ADR-PROJ010-001](../../projects/PROJ-010-cyber-ops/decisions/ADR-PROJ010-001-agent-team-architecture.md) | Agent Team Architecture | 10-agent roster (AD-002), 8-step workflow, capability boundaries, SDLC governance (AD-008), threat modeling methodology (AD-009), standalone design (AD-010) |
| [ADR-PROJ010-002](../../projects/PROJ-010-cyber-ops/decisions/ADR-PROJ010-002-skill-routing-invocation.md) | Skill Routing & Invocation | SKILL.md structure, keyword triggers, routing table, workflow patterns, circuit breaker integration |
| [ADR-PROJ010-003](../../projects/PROJ-010-cyber-ops/decisions/ADR-PROJ010-003-llm-portability.md) | LLM Portability | 38-field portable agent schema, body_format: markdown, RCCF prompt assembly, provider adapters |

### Architecture Decisions Implemented

| AD | Title | Implementation |
|----|-------|---------------|
| AD-001 | Methodology-First Design | All agents produce methodology guidance, not autonomous execution |
| AD-002 | 21-Agent Roster (10 eng + 11 red) | 10 /eng-team agents defined per roster specification |
| AD-008 | Five-Layer SDLC Governance | SSDF + MS SDL + SAMM + SLSA + DevSecOps in Layered SDLC Governance section |
| AD-009 | STRIDE+DREAD Default Threat Modeling | eng-architect criticality-based escalation (C1-C4) with LINDDUN for PII |
| AD-010 | Standalone Capable Design | All agents implement 3-level tool degradation (Level 0/1/2) |

### Phase 1 Research Provenance

| Artifact | Title | Contribution |
|----------|-------|-------------|
| A-001 through A-004 | Role Completeness Analysis | Validated 10-agent roster against elite organizations (Google, Microsoft, CrowdStrike, Mandiant) |
| B-003 | Security Standards Analysis | OWASP, NIST, CIS, SANS standards mapped to per-agent responsibilities |
| F-001 | SDLC Framework Comparison | MS SDL phase-to-agent mapping, SSDF practice-to-agent mapping |
| S-002 | Architecture Implications Synthesis | Agent architecture specification input, handoff protocols, cross-skill integration |

### Standards References

| Standard | Version | URL |
|----------|---------|-----|
| NIST SP 800-218 SSDF | v1.1 (2022) | https://csrc.nist.gov/publications/detail/sp/800-218/final |
| Microsoft SDL | 2024 | https://www.microsoft.com/en-us/securityengineering/sdl |
| OWASP ASVS | v5.0 (2025) | https://owasp.org/www-project-application-security-verification-standard/ |
| OWASP Top 10 | 2021 | https://owasp.org/www-project-top-ten/ |
| CWE Top 25 | 2025 | https://cwe.mitre.org/top25/archive/2025/2025_cwe_top25.html |
| Google SLSA | v1.0 (2023) | https://slsa.dev/spec/v1.0/ |
| OWASP SAMM | v2.0 | https://owaspsamm.org/ |
| CIS Benchmarks | Various | https://www.cisecurity.org/cis-benchmarks |
| NIST CSF | v2.0 (2024) | https://www.nist.gov/cyberframework |
| NIST SP 800-61 | r3 (2024) | https://csrc.nist.gov/publications/detail/sp/800-61/rev-3/final |

### Feature Traceability

| Feature | Title | Status |
|---------|-------|--------|
| FEAT-020 | SKILL.md & Routing | Completed |
| FEAT-021 | Architecture Agents (eng-architect, eng-lead) | Completed |
| FEAT-022 | Implementation Agents (eng-backend, eng-frontend, eng-infra) | Completed |
| FEAT-023 | Quality Agents (eng-qa, eng-security, eng-reviewer, eng-devsecops, eng-incident) | Completed |
| FEAT-024 | Templates & Playbook | Pending |
| FEAT-025 | /adversary Integration | Pending |

---

*Skill Version: 1.0.0*
*Constitutional Compliance: Jerry Constitution v1.0*
*PROJ-010: Cyber Ops -- Secure Engineering Team*
*Last Updated: 2026-02-22*
