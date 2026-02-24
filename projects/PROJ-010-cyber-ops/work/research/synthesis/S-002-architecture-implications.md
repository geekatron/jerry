# S-002: Architecture Implications Synthesis

> Synthesis | PROJ-010 Cyber Ops | Phase 1 Research

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | Architecture decision landscape and Phase 2 readiness |
| [Architecture Decision Inventory](#architecture-decision-inventory) | AD-001 through AD-012 decisions Phase 2 must formalize as ADRs |
| [Agent Architecture Specification Input](#agent-architecture-specification-input) | FEAT-010: agent identity, boundaries, handoff, tool mapping |
| [Skill Routing Specification Input](#skill-routing-specification-input) | FEAT-011: keyword triggers, routing tables, workflow patterns |
| [Security Architecture Specification Input](#security-architecture-specification-input) | FEAT-015: authorization model, scope enforcement, audit |
| [Cross-Cutting Architecture Concerns](#cross-cutting-architecture-concerns) | Issues affecting ALL Phase 2 features |
| [Open Questions for Phase 2](#open-questions-for-phase-2) | Genuine ambiguities research could not resolve |

---

## L0: Executive Summary

Phase 1 research across 6 streams and 20 artifacts produces 12 architecture decisions that Phase 2 must formalize as ADRs. The decisions fall into three confidence tiers: 7 HIGH-confidence decisions where independent streams converged on the same conclusion (methodology-first design, two-layer portability, SARIF normalization, layered authorization, YAML-first rule sets, common adapter interface, and the 21-agent roster), 3 MEDIUM-confidence decisions where strong evidence supports a clear recommendation but validation remains pending (agent isolation granularity, progressive autonomy deployment model, and cross-skill threat intelligence integration), and 2 decisions where research produced clear options with a recommended path but where Phase 2 design work will refine the specifics (kill chain workflow orchestration patterns and quality gate integration points). The architecture is anchored by three defining principles validated through cross-stream convergence: PROJ-010 is a methodology-guidance framework with tool augmentation (not an execution engine), security is an architectural property enforced through scope constraints (not an operational procedure relying on human oversight), and structured data formats (JSON Schema, SARIF, YAML) form the universal integration layer across tools, providers, and configurations. These 12 decisions map directly to Phase 2 features FEAT-010 through FEAT-015, providing the definitive specification input for each feature's ADR and design work.

---

## Architecture Decision Inventory

### AD-001: Methodology-First Design Paradigm

| Attribute | Value |
|-----------|-------|
| **Decision ID** | AD-001 |
| **Decision Title** | PROJ-010 operates as a methodology-guidance framework with tool augmentation, not an autonomous execution engine |
| **Research Evidence** | Convergence 1 in S-001: Stream D (LLM capability boundaries -- LLMs excel at structured reasoning but fail at exploit execution), Stream C (standalone capable pattern -- agents function fully without tools), Stream A (roster defined by knowledge domains, not tool operation). D-002 documents that hallucination is the dominant LLM failure mode (40%+ of AI-generated code contains flaws; NVD backlog worsened by false CVE submissions). |
| **Options Considered** | (1) Autonomous execution engine with LLM-driven tool automation. (2) Methodology-guidance framework with optional tool augmentation. (3) Hybrid with execution for some operations and guidance for others. |
| **Recommended Option** | Option 2: methodology-guidance framework. Every agent output provides methodology guidance, structured analysis, and verification instructions. Tools augment with real-time data and evidence but are never required for agent operation. |
| **Confidence Level** | HIGH -- three independent streams converged; this is the highest-confidence finding across all research. |
| **Maps to Phase 2 Feature** | ALL features. This is the foundational design principle that constrains every architectural decision. |

---

### AD-002: 21-Agent Roster (10 /eng-team + 11 /red-team)

| Attribute | Value |
|-----------|-------|
| **Decision ID** | AD-002 |
| **Decision Title** | Final agent roster: 10 /eng-team agents and 11 /red-team agents with 4 deferred agents |
| **Research Evidence** | A-004 (final roster with ATT&CK coverage proof), A-001 (elite engineering team patterns from Google, Microsoft, CrowdStrike, Mandiant), A-002 (red team patterns from TrustedSec, SpecterOps, Rapid7, Netflix), A-003 (MITRE ATT&CK 14-tactic analysis). Convergence 6: security decomposition requires multiple specialized roles validated independently by streams A, B, and F. |
| **Options Considered** | (1) PLAN.md baseline: 8 /eng-team + 9 /red-team = 17 agents. (2) Expanded roster: 10 /eng-team + 11 /red-team = 21 agents. (3) Further expansion with eng-threatintel, eng-compliance, red-opsec, red-cloud = 25 agents. |
| **Recommended Option** | Option 2: 21 agents. /eng-team adds eng-devsecops (automated security tooling) and eng-incident (post-deployment response). /red-team adds red-infra (C2 infrastructure, tool development -- highest-confidence addition across both rosters with three independent evidence streams) and red-social (human attack vector). Four agents deferred with specific reconsideration triggers documented in A-004. |
| **Confidence Level** | HIGH -- validated against 7 elite organizations; ATT&CK 14/14 tactic coverage proven; three evidence streams converge for red-infra. |
| **Maps to Phase 2 Feature** | FEAT-010 (Agent Team Architecture) |

---

### AD-003: Two-Layer LLM Portability Architecture

| Attribute | Value |
|-----------|-------|
| **Decision ID** | AD-003 |
| **Decision Title** | Semantic Layer (agent definitions) + Rendering Layer (provider adapter YAML configs) for LLM portability |
| **Research Evidence** | E-003 (architecture design with 4 provider adapter specifications), E-001 (RCCF portable prompt pattern, JSON Schema convergence, XML as Anthropic-specific anti-pattern), E-002 (industry convergence on agent-as-configuration pattern from CrewAI, LangChain, Google ADK; DSPy semantic-intent separation principle). Convergence 5: JSON Schema as universal tool/output definition format validated independently by streams C, E, and F. |
| **Options Considered** | (1) Single-layer: write provider-specific agents (fork per provider). (2) Abstraction library: code-based adapter layer (like LangChain Runnables). (3) Two-layer declarative: YAML configuration for rendering, markdown for agent definitions. (4) Compiler approach: DSPy-style compilation of semantic signatures to provider-specific prompts. |
| **Recommended Option** | Option 3: two-layer declarative. Agent definitions (Semantic Layer) capture provider-agnostic intent. Provider adapter YAML configs (Rendering Layer) describe transformation rules. 63% of fields fully portable, 24% require adaptation, 13% non-portable provider-specific optimizations. Backward compatible: existing 37 Jerry agents work unchanged with `portability.enabled` defaulting to false. |
| **Confidence Level** | HIGH -- E-001 and E-002 independently converge; industry has settled on configuration-driven definitions; 18 testable validation criteria (PV-001 through PV-018) defined. |
| **Maps to Phase 2 Feature** | FEAT-012 (LLM Portability Architecture) |

---

### AD-004: Three-Layer Authorization Architecture

| Attribute | Value |
|-----------|-------|
| **Decision ID** | AD-004 |
| **Decision Title** | Pre-engagement structural authorization + runtime scope enforcement + post-execution audit verification |
| **Research Evidence** | F-002 (OWASP Agentic AI Top 10 risk mapping, scope enforcement component design, per-agent authorization model, production tool patterns from XBOW and PentAGI), Convergence 3 in S-001 (streams F, C, and D independently conclude that authorization scope bounds risk more effectively than human oversight). |
| **Options Considered** | (1) Human-in-the-loop: human approves every agent action. (2) Policy-only: pre-engagement rules with no runtime enforcement. (3) Three-layer: structural + dynamic + retrospective authorization. (4) Full autonomy: agents operate within broad guidelines with post-hoc review only. |
| **Recommended Option** | Option 3: three-layer architecture. Layer 1 (structural): signed scope documents define authorization boundaries before engagement. Layer 2 (dynamic): scope oracle, tool proxy, and network enforcer intercept and validate every action at runtime. Layer 3 (retrospective): red-reporter performs audit verification with tamper-evident logs. This makes out-of-scope actions structurally impossible rather than procedurally prevented. |
| **Confidence Level** | HIGH -- OWASP Agentic AI Top 10 provides canonical risk taxonomy; XBOW and PentAGI validate isolated execution as production-viable; three streams converge on scope-over-oversight principle. |
| **Maps to Phase 2 Feature** | FEAT-015 (Authorization & Scope Control Architecture) |

---

### AD-005: MCP-Primary Tool Integration with CLI/API Fallback

| Attribute | Value |
|-----------|-------|
| **Decision ID** | AD-005 |
| **Decision Title** | MCP as primary integration protocol; CLI adapters as first fallback; API adapters as second fallback; all behind a common adapter interface |
| **Research Evidence** | C-003 (MCP adoption data: 97M+ monthly SDK downloads, 13,000+ servers, backed by Anthropic/OpenAI/Google/Microsoft; 6 existing security MCP servers validated; FastMCP 3.0 for server creation; common adapter interface design with `execute(params) -> StructuredResult`). |
| **Options Considered** | (1) MCP-only integration. (2) CLI-only via subprocess. (3) API-only via HTTP clients. (4) Protocol hierarchy: MCP primary, CLI fallback, API fallback, all behind common interface. |
| **Recommended Option** | Option 4: protocol hierarchy. Claude Code natively supports MCP, making it the natural primary protocol. CLI adapters handle tools without MCP servers (most current security tools). API adapters handle tools with REST/GraphQL interfaces (SonarQube, Burp Suite, ZAP). The common adapter interface (`execute(params) -> StructuredResult | ToolUnavailableError`) abstracts protocol details from agent logic, enabling tool substitution without agent changes. |
| **Confidence Level** | HIGH -- MCP ecosystem maturity validated; existing security MCP servers (pentest-mcp, hexstrike-ai, sast-mcp) prove the pattern; common interface pattern is standard in all analyzed frameworks. |
| **Maps to Phase 2 Feature** | FEAT-014 (Tool Integration Adapter Architecture) |

---

### AD-006: SARIF-Based Finding Normalization

| Attribute | Value |
|-----------|-------|
| **Decision ID** | AD-006 |
| **Decision Title** | SARIF v2.1.0 as the primary finding normalization format with a 12-field common Finding schema |
| **Research Evidence** | C-003 (SARIF as OASIS standard supported by CodeQL, Semgrep, Nuclei, Trivy, Checkmarx; common Finding schema design with id, source_tool, severity, category, title, description, location, evidence, remediation, references, confidence, raw_data). Convergence 5: JSON Schema for definitions, SARIF for findings, YAML for configuration -- three structured formats form the data interchange layer. |
| **Options Considered** | (1) Custom JSON schema per tool. (2) SARIF v2.1.0 as primary with normalizers for non-SARIF tools. (3) CycloneDX/SPDX for all outputs. (4) Unstructured text with regex parsing. |
| **Recommended Option** | Option 2: SARIF primary. SARIF v2.1.0 is already the output format for the highest-priority security tools (Semgrep, CodeQL, Nuclei, Trivy). Non-SARIF tools are normalized to the common Finding schema, which is serializable to/from SARIF. This enables cross-tool finding correlation, severity-based prioritization regardless of source, and uniform reporting. |
| **Confidence Level** | HIGH -- SARIF is an OASIS standard with broad tool support; convergence across streams C, E, and F on structured data formats. |
| **Maps to Phase 2 Feature** | FEAT-014 (Tool Integration Adapter Architecture) |

---

### AD-007: YAML-First Configurable Rule Sets with Profile Management

| Attribute | Value |
|-----------|-------|
| **Decision ID** | AD-007 |
| **Decision Title** | YAML as primary rule definition format with SonarQube-inspired profile management, ESLint-style cascading overrides, and Python escape hatch for complex rules |
| **Research Evidence** | F-003 (Semgrep YAML format, OPA/Rego patterns, SonarQube inheritance, Checkov dual-format, ESLint flat config analysis). Convergence 4: streams B, F, and A independently conclude that configurable rule sets are the correct compliance architecture (not a dedicated compliance agent). B-003 maps OWASP ASVS 3-level assurance model as natural configuration axis. |
| **Options Considered** | (1) YAML-only rules. (2) Python-only rules. (3) YAML primary with Python escape hatch (Checkov pattern). (4) OPA/Rego as rule language. (5) JSON Schema-based rules. |
| **Recommended Option** | Option 3: YAML primary with Python escape hatch. YAML handles the majority of rules with Semgrep-inspired structured schema (id, category, severity, description, rationale, references, configurable_params). Python handles complex rules requiring multi-step validation, dynamic computation, or cross-rule dependencies. Profile management follows SonarQube inheritance with 5-layer cascading: skill defaults -> organization profile -> team/project profile -> engagement overrides -> runtime flags. |
| **Confidence Level** | HIGH -- five independent rule systems analyzed converge on this pattern; eng-compliance deferral in A-004 validates configurable rules over static agent. |
| **Maps to Phase 2 Feature** | FEAT-013 (Configurable Rule Set Architecture) |

---

### AD-008: Layered SDLC Governance Model

| Attribute | Value |
|-----------|-------|
| **Decision ID** | AD-008 |
| **Decision Title** | Five-layer SDLC model with NIST SSDF as governance, MS SDL as workflow, OWASP SAMM as assessment, Google SLSA as supply chain, and DevSecOps as automation |
| **Research Evidence** | F-001 (MS SDL evolution, SSDF governance mapping, SAMM maturity levels, SLSA build levels, DevSecOps pipeline stages). B-003 (OWASP, NIST, CIS, SANS standards analysis with per-agent mapping). Convergence 2: supply chain security identified as critical emerging concern by streams B, F, and A independently. |
| **Options Considered** | (1) Single SDLC model (MS SDL only). (2) Standards menu (user selects one). (3) Layered model with each framework assigned to its area of strength. |
| **Recommended Option** | Option 3: layered model. Each framework serves a distinct, non-overlapping purpose: NIST SSDF for compliance traceability, MS SDL for phase-gate workflow structure, OWASP SAMM for maturity measurement, Google SLSA for build integrity, and DevSecOps for CI/CD integration. Every /eng-team agent security activity references the SSDF practice ID it implements. SLSA Build L2 minimum for production releases; Build L3 for C3/C4 engagements. |
| **Confidence Level** | HIGH -- all five models converge on supply chain security; each framework addresses a distinct gap; no single model covers all requirements. |
| **Maps to Phase 2 Feature** | FEAT-010 (Agent Team Architecture), FEAT-013 (Configurable Rule Set Architecture) |

---

### AD-009: STRIDE+DREAD Default Threat Modeling with Criticality Escalation

| Attribute | Value |
|-----------|-------|
| **Decision ID** | AD-009 |
| **Decision Title** | STRIDE for threat identification + DREAD for risk scoring as default, with methodology escalation by criticality level |
| **Research Evidence** | B-004 (comparison of STRIDE, DREAD, PASTA, LINDDUN, and Attack Trees; DREAD subjectivity analysis and agentic mitigation). Conflict resolution 4 in S-001: DREAD subjectivity mitigated in agentic context through consistent scoring rubrics, codified rules, and /adversary validation. |
| **Options Considered** | (1) STRIDE-only (no quantitative scoring). (2) STRIDE+CVSS (industry-standard scoring). (3) STRIDE+DREAD (simple quantitative scoring with agentic mitigation). (4) PASTA-only (business-impact-focused). (5) STRIDE+DREAD default with criticality-based escalation to Attack Trees and PASTA. |
| **Recommended Option** | Option 5: STRIDE+DREAD default with escalation. C1 uses STRIDE only. C2 adds DREAD scoring. C3 adds Attack Trees for complex path visualization. C4 adds PASTA stages 4-7 for business impact analysis. LINDDUN invoked when system processes PII subject to privacy regulations. Per R-011, users can substitute CVSS-based scoring via configurable rule sets. |
| **Confidence Level** | HIGH -- DREAD's primary weakness (subjectivity) is specifically addressed by the agentic context; escalation path covers all criticality levels; user override via R-011 eliminates lock-in. |
| **Maps to Phase 2 Feature** | FEAT-010 (Agent Team Architecture), FEAT-013 (Configurable Rule Set Architecture) |

---

### AD-010: Standalone Capable Design with Three-Level Degradation

| Attribute | Value |
|-----------|-------|
| **Decision ID** | AD-010 |
| **Decision Title** | All 21 agents function without any external tools; three-level graceful degradation (full tools, partial tools, standalone) |
| **Research Evidence** | C-003 (standalone capable design pattern with degradation ladder), Convergence 1 in S-001 (methodology-first design means agents are defined by knowledge domains, not tool operation), D-002 (LLMs reliably perform methodology guidance, code pattern detection, threat modeling, and report generation without tools). |
| **Options Considered** | (1) Tool-required: agents fail if tools unavailable. (2) Tool-preferred: agents degrade gracefully but some capabilities lost entirely. (3) Standalone capable: every capability works at all three levels with reduced evidence quality at lower levels. |
| **Recommended Option** | Option 3: standalone capable. Level 0 (full tool access): optimal evidence-backed analysis. Level 1 (partial tools): analysis with explicit uncertainty markers for gaps. Level 2 (no tools): LLM-only analysis with "unvalidated" markers and manual verification guidance. Every agent capability works at Level 2. Tools augment evidence quality; they do not enable reasoning. |
| **Confidence Level** | HIGH -- directly follows from AD-001 (methodology-first); validated by D-002 capability analysis; aligns with R-012. |
| **Maps to Phase 2 Feature** | FEAT-014 (Tool Integration Adapter Architecture), FEAT-010 (Agent Team Architecture) |

---

### AD-011: Agent Isolation Architecture

| Attribute | Value |
|-----------|-------|
| **Decision ID** | AD-011 |
| **Decision Title** | VM-per-engagement boundary, container-per-agent-group execution, sandbox-per-tool-execution, append-only evidence storage |
| **Research Evidence** | F-002 (isolation architecture comparison: container-per-agent from PentAGI, VM-per-engagement implied by XBOW, sandbox-per-execution from NVIDIA guidance, namespace-per-team from enterprise DevSecOps). C-003 (subprocess sandboxing, no shell=True, credential broker pattern). |
| **Options Considered** | (1) No isolation (shared process space). (2) Container-per-agent (full isolation per agent). (3) Container-per-agent-group (phase-based isolation). (4) VM-per-engagement with container-per-group and sandbox-per-execution (layered). |
| **Recommended Option** | Option 4: layered isolation. Engagement boundary uses VM or namespace for complete inter-engagement isolation. Agent execution uses container-per-agent-group so agents in the same kill-chain phase share context but are isolated from other phases. Tool execution uses fresh sandbox per invocation to prevent tool output from contaminating agent state. Evidence storage uses dedicated append-only volume for tamper-evident collection. |
| **Confidence Level** | MEDIUM -- pattern validated by XBOW and PentAGI production deployments, but the specific granularity (container-per-agent vs. container-per-phase) requires Phase 2 performance and coordination analysis. |
| **Maps to Phase 2 Feature** | FEAT-015 (Authorization & Scope Control Architecture) |

---

### AD-012: Progressive Autonomy Deployment Model

| Attribute | Value |
|-----------|-------|
| **Decision ID** | AD-012 |
| **Decision Title** | AWS Scoping Matrix progression: prescribed agency -> monitored agency -> supervised agency -> full agency |
| **Research Evidence** | F-002 (AWS Agentic AI Security Scoping Matrix with 4-level graduated controls), F-002 R-AUTH-009 (progressive autonomy deployment recommendation). |
| **Options Considered** | (1) Fixed autonomy level for all deployments. (2) Binary: human-in-the-loop or fully autonomous. (3) Progressive 4-level autonomy scaling with corresponding security controls. |
| **Recommended Option** | Option 3: progressive autonomy. New deployments start at prescribed agency (human approves every action). Organizations advance to monitored agency (near-real-time log review), supervised agency (phase boundary review), and full agency (engagement summary review) as confidence builds. Each level requires corresponding escalation in authorization controls, isolation, and audit granularity per the AWS matrix. |
| **Confidence Level** | MEDIUM -- the framework is well-defined by AWS, but the specific mapping of /red-team engagement phases to autonomy levels requires validation during Phase 5 purple team exercises. |
| **Maps to Phase 2 Feature** | FEAT-015 (Authorization & Scope Control Architecture) |

---

## Agent Architecture Specification Input

This section provides the definitive specification input for FEAT-010 (Agent Team Architecture).

### Agent Identity Schema

Every agent definition uses the portable schema from E-003, combining Jerry's existing YAML-frontmatter-with-markdown format and the new portability fields. The schema applies uniformly to all 21 agents.

**Identity fields (portable across all providers):**

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Agent identifier (e.g., `eng-architect`, `red-recon`) |
| `version` | string | Semantic version of agent definition |
| `description` | string | Purpose and invocation triggers, under 1024 characters |
| `identity.role` | string | Human-readable role title |
| `identity.expertise` | list[string] | Domain expertise areas |
| `identity.cognitive_mode` | enum | `divergent`, `convergent`, `integrative`, `systematic`, `strategic`, `forensic` |
| `persona.tone` | string | Communication tone |
| `persona.communication_style` | string | Interaction style |

**Capability fields (adaptation-required for portability):**

| Field | Type | Description |
|-------|------|-------------|
| `capabilities.allowed_tools` | list[string] | Tool identifiers; core tools portable, MCP tools require registration |
| `capabilities.output_formats` | list[string] | Supported output formats |
| `capabilities.forbidden_actions` | list[string] | Constitutional prohibitions |
| `capabilities.required_features` | list[string] | Provider features needed: `tool_use`, `structured_output`, `vision` |
| `model` | string | Model preference in `{provider}/{model}` format |

**Portability fields (new, optional per E-003):**

| Field | Type | Description |
|-------|------|-------------|
| `portability.enabled` | boolean | Multi-provider validated; default false |
| `portability.minimum_context_window` | integer | Minimum context window required |
| `portability.model_preferences` | list[string] | Ordered fallback list |
| `portability.reasoning_strategy` | enum | `adaptive` (default), `explicit_cot`, `none` |
| `portability.body_format` | enum | `markdown` (portable default for new agents), `xml` (Anthropic-optimized), `rccf` |

### Agent Capability Boundary Definitions

Each agent has a defined, non-overlapping capability domain. Boundaries were established in A-004 and refined through conflict resolution in S-001.

#### /eng-team Agent Boundaries (10 agents)

| Agent | Capability Domain | Does NOT Do | Primary Standards |
|-------|-------------------|-------------|-------------------|
| eng-architect | System design, ADRs, threat modeling (STRIDE/DREAD/PASTA), architecture review, NIST CSF governance | Implementation, testing, operational security | NIST CSF 2.0, STRIDE/DREAD |
| eng-lead | Implementation planning, code standards enforcement, dependency decisions, technical quality ownership | Architecture design, security review, testing execution | MS SDL phases, NIST SSDF |
| eng-backend | Server-side implementation, input validation, auth/authz, API security, database security | Frontend, infrastructure, architecture | OWASP Top 10, OWASP ASVS |
| eng-frontend | Client-side implementation, XSS prevention, CSP, CORS, output encoding | Backend, infrastructure, architecture | OWASP Top 10, OWASP ASVS |
| eng-infra | IaC, container security, network segmentation, secrets management, supply chain (SBOM, provenance, build reproducibility) | Application code, security review | CIS Benchmarks, SLSA |
| eng-qa | Test strategy, security test cases, fuzzing, boundary testing, coverage enforcement, security testing integration | Implementation, architecture, code review | OWASP Testing Guide |
| eng-security | Manual secure code review, security requirements verification (narrowed from PLAN.md baseline -- automated tooling moved to eng-devsecops) | Automated scanning, CI/CD, infrastructure | CWE Top 25, OWASP ASVS |
| eng-reviewer | Final review gate, architecture compliance, security standards compliance, /adversary integration for C2+ | Implementation, testing, design | All /eng-team standards |
| eng-devsecops | Automated security tooling: SAST/DAST pipeline, CI/CD security, secrets scanning, container scanning, dependency analysis (new, absorbed from overloaded eng-security) | Manual code review, architecture, implementation | DevSecOps patterns, SLSA |
| eng-incident | Incident response runbooks, vulnerability lifecycle management, post-deployment security monitoring (new, fills Mandiant/Google/Microsoft post-deployment gap) | Development, pre-deployment review | NIST SSDF Respond practices |

#### /red-team Agent Boundaries (11 agents)

| Agent | Capability Domain | Does NOT Do | ATT&CK Tactics |
|-------|-------------------|-------------|-----------------|
| red-lead | Scope definition, RoE, methodology selection, team coordination, authorization verification, operational OPSEC, QA, adaptation decisions (expanded from PLAN.md baseline) | Direct execution of techniques | All (oversight) |
| red-recon | OSINT, network enumeration, service discovery, technology fingerprinting, attack surface mapping, threat intelligence for eng-architect | Exploitation, privilege escalation | TA0043 Reconnaissance |
| red-vuln | Vulnerability identification, CVE research, exploit availability, attack path analysis, risk scoring | Exploitation execution, persistence | (Analysis support) |
| red-exploit | Exploit development, payload crafting, vuln chaining, PoC development, technical impact demonstration, phase-specific evasion (expanded: Impact demonstration ownership) | Reconnaissance, reporting, C2 infrastructure | TA0001 Initial Access, TA0002 Execution, TA0040 Impact (technical) |
| red-privesc | Local and domain privesc, credential harvesting, token manipulation, misconfig exploitation, phase-specific evasion | Lateral movement (until authorized), C2, reconnaissance | TA0004 Privilege Escalation, TA0006 Credential Access |
| red-lateral | Pivoting, tunneling, living-off-the-land, internal exploitation (narrowed: C2 infrastructure moved to red-infra) | C2 build/management, tool development | TA0008 Lateral Movement, TA0007 Discovery |
| red-persist | Backdoor placement, scheduled tasks, service manipulation, rootkit methodology, detection evasion analysis | Exploitation, reporting | TA0003 Persistence, TA0005 Defense Evasion (persistence-related) |
| red-exfil | Data identification, exfiltration channels, covert communication, DLP bypass assessment | Exploitation, privilege escalation | TA0009 Collection, TA0010 Exfiltration |
| red-reporter | Finding documentation, risk scoring, remediation recommendations, executive summaries, impact risk communication, scope compliance attestation (expanded: Impact documentation ownership) | Active testing, exploitation | TA0040 Impact (documentation) |
| red-infra | C2 framework management, payload building, redirector infrastructure, tool development, tool-level defense evasion, infrastructure OPSEC (new, highest-confidence addition) | Direct exploitation, reconnaissance | TA0042 Resource Development, TA0011 C2, TA0005 Defense Evasion (tool-level) |
| red-social | Social reconnaissance, phishing methodology, pretexting frameworks, human attack vector analysis (new, closes human vector gap) | Technical exploitation, infrastructure | TA0043 Reconnaissance (social), TA0001 Initial Access (phishing) |

### Inter-Agent Handoff Protocol Requirements

#### /eng-team: Sequential Phase-Gate Workflow

The /eng-team follows an 8-step sequential workflow (from F-001 SDLC mapping):

```
eng-architect -> eng-lead -> eng-backend/eng-frontend/eng-infra (parallel)
    -> eng-devsecops -> eng-qa -> eng-security -> eng-reviewer -> eng-incident
```

**Handoff requirements:**
- Each phase produces a defined artifact (design doc, implementation plan, code, scans, tests, review report)
- eng-reviewer is the mandatory final gate with /adversary integration for C2+ deliverables
- Phase transition requires prior phase artifact completion
- eng-incident activates post-deployment; not gated by eng-reviewer

#### /red-team: Non-Linear Kill Chain with Phase Verification

The /red-team workflow is explicitly non-linear per A-004 recommendation R-ROSTER-014. Real engagements are iterative -- exploitation discovers new recon targets, triggering return to earlier phases.

**Handoff requirements:**
- Any agent invocable in any order after red-lead establishes scope
- Kill chain organizes capability, not workflow sequence
- Explicit support for cycling between phases (e.g., red-exploit findings trigger new red-recon)
- Circuit breaker check at every phase transition per F-002 R-AUTH-006
- Scope revalidation at every transition
- All handoffs logged to tamper-evident audit trail

#### Cross-Skill Integration Points (Purple Team)

Four integration points operationalize the PLAN.md requirement that the two skills work as adversaries:

| Integration Point | Source Agent | Target Agent | Data Exchanged |
|-------------------|-------------|--------------|----------------|
| Threat-Informed Architecture | red-recon | eng-architect | Adversary TTPs, attack surface intelligence |
| Attack Surface Validation | red-recon, red-vuln | eng-infra, eng-devsecops | Validation results against hardened targets |
| Secure Code vs. Exploitation | red-exploit, red-privesc | eng-security, eng-backend, eng-frontend | Exploitation results against reviewed code |
| Incident Response Validation | red-persist, red-lateral, red-exfil | eng-incident | Exercise results against response runbooks |

### Agent-to-Tool Mapping

Each agent has a defined set of tool categories aligned with its capability domain. Actual tool availability depends on adapter implementation (AD-005) and engagement configuration.

#### /eng-team Tool Categories

| Agent | Primary Tool Categories | Example Tools |
|-------|------------------------|---------------|
| eng-architect | Threat modeling, architecture analysis | STRIDE/DREAD templates, architecture diagramming |
| eng-lead | Project planning, standards enforcement | Linting, formatting, dependency analysis |
| eng-backend | SAST, secrets detection, API testing | Semgrep, Gitleaks, OWASP ZAP |
| eng-frontend | Browser security, CSP validation | Lighthouse, CSP Evaluator, DOM analysis |
| eng-infra | IaC scanning, container scanning, SBOM | Checkov, Trivy, Syft, CIS-CAT |
| eng-qa | Test execution, fuzzing, coverage | pytest, AFL, coverage.py |
| eng-security | Code analysis, CVE databases | CodeQL, CWE database, NVD |
| eng-reviewer | Quality scoring, standards verification | /adversary integration |
| eng-devsecops | SAST/DAST pipeline, dependency scanning | Semgrep CI, Trivy CI, Snyk, Dependabot |
| eng-incident | Log analysis, vulnerability tracking | SIEM integration, CVE tracking |

#### /red-team Tool Categories

| Agent | Primary Tool Categories | Example Tools |
|-------|------------------------|---------------|
| red-lead | Scope management, authorization verification | Scope document tools, engagement tracking |
| red-recon | Network scanning, OSINT, DNS | Nmap, Shodan, Amass, theHarvester |
| red-vuln | Vulnerability scanning, CVE research | Nuclei, Nessus, CVE databases |
| red-exploit | Exploitation frameworks, payload delivery | Metasploit, custom exploits, Burp Suite |
| red-privesc | Privilege escalation enumeration | LinPEAS, WinPEAS, BloodHound |
| red-lateral | Pivoting, protocol tools | Impacket, CrackMapExec, Chisel |
| red-persist | Persistence mechanisms, rootkit analysis | Custom persistence tools, autoruns |
| red-exfil | Data transfer, covert channels | Custom exfil tools, DNS tunneling |
| red-reporter | Report generation, evidence compilation | Report templates, evidence vault |
| red-infra | C2 frameworks, payload building, redirectors | Cobalt Strike, Sliver, Mythic, redirector configs |
| red-social | Phishing, pretexting | GoPhish, social engineering toolkits |

---

## Skill Routing Specification Input

This section provides the definitive specification input for FEAT-011 (Skill Routing & Invocation).

### Keyword Trigger Maps

#### /eng-team Keyword Triggers

| Trigger Keywords | Agent | Routing Context |
|------------------|-------|-----------------|
| design, architecture, ADR, threat model, system design, STRIDE, DREAD, PASTA | eng-architect | Architecture and threat modeling tasks |
| implementation plan, code standards, PR review, dependencies, tech lead | eng-lead | Planning and standards enforcement |
| backend, server-side, API, authentication, authorization, database, input validation | eng-backend | Server-side implementation |
| frontend, client-side, XSS, CSP, CORS, output encoding, DOM | eng-frontend | Client-side implementation |
| infrastructure, IaC, container, Kubernetes, Docker, network, secrets, SBOM, supply chain | eng-infra | Infrastructure and supply chain security |
| test, QA, fuzzing, coverage, boundary testing, regression, security testing | eng-qa | Testing and quality assurance |
| code review, secure review, CWE, vulnerability assessment, security requirements | eng-security | Manual secure code review |
| final review, review gate, standards compliance, deliverable review | eng-reviewer | Final gate review |
| CI/CD, pipeline, SAST, DAST, scanning, automated security, container scan, dependency scan | eng-devsecops | Automated security tooling |
| incident, response, post-deployment, vulnerability lifecycle, monitoring, breach | eng-incident | Incident response and post-deployment |

#### /red-team Keyword Triggers

| Trigger Keywords | Agent | Routing Context |
|------------------|-------|-----------------|
| scope, rules of engagement, authorization, methodology, engagement, coordination | red-lead | Engagement management |
| reconnaissance, OSINT, enumeration, discovery, fingerprint, attack surface, DNS | red-recon | Reconnaissance phase |
| vulnerability, CVE, scan, exploit availability, attack path, risk score | red-vuln | Vulnerability analysis |
| exploit, payload, proof of concept, vulnerability chain, initial access, execution | red-exploit | Exploitation |
| privilege escalation, privesc, credential, token, misconfig, local admin, domain admin | red-privesc | Privilege escalation |
| lateral movement, pivot, tunnel, living off the land, internal network | red-lateral | Lateral movement |
| persistence, backdoor, scheduled task, rootkit, detection evasion | red-persist | Persistence |
| exfiltration, data theft, covert channel, DLP bypass, collection | red-exfil | Data exfiltration |
| report, finding, remediation, executive summary, documentation, engagement report | red-reporter | Reporting |
| C2, command and control, payload build, redirector, infrastructure, tool development | red-infra | Infrastructure and tooling |
| social engineering, phishing, pretext, human vector, spear phishing | red-social | Social engineering |

### Routing Decision Table

| Input Characteristics | Skill | Agent Selection | Routing Logic |
|-----------------------|-------|-----------------|---------------|
| Request about system design with security consideration | /eng-team | eng-architect | Architecture + security triggers |
| Request to implement secure backend feature | /eng-team | eng-lead -> eng-backend | eng-lead plans, eng-backend implements |
| Request to scan code for vulnerabilities | /eng-team | eng-devsecops | Automated scanning triggers |
| Request to review code for security flaws (manual) | /eng-team | eng-security | Manual review triggers |
| Request to review deliverable for standards compliance | /eng-team | eng-reviewer | Final gate triggers |
| Request for penetration test of target | /red-team | red-lead (first) | All engagements start with scope |
| Request for target reconnaissance | /red-team | red-recon (after red-lead scope) | Recon triggers, scope prerequisite |
| Request to exploit specific vulnerability | /red-team | red-exploit (after red-lead scope) | Exploit triggers, scope prerequisite |
| Request for engagement report | /red-team | red-reporter | Reporting triggers |
| Request for C2 setup or payload building | /red-team | red-infra | Infrastructure triggers |
| Request involving both building and attacking | Both | Cross-skill purple team routing | Both skill triggers present |
| Request about threat modeling informed by adversary TTPs | Both | red-recon -> eng-architect | Cross-skill integration point 1 |
| Safety alignment conflict (direct exploit code request) | /red-team | Reframe through methodology | Frame as PTES/OWASP methodology guidance per D-002 |

### Multi-Agent Workflow Patterns

#### Pattern 1: Sequential (eng-team default)

```
Trigger: "Build a secure API"
  -> eng-architect (design + threat model)
  -> eng-lead (implementation plan)
  -> eng-backend (implement)
  -> eng-devsecops (automated scans)
  -> eng-qa (tests)
  -> eng-security (manual review)
  -> eng-reviewer (final gate + /adversary)
```

Each agent completes before the next begins. Phase artifacts are the handoff mechanism.

#### Pattern 2: Non-Linear with Phase Cycling (red-team)

```
Trigger: "Penetration test against target X"
  -> red-lead (scope + authorization) [MANDATORY FIRST]
  -> red-recon (attack surface mapping)
  -> red-vuln (vulnerability identification)
  -> red-exploit (exploitation)
     -> discovers new attack surface -> cycles back to red-recon
  -> red-privesc (escalation)
     -> discovers new vulnerabilities -> cycles back to red-vuln
  -> red-lateral (network movement)
  -> red-persist (persistence, if in scope)
  -> red-exfil (data exfiltration, if in scope)
  -> red-reporter (documentation + remediation) [MANDATORY LAST for reporting]
```

Any agent invocable after red-lead establishes scope. Kill chain is capability organization, not workflow sequence. Circuit breaker check at every transition.

#### Pattern 3: Parallel Execution (within a phase)

```
Trigger: "Implement feature X" (after architecture phase)
  -> eng-backend + eng-frontend + eng-infra (parallel implementation)
  -> eng-devsecops (automated scans on all outputs)
  -> eng-qa (tests across all components)
```

Independent agents execute in parallel when their inputs are available and their work does not depend on each other's output.

#### Pattern 4: Purple Team Cross-Skill (integration testing)

```
Trigger: "Validate security of component Y"
  -> eng-architect (design review) + red-recon (attack surface)
  -> red-vuln (vulnerability analysis of eng-architect's design)
  -> red-exploit (attempt exploitation of eng-backend's implementation)
  -> eng-security (review findings) + eng-incident (response exercise)
  -> red-reporter + eng-reviewer (joint assessment)
```

Cross-skill routing activates the four integration points defined in A-004. Both skills' agents operate on shared artifacts.

#### Pattern 5: Conditional Branching (context-dependent)

```
Trigger: "Security assessment of application Z"
  Agent selects based on target characteristics:
    if web_application: eng-frontend + eng-backend focus
    if infrastructure: eng-infra focus
    if API: eng-backend + red-exploit (API testing)
    if source_code_available: eng-security + eng-devsecops
    if network_target: red-recon + red-vuln + red-exploit
```

Routing adapts based on the nature of the target, available information, and engagement scope.

---

## Security Architecture Specification Input

This section provides the definitive specification input for FEAT-015 (Authorization & Scope Control).

### Authorization Model

The three-layer authorization architecture (AD-004) implements R-020 (authorization verification before execution) as an architectural property.

#### Layer 1: Structural Authorization (Pre-Engagement)

| Component | Description | Owner | Enforcement |
|-----------|-------------|-------|-------------|
| Scope Document | Signed YAML defining authorized targets, techniques, time windows, exclusions, RoE | red-lead | Loaded at engagement start; immutable during engagement |
| Target Allowlist | Explicit IP ranges, domains, applications authorized for testing | red-lead | Network-level filtering; all agent network access through scope proxy |
| Technique Allowlist | MITRE ATT&CK technique IDs authorized for this engagement | red-lead | Tool access gated by technique mapping; unauthorized techniques structurally unavailable |
| Time Window | Start/end timestamps for engagement authorization | red-lead | Credential expiration tied to window; automatic revocation at close |
| Exclusion List | Systems, networks, data types that must not be touched | red-lead | Deny rules checked before every tool invocation; supersede all allow rules |

#### Layer 2: Dynamic Authorization (Runtime)

| Component | Function | Trust Level | Failure Mode |
|-----------|----------|-------------|--------------|
| Scope Oracle | Evaluates proposed actions against scope rules; separate trust domain | High -- independent process; agents cannot modify or bypass | Default deny; agents cannot operate if oracle unavailable |
| Tool Proxy | Intercepts all tool invocations; validates target and technique against scope | High -- only path to tool access | Tools inaccessible without proxy; no direct tool access |
| Network Enforcer | Firewall/proxy rules derived from scope document | High -- infrastructure-level | No network access outside scope; fail-closed |
| Credential Broker | Provides ephemeral, scope-bounded, time-limited tokens | High -- agents never see raw credentials | Credentials expire at window close; scope-limited blast radius |

#### Layer 3: Retrospective Authorization (Post-Execution)

| Activity | Description | Owner | Automation |
|----------|-------------|-------|-----------|
| Action Log Review | Every agent action compared against scope document | red-reporter | Automated scope compliance check |
| Evidence Verification | All findings traced to authorized actions within scope | red-reporter | Chain-of-custody verification |
| Scope Deviation Detection | Actions that approached or touched scope boundaries | red-lead | Automated boundary proximity analysis |
| Compliance Report | Formal attestation that engagement stayed within scope | red-lead, red-reporter | Generated from audit trail; requires red-lead sign-off |

### Scope Enforcement Components

Seven components form the scope enforcement infrastructure. These operate independently of agent code -- agents cannot modify, bypass, or disable any component.

| Component | Function | Trust Level | Failure Mode |
|-----------|----------|-------------|--------------|
| Scope Document Store | Immutable storage for signed scope definitions | Highest | Engagement cannot start without valid scope |
| Scope Oracle | Evaluates proposed actions against scope rules | High -- separate process, own trust domain | Default deny; engagement pauses |
| Tool Proxy | Intercepts all tool invocations; validates against scope | High -- only tool access path | Tools inaccessible; agent degrades to standalone |
| Network Enforcer | Firewall/proxy rules derived from scope document | High -- infrastructure-level | No network access outside scope; fail-closed |
| Audit Logger | Records all actions to tamper-evident log | High -- append-only; separate from agent access | Engagement pauses if audit system fails |
| Evidence Vault | Stores all artifacts with chain-of-custody | High -- append-only for agents; read by red-reporter | Evidence preserved even if agent systems fail |
| Circuit Breaker | Monitors for cascading failures and scope boundary proximity | Medium -- advisory and escalation | Alerts red-lead; does not independently halt engagement |

### Per-Agent Authorization Levels

Each of the 11 /red-team agents operates under distinct authorization constraints. This is the definitive per-agent authorization model from F-002.

| Agent | Authorization Level | Tool Access | Network Scope | Data Access |
|-------|---------------------|-------------|--------------|-------------|
| red-lead | Full engagement scope; can define/modify scope | All coordination tools | All authorized targets (verification) | Full audit trail; scope documents |
| red-recon | Reconnaissance-only | Passive/active recon tools only | Authorized target IPs/domains only | Target enumeration data; no exploit output |
| red-vuln | Analysis scope; read-only against targets | Vulnerability scanners, CVE databases | Authorized targets (scan only) | Scan results; CVE data; no credentials |
| red-exploit | Exploitation scope; target + technique allowlist | Exploitation frameworks within technique allowlist | Authorized targets only; port-level restrictions | Exploitation artifacts; PoC outputs |
| red-privesc | Post-exploitation; compromised host only | Privesc tools on compromised hosts | Compromised host only (until lateral authorized) | Local host data; credential material |
| red-lateral | Lateral movement; authorized network range | Pivoting tools, C2 usage via red-infra | Authorized network range | Internal network data within scope |
| red-persist | Persistence scope; only if authorized in RoE | Persistence mechanism tools | Compromised hosts within scope | Host-level configuration |
| red-exfil | Exfiltration scope; data types per RoE | Data identification and transfer tools | Evidence repository only (no external exfil) | Classified data within engagement scope |
| red-infra | Infrastructure scope; engagement infra only | C2 frameworks, payload builders, redirectors | Engagement infrastructure network | C2 infrastructure; payload artifacts |
| red-social | Social engineering; only if authorized in RoE | Phishing tools, pretexting frameworks | Email/communication channels as authorized | Contact lists; social data within scope |
| red-reporter | Report scope; read-only on all engagement data | Report generation tools | Evidence repository (read); report delivery (write) | Full engagement data (read-only) |

### Audit Trail Requirements

Per F-002 R-AUTH-005 and R-020 evidence preservation requirement:

| Requirement | Implementation |
|-------------|---------------|
| Tamper evidence | Hash-chained or signed log entries; append-only for agents |
| Completeness | Every agent action logged: timestamp, agent identity, tool invocation, target parameters, scope oracle decision, result |
| Chain of custody | All findings traced from discovery through agent action to scope authorization |
| Read access | red-reporter has read-only access for report generation |
| Retention | Engagement data retained per organizational policy; evidence vault survives agent system failure |
| Compliance output | Automated scope compliance report generated from audit trail; requires red-lead sign-off |

### OWASP Agentic AI Top 10 Coverage

The architecture addresses all 10 OWASP Agentic AI risks. Phase 2 must formalize these as architectural requirements.

| Risk | Mitigation | Implementing Components |
|------|-----------|------------------------|
| ASI01 Agent Goal Hijack | Immutable scope definitions from signed engagement file; goal validation at every decision point | Scope Document Store, Scope Oracle |
| ASI02 Tool Misuse | Default-deny tool access through scope-validating Tool Proxy; technique allowlist enforcement | Tool Proxy, Scope Oracle |
| ASI03 Identity/Privilege Abuse | Ephemeral, engagement-scoped credentials via Credential Broker; per-agent authorization levels | Credential Broker, Network Enforcer |
| ASI04 Supply Chain Vulnerabilities | Signed agent definitions; verified tool binaries; SLSA provenance for agent runtime | SLSA Build L2+, eng-infra |
| ASI05 Unexpected Code Execution | Sandboxed execution environments; code review for C3+ engagements | Sandbox-per-execution isolation |
| ASI06 Memory/Context Poisoning | Validated intelligence sources; context integrity verification; immutable engagement parameters | Scope Document Store |
| ASI07 Insecure Inter-Agent Communication | Authenticated inter-agent messaging; signed task delegation | Handoff protocol, chain-of-authority |
| ASI08 Cascading Failures | Circuit breakers at phase transitions; mandatory scope revalidation | Circuit Breaker |
| ASI09 Human-Agent Trust Exploitation | Mandatory evidence verification; confidence scoring; /adversary review | Audit Logger, Evidence Vault, /adversary |
| ASI10 Rogue Agents | Comprehensive audit logging; behavioral monitoring; scope verification at every invocation | All enforcement components |

---

## Cross-Cutting Architecture Concerns

These concerns affect ALL Phase 2 features (FEAT-010 through FEAT-015) and must be addressed holistically rather than within any single feature's ADR.

### Portability Layer Integration

**Affects:** FEAT-010 (agent definitions), FEAT-011 (routing), FEAT-012 (portability), FEAT-014 (tool integration)

All 21 agent definitions must use the portable agent schema from E-003. Phase 2 must decide:

- **Body format:** New agents use `body_format: markdown` (portable default per R-PORT-ARCH-002). Existing Jerry agents remain XML.
- **System prompt assembly:** Provider adapters use RCCF pattern (Role-Context-Constraints-Format) per R-PORT-ARCH-011. Section ordering adjustable per provider (open-source adapter places constraints before context).
- **Tool schema format:** All tool definitions use JSON Schema per R-PORT-ARCH-003. The common adapter interface (AD-005) must produce tool definitions in JSON Schema that the rendering layer transforms to provider-specific registration format.
- **Structured output:** The rendering layer handles the divergence (OpenAI `response_format`, Anthropic tool-call workaround, Google `response_schema`, open-source prompt-level). Agent definitions declare output schemas in JSON Schema; enforcement mechanism is the rendering layer's responsibility.
- **Reasoning strategy:** All agents default to `adaptive` per R-PORT-ARCH-004. Rendering layer injects CoT only for models that benefit (open-source, smaller models) and omits for frontier models.
- **Model preferences:** Each agent declares ordered fallback list per R-PORT-ARCH-005. Minimum two providers.

### Configurable Rule Set Integration

**Affects:** FEAT-010 (agent behavior), FEAT-011 (routing context), FEAT-013 (rule sets), FEAT-015 (scope enforcement)

Rule sets govern agent behavior across both skills. Phase 2 must integrate:

- **Agent-to-rule-set binding:** Each agent references its primary rule sets (e.g., eng-backend references OWASP ASVS, red-exploit references ATT&CK techniques). The active profile determines which rules apply.
- **Routing context:** Rule set configuration affects routing decisions. If an organization substitutes OWASP with a proprietary standard per R-011, the routing keywords must still resolve correctly.
- **Scope enforcement policies:** /red-team scope enforcement uses OPA/Rego architectural patterns per F-003. Scope oracle evaluates proposed actions against policy rules. The policy format must be the same YAML-first format as other rule sets for consistency.
- **Default rule sets:** /eng-team defaults to OWASP ASVS 5.0, OWASP Top 10 2025, CWE Top 25 2025, CIS Benchmarks, NIST SSDF. /red-team defaults to MITRE ATT&CK, PTES, OSSTMM, OWASP Testing Guide. All overridable per R-011 via profile cascading.

### Quality Gate Integration (/adversary)

**Affects:** FEAT-010 (agent output quality), FEAT-011 (routing to /adversary), FEAT-012 (cross-provider quality validation)

All deliverables from both skills go through /adversary quality enforcement per R-013 and R-024. Phase 2 must integrate:

- **Quality threshold:** >= 0.95 for PROJ-010 (above standard 0.92). Up to 5 creator-critic iterations per R-013.
- **S-014 LLM-as-Judge scoring:** Applied to all agent outputs. The same 6-dimension rubric (completeness, internal consistency, methodological rigor, evidence quality, actionability, traceability) applies to both /eng-team and /red-team deliverables.
- **Portability quality validation:** PV-015 uses S-014 scoring to validate cross-provider output quality. Threshold >= 0.85 on all target providers (0.07 degradation allowance).
- **eng-reviewer as final gate:** For /eng-team, eng-reviewer invokes /adversary for C2+ deliverables as the mandatory last step.
- **red-reporter quality:** /red-team findings go through /adversary for quality scoring and completeness review per PLAN.md integration table.
- **SDLC review phase:** MS SDL review phase maps to /adversary review points per F-001.

### Tool Integration Adapter Pattern

**Affects:** FEAT-010 (agent-to-tool mapping), FEAT-014 (adapter architecture), FEAT-015 (scope enforcement for tool access)

The common adapter interface (AD-005) cuts across agent definitions, tool integration, and scope enforcement. Phase 2 must integrate:

- **Adapter interface:** `execute(params) -> StructuredResult | ToolUnavailableError` implemented by all adapter types (MCP, CLI, API).
- **Scope-validating proxy:** For /red-team, all tool invocations pass through the Tool Proxy which validates target and technique parameters against scope before allowing execution. The adapter interface must support scope validation as a transparent middleware layer.
- **Finding normalization:** All adapters normalize output to the common Finding schema (AD-006). Cross-tool correlation and deduplication operate on normalized findings.
- **Graceful degradation:** Each agent's tool mapping must account for all three degradation levels (AD-010). Agent logic calls adapters; adapter availability determines evidence quality level.
- **Security controls:** Command allowlists (no shell=True), subprocess sandboxing, credential broker pattern, output schema validation, and output size limits are adapter-layer concerns, not agent-layer concerns.
- **Implementation priority:** P0 is the common adapter interface + standalone logic. P1 is SARIF parser + CLI adapters for highest-ROI tools (Nmap, Semgrep, Trivy, Nuclei). P2 is MCP evaluation + API adapters. P3 is custom MCP servers.

### Data Interchange Formats

**Affects:** ALL features

Three structured formats form the universal data interchange layer per Convergence 5 in S-001:

| Format | Purpose | Used By |
|--------|---------|---------|
| JSON Schema | Tool definitions, output schemas, agent capability declarations | FEAT-010, FEAT-012, FEAT-014 |
| SARIF v2.1.0 | Security finding normalization and cross-tool correlation | FEAT-014, FEAT-010 |
| YAML | Rule definitions, provider adapter configs, scope documents, agent frontmatter | FEAT-013, FEAT-012, FEAT-015, FEAT-010 |

### Defense Evasion Ownership Model

**Affects:** FEAT-010 (agent boundaries), FEAT-015 (technique authorization)

Defense Evasion (TA0005) is the largest ATT&CK tactic (43 techniques, 112 sub-techniques) and is distributed across agents per A-004 R-ROSTER-012:

- **red-infra** owns tool-level evasion (C2 obfuscation, payload encoding, redirector hardening)
- **Each operational agent** owns phase-specific evasion (red-persist owns persistence evasion, red-lateral owns movement evasion, red-exploit owns exploitation evasion)
- **No standalone evasion agent** -- following industry practice where evasion is embedded tradecraft

Phase 2 must ensure the authorization model (AD-004) accounts for distributed evasion technique authorization: each agent's technique allowlist must include the evasion techniques relevant to its operational phase.

### Safety Alignment Compatibility

**Affects:** FEAT-010 (agent prompt design), FEAT-011 (request framing)

Commercial LLM compliance with cyber attack assistance decreased from 52% to 28% (D-002). The methodology-first design (AD-001) inherently avoids most safety alignment conflicts, but Phase 2 must operationalize this:

- All /red-team agent prompts frame guidance within established professional methodology (PTES, OWASP, NIST) using professional security terminology
- Skill routing reframes direct exploit code requests as methodology guidance (routing decision table row: "Safety alignment conflict")
- /red-team never generates exploit code directly; it guides practitioners to use established exploitation frameworks
- The approach works because PROJ-010's design aligns with what models allow (methodology guidance) rather than what they refuse (direct exploitation)

---

## Open Questions for Phase 2

These are genuine ambiguities that Phase 1 research could not definitively resolve. Each requires deliberate design decisions during Phase 2 architecture work.

### OQ-001: Agent Isolation Granularity Trade-Off

**Context:** AD-011 recommends container-per-agent-group, but the specific grouping -- per individual agent vs. per kill-chain phase vs. per engagement stage -- involves performance and coordination trade-offs that research could not evaluate without implementation.

**What Phase 2 must decide:** The exact isolation boundary: which agents share a container, and what the inter-container communication overhead is. Container-per-agent provides maximum isolation but maximum overhead; container-per-phase provides practical isolation with manageable overhead; further analysis of coordination patterns during Phase 2 design will determine the right balance.

**Research input:** PentAGI uses container-per-engagement (single container, all tools). XBOW uses agent-per-vector (fine-grained). The right granularity depends on PROJ-010's specific coordination patterns which will be designed in Phase 2.

### OQ-002: Impact Technique Ownership Validation

**Context:** Conflict 2 in S-001 resolved Impact (TA0040) as shared: red-exploit owns technical demonstration, red-reporter owns documentation. This split is logical but rated MEDIUM confidence because it is untested.

**What Phase 2 must decide:** Formalize the split in agent definitions and validate during Phase 5 purple team exercises. If the split creates handoff friction, consider reassigning all Impact to red-exploit with red-reporter consuming the output.

### OQ-003: Cross-Skill Deployment Independence

**Context:** Conflict 3 in S-001 notes that the cross-skill threat intelligence integration (red-recon feeding eng-architect) assumes /eng-team and /red-team deploy together. If independent deployment is common, eng-threatintel may need to be reconsidered.

**What Phase 2 must decide:** Whether the architecture assumes co-deployment of both skills or must support independent operation. If independent: eng-threatintel becomes a required agent for standalone /eng-team deployment. If co-deployed: cross-skill integration points satisfy the threat intelligence requirement.

### OQ-004: Scope Document Signing and Verification Mechanism

**Context:** F-002 specifies that scope documents must be "signed" but does not prescribe the signing mechanism. Options range from simple HMAC to full PKI-based digital signatures.

**What Phase 2 must decide:** The specific signing mechanism for scope documents, balancing usability (operators should not need PKI infrastructure for simple engagements) with security (scope integrity is the foundation of the authorization model). Consider tiered signing: HMAC for C1/C2 engagements, digital signature for C3/C4.

### OQ-005: Structured Output Enforcement for Open-Source Models

**Context:** E-003's open-source adapter notes that structured output enforcement is "best_effort" for open-source models -- prompt-level schema instructions without server-side enforcement. The adapter specifies retry with explicit format reminder after failure, and raw output with validation errors after 3 failures.

**What Phase 2 must decide:** Whether the 3-retry-then-raw-output strategy is acceptable for security-critical structured outputs (engagement reports, scope compliance attestations, finding schemas). If not, open-source model support may need to mandate Instructor or Outlines for constrained generation, which adds infrastructure dependencies.

### OQ-006: Circuit Breaker Threshold Configuration

**Context:** F-002 R-AUTH-006 mandates circuit breakers at phase transitions but does not define the specific thresholds for triggering escalation vs. halt.

**What Phase 2 must decide:** What constitutes a "cascading failure pattern" that triggers the circuit breaker, what the specific thresholds are for alerting vs. pausing vs. halting the engagement, and whether circuit breaker sensitivity should be configurable per engagement profile (aligned with the configurable rule set architecture in AD-007).

### OQ-007: SDLC Maturity Baseline for Different Engagement Types

**Context:** AD-008 references OWASP SAMM Level 1 as minimum baseline, Level 2 as standard, and Level 3 for C4 engagements. But the mapping of engagement type to required maturity level is not fully specified.

**What Phase 2 must decide:** The specific SAMM maturity level requirements by engagement criticality, and whether maturity assessment is a prerequisite gate (must reach Level N before proceeding) or a measurement tool (assess current level, recommend improvements). This affects eng-lead's role as maturity assessor.
