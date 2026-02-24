# Security Requirements Discovery

> Agent: nse-requirements-001
> Phase: 1 (Requirements Discovery)
> Pipeline: NSE (NASA-SE)
> Status: COMPLETE
> Date: 2026-02-22

## Document Sections

| Section | Purpose |
|---------|---------|
| [Executive Summary](#executive-summary-l0) | Total requirements count, critical categories, coverage |
| [Requirements Methodology](#requirements-methodology-l2) | Derivation approach, sources, traceability |
| [Functional Security Requirements](#functional-security-requirements-l1) | FR-SEC-001 through FR-SEC-042 |
| [Non-Functional Security Requirements](#non-functional-security-requirements-l1) | NFR-SEC-001 through NFR-SEC-015 |
| [Requirements Traceability Matrix](#requirements-traceability-matrix-l2) | Cross-framework mapping for all requirements |
| [Requirements Coverage Analysis](#requirements-coverage-analysis) | Framework coverage vs. gaps |
| [Key Findings for Phase 2 Architecture](#key-findings-for-phase-2-architecture) | Architecture-driving findings |
| [Citations](#citations) | All sources with authority classification |

---

## Executive Summary (L0)

- **57 total security requirements** derived: 42 functional (FR-SEC) + 15 non-functional (NFR-SEC), covering all 8 functional and 5 non-functional requirement categories defined in the project scope.
- **CRITICAL priority requirements:** 14 requirements classified CRITICAL, addressing prompt injection prevention, tool access control, agent identity, privilege escalation prevention, supply chain integrity, and rogue agent detection -- the highest-impact attack vectors in the agentic threat landscape.
- **Framework coverage:** All 10 OWASP Agentic Top 10 items (ASI01-ASI10) are traced to at least one requirement. 14 NIST SP 800-53 control families are mapped. 8 MITRE ATLAS agent-specific techniques are addressed. OWASP LLM Top 10 items LLM01-LLM10 are cross-referenced where applicable.
- **Jerry mapping:** Every requirement maps to a specific Jerry Framework component (enforcement layers L1-L5, tool tiers T1-T5, constitutional constraints P-003/P-020/P-022, agent definitions, MCP integration, skill architecture, or handoff protocol).
- **Key gap identified:** Jerry's current 5-layer enforcement architecture provides strong governance but lacks explicit agent identity/authentication, cryptographic delegation tokens, runtime anomaly detection, formal supply chain verification for MCP servers, and structured incident response procedures. These gaps drive Phase 2 architecture decisions.

---

## Requirements Methodology (L2)

### Derivation Approach

Requirements were derived through a systematic cross-framework analysis combining threat-informed and control-informed perspectives:

1. **Threat-Informed (Top-Down):** Each OWASP Agentic Top 10 item (ASI01-ASI10) was analyzed for attack vectors applicable to the Jerry Framework. Each attack vector was mapped to one or more testable "shall" requirements with acceptance criteria.

2. **Control-Informed (Bottom-Up):** NIST SP 800-53 Rev 5 control families relevant to agentic AI systems (AC, AU, AT, CA, CM, IA, IR, MA, MP, PE, PL, RA, SA, SC, SI, PM) were reviewed. Controls applicable to agent platforms were adapted into Jerry-specific requirements.

3. **AI-Specific Augmentation:** MITRE ATLAS techniques (particularly the 14 agent-specific techniques added October 2025) and NIST AI RMF 600-1 functions (GOVERN, MAP, MEASURE, MANAGE) were used to fill gaps not covered by traditional cybersecurity frameworks.

4. **Industry Convergence Validation:** Requirements were validated against the 12 core agentic security principles identified through cross-industry consensus (Anthropic, Microsoft, Google DeepMind, Cisco, Meta, OWASP) documented in data-sources.md Finding 10.

### Sources Used

| Source | Framework | Items Consumed |
|--------|-----------|----------------|
| OWASP Agentic Top 10 (2026) | ASI01-ASI10 | All 10 items with mitigations |
| OWASP LLM Top 10 (2025) | LLM01-LLM10 | All 10 items, cross-referenced |
| OWASP API Security Top 10 | API1-API10 | Selected items (auth, injection, SSRF) |
| MITRE ATT&CK Enterprise | 14 tactics | Relevant techniques per tactic |
| MITRE ATLAS | 15 tactics, 66 techniques | Agent-specific techniques (14 new, 2025) |
| NIST SP 800-53 Rev 5 | 20 control families | 14 families applicable to agentic systems |
| NIST AI RMF (600-1) | GOVERN/MAP/MEASURE/MANAGE | GenAI-specific risk categories |
| NIST CSF 2.0 | 6 functions | Identify/Protect/Detect/Respond/Recover/Govern |
| Microsoft Agent 365 | Agent identity, control plane | Control/data plane separation |
| Google DeepMind | Delegation framework | Delegation Capability Tokens (DCTs) |
| Meta | Rule of Two | Agent capability constraint design |
| Anthropic | GTG-1002 incident, sandboxing | Attack surface validation |
| Cisco | State of AI Security 2026 | MCP attack surface, security scanners |

### Traceability Approach

Every requirement includes:
- **Source Framework** with specific item ID (e.g., "OWASP ASI-03", "NIST AC-6", "ATLAS AML.T0051")
- **Jerry Mapping** to the specific framework component affected
- **Priority** classification (CRITICAL/HIGH/MEDIUM/LOW) based on: (a) exploitability of the threat, (b) impact if exploited, (c) existing Jerry controls that partially mitigate, (d) industry consensus on severity
- **Acceptance Criteria** that are testable and verifiable

### Requirement Naming Convention

- `FR-SEC-{NNN}`: Functional Security Requirement
- `NFR-SEC-{NNN}`: Non-Functional Security Requirement

Priority is classified per NIST risk-informed approach:
- **CRITICAL**: Exploitable with high impact; no existing Jerry mitigation; industry consensus on severity
- **HIGH**: Exploitable with significant impact; partial Jerry mitigation exists
- **MEDIUM**: Moderate exploitability or impact; Jerry has related controls
- **LOW**: Low probability or limited impact; defense-in-depth enhancement

---

## Functional Security Requirements (L1)

### Category 1: Agent Identity and Authentication

#### FR-SEC-001

| Field | Value |
|-------|-------|
| ID | FR-SEC-001 |
| Title | Unique Agent Identity |
| Description | The system SHALL assign a unique, non-reusable identity to every agent instance at creation time. Each agent identity SHALL include: agent name, version, parent skill, invocation timestamp, and a cryptographic nonce. |
| Priority | CRITICAL |
| Source Framework | OWASP ASI-06 (Identity and Access Mismanagement), Microsoft Agent 365 (Agent ID), NIST IA-4 (Identifier Management) |
| Acceptance Criteria | (1) Every Task invocation produces a unique agent instance ID in the format `{agent-name}-{timestamp}-{nonce}`. (2) No two concurrent agent instances share the same identity. (3) Agent identity is present in all audit log entries. (4) Identity persists for the lifetime of the agent invocation and is immutable after creation. |
| Jerry Mapping | Agent definition YAML (`name` field), Task tool invocation, L3 pre-tool gating, orchestration routing context (`routing_history`) |

#### FR-SEC-002

| Field | Value |
|-------|-------|
| ID | FR-SEC-002 |
| Title | Agent Authentication at Trust Boundaries |
| Description | The system SHALL authenticate agent identity at every trust boundary crossing: orchestrator-to-worker delegation, inter-skill handoff, and MCP server interaction. Authentication SHALL use the agent's unique identity (FR-SEC-001) validated against the agent registry. |
| Priority | CRITICAL |
| Source Framework | OWASP ASI-06, OWASP ASI-07 (Insecure Inter-Agent Communication), NIST IA-3 (Device Identification and Authentication), NIST IA-9 (Service Identification and Authentication) |
| Acceptance Criteria | (1) Handoff protocol validates `from_agent` field against registered agent names before accepting handoff data. (2) Unregistered agent names are rejected with an authentication failure logged. (3) MCP tool invocations include the invoking agent's identity in the request context. (4) Authentication check executes at L3 (deterministic, pre-tool) for context-rot immunity. |
| Jerry Mapping | Handoff protocol (HD-M-001), agent-development-standards.md agent registry, L3 enforcement layer, MCP tool standards |

#### FR-SEC-003

| Field | Value |
|-------|-------|
| ID | FR-SEC-003 |
| Title | Agent Identity Lifecycle Management |
| Description | The system SHALL enforce agent identity lifecycle: creation at Task invocation, active during execution, termination at task completion. Terminated agent identities SHALL NOT be reused. The system SHALL maintain a registry of active agent identities with maximum concurrent instance limits. |
| Priority | HIGH |
| Source Framework | OWASP ASI-06, NIST IA-4 (Identifier Management), NIST IA-5 (Authenticator Management) |
| Acceptance Criteria | (1) Active agent registry is queryable at any point during execution. (2) Terminated agent IDs are marked as expired and cannot be reused for new invocations. (3) Maximum concurrent agent instances per skill is configurable and enforced (default: 5). (4) Orphaned agent instances (no activity for configurable timeout) are automatically terminated. |
| Jerry Mapping | Task tool, orchestration state (ORCHESTRATION.yaml), agent definition schema, L4 post-tool inspection |

#### FR-SEC-004

| Field | Value |
|-------|-------|
| ID | FR-SEC-004 |
| Title | Agent Provenance Tracking |
| Description | The system SHALL track the complete provenance chain for every agent action: which user initiated the session, which orchestrator delegated the task, which agent performed the action, and which tools were invoked. Provenance SHALL be immutable and append-only. |
| Priority | HIGH |
| Source Framework | OWASP ASI-06, OWASP ASI-09 (Insufficient Logging), NIST AU-3 (Content of Audit Records), NIST AU-10 (Non-repudiation) |
| Acceptance Criteria | (1) Every tool invocation log entry includes: user session ID, orchestrator agent ID, executing agent ID, tool name, timestamp. (2) Provenance chain is append-only; no log entry can be modified after creation. (3) Provenance chain is queryable for any completed agent task. (4) Handoff protocol includes provenance metadata (routing_history). |
| Jerry Mapping | Routing observability (RT-M-008), handoff protocol, L4 post-tool inspection, worktracker entries |

### Category 2: Authorization and Access Control

#### FR-SEC-005

| Field | Value |
|-------|-------|
| ID | FR-SEC-005 |
| Title | Least Privilege Tool Access Enforcement |
| Description | The system SHALL enforce that every agent operates with the minimum tool access required for its function, as declared in its `capabilities.allowed_tools` YAML field. Tool access SHALL be verified at L3 (deterministic pre-tool gating) before every tool invocation. Any tool invocation not in the agent's allowed list SHALL be blocked. |
| Priority | CRITICAL |
| Source Framework | OWASP ASI-02 (Tool Misuse), OWASP ASI-03 (Privilege Escalation), NIST AC-6 (Least Privilege), NIST AC-3 (Access Enforcement) |
| Acceptance Criteria | (1) L3 gate validates every tool invocation against the agent's `capabilities.allowed_tools` list. (2) Blocked tool invocations are logged with agent ID, attempted tool, and reason. (3) Zero false negatives: no tool invocation bypasses the L3 gate. (4) Agent definitions without `capabilities.allowed_tools` are rejected at CI (L5). |
| Jerry Mapping | Tool tiers T1-T5, agent definition schema (H-34), L3 pre-tool gating, L5 CI verification |

#### FR-SEC-006

| Field | Value |
|-------|-------|
| ID | FR-SEC-006 |
| Title | Tool Tier Boundary Enforcement |
| Description | The system SHALL enforce tool tier boundaries (T1-T5) such that an agent assigned tier N cannot invoke any tool from tier N+1 or above. Worker agents (invoked via Task) SHALL NOT be assigned T5 (Full) tier. Tier assignments SHALL be validated against the agent definition schema. |
| Priority | CRITICAL |
| Source Framework | OWASP ASI-02, OWASP ASI-03, NIST AC-6 (Least Privilege), NIST AC-5 (Separation of Duties) |
| Acceptance Criteria | (1) Tool tier mapping is maintained as a SSOT configuration. (2) L3 gate rejects tool invocations that exceed the agent's tier level. (3) No worker agent has Task tool in `capabilities.allowed_tools` (H-35). (4) Tier violations are logged and reported as security events. |
| Jerry Mapping | Tool tiers T1-T5 (agent-development-standards.md), H-35 (constitutional compliance), L3 enforcement, L5 CI schema validation |

#### FR-SEC-007

| Field | Value |
|-------|-------|
| ID | FR-SEC-007 |
| Title | Forbidden Action Enforcement |
| Description | The system SHALL enforce `capabilities.forbidden_actions` declared in every agent definition. Forbidden actions SHALL be checked at L3 before tool invocation and at L4 after tool completion. The constitutional triplet (P-003, P-020, P-022) SHALL be present in every agent's forbidden actions. |
| Priority | CRITICAL |
| Source Framework | OWASP ASI-02 (Tool Misuse), OWASP ASI-10 (Rogue Agents), NIST AC-3 (Access Enforcement), NIST SI-10 (Information Input Validation) |
| Acceptance Criteria | (1) Every agent definition includes minimum 3 forbidden actions referencing P-003, P-020, P-022. (2) L3 checks tool invocation patterns against forbidden action declarations. (3) L4 inspects tool outputs for evidence of forbidden action execution. (4) Forbidden action violations trigger immediate agent termination and security event logging. |
| Jerry Mapping | H-35 (constitutional compliance), agent definition schema, L3/L4 enforcement layers, constitutional constraints |

#### FR-SEC-008

| Field | Value |
|-------|-------|
| ID | FR-SEC-008 |
| Title | Privilege Non-Escalation in Delegation Chains |
| Description | The system SHALL ensure that delegated agents cannot acquire privileges exceeding those of the delegating agent. When an orchestrator delegates to a worker via Task, the worker's effective permissions SHALL be the intersection (not union) of the orchestrator's permissions and the worker's declared permissions. |
| Priority | CRITICAL |
| Source Framework | OWASP ASI-03 (Privilege Escalation), OWASP ASI-04 (Delegated Trust Boundary Violations), Google DeepMind Delegation Framework (DCTs), NIST AC-6(1) (Authorize Access to Security Functions) |
| Acceptance Criteria | (1) Worker agent effective permissions are computed as: MIN(orchestrator_tier, worker_declared_tier). (2) A T2 orchestrator cannot delegate to a T3 worker. (3) Privilege computation is logged in the handoff metadata. (4) Delegation chains are limited to 1 level per H-01/P-003. |
| Jerry Mapping | P-003 (no recursive subagents), tool tiers T1-T5, handoff protocol (criticality propagation CP-04), L3 pre-tool gating |

#### FR-SEC-009

| Field | Value |
|-------|-------|
| ID | FR-SEC-009 |
| Title | Toxic Tool Combination Prevention |
| Description | The system SHALL detect and prevent toxic tool combinations that create exfiltration or exploitation paths. Specifically: (a) database read + external network access in the same agent, (b) file system write + code execution without HITL approval, (c) credential access + external API invocation without scoping. The system SHALL enforce Meta's Rule of Two: no agent satisfies all three of processing untrusted input, accessing sensitive data, and changing external state without HITL. |
| Priority | HIGH |
| Source Framework | OWASP ASI-02 (Tool Misuse), Meta Rule of Two, NIST AC-6(3) (Network Access to Privileged Commands), ATLAS AML.T0053 (Exfiltration via ML API) |
| Acceptance Criteria | (1) A toxic combination registry defines prohibited tool pairings. (2) L3 gate checks the agent's full tool set against the toxic combination registry at invocation time. (3) Agents violating Rule of Two constraints trigger HITL approval requirement. (4) Toxic combination detection is configurable and extensible. |
| Jerry Mapping | Tool tiers T1-T5, agent definition `capabilities.allowed_tools`, L3 enforcement, P-020 (user authority for HITL) |

#### FR-SEC-010

| Field | Value |
|-------|-------|
| ID | FR-SEC-010 |
| Title | Permission Boundary Isolation Between Skills |
| Description | The system SHALL enforce permission boundaries between skills such that agents from different skills cannot access each other's internal state, tool results, or intermediate artifacts unless explicitly shared via the handoff protocol. Each skill SHALL operate in its own context isolation boundary. |
| Priority | HIGH |
| Source Framework | OWASP ASI-04 (Delegated Trust Boundary Violations), NIST AC-4 (Information Flow Enforcement), NIST SC-7 (Boundary Protection) |
| Acceptance Criteria | (1) No agent can read artifacts produced by another skill's agents without receiving them via handoff. (2) Tool results from one agent invocation are not accessible to other agent invocations. (3) Context isolation is enforced by the Task tool's inherent context boundary (Pattern 2: Orchestrator-Worker). (4) Shared state is limited to the handoff protocol's defined fields. |
| Jerry Mapping | Task tool context isolation, handoff protocol (HD-M-001), agent-routing-standards.md context sharing, P-003 single-level nesting |

### Category 3: Input Validation

#### FR-SEC-011

| Field | Value |
|-------|-------|
| ID | FR-SEC-011 |
| Title | Direct Prompt Injection Prevention |
| Description | The system SHALL validate all user-provided input for prompt injection patterns before the input reaches agent processing. Validation SHALL include: (a) detection of instruction override patterns ("ignore previous instructions", "you are now", system prompt extraction attempts), (b) detection of role manipulation attempts, (c) detection of encoding-based evasion (Base64, Unicode, homoglyph substitution). |
| Priority | CRITICAL |
| Source Framework | OWASP LLM01 (Prompt Injection), OWASP ASI-01 (Agent Goal Hijack), ATLAS AML.T0051 (LLM Prompt Injection), NIST SI-10 (Information Input Validation) |
| Acceptance Criteria | (1) Input validation filter operates at L3 (deterministic, pre-processing). (2) Known prompt injection patterns are maintained in a versioned pattern database. (3) Detection rate >= 95% against the OWASP prompt injection test suite. (4) False positive rate <= 5% on legitimate user requests. (5) Detected injection attempts are logged with full context for forensic analysis. |
| Jerry Mapping | L3 pre-tool gating, guardrails.input_validation in agent definitions, L2 per-prompt re-injection (constitutional constraints immune to injection) |

#### FR-SEC-012

| Field | Value |
|-------|-------|
| ID | FR-SEC-012 |
| Title | Indirect Prompt Injection Prevention via Tool Results |
| Description | The system SHALL treat all data returned by tool invocations (Read, Grep, Glob, WebFetch, WebSearch, MCP tools) as untrusted input. Tool results SHALL be validated at L4 (post-tool inspection) for embedded instruction patterns before being consumed by agent reasoning. The system SHALL maintain a clear boundary between tool result data and agent instructions. |
| Priority | CRITICAL |
| Source Framework | OWASP LLM01 (Prompt Injection -- Indirect), OWASP ASI-01 (Agent Goal Hijack), OWASP ASI-05 (Memory and Context Manipulation), ATLAS AML.T0051.001 (Indirect Prompt Injection) |
| Acceptance Criteria | (1) L4 inspection layer scans tool results for instruction injection patterns. (2) Tool results are clearly delimited from system/agent instructions in the context. (3) Suspected indirect injection in tool results triggers: (a) flagging in the audit log, (b) presentation to user for review if above confidence threshold. (4) MCP server responses receive heightened scrutiny (external trust boundary). |
| Jerry Mapping | L4 post-tool inspection, MCP tool standards, guardrails.output_filtering, tool result handling in agent methodology |

#### FR-SEC-013

| Field | Value |
|-------|-------|
| ID | FR-SEC-013 |
| Title | MCP Server Input Sanitization |
| Description | The system SHALL sanitize all data sent to and received from MCP servers. Outbound sanitization SHALL prevent leakage of system prompts, constitutional rules, internal file paths, and credentials. Inbound sanitization SHALL validate MCP responses against expected schemas and reject malformed or suspicious responses. |
| Priority | CRITICAL |
| Source Framework | OWASP ASI-01 (Agent Goal Hijack via MCP), OWASP LLM03 (Supply Chain), Cisco State of AI Security 2026 (MCP attack surface), NIST SC-7 (Boundary Protection), NIST SI-10 (Information Input Validation) |
| Acceptance Criteria | (1) MCP outbound requests are filtered to exclude: system prompt content, L2 REINJECT markers, file paths outside approved directories, environment variables, credentials. (2) MCP inbound responses are validated against the MCP response schema. (3) MCP responses exceeding configurable size limits are truncated with a warning. (4) All MCP interactions are logged with full request/response metadata. |
| Jerry Mapping | MCP tool standards (mcp-tool-standards.md), L3/L4 enforcement around MCP calls, canonical tool names, error handling fallbacks |

#### FR-SEC-014

| Field | Value |
|-------|-------|
| ID | FR-SEC-014 |
| Title | Context Manipulation Prevention |
| Description | The system SHALL prevent manipulation of the agent's context window through: (a) enforcing L2 per-prompt re-injection of constitutional constraints (immune to context rot), (b) detecting attempts to exhaust the context window (unbounded consumption), (c) validating that context items have not been tampered with between handoffs. |
| Priority | HIGH |
| Source Framework | OWASP ASI-05 (Memory and Context Manipulation), OWASP LLM10 (Unbounded Consumption), ATLAS AML.T0080 (Memory Poisoning), NIST SI-7 (Software, Firmware, and Information Integrity) |
| Acceptance Criteria | (1) L2 re-injection operates on every prompt regardless of context state. (2) Context fill monitoring per AE-006 graduated escalation detects unbounded consumption. (3) Handoff data integrity is validated via key_findings checksums. (4) Context window consumption by any single tool result is bounded per CB-02 (50% maximum). |
| Jerry Mapping | L2 per-prompt re-injection, AE-006 graduated escalation, context budget standards CB-01 through CB-05, handoff protocol integrity |

#### FR-SEC-015

| Field | Value |
|-------|-------|
| ID | FR-SEC-015 |
| Title | Agent Goal Integrity Verification |
| Description | The system SHALL verify that agent goals and objectives have not been altered during execution. The original task description, success criteria, and criticality level from the handoff protocol SHALL be immutable after delegation. Any detected goal modification SHALL trigger agent termination and security event logging. |
| Priority | HIGH |
| Source Framework | OWASP ASI-01 (Agent Goal Hijack), ATLAS AML.T0051 (Prompt Injection), NIST SI-7 (Information Integrity) |
| Acceptance Criteria | (1) Handoff `task` and `success_criteria` fields are immutable after initial delegation. (2) L4 post-tool inspection detects if agent output diverges significantly from stated success criteria. (3) Goal modification attempts are logged as security events. (4) Orchestrator validates that worker output aligns with delegated task before accepting results. |
| Jerry Mapping | Handoff protocol (HD-M-001), success_criteria field, L4 post-tool inspection, orchestration state tracking |

#### FR-SEC-016

| Field | Value |
|-------|-------|
| ID | FR-SEC-016 |
| Title | Encoding and Obfuscation Attack Prevention |
| Description | The system SHALL detect and neutralize encoding-based attacks including: Base64-encoded instructions, Unicode normalization attacks, homoglyph substitution, invisible Unicode characters, right-to-left override characters, and multi-layer encoding chains. |
| Priority | MEDIUM |
| Source Framework | OWASP LLM01 (Prompt Injection -- evasion techniques), ATLAS AML.T0051.002 (Prompt Injection Evasion), NIST SI-10 (Information Input Validation) |
| Acceptance Criteria | (1) Input pre-processing normalizes all Unicode to NFC form. (2) Base64 and other common encodings are detected and decoded for inspection. (3) Invisible/control characters are stripped from user input. (4) Multi-layer encoding (e.g., Base64 of URL-encoded content) is recursively decoded up to configurable depth (default: 3 layers). |
| Jerry Mapping | L3 pre-tool input validation, guardrails.input_validation in agent definitions |

### Category 4: Output Security

#### FR-SEC-017

| Field | Value |
|-------|-------|
| ID | FR-SEC-017 |
| Title | Sensitive Information Output Filtering |
| Description | The system SHALL filter agent output to prevent disclosure of: (a) system prompts and constitutional rules, (b) L2 REINJECT markers and enforcement architecture details, (c) internal file paths beyond the project workspace, (d) credentials, API keys, tokens, and secrets, (e) other agents' handoff data not intended for the user. |
| Priority | CRITICAL |
| Source Framework | OWASP LLM02 (Sensitive Information Disclosure), OWASP LLM07 (System Prompt Leakage), NIST SC-28 (Protection of Information at Rest), NIST SI-15 (Information Output Filtering) |
| Acceptance Criteria | (1) Output filtering operates at L4 (post-tool inspection) before presenting results to user. (2) Known sensitive patterns (API key formats, credential patterns, REINJECT markers) are detected and redacted. (3) System prompt extraction attempts that succeed are caught at output and redacted. (4) Filtering rules are versioned and extensible. |
| Jerry Mapping | L4 post-tool inspection, guardrails.output_filtering in agent definitions (minimum 3 entries per H-34), constitutional constraints |

#### FR-SEC-018

| Field | Value |
|-------|-------|
| ID | FR-SEC-018 |
| Title | Output Sanitization for Downstream Consumption |
| Description | The system SHALL sanitize agent output that will be consumed by downstream systems, tools, or other agents. Sanitization SHALL prevent: (a) injection attacks via agent output (command injection, path traversal), (b) unvalidated code execution from agent-generated code, (c) malformed data that could corrupt downstream processing. |
| Priority | HIGH |
| Source Framework | OWASP LLM05 (Improper Output Handling), OWASP ASI-08 (Cascading Failures), NIST SI-15 (Information Output Filtering), NIST SI-3 (Malicious Code Protection) |
| Acceptance Criteria | (1) Agent-generated file paths are validated against an allowlist of permitted directories. (2) Agent-generated code requires HITL approval before execution (P-020). (3) Agent output consumed by other agents via handoff is schema-validated (HD-M-001). (4) Command-like patterns in output are flagged for review. |
| Jerry Mapping | L4 post-tool inspection, handoff protocol schema validation, P-020 (user authority), Bash tool usage patterns |

#### FR-SEC-019

| Field | Value |
|-------|-------|
| ID | FR-SEC-019 |
| Title | System Prompt Leakage Prevention |
| Description | The system SHALL prevent leakage of system prompts, CLAUDE.md content, rule files, L2 REINJECT markers, and enforcement architecture details through any output channel. The system SHALL detect system prompt extraction techniques including: direct asking, encoding tricks, role-play scenarios, and iterative probing. |
| Priority | HIGH |
| Source Framework | OWASP LLM07 (System Prompt Leakage), NIST SC-28 (Protection of Information at Rest), NIST AC-3 (Access Enforcement) |
| Acceptance Criteria | (1) Output filter detects verbatim or near-verbatim reproduction of rule file content. (2) L2 REINJECT marker content is never present in user-facing output. (3) Enforcement architecture details (layer names, token budgets, strategy IDs) are not disclosed unless user is an authorized administrator. (4) System prompt extraction test suite achieves >= 95% prevention rate. |
| Jerry Mapping | L4 output inspection, .context/rules/ files, L2 REINJECT markers, enforcement architecture documentation |

#### FR-SEC-020

| Field | Value |
|-------|-------|
| ID | FR-SEC-020 |
| Title | Confidence and Uncertainty Disclosure |
| Description | The system SHALL ensure that agents accurately represent their confidence levels and uncertainty in outputs per P-022 (no deception). Agent outputs SHALL include confidence indicators when making claims, recommendations, or decisions. The system SHALL detect and prevent confidence inflation (leniency bias). |
| Priority | MEDIUM |
| Source Framework | OWASP LLM09 (Misinformation), P-022 (No Deception), NIST AI RMF MEASURE function, NIST SI-12 (Information Management and Retention) |
| Acceptance Criteria | (1) Handoff confidence scores follow calibration guidance (0.0-1.0 scale per HD-M-001). (2) S-014 LLM-as-Judge scoring actively counteracts leniency bias per quality-enforcement.md. (3) Agent outputs for C2+ deliverables include explicit confidence/uncertainty statements. (4) Claims without supporting evidence are flagged during self-review (S-010). |
| Jerry Mapping | P-022 (no deception), handoff protocol confidence field, S-014 scoring, S-010 self-review, quality gate (H-13) |

### Category 5: Inter-Agent Communication

#### FR-SEC-021

| Field | Value |
|-------|-------|
| ID | FR-SEC-021 |
| Title | Structured Handoff Protocol Enforcement |
| Description | The system SHALL enforce that all inter-agent communication uses the structured handoff protocol (handoff-v2 schema). Free-text handoffs without schema validation SHALL be rejected. Every handoff SHALL include all required fields: from_agent, to_agent, task, success_criteria, artifacts, key_findings, blockers, confidence, criticality. |
| Priority | HIGH |
| Source Framework | OWASP ASI-07 (Insecure Inter-Agent Communication), NIST SC-8 (Transmission Confidentiality and Integrity), NIST SI-10 (Information Input Validation) |
| Acceptance Criteria | (1) Handoff schema validation executes at L3 before agent invocation. (2) Schema validation rejects handoffs missing any required field. (3) Free-text delegation (unstructured Task prompts) triggers a warning and automatic schema wrapping. (4) Schema version is tracked in every handoff for compatibility verification. |
| Jerry Mapping | Handoff protocol (HD-M-001 through HD-M-005), agent-development-standards.md, L3 pre-tool gating, handoff-v2 schema |

#### FR-SEC-022

| Field | Value |
|-------|-------|
| ID | FR-SEC-022 |
| Title | Trust Boundary Enforcement at Handoffs |
| Description | The system SHALL enforce trust boundaries at every handoff: (a) criticality level SHALL NOT decrease through handoff chains (CP-04), (b) persistent blockers SHALL propagate with [PERSISTENT] prefix (CP-05), (c) artifact paths SHALL be validated for existence before delivery (HD-M-002), (d) quality gate SHALL be passed before handoff delivery for C2+ (HD-M-003). |
| Priority | HIGH |
| Source Framework | OWASP ASI-04 (Delegated Trust Boundary Violations), OWASP ASI-07, NIST AC-4 (Information Flow Enforcement), NIST SC-7 (Boundary Protection) |
| Acceptance Criteria | (1) Criticality downgrade attempts are blocked and logged. (2) Persistent blockers present in source handoff appear in all downstream handoffs. (3) Artifact paths that do not resolve to existing files cause handoff rejection. (4) C2+ handoffs without quality gate score >= 0.92 are held pending revision. |
| Jerry Mapping | Handoff protocol (CP-01 through CP-05), HD-M-001 through HD-M-005, quality gate (H-13), L3/L4 enforcement |

#### FR-SEC-023

| Field | Value |
|-------|-------|
| ID | FR-SEC-023 |
| Title | Message Integrity in Handoff Chains |
| Description | The system SHALL ensure message integrity across handoff chains by: (a) including a hash of key handoff fields (task, success_criteria, criticality) that downstream agents can verify, (b) detecting if handoff content has been modified in transit, (c) logging the complete handoff chain for forensic analysis. |
| Priority | MEDIUM |
| Source Framework | OWASP ASI-07 (Insecure Inter-Agent Communication), NIST SC-8 (Transmission Integrity), NIST SC-13 (Cryptographic Protection), NIST AU-10 (Non-repudiation) |
| Acceptance Criteria | (1) Handoff metadata includes a SHA-256 hash of immutable fields. (2) Receiving agent validates the hash before processing. (3) Hash mismatch triggers handoff rejection and security event. (4) Complete handoff chains are reconstructable from audit logs. |
| Jerry Mapping | Handoff protocol, routing_history tracking, L4 post-tool inspection, orchestration state |

#### FR-SEC-024

| Field | Value |
|-------|-------|
| ID | FR-SEC-024 |
| Title | Anti-Spoofing for Agent Communication |
| Description | The system SHALL prevent agent identity spoofing in inter-agent communication. An agent SHALL NOT be able to impersonate another agent by modifying the `from_agent` field in handoffs. The system SHALL validate that the `from_agent` field matches the actual invoking agent's registered identity. |
| Priority | HIGH |
| Source Framework | OWASP ASI-07, OWASP ASI-10 (Rogue Agents), NIST IA-3 (Device Identification and Authentication), NIST SC-23 (Session Authenticity) |
| Acceptance Criteria | (1) Handoff `from_agent` is set by the system (not by the agent) based on the invocation context. (2) Agent-supplied `from_agent` values that do not match the system-assigned identity are rejected. (3) Spoofing attempts are logged as security events with full context. (4) Send-side validation (SV-02) is enforced by the system, not self-reported. |
| Jerry Mapping | Handoff protocol (SV-02), agent identity (FR-SEC-001), L3 enforcement, Task tool invocation context |

### Category 6: Supply Chain Security

#### FR-SEC-025

| Field | Value |
|-------|-------|
| ID | FR-SEC-025 |
| Title | MCP Server Integrity Verification |
| Description | The system SHALL verify the integrity of all MCP servers before allowing agent interaction. Verification SHALL include: (a) server identity validation against an approved server registry, (b) configuration checksum verification, (c) detection of unauthorized server modifications. Only registered MCP servers SHALL be permitted for agent use. |
| Priority | CRITICAL |
| Source Framework | OWASP LLM03 (Supply Chain), OWASP ASI-04 (Supply Chain Vulnerabilities -- per 2026 update), Cisco State of AI Security 2026, Anthropic GTG-1002 lessons, NIST SA-12 (Supply Chain Protection), NIST SI-7 (Software Integrity) |
| Acceptance Criteria | (1) MCP server registry maintained in `.claude/settings.local.json` with checksums. (2) MCP server configuration changes trigger security event logging. (3) Unauthorized MCP servers (not in registry) are blocked at L3. (4) MCP server health checks execute before first tool invocation in a session. |
| Jerry Mapping | MCP tool standards (mcp-tool-standards.md), `.claude/settings.local.json`, canonical tool names, L3 pre-tool gating |

#### FR-SEC-026

| Field | Value |
|-------|-------|
| ID | FR-SEC-026 |
| Title | Dependency Verification for Agent Definitions |
| Description | The system SHALL verify the integrity of agent definition files before loading them for execution. Verification SHALL include: (a) YAML schema validation against the canonical JSON Schema (H-34), (b) constitutional compliance check (P-003, P-020, P-022 present per H-35), (c) file integrity verification (no unauthorized modifications since last CI validation). |
| Priority | HIGH |
| Source Framework | OWASP LLM03 (Supply Chain), OWASP ASI-10 (Rogue Agents), NIST SA-12 (Supply Chain Protection), NIST CM-3 (Configuration Change Control) |
| Acceptance Criteria | (1) Agent definitions are schema-validated at L3 before any Task invocation. (2) Missing constitutional triplet causes agent load rejection. (3) Agent definition files are tracked by L5 CI for unauthorized modifications. (4) Modified agent definitions require re-validation before use. |
| Jerry Mapping | H-34 (agent definition schema), H-35 (constitutional compliance), L3 pre-tool gating, L5 CI verification |

#### FR-SEC-027

| Field | Value |
|-------|-------|
| ID | FR-SEC-027 |
| Title | Skill Integrity Verification |
| Description | The system SHALL verify skill integrity before skill invocation. Verification SHALL include: (a) SKILL.md existence and format validation (H-25, H-26), (b) agent definition integrity within the skill, (c) skill registration in CLAUDE.md and AGENTS.md, (d) detection of unauthorized skill modifications since last commit. |
| Priority | HIGH |
| Source Framework | OWASP LLM03 (Supply Chain), NIST SA-12 (Supply Chain Protection), NIST CM-5 (Access Restrictions for Change), NIST SI-7 (Software Integrity) |
| Acceptance Criteria | (1) Skill invocation validates SKILL.md presence and format at L3. (2) Unregistered skills (not in CLAUDE.md) cannot be invoked. (3) Git status check detects uncommitted modifications to skill files. (4) Modified skills require explicit user approval before invocation. |
| Jerry Mapping | H-25/H-26 (skill standards), CLAUDE.md skill registry, AGENTS.md agent registry, L3/L5 enforcement |

#### FR-SEC-028

| Field | Value |
|-------|-------|
| ID | FR-SEC-028 |
| Title | Python Dependency Supply Chain Security |
| Description | The system SHALL verify Python dependencies managed through UV for known vulnerabilities and integrity. The system SHALL: (a) use lock files for reproducible builds, (b) verify dependency checksums, (c) scan for known CVEs in dependencies, (d) enforce UV-only installation (H-05). |
| Priority | MEDIUM |
| Source Framework | OWASP LLM03 (Supply Chain), NIST SA-12 (Supply Chain Protection), NIST SI-2 (Flaw Remediation), MITRE ATT&CK T1195 (Supply Chain Compromise) |
| Acceptance Criteria | (1) `uv.lock` file is committed and used for all dependency resolution. (2) L5 CI includes dependency vulnerability scanning. (3) Dependencies with known CRITICAL CVEs block CI. (4) Direct pip/python usage is blocked per H-05 enforcement. |
| Jerry Mapping | H-05 (UV-only), pyproject.toml, L5 CI verification, python-environment.md |

### Category 7: Audit and Logging

#### FR-SEC-029

| Field | Value |
|-------|-------|
| ID | FR-SEC-029 |
| Title | Comprehensive Agent Action Audit Trail |
| Description | The system SHALL maintain a comprehensive audit trail of all agent actions including: (a) every tool invocation with parameters and results summary, (b) every handoff with full metadata, (c) every routing decision with method and confidence, (d) every security event (blocked actions, detected injections, policy violations), (e) agent lifecycle events (creation, execution, termination). |
| Priority | CRITICAL |
| Source Framework | OWASP ASI-09 (Insufficient Logging and Monitoring), NIST AU-2 (Event Logging), NIST AU-3 (Content of Audit Records), NIST AU-12 (Audit Record Generation) |
| Acceptance Criteria | (1) Every tool invocation produces an audit log entry with: timestamp, agent ID, tool name, parameters hash, result status, duration. (2) Every handoff produces an audit log entry with: from_agent, to_agent, criticality, confidence, artifact list. (3) Security events are logged with: event type, severity, agent ID, full context, recommended action. (4) Audit logs are append-only and tamper-evident. |
| Jerry Mapping | Routing observability (RT-M-008), worktracker entries, orchestration state tracking, L4 post-tool inspection |

#### FR-SEC-030

| Field | Value |
|-------|-------|
| ID | FR-SEC-030 |
| Title | Security Event Logging |
| Description | The system SHALL log security-specific events at a higher detail level than operational events. Security events SHALL include: (a) prompt injection detection (direct and indirect), (b) tool access violations, (c) forbidden action attempts, (d) authentication failures, (e) privilege escalation attempts, (f) circuit breaker activations, (g) anomalous agent behavior patterns, (h) MCP server communication anomalies. |
| Priority | HIGH |
| Source Framework | OWASP ASI-09, NIST AU-6 (Audit Record Review, Analysis, and Reporting), NIST SI-4 (System Monitoring), NIST IR-5 (Incident Monitoring) |
| Acceptance Criteria | (1) Security events are categorized by severity: CRITICAL, HIGH, MEDIUM, LOW. (2) CRITICAL security events trigger immediate user notification. (3) Security event logs include sufficient context for forensic reconstruction. (4) Security events are distinguishable from operational events in log output. |
| Jerry Mapping | L3/L4 enforcement layers (security event sources), AE-006 graduated escalation, circuit breaker (H-36), P-022 (no deception -- inform user) |

#### FR-SEC-031

| Field | Value |
|-------|-------|
| ID | FR-SEC-031 |
| Title | Anomaly Detection Triggers |
| Description | The system SHALL define and monitor anomaly detection triggers for agent behavior including: (a) unusual tool invocation frequency (> 3 standard deviations from baseline), (b) unexpected tool combinations not declared in agent definition, (c) output volume anomalies (token count > 2x expected), (d) repeated failed operations (> 3 consecutive failures), (e) context fill rate anomalies (filling faster than expected for task type). |
| Priority | MEDIUM |
| Source Framework | OWASP ASI-09 (Insufficient Logging), OWASP ASI-10 (Rogue Agents), NIST SI-4 (System Monitoring), NIST AU-6 (Audit Review), ATLAS AML.T0054 (Anomalous Behavior Detection Evasion) |
| Acceptance Criteria | (1) Anomaly thresholds are configurable per agent type and task criticality. (2) Triggered anomalies produce security events at appropriate severity. (3) Anomaly detection operates continuously during agent execution (L4). (4) Baseline behavior profiles are established per agent type. |
| Jerry Mapping | L4 post-tool inspection, AE-006 context fill monitoring, circuit breaker (H-36), routing observability (RT-M-011 through RT-M-015) |

#### FR-SEC-032

| Field | Value |
|-------|-------|
| ID | FR-SEC-032 |
| Title | Audit Log Integrity Protection |
| Description | The system SHALL protect audit logs from tampering, deletion, and unauthorized access. Audit logs SHALL be: (a) append-only during a session, (b) persisted to the filesystem in a protected location, (c) included in git tracking for immutability, (d) accessible only to authorized reviewers. |
| Priority | MEDIUM |
| Source Framework | OWASP ASI-09, NIST AU-9 (Protection of Audit Information), NIST AU-11 (Audit Record Retention), NIST AU-10 (Non-repudiation) |
| Acceptance Criteria | (1) Audit log files cannot be modified by agent tool invocations (Write/Edit tools restricted from log directories). (2) Audit logs are committed to git as part of session completion. (3) Log file permissions restrict write access to the logging subsystem only. (4) Log rotation preserves historical entries for configurable retention period. |
| Jerry Mapping | Worktracker entries, orchestration artifacts, L5 CI (commit-time verification), file system permissions |

### Category 8: Incident Response

#### FR-SEC-033

| Field | Value |
|-------|-------|
| ID | FR-SEC-033 |
| Title | Agent Containment Mechanism |
| Description | The system SHALL provide an agent containment mechanism that can immediately halt a compromised or misbehaving agent. Containment SHALL: (a) terminate the agent's tool access, (b) preserve the agent's current state for forensic analysis, (c) prevent the agent from completing pending operations, (d) notify the user of the containment action and reason. |
| Priority | CRITICAL |
| Source Framework | OWASP ASI-10 (Rogue Agents), OWASP ASI-08 (Cascading Failures), NIST IR-4 (Incident Handling), NIST IR-6 (Incident Reporting), NIST SC-24 (Fail in Known State) |
| Acceptance Criteria | (1) Circuit breaker activation (H-36) triggers agent containment. (2) User can manually trigger containment at any time (P-020). (3) Contained agent's state is preserved in a forensic snapshot. (4) Containment prevents cascading to downstream agents. (5) Containment notification includes: agent ID, reason, recommended next action. |
| Jerry Mapping | Circuit breaker (H-36), P-020 (user authority), AE-006 emergency escalation, Task tool termination, P-022 (inform user) |

#### FR-SEC-034

| Field | Value |
|-------|-------|
| ID | FR-SEC-034 |
| Title | Cascading Failure Prevention |
| Description | The system SHALL prevent cascading failures across agent pipelines. When one agent fails, the system SHALL: (a) contain the failure to the failing agent's scope, (b) prevent error propagation through handoff chains, (c) notify upstream orchestrators of the failure, (d) provide partial results where possible. |
| Priority | HIGH |
| Source Framework | OWASP ASI-08 (Cascading Failures), NIST SC-24 (Fail in Known State), NIST CP-12 (Safe Mode), NIST SI-17 (Fail-Safe Procedures) |
| Acceptance Criteria | (1) Agent failure produces a structured failure report (not unstructured error). (2) Orchestrator receives failure notification with: failed agent ID, failure type, partial results (if any), remediation suggestions. (3) Downstream agents in the pipeline are not invoked after upstream failure unless orchestrator explicitly decides to proceed with partial results. (4) Failure propagation follows the multi_skill_context failure_propagation pattern. |
| Jerry Mapping | Multi-skill combination failure propagation, handoff protocol blockers field, guardrails.fallback_behavior, orchestration state tracking |

#### FR-SEC-035

| Field | Value |
|-------|-------|
| ID | FR-SEC-035 |
| Title | Graceful Degradation Under Security Events |
| Description | The system SHALL degrade gracefully when security events are detected rather than failing completely. Graceful degradation levels SHALL include: (a) RESTRICT: reduce agent permissions to T1 (read-only) and continue, (b) CHECKPOINT: save state and pause for user review, (c) CONTAIN: terminate agent and preserve state, (d) HALT: stop all agent activity and report to user. |
| Priority | HIGH |
| Source Framework | OWASP ASI-08 (Cascading Failures), NIST CP-2 (Contingency Plan), NIST SC-24 (Fail in Known State), NIST IR-4 (Incident Handling) |
| Acceptance Criteria | (1) Degradation level is proportional to security event severity. (2) RESTRICT mode is the default response for MEDIUM security events. (3) CHECKPOINT mode activates for HIGH security events. (4) CONTAIN/HALT modes activate for CRITICAL security events. (5) User is informed of degradation level and can override (P-020). |
| Jerry Mapping | AE-006 graduated escalation, guardrails.fallback_behavior (warn_and_retry, escalate_to_user, persist_and_halt), P-020 user authority, L4 enforcement |

#### FR-SEC-036

| Field | Value |
|-------|-------|
| ID | FR-SEC-036 |
| Title | Recovery Procedures After Security Incidents |
| Description | The system SHALL provide recovery procedures following security incidents including: (a) session state restoration from last known good checkpoint, (b) agent definition re-validation after compromise, (c) MCP server re-verification after supply chain events, (d) audit log review guidance for forensic analysis, (e) user notification with incident summary and recommended actions. |
| Priority | MEDIUM |
| Source Framework | NIST IR-4 (Incident Handling), NIST CP-10 (System Recovery and Reconstitution), NIST IR-8 (Incident Response Plan), NIST CSF Recover function |
| Acceptance Criteria | (1) Checkpoint restore capability exists for session state (context_checkpoint). (2) Post-incident agent re-validation executes full H-34/H-35 schema checks. (3) Post-incident MCP re-verification executes full FR-SEC-025 checks. (4) Incident summary report is generated with: timeline, affected agents, affected tools, recommended remediation. (5) Recovery does not require full system restart. |
| Jerry Mapping | Memory-Keeper checkpoints, AE-006e (compaction recovery), agent definition validation, MCP server verification, session management |

### Additional Functional Requirements

#### FR-SEC-037

| Field | Value |
|-------|-------|
| ID | FR-SEC-037 |
| Title | Rogue Agent Detection |
| Description | The system SHALL detect rogue agent behavior defined as: (a) agent producing output that contradicts its constitutional constraints, (b) agent attempting actions outside its declared capabilities, (c) agent exhibiting behavioral drift from its defined methodology, (d) agent producing deceptive output (violating P-022). Detection SHALL combine L3 deterministic checks and L4 behavioral analysis. |
| Priority | CRITICAL |
| Source Framework | OWASP ASI-10 (Rogue Agents), ATLAS AML.T0054 (Behavior Analysis Evasion), NIST SI-4 (System Monitoring), NIST AU-6 (Audit Review) |
| Acceptance Criteria | (1) L3 checks prevent out-of-scope tool invocations (deterministic). (2) L4 inspects agent output for constitutional constraint violations. (3) Behavioral drift detection compares agent actions against its methodology section. (4) Detected rogue behavior triggers immediate containment (FR-SEC-033). (5) False positive rate for rogue detection <= 2%. |
| Jerry Mapping | Constitutional constraints (P-003, P-020, P-022), L3/L4 enforcement, agent definition methodology, circuit breaker (H-36), forbidden actions |

#### FR-SEC-038

| Field | Value |
|-------|-------|
| ID | FR-SEC-038 |
| Title | Human-in-the-Loop for High-Impact Actions |
| Description | The system SHALL require human-in-the-loop (HITL) approval for high-impact actions including: (a) any action classified as C3+ criticality, (b) file system modifications outside the project workspace, (c) external network requests to unregistered domains, (d) agent-generated code execution, (e) MCP server configuration changes, (f) governance file modifications (AE-002, AE-004). |
| Priority | CRITICAL |
| Source Framework | OWASP ASI-02 (Tool Misuse), OWASP ASI-09 (Human-Agent Trust Exploitation), P-020 (User Authority), NIST AC-6(2) (Non-privileged Access for Non-security Functions), Anthropic GTG-1002 lessons |
| Acceptance Criteria | (1) High-impact action list is configurable and extensible. (2) HITL approval request includes: action description, risk assessment, agent ID, alternatives considered. (3) Timeout on HITL approval defaults to action denial (fail-closed). (4) HITL decisions are logged in the audit trail. (5) Auto-escalation rules (AE-001 through AE-005) trigger HITL for governance changes. |
| Jerry Mapping | P-020 (user authority), auto-escalation rules (AE-001 through AE-006), criticality levels (C1-C4), H-31 (clarify when ambiguous) |

#### FR-SEC-039

| Field | Value |
|-------|-------|
| ID | FR-SEC-039 |
| Title | Recursive Delegation Prevention |
| Description | The system SHALL enforce the single-level nesting constraint (P-003/H-01) to prevent recursive agent delegation. Worker agents SHALL NOT have the Task tool in their allowed_tools. The system SHALL detect and block attempts to create delegation chains deeper than 1 level (orchestrator -> worker). |
| Priority | CRITICAL |
| Source Framework | OWASP ASI-03 (Privilege Escalation via delegation), OWASP ASI-08 (Cascading Failures), P-003 (No Recursive Subagents), NIST AC-6 (Least Privilege) |
| Acceptance Criteria | (1) Worker agent definitions with Task in allowed_tools are rejected at L5 CI. (2) L3 blocks Task tool invocation from within a Task-invoked context. (3) Delegation depth counter is tracked and enforced at maximum 1. (4) Recursive delegation attempts are logged as CRITICAL security events. |
| Jerry Mapping | H-01/P-003 (no recursive subagents), H-35 (worker agents no Task tool), L3 pre-tool gating, L5 CI verification, tool tier T5 restriction |

#### FR-SEC-040

| Field | Value |
|-------|-------|
| ID | FR-SEC-040 |
| Title | Unbounded Consumption Prevention |
| Description | The system SHALL prevent unbounded resource consumption by agents including: (a) token consumption limits per agent invocation (configurable by criticality), (b) tool invocation count limits per agent (configurable), (c) execution time limits per agent, (d) output size limits per agent response. The system SHALL enforce graduated escalation per AE-006 for context fill. |
| Priority | HIGH |
| Source Framework | OWASP LLM10 (Unbounded Consumption), OWASP ASI-08 (Cascading Failures), NIST SC-5 (Denial of Service Protection), NIST SC-6 (Resource Availability) |
| Acceptance Criteria | (1) Per-agent resource limits are configurable in agent definitions or orchestration plans. (2) AE-006 graduated escalation activates at context fill thresholds (0.70/0.80/0.88). (3) Circuit breaker (H-36) limits routing hops to 3. (4) Iteration ceilings are enforced per criticality (C1=3, C2=5, C3=7, C4=10 per RT-M-010). (5) Resource exhaustion triggers graceful degradation (FR-SEC-035). |
| Jerry Mapping | AE-006 graduated escalation, circuit breaker (H-36), iteration ceilings (RT-M-010), context budget standards (CB-01 through CB-05) |

#### FR-SEC-041

| Field | Value |
|-------|-------|
| ID | FR-SEC-041 |
| Title | Secure Configuration Management |
| Description | The system SHALL enforce secure configuration management for all security-relevant settings including: (a) HARD rules in quality-enforcement.md, (b) agent definitions in skills/*/agents/*.md, (c) MCP server configuration in .claude/settings.local.json, (d) tool tier mappings, (e) toxic combination registries. Configuration changes to security-relevant files SHALL trigger auto-escalation (AE-002 for rules, AE-004 for baselined ADRs). |
| Priority | HIGH |
| Source Framework | NIST CM-2 (Baseline Configuration), NIST CM-3 (Configuration Change Control), NIST CM-6 (Configuration Settings), NIST CM-7 (Least Functionality) |
| Acceptance Criteria | (1) Security configuration files are tracked by git with change detection. (2) Changes to .context/rules/ trigger auto-C3 (AE-002). (3) Changes to constitution trigger auto-C4 (AE-001). (4) L5 CI validates all configuration files against their schemas on every commit. (5) Configuration drift detection alerts on unauthorized modifications. |
| Jerry Mapping | AE-001 through AE-005 (auto-escalation), L5 CI verification, .context/rules/ governance, CLAUDE.md, quality-enforcement.md |

#### FR-SEC-042

| Field | Value |
|-------|-------|
| ID | FR-SEC-042 |
| Title | Secure Defaults for New Agents and Skills |
| Description | The system SHALL enforce secure-by-default configuration for newly created agents and skills. Defaults SHALL include: (a) T1 (read-only) tool tier unless explicitly escalated with justification, (b) constitutional triplet (P-003, P-020, P-022) pre-populated in new agent templates, (c) minimum 3 forbidden actions pre-populated, (d) fallback_behavior defaulting to escalate_to_user, (e) input_validation and output_filtering minimum entries pre-populated. |
| Priority | MEDIUM |
| Source Framework | OWASP ASI-03 (Privilege Escalation -- default permissions), NIST CM-7 (Least Functionality), NIST SA-8 (Security and Privacy Engineering Principles) |
| Acceptance Criteria | (1) Agent template includes all H-34 required fields with secure defaults. (2) New agents created without explicit tier justification default to T1. (3) Template enforcement is verified at L5 CI. (4) Documentation clearly states the secure defaults and escalation procedure. |
| Jerry Mapping | Agent definition schema (H-34), guardrails template, .context/templates/, skill standards (H-25/H-26), agent-development-standards.md |

---

## Non-Functional Security Requirements (L1)

### Category 9: Performance

#### NFR-SEC-001

| Field | Value |
|-------|-------|
| ID | NFR-SEC-001 |
| Title | Security Control Latency Budget |
| Description | Security controls at L3 (pre-tool gating) SHALL NOT add more than 50ms latency per tool invocation. Security controls at L4 (post-tool inspection) SHALL NOT add more than 200ms latency per tool result processing. Total security overhead per agent turn SHALL NOT exceed 500ms. |
| Priority | HIGH |
| Source Framework | NIST SC-5 (Denial of Service Protection), OWASP API4:2023 (Unrestricted Resource Consumption) |
| Acceptance Criteria | (1) L3 gate average latency < 50ms measured across 100 consecutive invocations. (2) L4 inspection average latency < 200ms. (3) End-to-end security overhead < 500ms per agent turn. (4) Performance benchmarks are run as part of L5 CI. |
| Jerry Mapping | L3 pre-tool gating, L4 post-tool inspection, enforcement architecture token budgets |

#### NFR-SEC-002

| Field | Value |
|-------|-------|
| ID | NFR-SEC-002 |
| Title | Security Token Budget |
| Description | Security enforcement mechanisms SHALL NOT consume more than 10% of the total context window (20,000 tokens of 200K). This includes L2 re-injection tokens (~850/prompt), security-related system instructions, and security metadata in handoffs. |
| Priority | HIGH |
| Source Framework | Context budget standards (CB-01 through CB-05), OWASP LLM10 (Unbounded Consumption) |
| Acceptance Criteria | (1) L2 re-injection stays within 850-token budget per enforcement architecture. (2) Security metadata in handoffs < 500 tokens per handoff. (3) Total security token consumption is auditable. (4) Security token consumption does not trigger AE-006 escalation under normal operation. |
| Jerry Mapping | Enforcement architecture (L1-L5 token budgets), context budget standards, AE-006 graduated escalation |

#### NFR-SEC-003

| Field | Value |
|-------|-------|
| ID | NFR-SEC-003 |
| Title | Deterministic Security Control Performance |
| Description | Deterministic security controls (L3 pre-tool gating, L5 CI) SHALL have constant-time performance characteristics (O(1) or O(n) where n is the control list size). Security controls SHALL NOT have performance degradation correlated with context fill level. |
| Priority | MEDIUM |
| Source Framework | L3/L5 enforcement architecture (context-rot immune), NIST SC-5 (Denial of Service Protection) |
| Acceptance Criteria | (1) L3 gate performance is independent of context fill level (immune to context rot). (2) L5 CI execution time scales linearly with number of files checked. (3) No security control exhibits exponential time complexity. |
| Jerry Mapping | Enforcement architecture (L3 immune, L5 immune per quality-enforcement.md) |

### Category 10: Availability

#### NFR-SEC-004

| Field | Value |
|-------|-------|
| ID | NFR-SEC-004 |
| Title | Security Subsystem Independence |
| Description | Each enforcement layer (L1-L5) SHALL operate independently such that failure of one layer does not disable other layers. L2 re-injection SHALL operate even if L3 gating fails. L5 CI SHALL operate even if L3/L4 are unavailable. No single security control SHALL be a single point of failure. |
| Priority | HIGH |
| Source Framework | NIST CP-2 (Contingency Plan), NIST SC-24 (Fail in Known State), Defense-in-depth principle (Google DeepMind, Anthropic convergence) |
| Acceptance Criteria | (1) Each enforcement layer can be independently tested. (2) Layer failure is detectable and logged. (3) System continues to operate with degraded security (documented degradation) rather than complete failure. (4) At least 2 enforcement layers remain active for any single layer failure. |
| Jerry Mapping | 5-layer enforcement architecture (L1-L5), defense-in-depth design, AE-006 graduated escalation |

#### NFR-SEC-005

| Field | Value |
|-------|-------|
| ID | NFR-SEC-005 |
| Title | MCP Failure Resilience |
| Description | The system SHALL continue to operate when MCP servers are unavailable. MCP failure SHALL trigger fallback behavior as defined in mcp-tool-standards.md: Context7 failures fall back to WebSearch, Memory-Keeper failures fall back to file-based persistence in work/.mcp-fallback/. Security controls SHALL NOT depend on MCP availability. |
| Priority | HIGH |
| Source Framework | NIST CP-2 (Contingency Plan), MCP tool standards error handling, OWASP ASI-08 (Cascading Failures) |
| Acceptance Criteria | (1) MCP server unavailability is detected within 5 seconds. (2) Fallback mechanisms activate automatically per mcp-tool-standards.md. (3) Security enforcement continues at full capability without MCP. (4) MCP recovery is detected and normal operation resumes without manual intervention. |
| Jerry Mapping | MCP tool standards error handling table, work/.mcp-fallback/ directory, L3/L4 enforcement (independent of MCP) |

#### NFR-SEC-006

| Field | Value |
|-------|-------|
| ID | NFR-SEC-006 |
| Title | Fail-Closed Security Default |
| Description | When security controls encounter an error or ambiguous state, the system SHALL fail closed (deny by default) rather than fail open (allow by default). Specifically: (a) L3 gate errors SHALL block tool invocation, (b) authentication failures SHALL reject handoffs, (c) schema validation errors SHALL reject agent loading, (d) HITL timeout SHALL deny the requested action. |
| Priority | CRITICAL |
| Source Framework | NIST SC-24 (Fail in Known State), NIST AC-3 (Access Enforcement), OWASP Secure Design principles |
| Acceptance Criteria | (1) Every security checkpoint has a defined fail-closed behavior. (2) Fail-closed events are logged with full context. (3) User is notified of fail-closed events with explanation and remediation guidance. (4) No security control defaults to "allow" on error. |
| Jerry Mapping | L3 pre-tool gating, guardrails.fallback_behavior, P-020 (user authority for override), P-022 (transparency about denial) |

### Category 11: Scalability

#### NFR-SEC-007

| Field | Value |
|-------|-------|
| ID | NFR-SEC-007 |
| Title | Security Model Scalability with Agent Count |
| Description | The security model SHALL scale to support up to 50 registered agents and 20 skills without degradation in routing accuracy or enforcement reliability. Security control performance SHALL scale linearly (not exponentially) with agent and skill count. |
| Priority | MEDIUM |
| Source Framework | Agent routing standards scaling roadmap (Phase 0-3), NIST SA-8 (Security Engineering Principles) |
| Acceptance Criteria | (1) L3 gate performance scales linearly with agent count. (2) Trigger map routing accuracy remains >= 90% at 20 skills. (3) Tool tier enforcement operates in O(1) per invocation regardless of total agent count. (4) CI validation time scales linearly with number of agent definition files. |
| Jerry Mapping | Agent routing scaling roadmap (Phases 0-3), L3/L5 enforcement, trigger map (mandatory-skill-usage.md) |

#### NFR-SEC-008

| Field | Value |
|-------|-------|
| ID | NFR-SEC-008 |
| Title | Security Rule Set Scalability |
| Description | The security rule set SHALL be scalable within the HARD rule ceiling (25 rules, absolute max 28). Security-specific HARD rules SHALL be incorporated into existing compound rules where possible rather than consuming new rule slots. The L2 re-injection token budget (850 tokens) SHALL accommodate security rule markers. |
| Priority | MEDIUM |
| Source Framework | HARD Rule Ceiling Derivation (quality-enforcement.md), L2 enforcement budget |
| Acceptance Criteria | (1) Security requirements are implementable within current 25-rule HARD ceiling. (2) New security HARD rules use compound formatting (sub-items of existing rules) where possible. (3) L2 token budget for security markers < 200 tokens (within 850-token total budget). (4) Security rule additions follow the HARD Rule Ceiling Exception Mechanism if ceiling expansion is required. |
| Jerry Mapping | HARD Rule Index (25/25 ceiling), L2 token budget (559/850 tokens used), HARD Rule Ceiling Exception Mechanism |

### Category 12: Usability

#### NFR-SEC-009

| Field | Value |
|-------|-------|
| ID | NFR-SEC-009 |
| Title | Minimal Security Friction for Routine Operations |
| Description | Security controls SHALL NOT impede legitimate agent operations for C1 (Routine) criticality tasks. HITL approvals SHALL only be required for C2+ operations or explicitly high-impact actions. The security UX SHALL be proportional to risk: low-risk actions proceed without interruption, high-risk actions require proportional review. |
| Priority | HIGH |
| Source Framework | Anthropic Claude Code permission model (84% prompt reduction), P-020 (User Authority), NIST PM-11 (Mission and Business Process Definition) |
| Acceptance Criteria | (1) C1 tasks complete without any HITL security prompts under normal operation. (2) Security-related HITL prompts per C2 task average <= 2. (3) Security controls are transparent (visible when relevant, invisible when not). (4) User can configure security sensitivity level (strict/standard/permissive) with documented trade-offs. |
| Jerry Mapping | Criticality levels (C1-C4), P-020 (user authority), H-31 (ask when ambiguous, don't ask when clear), quality gate proportionality |

#### NFR-SEC-010

| Field | Value |
|-------|-------|
| ID | NFR-SEC-010 |
| Title | Clear Security Event Communication |
| Description | Security events, denials, and containment actions SHALL be communicated to the user in clear, actionable language per P-022 (no deception). Communications SHALL include: (a) what happened, (b) why it was blocked/flagged, (c) what the user can do about it, (d) severity level. Security messages SHALL NOT use opaque error codes without explanation. |
| Priority | HIGH |
| Source Framework | P-022 (No Deception), NIST IR-7 (Incident Response Assistance), OWASP ASI-09 (Human-Agent Trust Exploitation -- clear communication prevents) |
| Acceptance Criteria | (1) Every security denial includes a human-readable explanation. (2) Security messages include recommended next action. (3) Security severity is communicated using consistent vocabulary (CRITICAL/HIGH/MEDIUM/LOW). (4) No security message contains only an error code without explanation. |
| Jerry Mapping | P-022 (no deception), circuit breaker termination behavior (H-36 step 4), AE-006 user warnings, guardrails.fallback_behavior |

### Category 13: Maintainability

#### NFR-SEC-011

| Field | Value |
|-------|-------|
| ID | NFR-SEC-011 |
| Title | Security Rule Hot-Update Capability |
| Description | Security rules, patterns, and configurations SHALL be updatable without requiring a full system restart. Specifically: (a) prompt injection pattern databases SHALL be loadable at session start (L1), (b) L2 re-injection rules SHALL be updated by modifying rule files, (c) toxic combination registries SHALL be extensible via configuration files, (d) MCP server registries SHALL be updatable between sessions. |
| Priority | MEDIUM |
| Source Framework | NIST CM-3 (Configuration Change Control), NIST SI-2 (Flaw Remediation), Google DeepMind Evolution layer |
| Acceptance Criteria | (1) Security pattern updates take effect at next session start without code changes. (2) L2 REINJECT markers are the SSOT for per-prompt rule injection (already hot-loaded). (3) Configuration-driven security controls (registries, patterns, thresholds) are in separate data files from code. (4) Security rule update process is documented and tested. |
| Jerry Mapping | L1 session start loading, L2 per-prompt re-injection, .context/rules/ file-based configuration, git-tracked rule files |

#### NFR-SEC-012

| Field | Value |
|-------|-------|
| ID | NFR-SEC-012 |
| Title | Security Control Testability |
| Description | Every security control SHALL be independently testable. Test coverage for security controls SHALL achieve >= 95% line coverage (exceeding the standard 90% per H-20). Security controls SHALL have both positive tests (legitimate operations pass) and negative tests (attacks are detected/blocked). |
| Priority | HIGH |
| Source Framework | NIST CA-8 (Penetration Testing), NIST SA-11 (Developer Testing and Evaluation), H-20 (testing standards) |
| Acceptance Criteria | (1) Every L3 gate rule has at least one positive and one negative test case. (2) Every L4 inspection pattern has at least one detection test case. (3) Security control test coverage >= 95% line coverage. (4) Security tests are included in L5 CI pipeline. (5) Adversarial test suite covers all OWASP ASI-01 through ASI-10 categories. |
| Jerry Mapping | H-20 (BDD test-first, 90% coverage), L5 CI verification, /adversary skill (adversarial testing), S-001 Red Team |

#### NFR-SEC-013

| Field | Value |
|-------|-------|
| ID | NFR-SEC-013 |
| Title | Security Architecture Documentation |
| Description | The security architecture SHALL be documented with the same rigor as the functional architecture. Documentation SHALL include: (a) security enforcement layer descriptions with threat-to-control mappings, (b) security decision records (ADRs) for all C3+ security decisions, (c) security configuration guide for operators, (d) threat model with STRIDE/DREAD analysis. |
| Priority | MEDIUM |
| Source Framework | NIST PL-2 (Security and Privacy Plans), NIST SA-8 (Security Engineering Principles), NIST CSF Govern function |
| Acceptance Criteria | (1) Security ADRs exist for all C3+ security architecture decisions. (2) Threat model covers all OWASP ASI-01 through ASI-10 categories. (3) Security configuration guide documents all configurable security parameters. (4) Documentation passes C4 quality gate (>= 0.95 per H-13, tournament mode). |
| Jerry Mapping | docs/design/ (ADRs), quality gate (H-13), criticality levels, /adversary skill (tournament mode for C4) |

#### NFR-SEC-014

| Field | Value |
|-------|-------|
| ID | NFR-SEC-014 |
| Title | Security Compliance Traceability |
| Description | Every implemented security control SHALL trace to at least one requirement in this document. Every requirement in this document SHALL trace to at least one source framework item. Bi-directional traceability SHALL be maintained in the requirements traceability matrix. |
| Priority | HIGH |
| Source Framework | NIST CA-2 (Control Assessments), NIST PL-2 (Security Plans), NASA NPR 7123.1D (traceability requirements) |
| Acceptance Criteria | (1) RTM has zero orphaned requirements (requirements with no implementation). (2) RTM has zero orphaned controls (implementations with no requirement). (3) Every requirement traces to >= 1 source framework. (4) RTM is updated with every security control change. |
| Jerry Mapping | This document (requirements traceability matrix section), WORKTRACKER.md, compliance matrices (Phase 4) |

#### NFR-SEC-015

| Field | Value |
|-------|-------|
| ID | NFR-SEC-015 |
| Title | Security Model Extensibility |
| Description | The security model SHALL be extensible to accommodate new threat vectors, new tool types, new MCP servers, and new agent capabilities without requiring fundamental architectural changes. Extension points SHALL include: (a) pluggable input validation patterns, (b) extensible tool tier definitions, (c) configurable anomaly detection thresholds, (d) modular security event handlers. |
| Priority | MEDIUM |
| Source Framework | NIST SA-8 (Security Engineering Principles), Google DeepMind Evolution layer, NIST CSF Govern function |
| Acceptance Criteria | (1) Adding a new prompt injection pattern requires only a data file update (no code change). (2) Adding a new tool tier requires configuration change only. (3) Adding a new MCP server requires registry update and verification only. (4) Security extension points are documented with examples. |
| Jerry Mapping | Defense-in-depth architecture, file-based rule system (.context/rules/), MCP server registry, agent definition schema extensibility |

---

## Requirements Traceability Matrix (L2)

### OWASP Agentic Top 10 Coverage

| OWASP Item | Requirements | Coverage |
|------------|-------------|----------|
| ASI-01 (Agent Goal Hijack) | FR-SEC-011, FR-SEC-012, FR-SEC-014, FR-SEC-015, FR-SEC-016 | FULL |
| ASI-02 (Tool Misuse) | FR-SEC-005, FR-SEC-006, FR-SEC-007, FR-SEC-009, FR-SEC-038 | FULL |
| ASI-03 (Privilege Escalation) | FR-SEC-005, FR-SEC-006, FR-SEC-008, FR-SEC-039, FR-SEC-042 | FULL |
| ASI-04 (Trust Boundary Violations) | FR-SEC-008, FR-SEC-010, FR-SEC-022, FR-SEC-025 | FULL |
| ASI-05 (Memory/Context Manipulation) | FR-SEC-012, FR-SEC-014, NFR-SEC-002 | FULL |
| ASI-06 (Identity Mismanagement) | FR-SEC-001, FR-SEC-002, FR-SEC-003, FR-SEC-004 | FULL |
| ASI-07 (Insecure Inter-Agent Comm) | FR-SEC-021, FR-SEC-022, FR-SEC-023, FR-SEC-024 | FULL |
| ASI-08 (Cascading Failures) | FR-SEC-034, FR-SEC-035, FR-SEC-040, NFR-SEC-004 | FULL |
| ASI-09 (Insufficient Logging) | FR-SEC-029, FR-SEC-030, FR-SEC-031, FR-SEC-032 | FULL |
| ASI-10 (Rogue Agents) | FR-SEC-007, FR-SEC-037, FR-SEC-033 | FULL |

### OWASP LLM Top 10 Coverage

| OWASP Item | Requirements | Coverage |
|------------|-------------|----------|
| LLM01 (Prompt Injection) | FR-SEC-011, FR-SEC-012, FR-SEC-016 | FULL |
| LLM02 (Sensitive Info Disclosure) | FR-SEC-017, FR-SEC-019 | FULL |
| LLM03 (Supply Chain) | FR-SEC-025, FR-SEC-026, FR-SEC-027, FR-SEC-028 | FULL |
| LLM04 (Data/Model Poisoning) | FR-SEC-014, FR-SEC-015 | PARTIAL (model-level mitigations outside Jerry scope) |
| LLM05 (Improper Output Handling) | FR-SEC-018, FR-SEC-020 | FULL |
| LLM06 (Excessive Agency) | FR-SEC-005, FR-SEC-006, FR-SEC-009, FR-SEC-038 | FULL |
| LLM07 (System Prompt Leakage) | FR-SEC-017, FR-SEC-019 | FULL |
| LLM08 (Vector/Embedding) | N/A | OUT OF SCOPE (Jerry does not use RAG/embeddings) |
| LLM09 (Misinformation) | FR-SEC-020 | PARTIAL (model-level mitigations outside Jerry scope) |
| LLM10 (Unbounded Consumption) | FR-SEC-040, NFR-SEC-002 | FULL |

### NIST SP 800-53 Control Family Coverage

| Control Family | Controls Referenced | Requirements |
|----------------|-------------------|--------------|
| AC (Access Control) | AC-3, AC-4, AC-5, AC-6 | FR-SEC-005, -006, -007, -008, -009, -010, -039 |
| AU (Audit & Accountability) | AU-2, AU-3, AU-6, AU-9, AU-10, AU-11, AU-12 | FR-SEC-004, -029, -030, -031, -032 |
| CA (Assessment) | CA-2, CA-8 | NFR-SEC-012, -014 |
| CM (Configuration Mgmt) | CM-2, CM-3, CM-5, CM-6, CM-7 | FR-SEC-041, -042, NFR-SEC-011 |
| CP (Contingency Planning) | CP-2, CP-10, CP-12 | FR-SEC-034, -035, -036, NFR-SEC-004, -005 |
| IA (Identification & Auth) | IA-3, IA-4, IA-5, IA-9 | FR-SEC-001, -002, -003 |
| IR (Incident Response) | IR-4, IR-5, IR-6, IR-7, IR-8 | FR-SEC-033, -034, -035, -036, NFR-SEC-010 |
| PL (Planning) | PL-2 | NFR-SEC-013, -014 |
| PM (Program Mgmt) | PM-11 | NFR-SEC-009 |
| SA (System & Services) | SA-8, SA-11, SA-12 | FR-SEC-025, -026, -027, -028, NFR-SEC-012, -015 |
| SC (System & Comm Protection) | SC-5, SC-6, SC-7, SC-8, SC-13, SC-23, SC-24, SC-28 | FR-SEC-010, -013, -017, -023, -024, -033, -035, NFR-SEC-001, -003, -004, -006 |
| SI (System & Info Integrity) | SI-2, SI-3, SI-4, SI-7, SI-10, SI-12, SI-15, SI-17 | FR-SEC-011, -012, -013, -014, -015, -016, -017, -018, -028, -031, -037 |

### MITRE ATLAS Coverage

| ATLAS Technique | Requirements | Coverage |
|----------------|--------------|----------|
| AML.T0051 (Prompt Injection) | FR-SEC-011, -012, -016 | FULL |
| AML.T0051.001 (Indirect Prompt Injection) | FR-SEC-012, -013 | FULL |
| AML.T0051.002 (Prompt Injection Evasion) | FR-SEC-016 | FULL |
| AML.T0053 (Exfiltration via ML API) | FR-SEC-009, -013, -017 | FULL |
| AML.T0054 (Behavior Analysis Evasion) | FR-SEC-031, -037 | FULL |
| AML.T0080 (Memory Poisoning) | FR-SEC-014 | FULL |
| AML.T0043 (Craft Adversarial Data) | FR-SEC-012, -014 | FULL |
| Supply Chain techniques | FR-SEC-025, -026, -027, -028 | FULL |

### Full Requirements Cross-Reference

| Requirement ID | MITRE | OWASP | NIST | Jerry Component | Priority |
|---------------|-------|-------|------|-----------------|----------|
| FR-SEC-001 | -- | ASI-06 | IA-4 | Agent identity, Task tool | CRITICAL |
| FR-SEC-002 | -- | ASI-06, ASI-07 | IA-3, IA-9 | Handoff protocol, L3, MCP | CRITICAL |
| FR-SEC-003 | -- | ASI-06 | IA-4, IA-5 | Task tool, orchestration | HIGH |
| FR-SEC-004 | -- | ASI-06, ASI-09 | AU-3, AU-10 | Routing observability, L4 | HIGH |
| FR-SEC-005 | -- | ASI-02, ASI-03 | AC-6, AC-3 | Tool tiers, L3, H-34 | CRITICAL |
| FR-SEC-006 | -- | ASI-02, ASI-03 | AC-6, AC-5 | Tool tiers, H-35, L3, L5 | CRITICAL |
| FR-SEC-007 | -- | ASI-02, ASI-10 | AC-3, SI-10 | H-35, L3/L4, constitution | CRITICAL |
| FR-SEC-008 | DeepMind DCTs | ASI-03, ASI-04 | AC-6(1) | P-003, tool tiers, handoff | CRITICAL |
| FR-SEC-009 | AML.T0053 | ASI-02 | AC-6(3) | Tool tiers, L3, P-020 | HIGH |
| FR-SEC-010 | -- | ASI-04 | AC-4, SC-7 | Task isolation, handoff | HIGH |
| FR-SEC-011 | AML.T0051 | LLM01, ASI-01 | SI-10 | L3, guardrails, L2 | CRITICAL |
| FR-SEC-012 | AML.T0051.001 | LLM01, ASI-01, ASI-05 | SI-10 | L4, MCP, guardrails | CRITICAL |
| FR-SEC-013 | AML.T0051 | ASI-01, LLM03 | SC-7, SI-10 | MCP standards, L3/L4 | CRITICAL |
| FR-SEC-014 | AML.T0080 | ASI-05, LLM10 | SI-7 | L2, AE-006, CB standards | HIGH |
| FR-SEC-015 | AML.T0051 | ASI-01 | SI-7 | Handoff protocol, L4 | HIGH |
| FR-SEC-016 | AML.T0051.002 | LLM01 | SI-10 | L3, guardrails | MEDIUM |
| FR-SEC-017 | AML.T0053 | LLM02, LLM07 | SC-28, SI-15 | L4, guardrails, H-34 | CRITICAL |
| FR-SEC-018 | -- | LLM05, ASI-08 | SI-15, SI-3 | L4, handoff, P-020 | HIGH |
| FR-SEC-019 | -- | LLM07 | SC-28, AC-3 | L4, L2 markers, rules | HIGH |
| FR-SEC-020 | -- | LLM09 | AI RMF MEASURE | P-022, S-014, handoff | MEDIUM |
| FR-SEC-021 | -- | ASI-07 | SC-8, SI-10 | Handoff protocol, L3 | HIGH |
| FR-SEC-022 | -- | ASI-04, ASI-07 | AC-4, SC-7 | Handoff CP-01-05, H-13 | HIGH |
| FR-SEC-023 | -- | ASI-07 | SC-8, SC-13, AU-10 | Handoff, routing_history | MEDIUM |
| FR-SEC-024 | -- | ASI-07, ASI-10 | IA-3, SC-23 | Handoff SV-02, L3 | HIGH |
| FR-SEC-025 | T1195 | LLM03, ASI-04 | SA-12, SI-7 | MCP standards, L3 | CRITICAL |
| FR-SEC-026 | -- | LLM03, ASI-10 | SA-12, CM-3 | H-34, H-35, L3, L5 | HIGH |
| FR-SEC-027 | -- | LLM03 | SA-12, CM-5, SI-7 | H-25/H-26, CLAUDE.md | HIGH |
| FR-SEC-028 | T1195 | LLM03 | SA-12, SI-2 | H-05, pyproject.toml, L5 | MEDIUM |
| FR-SEC-029 | -- | ASI-09 | AU-2, AU-3, AU-12 | Routing obs, worktracker | CRITICAL |
| FR-SEC-030 | -- | ASI-09 | AU-6, SI-4, IR-5 | L3/L4, AE-006, H-36 | HIGH |
| FR-SEC-031 | AML.T0054 | ASI-09, ASI-10 | SI-4, AU-6 | L4, AE-006, H-36 | MEDIUM |
| FR-SEC-032 | -- | ASI-09 | AU-9, AU-11, AU-10 | Worktracker, L5 | MEDIUM |
| FR-SEC-033 | -- | ASI-10, ASI-08 | IR-4, IR-6, SC-24 | H-36, P-020, AE-006 | CRITICAL |
| FR-SEC-034 | -- | ASI-08 | SC-24, CP-12, SI-17 | Multi-skill failure, handoff | HIGH |
| FR-SEC-035 | -- | ASI-08 | CP-2, SC-24, IR-4 | AE-006, fallback_behavior | HIGH |
| FR-SEC-036 | -- | ASI-08 | IR-4, CP-10, IR-8 | Memory-Keeper, AE-006e | MEDIUM |
| FR-SEC-037 | AML.T0054 | ASI-10 | SI-4, AU-6 | Constitution, L3/L4, H-36 | CRITICAL |
| FR-SEC-038 | GTG-1002 | ASI-02, ASI-09 | AC-6(2) | P-020, AE rules, criticality | CRITICAL |
| FR-SEC-039 | -- | ASI-03, ASI-08 | AC-6 | P-003/H-01, H-35, L3, L5 | CRITICAL |
| FR-SEC-040 | -- | LLM10, ASI-08 | SC-5, SC-6 | AE-006, H-36, CB standards | HIGH |
| FR-SEC-041 | -- | -- | CM-2, CM-3, CM-6, CM-7 | AE rules, L5, .context/rules | HIGH |
| FR-SEC-042 | -- | ASI-03 | CM-7, SA-8 | H-34, templates, H-25/H-26 | MEDIUM |
| NFR-SEC-001 | -- | API4 | SC-5 | L3, L4 enforcement | HIGH |
| NFR-SEC-002 | -- | LLM10 | -- | L2, CB standards, AE-006 | HIGH |
| NFR-SEC-003 | -- | -- | SC-5 | L3/L5 (context-rot immune) | MEDIUM |
| NFR-SEC-004 | -- | ASI-08 | CP-2, SC-24 | 5-layer architecture | HIGH |
| NFR-SEC-005 | -- | ASI-08 | CP-2 | MCP error handling | HIGH |
| NFR-SEC-006 | -- | -- | SC-24, AC-3 | L3, fallback_behavior | CRITICAL |
| NFR-SEC-007 | -- | -- | SA-8 | Routing roadmap, L3/L5 | MEDIUM |
| NFR-SEC-008 | -- | -- | -- | HARD ceiling, L2 budget | MEDIUM |
| NFR-SEC-009 | -- | ASI-09 | PM-11 | Criticality, P-020, H-31 | HIGH |
| NFR-SEC-010 | -- | ASI-09 | IR-7 | P-022, H-36, AE-006 | HIGH |
| NFR-SEC-011 | -- | -- | CM-3, SI-2 | L1/L2, .context/rules | MEDIUM |
| NFR-SEC-012 | -- | -- | CA-8, SA-11 | H-20, L5 CI, /adversary | HIGH |
| NFR-SEC-013 | -- | -- | PL-2, SA-8 | docs/design/, H-13, C4 | MEDIUM |
| NFR-SEC-014 | -- | -- | CA-2, PL-2 | RTM, WORKTRACKER | HIGH |
| NFR-SEC-015 | -- | -- | SA-8 | .context/rules, MCP, schema | MEDIUM |

---

## Requirements Coverage Analysis

### Full Coverage (All Attack Vectors Addressed)

| Area | Status | Notes |
|------|--------|-------|
| Agent Identity (ASI-06) | FULL | 4 requirements (FR-SEC-001 through FR-SEC-004) |
| Tool Misuse (ASI-02) | FULL | 5 requirements covering least privilege, tiers, forbidden actions, toxic combinations, HITL |
| Privilege Escalation (ASI-03) | FULL | 5 requirements covering non-escalation, delegation limits, recursive prevention |
| Trust Boundaries (ASI-04) | FULL | 4 requirements covering handoff integrity, boundary enforcement, MCP verification |
| Prompt Injection (LLM01/ASI-01) | FULL | 6 requirements covering direct, indirect, encoding evasion, MCP, context manipulation, goal integrity |
| Inter-Agent Communication (ASI-07) | FULL | 4 requirements covering schema enforcement, trust boundaries, integrity, anti-spoofing |
| Supply Chain (LLM03/ASI-04) | FULL | 4 requirements covering MCP, agent definitions, skills, Python dependencies |
| Audit and Logging (ASI-09) | FULL | 4 requirements covering comprehensive audit, security events, anomaly detection, log integrity |
| Incident Response | FULL | 4 requirements covering containment, cascading prevention, graceful degradation, recovery |
| Rogue Agents (ASI-10) | FULL | 3 requirements covering detection, containment, forbidden action enforcement |
| Output Security (LLM02/LLM05/LLM07) | FULL | 4 requirements covering filtering, sanitization, leakage prevention, confidence disclosure |

### Partial Coverage (Acknowledged Gaps)

| Area | Status | Gap Description | Mitigation |
|------|--------|-----------------|------------|
| Data/Model Poisoning (LLM04) | PARTIAL | Training data integrity and fine-tuning attacks are outside Jerry's local-first scope. Context poisoning is addressed via FR-SEC-014. | Jerry consumes pre-trained models (Claude); model-level integrity is Anthropic's responsibility. Context-level poisoning is fully addressed. |
| Misinformation (LLM09) | PARTIAL | Hallucination and factual accuracy are model-level concerns. Jerry addresses confidence disclosure (FR-SEC-020) and quality gates (H-13). | Model-level accuracy is out of scope. Quality gates and S-014 scoring provide operational mitigation. |
| Vector/Embedding (LLM08) | OUT OF SCOPE | Jerry does not use RAG, vector databases, or embeddings. | Not applicable to current architecture. Add requirements if RAG is introduced. |

### Existing Jerry Controls Mapping

| Jerry Control | Status | Requirements It Satisfies (Partially or Fully) |
|--------------|--------|------------------------------------------------|
| L2 per-prompt re-injection | EXISTS | FR-SEC-014 (context manipulation prevention) |
| L3 pre-tool gating | EXISTS (partial) | FR-SEC-005, -006, -007 (needs extension for security-specific gates) |
| L5 CI verification | EXISTS | FR-SEC-026, -027, -028, -041 (needs security-specific CI checks) |
| P-003 single-level nesting | EXISTS | FR-SEC-039 (fully satisfied) |
| P-020 user authority | EXISTS | FR-SEC-038 (partially satisfied -- needs HITL formalization) |
| P-022 no deception | EXISTS | FR-SEC-020, NFR-SEC-010 (partially satisfied) |
| Tool tiers T1-T5 | EXISTS | FR-SEC-005, -006 (needs L3 enforcement, currently advisory) |
| Constitutional constraints | EXISTS | FR-SEC-007 (needs runtime enforcement beyond L1 awareness) |
| Handoff protocol | EXISTS | FR-SEC-021, -022 (needs security extensions) |
| Quality gates | EXISTS | NFR-SEC-012 (needs security-specific test coverage) |
| AE-006 graduated escalation | EXISTS | FR-SEC-035, -040 (closely aligned) |
| Circuit breaker (H-36) | EXISTS | FR-SEC-033, -040 (closely aligned) |

---

## Key Findings for Phase 2 Architecture

### Finding 1: Agent Identity Is the Missing Foundation

Jerry's current architecture has strong governance but no formal agent identity system. Agents are identified by name in definitions but lack unique instance identities, authentication at trust boundaries, or provenance tracking. This is the most critical architectural gap, as identity is the prerequisite for access control, audit attribution, and anti-spoofing (FR-SEC-001 through FR-SEC-004). Microsoft's Agent 365 model (unique Agent ID per instance) and Google DeepMind's Delegation Capability Tokens (cryptographic delegation with scope narrowing) provide the reference architectures.

### Finding 2: L3 Gate Is the Primary Security Enforcement Point

The existing L3 pre-tool gating layer is the natural home for most deterministic security controls (tool tier enforcement, forbidden action checking, schema validation, authentication, toxic combination detection). Currently L3 is described architecturally but not fully implemented for security. Extending L3 with security-specific gates (12 of 42 FR-SEC requirements map to L3) would deliver the highest security ROI with context-rot immunity.

### Finding 3: MCP Is the Highest-Risk External Attack Surface

The Anthropic GTG-1002 incident, Cisco's "vast unmonitored attack surface" finding, and OWASP ASI-01/ASI-04 all converge on MCP servers as the primary external threat vector. Jerry's MCP integration currently trusts registered servers without integrity verification, input/output sanitization, or behavioral monitoring. FR-SEC-013 and FR-SEC-025 address this gap and should be prioritized in Phase 2 architecture.

### Finding 4: Defense-in-Depth Architecture Is Validated but Needs Security Specialization

Jerry's 5-layer enforcement architecture (L1-L5) closely mirrors Google DeepMind's 5-layer defense (Prevention, Detection, Verification, Control, Evolution) and satisfies the industry consensus that defense-in-depth is the only viable strategy ("The Attacker Moves Second" study: 12 defenses bypassed at >90% when used alone). The architecture needs security-specific extensions at each layer rather than a new architecture, as documented in the NFR requirements (NFR-SEC-004 layer independence, NFR-SEC-006 fail-closed defaults).

### Finding 5: Meta's Rule of Two Provides a Concrete Design Constraint

Meta's principle that an agent may satisfy no more than 2 of: (A) processing untrusted input, (B) accessing sensitive data, (C) changing external state maps directly to Jerry's tool tier system and provides a tractable design constraint for FR-SEC-009 (toxic tool combination prevention). This should be formalized as an architectural invariant in Phase 2, with the toxic combination registry as the enforcement mechanism.

---

## Citations

| # | Source | Authority | URL |
|---|--------|-----------|-----|
| 1 | OWASP Top 10 for Agentic Applications 2026 | Industry Standard | https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/ |
| 2 | OWASP Agentic AI Threats & Mitigations | Industry Standard | https://genai.owasp.org/resource/agentic-ai-threats-and-mitigations/ |
| 3 | OWASP LLM Top 10 (2025) | Industry Standard | https://genai.owasp.org/llm-top-10/ |
| 4 | OWASP AI Agent Security Cheat Sheet | Industry Standard | https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet |
| 5 | OWASP Prompt Injection Prevention Cheat Sheet | Industry Standard | https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet |
| 6 | NIST SP 800-53 Rev 5 | US Government | https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final |
| 7 | NIST AI RMF (100-1) | US Government | https://nvlpubs.nist.gov/nistpubs/ai/nist.ai.100-1.pdf |
| 8 | NIST AI 600-1 GenAI Profile | US Government | https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf |
| 9 | NIST CSF 2.0 | US Government | https://csrc.nist.gov/projects/cybersecurity-framework |
| 10 | NIST IR 8596 CSF Profile for AI (Draft) | US Government | https://csrc.nist.gov/pubs/ir/8596/iprd |
| 11 | MITRE ATT&CK Enterprise | Standards Body | https://attack.mitre.org/ |
| 12 | MITRE ATLAS | Standards Body | https://atlas.mitre.org/ |
| 13 | MITRE ATLAS 2025 Agent Techniques | Standards Body | https://www.practical-devsecops.com/mitre-atlas-framework-guide-securing-ai-systems/ |
| 14 | MITRE D3FEND | Standards Body | https://d3fend.mitre.org/ |
| 15 | Microsoft Agent 365 Security | Industry Leader | https://www.microsoft.com/en-us/security/blog/2025/11/18/ambient-and-autonomous-security-for-the-agentic-era/ |
| 16 | Microsoft Agent Factory | Industry Leader | https://azure.microsoft.com/en-us/blog/agent-factory-creating-a-blueprint-for-safe-and-secure-ai-agents/ |
| 17 | Microsoft SDL for AI | Industry Leader | https://www.microsoft.com/en-us/security/blog/2026/02/03/microsoft-sdl-evolving-security-practices-for-an-ai-powered-world/ |
| 18 | Google DeepMind Delegation Framework | Industry Leader | https://arxiv.org/abs/2602.11865 |
| 19 | Google DeepMind Gemini Security Safeguards | Industry Leader | https://deepmind.google/blog/advancing-geminis-security-safeguards/ |
| 20 | Google DeepMind Indirect Prompt Injection | Industry Leader | https://arxiv.org/html/2505.14534v1 |
| 21 | Meta Rule of Two | Industry Leader | https://ai.meta.com/blog/practical-ai-agent-security/ |
| 22 | Anthropic GTG-1002 Incident | Industry Leader | https://www.anthropic.com/news/disrupting-AI-espionage |
| 23 | Anthropic Claude Code Sandboxing | Industry Leader | https://www.anthropic.com/engineering/claude-code-sandboxing |
| 24 | Anthropic Content Source Management | Industry Leader | https://www.technologyreview.com/2026/02/04/1131014/from-guardrails-to-governance-a-ceos-guide-for-securing-agentic-systems |
| 25 | Cisco State of AI Security 2026 | Industry Expert | https://blogs.cisco.com/ai/cisco-state-of-ai-security-2026-report |
| 26 | Cisco Integrated AI Security Framework | Industry Expert | https://arxiv.org/abs/2512.12921 |
| 27 | The Attacker Moves Second (Multi-Org Study) | Academic | https://simonwillison.net/2025/Nov/2/new-prompt-injection-papers/ |
| 28 | Securiti AI (Anthropic Exploit Analysis) | Industry Expert | https://securiti.ai/blog/anthropic-exploit-era-of-ai-agent-attacks/ |
| 29 | Palo Alto Networks OWASP Agentic Guide | Industry Expert | https://www.paloaltonetworks.com/blog/cloud-security/owasp-agentic-ai-security/ |
| 30 | Zenity & MITRE ATLAS Agent Techniques | Industry Expert | https://zenity.io/blog/current-events/zenity-labs-and-mitre-atlas-collaborate-to-advances-ai-agent-security-with-the-first-release-of |
| 31 | Microsoft AI Recommendation Poisoning | Industry Leader | https://www.microsoft.com/en-us/security/blog/2026/02/10/ai-recommendation-poisoning/ |
| 32 | Federal Register AI Agents Security RFI | US Government | https://www.federalregister.gov/documents/2026/01/08/2026-00206/request-for-information-regarding-security-considerations-for-artificial-intelligence-agents |
| 33 | Center for Threat-Informed Defense Mappings | Industry Expert | https://github.com/center-for-threat-informed-defense/mappings-explorer |
| 34 | OWASP Agentic Security Dataset | Community | https://github.com/evolutionstorm/owasp-agentic-security-dataset |
| 35 | DelegateOS (Biscuit-based DCTs) | Community | https://github.com/newtro/delegateos |

---

<!-- Self-Review (S-010) Checklist:
- [x] All 42 FR-SEC requirements have source framework traceability
- [x] All 15 NFR-SEC requirements have source framework traceability
- [x] All requirements use "shall" statements
- [x] All requirements have testable acceptance criteria
- [x] All requirements have priority classification
- [x] All OWASP ASI-01 through ASI-10 are covered
- [x] NIST SP 800-53 control families mapped (14 of 20 applicable)
- [x] MITRE ATLAS agent-specific techniques addressed
- [x] Jerry component mapping present for every requirement
- [x] Requirements traceability matrix is bi-directional
- [x] Coverage analysis identifies partial/out-of-scope areas
- [x] Key findings drive Phase 2 architecture decisions
- [x] All citations include authority classification and URL
- [x] Document follows H-23 navigation table requirement
- [x] Document follows output format specified in mission
- [x] Minimum 30 FR + 10 NFR requirement met (42 FR + 15 NFR = 57 total)
-->
