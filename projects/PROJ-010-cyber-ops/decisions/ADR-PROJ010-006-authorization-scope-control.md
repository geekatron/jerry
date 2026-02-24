# ADR-PROJ010-006: Authorization & Scope Control Architecture -- Three-Layer Defense-in-Depth

<!--
DOCUMENT-ID: ADR-PROJ010-006
AUTHOR: ps-architect agent
DATE: 2026-02-22
STATUS: PROPOSED
PARENT-FEATURE: FEAT-015 (Authorization & Scope Control Architecture)
PARENT-EPIC: EPIC-002 (Architecture & Design)
PROJECT: PROJ-010-cyber-ops
ADR-ID: ADR-PROJ010-006
TYPE: Architecture Decision Record
CRITICALITY: C4 (Critical -- irreversible, architecture/governance; most security-critical ADR in PROJ-010)
-->

> **ADR ID:** ADR-PROJ010-006
> **Version:** 1.0.0
> **Date:** 2026-02-22
> **Author:** ps-architect
> **Status:** PROPOSED
> **Deciders:** User (P-020 authority), ps-architect (recommendation)
> **Quality Target:** >= 0.95
> **Criticality:** C4 (Critical -- most security-critical ADR in PROJ-010)
> **Parent Feature:** FEAT-015 (Authorization & Scope Control Architecture)
> **Parent Epic:** EPIC-002 (Architecture & Design)

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Status](#status) | Current decision lifecycle stage and ratification requirements |
| [Context](#context) | Why this decision is needed; threat landscape; design-before-build rationale |
| [Decision](#decision) | Three-layer authorization architecture, scope enforcement components, per-agent model, isolation, progressive autonomy, guardrails, OWASP coverage, audit requirements |
| [Options Considered](#options-considered) | Four authorization approaches evaluated with trade-off analysis |
| [Consequences](#consequences) | Positive, negative, and neutral outcomes of the selected architecture |
| [Evidence Base](#evidence-base) | Research findings from F-002, F-003, S-001, S-002 that ground every design choice |
| [Compliance](#compliance) | Alignment with R-001, R-020, P-003, P-020, OWASP Agentic AI Top 10 |
| [Related Decisions](#related-decisions) | Upstream and downstream decision linkages |
| [Open Questions](#open-questions) | Genuine ambiguities requiring Phase 2 design resolution |
| [References](#references) | Source citations with publication dates and content descriptions |

---

## Status

**PROPOSED** -- This ADR requires full C4 governance review before acceptance:

1. **Adversarial review** by /adversary: PENDING (all 10 selected strategies required per C4 criticality)
2. **User ratification** per P-020 (User Authority): PENDING

**Design-Before-Build Rationale (R-001):** This ADR is written before any red-team agent implementation begins. The authorization architecture must be formalized, reviewed, and accepted before any agent with offensive capabilities is built. This is the foundational security constraint -- the scope enforcement infrastructure is the trust boundary within which all /red-team agents operate. Building agents before the trust boundary is defined inverts the security model.

**Downstream Dependency Gating:** The following Phase 2 and Phase 3 work items are blocked until this ADR reaches ACCEPTED status:

- All /red-team agent definition files (11 agents)
- FEAT-015 implementation tasks for scope enforcement components
- Phase 3 agent development for any agent with tool access
- Phase 5 purple team validation test plans (which test this architecture)

---

## Context

### Why This Decision Is Needed

PROJ-010 defines two Claude Code skills -- /eng-team (10 defensive security agents) and /red-team (11 offensive security agents) -- that provide methodology guidance for enterprise security operations. The /red-team skill guides real offensive techniques mapped to MITRE ATT&CK (R-018), which creates a category of risk absent from conventional LLM agent systems: agents that guide operations against live targets within authorized scope boundaries. A failure in scope enforcement does not produce incorrect output -- it produces unauthorized access to systems the engagement is not permitted to test.

This ADR formalizes the authorization and scope control architecture that makes out-of-scope actions structurally impossible rather than procedurally prevented. It is the primary ADR for R-020 (Authorization Verification) and the most security-critical architectural decision in the entire project.

### Threat Landscape: OWASP Agentic AI Top 10

The OWASP GenAI Security Project released the Top 10 for Agentic Applications in December 2025, developed through collaboration with over 100 security researchers, industry practitioners, and technology providers (OWASP GenAI, December 2025; F-002 Finding 1). Unlike the LLM Top 10 which focuses on content generation risks, the Agentic Top 10 addresses risks from autonomous action -- what happens when models can plan, persist, and delegate across tools and systems. For /red-team, four risks represent the highest priority:

| Risk ID | Risk Name | /red-team Threat |
|---------|-----------|-----------------|
| ASI01 | Agent Goal Hijack | Red team agent goals redirected to unauthorized targets via hidden prompts or injected instructions |
| ASI02 | Tool Misuse | Red team tools (nmap, Metasploit, sqlmap) used against targets not in engagement scope |
| ASI03 | Identity and Privilege Abuse | Red team credentials used to access production systems outside engagement scope |
| ASI08 | Cascading Failures | Failed exploitation triggers automated escalation beyond authorized scope boundaries |

The remaining six risks (ASI04 Supply Chain, ASI05 Unexpected Code Execution, ASI06 Memory/Context Poisoning, ASI07 Insecure Inter-Agent Communication, ASI09 Human-Agent Trust Exploitation, ASI10 Rogue Agents) are addressed by the architecture but represent lower priority for the scope control decision.

### Cross-Stream Convergence: Scope Over Oversight

Three independent research streams converged on the same conclusion (S-001 Convergence 3):

- **Stream F** (Authorization Architecture): Analysis of the OWASP Agentic AI Top 10 and the AWS Agentic AI Security Scoping Matrix concluded that authorization scope bounds risk more effectively than human oversight (F-002 Finding 2).
- **Stream C** (Tool Integration Security): Independently designed scoped credential management where agents never see raw credentials and all tool execution is sandboxed (S-001).
- **Stream D** (LLM Boundaries): Independently concluded that human-in-the-loop is required not because agents need approval for every action, but because agents cannot make authorization decisions, legal judgments, or novel discoveries (S-001).

**Consolidated Principle:** An agent with properly constrained authorization scopes poses bounded risk regardless of autonomy level. An agent that can only reach authorized targets, invoke authorized techniques, and write to designated evidence storage has a defined blast radius. Security is an architectural property enforced by infrastructure, not an operational procedure relying on human vigilance.

### Production Validation

Two production agentic security platforms validate the core architectural patterns (F-002 Findings 4):

- **XBOW** coordinates hundreds of autonomous AI agents, each focused on a specific attack vector, operating within defined application scope boundaries. All actions are logged with timestamps for audit trail reconstruction (XBOW, 2025).
- **PentAGI** runs fully autonomous penetration testing in isolated Docker environments with 20+ professional security tools, demonstrating that containerized isolation with scoped tool access is a production-viable safety pattern (GitHub/vxcontrol, 2025).

### Constraints

| Constraint | Source | Impact on Architecture |
|------------|--------|------------------------|
| R-001: Secure by Design | PLAN.md | Authorization architecture must be formalized before agent implementation begins |
| R-020: Authorization Verification | PLAN.md | Scope verification required before every tool execution; evidence preservation for audit |
| P-003: No Recursive Subagents | Jerry Constitution (H-01) | Scope enforcement cannot rely on nested agent hierarchies; single orchestrator-worker level |
| P-020: User Authority | Jerry Constitution (H-02) | User defines engagement scope through red-lead; architecture enforces but never overrides user intent |
| AD-001: Methodology-First Design | S-002 | Agents provide methodology guidance, not autonomous execution; scope constrains guidance boundaries |
| AD-010: Standalone Capable | S-002 | All agents function without tools; scope enforcement applies to tool-augmented operation |

---

## Decision

### 1. Three-Layer Authorization Architecture (AD-004)

The /red-team authorization architecture implements three defense-in-depth layers. Each layer operates independently -- failure of any single layer does not compromise the other two. The layers are designed so that out-of-scope actions are structurally impossible, not procedurally prevented.

#### Layer 1: Structural Authorization (Pre-Engagement)

Layer 1 defines the authorization boundary as an immutable data artifact before any active operations begin. Scope is treated as data, not as a prompt instruction. This layer is owned by red-lead and is the highest-trust component of the authorization architecture.

| Component | Description | Owner | Enforcement |
|-----------|-------------|-------|-------------|
| **Scope Document** | Signed YAML defining authorized targets, techniques, time windows, exclusions, and rules of engagement | red-lead | Loaded at engagement start; immutable during engagement; cannot be modified without re-authorization |
| **Target Allowlist** | Explicit list of IP ranges, domains, and applications authorized for testing | red-lead | Network-level enforcement; all agent network access filtered through scope proxy |
| **Technique Allowlist** | MITRE ATT&CK technique IDs authorized for this engagement | red-lead | Tool access gated by technique mapping; unauthorized techniques structurally unavailable |
| **Time Window** | Start/end timestamps for engagement authorization | red-lead | Credential expiration tied to time window; agent access automatically revoked at window close |
| **Exclusion List** | Explicit systems, networks, and data types that must not be touched | red-lead | Deny rules checked before every tool invocation; exclusions supersede all allow rules |
| **Rules of Engagement** | Engagement-specific behavioral constraints (e.g., no denial-of-service, no data destruction) | red-lead | Encoded as scope oracle policy rules; enforced at runtime alongside target and technique checks |

**Evidence basis:** F-002 Pattern 1 (Pre-Engagement Scope Definition); S-002 Layer 1 specification; F-003 OPA/Rego architectural patterns for policy-as-data.

#### Layer 2: Dynamic Authorization (Runtime)

Layer 2 intercepts and validates every agent action at runtime. Four enforcement components operate in a separate trust domain from the agents they govern. Agents cannot modify, bypass, or disable any Layer 2 component.

| Component | Function | Trust Level | Failure Mode |
|-----------|----------|-------------|--------------|
| **Scope Oracle** | Evaluates proposed actions against compiled scope rules; returns allow/deny decisions with reasons | High -- separate process with own trust domain; agents cannot modify oracle | Default deny; agents cannot operate if oracle unavailable |
| **Tool Proxy** | Intercepts all tool invocations; validates target and technique parameters against scope before permitting execution | High -- the only path to tool access; agents never invoke tools directly | Tools inaccessible without proxy; agent degrades to standalone mode (AD-010) |
| **Network Enforcer** | Firewall/proxy rules derived from scope document; restricts network reachability to authorized targets and ports | High -- infrastructure-level enforcement; operates below agent process boundary | No network access outside scope; fail-closed; agent network requests to unauthorized destinations silently dropped |
| **Credential Broker** | Provides ephemeral, scope-bounded, time-limited tokens; agents never see raw credentials | High -- mediates all credential access; credentials not stored in agent context | Credentials expire at window close; scope-limited blast radius even if agent is compromised |

**Evidence basis:** F-002 Pattern 2 (Runtime Scope Enforcement), Finding 6 (ephemeral credentials); S-002 Layer 2 specification; NVIDIA credential broker pattern (NVIDIA Developer Blog, 2025); Strata Identity JIT provisioning (Strata Identity, 2025).

#### Layer 3: Retrospective Authorization (Post-Execution)

Layer 3 performs post-engagement audit verification. This layer is owned by red-reporter and provides the compliance attestation that the engagement operated within authorized scope.

| Activity | Description | Owner | Automation |
|----------|-------------|-------|-----------|
| **Action Log Review** | Every agent action compared against scope document to verify compliance | red-reporter | Automated scope compliance check on tamper-evident action logs |
| **Evidence Verification** | All findings traced from discovery through agent action to scope authorization | red-reporter | Chain-of-custody verification; finding-to-authorization trace |
| **Scope Deviation Detection** | Identification of any actions that approached or touched scope boundaries | red-lead | Automated boundary proximity analysis; near-miss reporting |
| **Compliance Report** | Formal attestation that the engagement stayed within authorized scope | red-lead, red-reporter | Generated from audit trail; requires red-lead sign-off |

**Evidence basis:** F-002 Pattern 3 (Post-Execution Audit Verification); S-002 Layer 3 specification; XBOW audit trail pattern (XBOW, 2025); PentAGI logging within isolated Docker environments (GitHub/vxcontrol, 2025).

### 2. Seven Scope Enforcement Components

Seven components form the scope enforcement infrastructure. These operate independently of agent code -- agents cannot modify, bypass, or disable any component. Each component has a defined function, trust level, and failure mode.

| Component | Function | Trust Level | Failure Mode |
|-----------|----------|-------------|--------------|
| **Scope Document Store** | Immutable storage for signed scope definitions; the single source of truth for engagement authorization | Highest -- cannot be modified by agents; write access restricted to red-lead at engagement creation | Engagement cannot start without a valid, signed scope document |
| **Scope Oracle** | Evaluates proposed actions against scope rules; operates in a separate trust domain from agents | High -- separate process; own trust domain; agents cannot modify or bypass | Default deny; engagement pauses if oracle becomes unavailable |
| **Tool Proxy** | Intercepts all tool invocations; the only path through which agents access tools | High -- agents access tools exclusively through proxy; raw tool binaries not on agent PATH | Tools inaccessible without proxy; no direct tool access; agents degrade to standalone mode |
| **Network Enforcer** | Firewall/proxy rules derived from scope document; infrastructure-level network access control | High -- infrastructure-level; operates below agent process boundary | No network access outside scope; fail-closed; unauthorized destinations unreachable |
| **Audit Logger** | Records all actions to tamper-evident log; captures every agent decision and tool invocation | High -- append-only; separate storage from agent access; agents cannot read, modify, or delete logs | Engagement pauses if audit system fails; no unlogged operations permitted |
| **Evidence Vault** | Stores all engagement artifacts with chain-of-custody metadata; preserves findings and tool outputs | High -- append-only for agents; read access by red-reporter only; survives agent system failure | Evidence preserved independently of agent lifecycle; vault persists across agent restarts |
| **Circuit Breaker** | Monitors for cascading failure patterns and scope boundary proximity; detects anomalous agent behavior | Medium -- advisory and escalation role; does not independently halt engagement | Alerts red-lead for human judgment; logs warnings; does not block agent operations unilaterally |

**Evidence basis:** F-002 Scope Enforcement Architecture table; S-002 Scope Enforcement Components table; S-001 Convergence 3 (scope as architectural property).

### 3. Per-Agent Authorization Model

Each of the 11 /red-team agents operates under distinct, non-overlapping authorization constraints. Authorization levels are defined per agent and enforced by the scope enforcement infrastructure. No agent self-declares its authorization -- the Scope Oracle and Tool Proxy enforce the authorization level assigned to each agent identity.

| Agent | Authorization Level | Tool Access | Network Scope | Data Access |
|-------|---------------------|-------------|---------------|-------------|
| **red-lead** | Full engagement scope; sole authority to define and modify scope | All coordination tools; scope document management | All authorized targets (for verification purposes) | Full audit trail; scope documents; engagement metadata |
| **red-recon** | Reconnaissance scope only; passive and active reconnaissance within target allowlist | Passive/active recon tools only (nmap, Shodan, DNS tools, Amass, theHarvester) | Authorized target IPs/domains only; no exploitation ports | Target enumeration data; no exploit output; no credential material |
| **red-vuln** | Analysis scope; read-only interaction with targets; no exploitation | Vulnerability scanners (Nuclei, Nessus), CVE databases | Authorized targets (scan only, no exploitation traffic) | Scan results; CVE data; no credentials; no host-level data |
| **red-exploit** | Exploitation scope; constrained to target allowlist AND technique allowlist intersection | Exploitation frameworks (Metasploit, custom) within technique allowlist only | Authorized targets only; port-level restrictions per scope document | Exploitation artifacts; PoC outputs; no post-exploitation data |
| **red-privesc** | Post-exploitation scope; limited to already-compromised hosts only | Privilege escalation tools on compromised hosts (LinPEAS, WinPEAS, BloodHound) | Compromised host only; no lateral network access until explicitly authorized | Local host data; credential material on compromised host |
| **red-lateral** | Lateral movement scope; authorized internal network range only | Pivoting tools (Impacket, CrackMapExec, Chisel); C2 channel usage via red-infra infrastructure | Authorized network range as defined in scope document; C2 infrastructure | Internal network data within authorized scope |
| **red-persist** | Persistence scope; only permitted if explicitly authorized in Rules of Engagement | Persistence mechanism tools (custom persistence tools, autoruns analysis) | Compromised hosts within scope where persistence is authorized | Host-level configuration on authorized persistence targets |
| **red-exfil** | Exfiltration scope; data types explicitly specified in Rules of Engagement | Data identification and transfer tools; covert channel tools | Evidence repository only; no external exfiltration permitted | Classified data within engagement scope; exfiltration to evidence vault only |
| **red-infra** | Infrastructure scope; engagement infrastructure only; no target network access | C2 frameworks (Cobalt Strike, Sliver, Mythic), payload builders, redirector configuration | Engagement infrastructure network; no direct target access | C2 infrastructure configuration; payload artifacts; redirector logs |
| **red-social** | Social engineering scope; only permitted if explicitly authorized in Rules of Engagement | Phishing tools (GoPhish), pretexting frameworks, social engineering toolkits | Email/communication channels as authorized in scope document | Contact lists and social data within authorized scope |
| **red-reporter** | Report scope; read-only access to all engagement data; no active testing capability | Report generation tools; evidence compilation tools | Evidence repository (read access); report delivery channel (write access) | Full engagement data (read-only); audit trail; scope documents |

**Evidence basis:** F-002 Per-Agent Authorization Model table; S-002 Per-Agent Authorization Levels table; A-004 final roster definitions.

### 4. Layered Agent Isolation Architecture (AD-011)

Agent isolation implements defense-in-depth at the execution environment level. Four isolation layers prevent data leakage between engagements, unauthorized context sharing between agent groups, tool output contamination of agent state, and evidence tampering.

| Isolation Layer | Pattern | Boundary | Rationale |
|-----------------|---------|----------|-----------|
| **Engagement Boundary** | VM-per-engagement or namespace-per-engagement | Complete inter-engagement isolation; no data, credentials, or state shared between engagements | Prevents engagement data leakage; ensures engagement A's credentials, findings, and scope documents cannot be accessed by engagement B's agents |
| **Agent Group Boundary** | Container-per-agent-group | Phase-based isolation; agents in the same kill-chain phase share context but are isolated from other phases | Enables coordination within a phase (e.g., red-recon shares enumeration data within recon phase) while preventing premature access to other phases (e.g., exploitation agent cannot access persistence-phase data before authorization) |
| **Tool Execution Boundary** | Sandbox-per-tool-execution | Fresh sandbox per tool invocation; sandbox destroyed after execution completes | Prevents tool output from contaminating agent state; ensures each tool invocation starts from a clean environment; eliminates persistent side effects from tool execution |
| **Evidence Storage Boundary** | Dedicated append-only volume | Tamper-evident evidence collection; agents can write (append) but cannot modify or delete existing evidence | Maintains chain-of-custody integrity; evidence preserved independently of agent lifecycle; red-reporter has read-only access for report generation |

**Reference implementations:** PentAGI uses container-per-engagement with Docker isolation for all security testing operations (GitHub/vxcontrol, 2025). XBOW uses agent-per-vector isolation with defined application scope boundaries (XBOW, 2025). NVIDIA guidance recommends sandbox-per-execution with credential broker pattern (NVIDIA Developer Blog, 2025).

**Evidence basis:** F-002 Isolation Architecture Comparison and Recommended Isolation Architecture tables; S-002 AD-011 specification; C-003 subprocess sandboxing and credential broker patterns.

### 5. Progressive Autonomy Deployment Model (AD-012)

New /red-team deployments follow a graduated autonomy progression based on the AWS Agentic AI Security Scoping Matrix (AWS Security Blog, 2025). Organizations start at the most constrained level and advance as operational confidence builds. Each level requires corresponding escalation in authorization controls, isolation, and audit granularity.

| Level | Name | Human Oversight Model | Authorization Controls | Audit Granularity | Advancement Criteria |
|-------|------|-----------------------|------------------------|--------------------|----------------------|
| **Level 1** | Prescribed Agency | Human approves every agent action before execution | Full scope enforcement + per-action approval queue; agent proposes, human approves, scope oracle validates, tool proxy executes | Every action logged with human approval timestamp | Successful completion of 3+ engagements with zero scope deviations |
| **Level 2** | Monitored Agency | Near-real-time log review; human monitors agent actions as they occur | Full scope enforcement; agent executes within scope without per-action approval; human reviews logs within defined latency (e.g., 5 minutes) | Every action logged; dashboard with real-time action feed | Successful completion of 5+ engagements with zero scope deviations at Level 2 |
| **Level 3** | Supervised Agency | Phase boundary review; human reviews at kill-chain phase transitions | Full scope enforcement; agent operates autonomously within a phase; human approves phase transitions; circuit breaker check at every transition | Phase-level summary with drill-down to action-level detail | Successful completion of 10+ engagements with zero scope deviations at Level 3 |
| **Level 4** | Full Agency | Engagement summary review; human reviews completed engagement report | Full scope enforcement; agent operates autonomously across all phases within scope; human reviews final engagement report and compliance attestation | Engagement-level summary; full audit trail available on demand | Continuous operation with organizational risk acceptance |

**Key constraint:** Scope enforcement infrastructure (Layer 2) operates at full strength at ALL autonomy levels. Progressive autonomy reduces human oversight frequency, not scope enforcement rigor. Even at Level 4, the Scope Oracle, Tool Proxy, Network Enforcer, and Credential Broker validate every action. The difference is in when and how a human reviews the audit trail, not in whether the architecture enforces scope.

**Evidence basis:** F-002 Finding 3 (AWS Agentic AI Security Scoping Matrix); S-002 AD-012 specification; F-002 R-AUTH-009 recommendation.

### 6. OWASP Agentic AI Top 10 Coverage

The authorization architecture addresses all 10 risks from the OWASP Top 10 for Agentic Applications (December 2025). Each risk maps to specific mitigation mechanisms within the three-layer architecture and its enforcement components.

| Risk ID | Risk Name | Mitigation Approach | Implementing Components |
|---------|-----------|---------------------|-------------------------|
| **ASI01** | Agent Goal Hijack | Immutable scope definitions loaded from signed engagement file; goal validation against scope at every decision point; agent goals cannot override scope constraints regardless of prompt content | Scope Document Store (immutable signed scope), Scope Oracle (validates actions against scope rules) |
| **ASI02** | Tool Misuse | Default-deny tool access policy; all tool invocations intercepted by scope-validating proxy; target and technique parameters validated before execution; tools structurally inaccessible without proxy | Tool Proxy (intercepts all invocations), Scope Oracle (validates technique authorization) |
| **ASI03** | Identity and Privilege Abuse | Ephemeral, engagement-scoped credentials via Credential Broker; per-agent authorization levels enforced by infrastructure; network-level scope enforcement independent of agent identity claims | Credential Broker (ephemeral scope-bounded tokens), Network Enforcer (infrastructure-level reachability control) |
| **ASI04** | Supply Chain Vulnerabilities | Signed agent definitions prevent tampering; verified tool binaries with integrity checks; SLSA provenance for agent runtime components; agent dependencies audited before deployment | SLSA Build L2+ (supply chain integrity), signed agent definitions (eng-infra ownership) |
| **ASI05** | Unexpected Code Execution | Sandboxed execution environments per tool invocation; fresh sandbox per execution prevents persistent side effects; code review gate for C3+ engagement tool configurations | Sandbox-per-tool-execution isolation (AD-011 tool execution boundary) |
| **ASI06** | Memory and Context Poisoning | Validated intelligence sources only; context integrity verification; engagement parameters (scope document) are immutable and loaded from signed store, not from agent-accessible memory | Scope Document Store (immutable parameters), validated sources for agent context |
| **ASI07** | Insecure Inter-Agent Communication | Authenticated inter-agent messaging; signed task delegation with chain-of-authority verification; agents cannot impersonate other agents or forge handoff messages | Handoff protocol with authentication, chain-of-authority verification at phase transitions |
| **ASI08** | Cascading Failures | Circuit breakers at every kill-chain phase transition; mandatory scope revalidation before phase advancement; blast radius limits prevent a single agent failure from propagating through the agent chain | Circuit Breaker (cascading failure detection), phase transition scope revalidation |
| **ASI09** | Human-Agent Trust Exploitation | Mandatory evidence verification on all findings; confidence scoring prevents false-positive inflation; /adversary review of engagement reports validates accuracy before human consumption | Audit Logger (complete action record), Evidence Vault (chain-of-custody), /adversary quality review |
| **ASI10** | Rogue Agents | Comprehensive audit logging of every action; behavioral monitoring against expected patterns; scope verification at every tool invocation; no agent operates outside scope enforcement | All seven enforcement components collectively; Scope Oracle validates every action; Audit Logger captures every decision |

**Evidence basis:** F-002 OWASP Top 10 for Agentic Applications risk analysis table; S-002 OWASP Agentic AI Top 10 Coverage table; OWASP GenAI Security Project (December 2025).

### 7. Audit Trail Requirements

The audit subsystem implements the evidence preservation requirement of R-020. It operates independently of agent code and serves as the authoritative source for engagement documentation, compliance attestation, and post-engagement analysis.

| Requirement | Implementation | Evidence Basis |
|-------------|---------------|----------------|
| **Tamper Evidence** | Hash-chained or signed log entries; each entry references the hash of the previous entry; append-only storage prevents modification or deletion by agents | F-002 Finding 7; F-002 R-AUTH-005; production patterns from XBOW (timestamped audit trail) and PentAGI (comprehensive logging within Docker isolation) |
| **Completeness** | Every agent action logged with: timestamp, agent identity, tool invocation details (tool name, parameters), target parameters, Scope Oracle decision (allow/deny with reason), and action result (success/failure with output summary) | S-002 Audit Trail Requirements table; F-002 Pattern 3 (Post-Execution Audit Verification) |
| **Chain of Custody** | All findings traced from discovery (agent action) through the tool invocation that produced the finding to the scope authorization that permitted the action; unbroken chain from evidence to authorization | F-002 R-AUTH-005; S-002 Audit Trail Requirements (chain of custody row); OWASP Agentic AI recommendations on evidence preservation |
| **Access Control** | Audit Logger: write-only for agents (append); read access restricted to red-reporter for report generation and red-lead for compliance review; no agent can read, modify, or delete its own audit entries | S-002 Audit Trail Requirements (read access row); separation of audit access from agent access |
| **Retention** | Engagement data retained per organizational policy; evidence vault persists independently of agent system lifecycle; vault survives agent failure, restart, or decommissioning | S-002 Audit Trail Requirements (retention row); F-002 Evidence Vault failure mode (evidence preserved even if agent systems fail) |
| **Compliance Output** | Automated scope compliance report generated from audit trail at engagement conclusion; includes finding-to-authorization trace, scope boundary proximity report, and engagement timeline with action-scope mapping; requires red-lead sign-off before delivery | F-002 Pattern 3 (compliance report); S-002 Layer 3 specification |

### 8. Four-Layer Guardrail Architecture

Four guardrail layers provide defense-in-depth behavioral constraints that complement the scope enforcement components. Each layer operates at a different level of abstraction and catches different categories of unauthorized behavior.

| Layer | Guardrail Type | Enforcement Mechanism | /red-team Application | Action on Violation |
|-------|---------------|----------------------|----------------------|---------------------|
| **L1: Constitutional** | Hard constraints from Jerry framework that cannot be violated under any circumstances | Pre-loaded immutable rules checked before every action; not derived from engagement scope but from framework governance (H-01 through H-33) | R-020 scope verification; no out-of-scope actions permitted regardless of agent reasoning or prompt content | BLOCK -- hard deny; action rejected; violation logged |
| **L2: Policy** | Engagement-specific rules derived from the signed scope document | Loaded from Scope Document Store at engagement start; compiled into Scope Oracle evaluation rules; checked at every decision point | Authorized targets, techniques, time windows, exclusions, and rules of engagement as defined by red-lead | BLOCK -- action rejected; violation logged; alert to red-lead |
| **L3: Behavioral** | Runtime behavioral bounds that detect anomalous patterns | Monitored during execution by Circuit Breaker; pattern matching against expected agent behavior profiles | Circuit breakers triggered if agent behavior deviates from expected patterns (e.g., scanning non-target IPs, accessing tools outside agent authorization level) | ESCALATE -- alert to red-lead for human judgment; log anomaly; do not independently halt |
| **L4: Output** | Output validation and sanitization applied to all agent deliverables | Applied to all agent outputs before delivery; schema validation, confidence scoring, evidence chain verification | Evidence integrity checks on findings; report accuracy verification; confidence scoring on all vulnerability claims | HOLD -- output quarantined until verification completes; low-confidence findings flagged for review |

**Guardrail Enforcement Decision Table:**

| Scenario | L1 Action | L2 Action | L3 Action | L4 Action |
|----------|-----------|-----------|-----------|-----------|
| Agent targets out-of-scope system | BLOCK (hard deny) | -- | -- | -- |
| Agent uses unauthorized technique | BLOCK (hard deny) | -- | -- | -- |
| Agent operates outside time window | BLOCK (credential expired) | -- | -- | -- |
| Agent approaches scope boundary | ALLOW | WARN (log proximity) | ALERT (notify red-lead) | -- |
| Agent finds vulnerability in-scope | ALLOW | ALLOW | MONITOR | VERIFY (evidence chain) |
| Agent attempts unknown tool | BLOCK (default deny) | -- | -- | -- |
| Agent produces report with low confidence | ALLOW | ALLOW | ALLOW | HOLD (require verification) |
| Agent exhibits anomalous behavior pattern | ALLOW | ALLOW | ESCALATE (to red-lead) | -- |

**Evidence basis:** F-002 Guardrail Layer Architecture table; F-002 Guardrail Enforcement Decision Table; Enkrypt AI layered guardrail framework (Enkrypt AI, 2025); Forrester AEGIS six-domain framework (BigID, 2025).

### 9. Scope Document Specification

The scope document is the foundational trust artifact. It defines the complete authorization boundary for an engagement and is the input from which all runtime enforcement components derive their rules.

**Format:** Signed YAML with the following required fields:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `engagement_id` | string | Yes | Unique identifier for this engagement; used as namespace for all engagement artifacts |
| `version` | string | Yes | Scope document version; incremented on any modification (requires re-signing) |
| `authorized_targets` | list[object] | Yes | Explicit IP ranges, domains, and applications authorized for testing; each entry specifies target type (IP, CIDR, domain, application), value, and permitted interaction level (scan, exploit, persist) |
| `technique_allowlist` | list[string] | Yes | MITRE ATT&CK technique IDs authorized for this engagement (e.g., T1046, T1059.001); techniques not on this list are structurally unavailable |
| `time_window` | object | Yes | `start` and `end` timestamps (ISO 8601); engagement operations are only permitted within this window; credentials automatically expire at `end` |
| `exclusion_list` | list[object] | Yes (may be empty) | Systems, networks, IP ranges, and data types that must not be touched; exclusion rules are checked before allow rules and always supersede |
| `rules_of_engagement` | object | Yes | Engagement-specific behavioral constraints: permitted impact level (e.g., no denial-of-service, no data destruction), social engineering authorization (boolean), persistence authorization (boolean), exfiltration data types, notification requirements |
| `agent_authorizations` | map[string, object] | Yes | Per-agent authorization overrides; maps agent name to specific tool access, network scope, and data access constraints for this engagement |
| `signature` | object | Yes | Signing metadata: signer identity, signing timestamp, signature value, signing mechanism (per OQ-004 resolution) |
| `evidence_handling` | object | Yes | Evidence classification level, retention requirements, delivery mechanism, and access control policy for this engagement's artifacts |

**Immutability Constraint:** Once signed and loaded at engagement start, the scope document cannot be modified. Any scope change requires:
1. Red-lead creates a new scope document version
2. New document is signed (mechanism per OQ-004)
3. Engagement is paused
4. New document is loaded into the Scope Document Store
5. All enforcement components reload rules from the updated document
6. Engagement resumes with the updated scope

**Evidence basis:** F-002 Pattern 1 (Pre-Engagement Scope Definition); S-002 Layer 1 specification; F-003 R-RULES-005 (OPA/Rego patterns for scope enforcement).

### 10. Default-Deny Tool Access Policy

All /red-team agents operate under a default-deny tool access policy. No agent has implicit access to any tool. Tool access is explicitly granted per engagement through the scope document's `agent_authorizations` field and `technique_allowlist`.

**Policy rules:**

| Rule | Description | Enforcement Component |
|------|-------------|----------------------|
| **No implicit tool access** | No tool is available to any agent unless explicitly granted in the scope document for this engagement | Scope Oracle evaluates tool access requests against engagement-specific authorization |
| **Proxy-only access** | All tool invocations pass through the Tool Proxy; agents cannot invoke tools directly; raw tool binaries are not on any agent's PATH | Tool Proxy is the sole tool access gateway; no bypass path exists |
| **Technique-bound access** | Tools are accessible only for authorized techniques; a tool that supports multiple ATT&CK techniques is only permitted for the techniques on the allowlist | Scope Oracle validates that the requested tool usage maps to an authorized technique |
| **Fail-closed on proxy unavailability** | If the Tool Proxy becomes unavailable, all tool access ceases; agents degrade to standalone mode (AD-010 Level 2) rather than gaining unmediated tool access | Tool Proxy failure mode: tools inaccessible; agents continue with methodology guidance only |
| **Exclusion supersedes inclusion** | If a target appears on both the authorized targets list and the exclusion list, the exclusion takes precedence; deny rules always override allow rules | Scope Oracle checks exclusions before evaluating allowlists |

**Evidence basis:** F-002 R-AUTH-002 (Default-Deny Tool Access Policy); S-002 AD-004 specification ("out-of-scope actions structurally impossible"); F-002 Finding 2 (authorization scope bounds risk more effectively than human oversight).

---

## Options Considered

### Option 1: Human-in-the-Loop Approval for Every Action

**Description:** Human operator must approve every agent action before execution. No autonomous operation permitted.

| Dimension | Assessment |
|-----------|-----------|
| **Security** | Highest theoretical security -- every action is human-approved |
| **Practicality** | Impractical for real engagements; human becomes bottleneck; defeats the value proposition of agent-assisted operations |
| **Scalability** | Does not scale; approval latency grows linearly with action count |
| **Risk** | Human fatigue leads to rubber-stamping; security degrades with volume (NIST AI Agent RFI analysis, 2025) |
| **Evidence** | NIST AI Agent RFI (2025-0035) analysis concluded that human oversight alone is insufficient for bounding agent risk because human vigilance degrades with volume and repetition (F-002 Finding 2) |

**Verdict:** REJECTED. Human approval for every action creates an illusion of control that degrades with scale. It does not provide the architectural safety guarantee that scope enforcement provides.

### Option 2: Policy-Only (Pre-Engagement Rules, No Runtime Enforcement)

**Description:** Red-lead defines engagement scope as policy rules. Agents are instructed to follow the policy. No runtime enforcement infrastructure validates compliance.

| Dimension | Assessment |
|-----------|-----------|
| **Security** | Weak -- relies on agent behavioral compliance with prompt instructions; no structural enforcement |
| **Practicality** | Simple to implement; no enforcement infrastructure required |
| **Scalability** | Scales well; no runtime overhead |
| **Risk** | Single point of failure at the prompt level; ASI01 (goal hijack) directly bypasses this model; prompt injection can override policy instructions |
| **Evidence** | OWASP ASI01 (Agent Goal Hijack) specifically targets this failure mode: adversary manipulates agent goals through hidden prompts or injected instructions, and policy-as-prompt provides no structural defense (F-002 Finding 1) |

**Verdict:** REJECTED. Policy-as-prompt is the weakest authorization model because it relies on the same mechanism (LLM prompt processing) that is the attack surface for goal hijack. Scope must be enforced by infrastructure, not by instructions.

### Option 3: Three-Layer Architecture (Structural + Dynamic + Retrospective) -- SELECTED

**Description:** Pre-engagement scope definition (signed, immutable) combined with runtime enforcement (scope oracle, tool proxy, network enforcer, credential broker) and post-execution audit verification (tamper-evident logs, compliance report).

| Dimension | Assessment |
|-----------|-----------|
| **Security** | Highest structural security -- three independent layers; failure of any single layer does not compromise the others; out-of-scope actions structurally impossible |
| **Practicality** | Requires enforcement infrastructure development; justified by the security-critical nature of offensive agent operations |
| **Scalability** | Scales with engagement complexity; enforcement components are stateless decision points (scope oracle) or infrastructure (network enforcer) |
| **Risk** | Infrastructure complexity introduces operational overhead; mitigated by progressive autonomy deployment (AD-012) |
| **Evidence** | Three independent research streams converged on this architecture (S-001 Convergence 3); validated by XBOW and PentAGI production deployments (F-002 Finding 4); OWASP Agentic AI Top 10 risk mapping validates coverage of all 10 risks (F-002 Finding 1) |

**Verdict:** SELECTED. This is the only option that makes out-of-scope actions structurally impossible rather than procedurally prevented. The infrastructure investment is justified by the security-critical nature of /red-team operations.

### Option 4: Full Autonomy with Post-Hoc Review Only

**Description:** Agents operate with broad guidelines. Human reviews engagement results after completion. No runtime scope enforcement.

| Dimension | Assessment |
|-----------|-----------|
| **Security** | Lowest security -- damage occurs before review; no prevention, only detection |
| **Practicality** | Simplest to implement; maximum agent throughput |
| **Scalability** | Maximum scalability; no runtime overhead |
| **Risk** | Unbounded blast radius; a single out-of-scope action during engagement cannot be prevented; post-hoc review discovers damage after it has occurred |
| **Evidence** | This option violates the core finding that security must be an architectural property, not an operational procedure (S-001 Convergence 3); it fails to address ASI01, ASI02, ASI03, and ASI10 from the OWASP Agentic AI Top 10 (F-002 Finding 1) |

**Verdict:** REJECTED. Post-hoc review detects but does not prevent out-of-scope actions. For offensive security operations against live targets, prevention is the only acceptable control model.

---

## Consequences

### Positive

| Consequence | Impact | Evidence |
|-------------|--------|----------|
| Out-of-scope actions are structurally impossible, not procedurally prevented | Engagement risk is bounded by architecture regardless of agent behavior or prompt injection attempts | S-001 Convergence 3: three independent streams converge on scope-over-oversight |
| All 10 OWASP Agentic AI Top 10 risks are addressed with specific mitigation components | Architecture meets the current industry-standard risk taxonomy for autonomous agent security | F-002 Finding 1; S-002 OWASP Coverage table |
| Per-agent authorization model enforces least-privilege access across all 11 /red-team agents | Each agent can only access tools, networks, and data required for its specific role; blast radius of any single agent compromise is limited to that agent's authorization level | F-002 Per-Agent Authorization Model; S-002 Per-Agent Authorization Levels |
| Tamper-evident audit trail provides complete engagement accountability | Every action is logged with chain-of-custody from finding to authorization; enables compliance attestation and post-engagement analysis | F-002 Finding 7; F-002 R-AUTH-005 |
| Progressive autonomy deployment reduces organizational adoption risk | New deployments start at maximum human oversight and relax as confidence builds; organizations choose their comfort level | F-002 Finding 3 (AWS Scoping Matrix); S-002 AD-012 |
| Architecture validated by production agentic security platforms | XBOW and PentAGI demonstrate that isolated, scope-bounded autonomous offensive agents are production-viable | F-002 Finding 4 |

### Negative

| Consequence | Impact | Mitigation |
|-------------|--------|------------|
| Enforcement infrastructure development cost | Scope Oracle, Tool Proxy, Network Enforcer, Credential Broker, Audit Logger, Evidence Vault, and Circuit Breaker require implementation effort | Phased implementation: core components (Scope Oracle, Tool Proxy) in Phase 3; infrastructure components (Network Enforcer, Credential Broker) in Phase 4; validation in Phase 5 |
| Runtime latency from scope validation on every tool invocation | Every agent action incurs scope oracle evaluation overhead | Scope oracle is a stateless decision point evaluating against a loaded rule set; evaluation is sub-millisecond for typical rule set sizes; latency is negligible compared to tool execution time |
| Operational complexity for engagement setup | Scope document creation requires explicit specification of all authorization parameters before engagement begins | Red-lead agent assists with scope document creation; scope document templates for common engagement types reduce manual specification; engagement start validates document completeness |
| Isolation overhead from containerized execution | VM-per-engagement and container-per-agent-group introduce resource overhead compared to shared-process execution | Resource overhead is a cost of safety; containers are the industry-standard isolation mechanism (PentAGI, XBOW); modern container runtimes have minimal overhead for methodology-guidance workloads |

### Neutral

| Consequence | Description |
|-------------|-------------|
| This ADR does not specify the scope document signing mechanism | Signing mechanism (HMAC vs. PKI) is deferred to OQ-004 resolution; the architecture requires signing but is agnostic to the specific mechanism |
| This ADR does not specify circuit breaker threshold values | Threshold configuration is deferred to OQ-006 resolution; the architecture requires circuit breakers but thresholds depend on operational experience |
| This ADR does not mandate a specific container runtime | The isolation architecture (AD-011) specifies isolation levels but not implementation technology (Docker, Podman, Kubernetes, etc.); implementation choice is a Phase 3 decision |

---

## Evidence Base

Every design decision in this ADR traces to specific research findings produced during Phase 1.

### Primary Research Sources

| Source | Content | Key Findings Used |
|--------|---------|-------------------|
| F-002: Security Architecture Patterns | OWASP Agentic AI Top 10 risk mapping; scope enforcement component design; per-agent authorization model; isolation patterns; production tool analysis (XBOW, PentAGI); guardrail architecture; credential management; audit trail design | Findings 1-7; Patterns 1-3; Isolation Architecture; Guardrail Enforcement Decision Table; Recommendations R-AUTH-001 through R-AUTH-010 |
| F-003: Configurable Rule Sets | OPA/Rego patterns for scope enforcement policy evaluation; policy-as-data architecture; declarative rule definition; dual-format authoring | Finding 2 (OPA/Rego policy engine); R-RULES-005 (OPA/Rego patterns for scope enforcement) |
| S-002: Architecture Implications | AD-004, AD-011, AD-012 decision specifications; Security Architecture Specification Input (Layer 1/2/3 definitions, scope enforcement components, per-agent authorization levels, audit trail requirements, OWASP coverage table); open questions OQ-001, OQ-004, OQ-006 | Full Security Architecture Specification Input section; Open Questions OQ-001, OQ-004, OQ-006 |
| S-001: Cross-Stream Findings | Convergence 3 (authorization scope over human oversight); cross-stream validation from F, C, and D streams; consolidated conclusion on scope as architectural property | Convergence 3 analysis; consolidated conclusion |

### Industry Framework Sources

| Framework | Source | Date | Contribution to This ADR |
|-----------|--------|------|--------------------------|
| OWASP Top 10 for Agentic Applications | OWASP GenAI Security Project | December 2025 | Canonical 10-risk taxonomy (ASI01-ASI10); risk-to-mitigation mapping validates enforcement component design |
| AWS Agentic AI Security Scoping Matrix | AWS Security Blog | 2025 | 4-level progressive autonomy framework; graduated security control mapping |
| NVIDIA Sandboxing Guidance | NVIDIA Developer Blog | 2025 | Credential broker pattern; sandbox-per-execution isolation; network and filesystem controls |
| Strata Identity Agent Security | Strata Identity | 2025 | JIT provisioning; ephemeral identities; dynamic context-aware access enforcement |
| NIST AI Agent RFI (2025-0035) | NIST | 2025 | Authorization scope vs. human oversight analysis; scope bounds risk more effectively than oversight |
| Forrester AEGIS | BigID / Forrester | 2025 | Six-domain agentic AI governance framework (Identity, Data, Access, Monitoring, Governance, Resilience) |
| Enkrypt AI Guardrails | Enkrypt AI | 2025 | Layered guardrail framework with risk taxonomy specific to agent systems |

### Production System Validation

| System | Source | Date | Validation Provided |
|--------|--------|------|---------------------|
| XBOW | xbow.com; BusinessWire | 2025 | Hundreds of autonomous agents within scope boundaries; audit trail; machine-speed testing validates multi-agent offensive operations at scale |
| PentAGI | GitHub/vxcontrol/pentagi | 2025 | Docker isolation for autonomous pentesting; 20+ security tools; validates container-per-engagement isolation pattern |
| Escape | escape.tech | 2025 | Schema-based scope enforcement for API security testing; validates domain-specific scope boundaries |

---

## Compliance

### Requirements Compliance

| Requirement | Compliance | Implementation |
|-------------|------------|----------------|
| R-001: Secure by Design | COMPLIANT | This ADR is written before any agent implementation; authorization architecture formalized before agents with offensive capabilities are built |
| R-020: Authorization Verification | COMPLIANT (primary ADR) | Three-layer architecture implements scope verification before every tool execution (Layer 2) with evidence preservation (Layer 3 audit trail) |
| R-018: Real Offensive Techniques | COMPLIANT | Technique allowlist maps to MITRE ATT&CK technique IDs; real techniques are authorized per engagement scope; unauthorized techniques are structurally unavailable |
| R-013: C4 /adversary on Every Phase | COMPLIANT | This ADR is classified C4 and requires full adversarial review with all 10 strategies before acceptance |

### Constitutional Compliance

| Constraint | Compliance | Implementation |
|------------|------------|----------------|
| P-003 (H-01): No Recursive Subagents | COMPLIANT | Scope enforcement operates as infrastructure, not as nested agents; Scope Oracle is a service, not an agent |
| P-020 (H-02): User Authority | COMPLIANT | User defines engagement scope through red-lead; architecture enforces but never overrides user intent; progressive autonomy deployment (AD-012) allows user to select oversight level |
| P-022 (H-03): No Deception | COMPLIANT | Audit trail provides complete transparency; all scope oracle decisions logged with reasons; no agent action is hidden from the audit record |

### OWASP Agentic AI Top 10 Compliance

All 10 risks from the OWASP Top 10 for Agentic Applications (December 2025) are addressed by specific components in this architecture. See section 6 (OWASP Agentic AI Top 10 Coverage) for the complete risk-to-mitigation mapping.

---

## Related Decisions

### Upstream (This ADR Depends On)

| Decision | Relationship | Status |
|----------|-------------|--------|
| AD-001: Methodology-First Design | Constrains scope of authorization: agents provide methodology guidance, not autonomous execution; scope enforcement applies to tool-augmented operation | HIGH confidence (S-002) |
| AD-002: 21-Agent Roster | Defines the 11 /red-team agents whose authorization levels are specified in section 3 | HIGH confidence (S-002) |
| AD-005: MCP-Primary Tool Integration | Defines the tool integration protocol through which the Tool Proxy intercepts invocations | HIGH confidence (S-002) |
| AD-010: Standalone Capable Design | Defines the degradation behavior when Tool Proxy is unavailable: agents degrade to standalone mode rather than gaining unmediated tool access | HIGH confidence (S-002) |

### Downstream (Decisions That Depend On This ADR)

| Decision/Work Item | Relationship |
|--------------------|-------------|
| All 11 /red-team agent definitions | Agent definitions must reference per-agent authorization levels from section 3 |
| FEAT-015 implementation tasks | Scope enforcement components must be implemented per section 2 specifications |
| Phase 3 agent development | No agent with tool access can be built until scope enforcement infrastructure is in place |
| Phase 5 purple team validation | Test plans must verify authorization architecture per F-002 R-AUTH-010 |
| AD-007: YAML-First Configurable Rule Sets | Scope document YAML format aligns with the YAML-first configuration pattern; scope enforcement policies use OPA/Rego architectural patterns per F-003 |

### Sibling (Related Architecture Decisions)

| Decision | Relationship |
|----------|-------------|
| AD-011: Agent Isolation Architecture | Isolation layers (section 4) are the execution environment complement to authorization controls (sections 1-3) |
| AD-012: Progressive Autonomy Deployment | Autonomy progression (section 5) governs the human oversight model that operates alongside scope enforcement |

---

## Open Questions

### OQ-001: Agent Isolation Granularity Trade-Off

**Context:** AD-011 recommends container-per-agent-group (phase-based isolation), but the specific grouping -- per individual agent vs. per kill-chain phase vs. per engagement stage -- involves performance and coordination trade-offs that cannot be evaluated without implementation experience.

**What Must Be Decided:** Which agents share a container, and what the inter-container communication overhead is. Container-per-agent provides maximum isolation but maximum overhead; container-per-phase provides practical isolation with manageable overhead.

**Research Input:** PentAGI uses container-per-engagement (single container, all tools). XBOW uses agent-per-vector (fine-grained). The right granularity depends on PROJ-010's specific coordination patterns (F-002 Isolation Architecture Comparison; S-002 OQ-001).

**Decision Timing:** Phase 2 architecture design, informed by Phase 3 prototype performance measurements.

### OQ-004: Scope Document Signing Mechanism

**Context:** The architecture requires scope documents to be signed (section 9), but does not prescribe the specific signing mechanism. Options range from simple HMAC to full PKI-based digital signatures.

**What Must Be Decided:** The specific signing mechanism, balancing usability (operators should not need PKI infrastructure for simple engagements) with security (scope integrity is the foundation of the entire authorization model).

**Recommended Approach:** Tiered signing aligned with engagement criticality. HMAC for C1/C2 engagements (shared secret between red-lead and scope enforcement infrastructure; simple to configure). Digital signature (PKI) for C3/C4 engagements (non-repudiation; formal accountability chain; appropriate for high-impact engagements).

**Research Input:** S-002 OQ-004 identifies this as a Phase 2 design decision. The signing mechanism does not affect the architecture's security properties -- both HMAC and PKI provide integrity verification. The difference is in the trust model (shared secret vs. asymmetric keys) and operational overhead.

**Decision Timing:** Phase 2 architecture design, before scope document specification is finalized.

### OQ-006: Circuit Breaker Threshold Configuration

**Context:** The architecture mandates circuit breakers at phase transitions (section 2, Circuit Breaker component), but does not define the specific thresholds for triggering escalation vs. halt.

**What Must Be Decided:** What constitutes a "cascading failure pattern" that triggers the circuit breaker; the specific thresholds for alerting (notify red-lead) vs. pausing (halt current phase) vs. halting (terminate engagement); whether circuit breaker sensitivity should be configurable per engagement profile.

**Recommended Approach:** Circuit breaker sensitivity should be configurable via the engagement scope document or engagement profile (aligned with AD-007 configurable rule set architecture). Default thresholds should be conservative (escalate early, pause on repeated anomalies, halt on confirmed scope deviation). Operational experience from Phase 5 purple team exercises should refine threshold values.

**Research Input:** F-002 R-AUTH-006 mandates circuit breakers but defers threshold definition; S-002 OQ-006 identifies this as a Phase 2 design decision.

**Decision Timing:** Phase 2 architecture design, with threshold values refined during Phase 5 purple team validation.

---

## References

### Industry Leader Sources

| Source | Date | Content |
|--------|------|---------|
| [OWASP Top 10 for Agentic Applications](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/) | December 2025 | ASI01-ASI10 canonical risk taxonomy for autonomous AI agents |
| [OWASP GenAI Security Project -- Agentic Applications Announcement](https://genai.owasp.org/2025/12/09/owasp-top-10-for-agentic-applications-the-benchmark-for-agentic-security-in-the-age-of-autonomous-ai/) | December 2025 | Benchmark for agentic security; 100+ researcher collaboration |
| [OWASP -- Agentic AI Threats and Mitigations](https://genai.owasp.org/resource/agentic-ai-threats-and-mitigations/) | 2025 | Threat-model-based reference for emerging agentic threats |
| [AWS -- Agentic AI Security Scoping Matrix](https://aws.amazon.com/blogs/security/the-agentic-ai-security-scoping-matrix-a-framework-for-securing-autonomous-ai-systems/) | 2025 | 4-level autonomy classification with mapped security controls |
| [NVIDIA -- Practical Security Guidance for Sandboxing Agentic Workflows](https://developer.nvidia.com/blog/practical-security-guidance-for-sandboxing-agentic-workflows-and-managing-execution-risk) | 2025 | Credential scoping, network controls, filesystem restrictions for agent sandboxing |
| [NIST AI Agent RFI (2025-0035) Analysis](https://www.rockcybermusings.com/p/nist-ai-agent-rfi-2025-0035-human-oversight-wrong-fix) | 2025 | Authorization scope vs. human oversight; scope bounds risk more effectively |

### Industry Expert Sources

| Source | Date | Content |
|--------|------|---------|
| [Strata Identity -- 8 Strategies for AI Agent Security](https://www.strata.io/blog/agentic-identity/8-strategies-for-ai-agent-security-in-2025/) | 2025 | JIT provisioning, ephemeral identities, dynamic access for agents |
| [Enkrypt AI -- Securing AI Agents with Layered Guardrails](https://www.enkryptai.com/blog/securing-ai-agents-a-comprehensive-framework-for-agent-guardrails) | 2025 | Comprehensive agent guardrail framework with risk taxonomy |
| [BigID -- AEGIS Explained: Guardrails for Autonomous AI Systems](https://bigid.com/blog/what-is-aegis/) | 2025 | Forrester AEGIS six-domain framework analysis |

### Production System Sources

| Source | Date | Content |
|--------|------|---------|
| [XBOW -- Autonomous Offensive Security Platform](https://xbow.com) | 2025 | Hundreds of autonomous agents within defined scope boundaries |
| [PentAGI (GitHub: vxcontrol/pentagi)](https://github.com/vxcontrol/pentagi) | 2025 | Open-source autonomous AI pentesting with Docker isolation; 20+ tools |
| [Escape -- Agentic Pentesting Tools Comparison](https://escape.tech/blog/best-agentic-pentesting-tools/) | 2025 | Schema-based scope enforcement for domain-specific testing |

### PROJ-010 Research Artifacts

| Artifact | Content |
|----------|---------|
| F-002: Security Architecture Patterns | Primary research source: three-layer auth, OWASP Agentic AI Top 10, scope enforcement, per-agent auth model, isolation patterns, guardrail architecture |
| F-003: Configurable Rule Sets | OPA/Rego patterns for scope enforcement policy evaluation |
| S-001: Cross-Stream Findings | Convergence 3 (authorization scope over human oversight); cross-stream validation |
| S-002: Architecture Implications | AD-004, AD-011, AD-012 decision specifications; Security Architecture Specification Input; open questions |
