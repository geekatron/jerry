# Initiative: Development Skill Creation

> **ID**: INIT-DEV-SKILL
> **PS ID**: dev-skill
> **Status**: 🔄 IN PROGRESS
> **Created**: 2026-01-09
> **Branch**: cc/task-subtask

---

## Executive Summary

Create a `development` skill with specialized agents (dev-engineer, dev-qa, dev-reviewer) that embed quality criteria directly into the agent prompts, with an iterative validation loop that continues until all constraints pass.

---

## Problem Statement

### What We're Solving

Instead of building a work-tracker tool to track tasks, we're building a **development skill with agents that embody the quality criteria** and enforce them through an iterative validation loop.

### Why This Approach

1. Quality gates are **in the agents**, not in a separate tracking system
2. Leverages Claude's subagent capability as the enforcement mechanism
3. Uses the existing ps-* pattern that's already battle-tested
4. Agents persist artifacts that downstream agents read (P-002)

---

## Enforced Constraints

> ALL constraints MUST be validated before completion.

| ID | Constraint | Description | Validated In |
|----|------------|-------------|--------------|
| c-001 | 5W1H Research | 5W1H analysis before ANY implementation | V1 |
| c-002 | Context7 + WebSearch | Deep research with library docs and web | V1 |
| c-003 | Evidence-Based Citations | All decisions backed by authoritative sources | V1 |
| c-004 | Architecture Patterns | DDD, Hexagonal, CQRS, ES, Repository, DI | V1 |
| c-005 | Full Test Pyramid | Unit, Integration, System, E2E, Contract, Architecture | V1 |
| c-006 | No Placeholders | Real tests only, no stubs or fake data | V1 |
| c-007 | Edge Case Testing | Happy path + negative + edge + failure scenarios | V1 |
| c-008 | Actionable Feedback | QA provides specific, actionable feedback | V1 |
| c-009 | Escalation Path | Max 3 iterations → Distinguished Arch → User | V1 |
| c-010 | WORKTRACKER Integration | How skill integrates with tracking | D5, V1 |
| c-011 | Session Start Location | Where Claude sessions should start | D5, V1 |
| c-012 | State File Conflicts | .jerry state files handled correctly | D5, V1 |

---

## Workflow Orchestration

### Pattern Usage Summary

| Pattern | Name | Usage |
|---------|------|-------|
| Pattern 3 | Fan-Out (Parallel) | Phase 1: 6 parallel researchers |
| Pattern 4 | Fan-In (Synthesis) | Phase 2: Combine research |
| Pattern 2 | Sequential Chain | Phase 3: Sequential analysis |
| Pattern 5 | Research→Decision→Validation | Phase 4-5: ADRs + Validation |
| Pattern 1 | Single Agent | Phases 6-7: Review + Report |

---

## Phase 1: Parallel Research (Pattern 3 - Fan-Out)

```
═══════════════════════════════════════════════════════════════════════════════
                         PHASE 1: PARALLEL RESEARCH
                         Pattern 3 (Fan-Out)
                         6 parallel ps-researcher invocations
═══════════════════════════════════════════════════════════════════════════════

     ┌───────────────┐ ┌───────────────┐ ┌───────────────┐
     │ ps-researcher │ │ ps-researcher │ │ ps-researcher │
     │     R1        │ │     R2        │ │     R3        │
     │ Agent-based   │ │ Quality gates │ │ BDD/TDD in    │
     │ dev workflows │ │ enforcement   │ │ multi-agent   │
     └───────┬───────┘ └───────┬───────┘ └───────┬───────┘
             │                 │                 │
             ▼                 ▼                 ▼
         e-001.md          e-002.md          e-003.md

     ┌───────────────┐ ┌───────────────┐ ┌───────────────┐
     │ ps-researcher │ │ ps-researcher │ │ ps-researcher │
     │     R4        │ │     R5        │ │     R6        │
     │ Distinguished │ │ Concurrent    │ │ Task template │
     │ eng reviews   │ │ file access   │ │ schemas       │
     └───────┬───────┘ └───────┬───────┘ └───────┬───────┘
             │                 │                 │
             ▼                 ▼                 ▼
         e-004.md          e-005.md          e-006.md
```

### Research Tasks

| ID | Entry | Topic | Sources | Output |
|----|-------|-------|---------|--------|
| R1 | e-001 | Agent-based software development workflows | Context7, Google ADK, Anthropic | `research/dev-skill-e-001-agent-dev-workflows.md` |
| R2 | e-002 | Quality gate enforcement in CI/CD and agents | Google SRE, NASA IV&V, SWEBOK | `research/dev-skill-e-002-quality-gates.md` |
| R3 | e-003 | BDD/TDD in multi-agent systems | Context7 (behave, pytest-bdd), Beck | `research/dev-skill-e-003-bdd-multi-agent.md` |
| R4 | e-004 | Distinguished engineer review practices | Google Eng Practices, NASA SE Handbook | `research/dev-skill-e-004-distinguished-reviews.md` |
| R5 | e-005 | Concurrent file access patterns | Context7 (filelock), atomicwrites, Snowflake | `research/dev-skill-e-005-concurrent-access.md` |
| R6 | e-006 | Task template schemas | Jira, Linear, Scrum Guide, SAFe | `research/dev-skill-e-006-task-templates.md` |

---

## Phase 2: Synthesis (Pattern 4 - Fan-In)

```
═══════════════════════════════════════════════════════════════════════════════
                         PHASE 2: SYNTHESIS
                         Pattern 4 (Fan-In)
                         1 ps-synthesizer combining all research
═══════════════════════════════════════════════════════════════════════════════

  e-001 ──┐
  e-002 ──┤
  e-003 ──┼──▶ ┌─────────────────┐
  e-004 ──┤    │  ps-synthesizer │ ──▶ e-007.md
  e-005 ──┤    │      S1         │     (patterns, lessons,
  e-006 ──┘    └─────────────────┘      anti-patterns)
```

### Synthesis Task

| ID | Entry | Input | Output |
|----|-------|-------|--------|
| S1 | e-007 | e-001 through e-006 | `synthesis/dev-skill-e-007-pattern-synthesis.md` |

**Extraction Targets:**
- Patterns (PAT-xxx)
- Lessons Learned (LES-xxx)
- Anti-patterns (ANT-xxx)
- Contradictions between sources

---

## Phase 3: Analysis (Pattern 2 - Sequential)

```
═══════════════════════════════════════════════════════════════════════════════
                         PHASE 3: ANALYSIS
                         Pattern 2 (Sequential Chain)
                         3 sequential ps-analyst invocations
═══════════════════════════════════════════════════════════════════════════════

     ┌────────────────┐    ┌────────────────┐    ┌────────────────┐
     │   ps-analyst   │───▶│   ps-analyst   │───▶│   ps-analyst   │
     │      A1        │    │      A2        │    │      A3        │
     │ Trade-offs     │    │ Gap analysis   │    │ Risk (FMEA)    │
     └────────────────┘    └────────────────┘    └───────┬────────┘
            │                     │                      │
            ▼                     ▼                      ▼
        e-008.md              e-009.md               e-010.md
```

### Analysis Tasks

| ID | Entry | Type | Input | Output |
|----|-------|------|-------|--------|
| A1 | e-008 | Trade-off | e-007 | `analysis/dev-skill-e-008-trade-off.md` |
| A2 | e-009 | Gap Analysis | e-007, e-008 | `analysis/dev-skill-e-009-gap-analysis.md` |
| A3 | e-010 | Risk (FMEA) | e-007, e-008, e-009 | `analysis/dev-skill-e-010-risk-fmea.md` |

---

## Phase 4: Architecture Decisions (Pattern 5)

```
═══════════════════════════════════════════════════════════════════════════════
                         PHASE 4: ARCHITECTURE DECISIONS
                         Pattern 5 (Research → Decision)
                         5 sequential ps-architect invocations
═══════════════════════════════════════════════════════════════════════════════

     ┌──────────────┐   ┌──────────────┐   ┌──────────────┐
     │ ps-architect │──▶│ ps-architect │──▶│ ps-architect │
     │     D1       │   │     D2       │   │     D3       │
     │ ADR: Skill   │   │ ADR: Agent   │   │ ADR: Task    │
     │ architecture │   │ structure    │   │ templates    │
     └──────────────┘   └──────────────┘   └──────────────┘
            │                  │                  │
            ▼                  ▼                  ▼
        e-011.md           e-012.md           e-013.md

                        ┌──────────────┐   ┌──────────────┐
                     ──▶│ ps-architect │──▶│ ps-architect │
                        │     D4       │   │     D5       │
                        │ ADR: Iter    │   │ ADR: Work    │
                        │ loop design  │   │ tracker integ│
                        └──────────────┘   └──────────────┘
                               │                  │
                               ▼                  ▼
                           e-014.md           e-015.md
```

### Decision Tasks

| ID | Entry | ADR Topic | Input | Output |
|----|-------|-----------|-------|--------|
| D1 | e-011 | Skill Overall Architecture | e-007 to e-010 | `decisions/dev-skill-e-011-adr-architecture.md` |
| D2 | e-012 | Agent Structure (eng, qa, reviewer) | e-011 | `decisions/dev-skill-e-012-adr-agents.md` |
| D3 | e-013 | Task Template Schema | e-011, e-012 | `decisions/dev-skill-e-013-adr-templates.md` |
| D4 | e-014 | Iteration Loop Design | e-011, e-012 | `decisions/dev-skill-e-014-adr-iteration.md` |
| D5 | e-015 | WORKTRACKER Integration | e-011 to e-014 | `decisions/dev-skill-e-015-adr-integration.md` |

---

## Phases 5-7: Validation, Review, Report

```
═══════════════════════════════════════════════════════════════════════════════
                    ITERATION LOOP ENTRY POINT
═══════════════════════════════════════════════════════════════════════════════
                               │
                               ▼
                    ┌─────────────────────┐
                    │    ps-validator     │
                    │         V1          │
                    │                     │
                    │ Validates:          │
                    │ c-001 through c-012 │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   ALL CONSTRAINTS   │
                    │      PASSED?        │
                    └──────────┬──────────┘
                               │
             ┌─────────────────┴─────────────────┐
             │ YES                               │ NO
             ▼                                   ▼
      ┌─────────────┐                    ┌──────────────────┐
      │   PHASE 6   │                    │ ITERATION LOGIC  │
      │   REVIEW    │                    │                  │
      │             │                    │ iter++ <= 3?     │
      │ ps-reviewer │                    │   → Back to D1   │
      └──────┬──────┘                    │                  │
             │                           │ iter > 3?        │
             ▼                           │   → ESCALATE     │
      ┌─────────────┐                    │   → Dist. Arch   │
      │  PASSED?    │                    │   → Then User    │
      └──────┬──────┘                    └────────┬─────────┘
             │                                    │
    ┌────────┴────────┐                           │
    │ PASS            │ NEEDS_WORK                │
    ▼                 ▼                           │
┌─────────┐    ┌───────────────┐                  │
│ PHASE 7 │    │ Back to iter  │◀─────────────────┘
│ REPORT  │    │ loop with     │
│         │    │ feedback      │
└────┬────┘    └───────────────┘
     │
     ▼
┌─────────────────────┐
│   USER APPROVAL     │
│   GATE              │
└─────────────────────┘
```

### Validation/Review/Report Tasks

| ID | Entry | Agent | Output |
|----|-------|-------|--------|
| V1 | e-016 | ps-validator | `analysis/dev-skill-e-016-validation.md` |
| REV1 | e-017 | ps-reviewer | `reviews/dev-skill-e-017-design-review.md` |
| REP1 | e-018 | ps-reporter | `reports/dev-skill-e-018-status.md` |

---

## Iteration Loop State Machine

```
═══════════════════════════════════════════════════════════════════════════════
                    ITERATION LOOP STATE MACHINE
═══════════════════════════════════════════════════════════════════════════════

                         ┌───────────────┐
                         │   START       │
                         │ iteration = 0 │
                         └───────┬───────┘
                                 │
                                 ▼
                   ┌─────────────────────────┐
                   │     PHASE 4: DECIDE     │◀────────────────────────────┐
                   │     (ps-architect)      │                             │
                   └────────────┬────────────┘                             │
                                │                                          │
                                ▼                                          │
                   ┌─────────────────────────┐                             │
                   │     PHASE 5: VALIDATE   │                             │
                   │     (ps-validator)      │                             │
                   └────────────┬────────────┘                             │
                                │                                          │
                                ▼                                          │
                         ┌─────────────┐                                   │
                         │   PASSED?   │                                   │
                         └──────┬──────┘                                   │
                                │                                          │
               ┌────────────────┴────────────────┐                         │
               │ YES                             │ NO                      │
               ▼                                 ▼                         │
        ┌─────────────┐                   ┌─────────────┐                  │
        │ SUCCESS     │                   │ iteration++ │                  │
        └──────┬──────┘                   └──────┬──────┘                  │
               │                                 │                         │
               │                                 ▼                         │
               │                          ┌─────────────┐                  │
               │                          │ iter <= 3 ? │                  │
               │                          └──────┬──────┘                  │
               │                                 │                         │
               │                    ┌────────────┴────────────┐            │
               │                    │ YES                     │ NO         │
               │                    ▼                         ▼            │
               │             ┌─────────────┐           ┌─────────────┐     │
               │             │ ACTIONABLE  │           │ ESCALATE TO │     │
               │             │ FEEDBACK    │           │ DIST. ARCH  │     │
               │             └──────┬──────┘           └──────┬──────┘     │
               │                    │                         │            │
               │                    │                         ▼            │
               │                    │                  ┌─────────────┐     │
               │                    │                  │  RESOLVED?  │     │
               │                    │                  └──────┬──────┘     │
               │                    │                         │            │
               │                    │            ┌────────────┴────────┐   │
               │                    │            │ YES                 │NO │
               │                    │            ▼                     ▼   │
               │                    │     ┌─────────────┐       ┌─────────┐│
               │                    │     │ FEEDBACK    │       │ASK USER ││
               │                    │     └──────┬──────┘       └────┬────┘│
               │                    │            │                   │     │
               │                    └────────────┴───────────────────┘     │
               │                                 │                         │
               │                                 └─────────────────────────┘
               │
               ▼
        ┌─────────────┐
        │ PHASE 6:    │
        │ REVIEW      │
        └──────┬──────┘
               │
               ▼
        ┌─────────────┐
        │  PASSED?    │
        └──────┬──────┘
               │
  ┌────────────┴────────────┐
  │ PASS/CONCERNS           │ NEEDS_WORK/FAIL
  ▼                         ▼
┌─────────────┐      ┌─────────────┐
│ PHASE 7:    │      │ RETURN TO   │
│ REPORT      │      │ ITERATION   │────────────────────────────────────────┐
└─────────────┘      └─────────────┘                                        │
                                                                            │
                            (Back to PHASE 4 with review feedback)          │
                                                                            │
                                      ┌─────────────────────────────────────┘
                                      │
                                      ▼
                        ┌─────────────────────────┐
                        │     PHASE 4: DECIDE     │
                        │  (with review feedback) │
                        └─────────────────────────┘
```

---

## Actionable Feedback Format

When validation fails, feedback MUST be structured:

```yaml
validation_feedback:
  iteration: 1
  status: "GAPS_FOUND"
  total_constraints: 12
  passed: 9
  failed: 3
  gaps:
    - constraint_id: "c-005"
      description: "All test types required"
      status: "PARTIAL"
      evidence: "ADR-DEV-002 mentions Unit/Integration but omits Contract"
      remediation: "Add Contract test requirements to agent criteria"
      artifact_location: "decisions/dev-skill-e-012-adr-agent-structure.md"
      line_numbers: [45, 67]
  next_action: "ITERATE"
  target_phase: "PHASE_4"
  target_artifact: "e-012"
```

---

## Artifact Dependency Graph

```
                        PHASE 1: Research (Parallel)
    ┌──────────┬──────────┬──────────┬──────────┬──────────┐
    │          │          │          │          │          │
  e-001      e-002      e-003      e-004      e-005      e-006
    │          │          │          │          │          │
    └──────────┴──────────┴────┬─────┴──────────┴──────────┘
                               │
                        PHASE 2: Synthesis
                               │
                             e-007
                               │
        ┌──────────────────────┼──────────────────────┐
        │                      │                      │
     PHASE 3: Analysis (Sequential)
        │                      │                      │
      e-008 ─────────────▶ e-009 ─────────────▶ e-010
        │                      │                      │
        └──────────────────────┼──────────────────────┘
                               │
        PHASE 4: Architecture Decisions (Sequential)
                               │
      e-011 ──▶ e-012 ──▶ e-013 ──▶ e-014 ──▶ e-015
        │                                         │
        └─────────────────────┬───────────────────┘
                              │
                       PHASE 5: Validation
                              │
                            e-016 ◀──────────────────────┐
                              │                          │
                       PHASE 6: Review                   │
                              │                          │
                            e-017                        │
                              │                          │
                    ┌─────────┴─────────┐                │
                    │                   │                │
                  PASS              NEEDS_WORK ──────────┘
                    │
             PHASE 7: Report
                    │
                  e-018
                    │
                    ▼
            ┌─────────────────┐
            │ USER APPROVAL   │
            └─────────────────┘
```

---

## Execution Tracker

| Phase | Pattern | Agent | Entry | Status | Artifact |
|-------|---------|-------|-------|--------|----------|
| 1.1 | Fan-Out | ps-researcher | e-001 | ⏳ | `research/dev-skill-e-001-*.md` |
| 1.2 | Fan-Out | ps-researcher | e-002 | ⏳ | `research/dev-skill-e-002-*.md` |
| 1.3 | Fan-Out | ps-researcher | e-003 | ⏳ | `research/dev-skill-e-003-*.md` |
| 1.4 | Fan-Out | ps-researcher | e-004 | ⏳ | `research/dev-skill-e-004-*.md` |
| 1.5 | Fan-Out | ps-researcher | e-005 | ⏳ | `research/dev-skill-e-005-*.md` |
| 1.6 | Fan-Out | ps-researcher | e-006 | ⏳ | `research/dev-skill-e-006-*.md` |
| 2 | Fan-In | ps-synthesizer | e-007 | ⏳ | `synthesis/dev-skill-e-007-*.md` |
| 3.1 | Sequential | ps-analyst | e-008 | ⏳ | `analysis/dev-skill-e-008-*.md` |
| 3.2 | Sequential | ps-analyst | e-009 | ⏳ | `analysis/dev-skill-e-009-*.md` |
| 3.3 | Sequential | ps-analyst | e-010 | ⏳ | `analysis/dev-skill-e-010-*.md` |
| 4.1 | Sequential | ps-architect | e-011 | ⏳ | `decisions/dev-skill-e-011-*.md` |
| 4.2 | Sequential | ps-architect | e-012 | ⏳ | `decisions/dev-skill-e-012-*.md` |
| 4.3 | Sequential | ps-architect | e-013 | ⏳ | `decisions/dev-skill-e-013-*.md` |
| 4.4 | Sequential | ps-architect | e-014 | ⏳ | `decisions/dev-skill-e-014-*.md` |
| 4.5 | Sequential | ps-architect | e-015 | ⏳ | `decisions/dev-skill-e-015-*.md` |
| 5 | Single | ps-validator | e-016 | ⏳ | `analysis/dev-skill-e-016-*.md` |
| 6 | Single | ps-reviewer | e-017 | ⏳ | `reviews/dev-skill-e-017-*.md` |
| 7 | Single | ps-reporter | e-018 | ⏳ | `reports/dev-skill-e-018-*.md` |

---

## Iteration History

| Iteration | Date | Gaps Found | Status | Next Action |
|-----------|------|------------|--------|-------------|
| 0 | - | - | NOT_STARTED | Begin Phase 1 |

---

## Document History

| Date | Author | Changes |
|------|--------|---------|
| 2026-01-09 | Claude | Initial creation with full workflow |
