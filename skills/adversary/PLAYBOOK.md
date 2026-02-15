---
name: adversary-playbook
description: Step-by-step execution procedures for adversarial quality reviews, including strategy selection by criticality, scoring workflows, canonical strategy pairings, and full C4 tournament reviews.
version: "1.0.0"
skill: adversary
constitutional_compliance: Jerry Constitution v1.0
agents_covered:
  - adv-selector
  - adv-executor
  - adv-scorer
---

# Adversary Playbook

> **Version:** 1.0.0
> **Skill:** adversary
> **Purpose:** On-demand adversarial quality reviews using strategy templates
> **SSOT Reference:** `.context/rules/quality-enforcement.md`
> **Created:** 2026-02-15

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Strategy Selection Flowchart](#strategy-selection-flowchart) | Decision logic for choosing strategies by criticality |
| [Procedure 1: Review at C2 Criticality](#procedure-1-review-a-deliverable-at-c2-criticality) | Standard adversarial review workflow |
| [Procedure 2: Score with S-014](#procedure-2-score-a-deliverable-with-s-014-llm-as-judge) | Focused quality scoring |
| [Procedure 3: Devil's Advocate + Steelman](#procedure-3-run-devils-advocate--steelman-pairing) | Canonical pairing per H-16 |
| [Procedure 4: Full C4 Tournament](#procedure-4-full-c4-tournament-review) | All 10 strategies tournament |
| [Error Handling](#error-handling) | Failure scenarios and recovery |
| [Agent Orchestration Patterns](#agent-orchestration-patterns) | How to sequence agents |
| [Quick Reference Card](#quick-reference-card) | Summary table |

---

## Strategy Selection Flowchart

Use this flowchart to determine the correct strategy set for a deliverable.

```
STRATEGY SELECTION FLOWCHART:
=============================

START: What is the criticality level?
       |
       +-- Is it reversible in 1 session, <3 files?
       |   YES → C1 (Routine)
       |         Required: {S-010}
       |         Optional: {S-003, S-014}
       |
       +-- Is it reversible in 1 day, 3-10 files?
       |   YES → C2 (Standard)
       |         Required: {S-007, S-002, S-014}
       |         Optional: {S-003, S-010}
       |
       +-- Is it >1 day to reverse, >10 files, or API changes?
       |   YES → C3 (Significant)
       |         Required: {S-007, S-002, S-014, S-004, S-012, S-013}
       |         Optional: {S-001, S-003, S-010, S-011}
       |
       +-- Is it irreversible, architecture/governance/public?
           YES → C4 (Critical)
                 Required: ALL 10 strategies
                 Optional: None

AUTO-ESCALATION CHECKS:
  - Touches JERRY_CONSTITUTION.md? → Auto-C4 (AE-001)
  - Touches .context/rules/? → Auto-C3 minimum (AE-002)
  - New or modified ADR? → Auto-C3 minimum (AE-003)
  - Modifies baselined ADR? → Auto-C4 (AE-004)
  - Security-relevant code? → Auto-C3 minimum (AE-005)

H-16 ORDERING CONSTRAINT:
  S-003 (Steelman) MUST come BEFORE S-002 (Devil's Advocate)
  Always strengthen first, then challenge.
```

---

## Procedure 1: Review a Deliverable at C2 Criticality

**Goal:** Perform a standard adversarial review of a C2 deliverable using the required strategy set.

**Required strategies:** S-007 (Constitutional AI Critique), S-002 (Devil's Advocate), S-014 (LLM-as-Judge)

**Recommended additions:** S-003 (Steelman) before S-002 per H-16

### Step-by-Step

```
PROCEDURE: C2 Adversarial Review
=================================

Prerequisites:
  - Deliverable path identified
  - Criticality confirmed as C2 (reversible in 1 day, 3-10 files)
  - Auto-escalation checks passed (not auto-C3/C4)

Step 1: Strategy Selection (with optional user overrides)
  Agent: adv-selector
  Input: Criticality=C2, deliverable type, deliverable path,
         strategy overrides (if any — user-specified additions/removals)
  Output: Ordered strategy list with template paths

  Expected output (default):
    1. S-003 (Steelman) — optional but RECOMMENDED per H-16
    2. S-007 (Constitutional AI Critique) — required
    3. S-002 (Devil's Advocate) — required
    4. S-014 (LLM-as-Judge) — required (always last for scoring)

  User Override Example:
    User says: "Add S-004 Pre-Mortem and skip S-003 Steelman"
    adv-selector receives: Strategy Overrides = "+S-004, -S-003"
    adv-selector produces:
      1. S-007 (Constitutional AI Critique) — required
      2. S-002 (Devil's Advocate) — required
      3. S-004 (Pre-Mortem Analysis) — user-added
      4. S-014 (LLM-as-Judge) — required (always last)
    Note: S-003 removal means H-16 ordering constraint is N/A.
    Strategy Overrides Applied: "+S-004 (user), -S-003 (user)"

  Override Limits (P-020 respected, HARD rules preserved):
    - User CANNOT remove S-014 from C2+ reviews (H-13 requires scoring)
    - User CANNOT reorder S-003 after S-002 (H-16 is a HARD constraint)
    - User CAN add optional strategies from any criticality level
    - User CAN remove optional strategies
    - User CAN override scoring threshold (adv-scorer accepts custom input)

Step 2: Execute S-003 Steelman (H-16 compliance)
  Agent: adv-executor
  Input: Strategy=S-003, deliverable path,
         template=.context/templates/adversarial/s-003-steelman.md
  Output: Steelman report — strongest version of the argument

  Purpose: Ensure fair assessment by strengthening before challenging.

Step 3: Execute S-007 Constitutional AI Critique
  Agent: adv-executor
  Input: Strategy=S-007, deliverable path,
         template=.context/templates/adversarial/s-007-constitutional-ai.md
  Output: Constitutional compliance findings (Critical/Major/Minor)

Step 4: Execute S-002 Devil's Advocate
  Agent: adv-executor
  Input: Strategy=S-002, deliverable path,
         template=.context/templates/adversarial/s-002-devils-advocate.md
  Output: Assumption challenges and alternative perspectives

Step 5: Score with S-014 LLM-as-Judge
  Agent: adv-scorer
  Input: Deliverable path, findings from Steps 2-4
  Output: 6-dimension weighted composite score

  Verdict:
    Score >= 0.92 → PASS (H-13 threshold met)
    Score < 0.92 → REVISE (specific dimension feedback provided)

Step 6: Persist Results
  All outputs persisted to files per P-002.
  Orchestrator collects findings and score for decision.
```

### Example

```
User: "Run a C2 adversarial review on docs/decisions/adr-042-persistence.md"

Step 1: adv-selector → selects {S-003, S-007, S-002, S-014}
Step 2: adv-executor runs S-003 → strengthens the ADR's argument
Step 3: adv-executor runs S-007 → checks constitutional compliance
Step 4: adv-executor runs S-002 → challenges key assumptions
Step 5: adv-scorer runs S-014 → scores 0.87 (below 0.92 threshold)
Step 6: Result: REVISE — "Internal Consistency (0.75) and Evidence Quality (0.70)
        need improvement. Specific gaps: Section 3 contradicts Section 5 rationale;
        two claims lack source citations."
```

---

## Procedure 2: Score a Deliverable with S-014 LLM-as-Judge

**Goal:** Produce a quality score using the SSOT 6-dimension weighted rubric without running the full strategy battery.

**Strategy:** S-014 (LLM-as-Judge) only

### Step-by-Step

```
PROCEDURE: S-014 Quality Scoring
==================================

Prerequisites:
  - Deliverable path identified
  - Scoring dimensions confirmed (SSOT 6-dimension default)

Step 1: Read Deliverable
  Agent: adv-scorer
  Input: Deliverable path
  Action: Read the full deliverable content

Step 2: Score Each Dimension Independently
  Agent: adv-scorer
  Apply SSOT dimensions with weights:
    - Completeness (0.20): Does output address all requirements?
    - Internal Consistency (0.20): Are claims mutually consistent?
    - Methodological Rigor (0.20): Does approach follow established methods?
    - Evidence Quality (0.15): Are claims supported by credible evidence?
    - Actionability (0.15): Can output be acted upon with clear next steps?
    - Traceability (0.10): Can claims be traced to sources?

Step 3: Apply Leniency Bias Counteraction
  - Score each dimension against rubric LITERALLY, not impressionistically
  - When uncertain between adjacent scores, choose the LOWER one
  - Document specific evidence for each dimension score

Step 4: Compute Weighted Composite
  Formula: score = SUM(dimension_score * weight)

Step 5: Determine Verdict
  Score >= 0.92 → PASS (quality gate met, H-13)
  Score 0.85-0.91 → REVISE (close, targeted improvements)
  Score 0.70-0.84 → REVISE (significant gaps)
  Score 0.50-0.69 → REVISE (major revision needed)
  Score < 0.50 → ESCALATE (fundamental issues, may need rethink)

Step 6: Persist Score Report
  Output: Per-dimension scores, weighted composite, verdict,
          specific evidence for each score, improvement recommendations
```

### Example

```
User: "Score docs/synthesis/epic-003-final.md with LLM-as-Judge"

adv-scorer evaluates:
  Completeness:          0.95 * 0.20 = 0.190
  Internal Consistency:  0.90 * 0.20 = 0.180
  Methodological Rigor:  0.92 * 0.20 = 0.184
  Evidence Quality:      0.88 * 0.15 = 0.132
  Actionability:         0.94 * 0.15 = 0.141
  Traceability:          0.90 * 0.10 = 0.090
  ─────────────────────────────────────────
  Weighted Composite:              0.917

Verdict: REVISE (0.917 < 0.920 threshold)
Recommendation: "Evidence Quality (0.88) is the weakest dimension.
  Two claims in Section 4 need source citations. Adding these would
  likely push composite above 0.92."
```

---

## Procedure 3: Run Devil's Advocate + Steelman Pairing

**Goal:** Apply the canonical adversarial pairing: strengthen the argument (S-003), then challenge it (S-002). This satisfies H-16 (Steelman before critique).

**Strategies:** S-003 (Steelman Technique) followed by S-002 (Devil's Advocate)

### Step-by-Step

```
PROCEDURE: Steelman + Devil's Advocate Pairing
================================================

Prerequisites:
  - Deliverable path identified
  - H-16 compliance: S-003 MUST precede S-002

Step 1: Execute S-003 Steelman Technique
  Agent: adv-executor
  Input: Strategy=S-003, deliverable path,
         template=.context/templates/adversarial/s-003-steelman.md
  Process:
    1. Read the deliverable thoroughly
    2. Identify the core argument and supporting evidence
    3. Present the STRONGEST possible version of the argument
    4. Acknowledge what works well and why
    5. Fill in gaps that the author likely intended
  Output: Steelman report with:
    - Best interpretation of the argument
    - Strongest supporting evidence identified
    - Implicit strengths made explicit

Step 2: Execute S-002 Devil's Advocate
  Agent: adv-executor
  Input: Strategy=S-002, deliverable path,
         template=.context/templates/adversarial/s-002-devils-advocate.md,
         steelman_output (from Step 1)
  Process:
    1. Read the deliverable AND the steelman output
    2. Challenge the STEELMANNED argument (not the weakest reading)
    3. Identify assumptions that could be wrong
    4. Propose credible alternative interpretations
    5. Classify findings by severity (Critical/Major/Minor)
  Output: Devil's Advocate report with:
    - Challenged assumptions with severity
    - Alternative perspectives with evidence
    - Risk assessment of unexamined assumptions

Step 3: Synthesize Findings
  Orchestrator combines steelman and devil's advocate outputs.
  The combination provides a balanced assessment:
    - Steelman ensures fair treatment of the author's intent
    - Devil's Advocate ensures rigorous challenge of assumptions

Step 4: Persist Results
  Both reports persisted to files per P-002.
```

### Example

```
User: "Run Steelman and Devil's Advocate on this design document"

Step 1: adv-executor runs S-003 →
  "The design's core strength is its separation of concerns. The choice
   of event sourcing is well-motivated by the audit trail requirement.
   The author's implicit argument for CQRS follows logically from the
   read/write ratio analysis."

Step 2: adv-executor runs S-002 →
  "Even in its strongest form, the design has these challenges:
   [MAJOR] Event sourcing assumes bounded aggregate sizes — what happens
   when an aggregate accumulates 10,000+ events?
   [MAJOR] CQRS adds operational complexity — the 3:1 read/write ratio
   may not justify the additional infrastructure.
   [MINOR] No discussion of event versioning strategy."

Result: Balanced assessment with fair treatment AND rigorous challenge.
```

---

## Procedure 4: Full C4 Tournament Review

**Goal:** Execute all 10 selected adversarial strategies against a C4 (Critical) deliverable. This is the most thorough review level, required for irreversible decisions.

**Strategies:** All 10 — S-001, S-002, S-003, S-004, S-007, S-010, S-011, S-012, S-013, S-014

### Step-by-Step

```
PROCEDURE: C4 Tournament Review
=================================

Prerequisites:
  - Deliverable confirmed as C4 (irreversible, architecture/governance/public)
  - OR auto-escalated to C4 (AE-001: constitution, AE-004: baselined ADR)
  - All strategy templates available in .context/templates/adversarial/

Phase 1: Strategy Selection
  Agent: adv-selector
  Input: Criticality=C4, deliverable type, deliverable path
  Output: All 10 strategies in execution order

  REQUIRED EXECUTION ORDER (H-16 compliant):
    Group A — Self-Review:
      1. S-010 (Self-Refine)
    Group B — Strengthen:
      2. S-003 (Steelman Technique)
    Group C — Challenge:
      3. S-002 (Devil's Advocate)
      4. S-004 (Pre-Mortem Analysis)
      5. S-001 (Red Team Analysis)
    Group D — Verify:
      6. S-007 (Constitutional AI Critique)
      7. S-011 (Chain-of-Verification)
    Group E — Decompose:
      8. S-012 (FMEA)
      9. S-013 (Inversion Technique)
    Group F — Score:
      10. S-014 (LLM-as-Judge) — ALWAYS LAST

Phase 2: Strategy Execution (Groups A-E)
  Agent: adv-executor (invoked once per strategy by orchestrator)

  For each strategy 1-9:
    1. Load template from .context/templates/adversarial/
    2. Execute strategy against deliverable
    3. Classify findings: Critical / Major / Minor
    4. Persist execution report to file (P-002)

Phase 3: Quality Scoring (Group F)
  Agent: adv-scorer
  Input: Deliverable path + ALL findings from Phase 2
  Process:
    1. Score 6 SSOT dimensions using S-014 rubric
    2. Incorporate findings from all 9 prior strategies as evidence
    3. Apply strict leniency bias counteraction
    4. Compute weighted composite
  Output: Tournament score report

Phase 4: Tournament Verdict
  Orchestrator evaluates:
    - Weighted composite score vs 0.92 threshold
    - Count of Critical findings (any Critical → automatic REVISE)
    - Count of Major findings (>3 Major → recommend REVISE)

  Verdict:
    PASS: Score >= 0.92 AND no Critical findings
    REVISE: Score < 0.92 OR any Critical findings
    ESCALATE: Fundamental issues requiring human decision

Phase 5: Persist Tournament Summary
  All 10 strategy reports + tournament summary persisted per P-002.
```

### Example

```
User: "Run full C4 tournament on docs/governance/JERRY_CONSTITUTION.md changes"

Phase 1: adv-selector → all 10 strategies, C4 confirmed (AE-001)

Phase 2: adv-executor runs 9 strategies:
  S-010 Self-Refine → 2 Minor suggestions
  S-003 Steelman → Core governance model well-structured
  S-002 Devil's Advocate → 1 Major assumption challenged
  S-004 Pre-Mortem → 2 Major failure scenarios identified
  S-001 Red Team → 1 Critical governance bypass found
  S-007 Constitutional AI → 1 Major compliance gap
  S-011 Chain-of-Verification → 3 claims verified, 1 unverifiable
  S-012 FMEA → RPN analysis identifies 2 high-risk modes
  S-013 Inversion → Inverted claim reveals blind spot

Phase 3: adv-scorer runs S-014:
  Weighted Composite: 0.84

Phase 4: Verdict: REVISE
  Reason: 1 Critical finding (governance bypass) + score 0.84 < 0.92

Phase 5: Tournament summary persisted with all 10 reports.
```

---

## Error Handling

Common failure scenarios and recovery procedures for adversarial review workflows.

| Scenario | Detection | Recovery |
|----------|-----------|----------|
| **Strategy template not found** | adv-executor cannot read template file path | WARN the orchestrator. Skip the strategy and note it as "SKIPPED — template not found" in the execution report. If the strategy is required for the criticality level, the review is incomplete and MUST be reported as such. |
| **Deliverable file inaccessible** | Any agent cannot read the deliverable path | HALT the workflow. Report "ERROR: Deliverable not found at {path}". The orchestrator must resolve the path before retrying. |
| **Agent fails mid-execution** | Agent produces no output or produces malformed output | Orchestrator retries the agent once with the same input. If the second attempt fails, WARN and skip the strategy (if optional) or ESCALATE to the user (if required). |
| **Invalid score produced** | adv-scorer returns a score outside 0.0-1.0 range or composite does not match dimension sum | adv-scorer self-review (H-15) should catch this before persistence. If detected post-persistence, the orchestrator re-invokes adv-scorer with the same input. |

---

## Agent Orchestration Patterns

### Pattern 1: Quick Score (Single Agent)

```
TOPOLOGY:
---------

  +-------------+
  | adv-scorer  | --> Score report
  +-------------+

Use when: You just need a quality score, no strategy execution.
```

### Pattern 2: Strategy + Score (Two Agents)

```
TOPOLOGY:
---------

  +---------------+    +-------------+
  | adv-executor  |--->| adv-scorer  |
  | (run strategy)|    | (score)     |
  +---------------+    +-------------+

Use when: Running a specific strategy followed by scoring.
```

### Pattern 3: Full Review (All Three Agents)

```
TOPOLOGY:
---------

  +---------------+    +---------------+    +-------------+
  | adv-selector  |--->| adv-executor  |--->| adv-scorer  |
  | (pick)        |    | (run each)    |    | (score)     |
  +---------------+    +---------------+    +-------------+

Use when: Full criticality-based review. Selector picks strategies,
executor runs them sequentially, scorer produces final assessment.
```

### P-003 Compliance Note

The MAIN CONTEXT (Claude session) orchestrates ALL agent sequences. Agents return their output; the orchestrator decides the next step. No agent invokes another agent.

---

## Quick Reference Card

| Workflow | Agents Used | Typical Duration | When to Use |
|----------|-------------|------------------|-------------|
| Quick score | adv-scorer | 1 invocation | Need quality number only |
| Steelman + Devil's Advocate | adv-executor (x2) | 2 invocations | H-16 canonical pairing |
| C2 standard review | adv-selector + adv-executor (x3-4) + adv-scorer | 5-6 invocations | Standard deliverables |
| C3 significant review | adv-selector + adv-executor (x6-10) + adv-scorer | 8-12 invocations | Major deliverables |
| C4 tournament | adv-selector + adv-executor (x9) + adv-scorer | 11 invocations | Irreversible decisions |

---

*Playbook Version: 1.0.0*
*Skill: adversary*
*Constitutional Compliance: Jerry Constitution v1.0*
*SSOT: `.context/rules/quality-enforcement.md`*
*Created: 2026-02-15*
