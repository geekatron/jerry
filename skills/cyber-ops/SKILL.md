---
name: cyber-ops
description: "Engagement lifecycle coordinator for /red-team, /blue-team, and /rainbow. Orchestrates the 6-phase engagement lifecycle (Define, Provision, Execute, Analyze, Report, Teardown) across 3 modes: solo purple team, split red-vs-blue teams, and single-team operations. Invoke when setting up, running, or tearing down a security engagement. NOT for direct penetration testing, threat detection, or tool execution."
version: "1.0.0"
agents:
  - cyber-ops-lead
  - cyber-ops-provision
  - cyber-ops-analyze
  - cyber-ops-teardown
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, WebSearch, WebFetch, mcp__context7__resolve-library-id, mcp__context7__query-docs
activation-keywords:
  - "engagement"
  - "cyber-ops"
  - "purple team exercise"
  - "set up engagement"
  - "engagement lifecycle"
  - "define engagement"
  - "provision engagement"
  - "tear down engagement"
  - "engagement report"
  - "engagement scope"
  - "split team"
  - "red vs blue exercise"
---

# Cyber-Ops Skill

> **Version:** 1.0.0
> **Framework:** Jerry Cyber-Ops
> **Constitutional Compliance:** Jerry Constitution v1.0

## Document Sections

| Section | Purpose |
|---------|---------|
| [Document Audience](#document-audience-triple-lens) | Triple-Lens audience guide |
| [Purpose](#purpose) | Skill overview and lifecycle coordination role |
| [When to Use This Skill](#when-to-use-this-skill) | Activation triggers and engagement modes |
| [When NOT to Use This Skill](#when-not-to-use-this-skill) | Anti-patterns and misrouting consequences |
| [Available Agents](#available-agents) | 4-agent roster with roles and output locations |
| [P-003 Compliance](#p-003-compliance) | Flat invocation hierarchy from MAIN CONTEXT |
| [Invoking an Agent](#invoking-an-agent) | Three invocation methods with examples |
| [Engagement Lifecycle](#engagement-lifecycle) | 6-phase state machine (Define through Teardown) |
| [Engagement Modes](#engagement-modes) | Purple, split, and single-team configurations |
| [Constitutional Compliance](#constitutional-compliance) | Governing principles |
| [Quick Reference](#quick-reference) | Common workflows and agent selection hints |
| [Routing Disambiguation](#routing-disambiguation) | When this skill is the wrong choice |
| [References](#references) | Source document traceability |

## Document Audience (Triple-Lens)

This SKILL.md serves multiple audiences:

| Level | Audience | Sections to Focus On |
|-------|----------|---------------------|
| **L0 (Stakeholder)** | Engagement managers, leadership | [Purpose](#purpose), [When to Use This Skill](#when-to-use-this-skill), [Quick Reference](#quick-reference) |
| **L1 (Practitioner)** | Security operators invoking agents | [Available Agents](#available-agents), [Invoking an Agent](#invoking-an-agent), [Engagement Lifecycle](#engagement-lifecycle), [Engagement Modes](#engagement-modes) |
| **L2 (Architect)** | Framework designers, governance reviewers | [P-003 Compliance](#p-003-compliance), [Constitutional Compliance](#constitutional-compliance), [Routing Disambiguation](#routing-disambiguation) |

---

## Purpose

The Cyber-Ops skill is an **engagement lifecycle coordinator**. It does NOT perform offensive testing, defensive detection, or tool execution. Instead, it orchestrates the skills that do -- `/red-team`, `/blue-team`, and `/rainbow` -- across a structured 6-phase engagement lifecycle.

### Key Capabilities

- **Lifecycle Orchestration** -- Manages the Define, Provision, Execute, Analyze, Report, and Teardown phases as a state machine with confirmation gates (G1-G7)
- **Multi-Mode Engagement** -- Supports three engagement configurations: solo purple team, split red-vs-blue teams, and single-team operations
- **Infrastructure Lifecycle** -- Provisions and tears down engagement infrastructure (proxy chains, detection sensors, C2 frameworks) through delegation
- **Cross-Team Correlation** -- Correlates red team findings with blue team detections to produce gap analysis and ATT&CK coverage mapping
- **Evidence Archival** -- Manages secure archival with SHA-256 integrity verification before infrastructure destruction

### What This Skill Is NOT

This skill is a **coordinator**, not an operational skill. It does NOT:

- Execute penetration tests or offensive techniques (that is `/red-team`)
- Run threat detection, malware analysis, or YARA rules (that is `/blue-team`)
- Execute security tools, scanners, or exploit frameworks (that is `/rainbow`)
- Replace red-lead's scope authority or blue-lead's detection authority
- Operate without explicit human confirmation at each lifecycle gate

---

## When to Use This Skill

Activate when:

- Setting up a new security engagement (any mode)
- Running a purple team exercise with coordinated red and blue teams
- Provisioning engagement infrastructure (proxy chains, sensors, C2)
- Tearing down engagement infrastructure after completion
- Generating cross-team analysis comparing attack findings vs detection coverage
- Coordinating a split red-vs-blue exercise with independent teams
- Archiving engagement evidence for post-engagement review

## When NOT to Use This Skill

NEVER invoke this skill when:

- Task is direct penetration testing or offensive methodology -- Consequence: Cyber-ops loads lifecycle coordination agents, not kill chain agents; ATT&CK technique guidance absent; use `/red-team` instead
- Task is threat detection, malware analysis, or compliance auditing -- Consequence: Cyber-ops has no detection or forensic agents; YARA, Sigma, D3FEND methodology absent; use `/blue-team` instead
- Task is tool-assisted scanning, SBOM generation, or exploit execution -- Consequence: Cyber-ops delegates to /rainbow but does not execute tools directly; use `/rainbow` instead
- No engagement context exists (general security research) -- Consequence: Lifecycle agents require engagement configuration; agents halt at validation gates; use `/problem-solving` instead
- Building secure software or reviewing code for vulnerabilities -- Consequence: Cyber-ops is operations-focused, not engineering-focused; SDLC methodology absent; use `/eng-team` instead

---

## Available Agents

| Agent | Role | Tier | Model | Output Location |
|-------|------|------|-------|-----------------|
| `cyber-ops-lead` | Engagement Lifecycle Coordinator | T5 (Full) | opus | `work/engagements/{engagement-id}/cyber-ops-lead-{topic-slug}.md` |
| `cyber-ops-provision` | Infrastructure Lifecycle Manager | T2 (Read-Write) | sonnet | `work/engagements/{engagement-id}/cyber-ops-provision-{topic-slug}.md` |
| `cyber-ops-analyze` | Cross-Team Correlation Analyst | T2 (Read-Write) | opus | `work/engagements/{engagement-id}/cyber-ops-analyze-{topic-slug}.md` |
| `cyber-ops-teardown` | Cleanup and Archival Orchestrator | T2 (Read-Write) | sonnet | `work/engagements/{engagement-id}/cyber-ops-teardown-{topic-slug}.md` |

---

## P-003 Compliance

All cyber-ops agents are invoked **flat** from the MAIN CONTEXT. cyber-ops-lead coordinates by producing state files and handoff instructions, NOT by spawning subagents.

```
P-003 AGENT HIERARCHY:
======================

  +-------------------+
  | MAIN CONTEXT      |  <-- Orchestrator (Claude session)
  | (orchestrator)    |
  +-------------------+
     |    |    |    |
     v    v    v    v
  +------+ +------+ +------+ +------+
  |cyber-| |cyber-| |cyber-| |cyber-|
  |ops-  | |ops-  | |ops-  | |ops-  |
  |lead  | |provi-| |analy-| |tear- |
  |      | |sion  | |ze    | |down  |
  +------+ +------+ +------+ +------+

  /red-team, /blue-team, and /rainbow agents
  are ALSO invoked flat from MAIN CONTEXT --
  NOT nested under cyber-ops agents.

  +-------------------+
  | MAIN CONTEXT      |
  +-------------------+
     |  |  |  |  |  |  |  |
     v  v  v  v  v  v  v  v
  cyber-ops-*  red-*  blue-*  rainbow-*

  NO agent invokes another agent.
  Only MAIN CONTEXT orchestrates the sequence.
```

---

## Invoking an Agent

### Option 1: Natural Language Request

Simply describe what you need:

```
"Set up a new purple team engagement for the 10.0.0.0/24 network"
"Provision infrastructure for engagement ENG-0001"
"Analyze red team vs blue team results for the engagement"
"Tear down engagement ENG-0001 infrastructure"
```

The orchestrator will select the appropriate agent(s) based on keywords and context.

### Option 2: Explicit Agent Request

Request a specific agent:

```
"Use cyber-ops-lead to define a split red-vs-blue engagement"
"Have cyber-ops-provision set up the proxy chain and detection sensors"
"I need cyber-ops-analyze to correlate attack findings with detections"
"Ask cyber-ops-teardown to archive and destroy the engagement infrastructure"
```

### Option 3: Native Agent Invocation

Agents are registered via their definition files and discovered by Claude Code automatically. The orchestrator invokes them as named subagents:

```python
Task(
    description="cyber-ops-lead: Define purple team engagement",
    subagent_type="cyber-ops-lead",
    prompt="""
## CYBER-OPS CONTEXT (REQUIRED)
- **Engagement Mode:** purple
- **Target Scope:** 10.0.0.0/24
- **Requested Phase:** Define

## TASK
Define a purple team engagement for the specified target scope.
Produce engagement configuration YAML and await operator confirmation (G1).
"""
)
```

Claude Code enforces the agent's `tools` frontmatter -- cyber-ops-lead has access to all tools including Task; worker agents (provision, analyze, teardown) have T2 Read-Write access only.

---

## Engagement Lifecycle

The engagement lifecycle is a 6-phase state machine with confirmation gates (G1-G7) that require explicit operator approval before proceeding.

### Phase Diagram

```
  DEFINE         PROVISION       EXECUTE         ANALYZE        REPORT         TEARDOWN
+----------+   +----------+   +----------+   +----------+   +----------+   +----------+
|          |   |          |   |          |   |          |   |          |   |          |
| Config   |-->| Infra    |-->| Red/Blue |-->| Correlate|-->| Generate |-->| Archive  |
| YAML     |   | Standup  |   | Ops      |   | Findings |   | Report   |   | Destroy  |
|          |   |          |   |          |   |          |   |          |   |          |
+----+-----+   +----+-----+   +----+-----+   +----+-----+   +----+-----+   +----+-----+
     |              |              |              |              |              |
    [G1]           [G2,G3]        [G4]           [G5]           [G5]          [G6,G7]
```

### Phase Definitions

| Phase | Agent | Description | Gates |
|-------|-------|-------------|-------|
| **1. Define** | cyber-ops-lead | Parse requirements, produce engagement config YAML, define mode and scope | G1: Operator approves engagement config |
| **2. Provision** | cyber-ops-provision | Stand up infrastructure (proxy chains, C2, sensors, log collectors) | G2: Provision plan approved; G3: Infrastructure verified operational |
| **3. Execute** | red-lead, blue-lead (via MAIN CONTEXT) | Operational phase -- red team attacks, blue team defends (delegated to /red-team, /blue-team) | G4: Execution complete or halted |
| **4. Analyze** | cyber-ops-analyze | Correlate red findings with blue detections, ATT&CK coverage mapping, gap analysis | G5: Analysis reviewed by operator |
| **5. Report** | cyber-ops-lead | Generate engagement report from analysis artifacts | G5: Report approved by operator |
| **6. Teardown** | cyber-ops-teardown | Archive evidence (SHA-256 checksums), revoke credentials, destroy infrastructure | G6: Archive verified; G7: Destruction confirmed |

### Confirmation Gates

| Gate | Phase Boundary | Confirmation Required |
|------|----------------|----------------------|
| G1 | Define -> Provision | "Engagement config approved. Proceed to provisioning?" |
| G2 | Provision planning | "Provision plan reviewed. Stand up infrastructure?" |
| G3 | Provision -> Execute | "Infrastructure verified. Begin execution phase?" |
| G4 | Execute -> Analyze | "Execution complete. Proceed to analysis?" |
| G5 | Analyze -> Report | "Analysis and report reviewed. Approve?" |
| G6 | Report -> Teardown | "Archive integrity verified. Proceed to destruction?" |
| G7 | Teardown complete | "Infrastructure destroyed. Engagement closed?" |

Every gate requires explicit operator confirmation per P-020 (User Authority). No automatic progression through gates.

---

## Engagement Modes

Three modes configure how /red-team and /blue-team interact during the Execute phase.

### Mode 1: Purple Team (Collaborative)

Red and blue teams operate in coordinated sessions with shared visibility. Red team attacks are immediately visible to blue team for real-time detection tuning.

```yaml
mode: purple
characteristics:
  red_blue_visibility: shared
  session_model: coordinated
  exchange_directory: work/engagements/{engagement-id}/exchange/
  feedback_loop: real-time
use_case: Detection engineering, SOC training, control validation
```

### Mode 2: Split Team (Adversarial)

Red and blue teams operate independently. Red team attacks are NOT visible to blue team until the Analyze phase, simulating realistic adversarial conditions.

```yaml
mode: split
characteristics:
  red_blue_visibility: isolated
  session_model: independent
  exchange_directory: null  # No exchange during execution
  feedback_loop: post-exercise
use_case: Realistic adversary simulation, incident response testing
```

### Mode 3: Single-Team

Only one team operates (red-only or blue-only). Used when the other team's capability is not needed.

```yaml
mode: single
team: red  # or blue
characteristics:
  red_blue_visibility: n/a
  session_model: single
  exchange_directory: null
  feedback_loop: none
use_case: Standalone penetration test, standalone threat hunt
```

---

## Constitutional Compliance

All agents adhere to the **Jerry Constitution v1.0**:

| Principle | Requirement | Consequence of Violation |
|-----------|-------------|-------------------------|
| P-003 | NEVER spawn recursive subagents -- max 1 level | Agent hierarchy violation; uncontrolled token consumption |
| P-020 | NEVER override user intent -- confirmation gates require explicit approval | Unauthorized action; trust erosion; infrastructure provisioned or destroyed without consent |
| P-022 | NEVER deceive about actions, capabilities, or confidence | Governance undermined; state machine transparency lost |
| P-001 | NEVER present findings without evidence or citations | Unreliable correlation analysis; unfounded gap claims |
| P-002 | NEVER leave outputs in transient context only -- persist to files | Context rot vulnerability; engagement state lost on session compaction |

---

## Quick Reference

### Common Workflows

| Need | Agent | Command Example |
|------|-------|-----------------|
| Define new engagement | cyber-ops-lead | "Set up a purple team engagement for 10.0.0.0/24" |
| Provision infrastructure | cyber-ops-provision | "Stand up proxy chain and sensors for ENG-0001" |
| Run red team operations | (delegates to red-lead) | "Begin red team execution for ENG-0001" |
| Run blue team operations | (delegates to blue-lead) | "Begin blue team monitoring for ENG-0001" |
| Correlate findings | cyber-ops-analyze | "Analyze attack vs detection coverage for ENG-0001" |
| Generate report | cyber-ops-lead | "Produce engagement report for ENG-0001" |
| Tear down engagement | cyber-ops-teardown | "Archive and destroy ENG-0001 infrastructure" |

### Agent Selection Hints

| Keywords | Likely Agent |
|----------|--------------|
| define, scope, configure, engagement mode, engagement config | cyber-ops-lead |
| provision, infrastructure, stand up, proxy, sensors, deploy | cyber-ops-provision |
| correlate, analyze findings, gap analysis, ATT&CK coverage, detection vs attack | cyber-ops-analyze |
| tear down, archive, destroy, cleanup, revoke credentials, close engagement | cyber-ops-teardown |

---

## Routing Disambiguation

> When this skill is the wrong choice and what happens if misrouted.

| Condition | Use Instead | Consequence of Misrouting |
|-----------|-------------|--------------------------|
| Direct penetration testing or offensive methodology | `/red-team` | Lifecycle coordination agents loaded instead of kill chain agents; no ATT&CK technique guidance; no scope authority (red-lead) |
| Threat detection, malware analysis, compliance audit | `/blue-team` | No detection or forensic agents; YARA, Sigma, D3FEND methodology absent |
| Tool-assisted scanning, SBOM, exploit framework execution | `/rainbow` | Cyber-ops delegates to /rainbow but cannot execute tools directly; zone model not loaded |
| Building secure software, security architecture | `/eng-team` | Engagement lifecycle agents loaded instead of SDLC agents; no STRIDE/DREAD, OWASP, ASVS methodology |
| Adversarial quality review of deliverables | `/adversary` | Engagement lifecycle loaded instead of S-014 quality rubric; quality scoring unavailable |
| General security research without engagement context | `/problem-solving` | Lifecycle agents require engagement config; agents halt at validation gates |

---

## References

| Source | Content |
|--------|---------|
| `skills/red-team/SKILL.md` | Offensive security skill (delegated to during Execute phase) |
| `skills/blue-team/SKILL.md` | Defensive security skill (delegated to during Execute phase) |
| `skills/rainbow/SKILL.md` | Tool execution skill (delegated to for infrastructure operations) |
| `docs/governance/JERRY_CONSTITUTION.md` | Constitutional principles |
| `.context/rules/quality-enforcement.md` | Quality gate thresholds |
| `.context/rules/agent-development-standards.md` | Agent definition standards (H-34) |
| `.context/rules/skill-standards.md` | Skill structure standards (H-25, H-26) |

---

*Skill Version: 1.0.0*
*Constitutional Compliance: Jerry Constitution v1.0*
*Created: 2026-03-26*
