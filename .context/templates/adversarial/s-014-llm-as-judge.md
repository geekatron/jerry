# S-014 LLM-as-Judge Execution Template

<!--
TEMPLATE: S-014 LLM-as-Judge Adversarial Strategy Execution Template
VERSION: 1.0.0 | DATE: 2026-02-15
SOURCE: quality-enforcement.md SSOT, ADR-EPIC002-001, TEMPLATE-FORMAT.md v1.1.0
ENABLER: EN-803 (S-014 Template)
STATUS: ACTIVE
CONFORMANCE: TEMPLATE-FORMAT.md v1.1.0

Academic Foundation:
- Zheng et al. 2023: "Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena"
- Kim et al. 2023: "Prometheus: Inducing Fine-Grained Evaluation Capability in Language Models"
- Anthropic Constitutional AI evaluation methodology

Validates deliverable quality using structured rubric-based scoring with six weighted dimensions.
Highest-ranked strategy (composite score 4.40) in the Jerry quality framework.
-->

> **Type:** adversarial-strategy-template
> **Status:** ACTIVE
> **Version:** 1.0.0
> **Date:** 2026-02-15
> **Source:** quality-enforcement.md, ADR-EPIC002-001, ADR-EPIC002-002
> **Format Conformance:** TEMPLATE-FORMAT.md v1.1.0
> **Enabler:** EN-803

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Section 1: Identity](#section-1-identity) | Strategy classification and metadata |
| [Section 2: Purpose](#section-2-purpose) | When to use, expected outcomes, pairings |
| [Section 3: Prerequisites](#section-3-prerequisites) | Required inputs and context |
| [Section 4: Execution Protocol](#section-4-execution-protocol) | Step-by-step scoring procedure |
| [Section 5: Output Format](#section-5-output-format) | Required structure for score reports |
| [Section 6: Scoring Rubric](#section-6-scoring-rubric) | Meta-evaluation of strategy execution |
| [Section 7: Examples](#section-7-examples) | Concrete scoring demonstration |
| [Section 8: Integration](#section-8-integration) | Cross-strategy pairing and criticality mapping |
| [Validation Checklist](#validation-checklist) | Template compliance verification |

---

## Section 1: Identity

| Field | Value |
|-------|-------|
| Strategy ID | S-014 |
| Strategy Name | LLM-as-Judge |
| Family | Iterative Self-Correction |
| Composite Score | 4.40 |
| Finding Prefix | LJ-NNN |
| Version | 1.0.0 |
| Date | 2026-02-15 |

### Criticality Tier Table

| Criticality Level | C1 (Routine) | C2 (Standard) | C3 (Significant) | C4 (Critical) |
|-------------------|--------------|---------------|------------------|---------------|
| **S-014 Status** | OPTIONAL | REQUIRED | REQUIRED | REQUIRED |

**Source:** quality-enforcement.md Criticality Levels table (SSOT).

**Interpretation:** S-014 is the primary scoring mechanism for all C2+ deliverables. It provides the weighted composite score used to determine PASS/REVISE/ESCALATE verdicts per H-13.

---

## Section 2: Purpose

### When to Use

S-014 MUST be applied in the following scenarios:

1. **C2+ deliverable final scoring** — All Standard, Significant, and Critical deliverables require S-014 scoring to validate quality gate compliance (H-13 threshold >= 0.92).

2. **Creator-critic-revision cycle scoring** — Each iteration in the H-14 minimum 3-iteration cycle uses S-014 to measure progress and determine when the deliverable meets the quality threshold.

3. **Post-revision validation** — After addressing findings from other adversarial strategies (S-002, S-004, S-007, etc.), S-014 re-scoring validates whether improvements achieved the target composite score.

4. **Standalone quality assessment** — When a deliverable is complete but has not undergone structured adversarial review, S-014 provides comprehensive quality evaluation across all six dimensions.

5. **Multi-strategy orchestration scoring** — When multiple strategies execute in sequence (e.g., S-003 -> S-002 -> S-004 -> S-012), S-014 provides the final composite score incorporating all findings.

### When NOT to Use

S-014 should NOT be applied in these scenarios:

1. **Early-stage brainstorming or ideation** — S-014 evaluates structured deliverables against completion criteria. Use S-003 (Steelman) or S-013 (Inversion) for exploratory work. Redirect to S-003 for idea strengthening before scoring.

2. **Code implementation (non-design)** — S-014 is optimized for documentation, analysis, design, and research deliverables. Use H-20/H-21 (test-first BDD, coverage requirements) for code quality. Redirect to testing-standards.md.

3. **C1 Routine work where quality scoring is optional** — For reversible single-session work (<3 files), S-010 (Self-Refine) alone may suffice. S-014 is optional at C1 criticality. Use judgment based on user needs.

4. **Partial or incomplete deliverables** — S-014 expects a complete draft to score. Scoring incomplete work produces artificially low Completeness scores that do not reflect actual quality. Wait until deliverable reaches "draft complete" status.

### Expected Outcome

A successful S-014 execution produces:

- **Weighted composite score** (0.00-1.00) with mathematical precision to two decimal places
- **Per-dimension scores** (six dimensions, each 0.00-1.00) with specific evidence justifying each score
- **Verdict** (PASS/REVISE/ESCALATE) based on H-13 threshold (>= 0.92)
- **Priority-ordered improvement recommendations** tied to the weakest-scoring dimensions
- **Leniency bias counteraction documentation** demonstrating strict rubric application

### Pairing Recommendations

S-014 pairs with all other strategies as the final scoring mechanism:

| Pairing | Order | Rationale |
|---------|-------|-----------|
| **S-003 + S-014** | S-003 → S-014 | Steelman strengthens the deliverable before scoring (H-16 compliance for baseline quality) |
| **S-002 + S-014** | S-003 → S-002 → S-014 | H-16 requires S-003 before S-002; S-014 scores the revised deliverable |
| **S-004 + S-014** | S-003 → S-004 → S-014 | H-16 requires S-003 before S-004; S-014 validates risk mitigations |
| **S-007 + S-014** | S-007 → S-014 | Constitutional critique finds violations; S-014 scores corrected version |
| **S-010 + S-014** | S-010 → S-014 | Self-Refine iterates; S-014 confirms exit criteria (H-15 self-review before presentation) |
| **Multi-strategy orchestration** | S-003 → [S-002, S-004, S-007, S-012, S-013] → S-014 | All strategies execute; S-014 provides final composite score |

**H-16 Note:** S-014 is NOT a critique strategy, so H-16 (Steelman before critique) does not directly constrain S-014 placement. However, S-003 is RECOMMENDED before S-014 to establish a quality baseline that S-014 can score fairly.

---

## Section 3: Prerequisites

### Required Inputs

Before executing S-014, the following MUST be available:

- [ ] **Deliverable file path** — Valid absolute path to the deliverable being scored (markdown, code, design doc, research artifact, etc.)
- [ ] **Deliverable type identified** — Classification (ADR, Research, Analysis, Synthesis, Design, Code, Template, Other) to contextualize scoring
- [ ] **Criticality level assigned** — C1/C2/C3/C4 classification determines whether S-014 is required or optional
- [ ] **Deliverable completion status** — Deliverable MUST be in "draft complete" or later status (not partial or in-progress)

### Context Requirements

The scorer MUST have access to:

- **Quality-enforcement.md SSOT** — Source for the six dimension definitions, weights, and H-13 threshold (>= 0.92)
- **Deliverable requirements or specification** — To evaluate Completeness and Traceability dimensions accurately
- **Prior strategy execution reports (if available)** — Findings from S-002, S-004, S-007, etc. inform Evidence Quality and Methodological Rigor scores
- **Prior S-014 scores (if re-scoring after revision)** — To measure improvement and validate whether revisions addressed the weakest dimensions

### Ordering Constraints

S-014 execution has these dependencies:

1. **Deliverable MUST be complete** — Cannot score partial work; Completeness dimension requires all sections present.

2. **S-003 Steelman RECOMMENDED before S-014** — While not a hard H-16 constraint (S-014 is not a critique strategy), running S-003 first establishes a quality baseline that S-014 can score fairly. Without S-003, S-014 may score a weaker first draft.

3. **Other strategies SHOULD execute before S-014 in multi-strategy orchestration** — S-014 is typically the LAST strategy in a sequence (S-003 → S-002 → S-004 → S-014) to score the deliverable after all improvements.

4. **H-15 Self-Review BEFORE presenting S-014 score report** — The S-014 execution itself is a deliverable. Apply S-010 self-review to the score report before persisting (validate evidence, check leniency bias, verify math).

---

## Section 4: Execution Protocol

S-014 follows a seven-step procedure to produce a rubric-based quality score with leniency bias counteraction.

### Step 1: Read Deliverable and Context

**Action:** Load the deliverable content and gather all available context.

**Procedure:**
1. Read the deliverable file using the provided file path
2. Identify the deliverable type (ADR, Research, Analysis, etc.) and criticality level
3. Read the deliverable requirements or specification (if available) to understand expected scope
4. Read prior strategy execution reports (if available) to incorporate findings into scoring
5. Read prior S-014 score (if this is a re-scoring after revision) to measure improvement

**Output:** Complete understanding of deliverable content, requirements, and prior feedback.

---

### Step 2: Score Each Dimension Independently

**Action:** Evaluate the deliverable against EACH of the six SSOT dimensions independently, documenting specific evidence for each score.

**Procedure:**

For EACH dimension (Completeness, Internal Consistency, Methodological Rigor, Evidence Quality, Actionability, Traceability):

1. **Read the rubric criteria** for this dimension from quality-enforcement.md or the Scoring Rubric section below
2. **Evaluate the deliverable** against the criteria using specific evidence (quotes, section references, gaps)
3. **Apply leniency bias counteraction:**
   - Compare against rubric LITERALLY, not impressionistically
   - When uncertain between adjacent scores (e.g., 0.85 vs 0.90), choose the LOWER score
   - Document specific evidence; if you cannot point to evidence, the score is too high
4. **Assign a score** (0.00-1.00, two decimal places) with justification
5. **Document the score** in the findings table using LJ-NNN identifiers

**Decision Point:**
- If dimension score >= 0.90: Document exceptional evidence justifying the high score. Verify this is not leniency bias.
- If dimension score <= 0.50: Flag as Critical finding; this dimension has fundamental issues requiring substantial revision.

**Output:** Six independent dimension scores with evidence, documented in the findings table.

**Finding Documentation Format:**

| ID | Finding | Severity | Evidence | Affected Dimension |
|----|---------|----------|----------|--------------------|
| LJ-001 | Completeness score: {score}/1.00 | {Critical/Major/Minor} | {Specific evidence from deliverable} | Completeness |
| LJ-002 | Internal Consistency score: {score}/1.00 | {Critical/Major/Minor} | {Specific evidence} | Internal Consistency |
| ... | ... | ... | ... | ... |

**Severity Definitions:**
- **Critical:** Dimension score <= 0.50; fundamental issue blocking acceptance
- **Major:** Dimension score 0.51-0.84; significant gap requiring revision
- **Minor:** Dimension score 0.85-0.91; near-threshold, targeted improvement opportunity

---

### Step 3: Compute Weighted Composite Score

**Action:** Calculate the weighted composite score using the SSOT dimension weights.

**Procedure:**

1. **Retrieve dimension weights** from quality-enforcement.md (or use constants below):
   - Completeness: 0.20
   - Internal Consistency: 0.20
   - Methodological Rigor: 0.20
   - Evidence Quality: 0.15
   - Actionability: 0.15
   - Traceability: 0.10

2. **Compute weighted composite:**
   ```
   composite = (completeness_score * 0.20)
             + (internal_consistency_score * 0.20)
             + (methodological_rigor_score * 0.20)
             + (evidence_quality_score * 0.15)
             + (actionability_score * 0.15)
             + (traceability_score * 0.10)
   ```

3. **Round to two decimal places** (e.g., 0.8733 → 0.87)

4. **Verify mathematical accuracy:** Sum of weighted scores MUST equal the composite. Re-check if discrepancy detected.

**Output:** Weighted composite score (0.00-1.00, two decimal places).

---

### Step 4: Determine Verdict

**Action:** Apply the H-13 quality gate threshold and special conditions to determine the final verdict.

**Procedure:**

1. **Apply H-13 threshold:**
   - If composite >= 0.92: Verdict = **PASS** (quality gate met)
   - If composite 0.85-0.91: Verdict = **REVISE** (close to threshold, targeted improvements; REJECTED per H-13)
   - If composite 0.70-0.84: Verdict = **REVISE** (significant gaps, focused revision; REJECTED per H-13)
   - If composite 0.50-0.69: Verdict = **REVISE** (major gaps, substantial revision; REJECTED per H-13)
   - If composite < 0.50: Verdict = **ESCALATE** (fundamental issues, may need rethink; REJECTED per H-13)

2. **Check special conditions:**
   - If any dimension has a **Critical** finding (score <= 0.50): Override to **REVISE** regardless of composite score
   - If prior strategy reports contain unresolved **Critical** findings: Override to **REVISE** even if composite >= 0.92
   - If composite < 0.50 after 3+ revision cycles: Override to **ESCALATE** to user (H-14 cycle exhaustion)

3. **Document verdict rationale** in the score report (see Output Format section)

**Decision Point:**
- If verdict = PASS: Deliverable meets quality gate; proceed to persistence
- If verdict = REVISE: Deliverable requires revision; generate improvement recommendations (Step 5)
- If verdict = ESCALATE: Fundamental issues present; flag for user/orchestrator escalation

**Output:** Verdict (PASS/REVISE/ESCALATE) with rationale.

---

### Step 5: Generate Improvement Recommendations

**Action:** Create priority-ordered, actionable recommendations tied to the weakest-scoring dimensions.

**Procedure:**

1. **Rank dimensions by score** (lowest to highest)
2. **For each dimension scoring < 0.92:**
   - Identify the specific gap or weakness causing the low score
   - Formulate a concrete, actionable recommendation to address the gap
   - Estimate the target score achievable if the recommendation is implemented
3. **Prioritize recommendations:**
   - Priority 1: Weakest dimension (highest impact on composite score)
   - Priority 2: Second-weakest dimension with weight >= 0.15
   - Priority 3+: Remaining dimensions scoring < 0.92
4. **Document recommendations** in the Output Format table (see Section 5)

**Output:** Priority-ordered improvement recommendations table.

---

### Step 6: Apply Leniency Bias Check (H-15 Self-Review)

**Action:** Validate scoring rigor before persisting the score report.

**Procedure:**

Per H-15 (Self-review before presenting), execute this checklist:

- [ ] **Each dimension scored independently** — No dimension score was influenced by other dimensions
- [ ] **Evidence documented for each score** — Specific quotes, section references, or gap descriptions present for all six dimensions
- [ ] **Uncertain scores resolved downward** — When unsure between adjacent scores, the lower score was chosen
- [ ] **First-draft calibration considered** — If scoring a first draft, note that first drafts typically score 0.65-0.80 (descriptive observation, not a target range; exceptional first drafts may score higher, poor first drafts may score lower)
- [ ] **No dimension scored above 0.95 without exceptional evidence** — High scores (0.95+) have documented exceptional justification
- [ ] **High-scoring dimension verification** — For any dimension scoring > 0.90: list the 3 strongest evidence points that justify elevating it above "strong work" (0.90); if you cannot list 3 specific evidence points, revise the score downward
- [ ] **Low-scoring dimension verification** — List the 3 lowest-scoring dimensions and verify that specific evidence justifies each score; if evidence is vague or missing, document the gap explicitly
- [ ] **Weighted composite matches calculation** — Mathematical verification of composite = sum of (dimension * weight)
- [ ] **Verdict matches score range** — PASS/REVISE/ESCALATE verdict aligns with H-13 threshold and special conditions
- [ ] **Improvement recommendations are specific and actionable** — Not vague (e.g., "improve completeness") but concrete (e.g., "add Section 4 with risk mitigation strategies")

**Decision Point:**
- If all checklist items PASS: Proceed to Step 7 (persist score report)
- If any checklist item FAILS: Revise the score report to address the failure; re-execute this step

**Output:** Validated score report ready for persistence.

---

### Step 7: Persist Score Report

**Action:** Write the score report to the filesystem per P-002 (File Persistence).

**Procedure:**

1. **Determine output path:**
   - If orchestrator-provided: Use specified path
   - If standalone: Generate path based on deliverable name: `{deliverable-dir}/scoring/{deliverable-name}-score-{timestamp}.md`

2. **Write score report** using the Output Format (Section 5)

3. **Verify file written successfully** (check file exists and is readable)

4. **Return output path and verdict** to caller (orchestrator or user)

**Output:** Persisted score report file; output path and verdict returned to caller.

---

## Section 5: Output Format

Every S-014 execution MUST produce a score report with the following structure.

### Required Output Sections

#### 1. Header

```markdown
# Quality Score Report: {Deliverable Title}

## Scoring Context
- **Deliverable:** {absolute file path}
- **Deliverable Type:** {ADR|Research|Analysis|Synthesis|Design|Code|Template|Other}
- **Criticality Level:** {C1|C2|C3|C4}
- **Scoring Strategy:** S-014 (LLM-as-Judge)
- **SSOT Reference:** .context/rules/quality-enforcement.md
- **Scored By:** {Agent or User Name}
- **Scored:** {ISO-8601 timestamp}
- **Iteration:** {Revision cycle number, e.g., 1 = first score, 2 = after first revision}
```

---

#### 2. Summary

```markdown
## L0 Executive Summary

**Score:** {composite}/1.00 | **Verdict:** PASS/REVISE/ESCALATE | **Weakest Dimension:** {name} ({score})

**One-line assessment:** {Plain-language summary of quality status and top priority action}

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | {0.00-1.00} |
| **Threshold (H-13)** | 0.92 |
| **Verdict** | PASS / REVISE / ESCALATE |
| **Strategy Findings Incorporated** | {Yes (count) / No} |
| **Prior Score (if re-scoring)** | {previous composite, or N/A} |
| **Improvement Delta** | {current - prior, or N/A} |
```

---

#### 3. Findings Table

```markdown
## Dimension Scores

| Dimension | Weight | Score | Weighted | Severity | Evidence Summary |
|-----------|--------|-------|----------|----------|------------------|
| Completeness | 0.20 | {0.00-1.00} | {score * 0.20} | {Critical/Major/Minor} | {One-line evidence} |
| Internal Consistency | 0.20 | {0.00-1.00} | {score * 0.20} | {Critical/Major/Minor} | {One-line evidence} |
| Methodological Rigor | 0.20 | {0.00-1.00} | {score * 0.20} | {Critical/Major/Minor} | {One-line evidence} |
| Evidence Quality | 0.15 | {0.00-1.00} | {score * 0.15} | {Critical/Major/Minor} | {One-line evidence} |
| Actionability | 0.15 | {0.00-1.00} | {score * 0.15} | {Critical/Major/Minor} | {One-line evidence} |
| Traceability | 0.10 | {0.00-1.00} | {score * 0.10} | {Critical/Major/Minor} | {One-line evidence} |
| **TOTAL** | **1.00** | | **{composite}** | | |
```

**Severity Key:**
- **Critical:** Score <= 0.50 (fundamental issue blocking acceptance)
- **Major:** Score 0.51-0.84 (significant gap requiring revision)
- **Minor:** Score 0.85-0.91 (near-threshold, targeted improvement)

---

#### 4. Finding Details

```markdown
## Detailed Dimension Analysis

### Completeness ({score}/1.00) — {Severity}

**Evidence:**
{Specific evidence from the deliverable justifying this score: quotes, section references, analysis of coverage}

**Gaps:**
{Specific requirements not fully addressed, missing sections, incomplete analysis}

**Improvement Path:**
{Concrete actions that would raise this score to 0.92+}

---

### Internal Consistency ({score}/1.00) — {Severity}

**Evidence:**
{Specific evidence: consistent claims found, or contradictions/inconsistencies identified}

**Gaps:**
{Specific inconsistencies between sections, claims, data, or conclusions}

**Improvement Path:**
{Concrete actions to resolve inconsistencies and achieve 0.92+}

---

[... Repeat for all six dimensions: Methodological Rigor, Evidence Quality, Actionability, Traceability ...]
```

---

#### 5. Recommendations

```markdown
## Improvement Recommendations (Priority Ordered)

| Priority | Dimension | Current | Target | Recommendation |
|----------|-----------|---------|--------|----------------|
| 1 | {weakest dimension} | {score} | 0.92 | {Specific, actionable recommendation} |
| 2 | {second-weakest} | {score} | 0.92 | {Specific, actionable recommendation} |
| 3 | {third-weakest} | {score} | 0.92 | {Specific, actionable recommendation} |
| ... | ... | ... | ... | ... |

**Implementation Guidance:**
{Brief paragraph on how to approach these recommendations, sequencing, or dependencies}
```

---

#### 6. Scoring Impact

```markdown
## Scoring Impact Analysis

### Dimension Impact on Composite

This table shows how each dimension contributes to the weighted composite and how much improvement is needed to reach the H-13 threshold (0.92).

| Dimension | Weight | Score | Weighted Contribution | Gap to 0.92 Target | Weighted Gap |
|-----------|--------|-------|----------------------|-------------------|--------------|
| Completeness | 0.20 | {score} | {score * 0.20} | {0.92 - score} | {(0.92 - score) * 0.20} |
| Internal Consistency | 0.20 | {score} | {score * 0.20} | {0.92 - score} | {(0.92 - score) * 0.20} |
| Methodological Rigor | 0.20 | {score} | {score * 0.20} | {0.92 - score} | {(0.92 - score) * 0.20} |
| Evidence Quality | 0.15 | {score} | {score * 0.15} | {0.92 - score} | {(0.92 - score) * 0.15} |
| Actionability | 0.15 | {score} | {score * 0.15} | {0.92 - score} | {(0.92 - score) * 0.15} |
| Traceability | 0.10 | {score} | {score * 0.10} | {0.92 - score} | {(0.92 - score) * 0.10} |
| **TOTAL** | **1.00** | | **{composite}** | | **{sum of weighted gaps}** |

**Interpretation:**
- **Current composite:** {composite}/1.00
- **Target composite:** 0.92/1.00 (H-13 threshold)
- **Total weighted gap:** {0.92 - composite}
- **Largest improvement opportunity:** {dimension with highest weighted gap} ({weighted gap} available)

### Verdict Rationale

**Verdict:** {PASS/REVISE/ESCALATE}

**Rationale:**
{Explanation of why this verdict was assigned based on H-13 threshold, special conditions, and dimension analysis}
```

---

#### 7. Leniency Bias Check

```markdown
## Leniency Bias Check (H-15 Self-Review)

- [ ] Each dimension scored independently (no cross-dimension influence)
- [ ] Evidence documented for each score (specific quotes/references)
- [ ] Uncertain scores resolved downward (conservative scoring applied)
- [ ] First-draft calibration considered (if applicable: note that first drafts typically score 0.65-0.80 as descriptive observation; not a target range)
- [ ] No dimension scored above 0.95 without exceptional evidence
- [ ] High-scoring dimensions verified (for any dimension > 0.90: list 3 specific evidence points justifying the high score)
- [ ] Low-scoring dimensions verified (list 3 lowest-scoring dimensions with specific evidence for each)
- [ ] Weighted composite matches mathematical calculation
- [ ] Verdict matches score range table (H-13 compliance verified)
- [ ] Improvement recommendations are specific and actionable

**Leniency Bias Counteraction Notes:**
{Document any cases where scores were adjusted downward, or where exceptional evidence justified high scores}
```

---

### Evidence Requirements

Each dimension score in the Findings Table and Finding Details sections MUST include:

1. **Specific reference to location** in the deliverable (section name, line numbers, heading titles, or paragraph identifiers)
2. **Quotation or paraphrase** of the relevant content being evaluated (not just "Section 3 is incomplete" but "Section 3 lacks risk mitigation strategies; only risks are identified")
3. **Explanation of why** this constitutes the assigned score (how the evidence maps to the rubric criteria for that dimension)

---

## Section 6: Scoring Rubric

This section defines how to evaluate the quality of an S-014 execution itself (meta-evaluation).

### Threshold Bands

**SSOT threshold (from quality-enforcement.md, MUST NOT be redefined):** >= 0.92 weighted composite score. Below threshold = REJECTED; revision required per H-13.

**Operational bands for S-014 execution quality (template-specific subdivision for workflow guidance):**

| Band | Score Range | Outcome |
|------|------------|---------|
| PASS | >= 0.92 | S-014 execution accepted; score report is high quality |
| REVISE | 0.85 - 0.91 | S-014 execution requires targeted revision; close to threshold (REJECTED per H-13) |
| REJECTED | < 0.85 | S-014 execution inadequate; significant rework required (REJECTED per H-13) |

> **Note:** The SSOT defines only the 0.92 threshold with REJECTED as the below-threshold outcome. The REVISE band (0.85-0.91) is a template-specific operational category (not sourced from quality-enforcement.md) to distinguish near-threshold deliverables requiring targeted improvements from those requiring significant rework. Both REVISE and REJECTED are H-13 violations that trigger the revision cycle. REVISE is an operational workflow label, not a distinct acceptance state.

---

### Dimension Weights (from quality-enforcement.md, MUST NOT be redefined)

| Dimension | Weight | Measures (for S-014 execution quality) |
|-----------|--------|---------------------------------------|
| Completeness | 0.20 | All six dimensions scored; all required output sections present; no missing evidence |
| Internal Consistency | 0.20 | No contradictory dimension scores; verdict aligns with composite; math is correct |
| Methodological Rigor | 0.20 | Leniency bias counteraction applied; rubric followed literally; evidence-based scoring |
| Evidence Quality | 0.15 | Each dimension score backed by specific deliverable references and quotes |
| Actionability | 0.15 | Improvement recommendations are concrete, prioritized, and implementable |
| Traceability | 0.10 | Dimension scores linked to deliverable content; findings traced to rubric criteria |

---

### Strategy-Specific Rubric (4-Band Criteria)

For each dimension, evaluate S-014 execution quality using these criteria:

#### Completeness

| Score Range | Criteria |
|-------------|----------|
| **0.95 - 1.00** | All six dimensions scored with detailed evidence; all seven output sections present and complete; prior strategy findings incorporated (if available); leniency bias check fully documented; no gaps in scoring coverage |
| **0.90 - 0.94** | All six dimensions scored with evidence; all output sections present; minor gaps in evidence detail or leniency bias documentation; prior findings mostly incorporated |
| **0.85 - 0.89** | All six dimensions scored; some output sections incomplete (e.g., improvement recommendations lack specificity); evidence present but not always detailed; leniency bias check partially documented |
| **<= 0.84** | Missing dimension scores; output sections absent or severely incomplete; no evidence provided for some scores; leniency bias check missing |

---

#### Internal Consistency

| Score Range | Criteria |
|-------------|----------|
| **0.95 - 1.00** | All dimension scores align with evidence; weighted composite mathematically correct; verdict matches H-13 threshold exactly; no contradictions between findings and recommendations; severity levels consistent with scores (Critical <= 0.50, Major 0.51-0.84, Minor 0.85-0.91) |
| **0.90 - 0.94** | Dimension scores mostly align with evidence; composite calculation correct; verdict appropriate; minor inconsistencies (e.g., recommendation priority doesn't fully match dimension weakness) |
| **0.85 - 0.89** | Some dimension scores do not fully align with evidence; composite calculation correct but some dimension scores questionable; verdict broadly appropriate but rationale unclear |
| **<= 0.84** | Contradictory dimension scores and evidence; composite calculation errors; verdict does not match score range; severity levels inconsistent with scores |

---

#### Methodological Rigor

| Score Range | Criteria |
|-------------|----------|
| **0.95 - 1.00** | Leniency bias counteraction explicitly applied with verification (downward adjustments documented; high-scoring dimensions >0.90 have 3+ specific evidence points listed; low-scoring dimensions verified); rubric criteria followed literally; each dimension scored independently with no cross-influence; first-draft calibration considered as descriptive (not prescriptive); H-15 self-review checklist complete |
| **0.90 - 0.94** | Leniency bias counteraction applied; rubric mostly followed; dimensions scored independently; H-15 checklist mostly complete; minor procedural deviations |
| **0.85 - 0.89** | Some leniency bias counteraction; rubric followed but with impressionistic scoring in places; H-15 checklist partially complete; some dimension scores show cross-influence |
| **<= 0.84** | No leniency bias counteraction; rubric not followed; impressionistic scoring dominates; H-15 checklist missing or mostly incomplete; dimension scores show clear cross-influence |

---

#### Evidence Quality

| Score Range | Criteria |
|-------------|----------|
| **0.95 - 1.00** | Every dimension score backed by specific deliverable quotes or section references; gaps clearly identified with examples; evidence is credible and directly relevant to rubric criteria; no vague assertions |
| **0.90 - 0.94** | Most dimension scores have specific evidence; some gaps in evidence detail; evidence is relevant and credible; minimal vague assertions |
| **0.85 - 0.89** | Some dimension scores have specific evidence; many gaps in evidence detail; some vague assertions; evidence relevance unclear in places |
| **<= 0.84** | Few dimension scores have specific evidence; evidence is vague, missing, or not credible; assertions dominate over evidence |

---

#### Actionability

| Score Range | Criteria |
|-------------|----------|
| **0.95 - 1.00** | All improvement recommendations are concrete, specific, and implementable; recommendations prioritized by weighted gap impact; implementation guidance provided; recommendations directly address identified gaps |
| **0.90 - 0.94** | Most recommendations are concrete and implementable; prioritization mostly aligns with impact; some recommendations lack specificity; guidance present |
| **0.85 - 0.89** | Some recommendations are concrete; prioritization unclear; many recommendations vague (e.g., "improve completeness"); guidance minimal |
| **<= 0.84** | Recommendations are vague or generic; no prioritization; not implementable without significant interpretation; no guidance |

---

#### Traceability

| Score Range | Criteria |
|-------------|----------|
| **0.95 - 1.00** | Every dimension score traces to specific deliverable content (section/line references); findings linked to rubric criteria; composite calculation shown step-by-step; verdict rationale traces to H-13 threshold; SSOT references present |
| **0.90 - 0.94** | Most dimension scores traceable; rubric linkage mostly present; composite calculation shown; verdict rationale clear; SSOT referenced |
| **0.85 - 0.89** | Some dimension scores traceable; rubric linkage partial; composite calculation present but not detailed; verdict rationale unclear; SSOT reference missing |
| **<= 0.84** | Few dimension scores traceable; no rubric linkage; composite calculation missing or incorrect; verdict rationale absent; no SSOT reference |

---

## Section 7: Examples

### Example 1: C2 Standard Deliverable — ADR Scoring

**Context:**
- **Deliverable:** ADR-PROJ001-003 (Decision to adopt hexagonal architecture)
- **Deliverable Type:** ADR (Architecture Decision Record)
- **Criticality Level:** C2 (Standard) — Architecture decision affecting 3-10 files, reversible in 1 day
- **Iteration:** 1 (first score, initial draft)

---

**Before (Relevant Portion of ADR):**

```markdown
# ADR-PROJ001-003: Adopt Hexagonal Architecture

## Status
Proposed

## Context
We need to organize our codebase better. Hexagonal architecture seems like a good fit.

## Decision
We will use hexagonal architecture with ports and adapters.

## Consequences
- Code will be more modular
- Testing will be easier
- We'll have better separation of concerns
```

---

**Strategy Execution (S-014 Scoring):**

#### Step 1: Read Deliverable and Context
- Deliverable type: ADR
- Criticality: C2 (S-014 REQUIRED per quality-enforcement.md)
- No prior strategy reports available (first scoring pass)
- No prior S-014 score (initial draft)

#### Step 2: Score Each Dimension Independently

**Dimension 1: Completeness (0.65/1.00)**
- Evidence: ADR has Status, Context, Decision, Consequences sections (standard ADR structure present)
- Gaps: Context section is very brief (1 sentence), lacks problem statement detail; no Alternatives Considered section; no Implementation Plan; Consequences are high-level without specifics
- Leniency check: Initially considered 0.70, but "better separation of concerns" is vague and not explained → downgrade to 0.65
- Severity: Major

**Dimension 2: Internal Consistency (0.85/1.00)**
- Evidence: No contradictions detected; Decision aligns with Context (need for better organization → adopt hexagonal architecture)
- Gaps: Consequences claim "testing will be easier" but no explanation of how this relates to the architecture decision
- Leniency check: Considered 0.90, but unsure if the testing claim is justified → downgrade to 0.85
- Severity: Minor

**Dimension 3: Methodological Rigor (0.55/1.00)**
- Evidence: Standard ADR structure followed (status, context, decision, consequences)
- Gaps: No alternatives analysis; no evaluation criteria for architecture selection; no trade-offs discussed; "seems like a good fit" is not rigorous justification
- Leniency check: Initially considered 0.60, but lack of alternatives is a significant methodological gap → downgrade to 0.55
- Severity: Major

**Dimension 4: Evidence Quality (0.50/1.00)**
- Evidence: None — no citations, no references, no data supporting the decision
- Gaps: Claims like "seems like a good fit" are unsupported; no evidence that hexagonal architecture solves the stated problem; no examples or case studies
- Leniency check: This is a fundamental gap; cannot score higher than 0.50 without any supporting evidence
- Severity: Critical

**Dimension 5: Actionability (0.70/1.00)**
- Evidence: Decision is clear ("use hexagonal architecture with ports and adapters")
- Gaps: No implementation plan; no migration strategy; no timeline; no resource requirements; consequences are not actionable (what does "more modular" mean in practice?)
- Leniency check: Considered 0.75, but lack of any implementation guidance is significant → downgrade to 0.70
- Severity: Major

**Dimension 6: Traceability (0.40/1.00)**
- Evidence: None — no links to requirements, no references to problem statements, no traceability to prior ADRs
- Gaps: Context is so brief that the decision cannot be traced to specific needs; no relationship to other architecture decisions documented
- Leniency check: This is a severe gap; ADRs MUST be traceable to requirements → 0.40
- Severity: Critical

---

#### Step 3: Compute Weighted Composite Score

```
composite = (0.65 * 0.20) + (0.85 * 0.20) + (0.55 * 0.20) + (0.50 * 0.15) + (0.70 * 0.15) + (0.40 * 0.10)
          = 0.13 + 0.17 + 0.11 + 0.075 + 0.105 + 0.04
          = 0.63
```

**Weighted Composite: 0.63/1.00**

---

#### Step 4: Determine Verdict

- Composite score: 0.63
- H-13 threshold: 0.92
- Score range: 0.50-0.69 → **REVISE** (major gaps, substantial revision needed)
- Special conditions: Two Critical findings (Evidence Quality 0.50, Traceability 0.40) → confirms **REVISE**
- **Verdict: REVISE**

---

#### Step 5: Generate Improvement Recommendations

| Priority | Dimension | Current | Target | Recommendation |
|----------|-----------|---------|--------|----------------|
| 1 | Traceability | 0.40 | 0.92 | Add "Stakeholders" section identifying who requested this; link to FEAT-XXX or requirements doc; add "Related ADRs" section |
| 2 | Evidence Quality | 0.50 | 0.92 | Add "Research" section with 2-3 citations (e.g., Alistair Cockburn's hexagonal architecture paper); include case study or example |
| 3 | Methodological Rigor | 0.55 | 0.92 | Add "Alternatives Considered" section evaluating at least 2 other architectures (layered, clean); add trade-offs analysis |
| 4 | Actionability | 0.70 | 0.92 | Add "Implementation Plan" with phases, migration strategy, and timeline; expand Consequences with specific examples |
| 5 | Completeness | 0.65 | 0.92 | Expand Context to 3-5 paragraphs detailing the problem; add "Success Criteria" for evaluating the decision post-implementation |

---

**Findings (Using LJ-NNN Prefix):**

| ID | Finding | Severity | Evidence | Affected Dimension |
|----|---------|----------|----------|--------------------|
| LJ-001 | Completeness score: 0.65/1.00 | Major | Context section is 1 sentence; no Alternatives, Implementation Plan, or detailed Consequences | Completeness |
| LJ-002 | Internal Consistency score: 0.85/1.00 | Minor | "Testing will be easier" claim not explained or justified | Internal Consistency |
| LJ-003 | Methodological Rigor score: 0.55/1.00 | Major | No alternatives analysis; "seems like a good fit" is not rigorous; no evaluation criteria | Methodological Rigor |
| LJ-004 | Evidence Quality score: 0.50/1.00 | Critical | No citations, references, or data supporting the decision; all claims unsupported | Evidence Quality |
| LJ-005 | Actionability score: 0.70/1.00 | Major | No implementation plan, migration strategy, or timeline; consequences are vague | Actionability |
| LJ-006 | Traceability score: 0.40/1.00 | Critical | No links to requirements or stakeholders; decision cannot be traced to specific needs | Traceability |

---

**After (ADR Revised Based on Findings):**

```markdown
# ADR-PROJ001-003: Adopt Hexagonal Architecture

## Status
Proposed

## Context
Our current codebase suffers from tight coupling between business logic and infrastructure concerns. Specifically:
- Domain logic is intertwined with database access code, making unit testing difficult
- External API integrations are scattered across service classes, creating maintenance burden
- Adding new delivery mechanisms (e.g., CLI in addition to web API) requires duplicating business logic

This violates the Dependency Inversion Principle and makes our system fragile to infrastructure changes.

**Stakeholders:** Engineering team, Product Owner (requested CLI support in FEAT-042)

**Related ADRs:** None (this is our first architecture decision for the project)

## Alternatives Considered

### 1. Layered Architecture (Traditional N-Tier)
- **Pros:** Familiar, widely adopted, good separation of UI/business/data layers
- **Cons:** Dependencies flow downward (business layer depends on data layer), making testing hard; infrastructure changes ripple up
- **Trade-off:** Simplicity vs. testability and flexibility

### 2. Clean Architecture (Concentric Circles)
- **Pros:** Similar to hexagonal, strong dependency inversion, excellent testability
- **Cons:** More prescriptive layer structure; learning curve for team unfamiliar with the pattern
- **Trade-off:** Rigor vs. flexibility

### 3. Hexagonal Architecture (Ports and Adapters) — **SELECTED**
- **Pros:** Explicit ports isolate domain from infrastructure; adapters are swappable; domain logic is fully testable without mocks; supports multiple delivery mechanisms
- **Cons:** More files and abstractions (boilerplate); requires discipline to maintain boundaries
- **Trade-off:** Flexibility and testability vs. initial complexity

**Selection Rationale:** Hexagonal architecture best addresses our specific need for multiple delivery mechanisms (web API + CLI) while maximizing testability. The flexibility to swap adapters (e.g., migrate from filesystem to database persistence) outweighs the initial boilerplate cost.

## Decision
We will adopt Hexagonal Architecture with explicit ports (interfaces) and adapters (implementations):
- **Domain layer:** Business logic, entities, domain events, domain service interfaces (ports)
- **Application layer:** Use cases, commands, queries, handlers
- **Infrastructure layer:** Persistence adapters, messaging adapters, external API clients
- **Interface layer:** Web API controllers, CLI commands

Dependencies flow inward: Interface → Application → Domain. Infrastructure implements domain ports.

## Evidence
- Alistair Cockburn, "Hexagonal Architecture" (2005): Introduces the pattern and rationale [1]
- Netflix Tech Blog, "Hexagonal Architecture at Scale" (2018): Case study demonstrating maintainability benefits [2]
- Our FEAT-042 requirements explicitly request CLI support alongside the existing web API, validating the need for multiple delivery mechanisms

[1] https://alistair.cockburn.us/hexagonal-architecture/
[2] https://netflixtechblog.com/ready-for-changes-with-hexagonal-architecture-b315ec967749

## Consequences

### Positive
- **Testability:** Domain logic can be tested without database or HTTP mocks (unit tests run in milliseconds)
- **Flexibility:** Adding CLI delivery mechanism (FEAT-042) requires only a new interface adapter; no domain changes
- **Maintainability:** Infrastructure changes (e.g., swap PostgreSQL for DynamoDB) affect only the persistence adapter; domain remains untouched

### Negative
- **Boilerplate:** Each domain concept requires a port interface and adapter implementation (estimate 20% more files)
- **Learning curve:** Team members unfamiliar with hexagonal architecture need onboarding (estimate 1-2 days)

### Neutral
- **Architectural enforcement:** We will need architecture tests to validate layer boundaries (see Implementation Plan)

## Implementation Plan

### Phase 1: Foundation (Week 1)
- Create directory structure: `src/domain/`, `src/application/`, `src/infrastructure/`, `src/interface/`
- Implement bootstrap.py composition root (H-09 compliance)
- Add architecture tests validating layer dependencies (H-07, H-08)

### Phase 2: Migration (Weeks 2-3)
- Migrate one domain aggregate (WorkItem) to hexagonal structure as a reference implementation
- Refactor persistence to use Repository port + adapter pattern
- Update tests to use in-memory adapter for unit testing

### Phase 3: Expansion (Weeks 4-6)
- Migrate remaining domain aggregates
- Implement CLI interface adapter for FEAT-042

### Success Criteria
- All domain layer tests run without database or HTTP mocks (target: <1s test suite execution)
- CLI and web API share identical application layer code (no duplication)
- Architecture tests pass (no H-07, H-08 violations)

## Traceability
- **Requirements:** FEAT-042 (CLI support), TECH-DEBT-018 (testability issues)
- **Stakeholders:** Engineering team, Product Owner
- **Prior decisions:** None (first architecture ADR)
```

---

**After Re-Scoring (S-014 Applied Again):**

- **Completeness:** 0.95 (all sections present, detailed context, alternatives, implementation plan)
- **Internal Consistency:** 0.95 (no contradictions, all claims justified)
- **Methodological Rigor:** 0.92 (alternatives analyzed, trade-offs documented, selection rationale clear)
- **Evidence Quality:** 0.93 (two citations, case study, traceability to requirements)
- **Actionability:** 0.94 (phased implementation plan with timeline and success criteria)
- **Traceability:** 0.90 (stakeholders identified, requirements linked, related ADRs documented)

**Weighted Composite:** (0.95 * 0.20) + (0.95 * 0.20) + (0.92 * 0.20) + (0.93 * 0.15) + (0.94 * 0.15) + (0.90 * 0.10) = **0.93/1.00**

**Verdict:** PASS (H-13 threshold met)

---

## Section 8: Integration

### Canonical Pairings

S-014 is the universal scoring mechanism and pairs with all other strategies:

| Strategy Pair | Order | Rationale |
|---------------|-------|-----------|
| **S-003 + S-014** | S-003 → S-014 | Steelman strengthens deliverable before scoring; establishes quality baseline (H-16 compliance for baseline) |
| **S-002 + S-014** | S-003 → S-002 → S-014 | H-16 requires S-003 before S-002; Devil's Advocate finds flaws; S-014 scores revised version |
| **S-004 + S-014** | S-003 → S-004 → S-014 | H-16 requires S-003 before S-004; Pre-Mortem identifies risks; S-014 scores mitigated version |
| **S-007 + S-014** | S-007 → S-014 | Constitutional critique finds principle violations; S-014 scores compliant version |
| **S-010 + S-014** | S-010 → S-014 | Self-Refine iterates; S-014 confirms exit criteria (H-15 self-review before presentation) |
| **S-012 + S-014** | S-012 → S-014 | FMEA identifies failure modes; S-014 scores after mitigations added |
| **S-013 + S-014** | S-013 → S-014 | Inversion reveals assumptions; S-014 scores after assumptions addressed |
| **S-011 + S-014** | S-011 → S-014 | Chain-of-Verification validates claims; S-014 scores verified deliverable |
| **S-001 + S-014** | S-003 → S-001 → S-014 | H-16 requires S-003 before S-001; Red Team attacks; S-014 scores defended version |

**Multi-Strategy Orchestration (C3/C4):**
- **Typical sequence:** S-003 → [S-002, S-004, S-007, S-012, S-013] → S-014
- **S-014 position:** Always LAST in the sequence (scores the deliverable after all improvements)

---

### H-16 Compliance

**H-16 Rule:** Steelman before critique (S-003 MUST execute before S-002, S-004, S-001)

**S-014 Relationship to H-16:**
- S-014 is NOT a critique strategy (it is a scoring strategy)
- H-16 does NOT directly constrain S-014 placement
- However, **S-003 is RECOMMENDED before S-014** to establish a quality baseline that S-014 can score fairly
- Without S-003, S-014 may score a weaker first draft; with S-003, S-014 scores a strengthened version

**Compliant Orderings:**
- S-003 → S-014 (recommended)
- S-003 → S-002 → S-014 (H-16 compliant)
- S-014 alone (permitted but not optimal)

**Non-Compliant Orderings:**
- S-002 → S-003 → S-014 (H-16 violation: S-002 before S-003)
- S-004 → S-014 (H-16 violation if S-003 not already run: S-004 before S-003)

---

### Criticality-Based Selection Table

| Level | Name | Scope | Required Strategies | Optional Strategies | S-014 Status |
|-------|------|-------|---------------------|---------------------|--------------|
| C1 | Routine | Reversible in 1 session, <3 files | S-010 | S-003, S-014 | OPTIONAL |
| C2 | Standard | Reversible in 1 day, 3-10 files | S-007, S-002, S-014 | S-003, S-010 | REQUIRED |
| C3 | Significant | >1 day to reverse, >10 files, API changes | C2 + S-004, S-012, S-013 | S-001, S-003, S-010, S-011 | REQUIRED |
| C4 | Critical | Irreversible, architecture/governance/public | All 10 selected | None | REQUIRED |

**Source:** quality-enforcement.md Criticality Levels table (SSOT). Values MUST match exactly.

**S-014 Usage Pattern:**
- **C1:** Optional (quality scoring may be skipped for routine work; S-010 self-review alone may suffice)
- **C2:** Required (all Standard deliverables MUST achieve H-13 threshold >= 0.92)
- **C3:** Required (all Significant deliverables MUST achieve H-13 threshold >= 0.92)
- **C4:** Required (all Critical deliverables MUST achieve H-13 threshold >= 0.92 with all 10 strategies applied)

---

### Cross-References

**SSOT and Source Documents:**
- `.context/rules/quality-enforcement.md` — Authoritative source for H-13 threshold, dimension weights, criticality levels, strategy catalog
- `ADR-EPIC002-001` — Strategy selection methodology, composite score 4.40, exclusion rationale for S-005 through S-015
- `ADR-EPIC002-002` — 5-layer enforcement architecture, token budgets, leniency bias counteraction design
- `.context/templates/adversarial/TEMPLATE-FORMAT.md` — Canonical format this template conforms to (v1.1.0)

**Related Strategy Templates:**
- `s-003-steelman.md` — Pair before S-014 to strengthen deliverable before scoring
- `s-002-devils-advocate.md` — Pair with S-014 to score post-critique revision
- `s-004-pre-mortem.md` — Pair with S-014 to score post-risk-mitigation revision
- `s-007-constitutional-ai.md` — Pair with S-014 to score post-compliance revision
- `s-010-self-refine.md` — Pair with S-014 to score iterative self-improvement

**Agent Specifications:**
- `skills/adversary/agents/adv-scorer.md` — Agent implementing S-014 with detailed scoring process and leniency bias counteraction protocol

**HARD Rules:**
- H-13 (quality-enforcement.md) — Threshold >= 0.92 for C2+ deliverables
- H-14 (quality-enforcement.md) — Creator-critic-revision cycle, minimum 3 iterations
- H-15 (quality-enforcement.md) — Self-review before presenting (applies to S-014 score reports themselves)
- H-16 (quality-enforcement.md) — Steelman before critique (affects S-003 placement relative to S-002/S-004/S-001)
- H-17 (quality-enforcement.md) — Quality scoring REQUIRED for deliverables (mandates S-014 for C2+)

---

## Validation Checklist

Use this checklist to validate this S-014 template against TEMPLATE-FORMAT.md v1.1.0.

### Structure

- [x] All 8 canonical sections present in order (Identity, Purpose, Prerequisites, Execution Protocol, Output Format, Scoring Rubric, Examples, Integration)
- [x] H-23: Navigation table present with Document Sections
- [x] H-24: Navigation table uses anchor links
- [x] Metadata blockquote header present
- [x] File length 1030 lines (exceeds 200-500 target due to comprehensive example and detailed rubrics, but within acceptable range for highest-complexity strategy)

### Content per Section

| Section | Validation Criteria | Status |
|---------|---------------------|--------|
| 1. Identity | 7 required fields; Criticality Tier table; values match SSOT | ✓ PASS |
| 2. Purpose | 5 "When to Use"; 4 "When NOT to Use"; measurable outcome; pairing recommendations with H-16 | ✓ PASS |
| 3. Prerequisites | Input checklist (4 items); context requirements (4 items); ordering constraints (4 items) | ✓ PASS |
| 4. Execution Protocol | 7 steps; step format followed; decision points; LJ-NNN finding prefix; severity definitions | ✓ PASS |
| 5. Output Format | 7 output sections (header, summary, findings, details, recommendations, impact, bias check); scoring impact table with correct weights; evidence requirements | ✓ PASS |
| 6. Scoring Rubric | Threshold bands match SSOT; weights match SSOT; strategy-specific 4-band rubric for all 6 dimensions | ✓ PASS |
| 7. Examples | 1 example (ADR scoring); C2 criticality; Before/After; findings with LJ-NNN identifiers; 2 Critical findings (Evidence Quality, Traceability); 152 lines | ✓ PASS |
| 8. Integration | Pairings (9 strategies); H-16 compliance documented; criticality table matches SSOT; cross-references to SSOT, ADRs, templates, agents, HARD rules | ✓ PASS |

### Constants Compliance

- [x] H-13 threshold (>= 0.92) sourced from quality-enforcement.md, not redefined
- [x] Dimension weights (Completeness 0.20, etc.) sourced from quality-enforcement.md, not redefined
- [x] Criticality levels (C1 optional, C2+ required) sourced from quality-enforcement.md, not redefined
- [x] Finding prefix (LJ-NNN) sourced from TEMPLATE-FORMAT.md Strategy Catalog Reference
- [x] Composite score (4.40) sourced from quality-enforcement.md Strategy Catalog

### H-15 Self-Review (Leniency Bias Check for This Template)

- [x] Each section independently authored with specific evidence from TEMPLATE-FORMAT.md
- [x] No contradictions between sections (e.g., Criticality Tier Table matches Integration table)
- [x] Mathematical accuracy verified (dimension weights sum to 1.00)
- [x] Evidence quality: All constants traced to quality-enforcement.md; all format requirements traced to TEMPLATE-FORMAT.md
- [x] Actionability: Execution Protocol provides reproducible 7-step procedure; Output Format specifies exact structure
- [x] Traceability: All SSOT references documented in Cross-References; all HARD rules cited where applicable

**Template Quality Self-Assessment:** This template meets TEMPLATE-FORMAT.md v1.1.0 requirements with high fidelity. All 8 sections present and complete. All constants sourced from SSOT. Example demonstrates C2 scoring with measurable before/after improvement. No deviations from canonical format detected.

---

<!-- TEMPLATE INSTANTIATION NOTES:
- Format version: TEMPLATE-FORMAT.md v1.1.0
- All constants sourced from quality-enforcement.md (H-13 threshold, dimension weights, criticality levels)
- Finding prefix LJ-NNN assigned per TEMPLATE-FORMAT.md Strategy Catalog Reference
- Academic foundation: Zheng et al. 2023, Kim et al. 2023, Anthropic Constitutional AI
- Leniency bias counteraction is the core methodological differentiator for S-014
- This template is subject to C3+ review per AE-002 (touches .context/templates/)
-->

---

*Template Version: 1.0.0*
*Format Conformance: TEMPLATE-FORMAT.md v1.1.0*
*SSOT: `.context/rules/quality-enforcement.md`*
*Created: 2026-02-15*
*Enabler: EN-803*
