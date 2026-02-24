# S-003: Phase 1 Research Compendium

> Phase 1 Research Compendium | PROJ-010 Cyber Ops

## Document Sections

| Section | Purpose |
|---------|---------|
| [Executive Summary](#executive-summary) | Comprehensive overview of Phase 1 outcomes |
| [Research Inventory](#research-inventory) | All 23 research artifacts with metadata |
| [Definitive Decisions](#definitive-decisions) | All decisions made during Phase 1 research |
| [Phase 2 Readiness Assessment](#phase-2-readiness-assessment) | Per-feature readiness for FEAT-010 through FEAT-015 |
| [Requirement Fulfillment Matrix](#requirement-fulfillment-matrix) | R-001 through R-024 coverage status |
| [Risk Register](#risk-register) | Top risks identified during Phase 1 |
| [Source Authority Summary](#source-authority-summary) | Citation counts by R-006 category |
| [Research Artifact Index](#research-artifact-index) | Complete directory listing with file paths |

---

## Executive Summary

Phase 1 Research for PROJ-010 Cyber Ops is complete. Across 6 research streams, 20 primary artifacts, and 3 synthesis documents, this phase produced the definitive foundation for building two elite Jerry skills -- /eng-team (10 agents for secure-by-design software engineering) and /red-team (11 agents for offensive security operations). The combined 21-agent roster achieves 14/14 MITRE ATT&CK tactic coverage, validated by gap analysis against Google, Microsoft, CrowdStrike, Mandiant, TrustedSec, SpecterOps, and Rapid7 team structures.

Phase 1 produced 12 architecture decisions (AD-001 through AD-012) that Phase 2 must formalize as ADRs. Seven are HIGH-confidence decisions where independent research streams converged: methodology-first design (AD-001), the 21-agent roster (AD-002), two-layer portability (AD-003), three-layer authorization (AD-004), MCP-primary tool integration (AD-005), SARIF-based finding normalization (AD-006), and YAML-first rule sets (AD-007). Three are MEDIUM-confidence decisions requiring Phase 2 validation: agent isolation granularity (AD-011), progressive autonomy deployment (AD-012), and cross-skill threat intelligence integration. Two decisions have a clear recommended path that Phase 2 design will refine: layered SDLC governance (AD-008) and STRIDE+DREAD threat modeling with criticality escalation (AD-009).

The research identified three defining principles that anchor the entire architecture. First, PROJ-010 is a methodology-guidance framework with tool augmentation, not an autonomous execution engine -- LLMs excel at structured reasoning and methodology guidance but fundamentally cannot replace tool execution or human judgment for novel discovery. Second, security is an architectural property enforced through scope constraints, not an operational procedure dependent on human oversight -- out-of-scope actions should be structurally impossible rather than procedurally prevented. Third, structured data formats (JSON Schema for definitions, SARIF for findings, YAML for configuration) form the universal integration layer across tools, providers, and configurations.

The methodology framework layers five secure SDLC models (NIST SSDF for governance, MS SDL for workflow, OWASP SAMM for assessment, Google SLSA for supply chain, DevSecOps for automation), each assigned to its area of strength. Tool integration adopts MCP as the primary protocol with CLI and API adapter fallbacks, SARIF-based finding normalization, and strict "standalone capable" design where all 21 agents function without any external tools. LLM portability uses a two-layer architecture separating semantic agent intent from provider-specific rendering, achieving 63% full portability across Anthropic, OpenAI, Google, and open-source providers. Authorization implements a three-layer architecture (pre-engagement structural, runtime scope enforcement, post-execution audit) grounded in the OWASP Top 10 for Agentic Applications. Configurable rule sets adopt YAML-first definition with SonarQube-inspired profile management and ESLint-style cascading overrides.

All 24 PLAN.md requirements (R-001 through R-024) received research coverage. Research drew from 130+ unique sources across all 6 R-006 categories (Industry Leaders, Industry Experts, Industry Innovators, Community Leaders, Community Experts, Community Innovators), with sources dated 2024-2026 per R-009 (Current Intelligence). The total research corpus spans 9,863 lines across 22 persisted artifacts, with this compendium as the 23rd and final Phase 1 deliverable.

Seven open questions (OQ-001 through OQ-007) remain for Phase 2 resolution, none of which block the start of architecture work. All six Phase 2 features (FEAT-010 through FEAT-015) are assessed as READY or READY WITH CAVEATS.

---

## Research Inventory

All 23 Phase 1 research artifacts, ordered by stream and sequence.

| File ID | Title | Stream | Lines | Key Contribution |
|---------|-------|--------|------:|------------------|
| A-001 | Elite Security Engineering Team Structures | A: Role Completeness | 301 | Google, Microsoft, CrowdStrike, Mandiant team patterns; identified eng-devsecops and eng-incident gaps |
| A-002 | Red Team / Pentest Firm Structures | A: Role Completeness | 341 | TrustedSec, SpecterOps, Rapid7, Netflix patterns; identified red-infra and red-social gaps |
| A-003 | MITRE ATT&CK Capability Coverage Analysis | A: Role Completeness | 356 | 14-tactic coverage analysis; identified zero-coverage for TA0042 Resource Development and TA0005 Defense Evasion |
| A-004 | Final Roster Recommendation with Gap Analysis | A: Role Completeness | 341 | Definitive 21-agent roster; 4 deferred agents with triggers; 4 cross-skill integration points |
| B-001 | MITRE ATT&CK Framework Analysis | B: Methodology | 285 | ATT&CK as technique taxonomy; tactic-to-agent mapping for /red-team |
| B-002 | PTES and OSSTMM Methodology Analysis | B: Methodology | 297 | Offensive methodology selection; PTES 7-phase structure; OSSTMM 5-channel model |
| B-003 | OWASP, NIST, CIS, SANS Standards Analysis | B: Methodology | 417 | Defensive standards stack; agent-to-standards mapping; ASVS 5.0 3-level assurance model |
| B-004 | Threat Modeling Methodology Comparison | B: Methodology | 461 | STRIDE/DREAD/PASTA/LINDDUN/Attack Trees comparison; criticality-based escalation recommendation |
| C-001 | Offensive Tool Ecosystem Survey | C: Tool Integration | 485 | Metasploit, Nmap, Burp Suite, Nuclei, BloodHound ecosystem; integration pattern identification |
| C-002 | Defensive Tool Ecosystem Survey | C: Tool Integration | 536 | Semgrep, CodeQL, Trivy, Checkov, ZAP ecosystem; SARIF support analysis |
| C-003 | Agentic Tool Integration Patterns | C: Tool Integration | 629 | MCP protocol hierarchy; common adapter interface; SARIF normalization; standalone capable design; security controls |
| D-001 | Prior Art Survey -- Agentic Security Tools | D: Prior Art | 313 | XBOW, PentAGI, Strix, CAI survey; competitive landscape analysis |
| D-002 | LLM Capability Boundaries for Security Tasks | D: Prior Art | 465 | Capability matrix (HIGH/MEDIUM/fundamental limitations); hallucination analysis; safety alignment paradox |
| D-003 | Industry Perspectives & Source Coverage | D: Prior Art | 469 | Cross-category trend analysis; 6 differentiation opportunities; 130+ unique sources |
| E-001 | Universal Prompt Engineering Patterns | E: LLM Portability | 394 | RCCF pattern; XML anti-pattern; CoT model-dependence; JSON Schema convergence |
| E-002 | Multi-LLM Agent Framework Analysis | E: LLM Portability | 414 | CrewAI, LangChain, DSPy, Google ADK, Haystack, LiteLLM analysis; agent-as-configuration convergence |
| E-003 | Portability Architecture Recommendation | E: LLM Portability | 840 | Two-layer architecture; 4 provider adapters; 38-field portable schema; 18 validation criteria (PV-001 through PV-018) |
| F-001 | Secure SDLC Lifecycle Patterns | F: Secure SDLC | 408 | Five-layer SDLC model; MS SDL, NIST SSDF, OWASP SAMM, Google SLSA, DevSecOps comparison |
| F-002 | Security Architecture Patterns for Agent Teams | F: Secure SDLC | 391 | Three-layer authorization; OWASP Agentic AI Top 10; scope enforcement; per-agent auth model; progressive autonomy |
| F-003 | Configurable Rule Set Research | F: Secure SDLC | 502 | Semgrep, OPA/Rego, SonarQube, Checkov, ESLint analysis; YAML-first with profile management recommendation |
| S-001 | Cross-Stream Findings Consolidation | Synthesis | 502 | 6 convergence patterns; 5 conflict resolutions; requirements traceability; Phase 2 input summary |
| S-002 | Architecture Implications Synthesis | Synthesis | 716 | 12 architecture decisions (AD-001 through AD-012); specification input for FEAT-010/011/015; 7 open questions |
| S-003 | Phase 1 Research Compendium | Synthesis | -- | This document: definitive Phase 1 reference; research inventory; decisions roll-up; readiness assessment |

**Totals:** 23 artifacts across 7 directories (6 streams + 1 synthesis). 9,863 lines of primary research content (excluding this compendium).

---

## Definitive Decisions

All decisions made during Phase 1 research, organized by domain.

### Roster Decisions (from A-004)

| Decision | Detail | Confidence |
|----------|--------|------------|
| /eng-team roster: 10 agents | Baseline 8 + eng-devsecops (automated security tooling) + eng-incident (post-deployment response) | HIGH |
| /red-team roster: 11 agents | Baseline 9 + red-infra (C2, tool development, infrastructure OPSEC) + red-social (human attack vector) | HIGH |
| eng-security scope narrowed | Automated tooling moved to eng-devsecops; eng-security focuses on manual secure code review and security requirements verification | HIGH |
| eng-infra scope expanded | Added supply chain security: SBOM generation, dependency provenance, build reproducibility | HIGH |
| red-lead scope expanded | Added operational OPSEC, QA, adaptation decisions (absorbed from deferred red-opsec) | HIGH |
| red-exploit scope expanded | Added Impact (TA0040) technical demonstration and phase-specific evasion | MEDIUM |
| red-lateral scope narrowed | C2 infrastructure moved to red-infra; red-lateral focuses on pivoting, tunneling, LotL | HIGH |
| red-reporter scope expanded | Added Impact risk documentation and scope compliance attestation | MEDIUM |
| Defense Evasion distributed | red-infra owns tool-level evasion; each operational agent owns phase-specific evasion; no standalone evasion agent | HIGH |
| eng-threatintel deferred | Cross-skill integration with red-recon covers primary use case; reconsider if /eng-team deploys independently | MEDIUM |
| eng-compliance deferred | Configurable rule sets (R-011) serve compliance better than a static agent | HIGH |
| red-opsec deferred | Decomposes into red-infra (infrastructure OPSEC) + red-lead (operational OPSEC) | HIGH |
| red-cloud deferred | Explicitly out of scope per PLAN.md; future extension | HIGH |
| 4 cross-skill integration points | Threat-Informed Architecture, Attack Surface Validation, Secure Code vs. Exploitation, Incident Response Validation | HIGH |
| Non-linear kill chain workflow | Agents invocable in any order after red-lead scope; kill chain organizes capability, not sequence | HIGH |

### Architecture Decisions (from S-002: AD-001 through AD-012)

| Decision ID | Title | Confidence | Phase 2 Feature |
|-------------|-------|------------|-----------------|
| AD-001 | Methodology-first design paradigm (not autonomous execution) | HIGH | ALL |
| AD-002 | 21-agent roster (10 /eng-team + 11 /red-team) | HIGH | FEAT-010 |
| AD-003 | Two-layer LLM portability (Semantic Layer + Rendering Layer) | HIGH | FEAT-012 |
| AD-004 | Three-layer authorization (structural + dynamic + retrospective) | HIGH | FEAT-015 |
| AD-005 | MCP-primary tool integration with CLI/API fallback behind common adapter interface | HIGH | FEAT-014 |
| AD-006 | SARIF v2.1.0 as primary finding normalization format with 12-field common Finding schema | HIGH | FEAT-014 |
| AD-007 | YAML-first configurable rule sets with SonarQube-inspired profiles and ESLint-style cascading | HIGH | FEAT-013 |
| AD-008 | Five-layer SDLC governance (SSDF, MS SDL, SAMM, SLSA, DevSecOps) | HIGH | FEAT-010, FEAT-013 |
| AD-009 | STRIDE+DREAD default threat modeling with criticality-based escalation | HIGH | FEAT-010, FEAT-013 |
| AD-010 | Standalone capable design with three-level graceful degradation | HIGH | FEAT-014, FEAT-010 |
| AD-011 | Layered agent isolation (VM-per-engagement, container-per-group, sandbox-per-execution) | MEDIUM | FEAT-015 |
| AD-012 | Progressive autonomy deployment (AWS Scoping Matrix 4-level progression) | MEDIUM | FEAT-015 |

### Methodology Decisions (from B-003, B-004)

| Decision | Detail | Source |
|----------|--------|--------|
| Defensive standards stack | OWASP for application (eng-backend, eng-frontend), NIST for governance (eng-architect, eng-lead), CIS for infrastructure (eng-infra), CWE/SANS for weakness-aware development (all) | B-003 |
| OWASP ASVS 5.0 as primary verification standard | ~350 requirements across 17 chapters; 3-level assurance model as natural configuration axis | B-003 |
| STRIDE as primary threat identification | Systematic, property-based mapping; well-suited for agentic automation | B-004 |
| DREAD as primary risk scoring | 5-dimension scoring; subjectivity mitigated in agentic context through consistent rubrics | B-004 |
| Criticality-based methodology escalation | C1: STRIDE only; C2: +DREAD; C3: +Attack Trees; C4: +PASTA stages 4-7 | B-004 |
| LINDDUN for privacy-regulated applications | Invoked when system processes PII subject to GDPR, HIPAA, CCPA | B-004 |
| Offensive methodology: PTES/OSSTMM with ATT&CK mapping | PTES 7-phase structure as engagement workflow; OSSTMM for channel-based assessment; ATT&CK for technique taxonomy | B-001, B-002 |

### Tool Integration Decisions (from C-003)

| Decision | Detail | Source |
|----------|--------|--------|
| MCP as primary integration protocol | 97M+ monthly SDK downloads; 13,000+ servers; backed by major providers; security-specific servers validated | C-003 |
| Common adapter interface | `execute(params) -> StructuredResult \| ToolUnavailableError` for all adapter types | C-003 |
| SARIF v2.1.0 for finding normalization | OASIS standard; supported by CodeQL, Semgrep, Nuclei, Trivy, Checkmarx; 12-field common Finding schema | C-003 |
| Standalone capable design | Three-level degradation: full tools, partial tools, standalone; tools augment, not enable | C-003 |
| Security controls at adapter layer | Command allowlists (no shell=True), subprocess sandboxing, credential broker, output validation, size limits | C-003 |
| Implementation priority | P0: adapter interface + standalone; P1: SARIF + CLI adapters (Nmap, Semgrep, Trivy, Nuclei); P2: MCP evaluation + API; P3: custom MCP servers | C-003 |

### Portability Decisions (from E-003)

| Decision | Detail | Source |
|----------|--------|--------|
| Two-layer architecture | Semantic Layer (agent definitions in YAML + markdown) + Rendering Layer (provider adapter YAML configs) | E-003 |
| Markdown body as portable default | New agents use markdown body; XML is Anthropic-specific optimization | E-001, E-003 |
| JSON Schema as universal format | All tool definitions and output schemas use JSON Schema; all 4 providers and all 8 frameworks converge | E-001, E-002, E-003 |
| Adaptive reasoning strategy | Default to adaptive; inject CoT only for models that benefit; omit for frontier models | E-001, E-003 |
| LiteLLM for open-source models | Delegates chat template handling for 100+ models | E-002, E-003 |
| Model preferences as ordered fallbacks | Haystack FallbackChatGenerator pattern; minimum two providers per agent | E-003 |
| Backward compatible migration | Existing 37 Jerry agents work unchanged; `portability.enabled` defaults to false; 4-phase migration path | E-003 |
| 18 portability validation criteria | PV-001 through PV-018: 10 static, 6 behavioral, 2 regression; weighted composite >= 0.85 on all target providers | E-003 |

### Authorization Decisions (from F-002)

| Decision | Detail | Source |
|----------|--------|--------|
| Three-layer authorization architecture | Pre-engagement structural + runtime dynamic + post-execution retrospective | F-002 |
| Scope oracle as separate trust domain | Independent service; agents cannot modify, bypass, or disable scope enforcement | F-002 |
| Default-deny tool access | Tools explicitly granted per engagement scope; accessed through scope-validating proxy | F-002 |
| Per-agent authorization levels | 11 /red-team agents with distinct tool access, network scope, and data access constraints | F-002 |
| Ephemeral credential model | Time-bounded, scope-bounded, broker-mediated credentials; agents never see raw credentials | F-002 |
| Tamper-evident audit trail | Hash-chained or signed entries; append-only for agents; read-only for red-reporter | F-002 |
| Circuit breakers at phase transitions | Scope revalidation at every kill-chain transition; cascading failure detection | F-002 |
| Progressive autonomy deployment | AWS Scoping Matrix: prescribed -> monitored -> supervised -> full agency | F-002 |
| OWASP Agentic AI Top 10 coverage | All 10 risks (ASI01-ASI10) addressed with specific mitigation components | F-002 |
| Four-layer guardrail architecture | L1 Constitutional + L2 Policy + L3 Behavioral + L4 Output | F-002 |

### Rule Set Decisions (from F-003)

| Decision | Detail | Source |
|----------|--------|--------|
| YAML-first rule definition | Semgrep-inspired structured schema: id, category, severity, description, rationale, references, configurable_params | F-003 |
| Python escape hatch | Checkov dual-format pattern for complex rules requiring multi-step validation or dynamic computation | F-003 |
| SonarQube-inspired profile management | Extension/inheritance, per-engagement assignment, organizational hierarchy | F-003 |
| ESLint-style cascading overrides | 5-layer cascade: skill defaults -> org profile -> team/project profile -> engagement overrides -> runtime flags | F-003 |
| Standard rule schema | Shared schema for both /eng-team and /red-team rules | F-003 |
| OPA/Rego patterns for scope enforcement | Policy evaluation decoupled from enforcement; structured input/output; used internally with YAML surface | F-003 |
| /eng-team default rule sets | OWASP ASVS 5.0 (L1/L2/L3), OWASP Top 10 2025, CWE Top 25 2025, CIS Benchmarks, NIST SSDF | B-003, F-003 |
| /red-team default rule sets | MITRE ATT&CK (14 tactics), PTES (7 phases), OSSTMM (5 channels), OWASP Testing Guide | F-003 |
| Git-based rule versioning | Rules version-controlled; engagements pin to specific versions | F-003 |
| Rule testing framework | Positive/negative/parameter variation tests following Semgrep, OPA, ESLint patterns | F-003 |

---

## Phase 2 Readiness Assessment

For each of the 6 Phase 2 features, an assessment of research evidence, decisions already made, open questions, and readiness status.

### FEAT-010: Agent Team Architecture

**Research Evidence:**
- Final 21-agent roster with capability boundaries, ATT&CK coverage proof, and deferred agent rationale (A-004)
- Agent-to-standards mapping for all /eng-team agents (B-003)
- Agent-to-SDLC-phase mapping for all agents (F-001)
- Portable agent identity schema with 38 fields classified by portability (E-003)
- Multi-agent architecture validated by Wiz AI Cyber Model Arena (D-002)
- Agent capability boundary definitions for all 21 agents (S-002)
- Inter-agent handoff protocol requirements: sequential for /eng-team, non-linear for /red-team (S-002)
- Agent-to-tool category mapping for all 21 agents (S-002)

**Decisions Already Made:**
- AD-001 (methodology-first), AD-002 (21-agent roster), AD-008 (layered SDLC), AD-009 (STRIDE+DREAD), AD-010 (standalone capable)
- All roster decisions: additions, scope modifications, deferrals, integration points
- Defense Evasion distributed ownership model

**Open Questions:**
- OQ-002: Impact (TA0040) ownership split between red-exploit and red-reporter is MEDIUM confidence; validate during Phase 5
- OQ-003: Cross-skill deployment independence -- whether /eng-team must support standalone deployment without /red-team

**Readiness Status: READY**

All agent definitions, boundaries, handoff protocols, and workflow patterns are specified. Open questions do not block agent definition authoring.

---

### FEAT-011: Skill Routing and Invocation Architecture

**Research Evidence:**
- /eng-team 8-step sequential workflow (F-001)
- /red-team non-linear kill chain with phase cycling support (A-004)
- Keyword trigger maps for all 21 agents (S-002)
- Routing decision table with 12 routing scenarios (S-002)
- 5 multi-agent workflow patterns: sequential, non-linear, parallel, purple team, conditional (S-002)
- Safety alignment compatibility routing for /red-team requests (D-002)
- Standards-based routing context (B-003)

**Decisions Already Made:**
- /eng-team follows sequential phase-gate workflow; /red-team follows non-linear kill chain
- Purple team cross-skill routing activates 4 integration points
- Safety alignment conflicts reframed through professional methodology (PTES/OWASP/NIST)
- Circuit breaker check at every /red-team phase transition

**Open Questions:**
- No blocking open questions for routing architecture design

**Readiness Status: READY**

All routing tables, workflow patterns, and decision logic are specified.

---

### FEAT-012: LLM Portability Architecture

**Research Evidence:**
- Two-layer architecture design with 4 provider adapter specifications (E-003)
- Portable agent definition schema: 38 fields with portability classification (63% portable, 24% adaptation, 13% non-portable) (E-003)
- RCCF prompt pattern as maximally portable system prompt structure (E-001)
- JSON Schema as universal tool/output definition format (E-001, E-002)
- 18 portability validation criteria PV-001 through PV-018 (E-003)
- LiteLLM for open-source model support (E-002)
- Backward compatibility guarantees and 4-phase migration path (E-003)
- Industry convergence on agent-as-configuration from CrewAI, LangChain, Google ADK (E-002)

**Decisions Already Made:**
- AD-003 (two-layer architecture), markdown body as portable default, JSON Schema as universal format
- Adaptive reasoning strategy, LiteLLM for open-source, model preferences as ordered fallbacks
- Backward compatible design; 4-phase migration; 18 validation criteria

**Open Questions:**
- OQ-005: Structured output enforcement for open-source models -- whether 3-retry-then-raw-output is acceptable for security-critical structured outputs

**Readiness Status: READY WITH CAVEATS**

Architecture is fully specified. OQ-005 may affect open-source adapter design but does not block Anthropic/OpenAI/Google adapter work.

---

### FEAT-013: Configurable Rule Set Architecture

**Research Evidence:**
- YAML-first rule definition format with Semgrep-inspired schema (F-003)
- SonarQube-inspired profile management with inheritance (F-003)
- ESLint-style 5-layer cascading override mechanism (F-003)
- Checkov dual-format pattern (YAML primary, Python escape hatch) (F-003)
- Standard rule schema shared by /eng-team and /red-team (F-003)
- OPA/Rego patterns for /red-team scope enforcement policies (F-003)
- /eng-team default rule sets mapped to OWASP ASVS, CWE Top 25, CIS, NIST SSDF (B-003, F-003)
- /red-team default rule sets mapped to ATT&CK, PTES, OSSTMM (F-003)
- Rule testing framework patterns from Semgrep, OPA, ESLint (F-003)

**Decisions Already Made:**
- AD-007 (YAML-first with profiles and cascading), standard rule schema, dual-format authoring
- Default rule sets for both skills, git-based versioning, rule testing framework
- OPA/Rego architectural patterns for scope enforcement

**Open Questions:**
- No blocking open questions for rule set architecture design

**Readiness Status: READY**

Architecture is fully specified with clear implementation patterns from five analyzed systems.

---

### FEAT-014: Tool Integration Adapter Architecture

**Research Evidence:**
- MCP as primary integration protocol with adoption data (97M+ SDK downloads, 13,000+ servers) (C-003)
- Three adapter patterns: MCP server, CLI adapter, API adapter (C-003)
- Common adapter interface: `execute(params) -> StructuredResult | ToolUnavailableError` (C-003)
- SARIF-based finding normalization with 12-field common Finding schema (C-003)
- Standalone capable design with 3-level degradation (C-003)
- Security controls: command allowlists, subprocess sandboxing, credential broker, output validation (C-003)
- Implementation priority (P0-P3) with specific tool assignments (C-003)
- Offensive tool ecosystem survey: Nmap, Metasploit, Burp Suite, Nuclei, BloodHound (C-001)
- Defensive tool ecosystem survey: Semgrep, CodeQL, Trivy, Checkov, ZAP (C-002)
- Existing security MCP servers: mcp-for-security, pentest-mcp, hexstrike-ai, sast-mcp (C-003)

**Decisions Already Made:**
- AD-005 (MCP-primary with fallbacks), AD-006 (SARIF normalization), AD-010 (standalone capable)
- Common adapter interface design, security controls at adapter layer
- Implementation priority ordering (P0-P3)

**Open Questions:**
- No blocking open questions for adapter architecture design

**Readiness Status: READY**

Architecture is fully specified with clear protocol hierarchy, interface design, and implementation priority.

---

### FEAT-015: Authorization and Scope Control Architecture

**Research Evidence:**
- Three-layer authorization architecture (F-002)
- OWASP Agentic AI Top 10 risk-to-mitigation mapping (F-002)
- Per-agent authorization model for all 11 /red-team agents (F-002)
- 7 scope enforcement components: Scope Document Store, Scope Oracle, Tool Proxy, Network Enforcer, Audit Logger, Evidence Vault, Circuit Breaker (F-002)
- Progressive autonomy deployment via AWS Scoping Matrix (F-002)
- Production tool patterns from XBOW and PentAGI (F-002)
- Four-layer guardrail architecture (L1-L4) (F-002)
- OPA/Rego patterns for scope enforcement policies (F-003)

**Decisions Already Made:**
- AD-004 (three-layer authorization), AD-011 (layered isolation), AD-012 (progressive autonomy)
- Scope oracle as separate trust domain, default-deny tool access, ephemeral credentials
- Tamper-evident audit trail, circuit breakers at phase transitions
- Per-agent authorization levels for all 11 agents

**Open Questions:**
- OQ-001: Agent isolation granularity (container-per-agent vs. container-per-phase) -- performance trade-offs require Phase 2 analysis
- OQ-004: Scope document signing mechanism (HMAC vs. PKI) -- usability vs. security trade-off
- OQ-006: Circuit breaker threshold configuration -- specific thresholds for alerting vs. pausing vs. halting

**Readiness Status: READY WITH CAVEATS**

Core authorization architecture is fully specified. Three open questions affect implementation details but do not block the ADR or high-level design work. OQ-001 and OQ-004 require design trade-off analysis during Phase 2; OQ-006 can be deferred to implementation.

---

### Readiness Summary

| Feature | Status | Open Questions | Blocking Issues |
|---------|--------|:--------------:|:---------------:|
| FEAT-010: Agent Team Architecture | READY | OQ-002, OQ-003 | None |
| FEAT-011: Skill Routing and Invocation | READY | None | None |
| FEAT-012: LLM Portability | READY WITH CAVEATS | OQ-005 | None (affects open-source adapter only) |
| FEAT-013: Configurable Rule Sets | READY | None | None |
| FEAT-014: Tool Integration Adapters | READY | None | None |
| FEAT-015: Authorization and Scope Control | READY WITH CAVEATS | OQ-001, OQ-004, OQ-006 | None (implementation details) |

**Phase 2 can begin immediately.** No feature is BLOCKED. All 12 architecture decisions provide sufficient specification input for ADR authoring. Open questions affect implementation details, not architectural direction.

---

## Requirement Fulfillment Matrix

Coverage status of all 24 PLAN.md requirements based on Phase 1 research.

| Req | Name | Coverage | Evidence References | Completion Phase |
|-----|------|----------|--------------------:|-----------------|
| R-001 | Secure by Design | FULLY COVERED | B-003, B-004, F-001, S-001 Convergence 2 | Phase 2 (ADRs formalize) |
| R-002 | Architecturally Pure | FULLY COVERED | C-003, E-003, S-002 cross-cutting concerns | Phase 2 (architecture design) |
| R-003 | No Slop Code | FULLY COVERED | B-003 (CWE Top 25), D-002 (hallucination mitigation) | Phase 3/4 (implementation) |
| R-004 | No Shortcuts | FULLY COVERED | F-001 (layered SDLC), F-002 (scope enforcement) | All phases (process) |
| R-005 | Grounded in Reality | FULLY COVERED | D-002 (LLM boundaries), S-001 Convergence 1 (methodology-first) | All phases (principle) |
| R-006 | Evidence-Driven Decisions | FULLY COVERED | D-003 (130+ sources across 6 categories), all 20 artifacts with Evidence sections | Phase 1 (complete) |
| R-007 | Persistent Research Artifacts | FULLY COVERED | 23 artifacts persisted to `work/research/` | Phase 1 (complete) |
| R-008 | Role Completeness Analysis | FULLY COVERED | A-001, A-002, A-003, A-004 (gap analysis against 7+ elite organizations) | Phase 1 (complete) |
| R-009 | Current Intelligence | FULLY COVERED | Context7 + WebSearch across all streams; sources dated 2024-2026 | Phase 1 (complete) |
| R-010 | LLM Portability | FULLY COVERED | E-001, E-002, E-003 (two-layer architecture, 18 validation criteria) | Phase 2 (architecture), Phase 5 (validation) |
| R-011 | Configurable Rule Sets | FULLY COVERED | F-003, B-003 (YAML-first, profiles, cascading, defaults) | Phase 2 (architecture), Phase 3/4 (implementation) |
| R-012 | Tool Integration Architecture | FULLY COVERED | C-001, C-002, C-003 (MCP, adapters, SARIF, standalone) | Phase 2 (architecture), Phase 4 (implementation) |
| R-013 | C4 /adversary on Every Phase | PARTIALLY COVERED | B-003, F-001, S-002 (quality gate integration points defined) | Phase 2-6 (operationalized per phase) |
| R-014 | Full /orchestration Planning | PARTIALLY COVERED | F-001 (SDLC phase mapping), S-002 (workflow patterns) | Phase 2 (orchestration plan formalized) |
| R-015 | Detailed /worktracker | FULLY COVERED | All 20+ artifacts tracked; WORKTRACKER.md maintained | All phases (continuous) |
| R-016 | Challenge Weak Specifications | FULLY COVERED | A-004 (challenged PLAN.md roster gaps), D-002 (challenged execution assumptions) | Phase 1 (complete) |
| R-017 | Industry Leader Standard | FULLY COVERED | Validated against 7+ elite organizations; D-003 (6 differentiation opportunities) | All phases (standard) |
| R-018 | Real Offensive Techniques | FULLY COVERED | A-003, A-004 (14/14 ATT&CK coverage), B-001, B-002 (PTES/OSSTMM/ATT&CK) | Phase 4 (implementation) |
| R-019 | Secure SDLC Practices | FULLY COVERED | B-003, F-001 (OWASP ASVS, NIST SSDF, CIS, CWE mapped to agents) | Phase 3 (implementation) |
| R-020 | Authorization Verification | FULLY COVERED | F-002 (three-layer architecture, scope oracle, default-deny, audit trail) | Phase 2 (architecture), Phase 4 (implementation) |
| R-021 | Actionable Remediation | FULLY COVERED | A-004 (red-reporter generates remediation), D-002 (LLM report generation validated as HIGH capability) | Phase 4 (implementation) |
| R-022 | Agent Development Standards | FULLY COVERED | E-003 (portable agent schema, 38 fields), S-002 (agent identity schema) | Phase 2 (architecture), Phase 3/4 (implementation) |
| R-023 | Persist All Outputs | FULLY COVERED | C-003 (filesystem-as-memory), F-002 (evidence vault) | Phase 3/4 (implementation) |
| R-024 | /adversary Integration | FULLY COVERED | A-004, B-003, F-001, S-002 (eng-reviewer as final gate, quality gate integration) | Phase 3/4 (implementation) |

**Summary:** 22 of 24 requirements are FULLY COVERED by Phase 1 research. 2 requirements (R-013, R-014) are PARTIALLY COVERED because they describe process requirements that are operationalized across all phases -- the research foundation is complete, but ongoing execution is required. No requirement is NOT YET ADDRESSED.

---

## Risk Register

Top risks identified during Phase 1 research, ordered by risk severity (likelihood x impact).

| Risk ID | Description | Likelihood | Impact | Severity | Mitigation Strategy | Source |
|---------|-------------|:----------:|:------:|:--------:|---------------------|--------|
| RISK-001 | **LLM Hallucination in Security Outputs.** LLMs fabricate CVEs, generate plausible-but-incorrect vulnerability reports, and produce exploit code with subtle errors. Over 40% of AI-generated code contains security flaws. NVD backlog worsened by AI-generated false CVE submissions. | HIGH | HIGH | CRITICAL | AD-001 methodology-first design: provide guidance and verification instructions, not findings. Structured templates with explicit "verify by" instructions. Confidence indicators on all outputs. Never present AI-generated findings as ground truth. | D-002 |
| RISK-002 | **Safety Alignment Restricts Red Team Utility.** Commercial LLM compliance with cyber attack assistance decreased from 52% to 28%. Models refuse direct exploit code generation, attack automation, and malware creation. | HIGH | MEDIUM | HIGH | AD-001 methodology-first design inherently avoids safety filter triggers. All /red-team guidance framed within PTES/OWASP/NIST professional methodology. Skills guide practitioners to use established exploitation frameworks, not generate exploits directly. Conflict resolution 5 in S-001 validates this approach. | D-002 |
| RISK-003 | **Authorization Scope Bypass.** Agent actions outside defined engagement scope could create legal liability. Unauthorized testing is illegal regardless of intent. | LOW | CRITICAL | HIGH | AD-004 three-layer authorization architecture makes out-of-scope actions structurally impossible. Scope oracle as separate trust domain. Default-deny tool access. Network-level enforcement. Tamper-evident audit trail. Progressive autonomy deployment starting at prescribed agency. | F-002 |
| RISK-004 | **LLM Portability Degradation.** Cross-provider agent quality may degrade below acceptable thresholds, particularly for structured output and reasoning-heavy tasks on non-frontier models. | MEDIUM | MEDIUM | MEDIUM | AD-003 two-layer architecture with 63% portable fields. 18 validation criteria (PV-001 through PV-018) with behavioral threshold >= 0.85. Adaptive reasoning strategy. Model preferences as ordered fallback lists. Backward compatible design preserves Anthropic-optimized performance. | E-003 |
| RISK-005 | **Scope Creep from 21-Agent Roster.** 21 agents (up from 17 baseline) increases skill routing complexity, definition authoring effort, and testing surface. Four deferred agents create pressure for further expansion. | MEDIUM | MEDIUM | MEDIUM | Roster expansion justified by evidence (ATT&CK coverage gaps, organizational patterns). Four deferred agents have specific reconsideration triggers preventing ad-hoc addition. Non-overlapping capability boundaries minimize routing ambiguity. Kill chain organizes capability without requiring all agents active simultaneously. | A-004 |
| RISK-006 | **Tool Integration Ecosystem Fragmentation.** MCP is nascent; security tool MCP servers are limited. CLI adapters require per-tool maintenance. Tool output formats vary. | MEDIUM | MEDIUM | MEDIUM | AD-005 protocol hierarchy (MCP primary, CLI fallback, API fallback) behind common adapter interface abstracts fragmentation. AD-010 standalone capable design ensures agents function without any tools. SARIF normalization (AD-006) standardizes outputs regardless of source. Implementation priority (P0-P3) focuses effort on highest-ROI integrations. | C-003 |
| RISK-007 | **Configurable Rule Set Complexity.** 5-layer cascading overrides, dual-format authoring, and profile inheritance create configuration debugging challenges. | LOW | MEDIUM | MEDIUM | Sensible defaults reduce configuration need for most users. Profile management follows well-understood SonarQube pattern. YAML-first format is human-readable. Rule testing framework validates configurations. Git-based versioning provides configuration audit trail. | F-003 |
| RISK-008 | **Cross-Skill Deployment Independence.** If /eng-team deploys without /red-team, the threat intelligence integration point (red-recon -> eng-architect) is unavailable, leaving a methodology gap. | LOW | MEDIUM | LOW | OQ-003 flagged for Phase 2 resolution. If independent deployment is common, eng-threatintel should be reconsidered. Cross-skill integration is an optimization, not a dependency -- /eng-team operates fully without /red-team using standards-based threat modeling. | A-004, S-001 Conflict 3 |
| RISK-009 | **Agent Isolation Performance Overhead.** Layered isolation (VM/container/sandbox per AD-011) introduces latency for inter-agent communication and tool execution. | MEDIUM | LOW | LOW | OQ-001 flagged for Phase 2 performance analysis. Container-per-agent-group (not per-agent) reduces overhead. PentAGI and XBOW production deployments validate containerized execution viability. Granularity tunable based on Phase 2 findings. | F-002, S-002 |
| RISK-010 | **Structured Output Reliability on Open-Source Models.** Open-source models lack server-side structured output enforcement; prompt-level schema instructions are best-effort. | MEDIUM | LOW | LOW | OQ-005 flagged for Phase 2 design. 3-retry strategy with format reminder. Fallback to raw output with validation errors. Open-source adapter can mandate Instructor or Outlines for constrained generation if needed. Primary providers (Anthropic, OpenAI, Google) have native structured output support. | E-003 |

---

## Source Authority Summary

Citation analysis across all 20 primary research artifacts, organized by R-006 required source categories.

### Citations by Category

| R-006 Category | Representative Sources | Stream Coverage |
|----------------|----------------------|-----------------|
| **Industry Leaders** | Microsoft (SDL, Security Copilot, Sentinel, MSRC), Google (Sec-Gemini, Big Sleep, Project Zero, Chrome Security, SecOps), CrowdStrike (Charlotte AI, Charlotte Agentic SOAR), Palo Alto Networks (Unit 42, AI insider threat reports), AWS (Agentic AI Security Scoping Matrix) | A, B, C, D, E, F |
| **Industry Experts** | SANS Institute (SEC598, SEC411, AI Summit), NIST (CSF 2.0, SP 800-53 Rev 5, SP 800-218 SSDF, IR 8596 Cyber AI Profile), CISA (AI Data Security Guidance, AI in OT Principles, Collaboration Playbook), CERT/CC, NVIDIA (agentic AI security) | A, B, D, F |
| **Industry Innovators** | SpecterOps (BloodHound, BloodHound MCP, Scentry), Rapid7 (Metasploit, agentic SOC, AttackerKB), Snyk (DeepCode AI, hybrid architecture, transitive reachability), TrustedSec (TRU research), Netflix (Attack Emulation Team) | A, C, D |
| **Community Leaders** | OWASP (Top 10 2025, ASVS 5.0, SAMM, Top 10 for Agentic Applications, Top 10 for LLM Applications, Securing Agentic Apps Guide, Testing Guide), CISA (community perspective), ISC2 (Workforce Study 2025, AI Security Certificate), MITRE (ATT&CK, CWE Top 25 2025) | A, B, D, F |
| **Community Experts** | HackerOne (AI vulnerability reports, bionic hackers, XBOW data), Hack the Box (AI vs Human CTF), Stanford ARTEMIS (bug bounty benchmark), Black Hat/RSAC conference research, academic papers (CyberSecEval 3, HarmBench, Wiz AI Cyber Model Arena) | D |
| **Community Innovators** | ProjectDiscovery (Nuclei, AI templates), Metasploit community (MCP server), HexStrike AI (150+ tool MCP), PentAGI/PentestAgent (multi-agent pentest), Strix (autonomous AI agents), CAI (Cybersecurity AI), FastMCP, CrewAI, LangChain, DSPy, Google ADK, Haystack, LiteLLM | C, D, E |

### Coverage Summary

| Metric | Value |
|--------|-------|
| Total unique sources | 130+ |
| R-006 categories covered | 6 of 6 |
| Source date range | 2024-2026 |
| Streams with Evidence sections | 20 of 20 primary artifacts |
| Industry Leader sources | Microsoft, Google, CrowdStrike, Palo Alto Networks, AWS |
| Community Leader sources | OWASP, MITRE, CISA, ISC2 |
| Standards bodies cited | OWASP, NIST, CIS, SANS, MITRE, OASIS, ISO |
| Academic benchmarks cited | CyberSecEval 3, HarmBench, Wiz AI Cyber Model Arena, HTB CTF, Stanford ARTEMIS |

All six R-006 categories have substantive representation across multiple research streams. No category depends on a single stream for coverage. Source dates span 2024-2026, with the majority from 2025-2026, satisfying R-009 (Current Intelligence).

---

## Research Artifact Index

Complete directory listing of all Phase 1 research artifacts with paths relative to `work/research/`.

```
work/research/
|
+-- stream-a-role-completeness/
|   +-- A-001-elite-engineering-teams.md
|   +-- A-002-red-team-pentest-firms.md
|   +-- A-003-mitre-attack-coverage.md
|   +-- A-004-roster-recommendation.md
|
+-- stream-b-methodology/
|   +-- B-001-mitre-attack-framework.md
|   +-- B-002-ptes-osstmm-methodology.md
|   +-- B-003-owasp-nist-cis-sans.md
|   +-- B-004-threat-modeling-comparison.md
|
+-- stream-c-tool-integration/
|   +-- C-001-offensive-tools.md
|   +-- C-002-defensive-tools.md
|   +-- C-003-agentic-integration-patterns.md
|
+-- stream-d-prior-art/
|   +-- D-001-prior-art-survey.md
|   +-- D-002-llm-capability-boundaries.md
|   +-- D-003-industry-perspectives.md
|
+-- stream-e-llm-portability/
|   +-- E-001-universal-prompt-patterns.md
|   +-- E-002-multi-llm-frameworks.md
|   +-- E-003-portability-architecture-recommendation.md
|
+-- stream-f-secure-sdlc/
|   +-- F-001-secure-sdlc-patterns.md
|   +-- F-002-security-architecture-patterns.md
|   +-- F-003-configurable-rule-sets.md
|
+-- synthesis/
    +-- S-001-cross-stream-findings.md
    +-- S-002-architecture-implications.md
    +-- S-003-research-compendium.md          <-- this document
```

**Stream Summary:**

| Stream | Focus | Artifacts | Total Lines |
|--------|-------|:---------:|------------:|
| A: Role Completeness | Agent roster validation against industry | 4 | 1,339 |
| B: Methodology | Standards and threat modeling selection | 4 | 1,460 |
| C: Tool Integration | Tool ecosystem and integration architecture | 3 | 1,650 |
| D: Prior Art | LLM boundaries, industry perspectives, prior art | 3 | 1,247 |
| E: LLM Portability | Cross-provider architecture and patterns | 3 | 1,648 |
| F: Secure SDLC | SDLC models, authorization, rule sets | 3 | 1,301 |
| Synthesis | Cross-stream consolidation and architecture | 3 | 1,218+ |
| **Total** | | **23** | **9,863+** |
