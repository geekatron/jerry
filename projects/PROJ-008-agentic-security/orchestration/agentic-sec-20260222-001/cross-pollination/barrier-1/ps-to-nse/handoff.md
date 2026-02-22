# Barrier 1 Handoff: PS --> NSE

> Cross-pollination from Problem-Solving Pipeline Phase 1 to NASA-SE Pipeline Phase 2
> Workflow: agentic-sec-20260222-001
> Date: 2026-02-22

## Document Sections

| Section | Purpose |
|---------|---------|
| [1. Handoff Metadata](#1-handoff-metadata) | Agent identity, criticality, confidence assessment |
| [2. Key Findings](#2-key-findings) | Top 7 findings the NSE pipeline must act on |
| [3. Threat Landscape Summary](#3-threat-landscape-summary) | Synthesized threat landscape for architecture and requirements |
| [4. Gap Analysis Priorities](#4-gap-analysis-priorities) | Prioritized gaps with composite scores and risk rankings |
| [5. Requirements Implications](#5-requirements-implications) | How findings map to the 57 requirements baseline |
| [6. Architecture Constraints](#6-architecture-constraints) | Constraints and patterns that MUST be respected in Phase 2 |
| [7. Trade Study Inputs](#7-trade-study-inputs) | Data points for nse-explorer-002 trade studies |
| [8. Blockers](#8-blockers) | Risks and blockers that could impact Phase 2 |
| [9. Artifact References](#9-artifact-references) | Full paths to all PS Phase 1 artifacts |
| [10. Citations](#10-citations) | All claims traced to source artifacts |

---

## 1. Handoff Metadata

| Field | Value |
|-------|-------|
| **from_agents** | PS Pipeline Phase 1: ps-researcher-001, ps-researcher-002, ps-analyst-001 |
| **to_agents** | nse-architecture-001, nse-requirements-002, nse-explorer-002 |
| **criticality** | C4 |
| **confidence** | 0.88 |
| **phase_complete** | PS Phase 1 (Deep Research + Gap Analysis) |
| **phase_target** | NSE Phase 2 (Formal Architecture, Requirements Baseline, Trade Studies) |

**Confidence calibration:** 0.88 reflects comprehensive coverage (10 framework scopes, 7 competitive targets, 60 FMEA failure modes, 57 requirements mapped) with two residual gaps: (1) some threat categories (MCP protocol-specific threats) have no authoritative framework coverage yet, and (2) FMEA severity/occurrence/detection scores are expert-estimated, not empirically validated. These gaps are documented and do not materially affect the architectural direction.

---

## 2. Key Findings

The following 7 findings represent the most critical intelligence the NSE pipeline needs for Phase 2. Each is a convergent conclusion supported by multiple PS Phase 1 artifacts.

1. **Jerry's architecture is sound but its runtime enforcement is incomplete.** The 5-layer enforcement architecture (L1-L5), tool tier system (T1-T5), and constitutional governance are industry-leading at design-time. The critical gap is at L3 (pre-tool runtime gating) and L4 (post-tool output inspection), where no security-specific enforcement exists. Every one of the top 5 FMEA risks (RPN >= 400) exploits this L3/L4 gap. [ps-analyst-001, Executive Summary; ps-researcher-002, Cross-Framework Mapping]

2. **Indirect prompt injection via tool results is the #1 risk (RPN 504).** MCP tool results and file Read outputs enter LLM context without sanitization or source-tagging. The LLM cannot distinguish trusted instructions from untrusted data. All 10 frameworks analyzed identify this instruction/data confusion as the primary agentic attack vector. [ps-analyst-001, Priority Ranking #1; ps-researcher-002, ASI01 analysis]

3. **MCP supply chain is a full GAP -- the only threat category with zero Jerry coverage.** ASI04 (Supply Chain) is the only OWASP Agentic Top 10 item rated as a full GAP in the gap matrix (0/10 COVERED, 9/10 PARTIAL, 1/10 GAP). Jerry mandates MCP usage (MCP-001, MCP-002) but has no defense against poisoned MCP responses. Cisco calls MCP "a vast unmonitored attack surface." The ClawHavoc campaign (800+ malicious skills) and Cline supply chain attack demonstrate this is an active, scalable attack class. [ps-analyst-001, Gap Matrix ASI04; ps-researcher-001, Theme 2]

4. **Defense-in-depth is the only viable strategy -- validated by industry consensus.** A joint OpenAI/Anthropic/Google DeepMind study confirmed 12 published defenses were bypassed with >90% success rates using adaptive attacks. Anthropic, Google DeepMind, Microsoft, and Cisco independently converge on multi-layered architectures. Single-layer defenses fail systematically. Jerry's 5-layer architecture is correctly structured; the task is to specialize each layer for security functions. [ps-researcher-001, Theme 1; ps-researcher-002, Executive Summary]

5. **Context rot is a Jerry-specific security vector with no external framework equivalent.** No existing framework (MITRE, OWASP, NIST) explicitly models the degradation of behavioral constraints as context fills. This falls between ATLAS AML.T0080 (Context Poisoning) and OWASP ASI06 (Memory Poisoning) but is distinct: it is the natural entropic decay of L1 rules, not an adversarial injection. Jerry's L2 re-injection is the only known defense, and it is genuinely novel. [ps-researcher-002, Cross-Framework Mapping "Context Rot as Security Threat" gap; ps-analyst-001, Decision 6]

6. **18 of 57 security requirements have zero current Jerry coverage.** These requirements address functionality that does not exist in Jerry today, including cryptographic agent identity (FR-SEC-001/002), direct and indirect prompt injection prevention (FR-SEC-011/012), MCP server integrity verification (FR-SEC-025), comprehensive audit trail (FR-SEC-029), and rogue agent detection (FR-SEC-037). All 18 are rated CRITICAL or HIGH priority. [ps-analyst-001, Requirements-to-Gap Mapping, "No Current Coverage"]

7. **10 architecture decisions are recommended for Phase 2, with a clear dependency map and implementation order.** The decisions are organized around three independent tracks: (a) L3 gate infrastructure (Decision 3) as the foundation for Decisions 4, 7; (b) L4 tool-output firewall (Decision 1) enabling Decisions 5, 6, 8; and (c) Agent identity (Decision 9) enabling Decisions 7, 8. MCP verification (Decision 2) and adversarial testing (Decision 10) are independent. [ps-analyst-001, Recommended Phase 2 Architecture Priorities]

---

## 3. Threat Landscape Summary

### 3.1 Framework Scope

PS Phase 1 consumed 10 security framework scopes across 3 standards bodies (MITRE, OWASP, NIST) and analyzed 7 competitive targets (OpenClaw, Claude Agent SDK, Claude Code, claude-flow, Cline, Microsoft Agent 365, Cisco AI Defense). [ps-researcher-002, Executive Summary]

**Framework coverage:**
- 14 ATT&CK Enterprise tactics with 10 techniques mapped to agentic analogs
- 15 ATLAS AI-specific tactics with 66 techniques, including 14 new agent-specific techniques (Oct 2025)
- 40 OWASP risk items across 4 Top 10 lists (LLM, Agentic, API, Web)
- 20 NIST 800-53 control families (1,007 controls), 6 CSF 2.0 functions, 12 GenAI risk categories

### 3.2 Unified Threat Taxonomy (8 Categories)

The cross-framework mapping resolves to 8 primary threat categories. These are the authoritative threat categories for Phase 2 architecture. [ps-researcher-002, Cross-Framework Mapping]

| # | Threat Category | Priority | Jerry Gap Status | Key Framework References |
|---|----------------|----------|-----------------|-------------------------|
| 1 | Prompt Injection and Goal Hijack | P1 | PARTIAL -- L2 exists; no L3/L4 input/output sanitization | ATT&CK TA0001, ATLAS AML.T0080, LLM01, ASI01, NIST SI-10 |
| 2 | Tool Misuse and Excessive Agency | P1 | PARTIAL -- T1-T5 tiers defined; no runtime enforcement | ATT&CK TA0002, ATLAS AML.T0085.001, LLM06, ASI02, NIST AC-3/AC-6 |
| 3 | Memory and Context Manipulation | P1 | PARTIAL -- L2 re-injection, AE-006; no runtime integrity verification | ATT&CK TA0003, ATLAS AML.T0080, LLM04/LLM08, ASI06, NIST CM-3/SI-4 |
| 4 | Rogue Agents and Trust Exploitation | P1 | PARTIAL -- H-34 schema, L5 CI; no runtime behavioral monitoring | ATT&CK TA0005, ATLAS AML.T0081, LLM09, ASI09/ASI10, NIST AU-2/AU-6 |
| 5 | Privilege Escalation and Identity Abuse | P2 | PARTIAL -- P-003, T1-T5; no per-task credential scoping | ATT&CK TA0004, ATLAS AML.T0083, LLM06, ASI03, NIST IA-2/AC-6 |
| 6 | Supply Chain Compromise | P2 | GAP -- No MCP verification of any kind | ATT&CK TA0042, LLM03, ASI04, NIST SR |
| 7 | Information Disclosure and Exfiltration | P2 | PARTIAL -- Output filtering guardrails; no DLP | ATT&CK TA0009/TA0010, ATLAS AML.T0086, LLM02/LLM07, NIST SC-8/AC-4 |
| 8 | Inter-Agent Comms and Cascading Failures | P2 | PARTIAL -- Circuit breaker H-36, handoff schema; no crypto auth | ATT&CK TA0008, LLM05/LLM10, ASI07/ASI08, NIST SC-7/IR-4 |

**Additional Jerry-specific threats** (not fully addressed by any external framework):
- **Context Rot as Security Vector** (P1): L1 rule degradation under context pressure. L2 re-injection is the primary defense. [ps-researcher-002, Coverage Gaps]
- **MCP Protocol-Specific Threats** (P2): MCP is too new (late 2024) for dedicated framework coverage. Tool descriptor poisoning, server impersonation, and tool schema manipulation have no dedicated taxonomy. [ps-researcher-002, Coverage Gaps]

### 3.3 Most Directly Applicable Framework: OWASP Agentic Top 10

The OWASP Top 10 for Agentic Applications (2026) is the single most directly applicable framework for Jerry. All 10 items map to specific Jerry attack surfaces. [ps-researcher-002, OWASP Agentic Top 10 section]

**For nse-architecture-001:** The ASI01-ASI10 Jerry-Specific Threat Mapping table in ps-researcher-002 (lines 547-558) provides per-item existing mitigations and gaps that must drive architecture decisions.

**For nse-requirements-002:** The ASI01-ASI10 recommended mitigations with Jerry priority tiers (P1 Immediate, P2 Near-term, P3 Strategic) in ps-researcher-002 (lines 562-566) provide direct input for requirements prioritization.

### 3.4 Competitive Threat Intelligence

Key incidents and patterns from the competitive landscape that validate threat priorities:

| Incident/Finding | Significance for Phase 2 | Source |
|-------------------|--------------------------|--------|
| GTG-1002: First AI-orchestrated espionage (80-90% autonomous) | Proves behavioral guardrails insufficient against nation-state adversaries. Context splitting technique directly applicable to Jerry. | ps-researcher-001, Section 3 (C11) |
| ClawHavoc: 800+ malicious skills (20% of registry) | Validates supply chain as dominant attack vector. MCP ecosystem is analogous. | ps-researcher-001, Section 1 (C5) |
| Clinejection: Prompt injection in CI/CD to npm compromise | Demonstrates cascading supply chain attacks through AI agent CI workflows. | ps-researcher-001, Section 5 (C19, C20) |
| CVE-2026-25253: OpenClaw 1-click RCE (CVSS 8.8) | Shows consequences of default-permissive configuration + no auth. | ps-researcher-001, Section 1 (C2, C3) |
| Google DeepMind joint study: 12 defenses bypassed at >90% | Validates defense-in-depth as the only viable strategy. | ps-researcher-001, Theme 1 (C29) |
| Microsoft Entra Agent ID | Establishes enterprise reference architecture for agent identity. | ps-researcher-001, Section 6 (C21) |
| Cisco: "MCP creates a vast unmonitored attack surface" | Industry validation of MCP supply chain risk. | ps-researcher-001, Section 7 (C27) |

---

## 4. Gap Analysis Priorities

### 4.1 Top 5 Critical FMEA Risks (RPN >= 400)

All five exploit gaps in Jerry's L3/L4 enforcement layers. These are the risks that Phase 2 architecture MUST address. [ps-analyst-001, Executive Summary]

| Rank | Risk ID | Description | RPN | Gap Category |
|------|---------|-------------|-----|-------------|
| 1 | R-PI-002 | Indirect prompt injection via MCP tool results | 504 | No L4 tool-output sanitization |
| 2 | R-SC-001 | Malicious MCP server packages | 480 | No MCP supply chain verification |
| 3 | R-GB-001 | Constitutional circumvention via context rot | 432 | L2 defense exists but 5 Tier B rules lack L2 protection |
| 4 | R-CF-005 | False negatives in security controls | 405 | No adversarial testing program to validate controls |
| 5 | R-PI-003 | Indirect prompt injection via file contents | 392 | No content-source tagging on Read tool results |

### 4.2 Composite-Scored Priority Ranking (Top 10)

Scoring methodology: Risk (40%) + Feasibility (20%) + Competitive Impact (20%) + Dependency (20%). Scale: 1-10 per dimension. [ps-analyst-001, Priority Ranking]

| Rank | Gap | Composite | Risk | Feasibility | Competitive | Dependency | Phase 2 |
|------|-----|-----------|------|-------------|-------------|-----------|---------|
| 1 | MCP Supply Chain Verification | **8.8** | 10 | 7 | 9 | 8 | MUST |
| 2 | Tool-Output Firewall (L4) | **8.6** | 10 | 6 | 8 | 9 | MUST |
| 3 | Runtime Tool Access Matrix (L3) | **8.6** | 8 | 9 | 8 | 10 | MUST |
| 4 | Bash Tool Hardening (L3) | **8.2** | 10 | 8 | 7 | 6 | MUST |
| 5 | Context Rot Security Hardening | **7.4** | 10 | 7 | 4 | 6 | MUST |
| 6 | Secret Detection and DLP (L4) | **7.2** | 8 | 8 | 7 | 5 | MUST |
| 7 | Handoff Integrity Protocol | **6.8** | 8 | 5 | 6 | 7 | SHOULD |
| 8 | Comprehensive Audit Trail | **6.8** | 8 | 6 | 8 | 4 | SHOULD |
| 9 | Adversarial Testing Program | **6.6** | 10 | 7 | 6 | 2 | SHOULD |
| 10 | Agent Identity Foundation | **6.6** | 6 | 4 | 9 | 8 | SHOULD |

### 4.3 OWASP Agentic Top 10 Gap Matrix Summary

| Status | Count | Items |
|--------|-------|-------|
| COVERED | 0/10 | None |
| PARTIAL | 9/10 | ASI01, ASI02, ASI03, ASI05, ASI06, ASI07, ASI08, ASI09, ASI10 |
| GAP | 1/10 | ASI04 (Supply Chain Vulnerabilities) |

The consistent pattern: design-time controls (schema, CI) exist but runtime enforcement (L3/L4 security gates) is missing. [ps-analyst-001, Gap Matrix Summary]

### 4.4 NIST 800-53 Control Family Coverage

| Status | Count | Families |
|--------|-------|----------|
| COVERED | 1/10 | RA (Risk Assessment) |
| PARTIAL | 6/10 | AC, CM, IR, SC, SI, SA |
| GAP | 3/10 | AU (Audit), IA (Identity/Auth), SR (Supply Chain) |

The three GAP families (Audit, Identity, Supply Chain) correspond directly to the top critical gaps. [ps-analyst-001, NIST 800-53 Summary]

---

## 5. Requirements Implications

### 5.1 Coverage Summary for the 57 Requirements Baseline

The 57 security requirements from nse-requirements-001 (42 functional, 15 non-functional) map to gap status as follows. [ps-analyst-001, Requirements-to-Gap Mapping]

| Coverage Status | Count | Phase 2 Action |
|----------------|-------|---------------|
| No Current Coverage (urgent) | 18 | Architecture and implementation required |
| Partial Coverage (extend) | 26 | Security-specific extensions to existing controls |
| Fully Covered (validate) | 13 | Validation testing in Phase 4 |

### 5.2 Requirements with No Current Coverage (18 -- Architecture Required)

**For nse-requirements-002:** These 18 requirements MUST be baselined with traceability to Phase 2 architecture decisions.

| Requirement | Title | Priority | Architecture Decision |
|-------------|-------|----------|----------------------|
| FR-SEC-001 | Unique Agent Identity | CRITICAL | Decision 9 (Agent Identity) |
| FR-SEC-002 | Agent Authentication at Trust Boundaries | CRITICAL | Decision 9 |
| FR-SEC-011 | Direct Prompt Injection Prevention | CRITICAL | Decision 1 (Tool-Output Firewall) |
| FR-SEC-012 | Indirect Prompt Injection Prevention via Tool Results | CRITICAL | Decision 1 |
| FR-SEC-013 | MCP Server Input Sanitization | CRITICAL | Decision 2 (MCP Verification) |
| FR-SEC-025 | MCP Server Integrity Verification | CRITICAL | Decision 2 |
| FR-SEC-029 | Comprehensive Agent Action Audit Trail | CRITICAL | Decision 8 (Audit Trail) |
| FR-SEC-033 | Agent Containment Mechanism | CRITICAL | Decision 4 (Bash Hardening) |
| FR-SEC-037 | Rogue Agent Detection | CRITICAL | Decision 10 (Adversarial Testing) |
| FR-SEC-003 | Agent Identity Lifecycle Management | HIGH | Decision 9 |
| FR-SEC-004 | Agent Provenance Tracking | HIGH | Decision 9 + Decision 8 |
| FR-SEC-009 | Toxic Tool Combination Prevention | HIGH | Decision 3 (L3 Gate) + Decision 4 |
| FR-SEC-015 | Agent Goal Integrity Verification | HIGH | Decision 1 (L4 behavioral monitoring) |
| FR-SEC-019 | System Prompt Leakage Prevention | HIGH | Decision 5 (Secret Detection) |
| FR-SEC-023 | Message Integrity in Handoff Chains | MEDIUM | Decision 7 (Handoff Integrity) |
| FR-SEC-030 | Security Event Logging | HIGH | Decision 8 |
| FR-SEC-031 | Anomaly Detection Triggers | MEDIUM | Decision 10 |
| FR-SEC-036 | Recovery Procedures After Security Incidents | MEDIUM | Decision 8 |

### 5.3 Requirements with Partial Coverage (26 -- Extensions Required)

**For nse-requirements-002:** These requirements have existing Jerry controls but need security-specific extensions. The most critical (CRITICAL priority) are:

| Requirement | Title | Existing Control | Extension Needed |
|-------------|-------|-----------------|-----------------|
| FR-SEC-005 | Least Privilege Tool Access Enforcement | T1-T5 tiers, H-34, L5 CI | Runtime L3 enforcement (Decision 3) |
| FR-SEC-006 | Tool Tier Boundary Enforcement | T1-T5, H-35 worker restrictions | Runtime L3 gate (Decision 3) |
| FR-SEC-007 | Forbidden Action Enforcement | H-35, constitutional triplet | L3 pre-tool check (Decision 3) |
| FR-SEC-008 | Privilege Non-Escalation in Delegation | P-003, tool tiers, handoff protocol | Privilege intersection computation (Decision 7) |
| FR-SEC-017 | Sensitive Information Output Filtering | `no_secrets_in_output` guardrail | Deterministic L4 secret detection (Decision 5) |
| FR-SEC-038 | HITL for High-Impact Actions | P-020 user authority, AE rules | Formalized action classification (Decision 3) |
| FR-SEC-039 | Recursive Delegation Prevention | P-003/H-01, H-35 | L3 delegation depth enforcement (Decision 3) |
| NFR-SEC-006 | Fail-Closed Security Default | L3 concept, fallback_behavior | Define fail-closed for every checkpoint (Decision 3) |

[ps-analyst-001, Requirements-to-Gap Mapping, "Partial Coverage"]

### 5.4 Requirements Fully Covered (13 -- Validate in Phase 4)

These 13 requirements are satisfied by existing Jerry controls. Phase 4 validation testing should confirm:

NFR-SEC-001 through NFR-SEC-015 (excluding NFR-SEC-004 and NFR-SEC-006 which are partial). Key covered areas: security token budget (L2 559/850 tokens), deterministic control performance (L3/L5 immune), MCP failure resilience (fallback mechanism), scalability (routing roadmap), minimal friction (C1-C4 proportional enforcement), testability (H-20 BDD). [ps-analyst-001, Requirements-to-Gap Mapping, "Fully Covered"]

---

## 6. Architecture Constraints

The following constraints and patterns were identified in PS Phase 1 research that MUST be respected in Phase 2 architecture work. These are directed primarily at **nse-architecture-001**.

### 6.1 Trust Boundary Definitions

Three critical trust boundaries identified across all frameworks. [ps-researcher-002, ASI01/ASI02/ASI07 analyses; ps-analyst-001, Decision 1]

| Trust Boundary | Description | Current Status | Phase 2 Requirement |
|----------------|-------------|----------------|---------------------|
| **Tool-Result-to-Prompt** | Where tool execution results re-enter the LLM prompt context. Primary injection surface for indirect prompt injection. | NO BOUNDARY EXISTS. Tool results enter context raw. | MUST implement L4 tool-output firewall with content-source tagging (trusted/untrusted). |
| **Agent-to-Agent (Handoff)** | Where one agent passes context to another via Task tool or multi-skill coordination. | PARTIAL. Handoff schema defined (HD-M-001) but not enforced at L3. `from_agent` is self-reported. | MUST enforce handoff schema at L3. MUST implement system-set `from_agent`. SHOULD add cryptographic integrity for C3+. |
| **Framework-to-External (MCP)** | Where Jerry communicates with external MCP servers (Context7, Memory-Keeper). | NO BOUNDARY EXISTS. MCP responses consumed without validation. | MUST implement MCP server allowlist with hash pinning. MUST validate MCP response integrity. |

### 6.2 Zero-Trust Requirements

The competitive landscape analysis validates zero-trust as the correct architectural posture. [ps-researcher-001, Themes 1, 4, 7]

| Principle | Application to Jerry |
|-----------|---------------------|
| Never trust, always verify | Every tool result, MCP response, and handoff payload must be treated as potentially hostile |
| Least privilege access | Tool tier enforcement must move from advisory (design-time) to deterministic (runtime L3) |
| Assume breach | Security controls must assume that some layer has been bypassed; defense-in-depth compensates |
| Verify explicitly | Agent identity, handoff integrity, and MCP server integrity must be verifiable at runtime |

### 6.3 The L3/L4 Enforcement Gap (Critical Finding)

**This is the single most important architectural finding for Phase 2.**

Jerry's enforcement layers are correctly designed but unevenly populated with security functions. [ps-analyst-001, Executive Summary; ps-researcher-002, Cross-Framework Mapping]

| Layer | Current Security Function | Required Security Function |
|-------|--------------------------|---------------------------|
| L1 (Session start) | Behavioral rules loaded | Behavioral rules loaded (unchanged) |
| L2 (Every prompt) | Constitutional re-injection (20 Tier A rules) | Constitutional re-injection + promote H-18 to Tier A |
| **L3 (Pre-tool)** | **AST gating for worktracker only** | **Runtime tool access matrix, Bash command classification, MCP server verification, handoff schema enforcement, input injection detection, delegation depth check** |
| **L4 (Post-tool)** | **Self-correction only (advisory)** | **Tool-output firewall (injection scanning, content-source tagging), secret detection/DLP, system prompt leakage prevention, behavioral anomaly detection, audit event generation** |
| L5 (CI/commit) | Schema validation, git integrity | Schema validation + MCP config validation + dependency scanning + security-specific CI gates |

**For nse-architecture-001:** The Phase 2 formal architecture MUST define L3 and L4 as the primary security enforcement layers, with specific gate specifications for each security check listed above.

### 6.4 Supply Chain Verification Architecture

MCP supply chain verification requires controls at multiple points. [ps-analyst-001, Decision 2; ps-researcher-001, Theme 2]

| Control Point | Control | Implementation |
|--------------|---------|----------------|
| Configuration time | MCP server allowlist with SHA-256 hash pinning | Extend `.claude/settings.local.json` schema |
| Session start (L3) | Verify MCP server config hashes match pinned values | L3 pre-session check |
| CI/commit (L5) | Validate MCP configurations against allowlist | L5 CI gate |
| Runtime (L4) | Validate MCP response content for injection patterns | L4 tool-output firewall |

### 6.5 NPR 7123.1D Alignment Points

**For nse-architecture-001 specifically:** The formal security architecture should align with NPR 7123.1D technical requirements processes. Key alignment points from PS Phase 1:

| NPR 7123.1D Process | Security Architecture Application |
|----------------------|-----------------------------------|
| 4.2 Stakeholder Expectations | Agent users expect: no data exfiltration, no unauthorized actions, constitutional compliance |
| 4.3 Technical Requirements | The 57 security requirements (42 FR + 15 NFR) from nse-requirements-001 |
| 4.4 Logical Decomposition | L1-L5 enforcement layers with L3/L4 security specialization |
| 4.5 Design Solution | 10 architecture decisions with dependency map |
| 4.6 Product Realization | Implementation order (Decision 3 first, then 1/2 in parallel, etc.) |
| 4.7 Product Integration | Cross-layer integration (L3 gate feeds L4 inspection feeds L5 audit) |
| 4.8 Product Verification | Adversarial testing program (Decision 10), Phase 4 validation |

---

## 7. Trade Study Inputs

Data points for **nse-explorer-002** trade studies on security vs. performance and competing design approaches.

### 7.1 Security vs. Performance Trade-Offs

| Trade-Off | Option A | Option B | Evidence |
|-----------|----------|----------|----------|
| **L4 Tool-Output Scanning: Pattern-Match vs. Classifier** | Regex-based pattern matching (~0ms, zero tokens) | Dedicated LLM classifier (~300-5000ms, ~900-1500 tokens) | Microsoft uses a dedicated cross-prompt injection classifier (C24). For Jerry's local-first architecture, pattern-matching is recommended as the initial approach with classifier escalation for ambiguous cases. [ps-analyst-001, Decision 1; ps-researcher-001, Section 6] |
| **MCP Verification: Hash Pinning vs. Full Attestation** | SHA-256 hash pinning in config (LOW complexity) | Full attestation with signed manifests and runtime verification (HIGH complexity) | Hash pinning addresses the #2 risk (RPN 480) at LOW complexity. Full attestation is the long-term target but requires MCP ecosystem support that does not yet exist. [ps-analyst-001, Decision 2] |
| **Bash Tool: Allowlist vs. Blocklist** | Per-tier command allowlists (whitelist approach, higher security, lower flexibility) | Blocklisted dangerous commands (blacklist approach, lower security, higher flexibility) | Allowlist is recommended because blocklists are inherently incomplete -- new attack techniques create new commands to block. Per-tier allowlists align with T1-T5 existing architecture. [ps-analyst-001, Decision 4] |
| **Agent Identity: Lightweight Instance ID vs. Cryptographic Tokens** | Name-timestamp-nonce instance ID (LOW complexity, no crypto) | Macaroon/Biscuit delegation capability tokens (HIGH complexity, full crypto) | Lightweight instance ID is achievable in Phase 2 and provides attribution. Cryptographic tokens (per Google DeepMind arXiv:2602.11865) provide scope narrowing but require infrastructure. Recommend phased approach. [ps-analyst-001, Decision 9; ps-researcher-001, C31] |
| **Context Rot Defense: L2 Promotion vs. Session Partitioning** | Promote H-18 to Tier A (LOW complexity, +40 tokens within budget) | Auto-partition sessions at CRITICAL fill (MEDIUM complexity, Memory-Keeper integration) | Both should be implemented. H-18 promotion is trivial (291 tokens remaining in L2 budget). Session partitioning provides structural defense. [ps-analyst-001, Decision 6] |

### 7.2 Competitive Approaches to Common Problems

| Problem | Claude Code Approach | Microsoft Approach | Cisco Approach | Jerry Design Implication |
|---------|---------------------|-------------------|----------------|--------------------------|
| Prompt injection | Sandbox + static analysis + summarization (95% attack surface reduction, 98.5% detection rate) | AI Prompt Shield dedicated classifier | Real-time guardrails | Jerry should layer: L2 constitutional re-injection + L3 input validation + L4 output scanning. [ps-researcher-001, C8, C10, C23, C27] |
| Credential protection | Proxy pattern (agent never sees credentials) | Purview DLP (sensitivity labels) | Recommended (AI BOM) | Jerry's local-first architecture makes the proxy pattern less applicable. Secret detection (Decision 5) + file access control is the right approach. [ps-researcher-001, Section 2] |
| Agent identity | Per-session sandbox isolation | Entra Agent ID (immutable object ID, conditional access, lifecycle) | Recommended in taxonomy | Jerry should implement lightweight instance ID in Phase 2, design for Entra-equivalent in future phases. [ps-researcher-001, C21] |
| Supply chain | No MCP verification (equal gap with Jerry) | Defender scan + Security Exposure Management | Open-source MCP/A2A/skill scanners | Jerry should evaluate Cisco open-source scanners for L5 integration. [ps-researcher-001, C27] |
| Multi-agent security | N/A (single agent) | Control plane governance | Taxonomy-based (4-layer) | Jerry's P-003 single-level nesting provides the topological boundary. Add handoff integrity within that topology. [ps-researcher-001, Theme 7] |

### 7.3 Industry Best Practices for Adoption Evaluation

| Practice | Source | Applicability | Priority |
|----------|--------|---------------|----------|
| Meta's Rule of Two: max 2 of (untrusted input, sensitive data, external state change) without HITL | Meta AI (C30) | Map to T1-T5 tiers. Define toxic combination registry for L3 enforcement. | HIGH |
| Google DeepMind Delegation Capability Tokens (Macaroons/Biscuits) | arXiv:2602.11865 (C31) | Cryptographic caveats for minimum privilege across handoff chains. Long-term target. | MEDIUM |
| Microsoft Cross-Prompt Injection Classifier | Agent Factory (C24) | Dedicated classifier examining tool responses for injection. Heavy-weight but highest accuracy. | MEDIUM |
| Cisco AI BOM (Bill of Materials) | State of AI Security 2026 (C27) | Inventory of all AI components (models, tools, MCP servers) for supply chain governance. | HIGH |
| Microsoft Automated Red Teaming (PyRIT) | Agent Factory (C24) | Adversarial testing of agent definitions. Maps to Decision 10. | MEDIUM |

---

## 8. Blockers

### 8.1 Identified Blockers

| # | Blocker | Impact | Severity | Mitigation |
|---|---------|--------|----------|------------|
| 1 | **MCP protocol immaturity**: MCP is too new (late 2024) for dedicated security framework coverage. No standardized integrity verification mechanism exists in the protocol. | Phase 2 MCP verification architecture must be designed without protocol-level support. Hash pinning is a framework-level workaround. | HIGH | Design MCP verification at the Jerry configuration layer, not the protocol layer. Monitor MCP spec evolution. |
| 2 | **L3/L4 enforcement requires Claude Code architecture knowledge**: Implementing deterministic L3 pre-tool gates and L4 post-tool inspection requires understanding Claude Code's internal tool invocation pipeline. | Architecture may need to work within Claude Code's existing hook system rather than implementing true interception. | MEDIUM | Investigate Claude Code permission hooks and sandbox architecture. Design within existing extension points. |
| 3 | **No empirical FMEA calibration**: FMEA severity, occurrence, and detection scores are expert-estimated. Actual risk magnitudes may differ. | Priority rankings could shift after empirical testing. | LOW | Accept current rankings as best-available. Calibrate after adversarial testing program (Decision 10) is operational. |

### 8.2 Risks to Phase 2

| # | Risk | Likelihood | Impact | Mitigation |
|---|------|-----------|--------|------------|
| 1 | Architecture scope exceeds Phase 2 capacity (10 decisions, 18 new requirements, 26 extensions) | HIGH | Incomplete implementation | Strict MUST/SHOULD/CONSIDER prioritization. Decisions 1-6 are MUST; 7-10 are SHOULD. |
| 2 | Claude Code constraints limit L3/L4 implementation options | MEDIUM | Reduced security gate capability | Design modular architecture where L3/L4 gates can be progressively strengthened as platform capabilities evolve. |
| 3 | Context rot during Phase 2 execution (long sessions, high complexity) | MEDIUM | Quality degradation of architecture artifacts | Use Memory-Keeper for phase boundary state. Apply AE-006 graduated escalation. Partition into sub-sessions. |

---

## 9. Artifact References

### 9.1 PS Phase 1 Artifacts (Input to This Handoff)

| Artifact | Agent | Lines | Path |
|----------|-------|-------|------|
| Competitive Landscape Analysis | ps-researcher-001 | 667 | `projects/PROJ-008-agentic-security/orchestration/agentic-sec-20260222-001/ps/phase-1/ps-researcher-001/ps-researcher-001-competitive-landscape.md` |
| Threat Framework Analysis | ps-researcher-002 | 882 | `projects/PROJ-008-agentic-security/orchestration/agentic-sec-20260222-001/ps/phase-1/ps-researcher-002/ps-researcher-002-threat-framework-analysis.md` |
| Gap Analysis | ps-analyst-001 | 530 | `projects/PROJ-008-agentic-security/orchestration/agentic-sec-20260222-001/ps/phase-1/ps-analyst-001/ps-analyst-001-gap-analysis.md` |

### 9.2 NSE Phase 1 Artifacts (Referenced by Gap Analysis)

| Artifact | Description | Path |
|----------|-------------|------|
| Security Requirements (nse-requirements-001) | 57 requirements (42 FR + 15 NFR) | Referenced in ps-analyst-001; original artifact in NSE Phase 1 output |
| Risk Register (nse-explorer-001) | 60 FMEA failure modes across 10 categories | Referenced in ps-analyst-001; original artifact in NSE Phase 1 output |

### 9.3 Jerry Framework Rules (Referenced Throughout)

| File | Key Content |
|------|-------------|
| `.context/rules/quality-enforcement.md` | L1-L5 enforcement architecture, HARD Rule Index, Two-Tier Enforcement Model (559/850 L2 tokens), AE-006, criticality levels |
| `.context/rules/agent-development-standards.md` | T1-T5 tool tiers, orchestrator-worker (P-003), handoff protocol (HD-M-001-005), guardrails template |
| `.context/rules/agent-routing-standards.md` | Circuit breaker (H-36), anti-pattern catalog (AP-01-08), routing observability (RT-M-008) |
| `.context/rules/mcp-tool-standards.md` | MCP-001/MCP-002 mandates, canonical tool names, error handling |
| `CLAUDE.md` | Constitutional constraints (P-003, P-020, P-022), H-04, H-05 |

---

## 10. Citations

All claims in this handoff document trace to specific sections of PS Phase 1 artifacts. Citations use the format `[artifact, section/line]`.

### Claim-to-Source Trace Table

| Claim | Source |
|-------|--------|
| "Indirect prompt injection via MCP tool results is the #1 risk (RPN 504)" | ps-analyst-001, Priority Ranking, R-PI-002 (line 142) |
| "Malicious MCP server packages is the #2 risk (RPN 480)" | ps-analyst-001, Priority Ranking, R-SC-001 (line 143) |
| "Constitutional circumvention via context rot is the #3 risk (RPN 432)" | ps-analyst-001, Priority Ranking, R-GB-001 (line 148) |
| "False negatives in security controls is the #4 risk (RPN 405)" | ps-analyst-001, Priority Ranking, R-CF-005 (line 152) |
| "Indirect prompt injection via file contents is the #5 risk (RPN 392)" | ps-analyst-001, Executive Summary (line 31) |
| "0/10 COVERED, 9/10 PARTIAL, 1/10 GAP (ASI04)" | ps-analyst-001, Gap Matrix Summary (line 72) |
| "18 requirements with no current coverage" | ps-analyst-001, Requirements-to-Gap Mapping (line 249) |
| "26 requirements with partial coverage" | ps-analyst-001, Requirements-to-Gap Mapping (line 273) |
| "13 requirements fully covered" | ps-analyst-001, Requirements-to-Gap Mapping (line 306) |
| "10 architecture decisions recommended for Phase 2" | ps-analyst-001, Recommended Phase 2 Architecture Priorities (line 330) |
| "L2 token budget: 559/850 tokens, 291 remaining" | ps-analyst-001, Strength 1 (line 169); quality-enforcement.md |
| "12 published defenses bypassed with >90% success" | ps-researcher-001, Theme 1 (line 484, C29); ps-researcher-002, Executive Summary (line 36) |
| "MCP creates a vast unmonitored attack surface" | ps-researcher-001, Section 7 (line 413, C27) |
| "800+ malicious skills in ClawHub registry" | ps-researcher-001, Section 1 (line 69, C5) |
| "GTG-1002: 80-90% autonomous operation" | ps-researcher-001, Section 3 (line 197, C11) |
| "Model-level guardrails function as architectural suggestions" | ps-researcher-001, Section 2 (line 147, C9) |
| "Detection rate for known prompt injections: 98.5%" | ps-researcher-001, Section 3 (line 181, C8/C10) |
| "Sandboxing reduces attack surface by 95%" | ps-researcher-001, Section 3 (line 180, C8) |
| "Error amplification ~1.3x with structured handoffs vs. 17x" | agent-development-standards.md, Pattern 2 |
| "8 unified threat categories from 10 framework scopes" | ps-researcher-002, Cross-Framework Mapping (line 785) |
| "14 new agent-specific ATLAS techniques (Oct 2025)" | ps-researcher-002, Agent-Specific Techniques (line 116) |
| "Context rot as security threat -- no existing framework models this" | ps-researcher-002, Coverage Gaps (line 812) |
| "Microsoft Entra Agent ID: unique immutable object ID" | ps-researcher-001, Section 6 (line 335, C21) |
| "Google DeepMind Delegation Capability Tokens (Macaroons/Biscuits)" | ps-researcher-001, Consider Adopting #2 (line 582, C31) |
| "Cisco open-source MCP/A2A/skill security scanners" | ps-researcher-001, Section 7 (line 416, C27) |
| "Meta Rule of Two" | ps-researcher-001, Consider Adopting #1 (line 581, C30) |
| "60 FMEA failure modes across 10 categories" | ps-analyst-001, Executive Summary (line 31) |
| "57 total security requirements (42 FR + 15 NFR)" | ps-analyst-001, Executive Summary (line 27) |
| "Composite scoring: Risk 40%, Feasibility 20%, Competitive 20%, Dependency 20%" | ps-analyst-001, Scoring Methodology (lines 132-136) |
| "Decision dependency map: 3 independent tracks" | ps-analyst-001, Decision Dependency Map (lines 444-462) |

---

*Handoff version: 1.0.0 | Cross-pollination: Barrier 1, PS to NSE | Workflow: agentic-sec-20260222-001 | Date: 2026-02-22*
