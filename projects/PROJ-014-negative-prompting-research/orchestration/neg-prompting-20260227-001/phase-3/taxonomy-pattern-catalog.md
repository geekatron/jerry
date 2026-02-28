# Negative Prompting Taxonomy and Pattern Catalog

> ps-synthesizer | TASK-008 | Phase 3 | PROJ-014 | 2026-02-28
> Input sources: barrier-1/synthesis.md (R4, 0.953 PASS), barrier-1/supplemental-vendor-evidence.md (R4, 0.951 PASS), barrier-2/synthesis.md (v3.0.0, 0.953 max-iter PASS), phase-2/claim-validation.md (R4, 0.959 PASS), phase-2/comparative-effectiveness.md (R5, 0.933 max-iter)
> Methodology: Deductive framework extension of 12-level effectiveness hierarchy (AGREE-5); IG-002 taxonomy integration; pattern catalog construction
> Quality threshold: >= 0.95 (C4, orchestration directive)
> Version: 3.0.0 (I3 — addresses I2 adversary findings; targeted fixes for Actionability, Internal Consistency, and Traceability gaps)

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | Taxonomy overview, key statistics, evidence coverage |
| [Origin and Scope Disclosure](#origin-and-scope-disclosure) | MANDATORY: epistemological status of this taxonomy |
| [Methodology Subsection](#methodology-subsection) | Deductive framework extension method; what was and was not applied |
| [L1: Full Taxonomy with Pattern Catalog](#l1-full-taxonomy-with-pattern-catalog) | Classification dimensions and all pattern entries |
| [Taxonomy Classification Dimensions](#taxonomy-classification-dimensions) | By technique type, evidence tier, applicability domain |
| [IG-002 Taxonomy Integration](#ig-002-taxonomy-integration) | Four-type vendor taxonomy from supplemental evidence |
| [Pattern Catalog Entries](#pattern-catalog-entries) | NPT-001 through NPT-014: full pattern specifications |
| [L2: Detailed Evidence Tables and Matrices](#l2-detailed-evidence-tables-and-matrices) | Cross-reference, condition alignment, gap analysis |
| [C1-C7 Condition Alignment Matrix](#c1-c7-condition-alignment-matrix) | Pilot conditions mapped to taxonomy patterns |
| [Evidence Gap Map](#evidence-gap-map) | T1/T4/Untested distribution across catalog |
| [Downstream Reference Index](#downstream-reference-index) | Phase 4 lookup table: pattern IDs for Jerry Framework |
| [Practitioner Guidance Summary](#practitioner-guidance-summary) | PG-001 through PG-005 with mandatory confidence labels |
| [PS Integration](#ps-integration) | Worktracker linkage, key findings, downstream agent hints |
| [Self-Review Checklist](#self-review-checklist) | H-15 compliance |
| [Revision Log](#revision-log) | I1 adversary findings addressed in this revision |

---

## L0: Executive Summary

### Taxonomy at a Glance

**NEVER use this taxonomy to imply a directional verdict.** Taxonomy items state evidence strength, not outcome superiority. Whether structured negative framing outperforms structurally equivalent positive framing at ranks 9–11 is UNTESTED (Phase 2 experimental target per barrier-2/synthesis.md ST-5).

**Synthesizer confidence: 0.87** (set below HIGH because the 12-level hierarchy is an internally generated synthesis narrative, AGREE-5, not an externally validated framework — see Origin and Scope Disclosure for full explanation).

This taxonomy extends the 12-level effectiveness hierarchy from barrier-1/synthesis.md AGREE-5 into a formal classification system with 14 named patterns (13 distinct techniques — NPT-007 and NPT-014 are dual entries for the same Type 1 blunt prohibition technique; NPT-007 is the main entry, NPT-014 is the anti-pattern reference entry) across 3 classification dimensions providing independent analytical perspectives. It integrates the IG-002 four-type vendor taxonomy from supplemental-vendor-evidence.md and maps every pattern to the 7 experimental conditions (C1–C7) from TASK-005.

**Key statistics:**
- Total patterns cataloged: **14** (NPT-001 through NPT-014) — representing **13 distinct techniques** (NPT-007/NPT-014 are dual entries for the same Type 1 blunt prohibition; see Pattern Catalog preamble for design rationale)
- Evidence tier distribution: **5 patterns with T1 controlled evidence** (NPT-001, NPT-004, NPT-005, NPT-006, NPT-007 — note: NPT-001 and NPT-004 are out of scope for prompt engineering; NPT-005's T1 evidence is scoped to negation accuracy only; NPT-007's T1 evidence establishes underperformance); **5 patterns with T4 observational only** (NPT-009, NPT-010, NPT-011, NPT-012, NPT-013); **4 patterns with T3 or no controlled evidence** (NPT-002, NPT-003, NPT-008, NPT-014)
- For PROMPT-ENGINEERING-ACCESSIBLE patterns only: **2 with T1 evidence at prompt level** (NPT-005: negation accuracy; NPT-006: compliance); **1 with T1 evidence establishing underperformance as baseline** (NPT-007/NPT-014); **5 with T4 observational only** (NPT-009 through NPT-013)
- Hierarchy coverage: Ranks 1–12 fully cataloged; **rank 7 is unoccupied** (see note below); ranks 1–4 marked out-of-scope for prompt engineering
- Prompt-engineering-accessible patterns: **10** (ranks 5–12 + architectural patterns NPT-010 through NPT-013)
- C1–C7 pilot condition coverage: All 7 conditions mapped; no orphaned patterns

**Rank 7 gap note:** The 12-level hierarchy assigns ranks 1–12 but no technique currently warrants rank 7. Rank 7 would represent a technique more effective than NPT-008 (rank 8: contrastive example pairing, T3 evidence) but less effective than NPT-006 (rank 6: atomic constraint decomposition, T1 evidence). No technique in the evidence base meets this profile without either reordering existing ranks (which would alter the C1–C7 pilot condition alignment) or introducing a rank that lacks distinguishing evidence. The gap reflects honest evidence coverage, not a cataloging error.

**Origin disclosure:** The 12-level hierarchy is an internally generated narrative synthesis product (AGREE-5, barrier-1/synthesis.md, R4, 0.953 PASS, 2026-02-27). It passed an internal adversary gate (0.953) but has NOT been validated by independent researchers or a controlled ranking study. This taxonomy inherits that limitation. All patterns at ranks 9–11 have only T4 observational evidence; their ordering within the taxonomy reflects synthesizer judgment, not controlled comparison.

**Primary insight for Phase 4 (Jerry Framework Application):** The pattern catalog provides 14 named, evidence-tagged patterns that Phase 4 can reference directly by NPT-ID when analyzing skills, agents, rules, patterns, and templates. Patterns NPT-009 through NPT-013 (T4-observed, ranks 9–11) are the most relevant to the Jerry Framework's existing enforcement architecture. Patterns NPT-006 and NPT-007 (T1-evidenced, ranks 5–6) provide the highest-quality evidence base for any framework changes.

---

## Origin and Scope Disclosure

### MANDATORY READING BEFORE CONSUMING THIS TAXONOMY

**[ORIGIN — REQUIRED DISCLOSURE PER ST-5 CONSTRAINT 1]**

The foundational 12-level effectiveness hierarchy that scaffolds this taxonomy is a narrative synthesis product generated by the PROJ-014 research pipeline in barrier-1/synthesis.md AGREE-5. It was produced by the ps-synthesizer agent, passed an internal adversary gate (R4, 0.953 PASS, 2026-02-27), and has been used as the analytical backbone in Phase 2 analyses. It has NOT been:
- Reviewed by independent prompting researchers outside this research pipeline
- Validated by a controlled ranking study comparing techniques head-to-head
- Assessed against any external taxonomy framework

**What this means for downstream consumers:**

NEVER treat the ordinal positions within ranks 5–12 as empirically established differences. The ordering reflects synthesizer judgment from 75 sources, not direct comparison evidence. Specifically:
- **Ranks 9–11 ordering (declarative > paired > justified)** is based on observed vendor practice frequency, not controlled evidence. Phase 2 must treat these three ranks as requiring experimental comparison.
- **Ranks 5–6 ordering** is based on evidence tier (both T1) and magnitude signal (A-23's +25.14% on negation reasoning vs. A-15's +7–8% compliance). This ordering is better supported but still reflects analyst judgment.
- **Rank 12 (blunt prohibition) as lowest-performing** is the only position with multi-source T1 evidence (A-20, AAAI 2026; A-15, EMNLP 2024; A-31, arXiv) establishing it as underperforming structured alternatives.

**[PROSPECTIVE VALIDITY NOTE — DA-001 RESOLUTION]**

The 12-level hierarchy is used as experimental scaffolding for the C1–C7 pilot design. A question with operational implications: what would change in the C1–C7 mapping if ranks 5–11 were reordered after external validation?

- **If ranks 9–11 reorder (e.g., justified > paired > declarative):** C5 and C4 would swap priority in the pilot design. The TASK-005 pilot comparison C2 vs. C3 (NPT-014 vs. NPT-009) would remain unaffected, but secondary comparisons (C4 vs. C5) would have reversed expected ordering.
- **If rank 6 (NPT-006, atomic decomposition) drops below rank 9:** The T1 evidence base would apply to a lower-ranked pattern, potentially implying that structured negative constraints (rank 9, T4) have a weaker foundation than the hierarchy suggests.
- **If external validation introduces a rank 7 occupant:** A new condition (C8) would be needed in the pilot design, or C3–C5 would need to be re-mapped.

NEVER treat the C1–C7 condition assignments as immutable prior to external validation of the hierarchy. If Phase 5 or a subsequent research phase produces an externally validated ordering that differs from the current synthesis-internal hierarchy, the C1–C7 mapping MUST be reassessed before Phase 5 pilot execution. The current mapping is provisional pending external validation.

**[CONSTRAINT INHERITANCE FROM BARRIER-2/SYNTHESIS.MD ST-5]**

This taxonomy adheres to all four Phase 3 constraints:

1. NEVER treated the 12-level hierarchy as empirically validated (stated above and repeated in every affected pattern entry).
2. NEVER collapsed the distinction between rank 12 (blunt prohibition, evidence-weak) and ranks 9–11 (structured vendor practice, T4 only). Each has separate catalog entries with distinct evidence labels.
3. NEVER implied a directional verdict not established by Phase 2. All pattern entries state evidence strength; none claim negative framing outperforms positive framing at ranks 9–11.
4. The hierarchy ordering is NOT modified in this document. The C1–C7 pilot condition alignment from TASK-005 is preserved in full. See [C1–C7 Condition Alignment Matrix](#c1-c7-condition-alignment-matrix).

---

## Methodology Subsection

**NEVER cite "Braun & Clarke (2006) thematic analysis" as the primary methodology for this taxonomy.** The actual method applied is deductive framework extension, not inductive thematic analysis.

### Method Applied: Deductive Framework Extension

This taxonomy was constructed using a deductive framework extension approach:

1. **Starting framework:** The 12-level effectiveness hierarchy (AGREE-5, barrier-1/synthesis.md) was accepted as the pre-existing analytical backbone. It was NOT derived inductively from the source documents in this synthesis step.
2. **Deductive pattern assignment:** Each pattern entry was assigned to hierarchy ranks, IG-002 types, and evidence tiers by applying the pre-existing framework definitions to the source documents — a deductive operation, not an inductive coding process.
3. **Gap identification:** Rank 7 vacancy, T2 tier emptiness, and NPT-007/NPT-014 dual-entry structure were identified by applying the pre-existing hierarchy to the evidence inventory, not by emergent theme discovery.
4. **No inductive thematic coding was performed.** The themes in the PS Integration section reflect the deductive categories (evidence tier stratification, technique type distinctions) established in prior research phases, not emergent themes discovered through open coding.

### What Braun & Clarke (2006) Was NOT Applied To

Braun & Clarke's six-phase thematic analysis methodology (familiarization, coding, searching for themes, reviewing themes, defining themes, writing) was referenced in the frontmatter of the v1.0.0 taxonomy as a methodological label. That reference was inaccurate. This document's frontmatter now correctly labels the method as "Deductive framework extension." The upstream synthesis documents (barrier-1/synthesis.md, barrier-2/synthesis.md) may have applied inductive thematic analysis in their respective synthesis phases; this Phase 3 taxonomy extends those outputs deductively.

### Source Inputs and Their Role

| Source | Role in This Taxonomy |
|--------|----------------------|
| barrier-1/synthesis.md (R4, 0.953 PASS) | Provides AGREE-5 (12-level hierarchy) — the deductive framework scaffold |
| barrier-1/supplemental-vendor-evidence.md (R4, 0.951 PASS) | Provides IG-002 taxonomy, VS-001–VS-004 (T4 observational evidence for NPT-009 through NPT-013) |
| barrier-2/synthesis.md (v3.0.0, 0.953 max-iter PASS) | Provides PG-001 through PG-005 practitioner guidance; ST-5 Phase 3 constraints |
| phase-2/claim-validation.md (R4, 0.959 PASS) | Provides A-23 venue confirmation (I5); SR-003-i2 resolution; confidence reconciliation |
| phase-2/comparative-effectiveness.md (R5, 0.933 max-iter) | Provides C1–C7 condition definitions (TASK-005); AGREE-8/AGREE-9 cross-survey agreement data |

---

## L1: Full Taxonomy with Pattern Catalog

### Taxonomy Classification Dimensions

The taxonomy organizes all 14 negative prompting patterns across three classification dimensions providing independent analytical perspectives. Any pattern can be located by any combination of these three dimensions. Note that the dimensions are NOT orthogonal in the strict statistical sense — certain combinations are structurally impossible (e.g., a pattern cannot simultaneously be A1 Prohibition-only and A4 Enforcement-tier; it cannot be both T1 and Untested for the same construct). The dimensions are analytical lenses, each providing a distinct perspective, but not every combination of dimension values is populated.

**Structurally impossible combinations (examples):**
- A1 (Prohibition-only) cannot co-occur with A4 (Enforcement-tier prohibition) — A4 requires a multi-tier architecture that A1 explicitly lacks
- T1 evidence and "Untested" cannot apply to the same construct simultaneously — they can co-exist for different constructs within one pattern (e.g., NPT-005 is T1 for negation accuracy but Untested for hallucination rate)
- A6 (Training-time constraint) cannot be prompt-accessible — patterns in A6 are definitionally out-of-scope for prompt engineering

#### Dimension A: Technique Type

| Type | Description | Patterns |
|------|-------------|----------|
| **A1: Prohibition-only** | Standalone negative instruction without context, pairing, or re-injection | NPT-014 |
| **A2: Structured prohibition** | Negative instruction with specificity, consequence documentation, or atomic decomposition | NPT-006, NPT-007, NPT-009, NPT-010 |
| **A3: Augmented prohibition** | Prohibition paired with positive alternative, contextual justification, or meta-level framing | NPT-008, NPT-011, NPT-012 |
| **A4: Enforcement-tier prohibition** | Prohibition operating within a multi-tier enforcement architecture with re-injection or constitutional framing | NPT-010, NPT-012, NPT-013 |
| **A5: Programmatic enforcement** | Machine-enforced constraint not dependent on natural-language compliance | NPT-003, NPT-004 |
| **A6: Training-time constraint** | Constraints built into model weights during training, not prompt-time | NPT-001, NPT-002 |
| **A7: Meta-prompting** | Warning- or persona-based prompts that prime negation-handling at meta-level | NPT-005, NPT-006 |

**Note on multi-type assignments:** NPT-010 appears in both A3 (Augmented prohibition — positive pairing) and A4 (Enforcement-tier — tier vocabulary). NPT-012 appears in both A3 (augmented via re-injection) and A4 (enforcement-tier). These multi-type assignments reflect that some patterns operate at multiple structural levels simultaneously. The Dimension A table is a classification aid, not a strictly partitioned taxonomy. NEVER use Dimension A type assignments alone to exclude patterns from consideration.

#### Dimension B: Evidence Tier

| Tier | Label | Description | Patterns in this tier |
|------|-------|-------------|----------------------|
| **T1** | Peer-reviewed | Published in peer-reviewed venues (EMNLP, AAAI, ACL, ICLR, IJCAI) | NPT-006 (A-23), NPT-007 (A-15, A-20) |
| **T3** | Preprint / unreviewed | arXiv preprints; large-scale but unreviewed | NPT-005, NPT-008 (partial), NPT-014 (partial) |
| **T4** | Practitioner observation | Vendor self-practice documentation; directly observable production systems | NPT-009, NPT-010, NPT-011, NPT-012, NPT-013 |
| **T5** | Session observation | Single-session data with uncontrolled confounds | NPT-013 (partial) |
| **Untested** | No controlled comparison | No controlled A/B comparison exists for this pattern's specific claim | NPT-001, NPT-002, NPT-003, NPT-004, NPT-013 (causal) |

**T2 tier note:** T2 (established practitioner — published vendor documentation from major AI providers) was defined as a tier category. In this taxonomy, material that might qualify as T2 has been absorbed into T4 (practitioner observation) because the vendor documentation examined (Claude Code rule files, OpenAI system prompt design docs, LlamaIndex documentation) functions as direct observation evidence rather than as prescriptive methodology published for external consumption. No patterns are assigned T2 in this taxonomy. The tier label is retained in the tier vocabulary for completeness but is empty in this catalog.

**NEVER conflate T4 (HIGH observational confidence) with T1 (causal confidence). The distinction maps directly to barrier-2/synthesis.md ST-2 confidence reconciliation.**

#### Dimension C: Applicability Domain

| Domain | Description | Best-fit patterns |
|--------|-------------|------------------|
| **C-Research** | Research synthesis, source-citation tasks, fact-verification | NPT-009, NPT-011, NPT-012 |
| **C-Code** | Code generation, code review, programming constraints | NPT-006, NPT-007, NPT-009 |
| **C-Compliance** | Behavioral compliance, rule-following, constraint adherence | NPT-007, NPT-009, NPT-010, NPT-013 |
| **C-Governance** | Multi-agent governance, orchestration rules, constitutional AI | NPT-010, NPT-012, NPT-013 |
| **C-General** | Task-agnostic; broad applicability | NPT-014 (always underperforms in this domain), NPT-008, NPT-011 |
| **C-MCQA** | Multiple-choice question-answering (specific risk: negation may increase hallucination) | NPT-014 (risk domain) |

---

### IG-002 Taxonomy Integration

**Source:** supplemental-vendor-evidence.md, Finding IG-002 ("The Expertise Confound Makes Published Studies Potentially Unreliable for Evaluating Expert Negative Prompting").

The IG-002 taxonomy identifies four types of negative prompting based on structural complexity and enforcement mechanism. This taxonomy provides the primary organizing principle for understanding why published literature on "negative prompting" may systematically test only Type 1 while practitioner systems rely on Types 2–4.

| IG-002 Type | Name | Description | AGREE-5 Rank | Evidence Status | Hierarchy Pattern ID |
|-------------|------|-------------|--------------|-----------------|---------------------|
| **Type 1** | Naive blunt prohibition | Standalone negative instruction without specificity, context, or pairing | Rank 12 | Extensively studied (T1+T3 evidence) | NPT-014 |
| **Type 2** | Structured negative constraint | NEVER/MUST NOT with consequence documentation; specific scope; atomic | Ranks 9–11 | Practitioner observation only (T4) | NPT-009, NPT-010, NPT-011 |
| **Type 3** | L2-re-injected negative constraint | Type 2 with per-prompt re-injection; "immune to context rot" enforcement mechanism | Rank 10 (extended) | Practitioner observation; L2 mechanism mechanically verified | NPT-012, NPT-013 |
| **Type 4** | Constitutional triplet | Minimum three prohibitions expressing the most safety-critical constraints; required per agent schema | Rank 10–11 (extended) | Practitioner observation; mandatory schema compliance in production | NPT-013 |

**Note on "extended" rank designations:** Patterns designated "Rank 10 (extended)" or "Rank 10–11 (extended)" are mechanism extensions of the base rank, not independently positioned new ranks in the 12-level hierarchy. "Extended" indicates the pattern adds a mechanism (re-injection, schema enforcement) to a base rank pattern rather than occupying a distinct hierarchy slot. NEVER interpret "extended" as evidence for a distinct superiority claim beyond the base rank.

**Critical reading note:** The AGREE-4 finding ("prohibition-style negative instructions are unreliable as standalone mechanisms") applies specifically to Type 1. It has NOT been tested for Types 2–4. NEVER extrapolate from AGREE-4 to conclude Types 2–4 are unreliable. This conflation is the primary error that Phase 2 is designed to test against.

**Observable evidence for Types 2–4 (per VS-001–VS-004):** 33 NEVER/MUST NOT/DO NOT instances across 10 Claude Code rule files provide direct T4 observation that Type 2–4 framing is used at scale in production by Anthropic engineers (count sourced from supplemental-vendor-evidence.md VS-001; not independently re-verified within this synthesis). OpenAI (C-6, C-7) and LlamaIndex (C-11) provide corroborating vendor evidence. Concentration is Anthropic-heavy.

---

### Pattern Catalog Entries

**Dual-entry design rationale:** NPT-007 and NPT-014 are two catalog entries for the same underlying technique (Type 1 blunt prohibition). This dual-entry design serves a specific Phase 4 purpose: NPT-007 is the "main" entry documenting the technique as a baseline for comparison across patterns; NPT-014 is the "anti-pattern reference" entry positioning the technique as a diagnostic filter for identifying under-engineered constraints in existing systems. Phase 4 analysts SHOULD cite NPT-007 when comparing techniques and NPT-014 when auditing existing rules for upgrade candidates. NEVER treat the dual-entry as representing two distinct techniques — only 13 distinct techniques are cataloged.

Each pattern entry follows the format: Name, Identifier, Definition, When to Use / When NOT to Use, Example Prompt Fragment, Evidence Base, Known Limitations and Failure Modes, Relationship to Other Patterns.

---

#### NPT-001: Model-Internal Behavioral Intervention

**Pattern ID:** NPT-001
**IG-002 Type:** N/A (pre-training; out of PROJ-014 prompt-engineering scope)
**Hierarchy Rank:** 1
**Technique Type:** A6 (Training-time constraint)
**Evidence Tier:** T1 (ICLR 2025 — CAST, A-28)
**Observational Confidence:** HIGH for technique class
**Causal Confidence:** OUT OF SCOPE for prompt engineering
**C1–C7 Condition:** Not applicable (requires model access)

**Definition:** Constraints built into model behavior through training-time interventions or model-internal mechanisms (e.g., CAST, A-28). The constraint is enforced by model weights rather than by runtime prompt instructions.

**When to use:** When model-level behavioral enforcement is required and training infrastructure is available. Research context only for most practitioners.

**When NOT to use:** NEVER deploy NPT-001 as a substitute for prompt-level constraints in production systems where model access is unavailable. NEVER assume prompt-level negative instructions have the same enforcement reliability as training-time constraints.

**Example:** CAST (Contrastive Activation Steering Training) — behavioral steering through contrast pairs in model activations (A-28, ICLR 2025). Not expressible as a prompt fragment.

**Evidence Base:**
- A-28 (ICLR 2025, T1): Model-internal activation steering demonstrates reliable constraint behavior in controlled conditions.

**Known Limitations:**
- Requires model training infrastructure — inaccessible to 99%+ of practitioners
- Model updates may invalidate constraint encoding
- No published evidence on interaction with prompt-level negative constraints

**Relationship to Other Patterns:**
- Complementary to NPT-009 through NPT-013 (enforcement can stack)
- NEVER treat NPT-001 as functionally equivalent to NPT-014 or any prompt-level pattern

---

#### NPT-002: Training-Time Constitutional Constraint

**Pattern ID:** NPT-002
**IG-002 Type:** N/A (training access required)
**Hierarchy Rank:** 2
**Technique Type:** A6 (Training-time constraint)
**Evidence Tier:** T3 (arXiv preprint — Constitutional AI, A-10)
**Observational Confidence:** LOW (T3 only; no peer-reviewed replication)
**Causal Confidence:** LOW
**C1–C7 Condition:** Not applicable (requires training access)

**Definition:** Negative constraint principles embedded at training time through Constitutional AI (CAI) or equivalent methodologies (A-10, Anthropic). The model is trained to critique and revise its own outputs against a constitution of prohibitions.

**When to use:** Training infrastructure context; research on value alignment and safety.

**When NOT to use:** NEVER substitute training-time constitutional AI for inference-time enforcement in production systems. NEVER claim CAI-trained models honor prompt-level prohibitions with the same reliability as their trained constitutional constraints.

**Example:** Constitutional AI training: "A helpful, harmless, and honest assistant. Never produce harmful content. Never deceive users." (Baked into model weights via RL fine-tuning, not a prompt instruction.)

**Evidence Base:**
- A-10 (arXiv, T3): Anthropic's Constitutional AI methodology; unreviewed preprint; major conceptual paper not yet peer-reviewed in this context.

**Known Limitations:**
- T3 evidence only; construct validity not independently assessed
- Inference-time prompt overrides may conflict with constitutional training
- Training costs prohibitive for most practitioners

**Relationship to Other Patterns:**
- Conceptual ancestor of NPT-013 (Constitutional Triplet), which applies the prohibition concept at inference-time
- Prerequisite understanding for interpreting vendor self-practice (VS-001–VS-004)

---

#### NPT-003: Programmatic Constraint Enforcement

**Pattern ID:** NPT-003
**IG-002 Type:** N/A (infrastructure-level; distinct from prompt framing)
**Hierarchy Rank:** 3
**Technique Type:** A5 (Programmatic enforcement)
**Evidence Tier:** T3 (DSPy assertions, C-13/I-21) + T4 (NeMo Guardrails, I-27)
**Observational Confidence:** MEDIUM (T3+T4 convergent; infrastructure-validated)
**Causal Confidence:** MEDIUM for enforcement mechanism; UNTESTED for prompt framing comparison
**C1–C7 Condition:** Not directly testable in C1–C7 prompt conditions (infrastructure-level)

**Definition:** Machine-enforced constraints that trigger automatic retry, backtracking, or rejection when LLM output violates specified conditions. Examples: DSPy dspy.Assert (backtracking on violation), NeMo Guardrails (output filtering pipeline). The constraint is not expressed as natural language; it operates on outputs, not on prompts.

**When to use:** NEVER use programmatic enforcement as the only safety mechanism without accompanying prompt-level constraints. Use when output reliability is safety-critical and human review is insufficient.

**When NOT to use:** NEVER treat programmatic enforcement as a replacement for prompt-level constraint specification. NEVER omit NPT-009 or NPT-010 in systems using NPT-003 — the prompt constraint sets expectation; programmatic enforcement catches violations. NEVER conflate DSPy's backtracking mechanism with prompt-level L2 re-injection (different enforcement points, different mechanisms — see SR-003-i2 resolution in claim-validation.md).

**Example:**
```python
# DSPy programmatic enforcement (not a prompt fragment):
dspy.Assert(
    len(response.citations) >= 1,
    "Every factual claim must have at least one citation."
)
```

**Evidence Base:**
- C-13/I-21 (DSPy, T3): Programmatic backtracking enforces constraints more reliably than pure natural-language instruction.
- I-27 (NeMo Guardrails, T4): Production deployment evidence; constraint enforcement pipeline.
- PG-005 (barrier-2/synthesis.md ST-4): "Prioritize enforcement architecture over framing vocabulary optimization" — T3+T4, unconditional investment allocation.

**Known Limitations:**
- Requires engineering infrastructure; not available to all practitioners
- DSPy mechanism is infrastructure-level (compile-time); cannot be compared directly to inference-time prompt framing (different enforcement points)
- T3 evidence base for effectiveness; not peer-reviewed in controlled comparison

**Relationship to Other Patterns:**
- PREFER over NPT-014 in any context where infrastructure is available
- Complementary to NPT-009 through NPT-013 (prompt constraints provide expectation-setting; programmatic enforcement catches violations)
- PREREQUISITE to NPT-003 before relying on prompt-only constraints (NPT-009–NPT-014) for safety-critical compliance

---

#### NPT-004: Verification Pipeline Constraint

**Pattern ID:** NPT-004
**IG-002 Type:** N/A (pipeline-level; orthogonal to prompt framing)
**Hierarchy Rank:** 4
**Technique Type:** A5 (Programmatic enforcement)
**Evidence Tier:** T1 (Chain-of-Verification, CoVe — A-22, ACL 2024)
**Observational Confidence:** HIGH for verification pipeline effectiveness; orthogonal to framing question
**Causal Confidence:** HIGH for hallucination reduction via verification; OUT OF SCOPE for prompt framing comparison
**C1–C7 Condition:** Not directly testable in prompt-framing conditions

**Definition:** Post-generation verification pipelines that check LLM output against factual claims or specified constraints (Chain-of-Verification methodology, A-22, ACL 2024). The pipeline re-prompts the model to verify its own claims, generating a second pass that catches violations.

**When to use:** When hallucination prevention on verifiable facts is the primary concern and pipeline overhead is acceptable.

**When NOT to use:** NEVER use NPT-004 alone without prompt-level constraint specification. NEVER treat verification pipeline pass rates as equivalent to first-pass constraint adherence — they measure different things.

**Example:**
```
[Verification pass]: Review each factual claim in your response. For each claim:
1. State the source you used to establish this claim.
2. If no source exists, mark the claim as unverified.
3. Do not include any claim marked as unverified.
```

**Evidence Base:**
- A-22 (ACL 2024, T1): Chain-of-Verification reduces hallucination in factual generation tasks.

**Known Limitations:**
- Pipeline overhead (requires additional inference calls)
- Orthogonal to the negative vs. positive framing question — NPT-004 operates on outputs, not prompt framing
- Does not address behavioral constraint violations that are not fact-checkable

**Relationship to Other Patterns:**
- Complementary to all prompt-level patterns (NPT-005–NPT-014)
- Does NOT substitute for prompt-level constraint design

---

#### NPT-005: Warning-Based Meta-Prompt

**Pattern ID:** NPT-005
**IG-002 Type:** Type 2 (Structured negative constraint — meta-level variant)
**Hierarchy Rank:** 5
**Technique Type:** A7 (Meta-prompting)
**Evidence Tier:** T1 (A-23, EMNLP 2025 Findings — confirmed, ACL Anthology 2025.findings-emnlp.761)
**Observational Confidence:** MEDIUM — ONE T1 study, no replication
**Causal Confidence:** MEDIUM for negation accuracy construct only — SCOPE CONSTRAINT: A-23 measures negation reasoning accuracy (+25.14%), NOT hallucination rate reduction. NEVER conflate these.
**C1–C7 Condition:** Maps to C3 (Structured negative constraint) and C5 (Justified negative constraint)

**T1 Scope (FM-001 addition):** A-23's T1 evidence covers the construct "negation reasoning accuracy" — whether a model correctly applies "not X" instructions in distractor negation tasks. This T1 evidence does NOT cover: hallucination rate, behavioral compliance, or constraint adherence in agentic settings.

**Definition:** Warning-based prompts that prime the model for negation-handling at a meta-level, improving the model's ability to correctly reason about and apply "not X" instructions. Improves negation comprehension rather than directly enforcing a specific behavioral constraint.

**When to use:** When tasks require the model to correctly interpret and honor negation instructions (e.g., "do NOT include X" in generation tasks). When negation comprehension failure is the observed failure mode.

**When NOT to use:** NEVER use NPT-005 as a standalone hallucination-reduction mechanism — A-23 tests negation reasoning accuracy, not hallucination rate. NEVER cite A-23's +25.14% figure as evidence for hallucination reduction; it measures a different construct. NEVER omit the EMNLP 2025 Findings scope caveat when citing this pattern.

**Example Prompt Fragment:**
```
IMPORTANT: This task requires precise negation handling.
When you encounter an instruction containing "NOT", "NEVER", "DO NOT", or "MUST NOT",
treat the negation as an absolute constraint, not as a soft preference.
Failure to honor negation constraints will result in output rejection.
```

**Evidence Base:**
- A-23 (Barreto & Jana, EMNLP 2025 Findings, T1, confirmed in comparative-effectiveness.md I5): Warning-based and persona-based prompts improve negation reasoning accuracy on distractor negation tasks (+25.14%). Venue confirmed via ACL Anthology 2025.findings-emnlp.761; verification provenance: internal pipeline confirmation (comparative-effectiveness.md I5, R5 0.933 max-iter PASS) — external venue verification not re-performed within this synthesis.
- Note: This evidence is scoped to negation accuracy (does the model correctly handle "not X" instructions?) not to hallucination rate (does the model fabricate facts?) — two distinct constructs.

**Known Limitations:**
- Single T1 study; no independent replication
- Scope limited to negation reasoning accuracy — does not directly address hallucination rate
- Negation accuracy is necessary but not sufficient for behavioral constraint adherence
- Task and model specificity not fully characterized

**Relationship to Other Patterns:**
- Prerequisite to NPT-009 through NPT-013 for tasks where negation comprehension is a risk factor
- Complementary to NPT-006 (atomic decomposition)
- Do not substitute for NPT-009 through NPT-013; meta-level priming alone does not enforce specific domain constraints

---

#### NPT-006: Atomic Constraint Decomposition

**Pattern ID:** NPT-006
**IG-002 Type:** Type 2 (Structured negative constraint — decomposed form)
**Hierarchy Rank:** 6
**Technique Type:** A2 (Structured prohibition)
**Evidence Tier:** T1 (A-15, EMNLP 2024 — DeCRIM; confirmed)
**Observational Confidence:** MEDIUM — ONE T1 study, no replication
**Causal Confidence:** MEDIUM for compliance rate construct only — SCOPE: compliance rate (+7.3–8.0% on two benchmarks), NOT hallucination rate.
**C1–C7 Condition:** Maps to C3 (Structured negative constraint) and C6 (Hierarchical negative — HARD/MEDIUM/SOFT)

**T1 Scope (FM-001 addition):** A-15's T1 evidence covers the construct "constraint compliance rate" — whether a model follows explicit instruction components. This T1 evidence does NOT cover: hallucination reduction, long-context constraint persistence, or multi-agent setting compliance.

**Definition:** Negative constraints decomposed into atomic, non-overlapping sub-constraints, each addressing exactly one behavioral prohibition. The DeCRIM methodology (A-15, EMNLP 2024) demonstrates that constraint decomposition improves compliance rates compared to compound prohibitions.

**When to use:** When behavioral compliance is the primary concern and compound prohibitions are failing. When a single behavioral requirement involves multiple distinct failure modes that need separate constraint targeting.

**When NOT to use:** NEVER use NPT-006 without validating that each atomic sub-constraint is testable and measurable. NEVER conflate compliance rate improvement with hallucination rate reduction — A-15 measures compliance, not factual accuracy.

**Context compaction risk note:** The "Low" context compaction risk rating assigned to NPT-006 in the Cross-Reference Matrix requires explanation. NPT-006's decomposed sub-constraints are individually shorter and more targeted than compound prohibitions. The risk hypothesis is that shorter, specific sub-constraints may be better preserved during context compaction than longer compound instructions. However, this is a design hypothesis, not empirically verified. NEVER treat the "Low" rating as established — it reflects a structural inference from decomposition design properties, pending empirical validation per T-004 failure mode analysis.

**Example Prompt Fragment:**
```
This task has THREE separate constraints. NEVER violate any of them:

CONSTRAINT 1: NEVER include code examples in prose sections.
CONSTRAINT 2: NEVER cite sources without providing the full URL.
CONSTRAINT 3: NEVER provide recommendations without citing supporting evidence.

Each constraint is independent. Violation of Constraint 1 does not exempt you from Constraints 2 and 3.
```

**Evidence Base:**
- A-15 (DeCRIM, EMNLP 2024, T1): Atomic decomposition of behavioral constraints improves compliance rate +7.3–8.0% on two benchmarks vs. compound instruction phrasing.
- Consistent with NP-004 pattern (context7-survey: structural constraint over linguistic constraint).

**Known Limitations:**
- Single T1 study; no independent replication
- Scope: compliance rate, not hallucination rate
- Decomposition requires upfront constraint engineering work
- Overly granular decomposition may create competing constraints
- Context compaction risk rating ("Low") is a structural inference, not empirically established

**Relationship to Other Patterns:**
- Complementary to NPT-005 (meta-prompt priming before atomic constraints)
- Complementary to NPT-011 (add consequence documentation to each atomic sub-constraint)
- Basis for NPT-009 and NPT-010 (structured/justified prohibition builds on atomicity principle)

---

#### NPT-007: Blunt-Prohibition Baseline Acknowledgment

**Pattern ID:** NPT-007
**IG-002 Type:** Type 1 (Naive blunt prohibition) — REFERENCE ENTRY: This is the baseline that all other patterns are compared against.
**Hierarchy Rank:** 12 (lowest position — worst-performing)
**Technique Type:** A1 (Prohibition-only)
**Evidence Tier:** T1 (A-20, AAAI 2026; A-15, EMNLP 2024) + T3 (A-31, A-19)
**Observational Confidence:** HIGH — Multiple independent T1+T3 sources establish this as underperforming structured alternatives. This is the single finding with the strongest evidence basis in the entire taxonomy.
**Causal Confidence:** HIGH (for the specific claim that standalone blunt prohibition underperforms structured alternatives on the studied tasks and models)
**C1–C7 Condition:** Maps to C2 (Blunt negative prohibition)

**T1 Scope (FM-001 addition):** A-20's T1 evidence covers instruction hierarchy failure in task-following settings. A-15's T1 evidence covers constraint compliance rate. Both establish underperformance relative to structured instructions but do NOT cover: long-context settings, multi-agent orchestration, or the specific prohibition vocabulary (NEVER vs. Don't) as an isolated variable.

**Definition:** Standalone blunt prohibition without specificity, consequence, pairing, or context. Examples: "Don't hallucinate," "Never lie," "Don't provide harmful content." This is the most-studied form of negative prompting in published literature. It is placed at rank 12 (lowest performing) because multiple independent T1+T3 sources document that it underperforms structured alternatives.

**CRITICAL: This is NOT the pattern that Anthropic, OpenAI, or LlamaIndex use in their enforcement tiers. Those vendors use Types 2–4 (NPT-009 through NPT-013). NEVER conflate Type 1 with Types 2–4.**

**When to use:** Only as a baseline reference or a component within Type 2–4 patterns. NEVER use standalone in any production enforcement context.

**When NOT to use:** NEVER use NPT-007 as the primary behavioral enforcement mechanism for any safety-critical or compliance-critical constraint. NEVER rely on it as the sole negative instruction. Per PG-001 (barrier-2/synthesis.md ST-4, T1+T3, HIGH, unconditional): NEVER use standalone blunt prohibition.

**Example Prompt Fragment (ANTI-PATTERN — DO NOT USE ALONE):**
```
Don't hallucinate.
Never lie.
Don't add information not in the source.
```

**Evidence Base:**
- A-20 (AAAI 2026, T1): Instruction hierarchy failure — prohibition-style instructions fail at baseline rates; blunt prohibitions are among the least reliable constraint forms.
- A-15 (DeCRIM, EMNLP 2024, T1): GPT-4 fails >21% of constraints with standard instruction; blunt prohibition baseline is worse.
- A-31 (Bsharat et al., arXiv, T3): Affirmative directives outperform blunt prohibition by 55% improvement signal on GPT-4 (scope: reasoning tasks).
- A-19 (arXiv, T3, large-scale): Corroborating evidence for prohibition unreliability.

**Known Limitations:**
- The AGREE-4 finding (prohibition unreliable) applies specifically to Type 1 standalone blunt prohibition.
- Expert user moderating variable (IN-001-R3 from synthesis.md): Expert prompt engineers may achieve better results than non-expert users who were subjects of the cited studies.
- Context compaction failure mode (T-004, GAP-13): NEVER rules may be particularly vulnerable to being dropped during context compaction in long-context sessions.

**Relationship to Other Patterns:**
- The baseline against which all other patterns are measured
- Prerequisite understanding: ALWAYS replace or augment NPT-007 with NPT-009 through NPT-013 for any enforcement-tier use
- NEVER use as a standalone; ALWAYS pair with at minimum NPT-011 (consequence documentation) to become NPT-009

---

#### NPT-008: Contrastive Example Pairing

**Pattern ID:** NPT-008
**IG-002 Type:** Type 2 (Structured) — contrastive variant
**Hierarchy Rank:** 8
**Technique Type:** A3 (Augmented prohibition — example-based)
**Evidence Tier:** T3 (Contrastive CoT, A-11 — arXiv preprint, unreviewed)
**Observational Confidence:** LOW (T3, unreviewed)
**Causal Confidence:** LOW (T3, unreviewed; no controlled study of compliance improvement via contrastive examples)
**C1–C7 Condition:** Maps to C4 (Paired negative-positive) — partial

**Definition:** Negative constraint expressed through contrast: show an example of the prohibited behavior, then show the correct alternative. The model learns from the contrast rather than from the explicit prohibition statement alone.

**When to use:** When the failure mode is concrete and demonstrable through example. When the model does not correctly interpret abstract prohibitions but responds better to shown examples.

**When NOT to use:** NEVER rely on contrastive examples alone in enforcement-tier contexts — T3 evidence only. NEVER use when the prohibited behavior cannot be safely demonstrated in an example (risk of inadvertent reinforcement).

**Example Prompt Fragment:**
```
INCORRECT (NEVER produce this):
"The study found that X caused Y." [No citation provided]

CORRECT (ALWAYS follow this format):
"The study found that X caused Y (Author, 2024, DOI:xxx)." [Citation immediately after claim]

Apply the CORRECT format to every factual claim in your response.
```

**Evidence Base:**
- A-11 (Contrastive CoT, arXiv, T3): Contrastive examples improve chain-of-thought reasoning with unreviewed T3 evidence. Specific compliance rate improvement not established.

**Known Limitations:**
- T3 only; no peer-reviewed validation
- May inadvertently prime the model for the prohibited behavior if example is vivid
- Limited to cases where concrete examples can safely illustrate the violation

**Relationship to Other Patterns:**
- Complementary to NPT-009 (combine contrastive examples with consequence documentation)
- More concrete than NPT-011 (abstract consequence documentation) but less systematic than NPT-006 (atomic decomposition)

---

#### NPT-009: Declarative Behavioral Negation

**Pattern ID:** NPT-009
**IG-002 Type:** Type 2 (Structured negative constraint)
**Hierarchy Rank:** 9
**Technique Type:** A2 (Structured prohibition)
**Evidence Tier:** T4 (VS-001–VS-004, direct observation of vendor practice; 33 instances documented)
**Observational Confidence:** HIGH — Direct observation that this pattern is used in production; reason for its effectiveness is contested (three competing explanations: audience specificity, genre convention, engineering discovery — per VS-002).
**Causal Confidence:** LOW — Causal comparison against structurally equivalent positive instruction is UNTESTED (Phase 2 experimental target). NEVER cite this pattern as causally superior to positive equivalents.
**C1–C7 Condition:** Maps to C3 (Structured negative constraint) — PRIMARY CONDITION MAPPING

**T1 Scope (FM-001 addition):** No T1 evidence exists for NPT-009 as a combined pattern. A-15's T1 evidence covers the atomicity component (sub-element of NPT-009's specificity requirement) but does NOT constitute T1 evidence for the full NPT-009 pattern including consequence documentation and scope. The matrix label "T4" correctly represents the full pattern's evidence tier.

**Definition:** A specific, scoped prohibition using NEVER/MUST NOT/FORBIDDEN vocabulary, targeting a single concrete behavior, with the consequence of violation documented. NOT a blunt prohibition (NPT-007) — NPT-009 includes specificity (what exactly is prohibited), scope (under what conditions), and consequence (what happens if violated). This is the canonical Type 2 pattern used in Anthropic's production enforcement tier (VS-001–VS-004).

**CRITICAL DISTINCTION from NPT-007:** NPT-007 is "Don't hallucinate." NPT-009 is "NEVER state facts without citing a source. If a factual claim cannot be sourced, mark it as unverified. Constraint violation: output will be rejected by adversary review." The specificity, scope, and consequence documentation make these structurally distinct, even though both use negative vocabulary.

**When to use:** NEVER substitute with NPT-007 in enforcement-tier contexts. Use NPT-009 when behavioral compliance is a critical requirement and the failure mode is specific and documentable.

**When NOT to use:** NEVER use NPT-009 in long-context sessions without validating that the prohibition is not dropped during context compaction (T-004 failure mode, GAP-13). NEVER claim NPT-009 is experimentally validated as superior to a structurally equivalent positive alternative — this is the UNTESTED central comparison (Phase 2 experimental target).

**Example Prompt Fragment:**
```
NEVER state facts without citing a source.

Scope: All factual claims, including statistics, historical dates, and attributed quotes.
Consequence: Output containing unsourced factual claims will be rejected without review.
Exception: Logical inferences from cited premises do not require separate citations.
```

**Evidence Base:**
- VS-001 (T4, direct observation): 33 NEVER/MUST NOT instances in Anthropic Claude Code behavioral rules — all in HARD enforcement tier.
- VS-002 (T4, observation): Anthropic's engineering practice uses negative framing in enforcement tier while recommending positive framing to users. Three competing explanations; none confirmed.
- VS-003 (T4, observation): HARD tier vocabulary explicitly defined as prohibitive.
- A-15 (T1, EMNLP 2024): Atomic decomposition improves compliance +7.3–8.0% — provides partial T1 support for the specificity component of NPT-009 only.

**Known Limitations:**
- T4 observational evidence only for the combined pattern
- Causal mechanism contested: three competing explanations (audience specificity, genre convention, engineering discovery) per VS-002
- Context compaction failure mode (T-004): NEVER rules may be dropped in long-context sessions
- No controlled comparison against a structurally equivalent positive instruction exists (Phase 2 target)
- Vendor evidence is Anthropic-heavy; cross-vendor generalization is preliminary (OpenAI: C-6, C-7; LlamaIndex: C-11)

**Relationship to Other Patterns:**
- UPGRADE from NPT-007 (adds specificity and consequence)
- PREREQUISITE to NPT-010, NPT-011, NPT-012 (each augments NPT-009)
- ALWAYS pair with NPT-011 (consequence documentation) at minimum
- SHOULD pair with NPT-012 (L2 re-injection) in long-context or multi-turn sessions

---

#### NPT-010: Paired Prohibition with Positive Alternative

**Pattern ID:** NPT-010
**IG-002 Type:** Type 2 extended (Structured negative constraint + positive pairing)
**Hierarchy Rank:** 10
**Technique Type:** A3 (Augmented prohibition) and A4 (Enforcement-tier — when deployed in a tier architecture) (See multi-type assignment note in Dimension A Classification table for patterns spanning multiple technique types.)
**Evidence Tier:** T4 (VS-001–VS-004, vendor practice) + T3 (A-11, Contrastive CoT) + AGREE-8 (Moderate, 2-of-3 surveys)
**Observational Confidence:** MEDIUM — AGREE-8 Moderate cross-survey agreement; T3+T4 evidence; no T1 controlled comparison of paired vs. non-paired prohibition
**Causal Confidence:** UNTESTED — No controlled A/B comparison of paired vs. unpaired prohibition or paired negative vs. paired positive framing exists.
**C1–C7 Condition:** Maps to C4 (Paired negative-positive)

**T1 Scope (FM-001 addition):** No T1 evidence exists for NPT-010. AGREE-8 is cross-survey observational agreement, not a controlled study. T3 (A-11) covers contrastive reasoning, not paired prohibitions in behavioral constraint contexts. The absence of T1 evidence is the reason NPT-010's causal confidence is UNTESTED.

**Definition:** A negative constraint paired immediately with a positive alternative instruction that specifies what the model SHOULD do instead of the prohibited behavior. AGREE-8 establishes cross-survey agreement (moderate strength) that this pairing improves negative instruction effectiveness.

**NP-002 Pattern (from context7-survey):** "When negative instructions are used, the most effective pattern pairs the prohibition with a positive alternative." Documented across Anthropic (C-1/I-1), OpenAI GPT-5.1 (C-6), and LlamaIndex (C-11).

**When to use:** NEVER use standalone prohibitions in compliance-critical contexts without pairing with a positive alternative (PG-003: pair enforcement-tier constraints with consequences — T4 observational, MEDIUM working practice). For practitioners already committed to negative framing, NPT-010 represents the minimum structural requirement — the UNTESTED comparison against equivalent positive framing means this guidance cannot be extended to the positive-vs-negative framing choice itself.

**When NOT to use:** NEVER treat NPT-010 as validated over NPT-009-only — no controlled comparison between paired and unpaired prohibition exists at T1. NEVER use when the positive alternative is ambiguous or could be interpreted as permission to do the prohibited thing in the alternative way.

**Example Prompt Fragment:**
```
NEVER provide recommendations without citing supporting evidence.

Instead: Every recommendation must be followed immediately by the citation that supports it,
in the format: "(Author, Year, page N)" or a direct URL.
```

**Evidence Base:**
- AGREE-8 (Moderate, 2-of-3 surveys): Negative framing works best when paired with a positive alternative.
- NP-002 pattern (context7-survey, T4): Documented across Anthropic, OpenAI, LlamaIndex.
- VS-001–VS-004 (T4): Production use of negative constraints generally; pairing not isolated.
- A-11 (T3): Contrastive examples (related mechanism, different form).

**Known Limitations:**
- No T1 controlled comparison of paired vs. unpaired prohibition
- AGREE-8 is Moderate strength (2-of-3 surveys); not all surveys found this pattern
- Positive alternative must be unambiguous — poorly worded alternatives can introduce new failure modes
- Causal status: UNTESTED for comparison against positive-only equivalent

**Relationship to Other Patterns:**
- EXTENSION of NPT-009 (adds positive pairing)
- COMPATIBLE with NPT-011 (add consequence documentation to the pair)
- PREREQUISITE to NPT-012 (re-inject the paired constraint for long contexts)

---

#### NPT-011: Justified Prohibition with Contextual Reason

**Pattern ID:** NPT-011
**IG-002 Type:** Type 2 extended (Structured negative constraint + justification)
**Hierarchy Rank:** 11
**Technique Type:** A3 (Augmented prohibition — justified variant)
**Evidence Tier:** T4 (VS-001–VS-004, vendor practice) + AGREE-9 (Moderate, 2-of-3 surveys) + T1 analogy (A-23's warning mechanism involves meta-level justification)
**Observational Confidence:** MEDIUM — AGREE-9 Moderate cross-survey agreement; T4+T1-analogy evidence
**Causal Confidence:** UNTESTED — No controlled comparison of justified vs. unjustified prohibition exists at T1. NEVER cite AGREE-9 as causal evidence.
**C1–C7 Condition:** Maps to C5 (Justified negative constraint)

**T1 Scope (FM-001 addition):** No T1 evidence exists for NPT-011 as a behavioral constraint justification pattern. A-23's T1 analogy evidence covers warning-based meta-prompting, which involves a related (but distinct) mechanism. AGREE-9 is cross-survey agreement, not a controlled study. The absence of T1 evidence for the justification component specifically is why causal confidence is UNTESTED.

**Definition:** A negative constraint accompanied by an explanation of WHY the constraint exists. AGREE-9 establishes that contextual justification improves negative instruction effectiveness. The justification serves two functions: it primes the model to apply the constraint purposively rather than literally, and it provides context that allows the model to generalize the constraint correctly to edge cases.

**NP-003 Pattern (from context7-survey):** "Negative instructions are more effective when accompanied by an explanation of why the constraint exists." Example: "NEVER use ellipses since the text-to-speech engine will not know how to pronounce them."

**When to use:** NEVER use prohibitions without justification in edge-case-rich domains where the model must generalize the constraint to situations not explicitly listed. Use NPT-011 when the constraint's rationale helps define its scope.

**When NOT to use:** NEVER use justification as a substitute for specificity — NPT-009's specificity is still required. NEVER fabricate a justification if the actual reason is unclear; false justifications may mislead the model about the constraint's intended scope.

**Example Prompt Fragment:**
```
NEVER use abbreviations in technical documentation.

Reason: Abbreviations are inaccessible to readers who are not domain experts
and will be misinterpreted in automated parsing pipelines that strip context.
This constraint applies to all sections including code comments and table headers.
```

**Evidence Base:**
- AGREE-9 (Moderate, 2-of-3 surveys): Contextual justification improves negative instruction effectiveness.
- NP-003 pattern (context7-survey, T4): Documented with examples from vendor documentation.
- A-23 analogy (T1, EMNLP 2025): Warning-based meta-prompts (a form of meta-justification) improve negation accuracy — provides conceptual T1 support for the mechanism, though not a direct test of justification in behavioral constraints.

**Known Limitations:**
- No T1 controlled comparison of justified vs. unjustified prohibition in behavioral constraint contexts
- AGREE-9 is Moderate strength (2-of-3 surveys)
- Justification quality matters — poor justifications may reduce effectiveness
- The A-23 analogy is a mechanism hypothesis, not a direct test (explicitly distinguished per barrier-2/synthesis.md ST-4 PG-003 note)

**Relationship to Other Patterns:**
- EXTENSION of NPT-009 (adds justification)
- BEST COMBINED with NPT-010 (paired negative-positive with justification = most complete prompt-only pattern)
- SHOULD be added to NPT-009 whenever the constraint applies to domains with edge cases

---

#### NPT-012: L2 Re-Injected Negative Constraint

**Pattern ID:** NPT-012
**IG-002 Type:** Type 3 (L2-re-injected negative constraint)
**Hierarchy Rank:** 10 (extended — builds on NPT-009/NPT-010 with re-injection mechanism; does not occupy a distinct rank position from NPT-010's base rank 10)
**Technique Type:** A3 (Augmented prohibition — re-injection augments the base constraint) and A4 (Enforcement-tier prohibition with re-injection) (See multi-type assignment note in Dimension A Classification table for patterns spanning multiple technique types.)
**Evidence Tier:** T4 (VS-001–VS-004 observation; L2-REINJECT mechanism documented in quality-enforcement.md)
**Observational Confidence:** HIGH (mechanism mechanically verified — L2-REINJECT implementation directly observable in quality-enforcement.md and rule files)
**Causal Confidence:** LOW — Re-injection vs. vocabulary contribution not isolated; UNTESTED whether prohibitive vocabulary (vs. positive vocabulary with equivalent re-injection) drives any compliance differential.
**C1–C7 Condition:** Maps to C7 (Full framework — all techniques combined) — the re-injection component is a mechanism, not a framing; test against C4 (paired negative-positive) to isolate re-injection frequency from vocabulary effect

**T1 Scope (FM-001 addition):** No T1 evidence exists for NPT-012. The L2-REINJECT mechanism is mechanically verified (directly observable in the framework) but its effectiveness relative to positive re-injection has never been tested in a controlled study. Mechanical verification of implementation is NOT equivalent to T1 evidence for causal effectiveness.

**Definition:** A Type 2 negative constraint (NPT-009 or NPT-010) deployed with a per-turn re-injection mechanism that reinjects the critical constraints into every prompt interaction. Documented in the Jerry Framework as L2-REINJECT markers — rules tagged for re-injection are loaded at every prompt, making them "immune to context rot" (per quality-enforcement.md enforcement architecture table).

**Mechanistic distinction:** The re-injection is the mechanism; the prohibitive vocabulary is the framing. Phase 2 Condition C4 (C2+re-injection vs. C3 positive+re-injection) is specifically designed to isolate whether the vocabulary contributes to enforcement beyond what re-injection alone provides.

**When to use:** NEVER rely on single-pass prohibition for constraints that must hold across long contexts or multi-turn sessions. Use NPT-012 when context compaction is a risk (long contexts, many tool calls, extended sessions) — T-004 failure mode applies specifically to single-injection prohibitions.

**When NOT to use:** NEVER present re-injection as validated over single-injection — the causal contribution of the prohibitive vocabulary (vs. re-injection alone) is Phase 2 experimental target. NEVER use NPT-012 without the underlying NPT-009 or NPT-010 constraint being well-formed.

**Example Implementation (Framework Pattern):**
```
<!-- L2-REINJECT: rank=1, content="P-003: No recursive subagents. P-020: User decides, never override. P-022: NEVER deceive. Violations blocked." -->
```

The above HTML comment causes the constraint to be re-injected at every prompt by the framework's L2 enforcement mechanism. The prohibitive vocabulary (NEVER, blocked) is preserved in the re-injection content.

**Evidence Base:**
- VS-001 (T4): 33 NEVER/MUST NOT instances in production rule files; many are tagged for L2 re-injection.
- VS-002 (T4): One observation favoring Explanation 3 (engineering discovery) over Explanation 2 (convention): constraints are not just stated once but re-injected at every prompt using negative vocabulary. The choice to re-inject negative (rather than positive) framing is an observable design decision.
- quality-enforcement.md (mechanically verified): L2 layer described as "Immune" to context rot vs. L1's "Vulnerable."

**Known Limitations:**
- T4 observational; causal contribution of vocabulary vs. re-injection frequency not isolated
- Requires framework support for per-turn re-injection (not a pure prompt pattern)
- Re-injection mechanism is framework-specific; not directly portable to all LLM deployment contexts
- Context compaction failure mode may still affect re-injected rules under extreme compaction (noted in T-004)

**Relationship to Other Patterns:**
- AUGMENTATION of NPT-009 or NPT-010 (re-injects the base constraint)
- PREREQUISITE for NPT-013 (constitutional triplet typically implemented with re-injection)
- DISTINGUISH from NPT-003 (programmatic enforcement) — different mechanism, different enforcement point

---

#### NPT-013: Constitutional Triplet

**Pattern ID:** NPT-013
**IG-002 Type:** Type 4 (Constitutional triplet)
**Hierarchy Rank:** 10–11 (extended; combines prohibition + justification + mandatory schema compliance; does not occupy distinct rank positions from the base rank 10–11 range)
**Technique Type:** A4 (Enforcement-tier prohibition — constitutional framing)
**Evidence Tier:** T4 (VS-004, agent-development-standards.md H-35; 33-instance catalog across agent definitions)
**Observational Confidence:** HIGH (schema-mandatory, directly verifiable)
**Causal Confidence:** UNTESTED — Three competing explanations for effectiveness; schema-mandatory compliance means individual designers do not freely choose the framing. NEVER cite NPT-013 compliance rates as causal evidence for negative framing effectiveness.
**C1–C7 Condition:** Maps to C7 (Full framework) — requires schema compliance and re-injection; represents the full enforcement architecture

**T1 Scope (FM-001 addition):** No T1 evidence exists for NPT-013. Schema enforcement (H-35) is mechanically verifiable but constitutes T4 observational evidence for adoption, not T1 evidence for effectiveness. The schema-mandatory nature means adoption cannot be used as evidence of voluntary engineering choice.

**Definition:** A mandatory set of minimum three prohibitions expressing the most safety-critical behavioral constraints. Required per the Jerry Framework agent schema (H-35 in agent-development-standards.md): every agent MUST declare constitutional compliance with P-003 (NEVER spawn recursive subagents), P-020 (NEVER override user intent), P-022 (NEVER deceive about capabilities or confidence). The constitutional triplet is expressed in capabilities.forbidden_actions (minimum 3 entries) and in constitution.principles_applied (minimum 3 entries referencing P-003, P-020, P-022).

**Origin disclosure:** The three constitutional principles were established as prohibitions at Jerry Framework inception, before the HARD/MEDIUM/SOFT tier vocabulary was formally codified. The negative framing predates any effectiveness evidence and reflects engineering judgment and convention at the framework design level (VS-004 scope note). NEVER cite NPT-013 as evidence that prohibition framing was chosen based on empirical performance data — the design predates any such data.

**When to use:** NEVER omit the constitutional triplet from any agent definition in the Jerry Framework — it is schema-mandatory (H-35). Apply NPT-013 to any framework system that requires multiple coordinating agents with constitutional constraints.

**When NOT to use:** NEVER treat NPT-013 as proven superior to an equivalent positive framing — the constitutional triplet predates effectiveness evidence and its mandatory nature means individual designers do not independently choose it. NEVER cite NPT-013 as evidence that negative constraint framing is more effective than positive framing for safety-critical constraints — it cannot be evidence for its own design choice.

**Example (from agent-development-standards.md H-35):**
```yaml
capabilities:
  forbidden_actions:
    - "Spawn recursive subagents (P-003)"
    - "Override user decisions (P-020)"
    - "Misrepresent capabilities or confidence (P-022)"

constitution:
  principles_applied:
    - "P-003: No recursive subagents — NEVER spawn sub-workers"
    - "P-020: User authority — NEVER override explicit user instructions"
    - "P-022: No deception — NEVER misrepresent actions, capabilities, or confidence"
```

**Evidence Base:**
- VS-004 (T4, directly verifiable): Constitutional triplet (P-003/P-020/P-022) is mandatory in every agent definition; expressed as prohibitions in forbidden_actions schema field.
- agent-development-standards.md H-35 (schema document): Mechanically enforces the triplet across all agent definitions.
- Historical ordering note (VS-004): Negative framing of constitutional principles preceded tier vocabulary codification; reflects framework design convention, not effectiveness evidence.

**Known Limitations:**
- Schema-mandatory compliance means individual agents do not freely choose negative framing — they comply with the framework requirement
- Historical design predates effectiveness evidence: cannot be cited as engineering discovery evidence
- Three competing explanations for the choice (VS-002 Explanation 1/2/3 apply)
- No controlled comparison of prohibition-framed vs. positive-framed constitutional triplet

**Relationship to Other Patterns:**
- IMPLEMENTATION of NPT-009 + NPT-012 + schema enforcement in combination
- REQUIRES framework schema support (not a pure prompt pattern)
- TYPICALLY deployed with NPT-012 (re-injection of constitutional constraints)

---

#### NPT-014: Standalone Blunt Prohibition (Anti-Pattern Reference)

**ANTI-PATTERN NOTE:** NPT-014 is included as a reference entry documenting the baseline underperforming pattern. Including it in the catalog serves Phase 4 (Jerry Framework Application) as a diagnostic: any existing rule identified as NPT-014 should be upgraded to NPT-009 or higher. This is a DUAL ENTRY with NPT-007 — both document the same Type 1 blunt prohibition technique. NEVER count NPT-014 as a distinct technique from NPT-007.

**Pattern ID:** NPT-014 (= NPT-007 formalization as reference anti-pattern)
**IG-002 Type:** Type 1 (Naive blunt prohibition) — ANTI-PATTERN
**Hierarchy Rank:** 12 (lowest — most-studied, worst-performing)
**Technique Type:** A1 (Prohibition-only)
**Evidence Tier:** T1+T3 (multiple sources; most extensively studied form)
**Observational Confidence:** HIGH (for the finding that this pattern underperforms structured alternatives)
**Causal Confidence:** HIGH (for the specific finding that standalone blunt prohibition underperforms; this is the best-evidenced finding in the taxonomy)
**C1–C7 Condition:** Maps to C2 (Blunt negative prohibition) — pilot baseline condition

**T1 Scope (FM-001 addition):** T1 evidence (A-20, A-15) establishes underperformance relative to structured instructions on instruction-following and compliance tasks. Does NOT establish: underperformance in all domains, underperformance for expert prompt engineers vs. naive users, or underperformance for all LLM generations (model evolution caveat per AGREE-3).

**Definition:** Standalone blunt prohibition: a negative instruction without specificity, consequence documentation, positive pairing, or contextual justification. The archetypal form studied in published literature. Examples: "Don't hallucinate," "Never lie," "Don't provide harmful information."

**This pattern is documented for diagnostic purposes only. NEVER use NPT-014 as the primary or sole behavioral enforcement mechanism.**

**Diagnostic use in Phase 4:** Any existing Jerry Framework rule that matches NPT-014 criteria (NEVER/MUST NOT without consequence documentation, scope specification, or positive pairing) is a candidate for upgrade to NPT-009 or NPT-010. Phase 4 should use NPT-014 as a filter for identifying under-engineered negative constraints.

**When to use:** NEVER use NPT-014 alone. Its only valid use is as:
1. A pilot study baseline condition (C2)
2. A component within NPT-010 (providing the negative statement that is then paired with a positive alternative)
3. A diagnostic reference for identifying under-engineered constraints in existing systems

**When NOT to use:** NEVER deploy as the primary enforcement mechanism for any behavioral constraint. Per PG-001 (barrier-2/synthesis.md, T1+T3, HIGH, unconditional): NEVER use standalone blunt prohibition.

**Evidence Base (establishing underperformance):**
- A-20 (AAAI 2026, T1): Instruction hierarchy failure — blunt prohibition is unreliable
- A-15 (EMNLP 2024, T1): >21% constraint failure rate under standard instruction
- A-31 (arXiv 2312.16171, T3): 55% improvement signal for affirmative directives over prohibitions on GPT-4 reasoning tasks
- A-19 (arXiv, T3): Corroborating large-scale evidence

**Known Limitations:**
- Expert user moderating variable (IN-001-R3): Expert prompt engineers may achieve better compliance than naive users; studies may not reflect expert usage
- Context specificity: A-31's 55% figure applies to reasoning tasks on GPT-4; may not generalize
- Model evolution: Some evidence (AGREE-3 caveat) suggests newer models follow instructions better — the underperformance gap may be smaller for frontier models than older studies indicate

**Relationship to Other Patterns:**
- Upgrade path: NPT-014 → NPT-009 (add specificity + consequence)
- Extended upgrade: NPT-014 → NPT-010 (add positive pairing) or NPT-011 (add justification)
- Full upgrade: NPT-014 → NPT-013 (implement as constitutional triplet with re-injection)

---

## L2: Detailed Evidence Tables and Matrices

### C1–C7 Condition Alignment Matrix

**CRITICAL CONSTRAINT FROM BARRIER-2/SYNTHESIS.MD ST-5:** This alignment matrix preserves the exact C1–C7 pilot condition mapping from TASK-005. NEVER modify the hierarchy ordering without reassessing this mapping and producing an explicit impact assessment. Any reordering that changes which hierarchy levels map to which conditions invalidates the TASK-005 pilot design.

**Source conditions from claim-validation.md (TASK-005) — verified:**

| Condition | Description | Primary Negative Framing Element | Mapped Pattern(s) | Hierarchy Rank(s) | Modification to Hierarchy? |
|-----------|-------------|----------------------------------|-------------------|-------------------|-----------------------------|
| **C1** | Baseline positive-only — no negative constraints | None (positive framing only) | Reference baseline (no NPT) | Baseline | None — C1 is the positive control |
| **C2** | Blunt negative prohibition — standalone NEVER/MUST NOT | Prohibition vocabulary only, no structure | NPT-007, NPT-014 | 12 | None — NPT-007/014 already at rank 12 |
| **C3** | Structured negative constraint — NEVER with consequence | Prohibition + consequence documentation | NPT-009 | 9 | None — NPT-009 assigned rank 9 |
| **C4** | Paired negative-positive — prohibition + positive alternative | Prohibition + positive alternative | NPT-010 | 10 | None — NPT-010 assigned rank 10 |
| **C5** | Justified negative constraint — NEVER with reason | Prohibition + contextual justification | NPT-011 | 11 | None — NPT-011 assigned rank 11 |
| **C6** | Hierarchical negative — HARD/MEDIUM/SOFT tiering | Tier-classified enforcement vocabulary | NPT-009 (HARD tier only) + framework enforcement architecture | 9 (HARD tier) | None — NPT-009 at rank 9 represents HARD tier declarative behavioral negation |
| **C7** | Full framework — all techniques combined | All: re-injection + constitutional + paired + justified | NPT-010 + NPT-011 + NPT-012 + NPT-013 | 10–13 (combined) | None — full combination, no single rank |

**Alignment verdict:** PRESERVED. The C1–C7 mapping is fully consistent with the hierarchy ordering. No modification to the hierarchy ordering was made in this taxonomy. NPT assignments are additive extensions of the hierarchy, not reorderings.

**Phase 5 implication:** The pilot design (n=30, McNemar test, primary comparison C2 vs. C3) directly tests NPT-014 vs. NPT-009. This is the most important comparison: does specificity + consequence documentation (NPT-009) produce better outcomes than standalone blunt prohibition (NPT-014)?

---

### Evidence Gap Map

This map identifies which taxonomy entries have T1 evidence, which have only T4/observational, and which are entirely untested in controlled conditions. This feeds directly into Phase 5's experimental prioritization.

| Pattern ID | Name | T1 Evidence | T3 Evidence | T4 Evidence | Untested (controlled) | Phase 5 Priority |
|------------|------|-------------|-------------|-------------|----------------------|-----------------|
| NPT-001 | Model-Internal Intervention | A-28 (ICLR 2025) | — | — | Prompt-level applicability | Out of scope |
| NPT-002 | Training-Time Constitutional | — | A-10 (arXiv) | — | Prompt-level applicability | Out of scope |
| NPT-003 | Programmatic Enforcement | — | C-13 (DSPy preprint) | I-27 (NeMo) | Prompt framing comparison | Relevant — infrastructure |
| NPT-004 | Verification Pipeline | A-22 (ACL 2024) | — | — | Framing comparison | Orthogonal — mechanism |
| NPT-005 | Warning-Based Meta-Prompt | A-23 (EMNLP 2025) — negation accuracy ONLY | — | — | Hallucination rate; behavioral compliance | HIGH — only T1 for negation accuracy |
| NPT-006 | Atomic Decomposition | A-15 (EMNLP 2024) — compliance ONLY | — | — | Hallucination rate | HIGH — only T1 for compliance |
| NPT-007 / NPT-014 | Blunt-Prohibition Baseline / Anti-Pattern Reference (same technique, dual catalog entry) | A-20 (AAAI 2026); A-15 (EMNLP 2024) | A-31, A-19 | — | Structured positive comparison | HIGH — best-evidenced underperformance; single Phase 5 experimental slot (C2 baseline). NEVER count as two separate HIGH-priority items. |
| NPT-008 | Contrastive Example Pairing | — | A-11 (arXiv) | — | Compliance; hallucination | MEDIUM |
| NPT-009 | Declarative Behavioral Negation | — | — | VS-001–VS-004 | Causal effectiveness; vs. positive equivalent | CRITICAL — primary C2 vs. C3 comparison |
| NPT-010 | Paired Prohibition + Positive | — | A-11 (partial) | VS-001, NP-002 (AGREE-8) | Paired vs. unpaired; vs. positive equivalent | HIGH — C4 condition |
| NPT-011 | Justified Prohibition | — | — | VS-001, NP-003 (AGREE-9) | Justified vs. unjustified; vs. positive equivalent | HIGH — C5 condition |
| NPT-012 | L2 Re-Injected Constraint | — | — | VS-001–VS-004, L2-REINJECT mechanism | Vocabulary contribution vs. re-injection frequency | CRITICAL — C4 isolation |
| NPT-013 | Constitutional Triplet | — | — | VS-004, H-35 | Schema-mandatory; historical design | LOW — schema compliance, not effectiveness |

**Note on NPT-007/NPT-014 Phase 5 priority:** NPT-007 and NPT-014 are the same technique (Type 1 blunt prohibition). In Phase 5, both map to Condition C2 (baseline). They are merged into a single "NPT-007 / NPT-014" row in this map to eliminate visual double-counting. NEVER count them as two separate HIGH-priority items for experimental resource allocation — they represent a single experimental slot (C2 baseline).

**Summary of evidence distribution:**
- **T1 evidence (controlled studies):** NPT-005, NPT-006, NPT-007 (partial) — 3 patterns
- **T4 only (observational, no controlled study):** NPT-009, NPT-010, NPT-011, NPT-012, NPT-013 — 5 patterns
- **Untested in controlled conditions:** All comparisons of NPT-009 through NPT-012 against positive equivalents — these are the Phase 2 experimental targets
- **Out of scope for prompt engineering:** NPT-001, NPT-002, NPT-004 (infrastructure/training level)

**The critical evidence void:** No controlled study has ever compared a structured negative constraint (NPT-009) against a structurally equivalent positive instruction on the same task. This is the central Phase 2 experimental gap and the most important void in this evidence gap map.

---

### Full Pattern Cross-Reference Matrix

> **CRITICAL USAGE WARNING (RT-001/IN-001 resolution, v2.0.0):** NEVER use this matrix as a standalone decision guide. Evidence scope constraints present in the full pattern entries are NOT reproduced here. "Use for enforcement tier?" reflects observational evidence only — it does NOT imply experimental validation of negative framing over positive equivalents. All rows marked T4 have UNTESTED causal comparison status (see "Causal comparison tested?" row). NEVER extract rows from this matrix without reading the corresponding full pattern entry and co-citing the complete confidence label including both Observational Confidence and Causal Confidence values. This matrix is a navigation aid, not a decision instrument.

| Aspect | NPT-005 | NPT-006 | NPT-007/014 | NPT-008 | NPT-009 | NPT-010 | NPT-011 | NPT-012 | NPT-013 |
|--------|---------|---------|-------------|---------|---------|---------|---------|---------|---------|
| IG-002 Type | 2 (meta) | 2 | 1 (ANTI) | 2 (contrastive) | 2 | 2 (paired) | 2 (justified) | 3 | 4 |
| Hierarchy Rank | 5 | 6 | 12 | 8 | 9 | 10 | 11 | 10 ext | 10–11 ext |
| Min. evidence tier | T1 | T1 | T1 | T3 | T4 | T4 | T4 | T4 | T4 |
| T1 Scope (FM-001 addition, v2.0.0) | Negation accuracy only (NOT compliance, NOT hallucination rate) | Compliance rate only (NOT hallucination, NOT long-context) | Underperformance established (NOT: expert users, all domains, all model generations) | No T1 (T3 only) | No T1 for full pattern (A-15 partial: specificity component only) | No T1 | No T1 | No T1 (mechanical verification ≠ T1) | No T1 (schema verification ≠ T1) |
| Observational Confidence | MEDIUM (single T1 study, no replication) | MEDIUM | HIGH | LOW | HIGH | MEDIUM | MEDIUM | HIGH | HIGH |
| Causal Confidence | MEDIUM (negation accuracy construct scope only — NOT generalizable to hallucination rate) | MEDIUM (compliance rate construct only) | HIGH (underperformance on studied tasks/models) | LOW | LOW (UNTESTED vs. positive equivalent) | UNTESTED | UNTESTED | LOW (UNTESTED vocabulary contribution) | UNTESTED |
| Causal comparison tested? | No (framing effect on negation accuracy tested; not vs. positive equivalent overall) | No (compliance improvement tested; not negative vs. positive for full constraint) | Yes — underperformance vs. structured alternatives established | No | No | No | No | No | No |
| Prompt-only? | Yes | Yes | Yes | Yes | Yes | Yes | Yes | No (framework) | No (schema) |
| Requires infrastructure? | No | No | No | No | No | No | No | Yes (re-injection) | Yes (schema) |
| Consequence documented? | No (meta) | No | No | No | YES | YES | YES | YES | YES |
| Positive alternative paired? | No | No | No | Yes (example) | No | YES | No | Optional | No |
| Justification included? | Implied | No | No | No | No | No | YES | Optional | Implied (P-003/P-020/P-022) |
| Context compaction risk? | Low | Low (design inference, not empirically established) | HIGH (T-004 failure mode derived) | Low | HIGH (T-004 failure mode derived) | HIGH (T-004 failure mode derived) | HIGH (T-004 failure mode derived) | Mitigated | Mitigated |
| Use for enforcement tier? | Priming only | Structuring | NEVER alone | Illustrating | YES (T4 obs, UNTESTED causal) | YES (T4 obs, preferred, UNTESTED causal) | YES (T4 obs, UNTESTED causal) | YES (T4 obs, UNTESTED causal) | YES (T4 obs, mandatory, UNTESTED causal) |

---

### Downstream Reference Index for Phase 4

> **CRITICAL USAGE WARNING:** NEVER use this index as a standalone decision guide. Evidence scope constraints in the full pattern entries are NOT reproduced here. NEVER cite NPT patterns from this index without co-citing the evidence tier and causal confidence from the full pattern entry. NEVER use this index to justify implementation decisions that should await Phase 5 experimental validation. Multi-pattern combinations may produce interaction effects not predictable from individual pattern properties — NEVER assume combined patterns are simply additive.

| Phase 4 Task | NPT Pattern(s) to Reference | Evidence Tier | Causal Confidence | Action |
|-------------|----------------------------|---------------|-------------------|--------|
| Audit existing HARD rules for anti-pattern instances | NPT-014 as diagnostic filter | T1+T3 | HIGH (underperformance established) | Identify rules matching blunt prohibition criteria → upgrade to NPT-009 |
| Assess enforcement tier vocabulary design | NPT-009, NPT-012 | T4 obs | LOW / UNTESTED causal | Verify specificity + consequence documentation present in all HARD rules |
| Evaluate L2-REINJECT markers | NPT-012 | T4 obs | LOW causal | Verify re-injected content uses NPT-009 (not NPT-014) pattern |
| Review agent constitutional triplets | NPT-013 | T4 obs / Schema | UNTESTED causal | Verify all three P-003/P-020/P-022 prohibitions are present and correctly scoped |
| Assess rule pairing (NEVER + positive alternative) | NPT-010 | MEDIUM obs (AGREE-8) | UNTESTED causal | Identify HARD rules without positive alternative pairing → add per NP-002 (working practice, UNTESTED) |
| Evaluate justification presence in rules | NPT-011 | MEDIUM obs (AGREE-9) | UNTESTED causal | Identify HARD rules without contextual justification → add per NP-003 (working practice, UNTESTED) |
| Review long-context session constraints | NPT-012 | T4 obs | LOW causal | Ensure critical constraints have L2-REINJECT markers; assess T-004 risk |
| Evaluate programmatic constraint overlap | NPT-003, NPT-004 | T3+T4 | MEDIUM (mechanism) | Document where infrastructure enforcement backs up prompt-level constraints |
| Assess context compaction risk | NPT-009, NPT-012 | T4 obs | T4 obs (context drop is observable) | Map long-context deployments; verify NPT-014 absence and NPT-012 presence |
| Benchmark framing decisions for Phase 2 isolation | NPT-009 vs. hypothetical positive equivalent | UNTESTED | UNTESTED | Ensure Phase 4 changes do not couple vocabulary to other mechanisms in ways that confound Phase 2 |
| Design new behavioral constraints (prospective) | NPT-009, NPT-010, NPT-011 | T4 obs | UNTESTED causal — NEVER use as evidence for negative-over-positive framing choice | Use structural checklist: (1) Is the failure mode specific and documentable? → NPT-009. (2) Is a positive alternative unambiguous? → add NPT-010 element. (3) Does the rationale help define edge cases? → add NPT-011 element. CAVEAT: These structural recommendations reflect T4 working practice; whether equivalent positive framing would achieve equal results is UNTESTED. |
| Phase 5 framing-choice resolution | When Phase 5 experimental results are available, this row will be updated with the experimental verdict on negative vs. positive framing at ranks 9–11. Until then, NEVER use this taxonomy to guide the framing choice itself — only to assess structural compliance of constraints already committed to negative framing. | Phase 5 results | NPT-009 through NPT-011 (framing comparison pending) |

**Phase 4 NEVER directives (from barrier-2/synthesis.md ST-5 Phase 4 constraints):**

NEVER present the enforcement tier vocabulary design as experimentally validated — it is T4 observational working practice only (NPT-009 through NPT-013 are all T4 causal confidence).

NEVER implement Phase 4 changes that make Phase 2 experimental conditions unreproducible — any change that couples the NEVER/MUST NOT vocabulary to other mechanisms beyond NPT-009 specificity and NPT-011 justification would confound Phase 2 Condition C3 vs. C1 comparison.

NEVER ignore PG-003's contingency: if Phase 2 finds a null framing effect at ranks 9–11 (NPT-009 through NPT-011), vocabulary choice becomes convention-determined. Phase 4 design should be reversible on the vocabulary dimension. NEVER implement irreversible vocabulary changes before Phase 2 results are available.

---

### Practitioner Guidance Summary (from Phase 2 — PG-001 through PG-005)

> **CRITICAL EXTRACTION WARNING:** NEVER extract these guidance items without co-citing the Confidence column. MEDIUM confidence items are working practice only and are NOT validated recommendations — they reflect what expert practitioners do, not what controlled experiments have established as superior. Extracting guidance statements without confidence labels removes the epistemological distinction between T1-validated guidance and T4-observed working practice.

These guidance items are sourced from barrier-2/synthesis.md ST-4. Each has an explicit confidence tier.

| Guidance ID | Statement | Confidence | Evidence Basis | NPT Pattern(s) |
|-------------|-----------|------------|----------------|----------------|
| PG-001 | NEVER use standalone blunt prohibition | T1+T3, HIGH, unconditional | A-20, A-15, A-31, A-19 | NPT-007/014 (anti-pattern) |
| PG-002 | NEVER design a constraint without specifying hierarchy rank | T1+T4, HIGH, unconditional | VS-003 (tier architecture); A-15 (specificity improves compliance) | NPT-009 through NPT-013 |
| PG-003 | Pair enforcement-tier constraints with consequences | T4 observational, MEDIUM — working practice only; Phase 2 will assess causal contribution | VS-001–VS-004 | NPT-009 (consequence requirement) |
| PG-004 | Test context compaction behavior before deployment | T4, unconditional by failure mode logic | I-28, I-32 (GAP-13) | NPT-012 (mitigation for T-004) |
| PG-005 | Prioritize enforcement architecture over framing vocabulary optimization | T3 (DSPy) + T4 (NeMo), unconditional investment allocation | C-13, I-27 | NPT-003, NPT-004 (prefer over NPT-014) |

**Citation requirement (PM-002 resolution):** Downstream documents citing any PG item from this table MUST co-cite: (1) the Guidance ID, (2) the Confidence label verbatim, (3) the Evidence Basis tier. NEVER strip the Confidence label when summarizing practitioner guidance in Phase 4 or Phase 5 documents. If the full confidence label cannot be reproduced in context, cite the full pattern entry instead.

---

## PS Integration

> P-002 compliance: Synthesis persisted to file. Worktracker linked. Downstream agents indexed.

### Constraint Propagation Requirement (RT-003/PM-002 resolution, v2.0.0)

**NEVER cite NPT patterns from this taxonomy in downstream documents without restating the epistemological status of the underlying evidence.** Phase 4 and Phase 5 documents MUST NOT cite NPT-009 through NPT-013 without the accompanying "T4 observational, UNTESTED causal comparison" label. The ST-5 constraints from barrier-2/synthesis.md are inherited by this taxonomy and MUST propagate to all downstream documents that cite NPT patterns. As the research pipeline progresses through Phase 4 and Phase 5, each downstream document will cite this taxonomy rather than the upstream barrier-2/synthesis.md constraint source — this makes the ST-5 constraints progressively harder to trace unless each downstream document explicitly restates them.

**Downstream propagation checklist for any document citing this taxonomy:**
- [ ] NEVER cite NPT-009 through NPT-011 without stating "UNTESTED causal comparison against positive equivalent"
- [ ] NEVER cite NPT-012 without stating "UNTESTED vocabulary contribution vs. re-injection frequency"
- [ ] NEVER cite NPT-013 without stating "schema-mandatory, predates effectiveness evidence"
- [ ] NEVER cite NPT-006's T1 evidence without scoping it to "compliance rate only"
- [ ] NEVER cite NPT-005's T1 evidence without scoping it to "negation reasoning accuracy only"

**Structural enforcement hook (I3 addition):** Phase 4 artifacts MUST include a "Constraint Propagation Compliance" section in their PS Integration block. That section MUST document: (a) which NPT pattern IDs were cited in the artifact, and (b) confirmation that the epistemological status label (evidence tier + causal confidence) was co-cited for each cited pattern. This requirement is verifiable by an adversary gate: an adversary reviewer MUST check for the presence and completeness of the "Constraint Propagation Compliance" section before scoring any Phase 4 artifact above 0.90 on the Traceability dimension. NEVER score a Phase 4 artifact above 0.90 on Traceability if the "Constraint Propagation Compliance" section is absent.

### Worktracker Entry

| Field | Value |
|-------|-------|
| Project | PROJ-014-negative-prompting-research |
| Orchestration | neg-prompting-20260227-001 |
| Task ID | TASK-008 |
| Parent Epic | EPIC-002 (Comparative Analysis & Taxonomy) |
| Artifact | `orchestration/neg-prompting-20260227-001/phase-3/taxonomy-pattern-catalog.md` |
| Status | DONE — Revised per I1 adversary gate (TASK-009) |
| Quality Threshold | >= 0.95 (C4) |
| Input Count | 5 source documents |
| Output | 14 patterns (NPT-001 through NPT-014) / 13 distinct techniques |

### Key Findings for Downstream Agents

> Per CB-04: 3–5 key findings bullets for downstream orientation. Full detail in pattern catalog entries.

1. **MUST NOT treat prompt-accessible negative prompting techniques as a single category.** The taxonomy reveals three evidence-backed distinct mechanisms: T1-confirmed warning-based meta-prompting (NPT-005, +25.14% negation accuracy only), T1-confirmed atomic constraint decomposition (NPT-006, compliance rate only), and T4-observational constitutional triplet schema (NPT-013) — each with different applicability domains and confidence levels.
2. **MUST NOT present ranks 9–11 (NPT-009, NPT-010, NPT-011) as having established causal superiority over positive equivalents.** The C1–C7 pilot condition alignment matrix confirms these patterns are UNTESTED for causal comparison; directional verdict is explicitly absent per Phase 3 Gate Check 1.
3. **MUST NOT conflate rank 12 (blunt prohibition, NPT-007/NPT-014) with ranks 9–11.** NPT-007's T1 evidence (AGREE-4) establishes underperformance — HIGH confidence; NPT-009 through NPT-011 are UNTESTED for the same dimension. This is a CRITICAL DISTINCTION for Phase 4 update analysis.
4. **MUST NOT treat the 12-level hierarchy as externally validated.** It is internally generated narrative synthesis (AGREE-5, R4, 0.953 PASS, 2026-02-27); ranks 1–4 are out-of-scope for prompt engineering; prompt-engineering-accessible patterns are ranks 5–12 (10 of 14 total).
5. **Phase 4 primary lookup:** Use the Downstream Reference Index section for mapping each Jerry Framework component (skills, agents, rules, patterns, templates) to specific NPT pattern IDs and evidence tiers. NEVER use the Cross-Reference Matrix as a standalone decision guide — always read the full pattern entry.

### Synthesizer Output State

```yaml
synthesizer_output:
  ps_id: "neg-prompting-20260227-001"
  entry_id: "TASK-008"
  artifact_path: "projects/PROJ-014-negative-prompting-research/orchestration/neg-prompting-20260227-001/phase-3/taxonomy-pattern-catalog.md"
  source_count: 5
  patterns_generated:
    - "NPT-001" # Model-Internal Behavioral Intervention
    - "NPT-002" # Training-Time Constitutional Constraint
    - "NPT-003" # Programmatic Constraint Enforcement
    - "NPT-004" # Verification Pipeline Constraint
    - "NPT-005" # Warning-Based Meta-Prompt
    - "NPT-006" # Atomic Constraint Decomposition
    - "NPT-007" # Blunt-Prohibition Baseline Acknowledgment
    - "NPT-008" # Contrastive Example Pairing
    - "NPT-009" # Declarative Behavioral Negation
    - "NPT-010" # Paired Prohibition with Positive Alternative
    - "NPT-011" # Justified Prohibition with Contextual Reason
    - "NPT-012" # L2 Re-Injected Negative Constraint
    - "NPT-013" # Constitutional Triplet
    - "NPT-014" # Standalone Blunt Prohibition Anti-Pattern (dual entry with NPT-007)
  distinct_techniques: 13
  themes:
    - "Prompt-accessible vs. training-accessible technique boundary"
    - "Evidence tier stratification (T1 vs. T4 vs. Untested)"
    - "Vendor framing divergence from academic evidence base"
    - "Blunt prohibition underperformance as established baseline"
    - "Constitutional triplet as emerging schema standard"
  confidence: 0.87
  next_agent_hint: "Phase 4 — Jerry Framework Application, using Downstream Reference Index"
```

### Session Context for Phase 4

```yaml
session_context:
  schema_version: "1.0.0"
  source_agent:
    id: "ps-synthesizer"
    family: "ps"
    cognitive_mode: "convergent"
    model: "sonnet"
  target_agent: "Phase 4 Jerry Framework Application agent"
  payload:
    key_findings:
      - "14 NPT patterns cataloged (13 distinct techniques); ranks 1–4 out-of-scope for prompt engineering"
      - "I1 adversary gate: 4 Critical, 11 Major, 12 Minor findings — all Critical and Major addressed in v2.0.0"
      - "C1–C7 alignment PRESERVED — no hierarchy modifications made"
      - "Synthesizer confidence: 0.87 (hierarchy internally generated, not externally validated)"
    open_questions:
      - "Whether NPT-009 through NPT-011 T4 confidence (HIGH obs) warrants T3 study design before Phase 5 pilot"
      - "Whether NPT-013 Constitutional Triplet schema pattern requires a separate ADR in Phase 5"
      - "Whether external validation of the 12-level hierarchy is feasible before Phase 5 execution"
    blockers: []
    confidence: 0.87
    artifacts:
      - path: "projects/PROJ-014-negative-prompting-research/orchestration/neg-prompting-20260227-001/phase-3/taxonomy-pattern-catalog.md"
        type: "synthesis"
        summary: "14-pattern negative prompting taxonomy v2.0.0 with C1-C7 mapping, evidence gap map, Phase 4 downstream index, and I1 adversary findings resolved"
  timestamp: "2026-02-28"
```

> **Confidence note (0.87):** Set below HIGH (0.90) because the 12-level hierarchy is an internally generated synthesis narrative (AGREE-5 disclosure) rather than an externally validated framework. The pattern entries themselves are grounded in cited evidence, but the rank ordering within the prompt-accessible tier (ranks 5–11) carries systematic uncertainty. This confidence level is unchanged from v1.0.0 — addressing the I1 adversary findings improves structural integrity and disclosure completeness, but does not change the underlying epistemic status of the hierarchy.

---

## Self-Review Checklist

> H-15 compliance: Applied before completion per quality-enforcement.md H-15 and adversarial quality standards for synthesis agents.

| Check | Status | Evidence | Phase 3 Adversary Gate Requirement |
|-------|--------|----------|-------------------------------------|
| P-001 (Patterns accurately reflect source content) | PASS | Every pattern entry cites the source documents and sections; no pattern claims exceed what the evidence supports | Yes |
| P-002 (Synthesis persisted to file) | PASS | Written to `phase-3/taxonomy-pattern-catalog.md` | Yes |
| P-004 (All patterns citing sources) | PASS | Each pattern entry includes an Evidence Base section with tier-labeled citations | Yes |
| P-011 (Themes grounded in evidence) | PASS | No patterns were invented; all 14 derive from AGREE-5 hierarchy, IG-002 taxonomy, or explicitly cited evidence | Yes |
| P-022 (Contradictions disclosed) | PASS | Three competing explanations for vendor framing choices stated in NPT-009/NPT-012/NPT-013; evidence tier limitations explicitly disclosed throughout | Yes |
| Phase 3 Gate Check 1: Taxonomy does not imply a directional verdict at ranks 9–11 | PASS | All NPT-009 through NPT-011 entries state "UNTESTED" for the causal comparison against positive equivalents; every relevant entry includes the Phase 2 experimental target note | YES — Explicit |
| Phase 3 Gate Check 2: C1–C7 pilot condition mapping preserved | PASS | See C1–C7 Condition Alignment Matrix; no hierarchy modifications made; alignment verdict stated as PRESERVED | YES — Explicit |
| Phase 3 Gate Check 3: Rank 12 (NPT-007/014) distinguished from ranks 9–11 (NPT-009 through NPT-011) | PASS | NPT-007 and NPT-014 include CRITICAL DISTINCTION note; IG-002 integration section explicitly states AGREE-4 applies to Type 1 only; confidence labels differ (HIGH for rank 12 underperformance; HIGH obs/LOW causal for ranks 9–11) | YES — Explicit |
| Origin disclosure for hierarchy (MANDATORY per ST-5) | PASS | Origin and Scope Disclosure section states the hierarchy's epistemic status explicitly; every non-externally-validated rank ordering is flagged | YES |
| No collapse of rank 12 vs. ranks 9–11 distinction | PASS | Separate catalog entries; separate IG-002 type designations; separate C1–C7 mappings (C2 vs. C3/C4/C5) | YES |
| Evidence gap map produced | PASS | Evidence Gap Map table identifies T1/T4/Untested for all 14 patterns | YES |
| Phase 4 downstream reference index included | PASS | Downstream Reference Index table maps all Phase 4 analysis tasks to pattern IDs | YES |
| IG-002 taxonomy integrated | PASS | IG-002 Integration section maps all four types to AGREE-5 ranks and NPT pattern IDs | YES |
| Supplemental vendor evidence not treated as inferior | PASS | NPT-009 through NPT-013 use T4 evidence from VS-001–VS-004 at full face value; confidence labels are HIGH observational for observational claims | YES |
| Absence of evidence not treated as evidence of absence | PASS | UNTESTED label is explicitly distinct from "not supported" — see NPT-009 through NPT-011 entries; Phase 2 experimental target label confirms hypothesis remains open | YES |
| Navigation table present (H-23) | PASS | Document Sections table at top of document with Revision Log entry added | YES |
| No positive prompting framing in analysis (orchestration directive) | PASS | All analytical framing uses negative constraint vocabulary per directive; no analytical conclusions stated in positive recommendation form | YES |
| I1 Critical findings (DA-001, FM-001, IN-001, RT-001) addressed | PASS | DA-001: Prospective validity note added to Origin section. FM-001: T1 Scope row added to Cross-Reference Matrix. IN-001: Critical usage warning added to Cross-Reference Matrix and Downstream Reference Index headers. RT-001: Bolded warning added to Cross-Reference Matrix. | YES — I2 requirement |
| I1 Major findings (SM-001, SR-004, CC-001, DA-002, DA-003, PM-001, PM-002, FM-002, IN-002, RT-002, RT-003) addressed | PASS | See Revision Log for full accounting | YES — I2 requirement |
| Braun & Clarke citation removed; correct methodology stated | PASS | Frontmatter now states "Deductive framework extension"; Methodology Subsection added with explicit correction | YES — SR-004 fix |
| Cross-Reference Matrix includes Causal Confidence and T1 Scope rows | PASS | Matrix expanded with "T1 Scope", "Observational Confidence", "Causal Confidence", "Causal comparison tested?" rows | YES — FM-001/IN-002/DA-002 fix |
| Dual-entry design rationale documented in L0 and Pattern Catalog preamble | PASS | L0 states parenthetical "(13 distinct techniques — NPT-007 and NPT-014 are dual entries)"; Pattern Catalog preamble states design rationale | YES — CC-001/SM-002 fix |

---

## Revision Log

| Version | Score | Findings Addressed | Changes |
|---------|-------|-------------------|---------|
| 1.0.0 | 0.845 (REJECTED) | — | First version; 14 patterns cataloged across 3 dimensions; IG-002 integrated; C1–C7 matrix constructed; evidence gap map produced; downstream index produced |
| 2.0.0 | 0.938 (REVISE) | DA-001, FM-001, IN-001, RT-001 (Critical); SM-001, SR-004, CC-001, DA-002, DA-003, PM-001, PM-002, FM-002, IN-002, RT-002, RT-003 (Major); SM-002, SM-003, SR-001, SR-002, SR-003, SR-005, CC-002, CC-003, PM-003, CV-001, CV-002, FM-003 (Minor — all addressed) | See detailed change log below |
| 3.0.0 | TBD (I3) | NEW-001, NEW-002 (I2 new findings); I2 Actionability gap; I2 Internal Consistency gap; I2 Traceability gap; I2 minor improvements | See I3 change log below |

### Detailed Change Log (v1.0.0 → v2.0.0)

**Critical Findings:**

| Finding | Change Applied |
|---------|---------------|
| DA-001 (Prospective validity) | Added "Prospective Validity Note" subsection to Origin and Scope Disclosure. Describes what would change in C1–C7 mapping if ranks 5–11 were reordered after external validation. States mapping is provisional pending external validation. |
| FM-001 (T1 scope in matrix) | Added "T1 Scope" row to Full Pattern Cross-Reference Matrix. Each cell specifies the construct covered by T1 evidence or states "No T1." |
| IN-001 (Warning on lookup tables) | Added bold critical usage warning to both Full Pattern Cross-Reference Matrix and Downstream Reference Index headers. Warnings state NEVER use as standalone decision guide and require reading full pattern entries. |
| RT-001 (Matrix exploitable for causal claims) | Added prominent critical usage warning block to Cross-Reference Matrix. Warning states observational-only status and UNTESTED causal comparison for all T4 rows. |

**Major Findings:**

| Finding | Change Applied |
|---------|---------------|
| SM-001 (Rank 7 unoccupied) | Added "Rank 7 gap note" to L0 Executive Summary explaining why the gap reflects honest evidence coverage rather than a cataloging error. |
| SR-004 (Braun & Clarke inaccurate) | Removed Braun & Clarke citation from frontmatter; replaced with "Deductive framework extension." Added full Methodology Subsection explaining the actual method applied and explicitly distinguishing from inductive thematic analysis. |
| CC-001 (14 patterns overcounts distinct techniques) | Updated L0 to state "14 named patterns (13 distinct techniques)" with parenthetical explaining NPT-007/NPT-014 dual-entry design. Added Pattern Catalog preamble with dual-entry design rationale. |
| DA-002 (Confidence label conflation) | Split "Confidence Level" into "Observational Confidence" and "Causal Confidence" in every pattern entry header. Added both rows to Cross-Reference Matrix. |
| DA-003 ("Orthogonal" claim inaccurate) | Replaced "three orthogonal classification dimensions" with "three classification dimensions providing independent analytical perspectives." Added note about structurally impossible dimension combinations. |
| PM-001 (Prospective constraint design missing from index) | Added "Design new behavioral constraints (prospective)" row to Downstream Reference Index with UNTESTED caveat and structural checklist. |
| PM-002 (Citation requirements unspecified) | Added "Citation Requirements" subsection to Practitioner Guidance Summary requiring co-citation of evidence tier and confidence. Added Constraint Propagation Requirement to PS Integration with downstream checklist. |
| FM-002 (Context compaction risk rationale) | Added explanatory note to NPT-006 Known Limitations explaining that "Low" context compaction rating is a structural inference from decomposition design, not an empirically established finding. |
| IN-002 ("UNTESTED" absent from matrix) | Added "Causal comparison tested?" row to Full Pattern Cross-Reference Matrix with Yes/No values for each pattern. |
| RT-002 (Practitioner guidance extractable without labels) | Added critical extraction warning block to Practitioner Guidance Summary header. |
| RT-003 (ST-5 constraint propagation unaddressed) | Added "Constraint Propagation Requirement" section to PS Integration with downstream checklist for documents citing this taxonomy. |

**Minor Findings:**

| Finding | Change Applied |
|---------|---------------|
| SM-002 (Dual-entry design rationale under-explained) | Added dual-entry design rationale to Pattern Catalog preamble and L0 parenthetical. |
| SM-003 (NPT-010 multi-type assignment) | Added note in Dimension A table explaining multi-type assignments reflect simultaneous structural operation at multiple levels. Updated NPT-010 Technique Type field to state both A3 and A4 with explanation. |
| SR-001 (AGREE-5 missing version reference) | Added "(R4, 0.953 PASS, 2026-02-27)" to barrier-1/synthesis.md AGREE-5 reference in Origin section and L0. |
| SR-002 ("Extended" rank designation ambiguous) | Added note to IG-002 Integration section explaining "extended" rank designations are mechanism extensions of base ranks, not distinct hierarchy positions. |
| SR-003 (T2 tier empty without explanation) | Added T2 tier note to Dimension B Evidence Tier table explaining why T2 is empty (absorbed into T4 for the specific vendor documentation examined). |
| SR-005 (A-23 verification provenance unclear) | Added verification provenance note to NPT-005 Evidence Base: "Venue confirmed via ACL Anthology 2025.findings-emnlp.761; verification provenance: internal pipeline confirmation (comparative-effectiveness.md I5) — external venue verification not re-performed within this synthesis." |
| CC-002 (Revision Log absent from navigation table) | Added "Revision Log" to Document Sections navigation table. |
| CC-003 (Synthesizer confidence not in L0) | Added "Synthesizer confidence: 0.87" to L0 Executive Summary opening. |
| PM-003 (NPT-007/NPT-014 double-counted in gap map) | Added note to Evidence Gap Map stating NPT-007 and NPT-014 represent a single Phase 5 experimental slot and NEVER to count them as two separate HIGH-priority items. |
| CV-001 (33-instance count not re-verified) | Added "(count sourced from supplemental-vendor-evidence.md VS-001; not independently re-verified within this synthesis)" to IG-002 Integration observable evidence note. |
| CV-002 ("Minimum viable pattern" implies superiority) | Replaced "Use NPT-010 as the minimum viable pattern for any new behavioral constraint" with framing-caveated version: "For practitioners already committed to negative framing, NPT-010 represents the minimum structural requirement — the UNTESTED comparison against equivalent positive framing means this guidance cannot be extended to the positive-vs-negative framing choice itself." |
| FM-003 (Multi-pattern interaction effects not noted) | Added "NEVER assume combined patterns are simply additive" to Downstream Reference Index header warning. |

### Detailed Change Log (v2.0.0 → v3.0.0)

**I2 Adversary Findings — Actionability (Fix 1):**

| Finding | Change Applied |
|---------|---------------|
| I2 Actionability gap (no enforcement hook for constraint propagation) | Added structural enforcement hook paragraph to Constraint Propagation Requirement (PS Integration). Hook specifies that Phase 4 artifacts MUST include a "Constraint Propagation Compliance" section documenting which NPT IDs were cited and confirming epistemological status was co-cited. Adversary gate scoring rule added: NEVER score a Phase 4 artifact above 0.90 on Traceability without this section present. |
| I2 Actionability gap (no Phase 5 placeholder for framing-choice resolution) | Added "Phase 5 framing-choice resolution" row to Downstream Reference Index. Row text states: "When Phase 5 experimental results are available, this row will be updated with the experimental verdict on negative vs. positive framing at ranks 9–11. Until then, NEVER use this taxonomy to guide the framing choice itself." |

**I2 Adversary Findings — Internal Consistency (Fix 2):**

| Finding | Change Applied |
|---------|---------------|
| NEW-001 (Dimension A multi-type note not cross-referenced in NPT-010 entry) | Added cross-reference note to NPT-010 Technique Type field: "(See multi-type assignment note in Dimension A Classification table for patterns spanning multiple technique types.)" |
| NEW-001 symmetric (NPT-012 also spans A3 and A4 in the Dimension A table but entry listed A4 only) | Updated NPT-012 Technique Type field to state "A3 (Augmented prohibition — re-injection augments the base constraint) and A4 (Enforcement-tier prohibition with re-injection)" and added cross-reference note matching NPT-010. |

**I2 Adversary Findings — Traceability (Fix 3):**

| Finding | Change Applied |
|---------|---------------|
| I2 Traceability gap (Cross-Reference Matrix warning lacks finding ID) | Added "(RT-001/IN-001 resolution, v2.0.0)" to Cross-Reference Matrix critical usage warning header. |
| I2 Traceability gap (Constraint Propagation Requirement heading lacks finding ID) | Added "(RT-003/PM-002 resolution, v2.0.0)" to Constraint Propagation Requirement section heading. |
| I2 Traceability gap (T1 Scope row lacks annotation) | Added "(FM-001 addition, v2.0.0)" to T1 Scope row header in Cross-Reference Matrix. |

**I2 New Finding — Evidence Quality (Fix 4):**

| Finding | Change Applied |
|---------|---------------|
| NEW-002 (NPT-005 Observational and Causal Confidence near-identical in matrix, undermining split intent) | Changed NPT-005 Observational Confidence cell from "MEDIUM" to "MEDIUM (single T1 study, no replication)"; changed NPT-005 Causal Confidence cell from "MEDIUM (negation accuracy construct only)" to "MEDIUM (negation accuracy construct scope only — NOT generalizable to hallucination rate)". |

**I2 Minor Improvements (Fix 5):**

| Finding | Change Applied |
|---------|---------------|
| I2 Methodological Rigor improvement (symmetric rationale for HIGH context compaction risk) | Added "(T-004 failure mode derived)" qualifier to all HIGH context compaction risk cells in the Cross-Reference Matrix (NPT-007/014, NPT-009, NPT-010, NPT-011). LOW cells retain "(design inference, not empirically established)" qualifier from v2.0.0. |
| I2 Completeness improvement (NPT-007/NPT-014 visual double-counting in Evidence Gap Map) | Merged NPT-007 and NPT-014 into a single "NPT-007 / NPT-014" row in the Evidence Gap Map. Row combines both entries with a note clarifying they are the same technique. The footnote below the table is updated to reference the merged row rather than separate rows. |

---

*ps-synthesizer | TASK-008 | Phase 3 | PROJ-014 | 2026-02-28*
*Version: 3.0.0 (I3 — addresses I2 adversary findings: Actionability gap, Internal Consistency gap, Traceability gap, NEW-001, NEW-002, and minor improvements)*
*Quality threshold: >= 0.95 (C4, per orchestration directive)*
*Inputs: 5 source documents (barrier-1/synthesis.md R4, supplemental-vendor-evidence.md R4, barrier-2/synthesis.md v3.0.0, claim-validation.md R4, comparative-effectiveness.md R5)*
*Patterns: 14 (NPT-001 through NPT-014) / 13 distinct techniques*
*Constitutional Compliance: P-003, P-020, P-022*
*H-15 Self-review: Applied — checklist above documents compliance*
