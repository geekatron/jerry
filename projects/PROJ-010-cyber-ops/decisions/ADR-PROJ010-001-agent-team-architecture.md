# ADR-PROJ010-001: Agent Team Architecture for /eng-team and /red-team

<!--
DOCUMENT-ID: ADR-PROJ010-001
AUTHOR: ps-architect agent
DATE: 2026-02-22
STATUS: PROPOSED
PARENT-FEATURE: FEAT-010 (Agent Team Architecture)
PARENT-EPIC: EPIC-002 (Architecture & Design)
PROJECT: PROJ-010-cyber-ops
TYPE: Architecture Decision Record
-->

> **ADR ID:** ADR-PROJ010-001
> **Version:** 1.0.0
> **Date:** 2026-02-22
> **Author:** ps-architect
> **Status:** PROPOSED
> **Deciders:** User (P-020 authority), ps-architect (recommendation)
> **Quality Target:** >= 0.95
> **Parent Feature:** FEAT-010 (Agent Team Architecture)
> **Parent Epic:** EPIC-002 (Architecture & Design)

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Status](#status) | Current decision lifecycle stage |
| [Context](#context) | Why this decision is needed, constraints, Phase 1 research foundation |
| [Decision](#decision) | Agent identity schema, 21-agent roster, handoff protocols, cross-skill integration, SDLC governance, threat modeling, standalone design |
| [Options Considered](#options-considered) | Alternatives for each major sub-decision |
| [Consequences](#consequences) | Positive, negative, and neutral impacts |
| [Evidence Base](#evidence-base) | Citations from specific research artifacts |
| [Compliance](#compliance) | Jerry framework and PROJ-010 requirement compliance |
| [Related Decisions](#related-decisions) | Links to AD-001 through AD-010 and other ADRs |
| [Open Questions](#open-questions) | OQ-002 Impact ownership, OQ-003 cross-skill deployment independence |
| [References](#references) | Source citations |

---

## Status

**PROPOSED** -- This ADR requires ratification through the full governance process:

1. **Adversarial review** by ps-critic: PENDING
2. **User ratification** per P-020 (User Authority): PENDING

This ADR formalizes five architecture decisions from Phase 1 research:

| Decision | Title | Confidence |
|----------|-------|------------|
| AD-001 | Methodology-First Design Paradigm | HIGH |
| AD-002 | 21-Agent Roster (10 /eng-team + 11 /red-team) | HIGH |
| AD-008 | Layered SDLC Governance Model | HIGH |
| AD-009 | STRIDE+DREAD Default Threat Modeling with Criticality Escalation | HIGH |
| AD-010 | Standalone Capable Design with Three-Level Degradation | HIGH |

**Downstream Dependency Gating:** Upon acceptance, this ADR unblocks agent definition authoring (FEAT-010 implementation), skill routing design (FEAT-011), and tool integration architecture (FEAT-014) for all 21 agents.

---

## Context

### Why This Decision Is Needed

PROJ-010 introduces two new Jerry skills -- `/eng-team` (secure-by-design software engineering) and `/red-team` (offensive security operations). These skills require a formalized agent team architecture that defines: how many agents each skill contains, what each agent does and does not do, how agents hand off work to each other, how the two skills interact as adversaries, and what governance models constrain agent behavior. Without this ADR, agent definitions would be authored ad hoc, creating boundary overlap, coverage gaps, and inconsistent workflow patterns.

### Phase 1 Research Foundation

Phase 1 research across 6 streams and 20 artifacts produced the empirical foundation for this ADR. The research validated the architecture against 7 elite organizations (Google, Microsoft, CrowdStrike, Mandiant, TrustedSec, SpecterOps, Rapid7), achieved 14/14 MITRE ATT&CK tactic coverage, and identified 6 cross-stream convergence patterns where independent research streams arrived at the same conclusions (S-001).

The single most critical finding: LLMs excel at methodology guidance, structured reasoning, and report generation but fundamentally cannot replace tool execution or human judgment for novel discovery (S-001 Convergence 1, D-002). This validates PROJ-010's design as a methodology-guidance framework with tool augmentation, not an autonomous execution engine, and serves as the foundational constraint for every architectural decision in this ADR.

### Constraints

| Constraint | Source | Impact |
|------------|--------|--------|
| P-003: No Recursive Subagents | Jerry Constitution (HARD H-01) | All agent workflows operate within orchestrator -> worker pattern; no nested agent spawning |
| P-020: User Authority | Jerry Constitution (HARD H-02) | All architecture decisions require user ratification; agents cannot override user intent |
| R-001: Secure by Design | PLAN.md | Security is an architectural property, not an afterthought; every agent embeds security in its domain |
| R-008: Role Completeness | PLAN.md | Roster must demonstrate coverage gaps were analyzed against elite organizations |
| R-010: LLM Portability | PLAN.md | Agent definitions must use a portable schema supporting multiple LLM providers |
| R-012: Tool Integration | PLAN.md | All agents must function without tools (standalone capable) |
| R-017: Industry Leader Standard | PLAN.md | Architecture validated against industry-leading team structures |
| R-018: Real Offensive Techniques | PLAN.md | /red-team agents use real ATT&CK techniques, not theoretical abstractions |
| R-022: Agent Development Standards | PLAN.md | Agent definitions follow the portable schema from E-003 |
| Methodology-First (AD-001) | Phase 1 Convergence 1 | Agents provide methodology guidance with tool augmentation; they do not autonomously execute |
| Quality Gate >= 0.95 | PLAN.md R-013 | All PROJ-010 deliverables go through /adversary C4 review at this threshold |

---

## Decision

This section formalizes the agent team architecture for PROJ-010. It comprises seven sub-decisions organized as follows: the agent identity schema, the 21-agent roster with capability boundaries, scope modifications from the PLAN.md baseline, deferred agents with reconsideration triggers, inter-agent handoff protocols with cross-skill integration points, the defense evasion ownership model, agent-to-tool category mapping, layered SDLC governance (AD-008), threat modeling methodology (AD-009), and standalone capable design (AD-010).

### 1. Agent Identity Schema

Every agent definition uses the portable schema from E-003, combining Jerry's existing YAML-frontmatter-with-markdown format with new portability fields. The schema applies uniformly to all 21 agents.

#### Identity Fields (Fully Portable Across All Providers)

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

**Evidence:** E-003 portable agent schema design; E-001 RCCF prompt pattern; E-002 industry convergence on agent-as-configuration pattern (CrewAI, LangChain, Google ADK, DSPy).

#### Capability Fields (Adaptation-Required for Portability)

| Field | Type | Description |
|-------|------|-------------|
| `capabilities.allowed_tools` | list[string] | Tool identifiers; core tools portable, MCP tools require registration |
| `capabilities.output_formats` | list[string] | Supported output formats (JSON Schema-defined) |
| `capabilities.forbidden_actions` | list[string] | Constitutional prohibitions |
| `capabilities.required_features` | list[string] | Provider features needed: `tool_use`, `structured_output`, `vision` |
| `model` | string | Model preference in `{provider}/{model}` format |

**Evidence:** E-003 capability field classification; C-003 common adapter interface design; S-001 Convergence 5 (JSON Schema as universal tool/output definition format).

#### Portability Fields (New, Optional)

| Field | Type | Description |
|-------|------|-------------|
| `portability.enabled` | boolean | Multi-provider validated; default `false` |
| `portability.minimum_context_window` | integer | Minimum context window required |
| `portability.model_preferences` | list[string] | Ordered fallback list (minimum two providers per R-PORT-ARCH-005) |
| `portability.reasoning_strategy` | enum | `adaptive` (default), `explicit_cot`, `none` |
| `portability.body_format` | enum | `markdown` (portable default for new agents), `xml` (Anthropic-optimized), `rccf` |

New PROJ-010 agents use `body_format: markdown` as the portable default per E-001 finding that XML tags are Anthropic-specific optimization. Existing Jerry agents remain unchanged; `portability.enabled` defaults to `false` for backward compatibility (E-003 migration path).

**Evidence:** E-003 two-layer architecture design with 63% fully portable fields, 24% adaptation-required, 13% non-portable provider-specific; E-001 XML anti-pattern finding; E-002 Haystack FallbackChatGenerator pattern for model preferences.

### 2. The 21-Agent Roster with Capability Boundaries

The final roster comprises 10 /eng-team agents and 11 /red-team agents, expanded from the PLAN.md baseline of 8 /eng-team and 9 /red-team agents. The roster achieves 14/14 MITRE ATT&CK tactic coverage at STRONG level, validated against 7 elite organizations (A-004).

#### /eng-team: 10 Agents

| # | Agent | Capability Domain | Does NOT Do | Primary Standards |
|---|-------|-------------------|-------------|-------------------|
| 1 | eng-architect | System design, ADRs, threat modeling (STRIDE/DREAD/PASTA), architecture review, NIST CSF governance, threat intelligence consumption from /red-team cross-skill integration | Implementation, testing, operational security | NIST CSF 2.0, STRIDE/DREAD |
| 2 | eng-lead | Implementation planning, code standards enforcement, dependency decisions, technical quality ownership, SAMM maturity assessment | Architecture design, security review, testing execution | MS SDL phases, NIST SSDF |
| 3 | eng-backend | Server-side implementation, input validation, auth/authz, API security, database security | Frontend, infrastructure, architecture | OWASP Top 10, OWASP ASVS |
| 4 | eng-frontend | Client-side implementation, XSS prevention, CSP, CORS, output encoding | Backend, infrastructure, architecture | OWASP Top 10, OWASP ASVS |
| 5 | eng-infra | IaC, container security, network segmentation, secrets management, supply chain security (SBOM generation, dependency provenance, build reproducibility) | Application code, security review | CIS Benchmarks, Google SLSA |
| 6 | eng-qa | Test strategy, security test cases, fuzzing, property-based testing, boundary testing, security regression testing, coverage enforcement | Implementation, architecture, code review | OWASP Testing Guide |
| 7 | eng-security | Manual secure code review, security requirements verification, architecture security review (narrowed from PLAN.md -- automated tooling moved to eng-devsecops) | Automated scanning, CI/CD pipeline, infrastructure | CWE Top 25, OWASP ASVS |
| 8 | eng-reviewer | Final review gate, architecture compliance, security standards compliance, /adversary integration for C2+ deliverables | Implementation, testing, design | All /eng-team standards |
| 9 | eng-devsecops | Automated security tooling: SAST/DAST pipeline, CI/CD security, secrets scanning, container scanning, dependency analysis, security tooling selection (NEW -- absorbed from overloaded eng-security) | Manual code review, architecture, implementation | DevSecOps patterns, SLSA |
| 10 | eng-incident | Incident response runbooks, vulnerability lifecycle management, post-deployment security monitoring, containment coordination, remediation tracking (NEW -- fills post-deployment gap) | Development, pre-deployment review | NIST SSDF Respond practices |

**Evidence:** A-004 final roster decisions with evidence matrix; A-001 elite engineering team structures (Google Chrome 3 sub-teams, Microsoft SFI 14 Deputy CISOs, Mandiant IR "team of teams"); S-001 Convergence 6 (security decomposition requires multiple specialized roles).

#### /red-team: 11 Agents

| # | Agent | Capability Domain | Does NOT Do | ATT&CK Tactics |
|---|-------|-------------------|-------------|-----------------|
| 1 | red-lead | Scope definition, RoE, methodology selection, team coordination, authorization verification, operational OPSEC enforcement, findings QA, methodology adaptation decisions (expanded from PLAN.md) | Direct execution of techniques | All (oversight) |
| 2 | red-recon | OSINT, network enumeration, service discovery, technology fingerprinting, attack surface mapping, cross-skill threat intelligence for eng-architect | Exploitation, privilege escalation | TA0043 Reconnaissance |
| 3 | red-vuln | Vulnerability identification, CVE research, exploit availability assessment, attack path analysis, risk scoring | Exploitation execution, persistence | (Analysis support) |
| 4 | red-exploit | Exploit development, payload crafting, vulnerability chaining, PoC development, safe Impact demonstration (TA0040 technical), phase-specific defense evasion (expanded: Impact demonstration and execution-time evasion) | Reconnaissance, reporting, C2 infrastructure | TA0001 Initial Access, TA0002 Execution, TA0040 Impact (technical) |
| 5 | red-privesc | Local and domain privesc, credential harvesting, token manipulation, misconfig exploitation, credential-based defense evasion | Lateral movement (until authorized), C2, reconnaissance | TA0004 Privilege Escalation, TA0006 Credential Access |
| 6 | red-lateral | Pivoting, tunneling, living-off-the-land, internal exploitation, C2 usage during operations, network-level defense evasion (narrowed: C2 infrastructure design and management moved to red-infra) | C2 build/management, tool development | TA0008 Lateral Movement, TA0007 Discovery |
| 7 | red-persist | Backdoor placement, scheduled tasks, service manipulation, rootkit methodology, persistence-phase defense evasion (indicator removal, timestomping) | Exploitation, reporting | TA0003 Persistence, TA0005 Defense Evasion (persistence-related) |
| 8 | red-exfil | Data identification, exfiltration channels, covert communication, DLP bypass assessment, exfiltration-phase defense evasion (data encoding, encrypted channels) | Exploitation, privilege escalation | TA0009 Collection, TA0010 Exfiltration |
| 9 | red-reporter | Finding documentation, risk scoring, remediation recommendations, executive summaries, Impact risk communication and stakeholder documentation, scope compliance attestation (expanded: Impact documentation ownership) | Active testing, exploitation | TA0040 Impact (documentation) |
| 10 | red-infra | C2 framework management, payload building, redirector infrastructure, tool development, tool-level defense evasion (obfuscation, packing, sandbox evasion), infrastructure OPSEC, Resource Development (NEW -- highest-confidence addition across both rosters) | Direct exploitation, reconnaissance | TA0042 Resource Development, TA0011 Command and Control, TA0005 Defense Evasion (tool-level) |
| 11 | red-social | Social reconnaissance, phishing methodology, pretexting frameworks, vishing, credential harvesting via social channels, human attack vector analysis (NEW -- closes human vector gap) | Technical exploitation, infrastructure | TA0043 Reconnaissance (social), TA0001 Initial Access (phishing) |

**Evidence:** A-004 final roster with ATT&CK coverage proof (14/14 STRONG); A-002 red team patterns from 7 elite organizations; A-003 MITRE ATT&CK 14-tactic analysis; S-001 Convergence 1 (methodology-first design); S-001 Conflict 2 resolution (Impact shared ownership).

#### ATT&CK Coverage Proof

| Metric | Before (PLAN.md Baseline) | After (This ADR) |
|--------|---------------------------|-------------------|
| STRONG coverage | 8/14 (57%) | 14/14 (100%) |
| PARTIAL coverage | 2/14 (14%) | 0/14 (0%) |
| WEAK coverage | 2/14 (14%) | 0/14 (0%) |
| ZERO coverage | 2/14 (14%) | 0/14 (0%) |

The addition of 2 agents (red-infra, red-social) plus structural scope adjustments to 5 existing agents achieves full 14/14 tactic coverage. See A-004 for the complete tactic-by-tactic coverage table with technique counts.

### 3. Scope Modifications from PLAN.md Baseline

Seven agents have scope changes from the PLAN.md baseline, each driven by Phase 1 research evidence:

| Agent | Modification | Direction | Evidence |
|-------|-------------|-----------|----------|
| eng-security | Narrowed: removed SAST/DAST tooling and pipeline responsibilities (moved to eng-devsecops); retained manual secure code review, security requirements verification, architecture security review | Narrowed | A-001 Finding 2: Google Chrome splits security into 3 sub-teams; S-001 Convergence 6: single security role insufficient at elite team quality |
| eng-infra | Expanded: added explicit supply chain security scope (SBOM generation, dependency provenance, build reproducibility) | Expanded | S-001 Convergence 2: supply chain security as critical emerging concern (validated by OWASP Top 10 2025 A03, all 5 SDLC models); A-004 R-ROSTER-009 |
| eng-qa | Expanded: added security testing scope (fuzzing, property-based testing, security regression testing) | Expanded | A-001 Finding 2: Google Chrome Fuzzing team is distinct from manual review; A-004 roster changes table |
| red-lead | Expanded: added mid-engagement methodology adaptation, findings validation/QA, deconfliction management, post-engagement impact tracking, operational OPSEC enforcement | Expanded | A-002 Finding 5: CREST CCSAM validates lifecycle management as distinct from initial scope; A-002 Finding 3: OPSEC absorbed from deferred red-opsec |
| red-exploit | Expanded: added explicit Impact (TA0040) technical demonstration scope and execution-time defense evasion techniques (process injection, signed binary proxy execution) | Expanded | A-003 Finding 6: 14 Impact techniques had zero coverage; A-004 R-ROSTER-011/R-ROSTER-012 |
| red-lateral | Narrowed: removed C2 infrastructure design and management (moved to red-infra); retained C2 usage during lateral movement operations and network-level defense evasion | Narrowed | A-003 Rec 3: C2 separation; red-infra owns C2 architecture; red-lateral consumes C2 during operations |
| red-reporter | Expanded: added Impact risk documentation scope (stakeholder communication of impact potential, remediation urgency scoring) | Expanded | A-003 Rec 4: S-001 Conflict 2 resolution assigns Impact documentation to red-reporter |

### 4. Deferred Agents with Reconsideration Triggers

Four agents are deferred from the initial roster. Each has legitimate evidence supporting its existence but fails the decision criteria for immediate inclusion. Specific reconsideration triggers ensure these agents can be promoted when conditions warrant.

| Deferred Agent | Deferral Rationale | Reconsideration Trigger | Evidence |
|----------------|--------------------|------------------------|----------|
| eng-threatintel | Cross-skill integration with red-recon covers the primary use case (red-recon provides adversary TTPs to eng-architect for threat modeling). Adding a dedicated TI agent to /eng-team would duplicate a shared function. | /eng-team deployed independently of /red-team in scenarios where no red team engagement informs architecture decisions. | A-001 Finding 3: 3 of 4 elite organizations (Mandiant, CrowdStrike, Google Project Zero) maintain dedicated TI; A-004 R-ROSTER-005; S-001 Conflict 3 |
| eng-compliance | Compliance requirements vary radically by regulatory environment (HIPAA, PCI-DSS, FedRAMP, SOC 2). A static agent definition cannot cover this diversity credibly. Configurable rule sets (R-011) provide a better architecture. | Three or more users request compliance-specific guidance that configurable rule sets cannot serve. | A-001: Microsoft SDL compliance is the sole organizational evidence; A-004 R-ROSTER-006; S-001 Convergence 4 |
| red-opsec | Decomposes cleanly into two existing agents: infrastructure OPSEC (C2 hardening, redirector segmentation) goes to red-infra; operational OPSEC (communication discipline, artifact cleanup, deconfliction) goes to red-lead's expanded scope. No elite organization studied staffs a standalone OPSEC-only role. | Future engagement complexity reveals OPSEC coordination failures between red-infra and red-lead that distributed ownership cannot address. | A-002: recommended as conditional; A-004 R-ROSTER-007; S-001 Conflict 1 resolution |
| red-cloud | Explicitly out of scope per PLAN.md ("Cloud-specific provider tooling -- future extension"). Cloud-specific offensive operations are an emerging specialization (GIAC GCPN, DataDog Stratus Red Team, CyCognito 2026 research), but current agents are infrastructure-agnostic. | PROJ-010 scopes a cloud extension phase, or three distinct engagement scenarios require cloud-native attack paths that generic agents cannot address. | A-004 R-ROSTER-008; PLAN.md Out of Scope section |

### 5. Inter-Agent Handoff Protocols

#### /eng-team: 8-Step Sequential Phase-Gate Workflow

The /eng-team follows a sequential workflow mapped to Microsoft SDL phases and NIST SSDF practice groups (F-001):

```
Step 1: eng-architect   --> Design + Threat Model (STRIDE/DREAD)
Step 2: eng-lead        --> Implementation Plan + Security Standards Selection
Step 3: eng-backend / eng-frontend / eng-infra  --> Parallel Implementation
Step 4: eng-devsecops   --> Automated Security Scans (SAST/DAST/SCA/SBOM)
Step 5: eng-qa          --> Security Testing + Fuzzing + Coverage
Step 6: eng-security    --> Manual Secure Code Review
Step 7: eng-reviewer    --> Final Gate with /adversary Integration (C2+)
Step 8: eng-incident    --> Incident Response Plan + Runbooks (post-deployment)
```

**Handoff requirements:**

- Each phase produces a defined artifact (design doc, implementation plan, code, scan results, test results, review report, IR plan).
- Phase transition requires prior phase artifact completion.
- eng-backend, eng-frontend, and eng-infra execute in parallel at Step 3 when their inputs are available and their work does not depend on each other's output.
- eng-reviewer is the mandatory final gate with /adversary integration for C2+ deliverables per R-013.
- eng-incident activates post-deployment and is not gated by eng-reviewer for ongoing vulnerability lifecycle management.

**Evidence:** F-001 Agent Workflow Mapping (MS SDL phase-to-agent mapping, SSDF practice-to-agent mapping); S-002 Agent Architecture Specification Input (handoff protocol requirements).

#### /red-team: Non-Linear Kill Chain with Phase Cycling

The /red-team workflow is explicitly non-linear per A-004 R-ROSTER-014. Real engagements are iterative -- exploitation discovers new recon targets, triggering return to earlier phases. The kill chain organizes capability, not workflow sequence.

**Handoff requirements:**

- red-lead MUST establish scope and authorization before any other agent operates (mandatory first).
- After scope establishment, any agent is invocable in any order based on engagement context.
- Explicit support for cycling between phases (e.g., red-exploit findings trigger new red-recon; red-privesc discovers new vulnerabilities, triggering return to red-vuln).
- Circuit breaker check at every phase transition per F-002 R-AUTH-006 (scope revalidation, cascading failure detection).
- Scope revalidation at every agent transition against the signed scope document.
- All handoffs logged to tamper-evident audit trail per F-002 R-AUTH-005.
- red-reporter generates the final engagement report (mandatory last for reporting).

**Evidence:** A-004 R-ROSTER-014 (non-linear kill chain design); F-002 R-AUTH-006 (circuit breakers at phase transitions); S-002 handoff protocol requirements.

#### 4 Cross-Skill Integration Points (Purple Team)

Four integration points operationalize the PLAN.md requirement that "the two skills work as adversaries: /eng-team builds, /red-team breaks. The gap between them is where the hardening happens."

| # | Integration Point | Source Agent(s) | Target Agent(s) | Data Exchanged | Value |
|---|-------------------|----------------|-----------------|----------------|-------|
| 1 | Threat-Informed Architecture | red-recon | eng-architect | Adversary TTPs, threat landscape data, attack surface intelligence | Architecture decisions informed by real adversary behavior rather than theoretical threats; replaces the need for eng-threatintel |
| 2 | Attack Surface Validation | red-recon, red-vuln | eng-infra, eng-devsecops | Validation results against hardened targets, vulnerability scan findings | Validates that infrastructure hardening and security tooling actually reduce the attack surface as intended |
| 3 | Secure Code vs. Exploitation | red-exploit, red-privesc | eng-security, eng-backend, eng-frontend | Exploitation results against reviewed code, bypass demonstrations | Proves whether secure coding practices withstand real exploitation techniques; feedback loop drives hardening |
| 4 | Incident Response Validation | red-persist, red-lateral, red-exfil | eng-incident | Exercise results against response runbooks, detection gaps, evasion successes | Validates IR runbooks against real adversary post-exploitation behavior |

**Evidence:** A-004 R-ROSTER-013 (cross-skill integration establishment); A-002 Finding 7 (Netflix Attack Emulation Team model validates adversarial-collaborative dynamic); S-002 cross-skill integration point definitions.

### 6. Defense Evasion Ownership Model

Defense Evasion (TA0005) is the largest MITRE ATT&CK tactic with 43 techniques and 112 sub-techniques. Following industry practice where evasion is embedded tradecraft rather than a standalone function (A-003, A-004 R-ROSTER-012), defense evasion is distributed across agents:

| Owner | Evasion Domain | Techniques (Representative) |
|-------|---------------|---------------------------|
| red-infra | Tool-level evasion | C2 obfuscation, payload encoding/packing, execution guardrails, sandbox evasion, redirector hardening |
| red-exploit | Execution-time evasion | Process injection, signed binary proxy execution |
| red-privesc | Credential-based evasion | Access token manipulation |
| red-lateral | Network-level evasion | Traffic signaling, protocol tunneling |
| red-persist | Persistence-phase evasion | Indicator removal, rootkits, timestomping |
| red-exfil | Exfiltration-phase evasion | Data encoding, encrypted channels |

**Design rationale:** No elite organization studied staffs a dedicated "evasion specialist." Evasion is embedded in every operator's tradecraft, with infrastructure engineers (red-infra) handling tool-level evasion that cuts across all operations. Each operational agent owns the evasion techniques specific to its kill chain phase. The authorization model (AD-004) must include evasion techniques in each agent's technique allowlist for its operational phase.

**Evidence:** A-003 Finding 5 (Defense Evasion distributed ownership analysis); A-004 R-ROSTER-012 (distributed ownership recommendation); A-002 organizational evidence (no standalone evasion role observed).

### 7. Agent-to-Tool Category Mapping

Each agent has a defined set of tool categories aligned with its capability domain. Actual tool availability depends on adapter implementation (AD-005), engagement configuration, and degradation level (AD-010). Agent logic calls adapters via the common adapter interface (`execute(params) -> StructuredResult | ToolUnavailableError`); agents never invoke tools directly.

#### /eng-team Tool Categories

| Agent | Primary Tool Categories | Example Tools |
|-------|------------------------|---------------|
| eng-architect | Threat modeling, architecture analysis | STRIDE/DREAD templates, architecture diagramming |
| eng-lead | Project planning, standards enforcement | Linting, formatting, dependency analysis |
| eng-backend | SAST, secrets detection, API testing | Semgrep, Gitleaks, OWASP ZAP |
| eng-frontend | Browser security, CSP validation | Lighthouse, CSP Evaluator, DOM analysis |
| eng-infra | IaC scanning, container scanning, SBOM generation | Checkov, Trivy, Syft, CIS-CAT |
| eng-qa | Test execution, fuzzing, coverage | pytest, AFL, coverage.py |
| eng-security | Code analysis, CVE databases | CodeQL, CWE database, NVD |
| eng-reviewer | Quality scoring, standards verification | /adversary integration |
| eng-devsecops | SAST/DAST pipeline, dependency scanning, container scanning | Semgrep CI, Trivy CI, Snyk, Dependabot |
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
| red-exfil | Data transfer, covert channels | Custom exfiltration tools, DNS tunneling |
| red-reporter | Report generation, evidence compilation | Report templates, evidence vault |
| red-infra | C2 frameworks, payload building, redirectors | Cobalt Strike, Sliver, Mythic, redirector configs |
| red-social | Phishing, pretexting | GoPhish, social engineering toolkits |

**Evidence:** S-002 Agent-to-Tool Mapping; C-003 MCP integration patterns (97M+ monthly SDK downloads, 13,000+ servers) and CLI/API adapter architecture; AD-005 common adapter interface design.

### 8. Layered SDLC Governance Model (AD-008)

The /eng-team operates under a five-layer SDLC governance model where each framework serves a distinct, non-overlapping purpose. No single SDLC model covers all requirements; each addresses a different gap.

| Layer | Framework | Purpose | Primary Agents | Scope |
|-------|-----------|---------|----------------|-------|
| 1. Governance | NIST SP 800-218 SSDF | Compliance framework and practice requirements. 4 practice groups (Prepare, Protect, Produce, Respond) with 19 practices and 43 tasks. Methodology-agnostic and outcome-focused. | eng-lead, eng-architect | Full SDLC |
| 2. Lifecycle | Microsoft SDL (5 phases) | Phase-gate workflow structure. Requirements, Design, Implementation, Verification, Release. Maps directly to /eng-team 8-step workflow. | All /eng-team agents | Full SDLC |
| 3. Assessment | OWASP SAMM (3 maturity levels) | Quantitative maturity measurement across 15 security practices in 5 business functions. Level 1 (ad-hoc) minimum, Level 2 (defined) standard, Level 3 (optimized) for C4 engagements. | eng-lead, eng-reviewer | Organizational maturity |
| 4. Supply Chain | Google SLSA (4 build levels) | Build integrity and provenance. Build L2 minimum for production releases (hosted build, signed provenance). Build L3 for C3/C4 engagements (isolated environments). | eng-infra, eng-devsecops | Build and release |
| 5. Automation | DevSecOps patterns | CI/CD pipeline security integration. Automated security gates at every pipeline stage: SAST at build, DAST at test, SCA at build, container scanning at release. | eng-devsecops | CI/CD pipeline |

**SSDF Traceability Requirement:** Every security activity performed by an /eng-team agent includes a reference to the SSDF practice and task it implements (e.g., eng-security code review references PW.7; eng-infra build hardening references PO.5 and PS.2). This provides audit trail from agent outputs to governance framework compliance (F-001 R-SDLC-008).

**Configurability:** Per R-011 (configurable rule sets), users can override the default SDLC model selection. Organizations may substitute BSIMM for SAMM, ISO 27034 for SSDF, or other frameworks through profile cascading (F-001 R-SDLC-007).

**Evidence:** F-001 (5-model comparison with agent workflow mapping); B-003 (OWASP, NIST, CIS, SANS standards analysis with per-agent mapping); S-001 Convergence 2 (supply chain security as critical emerging concern); AD-008 decision record in S-002.

### 9. Threat Modeling Methodology (AD-009)

eng-architect uses STRIDE for threat identification and DREAD for risk scoring as the default threat modeling methodology, with methodology escalation by criticality level:

| Criticality | Methodology | Rationale |
|-------------|-------------|-----------|
| C1 (Routine) | STRIDE only | Sufficient for low-impact, reversible design decisions |
| C2 (Standard) | STRIDE + DREAD scoring | Adds quantitative risk scoring for prioritization |
| C3 (Significant) | STRIDE + DREAD + Attack Trees | Adds complex attack path visualization for multi-step threats |
| C4 (Critical) | STRIDE + DREAD + Attack Trees + PASTA stages 4-7 | Adds business impact analysis for irreversible, high-stakes architecture |
| PII Processing | + LINDDUN | Invoked when system processes PII subject to privacy regulations (GDPR, HIPAA, CCPA) |

**DREAD Subjectivity Mitigation:** DREAD's primary weakness (subjective scoring inconsistency across analysts) is specifically mitigated in the agentic context: (1) eng-architect applies consistent scoring rubrics codified in the agent definition, (2) scoring criteria are expressed as configurable rules, (3) /adversary integration validates scoring consistency for C2+ deliverables, (4) DREAD scores are cross-referenced with CVSS where applicable. Per R-011, users can substitute CVSS-based scoring via configurable rule sets if their organization prefers it (B-004 recommendation).

**Evidence:** B-004 (comparison of STRIDE, DREAD, PASTA, LINDDUN, Attack Trees); S-001 Conflict 4 resolution (DREAD subjectivity mitigated in agentic context); AD-009 decision record in S-002.

### 10. Standalone Capable Design (AD-010)

All 21 agents function without any external tools. Three-level graceful degradation ensures every agent capability works at every level, with reduced evidence quality at lower levels. Tools augment evidence quality; they do not enable reasoning.

| Level | Name | Conditions | Agent Behavior | Evidence Quality |
|-------|------|-----------|----------------|------------------|
| Level 0 | Full Tool Access | All configured tools available via adapters | Optimal evidence-backed analysis with real-time data | Highest -- tool-validated findings |
| Level 1 | Partial Tools | Some tools unavailable (adapter failure, missing configuration) | Analysis with explicit uncertainty markers for gaps where tools would have provided validation | Medium -- partial tool validation with explicit gaps noted |
| Level 2 | Standalone (No Tools) | No external tools available; LLM reasoning only | Full methodology guidance with "unvalidated" markers and manual verification instructions for every claim | Lowest -- LLM knowledge only with verification guidance |

**Design rationale:** This directly follows from AD-001 (methodology-first design). Agents are defined by their knowledge domains and decision-making roles, not by the tools they operate. Stream D (D-002) validated that LLMs reliably perform methodology guidance, code pattern detection, threat modeling facilitation, and report generation without tool augmentation. Tools provide real-time data and evidence validation; the absence of tools degrades evidence quality but does not prevent the agent from providing useful guidance.

**Degradation behavior:** When a tool invocation returns `ToolUnavailableError` from the common adapter interface, the agent: (1) notes the tool gap in its output with an explicit "unvalidated" marker, (2) provides the best analysis possible from LLM knowledge, (3) includes specific manual verification instructions the user can follow, and (4) adjusts its confidence indicators downward for claims that would have been tool-validated.

**Evidence:** C-003 standalone capable design pattern with degradation ladder; S-001 Convergence 1 (methodology-first means agents defined by knowledge, not tools); D-002 (LLMs reliably perform methodology guidance without tools); AD-010 decision record in S-002.

---

## Options Considered

### Sub-Decision: Roster Size (AD-002)

| Option | Description | Verdict |
|--------|-------------|---------|
| Option 1: PLAN.md Baseline | 8 /eng-team + 9 /red-team = 17 agents | REJECTED: Leaves 4 ATT&CK tactics at ZERO or WEAK coverage (TA0042, TA0005, TA0011, TA0040); eng-security overloaded with 3-4 roles; no post-deployment capability |
| **Option 2: Expanded Roster** | **10 /eng-team + 11 /red-team = 21 agents** | **SELECTED: Achieves 14/14 ATT&CK STRONG coverage; decomposes overloaded roles; adds post-deployment (eng-incident) and infrastructure (red-infra) capabilities; validated against 7 elite organizations** |
| Option 3: Full Expansion | 12 /eng-team + 13 /red-team = 25 agents (adds eng-threatintel, eng-compliance, red-opsec, red-cloud) | REJECTED: 4 additional agents fail inclusion criteria -- cross-skill integration covers TI, configurable rules cover compliance, OPSEC decomposes into existing agents, cloud is out of scope |

### Sub-Decision: SDLC Model (AD-008)

| Option | Description | Verdict |
|--------|-------------|---------|
| Option 1: Single Model | MS SDL only as SDLC framework | REJECTED: No supply chain coverage, no maturity assessment, no governance traceability |
| Option 2: Standards Menu | User selects one model per engagement | REJECTED: Models are complementary, not substitutable; each addresses a distinct gap |
| **Option 3: Layered Model** | **Each framework assigned to its area of strength (SSDF governance, SDL lifecycle, SAMM assessment, SLSA supply chain, DevSecOps automation)** | **SELECTED: Non-overlapping purposes; all 5 models converge on supply chain security; each addresses a gap the others miss; configurable per R-011** |

### Sub-Decision: Threat Modeling (AD-009)

| Option | Description | Verdict |
|--------|-------------|---------|
| Option 1: STRIDE Only | Threat identification without quantitative scoring | REJECTED: No risk prioritization capability; cannot rank threats by severity |
| Option 2: STRIDE + CVSS | Industry-standard vulnerability scoring | REJECTED: CVSS is vulnerability-specific, not threat-model-specific; does not score architectural threats |
| Option 3: STRIDE + DREAD | Simple quantitative scoring with agentic mitigation | CONSIDERED: Viable but insufficient for C3/C4 |
| Option 4: PASTA Only | Business-impact-focused threat modeling | REJECTED: Too heavyweight for routine (C1) design decisions |
| **Option 5: Escalating** | **STRIDE+DREAD default with criticality-based escalation to Attack Trees and PASTA** | **SELECTED: Proportional effort -- C1 gets STRIDE, C4 gets full methodology stack; DREAD subjectivity mitigated by agentic consistency; user can substitute CVSS via R-011** |

### Sub-Decision: Tool Dependency (AD-010)

| Option | Description | Verdict |
|--------|-------------|---------|
| Option 1: Tool-Required | Agents fail if tools unavailable | REJECTED: Contradicts methodology-first design (AD-001); creates fragile dependencies on external infrastructure |
| Option 2: Tool-Preferred | Graceful degradation but some capabilities lost entirely | REJECTED: Some agent capabilities becoming unavailable creates unpredictable behavior |
| **Option 3: Standalone Capable** | **Every capability works at all three levels with reduced evidence quality at lower levels** | **SELECTED: Directly follows AD-001; D-002 validates LLM methodology guidance works without tools; every agent retains full reasoning at Level 2 with explicit uncertainty markers** |

### Sub-Decision: Methodology Paradigm (AD-001)

| Option | Description | Verdict |
|--------|-------------|---------|
| Option 1: Autonomous Execution | LLM-driven tool automation executing attacks and builds | REJECTED: D-002 documents 40%+ AI-generated code contains security flaws; LLMs hallucinate CVEs; exploitation requires real-time system interaction LLMs cannot perform; safety alignment blocks direct exploitation (compliance dropped 52% to 28%) |
| **Option 2: Methodology Guidance** | **Every agent provides methodology guidance, structured analysis, and verification instructions; tools augment with real-time data but are never required** | **SELECTED: Highest-confidence finding across all research (S-001 Convergence 1); three independent streams converged; aligns with what LLMs excel at; avoids safety alignment conflicts** |
| Option 3: Hybrid | Execution for some operations, guidance for others | REJECTED: Creates inconsistent user expectations and unclear agent boundaries |

---

## Consequences

### Positive

| Consequence | Impact | Evidence |
|-------------|--------|----------|
| Full ATT&CK coverage | 14/14 tactics at STRONG level; no gaps in offensive methodology coverage | A-004 coverage proof table |
| Elite team parity | Architecture validated against Google, Microsoft, CrowdStrike, Mandiant, TrustedSec, SpecterOps, Rapid7 team structures | A-001, A-002 organizational analysis |
| Clear agent boundaries | Non-overlapping capability domains with explicit "does NOT do" constraints prevent scope creep and routing ambiguity | A-004 boundary definitions; S-002 capability boundary tables |
| Purple team integration | Four formalized integration points operationalize adversarial-collaborative dynamic between skills | A-004 R-ROSTER-013; Netflix model validation |
| Safety alignment compatibility | Methodology-first design avoids most safety alignment conflicts with commercial LLMs | D-002 safety alignment analysis; S-001 Conflict 5 resolution |
| Standalone resilience | All 21 agents function without any external tools, providing value even in constrained environments | C-003 standalone design; D-002 LLM capability validation |
| Governance traceability | Every eng-team security activity traces to SSDF practice IDs, enabling audit compliance | F-001 R-SDLC-008 |
| Configurable methodology | SDLC model, threat modeling approach, and rule sets are all overridable per R-011 | F-001 R-SDLC-007; B-004 CVSS substitution |
| Proportional threat modeling | Criticality-based escalation prevents over-engineering C1 decisions and under-analyzing C4 decisions | B-004 methodology comparison; AD-009 |

### Negative

| Consequence | Impact | Mitigation |
|-------------|--------|------------|
| Roster complexity | 21 agents create routing complexity for skill invocation (FEAT-011 must handle 21 routing targets) | Keyword trigger maps defined per agent in S-002; routing decision table covers common patterns |
| Distributed evasion risk | Defense Evasion spread across 6 agents could lead to coverage gaps or inconsistent evasion quality | red-infra as tool-level evasion owner provides centralized baseline; each agent's technique allowlist includes relevant evasion techniques |
| Cross-skill dependency | Integration points 1 and 3 assume /eng-team and /red-team deploy together | OQ-003 tracks this; eng-threatintel deferred as reconsideration if independent deployment is common |
| Impact split untested | TA0040 shared between red-exploit (technical) and red-reporter (documentation) is logical but unvalidated | OQ-002 tracks this; Phase 5 purple team exercises will validate; fallback is reassigning all Impact to red-exploit |
| DREAD subjectivity residual | Despite agentic mitigation, DREAD scoring may not satisfy organizations that mandate CVSS | R-011 allows CVSS substitution via configurable rule sets |
| 5-layer SDLC overhead | Five governance frameworks create documentation overhead per engagement | Agents automate SSDF traceability; SAMM assessment is optional per engagement; SLSA levels are automated tooling, not manual process |

### Neutral

| Consequence | Impact |
|-------------|--------|
| 4 deferred agents | eng-threatintel, eng-compliance, red-opsec, and red-cloud remain available for future inclusion with clear triggers; no capability is permanently excluded |
| Backward compatibility | Existing 37 Jerry agents are unaffected; portability.enabled defaults to false; PROJ-010 agents use the extended schema |

---

## Evidence Base

Every claim in this ADR traces to a specific Phase 1 research artifact. This section provides the citation index.

### Stream A: Role Completeness

| Artifact | Content | Citations in This ADR |
|----------|---------|----------------------|
| A-001 | Elite engineering team structures: Google (3 security sub-teams, Project Zero 54.2% manual/37.2% fuzzing), Microsoft (SFI, 14 Deputy CISOs, Durability Architects), CrowdStrike (1,778 engineers), Mandiant (IR "team of teams") | eng-devsecops addition, eng-incident addition, eng-security narrowing, security decomposition (Convergence 6) |
| A-002 | Red team patterns: TrustedSec (TRU research unit, engagement lead model), SpecterOps (BloodHound team), Rapid7 (Metasploit team), GitLab (Red Team Developer role), Netflix (Attack Emulation Team), EC Council (social engineering named role), IBM (3 pillars: technical/social/physical) | red-infra addition (4/7 organizations), red-social addition (4/7 organizations), red-lead expansion (CCSAM), red-opsec deferral, cross-skill integration (Netflix model) |
| A-003 | MITRE ATT&CK 14-tactic analysis: 203 techniques, 453 sub-techniques, coverage ratings per agent | ATT&CK coverage proof, Defense Evasion distributed ownership, Impact shared ownership, Resource Development gap, C2 gap |
| A-004 | Final roster with evidence matrix: 21-agent recommendation, 14 numbered recommendations (R-ROSTER-001 through R-ROSTER-014), deferred agents with triggers, cross-skill integration points, ATT&CK coverage before/after comparison | All roster decisions, scope modifications, deferred agents, integration points, non-linear workflow, defense evasion model |

### Stream B: Defensive Methodology

| Artifact | Content | Citations in This ADR |
|----------|---------|----------------------|
| B-003 | OWASP, NIST, CIS, SANS standards analysis with per-agent mapping: OWASP ASVS 5.0 (350 requirements, 17 chapters), OWASP Top 10 2025, CWE Top 25 2025, CIS Benchmarks (100+ guides), NIST CSF 2.0 (6 functions) | /eng-team primary standards assignments, SDLC governance model standards stack |
| B-004 | Threat modeling comparison: STRIDE, DREAD, PASTA, LINDDUN, Attack Trees; DREAD subjectivity analysis and agentic mitigation; criticality-based escalation recommendation | Threat modeling methodology (AD-009), DREAD mitigation rationale, criticality escalation table |

### Stream C: Tool Integration

| Artifact | Content | Citations in This ADR |
|----------|---------|----------------------|
| C-003 | MCP integration (97M+ SDK downloads, 13,000+ servers, 6 security MCP servers validated), common adapter interface, SARIF normalization, standalone capable design, security controls | Tool category mapping, standalone design (AD-010), degradation levels, common adapter interface |

### Stream D: LLM Boundaries

| Artifact | Content | Citations in This ADR |
|----------|---------|----------------------|
| D-002 | LLM capability matrix: 40%+ AI code contains flaws, NVD backlog worsened by false CVEs, safety alignment compliance dropped 52% to 28%, IRIS+GPT-4 2x CodeQL detection, Sec-Gemini 7x analyst time reduction, Wiz Arena confirms scaffold matters | Methodology-first design (AD-001), standalone capable (AD-010), safety alignment compatibility |

### Stream E: LLM Portability

| Artifact | Content | Citations in This ADR |
|----------|---------|----------------------|
| E-001 | Universal prompt patterns (RCCF), XML as Anthropic-specific anti-pattern, CoT model-dependence, JSON Schema convergence | Agent identity schema (body_format, reasoning_strategy) |
| E-002 | Framework analysis: CrewAI, LangChain, DSPy, Google ADK, Haystack, LiteLLM -- agent-as-configuration convergence | Agent identity schema design rationale |
| E-003 | Two-layer architecture, portable agent schema (38 fields, 63/24/13 portability split), 4 provider adapters, 18 validation criteria, backward compatibility | Full agent identity schema specification, portability fields |

### Stream F: Secure SDLC and Authorization

| Artifact | Content | Citations in This ADR |
|----------|---------|----------------------|
| F-001 | MS SDL (5 phases, 10 practices, continuous evolution), NIST SSDF (4 groups, 19 practices, v1.2 draft), OWASP SAMM (5 functions, 15 practices, 3 levels), Google SLSA (4 build levels), DevSecOps (pipeline stages with tooling) | Layered SDLC governance (AD-008), agent workflow mapping, SSDF traceability requirement |
| F-002 | Three-layer authorization architecture, OWASP Agentic AI Top 10 mapping (ASI01-ASI10), scope enforcement components, per-agent authorization levels, circuit breakers, progressive autonomy | /red-team handoff protocol (circuit breakers, scope revalidation, audit trail) |

### Synthesis Artifacts

| Artifact | Content | Citations in This ADR |
|----------|---------|----------------------|
| S-001 | Cross-stream findings: 6 convergence patterns, 5 conflict resolutions, requirements traceability (R-001 through R-024) | Convergence 1 (methodology-first), Convergence 2 (supply chain), Convergence 4 (configurable rules over compliance agent), Convergence 5 (JSON Schema), Convergence 6 (security decomposition); Conflict 1-5 resolutions |
| S-002 | Architecture implications: 12 architecture decisions (AD-001 through AD-012), agent identity schema, capability boundaries, handoff protocols, tool mappings, cross-cutting concerns | AD-001, AD-002, AD-008, AD-009, AD-010 specifications; agent boundary tables; defense evasion ownership model; safety alignment compatibility |

---

## Compliance

### Jerry Framework Compliance

| Constraint | Status | Implementation |
|------------|--------|----------------|
| P-003: No Recursive Subagents (H-01) | COMPLIANT | All workflows operate within orchestrator -> worker pattern. /eng-team sequential workflow and /red-team non-linear workflow both use single-level agent invocation. No agent spawns sub-agents. |
| P-020: User Authority (H-02) | COMPLIANT | ADR status is PROPOSED pending user ratification. All architecture decisions presented as recommendations. Configurable rule sets (R-011) ensure users can override methodology selections. |
| P-022: No Deception (H-03) | COMPLIANT | Standalone design (AD-010) requires explicit "unvalidated" markers when tools are unavailable. Agents never present LLM-generated findings as tool-validated ground truth. Confidence indicators adjust downward for unverified claims. |

### PROJ-010 Requirement Compliance

| Requirement | Status | Implementation |
|-------------|--------|----------------|
| R-001: Secure by Design | COMPLIANT | Security is distributed across all agents (Convergence 6), not concentrated in eng-security. Layered SDLC governance (AD-008) embeds security at every phase. Threat modeling (AD-009) is a design-time activity. |
| R-008: Role Completeness Analysis | COMPLIANT | Gap analysis against 7 elite organizations documented in A-001, A-002. ATT&CK 14/14 coverage proven in A-004. 4 deferred agents with triggers preserve extension paths. |
| R-010: LLM Portability | COMPLIANT | Agent identity schema from E-003 with 63% fully portable fields. `body_format: markdown` as portable default. `portability.enabled` for cross-provider validation. |
| R-012: Tool Integration Architecture | COMPLIANT | Standalone capable design (AD-010) ensures all 21 agents function without tools. Three-level degradation with explicit uncertainty markers. |
| R-013: C4 /adversary on Every Phase | COMPLIANT | eng-reviewer integrates /adversary for C2+ deliverables. Quality threshold >= 0.95 for PROJ-010. red-reporter outputs go through /adversary for quality scoring. |
| R-017: Industry Leader Standard | COMPLIANT | Validated against Google, Microsoft, CrowdStrike, Mandiant (engineering), TrustedSec, SpecterOps, Rapid7, Netflix (red team). 130+ unique sources across 6 R-006 categories. |
| R-018: Real Offensive Techniques | COMPLIANT | 14/14 ATT&CK tactic coverage at STRONG level. PTES/OSSTMM methodology. Technique-level agent mapping in A-003/A-004. Methodology-first design compatible with safety alignment. |
| R-022: Agent Development Standards | COMPLIANT | Portable agent schema from E-003 with identity, capability, and portability fields. RCCF prompt pattern for system prompt assembly. |

---

## Related Decisions

### Decisions Formalized in This ADR

| Decision | Title | Section |
|----------|-------|---------|
| AD-001 | Methodology-First Design Paradigm | [Options: Methodology Paradigm](#sub-decision-methodology-paradigm-ad-001), [Decision: Standalone Capable](#10-standalone-capable-design-ad-010) |
| AD-002 | 21-Agent Roster (10 /eng-team + 11 /red-team) | [Decision: Roster](#2-the-21-agent-roster-with-capability-boundaries), [Options: Roster Size](#sub-decision-roster-size-ad-002) |
| AD-008 | Layered SDLC Governance Model | [Decision: SDLC](#8-layered-sdlc-governance-model-ad-008), [Options: SDLC Model](#sub-decision-sdlc-model-ad-008) |
| AD-009 | STRIDE+DREAD Default Threat Modeling with Criticality Escalation | [Decision: Threat Modeling](#9-threat-modeling-methodology-ad-009), [Options: Threat Modeling](#sub-decision-threat-modeling-ad-009) |
| AD-010 | Standalone Capable Design with Three-Level Degradation | [Decision: Standalone](#10-standalone-capable-design-ad-010), [Options: Tool Dependency](#sub-decision-tool-dependency-ad-010) |

### Related Decisions Not in This ADR

| Decision | Title | Relationship | ADR |
|----------|-------|-------------|-----|
| AD-003 | Two-Layer LLM Portability Architecture | Defines the rendering layer that transforms agent definitions into provider-specific prompts; agent identity schema in this ADR is the semantic layer input | Future ADR for FEAT-012 |
| AD-004 | Three-Layer Authorization Architecture | Defines the scope enforcement infrastructure that constrains /red-team agent operations; this ADR's handoff protocols reference AD-004's circuit breakers and scope validation | Future ADR for FEAT-015 |
| AD-005 | MCP-Primary Tool Integration | Defines the adapter interface that this ADR's tool category mapping feeds into; agents call adapters, not tools directly | Future ADR for FEAT-014 |
| AD-006 | SARIF-Based Finding Normalization | Defines the finding format that /eng-team and /red-team agents produce and consume | Future ADR for FEAT-014 |
| AD-007 | YAML-First Configurable Rule Sets | Defines the profile management system that enables R-011 methodology overrides referenced in this ADR | Future ADR for FEAT-013 |
| AD-011 | Agent Isolation Architecture | Defines the container/VM isolation boundaries for agent execution; affects cross-skill integration feasibility | Future ADR for FEAT-015 |
| AD-012 | Progressive Autonomy Deployment Model | Defines the autonomy levels for /red-team operations; affects how handoff protocols enforce human oversight | Future ADR for FEAT-015 |

---

## Open Questions

### OQ-002: Impact Technique Ownership Validation

**Context:** This ADR resolves Impact (TA0040) as shared: red-exploit owns technical demonstration, red-reporter owns documentation and stakeholder communication (S-001 Conflict 2 resolution). This split follows the natural boundary between technical capability and communication.

**Confidence:** MEDIUM. The split is logical but untested in the agent architecture.

**What must be validated:** Phase 5 purple team exercises should test whether the red-exploit-to-red-reporter handoff for Impact findings creates friction. If the split causes information loss or handoff delays, consider reassigning all Impact to red-exploit with red-reporter consuming the output as read-only evidence.

**Evidence:** A-003 Finding 6 (14 Impact techniques with zero explicit coverage in baseline); A-004 R-ROSTER-011 (shared ownership recommendation).

### OQ-003: Cross-Skill Deployment Independence

**Context:** This ADR's cross-skill integration points (especially Integration Point 1: Threat-Informed Architecture, where red-recon feeds eng-architect) assume /eng-team and /red-team deploy together. If independent deployment is common, eng-threatintel may need to be promoted from deferred status.

**Confidence:** MEDIUM. Depends on the assumption of co-deployment.

**What must be decided:** Whether the architecture assumes co-deployment of both skills or must support independent operation. If independent: eng-threatintel becomes a required agent for standalone /eng-team deployment. If co-deployed: cross-skill integration points satisfy the threat intelligence requirement without function duplication.

**Evidence:** S-001 Conflict 3 (threat intelligence -- dedicated agent vs. cross-skill integration); A-004 R-ROSTER-005 (eng-threatintel deferral with trigger).

---

## References

### Primary Research Artifacts

| ID | Title | Location |
|----|-------|----------|
| S-002 | Architecture Implications Synthesis | `work/research/synthesis/S-002-architecture-implications.md` |
| S-001 | Cross-Stream Findings Consolidation | `work/research/synthesis/S-001-cross-stream-findings.md` |
| A-004 | Final Roster Recommendation with Gap Analysis | `work/research/stream-a-role-completeness/A-004-roster-recommendation.md` |
| A-001 | Elite Engineering Team Research | `work/research/stream-a-role-completeness/A-001-engineering-team-patterns.md` |
| A-002 | Red Team Organization Research | `work/research/stream-a-role-completeness/A-002-red-team-patterns.md` |
| A-003 | MITRE ATT&CK Coverage Analysis | `work/research/stream-a-role-completeness/A-003-attack-coverage.md` |
| B-003 | Defensive Standards Analysis | `work/research/stream-b-defensive-methodology/B-003-standards-analysis.md` |
| B-004 | Threat Modeling Comparison | `work/research/stream-b-defensive-methodology/B-004-threat-modeling.md` |
| C-003 | Tool Integration Architecture | `work/research/stream-c-tool-integration/C-003-tool-architecture.md` |
| D-002 | LLM Capability Boundaries | `work/research/stream-d-llm-boundaries/D-002-capability-matrix.md` |
| E-001 | Universal Prompt Patterns | `work/research/stream-e-llm-portability/E-001-prompt-patterns.md` |
| E-002 | Framework Analysis | `work/research/stream-e-llm-portability/E-002-framework-analysis.md` |
| E-003 | Portability Architecture | `work/research/stream-e-llm-portability/E-003-portability-architecture.md` |
| F-001 | Secure SDLC Lifecycle Patterns | `work/research/stream-f-secure-sdlc/F-001-secure-sdlc-patterns.md` |
| F-002 | Authorization and Scope Control | `work/research/stream-f-secure-sdlc/F-002-authorization-architecture.md` |

### External Standards

| Standard | Version | Usage in This ADR |
|----------|---------|-------------------|
| MITRE ATT&CK Enterprise | 2025 | 14-tactic coverage proof, agent-to-tactic mapping |
| NIST SP 800-218 SSDF | v1.1 (v1.2 draft Dec 2025) | Governance layer of SDLC model |
| Microsoft SDL | 2024 (Continuous SDL) | Lifecycle layer of SDLC model |
| OWASP SAMM | v2 | Assessment layer of SDLC model |
| Google SLSA | v1.0 | Supply chain layer of SDLC model |
| OWASP ASVS | 5.0 | /eng-team verification standard |
| OWASP Top 10 | 2025 | /eng-team awareness standard |
| CWE Top 25 | 2025 | eng-security code review focus |
| CIS Benchmarks | 2025 | eng-infra hardening standard |
| NIST CSF | 2.0 | eng-architect governance standard |
| PTES | Current | /red-team engagement methodology |
| OSSTMM | Current | /red-team engagement methodology |
| OWASP Testing Guide | Current | /red-team and eng-qa testing methodology |

### Organizational Evidence

| Organization | Type | Evidence Used |
|-------------|------|---------------|
| Google | Elite engineering | Chrome Security 3 sub-teams, Project Zero methodology, SPA Research |
| Microsoft | Elite engineering | SFI, 14 Deputy CISOs, SDL evolution, MSRC incident response |
| CrowdStrike | Elite engineering | 1,778 engineers, Falcon Intelligence |
| Mandiant | Elite engineering | IR "team of teams", threat intelligence |
| TrustedSec | Elite red team | TRU research unit, engagement lead model, social engineering |
| SpecterOps | Elite red team | BloodHound team, RTO training |
| Rapid7 | Elite red team | Metasploit team, PTES methodology |
| Netflix | Elite purple team | Attack Emulation Team, control confidence measurement |
| GitLab | Red team structure | Full career ladder, Red Team Developer role |
| EC Council | Certification body | Red team role taxonomy |
