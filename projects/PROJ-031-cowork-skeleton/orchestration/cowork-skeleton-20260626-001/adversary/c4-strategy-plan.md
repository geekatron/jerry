---
name: c4-strategy-plan
version: "1.0.0"
created: "2026-06-26"
criticality: C4
target_score: 0.95
max_iterations: 10
plateau_threshold: 0.01
---

# C4 Adversarial Strategy Execution Plan

> **Project:** PROJ-031-cowork-skeleton
> **Deliverable Type:** Skeleton Framework Definition
> **Criticality Level:** C4 (Critical — Irreversible, Architecture/Governance)
> **Target Quality Score:** >= 0.95 weighted composite (S-014 LLM-as-Judge)
> **Quality Threshold (Minimum):** >= 0.92 per H-13
> **SSOT Reference:** `.context/rules/quality-enforcement.md`
> **Strategy Templates:** `.context/templates/adversarial/s-*.md`

## Document Sections

| Section | Purpose |
|---------|---------|
| [Criticality Assessment](#criticality-assessment) | C4 classification and auto-escalation rules applied |
| [Strategy Execution Plan](#strategy-execution-plan-ordered) | Ordered waves with dependency tracking and parallelism indicators |
| [Wave-by-Wave Breakdown](#wave-by-wave-breakdown) | Detailed execution sequence with strategy details |
| [H-16 Compliance](#h-16-compliance) | Steelman-before-Devil's-Advocate ordering verification |
| [Iteration Control](#iteration-control) | Minimum/maximum iterations, plateau detection, escalation criteria |
| [Quality Dimensions (S-014)](#quality-dimensions-s-014-rubric) | Scoring rubric applied at each iteration |
| [Execution Guardrails](#execution-guardrails) | Constitutional compliance, feedback routing, finding persistence |
| [Reusability & Cross-Session](#reusability--cross-session-persistence) | How this plan is invoked at each quality gate |

---

## Criticality Assessment

**Requested Level:** C4
**Auto-Escalation Applied:** No (C4 is already maximum criticality)
**Final Level:** C4

**Justification:** PROJ-031-cowork-skeleton defines a foundational framework for cooperative work management. This is:
- **Irreversible:** Framework architecture decisions cannot be easily reverted once adopted
- **Governance-Critical:** Establishes core patterns and constraints for all downstream projects
- **Public-Facing:** Skeleton framework serves as reference/template for other projects
- **Scope:** Affects >10 files across multiple domains (orchestration, agents, templates)
- **Impact:** Changes to skeleton propagate to all dependent projects

All 10 selected strategies are required per SSOT C4 row: {S-001, S-002, S-003, S-004, S-007, S-010, S-011, S-012, S-013, S-014}.

---

## Strategy Execution Plan (Ordered)

This plan executes all 10 required C4 strategies in a deterministic sequence respecting H-16 ordering constraints (Steelman before Devil's Advocate) and H-15 requirements (Self-Review first).

### Summary Table

| Wave | Order | Strategy ID | Strategy Name | Parallelism | Dependency | Template Path |
|------|-------|------------|---------------|-------------|-----------|---------------|
| 1 | 1 | S-010 | Self-Refine | sequential | None (First) | `.context/templates/adversarial/s-010-self-refine.md` |
| 2 | 2 | S-003 | Steelman Technique | sequential | After S-010 | `.context/templates/adversarial/s-003-steelman.md` |
| 3 | 3a | S-002 | Devil's Advocate | parallel | After S-003 (H-16) | `.context/templates/adversarial/s-002-devils-advocate.md` |
| 3 | 3b | S-004 | Pre-Mortem Analysis | parallel | After S-003 | `.context/templates/adversarial/s-004-pre-mortem.md` |
| 3 | 3c | S-001 | Red Team Analysis | parallel | After S-003 | `.context/templates/adversarial/s-001-red-team.md` |
| 4 | 4a | S-007 | Constitutional AI Critique | parallel | After Wave 3 | `.context/templates/adversarial/s-007-constitutional-ai.md` |
| 4 | 4b | S-011 | Chain-of-Verification | parallel | After Wave 3 | `.context/templates/adversarial/s-011-cove.md` |
| 5 | 5a | S-012 | FMEA | parallel | After Wave 4 | `.context/templates/adversarial/s-012-fmea.md` |
| 5 | 5b | S-013 | Inversion Technique | parallel | After Wave 4 | `.context/templates/adversarial/s-013-inversion.md` |
| 6 | 6 | S-014 | LLM-as-Judge | sequential | After Wave 5 (All) | `.context/templates/adversarial/s-014-llm-as-judge.md` |

---

## Wave-by-Wave Breakdown

### Wave 1: Self-Review (Sequential)

**Executor:** Creator (prior to adversaries)
**Purpose:** Early self-correction reduces reviewer burden per H-15
**Timing:** Immediate (before adversarial reviews begin)

#### S-010: Self-Refine

| Property | Value |
|----------|-------|
| **Strategy ID** | S-010 |
| **Name** | Self-Refine |
| **Template** | `.context/templates/adversarial/s-010-self-refine.md` |
| **Evaluates** | Creator's output for obvious defects, completeness gaps, clarity issues |
| **Parallelism** | Sequential (must be first) |
| **Dependency** | None (first) |
| **Findings Route To** | CREATOR (for immediate revision before adversaries run) |
| **Evidence** | Self-review critique with specific improvement areas |
| **Duration Estimate** | 5-10 minutes (creator time) |

**Order Rank:** 1 (absolute first)

---

### Wave 2: Strengthen (Sequential)

**Executor:** Adversary agent (adv-executor via S-003 template)
**Purpose:** Strengthen the best version of the argument per H-16 (steelman before critique)
**Timing:** After S-010 completes

#### S-003: Steelman Technique

| Property | Value |
|----------|-------|
| **Strategy ID** | S-003 |
| **Name** | Steelman Technique |
| **Template** | `.context/templates/adversarial/s-003-steelman.md` |
| **Evaluates** | Most charitable interpretation of each design claim; identifies strongest counter-arguments implicitly |
| **Parallelism** | Sequential (must precede S-002 per H-16) |
| **Dependency** | After S-010 |
| **Findings Route To** | ORIGINAL CREATOR (not used for immediate revision; input to S-002 and later strategies) |
| **Evidence** | Strengthened argument, best-case scenarios, strongest possible positions |
| **Duration Estimate** | 10-15 minutes (agent time) |

**Order Rank:** 2 (second, must precede all critique)

**H-16 Compliance Statement:** S-003 is positioned at Wave 2, Order 2. S-002 (Devil's Advocate) is positioned at Wave 3, Order 3a. S-003 position (2) < S-002 position (3a). **H-16 constraint SATISFIED.**

---

### Wave 3: Challenge (Parallel)

**Executor:** Adversary agents (adv-executor via S-002, S-004, S-001 templates)
**Purpose:** Challenge assumptions, anticipate failures, explore vulnerabilities
**Timing:** After Wave 2 (S-003) completes

#### S-002: Devil's Advocate

| Property | Value |
|----------|-------|
| **Strategy ID** | S-002 |
| **Name** | Devil's Advocate |
| **Template** | `.context/templates/adversarial/s-002-devils-advocate.md` |
| **Evaluates** | Counter-arguments, assumptions challenged, potential weaknesses, claim support |
| **Parallelism** | Parallel within Wave 3 (with S-001, S-004) |
| **Dependency** | After S-003 (H-16 HARD constraint) |
| **Findings Route To** | ORIGINAL CREATOR |
| **Evidence** | Identified weaknesses, unsupported assumptions, alternative interpretations |
| **Duration Estimate** | 10-15 minutes (agent time) |

**Order Rank:** 3a

#### S-004: Pre-Mortem Analysis

| Property | Value |
|----------|-------|
| **Strategy ID** | S-004 |
| **Name** | Pre-Mortem Analysis |
| **Template** | `.context/templates/adversarial/s-004-pre-mortem.md` |
| **Evaluates** | Potential failure modes if implemented as designed; assumes current plan has failed, works backward to identify causes |
| **Parallelism** | Parallel within Wave 3 (with S-002, S-001) |
| **Dependency** | After S-003 (can run concurrently with S-002, S-001) |
| **Findings Route To** | ORIGINAL CREATOR |
| **Evidence** | Failure scenarios, root causes of hypothetical failures, prevention strategies |
| **Duration Estimate** | 10-15 minutes (agent time) |

**Order Rank:** 3b

#### S-001: Red Team Analysis

| Property | Value |
|----------|-------|
| **Strategy ID** | S-001 |
| **Name** | Red Team Analysis |
| **Template** | `.context/templates/adversarial/s-001-red-team.md` |
| **Evaluates** | Adversarial attack surface, vulnerabilities, exploitation paths, defensive gaps |
| **Parallelism** | Parallel within Wave 3 (with S-002, S-004) |
| **Dependency** | After S-003 (can run concurrently with S-002, S-004) |
| **Findings Route To** | ORIGINAL CREATOR |
| **Evidence** | Attack vectors, vulnerability evidence, exploitation scenarios, mitigation recommendations |
| **Duration Estimate** | 10-15 minutes (agent time) |

**Order Rank:** 3c

---

### Wave 4: Verify (Parallel)

**Executor:** Adversary agents (adv-executor via S-007, S-011 templates)
**Purpose:** Verify constitutional compliance and systematic claim validation
**Timing:** After Wave 3 (Challenge group) completes

#### S-007: Constitutional AI Critique

| Property | Value |
|----------|-------|
| **Strategy ID** | S-007 |
| **Name** | Constitutional AI Critique |
| **Template** | `.context/templates/adversarial/s-007-constitutional-ai.md` |
| **Evaluates** | Compliance with Jerry Constitution (P-001 through P-022); governance consistency; principle violations |
| **Parallelism** | Parallel within Wave 4 (with S-011) |
| **Dependency** | After Wave 3 |
| **Findings Route To** | ORIGINAL CREATOR |
| **Evidence** | Constitutional principle citations, violation evidence, remediation guidance |
| **Duration Estimate** | 10-15 minutes (agent time) |

**Order Rank:** 4a

**H-18 Note:** S-007 is required for all C2+ deliverables per H-18. At C4, it is REQUIRED.

#### S-011: Chain-of-Verification

| Property | Value |
|----------|-------|
| **Strategy ID** | S-011 |
| **Name** | Chain-of-Verification |
| **Template** | `.context/templates/adversarial/s-011-cove.md` |
| **Evaluates** | Systematic verification of each claim; evidence sufficiency; citation chains; gap identification |
| **Parallelism** | Parallel within Wave 4 (with S-007) |
| **Dependency** | After Wave 3 |
| **Findings Route To** | ORIGINAL CREATOR |
| **Evidence** | Claim verification matrices, evidence chains, gaps in citation, unsubstantiated assertions |
| **Duration Estimate** | 10-15 minutes (agent time) |

**Order Rank:** 4b

---

### Wave 5: Decompose (Parallel)

**Executor:** Adversary agents (adv-executor via S-012, S-013 templates)
**Purpose:** Systematic decomposition of design via failure mode and inversion analysis
**Timing:** After Wave 4 (Verify group) completes

#### S-012: FMEA (Failure Mode and Effects Analysis)

| Property | Value |
|----------|-------|
| **Strategy ID** | S-012 |
| **Name** | FMEA |
| **Template** | `.context/templates/adversarial/s-012-fmea.md` |
| **Evaluates** | Failure modes for each component/interface; effects, severity, occurrence, detection ratings; RPN (Risk Priority Number) calculation |
| **Parallelism** | Parallel within Wave 5 (with S-013) |
| **Dependency** | After Wave 4 |
| **Findings Route To** | ORIGINAL CREATOR |
| **Evidence** | Failure mode matrices, RPN scores, high-risk items, mitigation recommendations |
| **Duration Estimate** | 15-20 minutes (agent time) |

**Order Rank:** 5a

#### S-013: Inversion Technique

| Property | Value |
|----------|-------|
| **Strategy ID** | S-013 |
| **Name** | Inversion Technique |
| **Template** | `.context/templates/adversarial/s-013-inversion.md` |
| **Evaluates** | Inverts each design principle, constraint, and assumption to identify blind spots; "what if opposite is true?" analysis |
| **Parallelism** | Parallel within Wave 5 (with S-012) |
| **Dependency** | After Wave 4 |
| **Findings Route To** | ORIGINAL CREATOR |
| **Evidence** | Inverted principles, opposite assumptions, blind spot identification, overlooked scenarios |
| **Duration Estimate** | 10-15 minutes (agent time) |

**Order Rank:** 5b

---

### Wave 6: Quality Scoring (Sequential)

**Executor:** Scoring agent (adv-scorer via S-014 template)
**Purpose:** Aggregate all findings; produce final weighted composite quality score
**Timing:** After Wave 5 (all strategy findings) complete

#### S-014: LLM-as-Judge

| Property | Value |
|----------|-------|
| **Strategy ID** | S-014 |
| **Name** | LLM-as-Judge |
| **Template** | `.context/templates/adversarial/s-014-llm-as-judge.md` |
| **Evaluates** | All 6 quality dimensions (Completeness, Internal Consistency, Methodological Rigor, Evidence Quality, Actionability, Traceability) based on findings from all 9 prior strategies |
| **Parallelism** | Sequential (must be last) |
| **Dependency** | After Wave 5 (all strategies) |
| **Findings Route To** | ORIGINAL CREATOR (score + dimension breakdown + improvement guidance) |
| **Evidence** | Weighted composite score (0.0–1.0), per-dimension scores, evidence from all 9 strategies, leniency-bias counteraction |
| **Duration Estimate** | 20-30 minutes (agent time) |

**Order Rank:** 6 (absolute last)

**H-17 Note:** S-014 scoring is required for all C2+ deliverables per H-17. At C4, it is REQUIRED and ALWAYS LAST.

---

## H-16 Compliance

**HARD Rule H-16:** Steelman (S-003) MUST be applied before Devil's Advocate (S-002).

| Check | Result |
|-------|--------|
| S-003 ordered before S-002? | YES — S-003 at Wave 2, Order 2; S-002 at Wave 3, Order 3a |
| S-003 execution completes before S-002 starts? | YES — Sequential waves enforce execution order |
| No Devil's Advocate findings precede Steelman review? | YES — All Wave 3 strategies run AFTER S-003 completes |

**H-16 COMPLIANCE: SATISFIED**

---

## Iteration Control

### Iteration Bounds

| Parameter | Value | Source | Rationale |
|-----------|-------|--------|-----------|
| **Minimum Iterations** | 3 | H-14 | Creator-critic-revision cycle REQUIRED minimum |
| **Maximum Iterations (C4)** | 10 | RT-M-010, quality-enforcement.md | Criticality-proportional ceiling |
| **Target Score** | >= 0.95 | User specification | Project-specific excellence target (above 0.92 gate) |
| **Gate Threshold** | >= 0.92 | H-13 | Weighted composite quality score minimum |

### Plateau Detection (Circuit Breaker)

| Condition | Threshold | Action |
|-----------|-----------|--------|
| Score delta < 0.01 | 3 consecutive iterations | Circuit breaker activates; halt iteration and escalate to user |
| Iteration count reaches max | 10 iterations | Halt regardless of score; present best result to user |
| Critical findings (Quality Band: REJECTED) | < 0.85 score | May require significant rework instead of targeted iteration |

**Scoring Bands:**

| Band | Score Range | Outcome | Workflow |
|------|------------|---------|----------|
| PASS | >= 0.92 | Meets quality gate | Deliverable acceptable |
| PASS+ (Excellent) | >= 0.95 | Exceeds target (project-specific) | Premium quality achieved |
| REVISE | 0.85-0.91 | Rejected (H-13), near threshold | Targeted revision likely sufficient |
| REJECTED | < 0.85 | Rejected (H-13), significant rework | Major structural issues |

### Iteration Workflow

```
Iteration 1:
  1. Creator produces deliverable
  2. Creator runs S-010 (self-refine)
  3. Adversaries run Wave 1-5 (S-001, S-002, S-003, S-004, S-007, S-011, S-012, S-013)
  4. Scorer runs S-014 (LLM-as-Judge)
  5. Score returned to creator

If score >= 0.95:
  → DELIVERABLE ACCEPTED (exceeds target)
Else if score >= 0.92:
  → DELIVERABLE PASSES (meets gate)
Else if score >= 0.85:
  → REVISE BAND: Creator revises based on S-014 dimension breakdown
  → Go to Iteration 2
Else if score < 0.85:
  → REJECTED BAND: Creator performs major rework
  → Go to Iteration 2

Iteration 2, 3, ... N:
  1. Creator revises deliverable based on prior S-014 findings + dimension breakdown
  2. Creator runs S-010 (self-refine) on revised version
  3. Adversaries re-run Wave 1-5 (findings compared to prior iteration)
  4. Scorer runs S-014 with prior iteration score in context
  5. Score returned to creator
  6. Check plateau: if Δ < 0.01 for 3 consecutive iterations → escalate to user
  7. Check ceiling: if iteration == 10 and score < 0.92 → escalate to user
  8. If score >= 0.92 → PASS; if score >= 0.95 → PASS+ (premium)

Plateau Escalation (iteration N+2, Δ < 0.01 × 3):
  → Present current best score + findings to user
  → Inform user that improvement has plateaued
  → Ask user: (A) accept current score, (B) provide explicit guidance for next round, (C) redesign required

Max Iteration Escalation (iteration 10, score < 0.92):
  → Present best score achieved
  → Inform user that max 10 iterations reached
  → Ask user: (A) accept current deliverable, (B) pause and redesign approach, (C) continue with explicit acknowledgment of quality concerns
```

---

## Quality Dimensions (S-014 Rubric)

The LLM-as-Judge (S-014) evaluates all deliverables against a 6-dimension weighted rubric:

| # | Dimension | Weight | Definition | Evaluation Criteria |
|---|-----------|--------|-----------|---------------------|
| 1 | **Completeness** | 0.20 (20%) | All required elements present; no major gaps or TODOs | Checklist of required sections met; all promised deliverables included |
| 2 | **Internal Consistency** | 0.20 (20%) | No contradictions; terminology consistent; assumptions aligned | Cross-references valid; no conflicting statements; definitions stable |
| 3 | **Methodological Rigor** | 0.20 (20%) | Framework/methodology correctly applied; process evident | Steps traceable; methodology citations present; reasoning transparent |
| 4 | **Evidence Quality** | 0.15 (15%) | Claims supported by evidence; citations present; sources credible | Evidence specificity; chain-of-evidence present; source authority |
| 5 | **Actionability** | 0.15 (15%) | Deliverable enables downstream decisions/actions; guidance clear | Next steps specified; success criteria defined; ambiguity minimized |
| 6 | **Traceability** | 0.10 (10%) | Origin of claims traceable; source citations; decision rationale | Audit trail present; cross-references work; upstream decisions documented |

**Scoring Guidance:**

- **Score Range:** 0.0–1.0 (0%–100%)
- **Per-Dimension Scoring:** Each dimension scored 0–1.0 independently
- **Weighted Composite:** `final_score = Σ(dimension_score × weight)`
- **Leniency Bias Counteraction:** When uncertain between adjacent score levels, select the lower score; bias towards rigor
- **Anti-Leniency Statement Required:** S-014 MUST include explicit assertion: "This score reflects strict application of rubric without leniency bias. When dimension evidence was ambiguous, the lower score was selected."

---

## Execution Guardrails

### Constitutional Compliance (P-001 through P-022)

All adversarial agents operate under these constraints:

| Principle | Constraint | Consequence |
|-----------|-----------|-------------|
| **P-003** | No recursive subagents; max 1-level nesting (orchestrator → worker) | Uncontrolled token consumption; agent hierarchy collapse |
| **P-020** | Never override user intent; ask before destructive operations | Unauthorized changes; trust erosion |
| **P-022** | Never deceive about actions, capabilities, or confidence levels | Governance undermined; quality assessment invalidated |
| **P-002** | All findings MUST be persisted to project files; never leave in transient context | Context rot vulnerability; session compaction loss |
| **P-004** | Never omit strategy IDs, template paths, or evidence citations | Untraceable decisions; audit trail broken |
| **P-011** | Never make findings without tying them to specific deliverable evidence | Unsupported recommendations; confidence inflated |

### Finding Routing

All findings from Waves 1-5 (S-010 through S-013) MUST route to the **ORIGINAL CREATOR**, not to the orchestrator. The creator uses findings to revise the deliverable for the next iteration.

- **S-010 findings:** Creator self-identifies defects and corrects immediately (pre-adversary)
- **S-002, S-003, S-004, S-001 findings:** Routed to creator (improvement suggestions for next iteration)
- **S-007 findings:** Routed to creator (constitutional compliance gaps for next iteration)
- **S-011 findings:** Routed to creator (verification gaps for next iteration)
- **S-012 findings:** Routed to creator (failure modes for next iteration)
- **S-013 findings:** Routed to creator (blind spots for next iteration)
- **S-014 findings:** Routed to creator (score + dimension breakdown + guidance for next iteration)

**Orchestrator role:** Track iteration count, manage circuit breaker logic, escalate when plateau or max iterations reached.

### Evidence Persistence

All strategy-specific findings MUST be written to project files with the following structure:

```
projects/PROJ-031-cowork-skeleton/orchestration/cowork-skeleton-20260626-001/
├── adversary/
│   ├── c4-strategy-plan.md                          (this file)
│   ├── iteration-001/
│   │   ├── s-010-self-refine-findings.md
│   │   ├── s-003-steelman-findings.md
│   │   ├── s-002-devils-advocate-findings.md
│   │   ├── s-004-pre-mortem-findings.md
│   │   ├── s-001-red-team-findings.md
│   │   ├── s-007-constitutional-ai-findings.md
│   │   ├── s-011-cove-findings.md
│   │   ├── s-012-fmea-findings.md
│   │   ├── s-013-inversion-findings.md
│   │   ├── s-014-quality-score.md                   (score + dimension breakdown)
│   │   └── ITERATION_SUMMARY.md                     (iteration metadata)
│   ├── iteration-002/
│   │   └── (same structure; repeat as needed)
│   └── ...
```

Each findings file MUST include:
- Strategy ID + name + template path
- Summary of findings (key bullets)
- Evidence citations (specific deliverable locations)
- Actionable remediation suggestions
- Iteration number and timestamp
- Leniency bias check (for S-014 only)

---

## Reusability & Cross-Session Persistence

This strategy selection plan (c4-strategy-plan.md) is the **canonical reference** for all C4 quality gates applied to PROJ-031-cowork-skeleton deliverables.

### Invocation Protocol

Every time a C4 deliverable quality gate is triggered:

1. **Load this plan:** Read `c4-strategy-plan.md` to understand the strategy set and ordering
2. **Invoke adv-selector:** Confirm criticality level and strategy set mapping (should always be C4 → all 10 strategies)
3. **Invoke adv-executor:** Run strategies in Wave order (1→2→3→4→5)
4. **Invoke adv-scorer:** Run S-014 (Wave 6)
5. **Track iteration:** Create `iteration-NNN/` directory; persist all findings
6. **Check circuit breaker:** Plateau detection (Δ < 0.01 × 3 iterations) or max iterations (10) reached
7. **Escalate if needed:** If plateau or max reached, inform user with best score and findings; request explicit guidance

### Cross-Session Continuity

The plan persists across sessions via file storage:
- **Session 1:** Creator writes initial deliverable; quality gate runs iterations 1-3
- **Session 2:** Creator continues from `iteration-003/`; reads prior findings; resumes iteration 4+
- All prior iteration findings remain accessible in project files (not lost to session compaction)

This plan can be reused for:
- Initial deliverable quality gate (C4)
- Mid-project revision quality gates (C4)
- Final delivery quality verification (C4)
- Any new C4 deliverable for the same project (reuse structure, adjust deliverable path)

---

## References

| Source | Content | Location |
|--------|---------|----------|
| **SSOT** | Quality enforcement, criticality levels, strategy catalog, quality gate thresholds, dimensions, weights | `.context/rules/quality-enforcement.md` |
| **Skill Definition** | Adversary skill capabilities, agents, integration points | `skills/adversary/SKILL.md` |
| **Strategy Templates** | Execution templates for all 10 selected strategies | `.context/templates/adversarial/s-*.md` |
| **Constitutional Principles** | Governance constraints (P-001 through P-022) | `docs/governance/JERRY_CONSTITUTION.md` |
| **Criticality Levels** | Mapping of C1-C4 to strategy sets, enforcement tiers, auto-escalation rules | `.context/rules/quality-enforcement.md` § Criticality Levels |
| **H-16 Specification** | Steelman-before-Devil's-Advocate ordering constraint | `.context/rules/quality-enforcement.md` § HARD Rule Index |
| **Quality Gate Rubric** | 6-dimension weighted scoring for S-014 LLM-as-Judge | `.context/rules/quality-enforcement.md` § Quality Gate |
| **Iteration Bounds** | Minimum/maximum iteration ceilings by criticality, plateau detection | `agent-development-standards.md` § RT-M-010, quality-enforcement.md |

---

## Footer

**Plan Version:** 1.0.0
**Created:** 2026-06-26
**Criticality:** C4 (Critical)
**Target Quality Score:** >= 0.95
**Quality Gate Threshold:** >= 0.92
**Max Iterations:** 10
**Plateau Threshold (Circuit Breaker):** Δ < 0.01 × 3 consecutive iterations
**Strategy Set:** All 10 selected (C4 requirement; no optional strategies)
**H-16 Compliance:** SATISFIED (S-003 before S-002)
**SSOT Reference:** `.context/rules/quality-enforcement.md`
**Agent Architecture Compliance:** P-003 (single-level orchestrator → workers)
**Persistence Guarantee:** P-002 (all findings to project files)

**Next Step:** Invoke adv-selector to confirm criticality assessment and strategy set, then proceed to Wave 1 (S-010 Self-Refine).

---

*Canonical C4 Strategy Plan — PROJ-031-cowork-skeleton*
*Reusable at every C4 quality gate; cross-session persistent*
*Agent: adv-selector (strategy selection and planning)*
*Generated per quality-enforcement.md § Implementation*
