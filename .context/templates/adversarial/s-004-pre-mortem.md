# S-004: Pre-Mortem Analysis -- Adversarial Strategy Execution Template

<!--
TEMPLATE: S-004 Pre-Mortem Analysis Adversarial Strategy Execution Template
VERSION: 1.0.0 | DATE: 2026-02-15
SOURCE: quality-enforcement.md SSOT, ADR-EPIC002-001, TEMPLATE-FORMAT.md v1.1.0
ENABLER: EN-808 (S-004 Template)
STATUS: ACTIVE
CONFORMANCE: TEMPLATE-FORMAT.md v1.1.0

Academic Foundation:
- Klein (1998): "Sources of Power" -- prospective hindsight methodology (MIT Press)
- Klein (2007): "Performing a Project Premortem" (Harvard Business Review)
- Kahneman (2011): "Thinking, Fast and Slow" -- endorsement of pre-mortem as debiasing technique
- Mitchell et al. (1989): Prospective hindsight generates 30% more failure reasons than standard prediction

Origin: Gary Klein (1989), popularized by Daniel Kahneman.
Domain: Risk Management, Decision Science, Cognitive Psychology.
Key insight: Temporal perspective shift -- declaring failure as already happened overcomes
optimism bias and plan anchoring, enabling more complete failure enumeration.
-->

> **Type:** adversarial-strategy-template
> **Status:** ACTIVE
> **Version:** 1.0.0
> **Date:** 2026-02-15
> **Source:** quality-enforcement.md, ADR-EPIC002-001, ADR-EPIC002-002
> **Format Conformance:** TEMPLATE-FORMAT.md v1.1.0
> **Enabler:** EN-808

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Identity](#identity) | Strategy classification and metadata |
| [Purpose](#purpose) | When and why to apply Pre-Mortem Analysis |
| [Prerequisites](#prerequisites) | Required inputs and ordering constraints (H-16) |
| [Execution Protocol](#execution-protocol) | Step-by-step prospective hindsight procedure |
| [Output Format](#output-format) | Required structure for Pre-Mortem report |
| [Scoring Rubric](#scoring-rubric) | Meta-evaluation of strategy execution quality |
| [Examples](#examples) | Concrete C3 demonstration with findings |
| [Integration](#integration) | Cross-strategy pairing, H-16 compliance, criticality mapping |

---

## Identity

| Field | Value |
|-------|-------|
| Strategy ID | S-004 |
| Strategy Name | Pre-Mortem Analysis |
| Family | Role-Based Adversarialism |
| Composite Score | 4.10 |
| Finding Prefix | PM-NNN-{execution_id} |
| Version | 1.0.0 |
| Date | 2026-02-15 |

### Criticality Tier Table

| Level | Name | Status | Notes |
|-------|------|--------|-------|
| C1 | Routine | NOT USED | C1 enforces HARD rules only; Pre-Mortem not required or optional |
| C2 | Standard | NOT USED | S-004 not in C2 required or optional sets |
| C3 | Significant | REQUIRED | Part of C3 required set (C2 + S-004, S-012, S-013) |
| C4 | Critical | REQUIRED | All 10 strategies required; tournament mode |

**Source:** quality-enforcement.md Criticality Levels table (SSOT).

**Foundation:** Klein (1998) discovered that prospective hindsight -- imagining a future event has already occurred -- generates 30% more reasons for outcomes than standard prediction (Mitchell et al. 1989). Kahneman (2011) endorses Pre-Mortem as the single best debiasing technique for plan overconfidence.

**Jerry Implementation:** Declares the deliverable has "failed spectacularly" and works backward to enumerate failure causes. The temporal perspective shift overcomes optimism bias and plan anchoring inherent in forward-looking review. Implements H-16 ordering (S-003 Steelman MUST run before S-004).

---

## Purpose

### When to Use

1. **C3+ Deliverable Review:** ALL Significant+ deliverables MUST undergo Pre-Mortem analysis (required at C3). Apply after Steelman (S-003) has strengthened the deliverable per H-16.

2. **High-Stakes Plans or Proposals:** When a plan, design, or proposal has significant consequences if it fails -- architecture decisions, migration plans, API contracts, governance changes. The temporal perspective shift reveals risks that forward-looking review misses.

3. **Confident Teams or Consensus Decisions:** When optimism bias is high ("this plan is solid") and team members are reluctant to voice concerns. Pre-Mortem gives permission to imagine failure without appearing negative.

4. **Multi-Phase or Long-Duration Deliverables:** When the deliverable spans multiple phases, iterations, or sprints. Pre-Mortem identifies phase-specific failure modes and cascading risks that compound over time.

### When NOT to Use

1. **Trivial or C1/C2 Routine Decisions:** For reversible single-session work or standard decisions where S-002 (Devil's Advocate) already provides sufficient adversarial coverage. Redirect to S-002 for C2 critique.

2. **Already-Failed Deliverables:** If the deliverable has known Critical issues (e.g., from S-007 constitutional check), Pre-Mortem adds no value -- the failure is real, not hypothetical. Redirect to revision based on existing findings.

3. **Pure Analysis or Research Artifacts:** Pre-Mortem works best on plans, proposals, and decisions with future outcomes. For analysis deliverables where "failure" is ill-defined, redirect to S-013 (Inversion) for assumption stress-testing.

### Expected Outcome

A Pre-Mortem report containing:
- Declaration of failure with specific failure scenario description
- Enumeration of at least 5 failure causes with PM-NNN identifiers
- Categorization of failure causes by type (Technical, Process, Assumption, External, Resource)
- Severity classification (Critical/Major/Minor) with evidence for each finding
- Likelihood x Severity prioritization matrix for failure causes
- Mitigation plan for all Critical and Major failure causes
- Mapping of findings to the 6 S-014 scoring dimensions
- Measurable quality improvement when mitigations are addressed (target: 0.05+ composite score increase)

### Pairing Recommendations

**H-16 Compliance (MANDATORY):** Run S-003 Steelman BEFORE S-004 Pre-Mortem. H-16 requires the deliverable to be strengthened before adversarial critique. Pre-Mortem must analyze the strongest version, not a weak first draft.

| Pairing | Order | Rationale |
|---------|-------|-----------|
| **S-003 + S-004** | S-003 -> S-004 | H-16: Steelman strengthens before Pre-Mortem imagines failure |
| **S-004 + S-014** | S-004 -> S-014 | Findings feed dimension scoring; S-014 validates post-mitigation quality |
| **S-004 + S-002** | S-002 + S-004 (parallel or sequential) | Complementary: S-002 attacks current claims; S-004 imagines future failures |
| **S-004 + S-012** | S-004 -> S-012 | Pre-Mortem identifies high-level risks; FMEA decomposes into component failure modes |

**Optimal C3 sequence:** S-003 -> S-007 -> S-002 -> S-004 -> S-012 -> S-013 -> S-014

---

## Prerequisites

### Required Inputs

- [ ] Deliverable artifact (plan, design, ADR, proposal, architecture, etc.)
- [ ] Criticality level classification (C3 or C4)
- [ ] S-003 Steelman output (H-16 compliance: Steelman MUST have been applied first)
- [ ] Quality framework SSOT (`quality-enforcement.md`) for dimension weights and threshold
- [ ] Domain context sufficient to imagine realistic failure scenarios

### Context Requirements

The executor must have domain expertise sufficient to envision realistic failure modes, familiarity with the deliverable's goals and approach, access to the S-003 Steelman output, and understanding of the operational context (who uses the deliverable, what depends on it, what are the downstream consequences of failure).

### Ordering Constraints

**H-16 (MANDATORY):** S-003 Steelman MUST be applied before S-004 Pre-Mortem. The deliverable MUST be strengthened before prospective hindsight analysis begins. Executing S-004 without prior S-003 is an H-16 violation.

**Recommended sequence:**
1. S-010 Self-Refine (creator self-review)
2. S-003 Steelman (strengthen the deliverable)
3. S-007 Constitutional AI Critique (HARD rule compliance)
4. S-002 Devil's Advocate (challenge current claims)
5. **S-004 Pre-Mortem Analysis (this strategy)**
6. S-012 FMEA (decompose failure modes from Pre-Mortem findings)
7. S-014 LLM-as-Judge (score the revised deliverable)

**Minimum:** S-003 before S-004. S-014 after S-004 for dimensional scoring.

---

## Execution Protocol

### Step 1: Set the Stage

**Action:** Establish the Pre-Mortem context by identifying the deliverable, its goals, and the definition of "failure."

**Procedure:**
1. Read the deliverable and S-003 Steelman output in full (H-16 compliance check: if no S-003 output exists, STOP and flag H-16 violation)
2. Identify the deliverable's primary goals: what does success look like?
3. Define failure explicitly: "This deliverable has failed. What does that mean concretely?" (e.g., "The architecture was abandoned after 3 months," "The migration caused 2 days of downtime," "The API contract broke 5 downstream consumers")
4. Document the failure scenario in specific, vivid terms -- avoid vague "it didn't work" framing

**Decision Point:**
- If S-003 Steelman output is missing: STOP. Flag H-16 violation. Do not proceed until S-003 is applied.
- If S-003 output exists: Proceed to Step 2.

**Output:** Failure scenario declaration with specific, concrete description of what "failed spectacularly" means.

### Step 2: Declare Failure and Shift Perspective

**Action:** Adopt the temporal perspective shift. Declare that the deliverable has already failed and you are looking back to understand why.

**Procedure:**
1. State explicitly: "It is [date + 6 months]. This deliverable has failed spectacularly. We are now investigating why."
2. Adopt the retrospective mindset: you are not predicting failure, you are explaining it after the fact
3. This shift is critical -- Mitchell et al. (1989) demonstrated that "it has happened" framing generates 30% more failure causes than "it might happen" framing
4. Document the perspective shift in the output report

**Output:** Temporal perspective shift statement establishing the retrospective analysis frame.

### Step 3: Generate Failure Causes

**Action:** Enumerate all plausible reasons why the deliverable failed, working backward from the declared failure scenario.

**Procedure:**
For each failure cause, apply the 5 failure category lenses:

1. **Technical failures:** Implementation flaws, design weaknesses, scalability limits, performance issues, integration breakdowns
2. **Process failures:** Workflow gaps, missing reviews, inadequate testing, deployment risks, monitoring blind spots
3. **Assumption failures:** Unstated assumptions that proved wrong, environmental changes, dependency failures
4. **External failures:** Market changes, regulatory shifts, third-party deprecation, security threats
5. **Resource failures:** Skill gaps, staffing changes, timeline pressure, budget constraints

For each failure cause:
1. Describe the failure cause in specific terms (not "it was too slow" but "event replay took 45 minutes for 100K events, exceeding the 5-minute recovery SLA")
2. Assess **likelihood** (High/Medium/Low) -- how plausible is this failure?
3. Assess **severity** using standard definitions (see below)
4. Map to affected scoring dimension
5. Assign PM-NNN-{execution_id} identifier

**Decision Point:**
- If fewer than 5 failure causes generated: apply deeper analysis. Pre-Mortem should generate substantially more causes than standard review. Force each of the 5 category lenses.
- If Critical failure causes found: the deliverable has fundamental risks requiring mitigation before acceptance.

**Severity Definitions:**
- **Critical:** Failure cause would invalidate the deliverable or cause irreversible harm. Blocks acceptance.
- **Major:** Failure cause would significantly degrade deliverable value or require substantial rework. Requires mitigation.
- **Minor:** Failure cause would reduce quality but not block use. Improvement opportunity.

**Output:** Failure cause inventory with PM-NNN identifiers, categories, likelihood, severity, and affected dimensions.

### Step 4: Prioritize by Likelihood x Severity

**Action:** Rank failure causes by combined likelihood and severity to focus mitigation effort.

**Procedure:**
1. Create a prioritization matrix:
   - **P0 (Immediate):** Critical severity AND High/Medium likelihood -- MUST mitigate before acceptance
   - **P1 (Important):** Major severity AND High likelihood, OR Critical severity AND Low likelihood -- SHOULD mitigate
   - **P2 (Monitor):** Major severity AND Medium/Low likelihood, OR Minor severity -- MAY mitigate; acknowledge risk
2. Sort findings by priority (P0 first)
3. For each P0 and P1 finding, identify what would need to change in the deliverable to prevent this failure

**Output:** Prioritized failure cause table with P0/P1/P2 rankings.

### Step 5: Develop Mitigations

**Action:** For each P0 and P1 failure cause, develop a specific mitigation that the deliverable should incorporate.

**Procedure:**
1. For each P0 finding: specify the exact revision needed (content addition, risk acknowledgment, alternative approach, contingency plan)
2. For each P1 finding: specify the recommended revision with acceptance criteria
3. For P2 findings: note the risk and suggest monitoring approach
4. Verify each mitigation is concrete and actionable (not "consider risks" but "add Section 5: Risk Mitigation with contingency for event schema versioning")

**Output:** Mitigation plan with specific actions, acceptance criteria, and priority ordering.

### Step 6: Synthesize and Score Impact

**Action:** Produce a consolidated assessment mapping Pre-Mortem findings to quality dimensions.

**Procedure:**
1. Aggregate findings by severity: count Critical, Major, Minor
2. Map findings to the 6 scoring dimensions and assess net impact (Positive/Negative/Neutral) per dimension
3. Estimate composite score impact of mitigations
4. Determine overall assessment: major mitigation required / targeted mitigation / proceed with monitoring
5. Apply H-15 self-review before presenting

**Output:** Scoring Impact table, overall assessment, and mitigation guidance.

---

## Output Format

Every S-004 execution MUST produce a Pre-Mortem report with these sections:

### 1. Header

```markdown
# Pre-Mortem Report: {{DELIVERABLE_NAME}}

**Strategy:** S-004 Pre-Mortem Analysis
**Deliverable:** {{Artifact name, file path, or work item ID}}
**Criticality:** {{C3/C4}}
**Date:** {{ISO 8601 date}}
**Reviewer:** {{Agent ID or human name}}
**H-16 Compliance:** S-003 Steelman applied on {{date}} (confirmed)
**Failure Scenario:** {{Specific description of declared failure}}
```

### 2. Summary

2-3 sentence overall assessment covering: number and severity of failure causes identified, overall deliverable risk posture, and recommendation (ACCEPT with mitigations / REVISE / REJECT).

### 3. Findings Table

| ID | Failure Cause | Category | Likelihood | Severity | Priority | Affected Dimension |
|----|---------------|----------|------------|----------|----------|--------------------|
| PM-001-{execution_id} | {{Failure cause}} | {{Technical/Process/Assumption/External/Resource}} | {{H/M/L}} | Critical | P0 | {{Dimension}} |
| PM-002-{execution_id} | {{Failure cause}} | {{Category}} | {{H/M/L}} | Major | P1 | {{Dimension}} |

**Finding ID Format:** `PM-{NNN}-{execution_id}` where execution_id is a short timestamp or session identifier (e.g., `PM-001-20260215T1430`) to prevent ID collisions across tournament executions.

Severity definitions: see [Step 3: Generate Failure Causes](#step-3-generate-failure-causes).

### 4. Finding Details

Expanded description for each Critical and Major finding:

```markdown
### PM-001: {{Finding Title}} [CRITICAL]

**Failure Cause:** {{Specific description of how this failure manifests}}
**Category:** {{Technical/Process/Assumption/External/Resource}}
**Likelihood:** {{High/Medium/Low}} -- {{Justification}}
**Severity:** {{Critical/Major}} -- {{Consequence if failure occurs}}
**Evidence:** {{Specific references from the deliverable that create this risk}}
**Dimension:** {{Affected scoring dimension}}
**Mitigation:** {{Specific action to prevent or reduce this failure}}
**Acceptance Criteria:** {{What must be demonstrated to resolve this finding}}
```

### 5. Recommendations

Prioritized mitigation plan grouped by: **P0** (Critical -- MUST mitigate before acceptance), **P1** (Important -- SHOULD mitigate), **P2** (Monitor -- MAY mitigate; acknowledge risk). Each entry: PM-NNN identifier, specific mitigation action, and acceptance criteria.

### 6. Scoring Impact

Map Pre-Mortem findings to S-014 scoring dimensions (Completeness 0.20, Internal Consistency 0.20, Methodological Rigor 0.20, Evidence Quality 0.15, Actionability 0.15, Traceability 0.10). For each dimension, assess Impact (Positive/Negative/Neutral) with rationale referencing specific PM-NNN findings.

### Evidence Requirements

Each finding MUST include: specific reference to the location in the deliverable that creates the risk, description of the failure scenario with concrete consequences, and explanation of why this failure cause is plausible.

---

## Scoring Rubric

This rubric evaluates the **quality of the S-004 Pre-Mortem execution itself** (meta-evaluation), not the deliverable being reviewed.

### Threshold Bands

**SSOT threshold (from quality-enforcement.md, MUST NOT be redefined):** >= 0.92 weighted composite score. Below threshold = REJECTED; revision required per H-13.

**Operational bands for S-004 execution quality:**

| Band | Score Range | Outcome |
|------|------------|---------|
| PASS | >= 0.92 | Strategy execution accepted; failure analysis is thorough and evidence-based |
| REVISE | 0.85 - 0.91 | Strategy execution requires targeted revision; close to threshold |
| REJECTED | < 0.85 | Strategy execution inadequate; significant rework required (H-13) |

> **Note:** The SSOT defines only the 0.92 threshold with REJECTED as the below-threshold outcome. The REVISE band (0.85-0.91) is a template-specific operational category (not sourced from quality-enforcement.md) to distinguish near-threshold executions requiring targeted improvements from those requiring significant rework. Both REVISE and REJECTED trigger the revision cycle per H-13.

### Dimension Weights

From quality-enforcement.md (MUST NOT be redefined):

| Dimension | Weight | Measures (for S-004 execution quality) |
|-----------|--------|----------------------------------------|
| Completeness | 0.20 | All 5 failure categories explored; 5+ failure causes; mitigations for all P0/P1 findings |
| Internal Consistency | 0.20 | Findings do not contradict each other; severity/likelihood consistent with evidence; priorities coherent |
| Methodological Rigor | 0.20 | Temporal perspective shift applied; all 6 steps executed; H-16 verified; 5 category lenses used |
| Evidence Quality | 0.15 | Each failure cause backed by specific deliverable references and realistic scenarios |
| Actionability | 0.15 | Mitigations concrete; acceptance criteria specific and verifiable |
| Traceability | 0.10 | Findings linked to deliverable content; dimensions mapped; H-16 compliance documented |

### Strategy-Specific Rubric

| Dimension (Weight) | 0.95+ | 0.90-0.94 | 0.85-0.89 | <0.85 |
|--------------------|-------|-----------|-----------|-------|
| **Completeness (0.20)** | ALL 5 failure categories explored with 7+ causes; mitigations for all P0/P1; failure scenario vivid and specific | All 5 categories explored; 5-6 causes; mitigations for P0; failure scenario clear | 3-4 categories explored; 3-4 causes; some mitigations missing; failure scenario vague | <3 categories; <3 causes; no mitigations; no failure scenario |
| **Internal Consistency (0.20)** | Zero contradictions; severity/likelihood/priority perfectly aligned with evidence; failure causes do not overlap redundantly | No contradictions; severity mostly justified; minor priority alignment gaps | One minor inconsistency; some severity ratings questionable; overlapping causes not acknowledged | Multiple contradictions; arbitrary severity; redundant causes without differentiation |
| **Methodological Rigor (0.20)** | Temporal perspective shift explicitly documented; all 6 steps in order; H-16 verified with evidence; all 5 lenses applied; leniency bias counteracted | All steps executed; H-16 verified; most lenses applied; perspective shift present | 4-5 steps executed; H-16 noted; some lenses applied; perspective shift implicit | <4 steps; H-16 not checked; ad hoc failure enumeration; no perspective shift |
| **Evidence Quality (0.15)** | Every failure cause references specific deliverable content; realistic scenarios with concrete consequences; domain-informed analysis | Most causes have specific evidence; scenarios realistic; minor vagueness | Some causes have evidence; scenarios plausible but not specific; general domain knowledge | Causes speculative; no evidence; generic risks not tied to deliverable |
| **Actionability (0.15)** | ALL P0/P1 mitigations specific with verifiable acceptance criteria; creator can act without guessing | Most mitigations specific; acceptance criteria for P0 findings; minor gaps | Some mitigations present; criteria vague; creator must interpret | No mitigations; findings are observations without guidance |
| **Traceability (0.10)** | Every finding traces to deliverable content; all findings mapped to dimensions; H-16 documented with S-003 reference | Most findings traceable; dimension mapping present; H-16 documented | Some findings traceable; partial dimension mapping; H-16 mentioned | Findings not traceable; no dimension mapping; H-16 unknown |

---

## Examples

### Example 1: C3 Architecture Decision -- CQRS Event Store Migration

**Context:**
- **Deliverable:** Plan for migrating work item persistence from filesystem to event store with CQRS read models
- **Criticality Level:** C3 (Significant) -- >10 files affected, >1 day to reverse, API changes
- **Scenario:** S-003 Steelman applied first (H-16 compliance); S-002 Devil's Advocate also completed; now S-004 Pre-Mortem

**Before (Key Claims from Migration Plan after S-003 Steelman):**

The migration plan proposes: (1) replacing filesystem persistence with event store over 3 phases, (2) maintaining backward compatibility via dual-write during transition, (3) read model projections for query optimization, (4) estimated 2-week implementation timeline. The plan was strengthened by S-003 (evidence added, alternatives documented) and critiqued by S-002 (dual-write complexity flagged).

**Strategy Execution (S-004 Pre-Mortem):**

**Step 1: Set the Stage** -- Failure scenario: "It is August 2026. The event store migration was abandoned after Phase 2. Work item data was partially corrupted during dual-write, requiring 3 days of manual recovery. The team reverted to filesystem persistence."

**Step 2: Declare Failure** -- Temporal perspective shift established: analyzing from the retrospective frame of a failed migration.

**Step 3: Generate Failure Causes**

| ID | Failure Cause | Category | Likelihood | Severity | Priority | Affected Dimension |
|----|---------------|----------|------------|----------|----------|--------------------|
| PM-001-20260215T1430 | Dual-write consistency failure: events written to event store but filesystem write fails, creating divergent state | Technical | High | Critical | P0 | Internal Consistency |
| PM-002-20260215T1430 | Event schema evolution not planned: WorkItem events change shape in Phase 2, breaking Phase 1 projections | Assumption | Medium | Major | P1 | Completeness |
| PM-003-20260215T1430 | Read model projection lag exceeds user tolerance: CLI commands return stale data during high-activity periods | Technical | Medium | Major | P1 | Actionability |
| PM-004-20260215T1430 | 2-week timeline assumes no discovery work: actual event modeling and aggregate redesign takes 4+ weeks | Resource | High | Major | P1 | Evidence Quality |
| PM-005-20260215T1430 | Rollback path undefined: if Phase 2 fails, no documented procedure to revert to filesystem-only | Process | Medium | Major | P1 | Methodological Rigor |
| PM-006-20260215T1430 | Single developer knowledge concentration: if primary implementer is unavailable, migration stalls | Resource | Low | Minor | P2 | Actionability |

**Step 5: Develop Mitigations**

**P0:** PM-001-20260215T1430 -- Add transactional dual-write with compensating action (if either write fails, both roll back). Document the consistency guarantee in the plan. Acceptance criteria: dual-write failure scenario documented with specific recovery procedure.

**P1:** PM-002-20260215T1430 -- Add "Event Versioning Strategy" section with upcasting approach. PM-003-20260215T1430 -- Define acceptable staleness SLA and add synchronous fallback for critical queries. PM-004-20260215T1430 -- Add Phase 0 "Discovery Sprint" (1 week) for event modeling before implementation begins. PM-005-20260215T1430 -- Add "Rollback Procedure" section with step-by-step reversion for each phase.

**After (Migration Plan Revised Based on PM Findings):**

The creator addressed findings: added transactional dual-write section (PM-001-20260215T1430), event versioning strategy (PM-002-20260215T1430), staleness SLA with sync fallback (PM-003-20260215T1430), Phase 0 discovery sprint extending timeline to 3 weeks (PM-004-20260215T1430), and per-phase rollback procedures (PM-005-20260215T1430). PM-006-20260215T1430 acknowledged with cross-training note.

**Scoring Impact:**

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | PM-002-20260215T1430, PM-005-20260215T1430: Missing versioning strategy and rollback path are significant gaps |
| Internal Consistency | 0.20 | Negative | PM-001-20260215T1430: Dual-write without consistency guarantee contradicts "safe migration" claim |
| Methodological Rigor | 0.20 | Negative | PM-004-20260215T1430: Unrealistic timeline undermines plan credibility |
| Evidence Quality | 0.15 | Negative | PM-004-20260215T1430: No basis for 2-week estimate; no comparable migration data cited |
| Actionability | 0.15 | Negative | PM-003-20260215T1430, PM-006-20260215T1430: No staleness SLA; single-point-of-failure risk |
| Traceability | 0.10 | Neutral | Plan traces to architecture ADR and CQRS design decision |

**Result:** 1 Critical and 4 Major failure causes identified via prospective hindsight. After mitigation, the plan addressed all P0/P1 findings, improving 5 of 6 dimensions toward the 0.92 threshold.

---

## Integration

### Canonical Pairings

See [Pairing Recommendations](#pairing-recommendations) for the full pairing table (S-003, S-014, S-002, S-012) with rationale and optimal sequence.

### H-16 Compliance

**H-16 Rule:** Steelman before critique. S-003 MUST execute before S-004. Full ordering constraints and recommended sequences are documented in [Prerequisites: Ordering Constraints](#ordering-constraints) and [Purpose: Pairing Recommendations](#pairing-recommendations).

**Compliant:** S-003 -> S-004 -> S-014; S-003 -> S-002 -> S-004 -> S-014. **Non-Compliant:** S-004 without prior S-003; S-004 -> S-003.

### Criticality-Based Selection Table

From quality-enforcement.md (MUST NOT modify):

| Level | Required Strategies | Optional Strategies | S-004 Status |
|-------|---------------------|---------------------|--------------|
| C1 | S-010 | S-003, S-014 | NOT USED |
| C2 | S-007, S-002, S-014 | S-003, S-010 | NOT USED |
| C3 | C2 + S-004, S-012, S-013 | S-001, S-003, S-010, S-011 | **REQUIRED** |
| C4 | All 10 selected | None | **REQUIRED** |

**Source:** quality-enforcement.md Criticality Levels table (SSOT). Values MUST match exactly.

### Cross-References

**SSOT:** `.context/rules/quality-enforcement.md` (H-13 threshold, H-16, dimension weights, criticality levels) | `ADR-EPIC002-001` (strategy selection, score 4.10) | `ADR-EPIC002-002` (enforcement architecture) | `.context/templates/adversarial/TEMPLATE-FORMAT.md` v1.1.0

**Strategy Templates:** `s-003-steelman.md` (MUST run before S-004, H-16) | `s-002-devils-advocate.md` (complementary: current claims vs. future failures) | `s-012-fmea.md` (decomposes Pre-Mortem risks into component failure modes) | `s-013-inversion.md` (complementary: assumption mapping vs. failure imagination) | `s-014-llm-as-judge.md` (scores post-mitigation revision) | `s-001-red-team.md` (complementary Role-Based Adversarialism)

**Academic:** Klein (1998, 2007), Kahneman (2011), Mitchell et al. (1989). See file header.

**HARD Rules:** H-13 (threshold >= 0.92), H-14 (creator-critic cycle), H-15 (self-review), H-16 (steelman before critique), H-17 (scoring required) -- all from quality-enforcement.md

---

<!-- VALIDATION: 8 sections present | H-23/H-24 nav | PM-NNN prefix | H-16 documented | SSOT weights match | REVISE band noted | C3 example with Critical finding | No absolute paths | 4-band rubric | Under 500 lines -->

---

*Template Version: 1.0.0*
*Format Conformance: TEMPLATE-FORMAT.md v1.1.0*
*SSOT: `.context/rules/quality-enforcement.md`*
*Created: 2026-02-15*
*Enabler: EN-808*
