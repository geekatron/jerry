# B-003: OWASP, NIST, CIS, SANS Standards Analysis

> Stream B: Methodology Standards | PROJ-010 Cyber Ops | Phase 1 Research

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | High-level overview of defensive standards landscape |
| [L1: Key Findings](#l1-key-findings) | Structured findings on standard applicability |
| [L2: Detailed Analysis](#l2-detailed-analysis) | Deep analysis of OWASP, NIST, CIS, and SANS standards |
| [Agent Mapping](#agent-mapping) | How each standard maps to /eng-team agent capabilities |
| [Evidence and Citations](#evidence-and-citations) | Categorized, dated sources |
| [Recommendations](#recommendations) | Default rule set selections for /eng-team |

---

## L0: Executive Summary

The defensive standards landscape for the /eng-team skill spans four major organizations: OWASP (application security), NIST (government/enterprise security frameworks), CIS (configuration hardening), and SANS/CWE (software weakness classification). The 2025 OWASP Top 10 defines the 10 most critical web application security risks with Broken Access Control at A01. OWASP ASVS 5.0 (May 2025) provides approximately 350 verification requirements across 17 categories at 3 assurance levels. OWASP SAMM offers a maturity model across 5 business functions. NIST provides the overarching framework ecosystem: CSF 2.0 (6 functions), SP 800-53 Rev 5 (20 control families, 1,189 controls), and SP 800-218 SSDF (4 practice groups for secure software development). CIS Benchmarks cover 100+ configuration guides across 8 technology categories. The 2025 CWE Top 25 (SANS/MITRE) identifies the most dangerous software weaknesses. Together, these standards form a comprehensive defensive capability matrix that maps cleanly to /eng-team agent responsibilities: OWASP for application-layer security (eng-backend, eng-frontend, eng-security), NIST for governance and architectural compliance (eng-architect, eng-lead), CIS for infrastructure hardening (eng-infra), and CWE/SANS for weakness-aware development (all implementation agents).

---

## L1: Key Findings

### Finding 1: OWASP Top 10 2025 Reflects Evolving Threat Landscape

The 2025 edition introduces two new categories: A03 Software Supply Chain Failures and A10 Mishandling of Exceptional Conditions. Security Misconfiguration climbed from 5th to 2nd position. Server-Side Request Forgery (previously its own category A10:2021) was absorbed into Broken Access Control. These shifts indicate growing emphasis on supply chain security and error handling -- both directly relevant to eng-infra (supply chain) and eng-backend/eng-frontend (error handling).

### Finding 2: ASVS 5.0 Is the Most Comprehensive Application Security Verification Standard

OWASP ASVS version 5.0 (May 2025) expanded to ~350 requirements across 17 chapters, adding new coverage for Web Frontend Security (V3), Self-Contained Tokens (V9), OAuth and OIDC (V10), and WebRTC (V17). Its 3-level assurance model (Level 1 = baseline, Level 2 = standard default, Level 3 = high-assurance) provides a natural configuration axis for /eng-team's rule set system.

### Finding 3: NIST CSF 2.0 Added Govern as the Sixth Core Function

The February 2024 release of CSF 2.0 elevated Governance to a top-level function (alongside Identify, Protect, Detect, Respond, Recover). This formalizes cybersecurity risk management strategy, expectations, and policy -- directly relevant to eng-architect and eng-lead's responsibilities for security governance within the engineering team.

### Finding 4: NIST SP 800-218 SSDF Provides the Secure SDLC Backbone

The SSDF's 4 practice groups (Prepare the Organization, Protect the Software, Produce Well-Secured Software, Respond to Vulnerabilities) provide an outcome-based framework for secure software development that is methodology-agnostic. Version 1.2 (draft December 2025) adds practices for AI/ML software development. This is the natural governance framework for /eng-team's entire workflow.

### Finding 5: CIS Benchmarks Provide Actionable Configuration Hardening

With 100+ benchmarks across 8 technology categories, CIS provides the most actionable infrastructure hardening guidance. Recent updates include Kubernetes v1.29-1.31 support (EKS Benchmark v1.7.0) and Azure Foundations Benchmark v5.0.0. eng-infra should treat CIS Benchmarks as the default configuration baseline.

### Finding 6: CWE Top 25 2025 Confirms Persistent Weakness Patterns

The 2025 CWE Top 25 (released December 2025) continues to show Cross-Site Scripting (CWE-79), SQL Injection (CWE-89), and Cross-Site Request Forgery (CWE-352) at the top. Missing Authorization (CWE-862) jumped 5 positions to #4. New entries include classic buffer overflow, heap-based buffer overflow, and allocation of resources without limits. These weaknesses should be the primary focus of eng-security's code review rules.

---

## L2: Detailed Analysis

### OWASP Standards Suite

#### OWASP Top 10 (2025 Edition)

| Rank | Category | CWE Count | Key Changes from 2021 |
|------|----------|-----------|-----------------------|
| A01 | **Broken Access Control** | 40 CWEs | Maintains #1; absorbed SSRF from A10:2021 |
| A02 | **Security Misconfiguration** | -- | Climbed from #5 to #2; reflects widespread cloud misconfig |
| A03 | **Software Supply Chain Failures** | -- | NEW -- replaces "Vulnerable and Outdated Components"; expanded scope to supply chain |
| A04 | **Cryptographic Failures** | -- | Moved from #2 to #4; scope unchanged |
| A05 | **Injection** | -- | Dropped from #3 to #5; still critical but better tooling reduces prevalence |
| A06 | **Insecure Design** | -- | Stable at #6; emphasizes threat modeling and secure design patterns |
| A07 | **Authentication Failures** | -- | Renamed from "Identification and Authentication Failures"; moved from #7 |
| A08 | **Software or Data Integrity Failures** | -- | Stable; includes CI/CD pipeline integrity |
| A09 | **Security Logging and Alerting Failures** | -- | Renamed from "Security Logging and Monitoring Failures" |
| A10 | **Mishandling of Exceptional Conditions** | 24 CWEs | NEW -- improper error handling, logical errors, failing open |

**Agent Relevance:**
- eng-backend / eng-frontend: A01 (access control), A05 (injection), A07 (authentication), A10 (error handling)
- eng-architect: A06 (insecure design), A02 (misconfiguration architecture)
- eng-infra: A02 (misconfiguration), A03 (supply chain), A08 (CI/CD integrity)
- eng-security: All categories (review and verification)

#### OWASP ASVS 5.0 (May 2025)

ASVS provides detailed verification requirements organized into chapters, with 3 assurance levels:

| Level | Target | Assurance | Use Case |
|-------|--------|-----------|----------|
| **Level 1** | All software | Baseline hygiene, quick adoption | Minimum acceptable security; automated testing can verify most requirements |
| **Level 2** | Applications with sensitive data | Standard default | Majority of applications; requires manual testing for some requirements |
| **Level 3** | Critical applications (financial, medical, military) | High assurance | Highest trust; requires deep manual review, architecture analysis, threat modeling |

**ASVS 5.0 Chapter Structure (17 Chapters):**

| Chapter | Title | Key Focus |
|---------|-------|-----------|
| V1 | Architecture, Design, and Threat Modeling | Secure architecture requirements, threat modeling mandates |
| V2 | Authentication | MFA, credential handling, password policies |
| V3 | Web Frontend Security | NEW -- XSS prevention, CSP, CORS, client-side security |
| V4 | Access Control | RBAC, least privilege, authorization checks |
| V5 | Validation, Sanitization, and Encoding | Input validation, output encoding, parameterized queries |
| V6 | Stored Cryptography | Encryption at rest, key management, algorithm selection |
| V7 | Error Handling and Logging | Secure error handling, audit logging, log injection prevention |
| V8 | Data Protection | Data classification, PII handling, data minimization |
| V9 | Self-Contained Tokens | NEW -- JWT security, token validation, claim verification |
| V10 | OAuth and OIDC | NEW -- OAuth 2.0 security, OIDC implementation |
| V11 | HTTP Communication Security | TLS, HSTS, certificate pinning, secure headers |
| V12 | File and Resource Handling | Upload validation, path traversal prevention, resource limits |
| V13 | API and Web Service Security | API authentication, rate limiting, schema validation |
| V14 | Configuration | Security configuration, default credentials, feature flags |
| V15 | Business Logic | Business logic flaws, workflow bypass, race conditions |
| V16 | Malicious Code Prevention | Backdoor detection, dependency verification, integrity checks |
| V17 | WebRTC | NEW -- WebRTC security, SRTP, DTLS |

**Agent Relevance:**
- eng-architect: V1 (architecture and threat modeling)
- eng-backend: V2, V4, V5, V6, V7, V8, V10, V13, V15
- eng-frontend: V3, V5, V11, V17
- eng-infra: V11, V14, V16
- eng-security: All chapters (verification)
- eng-qa: V5 (validation testing), V15 (business logic testing)

#### OWASP SAMM (Software Assurance Maturity Model)

SAMM measures organizational security maturity across 5 business functions, each with 3 security practices:

| Business Function | Security Practices | Maturity Levels |
|-------------------|-------------------|-----------------|
| **Governance** | Strategy and Metrics, Policy and Compliance, Education and Guidance | 1-3 |
| **Design** | Threat Assessment, Security Requirements, Security Architecture | 1-3 |
| **Implementation** | Secure Build, Secure Deployment, Defect Management | 1-3 |
| **Verification** | Architecture Assessment, Requirements-Driven Testing, Security Testing | 1-3 |
| **Operations** | Incident Management, Environment Management, Operational Management | 1-3 |

**Agent Relevance:**
- eng-architect: Design function (Threat Assessment, Security Architecture)
- eng-lead: Governance function (Strategy, Policy, Education)
- eng-backend / eng-frontend / eng-infra: Implementation function (Secure Build, Secure Deployment)
- eng-qa / eng-security: Verification function (all 3 practices)
- eng-reviewer: Cross-function maturity assessment

### NIST Standards Suite

#### NIST Cybersecurity Framework 2.0 (February 2024)

CSF 2.0 defines 6 core functions:

| Function | ID | Purpose | /eng-team Relevance |
|----------|----|---------|---------------------|
| **Govern** | GV | Establish and monitor cybersecurity risk management strategy, expectations, and policy | eng-lead (team governance), eng-architect (architectural governance) |
| **Identify** | ID | Understand business context, critical assets, and associated risks | eng-architect (asset identification, risk assessment) |
| **Protect** | PR | Secure identified assets to prevent or reduce likelihood/impact of events | All implementation agents (eng-backend, eng-frontend, eng-infra) |
| **Detect** | DE | Discover and analyze anomalies, indicators of compromise, and adverse events | eng-security (SAST/DAST), eng-qa (security testing), eng-infra (monitoring) |
| **Respond** | RS | Take action regarding detected cybersecurity incidents | eng-security (incident response procedures), eng-lead (escalation) |
| **Recover** | RC | Restore assets and systems affected by incidents | eng-infra (disaster recovery), eng-lead (recovery coordination) |

**CSF 2.0 Tiers:**
| Tier | Name | Description |
|------|------|-------------|
| Tier 1 | Partial | Ad hoc, reactive |
| Tier 2 | Risk Informed | Aware but not organization-wide |
| Tier 3 | Repeatable | Formally approved, regularly updated |
| Tier 4 | Adaptive | Continuous improvement, lessons learned |

#### NIST SP 800-53 Rev 5 (20 Control Families, 1,189 Controls)

| Family ID | Family Name | Control Count (approx.) | /eng-team Agent |
|-----------|-------------|------------------------|-----------------|
| AC | Access Control | 25 | eng-backend (application AC), eng-infra (infrastructure AC) |
| AT | Awareness and Training | 6 | eng-lead (team training requirements) |
| AU | Audit and Accountability | 16 | eng-security (audit logging), eng-infra (log infrastructure) |
| CA | Assessment, Authorization, and Monitoring | 9 | eng-reviewer (assessment), eng-security (continuous monitoring) |
| CM | Configuration Management | 14 | eng-infra (configuration baseline), eng-lead (change control) |
| CP | Contingency Planning | 13 | eng-infra (backup/recovery), eng-architect (resilience design) |
| IA | Identification and Authentication | 12 | eng-backend (AuthN implementation), eng-architect (AuthN architecture) |
| IR | Incident Response | 10 | eng-security (IR procedures), eng-lead (IR coordination) |
| MA | Maintenance | 7 | eng-infra (system maintenance) |
| MP | Media Protection | 8 | eng-infra (data media handling) |
| PE | Physical and Environmental Protection | 23 | (Primarily out of scope for software engineering) |
| PL | Planning | 8 | eng-lead (security planning), eng-architect (architecture planning) |
| PM | Program Management | 32 | eng-lead (program-level security management) |
| PS | Personnel Security | 9 | (Primarily HR-focused, out of scope) |
| PT | PII Processing and Transparency | 8 | eng-backend (PII handling), eng-architect (privacy by design) |
| RA | Risk Assessment | 10 | eng-architect (risk assessment), eng-security (vulnerability scanning) |
| SA | System and Services Acquisition | 23 | eng-lead (acquisition controls), eng-infra (supply chain) |
| SC | System and Communications Protection | 51 | eng-backend (crypto, session mgmt), eng-infra (network protection) |
| SI | System and Information Integrity | 23 | eng-security (integrity checks), eng-qa (testing) |
| SR | Supply Chain Risk Management | 12 | eng-infra (supply chain controls), eng-lead (vendor management) |

**Key observation:** The two families added in Rev 5 -- PT (PII Processing) and SR (Supply Chain Risk Management) -- directly address OWASP Top 10 2025 entries A03 (Supply Chain) and A08 (Data Integrity).

#### NIST SP 800-218 SSDF (Secure Software Development Framework)

The SSDF defines 4 practice groups:

| Practice Group | ID | Purpose | Key Practices |
|----------------|----|---------|---------------|
| **Prepare the Organization** | PO | Ensure people, processes, and technology are prepared for secure development | PO.1: Define security requirements; PO.2: Implement roles and responsibilities; PO.3: Implement supporting toolchains; PO.4: Define and use criteria for software security checks; PO.5: Implement and maintain secure environments |
| **Protect the Software** | PS | Protect all components of the software from tampering and unauthorized access | PS.1: Protect all forms of code; PS.2: Provide a mechanism for verifying software release integrity; PS.3: Archive and protect each release |
| **Produce Well-Secured Software** | PW | Produce well-secured software with minimal vulnerabilities | PW.1: Design software to meet security requirements and mitigate risks; PW.2: Review the software design to verify compliance; PW.4: Reuse existing, well-secured software; PW.5: Create source code by adhering to secure coding practices; PW.6: Configure the compilation, interpreter, and build processes; PW.7: Review and/or analyze human-readable code; PW.8: Test executable code; PW.9: Configure software to have secure settings by default |
| **Respond to Vulnerabilities** | RV | Identify residual vulnerabilities, respond appropriately, and prevent recurrence | RV.1: Identify and confirm vulnerabilities; RV.2: Assess, prioritize, and remediate vulnerabilities; RV.3: Analyze vulnerabilities to identify root causes |

**SSDF 1.2 (Draft December 2025) Updates:**
- New practices for AI/ML software security
- Enhanced supply chain integrity practices
- Updated practices for container and serverless environments

**Agent Relevance:**
- eng-lead: PO (organizational preparation, roles, toolchains)
- eng-architect: PW.1, PW.2 (secure design)
- eng-backend / eng-frontend: PW.4, PW.5, PW.6, PW.9 (secure coding, configuration)
- eng-infra: PS (software protection), PO.5 (secure environments)
- eng-security: PW.7, PW.8 (code review, testing)
- eng-qa: PW.8 (executable code testing)
- eng-reviewer: PW.2, PW.7 (design review, code review)

### CIS Benchmarks

CIS publishes 100+ benchmarks across 8 technology categories:

| Category | Examples | /eng-team Agent |
|----------|----------|-----------------|
| **Operating Systems** | Windows Server 2025, Ubuntu 24.04, RHEL 9, macOS Sonoma | eng-infra |
| **Cloud Platforms** | AWS Foundations v4.0, Azure Foundations v5.0.0, GCP Foundations v3.0 | eng-infra |
| **Containerized Infrastructure** | Docker, Kubernetes v1.29-1.31, EKS v1.7.0, ECS | eng-infra |
| **Server Applications** | Apache, Nginx, SQL Server, PostgreSQL, MongoDB | eng-infra, eng-backend |
| **Desktop Applications** | Web browsers (Chrome, Firefox, Edge), Office suites | (Limited relevance for server-side engineering) |
| **Mobile Devices** | iOS, Android | (Out of scope unless mobile development) |
| **Network Devices** | Firewalls, routers, switches, VPNs | eng-infra |
| **Multi-function Print Devices** | Network printers | (Out of scope) |

**CIS Benchmark Levels:**
| Level | Name | Description |
|-------|------|-------------|
| Level 1 | Essential | Basic security settings that can be applied without impacting functionality |
| Level 2 | Defense in Depth | More restrictive settings that may impact some functionality; for higher-security environments |

**Agent Relevance:**
- eng-infra: Primary consumer -- CIS Benchmarks are eng-infra's default configuration baseline
- eng-backend: Database and application server benchmarks
- eng-architect: Cloud platform benchmarks inform infrastructure architecture decisions

### SANS/CWE Top 25 Most Dangerous Software Weaknesses (2025)

The 2025 CWE Top 25 (released December 2025, based on 39,000+ CVEs from June 2024-June 2025):

| Rank | CWE ID | Name | Category | /eng-team Agent |
|------|--------|------|----------|-----------------|
| 1 | CWE-79 | Cross-Site Scripting (XSS) | Injection | eng-frontend, eng-backend |
| 2 | CWE-89 | SQL Injection | Injection | eng-backend |
| 3 | CWE-352 | Cross-Site Request Forgery (CSRF) | Authentication | eng-frontend, eng-backend |
| 4 | CWE-862 | Missing Authorization | Access Control | eng-backend |
| 5 | CWE-78 | OS Command Injection | Injection | eng-backend |
| 6 | CWE-22 | Path Traversal | Input Validation | eng-backend |
| 7 | CWE-416 | Use After Free | Memory Safety | eng-backend (C/C++ contexts) |
| 8 | CWE-787 | Out-of-bounds Write | Memory Safety | eng-backend (C/C++ contexts) |
| 9 | CWE-20 | Improper Input Validation | Input Validation | eng-backend, eng-frontend |
| 10 | CWE-125 | Out-of-bounds Read | Memory Safety | eng-backend (C/C++ contexts) |
| 11 | CWE-120 | Classic Buffer Overflow | Memory Safety | eng-backend (C/C++ contexts) |
| 12 | CWE-798 | Use of Hard-coded Credentials | Authentication | eng-infra, eng-backend |
| 13 | CWE-918 | Server-Side Request Forgery (SSRF) | Input Validation | eng-backend |
| 14 | CWE-287 | Improper Authentication | Authentication | eng-backend |
| 15 | CWE-434 | Unrestricted Upload of File with Dangerous Type | Input Validation | eng-backend |
| 16 | CWE-502 | Deserialization of Untrusted Data | Input Validation | eng-backend |
| 17 | CWE-190 | Integer Overflow or Wraparound | Memory Safety | eng-backend (C/C++ contexts) |
| 18 | CWE-121 | Stack-based Buffer Overflow | Memory Safety | eng-backend (C/C++ contexts) |
| 19 | CWE-122 | Heap-based Buffer Overflow | Memory Safety | eng-backend (C/C++ contexts) |
| 20 | CWE-284 | Improper Access Control | Access Control | eng-backend |
| 21 | CWE-476 | NULL Pointer Dereference | Memory Safety | eng-backend (C/C++ contexts) |
| 22 | CWE-863 | Incorrect Authorization | Access Control | eng-backend |
| 23 | CWE-269 | Improper Privilege Management | Access Control | eng-backend, eng-infra |
| 24 | CWE-94 | Code Injection | Injection | eng-backend |
| 25 | CWE-770 | Allocation Without Limits or Throttling | Resource Management | eng-backend, eng-infra |

**Key Observations:**
- Injection (XSS, SQLi, CSRF, OS command injection, code injection) dominates the top 25
- Memory safety issues (7 entries) are concentrated in C/C++ contexts -- relevant for systems-level engineering
- Access control failures (CWE-862 Missing Authorization jumped to #4, CWE-284, CWE-863, CWE-269) reflect the same pattern as OWASP A01
- Missing Authorization (CWE-862) jumping 5 positions signals a fundamental gap in how applications verify user permissions

---

## Agent Mapping

### /eng-team Agent to Standards Mapping

| Agent | Primary Standards | Key Requirements |
|-------|-------------------|------------------|
| **eng-architect** | NIST CSF 2.0 (Govern, Identify), OWASP ASVS V1, SAMM Design, SSDF PW.1/PW.2 | Threat modeling, security architecture, risk assessment, secure design patterns |
| **eng-lead** | NIST CSF 2.0 (Govern), SAMM Governance, SSDF PO, NIST 800-53 PM/PL | Security strategy, policy enforcement, team security practices, change control |
| **eng-backend** | OWASP Top 10 (A01-A10), ASVS V2/V4/V5/V6/V7/V8/V10/V13/V15, CWE Top 25, SSDF PW.5 | Input validation, authentication, authorization, cryptography, secure coding |
| **eng-frontend** | OWASP Top 10 (A01, A05, A07), ASVS V3/V5/V11, CWE Top 25 (XSS, CSRF) | XSS prevention, CSP, CORS, output encoding, client-side security |
| **eng-infra** | CIS Benchmarks (all categories), NIST 800-53 (AC/CM/CP/SC/SR), SSDF PS/PO.5, OWASP Top 10 A02/A03 | Configuration hardening, supply chain security, container security, secrets management |
| **eng-qa** | OWASP ASVS (test requirements), SAMM Verification, SSDF PW.8 | Security test cases, fuzzing, boundary testing, ASVS verification level testing |
| **eng-security** | All OWASP standards, NIST 800-53 (AU/CA/RA/SI), CWE Top 25, SSDF PW.7/RV | SAST/DAST, code review, vulnerability assessment, dependency auditing |
| **eng-reviewer** | OWASP ASVS (review checklists), SAMM Verification, SSDF PW.2/PW.7 | Architecture compliance, security standards verification, final quality gate |

### Standards Stack by Development Phase

| Development Phase | Applicable Standards | Primary Agent |
|-------------------|---------------------|---------------|
| Requirements | NIST CSF 2.0, OWASP ASVS V1, SAMM Design | eng-architect |
| Architecture | OWASP ASVS V1, NIST 800-53, SSDF PW.1 | eng-architect |
| Implementation | OWASP Top 10, CWE Top 25, SSDF PW.5, CIS Benchmarks | eng-backend, eng-frontend, eng-infra |
| Testing | OWASP ASVS (all), SAMM Verification, SSDF PW.8 | eng-qa, eng-security |
| Review | OWASP ASVS, SSDF PW.7, SAMM Verification | eng-reviewer, eng-security |
| Deployment | CIS Benchmarks, SSDF PS, NIST 800-53 CM | eng-infra |
| Operations | NIST CSF 2.0 (Detect/Respond/Recover), SSDF RV | eng-security, eng-infra |

---

## Evidence and Citations

### Industry Leaders

| Source | Date | Content |
|--------|------|---------|
| [OWASP Top 10:2025](https://owasp.org/Top10/2025/) | 2025 | Official 2025 OWASP Top 10 categories |
| [OWASP ASVS 5.0](https://owasp.org/www-project-application-security-verification-standard/) | 2025-05 | Application Security Verification Standard version 5.0 |
| [OWASP SAMM](https://owaspsamm.org/) | 2025 | Software Assurance Maturity Model v2 |
| [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/) | 2025 | Application security implementation guidance (Context7: High reputation, 78.5 benchmark) |
| [NIST CSF 2.0](https://csrc.nist.gov/pubs/cswp/29/final) | 2024-02 | Cybersecurity Framework version 2.0 |
| [NIST SP 800-53 Rev 5](https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final) | 2020 (Updated 2023) | Security and Privacy Controls for Information Systems |
| [NIST SP 800-218 SSDF v1.1](https://csrc.nist.gov/pubs/sp/800/218/final) | 2022-02 | Secure Software Development Framework |
| [NIST SP 800-218r1 SSDF v1.2 (Draft)](https://csrc.nist.gov/pubs/sp/800/218/r1/ipd) | 2025-12 | SSDF v1.2 draft with AI/ML practices |
| [CIS Benchmarks](https://www.cisecurity.org/cis-benchmarks) | 2025 | Center for Internet Security configuration benchmarks |
| [CISA -- 2025 CWE Top 25](https://www.cisa.gov/news-events/alerts/2025/12/11/2025-cwe-top-25-most-dangerous-software-weaknesses) | 2025-12 | 2025 Most Dangerous Software Weaknesses |
| [CWE Top 25 (MITRE)](https://cwe.mitre.org/top25/archive/2025/2025_cwe_top25.html) | 2025 | Official CWE Top 25 listing |

### Industry Experts

| Source | Date | Content |
|--------|------|---------|
| [Aikido -- OWASP Top 10 2025 Changes](https://www.aikido.dev/blog/owasp-top-10-2025-changes-for-developers) | 2025 | Analysis of 2021 to 2025 changes |
| [Codific -- OWASP Top 10 2025](https://codific.com/owasp-top-10-2025-what-it-is-what-changed-and-what-to-do-with-it/) | 2025 | Detailed 2025 Top 10 analysis with remediation |
| [Codific -- OWASP ASVS Overview](https://codific.com/owasp-asvs-a-comprehensive-overview/) | 2025 | Comprehensive ASVS analysis |
| [Codific -- OWASP SAMM Introduction](https://codific.com/owasp-samm-comprehensive-introduction/) | 2025 | SAMM v2 comprehensive introduction |
| [CyberChief -- OWASP ASVS v5](https://www.cyberchief.ai/2025/10/owasp-asvs-v5-raising-bar-for.html) | 2025-10 | ASVS 5.0 analysis |
| [Aikido -- NIST SSDF Explained](https://www.aikido.dev/learn/compliance/compliance-frameworks/nist-ssdf) | 2025 | SSDF practice group analysis |
| [CyberSaint -- NIST 800-53 Control Families](https://www.cybersaint.io/blog/nist-800-53-control-families) | 2025 | All 20 control families explained |

### Industry Innovators

| Source | Date | Content |
|--------|------|---------|
| [GitLab -- OWASP Top 10 2025 Changes](https://about.gitlab.com/blog/2025-owasp-top-10-whats-changed-and-why-it-matters/) | 2025 | Developer-focused 2025 analysis |
| [Fastly -- 2025 OWASP Top 10](https://www.fastly.com/blog/new-2025-owasp-top-10-list-what-changed-what-you-need-to-know) | 2025 | Infrastructure perspective on 2025 Top 10 |
| [NIST SSDF Project](https://csrc.nist.gov/projects/ssdf) | 2025 | Official SSDF project page with updates |

### Community Experts

| Source | Date | Content |
|--------|------|---------|
| [Pivot Point Security -- SAMM and ASVS Together](https://www.pivotpointsecurity.com/using-owasps-software-assurance-maturity-model-samm-and-application-security-verification-standard-asvs-together/) | 2024 | Combining SAMM and ASVS for comprehensive coverage |
| [Pivot Point Security -- SAMM 5 Business Functions](https://www.pivotpointsecurity.com/owasp-samms-5-business-functions-unpacked/) | 2024 | Detailed SAMM business function analysis |
| [SaltyCloud -- NIST 800-53 Control Families](https://www.saltycloud.com/blog/nist-800-53-control-families/) | 2025 | All 20 control families with complete listings |
| [SitGuarding -- MITRE CWE Top 25 2025 Analysis](https://www.siteguarding.com/security-blog/mitre-top-25-most-dangerous-software-weaknesses-2025-complete-analysis-and-protection-guide) | 2025 | Complete CWE Top 25 2025 analysis |

### Community Innovators

| Source | Date | Content |
|--------|------|---------|
| [Equixly -- OWASP Top 10 2025 vs 2021](https://equixly.com/blog/2025/12/01/owasp-top-10-2025-vs-2021/) | 2025-12 | Side-by-side comparison of 2021 and 2025 editions |
| [BleepingComputer -- 2025 CWE Top 25](https://www.bleepingcomputer.com/news/security/mitre-shares-2025s-top-25-most-dangerous-software-weaknesses/) | 2025-12 | CWE Top 25 2025 coverage |
| [Huntress -- CIS Benchmarks](https://www.huntress.com/cybersecurity-101/topic/what-are-cis-benchmarks) | 2025 | CIS Benchmarks overview |

---

## Recommendations

### R1: OWASP ASVS 5.0 as the Default Application Security Rule Set

OWASP ASVS 5.0 SHOULD be the default application security verification standard for /eng-team. Its 3-level assurance model provides a natural configuration axis:
- **Level 1:** Default for standard applications
- **Level 2:** Default for applications with sensitive data (recommended default)
- **Level 3:** Required for security-critical applications

Per R-011, users MUST be able to override the ASVS level and substitute organization-specific standards.

### R2: NIST SP 800-218 SSDF as the Secure SDLC Governance Framework

The SSDF SHOULD be the governance backbone for the /eng-team workflow. Its 4 practice groups map cleanly to the eng-team agent workflow:
- PO (Prepare) maps to eng-lead and eng-architect (planning, requirements)
- PS (Protect) maps to eng-infra (software protection, CI/CD security)
- PW (Produce) maps to all implementation and review agents
- RV (Respond) maps to eng-security (vulnerability response)

### R3: CIS Benchmarks as Default Infrastructure Configuration Baseline

CIS Benchmarks SHOULD be eng-infra's default configuration baseline. The Level 1/Level 2 distinction maps to engagement criticality:
- Level 1: Standard environments
- Level 2: High-security environments

### R4: CWE Top 25 as Primary Code Review Focus

eng-security SHOULD use the CWE Top 25 as the primary focus list for code reviews. The CWE IDs provide:
- Specific weakness identification (more precise than OWASP Top 10 categories)
- Direct mapping to CVEs for real-world vulnerability context
- Annually updated ranking based on observed exploitation data

### R5: OWASP Top 10 2025 as Security Awareness Baseline

OWASP Top 10 SHOULD be used as the security awareness document for all /eng-team agents. Every agent SHOULD understand all 10 categories and how they relate to their specific role. This is a baseline -- ASVS provides the detailed verification requirements.

### R6: NIST CSF 2.0 for Security Governance Architecture

eng-architect SHOULD use NIST CSF 2.0's 6 functions as the top-level security governance framework for system architecture. The Govern function's addition in 2.0 reinforces that security risk management strategy must be an explicit architectural concern.

### R7: SAMM for Maturity Assessment

OWASP SAMM SHOULD be available as a maturity assessment tool within /eng-team. eng-lead can use SAMM assessments to identify organizational security practice gaps and drive improvement. This is complementary to (not a replacement for) ASVS verification.

### R8: Standards Layering Strategy

The recommended standards layering for /eng-team:

| Layer | Standard | Purpose |
|-------|----------|---------|
| Governance | NIST CSF 2.0, SSDF | Strategic security risk management and SDLC governance |
| Architecture | OWASP ASVS V1, NIST 800-53 | Secure architecture requirements and control selection |
| Implementation | OWASP Top 10, CWE Top 25, OWASP ASVS, CIS Benchmarks | Secure coding, configuration hardening |
| Verification | OWASP ASVS (all levels), SAMM Verification | Security testing and verification |
| Maturity | OWASP SAMM | Organizational security practice maturity |
