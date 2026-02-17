# S-013: Inversion Technique -- Adversarial Strategy Execution Template

<!--
TEMPLATE: S-013 Inversion Technique Adversarial Strategy Execution Template
VERSION: 1.0.0 | DATE: 2026-02-15
SOURCE: quality-enforcement.md SSOT, ADR-EPIC002-001, TEMPLATE-FORMAT.md v1.1.0
ENABLER: EN-808 (S-013 Template)
STATUS: ACTIVE
CONFORMANCE: TEMPLATE-FORMAT.md v1.1.0

Academic Foundation:
- Jacobi (attributed): "Invert, always invert" (man muss immer umkehren) -- mathematical problem-solving
- Munger, Charlie: "Poor Charlie's Almanack" -- Inversion as mental model for decision-making
- Bevelin (2007): "Seeking Wisdom: From Darwin to Munger" -- systematic assumption inversion
- Taleb (2012): "Antifragile" -- via negativa (removing harm vs. adding good)

Origin: Mathematical heuristic (Carl Jacobi), popularized as decision-making mental model by
Charlie Munger. Extended into Assumption Mapping & Stress Testing methodology.
Key insight: Instead of asking "how do I succeed?", ask "how could I guarantee failure?"
Then ensure those conditions are absent.
Distinct from S-004 Pre-Mortem: Pre-Mortem uses temporal perspective ("it already failed, why?");
Inversion systematically inverts goals and stress-tests assumptions without temporal framing.
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
| [Purpose](#purpose) | When and why to apply Inversion |
| [Prerequisites](#prerequisites) | Required inputs and ordering constraints (H-16) |
| [Execution Protocol](#execution-protocol) | Step-by-step inversion and assumption stress-testing procedure |
| [Output Format](#output-format) | Required structure for Inversion report |
| [Scoring Rubric](#scoring-rubric) | Meta-evaluation of strategy execution quality |
| [Examples](#examples) | Concrete C3 demonstration with findings |
| [Integration](#integration) | Cross-strategy pairing, H-16 compliance, criticality mapping |

---

## Identity

| Field | Value |
|-------|-------|
| Strategy ID | S-013 |
| Strategy Name | Inversion Technique |
| Family | Structured Decomposition |
| Composite Score | 4.25 |
| Finding Prefix | IN-NNN-{execution_id} |
| Version | 1.0.0 |
| Date | 2026-02-15 |

### Criticality Tier Table

| Level | Name | Status | Notes |
|-------|------|--------|-------|
| C1 | Routine | NOT USED | C1 enforces HARD rules only; Inversion not required or optional |
| C2 | Standard | NOT USED | S-013 not in C2 required or optional sets |
| C3 | Significant | REQUIRED | Part of C3 required set (C2 + S-004, S-012, S-013) |
| C4 | Critical | REQUIRED | All 10 strategies required; tournament mode |

**Source:** quality-enforcement.md Criticality Levels table (SSOT).

**Foundation:** Jacobi's mathematical heuristic ("invert, always invert") was generalized by Charlie Munger into a decision-making mental model: instead of asking how to achieve a goal, ask what would guarantee failure and then avoid those conditions. Bevelin (2007) systematized this into explicit assumption mapping and stress-testing. Taleb's via negativa reinforces the power of removing known failure conditions over adding speculative success factors.

**Jerry Adaptation:** Two-phase approach for deliverable quality review: (1) Map all assumptions the deliverable relies upon, making implicit assumptions explicit, (2) Stress-test each assumption by inverting it and evaluating consequences. Complements S-004 Pre-Mortem (temporal perspective) and S-012 FMEA (component decomposition) by operating at the assumption and goal level.

**Distinction from S-004 (Pre-Mortem):** Pre-Mortem declares "it has already failed" and works backward via temporal perspective shift. Inversion systematically inverts the deliverable's goals ("What would guarantee this fails?") and stress-tests each assumption ("What if this assumption is wrong?") without temporal framing. Pre-Mortem generates failure scenarios; Inversion identifies the specific assumptions and anti-goals that make failure possible.

---

## Purpose

### When to Use

1. **C3+ Deliverable Review:** ALL Significant+ deliverables MUST undergo Inversion analysis (required at C3). Apply after Steelman (S-003) has strengthened the deliverable per H-16.

2. **Assumption-Heavy Deliverables:** When a deliverable relies on many explicit or implicit assumptions (market conditions, technology capabilities, team expertise, timeline estimates). Inversion stress-tests each assumption by asking "What if this is wrong?"

3. **Goal-Oriented Plans or Proposals:** When a deliverable aims to achieve a specific outcome (adoption, performance target, quality standard). Inversion inverts the goal ("What would guarantee we MISS this target?") to reveal conditions that must be avoided.

4. **Complementing S-004 Pre-Mortem:** After Pre-Mortem identifies failure scenarios, Inversion maps the specific assumptions underlying those scenarios and stress-tests them individually. The two strategies together provide comprehensive risk coverage.

### When NOT to Use

1. **Deliverables Without Clear Goals or Assumptions:** Purely descriptive artifacts (status reports, meeting notes) do not benefit from goal inversion or assumption stress-testing. Redirect to S-002 (Devil's Advocate) for argument-level critique.

2. **Trivial or C1/C2 Decisions:** For reversible decisions where S-002 provides sufficient adversarial coverage. Redirect to S-002 for C2 and S-010 for C1.

3. **Already-Validated Assumptions:** If assumptions have been empirically validated (prototyped, measured, confirmed by stakeholders), Inversion stress-testing yields diminishing returns for those specific assumptions. Focus on unvalidated assumptions.

### Expected Outcome

An Inversion report containing:
- Clear statement of the deliverable's primary goals
- Inverted anti-goals ("What would guarantee failure?") with specific conditions
- Complete assumption map (explicit and implicit) with at least 5 assumptions identified
- Stress-test results for each assumption (IN-NNN identifiers)
- Severity classification (Critical/Major/Minor) based on consequence of assumption failure
- Mitigation recommendations for vulnerable assumptions
- Mapping of findings to the 6 S-014 scoring dimensions
- Measurable quality improvement when mitigations are addressed (target: 0.05+ composite score increase)

### Pairing Recommendations

**H-16 Compliance (MANDATORY):** S-003 Steelman is not directly named by H-16 for S-013 (H-16 specifically requires S-003 before S-002, S-004, S-001). However, S-013 is REQUIRED at C3+ where S-003 is effectively required due to H-16 mandating it before other C3 strategies. In practice, S-003 will always have run before S-013 in a compliant C3+ sequence.

| Pairing | Order | Rationale |
|---------|-------|-----------|
| **S-003 + S-013** | S-003 -> S-013 | H-16 compliance for overall C3 sequence; Inversion analyzes strengthened version |
| **S-004 + S-013** | S-004 -> S-013 | Pre-Mortem identifies failure scenarios; Inversion maps underlying assumptions |
| **S-012 + S-013** | S-012 + S-013 (parallel or sequential) | Complementary: FMEA bottom-up + Inversion top-down; cover different failure dimensions |
| **S-013 + S-014** | S-013 -> S-014 | Inversion findings feed dimension scoring; S-014 validates post-mitigation quality |

**Optimal C3 sequence:** S-003 -> S-007 -> S-002 -> S-004 -> S-012 -> S-013 -> S-014

---

## Prerequisites

### Required Inputs

- [ ] Deliverable artifact (plan, design, ADR, proposal, specification, etc.)
- [ ] Criticality level classification (C3 or C4)
- [ ] S-003 Steelman output (H-16 compliance for overall C3+ sequence)
- [ ] Quality framework SSOT (`quality-enforcement.md`) for dimension weights and threshold
- [ ] Domain context sufficient to identify realistic assumptions and anti-goals

### Context Requirements

The executor must understand the deliverable's goals clearly enough to invert them, have domain expertise sufficient to identify both explicit and implicit assumptions, and have access to S-004 Pre-Mortem output (if available) to map assumptions underlying identified failure scenarios. Understanding of the operational environment helps assess what "guaranteed failure" looks like.

### Ordering Constraints

**H-16 Context:** S-003 Steelman MUST have been applied before the C3+ adversarial sequence begins. While H-16 specifically names S-002/S-004/S-001, S-013 operates on the Steelman-strengthened deliverable in a compliant C3+ workflow.

**Recommended sequence:**
1. S-003 Steelman (strengthen the deliverable)
2. S-007 Constitutional AI Critique (HARD rule compliance)
3. S-002 Devil's Advocate (challenge claims)
4. S-004 Pre-Mortem (prospective hindsight)
5. S-012 FMEA (component decomposition)
6. **S-013 Inversion (this strategy -- assumption stress-testing)**
7. S-014 LLM-as-Judge (score the revised deliverable)

**Minimum:** S-003 before the adversarial sequence. S-014 after S-013 for dimensional scoring.

---

## Execution Protocol

### Step 1: State the Goals Clearly

**Action:** Extract and articulate the deliverable's primary goals in specific, measurable terms.

**Procedure:**
1. Read the deliverable and S-003 Steelman output in full
2. Identify the deliverable's stated goals (explicit success criteria, desired outcomes, target metrics)
3. Identify implicit goals (unstated but assumed: adoptability, maintainability, team capability)
4. Restate each goal in specific, measurable terms (not "improve quality" but "achieve >= 0.92 composite score on S-014 evaluation with all 6 dimensions above 0.85")
5. Confirm goal completeness: are there goals the deliverable SHOULD have but does not state?

**Decision Point:**
- If no clear goals found: flag as Completeness concern; construct inferred goals from deliverable context.
- If goals are vague: restate them precisely before proceeding (Inversion requires specific goals to invert).

**Output:** Goal inventory with specific, measurable descriptions for each explicit and implicit goal.

### Step 2: Invert the Goals (Anti-Goals)

**Action:** For each goal, ask: "What would guarantee we FAIL to achieve this goal?" Enumerate specific anti-goals.

**Procedure:**
For each goal from Step 1:
1. State the inversion: "To guarantee failure at [goal], we would need to..."
2. Enumerate specific conditions that would guarantee failure (not just "do it badly" but specific anti-patterns):
   - What actions would guarantee this goal is NOT met?
   - What conditions would make success impossible?
   - What would a saboteur do to ensure failure?
3. For each anti-goal condition, assess whether the deliverable currently avoids this condition
4. Flag any anti-goal conditions that the deliverable does NOT explicitly address
5. Assign IN-NNN identifiers to findings where the deliverable is vulnerable to an anti-goal

**Decision Point:**
- If all anti-goals are already addressed by the deliverable: document this as evidence of strength; deliverable is robust against inversion.
- If 3+ anti-goals are unaddressed: deliverable has significant assumption vulnerabilities.

**Output:** Anti-goal inventory with IN-NNN findings for unaddressed conditions.

### Step 3: Map All Assumptions

**Action:** Extract every assumption the deliverable relies upon, making implicit assumptions explicit.

**Procedure:**
1. Identify **explicit assumptions** stated in the deliverable (e.g., "We assume the team has Python expertise")
2. Identify **implicit assumptions** not stated but necessary for the deliverable to succeed:
   - **Technical:** What technology capabilities are assumed? (performance, scalability, compatibility)
   - **Process:** What workflow or operational conditions are assumed? (review cadence, deployment process)
   - **Resource:** What team skills, availability, or budget are assumed?
   - **Environmental:** What external conditions are assumed? (market, regulatory, dependency stability)
   - **Temporal:** What timeline assumptions are made? (development speed, adoption rate)
3. For each assumption, assess:
   - **Confidence:** How certain is this assumption? (High/Medium/Low)
   - **Validation status:** Is this assumption empirically validated, logically inferred, or merely hoped?
   - **Consequence of failure:** What happens if this assumption is wrong?
4. Create an assumption inventory with unique identifiers

**Output:** Assumption map with explicit/implicit classification, confidence, validation status, and failure consequence.

### Step 4: Stress-Test Each Assumption

**Action:** For each assumption, systematically ask: "What if this assumption is wrong?" and evaluate the consequences.

**Procedure:**
For each assumption from Step 3:
1. **Invert the assumption:** State the opposite ("The team does NOT have Python expertise")
2. **Evaluate plausibility:** How realistic is this inversion? (Some inversions are implausible; others are likely)
3. **Assess consequences:** If this assumption fails, what happens to the deliverable?
   - Does the deliverable still work partially?
   - Does the entire approach become invalid?
   - Are there cascading effects on other assumptions?
4. **Classify severity:**
   - **Critical:** Assumption failure invalidates the deliverable's core approach. Blocks acceptance.
   - **Major:** Assumption failure significantly degrades deliverable value. Requires mitigation.
   - **Minor:** Assumption failure reduces quality but deliverable remains viable. Improvement opportunity.
5. **Map to affected dimension:** Identify which scoring dimension is impacted
6. **Assign IN-NNN identifier** for assumptions with Major+ consequences

**Decision Point:**
- If Critical assumptions found with Low confidence: deliverable has fundamental vulnerability. Flag for immediate mitigation.
- If all assumptions are High confidence and empirically validated: deliverable is robust. Document strength.

**Output:** Stress-test results table with IN-NNN identifiers, assumption inversions, plausibility, severity, and affected dimensions.

### Step 5: Develop Mitigations

**Action:** For each vulnerable assumption (Critical and Major findings), develop specific mitigations.

**Procedure:**
1. For each Critical finding: specify how the deliverable should be revised to reduce dependency on this assumption (remove assumption, add contingency, validate empirically, add monitoring)
2. For each Major finding: specify recommended mitigation with acceptance criteria
3. For Minor findings: note the risk and suggest acknowledgment or monitoring
4. Verify each mitigation is concrete and actionable

**Output:** Mitigation plan with IN-NNN identifiers, specific actions, and acceptance criteria.

### Step 6: Synthesize and Score Impact

**Action:** Produce a consolidated Inversion assessment mapping findings to quality dimensions.

**Procedure:**
1. Aggregate findings: count Critical, Major, Minor assumptions; summarize anti-goal coverage
2. Map findings to the 6 scoring dimensions and assess net impact per dimension
3. Identify the most vulnerable assumption cluster (group of related assumptions that could fail together)
4. Determine overall assessment: significant revision required / targeted mitigation / proceed with monitoring
5. Apply H-15 self-review before presenting

**Output:** Scoring Impact table, overall assessment, and mitigation guidance.

---

## Output Format

Every S-013 execution MUST produce an Inversion report with these sections:

### 1. Header

```markdown
# Inversion Report: {{DELIVERABLE_NAME}}

**Strategy:** S-013 Inversion Technique
**Deliverable:** {{Artifact name, file path, or work item ID}}
**Criticality:** {{C3/C4}}
**Date:** {{ISO 8601 date}}
**Reviewer:** {{Agent ID or human name}}
**H-16 Compliance:** S-003 Steelman applied on {{date}} (confirmed)
**Goals Analyzed:** {{count}} | **Assumptions Mapped:** {{count}} | **Vulnerable Assumptions:** {{count}}
```

### 2. Summary

2-3 sentence overall assessment covering: number of goals inverted, assumptions mapped, vulnerable assumptions found, and recommendation (ACCEPT with mitigations / REVISE / REJECT).

### 3. Findings Table

| ID | Assumption / Anti-Goal | Type | Confidence | Severity | Evidence | Affected Dimension |
|----|------------------------|------|------------|----------|----------|--------------------|
| IN-001-{execution_id} | {{Assumption that failed stress-test}} | Assumption | {{H/M/L}} | Critical | {{Reference}} | {{Dimension}} |
| IN-002-{execution_id} | {{Anti-goal condition not addressed}} | Anti-Goal | N/A | Major | {{Reference}} | {{Dimension}} |

**Finding ID Format:** `IN-{NNN}-{execution_id}` where execution_id is a short timestamp or session identifier (e.g., `IN-001-20260215T1430`) to prevent ID collisions across tournament executions.

Severity definitions: see [Step 4: Stress-Test Each Assumption](#step-4-stress-test-each-assumption).

### 4. Finding Details

Expanded description for each Critical and Major finding:

```markdown
### IN-001: {{Finding Title}} [CRITICAL]

**Type:** {{Assumption / Anti-Goal}}
**Original Assumption:** {{The assumption as stated or inferred from the deliverable}}
**Inversion:** {{What happens if this assumption is wrong / anti-goal condition is present}}
**Plausibility:** {{How realistic is this inversion}} | **Confidence:** {{H/M/L}}
**Consequence:** {{Impact on the deliverable if this assumption fails}}
**Evidence:** {{Specific reference from the deliverable creating this vulnerability}}
**Dimension:** {{Affected scoring dimension}}
**Mitigation:** {{Specific action to reduce assumption dependency}}
**Acceptance Criteria:** {{What must be demonstrated to resolve this finding}}
```

### 5. Recommendations

Prioritized mitigations: **Critical** assumptions (MUST mitigate), **Major** assumptions (SHOULD mitigate), **Minor** assumptions (MAY mitigate). Each entry: IN-NNN identifier, mitigation action, acceptance criteria.

### 6. Scoring Impact

Map Inversion findings to S-014 scoring dimensions (Completeness 0.20, Internal Consistency 0.20, Methodological Rigor 0.20, Evidence Quality 0.15, Actionability 0.15, Traceability 0.10). For each dimension, assess Impact (Positive/Negative/Neutral) with rationale referencing specific IN-NNN findings.

### Evidence Requirements

Each finding MUST include: specific reference to the assumption or anti-goal condition in the deliverable, the inversion with plausibility assessment, and consequence description with specific impact on the deliverable.

---

## Scoring Rubric

This rubric evaluates the **quality of the S-013 Inversion execution itself** (meta-evaluation), not the deliverable being reviewed.

### Threshold Bands

**SSOT threshold (from quality-enforcement.md, MUST NOT be redefined):** >= 0.92 weighted composite score. Below threshold = REJECTED; revision required per H-13.

**Operational bands for S-013 execution quality:**

| Band | Score Range | Outcome |
|------|------------|---------|
| PASS | >= 0.92 | Strategy execution accepted; assumption mapping thorough and stress-testing rigorous |
| REVISE | 0.85 - 0.91 | Strategy execution requires targeted revision; close to threshold |
| REJECTED | < 0.85 | Strategy execution inadequate; significant rework required (H-13) |

> **Note:** Score bands (PASS/REVISE/REJECTED) are sourced from quality-enforcement.md (Operational Score Bands section). See SSOT for authoritative definitions.

### Dimension Weights

From quality-enforcement.md (MUST NOT be redefined):

| Dimension | Weight | Measures (for S-013 execution quality) |
|-----------|--------|----------------------------------------|
| Completeness | 0.20 | All goals inverted; all explicit and implicit assumptions mapped; 5+ assumptions stress-tested |
| Internal Consistency | 0.20 | Anti-goals and assumptions do not contradict; severity consistent with consequence assessment |
| Methodological Rigor | 0.20 | All 6 steps executed; both inversion phases (anti-goals + assumptions) applied; systematic stress-testing |
| Evidence Quality | 0.15 | Each finding backed by specific deliverable references; inversions plausible; consequences realistic |
| Actionability | 0.15 | Mitigations concrete; acceptance criteria specific and verifiable |
| Traceability | 0.10 | Findings linked to deliverable content and dimensions; IN-NNN identifiers used consistently |

### Strategy-Specific Rubric

| Dimension (Weight) | 0.95+ | 0.90-0.94 | 0.85-0.89 | <0.85 |
|--------------------|-------|-----------|-----------|-------|
| **Completeness (0.20)** | ALL goals inverted; ALL explicit + implicit assumptions mapped (5 categories); 7+ assumptions stress-tested; anti-goal coverage complete | Most goals inverted; most assumptions mapped; 5-6 stress-tested; minor coverage gaps | Core goals inverted; explicit assumptions mapped; some implicit missed; 3-4 stress-tested | Few goals inverted; only explicit assumptions; <3 stress-tested |
| **Internal Consistency (0.20)** | Zero contradictions; severity perfectly matches consequence analysis; anti-goals and assumptions coherent and non-redundant | No contradictions; severity mostly consistent; minor redundancy between findings | One minor inconsistency; some severity ratings questionable; overlapping findings | Multiple contradictions; arbitrary severity; anti-goals and assumptions confused |
| **Methodological Rigor (0.20)** | ALL 6 steps in order; both phases (inversion + stress-testing) systematic; 5 assumption categories used; S-004 distinction maintained | All steps executed; both phases present; most categories used; methodology mostly followed | 4-5 steps executed; one phase weak; some categories used; methodology loosely followed | Steps skipped; one phase missing; ad hoc analysis; no systematic method |
| **Evidence Quality (0.15)** | Every finding references specific deliverable content; inversions are plausible with realistic consequences; domain-informed analysis | Most findings have specific evidence; inversions mostly plausible; minor vagueness | Some findings have evidence; inversions reasonable but not fully justified; generic analysis | Findings speculative; inversions implausible; no evidence |
| **Actionability (0.15)** | ALL Critical/Major findings have specific mitigations with verifiable acceptance criteria | Most findings have mitigations; acceptance criteria for Critical findings; minor gaps | Some mitigations present; criteria vague; creator must interpret | No mitigations; findings are observations only |
| **Traceability (0.10)** | Every finding traces to specific deliverable content; all mapped to dimensions; IN-NNN consistent; assumption categories documented | Most findings traceable; dimension mapping present; IN-NNN consistent | Some findings traceable; partial dimension mapping; IN-NNN inconsistent | Not traceable; no dimension mapping; no identifiers |

---

## Examples

### Example 1: C3 Quality Framework Configuration -- Threshold and Weights Design

**Context:**
- **Deliverable:** Design proposal for configurable quality thresholds and dimension weights (allowing projects to customize the 0.92 threshold and 0.20/0.20/0.20/0.15/0.15/0.10 weights)
- **Criticality Level:** C3 (Significant) -- affects quality framework behavior, >10 files, API changes
- **Scenario:** S-003 Steelman applied (H-16), S-002, S-004, S-012 completed; now S-013 Inversion stress-tests assumptions

**Before (Key Claims from Design Proposal after Prior Strategies):**

The proposal allows: (1) per-project threshold override (min 0.80, max 0.99), (2) custom dimension weights (must sum to 1.00), (3) configuration via `quality-config.yaml`, (4) backward compatibility with default SSOT values. Prior strategies strengthened rationale (S-003), challenged necessity (S-002), identified risks around threshold gaming (S-004), and decomposed config file failure modes (S-012).

**Strategy Execution (Key Steps):**

**Step 1: State the Goals** -- Goals: (1) Project teams can customize quality thresholds to match risk profile, (2) Default SSOT values preserved for projects without custom config, (3) No configuration can result in quality degradation below acceptable minimums.

**Step 2: Invert the Goals** -- Anti-goals: "How would we guarantee quality degradation?" Answer: allow threshold to be set to 0.00 (guaranteed pass); allow a single dimension weight of 1.00 (bypass 5 of 6 dimensions); allow config to disable quality gate entirely.

**Step 3: Map Assumptions** (selected):
- Assumption A1: "0.80 minimum threshold is sufficient to prevent gaming" -- Confidence: Medium
- Assumption A2: "Weight sum = 1.00 constraint prevents manipulation" -- Confidence: Low
- Assumption A3: "Project teams will configure in good faith" -- Confidence: Low
- Assumption A4: "quality-config.yaml is tamper-resistant" -- Confidence: Medium

**Step 4: Stress-Test**

| ID | Assumption | Inversion | Severity | Affected Dimension |
|----|------------|-----------|----------|--------------------|
| IN-001-20260215T1430 | A2: Weight sum = 1.00 prevents manipulation | Setting Traceability weight to 0.60 and others to 0.08 each allows gaming by satisfying one easy dimension | Critical | Methodological Rigor |
| IN-002-20260215T1430 | A3: Good faith configuration | A hostile or rushed team sets threshold to 0.80 to rubber-stamp deliverables | Major | Evidence Quality |
| IN-003-20260215T1430 | A4: Config is tamper-resistant | No validation hook; config can be changed mid-review to lower threshold after a failing score | Major | Internal Consistency |
| IN-004-20260215T1430 | A1: 0.80 minimum is sufficient | At 0.80, a deliverable can have Critical findings (dimension <= 0.50) and still pass via high scores elsewhere | Major | Completeness |
| IN-005-20260215T1430 | Implicit: override history is tracked | No audit trail of threshold changes; cannot detect retroactive lowering | Minor | Traceability |

**Step 5: Develop Mitigations**

**Critical:** IN-001-20260215T1430 -- Add per-dimension weight bounds (min 0.05, max 0.40) preventing any single dimension from dominating. Acceptance criteria: no weight configuration can produce a PASS verdict with any dimension below 0.70.

**Major:** IN-002-20260215T1430 -- Add minimum threshold of 0.85 (not 0.80) with governance approval required for any threshold below SSOT default. IN-003-20260215T1430 -- Add config immutability during active review cycle (snapshot config at review start). IN-004-20260215T1430 -- Add dimension floor rule: no dimension below 0.60 regardless of composite score.

**After (Revised with Mitigations):**

The creator addressed findings: added weight bounds [0.05, 0.40] (IN-001-20260215T1430), raised minimum threshold to 0.85 with C3 governance approval for non-default values (IN-002-20260215T1430), added config snapshot mechanism (IN-003-20260215T1430), added dimension floor of 0.60 (IN-004-20260215T1430), and added config change audit log (IN-005-20260215T1430).

**Scoring Impact:**

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | IN-004-20260215T1430: No dimension floor allows Critical gaps to hide in composite |
| Internal Consistency | 0.20 | Negative | IN-003-20260215T1430: Mutable config during review creates inconsistent evaluation |
| Methodological Rigor | 0.20 | Negative | IN-001-20260215T1430: Weight manipulation circumvents 6-dimension methodology |
| Evidence Quality | 0.15 | Negative | IN-002-20260215T1430: Low threshold undermines evidence that quality gate is meaningful |
| Actionability | 0.15 | Neutral | Configuration mechanism itself is actionable |
| Traceability | 0.10 | Negative | IN-005-20260215T1430: No audit trail for config changes breaks traceability |

**Result:** 1 Critical and 3 Major assumption vulnerabilities identified via systematic inversion. Mitigations addressed all findings, adding defensive constraints that preserve quality framework integrity while allowing legitimate customization.

---

## Integration

### Canonical Pairings

See [Pairing Recommendations](#pairing-recommendations) for the full pairing table (S-003, S-004, S-012, S-014) with rationale and optimal sequence.

### H-16 Compliance

**H-16 Rule:** S-003 MUST execute before critique strategies (S-002, S-004, S-001). S-013 is not directly named in H-16 but operates within the C3+ sequence where H-16 is already satisfied. See [Prerequisites: Ordering Constraints](#ordering-constraints) for full sequence.

### Criticality-Based Selection Table

From quality-enforcement.md (MUST NOT modify):

| Level | Required Strategies | Optional Strategies | S-013 Status |
|-------|---------------------|---------------------|--------------|
| C1 | S-010 | S-003, S-014 | NOT USED |
| C2 | S-007, S-002, S-014 | S-003, S-010 | NOT USED |
| C3 | C2 + S-004, S-012, S-013 | S-001, S-003, S-010, S-011 | **REQUIRED** |
| C4 | All 10 selected | None | **REQUIRED** |

**Source:** quality-enforcement.md Criticality Levels table (SSOT). Values MUST match exactly.

### Cross-References

**SSOT:** `.context/rules/quality-enforcement.md` (H-13 threshold, dimension weights, criticality levels) | `ADR-EPIC002-001` (strategy selection, score 4.25) | `ADR-EPIC002-002` (enforcement architecture) | `.context/templates/adversarial/TEMPLATE-FORMAT.md` v1.1.0

**Strategy Templates:** `s-003-steelman.md` (prerequisite via H-16 for C3+ sequence) | `s-004-pre-mortem.md` (complementary: temporal failure vs. assumption stress-testing) | `s-012-fmea.md` (complementary: component decomposition vs. assumption-level analysis) | `s-014-llm-as-judge.md` (scores post-mitigation revision) | `s-002-devils-advocate.md` (complementary: argument attack vs. assumption inversion)

**Academic:** Jacobi (attributed), Munger "Poor Charlie's Almanack", Bevelin (2007) "Seeking Wisdom", Taleb (2012) "Antifragile". See file header.

**HARD Rules:** H-13 (threshold >= 0.92), H-14 (creator-critic cycle), H-15 (self-review), H-16 (steelman before critique), H-17 (scoring required) -- all from quality-enforcement.md

---

<!-- VALIDATION: 8 sections present | H-23/H-24 nav | IN-NNN prefix | H-16 documented | SSOT weights match | REVISE band noted | C3 example with Critical finding | Distinction from S-004 documented | No absolute paths | 4-band rubric | Under 500 lines -->

---

*Template Version: 1.0.0*
*Format Conformance: TEMPLATE-FORMAT.md v1.1.0*
*SSOT: `.context/rules/quality-enforcement.md`*
*Created: 2026-02-15*
*Enabler: EN-808*
