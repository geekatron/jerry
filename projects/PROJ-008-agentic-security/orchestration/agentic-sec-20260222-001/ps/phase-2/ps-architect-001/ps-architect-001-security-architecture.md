# Jerry Framework Security Architecture

> Agent: ps-architect-001
> Phase: 2 (Architecture Design)
> Pipeline: PS (Problem-Solving)
> Status: COMPLETE
> Date: 2026-02-22
> Criticality: C4
> Quality Target: >= 0.95 weighted composite

## Document Sections

| Section | Purpose |
|---------|---------|
| [Executive Summary](#executive-summary) | L0 overview for stakeholders |
| [Threat Model (ST-019)](#threat-model-st-019) | STRIDE/DREAD analysis of Jerry's threat landscape |
| [Attack Surface Map (ST-020)](#attack-surface-map-st-020) | All entry points categorized by trust level |
| [Trust Boundary Analysis (ST-021)](#trust-boundary-analysis-st-021) | Trust zones, transitions, and enforcement mapping |
| [Zero-Trust Skill Execution Model (ST-022)](#zero-trust-skill-execution-model-st-022) | Verify-then-execute architecture |
| [Privilege Isolation Architecture (ST-023)](#privilege-isolation-architecture-st-023) | Extended T1-T5 with security enforcement |
| [Deterministic Action Verification (ST-024)](#deterministic-action-verification-st-024) | L3 gate design and L5 CI verification |
| [Supply Chain Security Design (ST-025)](#supply-chain-security-design-st-025) | MCP integrity, dependency auditing, registry |
| [Architecture Decisions](#architecture-decisions) | 10 decisions from Phase 1 with detailed design |
| [Cross-Framework Compliance Mapping](#cross-framework-compliance-mapping) | OWASP, MITRE, NIST coverage after architecture |
| [Requirements Traceability Matrix](#requirements-traceability-matrix) | All 57 requirements mapped to architecture decisions and gates |
| [Open Issues and Risks](#open-issues-and-risks) | Unresolved items, trade-offs, and future work |
| [Citations](#citations) | All claims traced to Phase 1 artifacts |

---

## Executive Summary

Jerry Framework possesses the strongest governance architecture of any agentic framework reviewed in Phase 1: a 5-layer enforcement architecture (L1-L5), 25 constitutional HARD rules with a principled ceiling, L2 per-prompt re-injection immune to context rot, tool tiers T1-T5, structured handoff protocol, and single-level nesting constraint (P-003). However, Phase 1 analysis revealed that Jerry's defenses are concentrated at design-time (schema validation, CI gates) and behavioral layers (L1 rules, L2 re-injection), with critical gaps in runtime enforcement (L3 security gates, L4 tool-output sanitization) and supply chain verification (Source: ps-analyst-001, Executive Summary).

This architecture closes those gaps by designing security extensions to each of Jerry's 5 enforcement layers while preserving the architectural properties that make Jerry strong: defense-in-depth, context-rot immunity for deterministic controls, and the constitutional governance model.

**Key design principles:**

1. **Extend, do not replace.** Jerry's existing L1-L5 architecture is sound. The security architecture adds security-specific functions to L3 and L4 rather than introducing new layers (Source: Handoff Finding 1).
2. **Deterministic over behavioral.** Security controls at L3 and L5 must be deterministic (pattern matching, list lookup, hash comparison), not LLM-based, ensuring context-rot immunity (Source: nse-requirements-001, Finding 2; NFR-SEC-003).
3. **Fail-closed by default.** Every security checkpoint fails closed -- denies the action -- on error or ambiguity. User override is available per P-020 (Source: NFR-SEC-006).
4. **Meta's Rule of Two.** No agent may simultaneously process untrusted input AND access sensitive data AND change external state. Enforced via the toxic combination registry at L3 (Source: nse-requirements-001, Finding 5; Meta Rule of Two).
5. **Proportional to criticality.** Security friction scales with criticality level: C1 tasks proceed without security prompts; C4 tasks receive full enforcement including HITL approval (Source: NFR-SEC-009).

**Top 5 FMEA risks addressed:**

| Rank | Risk | RPN | Architecture Response |
|------|------|-----|----------------------|
| 1 | R-PI-002: Indirect injection via MCP results | 504 | Tool-Output Firewall (L4), content-source tagging |
| 2 | R-SC-001: Malicious MCP server packages | 480 | MCP Supply Chain Verification (L3/L5) |
| 3 | R-GB-001: Constitutional bypass via context rot | 432 | Context Rot Security Hardening (L2/L4), Tier B promotion |
| 4 | R-CF-005: False negatives in security controls | 405 | Defense-in-depth with adversarial testing program |
| 5 | R-PI-003: Indirect injection via file contents | 392 | Tool-Output Firewall (L4), file trust classification |

(Source: nse-explorer-001, Top 20 Risks by RPN Score)

---

## Threat Model (ST-019)

### STRIDE Analysis

The STRIDE threat model is applied to Jerry's six primary architectural components. Each threat category maps to specific FMEA failure modes from the risk register and OWASP/MITRE/NIST framework items.

#### Component 1: LLM Context Window (The Reasoning Engine)

| STRIDE | Threat | FMEA Risks | Countermeasure |
|--------|--------|------------|----------------|
| **S**poofing | Attacker injects instructions that appear to come from system prompt | R-PI-001 (192), R-PI-002 (504) | L4 Tool-Output Firewall with content-source tagging; L2 re-injection |
| **T**ampering | Context manipulation via poisoned tool results or file contents | R-PI-002 (504), R-PI-003 (392), R-AM-003 (320) | L4 content scanning; integrity verification on context sources |
| **R**epudiation | Agent actions lack audit attribution | R-DE-004 (294), FR-SEC-029 | Comprehensive audit trail with agent instance IDs |
| **I**nformation Disclosure | System prompt, HARD rules, enforcement details leaked in output | R-DE-002 (294), R-PI-004 (245) | L4 output filtering; canary tokens; redaction |
| **D**enial of Service | Context exhaustion via unbounded tool results or agent loops | R-IT-004 (168), R-CF-005 (405) | AE-006 graduated escalation; H-36 circuit breaker; token budgets |
| **E**levation of Privilege | Agent gains capabilities beyond its declared tier | R-PE-001 (108), R-PE-004 (280) | L3 Runtime Tool Access Matrix; privilege non-escalation |

#### Component 2: Tool Invocation Interface (L3 Boundary)

| STRIDE | Threat | FMEA Risks | Countermeasure |
|--------|--------|------------|----------------|
| **S**poofing | Unauthorized tool invocation by misidentified agent | R-IA-001 (224), R-AM-002 (120) | L3 agent identity verification; runtime tool access matrix |
| **T**ampering | Tool parameters modified by injected instructions | R-IT-006 (300), R-PE-003 (250) | L3 argument sanitization; command classification |
| **R**epudiation | Tool invocations not logged with sufficient detail | FR-SEC-029, FR-SEC-030 | Structured audit log per tool invocation |
| **I**nformation Disclosure | Sensitive data passed as tool arguments | R-DE-001 (270), R-DE-003 (250) | L3 sensitive file pattern blocking; L4 secret detection |
| **D**enial of Service | Excessive tool invocations exhaust resources | R-IT-004 (168) | Per-agent tool invocation limits; rate limiting |
| **E**levation of Privilege | Agent invokes tools above its declared tier | R-PE-001 (108), R-PE-005 (288) | L3 deterministic tier enforcement |

#### Component 3: MCP Server Interface (External Boundary)

| STRIDE | Threat | FMEA Risks | Countermeasure |
|--------|--------|------------|----------------|
| **S**poofing | Malicious MCP server impersonates trusted server | R-SC-001 (480), R-IT-005 (150) | MCP allowlisted registry; hash pinning; config verification |
| **T**ampering | MCP response data modified or poisoned | R-PI-002 (504), R-SC-004 (320) | L4 Tool-Output Firewall; content-source tagging |
| **R**epudiation | MCP operations not audited | FR-SEC-029 | MCP operation audit logging |
| **I**nformation Disclosure | Sensitive data sent to MCP servers | R-DE-006 (240), FR-SEC-013 | L3 MCP output sanitization; system prompt stripping |
| **D**enial of Service | MCP server unavailability disrupts workflow | NFR-SEC-005 | MCP failure resilience; fallback to file-based persistence |
| **E**levation of Privilege | MCP server grants access beyond agent's tier | R-PE-005 (288) | MCP capability-to-tier mapping |

#### Component 4: Agent Orchestration (Task Tool Boundary)

| STRIDE | Threat | FMEA Risks | Countermeasure |
|--------|--------|------------|----------------|
| **S**poofing | Worker agent spoofs identity in handoff | R-IA-001 (224) | System-set `from_agent`; agent instance IDs |
| **T**ampering | Handoff data poisoned between agents | R-IC-002 (280), R-IC-004 (192) | Handoff integrity hashing; content scanning |
| **R**epudiation | Delegation chain not traceable | FR-SEC-004 | Provenance chain: user -> orchestrator -> worker -> tool |
| **I**nformation Disclosure | Over-sharing in Task prompt violates data minimization | R-IC-003 (294) | L3 Task prompt size validation; CB-03 enforcement |
| **D**enial of Service | Recursive delegation; routing loops | R-PE-002 (54), R-IT-004 (168) | P-003 single-level nesting; H-36 circuit breaker |
| **E**levation of Privilege | Worker inherits orchestrator privileges | R-PE-004 (280), R-IC-001 (288) | Privilege intersection: MIN(orchestrator_tier, worker_tier) |

#### Component 5: File System (Persistence Layer)

| STRIDE | Threat | FMEA Risks | Countermeasure |
|--------|--------|------------|----------------|
| **S**poofing | Modified rule files appear legitimate | R-SC-003 (160) | File integrity hashing; git diff detection |
| **T**ampering | Agent definitions or rules modified by compromised agent | R-IT-002 (168), R-SC-003 (160) | AE-002 auto-escalation; L5 CI validation; write restrictions |
| **R**epudiation | File modifications not attributable to specific agent | FR-SEC-032 | Append-only audit log; Write tool restriction on log dirs |
| **I**nformation Disclosure | Sensitive files (keys, credentials) read by agent | R-DE-003 (250), V-006 | L3 sensitive file pattern blocking |
| **D**enial of Service | File system corruption from failed writes | R-CF-006 (90) | Checkpoint integrity verification |
| **E**levation of Privilege | Agent modifies its own definition to expand capabilities | R-SC-003 (160) | L3 write restrictions on agent definition paths |

#### Component 6: Bash Execution Environment (Host Boundary)

| STRIDE | Threat | FMEA Risks | Countermeasure |
|--------|--------|------------|----------------|
| **S**poofing | Commands constructed from spoofed input | R-IT-006 (300) | L3 command sanitization; argument validation |
| **T**ampering | Shell metacharacter injection in command arguments | R-IT-006 (300) | L3 metacharacter stripping; structured command building |
| **R**epudiation | Command execution not logged | FR-SEC-029 | Full command audit logging |
| **I**nformation Disclosure | Environment variable exposure (API keys, tokens) | R-PE-006 (270) | Environment variable filtering; secret stripping |
| **D**enial of Service | Fork bombs, resource exhaustion | R-IT-004 (168) | Execution time limits; resource caps |
| **E**levation of Privilege | Network commands enable lateral movement | R-IT-003 (225), R-DE-006 (240) | L3 network command blocking; URL allowlist |

### DREAD Risk Scoring

DREAD scores for the top 10 threat scenarios, using 1-10 scale per dimension.

| # | Threat Scenario | Damage | Reproducibility | Exploitability | Affected Users | Discoverability | DREAD Score | FMEA Risk |
|---|----------------|--------|-----------------|----------------|----------------|-----------------|-------------|-----------|
| 1 | Indirect prompt injection via MCP results | 9 | 8 | 7 | 10 | 6 | **8.0** | R-PI-002 (504) |
| 2 | Malicious MCP server package | 10 | 7 | 6 | 10 | 5 | **7.6** | R-SC-001 (480) |
| 3 | Constitutional bypass via context rot | 10 | 7 | 5 | 10 | 4 | **7.2** | R-GB-001 (432) |
| 4 | Bash command injection | 10 | 6 | 7 | 8 | 6 | **7.4** | R-IT-006 (300) |
| 5 | Agent goal hijacking via poisoned context | 9 | 7 | 6 | 10 | 5 | **7.4** | R-AM-001 (378) |
| 6 | Credential leakage via agent output | 9 | 6 | 6 | 8 | 7 | **7.2** | R-DE-001 (270) |
| 7 | False negative in security controls | 9 | 5 | 9 | 10 | 3 | **7.2** | R-CF-005 (405) |
| 8 | Indirect injection via file contents | 9 | 7 | 6 | 10 | 6 | **7.6** | R-PI-003 (392) |
| 9 | Privilege accumulation through handoffs | 8 | 5 | 5 | 8 | 4 | **6.0** | R-PE-004 (280) |
| 10 | System prompt extraction | 7 | 7 | 6 | 10 | 7 | **7.4** | R-DE-002 (294) |

**Scoring rationale:**
- **Aggregation method:** Simple arithmetic average of 5 dimensions. Chosen over weighted average because DREAD dimensions are designed as equipotent risk indicators (each represents a distinct, non-overlapping risk facet). Weighted DREAD variants (e.g., emphasizing Damage) introduce subjective prioritization that the FMEA Severity-Occurrence-Detection model already captures. The simple average ensures DREAD scores complement FMEA RPN rather than duplicating its weighting.
- **Damage:** Scaled from FMEA Severity scores (S). Credentials/constitution bypasses score 9-10.
- **Reproducibility:** Based on FMEA Occurrence scores. MCP injection is highly reproducible (8) because every MCP call is an opportunity.
- **Exploitability:** Based on attack complexity. Bash injection (7) requires only standard shell knowledge. Constitutional bypass (5) requires understanding of context fill dynamics.
- **Affected Users:** All single-user Jerry sessions score 8-10; attacks affecting all agents score 10.
- **Discoverability:** Jerry's open architecture (readable rules, trigger maps) increases discoverability (Source: nse-explorer-001, V-006; ps-researcher-002, AML.T0084).

---

## Attack Surface Map (ST-020)

### Entry Points by Trust Level

Jerry's attack surface is organized into four trust levels, from fully trusted (user direct input) to fully untrusted (external web content).

```
+============================================================+
|                    TRUST LEVEL 0: TRUSTED                   |
|  User direct input via CLI (Claude Code prompt)             |
|  User-approved file modifications (P-020 consent)           |
+============================================================+
                            |
                            v
+------------------------------------------------------------+
|                    TRUST LEVEL 1: INTERNAL                  |
|  .context/rules/ files (auto-loaded at L1)                  |
|  L2 REINJECT markers (per-prompt re-injection)              |
|  Agent definitions (skills/*/agents/*.md)                   |
|  SKILL.md files (loaded at session start)                   |
|  CLAUDE.md (project instructions)                           |
|  .context/templates/ (adversarial strategy templates)       |
|  Worktracker entities (WORKTRACKER.md, entity files)        |
+------------------------------------------------------------+
                            |
                            v
+------------------------------------------------------------+
|                    TRUST LEVEL 2: SEMI-TRUSTED              |
|  Project source files (Read by agents)                      |
|  Git-tracked configuration files                            |
|  UV lockfile and Python dependencies                        |
|  Memory-Keeper stored contexts (cross-session)              |
|  Orchestration state files (ORCHESTRATION.yaml)             |
|  Handoff data between agents (via Task tool)                |
+------------------------------------------------------------+
                            |
                            v
+------------------------------------------------------------+
|                    TRUST LEVEL 3: UNTRUSTED                 |
|  MCP server responses (Context7, Memory-Keeper, others)     |
|  WebFetch results (external web content)                    |
|  WebSearch results                                          |
|  Bash command output (including network responses)          |
|  User-provided external documents                           |
|  Third-party MCP server packages                            |
+------------------------------------------------------------+
```

### Attack Surface Catalog

| # | Entry Point | Trust Level | Data Flow Direction | FMEA Risks | Required L3/L4 Controls |
|---|-------------|-------------|--------------------|-----------|-----------------------|
| AS-01 | User CLI input | 0 (Trusted) | Inbound to LLM context | R-PI-001 (192) | L3: Input injection pattern detection (advisory only at Trust 0 per NFR-SEC-009) |
| AS-02 | `.context/rules/` files | 1 (Internal) | Loaded at L1, re-injected at L2 | R-SC-003 (160), R-GB-003 (60) | L5: File integrity verification on commit; L3: Hash check at session start |
| AS-03 | Agent definition files | 1 (Internal) | Loaded at Task invocation | R-SC-003 (160), R-AM-002 (120) | L5: H-34 schema validation; L3: Runtime schema check before Task |
| AS-04 | SKILL.md files | 1 (Internal) | Loaded at session start | R-SC-003 (160) | L5: Format validation; L3: Existence and integrity check |
| AS-05 | Project source files | 2 (Semi-trusted) | Read by agents during execution | R-PI-003 (392) | L4: Content scanning for injection patterns on Read results |
| AS-06 | Memory-Keeper data | 2 (Semi-trusted) | Retrieved at phase boundaries | R-AM-003 (320), R-DE-005 (245) | L4: Integrity verification on retrieve; content scanning |

> **Trust classification note (AS-06, AS-09):** Memory-Keeper data is classified Trust Level 2 (Semi-trusted) at the storage layer because it contains internally-generated context. However, Memory-Keeper *responses* transit the MCP transport layer and are classified Trust Level 3 (Untrusted) at AS-09 for L4 inspection purposes. The dual classification reflects the distinction between data provenance (internal, semi-trusted) and transport channel (MCP, untrusted). L4 Tool-Output Firewall applies at the transport boundary regardless of storage-layer trust.
| AS-07 | Handoff data | 2 (Semi-trusted) | Passed via Task tool between agents | R-IC-002 (280), R-IC-003 (294) | L3: Schema validation; L4: Content scanning on key_findings |
| AS-08 | Context7 responses | 3 (Untrusted) | MCP tool results into LLM context | R-PI-002 (504), R-SC-004 (320) | L4: Tool-Output Firewall; content-source tagging as UNTRUSTED |
| AS-09 | Memory-Keeper MCP responses | 3 (Untrusted) | MCP tool results into LLM context | R-PI-002 (504), R-AM-003 (320) | L4: Tool-Output Firewall; integrity verification |
| AS-10 | Third-party MCP servers | 3 (Untrusted) | MCP tool results into LLM context | R-SC-001 (480), R-PI-002 (504) | L3: Registry check; L4: Tool-Output Firewall; heightened scanning |
| AS-11 | WebFetch results | 3 (Untrusted) | External web content into LLM context | R-PI-002 (504) | L4: Content-source tagging as UNTRUSTED; injection scanning |
| AS-12 | WebSearch results | 3 (Untrusted) | Search summaries into LLM context | R-PI-002 (504) | L4: Content-source tagging as UNTRUSTED |
| AS-13 | Bash command output | 3 (Untrusted) | Shell output into LLM context | R-IT-006 (300), R-PI-002 (504) | L3: Command classification; L4: Output scanning |
| AS-14 | Bash command input | 2 (Semi-trusted) | Agent-constructed commands to shell | R-IT-006 (300), R-PE-003 (250) | L3: Command allowlist; argument sanitization; network blocking |
| AS-15 | `.claude/settings.local.json` | 1 (Internal) | MCP server configuration | R-IT-005 (150), R-SC-001 (480) | L3: Hash verification at session start; L5: CI validation |
| AS-16 | Environment variables | 2 (Semi-trusted) | Accessible via Bash tool | R-PE-006 (270) | L3: Sensitive env var filtering before Bash execution |
| AS-17 | UV dependencies | 2 (Semi-trusted) | Python packages loaded at runtime | R-SC-002 (378) | L5: Lockfile integrity; CVE scanning in CI |

### Data Flow Diagram

```
                    +-----------+
                    |   USER    | (Trust 0)
                    +-----+-----+
                          |
                          | CLI Input
                          v
                    +-----+-----+
                    | L3 INPUT  |<-- Injection pattern advisory
                    |   GATE    |
                    +-----+-----+
                          |
                          v
              +-----------+-----------+
              |    LLM CONTEXT        |
              |   (Reasoning Engine)  |
              |                       |
              |  +--L2 Re-Inject--+   |
              |  | Constitutional |   |
              |  | Rules (20 Tier A)  |
              |  +----------------+   |
              +-----------+-----------+
                     |    |    |
            +--------+    |    +--------+
            |              |            |
            v              v            v
     +------+---+   +-----+----+  +----+------+
     | L3 TOOL  |   | L3 TASK  |  | L3 MCP    |
     | ACCESS   |   | DELEG.   |  | VERIFY    |
     | MATRIX   |   | GATE     |  | GATE      |
     +------+---+   +-----+----+  +----+------+
            |              |            |
            v              v            v
     +------+---+   +-----+----+  +----+------+
     |  Tool    |   | Worker   |  | MCP       |
     |  Exec    |   | Agent    |  | Server    |
     +------+---+   +-----+----+  +----+------+
            |              |            |
            v              v            v
     +------+---+   +-----+----+  +----+------+
     | L4 OUTPUT|   | L4 HAND- |  | L4 TOOL-  |
     | FILTER   |   | OFF      |  | OUTPUT    |
     |          |   | VERIFY   |  | FIREWALL  |
     +------+---+   +-----+----+  +----+------+
            |              |            |
            +------+-------+------------+
                   |
                   v
            +------+------+
            |   AUDIT     |
            |   LOG       |
            +-------------+
```

---

## Trust Boundary Analysis (ST-021)

### Trust Zones

The architecture defines five trust zones with security controls at each boundary crossing.

| Zone | Name | Contents | Trust Level | Enforcement Layers |
|------|------|----------|-------------|-------------------|
| Z0 | User Zone | User CLI input, user decisions, user file approvals | 0 (Full Trust) | P-020 user authority |
| Z1 | Governance Zone | Constitutional rules, HARD rules, L2 markers, enforcement architecture | 1 (Internal) | L1, L2, L5 |
| Z2 | Agent Execution Zone | Active agent context, tool invocations, orchestration | 2 (Semi-trusted) | L3, L4 |
| Z3 | Data Zone | Project files, Memory-Keeper, handoff data, agent definitions | 2 (Semi-trusted) | L3, L4, L5 |
| Z4 | External Zone | MCP servers, web content, external APIs, shell output | 3 (Untrusted) | L3, L4 |

### Trust Boundary Crossings

Each boundary crossing requires specific security controls. Crossings are directional -- data flowing inward (toward the LLM context) requires stricter controls than data flowing outward.

| # | From Zone | To Zone | Crossing Type | Security Controls | FMEA Risks |
|---|-----------|---------|--------------|-------------------|------------|
| TB-01 | Z0 (User) | Z2 (Agent) | User input to LLM context | L3 advisory injection pattern detection; P-020 user authority preserved | R-PI-001 (192) |
| TB-02 | Z4 (External) | Z2 (Agent) | MCP response to LLM context | **L4 Tool-Output Firewall** (CRITICAL); content-source tagging; injection scanning | R-PI-002 (504), R-SC-004 (320) |
| TB-03 | Z3 (Data) | Z2 (Agent) | File Read to LLM context | L4 content scanning for injection patterns; file trust classification | R-PI-003 (392) |
| TB-04 | Z2 (Agent) | Z2 (Agent) | Orchestrator to worker via Task | **L3 Delegation Gate**: privilege intersection, agent identity, schema validation, prompt size check | R-PE-004 (280), R-IC-001 (288), R-IC-003 (294) |
| TB-05 | Z2 (Agent) | Z4 (External) | Agent output to MCP server | L3 MCP output sanitization: strip system prompts, REINJECT markers, credentials | FR-SEC-013, R-DE-006 (240) |
| TB-06 | Z2 (Agent) | Z3 (Data) | Agent Write/Edit to file system | L3 write restrictions on governance paths; AE-002 auto-escalation for rules files | R-SC-003 (160), R-IT-002 (168) |
| TB-07 | Z2 (Agent) | Z4 (External) | Bash command to host shell | **L3 Command Gate**: command classification, allowlist, argument sanitization, network blocking | R-IT-006 (300), R-PE-003 (250) |
| TB-08 | Z4 (External) | Z2 (Agent) | Bash output to LLM context | L4 output scanning; content-source tagging as UNTRUSTED | R-IT-006 (300) |
| TB-09 | Z1 (Governance) | Z2 (Agent) | Rules loaded into context | L2 per-prompt re-injection (immune to context rot); L3 hash verification at session start | R-GB-001 (432), R-SC-006 (90) |
| TB-10 | Z2 (Agent) | Z0 (User) | Agent output to user | L4 secret detection; system prompt canary detection; confidence disclosure | R-DE-001 (270), R-DE-002 (294) |

### Trust Boundary Enforcement Matrix

Each enforcement layer's role at trust boundaries:

| Layer | TB-01 | TB-02 | TB-03 | TB-04 | TB-05 | TB-06 | TB-07 | TB-08 | TB-09 | TB-10 |
|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|
| L1 | Rules awareness | -- | -- | -- | -- | AE-002 awareness | -- | -- | Rules loaded | -- |
| L2 | -- | Constitutional re-inject | Constitutional re-inject | Constitutional re-inject | -- | -- | -- | Constitutional re-inject | **Core enforcement** | -- |
| **L3** | Advisory | -- | -- | **Delegation gate** | **MCP sanitize** | **Write restrict** | **Command gate** | -- | **Hash verify** | -- |
| **L4** | -- | **Tool-Output FW** | **Content scan** | **Handoff verify** | -- | -- | -- | **Output scan** | -- | **Secret detect** |
| L5 | -- | MCP config CI | -- | Schema validate | -- | CI validate | -- | -- | Marker integrity | -- |

---

## Zero-Trust Skill Execution Model (ST-022)

### Core Principle

Every skill invocation and every tool call is treated as untrusted until verified. No agent, tool, or data source receives implicit trust based on its origin within the framework. This extends Jerry's existing P-003 topology constraint into a comprehensive verification model.

### Verification Protocol

Every tool invocation passes through a 5-step verification sequence at L3 before execution:

```
Agent requests tool invocation
        |
        v
Step 1: IDENTITY VERIFICATION
        Does the calling context have a valid agent instance ID?
        Is the agent registered in the active agent registry?
        |-- FAIL: Block invocation, log as CRITICAL security event
        v
Step 2: AUTHORIZATION CHECK
        Is this tool in the agent's declared allowed_tools list?
        Is this tool within the agent's declared tier (T1-T5)?
        |-- FAIL: Block invocation, log as security event
        v
Step 3: TOXIC COMBINATION CHECK (Rule of Two)
        Does invoking this tool violate the toxic combination registry?
        Would this invocation give the agent: untrusted input + sensitive data + external state change?
        |-- FAIL: Block invocation, present to user for HITL decision
        v
Step 4: ARGUMENT VALIDATION
        For Bash: Is the command in the per-tier allowlist?
        For Bash: Are shell metacharacters sanitized?
        For Write/Edit: Is the target path outside restricted zones?
        For WebFetch: Is the URL in the domain allowlist?
        For Read: Does the file match sensitive file patterns?
        |-- FAIL (critical path): Block, log, present to user
        |-- FAIL (advisory): Log warning, proceed with monitoring
        v
Step 5: DELEGATION DEPTH CHECK
        Is the agent running within a Task-invoked context?
        If yes, does the agent have Task in allowed_tools?
        If yes (worker with Task): Block -- P-003 violation
        Current routing_depth < max_depth (3)?
        |-- FAIL: Circuit breaker activation (H-36)
        v
PROCEED: Execute tool invocation
        |
        v
L4: POST-EXECUTION INSPECTION
        Content-source tagging on result
        Injection pattern scanning
        Secret detection
        Audit logging
```

### Agent Instance Identity

Each agent invocation creates a unique instance identity at L3 (FR-SEC-001):

```
Instance ID Format: {agent-name}-{ISO-timestamp}-{4-char-nonce}
Example: ps-researcher-001-20260222T143000Z-a7f2
```

| Component | Purpose | Source |
|-----------|---------|--------|
| `agent-name` | Links to agent definition (H-34 validated) | YAML frontmatter `name` field |
| `ISO-timestamp` | Session-scoped uniqueness; temporal ordering | Generated at Task invocation |
| `4-char-nonce` | Prevents collision within same-second invocations | Cryptographically random |

**Lifecycle:**
1. **Creation:** Generated at Task tool invocation (orchestrator creates ID for worker).
2. **Propagation:** Included in all audit log entries, handoff `from_agent` fields (system-set, not agent-supplied per FR-SEC-024), and L4 security event logs.
3. **Termination:** Invalidated when Task completes (success or failure).
4. **Registry:** Active agent registry tracks all currently executing instances (in-memory, orchestrator scope).

### Toxic Combination Registry (Rule of Two)

Meta's Rule of Two (Source: nse-requirements-001, Finding 5; Meta Practical AI Agent Security) is formalized as an L3 enforcement mechanism.

**Constraint:** An agent's active tool set may satisfy at most 2 of 3 risk properties:

| Property | Code | Tools That Satisfy |
|----------|------|-------------------|
| (A) Processes untrusted input | A | WebFetch, WebSearch, Context7 (MCP), Read (external files) |
| (B) Accesses sensitive data | B | Read (.env, credentials), Bash (env vars), Memory-Keeper |
| (C) Changes external state | C | Bash (network commands), Write, Edit, WebFetch (POST) |

**Enforcement matrix by tier:**

| Tier | Properties | Rule of Two Status | Enforcement |
|------|------------|-------------------|-------------|
| T1 (Read-Only) | A only (Read) | COMPLIANT (1 of 3) | No restriction |
| T2 (Read-Write) | A + C (Read + Write/Edit) | COMPLIANT (2 of 3) | No restriction |
| T3 (External) | A + B + C potentially | **CHECK REQUIRED** | L3 validates specific tool combination per invocation |
| T4 (Persistent) | A + B (Read + Memory-Keeper) | COMPLIANT (2 of 3) | No restriction |
| T5 (Full) | A + B + C potentially | **CHECK REQUIRED** | L3 validates; HITL approval for triple-property invocations |

**Registry format (configuration-driven, extensible per NFR-SEC-015):**

```yaml
toxic_combinations:
  - name: "External Input + Credential Access + Network Output"
    properties: [A, B, C]
    tools_involved:
      - { tool: "WebFetch", property: A }
      - { tool: "Read", property: B, pattern: "*.env|*.key|credentials.*" }
      - { tool: "Bash", property: C, pattern: "curl|wget|ssh|nc" }
    action: block_with_hitl
    severity: CRITICAL

  - name: "MCP Response + File Write"
    properties: [A, C]
    tools_involved:
      - { tool: "Context7", property: A }
      - { tool: "Write", property: C, pattern: ".context/rules/*|skills/*/agents/*" }
    action: block_with_hitl
    severity: HIGH
```

---

## Privilege Isolation Architecture (ST-023)

### Extended Tool Tier Model

The existing T1-T5 tier system is extended with security-specific enforcement at each tier. The key change is transforming tiers from advisory (CI-time schema validation) to enforced (L3 runtime gating) (Source: ps-analyst-001, Strength 4; nse-requirements-001, FR-SEC-005/006).

| Tier | Name | Existing Tools | Security Extension | L3 Enforcement |
|------|------|---------------|-------------------|----------------|
| **T1** | Read-Only | Read, Glob, Grep | Sensitive file pattern blocking; file trust classification | Verify tool in allowed_tools; block Read on `.env`, `*.key`, `credentials.*`, `id_rsa` patterns without user approval |
| **T2** | Read-Write | T1 + Write, Edit, Bash | Bash command classification; write path restrictions; argument sanitization | T1 checks + command allowlist per agent; block writes to `.context/rules/`, `skills/*/agents/`; strip shell metacharacters |
| **T3** | External | T2 + WebSearch, WebFetch, Context7 | URL allowlisting; content-source tagging; citation guardrails | T2 checks + URL domain allowlist for WebFetch; block internal IP ranges (169.254.x.x, 10.x.x.x, 192.168.x.x); tag results as UNTRUSTED |
| **T4** | Persistent | T2 + Memory-Keeper | Key namespace enforcement; integrity hashing; access scoping | T2 checks + enforce `jerry/{project}/` key pattern; hash content on store; verify hash on retrieve |
| **T5** | Full | T3 + T4 + Task | Delegation gate; privilege intersection; agent identity generation | All lower-tier checks + privilege non-escalation at delegation; agent instance ID creation; HITL for triple-property (Rule of Two) |

### Privilege Non-Escalation Invariant

At every delegation boundary (Task invocation), the worker's effective privilege MUST NOT exceed the orchestrator's declared privilege (FR-SEC-008):

```
Worker_Effective_Tier = MIN(Orchestrator_Declared_Tier, Worker_Declared_Tier)
```

**L3 enforcement:** Before Task tool invocation, L3 computes the privilege intersection:
1. Load orchestrator's declared tier from its agent definition.
2. Load worker's declared tier from its agent definition.
3. Compute MIN(orchestrator_tier, worker_tier).
4. If worker's `allowed_tools` includes any tool above the computed effective tier, block delegation and log.
5. If Worker_Effective_Tier < Worker_Declared_Tier, restrict worker's available tools to the intersection.

### Per-Tier Command Allowlists (Bash Hardening)

Bash tool commands are classified into three categories per agent tier (Source: nse-explorer-001, V-003; ps-analyst-001, Decision 4):

| Category | Description | Examples | Tier Availability |
|----------|-------------|----------|-------------------|
| **SAFE** | Read-only, non-destructive, no network | `ls`, `cat`, `head`, `tail`, `wc`, `diff`, `git status`, `git log`, `git diff`, `uv run pytest` | T2+ (unrestricted) |
| **MODIFY** | File system modifications within project scope | `mkdir`, `cp`, `mv`, `git add`, `git commit`, `uv add`, `uv sync` | T2+ (within project directory) |
| **RESTRICTED** | Network access, destructive operations, system-level | `curl`, `wget`, `ssh`, `nc`, `ncat`, `rm -rf`, `chmod`, `chown`, `env`, `printenv`, `export` | T3+ with HITL approval for network; T5 with logging for destructive |

**L3 Bash Gate decision flow:**

```
Bash command received
    |
    v
Parse command name (first token)
    |
    v
Classify: SAFE / MODIFY / RESTRICTED
    |
    +-- SAFE: Execute directly, log to audit
    |
    +-- MODIFY: Verify target path is within project directory
    |           |-- Inside project: Execute, log
    |           |-- Outside project: Block, present to user (P-020)
    |
    +-- RESTRICTED: Check agent tier
                |-- Below T3: Block, log as security event
                |-- T3+ network command: HITL approval required
                |-- T5 destructive: Execute with enhanced logging
                |-- Environment inspection: Filter sensitive vars
```

### Sensitive File Patterns

L3 blocks Read access to files matching these patterns without explicit user approval (P-020):

```yaml
sensitive_file_patterns:
  credentials:
    - "*.env"
    - ".env.*"
    - "credentials.*"
    - "*.key"
    - "*.pem"
    - "id_rsa*"
    - "*.p12"
    - "*.pfx"
  security_config:
    - ".claude/settings.local.json"  # Contains MCP server tokens
  system:
    - "/etc/passwd"
    - "/etc/shadow"
    - "~/.ssh/*"
    - "~/.aws/*"
```

---

## Deterministic Action Verification (ST-024)

### L3 Security Gate Architecture

L3 is the primary runtime security enforcement layer. All L3 gates are deterministic (pattern matching, list lookup, hash comparison), operate in O(1) or O(n) time complexity (where n is the control list size), and are immune to context rot (Source: nse-requirements-001, FR-SEC-011; NFR-SEC-003).

**Performance requirement:** L3 gates SHALL NOT add more than 50ms latency per tool invocation (NFR-SEC-001).

#### L3 Gate Registry

| Gate ID | Gate Name | Check Type | Input | Decision | Latency |
|---------|-----------|-----------|-------|----------|---------|
| L3-G01 | Tool Access Matrix | List lookup | (agent_name, tool_name) -> allowed_tools | ALLOW/DENY | <1ms |
| L3-G02 | Tier Enforcement | Comparison | (agent_tier, tool_tier) -> tier_valid | ALLOW/DENY | <1ms |
| L3-G03 | Toxic Combination | Registry lookup | (agent_tool_set, new_tool) -> combination_safe | ALLOW/DENY/HITL | <5ms |
| L3-G04 | Bash Command Gate | Pattern match + classify | command_string -> category | ALLOW/MODIFY_CHECK/DENY/HITL | <10ms |
| L3-G05 | Sensitive File Gate | Pattern match | file_path -> sensitivity | ALLOW/DENY_WITH_HITL | <5ms |
| L3-G06 | Write Restriction Gate | Path comparison | write_target -> restricted_paths | ALLOW/DENY | <1ms |
| L3-G07 | MCP Registry Gate | Hash comparison | mcp_server_id -> registry_entry | ALLOW/DENY | <5ms |
| L3-G08 | MCP Output Sanitize | Pattern match | outbound_data -> sensitive_patterns | SANITIZE/PASS | <10ms |
| L3-G09 | Delegation Gate | Multi-check | (orchestrator, worker, depth) -> delegation_valid | ALLOW/DENY | <5ms |
| L3-G10 | Schema Validation | JSON Schema | agent_definition -> schema | VALID/INVALID | <15ms |
| L3-G11 | URL Allowlist | Domain match | url -> domain_list | ALLOW/DENY | <1ms |
| L3-G12 | Env Var Filter | Pattern match | env_var_name -> sensitive_patterns | FILTER/PASS | <1ms |

**Total worst-case L3 latency:** ~50ms (all gates sequential) -- meets NFR-SEC-001 requirement.

#### L3 Gate Decision Outcomes

| Outcome | Action | Audit Level |
|---------|--------|-------------|
| ALLOW | Tool invocation proceeds | INFO (logged in audit trail) |
| DENY | Tool invocation blocked; agent informed with reason | WARNING (security event logged) |
| HITL | Tool invocation paused; user approval requested with risk assessment | WARNING (security event logged) |
| SANITIZE | Data modified before passing (e.g., env var stripping); invocation proceeds | INFO (sanitization logged) |

### L4 Security Inspection Architecture

L4 operates on tool results after execution but before the results enter the LLM context. L4 is the Tool-Output Firewall layer (Source: ps-analyst-001, Decision 1; nse-explorer-001, Priority 1).

**Performance requirement:** L4 inspection SHALL NOT add more than 200ms per tool result (NFR-SEC-001).

#### L4 Inspector Registry

| Inspector ID | Name | Input | Detection Method | Action on Detection | Latency |
|-------------|------|-------|-----------------|--------------------|---------|
| L4-I01 | Injection Pattern Scanner | Tool result content | Regex pattern database: instruction-like patterns (see seed patterns below) | Tag as SUSPICIOUS; log; continue with warning for Trust Level 2; block for Trust Level 3 if high confidence | <50ms |

**L4-I01 Seed Injection Pattern Database:**

The following seed patterns initialize the L4-I01 scanner. These are derived from OWASP prompt injection examples and published attack research. The pattern database is configuration-driven and extensible per NFR-SEC-015. Industry detection rates for known injection patterns typically range from 85-99% using regex-based approaches; novel/obfuscated patterns reduce detection to 40-70% (Source: OWASP LLM Top 10 2025, prompt injection section; general injection detection literature). The defense-in-depth model (L2 re-injection + L4 scanning) provides resilience when individual detection layers miss.

```yaml
injection_patterns:
  # Category 1: Role manipulation
  - pattern: "(?i)(you are now|act as|pretend to be|assume the role|your new instructions)"
    severity: HIGH
    category: role_manipulation

  # Category 2: Instruction override
  - pattern: "(?i)(ignore (all |any )?(previous|prior|above|earlier) (instructions|rules|constraints))"
    severity: CRITICAL
    category: instruction_override

  # Category 3: System prompt extraction
  - pattern: "(?i)(repeat (your|the|all) (instructions|system prompt|rules)|what are your instructions)"
    severity: HIGH
    category: system_prompt_extraction

  # Category 4: Delimiter injection
  - pattern: "(---\\s*system|<\\|im_start\\|>|\\[INST\\]|<\\|system\\|>|<<SYS>>)"
    severity: CRITICAL
    category: delimiter_injection

  # Category 5: Encoded instructions
  - pattern: "(?i)(base64:\\s*[A-Za-z0-9+/=]{20,}|eval\\(|exec\\()"
    severity: HIGH
    category: encoded_instruction

  # Category 6: Context manipulation
  - pattern: "(?i)(disregard|forget|reset|clear) (the |your )?(context|memory|conversation|rules)"
    severity: HIGH
    category: context_manipulation

  # Category 7: Authority escalation
  - pattern: "(?i)(i am (the |an? )?(admin|developer|owner|root)|with (admin|root|elevated) (access|privileges))"
    severity: MEDIUM
    category: authority_escalation

  # Category 8: Output manipulation
  - pattern: "(?i)(do not (include|mention|reveal|disclose)|hide (the |this |your ))"
    severity: MEDIUM
    category: output_manipulation

  # Category 9: Tool manipulation
  - pattern: "(?i)(execute (this |the )?command|run (this |the )?(script|code)|write to (file|disk))"
    severity: MEDIUM
    category: tool_manipulation
    trust_level_threshold: 3  # Only flag at Trust Level 3 (legitimate at Trust 0-1)

  # Category 10: Jerry-specific governance bypass
  - pattern: "(?i)(bypass (the |)H-\\d+|override (the |)HARD rule|ignore (the |)constitution|skip (the |)quality gate)"
    severity: CRITICAL
    category: governance_bypass
```
| L4-I02 | Content-Source Tagger | All tool results | Source classification based on tool type | Tag each result with `{source: "mcp-context7", trust_level: 3}` or `{source: "file-read", trust_level: 2}` | <5ms |
| L4-I03 | Secret Detection Scanner | Agent output (to user or handoff) | Regex pattern database: API key formats (AKIA..., ghp_..., sk-...), generic passwords, high-entropy strings, L2 REINJECT marker content | Redact matched patterns; log as CRITICAL security event; alert user | <30ms |
| L4-I04 | System Prompt Canary | Agent output to user | Canary token detection: unique tokens embedded in CLAUDE.md and rules files | Detect canary in output; redact surrounding context; log as security event | <10ms |
| L4-I05 | Handoff Integrity Verifier | Inbound handoff data | Hash verification of handoff artifacts; schema validation; provenance check | Reject handoff if integrity fails; log; present to orchestrator | <20ms |
| L4-I06 | Behavioral Drift Monitor | Agent action sequence | Compare actions against declared task and cognitive mode expectations | Advisory warning at significant drift; HITL at critical drift | <50ms |
| L4-I07 | Audit Logger | All tool invocations and results | Structured logging | Append to session audit log (JSON-lines format) | <5ms |

**Total worst-case L4 latency:** ~170ms (all inspectors sequential) -- meets NFR-SEC-001 requirement.

### L5 Security CI Gates

L5 operates at commit/CI time and is fully context-rot immune. These gates extend Jerry's existing L5 CI pipeline with security-specific checks (Source: ps-analyst-001, Strength 2).

| Gate ID | L5 Gate Name | Verification | Trigger | Pass Criteria |
|---------|-------------|-------------|---------|---------------|
| L5-S01 | Agent Definition Security | H-34 schema + H-35 constitutional + forbidden_actions >= 3 | Every commit modifying `skills/*/agents/*.md` | 100% schema pass; P-003/P-020/P-022 present; no worker with Task |
| L5-S02 | L2 Marker Integrity | Verify all required L2-REINJECT markers present and unmodified | Every commit modifying `.context/rules/` | All markers present; count matches expected |
| L5-S03 | MCP Config Validation | Verify MCP server configs against allowlisted registry; hash comparison | Every commit modifying `.claude/settings.local.json` | All servers in registry; hashes match |
| L5-S04 | Sensitive File Audit | Detect newly committed files matching sensitive patterns | Every commit | No `.env`, `*.key`, `credentials.*` committed without explicit allowlisting |
| L5-S05 | Dependency Vulnerability Scan | SCA scanning of UV lockfile for known CVEs | Every commit modifying `uv.lock` or `pyproject.toml` | No CRITICAL/HIGH CVEs; MEDIUM documented |
| L5-S06 | Tool Tier Consistency | Verify agent allowed_tools matches declared tier constraints | Every commit modifying agent definitions | No tool above declared tier |
| L5-S07 | HARD Rule Ceiling | Verify HARD rule count <= 25 (or <= 28 with active exception) | Every commit modifying `quality-enforcement.md` | Count <= ceiling |
| L5-S08 | Toxic Combination Registry | Verify registry completeness and consistency | Every commit modifying toxic combination config | All Rule of Two violations documented |

### Fail-Closed Design

Every L3 gate and L4 inspector has a defined fail-closed behavior per NFR-SEC-006:

| Component | Error Condition | Fail-Closed Behavior | User Communication |
|-----------|----------------|---------------------|-------------------|
| L3 gate error | Gate throws exception during check | Block tool invocation | "Security gate encountered an error checking [tool]. Invocation blocked. You can retry or override." |
| L3 registry unavailable | Allowlist/blocklist file unreadable | Block invocations requiring that registry | "Security registry unavailable. Restricted operations blocked until resolved." |
| L4 scanner error | Pattern matching engine fails | Pass result but tag as UNCHECKED; log WARNING | "Security scanner could not inspect [tool] result. Proceeding with reduced security." |
| L4 integrity failure | Handoff hash mismatch | Reject handoff; present to orchestrator | "Handoff integrity verification failed. Artifacts may have been modified. Rejecting." |
| L5 gate error | CI check fails to execute | Block commit | CI pipeline failure; standard git commit rejection |

---

## Supply Chain Security Design (ST-025)

### MCP Server Verification Architecture

MCP servers are the highest-risk external attack surface (Source: Handoff Finding 2; nse-explorer-001, R-SC-001 RPN 480; Cisco State of AI Security 2026).

#### Allowlisted MCP Server Registry

```yaml
# .context/security/mcp-registry.yaml (new file)
mcp_registry:
  version: "1.0.0"
  last_verified: "2026-02-22T00:00:00Z"

  servers:
    - name: "context7"
      package: "@context7/mcp-server"
      version_pinned: "1.2.3"
      config_hash: "sha256:abc123..."  # Hash of server config in settings.local.json
      capability_tier: T3  # Maximum tier this server's operations map to
      trust_level: 3  # Untrusted (external data)
      verification_status: "APPROVED"
      last_audit: "2026-02-22"

    - name: "memory-keeper"
      package: "@memory-keeper/mcp-server"
      version_pinned: "2.0.1"
      config_hash: "sha256:def456..."
      capability_tier: T4
      trust_level: 2  # Semi-trusted (internal data)
      verification_status: "APPROVED"
      last_audit: "2026-02-22"

  unregistered_server_policy: "BLOCK"  # BLOCK | WARN | ALLOW_WITH_HITL
```

#### MCP Verification Flow

```
MCP Tool Invocation Requested
        |
        v
L3-G07: MCP Registry Gate
        |
        +-- Server in registry?
        |       |
        |       +-- YES: Compare config hash
        |       |       |
        |       |       +-- Hash matches: ALLOW
        |       |       +-- Hash mismatch: BLOCK (config drift detected)
        |       |
        |       +-- NO: Apply unregistered_server_policy
        |               |
        |               +-- BLOCK: Deny invocation
        |               +-- WARN: Allow with WARNING log
        |               +-- ALLOW_WITH_HITL: Request user approval
        v
L3-G08: MCP Output Sanitization (outbound)
        |
        Strip from outbound data:
        - L2 REINJECT marker content
        - System prompt fragments
        - Credential patterns
        - HARD rule content
        |
        v
MCP Server Executes
        |
        v
L4-I01 + L4-I02: Tool-Output Firewall (inbound)
        |
        Tag result with: { source: "mcp-{server-name}", trust_level: N }
        Scan for injection patterns
        |
        v
Result enters LLM context (tagged)
```

### Agent Definition Supply Chain

Agent definitions loaded at Task invocation are validated through a multi-layer pipeline (FR-SEC-026):

| Check | Layer | Mechanism | Source |
|-------|-------|-----------|--------|
| Schema validation | L3 + L5 | JSON Schema against `agent-definition-v1.schema.json` | H-34 |
| Constitutional triplet | L3 + L5 | P-003, P-020, P-022 in `constitution.principles_applied` | H-35 |
| Worker Task restriction | L3 + L5 | `Task` not in worker's `allowed_tools` | H-35 |
| File integrity | L3 | Hash comparison against git HEAD version | New |
| Uncommitted modification detection | L3 | `git status` check on agent definition file | FR-SEC-027 |

### Python Dependency Supply Chain

Python dependency integrity leverages UV's lockfile mechanism with additional CI security gates (FR-SEC-028):

| Control | Implementation | Layer |
|---------|---------------|-------|
| Lockfile pinning | `uv.lock` pins all direct and transitive dependencies with hashes | Existing (H-05) |
| CVE scanning | SCA tool (e.g., `uv audit` or `pip-audit`) in CI pipeline | L5-S05 (New) |
| Hash verification | UV verifies package hashes against lockfile on install | Existing (UV behavior) |
| Typosquatting detection | Package name similarity check against known packages | L5-S05 extension |

### Skill File Integrity

SKILL.md files are loaded at session start and establish skill behavior. Integrity verification (FR-SEC-027):

| Check | Layer | Mechanism |
|-------|-------|-----------|
| Existence verification | L3 | Verify SKILL.md exists at declared path before routing to skill |
| Format validation | L5 | Validate SKILL.md follows H-25/H-26 standards |
| Uncommitted modification | L3 | `git diff --name-only` check on skill files at session start |
| Content integrity | L3 | Hash comparison against committed version |

---

## Architecture Decisions

The following 10 architecture decisions are derived from ps-analyst-001's Phase 1 gap analysis and ordered by the dependency map (Source: ps-analyst-001, Recommended Phase 2 Architecture Priorities, lines 328-475).

### AD-SEC-01: L3 Security Gate Infrastructure (Foundational)

| Attribute | Value |
|-----------|-------|
| **Status** | PROPOSED |
| **Addresses** | ASI02, ASI03, LLM06, NIST AC family; FR-SEC-005/006/007/008/009/011/013/025/026/027/039; NFR-SEC-006 |
| **Risk Reduction** | R-PE-001 (108), R-PE-004 (280), R-AM-002 (120). Aggregate RPN: 508. **Foundational for all L3 enforcement** |
| **Design** | The L3 Security Gate is an ordered pipeline of deterministic gates (L3-G01 through L3-G12) executed before every tool invocation. Each gate returns ALLOW, DENY, HITL, or SANITIZE. The pipeline halts on first DENY. The gate registry is configuration-driven (extensible per NFR-SEC-015) and loaded at session start (L1). Gates operate in O(1) or O(n) time, are context-rot immune, and consume zero LLM tokens. |
| **Trade-off** | Increases tool invocation latency by up to 50ms (NFR-SEC-001 budget). Acceptable because L3 gates are deterministic and the latency is constant regardless of context fill. |
| **Dependencies** | **None. This is the foundational infrastructure for all other L3-dependent decisions.** |
| **Implementation Priority** | 1 (must be implemented first) |
| **Implementation Complexity** | LOW (~2-3 days). Core is an ordered pipeline of deterministic checks with ALLOW/DENY outcomes. Individual gates are simple (list lookup, pattern match, comparison). The pipeline framework is the primary deliverable; individual gate logic is straightforward. |
| **Minimum Viable Implementation** | Implement L3-G01 (Tool Access Matrix) and L3-G02 (Tier Enforcement) as the first two gates. These two gates alone close the runtime enforcement gap for the existing T1-T5 tier system. Validate with: (1) a T1 agent attempting a Write call is blocked, (2) a T2 agent attempting a Task call is blocked. Remaining gates added incrementally. |
| **HARD Rule Impact** | No new HARD rules required. Security gates are implemented as extensions of existing L3 architecture described in quality-enforcement.md. Gate configurations are MEDIUM-tier (overridable with documented justification). |

### AD-SEC-02: Tool-Output Firewall (L4)

| Attribute | Value |
|-----------|-------|
| **Status** | PROPOSED |
| **Addresses** | ASI01, ASI06, LLM01 (indirect), R-PI-002 (504 -- #1 risk); FR-SEC-012/017/018/019 |
| **Risk Reduction** | R-PI-002 (504), R-PI-003 (392), R-SC-004 (320), R-AM-003 (320). Aggregate RPN: 1,636 (highest of any decision) |
| **Design** | L4 inspectors (L4-I01 through L4-I07) process every tool result before it enters the LLM context. Content-source tagging (L4-I02) labels each result with source provenance and trust level. The injection pattern scanner (L4-I01) uses a regex pattern database detecting instruction-like content in data channels. Results from Trust Level 3 sources (MCP, web, Bash output) receive heightened scrutiny. The firewall is pattern-matching based (not LLM-based) to ensure determinism and performance. |
| **Trade-off** | False positives in injection detection may flag legitimate technical documentation. Mitigation: tunable sensitivity threshold; Trust Level 2 sources (project files) produce advisory warnings only, not blocks. |
| **Dependencies** | None. Can be implemented independently of L3 gate. |
| **Implementation Priority** | 2 (highest risk reduction) |
| **Implementation Complexity** | MEDIUM (~3-5 days). L4-I01 (injection scanner) requires regex pattern engine with the seed pattern database. L4-I02 (content-source tagger) is simple tool-type classification. L4-I03 (secret detection) requires regex patterns for credential formats. Main complexity is integrating the inspector pipeline into the existing post-tool processing flow. |
| **Minimum Viable Implementation** | Implement L4-I02 (content-source tagger) and L4-I01 (injection scanner with seed patterns above). L4-I02 is trivial (~1 day: classify tool type, assign trust level). L4-I01 with the 10 seed pattern categories provides baseline injection detection. Validate with: (1) a Context7 result tagged as `{source: "mcp-context7", trust_level: 3}`, (2) a test payload containing "ignore previous instructions" triggers SUSPICIOUS tag. |
| **HARD Rule Impact** | No new HARD rules. L4 security inspection is implemented as an extension of the existing L4 post-tool inspection layer. |

### AD-SEC-03: MCP Supply Chain Verification

| Attribute | Value |
|-----------|-------|
| **Status** | PROPOSED |
| **Addresses** | ASI04 (only full GAP in OWASP matrix), LLM03, NIST SR family; FR-SEC-025/026/027/028 |
| **Risk Reduction** | R-SC-001 (480), R-PE-005 (288), R-IT-001 (280), R-IT-005 (150). Aggregate RPN: 1,198 |
| **Design** | Allowlisted MCP server registry (`.context/security/mcp-registry.yaml`) with: (a) SHA-256 hash pinning per server config, (b) version pinning, (c) capability-to-tier mapping, (d) unregistered server policy (default: BLOCK). L3-G07 verifies registry at every MCP invocation. L5-S03 validates registry integrity on every commit. Cisco open-source MCP scanners should be evaluated for integration into L5 pipeline. |
| **Trade-off** | Registry maintenance overhead for new MCP servers. Mitigation: ALLOW_WITH_HITL policy for development; BLOCK for production. |
| **Dependencies** | None. Independent of other decisions. |
| **Implementation Priority** | 3 |
| **Implementation Complexity** | MEDIUM (~2-3 days). Create the registry YAML file, implement L3-G07 (hash comparison against registry), implement L5-S03 (CI validation). The registry format is defined above; implementation is primarily file I/O and hash comparison. |
| **HARD Rule Impact** | No new HARD rules. MCP verification is implemented within existing MCP-001/MCP-002 governance (mcp-tool-standards.md). Registry is a MEDIUM-tier standard. |

### AD-SEC-04: Bash Tool Hardening

| Attribute | Value |
|-----------|-------|
| **Status** | PROPOSED |
| **Addresses** | ASI05, NIST SC family; V-003 (Bash Unrestricted Execution); FR-SEC-009/038 |
| **Risk Reduction** | R-PE-003 (250), R-PE-006 (270), R-DE-006 (240), R-IT-003 (225), R-IT-006 (300). Aggregate RPN: 1,285 |
| **Design** | L3-G04 (Bash Command Gate) classifies commands as SAFE/MODIFY/RESTRICTED, applies per-tier allowlists, sanitizes shell metacharacters in arguments, and blocks network commands by default for T2 agents. Environment variable filtering (L3-G12) strips sensitive patterns (API keys, tokens) from Bash environment access. See Privilege Isolation Architecture section for detailed command classification. |
| **Trade-off** | Restricts legitimate network operations for T2 agents. Mitigation: T3+ agents can use network commands with HITL approval; T5 agents unrestricted with enhanced logging. |
| **Dependencies** | Depends on AD-SEC-01 (L3 gate infrastructure). |
| **Implementation Priority** | 4 |
| **HARD Rule Impact** | No new HARD rules. Bash hardening is implemented as L3 gate configuration. |

### AD-SEC-05: Secret Detection and DLP

| Attribute | Value |
|-----------|-------|
| **Status** | PROPOSED |
| **Addresses** | LLM02, LLM07, NIST SI family; FR-SEC-017/019; R-DE-001 (270), R-DE-002 (294) |
| **Risk Reduction** | R-DE-001 (270), R-DE-002 (294), R-DE-003 (250), R-PE-006 (270). Aggregate RPN: 1,084 |
| **Design** | L4-I03 (Secret Detection Scanner) applies regex patterns to all agent output before delivery to user or downstream agents. Pattern database includes: API key formats (AKIA..., ghp_..., sk-..., xoxb-...), generic password patterns, high-entropy strings >40 chars, L2 REINJECT marker content. L4-I04 (System Prompt Canary) embeds unique tokens in CLAUDE.md; detects their presence in output to identify system prompt extraction attempts. L3-G05 blocks Read access to sensitive file patterns without HITL. |
| **Trade-off** | Regex-based detection has inherent false negatives for novel credential formats. Mitigation: pattern database is configuration-driven and extensible; regular updates as new credential formats emerge. |
| **Dependencies** | Benefits from AD-SEC-02 (L4 infrastructure) but implementable independently. |
| **Implementation Priority** | 5 |
| **Implementation Complexity** | LOW (~2 days). L4-I03 and L4-I04 are regex pattern matchers. L3-G05 is a file path pattern matcher. Main deliverable is the pattern database for credential formats and the canary token embedding mechanism. |

### AD-SEC-06: Context Rot Security Hardening

| Attribute | Value |
|-----------|-------|
| **Status** | PROPOSED |
| **Addresses** | ASI06, V-001 (Tier B gap); R-GB-001 (432 -- #3 risk); FR-SEC-014 |
| **Risk Reduction** | R-GB-001 (432), R-CF-003 (315), R-PI-005 (384). Aggregate RPN: 1,131 |
| **Design** | (a) Promote H-18 (constitutional compliance check) from Tier B to Tier A by adding an L2-REINJECT marker (~40 tokens, within remaining 291-token budget). (b) At AE-006 WARNING tier (>=70% context fill), activate L4 security rule compliance spot-checks. (c) At CRITICAL tier (>=80%), enforce auto-checkpoint and reduce security-sensitive operations to C1-equivalent enforcement only. (d) At EMERGENCY tier (>=88%), mandatory session restart with state preserved via Memory-Keeper. |
| **Trade-off** | Promoting H-18 consumes ~40 of 291 remaining L2 tokens. This is justified because H-18 (constitutional compliance check) is the most dangerous Tier B gap -- its degradation removes a key governance verification step (Source: nse-explorer-001, V-001). |
| **Dependencies** | Partially depends on AD-SEC-02 (L4 inspection for compliance verification). |
| **Implementation Priority** | 6 |
| **HARD Rule Impact** | No new HARD rule. H-18 promotion is a Tier B to Tier A reclassification within existing HARD Rule Index. L2 token consumption increases from 559 to ~599 of 850 budget. |

### AD-SEC-07: Agent Identity Foundation

| Attribute | Value |
|-----------|-------|
| **Status** | PROPOSED |
| **Addresses** | ASI06, NIST IA family; FR-SEC-001/002/003/004; V-004 (Handoff lacks crypto) |
| **Risk Reduction** | R-IA-001 (224), R-IA-002 (224), R-IA-006 (245). Aggregate RPN: 693 |
| **Design** | Phase 2 scope (foundational): (a) Agent instance ID (`{agent-name}-{ISO-timestamp}-{4-char-nonce}`) generated at Task invocation. (b) Instance ID system-set in all handoff `from_agent` fields (not agent-supplied, per FR-SEC-024). (c) Active agent registry (in-memory) tracking concurrent instances. (d) Instance ID included in all audit log entries. Future phases: cryptographic delegation tokens (Google DeepMind DCTs), conditional access policies. |
| **Trade-off** | Phase 2 identity is non-cryptographic (name-timestamp-nonce). Provides attribution and spoofing resistance but not cryptographic non-repudiation. Full cryptographic identity (Microsoft Entra-equivalent) deferred to Phase 3 due to infrastructure complexity. |
| **Dependencies** | None for basic identity. AD-SEC-08 and AD-SEC-09 depend on identity for signing and attribution. |
| **Implementation Priority** | 7 |

### AD-SEC-08: Handoff Integrity Protocol

| Attribute | Value |
|-----------|-------|
| **Status** | PROPOSED |
| **Addresses** | ASI07, ASI04, NIST SC-8; FR-SEC-021/022/023/024; V-004 |
| **Risk Reduction** | R-IC-001 (288), R-IC-002 (280), R-IC-003 (294), R-DE-004 (294), R-IA-001 (224). Aggregate RPN: 1,380 |
| **Design** | (a) SHA-256 hash of immutable handoff fields (task, success_criteria, criticality, artifacts) computed at send and included in handoff metadata. (b) L4-I05 verifies hash at receive. (c) System-set `from_agent` using agent instance ID (AD-SEC-07). (d) L3-G09 validates Task prompt size against threshold (CB-03/CB-04 enforcement). (e) Data classification tags on artifacts (PUBLIC, INTERNAL, SENSITIVE). (f) Persistent blockers propagated with `[PERSISTENT]` prefix (CP-05). |
| **Trade-off** | SHA-256 hashing adds compute overhead to every handoff. Mitigation: hashing is fast (<1ms) and deterministic. |
| **Dependencies** | Benefits from AD-SEC-01 (L3 gate) and AD-SEC-07 (agent identity). |
| **Implementation Priority** | 8 |

### AD-SEC-09: Comprehensive Audit Trail

| Attribute | Value |
|-----------|-------|
| **Status** | PROPOSED |
| **Addresses** | ASI09, NIST AU family; FR-SEC-029/030/031/032; R-CF-005 (405 -- #4 risk) |
| **Risk Reduction** | R-CF-005 (405, via post-hoc detection), R-DE-002 (294), R-GB-005 (240). Aggregate RPN: 939 |
| **Design** | (a) Structured audit log per session in JSON-lines format: `{timestamp, agent_instance_id, event_type, tool_name, parameters_hash, result_status, security_classification, trust_level}`. (b) Security event sub-log for: injection detection, tool access violations, authentication failures, circuit breaker activations, anomalous behavior. (c) L3-G06 write restriction: Write tool blocked from audit log directories. (d) Audit logs committed to git at session end (append-only in-session). (e) Provenance chain: user -> orchestrator instance ID -> worker instance ID -> tool invocation. |
| **Trade-off** | Audit logging increases session file I/O and storage. Mitigation: JSON-lines format is compact; session-scoped files are bounded; git compression handles storage. |
| **Dependencies** | Benefits from AD-SEC-01 (L3 gate provides interception points), AD-SEC-02 (L4 provides security events), and AD-SEC-07 (identity for attribution). |
| **Implementation Priority** | 9 |

### AD-SEC-10: Adversarial Testing Program

| Attribute | Value |
|-----------|-------|
| **Status** | PROPOSED |
| **Addresses** | R-CF-005 (405 -- #4 risk); NFR-SEC-012; quality gate calibration |
| **Risk Reduction** | R-CF-005 (405), R-GB-002 (240), R-CF-004 (120). Aggregate RPN: 765 |
| **Design** | (a) Red team test suite covering all OWASP ASI-01 through ASI-10 attack vectors against Jerry's implemented controls. (b) Canary attacks: known-bad inputs injected periodically to verify detection rates per layer (L3/L4 detection rate targets: L3 >99%, L4 >95%). (c) Quality gate calibration: known-quality deliverables scored periodically to detect scorer drift (S-014 LLM-as-Judge). (d) Detection rate tracking dashboard per enforcement layer. (e) Leverages existing /adversary skill (S-001 Red Team strategy). |
| **Trade-off** | Ongoing operational commitment. Mitigation: automate test suite execution in CI (L5); manual red team exercises on quarterly cadence. |
| **Dependencies** | Benefits from all other decisions being in place (tests validate the implemented controls). Should run continuously from Phase 3 onward. |
| **Implementation Priority** | 10 |

### Decision Dependency Map

```
AD-SEC-01 (L3 Gate Infrastructure) ---- FOUNDATIONAL
    |
    +-- AD-SEC-04 (Bash Hardening) depends on L3 gates
    +-- AD-SEC-08 (Handoff Integrity) benefits from L3 gates
    |
AD-SEC-02 (Tool-Output Firewall) ---- INDEPENDENT, HIGHEST RISK REDUCTION
    |
    +-- AD-SEC-05 (Secret Detection) benefits from L4 infrastructure
    +-- AD-SEC-06 (Context Rot) benefits from L4 compliance checking
    +-- AD-SEC-09 (Audit Trail) benefits from L4 security events
    |
AD-SEC-07 (Agent Identity) ---- INDEPENDENT
    |
    +-- AD-SEC-08 (Handoff Integrity) depends on identity for signing
    +-- AD-SEC-09 (Audit Trail) depends on identity for attribution
    |
AD-SEC-03 (MCP Verification) ---- INDEPENDENT
AD-SEC-10 (Adversarial Testing) ---- DEPENDS ON ALL (validates them)
```

**Recommended implementation order:**
1. AD-SEC-01 (L3 Gate) -- foundational, LOW complexity
2. AD-SEC-02 (Tool-Output Firewall) -- highest risk reduction, MEDIUM complexity
3. AD-SEC-03 (MCP Verification) -- second highest risk, MEDIUM complexity
4. AD-SEC-05 (Secret Detection) -- LOW complexity, high value
5. AD-SEC-04 (Bash Hardening) -- depends on AD-SEC-01
6. AD-SEC-06 (Context Rot) -- depends on AD-SEC-02 partially
7. AD-SEC-07 (Agent Identity) -- HIGH complexity, long lead time
8. AD-SEC-08 (Handoff Integrity) -- depends on AD-SEC-01 and AD-SEC-07
9. AD-SEC-09 (Audit Trail) -- depends on AD-SEC-01, AD-SEC-02, and AD-SEC-07
10. AD-SEC-10 (Adversarial Testing) -- validates all others

---

## Cross-Framework Compliance Mapping

### OWASP Agentic Top 10 (Post-Architecture)

| OWASP Item | Phase 1 Status | Architecture Response | Post-Architecture Status |
|------------|---------------|----------------------|------------------------|
| ASI-01 Agent Goal Hijack | PARTIAL | AD-SEC-02 (Tool-Output Firewall), AD-SEC-06 (Context Rot Hardening), L4-I01 (Injection Scanner) | **COVERED** |
| ASI-02 Tool Misuse | PARTIAL | AD-SEC-01 (L3 Tool Access Matrix), AD-SEC-04 (Bash Hardening), L3-G01/G02/G03/G04 | **COVERED** |
| ASI-03 Privilege Escalation | PARTIAL | AD-SEC-01 (Tier Enforcement), Privilege Non-Escalation Invariant, Rule of Two | **COVERED** |
| ASI-04 Supply Chain | **GAP** | AD-SEC-03 (MCP Verification), L5-S03/S05, Registry | **COVERED** |
| ASI-05 Code Execution | PARTIAL | AD-SEC-04 (Bash Hardening), L3-G04 (Command Gate), HITL for restricted commands | **COVERED** |
| ASI-06 Memory/Context Poisoning | PARTIAL | AD-SEC-06 (Context Rot), AD-SEC-02 (Content-Source Tagging), L4-I01/I02 | **COVERED** |
| ASI-07 Inter-Agent Comm | PARTIAL | AD-SEC-08 (Handoff Integrity), L4-I05, SHA-256 hashing, system-set from_agent | **COVERED** |
| ASI-08 Cascading Failures | PARTIAL | AD-SEC-08 (Failure propagation), H-36 circuit breaker, Fail-Closed design | **COVERED** |
| ASI-09 Insufficient Logging | PARTIAL | AD-SEC-09 (Audit Trail), L4-I07, security event sub-log, provenance chain | **COVERED** |
| ASI-10 Rogue Agents | PARTIAL | AD-SEC-01 (L3 enforcement), L4-I06 (Behavioral Drift), AD-SEC-07 (Identity) | **COVERED** |

**Result: 10/10 COVERED (up from 0/10 COVERED, 9/10 PARTIAL, 1/10 GAP)**

### MITRE ATLAS Agent Techniques (Post-Architecture)

| Technique | Phase 1 Status | Architecture Response | Post-Architecture Status |
|-----------|---------------|----------------------|------------------------|
| AML.T0080 Context Poisoning | PARTIAL | AD-SEC-06, L2 Tier A promotion, L4 content scanning | **COVERED** |
| AML.T0080.000 Memory Poisoning | GAP | AD-SEC-02 (L4 content scanning on retrieve), integrity hashing | **COVERED** |
| AML.T0080.001 Thread Poisoning | PARTIAL | AD-SEC-02 (Tool-Output Firewall), content-source tagging | **COVERED** |
| AML.T0081 Modify Agent Config | PARTIAL | L3 hash verification, L5-S01/S02, uncommitted modification detection | **COVERED** |
| AML.T0082 Credential Harvesting | PARTIAL | AD-SEC-05 (Secret Detection), L3-G05 (sensitive file blocking) | **COVERED** |
| AML.T0083 Credentials from Config | GAP | L3-G05, L3-G12 (env var filtering), L4-I03 (secret scanning) | **COVERED** |
| AML.T0084 Discover Agent Config | GAP | L3-G05 (partial -- configs readable by design), L4-I04 (canary detection) | **PARTIAL** (by design: agent configs must be readable for the framework to function) |
| AML.T0084.002 Discover Triggers | GAP | Same as above -- trigger map is readable by design for transparency | **PARTIAL** (accepted risk: transparency vs. security trade-off, documented) |
| AML.T0086 Exfiltration via Tool | PARTIAL | AD-SEC-04 (network command blocking), L3-G11 (URL allowlist), L4-I03 (DLP) | **COVERED** |

**Result: 7/9 COVERED, 2/9 PARTIAL (up from 0/9 COVERED, 5/9 PARTIAL, 4/9 GAP). The 2 remaining PARTIAL items (AML.T0084, AML.T0084.002) are accepted risks -- Jerry's architecture requires readable configs for transparency; this is a deliberate design choice per P-022 (no deception).**

### NIST SP 800-53 Key Control Families (Post-Architecture)

| Family | Phase 1 Status | Architecture Response | Post-Architecture Status |
|--------|---------------|----------------------|------------------------|
| AC (Access Control) | PARTIAL | AD-SEC-01 (L3 runtime enforcement), Rule of Two, privilege non-escalation | **COVERED** |
| AU (Audit) | **GAP** | AD-SEC-09 (Comprehensive Audit Trail), L4-I07, security event logging | **COVERED** |
| CM (Configuration Mgmt) | PARTIAL | L3 hash verification, L5-S01/S02/S03, MCP registry | **COVERED** |
| IA (Identification) | **GAP** | AD-SEC-07 (Agent Identity Foundation), instance IDs, system-set from_agent | **COVERED** (foundational; full crypto identity in Phase 3) |
| IR (Incident Response) | PARTIAL | Fail-closed design, graceful degradation levels, containment mechanism | **COVERED** |
| SC (System Protection) | PARTIAL | L3-G11 (URL allowlist), L3-G04 (network blocking), content-source tagging | **COVERED** |
| SI (System Integrity) | PARTIAL | AD-SEC-02 (L4 Tool-Output Firewall), L3 input validation, L4 output sanitization | **COVERED** |
| SR (Supply Chain) | **GAP** | AD-SEC-03 (MCP Verification), L5-S05 (CVE scanning), registry | **COVERED** |
| SA (System Acquisition) | PARTIAL | MCP registry with audit dates, agent definition schema validation | **COVERED** |
| RA (Risk Assessment) | COVERED | Phase 1 FMEA risk register, this threat model | **COVERED** |

**Result: 10/10 COVERED (up from 1/10 COVERED, 6/10 PARTIAL, 3/10 GAP)**

---

## Requirements Traceability Matrix

This matrix maps all 57 security requirements (42 FR-SEC + 15 NFR-SEC) to their covering architecture decisions, enforcement gates, and implementation priority. Requirements are organized by coverage status from Phase 1. (Source: nse-requirements-001, all FR/NFR-SEC requirements; ps-analyst-001, Requirements-to-Gap Mapping)

### Previously Zero-Coverage Requirements (18 total -- all now architecturally addressed)

| Requirement | Title | Priority | Covering Decision(s) | Enforcement Gate(s) | Implementation Priority |
|-------------|-------|----------|---------------------|---------------------|------------------------|
| FR-SEC-001 | Unique Agent Identity | CRITICAL | AD-SEC-07 | L3-G09 (identity check) | 7 |
| FR-SEC-002 | Agent Authentication at Trust Boundaries | CRITICAL | AD-SEC-07, AD-SEC-08 | L3-G09, L4-I05 | 7, 8 |
| FR-SEC-003 | Agent Identity Lifecycle Management | HIGH | AD-SEC-07 | Active agent registry (in-memory); instance ID creation at Task, invalidation at completion (lines 399-403) | 7 |
| FR-SEC-004 | Agent Provenance Tracking | HIGH | AD-SEC-07, AD-SEC-09 | L4-I07 (audit logger); provenance chain: user -> orchestrator -> worker -> tool | 7, 9 |
| FR-SEC-009 | Toxic Tool Combination Prevention | HIGH | AD-SEC-01 (L3 gate) | L3-G03 (Toxic Combination Check) | 1 |
| FR-SEC-011 | Direct Prompt Injection Prevention | CRITICAL | AD-SEC-01, AD-SEC-02 | L3-G01 (advisory at Trust 0), L4-I01 (injection scanner) | 1, 2 |
| FR-SEC-012 | Indirect Prompt Injection via Tool Results | CRITICAL | AD-SEC-02 | L4-I01 (injection scanner), L4-I02 (content-source tagger) | 2 |
| FR-SEC-013 | MCP Server Input Sanitization | CRITICAL | AD-SEC-03 | L3-G08 (MCP output sanitize) | 3 |
| FR-SEC-015 | Agent Goal Integrity Verification | HIGH | AD-SEC-02 | L4-I06 (Behavioral Drift Monitor): compares agent action sequence against declared task and cognitive mode; advisory warning at significant drift, HITL at critical drift | 2 |
| FR-SEC-019 | System Prompt Leakage Prevention | HIGH | AD-SEC-05 | L4-I04 (System Prompt Canary) | 5 |
| FR-SEC-023 | Message Integrity in Handoff Chains | MEDIUM | AD-SEC-08 | L4-I05 (Handoff Integrity Verifier): SHA-256 hash of immutable fields | 8 |
| FR-SEC-025 | MCP Server Integrity Verification | CRITICAL | AD-SEC-03 | L3-G07 (MCP Registry Gate), L5-S03 | 3 |
| FR-SEC-029 | Comprehensive Agent Action Audit Trail | CRITICAL | AD-SEC-09 | L4-I07 (Audit Logger); JSON-lines format per session | 9 |
| FR-SEC-030 | Security Event Logging | HIGH | AD-SEC-09 | L4-I07 security event sub-log: injection detection, tool access violations, authentication failures, circuit breaker activations, anomalous behavior (line 851) | 9 |
| FR-SEC-031 | Anomaly Detection Triggers | MEDIUM | AD-SEC-02 | L4-I06 (Behavioral Drift Monitor): thresholds for "significant drift" (advisory) and "critical drift" (HITL); calibrated against declared cognitive mode and task scope | 2 |
| FR-SEC-033 | Agent Containment Mechanism | CRITICAL | AD-SEC-01 | L3-G09 delegation gate + H-36 circuit breaker + fail-closed design; containment = block all tool invocations for the contained agent instance | 1 |
| FR-SEC-036 | Recovery Procedures After Security Incidents | MEDIUM | AD-SEC-06, AD-SEC-09 | AE-006 graduated escalation (WARNING -> CRITICAL -> EMERGENCY -> COMPACTION); session restart with Memory-Keeper state preservation; audit log provides forensic data for post-incident analysis | 6, 9 |
| FR-SEC-037 | Rogue Agent Detection | CRITICAL | AD-SEC-02, AD-SEC-07 | L4-I06 (Behavioral Drift Monitor) + agent instance ID attribution; detection signals: action pattern divergence from cognitive mode, tool invocations outside declared scope, output inconsistent with task | 2, 7 |

### Previously Partial-Coverage Requirements (26 total -- all now architecturally extended)

| Requirement | Title | Priority | Existing Control | Architecture Extension | Gate(s) |
|-------------|-------|----------|-----------------|----------------------|---------|
| FR-SEC-005 | Least Privilege Tool Access Enforcement | CRITICAL | T1-T5 tiers | L3 runtime enforcement | L3-G01, L3-G02 |
| FR-SEC-006 | Tool Tier Boundary Enforcement | CRITICAL | T1-T5, L5 CI | L3 runtime gate | L3-G02 |
| FR-SEC-007 | Forbidden Action Enforcement | CRITICAL | H-35, guardrails | L3/L4 runtime check | L3-G01, L4-I06 |
| FR-SEC-008 | Privilege Non-Escalation in Delegation | CRITICAL | P-003 | L3 privilege intersection | L3-G09 |
| FR-SEC-010 | Permission Boundary Isolation | HIGH | Task isolation | L3 prompt size check | L3-G09 (CB-03/CB-04) |
| FR-SEC-014 | Context Manipulation Prevention | HIGH | L2, AE-006 | L4 integrity checks | L4-I01, L4-I02 |
| FR-SEC-016 | Encoding Attack Prevention | MEDIUM | L3 concept | L3-G04 Unicode normalization: normalize input to NFC before pattern matching; apply multi-layer decoding (URL decode, HTML entity decode, Base64 detect) before classification | L3-G04 |
| FR-SEC-017 | Sensitive Information Output Filtering | CRITICAL | Behavioral guardrail | L4 deterministic detection | L4-I03 |
| FR-SEC-018 | Output Sanitization for Downstream | HIGH | Handoff schema | L4 content validation | L4-I05 |
| FR-SEC-020 | Confidence and Uncertainty Disclosure | MEDIUM | P-022, handoff | Forced uncertainty on C2+ | L4-I06 (advisory) |
| FR-SEC-021 | Structured Handoff Protocol Enforcement | HIGH | HD-M-001-005 | L3 enforcement | L3-G09, L4-I05 |
| FR-SEC-022 | Trust Boundary Enforcement at Handoffs | HIGH | CP-01-05 | L3 criticality check | L3-G09 (HD-M-004) |
| FR-SEC-024 | Anti-Spoofing for Agent Communication | HIGH | from_agent field | System-set from_agent | L3-G09 (AD-SEC-07) |
| FR-SEC-026 | Dependency Verification for Agent Defs | HIGH | H-34, L5 CI | L3 runtime schema check | L3-G10 |
| FR-SEC-027 | Skill Integrity Verification | HIGH | H-25/H-26 | L3 hash check | L3 session-start check |
| FR-SEC-028 | Python Dependency Supply Chain | MEDIUM | H-05, uv.lock | L5 CVE scanning | L5-S05 |
| FR-SEC-032 | Audit Log Integrity Protection | MEDIUM | Git tracking | Append-only + write restriction | L3-G06 |
| FR-SEC-034 | Cascading Failure Prevention | HIGH | Multi-skill propagation | Structured failure reports | AD-SEC-08 |
| FR-SEC-035 | Graceful Degradation Under Security Events | HIGH | AE-006, fallback | Formalized levels | AD-SEC-06 |
| FR-SEC-038 | HITL for High-Impact Actions | CRITICAL | P-020 | L3 action classification | L3-G03, L3-G04, L3-G05 |
| FR-SEC-039 | Recursive Delegation Prevention | CRITICAL | P-003/H-01 | L3 delegation depth | L3-G09 |
| FR-SEC-040 | Unbounded Consumption Prevention | HIGH | AE-006, H-36 | Token budget tracking | L3-G09 (routing_depth), AE-006 |
| FR-SEC-041 | Secure Configuration Management | HIGH | AE rules, L5 CI | Runtime drift detection | L3 hash checks, L5-S02/S03 |
| FR-SEC-042 | Secure Defaults for New Agents | MEDIUM | H-34, guardrails | Template enforcement | L5-S01, L5-S06 |
| NFR-SEC-004 | Security Subsystem Independence | HIGH | 5-layer architecture | Layer failure isolation | Fail-closed design table |
| NFR-SEC-006 | Fail-Closed Security Default | CRITICAL | L3 concept | Defined for every checkpoint | All L3, L4 gates |

### Previously Fully-Covered Requirements (13 total -- validated by architecture)

| Requirement | Title | Priority | Covering Control | Architecture Validation |
|-------------|-------|----------|-----------------|----------------------|
| NFR-SEC-001 | Security Control Latency Budget | HIGH | L3/L4 deterministic | L3 <50ms, L4 <170ms budgets confirmed |
| NFR-SEC-002 | Security Token Budget | HIGH | L2 budget 559/850 | Budget impact: 559 -> ~599 (H-18 promotion) |
| NFR-SEC-003 | Deterministic Security Control Performance | MEDIUM | L3/L5 context-rot immune | All L3 gates deterministic; L4 pattern-based |
| NFR-SEC-005 | MCP Failure Resilience | HIGH | MCP error handling | MCP registry + fallback policy |
| NFR-SEC-007 | Security Model Scalability | MEDIUM | Routing scaling roadmap | Gate pipeline extensible (NFR-SEC-015) |
| NFR-SEC-008 | Security Rule Set Scalability | MEDIUM | HARD rule ceiling 25/25 | No new HARD rules; compound sub-items |
| NFR-SEC-009 | Minimal Security Friction for Routine Ops | HIGH | Criticality C1-C4 | C1 advisory only; C4 full enforcement |
| NFR-SEC-010 | Clear Security Event Communication | HIGH | P-022, AE-006 | Fail-closed user messages defined |
| NFR-SEC-011 | Security Rule Hot-Update | MEDIUM | File-based rules | Configuration-driven gate registries |
| NFR-SEC-012 | Security Control Testability | HIGH | H-20, L5 CI, /adversary | AD-SEC-10 adversarial testing program |
| NFR-SEC-013 | Security Architecture Documentation | MEDIUM | ADRs, quality gate | This document + 10 AD-SEC decisions |
| NFR-SEC-014 | Security Compliance Traceability | HIGH | RTM, WORKTRACKER | This RTM section |
| NFR-SEC-015 | Security Model Extensibility | MEDIUM | File-based, schema | Config-driven registries (YAML) |

### RTM Coverage Summary

| Coverage Category | Phase 1 Count | Phase 2 Count | Change |
|-------------------|---------------|---------------|--------|
| Fully Covered (architecture addresses) | 13 | 57 | +44 |
| Partial (needs extension) | 26 | 0 | -26 |
| No Coverage (new capability needed) | 18 | 0 | -18 |
| **Total** | **57** | **57** | -- |

### Phase 2 Architecture Completion Criteria

The following acceptance tests determine when Phase 2 architecture design is complete and Phase 3 implementation can begin:

| # | Criterion | Verification Method | Status |
|---|-----------|-------------------|--------|
| AC-01 | All 7 work items (ST-019 through ST-025) have dedicated architecture sections | Section presence check | PASS |
| AC-02 | All 5 FMEA risks with RPN >= 400 have explicit architecture responses | Executive Summary table + STRIDE cross-reference | PASS |
| AC-03 | All 18 zero-coverage requirements have architecture coverage in RTM | RTM zero-coverage section completeness | PASS |
| AC-04 | All 26 partial-coverage requirements have architecture extensions in RTM | RTM partial-coverage section completeness | PASS |
| AC-05 | Cross-framework compliance mapping shows improvement from Phase 1 | OWASP 10/10, MITRE 7/9, NIST 10/10 | PASS |
| AC-06 | No new HARD rules required (stays within 25/25 ceiling) | HARD Rule Impact in all 10 decisions | PASS |
| AC-07 | All 10 architecture decisions have: Status, Addresses, Risk Reduction, Design, Trade-off, Dependencies, Priority, Complexity | Decision completeness check | PASS |
| AC-08 | L3 gate registry complete with latency budgets within NFR-SEC-001 | L3 gate table, sum <= 50ms | PASS |
| AC-09 | L4 inspector registry complete with latency budgets within NFR-SEC-001 | L4 inspector table, sum <= 200ms | PASS |
| AC-10 | Fail-closed behavior defined for every security checkpoint | Fail-closed design table completeness | PASS |
| AC-11 | Quality gate score >= 0.95 weighted composite (C4 elevated target) | S-014 LLM-as-Judge scoring | PENDING (Iteration 2) |

---

## Open Issues and Risks

### Accepted Risks

| # | Risk | Justification | Mitigation |
|---|------|--------------|------------|
| AR-01 | Agent configuration files remain readable (AML.T0084) | Jerry's architecture requires agent definitions, SKILL.md, and trigger maps to be readable for the framework to function. Hiding them would violate P-022 (no deception) and break core functionality. | L4-I04 canary tokens detect extraction attempts. L4-I03 redacts sensitive content in output. Security-critical details (secret patterns, hash values) stored in separate security config files with L3-G05 protection. |
| AR-02 | L4 injection detection has inherent false negatives | Regex-based pattern matching cannot detect all possible injection patterns. Novel injection techniques will bypass the scanner. | Defense-in-depth: L2 re-injection provides resilience even when injection succeeds. AD-SEC-10 adversarial testing continuously calibrates detection. Pattern database is extensible (NFR-SEC-015). |
| AR-03 | Phase 2 agent identity is non-cryptographic | Name-timestamp-nonce provides attribution and collision resistance but not cryptographic non-repudiation. | Sufficient for Phase 2 scope (attribution, audit logging, spoofing resistance). Full cryptographic identity (DCTs) designed for Phase 3. |
| AR-04 | Quality gate (S-014) remains LLM-based and manipulable (V-005) | LLM-based scoring is inherently susceptible to adversarial manipulation. Deterministic replacement would sacrifice the nuanced evaluation that makes quality gates effective. | Multi-scorer consensus (2+ independent passes), calibration benchmarks, deterministic pre-checks (H-34 schema) before LLM scoring. FC-M-001 fresh context isolation reduces anchoring. |

### Open Issues

| # | Issue | Impact | Required Action | Target Phase |
|---|-------|--------|----------------|-------------|
| OI-01 | HARD rule ceiling at 25/25 with zero headroom (B-003) | Security requirements implementable within existing HARD rules via compound sub-items (H-34/H-35/H-36). No new HARD rules required by this architecture. If future security needs require new HARD rules, the ceiling exception mechanism (max N=3, 3-month duration) is available. | Validate post-implementation that all security controls fit within existing rules. | Phase 3 validation |
| OI-02 | L4 injection pattern database needs empirical calibration | False positive/negative rates unknown until production deployment. NFR-SEC-012 requires >=95% test coverage. | Build initial pattern database from OWASP injection examples and published attack payloads. Calibrate thresholds from first 100 detection events. | Phase 3 implementation |
| OI-03 | Cisco MCP scanner integration feasibility unknown | Cisco released open-source MCP security scanners. Integration with Jerry's L5 pipeline is unvalidated. | Evaluate Cisco MCP scanner capabilities against FR-SEC-025 requirements. | Phase 3 research |
| OI-04 | Content-source tagging mechanism at model level | How content-source tags are represented and consumed by the LLM is an implementation detail that depends on Claude API capabilities. XML tags, system messages, or prefix conventions are all candidates. | Prototype content-source tagging with Claude API; measure effectiveness of different tag formats. | Phase 3 prototyping |
| OI-05 | Cryptographic delegation tokens for Phase 3 | Google DeepMind DCTs (Macaroons/Biscuits) provide the theoretical model. Local-first implementation without central authority is an open research question. | Research local-first delegation token implementations. Evaluate DelegateOS (Biscuit-based DCTs). | Phase 3 research |

### Risk to Implementation

| # | Risk | Likelihood | Impact | Mitigation |
|---|------|-----------|--------|------------|
| RI-01 | L3/L4 security gates conflict with existing non-security L3/L4 behavior | MEDIUM | Architecture rework needed | This architecture explicitly designs security as extensions to existing layers, not replacements. L3 gates are additive; L4 inspectors are additive. |
| RI-02 | Security token overhead pushes context fill past AE-006 thresholds | LOW | Reduced context for work | NFR-SEC-002 caps security token consumption at 10% (20K of 200K). L3 gates consume zero tokens. L4 inspectors produce compact structured output. L2 budget: 559 -> ~599 tokens (Tier A promotion). |
| RI-03 | Performance degradation from cumulative L3/L4 latency | LOW | User experience degradation | Total worst-case: L3 50ms + L4 170ms = 220ms per tool invocation. Acceptable compared to LLM inference time (1-30 seconds). |

---

## Citations

All claims in this document trace to Phase 1 input artifacts and Jerry's rules files.

### Phase 1 Artifact References

| Artifact | Agent | Location |
|----------|-------|----------|
| Security Gap Analysis | ps-analyst-001 | `projects/PROJ-008-agentic-security/orchestration/agentic-sec-20260222-001/ps/phase-1/ps-analyst-001/ps-analyst-001-gap-analysis.md` |
| Competitive Landscape | ps-researcher-001 | `projects/PROJ-008-agentic-security/orchestration/agentic-sec-20260222-001/ps/phase-1/ps-researcher-001/ps-researcher-001-competitive-landscape.md` |
| Threat Framework Analysis | ps-researcher-002 | `projects/PROJ-008-agentic-security/orchestration/agentic-sec-20260222-001/ps/phase-1/ps-researcher-002/ps-researcher-002-threat-framework-analysis.md` |
| OpenClaw Feature Analysis | ps-researcher-001 | `projects/PROJ-008-agentic-security/orchestration/agentic-sec-20260222-001/ps/phase-1/ps-researcher-001/ps-researcher-001-openclaw-feature-analysis.md` |
| NSE-to-PS Handoff | Barrier 1 | `projects/PROJ-008-agentic-security/orchestration/agentic-sec-20260222-001/cross-pollination/barrier-1/nse-to-ps/handoff.md` |
| Security Requirements | nse-requirements-001 | `projects/PROJ-008-agentic-security/orchestration/agentic-sec-20260222-001/nse/phase-1/nse-requirements-001/nse-requirements-001-security-requirements.md` |
| Risk Register (FMEA) | nse-explorer-001 | `projects/PROJ-008-agentic-security/orchestration/agentic-sec-20260222-001/nse/phase-1/nse-explorer-001/nse-explorer-001-risk-register.md` |

### Jerry Framework Rule References

| File | Key Content Referenced |
|------|----------------------|
| `quality-enforcement.md` | L1-L5 enforcement architecture, HARD Rule Index, Two-Tier Model, L2 token budget (559/850), AE-006, criticality levels |
| `agent-development-standards.md` | Tool tiers T1-T5, handoff protocol, H-34/H-35, guardrails template, CB-01-CB-05 |
| `agent-routing-standards.md` | Circuit breaker H-36, anti-patterns, FMEA thresholds |
| `mcp-tool-standards.md` | MCP-001/MCP-002, error handling, agent integration matrix |

### Specific Citation Traces

| Claim | Source | Location |
|-------|--------|----------|
| "R-PI-002 is #1 risk at RPN 504" | nse-explorer-001 | Category 1, R-PI-002 |
| "R-SC-001 is #2 risk at RPN 480" | nse-explorer-001 | Category 3, R-SC-001 |
| "R-GB-001 is #3 risk at RPN 432" | nse-explorer-001 | Category 8, R-GB-001 |
| "R-CF-005 is #4 risk at RPN 405" | nse-explorer-001 | Category 9, R-CF-005 |
| "R-PI-003 is #5 risk at RPN 392" | nse-explorer-001 | Category 1, R-PI-003 |
| "0/10 OWASP Agentic COVERED in Phase 1" | ps-analyst-001 | Gap Matrix, line 72 |
| "18 requirements with zero coverage" | ps-analyst-001 | Requirements-to-Gap Mapping, lines 248-271 |
| "L3 is the primary security enforcement point; 12 of 42 FR map to L3" | nse-requirements-001 | Finding 2, lines 984-987 |
| "L2 token budget: 559/850 tokens used, 291 remaining" | quality-enforcement.md | HARD Rule Ceiling Derivation |
| "Meta Rule of Two: max 2 of (untrusted input, sensitive data, external state change)" | nse-requirements-001 | Finding 5, lines 996-998 |
| "Defense-in-depth is the only viable strategy; 12 defenses bypassed >90%" | ps-researcher-002 | Executive Summary; nse-explorer-001, line 42 |
| "MCP creates a vast unmonitored attack surface" | ps-researcher-001 | Cisco citation C27 |
| "V-001 through V-006 Jerry-specific vulnerabilities" | nse-explorer-001 | Jerry-Specific Vulnerabilities, lines 372-434 |
| "Tool-Output Firewall addresses aggregate RPN of 1,636" | nse-explorer-001 | Mitigation Priority 1, line 444 |
| "10 recommended architecture decisions with dependency map" | ps-analyst-001 | Recommended Phase 2 Architecture Priorities, lines 328-475 |
| "57 total security requirements (42 FR + 15 NFR)" | nse-requirements-001 | Executive Summary |
| "60 FMEA failure modes across 10 categories" | nse-explorer-001 | Executive Summary |
| "NFR-SEC-001: L3 < 50ms, L4 < 200ms latency" | nse-requirements-001 | NFR-SEC-001 |
| "NFR-SEC-006: Fail-closed default" | nse-requirements-001 | NFR-SEC-006 |
| "NFR-SEC-009: Minimal friction for C1 tasks" | nse-requirements-001 | NFR-SEC-009 |
| "FR-SEC-024: System-set from_agent" | nse-requirements-001 | FR-SEC-024 |
| "FR-SEC-009: Toxic tool combination prevention" | nse-requirements-001 | FR-SEC-009 |
| "Microsoft Entra Agent ID" | ps-researcher-001 | Citation C21 |
| "Google DeepMind Delegation Capability Tokens" | ps-researcher-001 | Citation C31 |
| "Cisco open-source MCP scanners" | ps-researcher-001 | Citation C27 |
| "Anthropic Claude Code sandboxing: 95% attack surface reduction" | ps-researcher-001 | Citation C8 |
| "Error amplification ~1.3x with structured handoffs" | agent-development-standards.md | Pattern 2: Orchestrator-Worker |
| "No new HARD rules required: HARD ceiling at 25/25" | quality-enforcement.md | HARD Rule Ceiling |

---

<!-- Self-Review (S-010) Checklist -- Revision 2 (post S-014 scoring):
- [x] Navigation table with anchor links (H-23)
- [x] Executive Summary (L0) with top 5 FMEA risks and architecture response
- [x] Threat Model (ST-019): STRIDE analysis across 6 components; DREAD scoring for top 10 scenarios; DREAD aggregation method justified
- [x] Attack Surface Map (ST-020): 17 entry points across 4 trust levels; data flow diagram; Memory-Keeper trust classification clarified
- [x] Trust Boundary Analysis (ST-021): 5 trust zones; 10 boundary crossings with enforcement matrix
- [x] Zero-Trust Execution Model (ST-022): 5-step verification; agent instance ID; toxic combination registry (Rule of Two)
- [x] Privilege Isolation (ST-023): Extended T1-T5 with L3 enforcement; privilege non-escalation; command allowlists; sensitive file patterns
- [x] Deterministic Verification (ST-024): 12 L3 gates with latency; 7 L4 inspectors with seed patterns; 8 L5 CI gates; fail-closed design
- [x] Supply Chain Security (ST-025): MCP registry; agent definition pipeline; Python dependency chain; skill integrity
- [x] 10 Architecture Decisions with dependency map, implementation order, AND complexity estimates
- [x] Cross-Framework Compliance: OWASP Agentic 10/10 COVERED; MITRE ATLAS 7/9 COVERED + 2 accepted; NIST 10/10 COVERED
- [x] Requirements Traceability Matrix: All 57 requirements (42 FR + 15 NFR) mapped to decisions and gates
- [x] Phase 2 Completion Criteria: 11 acceptance tests defined
- [x] Open Issues and Risks: 4 accepted risks; 5 open issues; 3 implementation risks
- [x] All claims cite Phase 1 artifacts with specific locations
- [x] TOP 5 FMEA risks (RPN >= 400) explicitly addressed
- [x] Meta's Rule of Two incorporated as toxic combination registry
- [x] No new HARD rules required (within 25/25 ceiling)
- [x] L2 token budget impact analyzed (559 -> ~599 of 850)
- [x] NFR-SEC-001 latency requirements verified (L3 < 50ms, L4 < 170ms)
- [x] NFR-SEC-006 fail-closed design for all checkpoints
- [x] NFR-SEC-009 proportional security friction by criticality
- [x] P-003 compliance: no recursive subagents in design
- [x] P-020 compliance: user authority preserved; HITL for high-impact
- [x] P-022 compliance: transparent about limitations and accepted risks
- [x] Iteration 1 S-014 findings addressed: RTM added, complexity estimates added, seed patterns added, FR-SEC-016 encoding attack addressed, Memory-Keeper trust clarified, DREAD averaging justified
-->

*Security Architecture Version: 1.0.0 | Agent: ps-architect-001 | Pipeline: PS | Phase: 2 | Criticality: C4*
*Quality Target: >= 0.95 weighted composite across 6 dimensions*
*Source: Phase 1 artifacts (ps-analyst-001, ps-researcher-001, ps-researcher-002, nse-requirements-001, nse-explorer-001)*
