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
| Finding Prefix | SM-NNN-{execution_id} |
| Version | 1.0.0 |
| Date | 2026-02-15 |

### Criticality Tier Table

| Criticality Level | C1 (Routine) | C2 (Standard) | C3 (Significant) | C4 (Critical) |
|-------------------|--------------|---------------|------------------|---------------|
| **S-003 Status** | OPTIONAL | OPTIONAL | OPTIONAL | REQUIRED |

**Source:** quality-enforcement.md Criticality Levels table (SSOT).

**Interpretation:** OPTIONAL at C1/C2/C3, REQUIRED at C4. Strongly RECOMMENDED whenever critique strategies follow (H-16). **Unique Property:** S-003 is the only constructive adversarial strategy -- it strengthens rather than attacks.

---

## Section 2: Purpose

### When to Use

1. **Before adversarial critique (H-16):** Primary trigger. S-003 MUST run before S-002/S-004/S-001 to ensure critique targets the strongest version.
2. **Evaluating competing alternatives:** Steelman each option before comparing to prevent premature dismissal.
3. **Original author absent:** Reconstruct strongest interpretation of potentially under-expressed work.
4. **Idea being dismissed too quickly:** S-003 may reveal hidden strengths or confirm genuine weakness.
5. **C4 Critical (REQUIRED):** Mandatory first step in tournament-mode adversarial critique.

### When NOT to Use

1. **Deliverable already strong:** After multiple revision cycles with high S-014 scores, additional Steelmanning yields diminishing returns.
2. **Fundamentally flawed/unconstitutional proposals:** Skip S-003, proceed to S-007 Constitutional AI Critique.
3. **Analysis paralysis risk:** Excessive review time with no proportionate quality gain; document justification for skipping.

### Expected Outcome

A successful S-003 execution produces: (1) **Steelman Reconstruction** -- deliverable rewritten in strongest form with gaps filled, evidence strengthened, objections preemptively addressed; (2) **Improvement Findings Table** -- SM-NNN findings with severity classification (Critical/Major/Minor); (3) **Quality baseline** for downstream critique strategies (S-002, S-004, S-001) to attack fairly.

### Pairing Recommendations

S-003 is the canonical FIRST strategy in adversarial review sequences per H-16. S-003 has NO prerequisite strategies -- it is always the starting point. See [Section 8: Integration](#section-8-integration) for the full pairing table, H-16 compliance details, and multi-strategy orchestration sequences.

---

## Section 3: Prerequisites

### Required Inputs

- [ ] **Deliverable artifact** -- The document, design, code, or decision record to be strengthened
- [ ] **Deliverable intent** -- Understanding of what the deliverable is trying to achieve
- [ ] **Domain context** -- Sufficient background to identify the strongest possible interpretation
- [ ] **Criticality level** -- C1/C2/C3/C4 classification per quality-enforcement.md SSOT

### Context Requirements

The executor MUST have access to quality-enforcement.md SSOT (dimensions, weights, threshold), deliverable requirements/specification, and domain knowledge sufficient to identify missing evidence and fill gaps. Related prior art (citations, data) SHOULD be available if applicable.

### Ordering Constraints

1. **S-003 runs FIRST** per H-16 before any critique strategy (S-002, S-004, S-001). No prior adversarial strategy required.
2. **S-003 output feeds critique strategies.** The Steelman Reconstruction becomes the artifact S-002/S-004/S-001 evaluate.
3. **S-010 MAY precede S-003** (self-review is not constrained by H-16).
4. **S-003 is NOT a substitute for revision.** The author SHOULD incorporate findings before critique proceeds.

---

## Section 4: Execution Protocol

Six-step procedure producing a Steelman Reconstruction with documented improvement findings. Unlike critique strategies, S-003 identifies WHERE and HOW to STRENGTHEN -- findings are improvement opportunities, not defects. The executor adopts a charitable stance seeking the best possible interpretation.

### Step 1: Deep Understanding

**Action:** Read the deliverable and seek the most charitable interpretation of its intent, claims, and arguments.

**Procedure:**
1. Read without judgment; identify the core thesis -- "What is this fundamentally arguing?"
2. List all claims, arguments, and supporting evidence
3. For each claim, ask: "What is the most charitable interpretation?"
4. Note areas where intent is clear but expression is weak (strengthening opportunities, not failures)
5. Document initial understanding in a brief summary (3-5 sentences)

**Decision Point:** If fundamentally incoherent (no discernible thesis): flag and exit. Otherwise proceed to Step 2.

**Output:** Charitable interpretation summary with core thesis, key claims, and strengthening opportunities.

---

### Step 2: Identify Weaknesses in Presentation (Not Substance)

**Action:** Distinguish flaws in EXPRESSION from flaws in the IDEA. S-003 strengthens expression while preserving the original idea.

**Procedure:**
1. Classify each weakness as:
   - **Presentation:** Sound idea, poorly expressed (vague language, weak logical connections)
   - **Structural:** Incomplete argument structure (missing sections, reasoning gaps)
   - **Evidence:** Claims lack available supporting data (missing citations, anecdotal evidence)
   - **Substantive:** Idea itself may be flawed (noted but NOT addressed by S-003; left for S-002/S-004)
2. For each non-substantive weakness, note the strongest version of the author's likely intent
3. Estimate improvement magnitude (Critical / Major / Minor per Step 5 severity definitions)

**Decision Point:** If only substantive weaknesses found: document and proceed with caution; subsequent critique strategies may reject on substance. Otherwise proceed to Step 3.

**Output:** Weakness classification table with type, magnitude, and intended strongest interpretation.

---

### Step 3: Reconstruct the Argument

**Action:** Rewrite the deliverable in its strongest possible form while preserving original intent.

**Procedure:**
1. **Supply missing evidence:** Add citations, data, or logical arguments for unsupported claims
2. **Strengthen logical connections:** Add intermediate reasoning steps where jumps exist
3. **Address obvious objections:** Add preemptive responses to likely counterarguments
4. **Use strongest framing:** Replace vague language with specific, data-backed claims
5. **Upgrade evidence:** Replace anecdotal evidence with quantitative data; upgrade to authoritative sources
6. **Preserve original intent:** Do NOT change the fundamental thesis -- strengthen, not replace
7. **Label all changes:** Mark each improvement with SM-NNN for traceability

**Decision Point:** If reconstruction requires changing the thesis: STOP, document limitation, present best version of ORIGINAL thesis. Otherwise proceed to Step 4.

**Output:** Steelman Reconstruction with all changes labeled.

---

### Step 4: Identify the Best Case Scenario

**Action:** Articulate conditions under which the Steelman Reconstruction is most compelling.

**Procedure:**
1. Define ideal conditions: "Under what circumstances is this proposal strongest?"
2. Identify supporting assumptions that must be true for the argument to hold
3. Document the strongest evidence chain from premises to conclusions
4. Assess confidence: "How confident should a rational evaluator be in this version?"

**Output:** Best Case Scenario statement with ideal conditions, key assumptions, and confidence assessment.

---

### Step 5: Document Improvement Findings

**Action:** Formalize all improvements as SM-NNN findings with severity, before/after evidence, and dimension mapping.

**Procedure:**
1. For each Step 3 improvement: assign SM-NNN identifier, classify severity, tag affected dimension, document before/after content with rationale
2. Sort findings by severity (Critical first)
3. Map findings to the Scoring Impact table

**Finding Format:** `| SM-NNN | Description | Critical/Major/Minor | Original | Strengthened | Dimension |`

**Severity Definitions (Improvement Magnitude) -- canonical location, referenced by Step 2 and Output Format:**
- **Critical:** Fundamental gap undermining the core argument; filling it transforms the deliverable. Original could not withstand critique without this improvement.
- **Major:** Significant presentation/evidence/structure weakness; strengthening it materially improves quality. Original would score notably lower without it.
- **Minor:** Polish improving readability, precision, or rigor without changing core argument substance.

**Output:** Improvement Findings Table with SM-NNN identifiers, severity, before/after, and dimension mapping.

---

### Step 6: Present the Steelman

**Action:** Assemble and verify the final Steelman Reconstruction for downstream use.

**Procedure:**
1. Assemble output per Section 5 Output Format
2. Verify reconstruction preserves original intent and all improvements are traceable
3. Apply H-15 self-review before presenting
4. Confirm readiness for downstream critique strategies (S-002, S-004, S-001)

**Decision Point:** If substantially different from original (many Critical/Major): recommend author review before critique. If close to original (mostly Minor): proceed directly.

**Output:** Complete Steelman Report per Section 5, ready for downstream strategies.

---

## Section 5: Output Format

Every S-003 execution MUST produce a Steelman Report with the following sections.

> **Strategy-Specific Adaptation (CR-002):** S-003 replaces the standard "Recommendations" output section with "Steelman Reconstruction" (Section 3 below). This is a legitimate adaptation because the reconstruction IS the recommendation -- the deliverable rewritten in its strongest form is the actionable output of the Steelman technique.

### Required Output Sections

#### 1. Header

```markdown
# Steelman Report: {{Deliverable Title}}
## Steelman Context
- **Deliverable:** {{file path or artifact identifier}}
- **Deliverable Type:** {{ADR|Research|Analysis|Synthesis|Design|Code|Template|Other}}
- **Criticality Level:** {{C1|C2|C3|C4}}
- **Strategy:** S-003 (Steelman Technique)
- **SSOT Reference:** .context/rules/quality-enforcement.md
- **Steelman By:** {{Agent or User}} | **Date:** {{ISO-8601}} | **Original Author:** {{if different}}
```

#### 2. Summary

```markdown
## Summary
**Steelman Assessment:** {{1-2 sentence characterization}}
**Improvement Count:** {{N Critical, N Major, N Minor}}
**Original Strength:** {{Assessment of pre-Steelman quality}}
**Recommendation:** {{Incorporate improvements / Already strong / Fundamental revision needed}}
```

#### 3. Steelman Reconstruction

The complete deliverable rewritten in strongest form with inline `[SM-NNN]` annotations referencing the Findings Table.

#### 4. Improvement Findings Table

Per Step 5 format. **Severity Key:** See Step 5 Severity Definitions.

#### 5. Improvement Details

Expanded description for each Critical and Major improvement: Affected Dimension, Original Content, Strengthened Content, Rationale, Best Case Conditions.

#### 6. Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Positive/Neutral/Negative | {{Effect of improvements}} |
| Internal Consistency | 0.20 | ... | ... |
| Methodological Rigor | 0.20 | ... | ... |
| Evidence Quality | 0.15 | ... | ... |
| Actionability | 0.15 | ... | ... |
| Traceability | 0.10 | ... | ... |

Impact: **Positive** = directly strengthened; **Neutral** = already adequate; **Negative** = rare, new weakness introduced (flag for review).

### Evidence Requirements

Each finding MUST include: (1) specific location reference in original, (2) before content, (3) after content, (4) rationale mapping to scoring dimension.

---

## Section 6: Scoring Rubric

Meta-evaluation of S-003 execution quality. **SSOT threshold:** >= 0.92 weighted composite (quality-enforcement.md). Below = REJECTED per H-13.

### Threshold Bands

| Band | Score Range | Outcome |
|------|------------|---------|
| PASS | >= 0.92 | Steelman execution accepted; reconstruction is genuinely strongest version |
| REVISE | 0.85 - < 0.92 | Steelman execution requires targeted improvement; close to threshold (REJECTED per H-13) |
| REJECTED | < 0.85 | Steelman execution inadequate; significant rework required (REJECTED per H-13) |

> **Note:** REVISE band (0.85 to < 0.92) is template-specific (not from SSOT) to distinguish near-threshold from significant-rework cases. Both REVISE and REJECTED trigger revision per H-13.

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

Evaluate S-003 execution quality per dimension. Each cell describes the minimum bar for that band.

| Dimension | 0.95-1.00 | 0.90-0.94 | 0.85-0.89 | <= 0.84 |
|-----------|-----------|-----------|-----------|---------|
| **Completeness** | All sections examined; all presentation/structural/evidence weaknesses identified and addressed; best case scenario with assumptions | Most sections examined; Critical+Major addressed; best case present but incomplete | Core sections only; some Major weaknesses missed; best case undeveloped | Sections skipped; significant gaps; no best case |
| **Internal Consistency** | Fully coherent reconstruction; improvements reinforce each other; original intent preserved; severity classifications consistent | Mostly coherent; minor framing inconsistencies; original intent preserved | Some inconsistencies; improvements occasionally conflict or shift intent | Reconstruction contradicts itself; intent not preserved |
| **Methodological Rigor** | All 6 steps systematic; charitable interpretation documented; presentation vs. substance distinction clear; domain expertise demonstrated | All steps executed; distinction mostly maintained; minor deviations documented | Most steps executed; some blurring of presentation vs. substance | Steps skipped; no charitable interpretation; reconstruction replaces rather than strengthens |
| **Evidence Quality** | Every finding has specific before/after with location refs; claims supported by credible data; no fabricated evidence | Most findings have evidence; claims mostly supported; minor gaps for Minor findings | Critical/Major have evidence; some Minor lack detail; evidence reasonable but not authoritative | Findings lack evidence; claims unsupported or speculative |
| **Actionability** | All improvements concrete and directly incorporable; reconstruction is complete usable artifact; no interpretation required | Most directly incorporable; reconstruction usable; minor interpretation needed | Generally actionable; some improvements vague or need significant interpretation | Abstract or vague; not directly usable |
| **Traceability** | Every improvement traced with SM-NNN; findings linked to dimensions; inline annotations; rationale traces to requirements | Most traceable; SM-NNN consistent; most dimension linkage; minor annotation gaps | Some traceable; SM-NNN inconsistent; some dimension linkage missing | Not traceable; SM-NNN missing; no dimension linkage |

---

## Section 7: Examples

### Example 1: C2 Standard Deliverable -- ADR Steelman

**Context:**
- **Deliverable:** ADR proposing event-driven communication between bounded contexts
- **Deliverable Type:** ADR (Architecture Decision Record)
- **Criticality Level:** C2 (Standard) -- Architecture decision affecting 5 files, reversible in 1 day
- **Scenario:** S-003 applied before S-002 Devil's Advocate per H-16

---

**Before (Original ADR excerpt):**

```markdown
## Context
Our bounded contexts need to communicate. Direct method calls create coupling.
## Decision
Use domain events for inter-context communication.
## Consequences
- Bounded contexts will be more decoupled
- We need an event bus
- Eventually consistent
```

**Strategy Execution (S-003 Steelman):**

**Step 1: Deep Understanding**

Charitable interpretation: The author recognizes tight coupling between bounded contexts and proposes domain events -- a well-established DDD solution. The ADR is brief but directionally sound. Core thesis (event-driven communication reduces coupling) is valid and well-supported in DDD literature.

**Step 2: Identify Weaknesses in Presentation**

| Weakness | Type | Magnitude |
|----------|------|-----------|
| Context lacks specific coupling examples | Presentation | Major |
| No evidence or citations | Evidence | Major |
| "Eventually consistent" without trade-off analysis | Structural | Critical |
| No alternatives considered | Structural | Major |

All weaknesses are in presentation/structure/evidence -- NOT in the core idea.

**Step 3: Reconstruct the Argument (key sections shown)**

Context strengthened with [SM-001] specific coupling pain points (3 contexts named, cascade effects documented) and [SM-002] DDD literature citations (Evans 2003 Ch.14, Vernon 2013 Ch.8, H-07 linkage). Added [SM-003] Alternatives Considered table (shared DB/sync API/domain events with pros/cons/fit). Added [SM-004] Evidence section with authoritative references. Consequences expanded with [SM-005] specific consistency model, configurable staleness, synchronous fallback for critical operations, schema versioning strategy, and event ordering mitigation with correlation IDs.

**Step 4: Best Case Scenario**

The event-driven approach is strongest when bounded contexts have clear autonomy, events represent naturally occurring domain state changes (not forced communication), and eventual consistency is acceptable for the majority of cross-context interactions. Key assumptions: (1) contexts are genuinely independent bounded contexts, not a single context artificially split; (2) event volume is manageable with in-process bus; (3) team understands eventual consistency trade-offs. Confidence: HIGH given established DDD patterns and Jerry's existing architecture alignment.

**Step 5: Improvement Findings**

| ID | Improvement | Severity | Affected Dimension |
|----|-------------|----------|--------------------|
| SM-001-20260215T1400 | Added specific coupling examples (3 contexts, cascade effects) | Major | Evidence Quality |
| SM-002-20260215T1400 | Added authoritative citations (Evans, Vernon, H-07) | Major | Evidence Quality |
| SM-003-20260215T1400 | Added alternatives considered table | Major | Methodological Rigor |
| SM-004-20260215T1400 | Added Evidence section with chapter references | Major | Evidence Quality |
| SM-005-20260215T1400 | Expanded consequences with mitigations | Critical | Completeness |

**Finding ID Format:** `SM-{NNN}-{execution_id}` where execution_id is a short timestamp or session identifier (e.g., `SM-001-20260215T1400`) to prevent ID collisions across tournament executions.

**Step 6: Present the Steelman**

Self-review applied (H-15). Reconstruction verified as preserving original thesis (event-driven communication). All 5 improvements labeled with SM-NNN identifiers. Ready for S-002 Devil's Advocate per H-16.

**Outcome:** Original ADR was directionally sound but inadequately expressed. Steelman fills 4 Major and 1 Critical gap. All 6 scoring dimensions positively impacted. Strengthened version ready for S-002 critique per H-16.

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

**H-16 Rule:** S-003 MUST execute before S-002, S-004, S-001. S-003 IS the strategy H-16 references. S-003 output becomes the artifact evaluated by subsequent critique strategies. Skipping S-003 when critique strategies execute is an H-16 violation.

| Ordering | H-16 Status | Note |
|----------|-------------|------|
| S-003 --> S-002 --> S-014 | Compliant | Standard C2 sequence |
| S-003 --> S-004 --> S-014 | Compliant | Standard C3 sequence |
| S-003 --> S-002 --> S-004 --> S-014 | Compliant | Multi-critique |
| S-010 --> S-003 --> S-002 --> S-014 | Compliant | S-010 before S-003 permitted |
| S-002 --> S-003 | **VIOLATION** | Critique before Steelman |
| S-004/S-001 --> S-003 | **VIOLATION** | Critique before Steelman |
| S-002 without S-003 | **VIOLATION** | Critique without Steelman |

---

### Criticality-Based Selection Table

| Level | S-003 Status | Note |
|-------|-------------|------|
| C1 Routine | OPTIONAL | S-010 only required; S-003 may strengthen before optional S-014 |
| C2 Standard | OPTIONAL (effectively required) | H-16 mandates S-003 before S-002 which IS required at C2 |
| C3 Significant | OPTIONAL (effectively required) | H-16 mandates S-003 before S-004/S-001 |
| C4 Critical | REQUIRED | All 10 strategies; S-003 is mandatory first step |

**Source:** quality-enforcement.md Criticality Levels table (SSOT). Values MUST match exactly.

**H-16 Interaction:** At C2/C3, S-003 is "optional" per the SSOT criticality table, but H-16 requires Steelman before critique. Since critique strategies ARE required at C2+, S-003 is effectively required whenever they execute.

---

### Cross-References

**SSOT:** `.context/rules/quality-enforcement.md` (H-13 threshold, H-16, dimension weights, criticality levels, strategy catalog) | `ADR-EPIC002-001` (strategy selection, score 4.30) | `ADR-EPIC002-002` (enforcement architecture) | `.context/templates/adversarial/TEMPLATE-FORMAT.md` v1.1.0

**Strategy Templates:** `s-002-devils-advocate.md`, `s-004-pre-mortem.md`, `s-001-red-team.md` (downstream H-16 consumers) | `s-014-llm-as-judge.md` (scores reconstruction) | `s-007-constitutional-ai.md` (constitutional review) | `s-010-self-refine.md` (may precede S-003)

**HARD Rules:** H-13 (threshold >= 0.92), H-14 (creator-critic cycle), H-15 (self-review), H-16 (Steelman before critique), H-17 (scoring required) -- all from quality-enforcement.md

**Academic:** Davidson (1973) Principle of Charity | Wilson (1959) original formulation | Chappell (2012) Steelmanning | Galef (2021) Scout Mindset

---

<!-- VALIDATION: 8 sections present | H-23/H-24 nav | SM-NNN prefix | H-16 documented | SSOT weights match | REVISE band noted | Constructive orientation | C2+ example with Critical finding | No absolute paths | 4-band rubric -->

---

*Template Version: 1.0.0*
*Format Conformance: TEMPLATE-FORMAT.md v1.1.0*
*SSOT: `.context/rules/quality-enforcement.md`*
*Created: 2026-02-15*
*Enabler: EN-807*
