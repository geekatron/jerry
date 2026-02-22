# PROJ-010: Cyber Ops

> Two elite skill teams: a secure-by-design software engineering team and an offensive security red team. Built for a cybersecurity professional who needs real tools to own systems and harden them.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Objective](#objective) | What we're building and why |
| [Scope](#scope) | Boundaries |
| [Skill 1: /eng-team](#skill-1-eng-team) | Software engineering team skill |
| [Skill 2: /red-team](#skill-2-red-team) | Offensive security team skill |
| [Integration Points](#integration-points) | How the skills interact with each other and existing Jerry skills |
| [Requirements](#requirements) | 24 non-negotiable requirements across 5 categories |
| [Phases](#phases) | 6-phase execution plan with C4 quality gates |

---

## Objective

Build two specialized Jerry skills, each with their own agent teams:

1. **`/eng-team`** -- An elite software engineering team that produces secure, high-quality, production-grade code. Architects, engineers, QA, security reviewers. Every output goes through /adversary. Secure by design, not as an afterthought.

2. **`/red-team`** -- Offensive security operators. Recon, exploitation, privilege escalation, lateral movement, persistence, exfiltration. Real techniques, real tooling, real methodology. For authorized penetration testing and system hardening.

The two skills work as adversaries: /eng-team builds, /red-team breaks. The gap between them is where the hardening happens.

---

## Scope

### In Scope

- /eng-team skill with agent definitions, routing, templates
- /red-team skill with agent definitions, routing, templates
- Integration with /adversary for quality enforcement
- Real offensive security methodology (MITRE ATT&CK, OWASP, PTES, OSSTMM)
- Real defensive engineering practices (NIST, CIS, SANS, secure SDLC)
- Agent definition schemas per agent-development-standards
- Authorization and scope controls for offensive operations

### Out of Scope

- Actual exploitation tooling binaries (we orchestrate methodology, not ship malware)
- Cloud-specific provider tooling (AWS/GCP/Azure -- future extension)
- Compliance certification (we build to standards, not certify)

---

## Skill 1: /eng-team

> Elite software engineering team. Secure by design. Every deliverable through /adversary.

### Agents

| Agent | Role | Specialization |
|-------|------|----------------|
| eng-architect | Solution Architect | System design, ADRs, threat modeling (STRIDE/DREAD), architecture review. Produces designs that are defensible before a line of code is written. |
| eng-lead | Technical Lead | Implementation planning, code standards enforcement, PR review criteria, dependency decisions. Owns technical quality. |
| eng-backend | Backend Engineer | Server-side implementation. Secure coding (OWASP), input validation, authentication/authorization, API security, database security. |
| eng-frontend | Frontend Engineer | Client-side implementation. XSS prevention, CSP, CORS, secure state management, output encoding. |
| eng-infra | Infrastructure Engineer | IaC, container security, network segmentation, secrets management, CI/CD hardening, supply chain security. |
| eng-qa | QA Engineer | Test strategy, security test cases, fuzzing, boundary testing, regression suites, coverage enforcement. |
| eng-security | Security Engineer | Secure code review, SAST/DAST integration, vulnerability assessment, dependency auditing, security requirements verification. |
| eng-reviewer | Code Reviewer | Final review gate. Checks against architecture, security standards, coding standards, test coverage. Uses /adversary for C2+ deliverables. |

### Workflow

1. eng-architect produces design + threat model
2. eng-lead breaks down into implementation plan
3. eng-backend / eng-frontend / eng-infra implement
4. eng-qa writes and executes tests
5. eng-security performs security review
6. eng-reviewer final gate with /adversary integration
7. All deliverables scored via C4 /adversary for security-critical work

---

## Skill 2: /red-team

> Offensive security operators. Authorized penetration testing and system compromise for hardening.

### Agents

| Agent | Role | Specialization |
|-------|------|----------------|
| red-recon | Reconnaissance | OSINT, network enumeration, service discovery, technology fingerprinting, attack surface mapping. Passive and active recon. |
| red-vuln | Vulnerability Analyst | Vulnerability identification, CVE research, exploit availability assessment, attack path analysis, risk scoring (CVSS). |
| red-exploit | Exploitation Specialist | Exploit development, payload crafting, vulnerability chaining, proof-of-concept development. Web app, network, API, binary exploitation. |
| red-privesc | Privilege Escalation | Local and domain privilege escalation, credential harvesting, token manipulation, misconfig exploitation. Linux and Windows. |
| red-lateral | Lateral Movement | Pivoting, tunneling, C2 infrastructure, living-off-the-land techniques, internal network exploitation. |
| red-persist | Persistence Specialist | Backdoor placement, scheduled tasks, service manipulation, rootkit methodology, detection evasion analysis. |
| red-exfil | Data Exfiltration | Data identification, exfiltration channels, covert communication, DLP bypass assessment. |
| red-reporter | Engagement Reporter | Finding documentation, risk scoring, remediation recommendations, executive summaries, technical write-ups. |
| red-lead | Engagement Lead | Scope definition, rules of engagement, methodology selection (PTES/OSSTMM/ATT&CK), team coordination, authorization verification. |

### Methodology

Every engagement follows a structured methodology:

1. **red-lead** defines scope, rules of engagement, and verifies authorization
2. **red-recon** maps the attack surface
3. **red-vuln** identifies and prioritizes vulnerabilities
4. **red-exploit** develops and executes exploits (within scope)
5. **red-privesc** escalates access
6. **red-lateral** moves through the environment
7. **red-persist** establishes persistence (if in scope)
8. **red-exfil** tests data exfiltration paths
9. **red-reporter** documents everything with remediation guidance

### Authorization Controls

| Control | Implementation |
|---------|---------------|
| Scope verification | red-lead MUST verify authorization before any active testing |
| Rules of engagement | Defined and confirmed before engagement start |
| Out-of-scope protection | Agents MUST refuse actions outside defined scope |
| Evidence preservation | All actions logged with timestamps for audit trail |
| Remediation focus | Every finding includes actionable remediation |

---

## Integration Points

| Integration | Description |
|-------------|-------------|
| /eng-team + /adversary | All eng-team deliverables go through /adversary quality review. Security-critical work uses C4 tournament. |
| /red-team + /adversary | Red team findings go through /adversary for quality scoring and completeness review. |
| /eng-team + /red-team | Purple team mode: /red-team attacks what /eng-team builds. Gap analysis drives hardening. |
| /eng-team + /problem-solving | Complex engineering problems escalate to /problem-solving research pipeline. |
| /red-team + /problem-solving | Novel attack vectors escalate to /problem-solving for deep research. |
| /eng-team + /nasa-se | Security-critical systems use /nasa-se for formal requirements, V&V, and compliance. |

---

## Requirements

> **Classification: MISSION CRITICAL.** All requirements are non-negotiable. Quality threshold elevated to >= 0.95 (above standard 0.92). C4 /adversary enforcement on every phase with up to 5 creator-critic iterations.

### Foundational Principles

| ID | Requirement | Rationale |
|----|-------------|-----------|
| R-001 | **Secure by Design.** All code, architecture, and agent definitions MUST be secure by design -- security is a first-class architectural constraint, not a bolt-on. Threat modeling BEFORE implementation. | Security as afterthought produces exploitable systems. |
| R-002 | **Architecturally Pure.** All implementations MUST follow clean architecture principles (hexagonal/ports-and-adapters, dependency inversion, separation of concerns) and MUST be testable at every layer in isolation. No untestable code ships. | Architectural purity enables maintainability, testability, and portability. |
| R-003 | **No Slop Code.** Zero tolerance for placeholder implementations, TODO stubs shipped as deliverables, copy-paste patterns, magic strings, unclear naming, or code that "works but nobody knows why." Every line MUST be intentional, readable, and defensible. | Slop code is tech debt that compounds. Mission-critical systems cannot carry it. |
| R-004 | **No Shortcuts.** No skipping research, no skipping tests, no skipping reviews, no "we'll fix it later." Every phase completes fully before the next begins. If a step is hard, we do it properly -- not around it. | Shortcuts in mission-critical systems become failure modes. |
| R-005 | **Grounded in Reality.** All outputs MUST be real, actionable, and executable. No placeholder methodology, no theoretical frameworks that can't be applied, no inflated claims. If we can't demonstrate it works, it doesn't ship. No smoke-blowing. | Credibility requires honesty about capabilities and limitations. |

### Research and Evidence Standards

| ID | Requirement | Rationale |
|----|-------------|-----------|
| R-006 | **Evidence-Driven Decisions.** All architectural, methodological, and tooling decisions MUST be grounded in data and evidence from authoritative sources. Required source categories: Industry Experts, Industry Innovators, Industry Leaders, Community Experts, Community Innovators, Community Leaders. All decisions MUST include citations, references, and sources. | Unbacked decisions produce fragile systems. Authority comes from evidence. |
| R-007 | **Persistent Research Artifacts.** All analysis, discoveries, explorations, findings, research, and synthesis MUST be persisted to the repository under `work/research/`. No research lives only in conversation context. | Research that isn't persisted is research that's lost. |
| R-008 | **Role Completeness Analysis.** Research and analysis MUST be performed to validate that both /eng-team and /red-team have the most robust, complete agent rosters available. Missing roles MUST be identified through gap analysis against industry team structures and prior art. | Incomplete teams produce incomplete coverage. |
| R-009 | **Current Intelligence.** Research MUST use Context7 and WebSearch for current techniques, CVEs, tooling, and methodology. No reliance on stale training data. Sources MUST be dated and verifiable. | Cybersecurity is a moving target. Stale data = exploitable gaps. |

### Architecture and Portability

| ID | Requirement | Rationale |
|----|-------------|-----------|
| R-010 | **LLM Portability.** All agent definitions MUST be portable across LLM providers (OpenAI, Gemini, Anthropic, open-source models). Agent logic MUST NOT depend on provider-specific features. Prompt engineering MUST use universal patterns. Portability MUST be validated as a testable property. | Vendor lock-in is an unacceptable risk for mission-critical tooling. |
| R-011 | **Configurable Rule Sets.** Both skills MUST support user-provided rule sets and content for practices, standards, and methodologies. Users MUST be able to override default rules (e.g., substitute OWASP with org-specific standards) without modifying core skill code. | Different organizations have different standards. Flexibility is a requirement, not a feature. |
| R-012 | **Tool Integration Architecture.** Both skills MUST define integration points with external tooling frameworks (e.g., Metasploit, Burp Suite, Nmap, SAST/DAST tools, IaC scanners). Integration MUST be architected as pluggable adapters. Skills MUST be fully capable without external tools -- tools augment, not enable. | Real operators use real tools. But dependency on any single tool is a vulnerability. |

### Process and Quality

| ID | Requirement | Rationale |
|----|-------------|-----------|
| R-013 | **C4 /adversary on Every Phase.** Every phase deliverable MUST go through C4 /adversary review with a quality threshold of >= 0.95. Up to 5 creator-critic-revision iterations. Feedback MUST return to the creator for resolution. Below threshold = rejected, no exceptions. | Mission-critical software demands the highest quality bar. |
| R-014 | **Full /orchestration Planning.** MUST use orch-planner with all available agents from /orchestration and /problem-solving. Phases, gates, dependencies, and agent assignments MUST be formally planned and tracked. | Complex multi-phase work without orchestration produces chaos. |
| R-015 | **Detailed /worktracker.** A comprehensive worktracker MUST be maintained and kept current throughout the project. All work items, status changes, and completions MUST be reflected in real-time. | Untracked work is unmanageable work. |
| R-016 | **Challenge Weak Specifications.** When specifications are ambiguous, incomplete, or weak, they MUST be challenged with questions and enhanced before implementation proceeds. No building on shaky foundations. | Weak specs produce wrong implementations. Challenge early, build right. |
| R-017 | **Industry Leader Standard.** This project aims to be an industry exemplar for agentic cybersecurity tooling. Every decision, every agent, every output MUST reflect pioneering quality. "Good enough" is not good enough. | If we're not setting the standard, we're following someone else's. |

### Operational Requirements

| ID | Requirement | Rationale |
|----|-------------|-----------|
| R-018 | **/red-team agents MUST use real offensive security techniques** mapped to MITRE ATT&CK tactics and techniques. Methodology MUST follow PTES, OSSTMM, or equivalent recognized frameworks. | Real techniques produce real findings. Theoretical attacks miss real vulnerabilities. |
| R-019 | **/eng-team agents MUST follow secure SDLC practices** mapped to OWASP, NIST, CIS, and SANS standards. Secure coding MUST be verifiable, not aspirational. | Standards compliance without verification is theater. |
| R-020 | **/red-team MUST enforce authorization verification** before any active testing operation. Scope MUST be defined and confirmed. Out-of-scope actions MUST be refused. | Unauthorized testing is illegal. No exceptions. |
| R-021 | **/red-team findings MUST include actionable remediation guidance.** Offense serves defense. Every vulnerability report MUST tell the defender exactly how to fix it. | Findings without remediation are problems without solutions. |
| R-022 | **Agent definitions MUST follow Jerry agent-development-standards** and routing-standards. SKILL.md, agent schemas, and routing MUST comply with all applicable H-rules. | Framework compliance ensures consistency and maintainability. |
| R-023 | **All agents MUST persist outputs** to the repository per standard Jerry workflow. No outputs exist only in conversation context. | Unpersisted work is lost work. |
| R-024 | **Both skills MUST integrate with /adversary** for quality enforcement on all deliverables. | Quality enforcement is non-optional for mission-critical software. |

---

## Phases

> Every phase requires C4 /adversary review with >= 0.95 quality threshold and up to 5 creator-critic iterations. Phase gates are hard -- no phase advances without passing.

| Phase | Name | Description | Quality Gate |
|-------|------|-------------|--------------|
| 1 | Research | Industry research on offensive/defensive agent team patterns, existing tooling, methodology standards, role completeness analysis, tool integration landscape. Context7 + WebSearch for current state of art. All findings persisted to `work/research/`. | C4, >= 0.95 |
| 2 | Architecture | Agent team design, skill definitions, routing, integration architecture, portability design, configurable rule set architecture, tool integration adapter design. ADRs for all key decisions with evidence citations. | C4, >= 0.95 |
| 3 | /eng-team Build | Build the engineering team skill: agent definitions, templates, routing, /adversary integration. Secure by design. Architecturally pure. Testable. Portable. | C4, >= 0.95 |
| 4 | /red-team Build | Build the red team skill: agent definitions, templates, methodology, authorization controls, tool integration adapters. Real techniques, real methodology. | C4, >= 0.95 |
| 5 | Purple Team Validation | /red-team attacks /eng-team outputs. Gap analysis. Hardening cycle. Integration testing. Portability validation. | C4, >= 0.95 |
| 6 | Documentation | Skill documentation, usage guides, engagement templates, rule set customization guides, tool integration guides. | C4, >= 0.95 |
