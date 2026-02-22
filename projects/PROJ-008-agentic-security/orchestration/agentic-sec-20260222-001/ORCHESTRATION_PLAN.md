# ORCHESTRATION_PLAN.md

> **Document ID:** PROJ-008-ORCH-PLAN
> **Project:** PROJ-008-agentic-security
> **Workflow ID:** `agentic-sec-20260222-001`
> **Status:** ACTIVE
> **Version:** 2.0
> **Created:** 2026-02-22
> **Last Updated:** 2026-02-22

## Document Sections

| Section | Purpose |
|---------|---------|
| [Executive Summary](#1-executive-summary) | Workflow overview and identification |
| [Workflow Architecture](#2-workflow-architecture) | Pipeline diagram and pattern classification |
| [Phase Definitions](#3-phase-definitions) | Per-phase agent assignments and deliverables |
| [Sync Barrier Protocol](#4-sync-barrier-protocol) | Cross-pollination rules and artifacts |
| [Phase Gate Criteria](#5-phase-gate-criteria) | Transition requirements between phases |
| [Agent Registry](#6-agent-registry) | All agents across both pipelines |
| [Skill Routing Map](#7-skill-routing-map) | Which skill handles which work |
| [State Management](#8-state-management) | Artifact paths and checkpoint strategy |
| [Execution Constraints](#9-execution-constraints) | Constitutional and operational constraints |
| [Risk Register](#10-risk-register) | Project-level risks and mitigations |
| [Resumption Context](#11-resumption-context) | Current state and next actions |

---

## 1. Executive Summary

**Mission:** Make Jerry the most secure, highest-quality agentic framework on the market. Consume MITRE ATT&CK, MITRE ATLAS, OWASP (LLM/API/Web Top 10), and NIST (AI RMF/CSF 2.0/SP 800-53) as defensive allies. Set the industry standard that others benchmark against.

**Current State:** Planning complete. Awaiting Phase 1 execution kickoff.

**Orchestration Pattern:** Cross-Pollinated Pipeline (5 phases, 4 barriers)

**Criticality:** C4 (Mission-Critical: irreversible architecture/governance, AE-005 security-critical)

**Quality Threshold:** >= 0.95 weighted composite (elevated above standard 0.92 per user directive)

**Adversarial Strategy Set:** ALL 10 selected strategies (C4 tournament mode)

**Iteration Ceiling:** 5 iterations per quality gate (creator → critic → revision)

**Agent Execution Model:** Background agents (Task tool) with structured feedback to creator for revision

### 1.1 Workflow Identification

| Field | Value | Source |
|-------|-------|--------|
| Workflow ID | `agentic-sec-20260222-001` | auto |
| ID Format | `{purpose}-{YYYYMMDD}-{NNN}` | semantic-date-seq |
| Base Path | `orchestration/agentic-sec-20260222-001/` | Dynamic |

**Artifact Output Locations:**
- Pipeline PS: `orchestration/agentic-sec-20260222-001/ps/`
- Pipeline NSE: `orchestration/agentic-sec-20260222-001/nse/`
- Cross-pollination: `orchestration/agentic-sec-20260222-001/cross-pollination/`

### 1.2 Framework Scope (User-Confirmed)

| Framework | Scope | Items |
|-----------|-------|-------|
| MITRE ATT&CK Enterprise | 14 tactics, full technique matrix | Enterprise adversary behaviors |
| MITRE ATLAS | AI/ML-specific tactics and techniques | Adversarial ML, prompt injection, model manipulation |
| MITRE ATT&CK Mobile | Mobile-specific tactics | Mobile agent deployment risks |
| OWASP LLM Top 10 (2025) | 10 LLM-specific risks | Prompt injection, excessive agency, supply chain |
| OWASP API Security Top 10 | 10 API-specific risks | Broken auth, injection, SSRF |
| OWASP Web Top 10 | 10 web-specific risks | Injection, XSS, access control |
| NIST AI RMF (600-1) | AI risk management framework | AI-specific risk governance |
| NIST CSF 2.0 | Cybersecurity framework | Identify, Protect, Detect, Respond, Recover |
| NIST SP 800-53 | Security controls catalog | Technical and organizational controls |

---

## 2. Workflow Architecture

### 2.1 Pipeline Diagram

```
    PS PIPELINE (Problem-Solving)                  NSE PIPELINE (NASA-SE)
    ════════════════════════════                    ═══════════════════════

┌───────────────────────────────┐              ┌───────────────────────────────┐
│ PHASE 1: DEEP RESEARCH        │              │ PHASE 1: REQUIREMENTS         │
│ ───────────────────────────── │              │   DISCOVERY                   │
│ • ps-researcher-001           │              │ ───────────────────────────── │
│   (competitive landscape)     │              │ • nse-requirements-001        │
│ • ps-researcher-002           │              │   (security requirements)     │
│   (threat framework           │              │ • nse-explorer-001            │
│    consumption)               │              │   (risk register)             │
│ • ps-analyst-001              │              │                               │
│   (gap analysis)              │              │                               │
│ STATUS: PENDING               │              │ STATUS: PENDING               │
└──────────────┬────────────────┘              └──────────────┬────────────────┘
               │                                              │
               ▼                                              ▼
    ╔══════════════════════════════════════════════════════════════════════╗
    ║                         SYNC BARRIER 1                              ║
    ║  ┌────────────────────────────────────────────────────────────────┐ ║
    ║  │ ps→nse: Research findings, threat maps, gap priorities        │ ║
    ║  │ nse→ps: Requirements gaps, risk-driven research priorities    │ ║
    ║  └────────────────────────────────────────────────────────────────┘ ║
    ║  QUALITY GATE: >= 0.95 (S-014 + S-002 + S-007)                    ║
    ╚══════════════════════════════════════════════════════════════════════╝
               │                                              │
               ▼                                              ▼
┌───────────────────────────────┐              ┌───────────────────────────────┐
│ PHASE 2: ARCHITECTURE         │              │ PHASE 2: FORMAL DESIGN        │
│ ───────────────────────────── │              │ ───────────────────────────── │
│ • ps-architect-001            │              │ • nse-architecture-001        │
│   (security architecture)     │              │   (formal architecture)       │
│ • ps-researcher-003           │              │ • nse-requirements-002        │
│   (pattern research)          │              │   (requirements baseline)     │
│                               │              │ • nse-explorer-002            │
│                               │              │   (trade studies)             │
│ STATUS: PENDING               │              │ STATUS: PENDING               │
└──────────────┬────────────────┘              └──────────────┬────────────────┘
               │                                              │
               ▼                                              ▼
    ╔══════════════════════════════════════════════════════════════════════╗
    ║                         SYNC BARRIER 2                              ║
    ║  ┌────────────────────────────────────────────────────────────────┐ ║
    ║  │ ps→nse: Architecture patterns, ADR drafts, design rationale   │ ║
    ║  │ nse→ps: V&V plan, requirements trace, architecture gaps       │ ║
    ║  └────────────────────────────────────────────────────────────────┘ ║
    ║  QUALITY GATE: >= 0.95 | SRR/PDR Review Gate                      ║
    ╚══════════════════════════════════════════════════════════════════════╝
               │                                              │
               ▼                                              ▼
┌───────────────────────────────┐              ┌───────────────────────────────┐
│ PHASE 3: IMPLEMENTATION       │              │ PHASE 3: INTEGRATION          │
│ ───────────────────────────── │              │   VERIFICATION                │
│ • ps-analyst-002              │              │ ───────────────────────────── │
│   (implementation analysis)   │              │ • nse-verification-001        │
│ • ps-critic-001               │              │   (implementation V&V)        │
│   (security code review)      │              │ • nse-integration-001         │
│                               │              │   (integration verification)  │
│ STATUS: PENDING               │              │ STATUS: PENDING               │
└──────────────┬────────────────┘              └──────────────┬────────────────┘
               │                                              │
               ▼                                              ▼
    ╔══════════════════════════════════════════════════════════════════════╗
    ║                         SYNC BARRIER 3                              ║
    ║  ┌────────────────────────────────────────────────────────────────┐ ║
    ║  │ ps→nse: Implementation artifacts, code review findings        │ ║
    ║  │ nse→ps: V&V results, integration issues, compliance gaps      │ ║
    ║  └────────────────────────────────────────────────────────────────┘ ║
    ║  QUALITY GATE: >= 0.95 | CDR Review Gate                          ║
    ╚══════════════════════════════════════════════════════════════════════╝
               │                                              │
               ▼                                              ▼
┌───────────────────────────────┐              ┌───────────────────────────────┐
│ PHASE 4: ADVERSARIAL          │              │ PHASE 4: COMPLIANCE           │
│   VERIFICATION                │              │   VERIFICATION                │
│ ───────────────────────────── │              │ ───────────────────────────── │
│ • ps-investigator-001         │              │ • nse-verification-002        │
│   (adversarial testing)       │              │   (V&V execution)             │
│ • ps-reviewer-001             │              │ • nse-verification-003        │
│   (red team review)           │              │   (compliance verification)   │
│                               │              │                               │
│ STATUS: PENDING               │              │ STATUS: PENDING               │
└──────────────┬────────────────┘              └──────────────┬────────────────┘
               │                                              │
               ▼                                              ▼
    ╔══════════════════════════════════════════════════════════════════════╗
    ║                         SYNC BARRIER 4                              ║
    ║  ┌────────────────────────────────────────────────────────────────┐ ║
    ║  │ ps→nse: Adversarial findings, red team results, test gaps     │ ║
    ║  │ nse→ps: Compliance results, V&V coverage, documentation gaps  │ ║
    ║  └────────────────────────────────────────────────────────────────┘ ║
    ║  QUALITY GATE: >= 0.95 | TRR Review Gate                          ║
    ╚══════════════════════════════════════════════════════════════════════╝
               │                                              │
               ▼                                              ▼
┌───────────────────────────────┐              ┌───────────────────────────────┐
│ PHASE 5: DOCUMENTATION        │              │ PHASE 5: COMPLIANCE           │
│ ───────────────────────────── │              │   DOCUMENTATION               │
│ • ps-synthesizer-001          │              │ ───────────────────────────── │
│   (best practices synthesis)  │              │ • nse-verification-004        │
│ • ps-reporter-001             │              │   (compliance documentation)  │
│   (security guide)            │              │                               │
│                               │              │                               │
│ STATUS: PENDING               │              │ STATUS: PENDING               │
└───────────────────────────────┘              └───────────────────────────────┘
               │                                              │
               ▼                                              ▼
    ╔══════════════════════════════════════════════════════════════════════╗
    ║                     FINAL SYNTHESIS                                  ║
    ║  ┌────────────────────────────────────────────────────────────────┐ ║
    ║  │ orch-synthesizer-001: Unified security posture report          │ ║
    ║  │ Deliverable: synthesis/workflow-synthesis.md                   │ ║
    ║  └────────────────────────────────────────────────────────────────┘ ║
    ╚══════════════════════════════════════════════════════════════════════╝
```

### 2.2 Orchestration Pattern Classification

| Pattern | Applied | Description |
|---------|---------|-------------|
| Sequential | Yes | 5 phases execute in order within each pipeline |
| Concurrent | Yes | PS and NSE pipelines run in parallel |
| Barrier Sync | Yes | 4 cross-pollination barriers between phases |
| Hierarchical | Yes | Main context orchestrates worker agents |

---

## 3. Phase Definitions

### 3.1 PS Pipeline Phases

| Phase | Name | Purpose | Agents | Skill | Status |
|-------|------|---------|--------|-------|--------|
| 1 | Deep Research | Competitive analysis, threat framework consumption, gap analysis | ps-researcher-001, ps-researcher-002, ps-analyst-001 | /problem-solving | PENDING |
| 2 | Architecture | Security architecture design, pattern research, ADR drafting | ps-architect-001, ps-researcher-003 | /problem-solving | PENDING |
| 3 | Implementation | Implementation analysis, security code review | ps-analyst-002, ps-critic-001 | /problem-solving | PENDING |
| 4 | Adversarial Verification | Adversarial testing, red team review | ps-investigator-001, ps-reviewer-001 | /problem-solving | PENDING |
| 5 | Documentation | Best practices synthesis, security guide authoring | ps-synthesizer-001, ps-reporter-001 | /problem-solving | PENDING |

### 3.2 NSE Pipeline Phases

| Phase | Name | Purpose | Agents | Skill | Status |
|-------|------|---------|--------|-------|--------|
| 1 | Requirements Discovery | Security requirements, initial risk register | nse-requirements-001, nse-explorer-001 | /nasa-se | PENDING |
| 2 | Formal Design | Formal architecture, requirements baseline, trade studies | nse-architecture-001, nse-requirements-002, nse-explorer-002 | /nasa-se | PENDING |
| 3 | Integration Verification | Implementation V&V, integration verification | nse-verification-001, nse-integration-001 | /nasa-se | PENDING |
| 4 | Compliance Verification | V&V execution, compliance matrix verification | nse-verification-002, nse-verification-003 | /nasa-se | PENDING |
| 5 | Compliance Documentation | Compliance reports, coverage documentation | nse-verification-004 | /nasa-se | PENDING |

### 3.3 Phase Detail: Phase 1 - Deep Research / Requirements Discovery

**PS Pipeline - Phase 1: Deep Research**

| Agent | Task | Input | Output | Model |
|-------|------|-------|--------|-------|
| ps-researcher-001 | Competitive landscape analysis: OpenClaw/Clawdbot failures, Claude Agent SDK, Claude Code, claude-flow, Cline, Microsoft guidance, Cisco analysis | PLAN.md research targets | `ps/phase-1/ps-researcher-001/competitive-landscape.md` | opus |
| ps-researcher-002 | Threat framework consumption: MITRE ATT&CK Enterprise + ATLAS + Mobile, OWASP LLM/API/Web Top 10, NIST AI RMF + CSF 2.0 + SP 800-53 | Framework URLs, PLAN.md scope | `ps/phase-1/ps-researcher-002/threat-framework-analysis.md` | opus |
| ps-analyst-001 | Gap analysis: Jerry current posture vs. threat frameworks, priority risk matrix | ps-researcher-001 + ps-researcher-002 outputs | `ps/phase-1/ps-analyst-001/gap-analysis.md` | opus |

**NSE Pipeline - Phase 1: Requirements Discovery**

| Agent | Task | Input | Output | Model |
|-------|------|-------|--------|-------|
| nse-requirements-001 | Security requirements discovery: functional and non-functional security requirements from threat frameworks | PLAN.md scope, MITRE/OWASP/NIST references | `nse/phase-1/nse-requirements-001/security-requirements.md` | opus |
| nse-explorer-001 | Initial risk register: FMEA-style risk analysis for agentic security threats | PLAN.md research targets, threat context | `nse/phase-1/nse-explorer-001/risk-register.md` | opus |

### 3.4 Phase Detail: Phase 2 - Architecture / Formal Design

**PS Pipeline - Phase 2: Architecture**

| Agent | Task | Input | Output | Model |
|-------|------|-------|--------|-------|
| ps-architect-001 | Security architecture design: zero-trust skill execution, privilege isolation, deterministic verification, supply chain security | Phase 1 outputs, barrier-1 cross-pollination | `ps/phase-2/ps-architect-001/security-architecture.md` | opus |
| ps-researcher-003 | Security pattern research: industry patterns, defense-in-depth models, secure agent frameworks | Phase 1 gap analysis | `ps/phase-2/ps-researcher-003/security-patterns.md` | opus |

**NSE Pipeline - Phase 2: Formal Design**

| Agent | Task | Input | Output | Model |
|-------|------|-------|--------|-------|
| nse-architecture-001 | Formal security architecture: NPR 7123.1D compliant design, interface definitions | Phase 1 requirements, barrier-1 cross-pollination | `nse/phase-2/nse-architecture-001/formal-architecture.md` | opus |
| nse-requirements-002 | Requirements baseline: frozen requirements with traceability matrix | Phase 1 requirements, architecture input | `nse/phase-2/nse-requirements-002/requirements-baseline.md` | opus |
| nse-explorer-002 | Trade studies: security control trade-offs (performance vs. security, usability vs. restriction) | Architecture options | `nse/phase-2/nse-explorer-002/trade-studies.md` | opus |

### 3.5 Phase Detail: Phase 3 - Implementation / Integration Verification

**PS Pipeline - Phase 3: Implementation**

| Agent | Task | Input | Output | Model |
|-------|------|-------|--------|-------|
| ps-analyst-002 | Implementation analysis: security control implementation specifications, code patterns | Phase 2 architecture, barrier-2 cross-pollination | `ps/phase-3/ps-analyst-002/implementation-specs.md` | opus |
| ps-critic-001 | Security code review: review implemented controls against architecture, identify vulnerabilities | Implementation artifacts | `ps/phase-3/ps-critic-001/security-review.md` | opus |

**NSE Pipeline - Phase 3: Integration Verification**

| Agent | Task | Input | Output | Model |
|-------|------|-------|--------|-------|
| nse-verification-001 | Implementation V&V: verify controls against requirements, validate behavior | Requirements baseline, implementation artifacts | `nse/phase-3/nse-verification-001/implementation-vv.md` | opus |
| nse-integration-001 | Integration verification: verify security controls integrate correctly with existing Jerry framework | Integration test results, system behavior | `nse/phase-3/nse-integration-001/integration-report.md` | opus |

### 3.6 Phase Detail: Phase 4 - Adversarial Verification / Compliance Verification

**PS Pipeline - Phase 4: Adversarial Verification**

| Agent | Task | Input | Output | Model |
|-------|------|-------|--------|-------|
| ps-investigator-001 | Adversarial testing: prompt injection attacks, privilege escalation attempts, supply chain attack simulation | Implemented controls, threat model | `ps/phase-4/ps-investigator-001/adversarial-testing.md` | opus |
| ps-reviewer-001 | Red team review: S-001 Red Team strategy, S-012 FMEA, S-004 Pre-Mortem against full security architecture | Full security posture | `ps/phase-4/ps-reviewer-001/red-team-report.md` | opus |

**NSE Pipeline - Phase 4: Compliance Verification**

| Agent | Task | Input | Output | Model |
|-------|------|-------|--------|-------|
| nse-verification-002 | V&V execution: complete verification matrix, all requirements traced to evidence | Requirements baseline, implementation evidence | `nse/phase-4/nse-verification-002/vv-execution.md` | opus |
| nse-verification-003 | Compliance verification: MITRE ATT&CK coverage matrix, OWASP compliance matrix, NIST controls compliance | Framework mappings, implementation evidence | `nse/phase-4/nse-verification-003/compliance-matrix.md` | opus |

### 3.7 Phase Detail: Phase 5 - Documentation / Compliance Documentation

**PS Pipeline - Phase 5: Documentation**

| Agent | Task | Input | Output | Model |
|-------|------|-------|--------|-------|
| ps-synthesizer-001 | Best practices synthesis: unified security posture, lessons learned, industry positioning | All prior phase outputs | `ps/phase-5/ps-synthesizer-001/best-practices.md` | opus |
| ps-reporter-001 | Security guide: Jerry Security Architecture Guide, Secure Agent Development Guide, Incident Response Playbook | Best practices, architecture docs | `ps/phase-5/ps-reporter-001/security-guide.md` | opus |

**NSE Pipeline - Phase 5: Compliance Documentation**

| Agent | Task | Input | Output | Model |
|-------|------|-------|--------|-------|
| nse-verification-004 | Compliance documentation: MITRE ATT&CK coverage report, OWASP compliance report, NIST compliance report | Compliance matrices, V&V results | `nse/phase-5/nse-verification-004/compliance-reports.md` | opus |

---

## 4. Sync Barrier Protocol

### 4.1 Barrier Transition Rules

```
1. PRE-BARRIER CHECK
   □ All phase agents in both pipelines have completed
   □ All phase artifacts exist and are non-empty
   □ No blocking errors or unresolved critical issues
   □ Phase quality gate >= 0.95 (elevated C4 threshold)

2. CROSS-POLLINATION EXECUTION (C4 TOURNAMENT MODE)
   □ Extract key findings from source pipeline (3-5 bullets per CB-04)
   □ Create structured handoff artifact (HD-M-001 schema)
   □ Apply ALL 10 adversarial strategies (C4 tournament):
     - S-014 (LLM-as-Judge): Rubric-based scoring
     - S-003 (Steelman): Charitable reconstruction
     - S-013 (Inversion): "How could this fail?"
     - S-007 (Constitutional AI): Principle-by-principle
     - S-002 (Devil's Advocate): Strongest counterargument
     - S-004 (Pre-Mortem): "Imagine it failed -- why?"
     - S-010 (Self-Refine): Self-review before presenting
     - S-012 (FMEA): Systematic failure mode enumeration
     - S-011 (Chain-of-Verification): Factual verification
     - S-001 (Red Team): Adversary simulation
   □ Score with S-014: must achieve >= 0.95
   □ Up to 5 iterations (creator → critic → revision)
   □ Background critic agents with structured feedback to creator

3. POST-BARRIER VERIFICATION
   □ Receiving pipeline acknowledges handoff
   □ Key findings incorporated into next phase context
   □ Barrier status updated to COMPLETE
   □ Checkpoint created
   □ Memory-Keeper store for cross-session persistence
```

### 4.2 Barrier Definitions

| Barrier | After Phase | PS→NSE Content | NSE→PS Content | Status |
|---------|-------------|----------------|----------------|--------|
| barrier-1 | Phase 1 | Research findings, threat maps, gap priorities | Requirements gaps, risk-driven research priorities | PENDING |
| barrier-2 | Phase 2 | Architecture patterns, ADR drafts, design rationale | V&V plan, requirements trace, architecture gaps | PENDING |
| barrier-3 | Phase 3 | Implementation artifacts, code review findings | V&V results, integration issues, compliance gaps | PENDING |
| barrier-4 | Phase 4 | Adversarial findings, red team results, test gaps | Compliance results, V&V coverage, documentation gaps | PENDING |

---

## 5. Phase Gate Criteria

### 5.1 Gate 1: Research → Architecture (Phase 1 → Phase 2)

| Criterion | Validation | Required |
|-----------|------------|----------|
| All competitive analyses complete | 6 research targets analyzed (OpenClaw, Claude SDK, Claude Code, claude-flow, Cline, Microsoft/Cisco) | Yes |
| All threat frameworks consumed | MITRE ATT&CK Enterprise + ATLAS + Mobile consumed; OWASP LLM + API + Web Top 10 analyzed; NIST AI RMF + CSF 2.0 + SP 800-53 mapped | Yes |
| Gap analysis complete | Jerry vs. threats gap matrix with risk priority scores | Yes |
| Initial risk register created | FMEA-style with RPN scores for top threats | Yes |
| Security requirements drafted | Functional + non-functional security requirements documented | Yes |
| Quality gate passed | C4 tournament score >= 0.95 (all 10 strategies) on all Phase 1 deliverables | Yes |
| Barrier 1 cross-pollination complete | Both PS→NSE and NSE→PS handoffs delivered and accepted | Yes |

### 5.2 Gate 2: Architecture → Implementation (Phase 2 → Phase 3)

| Criterion | Validation | Required |
|-----------|------------|----------|
| Threat model complete | STRIDE/DREAD analysis with attack surface map and trust boundaries | Yes |
| Security architecture documented | Zero-trust model, privilege isolation, deterministic verification, supply chain security | Yes |
| ADRs authored | All significant architecture decisions recorded | Yes |
| Requirements baselined | Frozen requirements with bi-directional traceability | Yes |
| Trade studies complete | Security vs. performance, usability vs. restriction trade-offs analyzed | Yes |
| SRR/PDR review passed | System Requirements Review and Preliminary Design Review gates | Yes |
| Quality gate passed | C4 tournament score >= 0.95 (all 10 strategies) on all Phase 2 deliverables | Yes |
| Barrier 2 cross-pollination complete | Both directions delivered and accepted | Yes |

### 5.3 Gate 3: Implementation → Verification (Phase 3 → Phase 4)

| Criterion | Validation | Required |
|-----------|------------|----------|
| Security controls implemented | Governance HARD rules, L2 markers, auto-escalation rules | Yes |
| Agent security model operational | Schema extensions, permission boundaries, audit trails | Yes |
| Skill security model operational | Isolation, input validation, output sanitization | Yes |
| Infrastructure security implemented | MCP hardening, credential management, supply chain verification | Yes |
| Security code review complete | ps-critic-001 review with zero critical findings | Yes |
| Implementation V&V passed | Controls verified against requirements | Yes |
| CDR review passed | Critical Design Review gate | Yes |
| Quality gate passed | C4 tournament score >= 0.95 (all 10 strategies) on all Phase 3 deliverables | Yes |
| Barrier 3 cross-pollination complete | Both directions delivered and accepted | Yes |

### 5.4 Gate 4: Verification → Documentation (Phase 4 → Phase 5)

| Criterion | Validation | Required |
|-----------|------------|----------|
| Adversarial testing complete | Prompt injection, privilege escalation, supply chain attack simulation | Yes |
| Red team review complete | S-001 + S-012 + S-004 applied to full security posture | Yes |
| V&V execution complete | All requirements traced to verification evidence | Yes |
| Compliance matrices verified | MITRE, OWASP, NIST coverage confirmed | Yes |
| Zero critical/high findings unresolved | All critical and high severity findings addressed | Yes |
| TRR review passed | Test Readiness Review gate | Yes |
| Quality gate passed | C4 tournament score >= 0.95 (all 10 strategies) on all Phase 4 deliverables | Yes |
| Barrier 4 cross-pollination complete | Both directions delivered and accepted | Yes |

### 5.5 Gate 5: Documentation → Complete (Phase 5 Exit)

| Criterion | Validation | Required |
|-----------|------------|----------|
| Security guide published | Jerry Security Architecture Guide complete | Yes |
| Developer standards published | Secure Agent + Skill Development Guides complete | Yes |
| Compliance reports complete | MITRE, OWASP, NIST coverage reports finalized | Yes |
| Final synthesis created | Unified security posture report by orch-synthesizer-001 | Yes |
| Quality gate passed | C4 tournament score >= 0.95 (all 10 strategies) on all Phase 5 deliverables | Yes |
| All worktracker items resolved | All Epics, Features, Stories marked complete | Yes |

---

## 6. Agent Registry

### 6.1 PS Pipeline Agents

| Agent ID | Phase | Role | Cognitive Mode | Tool Tier | Input Artifacts | Output Artifact |
|----------|-------|------|---------------|-----------|-----------------|-----------------|
| ps-researcher-001 | 1 | Competitive landscape analysis | divergent | T3 | PLAN.md | competitive-landscape.md |
| ps-researcher-002 | 1 | Threat framework consumption | divergent | T3 | Framework references | threat-framework-analysis.md |
| ps-analyst-001 | 1 | Gap analysis | convergent | T2 | ps-researcher-001/002 outputs | gap-analysis.md |
| ps-architect-001 | 2 | Security architecture design | convergent | T2 | Phase 1 outputs, barrier-1 | security-architecture.md |
| ps-researcher-003 | 2 | Security pattern research | divergent | T3 | gap-analysis.md | security-patterns.md |
| ps-analyst-002 | 3 | Implementation specifications | convergent | T2 | Phase 2 outputs, barrier-2 | implementation-specs.md |
| ps-critic-001 | 3 | Security code review | convergent | T1 | Implementation artifacts | security-review.md |
| ps-investigator-001 | 4 | Adversarial testing | forensic | T2 | Controls, threat model | adversarial-testing.md |
| ps-reviewer-001 | 4 | Red team review | convergent | T1 | Full security posture | red-team-report.md |
| ps-synthesizer-001 | 5 | Best practices synthesis | integrative | T2 | All prior outputs | best-practices.md |
| ps-reporter-001 | 5 | Security guide authoring | integrative | T2 | Best practices, architecture | security-guide.md |

### 6.2 NSE Pipeline Agents

| Agent ID | Phase | Role | Cognitive Mode | Tool Tier | Input Artifacts | Output Artifact |
|----------|-------|------|---------------|-----------|-----------------|-----------------|
| nse-requirements-001 | 1 | Security requirements discovery | systematic | T2 | PLAN.md, frameworks | security-requirements.md |
| nse-explorer-001 | 1 | Initial risk register | divergent | T3 | Research targets | risk-register.md |
| nse-architecture-001 | 2 | Formal architecture | convergent | T2 | Phase 1, barrier-1 | formal-architecture.md |
| nse-requirements-002 | 2 | Requirements baseline | systematic | T2 | Phase 1 requirements | requirements-baseline.md |
| nse-explorer-002 | 2 | Trade studies | divergent | T3 | Architecture options | trade-studies.md |
| nse-verification-001 | 3 | Implementation V&V | systematic | T1 | Requirements, implementation | implementation-vv.md |
| nse-integration-001 | 3 | Integration verification | systematic | T2 | Integration targets | integration-report.md |
| nse-verification-002 | 4 | V&V execution | systematic | T1 | Requirements, evidence | vv-execution.md |
| nse-verification-003 | 4 | Compliance verification | systematic | T1 | Framework mappings | compliance-matrix.md |
| nse-verification-004 | 5 | Compliance documentation | systematic | T2 | Compliance matrices | compliance-reports.md |

### 6.3 Orchestration Agents

| Agent ID | Role | Invocation Point | Output |
|----------|------|-------------------|--------|
| orch-planner | Workflow planning | Session start | This document + ORCHESTRATION.yaml |
| orch-tracker | State tracking | After each agent/barrier completion | ORCHESTRATION.yaml updates |
| orch-synthesizer-001 | Final synthesis | After Phase 5 | synthesis/workflow-synthesis.md |

---

## 7. Skill Routing Map

| Work Item Scope | Primary Skill | Secondary Skill | Rationale |
|----------------|---------------|-----------------|-----------|
| Competitive research | /problem-solving | -- | Research/analysis is PS domain |
| Threat framework analysis | /problem-solving | -- | External framework consumption |
| Gap analysis | /problem-solving | -- | Analytical comparison |
| Security requirements | /nasa-se | -- | Requirements engineering is NSE domain |
| Risk register | /nasa-se | -- | Risk management per NPR 7123.1D |
| Architecture design | /problem-solving | /nasa-se | PS for creative design, NSE for formal validation |
| Trade studies | /nasa-se | -- | Structured decision analysis |
| Implementation specs | /problem-solving | -- | Code-level analysis |
| V&V planning/execution | /nasa-se | -- | Verification is NSE domain |
| Adversarial testing | /problem-solving | /adversary | PS for investigation, /adversary for strategy execution |
| Red team review | /adversary | /problem-solving | /adversary leads, PS supports |
| Compliance matrices | /nasa-se | -- | Compliance verification is NSE domain |
| Documentation | /problem-solving | -- | Synthesis and reporting |
| Worktracker management | /worktracker | -- | Entity lifecycle management |
| Workflow coordination | /orchestration | -- | Cross-pipeline coordination |

---

## 8. State Management

### 8.1 State Files

| File | Purpose |
|------|---------|
| `ORCHESTRATION.yaml` | Machine-readable state (SSOT) |
| `ORCHESTRATION_WORKTRACKER.md` | Tactical execution documentation |
| `ORCHESTRATION_PLAN.md` | This file - strategic context |

### 8.2 Artifact Path Structure

```
orchestration/agentic-sec-20260222-001/
├── ORCHESTRATION_PLAN.md
├── ORCHESTRATION_WORKTRACKER.md
├── ORCHESTRATION.yaml
├── ps/
│   ├── phase-1/
│   │   ├── ps-researcher-001/
│   │   │   └── ps-researcher-001-competitive-landscape.md
│   │   ├── ps-researcher-002/
│   │   │   └── ps-researcher-002-threat-framework-analysis.md
│   │   └── ps-analyst-001/
│   │       └── ps-analyst-001-gap-analysis.md
│   ├── phase-2/
│   │   ├── ps-architect-001/
│   │   │   └── ps-architect-001-security-architecture.md
│   │   └── ps-researcher-003/
│   │       └── ps-researcher-003-security-patterns.md
│   ├── phase-3/
│   │   ├── ps-analyst-002/
│   │   │   └── ps-analyst-002-implementation-specs.md
│   │   └── ps-critic-001/
│   │       └── ps-critic-001-security-review.md
│   ├── phase-4/
│   │   ├── ps-investigator-001/
│   │   │   └── ps-investigator-001-adversarial-testing.md
│   │   └── ps-reviewer-001/
│   │       └── ps-reviewer-001-red-team-report.md
│   └── phase-5/
│       ├── ps-synthesizer-001/
│       │   └── ps-synthesizer-001-best-practices.md
│       └── ps-reporter-001/
│           └── ps-reporter-001-security-guide.md
├── nse/
│   ├── phase-1/
│   │   ├── nse-requirements-001/
│   │   │   └── nse-requirements-001-security-requirements.md
│   │   └── nse-explorer-001/
│   │       └── nse-explorer-001-risk-register.md
│   ├── phase-2/
│   │   ├── nse-architecture-001/
│   │   │   └── nse-architecture-001-formal-architecture.md
│   │   ├── nse-requirements-002/
│   │   │   └── nse-requirements-002-requirements-baseline.md
│   │   └── nse-explorer-002/
│   │       └── nse-explorer-002-trade-studies.md
│   ├── phase-3/
│   │   ├── nse-verification-001/
│   │   │   └── nse-verification-001-implementation-vv.md
│   │   └── nse-integration-001/
│   │       └── nse-integration-001-integration-report.md
│   ├── phase-4/
│   │   ├── nse-verification-002/
│   │   │   └── nse-verification-002-vv-execution.md
│   │   └── nse-verification-003/
│   │       └── nse-verification-003-compliance-matrix.md
│   └── phase-5/
│       └── nse-verification-004/
│           └── nse-verification-004-compliance-reports.md
├── cross-pollination/
│   ├── barrier-1/
│   │   ├── ps-to-nse/
│   │   │   └── handoff.md
│   │   └── nse-to-ps/
│   │       └── handoff.md
│   ├── barrier-2/
│   │   ├── ps-to-nse/
│   │   │   └── handoff.md
│   │   └── nse-to-ps/
│   │       └── handoff.md
│   ├── barrier-3/
│   │   ├── ps-to-nse/
│   │   │   └── handoff.md
│   │   └── nse-to-ps/
│   │       └── handoff.md
│   └── barrier-4/
│       ├── ps-to-nse/
│       │   └── handoff.md
│       └── nse-to-ps/
│           └── handoff.md
└── synthesis/
    └── workflow-synthesis.md
```

### 8.3 Checkpoint Strategy

| Trigger | When | Purpose |
|---------|------|---------|
| PHASE_COMPLETE | After each phase (10 total: 5 per pipeline) | Phase-level rollback |
| BARRIER_COMPLETE | After each sync barrier (4 total) | Cross-pollination recovery |
| GATE_PASS | After each phase gate (5 total) | Gate-level recovery |
| MANUAL | User-triggered | Debug and inspection |

---

## 9. Execution Constraints

### 9.1 Hard Constraints (Jerry Constitution)

| Constraint | ID | Enforcement |
|------------|----|----|
| Single agent nesting | P-003 / H-01 | Orchestrator → Worker only |
| File persistence | P-002 | All state to filesystem |
| No deception | P-022 / H-03 | Transparent reasoning |
| User authority | P-020 / H-02 | User approves gates |
| Quality threshold | H-13 | >= 0.95 for all deliverables |
| Creator-critic-revision | H-14 | Minimum 3 iterations at barriers |
| Self-review | H-15 | S-010 before presenting |
| Steelman before critique | H-16 | S-003 before S-002 |
| Security auto-escalation | AE-005 | Auto-C3 minimum for all security work |

### 9.1.1 Worktracker Entity Templates

> **WTI-007:** Entity files created during orchestration MUST use canonical templates from `.context/templates/worktracker/`. Read the appropriate template first, then populate.

### 9.2 Operational Constraints

| Constraint | Value | Rationale |
|------------|-------|-----------|
| Max concurrent agents | 5 | Resource management (context windows) |
| Max barrier retries | 3 | Circuit breaker (H-36) |
| Checkpoint frequency | PHASE + BARRIER | Balanced recovery granularity |
| Quality criticality | **C4** (all phases) | Mission-critical, irreversible architecture + AE-005 security-critical |
| Quality threshold | **>= 0.95** | Elevated above standard 0.92 per user directive |
| Iteration ceiling | **5 iterations** per gate | Creator → Critic → Revision, up to 5 cycles |
| Adversarial strategies | **ALL 10** (C4 tournament): S-001, S-002, S-003, S-004, S-007, S-010, S-011, S-012, S-013, S-014 | C4 = all strategies required, none optional |
| Agent execution model | **Background agents** via Task tool | Critic runs in background, feedback returned to creator for revision |
| Data sources | **Clone repos** (MITRE STIX, NIST OSCAL, ATLAS) | Consume machine-readable data, not web scraping |
| Research standard | **Evidence-driven** with citations | All findings cite authoritative sources with authority classification |

---

## 10. Risk Register

| ID | Risk | Likelihood | Impact | RPN | Mitigation |
|----|------|------------|--------|-----|------------|
| R-001 | Context rot during long research phases | High | High | 9 | Checkpoint at phase boundaries; session restart between phases; use Memory-Keeper for cross-session state |
| R-002 | Framework scope creep (MITRE+OWASP+NIST is vast) | High | Medium | 6 | Strict scope per user decision; time-box each framework analysis; focus on agentic-relevant controls |
| R-003 | Competitive landscape evolves during project | Medium | Medium | 4 | Time-bound research to Phase 1; architecture designed for extensibility |
| R-004 | Security controls conflict with usability | Medium | High | 6 | Trade studies in Phase 2; user authority on trade-off decisions (H-02) |
| R-005 | Quality gate bottleneck at barriers | Medium | Medium | 4 | 3-iteration max per barrier; escalate to user if blocked |
| R-006 | MITRE ATLAS coverage gaps (AI-specific threats not fully mapped) | Medium | Medium | 4 | Supplement with academic research; note coverage gaps explicitly |
| R-007 | Implementation impacts existing Jerry functionality | Low | High | 3 | Integration verification in Phase 3 (NSE pipeline); regression testing |
| R-008 | Token exhaustion during adversarial testing phase | Medium | High | 6 | Session partitioning; checkpoint before each adversarial run; focus red team on highest-risk areas |

---

## 11. Resumption Context

### 11.1 Current Execution State

```
WORKFLOW STATUS AS OF 2026-02-22
================================

PS Pipeline:
  Phase 1 (Deep Research):        PENDING
  Phase 2 (Architecture):         PENDING
  Phase 3 (Implementation):       PENDING
  Phase 4 (Adversarial Verify):   PENDING
  Phase 5 (Documentation):        PENDING

NSE Pipeline:
  Phase 1 (Requirements):         PENDING
  Phase 2 (Formal Design):        PENDING
  Phase 3 (Integration V&V):      PENDING
  Phase 4 (Compliance V&V):       PENDING
  Phase 5 (Compliance Docs):      PENDING

Barriers:
  Barrier 1: PENDING
  Barrier 2: PENDING
  Barrier 3: PENDING
  Barrier 4: PENDING

Synthesis: PENDING
```

### 11.2 Next Actions

1. **Execute Phase 1 agents** (PS: ps-researcher-001, ps-researcher-002, ps-analyst-001 | NSE: nse-requirements-001, nse-explorer-001) -- PARALLEL execution
2. **Complete Barrier 1** cross-pollination after Phase 1
3. **Phase Gate 1** quality review before Phase 2

---

*Document ID: PROJ-008-ORCH-PLAN*
*Workflow ID: agentic-sec-20260222-001*
*Version: 2.0*
*Cross-Session Portable: All paths are repository-relative*
