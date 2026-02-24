---
name: red-team
description: >
  Offensive security team skill providing methodology guidance for penetration
  testing and red team engagements. Invoked when users request penetration
  testing, reconnaissance, vulnerability analysis, exploitation methodology,
  social engineering, C2 infrastructure, or engagement reporting. Routes to
  11 specialized agents covering the full MITRE ATT&CK kill chain.
  All engagements require red-lead scope authorization before any other agent.
  Follows PTES, OSSTMM, and ATT&CK methodology frameworks.
version: "1.0.0"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Task, WebSearch, WebFetch, mcp__context7__resolve-library-id, mcp__context7__query-docs
activation-keywords:
  - "penetration test"
  - "pentest"
  - "red team"
  - "offensive security"
  - "reconnaissance"
  - "exploit"
  - "privilege escalation"
  - "lateral movement"
  - "persistence"
  - "exfiltration"
  - "C2"
  - "command and control"
  - "social engineering"
  - "phishing"
  - "attack surface"
  - "kill chain"
  - "PTES"
  - "OSSTMM"
  - "ATT&CK"
  - "rules of engagement"
  - "engagement report"
---

# Red Team Skill

> **Version:** 1.0.0
> **Framework:** Jerry Red-Team
> **Constitutional Compliance:** Jerry Constitution v1.0
> **SSOT Reference:** ADR-PROJ010-001 (Agent Team Architecture), ADR-PROJ010-006 (Authorization & Scope Control)

## Document Audience (Triple-Lens)

This SKILL.md serves multiple audiences:

| Level | Audience | Sections to Focus On |
|-------|----------|---------------------|
| **L0 (Stakeholder)** | Engagement managers, leadership | [Purpose](#purpose), [When to Use This Skill](#when-to-use-this-skill), [Mandatory Authorization](#mandatory-authorization), [Quick Reference](#quick-reference) |
| **L1 (Practitioner)** | Security testers invoking agents | [Available Agents](#available-agents), [Invoking an Agent](#invoking-an-agent), [Orchestration Flow](#orchestration-flow), [Cross-Skill Integration Points](#cross-skill-integration-points) |
| **L2 (Architect)** | Framework designers, governance reviewers | [Authorization Architecture](#authorization-architecture), [Circuit Breaker Integration](#circuit-breaker-integration), [Safety Alignment Compatibility](#safety-alignment-compatibility), [Constitutional Compliance](#constitutional-compliance) |

---

## Purpose

The Red Team skill provides **methodology guidance for authorized penetration testing and red team engagements**. It routes to 11 specialized agents that collectively cover the full MITRE ATT&CK kill chain (14/14 tactics at STRONG coverage level), following established professional methodology frameworks: PTES (Penetration Testing Execution Standard), OSSTMM (Open Source Security Testing Methodology Manual), and NIST SP 800-115 (Technical Guide to Information Security Testing and Assessment).

### Key Capabilities

- **Scope & Authorization Management** -- Formal engagement scoping with Rules of Engagement, target allowlists, and technique authorization
- **Full Kill Chain Coverage** -- 11 agents spanning Reconnaissance through Exfiltration with explicit ATT&CK tactic mapping
- **Non-Linear Workflow** -- Iterative phase cycling that mirrors real engagement dynamics, not rigid sequential execution
- **Distributed Defense Evasion** -- TA0005 techniques embedded in each operational agent's phase-specific tradecraft
- **Cross-Skill Integration** -- 4 purple team integration points with /eng-team for adversarial-collaborative hardening
- **Three-Level Degradation** -- All agents function standalone (AD-010); tools augment evidence quality but do not enable reasoning

### What This Skill Is NOT

This skill provides **methodology guidance**, not autonomous exploitation. It does NOT:

- Execute exploits or payloads autonomously
- Access live systems or networks directly
- Generate weaponized exploit code
- Operate without explicit human authorization
- Replace human judgment for novel discovery or legal decisions

This design follows AD-001 (Methodology-First Design Paradigm): LLMs excel at methodology guidance, structured reasoning, and report generation but fundamentally cannot replace tool execution or human judgment for novel discovery (S-001 Convergence 1, D-002).

---

## When to Use This Skill

Activate when:

- Planning or executing a penetration testing engagement
- Performing reconnaissance or attack surface analysis
- Analyzing vulnerabilities and assessing exploit availability
- Developing exploitation methodology or payload crafting guidance
- Conducting privilege escalation, lateral movement, or persistence operations
- Planning data exfiltration testing within authorized scope
- Setting up C2 infrastructure or engagement tooling
- Conducting social engineering assessments (phishing, pretexting, vishing)
- Generating engagement reports with findings, risk scores, and remediation guidance
- Validating /eng-team defenses through adversarial testing (purple team)

**Do NOT use when:**

- Building secure software (use `/eng-team` instead)
- Performing adversarial quality reviews of deliverables (use `/adversary` instead)
- Conducting general security research without an engagement context (use `/problem-solving` instead)
- No active scope document exists and no engagement is being planned
- The target is outside any authorized engagement boundary

---

## Available Agents

| Agent | Role | ATT&CK Tactics | Model | Output Location |
|-------|------|----------------|-------|-----------------|
| `red-lead` | Engagement Lead & Scope Authority | All (oversight) | opus | `skills/red-team/output/{engagement-id}/red-lead-{topic-slug}.md` |
| `red-recon` | Reconnaissance Specialist | TA0043 Reconnaissance | sonnet | `skills/red-team/output/{engagement-id}/red-recon-{topic-slug}.md` |
| `red-vuln` | Vulnerability Analyst | Analysis support | sonnet | `skills/red-team/output/{engagement-id}/red-vuln-{topic-slug}.md` |
| `red-exploit` | Exploitation Specialist | TA0001, TA0002, TA0040 | sonnet | `skills/red-team/output/{engagement-id}/red-exploit-{topic-slug}.md` |
| `red-privesc` | Privilege Escalation Specialist | TA0004, TA0006 | sonnet | `skills/red-team/output/{engagement-id}/red-privesc-{topic-slug}.md` |
| `red-lateral` | Lateral Movement Specialist | TA0008, TA0007 | sonnet | `skills/red-team/output/{engagement-id}/red-lateral-{topic-slug}.md` |
| `red-persist` | Persistence Specialist (RoE-GATED) | TA0003, TA0005 | sonnet | `skills/red-team/output/{engagement-id}/red-persist-{topic-slug}.md` |
| `red-exfil` | Data Exfiltration Specialist (RoE-GATED) | TA0009, TA0010 | sonnet | `skills/red-team/output/{engagement-id}/red-exfil-{topic-slug}.md` |
| `red-reporter` | Engagement Reporter | TA0040 (documentation) | opus | `skills/red-team/output/{engagement-id}/red-reporter-{topic-slug}.md` |
| `red-infra` | Infrastructure & Tooling Specialist | TA0042, TA0011, TA0005 | sonnet | `skills/red-team/output/{engagement-id}/red-infra-{topic-slug}.md` |
| `red-social` | Social Engineering Specialist (RoE-GATED) | TA0043, TA0001 | sonnet | `skills/red-team/output/{engagement-id}/red-social-{topic-slug}.md` |

---

## Mandatory Authorization

> **ALL engagements MUST start with red-lead.** No other agent can operate without an active scope document.

This is the foundational security constraint for the /red-team skill. The authorization model ensures that offensive operations are structurally bounded -- out-of-scope actions are architecturally impossible, not merely procedurally discouraged.

### Authorization Flow

```
1. User requests engagement  -->  red-lead creates scope document
2. Scope document defines:
   - engagement_id (RED-NNNN format)
   - authorized_targets (IP ranges, domains, applications)
   - technique_allowlist (ATT&CK technique IDs)
   - time_window (start/end timestamps)
   - exclusion_list (systems/networks explicitly excluded)
   - rules_of_engagement (escalation procedures, communication channels)
   - agent_authorizations (which agents are permitted)
   - evidence_handling (storage, retention, destruction)
   - signature (user authorization confirmation)
3. Every subsequent agent validates against the scope document
4. Scope Oracle checks at every agent transition
5. RoE-gated agents (red-persist, red-exfil, red-social) require ADDITIONAL
   explicit authorization in the Rules of Engagement
```

### Scope Document YAML Schema

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

### What Happens Without Authorization

If any agent is invoked without an active scope document:

1. Agent HALTS immediately
2. Agent returns: `AUTHORIZATION REQUIRED: No active scope document found for this engagement. red-lead must establish scope before any operational agent can proceed.`
3. Orchestrator routes to red-lead for scope establishment

**Exception:** red-reporter can be invoked without active scope for report generation from existing findings.

---

## P-003 Compliance

All red-team agents are **workers**, NOT orchestrators. The MAIN CONTEXT (Claude session) orchestrates the workflow.

```
P-003 AGENT HIERARCHY:
======================

  +-------------------+
  | MAIN CONTEXT      |  <-- Orchestrator (Claude session)
  | (orchestrator)    |
  +-------------------+
     |  |  |  |  |  |
     v  v  v  v  v  v
  +------+ +------+ +------+ +------+ +------+ +------+
  | red- | | red- | | red- | | red- | | red- | | ...  |
  | lead | | recon| | vuln | |exploi| |privsc| |      |
  +------+ +------+ +------+ +------+ +------+ +------+

  Agents CANNOT invoke other agents.
  Agents CANNOT spawn subagents.
  Only MAIN CONTEXT orchestrates the sequence.
```

---

## Invoking an Agent

### Option 1: Natural Language Request

Simply describe what you need:

```
"Start a new penetration testing engagement for the 10.0.0.0/24 network"
"Perform reconnaissance on target.example.com"
"Analyze vulnerabilities found in the web application"
"Develop exploitation methodology for CVE-2026-1234"
"Set up C2 infrastructure for the engagement"
"Generate the final engagement report for RED-0001"
```

The orchestrator will select the appropriate agent(s) based on keywords and context.

### Option 2: Explicit Agent Request

Request a specific agent:

```
"Use red-lead to define scope for a new engagement"
"Have red-recon perform OSINT on the target domain"
"I need red-vuln to assess exploit availability for the discovered CVEs"
"Ask red-reporter to generate the executive summary"
```

### Option 3: Task Tool Invocation

For programmatic invocation within workflows:

```python
Task(
    description="red-recon: Reconnaissance of target network",
    subagent_type="general-purpose",
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

## Orchestration Flow

### Non-Linear Kill Chain with Phase Cycling

The /red-team workflow is explicitly **non-linear** per ADR-PROJ010-001 Section 5. Real engagements are iterative -- exploitation discovers new reconnaissance targets, triggering return to earlier phases. The kill chain organizes capability, not workflow sequence.

```
                    +------------+
                    |  red-lead  |  <-- MANDATORY FIRST (scope establishment)
                    +-----+------+
                          |
                          v
          +---------------+---------------+
          |     SCOPE ESTABLISHED         |
          |  (any agent invocable now)    |
          +------+------+------+----------+
                 |      |      |
     +-----------+  +---+---+  +-----------+
     |              |       |              |
     v              v       v              v
 +--------+   +--------+  +--------+  +--------+
 |red-recon|-->|red-vuln|  |red-    |  |red-    |
 +---+----+   +---+----+  |social* |  |infra   |
     |            |        +--------+  +--------+
     |   +--------+
     |   |
     v   v
 +--------+     +--------+     +--------+
 |red-    |---->|red-     |---->|red-    |
 |exploit |     |privesc  |     |lateral |
 +--------+     +--------+     +--------+
                                    |
                    +-------+-------+
                    |       |
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

 * = RoE-GATED (requires explicit authorization in Rules of Engagement)

 Arrows show COMMON flow, not required sequence.
 After scope establishment, any agent is invocable in any order.
 Cycling between phases is explicitly supported.
```

### Orchestration Rules

1. **red-lead MUST establish scope first (MANDATORY).** No other agent operates without an active scope document.

2. **After scope establishment, any agent is invocable in any order based on engagement context.** The kill chain is a capability map, not a sequential pipeline.

3. **Phase cycling is explicitly supported:**
   - red-exploit findings trigger new red-recon (discovered new targets)
   - red-privesc discovers new vulnerabilities, triggering return to red-vuln
   - red-lateral reveals new network segments, triggering red-recon
   - Any agent can feed findings back to any prior-phase agent

4. **Circuit breaker at every agent transition.** Scope revalidation occurs before each agent invocation. See [Circuit Breaker Integration](#circuit-breaker-integration).

5. **RoE-gated agents require additional authorization:**
   - **red-persist** -- only if `persistence_authorized: true` in RoE
   - **red-exfil** -- only if `exfiltration_authorized: true` in RoE, with `data_types_permitted` specifying allowed data categories
   - **red-social** -- only if `social_engineering_authorized: true` in RoE

6. **red-reporter generates the final engagement report (mandatory last for reporting).** The engagement is not complete without a formal report. red-reporter can also be invoked mid-engagement for interim findings.

7. **red-infra can be invoked at any point** to set up or modify engagement infrastructure (C2, redirectors, payloads).

---

## Cross-Skill Integration Points

Four integration points operationalize the adversarial-collaborative dynamic between /red-team and /eng-team. These are the purple team seams where offensive findings drive defensive hardening.

### Integration Point 1: Threat-Informed Architecture

| Attribute | Value |
|-----------|-------|
| **Source** | red-recon |
| **Target** | eng-architect |
| **Data Exchanged** | Adversary TTPs, threat landscape data, attack surface intelligence |
| **Value** | Architecture decisions informed by real adversary behavior rather than theoretical threats; replaces the need for a dedicated eng-threatintel agent |
| **Workflow** | red-recon produces threat intelligence during reconnaissance; eng-architect consumes it for STRIDE/DREAD threat modeling |

### Integration Point 2: Attack Surface Validation

| Attribute | Value |
|-----------|-------|
| **Source** | red-recon, red-vuln |
| **Target** | eng-infra, eng-devsecops |
| **Data Exchanged** | Validation results against hardened targets, vulnerability scan findings |
| **Value** | Validates that infrastructure hardening and security tooling actually reduce the attack surface as intended |
| **Workflow** | red-recon and red-vuln test eng-infra hardening; findings fed to eng-devsecops for pipeline security updates |

### Integration Point 3: Secure Code vs. Exploitation

| Attribute | Value |
|-----------|-------|
| **Source** | red-exploit, red-privesc |
| **Target** | eng-security, eng-backend, eng-frontend |
| **Data Exchanged** | Exploitation results against reviewed code, bypass demonstrations |
| **Value** | Proves whether secure coding practices withstand real exploitation techniques; feedback loop drives hardening |
| **Workflow** | red-exploit tests eng-backend/eng-frontend code; red-privesc tests privilege boundaries; findings drive eng-security review priorities |

### Integration Point 4: Incident Response Validation

| Attribute | Value |
|-----------|-------|
| **Source** | red-persist, red-lateral, red-exfil |
| **Target** | eng-incident |
| **Data Exchanged** | Exercise results against response runbooks, detection gaps, evasion successes |
| **Value** | Validates IR runbooks against real adversary post-exploitation behavior |
| **Workflow** | Post-exploitation agents test eng-incident response capabilities; detection gaps inform runbook revisions |

**Evidence:** ADR-PROJ010-001 Section 5 (Cross-Skill Integration Points); A-002 Finding 7 (Netflix Attack Emulation Team validates adversarial-collaborative dynamic).

---

## Safety Alignment Compatibility

### Methodology-First Design (AD-001)

The /red-team skill is designed for compatibility with LLM safety classifiers through a methodology-first approach:

1. **Professional context framing.** All agent guidance is framed within established professional methodology (PTES, OSSTMM, NIST SP 800-115, OWASP Testing Guide). This provides the professional context that safety classifiers use to distinguish legitimate security testing from malicious activity.

2. **Methodology guidance, not exploit generation.** Agents guide practitioners to use established frameworks (Metasploit, Burp Suite, Nmap) with methodology-driven approaches. They do not generate weaponized exploit code, raw shellcode, or novel attack payloads.

3. **Authorization as safety precondition.** The mandatory scope document establishes the authorized engagement context that safety classifiers expect for offensive security content. No agent operates without this context.

4. **Tool augmentation, not tool replacement.** Agents provide methodology for using security tools, not autonomous tool execution. The human practitioner remains in the loop for all tool operations.

5. **Evidence-based reasoning.** All findings cite ATT&CK technique IDs, CVE references, and methodology standards. Speculative or theoretical attacks are explicitly marked as such.

### Potential Safety Friction Points

| Agent | Potential Friction | Mitigation |
|-------|-------------------|------------|
| red-exploit | Exploitation methodology may trigger safety classifiers | Frame within PTES methodology; reference established tools; never generate raw exploit code |
| red-persist | Persistence techniques may appear malicious | Frame within authorized engagement scope; reference ATT&CK technique IDs; emphasize detection value |
| red-social | Social engineering may trigger manipulation classifiers | Frame within OSSTMM social engineering methodology; emphasize authorized testing context |
| red-exfil | Data exfiltration may appear as data theft | Frame within authorized scope; emphasize evidence vault storage; reference DLP testing methodology |

---

## Circuit Breaker Integration

Per ADR-PROJ010-006 (F-002 R-AUTH-006), a circuit breaker check occurs at every agent transition:

### Circuit Breaker Protocol

```
1. Agent completes work and returns output to orchestrator
2. Orchestrator selects next agent based on engagement context
3. CIRCUIT BREAKER CHECK:
   a. Scope revalidation: Is the target still within authorized scope?
   b. Time window check: Is the engagement still within authorized time?
   c. Technique check: Are the next agent's techniques in the allowlist?
   d. Agent authorization: Is the next agent in the agent_authorizations list?
   e. RoE gate: If next agent is RoE-gated, is it explicitly authorized?
   f. Cascading failure detection: Has any prior agent reported anomalies?
4. If ALL checks pass: Invoke next agent with scope context
5. If ANY check fails: HALT and escalate to red-lead for scope review
```

### Cascading Failure Detection

If an agent encounters unexpected behavior (target responds differently than expected, scope boundary ambiguity, tool failure affecting safety), it MUST:

1. Immediately halt current operations
2. Log the anomaly with full context
3. Return to the orchestrator with a SCOPE_REVIEW_REQUIRED flag
4. The orchestrator routes to red-lead for assessment before any further agent invocation

---

## Authorization Architecture

The /red-team skill implements a three-layer defense-in-depth authorization architecture per ADR-PROJ010-006:

### Layer 1: Structural Authorization (Pre-Engagement)

Static constraints defined before the engagement begins:

| Component | Function |
|-----------|----------|
| Scope Document | Defines authorized targets, techniques, time window, exclusions |
| Target Allowlist | IP ranges, domains, and applications explicitly permitted |
| Technique Allowlist | ATT&CK technique IDs each agent may use |
| Time Window | Start and end timestamps for authorized operations |
| Exclusion List | Systems and networks explicitly forbidden |
| Rules of Engagement | Escalation procedures, communication channels, gating conditions |
| Agent Authorizations | Which of the 11 agents are permitted for this engagement |

### Layer 2: Dynamic Authorization (During Engagement)

Runtime enforcement components that validate every action:

| Component | Function |
|-----------|----------|
| Scope Oracle | Validates every agent action against the scope document before execution |
| Tool Proxy | Default-deny policy; agents access tools only through the proxy, which enforces technique allowlist |
| Network Enforcer | Validates target addresses against the authorized target list |
| Credential Broker | Issues scoped credentials; agents never see raw credentials |

### Layer 3: Retrospective Authorization (Post-Engagement)

After-action verification that all operations remained within scope:

| Component | Function |
|-----------|----------|
| Action Log Review | Tamper-evident audit trail of all agent actions reviewed for scope compliance |
| Evidence Verification | All evidence artifacts verified against scope document targets |
| Compliance Report | Formal attestation that the engagement operated within authorized boundaries |

---

## Mandatory Persistence (P-002)

All agent outputs MUST be persisted to files. Transient-only output is a P-002 violation.

### Output Location Convention

```
skills/red-team/output/{engagement-id}/{agent-name}-{topic-slug}.md
```

**Examples:**
- `skills/red-team/output/RED-0001/red-lead-scope.md`
- `skills/red-team/output/RED-0001/red-recon-network-enumeration.md`
- `skills/red-team/output/RED-0001/red-vuln-cve-analysis.md`
- `skills/red-team/output/RED-0001/red-reporter-final-report.md`

### Evidence Storage

Evidence artifacts (screenshots, tool output, logs) are stored in:

```
skills/red-team/output/{engagement-id}/evidence/
```

---

## Adversarial Quality Mode

For C2+ engagement deliverables, the /adversary skill integration applies:

| Criticality | Application |
|-------------|-------------|
| C1 (Routine) | Self-review (S-010) on agent outputs |
| C2 (Standard) | S-007 Constitutional compliance + S-002 Devil's Advocate on methodology choices |
| C3 (Significant) | C2 + S-004 Pre-Mortem on engagement risks |
| C4 (Critical) | Full tournament review via /adversary on engagement reports and scope documents |

The scope document itself is always C4 criticality (irreversible authorization decision).

---

## Constitutional Compliance

All agents adhere to the **Jerry Constitution v1.0**:

| Principle | Requirement |
|-----------|-------------|
| P-001: Truth and Accuracy | All findings evidence-based with ATT&CK citations |
| P-002: File Persistence | All outputs persisted to files |
| P-003: No Recursive Subagents | Agents are workers, not orchestrators |
| P-020: User Authority | User can override any agent decision; user authorizes all scopes |
| P-022: No Deception | Limitations disclosed; confidence levels honest |
| R-020: Authorization Verification | Scope verification before every agent execution |

### PROJ-010 Specific Requirements

| Requirement | Enforcement |
|-------------|-------------|
| R-001: Secure by Design | Authorization is architectural, not procedural |
| R-018: Real Offensive Techniques | ATT&CK technique IDs used throughout |
| R-012: Tool Integration | Three-level degradation (AD-010) |
| R-010: LLM Portability | Portable agent schema with markdown body format |

---

## Quick Reference

### Common Workflows

| Need | Agent | Command Example |
|------|-------|-----------------|
| Start new engagement | red-lead | "Define scope for a penetration test of 10.0.0.0/24" |
| Network reconnaissance | red-recon | "Enumerate services on the target network" |
| Vulnerability analysis | red-vuln | "Assess exploit availability for discovered CVEs" |
| Exploitation methodology | red-exploit | "Develop exploitation approach for CVE-2026-1234" |
| Privilege escalation | red-privesc | "Identify privilege escalation paths on the compromised host" |
| Lateral movement | red-lateral | "Plan lateral movement to the domain controller" |
| Persistence (RoE-gated) | red-persist | "Establish persistence methodology for the engagement" |
| Data exfiltration (RoE-gated) | red-exfil | "Plan exfiltration of test data within scope" |
| C2 infrastructure | red-infra | "Set up C2 framework for the engagement" |
| Social engineering (RoE-gated) | red-social | "Design phishing campaign methodology for the engagement" |
| Engagement report | red-reporter | "Generate final engagement report for RED-0001" |

### Agent Selection Hints

| Keywords | Likely Agent |
|----------|--------------|
| scope, RoE, engagement, authorization, rules | red-lead |
| recon, OSINT, enumerate, scan, fingerprint, attack surface | red-recon |
| vulnerability, CVE, risk score, exploit availability | red-vuln |
| exploit, payload, initial access, PoC, bypass | red-exploit |
| privilege, escalation, credential, token, SYSTEM, root | red-privesc |
| lateral, pivot, tunnel, internal, living-off-the-land | red-lateral |
| persist, backdoor, scheduled task, rootkit, implant | red-persist |
| exfil, data, covert channel, DLP, collection | red-exfil |
| report, findings, executive summary, remediation | red-reporter |
| C2, command and control, infrastructure, payload, redirector | red-infra |
| phishing, social engineering, pretext, vishing | red-social |

### Defense Evasion Ownership

| Owner | Evasion Domain | Techniques |
|-------|---------------|------------|
| red-infra | Tool-level | C2 obfuscation, payload encoding/packing, sandbox evasion |
| red-exploit | Execution-time | Process injection, signed binary proxy execution |
| red-privesc | Credential-based | Access token manipulation |
| red-lateral | Network-level | Traffic signaling, protocol tunneling |
| red-persist | Persistence-phase | Indicator removal, rootkits, timestomping |
| red-exfil | Exfiltration-phase | Data encoding, encrypted channels |

---

## References

| Source | Content |
|--------|---------|
| ADR-PROJ010-001 | Agent Team Architecture (21-agent roster, handoff protocols, defense evasion model) |
| ADR-PROJ010-006 | Authorization & Scope Control (three-layer defense-in-depth) |
| ADR-PROJ010-002 | Skill Routing & Invocation |
| ADR-PROJ010-003 | LLM Portability Architecture |
| A-002 | Red team organizational patterns from 7 elite organizations |
| A-003 | MITRE ATT&CK 14-tactic coverage analysis |
| A-004 | Final roster with evidence matrix |
| B-001 | MITRE ATT&CK framework research |
| B-002 | PTES and OSSTMM methodology research |
| S-001 | Cross-stream synthesis findings |
| `docs/governance/JERRY_CONSTITUTION.md` | Constitutional principles |
| `.context/rules/quality-enforcement.md` | Quality gate thresholds |

---

*Skill Version: 1.0.0*
*Constitutional Compliance: Jerry Constitution v1.0*
*SSOT: ADR-PROJ010-001, ADR-PROJ010-006*
*Created: 2026-02-22*
