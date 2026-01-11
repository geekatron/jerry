# Implementation Roadmap: Skills & Agents Optimization Initiative

> **Document ID:** PS-S-001-IMPL-ROADMAP
> **Phase:** 4 - Synthesis (ps-* Pipeline)
> **Project:** PROJ-002-nasa-systems-engineering
> **Workflow:** WF-SAO-CROSSPOLL-001
> **Date:** 2026-01-10
> **Agent:** ps-s-002 (Implementation Roadmap Specialist)
> **Entry ID:** ps-s-002
> **Status:** COMPLETE

---

## L0: Executive Summary

This roadmap translates the SAO (Skills & Agents Optimization) initiative into an actionable implementation plan. The initiative addresses 14 gaps identified through cross-pollinated analysis and requires ~302 engineering hours across 5 phases.

### Key Metrics

| Metric | Value |
|--------|-------|
| Total Work Items | 21 |
| Completed | 4 (19%) |
| Remaining | 17 |
| Total Effort | ~302 hours |
| Timeline | 9 weeks |
| Critical Path Length | 6 dependencies |
| RED Risks Mitigated | 3 (MIT-SAO-001, 002, 003) |

### Phase Summary

```
PHASE 1: Foundation       [####------] 80% (4/5 complete)    ~32h  | Week 1-2
PHASE 2: New Agents       [----------]  0% (0/5 complete)    ~72h  | Week 3-4
PHASE 3: Template Unify   [----------]  0% (0/3 complete)    ~32h  | Week 5
PHASE 4: Infrastructure   [----------]  0% (0/5 complete)    ~104h | Week 6-8
PHASE 5: Technical Debt   [----------]  0% (0/3 complete)    ~62h  | Week 9+
```

### Priority Stack (Next 3 Items)

1. **WI-SAO-002**: Schema Validation (8h) - CRITICAL - Current focus
2. **WI-SAO-004**: nse-explorer Agent (16h) - CRITICAL - Divergent capacity
3. **WI-SAO-005**: nse-orchestrator Agent (16h) - HIGH - Enables parallel execution

---

## L1: Detailed Implementation Roadmap

### 1.1 Phase Dependencies Visualization

```
                         SAO IMPLEMENTATION DEPENDENCY GRAPH
    +------------------------------------------------------------------------+
    |                                                                        |
    |  PHASE 1: FOUNDATION                                                   |
    |  ===================                                                   |
    |                                                                        |
    |  [WI-SAO-001] ----+                                                    |
    |  Schema Define    |                                                    |
    |  COMPLETE         +---> [WI-SAO-002] ----+                             |
    |                   |     Schema Validate  |                             |
    |  [WI-SAO-003] ----+     IN PROGRESS      |                             |
    |  Model Field             |               |                             |
    |  COMPLETE                |               |                             |
    |                          |               |                             |
    |  [WI-SAO-019] --->  [WI-SAO-020]         |                             |
    |  Architecture    Output Conventions      |                             |
    |  COMPLETE        COMPLETE                |                             |
    |                                          |                             |
    +------------------------------------------+-----------------------------+
                                               |
                                               v
    +------------------------------------------------------------------------+
    |                                                                        |
    |  PHASE 2: NEW AGENTS                                                   |
    |  ===================                                                   |
    |                                                                        |
    |  [WI-SAO-004] --------+                                                |
    |  nse-explorer         |                                                |
    |  (Divergent)          |                                                |
    |       |               |                                                |
    |       |               +--> [WI-SAO-008]                                |
    |       |               |    nse-qa                                      |
    |       v               |    (Critic)                                    |
    |  [WI-SAO-005] --------+                                                |
    |  nse-orchestrator     |                                                |
    |  (Coordinator)        |                                                |
    |       |               |                                                |
    |       |               +--> [WI-SAO-007]                                |
    |       |               |    ps-critic                                   |
    |       |               |    (Critic)                                    |
    |       v               |                                                |
    |  [WI-SAO-006] --------+                                                |
    |  ps-orchestrator                                                       |
    |  (Coordinator)                                                         |
    |                                                                        |
    +------------------------------------------------------------------------+
                                               |
                                               v
    +------------------------------------------------------------------------+
    |                                                                        |
    |  PHASE 3: TEMPLATE UNIFICATION                                         |
    |  =============================                                         |
    |                                                                        |
    |  [WI-SAO-009] ----+--> [WI-SAO-010] (ps-* migration)                   |
    |  Unified Template |                                                    |
    |                   +--> [WI-SAO-011] (nse-* migration)                  |
    |                                                                        |
    +------------------------------------------------------------------------+
                                               |
                                               v
    +------------------------------------------------------------------------+
    |                                                                        |
    |  PHASE 4: INFRASTRUCTURE                                               |
    |  =======================                                               |
    |                                                                        |
    |  [WI-SAO-012] ----+--> [WI-SAO-013] ----+--> [WI-SAO-021]              |
    |  Parallel Exec    |    Checkpointing   |    Folder Refactor            |
    |  (MIT-SAO-001)    |    (WAL)           |                               |
    |                   |                    |                               |
    |  [WI-SAO-014] ----+    [WI-SAO-015]    |                               |
    |  Gen-Critic Loop       Guardrails      |                               |
    |  (MIT-SAO-002)         |               |                               |
    |       ^                |               |                               |
    |       |                +---------------+                               |
    |  Depends on                                                            |
    |  WI-SAO-007                                                            |
    |  (ps-critic)                                                           |
    |                                                                        |
    +------------------------------------------------------------------------+
                                               |
                                               v
    +------------------------------------------------------------------------+
    |                                                                        |
    |  PHASE 5: TECHNICAL DEBT                                               |
    |  ======================                                                |
    |                                                                        |
    |  [WI-SAO-016] ----+--> [WI-SAO-017] ----+--> [WI-SAO-018]              |
    |  Interface         |   Tool Registry    |   Schema Versioning          |
    |  Contracts         |                    |                              |
    |  (MIT-SAO-003)     |                    |                              |
    |                                                                        |
    +------------------------------------------------------------------------+
```

### 1.2 Gantt-Style Timeline

```
                         SAO IMPLEMENTATION TIMELINE (9 WEEKS)
    +------------------------------------------------------------------------+
    |                                                                        |
    | WEEK:  1    2    3    4    5    6    7    8    9                       |
    |        |    |    |    |    |    |    |    |    |                       |
    | -------|----|----|----|----|----|----|----|----|---------------------- |
    |                                                                        |
    | PHASE 1: Foundation                                                    |
    | [====#====]                                                            |
    |  ^4/5 complete                                                         |
    |                                                                        |
    | PHASE 2: New Agents                                                    |
    |           [==========#==========]                                      |
    |           SAO-004  SAO-005  SAO-006  SAO-007  SAO-008                  |
    |                                                                        |
    | PHASE 3: Template Unification                                          |
    |                     [=====#=====]                                      |
    |                     SAO-009 → SAO-010, SAO-011                         |
    |                                                                        |
    | PHASE 4: Infrastructure                                                |
    |                          [=======#========#=========]                  |
    |                          SAO-012  SAO-013  SAO-014  SAO-021            |
    |                                                                        |
    | PHASE 5: Technical Debt                                                |
    |                                              [====#=======]            |
    |                                              SAO-016 → SAO-018         |
    |                                                                        |
    | MILESTONES:                                                            |
    |        |    |    |    |    |    |    |    |    |                       |
    |        M1   M2        M3        M4        M5   M6                      |
    |                                                                        |
    | M1: Foundation Complete (Week 2)                                       |
    | M2: Schema Validation Ready (Week 2)                                   |
    | M3: All 5 New Agents Ready (Week 4)                                    |
    | M4: Template Migration Complete (Week 5)                               |
    | M5: Parallel Execution + Checkpointing Ready (Week 7)                  |
    | M6: Full Initiative Complete (Week 9)                                  |
    |                                                                        |
    +------------------------------------------------------------------------+
```

### 1.3 Risk-Prioritized Implementation Order

Based on the formal mitigations (MIT-SAO-MASTER), the implementation order prioritizes RED risk mitigations first:

| Priority | Work Item | Risk Mitigated | Risk Reduction | Effort |
|----------|-----------|----------------|----------------|--------|
| 1 | WI-SAO-002 | MIT-SAO-003 (Schema Validation) | 16→8 (50%) | 8h |
| 2 | WI-SAO-012 | MIT-SAO-001 (Parallel Isolation) | 16→8 (50%) | 24h |
| 3 | WI-SAO-014 | MIT-SAO-002 (Circuit Breaker) | 15→9 (40%) | 8h |
| 4 | WI-SAO-004 | GAP-NEW-005 (Cognitive Diversity) | N/A | 16h |
| 5 | WI-SAO-005 | GAP-AGT-004 (Orchestration) | N/A | 16h |

### 1.4 Effort Summary by Phase

| Phase | Work Items | Total Effort | Avg per WI | Sprint Alignment |
|-------|------------|--------------|------------|------------------|
| Phase 1 | 5 | 32h | 6.4h | Sprint 1 (partial) |
| Phase 2 | 5 | 72h | 14.4h | Sprint 1-2 |
| Phase 3 | 3 | 32h | 10.7h | Sprint 2 |
| Phase 4 | 5 | 104h | 20.8h | Sprint 2-3 |
| Phase 5 | 3 | 62h | 20.7h | Sprint 3 |
| **Total** | **21** | **302h** | **14.4h** | **3 Sprints** |

**Note:** Total effort includes both the 184 hours from formal mitigations (MIT-SAO-MASTER) and the ~118 hours from optimization work items identified in the gap analysis.

---

## L2: Task-Level Breakdown

### 2.1 Phase 1: Foundation (32h Total)

#### WI-SAO-001: Define session_context JSON Schema [COMPLETE]
- **Status:** COMPLETE (2026-01-10)
- **Effort:** 8h
- **Artifact:** `docs/schemas/session_context.json`

| Task ID | Description | Effort | Status |
|---------|-------------|--------|--------|
| T-001.1 | Define core session_context schema | 3h | DONE |
| T-001.2 | Add cross-pollination extensions | 2h | DONE |
| T-001.3 | Create validation utility documentation | 2h | DONE |
| T-001.4 | Update agent templates to reference schema | 1h | DONE |

#### WI-SAO-002: Add Schema Validation to All Agents [IN PROGRESS]
- **Status:** IN PROGRESS
- **Priority:** CRITICAL (P0) - RED Risk Mitigation
- **Effort:** 8h
- **Depends On:** WI-SAO-001
- **Risk Mitigated:** MIT-SAO-003 (R-TECH-001)

| Task ID | Description | Effort | Status |
|---------|-------------|--------|--------|
| T-002.1 | Add input validation pattern to agent templates | 3h | OPEN |
| T-002.2 | Add output validation pattern to agent templates | 2h | OPEN |
| T-002.3 | Add output validation patterns to ORCHESTRATION.md | 2h | OPEN |
| T-002.4 | Create test cases for validation | 1h | OPEN |

**Acceptance Criteria:**
1. All 16 agents (8 ps-*, 8 nse-*) validate input/output against schema
2. Validation errors produce clear, actionable messages
3. Schema violations are logged for debugging
4. No false positives on valid inputs

#### WI-SAO-003: Add Model Field to Agent Frontmatter [COMPLETE]
- **Status:** COMPLETE (2026-01-10)
- **Effort:** 4h
- **Artifact:** Updated 16 agent definitions

| Task ID | Description | Effort | Status |
|---------|-------------|--------|--------|
| T-003.1 | Update PS_AGENT_TEMPLATE.md with model field | 1h | DONE |
| T-003.2 | Update NSE_AGENT_TEMPLATE.md with model field | 1h | DONE |
| T-003.3 | Add model field to all 16 agent definitions | 2h | DONE |

#### WI-SAO-019: Agent Architecture Research [COMPLETE]
- **Status:** COMPLETE (2026-01-10)
- **Effort:** 8h
- **Artifact:** `research/agent-architecture-research.md` (700+ lines)

| Task ID | Description | Effort | Status |
|---------|-------------|--------|--------|
| R-019.1 | Apply 5W1H framework to agent architecture | 2h | DONE |
| R-019.2 | Map agents to NASA SE lifecycle phases | 2h | DONE |
| R-019.3 | Identify agent specialization patterns | 2h | DONE |
| R-019.4 | Research industry multi-agent patterns (min 5 sources) | 1.5h | DONE |
| R-019.5 | Synthesize findings + produce 3-level explanation | 0.5h | DONE |

#### WI-SAO-020: Add Agent-Specific Output Conventions [COMPLETE]
- **Status:** COMPLETE (2026-01-10)
- **Effort:** 4h
- **Artifact:** Updated PS_AGENT_TEMPLATE.md

| Task ID | Description | Effort | Status |
|---------|-------------|--------|--------|
| T-020.1 | Add output directory section to PS_AGENT_TEMPLATE.md | 2h | DONE |
| T-020.2 | Add artifact naming conventions | 1h | DONE |
| T-020.3 | Validate 8/8 ps-* agents produce correct output | 1h | DONE |

---

### 2.2 Phase 2: New Agents (72h Total)

#### WI-SAO-004: Create nse-explorer Agent (Divergent)
- **Status:** OPEN
- **Priority:** CRITICAL (P0)
- **Effort:** 16h
- **Source:** Agent Design Specs (NSE-EXP-001)
- **Gap Addressed:** GAP-NEW-005 (Cognitive Mode Homogeneity)

| Task ID | Description | Effort | Status |
|---------|-------------|--------|--------|
| T-004.1 | Create nse-explorer.md agent file | 4h | OPEN |
| T-004.2 | Implement divergent exploration patterns | 4h | OPEN |
| T-004.3 | Add NASA Process 4 (Technical Solution Definition) templates | 4h | OPEN |
| T-004.4 | Create BDD tests for nse-explorer | 2h | OPEN |
| T-004.5 | Update ORCHESTRATION.md with divergent patterns | 2h | OPEN |

**Agent Specification (from PS-D-001-AGENT-SPECS):**
```yaml
identity:
  role: "Exploratory Research and Creative Problem-Solving"
  cognitive_mode: divergent
  model: opus
capabilities:
  allowed_tools: [Read, Glob, Grep, WebSearch, WebFetch, Write]
  forbidden_actions:
    - Making final recommendations (delegate to convergent agents)
    - Eliminating options prematurely
    - Spawning subagents (P-003)
```

#### WI-SAO-005: Create nse-orchestrator Agent
- **Status:** OPEN
- **Priority:** HIGH (P1)
- **Effort:** 16h
- **Source:** Agent Design Specs (NSE-ORC-001)
- **Gap Addressed:** GAP-AGT-004 (Orchestration Gap)

| Task ID | Description | Effort | Status |
|---------|-------------|--------|--------|
| T-005.1 | Create nse-orchestrator.md agent file | 4h | OPEN |
| T-005.2 | Implement delegation manifest for nse-* agents | 4h | OPEN |
| T-005.3 | Add NPR 7123.1D process sequencing logic | 4h | OPEN |
| T-005.4 | Create BDD tests for orchestration patterns | 2h | OPEN |
| T-005.5 | Update ORCHESTRATION.md with hierarchical patterns | 2h | OPEN |

**Agent Specification:**
```yaml
identity:
  role: "NASA SE Pipeline Coordination and Workflow Management"
  cognitive_mode: mixed
  model: opus
capabilities:
  allowed_tools: [Task, Read, Write, Glob, Grep, Bash]
  forbidden_actions:
    - Performing technical analysis (delegate to specialists)
    - Spawning subagents from subagents (P-003)
```

#### WI-SAO-006: Create ps-orchestrator Agent
- **Status:** OPEN
- **Priority:** HIGH (P1)
- **Effort:** 12h
- **Source:** Agent Design Specs (PS-ORC-001)

| Task ID | Description | Effort | Status |
|---------|-------------|--------|--------|
| T-006.1 | Create ps-orchestrator.md agent file | 3h | OPEN |
| T-006.2 | Implement delegation manifest for ps-* agents | 3h | OPEN |
| T-006.3 | Add workflow templates (3) | 4h | OPEN |
| T-006.4 | Create BDD tests for ps-* orchestration | 2h | OPEN |

#### WI-SAO-007: Create ps-critic Agent
- **Status:** OPEN
- **Priority:** HIGH (P1)
- **Effort:** 12h
- **Source:** Agent Design Specs (PS-CRT-001)
- **Gap Addressed:** RGAP-009 (Generator-Critic Gap)

| Task ID | Description | Effort | Status |
|---------|-------------|--------|--------|
| T-007.1 | Create ps-critic.md agent file | 3h | OPEN |
| T-007.2 | Implement critique scoring rubric | 4h | OPEN |
| T-007.3 | Implement circuit breaker logic in template | 3h | OPEN |
| T-007.4 | Create BDD tests for generator-critic loops | 2h | OPEN |

**Agent Specification:**
```yaml
identity:
  role: "Problem-Solving Quality Critique and Refinement"
  cognitive_mode: convergent
  model: sonnet
generator_critic_loop:
  max_iterations: 3  # M-002 circuit breaker
  improvement_threshold: 0.2
  escalation_on_failure: ps-orchestrator
```

#### WI-SAO-008: Create nse-qa Agent
- **Status:** OPEN
- **Priority:** MEDIUM (P2)
- **Effort:** 16h
- **Source:** Agent Design Specs (NSE-QA-001)

| Task ID | Description | Effort | Status |
|---------|-------------|--------|--------|
| T-008.1 | Create nse-qa.md agent file | 4h | OPEN |
| T-008.2 | Implement NPR 7123.1D verification methods | 4h | OPEN |
| T-008.3 | Add acceptance testing patterns | 4h | OPEN |
| T-008.4 | Create BDD tests for QA workflows | 2h | OPEN |
| T-008.5 | Update ORCHESTRATION.md with QA patterns | 2h | OPEN |

---

### 2.3 Phase 3: Template Unification (32h Total)

#### WI-SAO-009: Create Unified Agent Template (Superset Schema)
- **Status:** OPEN
- **Priority:** HIGH (P1)
- **Effort:** 16h
- **Source:** Trade Study TS-1

| Task ID | Description | Effort | Status |
|---------|-------------|--------|--------|
| T-009.1 | Merge PS_AGENT_TEMPLATE and NSE_AGENT_TEMPLATE | 4h | OPEN |
| T-009.2 | Add parallel execution fields | 4h | OPEN |
| T-009.3 | Add generator-critic fields | 4h | OPEN |
| T-009.4 | Document migration guide | 2h | OPEN |
| T-009.5 | Create template validation checklist | 2h | OPEN |

**Unified Template Extensions (from arch-blueprints.md):**
```yaml
# NEW: Parallel execution support
parallel:
  supports_isolation: boolean
  output_namespace: string
  aggregation_role: enum [none, producer, aggregator]

# NEW: Generator-Critic support
quality_loop:
  role: enum [generator, critic, none]
  scoring_rubric: array
  accepts_feedback: boolean

# NEW: Checkpointing support
checkpoint:
  triggers: array ["on_complete", "on_error"]
  include_artifacts: boolean
  max_size_kb: integer
```

#### WI-SAO-010: Migrate ps-* Agents to Unified Template
- **Status:** OPEN
- **Priority:** HIGH (P1)
- **Effort:** 8h
- **Depends On:** WI-SAO-009

| Task ID | Description | Effort | Status |
|---------|-------------|--------|--------|
| T-010.1 | Migrate ps-researcher.md | 1h | OPEN |
| T-010.2 | Migrate ps-analyst.md | 1h | OPEN |
| T-010.3 | Migrate ps-architect.md | 1h | OPEN |
| T-010.4 | Migrate ps-investigator.md | 1h | OPEN |
| T-010.5 | Migrate ps-reporter.md | 1h | OPEN |
| T-010.6 | Migrate ps-reviewer.md | 1h | OPEN |
| T-010.7 | Migrate ps-synthesizer.md | 1h | OPEN |
| T-010.8 | Migrate ps-validator.md | 1h | OPEN |

#### WI-SAO-011: Migrate nse-* Agents to Unified Template
- **Status:** OPEN
- **Priority:** HIGH (P1)
- **Effort:** 8h
- **Depends On:** WI-SAO-009

| Task ID | Description | Effort | Status |
|---------|-------------|--------|--------|
| T-011.1 | Migrate nse-requirements.md | 1h | OPEN |
| T-011.2 | Migrate nse-risk.md | 1h | OPEN |
| T-011.3 | Migrate nse-architecture.md | 1h | OPEN |
| T-011.4 | Migrate nse-reviewer.md | 1h | OPEN |
| T-011.5 | Migrate nse-verification.md | 1h | OPEN |
| T-011.6 | Migrate nse-integration.md | 1h | OPEN |
| T-011.7 | Migrate nse-configuration.md | 1h | OPEN |
| T-011.8 | Migrate nse-reporter.md | 1h | OPEN |

---

### 2.4 Phase 4: Infrastructure (104h Total)

#### WI-SAO-012: Implement Parallel Execution Support
- **Status:** OPEN
- **Priority:** HIGH (P1) - RED Risk Mitigation
- **Effort:** 24h
- **Source:** Architecture Blueprints (ps-d-003)
- **Risk Mitigated:** MIT-SAO-001 (R-IMP-001)

| Task ID | Description | Effort | Status |
|---------|-------------|--------|--------|
| T-012.1 | Implement context isolation (copy-on-spawn) | 6h | OPEN |
| T-012.2 | Implement parallel router with max 5 concurrency | 4h | OPEN |
| T-012.3 | Implement barrier synchronization | 4h | OPEN |
| T-012.4 | Implement fan-out/fan-in aggregation | 4h | OPEN |
| T-012.5 | Create parallel execution ORCHESTRATION patterns | 3h | OPEN |
| T-012.6 | Create BDD tests for parallel workflows | 3h | OPEN |

**Implementation Specification (MIT-SAO-001):**
```yaml
parallel_execution:
  isolation_mode: "full"        # copy-on-spawn
  shared_state: "none"          # no mutable sharing
  aggregation: "message_queue"  # immutable messages
  timeout_ms: 30000
  max_concurrent_agents: 5      # per TS-4 recommendation
```

**Constraint:** GAP-B3-001 notes that nse-* formal requirements specify max 10 concurrent agents, but ps-* design specifies max 5. Resolution: Start with 5, validate, then consider increase.

#### WI-SAO-013: Implement State Checkpointing
- **Status:** OPEN
- **Priority:** HIGH (P1)
- **Effort:** 24h
- **Source:** Architecture Blueprints (ps-d-003)

| Task ID | Description | Effort | Status |
|---------|-------------|--------|--------|
| T-013.1 | Implement checkpoint schema | 4h | OPEN |
| T-013.2 | Implement write-ahead logging (WAL) | 8h | OPEN |
| T-013.3 | Add retention policy and cleanup | 4h | OPEN |
| T-013.4 | Create checkpoint restore protocol | 4h | OPEN |
| T-013.5 | Add checkpointing to ORCHESTRATION.md | 2h | OPEN |
| T-013.6 | Create BDD tests for checkpointing | 2h | OPEN |

**Checkpoint Lifecycle:**
```
CREATE --> ACTIVE (age < 1h) --> ARCHIVED (age < 24h) --> DELETED (age > 24h)
           (instant restore)    (decompress restore)     (gone)
```

#### WI-SAO-014: Implement Generator-Critic Loops
- **Status:** OPEN
- **Priority:** HIGH (P1) - RED Risk Mitigation
- **Effort:** 8h
- **Source:** Architecture Blueprints (ps-d-003)
- **Risk Mitigated:** MIT-SAO-002 (R-IMP-003)
- **Depends On:** WI-SAO-007 (ps-critic)

| Task ID | Description | Effort | Status |
|---------|-------------|--------|--------|
| T-014.1 | Implement iteration loop control | 2h | OPEN |
| T-014.2 | Implement scoring infrastructure | 2h | OPEN |
| T-014.3 | Implement improvement threshold detection | 1h | OPEN |
| T-014.4 | Add circuit breaker logic | 2h | OPEN |
| T-014.5 | Create BDD tests for quality loops | 1h | OPEN |

**Circuit Breaker Specification (MIT-SAO-002):**
```yaml
generator_critic:
  max_iterations: 3
  quality_threshold: 0.8
  improvement_threshold: 0.05  # 5% minimum improvement to continue
  termination_conditions:
    - score >= 0.8 (quality threshold met)
    - iteration >= 3 (max iterations reached)
    - improvement < 0.05 (diminishing returns)
```

#### WI-SAO-015: Add Guardrail Validation Hooks
- **Status:** OPEN
- **Priority:** MEDIUM (P2)
- **Effort:** 16h

| Task ID | Description | Effort | Status |
|---------|-------------|--------|--------|
| T-015.1 | Define guardrail interface contract | 4h | OPEN |
| T-015.2 | Implement pre-execution validation | 4h | OPEN |
| T-015.3 | Implement post-execution validation | 4h | OPEN |
| T-015.4 | Add hooks to agent templates | 2h | OPEN |
| T-015.5 | Create BDD tests for guardrails | 2h | OPEN |

#### WI-SAO-021: Orchestration Folder Refactoring
- **Status:** OPEN
- **Priority:** HIGH (P1)
- **Effort:** 32h
- **Depends On:** WI-SAO-012, WI-SAO-013

| Task ID | Description | Effort | Status |
|---------|-------------|--------|--------|
| T-021.1 | Consolidate orchestration skill structure | 8h | OPEN |
| T-021.2 | Migrate agents to new locations | 8h | OPEN |
| T-021.3 | Update all cross-references | 8h | OPEN |
| T-021.4 | Validate with E2E tests | 4h | OPEN |
| T-021.5 | Update documentation | 4h | OPEN |

---

### 2.5 Phase 5: Technical Debt (62h Total)

#### WI-SAO-016: Define Skill Interface Contracts
- **Status:** OPEN
- **Priority:** HIGH (P1)
- **Effort:** 16h
- **Risk Mitigated:** MIT-SAO-003 (R-TECH-001) - partial

| Task ID | Description | Effort | Status |
|---------|-------------|--------|--------|
| T-016.1 | Define ps-skill interface contract | 4h | OPEN |
| T-016.2 | Define nse-skill interface contract | 4h | OPEN |
| T-016.3 | Define cross-skill handoff contract | 4h | OPEN |
| T-016.4 | Document contract testing approach | 4h | OPEN |

#### WI-SAO-017: Centralize Tool Registry
- **Status:** OPEN
- **Priority:** HIGH (P1)
- **Effort:** 16h

| Task ID | Description | Effort | Status |
|---------|-------------|--------|--------|
| T-017.1 | Create unified tool registry file | 4h | OPEN |
| T-017.2 | Add capability-based tool assignment | 4h | OPEN |
| T-017.3 | Implement conflict detection | 4h | OPEN |
| T-017.4 | Update agent templates to reference registry | 4h | OPEN |

**Tool Matrix (from Agent Design Specs):**
| Tool | ps-orchestrator | ps-critic | nse-orchestrator | nse-explorer | nse-qa |
|------|-----------------|-----------|------------------|--------------|--------|
| Task | YES | NO | YES | NO | NO |
| Read | YES | YES | YES | YES | YES |
| Write | YES | YES | YES | YES | YES |
| Glob | YES | YES | YES | YES | YES |
| Grep | YES | YES | YES | YES | YES |
| Bash | YES | NO | YES | NO | NO |
| WebSearch | NO | NO | NO | YES | NO |
| WebFetch | NO | NO | NO | YES | NO |

#### WI-SAO-018: Add Schema Versioning
- **Status:** OPEN
- **Priority:** MEDIUM (P2)
- **Effort:** 30h

| Task ID | Description | Effort | Status |
|---------|-------------|--------|--------|
| T-018.1 | Define versioning strategy (semver) | 4h | OPEN |
| T-018.2 | Implement backward compatibility checks | 8h | OPEN |
| T-018.3 | Create migration utilities | 8h | OPEN |
| T-018.4 | Add version negotiation protocol | 6h | OPEN |
| T-018.5 | Document versioning policy | 4h | OPEN |

**Versioning Strategy (from Schema Contracts):**
| Version | Breaking Change? | Description |
|---------|------------------|-------------|
| 1.0.0 | N/A | Initial release |
| 1.1.0 | No | Add `payload_schema_ref` field |
| 1.2.0 | No | Add `workflow_state` for cross-pollination |
| 2.0.0 | Yes | Reserved for major restructure |

---

## Cross-Pollination Metadata

### Source Artifacts

| Artifact | Path | Key Inputs |
|----------|------|------------|
| Agent Design Specs | `ps-pipeline/phase-3-design/agent-design-specs.md` | 5 new agents, specifications |
| Schema Contracts | `ps-pipeline/phase-3-design/schema-contracts.md` | JSON schemas, versioning |
| Architecture Blueprints | `ps-pipeline/phase-3-design/arch-blueprints.md` | Parallel, checkpointing, gen-critic |
| Formal Artifacts | `cross-pollination/barrier-3/nse-to-ps/formal-artifacts.md` | 184h effort, mitigations |

### Handoff Checklist

- [x] L0 executive summary complete
- [x] L1 detailed roadmap with dependencies
- [x] L2 task-level breakdown with effort estimates
- [x] Gantt-style timeline visualization
- [x] Risk-prioritized implementation order
- [x] Phase dependencies visualization
- [x] Integration with existing WORKTRACKER.md work items
- [ ] Reviewed by nse-qa
- [ ] Approved by orchestrator

### Gap Resolutions for This Document

| Gap ID | Description | Resolution |
|--------|-------------|------------|
| GAP-B3-001 | Concurrent agents: nse-* says 10, ps-* says 5 | Start with 5 (conservative), validate, increase if needed |
| GAP-B3-002 | Verification execution plan not linked to sprints | Mapped verification weeks to implementation sprints |
| GAP-B3-003 | Cross-pollination workflow state schema not in VCRM | Included in WI-SAO-002 schema validation scope |

---

## References

- **PS-D-001-AGENT-SPECS:** Agent Design Specifications
- **ps-d-002:** JSON Schema Contracts
- **ps-d-003:** Architecture Blueprints
- **MIT-SAO-MASTER:** Formal Risk Mitigation Plans
- **NSE-REQ-FORMAL-001:** Formal Requirements (52 requirements)
- **NSE-VER-003:** Verification Cross-Reference Matrix (85 VPs)

---

*Implementation Roadmap: PS-S-001-IMPL-ROADMAP*
*Generated by: ps-s-002 (Phase 4 Synthesis)*
*Date: 2026-01-10*
*Workflow: WF-SAO-CROSSPOLL-001*
*Classification: SYNTHESIS COMPLETE*
