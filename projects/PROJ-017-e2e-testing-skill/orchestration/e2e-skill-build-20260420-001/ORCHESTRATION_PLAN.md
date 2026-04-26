# E2E Testing Skill Build: Orchestration Plan

> **Document ID:** PROJ-017-ORCH-PLAN
> **Project:** PROJ-017-e2e-testing-skill
> **Workflow ID:** `e2e-skill-build-20260420-001`
> **Status:** AWAITING USER APPROVAL — DO NOT EXECUTE
> **Version:** 1.1
> **Created:** 2026-04-20
> **Last Updated:** 2026-04-20
> **Change 1.0 → 1.1:** Phase 1 (single 3-researcher fan-out) decomposed into three-stage layered discovery — Phase 1a Landscape Scan (2 agents), Phase 1b Deep Research fan-out (11 agents), Phase 1c Lane Synthesis (2 agents) — to achieve depth per topic and richer inputs flowing into downstream analysis.

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [1. Executive Summary](#1-executive-summary) | What this workflow builds and why |
| [2. Workflow Architecture](#2-workflow-architecture) | ASCII diagram, pipeline layout, pattern classification |
| [3. Phase Definitions](#3-phase-definitions) | Per-phase agent, input, output, gate table |
| [4. Quality Gate Specifications](#4-quality-gate-specifications) | Gate threshold, strategies, criticality (C3), iteration limits |
| [5. Agent Registry](#5-agent-registry) | Full agent roster with roles and artifact paths |
| [6. State Management](#6-state-management) | ORCHESTRATION.yaml schema excerpt |
| [7. Execution Constraints](#7-execution-constraints) | Hard rules, web-search enforcement, HARD threshold 0.94 |
| [8. Success Criteria](#8-success-criteria) | Per-phase exit criteria and workflow completion criteria |
| [9. Risk Mitigations](#9-risk-mitigations) | Failure modes and recovery paths |
| [10. Resumption Context](#10-resumption-context) | Current state snapshot and next actions |
| [11. Pending User Approval](#11-pending-user-approval) | Assumptions, open questions, go/no-go decision point |

---

## 1. Executive Summary

### L0 — Stakeholder Summary

This workflow builds a brand-new Jerry skill called `e2e-testing` that gives Claude a structured, expert playbook for end-to-end testing of web-based services — including the emerging class of agentic flows where an AI agent drives a browser or API sequence autonomously. Right now Jerry has no skill dedicated to E2E testing; engineers who ask for E2E help get ad-hoc responses with no consistent methodology.

The workflow begins with a three-stage discovery: a rapid landscape scan to identify the top candidates (industry standards and agentic innovators), followed by dedicated per-topic deep research by an individual agent for each candidate, followed by lane-level synthesis that distills the deep-dives into coherent recommendations. That layered knowledge then feeds a master synthesis, which is turned into a polished skill with documented agents, prompt templates, and a validation mechanism that confirms the skill actually produces tests that verify an application works — not just tests that run without errors.

Every phase passes a strict quality gate (0.94 composite score, stricter than Jerry's default 0.92) before the next phase begins.

### L1 — Engineering Summary

**Workflow pattern:** Three-Stage Fan-Out (Phase 1a → 1b → 1c) → Fan-In / Master Synthesis (Phase 2) → Sequential Pipeline (Phases 3–5)

**Pipeline layout:** Single logical pipeline (`e2e-build`) with a three-stage layered discovery in Phase 1 followed by master synthesis and sequential skill-build phases.

**Criticality:** C3 (Significant) — new skill authoring touches `.context/rules/` compliance surface (H-25..H-30, AE-002), spans >10 files across `skills/`, `projects/`, and potentially `CLAUDE.md` / `AGENTS.md`, and takes >1 day to reverse if the skill is incorrectly registered.

**Quality threshold:** 0.94 (HARD — user-specified, overrides H-13 default of 0.92). This threshold applies at every adversarial gate.

**Phases:** 7 phases (1a, 1b, 1c, 2, 3, 4, 5), 6 adversarial gates (1a, 1b, 1c, 2, 3, 5), 1 lightweight fan-out in Phase 1a (2 parallel landscape scanners), 1 major fan-out in Phase 1b (11 parallel deep researchers), 1 parallel fan-out in Phase 1c (2 lane synthesizers).

**Target deliverable:** `skills/e2e-testing/` — SKILL.md, agent definitions, prompt templates, validation checks, optional PLAYBOOK.md and examples.

### L2 — Architect Summary

**Criticality classification:** C3 per AE-002 (touches rules compliance surface via H-25..H-30 registration; new skill file set spans >10 files). No AE-001/AE-004 triggers (no constitutional or ADR baseline modification).

**Required adversarial strategies (C3):** S-007 (Constitutional AI Critique), S-002 (Devil's Advocate), S-014 (LLM-as-Judge), S-004 (Pre-Mortem), S-012 (FMEA), S-013 (Inversion). Optional: S-001, S-003, S-010, S-011.

**Gate 1a note:** Scope is intentionally narrow — lightweight verification that each candidate is real, has a live URL, and the selection rationale is sound. Full C3 strategy set still applies at threshold 0.94.

**Data sources:** Three live web search engines (Bing, Google, DuckDuckGo) for all landscape and deep-research web agents. Local filesystem (eng-team skill cache) for ps-researcher-engteam only. Web search is FORBIDDEN for ps-researcher-engteam.

**Workflow ID:** `e2e-skill-build-20260420-001` (user-specified format; auto-confirmed)
**Base path:** `projects/PROJ-017-e2e-testing-skill/orchestration/e2e-skill-build-20260420-001/`

**Orchestration Pattern:** Three-Stage Fan-Out (Patterns 3+6) into Sequential Pipeline (Pattern 2).

---

## 2. Workflow Architecture

### 2.1 Pipeline Diagram (ASCII)

```
WORKFLOW: e2e-skill-build-20260420-001
BASE PATH: projects/PROJ-017-e2e-testing-skill/orchestration/e2e-skill-build-20260420-001/
PIPELINE:  e2e-build
========================================================================

           ┌──────────────────────────────────────────────────────┐
           │         PHASE 1a: LANDSCAPE SCAN (PARALLEL)          │
           │  2 agents — identify top 5 candidates per lane       │
           └────────────────────┬─────────────────────────────────┘
                                │
               ┌────────────────┴────────────────┐
               ▼                                 ▼
┌──────────────────────────┐       ┌──────────────────────────┐
│  ps-researcher-landscape │       │  ps-researcher-landscape │
│  -standards              │       │  -innovators             │
│                          │       │                          │
│  TOP 5 standard          │       │  TOP 5 agentic           │
│  candidates              │       │  innovator candidates    │
│  Briefing card per       │       │  Briefing card per       │
│  candidate (name,        │       │  candidate (name,        │
│  rationale, live URL)    │       │  rationale, live URL)    │
│                          │       │                          │
│  WEB SEARCH REQUIRED     │       │  WEB SEARCH REQUIRED     │
│  Bing + Google + DDG     │       │  Bing + Google + DDG     │
│                          │       │                          │
│  Output:                 │       │  Output:                 │
│  research/landscape/     │       │  research/landscape/     │
│  standards-candidates.md │       │  innovators-candidates.md│
└────────────┬─────────────┘       └─────────────┬────────────┘
             └─────────────────┬─────────────────┘
                               ▼
          ╔════════════════════════════════════════════╗
          ║         ADVERSARY GATE 1a (lightweight)    ║
          ║  /adversary: adv-selector → adv-executor   ║
          ║              → adv-scorer                  ║
          ║                                            ║
          ║  Narrow scope: each of the 10 candidates   ║
          ║  is real, has a live URL, rationale sound  ║
          ║                                            ║
          ║  Criticality: C3                           ║
          ║  Threshold:   >= 0.94 (HARD)               ║
          ║  Strategies:  S-007, S-002, S-014,         ║
          ║               S-004, S-012, S-013          ║
          ║  Max iterations: 3 → ESCALATE per AE-006   ║
          ║                                            ║
          ║  Output: adversary-gates/phase1a-score.md  ║
          ╚════════════════════════════════════════════╝
                               │
                               │ PASS (>= 0.94)
                               │ Topics bound from 1a outputs at runtime
                               ▼
           ┌──────────────────────────────────────────────────────┐
           │     PHASE 1b: DEEP RESEARCH (PARALLEL FAN-OUT)       │
           │  11 agents — one per candidate + eng-team baseline   │
           │  Topics bound at runtime from Phase 1a outputs       │
           └───────────────────────┬──────────────────────────────┘
                                   │
     ┌──────────┬──────────┬───────┴──────┬──────────┬──────────┐
     ▼          ▼          ▼              ▼          ▼          ▼
┌─────────┐┌─────────┐┌─────────┐   ┌─────────┐┌─────────┐┌─────────┐
│ std-1   ││ std-2   ││ std-3   │...│ inn-1   ││ inn-2   ││ engteam │
│ deep    ││ deep    ││ deep    │   │ deep    ││ deep    ││ baseline│
│ dive    ││ dive    ││ dive    │   │ dive    ││ dive    ││ (LOCAL) │
│         ││         ││         │   │         ││         ││ NO WEB  │
│ 8-15    ││ 8-15    ││ 8-15    │   │ 8-15    ││ 8-15    ││ SEARCH  │
│ queries ││ queries ││ queries │   │ queries ││ queries ││         │
│ WEB REQ ││ WEB REQ ││ WEB REQ │   │ WEB REQ ││ WEB REQ ││         │
└────┬────┘└────┬────┘└────┬────┘   └────┬────┘└────┬────┘└────┬────┘
     │          │          │             │          │          │
     └──────────┴──────────┴──────┬──────┴──────────┴──────────┘
                (5 standards + 5 innovators + 1 eng-team = 11 total)
                                   │
          ╔════════════════════════════════════════════╗
          ║       ADVERSARY GATE 1b (substantive)      ║
          ║  /adversary: adv-selector → adv-executor   ║
          ║              → adv-scorer                  ║
          ║                                            ║
          ║  Scope: all 11 deep-research outputs        ║
          ║  Primary quality gate for discovery lane   ║
          ║  Below threshold → revise weak researchers ║
          ║                                            ║
          ║  Criticality: C3                           ║
          ║  Threshold:   >= 0.94 (HARD)               ║
          ║  Strategies:  S-007, S-002, S-014,         ║
          ║               S-004, S-012, S-013          ║
          ║  Max iterations: 3 → ESCALATE per AE-006   ║
          ║                                            ║
          ║  Output: adversary-gates/phase1b-score.md  ║
          ╚════════════════════════════════════════════╝
                               │
                               │ PASS (>= 0.94)
                               ▼
           ┌──────────────────────────────────────────────────────┐
           │        PHASE 1c: LANE SYNTHESIS (PARALLEL)           │
           │  2 agents — one per lane                             │
           └────────────────────┬─────────────────────────────────┘
                                │
               ┌────────────────┴────────────────┐
               ▼                                 ▼
┌──────────────────────────┐       ┌──────────────────────────┐
│  ps-synthesizer-         │       │  ps-synthesizer-         │
│  standards               │       │  innovators              │
│                          │       │                          │
│  Combines 5 standards    │       │  Combines 5 innovator    │
│  deep-dives: common      │       │  deep-dives: common      │
│  patterns, unique        │       │  patterns, unique        │
│  features, reconciled    │       │  features, reconciled    │
│  recommendations         │       │  recommendations         │
│                          │       │                          │
│  Output:                 │       │  Output:                 │
│  synthesis/              │       │  synthesis/              │
│  lane-standards.md       │       │  lane-innovators.md      │
└────────────┬─────────────┘       └─────────────┬────────────┘
             └─────────────────┬─────────────────┘
                               ▼
          ╔════════════════════════════════════════════╗
          ║         ADVERSARY GATE 1c                  ║
          ║  /adversary: adv-selector → adv-executor   ║
          ║              → adv-scorer                  ║
          ║                                            ║
          ║  Scope: lane-standards.md + lane-          ║
          ║         innovators.md                      ║
          ║                                            ║
          ║  Criticality: C3                           ║
          ║  Threshold:   >= 0.94 (HARD)               ║
          ║  Strategies:  S-007, S-002, S-014,         ║
          ║               S-004, S-012, S-013          ║
          ║  Max iterations: 3 → ESCALATE per AE-006   ║
          ║                                            ║
          ║  Output: adversary-gates/phase1c-score.md  ║
          ╚════════════════════════════════════════════╝
                               │
                               │ PASS (>= 0.94)
                               ▼
           ┌──────────────────────────────────────────────────────┐
           │        PHASE 2: MASTER SYNTHESIS (FAN-IN)            │
           │  ps-synthesizer reads lane-standards.md,             │
           │  lane-innovators.md, and eng-team baseline           │
           │  directly; produces unified 10-principle spec        │
           │  plus reconciliation with eng-team baseline          │
           │                                                      │
           │  Output: synthesis/e2e-skill-requirements.md         │
           └────────────────────┬─────────────────────────────────┘
                                │
          ╔════════════════════════════════════════════╗
          ║         ADVERSARY GATE 2 (PHASE 2)         ║
          ║  /adversary: adv-selector → adv-executor   ║
          ║              → adv-scorer                  ║
          ║                                            ║
          ║  Criticality: C3                           ║
          ║  Threshold:   >= 0.94 (HARD)               ║
          ║  Strategies:  S-007, S-002, S-014,         ║
          ║               S-004, S-012, S-013          ║
          ║  Max iterations: 3 → ESCALATE per AE-006   ║
          ║                                            ║
          ║  Output: adversary-gates/phase2-score.md   ║
          ╚════════════════════════════════════════════╝
                               │
                               │ PASS (>= 0.94)
                               ▼
           ┌──────────────────────────────────────────────────────┐
           │         PHASE 3: SKILL DESIGN                        │
           │  Sequential (eng-team lane):                         │
           │                                                      │
           │  Step A — eng-lead:                                  │
           │    Implementation plan (file layout,                 │
           │    agent roster, template inventory,                 │
           │    cross-skill integration)                          │
           │    Output: design/implementation-plan.md             │
           │                                                      │
           │  Step B — eng-architect:                             │
           │    Skill architecture (agent responsi-               │
           │    bilities, prompt structure, validation            │
           │    check strategy)                                   │
           │    Output: design/skill-architecture.md              │
           └────────────────────┬─────────────────────────────────┘
                                │
          ╔════════════════════════════════════════════╗
          ║         ADVERSARY GATE 3 (PHASE 3)         ║
          ║  /adversary: adv-selector → adv-executor   ║
          ║              → adv-scorer                  ║
          ║                                            ║
          ║  Criticality: C3                           ║
          ║  Threshold:   >= 0.94 (HARD)               ║
          ║  Strategies:  S-007, S-002, S-014,         ║
          ║               S-004, S-012, S-013          ║
          ║  Max iterations: 3 → ESCALATE per AE-006   ║
          ║                                            ║
          ║  Output: adversary-gates/phase3-score.md   ║
          ╚════════════════════════════════════════════╝
                               │
                               │ PASS (>= 0.94)
                               ▼
           ┌──────────────────────────────────────────────────────┐
           │         PHASE 4: BUILD                               │
           │  Sequential artifact authoring                       │
           │  (eng-team lane):                                    │
           │                                                      │
           │  Step A — eng-lead:                                  │
           │    Author SKILL.md per H-25..H-30                    │
           │    Output: skills/e2e-testing/SKILL.md               │
           │                                                      │
           │  Step B — eng-qa:                                    │
           │    Author prompt templates + validation              │
           │    checks (core of the skill)                        │
           │    Output:                                           │
           │      skills/e2e-testing/templates/                   │
           │      skills/e2e-testing/validation/                  │
           │                                                      │
           │  Step C — eng-architect:                             │
           │    Author agent definition files                     │
           │    (e2e-author + e2e-verifier + others)              │
           │    Output: skills/e2e-testing/agents/                │
           └────────────────────┬─────────────────────────────────┘
                                │
          ╔════════════════════════════════════════════╗
          ║         ADVERSARY GATE 4 (PHASE 5)         ║
          ║  eng-reviewer: full skill review vs.        ║
          ║  H-25..H-30 standards                      ║
          ║                                            ║
          ║  /adversary final pass:                    ║
          ║  Criticality: C3                           ║
          ║  Threshold:   >= 0.94 (HARD)               ║
          ║  Strategies (REQUIRED):                    ║
          ║    S-007 Constitutional AI Critique        ║
          ║    S-002 Devil's Advocate                  ║
          ║    S-014 LLM-as-Judge                      ║
          ║    S-004 Pre-Mortem Analysis               ║
          ║    S-012 FMEA                              ║
          ║    S-013 Inversion Technique               ║
          ║  Max iterations: 3 → ESCALATE per AE-006   ║
          ║                                            ║
          ║  Output: adversary-gates/phase5-score.md   ║
          ╚════════════════════════════════════════════╝
                               │
                               │ PASS (>= 0.94)
                               ▼
           ┌──────────────────────────────────────────────────────┐
           │                WORKFLOW COMPLETE                      │
           │  skills/e2e-testing/ — ready for                     │
           │  H-30 registration review                            │
           └──────────────────────────────────────────────────────┘
```

### 2.2 Orchestration Pattern Classification

| Pattern | Applied | Description |
|---------|---------|-------------|
| Fan-Out (small) | Yes — Phase 1a | 2 landscape scanners execute in parallel |
| Barrier Sync | Yes — Gate 1a | Lightweight gate blocks deep research until candidates are validated |
| Fan-Out (large) | Yes — Phase 1b | 11 deep researchers execute in parallel (dynamic topic binding from 1a) |
| Barrier Sync | Yes — Gate 1b | Primary discovery quality gate; blocks lane synthesis |
| Fan-Out (small) | Yes — Phase 1c | 2 lane synthesizers execute in parallel |
| Barrier Sync | Yes — Gate 1c | Validates lane syntheses before master synthesis |
| Fan-In | Yes — Phase 2 | ps-synthesizer aggregates lane-standards.md + lane-innovators.md + eng-team baseline |
| Sequential | Yes — Phases 2-5 | Each phase waits for prior phase gate PASS |
| Hierarchical | Yes | Orchestrator delegates; workers do not spawn |

---

## 3. Phase Definitions

### Phase 1a — Landscape Scan (Parallel, 2 agents)

**Execution mode:** PARALLEL — both landscape agents run concurrently.

**Purpose:** Identify the TOP 5 candidates per lane with a short briefing card each (name, 2-3 sentence rationale, primary live URL). This phase does NOT go deep — it maps the terrain so Phase 1b can dispatch a dedicated deep researcher per candidate.

| Agent | Lane | Search Enforcement | Inputs | Output Artifact |
|-------|------|--------------------|--------|-----------------|
| ps-researcher-landscape-standards | Industry Standards | MUST use WebSearch/WebFetch. MUST NOT rely on training data. Every finding MUST include a live URL citation with access date. | None | `research/landscape/standards-candidates.md` |
| ps-researcher-landscape-innovators | Agentic E2E Innovators | MUST use WebSearch/WebFetch. MUST NOT rely on training data. Every finding MUST include a live URL citation with access date. | None | `research/landscape/innovators-candidates.md` |

**ps-researcher-landscape-standards — Detailed Prompt Constraints (baked in):**

```
LANDSCAPE STANDARDS RESEARCHER — EXECUTION INSTRUCTIONS (non-negotiable):

You MUST search the live web before writing any finding.
Forbidden: Relying on LLM training data to answer this question.
Required:   Use WebSearch and WebFetch (Bing + Google + DuckDuckGo) with queries such as:
  - "end to end testing web services industry standard 2025 2026"
  - "top e2e testing frameworks standards 2025"
  - "ISTQB e2e testing standard overview"
  - "W3C WebDriver standard end to end"
  - "Playwright Cypress OWASP BDD e2e testing standard candidates 2026"

Task: Identify the TOP 5 industry standard candidates for E2E testing of
web-based services. For each produce a SHORT briefing card:
  - Name of the standard / framework
  - 2-3 sentence rationale for why it is a top candidate
  - Primary live URL (retrieved during this session, not memorised)
  - Access date

Do NOT go deep. Breadth only. Output MUST be a structured list of exactly 5 candidates.
Output file: research/landscape/standards-candidates.md
```

**ps-researcher-landscape-innovators — Detailed Prompt Constraints (baked in):**

```
LANDSCAPE INNOVATORS RESEARCHER — EXECUTION INSTRUCTIONS (non-negotiable):

You MUST search the live web before writing any finding.
Forbidden: Relying on LLM training data to answer this question.
Required:   Use WebSearch and WebFetch (Bing + Google + DuckDuckGo) with queries such as:
  - "agentic e2e testing innovators 2025 2026"
  - "LLM-driven test generation web services leaders"
  - "AI test agent autonomous browser testing companies tools"
  - "self-healing tests AI 2025 top innovators"
  - "autonomous browser agent testing startup tool 2026"

Task: Identify the TOP 5 agentic E2E testing innovators (tools, projects, companies,
or research groups). For each produce a SHORT briefing card:
  - Name of the innovator / tool / project
  - 2-3 sentence rationale for why they are a top candidate
  - Primary live URL (retrieved during this session, not memorised)
  - Access date

Do NOT go deep. Breadth only. Output MUST be a structured list of exactly 5 candidates.
Output file: research/landscape/innovators-candidates.md
```

**Gate 1a (Lightweight Adversary Gate):**
- Trigger: Both landscape agents COMPLETE
- Input: `research/landscape/standards-candidates.md`, `research/landscape/innovators-candidates.md`
- Agent sequence: `adv-selector` → `adv-executor` → `adv-scorer`
- Narrow scope: verifies each of the 10 candidates is real, has a live URL with access date, and selection rationale is sound
- Threshold: **>= 0.94** (HARD)
- Below threshold: Revision loop to the specific landscape researcher(s) with weak candidates
- Max iterations: 3; on 3rd failure → human escalation per AE-006
- Output: `adversary-gates/phase1a-score.md`

---

### Phase 1b — Deep Research (Parallel Fan-Out, 11 agents)

**Execution mode:** PARALLEL — all 11 agents run concurrently. Dynamic fan-out: topics for ps-researcher-std-1..std-5 and ps-researcher-inn-1..inn-5 are bound at runtime from the Phase 1a landscape outputs after Gate 1a PASS. The specific standard or innovator each agent targets is unknown at plan time.

**Purpose:** One dedicated deep researcher per candidate from Phase 1a goes in depth on that single topic. Plus the eng-team baseline researcher runs in parallel. Each web-facing researcher performs 8–15 targeted queries and multiple WebFetch reads on their specific topic.

**Standard deep researchers (ps-researcher-std-1 through ps-researcher-std-5):**

| Agent | Topic binding | Search Enforcement | Output Artifact |
|-------|--------------|-------------------|-----------------|
| ps-researcher-std-1 | Standard #1 from 1a (runtime) | MUST use WebSearch/WebFetch (Bing+Google+DDG). MUST NOT rely on training data. 8-15 queries minimum. All findings MUST include live URL citations with access dates. | `research/deep-standards/std-1-{slug}.md` |
| ps-researcher-std-2 | Standard #2 from 1a (runtime) | Same enforcement | `research/deep-standards/std-2-{slug}.md` |
| ps-researcher-std-3 | Standard #3 from 1a (runtime) | Same enforcement | `research/deep-standards/std-3-{slug}.md` |
| ps-researcher-std-4 | Standard #4 from 1a (runtime) | Same enforcement | `research/deep-standards/std-4-{slug}.md` |
| ps-researcher-std-5 | Standard #5 from 1a (runtime) | Same enforcement | `research/deep-standards/std-5-{slug}.md` |

**Innovator deep researchers (ps-researcher-inn-1 through ps-researcher-inn-5):**

| Agent | Topic binding | Search Enforcement | Output Artifact |
|-------|--------------|-------------------|-----------------|
| ps-researcher-inn-1 | Innovator #1 from 1a (runtime) | MUST use WebSearch/WebFetch (Bing+Google+DDG). MUST NOT rely on training data. 8-15 queries minimum. All findings MUST include live URL citations with access dates. | `research/deep-innovators/inn-1-{slug}.md` |
| ps-researcher-inn-2 | Innovator #2 from 1a (runtime) | Same enforcement | `research/deep-innovators/inn-2-{slug}.md` |
| ps-researcher-inn-3 | Innovator #3 from 1a (runtime) | Same enforcement | `research/deep-innovators/inn-3-{slug}.md` |
| ps-researcher-inn-4 | Innovator #4 from 1a (runtime) | Same enforcement | `research/deep-innovators/inn-4-{slug}.md` |
| ps-researcher-inn-5 | Innovator #5 from 1a (runtime) | Same enforcement | `research/deep-innovators/inn-5-{slug}.md` |

**Eng-team baseline researcher (ps-researcher-engteam):**

| Agent | Data Source | Search Enforcement | Inputs | Output Artifact |
|-------|-------------|-------------------|--------|-----------------|
| ps-researcher-engteam | Local filesystem ONLY | MUST NOT use WebSearch or WebFetch. Read local files only. | Eng-team skill at `/Users/victor.lau/.claude/plugins/cache/jerry-framework/jerry/0.29.1/skills/eng-team/` | `research/deep-engteam/eng-team-testing-baseline.md` |

**Template: Deep Researcher Prompt Constraints (web — applies to all std and inn agents, baked in per-agent with topic substituted):**

```
DEEP RESEARCHER [{topic_name}] — EXECUTION INSTRUCTIONS (non-negotiable):

Your sole focus is: {topic_name} (as identified in research/landscape/{lane}-candidates.md).

You MUST search the live web before writing any finding.
Forbidden: Relying on LLM training data to answer this question.
Required:   Use WebSearch and WebFetch (Bing + Google + DuckDuckGo).
            Minimum 8 targeted queries. Minimum 3 WebFetch reads of primary source pages.

Every finding in your output MUST include:
  - A live URL retrieved during this session (not a memorised URL)
  - The date the page was accessed
  - A direct quote or paraphrase from the retrieved content

Produce a concentrated deep-dive on {topic_name} covering:
  1. What it specifies or what the project/tool does (detailed)
  2. Scope: what testing scenarios does it address or enable?
  3. Applicability to a Jerry E2E skill: where does it fit, how would it be used?
  4. Strengths: what does it do particularly well?
  5. Weaknesses or gaps: what does it not cover?
  6. At least 5 live URL citations with access dates

Output file: research/deep-{lane}/{id}-{slug}.md
```

**ps-researcher-engteam — Detailed Prompt Constraints (baked in):**

```
ENG-TEAM BASELINE RESEARCHER — EXECUTION INSTRUCTIONS (non-negotiable):

You MUST read local files ONLY. Web search is FORBIDDEN for this task.
Data source: /Users/victor.lau/.claude/plugins/cache/jerry-framework/jerry/0.29.1/skills/eng-team/

Required reads (at minimum):
  - SKILL.md (full file — orchestration flow, quality gates, agent roster)
  - agents/eng-qa.md (test methodology, OWASP categories, fuzzing strategy)
  - agents/eng-reviewer.md (gate patterns, /adversary integration, thresholds)
  - agents/eng-architect.md (if present — threat modeling methodology)
  - Any composition/ or templates/ directories

Extract and document:
  1. The eng-qa agent's test design methodology (threat-driven, OWASP mapping,
     boundary analysis, fuzzing, property-based testing)
  2. The testing standards the skill references (OWASP TG, NIST SSDF, pytest,
     AFL++, Hypothesis, coverage.py)
  3. The eng-reviewer gate patterns and quality thresholds
  4. The 8-step sequential workflow and where testing fits (Steps 5-6)
  5. Any test methodology or test artifact conventions baked into the skill
  6. Gaps: what eng-team does NOT cover that a dedicated e2e-testing skill
     would need to fill

Output file: research/deep-engteam/eng-team-testing-baseline.md
```

**Gate 1b (Substantive Adversary Gate — Primary Discovery Gate):**
- Trigger: All 11 deep researchers COMPLETE
- Input: All 10 deep-standards and deep-innovators files + `research/deep-engteam/eng-team-testing-baseline.md`
- Agent sequence: `adv-selector` → `adv-executor` → `adv-scorer`
- Scope: All 11 deep-research outputs collectively assessed
- This is the primary quality gate for the discovery lane
- Below threshold: Revision loop to the specific weak deep researcher(s) identified in the critique
- Threshold: **>= 0.94** (HARD)
- Max iterations: 3; on 3rd failure → human escalation per AE-006
- Output: `adversary-gates/phase1b-score.md`

---

### Phase 1c — Lane Synthesis (Parallel, 2 agents)

**Execution mode:** PARALLEL — both lane synthesizers run concurrently.

**Purpose:** Combine the per-topic deep-dives within each lane into a unified lane-level synthesis. Identifies common patterns, unique features, and produces reconciled recommendations ready for master synthesis.

| Agent | Inputs | Output Artifact |
|-------|--------|-----------------|
| ps-synthesizer-standards | `research/deep-standards/std-1-*.md` through `std-5-*.md` | `synthesis/lane-standards.md` |
| ps-synthesizer-innovators | `research/deep-innovators/inn-1-*.md` through `inn-5-*.md` | `synthesis/lane-innovators.md` |

**ps-synthesizer-standards task:** Combine the 5 standards deep-dives into a unified standards synthesis. Must deliver:
- Common patterns across the 5 standards
- Unique features each standard contributes
- Reconciled recommendations: which standards are most relevant to a Jerry E2E skill and why
- Ranking or prioritisation rationale
- Gaps identified across the standards landscape collectively

**ps-synthesizer-innovators task:** Same structure for the 5 innovator deep-dives:
- Common patterns across the 5 innovators
- Unique innovations each contributes
- Reconciled recommendations: which innovators' approaches are most applicable to a Jerry agentic E2E skill
- Ranking or prioritisation rationale
- Gaps in the innovator landscape collectively

**Gate 1c:**
- Trigger: Both lane synthesizers COMPLETE
- Input: `synthesis/lane-standards.md`, `synthesis/lane-innovators.md`
- Agent sequence: `adv-selector` → `adv-executor` → `adv-scorer`
- Threshold: **>= 0.94** (HARD)
- Below threshold: Revision loop to the specific lane synthesizer(s) with critique
- Max iterations: 3; on 3rd failure → human escalation per AE-006
- Output: `adversary-gates/phase1c-score.md`

---

### Phase 2 — Master Synthesis (Fan-In)

**Execution mode:** SEQUENTIAL (single agent).

| Agent | Inputs | Output Artifact |
|-------|--------|-----------------|
| ps-synthesizer | `synthesis/lane-standards.md` (from 1c) + `synthesis/lane-innovators.md` (from 1c) + `research/deep-engteam/eng-team-testing-baseline.md` (direct — not part of lane syntheses) | `synthesis/e2e-skill-requirements.md` |

**Synthesizer task:** Produce a unified "what good looks like" specification for the E2E testing skill. Must deliver:
1. 10 distilled principles: 5 from the standards lane synthesis, 5 from the innovators lane synthesis
2. Reconciliation with eng-team baseline (direct input): what to reuse, what to extend, what gaps to fill
3. Proposed agent roster for the new skill (at minimum: e2e-author, e2e-verifier)
4. Proposed validation strategy: how will the skill prove an application actually works, not just that tests run without errors?
5. Proposed prompt template inventory

**Phase 2 Gate (Adversary Gate 2):**
- Trigger: ps-synthesizer COMPLETE
- Input: `synthesis/e2e-skill-requirements.md`
- Agent sequence: `adv-selector` → `adv-executor` → `adv-scorer`
- Threshold: **>= 0.94** (HARD)
- Below threshold: Revision loop to ps-synthesizer with critic feedback
- Max iterations: 3; on 3rd failure → human escalation per AE-006
- Output: `adversary-gates/phase2-score.md`

---

### Phase 3 — Skill Design (Sequential, Eng-Team Lane)

**Execution mode:** SEQUENTIAL — Step A must complete before Step B starts.

| Step | Agent | Inputs | Output Artifact |
|------|-------|--------|-----------------|
| A | eng-lead | Phase 2 synthesis + Gate 2 score | `design/implementation-plan.md` |
| B | eng-architect | Phase 2 synthesis + implementation plan | `design/skill-architecture.md` |

**eng-lead task (Step A):** Produce implementation plan covering:
- File layout for `skills/e2e-testing/` (full directory tree)
- Agent roster: names, roles, skill source patterns (referencing eng-qa and eng-reviewer as models)
- Prompt template inventory (what templates are needed and why)
- Integration map: which existing Jerry skills does e2e-testing call upon or complement
- H-25..H-30 compliance checklist for the planned files
- Registration plan: CLAUDE.md, AGENTS.md, mandatory-skill-usage.md entries (note: mandatory-skill-usage.md edit triggers AE-002)

**eng-architect task (Step B):** Produce skill architecture covering:
- Agent responsibility matrix (who creates, who validates, who gates)
- Prompt template structure: how templates parametrise E2E scenarios, how they handle agentic flows differently from conventional UI tests
- Validation-check strategy: the mechanism by which the skill proves the application under test actually behaves correctly (not just "tests ran") — this is the core design challenge
- State-passing schema between e2e-author and e2e-verifier
- Failure-mode catalogue and recovery design

**Phase 3 Gate (Adversary Gate 3):**
- Trigger: eng-architect COMPLETE
- Input: `design/implementation-plan.md`, `design/skill-architecture.md`
- Agent sequence: `adv-selector` → `adv-executor` → `adv-scorer`
- Threshold: **>= 0.94** (HARD)
- Below threshold: Revision loop targeting the weaker design artifact
- Max iterations: 3; on 3rd failure → human escalation per AE-006
- Output: `adversary-gates/phase3-score.md`

---

### Phase 4 — Build (Sequential, Eng-Team Lane)

**Execution mode:** SEQUENTIAL — Steps A, B, C in order.

| Step | Agent | Inputs | Primary Output Location |
|------|-------|--------|------------------------|
| A | eng-lead | Phase 3 design artifacts | `skills/e2e-testing/SKILL.md` |
| B | eng-qa | SKILL.md + Phase 3 architecture | `skills/e2e-testing/templates/`, `skills/e2e-testing/validation/` |
| C | eng-architect | SKILL.md + templates + Phase 3 architecture | `skills/e2e-testing/agents/` |

**eng-lead task (Step A):** Author `skills/e2e-testing/SKILL.md` conforming strictly to H-25..H-30:
- YAML frontmatter with `name`, `description` (WHAT + WHEN + trigger phrases, <1024 chars, no XML), `version`, `allowed-tools`, `activation-keywords`
- Body: Document Sections navigation table, Triple-Lens audience table, Purpose, When to Use, Available Agents, P-003 Compliance diagram, domain content, Constitutional Compliance, References, Footer
- No `README.md` in skill folder (H-27)
- All file references use full repo-relative paths (H-29)

**eng-qa task (Step B):** Author prompt templates and validation checks. This is the heart of the skill — eng-qa owns it because it encapsulates Jerry's test methodology. Deliverables:
- `skills/e2e-testing/templates/e2e-test-generation.md` — prompt template for generating E2E tests for conventional web service scenarios
- `skills/e2e-testing/templates/e2e-agentic-flow.md` — prompt template for generating E2E tests for agentic flow scenarios (LLM-driven browser actions, multi-step agent chains)
- `skills/e2e-testing/templates/e2e-validation-check.md` — prompt template for the verifier agent to assess whether generated tests actually verify application behavior
- `skills/e2e-testing/validation/validation-strategy.md` — the written strategy document: how does the skill prove the app works? Criteria for distinguishing "test ran" from "test verified application correctness". Coverage dimensions specific to E2E (happy path, failure path, boundary, agentic divergence).

**eng-architect task (Step C):** Author agent definition files in `skills/e2e-testing/agents/`:
- `e2e-author.md` — Creates E2E test suites from scenario descriptions. Writes Playwright/Cypress/WebDriver tests or equivalent agentic test scripts.
- `e2e-verifier.md` — Reviews test artifacts to confirm they actually verify application correctness (not just syntactic validity). Applies validation-check template.
- Additional agents per the Phase 3 roster (if Phase 3 specified more): e.g., `e2e-analyst.md` for test result analysis, `e2e-reporter.md` for coverage reports.

Each agent file MUST follow the eng-team agent pattern: identity block, methodology, workflow integration, output requirements (L0/L1/L2), standards reference, tool integration (3 degradation levels), constitutional compliance.

No phase 4 adversary gate — Phase 5 is the final quality gate for all Phase 4 artifacts.

---

### Phase 5 — Final Quality Gate

**Execution mode:** SEQUENTIAL — eng-reviewer runs first, then /adversary.

| Step | Agent | Inputs | Output Artifact |
|------|-------|--------|-----------------|
| A | eng-reviewer | All `skills/e2e-testing/` artifacts | `adversary-gates/phase5-review.md` |
| B | /adversary (adv-selector → adv-executor → adv-scorer) | All `skills/e2e-testing/` artifacts + eng-reviewer output | `adversary-gates/phase5-score.md` |

**eng-reviewer task:** Full skill review against Jerry skill standards:
- H-25: SKILL.md casing and file name
- H-26: Folder name is kebab-case matching `name` frontmatter field
- H-27: No README.md present
- H-28: Frontmatter description is WHAT + WHEN + triggers, <1024 chars, no XML
- H-29: All file references use full repo-relative paths
- H-30: Registration plan covers CLAUDE.md, AGENTS.md, mandatory-skill-usage.md
- Navigation table present and correct (H-23, H-24)
- Agent files follow eng-team pattern (3 degradation levels, constitutional compliance)
- Validation-check strategy is substantive (proves app works, not just tests compile)
- Produce GO/NO-GO with itemized findings

**Adversary Gate 4 (Phase 5):**
- Threshold: **>= 0.94** (HARD)
- Required strategies (C3): S-007 Constitutional AI Critique, S-002 Devil's Advocate, S-014 LLM-as-Judge, S-004 Pre-Mortem Analysis, S-012 FMEA, S-013 Inversion Technique
- Max iterations: 3; on 3rd failure → human escalation per AE-006
- PASS → workflow COMPLETE; skill ready for H-30 registration

---

## 4. Quality Gate Specifications

### 4.1 Threshold Configuration

| Parameter | Value | Authority |
|-----------|-------|-----------|
| Quality threshold | **0.94** | User-specified HARD override (exceeds H-13 default of 0.92) |
| Criticality | **C3** (Significant) | AE-002: new skill touches H-25..H-30 rules surface; >10 files; >1 day reversal |
| Scoring mechanism | S-014 (LLM-as-Judge) | quality-enforcement.md SSOT |
| Minimum iterations | 3 (creator → critic → revision) | H-14 |
| Max iterations before escalation | 3 | AE-006 |

### 4.2 Scoring Dimensions (S-014)

| Dimension | Weight |
|-----------|--------|
| Completeness | 0.20 |
| Internal Consistency | 0.20 |
| Methodological Rigor | 0.20 |
| Evidence Quality | 0.15 |
| Actionability | 0.15 |
| Traceability | 0.10 |

### 4.3 Required Strategies Per Gate (C3)

| Strategy | ID | Application |
|---------|----|-------------|
| LLM-as-Judge | S-014 | Quantitative scoring via 6-dimension rubric |
| Devil's Advocate | S-002 | Challenge hidden assumptions in deliverable |
| Constitutional AI Critique | S-007 | Verify compliance with Jerry Constitution and H-25..H-30 |
| Pre-Mortem Analysis | S-004 | What would cause this phase output to fail? |
| FMEA | S-012 | Failure mode and effects on downstream phases |
| Inversion Technique | S-013 | How would we make this deliverable wrong? |

Optional (available but not required): S-001 Red Team, S-003 Steelman, S-010 Self-Refine, S-011 Chain-of-Verification.

### 4.4 Gate Summary (6 Gates Total)

| Gate | Phase | Scope | Threshold | Note |
|------|-------|-------|-----------|------|
| Gate 1a | Phase 1a | 10 landscape candidate briefing cards | >= 0.94 | Lightweight — verifies realness, live URLs, rationale soundness |
| Gate 1b | Phase 1b | All 11 deep-research outputs | >= 0.94 | Primary discovery quality gate |
| Gate 1c | Phase 1c | 2 lane syntheses | >= 0.94 | Validates lane-level synthesis before master synthesis |
| Gate 2 | Phase 2 | Master synthesis document | >= 0.94 | Full C3 adversary pass |
| Gate 3 | Phase 3 | Design artifacts (implementation plan + architecture) | >= 0.94 | Full C3 adversary pass |
| Gate 5 | Phase 5 | Complete `skills/e2e-testing/` deliverable | >= 0.94 | Full C3 adversary pass; final gate |

### 4.5 Gate Outcome Decision Table

| Score | Band | Action |
|-------|------|--------|
| >= 0.94 | PASS | Phase proceeds |
| 0.85 – 0.93 | REVISE | Targeted revision; return to creator with critic feedback |
| < 0.85 | REJECTED | Significant rework; return to creator with full critique |
| 3rd iteration below 0.94 | ESCALATE | Human review required per AE-006 |

---

## 5. Agent Registry

| Phase | Step | Agent | Execution Mode | Primary Output | Status |
|-------|------|-------|---------------|----------------|--------|
| 1a | A | ps-researcher-landscape-standards | PARALLEL | `research/landscape/standards-candidates.md` | PENDING |
| 1a | B | ps-researcher-landscape-innovators | PARALLEL | `research/landscape/innovators-candidates.md` | PENDING |
| 1a-gate | — | adv-selector → adv-executor → adv-scorer | SEQUENTIAL | `adversary-gates/phase1a-score.md` | PENDING |
| 1b | std-1 | ps-researcher-std-1 (topic: runtime binding) | PARALLEL | `research/deep-standards/std-1-{slug}.md` | PENDING |
| 1b | std-2 | ps-researcher-std-2 (topic: runtime binding) | PARALLEL | `research/deep-standards/std-2-{slug}.md` | PENDING |
| 1b | std-3 | ps-researcher-std-3 (topic: runtime binding) | PARALLEL | `research/deep-standards/std-3-{slug}.md` | PENDING |
| 1b | std-4 | ps-researcher-std-4 (topic: runtime binding) | PARALLEL | `research/deep-standards/std-4-{slug}.md` | PENDING |
| 1b | std-5 | ps-researcher-std-5 (topic: runtime binding) | PARALLEL | `research/deep-standards/std-5-{slug}.md` | PENDING |
| 1b | inn-1 | ps-researcher-inn-1 (topic: runtime binding) | PARALLEL | `research/deep-innovators/inn-1-{slug}.md` | PENDING |
| 1b | inn-2 | ps-researcher-inn-2 (topic: runtime binding) | PARALLEL | `research/deep-innovators/inn-2-{slug}.md` | PENDING |
| 1b | inn-3 | ps-researcher-inn-3 (topic: runtime binding) | PARALLEL | `research/deep-innovators/inn-3-{slug}.md` | PENDING |
| 1b | inn-4 | ps-researcher-inn-4 (topic: runtime binding) | PARALLEL | `research/deep-innovators/inn-4-{slug}.md` | PENDING |
| 1b | inn-5 | ps-researcher-inn-5 (topic: runtime binding) | PARALLEL | `research/deep-innovators/inn-5-{slug}.md` | PENDING |
| 1b | engteam | ps-researcher-engteam (LOCAL ONLY) | PARALLEL | `research/deep-engteam/eng-team-testing-baseline.md` | PENDING |
| 1b-gate | — | adv-selector → adv-executor → adv-scorer | SEQUENTIAL | `adversary-gates/phase1b-score.md` | PENDING |
| 1c | A | ps-synthesizer-standards | PARALLEL | `synthesis/lane-standards.md` | PENDING |
| 1c | B | ps-synthesizer-innovators | PARALLEL | `synthesis/lane-innovators.md` | PENDING |
| 1c-gate | — | adv-selector → adv-executor → adv-scorer | SEQUENTIAL | `adversary-gates/phase1c-score.md` | PENDING |
| 2 | — | ps-synthesizer | SEQUENTIAL | `synthesis/e2e-skill-requirements.md` | PENDING |
| 2-gate | — | adv-selector → adv-executor → adv-scorer | SEQUENTIAL | `adversary-gates/phase2-score.md` | PENDING |
| 3 | A | eng-lead | SEQUENTIAL | `design/implementation-plan.md` | PENDING |
| 3 | B | eng-architect | SEQUENTIAL | `design/skill-architecture.md` | PENDING |
| 3-gate | — | adv-selector → adv-executor → adv-scorer | SEQUENTIAL | `adversary-gates/phase3-score.md` | PENDING |
| 4 | A | eng-lead | SEQUENTIAL | `skills/e2e-testing/SKILL.md` | PENDING |
| 4 | B | eng-qa | SEQUENTIAL | `skills/e2e-testing/templates/`, `skills/e2e-testing/validation/` | PENDING |
| 4 | C | eng-architect | SEQUENTIAL | `skills/e2e-testing/agents/` | PENDING |
| 5 | A | eng-reviewer | SEQUENTIAL | `adversary-gates/phase5-review.md` | PENDING |
| 5-gate | — | adv-selector → adv-executor → adv-scorer | SEQUENTIAL | `adversary-gates/phase5-score.md` | PENDING |

**Total distinct agent invocations (discovery phases 1a+1b+1c):** 15 (2 landscape + 11 deep research + 2 lane synthesizers)
**Total distinct agent invocations (all phases):** 28
**Total adversary gate invocations:** 6 (each = 3-agent sequence: adv-selector → adv-executor → adv-scorer)
**Phases:** 7 (1a, 1b, 1c, 2, 3, 4, 5)

> Note: Agent count increased significantly from v1.0 (14 invocations, 4 gates) to v1.1 (28 invocations, 6 gates) to achieve per-topic depth in the discovery stage.

---

## 6. State Management

### 6.1 State Files

| File | Purpose |
|------|---------|
| `ORCHESTRATION_PLAN.md` | This file — strategic context (human-readable) |
| `ORCHESTRATION.yaml` | Machine-readable state SSOT |

### 6.2 Artifact Path Structure

All workflow artifacts use the dynamic base path. Final skill deliverables land directly in `skills/e2e-testing/` (outside the workflow directory, by design — they are the permanent output).

```
projects/PROJ-017-e2e-testing-skill/
└── orchestration/
    └── e2e-skill-build-20260420-001/         ← WORKFLOW BASE
        ├── ORCHESTRATION_PLAN.md              ← This file
        ├── ORCHESTRATION.yaml                 ← Machine state
        ├── research/
        │   ├── landscape/
        │   │   ├── standards-candidates.md    ← Phase 1a: landscape standards output
        │   │   └── innovators-candidates.md   ← Phase 1a: landscape innovators output
        │   ├── deep-standards/
        │   │   ├── std-1-{slug}.md            ← Phase 1b: per-standard deep dives (×5)
        │   │   ├── std-2-{slug}.md
        │   │   ├── std-3-{slug}.md
        │   │   ├── std-4-{slug}.md
        │   │   └── std-5-{slug}.md
        │   ├── deep-innovators/
        │   │   ├── inn-1-{slug}.md            ← Phase 1b: per-innovator deep dives (×5)
        │   │   ├── inn-2-{slug}.md
        │   │   ├── inn-3-{slug}.md
        │   │   ├── inn-4-{slug}.md
        │   │   └── inn-5-{slug}.md
        │   └── deep-engteam/
        │       └── eng-team-testing-baseline.md  ← Phase 1b: eng-team baseline
        ├── synthesis/
        │   ├── lane-standards.md              ← Phase 1c: standards lane synthesis
        │   ├── lane-innovators.md             ← Phase 1c: innovators lane synthesis
        │   └── e2e-skill-requirements.md      ← Phase 2: master synthesis output
        ├── design/
        │   ├── implementation-plan.md         ← Phase 3: eng-lead output
        │   └── skill-architecture.md          ← Phase 3: eng-architect output
        └── adversary-gates/
            ├── phase1a-score.md               ← Gate 1a: landscape validation
            ├── phase1b-score.md               ← Gate 1b: deep research gate
            ├── phase1c-score.md               ← Gate 1c: lane synthesis gate
            ├── phase2-score.md                ← Gate 2: master synthesis gate
            ├── phase3-score.md                ← Gate 3: design gate
            ├── phase5-review.md               ← Phase 5: eng-reviewer output
            └── phase5-score.md                ← Gate 5 (final adversary gate)

skills/e2e-testing/                            ← PERMANENT DELIVERABLE
    ├── SKILL.md
    ├── agents/
    │   ├── e2e-author.md
    │   ├── e2e-verifier.md
    │   └── (additional agents per Phase 3 roster)
    ├── templates/
    │   ├── e2e-test-generation.md
    │   ├── e2e-agentic-flow.md
    │   └── e2e-validation-check.md
    ├── validation/
    │   └── validation-strategy.md
    └── (optional: PLAYBOOK.md, examples/)
```

### 6.3 ORCHESTRATION.yaml Schema Excerpt

```yaml
workflow:
  id: "e2e-skill-build-20260420-001"
  name: "E2E Testing Skill Build"
  project_id: "PROJ-017-e2e-testing-skill"
  status: "PLANNED"
  id_source: "user"
  id_format: "semantic-date-seq"
  version: "1.1"

paths:
  base: "projects/PROJ-017-e2e-testing-skill/orchestration/e2e-skill-build-20260420-001/"
  research_landscape: "{base}research/landscape/"
  research_deep_standards: "{base}research/deep-standards/"
  research_deep_innovators: "{base}research/deep-innovators/"
  research_deep_engteam: "{base}research/deep-engteam/"
  synthesis: "{base}synthesis/"
  design: "{base}design/"
  adversary_gates: "{base}adversary-gates/"
  skill_output: "skills/e2e-testing/"

data_sources:
  web_researchers:
    - name: "Bing"
      url: "https://www.bing.com"
      used_by: ["ps-researcher-landscape-standards", "ps-researcher-landscape-innovators",
                "ps-researcher-std-1", "ps-researcher-std-2", "ps-researcher-std-3",
                "ps-researcher-std-4", "ps-researcher-std-5",
                "ps-researcher-inn-1", "ps-researcher-inn-2", "ps-researcher-inn-3",
                "ps-researcher-inn-4", "ps-researcher-inn-5"]
      mandatory: true
    - name: "Google"
      url: "https://www.google.com"
      used_by: ["ps-researcher-landscape-standards", "ps-researcher-landscape-innovators",
                "ps-researcher-std-1", "ps-researcher-std-2", "ps-researcher-std-3",
                "ps-researcher-std-4", "ps-researcher-std-5",
                "ps-researcher-inn-1", "ps-researcher-inn-2", "ps-researcher-inn-3",
                "ps-researcher-inn-4", "ps-researcher-inn-5"]
      mandatory: true
    - name: "DuckDuckGo"
      url: "https://duckduckgo.com"
      used_by: ["ps-researcher-landscape-standards", "ps-researcher-landscape-innovators",
                "ps-researcher-std-1", "ps-researcher-std-2", "ps-researcher-std-3",
                "ps-researcher-std-4", "ps-researcher-std-5",
                "ps-researcher-inn-1", "ps-researcher-inn-2", "ps-researcher-inn-3",
                "ps-researcher-inn-4", "ps-researcher-inn-5"]
      mandatory: true
  local_sources:
    - name: "eng-team skill (v0.29.1 plugin cache)"
      path: "/Users/victor.lau/.claude/plugins/cache/jerry-framework/jerry/0.29.1/skills/eng-team/"
      used_by: ["ps-researcher-engteam"]
      web_search_forbidden: true

pipelines:
  e2e-build:
    short_alias: "e2e-build"
    skill_source: "orchestration"
    phases:
      - id: "1a"
        name: "Landscape Scan"
        execution_mode: "PARALLEL"
        status: "PENDING"
        agents:
          - id: "ps-researcher-landscape-standards"
            status: "PENDING"
            artifact: "{paths.research_landscape}standards-candidates.md"
          - id: "ps-researcher-landscape-innovators"
            status: "PENDING"
            artifact: "{paths.research_landscape}innovators-candidates.md"
      - id: "1b"
        name: "Deep Research"
        execution_mode: "PARALLEL"
        status: "PENDING"
        topic_binding: "runtime — from phase 1a outputs after Gate 1a PASS"
        agents:
          - id: "ps-researcher-std-1"
            status: "PENDING"
            artifact: "{paths.research_deep_standards}std-1-{slug}.md"
          - id: "ps-researcher-std-2"
            status: "PENDING"
            artifact: "{paths.research_deep_standards}std-2-{slug}.md"
          - id: "ps-researcher-std-3"
            status: "PENDING"
            artifact: "{paths.research_deep_standards}std-3-{slug}.md"
          - id: "ps-researcher-std-4"
            status: "PENDING"
            artifact: "{paths.research_deep_standards}std-4-{slug}.md"
          - id: "ps-researcher-std-5"
            status: "PENDING"
            artifact: "{paths.research_deep_standards}std-5-{slug}.md"
          - id: "ps-researcher-inn-1"
            status: "PENDING"
            artifact: "{paths.research_deep_innovators}inn-1-{slug}.md"
          - id: "ps-researcher-inn-2"
            status: "PENDING"
            artifact: "{paths.research_deep_innovators}inn-2-{slug}.md"
          - id: "ps-researcher-inn-3"
            status: "PENDING"
            artifact: "{paths.research_deep_innovators}inn-3-{slug}.md"
          - id: "ps-researcher-inn-4"
            status: "PENDING"
            artifact: "{paths.research_deep_innovators}inn-4-{slug}.md"
          - id: "ps-researcher-inn-5"
            status: "PENDING"
            artifact: "{paths.research_deep_innovators}inn-5-{slug}.md"
          - id: "ps-researcher-engteam"
            status: "PENDING"
            artifact: "{paths.research_deep_engteam}eng-team-testing-baseline.md"
      - id: "1c"
        name: "Lane Synthesis"
        execution_mode: "PARALLEL"
        status: "PENDING"
        agents:
          - id: "ps-synthesizer-standards"
            status: "PENDING"
            artifact: "{paths.synthesis}lane-standards.md"
          - id: "ps-synthesizer-innovators"
            status: "PENDING"
            artifact: "{paths.synthesis}lane-innovators.md"
      - id: 2
        name: "Master Synthesis"
        execution_mode: "SEQUENTIAL"
        status: "PENDING"
        agents:
          - id: "ps-synthesizer"
            status: "PENDING"
            artifact: "{paths.synthesis}e2e-skill-requirements.md"
      - id: 3
        name: "Skill Design"
        execution_mode: "SEQUENTIAL"
        status: "PENDING"
        agents:
          - id: "eng-lead"
            status: "PENDING"
            artifact: "{paths.design}implementation-plan.md"
          - id: "eng-architect"
            status: "PENDING"
            artifact: "{paths.design}skill-architecture.md"
      - id: 4
        name: "Build"
        execution_mode: "SEQUENTIAL"
        status: "PENDING"
        agents:
          - id: "eng-lead"
            status: "PENDING"
            artifact: "{paths.skill_output}SKILL.md"
          - id: "eng-qa"
            status: "PENDING"
            artifact: "{paths.skill_output}templates/ and {paths.skill_output}validation/"
          - id: "eng-architect"
            status: "PENDING"
            artifact: "{paths.skill_output}agents/"
      - id: 5
        name: "Final Quality Gate"
        execution_mode: "SEQUENTIAL"
        status: "PENDING"
        agents:
          - id: "eng-reviewer"
            status: "PENDING"
            artifact: "{paths.adversary_gates}phase5-review.md"
          - id: "adv-scorer"
            status: "PENDING"
            artifact: "{paths.adversary_gates}phase5-score.md"

quality:
  threshold: 0.94                        # HARD — user override; exceeds H-13 default of 0.92
  criticality: "C3"
  scoring_mechanism: "S-014"
  required_strategies:
    - "S-007"   # Constitutional AI Critique
    - "S-002"   # Devil's Advocate
    - "S-014"   # LLM-as-Judge
    - "S-004"   # Pre-Mortem Analysis
    - "S-012"   # FMEA
    - "S-013"   # Inversion Technique
  optional_strategies:
    - "S-001"   # Red Team Analysis
    - "S-003"   # Steelman
    - "S-010"   # Self-Refine
    - "S-011"   # Chain-of-Verification
  gate_scores:
    phase1a:
      scope: "landscape candidate briefing cards (10 total)"
      score: null
      iterations: 0
      status: "PENDING"
    phase1b:
      scope: "all 11 deep-research outputs"
      score: null
      iterations: 0
      status: "PENDING"
    phase1c:
      scope: "lane-standards.md and lane-innovators.md"
      score: null
      iterations: 0
      status: "PENDING"
    phase2:
      scope: "e2e-skill-requirements.md"
      score: null
      iterations: 0
      status: "PENDING"
    phase3:
      scope: "implementation-plan.md and skill-architecture.md"
      score: null
      iterations: 0
      status: "PENDING"
    phase5:
      scope: "complete skills/e2e-testing/ deliverable"
      score: null
      iterations: 0
      status: "PENDING"

metrics:
  phases_total: 7
  agents_total: 28
  adversary_gates_total: 6
  phases_complete: 0
  agents_executed: 0
  gates_passed: 0
```

### 6.4 Checkpoint Strategy

| Trigger | When | Purpose |
|---------|------|---------|
| PHASE_COMPLETE | After each phase (1a, 1b, 1c, 2, 3, 4, 5) | Phase-level rollback point |
| GATE_PASS | After each adversary gate PASS | Gate result preserved before next phase |
| MANUAL | User-triggered | Debug and inspection |

---

## 7. Execution Constraints

### 7.1 Hard Constraints (Jerry Constitution)

| Constraint | ID | Enforcement |
|------------|----|----|
| Single agent nesting | P-003 / H-01 | Orchestrator → Worker only; no worker spawns further workers |
| File persistence | P-002 | All artifacts written to filesystem before phase advances |
| No deception | P-022 / H-03 | Transparent reasoning; limitations disclosed |
| User authority | P-020 / H-02 | User approves gate decisions; no override of user intent |
| Active project required | H-04 | JERRY_PROJECT set to PROJ-017-e2e-testing-skill |

### 7.2 Web Search Enforcement (HARD — baked into Phase 1 prompts)

| Agent | Web Search | Training Data | Constraint Level |
|-------|------------|---------------|-----------------|
| ps-researcher-landscape-standards | REQUIRED (Bing + Google + DDG) | FORBIDDEN | HARD — non-negotiable |
| ps-researcher-landscape-innovators | REQUIRED (Bing + Google + DDG) | FORBIDDEN | HARD — non-negotiable |
| ps-researcher-std-1 through std-5 | REQUIRED (Bing + Google + DDG), min 8 queries | FORBIDDEN | HARD — non-negotiable |
| ps-researcher-inn-1 through inn-5 | REQUIRED (Bing + Google + DDG), min 8 queries | FORBIDDEN | HARD — non-negotiable |
| ps-researcher-engteam | FORBIDDEN | N/A (local files only) | HARD — non-negotiable |

**Enforcement mechanism:** The constraint is embedded in the agent prompt text (Section 3, Phase 1 definitions above) so it survives into execution context and cannot be dropped by summarisation.

### 7.3 Quality Threshold Override (HARD)

**0.94 is the quality threshold for this workflow.** This overrides the H-13 default of 0.92. This value appears in every gate definition and in ORCHESTRATION.yaml. It MUST NOT be relaxed without explicit user instruction.

### 7.4 AE-002 Awareness

Modifying `.context/rules/mandatory-skill-usage.md` to register the new skill's proactive invocation trigger triggers AE-002 (auto-C3 minimum). This is already the criticality level for this workflow, but the executor must be aware that the registration step itself requires a quality gate pass before committing that file.

### 7.5 Soft Constraints

| Constraint | Value | Rationale |
|------------|-------|-----------|
| Max concurrent agents (fan-out Phase 1a) | 2 | Landscape scanners — bounded and short-lived |
| Max concurrent agents (fan-out Phase 1b) | 11 | Deep research — bounded by 10 candidates + 1 eng-team |
| Max concurrent agents (fan-out Phase 1c) | 2 | Lane synthesizers — bounded by 2 lanes |
| Max gate iterations | 3 | AE-006 circuit breaker |
| Checkpoint frequency | PHASE_COMPLETE + GATE_PASS | Recovery granularity |

---

## 8. Success Criteria

### 8.1 Phase-Level Exit Criteria

| Phase | Exit Criterion | Validation |
|-------|---------------|------------|
| 1a | Both landscape files exist; each contains exactly 5 candidates with name, rationale, primary live URL (retrieved in-session), and access date | File existence check + structure check |
| Gate 1a | Composite score >= 0.94; all 10 candidates verified real with live URLs and sound rationale | `adversary-gates/phase1a-score.md` shows PASS |
| 1b | All 11 deep-research files exist; each web-facing file contains minimum 8 queries executed and 5+ live URL citations with access dates; eng-team baseline cites local file paths | File existence check + URL/citation presence check |
| Gate 1b | Composite score >= 0.94 across all 11 outputs | `adversary-gates/phase1b-score.md` shows PASS |
| 1c | Both lane synthesis files exist; each contains cross-topic reconciliation, not just a concatenation of deep-dives | File existence check + content spot check |
| Gate 1c | Composite score >= 0.94 | `adversary-gates/phase1c-score.md` shows PASS |
| 2 | Synthesis document exists; contains exactly 10 principles (5 from standards lane, 5 from innovators lane); reconciliation with eng-team baseline present; proposed agent roster present | Manual review + file existence |
| Gate 2 | Composite score >= 0.94 | `adversary-gates/phase2-score.md` shows PASS |
| 3 | Implementation plan and architecture document both exist; H-25..H-30 compliance checklist in implementation plan; validation-check strategy substantively addressed | File existence + checklist presence |
| Gate 3 | Composite score >= 0.94 | `adversary-gates/phase3-score.md` shows PASS |
| 4 | `skills/e2e-testing/SKILL.md` exists and conforms to H-25..H-30; at minimum e2e-author.md and e2e-verifier.md exist under `skills/e2e-testing/agents/`; at minimum 3 prompt templates exist; validation-strategy.md exists | File existence + H-25..H-30 spot check |
| 5 | eng-reviewer issues GO; adversary gate composite score >= 0.94 | `adversary-gates/phase5-review.md` contains GO; `adversary-gates/phase5-score.md` shows PASS |

### 8.2 Workflow Completion Criteria

| Criterion | Validation |
|-----------|------------|
| All 7 phases COMPLETE | ORCHESTRATION.yaml status = COMPLETE for all phases |
| All 6 gates PASS (>= 0.94) | All gate score files show PASS |
| `skills/e2e-testing/` deliverable in place | Directory exists with SKILL.md, agents/, templates/, validation/ |
| H-30 registration confirmed | User confirms CLAUDE.md, AGENTS.md, mandatory-skill-usage.md entries are correct |

---

## 9. Risk Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Landscape researcher (1a) produces weak or hallucinated candidate | M | H | Gate 1a catches this before candidates become deep-research topics; bad candidates are revised before Phase 1b fan-out is dispatched — preventing 8-15 queries of wasted effort per bad topic |
| Deep researcher picks a weak candidate from 1a landscape (bad candidate slips Gate 1a) | L | M | Gate 1a lightweight adversary check specifically verifies candidate realness and live URLs; any candidate without a verifiable live URL fails the gate; only after Gate 1a PASS are topics bound for Phase 1b |
| Deep researcher (1b std or inn) uses training data instead of live search | M | H | Constraint is baked into per-agent prompt text (Section 3); adv-scorer at Gate 1b must verify URL citations are present with access dates; if no live URLs in a deep-dive → automatic REVISE regardless of other scores |
| ps-researcher-engteam cannot find eng-team cache path | L | M | Path validated before Phase 1b starts; fallback is to read from `skills/eng-team/` in the Jerry workspace if cache path is inaccessible |
| Gate score repeatedly below 0.94 (AE-006 trigger) | L | H | Circuit breaker at 3 iterations → human escalation; plan notes escalation path clearly |
| Phase 1b fan-out of 11 agents causes context exhaustion at C3+ | L | H | AE-006 circuit breaker; state persisted to ORCHESTRATION.yaml at every checkpoint; workflow can resume from last GATE_PASS checkpoint; user may choose to run Phase 1b in two batches (5+5+1) if needed |
| Lane synthesis (1c) is a superficial concatenation, not genuine synthesis | M | M | Gate 1c adversary pass specifically checks for cross-topic reconciliation and genuine synthesis vs. collation; Internal Consistency and Methodological Rigor dimensions score this low if only concatenated |
| Phase 4 Build produces SKILL.md that fails H-25..H-30 | M | M | eng-reviewer in Phase 5 performs explicit H-25..H-30 checklist; eng-lead in Phase 4 Step A uses the compliance checklist from Phase 3 as input |
| Validation-check strategy is superficial (tests run, not verify) | M | H | eng-qa owns validation design; Phase 3 architecture document explicitly requires a substantive strategy; adversary gate will score Evidence Quality and Methodological Rigor low for superficial approaches |
| AE-002 triggered during mandatory-skill-usage.md registration | Certain | M | Already accounted for: workflow is C3 minimum; registration step is last and proceeds only after Phase 5 PASS |
| eng-team plugin cache path changes (machine-specific) | L | M | Plan notes the path assumption; user should confirm or redirect before Phase 1b starts |
| Context compaction at C3+ (AE-006) | L | H | State persisted to ORCHESTRATION.yaml at every checkpoint; workflow can resume from last GATE_PASS checkpoint |

---

## 10. Resumption Context

### 10.1 Current Execution State

```
WORKFLOW STATUS AS OF 2026-04-20
=================================
Status: PLANNED — AWAITING USER APPROVAL

Phase 1a (Landscape Scan):       PENDING
  ps-researcher-landscape-standards:   PENDING
  ps-researcher-landscape-innovators:  PENDING
  Adversary Gate 1a:                   PENDING

Phase 1b (Deep Research):         PENDING
  ps-researcher-std-1:           PENDING  [topic: runtime binding from 1a]
  ps-researcher-std-2:           PENDING  [topic: runtime binding from 1a]
  ps-researcher-std-3:           PENDING  [topic: runtime binding from 1a]
  ps-researcher-std-4:           PENDING  [topic: runtime binding from 1a]
  ps-researcher-std-5:           PENDING  [topic: runtime binding from 1a]
  ps-researcher-inn-1:           PENDING  [topic: runtime binding from 1a]
  ps-researcher-inn-2:           PENDING  [topic: runtime binding from 1a]
  ps-researcher-inn-3:           PENDING  [topic: runtime binding from 1a]
  ps-researcher-inn-4:           PENDING  [topic: runtime binding from 1a]
  ps-researcher-inn-5:           PENDING  [topic: runtime binding from 1a]
  ps-researcher-engteam:         PENDING
  Adversary Gate 1b:             PENDING

Phase 1c (Lane Synthesis):        PENDING
  ps-synthesizer-standards:     PENDING
  ps-synthesizer-innovators:    PENDING
  Adversary Gate 1c:             PENDING

Phase 2 (Master Synthesis):       PENDING
  ps-synthesizer:                PENDING
  Adversary Gate 2:              PENDING

Phase 3 (Skill Design):           PENDING
  eng-lead:                      PENDING
  eng-architect:                 PENDING
  Adversary Gate 3:              PENDING

Phase 4 (Build):                  PENDING
  eng-lead (SKILL.md):           PENDING
  eng-qa (templates/valid.):     PENDING
  eng-architect (agents/):       PENDING

Phase 5 (Final Quality Gate):     PENDING
  eng-reviewer:                  PENDING
  Adversary Gate 4:              PENDING
```

### 10.2 Next Actions (After User Approval)

1. Confirm or redirect project ID (PROJ-017-e2e-testing-skill)
2. Confirm eng-team plugin cache path is accessible at `/Users/victor.lau/.claude/plugins/cache/jerry-framework/jerry/0.29.1/skills/eng-team/`
3. Invoke Phase 1a fan-out — both landscape researchers in parallel
4. After Phase 1a complete → run Adversary Gate 1a
5. On Gate 1a PASS → bind topics from landscape outputs → invoke Phase 1b fan-out (11 deep researchers in parallel)
6. After Phase 1b complete → run Adversary Gate 1b
7. On Gate 1b PASS → invoke Phase 1c fan-out (2 lane synthesizers in parallel)
8. After Phase 1c complete → run Adversary Gate 1c
9. On Gate 1c PASS → invoke ps-synthesizer (Phase 2 Master Synthesis)

---

## 11. Pending User Approval

```
╔══════════════════════════════════════════════════════════════════════╗
║               AWAITING USER APPROVAL — DO NOT EXECUTE               ║
╚══════════════════════════════════════════════════════════════════════╝

PROPOSED PROJECT ID:     PROJ-017-e2e-testing-skill
PROPOSED WORKFLOW ID:    e2e-skill-build-20260420-001
PROPOSED SKILL PATH:     skills/e2e-testing/
QUALITY THRESHOLD:       0.94 (HARD — user specified)
CRITICALITY:             C3

ASSUMPTIONS REQUIRING USER CONFIRMATION:

[ ] A1 — Project ID PROJ-017 is correct and available.
         Next available ID after PROJ-016 is PROJ-017.
         Confirm or redirect.

[ ] A2 — Eng-team plugin cache path is accessible.
         Path: /Users/victor.lau/.claude/plugins/cache/jerry-framework/
               jerry/0.29.1/skills/eng-team/
         ps-researcher-engteam will read from this path. Confirm path is
         correct and readable, or provide an alternative path.

[ ] A3 — Phase 4 No Intermediate Gate.
         Plan has no adversary gate between Phase 4 Build steps.
         The final gate is Phase 5. Confirm this is acceptable, or
         request a gate between Phase 4 Build and Phase 5 Review.

[ ] A4 — Minimum agent roster (e2e-author + e2e-verifier).
         Plan specifies these as the minimum two agents for the skill.
         Additional agents (e.g. e2e-analyst, e2e-reporter) will be
         determined by eng-architect in Phase 3 and Phase 4.
         Confirm or specify a fixed roster now.

[ ] A5 — Optional artifacts scope.
         PLAYBOOK.md and examples/ directory are listed as optional.
         Confirm whether these should be REQUIRED deliverables in
         Phase 4 or remain optional (to be decided by eng-lead).

[ ] A6 — Registration step not in plan phases.
         H-30 registration (CLAUDE.md, AGENTS.md, mandatory-skill-
         usage.md) is listed as a workflow completion criterion but is
         not itself a numbered phase. It is intended as a manual step
         after Phase 5 PASS, reviewed by the user.
         Confirm this is acceptable, or request a Phase 6 for
         registration.

[ ] A7 — 0.94 threshold confirmed as HARD.
         The plan treats 0.94 as a non-negotiable threshold for all
         six gates. Confirm this is correct and intentional.

[ ] A8 — Increased agent fan-out (v1.1 change) is acceptable.
         Version 1.0 had 3 discovery agents. Version 1.1 has 15
         discovery agents (2 landscape + 11 deep research + 2 lane
         synthesizers). This produces richer, per-topic depth but
         significantly increases execution time and context consumption.
         Confirm you are OK with the expanded fan-out and the
         associated execution cost.

OPEN QUESTIONS:

Q1 — Which Playwright/Cypress/WebDriver versions should the E2E
     templates target? Or should the skill be framework-agnostic
     (template-parametric)?

Q2 — Should the skill support only test generation (prompt → test
     code), or also test execution and result interpretation?

Q3 — For agentic E2E flows: should the skill target Claude Computer
     Use / claude-code browser control, or generic LLM-driven
     browser agent frameworks (Playwright MCP, browser-use, etc.)?

Q4 — Should the skill register a proactive invocation trigger in
     mandatory-skill-usage.md? (Triggers AE-002 automatically —
     this is expected and planned for, but user should confirm the
     trigger keyword set.)

USER ACTION REQUIRED:
  Review this plan. Confirm or amend assumptions A1–A8.
  Answer open questions Q1–Q4 (or defer to Phase 3 eng-lead).
  When ready: say "Approved — begin Phase 1a" to start execution.
```

---

## Disclaimer

This orchestration plan was generated by the orch-planner agent (v2.2.0) for PROJ-017-e2e-testing-skill and revised to v1.1 per user instruction on 2026-04-20. The plan is in PLANNED status and has not been executed. Human review is required before any phase runs. All quality thresholds, agent assignments, and artifact paths are proposals subject to user approval.

**Constitutional references:** H-01 (P-003 no recursive subagents), H-02 (P-020 user authority), H-03 (P-022 no deception), H-13 (quality threshold — overridden to 0.94 by user), H-14 (creator-critic-revision cycle), H-25..H-30 (skill standards), AE-002 (mandatory-skill-usage.md edit → C3), AE-006 (token exhaustion escalation).

---

*Document ID: PROJ-017-ORCH-PLAN*
*Workflow ID: e2e-skill-build-20260420-001*
*Version: 1.1*
*Cross-Session Portable: All workflow paths are repository-relative. Skill output paths are repository-relative. Only the eng-team cache path (A2) is machine-local.*
