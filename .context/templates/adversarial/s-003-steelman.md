# S-003: Steelman Technique -- Adversarial Strategy Execution Template

<!--
TEMPLATE: S-003 Steelman Technique Adversarial Strategy Execution Template
VERSION: 1.0.0 | DATE: 2026-02-15
SOURCE: quality-enforcement.md SSOT, ADR-EPIC002-001, TEMPLATE-FORMAT.md v1.1.0
ENABLER: EN-807 (S-003 Template)
STATUS: ACTIVE
CONFORMANCE: TEMPLATE-FORMAT.md v1.1.0

Academic Foundation:
- Davidson (1973): "Radical Interpretation" — Principle of Charity in analytic philosophy
- Wilson (1959): Original formulation of the Principle of Charity
- Chappell (2012): Steelmanning as intellectual practice in rationalist discourse
- Galef (2021): "The Scout Mindset" — seeking truth over defending positions

Strengthens deliverables by reconstructing arguments in their strongest possible form
before subjecting them to adversarial critique. Ensures fairness and robustness in review.
Second-highest-ranked strategy (composite score 4.30) in the Jerry quality framework.

UNIQUE PROPERTY: S-003 is the ONLY constructive (non-attacking) adversarial strategy.
It strengthens rather than critiques. H-16 mandates S-003 execution BEFORE all critique
strategies (S-002, S-004, S-001).
-->

> **Type:** adversarial-strategy-template
> **Status:** ACTIVE
> **Version:** 1.0.0
> **Date:** 2026-02-15
> **Source:** quality-enforcement.md, ADR-EPIC002-001, ADR-EPIC002-002
> **Format Conformance:** TEMPLATE-FORMAT.md v1.1.0
> **Enabler:** EN-807

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Section 1: Identity](#section-1-identity) | Strategy classification and metadata |
| [Section 2: Purpose](#section-2-purpose) | When to use, expected outcomes, pairings |
| [Section 3: Prerequisites](#section-3-prerequisites) | Required inputs and context |
| [Section 4: Execution Protocol](#section-4-execution-protocol) | Step-by-step Steelman reconstruction procedure |
| [Section 5: Output Format](#section-5-output-format) | Required structure for Steelman output |
| [Section 6: Scoring Rubric](#section-6-scoring-rubric) | Meta-evaluation of strategy execution |
| [Section 7: Examples](#section-7-examples) | Concrete Steelman demonstration |
| [Section 8: Integration](#section-8-integration) | Cross-strategy pairing and criticality mapping |

---

## Section 1: Identity

| Field | Value |
|-------|-------|
| Strategy ID | S-003 |
| Strategy Name | Steelman Technique |
| Family | Dialectical Synthesis |
| Composite Score | 4.30 |
| Finding Prefix | SM-NNN |
| Version | 1.0.0 |
| Date | 2026-02-15 |

### Criticality Tier Table

| Criticality Level | C1 (Routine) | C2 (Standard) | C3 (Significant) | C4 (Critical) |
|-------------------|--------------|---------------|------------------|---------------|
| **S-003 Status** | OPTIONAL | OPTIONAL | OPTIONAL | REQUIRED |

**Source:** quality-enforcement.md Criticality Levels table (SSOT).

**Interpretation:** S-003 is OPTIONAL at C1, C2, and C3, but REQUIRED at C4 where all 10 selected strategies must execute. Despite being optional at lower criticality levels, S-003 is strongly RECOMMENDED whenever adversarial critique strategies (S-002, S-004, S-001) will follow, per H-16 (Steelman before critique).

**Unique Property:** S-003 is the only constructive adversarial strategy -- it strengthens rather than attacks. Its findings identify improvement opportunities in the original, not failures.

---

## Section 2: Purpose

### When to Use

S-003 SHOULD be applied in the following scenarios:

1. **Before any adversarial critique (H-16 compliance):** H-16 mandates Steelman before Devil's Advocate (S-002), Pre-Mortem (S-004), and Red Team (S-001). Run S-003 FIRST to ensure critique targets the strongest version of the deliverable, not a weak first draft. This is the primary trigger for S-003.

2. **When evaluating competing alternatives:** If multiple design options, architectural approaches, or decision paths exist, Steelman each alternative before comparing. This prevents premature dismissal of viable options and ensures fair evaluation on merits rather than presentation quality.

3. **When the original author is absent:** If reviewing work created by someone else (or by a prior agent session), the deliverable may not represent the author's full intent. Steelman reconstructs the strongest interpretation, preventing unfair critique of poorly expressed but sound ideas.

4. **When an idea is being dismissed too quickly:** If initial reaction to a proposal is negative, apply S-003 before rejecting. The Steelman may reveal hidden strengths that change the evaluation, or confirm that the idea is genuinely weak even in its strongest form.

5. **C4 Critical deliverables (REQUIRED):** All 10 strategies execute at C4. S-003 is the mandatory first step before tournament-mode adversarial critique.

### When NOT to Use

S-003 SHOULD NOT be applied in these scenarios:

1. **Extreme time pressure where strengthening adds no value:** If the deliverable is already in its strongest form (e.g., after multiple revision cycles with high S-014 scores), additional Steelman reconstruction yields diminishing returns. Redirect to S-014 for final scoring instead.

2. **Clearly unethical, dangerous, or fundamentally flawed proposals:** The Steelman technique assumes the idea has potential merit worth surfacing. If the proposal violates constitutional principles (HARD rules) in ways that cannot be remediated, skip S-003 and proceed directly to S-007 Constitutional AI Critique to identify violations. Strengthening an unconstitutional proposal wastes effort.

3. **Analysis paralysis risk:** If the review process is already consuming excessive time and S-003 would further delay decision-making without proportionate quality improvement, proceed to critique strategies directly with documented justification for skipping S-003.

### Expected Outcome

A successful S-003 execution produces:

- **Steelman Reconstruction:** The deliverable rewritten in its strongest possible form, with gaps filled, evidence strengthened, logical connections tightened, and obvious objections preemptively addressed
- **Improvement Findings Table:** SM-NNN findings documenting WHAT was improved and WHY, enabling the original author to incorporate improvements
- **Improvement magnitude classification:** Each finding classified as Critical (fundamental gap filled), Major (significant strengthening), or Minor (polish applied)
- **Quality baseline:** A strengthened version that subsequent critique strategies (S-002, S-004, S-001) can attack fairly, ensuring robustness testing targets the best version

### Pairing Recommendations

S-003 is the canonical FIRST strategy in adversarial review sequences per H-16:

| Pairing | Order | Rationale |
|---------|-------|-----------|
| **S-003 + S-002** | S-003 --> S-002 | H-16 REQUIRED. Steelman before Devil's Advocate ensures critique targets strongest version |
| **S-003 + S-004** | S-003 --> S-004 | H-16 REQUIRED. Steelman before Pre-Mortem ensures risk analysis targets best-case scenario |
| **S-003 + S-001** | S-003 --> S-001 | H-16 REQUIRED. Steelman before Red Team ensures attack simulation targets fortified version |
| **S-003 + S-014** | S-003 --> S-014 | RECOMMENDED. Steelman strengthens deliverable before scoring, establishing quality baseline |
| **S-003 + S-007** | S-003 --> S-007 | RECOMMENDED. Steelman before constitutional review ensures fair evaluation |
| **Full C4 sequence** | S-003 --> [S-002, S-004, S-007, S-012, S-013] --> S-014 | S-003 always FIRST; S-014 always LAST |

**H-16 Note:** S-003 IS the strategy that H-16 requires to run first. S-003 itself has NO prerequisite strategies -- it is always the starting point of an adversarial review sequence.

---

## Section 3: Prerequisites

### Required Inputs

Before executing S-003, the following MUST be available:

- [ ] **Deliverable artifact** -- The document, design, code, or decision record to be strengthened
- [ ] **Deliverable intent** -- Understanding of what the deliverable is trying to achieve (from requirements, specifications, or context)
- [ ] **Domain context** -- Sufficient background knowledge to identify the strongest possible interpretation (domain expertise required)
- [ ] **Criticality level** -- C1/C2/C3/C4 classification to determine whether S-003 is optional or required

### Context Requirements

The Steelman executor MUST have access to:

- **Quality-enforcement.md SSOT** -- Source for scoring dimensions, weights, and threshold
- **Deliverable requirements or specification** -- To understand what "strongest form" means for this specific deliverable
- **Domain knowledge** -- S-003 requires sufficient expertise to identify missing evidence, strengthen logical connections, and fill gaps. Without domain knowledge, the Steelman may inadvertently weaken the argument
- **Related prior art (if available)** -- Existing research, citations, or data that could strengthen the deliverable's claims

### Ordering Constraints

S-003 has the following ordering properties:

1. **S-003 runs FIRST.** Per H-16, S-003 MUST execute before any critique strategy (S-002, S-004, S-001). No prior adversarial strategy is required before S-003.

2. **S-003 output feeds into critique strategies.** The Steelman Reconstruction produced by S-003 becomes the artifact that S-002 (Devil's Advocate), S-004 (Pre-Mortem), and S-001 (Red Team) evaluate.

3. **S-010 Self-Refine MAY precede S-003.** While not required, the creator may apply S-010 self-review before S-003 to address obvious surface issues. S-010 is not constrained by H-16 (it is self-review, not adversarial critique).

4. **S-003 is NOT a substitute for revision.** S-003 produces a reconstructed strongest version and improvement findings. The original author SHOULD incorporate S-003 findings before proceeding to critique strategies.

---

## Section 4: Execution Protocol

S-003 follows a six-step procedure to produce a Steelman Reconstruction with documented improvement findings.

**Orientation Note:** Unlike critique strategies that identify failures, S-003 identifies WHERE and HOW the deliverable can be STRENGTHENED. Findings are improvement opportunities, not defects. The executor adopts an empathetic, charitable stance -- seeking the best possible interpretation of the author's intent.

### Step 1: Deep Understanding

**Action:** Read the deliverable thoroughly and seek the most charitable interpretation of its intent, claims, and arguments.

**Procedure:**
1. Read the entire deliverable without judgment, focusing on understanding what the author is trying to achieve
2. Identify the core thesis or purpose -- "What is this deliverable fundamentally arguing or proposing?"
3. List all claims, arguments, and supporting evidence present in the deliverable
4. For each claim, ask: "What is the most charitable interpretation of this claim?"
5. Note areas where the author's intent is clear but expression is weak -- these are strengthening opportunities, not failures
6. Document initial understanding in a brief summary (3-5 sentences)

**Decision Point:**
- If the deliverable is fundamentally incoherent (no discernible thesis or purpose): Flag and recommend the author clarify intent before Steelman can proceed. Document the incoherence and exit.
- If intent is discernible: Proceed to Step 2.

**Output:** Charitable interpretation summary documenting the deliverable's core thesis, key claims, and identified strengthening opportunities.

---

### Step 2: Identify Weaknesses in Presentation (Not Substance)

**Action:** Distinguish between flaws in the IDEA and flaws in the EXPRESSION. S-003 focuses on strengthening expression while preserving the original idea.

**Procedure:**
1. For each section of the deliverable, classify weaknesses as:
   - **Presentation weakness:** The idea is sound but poorly expressed (vague language, missing evidence for a valid claim, weak logical connection that could be tightened)
   - **Structural weakness:** The argument structure is incomplete (missing sections, gaps in reasoning chain, absent counterargument handling)
   - **Evidence weakness:** Claims lack supporting data that is available or could be supplied (missing citations, unsupported assertions, anecdotal evidence where data exists)
   - **Substantive weakness:** The idea itself may be flawed (this is noted but NOT addressed by S-003; it is left for S-002/S-004 to evaluate)
2. For each presentation, structural, or evidence weakness, note the strongest possible version of what the author likely intended
3. Estimate the improvement magnitude for each weakness:
   - **Critical:** Fundamental gap that undermines the core argument -- filling it transforms the deliverable
   - **Major:** Significant weakness in presentation or evidence -- strengthening it substantially improves quality
   - **Minor:** Polish opportunity -- addressing it improves readability or rigor without changing substance

**Decision Point:**
- If only substantive weaknesses found (the idea itself is flawed, not just the expression): Document this assessment and proceed with caution. The Steelman will present the idea in its best light, but note that subsequent critique strategies may still reject it on substance.
- If presentation/structural/evidence weaknesses found: Proceed to Step 3.

**Output:** Weakness classification table with type, magnitude, and intended strongest interpretation.

---

### Step 3: Reconstruct the Argument

**Action:** Rewrite the deliverable in its strongest possible form, filling gaps and strengthening weak points while preserving the original author's intent.

**Procedure:**
1. **Supply missing evidence:** Where claims are unsupported, add citations, data, or logical arguments that support the claim (using domain knowledge and available references)
2. **Strengthen logical connections:** Where reasoning jumps exist, add intermediate steps that make the argument chain explicit and compelling
3. **Address obvious objections preemptively:** For each major claim, identify the most likely counterargument and add a preemptive response
4. **Frame for the most favorable audience:** Rewrite sections using the strongest available framing (e.g., replace vague "seems good" with specific "reduces latency by 40% based on benchmark data")
5. **Use the strongest available data:** Replace anecdotal evidence with quantitative data where possible; upgrade weak citations to authoritative sources
6. **Preserve original intent:** Do NOT change the fundamental thesis or direction. The Steelman strengthens the existing argument, it does not replace it with a different argument
7. **Label all changes:** Mark each improvement so the original author can see what was changed and why

**Decision Point:**
- If reconstruction requires changing the fundamental thesis: STOP. This is no longer Steelmanning -- it is creating a different argument. Document the limitation and present the best possible version of the ORIGINAL thesis.
- If reconstruction preserves original intent while substantially improving quality: Proceed to Step 4.

**Output:** Steelman Reconstruction -- the deliverable rewritten in its strongest form with all changes labeled.

---

### Step 4: Identify the Best Case Scenario

**Action:** Articulate the conditions under which the Steelman Reconstruction is most compelling, providing context for subsequent critique strategies.

**Procedure:**
1. Define the ideal conditions: "Under what circumstances is this proposal strongest?"
2. Identify supporting assumptions: "What must be true for this argument to hold?"
3. Document the strongest evidence chain: "What is the most compelling path from premises to conclusions?"
4. Note the target audience: "Who would find this argument most persuasive, and why?"
5. Assess confidence level: "How confident should a rational evaluator be in this Steelman version?"

**Output:** Best Case Scenario statement documenting ideal conditions, key assumptions, and confidence assessment.

---

### Step 5: Document Improvement Findings

**Action:** Formalize all improvements made during reconstruction as SM-NNN findings, documenting what was strengthened and why.

**Procedure:**
1. For each improvement made in Step 3, create a finding entry:
   - Assign unique identifier using SM-NNN prefix
   - Classify severity (improvement magnitude): Critical, Major, or Minor
   - Tag affected quality dimension (Completeness, Internal Consistency, Methodological Rigor, Evidence Quality, Actionability, Traceability)
   - Document the original content (before) and the strengthened content (after)
   - Explain why the improvement strengthens the argument
2. Sort findings by severity (Critical improvements first)
3. Map findings to the Scoring Impact table

**Finding Documentation Format:**

| ID | Improvement | Severity | Original | Strengthened | Affected Dimension |
|----|-------------|----------|----------|--------------|--------------------|
| SM-001 | {{Description of improvement}} | Critical/Major/Minor | {{Original content}} | {{Strengthened content}} | {{Dimension}} |

**Severity Definitions (Improvement Magnitude):**
- **Critical:** Fundamental gap in the original that undermines the core argument. Filling this gap transforms the deliverable from unconvincing to compelling. The original could not withstand critique without this improvement.
- **Major:** Significant weakness in presentation, evidence, or structure. Strengthening this materially improves quality across one or more scoring dimensions. The original would score notably lower without this improvement.
- **Minor:** Polish opportunity that improves readability, precision, or rigor without changing the substance or strength of the core argument.

**Output:** Improvement Findings Table with SM-NNN identifiers, severity, before/after content, and dimension mapping.

---

### Step 6: Present the Steelman

**Action:** Deliver the final Steelman Reconstruction with clear labeling and prepare the strengthened version for downstream critique strategies.

**Procedure:**
1. Assemble the complete Steelman output using the Output Format (Section 5)
2. Verify that the reconstruction preserves the original author's intent
3. Verify that all improvements are labeled and traceable
4. Apply H-15 self-review: check the Steelman output for quality before presenting
5. Confirm the Steelman is ready to serve as the baseline for critique strategies (S-002, S-004, S-001)

**Decision Point:**
- If the Steelman Reconstruction is substantially different from the original (many Critical/Major improvements): Recommend the original author review and incorporate improvements before critique proceeds
- If the Steelman Reconstruction is close to the original (mostly Minor improvements): The original is already strong; critique strategies can proceed directly

**Output:** Complete Steelman Report per Section 5 Output Format, ready for downstream strategies.

---

## Section 5: Output Format

Every S-003 execution MUST produce a Steelman Report with the following structure.

### Required Output Sections

#### 1. Header

```markdown
# Steelman Report: {{Deliverable Title}}

## Steelman Context
- **Deliverable:** {{Absolute file path or artifact identifier}}
- **Deliverable Type:** {{ADR|Research|Analysis|Synthesis|Design|Code|Template|Other}}
- **Criticality Level:** {{C1|C2|C3|C4}}
- **Strategy:** S-003 (Steelman Technique)
- **SSOT Reference:** .context/rules/quality-enforcement.md
- **Steelman By:** {{Agent or User Name}}
- **Date:** {{ISO-8601 timestamp}}
- **Original Author:** {{Name/ID of deliverable creator, if different from Steelman executor}}
```

#### 2. Summary

```markdown
## Summary

**Steelman Assessment:** {{1-2 sentence characterization of what was strengthened}}

**Improvement Count:** {{N Critical, N Major, N Minor improvements identified}}

**Original Strength:** {{Brief assessment of how strong the original was before Steelmanning}}

**Recommendation:** {{Incorporate improvements / Original already strong / Fundamental revision needed before Steelman can help}}
```

#### 3. Steelman Reconstruction

```markdown
## Steelman Reconstruction

{{The complete deliverable rewritten in its strongest possible form.
All improvements are marked with inline annotations [SM-NNN] referencing
the Improvement Findings Table.}}
```

#### 4. Improvement Findings Table

```markdown
## Improvement Findings

| ID | Improvement | Severity | Original | Strengthened | Affected Dimension |
|----|-------------|----------|----------|--------------|--------------------|
| SM-001 | {{Description}} | Critical/Major/Minor | {{Before}} | {{After}} | {{Dimension}} |
| SM-002 | {{Description}} | Critical/Major/Minor | {{Before}} | {{After}} | {{Dimension}} |
```

**Severity Key:**
- **Critical:** Fundamental gap filled; transforms core argument strength
- **Major:** Significant presentation/evidence/structure improvement
- **Minor:** Polish improving readability or precision

#### 5. Improvement Details

Expanded description for each Critical and Major improvement:

```markdown
### SM-001: {{Improvement Title}} [CRITICAL/MAJOR]

**Affected Dimension:** {{Dimension name}}
**Original Content:** {{Quote from original deliverable}}
**Strengthened Content:** {{Quote from Steelman Reconstruction}}
**Rationale:** {{Why this improvement strengthens the argument}}
**Best Case Conditions:** {{Under what conditions is this improvement most valuable}}
```

#### 6. Scoring Impact

```markdown
## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Positive/Negative/Neutral | {{How Steelman improvements affect this dimension}} |
| Internal Consistency | 0.20 | Positive/Negative/Neutral | {{How Steelman improvements affect this dimension}} |
| Methodological Rigor | 0.20 | Positive/Negative/Neutral | {{How Steelman improvements affect this dimension}} |
| Evidence Quality | 0.15 | Positive/Negative/Neutral | {{How Steelman improvements affect this dimension}} |
| Actionability | 0.15 | Positive/Negative/Neutral | {{How Steelman improvements affect this dimension}} |
| Traceability | 0.10 | Positive/Negative/Neutral | {{How Steelman improvements affect this dimension}} |
```

**Impact Interpretation:**
- **Positive:** Steelman improvements directly strengthened this dimension
- **Neutral:** Dimension was already adequate; no significant change from Steelmanning
- **Negative:** Rare; would indicate Steelman process introduced a new weakness (flag for review)

### Evidence Requirements

Each improvement finding MUST include:

1. **Specific reference to location** in the original deliverable (section name, line number, heading, or paragraph identifier)
2. **Quotation or paraphrase** of the original content that was strengthened
3. **The strengthened version** showing what replaced it and why it is stronger
4. **Explanation** of how the improvement strengthens the argument (maps to scoring dimension criteria)

---

## Section 6: Scoring Rubric

This section defines how to evaluate the quality of an S-003 execution itself (meta-evaluation of the Steelman process).

### Threshold Bands

**SSOT threshold (from quality-enforcement.md, MUST NOT be redefined):** >= 0.92 weighted composite score. Below threshold = REJECTED; revision required per H-13.

**Operational bands for S-003 execution quality (template-specific subdivision for workflow guidance):**

| Band | Score Range | Outcome |
|------|------------|---------|
| PASS | >= 0.92 | Steelman execution accepted; reconstruction is genuinely strongest version |
| REVISE | 0.85 - 0.91 | Steelman execution requires targeted improvement; close to threshold (REJECTED per H-13) |
| REJECTED | < 0.85 | Steelman execution inadequate; significant rework required (REJECTED per H-13) |

> **Note:** The SSOT defines only the 0.92 threshold with REJECTED as the below-threshold outcome. The REVISE band (0.85-0.91) is a template-specific operational category (not sourced from quality-enforcement.md) to distinguish near-threshold deliverables requiring targeted fixes from those requiring significant rework. Both REVISE and REJECTED trigger the revision cycle per H-13.

---

### Dimension Weights (from quality-enforcement.md, MUST NOT be redefined)

| Dimension | Weight | Measures (for S-003 execution quality) |
|-----------|--------|----------------------------------------|
| Completeness | 0.20 | All deliverable sections examined; all strengthening opportunities identified; no gaps in reconstruction |
| Internal Consistency | 0.20 | Reconstruction is internally coherent; improvements do not contradict each other or the original intent |
| Methodological Rigor | 0.20 | Charitable interpretation applied; presentation vs. substance distinction maintained; original intent preserved |
| Evidence Quality | 0.15 | Each improvement backed by specific before/after evidence; strengthened claims supported by credible data |
| Actionability | 0.15 | Improvements are concrete and incorporable; original author can act on findings |
| Traceability | 0.10 | Improvements linked to original content and scoring dimensions; SM-NNN identifiers used consistently |

---

### Strategy-Specific Rubric (4-Band Criteria)

For each dimension, evaluate S-003 execution quality using these criteria:

#### Completeness

| Score Range | Criteria |
|-------------|----------|
| **0.95 - 1.00** | All deliverable sections examined for strengthening opportunities; all significant presentation, structural, and evidence weaknesses identified; reconstruction addresses every identified weakness; best case scenario articulated with supporting assumptions |
| **0.90 - 0.94** | Most deliverable sections examined; major strengthening opportunities identified; reconstruction addresses Critical and Major weaknesses; best case scenario present but assumptions incomplete |
| **0.85 - 0.89** | Core sections examined; some strengthening opportunities missed; reconstruction addresses Critical weaknesses but misses some Major ones; best case scenario mentioned but not developed |
| **<= 0.84** | Sections skipped; significant strengthening opportunities missed; reconstruction is incomplete; no best case scenario articulated |

---

#### Internal Consistency

| Score Range | Criteria |
|-------------|----------|
| **0.95 - 1.00** | Reconstruction is fully coherent; all improvements align with and reinforce each other; no contradictions between strengthened sections; original author's intent preserved throughout; severity classifications consistent with improvement magnitude |
| **0.90 - 0.94** | Reconstruction mostly coherent; improvements generally align; minor inconsistencies between strengthened sections (e.g., slightly different framing in two places); original intent preserved |
| **0.85 - 0.89** | Reconstruction has some inconsistencies; a few improvements conflict with each other or subtly shift the original intent; severity classifications mostly reasonable |
| **<= 0.84** | Reconstruction contradicts itself; improvements conflict or change the fundamental thesis; original intent not preserved; severity classifications inconsistent |

---

#### Methodological Rigor

| Score Range | Criteria |
|-------------|----------|
| **0.95 - 1.00** | All 6 steps executed systematically; charitable interpretation explicitly documented; presentation vs. substance distinction clearly maintained; original intent verified at each step; no substantive changes disguised as presentation improvements; domain expertise demonstrated in strengthening |
| **0.90 - 0.94** | All steps executed; charitable interpretation applied; presentation vs. substance distinction mostly maintained; original intent preserved; minor deviations from methodology documented |
| **0.85 - 0.89** | Most steps executed; charitable interpretation attempted but not always achieved; some blurring between presentation and substance improvements; methodology followed with shortcuts |
| **<= 0.84** | Steps skipped or executed superficially; no charitable interpretation documented; presentation and substance changes mixed without distinction; methodology not followed; reconstruction replaces rather than strengthens |

---

#### Evidence Quality

| Score Range | Criteria |
|-------------|----------|
| **0.95 - 1.00** | Every improvement finding has specific before/after evidence with location references; strengthened claims supported by credible, authoritative data or reasoning; added evidence is verifiable and relevant; no fabricated or speculative evidence |
| **0.90 - 0.94** | Most improvements have specific evidence; strengthened claims mostly supported; evidence is credible; minor gaps in before/after documentation for Minor findings |
| **0.85 - 0.89** | Critical and Major improvements have evidence; some Minor improvements lack before/after detail; strengthened evidence is reasonable but not always authoritative |
| **<= 0.84** | Improvements lack evidence; strengthened claims unsupported or speculative; before/after comparison missing or vague; evidence quality questionable |

---

#### Actionability

| Score Range | Criteria |
|-------------|----------|
| **0.95 - 1.00** | All improvements are concrete and directly incorporable by the original author; Steelman Reconstruction is a complete, usable artifact; improvement findings include clear before/after that enables direct adoption; no interpretation required |
| **0.90 - 0.94** | Most improvements are directly incorporable; reconstruction is usable; some improvements require minor interpretation by the original author |
| **0.85 - 0.89** | Improvements are generally actionable; reconstruction provides guidance; some improvements are vague or require significant interpretation |
| **<= 0.84** | Improvements are abstract or vague; reconstruction is not directly usable; original author cannot act on findings without substantial additional work |

---

#### Traceability

| Score Range | Criteria |
|-------------|----------|
| **0.95 - 1.00** | Every improvement traced to specific original content with SM-NNN identifier; findings linked to scoring dimensions; reconstruction annotated with inline references; improvement rationale traces to deliverable requirements |
| **0.90 - 0.94** | Most improvements traceable; SM-NNN identifiers used consistently; most findings linked to dimensions; minor gaps in inline annotation |
| **0.85 - 0.89** | Some improvements traceable; SM-NNN identifiers present but inconsistent; some dimension linkage missing; tracing requires effort |
| **<= 0.84** | Improvements not traceable; SM-NNN identifiers missing; no dimension linkage; cannot connect improvements to original content |

---

## Section 7: Examples

### Example 1: C2 Standard Deliverable -- ADR Steelman

**Context:**
- **Deliverable:** ADR proposing event-driven communication between bounded contexts
- **Deliverable Type:** ADR (Architecture Decision Record)
- **Criticality Level:** C2 (Standard) -- Architecture decision affecting 5 files, reversible in 1 day
- **Scenario:** S-003 applied before S-002 Devil's Advocate per H-16

---

**Before (Original ADR):**

```markdown
# ADR-015: Event-Driven Communication Between Bounded Contexts

## Status
Proposed

## Context
Our bounded contexts need to communicate. Direct method calls create coupling.

## Decision
Use domain events for inter-context communication.

## Consequences
- Bounded contexts will be more decoupled
- We need an event bus
- Eventually consistent
```

---

**Strategy Execution (S-003 Steelman):**

**Step 1: Deep Understanding**

Charitable interpretation: The author recognizes a real architectural problem (tight coupling between bounded contexts via direct method calls) and proposes a well-established solution (domain events). The ADR is brief but directionally sound. The core thesis -- event-driven communication reduces coupling and improves modularity -- is valid and well-supported in DDD literature.

**Step 2: Identify Weaknesses in Presentation**

| Weakness | Type | Magnitude |
|----------|------|-----------|
| Context is one sentence; lacks specific examples of coupling pain | Presentation | Major |
| No evidence or citations supporting event-driven approach | Evidence | Major |
| "Eventually consistent" listed without explaining trade-offs or mitigation | Structural | Critical |
| No alternatives considered section | Structural | Major |
| Implementation details absent | Structural | Minor |

All weaknesses are in presentation, structure, or evidence -- NOT in the core idea, which is sound.

**Step 3: Reconstruct the Argument (Steelman Reconstruction)**

```markdown
# ADR-015: Event-Driven Communication Between Bounded Contexts

## Status
Proposed

## Context
Our system contains three bounded contexts (Projects, WorkItems, Quality) that
currently communicate via direct method calls. [SM-001] This creates tight coupling:
changing the WorkItem aggregate's interface requires modifications in both Projects
and Quality contexts, violating the bounded context isolation principle (Vernon 2013).

Specific coupling pain points:
- Projects context imports WorkItem domain objects to check status
- Quality context calls WorkItem service methods directly for scoring
- Any schema change in WorkItems cascades to 2+ other contexts

[SM-002] This coupling pattern is documented as an anti-pattern in domain-driven
design (Evans 2003, Chapter 14) and violates H-07 (domain layer isolation) when
cross-context calls bypass the application layer.

## Alternatives Considered [SM-003]

| Option | Pros | Cons | Fit |
|--------|------|------|-----|
| Shared database | Simple, immediate consistency | Tight schema coupling, no context isolation | Poor |
| Synchronous API calls | Familiar, immediate response | Runtime coupling, cascading failures | Moderate |
| Domain events (async) | Full decoupling, resilient, auditable | Eventual consistency, event schema management | Strong |

## Decision
Use domain events published through an in-process event bus for inter-context
communication. Each context publishes events when state changes; interested
contexts subscribe and react independently.

## Evidence [SM-004]
- Evans (2003) "Domain-Driven Design": Bounded contexts communicate via published
  language (Chapter 14)
- Vernon (2013) "Implementing Domain-Driven Design": Domain events as integration
  mechanism (Chapter 8)
- Jerry architecture-standards.md H-07: Domain layer MUST NOT import from other layers

## Consequences

### Positive
- Full bounded context isolation: contexts share only event schemas, not domain objects
- Resilience: failure in one context does not cascade to subscribers
- Auditability: event log provides complete history of inter-context communication

### Negative
- [SM-005] Eventual consistency: read models may be stale for up to N seconds
  (configurable per subscriber). Mitigation: use synchronous command responses
  for operations requiring immediate consistency; reserve events for notification
  and projection updates.
- Event schema evolution: requires versioning strategy to prevent breaking changes.
  Mitigation: use schema registry pattern with backward compatibility guarantees.

### Risks
- Event ordering: concurrent events may arrive out of order.
  Mitigation: include correlation ID and sequence number in event metadata.
```

**Step 5: Document Improvement Findings**

| ID | Improvement | Severity | Original | Strengthened | Affected Dimension |
|----|-------------|----------|----------|--------------|--------------------|
| SM-001 | Added specific coupling examples | Major | "Direct method calls create coupling" | Named three contexts, documented specific coupling points and cascade effects | Evidence Quality |
| SM-002 | Added authoritative citations | Major | No references | Evans (2003) and Vernon (2013) citations with chapter references; H-07 linkage | Evidence Quality |
| SM-003 | Added alternatives considered | Major | No alternatives section | Three-option comparison table with pros/cons/fit assessment | Methodological Rigor |
| SM-004 | Added Evidence section | Major | No supporting evidence | Three authoritative references with specific chapter citations | Evidence Quality |
| SM-005 | Expanded consequences with mitigations | Critical | "Eventually consistent" (no elaboration) | Specific consistency model, configurable staleness, synchronous fallback for critical operations, schema versioning strategy, event ordering mitigation | Completeness |

**Scoring Impact:**

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Positive | SM-003, SM-005: Added alternatives and detailed consequences with mitigations |
| Internal Consistency | 0.20 | Positive | Consequences now explicitly address trade-offs mentioned in context |
| Methodological Rigor | 0.20 | Positive | SM-003: Alternatives analysis follows standard ADR methodology |
| Evidence Quality | 0.15 | Positive | SM-001, SM-002, SM-004: Specific examples and authoritative citations added |
| Actionability | 0.15 | Positive | SM-005: Mitigations are concrete and implementable |
| Traceability | 0.10 | Positive | SM-002: Linked to H-07 and DDD literature; ADR now traceable to requirements |

**Outcome:** Original ADR was directionally sound but inadequately expressed. Steelman Reconstruction fills 4 Major and 1 Critical gap while preserving the original thesis. The strengthened version is now ready for S-002 Devil's Advocate critique per H-16, which can test whether event-driven communication is truly the best approach by attacking the strongest version of the argument.

---

## Section 8: Integration

### Canonical Pairings

S-003 is the canonical FIRST strategy in all adversarial review sequences:

| Strategy Pair | Order | Rationale |
|---------------|-------|-----------|
| **S-003 + S-002** | S-003 --> S-002 | H-16 REQUIRED. Steelman strengthens before Devil's Advocate attacks. Ensures critique targets merit, not presentation weakness |
| **S-003 + S-004** | S-003 --> S-004 | H-16 REQUIRED. Steelman establishes best case before Pre-Mortem identifies failure modes. Ensures risk analysis is fair |
| **S-003 + S-001** | S-003 --> S-001 | H-16 REQUIRED. Steelman fortifies before Red Team attacks. Ensures adversarial testing targets strongest defense |
| **S-003 + S-007** | S-003 --> S-007 | RECOMMENDED. Steelman before constitutional review ensures fair evaluation of compliance |
| **S-003 + S-014** | S-003 --> S-014 | RECOMMENDED. Steelman establishes quality baseline for scoring; S-014 scores strengthened version |
| **S-003 + S-010** | Independent | S-010 (self-review) is not constrained by H-16. Either may run first depending on workflow |

**Multi-Strategy Orchestration (C3/C4):**
- **Typical sequence:** S-003 --> [S-002, S-004, S-007, S-012, S-013] --> S-014
- **S-003 position:** Always FIRST in the sequence (strengthens before all critique)

---

### H-16 Compliance

**H-16 Rule:** Steelman before critique (S-003 MUST execute before S-002, S-004, S-001).

**S-003 IS the strategy that H-16 requires to run first.** This template defines the procedure for H-16 compliance. Specifically:

- S-003 has NO prerequisite adversarial strategies. It is always the starting point.
- S-003 output (the Steelman Reconstruction) becomes the artifact evaluated by subsequent critique strategies.
- Any adversarial review sequence that includes S-002, S-004, or S-001 MUST execute S-003 first.
- Skipping S-003 when S-002, S-004, or S-001 are applied constitutes an H-16 violation.

**Compliant Orderings:**
- S-003 --> S-002 --> S-014 (H-16 compliant)
- S-003 --> S-004 --> S-014 (H-16 compliant)
- S-003 --> S-001 --> S-014 (H-16 compliant)
- S-003 --> S-002 --> S-004 --> S-014 (H-16 compliant)
- S-010 --> S-003 --> S-002 --> S-014 (H-16 compliant; S-010 before S-003 is permitted)

**Non-Compliant Orderings:**
- S-002 --> S-003 (H-16 violation: Devil's Advocate before Steelman)
- S-004 --> S-003 (H-16 violation: Pre-Mortem before Steelman)
- S-001 --> S-003 (H-16 violation: Red Team before Steelman)
- S-002 without S-003 (H-16 violation: critique without Steelman)

---

### Criticality-Based Selection Table

| Level | Name | Scope | Required Strategies | Optional Strategies | S-003 Status |
|-------|------|-------|---------------------|---------------------|--------------|
| C1 | Routine | Reversible in 1 session, <3 files | S-010 | S-003, S-014 | OPTIONAL |
| C2 | Standard | Reversible in 1 day, 3-10 files | S-007, S-002, S-014 | S-003, S-010 | OPTIONAL |
| C3 | Significant | >1 day to reverse, >10 files, API changes | C2 + S-004, S-012, S-013 | S-001, S-003, S-010, S-011 | OPTIONAL |
| C4 | Critical | Irreversible, architecture/governance/public | All 10 selected | None | REQUIRED |

**Source:** quality-enforcement.md Criticality Levels table (SSOT). Values MUST match exactly.

**S-003 Usage Pattern:**
- **C1:** Optional. S-010 alone is the required strategy. S-003 may be used to strengthen deliverables before optional S-014 scoring.
- **C2:** Optional but RECOMMENDED when S-002 is required. H-16 mandates S-003 before S-002; while S-003 is listed as optional at C2, executing S-002 without S-003 violates H-16.
- **C3:** Optional but RECOMMENDED when S-004 or S-001 are applied. Same H-16 reasoning as C2.
- **C4:** Required. All 10 strategies execute; S-003 is the mandatory first step in the adversarial sequence.

**H-16 Interaction Note:** At C2 and C3, S-003 is listed as "optional" in the quality-enforcement.md criticality table. However, H-16 requires Steelman before critique. This means that when S-002 (required at C2) or S-004/S-001 (required/optional at C3) are executed, S-003 MUST precede them per H-16 regardless of its optional status in the criticality table. In practice, S-003 is effectively required whenever critique strategies execute.

---

### Cross-References

**SSOT and Source Documents:**
- `.context/rules/quality-enforcement.md` -- Authoritative source for H-16, H-13 threshold, dimension weights, criticality levels, strategy catalog
- `ADR-EPIC002-001` -- Strategy selection methodology, composite score 4.30, S-003 family classification (Dialectical Synthesis)
- `ADR-EPIC002-002` -- 5-layer enforcement architecture, token budgets
- `.context/templates/adversarial/TEMPLATE-FORMAT.md` -- Canonical format this template conforms to (v1.1.0)

**Related Strategy Templates:**
- `s-002-devils-advocate.md` -- Primary downstream consumer of S-003 output; H-16 requires S-003 before S-002
- `s-004-pre-mortem.md` -- Downstream consumer; H-16 requires S-003 before S-004
- `s-001-red-team.md` -- Downstream consumer; H-16 requires S-003 before S-001
- `s-014-llm-as-judge.md` -- Scores the Steelman Reconstruction or the revised deliverable incorporating S-003 improvements
- `s-007-constitutional-ai.md` -- Pair with S-003 for constitutional review of strengthened version
- `s-010-self-refine.md` -- May precede S-003; S-010 is not constrained by H-16

**HARD Rules:**
- H-16 (quality-enforcement.md) -- Steelman before critique; S-003 IS the strategy H-16 references
- H-13 (quality-enforcement.md) -- Threshold >= 0.92 for C2+ deliverables
- H-14 (quality-enforcement.md) -- Creator-critic-revision cycle, minimum 3 iterations
- H-15 (quality-enforcement.md) -- Self-review before presenting (applies to S-003 output itself)
- H-17 (quality-enforcement.md) -- Quality scoring REQUIRED for deliverables

**Academic Foundation:**
- Davidson (1973) "Radical Interpretation" -- Principle of Charity
- Wilson (1959) -- Original Principle of Charity formulation
- Chappell (2012) -- Steelmanning in rationalist discourse
- Galef (2021) "The Scout Mindset" -- Truth-seeking over position-defending

---

<!-- VALIDATION CHECKLIST (per TEMPLATE-FORMAT.md v1.1.0):
- [x] All 8 canonical sections present in order (Identity, Purpose, Prerequisites, Execution Protocol, Output Format, Scoring Rubric, Examples, Integration)
- [x] H-23: Navigation table present with Document Sections
- [x] H-24: Navigation table uses anchor links
- [x] Metadata blockquote header present
- [x] Finding prefix SM-NNN used consistently throughout
- [x] H-16 explicitly documented as S-003 being the FIRST strategy in canonical pairing
- [x] Criticality tier values match SSOT (Optional C1/C2/C3, Required C4)
- [x] Weights match SSOT exactly (0.20, 0.20, 0.20, 0.15, 0.15, 0.10)
- [x] REVISE band note included distinguishing it from SSOT threshold
- [x] Constructive orientation clear throughout (strengthening, not attacking)
- [x] Example at C2+ with at least one Critical improvement finding (SM-005)
- [x] Severity definitions adapted for improvement magnitude (not failure severity)
- [x] No absolute paths in template body
- [x] Strategy-specific rubric: 4-band criteria for all 6 dimensions
-->

---

*Template Version: 1.0.0*
*Format Conformance: TEMPLATE-FORMAT.md v1.1.0*
*SSOT: `.context/rules/quality-enforcement.md`*
*Created: 2026-02-15*
*Enabler: EN-807*
