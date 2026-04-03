# Use Case Capability Build: Orchestration Plan

> **Document ID:** PROJ-021-ORCH-PLAN
> **Workflow ID:** use-case-skills-20260308-001
> **Date:** 2026-03-08
> **Status:** PLANNED
> **Criticality:** C3 (Significant) — governance classification; quality reviews use C4 strategy set
> **Quality Threshold:** >= 0.95 (user override C-008 of default 0.92)
> **Quality Review Level:** C4 (all 10 strategies at every creator output)
> **Max Iterations per Creator-Adversary Loop:** 6
> **GitHub Issue:** #109 — Build use case capability: guided use case authoring, testing specifications, and contract design skills
> **Governing Constraints:** `projects/PROJ-021-use-case/work/prompt-engineering/npt-constraints.md` (C-001 through C-030)

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Workflow Overview](#l0-workflow-overview) | Stakeholder summary |
| [L1: Technical Plan](#l1-technical-plan) | Workflow diagram, phase definitions, agent assignments, barriers |
| [L2: Implementation Details](#l2-implementation-details) | State schema, path configuration, recovery strategies |
| [Operating Constraints](#operating-constraints) | Governing NPT-013 constraint set (C-001 through C-030) |
| [Risk Register](#risk-register) | Known risks and mitigations |
| [Disclaimer](#disclaimer) | Required output disclaimer |

---

## L0: Workflow Overview

This workflow builds three new Jerry skills that together enable **use-case-driven development**: starting from a plain-language description of what a system must do, and ending with verifiable test specifications and implementation contracts.

The three skills are: `/use-case` (guided use case authoring using Jacobson Use Case 2.0 and Cockburn's templates), `/test-spec` (converting use case artifacts into TDD/BDD test plans), and `/contract-design` (generating OpenAPI, CloudEvents, AsyncAPI, and JSON Schema contracts from use case interactions). Each skill stands alone but they form a natural pipeline: understand what the system does → define how to verify it → specify how to build it.

The work proceeds in five sequential phases: deep methodology research, architecture design, skill implementation (strictly ordered — each skill builds on the previous), a security red-team review of the implemented skills, and integration with the Jerry framework. Quality reviews using all 10 C4 adversarial strategies are applied at EVERY individual creator output — not just at phase boundaries — ensuring that no substandard deliverable propagates to a downstream consumer. The main context orchestrates only: it launches creator agents, launches background /adversary agents against each deliverable, routes feedback, and tracks state. It never produces deliverables directly.

---

## L1: Technical Plan

### Creator → Adversary Loop Pattern

Every single agent that produces a deliverable uses this pattern. The main context applies this at every step before releasing output to the next step:

```
Creator Agent (e.g., ps-researcher)
    │
    ▼  Produces deliverable
    │
    ▼  Main context launches background /adversary agent
┌──────────────────────────────────────────────────────┐
│  ADVERSARY C4 REVIEW (background agent)              │
│  All 10 strategies applied:                          │
│  S-014 (LLM-as-Judge), S-003 (Steelman),            │
│  S-013 (Inversion), S-007 (Constitutional),          │
│  S-002 (Devil's Advocate), S-004 (Pre-Mortem),      │
│  S-010 (Self-Refine), S-012 (FMEA),                 │
│  S-011 (Chain-of-Verification), S-001 (Red Team)    │
│  Threshold: >= 0.95  |  Max iterations: 6           │
└─────────────────────┬────────────────────────────────┘
                      │
                      ├── score >= 0.95  →  PASS: output released to next step
                      │
                      ├── score < 0.95, iter < 6  →  feedback to creator
                      │       → creator revises deliverable
                      │       → adversary re-reviews (iter++)
                      │
                      └── iter = 6, score < 0.95  →  ESCALATE to user (RT-M-010)
```

**Key principle:** The main context orchestrates this loop. It does not write deliverables. The creator agent writes; the adversary background agent critiques; the main context routes feedback and tracks iteration count.

---

### Workflow Diagram (ASCII)

```
WORKFLOW: use-case-skills-20260308-001
PATTERN: Sequential with Internal Fan-Out (Phase 1) + Strict Sequential (Phase 3)
CRITICALITY: C3 (governance)  |  QUALITY REVIEWS: C4 (all 10 strategies)
QUALITY THRESHOLD: >= 0.95  |  MAX ITERATIONS PER LOOP: 6

NOTATION: [ADV-C4] = background /adversary C4 review loop (all 10 strategies)
          ╔═══╗    = phase-boundary quality gate (also uses C4 strategy set)

═══════════════════════════════════════════════════════════════════════════════
PHASE 1: RESEARCH (Fan-Out / Fan-In)
═══════════════════════════════════════════════════════════════════════════════

                        ┌──────────────────────┐
                        │   PHASE 1 DISPATCH   │
                        │   (Main Context)     │
                        └──────────┬───────────┘
                                   │
          ┌────────────┬───────────┼───────────┬────────────┐
          ▼            ▼           ▼           ▼            ▼
   ┌────────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────┐
   │ Step 1     │ │ Step 2   │ │ Step 3   │ │ Step 4   │ │ Step 5       │
   │ Jacobson   │ │ Cockburn │ │ Industry │ │ Anthropic│ │ Jerry        │
   │ research   │ │ research │ │ sources  │ │ best     │ │ skill        │
   │            │ │          │ │          │ │ practices│ │ patterns     │
   │ps-researcher│ps-researcher│ps-researcher│ps-researcher│ps-analyst  │
   └──────┬─────┘ └─────┬────┘ └─────┬────┘ └─────┬────┘ └──────┬──────┘
          │             │            │             │              │
          ▼             ▼            ▼             ▼              ▼
     [ADV-C4]      [ADV-C4]     [ADV-C4]      [ADV-C4]      [ADV-C4]
          │             │            │             │              │
          └─────────────┴────────────┴─────────────┴──────────────┘
                                     │
                                     ▼ (all 5 steps PASS)
                        ┌──────────────────────┐
                        │ Research Synthesis   │
                        │ ps-synthesizer       │
                        └──────────┬───────────┘
                                   │
                                   ▼
                              [ADV-C4]
                                   │
                    ╔══════════════╧══════════════╗
                    ║        GATE-1               ║
                    ║  Research Quality Gate      ║
                    ║  C4: All 10 strategies      ║
                    ║  Threshold: >= 0.95         ║
                    ║  Max iterations: 6          ║
                    ╚══════════════╤══════════════╝
                                   │  PASS
═══════════════════════════════════╪═══════════════════════════════════════════
PHASE 2: ARCHITECTURE DESIGN (Partially Parallel)
═══════════════════════════════════╪═══════════════════════════════════════════
                                   │
                    ┌──────────────┴──────────────┐
                    │                             │
                    ▼                             ▼
         ┌─────────────────┐           ┌──────────────────┐
         │ Step 6          │           │ Step 8 (draft)   │
         │ File org design │           │ Agent decomp     │
         │ ps-architect    │           │ ps-architect     │
         └────────┬────────┘           └────────┬─────────┘
                  │                             │
                  ▼                             ▼
             [ADV-C4]                      [ADV-C4]
                  │                             │
                  └───────────┬────────────────-┘
                              │  (sync: both must PASS)
                              ▼
                   ┌──────────────────────┐
                   │ Step 7               │
                   │ Frontmatter schema   │
                   │ design (informs      │
                   │ both 6 + 8 output)   │
                   │ ps-architect         │
                   └──────────┬───────────┘
                              │
                              ▼
                         [ADV-C4]
                              │
                   ╔══════════╧═══════════╗
                   ║       GATE-2         ║
                   ║ Architecture Quality ║
                   ║ C4: All 10 strategies║
                   ║ Threshold: >= 0.95   ║
                   ║ Max iterations: 6    ║
                   ╚══════════╤═══════════╝
                              │  PASS
═══════════════════════════════╪═══════════════════════════════════════════════
PHASE 3: SKILL IMPLEMENTATION (Strictly Sequential)
═══════════════════════════════╪═══════════════════════════════════════════════
                              │
                              ▼
               ┌──────────────────────────────────┐
               │ Step 9: /use-case skill           │
               │ eng-architect (design)            │
               │ eng-lead (standards enforcement)  │
               │ eng-backend (implementation)      │
               │ eng-qa (test strategy)            │
               │ eng-security (security review)    │
               │ eng-reviewer (final review gate)  │
               └──────────────┬───────────────────┘
                              │
                              ▼
                   Sub-deliverables each get [ADV-C4]
                   before feeding to next sub-step:
                   ┌───────────────────────────────┐
                   │ eng-architect output → [ADV-C4]│
                   │ eng-lead output    → [ADV-C4] │
                   │ eng-backend output → [ADV-C4] │
                   │ eng-qa output      → [ADV-C4] │
                   │ eng-security output→ [ADV-C4] │
                   │ eng-reviewer output→ [ADV-C4] │
                   └───────────────┬───────────────┘
                                   │
                  ╔════════════════╧════════════════╗
                  ║           GATE-3                ║
                  ║  /use-case Skill Quality Gate   ║
                  ║  C4: All 10 strategies          ║
                  ║  Verifies: artifact format,     ║
                  ║  frontmatter schema,            ║
                  ║  sample UC, H-34 compliance     ║
                  ║  Threshold: >= 0.95             ║
                  ║  Max iterations: 6              ║
                  ╚════════════════╤════════════════╝
                                   │  PASS
                                   ▼
               ┌──────────────────────────────────┐
               │ Step 10: /test-spec skill         │
               │ eng-architect / eng-lead /        │
               │ eng-backend / eng-qa /            │
               │ eng-security / eng-reviewer       │
               └──────────────┬───────────────────┘
                              │
                              ▼
                   Sub-deliverables each get [ADV-C4]
                                   │
                  ╔════════════════╧════════════════╗
                  ║           GATE-4                ║
                  ║  /test-spec Skill Quality Gate  ║
                  ║  C4: All 10 strategies          ║
                  ║  Verifies: consumes /use-case   ║
                  ║  artifact, bidirectional trace  ║
                  ║  Threshold: >= 0.95             ║
                  ║  Max iterations: 6              ║
                  ╚════════════════╤════════════════╝
                                   │  PASS
                                   ▼
               ┌──────────────────────────────────┐
               │ Step 11: /contract-design skill   │
               │ eng-architect / eng-lead /        │
               │ eng-backend / eng-qa /            │
               │ eng-security / eng-reviewer       │
               └──────────────┬───────────────────┘
                              │
                              ▼
                   Sub-deliverables each get [ADV-C4]
                                   │
                  ╔════════════════╧════════════════╗
                  ║           GATE-5                ║
                  ║  /contract-design Skill Gate    ║
                  ║  C4: All 10 strategies          ║
                  ║  Verifies: contract traces to   ║
                  ║  UC interactions                ║
                  ║  Threshold: >= 0.95             ║
                  ║  Max iterations: 6              ║
                  ╚════════════════╤════════════════╝
                                   │  PASS
═══════════════════════════════════╪═══════════════════════════════════════════
PHASE 3b: RED-TEAM REVIEW (Security review of implemented skills)
═══════════════════════════════════╪═══════════════════════════════════════════
                                   │
                                   ▼
               ┌──────────────────────────────────┐
               │ Step 11b: Red-Team Review         │
               │ red-lead (scope + rules of        │
               │   engagement)                     │
               │ red-vuln (vulnerability analysis  │
               │   of agent defs + skill bounds    │
               │   + trigger map)                  │
               │ red-reporter (findings report)    │
               └──────────────┬───────────────────┘
                              │
                              ▼
                         [ADV-C4] (red-team report reviewed)
                              │
                  ╔═══════════╧════════════════════╗
                  ║         GATE-5b               ║
                  ║  Red-Team Security Gate       ║
                  ║  C4: All 10 strategies        ║
                  ║  Verifies: no P-003 bypass    ║
                  ║  vectors, no abuse vectors    ║
                  ║  in skill boundaries, no      ║
                  ║  trigger-map manipulation     ║
                  ║  Threshold: >= 0.95           ║
                  ║  Max iterations: 6            ║
                  ╚═══════════╤════════════════════╝
                              │  PASS
═══════════════════════════════╪═══════════════════════════════════════════════
PHASE 4: INTEGRATION AND VERIFICATION
═══════════════════════════════╪═══════════════════════════════════════════════
                             │
                             ▼
               ┌──────────────────────────┐
               │ Step 12: Integration     │
               │ Main context             │
               │ /worktracker link,       │
               │ trigger map registration,│
               │ CLAUDE.md, AGENTS.md     │
               └─────────────┬────────────┘
                             │
                             ▼
               ┌──────────────────────────┐
               │ Step 13: E2E Verification│
               │ ps-validator             │
               │ Sample UC → slice →      │
               │ test specs → contracts   │
               └─────────────┬────────────┘
                             │
                             ▼
                        [ADV-C4]
                             │
                  ╔══════════╧═══════════╗
                  ║      GATE-6          ║
                  ║ Final Quality Gate   ║
                  ║ C4: All 10 strategies║
                  ║ End-to-end pass      ║
                  ║ Threshold: >= 0.95   ║
                  ║ Max iterations: 6    ║
                  ╚══════════╤═══════════╝
                             │  PASS
                             ▼
                    ┌─────────────────┐
                    │  WORKFLOW DONE  │
                    │  3 skills live  │
                    │  All registered │
                    └─────────────────┘
```

---

### Phase Definitions

#### Phase 1: Research

**Pattern:** Fan-Out / Fan-In (Pattern 3)
**Goal:** Produce a comprehensive research foundation covering methodology, tooling, best practices, and existing Jerry patterns.
**Prerequisite:** None (entry phase)
**Exit criterion:** Research synthesis scores >= 0.95 at GATE-1
**Adversary coverage:** Every step output gets individual C4 adversary review before synthesis

| Step | Skill | Agent | Deliverable | Adversary Review | Notes |
|------|-------|-------|-------------|-----------------|-------|
| 1 | /problem-solving | ps-researcher | `research/jacobson-use-case-2.md` | [ADV-C4] before synthesis | Jacobson Use Case 2.0: seven activities, slice types (basic, precondition, alternative, error, enhancement), slice lifecycle states. Chapter-level citations required (C-023). |
| 2 | /problem-solving | ps-researcher | `research/cockburn-writing-effective-use-cases.md` | [ADV-C4] before synthesis | Cockburn's use case templates (casual/fully-dressed), goal levels (sea/fish/clam), precision levels, completeness heuristics. Chapter-level citations required. |
| 3 | /problem-solving | ps-researcher | `research/industry-sources.md` | [ADV-C4] before synthesis | 3+ additional industry sources: modern requirements tooling, use-case-driven development, UCDD methodologies. Web search required (C-024). |
| 4 | /problem-solving | ps-researcher | `research/anthropic-skill-best-practices.md` | [ADV-C4] before synthesis | Anthropic skill authoring best practices: progressive disclosure, token budgets, evaluation-driven development. Reference existing Jerry agent-development-standards.md. |
| 5 | /problem-solving | ps-analyst | `research/jerry-skill-pattern-analysis.md` | [ADV-C4] before synthesis | Analyze existing Jerry skills (/pm-pmm, /eng-team, /user-experience) for agent decomposition patterns, file organization, integration patterns (convergent mode). |
| 1-5 | /problem-solving | ps-synthesizer | `research/phase-1-synthesis.md` | [ADV-C4] → then GATE-1 | Cross-pollinate all five research streams. Identify conflicts, gaps, and design implications for Phase 2. |

**Fan-out execution:** Steps 1-4 run in parallel (independent research topics). Step 5 runs concurrently with 1-4 (independent codebase analysis). Each step output undergoes its own C4 adversary loop before synthesis. Synthesis runs after all five PASS.

**Agent count:** 3 distinct creator agents across 6 invocations; plus individual /adversary background agents per output.

---

#### Phase 2: Architecture Design

**Pattern:** Partial parallel then sequential convergence
**Goal:** Define the complete architecture for all three skills before any implementation begins.
**Prerequisite:** GATE-1 passed; Phase 1 synthesis available.
**Exit criterion:** Architecture design scores >= 0.95 at GATE-2
**Adversary coverage:** Each architecture sub-deliverable gets C4 adversary review before the next step may consume it

| Step | Skill | Agent | Deliverable | Adversary Review | Notes |
|------|-------|-------|-------------|-----------------|-------|
| 6 | /problem-solving | ps-architect | `architecture/file-organization.md` | [ADV-C4] → sync point | File organization for use case artifacts: one file per artifact, navigable, traversable, decomposed. /worktracker compatible (use cases → Features/Stories, slices → Tasks). Directory structure, naming conventions. |
| 7 | /problem-solving | ps-architect | `architecture/frontmatter-schema.md` + `architecture/shared-schema.json` | [ADV-C4] → step 8-final | Shared frontmatter schema (data contract between all 3 skills). JSON Schema validatable via `jerry ast validate`. Cross-reference fields for bidirectional linking. |
| 8 | /problem-solving | ps-architect | `architecture/agent-decomposition.md` | [ADV-C4] → GATE-2 | Agent decomposition for all 3 skills: which agents handle which concerns, tool tiers, orchestrator-worker topology, T2/T3/T4 classification, cognitive modes. |

**Execution order:** Steps 6 and 8-draft can begin in parallel after GATE-1. Each gets its own C4 adversary review. Step 7 requires both 6 and 8-draft PASS. Step 8-final follows step 7's PASS.

**Agent count:** 1 distinct creator agent, 3 invocations; plus individual /adversary background agents per output.

---

#### Phase 3: Skill Implementation

**Pattern:** Strictly sequential (each skill output is input to the next)
**Goal:** Implement all three skills with complete agent definitions, templates, and guided workflows.
**Prerequisite:** GATE-2 passed; all Phase 2 architecture documents available.
**Exit criterion:** Each skill gate (GATE-3, GATE-4, GATE-5) passes at >= 0.95 before proceeding.
**Adversary coverage:** Every sub-deliverable from every /eng-team agent gets its own C4 adversary review

| Step | Skill | Agents | Deliverable | Gate |
|------|-------|--------|-------------|------|
| 9 | /eng-team | eng-architect, eng-lead, eng-backend, eng-qa, eng-security, eng-reviewer | `/use-case` skill complete | GATE-3 |
| 10 | /eng-team | eng-architect, eng-lead, eng-backend, eng-qa, eng-security, eng-reviewer | `/test-spec` skill complete | GATE-4 |
| 11 | /eng-team | eng-architect, eng-lead, eng-backend, eng-qa, eng-security, eng-reviewer | `/contract-design` skill complete | GATE-5 |

**Agent role assignments per step:**

| Agent | Role |
|-------|------|
| eng-architect | Design skill architecture: internal structure, agent boundaries, data flow diagram |
| eng-lead | Standards enforcement: H-25, H-26, H-34, naming conventions, dependency governance |
| eng-backend | Implement agent definitions (.md + .governance.yaml), SKILL.md, templates |
| eng-qa | Design test strategy: how to verify guided workflow, template output, slicing correctness |
| eng-security | Security review of agent definitions: tool tier verification, forbidden actions, constitutional triplet |
| eng-reviewer | Final review gate: verifies all prior outputs before phase-level gate submission |

**Each agent output within a step undergoes its own C4 adversary review before being consumed by the next agent in the sequence.**

**Step 9 deliverables (/use-case):**
- `skills/use-case/SKILL.md` (H-25, H-26 compliant)
- `skills/use-case/agents/use-case-author.md` + `use-case-author.governance.yaml`
- `skills/use-case/agents/use-case-slicer.md` + `use-case-slicer.governance.yaml`
- `skills/use-case/agents/use-case-reviewer.md` + `use-case-reviewer.governance.yaml`
- `skills/use-case/agents/use-case-index.md` + `use-case-index.governance.yaml`
- `skills/use-case/templates/casual-template.md`
- `skills/use-case/templates/fully-dressed-template.md`
- `skills/use-case/templates/slice-template.md`
- `skills/use-case/templates/actor-goal-matrix-template.md`
- Sample use case artifact (demonstrates guided 5+ exchange workflow)

**Step 10 deliverables (/test-spec):**
- `skills/test-spec/SKILL.md`
- `skills/test-spec/agents/test-plan-generator.md` + `.governance.yaml`
- `skills/test-spec/agents/test-coverage-analyst.md` + `.governance.yaml`
- `skills/test-spec/templates/bdd-scenario-template.md`
- `skills/test-spec/templates/tdd-test-plan-template.md`

**Step 11 deliverables (/contract-design):**
- `skills/contract-design/SKILL.md`
- `skills/contract-design/agents/contract-generator.md` + `.governance.yaml`
- `skills/contract-design/agents/contract-validator.md` + `.governance.yaml`
- `skills/contract-design/templates/openapi-template.yaml`
- `skills/contract-design/templates/cloudevents-template.yaml`
- `skills/contract-design/templates/asyncapi-template.yaml`
- `skills/contract-design/templates/json-schema-template.json`

**Agent count:** 6 distinct agents per step, 18 invocations total across Phase 3; plus individual /adversary background agents per sub-deliverable.

---

#### Phase 3b: Red-Team Review

**Pattern:** Sequential
**Goal:** Security review of all three implemented skills before framework integration.
**Prerequisite:** GATE-5 passed; all three skills complete.
**Exit criterion:** GATE-5b passes at >= 0.95
**Adversary coverage:** Red-team report itself gets C4 adversary review

| Step | Skill | Agent | Deliverable | Notes |
|------|-------|-------|-------------|-------|
| 11b-scope | /red-team | red-lead | `security/red-team-scope.md` | Define scope and rules of engagement for reviewing all three skills |
| 11b-vuln | /red-team | red-vuln | `security/red-team-vulnerabilities.md` | Vulnerability analysis covering: (1) agent definitions for P-003 bypass vectors — can any agent be tricked into spawning recursive subagents? (2) skill boundaries for abuse vectors — can /use-case be misused to generate harmful content? (3) trigger map for routing manipulation — can adversarial input cause misrouting to wrong skill? |
| 11b-report | /red-team | red-reporter | `security/red-team-report.md` | Consolidated findings report with severity classification and remediation recommendations |

**Each red-team sub-deliverable gets its own C4 adversary review. The final report also gets C4 adversary review before GATE-5b.**

---

#### Phase 4: Integration and Verification

**Pattern:** Sequential
**Goal:** Integrate all three skills with Jerry framework, verify end-to-end pipeline, pass final quality gate.
**Prerequisite:** GATE-5b passed; red-team review complete.
**Exit criterion:** GATE-6 passes at >= 0.95

| Step | Skill | Agent | Deliverable | Notes |
|------|-------|-------|-------------|-------|
| 12 | Direct (main context) | — | Registration complete | Update `mandatory-skill-usage.md` trigger map (5-column format, AE-002 auto-C3 applies). Update `CLAUDE.md` skills table. Update `AGENTS.md`. Update `projects/README.md`. Create /worktracker integration documentation. |
| 13 | /problem-solving | ps-validator | `verification/e2e-verification-report.md` | End-to-end verification: run sample use case through all three skills, verify all cross-references, verify bidirectional traceability, verify frontmatter schema consistency. |
| 14 | /adversary | adv-scorer | `verification/final-quality-gate.md` | Quality gate all deliverables per quality-enforcement.md. Score >= 0.95 required. All 10 C4 strategies applied. |

**Step 13 (ps-validator) output gets C4 adversary review before GATE-6.**

**Agent count:** 2 distinct creator agents, 2 invocations (step 12 is main context, not a subagent); plus /adversary background agent for step 13 output.

---

### Sync Barriers

| Barrier | ID | Trigger | Strategy Set | Threshold | Max Iter |
|---------|----|---------|-------------|-----------|----------|
| After Phase 1 synthesis | GATE-1 | All research steps PASS C4 adversary + ps-synthesizer deliverable PASS C4 adversary | C4: All 10 (S-014, S-003, S-013, S-007, S-002, S-004, S-010, S-012, S-011, S-001) | >= 0.95 | 6 |
| After Phase 2 design | GATE-2 | Steps 6, 7, 8 all PASS C4 adversary + schema validated by `jerry ast validate` | C4: All 10 | >= 0.95 | 6 |
| After /use-case skill | GATE-3 | Step 9 all sub-deliverables PASS C4 adversary + sample use case passes `jerry ast validate` | C4: All 10 | >= 0.95 | 6 |
| After /test-spec skill | GATE-4 | Step 10 all sub-deliverables PASS C4 adversary + test spec consumes /use-case artifact with traceability | C4: All 10 | >= 0.95 | 6 |
| After /contract-design skill | GATE-5 | Step 11 all sub-deliverables PASS C4 adversary + contract traces to use case interactions | C4: All 10 | >= 0.95 | 6 |
| After red-team review | GATE-5b | Red-team report PASS C4 adversary + all findings dispositioned (accepted or remediated) | C4: All 10 | >= 0.95 | 6 |
| After full integration | GATE-6 | Steps 12-13 complete + E2E verification report PASS C4 adversary | C4: All 10 | >= 0.95 | 6 |

**Quality Gate Rule:** Any deliverable below threshold at any adversary loop triggers revision. At iteration ceiling (6), escalate to user with current best result and critic findings (RT-M-010, C-009).

---

### Execution Queue

Execution groups define what can run in parallel versus what must wait. Groups marked [ADV-C4] are the background adversary review groups that follow each creator group.

| Group | Phase | Steps | Parallel? | Depends On |
|-------|-------|-------|-----------|------------|
| G-01 | 1 | Steps 1, 2, 3, 4, 5 (creator) | YES — fan-out | None |
| G-01-ADV | 1 | [ADV-C4] for each step 1-5 output | YES — parallel per output | G-01 (individual) |
| G-02 | 1 | Research synthesis (ps-synthesizer) | NO — fan-in | G-01-ADV all PASS |
| G-02-ADV | 1 | [ADV-C4] for synthesis output | NO | G-02 complete |
| G-03 | 1 | GATE-1 | NO | G-02-ADV PASS |
| G-04 | 2 | Steps 6, 8-draft (creator) | YES — partial parallel | G-03 PASS |
| G-04-ADV | 2 | [ADV-C4] for each of steps 6, 8-draft | YES — parallel per output | G-04 (individual) |
| G-05 | 2 | Step 7 (creator) | NO — waits for 6 + 8-draft PASS | G-04-ADV both PASS |
| G-05-ADV | 2 | [ADV-C4] for step 7 output | NO | G-05 complete |
| G-06 | 2 | Step 8-final (creator) | NO | G-05-ADV PASS |
| G-06-ADV | 2 | [ADV-C4] for step 8-final output | NO | G-06 complete |
| G-07 | 2 | GATE-2 | NO | G-06-ADV PASS |
| G-08 | 3 | Step 9 sub-steps (creator pipeline: eng-architect → eng-lead → eng-backend → eng-qa → eng-security → eng-reviewer) | NO — sequential within step | G-07 PASS |
| G-08-ADV | 3 | [ADV-C4] after each eng-team sub-step output | NO — follows each sub-step | G-08 (each sub-step) |
| G-09 | 3 | GATE-3 | NO | G-08-ADV all PASS |
| G-10 | 3 | Step 10 sub-steps (same /eng-team pipeline) | NO | G-09 PASS |
| G-10-ADV | 3 | [ADV-C4] after each eng-team sub-step output | NO | G-10 (each sub-step) |
| G-11 | 3 | GATE-4 | NO | G-10-ADV all PASS |
| G-12 | 3 | Step 11 sub-steps (same /eng-team pipeline) | NO | G-11 PASS |
| G-12-ADV | 3 | [ADV-C4] after each eng-team sub-step output | NO | G-12 (each sub-step) |
| G-13 | 3 | GATE-5 | NO | G-12-ADV all PASS |
| G-13b-scope | 3b | Step 11b-scope (red-lead) | NO | G-13 PASS |
| G-13b-scope-ADV | 3b | [ADV-C4] for scope output | NO | G-13b-scope complete |
| G-13b-vuln | 3b | Step 11b-vuln (red-vuln) | NO | G-13b-scope-ADV PASS |
| G-13b-vuln-ADV | 3b | [ADV-C4] for vulnerability analysis | NO | G-13b-vuln complete |
| G-13b-report | 3b | Step 11b-report (red-reporter) | NO | G-13b-vuln-ADV PASS |
| G-13b-report-ADV | 3b | [ADV-C4] for red-team report | NO | G-13b-report complete |
| G-13b-gate | 3b | GATE-5b | NO | G-13b-report-ADV PASS |
| G-14 | 4 | Step 12 (integration, main context) | NO | G-13b-gate PASS |
| G-15 | 4 | Step 13 (E2E verification, ps-validator) | NO | G-14 complete |
| G-15-ADV | 4 | [ADV-C4] for E2E verification report | NO | G-15 complete |
| G-16 | 4 | GATE-6 + Step 14 (final scoring) | NO | G-15-ADV PASS |

---

### Dependencies Between Steps

```
Steps 1,2,3,4,5  ──[ADV-C4 each]──►  Research Synthesis  ──[ADV-C4]──►  GATE-1
                                                                              │
                          ┌───────────────────────────────────────────────────┘
                          │
                 Steps 6, 8-draft  ──[ADV-C4 each]──►
                     Step 7  ──[ADV-C4]──►
                       Step 8-final  ──[ADV-C4]──►  GATE-2
                                                        │
                          ┌─────────────────────────────┘
                          │
                    Step 9 (eng-architect→lead→backend→qa→security→reviewer,
                            each sub-step ──[ADV-C4]──►)  GATE-3
                          │
                    Step 10 (same pipeline) ──[ADV-C4 each]──►  GATE-4
                          │
                    Step 11 (same pipeline) ──[ADV-C4 each]──►  GATE-5
                          │
                    Step 11b (red-lead → red-vuln → red-reporter,
                              each ──[ADV-C4]──►)  GATE-5b
                          │
                    Step 12  ──►  Step 13  ──[ADV-C4]──►  GATE-6  ──►  DONE
```

**Critical path:** Steps 9 → GATE-3 → 10 → GATE-4 → 11 → GATE-5 → 11b → GATE-5b is the binding constraint. No parallelism permitted here.

---

### Success Criteria Per Phase

#### Phase 1 Success Criteria

- [ ] Jacobson Use Case 2.0 research: covers all seven activities, all five slice types, slice lifecycle states; chapter-level citations present; C4 adversary PASS
- [ ] Cockburn research: covers casual and fully-dressed templates, all three goal levels, precision levels, completeness heuristics; chapter-level citations present; C4 adversary PASS
- [ ] 3+ additional industry sources with web-search-sourced citations (C-024); C4 adversary PASS
- [ ] Anthropic skill authoring best practices documented with references to agent-development-standards.md; C4 adversary PASS
- [ ] Jerry skill pattern analysis covers at minimum /pm-pmm, /eng-team, /user-experience; C4 adversary PASS
- [ ] Synthesis identifies design implications for all three skills; C4 adversary PASS
- [ ] GATE-1 score >= 0.95

#### Phase 2 Success Criteria

- [ ] File organization design supports: one file per artifact, casual (50-100 lines), fully-dressed (200-250 lines max); C4 adversary PASS
- [ ] File organization is /worktracker compatible (use cases map to Features/Stories, slices map to Tasks)
- [ ] Dependency graph specification (Mermaid, dynamically generated from frontmatter)
- [ ] Auto-generated index specification (filterable by actor, goal level, status, domain)
- [ ] Frontmatter schema is valid JSON Schema, validated by `jerry ast validate`; C4 adversary PASS
- [ ] Frontmatter schema covers cross-reference fields for bidirectional linking between all three skills
- [ ] Agent decomposition covers all 9 agents across 3 skills, with tool tiers (T1-T5), cognitive modes, and constitutional triplet specified; C4 adversary PASS
- [ ] GATE-2 score >= 0.95

#### Phase 3 Success Criteria (/use-case — GATE-3)

- [ ] SKILL.md compliant with H-25, H-26 (WHAT+WHEN+triggers, repo-relative paths, < 1024 chars description)
- [ ] All 4 agent definitions: .md + .governance.yaml validated against agent-governance-v1.schema.json
- [ ] Constitutional triplet (P-003, P-020, P-022) in all agent .governance.yaml files (H-34)
- [ ] Guided experience: minimum 5 exchanges per interactive workflow specification
- [ ] Casual and fully-dressed templates present
- [ ] Slicing template present (covers basic, precondition, alternative, error, enhancement patterns)
- [ ] Actor-goal matrix template present
- [ ] Sample use case artifact passes `jerry ast validate`
- [ ] Each /eng-team sub-deliverable passed C4 adversary
- [ ] GATE-3 score >= 0.95

#### Phase 3 Success Criteria (/test-spec — GATE-4)

- [ ] SKILL.md compliant with H-25, H-26
- [ ] All 2 agent definitions: .md + .governance.yaml validated
- [ ] /test-spec consumes /use-case artifact (reads frontmatter cross-references)
- [ ] Given/When/Then format implemented in BDD scenarios
- [ ] Bidirectional traceability: test spec references use case step IDs; use case lists derived test IDs
- [ ] Each /eng-team sub-deliverable passed C4 adversary
- [ ] GATE-4 score >= 0.95

#### Phase 3 Success Criteria (/contract-design — GATE-5)

- [ ] SKILL.md compliant with H-25, H-26
- [ ] All 2 agent definitions: .md + .governance.yaml validated
- [ ] Contracts (OpenAPI, CloudEvents, AsyncAPI, JSON Schema) generated from use case interactions
- [ ] Contract artifacts trace to specific use case interaction steps via frontmatter fields
- [ ] Each /eng-team sub-deliverable passed C4 adversary
- [ ] GATE-5 score >= 0.95

#### Phase 3b Success Criteria (Red-Team — GATE-5b)

- [ ] Red-team scope document defines attack surface for all three skills
- [ ] Vulnerability analysis addresses P-003 bypass vectors (agent definition manipulation)
- [ ] Vulnerability analysis addresses content abuse vectors (/use-case skill misuse)
- [ ] Vulnerability analysis addresses trigger-map routing manipulation
- [ ] All identified vulnerabilities have severity classification and remediation recommendation
- [ ] All critical/high findings remediated or accepted with documented rationale
- [ ] Red-team report passed C4 adversary
- [ ] GATE-5b score >= 0.95

#### Phase 4 Success Criteria

- [ ] `mandatory-skill-usage.md` trigger map updated with 5-column format entries for all three skills
- [ ] `CLAUDE.md` skills table updated with all three skills
- [ ] `AGENTS.md` updated with all 9 new agents
- [ ] /worktracker integration: use cases create Features/Stories, slices create Tasks
- [ ] E2E verification: sample use case traverses full pipeline (→ slice → test specs → contracts) with all cross-references verified
- [ ] All cross-references are bidirectional (no orphaned links)
- [ ] E2E verification report passed C4 adversary
- [ ] GATE-6 score >= 0.95

---

### Agent Summary

| Phase | Creator Agents Invoked | Invocations | /adversary Loops |
|-------|----------------------|-------------|-----------------|
| Phase 1 | ps-researcher, ps-analyst, ps-synthesizer | 6 creator | 6 adversary loops (1 per output) |
| Phase 2 | ps-architect | 4 creator invocations (6, 8-draft, 7, 8-final) | 4 adversary loops |
| Phase 3 | eng-architect, eng-lead, eng-backend, eng-qa, eng-security, eng-reviewer | 18 creator (6 agents × 3 steps) | ~18 adversary loops (1 per sub-deliverable) |
| Phase 3b | red-lead, red-vuln, red-reporter | 3 creator | 3 adversary loops |
| Phase 4 | ps-validator, adv-scorer | 2 creator | 1 adversary loop (step 13 output) |
| Gates | adv-executor, adv-scorer | 7 gates | — |
| **Total** | **14 distinct agents** | **~33 creator invocations** | **~32 adversary background loops** |

---

## L2: Implementation Details

### Dynamic Path Configuration

All artifact paths use the dynamic workflow identifier. No hardcoded pipeline names.

| Path Type | Pattern | Example |
|-----------|---------|---------|
| Base | `projects/PROJ-021-use-case/orchestration/use-case-skills-20260308-001/` | — |
| Research | `{base}research/{slug}.md` | `{base}research/jacobson-use-case-2.md` |
| Architecture | `{base}architecture/{slug}.md` | `{base}architecture/file-organization.md` |
| Security | `{base}security/{slug}.md` | `{base}security/red-team-report.md` |
| Verification | `{base}verification/{slug}.md` | `{base}verification/e2e-verification-report.md` |
| Skill artifacts | `skills/{skill-name}/` | `skills/use-case/SKILL.md` |
| Agent definitions | `skills/{skill-name}/agents/{agent-name}.md` | `skills/use-case/agents/use-case-author.md` |
| Templates | `skills/{skill-name}/templates/{template-name}.md` | `skills/use-case/templates/casual-template.md` |

### Checkpoint Locations

Checkpoints enable session resume at any phase boundary. The orchestration state in `ORCHESTRATION.yaml` is the authoritative resume point.

| Checkpoint | ID | Location | State Captured |
|------------|----|----------|----------------|
| After GATE-1 | CP-001 | After Phase 1 complete | Research artifacts, GATE-1 score, synthesis findings |
| After GATE-2 | CP-002 | After Phase 2 complete | Architecture artifacts, GATE-2 score, schema validated |
| After GATE-3 | CP-003 | After /use-case complete | /use-case skill artifacts, GATE-3 score |
| After GATE-4 | CP-004 | After /test-spec complete | /test-spec skill artifacts, GATE-4 score |
| After GATE-5 | CP-005 | After /contract-design complete | /contract-design skill artifacts, GATE-5 score |
| After GATE-5b | CP-005b | After red-team complete | Red-team report, GATE-5b score, remediations |
| After GATE-6 | CP-006 | Workflow complete | All artifacts, GATE-6 score, registration verified |

**Resume protocol:** Read `ORCHESTRATION.yaml` → find last checkpoint with `status: passed` → resume at the next execution group.

### Quality Gate Definitions

Every creator output and every phase gate uses the full C4 adversarial strategy set per `quality-enforcement.md`.

**C4 Required Strategies (all 10 applied at every review):**
- S-014 LLM-as-Judge: Apply strict scoring rubric with 6 weighted dimensions
- S-003 Steelman: Strengthen the deliverable's best arguments before critique
- S-013 Inversion: Invert the goal to find what could cause failure
- S-007 Constitutional AI Critique: Verify governance and constitutional compliance
- S-002 Devil's Advocate: Challenge core assumptions
- S-004 Pre-Mortem: Identify ways the deliverable could fail in production
- S-010 Self-Refine: Systematic self-improvement pass before external critique
- S-012 FMEA: Systematic failure mode and effects analysis
- S-011 Chain-of-Verification: Verify claims through independent reasoning chains
- S-001 Red Team Analysis: Adversarial assessment for vulnerabilities and attack vectors

**Scoring Dimensions (S-014):**

| Dimension | Weight | Notes |
|-----------|--------|-------|
| Completeness | 0.20 | All required deliverables present |
| Internal Consistency | 0.20 | No contradictions across artifacts |
| Methodological Rigor | 0.20 | Methodology correctly applied (Jacobson, Cockburn) |
| Evidence Quality | 0.15 | Citations present (C-023), web search conducted (C-024) |
| Actionability | 0.15 | Deliverables usable by downstream skill/agent |
| Traceability | 0.10 | Cross-references complete and bidirectional |

### Main Context Orchestration Protocol

The main context NEVER produces deliverables. Its sole responsibilities are:

1. Launch creator agent with task specification
2. Receive creator output (file path reference, not inline content per CP-01)
3. Launch background /adversary agent with: (a) creator output path, (b) C4 strategy set, (c) threshold 0.95, (d) max iterations 6
4. Receive adversary score and findings
5. If score < 0.95 and iterations < 6: route findings back to creator → go to step 1
6. If score >= 0.95: mark output PASSED, proceed to next step
7. If iterations = 6 and score < 0.95: escalate to user per RT-M-010 and C-009
8. Update orch-tracker (ORCHESTRATION.yaml status fields)

### Recovery Strategies

| Failure Mode | Recovery Action | Escalation |
|-------------|----------------|------------|
| Research agent fails to find sources | Retry with alternative search terms (C-024); if 3 attempts fail, escalate to user (H-31) | User provides alternative sources |
| Adversary score < 0.95, iteration < 6 | Apply critic findings, revise specific low-scoring dimensions, re-submit to adversary | — |
| Adversary score < 0.95, iteration = 6 | Present best result to user with critic findings, ask for guidance (C-009) | User decides: accept, modify threshold, or provide additional context |
| Schema validation fails (`jerry ast validate`) | Fix frontmatter fields identified by validation output; re-validate; adversary re-reviews | — |
| /use-case artifact format incompatible with /test-spec | Pause Phase 3; return to Phase 2 to revise frontmatter schema; apply GATE-2 again | Add Phase 2b iteration to ORCHESTRATION.yaml |
| Red-team finds critical P-003 bypass vector | Halt Phase 4; return to affected Phase 3 step for remediation; re-run GATE-5 and GATE-5b | — |
| mandatory-skill-usage.md update blocked (AE-002 auto-C3) | This plan already accounts for C3 criticality. No escalation needed. | — |
| MCP server unavailable | Persist context to `work/.mcp-fallback/{key}.md` per mcp-tool-standards.md | Log in worktracker entry |
| Context fill CRITICAL (>= 0.80, AE-006c) | Auto-checkpoint current state, reduce verbosity of subsequent agent outputs | — |
| Context fill EMERGENCY (>= 0.88, AE-006d) | Mandatory checkpoint, warn user, prepare handoff for next session | — |
| High token consumption from C4 adversary loops | Expected and accounted for. If context CRITICAL triggers, checkpoint and resume. | — |

---

## Operating Constraints

The following NPT-013 constraints (C-001 through C-030) govern this workflow. The authoritative source is `projects/PROJ-021-use-case/work/prompt-engineering/npt-constraints.md` (generated in parallel — reference that file for full constraint text).

| ID | Constraint | Impact on Plan |
|----|-----------|----------------|
| C-001 | NEVER begin orchestration without plan | This document satisfies C-001 |
| C-002 | NEVER proceed without verifying project context | Active project: PROJ-021-use-case verified |
| C-003 | NEVER skip research when building new capabilities | Phase 1 (5 research steps) is mandatory before implementation |
| C-004 | NEVER implement without architecture design | Phase 2 is mandatory before Phase 3 |
| C-005 | NEVER execute all work in main context | Main context orchestrates only; all creator work delegated to specialized agents |
| C-006 | NEVER skip /worktracker entity creation | Step 12 and `ORCHESTRATION_WORKTRACKER.md` address this |
| C-007 | NEVER allow creator output to proceed without /adversary C4 review | Every creator output gets individual C4 adversary loop before use by any downstream consumer |
| C-008 | Quality gate >= 0.95 (user override) | All gates set to >= 0.95; adversary loops also use >= 0.95 |
| C-009 | Max 6 iterations per creator-adversary loop | All adversary loops set max_iterations: 6 |
| C-010 | NEVER mix concerns across phases | Phase 1 = research only, Phase 2 = architecture only, Phase 3 = implementation only |
| C-011 | NEVER implement before all architecture artifacts complete | GATE-2 blocks Phase 3 start |
| C-012 | NEVER skip Phase 3 sequential ordering | Strict sequential: Step 9 → GATE-3 → Step 10 → GATE-4 → Step 11 → GATE-5 |
| C-013 | NEVER skip E2E verification | Step 13 is mandatory before GATE-6 |
| C-014 | NEVER register skills without verification | Registration (Step 12) occurs after GATE-5b (red-team cleared), E2E verification (Step 13) follows |
| C-015 | NEVER omit constitutional triplet from agent definitions | H-34 compliance required for all 9 new agents; verified at GATE-3, GATE-4, GATE-5 |
| C-016 | NEVER use hardcoded pipeline names | All paths use `use-case-skills-20260308-001` dynamic identifier |
| C-017 | NEVER omit plan disclaimer | Disclaimer section present |
| C-018 | NEVER generate incomplete ORCHESTRATION.yaml | ORCHESTRATION.yaml has all phase definitions before this file is written |
| C-019 | NEVER omit worktracker entities | ORCHESTRATION_WORKTRACKER.md created alongside this plan |
| C-020 | NEVER generate frontmatter schemas without `jerry ast validate` verification | GATE-2 explicitly requires `jerry ast validate` pass |
| C-021 | NEVER skip trigger map 5-column format | Step 12 uses 5-column format per agent-routing-standards.md RT-M-003 |
| C-022 | NEVER assume — verify from authoritative sources | All research steps require citations (C-023); web search required (C-024) |
| C-023 | Source citations required on all claims | Enforced in research step deliverable specifications |
| C-024 | Web search before technical decisions | Enforced in Steps 1-4 (ps-researcher uses T3 tools) |
| C-025 | Use specialized /skill agents, not generic agents | All steps mapped to specific Jerry skills and named agents |
| C-026 | Persist everything to files | All deliverables have explicit file paths in phase definitions |
| C-027 | Create /worktracker entities before execution | ORCHESTRATION_WORKTRACKER.md created at plan time |
| C-028 | Keep worktracker entities current | orch-tracker updates ORCHESTRATION.yaml after each agent completion |
| C-029 | Documentation accuracy | All file paths and agent names are real Jerry entities |
| C-030 | Completeness before handoff | All required deliverables specified for every step |

---

## Risk Register

| ID | Risk | Likelihood | Impact | Mitigation |
|----|------|-----------|--------|-----------|
| R-01 | Phase 3 sequential dependency: /test-spec cannot consume /use-case output due to schema mismatch | Medium | High | GATE-3 explicitly verifies artifact format. If mismatch at GATE-4, recovery strategy returns to Phase 2 for schema revision. |
| R-02 | Research Phase 1 finds conflicting guidance between Jacobson and Cockburn methodologies | Medium | Medium | ps-synthesizer explicitly tasked with identifying conflicts. ps-architect resolves conflicts in Phase 2 design. |
| R-03 | Context fill during Phase 3 (large skill implementation + C4 adversary loops per sub-step) triggers AE-006c/d | High | Medium | Checkpoints at every GATE (CP-001 through CP-006). Recovery protocol in ORCHESTRATION.yaml. C4 adversary loops are expected to consume significant tokens — checkpoint aggressively. |
| R-04 | mandatory-skill-usage.md update requires C3 review per AE-002 | Certain | Low | Already planned as C3 criticality. No additional escalation needed — plan accounts for it. |
| R-05 | 9 new agent .governance.yaml files fail JSON Schema validation | Medium | High | H-34 compliance checked at each GATE before proceeding to next phase. eng-backend reads agent-governance-v1.schema.json before writing files. |
| R-06 | /adversary adv-scorer applies leniency bias (H-13 warns against this) | Low | High | adv-scorer prompt explicitly includes anti-leniency guardrail per S-014. Quality threshold 0.95 (not 0.85) reduces leniency risk. |
| R-07 | Jerry ast validate not available or produces unexpected errors | Low | High | Step 7 deliverable includes validation step. If CLI unavailable, use manual frontmatter review as fallback and document gap. |
| R-08 | 3+ industry sources in Step 3 unavailable or low-quality | Low | Medium | ps-researcher uses web search (T3 tools). If fewer than 3 high-quality sources found, escalate to user per H-31 before proceeding. |
| R-09 | Bidirectional cross-references break when file paths change | Medium | Medium | All cross-references use relative paths from the shared frontmatter schema. File organization architecture (Step 6) must specify stable path conventions. |
| R-10 | High token consumption from C4 adversary loop at every creator output | High | Medium | Accepted trade-off for quality assurance. Expected token budget is 2-3x a C3 review workflow. Mitigated by checkpoint-at-every-gate protocol and AE-006c/d handling. |
| R-11 | Red-team (Phase 3b) finds critical vulnerability requiring Phase 3 rework | Low | High | Red-team scope defined before engagement. If critical finding requires rework, pause Phase 4, return to affected step, re-run GATE-5 and GATE-5b. |
| R-12 | C4 adversary loop with max 6 iterations still does not converge | Very Low | Medium | At iteration 6, present best result to user with all critic findings. User decides threshold adjustment or additional context provision. Do not silently accept below-threshold work. |

---

## Disclaimer

This orchestration plan was generated by the orch-planner agent (v2.2.0) for project PROJ-021-use-case, workflow use-case-skills-20260308-001. Human review is recommended before execution begins.

This plan references `projects/PROJ-021-use-case/work/prompt-engineering/npt-constraints.md` as the authoritative NPT-013 constraint source. That file was generated in parallel and should be consulted for the full C-001 through C-030 constraint text.

Auto-escalation rule AE-002 applies to this workflow: updating `mandatory-skill-usage.md` in Phase 4 (Step 12) touches `.context/rules/` and is auto-C3 minimum. This plan already classifies the workflow at C3, so no additional escalation is required.

**Quality review clarification:** The governance criticality classification is C3 (Significant). However, every individual creator output uses the C4 strategy set (all 10 strategies). This means quality enforcement operates at C4 intensity throughout, even though the governance and AE-rule classification remains C3.

**P-043:** This plan is an internal orchestration artifact generated by the Jerry framework. It does not represent official NASA guidance or any external authority.
