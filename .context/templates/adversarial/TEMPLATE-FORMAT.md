# Adversarial Strategy Execution Template -- Format Standard

<!--
TEMPLATE: Adversarial Strategy Execution Template Format
VERSION: 1.0.0 | DATE: 2026-02-14
SOURCE: EPIC-003 Quality Framework, quality-enforcement.md SSOT
ENABLER: EN-801 (Template Format Standard)
STATUS: ACTIVE

Canonical format that ALL adversarial strategy execution templates MUST follow.
Defines 8 required sections, their ordering, and content expectations.
All 10 selected strategy templates (S-001 through S-014) are validated against this format.
-->

> **Type:** template-format
> **Status:** ACTIVE
> **Version:** 1.0.0
> **Date:** 2026-02-14
> **Source:** quality-enforcement.md SSOT, ADR-EPIC002-001, ADR-EPIC002-002
> **Enabler:** EN-801

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Overview](#overview) | What this format defines and how to use it |
| [Strategy Catalog Reference](#strategy-catalog-reference) | The 10 strategies requiring templates |
| [Section 1: Identity](#section-1-identity) | Strategy identification and classification |
| [Section 2: Purpose](#section-2-purpose) | When and why to apply the strategy |
| [Section 3: Prerequisites](#section-3-prerequisites) | Required inputs and context |
| [Section 4: Execution Protocol](#section-4-execution-protocol) | Step-by-step reproducible procedure |
| [Section 5: Output Format](#section-5-output-format) | Required structure for strategy output |
| [Section 6: Scoring Rubric](#section-6-scoring-rubric) | Quality evaluation of strategy execution |
| [Section 7: Examples](#section-7-examples) | Concrete before/after demonstrations |
| [Section 8: Integration](#section-8-integration) | Cross-strategy pairing and criticality mapping |
| [Validation Checklist](#validation-checklist) | Compliance verification for templates |
| [Constants Reference](#constants-reference) | Authoritative values from quality-enforcement.md |

---

## Overview

This document defines the **canonical format** for all adversarial strategy execution templates. Every strategy template MUST include the 8 sections defined here, in the specified order.

**Scope:** 10 selected strategies from ADR-EPIC002-001.

**Authority:** All constants (thresholds, weights, criticality levels) are sourced from `.context/rules/quality-enforcement.md`. Templates MUST NOT redefine these constants.

**File naming:** `.context/templates/adversarial/{S-NNN}-{strategy-slug}.md`

**Target length per template:** 200-400 lines.

---

## Strategy Catalog Reference

| ID | Strategy | Score | Family | Finding Prefix |
|----|----------|-------|--------|----------------|
| S-014 | LLM-as-Judge | 4.40 | Iterative Self-Correction | LJ-NNN |
| S-003 | Steelman Technique | 4.30 | Dialectical Synthesis | SM-NNN |
| S-013 | Inversion Technique | 4.25 | Structured Decomposition | IN-NNN |
| S-007 | Constitutional AI Critique | 4.15 | Iterative Self-Correction | CC-NNN |
| S-002 | Devil's Advocate | 4.10 | Role-Based Adversarialism | DA-NNN |
| S-004 | Pre-Mortem Analysis | 4.10 | Role-Based Adversarialism | PM-NNN |
| S-010 | Self-Refine | 4.00 | Iterative Self-Correction | SR-NNN |
| S-012 | FMEA | 3.75 | Structured Decomposition | FM-NNN |
| S-011 | Chain-of-Verification | 3.75 | Structured Decomposition | CV-NNN |
| S-001 | Red Team Analysis | 3.35 | Role-Based Adversarialism | RT-NNN |

Each strategy uses a unique 2-letter **Finding Prefix** for its findings (e.g., DA-001). Templates MUST define their prefix in Section 1.

---

## Section 1: Identity

Every template MUST begin with an Identity section containing these fields in a table:

| Field | Description | Example |
|-------|-------------|---------|
| Strategy ID | From quality-enforcement.md catalog | S-014 |
| Strategy Name | Full human-readable name | LLM-as-Judge |
| Family | Strategy family classification | Iterative Self-Correction |
| Composite Score | From ADR-EPIC002-001 | 4.40 |
| Finding Prefix | 2-letter code + NNN sequence | LJ-NNN |
| Version | Semantic version of the template | 1.0.0 |
| Date | Last updated date (ISO 8601) | 2026-02-14 |

**Criticality Tier Table (REQUIRED):** Each template MUST include a table showing where the strategy is REQUIRED, OPTIONAL, or NOT USED at each criticality level (C1-C4). Values are sourced from the Criticality Levels table in quality-enforcement.md.

---

## Section 2: Purpose

Every template MUST include a Purpose section with these subsections:

**When to Use:** At least 3 concrete scenarios with actionable trigger conditions.

**When NOT to Use:** At least 2 exclusions with reasoning and redirect to an alternative strategy where appropriate.

**Expected Outcome:** What a successful application produces. MUST be specific and measurable.

**Pairing Recommendations:** Which strategies pair with this one, in what order. MUST reference H-16 (Steelman before critique) where applicable. Format: "Run S-003 before S-002 (H-16 compliance)."

---

## Section 3: Prerequisites

Every template MUST include a Prerequisites section with:

**Required Inputs:** Checklist of artifacts and context needed before execution.

**Context Requirements:** Background knowledge or state assumed.

**Ordering Constraints:** Dependencies on prior strategy execution (e.g., H-16 requires S-003 before S-002).

---

## Section 4: Execution Protocol

The **core section**. MUST provide a step-by-step, reproducible procedure.

### Required Structure

1. **Numbered steps** (minimum 4) with clear, imperative actions
2. **Decision points** with explicit criteria for branching
3. **Output requirements** specifying what each step produces
4. **Finding identifiers** using the strategy-specific prefix

### Step Format

Each step MUST follow this structure:

```markdown
### Step N: {{STEP_TITLE}}

**Action:** {{Clear imperative description}}

**Procedure:**
1. {{Sub-step 1}}
2. {{Sub-step 2}}

**Decision Point (if applicable):**
- If {{condition A}}: {{action A}}
- If {{condition B}}: {{action B}}

**Output:** {{What this step produces}}
```

### Finding Documentation Format

Every finding MUST be documented as:

| ID | Finding | Severity | Evidence | Affected Dimension |
|----|---------|----------|----------|--------------------|
| {{PREFIX}}-001 | {{Description}} | Critical/Major/Minor | {{Reference}} | {{Dimension}} |

**Severity definitions:**
- **Critical:** Invalidates the deliverable or violates a HARD rule. Blocks acceptance.
- **Major:** Significant quality gap. Requires revision.
- **Minor:** Improvement opportunity. Does not block acceptance.

**Affected Dimension:** One of the 6 scoring dimensions (Completeness, Internal Consistency, Methodological Rigor, Evidence Quality, Actionability, Traceability).

---

## Section 5: Output Format

Every template MUST define the required structure of its output document.

### Required Output Sections

1. **Header:** Strategy ID, deliverable reviewed, date, reviewer, criticality level
2. **Summary:** Brief overall assessment (2-3 sentences)
3. **Findings Table:** All findings per the format in Section 4
4. **Finding Details:** Expanded description for each Critical and Major finding
5. **Recommendations:** Prioritized actions to address findings
6. **Scoring Impact:** Findings mapped to S-014 scoring dimensions

### Scoring Impact Table

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Positive/Negative/Neutral | {{Justification}} |
| Internal Consistency | 0.20 | Positive/Negative/Neutral | {{Justification}} |
| Methodological Rigor | 0.20 | Positive/Negative/Neutral | {{Justification}} |
| Evidence Quality | 0.15 | Positive/Negative/Neutral | {{Justification}} |
| Actionability | 0.15 | Positive/Negative/Neutral | {{Justification}} |
| Traceability | 0.10 | Positive/Negative/Neutral | {{Justification}} |

### Evidence Requirements

Each finding MUST include: specific reference to location in the deliverable, quotation or paraphrase of the problematic content, and explanation of why it is a finding.

---

## Section 6: Scoring Rubric

Every template MUST include a rubric for meta-evaluating the strategy execution quality.

### Threshold Bands (from quality-enforcement.md, MUST NOT be redefined)

| Band | Score Range | Outcome |
|------|------------|---------|
| PASS | >= 0.92 | Strategy execution accepted |
| REVISE | 0.85 - 0.91 | Strategy execution requires improvement |
| ESCALATE | < 0.85 | Strategy execution inadequate; escalate |

### Dimension Weights (from quality-enforcement.md, MUST NOT be redefined)

| Dimension | Weight | Measures (for strategy execution) |
|-----------|--------|-----------------------------------|
| Completeness | 0.20 | All steps executed; all deliverable aspects examined |
| Internal Consistency | 0.20 | No contradictory findings; consistent severity |
| Methodological Rigor | 0.20 | Procedure followed faithfully; no shortcuts |
| Evidence Quality | 0.15 | Each finding backed by specific evidence |
| Actionability | 0.15 | Recommendations concrete, prioritized, implementable |
| Traceability | 0.10 | Findings linked to source material and dimensions |

### Strategy-Specific Rubric (REQUIRED)

Each template MUST provide a scoring criteria table with 4 bands (0.95+, 0.90-0.94, 0.85-0.89, <0.85) for each of the 6 dimensions, with criteria specific to that strategy.

---

## Section 7: Examples

Every template MUST include at least one concrete example with:

1. **Context:** Deliverable being reviewed and criticality level
2. **Before:** Relevant portion of the deliverable before strategy application
3. **Strategy Execution:** Key steps applied to the example
4. **Findings:** Example findings using the strategy-specific identifiers and the standard findings table format
5. **After:** How the deliverable improved based on findings

---

## Section 8: Integration

Every template MUST include an Integration section with:

**Canonical Pairings:** Paired strategies with ordering rationale.

**H-16 Compliance:** Explicit documentation if this strategy is affected by H-16 (Steelman before critique).

**Criticality-Based Selection Table:** Which strategies run at C1-C4 and where this strategy fits. Values MUST match quality-enforcement.md:

| Level | Required Strategies | Optional Strategies |
|-------|---------------------|---------------------|
| C1 | S-010 | S-003, S-014 |
| C2 | S-007, S-002, S-014 | S-003, S-010 |
| C3 | C2 + S-004, S-012, S-013 | S-001, S-003, S-010, S-011 |
| C4 | All 10 selected | None |

**Cross-References:** Links to `.context/rules/quality-enforcement.md` and related strategy templates.

---

## Validation Checklist

Use this checklist to validate any strategy template against this format.

### Structure

- [ ] All 8 canonical sections present in order (Identity, Purpose, Prerequisites, Execution Protocol, Output Format, Scoring Rubric, Examples, Integration)
- [ ] H-23: Navigation table present
- [ ] H-24: Navigation table uses anchor links
- [ ] Metadata blockquote header present
- [ ] File length under 500 lines

### Content per Section

| Section | Validation Criteria |
|---------|---------------------|
| 1. Identity | 7 required fields; Criticality Tier table; values match SSOT |
| 2. Purpose | 3+ "When to Use"; 2+ "When NOT to Use"; measurable outcome; pairing recs |
| 3. Prerequisites | Input checklist; context reqs; ordering constraints (H-16) |
| 4. Execution Protocol | 4+ steps; step format followed; decision points; finding prefix; severity defs |
| 5. Output Format | 6 output sections; scoring impact table with correct weights; evidence reqs |
| 6. Scoring Rubric | Threshold bands match SSOT; weights match SSOT; strategy-specific 4-band rubric |
| 7. Examples | 1+ example; Before/After; findings with identifiers; severity applied |
| 8. Integration | Pairings; H-16; criticality table matches SSOT; cross-references |

---

## Constants Reference

All values sourced from `.context/rules/quality-enforcement.md`. MUST NOT be redefined in templates.

### Quality Gate

| Constant | Value |
|----------|-------|
| Threshold | >= 0.92 weighted composite |
| Minimum Cycle Count | 3 iterations (creator -> critic -> revision) |
| Below Threshold Action | REJECTED; revision required (H-13) |

### Scoring Dimensions and Weights

| Dimension | Weight |
|-----------|--------|
| Completeness | 0.20 |
| Internal Consistency | 0.20 |
| Methodological Rigor | 0.20 |
| Evidence Quality | 0.15 |
| Actionability | 0.15 |
| Traceability | 0.10 |

### Criticality Levels

| Level | Name | Required Strategies | Optional Strategies |
|-------|------|---------------------|---------------------|
| C1 | Routine | S-010 | S-003, S-014 |
| C2 | Standard | S-007, S-002, S-014 | S-003, S-010 |
| C3 | Significant | C2 + S-004, S-012, S-013 | S-001, S-003, S-010, S-011 |
| C4 | Critical | All 10 selected | None |

### Relevant HARD Rules

| ID | Rule | Relevance to Templates |
|----|------|------------------------|
| H-13 | Quality threshold >= 0.92 for C2+ | Scoring Rubric thresholds |
| H-14 | Creator-critic-revision cycle (3 min) | Execution Protocol iteration count |
| H-15 | Self-review before presenting (S-010) | S-010 template prerequisite flow |
| H-16 | Steelman before critique (S-003) | Ordering constraint for S-002, S-004, S-001 |
| H-17 | Quality scoring REQUIRED for deliverables | Output Format scoring impact |
| H-18 | Constitutional compliance check (S-007) | S-007 template applicability |

---

<!--
TEMPLATE NOTES:

1. INSTANTIATION: Each strategy template replaces {{PLACEHOLDER}} values.
   Strategy-specific content fills the Execution Protocol and Examples.
   Constants (weights, thresholds, criticality sets) are NEVER modified.
   Finding prefixes are assigned in the Strategy Catalog Reference above.

2. VALIDATION: Use the Validation Checklist to verify compliance.
   Templates failing validation MUST be revised. Validation is part of
   the creator-critic-revision cycle (H-14).

3. MAINTENANCE: This format is versioned; changes require C3+ review
   (AE-002 applies). quality-enforcement.md is the SSOT.

4. TRACEABILITY:
   - EN-801: This document (Template Format Standard)
   - EN-803 through EN-809: Individual strategy templates
   - quality-enforcement.md: SSOT for all constants
   - ADR-EPIC002-001: Strategy selection and composite scores
   - ADR-EPIC002-002: Enforcement architecture

VERSION: 1.0.0 | CREATED: 2026-02-14 | ENABLER: EN-801
-->
