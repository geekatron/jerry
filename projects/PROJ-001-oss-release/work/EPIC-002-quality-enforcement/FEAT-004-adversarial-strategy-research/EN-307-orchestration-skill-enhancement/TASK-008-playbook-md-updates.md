# TASK-008: Orchestration PLAYBOOK.md Update Content

<!--
DOCUMENT-ID: FEAT-004:EN-307:TASK-008
VERSION: 1.0.0
AGENT: ps-architect-307
DATE: 2026-02-13
STATUS: Complete
PARENT: EN-307 (Orchestration Skill Enhancement - Adversarial Loops)
FEATURE: FEAT-004 (Adversarial Strategy Research & Skill Enhancement)
EPIC: EPIC-002 (Quality Framework Enforcement)
PROJECT: PROJ-001-oss-release
ACTIVITY: DOCUMENTATION
-->

> **Version:** 1.0.0
> **Agent:** ps-architect-307
> **Quality Target:** >= 0.92
> **Purpose:** Define the content to add to the orchestration PLAYBOOK.md (v4.0.0) documenting adversarial workflow guidance, quality gate workflows, and anti-patterns

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What this update delivers |
| [Version Bump](#version-bump) | PLAYBOOK.md version change |
| [L0 Additions: Adversarial Overview](#l0-additions-adversarial-overview) | ELI5 explanation of adversarial feedback loops |
| [L1 Additions: Adversarial Workflow](#l1-additions-adversarial-workflow) | Step-by-step adversarial workflow execution |
| [L1 Additions: Updated Pattern Selection](#l1-additions-updated-pattern-selection) | Pattern 9 in decision tree |
| [L1 Additions: Quality Gate Scenarios](#l1-additions-quality-gate-scenarios) | Common quality gate scenarios |
| [L2 Additions: Anti-Pattern Catalog](#l2-additions-anti-pattern-catalog) | New adversarial anti-patterns |
| [L2 Additions: Updated Constraints](#l2-additions-updated-constraints) | New hard/soft constraints |
| [L2 Additions: Updated Invariants](#l2-additions-updated-invariants) | New invariant checklist entries |
| [L2 Additions: Circuit Breaker Update](#l2-additions-circuit-breaker-update) | Updated circuit breaker config |
| [Integration Points](#integration-points) | Where new content inserts |
| [Traceability](#traceability) | Mapping to requirements |
| [References](#references) | Source citations |

---

## Summary

This document defines the content additions and modifications needed for the orchestration PLAYBOOK.md to include adversarial workflow guidance. The updates transform PLAYBOOK.md from v3.1.0 to v4.0.0. This document does NOT directly modify the existing PLAYBOOK.md file; it specifies the exact content to add, where to add it, and what to modify.

Key additions:
1. **L0 adversarial explanation** -- ELI5 for stakeholders on what adversarial review means
2. **L1 adversarial workflow** -- Step-by-step guide for executing adversarial feedback loops
3. **L1 quality gate scenarios** -- Common scenarios (PASS, CONDITIONAL PASS, FAIL, early exit)
4. **L2 adversarial anti-patterns** -- AP-005 through AP-008 added to anti-pattern catalog
5. **L2 updated constraints** -- New hard constraints for adversarial review
6. **L2 updated invariants** -- New invariant checklist entries
7. **Updated circuit breaker** -- Aligned with quality gate threshold

---

## Version Bump

| Field | Old | New |
|-------|-----|-----|
| Version | 3.1.0 | 4.0.0 |
| patterns_covered | 8 patterns | 9 patterns (added adversarial-feedback) |

---

## L0 Additions: Adversarial Overview

### Insert After "The Cast of Characters" Section

```markdown
## What Is Adversarial Review?

### The Quality Checkpoint Metaphor

```
+===================================================================+
|                  THE QUALITY CHECKPOINT                            |
+===================================================================+
|                                                                   |
|   Think of adversarial review like a quality inspection:          |
|                                                                   |
|   +--------+     +--------+     +--------+     +--------+         |
|   |BUILDER |     |INSPECT |     |FIX     |     |APPROVE |         |
|   |creates |---->|OR finds|---->|issues  |---->|quality |         |
|   |artifact|     |issues  |     |found   |     |passes  |         |
|   +--------+     +--------+     +--------+     +--------+         |
|                      |                             ^               |
|                      +-------- repeat until -------+               |
|                                                                   |
|   - Builder (Creator) produces work                               |
|   - Inspector (Critic) challenges and scores it                   |
|   - Builder revises based on feedback                             |
|   - Process repeats until quality score >= 0.92                  |
|   - If not met after 3 rounds, humans decide                     |
|                                                                   |
+===================================================================+
```

**Plain English:**
Adversarial review is a quality assurance process where specialized critic agents challenge and score the work of creator agents. It is like having a rigorous peer review built into every workflow. The orchestration skill automatically embeds these review cycles so quality enforcement is structural, not optional.

### Why Adversarial Review Matters

| Without Adversarial Review | With Adversarial Review |
|----------------------------|------------------------|
| Artifacts accepted as-is | Every artifact challenged and improved |
| Hidden assumptions persist | Assumptions surfaced and tested |
| Quality depends on individual agent | Quality enforced by process |
| No quality score tracking | Measurable quality improvement per iteration |
| Issues found late in workflow | Issues caught early per phase |
```

---

## L1 Additions: Adversarial Workflow

### Insert After "Workflow: Cross-Pollinated Pipeline" Section

```markdown
## Workflow: Adversarial Feedback Loop

### Overview

When adversarial validation is enabled (default for new workflows), the orchestration automatically inserts creator-critic-revision cycles at each qualifying phase.

### Phase A: Plan Generation (Automatic)

The orch-planner automatically detects phases requiring adversarial review and generates execution queue groups:

```
Group N:     Creator agents (produce initial artifacts)
Group N+1:   Critic - Iteration 1 (challenge + score)
Group N+2:   Revision - Iteration 1 (address findings)
Group N+3:   Critic - Iteration 2 (re-evaluate + score)
Group N+4:   Revision - Iteration 2 (final improvements)
Group N+5:   Critic - Iteration 3 (final scoring, may be SKIPPED)
Group N+6:   Validation (quality verdict)
```

**What triggers adversarial review:**
- Artifact type is architecture, decision, requirements, research, or process
- Decision criticality is C2 or higher
- Phase produces deliverables consumed by downstream phases

### Phase B: Execute Creator Agents

1. Execute all creator agents in the group (PARALLEL)
2. Update ORCHESTRATION.yaml via orch-tracker
3. Creator artifacts are now ready for adversarial review

### Phase C: Adversarial Iteration Loop

For each iteration (1 through 3):

1. **Critic execution:**
   - Critic agents review creator artifacts using assigned strategies
   - S-014 LLM-as-Judge produces quality score (0.00-1.00)
   - Critic artifacts document findings by severity (BLOCKING, MAJOR, MINOR)

2. **Score evaluation:**
   - orch-tracker records score in ORCHESTRATION.yaml
   - Evaluate quality gate:
     - Score >= 0.92 -> PASS (can exit early if iteration >= 2)
     - Score < 0.92 and more iterations -> CONTINUE
     - Score >= 0.85 at max iterations -> CONDITIONAL PASS
     - Score < 0.85 at max iterations -> FAIL

3. **Revision (if CONTINUE):**
   - Creator agents revise artifacts based on critique
   - Findings resolution tracked per severity
   - Next iteration begins

### Phase D: Validation

After the final iteration:

1. ps-validator reviews final artifacts
2. Validates against enabler acceptance criteria
3. Produces verdict: PASS / CONDITIONAL PASS / FAIL
4. orch-tracker records verdict in ORCHESTRATION.yaml

### Phase E: Quality Gate Resolution

**If PASS:** Phase complete, proceed to next phase or barrier
**If CONDITIONAL PASS:** User ratification required before proceeding (P-020)
**If FAIL:** Blocker created, next phase BLOCKED, escalation to user

### Example: Executing Adversarial Review

```
User: "Execute adversarial iteration 1 for Phase 2"

Claude: [Reads ORCHESTRATION.yaml for current state]
        [Identifies critic agents and their strategies]
        [Executes ps-critic-303 with S-002, S-007, S-014]
        [Extracts quality score from critique artifact]
        [Updates ORCHESTRATION.yaml via orch-tracker:]

        iterations:
          - iteration: 1
            status: "COMPLETE"
            scores: { EN-303: 0.79 }

        [Score 0.79 < 0.92 -> CONTINUE to iteration 2]
        [Reports: "Iteration 1 complete. Score: 0.79. 3 blocking findings.
                   Proceeding to revision."]
```
```

---

## L1 Additions: Updated Pattern Selection

### Update Pattern Selection Decision Tree

Add Pattern 9 to the decision tree:

```markdown
### Pattern Selection Decision Tree (Updated v4.0.0)

```
START: How many agents?
       |
  +----+----+
  |         |
  v         v
ONE       MULTIPLE
  |         |
  v         v
Pattern 1   Dependencies?
(Single)    |
       +----+----+
       |         |
       v         v
      YES        NO
       |         |
       v         v
   Pattern 2   Pattern 3/4
   (Sequential) (Fan-Out/In)
       |
       v
   Bidirectional?
       |
  +----+----+
  |         |
  v         v
 YES        NO
  |         |
  v         v
Pattern 5   Quality gates?
(Cross-Poll) |
        +----+----+
        |         |
        v         v
       YES        NO
        |         |
        v         v
   Adversarial?  Pattern 6
        |         (Diamond)
   +----+----+
   |         |
   v         v
  YES        NO
   |         |
   v         v
Pattern 9   Pattern 7/8
(Adversarial) (Review/Loop)
```

### Updated Pattern Summary

| # | Pattern | When to Use | Cognitive Mode |
|---|---------|-------------|----------------|
| 1 | **Single Agent** | Direct task, no coordination | Depends on agent |
| 2 | **Sequential Chain** | Order-dependent state passing | Convergent |
| 3 | **Fan-Out** | Parallel independent research | Divergent |
| 4 | **Fan-In** | Aggregate multiple outputs | Convergent |
| 5 | **Cross-Pollinated** | Bidirectional pipeline exchange | Mixed |
| 6 | **Divergent-Convergent** | Explore then converge (diamond) | Divergent -> Convergent |
| 7 | **Review Gate** | Quality checkpoint (SRR/PDR/CDR) | Convergent |
| 8 | **Generator-Critic** | Iterative refinement loop | Convergent |
| **9** | **Adversarial Feedback** | **Creator-critic-revision with quality gates** | **Convergent** |
```

---

## L1 Additions: Quality Gate Scenarios

### Insert After "Common Scenarios" Section

```markdown
### Scenario: Quality Gate PASS

```yaml
# Iteration 2 score meets threshold
iterations:
  - iteration: 2
    scores: { EN-303: 0.928 }
    # 0.928 >= 0.92 -> PASS

# Remaining iterations SKIPPED
  - iteration: 3
    status: "SKIPPED"
    note: "Score 0.928 >= 0.92 at iteration 2"
```

**Resolution:** Phase marked complete, proceed to next phase.

### Scenario: Quality Gate CONDITIONAL PASS

```yaml
# Max iterations reached, score between 0.85 and 0.92
iterations:
  - iteration: 3
    scores: { EN-302: 0.893 }
    # 0.893 < 0.92 but >= 0.85 -> CONDITIONAL PASS

quality_gate_result: "CONDITIONAL_PASS"
awaiting_ratification: true
```

**Resolution Options:**
1. **Ratify:** User confirms the score is acceptable -> phase complete
2. **Extend:** User authorizes additional iteration(s)
3. **Accept with conditions:** User documents accepted risks

### Scenario: Quality Gate FAIL

```yaml
# Max iterations reached, score below 0.85
iterations:
  - iteration: 3
    scores: { EN-XXX: 0.78 }
    # 0.78 < 0.85 -> FAIL

blockers:
  active:
    - id: "BLK-QG-001"
      description: "Quality score 0.78 < 0.92 after 3 iterations for EN-XXX"
      severity: "HIGH"
```

**Resolution Options:**
1. **Root cause:** Investigate why quality is low
2. **Redesign:** Revise approach and restart adversarial cycle
3. **Escalate:** Bring in additional expertise
4. **Override:** User explicitly accepts risk (P-020)

### Scenario: Early Exit from Adversarial Cycle

Early exit is allowed when:
- All enablers score >= 0.92 at iteration 2
- No BLOCKING findings remain unresolved
- Criticality is NOT C4

```yaml
iterations:
  - iteration: 1
    scores: { EN-302: 0.79 }
  - iteration: 2
    scores: { EN-302: 0.935 }
    # All enablers PASS, no blocking findings
  - iteration: 3
    status: "SKIPPED"
    note: "All enablers achieved PASS at iteration 2"
```
```

---

## L2 Additions: Anti-Pattern Catalog

### AP-005: Leniency Drift

```markdown
### AP-005: Leniency Drift

```
+===================================================================+
| ANTI-PATTERN: Leniency Drift                                      |
+===================================================================+
|                                                                   |
| SYMPTOM:    Quality scores consistently at 0.93-0.95 from         |
|             iteration 1. No iteration ever needs revision.         |
|             Adversarial review is rubber-stamp, not genuine.       |
|                                                                   |
| CAUSE:      Critic agents not calibrated for anti-leniency.       |
|             Missing H-16 calibration in critic prompts.            |
|                                                                   |
| IMPACT:     - Quality gate is meaningless (always passes)         |
|             - Hidden issues slip through unchallenged              |
|             - Adversarial review wastes tokens without value       |
|                                                                   |
| FIX:        ALWAYS include anti-leniency calibration (H-16).      |
|             Monitor for suspiciously high first-iteration scores.  |
|             If iter 1 score > 0.90, flag for human review.        |
|                                                                   |
+===================================================================+
```
```

### AP-006: Strategy Misalignment

```markdown
### AP-006: Strategy Misalignment

```
+===================================================================+
| ANTI-PATTERN: Strategy Misalignment                                |
+===================================================================+
|                                                                   |
| SYMPTOM:    Critic applies Red Team (S-001) to routine C1 task.   |
|             Or applies Self-Refine (S-010) to C4 critical ADR.    |
|             Strategy intensity mismatches criticality.             |
|                                                                   |
| CAUSE:      Criticality not assessed. Default strategies used     |
|             without consulting C1-C4 framework.                    |
|                                                                   |
| IMPACT:     - Over-review of routine work (wasted tokens)         |
|             - Under-review of critical work (quality risk)         |
|             - Token budget exhausted on low-value reviews          |
|                                                                   |
| FIX:        ALWAYS assess criticality per phase.                   |
|             Use strategy selection algorithm from TASK-002.        |
|             Match strategy intensity to criticality level.         |
|                                                                   |
+===================================================================+
```
```

### AP-007: Adversarial Bypass

```markdown
### AP-007: Adversarial Bypass

```
+===================================================================+
| ANTI-PATTERN: Adversarial Bypass                                   |
+===================================================================+
|                                                                   |
| SYMPTOM:    Adversarial cycle skipped entirely. Artifacts marked   |
|             COMPLETE without any quality score. Phase proceeds     |
|             without critic review.                                 |
|                                                                   |
| CAUSE:      Orchestrator ignores adversarial execution queue       |
|             groups. Manual status override without review.         |
|                                                                   |
| IMPACT:     - No quality assurance for the phase                  |
|             - Downstream consumers receive unvalidated artifacts   |
|             - Evidence-based closure (V-060) violated              |
|                                                                   |
| FIX:        NEVER mark artifacts COMPLETE without S-014 score.    |
|             Enforce evidence-based closure via orch-tracker.       |
|             Barrier gate blocks cross-pollination without scores.  |
|                                                                   |
+===================================================================+
```
```

### AP-008: Score Inflation via Revision Accumulation

```markdown
### AP-008: Score Inflation via Revision Accumulation

```
+===================================================================+
| ANTI-PATTERN: Score Inflation via Revision Accumulation            |
+===================================================================+
|                                                                   |
| SYMPTOM:    Revision adds content addressing critique but          |
|             introduces new issues not caught by next iteration.    |
|             Score increases but artifact quality does not.         |
|                                                                   |
| CAUSE:      Critic focuses only on previously-flagged issues       |
|             and does not re-evaluate the full artifact.            |
|                                                                   |
| IMPACT:     - False sense of quality improvement                  |
|             - New issues introduced during revision persist        |
|             - Final artifact has hidden quality gaps               |
|                                                                   |
| FIX:        Critic MUST evaluate the FULL artifact at each         |
|             iteration, not just previously-flagged sections.       |
|             Use S-013 Inversion at iteration 2 to catch new        |
|             issues introduced by revision.                         |
|                                                                   |
+===================================================================+
```
```

---

## L2 Additions: Updated Constraints

### New Hard Constraints

Add to the Hard Constraints table:

```markdown
| ID | Constraint | Rationale |
|----|------------|-----------|
| HC-001 | Maximum ONE level of agent nesting | P-003 Jerry Constitution |
| HC-002 | ORCHESTRATION.yaml is SSOT | Single source of truth for recovery |
| HC-003 | Barriers are blocking (never optional) | Cross-pollination is the point |
| HC-004 | Checkpoints required at phase boundaries | Context rot survival |
| HC-005 | Agent outputs must be persisted to files | P-002 File Persistence |
| **HC-006** | **Quality gate >= 0.92 for phase completion** | **H-13 quality enforcement** |
| **HC-007** | **Minimum 3 adversarial iterations** | **H-14 iteration requirement** |
| **HC-008** | **S-014 scoring at every iteration** | **H-15 mandatory scoring** |
| **HC-009** | **Evidence-based closure required** | **V-060 closure enforcement** |
| **HC-010** | **Barrier gate blocks without quality scores** | **FR-307-018** |
```

### New Soft Constraints

```markdown
| ID | Constraint | When to Relax |
|----|------------|---------------|
| SC-001 | Parallel execution for independent agents | If debugging, run sequential |
| SC-002 | Agent output in designated directory | If special output format needed |
| SC-003 | Cross-pollination at every barrier | If tracks truly independent |
| **SC-004** | **Anti-leniency calibration for critics** | **Never -- always required (H-16)** |
| **SC-005** | **Strategy assignment matches criticality** | **User override with justification** |
```

---

## L2 Additions: Updated Invariants

### New Invariant Entries

```markdown
[X] INV-006: Quality score exists before artifact marked COMPLETE
           Violation: Evidence-based closure broken, unvalidated artifacts downstream

[X] INV-007: Barrier cannot be crossed without upstream quality gate PASS
           Violation: Unvalidated artifacts flow to cross-pollination

[X] INV-008: Critic agents include anti-leniency calibration
           Violation: Rubber-stamp reviews, meaningless quality scores

[X] INV-009: Quality threshold read from SSOT, not hardcoded
           Violation: Threshold drift between consumers, inconsistent enforcement
```

---

## L2 Additions: Circuit Breaker Update

### Updated Generator-Critic Circuit Breaker

Update the existing circuit breaker section to align with adversarial quality gates:

```yaml
circuit_breaker:
  max_iterations: 3                # Hard limit (H-14)
  quality_threshold: 0.92          # Updated from 0.85 to 0.92 (H-13)
  conditional_threshold: 0.85      # NEW: CONDITIONAL PASS threshold
  escalation: human_review         # After 3 fails -> human intervention (P-020)
  early_exit: true                 # NEW: Can exit at iteration 2 if threshold met
  early_exit_min_iteration: 2      # NEW: Earliest possible exit
  early_exit_exclusion: "C4"       # NEW: C4 always completes all iterations
```

**Change from v3.1.0:** `quality_threshold` raised from 0.85 to 0.92 to align with H-13 quality gate requirement. The old 0.85 threshold becomes the `conditional_threshold` for CONDITIONAL PASS determination.

---

## Integration Points

### Where Content Inserts into Existing PLAYBOOK.md

| New Content | Insert Location | Type |
|-------------|----------------|------|
| L0 Adversarial Overview | After "The Cast of Characters" in L0 section | Insert new section |
| L1 Adversarial Workflow | After "Workflow: Cross-Pollinated Pipeline" in L1 section | Insert new section |
| L1 Updated Pattern Selection | Replace existing pattern decision tree | Replace |
| L1 Quality Gate Scenarios | After "Common Scenarios" in L1 section | Append |
| L2 Anti-Patterns AP-005 through AP-008 | After AP-004 in Anti-Pattern Catalog | Append |
| L2 Updated Constraints | Append to Hard/Soft Constraints tables | Append |
| L2 Updated Invariants | Append to Invariant Checklist | Append |
| L2 Circuit Breaker Update | Replace existing circuit_breaker section | Replace |
| v4.0.0 version footer | Replace version in footer | Replace |

---

## Traceability

| Requirement | Content Section | Status |
|-------------|----------------|--------|
| NFR-307-007 | All sections (PLAYBOOK documentation completeness) | Covered |
| NFR-307-008 | L1 Adversarial Workflow (live example references) | Covered |
| NFR-307-005 | L0 overview, L2 constraints (P-003 compliance) | Covered |
| NFR-307-001 | L1 Quality Gate Scenarios (backward compatibility) | Covered |
| NFR-307-002 | L1 Adversarial Workflow (opt-out mentioned) | Covered |

---

## References

| # | Citation | Sections Referenced |
|---|----------|-------------------|
| 1 | FEAT-004:EN-307:TASK-001 (Requirements) | NFR-307-001 through NFR-307-008 |
| 2 | FEAT-004:EN-307:TASK-002 (Planner Design) | Detection, strategy selection, iteration |
| 3 | FEAT-004:EN-307:TASK-003 (Tracker Design) | Quality gate logic, escalation, early exit |
| 4 | Orchestration PLAYBOOK.md v3.1.0 | Baseline for integration points |
| 5 | ADR-EPIC002-001 | Strategy pool |
| 6 | Barrier-2 ENF-to-ADV Handoff | H-13 through H-17 |

---

*Document ID: FEAT-004:EN-307:TASK-008*
*Agent: ps-architect-307*
*Created: 2026-02-13*
*Status: Complete*
