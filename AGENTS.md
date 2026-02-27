# AGENTS.md - Registry of Available Specialists

> This file documents the sub-agent personas available for task delegation.
> Each agent has specialized capabilities and context isolation.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Agent Philosophy](#agent-philosophy) | Core principles of agent-based work |
| [Agent Summary](#agent-summary) | Quick count by skill |
| [Problem-Solving Skill Agents](#problem-solving-skill-agents) | ps-* agents (9 total) |
| [NASA SE Skill Agents](#nasa-se-skill-agents) | nse-* agents (10 total) |
| [Orchestration Skill Agents](#orchestration-skill-agents) | orch-* agents (3 total) |
| [Adversary Skill Agents](#adversary-skill-agents) | adv-* agents (3 total) |
| [Worktracker Skill Agents](#worktracker-skill-agents) | wt-* agents (3 total) |
| [Transcript Skill Agents](#transcript-skill-agents) | ts-* agents (5 total) |
| [Framework Voice Skill Agents](#framework-voice-skill-agents) | sb-* agents (3 total) |
| [Session Voice Skill Agents](#session-voice-skill-agents) | sb-voice agent (1 total) |
| [Eng-Team Skill Agents](#eng-team-skill-agents) | eng-* agents (10 total) |
| [Red-Team Skill Agents](#red-team-skill-agents) | red-* agents (11 total) |
| [Diataxis Skill Agents](#diataxis-skill-agents) | diataxis-* agents (6 total) |
| [MCP Tool Access](#mcp-tool-access) | Context7 and Memory-Keeper agent matrix |
| [Agent Handoff Protocol](#agent-handoff-protocol) | Multi-agent coordination |
| [Adding New Agents](#adding-new-agents) | Extension guide |

---

## Agent Philosophy

Jerry uses a **skill-based agent pattern** where specialized agents are scoped
to specific skills. This provides:

1. **Context Isolation** - Each agent has focused context
2. **Expertise Depth** - Specialists know their domain deeply
3. **Parallel Execution** - Multiple agents can work concurrently
4. **Quality Gates** - Handoffs enforce review checkpoints

---

## Agent Summary

| Category | Count | Scope |
|----------|-------|-------|
| Problem-Solving Agents | 9 | `/problem-solving` skill |
| NASA SE Agents | 10 | `/nasa-se` skill |
| Orchestration Agents | 3 | `/orchestration` skill |
| Adversary Agents | 3 | `/adversary` skill |
| Worktracker Agents | 3 | `/worktracker` skill |
| Transcript Agents | 5 | `/transcript` skill |
| Framework Voice Agents | 3 | `/saucer-boy-framework-voice` skill |
| Session Voice Agents | 1 | `/saucer-boy` skill |
| Eng-Team Agents | 10 | `/eng-team` skill |
| Red-Team Agents | 11 | `/red-team` skill |
| Diataxis Agents | 6 | `/diataxis` skill |
| **Total** | **64** | |

> **Verification:** Agent counts verified against filesystem scan (`skills/*/agents/*.md`).
> 68 total files found; 4 template/extension files excluded from counts:
> `NSE_AGENT_TEMPLATE.md`, `NSE_EXTENSION.md`, `PS_AGENT_TEMPLATE.md`, `PS_EXTENSION.md`.
> Per-skill sum: 9 + 10 + 3 + 3 + 3 + 5 + 3 + 1 + 10 + 11 + 6 = 64 invokable agents.
> Last verified: 2026-02-26.

---

## Problem-Solving Skill Agents

These agents are scoped to the `problem-solving` skill and invoked via `/problem-solving`.

| Agent | File | Role | Cognitive Mode |
|-------|------|------|----------------|
| ps-researcher | `skills/problem-solving/agents/ps-researcher.md` | Research Specialist | Divergent |
| ps-analyst | `skills/problem-solving/agents/ps-analyst.md` | Analysis Specialist | Convergent |
| ps-synthesizer | `skills/problem-solving/agents/ps-synthesizer.md` | Synthesis Specialist | Integrative |
| ps-validator | `skills/problem-solving/agents/ps-validator.md` | Validation Specialist | Systematic |
| ps-architect | `skills/problem-solving/agents/ps-architect.md` | Architecture Specialist | Strategic |
| ps-reviewer | `skills/problem-solving/agents/ps-reviewer.md` | Review Specialist | Critical |
| ps-critic | `skills/problem-solving/agents/ps-critic.md` | Quality Evaluator | Convergent |
| ps-investigator | `skills/problem-solving/agents/ps-investigator.md` | Investigation Specialist | Forensic |
| ps-reporter | `skills/problem-solving/agents/ps-reporter.md` | Reporting Specialist | Communicative |

**Key Capabilities:**

| Agent | Primary Use Case | Output Type |
|-------|------------------|-------------|
| ps-researcher | Literature review, web research, source validation | Research findings |
| ps-analyst | Root cause analysis, trade-offs, gap analysis, risk | Analysis reports |
| ps-synthesizer | Pattern synthesis across multiple research outputs | Synthesis documents |
| ps-validator | Constraint verification, design validation | Validation reports |
| ps-architect | Architecture decisions, ADR production | Design documents, ADRs |
| ps-reviewer | Code review, design review, security review | Review reports |
| ps-critic | Quality evaluation for creator-critic-revision cycles | Critique reports with scores |
| ps-investigator | Failure analysis, debugging, 5 Whys | Investigation reports |
| ps-reporter | Status reports, phase progress, summaries | Status documents |

**Invocation**: Use `/problem-solving` skill which orchestrates these agents.

**Artifact Location**: `{project}/research/`, `{project}/analysis/`, `{project}/synthesis/`, `{project}/critiques/`

---

## NASA SE Skill Agents

These agents implement NASA Systems Engineering processes per NPR 7123.1D.

| Agent | File | Role | NASA Process |
|-------|------|------|--------------|
| nse-requirements | `skills/nasa-se/agents/nse-requirements.md` | Requirements Engineer | Processes 1, 2, 11 |
| nse-verification | `skills/nasa-se/agents/nse-verification.md` | V&V Specialist | Processes 7, 8 |
| nse-risk | `skills/nasa-se/agents/nse-risk.md` | Risk Manager | Process 13 |
| nse-architecture | `skills/nasa-se/agents/nse-architecture.md` | System Architect | Processes 3, 4 |
| nse-integration | `skills/nasa-se/agents/nse-integration.md` | Integration Engineer | Process 9 |
| nse-configuration | `skills/nasa-se/agents/nse-configuration.md` | CM Specialist | Process 10 |
| nse-qa | `skills/nasa-se/agents/nse-qa.md` | Quality Assurance | Process 12 |
| nse-reviewer | `skills/nasa-se/agents/nse-reviewer.md` | Review Coordinator | All reviews (SRR/PDR/CDR/TRR/FRR) |
| nse-reporter | `skills/nasa-se/agents/nse-reporter.md` | Status Reporter | Reporting and metrics |
| nse-explorer | `skills/nasa-se/agents/nse-explorer.md` | Domain Explorer | Research and discovery |

**Key Capabilities:**

| Agent | Primary Deliverable | Output Location |
|-------|---------------------|-----------------|
| nse-requirements | Requirements specs, VCRM | `{project}/requirements/` |
| nse-verification | VCRM, test procedures, validation plans | `{project}/verification/` |
| nse-risk | Risk registers, assessments | `{project}/risks/` |
| nse-architecture | Architecture docs, interface specs | `{project}/architecture/` |
| nse-integration | Integration plans, test results | `{project}/integration/` |
| nse-configuration | Baselines, change control | `{project}/configuration/` |
| nse-qa | Quality plans, audits | `{project}/quality/` |
| nse-reviewer | Review packages, findings | `{project}/reviews/` |
| nse-reporter | Status reports, metrics | `{project}/reports/` |
| nse-explorer | Domain research, trade studies | `{project}/research/` |

**Invocation**: Use `/nasa-se` skill which orchestrates these agents.

**All outputs include mandatory NASA disclaimer** per P-043.

---

## Orchestration Skill Agents

These agents manage multi-agent workflow orchestration and state tracking.

| Agent | File | Role | Cognitive Mode |
|-------|------|------|----------------|
| orch-planner | `skills/orchestration/agents/orch-planner.md` | Orchestration Planner | Convergent |
| orch-tracker | `skills/orchestration/agents/orch-tracker.md` | State Tracker | Convergent |
| orch-synthesizer | `skills/orchestration/agents/orch-synthesizer.md` | Workflow Synthesizer | Integrative |

**Key Capabilities:**

| Agent | Primary Use Case | Output Type |
|-------|------------------|-------------|
| orch-planner | Multi-agent workflow design, pipeline architecture, quality gate planning | ORCHESTRATION_PLAN.md, ORCHESTRATION.yaml |
| orch-tracker | State updates, artifact registration, quality score tracking, checkpoint creation | Updated ORCHESTRATION.yaml, WORKTRACKER.md |
| orch-synthesizer | Cross-pipeline synthesis, barrier aggregation, final reporting | Synthesis reports, workflow summaries |

**Invocation**: Use `/orchestration` skill for multi-phase workflows.

**Artifact Location**: `{project}/orchestration/{workflow-id}/`

---

## Adversary Skill Agents

These agents implement adversarial quality strategies for deliverable review.

| Agent | File | Role | Cognitive Mode |
|-------|------|------|----------------|
| adv-selector | `skills/adversary/agents/adv-selector.md` | Strategy Selector | Convergent |
| adv-executor | `skills/adversary/agents/adv-executor.md` | Strategy Executor | Convergent |
| adv-scorer | `skills/adversary/agents/adv-scorer.md` | Quality Scorer | Convergent |

**Key Capabilities:**

| Agent | Primary Use Case | Output Type |
|-------|------------------|-------------|
| adv-selector | Map criticality levels (C1-C4) to adversarial strategy sets per SSOT | Strategy selection plan |
| adv-executor | Execute strategy templates against deliverables, produce findings | Strategy execution reports |
| adv-scorer | Apply S-014 LLM-as-Judge scoring with dimension-level rubrics | Quality score reports |

**Invocation**: Use `/adversary` skill for standalone adversarial review or integrated into creator-critic-revision cycles.

**Strategy Templates**: `.context/templates/adversarial/s-{NNN}-{name}.md`

---

## Worktracker Skill Agents

These agents manage work item verification, visualization, and auditing.

| Agent | File | Role | Cognitive Mode |
|-------|------|------|----------------|
| wt-verifier | `skills/worktracker/agents/wt-verifier.md` | Status Verification Specialist | Convergent |
| wt-visualizer | `skills/worktracker/agents/wt-visualizer.md` | Visualization Specialist | Divergent |
| wt-auditor | `skills/worktracker/agents/wt-auditor.md` | Integrity Auditor | Systematic |

**Key Capabilities:**

| Agent | Primary Use Case | Output Type |
|-------|------------------|-------------|
| wt-verifier | Validate acceptance criteria, evidence, and completion readiness before DONE transitions | Verification reports |
| wt-visualizer | Generate burndown charts, dependency graphs, timeline views | Visual dashboards (ASCII/Mermaid) |
| wt-auditor | Cross-file integrity checks, template compliance, orphan detection | Audit reports |

**Invocation**: Use `/worktracker` skill for work item management.

**WTI Rules Enforced**: WTI-002 (No Closure Without Verification), WTI-003 (Truthful State), WTI-006 (Evidence-Based Closure)

**AST Enforcement (H-33):** All wt-* agents have Bash tool access and MUST use `jerry ast` CLI commands (`uv run --directory ${CLAUDE_PLUGIN_ROOT} jerry ast frontmatter`, `jerry ast validate`, etc.) for frontmatter extraction and entity validation. Regex-based frontmatter parsing (`> **Status:**` grep) is prohibited.

---

## Transcript Skill Agents

These agents parse, extract, and format transcript files.

| Agent | File | Role | Cognitive Mode |
|-------|------|------|----------------|
| ts-parser | `skills/transcript/agents/ts-parser.md` | Transcript Parsing Orchestrator | Convergent |
| ts-extractor | `skills/transcript/agents/ts-extractor.md` | Entity Extractor | Divergent |
| ts-formatter | `skills/transcript/agents/ts-formatter.md` | Output Formatter | Convergent |
| ts-mindmap-ascii | `skills/transcript/agents/ts-mindmap-ascii.md` | ASCII Mind Map Generator | Convergent |
| ts-mindmap-mermaid | `skills/transcript/agents/ts-mindmap-mermaid.md` | Mermaid Mind Map Generator | Convergent |

**Key Capabilities:**

| Agent | Primary Use Case | Output Type |
|-------|------------------|-------------|
| ts-parser | VTT/SRT/plain text parsing with Python delegation (Strategy Pattern orchestrator) | canonical-transcript.json, chunks/ |
| ts-extractor | Extract entities (people, topics, decisions) from parsed transcripts | extraction-report.json |
| ts-formatter | Format transcripts as markdown, text, or structured output | Formatted transcript files |
| ts-mindmap-ascii | Generate ASCII mind maps from transcript structure | ASCII diagrams |
| ts-mindmap-mermaid | Generate Mermaid mind maps from transcript structure | Mermaid diagrams |

**Invocation**: Use `/transcript` skill for transcript processing.

**Hybrid Architecture**: ts-parser delegates VTT files to Python parser (1,250x cost reduction), uses LLM fallback for SRT/plain text.

---

## Diataxis Skill Agents

These agents implement Diataxis four-quadrant documentation methodology through the `/diataxis` skill. Four writer agents produce quadrant-specific documentation, a classifier routes requests to the correct quadrant, and an auditor evaluates existing documentation quality.

| Agent | File | Role | Cognitive Mode |
|-------|------|------|----------------|
| diataxis-tutorial | `skills/diataxis/agents/diataxis-tutorial.md` | Tutorial Writer | Systematic |
| diataxis-howto | `skills/diataxis/agents/diataxis-howto.md` | How-To Guide Writer | Systematic |
| diataxis-reference | `skills/diataxis/agents/diataxis-reference.md` | Reference Writer | Systematic |
| diataxis-explanation | `skills/diataxis/agents/diataxis-explanation.md` | Explanation Writer | Divergent |
| diataxis-classifier | `skills/diataxis/agents/diataxis-classifier.md` | Documentation Classifier | Convergent |
| diataxis-auditor | `skills/diataxis/agents/diataxis-auditor.md` | Documentation Auditor | Systematic |

**Key Capabilities:**

| Agent | Primary Use Case | Output Type |
|-------|------------------|-------------|
| diataxis-tutorial | Learning-oriented docs with step-by-step guided experience | Tutorial documents |
| diataxis-howto | Goal-oriented docs for competent users solving specific problems | How-to guide documents |
| diataxis-reference | Information-oriented docs with structured, neutral descriptions | Reference documents |
| diataxis-explanation | Understanding-oriented docs with context, connections, and rationale | Explanation documents |
| diataxis-classifier | Classify requests into Diataxis quadrants using two-axis test | Classification results |
| diataxis-auditor | Audit existing docs against per-quadrant quality criteria | Audit reports |

**Invocation**: Use `/diataxis` skill. Classifier routes requests; writer agents produce documents; auditor evaluates quality.

**Model Tiers:** diataxis-explanation (opus), diataxis-classifier (haiku); all others (sonnet).

**Tool Tiers:** diataxis-classifier and diataxis-auditor are T1 (read-only); all writer agents are T2 (read-write).

**Artifact Location**: `projects/${JERRY_PROJECT}/docs/{quadrant}/{topic-slug}.md`

---

## MCP Tool Access

Agents with MCP (Model Context Protocol) tool access for external documentation lookup and cross-session memory.

### Context7 (Documentation Lookup)

| Agent | Skill | Tools |
|-------|-------|-------|
| ps-researcher | problem-solving | resolve-library-id, query-docs |
| ps-analyst | problem-solving | resolve-library-id, query-docs |
| ps-architect | problem-solving | resolve-library-id, query-docs |
| ps-investigator | problem-solving | resolve-library-id, query-docs |
| ps-synthesizer | problem-solving | resolve-library-id, query-docs |
| nse-explorer | nasa-se | resolve-library-id, query-docs |
| nse-architecture | nasa-se | resolve-library-id, query-docs |
| eng-architect | eng-team | resolve-library-id, query-docs |
| eng-lead | eng-team | resolve-library-id, query-docs |
| eng-backend | eng-team | resolve-library-id, query-docs |
| eng-frontend | eng-team | resolve-library-id, query-docs |
| eng-infra | eng-team | resolve-library-id, query-docs |
| eng-devsecops | eng-team | resolve-library-id, query-docs |
| eng-qa | eng-team | resolve-library-id, query-docs |
| eng-security | eng-team | resolve-library-id, query-docs |
| eng-reviewer | eng-team | resolve-library-id, query-docs |
| eng-incident | eng-team | resolve-library-id, query-docs |
| red-lead | red-team | resolve-library-id, query-docs |
| red-recon | red-team | resolve-library-id, query-docs |
| red-vuln | red-team | resolve-library-id, query-docs |
| red-exploit | red-team | resolve-library-id, query-docs |
| red-privesc | red-team | resolve-library-id, query-docs |
| red-lateral | red-team | resolve-library-id, query-docs |
| red-persist | red-team | resolve-library-id, query-docs |
| red-exfil | red-team | resolve-library-id, query-docs |
| red-reporter | red-team | resolve-library-id, query-docs |
| red-infra | red-team | resolve-library-id, query-docs |
| red-social | red-team | resolve-library-id, query-docs |

### Memory-Keeper (Cross-Session Persistence)

| Agent | Skill | Tools |
|-------|-------|-------|
| orch-planner | orchestration | store, retrieve, search |
| orch-tracker | orchestration | store, retrieve, search |
| orch-synthesizer | orchestration | retrieve, search |
| ps-architect | problem-solving | store, retrieve, search |
| nse-requirements | nasa-se | store, retrieve, search |
| ts-parser | transcript | store, retrieve |
| ts-extractor | transcript | store, retrieve |

> **Not included (by design):** adv-* (self-contained strategy execution), sb-* (voice quality gate), wt-* (read-only auditing), ps-critic/ps-validator (quality evaluation), ps-reporter (report generation). eng-*/red-* agents do not use Memory-Keeper; their persistence model uses file-based output per P-002 (engagement-scoped output directories), not cross-session MCP storage.

---

## Framework Voice Skill Agents

These agents are scoped to the `saucer-boy-framework-voice` skill (internal, not user-invocable).

| Agent | File | Role | Cognitive Mode |
|-------|------|------|----------------|
| `sb-reviewer` | `skills/saucer-boy-framework-voice/agents/sb-reviewer.md` | Voice compliance review — evaluates text against 5 Authenticity Tests | convergent |
| `sb-rewriter` | `skills/saucer-boy-framework-voice/agents/sb-rewriter.md` | Voice transformation — rewrites framework output to Saucer Boy voice | divergent |
| `sb-calibrator` | `skills/saucer-boy-framework-voice/agents/sb-calibrator.md` | Voice fidelity scoring — scores text on 0-1 scale across 5 voice traits | convergent |

**Progressive Disclosure**: Agents load reference files on-demand to minimize context window usage. Always-load files vary by agent (sb-rewriter: voice-guide.md + vocabulary-reference.md; sb-calibrator: voice-guide.md; sb-reviewer: SKILL.md body only).

---

## Session Voice Skill Agents

This agent is scoped to the `saucer-boy` skill and invoked via `/saucer-boy`.

| Agent | File | Role | Cognitive Mode |
|-------|------|------|----------------|
| `sb-voice` | `skills/saucer-boy/agents/sb-voice.md` | Session conversational voice — McConkey personality for work sessions | divergent |

**Two Modes**: Ambient session personality (always-on during session) and explicit McConkey invocation (on-demand persona responses). Personality disengages for hard stops, security, governance, and user override (P-020).

---

## Eng-Team Skill Agents

These agents implement secure software engineering methodology through the `/eng-team` skill, covering the full SDLC with security hardening at every phase. Follows an 8-step sequential phase-gate workflow with NIST SSDF governance, Microsoft SDL phases, OWASP ASVS verification, SLSA supply chain integrity, and DevSecOps automation patterns.

| Agent | File | Role | Cognitive Mode |
|-------|------|------|----------------|
| eng-architect | `skills/eng-team/agents/eng-architect.md` | Solution Architect and Threat Modeler | Strategic |
| eng-lead | `skills/eng-team/agents/eng-lead.md` | Engineering Lead and Standards Enforcer | Convergent |
| eng-backend | `skills/eng-team/agents/eng-backend.md` | Secure Backend Engineer | Systematic |
| eng-frontend | `skills/eng-team/agents/eng-frontend.md` | Secure Frontend Engineer | Systematic |
| eng-infra | `skills/eng-team/agents/eng-infra.md` | Secure Infrastructure Engineer | Systematic |
| eng-devsecops | `skills/eng-team/agents/eng-devsecops.md` | DevSecOps Pipeline Engineer | Systematic |
| eng-qa | `skills/eng-team/agents/eng-qa.md` | Security QA Engineer | Systematic |
| eng-security | `skills/eng-team/agents/eng-security.md` | Security Code Review Specialist | Forensic |
| eng-reviewer | `skills/eng-team/agents/eng-reviewer.md` | Final Review Gate and Quality Enforcer | Convergent |
| eng-incident | `skills/eng-team/agents/eng-incident.md` | Incident Response Specialist | Forensic |

**Key Capabilities:**

| Agent | Primary Use Case | Output Type |
|-------|------------------|-------------|
| eng-architect | System design, architecture decisions, threat modeling (STRIDE/DREAD/PASTA) | Architecture decision records, threat models |
| eng-lead | Implementation planning, code standards enforcement, dependency governance | Implementation plans, standards mappings |
| eng-backend | Server-side implementation with OWASP Top 10 and ASVS 5.0 compliance | Secure backend code, API security artifacts |
| eng-frontend | Client-side implementation with XSS prevention, CSP, CORS hardening | Secure frontend code, CSP configurations |
| eng-infra | IaC security, container hardening, SBOM generation, SLSA compliance | Infrastructure configurations, SBOMs |
| eng-devsecops | SAST/DAST pipeline integration, secrets scanning, dependency analysis | Pipeline configurations, scan reports |
| eng-qa | Security test strategy, fuzzing campaigns, property-based testing | Test artifacts, coverage reports |
| eng-security | Manual secure code review against CWE Top 25 and OWASP ASVS | Finding reports with CWE classifications |
| eng-reviewer | Final gate with /adversary integration for C2+ at >= 0.95 threshold | Quality scores, compliance status |
| eng-incident | Incident response runbooks, vulnerability lifecycle management | IR plans, monitoring configurations |

**Invocation**: Use `/eng-team` skill which orchestrates these agents in an 8-step sequential phase-gate workflow.

**Model Tiers:** eng-architect (opus), eng-reviewer (opus); all others (sonnet).

**Artifact Location**: `skills/eng-team/output/{engagement-id}/`

---

## Red-Team Skill Agents

These agents implement offensive security methodology through the `/red-team` skill, covering the full MITRE ATT&CK kill chain (14/14 tactics). Follows a non-linear workflow with mandatory scope authorization (red-lead first), circuit breaker checks at every agent transition, and RoE-gated agents for high-impact operations. Follows PTES, OSSTMM, and NIST SP 800-115 methodologies.

| Agent | File | Role | Cognitive Mode |
|-------|------|------|----------------|
| red-lead | `skills/red-team/agents/red-lead.md` | Engagement Lead & Scope Authority | Strategic |
| red-recon | `skills/red-team/agents/red-recon.md` | Reconnaissance Specialist | Divergent |
| red-vuln | `skills/red-team/agents/red-vuln.md` | Vulnerability Analyst | Systematic |
| red-exploit | `skills/red-team/agents/red-exploit.md` | Exploitation Specialist | Systematic |
| red-privesc | `skills/red-team/agents/red-privesc.md` | Privilege Escalation Specialist | Systematic |
| red-lateral | `skills/red-team/agents/red-lateral.md` | Lateral Movement Specialist | Systematic |
| red-persist | `skills/red-team/agents/red-persist.md` | Persistence Specialist (RoE-GATED) | Systematic |
| red-exfil | `skills/red-team/agents/red-exfil.md` | Data Exfiltration Specialist (RoE-GATED) | Systematic |
| red-reporter | `skills/red-team/agents/red-reporter.md` | Engagement Reporter & Documentation Specialist | Integrative |
| red-infra | `skills/red-team/agents/red-infra.md` | Infrastructure & Tooling Specialist | Systematic |
| red-social | `skills/red-team/agents/red-social.md` | Social Engineering Specialist (RoE-GATED) | Divergent |

**Key Capabilities:**

| Agent | Primary Use Case | Output Type |
|-------|------------------|-------------|
| red-lead | Scope establishment, RoE definition, authorization management | Scope documents, RoE YAML |
| red-recon | OSINT, network enumeration, service discovery, attack surface mapping | Reconnaissance reports |
| red-vuln | Vulnerability identification, CVE research, exploit availability assessment | Vulnerability reports with risk scores |
| red-exploit | Exploit methodology, payload crafting guidance, vulnerability chaining | Exploitation methodology reports |
| red-privesc | Local/domain privilege escalation, credential harvesting, token manipulation | Privilege escalation reports |
| red-lateral | Network pivoting, tunneling, living-off-the-land techniques | Lateral movement reports |
| red-persist | Backdoor placement methodology, scheduled tasks, rootkit analysis (RoE-GATED) | Persistence methodology reports |
| red-exfil | Data exfiltration channels, covert communication, DLP bypass (RoE-GATED) | Exfiltration methodology reports |
| red-reporter | Engagement reports, finding documentation, executive summaries | Final engagement reports |
| red-infra | C2 framework management, payload building, redirector infrastructure | Infrastructure methodology reports |
| red-social | Phishing campaigns, pretexting, vishing methodology (RoE-GATED) | Social engineering methodology reports |

**Invocation**: Use `/red-team` skill. red-lead MUST establish scope first (mandatory). After scope, any agent is invocable in any order.

**Model Tiers:** red-lead (opus), red-reporter (opus); all others (sonnet).

**Artifact Location**: `skills/red-team/output/{engagement-id}/`

**RoE-Gated Agents:** red-persist, red-exfil, red-social require explicit authorization in the Rules of Engagement beyond standard scope authorization.

---

## Agent Handoff Protocol

### Triggering Handoffs

Handoffs are triggered by:
1. **Hook-based**: `scripts/subagent_stop.py` detects completion
2. **Explicit**: Parent agent delegates via Task tool
3. **Skill-based**: Skill orchestrator routes to appropriate specialist

### Handoff Data

When handing off between agents, include:
```json
{
  "from_agent": "ps-researcher",
  "to_agent": "ps-analyst",
  "context": {
    "task_id": "WORK-123",
    "artifacts": ["research/proj-001-e-001-research.md"],
    "summary": "Completed initial research on architecture patterns"
  },
  "request": "Analyze findings and identify gaps"
}
```

---

## Adding New Agents

New agents should be added within their respective skill directory:

1. Create agent file in `skills/{skill-name}/agents/{agent-name}.md`
2. Define persona, responsibilities, and constraints
3. Register in this file (AGENTS.md) under the skill section
4. Update skill orchestrator to know about the new agent
5. Add relevant hooks if needed

### Agent File Template

```markdown
---
name: {agent-name}
description: |
  Use this agent when {trigger conditions}.
  <example>User: "{example prompt}"</example>
model: sonnet
tools:
  - Read
  - Grep
  - Glob
---

# {Agent Name}

## Persona
{One paragraph describing the agent's character and expertise}

## Responsibilities
- {Primary responsibility}
- {Secondary responsibility}
- ...

## Constraints
- {What this agent should NOT do}
- {Boundaries of authority}

## Input Format
{What information this agent needs to start work}

## Output Format
{What this agent produces when done}

## Handoff Triggers
{When this agent should hand off to another}
```
