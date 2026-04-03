# Use Case Capability Build: Orchestration Worktracker

> **Type:** orchestration-worktracker
> **Status:** pending
> **Workflow ID:** use-case-skills-20260308-001
> **Project:** PROJ-021-use-case
> **GitHub Issue:** #109
> **Created:** 2026-03-08T00:00:00Z
> **Criticality:** C3 (governance) / C4 quality reviews at every creator output
> **Quality Threshold:** >= 0.95
> **Max Iterations per Adversary Loop:** 6

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Worktracker Entities](#worktracker-entities) | /worktracker entities to create before execution |
| [Execution Log](#execution-log) | Step-by-step execution record (updated by orch-tracker) |
| [Gate Decisions](#gate-decisions) | Quality gate pass/fail record (phase gates + per-step adversary loops) |
| [Checkpoint Log](#checkpoint-log) | Session resume points |
| [Routing Decisions](#routing-decisions) | Routing record per RT-M-008 |
| [Blockers](#blockers) | Current and persistent blockers |
| [Progress Dashboard](#progress-dashboard) | At-a-glance workflow status |
| [Constraint Compliance Checklist](#constraint-compliance-checklist) | Pre-execution verification |

---

## Worktracker Entities

The following /worktracker entities MUST be created before execution begins (C-027). Entity templates are at `.context/templates/worktracker/`.

### Required Entities

| Entity Type | ID (suggested) | Title | Parent | Status |
|-------------|----------------|-------|--------|--------|
| EPIC | EPIC-021-001 | Use Case Capability Build | — (top-level) | pending |
| FEATURE | FEAT-021-001 | /use-case Skill | EPIC-021-001 | pending |
| FEATURE | FEAT-021-002 | /test-spec Skill | EPIC-021-001 | pending |
| FEATURE | FEAT-021-003 | /contract-design Skill | EPIC-021-001 | pending |
| ENABLER | EN-021-001 | Use Case Methodology Research | FEAT-021-001 | pending |
| ENABLER | EN-021-002 | Shared Architecture Design | FEAT-021-001 | pending |
| ENABLER | EN-021-003 | Red-Team Security Review | EPIC-021-001 | pending |
| STORY | ST-021-001 | Guided Use Case Authoring Workflow | FEAT-021-001 | pending |
| STORY | ST-021-002 | Use Case Slicing with Jacobson Patterns | FEAT-021-001 | pending |
| STORY | ST-021-003 | Use Case Index and Navigation | FEAT-021-001 | pending |
| STORY | ST-021-004 | BDD Test Plan Generation from Use Cases | FEAT-021-002 | pending |
| STORY | ST-021-005 | TDD Coverage Analysis | FEAT-021-002 | pending |
| STORY | ST-021-006 | OpenAPI Contract Generation | FEAT-021-003 | pending |
| STORY | ST-021-007 | CloudEvents/AsyncAPI Contract Generation | FEAT-021-003 | pending |
| STORY | ST-021-008 | Worktracker Integration (UC → Features/Stories) | FEAT-021-001 | pending |

### Entity Creation Note

Per WTI-007: read canonical worktracker templates from `.context/templates/worktracker/` before creating entity files. Use EPIC.md, FEATURE.md, ENABLER.md, STORY.md, and TASK.md templates respectively.

Per C-019 and C-027: all entities above MUST be created and their IDs registered in the project WORKTRACKER.md before Step 1 (first research agent) executes.

---

## Execution Log

Updated by orch-tracker after each agent completion. Adversary loop outcomes are recorded alongside the creator step they protect.

| # | Date | Group | Step / Sub-Step | Agent | Status | Adversary Iter | Adversary Score | Notes |
|---|------|-------|-----------------|-------|--------|----------------|-----------------|-------|
| — | — | — | — | — | — | — | — | Awaiting first execution |

---

## Gate Decisions

### Phase-Boundary Quality Gates

| Gate | Date | Score | Threshold | Result | Iterations Used | Critic Findings Summary |
|------|------|-------|-----------|--------|-----------------|------------------------|
| GATE-1 | — | — | 0.95 | pending | — | — |
| GATE-2 | — | — | 0.95 | pending | — | — |
| GATE-3 | — | — | 0.95 | pending | — | — |
| GATE-4 | — | — | 0.95 | pending | — | — |
| GATE-5 | — | — | 0.95 | pending | — | — |
| GATE-5b | — | — | 0.95 | pending | — | — |
| GATE-6 | — | — | 0.95 | pending | — | — |

### Per-Step Adversary Loop Outcomes

Individual C4 adversary reviews at every creator output. Populated by orch-tracker as each loop completes.

#### Phase 1 Adversary Loops

| Step Output | Final Score | Iterations | Result | Notes |
|-------------|-------------|------------|--------|-------|
| step-1 (Jacobson research) | — | — | pending | — |
| step-2 (Cockburn research) | — | — | pending | — |
| step-3 (Industry sources) | — | — | pending | — |
| step-4 (Anthropic best practices) | — | — | pending | — |
| step-5 (Jerry pattern analysis) | — | — | pending | — |
| synthesis (phase-1-synthesis.md) | — | — | pending | — |

#### Phase 2 Adversary Loops

| Step Output | Final Score | Iterations | Result | Notes |
|-------------|-------------|------------|--------|-------|
| step-6 (File organization design) | — | — | pending | — |
| step-8-draft (Agent decomp draft) | — | — | pending | — |
| step-7 (Frontmatter schema) | — | — | pending | — |
| step-8-final (Agent decomp final) | — | — | pending | — |

#### Phase 3 Adversary Loops — /use-case (Step 9)

| Sub-Step Output | Final Score | Iterations | Result | Notes |
|-----------------|-------------|------------|--------|-------|
| eng-architect (skill architecture) | — | — | pending | — |
| eng-lead (standards enforcement review) | — | — | pending | — |
| eng-backend (agent implementation) | — | — | pending | — |
| eng-qa (test strategy) | — | — | pending | — |
| eng-security (security review) | — | — | pending | — |
| eng-reviewer (final review gate) | — | — | pending | — |

#### Phase 3 Adversary Loops — /test-spec (Step 10)

| Sub-Step Output | Final Score | Iterations | Result | Notes |
|-----------------|-------------|------------|--------|-------|
| eng-architect (skill architecture) | — | — | pending | — |
| eng-lead (standards enforcement review) | — | — | pending | — |
| eng-backend (agent implementation) | — | — | pending | — |
| eng-qa (test strategy) | — | — | pending | — |
| eng-security (security review) | — | — | pending | — |
| eng-reviewer (final review gate) | — | — | pending | — |

#### Phase 3 Adversary Loops — /contract-design (Step 11)

| Sub-Step Output | Final Score | Iterations | Result | Notes |
|-----------------|-------------|------------|--------|-------|
| eng-architect (skill architecture) | — | — | pending | — |
| eng-lead (standards enforcement review) | — | — | pending | — |
| eng-backend (agent implementation) | — | — | pending | — |
| eng-qa (test strategy) | — | — | pending | — |
| eng-security (security review) | — | — | pending | — |
| eng-reviewer (final review gate) | — | — | pending | — |

#### Phase 3b Adversary Loops — Red-Team (Step 11b)

| Sub-Step Output | Final Score | Iterations | Result | Notes |
|-----------------|-------------|------------|--------|-------|
| red-lead (scope document) | — | — | pending | — |
| red-vuln (vulnerability analysis) | — | — | pending | — |
| red-reporter (findings report) | — | — | pending | — |

#### Phase 4 Adversary Loops

| Step Output | Final Score | Iterations | Result | Notes |
|-------------|-------------|------------|--------|-------|
| step-13 (E2E verification report) | — | — | pending | — |

---

## Checkpoint Log

| CP | Gate | Date | Resumable From | State File |
|----|------|------|----------------|-----------|
| CP-001 | GATE-1 | — | Phase 2, Group G-04 | ORCHESTRATION.yaml |
| CP-002 | GATE-2 | — | Phase 3, Group G-08 | ORCHESTRATION.yaml |
| CP-003 | GATE-3 | — | Phase 3, Group G-10 | ORCHESTRATION.yaml |
| CP-004 | GATE-4 | — | Phase 3, Group G-12 | ORCHESTRATION.yaml |
| CP-005 | GATE-5 | — | Phase 3b, Group G-13b-scope | ORCHESTRATION.yaml |
| CP-005b | GATE-5b | — | Phase 4, Group G-14 | ORCHESTRATION.yaml |
| CP-006 | GATE-6 | — | Workflow complete | ORCHESTRATION.yaml |

**Resume Protocol:** Read `ORCHESTRATION.yaml` → find last checkpoint with `status: passed` → resume at the next pending execution group.

---

## Routing Decisions

Per RT-M-008. Updated as routing decisions are made.

| # | Method | Layer | Selected Skill | Keywords Matched | Suppressed | Confidence | User Corrected |
|---|--------|-------|----------------|-----------------|------------|------------|----------------|
| 1 | explicit | 0 | /orchestration | orchestration, workflow, phases, multi-agent | — | 1.0 | No |

---

## Blockers

No blockers at plan creation time.

**Active Blockers:** None

**Resolved Blockers:** None

> **Note:** Persistent blockers are prefixed with `[PERSISTENT]` per HD-M-005 and CP-05.

---

## Progress Dashboard

```
WORKFLOW: use-case-skills-20260308-001
STATUS: PLANNED
CRITICALITY: C3 (governance) | QUALITY REVIEWS: C4 (all 10 strategies at every output)
QUALITY THRESHOLD: >= 0.95 | MAX ADVERSARY ITERATIONS: 6

+-----------------------------------------------------------------------+
|                  USE CASE CAPABILITY BUILD                             |
+-----------------------------------------------------------------------+
| Phase 1: Research          [....................] 0%  (0/6 steps)      |
| Phase 2: Architecture      [....................] 0%  (0/4 steps)      |
| Phase 3: Implementation    [....................] 0%  (0/3 steps)      |
| Phase 3b: Red-Team Review  [....................] 0%  (0/3 sub-steps)  |
| Phase 4: Integration       [....................] 0%  (0/3 steps)      |
+-----------------------------------------------------------------------+
| Phase Gates (7 total):     [....................] 0%  (0/7 passed)     |
| Adversary Loops (~32):     [....................] 0%  (0/~32 passed)   |
| Skills Implemented:        [....................] 0%  (0/3 live)       |
+-----------------------------------------------------------------------+
| Overall:                   [....................] 0%                    |
+-----------------------------------------------------------------------+

NEXT ACTION: Create /worktracker entities (EPIC-021-001, FEAT-021-001 through FEAT-021-003,
             EN-021-001 through EN-021-003, ST-021-001 through ST-021-008)
             then execute Group G-01 (fan-out research).
```

---

## Constraint Compliance Checklist

Verify before execution starts:

- [ ] C-001: Orchestration plan created (ORCHESTRATION_PLAN.md + ORCHESTRATION.yaml)
- [ ] C-005: Main context configured as orchestrator-only (no deliverable production)
- [ ] C-006: /worktracker entities created (EPIC, 3 FEATUREs, 3 ENABLERs, 8 STORYs)
- [ ] C-007: Every creator output assigned a background /adversary C4 loop
- [ ] C-009: Max iterations set to 6 in all adversary loops and all gates
- [ ] C-018: ORCHESTRATION.yaml complete phase definitions verified (5 phases, 7 gates, adversary_loop_config defined)
- [ ] C-019: ORCHESTRATION_WORKTRACKER.md created (this file)
- [ ] C-027: Entities created before first execution step
- [ ] NPT constraints file exists at `projects/PROJ-021-use-case/work/prompt-engineering/npt-constraints.md`
- [ ] Active project PROJ-021-use-case set (H-04)
- [ ] Red-team review phase (Phase 3b) acknowledged: Phase 4 prerequisite is GATE-5b (not GATE-5)

---

## Disclaimer

This orchestration worktracker was generated by the orch-planner agent (v2.2.0) for workflow use-case-skills-20260308-001. Human review recommended before execution begins.
