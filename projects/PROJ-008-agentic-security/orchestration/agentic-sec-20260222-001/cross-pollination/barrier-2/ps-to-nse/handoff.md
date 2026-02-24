# Barrier 2 Handoff: PS --> NSE

> Cross-pollination from Problem-Solving Pipeline Phase 2 to NASA-SE Pipeline Phase 3
> Workflow: agentic-sec-20260222-001
> Date: 2026-02-22
> Criticality: C4

## Document Sections

| Section | Purpose |
|---------|---------|
| [1. Handoff Metadata](#1-handoff-metadata) | Agent identity, criticality, confidence, phase context |
| [2. Key Findings](#2-key-findings) | Top 7 findings NSE Phase 3 must act on |
| [3. Security Architecture Summary](#3-security-architecture-summary) | Synthesized ps-architect-001 architecture for NSE consumption |
| [4. Security Pattern Recommendations](#4-security-pattern-recommendations) | Synthesized ps-researcher-003 patterns for implementation guidance |
| [5. Verification Priorities for nse-verification-001](#5-verification-priorities-for-nse-verification-001) | What to verify first and where the highest risk lies |
| [6. Integration Priorities for nse-integration-001](#6-integration-priorities-for-nse-integration-001) | How security controls integrate with existing Jerry governance |
| [7. Compliance Mapping](#7-compliance-mapping) | Architecture coverage against MITRE, OWASP, NIST |
| [8. Blockers and Risks](#8-blockers-and-risks) | Known issues and risks for Phase 3 |
| [9. Artifact References](#9-artifact-references) | Full paths to all artifacts |
| [10. Citations](#10-citations) | All claims traced to source artifacts |

---

## 1. Handoff Metadata

| Field | Value |
|-------|-------|
| **from_agents** | PS Pipeline Phase 2: ps-architect-001 (Security Architecture), ps-researcher-003 (Security Patterns) |
| **to_agents** | NSE Pipeline Phase 3: nse-verification-001 (Implementation V&V), nse-integration-001 (Integration Verification) |
| **criticality** | C4 |
| **confidence** | 0.92 |
| **phase_complete** | PS Phase 2 (Architecture Design + Security Pattern Research) |
| **phase_target** | NSE Phase 3 (Implementation V&V + Integration Verification) |
| **barrier_predecessor** | Barrier 1 PS-to-NSE (Phase 1 findings to Phase 2 architecture) |

**Confidence calibration:** 0.92 reflects: (a) comprehensive architecture covering all 57 requirements with 10 architecture decisions, 12 L3 gates, 7 L4 inspectors, and 8 L5 CI gates; (b) 47 industry security patterns researched from 60+ sources validating the architecture approach; (c) full compliance mapping (OWASP 10/10, NIST 10/10, MITRE 7/9); (d) two residual gaps reducing confidence from 1.0: (1) L4 injection pattern database effectiveness is unvalidated empirically (OI-02 in ps-architect-001), and (2) content-source tagging mechanism at model level needs prototyping (OI-04). Both gaps are addressable in Phase 3 implementation.

**Context continuity from Barrier 1:** Barrier 1 transferred 7 key findings including the L3/L4 enforcement gap, indirect prompt injection as #1 risk (RPN 504), MCP supply chain as only full GAP, and 10 recommended architecture decisions. PS Phase 2 has designed the architecture to close all identified gaps. This Barrier 2 handoff transfers the completed architecture and pattern research to NSE Phase 3 for verification and integration planning. [Barrier 1 handoff, Section 2]

---

## 2. Key Findings

The following 7 findings represent the most critical intelligence NSE Phase 3 agents need. Each is a convergent conclusion from ps-architect-001's architecture and ps-researcher-003's pattern research.

1. **The security architecture closes all 57 requirement gaps without adding new HARD rules.** All 18 previously zero-coverage requirements and 26 partial-coverage requirements now have architecture coverage through 10 architecture decisions (AD-SEC-01 through AD-SEC-10). The HARD rule ceiling remains at 25/25 -- all security controls are implemented as extensions to existing L3/L4/L5 layers and as configuration-driven registries, not new governance rules. [ps-architect-001, RTM Coverage Summary; Architecture Decisions, HARD Rule Impact]

2. **L3 is the primary security enforcement layer with 12 deterministic gates totaling <50ms latency.** The L3 Security Gate pipeline (L3-G01 through L3-G12) intercepts every tool invocation with deterministic checks: tool access matrix, tier enforcement, toxic combination detection, Bash command classification, MCP server verification, delegation gating, and more. All gates are context-rot immune and fail-closed by default (NFR-SEC-006). 19 requirements allocate to L3 as primary. [ps-architect-001, L3 Gate Registry; nse-architecture-001, SS-L3]

3. **L4 Tool-Output Firewall addresses the #1 risk (RPN 504) with 7 inspectors totaling <170ms latency.** L4 inspectors (L4-I01 through L4-I07) cover injection pattern scanning, content-source tagging, secret detection, system prompt canary detection, handoff integrity verification, behavioral drift monitoring, and audit logging. The firewall is pattern-matching based (not LLM-based) to ensure determinism and performance. 15 requirements allocate to L4 as primary. [ps-architect-001, L4 Inspector Registry; ps-researcher-003, Recommendation 1]

4. **Industry consensus validates Jerry's architectural approach, but no single defense is sufficient.** 47 patterns from 60+ sources confirm: (a) deterministic gating is the industry consensus (Pattern 1.1: Guardrails-by-Construction), (b) content-source tagging is the critical missing defense (Pattern 4.1: Spotlighting), (c) defense-in-depth is the only viable strategy (PALADIN reduces attacks from 73.2% to 8.7%, not zero). Jerry's L2 re-injection has no direct industry analog and is architecturally novel. [ps-researcher-003, Executive Summary Findings 1, 2, 6, 7]

5. **Five innovation areas exist where Jerry must go beyond industry patterns.** (a) L2 re-injection as a security watchdog -- no external equivalent exists; (b) context rot as a security metric -- no framework models this; (c) MCP protocol-specific security standards -- emerging but immature; (d) real-time toxic combination detection -- Meta's Rule of Two has no production implementation; (e) quality gate LLM-as-Judge security -- no framework addresses adversarial score manipulation. [ps-researcher-003, Gap Analysis, Gaps 1-5]

6. **The architecture achieves defense-in-depth with every critical risk covered by at least two independent layers.** The top 5 FMEA risks all have multi-layer responses: R-PI-002 (RPN 504) covered by L2 + L3 + L4 + L5; R-SC-001 (RPN 480) by L3 + L4 + L5; R-GB-001 (RPN 432) by L1 + L2 + L4 + L6; R-CF-005 (RPN 405) by L5 + L6; R-PI-003 (RPN 392) by L2 + L4. No single-point-of-failure exists for any RPN >= 400 risk. [ps-architect-001, Executive Summary FMEA table; ps-researcher-003, Defense-in-Depth Model]

7. **Implementation should follow a specific dependency-driven order starting with L3 gate infrastructure.** The recommended implementation order is: (1) AD-SEC-01 (L3 Gate, foundational, LOW complexity), (2) AD-SEC-02 (Tool-Output Firewall, highest risk reduction, MEDIUM), (3) AD-SEC-03 (MCP Verification, MEDIUM), (4) AD-SEC-05 (Secret Detection, LOW), (5) AD-SEC-04 (Bash Hardening, depends on #1), (6) AD-SEC-06 (Context Rot, depends on #2), (7-10) Identity, Handoff, Audit, Testing. [ps-architect-001, Decision Dependency Map and recommended implementation order]

---

## 3. Security Architecture Summary

### 3.1 Architecture Decisions (AD-SEC-01 through AD-SEC-10)

The 10 architecture decisions are organized into three independent implementation tracks plus one cross-cutting validation track. All decisions have status PROPOSED.

| ID | Decision | Aggregate RPN Addressed | Dependencies | Impl. Priority | Complexity | Key Gates |
|----|----------|------------------------|-------------|----------------|------------|-----------|
| AD-SEC-01 | L3 Security Gate Infrastructure | 508 | None (foundational) | 1 | LOW | L3-G01 through L3-G12 |
| AD-SEC-02 | Tool-Output Firewall (L4) | 1,636 | None | 2 | MEDIUM | L4-I01 through L4-I07 |
| AD-SEC-03 | MCP Supply Chain Verification | 1,198 | None | 3 | MEDIUM | L3-G07, L3-G08, L5-S03 |
| AD-SEC-04 | Bash Tool Hardening | 1,285 | AD-SEC-01 | 4 | MEDIUM | L3-G04, L3-G12 |
| AD-SEC-05 | Secret Detection and DLP | 1,084 | Independent (benefits from AD-SEC-02) | 5 | LOW | L4-I03, L4-I04, L3-G05 |
| AD-SEC-06 | Context Rot Security Hardening | 1,131 | Partially AD-SEC-02 | 6 | MEDIUM | L2 Tier A promotion, AE-006 |
| AD-SEC-07 | Agent Identity Foundation | 693 | None | 7 | HIGH | L3-G09 (identity), agent registry |
| AD-SEC-08 | Handoff Integrity Protocol | 1,380 | AD-SEC-01, AD-SEC-07 | 8 | MEDIUM | L4-I05, SHA-256 hashing |
| AD-SEC-09 | Comprehensive Audit Trail | 939 | AD-SEC-01, AD-SEC-02, AD-SEC-07 | 9 | MEDIUM | L4-I07, L3-G06 |
| AD-SEC-10 | Adversarial Testing Program | 765 | All others (validates them) | 10 | MEDIUM | /adversary integration, L5 CI |

**Dependency tracks:**

- **Track A (L3 Foundation):** AD-SEC-01 -> AD-SEC-04 -> AD-SEC-08
- **Track B (L4 Firewall):** AD-SEC-02 -> AD-SEC-05, AD-SEC-06, AD-SEC-09
- **Track C (Identity):** AD-SEC-07 -> AD-SEC-08, AD-SEC-09
- **Independent:** AD-SEC-03 (MCP), AD-SEC-10 (Testing validates all)

[ps-architect-001, Architecture Decisions section and Decision Dependency Map]

### 3.2 L3 Gate Specifications (12 Gates, <50ms Total)

L3 is the primary runtime security enforcement layer. All gates are deterministic (pattern matching, list lookup, hash comparison), context-rot immune, and fail-closed by default.

| Gate ID | Name | Check Type | Decision | Latency |
|---------|------|-----------|----------|---------|
| L3-G01 | Tool Access Matrix | List lookup: (agent, tool) -> allowed_tools | ALLOW/DENY | <1ms |
| L3-G02 | Tier Enforcement | Comparison: (agent_tier, tool_tier) -> valid | ALLOW/DENY | <1ms |
| L3-G03 | Toxic Combination | Registry lookup: Meta Rule of Two | ALLOW/DENY/HITL | <5ms |
| L3-G04 | Bash Command Gate | Pattern match + classify: SAFE/MODIFY/RESTRICTED | ALLOW/MODIFY_CHECK/DENY/HITL | <10ms |
| L3-G05 | Sensitive File Gate | Pattern match: *.env, *.key, credentials.*, id_rsa* | ALLOW/DENY_WITH_HITL | <5ms |
| L3-G06 | Write Restriction Gate | Path comparison: audit logs, .context/rules/ | ALLOW/DENY | <1ms |
| L3-G07 | MCP Registry Gate | Hash comparison: server config -> registry | ALLOW/DENY | <5ms |
| L3-G08 | MCP Output Sanitize | Pattern match: strip system prompts, credentials | SANITIZE/PASS | <10ms |
| L3-G09 | Delegation Gate | Multi-check: identity, depth, privilege intersection | ALLOW/DENY | <5ms |
| L3-G10 | Schema Validation | JSON Schema: agent definition validation | VALID/INVALID | <15ms |
| L3-G11 | URL Allowlist | Domain match: block internal IPs | ALLOW/DENY | <1ms |
| L3-G12 | Env Var Filter | Pattern match: strip API keys, tokens | FILTER/PASS | <1ms |

**Total worst-case L3 latency:** ~50ms (all gates sequential) -- meets NFR-SEC-001. [ps-architect-001, L3 Gate Registry]

### 3.3 L4 Inspector Specifications (7 Inspectors, <170ms Total)

L4 operates on tool results after execution but before results enter LLM context. Pattern-matching based (not LLM-based) for determinism.

| Inspector ID | Name | Detection Method | Action | Latency |
|-------------|------|-----------------|--------|---------|
| L4-I01 | Injection Pattern Scanner | Regex: 10 categories of injection patterns | Tag SUSPICIOUS; block Trust Level 3 high-confidence | <50ms |
| L4-I02 | Content-Source Tagger | Tool type classification | Tag with {source, trust_level: 0-3} | <5ms |
| L4-I03 | Secret Detection Scanner | Regex: API keys (AKIA, ghp_, sk-), passwords, L2 markers | Redact; CRITICAL event | <30ms |
| L4-I04 | System Prompt Canary | Canary token detection in output | Redact surrounding context | <10ms |
| L4-I05 | Handoff Integrity Verifier | SHA-256 hash verification, schema validation | Reject on integrity failure | <20ms |
| L4-I06 | Behavioral Drift Monitor | Action sequence vs. declared task and cognitive mode | Advisory/HITL at drift | <50ms |
| L4-I07 | Audit Logger | Structured JSON-lines logging | Append to session log | <5ms |

**Total worst-case L4 latency:** ~170ms (all inspectors sequential) -- meets NFR-SEC-001. [ps-architect-001, L4 Inspector Registry]

### 3.4 L5 CI Gate Specifications (8 Gates)

| Gate ID | Name | Trigger | Pass Criteria |
|---------|------|---------|---------------|
| L5-S01 | Agent Definition Security | Commit modifying agents | 100% schema pass; P-003/P-020/P-022 present |
| L5-S02 | L2 Marker Integrity | Commit modifying rules | All markers present; count matches |
| L5-S03 | MCP Config Validation | Commit modifying settings | All servers in registry; hashes match |
| L5-S04 | Sensitive File Audit | Every commit | No .env, *.key committed |
| L5-S05 | Dependency Vulnerability Scan | Commit modifying uv.lock | No CRITICAL/HIGH CVEs |
| L5-S06 | Tool Tier Consistency | Commit modifying agents | No tool above declared tier |
| L5-S07 | HARD Rule Ceiling | Commit modifying quality-enforcement.md | Count <= 25 (or <= 28 with exception) |
| L5-S08 | Toxic Combination Registry | Commit modifying toxic config | All Rule of Two violations documented |

[ps-architect-001, L5 Security CI Gates]

### 3.5 Trust Boundary Enforcement Matrix

The architecture defines 5 trust zones (Z0-Z4) with 10 trust boundary crossings (TB-01 through TB-10). Each crossing has specific L3/L4/L5 controls.

| Boundary | From -> To | Most Critical Control | Risk Addressed |
|----------|-----------|----------------------|----------------|
| TB-02 | Z4 (External) -> Z2 (Agent) | L4 Tool-Output Firewall | R-PI-002 (504) |
| TB-03 | Z3 (Data) -> Z2 (Agent) | L4 Content scanning | R-PI-003 (392) |
| TB-04 | Z2 (Agent) -> Z2 (Agent) | L3 Delegation Gate | R-PE-004 (280), R-IC-001 (288) |
| TB-05 | Z2 (Agent) -> Z4 (External) | L3 MCP Output Sanitization | FR-SEC-013, R-DE-006 (240) |
| TB-07 | Z2 (Agent) -> Z4 (External) | L3 Bash Command Gate | R-IT-006 (300) |
| TB-09 | Z1 (Governance) -> Z2 (Agent) | L2 Per-prompt Re-injection | R-GB-001 (432) |

The Trust Boundary Enforcement Matrix maps each enforcement layer's role at all 10 boundaries. L3 provides primary enforcement at 7 boundaries; L4 at 4 boundaries; L5 at 3 boundaries. No boundary lacks at least two layers of enforcement. [ps-architect-001, Trust Boundary Analysis ST-021]

### 3.6 Requirements Traceability (57 Requirements -> Architecture)

All 57 requirements are now architecturally addressed:

| Category | Phase 1 Count | Phase 2 Count | Change |
|----------|---------------|---------------|--------|
| Fully Covered | 13 | 57 | +44 |
| Partial Coverage | 26 | 0 | -26 |
| No Coverage | 18 | 0 | -18 |

**Subsystem allocation summary:**

| Subsystem | Primary Count | Supporting Count |
|-----------|---------------|------------------|
| SS-L3 (Pre-Tool Gate) | 19 | 19 |
| SS-L4 (Post-Tool Firewall) | 15 | 17 |
| SS-L5 (CI/Commit) | 5 | 13 |
| SS-AUD (Audit Trail) | 4 | 12 |
| SS-AID (Agent Identity) | 4 | 3 |
| SS-L2 (Per-Prompt) | 2 | 6 |
| SS-L1 (Session Start) | 2 | 2 |

The formal architecture (nse-architecture-001) provides bidirectional traceability: every requirement maps to a primary subsystem and covering gates, and every gate maps back to its driving requirements. [ps-architect-001, Requirements Traceability Matrix; nse-architecture-001, Security Requirements Allocation]

---

## 4. Security Pattern Recommendations

### 4.1 Pattern Catalog Overview (47 Patterns, 7 Research Areas)

ps-researcher-003 identified 47 concrete security patterns across 7 research areas from 60+ sources (academic, industry frameworks, production implementations). Patterns are organized by applicability to Jerry's enforcement layers.

| Research Area | Pattern Count | Key Patterns | Jerry Layer |
|--------------|---------------|-------------|-------------|
| L3/L4 Security Gate Patterns | 5 | Guardrails-by-Construction (1.1), Tool-Output Firewall (1.2), CaMeL dual-model (1.3), Command Classification (1.5) | L3, L4 |
| MCP/Tool Supply Chain | 4 | MCP Integrity Pipeline (2.1), Hash Pinning (2.2), AI BOM (2.3), Runtime Monitoring (2.4) | L3, L4, L5 |
| Agent Identity and Auth | 4 | Delegation Capability Tokens (3.1), Entra Model (3.2), Token Vault (3.3), Scope Attenuation (3.4) | L3 |
| Prompt Injection Defense | 5 | Spotlighting/Content-Source Tagging (4.1), Google 5-Layer (4.2), PALADIN (4.3), RL Defense (4.5) | L2, L3, L4 |
| Context Integrity | 4 | Watchdog Timer (5.1), Protection Rings (5.2), Session Partitioning (5.3), Rule File Integrity (5.4) | L1, L2, L3 |
| Rogue Agent Detection | 4 | Behavioral Baseline (6.1), Goal Consistency (6.2), Kill Switch (6.3), Consensus Validation (6.4) | L4 |
| Zero-Trust Architecture | 4 | Agent-Aware Zero Trust (7.1), Dynamic Trust Decay (7.2), Microsegmentation (7.3), Per-Request Verification (7.4) | L3, L4 |

[ps-researcher-003, Pattern Catalog and Defense-in-Depth Model]

### 4.2 Top 7 Integration Recommendations (Priority Ordered)

| Priority | Recommendation | Patterns | Aggregate RPN | Requirements Addressed |
|----------|---------------|----------|---------------|----------------------|
| 1 | Implement L4 Tool-Output Firewall | 1.2, 4.1 | 1,636 | FR-SEC-012, 013, 017, 018, 019 |
| 2 | Implement L3 Security Gate Pipeline | 1.1, 1.5, 3.4, 7.4 | 1,285+ | FR-SEC-005-009, 011, 026, 039 |
| 3 | Implement MCP Supply Chain Verification | 2.1, 2.2, 2.3 | 1,198 | FR-SEC-025-028 |
| 4 | Implement Lightweight Agent Identity | 3.1, 3.2, 3.4 | 693 | FR-SEC-001-004, 024 |
| 5 | Implement Behavioral Monitoring and Containment | 6.1, 6.2, 6.3, 7.2 | 1,054 | FR-SEC-037, 033, 031, 029 |
| 6 | Harden L2 Re-Injection as Security Watchdog | 5.1, 5.2, 5.3, 5.4 | 1,131 | R-GB-001, V-001, V-006 |
| 7 | Implement Comprehensive Audit Trail | OpenTelemetry GenAI, NIST AU | 939 | FR-SEC-029-032 |

[ps-researcher-003, Jerry Integration Recommendations]

### 4.3 Gap Areas Where Jerry Must Innovate

| Gap | Description | Innovation Required | Industry Status |
|-----|-------------|-------------------|----------------|
| L2 Re-injection as Security Mechanism | No direct industry analog; closest are watchdog timers and memory protection rings | Harden from behavioral to security enforcement with integrity verification | No external equivalent |
| Context Rot as Security Threat | No framework models L1 rule degradation under context pressure | Formalize as security metric with quantified degradation curves and trust decay | Falls between ATLAS AML.T0080 and OWASP ASI06 |
| MCP Protocol Security Standards | OWASP guide and Cisco scanner are emerging but immature | Define Jerry-specific MCP security policy exceeding draft spec | Emerging (Feb 2026) |
| Real-Time Toxic Combination Detection | Meta's Rule of Two constraint exists; no production implementation | L3 gate tracking real-time property accumulation per agent | Meta theoretical only |
| Quality Gate Security | No framework addresses adversarial manipulation of LLM-as-Judge scoring | Multi-scorer consensus, calibration, deterministic pre-checks | Jerry-specific (V-005) |

[ps-researcher-003, Gap Analysis]

---

## 5. Verification Priorities for nse-verification-001

### 5.1 Highest-Risk Architecture Decisions

The following decisions carry the highest verification priority because they address the highest-RPN risks and have the most complex implementations.

| Priority | Decision | Risk | Why Highest Verification Priority |
|----------|----------|------|-----------------------------------|
| 1 | AD-SEC-02 (Tool-Output Firewall) | R-PI-002 (RPN 504) | Addresses the #1 risk with the highest aggregate RPN reduction (1,636). Injection pattern detection effectiveness is empirically unvalidated (OI-02). False positive/negative rates unknown. Content-source tagging mechanism at model level needs prototyping (OI-04). |
| 2 | AD-SEC-01 (L3 Gate Infrastructure) | Foundation for all L3 | Single point of failure for all L3 enforcement. If the gate pipeline framework has defects, all downstream L3 gates inherit them. Must verify: gate ordering, fail-closed behavior, ALLOW/DENY/HITL handling, latency under load. |
| 3 | AD-SEC-03 (MCP Verification) | R-SC-001 (RPN 480) | Closes the only full GAP in OWASP Agentic matrix (ASI-04). Hash pinning implementation must be verified for: registry format correctness, hash mismatch detection, unregistered server blocking, CI validation. Cisco MCP scanner integration is unvalidated (OI-03). |
| 4 | AD-SEC-06 (Context Rot Hardening) | R-GB-001 (RPN 432) | Addresses a Jerry-specific threat with no industry precedent. L2 Tier A promotion of H-18 consumes L2 token budget (559 -> ~599 of 850). Must verify: H-18 marker presence, L2 budget compliance, AE-006 enforcement strengthening, behavioral verification at elevated context fill. |
| 5 | AD-SEC-04 (Bash Hardening) | R-IT-006 (RPN 300) | Command classification SAFE/MODIFY/RESTRICTED must be verified for: complete coverage of dangerous commands, metacharacter sanitization effectiveness, per-tier allowlist correctness, HITL invocation for RESTRICTED category. |

[ps-architect-001, Architecture Decisions, Risk Reduction values; Open Issues OI-02, OI-03, OI-04]

### 5.2 Requirements Needing Most Rigorous V&V

| Requirement | Priority | Why Rigorous V&V Required |
|-------------|----------|--------------------------|
| FR-SEC-012 (Indirect Injection Prevention) | CRITICAL | Addresses #1 risk (RPN 504). Regex-based detection has inherent false negatives for novel patterns (AR-02). Must test against OWASP injection test suite and novel attack payloads. |
| FR-SEC-025 (MCP Server Integrity) | CRITICAL | Only full GAP closure. Verify hash pinning, registry enforcement, config drift detection. |
| FR-SEC-005/006 (Tool Access/Tier Enforcement) | CRITICAL | Transforms advisory tier system into runtime enforcement. Zero false negatives required: no tool invocation may bypass L3 gate (AC per FR-SEC-005). |
| FR-SEC-033 (Agent Containment) | CRITICAL | Kill switch mechanism. Must verify: containment triggers fire correctly, all tool invocations halt, forensic snapshot captured, user notification works. |
| NFR-SEC-001 (Latency Budget) | HIGH | L3 <50ms, L4 <200ms. Must be validated under realistic load, not just worst-case arithmetic. |
| NFR-SEC-006 (Fail-Closed Default) | CRITICAL | Every gate and inspector must fail closed on error. Verify by inducing failures in each component. |

[ps-architect-001, Requirements Traceability Matrix; nse-requirements-002, Acceptance Criteria]

### 5.3 Known Weak Points

| Weak Point | Location | Impact | Verification Approach |
|------------|----------|--------|----------------------|
| L4-I01 seed injection patterns (10 categories) may miss novel attacks | L4 Inspector Registry | False negatives allow injection bypass | Run OWASP injection test suite + generate novel payloads via /adversary S-001 Red Team. Target: >=95% detection per FR-SEC-011. |
| Content-source tagging effectiveness depends on Claude model compliance | L4-I02 | Tags may be ignored by model reasoning | Prototype multiple tag formats (XML delimiters, system message prefix, base64 encoding per Spotlighting). Measure injection success rate with/without tagging. |
| Bash command classification completeness | L3-G04 | Uncategorized commands may bypass gate | Enumerate all Bash commands used in Jerry workflows. Verify every command maps to SAFE/MODIFY/RESTRICTED. Run fuzzing with command variants. |
| Agent identity is non-cryptographic (Phase 2) | AD-SEC-07 | Name-timestamp-nonce is spoofable if attacker controls context | Accepted risk (AR-03). Verify spoofing resistance within Jerry's P-003 topology (orchestrator generates ID, worker cannot modify). |
| Quality gate S-014 remains manipulable | V-005 | Security deliverables could inflate own scores | Multi-scorer consensus verification. Inject known-bad deliverables and verify scoring correctly identifies defects. |
| Tier B HARD rules (5 rules) lack L2 re-injection | quality-enforcement.md | H-18 promotion closes 1 gap; H-04, H-16, H-17, H-32 remain Tier B | Verify H-18 promotion effectiveness. Assess remaining Tier B rules for context-rot-induced failures at high context fill. |

[ps-architect-001, Accepted Risks AR-01 through AR-04, Open Issues OI-01 through OI-05; ps-researcher-003, Gap Analysis]

---

## 6. Integration Priorities for nse-integration-001

### 6.1 Integration with Existing Jerry Governance

The security architecture is designed as extensions to existing governance, not replacements. The following table maps new security controls to existing Jerry mechanisms they integrate with.

| New Security Control | Existing Jerry Mechanism | Integration Point | Regression Risk |
|---------------------|-------------------------|-------------------|----------------|
| L3 Security Gate Pipeline (AD-SEC-01) | Existing L3 AST gating (H-33, worktracker) | L3 gates are additive checks in the existing L3 pipeline | LOW: additive only; existing L3 checks unchanged |
| L4 Tool-Output Firewall (AD-SEC-02) | Existing L4 self-correction (advisory) | L4 inspectors added to post-tool processing flow | MEDIUM: must not interfere with L4 self-correction or context budget (CB-02) |
| MCP Registry (AD-SEC-03) | MCP tool standards (MCP-001/MCP-002) | New `.context/security/mcp-registry.yaml` alongside existing `.claude/settings.local.json` | LOW: registry is a parallel config file; does not modify existing MCP config |
| Bash Command Gate (AD-SEC-04) | Existing Bash tool usage patterns, H-05 UV-only | L3-G04 classifies commands before Bash execution | MEDIUM: must not block legitimate UV commands (`uv run`, `uv add`, `uv sync`) |
| Secret Detection (AD-SEC-05) | Existing `no_secrets_in_output` guardrail (behavioral) | L4-I03 adds deterministic enforcement to existing behavioral guardrail | LOW: deterministic check supplements behavioral guardrail |
| H-18 Tier A Promotion (AD-SEC-06) | L2 REINJECT markers, L2 token budget (559/850) | Add ~40-token L2 marker for H-18 (599/850 post-promotion) | LOW: within token budget; no existing markers modified |
| Agent Instance ID (AD-SEC-07) | Agent definition `name` field, handoff `from_agent` | System-set `from_agent` replaces agent-supplied value | MEDIUM: handoff consumers must adapt to system-set identity format |
| Handoff Integrity (AD-SEC-08) | Handoff protocol (HD-M-001 through HD-M-005) | SHA-256 hash added to handoff metadata; L4-I05 verifies on receive | LOW: additive fields; existing handoff fields unchanged |
| Audit Trail (AD-SEC-09) | Routing observability (RT-M-008), worktracker entries | New JSON-lines audit log per session; L3-G06 write-protects log directory | LOW: parallel logging system; does not modify routing or worktracker |
| Adversarial Testing (AD-SEC-10) | /adversary skill (S-001 Red Team), L5 CI pipeline | Red team test suite added to L5 CI; automated canary attacks | LOW: extends existing /adversary and CI infrastructure |

[ps-architect-001, all 10 Architecture Decisions; nse-architecture-001, System Decomposition]

### 6.2 L3/L4 Gate Interactions with Existing Enforcement

| Existing Mechanism | New L3/L4 Interaction | Interaction Type | Verification Need |
|-------------------|----------------------|------------------|------------------|
| H-34 Schema Validation (L5 CI) | L3-G10 adds runtime schema check before Task invocation | Complementary: L5 at commit, L3 at runtime | Verify L3-G10 and L5-S01 use identical schema; no divergence |
| H-35 Worker Task Restriction (L5 CI) | L3-G09 enforces P-003 at runtime; blocks Task tool for workers | Complementary: L5 at commit, L3 at runtime | Verify L3-G09 catches cases L5-S01 catches (same restriction, different enforcement point) |
| H-36 Circuit Breaker (3 hops) | L3-G09 delegation depth check integrated with circuit breaker | Extends: routing depth check is part of L3-G09 | Verify routing_depth counter incremented correctly; circuit breaker fires at 3 |
| AE-006 Graduated Escalation | AD-SEC-06 strengthens enforcement at WARNING/CRITICAL/EMERGENCY tiers | Extends: adds security-specific actions at each tier | Verify security actions do not conflict with existing AE-006 behavioral actions |
| T1-T5 Tool Tiers | L3-G01 and L3-G02 enforce tiers at runtime | Transforms: from advisory (L5-only) to enforced (L3+L5) | Most critical regression test: verify T1 agents can still Read; T2 can still Write within project scope |
| P-020 User Authority | L3 HITL mechanism for RESTRICTED operations | Preserves: P-020 is maintained; HITL adds structured approval | Verify HITL approval flow does not override P-020 or add unintended friction to C1 tasks |
| CB-02 Tool Result Budget (50%) | L4-I02 content-source tagging adds metadata to results | Potential conflict: tagging increases result size; may push closer to CB-02 threshold | Measure content-source tag overhead; ensure tagging overhead does not meaningfully impact CB-02 compliance |

[ps-architect-001, Trust Boundary Enforcement Matrix; nse-architecture-001, Interface Definitions; quality-enforcement.md, enforcement architecture]

### 6.3 Regression Risks

| Risk | Severity | Scenario | Mitigation |
|------|----------|----------|------------|
| L3 gates block legitimate operations | HIGH | Overly strict allowlists prevent normal agent workflow (e.g., T2 agent cannot `git commit`) | Verify per-tier command allowlists include all commands used in current Jerry workflows. Test with existing agent definitions before enabling enforcement. |
| L4 injection scanner flags technical documentation | MEDIUM | Documentation containing phrases like "ignore previous" or code examples with injection patterns triggers false positives | Trust Level 2 sources (project files) produce advisory warnings only, not blocks. Tune sensitivity thresholds based on false positive rate. |
| Content-source tagging increases context consumption | LOW | L4-I02 metadata on every tool result increases context fill rate, triggering AE-006 earlier | Measure tag overhead per tool result (estimated <50 tokens). Adjust AE-006 thresholds if needed. |
| Agent identity format change breaks handoff consumers | MEDIUM | System-set `from_agent` uses instance ID format (`name-timestamp-nonce`) instead of plain agent name | Verify all handoff consumers (orch-tracker, orch-synthesizer, skill orchestrators) handle new format. Consider backward-compatible format with plain name plus instance suffix. |
| MCP registry blocks development workflows | LOW | BLOCK policy for unregistered servers prevents adding new MCP servers without registry update | Use ALLOW_WITH_HITL policy for development; BLOCK for production. Document registry update process. |

[ps-architect-001, Trade-offs in AD-SEC-01 through AD-SEC-10; nse-architecture-001, Trust Boundaries]

---

## 7. Compliance Mapping

### 7.1 OWASP Agentic Top 10 (Post-Architecture)

| OWASP Item | Phase 1 Status | Post-Architecture Status | Key Architecture Response |
|------------|---------------|------------------------|--------------------------|
| ASI-01 Agent Goal Hijack | PARTIAL | **COVERED** | AD-SEC-02 (Tool-Output Firewall), AD-SEC-06 (Context Rot), L4-I01 |
| ASI-02 Tool Misuse | PARTIAL | **COVERED** | AD-SEC-01 (L3 Tool Access Matrix), AD-SEC-04 (Bash Hardening) |
| ASI-03 Privilege Escalation | PARTIAL | **COVERED** | AD-SEC-01 (Tier Enforcement), Privilege Non-Escalation, Rule of Two |
| ASI-04 Supply Chain | **GAP** | **COVERED** | AD-SEC-03 (MCP Verification), L5-S03/S05, Registry |
| ASI-05 Code Execution | PARTIAL | **COVERED** | AD-SEC-04 (Bash Hardening), L3-G04 |
| ASI-06 Memory/Context Poisoning | PARTIAL | **COVERED** | AD-SEC-06 (Context Rot), AD-SEC-02 (Content-Source Tagging) |
| ASI-07 Inter-Agent Comm | PARTIAL | **COVERED** | AD-SEC-08 (Handoff Integrity), SHA-256 hashing |
| ASI-08 Cascading Failures | PARTIAL | **COVERED** | H-36 circuit breaker, Fail-Closed design |
| ASI-09 Insufficient Logging | PARTIAL | **COVERED** | AD-SEC-09 (Audit Trail), L4-I07 |
| ASI-10 Rogue Agents | PARTIAL | **COVERED** | AD-SEC-01, L4-I06 (Behavioral Drift), AD-SEC-07 |

**Result: 10/10 COVERED** (up from 0/10 COVERED, 9/10 PARTIAL, 1/10 GAP). [ps-architect-001, Cross-Framework Compliance Mapping]

### 7.2 MITRE ATLAS Agent Techniques (Post-Architecture)

| Status | Count | Items |
|--------|-------|-------|
| COVERED | 7/9 | AML.T0080, T0080.000, T0080.001, T0081, T0082, T0083, T0086 |
| PARTIAL (accepted) | 2/9 | AML.T0084, T0084.002 (agent config readable by design per P-022) |

The 2 remaining PARTIAL items are accepted risks: Jerry's architecture requires readable agent definitions and trigger maps for the framework to function. Hiding them would violate P-022 (no deception). [ps-architect-001, MITRE ATLAS mapping]

### 7.3 NIST SP 800-53 Key Control Families (Post-Architecture)

| Family | Phase 1 Status | Post-Architecture Status |
|--------|---------------|------------------------|
| AC (Access Control) | PARTIAL | **COVERED** -- AD-SEC-01 (L3 runtime), Rule of Two |
| AU (Audit) | **GAP** | **COVERED** -- AD-SEC-09 (Audit Trail) |
| CM (Configuration Mgmt) | PARTIAL | **COVERED** -- L3 hash verification, L5-S01/S02/S03 |
| IA (Identification) | **GAP** | **COVERED** -- AD-SEC-07 (Agent Identity, foundational; full crypto Phase 3) |
| IR (Incident Response) | PARTIAL | **COVERED** -- Fail-closed, containment, graduated degradation |
| SC (System Protection) | PARTIAL | **COVERED** -- L3-G11 (URL allowlist), content-source tagging |
| SI (System Integrity) | PARTIAL | **COVERED** -- AD-SEC-02 (L4 Firewall), L3 input validation |
| SR (Supply Chain) | **GAP** | **COVERED** -- AD-SEC-03 (MCP Verification), L5-S05 |
| SA (System Acquisition) | PARTIAL | **COVERED** -- MCP registry, agent schema validation |
| RA (Risk Assessment) | COVERED | **COVERED** -- Phase 1 FMEA + this threat model |

**Result: 10/10 COVERED** (up from 1/10 COVERED, 6/10 PARTIAL, 3/10 GAP). [ps-architect-001, NIST SP 800-53 mapping]

---

## 8. Blockers and Risks

### 8.1 Blockers Carried Forward from Barrier 1

| # | Blocker | Status | Phase 2 Resolution |
|---|---------|--------|-------------------|
| B1-1 | MCP protocol immaturity (no standardized integrity verification) | **PARTIALLY MITIGATED** | Architecture designs verification at Jerry configuration layer (hash pinning, registry) rather than protocol layer. MCP protocol evolution should be monitored. |
| B1-2 | L3/L4 enforcement requires Claude Code architecture knowledge | **OPEN** | Architecture designs gates as additive pipeline stages. Actual integration with Claude Code's tool invocation pipeline is an implementation-phase concern. |
| B1-3 | No empirical FMEA calibration | **OPEN** | Accept current rankings. AD-SEC-10 (Adversarial Testing) provides calibration mechanism post-implementation. |

[Barrier 1 handoff, Section 8]

### 8.2 New Blockers from Phase 2

| # | Blocker | Impact | Severity |
|---|---------|--------|----------|
| B2-1 | L4 injection pattern database effectiveness unvalidated (OI-02) | False positive/negative rates unknown until deployment. NFR-SEC-012 requires >=95% detection. | HIGH |
| B2-2 | Content-source tagging mechanism at model level unprototyped (OI-04) | Tag format effectiveness (XML delimiters vs. system messages vs. encoding) depends on Claude API capabilities. | MEDIUM |
| B2-3 | Cisco MCP Scanner integration feasibility unvalidated (OI-03) | Open-source scanner capabilities may not match FR-SEC-025 requirements. | MEDIUM |
| B2-4 | Cryptographic delegation tokens deferred to Phase 3 (OI-05) | Phase 2 identity is non-cryptographic. Non-repudiation unavailable until DCT implementation. | LOW (accepted risk AR-03) |

[ps-architect-001, Open Issues OI-02 through OI-05]

### 8.3 Risks to Phase 3

| # | Risk | Likelihood | Impact | Mitigation |
|---|------|-----------|--------|------------|
| R3-1 | L3/L4 security gates conflict with existing non-security L3/L4 behavior | MEDIUM | Architecture rework | Security designed as extensions, not replacements. Integration tests critical. |
| R3-2 | Security token overhead pushes context fill past AE-006 thresholds | LOW | Reduced work context | L3 gates zero tokens; L4 compact output; L2 budget 559 -> ~599 (within 850 limit). |
| R3-3 | Performance degradation from cumulative L3/L4 latency | LOW | UX degradation | Total: L3 50ms + L4 170ms = 220ms per tool invocation vs. 1-30s LLM inference time. |
| R3-4 | Regex injection detection has inherent false negatives for novel attacks | HIGH | Security gap remains | Defense-in-depth: L2 re-injection resilient even when injection succeeds. AD-SEC-10 continuous calibration. |
| R3-5 | HARD rule ceiling at 25/25 with zero headroom constrains future security needs | MEDIUM | Cannot add new HARD rules | All security controls implemented without new HARD rules. Ceiling exception mechanism available (max N=3, 3-month duration). |
| R3-6 | [PERSISTENT] Integration complexity between Track A (L3), Track B (L4), and Track C (Identity) | MEDIUM | Coordination overhead | Tracks designed for independent implementation. Integration points are well-defined interfaces. Verify interfaces before parallel implementation. |

[ps-architect-001, Risks to Implementation RI-01 through RI-03; Open Issues]

---

## 9. Artifact References

### 9.1 PS Phase 2 Artifacts (Input to This Handoff)

| Artifact | Agent | Path |
|----------|-------|------|
| Security Architecture | ps-architect-001 | `projects/PROJ-008-agentic-security/orchestration/agentic-sec-20260222-001/ps/phase-2/ps-architect-001/ps-architect-001-security-architecture.md` |
| Security Pattern Research | ps-researcher-003 | `projects/PROJ-008-agentic-security/orchestration/agentic-sec-20260222-001/ps/phase-2/ps-researcher-003/ps-researcher-003-security-patterns.md` |

### 9.2 NSE Phase 2 Artifacts (Available to Receiving Agents)

| Artifact | Agent | Path |
|----------|-------|------|
| Formal Security Architecture | nse-architecture-001 | `projects/PROJ-008-agentic-security/orchestration/agentic-sec-20260222-001/nse/phase-2/nse-architecture-001/nse-architecture-001-formal-architecture.md` |
| Requirements Baseline (BL-SEC-001) | nse-requirements-002 | `projects/PROJ-008-agentic-security/orchestration/agentic-sec-20260222-001/nse/phase-2/nse-requirements-002/nse-requirements-002-requirements-baseline.md` |

### 9.3 Cross-Pollination Predecessor

| Artifact | Path |
|----------|------|
| Barrier 1 PS-to-NSE Handoff | `projects/PROJ-008-agentic-security/orchestration/agentic-sec-20260222-001/cross-pollination/barrier-1/ps-to-nse/handoff.md` |

### 9.4 PS Phase 1 Artifacts (Referenced Transitively)

| Artifact | Agent | Path |
|----------|-------|------|
| Competitive Landscape | ps-researcher-001 | `projects/PROJ-008-agentic-security/orchestration/agentic-sec-20260222-001/ps/phase-1/ps-researcher-001/ps-researcher-001-competitive-landscape.md` |
| Threat Framework Analysis | ps-researcher-002 | `projects/PROJ-008-agentic-security/orchestration/agentic-sec-20260222-001/ps/phase-1/ps-researcher-002/ps-researcher-002-threat-framework-analysis.md` |
| Gap Analysis | ps-analyst-001 | `projects/PROJ-008-agentic-security/orchestration/agentic-sec-20260222-001/ps/phase-1/ps-analyst-001/ps-analyst-001-gap-analysis.md` |

### 9.5 NSE Phase 1 Artifacts (Referenced Transitively)

| Artifact | Agent | Path |
|----------|-------|------|
| Security Requirements | nse-requirements-001 | `projects/PROJ-008-agentic-security/orchestration/agentic-sec-20260222-001/nse/phase-1/nse-requirements-001/nse-requirements-001-security-requirements.md` |
| Risk Register (FMEA) | nse-explorer-001 | `projects/PROJ-008-agentic-security/orchestration/agentic-sec-20260222-001/nse/phase-1/nse-explorer-001/nse-explorer-001-risk-register.md` |

### 9.6 Jerry Framework Rules (Referenced Throughout)

| File | Key Content |
|------|-------------|
| `.context/rules/quality-enforcement.md` | L1-L5 enforcement architecture, HARD Rule Index (25/25), Two-Tier Model, L2 token budget (559/850), AE-006, criticality |
| `.context/rules/agent-development-standards.md` | T1-T5 tool tiers, handoff protocol, H-34/H-35, guardrails template, CB-01-CB-05 |
| `.context/rules/agent-routing-standards.md` | Circuit breaker H-36, anti-pattern catalog, FMEA monitoring thresholds |
| `.context/rules/mcp-tool-standards.md` | MCP-001/MCP-002, canonical tool names, error handling, agent integration matrix |
| `CLAUDE.md` | Constitutional constraints (P-003, P-020, P-022), H-04, H-05 |

---

## 10. Citations

All claims in this handoff document trace to specific PS Phase 2 artifacts or Jerry framework rules. Citations use the format `[artifact, section/identifier]`.

### Claim-to-Source Trace Table

| Claim | Source |
|-------|--------|
| "All 57 requirement gaps closed without new HARD rules" | ps-architect-001, RTM Coverage Summary (line 1105-1110); Architecture Decisions, HARD Rule Impact (all 10 decisions state "No new HARD rules") |
| "L3 has 12 deterministic gates totaling <50ms" | ps-architect-001, L3 Gate Registry (lines 554-568) |
| "L4 has 7 inspectors totaling <170ms" | ps-architect-001, L4 Inspector Registry (lines 588-656) |
| "8 L5 CI gates" | ps-architect-001, L5 Security CI Gates (lines 662-672) |
| "19 requirements allocate to L3 as primary" | nse-architecture-001, Allocation Summary (line 434) |
| "15 requirements allocate to L4 as primary" | nse-architecture-001, Allocation Summary (line 435) |
| "47 patterns from 60+ sources" | ps-researcher-003, Executive Summary (line 32) |
| "Deterministic gating is the industry consensus" | ps-researcher-003, Finding 1 (lines 36-37) |
| "Content-source tagging is the critical missing defense" | ps-researcher-003, Finding 2 (lines 38-39) |
| "Defense-in-depth reduces attacks from 73.2% to 8.7%" | ps-researcher-003, Pattern 4.3 PALADIN (line 276) |
| "L2 re-injection has no direct industry analog" | ps-researcher-003, Finding 7 (lines 47-48); Gap Analysis Gap 1 (lines 599-607) |
| "5 innovation areas where Jerry must go beyond industry" | ps-researcher-003, Gap Analysis (lines 595-639) |
| "Top 5 FMEA risks covered by 2+ layers" | ps-architect-001, Defense Layering table in Executive Summary (lines 46-53) |
| "R-PI-002 is #1 risk at RPN 504" | ps-architect-001, DREAD Scoring (line 137); nse-explorer-001 (Category 1) |
| "AD-SEC-02 has highest aggregate RPN reduction (1,636)" | ps-architect-001, AD-SEC-02 Risk Reduction (line 826); ps-researcher-003, Recommendation 1 (line 510) |
| "MCP Supply Chain is only full GAP in OWASP Agentic matrix" | ps-architect-001, OWASP Agentic Compliance (line 982); ps-analyst-001, Gap Matrix ASI04 |
| "OWASP post-architecture: 10/10 COVERED" | ps-architect-001, Cross-Framework Compliance (line 990) |
| "NIST post-architecture: 10/10 COVERED" | ps-architect-001, NIST Key Control Families (line 1023) |
| "MITRE post-architecture: 7/9 COVERED, 2 accepted" | ps-architect-001, MITRE ATLAS (line 1006) |
| "Recommended implementation order: AD-SEC-01 first" | ps-architect-001, Decision Dependency Map (lines 959-969) |
| "Trust boundary enforcement: 5 zones, 10 crossings" | ps-architect-001, Trust Boundary Analysis ST-021 (lines 288-329) |
| "Toxic combination registry enforces Meta Rule of Two" | ps-architect-001, Zero-Trust Model ST-022 (lines 409-451) |
| "L2 token budget impact: 559 -> ~599 of 850" | ps-architect-001, AD-SEC-06 (line 886) |
| "Agent instance ID format: {name}-{timestamp}-{nonce}" | ps-architect-001, AD-SEC-07 (line 895); nse-architecture-001, SS-AID (line 239) |
| "57 requirements (42 FR + 15 NFR)" | nse-requirements-002, Baseline Metadata (line 52) |
| "BL-SEC-001 baseline version 1.0.0" | nse-requirements-002, Baseline Metadata (line 47) |
| "Subsystem decomposition: 5 primary + 2 cross-cutting" | nse-architecture-001, System Decomposition (line 114) |
| "Content-source tagging mechanism unprototyped" | ps-architect-001, Open Issue OI-04 (line 1150) |
| "Cisco MCP scanner integration unvalidated" | ps-architect-001, Open Issue OI-03 (line 1149) |
| "Injection pattern database needs empirical calibration" | ps-architect-001, Open Issue OI-02 (line 1148) |
| "Phase 2 identity is non-cryptographic" | ps-architect-001, Accepted Risk AR-03 (line 1140) |
| "L4 injection detection has inherent false negatives" | ps-architect-001, Accepted Risk AR-02 (line 1139) |
| "Barrier 1 transferred 7 key findings" | Barrier 1 handoff, Section 2 Key Findings (lines 39-56) |
| "HARD rule ceiling at 25/25 with zero headroom" | quality-enforcement.md, HARD Rule Ceiling; ps-architect-001, OI-01 (line 1147) |

---

*Handoff version: 1.0.0 | Cross-pollination: Barrier 2, PS to NSE | Workflow: agentic-sec-20260222-001 | Date: 2026-02-22*
*Self-review (S-010) completed: Navigation table with anchors (H-23), all 10 required sections present, every claim cited to source artifact, file paths only in artifact references (CB-03), 7 key findings for orientation (CB-04), C4 criticality with actionable verification/integration priorities.*
