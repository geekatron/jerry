# PROJ-008: Agentic Security

> Mission-critical security-first agentic platform. Competitive gap analysis and hardening of Jerry Framework to crush all competition in the agentic ecosystem.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Objective](#objective) | Project goals and vision |
| [Scope](#scope) | What's in and out of scope |
| [Framework Scope](#framework-scope) | MITRE, OWASP, NIST framework decisions |
| [Research Targets](#research-targets) | Competitive landscape and security analysis targets |
| [Phases](#phases) | High-level execution phases |
| [Phase Details](#phase-details) | Detailed phase breakdown with skill assignments |
| [Phase Gate Criteria](#phase-gate-criteria) | Transition requirements between phases |
| [Orchestration](#orchestration) | Multi-pipeline workflow coordination |
| [Worktracker Decomposition](#worktracker-decomposition) | Epic/Feature hierarchy overview |
| [Success Criteria](#success-criteria) | How we measure success |
| [Risk Register](#risk-register) | Project-level risks |

---

## Objective

Make Jerry the most secure, highest-quality agentic framework available. Enable anyone with an idea to bring it to fruition without worrying about security issues or bad practices. Security and quality are first-class concerns, not afterthoughts.

**Core thesis:** The agentic ecosystem is rife with security nightmares (OpenClaw/Clawdbot being the poster child). Jerry already has governance, quality enforcement, and constitutional constraints. We need to extend this foundation into a comprehensive security-first agent platform that is future-proof and sets the standard for the industry.

**Differentiator:** We don't just defend -- we consume MITRE ATT&CK, MITRE ATLAS, OWASP, and NIST as active allies. Every known adversary technique becomes a test case. Every compliance control becomes a verification target.

---

## Scope

### In Scope

- Deep competitive research: OpenClaw/Clawdbot, Claude Agent SDK, claude-flow, Cline, and emerging agentic frameworks
- Security gap analysis: Jerry vs. industry threats (prompt injection, credential exposure, supply chain attacks, SSRF, RCE, auth bypass)
- Security architecture: Deterministic action verification, privilege isolation, behavioral sandboxing, supply chain verification
- Jerry hardening: Extend governance/quality framework with security-specific controls
- Skill/agent security model: Secure-by-default skill execution, permission boundaries, audit trails
- Future-proofing: Extensible security model that scales with new threat vectors
- Compliance mapping: Full coverage of MITRE, OWASP, and NIST frameworks

### Out of Scope

- Building a competing product from scratch (we extend Jerry)
- Cloud hosting / SaaS deployment (Jerry is local-first)
- Marketing / branding (separate concern)
- Runtime monitoring / SIEM integration (future project)

---

## Framework Scope

Confirmed scope decisions for threat framework consumption:

### MITRE Frameworks

| Framework | Scope | Relevance to Agentic Systems |
|-----------|-------|------------------------------|
| **ATT&CK Enterprise** | 14 tactics, full technique matrix | Traditional adversary behaviors: initial access, execution, persistence, privilege escalation, defense evasion, credential access, discovery, lateral movement, collection, C2, exfiltration, impact |
| **ATLAS** (Adversarial Threat Landscape for AI Systems) | AI/ML-specific tactics and techniques | Prompt injection, model manipulation, training data poisoning, ML supply chain, model evasion, AI-specific reconnaissance |
| **ATT&CK Mobile** | Mobile-specific tactics | Mobile agent deployment scenarios, mobile app security models |

### OWASP Frameworks

| Framework | Items | Relevance to Agentic Systems |
|-----------|-------|------------------------------|
| **LLM Top 10 (2025)** | LLM01-LLM10 | Prompt injection, sensitive info disclosure, supply chain, data poisoning, improper output handling, excessive agency, system prompt leakage, vector/embedding weaknesses, misinformation, unbounded consumption |
| **Agentic Top 10 (2026)** | ASI01-ASI10 | Agent goal hijack, tool misuse, privilege escalation, delegated trust boundary violations, memory/context manipulation, identity/access mismanagement, insecure inter-agent communication, cascading failures, insufficient logging, rogue agents |
| **API Security Top 10** | API1-API10 | Broken auth, broken object-level auth, excessive data exposure, lack of resources/rate limiting, broken function-level auth, mass assignment, SSRF, security misconfiguration, improper asset management, unsafe API consumption |
| **Web Top 10** | A01-A10 | Broken access control, cryptographic failures, injection, insecure design, security misconfiguration, vulnerable components, auth failures, data integrity failures, logging failures, SSRF |

### NIST Frameworks

| Framework | Scope | Relevance to Agentic Systems |
|-----------|-------|------------------------------|
| **AI RMF (600-1)** | AI risk management framework | AI-specific risk governance: MAP, MEASURE, MANAGE, GOVERN functions |
| **CSF 2.0** | Cybersecurity framework | Foundational security: Identify, Protect, Detect, Respond, Recover, Govern |
| **SP 800-53** | Security controls catalog | Technical + organizational controls: access control, audit, configuration, incident response, system protection |

---

## Research Targets

| Target | Focus Area |
|--------|------------|
| OpenClaw/Clawdbot | Security failures: CVE-2026-25253 (RCE), auth bypass, SSRF, supply chain poisoning, prompt injection, credential leakage |
| Claude Agent SDK | Official Anthropic patterns, security model, tool execution sandboxing |
| Claude Code | Permission model, hooks, sandbox, tool approval workflow |
| claude-flow | Multi-agent orchestration security, swarm coordination risks |
| Cline (claude-dev) | VS Code extension security model, user approval patterns |
| Microsoft guidance | Identity isolation, runtime risk, control/data plane separation |
| Cisco analysis | Agent architecture weaknesses, secure framework requirements |

---

## Phases

| Phase | Name | Description | PS Pipeline | NSE Pipeline |
|-------|------|-------------|-------------|--------------|
| 1 | Deep Research | Competitive landscape, threat framework consumption, gap analysis | Competitive analysis, framework consumption, gap analysis | Requirements discovery, risk register |
| 2 | Architecture | Security architecture design, threat model, ADRs | Architecture design, pattern research | Formal architecture, requirements baseline, trade studies |
| 3 | Implementation | Security controls, hardening, skill security model | Implementation specs, code review | Implementation V&V, integration verification |
| 4 | Verification | Security testing, adversarial review, compliance verification | Adversarial testing, red team | V&V execution, compliance matrices |
| 5 | Documentation | Security guide, best practices, compliance reports | Best practices synthesis, security guide | Compliance documentation |

---

## Phase Details

### Phase 1: Deep Research (PS) / Requirements Discovery (NSE)

**Objective:** Comprehensive understanding of the agentic security landscape, threat frameworks, and Jerry's current posture.

**PS Pipeline (3 agents):**
- **ps-researcher-001**: Competitive landscape analysis across all 7 research targets
- **ps-researcher-002**: Consumption of all 9 framework scopes (MITRE ATT&CK/ATLAS/Mobile + OWASP LLM/API/Web + NIST AI RMF/CSF/800-53)
- **ps-analyst-001**: Gap analysis -- Jerry current posture vs. all threat frameworks, producing a risk-prioritized gap matrix

**NSE Pipeline (2 agents):**
- **nse-requirements-001**: Security requirements discovery -- functional and non-functional requirements derived from threat frameworks
- **nse-explorer-001**: Initial risk register -- FMEA-style analysis of agentic security threats with RPN scoring

**Deliverables:** Competitive landscape report, threat framework analysis, gap analysis, security requirements, risk register

### Phase 2: Architecture (PS) / Formal Design (NSE)

**Objective:** Security architecture design informed by Phase 1 research, with formal requirements and trade-off analysis.

**PS Pipeline (2 agents):**
- **ps-architect-001**: Security architecture -- zero-trust skill execution, privilege isolation, deterministic verification (L3/L5), supply chain security
- **ps-researcher-003**: Security pattern research -- industry patterns, defense-in-depth models, secure agent framework patterns

**NSE Pipeline (3 agents):**
- **nse-architecture-001**: Formal architecture -- NPR 7123.1D compliant design with interface definitions
- **nse-requirements-002**: Requirements baseline -- frozen requirements with bi-directional traceability matrix
- **nse-explorer-002**: Trade studies -- security vs. performance, usability vs. restriction, coverage vs. complexity

**Deliverables:** Security architecture document, ADR series, formal architecture, requirements baseline, trade studies

### Phase 3: Implementation (PS) / Integration Verification (NSE)

**Objective:** Implement security controls and verify integration with existing Jerry framework.

**PS Pipeline (2 agents):**
- **ps-analyst-002**: Implementation specifications -- detailed specs for each security control
- **ps-critic-001**: Security code review -- review all implemented controls against architecture

**NSE Pipeline (2 agents):**
- **nse-verification-001**: Implementation V&V -- verify controls against requirements baseline
- **nse-integration-001**: Integration verification -- confirm security controls integrate correctly with existing Jerry governance

**Deliverables:** Implementation specs, security review, V&V report, integration report

### Phase 4: Adversarial Verification (PS) / Compliance Verification (NSE)

**Objective:** Adversarial testing of security posture and compliance verification against all frameworks.

**PS Pipeline (2 agents):**
- **ps-investigator-001**: Adversarial testing -- prompt injection attacks, privilege escalation attempts, supply chain attack simulation
- **ps-reviewer-001**: Red team review -- S-001 Red Team + S-012 FMEA + S-004 Pre-Mortem against full security architecture

**NSE Pipeline (2 agents):**
- **nse-verification-002**: V&V execution -- complete verification matrix with all requirements traced to evidence
- **nse-verification-003**: Compliance verification -- MITRE ATT&CK coverage, OWASP compliance, NIST controls compliance

**Deliverables:** Adversarial test results, red team report, V&V matrix, compliance matrices (MITRE, OWASP, NIST)

### Phase 5: Documentation (PS) / Compliance Documentation (NSE)

**Objective:** Publish security guides, developer standards, and compliance reports.

**PS Pipeline (2 agents):**
- **ps-synthesizer-001**: Best practices synthesis -- unified security posture, lessons learned, industry positioning
- **ps-reporter-001**: Security guide -- Jerry Security Architecture Guide, Secure Development Guides, Incident Response Playbook

**NSE Pipeline (1 agent):**
- **nse-verification-004**: Compliance documentation -- MITRE ATT&CK coverage report, OWASP compliance report, NIST compliance report

**Deliverables:** Security guide, developer standards, compliance reports, final synthesis

---

## Phase Gate Criteria

| Gate | Transition | Key Criteria |
|------|-----------|--------------|
| Gate 1 | Research → Architecture | All competitive analyses + framework consumption complete; gap analysis with risk priorities; initial requirements + risk register; C4 tournament quality >= 0.95 (all 10 strategies) |
| Gate 2 | Architecture → Implementation | Threat model (STRIDE/DREAD) complete; architecture documented with ADRs; requirements baselined; SRR/PDR review passed; C4 tournament quality >= 0.95 |
| Gate 3 | Implementation → Verification | All controls implemented; agent/skill security operational; code review with zero critical findings; V&V against requirements; CDR passed; C4 tournament quality >= 0.95 |
| Gate 4 | Verification → Documentation | Adversarial testing complete; red team review complete; compliance matrices verified; zero critical/high unresolved; TRR passed; C4 tournament quality >= 0.95 |
| Gate 5 | Documentation → Complete | Security guide published; developer standards published; compliance reports finalized; final synthesis complete; C4 tournament quality >= 0.95 |

---

## Orchestration

**Workflow ID:** `agentic-sec-20260222-001`
**Pattern:** Cross-Pollinated Pipeline (5 phases, 4 sync barriers)
**Pipelines:** PS (problem-solving) + NSE (nasa-se)
**Criticality:** C4 (Mission-Critical: irreversible architecture/governance, AE-005 security-critical)

**Orchestration Artifacts:**
- `orchestration/agentic-sec-20260222-001/ORCHESTRATION_PLAN.md` -- Strategic context
- `orchestration/agentic-sec-20260222-001/ORCHESTRATION.yaml` -- Machine-readable state (SSOT)
- `orchestration/agentic-sec-20260222-001/ORCHESTRATION_WORKTRACKER.md` -- Execution tracking

**Skills Involved:**

| Skill | Role | Phases |
|-------|------|--------|
| /orchestration | Workflow coordination, state tracking | All |
| /problem-solving | Research, analysis, architecture, adversarial, documentation | 1-5 (PS pipeline) |
| /nasa-se | Requirements, V&V, compliance, formal design | 1-5 (NSE pipeline) |
| /worktracker | Work item management, progress tracking | All |
| /adversary | Adversarial strategies at quality gates | Phase 4, all barriers |

---

## Worktracker Decomposition

### Epic Hierarchy

| Epic | Name | Phase | Features |
|------|------|-------|----------|
| EPIC-001 | Security Research & Threat Intelligence | 1 | FEAT-001 (Competitive), FEAT-002 (Frameworks), FEAT-003 (Gap Analysis) |
| EPIC-002 | Security Architecture Design | 2 | FEAT-004 (Threat Model), FEAT-005 (Architecture), FEAT-006 (Requirements) |
| EPIC-003 | Security Controls Implementation | 3 | FEAT-007 (Governance), FEAT-008 (Agent Security), FEAT-009 (Skill Security), FEAT-010 (Infrastructure) |
| EPIC-004 | Security Verification & Validation | 4 | FEAT-011 (Testing), FEAT-012 (Adversarial), FEAT-013 (Compliance) |
| EPIC-005 | Security Documentation & Standards | 5 | FEAT-014 (Security Guide), FEAT-015 (Dev Standards), FEAT-016 (Compliance Docs) |

### Feature Breakdown

See `WORKTRACKER.md` for full decomposition with Stories and Tasks per Feature.

---

## Success Criteria

1. Comprehensive threat model covering all known agentic attack vectors
2. Jerry security architecture that addresses every OpenClaw failure mode
3. Deterministic security controls (not just guidelines) enforced at L3/L5
4. Zero-trust skill execution model with cryptographic verification
5. Quality gate score >= 0.95 on all security deliverables (C4 tournament mode, all 10 adversarial strategies)
6. Security-first documentation that enables safe community contributions
7. Full coverage mapping against MITRE ATT&CK Enterprise + ATLAS + Mobile
8. Full compliance mapping against OWASP LLM + API + Web Top 10
9. Full compliance mapping against NIST AI RMF + CSF 2.0 + SP 800-53
10. Industry-leading security posture verified through adversarial testing (S-001 Red Team)

---

## Risk Register

| ID | Risk | Likelihood | Impact | Mitigation |
|----|------|------------|--------|------------|
| R-001 | Context rot during long research phases | High | High | Checkpoint at phase boundaries; session restart between phases |
| R-002 | Framework scope creep (MITRE+OWASP+NIST is vast) | High | Medium | Strict scope; time-box each framework; focus on agentic-relevant controls |
| R-003 | Competitive landscape evolves during project | Medium | Medium | Time-bound research to Phase 1; extensible architecture |
| R-004 | Security controls conflict with usability | Medium | High | Trade studies in Phase 2; user authority on trade-offs |
| R-005 | Quality gate bottleneck at barriers | Medium | Medium | 3-iteration max per barrier; escalate to user |
| R-006 | MITRE ATLAS coverage gaps | Medium | Medium | Supplement with academic research; note gaps |
| R-007 | Implementation impacts existing functionality | Low | High | Integration V&V in Phase 3; regression testing |
| R-008 | Token exhaustion during adversarial testing | Medium | High | Session partitioning; checkpoint before each adversarial run |

---

## Data Source Registry

All Phase 1 agents MUST consume data from the verified sources in:
`work/EPIC-001-security-research/FEAT-002-threat-frameworks/data-sources.md`

Key repositories to clone and consume programmatically:

| Source | Repository | Format |
|--------|-----------|--------|
| ATT&CK Enterprise | `mitre-attack/attack-stix-data` | STIX 2.1 JSON |
| ATT&CK Python API | `mitre-attack/mitreattack-python` | Python library |
| ATLAS (AI threats) | `mitre-atlas/atlas-data` | YAML + STIX 2.1 |
| D3FEND (defenses) | `d3fend/d3fend-ontology` | OWL ontology |
| SP 800-53 Controls | `usnistgov/oscal-content` | JSON/YAML/XML |
| OWASP LLM Top 10 | `OWASP/www-project-top-10-for-large-language-model-applications` | Markdown/PDF |
| OWASP Agentic Top 10 | `genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/` | Web/PDF |
| OWASP API Security | `OWASP/API-Security` | Markdown |
| Cross-Framework Mapping | `emmanuelgjr/owaspllmtop10mapping` | Spreadsheets |
| ATT&CK-to-Controls Mapping | `center-for-threat-informed-defense/mappings-explorer` | Structured data |
