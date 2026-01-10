# Orchestration Testing Strategy: NASA SE Skill

> **Document ID:** TEST-NSE-ORCH-001
> **Version:** 1.0
> **Date:** 2026-01-09
> **Status:** IN PROGRESS
> **Author:** Claude Code

---

## L0: Executive Summary (ELI5)

**What is orchestration?**
Think of the 8 NASA SE agents as specialists in a hospital. The orchestration is like the patient flow system that decides: "First see the nurse (nse-requirements), then the specialist (nse-verification), then the pharmacist (nse-risk)." Without orchestration, patients would wander around confused.

**Why test it?**
We need to prove that when you ask "prepare for CDR", the right specialists get involved in the right order, share information correctly, and don't step on each other's toes.

**What are we testing?**
- Do agents run in the right order?
- Do they pass information correctly?
- What happens when something goes wrong?
- Do all 4 workflow "recipes" work end-to-end?

**Success means:** You can confidently say "prepare for CDR" and get a complete, correct result every time.

---

## L1: Technical Test Plan (Software Engineer Level)

### 1.1 Test Scope

**In Scope:**
| Category | Items | Test Count |
|----------|-------|------------|
| Patterns | Sequential, Fan-Out, Fan-In, Review Gate | 4 |
| Workflows | CDR Prep, Change Impact, Risk Escalation, Bootstrap | 4 |
| State Handoff | Agent-to-agent data passing | 8 combinations |
| Error Handling | Timeout, Invalid input, Missing dependency | 3 |
| **Total Test Scenarios** | | **19** |

**Out of Scope:**
- Performance/load testing
- Security testing
- Multi-user concurrency

### 1.2 Test Environment

```yaml
environment:
  framework: Jerry Framework
  skill: nasa-se (8 agents)
  test_project: PROJ-002-nasa-systems-engineering
  state_location: projects/PROJ-002.../tests/orchestration-state/
  output_location: projects/PROJ-002.../tests/orchestration-results/
```

### 1.3 Test Execution Method

Since agents are AI-driven, testing is executed via:
1. **Simulated invocation** - Describe the scenario, execute, observe
2. **State inspection** - Check state files produced
3. **Output validation** - Verify artifacts match expected format
4. **Compatibility recording** - Document actual vs expected behavior

### 1.4 Test Case Template

```markdown
### TEST-ORCH-XXX: {Test Name}

**Pattern/Workflow:** {which pattern or workflow}
**Type:** Happy Path / Negative / Edge Case

**Preconditions:**
- {required state before test}

**Steps:**
1. {step 1}
2. {step 2}
...

**Expected Results:**
- {what should happen}

**Actual Results:**
- {filled in during execution}

**Status:** ⬜ Not Run | ✅ Pass | ❌ Fail | ⚠️ Partial

**Issues Found:**
- {any issues discovered}
```

---

## L2: Systems Architecture Testing (Principal Architect Level)

### 2.1 Orchestration Architecture Overview

```
                    User Request
                         │
                         ▼
              ┌─────────────────────┐
              │   SKILL.md Router   │
              │  (Pattern Selection)│
              └──────────┬──────────┘
                         │
         ┌───────────────┼───────────────┐
         ▼               ▼               ▼
    ┌─────────┐    ┌─────────┐    ┌─────────┐
    │Sequential│    │ Fan-Out │    │Fan-In   │
    │ Pattern  │    │ Pattern │    │Pattern  │
    └────┬────┘    └────┬────┘    └────┬────┘
         │               │               │
         ▼               ▼               ▼
    ┌─────────────────────────────────────────┐
    │           State Handoff Layer           │
    │  (JSON schema, file-based persistence)  │
    └─────────────────────────────────────────┘
         │               │               │
         ▼               ▼               ▼
    ┌─────────┐    ┌─────────┐    ┌─────────┐
    │ Agent A │    │ Agent B │    │ Agent C │
    └─────────┘    └─────────┘    └─────────┘
```

### 2.2 Critical Validation Points

| Validation Point | Why Critical | How Tested |
|------------------|--------------|------------|
| Agent invocation order | Wrong order = invalid outputs | Sequential pattern tests |
| State schema compliance | Broken schema = failed handoff | Schema validation tests |
| Parallel execution isolation | Race conditions = data corruption | Fan-out tests |
| Aggregation completeness | Missing inputs = incomplete reports | Fan-in tests |
| Gate decision accuracy | Wrong gate = premature/delayed reviews | Review gate tests |
| Error propagation | Silent failures = hidden problems | Negative path tests |

### 2.3 Compatibility Matrix Structure

The compatibility matrix will answer:
- Does Agent A → Agent B handoff work?
- Does Pattern X with Agents Y and Z work?
- Does Workflow W complete successfully?

```
Matrix Dimensions:
- Rows: Source agents (or patterns/workflows)
- Columns: Target agents (or outcomes)
- Cells: ✅ Compatible | ⚠️ Partial | ❌ Incompatible | ⬜ Not Tested
```

### 2.4 Risk Areas Requiring Extra Scrutiny

| Risk Area | Concern | Test Focus |
|-----------|---------|------------|
| State loss between agents | Context not preserved | Verify state files exist and are readable |
| Parallel agent interference | Overwriting shared state | Verify isolation in fan-out |
| Missing input tolerance | Does agent fail gracefully? | Test with missing preconditions |
| Cyclic dependencies | Infinite loops | Verify DAG structure enforced |
| P-003 violation | Recursive agent spawning | Verify no agent spawns sub-agents |

---

## 3. Test Suites

### 3.1 Pattern Tests (4 tests)

#### TEST-ORCH-001: Sequential Chain Pattern

**Pattern:** Sequential
**Type:** Happy Path

**Preconditions:**
- Project PROJ-002 exists
- No existing test artifacts

**Scenario:**
```
User: "Create a requirements spec, then create VCRM for it, then assess risks"
Expected Flow: nse-requirements → nse-verification → nse-risk
```

**Steps:**
1. Invoke nse-requirements to create requirements
2. Verify requirements artifact exists
3. Invoke nse-verification with requirements as input
4. Verify VCRM artifact exists and references requirements
5. Invoke nse-risk with both artifacts as input
6. Verify risk register exists and references both inputs

**Expected Results:**
- 3 artifacts created in correct sequence
- Each artifact references previous artifacts
- State handoff completes between each agent

**Actual Results:** ⬜ Pending

**Status:** ⬜ Not Run

---

#### TEST-ORCH-002: Fan-Out Parallel Pattern

**Pattern:** Fan-Out
**Type:** Happy Path

**Preconditions:**
- Requirements baseline exists (REQ-NSE-SKILL-001.md)

**Scenario:**
```
Trigger: Requirements baseline approved
Expected Flow: Parallel execution of nse-verification, nse-architecture, nse-risk
```

**Steps:**
1. Use existing REQ-NSE-SKILL-001.md as baseline
2. Invoke fan-out pattern with 3 agents in parallel
3. Verify each agent produces output independently
4. Verify no interference between outputs
5. Verify all outputs reference same input requirements

**Expected Results:**
- 3 artifacts created
- Artifacts are independent (no state collision)
- All reference same requirements baseline

**Actual Results:** ⬜ Pending

**Status:** ⬜ Not Run

---

#### TEST-ORCH-003: Fan-In Aggregation Pattern

**Pattern:** Fan-In
**Type:** Happy Path

**Preconditions:**
- Outputs exist from: nse-requirements, nse-verification, nse-risk, nse-integration, nse-configuration

**Scenario:**
```
Aggregator: nse-reporter
Expected Flow: Read from 5+ sources, produce consolidated status report
```

**Steps:**
1. Verify all source artifacts exist (from dog-fooding)
2. Invoke nse-reporter to aggregate
3. Verify status report includes data from all sources
4. Verify no source is omitted
5. Verify metrics are calculated correctly

**Expected Results:**
- Single consolidated status report
- All 6 domains represented
- Metrics match source data

**Actual Results:** ⬜ Pending

**Status:** ⬜ Not Run

---

#### TEST-ORCH-004: Review Gate Pattern

**Pattern:** Review Gate
**Type:** Happy Path

**Preconditions:**
- Artifacts exist for a review (requirements, design, verification, risks)

**Scenario:**
```
Gate: CDR readiness assessment
Expected Flow: nse-reviewer assesses entrance criteria, returns READY/NOT READY
```

**Steps:**
1. Gather all artifacts for CDR entrance criteria
2. Invoke nse-reviewer with gate type = CDR
3. Verify entrance criteria checklist is evaluated
4. Verify recommendation is produced
5. If NOT READY, verify remediation actions listed

**Expected Results:**
- Entrance criteria evaluated (10 criteria)
- Clear READY / NOT READY / CONDITIONALLY READY verdict
- If not ready, specific gaps identified

**Actual Results:** ⬜ Pending

**Status:** ⬜ Not Run

---

### 3.2 Workflow Tests (4 tests)

#### TEST-ORCH-005: CDR Preparation Workflow

**Workflow:** CDR Preparation
**Type:** End-to-End Happy Path

**Preconditions:**
- Project with existing requirements baseline

**Scenario:**
```
User: "Help me prepare for CDR"
Expected: 4-phase workflow executes completely
```

**Steps:**
1. Phase 1: Baseline check (nse-requirements, nse-configuration)
2. Phase 2: Parallel artifact generation (4 agents)
3. Phase 3: Readiness assessment (nse-reviewer)
4. Phase 4: Status package (nse-reporter)

**Expected Results:**
- All 4 phases complete
- User checkpoint presented at end
- CDR package artifacts generated

**Actual Results:** ⬜ Pending

**Status:** ⬜ Not Run

---

#### TEST-ORCH-006: Requirements Change Impact Workflow

**Workflow:** Change Impact Assessment
**Type:** End-to-End Happy Path

**Preconditions:**
- Existing requirements baseline
- Specific requirement to change (e.g., REQ-NSE-FUN-001)

**Scenario:**
```
User: "What's the impact if we change REQ-NSE-FUN-001?"
Expected: Parallel impact assessment across 5 domains
```

**Steps:**
1. nse-requirements traces dependencies
2. Parallel: verification, architecture, integration, risk assess impact
3. nse-configuration prepares change request summary
4. User presented with impact summary

**Expected Results:**
- Impact assessed across all domains
- Affected artifacts identified
- Change request package prepared

**Actual Results:** ⬜ Pending

**Status:** ⬜ Not Run

---

#### TEST-ORCH-007: Risk Escalation Workflow

**Workflow:** Risk Escalation
**Type:** End-to-End Happy Path

**Preconditions:**
- Risk register with at least one RED risk (R-001 qualifies)

**Scenario:**
```
Trigger: Risk score >= 16 detected
Expected: Immediate escalation workflow
```

**Steps:**
1. nse-risk generates risk brief
2. nse-reporter generates executive alert
3. User notification generated
4. Follow-up: architecture and verification assess alternatives

**Expected Results:**
- Risk brief artifact created
- Executive alert created
- User clearly notified of RED risk
- Mitigation options presented

**Actual Results:** ⬜ Pending

**Status:** ⬜ Not Run

---

#### TEST-ORCH-008: Project Bootstrap Workflow

**Workflow:** New Project Bootstrap
**Type:** End-to-End Happy Path

**Preconditions:**
- Fresh project directory (no existing SE artifacts)

**Scenario:**
```
User: "Initialize SE artifacts for a new project"
Expected: Complete set of SE templates created
```

**Steps:**
1. nse-requirements creates requirements template
2. nse-risk creates risk register
3. Parallel: architecture, verification, integration, configuration create templates
4. nse-reporter creates initial status

**Expected Results:**
- 7 template artifacts created
- All agents contribute
- User checkpoint for baseline approval

**Actual Results:** ⬜ Pending

**Status:** ⬜ Not Run

---

### 3.3 State Handoff Tests (8 tests)

#### TEST-ORCH-009: Requirements → Verification Handoff

**Source:** nse-requirements
**Target:** nse-verification

**Steps:**
1. nse-requirements produces output with state
2. Verify state includes `handoff_ready[nse-verification] = true`
3. nse-verification receives requirements artifact path
4. nse-verification produces VCRM referencing requirements

**Expected Results:**
- State schema valid
- Handoff flag set correctly
- Target agent can read source artifacts

**Status:** ⬜ Not Run

---

#### TEST-ORCH-010: Requirements → Risk Handoff

**Source:** nse-requirements
**Target:** nse-risk

**Status:** ⬜ Not Run

---

#### TEST-ORCH-011: Requirements → Architecture Handoff

**Source:** nse-requirements
**Target:** nse-architecture

**Status:** ⬜ Not Run

---

#### TEST-ORCH-012: Architecture → Integration Handoff

**Source:** nse-architecture
**Target:** nse-integration

**Status:** ⬜ Not Run

---

#### TEST-ORCH-013: Integration → Configuration Handoff

**Source:** nse-integration
**Target:** nse-configuration

**Status:** ⬜ Not Run

---

#### TEST-ORCH-014: All Agents → Reporter Handoff

**Source:** All 7 domain agents
**Target:** nse-reporter

**Status:** ⬜ Not Run

---

#### TEST-ORCH-015: All Agents → Reviewer Handoff

**Source:** All 7 domain agents
**Target:** nse-reviewer

**Status:** ⬜ Not Run

---

#### TEST-ORCH-016: Risk → Architecture Handoff (Risk Mitigation)

**Source:** nse-risk (RED risk identified)
**Target:** nse-architecture (design alternatives)

**Status:** ⬜ Not Run

---

### 3.4 Negative Path Tests (3 tests)

#### TEST-ORCH-017: Missing Dependency Handling

**Type:** Negative Path

**Scenario:**
```
Invoke nse-verification without requirements baseline
Expected: Graceful failure with clear error message
```

**Steps:**
1. Attempt to create VCRM with no requirements
2. Verify agent does not crash
3. Verify clear error message produced
4. Verify partial work is preserved (if any)

**Expected Results:**
- Agent handles missing input gracefully
- Clear error: "Requirements baseline not found"
- No corrupted state left behind

**Status:** ⬜ Not Run

---

#### TEST-ORCH-018: Invalid State Schema Handling

**Type:** Negative Path

**Scenario:**
```
Provide malformed state JSON to agent
Expected: Validation error, not crash
```

**Steps:**
1. Create invalid state file
2. Attempt agent invocation that reads state
3. Verify schema validation catches error
4. Verify meaningful error message

**Expected Results:**
- Schema validation works
- Clear error about invalid state
- Agent suggests remediation

**Status:** ⬜ Not Run

---

#### TEST-ORCH-019: Cascade Failure Prevention

**Type:** Negative Path

**Scenario:**
```
One agent in a fan-out fails
Expected: Other agents complete, failure isolated
```

**Steps:**
1. Execute fan-out with 3 agents
2. Simulate failure in one agent
3. Verify other 2 agents complete
4. Verify failure is reported clearly
5. Verify successful outputs preserved

**Expected Results:**
- Failure isolated to one agent
- Other agents complete successfully
- User informed of partial success

**Status:** ⬜ Not Run

---

## 4. Compatibility Matrix Template

### 4.1 Agent-to-Agent Handoff Matrix

|              | →req | →ver | →risk | →arch | →integ | →config | →review | →report |
|--------------|:----:|:----:|:-----:|:-----:|:------:|:-------:|:-------:|:-------:|
| **req→**     | -    | ⬜   | ⬜    | ⬜    | ⬜     | ⬜      | ⬜      | ⬜      |
| **ver→**     | N/A  | -    | ⬜    | N/A   | N/A    | ⬜      | ⬜      | ⬜      |
| **risk→**    | N/A  | ⬜   | -     | ⬜    | N/A    | ⬜      | ⬜      | ⬜      |
| **arch→**    | N/A  | ⬜   | ⬜    | -     | ⬜     | ⬜      | ⬜      | ⬜      |
| **integ→**   | N/A  | ⬜   | ⬜    | N/A   | -      | ⬜      | ⬜      | ⬜      |
| **config→**  | N/A  | N/A  | N/A   | N/A   | N/A    | -       | ⬜      | ⬜      |
| **review→**  | N/A  | N/A  | N/A   | N/A   | N/A    | N/A     | -       | ⬜      |
| **report→**  | N/A  | N/A  | N/A   | N/A   | N/A    | N/A     | N/A     | -       |

**Legend:** ✅ Compatible | ⚠️ Partial | ❌ Incompatible | ⬜ Not Tested | N/A Not Applicable

### 4.2 Pattern Compatibility

| Pattern | req | ver | risk | arch | integ | config | review | report |
|---------|:---:|:---:|:----:|:----:|:-----:|:------:|:------:|:------:|
| Sequential | ⬜ | ⬜ | ⬜  | ⬜   | ⬜    | ⬜     | ⬜     | ⬜     |
| Fan-Out    | ⬜ | ⬜ | ⬜  | ⬜   | ⬜    | ⬜     | ⬜     | ⬜     |
| Fan-In     | ⬜ | ⬜ | ⬜  | ⬜   | ⬜    | ⬜     | ⬜     | ⬜     |
| Review Gate| ⬜ | ⬜ | ⬜  | ⬜   | ⬜    | ⬜     | ⬜     | ⬜     |

### 4.3 Workflow Completion Status

| Workflow | Phase 1 | Phase 2 | Phase 3 | Phase 4 | Overall |
|----------|:-------:|:-------:|:-------:|:-------:|:-------:|
| CDR Prep | ⬜      | ⬜      | ⬜      | ⬜      | ⬜      |
| Change Impact | ⬜ | ⬜     | ⬜      | -       | ⬜      |
| Risk Escalation | ⬜ | ⬜   | ⬜      | -       | ⬜      |
| Bootstrap | ⬜     | ⬜      | ⬜      | -       | ⬜      |

---

## 5. Issue Tracking Template

| Issue ID | Test | Severity | Description | Resolution | Status |
|----------|------|----------|-------------|------------|--------|
| ORCH-ISS-001 | - | - | - | - | - |

**Severity Scale:**
- **Critical:** Blocks orchestration entirely
- **High:** Workflow fails but workaround exists
- **Medium:** Partial failure, degraded output
- **Low:** Cosmetic or documentation issue

---

## 6. Success Criteria

### 6.1 Minimum Viable Orchestration

To declare orchestration "working", ALL must pass:
- [ ] TEST-ORCH-001 (Sequential) - PASS
- [ ] TEST-ORCH-003 (Fan-In) - PASS
- [ ] TEST-ORCH-008 (Bootstrap) - PASS
- [ ] TEST-ORCH-017 (Error handling) - PASS

### 6.2 Full Orchestration Validation

For production release:
- [ ] All 4 pattern tests pass
- [ ] All 4 workflow tests pass
- [ ] At least 6 of 8 handoff tests pass
- [ ] All 3 negative path tests pass
- [ ] Compatibility matrix > 80% green
- [ ] No Critical or High severity issues open

---

## 7. Execution Schedule

| Phase | Tests | Status |
|-------|-------|--------|
| Phase A: Patterns | TEST-ORCH-001 to 004 | ⬜ Pending |
| Phase B: Workflows | TEST-ORCH-005 to 008 | ⬜ Pending |
| Phase C: Handoffs | TEST-ORCH-009 to 016 | ⬜ Pending |
| Phase D: Negative | TEST-ORCH-017 to 019 | ⬜ Pending |
| Phase E: Matrix | Fill compatibility matrix | ⬜ Pending |

---

*DISCLAIMER: This test strategy is AI-generated. All test results require human verification and professional engineering judgment.*
