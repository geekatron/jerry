# F-001: Secure SDLC Lifecycle Patterns

> Stream F: Secure SDLC | PROJ-010 Cyber Ops | Phase 1 Research

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | High-level synthesis of secure SDLC models |
| [L1: Key Findings](#l1-key-findings) | Numbered findings with evidence on each model |
| [L2: Detailed Analysis](#l2-detailed-analysis) | Deep comparison of MS SDL, NIST SSDF, OWASP SAMM, SLSA, DevSecOps |
| [Agent Workflow Mapping](#agent-workflow-mapping) | Which /eng-team agent handles which SDLC phase per model |
| [Comparison Matrix](#comparison-matrix) | Side-by-side model comparison across dimensions |
| [Evidence and Citations](#evidence-and-citations) | Categorized sources per R-006 |
| [Recommendations](#recommendations) | Numbered recommendations for /eng-team SDLC integration |

---

## L0: Executive Summary

Five secure SDLC models were analyzed for integration into the /eng-team skill: Microsoft SDL (classic and continuous), NIST SP 800-218 SSDF, OWASP SAMM, Google SLSA, and DevSecOps lifecycle patterns. Microsoft SDL provides the most mature phase-gate model with 5 core phases (requirements, design, implementation, verification, release) and continuous SDL extensions for CI/CD environments, directly mapping to the /eng-team workflow from eng-architect through eng-reviewer. NIST SSDF offers 4 outcome-based practice groups (Prepare, Protect, Produce, Respond) that serve as the governance backbone without prescribing implementation methodology, making it the natural compliance framework for /eng-team. OWASP SAMM provides organizational maturity measurement across 15 security practices in 5 business functions, enabling /eng-team to assess and improve security posture over time. Google SLSA addresses the supply chain security gap with 4 build levels of increasing provenance integrity, directly relevant to eng-infra and eng-devsecops responsibilities. DevSecOps patterns provide the CI/CD integration glue that connects all models through automated security tooling at every pipeline stage. The recommended architecture for /eng-team is a layered approach: NIST SSDF as the governance framework, Microsoft SDL phases mapped to the agent workflow, OWASP SAMM for maturity assessment, SLSA for supply chain integrity, and DevSecOps automation patterns for CI/CD integration.

---

## L1: Key Findings

### Finding 1: Microsoft SDL Has Evolved from Waterfall Gates to Continuous Security Measurement

Microsoft's SDL, originally developed in 2004, has undergone significant evolution. In 2023 alone, six new requirements were introduced, six were retired, and 19 received major updates (Microsoft Security Blog, March 2024). The continuous SDL model shifts from one-time phase-gate checks to frequent security state measurement throughout the development lifecycle. Microsoft is now investing in new threat modeling capabilities, accelerating adoption of memory-safe languages, and focusing on securing open-source software and the software supply chain. SDL is a critical pillar of the Microsoft Secure Future Initiative, a multi-year commitment to advance how Microsoft designs, builds, tests, and operates cloud technology. The 10 SDL practices are designed to integrate into existing development processes with minimal disruption, prioritized to rapidly reduce business risk. This evolution from static phase gates to continuous measurement directly aligns with the /eng-team model where agents operate throughout the lifecycle rather than only at designated checkpoints.

### Finding 2: NIST SSDF Is the Outcome-Based Governance Standard That Federal and Private Sectors Are Converging On

NIST SP 800-218 defines 4 practice groups with approximately 19 practices and 43 tasks that are methodology-agnostic and outcome-focused (NIST CSRC, February 2022). The framework is designed so that organizations adopt a risk-based approach to determine what practices are relevant. SSDF v1.2 (initial public draft December 2025) adds practices for AI/ML software security, enhanced supply chain integrity, and updated practices for container and serverless environments (NIST News, December 2025). CISA has endorsed SSDF as the baseline for federal software supply chain security. The SSDF's strength for /eng-team is that it prescribes outcomes (what secure software development looks like) without prescribing methods (how to achieve it), allowing the agent team to implement SSDF practices using whatever specific methodologies and tools are appropriate for the engagement context.

### Finding 3: OWASP SAMM Provides the Only Quantitative Maturity Assessment Model Among the Five Frameworks

OWASP SAMM v2 defines 15 security practices across 5 business functions (Governance, Design, Implementation, Verification, Operations), each with 2 activity streams and 3 maturity levels (OWASP SAMM, 2025). Unlike other models that define what to do, SAMM measures how well an organization does it. The maturity levels provide a progression path: Level 1 represents initial, ad-hoc practices; Level 2 represents defined and repeatable practices; Level 3 represents optimized and measured practices. For /eng-team, SAMM provides the assessment dimension that other frameworks lack -- eng-lead can use SAMM to evaluate the maturity of the team's security practices and identify improvement priorities. The 15 practices map directly to /eng-team agent responsibilities, making SAMM assessments actionable rather than theoretical.

### Finding 4: Google SLSA Addresses the Supply Chain Gap That Other SDLC Models Underserve

SLSA v1.0 defines a Build track with 4 levels of increasing supply chain integrity (SLSA.dev, 2024). Build L0 represents no SLSA (baseline). Build L1 requires provenance documentation showing how the package was built. Build L2 requires a hosted build service that generates and signs provenance through digital signatures. Build L3 requires builds in isolated environments (containers or VMs created specifically for the build) that are not reused and cannot be influenced by other build processes. SLSA was contributed to and is now governed by the OpenSSF (Open Source Security Foundation). The OWASP Top 10 2025 introduced A03 Software Supply Chain Failures as a new category (B-003 Finding 1), and SLSA directly addresses this emerging risk. For /eng-team, SLSA maps primarily to eng-infra (build infrastructure) and eng-devsecops (CI/CD pipeline security), with eng-reviewer validating SLSA level compliance.

### Finding 5: DevSecOps Integration Patterns Provide the Automation Layer That Connects All Models

The DevSecOps market grew to USD 8.93 billion in 2024 and is projected to reach USD 26.21 billion by 2032 (Fortune Business Insights, 2025), reflecting industry-wide adoption. The core principle is shift-left: integrating security checks at every pipeline stage rather than bolting them on at the end. Vulnerabilities discovered during coding cost approximately 10x less to fix than those found in later stages (MosChip, December 2025). DevSecOps is not a standalone framework but an integration pattern that operationalizes the other four models through automation: SAST/DAST in the pipeline (MS SDL verification phase), provenance generation (SLSA), automated policy enforcement (SSDF PW practices), and continuous measurement (SAMM Operations function). For /eng-team, DevSecOps patterns are primarily the domain of eng-devsecops, with eng-infra managing the pipeline infrastructure and eng-security configuring the security tooling.

### Finding 6: All Five Models Converge on Supply Chain Security as the Critical Emerging Concern

Microsoft SDL's 2023 updates explicitly focus on securing open-source software and the software supply chain. NIST SSDF v1.2 enhances supply chain integrity practices. OWASP Top 10 2025 introduced A03 Software Supply Chain Failures. Google SLSA's entire purpose is supply chain integrity. DevSecOps pipelines increasingly include SCA (Software Composition Analysis) and SBOM generation. This convergence validates the A-004 roster decision to expand eng-infra's scope to include explicit supply chain security (SBOM generation, dependency provenance, build reproducibility) and the addition of eng-devsecops for automated dependency analysis and container scanning. The /eng-team architecture must treat supply chain security as a first-class concern distributed across eng-infra (infrastructure), eng-devsecops (tooling), and eng-reviewer (verification).

---

## L2: Detailed Analysis

### Microsoft SDL (Security Development Lifecycle)

#### Classic SDL: 5 Core Phases

| Phase | Activities | Security Practices | /eng-team Agent |
|-------|-----------|-------------------|-----------------|
| **Requirements** | Define security requirements, quality gates, risk assessment | Establish security and privacy requirements, create quality gates/bug bars, perform security and privacy risk assessments | eng-architect, eng-lead |
| **Design** | Threat modeling, attack surface analysis, design review | Establish design requirements, perform attack surface analysis/reduction, use threat modeling (STRIDE/DREAD per B-004) | eng-architect |
| **Implementation** | Secure coding, static analysis, banned functions | Specify tools and toolchains, enforce banned functions, perform static analysis (SAST) | eng-backend, eng-frontend, eng-devsecops |
| **Verification** | Dynamic testing, fuzz testing, attack surface review | Perform dynamic analysis (DAST), fuzz testing, attack surface review | eng-qa, eng-security, eng-reviewer |
| **Release** | Incident response plan, final security review, archive | Create incident response plan, conduct final security review, certify release and archive | eng-reviewer, eng-incident |

#### Continuous SDL Evolution

| Aspect | Classic SDL | Continuous SDL |
|--------|------------|----------------|
| Measurement frequency | Per-phase gates | Continuous throughout lifecycle |
| Threat modeling | Once during design | Updated throughout lifecycle |
| Security tooling | Pre-release verification | Integrated into CI/CD pipeline |
| Supply chain | Not originally addressed | Explicit focus area (2023 update) |
| AI/ML security | Not addressed | Responsible AI integrated into SDL |
| Memory safety | Language-agnostic | Accelerating memory-safe language adoption |
| Update cadence | Periodic major revisions | Annual requirement updates (6 added, 6 retired, 19 updated in 2023) |

#### Microsoft SDL 10 Security Practices (2024)

| # | Practice | Description |
|---|----------|-------------|
| 1 | Provide Training | Security awareness and skills development |
| 2 | Define Security Requirements | Define minimum security baselines |
| 3 | Define Metrics and Compliance Reporting | Track security posture quantitatively |
| 4 | Perform Threat Modeling | STRIDE-based systematic threat identification |
| 5 | Establish Design Requirements | Secure design patterns and principles |
| 6 | Define and Use Cryptography Standards | Approved algorithms, key management |
| 7 | Manage the Security Risk of Using Third-Party Components | SCA, dependency management, SBOM |
| 8 | Use Approved Tools | Standardized, vetted toolchains |
| 9 | Perform Security Testing (SAST/DAST/Pen Testing) | Multi-layer security testing |
| 10 | Establish a Standard Incident Response Process | Preparedness for post-release vulnerabilities |

### NIST SP 800-218 SSDF

#### 4 Practice Groups with Practices and Tasks

| Practice Group | ID | Practices | Key Tasks | /eng-team Agent(s) |
|----------------|----|-----------|-----------|---------------------|
| **Prepare the Organization** | PO | PO.1: Define security requirements | Identify and document security requirements for software | eng-architect, eng-lead |
| | | PO.2: Implement roles and responsibilities | Assign security-relevant roles | eng-lead |
| | | PO.3: Implement supporting toolchains | Deploy and configure security tools | eng-devsecops |
| | | PO.4: Define criteria for security checks | Establish pass/fail criteria | eng-reviewer, eng-security |
| | | PO.5: Implement secure environments | Harden development, build, and deployment environments | eng-infra |
| **Protect the Software** | PS | PS.1: Protect all forms of code | Source code access control, integrity verification | eng-infra |
| | | PS.2: Verify software release integrity | Signing, checksums, provenance | eng-infra, eng-devsecops |
| | | PS.3: Archive and protect each release | Release artifact management | eng-infra |
| **Produce Well-Secured Software** | PW | PW.1: Design to meet security requirements | Secure architecture and threat modeling | eng-architect |
| | | PW.2: Review software design | Architecture review for security compliance | eng-architect, eng-reviewer |
| | | PW.4: Reuse well-secured software | Vetted libraries and components | eng-backend, eng-frontend |
| | | PW.5: Adhere to secure coding practices | OWASP, CWE, language-specific standards | eng-backend, eng-frontend |
| | | PW.6: Configure compilation and build securely | Compiler flags, build hardening | eng-infra, eng-devsecops |
| | | PW.7: Review human-readable code | Manual and automated code review | eng-security, eng-reviewer |
| | | PW.8: Test executable code | SAST, DAST, fuzzing, penetration testing | eng-qa, eng-security |
| | | PW.9: Configure software for secure defaults | Secure-by-default configuration | eng-backend, eng-infra |
| **Respond to Vulnerabilities** | RV | RV.1: Identify and confirm vulnerabilities | Vulnerability discovery and triage | eng-security, eng-incident |
| | | RV.2: Assess, prioritize, and remediate | Risk-based vulnerability management | eng-incident, eng-security |
| | | RV.3: Analyze root causes | Root cause analysis to prevent recurrence | eng-incident, eng-architect |

#### SSDF v1.2 Draft Updates (December 2025)

| Update Area | Description | /eng-team Impact |
|-------------|-------------|------------------|
| AI/ML practices | New practices for AI model security throughout SDLC | Future extension for AI-assisted agents |
| Supply chain integrity | Enhanced practices for software provenance and SBOM | Strengthens eng-infra and eng-devsecops scope |
| Container and serverless | Updated practices for modern deployment models | Directly relevant to eng-infra |
| Generative AI profile | SP 800-218A augments SSDF for generative AI development | Relevant if /eng-team builds AI-integrated systems |

### OWASP SAMM v2

#### 5 Business Functions, 15 Security Practices, 30 Activity Streams

| Business Function | Security Practice | Stream A | Stream B | /eng-team Agent |
|-------------------|-------------------|----------|----------|-----------------|
| **Governance** | Strategy and Metrics | Create and promote | Measure and improve | eng-lead |
| | Policy and Compliance | Policy and standards | Compliance management | eng-lead, eng-reviewer |
| | Education and Guidance | Training and awareness | Organization and culture | eng-lead |
| **Design** | Threat Assessment | Application risk profile | Threat modeling | eng-architect |
| | Security Requirements | Software requirements | Supplier security | eng-architect, eng-lead |
| | Security Architecture | Architecture design | Technology management | eng-architect |
| **Implementation** | Secure Build | Build process | Software dependencies | eng-devsecops, eng-infra |
| | Secure Deployment | Deployment process | Secret management | eng-infra |
| | Defect Management | Defect tracking | Metrics and feedback | eng-security, eng-incident |
| **Verification** | Architecture Assessment | Architecture validation | Architecture mitigation | eng-reviewer, eng-architect |
| | Requirements-Driven Testing | Control verification | Misuse/abuse testing | eng-qa |
| | Security Testing | Scalable baseline | Deep understanding | eng-security, eng-qa |
| **Operations** | Incident Management | Detection | Response | eng-incident |
| | Environment Management | Configuration hardening | Patching and updating | eng-infra |
| | Operational Management | Data protection | System decomissioning | eng-infra, eng-lead |

#### Maturity Level Progression

| Level | Characteristics | Verification Method | /eng-team Application |
|-------|----------------|--------------------|-----------------------|
| **Level 1** | Initial, ad-hoc practices; basic awareness | Self-assessment | Minimum baseline for any /eng-team engagement |
| **Level 2** | Defined and repeatable; consistently applied | Peer review, tooling validation | Standard target for most engagements |
| **Level 3** | Optimized and measured; continuous improvement | Metrics-driven, /adversary C4 review | Target for mission-critical (C4) engagements |

### Google SLSA (Supply-chain Levels for Software Artifacts)

#### Build Track: 4 Levels

| Level | Requirements | Provenance | Build Platform | /eng-team Agent |
|-------|-------------|-----------|----------------|-----------------|
| **Build L0** | No requirements | None | Any | (Baseline -- no SLSA) |
| **Build L1** | Provenance exists documenting how package was built | Automatically generated; includes build platform and process | Any (including local) | eng-devsecops (generates provenance) |
| **Build L2** | Hosted build service generates and signs provenance | Authenticated; signed by build service | Hosted service (GitHub Actions, Google Cloud Build, etc.) | eng-infra (hosts build), eng-devsecops (configures signing) |
| **Build L3** | Isolated build environment; tamper protection | Authenticated; signed; verifiably isolated | Hardened hosted service with isolation (containers/VMs not reused) | eng-infra (hardens build platform), eng-devsecops (validates isolation) |

#### SLSA Provenance Requirements

| Aspect | L1 | L2 | L3 |
|--------|----|----|-----|
| **Completeness** | Build platform, process, inputs documented | L1 + builder identity authenticated | L2 + input dependencies tracked |
| **Authenticity** | Provenance exists | Provenance signed by build service | Provenance from hardened, isolated builder |
| **Accuracy** | Best effort | Resistant to forgery | Resistant to insider tampering within build process |

#### SLSA and OWASP Top 10 2025 A03 Mapping

| OWASP A03 Concern | SLSA Mitigation | Level Required |
|--------------------|-----------------|----------------|
| Compromised build pipeline | Isolated build environments, provenance signing | Build L2+ |
| Tampered dependencies | Dependency provenance tracking, SBOM integration | Build L3 |
| Unverified package sources | Provenance authentication, build platform attestation | Build L2+ |
| Missing build reproducibility | Build isolation, non-reusable environments | Build L3 |

### DevSecOps Lifecycle Integration Patterns

#### Security Activities by Pipeline Stage

| Pipeline Stage | Security Activities | Tools (Representative) | /eng-team Agent |
|----------------|--------------------|-----------------------|-----------------|
| **Plan** | Threat modeling, security requirements, risk assessment | Microsoft Threat Modeling Tool, OWASP Threat Dragon | eng-architect |
| **Code** | Secure coding standards, pre-commit hooks, IDE security plugins | Semgrep, SonarLint, ESLint security rules | eng-backend, eng-frontend |
| **Build** | SAST, dependency analysis, license compliance, SBOM generation | Semgrep, Snyk, OWASP Dependency-Check, Syft | eng-devsecops |
| **Test** | DAST, IAST, fuzzing, security regression testing | OWASP ZAP, Burp Suite, AFL, OSS-Fuzz | eng-qa, eng-security |
| **Release** | Container scanning, IaC scanning, signing, provenance | Trivy, Checkov, Cosign, SLSA generators | eng-infra, eng-devsecops |
| **Deploy** | Configuration validation, secrets scanning, runtime protection | CIS Benchmarks, TruffleHog, Falco | eng-infra |
| **Operate** | Vulnerability monitoring, incident response, patching | Dependabot, NIST NVD, PagerDuty | eng-incident, eng-infra |
| **Monitor** | SIEM integration, anomaly detection, audit logging | ELK Stack, Splunk, Datadog | eng-security, eng-incident |

#### Shift-Left Economics

| Discovery Phase | Relative Cost to Fix | SDLC Model Alignment |
|-----------------|---------------------|---------------------|
| Requirements/Design | 1x (baseline) | MS SDL Requirements/Design, SSDF PO/PW.1 |
| Implementation | 6.5x | MS SDL Implementation, SSDF PW.5 |
| Testing | 15x | MS SDL Verification, SSDF PW.8 |
| Production | 100x | SSDF RV, SAMM Operations |

---

## Agent Workflow Mapping

### /eng-team Agent to Secure SDLC Phase Mapping

| /eng-team Agent | MS SDL Phase | SSDF Practice Group | SAMM Business Function | SLSA Role | DevSecOps Stage |
|-----------------|-------------|---------------------|----------------------|-----------|-----------------|
| eng-architect | Requirements, Design | PO (PO.1), PW (PW.1, PW.2) | Design (all 3 practices) | -- | Plan |
| eng-lead | Requirements | PO (PO.1, PO.2, PO.4) | Governance (all 3 practices) | -- | Plan |
| eng-backend | Implementation | PW (PW.4, PW.5, PW.9) | Implementation (Secure Build) | -- | Code |
| eng-frontend | Implementation | PW (PW.4, PW.5, PW.9) | Implementation (Secure Build) | -- | Code |
| eng-infra | Implementation, Release | PS (all), PO.5, PW.6 | Implementation (Secure Deployment), Operations (Environment Mgmt) | Build platform owner (L2/L3) | Build, Release, Deploy |
| eng-qa | Verification | PW (PW.8) | Verification (Requirements-Driven Testing, Security Testing) | -- | Test |
| eng-security | Verification | PW (PW.7, PW.8), RV.1 | Verification (all 3 practices) | -- | Test, Monitor |
| eng-reviewer | Verification, Release | PW (PW.2, PW.7), PO.4 | Verification (Architecture Assessment) | Provenance verifier | Release |
| eng-devsecops | Implementation, Verification | PO.3, PS.2, PW.6 | Implementation (Secure Build) | Provenance generator (L1+), signing (L2+) | Build, Release |
| eng-incident | Release (IR plan), Post-release | RV (all) | Operations (Incident Management) | -- | Operate, Monitor |

### Workflow Sequence with SDLC Model Integration

```
1. eng-architect  --> MS SDL Requirements/Design + SSDF PO/PW.1 + SAMM Design
   Output: Architecture + Threat Model (STRIDE/DREAD per B-004)

2. eng-lead       --> MS SDL Requirements + SSDF PO + SAMM Governance
   Output: Implementation Plan + Security Standards Selection

3. eng-backend    --> MS SDL Implementation + SSDF PW.5 + OWASP Top 10/CWE Top 25
   eng-frontend   --> MS SDL Implementation + SSDF PW.5 + OWASP ASVS V3
   eng-infra      --> MS SDL Implementation + SSDF PS/PO.5 + CIS Benchmarks + SLSA L2/L3
   Output: Secure Implementation + Build Infrastructure + SLSA Provenance

4. eng-devsecops  --> DevSecOps Pipeline + SSDF PO.3/PS.2 + SLSA L1+
   Output: SAST/DAST Pipeline + Dependency Analysis + SBOM + Signed Provenance

5. eng-qa         --> MS SDL Verification + SSDF PW.8 + SAMM Verification
   Output: Security Test Results + Fuzzing Results

6. eng-security   --> MS SDL Verification + SSDF PW.7/RV.1 + CWE Top 25
   Output: Secure Code Review + Vulnerability Assessment

7. eng-reviewer   --> MS SDL Release + SSDF PW.2/PO.4 + SAMM Architecture Assessment
   Output: Final Security Gate (with /adversary C4 for mission-critical)

8. eng-incident   --> MS SDL Release (IR Plan) + SSDF RV + SAMM Operations
   Output: Incident Response Plan + Runbooks
```

---

## Comparison Matrix

### Model Comparison Across Key Dimensions

| Dimension | Microsoft SDL | NIST SSDF | OWASP SAMM | Google SLSA | DevSecOps |
|-----------|--------------|-----------|------------|-------------|-----------|
| **Type** | Phase-gate lifecycle model | Outcome-based practice framework | Maturity assessment model | Supply chain integrity specification | Integration pattern |
| **Scope** | Full SDLC | Full SDLC | Full SDLC + organizational maturity | Build and release (supply chain) | CI/CD pipeline |
| **Prescriptiveness** | Medium (practices defined, methods flexible) | Low (outcomes defined, methods open) | Medium (practices + levels defined) | High (specific requirements per level) | Low (patterns, not prescriptions) |
| **Measurement** | Compliance checks per phase | Practice adoption assessment | 3-level maturity scoring (quantitative) | 4-level build integrity (binary pass/fail) | Automated tool metrics |
| **Supply chain focus** | Added in 2023 updates | PS practice group + v1.2 enhancements | Secure Build practice (Implementation) | Primary and sole focus | SCA and SBOM in pipeline |
| **Threat modeling** | Core requirement (Practice 4) | PW.1 (design to meet security requirements) | Design function (Threat Assessment) | Not addressed | Plan stage activity |
| **Automation suitability** | High (continuous SDL) | Medium (outcomes require interpretation) | Low (assessment is manual/judgment-based) | High (automated provenance) | Very high (CI/CD native) |
| **Governance body** | Microsoft (proprietary) | NIST (US government) | OWASP (open community) | OpenSSF (open foundation) | Industry practice (no single owner) |
| **Regulatory adoption** | Industry standard (de facto) | US federal mandate (EO 14028) | Voluntary assessment | Growing adoption (OpenSSF ecosystem) | Industry standard (de facto) |
| **Agent team fit** | Excellent (phases map to agents) | Excellent (practices map to agents) | Good (assessment complements execution) | Good (specific to infra/devsecops) | Excellent (pipeline maps to agents) |

### Model Complementarity Matrix

| Model Pair | Relationship | Integration Point |
|------------|-------------|-------------------|
| MS SDL + SSDF | SDL phases implement SSDF practices | SDL Design phase implements SSDF PW.1; SDL Verification implements SSDF PW.7/PW.8 |
| MS SDL + SAMM | SAMM measures SDL practice maturity | SDL practices are assessed using SAMM maturity levels |
| MS SDL + SLSA | SLSA specifies SDL Release phase supply chain | SDL Release implements SLSA Build L2/L3 requirements |
| MS SDL + DevSecOps | DevSecOps automates SDL practices | Continuous SDL is DevSecOps applied to SDL |
| SSDF + SAMM | SSDF defines what; SAMM measures how well | SAMM maturity levels apply to SSDF practice adoption |
| SSDF + SLSA | SLSA operationalizes SSDF PS practices | SSDF PS.2 (verify release integrity) maps to SLSA provenance |
| SSDF + DevSecOps | DevSecOps automates SSDF tasks | SSDF PO.3 (implement toolchains) is DevSecOps pipeline |
| SAMM + DevSecOps | DevSecOps implementation drives SAMM maturity | SAMM Implementation/Verification maturity increases with DevSecOps adoption |
| SLSA + DevSecOps | SLSA requirements are implemented in DevSecOps pipeline | SLSA provenance generation is a DevSecOps pipeline stage |

---

## Evidence and Citations

### Industry Leaders

| Source | Date | Content |
|--------|------|---------|
| [Microsoft -- Evolving SDL: How Continuous SDL Can Help](https://www.microsoft.com/en-us/security/blog/2024/03/07/evolving-microsoft-security-development-lifecycle-sdl-how-continuous-sdl-can-help-you-build-more-secure-software/) | March 2024 | Continuous SDL evolution, 2023 updates (6 new, 6 retired, 19 updated requirements) |
| [Microsoft -- Security Development Lifecycle](https://www.microsoft.com/en-us/securityengineering/sdl) | 2025 | Official SDL overview: 5 core phases, 10 security practices |
| [Microsoft -- SDL Practices](https://www.microsoft.com/en-us/securityengineering/sdl/practices) | 2025 | Detailed 10 SDL practices for integration into development processes |
| [Microsoft Learn -- SDL Service Assurance](https://learn.microsoft.com/en-us/compliance/assurance/assurance-microsoft-security-development-lifecycle) | 2025 | SDL requirements, automated tooling, commit pipeline integration |
| [NIST SP 800-218 SSDF v1.1](https://csrc.nist.gov/pubs/sp/800/218/final) | February 2022 | SSDF 4 practice groups, 19 practices, 43 tasks |
| [NIST SP 800-218r1 SSDF v1.2 (Draft)](https://csrc.nist.gov/pubs/sp/800/218/r1/ipd) | December 2025 | SSDF v1.2 with AI/ML practices, supply chain enhancements |
| [NIST -- SSDF v1.2 Available for Public Comment](https://www.nist.gov/news-events/news/2025/12/secure-software-development-framework-ssdf-version-12-available-public) | December 2025 | SSDF v1.2 draft announcement per EO 14306 |
| [CISA -- NIST SSDF v1.1 Resources](https://www.cisa.gov/resources-tools/resources/nist-sp-800-218-secure-software-development-framework-v11-recommendations-mitigating-risk-software) | 2025 | Federal endorsement of SSDF |
| [OWASP SAMM](https://owaspsamm.org/) | 2025 | Official SAMM v2 site: 5 business functions, 15 practices, 3 maturity levels |
| [OWASP SAMM -- The Model](https://owaspsamm.org/model/) | 2025 | Detailed model structure and practice definitions |
| [SLSA -- Supply-chain Levels for Software Artifacts](https://slsa.dev/) | 2025 | Official SLSA specification site |
| [SLSA -- Security Levels v1.0](https://slsa.dev/spec/v1.0/levels) | 2024 | Build L0-L3 requirements, provenance specifications |
| [SLSA -- What's New in v1.0](https://slsa.dev/spec/v1.0/whats-new) | 2024 | Track-based structure, simplified requirements |
| [OpenSSF -- SLSA Project](https://openssf.org/projects/slsa/) | 2025 | SLSA governance and OpenSSF integration |

### Industry Experts

| Source | Date | Content |
|--------|------|---------|
| [Aikido -- NIST SSDF Explained](https://www.aikido.dev/learn/compliance/compliance-frameworks/nist-ssdf) | 2025 | SSDF practice group analysis and implementation guidance |
| [Black Duck -- Implementing NIST SSDF Best Practices](https://www.blackduck.com/blog/nist-ssdf-secure-software-development.html) | 2025 | SSDF implementation best practices for enterprises |
| [Codific -- OWASP SAMM Comprehensive Introduction](https://codific.com/owasp-samm-comprehensive-introduction/) | 2025 | Detailed SAMM v2 analysis with practice breakdowns |
| [SecureTeam -- Exploring OWASP SAMM](https://secureteam.co.uk/2025/01/25/exploring-the-owasp-software-assurance-maturity-model-samm/) | January 2025 | SAMM exploration with practical application guidance |
| [Threat-Modeling.com -- Microsoft SDL](https://threat-modeling.com/microsoft-security-development-lifecycle-sdl/) | 2025 | Comprehensive SDL analysis with threat modeling focus |
| [Cycode -- SLSA Framework Key Takeaways](https://cycode.com/blog/key-takeaways-from-google-slsa-cybersecurity-framework/) | 2025 | SLSA practical implications for development teams |
| [Cycode -- Mastering SDLC Security](https://cycode.com/blog/mastering-sdlc-security-best-practices/) | 2025 | SDLC security best practices across models |

### Industry Innovators

| Source | Date | Content |
|--------|------|---------|
| [Wiz -- SLSA Framework](https://www.wiz.io/academy/application-security/slsa-framework) | 2025 | SLSA framework analysis with cloud security context |
| [Chainguard Academy -- Introduction to SLSA](https://edu.chainguard.dev/compliance/slsa/what-is-slsa/) | 2025 | SLSA educational overview with supply chain focus |
| [Sonar -- SLSA Supply Chain Levels](https://www.sonarsource.com/resources/library/slsa/) | 2025 | SLSA integration with code quality workflows |
| [Xygeni -- OWASP SAMM](https://xygeni.io/articles/owasp-samm-software-assurance-maturity-model/) | 2025 | SAMM application in modern software supply chain security |
| [Jit -- SSDLC Overview](https://www.jit.io/resources/devsecops/ssdlc-secure-software-development-lifecycle) | 2025 | Secure SDLC patterns and DevSecOps integration |
| [UpCoreTech -- DevSecOps Pipelines 2024](https://www.upcoretech.com/insights/devsecops-pipelines/) | 2024 | DevSecOps pipeline architecture and tooling |

### Community Leaders

| Source | Date | Content |
|--------|------|---------|
| [NIST SSDF Project Page](https://csrc.nist.gov/projects/ssdf) | 2025 | Official SSDF project with updates and community resources |
| [OWASP SAMM -- Quick Start Guide](https://owaspsamm.org/guidance/quick-start-guide/) | 2025 | SAMM v2 quick start for organizations |
| [SLSA -- Producing Artifacts Requirements](https://slsa.dev/spec/v1.0/requirements) | 2024 | Detailed SLSA producer and build platform requirements |
| [SLSA -- Provenance Specification](https://slsa.dev/spec/v1.0/provenance) | 2024 | SLSA provenance format and content requirements |

### Community Experts

| Source | Date | Content |
|--------|------|---------|
| [MosChip -- DevSecOps: Integrating Security at Every SDLC Stage](https://moschip.com/blog/quality-automation-engineering/devsecops-integrating-security-at-every-stage-of-the-sdlc/) | December 2025 | DevSecOps lifecycle integration with 10x cost reduction data |
| [Fidelis Security -- DevSecOps in SDLC](https://fidelissecurity.com/cybersecurity-101/cloud-security/what-is-devsecops/) | 2025 | DevSecOps methodology for secure agile development |
| [ImpactQA -- DevSecOps Methodology](https://www.impactqa.com/blog/how-does-devsecops-methodology-help-integrate-security-into-the-devops-lifecycle-efficiently/) | 2025 | DevSecOps integration efficiency analysis |
| [JFrog -- Secure SDLC](https://jfrog.com/learn/devsecops/ssdlc-secure-software-development-lifecycle/) | 2025 | SSDLC with software supply chain management focus |
| [Knowledge Junction -- Exploring Microsoft SDL](https://knowledge-junction.in/2024/01/07/exploring-microsoft-security-development-lifecycle-sdl/) | January 2024 | SDL phase-by-phase exploration |
| [OWASP Developer Guide -- SAMM](https://devguide.owasp.org/en/11-security-gap-analysis/01-guides/01-samm/) | 2025 | SAMM integration into developer workflow |

### Community Innovators

| Source | Date | Content |
|--------|------|---------|
| [Leanware -- Secure Development Lifecycle Guide](https://www.leanware.co/insights/secure-development-lifecycle-guide) | 2025 | SDL best practices and implementation guide |
| [ActiveState -- SLSA](https://www.activestate.com/resources/quick-reads/supply-chain-levels-for-software-artifacts-slsa/) | 2025 | SLSA practical implementation for development teams |
| [Google Cloud Blog -- SLSA Framework Introduction](https://cloud.google.com/blog/products/application-development/google-introduces-slsa-framework) | 2025 | Original SLSA introduction and Google's internal practices |

---

## Recommendations

### R-SDLC-001: Adopt NIST SSDF as the Governance Framework for /eng-team

NIST SSDF SHOULD be the governance backbone for the /eng-team skill. Its 4 practice groups (PO, PS, PW, RV) map directly to /eng-team agent responsibilities without prescribing specific implementation methods. This allows the agent team to adapt practices to engagement context while maintaining compliance with a recognized government and industry standard. Each agent's security responsibilities can be traced to specific SSDF practices and tasks, providing audit trail and accountability. Priority: HIGH.

### R-SDLC-002: Implement Microsoft SDL Phases as the /eng-team Workflow Structure

Microsoft SDL's 5-phase model (Requirements, Design, Implementation, Verification, Release) SHOULD define the /eng-team workflow sequence. The continuous SDL evolution (measuring security state frequently, not just at phase gates) aligns with /eng-team's agent-based model where security is enforced at every step through agent-specific rules. The 10 SDL practices provide concrete activities that map to individual agent responsibilities. Priority: HIGH.

### R-SDLC-003: Integrate OWASP SAMM for Maturity Assessment Capability

OWASP SAMM SHOULD be available within /eng-team for eng-lead to assess and track security practice maturity. SAMM assessments should be performed at engagement start (baseline) and end (progress measurement). The 3 maturity levels provide a natural progression path that eng-lead can use to set targets and measure improvement. SAMM is complementary to (not a replacement for) SSDF compliance and SDL phase execution. Priority: MEDIUM.

### R-SDLC-004: Require SLSA Build L2 as Minimum for Production Releases

eng-infra and eng-devsecops SHOULD implement SLSA Build L2 (hosted build service with signed provenance) as the minimum requirement for production releases. SLSA Build L3 (isolated, hardened build environments) SHOULD be required for security-critical (C3/C4) engagements. This directly addresses the supply chain security convergence identified in Finding 6 and OWASP Top 10 2025 A03 (Software Supply Chain Failures). Priority: HIGH.

### R-SDLC-005: Implement DevSecOps Automation Patterns for CI/CD Integration

eng-devsecops SHOULD implement automated security gates at every CI/CD pipeline stage following the DevSecOps integration pattern: SAST at build, DAST at test, SCA at build, container scanning at release, configuration validation at deploy. This automation layer operationalizes the MS SDL continuous measurement model and the SSDF PO.3 (implement supporting toolchains) practice. Pipeline security gates should be configurable per R-011. Priority: HIGH.

### R-SDLC-006: Use a Layered SDLC Model Architecture

/eng-team SHOULD implement a layered SDLC model architecture where each model serves a distinct purpose:
- **Layer 1 (Governance):** NIST SSDF -- compliance framework and practice requirements
- **Layer 2 (Lifecycle):** Microsoft SDL -- phase structure and workflow sequence
- **Layer 3 (Assessment):** OWASP SAMM -- maturity measurement and improvement tracking
- **Layer 4 (Supply Chain):** Google SLSA -- build integrity and provenance
- **Layer 5 (Automation):** DevSecOps -- CI/CD pipeline security integration

This layered approach avoids model conflict by assigning each framework to its area of strength. Priority: HIGH.

### R-SDLC-007: Make SDLC Model Selection Configurable per R-011

Per R-011 (Configurable Rule Sets), users MUST be able to override the default SDLC model selection. Organizations may use different frameworks (e.g., BSIMM instead of SAMM, ISO 27034 instead of SSDF). The /eng-team architecture should support: substitution of governance framework, modification of phase-gate criteria, alternative maturity models, and custom supply chain integrity levels. Priority: MEDIUM.

### R-SDLC-008: Map All Agent Security Activities to SSDF Practice IDs

Every security activity performed by an /eng-team agent SHOULD include a reference to the SSDF practice and task it implements (e.g., eng-security code review references PW.7). This provides traceability from agent outputs to governance framework compliance, supporting audit requirements and enabling eng-reviewer to verify completeness of SSDF practice coverage. Priority: MEDIUM.
