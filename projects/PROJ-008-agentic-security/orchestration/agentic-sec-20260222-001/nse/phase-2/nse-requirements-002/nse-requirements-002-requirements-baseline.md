# Agentic Security Requirements Baseline

> Agent: nse-requirements-002
> Phase: 2 (Requirements Baseline)
> Pipeline: NSE (NASA-SE)
> Status: BASELINED
> Date: 2026-02-22
> Baseline ID: BL-SEC-001
> Version: 1.0.0
> Authority: nse-requirements-002 (Requirements Engineer -- Baseline Freeze)
> Quality Gate: C4 (>= 0.95)

## Document Sections

| Section | Purpose |
|---------|---------|
| [Baseline Metadata](#baseline-metadata) | Version, authority, change control, source artifacts |
| [Baseline Methodology](#baseline-methodology) | Freeze criteria, baselined content scope, exclusions |
| [Category 1: Agent Identity and Authentication](#category-1-agent-identity-and-authentication) | FR-SEC-001 through FR-SEC-004 |
| [Category 2: Authorization and Access Control](#category-2-authorization-and-access-control) | FR-SEC-005 through FR-SEC-010 |
| [Category 3: Input Validation](#category-3-input-validation) | FR-SEC-011 through FR-SEC-016 |
| [Category 4: Output Security](#category-4-output-security) | FR-SEC-017 through FR-SEC-020 |
| [Category 5: Inter-Agent Communication](#category-5-inter-agent-communication) | FR-SEC-021 through FR-SEC-024 |
| [Category 6: Supply Chain Security](#category-6-supply-chain-security) | FR-SEC-025 through FR-SEC-028 |
| [Category 7: Audit and Logging](#category-7-audit-and-logging) | FR-SEC-029 through FR-SEC-032 |
| [Category 8: Incident Response](#category-8-incident-response) | FR-SEC-033 through FR-SEC-036 |
| [Category 9: Additional Functional Requirements](#category-9-additional-functional-requirements) | FR-SEC-037 through FR-SEC-042 |
| [Category 10: Performance](#category-10-performance) | NFR-SEC-001 through NFR-SEC-003 |
| [Category 11: Availability](#category-11-availability) | NFR-SEC-004 through NFR-SEC-006 |
| [Category 12: Scalability](#category-12-scalability) | NFR-SEC-007 through NFR-SEC-008 |
| [Category 13: Usability](#category-13-usability) | NFR-SEC-009 through NFR-SEC-010 |
| [Category 14: Maintainability](#category-14-maintainability) | NFR-SEC-011 through NFR-SEC-015 |
| [Bi-Directional Traceability Matrix](#bi-directional-traceability-matrix) | Forward and reverse traceability |
| [MITRE Coverage Matrix](#mitre-coverage-matrix) | ATT&CK and ATLAS mapping |
| [OWASP Coverage Matrix](#owasp-coverage-matrix) | Agentic Top 10, LLM Top 10, API Top 10, Web Top 10 |
| [NIST Coverage Matrix](#nist-coverage-matrix) | AI RMF, CSF 2.0, SP 800-53 |
| [Baseline Summary Statistics](#baseline-summary-statistics) | Counts, coverage, priority distribution |
| [Change Control Process](#change-control-process) | CR process, impact assessment, approval authority |

---

## Baseline Metadata

| Field | Value |
|-------|-------|
| Baseline ID | BL-SEC-001 |
| Version | 1.0.0 |
| Baseline Date | 2026-02-22 |
| Authority | nse-requirements-002 |
| Classification | C4 (Mission-Critical) |
| Quality Threshold | >= 0.95 (weighted composite, S-014) |
| Total Requirements | 57 (42 functional + 15 non-functional) |
| Priority Distribution | 17 CRITICAL, 26 HIGH, 14 MEDIUM, 0 LOW |
| Work Items | ST-026 (Functional), ST-027 (Non-Functional), ST-028 (Compliance Matrix) |

### Source Artifacts

| Artifact | Agent | Path |
|----------|-------|------|
| Security Requirements Discovery | nse-requirements-001 | `orchestration/agentic-sec-20260222-001/nse/phase-1/nse-requirements-001/nse-requirements-001-security-requirements.md` |
| Agentic Security Risk Register (FMEA) | nse-explorer-001 | `orchestration/agentic-sec-20260222-001/nse/phase-1/nse-explorer-001/nse-explorer-001-risk-register.md` |
| Security Gap Analysis | ps-analyst-001 | `orchestration/agentic-sec-20260222-001/ps/phase-1/ps-analyst-001/ps-analyst-001-gap-analysis.md` |
| Threat Framework Analysis | ps-researcher-002 | `orchestration/agentic-sec-20260222-001/ps/phase-1/ps-researcher-002/ps-researcher-002-threat-framework-analysis.md` |
| PS-to-NSE Cross-Pollination Handoff | barrier-1 | `orchestration/agentic-sec-20260222-001/cross-pollination/barrier-1/ps-to-nse/handoff.md` |

### Baseline Rules

1. **Freeze Scope:** All 57 requirements (FR-SEC-001 through FR-SEC-042, NFR-SEC-001 through NFR-SEC-015) are frozen at the versions documented in this file.
2. **No Invention:** This baseline does NOT introduce new requirements. It formalizes, enriches, and traces what Phase 1 discovered.
3. **Change Authority:** Post-baseline modifications require a formal Change Request (CR) per the [Change Control Process](#change-control-process).
4. **Testability Mandate:** Every baselined requirement includes testable acceptance criteria.
5. **Traceability Mandate:** Every requirement traces to at least one source framework and at least one FMEA risk.

---

## Baseline Methodology

### Enrichment Process

Each Phase 1 requirement was enriched with the following baseline fields not present in the discovery artifact:

| Baseline Field | Source | Purpose |
|----------------|--------|---------|
| Rationale | Gap analysis (ps-analyst-001), risk register (nse-explorer-001) | Documents WHY this requirement exists |
| Current Jerry Coverage | Gap analysis gap matrix | Documents what Jerry already provides |
| Gap Status | Gap analysis requirements-to-gap mapping | NO COVERAGE / PARTIAL / FULL |
| Parent Risk IDs | Risk register FMEA | Links to specific failure modes driving this requirement |
| Phase 2 Architecture Decision | Gap analysis recommended priorities | Links to architecture decision(s) that implement this requirement |

### Baselined Requirement Format

Each requirement uses a consistent table format with 12 fields:

| Field | Description |
|-------|-------------|
| ID | Unique identifier (FR-SEC-NNN or NFR-SEC-NNN) |
| Title | Short descriptive name |
| Priority | CRITICAL / HIGH / MEDIUM / LOW |
| Description | Formal "SHALL" statement defining the requirement |
| Rationale | Why this requirement exists -- threat context, risk justification |
| Current Jerry Coverage | What Jerry currently provides toward this requirement |
| Gap Status | NO COVERAGE / PARTIAL / FULL |
| Source Frameworks | Specific framework items (OWASP, MITRE, NIST) |
| Acceptance Criteria | Testable, verifiable criteria (numbered) |
| Parent Risk IDs | FMEA risk register IDs driving this requirement |
| Jerry Mapping | Specific Jerry components affected |
| Phase 2 Architecture Decision | Recommended architecture decision reference(s) |

---

## Category 1: Agent Identity and Authentication

### FR-SEC-001

| Field | Value |
|-------|-------|
| ID | FR-SEC-001 |
| Title | Unique Agent Identity |
| Priority | CRITICAL |
| Description | The system SHALL assign a unique, non-reusable identity to every agent instance at creation time. Each agent identity SHALL include: agent name, version, parent skill, invocation timestamp, and a cryptographic nonce. |
| Rationale | Identity is the missing foundation for Jerry's security model. Without unique agent identities, access control, audit attribution, and anti-spoofing are impossible. Microsoft's Agent 365 (unique Agent ID per instance) and Google DeepMind's Delegation Capability Tokens validate this as a foundational enterprise requirement. The gap analysis identifies "No Runtime Agent Identity" as the #4 critical gap with aggregate RPN 693. |
| Current Jerry Coverage | Agent definitions include a `name` field (string-based, not unique per instance). No cryptographic identity. No instance-level uniqueness. Agent names are shared across invocations. |
| Gap Status | NO COVERAGE |
| Source Frameworks | OWASP ASI-06 (Identity and Access Mismanagement), Microsoft Agent 365 (Agent ID), NIST IA-4 (Identifier Management) |
| Acceptance Criteria | (1) Every Task invocation produces a unique agent instance ID in the format `{agent-name}-{timestamp}-{nonce}`. (2) No two concurrent agent instances share the same identity. (3) Agent identity is present in all audit log entries. (4) Identity persists for the lifetime of the agent invocation and is immutable after creation. |
| Parent Risk IDs | R-IA-001 (Agent identity spoofing), R-IA-002 (Session hijacking), R-DE-004 (Cross-agent data leakage) |
| Jerry Mapping | Agent definition YAML (`name` field), Task tool invocation, L3 pre-tool gating, orchestration routing context (`routing_history`) |
| Phase 2 Architecture Decision | Decision 9 (Runtime Agent Identity) |

### FR-SEC-002

| Field | Value |
|-------|-------|
| ID | FR-SEC-002 |
| Title | Agent Authentication at Trust Boundaries |
| Priority | CRITICAL |
| Description | The system SHALL authenticate agent identity at every trust boundary crossing: orchestrator-to-worker delegation, inter-skill handoff, and MCP server interaction. Authentication SHALL use the agent's unique identity (FR-SEC-001) validated against the agent registry. |
| Rationale | Trust boundaries (Tool-Result-to-Prompt, Agent-to-Agent, Framework-to-External) are the primary attack surfaces identified by the PS-to-NSE handoff. Without authentication at these boundaries, handoff `from_agent` fields can be spoofed, MCP interactions lack attribution, and rogue agents cannot be distinguished from legitimate ones. |
| Current Jerry Coverage | Handoff protocol defines `from_agent` field but it is self-reported by the agent, not system-verified. No authentication mechanism exists at trust boundaries. |
| Gap Status | NO COVERAGE |
| Source Frameworks | OWASP ASI-06, OWASP ASI-07 (Insecure Inter-Agent Communication), NIST IA-3 (Device Identification and Authentication), NIST IA-9 (Service Identification and Authentication) |
| Acceptance Criteria | (1) Handoff protocol validates `from_agent` field against registered agent names before accepting handoff data. (2) Unregistered agent names are rejected with an authentication failure logged. (3) MCP tool invocations include the invoking agent's identity in the request context. (4) Authentication check executes at L3 (deterministic, pre-tool) for context-rot immunity. |
| Parent Risk IDs | R-IA-001 (Agent identity spoofing), R-IA-003 (Authority bypass), R-IC-001 (Trust boundary exploitation) |
| Jerry Mapping | Handoff protocol (HD-M-001), agent-development-standards.md agent registry, L3 enforcement layer, MCP tool standards |
| Phase 2 Architecture Decision | Decision 9 (Runtime Agent Identity) |

### FR-SEC-003

| Field | Value |
|-------|-------|
| ID | FR-SEC-003 |
| Title | Agent Identity Lifecycle Management |
| Priority | HIGH |
| Description | The system SHALL enforce agent identity lifecycle: creation at Task invocation, active during execution, termination at task completion. Terminated agent identities SHALL NOT be reused. The system SHALL maintain a registry of active agent identities with maximum concurrent instance limits. |
| Rationale | Lifecycle management prevents replay attacks (reusing terminated identities), resource exhaustion (unbounded agent spawning), and orphaned agents (active agents with no parent context). The identity lifecycle is a prerequisite for the comprehensive audit trail (FR-SEC-029). |
| Current Jerry Coverage | Task tool creates and terminates agent contexts, but no formal identity lifecycle is tracked. No active agent registry. No concurrent instance limits. |
| Gap Status | NO COVERAGE |
| Source Frameworks | OWASP ASI-06, NIST IA-4 (Identifier Management), NIST IA-5 (Authenticator Management) |
| Acceptance Criteria | (1) Active agent registry is queryable at any point during execution. (2) Terminated agent IDs are marked as expired and cannot be reused for new invocations. (3) Maximum concurrent agent instances per skill is configurable and enforced (default: 5). (4) Orphaned agent instances (no activity for configurable timeout) are automatically terminated. |
| Parent Risk IDs | R-IA-002 (Session hijacking), R-CF-001 (Unbounded agent spawning), R-AM-004 (Rogue agent behavior) |
| Jerry Mapping | Task tool, orchestration state (ORCHESTRATION.yaml), agent definition schema, L4 post-tool inspection |
| Phase 2 Architecture Decision | Decision 9 (Runtime Agent Identity) |

### FR-SEC-004

| Field | Value |
|-------|-------|
| ID | FR-SEC-004 |
| Title | Agent Provenance Tracking |
| Priority | HIGH |
| Description | The system SHALL track the complete provenance chain for every agent action: which user initiated the session, which orchestrator delegated the task, which agent performed the action, and which tools were invoked. Provenance SHALL be immutable and append-only. |
| Rationale | Provenance is the forensic backbone of the security model. Without it, incident response (FR-SEC-033 through FR-SEC-036) cannot reconstruct attack chains, audit logs (FR-SEC-029) lack attribution, and non-repudiation (NIST AU-10) is unachievable. The gap analysis identifies "No Comprehensive Audit Trail" as the #5 critical gap with aggregate RPN 765. |
| Current Jerry Coverage | Routing observability (RT-M-008) captures routing decisions. Handoff protocol includes routing_history. Worktracker entries provide session-level tracking. No unified provenance chain linking user -> orchestrator -> agent -> tool. |
| Gap Status | PARTIAL |
| Source Frameworks | OWASP ASI-06, OWASP ASI-09 (Insufficient Logging), NIST AU-3 (Content of Audit Records), NIST AU-10 (Non-repudiation) |
| Acceptance Criteria | (1) Every tool invocation log entry includes: user session ID, orchestrator agent ID, executing agent ID, tool name, timestamp. (2) Provenance chain is append-only; no log entry can be modified after creation. (3) Provenance chain is queryable for any completed agent task. (4) Handoff protocol includes provenance metadata (routing_history). |
| Parent Risk IDs | R-IA-001 (Agent identity spoofing), R-DE-002 (System prompt exposure), R-AM-004 (Rogue agent behavior) |
| Jerry Mapping | Routing observability (RT-M-008), handoff protocol, L4 post-tool inspection, worktracker entries |
| Phase 2 Architecture Decision | Decision 9 (Runtime Agent Identity), Decision 8 (Comprehensive Audit Trail) |

---

## Category 2: Authorization and Access Control

### FR-SEC-005

| Field | Value |
|-------|-------|
| ID | FR-SEC-005 |
| Title | Least Privilege Tool Access Enforcement |
| Priority | CRITICAL |
| Description | The system SHALL enforce that every agent operates with the minimum tool access required for its function, as declared in its `capabilities.allowed_tools` YAML field. Tool access SHALL be verified at L3 (deterministic pre-tool gating) before every tool invocation. Any tool invocation not in the agent's allowed list SHALL be blocked. |
| Rationale | Tool access is the primary attack surface for agent manipulation. The gap analysis shows OWASP ASI-02 (Tool Misuse) at PARTIAL coverage because tool tiers are defined and validated at CI (L5) but not enforced at runtime (L3). An agent can potentially invoke tools above its declared tier because the L3 gate currently only checks structural constraints, not security-specific tool access lists. |
| Current Jerry Coverage | Tool tiers T1-T5 defined in agent-development-standards.md. H-34 schema validates `capabilities.allowed_tools` at CI. H-35 ensures workers exclude Task tool. L3 gate exists but does not enforce per-agent tool allowlists at runtime. |
| Gap Status | PARTIAL |
| Source Frameworks | OWASP ASI-02 (Tool Misuse), OWASP ASI-03 (Privilege Escalation), NIST AC-6 (Least Privilege), NIST AC-3 (Access Enforcement) |
| Acceptance Criteria | (1) L3 gate validates every tool invocation against the agent's `capabilities.allowed_tools` list. (2) Blocked tool invocations are logged with agent ID, attempted tool, and reason. (3) Zero false negatives: no tool invocation bypasses the L3 gate. (4) Agent definitions without `capabilities.allowed_tools` are rejected at CI (L5). |
| Parent Risk IDs | R-PE-001 (Tool tier bypass), R-AM-002 (Tool misuse), R-PE-003 (Permission boundary escape via Bash) |
| Jerry Mapping | Tool tiers T1-T5, agent definition schema (H-34), L3 pre-tool gating, L5 CI verification |
| Phase 2 Architecture Decision | Decision 3 (L3 Security Gate Extension) |

### FR-SEC-006

| Field | Value |
|-------|-------|
| ID | FR-SEC-006 |
| Title | Tool Tier Boundary Enforcement |
| Priority | CRITICAL |
| Description | The system SHALL enforce tool tier boundaries (T1-T5) such that an agent assigned tier N cannot invoke any tool from tier N+1 or above. Worker agents (invoked via Task) SHALL NOT be assigned T5 (Full) tier. Tier assignments SHALL be validated against the agent definition schema. |
| Rationale | Tool tiers are Jerry's primary capability restriction mechanism, but they are currently advisory -- validated at CI but not enforced at runtime. The FMEA risk R-PE-001 (Tool tier bypass, RPN 108) has a low RPN only because the Detection score (3) assumes L3 enforcement exists, which it currently does not for security-specific tier checking. Without runtime enforcement, the entire tier system is a governance aspiration rather than a security control. |
| Current Jerry Coverage | T1-T5 tier definitions in agent-development-standards.md with clear selection guidelines. H-35 prevents worker agents from having Task tool. L5 CI validates allowed_tools in schema. No runtime L3 tier enforcement. |
| Gap Status | PARTIAL |
| Source Frameworks | OWASP ASI-02, OWASP ASI-03, NIST AC-6 (Least Privilege), NIST AC-5 (Separation of Duties) |
| Acceptance Criteria | (1) Tool tier mapping is maintained as a SSOT configuration. (2) L3 gate rejects tool invocations that exceed the agent's tier level. (3) No worker agent has Task tool in `capabilities.allowed_tools` (H-35). (4) Tier violations are logged and reported as security events. |
| Parent Risk IDs | R-PE-001 (Tool tier bypass), R-PE-005 (MCP elevated access), R-AM-002 (Tool misuse) |
| Jerry Mapping | Tool tiers T1-T5 (agent-development-standards.md), H-35 (constitutional compliance), L3 enforcement, L5 CI schema validation |
| Phase 2 Architecture Decision | Decision 3 (L3 Security Gate Extension) |

### FR-SEC-007

| Field | Value |
|-------|-------|
| ID | FR-SEC-007 |
| Title | Forbidden Action Enforcement |
| Priority | CRITICAL |
| Description | The system SHALL enforce `capabilities.forbidden_actions` declared in every agent definition. Forbidden actions SHALL be checked at L3 before tool invocation and at L4 after tool completion. The constitutional triplet (P-003, P-020, P-022) SHALL be present in every agent's forbidden actions. |
| Rationale | Forbidden actions are the negative-space complement to allowed tools. While allowed tools define what an agent CAN do, forbidden actions define what it MUST NOT do. The gap analysis shows constitutional constraints are loaded at L1 (session start) and re-injected at L2 (per-prompt), but not enforced deterministically at L3/L4. This means forbidden action declarations are behavioral guidance rather than deterministic controls. |
| Current Jerry Coverage | H-35 requires minimum 3 forbidden actions referencing P-003, P-020, P-022 in every agent definition. L2 re-injects the constitutional triplet per prompt. L5 CI validates forbidden_actions in schema. No L3/L4 deterministic enforcement of forbidden action patterns. |
| Gap Status | PARTIAL |
| Source Frameworks | OWASP ASI-02 (Tool Misuse), OWASP ASI-10 (Rogue Agents), NIST AC-3 (Access Enforcement), NIST SI-10 (Information Input Validation) |
| Acceptance Criteria | (1) Every agent definition includes minimum 3 forbidden actions referencing P-003, P-020, P-022. (2) L3 checks tool invocation patterns against forbidden action declarations. (3) L4 inspects tool outputs for evidence of forbidden action execution. (4) Forbidden action violations trigger immediate agent termination and security event logging. |
| Parent Risk IDs | R-AM-004 (Rogue agent behavior), R-GB-001 (Constitutional circumvention), R-AM-002 (Tool misuse) |
| Jerry Mapping | H-35 (constitutional compliance), agent definition schema, L3/L4 enforcement layers, constitutional constraints |
| Phase 2 Architecture Decision | Decision 3 (L3 Security Gate Extension) |

### FR-SEC-008

| Field | Value |
|-------|-------|
| ID | FR-SEC-008 |
| Title | Privilege Non-Escalation in Delegation Chains |
| Priority | CRITICAL |
| Description | The system SHALL ensure that delegated agents cannot acquire privileges exceeding those of the delegating agent. When an orchestrator delegates to a worker via Task, the worker's effective permissions SHALL be the intersection (not union) of the orchestrator's permissions and the worker's declared permissions. |
| Rationale | Privilege non-escalation is the foundational security property for delegation. Google DeepMind's Delegation Capability Tokens (DCTs) formalize this as cryptographic scope narrowing. OWASP ASI-04 identifies trust boundary violations from privilege accumulation across delegation chains. The FMEA risk R-PE-004 (Privilege accumulation through multi-hop handoffs, RPN 280) documents this threat. Without intersection semantics, a T3 orchestrator could delegate to a T5 worker, effectively escalating privileges. |
| Current Jerry Coverage | P-003 limits delegation to single level (orchestrator -> worker). H-35 prevents workers from having Task tool. Tool tiers exist but intersection semantics are not computed at delegation time. No privilege tracking in handoff metadata. |
| Gap Status | PARTIAL |
| Source Frameworks | OWASP ASI-03 (Privilege Escalation), OWASP ASI-04 (Delegated Trust Boundary Violations), Google DeepMind Delegation Framework (DCTs), NIST AC-6(1) (Authorize Access to Security Functions) |
| Acceptance Criteria | (1) Worker agent effective permissions are computed as: MIN(orchestrator_tier, worker_declared_tier). (2) A T2 orchestrator cannot delegate to a T3 worker. (3) Privilege computation is logged in the handoff metadata. (4) Delegation chains are limited to 1 level per H-01/P-003. |
| Parent Risk IDs | R-PE-004 (Privilege accumulation through handoffs), R-PE-005 (MCP elevated access), R-PE-001 (Tool tier bypass) |
| Jerry Mapping | P-003 (no recursive subagents), tool tiers T1-T5, handoff protocol (criticality propagation CP-04), L3 pre-tool gating |
| Phase 2 Architecture Decision | Decision 7 (Privilege Non-Escalation Enforcement) |

### FR-SEC-009

| Field | Value |
|-------|-------|
| ID | FR-SEC-009 |
| Title | Toxic Tool Combination Prevention |
| Priority | HIGH |
| Description | The system SHALL detect and prevent toxic tool combinations that create exfiltration or exploitation paths. Specifically: (a) database read + external network access in the same agent, (b) file system write + code execution without HITL approval, (c) credential access + external API invocation without scoping. The system SHALL enforce Meta's Rule of Two: no agent satisfies all three of processing untrusted input, accessing sensitive data, and changing external state without HITL. |
| Rationale | Toxic tool combinations are the mechanism by which individual safe tools become dangerous in combination. The gap analysis identifies Bash tool unrestricted execution as the #3 critical gap with aggregate RPN 1,285, specifically because Bash combined with Read creates a credential harvesting + exfiltration path. Meta's Rule of Two provides a concrete, enforceable design constraint adopted by industry consensus. |
| Current Jerry Coverage | Tool tiers restrict Bash to T2+. Agent definitions declare allowed_tools. No toxic combination registry. No Rule of Two enforcement. No HITL for dangerous combinations. |
| Gap Status | NO COVERAGE |
| Source Frameworks | OWASP ASI-02 (Tool Misuse), Meta Rule of Two, NIST AC-6(3) (Network Access to Privileged Commands), ATLAS AML.T0053 (Exfiltration via ML API) |
| Acceptance Criteria | (1) A toxic combination registry defines prohibited tool pairings. (2) L3 gate checks the agent's full tool set against the toxic combination registry at invocation time. (3) Agents violating Rule of Two constraints trigger HITL approval requirement. (4) Toxic combination detection is configurable and extensible. |
| Parent Risk IDs | R-PE-003 (Permission boundary escape via Bash), R-DE-006 (Exfiltration via Bash), R-DE-001 (Credential leakage) |
| Jerry Mapping | Tool tiers T1-T5, agent definition `capabilities.allowed_tools`, L3 enforcement, P-020 (user authority for HITL) |
| Phase 2 Architecture Decision | Decision 3 (L3 Security Gate Extension), Decision 4 (Bash Command Sandboxing) |

### FR-SEC-010

| Field | Value |
|-------|-------|
| ID | FR-SEC-010 |
| Title | Permission Boundary Isolation Between Skills |
| Priority | HIGH |
| Description | The system SHALL enforce permission boundaries between skills such that agents from different skills cannot access each other's internal state, tool results, or intermediate artifacts unless explicitly shared via the handoff protocol. Each skill SHALL operate in its own context isolation boundary. |
| Rationale | Context isolation prevents cross-contamination between skills and limits the blast radius of a compromised agent. The Task tool's inherent context boundary (Pattern 2: Orchestrator-Worker) provides natural isolation, but intermediate artifacts on the filesystem are accessible to any agent with Read access. OWASP ASI-04 identifies trust boundary violations as a top-10 agentic threat. |
| Current Jerry Coverage | Task tool provides context isolation (each worker gets fresh context). Handoff protocol defines explicit data sharing. However, filesystem artifacts are accessible to any agent with Read tool access (T1+). No directory-level permission enforcement between skills. |
| Gap Status | PARTIAL |
| Source Frameworks | OWASP ASI-04 (Delegated Trust Boundary Violations), NIST AC-4 (Information Flow Enforcement), NIST SC-7 (Boundary Protection) |
| Acceptance Criteria | (1) No agent can read artifacts produced by another skill's agents without receiving them via handoff. (2) Tool results from one agent invocation are not accessible to other agent invocations. (3) Context isolation is enforced by the Task tool's inherent context boundary (Pattern 2: Orchestrator-Worker). (4) Shared state is limited to the handoff protocol's defined fields. |
| Parent Risk IDs | R-DE-004 (Cross-agent data leakage), R-IC-001 (Trust boundary exploitation), R-PE-004 (Privilege accumulation) |
| Jerry Mapping | Task tool context isolation, handoff protocol (HD-M-001), agent-routing-standards.md context sharing, P-003 single-level nesting |
| Phase 2 Architecture Decision | Decision 3 (L3 Security Gate Extension) |

---

## Category 3: Input Validation

### FR-SEC-011

| Field | Value |
|-------|-------|
| ID | FR-SEC-011 |
| Title | Direct Prompt Injection Prevention |
| Priority | CRITICAL |
| Description | The system SHALL validate all user-provided input for prompt injection patterns before the input reaches agent processing. Validation SHALL include: (a) detection of instruction override patterns ("ignore previous instructions", "you are now", system prompt extraction attempts), (b) detection of role manipulation attempts, (c) detection of encoding-based evasion (Base64, Unicode, homoglyph substitution). |
| Rationale | Direct prompt injection is the primary attack vector against LLM-based systems. The FMEA risk R-PI-001 (Direct prompt injection, RPN 192) has a moderate RPN because Jerry's L2 re-injection provides strong resilience -- constitutional rules are re-injected every prompt regardless of injection attempts. However, L3 input validation does not currently exist, meaning injection patterns reach the LLM unfiltered. The gap analysis shows ASI-01 at PARTIAL coverage specifically because L3 input sanitization is missing. |
| Current Jerry Coverage | L2 per-prompt re-injection of constitutional rules (immune to context rot). P-020 user authority re-injected every prompt. No L3 input validation for injection patterns. No pattern database for known injection techniques. |
| Gap Status | NO COVERAGE (for L3 input validation; L2 provides partial resilience) |
| Source Frameworks | OWASP LLM01 (Prompt Injection), OWASP ASI-01 (Agent Goal Hijack), ATLAS AML.T0051 (LLM Prompt Injection), NIST SI-10 (Information Input Validation) |
| Acceptance Criteria | (1) Input validation filter operates at L3 (deterministic, pre-processing). (2) Known prompt injection patterns are maintained in a versioned pattern database. (3) Detection rate >= 95% against the OWASP prompt injection test suite. (4) False positive rate <= 5% on legitimate user requests. (5) Detected injection attempts are logged with full context for forensic analysis. |
| Parent Risk IDs | R-PI-001 (Direct prompt injection), R-PI-005 (Goal hijacking via progressive manipulation), R-AM-001 (Agent goal hijacking) |
| Jerry Mapping | L3 pre-tool gating, guardrails.input_validation in agent definitions, L2 per-prompt re-injection (constitutional constraints immune to injection) |
| Phase 2 Architecture Decision | Decision 1 (Tool-Output Firewall) |

### FR-SEC-012

| Field | Value |
|-------|-------|
| ID | FR-SEC-012 |
| Title | Indirect Prompt Injection Prevention via Tool Results |
| Priority | CRITICAL |
| Description | The system SHALL treat all data returned by tool invocations (Read, Grep, Glob, WebFetch, WebSearch, MCP tools) as untrusted input. Tool results SHALL be validated at L4 (post-tool inspection) for embedded instruction patterns before being consumed by agent reasoning. The system SHALL maintain a clear boundary between tool result data and agent instructions. |
| Rationale | Indirect prompt injection via tool results is the #1 risk in the FMEA register (R-PI-002, RPN 504). The gap analysis identifies "No Tool-Output Firewall" as the #1 critical gap with aggregate RPN 1,636. Every framework -- OWASP, MITRE, Cisco -- identifies instruction/data confusion as the primary agentic attack vector. Jerry mandates MCP usage (MCP-001, MCP-002) but has no defense against poisoned responses. The joint OpenAI/Anthropic/Google DeepMind study demonstrated >90% bypass rates against published defenses when used alone, validating defense-in-depth as the only viable strategy. |
| Current Jerry Coverage | No L3/L4 gate on MCP tool output content. No content scanning on Read tool results. L2 re-injection provides partial resilience (constitutional rules persist regardless of tool output content). No data/instruction boundary enforcement. |
| Gap Status | NO COVERAGE |
| Source Frameworks | OWASP LLM01 (Prompt Injection -- Indirect), OWASP ASI-01 (Agent Goal Hijack), OWASP ASI-05 (Memory and Context Manipulation), ATLAS AML.T0051.001 (Indirect Prompt Injection) |
| Acceptance Criteria | (1) L4 inspection layer scans tool results for instruction injection patterns. (2) Tool results are clearly delimited from system/agent instructions in the context. (3) Suspected indirect injection in tool results triggers: (a) flagging in the audit log, (b) presentation to user for review if above confidence threshold. (4) MCP server responses receive heightened scrutiny (external trust boundary). |
| Parent Risk IDs | R-PI-002 (Indirect injection via MCP tool results, RPN 504), R-PI-003 (Indirect injection via file contents, RPN 392), R-SC-004 (Context7 data poisoning, RPN 320) |
| Jerry Mapping | L4 post-tool inspection, MCP tool standards, guardrails.output_filtering, tool result handling in agent methodology |
| Phase 2 Architecture Decision | Decision 1 (Tool-Output Firewall) |

### FR-SEC-013

| Field | Value |
|-------|-------|
| ID | FR-SEC-013 |
| Title | MCP Server Input Sanitization |
| Priority | CRITICAL |
| Description | The system SHALL sanitize all data sent to and received from MCP servers. Outbound sanitization SHALL prevent leakage of system prompts, constitutional rules, internal file paths, and credentials. Inbound sanitization SHALL validate MCP responses against expected schemas and reject malformed or suspicious responses. |
| Rationale | MCP is the highest-risk external attack surface. The Anthropic GTG-1002 incident, Cisco's "vast unmonitored attack surface" finding, and OWASP ASI-01/ASI-04 all converge on MCP servers as the primary external threat vector. Jerry's MCP integration currently trusts registered servers without input/output sanitization. The FMEA risk R-SC-001 (Malicious MCP server packages, RPN 480) is the #2 highest-scoring risk. |
| Current Jerry Coverage | MCP tool standards define canonical tool names and error handling fallbacks. No input/output sanitization on MCP communications. No schema validation on MCP responses. No outbound data leakage prevention. |
| Gap Status | NO COVERAGE |
| Source Frameworks | OWASP ASI-01 (Agent Goal Hijack via MCP), OWASP LLM03 (Supply Chain), Cisco State of AI Security 2026 (MCP attack surface), NIST SC-7 (Boundary Protection), NIST SI-10 (Information Input Validation) |
| Acceptance Criteria | (1) MCP outbound requests are filtered to exclude: system prompt content, L2 REINJECT markers, file paths outside approved directories, environment variables, credentials. (2) MCP inbound responses are validated against the MCP response schema. (3) MCP responses exceeding configurable size limits are truncated with a warning. (4) All MCP interactions are logged with full request/response metadata. |
| Parent Risk IDs | R-SC-001 (Malicious MCP server packages, RPN 480), R-PI-002 (Indirect injection via MCP, RPN 504), R-SC-004 (Context7 data poisoning, RPN 320) |
| Jerry Mapping | MCP tool standards (mcp-tool-standards.md), L3/L4 enforcement around MCP calls, canonical tool names, error handling fallbacks |
| Phase 2 Architecture Decision | Decision 1 (Tool-Output Firewall), Decision 2 (MCP Supply Chain Verification) |

### FR-SEC-014

| Field | Value |
|-------|-------|
| ID | FR-SEC-014 |
| Title | Context Manipulation Prevention |
| Priority | HIGH |
| Description | The system SHALL prevent manipulation of the agent's context window through: (a) enforcing L2 per-prompt re-injection of constitutional constraints (immune to context rot), (b) detecting attempts to exhaust the context window (unbounded consumption), (c) validating that context items have not been tampered with between handoffs. |
| Rationale | Context manipulation is a meta-attack that undermines all behavioral guardrails. The FMEA risk R-GB-001 (Constitutional circumvention via context rot, RPN 432) is the #3 highest-scoring risk. Jerry's L2 re-injection is a genuinely novel defense -- no other framework has an equivalent mechanism -- but it protects only the 20 Tier A HARD rules. Context manipulation via unbounded tool results (CB-02 violation) or poisoned handoff data can still degrade agent reasoning quality. |
| Current Jerry Coverage | L2 per-prompt re-injection (immune to context rot). AE-006 graduated escalation for context fill monitoring. Context budget standards CB-01 through CB-05 (advisory). No integrity verification on handoff data or Memory-Keeper stored content. |
| Gap Status | PARTIAL |
| Source Frameworks | OWASP ASI-05 (Memory and Context Manipulation), OWASP LLM10 (Unbounded Consumption), ATLAS AML.T0080 (Memory Poisoning), NIST SI-7 (Software, Firmware, and Information Integrity) |
| Acceptance Criteria | (1) L2 re-injection operates on every prompt regardless of context state. (2) Context fill monitoring per AE-006 graduated escalation detects unbounded consumption. (3) Handoff data integrity is validated via key_findings checksums. (4) Context window consumption by any single tool result is bounded per CB-02 (50% maximum). |
| Parent Risk IDs | R-GB-001 (Constitutional circumvention via context rot, RPN 432), R-AM-003 (Memory/context manipulation, RPN 320), R-PI-005 (Goal hijacking via progressive manipulation, RPN 384) |
| Jerry Mapping | L2 per-prompt re-injection, AE-006 graduated escalation, context budget standards CB-01 through CB-05, handoff protocol integrity |
| Phase 2 Architecture Decision | Decision 1 (Tool-Output Firewall) |

### FR-SEC-015

| Field | Value |
|-------|-------|
| ID | FR-SEC-015 |
| Title | Agent Goal Integrity Verification |
| Priority | HIGH |
| Description | The system SHALL verify that agent goals and objectives have not been altered during execution. The original task description, success criteria, and criticality level from the handoff protocol SHALL be immutable after delegation. Any detected goal modification SHALL trigger agent termination and security event logging. |
| Rationale | Goal integrity is the semantic counterpart to context integrity (FR-SEC-014). While FR-SEC-014 prevents structural manipulation of the context, FR-SEC-015 prevents semantic manipulation of the agent's objectives. The FMEA risk R-AM-001 (Agent goal hijacking, RPN 378) documents the threat of an attacker progressively steering an agent away from its intended purpose. Without goal verification, subtle misdirection across multiple turns is undetectable. |
| Current Jerry Coverage | Handoff protocol includes `task` and `success_criteria` fields. No immutability enforcement on these fields after delegation. No L4 output-vs-goal consistency checking. No behavioral drift detection. |
| Gap Status | NO COVERAGE |
| Source Frameworks | OWASP ASI-01 (Agent Goal Hijack), ATLAS AML.T0051 (Prompt Injection), NIST SI-7 (Information Integrity) |
| Acceptance Criteria | (1) Handoff `task` and `success_criteria` fields are immutable after initial delegation. (2) L4 post-tool inspection detects if agent output diverges significantly from stated success criteria. (3) Goal modification attempts are logged as security events. (4) Orchestrator validates that worker output aligns with delegated task before accepting results. |
| Parent Risk IDs | R-AM-001 (Agent goal hijacking, RPN 378), R-PI-005 (Goal hijacking via progressive manipulation, RPN 384), R-GB-002 (Quality gate manipulation) |
| Jerry Mapping | Handoff protocol (HD-M-001), success_criteria field, L4 post-tool inspection, orchestration state tracking |
| Phase 2 Architecture Decision | Decision 1 (Tool-Output Firewall) |

### FR-SEC-016

| Field | Value |
|-------|-------|
| ID | FR-SEC-016 |
| Title | Encoding and Obfuscation Attack Prevention |
| Priority | MEDIUM |
| Description | The system SHALL detect and neutralize encoding-based attacks including: Base64-encoded instructions, Unicode normalization attacks, homoglyph substitution, invisible Unicode characters, right-to-left override characters, and multi-layer encoding chains. |
| Rationale | Encoding-based evasion is a well-documented technique for bypassing prompt injection filters. ATLAS AML.T0051.002 specifically addresses prompt injection evasion techniques. While individually less impactful than indirect injection, encoding attacks can bypass L3 input validation (FR-SEC-011) if not explicitly handled. |
| Current Jerry Coverage | No input pre-processing for encoding normalization. No multi-layer decoding. No homoglyph detection. |
| Gap Status | NO COVERAGE |
| Source Frameworks | OWASP LLM01 (Prompt Injection -- evasion techniques), ATLAS AML.T0051.002 (Prompt Injection Evasion), NIST SI-10 (Information Input Validation) |
| Acceptance Criteria | (1) Input pre-processing normalizes all Unicode to NFC form. (2) Base64 and other common encodings are detected and decoded for inspection. (3) Invisible/control characters are stripped from user input. (4) Multi-layer encoding (e.g., Base64 of URL-encoded content) is recursively decoded up to configurable depth (default: 3 layers). |
| Parent Risk IDs | R-PI-001 (Direct prompt injection), R-PI-006 (Injection via structured data) |
| Jerry Mapping | L3 pre-tool input validation, guardrails.input_validation in agent definitions |
| Phase 2 Architecture Decision | Decision 1 (Tool-Output Firewall) |

---

## Category 4: Output Security

### FR-SEC-017

| Field | Value |
|-------|-------|
| ID | FR-SEC-017 |
| Title | Sensitive Information Output Filtering |
| Priority | CRITICAL |
| Description | The system SHALL filter agent output to prevent disclosure of: (a) system prompts and constitutional rules, (b) L2 REINJECT markers and enforcement architecture details, (c) internal file paths beyond the project workspace, (d) credentials, API keys, tokens, and secrets, (e) other agents' handoff data not intended for the user. |
| Rationale | Output filtering is the last line of defense before information reaches the user or downstream systems. The gap analysis shows OWASP LLM02 (Sensitive Information Disclosure) and LLM07 (System Prompt Leakage) both at PARTIAL coverage. Jerry's guardrails template requires `no_secrets_in_output` but this is a behavioral L1 guardrail, not a deterministic L4 filter. The FMEA risks R-DE-001 (Credential leakage, RPN 270) and R-DE-002 (System prompt exposure, RPN 294) both cite the absence of L4 deterministic filtering. |
| Current Jerry Coverage | Guardrails template requires `no_secrets_in_output` in output_filtering (behavioral, L1). P-022 prevents deceptive output. No L4 deterministic secret detection. No output scanning for system prompt content. No credential pattern matching. |
| Gap Status | PARTIAL |
| Source Frameworks | OWASP LLM02 (Sensitive Information Disclosure), OWASP LLM07 (System Prompt Leakage), NIST SC-28 (Protection of Information at Rest), NIST SI-15 (Information Output Filtering) |
| Acceptance Criteria | (1) Output filtering operates at L4 (post-tool inspection) before presenting results to user. (2) Known sensitive patterns (API key formats, credential patterns, REINJECT markers) are detected and redacted. (3) System prompt extraction attempts that succeed are caught at output and redacted. (4) Filtering rules are versioned and extensible. |
| Parent Risk IDs | R-DE-001 (Credential leakage, RPN 270), R-DE-002 (System prompt exposure, RPN 294), R-DE-003 (Sensitive file content exposure, RPN 250) |
| Jerry Mapping | L4 post-tool inspection, guardrails.output_filtering in agent definitions (minimum 3 entries per H-34), constitutional constraints |
| Phase 2 Architecture Decision | Decision 5 (L4 Output Security Gate) |

### FR-SEC-018

| Field | Value |
|-------|-------|
| ID | FR-SEC-018 |
| Title | Output Sanitization for Downstream Consumption |
| Priority | HIGH |
| Description | The system SHALL sanitize agent output that will be consumed by downstream systems, tools, or other agents. Sanitization SHALL prevent: (a) injection attacks via agent output (command injection, path traversal), (b) unvalidated code execution from agent-generated code, (c) malformed data that could corrupt downstream processing. |
| Rationale | Agent output becomes input for downstream consumers (other agents via handoff, Bash tool execution, file writes). If agent output contains malicious patterns, they propagate through the pipeline. OWASP ASI-08 (Cascading Failures) identifies this as a compound threat where one compromised agent's output corrupts downstream agents. |
| Current Jerry Coverage | Handoff schema (HD-M-001) validates structure but not content. P-020 requires user approval for code execution. Agent-generated code lacks static analysis before execution. |
| Gap Status | PARTIAL |
| Source Frameworks | OWASP LLM05 (Improper Output Handling), OWASP ASI-08 (Cascading Failures), NIST SI-15 (Information Output Filtering), NIST SI-3 (Malicious Code Protection) |
| Acceptance Criteria | (1) Agent-generated file paths are validated against an allowlist of permitted directories. (2) Agent-generated code requires HITL approval before execution (P-020). (3) Agent output consumed by other agents via handoff is schema-validated (HD-M-001). (4) Command-like patterns in output are flagged for review. |
| Parent Risk IDs | R-CF-003 (Error propagation through handoff chains), R-AM-002 (Tool misuse), R-DE-006 (Exfiltration via Bash) |
| Jerry Mapping | L4 post-tool inspection, handoff protocol schema validation, P-020 (user authority), Bash tool usage patterns |
| Phase 2 Architecture Decision | Decision 5 (L4 Output Security Gate) |

### FR-SEC-019

| Field | Value |
|-------|-------|
| ID | FR-SEC-019 |
| Title | System Prompt Leakage Prevention |
| Priority | HIGH |
| Description | The system SHALL prevent leakage of system prompts, CLAUDE.md content, rule files, L2 REINJECT markers, and enforcement architecture details through any output channel. The system SHALL detect system prompt extraction techniques including: direct asking, encoding tricks, role-play scenarios, and iterative probing. |
| Rationale | System prompt leakage exposes the governance structure, enabling targeted attacks against specific enforcement gaps. The FMEA risk R-DE-002 (System prompt exposure, RPN 294) and R-PI-004 (System prompt extraction, RPN 245) both address this threat. L2 re-injection ensures rules persist even if extracted (the attacker knows the rules but cannot disable them), but leakage still aids attacker reconnaissance. |
| Current Jerry Coverage | L2 re-injection ensures rules persist regardless of extraction. P-022 prevents deceptive output. No L4 output filter for system prompt content. No canary token detection. |
| Gap Status | PARTIAL |
| Source Frameworks | OWASP LLM07 (System Prompt Leakage), NIST SC-28 (Protection of Information at Rest), NIST AC-3 (Access Enforcement) |
| Acceptance Criteria | (1) Output filter detects verbatim or near-verbatim reproduction of rule file content. (2) L2 REINJECT marker content is never present in user-facing output. (3) Enforcement architecture details (layer names, token budgets, strategy IDs) are not disclosed unless user is an authorized administrator. (4) System prompt extraction test suite achieves >= 95% prevention rate. |
| Parent Risk IDs | R-DE-002 (System prompt exposure, RPN 294), R-PI-004 (System prompt extraction, RPN 245) |
| Jerry Mapping | L4 output inspection, .context/rules/ files, L2 REINJECT markers, enforcement architecture documentation |
| Phase 2 Architecture Decision | Decision 5 (L4 Output Security Gate) |

### FR-SEC-020

| Field | Value |
|-------|-------|
| ID | FR-SEC-020 |
| Title | Confidence and Uncertainty Disclosure |
| Priority | MEDIUM |
| Description | The system SHALL ensure that agents accurately represent their confidence levels and uncertainty in outputs per P-022 (no deception). Agent outputs SHALL include confidence indicators when making claims, recommendations, or decisions. The system SHALL detect and prevent confidence inflation (leniency bias). |
| Rationale | Confidence inflation is a known LLM failure mode (leniency bias documented in quality-enforcement.md). Without forced uncertainty disclosure, agents can present low-confidence conclusions as high-confidence, violating P-022 and degrading user trust. OWASP LLM09 (Misinformation) and OWASP ASI-09 (Human-Agent Trust Exploitation) both address this threat. |
| Current Jerry Coverage | Handoff confidence scores with calibration guidance (0.0-1.0 scale per HD-M-001). S-014 LLM-as-Judge scoring counteracts leniency bias. S-010 self-review. No forced uncertainty disclosure on agent outputs. |
| Gap Status | PARTIAL |
| Source Frameworks | OWASP LLM09 (Misinformation), P-022 (No Deception), NIST AI RMF MEASURE function, NIST SI-12 (Information Management and Retention) |
| Acceptance Criteria | (1) Handoff confidence scores follow calibration guidance (0.0-1.0 scale per HD-M-001). (2) S-014 LLM-as-Judge scoring actively counteracts leniency bias per quality-enforcement.md. (3) Agent outputs for C2+ deliverables include explicit confidence/uncertainty statements. (4) Claims without supporting evidence are flagged during self-review (S-010). |
| Parent Risk IDs | R-GB-002 (Quality gate manipulation), R-AM-004 (Rogue agent behavior) |
| Jerry Mapping | P-022 (no deception), handoff protocol confidence field, S-014 scoring, S-010 self-review, quality gate (H-13) |
| Phase 2 Architecture Decision | Decision 5 (L4 Output Security Gate) |

---

## Category 5: Inter-Agent Communication

### FR-SEC-021

| Field | Value |
|-------|-------|
| ID | FR-SEC-021 |
| Title | Structured Handoff Protocol Enforcement |
| Priority | HIGH |
| Description | The system SHALL enforce that all inter-agent communication uses the structured handoff protocol (handoff-v2 schema). Free-text handoffs without schema validation SHALL be rejected. Every handoff SHALL include all required fields: from_agent, to_agent, task, success_criteria, artifacts, key_findings, blockers, confidence, criticality. |
| Rationale | Structured handoffs mitigate error amplification (R-T02, RPN 336) by replacing free-text summaries with schema-validated data contracts. The gap analysis shows OWASP ASI-07 (Insecure Inter-Agent Communication) at PARTIAL coverage because handoff schema validation is defined but not enforced at L3. Handoff protocol is currently HD-M-001 (MEDIUM standard) rather than a HARD rule, meaning non-compliant handoffs are not deterministically blocked. |
| Current Jerry Coverage | Handoff protocol (HD-M-001 through HD-M-005) fully defined in agent-development-standards.md. Handoff-v2 schema specified. Send-side and receive-side validation defined. All standards are MEDIUM tier (not enforced, recommended). |
| Gap Status | PARTIAL |
| Source Frameworks | OWASP ASI-07 (Insecure Inter-Agent Communication), NIST SC-8 (Transmission Confidentiality and Integrity), NIST SI-10 (Information Input Validation) |
| Acceptance Criteria | (1) Handoff schema validation executes at L3 before agent invocation. (2) Schema validation rejects handoffs missing any required field. (3) Free-text delegation (unstructured Task prompts) triggers a warning and automatic schema wrapping. (4) Schema version is tracked in every handoff for compatibility verification. |
| Parent Risk IDs | R-IC-001 (Trust boundary exploitation), R-IC-002 (Handoff poisoning), R-CF-003 (Error propagation through handoff chains) |
| Jerry Mapping | Handoff protocol (HD-M-001 through HD-M-005), agent-development-standards.md, L3 pre-tool gating, handoff-v2 schema |
| Phase 2 Architecture Decision | Decision 6 (Handoff Security Extensions) |

### FR-SEC-022

| Field | Value |
|-------|-------|
| ID | FR-SEC-022 |
| Title | Trust Boundary Enforcement at Handoffs |
| Priority | HIGH |
| Description | The system SHALL enforce trust boundaries at every handoff: (a) criticality level SHALL NOT decrease through handoff chains (CP-04), (b) persistent blockers SHALL propagate with [PERSISTENT] prefix (CP-05), (c) artifact paths SHALL be validated for existence before delivery (HD-M-002), (d) quality gate SHALL be passed before handoff delivery for C2+ (HD-M-003). |
| Rationale | Trust boundary violations at handoffs are a compound threat: criticality downgrade allows under-review, artifact path manipulation enables read-access to unintended files, and blocker suppression hides systemic issues. The PS-to-NSE handoff identified three trust boundaries (Tool-Result-to-Prompt, Agent-to-Agent, Framework-to-External) that require enforcement. |
| Current Jerry Coverage | CP-01 through CP-05 context passing conventions defined. HD-M-001 through HD-M-005 handoff standards defined. All are MEDIUM tier (recommended, not enforced). No L3 enforcement of trust boundary rules at handoffs. |
| Gap Status | PARTIAL |
| Source Frameworks | OWASP ASI-04 (Delegated Trust Boundary Violations), OWASP ASI-07, NIST AC-4 (Information Flow Enforcement), NIST SC-7 (Boundary Protection) |
| Acceptance Criteria | (1) Criticality downgrade attempts are blocked and logged. (2) Persistent blockers present in source handoff appear in all downstream handoffs. (3) Artifact paths that do not resolve to existing files cause handoff rejection. (4) C2+ handoffs without quality gate score >= 0.92 are held pending revision. |
| Parent Risk IDs | R-IC-001 (Trust boundary exploitation), R-PE-004 (Privilege accumulation through handoffs), R-CF-003 (Error propagation) |
| Jerry Mapping | Handoff protocol (CP-01 through CP-05), HD-M-001 through HD-M-005, quality gate (H-13), L3/L4 enforcement |
| Phase 2 Architecture Decision | Decision 6 (Handoff Security Extensions) |

### FR-SEC-023

| Field | Value |
|-------|-------|
| ID | FR-SEC-023 |
| Title | Message Integrity in Handoff Chains |
| Priority | MEDIUM |
| Description | The system SHALL ensure message integrity across handoff chains by: (a) including a hash of key handoff fields (task, success_criteria, criticality) that downstream agents can verify, (b) detecting if handoff content has been modified in transit, (c) logging the complete handoff chain for forensic analysis. |
| Rationale | The risk register vulnerability V-004 identifies that handoffs have no cryptographic verification. Without integrity checking, a compromised intermediate agent could modify handoff content without detection, enabling the Telephone Game anti-pattern (AP-03) to become a security vulnerability rather than just a quality degradation. |
| Current Jerry Coverage | Handoff protocol tracks routing_history. No cryptographic integrity verification on handoff fields. No hash computation or verification. Complete handoff chains are partially reconstructable from worktracker entries but not from a dedicated integrity log. |
| Gap Status | NO COVERAGE |
| Source Frameworks | OWASP ASI-07 (Insecure Inter-Agent Communication), NIST SC-8 (Transmission Integrity), NIST SC-13 (Cryptographic Protection), NIST AU-10 (Non-repudiation) |
| Acceptance Criteria | (1) Handoff metadata includes a SHA-256 hash of immutable fields. (2) Receiving agent validates the hash before processing. (3) Hash mismatch triggers handoff rejection and security event. (4) Complete handoff chains are reconstructable from audit logs. |
| Parent Risk IDs | R-IC-002 (Handoff poisoning), R-IC-004 (Cross-pipeline contamination), R-AM-003 (Memory/context manipulation) |
| Jerry Mapping | Handoff protocol, routing_history tracking, L4 post-tool inspection, orchestration state |
| Phase 2 Architecture Decision | Decision 6 (Handoff Security Extensions) |

### FR-SEC-024

| Field | Value |
|-------|-------|
| ID | FR-SEC-024 |
| Title | Anti-Spoofing for Agent Communication |
| Priority | HIGH |
| Description | The system SHALL prevent agent identity spoofing in inter-agent communication. An agent SHALL NOT be able to impersonate another agent by modifying the `from_agent` field in handoffs. The system SHALL validate that the `from_agent` field matches the actual invoking agent's registered identity. |
| Rationale | Agent spoofing enables a compromised agent to impersonate a trusted agent, bypassing trust-based access controls and corrupting audit trails. Send-side validation (SV-02) currently relies on the agent self-reporting its identity -- a classic confused deputy problem. The system must set `from_agent` based on the invocation context, not the agent's self-declaration. |
| Current Jerry Coverage | SV-02 defines that `from_agent` should match the sending agent's name. This is a self-reported check -- the sending agent validates itself. No system-level identity injection. No detection of spoofed from_agent values. |
| Gap Status | NO COVERAGE |
| Source Frameworks | OWASP ASI-07, OWASP ASI-10 (Rogue Agents), NIST IA-3 (Device Identification and Authentication), NIST SC-23 (Session Authenticity) |
| Acceptance Criteria | (1) Handoff `from_agent` is set by the system (not by the agent) based on the invocation context. (2) Agent-supplied `from_agent` values that do not match the system-assigned identity are rejected. (3) Spoofing attempts are logged as security events with full context. (4) Send-side validation (SV-02) is enforced by the system, not self-reported. |
| Parent Risk IDs | R-IA-001 (Agent identity spoofing), R-IC-002 (Handoff poisoning), R-AM-004 (Rogue agent behavior) |
| Jerry Mapping | Handoff protocol (SV-02), agent identity (FR-SEC-001), L3 enforcement, Task tool invocation context |
| Phase 2 Architecture Decision | Decision 9 (Runtime Agent Identity), Decision 6 (Handoff Security Extensions) |

---

## Category 6: Supply Chain Security

### FR-SEC-025

| Field | Value |
|-------|-------|
| ID | FR-SEC-025 |
| Title | MCP Server Integrity Verification |
| Priority | CRITICAL |
| Description | The system SHALL verify the integrity of all MCP servers before allowing agent interaction. Verification SHALL include: (a) server identity validation against an approved server registry, (b) configuration checksum verification, (c) detection of unauthorized server modifications. Only registered MCP servers SHALL be permitted for agent use. |
| Rationale | MCP supply chain is the #2 critical gap with aggregate RPN 1,198. Malicious MCP servers (R-SC-001, RPN 480) represent the second-highest risk in the entire register. Cisco identifies MCP as a "vast unmonitored attack surface." The ClawHavoc campaign (800+ malicious skills) and the Cline supply chain attack demonstrate this is an active, scalable attack class. Jerry currently configures MCP servers manually in `.claude/settings.local.json` with no integrity checking. |
| Current Jerry Coverage | MCP servers registered in `.claude/settings.local.json`. No integrity verification. No checksum validation. No approved server registry beyond the configuration file. No runtime monitoring. |
| Gap Status | NO COVERAGE |
| Source Frameworks | OWASP LLM03 (Supply Chain), OWASP ASI-04 (Supply Chain Vulnerabilities), Cisco State of AI Security 2026, Anthropic GTG-1002 lessons, NIST SA-12 (Supply Chain Protection), NIST SI-7 (Software Integrity) |
| Acceptance Criteria | (1) MCP server registry maintained in `.claude/settings.local.json` with checksums. (2) MCP server configuration changes trigger security event logging. (3) Unauthorized MCP servers (not in registry) are blocked at L3. (4) MCP server health checks execute before first tool invocation in a session. |
| Parent Risk IDs | R-SC-001 (Malicious MCP server packages, RPN 480), R-SC-002 (Dependency poisoning, RPN 378), R-PI-002 (Indirect injection via MCP, RPN 504) |
| Jerry Mapping | MCP tool standards (mcp-tool-standards.md), `.claude/settings.local.json`, canonical tool names, L3 pre-tool gating |
| Phase 2 Architecture Decision | Decision 2 (MCP Supply Chain Verification) |

### FR-SEC-026

| Field | Value |
|-------|-------|
| ID | FR-SEC-026 |
| Title | Dependency Verification for Agent Definitions |
| Priority | HIGH |
| Description | The system SHALL verify the integrity of agent definition files before loading them for execution. Verification SHALL include: (a) YAML schema validation against the canonical JSON Schema (H-34), (b) constitutional compliance check (P-003, P-020, P-022 present per H-35), (c) file integrity verification (no unauthorized modifications since last CI validation). |
| Rationale | Agent definitions are the behavioral genome of each agent. The FMEA risk R-SC-003 (Skill/agent definition tampering, RPN 160) documents the threat of malicious modifications to agent YAML/Markdown that alter behavior, remove guardrails, or expand tool access. H-34 provides CI-time validation but no runtime verification. |
| Current Jerry Coverage | H-34 schema validation at L5 CI. H-35 constitutional triplet verification at L5 CI. Git version control tracks modifications. No runtime (L3) verification of agent definitions before loading. |
| Gap Status | PARTIAL |
| Source Frameworks | OWASP LLM03 (Supply Chain), OWASP ASI-10 (Rogue Agents), NIST SA-12 (Supply Chain Protection), NIST CM-3 (Configuration Change Control) |
| Acceptance Criteria | (1) Agent definitions are schema-validated at L3 before any Task invocation. (2) Missing constitutional triplet causes agent load rejection. (3) Agent definition files are tracked by L5 CI for unauthorized modifications. (4) Modified agent definitions require re-validation before use. |
| Parent Risk IDs | R-SC-003 (Skill/agent definition tampering, RPN 160), R-AM-004 (Rogue agent behavior), R-GB-001 (Constitutional circumvention) |
| Jerry Mapping | H-34 (agent definition schema), H-35 (constitutional compliance), L3 pre-tool gating, L5 CI verification |
| Phase 2 Architecture Decision | Decision 2 (MCP Supply Chain Verification) |

### FR-SEC-027

| Field | Value |
|-------|-------|
| ID | FR-SEC-027 |
| Title | Skill Integrity Verification |
| Priority | HIGH |
| Description | The system SHALL verify skill integrity before skill invocation. Verification SHALL include: (a) SKILL.md existence and format validation (H-25, H-26), (b) agent definition integrity within the skill, (c) skill registration in CLAUDE.md and AGENTS.md, (d) detection of unauthorized skill modifications since last commit. |
| Rationale | Skills are the organizational unit above agents. A compromised skill could contain modified agent definitions, altered SKILL.md routing metadata, or unregistered agents. The supply chain threat extends from individual agent definitions (FR-SEC-026) to the skill container level. |
| Current Jerry Coverage | H-25/H-26 skill standards verified at L5 CI. CLAUDE.md and AGENTS.md skill registration. Git tracks skill modifications. No runtime (L3) skill integrity verification. |
| Gap Status | PARTIAL |
| Source Frameworks | OWASP LLM03 (Supply Chain), NIST SA-12 (Supply Chain Protection), NIST CM-5 (Access Restrictions for Change), NIST SI-7 (Software Integrity) |
| Acceptance Criteria | (1) Skill invocation validates SKILL.md presence and format at L3. (2) Unregistered skills (not in CLAUDE.md) cannot be invoked. (3) Git status check detects uncommitted modifications to skill files. (4) Modified skills require explicit user approval before invocation. |
| Parent Risk IDs | R-SC-003 (Skill/agent definition tampering, RPN 160), R-SC-006 (L2-REINJECT marker tampering, RPN 90) |
| Jerry Mapping | H-25/H-26 (skill standards), CLAUDE.md skill registry, AGENTS.md agent registry, L3/L5 enforcement |
| Phase 2 Architecture Decision | Decision 2 (MCP Supply Chain Verification) |

### FR-SEC-028

| Field | Value |
|-------|-------|
| ID | FR-SEC-028 |
| Title | Python Dependency Supply Chain Security |
| Priority | MEDIUM |
| Description | The system SHALL verify Python dependencies managed through UV for known vulnerabilities and integrity. The system SHALL: (a) use lock files for reproducible builds, (b) verify dependency checksums, (c) scan for known CVEs in dependencies, (d) enforce UV-only installation (H-05). |
| Rationale | Python dependency poisoning (R-SC-002, RPN 378) is a well-established attack vector. UV's lock file provides reproducibility but not vulnerability scanning. H-05 enforcement prevents pip usage but does not verify the integrity of UV-resolved packages. |
| Current Jerry Coverage | H-05 UV-only enforcement for Python. `uv.lock` committed for reproducible builds. Git version control. No dependency vulnerability scanning. No CVE checking in CI. |
| Gap Status | PARTIAL |
| Source Frameworks | OWASP LLM03 (Supply Chain), NIST SA-12 (Supply Chain Protection), NIST SI-2 (Flaw Remediation), MITRE ATT&CK T1195 (Supply Chain Compromise) |
| Acceptance Criteria | (1) `uv.lock` file is committed and used for all dependency resolution. (2) L5 CI includes dependency vulnerability scanning. (3) Dependencies with known CRITICAL CVEs block CI. (4) Direct pip/python usage is blocked per H-05 enforcement. |
| Parent Risk IDs | R-SC-002 (Dependency poisoning, RPN 378), R-SC-005 (Model supply chain, RPN 180) |
| Jerry Mapping | H-05 (UV-only), pyproject.toml, L5 CI verification, python-environment.md |
| Phase 2 Architecture Decision | Decision 2 (MCP Supply Chain Verification) |

---

## Category 7: Audit and Logging

### FR-SEC-029

| Field | Value |
|-------|-------|
| ID | FR-SEC-029 |
| Title | Comprehensive Agent Action Audit Trail |
| Priority | CRITICAL |
| Description | The system SHALL maintain a comprehensive audit trail of all agent actions including: (a) every tool invocation with parameters and results summary, (b) every handoff with full metadata, (c) every routing decision with method and confidence, (d) every security event (blocked actions, detected injections, policy violations), (e) agent lifecycle events (creation, execution, termination). |
| Rationale | Comprehensive audit is the #5 critical gap with aggregate RPN 765. Without it, attacks cannot be detected post-hoc, forensic analysis is impossible, and incident response (FR-SEC-033 through FR-SEC-036) has no data to work with. OWASP ASI-09, Cisco State of AI Security 2026, and NIST 800-53 AU family all identify insufficient logging as a top-10 agentic risk. Current routing observability (RT-M-008) covers only routing decisions, not the full action spectrum. |
| Current Jerry Coverage | Routing observability (RT-M-008) captures routing decisions. Worktracker entries provide session-level tracking. Orchestration state tracks workflow progress. No unified audit trail covering all agent actions, tool invocations, and security events. |
| Gap Status | PARTIAL |
| Source Frameworks | OWASP ASI-09 (Insufficient Logging and Monitoring), NIST AU-2 (Event Logging), NIST AU-3 (Content of Audit Records), NIST AU-12 (Audit Record Generation) |
| Acceptance Criteria | (1) Every tool invocation produces an audit log entry with: timestamp, agent ID, tool name, parameters hash, result status, duration. (2) Every handoff produces an audit log entry with: from_agent, to_agent, criticality, confidence, artifact list. (3) Security events are logged with: event type, severity, agent ID, full context, recommended action. (4) Audit logs are append-only and tamper-evident. |
| Parent Risk IDs | R-DE-002 (System prompt exposure), R-AM-004 (Rogue agent behavior), R-GB-002 (Quality gate manipulation) |
| Jerry Mapping | Routing observability (RT-M-008), worktracker entries, orchestration state tracking, L4 post-tool inspection |
| Phase 2 Architecture Decision | Decision 8 (Comprehensive Audit Trail) |

### FR-SEC-030

| Field | Value |
|-------|-------|
| ID | FR-SEC-030 |
| Title | Security Event Logging |
| Priority | HIGH |
| Description | The system SHALL log security-specific events at a higher detail level than operational events. Security events SHALL include: (a) prompt injection detection (direct and indirect), (b) tool access violations, (c) forbidden action attempts, (d) authentication failures, (e) privilege escalation attempts, (f) circuit breaker activations, (g) anomalous agent behavior patterns, (h) MCP server communication anomalies. |
| Rationale | Security events require higher fidelity logging than operational events to enable forensic reconstruction and pattern detection. Generic operational logs lack the context needed for security incident investigation. Distinguishing security events from operational events enables prioritized monitoring and alerting. |
| Current Jerry Coverage | L3/L4 enforcement layers generate implicit security events (blocked actions, AE-006 escalation, circuit breaker activation). No formal security event categorization. No severity classification for security events. No unified security event log. |
| Gap Status | PARTIAL |
| Source Frameworks | OWASP ASI-09, NIST AU-6 (Audit Record Review, Analysis, and Reporting), NIST SI-4 (System Monitoring), NIST IR-5 (Incident Monitoring) |
| Acceptance Criteria | (1) Security events are categorized by severity: CRITICAL, HIGH, MEDIUM, LOW. (2) CRITICAL security events trigger immediate user notification. (3) Security event logs include sufficient context for forensic reconstruction. (4) Security events are distinguishable from operational events in log output. |
| Parent Risk IDs | R-GB-001 (Constitutional circumvention), R-AM-004 (Rogue agent behavior), R-IC-001 (Trust boundary exploitation) |
| Jerry Mapping | L3/L4 enforcement layers (security event sources), AE-006 graduated escalation, circuit breaker (H-36), P-022 (no deception -- inform user) |
| Phase 2 Architecture Decision | Decision 8 (Comprehensive Audit Trail) |

### FR-SEC-031

| Field | Value |
|-------|-------|
| ID | FR-SEC-031 |
| Title | Anomaly Detection Triggers |
| Priority | MEDIUM |
| Description | The system SHALL define and monitor anomaly detection triggers for agent behavior including: (a) unusual tool invocation frequency (> 3 standard deviations from baseline), (b) unexpected tool combinations not declared in agent definition, (c) output volume anomalies (token count > 2x expected), (d) repeated failed operations (> 3 consecutive failures), (e) context fill rate anomalies (filling faster than expected for task type). |
| Rationale | Anomaly detection is a defense-in-depth mechanism that catches attacks bypassing deterministic controls. ATLAS AML.T0054 documents behavior analysis evasion techniques, meaning anomaly detection must be sophisticated enough to detect evasive patterns. AE-006 context fill monitoring provides a partial baseline but covers only one of the five anomaly dimensions. |
| Current Jerry Coverage | AE-006 graduated escalation monitors context fill. Circuit breaker (H-36) limits routing hops. RT-M-011 through RT-M-015 define FMEA monitoring thresholds. No runtime anomaly detection implementation. Thresholds defined but not instrumented. |
| Gap Status | PARTIAL |
| Source Frameworks | OWASP ASI-09 (Insufficient Logging), OWASP ASI-10 (Rogue Agents), NIST SI-4 (System Monitoring), NIST AU-6 (Audit Review), ATLAS AML.T0054 (Anomalous Behavior Detection Evasion) |
| Acceptance Criteria | (1) Anomaly thresholds are configurable per agent type and task criticality. (2) Triggered anomalies produce security events at appropriate severity. (3) Anomaly detection operates continuously during agent execution (L4). (4) Baseline behavior profiles are established per agent type. |
| Parent Risk IDs | R-AM-004 (Rogue agent behavior), R-CF-005 (False negatives in security controls, RPN 405), R-PI-005 (Goal hijacking via progressive manipulation) |
| Jerry Mapping | L4 post-tool inspection, AE-006 context fill monitoring, circuit breaker (H-36), routing observability (RT-M-011 through RT-M-015) |
| Phase 2 Architecture Decision | Decision 8 (Comprehensive Audit Trail) |

### FR-SEC-032

| Field | Value |
|-------|-------|
| ID | FR-SEC-032 |
| Title | Audit Log Integrity Protection |
| Priority | MEDIUM |
| Description | The system SHALL protect audit logs from tampering, deletion, and unauthorized access. Audit logs SHALL be: (a) append-only during a session, (b) persisted to the filesystem in a protected location, (c) included in git tracking for immutability, (d) accessible only to authorized reviewers. |
| Rationale | Audit logs that can be modified are useless for forensic analysis and non-repudiation. NIST AU-9 specifically addresses protection of audit information. If a compromised agent can modify or delete its own audit trail, the comprehensive audit (FR-SEC-029) is undermined. Jerry's filesystem-as-memory architecture means audit logs are files, making file-level access control the primary integrity mechanism. |
| Current Jerry Coverage | Worktracker entries and orchestration artifacts are committed to git (immutable after commit). No session-level audit log protection (during active session, files are writable). No directory-level access restrictions for log files. |
| Gap Status | PARTIAL |
| Source Frameworks | OWASP ASI-09, NIST AU-9 (Protection of Audit Information), NIST AU-11 (Audit Record Retention), NIST AU-10 (Non-repudiation) |
| Acceptance Criteria | (1) Audit log files cannot be modified by agent tool invocations (Write/Edit tools restricted from log directories). (2) Audit logs are committed to git as part of session completion. (3) Log file permissions restrict write access to the logging subsystem only. (4) Log rotation preserves historical entries for configurable retention period. |
| Parent Risk IDs | R-GB-002 (Quality gate manipulation), R-DE-002 (System prompt exposure), R-AM-004 (Rogue agent behavior) |
| Jerry Mapping | Worktracker entries, orchestration artifacts, L5 CI (commit-time verification), file system permissions |
| Phase 2 Architecture Decision | Decision 8 (Comprehensive Audit Trail) |

---

## Category 8: Incident Response

### FR-SEC-033

| Field | Value |
|-------|-------|
| ID | FR-SEC-033 |
| Title | Agent Containment Mechanism |
| Priority | CRITICAL |
| Description | The system SHALL provide an agent containment mechanism that can immediately halt a compromised or misbehaving agent. Containment SHALL: (a) terminate the agent's tool access, (b) preserve the agent's current state for forensic analysis, (c) prevent the agent from completing pending operations, (d) notify the user of the containment action and reason. |
| Rationale | Containment is the first response to a detected security incident. Without it, a compromised agent continues operating while the incident is investigated. The circuit breaker (H-36) provides the architectural mechanism but is currently scoped to routing loops, not security events. Extending containment to security events (per FR-SEC-030 triggers) creates a unified incident response capability. |
| Current Jerry Coverage | Circuit breaker (H-36) halts routing at 3 hops. P-020 allows user to manually halt agents. AE-006 emergency escalation provides checkpoint + warn behavior. No security-event-triggered containment. No forensic snapshot capability. |
| Gap Status | PARTIAL |
| Source Frameworks | OWASP ASI-10 (Rogue Agents), OWASP ASI-08 (Cascading Failures), NIST IR-4 (Incident Handling), NIST IR-6 (Incident Reporting), NIST SC-24 (Fail in Known State) |
| Acceptance Criteria | (1) Circuit breaker activation (H-36) triggers agent containment. (2) User can manually trigger containment at any time (P-020). (3) Contained agent's state is preserved in a forensic snapshot. (4) Containment prevents cascading to downstream agents. (5) Containment notification includes: agent ID, reason, recommended next action. |
| Parent Risk IDs | R-AM-004 (Rogue agent behavior), R-CF-001 (Unbounded agent spawning), R-GB-001 (Constitutional circumvention) |
| Jerry Mapping | Circuit breaker (H-36), P-020 (user authority), AE-006 emergency escalation, Task tool termination, P-022 (inform user) |
| Phase 2 Architecture Decision | Decision 10 (Incident Response Framework) |

### FR-SEC-034

| Field | Value |
|-------|-------|
| ID | FR-SEC-034 |
| Title | Cascading Failure Prevention |
| Priority | HIGH |
| Description | The system SHALL prevent cascading failures across agent pipelines. When one agent fails, the system SHALL: (a) contain the failure to the failing agent's scope, (b) prevent error propagation through handoff chains, (c) notify upstream orchestrators of the failure, (d) provide partial results where possible. |
| Rationale | Cascading failures are a compound threat where one agent's failure degrades or compromises downstream agents. The FMEA Category 9 (Cascading Failures, average RPN 252) documents six failure modes in this category. The multi_skill_context failure_propagation pattern addresses this architecturally but is not enforced. |
| Current Jerry Coverage | Multi-skill combination failure propagation defined in agent-routing-standards.md. Handoff protocol blockers field captures known impediments. Guardrails fallback_behavior provides per-agent failure modes. No enforcement of failure containment at L3/L4. |
| Gap Status | PARTIAL |
| Source Frameworks | OWASP ASI-08 (Cascading Failures), NIST SC-24 (Fail in Known State), NIST CP-12 (Safe Mode), NIST SI-17 (Fail-Safe Procedures) |
| Acceptance Criteria | (1) Agent failure produces a structured failure report (not unstructured error). (2) Orchestrator receives failure notification with: failed agent ID, failure type, partial results (if any), remediation suggestions. (3) Downstream agents in the pipeline are not invoked after upstream failure unless orchestrator explicitly decides to proceed with partial results. (4) Failure propagation follows the multi_skill_context failure_propagation pattern. |
| Parent Risk IDs | R-CF-003 (Error propagation through handoff chains), R-CF-004 (Quality degradation through iterations), R-CF-001 (Unbounded agent spawning) |
| Jerry Mapping | Multi-skill combination failure propagation, handoff protocol blockers field, guardrails.fallback_behavior, orchestration state tracking |
| Phase 2 Architecture Decision | Decision 10 (Incident Response Framework) |

### FR-SEC-035

| Field | Value |
|-------|-------|
| ID | FR-SEC-035 |
| Title | Graceful Degradation Under Security Events |
| Priority | HIGH |
| Description | The system SHALL degrade gracefully when security events are detected rather than failing completely. Graceful degradation levels SHALL include: (a) RESTRICT: reduce agent permissions to T1 (read-only) and continue, (b) CHECKPOINT: save state and pause for user review, (c) CONTAIN: terminate agent and preserve state, (d) HALT: stop all agent activity and report to user. |
| Rationale | Binary security responses (allow/deny) are insufficient for agentic systems where partial progress has value. The AE-006 graduated escalation already implements a graduated response for context fill; extending this pattern to security events provides proportional response. Anthropic's Claude Code permission model demonstrates that proportional security reduces friction by 84% while maintaining protection. |
| Current Jerry Coverage | AE-006 graduated escalation (NOMINAL -> WARNING -> CRITICAL -> EMERGENCY -> COMPACTION). Guardrails fallback_behavior (warn_and_retry, escalate_to_user, persist_and_halt). P-020 user authority for override. No security-event-specific degradation levels. |
| Gap Status | PARTIAL |
| Source Frameworks | OWASP ASI-08 (Cascading Failures), NIST CP-2 (Contingency Plan), NIST SC-24 (Fail in Known State), NIST IR-4 (Incident Handling) |
| Acceptance Criteria | (1) Degradation level is proportional to security event severity. (2) RESTRICT mode is the default response for MEDIUM security events. (3) CHECKPOINT mode activates for HIGH security events. (4) CONTAIN/HALT modes activate for CRITICAL security events. (5) User is informed of degradation level and can override (P-020). |
| Parent Risk IDs | R-CF-005 (False negatives in security controls, RPN 405), R-GB-001 (Constitutional circumvention, RPN 432), R-CF-002 (Cascading quality degradation) |
| Jerry Mapping | AE-006 graduated escalation, guardrails.fallback_behavior (warn_and_retry, escalate_to_user, persist_and_halt), P-020 user authority, L4 enforcement |
| Phase 2 Architecture Decision | Decision 10 (Incident Response Framework) |

### FR-SEC-036

| Field | Value |
|-------|-------|
| ID | FR-SEC-036 |
| Title | Recovery Procedures After Security Incidents |
| Priority | MEDIUM |
| Description | The system SHALL provide recovery procedures following security incidents including: (a) session state restoration from last known good checkpoint, (b) agent definition re-validation after compromise, (c) MCP server re-verification after supply chain events, (d) audit log review guidance for forensic analysis, (e) user notification with incident summary and recommended actions. |
| Rationale | Recovery completes the incident response lifecycle (Detect -> Contain -> Recover). Without recovery procedures, post-incident state is uncertain and the system may remain in a degraded or compromised state. NIST CSF Recover function and IR-4 both require documented recovery procedures. |
| Current Jerry Coverage | Memory-Keeper checkpoints (context_checkpoint). AE-006e compaction recovery. Agent definition validation via H-34/H-35. No integrated recovery workflow. No incident summary generation. |
| Gap Status | PARTIAL |
| Source Frameworks | NIST IR-4 (Incident Handling), NIST CP-10 (System Recovery and Reconstitution), NIST IR-8 (Incident Response Plan), NIST CSF Recover function |
| Acceptance Criteria | (1) Checkpoint restore capability exists for session state (context_checkpoint). (2) Post-incident agent re-validation executes full H-34/H-35 schema checks. (3) Post-incident MCP re-verification executes full FR-SEC-025 checks. (4) Incident summary report is generated with: timeline, affected agents, affected tools, recommended remediation. (5) Recovery does not require full system restart. |
| Parent Risk IDs | R-CF-006 (Context rot after compaction), R-SC-001 (Malicious MCP server packages), R-AM-004 (Rogue agent behavior) |
| Jerry Mapping | Memory-Keeper checkpoints, AE-006e (compaction recovery), agent definition validation, MCP server verification, session management |
| Phase 2 Architecture Decision | Decision 10 (Incident Response Framework) |

---

## Category 9: Additional Functional Requirements

### FR-SEC-037

| Field | Value |
|-------|-------|
| ID | FR-SEC-037 |
| Title | Rogue Agent Detection |
| Priority | CRITICAL |
| Description | The system SHALL detect rogue agent behavior defined as: (a) agent producing output that contradicts its constitutional constraints, (b) agent attempting actions outside its declared capabilities, (c) agent exhibiting behavioral drift from its defined methodology, (d) agent producing deceptive output (violating P-022). Detection SHALL combine L3 deterministic checks and L4 behavioral analysis. |
| Rationale | Rogue agents are the terminal threat in agentic systems -- an agent that has been compromised but continues to operate within the system. OWASP ASI-10 specifically addresses this threat. The gap analysis shows ASI-10 at PARTIAL coverage: constitutional constraints provide behavioral guidance, but no runtime behavioral anomaly detection or drift monitoring exists. L3 deterministic checks catch out-of-scope tool access; L4 behavioral analysis catches subtler deviations. |
| Current Jerry Coverage | Constitutional triplet (P-003, P-020, P-022) in every agent per H-35. L2 re-injection of constitutional constraints. H-34 schema validation. No runtime behavioral anomaly detection. No behavioral drift monitoring. No methodology compliance checking. |
| Gap Status | PARTIAL |
| Source Frameworks | OWASP ASI-10 (Rogue Agents), ATLAS AML.T0054 (Behavior Analysis Evasion), NIST SI-4 (System Monitoring), NIST AU-6 (Audit Review) |
| Acceptance Criteria | (1) L3 checks prevent out-of-scope tool invocations (deterministic). (2) L4 inspects agent output for constitutional constraint violations. (3) Behavioral drift detection compares agent actions against its methodology section. (4) Detected rogue behavior triggers immediate containment (FR-SEC-033). (5) False positive rate for rogue detection <= 2%. |
| Parent Risk IDs | R-AM-004 (Rogue agent behavior), R-GB-001 (Constitutional circumvention, RPN 432), R-PI-005 (Goal hijacking via progressive manipulation) |
| Jerry Mapping | Constitutional constraints (P-003, P-020, P-022), L3/L4 enforcement, agent definition methodology, circuit breaker (H-36), forbidden actions |
| Phase 2 Architecture Decision | Decision 3 (L3 Security Gate Extension), Decision 5 (L4 Output Security Gate) |

### FR-SEC-038

| Field | Value |
|-------|-------|
| ID | FR-SEC-038 |
| Title | Human-in-the-Loop for High-Impact Actions |
| Priority | CRITICAL |
| Description | The system SHALL require human-in-the-loop (HITL) approval for high-impact actions including: (a) any action classified as C3+ criticality, (b) file system modifications outside the project workspace, (c) external network requests to unregistered domains, (d) agent-generated code execution, (e) MCP server configuration changes, (f) governance file modifications (AE-002, AE-004). |
| Rationale | HITL is the ultimate control mechanism and the foundation of P-020 (user authority). The Anthropic GTG-1002 incident demonstrated that automated agent actions without HITL approval can escalate rapidly. OWASP ASI-09 identifies human-agent trust exploitation as a top-10 threat -- maintaining clear HITL boundaries prevents the system from accumulating unchecked authority. |
| Current Jerry Coverage | P-020 user authority principle. Auto-escalation rules AE-001 through AE-005. Criticality levels C1-C4. H-31 clarify when ambiguous. No formalized HITL trigger list. No timeout-to-denial default. |
| Gap Status | PARTIAL |
| Source Frameworks | OWASP ASI-02 (Tool Misuse), OWASP ASI-09 (Human-Agent Trust Exploitation), P-020 (User Authority), NIST AC-6(2) (Non-privileged Access for Non-security Functions), Anthropic GTG-1002 lessons |
| Acceptance Criteria | (1) High-impact action list is configurable and extensible. (2) HITL approval request includes: action description, risk assessment, agent ID, alternatives considered. (3) Timeout on HITL approval defaults to action denial (fail-closed). (4) HITL decisions are logged in the audit trail. (5) Auto-escalation rules (AE-001 through AE-005) trigger HITL for governance changes. |
| Parent Risk IDs | R-PE-003 (Permission boundary escape via Bash), R-GB-001 (Constitutional circumvention), R-AM-002 (Tool misuse) |
| Jerry Mapping | P-020 (user authority), auto-escalation rules (AE-001 through AE-006), criticality levels (C1-C4), H-31 (clarify when ambiguous) |
| Phase 2 Architecture Decision | Decision 3 (L3 Security Gate Extension) |

### FR-SEC-039

| Field | Value |
|-------|-------|
| ID | FR-SEC-039 |
| Title | Recursive Delegation Prevention |
| Priority | CRITICAL |
| Description | The system SHALL enforce the single-level nesting constraint (P-003/H-01) to prevent recursive agent delegation. Worker agents SHALL NOT have the Task tool in their allowed_tools. The system SHALL detect and block attempts to create delegation chains deeper than 1 level (orchestrator -> worker). |
| Rationale | Recursive delegation is the most dangerous topology violation because it creates uncontrolled agent proliferation, exponential error amplification (17x for uncoordinated topologies per Google DeepMind), and accountability loss. P-003 is the strongest topological defense in any agentic framework reviewed. The FMEA risk R-PE-002 (P-003 nesting violation, RPN 54) has a low RPN precisely because P-003 + H-35 + L2 re-injection provide strong existing controls. This requirement formalizes adding L3 deterministic enforcement to make the defense complete. |
| Current Jerry Coverage | H-01/P-003 HARD rule (no recursive subagents). H-35 requires workers exclude Task from allowed_tools. L2 re-injects P-003 every prompt. L5 CI validates agent definitions. No L3 runtime enforcement of delegation depth. |
| Gap Status | PARTIAL (strong existing controls, needs L3 deterministic gate) |
| Source Frameworks | OWASP ASI-03 (Privilege Escalation via delegation), OWASP ASI-08 (Cascading Failures), P-003 (No Recursive Subagents), NIST AC-6 (Least Privilege) |
| Acceptance Criteria | (1) Worker agent definitions with Task in allowed_tools are rejected at L5 CI. (2) L3 blocks Task tool invocation from within a Task-invoked context. (3) Delegation depth counter is tracked and enforced at maximum 1. (4) Recursive delegation attempts are logged as CRITICAL security events. |
| Parent Risk IDs | R-PE-002 (P-003 nesting violation, RPN 54), R-CF-001 (Unbounded agent spawning), R-PE-004 (Privilege accumulation) |
| Jerry Mapping | H-01/P-003 (no recursive subagents), H-35 (worker agents no Task tool), L3 pre-tool gating, L5 CI verification, tool tier T5 restriction |
| Phase 2 Architecture Decision | Decision 3 (L3 Security Gate Extension) |

### FR-SEC-040

| Field | Value |
|-------|-------|
| ID | FR-SEC-040 |
| Title | Unbounded Consumption Prevention |
| Priority | HIGH |
| Description | The system SHALL prevent unbounded resource consumption by agents including: (a) token consumption limits per agent invocation (configurable by criticality), (b) tool invocation count limits per agent (configurable), (c) execution time limits per agent, (d) output size limits per agent response. The system SHALL enforce graduated escalation per AE-006 for context fill. |
| Rationale | Unbounded consumption is both a denial-of-service attack and a cost amplification attack. The gap analysis shows OWASP LLM10 (Unbounded Consumption) as one of the few COVERED items because AE-006, H-36, and RT-M-010 provide multiple independent controls. This requirement formalizes the existing controls and extends them with per-agent resource limits not currently configurable. |
| Current Jerry Coverage | AE-006 graduated escalation (context fill thresholds at 0.70/0.80/0.88). H-36 circuit breaker (3 hop maximum). RT-M-010 iteration ceilings (C1=3, C2=5, C3=7, C4=10). CB-01 through CB-05 context budget standards. No per-agent token, tool invocation, or time limits. |
| Gap Status | PARTIAL |
| Source Frameworks | OWASP LLM10 (Unbounded Consumption), OWASP ASI-08 (Cascading Failures), NIST SC-5 (Denial of Service Protection), NIST SC-6 (Resource Availability) |
| Acceptance Criteria | (1) Per-agent resource limits are configurable in agent definitions or orchestration plans. (2) AE-006 graduated escalation activates at context fill thresholds (0.70/0.80/0.88). (3) Circuit breaker (H-36) limits routing hops to 3. (4) Iteration ceilings are enforced per criticality (C1=3, C2=5, C3=7, C4=10 per RT-M-010). (5) Resource exhaustion triggers graceful degradation (FR-SEC-035). |
| Parent Risk IDs | R-CF-001 (Unbounded agent spawning), R-CF-005 (False negatives in security controls, RPN 405), R-CF-006 (Context rot after compaction) |
| Jerry Mapping | AE-006 graduated escalation, circuit breaker (H-36), iteration ceilings (RT-M-010), context budget standards (CB-01 through CB-05) |
| Phase 2 Architecture Decision | Decision 3 (L3 Security Gate Extension) |

### FR-SEC-041

| Field | Value |
|-------|-------|
| ID | FR-SEC-041 |
| Title | Secure Configuration Management |
| Priority | HIGH |
| Description | The system SHALL enforce secure configuration management for all security-relevant settings including: (a) HARD rules in quality-enforcement.md, (b) agent definitions in skills/*/agents/*.md, (c) MCP server configuration in .claude/settings.local.json, (d) tool tier mappings, (e) toxic combination registries. Configuration changes to security-relevant files SHALL trigger auto-escalation (AE-002 for rules, AE-004 for baselined ADRs). |
| Rationale | Security configuration is the control plane for all other security requirements. If configuration can be modified without detection or review, all downstream security controls are undermined. NIST CM-2 through CM-7 comprehensively address configuration management. Jerry's auto-escalation rules (AE-001 through AE-005) provide the policy framework but not the detection mechanism for unauthorized changes during active sessions. |
| Current Jerry Coverage | Auto-escalation rules AE-001 through AE-005 define escalation triggers. Git version control tracks all configuration changes. L5 CI validates configuration files. No runtime configuration drift detection during active sessions. |
| Gap Status | PARTIAL |
| Source Frameworks | NIST CM-2 (Baseline Configuration), NIST CM-3 (Configuration Change Control), NIST CM-6 (Configuration Settings), NIST CM-7 (Least Functionality) |
| Acceptance Criteria | (1) Security configuration files are tracked by git with change detection. (2) Changes to .context/rules/ trigger auto-C3 (AE-002). (3) Changes to constitution trigger auto-C4 (AE-001). (4) L5 CI validates all configuration files against their schemas on every commit. (5) Configuration drift detection alerts on unauthorized modifications. |
| Parent Risk IDs | R-SC-003 (Skill/agent definition tampering, RPN 160), R-SC-006 (L2-REINJECT marker tampering, RPN 90), R-GB-001 (Constitutional circumvention) |
| Jerry Mapping | AE-001 through AE-005 (auto-escalation), L5 CI verification, .context/rules/ governance, CLAUDE.md, quality-enforcement.md |
| Phase 2 Architecture Decision | Decision 2 (MCP Supply Chain Verification) |

### FR-SEC-042

| Field | Value |
|-------|-------|
| ID | FR-SEC-042 |
| Title | Secure Defaults for New Agents and Skills |
| Priority | MEDIUM |
| Description | The system SHALL enforce secure-by-default configuration for newly created agents and skills. Defaults SHALL include: (a) T1 (read-only) tool tier unless explicitly escalated with justification, (b) constitutional triplet (P-003, P-020, P-022) pre-populated in new agent templates, (c) minimum 3 forbidden actions pre-populated, (d) fallback_behavior defaulting to escalate_to_user, (e) input_validation and output_filtering minimum entries pre-populated. |
| Rationale | Secure defaults prevent the creation of overprivileged agents through developer oversight. NIST CM-7 (Least Functionality) and OWASP ASI-03 (Privilege Escalation -- default permissions) both emphasize that defaults should be restrictive. The existing guardrails template in agent-development-standards.md provides guidance but not enforcement -- new agents can omit security fields without CI failure. |
| Current Jerry Coverage | Guardrails template documented in agent-development-standards.md. Agent definition schema (H-34) requires security fields. Constitutional triplet requirement (H-35). Agent templates in .context/templates/ (existence varies). No enforcement that new agents use secure defaults. |
| Gap Status | PARTIAL |
| Source Frameworks | OWASP ASI-03 (Privilege Escalation -- default permissions), NIST CM-7 (Least Functionality), NIST SA-8 (Security and Privacy Engineering Principles) |
| Acceptance Criteria | (1) Agent template includes all H-34 required fields with secure defaults. (2) New agents created without explicit tier justification default to T1. (3) Template enforcement is verified at L5 CI. (4) Documentation clearly states the secure defaults and escalation procedure. |
| Parent Risk IDs | R-PE-001 (Tool tier bypass), R-AM-002 (Tool misuse), R-SC-003 (Skill/agent definition tampering) |
| Jerry Mapping | Agent definition schema (H-34), guardrails template, .context/templates/, skill standards (H-25/H-26), agent-development-standards.md |
| Phase 2 Architecture Decision | Decision 2 (MCP Supply Chain Verification) |

---

## Category 10: Performance

### NFR-SEC-001

| Field | Value |
|-------|-------|
| ID | NFR-SEC-001 |
| Title | Security Control Latency Budget |
| Priority | HIGH |
| Description | Security controls at L3 (pre-tool gating) SHALL NOT add more than 50ms latency per tool invocation. Security controls at L4 (post-tool inspection) SHALL NOT add more than 200ms latency per tool result processing. Total security overhead per agent turn SHALL NOT exceed 500ms. |
| Rationale | Security controls that degrade performance become candidates for bypass. The 50ms/200ms/500ms budgets ensure security overhead is imperceptible to the user. L3 gates are tighter because they execute synchronously before every tool call. |
| Current Jerry Coverage | No security-specific gates to benchmark. L2 re-injection adds ~850 tokens per prompt (token cost, not latency). |
| Gap Status | NO COVERAGE (no security controls to measure) |
| Source Frameworks | NIST SC-5 (Denial of Service Protection), OWASP API4:2023 (Unrestricted Resource Consumption) |
| Acceptance Criteria | (1) L3 gate average latency < 50ms measured across 100 consecutive invocations. (2) L4 inspection average latency < 200ms. (3) End-to-end security overhead < 500ms per agent turn. (4) Performance benchmarks are run as part of L5 CI. |
| Parent Risk IDs | R-CF-005 (False negatives in security controls, RPN 405) |
| Jerry Mapping | L3 pre-tool gating, L4 post-tool inspection, enforcement architecture token budgets |
| Phase 2 Architecture Decision | Decision 3 (L3 Security Gate Extension), Decision 5 (L4 Output Security Gate) |

### NFR-SEC-002

| Field | Value |
|-------|-------|
| ID | NFR-SEC-002 |
| Title | Security Token Budget |
| Priority | HIGH |
| Description | Security enforcement mechanisms SHALL NOT consume more than 10% of the total context window (20,000 tokens of 200K). This includes L2 re-injection tokens (~850/prompt), security-related system instructions, and security metadata in handoffs. |
| Rationale | Token consumption directly competes with productive agent work. Current enforcement uses ~15,350 tokens (7.7% of 200K). Security extensions must fit within the remaining 2.3% budget to maintain the 10% ceiling. |
| Current Jerry Coverage | L2 re-injection within 850-token budget (559/850 used). Total enforcement ~15,350 tokens. No security-specific token budget tracking. |
| Gap Status | PARTIAL |
| Source Frameworks | Context budget standards (CB-01 through CB-05), OWASP LLM10 (Unbounded Consumption) |
| Acceptance Criteria | (1) L2 re-injection stays within 850-token budget. (2) Security metadata in handoffs < 500 tokens per handoff. (3) Total security token consumption is auditable. (4) Security token consumption does not trigger AE-006 escalation under normal operation. |
| Parent Risk IDs | R-CF-006 (Context rot after compaction), R-GB-001 (Constitutional circumvention via context rot) |
| Jerry Mapping | Enforcement architecture (L1-L5 token budgets), context budget standards, AE-006 graduated escalation |
| Phase 2 Architecture Decision | Decision 1 (Tool-Output Firewall) |

### NFR-SEC-003

| Field | Value |
|-------|-------|
| ID | NFR-SEC-003 |
| Title | Deterministic Security Control Performance |
| Priority | MEDIUM |
| Description | Deterministic security controls (L3 pre-tool gating, L5 CI) SHALL have constant-time performance characteristics (O(1) or O(n) where n is the control list size). Security controls SHALL NOT have performance degradation correlated with context fill level. |
| Rationale | Context-rot immunity is a fundamental property of L3 and L5 enforcement layers. Security controls added to these layers must preserve this property. |
| Current Jerry Coverage | L3 and L5 documented as context-rot immune. No security-specific controls to verify against. |
| Gap Status | NO COVERAGE (no security controls to measure) |
| Source Frameworks | L3/L5 enforcement architecture (context-rot immune), NIST SC-5 (Denial of Service Protection) |
| Acceptance Criteria | (1) L3 gate performance is independent of context fill level. (2) L5 CI execution time scales linearly with file count. (3) No security control exhibits exponential time complexity. |
| Parent Risk IDs | R-GB-001 (Constitutional circumvention via context rot, RPN 432) |
| Jerry Mapping | Enforcement architecture (L3 immune, L5 immune per quality-enforcement.md) |
| Phase 2 Architecture Decision | Decision 3 (L3 Security Gate Extension) |

---

## Category 11: Availability

### NFR-SEC-004

| Field | Value |
|-------|-------|
| ID | NFR-SEC-004 |
| Title | Security Subsystem Independence |
| Priority | HIGH |
| Description | Each enforcement layer (L1-L5) SHALL operate independently such that failure of one layer does not disable other layers. No single security control SHALL be a single point of failure. |
| Rationale | Defense-in-depth requires layer independence. The joint OpenAI/Anthropic/Google DeepMind study demonstrated any single defense can be bypassed at >90%. Jerry's architecture provides independent layers by design; this requirement formalizes the independence property. |
| Current Jerry Coverage | 5-layer enforcement architecture with documented independence. No formal independence testing between layers. |
| Gap Status | PARTIAL |
| Source Frameworks | NIST CP-2 (Contingency Plan), NIST SC-24 (Fail in Known State), Defense-in-depth principle |
| Acceptance Criteria | (1) Each enforcement layer can be independently tested. (2) Layer failure is detectable and logged. (3) System operates with degraded security rather than complete failure. (4) At least 2 enforcement layers remain active for any single layer failure. |
| Parent Risk IDs | R-CF-005 (False negatives, RPN 405), R-GB-001 (Constitutional circumvention, RPN 432) |
| Jerry Mapping | 5-layer enforcement architecture (L1-L5), defense-in-depth design, AE-006 graduated escalation |
| Phase 2 Architecture Decision | Decision 3 (L3 Security Gate Extension), Decision 5 (L4 Output Security Gate) |

### NFR-SEC-005

| Field | Value |
|-------|-------|
| ID | NFR-SEC-005 |
| Title | MCP Failure Resilience |
| Priority | HIGH |
| Description | The system SHALL continue to operate when MCP servers are unavailable. Security controls SHALL NOT depend on MCP availability. |
| Rationale | If security controls depend on MCP, an attacker can disable security by denying MCP access. Security must operate entirely within Jerry's local enforcement architecture (L1-L5). |
| Current Jerry Coverage | MCP error handling fallbacks defined in mcp-tool-standards.md. No explicit assertion that security controls are MCP-independent. |
| Gap Status | PARTIAL |
| Source Frameworks | NIST CP-2 (Contingency Plan), MCP tool standards error handling, OWASP ASI-08 (Cascading Failures) |
| Acceptance Criteria | (1) MCP unavailability detected within 5 seconds. (2) Fallback mechanisms activate automatically. (3) Security enforcement continues at full capability without MCP. (4) MCP recovery resumes normal operation without manual intervention. |
| Parent Risk IDs | R-SC-001 (Malicious MCP server packages), R-IF-003 (Network connectivity issues) |
| Jerry Mapping | MCP tool standards error handling, work/.mcp-fallback/, L3/L4 enforcement (independent of MCP) |
| Phase 2 Architecture Decision | Decision 2 (MCP Supply Chain Verification) |

### NFR-SEC-006

| Field | Value |
|-------|-------|
| ID | NFR-SEC-006 |
| Title | Fail-Closed Security Default |
| Priority | CRITICAL |
| Description | When security controls encounter an error or ambiguous state, the system SHALL fail closed (deny by default) rather than fail open. L3 gate errors SHALL block tool invocation. Authentication failures SHALL reject handoffs. Schema validation errors SHALL reject agent loading. HITL timeout SHALL deny the requested action. |
| Rationale | Fail-closed is the foundational security principle. Every other requirement assumes this behavior. If any checkpoint defaults to "allow" on error, it becomes a trivially exploitable bypass. |
| Current Jerry Coverage | Guardrails fallback_behavior includes escalate_to_user and persist_and_halt. No explicit fail-closed policy for L3 gate errors. No HITL timeout-to-denial default. |
| Gap Status | PARTIAL |
| Source Frameworks | NIST SC-24 (Fail in Known State), NIST AC-3 (Access Enforcement), OWASP Secure Design principles |
| Acceptance Criteria | (1) Every security checkpoint has a defined fail-closed behavior. (2) Fail-closed events are logged with full context. (3) User notified with explanation and remediation guidance. (4) No security control defaults to "allow" on error. |
| Parent Risk IDs | R-CF-005 (False negatives, RPN 405), R-GB-001 (Constitutional circumvention, RPN 432) |
| Jerry Mapping | L3 pre-tool gating, guardrails.fallback_behavior, P-020 (user authority for override), P-022 (transparency) |
| Phase 2 Architecture Decision | Decision 3 (L3 Security Gate Extension) |

---

## Category 12: Scalability

### NFR-SEC-007

| Field | Value |
|-------|-------|
| ID | NFR-SEC-007 |
| Title | Security Model Scalability with Agent Count |
| Priority | MEDIUM |
| Description | The security model SHALL scale to support up to 50 registered agents and 20 skills without degradation. Security control performance SHALL scale linearly (not exponentially) with agent and skill count. |
| Rationale | Jerry's scaling roadmap projects growth from 8 skills to 20+. Security controls must scale proportionally or become bottlenecks encouraging bypass. |
| Current Jerry Coverage | Scaling roadmap defined (Phases 0-3). L3/L5 designed for scalability. No security-specific scalability testing. |
| Gap Status | NO COVERAGE (no security controls to scale-test) |
| Source Frameworks | Agent routing standards scaling roadmap, NIST SA-8 (Security Engineering Principles) |
| Acceptance Criteria | (1) L3 gate performance scales linearly with agent count. (2) Routing accuracy >= 90% at 20 skills. (3) Tool tier enforcement O(1) per invocation. (4) CI validation scales linearly with agent file count. |
| Parent Risk IDs | R-CF-005 (False negatives in security controls) |
| Jerry Mapping | Agent routing scaling roadmap, L3/L5 enforcement, trigger map |
| Phase 2 Architecture Decision | Decision 3 (L3 Security Gate Extension) |

### NFR-SEC-008

| Field | Value |
|-------|-------|
| ID | NFR-SEC-008 |
| Title | Security Rule Set Scalability |
| Priority | MEDIUM |
| Description | The security rule set SHALL be scalable within the HARD rule ceiling (25 rules, absolute max 28). Security-specific HARD rules SHALL use compound formatting where possible. The L2 re-injection token budget (850 tokens) SHALL accommodate security rule markers. |
| Rationale | The 25-rule ceiling is derived from cognitive load, enforcement coverage, and governance burden convergence. Current budget: 25/25 rules, 559/850 L2 tokens. Security must work within these constraints. |
| Current Jerry Coverage | HARD Rule Index at ceiling (25/25). L2 budget at 559/850. Ceiling exception mechanism defined. Compound rule formatting established. |
| Gap Status | PARTIAL |
| Source Frameworks | HARD Rule Ceiling Derivation (quality-enforcement.md), L2 enforcement budget |
| Acceptance Criteria | (1) Security implementable within 25-rule ceiling. (2) Compound formatting for new security rules. (3) Security L2 markers < 200 tokens. (4) Ceiling Exception Mechanism used if expansion needed. |
| Parent Risk IDs | R-GB-001 (Constitutional circumvention via context rot, RPN 432) |
| Jerry Mapping | HARD Rule Index (25/25), L2 budget (559/850), Ceiling Exception Mechanism |
| Phase 2 Architecture Decision | N/A (governance constraint) |

---

## Category 13: Usability

### NFR-SEC-009

| Field | Value |
|-------|-------|
| ID | NFR-SEC-009 |
| Title | Minimal Security Friction for Routine Operations |
| Priority | HIGH |
| Description | Security controls SHALL NOT impede legitimate agent operations for C1 (Routine) tasks. HITL approvals SHALL only be required for C2+ operations or high-impact actions. Security UX SHALL be proportional to risk. |
| Rationale | Security that impedes productivity gets disabled. Anthropic's Claude Code achieved 84% prompt reduction with proportional controls. Jerry's criticality levels (C1-C4) provide the natural framework. |
| Current Jerry Coverage | Criticality levels C1-C4. P-020 user authority. H-31 proportional questioning. No explicit security friction budget per criticality. |
| Gap Status | PARTIAL |
| Source Frameworks | Anthropic Claude Code permission model, P-020 (User Authority), NIST PM-11 |
| Acceptance Criteria | (1) C1 tasks complete without HITL security prompts. (2) C2 tasks average <= 2 security prompts. (3) Security controls are transparent (visible when relevant). (4) Configurable security sensitivity (strict/standard/permissive). |
| Parent Risk IDs | R-GB-002 (Quality gate manipulation -- users bypass friction) |
| Jerry Mapping | Criticality levels (C1-C4), P-020, H-31, quality gate proportionality |
| Phase 2 Architecture Decision | Decision 3 (L3 Security Gate Extension) |

### NFR-SEC-010

| Field | Value |
|-------|-------|
| ID | NFR-SEC-010 |
| Title | Clear Security Event Communication |
| Priority | HIGH |
| Description | Security events, denials, and containment actions SHALL be communicated in clear, actionable language per P-022. Communications SHALL include: what happened, why blocked, what user can do, and severity level. |
| Rationale | Clear communication is the interface between security controls and user trust. If denials are opaque, users seek bypass. OWASP ASI-09 identifies clear communication as defense against trust exploitation. |
| Current Jerry Coverage | P-022 no deception. Circuit breaker includes user notification. AE-006 includes warnings. No standardized security message format. |
| Gap Status | PARTIAL |
| Source Frameworks | P-022 (No Deception), NIST IR-7, OWASP ASI-09 |
| Acceptance Criteria | (1) Every denial includes human-readable explanation. (2) Messages include recommended next action. (3) Consistent severity vocabulary (CRITICAL/HIGH/MEDIUM/LOW). (4) No opaque error codes without explanation. |
| Parent Risk IDs | R-GB-002 (Quality gate manipulation), R-AM-004 (Rogue agent behavior) |
| Jerry Mapping | P-022, circuit breaker (H-36 step 4), AE-006 user warnings, guardrails.fallback_behavior |
| Phase 2 Architecture Decision | Decision 10 (Incident Response Framework) |

---

## Category 14: Maintainability

### NFR-SEC-011

| Field | Value |
|-------|-------|
| ID | NFR-SEC-011 |
| Title | Security Rule Hot-Update Capability |
| Priority | MEDIUM |
| Description | Security rules, patterns, and configurations SHALL be updatable without full system restart. Prompt injection patterns loadable at L1, L2 rules updated via file modification, registries extensible via configuration files. |
| Rationale | Security threats evolve rapidly. Jerry's file-based rule system provides hot-update capability for behavioral rules; security rules should follow the same pattern. |
| Current Jerry Coverage | L1 session-start loading. L2 REINJECT markers as SSOT. Git-tracked rule files. No security-specific pattern databases. |
| Gap Status | PARTIAL |
| Source Frameworks | NIST CM-3, NIST SI-2, Google DeepMind Evolution layer |
| Acceptance Criteria | (1) Security updates take effect at next session start. (2) L2 markers are SSOT for per-prompt injection. (3) Configuration-driven controls in separate data files. (4) Update process documented and tested. |
| Parent Risk IDs | R-SC-006 (L2-REINJECT marker tampering), R-GB-001 (Constitutional circumvention) |
| Jerry Mapping | L1 session start, L2 re-injection, .context/rules/, git-tracked files |
| Phase 2 Architecture Decision | Decision 3 (L3 Security Gate Extension) |

### NFR-SEC-012

| Field | Value |
|-------|-------|
| ID | NFR-SEC-012 |
| Title | Security Control Testability |
| Priority | HIGH |
| Description | Every security control SHALL be independently testable. Test coverage >= 95% (exceeding standard 90% per H-20). Both positive tests (legitimate operations pass) and negative tests (attacks detected/blocked) required. |
| Rationale | Untestable security is unverifiable security. The 95% threshold reflects higher consequence of security failures. |
| Current Jerry Coverage | H-20 BDD test-first with 90% coverage. L5 CI test execution. /adversary for adversarial testing. No security-specific test suite. |
| Gap Status | PARTIAL |
| Source Frameworks | NIST CA-8 (Penetration Testing), NIST SA-11, H-20 |
| Acceptance Criteria | (1) Every L3 rule has positive and negative test cases. (2) Every L4 pattern has detection test cases. (3) Security coverage >= 95%. (4) Security tests in L5 CI. (5) Adversarial suite covers ASI-01 through ASI-10. |
| Parent Risk IDs | R-CF-005 (False negatives, RPN 405) |
| Jerry Mapping | H-20, L5 CI, /adversary skill, S-001 Red Team |
| Phase 2 Architecture Decision | N/A (testing infrastructure) |

### NFR-SEC-013

| Field | Value |
|-------|-------|
| ID | NFR-SEC-013 |
| Title | Security Architecture Documentation |
| Priority | MEDIUM |
| Description | Security architecture SHALL be documented with the same rigor as functional architecture: enforcement layer descriptions, security ADRs for C3+ decisions, configuration guide, threat model. |
| Rationale | Undocumented security cannot be audited or maintained. NIST PL-2 and CSF Govern require documentation. |
| Current Jerry Coverage | docs/design/ for ADRs. Quality gate (H-13). Criticality levels. /adversary for C4 review. No security-specific documentation standards. |
| Gap Status | PARTIAL |
| Source Frameworks | NIST PL-2, NIST SA-8, NIST CSF Govern |
| Acceptance Criteria | (1) Security ADRs for all C3+ decisions. (2) Threat model covers ASI-01 through ASI-10. (3) Configuration guide for all parameters. (4) Documentation passes C4 quality gate (>= 0.95). |
| Parent Risk IDs | R-GB-001 (Constitutional circumvention), R-GB-002 (Quality gate manipulation) |
| Jerry Mapping | docs/design/, quality gate (H-13), criticality levels, /adversary |
| Phase 2 Architecture Decision | N/A (documentation) |

### NFR-SEC-014

| Field | Value |
|-------|-------|
| ID | NFR-SEC-014 |
| Title | Security Compliance Traceability |
| Priority | HIGH |
| Description | Every implemented security control SHALL trace to at least one requirement. Every requirement SHALL trace to at least one source framework item. Bi-directional traceability SHALL be maintained. |
| Rationale | Traceability ensures no requirement is orphaned and no implementation is undocumented. NASA NPR 7123.1D requires bi-directional traceability for mission-critical systems. |
| Current Jerry Coverage | This baseline provides the traceability matrix. Phase 1 requirements include source framework references. No automated verification. |
| Gap Status | PARTIAL |
| Source Frameworks | NIST CA-2, NIST PL-2, NASA NPR 7123.1D |
| Acceptance Criteria | (1) Zero orphaned requirements. (2) Zero orphaned controls. (3) Every requirement traces to >= 1 framework. (4) RTM updated with every change. |
| Parent Risk IDs | R-GB-002 (Quality gate manipulation) |
| Jerry Mapping | This document (RTM section), WORKTRACKER.md, compliance matrices |
| Phase 2 Architecture Decision | N/A (traceability infrastructure) |

### NFR-SEC-015

| Field | Value |
|-------|-------|
| ID | NFR-SEC-015 |
| Title | Security Model Extensibility |
| Priority | MEDIUM |
| Description | Security model SHALL be extensible for new threats, tools, MCP servers, and capabilities without architectural changes. Extension points: pluggable validation patterns, extensible tiers, configurable thresholds, modular event handlers. |
| Rationale | The threat landscape evolves rapidly (OWASP Agentic Top 10 is 2026; ATLAS added 14 techniques in Oct 2025). A model requiring architectural changes per threat will fall behind. |
| Current Jerry Coverage | Defense-in-depth with layered enforcement. File-based rule system. Extensible MCP registry and agent schema. No pluggable security patterns. |
| Gap Status | PARTIAL |
| Source Frameworks | NIST SA-8, Google DeepMind Evolution layer, NIST CSF Govern |
| Acceptance Criteria | (1) New injection pattern = data file update only. (2) New tool tier = config change only. (3) New MCP server = registry update + verification. (4) Extension points documented with examples. |
| Parent Risk IDs | R-SC-004 (Context7 data poisoning), R-PI-006 (Injection via structured data) |
| Jerry Mapping | Defense-in-depth, .context/rules/, MCP registry, agent definition schema |
| Phase 2 Architecture Decision | Decision 3 (L3 Security Gate Extension) |

---

## Bi-Directional Traceability Matrix

### Forward Traceability: Requirement to Framework

| Req ID | Priority | MITRE | OWASP Agentic | OWASP LLM | NIST 800-53 | Gap Status |
|--------|----------|-------|---------------|-----------|-------------|------------|
| FR-SEC-001 | CRITICAL | -- | ASI-06 | -- | IA-4 | NO COVERAGE |
| FR-SEC-002 | CRITICAL | -- | ASI-06, ASI-07 | -- | IA-3, IA-9 | NO COVERAGE |
| FR-SEC-003 | HIGH | -- | ASI-06 | -- | IA-4, IA-5 | NO COVERAGE |
| FR-SEC-004 | HIGH | -- | ASI-06, ASI-09 | -- | AU-3, AU-10 | PARTIAL |
| FR-SEC-005 | CRITICAL | -- | ASI-02, ASI-03 | -- | AC-6, AC-3 | PARTIAL |
| FR-SEC-006 | CRITICAL | -- | ASI-02, ASI-03 | -- | AC-6, AC-5 | PARTIAL |
| FR-SEC-007 | CRITICAL | -- | ASI-02, ASI-10 | -- | AC-3, SI-10 | PARTIAL |
| FR-SEC-008 | CRITICAL | DCTs | ASI-03, ASI-04 | -- | AC-6(1) | PARTIAL |
| FR-SEC-009 | HIGH | AML.T0053 | ASI-02 | -- | AC-6(3) | NO COVERAGE |
| FR-SEC-010 | HIGH | -- | ASI-04 | -- | AC-4, SC-7 | PARTIAL |
| FR-SEC-011 | CRITICAL | AML.T0051 | ASI-01 | LLM01 | SI-10 | NO COVERAGE |
| FR-SEC-012 | CRITICAL | AML.T0051.001 | ASI-01, ASI-05 | LLM01 | SI-10 | NO COVERAGE |
| FR-SEC-013 | CRITICAL | AML.T0051 | ASI-01 | LLM03 | SC-7, SI-10 | NO COVERAGE |
| FR-SEC-014 | HIGH | AML.T0080 | ASI-05 | LLM10 | SI-7 | PARTIAL |
| FR-SEC-015 | HIGH | AML.T0051 | ASI-01 | -- | SI-7 | NO COVERAGE |
| FR-SEC-016 | MEDIUM | AML.T0051.002 | -- | LLM01 | SI-10 | NO COVERAGE |
| FR-SEC-017 | CRITICAL | AML.T0053 | -- | LLM02, LLM07 | SC-28, SI-15 | PARTIAL |
| FR-SEC-018 | HIGH | -- | ASI-08 | LLM05 | SI-15, SI-3 | PARTIAL |
| FR-SEC-019 | HIGH | -- | -- | LLM07 | SC-28, AC-3 | PARTIAL |
| FR-SEC-020 | MEDIUM | -- | -- | LLM09 | AI RMF | PARTIAL |
| FR-SEC-021 | HIGH | -- | ASI-07 | -- | SC-8, SI-10 | PARTIAL |
| FR-SEC-022 | HIGH | -- | ASI-04, ASI-07 | -- | AC-4, SC-7 | PARTIAL |
| FR-SEC-023 | MEDIUM | -- | ASI-07 | -- | SC-8, SC-13 | NO COVERAGE |
| FR-SEC-024 | HIGH | -- | ASI-07, ASI-10 | -- | IA-3, SC-23 | NO COVERAGE |
| FR-SEC-025 | CRITICAL | T1195 | ASI-04 | LLM03 | SA-12, SI-7 | NO COVERAGE |
| FR-SEC-026 | HIGH | -- | ASI-10 | LLM03 | SA-12, CM-3 | PARTIAL |
| FR-SEC-027 | HIGH | -- | -- | LLM03 | SA-12, CM-5 | PARTIAL |
| FR-SEC-028 | MEDIUM | T1195 | -- | LLM03 | SA-12, SI-2 | PARTIAL |
| FR-SEC-029 | CRITICAL | -- | ASI-09 | -- | AU-2, AU-3 | PARTIAL |
| FR-SEC-030 | HIGH | -- | ASI-09 | -- | AU-6, SI-4 | PARTIAL |
| FR-SEC-031 | MEDIUM | AML.T0054 | ASI-09, ASI-10 | -- | SI-4, AU-6 | PARTIAL |
| FR-SEC-032 | MEDIUM | -- | ASI-09 | -- | AU-9, AU-10 | PARTIAL |
| FR-SEC-033 | CRITICAL | -- | ASI-10, ASI-08 | -- | IR-4, SC-24 | PARTIAL |
| FR-SEC-034 | HIGH | -- | ASI-08 | -- | SC-24, CP-12 | PARTIAL |
| FR-SEC-035 | HIGH | -- | ASI-08 | -- | CP-2, SC-24 | PARTIAL |
| FR-SEC-036 | MEDIUM | -- | ASI-08 | -- | IR-4, CP-10 | PARTIAL |
| FR-SEC-037 | CRITICAL | AML.T0054 | ASI-10 | -- | SI-4, AU-6 | PARTIAL |
| FR-SEC-038 | CRITICAL | GTG-1002 | ASI-02, ASI-09 | -- | AC-6(2) | PARTIAL |
| FR-SEC-039 | CRITICAL | -- | ASI-03, ASI-08 | -- | AC-6 | PARTIAL |
| FR-SEC-040 | HIGH | -- | ASI-08 | LLM10 | SC-5, SC-6 | PARTIAL |
| FR-SEC-041 | HIGH | -- | -- | -- | CM-2, CM-3 | PARTIAL |
| FR-SEC-042 | MEDIUM | -- | ASI-03 | -- | CM-7, SA-8 | PARTIAL |
| NFR-SEC-001 | HIGH | -- | -- | API4 | SC-5 | NO COVERAGE |
| NFR-SEC-002 | HIGH | -- | -- | LLM10 | -- | PARTIAL |
| NFR-SEC-003 | MEDIUM | -- | -- | -- | SC-5 | NO COVERAGE |
| NFR-SEC-004 | HIGH | -- | ASI-08 | -- | CP-2, SC-24 | PARTIAL |
| NFR-SEC-005 | HIGH | -- | ASI-08 | -- | CP-2 | PARTIAL |
| NFR-SEC-006 | CRITICAL | -- | -- | -- | SC-24, AC-3 | PARTIAL |
| NFR-SEC-007 | MEDIUM | -- | -- | -- | SA-8 | NO COVERAGE |
| NFR-SEC-008 | MEDIUM | -- | -- | -- | -- | PARTIAL |
| NFR-SEC-009 | HIGH | -- | ASI-09 | -- | PM-11 | PARTIAL |
| NFR-SEC-010 | HIGH | -- | ASI-09 | -- | IR-7 | PARTIAL |
| NFR-SEC-011 | MEDIUM | -- | -- | -- | CM-3, SI-2 | PARTIAL |
| NFR-SEC-012 | HIGH | -- | -- | -- | CA-8, SA-11 | PARTIAL |
| NFR-SEC-013 | MEDIUM | -- | -- | -- | PL-2, SA-8 | PARTIAL |
| NFR-SEC-014 | HIGH | -- | -- | -- | CA-2, PL-2 | PARTIAL |
| NFR-SEC-015 | MEDIUM | -- | -- | -- | SA-8 | PARTIAL |

### Reverse Traceability: Framework to Requirements

#### OWASP Agentic Top 10

| OWASP Item | Item Name | Requirements | Coverage |
|------------|-----------|-------------|----------|
| ASI-01 | Agent Goal Hijack | FR-SEC-011, -012, -013, -014, -015, -016 | FULL |
| ASI-02 | Tool Misuse & Exploitation | FR-SEC-005, -006, -007, -009, -038 | FULL |
| ASI-03 | Identity & Privilege Abuse | FR-SEC-005, -006, -008, -039, -042 | FULL |
| ASI-04 | Trust Boundary Violations | FR-SEC-008, -010, -022, -025 | FULL |
| ASI-05 | Memory & Context Manipulation | FR-SEC-012, -014, NFR-SEC-002 | FULL |
| ASI-06 | Identity Mismanagement | FR-SEC-001, -002, -003, -004 | FULL |
| ASI-07 | Insecure Inter-Agent Comm | FR-SEC-021, -022, -023, -024 | FULL |
| ASI-08 | Cascading Failures | FR-SEC-034, -035, -040, NFR-SEC-004 | FULL |
| ASI-09 | Insufficient Logging | FR-SEC-029, -030, -031, -032 | FULL |
| ASI-10 | Rogue Agents | FR-SEC-007, -037, -033 | FULL |

**Coverage: 10/10 FULL**

#### OWASP LLM Top 10

| OWASP Item | Item Name | Requirements | Coverage |
|------------|-----------|-------------|----------|
| LLM01 | Prompt Injection | FR-SEC-011, -012, -016 | FULL |
| LLM02 | Sensitive Info Disclosure | FR-SEC-017, -019 | FULL |
| LLM03 | Supply Chain | FR-SEC-025, -026, -027, -028 | FULL |
| LLM04 | Data/Model Poisoning | FR-SEC-014, -015 | PARTIAL (model-level outside scope) |
| LLM05 | Improper Output Handling | FR-SEC-018, -020 | FULL |
| LLM06 | Excessive Agency | FR-SEC-005, -006, -009, -038 | FULL |
| LLM07 | System Prompt Leakage | FR-SEC-017, -019 | FULL |
| LLM08 | Vector/Embedding | N/A | OUT OF SCOPE |
| LLM09 | Misinformation | FR-SEC-020 | PARTIAL (model-level outside scope) |
| LLM10 | Unbounded Consumption | FR-SEC-040, NFR-SEC-002 | FULL |

**Coverage: 7/10 FULL, 2/10 PARTIAL, 1/10 OUT OF SCOPE**

---

## MITRE Coverage Matrix

### MITRE ATT&CK Enterprise (Agent-Relevant Tactics)

| Tactic ID | Tactic Name | Requirements | Coverage |
|-----------|-------------|-------------|----------|
| TA0001 | Initial Access | FR-SEC-011, -012 (injection as initial access) | FULL |
| TA0003 | Persistence | FR-SEC-025, -041 (config-based persistence) | FULL |
| TA0004 | Privilege Escalation | FR-SEC-005, -006, -008, -039 | FULL |
| TA0005 | Defense Evasion | FR-SEC-016, -037 (encoding evasion, rogue detection) | FULL |
| TA0006 | Credential Access | FR-SEC-017, -019 (credential leakage prevention) | FULL |
| TA0007 | Discovery | FR-SEC-010, -032 (boundary isolation, log protection) | FULL |
| TA0008 | Lateral Movement | FR-SEC-010, -022, -024 (boundary enforcement) | FULL |
| TA0009 | Collection | FR-SEC-014, -029 (context protection, audit) | FULL |
| TA0010 | Exfiltration | FR-SEC-009, -013, -017 (toxic combos, MCP, filtering) | FULL |
| TA0011 | Command & Control | FR-SEC-025, -013 (MCP verification) | FULL |
| TA0040 | Impact | FR-SEC-033, -034, -035 (containment, cascading, degradation) | FULL |
| T1195 | Supply Chain Compromise | FR-SEC-025, -026, -027, -028 | FULL |

### MITRE ATLAS (Agent-Specific Techniques)

| Technique ID | Technique Name | Requirements | Coverage |
|-------------|---------------|-------------|----------|
| AML.T0051 | LLM Prompt Injection | FR-SEC-011, -012, -016 | FULL |
| AML.T0051.001 | Indirect Prompt Injection | FR-SEC-012, -013 | FULL |
| AML.T0051.002 | Prompt Injection Evasion | FR-SEC-016 | FULL |
| AML.T0053 | Exfiltration via ML API | FR-SEC-009, -013, -017 | FULL |
| AML.T0054 | Behavior Analysis Evasion | FR-SEC-031, -037 | FULL |
| AML.T0080 | AI Agent Context Poisoning | FR-SEC-014 | FULL |
| AML.T0080.000 | Context Poisoning: Memory | FR-SEC-014, -023 | FULL |
| AML.T0080.001 | Context Poisoning: Thread | FR-SEC-012, -014 | FULL |
| AML.T0081 | Modify AI Agent Config | FR-SEC-041, -026 | FULL |
| AML.T0082 | RAG Credential Harvesting | FR-SEC-017 | FULL |
| AML.T0083 | Credentials from AI Config | FR-SEC-025, -041 | FULL |
| AML.T0043 | Craft Adversarial Data | FR-SEC-012, -014 | FULL |
| AML.T0018 | ML Supply Chain Compromise | FR-SEC-025, -026, -027, -028 | FULL |

**Coverage: 13/13 techniques mapped, all FULL**

---

## OWASP Coverage Matrix

### OWASP API Security Top 10 (Agent-Relevant Items)

| API Item | Item Name | Requirements | Coverage |
|----------|-----------|-------------|----------|
| API1 | Broken Object Level Auth | FR-SEC-001, -002 (agent identity/auth) | FULL |
| API2 | Broken Authentication | FR-SEC-002, -024 (auth at boundaries, anti-spoofing) | FULL |
| API3 | Broken Object Property Auth | FR-SEC-005, -006 (tool access enforcement) | FULL |
| API4 | Unrestricted Resource Consumption | FR-SEC-040, NFR-SEC-001 | FULL |
| API5 | Broken Function Level Auth | FR-SEC-007, -008 (forbidden actions, privilege) | FULL |
| API6 | Unrestricted Server-Side Requests | FR-SEC-013 (MCP sanitization) | FULL |
| API8 | Security Misconfiguration | FR-SEC-041, -042 (secure config, secure defaults) | FULL |
| API10 | Unsafe Consumption of APIs | FR-SEC-012, -013, -025 (tool results, MCP) | FULL |

### OWASP Web Top 10 (Agent-Relevant Items)

| Web Item | Item Name | Requirements | Coverage |
|----------|-----------|-------------|----------|
| A01 | Broken Access Control | FR-SEC-005, -006, -008, -010 | FULL |
| A02 | Cryptographic Failures | FR-SEC-023 (handoff integrity) | FULL |
| A03 | Injection | FR-SEC-011, -012, -013, -016 | FULL |
| A04 | Insecure Design | NFR-SEC-006, -015 (fail-closed, extensibility) | FULL |
| A05 | Security Misconfiguration | FR-SEC-041, -042 | FULL |
| A06 | Vulnerable Components | FR-SEC-025, -026, -027, -028 | FULL |
| A07 | Identity & Auth Failures | FR-SEC-001, -002, -003 | FULL |
| A08 | Software & Data Integrity | FR-SEC-026, -032, -041 | FULL |
| A09 | Security Logging Failures | FR-SEC-029, -030, -031 | FULL |
| A10 | Server-Side Request Forgery | FR-SEC-013 | FULL |

---

## NIST Coverage Matrix

### NIST AI RMF (600-1)

| Function | Sub-Function | Requirements | Coverage |
|----------|-------------|-------------|----------|
| GOVERN | Policies and accountability | FR-SEC-041, NFR-SEC-008 | FULL |
| MAP | AI risk identification | FR-SEC-037 (rogue detection), NFR-SEC-013 | FULL |
| MEASURE | AI risk measurement | FR-SEC-020 (confidence), NFR-SEC-012 | FULL |
| MANAGE | AI risk treatment | FR-SEC-033, -035 (containment, degradation) | FULL |

### NIST CSF 2.0

| Function | Requirements | Coverage |
|----------|-------------|----------|
| IDENTIFY | FR-SEC-001, -003, -031 (identity, lifecycle, anomaly) | FULL |
| PROTECT | FR-SEC-005-013 (access control, input validation) | FULL |
| DETECT | FR-SEC-029-031, -037 (audit, anomaly, rogue detection) | FULL |
| RESPOND | FR-SEC-033-035 (containment, cascading, degradation) | FULL |
| RECOVER | FR-SEC-036 (recovery procedures) | FULL |
| GOVERN | FR-SEC-041, NFR-SEC-008, -013, -014 | FULL |

### NIST SP 800-53 Rev 5 Control Families

| Family | Controls Referenced | Requirements | Coverage |
|--------|-------------------|-------------|----------|
| AC (Access Control) | AC-3, AC-4, AC-5, AC-6 | FR-SEC-005, -006, -007, -008, -009, -010, -039 | FULL |
| AU (Audit) | AU-2, AU-3, AU-6, AU-9, AU-10, AU-11, AU-12 | FR-SEC-004, -029, -030, -031, -032 | FULL |
| CA (Assessment) | CA-2, CA-8 | NFR-SEC-012, -014 | FULL |
| CM (Config Mgmt) | CM-2, CM-3, CM-5, CM-6, CM-7 | FR-SEC-041, -042, NFR-SEC-011 | FULL |
| CP (Contingency) | CP-2, CP-10, CP-12 | FR-SEC-034, -035, -036, NFR-SEC-004, -005 | FULL |
| IA (ID & Auth) | IA-3, IA-4, IA-5, IA-9 | FR-SEC-001, -002, -003 | FULL |
| IR (Incident Resp) | IR-4, IR-5, IR-6, IR-7, IR-8 | FR-SEC-033, -034, -035, -036, NFR-SEC-010 | FULL |
| PL (Planning) | PL-2 | NFR-SEC-013, -014 | FULL |
| PM (Program Mgmt) | PM-11 | NFR-SEC-009 | FULL |
| SA (Sys & Services) | SA-8, SA-11, SA-12 | FR-SEC-025, -026, -027, -028, NFR-SEC-012, -015 | FULL |
| SC (Sys & Comm) | SC-5, SC-6, SC-7, SC-8, SC-13, SC-23, SC-24, SC-28 | FR-SEC-010, -013, -017, -023, -024, -033, -035, NFR-SEC-001, -003, -004, -006 | FULL |
| SI (Sys & Info) | SI-2, SI-3, SI-4, SI-7, SI-10, SI-12, SI-15, SI-17 | FR-SEC-011, -012, -013, -014, -015, -016, -017, -018, -028, -031, -037 | FULL |

**Coverage: 12/12 applicable control families FULL**

---

## Baseline Summary Statistics

### Requirements Count

| Category | Type | Count | CRITICAL | HIGH | MEDIUM |
|----------|------|-------|----------|------|--------|
| Agent Identity & Auth | FR | 4 | 2 | 2 | 0 |
| Authorization & Access Control | FR | 6 | 4 | 2 | 0 |
| Input Validation | FR | 6 | 3 | 2 | 1 |
| Output Security | FR | 4 | 1 | 2 | 1 |
| Inter-Agent Communication | FR | 4 | 0 | 3 | 1 |
| Supply Chain Security | FR | 4 | 1 | 2 | 1 |
| Audit and Logging | FR | 4 | 1 | 1 | 2 |
| Incident Response | FR | 4 | 1 | 2 | 1 |
| Additional Functional | FR | 6 | 3 | 2 | 1 |
| Performance | NFR | 3 | 0 | 2 | 1 |
| Availability | NFR | 3 | 1 | 2 | 0 |
| Scalability | NFR | 2 | 0 | 0 | 2 |
| Usability | NFR | 2 | 0 | 2 | 0 |
| Maintainability | NFR | 5 | 0 | 2 | 3 |
| **TOTAL** | **FR+NFR** | **57** | **17** | **26** | **14** |

### Gap Status Distribution

| Gap Status | Count | Percentage |
|------------|-------|------------|
| NO COVERAGE | 15 | 26.3% |
| PARTIAL | 42 | 73.7% |
| FULL | 0 | 0.0% |

**Note:** NO COVERAGE indicates Jerry has no existing control addressing this requirement. PARTIAL indicates Jerry has related controls that partially satisfy the requirement. FULL would indicate complete satisfaction before Phase 2 implementation. The 0% FULL count is expected -- if requirements were already fully satisfied, they would not need to be baselined for Phase 2 implementation.

### Framework Coverage Summary

| Framework | Items Mapped | Coverage |
|-----------|-------------|----------|
| OWASP Agentic Top 10 | 10/10 | 100% FULL |
| OWASP LLM Top 10 | 9/10 (1 OUT OF SCOPE) | 78% FULL, 22% PARTIAL |
| OWASP API Security Top 10 | 8/10 relevant | 100% FULL |
| OWASP Web Top 10 | 10/10 | 100% FULL |
| MITRE ATT&CK Enterprise | 12 tactics | 100% FULL |
| MITRE ATLAS | 13 techniques | 100% FULL |
| NIST SP 800-53 | 12 control families | 100% FULL |
| NIST AI RMF | 4 functions | 100% FULL |
| NIST CSF 2.0 | 6 functions | 100% FULL |

### Top 5 FMEA Risks Addressed

| Rank | Risk ID | RPN | Risk Description | Requirements |
|------|---------|-----|------------------|-------------|
| 1 | R-PI-002 | 504 | Indirect prompt injection via MCP tool results | FR-SEC-012, -013 |
| 2 | R-SC-001 | 480 | Malicious MCP server packages | FR-SEC-025, -013 |
| 3 | R-GB-001 | 432 | Constitutional circumvention via context rot | FR-SEC-014, -037 |
| 4 | R-CF-005 | 405 | False negatives in security controls | FR-SEC-031, NFR-SEC-006, -012 |
| 5 | R-PI-003 | 392 | Indirect prompt injection via file contents | FR-SEC-012, -011 |

---

## Change Control Process

### Change Request (CR) Process

All modifications to baselined requirements MUST follow this process:

| Step | Action | Authority |
|------|--------|-----------|
| 1 | Submit CR with: requirement ID, proposed change, rationale, impact assessment | Any stakeholder |
| 2 | Impact assessment: affected requirements, affected framework mappings, affected FMEA risks | nse-requirements-002 (or successor) |
| 3 | Review at appropriate criticality level (CR affecting CRITICAL requirements = C4 review) | Per quality-enforcement.md |
| 4 | Approval | C1-C2: requirements agent; C3: lead engineer; C4: architecture review board |
| 5 | Implementation: update this baseline, update traceability matrices, update worktracker | Assigned implementer |
| 6 | Verification: confirm traceability integrity, framework coverage maintained | V&V agent |

### Impact Assessment Requirements

Every CR MUST include:

1. **Requirement Impact:** Which baselined requirements are affected (ID list)
2. **Traceability Impact:** Which framework mappings change (OWASP, MITRE, NIST)
3. **Risk Impact:** Which FMEA risks are affected (risk ID list, RPN changes)
4. **Architecture Impact:** Which Phase 2 architecture decisions are affected
5. **Downstream Impact:** Which dependent requirements are affected (dependency chain)

### Version Control

| Version | Date | Change Description | CR ID |
|---------|------|--------------------|-------|
| 1.0.0 | 2026-02-22 | Initial baseline freeze | N/A (initial) |

---

*Baseline Authority: nse-requirements-002*
*Classification: C4 (Mission-Critical)*
*Quality Gate: S-014 scoring target >= 0.95*
*Work Items: ST-026, ST-027, ST-028*
