# B-002: PTES and OSSTMM Methodology Analysis

> Stream B: Methodology Standards | PROJ-010 Cyber Ops | Phase 1 Research

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | High-level comparison of PTES and OSSTMM |
| [L1: Key Findings](#l1-key-findings) | Structured findings on methodology fit |
| [L2: Detailed Analysis](#l2-detailed-analysis) | Deep phase-by-phase analysis of both frameworks |
| [Agent Mapping](#agent-mapping) | How each methodology maps to /red-team agents |
| [Evidence and Citations](#evidence-and-citations) | Categorized, dated sources |
| [Recommendations](#recommendations) | Default methodology selections for /red-team |

---

## L0: Executive Summary

PTES (Penetration Testing Execution Standard) and OSSTMM (Open Source Security Testing Methodology Manual) are the two principal open penetration testing methodologies. PTES defines a 7-phase engagement lifecycle from Pre-engagement through Reporting, directly mirroring the /red-team agent workflow. OSSTMM (version 3, maintained by ISECOM) takes a broader operational security approach, covering 5 channels (Human, Physical, Wireless, Telecommunications, Data Networks) with quantitative security metrics via its Risk Assessment Values (RAV). For the /red-team skill, PTES provides the best structural fit as the primary engagement workflow framework -- its phases map 1:1 to agent responsibilities. OSSTMM provides complementary depth for methodology rigor, particularly its quantitative measurement approach and its coverage of non-technical security channels that PTES treats less formally. The recommended approach is PTES as the primary workflow backbone with OSSTMM's RAV scoring and channel coverage integrated as supplementary methodology.

---

## L1: Key Findings

### Finding 1: PTES Phases Map Directly to /red-team Agent Workflow

The 7 PTES phases (Pre-engagement, Intelligence Gathering, Threat Modeling, Vulnerability Analysis, Exploitation, Post-Exploitation, Reporting) correspond almost exactly to the /red-team agent sequence defined in PLAN.md. This is not coincidental -- PLAN.md's methodology was likely influenced by PTES's well-established structure.

### Finding 2: OSSTMM Provides Quantitative Rigor PTES Lacks

OSSTMM's Risk Assessment Values (RAV) provide a quantitative security measurement methodology. Where PTES is qualitative ("we found these vulnerabilities"), OSSTMM enables quantitative statements ("the attack surface has a RAV score of X, with Y operational controls and Z data controls"). This quantitative approach is valuable for red-reporter's engagement scoring.

### Finding 3: OSSTMM's 5-Channel Model Expands Scope Beyond Network Testing

OSSTMM tests across Human Security, Physical Security, Wireless Communications, Telecommunications, and Data Networks. Most penetration tests focus primarily on Data Networks. The /red-team skill should support multi-channel engagements for comprehensive assessments, even if Data Networks remains the default.

### Finding 4: PTES Has Superior Technical Guidelines

PTES provides detailed technical guidelines for each phase, including specific tool recommendations, technique descriptions, and output expectations. The PTES Technical Guidelines document is essentially a practitioner's reference manual. OSSTMM is more methodological and less technically prescriptive.

### Finding 5: Neither Methodology Alone Is Sufficient for an Agentic Red Team

PTES provides workflow structure but lacks quantitative measurement. OSSTMM provides measurement rigor but lacks the detailed engagement workflow. An agentic red team benefits from combining PTES's workflow with OSSTMM's measurement, overlaid with ATT&CK's technique taxonomy (B-001).

---

## L2: Detailed Analysis

### PTES: The 7 Phases

#### Phase 1: Pre-engagement Interactions

| Aspect | Detail |
|--------|--------|
| **Purpose** | Establish scope, objectives, rules of engagement, and authorization before testing begins |
| **Key Activities** | Scope definition (IP ranges, domains, applications); Rules of engagement (testing windows, escalation procedures, emergency contacts); Authorization documentation (signed agreements, legal review); Communication plan (status updates, finding severity thresholds) |
| **Outputs** | Signed statement of work, rules of engagement document, scope definition, emergency contact list |
| **Agent Mapping** | **red-lead** -- This phase is entirely red-lead's responsibility. Authorization verification (R-020) maps directly here. |

#### Phase 2: Intelligence Gathering

| Aspect | Detail |
|--------|--------|
| **Purpose** | Gather maximum information about the target to identify entry points and attack surface |
| **Key Activities** | **Passive Recon:** OSINT, DNS enumeration, WHOIS, public records, social media, job postings, leaked credentials, search engine dorking; **Active Recon:** Port scanning, service enumeration, technology fingerprinting, web crawling, email harvesting; **Organizational Recon:** Employee identification, org chart mapping, technology stack identification, supplier/partner relationships |
| **Outputs** | Target profile document, network maps, service inventory, technology stack analysis, identified personnel, potential entry points |
| **Agent Mapping** | **red-recon** -- Full ownership. Maps to ATT&CK TA0043 Reconnaissance. |

#### Phase 3: Threat Modeling

| Aspect | Detail |
|--------|--------|
| **Purpose** | Analyze gathered intelligence to identify most likely and most impactful attack paths |
| **Key Activities** | Asset identification and valuation; Threat actor profiling (what adversary are we emulating?); Attack tree construction; Attack path prioritization by likelihood and impact; Business logic analysis for application testing |
| **Outputs** | Threat model document, prioritized attack paths, attack trees, asset inventory with risk ratings |
| **Agent Mapping** | **red-vuln** (threat-to-vulnerability correlation) + **red-lead** (strategic threat modeling and attack path prioritization) |

#### Phase 4: Vulnerability Analysis

| Aspect | Detail |
|--------|--------|
| **Purpose** | Identify specific vulnerabilities that can be exploited along prioritized attack paths |
| **Key Activities** | Automated vulnerability scanning (network, web application, infrastructure); Manual vulnerability identification; CVE research and exploit availability assessment; Vulnerability validation (distinguishing true positives from false positives); Attack path refinement based on confirmed vulnerabilities; CVSS scoring and risk prioritization |
| **Outputs** | Validated vulnerability inventory, CVSS scores, exploit availability assessment, refined attack paths |
| **Agent Mapping** | **red-vuln** -- Full ownership. This is red-vuln's core responsibility. |

#### Phase 5: Exploitation

| Aspect | Detail |
|--------|--------|
| **Purpose** | Actively exploit validated vulnerabilities to prove they are real and demonstrate business impact |
| **Key Activities** | Exploit selection/development/customization; Payload crafting for specific targets; Vulnerability chaining (combining multiple vulns for greater impact); Evasion technique application; Proof-of-concept development; Initial foothold establishment; Categories: network exploitation, web application exploitation, API exploitation, social engineering exploitation, wireless exploitation, physical exploitation |
| **Outputs** | Proof-of-concept exploits, access evidence (screenshots, session captures), exploitation timeline |
| **Agent Mapping** | **red-exploit** -- Primary owner. May coordinate with red-privesc for chained exploitation. |

#### Phase 6: Post-Exploitation

| Aspect | Detail |
|--------|--------|
| **Purpose** | Demonstrate full business impact by escalating privileges, moving laterally, and demonstrating data compromise |
| **Key Activities** | **Privilege Escalation:** Local privesc (kernel exploits, misconfigs, SUID/sudo abuse), domain privesc (Kerberoasting, DCSync, GPO abuse); **Credential Harvesting:** Memory dumping, SAM/NTDS extraction, keylogging, token theft; **Lateral Movement:** Pivoting, pass-the-hash/ticket, remote execution, internal scanning; **Persistence:** Backdoor placement, scheduled tasks, service creation (if in scope); **Data Exfiltration:** Data identification, staging, exfiltration channel testing; **Pillaging:** Sensitive data identification, configuration file harvesting, intellectual property identification |
| **Outputs** | Privilege escalation evidence, lateral movement maps, data compromise evidence, persistence mechanism documentation |
| **Agent Mapping** | **red-privesc** (privilege escalation, credential harvesting), **red-lateral** (lateral movement, pivoting), **red-persist** (persistence), **red-exfil** (data identification and exfiltration) |

#### Phase 7: Reporting

| Aspect | Detail |
|--------|--------|
| **Purpose** | Document all findings with remediation guidance for both technical and executive audiences |
| **Key Activities** | **Executive Summary:** Business risk overview, key findings, strategic recommendations for leadership; **Technical Report:** Detailed vulnerability descriptions, exploitation evidence, step-by-step reproduction instructions, CVSS scores; **Remediation Plan:** Prioritized remediation steps, short-term mitigations, long-term hardening recommendations; **Appendices:** Raw scan data, tool output, screenshots, timeline of activities |
| **Outputs** | Executive summary, technical report, remediation plan, appendices, ATT&CK Navigator layer |
| **Agent Mapping** | **red-reporter** -- Full ownership. All other agents feed findings to red-reporter throughout the engagement. |

### OSSTMM: The 5 Channels and Test Types

#### Channel Overview

| Channel | Scope | Test Focus |
|---------|-------|------------|
| **Human Security** | Personnel, social engineering, policy adherence | Phishing, pretexting, tailgating, insider threat simulation, awareness testing |
| **Physical Security** | Buildings, data centers, hardware, physical infrastructure | Physical access controls, surveillance, locks, alarm systems, dumpster diving, badge cloning |
| **Wireless Communications** | Wi-Fi, Bluetooth, RFID, NFC, other wireless protocols | Wireless network security, rogue access points, protocol vulnerabilities, signal interception |
| **Telecommunications** | Phone systems, VoIP, PBX, fax, analog/digital comms | PBX exploitation, voicemail hacking, caller ID spoofing, VoIP security, war dialing |
| **Data Networks** | TCP/IP networks, internet-facing and internal systems | Network penetration testing, web application testing, API testing, infrastructure testing |

#### OSSTMM Test Types

OSSTMM defines 6 test types that determine the tester's and target's knowledge:

| Test Type | Tester Knowledge | Target Knowledge | Equivalent Term |
|-----------|-----------------|------------------|-----------------|
| **Blind** | No prior knowledge of target | Target is aware of testing | Black-box with notification |
| **Double Blind** | No prior knowledge of target | Target is NOT aware of testing | True black-box / red team |
| **Gray Box** | Partial knowledge of target | Target is aware of testing | Gray-box with notification |
| **Double Gray Box** | Partial knowledge of target | Target has partial knowledge of test scope | Gray-box / partial notification |
| **Tandem** | Full knowledge of target | Full cooperation with target | White-box / crystal-box |
| **Reversal** | Full knowledge of target | Target is NOT aware of testing | White-box red team |

#### OSSTMM Risk Assessment Values (RAV)

OSSTMM's quantitative approach uses the RAV formula to produce a numerical security score:

| Component | Description |
|-----------|-------------|
| **Operational Security** | Controls that actively protect against threats |
| **Loss Controls** | Mechanisms that limit damage after a breach |
| **Limitations** | Weaknesses, vulnerabilities, and exposures |
| **Porosity** | Points of access or interaction |
| **Attack Surface** | Total measurable exposure |

**RAV Calculation:** RAV = (Operational Controls + Loss Controls) / (Limitations + Porosity)
- RAV > 1.0 = Controls exceed exposure (generally secure)
- RAV < 1.0 = Exposure exceeds controls (vulnerable)
- RAV = 1.0 = Controls match exposure (balanced)

### PTES vs. OSSTMM Comparative Analysis

| Dimension | PTES | OSSTMM |
|-----------|------|--------|
| **Primary Focus** | Penetration testing methodology | Operational security testing methodology |
| **Scope** | Network and application testing | All 5 security channels (human, physical, wireless, telecom, data) |
| **Structure** | 7 sequential phases | 5 parallel channels with 6 test types |
| **Measurement** | Qualitative (findings + CVSS) | Quantitative (RAV scoring) |
| **Technical Depth** | Deep -- includes technical guidelines | Moderate -- methodology-focused, less prescriptive |
| **Reporting** | Executive + Technical dual-report model | RAV scorecard with operational metrics |
| **Maturity** | Established 2009, widely adopted | Version 3 (ISECOM), academic and enterprise adoption |
| **Workflow Fit** | Sequential phases map to agent workflow | Channel-based structure requires adaptation |
| **Strengths** | Clear practitioner workflow, detailed technical guidance, industry standard | Quantitative measurement, multi-channel coverage, test type taxonomy |
| **Weaknesses** | No quantitative security scoring, primarily technical channel focus | Less detailed technical guidance, complex RAV calculation, less industry adoption for pure pentesting |
| **Best For** | Standard penetration testing engagements | Comprehensive operational security audits |

### Methodology Combination for Agentic Red Team

The optimal approach for /red-team is a layered methodology:

| Layer | Source | Purpose |
|-------|--------|---------|
| **Workflow Structure** | PTES 7 phases | Agent sequencing and engagement lifecycle |
| **Technique Taxonomy** | MITRE ATT&CK (B-001) | Technique classification, reporting, coverage tracking |
| **Channel Coverage** | OSSTMM 5 channels | Multi-channel scope definition and coverage assurance |
| **Test Type Classification** | OSSTMM 6 test types | Engagement type taxonomy (blind, gray box, etc.) |
| **Quantitative Measurement** | OSSTMM RAV | Engagement outcome scoring and trend tracking |
| **Technical Guidance** | PTES Technical Guidelines | Practitioner-level technique execution guidance |

---

## Agent Mapping

### PTES Phase to /red-team Agent Mapping

| PTES Phase | /red-team Agent | Agent Role in Phase |
|------------|-----------------|---------------------|
| 1. Pre-engagement | **red-lead** | Scope definition, authorization verification, rules of engagement, methodology selection |
| 2. Intelligence Gathering | **red-recon** | OSINT, active scanning, technology fingerprinting, attack surface mapping |
| 3. Threat Modeling | **red-vuln** + **red-lead** | Attack path analysis (red-vuln), strategic threat modeling (red-lead) |
| 4. Vulnerability Analysis | **red-vuln** | Vulnerability identification, CVE research, CVSS scoring, exploit availability |
| 5. Exploitation | **red-exploit** | Exploit development, payload crafting, initial access, proof-of-concept |
| 6. Post-Exploitation | **red-privesc**, **red-lateral**, **red-persist**, **red-exfil** | Privilege escalation, lateral movement, persistence, data exfiltration |
| 7. Reporting | **red-reporter** | Finding documentation, risk scoring, remediation guidance, executive summary |

### OSSTMM Channel to /red-team Agent Mapping

| OSSTMM Channel | Primary Agent | Secondary Agents |
|----------------|---------------|------------------|
| Human Security | **red-recon** (social engineering recon) | red-exploit (social engineering execution) |
| Physical Security | **red-recon** (physical recon) | red-exploit (physical access exploitation) |
| Wireless Communications | **red-recon** (wireless recon) | red-exploit (wireless exploitation), red-vuln (wireless vuln analysis) |
| Telecommunications | **red-recon** (telecom recon) | red-exploit (telecom exploitation) |
| Data Networks | **All agents** | Full engagement workflow across all agents |

### Methodology Selection by Engagement Type

red-lead should select methodology based on engagement type:

| Engagement Type | Primary Methodology | Supplementary | Test Type (OSSTMM) |
|-----------------|--------------------|--------------|--------------------|
| Standard penetration test | PTES | ATT&CK technique mapping | Blind or Gray Box |
| Red team assessment | PTES + ATT&CK (threat emulation) | OSSTMM RAV scoring | Double Blind or Reversal |
| Comprehensive security audit | OSSTMM (all channels) | PTES for data network phase | Tandem |
| Web application test | PTES (phases 2-7) | OWASP Testing Guide, ATT&CK | Blind or Tandem |
| Social engineering assessment | OSSTMM Human Security | PTES Intelligence Gathering | Blind or Double Blind |
| Physical security assessment | OSSTMM Physical Security | PTES Pre-engagement | Blind or Double Blind |

---

## Evidence and Citations

### Industry Leaders

| Source | Date | Content |
|--------|------|---------|
| [PTES -- Penetration Testing Execution Standard](http://www.pentest-standard.org/index.php/Main_Page) | 2009-present | Official PTES standard and methodology |
| [PTES Technical Guidelines](http://www.pentest-standard.org/index.php/PTES_Technical_Guidelines) | 2009-present | Detailed technical guidelines for each PTES phase |
| [ISECOM -- OSSTMM 3](https://www.isecom.org/OSSTMM.3.pdf) | 2010 (v3) | Official Open Source Security Testing Methodology Manual |
| [ISECOM Research](https://www.isecom.org/research.html) | 2025 | ISECOM's research and methodology updates |

### Industry Experts

| Source | Date | Content |
|--------|------|---------|
| [Sprocket Security -- 5 Pentesting Standards to Know in 2025](https://www.sprocketsecurity.com/blog/pentesting-standards-2025) | 2025 | Comparative analysis of current penetration testing standards |
| [DeepStrike -- Penetration Testing Methodology 2025](https://deepstrike.io/blog/penetration-testing-methodology) | 2025 | Modern penetration testing methodology guide |
| [VikingCloud -- What is PTES?](https://www.vikingcloud.com/blog/what-is-penetration-testing-execution-standard) | 2025 | PTES overview and phase analysis |

### Industry Innovators

| Source | Date | Content |
|--------|------|---------|
| [OWASP -- Penetration Testing Methodologies](https://owasp.org/www-project-web-security-testing-guide/v41/3-The_OWASP_Testing_Framework/1-Penetration_Testing_Methodologies) | 2021 (v4.1) | OWASP comparison of penetration testing methodologies |
| [Datami -- 7 PTES Stages](https://datami.ee/blog/penetration-testing-execution-standard-7-ptes-stages/) | 2024 | Detailed breakdown of each PTES stage |

### Community Experts

| Source | Date | Content |
|--------|------|---------|
| [ResilientX -- OSSTMM Comprehensive Overview](https://www.resilientx.com/blog/osstmm-open-source-security-testing-methodology-manual-a-comprehensive-overview) | 2024 | Detailed OSSTMM analysis including channels and test types |
| [KirkpatrickPrice -- What You Need to Know About OSSTMM](https://kirkpatrickprice.com/blog/what-you-need-to-know-about-osstmm/) | 2024 | OSSTMM overview with practical application guidance |
| [GeeksforGeeks -- PTES](https://www.geeksforgeeks.org/software-engineering/penetration-testing-execution-standard-ptes/) | 2024 | PTES educational reference |

### Community Innovators

| Source | Date | Content |
|--------|------|---------|
| [Qualysec -- What is PTES?](https://qualysec.com/penetration-testing-execution-standard/) | 2024 | PTES analysis with modern application context |
| [Medium / Tahir -- OSSTMM Overview](https://medium.com/@tahirbalarabe2/overview-of-isecoms-open-source-security-testing-methodology-manual-osstmm-6c2ada15436b) | 2024 | OSSTMM practical overview |

---

## Recommendations

### R1: PTES as Primary Engagement Workflow

PTES SHOULD be the primary workflow structure for /red-team engagements. Its 7-phase model maps directly to the agent workflow defined in PLAN.md. red-lead should use PTES as the default methodology selection, with the option to switch to OSSTMM for specific engagement types (comprehensive audits, physical/wireless assessments).

### R2: OSSTMM Test Type Taxonomy for Engagement Classification

OSSTMM's 6 test types SHOULD be adopted as the standard engagement classification taxonomy. When red-lead defines an engagement, the test type (Blind, Double Blind, Gray Box, Double Gray Box, Tandem, Reversal) should be specified and drive agent behavior (e.g., Double Blind engagements restrict red-recon from using insider information).

### R3: OSSTMM RAV Scoring for Quantitative Reporting

red-reporter SHOULD incorporate OSSTMM's RAV scoring methodology (or a simplified derivative) to provide quantitative security measurements alongside qualitative findings. This enables:
- Trend tracking across multiple engagements
- Objective comparison of security posture before/after remediation
- Executive-friendly single-number security scores

### R4: Multi-Channel Scope Support

The /red-team skill SHOULD support OSSTMM's 5-channel scope model. While Data Networks will be the default channel, red-lead should be able to define engagements across Human, Physical, Wireless, and Telecommunications channels. Agent behavior should adapt based on active channels.

### R5: Configurable Methodology Selection (R-011 Compliance)

Per R-011 (Configurable Rule Sets), the /red-team skill MUST allow users to override the default PTES methodology with organization-specific engagement frameworks. This should be implemented as a methodology configuration layer that red-lead consults when defining engagement workflow.

### R6: PTES Technical Guidelines as Agent Knowledge Base Source

PTES Technical Guidelines SHOULD be a primary source for agent-level technical knowledge bases. Each /red-team agent's knowledge of techniques, tools, and outputs should reference PTES Technical Guidelines for its corresponding phase.
