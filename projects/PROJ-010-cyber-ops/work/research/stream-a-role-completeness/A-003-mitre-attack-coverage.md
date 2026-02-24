# A-003: MITRE ATT&CK Capability Coverage Analysis

> Stream A: Role Completeness | PROJ-010 Cyber Ops | Phase 1 Research

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | 3-5 sentence overview for any stakeholder |
| [L1: Key Findings](#l1-key-findings) | Structured findings by theme |
| [L2: Detailed Analysis](#l2-detailed-analysis) | Deep analysis with tables, comparisons, mappings |
| [Evidence and Citations](#evidence-and-citations) | All sources categorized by authority type |
| [Gap Analysis](#gap-analysis) | Tactics with zero or weak coverage |
| [Recommendations](#recommendations) | Specific agent roster or scope changes |

---

## L0: Executive Summary

Mapping all 14 MITRE ATT&CK Enterprise tactics to the proposed 9 /red-team agents reveals strong coverage for the mid-to-late kill chain (Execution through Exfiltration) but significant gaps in the pre-operational and support phases. Two tactics have zero direct agent coverage: Resource Development (TA0042 -- acquiring infrastructure, developing tools, staging capabilities) and Defense Evasion (TA0005 -- a 43-technique tactic that spans the entire engagement lifecycle). Two additional tactics have weak coverage: Reconnaissance (TA0043 -- partially covered by red-recon but missing social engineering reconnaissance), and Command and Control (TA0011 -- distributed across agents with no primary owner). The overall ATT&CK coverage rate is 10 of 14 tactics with strong coverage (71%), 2 with partial coverage (14%), and 2 with zero coverage (14%). These gaps directly align with the missing roles identified in A-002: the Resource Development gap maps to the proposed red-infra agent, and the Defense Evasion gap represents a cross-cutting concern that requires either a dedicated agent or explicit distribution across all operational agents.

---

## L1: Key Findings

### Finding 1: Resource Development (TA0042) Has Zero Coverage

Resource Development is the second tactic in the ATT&CK matrix (after Reconnaissance) and covers the adversary's pre-operational preparation: acquiring infrastructure (domains, servers, VPS), developing or acquiring capabilities (malware, exploits, tools), staging capabilities for deployment, compromising accounts for use in operations, and establishing digital identities. This is not a theoretical concern -- APT groups invest significant effort in Resource Development before any target interaction occurs.

The proposed /red-team has no agent whose primary responsibility is acquiring, configuring, and managing the infrastructure and tooling that operators need. red-exploit touches on "payload crafting" and red-lateral mentions "C2 infrastructure," but the systematic preparation of operational infrastructure, domains, certificates, accounts, and tools is unowned.

This gap directly validates the A-002 recommendation for a **red-infra** agent.

### Finding 2: Defense Evasion (TA0005) Has Zero Primary Coverage

Defense Evasion is the largest tactic in the ATT&CK framework with 43 techniques and numerous sub-techniques. It spans the entire engagement lifecycle -- adversaries need to evade detection during every phase from Initial Access through Exfiltration. Techniques include: process injection, obfuscation, rootkit deployment, indicator removal, signed binary proxy execution, access token manipulation, BITS jobs, DLL side-loading, and dozens more.

The proposed /red-team distributes evasion implicitly: red-persist mentions "detection evasion analysis" and red-lateral implies some evasion. But Defense Evasion is the single largest collection of techniques in the entire framework and has no primary owner. In real engagements, evasion is the difference between a successful operation and an early detection -- it deserves dedicated expertise or explicit distribution with clear accountability.

### Finding 3: Command and Control (TA0011) Lacks Primary Ownership

Command and Control covers how adversaries communicate with compromised systems: application layer protocols, encrypted channels, multi-stage channels, domain fronting, DNS tunneling, traffic signaling, and more. red-lateral's description mentions "C2 infrastructure" as one of several responsibilities, but C2 architecture, channel selection, protocol configuration, and communication resilience are a full specialization in real red team operations.

SANS SEC565 dedicates significant attention to C2 infrastructure. Outflank built an entire product (Outflank C2) specifically for OPSEC-focused command and control. Bishop Fox's 2025 tools guide specifically covers C2 frameworks as a distinct category. The complexity of modern C2 (multi-hop, domain fronting, cloud C2, P2P C2) exceeds what can be a secondary responsibility of a lateral movement agent.

### Finding 4: Reconnaissance Coverage is Partial

red-recon covers "OSINT, network enumeration, service discovery, technology fingerprinting, attack surface mapping" -- these map well to the technical reconnaissance techniques in ATT&CK (Active Scanning, Search Open Domains/Websites, Gather Victim Network/Host/Identity Information). However, ATT&CK Reconnaissance also includes techniques that require social engineering context: Phishing for Information (T1598), Gather Victim Org Information (T1591), and Search Closed Sources (T1597).

Without a social engineering specialist (recommended in A-002), social reconnaissance techniques lack coverage. red-recon handles technical reconnaissance well but social/organizational reconnaissance is a gap.

### Finding 5: Strong Coverage Exists for Core Operational Tactics

The proposed roster provides strong coverage for the 6 core operational tactics that form the heart of most engagements: Execution (red-exploit), Persistence (red-persist), Privilege Escalation (red-privesc), Credential Access (red-privesc), Lateral Movement (red-lateral), and Collection + Exfiltration (red-exfil). These agents map well to their respective ATT&CK tactics, and the kill-chain-based decomposition is well-suited for these middle phases.

### Finding 6: Impact (TA0040) Has Ambiguous Coverage

Impact covers adversary actions intended to disrupt, destroy, or manipulate systems and data: data destruction, defacement, disk wipe, endpoint denial of service, firmware corruption, inhibit system recovery, resource hijacking, and service stop. The proposed /red-team has no agent explicitly responsible for impact assessment. red-exploit could potentially cover impact techniques, but "proof-of-concept development" differs from "impact demonstration."

In real red team engagements, demonstrating potential impact (without causing actual damage) is critical for communicating risk to stakeholders. This function is partially covered by red-reporter (documenting impact) but the technical execution of impact assessment has no clear owner.

---

## L2: Detailed Analysis

### Complete Tactic-to-Agent Mapping

The following table maps each of the 14 MITRE ATT&CK Enterprise tactics to the proposed /red-team agents, with coverage assessment.

| # | Tactic ID | Tactic Name | Key Techniques (examples) | Primary Agent | Supporting Agents | Coverage Rating |
|---|-----------|-------------|--------------------------|---------------|-------------------|-----------------|
| 1 | TA0043 | Reconnaissance | Active Scanning, Search Open Technical Databases, Gather Victim Host/Network/Identity/Org Info, Phishing for Information | **red-recon** | red-vuln (tech fingerprinting) | PARTIAL -- technical recon strong, social recon gap |
| 2 | TA0042 | Resource Development | Acquire Infrastructure, Compromise Accounts, Develop Capabilities, Obtain Capabilities, Stage Capabilities | **NONE** | red-exploit (payload), red-lateral (C2 -- partial) | ZERO -- no agent owns pre-operational infrastructure/tooling |
| 3 | TA0001 | Initial Access | Phishing, Exploit Public-Facing Application, Valid Accounts, Supply Chain Compromise, Drive-by Compromise | **red-exploit** | red-recon (targeting), red-vuln (vuln identification) | STRONG |
| 4 | TA0002 | Execution | Command and Scripting Interpreter, Exploitation for Client Execution, System Services, User Execution, WMI | **red-exploit** | red-privesc (execution context), red-lateral (remote execution) | STRONG |
| 5 | TA0003 | Persistence | Boot/Logon Autostart, Create Account, Scheduled Task/Job, Server Software Component, Implant Internal Image | **red-persist** | red-privesc (elevated persistence) | STRONG |
| 6 | TA0004 | Privilege Escalation | Exploitation for Privilege Escalation, Access Token Manipulation, Process Injection, Valid Accounts, Abuse Elevation Control | **red-privesc** | red-exploit (exploit dev support) | STRONG |
| 7 | TA0005 | Defense Evasion | Obfuscated Files, Process Injection, Indicator Removal, Signed Binary Proxy Execution, Access Token Manipulation, Rootkits, BITS Jobs, DLL Side-Loading | **NONE** | red-persist (evasion analysis -- secondary), red-lateral (evasion during movement -- implicit) | ZERO -- 43 techniques, largest tactic, no primary owner |
| 8 | TA0006 | Credential Access | Brute Force, Credential Dumping, Input Capture, Kerberoasting, LLMNR/NBT-NS Poisoning, Steal Application Access Token | **red-privesc** | red-lateral (credential use during movement) | STRONG |
| 9 | TA0007 | Discovery | Account Discovery, Network Service Discovery, System Information Discovery, Permission Groups Discovery, Remote System Discovery | **red-recon** | red-lateral (internal discovery), red-privesc (privilege discovery) | STRONG |
| 10 | TA0008 | Lateral Movement | Remote Services, Exploitation of Remote Services, Internal Spearphishing, Lateral Tool Transfer, Taint Shared Content | **red-lateral** | red-exploit (exploitation support), red-privesc (credential use) | STRONG |
| 11 | TA0009 | Collection | Data from Local System, Data from Network Shared Drive, Screen Capture, Clipboard Data, Email Collection, Audio/Video Capture | **red-exfil** | red-recon (target identification), red-lateral (access to collection sources) | STRONG |
| 12 | TA0011 | Command and Control | Application Layer Protocol, Encrypted Channel, Proxy, Multi-Stage Channels, Domain Fronting, DNS Tunneling, Traffic Signaling | **red-lateral** (partial -- "C2 infrastructure" listed) | red-persist (comms with persistent implants), red-exfil (C2 for exfil) | WEAK -- C2 is a secondary responsibility of red-lateral, not primary |
| 13 | TA0010 | Exfiltration | Exfiltration Over C2 Channel, Over Alternative Protocol, Over Web Service, Automated Exfiltration, Physical Medium, Scheduled Transfer | **red-exfil** | red-lateral (channel setup) | STRONG |
| 14 | TA0040 | Impact | Data Destruction, Data Encrypted for Impact, Defacement, Disk Wipe, Endpoint DoS, Firmware Corruption, Resource Hijacking, Service Stop | **NONE** (ambiguous) | red-exploit (technical execution -- potential), red-reporter (impact documentation) | WEAK -- impact demonstration has no clear primary owner |

### Coverage Summary

| Coverage Rating | Count | Tactics | Percentage |
|-----------------|-------|---------|------------|
| STRONG | 8 | Initial Access, Execution, Persistence, Privilege Escalation, Credential Access, Discovery, Lateral Movement, Exfiltration | 57% |
| PARTIAL | 2 | Reconnaissance, Collection | 14% |
| WEAK | 2 | Command and Control, Impact | 14% |
| ZERO | 2 | Resource Development, Defense Evasion | 14% |

### Technique Density Analysis

Understanding the relative size and complexity of each tactic provides context for coverage gaps.

| Tactic | Technique Count (approx) | Sub-Technique Count (approx) | Gap Severity Context |
|--------|-------------------------|-----------------------------|--------------------|
| Reconnaissance | 10 | 30+ | Partial coverage acceptable -- most techniques covered by red-recon |
| Resource Development | 7 | 14 | ZERO coverage on 7 techniques is a significant gap |
| Initial Access | 9 | 12 | Strong coverage |
| Execution | 14 | 19 | Strong coverage |
| Persistence | 19 | 79 | Strong coverage via dedicated red-persist |
| Privilege Escalation | 13 | 37 | Strong coverage via dedicated red-privesc |
| **Defense Evasion** | **43** | **112** | **ZERO coverage on the LARGEST tactic in the framework -- critical gap** |
| Credential Access | 17 | 47 | Strong coverage via red-privesc |
| Discovery | 32 | 11 | Strong coverage via red-recon |
| Lateral Movement | 9 | 12 | Strong coverage via dedicated red-lateral |
| Collection | 17 | 18 | Strong coverage via red-exfil |
| Command and Control | 16 | 27 | Weak coverage -- distributed, no primary owner |
| Exfiltration | 9 | 7 | Strong coverage via dedicated red-exfil |
| Impact | 14 | 9 | Weak coverage -- no clear primary owner |

**Total Enterprise Matrix**: 203 techniques, 453 sub-techniques (as of 2025 data).

### Defense Evasion Deep Dive

Defense Evasion (TA0005) warrants special attention due to its size (43 techniques, 112 sub-techniques) and the complete absence of a primary owning agent.

| Technique Category | Example Techniques | Would Need Agent |
|-------------------|-------------------|-----------------|
| Code Obfuscation | Obfuscated Files or Information (T1027), Software Packing (T1027.002) | red-infra (tool preparation) |
| Process Manipulation | Process Injection (T1055), DLL Side-Loading (T1574.002), Process Hollowing (T1055.012) | red-exploit or red-persist |
| Credential/Token Manipulation | Access Token Manipulation (T1134), Steal or Forge Kerberos Tickets (T1558) | red-privesc |
| Indicator Removal | Indicator Removal (T1070), Clear Windows Event Logs (T1070.001), File Deletion (T1070.004) | red-persist (cleanup) |
| Execution Guardrails | Execution Guardrails (T1480), Environmental Keying (T1480.001) | red-infra (tool design) |
| Signed Execution | Signed Binary Proxy Execution (T1218), Rundll32 (T1218.011), Mshta (T1218.005) | red-exploit or red-lateral |
| Rootkits and Firmware | Rootkits (T1014), Firmware Corruption (for evasion) | red-persist |
| Network Evasion | Traffic Signaling (T1205), Domain Fronting (T1090.004), Protocol Tunneling (T1572) | red-lateral (C2 evasion) |
| Virtualization/Sandbox Evasion | Virtualization/Sandbox Evasion (T1497), System Checks (T1497.001), Time-Based Evasion (T1497.003) | red-infra (tool design) |

**Key Insight**: Defense Evasion techniques cut across every operational phase. They are needed during exploitation (obfuscation), persistence (rootkits, indicator removal), lateral movement (network evasion), privilege escalation (token manipulation), and exfiltration (traffic hiding). This cross-cutting nature means either: (a) every operational agent needs explicit evasion competency, or (b) a dedicated agent owns evasion strategy and advises operational agents.

### Command and Control Deep Dive

| Technique | Description | Current Coverage |
|-----------|-------------|-----------------|
| Application Layer Protocol (T1071) | Web, DNS, Mail protocols for C2 | red-lateral (implicit) |
| Encrypted Channel (T1573) | Symmetric/asymmetric encryption for C2 | Nowhere explicitly |
| Multi-Stage Channels (T1104) | Separate channels for different stages | Nowhere explicitly |
| Proxy (T1090) | External proxy, multi-hop proxy, domain fronting | red-lateral (implicit) |
| Non-Application Layer Protocol (T1095) | Raw sockets, custom protocols | Nowhere explicitly |
| Data Encoding (T1132) | Standard/non-standard encoding for C2 | Nowhere explicitly |
| Dynamic Resolution (T1568) | Fast flux, DGA, DNS calculation | Nowhere explicitly |
| Ingress Tool Transfer (T1105) | Download tools post-compromise | red-lateral (tool transfer mentioned) |
| Non-Standard Port (T1571) | Using unusual ports for C2 | Nowhere explicitly |
| Remote Access Software (T1219) | Using legitimate remote tools | Nowhere explicitly |
| Traffic Signaling (T1205) | Wake-on-LAN, port knocking | Nowhere explicitly |
| Web Service (T1102) | Dead drops, bidirectional via web services | Nowhere explicitly |

**Key Insight**: Of the 16 C2 techniques, only 2-3 are implicitly covered by red-lateral. The remaining 12-13 techniques have no explicit coverage. C2 architecture is a deep specialization that includes protocol selection, encryption implementation, infrastructure design, resilience against takedown, and OPSEC hardening.

### Impact Tactic Deep Dive

| Technique | Description | Current Coverage |
|-----------|-------------|-----------------|
| Account Access Removal (T1531) | Lock legitimate users out | Nowhere explicitly |
| Data Destruction (T1485) | Delete/overwrite data | Nowhere explicitly |
| Data Encrypted for Impact (T1486) | Ransomware-style encryption | Nowhere explicitly |
| Data Manipulation (T1565) | Modify data at rest or in transit | Nowhere explicitly |
| Defacement (T1491) | Internal/external defacement | Nowhere explicitly |
| Disk Wipe (T1561) | Disk structure/content wipe | Nowhere explicitly |
| Endpoint Denial of Service (T1499) | Application/OS/network DoS | Nowhere explicitly |
| Firmware Corruption (T1495) | BIOS/UEFI corruption | Nowhere explicitly |
| Inhibit System Recovery (T1490) | Delete backups, disable recovery | Nowhere explicitly |
| Network Denial of Service (T1498) | Direct/reflected amplification | Nowhere explicitly |
| Resource Hijacking (T1496) | Cryptojacking, compute theft | Nowhere explicitly |
| Service Stop (T1489) | Stop critical services | Nowhere explicitly |
| System Shutdown/Reboot (T1529) | Forced shutdown/reboot | Nowhere explicitly |
| Financial Theft (T1657) | Unauthorized fund transfer | Nowhere explicitly |

**Key Insight**: None of the 14 Impact techniques have explicit agent coverage. In ethical red team engagements, impact is typically demonstrated safely (e.g., showing that ransomware COULD encrypt files without actually encrypting them). This "impact assessment" function is valuable for communicating risk to stakeholders and belongs naturally to either red-exploit (technical capability to demonstrate impact) or red-reporter (impact documentation and risk communication).

---

## Evidence and Citations

### Industry Leaders

| Source | Date | URL | Content |
|--------|------|-----|---------|
| MITRE ATT&CK Enterprise Matrix | 2025 | [attack.mitre.org](https://attack.mitre.org/) | Authoritative source for all 14 tactics, 203 techniques, 453 sub-techniques |
| MITRE ATT&CK -- Collection (TA0009) | 2025 | [attack.mitre.org](https://attack.mitre.org/tactics/TA0009/) | Collection tactic definition and techniques |
| MITRE ATT&CK -- Exfiltration (TA0010) | 2025 | [attack.mitre.org](https://attack.mitre.org/tactics/TA0010/) | Exfiltration tactic definition, 9 techniques including C2 channel, alternative protocol, web service, cloud storage |
| MITRE ATT&CK -- Exfiltration Over C2 (T1041) | 2025 | [attack.mitre.org](https://attack.mitre.org/techniques/T1041/) | Exfiltration over existing C2 channel |
| MITRE ATT&CK -- Exfiltration Over Alt Protocol (T1048) | 2025 | [attack.mitre.org](https://attack.mitre.org/techniques/T1048/) | FTP, SMTP, HTTP/S, DNS, SMB exfiltration |
| MITRE ATT&CK -- Exfiltration Over Web Service (T1567) | 2025 | [attack.mitre.org](https://attack.mitre.org/techniques/T1567/) | Cloud storage exfiltration (Dropbox, Google Docs) |
| MITRE ATT&CK -- Exfiltration to Cloud Storage (T1567.002) | 2025 | [attack.mitre.org](https://attack.mitre.org/techniques/T1567/002/) | Sub-technique: cloud storage as exfil target |
| MITRE ATT&CK -- Exfiltration Over Other Medium (T1011) | 2025 | [attack.mitre.org](https://attack.mitre.org/techniques/T1011/) | WiFi, modem, cellular, Bluetooth, RF exfiltration |
| MITRE ATT&CK -- Automated Exfiltration (T1020) | 2025 | [attack.mitre.org](https://attack.mitre.org/techniques/T1020/) | Automated data collection and exfiltration |
| MITRE ATT&CK -- Adversary Emulation Plans | 2025 | [attack.mitre.org](https://attack.mitre.org/resources/adversary-emulation-plans/) | Official adversary emulation resources for red teams |
| MITRE ATT&CK -- ATT&CK Data and Tools | 2025 | [attack.mitre.org](https://attack.mitre.org/resources/attack-data-and-tools/) | ATT&CK Navigator, data resources |

### Industry Experts

| Source | Date | URL | Content |
|--------|------|-----|---------|
| CISA -- Best Practices for MITRE ATT&CK Mapping | 2023 | [cisa.gov](https://www.cisa.gov/sites/default/files/2023-01/Best%20Practices%20for%20MITRE%20ATTCK%20Mapping.pdf) | Official US government guidance on ATT&CK mapping methodology |
| CISA -- ATT&CK Mapping Best Practices (alternate) | 2023 | [cisa.gov](https://www.cisa.gov/sites/default/files/publications/Best%20Practices%20for%20MITRE%20ATTCK%20Mapping.pdf) | Additional CISA mapping guidance |
| Picus Security -- MITRE ATT&CK Framework Guide | 2025 | [picussecurity.com](https://www.picussecurity.com/mitre-attack-framework) | Comprehensive ATT&CK guide with tactics, techniques coverage |
| CyberDefenders -- MITRE ATT&CK for SOC and DFIR | 2025 | [cyberdefenders.org](https://cyberdefenders.org/blog/mitre-attack-framework/) | Complete field guide for mapping alerts and investigations |
| SANS SEC565 | 2025 | [sans.org](https://www.sans.org/cyber-security-courses/red-team-operations-adversary-emulation) | Red Team Operations course covering ATT&CK-based methodology |

### Industry Innovators

| Source | Date | URL | Content |
|--------|------|-----|---------|
| Wiz -- MITRE ATT&CK Framework Guide | 2025 | [wiz.io](https://www.wiz.io/academy/detection-and-response/mitre-attack-framework) | Tactics overview, 203 techniques, 453 sub-techniques |
| Palo Alto Networks -- MITRE ATT&CK Matrix | 2025 | [paloaltonetworks.com](https://www.paloaltonetworks.com/cyberpedia/what-is-mitre-attack-matrix) | Matrix structure, Navigator tool |
| Palo Alto Networks -- MITRE ATT&CK | 2025 | [paloaltonetworks.com](https://www.paloaltonetworks.com/cyberpedia/what-is-mitre-attack) | Framework overview, use cases |
| Hexnode -- MITRE ATT&CK Framework Guide | 2025 | [hexnode.com](https://www.hexnode.com/blogs/mitre-attack-framework/) | Complete framework guide |
| BitSight -- MITRE ATT&CK Components | 2025 | [bitsight.com](https://www.bitsight.com/blog/mitre-attack-framework) | Key framework components |
| Bishop Fox -- 2025 Red Team Tools | 2025 | [bishopfox.com](https://bishopfox.com/blog/2025-red-team-tools-c2-frameworks-active-directory-network-exploitation) | C2 frameworks, AD tools, network exploitation tools |
| Outflank -- OPSEC-Focused C2 | 2025 | [outflank.nl](https://www.outflank.nl/products/outflank-security-tooling/outflank-c2/) | OPSEC-focused C2 purpose-built for red teams |

### Community Leaders

| Source | Date | URL | Content |
|--------|------|-----|---------|
| CrowdStrike -- MITRE ATT&CK Framework | 2025 | [crowdstrike.com](https://www.crowdstrike.com/en-us/cybersecurity-101/cyberattacks/mitre-attack-framework/) | Framework overview, red team usage |
| Exabeam -- MITRE ATT&CK Explainer | 2025 | [exabeam.com](https://www.exabeam.com/explainers/mitre-attck/what-is-mitre-attck-an-explainer/) | Detailed ATT&CK explanation |
| Aujas -- ATT&CK Approach for Red Team Sims | 2025 | [blog.aujas.com](https://blog.aujas.com/the-mitre-attck-approach-for-effective-red-team-simulations) | ATT&CK-based red team simulation methodology |
| StartupDefense -- Comprehensive ATT&CK Tactics Guide | 2025 | [startupdefense.io](https://www.startupdefense.io/blog/comprehensive-guide-to-att-ck-tactics-the-mitre-framework) | Guide to all ATT&CK tactics |

### Community Experts

| Source | Date | URL | Content |
|--------|------|-----|---------|
| MITRE ATT&CK Blog -- Getting Started with Red Teaming | 2025 | [medium.com/mitre-attack](https://medium.com/mitre-attack/getting-started-with-attack-red-29f074ccf7e3) | ATT&CK-based red team methodology guide |
| Parrot CTFs -- Red Team Infrastructure | 2025 | [parrot-ctfs.com](https://parrot-ctfs.com/blog/red-team-infrastructure-complete-guide-to-setup-and-best-practices-in-2025/) | Infrastructure setup covering C2, redirectors, OPSEC |
| Mindgard -- Red Team Operations Phases | 2025 | [mindgard.ai](https://mindgard.ai/blog/red-team-operations-phases-of-engagement) | 5 phases of red team engagement with ATT&CK mapping |

### Community Innovators

| Source | Date | URL | Content |
|--------|------|-----|---------|
| DataDog -- Stratus Red Team | 2025 | [github.com](https://github.com/DataDog/stratus-red-team) | Cloud-focused adversary emulation with ATT&CK mapping |

---

## Gap Analysis

### Coverage Gaps by Severity

| Gap | Tactic | Severity | Technique Count | Impact |
|-----|--------|----------|-----------------|--------|
| **Defense Evasion -- ZERO coverage** | TA0005 | CRITICAL | 43 techniques, 112 sub-techniques | Defense Evasion is the largest tactic and cuts across every operational phase. Without evasion capability, all other red team operations are detectible. In real engagements, evasion is the primary differentiator between a "pentest" and a "red team operation." |
| **Resource Development -- ZERO coverage** | TA0042 | HIGH | 7 techniques, 14 sub-techniques | Pre-operational infrastructure and tooling preparation has no owner. Operators cannot conduct engagements without infrastructure (C2 servers, domains, tools, accounts). This directly maps to the missing red-infra agent from A-002. |
| **Command and Control -- WEAK coverage** | TA0011 | MEDIUM-HIGH | 16 techniques, 27 sub-techniques | C2 architecture, protocol selection, encryption, resilience, and OPSEC are secondary to red-lateral's primary mission of lateral movement. Only 2-3 of 16 techniques have implicit coverage. This gap exacerbates the Defense Evasion gap since C2 OPSEC is a form of evasion. |
| **Impact -- WEAK coverage** | TA0040 | MEDIUM | 14 techniques, 9 sub-techniques | Impact demonstration (safe simulation of destructive capabilities) has no clear owner. red-reporter documents findings but cannot technically demonstrate impact scenarios. Red team engagements gain credibility by demonstrating "what could happen" -- this requires technical capability. |
| **Reconnaissance -- PARTIAL** | TA0043 | LOW-MEDIUM | 10 techniques, 30+ sub-techniques | Social reconnaissance techniques (Phishing for Information, Gather Victim Org Info) lack coverage due to missing social engineering agent. Technical reconnaissance is well covered by red-recon. |

### Cross-Cutting Coverage Pattern

Several ATT&CK tactics are "cross-cutting" -- they apply throughout the engagement rather than at a single phase. The kill-chain-based agent decomposition handles phase-specific tactics well but struggles with cross-cutting concerns:

| Cross-Cutting Tactic | Nature | Problem |
|----------------------|--------|---------|
| Defense Evasion | Needed during EVERY operational phase | No single phase-based agent can own this |
| Command and Control | Active from Initial Access through Exfiltration | Assigned as secondary to red-lateral but needed by red-persist, red-exfil, red-privesc |
| Resource Development | Pre-operational, supports ALL subsequent phases | No phase-based agent covers pre-operational work |
| Discovery | Ongoing throughout engagement, not just during recon | red-recon is the natural owner but Discovery happens during lateral movement and privilege escalation too |

---

## Recommendations

### Recommendation 1: Address Resource Development Gap with red-infra Agent

**Priority**: HIGH
**Action**: Add red-infra agent (aligned with A-002 recommendation) with explicit MITRE ATT&CK TA0042 coverage.

| TA0042 Technique | red-infra Responsibility |
|-----------------|--------------------------|
| Acquire Infrastructure (T1583) | Domain registration, VPS provisioning, cloud infrastructure, DNS configuration |
| Compromise Accounts (T1586) | Operational accounts for social media, email, cloud services |
| Develop Capabilities (T1587) | Custom malware, exploit development, self-signed certificates |
| Obtain Capabilities (T1588) | Tool acquisition, exploit sourcing, digital certificates |
| Stage Capabilities (T1608) | Upload capabilities to infrastructure, configure distribution points |
| Compromise Infrastructure (T1584) | Leveraging compromised third-party infrastructure |
| Establish Accounts (T1585) | Creating accounts with email providers, social media |

### Recommendation 2: Address Defense Evasion as a Cross-Cutting Concern

**Priority**: CRITICAL
**Action**: Two options, recommend Option A.

**Option A (Recommended): Explicit evasion competency in every operational agent + red-infra as evasion tooling owner.**

Distribute Defense Evasion techniques to the agents that need them most:

| Agent | Defense Evasion Techniques Assigned |
|-------|-------------------------------------|
| red-infra (NEW) | Obfuscation, packing, execution guardrails, sandbox evasion (tool-level evasion built into payloads and infrastructure) |
| red-exploit | Process injection, signed binary proxy execution (execution-time evasion) |
| red-privesc | Access token manipulation, credential-based evasion |
| red-persist | Indicator removal, rootkits, timestomping (persistence evasion) |
| red-lateral | Network evasion, traffic signaling, protocol tunneling (movement evasion) |
| red-exfil | Data encoding, encrypted channels for exfil (exfiltration evasion) |

**Option B (Alternative): Dedicated red-evasion agent.**

A standalone agent that advises all operational agents on evasion techniques and owns the evasion strategy for the engagement. Risk: creates handoff overhead and may slow operations.

### Recommendation 3: Strengthen C2 Coverage

**Priority**: MEDIUM-HIGH
**Action**: Assign Command and Control (TA0011) as a primary responsibility of red-infra rather than a secondary responsibility of red-lateral.

| Function | Current Owner | Recommended Owner |
|----------|--------------|-------------------|
| C2 architecture design | red-lateral (secondary) | red-infra (primary) |
| C2 protocol selection | Unowned | red-infra |
| C2 encryption and OPSEC | Unowned | red-infra |
| C2 infrastructure resilience | Unowned | red-infra |
| C2 usage during operations | N/A | red-lateral, red-persist, red-exfil (consumers) |

This separates C2 infrastructure (design, build, maintain -- red-infra) from C2 usage (operational communication -- operational agents).

### Recommendation 4: Clarify Impact Coverage

**Priority**: MEDIUM
**Action**: Expand red-exploit's scope to explicitly include safe impact demonstration, OR assign impact techniques to red-reporter as "impact assessment and documentation."

Recommended approach: Split Impact between two agents:
- **red-exploit**: Technical impact demonstration capability (safe simulation of data destruction, ransomware, DoS)
- **red-reporter**: Impact risk documentation, stakeholder communication of impact potential, remediation urgency scoring

### Recommendation 5: Strengthen Social Reconnaissance

**Priority**: LOW-MEDIUM (dependent on A-002 red-social recommendation)
**Action**: If red-social is added per A-002, assign social reconnaissance techniques (T1591, T1597, T1598) as a shared responsibility between red-recon (technical context) and red-social (social/organizational context).

### Summary: ATT&CK Coverage After Recommendations

| Tactic | Coverage Before | Coverage After | Change |
|--------|-----------------|---------------|--------|
| Reconnaissance (TA0043) | PARTIAL | STRONG | red-social covers social recon |
| Resource Development (TA0042) | ZERO | STRONG | red-infra owns entirely |
| Initial Access (TA0001) | STRONG | STRONG | No change |
| Execution (TA0002) | STRONG | STRONG | No change |
| Persistence (TA0003) | STRONG | STRONG | No change |
| Privilege Escalation (TA0004) | STRONG | STRONG | No change |
| Defense Evasion (TA0005) | ZERO | STRONG | Distributed across agents with red-infra as tooling owner |
| Credential Access (TA0006) | STRONG | STRONG | No change |
| Discovery (TA0007) | STRONG | STRONG | No change |
| Lateral Movement (TA0008) | STRONG | STRONG | No change |
| Collection (TA0009) | STRONG | STRONG | No change |
| Command and Control (TA0011) | WEAK | STRONG | red-infra as primary C2 infrastructure owner |
| Exfiltration (TA0010) | STRONG | STRONG | No change |
| Impact (TA0040) | WEAK | STRONG | Split between red-exploit (demonstration) and red-reporter (documentation) |

**Overall coverage improvement**: From 57% STRONG (8/14) to 100% STRONG (14/14) with the addition of 2 agents (red-infra, red-social) and structural adjustments to existing agents.
