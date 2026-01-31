# EN-020: Adversarial Critic and Reviewer Agents

<!--
TEMPLATE: Enabler
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.9
CREATED: 2026-01-31 (FEAT-005 adversarial feedback loop requirement)
PURPOSE: Research and implement adversarial evaluation agents for quality gates
-->

> **Type:** enabler
> **Status:** pending
> **Priority:** high
> **Impact:** high
> **Enabler Type:** exploration
> **Created:** 2026-01-31T01:00:00Z
> **Due:** TBD
> **Completed:** -
> **Parent:** FEAT-003
> **Owner:** Claude
> **Effort:** 13

---

## Summary

Research and create best-in-class adversarial critic and reviewer agents for the problem-solving and nasa-se skills. The current `ps-critic` agent is designed for constructive iterative improvement, but FEAT-005 compliance gates require a more rigorous adversarial evaluation approach that actively seeks flaws, gaps, and non-compliance.

**Technical Scope:**
- Research adversarial evaluation patterns in LLM agent architectures
- Analyze existing Jerry skill patterns for clean extension points
- Design adversarial prompting protocols for quality gates
- Implement `ps-critic-adversarial` mode or variant
- Update nasa-se review agents with adversarial capabilities

---

## Problem Statement

The current `ps-critic` agent (v2.2.0) has a **constructive** communication style optimized for Self-Refine iterative improvement loops. However, compliance quality gates in FEAT-005 and similar workflows require:

1. **Red Team Mindset** - Assume problems exist until proven otherwise
2. **Mandatory Findings** - Require minimum issue identification (not rubber-stamp approvals)
3. **Checklist Enforcement** - No partial credit; evidence required for every pass
4. **Counter-Example Seeking** - Force identification of failure scenarios
5. **Adversarial Challenge** - Question every claim and assumption

Without adversarial prompting, quality gates risk becoming performative rather than rigorous.

---

## Business Value

### Features Unlocked

- **Rigorous Compliance Gates** - FEAT-005 and future compliance workflows benefit from adversarial evaluation
- **Improved Quality Assurance** - Catch more issues before they reach production
- **Audit Trail Integrity** - Stronger evidence that quality was actually verified
- **Reusable Pattern** - Adversarial agents can be used across all Jerry skills

### Strategic Alignment

| Alignment Area | Impact |
|----------------|--------|
| Jerry Constitution P-001 (Truth) | HIGH - Adversarial evaluation surfaces truth |
| Jerry Constitution P-022 (No Deception) | HIGH - Cannot hide quality issues |
| FEAT-005 Compliance | CRITICAL - Required for feedback loop effectiveness |
| NASA-SE Quality Practices | HIGH - Aligns with independent verification |

---

## Technical Approach

### Phase 1: Research (4h)

1. **Industry Research** - Survey adversarial evaluation patterns in LLM systems
   - Constitutional AI red-teaming approaches
   - LLM-as-a-Judge evaluation frameworks (DeepEval, RAGAS)
   - Adversarial prompt engineering techniques
   - Red team/blue team patterns in AI safety

2. **Jerry Skill Analysis** - Understand existing agent extension patterns
   - How are agent variants implemented?
   - Where do prompting modes live (agent definition vs. invocation)?
   - What's the cleanest extension approach for existing agents?

3. **Document Findings** - Produce research synthesis

### Phase 2: Design (3h)

1. **Adversarial Protocol Design** - Define the prompting strategy
   - Red Team framing
   - Mandatory findings requirements
   - Checklist enforcement rules
   - Counter-example protocol

2. **Agent Architecture Decision** - Choose implementation approach:
   - Option A: Add "adversarial mode" to existing ps-critic
   - Option B: Create separate ps-critic-adversarial agent
   - Option C: Invocation-time prompting (no agent changes)

3. **NASA-SE Integration** - Plan adversarial capabilities for:
   - nse-reviewer (technical reviews)
   - nse-validator (verification)

### Phase 3: Implementation (4h)

1. Implement chosen agent architecture
2. Create adversarial prompting templates
3. Update SKILL.md documentation
4. Integration with orchestration workflows

### Phase 4: Validation (2h)

1. Test against FEAT-005 sample deliverables
2. Compare adversarial vs. constructive evaluation results
3. Validate feedback loop effectiveness

### Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     ADVERSARIAL EVALUATION ARCHITECTURE                      │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  CURRENT STATE (Constructive)           FUTURE STATE (Adversarial)          │
│  ┌─────────────────────────┐           ┌─────────────────────────┐         │
│  │      ps-critic          │           │      ps-critic          │         │
│  │  ┌─────────────────┐    │           │  ┌─────────────────┐    │         │
│  │  │ Tone: Analytical│    │    ──►    │  │ Mode: STANDARD  │    │         │
│  │  │ Style: Helpful  │    │           │  │ Mode: ADVERSARIAL│   │         │
│  │  └─────────────────┘    │           │  └─────────────────┘    │         │
│  └─────────────────────────┘           └─────────────────────────┘         │
│                                                                              │
│  ADVERSARIAL MODE CHARACTERISTICS:                                          │
│  ┌────────────────────────────────────────────────────────────────────────┐│
│  │ 1. RED TEAM FRAMING - "Assume problems exist"                          ││
│  │ 2. MANDATORY FINDINGS - "Must identify ≥3 issues"                      ││
│  │ 3. CHECKLIST ENFORCEMENT - "Evidence required for PASS"                ││
│  │ 4. DEVIL'S ADVOCATE - "What could go wrong?"                           ││
│  │ 5. COUNTER-EXAMPLES - "Identify failure scenarios"                     ││
│  │ 6. NO RUBBER STAMPS - "Perfect scores require justification"           ││
│  └────────────────────────────────────────────────────────────────────────┘│
│                                                                              │
│  INVOCATION PATTERN:                                                         │
│  ┌────────────────────────────────────────────────────────────────────────┐│
│  │ Task(                                                                   ││
│  │   prompt="""                                                            ││
│  │   ## ADVERSARIAL EVALUATION MODE                                        ││
│  │   You are operating as an ADVERSARIAL CRITIC...                         ││
│  │   [Red team framing, mandatory findings, etc.]                          ││
│  │   """                                                                   ││
│  │ )                                                                       ││
│  └────────────────────────────────────────────────────────────────────────┘│
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Non-Functional Requirements (NFRs) Addressed

| NFR Category | Requirement | Current State | Target State |
|--------------|-------------|---------------|--------------|
| Quality | Rigorous evaluation | Constructive feedback | Adversarial challenge |
| Accuracy | Issue detection rate | Unknown | ≥ 90% of real issues found |
| Reliability | False positive rate | Unknown | ≤ 20% false positives |
| Compliance | Checklist enforcement | Partial | 100% evidence-based |

---

## Children (Tasks)

### Task Inventory

| ID | Title | Status | Effort | Owner |
|----|-------|--------|--------|-------|
| TASK-425 | Research adversarial evaluation patterns | pending | 3 | - |
| TASK-426 | Analyze Jerry skill extension patterns | pending | 1 | - |
| TASK-427 | Design adversarial prompting protocol | pending | 2 | - |
| TASK-428 | Architecture decision (mode vs. variant) | pending | 1 | - |
| TASK-429 | Implement adversarial agent capabilities | pending | 3 | - |
| TASK-430 | Update SKILL.md documentation | pending | 1 | - |
| TASK-431 | Validate with FEAT-005 deliverables | pending | 2 | - |

---

## Progress Summary

### Status Overview

```
+------------------------------------------------------------------+
|                   ENABLER PROGRESS TRACKER                        |
+------------------------------------------------------------------+
| Tasks:     [....................] 0% (0/7 completed)             |
| Effort:    [....................] 0% (0/13 points completed)     |
+------------------------------------------------------------------+
| Overall:   [....................] 0%                             |
+------------------------------------------------------------------+
```

### Progress Metrics

| Metric | Value |
|--------|-------|
| **Total Tasks** | 7 |
| **Completed Tasks** | 0 |
| **Total Effort (points)** | 13 |
| **Completed Effort** | 0 |
| **Completion %** | 0% |

---

## Acceptance Criteria

### Definition of Done

- [ ] Research document produced with industry best practices
- [ ] Jerry skill extension patterns documented
- [ ] Adversarial prompting protocol designed and documented
- [ ] Architecture decision made and documented (ADR)
- [ ] Implementation complete (agent mode or variant)
- [ ] SKILL.md updated with adversarial usage instructions
- [ ] Validated against FEAT-005 sample deliverables
- [ ] Integration with orchestration workflows documented

### Technical Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| TC-1 | Adversarial evaluation finds ≥ 90% of intentionally planted issues | [ ] |
| TC-2 | Checklist items require explicit evidence for PASS status | [ ] |
| TC-3 | Perfect scores (1.0) require documented justification | [ ] |
| TC-4 | Protocol integrates cleanly with ORCHESTRATION.yaml quality gates | [ ] |

---

## Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Over-aggressive evaluation creates false positives | Medium | Medium | Calibrate with known-good samples |
| Adversarial prompting conflicts with Constitutional AI | Low | High | Align with P-001 (Truth) and P-022 (No Deception) |
| Implementation complexity delays FEAT-005 | Medium | High | Start with invocation-time prompting (Option C) |
| Inconsistent evaluation across invocations | Medium | Medium | Structured checklist enforcement |

---

## Dependencies

### Depends On

- [ps-critic v2.2.0](../../../../../skills/problem-solving/agents/ps-critic.md) - Current agent to extend
- [FEAT-005 Orchestration](../../FEAT-005-skill-compliance/orchestration/ORCHESTRATION_PLAN.md) - Quality gate requirements

### Enables

- [FEAT-005 Quality Gates](../../FEAT-005-skill-compliance/FEAT-005-skill-compliance.md) - Rigorous compliance evaluation
- Future Jerry compliance workflows
- NASA-SE independent verification patterns

---

## Related Items

### Hierarchy

- **Parent:** [FEAT-003: Future Enhancements](../FEAT-003-future-enhancements.md)

### Related Items

- **Discovery:** [DISC-002: Adversarial Prompting Protocol](../FEAT-003--DISC-002-adversarial-prompting-protocol.md)
- **Related Feature:** [FEAT-005: Skill Compliance](../../FEAT-005-skill-compliance/FEAT-005-skill-compliance.md)

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-01-31 | Claude | pending | Enabler created per FEAT-005 adversarial feedback loop requirement |

---

*Enabler Version: 1.0.0*
*Created: 2026-01-31*
