# B-001: MITRE ATT&CK Framework Analysis

> Stream B: Methodology Standards | PROJ-010 Cyber Ops | Phase 1 Research

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | High-level overview of ATT&CK and its relevance to /red-team |
| [L1: Key Findings](#l1-key-findings) | Structured findings on tactics, techniques, and tooling |
| [L2: Detailed Analysis](#l2-detailed-analysis) | Deep analysis of all 14 tactics, sub-techniques, Navigator, and tool mapping |
| [Agent Mapping](#agent-mapping) | How ATT&CK maps to specific /red-team agents |
| [Evidence and Citations](#evidence-and-citations) | Categorized, dated sources |
| [Recommendations](#recommendations) | Default methodology selections for /red-team |

---

## L0: Executive Summary

MITRE ATT&CK is the de facto global knowledge base of adversary tactics, techniques, and procedures (TTPs) based on real-world observations. The Enterprise matrix (version 18.1, December 2025) defines 14 tactics spanning the full attack lifecycle from Reconnaissance through Impact, encompassing 203 techniques and 453 sub-techniques. ATT&CK provides the structural backbone for the /red-team skill's methodology: every /red-team agent maps directly to one or more ATT&CK tactics, every offensive action is classifiable by ATT&CK technique ID, and the ATT&CK Navigator provides the visualization layer for engagement coverage mapping and detection gap analysis. The framework's STIX 2.1 data format enables programmatic integration, making it suitable for agentic automation.

---

## L1: Key Findings

### Finding 1: ATT&CK Provides Complete Kill Chain Coverage

The 14 tactics map cleanly to the /red-team engagement workflow defined in PLAN.md. Each tactic represents a distinct adversary objective, and the technique layer beneath provides the "how" for each objective. The framework is continuously updated with real-world threat intelligence, with version 18.1 (December 2025) adding enhanced guidance for software supply chains, cloud identities, and edge/virtualization systems.

### Finding 2: Sub-Technique Depth Is Critical for Agent Specialization

Sub-techniques provide the granularity needed for agent-level specialization. For example, Credential Access (TA0006) contains techniques like "OS Credential Dumping" (T1003) with 8 sub-techniques (LSASS Memory, SAM, DCSync, etc.), each requiring different tooling and methodology. This sub-technique depth directly informs what each /red-team agent must know and be capable of guiding.

### Finding 3: Tool-to-Technique Mapping Enables Realistic Engagement Planning

ATT&CK catalogues real-world software (both adversary tools and legitimate tools abused by adversaries) with technique mappings. Cobalt Strike (S0154) maps to over 30 techniques across all 14 tactics. Mimikatz maps primarily to Credential Access. This mapping is essential for /red-team agents that need to recommend and orchestrate tooling.

### Finding 4: ATT&CK Navigator Is the Standard Visualization Layer

The ATT&CK Navigator is a web-based annotation tool that enables layer-based visualization of technique coverage, detection gaps, and engagement scope. It supports custom layers for red team planning, blue team detection mapping, and gap analysis -- directly supporting the purple team validation workflow in EPIC-005.

### Finding 5: Top Techniques Reflect Current Threat Landscape

In 2025, the top 10 ATT&CK techniques accounted for 93% of observed malicious activity. T1055 Process Injection and T1059 Command and Scripting Interpreter lead, followed by T1486 Data Encrypted for Impact (ransomware), T1071 Application Layer Protocol (C2 and exfiltration), and T1555 Credentials from Password Stores (appearing in 29% of malware samples). These statistics should inform /red-team agent prioritization.

---

## L2: Detailed Analysis

### The 14 ATT&CK Tactics

The tactics are ordered by their position in the attack lifecycle. Each tactic has a unique ID (TA00XX) and contains multiple techniques.

| # | Tactic | ID | Description | Key Techniques (Examples) | Technique Count (approx.) |
|---|--------|----|-------------|---------------------------|--------------------------|
| 1 | **Reconnaissance** | TA0043 | Gathering information to plan future operations. Passive and active information collection before committing to an attack. | T1595 Active Scanning, T1592 Gather Victim Host Info, T1589 Gather Victim Identity Info, T1590 Gather Victim Network Info, T1591 Gather Victim Org Info, T1598 Phishing for Information | 10 |
| 2 | **Resource Development** | TA0042 | Establishing infrastructure and capabilities to support operations. Creating or acquiring tools, accounts, and infrastructure. | T1583 Acquire Infrastructure, T1586 Compromise Accounts, T1584 Compromise Infrastructure, T1587 Develop Capabilities, T1585 Establish Accounts, T1588 Obtain Capabilities | 8 |
| 3 | **Initial Access** | TA0001 | Techniques to gain a foothold in the target environment. The entry point for active exploitation. | T1566 Phishing, T1190 Exploit Public-Facing Application, T1133 External Remote Services, T1078 Valid Accounts, T1189 Drive-by Compromise, T1195 Supply Chain Compromise | 10 |
| 4 | **Execution** | TA0002 | Running malicious code on local or remote systems. The "doing things" tactic -- where payloads execute. | T1059 Command and Scripting Interpreter (PowerShell, Bash, Python, etc.), T1053 Scheduled Task/Job, T1047 Windows Management Instrumentation, T1204 User Execution, T1203 Exploitation for Client Execution | 14 |
| 5 | **Persistence** | TA0003 | Maintaining access across restarts, credential changes, or other interruptions. Ensuring continued presence. | T1547 Boot or Logon Autostart Execution, T1053 Scheduled Task/Job, T1136 Create Account, T1543 Create or Modify System Process, T1546 Event Triggered Execution, T1574 Hijack Execution Flow | 20 |
| 6 | **Privilege Escalation** | TA0004 | Gaining higher-level permissions. Moving from user to admin/root/SYSTEM. Often shares techniques with Persistence. | T1548 Abuse Elevation Control Mechanism, T1134 Access Token Manipulation, T1068 Exploitation for Privilege Escalation, T1055 Process Injection, T1078 Valid Accounts, T1547 Boot or Logon Autostart Execution | 14 |
| 7 | **Defense Evasion** | TA0005 | Avoiding detection throughout the operation. The largest tactic by technique count, reflecting the diversity of detection mechanisms. | T1070 Indicator Removal, T1036 Masquerading, T1027 Obfuscated Files or Information, T1055 Process Injection, T1218 System Binary Proxy Execution, T1562 Impair Defenses, T1112 Modify Registry | 43 |
| 8 | **Credential Access** | TA0006 | Stealing credentials -- passwords, tokens, tickets, hashes. The enabler for privilege escalation and lateral movement. | T1003 OS Credential Dumping, T1555 Credentials from Password Stores, T1110 Brute Force, T1557 Adversary-in-the-Middle, T1558 Steal or Forge Kerberos Tickets, T1552 Unsecured Credentials | 17 |
| 9 | **Discovery** | TA0007 | Learning about the environment -- systems, configurations, network layout, user accounts, services. Situational awareness. | T1087 Account Discovery, T1083 File and Directory Discovery, T1046 Network Service Discovery, T1057 Process Discovery, T1018 Remote System Discovery, T1082 System Information Discovery | 32 |
| 10 | **Lateral Movement** | TA0008 | Moving through the network to reach additional systems. Pivoting, tunneling, and remote execution. | T1021 Remote Services (RDP, SSH, SMB, WinRM), T1570 Lateral Tool Transfer, T1080 Taint Shared Content, T1563 Remote Service Session Hijacking, T1550 Use Alternate Authentication Material | 9 |
| 11 | **Collection** | TA0009 | Gathering data of interest -- files, emails, screenshots, keystrokes. Identifying and staging data for exfiltration. | T1560 Archive Collected Data, T1119 Automated Collection, T1005 Data from Local System, T1039 Data from Network Shared Drive, T1025 Data from Removable Media, T1074 Data Staged | 17 |
| 12 | **Command and Control** | TA0011 | Communication between compromised systems and attacker infrastructure. C2 channels, protocols, and evasion. | T1071 Application Layer Protocol, T1132 Data Encoding, T1001 Data Obfuscation, T1573 Encrypted Channel, T1105 Ingress Tool Transfer, T1571 Non-Standard Port, T1572 Protocol Tunneling | 17 |
| 13 | **Exfiltration** | TA0010 | Transferring collected data outside the target environment. The "getting data out" tactic. | T1041 Exfiltration Over C2 Channel, T1048 Exfiltration Over Alternative Protocol, T1567 Exfiltration Over Web Service, T1029 Scheduled Transfer, T1537 Transfer Data to Cloud Account | 9 |
| 14 | **Impact** | TA0040 | Disrupting availability or compromising integrity. Ransomware, destruction, defacement, resource hijacking. | T1486 Data Encrypted for Impact, T1485 Data Destruction, T1491 Defacement, T1499 Endpoint Denial of Service, T1496 Resource Hijacking, T1531 Account Access Removal | 14 |

**Total:** ~203 techniques, ~453 sub-techniques across Enterprise matrix.

### Engagement Phase Mapping

ATT&CK tactics map directly to engagement phases used in penetration testing:

| Engagement Phase | ATT&CK Tactics | /red-team Agent |
|------------------|----------------|-----------------|
| Pre-engagement / Planning | (Authorization controls -- outside ATT&CK) | red-lead |
| Reconnaissance | TA0043 Reconnaissance, TA0042 Resource Development | red-recon |
| Vulnerability Analysis | TA0043 Reconnaissance (active scanning), TA0007 Discovery | red-vuln |
| Initial Access / Exploitation | TA0001 Initial Access, TA0002 Execution | red-exploit |
| Privilege Escalation | TA0004 Privilege Escalation, TA0006 Credential Access | red-privesc |
| Lateral Movement | TA0008 Lateral Movement, TA0007 Discovery, TA0011 Command and Control | red-lateral |
| Persistence | TA0003 Persistence, TA0005 Defense Evasion | red-persist |
| Collection / Exfiltration | TA0009 Collection, TA0010 Exfiltration | red-exfil |
| Impact Assessment | TA0040 Impact | red-exploit (impact demonstration) |
| Reporting | (Reporting -- outside ATT&CK) | red-reporter |

### Sub-Technique Depth: Critical Tactics

The following tactics have the deepest sub-technique trees and are most critical for agent specialization:

**Defense Evasion (TA0005) -- 43 techniques, ~100+ sub-techniques:**
This is the largest tactic. Key sub-technique clusters:
- T1027 Obfuscated Files or Information: 12 sub-techniques (Binary Padding, Software Packing, Steganography, Compile After Delivery, Stripped Payloads, HTML Smuggling, Dynamic API Resolution, Embedded Payloads, Command Obfuscation, Fileless Storage, etc.)
- T1218 System Binary Proxy Execution: 14 sub-techniques (Rundll32, Regsvr32, CMSTP, InstallUtil, Mshta, Msiexec, Odbcconf, Regsvcs/Regasm, MMC, Mavinject, etc.)
- T1055 Process Injection: 12 sub-techniques (DLL Injection, PE Injection, Thread Execution Hijacking, Asynchronous Procedure Call, Thread Local Storage, Ptrace System Calls, Proc Memory, Extra Window Memory Injection, Process Hollowing, Process Doppelganging, VDSO Hijacking, ListPlanting)

**Credential Access (TA0006) -- 17 techniques, ~50+ sub-techniques:**
- T1003 OS Credential Dumping: 8 sub-techniques (LSASS Memory, SAM, NTDS, LSA Secrets, DCSync, Proc Filesystem, /etc/passwd and /etc/shadow, Cached Domain Credentials)
- T1558 Steal or Forge Kerberos Tickets: 4 sub-techniques (Golden Ticket, Silver Ticket, Kerberoasting, AS-REP Roasting)
- T1556 Modify Authentication Process: 6 sub-techniques (Domain Controller Authentication, Password Filter DLL, Pluggable Authentication Modules, Network Device Authentication, Reversible Encryption, Multi-Factor Authentication Interception)

**Persistence (TA0003) -- 20 techniques, ~80+ sub-techniques:**
- T1547 Boot or Logon Autostart Execution: 15 sub-techniques (Registry Run Keys, Authentication Packages, Time Providers, Winlogon Helper DLL, Security Support Provider, Kernel Modules and Extensions, Re-opened Applications, LSASS Driver, Shortcut Modification, Port Monitors, Plist Modification, Login Items, XDG Autostart Entries, Active Setup, Print Processors)
- T1546 Event Triggered Execution: 16 sub-techniques (Change Default File Association, Screensaver, WMI Event Subscription, Unix Shell Configuration Modification, Trap, LC_LOAD_DYLIB Addition, Netsh Helper DLL, Accessibility Features, AppCert DLLs, AppInit DLLs, Application Shimming, Image File Execution Options Injection, PowerShell Profile, Emond, Component Object Model Hijacking, Installer Packages)

### ATT&CK Navigator and Detection Mapping

**Purpose:** The ATT&CK Navigator is a web-based tool for annotating and exploring ATT&CK matrices.

**Red Team Use Cases:**
1. **Engagement Planning:** Create layers showing techniques in scope for the engagement. Annotate with priority, tool assignments, and agent responsibilities.
2. **Coverage Tracking:** During engagement, mark techniques as attempted, successful, or blocked. Track coverage completeness.
3. **Gap Analysis:** Compare red team coverage layer against blue team detection layer to identify detection gaps (purple team mode per FEAT-040).
4. **Threat Emulation:** Load APT group technique layers to emulate specific threat actors. ATT&CK catalogues over 140 APT groups with technique mappings.

**Detection Mapping:**
- Each technique in ATT&CK includes detection guidance: data sources, detection analytics, and log sources.
- Decider (companion tool) helps analysts map observed behaviors to ATT&CK techniques through guided questioning.
- Detection layers can be overlaid with red team engagement layers to calculate coverage percentages and identify blind spots.

**Integration with /red-team:**
- red-lead uses Navigator for engagement scoping and authorization mapping
- red-reporter uses Navigator layers to visualize findings
- Purple team validation (FEAT-040) uses dual-layer comparison (red coverage vs. blue detection)

### Red Team Tool-to-Technique Mapping

Major offensive tools are catalogued in ATT&CK as "Software" with technique mappings:

| Tool | ATT&CK ID | Technique Coverage | Primary Tactics |
|------|-----------|-------------------|-----------------|
| **Cobalt Strike** | S0154 | 30+ techniques across all 14 tactics | Execution, C2, Lateral Movement, Defense Evasion, Credential Access |
| **Metasploit** | S0081 | Modules implement techniques across all 14 tactics | Initial Access, Execution, Privilege Escalation, Post-Exploitation |
| **Mimikatz** | S0002 | 15+ techniques | Credential Access (primary), Privilege Escalation, Defense Evasion |
| **Empire** | S0363 | 25+ techniques | Execution, Persistence, Privilege Escalation, C2 |
| **Impacket** | S0357 | 12+ techniques | Credential Access, Lateral Movement, Execution |
| **BloodHound** | S0521 | 5+ techniques | Discovery (primary), Reconnaissance |
| **Nmap** | S0108 | 3+ techniques | Reconnaissance, Discovery |
| **CrackMapExec** | S0488 | 10+ techniques | Credential Access, Lateral Movement, Discovery, Execution |
| **PsExec** | S0029 | 5+ techniques | Execution, Lateral Movement |
| **Rubeus** | S0378 | 6+ techniques | Credential Access (Kerberos attacks) |

**Living-off-the-Land Binaries (LOLBins):**
ATT&CK also catalogues legitimate system binaries abused by adversaries:
- PowerShell (T1059.001) -- Execution, Defense Evasion
- cmd.exe (T1059.003) -- Execution
- certutil (T1140, T1105) -- Defense Evasion, Ingress Tool Transfer
- bitsadmin (T1197, T1105) -- Persistence, Ingress Tool Transfer
- wmic (T1047) -- Execution, Discovery
- rundll32 (T1218.011) -- Defense Evasion
- regsvr32 (T1218.010) -- Defense Evasion

### STIX 2.1 Data Format for Programmatic Access

ATT&CK data is distributed in STIX 2.1 JSON format via the `mitre-attack/attack-stix-data` repository (High reputation, 87.5 benchmark score on Context7). This enables:
- Programmatic querying of techniques, tactics, and their relationships
- Filtering techniques by tactic, platform, or data source
- Building automated engagement checklists
- Generating Navigator layers from engagement scope definitions

Key STIX object types:
- `attack-pattern` -- Techniques and sub-techniques
- `x-mitre-tactic` -- Tactics
- `x-mitre-matrix` -- Matrix definitions
- `malware` / `tool` -- Software entries with technique relationships
- `intrusion-set` -- Threat actor groups with technique relationships

---

## Agent Mapping

### /red-team Agent to ATT&CK Tactic Mapping

| Agent | Primary ATT&CK Tactics | Technique Responsibility | Key Techniques |
|-------|------------------------|--------------------------|----------------|
| **red-lead** | All (oversight) | Engagement scoping, methodology selection, ATT&CK Navigator layer management | Scope definition mapped to tactic coverage targets |
| **red-recon** | TA0043 Reconnaissance, TA0042 Resource Development | All Recon techniques, passive and active | T1595 Active Scanning, T1592-T1591 Gather Victim Info, T1598 Phishing for Information |
| **red-vuln** | TA0043 Reconnaissance (active), TA0007 Discovery | Vulnerability identification, CVE correlation, attack path analysis | T1595.002 Vulnerability Scanning, T1046 Network Service Discovery, T1518 Software Discovery |
| **red-exploit** | TA0001 Initial Access, TA0002 Execution | Exploit development and execution, payload delivery | T1190 Exploit Public-Facing App, T1566 Phishing, T1059 Command and Scripting Interpreter, T1203 Exploitation for Client Execution |
| **red-privesc** | TA0004 Privilege Escalation, TA0006 Credential Access | Local/domain privesc, credential harvesting | T1068 Exploitation for Privesc, T1003 OS Credential Dumping, T1558 Kerberos Tickets, T1548 Abuse Elevation Control |
| **red-lateral** | TA0008 Lateral Movement, TA0011 Command and Control, TA0007 Discovery | Pivoting, tunneling, C2, internal recon | T1021 Remote Services, T1071 Application Layer Protocol, T1572 Protocol Tunneling, T1570 Lateral Tool Transfer |
| **red-persist** | TA0003 Persistence, TA0005 Defense Evasion | Backdoor placement, detection evasion | T1547 Boot/Logon Autostart, T1053 Scheduled Task/Job, T1027 Obfuscated Files, T1562 Impair Defenses |
| **red-exfil** | TA0009 Collection, TA0010 Exfiltration | Data identification, staging, exfiltration | T1005 Data from Local System, T1560 Archive Collected Data, T1041 Exfil Over C2, T1567 Exfil Over Web Service |
| **red-reporter** | All (documentation) | Finding documentation with ATT&CK technique IDs, Navigator layer generation | Maps all findings to technique IDs with detection recommendations |

### Cross-Tactic Coverage Analysis

Several ATT&CK tactics span multiple agents:
- **Discovery (TA0007):** Shared between red-recon (external), red-vuln (vulnerability-focused), and red-lateral (internal). Each agent handles discovery within their operational phase.
- **Defense Evasion (TA0005):** While red-persist owns this primarily, ALL agents must be aware of evasion techniques relevant to their operational phase. red-exploit must evade endpoint detection; red-lateral must evade network detection.
- **Credential Access (TA0006):** Primarily red-privesc, but red-lateral may perform credential access during pivoting, and red-exploit may chain credential access with initial exploitation.

---

## Evidence and Citations

### Industry Leaders

| Source | Date | Content |
|--------|------|---------|
| [MITRE ATT&CK](https://attack.mitre.org/) | 2025-12 (v18.1) | Official ATT&CK Enterprise matrix, tactics, techniques, software catalogue |
| [MITRE ATT&CK Navigator](https://mitre-attack.github.io/attack-navigator/) | 2025 | Official web-based annotation and visualization tool |
| [MITRE ATT&CK STIX Data](https://github.com/mitre-attack/attack-stix-data) | 2025 | Official STIX 2.1 JSON data repository (Context7: High reputation, 87.5 benchmark) |
| [CISA Best Practices for MITRE ATT&CK Mapping](https://www.cisa.gov/sites/default/files/2023-01/Best%20Practices%20for%20MITRE%20ATTCK%20Mapping.pdf) | 2023-01 | US government guidance on ATT&CK mapping methodology |

### Industry Experts

| Source | Date | Content |
|--------|------|---------|
| [Picus Security -- Top Ten MITRE ATT&CK Techniques](https://www.picussecurity.com/resource/the-top-ten-mitre-attck-techniques) | 2025 | Analysis: top 10 techniques account for 93% of malicious activity |
| [CrowdStrike -- MITRE ATT&CK Framework](https://www.crowdstrike.com/en-us/cybersecurity-101/cyberattacks/mitre-attack-framework/) | 2025 | Industry perspective on ATT&CK usage in threat intelligence |
| [MITRE ATT&CK -- Cobalt Strike S0154](https://attack.mitre.org/software/S0154/) | 2025 | Official tool-to-technique mapping for Cobalt Strike |
| [Exabeam -- ATT&CK Navigator Use Cases](https://www.exabeam.com/explainers/mitre-attck/mitre-attck-navigator-use-cases-layers-and-how-to-get-started/) | 2025 | Navigator use cases for red/blue team operations |

### Industry Innovators

| Source | Date | Content |
|--------|------|---------|
| [Red Canary -- Atomic Red Team](https://github.com/redcanaryco/atomic-red-team) | 2025 | 8,425 test snippets mapped to ATT&CK (Context7: High reputation) |
| [MITRE Caldera](https://caldera.readthedocs.io/) | 2025 | Autonomous adversary emulation platform (Context7: High reputation, 66.1 benchmark) |
| [Vectra AI -- Cobalt Strike Detection](https://www.vectra.ai/topics/cobalt-strike) | 2025 | Detection engineering for Cobalt Strike mapped to ATT&CK |

### Community Experts

| Source | Date | Content |
|--------|------|---------|
| [Wiz -- MITRE ATT&CK Framework Guide](https://www.wiz.io/academy/detection-and-response/mitre-attack-framework) | 2025 | Comprehensive guide to 14 tactics with cloud context |
| [Splunk -- MITRE ATT&CK Complete Guide](https://www.splunk.com/en_us/blog/learn/mitre-attack.html) | 2025 | Guide to ATT&CK matrices, tactics, techniques |
| [Blake Strom / MITRE -- Getting Started with ATT&CK: Red Teaming](https://medium.com/mitre-attack/getting-started-with-attack-red-29f074ccf7e3) | 2019 | Foundational guide to red teaming with ATT&CK |

### Community Innovators

| Source | Date | Content |
|--------|------|---------|
| [Security Boulevard -- MITRE Revamps ATT&CK](https://securityboulevard.com/2025/11/cybersecurity-snapshot-ai-will-take-center-stage-in-cyber-in-2026-google-says-as-mitre-revamps-attck-framework/) | 2025-11 | ATT&CK v18 enhancements for supply chain, cloud, edge |
| [mitre-attack/mitreattack-python](https://github.com/mitre-attack/mitreattack-python) | 2025 | Python library for ATT&CK data manipulation (Context7: High reputation) |

---

## Recommendations

### R1: ATT&CK as the Primary Methodology Backbone

ATT&CK SHOULD be the primary taxonomy and classification system for all /red-team operations. Every technique executed during an engagement MUST be tagged with its ATT&CK technique ID (T-code). This enables:
- Consistent reporting across engagements
- Coverage measurement against the full matrix
- Detection gap analysis in purple team mode
- Threat emulation planning against specific APT groups

### R2: Navigator Layer Generation as a Core red-reporter Capability

red-reporter SHOULD generate ATT&CK Navigator layers as a standard engagement deliverable. Layers should include:
- Engagement scope layer (planned techniques)
- Execution coverage layer (techniques attempted and results)
- Detection gap layer (techniques that succeeded undetected)
- Remediation priority layer (techniques prioritized by business impact)

### R3: Sub-Technique Depth for Agent Knowledge Bases

Each /red-team agent SHOULD have deep knowledge of sub-techniques within their responsible tactics. Agent definitions should reference specific sub-technique IDs, not just parent techniques. This is critical for:
- red-privesc: Must know all 8 OS Credential Dumping sub-techniques, all 4 Kerberos attack sub-techniques
- red-persist: Must know all 15 Boot/Logon Autostart sub-techniques, all 16 Event Triggered Execution sub-techniques
- red-exploit: Must know all Command and Scripting Interpreter sub-techniques (PowerShell, Bash, Python, JavaScript, VBScript, etc.)

### R4: Atomic Red Team Integration for Technique Validation

The Atomic Red Team library (8,425 test snippets, Context7 High reputation) SHOULD be referenced as the standard technique validation resource. Each /red-team agent can reference Atomic Red Team tests for:
- Technique execution examples
- Detection validation
- Reproducible test cases

### R5: STIX Data Integration for Programmatic ATT&CK Access

The /red-team skill SHOULD leverage the ATT&CK STIX 2.1 data format for programmatic technique lookup, filtering, and relationship traversal. This enables:
- Automated engagement checklist generation from scope definitions
- Technique-to-tool mapping lookups
- APT group technique profile loading
- Detection data source identification

### R6: Defense Evasion as a Cross-Cutting Concern

Defense Evasion (TA0005) SHOULD NOT be isolated to red-persist alone. Every /red-team agent MUST incorporate relevant evasion techniques for their operational phase. This should be architected as a cross-cutting concern in the agent knowledge base, not a single-agent responsibility.
