# Agent Verification Gap Analysis: ps-* and nse-* Families

> **Document ID:** WI-SAO-029-E-002-GAP
> **Version:** 1.0
> **Date:** 2026-01-11
> **Author:** ps-analyst (v2.1.0)
> **Status:** COMPLETE

---

## L0: Executive Summary (ELI5)

We analyzed the gap between existing orchestration test coverage and the new agent requirements for the Jerry framework. Here's what we found:

**The Good News:** All 19 orchestration tests passed on 2026-01-10, covering the 10 nse-* (NASA Systems Engineering) agents across 4 patterns, 4 workflows, 8 handoff scenarios, and 3 error handling tests. The nse-* family is production-ready for orchestration workflows.

**The Gap:** The 9 ps-* (Problem Solving) agents have ZERO orchestration test coverage despite having:
- All agents upgraded to v2.1.0 with conformance PASS
- Full session_context schema implementation (WI-SAO-002)
- Identical architectural patterns to the tested nse-* agents

**The Risk:** Without orchestration tests, we cannot confirm that ps-* agents will behave correctly in multi-agent workflows, despite having individual conformance. This is analogous to testing car components but never driving the assembled car.

**Recommendation:** Execute 12 priority tests for ps-* orchestration before declaring the framework production-ready. Estimated effort: 1-2 days.

---

## L1: Technical Analysis (Software Engineer)

### 1. Existing Test Coverage Analysis

The existing 19 orchestration tests (ORCHESTRATION-TEST-STRATEGY.md) exclusively test nse-* agents:

| Test ID | Pattern/Workflow | Agents Tested | Status |
|---------|------------------|---------------|--------|
| ORCH-001 | Sequential | nse-requirements → nse-verification → nse-risk | PASS |
| ORCH-002 | Fan-Out | nse-verification, nse-architecture, nse-risk | PASS |
| ORCH-003 | Fan-In | All nse-* → nse-reporter | PASS |
| ORCH-004 | Review Gate | All nse-* → nse-reviewer | PASS |
| ORCH-005 | CDR Prep Workflow | 8 nse-* agents | PASS |
| ORCH-006 | Change Impact | nse-requirements + 4 parallel | PASS |
| ORCH-007 | Risk Escalation | nse-risk, nse-reporter, nse-architecture, nse-verification | PASS |
| ORCH-008 | Bootstrap | 7 nse-* agents | PASS |
| ORCH-009-016 | State Handoffs | Various nse-* pairs | PASS (8/8) |
| ORCH-017-019 | Error Handling | Design validation | PASS (3/3) |

**Total nse-* Coverage:** 100% of agents tested in orchestration
**Total ps-* Coverage:** 0% of agents tested in orchestration

### 2. ps-* Agent Inventory Analysis

| Agent | Version | Conformance | Session Context | Orchestration Tested |
|-------|---------|-------------|-----------------|----------------------|
| ps-analyst | 2.1.0 | PASS | Yes (v1.0.0) | **NO** |
| ps-architect | 2.1.0 | PASS | Yes (v1.0.0) | **NO** |
| ps-critic | 2.1.0 | PASS | Yes (v1.0.0) | **NO** |
| ps-investigator | 2.1.0 | PASS | Yes (v1.0.0) | **NO** |
| ps-reporter | 2.1.0 | PASS | Yes (v1.0.0) | **NO** |
| ps-researcher | 2.1.0 | PASS | Yes (v1.0.0) | **NO** |
| ps-reviewer | 2.1.0 | PASS | Yes (v1.0.0) | **NO** |
| ps-synthesizer | 2.1.0 | PASS | Yes (v1.0.0) | **NO** |
| ps-validator | 2.1.0 | PASS | Yes (v1.0.0) | **NO** |

### 3. Session Context Schema Comparison

Both agent families implement the same session_context schema (v1.0.0):

```yaml
# Common structure in both ps-* and nse-* agents
session_context:
  schema: "docs/schemas/session_context.json"
  schema_version: "1.0.0"
  input_validation: true
  output_validation: true
  on_receive:
    - validate_session_id
    - check_schema_version
    - extract_key_findings
    - process_blockers
  on_send:
    - populate_key_findings
    - calculate_confidence
    - list_artifacts
    - set_timestamp
```

**Implication:** The ps-* agents have the same handoff mechanisms as nse-*, but these have never been exercised in actual orchestration.

### 4. Capability Mapping: ps-* to nse-* Equivalents

| ps-* Agent | Functional Equivalent in nse-* | Pattern Applicability |
|------------|--------------------------------|----------------------|
| ps-analyst | nse-risk (analysis focus) | Sequential, Fan-In |
| ps-architect | nse-architecture | Sequential, Fan-Out |
| ps-critic | (new - generator-critic) | Generator-Critic Loop |
| ps-investigator | nse-risk (incident focus) | Sequential |
| ps-reporter | nse-reporter | Fan-In |
| ps-researcher | nse-explorer | Sequential, Fan-Out |
| ps-reviewer | nse-reviewer | Review Gate |
| ps-synthesizer | nse-reporter (aggregation) | Fan-In |
| ps-validator | nse-verification | Sequential |

### 5. Version Bump Risk Analysis (2.0.0 → 2.1.0)

The 2.1.0 version bump introduced:
1. **Session context validation** (WI-SAO-002) - New feature
2. **on_receive/on_send hooks** - New feature
3. **schema_version tracking** - New feature

**Risk Assessment:**
- These features were added but never integration-tested in orchestration
- The nse-* tests that passed used agents at v2.1.0 with these features
- ps-* at v2.1.0 may have subtle differences in implementation

---

## L2: Architectural Implications (Principal Architect)

### 1. Verification Gap Root Cause

The verification gap exists because:

1. **Separate development tracks:** nse-* agents were developed for NASA SE workflows and tested immediately in that context
2. **Generic framework assumption:** ps-* agents were assumed to work because they share architectural patterns
3. **Test strategy scope:** ORCHESTRATION-TEST-STRATEGY.md was scoped to nse-* only

### 2. Cross-Family Interoperability Question

A critical unanswered question: **Can ps-* and nse-* agents interoperate in the same workflow?**

Scenarios requiring cross-family interop:
- ps-researcher gathering data for nse-requirements
- ps-analyst performing gap analysis on nse-verification output
- ps-reviewer validating nse-architecture decisions
- ps-critic evaluating nse-reporter output quality

**Session context schema compatibility suggests YES, but no evidence exists.**

### 3. Generator-Critic Pattern Gap

ps-critic is a new agent type (Belbin: Monitor Evaluator) designed for iterative refinement loops. This pattern does NOT exist in nse-* family and has NO test coverage.

```
Generator-Critic Loop (untested):
┌──────────────────────────────────────────────┐
│  Orchestrator                                 │
│    │                                          │
│    ├─► ps-architect ─► creates design.md ─┐  │
│    │                                       │  │
│    │   ◄──── ps-critic ◄── evaluates ◄────┘  │
│    │                                          │
│    │   quality_score < 0.85?                  │
│    │     YES → send feedback to generator     │
│    │     NO  → accept and proceed             │
│    │                                          │
│    └─► max 3 iterations (circuit breaker)     │
└──────────────────────────────────────────────┘
```

### 4. Systemic Risk Assessment

| Risk | Likelihood | Impact | RPN |
|------|------------|--------|-----|
| ps-* fails in Sequential pattern | LOW (20%) | MEDIUM (5) | 1.0 |
| ps-* fails in Fan-Out pattern | LOW (20%) | MEDIUM (5) | 1.0 |
| ps-* fails in Fan-In aggregation | MEDIUM (40%) | HIGH (7) | 2.8 |
| Generator-Critic loop fails | MEDIUM (50%) | HIGH (8) | 4.0 |
| Cross-family handoff fails | MEDIUM (30%) | HIGH (8) | 2.4 |
| Session context schema mismatch | LOW (10%) | CRITICAL (9) | 0.9 |

**Total Risk Exposure:** 12.1 (MEDIUM-HIGH)

---

## Prioritized Test Recommendations

### Priority 1: CRITICAL (Must Test Before Production)

| Test ID | Name | Effort | Pattern | Agents | Rationale |
|---------|------|--------|---------|--------|-----------|
| PS-ORCH-001 | Sequential Research-Analysis | Small | Sequential | ps-researcher → ps-analyst | Core workflow, mirrors ORCH-001 |
| PS-ORCH-002 | Fan-In Synthesis | Medium | Fan-In | ps-researcher, ps-analyst, ps-architect → ps-synthesizer | Aggregation pattern critical for knowledge synthesis |
| PS-ORCH-003 | Generator-Critic Loop | Large | Iterative | ps-architect ↔ ps-critic | NEW pattern, no prior validation |
| PS-ORCH-004 | Review Gate | Medium | Review Gate | All ps-* → ps-reviewer | Mirrors ORCH-004 |

### Priority 2: HIGH (Should Test)

| Test ID | Name | Effort | Pattern | Agents | Rationale |
|---------|------|--------|---------|--------|-----------|
| PS-ORCH-005 | Fan-Out Investigation | Medium | Fan-Out | ps-investigator, ps-analyst, ps-researcher | Parallel analysis pattern |
| PS-ORCH-006 | Validation Chain | Small | Sequential | ps-architect → ps-validator → ps-reporter | Design validation workflow |
| CROSS-ORCH-001 | Cross-Family Handoff | Medium | Sequential | ps-researcher → nse-requirements | Interoperability validation |
| CROSS-ORCH-002 | Mixed Fan-In | Medium | Fan-In | ps-analyst + nse-risk → ps-reporter | Cross-family aggregation |

### Priority 3: MEDIUM (Nice to Have)

| Test ID | Name | Effort | Pattern | Agents | Rationale |
|---------|------|--------|---------|--------|-----------|
| PS-ORCH-007 | Incident Investigation | Medium | Sequential | ps-investigator → ps-analyst → ps-reporter | Incident workflow |
| PS-ORCH-008 | Knowledge Bootstrap | Large | Mixed | ps-researcher → ps-synthesizer → ps-architect | Full knowledge pipeline |
| PS-NEG-001 | Missing Dependency | Small | Error | ps-validator (no input) | Error handling |
| PS-NEG-002 | Invalid Schema | Small | Error | Malformed session_context | Schema validation |

### Effort Estimates

| Size | Time | Description |
|------|------|-------------|
| Small | 2-4 hours | Single pattern, 2-3 agents |
| Medium | 4-8 hours | Multi-phase, 3-5 agents |
| Large | 8-16 hours | Complex patterns, circuit breakers |

### Total Effort Summary

| Priority | Tests | Total Effort |
|----------|-------|--------------|
| CRITICAL | 4 | 16-24 hours |
| HIGH | 4 | 12-20 hours |
| MEDIUM | 4 | 12-20 hours |
| **TOTAL** | **12** | **40-64 hours** (1-2 weeks) |

---

## Risk Assessment for Skipping Tests

### If CRITICAL Tests Skipped

| Consequence | Likelihood | Impact |
|-------------|------------|--------|
| ps-* workflows fail in production | HIGH (70%) | Production outage |
| Generator-Critic loops infinite | MEDIUM (40%) | Resource exhaustion |
| Users lose trust in ps-* family | HIGH (60%) | Adoption failure |

**Recommendation:** CRITICAL tests are non-negotiable.

### If HIGH Tests Skipped

| Consequence | Likelihood | Impact |
|-------------|------------|--------|
| Cross-family workflows unusable | MEDIUM (50%) | Feature limitation |
| Parallel analysis patterns fail | LOW (30%) | Degraded performance |
| Fan-out patterns untested | MEDIUM (40%) | Limited parallelism |

**Recommendation:** HIGH tests strongly recommended.

### If MEDIUM Tests Skipped

| Consequence | Likelihood | Impact |
|-------------|------------|--------|
| Edge cases may fail | LOW (20%) | Minor issues |
| Error handling unclear | LOW (20%) | Debugging difficulty |
| Bootstrap workflow untested | LOW (30%) | Onboarding friction |

**Recommendation:** MEDIUM tests can be deferred if time-constrained.

---

## Evidence Summary

| Evidence ID | Type | Source | Relevance |
|-------------|------|--------|-----------|
| E-001 | Test Results | ORCHESTRATION-TEST-STRATEGY.md | 19/19 nse-* tests PASS |
| E-002 | Agent Definition | ps-analyst.md | Session context v1.0.0 implemented |
| E-003 | Agent Definition | ps-critic.md | Generator-critic pattern defined |
| E-004 | Test Evidence | orchestration-results/ | 36 artifact files from nse-* tests |
| E-005 | Schema | session_context schema | Identical between families |
| E-006 | Agent Definition | nse-reporter.md | Reference aggregator pattern |
| E-007 | Agent Definition | nse-reviewer.md | Reference review gate pattern |
| E-008 | Compatibility Matrix | ORCHESTRATION-TEST-STRATEGY.md line 719-746 | 100% nse-* compatibility |

---

## Conclusions

1. **Significant verification gap exists:** ps-* agents have 0% orchestration test coverage despite being architecturally equivalent to fully-tested nse-* agents.

2. **Risk is MEDIUM-HIGH:** Without orchestration testing, we cannot confirm multi-agent workflows will succeed with ps-* agents.

3. **Cross-family interoperability is unknown:** No tests validate that ps-* and nse-* can work together.

4. **Generator-Critic pattern is completely untested:** This new pattern has no validation.

5. **Effort is manageable:** 4 CRITICAL tests can be completed in 1-2 days; full coverage in 1-2 weeks.

---

## Recommendations

1. **IMMEDIATE:** Execute PS-ORCH-001 through PS-ORCH-004 (CRITICAL priority)
2. **SHORT-TERM:** Execute PS-ORCH-005 through CROSS-ORCH-002 (HIGH priority)
3. **MEDIUM-TERM:** Complete remaining tests and add to CI pipeline
4. **ONGOING:** Maintain test parity between ps-* and nse-* families

---

## PS Integration

- **PS ID:** WI-SAO-029
- **Entry ID:** e-002
- **Analysis Type:** Gap Analysis
- **Artifact Path:** `projects/PROJ-002-nasa-systems-engineering/analysis/wi-sao-029-e-002-verification-gap-analysis.md`

---

*DISCLAIMER: This analysis is AI-generated using established gap analysis methodology. All recommendations require human review and prioritization based on project constraints.*

*Generated by ps-analyst agent v2.1.0*
*Date: 2026-01-11*
*Constitutional Compliance: Jerry Constitution v1.0 (P-001, P-002, P-004, P-011, P-022)*
