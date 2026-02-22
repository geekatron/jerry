# A-001: Elite Security Engineering Team Structures

> Stream A: Role Completeness | PROJ-010 Cyber Ops | Phase 1 Research

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | 3-5 sentence overview for any stakeholder |
| [L1: Key Findings](#l1-key-findings) | Structured findings by theme |
| [L2: Detailed Analysis](#l2-detailed-analysis) | Deep analysis with tables, comparisons, mappings |
| [Evidence and Citations](#evidence-and-citations) | All sources categorized by authority type |
| [Gap Analysis](#gap-analysis) | Missing roles in proposed /eng-team roster |
| [Recommendations](#recommendations) | Specific agent roster change recommendations |

---

## L0: Executive Summary

Elite security-focused engineering teams at Google, Microsoft, CrowdStrike, and Mandiant consistently organize around specialized functional areas rather than general-purpose engineering roles. Google's Chrome Security team operates with distinct sub-teams (Product Security, Fuzzing, Security Architecture) while Project Zero maintains a small team of specialist vulnerability researchers using both manual code review and automated fuzzing. Microsoft's Secure Future Initiative has embedded Deputy CISOs in every engineering division and is deploying "Durability Architects" and a global Security Ambassador program to create security-first culture at scale. CrowdStrike's ~1,778-person engineering organization (30% of workforce) operates with fluid role boundaries to solve customer problems end-to-end. Mandiant employs a "team of teams" model integrating forensics, threat intelligence, malware analysis, remediation, and crisis communications. The proposed /eng-team roster covers core engineering functions but has notable gaps in threat intelligence, incident response, compliance/governance, and DevSecOps pipeline engineering that elite teams consistently staff as distinct specializations.

---

## L1: Key Findings

### Finding 1: Security is Embedded, Not Bolted On

Every elite organization studied has moved away from "security team reviews engineering output" toward security being structurally embedded in engineering teams. Microsoft's Secure Future Initiative (April 2025) is the most visible example: 14 Deputy CISOs now sit inside engineering divisions, not in a separate security organization. Google's Chrome Security team has dedicated security engineers working within the Chrome product team, not as external reviewers. This "embedded model" contrasts with the /eng-team's proposed workflow where eng-security appears as a sequential review step (step 5 of 7), suggesting a bolt-on pattern rather than embedded security.

### Finding 2: Specialization Depth Exceeds Proposed Roster

Google Chrome Security operates with at least three distinct specialized sub-teams within security alone:
- **Product Security**: Vulnerability management, incident response, security update release management, coordination and disclosure
- **Fuzzing Team**: Automated vulnerability discovery, MojoJS fuzzer, WebIDL fuzzer, browser fuzztests
- **Security Architecture Team**: Origin calculation security, process isolation, out-of-process iframes security

The proposed /eng-team collapses all of these into a single eng-security role. Elite teams have found that fuzzing, architecture review, and vulnerability management require distinct specializations.

### Finding 3: Threat Intelligence is a Distinct Function

Mandiant's "team of teams" model explicitly separates threat intelligence from other security functions. Threat intelligence analysts identify threat actors, tactics, and indicators of compromise -- this is a research and analysis function distinct from security engineering. CrowdStrike's Falcon platform is built around threat intelligence as a core product function. The proposed /eng-team has no threat intelligence capability, meaning defensive engineering decisions would lack adversary-informed context.

### Finding 4: Crisis and Incident Response is Structural

Mandiant launched dedicated Cyber Crisis Communication Planning and Response Services in 2022, recognizing that incident response requires specialized crisis communications, stakeholder messaging, and regulatory framework alignment. Google's Chrome Product Security team owns incident response as a distinct responsibility. The proposed /eng-team has no incident response capability -- there is no agent responsible for what happens when a vulnerability is discovered in production.

### Finding 5: DevSecOps Pipeline Engineering is a Distinct Role

Modern security engineering organizations consistently staff dedicated DevSecOps or "Security Tooling" engineers responsible for SAST/DAST tool integration, CI/CD pipeline security, secrets scanning, dependency analysis, and container security orchestration. The AppSec function guide from Matthias Rohr identifies this as a distinct organizational function: "implementing secure defaults, security policies, and guardrails for the dev teams, integrating security scanning tools." The proposed eng-infra agent touches on some of this, but CI/CD security pipeline design and security tooling integration is a full-time specialization in elite teams, not a subset of infrastructure engineering.

### Finding 6: Security Champions Programs Scale Embedded Security

Microsoft's Secure Future Initiative targets 5% employee participation in its Security Ambassador program. Google has a similar model where engineers dedicate "20% time" to security projects (as evidenced by Dillon Franke working with Project Zero as 20% time). GitLab's handbook documents the "Security Champion" role explicitly. The proposed /eng-team lacks a mechanism for embedding security awareness into non-security engineering roles -- there is no equivalent of the security champion or ambassador pattern.

### Finding 7: Compliance and Governance is a Distinct Function

NIST 800-53, SOC 2, ISO 27001, PCI DSS, and industry-specific regulations require dedicated compliance engineering effort that goes beyond "writing secure code." Compliance verification, audit support, evidence collection, and regulatory mapping are distinct from security engineering. The proposed /eng-team has no compliance or governance agent, meaning teams working in regulated environments would lack coverage for this critical function.

---

## L2: Detailed Analysis

### Organization-by-Organization Breakdown

#### Google Project Zero

| Attribute | Detail |
|-----------|--------|
| Team Size | Small, elite (estimated 10-20 researchers) |
| Focus | Zero-day vulnerability discovery across all major software |
| Key Roles | Vulnerability researchers, technical writers |
| Discovery Methods | Manual source code review (54.2%), fuzzing (37.2%), other (8.6%) |
| Notable Members | Ivan Fratric, Seth Jenkins, Dillon Franke (20% time) |
| Research Output | 2025: "Reporting Transparency" trial -- early public notification within one week of vulnerability reports |
| Organizational Model | Pure research team -- finds vulnerabilities, discloses to vendors |

**Relevance to /eng-team**: Project Zero represents the "offense informs defense" model. Their research methodology (manual code review + fuzzing) maps directly to eng-security + automated tooling. However, they are purely a research/discovery team -- they do not build production software. The /eng-team needs the equivalent of this capability embedded in the engineering workflow.

#### Google Chrome Security

| Sub-Team | Function | Staffing Pattern |
|-----------|----------|-----------------|
| Product Security | Vulnerability management, incident response, security updates, coordination/disclosure | Multiple security engineers (junior through senior), expanding to Mexico City |
| Fuzzing | Automated vulnerability discovery, MojoJS fuzzer, WebIDL fuzzer, browser fuzztests | 3 software engineers (junior through senior) in Mexico City |
| Security Architecture | Origin calculation security, process isolation, OOPIF security | Dedicated architecture team |

**Relevance to /eng-team**: Chrome Security demonstrates that "security engineering" is not one role but at least three distinct specializations. The Product Security team owns the vulnerability lifecycle -- something the proposed /eng-team does not have a dedicated agent for.

#### Microsoft Security Engineering

| Initiative | Detail |
|------------|--------|
| Secure Future Initiative (SFI) | Launched 2024, major restructuring of security governance |
| Deputy CISOs | 14 dCISOs embedded in engineering divisions, reporting to CISO and division heads |
| Durability Architects | Embedded in each division, champion "fix-once, fix-forever" mindset |
| Security Ambassador Program | Launching Fall 2025, targets 5% employee participation as grassroots security advocates |
| SDL Evolution | Continuous SDL (March 2024) -- security embedded in DevOps rather than phase gates |

**Relevance to /eng-team**: Microsoft's model shows that security at scale requires: (1) executive-level security embedding (Deputy CISOs), (2) architectural security champions (Durability Architects), and (3) grassroots peer-to-peer security culture (Ambassadors). The /eng-team's eng-reviewer role partially covers (2) but there is no equivalent of (1) or (3).

#### CrowdStrike Engineering

| Attribute | Detail |
|-----------|--------|
| Engineering Headcount | ~1,778 (30% of ~10,118 total employees) |
| Leadership | Elia Zaitsev (Global CTO), Patrick McCormack (VP Cloud Engineering) |
| Engineering Philosophy | Fluid roles, engineers solve customer problems end-to-end |
| Focus Areas | Data at scale, distributed systems, data science, AI, malware research |

**Relevance to /eng-team**: CrowdStrike's "fluid roles" model contrasts with rigid role definitions. Their engineers are expected to work across the stack. This suggests the /eng-team may benefit from an agent that coordinates cross-cutting concerns rather than having strictly siloed responsibilities.

#### Mandiant (Google Cloud)

| Team | Function |
|------|----------|
| Forensics | Deep forensic analysis of systems and incidents |
| Threat Intelligence | Identify threat actors, TTPs, IoCs |
| Malware Analysis | Analyze malicious code and techniques |
| Remediation | Address vulnerabilities, remove attacker access |
| Crisis Communications | Media inquiries, stakeholder messaging, regulatory alignment |

**Relevance to /eng-team**: Mandiant's model is the gold standard for "what happens after something goes wrong." The proposed /eng-team is entirely pre-incident -- it builds and reviews but has no agents for forensics, malware analysis, or incident remediation. While these are primarily defensive/responsive functions, elite engineering teams need incident response capability.

### Composite Role Matrix: Elite Teams vs. Proposed /eng-team

| Role/Function | Google (PZ/Chrome) | Microsoft (SFI/SDL) | CrowdStrike | Mandiant | Proposed /eng-team | Coverage |
|---------------|---------------------|---------------------|-------------|----------|-------------------|----------|
| Solution Architecture | Chrome Security Architecture | Durability Architects | -- | -- | eng-architect | COVERED |
| Technical Leadership | -- | Deputy CISOs | VP Engineering | Team Leads | eng-lead | COVERED |
| Backend Engineering | -- | SDL teams | Core engineering | -- | eng-backend | COVERED |
| Frontend Engineering | -- | SDL teams | Core engineering | -- | eng-frontend | COVERED |
| Infrastructure/IaC | -- | -- | Cloud engineering | -- | eng-infra | COVERED |
| QA/Testing | Chrome Fuzzing team | SDL verification | -- | -- | eng-qa | PARTIAL (see Finding 2) |
| Security Engineering | Product Security | SDL security | Security teams | -- | eng-security | PARTIAL (overloaded) |
| Code Review | -- | SDL peer review | -- | -- | eng-reviewer | COVERED |
| Threat Modeling | Chrome Security Architecture | SDL threat modeling | Threat intelligence | Threat Intelligence | eng-architect (partial) | PARTIAL |
| Fuzzing/Automation | Chrome Fuzzing (dedicated) | SDL tools | -- | -- | eng-qa (partial) | GAP (not dedicated) |
| Vulnerability Management | Product Security (dedicated) | MSRC (dedicated) | Falcon platform | Forensics + Intel | -- | GAP |
| Incident Response | Product Security | MSRC | IR teams | IR (core business) | -- | GAP |
| Threat Intelligence | Project Zero (research) | MSTIC | Falcon Intelligence | TI (core business) | -- | GAP |
| Compliance/Governance | -- | SDL compliance | -- | -- | -- | GAP |
| DevSecOps/Tooling | Chrome DevRel/Tools | SDL tooling | Platform engineering | -- | -- | GAP |
| Crisis Communications | -- | -- | -- | Crisis Comms (dedicated) | -- | GAP |
| Security Champions | 20% time model | Ambassadors (5% target) | Fluid roles | -- | -- | GAP |
| Supply Chain Security | -- | SFI supply chain | -- | -- | eng-infra (partial) | PARTIAL |
| Malware Analysis | Project Zero | -- | Malware research | Malware Analysis | -- | N/A (offensive) |

### AppSec Organizational Function Model

Based on Matthias Rohr's organizational AppSec guide and industry patterns, security engineering functions decompose into:

| Function | Description | /eng-team Coverage |
|----------|-------------|-------------------|
| Security Architecture | Architectural concepts, standards, blueprints, secure design reviews | eng-architect (COVERED) |
| Security Engineering | Threat modeling, security testing, code reviews, SAST/DAST | eng-security (COVERED but overloaded) |
| Security Tooling/DevSecOps | Tool integration, CI/CD security, scanning pipeline orchestration | NONE (GAP) |
| Security Champions/Liaisons | Embedded security advocates in dev teams, SPoC for security matters | NONE (GAP) |
| Vulnerability Management | Triage, prioritization, tracking, SLA enforcement for security findings | NONE (GAP) |
| Compliance Engineering | Regulatory mapping, evidence collection, audit support | NONE (GAP) |
| Incident Response | Detection, triage, containment, remediation, post-incident review | NONE (GAP) |

---

## Evidence and Citations

### Industry Leaders

| Source | Date | URL | Content |
|--------|------|-----|---------|
| Google Project Zero -- About | 2025 | [projectzero.google](https://projectzero.google/about-pz.html) | Team mission, discovery methodology (54.2% manual, 37.2% fuzzing) |
| Google Project Zero -- Working at P0 | 2025 | [projectzero.google](https://projectzero.google/working-at-project-zero.html) | Team composition, 20% time model |
| Google Project Zero -- Reporting Transparency | July 2025 | [projectzero.google](https://projectzero.google/) | New disclosure practices, early public notification |
| Google Chrome Security Q1 2025 | 2025 | [chromium.org](https://groups.google.com/a/chromium.org/g/security-dev/c/OL2skVyt8Wg) | Chrome Security team sub-teams: Product Security, Fuzzing, Architecture |
| Google Chrome Security Q3 2025 | 2025 | [chromium.org](https://groups.google.com/a/chromium.org/g/security-dev/c/s-UR_4pJvOY) | Team expansion, Mexico City hiring, role levels |
| Google Chrome Security Q4 2025 | 2025 | [chromium.org](https://www.chromium.org/Home/chromium-security/quarterly-updates/) | Ongoing team updates |
| Google SPA Research | 2025 | [research.google](https://research.google/teams/security-privacy-and-abuse/) | Security, Privacy and Abuse research team |
| Microsoft SDL Practices | 2025 | [microsoft.com](https://www.microsoft.com/en-us/securityengineering/sdl/practices) | SDL 5 phases: requirements, design, implementation, verification, release |
| Microsoft Evolving SDL | March 2024 | [microsoft.com](https://www.microsoft.com/en-us/security/blog/2024/03/07/evolving-microsoft-security-development-lifecycle-sdl-how-continuous-sdl-can-help-you-build-more-secure-software/) | Continuous SDL evolution |
| Microsoft SFI Progress Report | April 2025 | [microsoft.com](https://www.microsoft.com/en-us/security/blog/2025/04/21/securing-our-future-april-2025-progress-report-on-microsofts-secure-future-initiative/) | Deputy CISOs, Durability Architects, Ambassador program |
| Microsoft Deputy CISOs | April 2025 | [microsoft.com](https://www.microsoft.com/en-us/security/blog/2025/04/08/meet-the-deputy-cisos-who-help-shape-microsofts-approach-to-cybersecurity/) | 14 Deputy CISOs, reporting structure, embedded security model |
| Microsoft SFI Durability | June 2025 | [microsoft.com](https://www.microsoft.com/en-us/security/blog/2025/06/26/building-security-that-lasts-microsofts-journey-towards-durability-at-scale/) | Durability Architects, "fix-once, fix-forever" |
| Microsoft SFI Patterns | August 2025 | [microsoft.com](https://www.microsoft.com/en-us/security/blog/2025/08/06/sharing-practical-guidance-launching-microsoft-secure-future-initiative-sfi-patterns-and-practices/) | Practical SFI implementation guidance |
| Microsoft Security Culture | October 2025 | [microsoft.com](https://www.microsoft.com/en-us/security/blog/2025/10/13/building-a-lasting-security-culture-at-microsoft/) | Security Ambassador program, 5% participation target |
| CrowdStrike Engineering | 2025 | [crowdstrike.com](https://www.crowdstrike.com/en-us/careers/engineering-technology-team/) | 1,778 engineers, 30% of workforce, fluid roles |
| Mandiant IR Services | 2025 | [mandiant.com](https://www.mandiant.com/services/incident-response) | "Team of teams" model |
| Mandiant IR Best Practices | 2025 | [services.google.com](https://services.google.com/fh/files/misc/mandiant_incident_response_best_practices_2025.pdf) | IR best practices white paper |
| Google/Mandiant IDC Leader | 2025 | [cloud.google.com](https://cloud.google.com/blog/products/identity-security/google-named-a-leader-in-idc-marketscape-worldwide-incident-response-2025-vendor-assessment) | Named Leader in IDC MarketScape IR 2025 |

### Industry Experts

| Source | Date | URL | Content |
|--------|------|-----|---------|
| Matthias Rohr -- Organizational AppSec Functions | March 2024 | [matthiasrohr.de](https://matthiasrohr.de/2024/03/31/a-guide-to-organizational-appsec-functions/) | AppSec team composition, function decomposition |
| Adam Shostack -- Building AppSec Team | 2025 | [shostack.org](https://shostack.org/blog/application-security-team/) | AppSec team building strategies |
| Sygnia -- Building High-Performance IR Teams | 2025 | [sygnia.co](https://www.sygnia.co/blog/incident-response-team/) | IR team roles, responsibilities, structure |
| SecurityWeek -- Deputy CISOs | 2025 | [securityweek.com](https://www.securityweek.com/ciso-conversations-are-microsofts-deputy-cisos-a-signpost-to-the-future/) | Analysis of Deputy CISO model as industry trend |
| Cybersecurity Dive -- Microsoft Restructuring | 2025 | [cybersecuritydive.com](https://www.cybersecuritydive.com/news/microsoft-security-governance-cisos/715194/) | Microsoft security governance restructuring analysis |

### Industry Innovators

| Source | Date | URL | Content |
|--------|------|-----|---------|
| Wiz -- AppSec Engineers Guide | 2025 | [wiz.io](https://www.wiz.io/academy/application-security/appsec-engineers) | AppSec engineer responsibilities, career progression |
| Apiiro -- Security Champions + AppSec Engineers | 2025 | [apiiro.com](https://apiiro.com/blog/better-together-security-champions-and-application-security-engineers/) | Champion/engineer collaboration model |
| AppSecEngineer -- Security Champions Guide | 2025 | [appsecengineer.com](https://www.appsecengineer.com/enterprises/e-books/the-ultimate-guide-to-building-security-champions) | Comprehensive champion program guide |

### Community Leaders

| Source | Date | URL | Content |
|--------|------|-----|---------|
| NIST -- DevSecOps Practices | 2025 | [nccoe.nist.gov](https://www.nccoe.nist.gov/projects/secure-software-development-security-and-operations-devsecops-practices) | Federal DevSecOps guidance |
| NIST 800-53 | ongoing | (referenced in search results) | Compliance framework covering access control, IR, cryptography |
| CMU SEI -- DevSecOps Challenges | 2025 | [sei.cmu.edu](https://www.sei.cmu.edu/blog/5-challenges-to-implementing-devsecops-and-how-to-overcome-them/) | 5 implementation challenges including knowledge gaps |

### Community Experts

| Source | Date | URL | Content |
|--------|------|-----|---------|
| GitLab Handbook -- AppSec Engineer | 2025 | [handbook.gitlab.com](https://handbook.gitlab.com/job-families/security/application-security/) | GitLab's AppSec engineer role definition |
| HackerOne -- AppSec Engineer | 2025 | [hackerone.com](https://www.hackerone.com/knowledge-center/application-security-engineer) | AppSec career path, responsibilities |
| DestCert -- AppSec Career Path | 2025 | [destcert.com](https://destcert.com/career-guide/application-security-engineer-career-path/) | AppSec career progression |

### Community Innovators

| Source | Date | URL | Content |
|--------|------|-----|---------|
| Oligo -- DevSecOps 2025 | 2025 | [oligo.security](https://www.oligo.security/academy/devsecops-in-2025-principles-technologies-best-practices) | DevSecOps principles, technologies, practices |
| Checkmarx -- DevSecOps Best Practices | 2025 | [checkmarx.com](https://checkmarx.com/learn/developers/devsecops-best-practices/) | DevSecOps integration practices |

---

## Gap Analysis

### Critical Gaps (Present in 3+ elite organizations, absent from /eng-team)

| Gap | Severity | Evidence | Impact |
|-----|----------|----------|--------|
| **No Incident Response Agent** | HIGH | Mandiant IR (core business), Google Chrome Product Security (owns IR), Microsoft MSRC (dedicated IR) | The /eng-team can build and review but cannot respond when vulnerabilities are discovered in production. No agent owns vulnerability triage, containment, remediation coordination, or post-incident review. |
| **No Threat Intelligence Agent** | HIGH | Mandiant TI (core function), CrowdStrike Falcon Intelligence (core product), Google Project Zero (research-driven TI) | Defensive engineering decisions are made without adversary-informed context. The eng-architect cannot produce threat models informed by current threat landscape data without a threat intelligence function. |
| **No DevSecOps/Security Tooling Agent** | MEDIUM-HIGH | Google Chrome (Fuzzing team for automated tooling), Microsoft (SDL tooling), all AppSec guides identify tooling as distinct function | SAST/DAST integration, CI/CD security pipeline design, scanning orchestration, and security tooling selection are distinct from security engineering. eng-security is overloaded with both manual review and tooling responsibilities. |
| **No Compliance/Governance Agent** | MEDIUM | Microsoft (SDL compliance), NIST frameworks, all regulated industries require compliance engineering | Teams in regulated environments (healthcare, finance, government) have no agent for regulatory mapping, evidence collection, audit preparation, or compliance verification. |

### Moderate Gaps (Present in 1-2 elite organizations, relevant to /eng-team scope)

| Gap | Severity | Evidence | Impact |
|-----|----------|----------|--------|
| **eng-security is overloaded** | MEDIUM | Google Chrome splits into 3 sub-teams (Product Security, Fuzzing, Architecture); AppSec guides decompose into 5-7 distinct functions | One agent cannot credibly cover secure code review, SAST/DAST integration, vulnerability assessment, dependency auditing, AND security requirements verification. This is 3-4 roles in elite teams. |
| **No security-aware testing specialist** | MEDIUM | Google Chrome Fuzzing team is distinct from QA; security testing (fuzzing, property-based testing, chaos engineering) differs from functional testing | eng-qa covers functional testing; security-specific testing patterns (fuzzing, mutation testing, security regression) are distinct specializations. |
| **Weak supply chain security coverage** | LOW-MEDIUM | Microsoft SFI has dedicated supply chain focus; SBOM management, dependency verification, build pipeline integrity are growing concerns | eng-infra partially covers this, but software supply chain security (SBOM generation, provenance verification, dependency pinning, build reproducibility) is becoming a distinct specialization. |

### Structural Gaps (Pattern-level issues)

| Gap | Nature | Evidence |
|-----|--------|----------|
| **Sequential security review vs. embedded security** | The /eng-team workflow places eng-security at step 5 of 7, treating security as a late-stage review rather than an embedded practice. | Microsoft SFI embeds Deputy CISOs in divisions. Google has security in product teams. Industry trend is "shift left" -- security embedded from design through delivery, not as a gate. |
| **No cross-cutting security advocacy** | No mechanism for security knowledge sharing or culture building across non-security agents. | Microsoft Security Ambassador (5% participation), Google 20% time model, industry Security Champions programs all create distributed security awareness. |

---

## Recommendations

### Priority 1: Add Missing Agents (HIGH confidence)

| Proposed Agent | Role | Rationale |
|----------------|------|-----------|
| **eng-incident** | Incident Response Engineer | Owns vulnerability triage, containment coordination, remediation tracking, post-incident review, and communication. Every elite organization has dedicated IR capability. Fills the "what happens after deployment" gap. |
| **eng-devsecops** | DevSecOps Pipeline Engineer | Owns SAST/DAST pipeline integration, CI/CD security hardening, secrets scanning configuration, dependency analysis automation, container scanning, and security tooling selection. Unbundles the tooling responsibility from eng-security. |

### Priority 2: Add Conditional Agents (MEDIUM confidence -- strong evidence, may depend on scope decision)

| Proposed Agent | Role | Rationale |
|----------------|------|-----------|
| **eng-threatintel** | Threat Intelligence Analyst | Provides adversary-informed context for threat modeling, maps current CVEs and TTPs to architecture decisions, maintains threat landscape awareness. Strongly evidenced in Mandiant/CrowdStrike models. May overlap with /red-team's red-recon -- cross-skill integration opportunity. |
| **eng-compliance** | Compliance Engineer | Owns regulatory mapping, evidence collection, audit preparation, compliance verification against NIST/CIS/SOC2/PCI-DSS/HIPAA. Critical for teams in regulated industries. May be covered by configurable rule sets (R-011) rather than a dedicated agent. |

### Priority 3: Structural Adjustments (HIGH confidence)

| Adjustment | Description | Rationale |
|------------|-------------|-----------|
| **Restructure eng-security scope** | Narrow eng-security to manual secure code review, security requirements verification, and architecture security review. Move tooling responsibilities to eng-devsecops. | Google Chrome splits this into 3 teams. One agent covering all security functions is not credible. |
| **Embed security in workflow, not just review** | Modify the workflow so eng-security participates from step 1 (alongside eng-architect) rather than entering at step 5. | Microsoft SFI, Google, and all "shift-left" evidence shows security must be embedded from design, not bolted on at review. |
| **Add security testing scope to eng-qa** | Explicitly include fuzzing, property-based testing, and security regression testing in eng-qa's scope. Alternatively, create eng-sectest for dedicated security testing. | Google Chrome has a dedicated Fuzzing team. Security testing differs from functional testing in methodology and tooling. |

### Summary: Proposed /eng-team Roster Change

| Current (8 agents) | Proposed (10-12 agents) | Change |
|--------------------|------------------------|--------|
| eng-architect | eng-architect | No change |
| eng-lead | eng-lead | No change |
| eng-backend | eng-backend | No change |
| eng-frontend | eng-frontend | No change |
| eng-infra | eng-infra | No change |
| eng-qa | eng-qa | Expanded scope: add security testing |
| eng-security | eng-security | Narrowed scope: manual review + requirements |
| eng-reviewer | eng-reviewer | No change |
| -- | **eng-devsecops** (NEW) | DevSecOps pipeline, tooling, automation |
| -- | **eng-incident** (NEW) | Incident response, vulnerability management |
| -- | eng-threatintel (conditional NEW) | Threat intelligence for defensive context |
| -- | eng-compliance (conditional NEW) | Compliance engineering for regulated environments |

**Net assessment**: The proposed 8-agent roster covers the core "build and review" workflow but lacks post-deployment capability (incident response), automated security infrastructure (DevSecOps), and misses the industry-wide trend of decomposing "security engineering" into multiple specialized functions. Adding 2 agents (eng-devsecops, eng-incident) is strongly supported by evidence. Adding 2 more (eng-threatintel, eng-compliance) depends on whether cross-skill integration with /red-team and configurable rule sets (R-011) can cover those functions.
