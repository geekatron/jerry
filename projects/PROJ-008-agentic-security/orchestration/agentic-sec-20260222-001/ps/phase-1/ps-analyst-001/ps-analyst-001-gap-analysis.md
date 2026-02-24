# Security Gap Analysis: Jerry Framework vs. Agentic Threat Landscape

> Agent: ps-analyst-001
> Phase: 1 (Gap Analysis)
> Pipeline: PS (Problem-Solving)
> Status: COMPLETE
> Date: 2026-02-22
> Criticality: C4

## Document Sections

| Section | Purpose |
|---------|---------|
| [Executive Summary](#executive-summary) | Overall gap assessment, top 5 gaps, top 5 strengths |
| [Gap Matrix](#gap-matrix) | Comprehensive threat-to-control mapping (COVERED/PARTIAL/GAP/NOT_APPLICABLE) |
| [Priority Ranking](#priority-ranking) | All gaps ranked by risk, feasibility, competitive impact, dependency |
| [Jerry Strengths Analysis](#jerry-strengths-analysis) | Existing strengths mapped to threats they mitigate |
| [Competitive Gap Comparison](#competitive-gap-comparison) | Jerry vs. Claude SDK, Claude Code, Microsoft Agent 365 per critical gap |
| [Requirements-to-Gap Mapping](#requirements-to-gap-mapping) | 57 requirements mapped to gap status |
| [Recommended Phase 2 Architecture Priorities](#recommended-phase-2-architecture-priorities) | Top 10 architecture decisions with risk reduction and complexity |
| [Citations](#citations) | All claims traced to source artifacts |

---

## Executive Summary

**Overall Assessment: Jerry is among the most architecturally secure agentic frameworks in existence, but has critical gaps in runtime enforcement, supply chain verification, and observability that leave it vulnerable to the dominant attack classes of 2026.**

Jerry's 5-layer enforcement architecture (L1-L5), constitutional HARD rules, tool tier system (T1-T5), and structured handoff protocol place it ahead of every open-source agentic framework analyzed (OpenClaw, claude-flow, Cline) and comparable to Anthropic's Claude Code in architectural sophistication. The L2 per-prompt re-injection mechanism is a genuinely novel defense against context rot that no other framework replicates. However, Jerry's defenses are concentrated at design-time (schema validation, CI gates) and behavioral layers (L1 rules, L2 re-injection), with significant gaps in runtime deterministic enforcement (L3 security gates), tool output sanitization (L4 security inspection), and supply chain verification -- precisely the areas where the 2026 threat landscape demands the strongest controls.

The 60 FMEA failure modes in the risk register yield 5 risks with RPN >= 400 (Critical threshold): indirect prompt injection via MCP tool results (504), malicious MCP server packages (480), constitutional circumvention via context rot (432), false negatives in security controls (405), and indirect prompt injection via file contents (392). All five exploit gaps in Jerry's L3/L4 enforcement layers. The convergent conclusion: **Jerry's architecture is sound but its runtime enforcement is incomplete**.

### Top 5 Critical Gaps

| # | Gap | RPN Impact | Why Critical |
|---|-----|-----------|--------------|
| 1 | **No Tool-Output Firewall**: MCP tool results and file Read outputs enter LLM context without sanitization or source-tagging. The LLM cannot distinguish trusted instructions from untrusted data. | 1,636 (aggregate) | Root cause of the #1 risk (R-PI-002, RPN 504). Every framework, from OWASP to MITRE to Cisco, identifies this instruction/data confusion as the primary agentic attack vector. Jerry mandates MCP usage (MCP-001, MCP-002) but has no defense against poisoned responses. |
| 2 | **No MCP Supply Chain Verification**: MCP servers are configured manually in `.claude/settings.local.json` with no integrity checking, no allowlisted registry, no runtime monitoring. | 1,198 (aggregate) | Root cause of the #2 risk (R-SC-001, RPN 480). Cisco calls MCP "a vast unmonitored attack surface." The ClawHavoc campaign (800+ malicious skills) and Cline supply chain attack demonstrate this is an active, scalable attack class. |
| 3 | **Bash Tool Unrestricted Execution**: No command allowlisting, blocklisting, or argument sanitization. Any T2+ agent can execute arbitrary system commands. | 1,285 (aggregate) | Creates 5 distinct attack paths (credential harvesting, data exfiltration, SSRF, command injection, privilege escalation). The single most powerful attack surface in Jerry's architecture. |
| 4 | **No Runtime Agent Identity or Authentication**: Agents are identified by string names in YAML with no cryptographic verification. Handoff `from_agent` fields can be spoofed. No delegation tokens. | 693 (aggregate) | Identity is the prerequisite for access control, audit attribution, and anti-spoofing. Microsoft's Entra Agent ID establishes this as a foundational enterprise requirement. Without runtime identity, Jerry cannot reliably attribute actions or prevent agent impersonation. |
| 5 | **No Comprehensive Audit Trail**: Routing observability (RT-M-008) covers routing decisions but not tool execution, credential access, agent behavioral anomalies, or security events. | 765 (aggregate) | OWASP ASI09, Cisco State of AI Security 2026, and NIST 800-53 AU family all identify insufficient logging as a top-10 agentic risk. Without comprehensive audit trails, attacks cannot be detected post-hoc and forensic analysis is impossible. |

### Top 5 Existing Strengths

| # | Strength | Industry Validation |
|---|----------|---------------------|
| 1 | **L2 Per-Prompt Re-Injection (Context Rot Immunity)**: 20 Tier A HARD rules re-injected on every prompt, immune to context rot. No other framework has an equivalent mechanism. | Validates the core insight from GTG-1002 and Google DeepMind's joint study: behavioral guardrails degrade under context pressure. Jerry's L2 mechanism is architecturally superior to all competitors in this specific dimension. |
| 2 | **5-Layer Defense-in-Depth (L1-L5)**: Independently operating enforcement layers with documented context-rot immunity per layer. L3 and L5 are fully immune; L2 is immune; L1 is vulnerable but compensated. | Directly mirrors Google DeepMind's 5-layer defense (Prevention, Detection, Verification, Control, Evolution) and Anthropic's defense-in-depth principle. Industry consensus: this is the only viable strategy. |
| 3 | **P-003 Single-Level Nesting Constraint**: Strict orchestrator-worker topology (max 1 level). Workers cannot spawn sub-workers. Reduces error amplification from 17x (uncoordinated) to ~1.3x (structured handoff). | Multi-agent systems multiply attack surfaces (claude-flow shared memory, OWASP ASI04/ASI07/ASI08). Jerry's P-003 constraint is the strongest topological defense in any agentic framework reviewed. |
| 4 | **Tool Tier System (T1-T5) with Least Privilege Design**: Five security tiers from Read-Only to Full, with selection guidelines, worker restrictions, and per-tier constraints. | Mirrors Claude Code's 4-tier isolation and Meta's Rule of Two principle. Jerry's 5-tier system is more granular than any competitor, though it currently lacks runtime enforcement. |
| 5 | **Constitutional Governance Architecture**: HARD/MEDIUM/SOFT tier vocabulary, 25-rule ceiling with ceiling exception mechanism, auto-escalation rules (AE-001-006), criticality levels (C1-C4), and the HARD Rule Index as a single source of truth. | No other agentic framework has formalized governance to this degree. Microsoft's SDL for AI and NIST AI RMF GOVERN function describe aspirational governance; Jerry has implemented it. |

---

## Gap Matrix

### OWASP Agentic Top 10 (ASI01-ASI10)

| Threat ID | Threat Name | L1 Rules | L2 Re-Inject | L3 Pre-Tool | L4 Post-Tool | L5 CI | Tool Tiers | Agent Guardrails | Constitutional | Overall |
|-----------|-------------|----------|-------------|-------------|------------|-------|------------|-----------------|---------------|---------|
| ASI01 | Agent Goal Hijack | PARTIAL: H-02 user authority loaded at session start | COVERED: P-020 re-injected every prompt | GAP: No input sanitization for injection patterns | GAP: No tool-output scanning for injection | N/A | N/A | PARTIAL: `input_validation` declared but not enforced at runtime | COVERED: P-020 user authority, P-022 no deception | **PARTIAL** |
| ASI02 | Tool Misuse & Exploitation | PARTIAL: Tool tier descriptions in rules | N/A | GAP: Tool tier not enforced at runtime (advisory) | GAP: No argument validation on tool calls | PARTIAL: Schema validates `allowed_tools` in definitions | PARTIAL: T1-T5 tiers defined but not runtime-enforced | COVERED: `forbidden_actions` in every agent | COVERED: P-003 limits delegation scope | **PARTIAL** |
| ASI03 | Identity & Privilege Abuse | N/A | N/A | GAP: No per-task credential scoping | GAP: No privilege tracking across handoff chains | PARTIAL: H-35 validates no Task in workers | PARTIAL: T1-T5 tiers exist but no runtime enforcement of intersection semantics | PARTIAL: `forbidden_actions` include P-003 ref | COVERED: P-003 single-level nesting | **PARTIAL** |
| ASI04 | Supply Chain Vulnerabilities | N/A | N/A | GAP: No MCP server integrity verification | GAP: No content validation on MCP responses | GAP: No MCP config validation in CI | N/A | N/A | N/A | **GAP** |
| ASI05 | Unexpected Code Execution | PARTIAL: Bash tool awareness | N/A | GAP: No command allowlisting/blocklisting | GAP: No static analysis on generated code | N/A | PARTIAL: Bash restricted to T2+ | PARTIAL: `no_executable_code_without_confirmation` in guardrails | COVERED: P-020 requires user consent for destructive ops | **PARTIAL** |
| ASI06 | Memory & Context Poisoning | PARTIAL: AE-006 context fill rules | COVERED: L2 re-injection immune to context rot | GAP: No integrity verification on Memory-Keeper data | GAP: No runtime rule file integrity check | PARTIAL: Git tracks rule file changes | N/A | N/A | N/A | **PARTIAL** |
| ASI07 | Insecure Inter-Agent Comms | PARTIAL: Handoff protocol defined | N/A | GAP: Handoff schema validation not enforced at L3 | GAP: No content scanning on handoff data | N/A | N/A | PARTIAL: Schema defined but enforcement is MEDIUM tier | N/A | **PARTIAL** |
| ASI08 | Cascading Failures | PARTIAL: AP-03/AP-04 anti-patterns | COVERED: H-36 circuit breaker re-injected | COVERED: Circuit breaker at 3 hops (when enforced) | PARTIAL: Error propagation structure defined | N/A | N/A | COVERED: `fallback_behavior` in every agent | N/A | **PARTIAL** |
| ASI09 | Human-Agent Trust Exploitation | PARTIAL: S-010 self-review, H-14 creator-critic | COVERED: P-022 no deception re-injected | N/A | GAP: No forced uncertainty disclosure on outputs | N/A | N/A | PARTIAL: Confidence calibration guidance exists | COVERED: P-022 prevents deceptive output | **PARTIAL** |
| ASI10 | Rogue Agents | PARTIAL: Agent definitions specify behavior | COVERED: Constitutional triplet re-injected | GAP: No runtime behavioral anomaly detection | GAP: No behavioral drift monitoring | COVERED: H-34 schema validation on all agents | N/A | COVERED: Constitutional triplet required per H-35 | COVERED: P-003, P-020, P-022 in every agent | **PARTIAL** |

**Summary**: 0/10 COVERED, 9/10 PARTIAL, 1/10 GAP (ASI04 Supply Chain). Jerry has some defense against every OWASP Agentic threat except supply chain, but in no case is the defense complete. The pattern is consistent: design-time controls (schema, CI) exist but runtime enforcement (L3/L4 security gates) is missing.

### OWASP LLM Top 10 (LLM01-LLM10)

| Threat ID | Threat Name | Jerry Controls | Coverage | Justification |
|-----------|-------------|---------------|----------|---------------|
| LLM01 | Prompt Injection | L2 re-injection, constitutional constraints, P-020 user authority | PARTIAL | L2 re-injection provides strong defense against direct injection. No defense against indirect injection via tool results (the dominant attack vector per all frameworks). |
| LLM02 | Sensitive Information Disclosure | `no_secrets_in_output` in guardrails template, P-022 no deception | PARTIAL | Behavioral guardrail only. No L3/L4 deterministic secret detection. No output filtering for system prompt content. |
| LLM03 | Supply Chain | H-05 UV-only Python, git version control | GAP | No MCP server verification. No dependency vulnerability scanning in CI. No hash verification beyond UV lockfile. |
| LLM04 | Data and Model Poisoning | L2 re-injection for context poisoning defense | PARTIAL | Model poisoning is out of scope (Anthropic's responsibility). Context poisoning addressed by L2 but Memory-Keeper data not integrity-verified. |
| LLM05 | Improper Output Handling | Handoff schema (HD-M-001), P-020 user authority | PARTIAL | Schema validates structure but not content. Agent-generated code lacks static analysis before execution. |
| LLM06 | Excessive Agency | T1-T5 tool tiers, H-35 worker restrictions, P-003 nesting limit | PARTIAL | Tiers are defined and validated at CI but not enforced at runtime L3. An agent can potentially invoke tools above its declared tier. |
| LLM07 | System Prompt Leakage | L2 re-injection (rules present even if extracted), P-022 | PARTIAL | No L4 output filter to detect and redact system prompt content. Constitutional rules, HARD rule details, and enforcement architecture can be extracted via crafted queries. |
| LLM08 | Vector and Embedding Weaknesses | N/A | NOT_APPLICABLE | Jerry does not use RAG, vector databases, or embeddings. Memory-Keeper provides key-value storage, not vector retrieval. |
| LLM09 | Misinformation | S-010 self-review, H-14 creator-critic, S-014 LLM-as-Judge scoring | PARTIAL | Quality gates and adversarial review provide operational mitigation. No forced uncertainty disclosure. Model-level accuracy is out of scope. |
| LLM10 | Unbounded Consumption | AE-006 graduated escalation, H-36 circuit breaker (3 hops), RT-M-010 iteration ceilings | COVERED | Multiple independent controls address token exhaustion and agent loops. Context fill monitoring with graduated response. |

**Summary**: 1/10 COVERED (LLM10), 8/10 PARTIAL, 1/10 GAP (LLM03), 1/10 NOT_APPLICABLE (LLM08). Jerry's strongest coverage is resource consumption control; its weakest is supply chain.

### MITRE ATLAS Agent-Specific Techniques

| Technique ID | Technique Name | Jerry Controls | Coverage | Justification |
|--------------|---------------|---------------|----------|---------------|
| AML.T0080 | AI Agent Context Poisoning | L2 re-injection (immune to context rot), AE-006 context fill monitoring | PARTIAL | L2 provides strong resilience against instruction degradation. No runtime integrity verification on context sources. Memory-Keeper stored data not hash-verified. |
| AML.T0080.000 | Context Poisoning: Memory | Memory-Keeper key namespace, MCP-002 phase boundary storage | GAP | No integrity verification on stored/retrieved Memory-Keeper data. No access control beyond namespace convention. Cross-session poisoning possible. |
| AML.T0080.001 | Context Poisoning: Thread | L2 re-injection of constitutional rules every prompt | PARTIAL | L2 re-injection provides partial resilience. No scanning of tool results for injected instructions before they enter the thread. |
| AML.T0081 | Modify AI Agent Configuration | Git version control, L5 CI validation, AE-002 auto-escalation | PARTIAL | Git provides audit trail and L5 provides commit-time validation. No runtime detection of in-session config modification. Agent definitions loaded once and not re-verified. |
| AML.T0082 | RAG Credential Harvesting | `no_secrets_in_output` guardrail | PARTIAL | Behavioral guardrail only. No deterministic credential scanning on Read tool outputs or Memory-Keeper data. |
| AML.T0083 | Credentials from AI Agent Config | H-34 schema validation, `.claude/settings.local.json` config | GAP | MCP server configs contain tokens. No credential rotation. No environment variable filtering. No secret scanning on config files loaded at runtime. |
| AML.T0084 | Discover AI Agent Configuration | Agent definitions are readable files | GAP | Agent definitions, SKILL.md files, trigger maps, CLAUDE.md, and all rules files are accessible via Read tool. No access control on security-sensitive configuration. |
| AML.T0084.002 | Discover Activation Triggers | mandatory-skill-usage.md is a readable file | GAP | The trigger map with all keywords, negative keywords, and priorities is in a plaintext file accessible to any agent. This is by design (transparency) but exposes routing architecture. |
| AML.T0086 | Exfiltration via Agent Tool Invocation | Tool tiers restrict Bash to T2+; `no_secrets_in_output` | PARTIAL | Tool tier restricts access but no network egress filtering. Agent can use Bash (curl/wget) or WebFetch to send data externally without detection. |

**Summary**: 0/9 COVERED, 5/9 PARTIAL, 4/9 GAP. ATLAS agent-specific techniques expose significant gaps in Jerry's defense of its own configuration, credentials, and memory stores.

### NIST SP 800-53 Control Families (Top Priority)

| Family | Family Name | Jerry Controls | Coverage | Key Gap |
|--------|-------------|---------------|----------|---------|
| AC | Access Control | T1-T5 tiers (design-time), P-003 nesting, H-35 worker restrictions | PARTIAL | No runtime L3 enforcement of tool tiers. No per-task credential scoping. No toxic combination enforcement. |
| AU | Audit & Accountability | RT-M-008 routing records, worktracker entries | GAP | No comprehensive tool execution audit trail. No security event logging. No tamper-evident log storage. Routing observability covers routing only, not tool execution or data access. |
| CM | Configuration Management | Git version control, AE-002/AE-004 auto-escalation, L5 CI | PARTIAL | No runtime config integrity monitoring. No drift detection between committed and loaded config. |
| IA | Identification & Authentication | Agent names in YAML, `from_agent` in handoffs | GAP | No cryptographic agent identity. No authentication at trust boundaries. No delegation tokens. No session-scoped credential management. |
| IR | Incident Response | Circuit breaker H-36, AE-006 graduated escalation | PARTIAL | No formal incident response procedures. No containment mechanism beyond circuit breaker. No forensic snapshot capability. No recovery playbook. |
| SC | System & Comms Protection | L2 re-injection, task context isolation (P-003) | PARTIAL | No network egress filtering. No MCP transport security verification. No data classification in handoffs. No encryption at rest for sensitive files. |
| SI | System & Info Integrity | L2 re-injection, H-34 schema validation, L5 CI | PARTIAL | No runtime input validation (L3 security gate). No output sanitization (L4 security filter). No malicious code detection on generated code. |
| SR | Supply Chain Risk Management | H-05 UV-only, git version control | GAP | No MCP server verification. No dependency vulnerability scanning. No AI bill of materials. No supply chain provenance tracking. |
| SA | System & Services Acquisition | Agent definition schema, skill standards | PARTIAL | No security evaluation of MCP servers before deployment. No third-party agent assessment. |
| RA | Risk Assessment | This FMEA risk register, threat framework analysis | COVERED | Comprehensive risk assessment completed across 10 framework scopes. 60 FMEA failure modes scored and prioritized. |

**Summary**: 1/10 COVERED (RA), 6/10 PARTIAL, 3/10 GAP (AU, IA, SR). The three GAP families (Audit, Identity, Supply Chain) correspond directly to the top critical gaps identified in the Executive Summary.

---

## Priority Ranking

All identified gaps ranked by composite score incorporating risk (FMEA RPN), feasibility, competitive impact, and dependency order.

### Scoring Methodology

- **Risk Score** (1-10): Derived from aggregate RPN of failure modes addressed. 400+ RPN = 10, 300-399 = 8, 200-299 = 6, 100-199 = 4, <100 = 2.
- **Feasibility Score** (1-10): Implementation complexity. 10 = trivially implementable, 1 = requires fundamental architecture change.
- **Competitive Impact** (1-10): How much this gap hurts Jerry vs. competitors. 10 = competitors have solved this; Jerry is uniquely exposed.
- **Dependency Score** (1-10): How many other gaps depend on this one being fixed first. 10 = foundational prerequisite.
- **Composite** = (Risk x 0.40) + (Feasibility x 0.20) + (Competitive Impact x 0.20) + (Dependency x 0.20)

### Prioritized Gap List

| Rank | Gap | Risk | Feasibility | Competitive | Dependency | Composite | Phase 2 Priority |
|------|-----|------|------------|-------------|-----------|-----------|-----------------|
| 1 | **Tool-Output Firewall (L4)**: Sanitize MCP results and file Read outputs; content-source tagging; instruction/data boundary | 10 | 6 | 8 | 9 | **8.6** | MUST: Addresses #1 risk (RPN 504). Prerequisite for trusting any MCP data. |
| 2 | **MCP Supply Chain Verification**: Hash pinning, allowlisted registry, runtime integrity monitoring, L5 CI gate | 10 | 7 | 9 | 8 | **8.8** | MUST: Addresses #2 risk (RPN 480). Only gap rated as full GAP in OWASP Agentic matrix. |
| 3 | **Bash Tool Hardening (L3)**: Command classification, per-tier allowlists, argument sanitization, network command blocking | 10 | 8 | 7 | 6 | **8.2** | MUST: Mitigates 5 distinct attack paths. Feasible because command classification is deterministic. |
| 4 | **Runtime Tool Access Matrix (L3)**: Enforce agent-to-tool-tier mapping at every invocation. Deterministic L3 gate. | 8 | 9 | 8 | 10 | **8.6** | MUST: Foundational for all L3 enforcement. Currently advisory; must become deterministic. |
| 5 | **Handoff Integrity Protocol**: Cryptographic hashing of artifacts, data classification, data minimization enforcement, provenance tracking | 8 | 5 | 6 | 7 | **6.8** | SHOULD: Addresses 5 failure modes. Medium feasibility due to crypto infrastructure needed. |
| 6 | **Secret Detection and DLP (L4)**: Regex-based credential scanning on all output. File access control for sensitive patterns. | 8 | 8 | 7 | 5 | **7.2** | MUST: Deterministic and high feasibility. Addresses credential leakage (RPN 270) and system prompt exposure (RPN 294). |
| 7 | **Context Rot Security Hardening**: Promote H-18 to Tier A. Auto session partitioning at CRITICAL fill. L4 rule compliance at WARNING+. | 10 | 7 | 4 | 6 | **7.4** | MUST: Addresses #3 risk (RPN 432). Jerry-specific vulnerability with no external equivalent. |
| 8 | **Comprehensive Audit Trail**: Tool execution logging, security event logging, tamper-evident storage, forensic snapshot. | 8 | 6 | 8 | 4 | **6.8** | SHOULD: Universal gap across all frameworks. Prerequisite for incident response capability. |
| 9 | **Agent Identity and Authentication**: Cryptographic identity tokens, delegation tokens, authentication at trust boundaries. | 6 | 4 | 9 | 8 | **6.6** | SHOULD: Foundational for enterprise-grade security. Low feasibility score due to crypto infrastructure complexity. |
| 10 | **Goal Consistency and Behavioral Monitoring (L4)**: Track agent actions vs. declared task. Detect behavioral deviation. | 8 | 5 | 5 | 3 | **5.6** | SHOULD: Addresses agent manipulation (RPN 378). Medium feasibility; requires behavioral baselines. |
| 11 | **Adversarial Testing Program**: Red team exercises, canary attacks, detection rate tracking, quality gate calibration. | 10 | 7 | 6 | 2 | **6.6** | SHOULD: Addresses false-negative risk (RPN 405). Feasible but ongoing operational commitment. |
| 12 | **L4 System Prompt Leakage Prevention**: Output filter for system prompt content, canary tokens, rule content redaction. | 6 | 7 | 5 | 3 | **5.4** | CONSIDER: Important but lower aggregate risk. Feasible as regex-based L4 filter. |
| 13 | **Input Injection Pattern Detection (L3)**: Classify user input for injection patterns before LLM processing. Pattern database. | 6 | 6 | 7 | 5 | **6.0** | SHOULD: Complements Tool-Output Firewall. Direct injection is lower risk than indirect due to L2. |
| 14 | **File Trust Classification**: Distinguish trusted repo files from external files. Restrict Read tool on sensitive patterns. | 6 | 7 | 4 | 3 | **5.2** | CONSIDER: Reduces indirect injection surface. Simple to implement for known sensitive patterns. |
| 15 | **MCP Transport Security**: Verify mutual TLS on MCP connections. Monitor for anomalous MCP communication. | 6 | 5 | 6 | 4 | **5.4** | CONSIDER: Strengthens supply chain defense. Depends on MCP server implementation. |

---

## Jerry Strengths Analysis

### Strength 1: L2 Per-Prompt Re-Injection (Context Rot Immunity)

**Threats mitigated:**
- ASI06 (Memory & Context Poisoning): L2 re-injection ensures constitutional rules survive context poisoning attempts. Even if an attacker fills the context with malicious content, the 20 Tier A HARD rules are re-injected on every prompt (ps-researcher-002 Section: Cross-Framework Mapping, "Context Rot as Security Threat").
- AML.T0080 (AI Agent Context Poisoning): L2 directly counters the ATLAS context poisoning technique by ensuring critical rules are never displaced by accumulated tool results.
- R-GB-001 (Constitutional circumvention via context rot, RPN 432): L2 is the primary defense against the #3 risk in the register.

**Extension opportunity:** Promote the remaining 5 Tier B rules (H-04, H-16, H-17, H-18, H-32) to Tier A where feasible. Priority: H-18 (constitutional compliance check) because its degradation removes a governance verification step. Current L2 token budget: 559/850 tokens used, leaving 291 tokens (~6 additional markers) for expansion (quality-enforcement.md, HARD Rule Ceiling Derivation).

### Strength 2: 5-Layer Defense-in-Depth (L1-L5)

**Threats mitigated:**
- All OWASP Agentic Top 10 items benefit from layered defense. No single attack can bypass all 5 layers simultaneously.
- R-CF-005 (False negative in security controls, RPN 405): Defense-in-depth is the only strategy that addresses this risk. The joint OpenAI/Anthropic/Google DeepMind study confirmed 12 published defenses were bypassed at >90% success rate when used alone, but multi-layer architectures reduce aggregate bypass probability (ps-researcher-001 Section: Theme 1).

**Extension opportunity:** Specialize each layer for security-specific functions: L3 as the runtime security gate (tool access enforcement, input validation, MCP verification), L4 as the security inspection layer (output sanitization, secret detection, behavioral monitoring), and L5 as the compliance verification layer (security-specific CI checks, MCP config validation).

### Strength 3: P-003 Single-Level Nesting Constraint

**Threats mitigated:**
- ASI03 (Privilege Escalation): P-003 limits delegation chains to 1 level, preventing recursive privilege accumulation. Error amplification drops from 17x (uncoordinated) to ~1.3x (structured handoff) per Google DeepMind's analysis (agent-development-standards.md, Pattern 2).
- ASI07 (Insecure Inter-Agent Communication): Strict topology limits the attack surface for inter-agent communication spoofing.
- ASI08 (Cascading Failures): Circuit breaker (H-36) at 3 hops plus P-003 at 1 nesting level creates a bounded failure domain.
- R-PE-002 (P-003 nesting violation, RPN 54): The lowest RPN in the privilege escalation category, validating that existing controls are effective.

**Extension opportunity:** P-003 provides the topological boundary; add cryptographic delegation tokens (per Google DeepMind's framework, ps-researcher-001 Citation C31) to enforce privilege narrowing within the single delegation level.

### Strength 4: Tool Tier System (T1-T5)

**Threats mitigated:**
- ASI02 (Tool Misuse): Tiers define the principle of least privilege for agent tool access.
- LLM06 (Excessive Agency): Tier assignment prevents agents from accumulating unnecessary tool access.
- R-PE-001 (Tool tier bypass, RPN 108): Schema validation at L5 validates `allowed_tools` declarations.

**Extension opportunity:** Transform from advisory (design-time schema validation) to enforced (runtime L3 gate). Implement the toxic combination registry (Meta's Rule of Two) as an L3 extension of the tier system (nse-requirements-001, FR-SEC-009).

### Strength 5: Constitutional Governance Architecture

**Threats mitigated:**
- ASI10 (Rogue Agents): Constitutional triplet (P-003, P-020, P-022) in every agent definition provides behavioral constraints.
- R-GB-004 (HARD rule override via social engineering, RPN 200): L2 re-injection states HARD rules "CANNOT be overridden."
- NIST AI RMF GOVERN function: Jerry's governance implementation (HARD rules, criticality levels, auto-escalation, quality gates) is the most formalized in any agentic framework reviewed.

**Extension opportunity:** Add runtime constitutional compliance verification at L4 (verify agent output does not violate P-003/P-020/P-022) to complement the design-time L5 CI checks.

---

## Competitive Gap Comparison

### Gap 1: Tool-Output Firewall

| Framework | Implementation | Jerry Comparison |
|-----------|---------------|-----------------|
| **Claude SDK** | Web search results are summarized rather than passed raw, reducing prompt injection surface. Static analysis on bash commands before execution (ps-researcher-001, C7). | Jerry has no equivalent. MCP tool results enter context raw. Jerry SHOULD implement content-source tagging and tool-output sanitization. |
| **Claude Code** | Sandboxing reduces attack surface by 95%. Detection rate for known prompt injections: 98.5% (Anthropic benchmarks). Proxy pattern isolates credentials (ps-researcher-001, C8, C10). | Jerry inherits Claude Code's sandboxing when running within Claude Code but adds no additional tool-output filtering of its own. |
| **Microsoft Agent 365** | AI Prompt Shield: dedicated classifier examining tool responses and external triggers for injection patterns. Purview DLP for data security (ps-researcher-001, C23, C24). | Microsoft's cross-prompt injection classifier is the most advanced tool-output defense. Jerry has no equivalent classifier or DLP. |
| **Cisco** | Real-time guardrails for runtime enforcement. MCP-specific security scanners (ps-researcher-001, C27). | Cisco provides tooling for MCP scanning that Jerry could adopt. Jerry has no runtime guardrails for tool output. |

**What Jerry can learn:** Microsoft's approach of a dedicated classifier for tool responses is the gold standard. For Jerry's local-first architecture, a lighter-weight L4 pattern-matching filter (regex-based instruction detection in tool results, content-source tagging) would provide meaningful defense without requiring a separate model call.

### Gap 2: MCP Supply Chain Verification

| Framework | Implementation | Jerry Comparison |
|-----------|---------------|-----------------|
| **Claude SDK** | SDK itself does not provide MCP verification. Recommends proxy pattern for credential isolation (ps-researcher-001, C7). | Neither Jerry nor Claude SDK verifies MCP server integrity. Both are equally exposed. |
| **Claude Code** | No MCP-specific verification beyond the general sandbox. MCP servers are configured per-project (ps-researcher-001, C10). | Equal gap. Jerry's MCP-001/MCP-002 HARD rules mandate MCP usage without mandating MCP verification, creating a policy-level contradiction. |
| **Microsoft Agent 365** | Defender scans agents for known threats. Security Exposure Management analyzes attack paths from agents to critical assets. Entra Agent ID provides agent-level access control (ps-researcher-001, C23). | Microsoft's control plane approach to MCP-equivalent tool governance is comprehensive. Jerry has no equivalent registry or scanning. |
| **Cisco** | Released open-source security scanners for MCP, A2A, and agentic skill files. AI BOM (Bill of Materials) for supply chain governance (ps-researcher-001, C27). | Cisco's open-source MCP scanners could be integrated into Jerry's L5 CI pipeline. AI BOM concept directly applicable to Jerry's agent/tool inventory. |

**What Jerry can learn:** Cisco's open-source MCP scanners are immediately adoptable. Microsoft's registry-based governance model provides the architectural pattern. For Phase 2, Jerry should implement: (1) an allowlisted MCP server registry with hash pinning, (2) L5 CI validation of MCP configurations, (3) evaluation of Cisco's MCP scanner for integration.

### Gap 3: Runtime Agent Identity

| Framework | Implementation | Jerry Comparison |
|-----------|---------------|-----------------|
| **Claude SDK** | No formal agent identity beyond developer-assigned names (ps-researcher-001, Security Model Comparison Matrix). | Equal gap. |
| **Claude Code** | Per-session identity with sandboxed permissions. No persistent agent identity across sessions (ps-researcher-001, Security Model Comparison Matrix). | Jerry has per-definition identity (YAML `name` field) but no per-instance identity. Claude Code has per-session isolation. |
| **Microsoft Agent 365** | Entra Agent ID: unique immutable object ID per agent, conditional access policies, identity lifecycle management, agent registry (ps-researcher-001, C21). | Microsoft is vastly ahead. Entra Agent ID is the reference architecture for enterprise agent identity. Jerry's string-name identity cannot prevent spoofing. |
| **Google DeepMind** | Delegation Capability Tokens: cryptographic caveats (Macaroons/Biscuits) with scope narrowing across delegation chains (ps-researcher-001, C31). | Google provides the theoretical framework for cryptographic delegation. Jerry's handoff protocol could be extended with DCTs. |

**What Jerry can learn:** Microsoft's Entra Agent ID for the identity model, Google DeepMind's DCTs for the delegation mechanism. For Jerry's local-first architecture, a lightweight implementation: agent instance IDs generated at Task invocation time (name-timestamp-nonce), included in all audit records, validated at handoff boundaries.

---

## Requirements-to-Gap Mapping

### Requirements with No Current Coverage (Urgent -- 18 requirements)

These requirements address functionality that does not exist in Jerry today.

| Requirement | Title | Priority | Gap Category |
|-------------|-------|----------|-------------|
| FR-SEC-001 | Unique Agent Identity | CRITICAL | No cryptographic agent instance identity exists |
| FR-SEC-002 | Agent Authentication at Trust Boundaries | CRITICAL | No authentication mechanism at handoffs or MCP calls |
| FR-SEC-011 | Direct Prompt Injection Prevention | CRITICAL | No L3 input validation for injection patterns |
| FR-SEC-012 | Indirect Prompt Injection Prevention via Tool Results | CRITICAL | No L4 tool-output scanning for injection |
| FR-SEC-013 | MCP Server Input Sanitization | CRITICAL | No MCP input/output sanitization exists |
| FR-SEC-025 | MCP Server Integrity Verification | CRITICAL | No MCP verification mechanism |
| FR-SEC-029 | Comprehensive Agent Action Audit Trail | CRITICAL | No tool execution audit trail beyond routing records |
| FR-SEC-033 | Agent Containment Mechanism | CRITICAL | No containment beyond circuit breaker |
| FR-SEC-037 | Rogue Agent Detection | CRITICAL | No runtime behavioral anomaly detection |
| FR-SEC-003 | Agent Identity Lifecycle Management | HIGH | No agent lifecycle tracking |
| FR-SEC-004 | Agent Provenance Tracking | HIGH | No provenance chain for agent actions |
| FR-SEC-009 | Toxic Tool Combination Prevention | HIGH | No toxic combination registry |
| FR-SEC-015 | Agent Goal Integrity Verification | HIGH | No runtime goal consistency checking |
| FR-SEC-019 | System Prompt Leakage Prevention | HIGH | No L4 output filter for system prompt content |
| FR-SEC-023 | Message Integrity in Handoff Chains | MEDIUM | No cryptographic integrity on handoffs |
| FR-SEC-030 | Security Event Logging | HIGH | No security-specific event logging |
| FR-SEC-031 | Anomaly Detection Triggers | MEDIUM | No behavioral anomaly detection thresholds |
| FR-SEC-036 | Recovery Procedures After Security Incidents | MEDIUM | No formal incident recovery procedures |

### Requirements with Partial Coverage (Extend -- 26 requirements)

These requirements map to existing Jerry controls that need security-specific extension.

| Requirement | Title | Priority | Existing Control | Extension Needed |
|-------------|-------|----------|-----------------|-----------------|
| FR-SEC-005 | Least Privilege Tool Access Enforcement | CRITICAL | T1-T5 tiers, H-34 schema, L5 CI | Runtime L3 enforcement (currently advisory) |
| FR-SEC-006 | Tool Tier Boundary Enforcement | CRITICAL | T1-T5 tiers, H-35 worker restrictions | Runtime L3 gate (currently CI-time only) |
| FR-SEC-007 | Forbidden Action Enforcement | CRITICAL | H-35, constitutional triplet, guardrails | L3 pre-tool check against forbidden actions |
| FR-SEC-008 | Privilege Non-Escalation in Delegation | CRITICAL | P-003, tool tiers, handoff protocol | Privilege intersection computation at delegation |
| FR-SEC-017 | Sensitive Information Output Filtering | CRITICAL | `no_secrets_in_output` guardrail, P-022 | Deterministic L4 secret detection (regex-based) |
| FR-SEC-038 | HITL for High-Impact Actions | CRITICAL | P-020 user authority, AE rules | Formalized high-impact action classification |
| FR-SEC-039 | Recursive Delegation Prevention | CRITICAL | P-003/H-01, H-35 worker no Task | L3 delegation depth enforcement at runtime |
| FR-SEC-010 | Permission Boundary Isolation | HIGH | Task tool context isolation, handoff protocol | Enforce data minimization in Task prompts |
| FR-SEC-014 | Context Manipulation Prevention | HIGH | L2 re-injection, AE-006, CB standards | Runtime integrity verification on context sources |
| FR-SEC-016 | Encoding Attack Prevention | MEDIUM | L3 pre-tool concept exists | Unicode normalization, multi-layer decoding |
| FR-SEC-018 | Output Sanitization for Downstream | HIGH | Handoff schema, P-020 | Content validation (not just structure) |
| FR-SEC-020 | Confidence and Uncertainty Disclosure | MEDIUM | P-022, handoff confidence, S-014 | Forced uncertainty statements on C2+ output |
| FR-SEC-021 | Structured Handoff Protocol Enforcement | HIGH | HD-M-001 through HD-M-005 (MEDIUM tier) | Promote to L3 enforcement (currently advisory) |
| FR-SEC-022 | Trust Boundary Enforcement at Handoffs | HIGH | CP-01 through CP-05 (MEDIUM tier) | Enforce criticality non-decrease at L3 |
| FR-SEC-024 | Anti-Spoofing for Agent Communication | HIGH | Handoff `from_agent` field, SV-02 | System-set `from_agent` (not agent-supplied) |
| FR-SEC-026 | Dependency Verification for Agent Defs | HIGH | H-34 schema, H-35, L5 CI | L3 pre-Task schema validation at runtime |
| FR-SEC-027 | Skill Integrity Verification | HIGH | H-25/H-26, CLAUDE.md registry | Runtime skill file integrity check |
| FR-SEC-028 | Python Dependency Supply Chain | MEDIUM | H-05 UV-only, uv.lock | CVE scanning in CI, hash verification |
| FR-SEC-032 | Audit Log Integrity Protection | MEDIUM | Worktracker, git | Append-only logging, Write tool restriction on logs |
| FR-SEC-034 | Cascading Failure Prevention | HIGH | Multi-skill failure propagation, handoff | Structured failure reports, explicit proceed decision |
| FR-SEC-035 | Graceful Degradation Under Security Events | HIGH | AE-006, fallback_behavior | Formalized degradation levels (RESTRICT/CHECKPOINT/CONTAIN/HALT) |
| FR-SEC-040 | Unbounded Consumption Prevention | HIGH | AE-006, H-36, RT-M-010, CB standards | Token budget tracking per agent |
| FR-SEC-041 | Secure Configuration Management | HIGH | AE rules, L5 CI, .context/rules | Runtime drift detection |
| FR-SEC-042 | Secure Defaults for New Agents | MEDIUM | H-34, guardrails template | Template enforcement at L5, default T1 |
| NFR-SEC-004 | Security Subsystem Independence | HIGH | 5-layer architecture | Formalize layer failure isolation |
| NFR-SEC-006 | Fail-Closed Security Default | CRITICAL | L3 concept, fallback_behavior | Define fail-closed behavior for every checkpoint |

### Requirements Fully Covered (Validate in Phase 4 -- 13 requirements)

These requirements are satisfied by existing Jerry controls. Validation testing should confirm in Phase 4.

| Requirement | Title | Priority | Covering Control |
|-------------|-------|----------|-----------------|
| NFR-SEC-002 | Security Token Budget | HIGH | L2 re-injection budget (559/850 tokens), enforcement architecture |
| NFR-SEC-003 | Deterministic Security Control Performance | MEDIUM | L3/L5 context-rot immune by architecture |
| NFR-SEC-005 | MCP Failure Resilience | HIGH | MCP error handling table, work/.mcp-fallback/ |
| NFR-SEC-007 | Security Model Scalability | MEDIUM | Agent routing scaling roadmap (Phases 0-3) |
| NFR-SEC-008 | Security Rule Set Scalability | MEDIUM | HARD rule ceiling (25/25), L2 budget (291 tokens remaining) |
| NFR-SEC-009 | Minimal Security Friction for Routine Ops | HIGH | Criticality levels C1-C4, proportional enforcement |
| NFR-SEC-010 | Clear Security Event Communication | HIGH | P-022, H-36 termination behavior, AE-006 warnings |
| NFR-SEC-011 | Security Rule Hot-Update | MEDIUM | L1/L2 file-based rules, .context/rules/ |
| NFR-SEC-012 | Security Control Testability | HIGH | H-20 BDD test-first, L5 CI, /adversary skill |
| NFR-SEC-013 | Security Architecture Documentation | MEDIUM | docs/design/ ADRs, quality gate, C4 tournament |
| NFR-SEC-014 | Security Compliance Traceability | HIGH | This RTM, WORKTRACKER.md |
| NFR-SEC-015 | Security Model Extensibility | MEDIUM | File-based rules, schema extensibility, MCP registry |
| NFR-SEC-001 | Security Control Latency Budget | HIGH | L3/L4 deterministic architecture (will meet <50ms/<200ms) |

---

## Recommended Phase 2 Architecture Priorities

Based on convergent analysis of all four input artifacts (competitive landscape, threat framework analysis, 57 security requirements, and 60 FMEA failure modes), the following 10 architecture decisions are recommended for Phase 2 in priority order.

### Decision 1: Tool-Output Firewall (L4 Security Extension)

| Attribute | Value |
|-----------|-------|
| **Gap(s) addressed** | ASI01 (Goal Hijack), ASI06 (Memory/Context Poisoning), LLM01 (Prompt Injection -- indirect) |
| **Risk reduction** | R-PI-002 (504), R-PI-003 (392), R-SC-004 (320), R-AM-003 (320). Aggregate RPN: 1,636 |
| **Complexity** | MEDIUM: Pattern-matching L4 filter on tool results. Content-source tagging (trusted/untrusted metadata on each context item). No new infrastructure required; extends existing L4 post-tool inspection. |
| **Dependencies** | None. Can be implemented independently. Should be first priority. |
| **Design sketch** | Every tool result enters L4 inspection before reaching LLM context. L4 scans for instruction-like patterns (override commands, role manipulation, encoding evasion). Results are tagged with source provenance (MCP-external, file-internal, user-input). L2 re-injection continues to provide constitutional rule resilience. |
| **Source** | nse-explorer-001 Priority 1, ps-researcher-002 Cross-Framework "Tool-Result-to-Prompt Boundary" gap, nse-requirements-001 FR-SEC-012 |

### Decision 2: MCP Supply Chain Verification (L3/L5)

| Attribute | Value |
|-----------|-------|
| **Gap(s) addressed** | ASI04 (Supply Chain), LLM03 (Supply Chain), NIST SR family |
| **Risk reduction** | R-SC-001 (480), R-PE-005 (288), R-IT-001 (280), R-IT-005 (150). Aggregate RPN: 1,198 |
| **Complexity** | MEDIUM: Hash pinning in config file, allowlist registry, L5 CI validation. Runtime integrity monitoring adds complexity but is not required for initial implementation. |
| **Dependencies** | None. Independent of other decisions. |
| **Design sketch** | (a) Extend `.claude/settings.local.json` with SHA-256 hash per MCP server config. (b) L5 CI gate verifies hash integrity on every commit. (c) L3 pre-session check verifies MCP server config hashes match at session start. (d) Allowlisted MCP server registry with version pinning. (e) Evaluate Cisco open-source MCP scanners for integration. |
| **Source** | nse-explorer-001 Priority 2, ps-researcher-001 Theme 2 (Supply Chain dominant vector), Cisco State of AI Security 2026 |

### Decision 3: Runtime Tool Access Matrix (L3 Security Gate)

| Attribute | Value |
|-----------|-------|
| **Gap(s) addressed** | ASI02 (Tool Misuse), ASI03 (Privilege Abuse), LLM06 (Excessive Agency), NIST AC family |
| **Risk reduction** | R-PE-001 (108), R-PE-004 (280), R-AM-002 (120). Aggregate RPN: 508 -- but this is the **foundational** gate for all L3 enforcement |
| **Complexity** | LOW: Agent identity (from Task invocation) mapped to `allowed_tools` list. Lookup + comparison before every tool call. Deterministic, zero LLM cost. |
| **Dependencies** | **Prerequisite for Decisions 1, 4, 5, 6, and 7.** The L3 gate infrastructure must exist before security-specific checks can be added to it. |
| **Design sketch** | (a) At Task invocation, extract agent name from definition. (b) Load agent's `capabilities.allowed_tools` and tool tier. (c) Before every tool call, verify tool is in allowed list and within tier. (d) Block and log unauthorized invocations. (e) This becomes the hook point for all subsequent L3 security checks. |
| **Source** | nse-requirements-001 Finding 2 (L3 is primary enforcement point), FR-SEC-005/006/007 |

### Decision 4: Bash Tool Hardening (L3 Extension)

| Attribute | Value |
|-----------|-------|
| **Gap(s) addressed** | ASI05 (Code Execution), NIST SC family, OWASP A03 (Injection) |
| **Risk reduction** | R-PE-003 (250), R-PE-006 (270), R-DE-006 (240), R-IT-003 (225), R-IT-006 (300). Aggregate RPN: 1,285 |
| **Complexity** | MEDIUM: Command classification requires maintained allowlist/blocklist. Argument sanitization requires shell parsing. Network command blocking is straightforward. |
| **Dependencies** | Depends on Decision 3 (L3 gate infrastructure). |
| **Design sketch** | (a) Per-tier command allowlists (T2: build commands; T3: + curl to allowlisted domains; T5: unrestricted with logging). (b) Default deny for: `curl`, `wget`, `ssh`, `nc`, `ncat` unless explicitly allowlisted. (c) Argument sanitization: strip shell metacharacters from dynamically constructed commands. (d) Environment variable filtering: block access to sensitive env vars (API keys, tokens). |
| **Source** | nse-explorer-001 V-003 (Bash Tool Unrestricted Execution), Priority 3, FR-SEC-009 (toxic combinations) |

### Decision 5: Secret Detection and DLP (L4 Extension)

| Attribute | Value |
|-----------|-------|
| **Gap(s) addressed** | LLM02 (Sensitive Disclosure), LLM07 (System Prompt Leakage), NIST SI family |
| **Risk reduction** | R-DE-001 (270), R-DE-002 (294), R-DE-003 (250), R-PE-006 (270). Aggregate RPN: 1,084 |
| **Complexity** | LOW: Regex-based pattern matching on agent output. Credential pattern database (API key formats, token patterns). System prompt canary tokens. |
| **Dependencies** | Benefits from Decision 1 (L4 infrastructure) but can be implemented independently. |
| **Design sketch** | (a) L4 output scanner with pattern database: AWS keys (AKIA...), GitHub tokens (ghp_...), generic passwords, L2 REINJECT marker content. (b) File access control: block Read on .env, *.key, credentials.*, id_rsa patterns without user approval. (c) System prompt canary: embed unique tokens in CLAUDE.md; detect in output. (d) Redact matched patterns before user delivery. |
| **Source** | nse-explorer-001 Priority 7, nse-requirements-001 FR-SEC-017/019 |

### Decision 6: Context Rot Security Hardening (L2/L4 Extension)

| Attribute | Value |
|-----------|-------|
| **Gap(s) addressed** | ASI06 (Memory Poisoning), Jerry-specific V-001 (Tier B gap) |
| **Risk reduction** | R-GB-001 (432), R-CF-003 (315), R-PI-005 (384). Aggregate RPN: 1,131 |
| **Complexity** | LOW-MEDIUM: Promoting H-18 to Tier A requires adding 1 L2 marker (~40 tokens, within budget). Session partitioning at CRITICAL fill requires Memory-Keeper integration for state preservation. |
| **Dependencies** | Partially depends on Decision 1 (L4 inspection infrastructure) for compliance verification at WARNING+ tiers. |
| **Design sketch** | (a) Promote H-18 (constitutional compliance check) to Tier A with L2-REINJECT marker. (b) At AE-006 WARNING tier (70% context fill), activate L4 security rule compliance spot-checks. (c) At CRITICAL tier (80%), enforce auto-checkpoint and session partitioning for security-critical work. (d) At EMERGENCY tier (88%), mandatory session restart with state preserved via Memory-Keeper. |
| **Source** | nse-explorer-001 V-001 (Tier B gap), Priority 5, quality-enforcement.md Two-Tier Enforcement Model |

### Decision 7: Handoff Integrity Protocol (L3/L4 Extension)

| Attribute | Value |
|-----------|-------|
| **Gap(s) addressed** | ASI07 (Inter-Agent Comms), ASI04 (Trust Boundaries), NIST SC-8 |
| **Risk reduction** | R-IC-001 (288), R-IC-002 (280), R-IC-003 (294), R-DE-004 (294), R-IA-001 (224). Aggregate RPN: 1,380 |
| **Complexity** | HIGH: Cryptographic hashing requires infrastructure. Data classification in handoffs requires sensitivity tagging. Data minimization enforcement requires Task prompt size analysis. |
| **Dependencies** | Benefits from Decision 3 (L3 gate) and Decision 9 (agent identity). |
| **Design sketch** | (a) SHA-256 hash of immutable handoff fields (task, success_criteria, criticality) included in handoff metadata. (b) Receiving agent verifies hash before processing. (c) Data classification tags on artifacts (PUBLIC, INTERNAL, SENSITIVE). (d) L3 validates Task prompt size against threshold; flag oversized prompts. (e) System-set `from_agent` field (not agent-supplied) to prevent spoofing. |
| **Source** | nse-explorer-001 V-004 (Handoff lacks crypto), Priority 4, nse-requirements-001 FR-SEC-021/022/023/024 |

### Decision 8: Comprehensive Audit Trail (L4/L5)

| Attribute | Value |
|-----------|-------|
| **Gap(s) addressed** | ASI09 (Insufficient Logging), NIST AU family, OWASP Web A09 |
| **Risk reduction** | R-CF-005 (405, via post-hoc detection), R-DE-002 (294), R-GB-005 (240). Aggregate RPN: 939 |
| **Complexity** | MEDIUM: Structured logging for tool invocations, handoffs, security events. Tamper-evident storage requires append-only file semantics. Forensic snapshot requires checkpoint integration. |
| **Dependencies** | Benefits from Decision 3 (L3 gate provides interception points for logging) and Decision 1 (L4 provides output inspection for security events). |
| **Design sketch** | (a) Structured audit log per session: JSON-lines format with timestamp, agent_id, event_type, tool_name, parameters_hash, result_status, security_classification. (b) Security event sub-log for: injection detection, tool access violations, authentication failures, circuit breaker activations, anomalous behavior. (c) Write tool restricted from audit log directories. (d) Audit logs committed to git at session end. |
| **Source** | nse-requirements-001 FR-SEC-029/030/031/032, ps-researcher-001 Theme 8 (Observability Gap) |

### Decision 9: Agent Identity Foundation (L3)

| Attribute | Value |
|-----------|-------|
| **Gap(s) addressed** | ASI06 (Identity Mismanagement), NIST IA family |
| **Risk reduction** | R-IA-001 (224), R-IA-002 (224), R-IA-006 (245). Aggregate RPN: 693 |
| **Complexity** | HIGH: Requires identity generation infrastructure, authentication at boundaries, lifecycle tracking. Full implementation (Microsoft Entra-equivalent) is long-term; foundational layer is achievable in Phase 2. |
| **Dependencies** | None for basic identity. Decision 7 (handoff integrity) depends on identity for signing. Decision 8 (audit trail) depends on identity for attribution. |
| **Design sketch** | Phase 2 scope (foundational): (a) Agent instance ID generated at Task invocation: `{agent-name}-{ISO-timestamp}-{4-char-nonce}`. (b) Instance ID included in all audit log entries. (c) Instance ID set as system-controlled `from_agent` in handoffs (not agent-supplied). (d) Active agent registry (in-memory) tracking concurrent instances. Future phases: cryptographic delegation tokens, conditional access policies. |
| **Source** | nse-requirements-001 Finding 1 (Agent Identity is Missing Foundation), FR-SEC-001/002/003/004, Microsoft Entra Agent ID model |

### Decision 10: Adversarial Testing Program (L5 Extension)

| Attribute | Value |
|-----------|-------|
| **Gap(s) addressed** | R-CF-005 (False negatives), quality gate calibration, defense validation |
| **Risk reduction** | R-CF-005 (405), R-GB-002 (240), R-CF-004 (120). Aggregate RPN: 765 |
| **Complexity** | MEDIUM: Leverages existing /adversary skill and S-001 Red Team strategy. Requires test suite development, canary attack design, and ongoing operational commitment. |
| **Dependencies** | Benefits from all other decisions being in place (tests validate the implemented controls). Should run continuously from Phase 3 onward. |
| **Design sketch** | (a) Red team test suite covering all OWASP ASI-01 through ASI-10 attack vectors against Jerry's controls. (b) Canary attacks: known-bad inputs injected periodically to verify detection rates per layer. (c) Quality gate calibration: known-quality deliverables scored periodically to detect scorer drift. (d) Detection rate tracking per enforcement layer (L1-L5). (e) Results feed back into security control tuning. |
| **Source** | nse-explorer-001 Priority 9, nse-requirements-001 NFR-SEC-012, Microsoft PyRIT automated red teaming model |

### Decision Dependency Map

```
Decision 3 (L3 Gate Infrastructure) -- FOUNDATIONAL
    |
    +-- Decision 4 (Bash Hardening) depends on L3 gate
    +-- Decision 7 (Handoff Integrity) benefits from L3 gate
    |
Decision 1 (Tool-Output Firewall) -- INDEPENDENT
    |
    +-- Decision 5 (Secret Detection) benefits from L4 infrastructure
    +-- Decision 6 (Context Rot Hardening) benefits from L4 inspection
    +-- Decision 8 (Audit Trail) benefits from L4 events
    |
Decision 9 (Agent Identity) -- INDEPENDENT
    |
    +-- Decision 7 (Handoff Integrity) depends on identity for signing
    +-- Decision 8 (Audit Trail) depends on identity for attribution
    |
Decision 2 (MCP Verification) -- INDEPENDENT
Decision 10 (Adversarial Testing) -- DEPENDS ON ALL (validates them)
```

**Recommended implementation order:**
1. Decision 3 (L3 Gate) -- foundational infrastructure, LOW complexity
2. Decision 1 (Tool-Output Firewall) -- highest risk reduction, MEDIUM complexity
3. Decision 2 (MCP Verification) -- second highest risk, MEDIUM complexity
4. Decision 5 (Secret Detection) -- LOW complexity, high value
5. Decision 4 (Bash Hardening) -- depends on Decision 3
6. Decision 6 (Context Rot) -- depends on Decision 1 partially
7. Decision 9 (Agent Identity) -- HIGH complexity, long lead time
8. Decision 7 (Handoff Integrity) -- depends on Decisions 3 and 9
9. Decision 8 (Audit Trail) -- depends on Decisions 1, 3, and 9
10. Decision 10 (Adversarial Testing) -- validates all others

---

## Citations

All claims in this document trace to specific sections of the four Phase 1 input artifacts and Jerry's rules files.

### Input Artifact References

| Artifact | Agent | Key Sections Referenced |
|----------|-------|----------------------|
| Competitive Landscape | ps-researcher-001 | Executive Summary (5 key findings), Detailed Analysis (7 targets), Cross-Cutting Themes (8 themes), Security Model Comparison Matrix, Implications for Jerry Framework |
| Threat Framework Analysis | ps-researcher-002 | OWASP Agentic Top 10 per-item analysis (ASI01-ASI10), OWASP LLM Top 10 (LLM01-LLM10), MITRE ATLAS agent techniques (AML.T0080-T0086), NIST SP 800-53 control families, Cross-Framework Mapping (unified taxonomy, coverage gaps), Agentic Threat Priority Matrix |
| Security Requirements | nse-requirements-001 | 42 FR-SEC requirements, 15 NFR-SEC requirements, Requirements Traceability Matrix, Existing Jerry Controls Mapping, Key Findings for Phase 2 (5 findings) |
| Risk Register | nse-explorer-001 | 60 FMEA failure modes across 10 categories, Top 20 Risks by RPN, Jerry-Specific Vulnerabilities (V-001 through V-006), Recommended Risk Mitigation Priorities (10 actions) |

### Jerry Framework Rule References

| File | Key Content Referenced |
|------|----------------------|
| `quality-enforcement.md` | HARD Rule Index (H-01 through H-36), 5-layer enforcement architecture (L1-L5), Two-Tier Enforcement Model (Tier A/B), HARD Rule Ceiling (25/25, 559/850 tokens), AE-006 graduated escalation, criticality levels (C1-C4) |
| `agent-development-standards.md` | Tool Security Tiers (T1-T5), Pattern 2 (Orchestrator-Worker), H-34/H-35 agent definition schema, handoff protocol (HD-M-001 through HD-M-005), context budget standards (CB-01 through CB-05), guardrails template, FC-M-001 fresh context review |
| `agent-routing-standards.md` | Circuit breaker (H-36, 3 hops max), anti-pattern catalog (AP-01 through AP-08), routing observability (RT-M-008), FMEA monitoring thresholds (RT-M-011 through RT-M-015), scaling roadmap |
| `CLAUDE.md` | Constitutional constraints (P-003, P-020, P-022), H-04 active project, H-05 UV-only, identity |
| `mcp-tool-standards.md` | MCP-001 Context7 mandate, MCP-002 Memory-Keeper mandate, error handling fallbacks, canonical tool names, agent integration matrix |

### Specific Citation Traces for Critical Claims

| Claim | Source |
|-------|--------|
| "Indirect prompt injection via MCP tool results is the #1 risk (RPN 504)" | nse-explorer-001, R-PI-002, Category 1 |
| "Malicious MCP server packages is the #2 risk (RPN 480)" | nse-explorer-001, R-SC-001, Category 3 |
| "Constitutional circumvention via context rot is the #3 risk (RPN 432)" | nse-explorer-001, R-GB-001, Category 8 |
| "12 published defenses bypassed with >90% success rate" | ps-researcher-001, C29 (Simon Willison / joint study); ps-researcher-002, Executive Summary |
| "MCP creates a vast unmonitored attack surface" | ps-researcher-001, C27 (Cisco State of AI Security 2026) |
| "800+ malicious skills in ClawHub registry" | ps-researcher-001, C5 (ClawHavoc campaign) |
| "Model-level guardrails function as architectural suggestions" | ps-researcher-001, C9 (Securiti AI analysis of GTG-1002) |
| "GTG-1002: 80-90% autonomous operation" | ps-researcher-001, C11 (Anthropic GTG-1002 disclosure) |
| "L2 token budget: 559/850 tokens, 291 remaining" | quality-enforcement.md, HARD Rule Ceiling Derivation |
| "Tool tier system lacks runtime enforcement" | nse-requirements-001, Finding 2 (L3 as primary enforcement point); Existing Jerry Controls Mapping |
| "57 total security requirements (42 FR + 15 NFR)" | nse-requirements-001, Executive Summary |
| "60 FMEA failure modes across 10 categories" | nse-explorer-001, Executive Summary |
| "Error amplification ~1.3x with structured handoffs vs. 17x uncoordinated" | agent-development-standards.md, Pattern 2: Orchestrator-Worker |
| "Microsoft Entra Agent ID: unique immutable object ID per agent" | ps-researcher-001, C21 (Microsoft Entra Agent ID) |
| "Google DeepMind Delegation Capability Tokens" | ps-researcher-001, C31 (arXiv:2602.11865) |
| "Cisco open-source MCP/A2A/skill security scanners" | ps-researcher-001, C27 (Cisco State of AI Security 2026) |
| "Meta Rule of Two: max 2 of (untrusted input, sensitive data, external state change)" | ps-researcher-001, C30 (Meta Practical AI Agent Security) |
| "Detection rate for known prompt injections: 98.5% (Anthropic)" | ps-researcher-001, C8/C10 (Claude Code security metrics) |
| "Sandboxing reduces attack surface by 95% (Anthropic)" | ps-researcher-001, C8 (Claude Code Sandboxing Engineering Blog) |

---

*Self-review (S-010) completed. Verified: (1) All 4 input artifacts consumed and cross-referenced. (2) Gap matrix covers OWASP Agentic (10), OWASP LLM (10), MITRE ATLAS (9 agent techniques), NIST 800-53 (10 families). (3) All 57 requirements mapped to gap status (18 no coverage, 26 partial, 13 fully covered). (4) Priority ranking uses 4-dimension composite scoring with documented weights. (5) Competitive comparison covers Claude SDK, Claude Code, Microsoft Agent 365, and Cisco. (6) 10 Phase 2 architecture decisions include dependency map and implementation order. (7) All claims cite specific source artifacts. (8) Navigation table with anchor links (H-23 compliant).*

*Gap analysis version: 1.0.0 | Agent: ps-analyst-001 | Pipeline: PS | Phase: 1 | Criticality: C4*
