# TASK-006: PLAYBOOK.md Update Content for Adversarial Workflows

<!--
DOCUMENT-ID: FEAT-004:EN-304:TASK-006
VERSION: 1.0.0
AGENT: ps-architect-304 (creator)
DATE: 2026-02-13
STATUS: Draft
PARENT: EN-304 (Problem-Solving Skill Enhancement)
FEATURE: FEAT-004 (Adversarial Strategy Research & Skill Enhancement)
EPIC: EPIC-002 (Quality Framework Enforcement)
PROJECT: PROJ-001-oss-release
ACTIVITY: DOCUMENTATION
INPUT: TASK-001 (requirements), TASK-002 (mode design), TASK-003 (invocation protocol), TASK-004 (agent spec), TASK-005 (SKILL.md updates)
-->

> **Version:** 1.0.0
> **Agent:** ps-architect-304
> **Quality Target:** >= 0.92
> **Purpose:** Define the content updates for `skills/problem-solving/PLAYBOOK.md` to include adversarial workflow procedures -- when to invoke each mode, how to interpret results, how to integrate the creator-critic-revision cycle with adversarial strategies. This document specifies WHAT to add; it does NOT modify PLAYBOOK.md directly.

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What this document delivers |
| [Version Change](#version-change) | PLAYBOOK.md version bump |
| [Pattern 6 Updates](#pattern-6-updates) | Updated Generator-Critic Loop with adversarial integration |
| [New Pattern: Adversarial Review Pipeline](#new-pattern-adversarial-review-pipeline) | Complete adversarial workflow procedure |
| [New Pattern: Criticality-Driven Review](#new-pattern-criticality-driven-review) | C1-C4 decision workflow |
| [New Section: Mode Invocation Guide](#new-section-mode-invocation-guide) | When to invoke each mode with decision criteria |
| [New Section: Interpreting Adversarial Results](#new-section-interpreting-adversarial-results) | How to read and act on mode outputs |
| [New Section: Creator-Critic-Revision Cycle](#new-section-creator-critic-revision-cycle) | Full lifecycle procedure with adversarial integration |
| [New Section: Escalation Procedures](#new-section-escalation-procedures) | When and how to escalate to human review |
| [Updated Section: Circuit Breaker](#updated-section-circuit-breaker) | Updated thresholds for adversarial mode |
| [Traceability](#traceability) | Mapping to TASK-001 requirements |
| [References](#references) | Source citations |

---

## Summary

This document specifies the content to be added to `skills/problem-solving/PLAYBOOK.md` (currently v3.3.0) to include adversarial workflow procedures. The current PLAYBOOK.md documents the Generator-Critic Loop (Pattern 6) with a circuit breaker threshold of 0.85 and no adversarial strategy guidance. After this update, the playbook will provide:

- An updated Pattern 6 with adversarial mode integration
- Two new patterns: Adversarial Review Pipeline and Criticality-Driven Review
- A mode invocation guide explaining when to use each of the 10 modes
- Result interpretation guidance for each mode's output
- A complete creator-critic-revision cycle procedure
- Escalation procedures for human involvement

---

## Version Change

| Attribute | Current | Updated |
|-----------|---------|---------|
| PLAYBOOK.md version | 3.3.0 | 4.0.0 |

---

## Pattern 6 Updates

### Current Pattern 6: Generator-Critic Loop

The current PLAYBOOK.md documents Pattern 6 with these parameters:
- Circuit breaker: max 3 iterations, threshold 0.85
- No adversarial mode awareness
- No criticality-based strategy selection

### Updated Pattern 6: Generator-Critic Loop (with Adversarial Integration)

**Replace the existing Pattern 6 content with:**

```markdown
## Pattern 6: Generator-Critic Loop

### Overview

The Generator-Critic Loop is the core iterative refinement pattern in /problem-solving.
A generator agent (e.g., ps-architect, ps-researcher) produces an artifact, and
the ps-critic agent evaluates it against quality criteria. The loop repeats until
the quality gate is met or the circuit breaker trips.

### Standard Mode (Backward Compatible)

When no adversarial context is provided:
- **Threshold:** 0.85
- **Max iterations:** 3
- **Criteria:** Default quality dimensions (Completeness, Accuracy, Clarity, Actionability, Alignment)
- **Behavior:** Identical to PLAYBOOK.md v3.3.0

### Adversarial Mode (New in v4.0.0)

When adversarial context is provided (explicitly or via automatic detection):
- **Threshold:** 0.92 (HARD rule H-13, sourced from quality-enforcement.md SSOT)
- **Min iterations:** 3 (HARD rule H-14)
- **Criteria:** Mode-specific evaluation criteria (see TASK-002 mode definitions)
- **Strategy selection:** Based on criticality level (C1-C4) per EN-303 decision tree
- **Scoring:** S-014 LLM-as-Judge with anti-leniency calibration (HARD rule H-16)

### Loop Flow

```
Orchestrator (main context):
  |
  +-- Iteration 1: CREATE
  |     Generator agent creates initial artifact
  |     Creator applies S-010 self-refine during creation
  |
  +-- Iteration 2: CRITIQUE
  |     Orchestrator invokes ps-critic with adversarial context
  |     ps-critic executes mode pipeline per criticality level
  |     ps-critic returns: quality score, findings, recommendations
  |
  +-- Iteration 3: REVISE + VERIFY
  |     Generator revises artifact based on critique
  |     Orchestrator invokes ps-critic for verification
  |     ps-critic applies S-014 scoring + S-011 verification
  |
  +-- Decision:
        IF score >= threshold (0.92 adversarial, 0.85 standard): ACCEPT
        ELIF iteration >= max AND score >= 0.85: ACCEPT_WITH_CAVEATS
        ELIF no improvement for 2 consecutive: PLATEAU -> ESCALATE
        ELSE: Additional iteration (if budget allows)
```

### Circuit Breaker Parameters

| Parameter | Standard Mode | Adversarial Mode |
|-----------|--------------|------------------|
| Max iterations | 3 | 3 (minimum per H-14) |
| Acceptance threshold | 0.85 | 0.92 (H-13) |
| Improvement threshold | 0.10 | 0.05 |
| Plateau detection | 2 consecutive | 2 consecutive |
| Plateau action | Accept with caveats | Escalate to user (P-020) |
```

---

## New Pattern: Adversarial Review Pipeline

**Location:** After Pattern 6 (or as a new Pattern 7).

### Content

```markdown
## Pattern 7: Adversarial Review Pipeline

### When to Use

Use the Adversarial Review Pipeline when:
- The artifact requires review at C2+ criticality
- Multiple adversarial strategies should be applied in sequence
- Quality gate of >= 0.92 must be met
- The orchestration plan specifies adversarial review as a phase

### Procedure

**Step 1: Determine Criticality**

| Signal | Criticality |
|--------|-------------|
| Routine code, documentation | C1 |
| New feature, interface change, refactoring | C2 |
| Architecture decision, cross-boundary change, ADR | C3 |
| Constitutional amendment, irreversible decision | C4 |
| Modifies JERRY_CONSTITUTION.md | Auto-escalate to C3+ |
| Modifies .claude/rules/ | Auto-escalate to C3+ |
| Modifies baselined ADR | Auto-escalate to C4 |

**Step 2: Select Pipeline**

| Criticality | Pipeline |
|-------------|----------|
| C1 | `self-refine` |
| C2 | `steelman` -> `constitutional` -> `devils-advocate` -> `llm-as-judge` |
| C3 | `steelman` -> `inversion` -> `constitutional` -> `devils-advocate` -> `pre-mortem` -> `fmea` -> `llm-as-judge` |
| C4 | All 10 modes (see canonical C4 pipeline in SKILL.md) |

**Step 3: Execute Pipeline**

Invoke ps-critic with the selected pipeline:

```yaml
# Example: C3 adversarial review
PS CONTEXT:
  PS ID: epic-002
  Entry ID: e-304
  Iteration: 2
  Artifact: projects/PROJ-001/decisions/ADR-003.md
  Generator: ps-architect

ADVERSARIAL CONTEXT:
  Mode: auto
  Criticality: C3
  Phase: PH-DESIGN
  Target Type: TGT-DEC
  Maturity: MAT-DRAFT
  Team: TEAM-MULTI
  Enforcement: ENF-FULL
  Platform: PLAT-CC
  Token Budget: TOK-FULL
```

**Step 4: Process Results**

See "Interpreting Adversarial Results" section below.

**Step 5: Iterate or Accept**

Follow the circuit breaker logic from Pattern 6 (adversarial mode).

### Anti-Patterns

| Anti-Pattern | Why It Fails | Correct Approach |
|-------------|-------------|------------------|
| Running C4 pipeline for routine code | Wastes ~50,000 tokens on low-risk work | Use C1 (self-refine only) |
| Skipping steelman before devils-advocate | DA attacks strawman, producing false positives | Always run steelman first (SEQ-001) |
| Running llm-as-judge first | No adversarial findings to inform scoring | Judge should be last (SEQ-003) |
| Ignoring TEAM-SINGLE constraints at C3+ | Single-agent DA is weak | Escalate to TEAM-MULTI or TEAM-HIL |
| Accepting score > 0.92 without anti-leniency check | Leniency bias produces inflated scores | Always verify H-16 compliance |
```

---

## New Pattern: Criticality-Driven Review

**Location:** After Pattern 7.

### Content

```markdown
## Pattern 8: Criticality-Driven Review

### When to Use

Use Criticality-Driven Review when you need to determine the appropriate
level of adversarial scrutiny for an artifact. This pattern implements
the EN-303 decision tree in a human-friendly procedure.

### Decision Procedure

```
START
  |
  +-- Is the artifact modifying governance files?
  |     (JERRY_CONSTITUTION.md, .claude/rules/*, baselined ADRs)
  |     YES -> C3 minimum (C4 if baselined ADR) -> Go to C3/C4 pipeline
  |     NO  -> Continue
  |
  +-- Is this an architecture decision or new ADR?
  |     YES -> C3 minimum -> Go to C3 pipeline
  |     NO  -> Continue
  |
  +-- Is this a new feature or non-trivial change?
  |     YES -> C2 -> Go to C2 pipeline
  |     NO  -> Continue
  |
  +-- Is this routine work (standard code, docs, config)?
        YES -> C1 -> Go to C1 pipeline
```

### Phase Adjustments

After determining base criticality, adjust for phase:

| Phase | C1 | C2 | C3 | C4 |
|-------|----|----|----|----|
| PH-EXPLORE | Keep C1 | Downgrade to C1 (unless auto-escalated) | Downgrade to C2 (unless auto-escalated) | Downgrade to C3 (unless auto-escalated) |
| PH-DESIGN | Keep C1 | Full C2 | Full C3 | Full C4 |
| PH-IMPL | Keep C1 | Full C2 | C3 minus pre-mortem | Full C4 |
| PH-VALID | S-014 only | S-007 + S-014 | S-007 + S-014 + S-011 + S-012 | Full C4 |
| PH-MAINT | S-010 + S-014 | S-007 + S-014 | S-007 + S-014 + S-012 + S-011 | Full C4 (if scope warrants) |

**CRITICAL: PR-001 Precedence Rule.** If criticality was auto-escalated (AE-001 through AE-005), phase modifiers CANNOT reduce it below the escalated level. This protects governance reviews from being downgraded by phase convenience.
```

---

## New Section: Mode Invocation Guide

**Location:** After the patterns section.

### Content

```markdown
## Mode Invocation Guide

### When to Use Each Mode

| Mode | Use When | Do NOT Use When |
|------|----------|-----------------|
| `self-refine` | Creator wants to improve before external critique; first step in any review cycle | Validation phase (scoring preferred); as substitute for external critique |
| `steelman` | About to run adversarial challenge (DA, constitutional, red-team); reviewing arguments or decisions | Pure code review (no arguments); early exploration (no argument formed) |
| `inversion` | Starting design review; need failure criteria; need anti-pattern checklist | Validation phase (adds noise); artifact already baselined |
| `constitutional` | Code review; checking standards compliance; any C2+ review | Early exploration (no standards yet); no codified rules exist |
| `devils-advocate` | Challenging design decisions; reviewing architecture; testing assumptions | C1 routine work; without prior steelman; TEAM-SINGLE (use self-refine instead) |
| `pre-mortem` | Architecture decisions; process designs; planning phase | Implementation phase (too late); routine code changes |
| `fmea` | System design; process definitions; any artifact with enumerable components | Early exploration (insufficient detail); pure research documents |
| `chain-of-verification` | Research documents; requirements with factual claims; documentation | Architecture (few factual claims); pure code |
| `llm-as-judge` | Quality gate evaluation; scoring; any C2+ final assessment | Early exploration (no rubric); as sole strategy (combine with others) |
| `red-team` | Security review; architecture review; C3-C4 governance review | C1-C2 routine work; early exploration (premature pressure) |

### Mode Selection Quick Reference

**"I need to review code"** -> `constitutional` + `llm-as-judge` (C2) or + `fmea` + `inversion` (C3)

**"I need to review an ADR"** -> `steelman` + `constitutional` + `devils-advocate` + `pre-mortem` + `llm-as-judge` (C3)

**"I need to check if claims are correct"** -> `chain-of-verification`

**"I need to find security issues"** -> `red-team` + `inversion` + `constitutional`

**"I need a quality score"** -> `llm-as-judge` (always include anti-leniency calibration)

**"I need to find how this could fail"** -> `pre-mortem` + `fmea` + `inversion`
```

---

## New Section: Interpreting Adversarial Results

**Location:** After the Mode Invocation Guide.

### Content

```markdown
## Interpreting Adversarial Results

### Understanding Mode Outputs

Each adversarial mode produces a specific type of output. Here is how to interpret and act on each:

#### `self-refine` Output

**Contains:** Issue list with locations, descriptions, and revision recommendations.
**Action:** Creator addresses issues in priority order. Focus on HIGH priority items first.
**Success indicator:** Issue count decreases across iterations.

#### `steelman` Output

**Contains:** Reconstructed argument, explicit assumptions, strongest reasoning chain.
**Action:** Review the steelmanned version. If it differs significantly from the original, the original's argument was weak. Use the steelmanned version as the basis for subsequent adversarial challenge.
**Success indicator:** Subsequent adversarial modes (DA, constitutional) find fewer issues.

#### `inversion` Output

**Contains:** Anti-pattern checklist, inverted success criteria, blind spot analysis.
**Action:** Check the artifact against each anti-pattern. Any match is a defect. Persist the checklist for future reviews of similar artifacts.
**Success indicator:** Zero anti-pattern matches in the artifact.

#### `constitutional` Output

**Contains:** Principle-by-principle compliance report (PASS/PARTIAL/FAIL per rule).
**Action:** Fix all HARD rule FAIL violations immediately (these block quality gate). Address PARTIAL violations. SOFT violations are advisory.
**Success indicator:** All HARD rules PASS. All MEDIUM rules PASS or have documented waivers.

#### `devils-advocate` Output

**Contains:** Challenged assumptions, challenged decisions with alternatives, robustness assessment.
**Action:** For each challenge: if the alternative is stronger, revise the decision. If the original withstands challenge, document the robustness evidence.
**Success indicator:** Most decisions survive challenge with documented evidence.

#### `pre-mortem` Output

**Contains:** Failure narratives, root causes traced to artifact, risk matrix, preventive measures.
**Action:** Add preventive measures for high-probability/high-severity scenarios. Document accepted risks for lower-severity scenarios.
**Success indicator:** All high-severity scenarios have mitigations.

#### `fmea` Output

**Contains:** FMEA table with S/O/D/RPN ratings, critical items (RPN > 200).
**Action:** Address all RPN > 200 items. Review all Severity >= 8 items. Mitigations should reduce O or D ratings.
**Success indicator:** No items with RPN > 200 after revision.

#### `chain-of-verification` Output

**Contains:** Claim inventory, verification status per claim, contradicted claims with corrections.
**Action:** Fix all CONTRADICTED claims. Flag UNVERIFIED claims for human verification. Remove or caveat claims that cannot be verified.
**Success indicator:** Zero CONTRADICTED claims. All claims VERIFIED or explicitly flagged as UNVERIFIED.

#### `llm-as-judge` Output

**Contains:** Quality score (0.00-1.00), dimension breakdown, pass/fail, improvement areas.
**Action:** If score >= 0.92: ACCEPT. If < 0.92: address improvement areas in priority order.
**Success indicator:** Score >= 0.92 with anti-leniency calibration confirmed.

#### `red-team` Output

**Contains:** Attack surface analysis, vulnerability report, critical vulnerabilities, defense recommendations.
**Action:** Implement defenses for all critical vulnerabilities. Document residual risks for lower-severity findings.
**Success indicator:** No critical vulnerabilities without defenses.
```

---

## New Section: Creator-Critic-Revision Cycle

**Location:** After "Interpreting Adversarial Results."

### Content

```markdown
## Creator-Critic-Revision Cycle (Adversarial)

### Minimum 3-Iteration Cycle (HARD Rule H-14)

Every adversarial review MUST include at least 3 iterations:

### Iteration 1: CREATE

| Step | Actor | Strategy | Output |
|------|-------|----------|--------|
| 1.1 | Creator agent | S-010 Self-Refine | Initial artifact with self-improvement |
| 1.2 | Creator agent | -- | Artifact persisted to filesystem |

**Quality expectation:** ~0.60-0.80 (draft quality, not yet reviewed).

### Iteration 2: CRITIQUE

| Step | Actor | Strategy | Output |
|------|-------|----------|--------|
| 2.1 | Orchestrator | Determine criticality (C1-C4) | Criticality level |
| 2.2 | Orchestrator | Select mode pipeline | Ordered mode list |
| 2.3 | ps-critic | Execute pipeline (per criticality) | Per-mode findings |
| 2.4 | ps-critic | S-014 scoring (last in pipeline) | Quality score + improvement areas |

**Quality expectation:** Score provides baseline for improvement tracking.

### Iteration 3: REVISE + VERIFY

| Step | Actor | Strategy | Output |
|------|-------|----------|--------|
| 3.1 | Creator agent | S-010 Self-Refine | Revised artifact addressing critique findings |
| 3.2 | ps-critic | S-014 + S-011 | Verification of revisions + updated score |
| 3.3 | Orchestrator | Circuit breaker check | ACCEPT / REVISE / ESCALATE |

**Quality expectation:** >= 0.92 (quality gate target).

### Extended Iterations (4+)

If quality gate not met after iteration 3:

| Condition | Action |
|-----------|--------|
| Score >= 0.92 | ACCEPT |
| Score >= 0.85 AND iteration >= 3 | ACCEPT_WITH_CAVEATS (document shortfall) |
| Score < 0.85 AND iteration >= 3 | ESCALATE to user per P-020 |
| Improvement delta < 0.05 for 2 consecutive | PLATEAU detected; escalate or accept with caveats |
| Token budget exhausted | Complete current mode; accept with caveats; escalate if C3+ |

### Cycle Tracking

Track each iteration's results for trend analysis:

```
Iteration 1: CREATE         -> Score: N/A (self-refine only)
Iteration 2: CRITIQUE       -> Score: 0.78 (C2 pipeline)
Iteration 3: REVISE+VERIFY  -> Score: 0.93 PASS (delta: +0.15)
Result: ACCEPTED at iteration 3
```
```

---

## New Section: Escalation Procedures

**Location:** After "Creator-Critic-Revision Cycle."

### Content

```markdown
## Escalation Procedures

### When to Escalate to Human Review

| Condition | Escalation Type | Action |
|-----------|----------------|--------|
| C4 criticality | MANDATORY | Human MUST review and ratify (P-020) |
| AE-006: TOK-EXHAUST + C3+ | MANDATORY | Human review required; agent review quality degraded |
| ENF-MIN-002: ENF-MIN + C3+ | MANDATORY | Human compensates for missing enforcement layers |
| TEAM-SINGLE + C4 | MANDATORY | Cannot perform C4 as single agent |
| Score < 0.80 after 3 iterations | RECOMMENDED | Agent-only review not producing adequate quality |
| Plateau detected (2 consecutive < 0.05 delta) | RECOMMENDED | Further iteration unlikely to improve quality |
| FMEA item with RPN > 400 | RECOMMENDED | High-risk item needs human judgment |
| Constitutional HARD rule FAIL on governance file | MANDATORY | Governance changes require human ratification |

### Escalation Message Template

When escalating to human review, provide:

```markdown
## ESCALATION: Human Review Required

**Artifact:** {artifact path}
**Criticality:** {C-level}
**Reason:** {escalation condition}
**Current Score:** {quality score}
**Iterations Completed:** {count}

### Summary of Findings
{top 3 findings from adversarial review}

### Specific Questions for Human Reviewer
1. {specific question needing human judgment}
2. {specific question needing human judgment}

### Recommendation
{ACCEPT_WITH_CAVEATS / REVISE / REJECT}
```

### Post-Escalation

After human review:
- Document human decision in the artifact's history
- If human accepts: close the review cycle
- If human requests revision: return to CREATE phase with human feedback
- Record the escalation and outcome for future calibration
```

---

## Updated Section: Circuit Breaker

### Current Circuit Breaker (v3.3.0)

```
max_iterations: 3
threshold: 0.85
```

### Updated Circuit Breaker (v4.0.0)

**Replace with dual-mode parameters:**

```markdown
### Circuit Breaker Configuration

| Parameter | Standard Mode | Adversarial Mode |
|-----------|--------------|------------------|
| Max iterations | 3 | 3 (min per H-14, extendable) |
| Acceptance threshold | 0.85 | 0.92 (H-13, from SSOT) |
| Improvement threshold | 0.10 per iteration | 0.05 per iteration |
| Plateau detection | 2 consecutive < threshold | 2 consecutive < 0.05 delta |
| Plateau action | Accept with caveats | Escalate to user (P-020) |
| Anti-leniency | Not required | REQUIRED (H-16) |
| Score tracking | Optional | REQUIRED (trend analysis) |

### Decision Logic

```
IF adversarial_mode:
    threshold = 0.92  # From quality-enforcement.md SSOT
ELSE:
    threshold = 0.85  # Backward compatible

IF score >= threshold:
    ACCEPT
ELIF iteration >= max_iterations:
    IF score >= 0.85:
        ACCEPT_WITH_CAVEATS
    ELSE:
        ESCALATE (P-020)
ELIF plateau_detected:
    ACCEPT_WITH_CAVEATS or ESCALATE
ELSE:
    REVISE
```
```

---

## Traceability

### Requirements Coverage

| Requirement | Coverage |
|-------------|----------|
| FR-304-005 (Multi-mode pipelines) | Adversarial Review Pipeline pattern |
| FR-304-006 (C1-C4 mapping) | Criticality-Driven Review pattern |
| FR-304-009 (Creator-critic cycle) | Creator-Critic-Revision Cycle section |
| FR-304-010 (Phase-strategy interaction) | Phase Adjustments table in Criticality-Driven Review |
| FR-304-011 (Escalation) | Escalation Procedures section |
| FR-304-012 (Token budget adaptation) | Referenced in Pattern 7 and Circuit Breaker |
| BC-304-001 (Default behavior) | Pattern 6 Standard Mode preserved |
| BC-304-003 (Threshold migration) | Dual-mode circuit breaker |
| EN-304 AC-8 | This document (PLAYBOOK.md adversarial workflow procedures) |

---

## References

| # | Citation | Relevance |
|---|----------|-----------|
| 1 | PLAYBOOK.md v3.3.0 | Current /problem-solving playbook (baseline) |
| 2 | EN-303 TASK-004 | Decision tree, auto-escalation rules, cycle mapping |
| 3 | EN-303 TASK-001 | Phase-strategy interaction matrix |
| 4 | TASK-001 (this enabler) | Formal requirements |
| 5 | TASK-002 (this enabler) | Mode definitions and sequencing rules |
| 6 | TASK-003 (this enabler) | Invocation protocol and pipeline execution model |
| 7 | TASK-004 (this enabler) | Agent spec updates with circuit breaker parameters |
| 8 | TASK-005 (this enabler) | SKILL.md update content (cross-reference) |
| 9 | Barrier-2 ENF-to-ADV | Enforcement architecture, HARD rules H-13/H-14/H-15/H-16 |
| 10 | EN-404 HARD rules | H-13 (0.92 threshold), H-14 (3-iteration min), H-16 (anti-leniency) |

---

*Document ID: FEAT-004:EN-304:TASK-006*
*Agent: ps-architect-304*
*Created: 2026-02-13*
*Status: Draft*
