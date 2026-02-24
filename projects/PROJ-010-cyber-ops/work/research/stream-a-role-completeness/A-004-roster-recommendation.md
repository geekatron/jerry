# A-004: Final Roster Recommendation with Gap Analysis

> Stream A: Role Completeness | PROJ-010 Cyber Ops | Phase 1 Research

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | 3-5 sentence synthesis for any stakeholder |
| [L1: Key Findings](#l1-key-findings) | Consolidated findings from A-001, A-002, A-003 |
| [L2: Detailed Analysis](#l2-detailed-analysis) | Final rosters, ATT&CK coverage proof, integration, decision matrix |
| [Recommendations](#recommendations) | Concrete numbered recommendations R-ROSTER-001 through R-ROSTER-014 |
| [Evidence and Citations](#evidence-and-citations) | All sources rolled up with categorization per R-006 |

---

## L0: Executive Summary

Synthesizing evidence from elite engineering team structures (A-001), red team and pentest firm patterns (A-002), and MITRE ATT&CK coverage analysis (A-003), this artifact delivers definitive roster decisions for both /eng-team and /red-team skills. The /eng-team roster grows from 8 to 10 agents with the addition of eng-devsecops and eng-incident, resolving the four critical gaps identified across Google, Microsoft, CrowdStrike, and Mandiant while keeping roster size manageable for skill routing. The /red-team roster grows from 9 to 11 agents with the addition of red-infra and red-social, closing the two zero-coverage MITRE ATT&CK tactics (Resource Development and Defense Evasion) and addressing the three universally-staffed roles missing from the original roster. Four conditional agents (eng-threatintel, eng-compliance, red-opsec, red-cloud) are deferred with specific triggers for reconsideration, avoiding roster bloat while preserving extension paths. The combined 21-agent roster achieves 14/14 ATT&CK tactic coverage, addresses all critical gaps flagged by 3+ elite organizations, and introduces 4 cross-skill purple team integration points where /eng-team and /red-team agents interact directly.

---

## L1: Key Findings

### Consolidated Finding 1: Security Engineering Decomposition is Universal

A-001 documented that Google Chrome Security operates three distinct sub-teams (Product Security, Fuzzing, Security Architecture), Microsoft's Secure Future Initiative embeds 14 Deputy CISOs with Durability Architects across divisions, and the AppSec organizational model decomposes into 5-7 distinct functions. The proposed eng-security agent collapses all of these into one role. This finding is reinforced by A-002's observation that offensive teams similarly decompose security testing across multiple specialists. The resolution is to narrow eng-security's scope to manual secure code review and security requirements verification, while spinning off automated tooling (SAST/DAST pipeline, CI/CD security) to a new eng-devsecops agent.

### Consolidated Finding 2: Post-Deployment Capability is Non-Negotiable

A-001 identified that Mandiant's "team of teams" model, Google Chrome's Product Security team, and Microsoft's MSRC all maintain dedicated incident response as a structural function -- not an ad-hoc activity. A-002 reinforced this from the offensive perspective: Netflix's Attack Emulation Team measures success by "control confidence, resilience, security awareness, and response readiness" -- metrics that require a defensive counterpart capable of incident response. The /eng-team has no agent for what happens after deployment. eng-incident fills this gap.

### Consolidated Finding 3: Red Team Tool Development is a Core Function, Not a Support Activity

A-002 found dedicated tool development in every major red team organization: TrustedSec's TRU research unit, SpecterOps' BloodHound team, Rapid7's Metasploit team, and GitLab's explicit "Red Team Developer" role. A-003 confirmed this independently: MITRE ATT&CK Resource Development (TA0042) -- the tactic covering infrastructure acquisition, capability development, and staging -- has zero agent coverage. The convergence from both organizational evidence (A-002) and framework coverage analysis (A-003) makes red-infra the highest-confidence addition across both rosters.

### Consolidated Finding 4: Social Engineering is a Pillar, Not a Technique

A-002 documented social engineering as a named role in EC Council's red team taxonomy, a dedicated service line at TrustedSec, and a core function in IBM's red team definition. A-003 found that ATT&CK Reconnaissance (TA0043) has partial coverage because social reconnaissance techniques (Phishing for Information T1598, Gather Victim Org Information T1591) fall outside red-recon's technical OSINT scope. The human attack vector requires distinct expertise in psychology, communications, and scenario design that cannot be absorbed by a technical exploitation agent. red-social fills this gap.

### Consolidated Finding 5: Defense Evasion Requires Distributed Ownership, Not a Dedicated Agent

A-003 identified Defense Evasion (TA0005) as the largest ATT&CK tactic (43 techniques, 112 sub-techniques) with zero primary coverage. A-003 presented two options: (a) distribute evasion competency across operational agents with red-infra as the tooling owner, or (b) create a dedicated red-evasion agent. A-002's organizational evidence resolves this: no elite organization studied staffs a dedicated "evasion specialist" -- instead, evasion is embedded in every operator's tradecraft, with infrastructure engineers handling tool-level evasion (obfuscation, packing, sandbox evasion). Option A -- distributed ownership with red-infra as evasion tooling owner -- aligns with industry practice.

### Consolidated Finding 6: OPSEC is Best Absorbed by red-infra and red-lead

A-002 recommended red-opsec as a conditional agent. A-003's analysis of Command and Control (TA0011) and Defense Evasion (TA0005) shows that OPSEC decomposes into two concerns: infrastructure OPSEC (C2 hardening, redirector configuration, domain management) and operational OPSEC (communication discipline, artifact cleanup, blue team deconfliction). The first belongs to red-infra; the second belongs to red-lead's expanded scope. A standalone red-opsec agent would create handoff overhead without adding a distinct knowledge domain. This resolves the A-002 conditional recommendation against a standalone agent.

### Consolidated Finding 7: Threat Intelligence Bridges Offense and Defense

A-001 identified threat intelligence as a critical gap for /eng-team (Mandiant, CrowdStrike, Google Project Zero all maintain dedicated TI). A-002 identified it as a moderate gap for /red-team (Netflix integrates TI natively, adversary emulation requires TI for TTP selection). Rather than adding dedicated TI agents to both rosters, the threat intelligence function is best served as a cross-skill integration point: /red-team's red-recon provides adversary-informed intelligence to /eng-team's eng-architect for threat modeling. This avoids duplicating a shared function across two skills.

### Consolidated Finding 8: Four Conditional Agents Have Clear Deferral Rationale

The three research artifacts collectively identified 4 conditional agents: eng-threatintel, eng-compliance, red-opsec, and red-cloud. Each has legitimate evidence but fails the decision criteria for immediate inclusion:
- **eng-threatintel**: Cross-skill integration with red-recon covers the primary use case (Finding 7).
- **eng-compliance**: Compliance engineering varies radically by regulatory environment; configurable rule sets (R-011) are a better fit than a static agent.
- **red-opsec**: Decomposes cleanly into red-infra + red-lead scope expansion (Finding 6).
- **red-cloud**: Explicitly out of scope per PLAN.md; cloud-specific offensive operations are a future extension.

---

## L2: Detailed Analysis

### Final /eng-team Roster

#### Roster Changes from Current 8-Agent Baseline

| Agent | Status | Scope Change | Evidence Source |
|-------|--------|-------------|----------------|
| eng-architect | RETAIN | Add explicit threat intelligence consumption from /red-team cross-skill integration | A-001 Finding 3 (Mandiant, CrowdStrike TI) |
| eng-lead | RETAIN | No change | A-001: covered by elite teams |
| eng-backend | RETAIN | No change | A-001: covered by elite teams |
| eng-frontend | RETAIN | No change | A-001: covered by elite teams |
| eng-infra | RETAIN | Add explicit supply chain security scope (SBOM generation, dependency provenance, build reproducibility) | A-001: Microsoft SFI supply chain focus, PARTIAL coverage |
| eng-qa | RETAIN | Add security testing scope: fuzzing, property-based testing, security regression testing | A-001 Finding 2 (Google Chrome Fuzzing team is distinct), A-001 moderate gap |
| eng-security | RETAIN (NARROWED) | Narrow to manual secure code review, security requirements verification, architecture security review. Remove SAST/DAST tooling and pipeline responsibilities | A-001 Finding 2 (Google splits into 3 sub-teams), A-001 Finding 5 (DevSecOps is distinct) |
| eng-reviewer | RETAIN | No change | A-001: covered by elite teams |
| **eng-devsecops** | **ADD** | SAST/DAST pipeline integration, CI/CD security hardening, secrets scanning, dependency analysis automation, container scanning, security tooling selection and orchestration | A-001 Finding 5, AppSec function model |
| **eng-incident** | **ADD** | Vulnerability triage, containment coordination, remediation tracking, post-incident review, communication templates, runbook development | A-001 Finding 4 (Mandiant, Google Chrome, Microsoft MSRC) |

#### Justification for Each Decision

**eng-devsecops (ADD)**: Three independent evidence streams converge on this addition. First, A-001 documents that Google Chrome maintains a dedicated Fuzzing team for automated security tooling, distinct from Product Security's manual review. Second, Microsoft's SDL evolution explicitly separates security tooling integration from security review. Third, Matthias Rohr's AppSec organizational model identifies "Security Tooling/DevSecOps" as a distinct function covering tool integration, CI/CD security, and scanning pipeline orchestration. The function eng-security currently carries (SAST/DAST integration, dependency analysis, container scanning) represents a full specialization in every elite organization studied. Splitting it off reduces eng-security's overloaded scope while giving automated security infrastructure a dedicated owner.

**eng-incident (ADD)**: A-001 documents dedicated incident response capability at Mandiant (core business -- "team of teams" model), Google Chrome Product Security (owns vulnerability lifecycle), and Microsoft MSRC (dedicated incident response). The absence of post-deployment capability means the /eng-team can build and review but has no agent for what happens when a vulnerability is discovered in production. Sygnia's research on building high-performance IR teams confirms this requires specialized skills in detection, triage, containment, remediation, and post-incident analysis. eng-incident closes the "what happens after deployment" gap.

**eng-threatintel (DEFER)**: While Mandiant (core function), CrowdStrike (core product), and Google Project Zero (research-driven TI) all maintain dedicated threat intelligence, the primary /eng-team use case for TI is informing threat models during architecture design. This is better served by cross-skill integration -- red-recon provides adversary context to eng-architect -- rather than duplicating TI capability in the engineering roster. Reconsideration trigger: if /eng-team operates independently of /red-team in deployments where no red team engagement is planned, a dedicated eng-threatintel becomes necessary.

**eng-compliance (DEFER)**: Microsoft SDL compliance and NIST frameworks demonstrate that compliance engineering is a real function, but compliance requirements vary radically by industry (healthcare: HIPAA, finance: PCI-DSS, government: FedRAMP, general: SOC 2). A static agent definition cannot cover this diversity credibly. R-011 (configurable rule sets) provides a better architecture: users supply their regulatory mapping, and eng-reviewer validates against user-provided standards. Reconsideration trigger: if three or more users request compliance-specific guidance that configurable rule sets cannot serve.

#### Final /eng-team Roster (10 agents)

| # | Agent | Role | Primary Responsibility |
|---|-------|------|----------------------|
| 1 | eng-architect | Solution Architect | System design, ADRs, threat modeling (STRIDE/DREAD), architecture review, threat intelligence consumption |
| 2 | eng-lead | Technical Lead | Implementation planning, code standards, PR review criteria, dependency decisions |
| 3 | eng-backend | Backend Engineer | Server-side implementation, secure coding (OWASP), input validation, auth, API security |
| 4 | eng-frontend | Frontend Engineer | Client-side implementation, XSS prevention, CSP, CORS, secure state management |
| 5 | eng-infra | Infrastructure Engineer | IaC, container security, network segmentation, secrets management, supply chain security (SBOM, provenance) |
| 6 | eng-qa | QA Engineer | Test strategy, security test cases, fuzzing, property-based testing, security regression, coverage enforcement |
| 7 | eng-security | Security Engineer | Manual secure code review, security requirements verification, architecture security review |
| 8 | eng-reviewer | Code Reviewer | Final review gate, architecture compliance, security standards, /adversary integration |
| 9 | eng-devsecops | DevSecOps Engineer | SAST/DAST pipeline, CI/CD security, secrets scanning, dependency analysis, container scanning, tooling selection |
| 10 | eng-incident | Incident Response Engineer | Vulnerability triage, containment, remediation tracking, post-incident review, runbooks |

---

### Final /red-team Roster

#### Roster Changes from Current 9-Agent Baseline

| Agent | Status | Scope Change | Evidence Source |
|-------|--------|-------------|----------------|
| red-lead | RETAIN (EXPANDED) | Add mid-engagement methodology adaptation, findings validation/QA, deconfliction management, post-engagement impact tracking, operational OPSEC enforcement | A-002 Finding 5 (CREST CCSAM), A-002 Finding 3 (OPSEC), A-002 structural gap |
| red-recon | RETAIN | Add explicit cross-skill integration point for providing TI to /eng-team | A-002: covered, A-003: PARTIAL due to social recon gap (addressed by red-social) |
| red-vuln | RETAIN | No change | A-002/A-003: strong coverage |
| red-exploit | RETAIN (EXPANDED) | Add explicit Impact (TA0040) demonstration scope -- safe simulation of destructive capabilities for risk communication; add execution-time Defense Evasion techniques (process injection, signed binary proxy execution) | A-003 Finding 6 (Impact ambiguous), A-003 Rec 2/4 |
| red-privesc | RETAIN | Add explicit credential-based Defense Evasion techniques (access token manipulation) | A-003 Rec 2 |
| red-lateral | RETAIN (NARROWED for C2) | Remove C2 infrastructure design (moved to red-infra); retain C2 usage during lateral movement operations; add network-level Defense Evasion techniques (traffic signaling, protocol tunneling) | A-003 Rec 3 (C2 separation), A-003 Rec 2 |
| red-persist | RETAIN | Add explicit persistence-phase Defense Evasion techniques (indicator removal, rootkits, timestomping) | A-003 Rec 2 |
| red-exfil | RETAIN | Add explicit exfiltration-phase Defense Evasion techniques (data encoding, encrypted channels) | A-003 Rec 2 |
| red-reporter | RETAIN (EXPANDED) | Add Impact risk documentation scope -- stakeholder communication of impact potential, remediation urgency scoring | A-003 Rec 4 |
| **red-infra** | **ADD** | C2 infrastructure design and management, redirector configuration, domain management, custom payload development, implant creation, infrastructure-as-code for engagement environments, tool-level Defense Evasion (obfuscation, packing, execution guardrails, sandbox evasion), OPSEC hardening of infrastructure, Resource Development (TA0042 -- all 7 techniques), Command and Control (TA0011 -- infrastructure design, protocol selection, encryption, resilience) | A-002 Finding 1, A-003 Finding 1, A-003 Finding 3, A-003 Rec 1/2/3 |
| **red-social** | **ADD** | Phishing campaign design and execution, pretexting scenario development, vishing methodology, credential harvesting via social channels, physical pretexting planning, social reconnaissance (T1591, T1597, T1598), social attack vector integration with technical exploitation | A-002 Finding 2, A-003 Finding 4 |

#### Justification for Each Decision

**red-infra (ADD)**: This is the highest-confidence addition across the entire project. Three independent evidence streams converge: (1) A-002 documents dedicated tool development at TrustedSec TRU, SpecterOps (BloodHound), Rapid7 (Metasploit), and GitLab (Red Team Developer role) -- 4 of 7 organizations studied staff this as a distinct role. (2) A-003 identifies Resource Development (TA0042) as a zero-coverage tactic with 7 techniques and 14 sub-techniques completely unowned. (3) A-003 identifies Command and Control (TA0011) as a weak-coverage tactic with only 2-3 of 16 techniques implicitly addressed by red-lateral. red-infra resolves all three gaps simultaneously by owning pre-operational infrastructure, tooling, C2 architecture, and tool-level Defense Evasion. This single agent addition closes two of the four ATT&CK coverage gaps.

**red-social (ADD)**: Two independent evidence streams support this addition. (1) A-002 documents social engineering as a named role in EC Council's taxonomy, a dedicated service at TrustedSec, and a core function in IBM's and ASIS International's red team definitions -- present in 4+ of 7 organizations studied. (2) A-003 finds that ATT&CK Reconnaissance social techniques (Phishing for Information T1598, Gather Victim Org Information T1591, Search Closed Sources T1597) have no coverage, contributing to the PARTIAL rating for TA0043. Social engineering requires distinct expertise (psychology, communications, scenario design) that cannot be credibly absorbed by red-exploit's technical exploitation focus. The human attack vector is one of three pillars of red teaming alongside technical and physical.

**red-opsec (DEFER -- absorbed into red-infra + red-lead)**: A-002 recommended OPSEC as a conditional agent. Analysis shows OPSEC decomposes into two distinct domains: (1) infrastructure OPSEC (C2 hardening, redirector segmentation, domain management, infrastructure resilience) which is structurally identical to red-infra's responsibilities, and (2) operational OPSEC (communication discipline, artifact cleanup, blue team deconfliction, operational discipline enforcement) which extends red-lead's engagement management scope. No elite organization studied staffs a dedicated OPSEC-only role; OPSEC is a competency distributed across infrastructure engineers and engagement leads. Adding a standalone agent would create handoff overhead without a distinct knowledge domain.

**red-cloud (DEFER)**: GIAC's GCPN certification, DataDog's Stratus Red Team tool, and CyCognito's 2026 research all indicate cloud-specific offensive operations are an emerging specialization. However, PLAN.md explicitly excludes "Cloud-specific provider tooling" as out of scope for the initial build. The current agents are infrastructure-agnostic, which provides flexibility. Reconsideration trigger: when PROJ-010 scopes a cloud extension phase or when three distinct engagement scenarios require cloud-native attack paths that generic agents cannot address.

#### Final /red-team Roster (11 agents)

| # | Agent | Role | Primary Responsibility |
|---|-------|------|----------------------|
| 1 | red-lead | Engagement Lead | Scope, RoE, methodology, team coordination, authorization, findings QA, methodology adaptation, operational OPSEC, post-engagement impact tracking |
| 2 | red-recon | Reconnaissance | OSINT, network enumeration, service discovery, technology fingerprinting, attack surface mapping, cross-skill TI to /eng-team |
| 3 | red-vuln | Vulnerability Analyst | Vulnerability identification, CVE research, exploit availability, attack path analysis, CVSS scoring |
| 4 | red-exploit | Exploitation Specialist | Exploit development, payload crafting, vulnerability chaining, PoC development, safe Impact demonstration (TA0040), execution-time evasion |
| 5 | red-privesc | Privilege Escalation | Local/domain privesc, credential harvesting, token manipulation, misconfig exploitation, credential-based evasion |
| 6 | red-lateral | Lateral Movement | Pivoting, tunneling, living-off-the-land, internal exploitation, C2 usage during operations, network-level evasion |
| 7 | red-persist | Persistence Specialist | Backdoor placement, scheduled tasks, service manipulation, rootkit methodology, persistence-phase evasion (indicator removal, timestomping) |
| 8 | red-exfil | Data Exfiltration | Data identification, exfiltration channels, covert communication, DLP bypass, exfiltration-phase evasion |
| 9 | red-reporter | Engagement Reporter | Finding documentation, risk scoring, remediation recommendations, executive summaries, Impact risk documentation |
| 10 | red-infra | Infrastructure and Tool Engineer | C2 design and management, redirectors, domains, custom payloads, implants, IaC for engagements, tool-level evasion (obfuscation, packing, sandbox evasion), infrastructure OPSEC, Resource Development (TA0042), C2 architecture (TA0011) |
| 11 | red-social | Social Engineering Specialist | Phishing campaigns, pretexting, vishing, credential harvesting via social channels, social recon (T1591/T1597/T1598), social attack vector integration |

---

### MITRE ATT&CK Coverage After Changes

The following table proves that the recommended 11-agent /red-team roster achieves full tactic coverage across all 14 MITRE ATT&CK Enterprise tactics.

| # | Tactic ID | Tactic Name | Technique Count | Primary Agent | Supporting Agents | Coverage Before | Coverage After | Change Reason |
|---|-----------|-------------|-----------------|---------------|-------------------|-----------------|----------------|---------------|
| 1 | TA0043 | Reconnaissance | 10 techniques, 30+ sub-techniques | red-recon | red-social (social recon: T1591, T1597, T1598), red-vuln (tech fingerprinting) | PARTIAL | **STRONG** | red-social covers social reconnaissance gap |
| 2 | TA0042 | Resource Development | 7 techniques, 14 sub-techniques | **red-infra** | -- | ZERO | **STRONG** | red-infra owns all 7 techniques: Acquire Infrastructure (T1583), Compromise Accounts (T1586), Develop Capabilities (T1587), Obtain Capabilities (T1588), Stage Capabilities (T1608), Compromise Infrastructure (T1584), Establish Accounts (T1585) |
| 3 | TA0001 | Initial Access | 9 techniques, 12 sub-techniques | red-exploit | red-recon (targeting), red-vuln (vuln ID), red-social (phishing -- T1566) | STRONG | **STRONG** | red-social adds phishing initial access vector |
| 4 | TA0002 | Execution | 14 techniques, 19 sub-techniques | red-exploit | red-privesc (execution context), red-lateral (remote execution) | STRONG | **STRONG** | No change needed |
| 5 | TA0003 | Persistence | 19 techniques, 79 sub-techniques | red-persist | red-privesc (elevated persistence) | STRONG | **STRONG** | No change needed |
| 6 | TA0004 | Privilege Escalation | 13 techniques, 37 sub-techniques | red-privesc | red-exploit (exploit dev support) | STRONG | **STRONG** | No change needed |
| 7 | TA0005 | Defense Evasion | 43 techniques, 112 sub-techniques | **Distributed** (red-infra as tooling owner) | red-infra: obfuscation, packing, execution guardrails, sandbox evasion; red-exploit: process injection, signed binary proxy; red-privesc: access token manipulation; red-persist: indicator removal, rootkits, timestomping; red-lateral: traffic signaling, protocol tunneling; red-exfil: data encoding, encrypted channels | ZERO | **STRONG** | Distributed ownership per A-003 Option A; red-infra owns tool-level evasion, each operational agent owns phase-specific evasion techniques |
| 8 | TA0006 | Credential Access | 17 techniques, 47 sub-techniques | red-privesc | red-lateral (credential use), red-social (social credential harvesting) | STRONG | **STRONG** | red-social adds social credential harvesting |
| 9 | TA0007 | Discovery | 32 techniques, 11 sub-techniques | red-recon | red-lateral (internal discovery), red-privesc (privilege discovery) | STRONG | **STRONG** | No change needed |
| 10 | TA0008 | Lateral Movement | 9 techniques, 12 sub-techniques | red-lateral | red-exploit (exploitation support), red-privesc (credential use) | STRONG | **STRONG** | No change needed |
| 11 | TA0009 | Collection | 17 techniques, 18 sub-techniques | red-exfil | red-recon (target identification), red-lateral (access to sources) | STRONG | **STRONG** | No change needed |
| 12 | TA0011 | Command and Control | 16 techniques, 27 sub-techniques | **red-infra** (architecture, design, protocol selection, encryption, resilience) | red-lateral (C2 usage during movement), red-persist (C2 for persistent comms), red-exfil (C2 for exfil) | WEAK | **STRONG** | C2 infrastructure design moved from red-lateral (secondary) to red-infra (primary); operational agents consume C2 but red-infra builds and maintains it |
| 13 | TA0010 | Exfiltration | 9 techniques, 7 sub-techniques | red-exfil | red-lateral (channel setup) | STRONG | **STRONG** | No change needed |
| 14 | TA0040 | Impact | 14 techniques, 9 sub-techniques | **red-exploit** (technical demonstration) | red-reporter (risk documentation and stakeholder communication) | WEAK | **STRONG** | red-exploit explicitly owns safe impact demonstration; red-reporter owns impact risk documentation for stakeholders |

#### Coverage Summary

| Rating | Before (A-003) | After (A-004) | Delta |
|--------|----------------|---------------|-------|
| STRONG | 8/14 (57%) | 14/14 (100%) | +6 tactics |
| PARTIAL | 2/14 (14%) | 0/14 (0%) | -2 (upgraded) |
| WEAK | 2/14 (14%) | 0/14 (0%) | -2 (upgraded) |
| ZERO | 2/14 (14%) | 0/14 (0%) | -2 (upgraded) |

The addition of 2 agents (red-infra, red-social) plus structural scope adjustments to 5 existing agents (red-lead, red-exploit, red-persist, red-lateral, red-exfil) achieves full 14/14 tactic coverage.

---

### Cross-Skill Integration Points

Where /eng-team and /red-team agents interact directly for purple team collaboration.

| # | Integration Point | /eng-team Agent(s) | /red-team Agent(s) | Interaction Mode | Value |
|---|-------------------|--------------------|--------------------|-----------------|-------|
| 1 | **Threat-Informed Architecture** | eng-architect (consumes TI for threat models) | red-recon (provides adversary TTPs, threat landscape data) | Collaborative: red-recon feeds current threat actor TTPs into eng-architect's STRIDE/DREAD threat models | Architecture decisions informed by real adversary behavior rather than theoretical threats. Replaces the need for a dedicated eng-threatintel agent. |
| 2 | **Attack Surface Validation** | eng-infra (defines infrastructure), eng-devsecops (defines security tooling) | red-recon (maps attack surface), red-vuln (identifies vulnerabilities) | Adversarial: red-recon and red-vuln test the attack surface that eng-infra and eng-devsecops defined and hardened | Validates that infrastructure hardening and security tooling actually reduce the attack surface as intended. |
| 3 | **Secure Code vs. Exploitation** | eng-security (secure code review), eng-backend/eng-frontend (implementation) | red-exploit (exploitation), red-privesc (privilege escalation) | Adversarial: red-exploit and red-privesc attempt to exploit code that eng-security reviewed and eng-backend/eng-frontend built | Proves whether secure coding practices withstand real exploitation techniques. Feedback loop drives hardening. |
| 4 | **Incident Response Validation** | eng-incident (IR procedures, runbooks) | red-persist (persistence), red-lateral (lateral movement), red-exfil (exfiltration) | Adversarial: red team executes post-exploitation chain while eng-incident attempts detection, containment, and remediation | Validates IR runbooks against real adversary post-exploitation behavior. Netflix model: "increased control confidence, resilience, security awareness, and response readiness." |

These four integration points operationalize the PLAN.md requirement that "The two skills work as adversaries: /eng-team builds, /red-team breaks. The gap between them is where the hardening happens." Netflix's Attack Emulation Team model (A-002) validates that this adversarial-collaborative dynamic is how elite organizations measure and improve security posture.

---

### Decision Matrix

For each proposed new agent, the following matrix documents evidence strength, organizational prevalence, ATT&CK impact, and risk of omission.

#### Agents Added to Final Roster

| Agent | Evidence Strength | Elite Orgs with Equivalent | ATT&CK Tactic Impact | Risk if Omitted |
|-------|------------------|---------------------------|----------------------|-----------------|
| **eng-devsecops** | HIGH | 3 of 4: Google Chrome (Fuzzing team for automated tooling), Microsoft (SDL tooling), AppSec organizational model (distinct function). CrowdStrike (implied via "platform engineering"). | N/A (defensive skill) | eng-security remains overloaded with 3-4 roles worth of responsibilities. Automated security tooling (SAST/DAST pipelines, scanning orchestration) has no dedicated owner. Elite teams universally separate manual review from automated tooling. |
| **eng-incident** | HIGH | 3 of 4: Mandiant (core business -- IR "team of teams"), Google Chrome Product Security (owns vulnerability lifecycle), Microsoft MSRC (dedicated IR). CrowdStrike (IR as service). | N/A (defensive skill) | /eng-team has zero post-deployment capability. No agent for vulnerability triage, containment, remediation coordination, or post-incident review. The team can build and review but cannot respond. |
| **red-infra** | HIGH | 4 of 7: TrustedSec TRU (dedicated research unit), SpecterOps (BloodHound team), Rapid7 (Metasploit team), GitLab (Red Team Developer role). Microsoft and Netflix also maintain custom tooling. | Closes 2 gaps: Resource Development (TA0042 -- ZERO to STRONG), Command and Control (TA0011 -- WEAK to STRONG). Major contributor to Defense Evasion (TA0005 -- ZERO to STRONG via tool-level evasion). | 3 ATT&CK tactics remain uncovered or weak. Operators have no infrastructure support for C2, domains, redirectors, custom payloads. Every elite red team organization staffs this function. |
| **red-social** | HIGH | 4 of 7: EC Council (named role), TrustedSec (dedicated service), IBM (core red team function), ASIS International (social + physical). Netflix (workforce education). | Closes Reconnaissance gap: TA0043 PARTIAL to STRONG (social recon techniques T1591, T1597, T1598). Strengthens Initial Access via phishing (T1566). Strengthens Credential Access via social harvesting. | The human attack vector -- consistently identified as one of three red team pillars (technical, social, physical) -- has zero coverage. Phishing is the most common real-world initial access vector. |

#### Agents Deferred (Not in Final Roster)

| Agent | Evidence Strength | Elite Orgs with Equivalent | ATT&CK Tactic Impact | Deferral Rationale | Reconsideration Trigger |
|-------|------------------|---------------------------|----------------------|-------------------|------------------------|
| **eng-threatintel** | MEDIUM | 3 of 4: Mandiant TI (core function), CrowdStrike Falcon Intelligence (core product), Google Project Zero (research-driven TI). | N/A (defensive skill) | Cross-skill integration (red-recon to eng-architect) covers primary use case without duplicating a function across two skills. | /eng-team deployed independently of /red-team where no red team engagement informs architecture. |
| **eng-compliance** | MEDIUM | 1 of 4: Microsoft SDL compliance. NIST/CIS/SOC2 are frameworks, not organizational roles observed in studied teams. | N/A (defensive skill) | Compliance requirements vary radically by industry (HIPAA, PCI-DSS, FedRAMP, SOC 2). Configurable rule sets (R-011) provide better architecture than a static agent. | 3+ users request compliance-specific guidance that configurable rule sets cannot serve. |
| **red-opsec** | MEDIUM | 0 dedicated: No studied organization staffs a standalone OPSEC-only role. OPSEC is embedded in infrastructure engineers and engagement leads. | Indirect contributor to Defense Evasion (TA0005). | Decomposes cleanly: infrastructure OPSEC to red-infra, operational OPSEC to red-lead. Standalone agent creates handoff overhead without distinct knowledge domain. | Future engagement complexity reveals OPSEC coordination failures between red-infra and red-lead. |
| **red-cloud** | MEDIUM | Emerging: GIAC GCPN (certification), DataDog Stratus (tool), CyCognito (trends). 0 of 7 studied organizations staff a dedicated cloud-only red team role -- cloud is embedded in existing operator expertise. | Would add depth to multiple tactics for cloud-specific technique variants. | Explicitly out of scope per PLAN.md. Current agents are infrastructure-agnostic. | PROJ-010 cloud extension phase scoped, or 3 engagement scenarios require cloud-native attack paths. |

---

## Recommendations

### Roster Composition

| ID | Recommendation | Priority | Rationale |
|----|---------------|----------|-----------|
| R-ROSTER-001 | Add eng-devsecops to /eng-team roster. Scope: SAST/DAST pipeline integration, CI/CD security hardening, secrets scanning, dependency analysis automation, container scanning, security tooling selection. | HIGH | 3/4 elite organizations separate automated security tooling from manual review (A-001 Finding 5). Unbundles eng-security's overloaded scope. |
| R-ROSTER-002 | Add eng-incident to /eng-team roster. Scope: vulnerability triage, containment coordination, remediation tracking, post-incident review, communication templates, runbook development. | HIGH | 3/4 elite organizations maintain dedicated IR (A-001 Finding 4). /eng-team currently has zero post-deployment capability. |
| R-ROSTER-003 | Add red-infra to /red-team roster. Scope: C2 infrastructure, redirectors, domains, custom payloads, implants, IaC for engagements, tool-level Defense Evasion, infrastructure OPSEC, full TA0042 ownership, TA0011 architecture. | HIGH | 4/7 organizations staff dedicated tool development (A-002 Finding 1). Closes 2 zero-coverage ATT&CK tactics and 1 weak-coverage tactic (A-003 Findings 1, 2, 3). Highest-confidence addition across both rosters. |
| R-ROSTER-004 | Add red-social to /red-team roster. Scope: phishing campaigns, pretexting, vishing, credential harvesting via social channels, social reconnaissance (T1591/T1597/T1598), social attack vector integration. | HIGH | 4/7 organizations include social engineering as distinct function (A-002 Finding 2). Closes TA0043 partial coverage (A-003 Finding 4). Human attack vector is one of three red team pillars. |
| R-ROSTER-005 | Defer eng-threatintel. Cover via cross-skill integration: red-recon provides adversary TI to eng-architect for threat modeling. | MEDIUM | Cross-skill integration avoids function duplication. Reconsider if /eng-team deploys independently. |
| R-ROSTER-006 | Defer eng-compliance. Cover via configurable rule sets (R-011) for regulatory mapping. | MEDIUM | Compliance varies radically by industry. Static agent cannot credibly cover HIPAA + PCI-DSS + FedRAMP + SOC 2. |
| R-ROSTER-007 | Defer red-opsec. Absorb into red-infra (infrastructure OPSEC) and red-lead (operational OPSEC). | MEDIUM | No studied organization staffs a standalone OPSEC-only role. Decomposes cleanly into existing agents. |
| R-ROSTER-008 | Defer red-cloud. Currently out of scope per PLAN.md. | LOW | Explicitly excluded. Cloud-specific offensive operations are a future extension. |

### Scope Modifications to Existing Agents

| ID | Recommendation | Priority | Rationale |
|----|---------------|----------|-----------|
| R-ROSTER-009 | Narrow eng-security scope to manual secure code review, security requirements verification, and architecture security review. Remove SAST/DAST tooling responsibilities (moved to eng-devsecops). | HIGH | Google Chrome splits security into 3 sub-teams (A-001 Finding 2). One agent covering all security functions is not credible at elite team quality. |
| R-ROSTER-010 | Expand red-lead scope to include mid-engagement methodology adaptation, findings validation/QA, deconfliction management, post-engagement impact tracking, and operational OPSEC enforcement. | HIGH | CREST CCSAM certification validates lifecycle management as distinct from initial scope definition (A-002 Finding 5). TrustedSec lead is hands-on-keyboard AND client interface. Absorbs operational OPSEC from deferred red-opsec. |
| R-ROSTER-011 | Assign Impact (TA0040) as shared responsibility: red-exploit owns technical impact demonstration (safe simulation), red-reporter owns impact risk documentation and stakeholder communication. | MEDIUM | A-003 Finding 6 identified 14 Impact techniques with zero explicit coverage. Split matches the natural boundary between technical capability (red-exploit) and communication (red-reporter). |
| R-ROSTER-012 | Distribute Defense Evasion (TA0005) across all operational agents per A-003 Option A. red-infra owns tool-level evasion; each operational agent owns phase-specific evasion techniques. | HIGH | A-003 identifies TA0005 as the largest tactic (43 techniques, 112 sub-techniques) with zero coverage. Distributed ownership aligns with industry practice where evasion is embedded tradecraft, not a standalone function. |

### Structural Recommendations

| ID | Recommendation | Priority | Rationale |
|----|---------------|----------|-----------|
| R-ROSTER-013 | Establish four cross-skill integration points between /eng-team and /red-team: (1) Threat-Informed Architecture, (2) Attack Surface Validation, (3) Secure Code vs. Exploitation, (4) Incident Response Validation. Define integration protocols during Phase 2 Architecture. | HIGH | Netflix Attack Emulation Team model demonstrates that adversarial-collaborative integration is how elite organizations improve security posture (A-002 Finding 7). PLAN.md requires "the two skills work as adversaries." |
| R-ROSTER-014 | Design /red-team workflow to support non-linear kill chain iteration. Agents must be invocable in any order, with explicit support for cycling between phases (e.g., exploitation discovers new recon targets, triggering return to red-recon). | MEDIUM | A-002 structural gap: "Kill-chain-based decomposition may be too rigid." Real engagements are iterative. TrustedSec operators span the full chain. Kill chain organizes capability, not workflow sequence. |

---

## Evidence and Citations

All citations are rolled up from A-001, A-002, and A-003 with categorization per R-006. Sources that informed multiple findings are listed once with all relevant artifact references.

### Industry Leaders

| Source | Date | Content | Used In |
|--------|------|---------|---------|
| MITRE ATT&CK Enterprise Matrix | 2025 | Authoritative source for 14 tactics, 203 techniques, 453 sub-techniques | A-003 (all findings) |
| MITRE ATT&CK Adversary Emulation Plans | 2025 | Official adversary emulation resources | A-002, A-003 |
| Google Project Zero -- About, Working at P0, Reporting Transparency | 2025 | Team mission, methodology (54.2% manual, 37.2% fuzzing), 20% time model | A-001 (Findings 1, 2, 6) |
| Google Chrome Security Q1/Q3/Q4 2025 | 2025 | Sub-teams: Product Security, Fuzzing, Architecture; team expansion | A-001 (Finding 2) |
| Google SPA Research | 2025 | Security, Privacy and Abuse research team | A-001 |
| Google AI Red Team | 2025 | Google's AI red team approach | A-002 |
| Microsoft SDL Practices and Continuous SDL | 2024-2025 | SDL 5 phases, continuous SDL evolution | A-001 (Findings 1, 5) |
| Microsoft SFI Progress Report, Deputy CISOs, Durability, Patterns, Security Culture | 2025 | 14 Deputy CISOs, Durability Architects, Ambassador program (5% target) | A-001 (Findings 1, 6, 7) |
| Microsoft AI Red Team and 100 AI Products Report | 2025 | AI red team structure and scale | A-002 |
| CrowdStrike Engineering | 2025 | 1,778 engineers, 30% of workforce, fluid roles | A-001 (Finding 1) |
| Mandiant IR Services, Best Practices, IDC Leader | 2025 | "Team of teams" model, IR best practices | A-001 (Findings 3, 4) |
| Netflix Attack Emulation Team | 2025 | Blends offensive, defensive, TI; measures control confidence and resilience | A-002 (Findings 5, 7) |

### Industry Experts

| Source | Date | Content | Used In |
|--------|------|---------|---------|
| SANS SEC565 Red Team Operations | 2025 | OPSEC, C2, adversary emulation methodology | A-002 (Finding 3), A-003 (Finding 3) |
| GIAC Offensive Certifications (GCPN, GAWN) | 2025 | Cloud pentest, wireless, offensive cert landscape | A-002 (Findings 4, 6) |
| CREST Certifications (CPSA, CRT, CCT, CCSAM, CCSAS) | 2025-2026 | Full hierarchy, CCSAM engagement management, CCSAS specialization | A-002 (Finding 5) |
| EC Council Red Team Careers | 2025 | Red team roles: leader, pentester, social engineer, specialists | A-002 (Finding 2) |
| CISA MITRE ATT&CK Mapping Best Practices | 2023 | Official US government ATT&CK mapping guidance | A-002, A-003 |
| Matthias Rohr -- Organizational AppSec Functions | March 2024 | AppSec team composition, function decomposition | A-001 (Finding 5) |
| Adam Shostack -- Building AppSec Team | 2025 | AppSec team building strategies | A-001 |
| Sygnia -- Building High-Performance IR Teams | 2025 | IR team roles, responsibilities, structure | A-001 (Finding 4) |
| SecurityWeek, Cybersecurity Dive -- Microsoft Deputy CISOs Analysis | 2025 | Deputy CISO model as industry trend | A-001 (Finding 1) |
| Picus Security -- MITRE ATT&CK Framework Guide | 2025 | Comprehensive ATT&CK guide with coverage analysis | A-003 |
| CyberDefenders -- MITRE ATT&CK for SOC and DFIR | 2025 | Field guide for investigations and alert mapping | A-003 |

### Industry Innovators

| Source | Date | Content | Used In |
|--------|------|---------|---------|
| SpecterOps -- Services, RTO Training | 2025 | Pentest, Red Team, Purple Team, tool development DNA (BloodHound) | A-002 (Finding 1) |
| TrustedSec -- Putting the Team in Red Team, Services, Engagement Guide | 2025 | Engagement lead model, TRU research unit, staffing philosophy | A-002 (Findings 1, 2, 5) |
| Rapid7 -- Pentest Services, Metasploit Pro | 2025 | Team backgrounds, methodology (PTES, OWASP), Metasploit framework | A-002 (Finding 1) |
| Bishop Fox -- Red Teaming, 2025 Tools Guide | 2025 | C2 frameworks, AD tools, network exploitation | A-002, A-003 |
| CyCognito -- Red Teaming 2026 | 2026 | Cloud specialization, bleeding edge trends | A-002 (Finding 4) |
| Outflank -- OPSEC-Focused C2 | 2025 | OPSEC-focused C2 purpose-built for red teams | A-002 (Finding 3), A-003 |
| Wiz -- AppSec Engineers Guide, MITRE ATT&CK Guide | 2025 | AppSec responsibilities, ATT&CK tactics overview | A-001, A-003 |
| Apiiro -- Security Champions + AppSec Engineers | 2025 | Champion/engineer collaboration model | A-001 (Finding 6) |
| DataDog -- Stratus Red Team | 2025 | Cloud-focused adversary emulation with ATT&CK mapping | A-002 (Finding 4), A-003 |

### Community Leaders

| Source | Date | Content | Used In |
|--------|------|---------|---------|
| NIST DevSecOps Practices, NIST 800-53 | 2025 | Federal DevSecOps guidance, compliance framework | A-001 (Finding 7) |
| CMU SEI -- DevSecOps Challenges | 2025 | Implementation challenges including knowledge gaps | A-001 (Finding 5) |
| CrowdStrike -- MITRE ATT&CK Framework | 2025 | Framework overview, red team usage | A-003 |
| Proofpoint -- Red Team Definition | 2025 | Industry-standard red team definition | A-002 |
| Cobalt Strike / Outflank -- Red Team Bundle | 2025 | Professional red team tooling ecosystem | A-002 |

### Community Experts

| Source | Date | Content | Used In |
|--------|------|---------|---------|
| GitLab Handbook -- Red Team Roles | Oct 2025 | Full career ladder: Engineer through Manager, Red Team Developer role | A-002 (Findings 1, 7) |
| GitLab Handbook -- AppSec Engineer | 2025 | GitLab's AppSec engineer role definition | A-001 |
| IBM -- What is Red Teaming | 2025 | Red team definition: technical + social + physical | A-002 (Finding 2) |
| ASIS International -- Red Team Guide | Dec 2024 | Physical security testing, organizational red teaming | A-002 (Findings 2, 6) |
| Compass Security, Security Blue Team, Infosec Institute -- Red Team Career Guides | 2025 | Red team operator career paths and skills | A-002 |
| HackerOne, DestCert -- AppSec Career Paths | 2025 | AppSec career progression | A-001 |
| MITRE ATT&CK Blog -- Getting Started with Red Teaming | 2025 | ATT&CK-based red team methodology | A-002, A-003 |
| AppSecEngineer -- Security Champions Guide | 2025 | Comprehensive champion program guide | A-001 (Finding 6) |

### Community Innovators

| Source | Date | Content | Used In |
|--------|------|---------|---------|
| Parrot CTFs -- Red Team Infrastructure Guide | 2025 | Infrastructure setup, C2, redirectors, OPSEC | A-002 (Finding 3), A-003 |
| Medium (Azefox, Faris Faisal, Karthikeyan) -- Red Team Operations and C2 | 2025 | Red team operations introduction, C2 infrastructure | A-002 |
| Oligo, Checkmarx -- DevSecOps 2025 | 2025 | DevSecOps principles, technologies, practices | A-001 (Finding 5) |
