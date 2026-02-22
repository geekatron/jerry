# FEAT-041: /eng-team vs /red-team Gap Analysis Report

> **SSOT:** ADR-PROJ010-001 (Agent Team Architecture), ADR-PROJ010-006 (Authorization & Scope Control)
> **Framework:** MITRE ATT&CK Enterprise v15 (14 tactics, 203 techniques, 453 sub-techniques)
> **Scope:** /eng-team (10 agents) vs /red-team (11 agents) coverage analysis
> **Parent:** EPIC-005 Purple Team Validation
> **Created:** 2026-02-22
> **Classification:** C4 Critical Deliverable (quality threshold >= 0.95)

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0 Executive Summary](#l0-executive-summary) | Stakeholder-facing coverage findings and risk posture |
| [Methodology](#methodology) | Analysis approach, data sources, mapping criteria |
| [ATT&CK Coverage Matrix](#attck-coverage-matrix) | 14-tactic offense/defense coverage table |
| [Gap Inventory](#gap-inventory) | All identified gaps with severity classification |
| [Defensive Coverage Analysis](#defensive-coverage-analysis) | /eng-team capability-to-ATT&CK mapping |
| [Offensive Coverage Analysis](#offensive-coverage-analysis) | /red-team agent-to-ATT&CK mapping |
| [Coverage Statistics](#coverage-statistics) | Quantitative coverage metrics |
| [Remediation Recommendations](#remediation-recommendations) | Prioritized actions per gap |
| [L2 Strategic Implications](#l2-strategic-implications) | Long-term architectural and organizational impact |
| [References](#references) | Source document traceability |

---

## L0 Executive Summary

The /eng-team and /red-team skills achieve **STRONG** coverage across 10 of 14 MITRE ATT&CK Enterprise tactics and **PARTIAL** coverage across the remaining 4. No tactic has zero coverage on both sides. However, the analysis identified **27 discrete gaps** distributed across both offensive and defensive domains.

**Key Findings:**

1. **Two critical gaps** exist where offensive capability has no corresponding defensive countermeasure: TA0005 Defense Evasion (distributed across 6 red-team agents with no dedicated eng-team detection capability) and TA0011 Command and Control (red-infra covers 6 C2 techniques with no eng-team C2 detection agent).

2. **Four high-severity gaps** exist where defensive coverage is present but untested by red-team: OWASP A04 Insecure Design has no corresponding offensive validation; SLSA supply chain integrity has no adversarial supply chain test agent; eng-frontend CSP/CORS hardening has no corresponding red-team browser exploitation capability; and eng-devsecops CI/CD security gates have no pipeline attack simulation.

3. **The /eng-team maps to SDLC frameworks (NIST SSDF, OWASP ASVS, CIS Benchmarks) rather than ATT&CK.** This creates a structural impedance mismatch: eng-team agents think in terms of secure development practices, while red-team agents think in terms of adversary tactics. The purple team framework (FEAT-040) addresses this through integration points, but technique-level defensive mapping to ATT&CK is incomplete.

4. **Overall bidirectional coverage rate: 71%** (10 of 14 tactics have both offensive and defensive coverage at the tactic level). At the technique level, bidirectional coverage drops to approximately **58%** when considering specific sub-technique pairings.

**Risk Posture:** MODERATE. The framework has strong foundational coverage for the attack lifecycle from reconnaissance through exfiltration. Critical gaps concentrate in detection engineering (defense evasion, C2 detection) and validation coverage (untested defenses), both of which are addressable through targeted agent enhancements and purple team integration point activation.

---

## Methodology

### Analysis Approach

This gap analysis follows a five-step methodology:

1. **Extract Red Team ATT&CK Coverage.** Enumerate every ATT&CK tactic and technique explicitly claimed by each of the 11 /red-team agents from their agent definition files and the SKILL.md defense evasion ownership table.

2. **Extract Eng Team Defensive Coverage.** Map each of the 10 /eng-team agent capabilities to the ATT&CK tactics they defend against, translating SDLC framework references (OWASP, NIST SSDF, CIS, SANS) to corresponding ATT&CK technique coverage.

3. **Build 14-Row Coverage Matrix.** For each of the 14 ATT&CK Enterprise tactics, document which red-team agents provide offensive coverage and which eng-team agents provide defensive coverage.

4. **Identify Gaps.** Classify gaps into four categories:
   - **GAP-DEFENSE**: Offensive capability exists with no corresponding defensive countermeasure
   - **GAP-OFFENSE**: Defensive capability exists with no corresponding offensive test
   - **PARTIAL**: Some techniques within a tactic are covered but others are missing
   - **NO_COVERAGE**: Neither side addresses the tactic (none found in this analysis)

5. **Classify Severity.** Apply severity ratings based on:
   - **Critical**: Entire tactic uncovered on one side, or fundamental detection gap
   - **High**: Key techniques within a tactic missing, or primary defense untested
   - **Medium**: Secondary techniques missing within otherwise covered tactics
   - **Low**: Edge-case gaps or techniques with minimal real-world exploitation frequency

### Data Sources

| Source | Content | Location |
|--------|---------|----------|
| /red-team SKILL.md | Agent roster, ATT&CK mappings, defense evasion table, integration points | `skills/red-team/SKILL.md` |
| /eng-team SKILL.md | Agent roster, 8-step workflow, SDLC governance layers | `skills/eng-team/SKILL.md` |
| Red-team agent files (11) | Per-agent ATT&CK technique references, methodology, authorization constraints | `skills/red-team/agents/red-*.md` |
| Eng-team agent files (10) | Per-agent capabilities, OWASP/NIST/CIS mappings, SSDF practice references | `skills/eng-team/agents/eng-*.md` |
| ADR-PROJ010-001 | Agent team architecture, 21-agent roster, handoff protocols | `projects/PROJ-010-cyber-ops/decisions/ADR-PROJ010-001-agent-team-architecture.md` |
| ADR-PROJ010-006 | Three-layer authorization architecture, scope enforcement | `projects/PROJ-010-cyber-ops/decisions/ADR-PROJ010-006-authorization-scope-control.md` |
| Purple Team Framework (FEAT-040) | Integration points IP-1 through IP-4, finding flow, engagement protocol | `projects/PROJ-010-cyber-ops/work/EPIC-005-purple-team-validation/FEAT-040-purple-team-framework/purple-team-integration-framework.md` |
| A-003 ATT&CK Coverage Research | Phase 1 baseline coverage analysis, improvement recommendations | `projects/PROJ-010-cyber-ops/work/research/stream-a-role-completeness/A-003-mitre-attack-coverage.md` |

### Mapping Criteria

The /eng-team does not use ATT&CK natively. Defensive coverage was mapped by translating each eng-team agent's framework references to the ATT&CK techniques those frameworks mitigate:

| Defensive Framework | ATT&CK Mapping Rationale |
|---------------------|--------------------------|
| OWASP Top 10 (A01-A10) | Maps to TA0001 Initial Access (web exploitation), TA0002 Execution (injection), TA0004 Privilege Escalation (broken access control) |
| OWASP ASVS 5.0 | Maps to TA0006 Credential Access (authentication chapters), TA0001 (session management), TA0009 Collection (data protection chapters) |
| NIST SSDF (PO/PS/PW/RV) | Maps broadly to TA0042 Resource Development (PS practices), TA0001-TA0002 (PW practices), post-deployment response (RV practices) |
| CIS Benchmarks | Maps to TA0003 Persistence (OS hardening), TA0004 Privilege Escalation (privilege restrictions), TA0007 Discovery (service hardening) |
| NIST SP 800-61 (IR) | Maps to TA0040 Impact (response), and detection across TA0003/TA0005/TA0008/TA0010 |
| SLSA Build Levels | Maps to TA0042 Resource Development (supply chain integrity) |
| STRIDE/DREAD/PASTA Threat Modeling | Maps broadly to all TA categories through threat identification |

---

## ATT&CK Coverage Matrix

The following matrix maps all 14 MITRE ATT&CK Enterprise tactics to their offensive (/red-team) and defensive (/eng-team) coverage, identifying the responsible agents and coverage level.

### Coverage Legend

| Symbol | Meaning |
|--------|---------|
| STRONG | Multiple agents, explicit technique references, comprehensive methodology |
| MODERATE | One or more agents with partial technique coverage |
| WEAK | Indirect coverage through adjacent capabilities; no explicit technique ownership |
| NONE | No agent addresses this tactic |

### Matrix

| # | ATT&CK Tactic | ID | Red Team Agent(s) | Red Coverage | Eng Team Agent(s) | Eng Coverage | Bidirectional |
|---|---------------|-----|-------------------|--------------|-------------------|--------------|---------------|
| 1 | Reconnaissance | TA0043 | red-recon, red-social | STRONG | eng-architect (threat modeling), eng-infra (attack surface reduction) | MODERATE | Yes |
| 2 | Resource Development | TA0042 | red-infra | STRONG | eng-infra (SLSA, SBOM), eng-devsecops (supply chain scanning) | MODERATE | Yes |
| 3 | Initial Access | TA0001 | red-exploit, red-social | STRONG | eng-backend (OWASP Top 10), eng-frontend (XSS/CORS), eng-devsecops (DAST) | STRONG | Yes |
| 4 | Execution | TA0002 | red-exploit | STRONG | eng-backend (input validation, injection prevention), eng-devsecops (SAST), eng-security (code review) | STRONG | Yes |
| 5 | Persistence | TA0003 | red-persist (RoE-gated) | STRONG | eng-infra (CIS hardening, OS config), eng-incident (monitoring, detection) | MODERATE | Yes |
| 6 | Privilege Escalation | TA0004 | red-privesc | STRONG | eng-backend (RBAC/ABAC, least privilege), eng-infra (CIS hardening), eng-security (ASVS verification) | STRONG | Yes |
| 7 | Defense Evasion | TA0005 | red-infra, red-exploit, red-privesc, red-lateral, red-persist, red-exfil (distributed) | STRONG | eng-devsecops (scanning), eng-incident (monitoring) | WEAK | Partial |
| 8 | Credential Access | TA0006 | red-privesc | STRONG | eng-backend (auth implementation), eng-security (ASVS auth chapters), eng-devsecops (secrets scanning) | STRONG | Yes |
| 9 | Discovery | TA0007 | red-lateral | STRONG | eng-infra (network segmentation, service hardening), eng-incident (anomaly detection) | MODERATE | Yes |
| 10 | Lateral Movement | TA0008 | red-lateral | STRONG | eng-infra (network segmentation, microsegmentation), eng-incident (monitoring, containment) | MODERATE | Yes |
| 11 | Collection | TA0009 | red-exfil (RoE-gated) | STRONG | eng-backend (data access controls), eng-security (data flow tracing), eng-incident (DLP monitoring) | MODERATE | Yes |
| 12 | Exfiltration | TA0010 | red-exfil (RoE-gated) | STRONG | eng-incident (DLP, monitoring), eng-infra (network egress controls) | WEAK | Partial |
| 13 | Command and Control | TA0011 | red-infra | STRONG | eng-incident (monitoring), eng-infra (network controls) | WEAK | Partial |
| 14 | Impact | TA0040 | red-exploit (demo only), red-reporter (documentation) | MODERATE | eng-incident (IR runbooks, containment, recovery) | STRONG | Yes |

### Coverage Summary by Tactic

| Coverage Level | Count | Tactics |
|----------------|-------|---------|
| Both STRONG | 4 | TA0001 Initial Access, TA0002 Execution, TA0004 Privilege Escalation, TA0006 Credential Access |
| Bidirectional (mixed strength) | 7 | TA0043, TA0042, TA0003, TA0007, TA0008, TA0009, TA0040 |
| Partial (one side WEAK) | 3 | TA0005 Defense Evasion, TA0010 Exfiltration, TA0011 Command and Control |
| No Coverage | 0 | None |

---

## Gap Inventory

### Gap Classification Summary

| Severity | Count | Description |
|----------|-------|-------------|
| Critical | 2 | Entire defensive capability missing for a major offensive tactic |
| High | 4 | Key techniques or primary defenses missing or untested |
| Medium | 12 | Secondary techniques missing within otherwise covered tactics |
| Low | 9 | Edge-case gaps with minimal real-world exploitation frequency |
| **Total** | **27** | |

### Critical Gaps

#### GAP-C01: Defense Evasion Detection Gap (TA0005)

| Attribute | Detail |
|-----------|--------|
| **Gap Type** | GAP-DEFENSE |
| **Severity** | Critical |
| **Tactic** | TA0005 Defense Evasion |
| **Offensive Coverage** | 6 agents with distributed ownership: red-infra (T1027, T1140, T1480, T1497, T1553), red-exploit (T1055, T1218), red-privesc (T1134), red-lateral (T1205, T1572), red-persist (T1070, T1070.006, T1014), red-exfil (data encoding, encrypted channels) -- 15 techniques total |
| **Defensive Coverage** | No dedicated detection engineering agent. eng-devsecops provides SAST/DAST (catches some evasion at code level). eng-incident provides post-compromise monitoring (catches some evasion at runtime). Neither agent explicitly addresses defense evasion technique detection. |
| **Risk** | Adversaries can evade all automated defenses. The 15 red-team evasion techniques have no systematic detection methodology. This is the most comprehensive offensive capability with the least corresponding defensive coverage. |
| **ATT&CK Techniques Uncovered** | T1027 (Obfuscated Files), T1055 (Process Injection), T1070 (Indicator Removal), T1014 (Rootkit), T1205 (Traffic Signaling), T1572 (Protocol Tunneling), T1134 (Access Token Manipulation), T1218 (Signed Binary Proxy Execution), T1480 (Execution Guardrails), T1497 (Sandbox Evasion), T1553 (Subvert Trust Controls), T1140 (Deobfuscate Files) |
| **Integration Point** | IP-4 (Incident Response Validation): red-persist/red-lateral/red-exfil <-> eng-incident -- this integration point exists but does not cover detection engineering |

#### GAP-C02: Command and Control Detection Gap (TA0011)

| Attribute | Detail |
|-----------|--------|
| **Gap Type** | GAP-DEFENSE |
| **Severity** | Critical |
| **Tactic** | TA0011 Command and Control |
| **Offensive Coverage** | red-infra covers 6 C2 techniques: T1071 (Application Layer Protocol), T1090 (Proxy), T1095 (Non-Application Layer Protocol), T1105 (Ingress Tool Transfer), T1132 (Data Encoding), T1573 (Encrypted Channel) |
| **Defensive Coverage** | eng-incident addresses monitoring broadly but has no explicit C2 detection methodology. eng-infra provides network segmentation and egress controls (mitigates but does not detect). No agent performs C2 traffic analysis, beaconing detection, or JA3/JA3S fingerprinting. |
| **Risk** | Established C2 channels can persist undetected. Without C2-specific detection, red-infra's infrastructure remains invisible to the defensive team throughout an engagement. This directly undermines incident response effectiveness. |
| **ATT&CK Techniques Uncovered** | T1071 (Application Layer Protocol -- detection), T1090 (Proxy -- detection), T1095 (Non-Application Layer Protocol -- detection), T1132 (Data Encoding -- detection), T1573 (Encrypted Channel -- detection) |

### High Gaps

#### GAP-H01: Insecure Design Validation Gap (OWASP A04)

| Attribute | Detail |
|-----------|--------|
| **Gap Type** | GAP-OFFENSE |
| **Severity** | High |
| **Tactic** | TA0001 Initial Access (design-level) |
| **Defensive Coverage** | eng-architect produces threat models using STRIDE/DREAD/PASTA. eng-backend verifies A04 compliance through secure defaults and threat model adherence. |
| **Offensive Coverage** | No red-team agent validates architectural design decisions. red-exploit tests implementation vulnerabilities (T1190, T1133, T1078) but does not test design-level flaws (business logic abuse, race conditions in design, trust boundary violations). |
| **Risk** | Architecture-level vulnerabilities may pass through the entire SDLC without adversarial testing. Threat models are self-validated by the defensive team, never stress-tested by the offensive team. |

#### GAP-H02: Supply Chain Attack Simulation Gap (TA0042)

| Attribute | Detail |
|-----------|--------|
| **Gap Type** | GAP-OFFENSE |
| **Severity** | High |
| **Tactic** | TA0042 Resource Development |
| **Defensive Coverage** | eng-infra implements SLSA build levels, SBOM generation (Syft), and dependency provenance verification. eng-devsecops runs dependency analysis (Snyk, Dependabot, OSV-Scanner) and container scanning (Trivy, Grype). |
| **Offensive Coverage** | red-infra covers TA0042 from the infrastructure provisioning perspective (T1583 Acquire Infrastructure, T1587 Develop Capabilities, T1588 Obtain Capabilities) but does NOT simulate supply chain attacks against the defender's build pipeline. red-infra builds offensive infrastructure; it does not attack defensive infrastructure. |
| **Risk** | SLSA and SBOM defenses are never adversarially tested. Supply chain attacks (dependency confusion, typosquatting, build pipeline compromise) represent a growing threat vector with no offensive simulation. eng-incident has a supply chain attack runbook but no corresponding red-team exercise. |

#### GAP-H03: Browser Exploitation and Client-Side Attack Gap

| Attribute | Detail |
|-----------|--------|
| **Gap Type** | GAP-OFFENSE |
| **Severity** | High |
| **Tactic** | TA0001 Initial Access, TA0002 Execution (client-side) |
| **Defensive Coverage** | eng-frontend implements XSS prevention (reflected, stored, DOM-based), CSP design, CORS hardening, output encoding, and secure state management. |
| **Offensive Coverage** | No red-team agent specializes in client-side exploitation. red-exploit focuses on server-side exploitation (T1190 Exploit Public-Facing Application) and limited client execution (T1203 Exploitation for Client Execution). red-social handles phishing delivery but not browser-based exploitation chains. No agent tests CSP bypass, DOM clobbering, prototype pollution, or client-side template injection. |
| **Risk** | eng-frontend defenses (CSP, CORS, XSS prevention) are never adversarially validated. The entire client-side attack surface relies solely on defensive self-verification and DAST scanning. |

#### GAP-H04: CI/CD Pipeline Attack Simulation Gap

| Attribute | Detail |
|-----------|--------|
| **Gap Type** | GAP-OFFENSE |
| **Severity** | High |
| **Tactic** | TA0002 Execution, TA0003 Persistence (pipeline context) |
| **Defensive Coverage** | eng-devsecops configures CI/CD security gates with blocking thresholds, SAST/DAST/secrets scanning, and SLSA build automation. eng-infra provides IaC scanning (Checkov, tfsec). |
| **Offensive Coverage** | No red-team agent simulates attacks against the CI/CD pipeline itself. The build pipeline is treated as trusted infrastructure by all red-team agents. No agent tests: poisoned pipeline execution, secrets extraction from CI environment variables, build cache poisoning, or runner compromise. |
| **Risk** | The CI/CD pipeline is a high-value target (contains secrets, has deployment access, processes untrusted code). Without offensive pipeline testing, eng-devsecops security gates are validated only by the tools themselves, creating a self-referential validation loop. |

### Medium Gaps

#### GAP-M01: Rootkit Detection Gap (T1014)

| Attribute | Detail |
|-----------|--------|
| **Gap Type** | GAP-DEFENSE |
| **Severity** | Medium |
| **Tactic** | TA0005 Defense Evasion |
| **Detail** | red-persist provides rootkit methodology guidance (T1014). No eng-team agent addresses rootkit detection or kernel-level integrity monitoring. eng-incident monitoring assumes standard system visibility, which rootkits subvert. |

#### GAP-M02: Timestomping Detection Gap (T1070.006)

| Attribute | Detail |
|-----------|--------|
| **Gap Type** | GAP-DEFENSE |
| **Severity** | Medium |
| **Tactic** | TA0005 Defense Evasion |
| **Detail** | red-persist applies timestomping to persistence artifacts. No eng-team agent addresses timestamp integrity verification or forensic timeline analysis. eng-incident runbooks do not include timestomping detection procedures. |

#### GAP-M03: Protocol Tunneling Detection Gap (T1572)

| Attribute | Detail |
|-----------|--------|
| **Gap Type** | GAP-DEFENSE |
| **Severity** | Medium |
| **Tactic** | TA0005 Defense Evasion / TA0011 C2 |
| **Detail** | red-lateral uses protocol tunneling to encapsulate movement traffic within legitimate protocols. eng-infra provides network segmentation but does not perform deep packet inspection or protocol analysis to detect tunneled traffic. |

#### GAP-M04: Traffic Signaling Detection Gap (T1205)

| Attribute | Detail |
|-----------|--------|
| **Gap Type** | GAP-DEFENSE |
| **Severity** | Medium |
| **Tactic** | TA0005 Defense Evasion |
| **Detail** | red-lateral applies traffic signaling to evade network monitoring. No eng-team agent addresses traffic signaling detection. eng-incident monitoring configurations do not include network behavioral analysis for signaling patterns. |

#### GAP-M05: DLP Bypass Validation Gap (TA0010)

| Attribute | Detail |
|-----------|--------|
| **Gap Type** | GAP-DEFENSE |
| **Severity** | Medium |
| **Tactic** | TA0010 Exfiltration |
| **Detail** | red-exfil covers exfiltration over C2 (T1041), alternative protocols (T1048), and web services (T1567). eng-incident references DLP monitoring but no eng-team agent implements or configures DLP rules. DLP is mentioned as a capability assumption, not an implemented defense. |

#### GAP-M06: Internal Discovery Detection Gap (TA0007)

| Attribute | Detail |
|-----------|--------|
| **Gap Type** | GAP-DEFENSE |
| **Severity** | Medium |
| **Tactic** | TA0007 Discovery |
| **Detail** | red-lateral performs internal discovery (T1018, T1046, T1049, T1082, T1083). eng-infra provides network segmentation to limit discovery scope, and eng-incident monitors for anomalies. However, no eng-team agent configures specific detection rules for internal network scanning, service enumeration, or file system discovery patterns. |

#### GAP-M07: Living-Off-the-Land Detection Gap (LOLBins)

| Attribute | Detail |
|-----------|--------|
| **Gap Type** | GAP-DEFENSE |
| **Severity** | Medium |
| **Tactic** | TA0008 Lateral Movement |
| **Detail** | red-lateral prefers living-off-the-land techniques using built-in tools (PowerShell remoting, WMI, SSH, RDP). These techniques evade traditional endpoint detection because they use legitimate system binaries. No eng-team agent addresses LOLBin detection or behavioral analysis for legitimate tool misuse. |

#### GAP-M08: Vishing Validation Gap

| Attribute | Detail |
|-----------|--------|
| **Gap Type** | GAP-OFFENSE (partial) |
| **Severity** | Medium |
| **Tactic** | TA0001 Initial Access (social) |
| **Detail** | red-social includes vishing (voice phishing) methodology. However, the engagement framework is designed for LLM-based interactions, not voice channel testing. Vishing methodology guidance can be produced, but actual voice social engineering testing requires human practitioners and telecommunications infrastructure outside the LLM agent scope. |

#### GAP-M09: Physical Security Testing Gap

| Attribute | Detail |
|-----------|--------|
| **Gap Type** | GAP-OFFENSE |
| **Severity** | Medium |
| **Tactic** | TA0001 Initial Access |
| **Detail** | Neither skill addresses physical access vectors (tailgating, USB drop attacks, hardware implants). OSSTMM Section VI (Physical Security Testing) has no corresponding agent on either side. This is an accepted scope limitation of LLM-based agent frameworks. |

#### GAP-M10: Wireless Network Testing Gap

| Attribute | Detail |
|-----------|--------|
| **Gap Type** | GAP-OFFENSE |
| **Severity** | Medium |
| **Tactic** | TA0001 Initial Access |
| **Detail** | Neither skill addresses wireless network attack vectors (rogue AP, evil twin, WPA cracking, Bluetooth exploitation). OSSTMM Section IV (Wireless Security Testing) has no corresponding agent. This is an accepted scope limitation of LLM-based agent frameworks that cannot interact with wireless hardware. |

#### GAP-M11: Ransomware Recovery Validation Gap

| Attribute | Detail |
|-----------|--------|
| **Gap Type** | GAP-OFFENSE |
| **Severity** | Medium |
| **Tactic** | TA0040 Impact |
| **Detail** | eng-incident has a ransomware runbook (encryption attack, backup destruction, extortion). red-exploit demonstrates impact only in safe/controlled mode (T1486 Data Encrypted for Impact -- demonstration only). The ransomware runbook is never validated against a realistic ransomware simulation. red-exploit's "demonstration only" constraint limits the fidelity of impact testing. |

#### GAP-M12: MFA Fatigue Attack Coverage Gap

| Attribute | Detail |
|-----------|--------|
| **Gap Type** | GAP-DEFENSE |
| **Severity** | Medium |
| **Tactic** | TA0006 Credential Access |
| **Detail** | red-social references MFA fatigue as a credential harvesting technique. eng-backend implements MFA support but no eng-team agent addresses MFA fatigue detection, rate limiting on MFA push notifications, or number matching enforcement. eng-incident's authentication compromise runbook does not specifically address MFA fatigue scenarios. |

### Low Gaps

#### GAP-L01: Email Collection Detection (T1114)

| Attribute | Detail |
|-----------|--------|
| **Gap Type** | GAP-DEFENSE |
| **Severity** | Low |
| **Tactic** | TA0009 Collection |
| **Detail** | red-exfil covers T1114 Email Collection. No eng-team agent addresses email security monitoring or mailbox access auditing. Email infrastructure is outside the current scope of both skills. |

#### GAP-L02: Taint Shared Content Detection (T1080)

| Attribute | Detail |
|-----------|--------|
| **Gap Type** | GAP-DEFENSE |
| **Severity** | Low |
| **Tactic** | TA0008 Lateral Movement |
| **Detail** | red-lateral references T1080 Taint Shared Content. No eng-team agent addresses shared content integrity monitoring or detection of content modification on file shares. |

#### GAP-L03: Forced Authentication Detection (T1187)

| Attribute | Detail |
|-----------|--------|
| **Gap Type** | GAP-DEFENSE |
| **Severity** | Low |
| **Tactic** | TA0006 Credential Access |
| **Detail** | red-privesc covers T1187 Forced Authentication (LLMNR/NBT-NS poisoning, responder attacks). eng-backend implements authentication but does not address forced authentication protocol-level attacks. Network-level mitigations (disabling LLMNR/NBT-NS) fall between eng-infra and eng-backend without clear ownership. |

#### GAP-L04: Kerberos Attack Detection (T1558)

| Attribute | Detail |
|-----------|--------|
| **Gap Type** | GAP-DEFENSE |
| **Severity** | Low |
| **Tactic** | TA0006 Credential Access |
| **Detail** | red-privesc covers T1558 Steal or Forge Kerberos Tickets (Kerberoasting, Golden/Silver Ticket). eng-backend implements authentication frameworks but does not address Active Directory-specific Kerberos attack detection. This is an environment-dependent gap relevant only to AD-integrated deployments. |

#### GAP-L05: Create Account Detection (T1136)

| Attribute | Detail |
|-----------|--------|
| **Gap Type** | GAP-DEFENSE |
| **Severity** | Low |
| **Tactic** | TA0003 Persistence |
| **Detail** | red-persist covers T1136 Create Account for persistence. eng-backend implements RBAC/ABAC but does not monitor for unauthorized account creation events. eng-incident monitoring configurations do not specifically alert on new account creation outside authorized provisioning workflows. |

#### GAP-L06: Data from Information Repositories (T1213)

| Attribute | Detail |
|-----------|--------|
| **Gap Type** | GAP-DEFENSE |
| **Severity** | Low |
| **Tactic** | TA0009 Collection |
| **Detail** | red-exfil covers T1213 Data from Information Repositories (wikis, SharePoint, code repositories). No eng-team agent addresses access auditing for information repositories. Repository access controls exist at the platform level but are outside current agent scope. |

#### GAP-L07: Sandbox Evasion Validation (T1497)

| Attribute | Detail |
|-----------|--------|
| **Gap Type** | GAP-DEFENSE |
| **Severity** | Low |
| **Tactic** | TA0005 Defense Evasion |
| **Detail** | red-infra covers T1497 Virtualization/Sandbox Evasion for payload development. eng-devsecops uses sandboxed analysis environments (DAST scanning) but does not address anti-sandbox evasion techniques. Payloads designed to evade sandbox analysis could bypass DAST gates. |

#### GAP-L08: WMI Lateral Movement Detection (T1047)

| Attribute | Detail |
|-----------|--------|
| **Gap Type** | GAP-DEFENSE |
| **Severity** | Low |
| **Tactic** | TA0008 Lateral Movement |
| **Detail** | red-lateral covers T1047 Windows Management Instrumentation for lateral movement. No eng-team agent addresses WMI event monitoring or WMI command auditing. WMI-based lateral movement is environment-dependent (Windows infrastructure). |

#### GAP-L09: Process Injection Detection (T1055)

| Attribute | Detail |
|-----------|--------|
| **Gap Type** | GAP-DEFENSE |
| **Severity** | Low |
| **Tactic** | TA0005 Defense Evasion / TA0004 Privilege Escalation |
| **Detail** | red-exploit covers T1055 Process Injection as an execution-time evasion technique. No eng-team agent addresses process injection detection (ETW monitoring, DLL load monitoring, memory integrity checking). This gap is partially mitigated by runtime application security controls but no explicit detection exists. |

---

## Defensive Coverage Analysis

This section maps /eng-team agent capabilities to MITRE ATT&CK tactics, documenting the translation from SDLC frameworks to adversary-relevant defenses.

### eng-architect

| Defensive Capability | Framework Reference | ATT&CK Mapping | Coverage Strength |
|----------------------|-------------------|----------------|-------------------|
| Threat modeling (STRIDE/DREAD/PASTA) | NIST CSF 2.0, OWASP Threat Modeling | All tactics (identifies threats) | MODERATE -- identifies threats but does not implement mitigations |
| Trust boundary analysis | PASTA methodology | TA0001 (boundary violations), TA0008 (segmentation) | MODERATE |
| Security architecture patterns | NIST CSF 2.0 ID/PR | TA0001, TA0004, TA0005 (architectural controls) | MODERATE |
| SSDF: PO.1, PO.2, PO.5 | NIST SSDF | Process-level coverage for all tactics | WEAK (process, not technical) |

### eng-lead

| Defensive Capability | Framework Reference | ATT&CK Mapping | Coverage Strength |
|----------------------|-------------------|----------------|-------------------|
| Implementation planning with security standards | MS SDL, OWASP SAMM | All tactics (standards enforcement) | WEAK (process orchestration) |
| Dependency governance | SAMM v2.0 | TA0042 (supply chain) | MODERATE |
| SSDF: PO.1, PO.3, PS.1, PS.2 | NIST SSDF | Process-level governance | WEAK (process, not technical) |

### eng-backend

| Defensive Capability | Framework Reference | ATT&CK Mapping | Coverage Strength |
|----------------------|-------------------|----------------|-------------------|
| OWASP Top 10 mitigations (A01-A10) | OWASP Top 10 2021 | TA0001 (A01, A03, A07, A10), TA0002 (A03), TA0004 (A01), TA0006 (A02, A07) | STRONG |
| Input validation at trust boundaries | OWASP ASVS 5.0 Ch. 5 | TA0001 (injection), TA0002 (command execution) | STRONG |
| Auth implementation (OAuth2, OIDC, RBAC, ABAC) | OWASP ASVS 5.0 Ch. 2-4 | TA0004 (privilege escalation), TA0006 (credential access) | STRONG |
| API security (rate limiting, schema validation) | OWASP API Security Top 10 | TA0001, TA0043 (rate limiting reduces recon) | MODERATE |
| Database security (parameterized queries, least privilege) | OWASP ASVS 5.0 Ch. 12 | TA0002 (SQL injection), TA0009 (data access control) | STRONG |
| SSDF: PW.1, PW.5, PW.6 | NIST SSDF | Implementation-level security | STRONG |

### eng-frontend

| Defensive Capability | Framework Reference | ATT&CK Mapping | Coverage Strength |
|----------------------|-------------------|----------------|-------------------|
| XSS prevention (reflected, stored, DOM-based) | OWASP Top 10 A03/A07 | TA0002 (client-side execution) | STRONG |
| Content Security Policy (CSP) design | W3C CSP Level 3 | TA0002 (script execution restriction) | STRONG |
| CORS hardening | OWASP CORS guidance | TA0001 (cross-origin attacks) | MODERATE |
| Output encoding | OWASP Encoding Project | TA0002 (injection prevention) | STRONG |
| SSDF: PW.1, PW.5, PW.6 | NIST SSDF | Implementation-level security | STRONG |

### eng-infra

| Defensive Capability | Framework Reference | ATT&CK Mapping | Coverage Strength |
|----------------------|-------------------|----------------|-------------------|
| IaC security scanning (Checkov, tfsec) | CIS Benchmarks | TA0001 (misconfiguration), TA0003 (config hardening) | MODERATE |
| Container hardening (non-root, minimal base, Trivy) | CIS Docker/K8s Benchmarks | TA0002 (execution restriction), TA0004 (privilege containment) | STRONG |
| Network segmentation (microsegmentation) | NIST SP 800-207 Zero Trust | TA0007 (discovery limitation), TA0008 (movement restriction) | STRONG |
| Secrets management (vault, rotation) | OWASP Secrets Management | TA0006 (credential protection) | STRONG |
| SBOM generation (Syft) | NTIA SBOM Minimum Elements | TA0042 (supply chain transparency) | MODERATE |
| SLSA build levels | SLSA v1.0 | TA0042 (build integrity) | STRONG |
| CIS Benchmark compliance | CIS Benchmarks v8 | TA0003 (hardening), TA0004 (privilege restriction) | STRONG |
| SSDF: PS.1, PS.2, PS.3, PW.4 | NIST SSDF | Infrastructure security | STRONG |

### eng-devsecops

| Defensive Capability | Framework Reference | ATT&CK Mapping | Coverage Strength |
|----------------------|-------------------|----------------|-------------------|
| SAST (Semgrep CI, CodeQL) | NIST SSDF PW.7 | TA0001 (code-level vulnerability detection), TA0002 (injection detection) | STRONG |
| DAST (OWASP ZAP, Nuclei) | OWASP Testing Guide | TA0001 (runtime vulnerability detection) | STRONG |
| Secrets scanning (Gitleaks, TruffleHog) | OWASP Secrets Management | TA0006 (credential exposure prevention) | STRONG |
| Container scanning (Trivy, Grype) | CIS Benchmarks | TA0042 (vulnerable component detection) | STRONG |
| Dependency analysis (Snyk, Dependabot, OSV-Scanner) | OWASP Dependency-Check | TA0042 (known vulnerability detection) | STRONG |
| CI/CD security gates | DevSecOps Best Practices | TA0001, TA0002 (pre-deployment blocking) | STRONG |
| SSDF: PW.7, PW.8, PS.1 | NIST SSDF | Automated verification | STRONG |

### eng-qa

| Defensive Capability | Framework Reference | ATT&CK Mapping | Coverage Strength |
|----------------------|-------------------|----------------|-------------------|
| Security test strategy | OWASP Testing Guide v4.2 | All applicable tactics (test coverage) | MODERATE |
| Fuzzing (AFL, libFuzzer) | CWE fuzzing guidelines | TA0001 (input boundary testing), TA0002 (execution testing) | MODERATE |
| Property-based testing (Hypothesis) | Test methodology | TA0001, TA0002 (invariant testing) | MODERATE |
| SSDF: PW.7, PW.8 | NIST SSDF | Test verification | MODERATE |

### eng-security

| Defensive Capability | Framework Reference | ATT&CK Mapping | Coverage Strength |
|----------------------|-------------------|----------------|-------------------|
| Manual code review | CWE Top 25 2025 | TA0001 (vulnerability identification), TA0002 (injection review) | STRONG |
| ASVS 5.0 verification | OWASP ASVS 5.0 | TA0004 (access control), TA0006 (authentication), TA0009 (data protection) | STRONG |
| CVSS scoring | FIRST CVSS v4.0 | Risk quantification for all tactics | MODERATE (scoring, not defense) |
| Data flow tracing | Threat modeling | TA0009 (collection path identification), TA0010 (exfiltration path identification) | MODERATE |
| SSDF: PW.7 | NIST SSDF | Review verification | STRONG |

### eng-reviewer

| Defensive Capability | Framework Reference | ATT&CK Mapping | Coverage Strength |
|----------------------|-------------------|----------------|-------------------|
| Final quality gate | Quality enforcement SSOT | All tactics (compliance verification) | MODERATE (process gate, not technical) |
| Architecture compliance check | ADR compliance | TA0001, TA0004 (architectural control enforcement) | MODERATE |
| /adversary integration for C2+ | S-014 LLM-as-Judge | Adversarial quality review | MODERATE |
| SSDF: RV.1, RV.2, RV.3 | NIST SSDF | Release verification | MODERATE |

### eng-incident

| Defensive Capability | Framework Reference | ATT&CK Mapping | Coverage Strength |
|----------------------|-------------------|----------------|-------------------|
| IR runbooks (6 categories) | NIST SP 800-61 Rev. 2 | TA0040 (response and recovery), TA0003 (persistence detection), TA0008 (containment) | STRONG |
| Vulnerability lifecycle management | NIST SSDF RV practices | All tactics (post-discovery) | STRONG |
| Monitoring configuration | NIST CSF DE.CM | TA0003 (persistence monitoring), TA0005 (partial evasion detection), TA0008 (movement detection), TA0010 (exfiltration monitoring) | MODERATE |
| Containment procedures | NIST SP 800-61 | TA0008 (lateral movement containment), TA0040 (impact containment) | STRONG |
| Remediation tracking with SLAs | Vulnerability management | All tactics (post-detection) | STRONG |
| Integration Point IP-4 | Purple team framework FEAT-040 | Cross-skill validation of detection capabilities | MODERATE |
| SSDF: RV.1, RV.2, RV.3 | NIST SSDF | Post-deployment response | STRONG |

---

## Offensive Coverage Analysis

This section maps /red-team agent capabilities to their ATT&CK tactic and technique assignments.

### Agent-to-Tactic Mapping

| Agent | Primary Tactic(s) | Techniques (explicit) | RoE-Gated | Defense Evasion Domain |
|-------|-------------------|----------------------|-----------|----------------------|
| red-lead | All (oversight) | None specific (methodology selection) | No | None (oversight) |
| red-recon | TA0043 Reconnaissance | T1595, T1592, T1589, T1590, T1591, T1593, T1594, T1596, T1597, T1598 | No | None |
| red-vuln | None (analysis support) | None specific (CVE research, CVSS scoring) | No | None |
| red-exploit | TA0001, TA0002, TA0040 | T1190, T1133, T1078, T1059, T1203, T1485, T1486, T1489 | No | Execution-time: T1055, T1218 |
| red-privesc | TA0004, TA0006 | T1068, T1078, T1134, T1548, T1574, T1003, T1110, T1187, T1552, T1558 | No | T1134 (Access Token Manipulation) |
| red-lateral | TA0008, TA0007 | T1021, T1021.001, T1047, T1021.006, T1080, T1570, T1018, T1046, T1049, T1082, T1083 | No | T1205 (Traffic Signaling), T1572 (Protocol Tunneling) |
| red-persist | TA0003, TA0005 (persistence) | T1053, T1543, T1547, T1546, T1505, T1136, T1070, T1070.006, T1014 | Yes | T1070 (Indicator Removal), T1070.006 (Timestomping), T1014 (Rootkit) |
| red-exfil | TA0009, TA0010 | T1005, T1039, T1114, T1213, T1560, T1041, T1048, T1567, T1030 | Yes | Data encoding, encrypted channels |
| red-reporter | TA0040 (documentation) | None specific (finding documentation) | No | None |
| red-infra | TA0042, TA0011, TA0005 (tool) | T1583, T1584, T1587, T1588, T1608, T1071, T1090, T1095, T1105, T1132, T1573, T1027, T1140, T1480, T1497, T1553 | No | T1027, T1140, T1480, T1497, T1553 |
| red-social | TA0043 (social), TA0001 (phishing) | T1589, T1591, T1593, T1597, T1566, T1566.001, T1566.002, T1566.003, T1598 | Yes | None |

### Defense Evasion Distribution (TA0005)

The /red-team uses a distributed defense evasion ownership model (ADR-PROJ010-001, Section 4.3.5) where evasion techniques are assigned to the agent most contextually appropriate for their application:

| Agent | Evasion Domain | Techniques | Rationale |
|-------|---------------|------------|-----------|
| red-infra | Tool-level evasion | T1027, T1140, T1480, T1497, T1553 | Payload obfuscation and sandbox evasion during tool development |
| red-exploit | Execution-time evasion | T1055, T1218 | Process injection and signed binary abuse during exploitation |
| red-privesc | Privilege-context evasion | T1134 | Access token manipulation during privilege escalation |
| red-lateral | Network-level evasion | T1205, T1572 | Traffic signaling and protocol tunneling during movement |
| red-persist | Persistence-phase evasion | T1070, T1070.006, T1014 | Indicator removal, timestomping, rootkits to protect persistence |
| red-exfil | Exfiltration evasion | Data encoding, encrypted channels | Data obfuscation during exfiltration |

**Total TA0005 techniques covered:** 15 explicit technique references across 6 agents.

### Technique Coverage Quantification

| Tactic | ATT&CK Techniques (Enterprise v15) | Red-Team Techniques Covered | Coverage % |
|--------|--------------------------------------|---------------------------|------------|
| TA0043 Reconnaissance | 10 | 10 (red-recon: all 10 techniques) | 100% |
| TA0042 Resource Development | 7 | 5 (red-infra) | 71% |
| TA0001 Initial Access | 9 | 6 (red-exploit: 3, red-social: 3 phishing variants + info phishing) | 67% |
| TA0002 Execution | 14 | 2 (red-exploit: T1059, T1203) | 14% |
| TA0003 Persistence | 19 | 6 (red-persist) | 32% |
| TA0004 Privilege Escalation | 13 | 5 (red-privesc) | 38% |
| TA0005 Defense Evasion | 42 | 15 (distributed across 6 agents) | 36% |
| TA0006 Credential Access | 17 | 5 (red-privesc) | 29% |
| TA0007 Discovery | 32 | 5 (red-lateral) | 16% |
| TA0008 Lateral Movement | 9 | 6 (red-lateral) | 67% |
| TA0009 Collection | 17 | 5 (red-exfil) | 29% |
| TA0010 Exfiltration | 9 | 4 (red-exfil) | 44% |
| TA0011 Command and Control | 16 | 6 (red-infra) | 38% |
| TA0040 Impact | 13 | 3 (red-exploit, demo only) | 23% |

**Note:** Technique counts reflect primary techniques only (not sub-techniques). ATT&CK Enterprise v15 technique counts per tactic are approximate reference values. Coverage percentages indicate the proportion of ATT&CK techniques within each tactic that have explicit red-team agent ownership.

---

## Coverage Statistics

### Tactic-Level Bidirectional Coverage

| Metric | Value |
|--------|-------|
| Total ATT&CK Enterprise Tactics | 14 |
| Tactics with Red-Team Coverage | 14 (100%) |
| Tactics with Eng-Team Coverage | 14 (100%) |
| Tactics with STRONG Bidirectional Coverage | 4 (29%) |
| Tactics with Bidirectional Coverage (any strength) | 11 (79%) |
| Tactics with Partial Coverage (one side WEAK) | 3 (21%) |
| Tactics with No Coverage (either side) | 0 (0%) |

### Gap Distribution

| Gap Type | Count | Percentage |
|----------|-------|------------|
| GAP-DEFENSE (attack without defense) | 16 | 59% |
| GAP-OFFENSE (defense without test) | 9 | 33% |
| PARTIAL (technique-level) | 2 | 7% |
| NO_COVERAGE | 0 | 0% |
| **Total** | **27** | **100%** |

### Gap Severity Distribution

| Severity | Count | Percentage |
|----------|-------|------------|
| Critical | 2 | 7% |
| High | 4 | 15% |
| Medium | 12 | 44% |
| Low | 9 | 33% |
| **Total** | **27** | **100%** |

### Coverage by ATT&CK Kill Chain Phase

| Kill Chain Phase | Tactics | Red Coverage | Eng Coverage | Gap Count |
|-----------------|---------|-------------|-------------|-----------|
| Pre-Attack | TA0043, TA0042 | STRONG | MODERATE | 2 (GAP-H02, GAP-M09) |
| Initial Compromise | TA0001, TA0002 | STRONG | STRONG | 4 (GAP-H01, GAP-H03, GAP-M08, GAP-M10) |
| Post-Exploitation | TA0003, TA0004, TA0005, TA0006 | STRONG | MODERATE-STRONG | 10 (GAP-C01, GAP-M01, GAP-M02, GAP-M12, GAP-L03, GAP-L04, GAP-L05, GAP-L07, GAP-L09, plus TA0004/TA0006 covered) |
| Propagation | TA0007, TA0008 | STRONG | MODERATE | 4 (GAP-M06, GAP-M07, GAP-L02, GAP-L08) |
| Action on Objectives | TA0009, TA0010, TA0011, TA0040 | STRONG | MODERATE-WEAK | 7 (GAP-C02, GAP-M03, GAP-M04, GAP-M05, GAP-M11, GAP-L01, GAP-L06) |

### Defense Evasion Gap Concentration

Defense evasion represents the single largest coverage asymmetry:

| Metric | Value |
|--------|-------|
| Red-team TA0005 techniques | 15 (across 6 agents) |
| Eng-team TA0005 detection techniques | 0 (explicit) |
| Eng-team indirect TA0005 coverage | 3 (SAST catches some code-level evasion, DAST catches some runtime evasion, monitoring catches some behavioral indicators) |
| Gaps in TA0005 alone | 5 (GAP-C01, GAP-M01, GAP-M02, GAP-M03, GAP-M04) |

---

## Remediation Recommendations

### Priority 1: Critical Gap Remediation

#### REC-C01: Create Detection Engineering Agent (eng-detection)

**Addresses:** GAP-C01 (Defense Evasion), GAP-C02 (C2 Detection), GAP-M01 (Rootkit), GAP-M02 (Timestomping), GAP-M03 (Protocol Tunneling), GAP-M04 (Traffic Signaling), GAP-M06 (Internal Discovery Detection), GAP-M07 (LOLBin Detection), GAP-L07 (Sandbox Evasion), GAP-L08 (WMI Detection), GAP-L09 (Process Injection Detection)

**Recommendation:** Create a new /eng-team agent, **eng-detection**, specializing in detection engineering and threat hunting. This agent would own:

- **Detection rule development:** SIGMA rules, YARA rules, Suricata/Snort signatures mapped to ATT&CK technique IDs
- **C2 traffic analysis:** Beaconing detection, JA3/JA3S fingerprinting, DNS anomaly detection, protocol analysis
- **Defense evasion detection:** Process injection monitoring (ETW), LOLBin behavioral analysis, rootkit detection (kernel integrity), timestomping detection (MFT analysis)
- **Network behavioral analysis:** Traffic signaling detection, protocol tunneling identification, lateral movement patterns
- **SSDF mapping:** RV.1 (identify vulnerabilities), DE.CM (continuous monitoring)
- **Integration Point:** Extends IP-4 (Incident Response Validation) by adding proactive detection engineering that feeds eng-incident's reactive response capabilities

**Impact:** Resolves 11 of 27 gaps (41%), including both critical gaps. Estimated agent complexity: comparable to eng-incident.

**Effort Estimate:** Medium-high. Requires new agent definition, detection methodology framework, SIGMA/YARA template library, and integration with eng-incident workflow.

#### REC-C02: Enhance eng-incident with C2 Detection Runbooks

**Addresses:** GAP-C02 (C2 Detection) -- interim measure pending REC-C01

**Recommendation:** If REC-C01 is deferred, add C2 detection methodology to eng-incident's monitoring configuration capabilities:

- Add a "Command and Control Detection" runbook category alongside the existing 6 categories
- Include beaconing pattern detection, encrypted channel analysis, and proxy chain identification
- Reference ATT&CK T1071, T1090, T1095, T1132, T1573 in runbook scope

**Impact:** Partially addresses GAP-C02 within existing agent architecture. Does not address the broader detection engineering gap (GAP-C01).

### Priority 2: High Gap Remediation

#### REC-H01: Create Architecture Validation Agent or Red-Team Design Review Capability

**Addresses:** GAP-H01 (Insecure Design Validation)

**Recommendation:** Extend the purple team framework (IP-1: Threat-Informed Architecture) to include adversarial design review. Two implementation options:

- **Option A:** Add architectural attack methodology to red-vuln's scope (red-vuln currently bridges recon and exploitation; design-level vulnerability analysis is a natural extension)
- **Option B:** Create a purple team engagement type "Architecture Stress Test" where red-recon and red-vuln collaborate to attack eng-architect's threat model assumptions

**Impact:** Closes the design-level validation gap. Ensures threat models are stress-tested by adversarial perspective before implementation begins.

#### REC-H02: Add Supply Chain Attack Simulation Capability

**Addresses:** GAP-H02 (Supply Chain Attack Simulation)

**Recommendation:** Extend red-infra's scope to include supply chain attack simulation against the defensive build pipeline, or create a dedicated enabler for supply chain purple team exercises:

- Dependency confusion simulation (test Snyk/Dependabot detection of malicious package substitution)
- Build pipeline integrity testing (test SLSA provenance verification with tampered artifacts)
- Container image supply chain testing (test Trivy/Grype detection of backdoored base images)

**Impact:** Validates eng-infra SLSA and eng-devsecops dependency scanning against realistic supply chain attack scenarios.

#### REC-H03: Add Client-Side Exploitation Capability to Red Team

**Addresses:** GAP-H03 (Browser Exploitation)

**Recommendation:** Extend red-exploit's technique scope to include client-side exploitation techniques, or create a new specialized agent (red-client):

- CSP bypass methodology
- DOM clobbering and prototype pollution testing
- Client-side template injection
- XSS filter evasion (complementing red-social's phishing delivery)

**Impact:** Provides adversarial validation of eng-frontend's XSS prevention, CSP, and CORS hardening. Connects red-social's phishing delivery to browser-based exploitation chains.

#### REC-H04: Add CI/CD Pipeline Attack Capability

**Addresses:** GAP-H04 (CI/CD Pipeline Attack Simulation)

**Recommendation:** Create a purple team exercise type for CI/CD pipeline security assessment:

- Test CI/CD security gates with crafted bypass payloads
- Validate secrets protection in build environments
- Test SLSA build provenance verification under adversarial conditions
- Simulate runner compromise and pipeline poisoning scenarios

**Impact:** Breaks the self-referential validation loop where eng-devsecops tools validate themselves. Provides external adversarial perspective on pipeline security.

### Priority 3: Medium Gap Remediation

#### REC-M01: Expand eng-incident Monitoring Scope

**Addresses:** GAP-M05 (DLP), GAP-M06 (Internal Discovery Detection), GAP-L01 (Email Collection), GAP-L05 (Account Creation)

**Recommendation:** Expand eng-incident's monitoring configuration methodology to include:

- DLP rule design and validation (currently referenced but not implemented)
- Internal network scan detection rules
- Unauthorized account creation alerting
- Email access anomaly detection

**Impact:** Strengthens post-deployment detection across 4 medium and low gaps.

#### REC-M02: Add MFA Resilience to eng-backend

**Addresses:** GAP-M12 (MFA Fatigue)

**Recommendation:** Add MFA fatigue attack resilience to eng-backend's authentication implementation methodology:

- Number matching enforcement for MFA push notifications
- Rate limiting on MFA challenge issuance
- MFA fatigue detection alerting (multiple denied push notifications)
- Phishing-resistant MFA recommendation (FIDO2/WebAuthn)

**Impact:** Addresses the growing MFA fatigue attack vector with concrete implementation guidance.

#### REC-M03: Document Accepted Scope Limitations

**Addresses:** GAP-M08 (Vishing), GAP-M09 (Physical), GAP-M10 (Wireless)

**Recommendation:** Formally document the following as accepted scope limitations of the LLM-based agent framework:

- Voice channel social engineering (vishing) requires human practitioners
- Physical security testing requires physical presence
- Wireless testing requires specialized hardware interaction

These should be documented in the framework scope statement rather than treated as remediation items. The /red-team can provide methodology guidance for all three, but execution requires human practitioners operating outside the LLM agent framework.

#### REC-M04: Create Ransomware Simulation Exercise Protocol

**Addresses:** GAP-M11 (Ransomware Recovery Validation)

**Recommendation:** Design a purple team exercise protocol that validates eng-incident's ransomware runbook:

- red-exploit demonstrates controlled encryption impact (within existing "demonstration only" constraint)
- eng-incident executes ransomware runbook
- Purple team framework (FEAT-040) measures response time, containment effectiveness, and recovery procedures

**Impact:** Validates the ransomware runbook through controlled exercise without requiring red-exploit to perform actual destructive operations.

### Priority 4: Low Gap Remediation

#### REC-L01: Enhance Network Protocol Monitoring (Batch)

**Addresses:** GAP-L02 (Shared Content), GAP-L03 (Forced Authentication), GAP-L04 (Kerberos), GAP-L08 (WMI)

**Recommendation:** These are environment-dependent gaps relevant to specific deployment contexts (Active Directory, Windows-heavy networks). Address through:

- Environment-specific monitoring addendum to eng-incident runbooks
- Detection rule templates for common Active Directory attacks
- Network protocol monitoring configuration for Windows environments

**Impact:** Addresses 4 low-severity gaps with a single monitoring configuration enhancement.

### Remediation Impact Summary

| Recommendation | Gaps Addressed | Severity Coverage | Effort |
|---------------|---------------|-------------------|--------|
| REC-C01: eng-detection agent | 11 | 2 Critical, 3 Medium, 6 Low | Medium-High |
| REC-C02: eng-incident C2 runbooks | 1 | 1 Critical (interim) | Low |
| REC-H01: Architecture validation | 1 | 1 High | Medium |
| REC-H02: Supply chain simulation | 1 | 1 High | Medium |
| REC-H03: Client-side exploitation | 1 | 1 High | Medium |
| REC-H04: CI/CD pipeline attack | 1 | 1 High | Medium |
| REC-M01: eng-incident monitoring | 4 | 1 Medium, 3 Low | Low-Medium |
| REC-M02: MFA resilience | 1 | 1 Medium | Low |
| REC-M03: Document scope limits | 3 | 3 Medium | Low |
| REC-M04: Ransomware exercise | 1 | 1 Medium | Medium |
| REC-L01: Protocol monitoring | 4 | 4 Low | Low |

**Total coverage if all recommendations implemented:** 27 of 27 gaps addressed (100%).

---

## L2 Strategic Implications

### 1. Structural Impedance Mismatch

The most significant strategic finding is the **framework impedance mismatch** between /eng-team and /red-team. The red-team operates natively in ATT&CK tactic/technique space, while the eng-team operates in SDLC framework space (OWASP, NIST SSDF, CIS). This creates three consequences:

- **Translation burden:** Every purple team exercise requires mapping between SDLC controls and ATT&CK techniques. This mapping is currently performed ad-hoc in this analysis rather than systematically maintained.
- **Coverage blind spots:** Defenses framed as SDLC practices (e.g., "input validation" or "secure defaults") may appear comprehensive within their framework but leave ATT&CK technique-level gaps that are only visible when the ATT&CK lens is applied.
- **Communication gap:** eng-team agents report in OWASP/ASVS terms; red-team agents report in ATT&CK terms. The purple team integration points (IP-1 through IP-4) bridge this at the integration level, but individual agents still think in their native framework.

**Strategic Recommendation:** Develop a maintained ATT&CK-to-SDLC mapping table as a shared artifact between the two skills. This table would serve as the authoritative translation layer for purple team exercises and gap tracking.

### 2. Detection Engineering Gap as Systemic Risk

The absence of a dedicated detection engineering capability is not merely a single gap but a **systemic risk** that affects the entire defensive posture. The /eng-team follows a "build secure, scan for vulnerabilities, respond to incidents" model. This model has a structural blind spot: it assumes that security controls are either present (prevent attack) or absent (incident response triggers). It does not address the middle ground where controls exist but are evaded.

Defense evasion is the adversary's answer to detection. With 15 evasion techniques distributed across 6 red-team agents and no corresponding detection engineering capability, the framework has a systematic inability to detect sophisticated adversaries who have bypassed prevention controls but have not yet triggered incident response thresholds.

**Strategic Recommendation:** Prioritize REC-C01 (eng-detection agent) as the single highest-impact investment. This agent fills a systemic gap rather than a technique-level gap.

### 3. Self-Referential Validation Anti-Pattern

Four gaps (GAP-H01, GAP-H02, GAP-H03, GAP-H04) share a common root cause: **defenses validated only by their own tooling**. eng-architect's threat models are reviewed by eng-reviewer (same team). eng-frontend's CSP is tested by eng-devsecops DAST (same pipeline). eng-infra's SLSA is verified by eng-infra's own SLSA tooling. eng-devsecops CI/CD gates are tested by eng-devsecops itself.

This self-referential validation pattern is the primary reason the purple team framework (FEAT-040) exists. However, the current integration points (IP-1 through IP-4) address cross-skill collaboration at the engagement level, not at the individual control validation level. Controls validated only internally have unknown real-world effectiveness.

**Strategic Recommendation:** Extend the purple team exercise protocol to include "control validation" exercises where specific defensive controls are tested against specific offensive techniques, beyond the current engagement-level integration.

### 4. Kill Chain Phase Coverage Asymmetry

Coverage quality degrades along the kill chain:

- **Pre-Attack and Initial Compromise:** Strong bidirectional coverage (both skills have mature capabilities)
- **Post-Exploitation:** Strong offensive, moderate-to-weak defensive (detection gaps emerge)
- **Action on Objectives:** Strong offensive, weak defensive (C2 and exfiltration detection gaps)

This pattern reflects a common real-world trend: organizations invest heavily in prevention (perimeter and initial access defenses) while underinvesting in detection and response for post-compromise activity. The framework mirrors this industry-wide pattern.

**Strategic Recommendation:** Invest disproportionately in post-exploitation and action-on-objectives defensive capabilities (REC-C01, REC-C02, REC-M01) to flatten the coverage asymmetry across kill chain phases.

### 5. RoE-Gated Agent Impact on Coverage Validation

Three red-team agents are RoE-gated: red-persist, red-exfil, and red-social. This means that persistence, exfiltration, and social engineering testing require explicit authorization before they can proceed. While this is architecturally correct for safety (ADR-PROJ010-006), it creates a practical coverage validation gap: organizations that do not authorize these activities in their RoE will have permanently untested defenses in TA0003, TA0009, TA0010, and social engineering aspects of TA0001/TA0043.

**Strategic Recommendation:** Document the coverage implications of RoE restrictions. When RoE gates prevent testing, the gap analysis should flag the corresponding defensive controls as "untested due to RoE restriction" rather than "tested and validated."

### 6. Agent Count Growth Trajectory

This analysis recommends adding 1-2 new agents (eng-detection, potentially red-client). The current roster stands at 21 agents (10 eng + 11 red). Adding agents increases complexity in:

- Agent coordination overhead
- Context window consumption during orchestration
- Integration point surface area
- Quality assurance burden

**Strategic Recommendation:** Evaluate whether eng-detection capabilities can be partially absorbed by eng-incident (monitoring expansion) before committing to a new agent. If a new agent is required, follow the portability and standalone design principles (AD-010) established in ADR-PROJ010-001 to minimize coordination overhead.

---

## References

| Source | Location | Content |
|--------|----------|---------|
| ADR-PROJ010-001 | `projects/PROJ-010-cyber-ops/decisions/ADR-PROJ010-001-agent-team-architecture.md` | 21-agent roster, handoff protocols, defense evasion ownership model |
| ADR-PROJ010-006 | `projects/PROJ-010-cyber-ops/decisions/ADR-PROJ010-006-authorization-scope-control.md` | Three-layer authorization architecture, RoE gating |
| FEAT-040 Purple Team Framework | `projects/PROJ-010-cyber-ops/work/EPIC-005-purple-team-validation/FEAT-040-purple-team-framework/purple-team-integration-framework.md` | Integration points IP-1 through IP-4, engagement protocol |
| A-003 ATT&CK Coverage Research | `projects/PROJ-010-cyber-ops/work/research/stream-a-role-completeness/A-003-mitre-attack-coverage.md` | Phase 1 baseline ATT&CK analysis |
| /red-team SKILL.md | `skills/red-team/SKILL.md` | 11-agent roster, ATT&CK mappings, kill chain workflow |
| /eng-team SKILL.md | `skills/eng-team/SKILL.md` | 10-agent roster, 8-step SDLC workflow |
| Red-team agents (11) | `skills/red-team/agents/red-*.md` | Per-agent ATT&CK technique references |
| Eng-team agents (10) | `skills/eng-team/agents/eng-*.md` | Per-agent defensive capabilities |
| MITRE ATT&CK Enterprise v15 | External reference | 14 tactics, 203 techniques, 453 sub-techniques |
| OWASP Top 10 2021 | External reference | Web application security risks |
| OWASP ASVS 5.0 | External reference | Application security verification standard |
| NIST SSDF v1.1 | External reference | Secure Software Development Framework |
| CIS Benchmarks v8 | External reference | Center for Internet Security configuration benchmarks |
| NIST SP 800-61 Rev. 2 | External reference | Computer Security Incident Handling Guide |
| SLSA v1.0 | External reference | Supply-chain Levels for Software Artifacts |

---

*Report Version: 1.0.0*
*Classification: C4 Critical Deliverable*
*Quality Threshold: >= 0.95*
*SSOT: ADR-PROJ010-001, ADR-PROJ010-006, FEAT-040*
*Created: 2026-02-22*
*Parent: FEAT-041 (EPIC-005 Purple Team Validation)*
