# /red-team User Guide

> Offensive security methodology guidance through 11 specialized agents covering the full MITRE ATT&CK kill chain for authorized penetration testing and red team engagements.

**Version:** 1.0.0 | **Skill:** /red-team | **Last Updated:** 2026-02-22
**SSOT:** ADR-PROJ010-001 (Agent Team Architecture), ADR-PROJ010-006 (Authorization & Scope Control)

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Quick Start](#l0-quick-start) | Get started with your first engagement |
| [Skill Overview](#skill-overview) | What /red-team does, what it does not do, and when to use it |
| [Agent Registry](#agent-registry) | All 11 agents with capabilities, ATT&CK mapping, and authorization levels |
| [Choosing the Right Agent](#choosing-the-right-agent) | Decision table for agent selection |
| [L1: Engagement Workflow](#l1-engagement-workflow) | End-to-end penetration testing scenario |
| [Authorization Procedures](#authorization-procedures) | Scope documents, Rules of Engagement, and the authorization flow |
| [How to Invoke Agents](#how-to-invoke-agents) | Three invocation methods |
| [The Kill Chain Workflow](#the-kill-chain-workflow) | Non-linear workflow with phase cycling |
| [RoE-Gated Agents](#roe-gated-agents) | Special authorization for persistence, exfiltration, and social engineering |
| [Output Levels](#output-levels) | Understanding L0, L1, L2 output |
| [L2: Advanced Configuration](#l2-advanced-configuration) | Authorization architecture, methodology frameworks, integration points |
| [Authorization Architecture](#authorization-architecture) | Three-layer defense-in-depth model |
| [Methodology Reference](#methodology-reference) | PTES, OSSTMM, MITRE ATT&CK mapping |
| [Integration Points](#integration-points) | Working with /eng-team, /adversary, /problem-solving, /nasa-se |
| [Reporting Format](#reporting-format) | Finding documentation and engagement report structure |
| [Common Scenarios](#common-scenarios) | Real-world engagement patterns |
| [Troubleshooting and FAQ](#troubleshooting-and-faq) | Common issues and solutions |
| [References](#references) | Standards, ADRs, and source material |

---

## L0: Quick Start

### What Is /red-team?

The /red-team skill provides **methodology guidance for authorized penetration testing and red team engagements**. It routes to 11 specialized agents that collectively cover the full MITRE ATT&CK kill chain (14 out of 14 tactics at STRONG coverage level).

The skill produces methodology guidance, structured analysis, and engagement reports. It does NOT execute exploits autonomously, access live systems directly, or generate weaponized exploit code. Agents guide practitioners through established professional methodology (PTES, OSSTMM, NIST SP 800-115) to use industry-standard tools (Metasploit, Burp Suite, Nmap, BloodHound).

### The Golden Rule: Scope First

**All engagements MUST start with red-lead.** No other agent can operate without an active scope document. This is a structural safety constraint, not a suggestion.

### Your First Engagement in 4 Steps

**Step 1: Define scope.**

```
"Start a new penetration testing engagement for the 10.0.0.0/24 network"
```

red-lead creates a scope document defining authorized targets, allowed techniques, time window, exclusions, rules of engagement, and evidence handling.

**Step 2: Authorize the scope.**

Review the scope document. Confirm authorization:

```
"I authorize this engagement within the defined scope"
```

**Step 3: Begin the engagement.**

```
"Perform reconnaissance on the authorized targets"
```

red-recon maps the attack surface within the authorized scope.

**Step 4: Generate the report.**

```
"Generate the final engagement report for RED-0001"
```

red-reporter synthesizes all findings into a comprehensive report with executive summary, technical details, and remediation recommendations.

### Quick Agent Reference

| I need to... | Ask for... | Restrictions |
|--------------|------------|--------------|
| Define engagement scope | red-lead | Mandatory first step |
| Perform reconnaissance | red-recon | Within target allowlist |
| Analyze vulnerabilities | red-vuln | Scan only, no exploitation |
| Develop exploitation methodology | red-exploit | Target + technique intersection |
| Escalate privileges | red-privesc | Compromised hosts only |
| Move laterally | red-lateral | Authorized network range only |
| Establish persistence | red-persist | RoE-GATED -- requires explicit authorization |
| Plan data exfiltration | red-exfil | RoE-GATED -- requires explicit authorization |
| Set up C2 infrastructure | red-infra | Engagement infrastructure only |
| Conduct social engineering | red-social | RoE-GATED -- requires explicit authorization |
| Generate engagement report | red-reporter | Read-only access to findings |

---

## Skill Overview

### Purpose

The /red-team skill provides structured offensive security methodology guidance for authorized engagements. It organizes 11 agents across the MITRE ATT&CK kill chain, following established professional methodology frameworks:

| Framework | Role |
|-----------|------|
| **PTES** (Penetration Testing Execution Standard) | Primary engagement methodology covering pre-engagement through reporting |
| **OSSTMM** (Open Source Security Testing Methodology Manual) | Security testing methodology with social engineering coverage |
| **NIST SP 800-115** | Technical guide to information security testing and assessment |
| **MITRE ATT&CK** | Technique-level mapping for all agent activities (14/14 tactic coverage) |

### What /red-team Is NOT

This is a methodology-guidance framework, not an autonomous exploitation engine. /red-team does NOT:

- Execute exploits or payloads autonomously
- Access live systems or networks directly
- Generate weaponized exploit code
- Operate without explicit human authorization
- Replace human judgment for novel discovery or legal decisions

Agents guide practitioners through methodology. The human practitioner remains in the loop for all tool operations.

### When to Use /red-team

Use this skill when you are:

- Planning or executing a penetration testing engagement
- Performing reconnaissance or attack surface analysis
- Analyzing vulnerabilities and assessing exploit availability
- Developing exploitation methodology or payload crafting guidance
- Conducting privilege escalation, lateral movement, or persistence operations
- Planning data exfiltration testing within authorized scope
- Setting up C2 infrastructure or engagement tooling
- Conducting social engineering assessments
- Generating engagement reports with findings, risk scores, and remediation guidance
- Validating /eng-team defenses through adversarial testing (purple team)

### When NOT to Use /red-team

- For building secure software, use `/eng-team`
- For adversarial quality reviews of deliverables, use `/adversary`
- For general security research without an engagement context, use `/problem-solving`
- When no active scope document exists and no engagement is being planned
- When the target is outside any authorized engagement boundary

---

## Agent Registry

### red-lead -- Engagement Lead and Scope Authority

| Attribute | Value |
|-----------|-------|
| **Role** | Scope definition, RoE, methodology selection, team coordination |
| **ATT&CK Tactics** | All (oversight role) |
| **Authorization** | Full engagement scope; sole authority to create/modify scope |
| **Model** | opus |

**Capabilities:**
- Creates and manages scope documents with YAML schema (engagement_id, authorized_targets, technique_allowlist, time_window, exclusions, rules_of_engagement, agent_authorizations, evidence_handling, signature)
- Defines Rules of Engagement including escalation procedures, emergency stop conditions, and communication channels
- Selects engagement methodology (PTES, OSSTMM, NIST SP 800-115)
- Authorizes which agents may participate and which techniques they may use
- Performs mid-engagement scope modifications when new targets are discovered
- Enforces operational OPSEC across the team
- Validates findings quality before reporting
- Serves as circuit breaker authority when agents flag scope issues

**What red-lead does NOT do:** Execute offensive techniques directly. red-lead is oversight, not execution.

**Example request:** "Define scope for a penetration test of the 10.0.0.0/24 network with web application testing"

---

### red-recon -- Reconnaissance Specialist

| Attribute | Value |
|-----------|-------|
| **Role** | OSINT, network enumeration, attack surface mapping |
| **ATT&CK Tactics** | TA0043 Reconnaissance |
| **Authorization** | Passive/active recon within target allowlist only |
| **Model** | sonnet |

**Capabilities:**
- Open source intelligence (OSINT) gathering on authorized targets
- Network enumeration and service discovery (Nmap, Masscan)
- DNS reconnaissance and subdomain enumeration (Amass, theHarvester)
- Technology fingerprinting and version identification
- Attack surface mapping and analysis
- Cross-skill threat intelligence feed to eng-architect (Integration Point 1)

**Example request:** "Enumerate services and map the attack surface of the authorized network range"

---

### red-vuln -- Vulnerability Analyst

| Attribute | Value |
|-----------|-------|
| **Role** | Vulnerability identification, CVE research, risk scoring |
| **ATT&CK Tactics** | Analysis support (no direct tactic mapping) |
| **Authorization** | Scan only; no exploitation |
| **Model** | sonnet |

**Capabilities:**
- Vulnerability identification against discovered services
- CVE research and exploit availability assessment
- Attack path analysis and vulnerability chaining
- Risk scoring using CVSS and DREAD
- Vulnerability scanner methodology (Nuclei, Nessus, OpenVAS)
- Prioritized vulnerability list for red-exploit targeting

**Example request:** "Assess exploit availability for the CVEs discovered on the web application"

---

### red-exploit -- Exploitation Specialist

| Attribute | Value |
|-----------|-------|
| **Role** | Exploit development methodology, payload crafting, impact demonstration |
| **ATT&CK Tactics** | TA0001 Initial Access, TA0002 Execution, TA0040 Impact (technical) |
| **Authorization** | Target AND technique allowlist intersection |
| **Model** | sonnet |

**Capabilities:**
- Exploit development methodology for identified vulnerabilities
- Payload crafting guidance using established frameworks (Metasploit, Burp Suite, sqlmap)
- Vulnerability chaining for multi-step exploitation paths
- Proof-of-concept development methodology
- Safe impact demonstration (TA0040) without causing actual damage
- Execution-time defense evasion (process injection, signed binary proxy execution)
- Web application exploitation following OWASP Testing Guide
- Client-side exploitation (CSP bypass, DOM clobbering, prototype pollution, XSS filter evasion)

**What red-exploit does NOT do:** Generate weaponized exploit code directly. Guides use of established frameworks instead.

**Example request:** "Develop exploitation methodology for CVE-2026-1234 targeting the web application"

---

### red-privesc -- Privilege Escalation Specialist

| Attribute | Value |
|-----------|-------|
| **Role** | Local/domain privilege escalation, credential harvesting |
| **ATT&CK Tactics** | TA0004 Privilege Escalation, TA0006 Credential Access |
| **Authorization** | Compromised hosts only |
| **Model** | sonnet |

**Capabilities:**
- Local privilege escalation enumeration (LinPEAS, WinPEAS)
- Domain privilege escalation paths (BloodHound, Kerberoasting)
- Credential harvesting from compromised hosts
- Token manipulation and misuse
- Misconfiguration exploitation for privilege escalation
- Credential-based defense evasion (access token manipulation)

**Example request:** "Identify privilege escalation paths on the compromised web server"

---

### red-lateral -- Lateral Movement Specialist

| Attribute | Value |
|-----------|-------|
| **Role** | Pivoting, tunneling, internal network movement |
| **ATT&CK Tactics** | TA0008 Lateral Movement, TA0007 Discovery |
| **Authorization** | Authorized internal network range only |
| **Model** | sonnet |

**Capabilities:**
- Pivoting through compromised hosts to reach internal networks
- Tunneling methodologies (SSH tunnels, Chisel, socks proxies)
- Living-off-the-land techniques using built-in OS tools
- Internal exploitation of discovered services
- C2 channel usage during operations (infrastructure from red-infra)
- Network-level defense evasion (traffic signaling, protocol tunneling)

**Note:** red-lateral uses C2 infrastructure designed by red-infra but does not build or manage it.

**Example request:** "Plan lateral movement from the compromised DMZ server to the internal domain controller"

---

### red-persist -- Persistence Specialist (RoE-GATED)

| Attribute | Value |
|-----------|-------|
| **Role** | Backdoor methodology, scheduled tasks, rootkit analysis |
| **ATT&CK Tactics** | TA0003 Persistence, TA0005 Defense Evasion (persistence-related) |
| **Authorization** | RoE-GATED -- requires `persistence_authorized: true` in scope |
| **Model** | sonnet |

**Capabilities:**
- Backdoor placement methodology (web shells, implants, authorized types)
- Scheduled task and cron job persistence mechanisms
- Service manipulation for persistent access (Windows services, systemd units)
- Rootkit methodology and analysis guidance
- Registry-based persistence (Run keys, COM objects, WMI event subscriptions)
- Boot and logon autostart execution mechanisms
- Persistence-phase defense evasion (indicator removal, timestomping)
- Mandatory cleanup documentation for engagement close-out

**IMPORTANT:** This agent halts immediately if `persistence_authorized` is not `true` in the scope document. All persistence mechanisms are documented for complete cleanup.

**Example request:** "Establish persistence methodology on the compromised host using scheduled tasks"

---

### red-exfil -- Data Exfiltration Specialist (RoE-GATED)

| Attribute | Value |
|-----------|-------|
| **Role** | Data identification, exfiltration channels, DLP bypass assessment |
| **ATT&CK Tactics** | TA0009 Collection, TA0010 Exfiltration |
| **Authorization** | RoE-GATED -- requires `exfiltration_authorized: true` with `data_types_permitted` |
| **Model** | sonnet |

**Capabilities:**
- Data identification and classification within engagement scope
- Exfiltration channel methodology (DNS tunneling, HTTP/S, encrypted channels)
- Covert communication channel design for testing
- DLP bypass assessment methodology
- Exfiltration-phase defense evasion (data encoding, encrypted channels)
- All exfiltration directed to evidence vault, never to external destinations

**IMPORTANT:** This agent only permits exfiltration of data types specified in `data_types_permitted` within the RoE. All exfiltrated data goes to the engagement evidence vault.

**Example request:** "Plan exfiltration of test data using DNS tunneling to assess DLP controls"

---

### red-infra -- Infrastructure and Tooling Specialist

| Attribute | Value |
|-----------|-------|
| **Role** | C2 frameworks, payload building, redirectors, infrastructure OPSEC |
| **ATT&CK Tactics** | TA0042 Resource Development, TA0011 Command and Control, TA0005 Defense Evasion (tool-level) |
| **Authorization** | Engagement infrastructure only; no direct target access |
| **Model** | sonnet |

**Capabilities:**
- C2 framework management (Cobalt Strike, Sliver, Mythic)
- Payload building and delivery methodology
- Redirector infrastructure design and hardening
- Tool development and customization methodology
- Tool-level defense evasion (C2 obfuscation, payload encoding/packing, sandbox evasion)
- Infrastructure OPSEC and operational security
- Supply chain attack simulation (dependency confusion, build pipeline integrity testing)
- CI/CD pipeline attack methodology (poisoned pipeline execution, secrets extraction)

**Note:** red-infra builds and manages the engagement infrastructure. It does not interact with targets directly. Other agents (red-exploit, red-lateral) use the infrastructure red-infra provides.

**Example request:** "Set up a Sliver C2 framework with HTTPS redirectors for the engagement"

---

### red-social -- Social Engineering Specialist (RoE-GATED)

| Attribute | Value |
|-----------|-------|
| **Role** | Phishing, pretexting, vishing, human attack vector analysis |
| **ATT&CK Tactics** | TA0043 Reconnaissance (social), TA0001 Initial Access (phishing) |
| **Authorization** | RoE-GATED -- requires `social_engineering_authorized: true` in scope |
| **Model** | sonnet |

**Capabilities:**
- Social reconnaissance and personnel OSINT
- Phishing campaign methodology (spear-phishing, whaling, GoPhish)
- Pretexting framework development
- Vishing (voice phishing) methodology
- Credential harvesting via social channels
- Human attack vector analysis

**IMPORTANT:** This agent halts immediately if `social_engineering_authorized` is not `true` in the scope document. Targets individuals only within the authorized scope.

**Example request:** "Design a spear-phishing campaign methodology for the authorized engagement"

---

### red-reporter -- Engagement Reporter and Documentation Specialist

| Attribute | Value |
|-----------|-------|
| **Role** | Finding documentation, risk scoring, reports, scope compliance attestation |
| **ATT&CK Tactics** | TA0040 Impact (documentation side) |
| **Authorization** | Read-only access to all engagement data; no active testing |
| **Model** | opus |

**Capabilities:**
- Comprehensive engagement report generation (executive summary, technical detail, strategic implications)
- Individual finding documentation with severity, evidence, and remediation recommendations
- Risk scoring using CVSS, DREAD, or engagement-specific frameworks
- Executive summary writing for non-technical stakeholders
- Impact risk communication in business-relevant language
- Scope compliance attestation verifying all operations stayed within authorized boundaries
- Evidence chain validation from discovery through exploitation
- Interim report generation during ongoing engagements

**Exception:** red-reporter can be invoked without an active scope for report generation from existing findings (e.g., for completed engagements).

**Example request:** "Generate the final engagement report for RED-0001 with executive summary and remediation priorities"

---

## Choosing the Right Agent

| Your Request Contains... | Use This Agent | Notes |
|--------------------------|----------------|-------|
| scope, RoE, engagement, authorization, rules | red-lead | Always start here |
| recon, OSINT, enumerate, scan, fingerprint, attack surface | red-recon | Scope must be active |
| vulnerability, CVE, risk score, exploit availability | red-vuln | Scan only, no exploitation |
| exploit, payload, initial access, PoC, bypass | red-exploit | Requires vulnerability findings |
| privilege, escalation, credential, token, SYSTEM, root | red-privesc | Compromised host required |
| lateral, pivot, tunnel, internal, living-off-the-land | red-lateral | Authorized network range only |
| persist, backdoor, scheduled task, rootkit, implant | red-persist | RoE-GATED |
| exfil, data, covert channel, DLP, collection | red-exfil | RoE-GATED |
| C2, command and control, infrastructure, redirector | red-infra | Engagement infra only |
| phishing, social engineering, pretext, vishing | red-social | RoE-GATED |
| report, findings, executive summary, remediation | red-reporter | Read-only |

---

## L1: Engagement Workflow

### Authorization Procedures

#### The Scope Document

Every engagement starts with a scope document. This is a signed YAML artifact that defines the complete authorization boundary. The scope document is created by red-lead and must be authorized by you (the user) before any operational agent can proceed.

#### Scope Document Fields

| Field | Purpose | Example |
|-------|---------|---------|
| `engagement_id` | Unique engagement identifier | `RED-0001` |
| `authorized_targets` | Explicit targets (IP ranges, domains, apps) | `10.0.0.0/24`, `target.example.com` |
| `technique_allowlist` | Authorized ATT&CK technique IDs | `T1595`, `T1190`, `T1059` |
| `time_window` | Start and end timestamps | `2026-03-01T08:00Z` to `2026-03-15T18:00Z` |
| `exclusion_list` | Systems that must NOT be touched | `10.0.0.1` (prod gateway), `hr.target.com` |
| `rules_of_engagement` | Behavioral constraints and gating flags | Emergency stop number, social engineering authorization |
| `agent_authorizations` | Which agents may participate | `[red-recon, red-vuln, red-exploit, ...]` |
| `evidence_handling` | Storage, retention, and destruction policy | 90-day retention, secure-delete |
| `signature` | Your authorization confirmation | "I authorize this engagement within the defined scope" |

#### Example Scope Document

```yaml
scope:
  engagement_id: "RED-0001"
  version: "1.0"
  authorized_targets:
    - type: "network"
      value: "10.0.0.0/24"
    - type: "domain"
      value: "target.example.com"
    - type: "application"
      value: "https://app.target.example.com"
  technique_allowlist:
    - "T1595"   # Active Scanning
    - "T1592"   # Gather Victim Host Information
    - "T1190"   # Exploit Public-Facing Application
    - "T1059"   # Command and Scripting Interpreter
    - "T1078"   # Valid Accounts
  time_window:
    start: "2026-03-01T08:00:00Z"
    end: "2026-03-15T18:00:00Z"
  exclusion_list:
    - "10.0.0.1"         # Production gateway
    - "hr.target.com"    # HR systems
  rules_of_engagement:
    escalation_contact: "security-lead@target.com"
    emergency_stop: "Call +1-555-0100"
    communication_channel: "encrypted-chat"
    social_engineering_authorized: false
    persistence_authorized: false
    exfiltration_authorized: true
    data_types_permitted:
      - "non-production test data"
  agent_authorizations:
    - red-recon
    - red-vuln
    - red-exploit
    - red-privesc
    - red-lateral
    - red-exfil
    - red-infra
    - red-reporter
  evidence_handling:
    storage: "skills/red-team/output/RED-0001/evidence/"
    retention_days: 90
    destruction_method: "secure-delete"
  signature:
    authorized_by: "user"
    date: "2026-03-01"
    confirmation: "I authorize this engagement within the defined scope"
```

#### What Happens Without Authorization

If any agent is invoked without an active scope document:

1. The agent **halts immediately**
2. The agent returns: `AUTHORIZATION REQUIRED: No active scope document found. red-lead must establish scope before any operational agent can proceed.`
3. The orchestrator routes to red-lead for scope establishment

---

### How to Invoke Agents

#### Method 1: Natural Language (Recommended)

```
"Start a new penetration testing engagement for the 10.0.0.0/24 network"
"Perform reconnaissance on target.example.com"
"Analyze vulnerabilities found in the web application"
"Generate the final engagement report for RED-0001"
```

#### Method 2: Explicit Agent Request

```
"Use red-lead to define scope for a new engagement"
"Have red-recon perform OSINT on the target domain"
"I need red-vuln to assess exploit availability for the discovered CVEs"
"Ask red-reporter to generate the executive summary"
```

#### Method 3: Task Tool Invocation

```python
Task(
    description="red-recon: Reconnaissance of target network",
    prompt="""
You are the red-recon agent (v1.0.0).

## RED TEAM CONTEXT (REQUIRED)
- **Engagement ID:** RED-0001
- **Scope Document:** skills/red-team/output/RED-0001/red-lead-scope.md
- **Target:** 10.0.0.0/24
- **Phase:** Reconnaissance

## MANDATORY PERSISTENCE (P-002)
Create file at: skills/red-team/output/RED-0001/red-recon-network-enumeration.md

## TASK
Perform network reconnaissance methodology guidance for the authorized target range.
"""
)
```

---

### The Kill Chain Workflow

Unlike /eng-team's sequential 8-step workflow, /red-team uses a **non-linear kill chain**. After red-lead establishes scope, agents can be invoked in any order based on engagement context. Real engagements are iterative -- exploitation discovers new reconnaissance targets, triggering return to earlier phases.

```
                    +------------+
                    |  red-lead  |  <-- MANDATORY FIRST
                    +-----+------+
                          |
                          v
          +--- SCOPE ESTABLISHED ---+
          | (any agent invocable)   |
          +------+------+------+---+
                 |      |      |
     +-----------+  +---+  +---+-----------+
     v              v      v               v
 +--------+   +--------+  +--------+  +--------+
 |red-recon|-->|red-vuln|  |red-    |  |red-    |
 +---+----+   +---+----+  |social* |  |infra   |
     |            |        +--------+  +--------+
     |   +--------+
     v   v
 +--------+     +--------+     +--------+
 |red-    |---->|red-     |---->|red-    |
 |exploit |     |privesc  |     |lateral |
 +--------+     +--------+     +--------+
                                    |
                    +-------+-------+
                    v       v
              +--------+ +--------+
              |red-    | |red-    |
              |persist*| |exfil* |
              +--------+ +--------+
                    |
                    v
              +----------+
              |red-      |  <-- MANDATORY LAST (for reporting)
              |reporter  |
              +----------+

 * = RoE-GATED (requires explicit authorization)
 Arrows show COMMON flow, not required sequence.
```

#### Workflow Rules

1. **red-lead MUST establish scope first.** No exceptions.
2. **After scope, any agent is invocable in any order** based on engagement context.
3. **Phase cycling is supported.** Exploitation may reveal new recon targets. Privilege escalation may uncover new vulnerabilities. Lateral movement may expose new network segments. Any agent can feed findings back to any prior-phase agent.
4. **Circuit breaker at every agent transition.** Scope revalidation occurs before each agent invocation.
5. **red-reporter generates the final report** (mandatory last for reporting). Can also produce interim reports during the engagement.
6. **red-infra can be invoked at any point** to set up or modify engagement infrastructure.

---

### RoE-Gated Agents

Three agents require additional explicit authorization in the Rules of Engagement before they can operate:

| Agent | RoE Gate Flag | Why It Is Gated |
|-------|---------------|-----------------|
| **red-persist** | `persistence_authorized: true` | Establishing backdoors and persistence mechanisms carries elevated risk of detection and operational impact |
| **red-exfil** | `exfiltration_authorized: true` + `data_types_permitted` | Data exfiltration testing must specify exactly which data types can be collected |
| **red-social** | `social_engineering_authorized: true` | Social engineering targets human subjects, requiring explicit consent and ethical boundaries |

If a RoE-gated agent is invoked without its authorization flag set to `true`, the agent halts immediately and returns to red-lead for scope review.

---

### Output Levels

Every agent produces output at three levels:

| Level | Audience | Content |
|-------|----------|---------|
| **L0 (Executive Summary)** | Engagement managers, leadership | Business-language overview of findings, risk implications, and remediation priorities |
| **L1 (Technical Detail)** | Security practitioners, engineers | Step-by-step methodology, ATT&CK technique references, tool configurations, evidence artifacts |
| **L2 (Strategic Implications)** | Architecture reviewers, security strategists | Defense gap analysis, long-term security posture assessment, recommendations for /eng-team hardening |

**Output Location:** All files are saved at:
```
skills/red-team/output/{engagement-id}/{agent-name}-{topic-slug}.md
```

**Evidence Storage:**
```
skills/red-team/output/{engagement-id}/evidence/
```

---

## L2: Advanced Configuration

### Authorization Architecture

The /red-team skill implements a three-layer defense-in-depth authorization architecture (ADR-PROJ010-006). This ensures that out-of-scope actions are **structurally impossible**, not merely procedurally discouraged.

#### Layer 1: Structural Authorization (Pre-Engagement)

Static constraints defined before the engagement begins:

| Component | Function |
|-----------|----------|
| **Scope Document** | Signed YAML defining all authorization boundaries; immutable during engagement |
| **Target Allowlist** | IP ranges, domains, and applications explicitly permitted |
| **Technique Allowlist** | ATT&CK technique IDs each agent may use |
| **Time Window** | Start/end timestamps; credentials expire at window close |
| **Exclusion List** | Systems explicitly forbidden; exclusions always supersede allows |
| **Rules of Engagement** | Escalation procedures, communication channels, gating conditions |

#### Layer 2: Dynamic Authorization (During Engagement)

Runtime enforcement components that validate every action:

| Component | Function |
|-----------|----------|
| **Scope Oracle** | Validates every action against scope rules; returns allow/deny with reasons |
| **Tool Proxy** | Intercepts all tool invocations; default-deny policy; agents never invoke tools directly |
| **Network Enforcer** | Infrastructure-level network access control derived from scope document |
| **Credential Broker** | Provides ephemeral, scope-bounded, time-limited tokens; agents never see raw credentials |

#### Layer 3: Retrospective Authorization (Post-Engagement)

After-action verification:

| Component | Function |
|-----------|----------|
| **Action Log Review** | Every agent action compared against scope for compliance |
| **Evidence Verification** | Findings traced from discovery to scope authorization |
| **Compliance Report** | Formal attestation that the engagement stayed within scope |

#### Per-Agent Authorization Levels

Each agent operates under distinct authorization constraints:

| Agent | Network Access | Data Access | Special Constraints |
|-------|---------------|-------------|---------------------|
| red-lead | Verification only | Full audit trail, scope docs | Creates scope; no direct target interaction |
| red-recon | Authorized targets (recon only) | Enumeration data only | No exploitation traffic |
| red-vuln | Authorized targets (scan only) | Scan results, CVE data | No credentials or host-level data |
| red-exploit | Authorized targets (exploitation) | Exploitation artifacts | Target + technique intersection |
| red-privesc | Compromised host only | Local host data, credentials | No lateral network access |
| red-lateral | Authorized network range | Internal network data | Uses red-infra C2 |
| red-persist | Authorized persistence targets | Host configuration | RoE gate + compromised hosts only |
| red-exfil | Evidence vault only | Scope-permitted data types | No external exfiltration |
| red-infra | Engagement infrastructure only | C2 config, payload artifacts | No direct target access |
| red-social | Authorized communication channels | Authorized contact lists | RoE gate + authorized individuals only |
| red-reporter | Evidence vault (read-only) | Full engagement data (read-only) | No active testing |

#### Circuit Breaker Protocol

At every agent transition, a circuit breaker check occurs:

1. Scope revalidation: Is the target still within authorized scope?
2. Time window check: Is the engagement still within authorized time?
3. Technique check: Are the next agent's techniques in the allowlist?
4. Agent authorization: Is the next agent in the agent_authorizations list?
5. RoE gate: If next agent is RoE-gated, is it explicitly authorized?
6. Cascading failure detection: Has any prior agent reported anomalies?

If **all checks pass**, the next agent proceeds. If **any check fails**, operations halt and red-lead is invoked for scope review.

---

### Methodology Reference

#### PTES Mapping

| PTES Phase | /red-team Agent(s) |
|------------|-------------------|
| Pre-Engagement Interactions | red-lead |
| Intelligence Gathering | red-recon |
| Threat Modeling | red-vuln (with red-recon input) |
| Vulnerability Analysis | red-vuln |
| Exploitation | red-exploit |
| Post-Exploitation | red-privesc, red-lateral, red-persist, red-exfil |
| Reporting | red-reporter |

#### MITRE ATT&CK Coverage

The /red-team skill achieves 14/14 tactic coverage at STRONG level:

| ATT&CK Tactic | ID | Primary Agent |
|----------------|----|---------------|
| Reconnaissance | TA0043 | red-recon, red-social |
| Resource Development | TA0042 | red-infra |
| Initial Access | TA0001 | red-exploit, red-social |
| Execution | TA0002 | red-exploit |
| Persistence | TA0003 | red-persist |
| Privilege Escalation | TA0004 | red-privesc |
| Defense Evasion | TA0005 | Distributed (red-infra, red-exploit, red-privesc, red-lateral, red-persist, red-exfil) |
| Credential Access | TA0006 | red-privesc |
| Discovery | TA0007 | red-lateral |
| Lateral Movement | TA0008 | red-lateral |
| Collection | TA0009 | red-exfil |
| Exfiltration | TA0010 | red-exfil |
| Command and Control | TA0011 | red-infra |
| Impact | TA0040 | red-exploit (technical), red-reporter (documentation) |

#### Defense Evasion Ownership

Defense Evasion (TA0005) is distributed across agents by phase:

| Agent | Evasion Domain | Example Techniques |
|-------|---------------|-------------------|
| red-infra | Tool-level | C2 obfuscation, payload encoding, sandbox evasion |
| red-exploit | Execution-time | Process injection, signed binary proxy execution |
| red-privesc | Credential-based | Access token manipulation |
| red-lateral | Network-level | Traffic signaling, protocol tunneling |
| red-persist | Persistence-phase | Indicator removal, rootkits, timestomping |
| red-exfil | Exfiltration-phase | Data encoding, encrypted channels |

#### OSSTMM Coverage

OSSTMM methodology supports the social engineering and physical testing vectors:

| OSSTMM Section | /red-team Coverage |
|----------------|-------------------|
| Section III: Regulatory Framework | red-lead scope definition |
| Section V: Human Security Testing | red-social |
| Section VI: Physical Security Testing | Out of scope for PROJ-010 |
| Section VII: Wireless Security Testing | Covered by red-recon (wireless enumeration) |
| Section VIII: Telecommunications | red-social (vishing) |
| Section IX: Data Network Security | red-recon through red-exfil |

---

### Integration Points

#### Integration with /eng-team (Purple Team)

Four integration points connect offensive findings to defensive hardening:

| Integration Point | Red-Team Source | Eng-Team Target | Value |
|-------------------|----------------|-----------------|-------|
| **1. Threat-Informed Architecture** | red-recon | eng-architect | Real adversary TTPs inform threat model accuracy beyond theoretical threats |
| **2. Attack Surface Validation** | red-recon, red-vuln | eng-infra, eng-devsecops | Validates that infrastructure hardening actually reduces attack surface |
| **3. Secure Code vs. Exploitation** | red-exploit, red-privesc | eng-security, eng-backend, eng-frontend | Proves whether secure coding practices withstand real exploitation |
| **4. Incident Response Validation** | red-persist, red-lateral, red-exfil | eng-incident | Validates IR runbooks against real post-exploitation techniques |

For full purple team engagement workflows, see the Purple Team Integration Framework.

#### Integration with /adversary

/adversary provides quality scoring for engagement deliverables:

| Criticality | Application |
|-------------|-------------|
| C1 (Routine) | Self-review (S-010) on agent outputs |
| C2 (Standard) | S-007 Constitutional compliance + S-002 Devil's Advocate |
| C3 (Significant) | C2 + S-004 Pre-Mortem on engagement risks |
| C4 (Critical) | Full tournament review on engagement reports and scope documents |

The scope document itself is always C4 criticality (irreversible authorization decision).

#### Integration with /problem-solving

Use /problem-solving for research tasks that precede /red-team work:

- "Research current CVE trends for Apache Struts" (use /problem-solving)
- "Develop exploitation methodology for CVE-2026-1234" (use /red-team)

#### Integration with /nasa-se

Use /nasa-se for formal requirements specification and V&V activities that complement /red-team engagements:

- Requirements for scope document completeness
- Verification of authorization architecture compliance
- Formal technical reviews of engagement methodology

---

### Reporting Format

#### Engagement Report Structure

red-reporter produces the final engagement report with three levels:

**L0 -- Executive Summary (for leadership):**
- Engagement scope and duration
- Key findings count by severity (Critical/High/Medium/Low/Informational)
- Top 3 most impactful findings in business language
- Overall security posture assessment
- Risk summary with remediation priority recommendations

**L1 -- Technical Detail (for security teams):**
- Complete finding inventory with ATT&CK technique IDs, CVE references, and CWE mappings
- Step-by-step exploitation methodology per finding (following PTES, not weaponized code)
- Evidence references stored in the evidence vault
- CVSS/DREAD severity scores for each finding
- Specific remediation guidance with implementation examples
- Attack path diagrams showing the chain from reconnaissance to impact

**L2 -- Strategic Implications (for architecture and governance):**
- Systemic vulnerability patterns indicating architectural weaknesses
- Defense-in-depth assessment (which layers held, which failed)
- Comparison with industry benchmarks
- Long-term remediation roadmap
- Recommendations for /eng-team hardening priorities

#### Finding Record Format

Each finding includes:

| Field | Description |
|-------|-------------|
| Finding ID | Unique identifier (e.g., `RED-0001-F001`) |
| Severity | Critical / High / Medium / Low / Informational |
| ATT&CK Technique | Technique ID (e.g., T1190 -- Exploit Public-Facing Application) |
| Title | Concise finding title |
| Description | Detailed description with exploitation methodology |
| Evidence | Tool output, screenshots, logs stored in evidence vault |
| Remediation | Specific, actionable fix with implementation guidance |
| CVSS Score | Quantitative severity rating |
| Confidence | Confirmed / Probable / Possible |

#### Scope Compliance Attestation

Every engagement concludes with a formal scope compliance report produced by red-lead and red-reporter:

- All operations verified against the scope document
- Target boundary compliance confirmed
- Technique allowlist compliance confirmed
- Time window compliance confirmed
- Evidence handling compliance confirmed
- Formal attestation that the engagement operated within authorized boundaries

---

## Common Scenarios

### Scenario 1: External Network Penetration Test

**Goal:** Assess the external attack surface of a corporate network.

1. "Define scope for an external penetration test of target.example.com and the 203.0.113.0/24 range" -- red-lead creates the scope document
2. "Perform external reconnaissance including DNS enumeration and service discovery" -- red-recon maps the attack surface
3. "Assess vulnerabilities on the discovered web applications and exposed services" -- red-vuln identifies exploitable CVEs
4. "Develop exploitation methodology for the top 3 vulnerabilities" -- red-exploit guides the exploitation approach
5. "Identify privilege escalation paths on the compromised web server" -- red-privesc explores escalation opportunities
6. "Generate the final engagement report with executive summary" -- red-reporter synthesizes all findings

### Scenario 2: Internal Red Team Exercise with Full Kill Chain

**Goal:** Simulate an advanced persistent threat from initial access through exfiltration.

1. "Define scope for an internal red team exercise with persistence and exfiltration authorized" -- red-lead creates scope with RoE gates enabled
2. "Set up C2 infrastructure with Sliver and HTTPS redirectors" -- red-infra builds the engagement infrastructure
3. "Perform internal network reconnaissance from the assumed-breach position" -- red-recon maps the internal network
4. "Exploit the discovered file server vulnerability" -- red-exploit gains initial foothold
5. "Escalate privileges to domain admin" -- red-privesc achieves domain compromise
6. "Establish persistence using scheduled tasks on 3 hosts" -- red-persist maintains access
7. "Move laterally to the database server" -- red-lateral reaches the target data
8. "Exfiltrate test data to assess DLP controls" -- red-exfil tests data loss prevention
9. "Generate the comprehensive engagement report" -- red-reporter documents everything

### Scenario 3: Social Engineering Assessment

**Goal:** Test human security awareness through phishing.

1. "Define scope for a social engineering assessment with phishing authorized" -- red-lead creates scope with `social_engineering_authorized: true`
2. "Perform social reconnaissance on the target organization" -- red-social gathers information on personnel
3. "Design a spear-phishing campaign targeting the finance department" -- red-social develops the methodology
4. "Generate the phishing assessment report with click rates and recommendations" -- red-reporter documents results

### Scenario 4: Purple Team Exercise

**Goal:** Validate /eng-team defenses through adversarial testing.

1. "Define scope for a purple team exercise focused on the payment service" -- red-lead creates scope with `PT-NNNN` engagement ID
2. eng-architect provides the threat model as the defensive baseline
3. "Perform reconnaissance against the payment service infrastructure" -- red-recon assesses the hardened target
4. "Attempt exploitation of the payment API" -- red-exploit tests eng-backend/eng-frontend defenses
5. "Test the IR runbooks by establishing persistence and triggering detection" -- red-persist validates eng-incident detection rules
6. "Generate the purple team report with finding-to-remediation mapping" -- red-reporter produces the cross-skill report

---

## Troubleshooting and FAQ

### Why did the agent say "AUTHORIZATION REQUIRED"?

Every operational agent (all except red-lead) requires an active scope document. If no scope document exists for the current engagement, the agent halts and directs you to red-lead.

**Fix:** Start with red-lead to create and authorize a scope document.

### Why did the RoE-gated agent refuse to proceed?

Three agents (red-persist, red-exfil, red-social) require explicit authorization flags in the scope document's Rules of Engagement section. If the flag is not set to `true`, the agent halts.

**Fix:** Ask red-lead to modify the scope document with the appropriate RoE flag, then re-authorize.

### Can I modify the scope mid-engagement?

Yes. Ask red-lead to create a new scope document version:

```
"Add 10.0.1.0/24 to the authorized targets for RED-0001"
```

Scope modification follows a strict process: red-lead creates a new version, you authorize it, and all enforcement components reload with the updated rules.

### What happens if the time window expires?

All credentials automatically expire. Agents lose tool access and degrade to standalone mode (Level 2). No further operations against targets are possible until red-lead creates a new scope document with an updated time window.

### Can I use /red-team without /eng-team?

Yes. /red-team is fully standalone. The /eng-team integration points (purple team) enable adversarial-collaborative hardening, but /red-team conducts complete penetration testing engagements independently.

### What is the difference between red-exploit and red-privesc?

- **red-exploit** handles initial access and execution -- getting a foothold on the target through vulnerability exploitation
- **red-privesc** handles privilege escalation and credential access -- gaining higher privileges once a foothold exists

red-exploit gets you in. red-privesc gets you elevated.

### What is the difference between red-lateral and red-infra?

- **red-infra** builds and manages the engagement infrastructure (C2 frameworks, redirectors, payloads). It does not interact with targets.
- **red-lateral** uses the infrastructure red-infra provides to move through the target network. It consumes C2 channels but does not build them.

### How are engagement reports reviewed for quality?

red-reporter outputs go through /adversary quality scoring. For scope documents (always C4), all 10 adversarial strategies apply. For engagement reports, the criticality level determines the strategy set. The quality threshold is >= 0.95 for PROJ-010 deliverables.

### How do engagement IDs work?

Engagement IDs follow the `RED-NNNN` format (e.g., `RED-0001`). For purple team exercises, the `PT-NNNN` format is used. The engagement ID organizes all output files and evidence into a single directory.

---

## References

### Architecture Decision Records

| ADR | Title |
|-----|-------|
| ADR-PROJ010-001 | Agent Team Architecture -- 11-agent roster, non-linear kill chain, defense evasion model, cross-skill integration |
| ADR-PROJ010-006 | Authorization & Scope Control -- three-layer defense-in-depth, per-agent authorization, circuit breakers, OWASP Agentic AI Top 10 coverage |
| ADR-PROJ010-002 | Skill Routing and Invocation -- keyword triggers, routing table |
| ADR-PROJ010-003 | LLM Portability -- portable agent schema, multi-provider support |

### Methodology Standards

| Standard | Version | Application |
|----------|---------|-------------|
| PTES | Current | Primary engagement methodology (pre-engagement through reporting) |
| OSSTMM | Current | Security testing methodology with social engineering coverage |
| NIST SP 800-115 | Current | Technical guide to information security testing and assessment |
| MITRE ATT&CK Enterprise | 2025 | Technique-level mapping for all agent activities (14/14 tactic coverage) |
| OWASP Testing Guide | Current | Web application security testing methodology |

### Security Framework References

| Framework | Application |
|-----------|-------------|
| OWASP Agentic AI Top 10 (Dec 2025) | Risk taxonomy for the authorization architecture (ASI01-ASI10) |
| AWS Agentic AI Security Scoping Matrix | Progressive autonomy deployment model |
| CVSS v3.1/v4.0 | Vulnerability severity scoring |
| DREAD | Risk quantification for threat modeling |

### Agent Definition Files

| Agent | File Path |
|-------|-----------|
| red-lead | `skills/red-team/agents/red-lead.md` |
| red-recon | `skills/red-team/agents/red-recon.md` |
| red-vuln | `skills/red-team/agents/red-vuln.md` |
| red-exploit | `skills/red-team/agents/red-exploit.md` |
| red-privesc | `skills/red-team/agents/red-privesc.md` |
| red-lateral | `skills/red-team/agents/red-lateral.md` |
| red-persist | `skills/red-team/agents/red-persist.md` |
| red-exfil | `skills/red-team/agents/red-exfil.md` |
| red-infra | `skills/red-team/agents/red-infra.md` |
| red-social | `skills/red-team/agents/red-social.md` |
| red-reporter | `skills/red-team/agents/red-reporter.md` |

### Related Documents

| Document | Location |
|----------|----------|
| Purple Team Integration Framework | `projects/PROJ-010-cyber-ops/work/EPIC-005-purple-team-validation/FEAT-040-purple-team-framework/purple-team-integration-framework.md` |
| /eng-team User Guide | `projects/PROJ-010-cyber-ops/work/EPIC-006-documentation-guides/FEAT-050-eng-team-documentation/eng-team-user-guide.md` |

---

*Document Version: 1.0.0*
*SSOT: ADR-PROJ010-001, ADR-PROJ010-006*
*Feature: FEAT-051 (/red-team User Documentation)*
*Created: 2026-02-22*
