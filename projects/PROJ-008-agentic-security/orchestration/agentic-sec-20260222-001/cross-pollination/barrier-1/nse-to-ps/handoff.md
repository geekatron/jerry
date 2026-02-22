# Barrier 1 Handoff: NSE -> PS

> Cross-pollination from NASA-SE Pipeline Phase 1 to Problem-Solving Pipeline Phase 2
> Workflow: agentic-sec-20260222-001
> Date: 2026-02-22

## Document Sections

| Section | Purpose |
|---------|---------|
| [Handoff Metadata](#1-handoff-metadata) | Agent identifiers, criticality, confidence |
| [Key Findings](#2-key-findings) | Critical findings the PS pipeline must act on in Phase 2 |
| [Requirements Summary](#3-requirements-summary) | Synthesized requirements from nse-requirements-001 |
| [Risk Register Highlights](#4-risk-register-highlights) | Top risks from FMEA (nse-explorer-001) |
| [Architecture-Driving Requirements](#5-architecture-driving-requirements) | Requirements that MUST shape Phase 2 security architecture |
| [Research Priorities for ps-researcher-003](#6-research-priorities-for-ps-researcher-003) | Areas where industry pattern research would most benefit Jerry |
| [Compliance Framework Mapping](#7-compliance-framework-mapping) | Requirements mapped to compliance frameworks |
| [Blockers](#8-blockers) | Blockers or risks that could impact Phase 2 |
| [Artifact References](#9-artifact-references) | Full paths to all NSE Phase 1 artifacts |
| [Citations](#10-citations) | All claims traced to source artifacts |

---

## 1. Handoff Metadata

| Field | Value |
|-------|-------|
| from_agent | NSE Pipeline Phase 1 (nse-requirements-001, nse-explorer-001) |
| to_agents | ps-architect-001 (Security Architecture Design), ps-researcher-003 (Security Pattern Research) |
| criticality | C4 |
| confidence | 0.88 |
| artifacts | 3 (security requirements, risk register, gap analysis) |
| requirements_count | 57 total (42 FR-SEC + 15 NFR-SEC) |
| failure_modes_count | 60 across 10 FMEA categories |
| gaps_identified | 18 requirements with zero current coverage, 26 with partial coverage |

**Confidence rationale:** 0.88 reflects high confidence in the requirements completeness (all 10 OWASP Agentic Top 10 items traced, 14 NIST 800-53 families mapped, 8 MITRE ATLAS techniques addressed) with a minor deduction for inherent uncertainty in FMEA occurrence and detection scores, which are calibrated against industry data but not empirically validated against Jerry-specific attack campaigns.

---

## 2. Key Findings

These are the most critical findings from NSE Phase 1 that the PS pipeline MUST act on in Phase 2.

1. **Jerry's architecture is sound but its runtime enforcement is incomplete.** The 5-layer enforcement architecture (L1-L5), constitutional HARD rules, and tool tier system (T1-T5) exceed most agentic frameworks. However, defenses are concentrated at design-time (schema validation, CI gates) and behavioral layers (L1 rules, L2 re-injection), with significant gaps in runtime L3 security gates and L4 tool-output sanitization -- precisely the areas where the 2026 threat landscape demands the strongest controls. (Source: ps-analyst-001, Executive Summary)

2. **Indirect prompt injection via MCP tool results is the #1 risk (RPN 504).** MCP tool outputs enter the LLM context without content-source tagging or sanitization. The LLM cannot distinguish trusted instructions from untrusted data. This is the architectural root cause of the highest-scoring failure mode in the entire risk register. Jerry mandates MCP usage (MCP-001, MCP-002) but has no defense against poisoned responses. (Source: nse-explorer-001, R-PI-002; nse-explorer-001, V-002)

3. **Five risks exceed the CRITICAL threshold (RPN >= 400).** R-PI-002 (504), R-SC-001 (480), R-GB-001 (432), R-CF-005 (405), R-PI-003 (392). All five exploit gaps in Jerry's L3/L4 enforcement layers. The convergent conclusion across all three artifacts is that L3 and L4 are the primary security enforcement gaps. (Source: nse-explorer-001, Top 20 Risks; ps-analyst-001, Executive Summary)

4. **18 requirements have zero current Jerry coverage.** These include 9 CRITICAL-priority requirements: FR-SEC-001 (unique agent identity), FR-SEC-002 (agent authentication), FR-SEC-011 (direct injection prevention), FR-SEC-012 (indirect injection prevention), FR-SEC-013 (MCP sanitization), FR-SEC-025 (MCP integrity verification), FR-SEC-029 (audit trail), FR-SEC-033 (containment mechanism), FR-SEC-037 (rogue agent detection). (Source: ps-analyst-001, Requirements-to-Gap Mapping)

5. **L3 is the primary security enforcement point.** 12 of 42 functional requirements map to L3 (deterministic pre-tool gating). L3 is context-rot immune, zero LLM cost, and already architecturally defined but not fully implemented for security. Extending L3 delivers the highest security ROI. (Source: nse-requirements-001, Finding 2; ps-analyst-001, Decision 3)

6. **MCP supply chain is the only full GAP in the OWASP Agentic Top 10 matrix.** Jerry has PARTIAL coverage against 9 of 10 OWASP Agentic threats but zero coverage against ASI-04 (Supply Chain Vulnerabilities). No MCP server integrity verification, no allowlisted registry, no runtime monitoring. (Source: ps-analyst-001, Gap Matrix; nse-explorer-001, R-SC-001)

7. **Meta's Rule of Two provides a concrete, implementable design constraint.** An agent may satisfy no more than 2 of: (A) processing untrusted input, (B) accessing sensitive data, (C) changing external state. This maps directly to Jerry's tool tier system and provides the design constraint for FR-SEC-009 (toxic tool combination prevention). (Source: nse-requirements-001, Finding 5)

---

## 3. Requirements Summary

### Priority Distribution

| Priority | Count | Percentage | Coverage Status |
|----------|-------|------------|----------------|
| CRITICAL | 14 | 24.6% | 0 fully covered, 7 partial, 7 no coverage |
| HIGH | 25 | 43.9% | 6 fully covered, 14 partial, 5 no coverage |
| MEDIUM | 12 | 21.1% | 7 fully covered, 2 partial, 3 no coverage |
| LOW | 0 | 0% | -- |
| **CRITICAL + NFR-SEC-006** | **15** | **26.3%** | NFR-SEC-006 (Fail-Closed Default) is CRITICAL |

(Source: nse-requirements-001, Executive Summary, lines 26-31; ps-analyst-001, Requirements-to-Gap Mapping)

### CRITICAL Priority Requirements (14 total)

These 14 requirements represent the highest-impact security capabilities Jerry must implement. ps-architect-001 must ensure the Phase 2 architecture addresses all of these.

| Requirement | Title | Current Coverage | Architecture Impact |
|-------------|-------|-----------------|-------------------|
| FR-SEC-001 | Unique Agent Identity | NO COVERAGE | Foundational -- prerequisite for authentication, audit, anti-spoofing |
| FR-SEC-002 | Agent Authentication at Trust Boundaries | NO COVERAGE | Handoff protocol extension, L3 gate |
| FR-SEC-005 | Least Privilege Tool Access Enforcement | PARTIAL (tiers exist, no L3 runtime) | L3 gate -- transform advisory tiers to enforced |
| FR-SEC-006 | Tool Tier Boundary Enforcement | PARTIAL (CI-time only) | L3 gate -- runtime tier checking |
| FR-SEC-007 | Forbidden Action Enforcement | PARTIAL (H-35 schema, no runtime) | L3/L4 gate -- check forbidden actions at runtime |
| FR-SEC-008 | Privilege Non-Escalation in Delegation | PARTIAL (P-003, no intersection) | L3 -- compute permission intersection at delegation |
| FR-SEC-011 | Direct Prompt Injection Prevention | NO COVERAGE | L3 input validation -- injection pattern detection |
| FR-SEC-012 | Indirect Prompt Injection via Tool Results | NO COVERAGE | L4 Tool-Output Firewall -- highest risk reduction |
| FR-SEC-013 | MCP Server Input Sanitization | NO COVERAGE | L3/L4 -- MCP input/output filtering |
| FR-SEC-017 | Sensitive Information Output Filtering | PARTIAL (behavioral only) | L4 -- deterministic secret detection |
| FR-SEC-025 | MCP Server Integrity Verification | NO COVERAGE | L3/L5 -- hash pinning, registry, CI gate |
| FR-SEC-029 | Comprehensive Agent Action Audit Trail | NO COVERAGE | L4/L5 -- structured audit logging |
| FR-SEC-033 | Agent Containment Mechanism | NO COVERAGE | Circuit breaker extension -- forensic snapshot |
| FR-SEC-037 | Rogue Agent Detection | NO COVERAGE | L3/L4 -- behavioral anomaly detection |
| FR-SEC-038 | HITL for High-Impact Actions | PARTIAL (P-020 exists, no formalization) | L3 -- action classification (safe/destructive) |
| FR-SEC-039 | Recursive Delegation Prevention | PARTIAL (P-003/H-01 exist) | L3 -- runtime delegation depth enforcement |
| NFR-SEC-006 | Fail-Closed Security Default | PARTIAL (concept exists) | All layers -- define fail-closed for every checkpoint |

(Source: nse-requirements-001, Functional Security Requirements, lines 87-610; ps-analyst-001, Requirements-to-Gap Mapping, lines 248-305)

### Requirement Categories and Coverage

| Category | FR Count | Coverage |
|----------|----------|----------|
| 1: Agent Identity and Authentication | 4 (FR-SEC-001 to 004) | 0 COVERED, 2 PARTIAL, 2 GAP |
| 2: Authorization and Access Control | 6 (FR-SEC-005 to 010) | 0 COVERED, 6 PARTIAL |
| 3: Input Validation | 6 (FR-SEC-011 to 016) | 0 COVERED, 2 PARTIAL, 4 GAP |
| 4: Output Security | 4 (FR-SEC-017 to 020) | 0 COVERED, 4 PARTIAL |
| 5: Inter-Agent Communication | 4 (FR-SEC-021 to 024) | 0 COVERED, 4 PARTIAL |
| 6: Supply Chain Security | 4 (FR-SEC-025 to 028) | 0 COVERED, 1 PARTIAL, 3 GAP |
| 7: Audit and Logging | 4 (FR-SEC-029 to 032) | 0 COVERED, 0 PARTIAL, 4 GAP |
| 8: Incident Response | 4 (FR-SEC-033 to 036) | 0 COVERED, 1 PARTIAL, 3 GAP |
| Additional FR | 6 (FR-SEC-037 to 042) | 0 COVERED, 4 PARTIAL, 2 GAP |
| Non-Functional | 15 (NFR-SEC-001 to 015) | 13 COVERED, 2 PARTIAL |

(Source: nse-requirements-001, Requirements Coverage Analysis, lines 933-975; ps-analyst-001, Requirements-to-Gap Mapping, lines 248-325)

### The 18 Urgent Requirements (Zero Current Coverage)

These 18 requirements address functionality that does not exist in Jerry today. ps-architect-001 must ensure the Phase 2 architecture creates the foundational capabilities for all of these.

| Requirement | Title | Priority | Gap Category |
|-------------|-------|----------|-------------|
| FR-SEC-001 | Unique Agent Identity | CRITICAL | No cryptographic agent instance identity |
| FR-SEC-002 | Agent Authentication at Trust Boundaries | CRITICAL | No authentication mechanism at handoffs or MCP |
| FR-SEC-011 | Direct Prompt Injection Prevention | CRITICAL | No L3 input validation for injection patterns |
| FR-SEC-012 | Indirect Prompt Injection Prevention via Tool Results | CRITICAL | No L4 tool-output scanning for injection |
| FR-SEC-013 | MCP Server Input Sanitization | CRITICAL | No MCP input/output sanitization |
| FR-SEC-025 | MCP Server Integrity Verification | CRITICAL | No MCP verification mechanism |
| FR-SEC-029 | Comprehensive Agent Action Audit Trail | CRITICAL | No tool execution audit trail beyond routing records |
| FR-SEC-033 | Agent Containment Mechanism | CRITICAL | No containment beyond circuit breaker |
| FR-SEC-037 | Rogue Agent Detection | CRITICAL | No runtime behavioral anomaly detection |
| FR-SEC-003 | Agent Identity Lifecycle Management | HIGH | No agent lifecycle tracking |
| FR-SEC-004 | Agent Provenance Tracking | HIGH | No provenance chain for agent actions |
| FR-SEC-009 | Toxic Tool Combination Prevention | HIGH | No toxic combination registry |
| FR-SEC-015 | Agent Goal Integrity Verification | HIGH | No runtime goal consistency checking |
| FR-SEC-019 | System Prompt Leakage Prevention | HIGH | No L4 output filter for system prompt content |
| FR-SEC-030 | Security Event Logging | HIGH | No security-specific event logging |
| FR-SEC-023 | Message Integrity in Handoff Chains | MEDIUM | No cryptographic integrity on handoffs |
| FR-SEC-031 | Anomaly Detection Triggers | MEDIUM | No behavioral anomaly detection thresholds |
| FR-SEC-036 | Recovery Procedures After Security Incidents | MEDIUM | No formal incident recovery procedures |

(Source: ps-analyst-001, Requirements-to-Gap Mapping, lines 248-271)

---

## 4. Risk Register Highlights

### Top 10 Failure Modes by RPN

| Rank | Risk ID | Failure Mode | S | O | D | RPN | Category | Required Action |
|------|---------|-------------|---|---|---|-----|----------|----------------|
| 1 | R-PI-002 | Indirect prompt injection via MCP tool results | 9 | 8 | 7 | **504** | Prompt Injection | CRITICAL: Tool-Output Firewall (L4) |
| 2 | R-SC-001 | Malicious MCP server packages | 10 | 8 | 6 | **480** | Supply Chain | CRITICAL: MCP supply chain verification |
| 3 | R-GB-001 | Constitutional circumvention via context rot | 10 | 6 | 7.2 | **432** | Governance Bypass | CRITICAL: Promote Tier B rules; session partitioning |
| 4 | R-CF-005 | False negative in security controls | 9 | 5 | 9 | 405 | Cascading Failures | CRITICAL: Adversarial testing program |
| 5 | R-PI-003 | Indirect prompt injection via file contents | 9 | 7 | 6 | **392** | Prompt Injection | CRITICAL: L4 content scanning on Read results |
| 6 | R-PI-005 | Goal hijacking via progressive context manipulation | 8 | 6 | 8 | 384 | Prompt Injection | HIGH: Session-level behavioral drift detection |
| 7 | R-AM-001 | Agent goal hijacking through poisoned context | 9 | 7 | 6 | **378** | Agent Manipulation | HIGH: Goal consistency monitoring (L4) |
| 8 | R-SC-002 | Dependency poisoning via compromised packages | 9 | 6 | 7 | 378 | Supply Chain | HIGH: Dependency verification, SCA scanning |
| 9 | R-SC-004 | Context7 library data poisoning | 8 | 5 | 8 | 320 | Supply Chain | HIGH: Source verification layer |
| 10 | R-AM-003 | Memory/context manipulation via Memory-Keeper | 8 | 5 | 8 | 320 | Agent Manipulation | HIGH: Integrity verification on stored data |

(Source: nse-explorer-001, Top 20 Risks by RPN Score, lines 293-317)

### Risk Category Distribution

| Category | Failure Modes | Avg RPN | Top Risk | Key Insight |
|----------|---------------|---------|----------|-------------|
| 1: Prompt Injection | 6 | 333 | R-PI-002 (504) | Indirect injection via data channels dominates; L2 resilient to direct only |
| 2: Privilege Escalation | 6 | 208 | R-PE-005 (288) | MCP-based escalation and handoff accumulation are primary gaps |
| 3: Supply Chain | 6 | 268 | R-SC-001 (480) | MCP is the #1 supply chain threat; Context7 poisoning is Jerry-specific |
| 4: Data Exfiltration | 6 | 265 | R-DE-002 (294) | System prompt exposure and cross-agent leakage; no deterministic DLP |
| 5: Agent Manipulation | 6 | 241 | R-AM-001 (378) | Gap between schema validation (H-34) and runtime behavioral enforcement |
| 6: Inter-Agent Communication | 6 | 235 | R-IC-003 (294) | MEDIUM-tier data minimization not enforced at L3; no crypto in handoffs |
| 7: Infrastructure | 6 | 215 | R-IT-006 (300) | Bash unrestricted execution is single most powerful attack surface |
| 8: Governance Bypass | 6 | 231 | R-GB-001 (432) | Tier B rules vulnerable to context rot; quality gate LLM-as-Judge manipulable |
| 9: Cascading Failures | 6 | 252 | R-CF-005 (405) | Defense-in-depth still has inherent false-negative gaps; handoff quality degradation |
| 10: Identity and Access | 6 | 196 | R-IA-006 (245) | No cryptographic agent identity; string-name identification spoofable |

(Source: nse-explorer-001, Category Summaries throughout Risk Register, lines 122-289)

### Jerry-Specific Vulnerabilities (V-001 through V-006)

These are vulnerabilities specific to Jerry's architecture that do not apply to generic agentic frameworks. ps-architect-001 must address each.

| ID | Vulnerability | Severity | Root Cause |
|----|--------------|----------|------------|
| V-001 | **L2 Re-Injection Gap (Tier B Rules):** 5 of 25 HARD rules (H-04, H-16, H-17, H-18, H-32) rely on compensating controls that degrade at high context fill. H-18 (constitutional compliance check) is the most dangerous gap. | HIGH | Two-Tier enforcement model; Tier B rules not L2-protected |
| V-002 | **MCP Tool Output Channel:** MCP tool outputs enter LLM context without content-source tagging or sanitization. The LLM cannot distinguish trusted instructions from untrusted MCP data. Root cause of R-PI-002 (RPN 504). | CRITICAL | Instruction/data confusion; no Tool-Output Firewall |
| V-003 | **Bash Tool Unrestricted Execution:** No command allowlisting, blocklisting, or argument sanitization. Any T2+ agent can execute arbitrary commands including network operations and env var inspection. Single most powerful attack surface. | CRITICAL | No per-command restriction within Bash tool |
| V-004 | **Handoff Protocol Lacks Cryptographic Integrity:** Handoff data is plain text/YAML with no signing, hashing, or authentication. `from_agent` can be spoofed. Artifact paths can be redirected. | HIGH | No crypto infrastructure in handoff protocol |
| V-005 | **Quality Gate LLM-as-Judge Vulnerability:** S-014 scorer is itself an LLM agent whose scoring can be influenced by crafted deliverable content. Particularly dangerous for security deliverables. | MEDIUM | LLM-based scoring inherently manipulable |
| V-006 | **Filesystem as Infinite Memory (Persistence Threat):** File system contains complete accumulated knowledge, all rules, enforcement gaps, quality thresholds. High-value target. | MEDIUM | Core design principle creates concentrated attack target |

(Source: nse-explorer-001, Jerry-Specific Vulnerabilities, lines 372-434)

### Prioritized Mitigation Recommendations (Top 10)

These are the risk register's recommended mitigation actions, ordered by aggregate RPN impact across addressed failure modes.

| Priority | Action | Addressed Risks | Aggregate RPN | Layer |
|----------|--------|----------------|---------------|-------|
| 1 | **Tool-Output Firewall (L4):** Sanitize all MCP/Read outputs; content-source tagging | R-PI-002, R-PI-003, R-SC-004, R-AM-003 | 1,636 | L4 |
| 2 | **MCP Supply Chain Verification:** Hash pinning, allowlisted registry, L5 CI gate | R-SC-001, R-PE-005, R-IT-001, R-IT-005 | 1,198 | L3/L5 |
| 3 | **Bash Tool Hardening (L3):** Command classification, allowlisting, arg sanitization | R-PE-003, R-PE-006, R-DE-006, R-IT-003, R-IT-006 | 1,285 | L3 |
| 4 | **Handoff Integrity Protocol:** Crypto hashing, data classification, provenance | R-IC-001, R-IC-002, R-IC-003, R-DE-004, R-IA-001 | 1,380 | L3/L4 |
| 5 | **Context Rot Security Hardening:** Promote H-18 to Tier A; session partitioning | R-GB-001, R-CF-003, R-PI-005 | 1,131 | L2/L4 |
| 6 | **Runtime Tool Access Matrix (L3):** Enforce tool-tier at every invocation | R-PE-001, R-PE-004, R-AM-002 | 508 | L3 |
| 7 | **Secret Detection and DLP (L4):** Regex-based credential scanning on all output | R-DE-001, R-DE-003, R-DE-005, R-PE-006 | 1,025 | L4 |
| 8 | **Goal Consistency / Behavioral Monitoring (L4):** Track agent actions vs. declared task | R-AM-001, R-AM-004, R-AM-005, R-GB-004 | 1,054 | L4 |
| 9 | **Adversarial Testing Program:** Red team exercises, canary attacks, detection rates | R-CF-005, R-GB-002, R-CF-004 | 765 | L5 |
| 10 | **Agent Identity and Authentication:** Crypto identity tokens, delegation tokens | R-IA-001, R-IA-002, R-IA-006 | 693 | L3/L4 |

(Source: nse-explorer-001, Recommended Risk Mitigation Priorities, lines 438-455)

---

## 5. Architecture-Driving Requirements

These requirements and findings MUST shape ps-architect-001's Phase 2 security architecture design. They are organized by the architectural capability they demand.

### 5.1 L3 Gate Requirements (12 of 42 FR map to L3)

L3 (deterministic pre-tool gating) is the primary security enforcement point. It is context-rot immune, zero LLM cost, and already architecturally defined. The following requirements demand L3 implementation.

| Requirement | L3 Security Gate Function |
|-------------|--------------------------|
| FR-SEC-005 | Verify tool invocation against agent's `allowed_tools` list |
| FR-SEC-006 | Verify tool is within agent's declared tier (T1-T5) |
| FR-SEC-007 | Check tool invocation patterns against `forbidden_actions` |
| FR-SEC-008 | Compute permission intersection: MIN(orchestrator_tier, worker_tier) at delegation |
| FR-SEC-009 | Check agent's full tool set against toxic combination registry (Rule of Two) |
| FR-SEC-011 | Classify user input for injection patterns before LLM processing |
| FR-SEC-013 | Sanitize data sent to MCP servers (no system prompts, REINJECT markers, credentials) |
| FR-SEC-025 | Verify MCP server identity against approved registry; config checksum verification |
| FR-SEC-026 | Validate agent definition schema (H-34) at runtime before Task invocation |
| FR-SEC-027 | Validate SKILL.md existence and format; detect uncommitted modifications |
| FR-SEC-039 | Block Task tool invocation from within Task-invoked context (delegation depth = 1) |
| NFR-SEC-006 | All L3 gate errors MUST fail-closed (deny by default) |

**Key design constraint:** NFR-SEC-001 requires L3 gates add no more than 50ms latency per tool invocation. These must be deterministic checks (pattern matching, list lookup, hash comparison), not LLM-based.

(Source: nse-requirements-001, Finding 2, lines 984-987; acceptance criteria throughout Category 2-6 requirements)

### 5.2 L4 Tool-Output Firewall Requirements

L4 (post-tool inspection) is where the Tool-Output Firewall must operate. This addresses the #1 risk (R-PI-002, RPN 504).

| Requirement | L4 Security Inspection Function |
|-------------|--------------------------------|
| FR-SEC-012 | Scan tool results for embedded instruction patterns before LLM consumption |
| FR-SEC-017 | Filter output to prevent disclosure of system prompts, credentials, REINJECT markers |
| FR-SEC-018 | Sanitize output consumed by downstream agents (injection prevention, path validation) |
| FR-SEC-019 | Detect system prompt extraction techniques; redact rule content in output |
| FR-SEC-029 | Structured audit logging of all tool invocations and security events |
| FR-SEC-030 | Security event logging (injection detection, access violations, anomalies) |
| FR-SEC-031 | Anomaly detection triggers (tool frequency, unexpected combinations, volume anomalies) |
| FR-SEC-037 | Rogue agent detection (constitutional violation, out-of-scope actions, behavioral drift) |

**Key design constraint:** NFR-SEC-001 requires L4 inspection add no more than 200ms latency per tool result. Pattern-matching approaches (regex-based credential scanning, instruction pattern detection) satisfy this. LLM-based behavioral analysis may require sampling rather than exhaustive checking.

(Source: nse-requirements-001, acceptance criteria throughout Category 3-4, 7-8; ps-analyst-001, Decisions 1 and 5)

### 5.3 Zero-Trust Requirements

The architecture must treat all data channels as untrusted, including internal handoffs.

| Requirement | Zero-Trust Principle |
|-------------|---------------------|
| FR-SEC-002 | Authenticate agent identity at every trust boundary |
| FR-SEC-012 | Treat all tool results as untrusted input |
| FR-SEC-013 | Treat all MCP server responses as untrusted; heightened scrutiny for external |
| FR-SEC-022 | Enforce trust boundaries at every handoff (criticality non-decrease, artifact validation) |
| FR-SEC-024 | System-set `from_agent` (not agent-supplied) to prevent spoofing |
| FR-SEC-010 | Enforce permission boundaries between skills; no cross-skill state access |

(Source: nse-requirements-001, Categories 1-2 and 5)

### 5.4 Supply Chain Verification Requirements

| Requirement | Verification Mechanism |
|-------------|----------------------|
| FR-SEC-025 | MCP server identity + config checksum + approved registry |
| FR-SEC-026 | Agent definition schema + constitutional compliance + file integrity at L3 |
| FR-SEC-027 | Skill file existence + format validation + uncommitted modification detection |
| FR-SEC-028 | UV lockfile integrity + CVE scanning in CI + hash verification |

(Source: nse-requirements-001, Category 6, lines 387-435)

### 5.5 Audit and Observability Requirements

| Requirement | Audit Capability |
|-------------|-----------------|
| FR-SEC-004 | Complete provenance chain: user -> orchestrator -> agent -> tool (append-only) |
| FR-SEC-029 | Structured audit of every tool invocation, handoff, routing decision, security event |
| FR-SEC-030 | Security event sub-log with severity classification and immediate CRITICAL notification |
| FR-SEC-031 | Behavioral anomaly detection with configurable thresholds per agent type |
| FR-SEC-032 | Tamper-evident log storage; Write tool restricted from audit directories |

(Source: nse-requirements-001, Category 7, lines 437-485)

### 5.6 The L3/L4 Runtime Enforcement Gap (Critical Finding)

**This is the single most important architectural finding from Phase 1.**

Jerry's current security posture by enforcement layer:

| Layer | Current State | Security Gap |
|-------|--------------|-------------|
| L1 (session start) | Rules loaded; behavioral foundation | Vulnerable to context rot |
| L2 (every prompt) | 20 Tier A rules re-injected; immune to context rot | 5 Tier B rules not protected |
| **L3 (pre-tool)** | **Architecturally defined but NOT security-implemented** | **12 FR-SEC requirements need L3 gates** |
| **L4 (post-tool)** | **Advisory inspection only; no security-specific filtering** | **8 FR-SEC requirements need L4 inspection** |
| L5 (CI/commit) | Schema validation, linting | Needs MCP config validation, security-specific checks |

The gap analysis (ps-analyst-001) found that 0 of 10 OWASP Agentic Top 10 items have COVERED status. All are PARTIAL or GAP. The consistent pattern: design-time controls exist (schema, CI) but runtime enforcement (L3/L4 security gates) is missing.

(Source: ps-analyst-001, Gap Matrix, lines 57-72; Executive Summary, line 29)

---

## 6. Research Priorities for ps-researcher-003

The following research areas would most benefit Jerry's Phase 2 security architecture. Priorities are ordered by aggregate RPN impact of the gaps they address.

### Priority 1: Tool-Output Firewall Patterns (Aggregate RPN: 1,636)

**Research focus:** Industry approaches to sanitizing tool/function results before they enter LLM context. How do production agentic systems distinguish instruction channels from data channels?

**Key questions:**
- What content-source tagging schemes exist? (Microsoft AI Prompt Shield, Google DeepMind input/output firewalls)
- What regex/pattern-matching approaches detect instruction-like content in data channels?
- What are the false positive rates for instruction detection in legitimate technical documentation?
- How does Anthropic's Claude Code handle indirect injection via file contents?

**Source requirements:** FR-SEC-012 (indirect injection), FR-SEC-013 (MCP sanitization)
(Source: nse-explorer-001, R-PI-002 recommended action; ps-analyst-001, Decision 1)

### Priority 2: MCP Supply Chain Verification Approaches (Aggregate RPN: 1,198)

**Research focus:** Mechanisms for verifying MCP server integrity, from hash pinning to runtime behavioral monitoring.

**Key questions:**
- What does Cisco's open-source MCP security scanner detect? Can it integrate into L5 CI?
- What hash pinning schemes work for MCP server configurations?
- How does OWASP MCP Top 10 recommend verifying server identity?
- What runtime integrity monitoring is feasible for local MCP server processes?

**Source requirements:** FR-SEC-025 (MCP integrity), FR-SEC-026 (dependency verification)
(Source: nse-explorer-001, R-SC-001 recommended action; ps-analyst-001, Decision 2)

### Priority 3: Bash Tool Hardening Techniques (Aggregate RPN: 1,285)

**Research focus:** Command classification, sandboxing, and argument sanitization approaches for shell execution in agentic environments.

**Key questions:**
- How does Anthropic's Claude Code sandbox restrict shell commands? (bubblewrap/seatbelt isolation)
- What command allowlisting approaches are used in production CI/CD systems?
- How can shell metacharacter injection be prevented in dynamically constructed commands?
- What environment variable sandboxing mechanisms are available per OS?

**Source requirements:** FR-SEC-009 (toxic combinations), FR-SEC-038 (HITL for high-impact)
(Source: nse-explorer-001, V-003; ps-analyst-001, Decision 4)

### Priority 4: Runtime Agent Identity Models (Aggregate RPN: 693)

**Research focus:** Lightweight agent identity and delegation mechanisms suitable for local-first agentic frameworks.

**Key questions:**
- How does Microsoft Entra Agent ID implement per-instance identity without centralized infrastructure?
- How do Google DeepMind's Delegation Capability Tokens (Macaroons/Biscuits) narrow scope?
- What is the minimum viable agent identity for a local-first framework? (name-timestamp-nonce?)
- How can delegation tokens be verified without a central authority?

**Source requirements:** FR-SEC-001 through FR-SEC-004 (identity and authentication)
(Source: nse-requirements-001, Finding 1; ps-analyst-001, Decision 9)

### Priority 5: Comprehensive Audit Trail Architectures (Aggregate RPN: 939)

**Research focus:** Structured audit logging for multi-agent systems, including tamper-evident storage and forensic analysis capabilities.

**Key questions:**
- What structured logging formats are used in agentic platforms? (JSON-lines, OpenTelemetry?)
- How do existing frameworks achieve tamper-evident log storage without a centralized service?
- What forensic snapshot capabilities exist for preserving agent state at containment time?
- How does Microsoft's Cloud Adoption Framework for AI Agents handle observability?

**Source requirements:** FR-SEC-029 through FR-SEC-032 (audit and logging)
(Source: nse-requirements-001, Category 7; ps-analyst-001, Decision 8)

### Priority 6: Meta's Rule of Two Implementation Patterns

**Research focus:** Practical implementation of the Rule of Two constraint in tool tier systems.

**Key questions:**
- How does Meta implement the "no more than 2 of 3" constraint operationally?
- What toxic combination registries exist in production agent platforms?
- How can the constraint be expressed as an L3 gate check?

**Source requirements:** FR-SEC-009 (toxic tool combination prevention)
(Source: nse-requirements-001, Finding 5, lines 996-998)

---

## 7. Compliance Framework Mapping

### OWASP Agentic Top 10 Coverage

| OWASP Item | Requirements | Jerry Coverage Status |
|------------|-------------|---------------------|
| ASI-01 Agent Goal Hijack | FR-SEC-011, -012, -014, -015, -016 | PARTIAL: L2 re-injection helps; no L3 input validation, no L4 tool-output scanning |
| ASI-02 Tool Misuse | FR-SEC-005, -006, -007, -009, -038 | PARTIAL: Tiers defined, not runtime-enforced |
| ASI-03 Privilege Escalation | FR-SEC-005, -006, -008, -039, -042 | PARTIAL: P-003 strong; no runtime tier enforcement |
| ASI-04 Supply Chain | FR-SEC-008, -010, -022, -025 | **GAP: No MCP verification exists** |
| ASI-05 Code Execution | FR-SEC-012, -014, NFR-SEC-002 | PARTIAL: No Bash command filtering |
| ASI-06 Memory/Context Poisoning | FR-SEC-001, -002, -003, -004 | PARTIAL: No agent identity system |
| ASI-07 Inter-Agent Communication | FR-SEC-021, -022, -023, -024 | PARTIAL: Schema defined, not L3-enforced |
| ASI-08 Cascading Failures | FR-SEC-034, -035, -040, NFR-SEC-004 | PARTIAL: Circuit breaker exists; no containment mechanism |
| ASI-09 Insufficient Logging | FR-SEC-029, -030, -031, -032 | PARTIAL: Routing observability only; no tool/security audit |
| ASI-10 Rogue Agents | FR-SEC-007, -037, -033 | PARTIAL: Constitutional triplet in agents; no runtime detection |

**Result:** 0 of 10 COVERED, 9 of 10 PARTIAL, 1 of 10 GAP.
(Source: ps-analyst-001, Gap Matrix, lines 57-72)

### MITRE ATLAS Agent Technique Coverage

| Technique | Requirements | Jerry Coverage |
|-----------|-------------|---------------|
| AML.T0080 Context Poisoning | FR-SEC-014 | PARTIAL (L2 resilient; no runtime integrity verification) |
| AML.T0080.000 Memory Poisoning | FR-SEC-014 | GAP (no Memory-Keeper integrity checks) |
| AML.T0080.001 Thread Poisoning | FR-SEC-012, -014 | PARTIAL (L2 re-injection; no tool-result scanning) |
| AML.T0081 Modify Agent Config | FR-SEC-041 | PARTIAL (git + L5 CI; no runtime drift detection) |
| AML.T0082 RAG Credential Harvesting | FR-SEC-017 | PARTIAL (behavioral guardrail; no deterministic scan) |
| AML.T0083 Credentials from Config | FR-SEC-025, -041 | GAP (MCP configs contain tokens; no secret scan) |
| AML.T0084 Discover Agent Config | FR-SEC-027 | GAP (all config files accessible via Read tool) |
| AML.T0084.002 Discover Triggers | -- | GAP (trigger map in plaintext, by design) |
| AML.T0086 Exfiltration via Tool | FR-SEC-009, -013, -017 | PARTIAL (tool tier exists; no network filtering) |

**Result:** 0 of 9 COVERED, 5 of 9 PARTIAL, 4 of 9 GAP. The ATLAS gaps concentrate in credential and configuration discovery.
(Source: ps-analyst-001, Gap Matrix, lines 92-105)

### NIST SP 800-53 Control Families (Key Gaps)

| Family | Status | Key Gap |
|--------|--------|---------|
| AC (Access Control) | PARTIAL | No runtime L3 enforcement of tool tiers |
| **AU (Audit)** | **GAP** | **No comprehensive tool execution audit trail** |
| CM (Configuration Mgmt) | PARTIAL | No runtime config integrity monitoring |
| **IA (Identification)** | **GAP** | **No cryptographic agent identity or authentication** |
| IR (Incident Response) | PARTIAL | No formal IR procedures, no containment beyond circuit breaker |
| SC (System Protection) | PARTIAL | No network egress filtering, no MCP transport security |
| SI (System Integrity) | PARTIAL | No runtime input validation (L3 gate), no output sanitization (L4) |
| **SR (Supply Chain)** | **GAP** | **No MCP verification, no dependency vulnerability scanning** |
| RA (Risk Assessment) | COVERED | This FMEA risk register satisfies RA requirements |

(Source: ps-analyst-001, Gap Matrix, lines 107-122)

---

## 8. Blockers

### Active Blockers

| # | Blocker | Impact | Mitigation |
|---|---------|--------|------------|
| B-001 | **No L3 runtime security infrastructure exists.** 12 FR-SEC requirements map to L3 but no security-specific L3 gate code exists today. L3 is architecturally defined in quality-enforcement.md but implemented only for tool-call routing, not security enforcement. | Phase 2 architecture must DESIGN the L3 security gate infrastructure before any L3-dependent requirement can be implemented in Phase 3. | ps-architect-001 must treat the L3 Security Gate as Decision 3 (foundational infrastructure). |
| B-002 | **No agent instance identity mechanism.** Agent identity (FR-SEC-001) is a prerequisite for authentication (FR-SEC-002), audit attribution (FR-SEC-029), handoff integrity (FR-SEC-023), and anti-spoofing (FR-SEC-024). Without identity, 5+ downstream requirements are blocked. | ps-architect-001 must design at minimum a lightweight identity scheme (name-timestamp-nonce) as a Phase 2 architectural decision. | Defer full cryptographic identity (Microsoft Entra-equivalent) to Phase 3; design the interface and namespace now. |
| B-003 | **HARD rule ceiling at 25/25 with zero headroom.** Security requirements may need new HARD rules but the ceiling is full. L2 token budget has 291 tokens remaining (~6 additional markers). | Security architecture must be expressible within existing HARD rules (compound sub-items) or use the ceiling exception mechanism (max N=3 temporary slots, 3-month duration). | ps-architect-001 must validate that security controls fit within existing H-34/H-35/H-36 compound rules or propose ceiling exception ADR. |

### Risks to Phase 2

| # | Risk | Likelihood | Impact | Mitigation |
|---|------|-----------|--------|------------|
| R-001 | L3/L4 security gates may conflict with existing non-security L3/L4 behavior | MEDIUM | Phase 2 architecture may need to reconcile security gates with existing enforcement patterns | ps-architect-001 should explicitly design the security extension points within L3/L4, not replace them |
| R-002 | Token budget for security metadata may push context fill beyond AE-006 thresholds in long sessions | LOW | Security overhead could reduce available context for actual work | NFR-SEC-002 caps security token consumption at 10% (20K of 200K). ps-architect-001 must verify compliance |
| R-003 | Industry patterns from ps-researcher-003 may reveal approaches incompatible with Jerry's local-first architecture | MEDIUM | Some recommended patterns (centralized identity servers, cloud-based audit) won't apply | ps-researcher-003 should filter for local-first compatible patterns; ps-architect-001 should design local-first adaptations |

---

## 9. Artifact References

| Artifact | Path | Description |
|----------|------|-------------|
| Security Requirements | `orchestration/agentic-sec-20260222-001/nse/phase-1/nse-requirements-001/nse-requirements-001-security-requirements.md` | 1,061 lines. 57 security requirements (42 FR-SEC + 15 NFR-SEC) with full traceability to OWASP, MITRE ATLAS, NIST 800-53, and Jerry components. Includes RTM, coverage analysis, and 5 key findings. |
| Risk Register (FMEA) | `orchestration/agentic-sec-20260222-001/nse/phase-1/nse-explorer-001/nse-explorer-001-risk-register.md` | 499 lines. 60 FMEA failure modes across 10 categories with S/O/D scoring. Top 20 by RPN, risk heat map, Jerry-specific vulnerabilities (V-001 to V-006), and 10 prioritized mitigation actions. |
| Gap Analysis | `orchestration/agentic-sec-20260222-001/ps/phase-1/ps-analyst-001/ps-analyst-001-gap-analysis.md` | 530 lines. Comprehensive threat-to-control mapping across OWASP Agentic (10), OWASP LLM (10), MITRE ATLAS (9), NIST 800-53 (10 families). 57 requirements mapped to gap status. 15 prioritized gaps with composite scoring. 10 architecture decisions with dependency map. |

---

## 10. Citations

All claims in this handoff document trace to specific sections of the three input artifacts.

| Claim | Source Artifact | Location |
|-------|----------------|----------|
| "57 total security requirements (42 FR + 15 NFR)" | nse-requirements-001 | Executive Summary, line 26 |
| "14 CRITICAL priority requirements" | nse-requirements-001 | Executive Summary, line 27 |
| "All 10 OWASP Agentic Top 10 items traced to at least one requirement" | nse-requirements-001 | Executive Summary, line 28 |
| "60 FMEA failure modes across 10 categories" | nse-explorer-001 | Executive Summary, line 39 |
| "R-PI-002: Indirect prompt injection via MCP tool results, RPN 504" | nse-explorer-001 | Category 1, line 130 |
| "R-SC-001: Malicious MCP server packages, RPN 480" | nse-explorer-001 | Category 3, line 163 |
| "R-GB-001: Constitutional circumvention via context rot, RPN 432" | nse-explorer-001 | Category 8, line 248 |
| "R-CF-005: False negative in security controls, RPN 405" | nse-explorer-001 | Category 9, line 269 |
| "R-PI-003: Indirect prompt injection via file contents, RPN 392" | nse-explorer-001 | Category 1, line 131 |
| "V-001 through V-006 Jerry-specific vulnerabilities" | nse-explorer-001 | Jerry-Specific Vulnerabilities, lines 372-434 |
| "Top 10 mitigation priorities with aggregate RPNs" | nse-explorer-001 | Recommended Risk Mitigation Priorities, lines 438-455 |
| "0/10 OWASP Agentic Top 10 COVERED, 9/10 PARTIAL, 1/10 GAP" | ps-analyst-001 | Gap Matrix, line 72 |
| "18 requirements with no current coverage" | ps-analyst-001 | Requirements-to-Gap Mapping, lines 248-271 |
| "26 requirements with partial coverage" | ps-analyst-001 | Requirements-to-Gap Mapping, lines 273-305 |
| "13 requirements fully covered" | ps-analyst-001 | Requirements-to-Gap Mapping, lines 306-324 |
| "L3 is the primary security enforcement point; 12 of 42 FR map to L3" | nse-requirements-001 | Finding 2, lines 984-987 |
| "L2 token budget: 559/850 tokens used, 291 remaining" | ps-analyst-001 | Citation Traces, line 514 |
| "Defense-in-depth is the only viable strategy; 12 defenses bypassed >90%" | nse-explorer-001 | Executive Summary, line 42 |
| "Meta Rule of Two: max 2 of (untrusted input, sensitive data, external state change)" | nse-requirements-001 | Finding 5, lines 996-998 |
| "10 recommended Phase 2 architecture decisions with dependency map" | ps-analyst-001 | Recommended Phase 2 Architecture Priorities, lines 328-475 |
| "MCP creates a vast unmonitored attack surface" | nse-explorer-001 | Category 3 Summary, line 170 |
| "Model-level guardrails function as architectural suggestions, not enforcement" | nse-explorer-001 | Category 5 Summary, line 204 |
| "Tool-Output Firewall addresses aggregate RPN of 1,636" | nse-explorer-001 | Mitigation Priority 1, line 444 |
| "HARD rule ceiling 25/25 with zero headroom" | ps-analyst-001 | Context in multiple sections; quality-enforcement.md |

---

*Handoff version: 1.0.0 | Criticality: C4 | Confidence: 0.88*
*Source pipeline: NSE Phase 1 (nse-requirements-001, nse-explorer-001)*
*Consuming pipeline: PS Phase 2 (ps-architect-001, ps-researcher-003)*
*Workflow: agentic-sec-20260222-001 | Barrier: 1 | Direction: NSE -> PS*
