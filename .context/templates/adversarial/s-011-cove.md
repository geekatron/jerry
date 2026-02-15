# S-011: Chain-of-Verification -- Adversarial Strategy Execution Template

<!--
TEMPLATE: S-011 Chain-of-Verification Adversarial Strategy Execution Template
VERSION: 1.0.0 | DATE: 2026-02-15
SOURCE: quality-enforcement.md SSOT, ADR-EPIC002-001, TEMPLATE-FORMAT.md v1.1.0
ENABLER: EN-809 (S-011 Template)
STATUS: ACTIVE
CONFORMANCE: TEMPLATE-FORMAT.md v1.1.0

Academic Foundation:
- Dhuliawala et al. (2023): "Chain-of-Verification Reduces Hallucination in Large Language Models" (Meta AI)
- Weng et al. (2023): Factual consistency verification in LLM-generated content
- Min et al. (2023): FActScore -- Fine-grained Atomic Evaluation of Factual Precision
- Manakul et al. (2023): SelfCheckGPT -- Zero-Resource Black-Box Hallucination Detection

Origin: Dhuliawala et al. (2023), Meta AI research.
Domain: Factual Verification, Hallucination Detection, Consistency Checking.
Key insight: Generating verification questions about claims, answering them independently
(without referring to the original), and checking for inconsistencies systematically detects
factual errors, hallucinations, and cross-reference failures that direct review misses.
-->

> **Type:** adversarial-strategy-template
> **Status:** ACTIVE
> **Version:** 1.0.0
> **Date:** 2026-02-15
> **Source:** quality-enforcement.md, ADR-EPIC002-001, ADR-EPIC002-002
> **Format Conformance:** TEMPLATE-FORMAT.md v1.1.0
> **Enabler:** EN-809

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Identity](#identity) | Strategy classification and metadata |
| [Purpose](#purpose) | When and why to apply Chain-of-Verification |
| [Prerequisites](#prerequisites) | Required inputs and ordering constraints (H-16) |
| [Execution Protocol](#execution-protocol) | Step-by-step claim extraction and independent verification procedure |
| [Output Format](#output-format) | Required structure for CoVe report |
| [Scoring Rubric](#scoring-rubric) | Meta-evaluation of strategy execution quality |
| [Examples](#examples) | Concrete C3 demonstration with findings |
| [Integration](#integration) | Cross-strategy pairing, H-16 compliance, criticality mapping |

---

## Identity

| Field | Value |
|-------|-------|
| Strategy ID | S-011 |
| Strategy Name | Chain-of-Verification |
| Family | Structured Decomposition |
| Composite Score | 3.75 |
| Finding Prefix | CV-NNN |
| Version | 1.0.0 |
| Date | 2026-02-15 |

### Criticality Tier Table

| Level | Name | Status | Notes |
|-------|------|--------|-------|
| C1 | Routine | NOT USED | C1 enforces HARD rules only; CoVe not required or optional |
| C2 | Standard | NOT USED | S-011 not in C2 required or optional sets |
| C3 | Significant | OPTIONAL | Part of C3 optional set (S-001, S-003, S-010, S-011) |
| C4 | Critical | REQUIRED | All 10 strategies required; tournament mode |

**Source:** quality-enforcement.md Criticality Levels table (SSOT).

**Foundation:** Dhuliawala et al. (2023) demonstrated that LLMs can significantly reduce hallucinations by generating verification questions about their own claims, answering those questions independently (without access to the original output), and flagging inconsistencies. Min et al. (2023) showed that decomposing statements into atomic facts enables fine-grained factual precision scoring. This decompose-verify-compare pattern detects errors that holistic review misses.

**Jerry Implementation:** Extracts all testable claims from a deliverable (factual assertions, SSOT references, cross-references, numerical values, rule citations), generates verification questions for each, answers those questions independently using source documents, and flags discrepancies as CV-NNN findings. Particularly valuable for verifying SSOT alignment, cross-reference accuracy, and quoted values. H-16 compliance: S-003 SHOULD run before S-011 (strengthen before verifying, though CoVe is verification-oriented rather than critique-oriented, making H-16 indirect).

---

## Purpose

### When to Use

1. **C4 Critical Deliverable Review:** ALL Critical deliverables MUST undergo Chain-of-Verification (required at C4). Apply after Steelman (S-003) has strengthened the deliverable per H-16.

2. **SSOT Alignment Verification:** When a deliverable quotes values, thresholds, weights, or constants from a Single Source of Truth document. CoVe independently verifies that quoted values match their source -- a common failure mode when documents evolve independently.

3. **Cross-Reference Accuracy:** When a deliverable references other documents, strategies, rules, or decisions. CoVe verifies that referenced content actually says what is claimed -- catching broken references, outdated citations, and mischaracterizations.

4. **Governance and Rule Documentation:** When the deliverable defines or references HARD rules, criticality levels, or enforcement mechanisms. CoVe verifies that every rule citation, threshold value, and criticality assignment matches the authoritative source exactly.

### When NOT to Use

1. **Purely Creative or Design Content:** When the deliverable contains subjective design decisions, creative proposals, or opinion-based content where "facts" are inherently arguable. Redirect to S-002 (Devil's Advocate) for challenging subjective claims or S-004 (Pre-Mortem) for risk analysis.

2. **Deliverables With No Testable Factual Claims:** If the deliverable makes no assertions that can be independently verified (no quoted values, no cross-references, no rule citations), CoVe has nothing to verify. Redirect to S-013 (Inversion) for assumption stress-testing.

### Expected Outcome

A Chain-of-Verification report containing:
- Claim inventory: all testable factual claims extracted from the deliverable (minimum 5)
- Verification question set: specific questions generated for each claim
- Independent verification results: answers derived from source documents without deliverable reference
- Discrepancy analysis: comparison of original claims against independent verification
- CV-NNN identified findings with severity classification (Critical/Major/Minor)
- Correction recommendations for all verified discrepancies
- Mapping of findings to the 6 S-014 scoring dimensions
- Measurable quality improvement when corrections are applied (target: 0.03+ composite score increase)

### Pairing Recommendations

**H-16 Compliance (INDIRECT):** S-003 Steelman SHOULD run before S-011 CoVe. While CoVe is verification-oriented rather than critique-oriented (making H-16 indirect), strengthening the deliverable first ensures CoVe verifies the strongest version of factual claims.

| Pairing | Order | Rationale |
|---------|-------|-----------|
| **S-003 + S-011** | S-003 -> S-011 | Steelman strengthens claims before CoVe verifies them |
| **S-011 + S-014** | S-011 -> S-014 | Verified claims feed accurate dimension scoring |
| **S-007 + S-011** | S-007 -> S-011 | Constitutional check flags rule violations; CoVe verifies cited values |
| **S-011 + S-001** | S-011 -> S-001 | CoVe establishes factual baseline; Red Team attacks from verified foundation |

**Optimal C3 sequence:** S-003 -> S-007 -> S-002 -> S-004 -> S-012 -> S-013 -> S-011 -> S-014

---

## Prerequisites

### Required Inputs

- [ ] Deliverable artifact containing factual claims, references, or quoted values
- [ ] Criticality level classification (C3 optional or C4 required)
- [ ] S-003 Steelman output (H-16 indirect compliance: Steelman SHOULD have been applied first)
- [ ] Source documents referenced by the deliverable (SSOT files, ADRs, rule documents)
- [ ] Quality framework SSOT (`quality-enforcement.md`) for dimension weights and threshold

### Context Requirements

The executor must have access to all source documents cited or referenced in the deliverable, familiarity with the deliverable's domain sufficient to identify testable claims, and the ability to answer verification questions independently using source materials without referring to the deliverable's characterization of those sources.

### Ordering Constraints

**H-16 (INDIRECT):** S-003 Steelman SHOULD be applied before S-011 CoVe. While CoVe is verification-oriented (not critique-oriented), H-16's spirit of strengthening before challenging applies. Executing S-011 without prior S-003 is not a strict H-16 violation but is discouraged.

**Recommended sequence:**
1. S-010 Self-Refine (creator self-review)
2. S-003 Steelman (strengthen the deliverable)
3. S-007 Constitutional AI Critique (HARD rule compliance)
4. S-002 Devil's Advocate (challenge current claims)
5. S-004 Pre-Mortem Analysis (imagine future failures)
6. S-012 FMEA (decompose failure modes)
7. S-013 Inversion (stress-test assumptions)
8. **S-011 Chain-of-Verification (this strategy)**
9. S-001 Red Team Analysis (adversarial exploitation)
10. S-014 LLM-as-Judge (score the revised deliverable)

**Minimum:** S-003 before S-011 (recommended). S-014 after S-011 for dimensional scoring.

---

## Execution Protocol

### Step 1: Extract Claims

**Action:** Read the deliverable and extract all testable factual claims, assertions, references, and cited values.

**Procedure:**
1. Read the deliverable and S-003 Steelman output (if no S-003 output exists, note the gap but proceed -- H-16 is indirect for CoVe)
2. Extract claims in these categories:
   - **Quoted values:** Numbers, thresholds, weights, percentages cited from source documents
   - **Rule citations:** References to HARD rules (H-01 through H-24), their content, and consequences
   - **Cross-references:** Claims about what other documents contain or state
   - **Historical assertions:** Claims about decisions made, rationale given, or precedents set
   - **Behavioral claims:** Assertions about how systems, processes, or frameworks behave
3. For each claim, record: the exact text from the deliverable, the claimed source, and the claim type
4. Assign claim identifiers: CL-001, CL-002, etc. (internal tracking, not finding IDs)

**Decision Point:**
- If fewer than 5 testable claims extracted: the deliverable may not be suitable for CoVe. Consider whether claims are implicit (unstated assumptions that can be extracted) or whether to redirect to S-013 (Inversion).
- If 5+ claims extracted: Proceed to Step 2.

**Output:** Claim inventory with CL-NNN identifiers, exact text, claimed sources, and claim types.

### Step 2: Generate Verification Questions

**Action:** For each extracted claim, formulate specific verification questions that would confirm or refute the claim.

**Procedure:**
1. For each claim, generate 1-3 verification questions that:
   - Can be answered independently using only the source document (not the deliverable)
   - Are specific enough to yield a definitive answer
   - Test the exact assertion made, not a paraphrase
2. For quoted values: "What is the exact value of X in source document Y?"
3. For rule citations: "What does rule H-NN state in quality-enforcement.md?"
4. For cross-references: "What does document X actually say about topic Y?"
5. For behavioral claims: "According to source Z, how does mechanism W function?"

**Output:** Verification question set with VQ-NNN identifiers linked to CL-NNN claims.

### Step 3: Independent Verification

**Action:** Answer each verification question using ONLY the source documents, without referring to the deliverable's characterization.

**Procedure:**
1. For each verification question, locate the relevant source document
2. Read the source document independently -- do NOT re-read the deliverable's claim
3. Answer the verification question based solely on the source material
4. Record the independent answer with exact quotes or values from the source
5. Note any cases where the source document does not contain the claimed information

**Decision Point:**
- If source document is unavailable: mark the claim as UNVERIFIABLE and note the gap. This itself may be a finding (referencing non-existent or inaccessible sources).
- If source document is available: record independent answer and proceed to Step 4.

**Output:** Independent verification answers with source document references and exact quotes.

### Step 4: Consistency Check

**Action:** Compare each independent verification answer against the original claim to identify discrepancies.

**Procedure:**
1. For each claim-answer pair, classify the result:
   - **VERIFIED:** Independent answer matches the claim exactly
   - **MINOR DISCREPANCY:** Independent answer is close but differs in non-material ways (e.g., rounding, paraphrasing that preserves meaning)
   - **MATERIAL DISCREPANCY:** Independent answer contradicts or significantly differs from the claim
   - **UNVERIFIABLE:** Source document unavailable or does not address the claim
2. For each MATERIAL DISCREPANCY and UNVERIFIABLE result, create a CV-NNN finding:
   - Describe the discrepancy in specific terms (what the deliverable claims vs. what the source says)
   - Assess **severity** using standard definitions (see below)
   - Map to affected scoring dimension
3. For MINOR DISCREPANCY results, assess whether the deviation could cause downstream errors

**Severity Definitions:**
- **Critical:** Claim contradicts source on a material point that would invalidate the deliverable or violate a HARD rule. Blocks acceptance.
- **Major:** Claim mischaracterizes source in a way that could mislead readers or cause incorrect downstream decisions. Requires correction.
- **Minor:** Claim paraphrases source imprecisely but preserves essential meaning. Improvement opportunity.

**Output:** Consistency check results with CV-NNN findings for all discrepancies.

### Step 5: Synthesize and Score Impact

**Action:** Produce a consolidated verification assessment mapping findings to quality dimensions.

**Procedure:**
1. Aggregate verification results: count VERIFIED, MINOR DISCREPANCY, MATERIAL DISCREPANCY, UNVERIFIABLE
2. Aggregate findings by severity: count Critical, Major, Minor
3. Calculate verification rate: VERIFIED / total claims
4. Map findings to the 6 scoring dimensions and assess net impact per dimension
5. Determine overall assessment: corrections required / minor revisions / verified clean
6. Apply H-15 self-review before presenting

**Output:** Verification summary, scoring impact table, overall assessment, and correction guidance.

---

## Output Format

Every S-011 execution MUST produce a Chain-of-Verification report with these sections:

### 1. Header

```markdown
# Chain-of-Verification Report: {{DELIVERABLE_NAME}}

**Strategy:** S-011 Chain-of-Verification
**Deliverable:** {{Artifact name, file path, or work item ID}}
**Criticality:** {{C3/C4}}
**Date:** {{ISO 8601 date}}
**Reviewer:** {{Agent ID or human name}}
**H-16 Compliance:** S-003 Steelman applied on {{date}} (confirmed/not applied -- indirect)
**Claims Extracted:** {{N}} | **Verified:** {{N}} | **Discrepancies:** {{N}}
```

### 2. Summary

2-3 sentence overall assessment covering: number of claims verified, verification rate, severity of discrepancies found, and recommendation (ACCEPT / REVISE with corrections / REJECT).

### 3. Findings Table

| ID | Claim | Source | Discrepancy | Severity | Affected Dimension |
|----|-------|--------|-------------|----------|--------------------|
| CV-001 | {{What deliverable claims}} | {{Source document}} | {{How it differs}} | Critical | {{Dimension}} |
| CV-002 | {{What deliverable claims}} | {{Source document}} | {{How it differs}} | Major | {{Dimension}} |

### 4. Finding Details

Expanded description for each Critical and Major finding:

```markdown
### CV-001: {{Finding Title}} [CRITICAL]

**Claim (from deliverable):** {{Exact text from the deliverable}}
**Source Document:** {{Document name and location}}
**Independent Verification:** {{What the source actually says, with exact quote}}
**Discrepancy:** {{Specific description of how the claim differs from the source}}
**Severity:** {{Critical/Major}} -- {{Consequence of this discrepancy}}
**Dimension:** {{Affected scoring dimension}}
**Correction:** {{Exact text change needed to align with source}}
```

### 5. Recommendations

Corrections grouped by severity: **Critical** (MUST correct before acceptance), **Major** (SHOULD correct), **Minor** (MAY correct). Each entry: CV-NNN identifier, exact correction needed, and source reference for the correct value.

### 6. Scoring Impact

Map CoVe findings to S-014 scoring dimensions (Completeness 0.20, Internal Consistency 0.20, Methodological Rigor 0.20, Evidence Quality 0.15, Actionability 0.15, Traceability 0.10). For each dimension, assess Impact (Positive/Negative/Neutral) with rationale referencing specific CV-NNN findings.

### Evidence Requirements

Each finding MUST include: exact text from the deliverable containing the incorrect claim, exact text from the source document showing the correct information, and a clear description of the discrepancy.

---

## Scoring Rubric

This rubric evaluates the **quality of the S-011 CoVe execution itself** (meta-evaluation), not the deliverable being reviewed.

### Threshold Bands

**SSOT threshold (from quality-enforcement.md, MUST NOT be redefined):** >= 0.92 weighted composite score. Below threshold = REJECTED; revision required per H-13.

**Operational bands for S-011 execution quality:**

| Band | Score Range | Outcome |
|------|------------|---------|
| PASS | >= 0.92 | Strategy execution accepted; verification is thorough and evidence-based |
| REVISE | 0.85 - 0.91 | Strategy execution requires targeted revision; close to threshold |
| REJECTED | < 0.85 | Strategy execution inadequate; significant rework required (H-13) |

> **Note:** The SSOT defines only the 0.92 threshold with REJECTED as the below-threshold outcome. The REVISE band (0.85-0.91) is a template-specific operational category (not sourced from quality-enforcement.md) to distinguish near-threshold executions requiring targeted improvements from those requiring significant rework. Both REVISE and REJECTED trigger the revision cycle per H-13.

### Dimension Weights

From quality-enforcement.md (MUST NOT be redefined):

| Dimension | Weight | Measures (for S-011 execution quality) |
|-----------|--------|----------------------------------------|
| Completeness | 0.20 | All testable claims extracted; verification questions cover all claim types; no claims skipped |
| Internal Consistency | 0.20 | Verification results do not contradict each other; severity consistent with discrepancy magnitude |
| Methodological Rigor | 0.20 | All 5 steps executed; independent verification truly independent; source documents actually consulted |
| Evidence Quality | 0.15 | Each finding includes exact quotes from both deliverable and source; discrepancies precisely described |
| Actionability | 0.15 | Corrections specific with exact replacement text; creator can fix without re-researching |
| Traceability | 0.10 | Every finding traces claim to source; dimensions mapped; verification chain documented |

### Strategy-Specific Rubric

| Dimension (Weight) | 0.95+ | 0.90-0.94 | 0.85-0.89 | <0.85 |
|--------------------|-------|-----------|-----------|-------|
| **Completeness (0.20)** | ALL testable claims extracted (5+ categories); verification questions for every claim; zero skipped claims | Most claims extracted; questions for all major claims; 1-2 minor claims skipped | Core claims extracted; some claim types missed; verification questions for most | <50% claims extracted; major gaps in coverage; no systematic extraction |
| **Internal Consistency (0.20)** | Zero contradictions in verification results; severity aligned with discrepancy magnitude; consistent methodology across all claims | No contradictions; severity mostly proportionate; minor methodology variations | One inconsistency; some severity ratings questionable | Multiple contradictions; arbitrary severity; inconsistent methodology |
| **Methodological Rigor (0.20)** | All 5 steps in order; independent verification demonstrably independent (source quotes provided); all source documents consulted; leniency bias counteracted | All steps executed; independence maintained; most sources consulted | 4 steps executed; independence unclear for some claims; some sources not consulted | <4 steps; verification not independent; sources not consulted |
| **Evidence Quality (0.15)** | Every finding includes exact deliverable text AND exact source quote; discrepancies precisely characterized with page/section references | Most findings have both quotes; discrepancies clearly described; minor reference gaps | Some findings have quotes; discrepancies described but not precisely | Findings lack quotes; discrepancies vaguely described |
| **Actionability (0.15)** | ALL corrections include exact replacement text; creator can apply corrections mechanically without interpretation | Most corrections specific; replacement text for Critical findings; minor gaps | Some corrections present; text vague; creator must re-research some | No corrections; findings identify problems without solutions |
| **Traceability (0.10)** | Every finding has full claim -> question -> source -> answer -> discrepancy chain; all mapped to dimensions | Most findings have verification chain; dimension mapping present | Some findings traceable; partial chains; partial dimension mapping | Findings not traceable; no verification chain documented |

---

## Examples

### Example 1: C3 Strategy Template -- SSOT Value Verification

**Context:**
- **Deliverable:** Draft adversarial strategy template (s-012-fmea.md) defining FMEA execution procedure
- **Criticality Level:** C3 (Significant) -- template in `.context/templates/`, AE-002 applies
- **Scenario:** S-003 Steelman applied first; S-002 and S-004 completed; now S-011 CoVe to verify factual accuracy

**Before (Key Claims from FMEA Template after S-003 Steelman):**

The template claims: (1) "S-012 composite score: 3.85" in the Identity table, (2) "Completeness weight: 0.25" in the Scoring Rubric, (3) "S-012 is REQUIRED at C2" in the Criticality Tier Table, (4) "quality threshold >= 0.90 for C2+ deliverables" in the Threshold Bands section, (5) "H-14 requires minimum 2 iterations" in the Prerequisites section.

**Strategy Execution (S-011 CoVe):**

**Step 1: Extract Claims** -- 5 factual claims extracted with specific quoted text and claimed sources.

**Step 2: Generate Verification Questions**
- VQ-001: "What is the composite score for S-012 in ADR-EPIC002-001?"
- VQ-002: "What is the weight for Completeness in quality-enforcement.md?"
- VQ-003: "At which criticality levels is S-012 required per quality-enforcement.md?"
- VQ-004: "What is the quality threshold in quality-enforcement.md?"
- VQ-005: "What is the minimum iteration count per H-14 in quality-enforcement.md?"

**Step 3: Independent Verification** (answers from source documents only)
- VQ-001: ADR-EPIC002-001 states S-012 composite score is **3.75** (not 3.85)
- VQ-002: quality-enforcement.md states Completeness weight is **0.20** (not 0.25)
- VQ-003: quality-enforcement.md states S-012 is required at **C3** (C2 + S-004, S-012, S-013), not C2
- VQ-004: quality-enforcement.md states threshold is **>= 0.92** (not >= 0.90)
- VQ-005: quality-enforcement.md states **3 iterations** minimum (not 2)

**Step 4: Consistency Check**

| ID | Claim | Source | Discrepancy | Severity | Affected Dimension |
|----|-------|--------|-------------|----------|--------------------|
| CV-001 | "Composite score: 3.85" | ADR-EPIC002-001 | Source says 3.75; template overstates by 0.10 | Major | Evidence Quality |
| CV-002 | "Completeness weight: 0.25" | quality-enforcement.md | Source says 0.20; template overstates by 0.05; weights would sum > 1.00 | Critical | Internal Consistency |
| CV-003 | "S-012 REQUIRED at C2" | quality-enforcement.md | Source says REQUIRED at C3; template promotes S-012 one tier too early | Major | Traceability |
| CV-004 | "Threshold >= 0.90" | quality-enforcement.md | Source says >= 0.92; template understates threshold by 0.02 | Critical | Methodological Rigor |
| CV-005 | "Minimum 2 iterations" | quality-enforcement.md | Source says 3 iterations; template understates minimum cycle count | Major | Completeness |

**After (FMEA Template Corrected Based on CV Findings):**

The creator corrected all 5 discrepancies: composite score to 3.75 (CV-001), Completeness weight to 0.20 (CV-002), criticality tier to C3 (CV-003), threshold to >= 0.92 (CV-004), and iteration count to 3 (CV-005). Verification rate improved from 0/5 (0%) to 5/5 (100%).

**Scoring Impact:**

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | CV-005: Understated iteration minimum leaves process incomplete |
| Internal Consistency | 0.20 | Negative | CV-002: Incorrect weight breaks summation invariant (weights must sum to 1.00) |
| Methodological Rigor | 0.20 | Negative | CV-004: Understated threshold weakens quality gate enforcement |
| Evidence Quality | 0.15 | Negative | CV-001: Incorrect composite score undermines source credibility |
| Actionability | 0.15 | Neutral | Corrections are straightforward value replacements |
| Traceability | 0.10 | Negative | CV-003: Incorrect criticality tier breaks SSOT traceability chain |

**Result:** 2 Critical and 3 Major discrepancies identified. All 5 SSOT values were incorrect in the original template. After corrections, the template achieved 100% verification alignment with source documents.

---

## Integration

### Canonical Pairings

See [Pairing Recommendations](#pairing-recommendations) for the full pairing table (S-003, S-014, S-007, S-001) with rationale and optimal sequence.

### H-16 Compliance

**H-16 Rule:** Steelman before critique. S-003 SHOULD execute before S-011 (indirect: CoVe is verification-oriented, not critique-oriented). Full ordering constraints and recommended sequences are documented in [Prerequisites: Ordering Constraints](#ordering-constraints) and [Purpose: Pairing Recommendations](#pairing-recommendations).

**Recommended:** S-003 -> S-011 -> S-014. **Acceptable:** S-011 without prior S-003 (H-16 indirect). **Non-Compliant:** Not applicable -- H-16 is indirect for CoVe.

### Criticality-Based Selection Table

From quality-enforcement.md (MUST NOT modify):

| Level | Required Strategies | Optional Strategies | S-011 Status |
|-------|---------------------|---------------------|--------------|
| C1 | S-010 | S-003, S-014 | NOT USED |
| C2 | S-007, S-002, S-014 | S-003, S-010 | NOT USED |
| C3 | C2 + S-004, S-012, S-013 | S-001, S-003, S-010, S-011 | **OPTIONAL** |
| C4 | All 10 selected | None | **REQUIRED** |

**Source:** quality-enforcement.md Criticality Levels table (SSOT). Values MUST match exactly.

### Cross-References

**SSOT:** `.context/rules/quality-enforcement.md` (H-13 threshold, H-16, dimension weights, criticality levels) | `ADR-EPIC002-001` (strategy selection, score 3.75) | `ADR-EPIC002-002` (enforcement architecture) | `.context/templates/adversarial/TEMPLATE-FORMAT.md` v1.1.0

**Strategy Templates:** `s-003-steelman.md` (SHOULD run before S-011, H-16 indirect) | `s-007-constitutional-ai.md` (complementary: constitutional check before factual verification) | `s-014-llm-as-judge.md` (scores post-correction revision) | `s-001-red-team.md` (complementary: attacks from verified factual baseline) | `s-013-inversion.md` (complementary: tests assumptions CoVe cannot verify) | `s-004-pre-mortem.md` (complementary: imagines failures CoVe cannot detect)

**Academic:** Dhuliawala et al. (2023), Weng et al. (2023), Min et al. (2023), Manakul et al. (2023). See file header.

**HARD Rules:** H-13 (threshold >= 0.92), H-14 (creator-critic cycle), H-15 (self-review), H-16 (steelman before critique -- indirect for CoVe), H-17 (scoring required) -- all from quality-enforcement.md

---

<!-- VALIDATION: 8 sections present | H-23/H-24 nav | CV-NNN prefix | H-16 documented (indirect) | SSOT weights match | REVISE band noted | C3 example with Critical finding | No absolute paths | 4-band rubric | Under 500 lines -->

---

*Template Version: 1.0.0*
*Format Conformance: TEMPLATE-FORMAT.md v1.1.0*
*SSOT: `.context/rules/quality-enforcement.md`*
*Created: 2026-02-15*
*Enabler: EN-809*
