# /eng-team User Guide

> Secure engineering methodology guidance through 10 specialized agents covering the full software development lifecycle.

**Version:** 1.0.0 | **Skill:** /eng-team | **Last Updated:** 2026-02-22
**SSOT:** ADR-PROJ010-001 (Agent Team Architecture), ADR-PROJ010-002 (Skill Routing)

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Quick Start](#l0-quick-start) | Get productive in 5 minutes |
| [Skill Overview](#skill-overview) | What /eng-team does and when to use it |
| [Agent Registry](#agent-registry) | All 10 agents with capabilities and use cases |
| [Choosing the Right Agent](#choosing-the-right-agent) | Decision table for agent selection |
| [L1: Workflow Usage](#l1-workflow-usage) | End-to-end scenarios with step-by-step examples |
| [How to Invoke Agents](#how-to-invoke-agents) | Three invocation methods |
| [The 8-Step Workflow](#the-8-step-workflow) | Sequential phase-gate process |
| [Output Levels](#output-levels) | Understanding L0, L1, L2 output |
| [L2: Advanced Configuration](#l2-advanced-configuration) | Rule sets, governance models, integration points |
| [Configuration Options](#configuration-options) | Customizing SDLC governance and threat modeling |
| [Integration Points](#integration-points) | Working with /adversary, /problem-solving, /nasa-se, /red-team |
| [Engagement Management](#engagement-management) | Engagement IDs, output organization, artifact persistence |
| [Common Scenarios](#common-scenarios) | Real-world usage patterns |
| [Troubleshooting and FAQ](#troubleshooting-and-faq) | Common issues and solutions |
| [References](#references) | Standards, ADRs, and source material |

---

## L0: Quick Start

### What Is /eng-team?

The /eng-team skill provides security-focused software engineering guidance through 10 specialized agents. Each agent covers a specific phase of the secure development lifecycle -- from architecture and threat modeling through implementation, testing, code review, and incident response.

The skill produces **methodology guidance and artifacts**, not autonomous code execution. Agents guide you through security best practices, generate threat models, review code for vulnerabilities, design CI/CD security pipelines, and create incident response plans. All outputs are persisted as files for auditability and reuse.

### Your First Engagement in 3 Steps

**Step 1: Describe what you need.**

```
"Design a secure microservice architecture for a payment processing system"
```

The orchestrator routes your request to the appropriate agent (in this case, eng-architect) based on keywords in your request.

**Step 2: Review the output.**

The agent produces a file at `skills/eng-team/output/{engagement-id}/eng-architect-{topic}.md` containing:

- **L0 (Executive Summary):** High-level overview for stakeholders
- **L1 (Technical Detail):** Implementation-specific guidance with code examples
- **L2 (Strategic Implications):** Long-term architecture considerations

**Step 3: Continue the workflow.**

Ask for the next step:

```
"Now create the implementation plan based on this architecture"
```

The orchestrator routes to eng-lead, which builds on eng-architect's output.

### Quick Agent Reference

| I need to... | Ask for... |
|--------------|------------|
| Design a system with security | eng-architect |
| Plan the implementation | eng-lead |
| Build a secure backend | eng-backend |
| Build a secure frontend | eng-frontend |
| Harden infrastructure | eng-infra |
| Set up automated security scanning | eng-devsecops |
| Write security test cases | eng-qa |
| Review code for vulnerabilities | eng-security |
| Run the final quality gate | eng-reviewer |
| Create incident response plans | eng-incident |

---

## Skill Overview

### Purpose

The /eng-team skill provides a structured secure software engineering framework. It integrates five industry-standard governance models into a single cohesive workflow:

| Governance Layer | Framework | What It Provides |
|-----------------|-----------|------------------|
| Governance | NIST SP 800-218 SSDF | Organizational security practices (19 practices, 43 tasks) |
| Lifecycle | Microsoft SDL | Phase-gated secure development (5 phases) |
| Assessment | OWASP SAMM | Security maturity measurement (3 levels, 15 practices) |
| Supply Chain | Google SLSA | Build integrity and provenance (4 build levels) |
| Automation | DevSecOps patterns | Automated CI/CD security gates |

### When to Use /eng-team

Use this skill when you are:

- Designing a new system or service that needs security hardening
- Performing threat modeling on an existing or proposed architecture
- Implementing backend or frontend components with security requirements
- Setting up secure CI/CD pipelines with automated scanning
- Writing security-focused test cases or planning fuzzing campaigns
- Conducting manual secure code review
- Creating incident response plans or post-deployment runbooks
- Reviewing deliverables against security standards (OWASP, NIST, CIS, SLSA)

### When NOT to Use /eng-team

- For penetration testing or offensive security operations, use `/red-team`
- For adversarial quality reviews of deliverables, use `/adversary`
- For general security research without an engineering context, use `/problem-solving`

### Key Design Principles

1. **Methodology-first.** Agents provide structured guidance and produce artifacts. They do not autonomously write production code or deploy infrastructure (AD-001).
2. **Standalone capable.** Every agent works without external tools. Tools enhance evidence quality but are never required for reasoning (AD-010).
3. **Persistent output.** All artifacts are saved to files. Nothing is lost to context window limitations (P-002).

---

## Agent Registry

### eng-architect -- Solution Architect and Threat Modeler

| Attribute | Value |
|-----------|-------|
| **Role** | System design, architecture decisions, threat modeling |
| **Workflow Position** | Step 1 (mandatory first step for full workflow) |
| **Key Standards** | NIST CSF 2.0, STRIDE, DREAD, PASTA, LINDDUN, Attack Trees |
| **Model** | opus |

**Capabilities:**
- Produces system architecture designs with explicit security constraints
- Creates architecture decision records (ADRs) with security rationale
- Performs threat modeling using STRIDE/DREAD at minimum, escalating to PASTA and Attack Trees for higher criticality
- Defines trust boundaries, data flow diagrams, and attack surface maps
- Maps decisions to NIST CSF 2.0 functions (Identify, Protect, Detect, Respond, Recover)
- Consumes threat intelligence from /red-team when available (Integration Point 1)

**Threat Modeling Depth by Criticality:**

| Criticality | Approach |
|-------------|----------|
| C1 (Routine) | STRIDE only |
| C2 (Standard) | STRIDE + DREAD scoring |
| C3 (Significant) | STRIDE + DREAD + Attack Trees |
| C4 (Critical) | STRIDE + DREAD + Attack Trees + PASTA stages 4-7 |
| PII involved | Add LINDDUN to any level |

**Example request:** "Create a STRIDE threat model for the authentication service with DREAD risk scoring"

---

### eng-lead -- Engineering Lead and Standards Enforcer

| Attribute | Value |
|-----------|-------|
| **Role** | Implementation planning, code standards, dependency governance |
| **Workflow Position** | Step 2 |
| **Key Standards** | MS SDL Requirements phase, NIST SSDF PO/PS, OWASP SAMM |
| **Model** | sonnet |

**Capabilities:**
- Produces implementation plans with work breakdown and security milestones
- Enforces coding standards and linting configuration
- Makes dependency governance decisions with supply chain risk assessment
- Performs OWASP SAMM maturity assessments
- Maps plans to NIST SSDF Prepare Organization and Protect Software practices

**Example request:** "Plan the implementation for the new API gateway with security standards mapping"

---

### eng-backend -- Secure Backend Engineer

| Attribute | Value |
|-----------|-------|
| **Role** | Server-side implementation with security controls |
| **Workflow Position** | Step 3 (parallel with eng-frontend and eng-infra) |
| **Key Standards** | OWASP Top 10, OWASP ASVS 5.0 |
| **Model** | sonnet |

**Capabilities:**
- Server-side implementation guidance with input validation patterns
- Authentication and authorization implementation (OAuth 2.0, OIDC, RBAC, ABAC)
- API security design (rate limiting, request validation, response filtering)
- Database security (parameterized queries, encryption at rest, access controls)
- Session management and CSRF protection

**Example request:** "Implement the user registration endpoint with input validation and rate limiting"

---

### eng-frontend -- Secure Frontend Engineer

| Attribute | Value |
|-----------|-------|
| **Role** | Client-side implementation with XSS prevention and CSP |
| **Workflow Position** | Step 3 (parallel with eng-backend and eng-infra) |
| **Key Standards** | OWASP Top 10, OWASP ASVS 5.0 |
| **Model** | sonnet |

**Capabilities:**
- Client-side security implementation (XSS prevention, output encoding)
- Content Security Policy (CSP) configuration and validation
- Cross-Origin Resource Sharing (CORS) hardening
- Client-side storage security (cookies, localStorage, sessionStorage)
- Subresource Integrity (SRI) implementation

**Example request:** "Add CSP headers and XSS protection to the admin dashboard"

---

### eng-infra -- Secure Infrastructure Engineer

| Attribute | Value |
|-----------|-------|
| **Role** | IaC security, container hardening, supply chain integrity |
| **Workflow Position** | Step 3 (parallel with eng-backend and eng-frontend) |
| **Key Standards** | CIS Benchmarks, Google SLSA, NIST SSDF |
| **Model** | sonnet |

**Capabilities:**
- Infrastructure as Code (IaC) security review and hardening
- Container image security (base image selection, layer minimization, user permissions)
- SBOM generation with dependency provenance
- SLSA build integrity and provenance verification
- Secrets management architecture (vault integration, rotation policies)
- Network segmentation and firewall rules

**Example request:** "Design the container security configuration with SBOM generation and SLSA Level 2 provenance"

---

### eng-devsecops -- DevSecOps Pipeline Engineer

| Attribute | Value |
|-----------|-------|
| **Role** | Automated security scanning and CI/CD security gates |
| **Workflow Position** | Step 4 |
| **Key Standards** | DevSecOps patterns, Google SLSA, NIST SSDF PW.7/PW.8/PS.1 |
| **Model** | sonnet |

**Capabilities:**
- SAST pipeline configuration (Semgrep CI, CodeQL, SonarQube)
- DAST pipeline configuration (OWASP ZAP, Nuclei, Burp Suite CI)
- Secrets scanning (Gitleaks, TruffleHog)
- Container scanning (Trivy, Grype, Docker Scout)
- Dependency analysis (Snyk, Dependabot, OSV-Scanner)
- CI/CD security gate design with blocking and warning thresholds
- SLSA build automation for provenance and integrity

**CI/CD Gate Thresholds:**

| Finding Severity | Pipeline Action |
|-----------------|----------------|
| Critical | BLOCK deployment |
| High | BLOCK deployment |
| Medium | WARN, track for remediation |
| Low/Info | LOG for awareness |

**Example request:** "Set up SAST and container scanning in the CI pipeline with blocking thresholds"

---

### eng-qa -- Security QA Engineer

| Attribute | Value |
|-----------|-------|
| **Role** | Security test strategy, fuzzing, property-based testing |
| **Workflow Position** | Step 5 |
| **Key Standards** | OWASP Testing Guide |
| **Model** | sonnet |

**Capabilities:**
- Security test strategy design covering authentication, authorization, input validation
- Fuzzing campaign design (AFL, libFuzzer, custom fuzzers)
- Property-based testing for security invariants
- Boundary testing for input validation controls
- Security regression test suites
- Coverage enforcement and gap analysis

**Example request:** "Write security test cases with fuzzing for the authentication flow"

---

### eng-security -- Security Code Review Specialist

| Attribute | Value |
|-----------|-------|
| **Role** | Manual secure code review and ASVS verification |
| **Workflow Position** | Step 6 |
| **Key Standards** | CWE Top 25, OWASP ASVS 5.0, CVSS |
| **Model** | sonnet |

**Capabilities:**
- Manual secure code review with data flow tracing
- CWE Top 25 vulnerability identification (XSS, SQL injection, authentication bypass, path traversal, and more)
- OWASP ASVS 5.0 chapter verification (V1-V9)
- Business logic vulnerability identification (flaws automated tools cannot detect)
- CVSS severity scoring for all findings
- Remediation guidance with specific code examples

**Note:** This agent focuses exclusively on manual review. For automated scanning (SAST, DAST, container scanning), use eng-devsecops.

**Example request:** "Review the payment module for CWE Top 25 vulnerabilities with ASVS verification"

---

### eng-reviewer -- Final Review Gate and Quality Enforcer

| Attribute | Value |
|-----------|-------|
| **Role** | Mandatory final gate with /adversary integration |
| **Workflow Position** | Step 7 (mandatory before release) |
| **Key Standards** | All /eng-team standards aggregated |
| **Model** | opus |

**Capabilities:**
- Final compliance verification against all security standards
- Architecture compliance review against eng-architect decisions
- Test coverage verification against eng-qa results
- /adversary integration for C2+ deliverables at >= 0.95 quality threshold
- Quality scoring using S-014 LLM-as-Judge with 6-dimension rubric
- Release readiness assessment

**Quality Gate Decision:**

| Score | Outcome |
|-------|---------|
| >= 0.95 | PASS -- deliverable approved |
| 0.85 - 0.94 | REVISE -- targeted revision required |
| < 0.85 | REJECTED -- significant rework required |

**Example request:** "Final review of the release candidate against all security standards"

---

### eng-incident -- Incident Response Specialist

| Attribute | Value |
|-----------|-------|
| **Role** | Post-deployment IR plans, runbooks, detection engineering |
| **Workflow Position** | Step 8 (post-deployment, independently activatable) |
| **Key Standards** | NIST SP 800-61, NIST SSDF RV practices, SIGMA, YARA, Suricata |
| **Model** | sonnet |

**Capabilities:**
- Incident response runbook design for common attack scenarios (credential compromise, data breach, ransomware, supply chain attack, insider threat)
- Vulnerability lifecycle management (discovery through remediation with SLA tracking)
- Post-deployment monitoring configuration (log analysis, alerting, anomaly detection)
- Detection rule development for defense evasion (TA0005) and command-and-control (TA0011)
- C2 beaconing detection methodology (JA3/JA3S fingerprinting, protocol analysis)
- DLP rule design for exfiltration prevention
- Network behavioral analysis for lateral movement detection

**Key Difference:** eng-incident can be invoked independently of the 8-step workflow. It does not require prior steps to have completed. Use it any time you need post-deployment security guidance.

**Example request:** "Create an IR runbook for credential compromise with C2 detection rules"

---

## Choosing the Right Agent

Use this table when you are unsure which agent to request.

| Your Request Contains... | Use This Agent |
|--------------------------|----------------|
| design, architecture, threat model, STRIDE, DREAD, ADR, trust boundary | eng-architect |
| plan, standards, dependencies, code standards, SAMM, work breakdown | eng-lead |
| backend, API, server, auth, database, input validation, OWASP Top 10 | eng-backend |
| frontend, XSS, CSP, CORS, client, browser, output encoding | eng-frontend |
| infrastructure, IaC, container, secrets, SBOM, SLSA, supply chain | eng-infra |
| pipeline, SAST, DAST, CI/CD, scanning, DevSecOps, automation | eng-devsecops |
| test, QA, fuzzing, coverage, boundary testing, property-based | eng-qa |
| code review, CWE, ASVS, manual review, vulnerability, security review | eng-security |
| final review, quality gate, compliance, release, /adversary | eng-reviewer |
| incident, runbook, response, monitoring, post-deployment, detection rules | eng-incident |

**Tip:** If you are unsure, simply describe your need in natural language. The orchestrator will route to the correct agent based on context.

---

## L1: Workflow Usage

### How to Invoke Agents

There are three ways to invoke /eng-team agents:

#### Method 1: Natural Language (Recommended)

Simply describe what you need. The orchestrator selects the appropriate agent:

```
"Design a secure microservice architecture with threat model"
"Review this API implementation for OWASP Top 10 vulnerabilities"
"Set up a DevSecOps pipeline with SAST and container scanning"
"Create an incident response runbook for credential compromise"
```

#### Method 2: Explicit Agent Request

Name the specific agent you want:

```
"Use eng-architect to create a threat model for the payment service"
"Have eng-devsecops design the CI/CD security pipeline"
"I need eng-security to review the authentication module"
```

#### Method 3: Task Tool Invocation

For programmatic use within orchestration workflows:

```python
Task(
    description="eng-architect: Threat model for payment service",
    prompt="""
You are the eng-architect agent (v1.0.0).

## ENG CONTEXT (REQUIRED)
- **Engagement ID:** ENG-0042
- **Topic:** Payment Service Threat Model

## MANDATORY PERSISTENCE (P-002)
Create file at: skills/eng-team/output/ENG-0042/eng-architect-payment-threat-model.md

## TASK
Produce a threat model for the payment service using STRIDE analysis
with DREAD risk scoring.
"""
)
```

---

### The 8-Step Workflow

The /eng-team follows an 8-step sequential workflow. Each step builds on the previous step's output.

```
Step 1: eng-architect    --> Design + Threat Model
    |
Step 2: eng-lead         --> Implementation Plan + Security Standards
    |
Step 3: eng-backend / eng-frontend / eng-infra  --> Parallel Implementation
    |
Step 4: eng-devsecops    --> Automated Security Scans
    |
Step 5: eng-qa           --> Testing + Fuzzing
    |
Step 6: eng-security     --> Manual Security Review
    |
Step 7: eng-reviewer     --> Final Gate + /adversary for C2+
    |
Step 8: eng-incident     --> IR Plan + Runbooks (post-deployment)
```

**Key Rules:**

- Steps 1-7 are sequential. Each step requires the prior step's artifacts.
- Step 3 is an exception: eng-backend, eng-frontend, and eng-infra execute in parallel.
- Step 7 (eng-reviewer) is the mandatory final gate. No release without it.
- Step 8 (eng-incident) activates post-deployment and can also be invoked independently.
- You do not need to run all 8 steps. Run only the steps relevant to your task.

#### How State Passes Between Agents

Each agent produces output that the next agent consumes:

| Agent | Produces | Consumed By |
|-------|----------|-------------|
| eng-architect | System design, threat model, ADRs | eng-lead |
| eng-lead | Implementation plan, standards mapping | eng-backend, eng-frontend, eng-infra |
| eng-backend | Server-side implementation artifacts | eng-devsecops, eng-qa |
| eng-frontend | Client-side implementation artifacts | eng-devsecops, eng-qa |
| eng-infra | IaC templates, container configs, SBOM | eng-devsecops, eng-qa |
| eng-devsecops | Scan results, pipeline configs | eng-qa, eng-security |
| eng-qa | Test results, coverage reports | eng-security |
| eng-security | Code review findings, ASVS verification | eng-reviewer |
| eng-reviewer | Quality gate decision, compliance status | Release decision |
| eng-incident | IR plans, monitoring configs | Next development cycle |

---

### Output Levels

Every agent produces output at three levels, ensuring the right information reaches the right audience:

| Level | Audience | Content |
|-------|----------|---------|
| **L0 (Executive Summary)** | Leadership, project managers | Plain-language overview of findings and recommendations. Answers "What does this mean for the project?" |
| **L1 (Technical Detail)** | Developers, engineers | Implementation-specific content with code examples, configuration guidance, and specific remediation steps |
| **L2 (Strategic Implications)** | Architects, governance reviewers | Trade-offs, long-term risks, alignment with security posture, and architectural evolution considerations |

**Output Location:** All output files are saved at:
```
skills/eng-team/output/{engagement-id}/{agent-name}-{topic-slug}.md
```

---

## L2: Advanced Configuration

### Configuration Options

#### SDLC Governance Customization

The default governance model layers five frameworks. You can customize which frameworks apply:

| Layer | Default Framework | Alternatives |
|-------|------------------|--------------|
| Governance | NIST SSDF | ISO 27034 |
| Lifecycle | Microsoft SDL | (standard across engagements) |
| Assessment | OWASP SAMM | BSIMM |
| Supply Chain | Google SLSA | (standard across engagements) |
| Automation | DevSecOps patterns | (standard across engagements) |

To override, specify your preference in the request:

```
"Design the architecture using BSIMM instead of SAMM for maturity assessment"
```

Per R-011 (configurable rule sets), organizations can substitute frameworks through profile cascading.

#### Threat Modeling Configuration

The default threat modeling methodology (STRIDE + DREAD with criticality-based escalation) can be customized:

- **CVSS substitution:** "Use CVSS instead of DREAD for risk scoring" -- for organizations that mandate CVSS
- **Privacy analysis:** "Include LINDDUN analysis" -- automatically added when PII is identified, but can be requested explicitly
- **Full PASTA analysis:** "Use PASTA for the complete threat analysis" -- use for C4 engagements requiring business impact analysis

#### Quality Threshold

The default quality threshold is >= 0.95 for PROJ-010 deliverables (per R-013). This threshold governs eng-reviewer's final gate decision:

- Deliverables scoring below the threshold are rejected
- /adversary integration applies for all C2+ deliverables
- For C4 deliverables (security architecture, authentication systems), all 10 adversarial strategies apply

---

### Integration Points

#### Integration with /adversary

eng-reviewer invokes /adversary for C2+ deliverables. The quality review uses the S-014 LLM-as-Judge scoring rubric with six dimensions:

| Dimension | Weight | What It Measures |
|-----------|--------|-----------------|
| Completeness | 0.20 | All required elements present |
| Internal Consistency | 0.20 | No contradictions within the deliverable |
| Methodological Rigor | 0.20 | Proper methodology application |
| Evidence Quality | 0.15 | Claims supported by evidence |
| Actionability | 0.15 | Recommendations are implementable |
| Traceability | 0.10 | Decisions trace to requirements and standards |

#### Integration with /problem-solving

Use /problem-solving for research and analysis tasks that precede /eng-team work:

- "Research the current state of WebSocket security best practices" (use /problem-solving)
- "Design a secure WebSocket implementation based on the research" (use /eng-team)

#### Integration with /nasa-se

Use /nasa-se for formal requirements and verification activities:

- Requirements specification and management
- Formal V&V (Verification and Validation) activities
- Technical review processes

/eng-team focuses on security-specific implementation; /nasa-se provides the broader systems engineering framework.

#### Integration with /red-team (Purple Team)

The /eng-team and /red-team skills work as adversaries through four integration points:

| Integration Point | What Happens |
|-------------------|-------------|
| **1. Threat-Informed Architecture** | red-recon provides real adversary TTPs to eng-architect, improving threat model accuracy beyond theoretical threats |
| **2. Attack Surface Validation** | red-recon and red-vuln test eng-infra and eng-devsecops hardening to validate that infrastructure security actually reduces attack surface |
| **3. Secure Code vs. Exploitation** | red-exploit and red-privesc test eng-backend and eng-frontend code to prove whether secure coding practices withstand real exploitation |
| **4. Incident Response Validation** | red-persist, red-lateral, and red-exfil test eng-incident runbooks and detection rules against real post-exploitation techniques |

For full purple team engagement workflows, see the Purple Team Integration Framework.

---

### Engagement Management

#### Engagement IDs

Each engagement uses an ID in `ENG-NNNN` format (e.g., `ENG-0042`). The engagement ID:

- Organizes all output files into a single directory
- Links artifacts across agent outputs
- Enables tracing from findings to decisions

#### Output Organization

```
skills/eng-team/output/
  ENG-0042/
    eng-architect-payment-threat-model.md
    eng-lead-payment-implementation-plan.md
    eng-backend-payment-api-security.md
    eng-frontend-payment-dashboard-csp.md
    eng-infra-payment-container-config.md
    eng-devsecops-payment-pipeline-security.md
    eng-qa-payment-security-tests.md
    eng-security-payment-code-review.md
    eng-reviewer-payment-final-gate.md
    eng-incident-payment-ir-runbook.md
```

#### Tool Degradation Levels

Every agent operates at one of three levels depending on tool availability:

| Level | Name | Behavior |
|-------|------|----------|
| Level 0 | Full Tool Access | Optimal evidence-backed analysis with real-time data |
| Level 1 | Partial Tools | Analysis with explicit uncertainty markers for gaps |
| Level 2 | Standalone | Full methodology guidance; all claims marked "unvalidated" with manual verification instructions |

You do not need to configure this. Agents automatically adapt to available tools.

---

## Common Scenarios

### Scenario 1: Building a New Service from Scratch

**Goal:** Design and implement a secure new microservice.

1. "Design a secure architecture for a user notification service" -- eng-architect produces the threat model and ADRs
2. "Plan the implementation based on this architecture" -- eng-lead produces the implementation plan
3. "Implement the notification API with input validation and rate limiting" -- eng-backend produces the server-side code guidance
4. "Set up SAST and dependency scanning for the notification service" -- eng-devsecops configures the pipeline
5. "Write security test cases for the notification flow" -- eng-qa produces the test strategy
6. "Review the notification service for CWE Top 25 vulnerabilities" -- eng-security performs manual review
7. "Final review before release" -- eng-reviewer runs the quality gate

### Scenario 2: Adding Security to an Existing Codebase

**Goal:** Harden an existing application.

1. "Review the authentication module for security vulnerabilities" -- eng-security performs a targeted code review
2. "Set up automated scanning for the existing codebase" -- eng-devsecops configures SAST/DAST
3. "Create security test cases for the areas flagged by the review" -- eng-qa targets testing at weak areas
4. "Create an IR runbook for the most likely attack scenarios" -- eng-incident prepares post-deployment defenses

### Scenario 3: Setting Up DevSecOps for a Team

**Goal:** Establish automated security scanning in CI/CD.

1. "Evaluate our tech stack and recommend security scanning tools" -- eng-devsecops performs tool selection
2. "Configure SAST with Semgrep for our Python/TypeScript codebase" -- eng-devsecops produces pipeline configs
3. "Add container scanning with Trivy and secrets scanning with Gitleaks" -- eng-devsecops extends the pipeline
4. "Define the blocking thresholds for Critical and High findings" -- eng-devsecops configures gates

### Scenario 4: Post-Incident Response Planning

**Goal:** Create IR readiness artifacts after a security incident.

1. "Create IR runbooks for credential compromise, data breach, and ransomware scenarios" -- eng-incident produces runbooks
2. "Configure detection rules for C2 beaconing and defense evasion" -- eng-incident produces detection engineering guidance
3. "Define the vulnerability lifecycle management process with SLAs" -- eng-incident produces the lifecycle framework

---

## Troubleshooting and FAQ

### Why did the agent produce a different output level than I expected?

All agents produce L0, L1, and L2 output by default. If you only need one level, specify it in your request:

```
"Give me just the executive summary (L0) for the threat model"
```

### Can I skip steps in the 8-step workflow?

Yes. The workflow is a recommended sequence, not a requirement. You can invoke any agent independently. However, agents in later steps produce better output when they have access to earlier steps' artifacts. For example, eng-security produces more targeted reviews when eng-architect's threat model is available.

### What happens if a tool is unavailable?

Agents degrade gracefully per the standalone capable design (AD-010):

- **Level 0:** All tools available -- full analysis
- **Level 1:** Some tools unavailable -- analysis proceeds with explicit uncertainty markers
- **Level 2:** No tools -- full methodology guidance with "unvalidated" markers

The agent automatically detects tool availability. No configuration is needed.

### How do I get /adversary quality scoring on my deliverable?

Request it through eng-reviewer:

```
"Run the final quality gate with /adversary scoring on this deliverable"
```

For C2+ deliverables, eng-reviewer automatically invokes /adversary. For C1 deliverables, you can request it explicitly.

### What is the difference between eng-security and eng-devsecops?

- **eng-security** performs manual secure code review. It traces data flows, identifies business logic flaws, and verifies OWASP ASVS requirements. It finds things automated tools miss.
- **eng-devsecops** configures and runs automated security tools (SAST, DAST, secrets scanning, container scanning). It catches known vulnerability patterns at scale.

Both are complementary. Use eng-devsecops for breadth (automated scanning of the entire codebase) and eng-security for depth (manual analysis of critical components).

### Can I use /eng-team without /red-team?

Yes. /eng-team is fully standalone. The /red-team integration points (purple team) enhance security posture by validating defenses against real adversary techniques, but /eng-team operates independently for all 8 workflow steps.

### How do engagement IDs work?

Engagement IDs (`ENG-NNNN`) are assigned per engagement. All agents within the same engagement share the same ID, and all output files are organized under that ID's directory. If you do not specify an engagement ID, the system assigns one.

---

## References

### Architecture Decision Records

| ADR | Title |
|-----|-------|
| ADR-PROJ010-001 | Agent Team Architecture -- 10-agent roster, 8-step workflow, SDLC governance, threat modeling methodology |
| ADR-PROJ010-002 | Skill Routing and Invocation -- keyword triggers, routing table, workflow patterns |
| ADR-PROJ010-003 | LLM Portability -- portable agent schema, multi-provider support |

### Security Standards

| Standard | Version | Application |
|----------|---------|-------------|
| NIST SP 800-218 SSDF | v1.1 (2022) | Governance layer -- organizational security practices |
| Microsoft SDL | 2024 | Lifecycle layer -- phase-gated secure development |
| OWASP ASVS | v5.0 (2025) | Verification standard for eng-security and eng-backend/eng-frontend |
| OWASP Top 10 | 2021 | Awareness standard for common vulnerabilities |
| CWE Top 25 | 2025 | Code review focus areas for eng-security |
| Google SLSA | v1.0 (2023) | Supply chain integrity for eng-infra and eng-devsecops |
| OWASP SAMM | v2.0 | Maturity assessment for eng-lead |
| CIS Benchmarks | Various | Infrastructure hardening for eng-infra |
| NIST CSF | v2.0 (2024) | Governance mapping for eng-architect |
| NIST SP 800-61 | r3 (2024) | Incident handling methodology for eng-incident |

### Agent Definition Files

| Agent | File Path |
|-------|-----------|
| eng-architect | `skills/eng-team/agents/eng-architect.md` |
| eng-lead | `skills/eng-team/agents/eng-lead.md` |
| eng-backend | `skills/eng-team/agents/eng-backend.md` |
| eng-frontend | `skills/eng-team/agents/eng-frontend.md` |
| eng-infra | `skills/eng-team/agents/eng-infra.md` |
| eng-devsecops | `skills/eng-team/agents/eng-devsecops.md` |
| eng-qa | `skills/eng-team/agents/eng-qa.md` |
| eng-security | `skills/eng-team/agents/eng-security.md` |
| eng-reviewer | `skills/eng-team/agents/eng-reviewer.md` |
| eng-incident | `skills/eng-team/agents/eng-incident.md` |

---

*Document Version: 1.0.0*
*SSOT: ADR-PROJ010-001, ADR-PROJ010-002*
*Feature: FEAT-050 (/eng-team User Documentation)*
*Created: 2026-02-22*
