# PS-* Orchestration Test Plan

> **Document ID:** TEST-PLAN-PS-ORCH-001
> **Version:** 1.0
> **Date:** 2026-01-11
> **Author:** Claude Code (Orchestrator)
> **Status:** APPROVED
> **Source:** Gap Analysis WI-SAO-029-E-002-GAP

---

## L0: Executive Summary (ELI5)

This test plan defines 12 orchestration tests for ps-* agents to achieve parity with the existing nse-* test coverage. The gap analysis revealed that ps-* agents have 0% orchestration test coverage despite having the same architectural patterns as the fully-tested nse-* agents.

**Why this matters:** Testing individual agents is like testing car parts - it doesn't tell you if the car drives. Orchestration tests verify that agents work together correctly in multi-agent workflows.

**Goal:** Execute all 12 tests and achieve 100% PASS rate for ps-* orchestration.

---

## L1: Test Strategy (Software Engineer)

### 1. Test Categories

| Category | Tests | Priority | Pattern Coverage |
|----------|-------|----------|------------------|
| CRITICAL | PS-ORCH-001 to 004 | P0 | Sequential, Fan-In, Generator-Critic, Review Gate |
| HIGH | PS-ORCH-005 to 006, CROSS-ORCH-001 to 002 | P1 | Fan-Out, Validation Chain, Cross-Family |
| MEDIUM | PS-ORCH-007 to 008, PS-NEG-001 to 002 | P2 | Incident, Bootstrap, Error Handling |

### 2. Test Environment

```yaml
environment:
  framework: Jerry v1.0
  claude_code: Task tool with subagent_type="general-purpose"
  context_size: 200K tokens (isolated per agent)
  max_parallel_agents: 10
  session_context_schema: v1.0.0

constraints:
  P-003: Maximum 1 level nesting (MAIN CONTEXT → worker)
  P-002: All outputs persisted to filesystem
  P-022: No deception about capabilities or confidence
```

### 3. Test Artifacts Location

```
projects/PROJ-002-nasa-systems-engineering/tests/ps-orchestration-results/
├── PS-ORCH-001-results.md     # Sequential Research-Analysis
├── PS-ORCH-002-results.md     # Fan-In Synthesis
├── PS-ORCH-003-results.md     # Generator-Critic Loop
├── PS-ORCH-004-results.md     # Review Gate
├── PS-ORCH-005-results.md     # Fan-Out Investigation
├── PS-ORCH-006-results.md     # Validation Chain
├── PS-ORCH-007-results.md     # Incident Investigation
├── PS-ORCH-008-results.md     # Knowledge Bootstrap
├── CROSS-ORCH-001-results.md  # Cross-Family Handoff
├── CROSS-ORCH-002-results.md  # Mixed Fan-In
├── PS-NEG-001-results.md      # Missing Dependency (error handling)
├── PS-NEG-002-results.md      # Invalid Schema (error handling)
└── SUMMARY.md                  # Aggregate results
```

---

## L2: Test Specifications (Principal Architect)

### CRITICAL Tests (Must Pass for Production)

#### PS-ORCH-001: Sequential Research-Analysis

```yaml
test_id: PS-ORCH-001
name: Sequential Research-Analysis
priority: CRITICAL
pattern: Sequential Chain
estimated_duration: 4h

agents:
  - role: producer
    agent: ps-researcher
    input: Test problem statement
    output: research/{ps-id}-{entry-id}-research.md

  - role: consumer
    agent: ps-analyst
    input: session_context with ps-researcher output
    output: analysis/{ps-id}-{entry-id}-analysis.md

session_context_validation:
  on_handoff:
    - session_context.key_findings populated by ps-researcher
    - session_context.input_artifacts contains research path
    - Schema validation passes (v1.0.0)

success_criteria:
  - Both agents complete without error
  - Both artifacts exist and are >100 lines
  - ps-analyst references ps-researcher findings
  - No schema validation errors

failure_modes:
  - F1: ps-researcher fails to create artifact → FAIL
  - F2: session_context malformed → FAIL
  - F3: ps-analyst ignores input → FAIL
```

#### PS-ORCH-002: Fan-In Synthesis

```yaml
test_id: PS-ORCH-002
name: Fan-In Synthesis
priority: CRITICAL
pattern: Fan-In Aggregation
estimated_duration: 6h

agents:
  - role: producer-1
    agent: ps-researcher
    execution: parallel
    output: research/{ps-id}-{entry-id}-research.md

  - role: producer-2
    agent: ps-analyst
    execution: parallel
    output: analysis/{ps-id}-{entry-id}-analysis.md

  - role: producer-3
    agent: ps-architect
    execution: parallel
    output: designs/{ps-id}-{entry-id}-design.md

  - role: aggregator
    agent: ps-synthesizer
    input: session_context with 3 input_artifacts
    output: synthesis/{ps-id}-{entry-id}-synthesis.md

session_context_validation:
  on_aggregation:
    - session_context.input_artifacts.length == 3
    - All 3 artifacts exist
    - Each artifact has distinct perspective

success_criteria:
  - All 3 parallel agents complete successfully
  - ps-synthesizer correctly aggregates all perspectives
  - Final synthesis references all 3 source materials
  - Parallel execution verified (overlapping timestamps)

failure_modes:
  - F1: Any parallel agent fails → PARTIAL (retry)
  - F2: Aggregation misses input → FAIL
  - F3: Synthesis lacks traceability → FAIL
```

#### PS-ORCH-003: Generator-Critic Loop

```yaml
test_id: PS-ORCH-003
name: Generator-Critic Loop
priority: CRITICAL
pattern: Iterative Refinement
estimated_duration: 8h

agents:
  - role: generator
    agent: ps-architect
    iterations: 1-3
    output: designs/{ps-id}-{entry-id}-iter{n}-design.md

  - role: critic
    agent: ps-critic
    iterations: 1-3
    output: critiques/{ps-id}-{entry-id}-iter{n}-critique.md

loop_control:
  managed_by: MAIN CONTEXT (P-003 compliant)
  quality_threshold: 0.85
  max_iterations: 3
  improvement_target: 0.10 per iteration

session_context_validation:
  per_iteration:
    - ps-critic returns quality_score (0.0-1.0)
    - ps-critic provides actionable_improvements[]
    - ps-architect receives feedback via session_context

success_criteria:
  - Loop terminates (quality >= 0.85 OR iterations == 3)
  - Each iteration shows quality_score
  - Quality improves across iterations
  - Circuit breaker enforced by MAIN CONTEXT

failure_modes:
  - F1: Infinite loop (no termination) → CRITICAL FAIL
  - F2: Quality doesn't improve → WARNING (acceptable if terminates)
  - F3: ps-critic provides no feedback → FAIL
```

#### PS-ORCH-004: Review Gate

```yaml
test_id: PS-ORCH-004
name: Review Gate
priority: CRITICAL
pattern: Review Gate
estimated_duration: 6h

agents:
  - role: reviewable
    agent: any ps-* (output from PS-ORCH-001 or PS-ORCH-002)

  - role: reviewer
    agent: ps-reviewer
    input: Review package session_context
    output: reviews/{ps-id}-{entry-id}-review.md

session_context_validation:
  on_review:
    - session_context.input_artifacts contains reviewable content
    - Review scope defined

success_criteria:
  - ps-reviewer generates structured review report
  - Findings categorized by severity (CRITICAL, HIGH, MEDIUM, LOW)
  - Constitutional compliance checked (P-001, P-002, P-022)
  - Go/No-Go recommendation provided

failure_modes:
  - F1: Review report missing severity levels → FAIL
  - F2: No Go/No-Go recommendation → FAIL
```

### HIGH Priority Tests

#### PS-ORCH-005: Fan-Out Investigation

```yaml
test_id: PS-ORCH-005
name: Fan-Out Investigation
priority: HIGH
pattern: Fan-Out Parallel
estimated_duration: 6h

agents:
  - agent: ps-investigator
    focus: incident analysis
    execution: parallel

  - agent: ps-analyst
    focus: pattern analysis
    execution: parallel

  - agent: ps-researcher
    focus: background research
    execution: parallel

success_criteria:
  - All 3 agents execute in parallel (verified by timestamps)
  - Each provides unique perspective on same problem
  - No cross-contamination between parallel contexts
```

#### PS-ORCH-006: Validation Chain

```yaml
test_id: PS-ORCH-006
name: Validation Chain
priority: HIGH
pattern: Sequential Validation
estimated_duration: 6h

agents:
  - agent: ps-architect
    role: create design

  - agent: ps-validator
    role: validate design

  - agent: ps-reporter
    role: generate validation report

success_criteria:
  - Chain completes sequentially
  - Each handoff maintains traceability
  - Validation findings propagate to report
```

#### CROSS-ORCH-001: Cross-Family Handoff

```yaml
test_id: CROSS-ORCH-001
name: Cross-Family Handoff
priority: HIGH
pattern: Sequential Cross-Family
estimated_duration: 4h

agents:
  - agent: ps-researcher
    family: ps-*
    output: Research on NASA SE topic

  - agent: nse-requirements
    family: nse-*
    input: ps-researcher output

success_criteria:
  - ps-* to nse-* handoff succeeds
  - Schema compatible across families
  - nse-requirements successfully consumes ps-* output
```

#### CROSS-ORCH-002: Mixed Fan-In

```yaml
test_id: CROSS-ORCH-002
name: Mixed Fan-In
priority: HIGH
pattern: Fan-In Mixed Family
estimated_duration: 4h

agents:
  - agent: ps-analyst
    family: ps-*
    execution: parallel

  - agent: nse-risk
    family: nse-*
    execution: parallel

  - agent: ps-reporter
    family: ps-*
    role: aggregator

success_criteria:
  - Mixed family aggregation succeeds
  - ps-reporter correctly references both families
  - No schema incompatibilities
```

### MEDIUM Priority Tests

#### PS-ORCH-007: Incident Investigation

```yaml
test_id: PS-ORCH-007
name: Incident Investigation
priority: MEDIUM
pattern: Sequential
agents: ps-investigator → ps-analyst → ps-reporter
```

#### PS-ORCH-008: Knowledge Bootstrap

```yaml
test_id: PS-ORCH-008
name: Knowledge Bootstrap
priority: MEDIUM
pattern: Mixed
agents: ps-researcher → ps-synthesizer → ps-architect
```

#### PS-NEG-001: Missing Dependency (Error Handling)

```yaml
test_id: PS-NEG-001
name: Missing Dependency
priority: MEDIUM
pattern: Error Handling

test_scenario:
  action: Invoke ps-validator with empty session_context
  expected: Graceful error with clear message

success_criteria:
  - Error caught before execution
  - Clear error message returned
  - No orphaned processes
```

#### PS-NEG-002: Invalid Schema (Error Handling)

```yaml
test_id: PS-NEG-002
name: Invalid Schema
priority: MEDIUM
pattern: Error Handling

test_scenario:
  action: Invoke any ps-* with malformed session_context
  expected: Schema validation catches error

success_criteria:
  - Schema validation rejects invalid input
  - Error message identifies violation
  - Agent does not proceed with invalid context
```

---

## Test Execution Checklist

### Pre-Execution

- [ ] Verify all 9 ps-* agents at v2.1.0 with conformance PASS
- [ ] Verify session_context schema v1.0.0 available
- [ ] Create `tests/ps-orchestration-results/` directory
- [ ] Review test problem statements for appropriateness

### Execution Order

1. **CRITICAL (Sequential)**
   - [ ] PS-ORCH-001 (establishes baseline)
   - [ ] PS-ORCH-004 (uses PS-ORCH-001 output)
   - [ ] PS-ORCH-002 (Fan-In, more complex)
   - [ ] PS-ORCH-003 (Generator-Critic, most complex)

2. **HIGH (Can parallelize some)**
   - [ ] PS-ORCH-005 (Fan-Out)
   - [ ] PS-ORCH-006 (Validation Chain)
   - [ ] CROSS-ORCH-001 (Cross-Family)
   - [ ] CROSS-ORCH-002 (Mixed Fan-In)

3. **MEDIUM (Lower priority)**
   - [ ] PS-ORCH-007 (Incident)
   - [ ] PS-ORCH-008 (Bootstrap)
   - [ ] PS-NEG-001 (Error: Missing Dep)
   - [ ] PS-NEG-002 (Error: Invalid Schema)

### Post-Execution

- [ ] All test result files created in `ps-orchestration-results/`
- [ ] SUMMARY.md generated with aggregate results
- [ ] WORKTRACKER.md updated with completion status
- [ ] Any failures documented with root cause analysis

---

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| Agent timeout | Set reasonable timeout; retry once on timeout |
| Context exhaustion | Monitor context usage; summarize if needed |
| Infinite loop (PS-ORCH-003) | Circuit breaker enforced by MAIN CONTEXT (max 3 iterations) |
| Schema mismatch | Validate schema compliance on every handoff |
| Parallel agent failure | Use `run_in_background: true`; handle individual failures |

---

## Evidence Requirements

Each test MUST produce:

1. **Test Result Document** (`PS-ORCH-XXX-results.md`)
   - Test ID, Date, Duration
   - Pass/Fail status with evidence
   - Artifacts produced (with line counts)
   - Session context validation results
   - Any issues encountered

2. **Agent Artifacts** (in appropriate directories)
   - Research: `research/{ps-id}-{entry-id}-*.md`
   - Analysis: `analysis/{ps-id}-{entry-id}-*.md`
   - Designs: `designs/{ps-id}-{entry-id}-*.md`
   - Synthesis: `synthesis/{ps-id}-{entry-id}-*.md`
   - Critiques: `critiques/{ps-id}-{entry-id}-*.md`
   - Reviews: `reviews/{ps-id}-{entry-id}-*.md`

---

## Traceability

| Source | This Document | Worktracker |
|--------|---------------|-------------|
| Gap Analysis E-002 | Test specifications | WI-SAO-029 |
| ORCH-001 (nse-*) | PS-ORCH-001 | T-029.1 |
| ORCH-003 (nse-*) | PS-ORCH-002 | T-029.2 |
| (new pattern) | PS-ORCH-003 | T-029.3 |
| ORCH-004 (nse-*) | PS-ORCH-004 | T-029.4 |

---

## Approval

| Role | Name | Date | Signature |
|------|------|------|-----------|
| Test Author | Claude Code (Orchestrator) | 2026-01-11 | AUTO |
| Technical Review | PENDING | - | - |
| User Approval | PENDING | - | - |

---

*DISCLAIMER: This test plan is AI-generated based on gap analysis and existing nse-* test patterns. All test specifications require human review before execution.*

*Generated by Claude Code (Orchestrator)*
*Date: 2026-01-11*
*Constitutional Compliance: P-001 (Accuracy), P-002 (Persistence), P-022 (No Deception)*
