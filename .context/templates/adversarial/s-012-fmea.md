# S-012: FMEA (Failure Mode and Effects Analysis) -- Adversarial Strategy Execution Template

<!--
TEMPLATE: S-012 FMEA Adversarial Strategy Execution Template
VERSION: 1.0.0 | DATE: 2026-02-15
SOURCE: quality-enforcement.md SSOT, ADR-EPIC002-001, TEMPLATE-FORMAT.md v1.1.0
ENABLER: EN-808 (S-012 Template)
STATUS: ACTIVE
CONFORMANCE: TEMPLATE-FORMAT.md v1.1.0

Academic Foundation:
- MIL-P-1629 (1949): U.S. Military "Procedures for Performing a Failure Mode, Effects and Criticality Analysis"
- AIAG/VDA FMEA Handbook (2019): Automotive industry standard FMEA methodology
- Stamatis (2003): "Failure Mode and Effects Analysis: FMEA from Theory to Execution"
- IEC 60812:2018: "Failure modes and effects analysis (FMEA and FMECA)"
- NPR 7123.1D: NASA Systems Engineering Processes and Requirements

Origin: U.S. Military 1949 (MIL-P-1629), adopted by NASA Apollo program, standardized by
automotive industry (AIAG). Extended to software, processes, and decision analysis.
Key output: Risk Priority Number (RPN) = Severity x Occurrence x Detection (each 1-10).
Systematic bottom-up enumeration of ALL failure modes per component/element.
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
| [Purpose](#purpose) | When and why to apply FMEA |
| [Prerequisites](#prerequisites) | Required inputs and ordering constraints (H-16) |
| [Execution Protocol](#execution-protocol) | Step-by-step FMEA decomposition and RPN procedure |
| [Output Format](#output-format) | Required structure for FMEA report |
| [Scoring Rubric](#scoring-rubric) | Meta-evaluation of strategy execution quality |
| [Examples](#examples) | Concrete C3 demonstration with findings |
| [Integration](#integration) | Cross-strategy pairing, H-16 compliance, criticality mapping |

---

## Identity

| Field | Value |
|-------|-------|
| Strategy ID | S-012 |
| Strategy Name | FMEA (Failure Mode and Effects Analysis) |
| Family | Structured Decomposition |
| Composite Score | 3.75 |
| Finding Prefix | FM-NNN-{execution_id} |
| Version | 1.0.0 |
| Date | 2026-02-15 |

### Criticality Tier Table

| Level | Name | Status | Notes |
|-------|------|--------|-------|
| C1 | Routine | NOT USED | C1 enforces HARD rules only; FMEA not required or optional |
| C2 | Standard | NOT USED | S-012 not in C2 required or optional sets |
| C3 | Significant | REQUIRED | Part of C3 required set (C2 + S-004, S-012, S-013) |
| C4 | Critical | REQUIRED | All 10 strategies required; tournament mode |

**Source:** quality-enforcement.md Criticality Levels table (SSOT).

**Foundation:** FMEA originated in U.S. Military reliability engineering (MIL-P-1629, 1949) and was adopted by NASA for Apollo mission hardware analysis. The automotive industry standardized it via AIAG/VDA. FMEA's power lies in systematic bottom-up decomposition: every element is examined for every possible failure mode, ensuring nothing is missed through intuition alone.

**Jerry Adaptation:** Generalized from hardware to software deliverables, designs, processes, and documents. "Components" become deliverable elements (sections, claims, decisions, interfaces). "Failure modes" become quality failures (incompleteness, inconsistency, ambiguity, missing evidence). RPN calculation prioritizes corrective action.

---

## Purpose

### When to Use

1. **C3+ Deliverable Review:** ALL Significant+ deliverables MUST undergo FMEA (required at C3). Apply after Steelman (S-003) has strengthened the deliverable per H-16.

2. **Complex Multi-Component Deliverables:** When a deliverable has many interacting parts (multi-section documents, multi-layer architectures, multi-phase plans) where individual component failures can cascade.

3. **After Pre-Mortem (S-004):** FMEA decomposes the high-level risks identified by Pre-Mortem into specific component-level failure modes with quantified severity, occurrence, and detection ratings.

4. **Design and Architecture Reviews:** When systematic enumeration of ALL possible failure modes is more valuable than targeted critique. FMEA's bottom-up approach complements S-002's top-down argument attack and S-004's prospective hindsight.

### When NOT to Use

1. **Simple or C1/C2 Deliverables:** FMEA's systematic decomposition overhead is disproportionate for deliverables with few components. For C2, S-002 (Devil's Advocate) provides sufficient adversarial coverage. Redirect to S-002.

2. **Deliverables Without Decomposable Elements:** If the deliverable is a single monolithic argument or brief narrative without distinct components, FMEA's element-by-element approach yields poor results. Redirect to S-013 (Inversion) for assumption stress-testing.

3. **Time-Critical Reviews:** FMEA is the most time-intensive adversarial strategy due to exhaustive enumeration. When time is constrained and C3 is not mandatory, use S-004 (Pre-Mortem) for faster risk identification.

### Expected Outcome

An FMEA report containing:
- Decomposition of the deliverable into discrete elements (5+ for C3 deliverables)
- Enumeration of failure modes per element (2+ per element minimum)
- RPN calculation (Severity x Occurrence x Detection, each 1-10) for each failure mode
- FM-NNN identifiers for all findings
- Prioritized corrective actions for highest-RPN failure modes
- Mapping of findings to the 6 S-014 scoring dimensions
- Measurable quality improvement when corrective actions are implemented (target: 0.05+ composite score increase)

### Pairing Recommendations

**H-16 Compliance (MANDATORY):** S-003 Steelman is not directly required before S-012 by H-16 (H-16 specifically requires S-003 before S-002, S-004, S-001). However, S-012 is REQUIRED at C3+ where S-003 is effectively required due to H-16 mandating it before other C3 strategies. In practice, S-003 will always have run before S-012 in a compliant C3+ sequence.

| Pairing | Order | Rationale |
|---------|-------|-----------|
| **S-003 + S-012** | S-003 -> S-012 | H-16 compliance for the overall C3 sequence; FMEA analyzes strengthened version |
| **S-004 + S-012** | S-004 -> S-012 | Pre-Mortem identifies high-level risks; FMEA decomposes into component failure modes |
| **S-012 + S-014** | S-012 -> S-014 | FMEA findings feed dimension scoring; S-014 validates post-correction quality |
| **S-012 + S-013** | S-012 + S-013 (parallel or sequential) | Complementary: FMEA bottom-up decomposition + Inversion top-down assumption testing |

**Optimal C3 sequence:** S-003 -> S-007 -> S-002 -> S-004 -> S-012 -> S-013 -> S-014

---

## Prerequisites

### Required Inputs

- [ ] Deliverable artifact (design, plan, architecture, API specification, etc.)
- [ ] Criticality level classification (C3 or C4)
- [ ] S-003 Steelman output (H-16 compliance for overall C3+ sequence)
- [ ] Quality framework SSOT (`quality-enforcement.md`) for dimension weights and threshold
- [ ] Domain expertise sufficient to identify realistic failure modes per component

### Context Requirements

The executor must understand the deliverable's structure well enough to decompose it into discrete elements, have domain knowledge sufficient to enumerate realistic failure modes for each element, and understand how failures in one element cascade to others. Access to S-004 Pre-Mortem output (if available) helps focus FMEA on highest-risk areas.

### Ordering Constraints

**H-16 Context:** S-003 Steelman MUST have been applied before the C3+ adversarial sequence begins. While H-16 specifically names S-002/S-004/S-001, S-012 operates on the Steelman-strengthened deliverable in a compliant C3+ workflow.

**Recommended sequence:**
1. S-003 Steelman (strengthen the deliverable)
2. S-007 Constitutional AI Critique (HARD rule compliance)
3. S-002 Devil's Advocate (challenge claims)
4. S-004 Pre-Mortem (prospective hindsight)
5. **S-012 FMEA (this strategy -- systematic decomposition)**
6. S-013 Inversion (assumption stress-testing)
7. S-014 LLM-as-Judge (score the revised deliverable)

**Minimum:** S-003 before the adversarial sequence. S-014 after S-012 for dimensional scoring.

---

## Execution Protocol

### RPN Scale Reference

The RPN (Risk Priority Number) is the product of three independent ratings (each 1-10):

| Rating | Severity (S) | Occurrence (O) | Detection (D) |
|--------|-------------|-----------------|----------------|
| 1-2 | Negligible impact | Very unlikely | Almost certain to detect |
| 3-4 | Minor degradation | Unlikely | High detection probability |
| 5-6 | Moderate quality gap | Possible | Moderate detection probability |
| 7-8 | Significant deficiency | Likely | Low detection probability |
| 9-10 | Deliverable-invalidating | Very likely/certain | Undetectable without this analysis |

**RPN Range:** 1 (lowest risk) to 1000 (highest risk). Higher RPN = higher priority for corrective action.

### Step 1: Decompose the Deliverable

**Action:** Break the deliverable into discrete, analyzable elements.

**Procedure:**
1. Identify the deliverable's top-level structure (sections, layers, components, phases, interfaces)
2. Decompose each top-level element into sub-elements where meaningful (e.g., a "Decision" section decomposes into: problem statement, alternatives analysis, selection rationale, consequences)
3. Create an element inventory with unique identifiers
4. Target: 5-15 elements for a typical C3 deliverable; more for C4
5. Verify decomposition is MECE (Mutually Exclusive, Collectively Exhaustive) -- no gaps, no overlaps

**Decision Point:**
- If fewer than 5 elements identified: deliverable may not warrant FMEA. Consider redirect to S-013 (Inversion).
- If more than 20 elements: group related sub-elements to keep analysis tractable.

**Output:** Element inventory table with identifiers and descriptions.

### Step 2: Enumerate Failure Modes per Element

**Action:** For each element, systematically identify ALL ways it could fail to achieve its purpose.

**Procedure:**
For each element, apply the 5 failure mode lenses:

1. **Missing:** Element is absent, incomplete, or has gaps (e.g., missing section, undefined interface)
2. **Incorrect:** Element contains errors, contradictions, or wrong information (e.g., wrong metric, flawed logic)
3. **Ambiguous:** Element can be interpreted multiple ways (e.g., vague requirement, undefined term)
4. **Inconsistent:** Element contradicts other elements in the deliverable (e.g., claims conflict, data disagrees)
5. **Insufficient:** Element is present but inadequate in depth, evidence, or rigor (e.g., weak justification, anecdotal evidence)

For each failure mode:
1. Describe the specific failure (not "missing content" but "Section 3 lacks rollback procedure for Phase 2 failure")
2. Identify the effect on the deliverable and downstream consumers
3. Assign FM-NNN-{execution_id} identifier

**Output:** Failure mode inventory with FM-NNN-{execution_id} identifiers, one or more per element.

### Step 3: Rate Severity, Occurrence, and Detection

**Action:** Assign S/O/D ratings (each 1-10) to each failure mode using the RPN Scale Reference above.

**Procedure:**
For each failure mode:
1. **Severity (S):** How bad is the effect if this failure mode occurs? (1 = negligible, 10 = deliverable-invalidating)
2. **Occurrence (O):** How likely is this failure mode to be present? (1 = very unlikely, 10 = certain)
3. **Detection (D):** How likely is this failure to go undetected without FMEA? (1 = obvious, 10 = undetectable)
4. **Calculate RPN:** S x O x D

**Severity Classification (mapping to standard severity):**
- **Critical:** RPN >= 200 OR Severity rating >= 9. Blocks acceptance.
- **Major:** RPN 80-199 OR Severity rating 7-8. Requires corrective action.
- **Minor:** RPN < 80 AND Severity rating <= 6. Improvement opportunity.

**Decision Point:**
- If any failure mode has RPN >= 200: Flag as Critical. Deliverable has high-risk failure modes.
- If total failure modes with RPN > 80 exceed 30% of all modes: Deliverable has systemic quality issues.

**Output:** Rated failure mode table with S, O, D, RPN, and severity classification for each FM-NNN.

### Step 4: Prioritize and Develop Corrective Actions

**Action:** Rank failure modes by RPN and develop specific corrective actions for the highest-priority findings.

**Procedure:**
1. Sort all failure modes by RPN (highest first)
2. For each Critical finding (RPN >= 200): develop a mandatory corrective action with specific deliverable change
3. For each Major finding (RPN 80-199): develop a recommended corrective action
4. For Minor findings: note improvement opportunity; corrective action optional
5. Map each finding to the affected S-014 scoring dimension
6. Estimate post-correction RPN (what the RPN would be after the corrective action)

**Output:** Prioritized corrective action table with FM-NNN identifiers, current RPN, corrective action, and estimated post-correction RPN.

### Step 5: Synthesize and Score Impact

**Action:** Produce a consolidated FMEA assessment mapping findings to quality dimensions.

**Procedure:**
1. Aggregate findings: count Critical, Major, Minor; sum RPNs
2. Map findings to the 6 scoring dimensions and assess net impact per dimension
3. Identify the element with the highest total RPN (most failure-prone component)
4. Determine overall assessment: significant rework required / targeted corrections / acceptable with monitoring
5. Apply H-15 self-review before presenting

**Output:** Scoring Impact table, overall assessment, and corrective action guidance.

---

## Output Format

Every S-012 execution MUST produce an FMEA report with these sections:

### 1. Header

```markdown
# FMEA Report: {{DELIVERABLE_NAME}}

**Strategy:** S-012 FMEA (Failure Mode and Effects Analysis)
**Deliverable:** {{Artifact name, file path, or work item ID}}
**Criticality:** {{C3/C4}}
**Date:** {{ISO 8601 date}}
**Reviewer:** {{Agent ID or human name}}
**H-16 Compliance:** S-003 Steelman applied on {{date}} (confirmed)
**Elements Analyzed:** {{count}} | **Failure Modes Identified:** {{count}} | **Total RPN:** {{sum}}
```

### 2. Summary

2-3 sentence overall assessment covering: number of elements analyzed, failure modes found, highest-RPN finding, and recommendation (ACCEPT with corrections / REVISE / REJECT).

### 3. Findings Table

| ID | Element | Failure Mode | S | O | D | RPN | Severity | Corrective Action | Affected Dimension |
|----|---------|-------------|---|---|---|-----|----------|-------------------|--------------------|
| FM-001-{execution_id} | {{Element}} | {{Failure}} | {{1-10}} | {{1-10}} | {{1-10}} | {{RPN}} | Critical | {{Action}} | {{Dimension}} |

**Finding ID Format:** `FM-{NNN}-{execution_id}` where execution_id is a short timestamp or session identifier (e.g., `FM-001-20260215T1430`) to prevent ID collisions across tournament executions.

Severity classification: see [Step 3](#step-3-rate-severity-occurrence-and-detection).

### 4. Finding Details

Expanded description for each Critical and Major finding: Element, Failure Mode, Effect, S/O/D rationale, Corrective Action, Acceptance Criteria, Post-Correction RPN estimate.

### 5. Recommendations

Prioritized corrective actions grouped by severity (Critical first, then Major). Each entry: FM-NNN identifier, corrective action, acceptance criteria, estimated RPN reduction.

### 6. Scoring Impact

Map FMEA findings to S-014 scoring dimensions (Completeness 0.20, Internal Consistency 0.20, Methodological Rigor 0.20, Evidence Quality 0.15, Actionability 0.15, Traceability 0.10). For each dimension, assess Impact (Positive/Negative/Neutral) with rationale referencing specific FM-NNN findings.

### Evidence Requirements

Each finding MUST include: specific element reference, description of the failure mode with concrete effects, S/O/D ratings with justification, and specific corrective action.

---

## Scoring Rubric

This rubric evaluates the **quality of the S-012 FMEA execution itself** (meta-evaluation), not the deliverable being reviewed.

### Threshold Bands

**SSOT threshold (from quality-enforcement.md, MUST NOT be redefined):** >= 0.92 weighted composite score. Below threshold = REJECTED; revision required per H-13.

**Operational bands for S-012 execution quality:**

| Band | Score Range | Outcome |
|------|------------|---------|
| PASS | >= 0.92 | Strategy execution accepted; decomposition thorough and RPN ratings well-calibrated |
| REVISE | 0.85 - 0.91 | Strategy execution requires targeted revision; close to threshold |
| REJECTED | < 0.85 | Strategy execution inadequate; significant rework required (H-13) |

> **Note:** The SSOT defines only the 0.92 threshold with REJECTED as the below-threshold outcome. The REVISE band (0.85-0.91) is a template-specific operational category (not sourced from quality-enforcement.md) to distinguish near-threshold executions requiring targeted improvements from those requiring significant rework. Both REVISE and REJECTED trigger the revision cycle per H-13.

### Dimension Weights

From quality-enforcement.md (MUST NOT be redefined):

| Dimension | Weight | Measures (for S-012 execution quality) |
|-----------|--------|----------------------------------------|
| Completeness | 0.20 | MECE decomposition; all elements examined; all 5 failure mode lenses applied per element |
| Internal Consistency | 0.20 | S/O/D ratings calibrated consistently across elements; RPN calculations correct; no contradictory assessments |
| Methodological Rigor | 0.20 | All 5 steps executed; FMEA methodology followed faithfully; RPN scale applied systematically |
| Evidence Quality | 0.15 | Each failure mode backed by specific element references; S/O/D ratings justified |
| Actionability | 0.15 | Corrective actions concrete and implementable; post-correction RPN estimated |
| Traceability | 0.10 | Findings linked to elements and dimensions; FM-NNN identifiers used consistently |

### Strategy-Specific Rubric

| Dimension (Weight) | 0.95+ | 0.90-0.94 | 0.85-0.89 | <0.85 |
|--------------------|-------|-----------|-----------|-------|
| **Completeness (0.20)** | MECE decomposition; ALL 5 lenses per element; 2+ failure modes per element; every element examined | Most elements examined; most lenses applied; some elements have only 1 failure mode | Core elements examined; 2-3 lenses applied; several elements skipped | Partial decomposition; few lenses; major elements unexamined |
| **Internal Consistency (0.20)** | S/O/D ratings perfectly calibrated across elements; all RPN calculations verified; no contradictory ratings | Mostly calibrated; RPNs correct; minor calibration drift between elements | Some calibration inconsistencies; RPNs correct but ratings questionable | Arbitrary ratings; calculation errors; contradictory assessments |
| **Methodological Rigor (0.20)** | ALL 5 steps executed; FMEA methodology followed precisely; RPN scale consistently applied; all failure modes classified | All steps executed; methodology mostly followed; minor deviations documented | 4 steps executed; methodology partially followed; RPN scale loosely applied | Steps skipped; ad hoc failure enumeration; no systematic RPN |
| **Evidence Quality (0.15)** | Every failure mode references specific element content; S/O/D ratings justified with concrete reasoning; effects described in detail | Most failure modes have specific evidence; ratings mostly justified; effects described | Some failure modes have evidence; ratings partially justified; effects vague | Failure modes speculative; ratings unjustified; effects not described |
| **Actionability (0.15)** | ALL Critical/Major findings have specific corrective actions with acceptance criteria and post-correction RPN estimates | Most findings have corrective actions; acceptance criteria for Critical; post-correction RPN estimated | Some corrective actions present; criteria vague; post-correction RPN not estimated | No corrective actions; findings are observations only |
| **Traceability (0.10)** | Every finding traces to specific element; all findings mapped to dimensions; FM-NNN used consistently; element inventory complete | Most findings traceable; dimension mapping present; FM-NNN consistent | Some findings traceable; partial dimension mapping; FM-NNN inconsistent | Not traceable; no dimension mapping; no element inventory |

---

## Examples

### Example 1: C3 API Contract Design Review

**Context:**
- **Deliverable:** API contract specification for Jerry CLI plugin interface (defines how external plugins interact with the Jerry framework)
- **Criticality Level:** C3 (Significant) -- >10 files affected, public API, >1 day to reverse
- **Scenario:** S-003 Steelman applied (H-16), S-002 and S-004 completed; now S-012 FMEA decomposes into component failure modes

**Before (Key Elements from API Contract after S-003 Steelman):**

The API contract defines: (1) Plugin registration interface, (2) Event subscription mechanism, (3) Command extension points, (4) Error handling protocol, (5) Versioning scheme. S-003 strengthened the rationale; S-004 identified high-level risks around backward compatibility.

**Strategy Execution (Key Steps):**

**Step 1: Decompose** -- 5 top-level elements identified (registration, events, commands, errors, versioning), decomposed into 12 sub-elements.

**Step 2: Enumerate Failure Modes** (selected findings):

| ID | Element | Failure Mode | S | O | D | RPN | Severity | Affected Dimension |
|----|---------|-------------|---|---|---|-----|----------|---------------------|
| FM-001-20260215T1600 | Event subscription | No mechanism for plugin to unsubscribe from events; memory leak on plugin unload | 8 | 7 | 8 | 448 | Critical | Completeness |
| FM-002-20260215T1600 | Error handling | Error codes not defined; plugins cannot distinguish recoverable from fatal errors | 7 | 8 | 5 | 280 | Critical | Actionability |
| FM-003-20260215T1600 | Versioning | No deprecation policy for API changes; plugins break silently on major version bumps | 8 | 5 | 7 | 280 | Critical | Methodological Rigor |
| FM-004-20260215T1600 | Command extension | No namespace isolation; plugin commands can collide with core commands | 6 | 6 | 6 | 216 | Critical | Internal Consistency |
| FM-005-20260215T1600 | Registration | No capability declaration; framework cannot validate plugin compatibility before loading | 5 | 4 | 5 | 100 | Major | Evidence Quality |

**After (API Contract Revised):**

The creator addressed findings: added unsubscribe mechanism with cleanup hook (FM-001), defined error code taxonomy with recovery guidance (FM-002), added deprecation policy with 2-version support window (FM-003), added plugin namespace prefix requirement (FM-004), and added capability manifest to registration (FM-005). Total RPN reduced from 1324 to estimated 280.

**Scoring Impact:**

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | FM-001: Missing unsubscribe mechanism is a fundamental gap |
| Internal Consistency | 0.20 | Negative | FM-004: Namespace collision risk creates inconsistent behavior |
| Methodological Rigor | 0.20 | Negative | FM-003: No deprecation policy undermines API contract rigor |
| Evidence Quality | 0.15 | Negative | FM-005: No capability validation means contract is unverifiable |
| Actionability | 0.15 | Negative | FM-002: Undefined error codes make plugin development unactionable |
| Traceability | 0.10 | Neutral | API contract traces to architecture ADR and plugin requirements |

---

## Integration

### Canonical Pairings

See [Pairing Recommendations](#pairing-recommendations) for the full pairing table (S-003, S-004, S-013, S-014) with rationale and optimal sequence.

### H-16 Compliance

**H-16 Rule:** S-003 MUST execute before critique strategies (S-002, S-004, S-001). S-012 is not directly named in H-16 but operates within the C3+ sequence where H-16 is already satisfied. See [Prerequisites: Ordering Constraints](#ordering-constraints) for full sequence.

### Criticality-Based Selection Table

From quality-enforcement.md (MUST NOT modify):

| Level | Required Strategies | Optional Strategies | S-012 Status |
|-------|---------------------|---------------------|--------------|
| C1 | S-010 | S-003, S-014 | NOT USED |
| C2 | S-007, S-002, S-014 | S-003, S-010 | NOT USED |
| C3 | C2 + S-004, S-012, S-013 | S-001, S-003, S-010, S-011 | **REQUIRED** |
| C4 | All 10 selected | None | **REQUIRED** |

**Source:** quality-enforcement.md Criticality Levels table (SSOT). Values MUST match exactly.

### Cross-References

**SSOT:** `.context/rules/quality-enforcement.md` (H-13 threshold, dimension weights, criticality levels) | `ADR-EPIC002-001` (strategy selection, score 3.75) | `ADR-EPIC002-002` (enforcement architecture) | `.context/templates/adversarial/TEMPLATE-FORMAT.md` v1.1.0

**Strategy Templates:** `s-003-steelman.md` (prerequisite via H-16 for C3+ sequence) | `s-004-pre-mortem.md` (Pre-Mortem identifies high-level risks; FMEA decomposes) | `s-013-inversion.md` (complementary: bottom-up decomposition + top-down assumption inversion) | `s-014-llm-as-judge.md` (scores post-correction revision) | `s-002-devils-advocate.md` (complementary: argument attack vs. component analysis)

**Academic:** MIL-P-1629, AIAG/VDA (2019), Stamatis (2003), IEC 60812:2018, NPR 7123.1D. See file header.

**HARD Rules:** H-13 (threshold >= 0.92), H-14 (creator-critic cycle), H-15 (self-review), H-16 (steelman before critique), H-17 (scoring required) -- all from quality-enforcement.md

---

<!-- VALIDATION: 8 sections present | H-23/H-24 nav | FM-NNN prefix | H-16 documented | SSOT weights match | REVISE band noted | C3 example with Critical findings | RPN methodology | No absolute paths | 4-band rubric | Under 500 lines -->

---

*Template Version: 1.0.0*
*Format Conformance: TEMPLATE-FORMAT.md v1.1.0*
*SSOT: `.context/rules/quality-enforcement.md`*
*Created: 2026-02-15*
*Enabler: EN-808*
