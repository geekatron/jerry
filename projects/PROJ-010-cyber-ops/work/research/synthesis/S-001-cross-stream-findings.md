# S-001: Cross-Stream Findings Consolidation

> Synthesis | PROJ-010 Cyber Ops | Phase 1 Research

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | Major cross-stream conclusions for Phase 2 |
| [L1: Consolidated Findings by Theme](#l1-consolidated-findings-by-theme) | Definitive findings organized by architectural theme |
| [L2: Cross-Stream Convergence Analysis](#l2-cross-stream-convergence-analysis) | Where independent streams arrived at the same conclusions |
| [L2: Cross-Stream Conflicts and Resolutions](#l2-cross-stream-conflicts-and-resolutions) | Conflicts between streams with documented resolution |
| [Requirements Traceability](#requirements-traceability) | Findings mapped to R-001 through R-024 |
| [Phase 2 Input Summary](#phase-2-input-summary) | Specific findings feeding each FEAT-010 through FEAT-015 |

---

## L0: Executive Summary

Phase 1 research across 6 streams and 20 artifacts produces a definitive foundation for PROJ-010's architecture phase. The combined agent roster of 21 agents (10 /eng-team, 11 /red-team) achieves 14/14 MITRE ATT&CK tactic coverage while maintaining manageable skill routing complexity, validated by gap analysis against Google, Microsoft, CrowdStrike, Mandiant, TrustedSec, SpecterOps, and Rapid7 team structures. The methodology framework layers NIST SSDF as governance backbone, Microsoft SDL phases as workflow structure, OWASP ASVS/SAMM for verification and maturity assessment, STRIDE+DREAD as the default threat modeling methodology, and CIS Benchmarks for infrastructure hardening -- each framework assigned to its area of strength to avoid overlap or conflict. Tool integration adopts MCP as the primary protocol with CLI and API adapter fallbacks, SARIF-based finding normalization, and a strict "standalone capable" design where all 21 agents function without any external tools. LLM portability is achieved through a two-layer architecture separating semantic agent intent from provider-specific rendering, using YAML configuration rather than compiled adapter code, with 63% of agent definition fields fully portable across Anthropic, OpenAI, Google, and open-source providers. Authorization and scope control for /red-team implements a three-layer architecture (pre-engagement structural authorization, runtime scope enforcement via scope oracle, post-execution audit verification) grounded in the OWASP Top 10 for Agentic Applications risk taxonomy and validated by production tool patterns from XBOW and PentAGI. Configurable rule sets adopt a YAML-first rule definition format with SonarQube-inspired profile management, cascading overrides, and comprehensive default rule sets mapped to OWASP ASVS, CWE Top 25, MITRE ATT&CK, and PTES. The single most critical cross-stream finding is that LLMs excel at methodology guidance, structured reasoning, and report generation but fundamentally cannot replace tool execution or human judgment for novel discovery -- validating PROJ-010's design as a methodology-guidance framework with tool augmentation, not an autonomous execution engine.

---

## L1: Consolidated Findings by Theme

### Agent Team Design

**Final Roster: 21 agents (10 /eng-team + 11 /red-team)**

The /eng-team roster grows from the PLAN.md baseline of 8 to 10 agents with the addition of eng-devsecops and eng-incident. eng-devsecops absorbs automated security tooling responsibilities (SAST/DAST pipeline, CI/CD security, secrets scanning, container scanning) from the overloaded eng-security agent, which narrows to manual secure code review and security requirements verification. eng-incident fills the post-deployment gap identified at Mandiant, Google Chrome, and Microsoft MSRC -- the team can now build, review, and respond. eng-infra gains explicit supply chain security scope (SBOM generation, dependency provenance, build reproducibility). Two agents are deferred: eng-threatintel (covered by cross-skill integration with red-recon) and eng-compliance (better served by configurable rule sets per R-011).

The /red-team roster grows from 9 to 11 agents with the addition of red-infra and red-social. red-infra is the highest-confidence addition across both rosters -- three independent evidence streams converge: organizational evidence (4 of 7 elite organizations staff dedicated tool development), ATT&CK coverage (Resource Development TA0042 had zero coverage), and C2 architecture (TA0011 was weak coverage). red-social closes the human attack vector gap, covering social reconnaissance techniques (T1591, T1597, T1598) and phishing as the most common real-world initial access vector. Defense Evasion (TA0005, the largest ATT&CK tactic with 43 techniques and 112 sub-techniques) is distributed across all operational agents with red-infra as tool-level evasion owner, following industry practice where evasion is embedded tradecraft rather than a standalone function. Two agents are deferred: red-opsec (decomposes into red-infra + red-lead scope expansion) and red-cloud (explicitly out of scope per PLAN.md).

**Cross-Skill Integration Points:**
Four purple team integration points operationalize the PLAN.md requirement that "the two skills work as adversaries": (1) Threat-Informed Architecture (red-recon feeds adversary TTPs to eng-architect for threat modeling), (2) Attack Surface Validation (red-recon/red-vuln test what eng-infra/eng-devsecops hardened), (3) Secure Code vs. Exploitation (red-exploit/red-privesc attack what eng-security reviewed and eng-backend/eng-frontend built), (4) Incident Response Validation (red-persist/red-lateral/red-exfil exercise eng-incident's runbooks).

**Workflow Design:**
The /red-team workflow must support non-linear kill chain iteration. Real engagements are iterative -- exploitation discovers new recon targets, triggering return to earlier phases. The kill chain organizes capability, not workflow sequence. Agents must be invocable in any order with explicit support for cycling between phases.

| Source | Finding |
|--------|---------|
| A-004 | Final roster decisions, ATT&CK coverage proof, integration points |
| A-001 | Elite engineering team structures (Google, Microsoft, CrowdStrike, Mandiant) |
| A-002 | Red team/pentest firm patterns (TrustedSec, SpecterOps, Rapid7, Netflix) |
| A-003 | MITRE ATT&CK 14-tactic coverage analysis |

---

### Methodology Framework

**Layered SDLC Model Architecture:**
Five secure SDLC models serve distinct, non-overlapping purposes:

| Layer | Model | Purpose | Primary Agents |
|-------|-------|---------|----------------|
| Governance | NIST SP 800-218 SSDF | Compliance framework, practice requirements | eng-lead, eng-architect |
| Lifecycle | Microsoft SDL (5 phases) | Workflow structure, phase-gate model | All /eng-team agents |
| Assessment | OWASP SAMM (3 maturity levels) | Maturity measurement, improvement tracking | eng-lead, eng-reviewer |
| Supply Chain | Google SLSA (4 build levels) | Build integrity, provenance | eng-infra, eng-devsecops |
| Automation | DevSecOps patterns | CI/CD pipeline security integration | eng-devsecops |

**Threat Modeling Default:**
STRIDE for threat identification + DREAD for risk scoring, with criticality-based methodology escalation: C1 uses STRIDE only, C2 adds DREAD scoring, C3 adds Attack Trees for complex attack path visualization, C4 adds PASTA stages 4-7 for business impact analysis. LINDDUN is invoked when the system processes PII subject to privacy regulations (GDPR, HIPAA, CCPA). The DREAD subjectivity concern is mitigated in the agentic context because eng-architect applies consistent scoring rubrics and /adversary integration validates scoring consistency.

**Defensive Standards Stack:**

| Layer | Standard | Purpose |
|-------|----------|---------|
| Awareness | OWASP Top 10 2025 | Security awareness baseline for all agents |
| Verification | OWASP ASVS 5.0 (3 levels) | Application security verification requirements (~350 requirements, 17 chapters) |
| Code Review | CWE Top 25 2025 | Primary weakness focus list for eng-security |
| Infrastructure | CIS Benchmarks (100+ guides) | Configuration hardening baseline for eng-infra |
| Governance | NIST CSF 2.0 (6 functions) | Top-level security governance for eng-architect |

**Offensive Methodology:**
/red-team engagements follow PTES, OSSTMM, or equivalent recognized frameworks with mandatory MITRE ATT&CK technique mapping. The final 11-agent roster achieves 14/14 ATT&CK tactic coverage at STRONG level.

| Source | Finding |
|--------|---------|
| B-003 | OWASP, NIST, CIS, SANS standards analysis and agent mapping |
| B-004 | STRIDE/DREAD/PASTA/LINDDUN/Attack Trees comparison and recommendation |
| F-001 | MS SDL, NIST SSDF, OWASP SAMM, Google SLSA, DevSecOps comparison |

---

### Tool Integration Architecture

**Integration Protocol Hierarchy:**
1. MCP servers (primary) -- Claude Code natively supports MCP; 13,000+ servers launched in 2025; security-specific MCP servers validated (mcp-for-security, pentest-mcp, hexstrike-ai, sast-mcp)
2. CLI adapters (fallback) -- subprocess execution with structured output parsing for tools without MCP servers
3. API adapters -- HTTP/RPC client for tools exposing REST/GraphQL APIs (SonarQube, Burp Suite, ZAP)

**Common Adapter Interface:**
All adapter types implement `execute(params) -> StructuredResult | ToolUnavailableError`. Agent code calls adapters, never tools directly. This abstraction enables tool substitution without agent changes.

**SARIF-Based Finding Normalization:**
SARIF v2.1.0 (OASIS standard) is the primary normalization format. All tool outputs are normalized to a common `Finding` schema (id, source_tool, severity, category, title, description, location, evidence, remediation, references, confidence, raw_data). This enables cross-tool finding correlation, severity-based prioritization regardless of source, and uniform reporting.

**Standalone Capable Design (R-012):**
Three-level graceful degradation: Level 0 (full tool access -- optimal), Level 1 (partial tools -- analysis with explicit uncertainty markers), Level 2 (no tools -- LLM-only analysis with "unvalidated" markers and manual verification guidance). Every agent capability works at Level 2 with reduced evidence quality. Tools augment; they do not enable.

**Security Controls:**
Command allowlists (no shell=True), subprocess sandboxing, credential broker pattern (agents never see raw credentials), output schema validation before agent consumption (prompt injection via tool output is a documented MCP attack vector), and output size limits to prevent context window exhaustion.

| Source | Finding |
|--------|---------|
| C-003 | MCP integration patterns, CLI/API adapter architecture, SARIF normalization, standalone design, security controls |

---

### LLM Portability

**Two-Layer Architecture:**

| Layer | Content | Authorship |
|-------|---------|------------|
| Semantic Layer | Agent definition files (YAML frontmatter + markdown body) -- what the agent is and does | Skill developers |
| Rendering Layer | Provider adapter YAML configs -- how to transform definitions into provider-specific prompts | Framework maintainers (once per provider) |

**Portability Classification:** 63% of agent definition fields are fully portable (identity, persona, guardrails, tool schemas, output schemas), 24% require adaptation (tool registration, model preferences, reasoning strategy), and 13% are non-portable provider-exclusive optimizations (extended thinking, grounding APIs, prompt caching).

**Key Design Decisions:**
- Markdown body format as the portable default for new agents (XML tags are Anthropic-specific optimization per E-001)
- JSON Schema as the universal tool/output definition format (all 4 major providers and all 8 frameworks analyzed converge on this)
- Adaptive reasoning strategy by default (explicit CoT degrades frontier model performance per 2025 research, but benefits smaller open-source models)
- LiteLLM delegates open-source chat template handling (5+ distinct formats; LiteLLM handles 100+ models, used by Google ADK and CrewAI)
- Model preferences as ordered fallback lists (Haystack FallbackChatGenerator pattern for operational resilience)
- Backward compatible: existing 37 Jerry agents work unchanged; `portability.enabled` defaults to false

**Portability Validation:** 18 testable criteria (PV-001 through PV-018): 10 static analysis tests (CI-runnable), 6 behavioral tests (require cross-provider invocation), 2 regression tests (backward compatibility). Behavioral validation target: weighted composite score >= 0.85 on all target providers (0.07 degradation allowance from primary provider threshold of 0.92).

| Source | Finding |
|--------|---------|
| E-003 | Two-layer architecture, provider adapter specs, validation criteria, migration path |
| E-001 | Universal prompt patterns (RCCF), XML anti-pattern, CoT model-dependence |
| E-002 | Framework analysis (CrewAI, LangChain, DSPy, Google ADK, Haystack, LiteLLM) |

---

### Authorization and Scope Control

**Three-Layer Authorization Architecture:**

| Layer | Type | Timing | Owner |
|-------|------|--------|-------|
| 1. Structural | Pre-engagement scope definition (signed YAML: target allowlist, technique allowlist, time window, exclusion list, RoE) | Before engagement | red-lead |
| 2. Dynamic | Runtime scope enforcement (scope oracle, tool proxy, network enforcer) -- every agent action intercepted and validated | During engagement | Scope enforcement infrastructure |
| 3. Retrospective | Post-execution audit verification (action log review, evidence verification, scope deviation detection, compliance report) | After engagement | red-reporter |

**Core Principle:** Authorization scope bounds risk more effectively than human oversight. An agent with properly constrained authorization scopes poses bounded risk regardless of autonomy level. Security is an architectural property, not an operational procedure.

**OWASP Agentic AI Top 10 Coverage:**
The architecture addresses all 10 risks (ASI01-ASI10), with highest priority on: ASI01 Agent Goal Hijack (immutable scope definitions loaded from signed engagement file), ASI02 Tool Misuse (default-deny tool access through scope-validating proxy), ASI03 Identity/Privilege Abuse (ephemeral, engagement-scoped credentials via credential broker), ASI08 Cascading Failures (circuit breakers at phase transitions with mandatory scope revalidation).

**Per-Agent Authorization Model:**
Each agent operates under distinct authorization levels: red-lead has full engagement scope, red-recon has reconnaissance-only scope, red-exploit has target+technique allowlist scope, red-privesc has compromised-host-only scope until lateral movement authorized, and so on. Default-deny tool access: tools are explicitly granted per engagement scope, not implicitly available.

**Scope Enforcement Components:**
Scope Document Store (immutable, signed), Scope Oracle (separate trust domain, evaluates actions against rules), Tool Proxy (intercepts all invocations), Network Enforcer (infrastructure-level fail-closed), Audit Logger (tamper-evident, append-only), Evidence Vault (chain-of-custody), Circuit Breaker (cascading failure detection).

**Progressive Autonomy Deployment:**
Following AWS Agentic AI Security Scoping Matrix: prescribed agency (human approves every action) -> monitored agency (human reviews logs in near-real-time) -> supervised agency (human reviews at phase boundaries) -> full agency (human reviews engagement summary).

| Source | Finding |
|--------|---------|
| F-002 | OWASP Agentic AI Top 10, layered authorization architecture, scope enforcement, isolation patterns, production tool analysis (XBOW, PentAGI) |

---

### Configurable Rule Sets

**Architecture: YAML-first with SonarQube-inspired profile management and ESLint-style cascading overrides.**

**Rule Definition Format:**
YAML as primary format (inspired by Semgrep's structured schema: id, category, severity, description, rationale, references, configurable_params). Python escape hatch for complex rules that YAML cannot express (multi-step validation, dynamic computation, cross-rule dependencies), following Checkov's dual-format pattern.

**Profile Management:**
1. Default profiles provided by each skill (e.g., "OWASP ASVS Level 2" for /eng-team, "PTES Standard" for /red-team)
2. Profile extension -- users inherit defaults and add/override rules without modifying originals (SonarQube inheritance model)
3. Per-engagement profile assignment -- different engagements use different profiles
4. Organizational profile hierarchy -- parent profiles for organizations, child profiles for teams

**Cascading Override Mechanism:**
```
1. Skill defaults (lowest priority)
2. Organization profile
3. Team/project profile
4. Engagement overrides
5. Runtime flags (highest priority)
```

**Default Rule Sets:**

| Skill | Default Rule Sets |
|-------|-------------------|
| /eng-team | OWASP ASVS 5.0 (L1/L2/L3), OWASP Top 10 2025, CWE Top 25 2025, CIS Benchmarks, NIST SSDF practices |
| /red-team | MITRE ATT&CK (14 tactics), PTES (7 phases), OSSTMM (5 channels), OWASP Testing Guide |

**Scope Enforcement Policies:**
/red-team scope enforcement uses OPA/Rego architectural patterns: policy evaluation decoupled from enforcement, structured input documents (proposed actions as JSON), policy decisions as structured output (allow/deny with reasons). The pattern is implemented architecturally, not necessarily requiring the OPA runtime.

| Source | Finding |
|--------|---------|
| F-003 | Semgrep YAML format, OPA/Rego patterns, SonarQube profiles, Checkov dual-format, ESLint flat config, rule schema |

---

### Quality and Compliance

**SDLC Governance:**
NIST SP 800-218 SSDF serves as the governance backbone. Its 4 practice groups (Prepare, Protect, Produce, Respond) map directly to /eng-team agent responsibilities without prescribing implementation methods. Every agent security activity should reference the SSDF practice ID it implements for traceability and audit compliance.

**Supply Chain Security:**
All five SDLC models converge on supply chain security as the critical emerging concern. The 2025 OWASP Top 10 introduced A03 Software Supply Chain Failures. Google SLSA Build L2 (hosted build with signed provenance) is the minimum for production releases; Build L3 (isolated environments) is required for C3/C4 engagements. eng-infra owns build platform, eng-devsecops owns provenance generation and signing.

**Maturity Assessment:**
OWASP SAMM provides quantitative maturity measurement across 15 security practices. Level 1 (ad-hoc) is the minimum baseline, Level 2 (defined/repeatable) is the standard target, Level 3 (optimized/measured) is for C4 mission-critical engagements. eng-lead uses SAMM to assess posture and track improvement.

**Quality Integration:**
All deliverables go through /adversary C4 review with >= 0.95 quality threshold per PLAN.md R-013. SDLC compliance is verified by eng-reviewer as the final gate. The /adversary skill's S-014 LLM-as-Judge scoring operates on agent outputs and is also used (via PV-015) to validate cross-provider output quality for portability.

| Source | Finding |
|--------|---------|
| F-001 | MS SDL evolution, SSDF governance, SAMM maturity, SLSA supply chain, DevSecOps automation |
| B-003 | Standards layering (OWASP, NIST, CIS, SANS) with agent mapping |

---

### LLM Capability Boundaries

**What LLMs Reliably Do (HIGH confidence for PROJ-010):**
- Methodology guidance and knowledge retrieval -- core PROJ-010 value
- Code vulnerability pattern detection (with tool augmentation: IRIS+GPT-4 detected 2x more than CodeQL alone)
- Threat intelligence synthesis (7x analyst time reduction with Sec-Gemini)
- Security report generation and structuring
- Configuration analysis against best practices
- Risk prioritization and threat modeling facilitation

**What LLMs Struggle With (MEDIUM -- require tool augmentation):**
- Novel exploit development (~0% success on refactored code; CVE-Genie reproduces only 51% of known CVEs)
- Runtime analysis and dynamic testing (fundamental limitation: cannot interact with running systems)
- Multi-step attack chains (effectiveness decreases, cost increases 2-2.5x moving from directed to broad-scope)
- Binary exploitation (requires extensive scaffolding per PwnGPT benchmark)

**What LLMs Cannot Do (fundamental limitations):**
- True zero-day discovery in the wild without specialized infrastructure
- Adaptive adversary simulation requiring persistent state
- Physical security assessment
- Legal and compliance judgment (authorization decisions, disclosure decisions)

**Dominant Failure Mode: Hallucination.**
LLMs fabricate CVEs, generate plausible-but-incorrect vulnerability reports, and produce exploit code with subtle errors. Over 40% of AI-generated code contains security flaws. Open-source maintainers report ~2 AI-generated false security reports per week. The NVD backlog crisis was worsened by AI-generated false CVE submissions.

**Mitigation Strategy:**
PROJ-010 skills provide methodology guidance and structured analysis frameworks rather than generating vulnerability findings directly. Every output includes confidence indicators and "verify by" instructions. Skills never present AI-generated findings as ground truth. Structured templates with explicit verification guidance are essential.

**Safety Alignment Paradox:**
Commercial LLM compliance with cyber attack assistance decreased from 52% to 28% (improved safety), but this also reduces legitimate red-team utility. PROJ-010 frames all guidance within established professional methodology (PTES, OWASP, NIST) to work within safety boundaries. The methodology-first approach inherently avoids most safety alignment conflicts.

**Multi-Agent Architecture Validated:**
Wiz AI Cyber Model Arena confirmed that agent scaffold matters as much as model capability -- the same model performs dramatically differently depending on orchestration. Claude Code on Claude Opus 4.6 ranked first overall. This directly supports Jerry's multi-skill architecture approach and validates domain specialization over generalization.

| Source | Finding |
|--------|---------|
| D-002 | Capability matrix, academic benchmarks (CyberSecEval 3, HarmBench, Wiz Arena, HTB, ARTEMIS), failure modes, ethical boundaries, design implications |

---

## L2: Cross-Stream Convergence Analysis

Independent streams arriving at the same conclusions represent the highest-confidence findings. Six convergence patterns emerged.

### Convergence 1: Methodology-First Design Over Execution Automation

**Streams:** D (LLM Boundaries) + C (Tool Integration) + A (Role Completeness)

Stream D independently concluded that LLMs excel at structured reasoning, methodology guidance, and knowledge synthesis but fail at exploit execution, runtime analysis, and novel discovery. Stream C independently designed the "standalone capable" pattern where agents function fully without tools, using LLM reasoning for methodology guidance. Stream A's roster design implicitly adopted methodology guidance as the operating model -- agents are defined by their knowledge domains and decision-making roles, not by the tools they operate.

**Consolidated Conclusion:** PROJ-010 is definitively a methodology-guidance framework with tool augmentation, not an autonomous execution engine. This is the highest-confidence design principle, validated independently from three perspectives.

### Convergence 2: Supply Chain Security as Critical Emerging Concern

**Streams:** B (Defensive Standards) + F (Secure SDLC) + A (Role Completeness)

Stream B documented OWASP Top 10 2025's new A03 Software Supply Chain Failures and NIST SP 800-53 Rev 5's addition of the SR (Supply Chain Risk Management) control family. Stream F independently found that all five SDLC models (MS SDL, SSDF, SAMM, SLSA, DevSecOps) converge on supply chain security. Stream A independently expanded eng-infra's scope to include SBOM generation, dependency provenance, and build reproducibility, and added eng-devsecops for automated dependency analysis and container scanning.

**Consolidated Conclusion:** Supply chain security is a first-class architectural concern distributed across eng-infra (infrastructure), eng-devsecops (tooling), and eng-reviewer (verification). SLSA Build L2 minimum for production, L3 for C3/C4.

### Convergence 3: Authorization Scope Over Human Oversight for Agent Safety

**Streams:** F (Authorization Architecture) + C (Tool Integration Security) + D (LLM Boundaries)

Stream F's analysis of OWASP Agentic AI Top 10 and AWS Scoping Matrix concluded that authorization scope bounds risk more effectively than human oversight. Stream C independently designed scoped credential management where agents never see raw credentials and all tool execution is sandboxed. Stream D independently concluded that human-in-the-loop is required not because agents need approval for every action, but because agents cannot make authorization decisions, legal judgments, or novel discoveries.

**Consolidated Conclusion:** The authorization architecture should make out-of-scope actions structurally impossible rather than relying solely on human approval. Scope is an architectural property enforced by infrastructure (network rules, tool proxies, scope oracle), with human oversight at phase boundaries and for decisions requiring judgment.

### Convergence 4: Configurable Rule Sets as the Compliance Architecture

**Streams:** B (Defensive Standards) + F (Configurable Rules) + A (Roster -- eng-compliance deferral)

Stream B identified that OWASP ASVS's 3-level assurance model provides a natural configuration axis for rule sets. Stream F independently analyzed five rule configuration systems (Semgrep, OPA, SonarQube, Checkov, ESLint) and designed the YAML-first profile management architecture. Stream A independently deferred eng-compliance because "compliance requirements vary radically by regulatory environment; configurable rule sets (R-011) are a better fit than a static agent."

**Consolidated Conclusion:** Configurable rule sets are the correct architecture for compliance, not a dedicated compliance agent. The profile management system with cascading overrides satisfies organizational diversity while maintaining sensible defaults.

### Convergence 5: SARIF and Structured Output as Integration Lingua Franca

**Streams:** C (Tool Integration) + E (LLM Portability) + F (Configurable Rules)

Stream C selected SARIF v2.1.0 as the primary finding normalization format for tool integration. Stream E independently selected JSON Schema as the universal tool and output definition format for portability. Stream F independently found that all five rule configuration systems converge on structured, validatable schemas (YAML or JSON Schema). All three streams arrived at the same principle: structured, schema-validated data formats are the integration mechanism across tools, providers, and configurations.

**Consolidated Conclusion:** JSON Schema for definitions, SARIF for findings, YAML for configuration. These three structured formats form the data interchange layer across all PROJ-010 subsystems.

### Convergence 6: Security Decomposition Requires Multiple Specialized Roles

**Streams:** A (Role Completeness) + B (Methodology Standards) + F (Secure SDLC)

Stream A documented that Google Chrome Security operates three sub-teams, Microsoft embeds 14 Deputy CISOs, and the AppSec model decomposes into 5-7 functions -- all indicating that a single "security" role is insufficient. Stream B independently mapped distinct standards to distinct agent responsibilities (OWASP for eng-backend/eng-frontend, NIST for eng-architect/eng-lead, CIS for eng-infra). Stream F independently mapped SDLC phases to specific agents, confirming that security responsibilities distribute across the entire team rather than concentrating in one role.

**Consolidated Conclusion:** eng-security narrows to manual secure code review. Automated tooling goes to eng-devsecops. Infrastructure hardening goes to eng-infra. Governance goes to eng-lead. Architecture security goes to eng-architect. Post-deployment goes to eng-incident. Security is everyone's responsibility with specific, non-overlapping specializations.

---

## L2: Cross-Stream Conflicts and Resolutions

### Conflict 1: OPSEC as Standalone Agent vs. Distributed Competency

**Streams in Tension:** A-002 (recommended red-opsec as conditional agent) vs. A-003 (distributed Defense Evasion ownership)

**Nature of Conflict:** A-002's organizational evidence suggested a dedicated OPSEC agent, while A-003's ATT&CK analysis showed Defense Evasion (which includes OPSEC techniques) should be distributed across operational agents.

**Resolution (from A-004):** OPSEC decomposes into two distinct domains: infrastructure OPSEC (C2 hardening, redirector segmentation) which belongs to red-infra, and operational OPSEC (communication discipline, artifact cleanup, deconfliction) which belongs to red-lead's expanded scope. No elite organization studied staffs a standalone OPSEC-only role. A dedicated agent would create handoff overhead without a distinct knowledge domain.

**Confidence:** HIGH. Both organizational evidence and framework analysis independently support the distributed model.

### Conflict 2: Impact (TA0040) Ownership -- Offensive Demonstration vs. Risk Communication

**Streams in Tension:** A-003 (14 Impact techniques with unclear ownership) vs. A-002 (red team organizations focus on demonstrated impact)

**Nature of Conflict:** Impact techniques span both technical capability (demonstrating system compromise) and stakeholder communication (conveying risk severity). No single agent naturally owns both.

**Resolution (from A-004):** Shared responsibility: red-exploit owns technical impact demonstration (safe simulation of destructive capabilities), red-reporter owns impact risk documentation and stakeholder communication. This split follows the natural boundary between technical capability and communication.

**Confidence:** MEDIUM. The split is logical but untested in the agent architecture; validate during Phase 5 purple team exercises.

### Conflict 3: Threat Intelligence -- Dedicated Agent vs. Cross-Skill Integration

**Streams in Tension:** A-001 (3 of 4 elite engineering organizations have dedicated TI) vs. PLAN.md (no TI agent in either roster)

**Nature of Conflict:** Organizational evidence strongly supports dedicated threat intelligence, but adding TI agents to both rosters would duplicate a shared function.

**Resolution (from A-004):** Cross-skill integration serves the primary use case: red-recon provides adversary-informed intelligence to eng-architect for threat modeling. This avoids function duplication. Reconsideration trigger: if /eng-team deploys independently of /red-team in scenarios where no red team engagement informs architecture.

**Confidence:** MEDIUM. Depends on the assumption that /eng-team and /red-team deploy together. If independent deployment is common, eng-threatintel should be reconsidered.

### Conflict 4: DREAD Scoring Subjectivity vs. Quantitative Risk Requirement

**Streams in Tension:** B-004 (DREAD has known subjectivity criticism; Microsoft has moved toward CVSS for some uses) vs. PLAN.md (requires quantitative risk scoring for threat models)

**Nature of Conflict:** DREAD provides the simplest quantitative scoring but is criticized for inconsistency across analysts.

**Resolution (from B-004):** The subjectivity criticism is mitigated in the agentic context because: (1) eng-architect applies consistent scoring rubrics (unlike human teams with varying expertise), (2) scoring criteria are codified as configurable rules in the agent definition, (3) /adversary integration validates scoring consistency for C2+ deliverables, (4) DREAD scores are cross-referenced with CVSS where applicable. Per R-011, users can substitute CVSS-based scoring if their organization prefers it.

**Confidence:** HIGH. The agentic context specifically addresses DREAD's primary weakness.

### Conflict 5: Safety Alignment vs. Red Team Utility

**Streams in Tension:** D-002 (commercial LLMs refuse many offensive security requests; compliance decreased from 52% to 28%) vs. PLAN.md R-018 (agents MUST use real offensive techniques mapped to ATT&CK)

**Nature of Conflict:** Safety-aligned models refuse direct exploit code generation, attack automation, and malware creation -- yet /red-team is intended to guide real offensive methodology.

**Resolution (from D-002):** The methodology-first design inherently avoids most safety alignment conflicts. /red-team provides methodology guidance, planning, analysis, and reporting -- all within the "allowed" zone for safety-aligned models. Skills frame all guidance within established professional methodology (PTES, OWASP, NIST) using professional security terminology. /red-team never generates exploit code directly; it guides practitioners to use established exploitation frameworks with methodology-driven approach. The conflict resolves because PROJ-010's design aligns with what models allow (methodology guidance) rather than what they refuse (direct exploitation).

**Confidence:** HIGH. The resolution is a direct consequence of the methodology-first architecture, which is independently validated by the convergence analysis.

---

## Requirements Traceability

Every consolidated finding maps to one or more of the 24 PLAN.md requirements.

| Requirement | Requirement Name | Contributing Streams | Key Finding |
|-------------|------------------|---------------------|-------------|
| R-001 | Secure by Design | B, F | STRIDE+DREAD default threat modeling; layered SDLC with security at every phase; NIST SSDF governance |
| R-002 | Architecturally Pure | C, E | Two-layer portability architecture; common adapter interface; SARIF normalization; separation of semantic intent from rendering |
| R-003 | No Slop Code | B, D | CWE Top 25 as code review focus; hallucination mitigation through structured templates with verification guidance |
| R-004 | No Shortcuts | F | Layered SDLC (5 models); SLSA provenance; DevSecOps automation at every pipeline stage; no phase skipping |
| R-005 | Grounded in Reality | D | LLM capability boundaries documented; "unvalidated" markers for tool-less analysis; methodology-first design over execution claims |
| R-006 | Evidence-Driven Decisions | All | 130+ unique sources across 6 R-006 categories (Industry Leaders/Experts/Innovators, Community Leaders/Experts/Innovators) |
| R-007 | Persistent Research Artifacts | All | 20 artifacts across 6 streams persisted to work/research/ |
| R-008 | Role Completeness Analysis | A | A-001 through A-004: gap analysis against 7+ elite organizations; ATT&CK 14/14 tactic coverage; 4 conditional agents with deferral rationale |
| R-009 | Current Intelligence | All | Context7 and WebSearch used across all streams; sources dated 2024-2026; CWE Top 25 2025, OWASP ASVS 5.0, ATT&CK 2025 |
| R-010 | LLM Portability | E | Two-layer architecture; 63% portable fields; 4 provider adapters (Anthropic, OpenAI, Google, open-source); 18 validation criteria; backward compatible |
| R-011 | Configurable Rule Sets | F, B | YAML-first format; SonarQube profile management; cascading overrides; comprehensive defaults mapped to OWASP ASVS, CWE, ATT&CK, PTES |
| R-012 | Tool Integration Architecture | C | MCP primary protocol; CLI/API adapter fallbacks; common interface; SARIF normalization; standalone capable with 3-level degradation |
| R-013 | C4 /adversary on Every Phase | B, F | Quality gate integration points defined; S-014 scoring used for portability validation (PV-015); SDLC models mapped to /adversary review points |
| R-014 | Full /orchestration Planning | F | SDLC phases mapped to agent workflow; DevSecOps pipeline stages mapped to agents; SSDF practice groups mapped to agent responsibilities |
| R-015 | Detailed /worktracker | All | All 20 research artifacts tracked with stream/artifact IDs; WORKTRACKER.md maintained with FEAT-level tracking |
| R-016 | Challenge Weak Specifications | A, D | A-004 challenges and resolves PLAN.md roster gaps; D-002 challenges autonomous execution assumptions with capability evidence |
| R-017 | Industry Leader Standard | All | Validated against Google, Microsoft, CrowdStrike, Mandiant, TrustedSec, SpecterOps, Rapid7, Netflix team structures and practices |
| R-018 | Real Offensive Techniques | A, B | 14/14 ATT&CK tactic coverage; PTES/OSSTMM methodology; technique-level agent mapping; methodology-first design compatible with safety alignment |
| R-019 | Secure SDLC Practices | B, F | OWASP ASVS 5.0, NIST SSDF, CIS Benchmarks, CWE Top 25 mapped to specific agents; SAMM maturity assessment |
| R-020 | Authorization Verification | F | Three-layer authorization architecture; scope oracle; default-deny tool access; ephemeral credentials; tamper-evident audit trail |
| R-021 | Actionable Remediation | A, D | red-reporter generates remediation guidance; eng-incident handles vulnerability lifecycle; D-002 validates LLM report generation as HIGH capability |
| R-022 | Agent Development Standards | E | Portable agent definition schema with 38 fields classified by portability; RCCF pattern for system prompt assembly |
| R-023 | Persist All Outputs | C, D | Filesystem-as-memory architecture; tool findings persisted via SARIF; evidence vault for /red-team engagement data |
| R-024 | /adversary Integration | A, B, F | eng-reviewer as final gate with /adversary C4; cross-skill integration points; DREAD scoring validated through /adversary; SDLC review phase maps to /adversary |

---

## Phase 2 Input Summary

For each Phase 2 Architecture feature, the specific findings from this synthesis that feed into that feature's design.

### FEAT-010: Agent Team Architecture

| Input | Source | Description |
|-------|--------|-------------|
| Final /eng-team roster (10 agents) | A-004 | eng-architect, eng-lead, eng-backend, eng-frontend, eng-infra, eng-qa, eng-security (narrowed), eng-reviewer, eng-devsecops (new), eng-incident (new) |
| Final /red-team roster (11 agents) | A-004 | red-lead (expanded), red-recon, red-vuln, red-exploit (expanded), red-privesc, red-lateral (narrowed for C2), red-persist, red-exfil, red-reporter (expanded), red-infra (new), red-social (new) |
| Scope modifications for 7 retained agents | A-004 | eng-security narrowed, eng-infra expanded (supply chain), eng-qa expanded (security testing), red-lead expanded (OPSEC, QA, adaptation), red-exploit expanded (Impact, evasion), red-lateral narrowed (C2 to red-infra), red-reporter expanded (Impact documentation) |
| 4 deferred agents with triggers | A-004 | eng-threatintel, eng-compliance, red-opsec, red-cloud -- each with specific reconsideration conditions |
| 4 cross-skill integration points | A-004 | Threat-Informed Architecture, Attack Surface Validation, Secure Code vs. Exploitation, Incident Response Validation |
| Non-linear kill chain workflow | A-004 R-ROSTER-014 | /red-team agents invocable in any order; explicit cycling support between phases |
| Defense Evasion distributed ownership | A-004 R-ROSTER-012 | red-infra owns tool-level evasion; each operational agent owns phase-specific evasion |
| ATT&CK 14/14 coverage proof | A-004 | Full tactic-to-agent mapping with technique counts and coverage ratings |
| Agent-to-standards mapping | B-003 | Each /eng-team agent mapped to primary standards (OWASP, NIST, CIS, CWE) |
| Agent-to-SDLC-phase mapping | F-001 | Each agent mapped to MS SDL phase, SSDF practice, SAMM function, SLSA role, DevSecOps stage |
| Multi-agent architecture validated | D-002 | Wiz Arena confirms scaffold matters as much as model; domain specialization over generalization |

### FEAT-011: Skill Routing and Invocation Architecture

| Input | Source | Description |
|-------|--------|-------------|
| /eng-team 8-step workflow sequence | F-001 | eng-architect -> eng-lead -> eng-backend/frontend/infra -> eng-devsecops -> eng-qa -> eng-security -> eng-reviewer -> eng-incident |
| /red-team non-linear kill chain | A-004 | 11 agents invocable in any order; kill chain organizes capability, not workflow sequence |
| Threat modeling methodology selection | B-004 | eng-architect routes to STRIDE/DREAD/PASTA/LINDDUN/Attack Trees based on criticality level and engagement context |
| Standards-based routing context | B-003 | Agent routing should consider which standards apply (OWASP for web, CIS for infra, CWE for code review) |
| Phase transition verification | F-002 | Circuit breaker checks at every kill-chain phase transition for /red-team |
| Purple team routing | A-004 | Cross-skill routing for 4 integration points (red-recon to eng-architect, red-exploit to eng-backend, etc.) |
| Safety alignment compatibility | D-002 | Routing must frame requests as professional methodology guidance to avoid safety filter triggers |

### FEAT-012: LLM Portability Architecture

| Input | Source | Description |
|-------|--------|-------------|
| Two-layer architecture design | E-003 | Semantic Layer (agent definitions) + Rendering Layer (provider adapter YAML configs) |
| 4 provider adapter specifications | E-003 | Anthropic, OpenAI, Google, open-source (via LiteLLM) adapter YAML configs |
| Portable agent definition schema (38 fields) | E-003 | Identity, capability, guardrail, tool schema, output schema, portability config fields with portability classification |
| 18 portability validation criteria | E-003 | PV-001 through PV-018: static, behavioral, and regression tests |
| RCCF prompt pattern | E-001 via E-003 | Role-Context-Constraints-Format as maximally portable system prompt structure |
| JSON Schema as universal format | E-001/E-002 via E-003 | All tool definitions and output schemas use JSON Schema |
| Adaptive reasoning strategy | E-001 via E-003 | CoT injection only for models that benefit; omit for frontier models |
| LiteLLM for open-source models | E-002 via E-003 | Delegate chat template handling to LiteLLM for 100+ models |
| Backward compatibility guarantees | E-003 | Existing 37 agents work unchanged; portability section optional |
| Migration path (4 phases) | E-003 | Foundation -> new agent authoring -> cross-provider validation -> existing agent migration (optional) |

### FEAT-013: Configurable Rule Set Architecture

| Input | Source | Description |
|-------|--------|-------------|
| YAML-first rule definition format | F-003 | Semgrep-inspired structured schema with required fields (id, category, severity, description, rationale, references) |
| Profile management system | F-003 | SonarQube-inspired: defaults, extension, per-engagement assignment, organizational hierarchy |
| Cascading override mechanism | F-003 | 5-layer cascade: skill defaults -> org profile -> team profile -> engagement overrides -> runtime flags |
| Dual-format authoring | F-003 | YAML for simple rules, Python for complex rules (Checkov pattern) |
| Standard rule schema | F-003 R-RULES-006 | Shared schema for both /eng-team and /red-team rules |
| /eng-team default rule sets | B-003, F-003 | OWASP ASVS 5.0 (3 levels), OWASP Top 10 2025, CWE Top 25 2025, CIS Benchmarks, NIST SSDF |
| /red-team default rule sets | F-003 | MITRE ATT&CK (14 tactics), PTES (7 phases), OSSTMM (5 channels), OWASP Testing Guide |
| Scope enforcement policy patterns | F-003 | OPA/Rego architectural patterns for /red-team scope enforcement |
| Rule testing framework | F-003 | Positive/negative/parameter variation tests following Semgrep, OPA, ESLint patterns |
| Git-based rule versioning | F-003 | Rules version-controlled; engagements pin to specific versions |

### FEAT-014: Tool Integration Adapter Architecture

| Input | Source | Description |
|-------|--------|-------------|
| MCP as primary integration protocol | C-003 | 97M+ monthly SDK downloads; 13,000+ servers; backed by Anthropic/OpenAI/Google/Microsoft; FastMCP 3.0 for server creation |
| Three adapter patterns | C-003 | MCP server, CLI adapter, API adapter -- all implementing common interface |
| Common adapter interface | C-003 | `execute(params) -> StructuredResult \| ToolUnavailableError` |
| SARIF-based finding normalization | C-003 | Common Finding schema with 12 fields; SARIF v2.1.0 as primary format |
| Standalone capable design | C-003 | 3-level graceful degradation; tools augment, not enable |
| Security controls | C-003 | Command allowlists, subprocess sandboxing, credential broker, output validation, size limits |
| Implementation priority | C-003 | P0: adapter interface + standalone logic; P1: SARIF + CLI adapters (Nmap, Semgrep, Trivy, Nuclei); P2: MCP evaluation + API adapters; P3: custom MCP servers + library adapters |
| Existing security MCP servers | C-003 | Reference implementations: mcp-for-security, pentest-mcp, hexstrike-ai, sast-mcp, Semgrep MCP |
| Tool orchestration patterns | C-003 | Sequential chaining, parallel execution, conditional branching |
| Output sanitization requirements | C-003 | Schema validation before agent consumption; prompt injection via tool output documented as MCP attack vector |

### FEAT-015: Authorization and Scope Control Architecture

| Input | Source | Description |
|-------|--------|-------------|
| Three-layer authorization architecture | F-002 | Structural (pre-engagement) + Dynamic (runtime) + Retrospective (post-execution) |
| OWASP Agentic AI Top 10 risk mapping | F-002 | ASI01-ASI10 risk-to-mitigation mapping for /red-team and /eng-team |
| Per-agent authorization model | F-002 | 11 agents with distinct authorization levels, tool access, network scope, data access |
| Scope enforcement components | F-002 | Scope Document Store, Scope Oracle, Tool Proxy, Network Enforcer, Audit Logger, Evidence Vault, Circuit Breaker |
| Default-deny tool access policy | F-002 | Tools explicitly granted per engagement scope; accessed through scope-validating proxy |
| Ephemeral credential model | F-002 | Time-bounded, scope-bounded, broker-mediated credentials |
| Tamper-evident audit trail | F-002 | Hash-chained or signed log entries; append-only for agents; read-only for red-reporter |
| Circuit breakers at phase transitions | F-002 | Scope revalidation at every kill-chain phase transition; cascading failure detection |
| Progressive autonomy deployment | F-002 | AWS Scoping Matrix: prescribed -> monitored -> supervised -> full agency |
| Production tool patterns | F-002 | XBOW (hundreds of autonomous agents within scope boundaries), PentAGI (Docker isolation, 20+ tools) |
| Guardrail layer architecture | F-002 | L1 Constitutional + L2 Policy + L3 Behavioral + L4 Output |
| Scope oracle as separate trust domain | F-002 | Independent service; agents cannot modify, bypass, or disable scope enforcement |
