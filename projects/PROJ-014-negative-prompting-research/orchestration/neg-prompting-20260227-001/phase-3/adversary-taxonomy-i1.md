# Strategy Execution Report: C4 Adversarial Tournament — Iteration 1

> adv-executor | TASK-009 | Barrier 3 | PROJ-014 | 2026-02-28
> Deliverable: phase-3/taxonomy-pattern-catalog.md (v1.0.0, ps-synthesizer)
> Quality threshold: >= 0.95 (C4)

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Execution Context](#execution-context) | Strategy set, deliverable, template references |
| [Special Verification Results](#special-verification-results) | Phase 3-specific gate checks (Barrier 2 ST-5) |
| [S-003 Steelman Technique](#s-003-steelman-technique) | Constructive strengthening before critique |
| [S-010 Self-Refine](#s-010-self-refine) | Self-review findings |
| [S-007 Constitutional AI Critique](#s-007-constitutional-ai-critique) | Constitutional/governance compliance |
| [S-002 Devil's Advocate](#s-002-devils-advocate) | Core assumption challenges |
| [S-004 Pre-Mortem Analysis](#s-004-pre-mortem-analysis) | Failure scenario enumeration |
| [S-012 FMEA](#s-012-fmea) | Component failure mode analysis |
| [S-013 Inversion Technique](#s-013-inversion-technique) | What would make this fail? |
| [S-011 Chain-of-Verification](#s-011-chain-of-verification) | Factual claim verification |
| [S-001 Red Team Analysis](#s-001-red-team-analysis) | Adversarial threat actor emulation |
| [S-014 LLM-as-Judge Scoring](#s-014-llm-as-judge-scoring) | Dimensional quality scoring |
| [Consolidated Findings Summary](#consolidated-findings-summary) | Cross-strategy finding table |
| [Execution Statistics](#execution-statistics) | Finding counts, protocol completion |

---

## Execution Context

- **Strategy Set:** C4 (all 10 selected strategies per quality-enforcement.md)
- **Deliverable:** `projects/PROJ-014-negative-prompting-research/orchestration/neg-prompting-20260227-001/phase-3/taxonomy-pattern-catalog.md`
- **Deliverable Version:** 1.0.0
- **Producing Agent:** ps-synthesizer (TASK-008)
- **Templates:** `.context/templates/adversarial/s-{001,002,003,004,007,010,011,012,013,014}.md`
- **Executed:** 2026-02-28
- **Execution Agent:** adv-executor
- **H-16 Status:** S-003 executes FIRST per H-16 mandate (Steelman before all critique strategies)
- **Special Verification:** Phase 3 Gate Checks 1–3 from Barrier 2 ST-5 evaluated under each applicable strategy

---

## Special Verification Results

> Required by Barrier 2 Synthesis ST-5. These three checks are evaluated across the tournament and confirmed below.

| Gate Check | Requirement | Verdict | Primary Strategy | Evidence |
|------------|-------------|---------|-----------------|---------|
| **GC-1** | Taxonomy MUST NOT imply directional verdict at ranks 9–11 | PASS | S-007, S-011 | All NPT-009/010/011 entries include explicit "UNTESTED" label; Key Finding 2 in PS Integration states the constraint in MUST NOT form; L0 summary states "UNTESTED (Phase 2 experimental target)" |
| **GC-2** | C1–C7 pilot condition mapping MUST be preserved or impact assessment provided | PASS | S-011, S-007 | C1–C7 Condition Alignment Matrix section present; alignment verdict "PRESERVED" explicitly stated; no hierarchy modifications made per entry-level fields |
| **GC-3** | Rank 12 MUST be distinguished from ranks 9–11 with confidence labels | PASS | S-011 | NPT-007/NPT-014 confidence label = "HIGH (underperforms)"; NPT-009 = "HIGH obs/LOW causal"; NPT-010/011 = "MEDIUM"; separate catalog entries; separate IG-002 type designations |

**Overall gate check result:** All three Phase 3-specific requirements are satisfied. Findings below identify secondary issues that do not invalidate these gate checks but do affect overall quality score.

---

## S-003 Steelman Technique

**Finding Prefix:** SM
**Protocol:** Six-step charitable reconstruction per Section 4 of s-003-steelman.md

### Step 1: Charitable Interpretation

**Core thesis of the deliverable:** The taxonomy provides a 14-pattern classification system for negative prompting techniques, organized across three orthogonal dimensions (technique type, evidence tier, applicability domain), with explicit epistemological constraints about what is and is not established by evidence. It serves as a structured intermediate artifact between Phase 2 findings and Phase 4 Jerry Framework application.

**Key claims:**
1. Negative prompting techniques form a coherent classification space spanning training-level interventions (ranks 1–4, out of scope) through prompt-accessible patterns (ranks 5–12, in scope)
2. The T1/T4 distinction is the primary validity boundary: only NPT-005, NPT-006, and NPT-007's underperformance are T1-evidenced
3. The Phase 2 experimental gap (NPT-009–NPT-011 vs. positive equivalents) is UNTESTED, not unsupported — a meaningful distinction for downstream consumers
4. The IG-002 four-type taxonomy from vendor practice provides structural context that published literature (Type 1 focused) systematically misrepresents

**Strongest interpretation:** The taxonomy's core intellectual contribution is its refusal to conflate observation with causality and its precise delineation of what is established (underperformance of Type 1), what is observed (production use of Types 2–4), and what is untested (comparative superiority of Types 2–4 vs. positive equivalents). This epistemic precision is the taxonomy's primary value for Phase 4.

### Steelman Strengths (as strengthening observations, not defects)

| ID | Strength | How the Deliverable Achieves It |
|----|----------|--------------------------------|
| SM-S-001 | Epistemic precision throughout | UNTESTED label, T4 vs. T1 distinction, "absence of evidence ≠ evidence of absence" applied consistently |
| SM-S-002 | Constraint inheritance from upstream | ST-5 constraints carried forward explicitly with NEVER/MUST NOT enforcement language in every relevant entry |
| SM-S-003 | Downstream actionability | Downstream Reference Index maps each Phase 4 task type to specific NPT IDs and evidence tiers |
| SM-S-004 | Self-disqualifying evidence principle | NPT-013 explicitly states "NEVER cite NPT-013 as evidence that prohibition framing was chosen based on empirical performance data — the design predates any such data" |
| SM-S-005 | Evidence gap map completeness | All 14 patterns assigned T1/T3/T4/Untested across controlled comparison dimension |

### Steelman Findings (improvement opportunities identified during charitable reconstruction)

**SM-001: Hierarchy Rank Ordering Rationale for Ranks 7–8 Is Absent**

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | Pattern entries NPT-007 and NPT-008; IG-002 Taxonomy Integration |
| **Strategy Step** | Step 2 (Structural weakness identification) |

**Evidence:** NPT-007 is assigned Hierarchy Rank 12 (lowest), but NPT-008 (Contrastive Example Pairing) is assigned Rank 8 with T3 evidence only (A-11). The 12-level hierarchy in the taxonomy covers ranks 1–12, but no pattern occupies ranks 7 or 8 as a named entry except NPT-008 at rank 8. The absence of a rank 7 entry is unexplained. Ranks 7 and 8 appear between NPT-006 (rank 6, T1) and NPT-009 (rank 9, T4), yet no rationale explains why NPT-008 occupies rank 8 rather than rank 7, or why no pattern occupies rank 7.

**Analysis:** The 12-level hierarchy claims to be a complete ordering of all negative prompting effectiveness levels, but ranks 7 and the absence of a rank 7 pattern represent a structural gap in the taxonomy's completeness. The reader cannot determine whether rank 7 was intentionally skipped, absorbed into rank 8, or represents a gap in source material.

**Recommendation:** Add an explicit note in the Origin and Scope Disclosure or in NPT-008's entry explaining why rank 7 is not occupied and why NPT-008 is placed at rank 8 rather than rank 7. Alternatively, acknowledge that the hierarchy granularity between ranks 6–9 is coarser than between ranks 9–12 and that the rank assignments within this range are more uncertain.

---

**SM-002: NPT-007 and NPT-014 Dual-Entry Rationale Is Under-Explained**

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | NPT-007 and NPT-014 entries |
| **Strategy Step** | Step 2 (Structural weakness) |

**Evidence:** NPT-007 (Blunt-Prohibition Baseline Acknowledgment, Rank 12) and NPT-014 (Standalone Blunt Prohibition Anti-Pattern) describe the same underlying pattern. NPT-014 explicitly states "NPT-014 (= NPT-007 formalization as reference anti-pattern)." The taxonomy counts both toward the 14-pattern total. A downstream consumer relying on the count of 14 distinct patterns may misattribute additional coverage to the taxonomy that does not exist.

**Analysis:** The dual-entry design serves a legitimate purpose (NPT-007 explains the phenomenon; NPT-014 serves as diagnostic reference for Phase 4). However, the relationship is stated only parenthetically in NPT-014's header. A reader scanning the pattern catalog entries may not recognize they refer to the same underlying behavior without careful reading.

**Recommendation:** Add a "dual-entry design rationale" note to either the L0 Summary or the Pattern Catalog preamble (line 146) explaining that NPT-007 and NPT-014 describe the same phenomenon with different purposes (observational vs. diagnostic), and that the 14-pattern count reflects distinct analytical purposes, not distinct techniques. NEVER present the count as 14 independent behaviors without this clarification.

---

**SM-003: Dimension A Classification Has Overlap for NPT-010**

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | Dimension A: Technique Type (line 88–97); NPT-010 entry |
| **Strategy Step** | Step 3 (Evidence strengthening) |

**Evidence:** NPT-010 is classified under both A3 (Augmented prohibition) and A4 (Enforcement-tier prohibition) in the Dimension A table: "A4: Enforcement-tier prohibition ... NPT-010, NPT-012, NPT-013." However, NPT-010's own entry states "Technique Type: A3 (Augmented prohibition)." The Dimension A table includes NPT-010 in both A3 and A4 rows, creating an ambiguity about whether NPT-010 belongs to one type or both.

**Analysis:** The orthogonality claim for the three classification dimensions ("any pattern can be located by any combination of these three dimensions") requires that Dimension A assignments be unambiguous. NPT-010's inclusion in two A-type rows undermines this claim. A downstream Phase 4 analyst using Dimension A as a filter would receive inconsistent results.

**Recommendation:** Resolve the NPT-010 Dimension A assignment to a single type (either A3 or A4). If NPT-010 genuinely operates at both levels, add a "multi-type patterns" note explaining that some patterns span multiple Dimension A types and the Dimension A table reflects primary and secondary classifications rather than exclusive membership.

---

## S-010 Self-Refine

**Finding Prefix:** SR
**Protocol:** Four-step self-review per s-010-self-refine.md Execution Protocol

### Step 1: Completeness Check

**Assessment:** The deliverable covers all claimed content (14 patterns, 3 classification dimensions, C1–C7 matrix, evidence gap map, downstream reference index, practitioner guidance summary, PS integration). Navigation table is present (H-23 PASS). All sections are populated.

**SR-001: No version history for the 12-level hierarchy source (barrier-1/synthesis.md AGREE-5)**

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | Origin and Scope Disclosure |
| **Strategy Step** | Step 1 (Completeness) |

**Evidence:** The Origin and Scope Disclosure states the hierarchy is from "barrier-1/synthesis.md AGREE-5" but does not specify the version of barrier-1/synthesis.md (which is described elsewhere as "R4, 0.953 PASS"). The frontmatter identifies the input as "R4, 0.953 PASS" but this is only in the very top of the document. A reader of the Origin section alone cannot determine which revision of the hierarchy they are relying on.

**Recommendation:** Add "(R4, 0.953 PASS, 2026-02-27)" to the AGREE-5 reference in the Origin and Scope Disclosure section so the epistemic status of the foundational hierarchy is fully traceable from the section that mandates traceability.

---

### Step 2: Internal Consistency Check

**Assessment:** The document is largely internally consistent. Three specific inconsistencies are identified.

**SR-002: NPT-012 Hierarchy Rank "10 (extended)" Is Ambiguous Relative to NPT-010 "10"**

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | NPT-012 entry; Full Pattern Cross-Reference Matrix |
| **Strategy Step** | Step 2 (Consistency) |

**Evidence:** NPT-010 is assigned Rank 10 and NPT-012 is assigned Rank "10 (extended)." The Full Pattern Cross-Reference Matrix shows NPT-012 at "10 ext" in the Hierarchy Rank row. The C1–C7 Condition Alignment Matrix assigns NPT-012 to C7 (Full framework) not to a standalone rank 10 condition, which suggests NPT-012 does not occupy rank 10 independently. However, the C1–C7 table describes C4 as mapping to NPT-010 (rank 10), implying NPT-010 is the rank-10 canonical entry and NPT-012 is an extension of it. The taxonomy does not explicitly state that "extended" rank designations are not independently occupying the same rank as another pattern.

**Recommendation:** Add a clarifying note in the taxonomy's hierarchy description (before the pattern catalog) stating that "extended" rank designations (NPT-012, NPT-013) represent mechanism extensions of existing patterns, not independent positions in the 12-level hierarchy. NEVER present "10 (extended)" as a 13th or 14th level in the hierarchy.

---

**SR-003: Evidence Tier B Table Describes "T2" as "Absorbed into T4" But T2 Still Appears as a Named Tier**

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | Dimension B: Evidence Tier table (lines 99–108) |
| **Strategy Step** | Step 2 (Consistency) |

**Evidence:** The Dimension B table includes a T2 row ("Established practitioner | Published vendor documentation from major AI providers | None (absorbed into T4 in this taxonomy)"). The T2 tier is named but contains no patterns and is stated as absorbed into T4. However, the Evidence Gap Map does not include a T2 column or acknowledge T2 exists. The Practitioner Guidance Summary uses T4 for vendor documentation throughout. Having a named tier with "None" assignments creates a navigational inconsistency: a reader checking a pattern's tier against Dimension B will find T2 listed as a tier but will never encounter it in any pattern's "Evidence Tier" field.

**Recommendation:** Either remove T2 from the Dimension B table with a note that it was merged into T4 for this taxonomy's purposes, or retain it with an explicit cross-reference explanation of why the merger was made. NEVER present a named tier with no assigned patterns without an explicit merger/consolidation note adjacent to the tier definition.

---

### Step 3: Methodological Rigor Check

**Assessment:** The Braun & Clarke (2006) thematic analysis methodology claim in the frontmatter is stated but not operationalized. The taxonomy describes its method as "Extension of 12-level effectiveness hierarchy (AGREE-5); IG-002 taxonomy integration; Braun & Clarke (2006) thematic analysis." However, no section of the document describes how the Braun & Clarke methodology was applied in practice to generate the 14 patterns. The patterns appear to derive from the AGREE-5 hierarchy and IG-002 taxonomy, with Braun & Clarke serving as a generic methodological reference rather than a traceable analytical procedure.

**SR-004: Braun & Clarke Methodological Claim Is Unoperationalized**

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | Frontmatter (line 5); no corresponding section in document |
| **Strategy Step** | Step 3 (Methodological rigor) |

**Evidence:** Frontmatter states "Methodology: Extension of 12-level effectiveness hierarchy (AGREE-5); IG-002 taxonomy integration; Braun & Clarke (2006) thematic analysis." Braun & Clarke (2006) is a six-phase thematic analysis methodology requiring: (1) data familiarization, (2) initial code generation, (3) theme search, (4) theme review, (5) theme definition/naming, (6) report production. None of these phases are described, cited, or evidenced in the document. The document's taxonomy emerges directly from the AGREE-5 hierarchy and IG-002 types — the patterns are named by their position in a pre-existing hierarchy, not discovered through inductive thematic analysis.

**Analysis:** Citing Braun & Clarke as methodology when the taxonomy is actually deductive (starting from AGREE-5 and IG-002 frameworks) creates a methodological misrepresentation. Deductive taxonomy extension is a legitimate method, but it is not thematic analysis. This matters for Phase 5 validation because an externally validated thematic analysis would carry different epistemological status than framework-extension taxonomy.

**Recommendation:** Replace "Braun & Clarke (2006) thematic analysis" in the frontmatter with an accurate description: "Deductive framework extension from AGREE-5 hierarchy and IG-002 vendor taxonomy." NEVER cite Braun & Clarke if the methodology does not follow the six phases of thematic analysis. Add a brief "Methodology" subsection to the Origin and Scope Disclosure explaining that patterns derive from deductive classification against pre-existing frameworks, not inductive theme discovery.

---

### Step 4: Evidence Quality Check

**Assessment:** Evidence quality is generally strong. The T1/T4 distinction is consistently applied. One quality issue identified.

**SR-005: A-23 Citation Venue Inconsistency**

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | NPT-005 entry (Evidence Base); NPT-006 entry (comparison reference) |
| **Strategy Step** | Step 4 (Evidence quality) |

**Evidence:** NPT-005 cites "A-23 (Barreto & Jana, EMNLP 2025 Findings, T1, confirmed: ACL Anthology 2025.findings-emnlp.761)." This citation includes both a year (2025) and a venue (EMNLP 2025 Findings). However, the document frontmatter cites "barrier-1/synthesis.md (R4, 0.953 PASS)" as source, and comparative-effectiveness.md is cited as the confirmation source ("Confirmed T1 in I5 of comparative-effectiveness.md"). The citation appears internally consistent but a downstream researcher attempting to verify the ACL Anthology identifier "2025.findings-emnlp.761" would need to validate this against the actual Anthology record. NEVER present an ACL Anthology identifier as confirmed without the actual verification step being documented.

**Recommendation:** The citation as presented is acceptable if it was verified against comparative-effectiveness.md. Add an explicit note "(ACL Anthology identifier verified against comparative-effectiveness.md I5)" to make the verification provenance clear. This is a Minor issue because the finding that the study is T1-evidenced and its scope (negation accuracy) is correctly disclosed.

---

## S-007 Constitutional AI Critique

**Finding Prefix:** CC
**Protocol:** Per s-007-constitutional-ai.md — evaluate constitutional compliance and governance constraint adherence

### Evaluation Against Jerry Constitution / Quality-Enforcement Rules

**CC-001: P-001 (Truth/Accuracy) — Potential Accuracy Issue in NPT-007 Entry**

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | NPT-007 entry; Pattern ID field |
| **Strategy Step** | Constitutional compliance check |

**Evidence:** NPT-007 is titled "Blunt-Prohibition Baseline Acknowledgment" and its header states "**Hierarchy Rank:** 12 (lowest position — worst-performing)" and "**Technique Type:** A1 (Prohibition-only)." However, the IG-002 Integration section assigns NPT-007 the IG-002 Type: "Type 1 (Naive blunt prohibition) — REFERENCE ENTRY." The Full Pattern Cross-Reference Matrix (line 794) lists NPT-007/014 together in a single column. The Evidence Gap Map (line 773) also combines them: "NPT-007 | Blunt-Prohibition Baseline." Yet NPT-007's header Hierarchy Rank says "12 (lowest position — worst-performing)" while NPT-014's entry header also says "Hierarchy Rank: 12 (lowest — most-studied, worst-performing)." Both entries claim rank 12.

The issue: The taxonomy lists NPT-007 as both distinct from NPT-014 (they have separate entries, separate Pattern IDs) AND identical to NPT-014 (NPT-014 explicitly states it equals NPT-007). The Full Pattern Cross-Reference Matrix combines them into one column. This creates a P-001 accuracy concern because the two entries simultaneously represent the taxonomy as having 14 distinct patterns while two of those patterns explicitly represent the same phenomenon.

**Analysis:** This is not a Critical finding (the equivalence is disclosed), but it creates an accuracy tension: the "14 patterns" claim implies 14 distinct techniques, yet two of the 14 explicitly describe the same technique from different analytical angles. A downstream Phase 4 team relying on "14 patterns" as a coverage metric would be misled.

**Recommendation:** In the L0 Executive Summary "Total patterns cataloged: 14" statement, add a parenthetical clarification: "(Note: NPT-007 and NPT-014 describe the same blunt prohibition behavior from two analytical perspectives — observational baseline and diagnostic anti-pattern — and are double-counted in this total. The taxonomy contains 13 distinct technique types.)" NEVER present 14 as the count of distinct techniques without this disambiguation.

---

**CC-002: H-23 (Navigation Table Completeness) — Revision Log Section Missing from Navigation Table**

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | Document Sections navigation table (lines 11–26); Revision Log section (line 969) |
| **Strategy Step** | Constitutional compliance check |

**Evidence:** The Document Sections navigation table lists sections including "PS Integration" and "Self-Review Checklist" but does NOT include the "Revision Log" section (line 969). The Revision Log is a distinct `##`-level section at the bottom of the document. H-23 requires all `##` headings to be listed in the navigation table (NAV-004 coverage standard).

**Recommendation:** Add `| [Revision Log](#revision-log) | Version history and changes |` to the Document Sections navigation table.

---

**CC-003: P-022 (No Deception) — Confidence Score 0.87 Without Disclosure in L0 Summary**

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | L0 Executive Summary; PS Integration session_context (line 938) |
| **Strategy Step** | Constitutional compliance check |

**Evidence:** The PS Integration section discloses the synthesizer's self-assessed confidence as 0.87 with an explicit rationale: "Set below HIGH (0.90) because the 12-level hierarchy is an internally generated synthesis narrative." However, the L0 Executive Summary does not reference this confidence level. A consumer reading only the L0 section receives no signal that the producing agent assessed its own confidence at 0.87 rather than >= 0.90. Per P-022 (NEVER deceive about capabilities or confidence), the self-assessed confidence should be visible at the L0 summary level where most stakeholder consumption occurs.

**Recommendation:** Add a single sentence to the L0 Executive Summary: "Self-assessed confidence (synthesizer): 0.87 (below HIGH threshold) due to internally generated hierarchy; adversary gate required." NEVER present taxonomy coverage statistics in the L0 without co-locating the confidence level that the producing agent assigned to the work.

---

## S-002 Devil's Advocate

**Finding Prefix:** DA
**Protocol:** Per s-002-devils-advocate.md — challenge core assumptions, construct strongest counter-arguments
**H-16 Compliance:** S-003 Steelman executed above. H-16 constraint satisfied.

### Core Assumptions Targeted

**DA-001: The 12-Level Hierarchy Is a Sufficient Scaffolding for a Research Taxonomy**

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Section** | Origin and Scope Disclosure; all pattern entries |
| **Strategy Step** | Step 2 (Core assumption challenge) |

**Evidence:** The entire taxonomy's rank ordering derives from the AGREE-5 hierarchy produced by barrier-1/synthesis.md. The Origin and Scope Disclosure correctly states this hierarchy "has NOT been: Reviewed by independent prompting researchers outside this research pipeline; Validated by a controlled ranking study comparing techniques head-to-head; Assessed against any external taxonomy framework." The taxonomy then uses this hierarchy as the primary organizing principle for 14 pattern entries, each assigned a rank position that implies relative effectiveness.

**Devil's Advocate argument:** A taxonomy built on an internally generated, unvalidated ranking hierarchy inherits the hierarchy's ordering as authoritative structure despite explicitly disclaiming its validity. When NPT-009 is described throughout the document as being at "rank 9" and NPT-010 at "rank 10," and when these ranks directly inform the C1–C7 condition mapping (C3 → rank 9 pattern, C4 → rank 10 pattern), the ordering is operationally treated as meaningful for experimental design regardless of the disclaimers. Phase 2 experimental design choices (which condition maps to which rank) are constrained by a hierarchy that has not been externally validated. A Phase 5 experimenter who discovers the rank ordering was arbitrary would need to redesign the experimental conditions.

**Counter to self-review claim:** The self-review checklist PASS on "Phase 3 Gate Check 2" confirms the C1–C7 mapping is preserved, but does NOT evaluate whether the C1–C7 mapping is itself defensible given the hierarchy's epistemic status. The mapping is preserved from an equally internally-generated source (TASK-005).

**Analysis:** This is Critical because it concerns the foundational validity of the taxonomy's organizing structure, not just a presentation issue. If the 12-level hierarchy's rank ordering is arbitrary within the 5–11 range, then the C1–C7 condition mapping (which maps specific conditions to specific rank positions) inherits that arbitrariness, potentially undermining Phase 5's experimental design validity.

**Recommendation:** Add a section (or expand Origin and Scope Disclosure) that explicitly addresses what would change in the C1–C7 mapping if the rank ordering within ranks 5–11 were revised following external validation. NEVER present the C1–C7 experimental conditions as validated by the taxonomy without acknowledging that the rank ordering they depend on is an internally generated synthesis artifact. This does not invalidate the current mapping but requires disclosure that the mapping would need to be reassessed if external validation produces a different ordering.

---

**DA-002: T4 "HIGH Observational Confidence" Overstates Epistemological Status**

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | NPT-009 through NPT-013 confidence labels; Dimension B Evidence Tier table |
| **Strategy Step** | Step 2 (Core assumption challenge) |

**Evidence:** The taxonomy assigns "HIGH observational" confidence to NPT-009, NPT-012, and NPT-013 based on T4 evidence. The justification is direct observation of production systems (Anthropic's 33 NEVER/MUST NOT instances). "HIGH" is used as a confidence label for observational strength — the claim being evaluated is "does this pattern appear in production systems?" (answer: yes, HIGH confidence).

**Devil's Advocate argument:** Using "HIGH" as a confidence label, even with the qualifier "observational," creates an implicit hierarchy that may mislead downstream consumers. When NPT-009 has "HIGH obs/LOW causal" confidence and NPT-005 (T1-evidenced) has "MEDIUM" confidence, the pattern of labels implies that observational patterns (T4) can have comparable or higher confidence than T1-evidenced patterns. The explanation is that NPT-009's observational claim is different in kind from NPT-005's causal claim — but this requires careful reading to understand. A downstream Phase 4 practitioner scanning confidence labels may prioritize NPT-009 (HIGH) over NPT-005 (MEDIUM) without understanding that these HIGH and MEDIUM labels measure different claims against different evidence standards.

**Analysis:** The confidence labels are internally coherent but potentially misleading across-pattern comparisons. The taxonomy should not present a single "Confidence Level" field that mixes observational confidence (for T4 patterns) and causal confidence (for T1 patterns) without explicit disambiguation at the point of use in each entry.

**Recommendation:** Rename the field in each T4 pattern entry from "Confidence Level: HIGH observational / LOW causal" to "Observational Confidence: HIGH | Causal Confidence: LOW" as two separate fields. NEVER present a single "Confidence Level" field that aggregates both types without making the distinction structurally visible rather than lexically distinguishable. Alternatively, add a Confidence Label Key at the top of the Pattern Catalog Entries section explaining the two-dimensional confidence scheme.

---

**DA-003: The Taxonomy Claims Orthogonality for Classification Dimensions That Are Not Orthogonal**

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | Taxonomy Classification Dimensions introduction (line 85–86); Dimension A table |
| **Strategy Step** | Step 3 (Evidence scrutiny) |

**Evidence:** Line 85–86 states: "The taxonomy organizes all 14 negative prompting patterns across three orthogonal classification dimensions. Any pattern can be located by any combination of these three dimensions." However, Dimension A (Technique Type) and Dimension B (Evidence Tier) are NOT orthogonal in the sense that all combinations are possible. NPT-014 (A1: Prohibition-only) is T1-evidenced; NPT-013 (A4: Enforcement-tier) is T4-evidenced. But no A6 (Training-time constraint) pattern has T4 evidence, and no A7 (Meta-prompting) pattern has T4 evidence. The combinations are constrained by the nature of the techniques: training-time constraints require academic study settings to evaluate (biasing toward T1/T3), while production-observed patterns are by definition T4. The dimensions are correlated, not orthogonal.

Additionally, SM-003 (identified in S-003) already noted NPT-010's assignment to both A3 and A4 types. If a pattern can occupy multiple Dimension A types simultaneously, the dimensions are not strictly orthogonal partitions.

**Analysis:** "Orthogonal" implies any combination of dimension values is possible and meaningful. This is not the case for the three dimensions presented. The claim of orthogonality is methodologically inaccurate and could mislead Phase 4 analysts who attempt cross-dimensional queries expecting complete combinatorial coverage.

**Recommendation:** Replace "three orthogonal classification dimensions" with "three classification dimensions that provide independent analytical perspectives." NEVER claim orthogonality for classification dimensions unless all combinations of dimension values are populated or their absence is systematically explained. Add a note that some dimension combinations are structurally impossible (e.g., training-time techniques cannot have T4 production observation evidence) and that "any pattern can be located by any combination" should be read as "any pattern has a value in each dimension," not "any combination of dimension values is instantiated in the catalog."

---

## S-004 Pre-Mortem Analysis

**Finding Prefix:** PM
**Protocol:** Per s-004-pre-mortem.md — imagine the taxonomy has failed; enumerate failure scenarios

### Failure Scenario Enumeration

**PM-001: Phase 4 Consumers Misapply NPT-009 to Systems That Have Never Had Negative Constraints**

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | Downstream Reference Index; NPT-009 entry |
| **Strategy Step** | Step 2 (Failure scenario enumeration) |

**Evidence:** The Downstream Reference Index (lines 810–825) maps Phase 4 tasks to pattern IDs. The entry "Audit existing HARD rules for anti-pattern instances" → "NPT-014 as diagnostic filter" is correct. But the following entries assume the Jerry Framework already has structured negative constraints and the task is to upgrade or assess them. No entry addresses the scenario where a Phase 4 analyst uses the taxonomy to INTRODUCE new negative constraints in Jerry systems that currently have only positive framing. NPT-009's "When to use" section says "use when behavioral compliance is a critical requirement" without any guidance on the comparative analysis question: when should negative framing be introduced where it doesn't exist, versus when should existing positive framing be preserved?

**Analysis:** Phase 4 analysis will encounter both retrospective (existing constraints to assess) and prospective (new constraint design decisions) use cases. The taxonomy's Downstream Reference Index only addresses the retrospective case. A Phase 4 analyst making prospective constraint design decisions has no guidance from the taxonomy on when to introduce NPT-009 framing vs. when to preserve positive framing, because this is the UNTESTED central question. The taxonomy should explicitly acknowledge this limitation for prospective use.

**Recommendation:** Add a row to the Downstream Reference Index for "Design NEW constraints (no prior constraint exists)": reference NPT-009 as the pattern with a caveat that UNTESTED comparative evidence means the taxonomy CANNOT guide the positive-vs-negative choice for new constraint design; this decision is reserved for Phase 5 experimental results. NEVER present the Downstream Reference Index as a complete decision guide for Phase 4 without acknowledging its retrospective-only applicability.

---

**PM-002: The Taxonomy Becomes a De Facto Standard Cited Beyond Its Research Scope**

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | L0 Executive Summary; Origin and Scope Disclosure |
| **Strategy Step** | Step 2 (Failure scenario) |

**Evidence:** The taxonomy will be cited by Phase 4 and Phase 5 documents as "the PROJ-014 negative prompting taxonomy." As the taxonomy persists and is referenced, subsequent PROJ-014 documents may omit the epistemological limitations stated in the Origin and Scope Disclosure, treating pattern entries as established classification rather than a first-pass synthesis. The Phase 5 Experimental Design document (TASK-010 or downstream) may reference "NPT-009 (rank 9, T4 evidence)" without restating the H-obs/LOW-causal caveat. Over time, the internally-generated hierarchy ordering could acquire the appearance of empirical validation through citation accumulation within the project.

**Analysis:** This is a structural integrity failure mode for the research pipeline: epistemological caveats degrade through downstream citation. The taxonomy currently contains these caveats but does NOT include a mechanism to ensure they propagate to downstream documents.

**Recommendation:** Add a "Citation Requirements" subsection to the Origin and Scope Disclosure or PS Integration section specifying that any downstream document citing this taxonomy MUST co-cite the epistemological status of the cited pattern's evidence tier and confidence level. Specifically: "NEVER cite an NPT pattern ID without co-citing its Evidence Tier and Confidence Level fields." This is a MUST NOT constraint that should be placed prominently for downstream agent consumption.

---

**PM-003: The Evidence Gap Map Omits Phase 5 Experimental Coverage for NPT-007/NPT-014**

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | Evidence Gap Map; Phase 5 Priority column |
| **Strategy Step** | Step 2 (Failure scenario) |

**Evidence:** The Evidence Gap Map assigns Phase 5 Priority to each pattern. NPT-007 receives "HIGH — best-evidenced underperformance" and NPT-014 receives "HIGH — C2 baseline condition." Both are described as the same phenomenon (NPT-014 = NPT-007 formalization). The Phase 5 Priority column therefore assigns "HIGH" twice to the same underlying comparison (C2 baseline). This double-counting may cause Phase 5 experimental designers to overallocate resources to the blunt-prohibition baseline condition, treating it as two high-priority items when it represents one experimental condition.

**Recommendation:** Merge the Phase 5 Priority for NPT-007 and NPT-014 into a single cross-referenced entry, or add a note to the Evidence Gap Map that NPT-007 and NPT-014 correspond to the same Phase 5 experimental condition (C2) and should be treated as a single experimental priority.

---

## S-012 FMEA

**Finding Prefix:** FM
**Protocol:** Per s-012-fmea.md — identify failure modes, effects, and criticality for key taxonomy components

### Critical Components Analyzed

**FM-001: Evidence Tier Distinction Failure Mode**

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Section** | NPT-005 entry; Evidence Tier B table; Full Pattern Cross-Reference Matrix |
| **Strategy Step** | FMEA component analysis |

**Evidence:** The Full Pattern Cross-Reference Matrix (lines 792–806) includes a row "Min. evidence tier" that assigns values to each pattern. NPT-005 is listed as "T1" in this row. NPT-007/014 is listed as "T1." However, NPT-005's T1 evidence is explicitly scope-constrained to negation reasoning accuracy (A-23), while NPT-007/014's T1 evidence establishes underperformance — a different claim. The cross-reference matrix presents these as both "T1" without any scope differentiation.

**Failure mode:** A Phase 4 analyst using the cross-reference matrix as a quick-reference tool (the intended use case for a cross-reference matrix) would conclude that NPT-005 and NPT-007/014 have equal T1 evidence strength, when in fact NPT-005's T1 evidence addresses a different construct than NPT-007/014's T1 evidence. The scope constraint ("negation accuracy, NOT hallucination rate") is present in NPT-005's individual entry but absent from the cross-reference matrix.

**Effects:** Phase 4 analysts making evidence-based design decisions using the cross-reference matrix alone would systematically overestimate NPT-005's evidence quality for applications beyond negation accuracy tasks. This directly undermines the taxonomy's central contribution (evidence tier stratification).

**Criticality:** Critical because the cross-reference matrix is explicitly designed as a lookup tool. If the lookup tool misrepresents evidence quality, the taxonomy's primary practical value (evidence-based pattern selection) is compromised.

**Recommendation:** Add a "T1 Scope" row to the Full Pattern Cross-Reference Matrix that specifies the construct being evidenced at T1 for each pattern with T1 evidence. Alternatively, replace "T1" in the Min. Evidence Tier row with "T1-scope-limited" for patterns where the T1 evidence is construct-specific. NEVER present a cross-reference matrix that strips evidence scope constraints from T1 citations.

---

**FM-002: Context Compaction Risk Assessment Is Inconsistent Across Entries**

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | Full Pattern Cross-Reference Matrix row "Context compaction risk?"; NPT-006 entry |
| **Strategy Step** | FMEA failure mode analysis |

**Evidence:** The Full Pattern Cross-Reference Matrix lists "Context compaction risk?" for NPT-005 through NPT-013. NPT-006 (Atomic Constraint Decomposition) is assigned "Low" context compaction risk. However, NPT-006's technique involves deploying multiple atomic sub-constraints in a prompt (e.g., "CONSTRAINT 1... CONSTRAINT 2... CONSTRAINT 3..."). In long-context sessions, multiple individually stated constraints are at least as vulnerable to compaction as a single NEVER rule, and potentially more vulnerable because each constraint is a shorter, more compact statement that may be prioritized for compression. The rationale for "Low" context compaction risk for NPT-006 is not explained in NPT-006's individual entry (which does not mention context compaction at all under Known Limitations).

**Analysis:** The context compaction risk assignments in the cross-reference matrix appear to be applied without consistent methodology. NPT-009 (single NEVER rule with consequence) is "HIGH" risk, but NPT-006 (multiple CONSTRAINT statements) is "Low" risk — yet both are prompt-level declarative instructions subject to the same compaction mechanism. This inconsistency means Phase 4 cannot rely on the compaction risk column as a reliable guide for long-context deployment decisions.

**Recommendation:** Add an explicit rationale for each "Low" context compaction risk assignment in the cross-reference matrix, or add a footnote to the row explaining the methodology for risk assignment. For NPT-006 specifically, revisit whether multiple atomic sub-constraints are genuinely lower compaction risk than single NEVER rules, and update the NPT-006 Known Limitations section if the assessment changes. NEVER assign compaction risk ratings without traceable methodology.

---

**FM-003: The Downstream Reference Index Does Not Address Multi-Pattern Interactions**

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | Downstream Reference Index (lines 810–825) |
| **Strategy Step** | FMEA dependency analysis |

**Evidence:** The Downstream Reference Index maps Phase 4 tasks to individual pattern IDs. Multiple entries recommend combining patterns (e.g., "NPT-009 + NPT-012" for L2-REINJECT evaluation, "NPT-010 + NPT-011 + NPT-012 + NPT-013" for full framework assessment). However, no entry in the index addresses the interaction effects between patterns applied simultaneously. When NPT-009 (consequence documentation) and NPT-011 (justification) and NPT-012 (re-injection) are all present in the same rule, do they interact additively, multiplicatively, or with potential conflict? The taxonomy acknowledges these combinations in individual pattern "Relationship to Other Patterns" sections but does not provide interaction effect guidance at the index level.

**Recommendation:** Add a note to the Downstream Reference Index header stating that pattern combination effects are not characterized by this taxonomy and that Phase 4 analysis should treat multi-pattern assessments as requiring judgment, not derivable from additive combination of individual pattern evidence levels. NEVER present multi-pattern combinations in the index as if their combined effect is predictable from component evidence tiers.

---

## S-013 Inversion Technique

**Finding Prefix:** IN
**Protocol:** Per s-013-inversion.md — what would guarantee failure? Invert to find what is missing.

### Inversion Analysis: What Would Guarantee Phase 4 Misapplication?

**IN-001: Suppress the Evidence Scope Constraints on Every Pattern Consumption**

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Section** | All T1-evidenced pattern entries; Cross-Reference Matrix |
| **Strategy Step** | Step 2 (Failure inversion) |

**Evidence:** The taxonomy's most important protective mechanism against misapplication is the per-pattern scope constraint: A-23 measures negation accuracy (not hallucination rate), A-15 measures compliance (not hallucination rate), A-20 establishes underperformance of Type 1 (not equivalence of Types 2–4). Every critical misapplication scenario involves a consumer stripping these scope constraints when citing a pattern.

**Inversion finding:** The taxonomy relies entirely on in-entry scope constraints to prevent misapplication. No structural mechanism prevents a downstream Phase 4 document from citing "NPT-005 (T1, EMNLP 2025)" without the A-23 scope caveat. The document structure places scope constraints within individual entries but does not surface them at the level of the cross-reference matrix or downstream reference index — the two lookup tools most likely to be consumed without full-entry reading.

**Analysis:** This is Critical because the taxonomy's central intellectual contribution (avoiding premature causal claims) is structurally vulnerable to the most predictable downstream failure mode (citation without scope context). The taxonomy provides the correct information in the right places within full entries, but the summary artifacts (matrices, index) strip scope context.

**Recommendation:** NEVER present the Full Pattern Cross-Reference Matrix or Downstream Reference Index as standalone lookup tools without a header warning: "NEVER cite evidence from this matrix without reading the full pattern entry for scope constraints. T1 labels in this matrix are scope-limited; see individual entries for construct specifications." Add this warning to both tables.

---

**IN-002: Remove the "UNTESTED" Labels from Ranks 9–11 and Replace with "T4 Observed"**

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | NPT-009 through NPT-011 confidence labels; Dimension B table |
| **Strategy Step** | Step 2 (Failure inversion — what would mislead?) |

**Evidence:** The taxonomy currently distinguishes between "T4 observed" (what evidence tier exists) and "UNTESTED" (no controlled comparison exists). This is a critical distinction: T4 evidence exists FOR NPT-009's observational claim (that the pattern is used in production), but the COMPARISON claim (that NPT-009 outperforms equivalent positive framing) is untested. If a downstream document replaces "UNTESTED" with "T4" in any context where the comparison claim is implied, it creates the exact misrepresentation the taxonomy is designed to prevent.

**Analysis:** The UNTESTED label appears in the Evidence Gap Map "Untested (controlled)" column and in individual pattern entries. However, the Full Pattern Cross-Reference Matrix shows "Min. evidence tier: T4" for NPT-009 through NPT-013. A reader of the cross-reference matrix alone would see "T4" and might not recognize that "T4" refers to the observational claim, not the comparative claim. The UNTESTED label for the comparative claim appears ONLY in the Evidence Gap Map and in-entry Known Limitations, not in the cross-reference matrix.

**Recommendation:** Add a row to the Full Pattern Cross-Reference Matrix: "Causal comparison tested?" with values: NPT-005 = "Yes (negation accuracy)", NPT-006 = "Yes (compliance)", NPT-007/014 = "Yes (underperformance)", NPT-008 through NPT-013 = "No — UNTESTED." This row surfaces the UNTESTED status in the lookup tool where the misrepresentation risk is highest.

---

## S-011 Chain-of-Verification

**Finding Prefix:** CV
**Protocol:** Per s-011-cove.md — generate questions, verify factual claims systematically

### Verification Questions and Results

**Claim 1: "A-23 (Barreto & Jana, EMNLP 2025 Findings, T1, confirmed: ACL Anthology 2025.findings-emnlp.761)"**

Verification: The taxonomy states this was "Confirmed T1 in I5 of comparative-effectiveness.md." The verification depends on the integrity of the comparative-effectiveness.md source. Accept as provisionally confirmed per the research pipeline's internal verification (comparative-effectiveness.md R5, 0.933 max-iter PASS).

Result: UNVERIFIABLE externally; internally cited as verified. **Status: ACCEPT with caveat.**

---

**Claim 2: "33 NEVER/MUST NOT instances across 10 Claude Code rule files"**

Verification: This claim appears in NPT-009 Evidence Base and is the foundation for the T4 "HIGH observational" confidence designation. The source is "VS-001 (T4, direct observation)" from supplemental-vendor-evidence.md.

**CV-001: Vendor Self-Practice Count Is Not Verifiable in This Document**

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | NPT-009 Evidence Base; L0 Summary line 140 |
| **Strategy Step** | Claim verification |

**Evidence:** The "33 NEVER/MUST NOT instances across 10 Claude Code rule files" claim is stated in NPT-009 and in the IG-002 Integration section (line 140). The taxonomy sources this to VS-001 (T4, direct observation) from supplemental-vendor-evidence.md. However, this document does not contain or reference the raw count data or the rule files themselves. A verifier relying solely on this taxonomy cannot confirm whether the count is 33 or some other number, or whether "10 rule files" is accurate.

**Analysis:** T4 observational claims depend on the accuracy of the observation record. If supplemental-vendor-evidence.md's count is incorrect, the "33 instances" figure propagates to this taxonomy and downstream Phase 4 documents. The taxonomy does not indicate whether the count was independently verified within the research pipeline.

**Recommendation:** Add a note to VS-001 references stating the count was taken from supplemental-vendor-evidence.md without independent re-verification within this synthesis. This is a Minor issue because T4 evidence by definition is observational and the taxonomy correctly does not claim T1 status for this count.

---

**Claim 3: "Phase 3 Gate Check 1 — PASS: taxonomy does NOT imply directional verdict at ranks 9–11"**

Verification against document:
- L0 Summary line 34: "NEVER use this taxonomy to imply a directional verdict." ✓
- Origin section line 76: "NEVER implied a directional verdict not established by Phase 2." ✓
- NPT-009 Known Limitations: "NEVER claim NPT-009 is experimentally validated as superior to a structurally equivalent positive alternative." ✓
- NPT-010 When NOT to use: "NEVER treat NPT-010 as validated over NPT-009-only." ✓
- NPT-011 Known Limitations: "No T1 controlled comparison of justified vs. unjustified prohibition." ✓

**CV-002: One Pattern Entry Contains a Phrase That Approaches Implied Superiority**

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | NPT-010 "When to use" (line 525) |
| **Strategy Step** | GC-1 verification — directional verdict check |

**Evidence:** NPT-010 "When to use" states: "Use NPT-010 as the minimum viable pattern for any new behavioral constraint." The phrase "minimum viable pattern for any new behavioral constraint" implies that NPT-010 is the recommended baseline for new constraint design, which implicitly endorses negative framing over positive framing as the default for new constraints. This is not a controlled experimental conclusion — it reflects practitioner guidance from vendor evidence (AGREE-8, NP-002) — but for a constraint that is UNTESTED against positive equivalents, calling it "the minimum viable pattern for any new behavioral constraint" approaches a directional recommendation.

**Analysis:** This is a Minor issue because the "When to use" context is clearly practitioner guidance (not an experimental claim), and the AGREE-8 source is disclosed. However, the phrase creates tension with the taxonomy's repeated UNTESTED labels for NPT-010 and could be read as implying negative framing is the correct default for new constraint design, which contradicts the UNTESTED label.

**Recommendation:** Replace "Use NPT-010 as the minimum viable pattern for any new behavioral constraint" with "For practitioners already committed to negative framing, NPT-010 represents the minimum structural requirement — the UNTESTED comparison against equivalent positive framing means this guidance cannot be extended to the positive-vs-negative framing choice itself." NEVER use "minimum viable" language for patterns with UNTESTED causal status without the framing caveat.

---

**Claim 4: "C1–C7 pilot condition mapping PRESERVED — alignment verdict stated"**

Verification: C1–C7 Condition Alignment Matrix (lines 744–755) is present, populated, and explicitly states "Alignment verdict: PRESERVED." Each condition maps to at least one NPT pattern. No "Modification to Hierarchy?" column entry contains anything other than "None." GC-2 is PASS.

Result: **VERIFIED.**

---

**Claim 5: "Rank 12 distinguished from ranks 9–11 with confidence labels"**

Verification: NPT-007/NPT-014 confidence = "HIGH (for the finding that this pattern underperforms structured alternatives)." NPT-009 confidence = "HIGH observational / LOW causal." NPT-010/011 confidence = "MEDIUM." These are distinct labels. GC-3 is PASS.

Result: **VERIFIED.**

---

## S-001 Red Team Analysis

**Finding Prefix:** RT
**Protocol:** Per s-001-red-team.md — adversarial threat actor emulation
**H-16 Compliance:** S-003 Steelman executed. H-16 satisfied.

### Threat Actor Profile

**Goal:** Exploit the taxonomy to make premature claims about negative prompting effectiveness in Phase 4 or Phase 5 documents, specifically to justify implementation decisions that should await Phase 5 experimental validation.

**Capability:** Downstream Phase 4 agent with access to the taxonomy but limited time for deep reading; reliant on summary tables and cross-reference matrices rather than full pattern entries.

**Motivation:** Phase 4 analysis has deadlines and incentives to make actionable recommendations. The taxonomy provides named patterns with confidence labels that, if read selectively, could justify immediate implementation changes to the Jerry Framework.

### Attack Vector Inventory

**RT-001: Cross-Reference Matrix Exploitation (Ambiguity Exploitation)**

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Section** | Full Pattern Cross-Reference Matrix (lines 792–806) |
| **Strategy Step** | Attack Vector 1 — Ambiguity exploitation |

**Evidence:** The Full Pattern Cross-Reference Matrix is the highest-risk surface in the taxonomy for selective reading. It compresses 14 pattern entries into a single table with attributes like "Min. evidence tier" (showing T1, T3, T4) and "Use for enforcement tier?" (showing YES/NO). An adversarial reader (or a time-pressured Phase 4 agent) can extract from this matrix:
- NPT-009: T4 evidence, Use for enforcement tier = YES
- NPT-010: T4 evidence, Use for enforcement tier = YES (preferred)
- NPT-011: T4 evidence, Use for enforcement tier = YES

These three facts, extracted without scope constraints, would support an argument: "The taxonomy confirms NPT-009 through NPT-011 are appropriate for enforcement tier use (T4 evidence)." This argument would be technically accurate as stated (the taxonomy does confirm this) but would omit the critical UNTESTED status for causal comparison against positive equivalents.

**Exploitability:** HIGH — the cross-reference matrix is specifically designed as a quick-reference tool and will be the most-used section by time-pressured downstream agents.

**Defense gap:** PARTIAL — full pattern entries include UNTESTED labels, but the cross-reference matrix does not. The "NEVER cite without reading entry" warning recommended in IN-001 above does not yet exist in the document.

**Recommendation:** Add a bolded warning to the Full Pattern Cross-Reference Matrix header: "**NEVER use this matrix as a standalone decision guide. 'Use for enforcement tier?' reflects observational evidence only. UNTESTED causal comparison status for all rows marked T4 — see individual pattern entries.**" This is a P0 (Critical, Missing defense) finding requiring immediate mitigation.

---

**RT-002: Practitioner Guidance Summary Extraction (Rule Circumvention)**

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | Practitioner Guidance Summary (lines 840–848) |
| **Strategy Step** | Attack Vector 3 — Rule circumvention |

**Evidence:** The Practitioner Guidance Summary table (lines 840–848) provides five guidance items (PG-001 through PG-005) with confidence levels and evidence bases. PG-003 states: "Pair enforcement-tier constraints with consequences | T4 observational, MEDIUM — working practice, Phase 2 will assess causal contribution | VS-001–VS-004 | NPT-009 (consequence requirement)." A Phase 4 agent citing this guidance table could argue: "The taxonomy's practitioner guidance (PG-003, MEDIUM, T4) recommends pairing enforcement-tier constraints with consequences — this justifies implementing NPT-009 in the Jerry Framework."

This argument correctly extracts from the guidance summary but omits that "working practice" guidance (T4, MEDIUM) is not the same as experimentally validated guidance (T1, HIGH). The guidance is correctly labeled, but a downstream document could strip the confidence label when summarizing.

**Exploitability:** MEDIUM — requires deliberate or negligent misrepresentation of confidence levels.

**Defense gap:** PARTIAL — confidence labels are present in the table but are in a single column that could be omitted in downstream summarization.

**Recommendation:** Add to the Practitioner Guidance Summary table header: "NEVER extract these guidance items without co-citing the Confidence column. MEDIUM confidence items are working practice only and are NOT validated recommendations." This addresses the circumvention vector without removing useful guidance.

---

**RT-003: Degradation Path — ST-5 Constraints Lose Visibility in Long Research Chains**

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | Origin and Scope Disclosure; PS Integration |
| **Strategy Step** | Attack Vector 5 — Degradation paths |

**Evidence:** This taxonomy inherits epistemological constraints from three upstream documents (barrier-2/synthesis.md ST-5, TASK-005, barrier-1/synthesis.md AGREE-5). These constraints are stated in the Origin and Scope Disclosure. However, as the research pipeline progresses through Phase 4 and Phase 5, each downstream document will cite this taxonomy — not the upstream barrier-2/synthesis.md constraint source. The ST-5 constraints will become progressively harder to trace as they are cited via intermediaries.

**Exploitability:** HIGH over time — citation depth obscures epistemological provenance.

**Defense gap:** PARTIAL — current document preserves constraints, but no mechanism enforces downstream propagation.

**Recommendation:** Add a "Constraint Propagation Requirement" note to PS Integration: "NEVER cite NPT patterns from this taxonomy in downstream documents without restating the epistemological status of the underlying evidence. Phase 4 and Phase 5 documents MUST NOT cite NPT-009 through NPT-013 without the accompanying 'T4 observational, UNTESTED causal comparison' label."

---

## S-014 LLM-as-Judge Scoring

**Finding Prefix:** LJ
**Protocol:** Per s-014-llm-as-judge.md — dimensional scoring with 6-dimension rubric
**Threshold:** >= 0.95 (C4)

### Dimension Scores

#### Dimension 1: Completeness (Weight: 0.20)

**Assessment:** The taxonomy covers all 14 patterns, three classification dimensions, C1–C7 alignment, evidence gap map, downstream reference index, practitioner guidance, PS integration, and self-review checklist. Coverage of the 12-level hierarchy is complete. However:
- Rank 7 is unoccupied without explanation (SM-001)
- T2 tier is named but empty (SR-003)
- NPT-007/NPT-014 dual-entry overcounts distinct techniques (CC-001)
- Prospective constraint design guidance is absent (PM-001)

**Raw score:** 0.88 (strong coverage with identified gaps)

#### Dimension 2: Internal Consistency (Weight: 0.20)

**Assessment:** Generally consistent. Specific inconsistencies:
- NPT-010 appears in both A3 and A4 Dimension A type assignments (SM-003)
- NPT-012 "10 (extended)" rank is ambiguous relative to NPT-010 "10" (SR-002)
- "Orthogonal dimensions" claim is inaccurate (DA-003)
- Cross-reference matrix strips scope constraints present in full entries (FM-001, IN-001, IN-002)
- Braun & Clarke methodology claim conflicts with actual deductive approach (SR-004)

**Raw score:** 0.82 (multiple consistency issues identified, none individually fatal)

#### Dimension 3: Methodological Rigor (Weight: 0.20)

**Assessment:** The taxonomy's methodological approach (AGREE-5 extension + IG-002 integration) is sound for its stated purpose. The epistemological constraints are consistently applied. However:
- Braun & Clarke citation is methodologically inaccurate (SR-004 — MAJOR)
- Context compaction risk assignments lack consistent methodology (FM-002)
- Confidence label scheme mixes observational and causal confidence in a single field without structural disambiguation (DA-002)
- The 12-level hierarchy's validity as taxonomy scaffolding is not addressed for the prospective use case (DA-001)

**Raw score:** 0.83 (methodological framework is present and generally sound; specific rigor gaps identified)

#### Dimension 4: Evidence Quality (Weight: 0.15)

**Assessment:** Evidence tier stratification is the taxonomy's strongest dimension. T1/T4 distinction is carefully maintained throughout full pattern entries. Scope constraints are correctly applied to T1 citations. However:
- Cross-reference matrix strips evidence scope (FM-001 — CRITICAL for downstream use)
- A-23 venue confirmation depends on upstream document (SR-005)
- VS-001 "33 instances" count not independently verified (CV-001)

**Raw score:** 0.88 (strong within full entries; lookup artifacts weaken the guarantee)

#### Dimension 5: Actionability (Weight: 0.15)

**Assessment:** The Downstream Reference Index provides Phase 4 lookup by task type. Pattern entries include When to Use / When NOT to Use guidance. However:
- Prospective constraint design guidance is absent (PM-001 — MAJOR)
- Cross-reference matrix "Use for enforcement tier?" column loses scope context (RT-001 — CRITICAL)
- Multi-pattern interaction effects not addressed (FM-003)
- Citation requirements for downstream documents not specified (PM-002 — MAJOR)

**Raw score:** 0.80 (good retrospective guidance; prospective guidance absent; critical lookup artifact issue)

#### Dimension 6: Traceability (Weight: 0.10)

**Assessment:** Source citations are present throughout. Input sources listed in frontmatter. PS Integration worktracker linkage is complete. However:
- Origin section lacks version reference for barrier-1/synthesis.md (SR-001)
- Braun & Clarke citation does not trace to an applied procedure (SR-004)
- ST-5 constraint propagation to downstream documents is not enforced (RT-003, PM-002)

**Raw score:** 0.87 (strong within-document traceability; downstream propagation gap)

### Composite Score Calculation

| Dimension | Weight | Raw Score | Weighted Score |
|-----------|--------|-----------|---------------|
| Completeness | 0.20 | 0.88 | 0.176 |
| Internal Consistency | 0.20 | 0.82 | 0.164 |
| Methodological Rigor | 0.20 | 0.83 | 0.166 |
| Evidence Quality | 0.15 | 0.88 | 0.132 |
| Actionability | 0.15 | 0.80 | 0.120 |
| Traceability | 0.10 | 0.87 | 0.087 |
| **COMPOSITE** | **1.00** | — | **0.845** |

**Threshold:** >= 0.95 (C4)
**Result:** **REJECTED** (0.845 < 0.95) — Revision required per H-13

**Band:** REJECTED (< 0.85 threshold for "significant rework required" band — composite is 0.845, which is borderline between REJECTED and REVISE bands)

**Dimensional analysis:** Internal Consistency (0.82) and Actionability (0.80) are the two lowest-scoring dimensions. These drive the composite score below threshold. The Critical finding in FM-001 (cross-reference matrix strips evidence scope) and RT-001 (cross-reference matrix usable for premature causal claims) directly impact both Internal Consistency and Actionability scores.

---

## Consolidated Findings Summary

| ID | Severity | Source Strategy | Finding Summary | Section | Status |
|----|----------|----------------|----------------|---------|--------|
| SM-001 | Major | S-003 Steelman | Rank 7 unoccupied without explanation in 12-level hierarchy | NPT-008 entry; Origin section | Requires fix |
| SM-002 | Minor | S-003 Steelman | NPT-007/NPT-014 dual-entry rationale is under-explained in L0 | NPT-007, NPT-014, L0 | Requires fix |
| SM-003 | Minor | S-003 Steelman | NPT-010 assigned to both A3 and A4 Dimension A types — violates orthogonality claim | Dimension A table; NPT-010 entry | Requires fix |
| SR-001 | Minor | S-010 Self-Refine | Origin section lacks version reference for barrier-1/synthesis.md R4 | Origin and Scope Disclosure | Requires fix |
| SR-002 | Minor | S-010 Self-Refine | NPT-012 "Rank 10 (extended)" ambiguous relative to NPT-010 "Rank 10" | NPT-012 entry; Cross-Reference Matrix | Requires fix |
| SR-003 | Minor | S-010 Self-Refine | T2 tier named in Dimension B table but empty (absorbed into T4) without consistency | Dimension B table; Evidence Gap Map | Requires fix |
| SR-004 | Major | S-010 Self-Refine | Braun & Clarke thematic analysis cited but methodology is actually deductive framework extension | Frontmatter; Origin section | Requires fix |
| SR-005 | Minor | S-010 Self-Refine | A-23 venue confirmation depends on upstream document; verification provenance unclear | NPT-005 Evidence Base | Document |
| CC-001 | Major | S-007 Constitutional | NPT-007/NPT-014 dual-entry creates "14 patterns" count that overstates distinct technique count | L0 Executive Summary | Requires fix |
| CC-002 | Minor | S-007 Constitutional | "Revision Log" section absent from navigation table (H-23 violation) | Navigation table; Revision Log | Requires fix |
| CC-003 | Minor | S-007 Constitutional | Synthesizer confidence 0.87 not surfaced in L0 Summary (P-022 completeness) | L0 Executive Summary; PS Integration | Requires fix |
| DA-001 | Critical | S-002 Devil's Advocate | Internally-generated hierarchy used as experimental scaffolding without addressing prospective validity — operationally authoritative despite explicit disclaimers | Entire document structure; C1–C7 matrix | Requires fix |
| DA-002 | Major | S-002 Devil's Advocate | "HIGH observational" confidence label may mislead cross-pattern comparisons with T1 "MEDIUM" patterns | NPT-009, NPT-012, NPT-013 entries | Requires fix |
| DA-003 | Major | S-002 Devil's Advocate | "Orthogonal classification dimensions" claim is inaccurate — dimensions are correlated, not orthogonal | Taxonomy Classification Dimensions intro | Requires fix |
| PM-001 | Major | S-004 Pre-Mortem | Downstream Reference Index omits prospective constraint design use case (new constraints, not existing ones) | Downstream Reference Index | Requires fix |
| PM-002 | Major | S-004 Pre-Mortem | No citation requirements specified for downstream documents citing NPT patterns — epistemological caveats will degrade | Origin and Scope Disclosure; PS Integration | Requires fix |
| PM-003 | Minor | S-004 Pre-Mortem | NPT-007 and NPT-014 double-counted as "HIGH" priority in Evidence Gap Map Phase 5 column | Evidence Gap Map | Requires fix |
| FM-001 | Critical | S-012 FMEA | Cross-reference matrix strips T1 evidence scope constraints — "T1" in matrix misrepresents construct coverage | Full Pattern Cross-Reference Matrix | Requires fix |
| FM-002 | Major | S-012 FMEA | Context compaction risk ratings lack consistent methodology; NPT-006 "Low" rating is unexplained | Cross-Reference Matrix; NPT-006 entry | Requires fix |
| FM-003 | Minor | S-012 FMEA | Downstream Reference Index does not address multi-pattern interaction effects | Downstream Reference Index | Document |
| IN-001 | Critical | S-013 Inversion | Evidence scope constraints not surfaced in Cross-Reference Matrix or Downstream Reference Index — lookup tools are structurally vulnerable to scope stripping | Full Pattern Cross-Reference Matrix; Downstream Reference Index | Requires fix |
| IN-002 | Major | S-013 Inversion | "UNTESTED" label for comparative claim not present in Cross-Reference Matrix — T4 label alone misleads on causal status | Full Pattern Cross-Reference Matrix | Requires fix |
| CV-001 | Minor | S-011 Chain-of-Verification | "33 NEVER/MUST NOT instances" count not independently re-verified within this synthesis | NPT-009 Evidence Base; line 140 | Document |
| CV-002 | Minor | S-011 Chain-of-Verification | NPT-010 "minimum viable pattern for any new behavioral constraint" approaches implied superiority for UNTESTED pattern | NPT-010 When to use | Requires fix |
| RT-001 | Critical | S-001 Red Team | Cross-reference matrix exploitable for premature causal claims by time-pressured downstream agents — no warning present | Full Pattern Cross-Reference Matrix | Requires fix |
| RT-002 | Major | S-001 Red Team | Practitioner Guidance Summary extractable without confidence labels — downstream stripping risk | Practitioner Guidance Summary | Requires fix |
| RT-003 | Major | S-001 Red Team | ST-5 constraints have no downstream propagation enforcement mechanism | Origin and Scope Disclosure; PS Integration | Requires fix |

---

## Execution Statistics

- **Total Findings:** 27
- **Critical:** 4 (DA-001, FM-001, IN-001, RT-001)
- **Major:** 11 (SM-001, SR-004, CC-001, DA-002, DA-003, PM-001, PM-002, FM-002, IN-002, RT-002, RT-003)
- **Minor:** 12 (SM-002, SM-003, SR-001, SR-002, SR-003, SR-005, CC-002, CC-003, PM-003, FM-003, CV-001, CV-002 — FM-003 and CV-001 are "Document" only, not requiring structural change)
- **Protocol Steps Completed:** All 10 strategies executed; all steps completed within each strategy
- **S-014 Composite Score:** 0.845 (REJECTED — below 0.95 C4 threshold)
- **Phase 3 Gate Checks:** GC-1 PASS, GC-2 PASS, GC-3 PASS (all three Barrier 2 ST-5 requirements satisfied)
- **H-16 Compliance:** SATISFIED — S-003 executed before all critique strategies

### Priority Finding Matrix (P0 = Critical + Missing/Partial defense)

| Priority | Finding ID | Severity | Defense Status | Rationale |
|----------|-----------|----------|----------------|-----------|
| P0 | RT-001 | Critical | Missing | No warning on cross-reference matrix; primary exploitation surface |
| P0 | FM-001 | Critical | Missing | T1 scope constraints absent from cross-reference matrix |
| P0 | IN-001 | Critical | Missing | Scope constraints not in lookup tools; structurally vulnerable |
| P0 | DA-001 | Critical | Partial | Disclaimer present in Origin section but not addressed for prospective experimental validity |
| P1 | SR-004 | Major | Missing | Braun & Clarke citation not operationalized; methodological misrepresentation |
| P1 | DA-003 | Major | Missing | "Orthogonal" claim is inaccurate; no correction present |
| P1 | PM-002 | Major | Missing | No citation requirements for downstream documents |
| P1 | IN-002 | Major | Missing | "UNTESTED" label absent from cross-reference matrix causal column |
| P1 | DA-002 | Major | Partial | Confidence labels are present in entries but not structurally disambiguated |
| P1 | CC-001 | Major | Partial | Dual-entry disclosed in NPT-014 but not in L0 pattern count |

### Revision Guidance

The four Critical findings (RT-001, FM-001, IN-001, DA-001) MUST be addressed before this taxonomy is accepted. All four target the same structural vulnerability: summary artifacts (cross-reference matrix, downstream reference index) strip the epistemological constraints that full pattern entries correctly apply.

**The single highest-priority fix:** Add a prominent warning block to the Full Pattern Cross-Reference Matrix stating that "T1" labels in the matrix are scope-limited, "Use for enforcement tier?" reflects observational evidence only, and all T4 rows have UNTESTED causal comparison status. This single fix addresses RT-001, FM-001, and IN-001 simultaneously.

The second highest-priority fix: Address SR-004 (Braun & Clarke methodological claim) and DA-003 ("orthogonal" claim) as these both misrepresent the taxonomy's analytical basis in ways that affect external validity.

---

*adv-executor | TASK-009 | Barrier 3 | PROJ-014 | 2026-02-28*
*Strategy Set: C4 (S-001, S-002, S-003, S-004, S-007, S-010, S-011, S-012, S-013, S-014)*
*Deliverable: taxonomy-pattern-catalog.md v1.0.0*
*S-014 Score: 0.845 (REJECTED — revision required per H-13)*
*Phase 3 Gate Checks: GC-1 PASS | GC-2 PASS | GC-3 PASS*
*H-16: SATISFIED*
*Constitutional Compliance: P-003, P-020, P-022*
