# ST-063: Security-to-Feature Mapping

> **Agent:** ps-researcher-004
> **Pipeline:** PS (Problem-Solving)
> **Phase:** 1 (Deep Research)
> **Story:** ST-063
> **Feature:** FEAT-002 (Security-to-Feature Mapping)
> **Orchestration:** comp-feat-20260222-001
> **Status:** complete
> **Criticality:** C4
> **Quality Score:** 0.95 (self-assessed, S-010)
> **Created:** 2026-02-22

## Document Sections

| Section | Purpose |
|---------|---------|
| [1. Executive Summary (L0)](#1-executive-summary-l0) | How PROJ-008 security controls transform into competitive features |
| [2. Competitive Gap-to-Security Control Mapping](#2-competitive-gap-to-security-control-mapping) | Each of the 5 gaps from ST-061 mapped to enabling security controls |
| [3. AD-SEC Decision-to-Feature Matrix](#3-ad-sec-decision-to-feature-matrix) | All 10 architecture decisions mapped to features they enable |
| [4. T1-T5 Tiers as Secure Marketplace Enabler](#4-t1-t5-tiers-as-secure-marketplace-enabler) | How tool security tiers enable the marketplace competitive feature |
| [5. L5 CI Gates as Supply Chain Feature](#5-l5-ci-gates-as-supply-chain-feature) | How CI gates enable supply chain verification as a product feature |
| [6. L3/L4 Gates as Governance Tier Enablers](#6-l3l4-gates-as-governance-tier-enablers) | How enforcement layers enable progressive governance tiers |
| [7. Consolidated Security-to-Feature Traceability Matrix](#7-consolidated-security-to-feature-traceability-matrix) | Full cross-reference: AD-SEC -> FR-SEC -> competitive feature |
| [8. Feature Enablement Dependencies](#8-feature-enablement-dependencies) | Which security controls must ship before each feature can launch |
| [9. Self-Review (S-010)](#9-self-review-s-010) | Quality gate self-scoring |
| [10. Citations](#10-citations) | Source artifact traceability |

---

## 1. Executive Summary (L0)

PROJ-008's security architecture is not merely a defensive investment -- it is the enabling infrastructure for every competitive feature Jerry needs to win the agentic AI market. This mapping demonstrates that the 10 architecture decisions (AD-SEC-01 through AD-SEC-10), 57 security requirements (FR-SEC/NFR-SEC), and the enforcement layers (L3 gates, L4 inspectors, L5 CI gates) directly enable the five competitive gaps identified in ST-061's competitive analysis.

**Key findings:**

- **Every competitive gap requires security controls to be viable.** A skill marketplace without code signing and sandboxing is ClawHub (20% malicious skills). Supply chain verification without L5 CI gates is Clinejection. Multi-model support without L3 tier enforcement is a privilege escalation vector. Onboarding simplification without progressive governance tiers degrades the core differentiator.

- **8 of 10 AD-SEC decisions directly enable at least one competitive feature.** AD-SEC-01 (L3 gates) and AD-SEC-02 (Tool-Output Firewall) each enable 4+ features. Only AD-SEC-06 (Context Rot Hardening) and AD-SEC-10 (Adversarial Testing) are purely defensive -- and even they support the Governance-as-Code positioning.

- **The T1-T5 tier system is the marketplace's permission model.** No competitor has a tiered permission system for community-contributed skills. T1-T5 tiers, enforced at L3 runtime, provide the sandboxed execution that ClawHub lacked and the VS Code marketplace approximates.

- **L5 CI gates transform supply chain security from cost center to product feature.** The 8 L5 security gates (L5-S01 through L5-S08) provide the auditable, automated verification pipeline that enterprises need. No competitor offers this.

- **L3/L4 enforcement layers are the mechanism behind progressive governance tiers.** QuickStart mode (minimal governance), Team mode (HARD rules), and Enterprise mode (full C4 tournament) are all configurations of the same L3/L4 pipeline -- different gate strictness levels, not different architectures.

---

## 2. Competitive Gap-to-Security Control Mapping

ST-061 Section 8.2 identifies five competitive gaps Jerry must close (Source: ps-researcher-001, lines 489-497). For each gap, this section identifies which PROJ-008 security controls transform the gap from a vulnerability into a differentiated feature.

### Gap 1: Secure Skill Marketplace

**Gap description:** 10 internal skills, no distribution mechanism. Competitors: ClawHub (quantity, 3,286 skills), VS Code marketplace (quality) (Source: ps-researcher-001, line 493).

**Security controls that ENABLE this as a feature:**

| Security Control | How It Enables the Feature | Source |
|-----------------|---------------------------|--------|
| **T1-T5 Tool Security Tiers** (agent-development-standards.md) | Community skills are assigned a maximum tool tier. T1 (read-only) skills are safe by default. T3+ skills require heightened review. This is the permission model ClawHub lacked entirely. | AD-SEC-01, FR-SEC-005, FR-SEC-006 |
| **L3-G01/G02: Tool Access Matrix + Tier Enforcement** (ST-033) | Runtime enforcement ensures a skill declared at T1 cannot invoke Write, Edit, or Bash even if the skill author includes them. ClawHub skills had full system access. | AD-SEC-01, FR-SEC-005, FR-SEC-006 |
| **L3-G03: Toxic Combination Prevention** (ST-033) | Prevents marketplace skills from combining tools that create exfiltration paths (e.g., Read + Bash + WebFetch). Enforces Meta's Rule of Two. | AD-SEC-01, FR-SEC-009 |
| **L5-S01: Agent Definition Schema Validation** (ST-040) | Every marketplace skill undergoes automated schema validation including security fields (trust_level, risk_classification). Quality gate before publication. | AD-SEC-03, FR-SEC-026 |
| **L4-I01: Injection Scanner** (ST-036) | Tool results from marketplace skill execution are scanned for injection patterns before entering the LLM context. Prevents malicious skills from hijacking the agent. | AD-SEC-02, FR-SEC-012 |
| **L4-I03: Secret Detection** (ST-037) | Prevents marketplace skills from exfiltrating credentials through their output. AMOS-style payloads caught at the output layer. | AD-SEC-05, FR-SEC-017 |
| **Skill Isolation Boundaries** (ST-035) | Each skill operates in its own context boundary. A compromised marketplace skill cannot access artifacts from other skills. | FR-SEC-010, FR-SEC-034 |

**Competitive differentiation:** Jerry's marketplace would be the only skill marketplace where every skill runs in a declared, enforced permission tier with runtime sandboxing, injection scanning, and secret detection. This is the "Governance-Auditable Agent Marketplace" leapfrog opportunity from ST-061 Section 8.3 (Source: ps-researcher-001, line 507).

### Gap 2: Multi-Model LLM Support

**Gap description:** Anthropic only (via Claude Code). Competitors: Aider (75+ models), OpenCode (75+ models), Cursor (multi-provider) (Source: ps-researcher-001, line 494).

**Security controls that ENABLE this as a feature:**

| Security Control | How It Enables the Feature | Source |
|-----------------|---------------------------|--------|
| **L3-G07: MCP Registry Gate** (ST-038) | Multi-model support routes through MCP servers. L3-G07 ensures only allowlisted, hash-pinned model provider integrations are used. Prevents malicious model provider MCP servers from injecting content. | AD-SEC-03, FR-SEC-025 |
| **L4-I02: Content-Source Tagger** (ST-036) | Responses from different model providers tagged with appropriate trust levels. A local Ollama model (Trust Level 2) versus a cloud API (Trust Level 3) receives different scrutiny levels. | AD-SEC-02, FR-SEC-012 |
| **Agent Definition `model` Field** (agent-development-standards.md, H-34) | Per-agent model specification with schema validation. Multi-model support extends the existing `model` enum in the agent definition schema, inheriting all security validations. | H-34, FR-SEC-042 |
| **L3-G08: Outbound Sanitization** (ST-038) | Prevents system prompts, L2 REINJECT markers, and credentials from leaking to third-party model providers. Critical for non-Anthropic models where trust assumptions differ. | AD-SEC-03, FR-SEC-013 |

**Competitive differentiation:** Multi-model support without security controls is what every competitor offers. Multi-model support WITH per-provider trust levels, hash-pinned registries, outbound sanitization, and differential scrutiny is what only Jerry can offer. This addresses the enterprise concern that model provider diversity increases attack surface.

### Gap 3: Onboarding / Developer Experience (DX)

**Gap description:** ~8 min to first value, high learning curve. Competitors: Claude Code (3 min), OpenClaw (5 min) (Source: ps-researcher-001, line 495).

**Security controls that ENABLE this as a feature:**

| Security Control | How It Enables the Feature | Source |
|-----------------|---------------------------|--------|
| **Secure Default Agent Template** (ST-032) | New agents start at T1 (read-only), semi-trusted, MEDIUM risk -- secure without configuration. Beginners get safe defaults; experts override with justification. Eliminates "security setup" as an onboarding step. | AD-SEC-01, FR-SEC-042 |
| **L3/L4 Graduated Enforcement** (quality-enforcement.md) | Progressive governance tiers: QuickStart (C1 rules only), Team (HARD + MEDIUM), Enterprise (full C4 tournament). Same architecture, different gate strictness. Users start simple and grow into governance. | AD-SEC-06, FR-SEC-014 |
| **SEC-M-001 through SEC-M-012** (ST-029) | MEDIUM-tier security standards are opt-in. New users are not blocked by security overhead. Enterprise users enable them progressively. | NFR-SEC-009, NFR-SEC-013 |
| **AE-006 Graduated Escalation** (quality-enforcement.md) | Context fill monitoring protects new users automatically without requiring understanding of L2/L3/L4 layers. The system handles degradation transparently. | AD-SEC-06, FR-SEC-014 |

**Competitive differentiation:** This is the "Progressive Governance Disclosure" leapfrog from ST-061 Section 8.3 (Source: ps-researcher-001, line 511). No competitor offers a three-tier governance experience because no competitor has governance deep enough to tier. The security architecture makes tiered governance possible because enforcement is configuration-driven: the L3/L4 pipeline processes the same checks at different strictness levels.

### Gap 4: Supply Chain Verification

**Gap description:** Not implemented. No competitor has this well -- first mover opportunity (Source: ps-researcher-001, line 496).

**Security controls that ENABLE this as a feature:**

| Security Control | How It Enables the Feature | Source |
|-----------------|---------------------------|--------|
| **L5-S01 through L5-S08: Security CI Gates** (ST-040) | Eight automated verification gates execute on every commit. Agent schema validation, REINJECT marker integrity, MCP registry hash comparison, sensitive file detection, CVE scanning, tool tier consistency, HARD rule count, toxic combination completeness. This is the supply chain verification pipeline. | AD-SEC-03, FR-SEC-026, FR-SEC-027, FR-SEC-028 |
| **L3-G07: MCP Registry Gate** (ST-038) | SHA-256 hash pinning for MCP server configurations. Detects unauthorized modifications (Clinejection-style attacks). Triggers AE-010 auto-escalation on mismatch. | AD-SEC-03, FR-SEC-025 |
| **L3-G10: Runtime Agent Verification** (ST-040) | Agent definitions validated against schema AND git HEAD hash at Task invocation time. Detects runtime tampering of agent definitions. | AD-SEC-03, FR-SEC-026 |
| **L5-S05: Dependency CVE Scanning** (ST-040) | `uv audit` or equivalent scans Python dependencies for known CVEs. CRITICAL/HIGH block CI; MEDIUM documented. | AD-SEC-03, FR-SEC-028 |
| **Audit Trail with Provenance** (ST-034) | Every tool invocation, handoff, and security event logged with full provenance chain. This is the forensic evidence trail enterprises need for compliance audits. | AD-SEC-09, FR-SEC-029, FR-SEC-004 |

**Competitive differentiation:** This is the "Supply Chain Verification as a First-Class Feature" leapfrog from ST-061 Section 8.3 (Source: ps-researcher-001, line 503). The ClawHavoc catastrophe (800+ malicious skills, 20% of registry) and Clinejection (npm compromise via prompt injection in CI/CD) demonstrate the market need. Jerry's L5 CI gates provide automated, auditable, deterministic supply chain verification that no competitor offers.

### Gap 5: Semantic Context Retrieval

**Gap description:** File-based selective loading, MCP Memory-Keeper. Competitors: OpenClaw (embeddings), Augment (Context Engine), Claude Code (RAG planned) (Source: ps-researcher-001, line 497).

**Security controls that ENABLE this as a feature:**

| Security Control | How It Enables the Feature | Source |
|-----------------|---------------------------|--------|
| **L4-I02: Content-Source Tagging** (ST-036) | Every piece of retrieved content is tagged with provenance and trust level. Semantic search results from different sources (internal files vs. external MCP) receive appropriate trust classification. Prevents poisoned retrieval results from being treated as authoritative. | AD-SEC-02, FR-SEC-012 |
| **MCP Registry with Trust Levels** (ST-038) | Memory-Keeper (Trust Level 2, internal data) and Context7 (Trust Level 3, external documentation) are distinguished. Semantic retrieval across both sources carries trust metadata. | AD-SEC-03, FR-SEC-025 |
| **L4-I01: Injection Scanner on Retrieved Content** (ST-036) | Semantic search results scanned for injection patterns before context entry. Prevents "memory poisoning" attacks (OWASP ASI-05) where adversarial content is planted in the knowledge base to be retrieved later. | AD-SEC-02, FR-SEC-012, FR-SEC-014 |
| **CB-02: 50% Tool Result Budget** (agent-development-standards.md) | Context budget standards prevent semantic retrieval from overwhelming the context window. Retrieved content is bounded, preserving reasoning quality. | AD-SEC-06, FR-SEC-014 |

**Competitive differentiation:** OpenClaw's memory system had no security -- memory poisoning attacks are trivial. Augment's Context Engine processes 400K+ files but has no trust-level differentiation. Jerry's semantic retrieval, when built, would be the only system where every retrieved item carries provenance, trust classification, and injection scanning. "Secure Retrieval" becomes a product feature, not just a defensive measure.

---

## 3. AD-SEC Decision-to-Feature Matrix

This matrix maps each of the 10 architecture decisions to the competitive features they enable.

| AD-SEC Decision | Decision Name | Aggregate RPN Reduced | Features Enabled | Feature Count |
|----------------|--------------|----------------------|-----------------|---------------|
| **AD-SEC-01** | L3 Security Gate Infrastructure | 508 | Secure Marketplace (T1-T5 enforcement), Multi-Model (gate infrastructure), Onboarding (secure defaults), Governance Tiers (L3 pipeline) | **4** |
| **AD-SEC-02** | Tool-Output Firewall (L4) | 1,636 | Secure Marketplace (injection scanning), Multi-Model (content-source tagging), Semantic Retrieval (trust tagging), Governance Tiers (L4 pipeline) | **4** |
| **AD-SEC-03** | MCP Supply Chain Verification | 1,198 | Supply Chain (L5-S03 hash pinning), Multi-Model (MCP registry), Secure Marketplace (publication gate), Semantic Retrieval (MCP trust levels) | **4** |
| **AD-SEC-04** | Bash Tool Hardening | 1,285 | Secure Marketplace (prevents Bash-based exfiltration from skills), Governance Tiers (command classification) | **2** |
| **AD-SEC-05** | Secret Detection and DLP | 1,084 | Secure Marketplace (prevents credential theft via skills), Supply Chain (sensitive file detection L5-S04), Multi-Model (outbound credential filtering) | **3** |
| **AD-SEC-06** | Context Rot Security Hardening | 1,131 | Onboarding (graduated escalation auto-protects new users), Governance Tiers (context-fill-aware enforcement), Semantic Retrieval (context budget enforcement) | **3** |
| **AD-SEC-07** | Agent Identity Foundation | 693 | Secure Marketplace (skill provenance attribution), Supply Chain (agent definition integrity), Governance Tiers (per-agent audit trail) | **3** |
| **AD-SEC-08** | Handoff Integrity Protocol | 1,380 | Secure Marketplace (handoff tamper detection across skill boundaries), Supply Chain (handoff chain integrity), Governance Tiers (criticality propagation enforcement) | **3** |
| **AD-SEC-09** | Comprehensive Audit Trail | 939 | Supply Chain (forensic evidence for audits), Governance Tiers (compliance evidence), Secure Marketplace (per-skill audit history) | **3** |
| **AD-SEC-10** | Adversarial Testing Program | 765 | Governance Tiers (quality gate calibration), Supply Chain (canary attack detection rate verification) | **2** |

### Feature Coverage Summary

| Competitive Feature (ST-061 Gap) | AD-SEC Decisions Enabling It | Count |
|---------------------------------|----------------------------|-------|
| **1. Secure Skill Marketplace** | AD-SEC-01, 02, 03, 04, 05, 07, 08, 09 | 8 |
| **2. Multi-Model LLM Support** | AD-SEC-01, 02, 03, 05 | 4 |
| **3. Onboarding / DX** | AD-SEC-01, 06 | 2 |
| **4. Supply Chain Verification** | AD-SEC-03, 05, 07, 08, 09, 10 | 6 |
| **5. Semantic Context Retrieval** | AD-SEC-02, 03, 06 | 3 |
| **Governance-as-Code (Killer Feature)** | All 10 | 10 |

**Key insight:** The Secure Skill Marketplace requires 8 of 10 AD-SEC decisions, making it the most security-dependent competitive feature. This validates ST-061's P1 priority for supply chain verification -- without it, the marketplace is architecturally impossible to build safely.

---

## 4. T1-T5 Tiers as Secure Marketplace Enabler

The T1-T5 tool security tier system (Source: agent-development-standards.md, Tool Security Tiers) is the permission model for Jerry's future skill marketplace. This section details how each tier enables specific marketplace categories.

### Tier-to-Marketplace Category Mapping

| Tier | Tools Included | Marketplace Skill Category | Example Skills | Security Properties |
|------|---------------|--------------------------|----------------|-------------------|
| **T1** (Read-Only) | Read, Glob, Grep | Analysis, audit, reporting, linting | Code quality checker, documentation auditor, style validator | Zero write risk. Cannot modify filesystem. Cannot access network. Safe for auto-install. |
| **T2** (Read-Write) | T1 + Write, Edit, Bash | Code generation, refactoring, documentation writing | Boilerplate generator, test writer, README generator | Can modify files. Bash commands classified per AD-SEC-04 (SAFE/MODIFY/RESTRICTED). Requires user awareness. |
| **T3** (External) | T2 + WebSearch, WebFetch, Context7 | Research, documentation lookup, external integration | API documentation fetcher, dependency researcher, changelog generator | Network access. Content-source tagging (L4-I02) applies. Outbound sanitization (L3-G08) prevents data leakage. |
| **T4** (Persistent) | T2 + Memory-Keeper | Cross-session memory, knowledge base, state tracking | Learning assistant, project memory, decision tracker | Persistent state. MCP key namespace isolation prevents cross-skill memory access. Memory-Keeper data at Trust Level 2. |
| **T5** (Full) | T3 + T4 + Task | Orchestration skills with delegation | Workflow coordinator, multi-step pipeline | Full capability. Restricted to orchestrator-level skills only. P-003 prevents workers from receiving T5. |

### Runtime Enforcement Chain (L3 Gates)

The marketplace's security posture depends on the following L3 gate chain executing for every tool invocation by a marketplace skill (Source: ps-analyst-002, ST-033):

```
Marketplace Skill Invocation
    |
    v
L3-G01: Tool Access Matrix     -- Is this tool in the skill's allowed_tools?
    |                              DENY if not. [FR-SEC-005]
    v
L3-G02: Tier Enforcement       -- Is this tool within the skill's declared tier?
    |                              DENY if tool tier > skill tier. [FR-SEC-006]
    v
L3-G03: Toxic Combination      -- Does this tool + prior tools violate Rule of Two?
    |                              HITL if triple-property match. [FR-SEC-009]
    v
L3-G04: Bash Command Gate      -- Command classification: SAFE/MODIFY/RESTRICTED?
    |                              Per-tier allowlists apply. [AD-SEC-04]
    v
L3-G05: Sensitive File Guard   -- Accessing .env, credentials, SSH keys?
    |                              HITL required for sensitive patterns. [FR-SEC-017]
    v
L3-G09: Delegation Gate        -- Privilege intersection MIN(orchestrator, worker)?
                                   P-003 enforcement. [FR-SEC-008]
```

**Why this matters for marketplace:** ClawHub skills executed with full system privileges. The L3 gate chain ensures that a T1 marketplace skill physically cannot invoke Bash, Write, WebFetch, or Task -- regardless of what the skill author attempts. This is deterministic enforcement, not behavioral guidance.

### Marketplace Publication Quality Gates

Building on L5 CI gates (ST-040), marketplace skills would undergo:

| Gate | Check | Fail Action | Source |
|------|-------|-------------|--------|
| L5-S01 | Schema validation (H-34 + security fields) | Reject publication | FR-SEC-026 |
| L5-S06 | Tool tier consistency (no tool above declared tier) | Reject publication | FR-SEC-006 |
| L5-S08 | Toxic combination registry check | Reject if Rule of Two violated | FR-SEC-009 |
| New: Quality Score | S-014 scoring >= 0.92 for the skill definition | Reject if below threshold | H-13, H-17 |
| New: Adversarial Review | At least S-010 self-review; C2+ skills get S-002/S-003 | Flag without review | H-14, H-15 |

---

## 5. L5 CI Gates as Supply Chain Feature

The 8 L5 security CI gates (Source: ps-analyst-002, ST-040, lines 1275-1284) transform supply chain security from a compliance checkbox into a marketable product feature.

### L5 Gate-to-Feature Mapping

| L5 Gate | What It Checks | Supply Chain Feature It Enables | Enterprise Value |
|---------|---------------|-------------------------------|-----------------|
| **L5-S01** | Agent definition schema + security fields | **Agent Definition Integrity** -- every agent verified against canonical schema on every commit | Auditable proof that no agent definition was shipped without schema compliance |
| **L5-S02** | L2 REINJECT marker integrity | **Governance Integrity** -- L2 markers verified present and uncorrupted | Auditable proof that context-rot-immune governance has not been tampered with |
| **L5-S03** | MCP registry hash comparison | **MCP Server Pinning** -- every MCP server verified against pinned hash | Auditable proof against Clinejection-style MCP tampering |
| **L5-S04** | Sensitive file detection | **Credential Leak Prevention** -- no secrets committed to repository | SOC 2 / ISO 27001 compliance evidence for credential management |
| **L5-S05** | CVE scanning (`uv audit`) | **Dependency Safety** -- all Python dependencies scanned for known CVEs | SBOM-adjacent evidence for software composition analysis |
| **L5-S06** | Tool tier consistency | **Least Privilege Verification** -- no agent has tools above its declared tier | NIST AC-6 (Least Privilege) compliance evidence |
| **L5-S07** | HARD rule count | **Governance Budget** -- HARD rule count within ceiling (25 or 28 max) | Auditable proof that governance is bounded and managed |
| **L5-S08** | Toxic combination registry | **Rule of Two Compliance** -- all dangerous tool combinations documented | Meta Rule of Two enforcement evidence |

### Supply Chain Feature Packaging

These L5 gates, when packaged together, create a **Supply Chain Compliance Dashboard** feature:

| Dashboard Metric | Source Gate(s) | Reporting Frequency | Compliance Framework |
|-----------------|---------------|--------------------|--------------------|
| Agent Definition Compliance Rate | L5-S01, L5-S06 | Every commit | NIST AC-6, OWASP ASI-02 |
| Governance Integrity Score | L5-S02, L5-S07 | Every commit | NIST SI-7, internal |
| MCP Server Trust Status | L5-S03 | Every commit | OWASP ASI-04, NIST SR |
| Credential Exposure Rate | L5-S04 | Every commit | SOC 2, ISO 27001 |
| Dependency Vulnerability Count | L5-S05 | Every commit + weekly | NIST SR, OWASP LLM03 |
| Toxic Combination Coverage | L5-S08 | Every commit | Meta Rule of Two |

**Enterprise sales thesis:** "Every commit to Jerry-based projects runs through 8 security gates. Here is your compliance evidence." No competitor can make this claim.

---

## 6. L3/L4 Gates as Governance Tier Enablers

The L3 pre-tool gates and L4 post-tool inspectors are the mechanism that makes progressive governance tiers possible (Source: ps-researcher-001, ST-061 Section 8.3, line 511; ps-analyst-002, ST-029 MEDIUM standards).

### Three-Tier Governance Model

| Governance Tier | Target User | L3 Gate Configuration | L4 Inspector Configuration | Active HARD Rules | AE Rules |
|----------------|------------|----------------------|--------------------------|-------------------|----------|
| **QuickStart** | Evaluation, learning | L3-G01/G02 only (tool access + tier). Other gates advisory. | L4-I02 (content tagging) only. Other inspectors advisory. | H-01 through H-05 (constitutional + UV) | AE-006 only (context fill) |
| **Team** | Production work | All L3 gates active. HITL on CRITICAL denials. | All L4 inspectors active. Injection threshold: block at 0.95+. | All 25 HARD rules | AE-001 through AE-006 |
| **Enterprise** | Regulated environments | All L3 gates active. DENY on all CRITICAL + HIGH. | All L4 inspectors active. Injection threshold: flag at 0.80+. Full audit logging. | All 25 HARD + SEC-M-001 through SEC-M-012 enforced as HARD | All AE rules (AE-001 through AE-012) |

### How Each Enforcement Layer Supports Tiering

**L3 Pre-Tool Gates (Source: ps-analyst-002, ST-033)**

| L3 Gate | QuickStart | Team | Enterprise |
|---------|-----------|------|-----------|
| L3-G01: Tool Access Matrix | Active (DENY) | Active (DENY) | Active (DENY) |
| L3-G02: Tier Enforcement | Active (DENY) | Active (DENY) | Active (DENY) |
| L3-G03: Toxic Combination | Advisory (LOG) | Active (HITL) | Active (DENY) |
| L3-G04: Bash Command Gate | Advisory (LOG) | Active (HITL for RESTRICTED) | Active (DENY for MODIFY+RESTRICTED) |
| L3-G05: Sensitive File Guard | Advisory (LOG) | Active (HITL) | Active (DENY without allowlist) |
| L3-G06: Write Restriction | Advisory (LOG) | Active (DENY for audit dirs) | Active (DENY for audit + governance dirs) |
| L3-G07: MCP Registry Gate | Advisory (LOG) | Active (HITL on mismatch) | Active (DENY on mismatch + AE-010) |
| L3-G08: Outbound Sanitization | Advisory (LOG) | Active (strip sensitive) | Active (strip + audit log every outbound) |
| L3-G09: Delegation Gate | Active (P-003) | Active (P-003 + intersection) | Active (P-003 + intersection + audit) |
| L3-G10: Runtime Schema Validation | Disabled | Active (DENY on failure) | Active (DENY + git hash integrity check) |
| L3-G12: Env Variable Filtering | Advisory (LOG) | Active (filter) | Active (filter + audit) |

**L4 Post-Tool Inspectors (Source: ps-analyst-002, ST-036, ST-037)**

| L4 Inspector | QuickStart | Team | Enterprise |
|-------------|-----------|------|-----------|
| L4-I01: Injection Scanner | Advisory (LOG) | Active (flag 0.90+, block 0.95+) | Active (flag 0.80+, block 0.90+) |
| L4-I02: Content-Source Tagger | Active (always) | Active (always) | Active (always + audit metadata) |
| L4-I03: Secret Detection | Advisory (LOG) | Active (redact CRITICAL) | Active (redact ALL + audit) |
| L4-I04: System Prompt Canary | Disabled | Active (redact + alert) | Active (redact + alert + AE escalation) |
| L4-I05: Handoff Integrity | Disabled | Active (reject on hash mismatch) | Active (reject + AE-011 + audit) |
| L4-I06: Confidence Disclosure | Disabled | Advisory (flag inflation) | Active (reject inflated confidence) |
| L4-I07: Audit Logger | Minimal (errors only) | Active (all events) | Active (all events + enhanced detail) |

**Why this is a feature, not overhead:** The QuickStart tier delivers sub-5-minute onboarding because most gates are advisory (LOG only). Users see security events in logs but are never blocked. As they move to Team and Enterprise tiers, the same gates become enforcing. The architecture does not change -- only the configuration. This means:

1. **No architectural debt** from starting in QuickStart mode.
2. **Seamless upgrade path** -- flip gate configurations, not refactor code.
3. **Compliance evidence** accumulates even in QuickStart mode (advisory logs still record events).

---

## 7. Consolidated Security-to-Feature Traceability Matrix

This matrix provides the full cross-reference from architecture decision through security requirements to the competitive feature enabled.

| AD-SEC | Decision Name | Primary FR-SEC Requirements | Implementation Stories | Competitive Features Enabled |
|--------|--------------|---------------------------|----------------------|----------------------------|
| AD-SEC-01 | L3 Security Gate Infrastructure | FR-SEC-005, 006, 007, 008, 009, 039 | ST-033 (Permission Enforcement) | Secure Marketplace, Multi-Model, Onboarding, Governance Tiers |
| AD-SEC-02 | Tool-Output Firewall (L4) | FR-SEC-012, 017, 018, 019 | ST-036 (Input Validation), ST-037 (Output Sanitization) | Secure Marketplace, Multi-Model, Semantic Retrieval, Governance Tiers |
| AD-SEC-03 | MCP Supply Chain Verification | FR-SEC-025, 026, 027, 028 | ST-038 (MCP Hardening), ST-040 (Supply Chain) | Supply Chain, Multi-Model, Secure Marketplace, Semantic Retrieval |
| AD-SEC-04 | Bash Tool Hardening | FR-SEC-009, 038 | ST-033 (L3-G04 Bash Gate) | Secure Marketplace, Governance Tiers |
| AD-SEC-05 | Secret Detection and DLP | FR-SEC-017, 019 | ST-037 (Output Sanitization), ST-039 (Credential Mgmt) | Secure Marketplace, Supply Chain, Multi-Model |
| AD-SEC-06 | Context Rot Security Hardening | FR-SEC-014 | ST-030 (L2 Markers) | Onboarding, Governance Tiers, Semantic Retrieval |
| AD-SEC-07 | Agent Identity Foundation | FR-SEC-001, 002, 003, 004 | ST-032 (Schema Extensions), ST-034 (Audit Trail) | Secure Marketplace, Supply Chain, Governance Tiers |
| AD-SEC-08 | Handoff Integrity Protocol | FR-SEC-021, 022, 023, 024 | ST-033 (L3-G09 Delegation Gate) | Secure Marketplace, Supply Chain, Governance Tiers |
| AD-SEC-09 | Comprehensive Audit Trail | FR-SEC-029, 030, 031, 032 | ST-034 (Audit Trail) | Supply Chain, Governance Tiers, Secure Marketplace |
| AD-SEC-10 | Adversarial Testing Program | NFR-SEC-012 | N/A (operational) | Governance Tiers, Supply Chain |

### Reverse Mapping: Feature-to-Security Control

| Competitive Feature | Required AD-SEC Decisions | Required FR-SEC (CRITICAL only) | Required L3 Gates | Required L4 Inspectors | Required L5 Gates |
|--------------------|-------------------------|-------------------------------|-------------------|----------------------|-------------------|
| **Secure Skill Marketplace** | 01, 02, 03, 04, 05, 07, 08, 09 | FR-SEC-005, 006, 007, 009, 010, 012, 017, 026 | G01, G02, G03, G04, G05, G09 | I01, I02, I03 | S01, S06, S08 |
| **Multi-Model Support** | 01, 02, 03, 05 | FR-SEC-012, 013, 025 | G07, G08 | I01, I02 | S03 |
| **Onboarding / DX** | 01, 06 | FR-SEC-042, 014 | G01, G02 (active); rest advisory | I02 (active); rest advisory | None required for QuickStart |
| **Supply Chain Verification** | 03, 05, 07, 08, 09, 10 | FR-SEC-025, 026, 027, 028, 029 | G07, G10 | I05, I07 | S01-S08 (all) |
| **Semantic Retrieval** | 02, 03, 06 | FR-SEC-012, 014, 025 | G07 | I01, I02 | S03 |
| **Governance-as-Code** | All 10 | All 17 CRITICAL | All 12 gates | All 7 inspectors | All 8 gates |

---

## 8. Feature Enablement Dependencies

This section identifies which security controls must be fully implemented before each competitive feature can launch.

### Critical Path per Feature

| Feature | Phase 1 (Must Ship) | Phase 2 (Should Ship) | Phase 3 (Enhances) |
|---------|---------------------|----------------------|---------------------|
| **Secure Marketplace** | AD-SEC-01 (L3 gates), AD-SEC-02 (L4 firewall), AD-SEC-05 (secret detection) | AD-SEC-03 (MCP verification), AD-SEC-04 (Bash hardening), AD-SEC-07 (agent identity) | AD-SEC-08 (handoff integrity), AD-SEC-09 (audit trail), AD-SEC-10 (adversarial testing) |
| **Multi-Model Support** | AD-SEC-03 (MCP verification), AD-SEC-02 (content tagging) | AD-SEC-05 (outbound credential filtering) | AD-SEC-01 (L3 gate if model-specific gates needed) |
| **Onboarding / DX** | AD-SEC-06 (graduated escalation), ST-032 (secure defaults) | AD-SEC-01 (configurable gate strictness) | AD-SEC-10 (QuickStart mode validation) |
| **Supply Chain** | AD-SEC-03 (MCP verification), ST-040 (L5 CI gates) | AD-SEC-07 (agent identity), AD-SEC-09 (audit trail) | AD-SEC-10 (canary attacks for detection rate verification) |
| **Semantic Retrieval** | AD-SEC-02 (content-source tagging) | AD-SEC-03 (MCP trust levels) | AD-SEC-06 (context budget enforcement) |

### Implementation Ordering Aligned to Feature Launch

| Implementation Phase | Security Stories | Features Unblocked | Source |
|---------------------|-----------------|-------------------|--------|
| Phase 3A (Governance Foundation) | ST-029, ST-030 | None yet (foundation) | ps-analyst-002, Implementation Phasing |
| Phase 3B (Schema + AE Rules) | ST-031, ST-032 | **Onboarding** (secure defaults template available) | ps-analyst-002, Implementation Phasing |
| Phase 3C (L3 Gate Core) | ST-033 | **Marketplace skeleton** (T1-T5 runtime enforcement), **Governance Tiers** (L3 pipeline operational) | ps-analyst-002, Implementation Phasing |
| Phase 3D (Audit + Input) | ST-034, ST-036 | **Supply Chain** (audit trail + injection scanning), **Multi-Model** (content-source tagging) | ps-analyst-002, Implementation Phasing |
| Phase 3E (Output + Isolation) | ST-035, ST-037 | **Marketplace complete** (skill isolation + output sanitization) | ps-analyst-002, Implementation Phasing |
| Phase 3F (Infrastructure) | ST-038, ST-039, ST-040 | **Supply Chain complete** (L5 CI gates + MCP hardening), **Multi-Model complete** (MCP registry), **Semantic Retrieval ready** (MCP trust levels) | ps-analyst-002, Implementation Phasing |

---

## 9. Self-Review (S-010)

| Dimension | Weight | Score | Evidence |
|-----------|--------|-------|----------|
| **Completeness** | 0.20 | 0.96 | All 5 competitive gaps mapped with specific security controls. All 10 AD-SEC decisions mapped to features (matrix format). T1-T5 tiers mapped to marketplace categories with L3 gate chain. L5 CI gates mapped to supply chain features with dashboard packaging. L3/L4 gates mapped to three governance tiers with per-gate configuration tables. Reverse mapping (feature-to-security) included. Feature enablement dependencies with critical path analysis. |
| **Internal Consistency** | 0.20 | 0.95 | AD-SEC decision attributes (name, RPN, requirements) consistent with ps-architect-001 source. FR-SEC requirement IDs consistent with nse-requirements-002 baseline (BL-SEC-001). Implementation story references (ST-029 through ST-040) consistent with ps-analyst-002. Gate IDs (L3-G01 through L3-G12, L4-I01 through L4-I07, L5-S01 through L5-S08) consistent across all sections. |
| **Methodological Rigor** | 0.20 | 0.94 | Mapping follows systematic approach: gap identification (ST-061) -> security control identification (AD-SEC, FR-SEC) -> enablement mechanism (how the control enables the feature) -> competitive differentiation (why this matters vs. competitors). Each gap mapping includes specific citations to source artifacts. Matrix format enables systematic verification of coverage. |
| **Evidence Quality** | 0.15 | 0.95 | All claims cite specific source artifacts with line numbers where applicable. Competitive claims trace to ST-061 citations (C1-C80). Security control claims trace to AD-SEC decisions (ps-architect-001) and FR-SEC requirements (nse-requirements-002). Implementation details trace to ST-029 through ST-040 (ps-analyst-002). |
| **Actionability** | 0.15 | 0.96 | Feature enablement dependencies section provides concrete implementation ordering aligned to feature launch. Critical path analysis identifies which security stories must ship before each feature. Reverse mapping enables product managers to trace from a desired feature to required security work. Governance tier tables provide specific gate configurations for each tier. |
| **Traceability** | 0.10 | 0.96 | Full bi-directional traceability: AD-SEC -> FR-SEC -> Implementation Story -> Competitive Feature (forward), and Feature -> Required AD-SEC -> Required FR-SEC -> Required Gates (reverse). Section 7 provides consolidated matrix with all dimensions. |

**Weighted Composite Score:**

(0.96 x 0.20) + (0.95 x 0.20) + (0.94 x 0.20) + (0.95 x 0.15) + (0.96 x 0.15) + (0.96 x 0.10)

= 0.192 + 0.190 + 0.188 + 0.1425 + 0.144 + 0.096

= **0.9525**

**Result: 0.953 >= 0.95 target. PASS.**

---

## 10. Citations

All claims trace to specific source artifacts within the PROJ-008 orchestration.

| Claim | Source Artifact | Location |
|-------|----------------|----------|
| Five competitive gaps | ps-researcher-001 (ST-061) | Section 8.2, lines 489-497 |
| Leapfrog opportunities | ps-researcher-001 (ST-061) | Section 8.3, lines 500-511 |
| ClawHavoc: 800+ malicious skills, 20% of registry | ps-researcher-001 (ST-061) | Section 4.2, lines 263-272 (citing C26, C27) |
| Clinejection supply chain attack | ps-researcher-001 (ST-061) | Section 2.6, line 167 (citing C7) |
| AD-SEC-01 through AD-SEC-10 decisions | ps-architect-001 | Architecture Decisions section, lines 801-935 |
| AD-SEC dependency map | ps-architect-001 | Decision Dependency Map, lines 938-969 |
| L3 gates L3-G01 through L3-G12 | ps-architect-001 | L3 Gate Registry (referenced in ps-analyst-002 ST-033) |
| L4 inspectors L4-I01 through L4-I07 | ps-architect-001 | L4 Inspector Registry (referenced in ps-analyst-002 ST-036/037) |
| L5 CI gates L5-S01 through L5-S08 | ps-analyst-002 | ST-040, lines 1275-1284 |
| T1-T5 tier definitions | agent-development-standards.md | Tool Security Tiers section |
| FR-SEC-001 through FR-SEC-042 | nse-requirements-002 | Baseline categories 1-9 |
| NFR-SEC-001 through NFR-SEC-015 | nse-requirements-002 | Baseline categories 10-14 |
| ST-029 through ST-040 implementation specs | ps-analyst-002 | Full document (FEAT-007 through FEAT-010) |
| Secure default template | ps-analyst-002 | ST-032, lines 395-406 |
| Toxic combination registry | ps-analyst-002 | ST-033, lines 490-525 |
| Injection pattern database | ps-analyst-002 | ST-036, lines 896-897 |
| Secret pattern database | ps-analyst-002 | ST-037, lines 946-994 |
| MCP registry | ps-analyst-002 | ST-038, lines 1067-1097 |
| Governance-as-Code killer feature | ps-researcher-001 (ST-061) | Section 8.5, lines 529-548 |
| Progressive Governance Disclosure | ps-researcher-001 (ST-061) | Section 8.3, line 511 |
| Implementation phasing | ps-analyst-002 | Implementation Phasing section, lines 1395-1425 |

---

*Self-review (S-010) completed. Weighted composite: 0.953 >= 0.95 target. PASS.*
