# Adversarial Finding Report: ps-researcher-001 (Iteration 3)

> C4 Tournament | PROJ-014 | 2026-02-27
> Deliverable: research/academic-survey.md (Revision 3)
> Strategies executed: 10/10
> Prior score: 0.86 (REVISE)

---

## Execution Context

- **Strategy Set:** S-010, S-003, S-002, S-004, S-001, S-007, S-011, S-012, S-013, S-014
- **Template Directory:** `.context/templates/adversarial/`
- **Deliverable Path:** `projects/PROJ-014-negative-prompting-research/research/academic-survey.md`
- **Criticality:** C4 (Critical)
- **Quality Threshold:** >= 0.95
- **Iteration:** 3 of 5
- **Executed:** 2026-02-27
- **Prior Iteration Findings:** `agent-gates/ps-researcher-001-findings-iter2.md`

---

## Iteration 2 Finding Resolution Tracking

The following table assesses whether each finding from Iteration 2 was adequately addressed in Revision 3. Each claim is verified against the actual file content, not the researcher's self-reported resolution description.

### Major Findings (2 from Iteration 2)

| Finding ID | Original Issue | Resolution Status | Assessment |
|------------|----------------|-------------------|------------|
| SR-001-I2 | CAST included in "When Negative Prompting Works" — activation steering is not a prompting technique | RESOLVED | VERIFIED. "When Negative Prompting Works" (lines 39-46) now contains ONLY two prompt-level techniques: warning-based meta-prompting (Barreto/Jana) and atomic constraint decomposition (Ferraz/DeCRIM). CAST has been moved to a new dedicated "Model-Internal Approaches to Negative Constraints" subsection (lines 48-52) with an explicit disclaimer: "CAST is **not a prompting technique**" and "results cannot be reproduced through prompt engineering alone." L1 Source 28 Quality Notes state "Note: CAST is a model-internal activation steering technique, not a prompt engineering approach." L2 Source 28 categorized as "(c) Training/alignment constraints (mechanistic intervention -- not a prompt engineering technique)." This is a thorough, multi-layer resolution. ADEQUATE. |
| SR-002-I2 | Source 12 double-counted in Tier 1 (listed under both IJCAI and LLM@IJCAI); workshop conflated with main track | RESOLVED | VERIFIED. Source Quality Assessment (lines 554-561) now shows: Tier 1 = 13 unique sources (no Source 12); Tier 2 = 5 sources (now includes LLM@IJCAI'23 symposium: Source 12). The explanatory note (lines 561) distinguishes Source 1 (IJCAI main track, Tier 1) from Source 12 (LLM@IJCAI'23 symposium, Tier 2). The double-counting is eliminated. Tier counts are now internally consistent: 13 + 5 + 10 + 1 + 1 = 30. ADEQUATE. |

### Minor Findings (5 from Iteration 2)

| Finding ID | Original Issue | Resolution Status | Assessment |
|------------|----------------|-------------------|------------|
| SR-003-I2 | Document header "26 peer-reviewed or under review" overstated peer-review status | RESOLVED | VERIFIED. Header (line 4) now reads: "13 Tier 1 peer-reviewed + 4 Tier 2 peer-reviewed + 1 workshop/symposium peer-reviewed + 10 arXiv preprints + 1 rejected submission + 1 commercially-affiliated report." The count reconciles: 13 + 4 + 1 (workshop) = 18 peer-reviewed + 10 preprints + 1 rejected + 1 commercial = 30. The "under review" characterization is gone. ADEQUATE. Note: See new finding IT3-001 on arithmetic in the header. |
| CV-001-I2 | CAST "harmless acceptance at 97.8%" vs. "harmless refusal 2.20%" terminology inconsistency | RESOLVED | VERIFIED. L2 Source 28 (lines 453) now reads: "harmless refusal stayed at 2.20% (i.e., only 2.20% of harmless prompts were incorrectly refused; 97.8% of harmless prompts were correctly accepted)." L0 "Model-Internal Approaches" section (lines 51) uses: "harmless refusal stays at only 2.20% (i.e., 97.8% of harmless prompts are correctly accepted)." Both are now consistent and self-explanatory. ADEQUATE. |
| PM-001-I2 | 60% hallucination reduction claim origin remains uncited | RESOLVED | VERIFIED. PROJ-014 Hypothesis Context (lines 69-72) now states: "Despite extensive search, no specific vendor document, blog post, or practitioner publication could be identified as the origin of this figure. It appears to be an informal 'rule of thumb' circulating in practitioner communities (prompt engineering forums, internal vendor guidance, conference hallway discussions) without a single traceable published source." This is honest per P-022 and constitutes an acceptable resolution: the researcher genuinely cannot cite what does not exist. ADEQUATE. |
| CC-001-I2 | Header source classification inconsistency — P-022 concern | RESOLVED | VERIFIED. See SR-003-I2 above. The header now matches the body's tier vocabulary. ADEQUATE. |
| IN-001-I2 | Source 2 creates implicit fifth category outside the four-phenomena taxonomy | RESOLVED | VERIFIED. L0 taxonomy (lines 36-37) now includes: "Note on cross-modality context: Source 2 (Ban et al., 2024) studies negative prompt mechanisms in diffusion models (image generation), not LLMs. It falls outside the four LLM-specific phenomena above and is included solely for mechanistic analogy." The Phenomenon Taxonomy Coverage table (lines 591-608) explicitly categorizes Source 2 as "Cross-modality context (outside LLM taxonomy)" with a count of 1. Total accounts for all 30 sources. ADEQUATE. |

**Resolution Summary:** 2/2 Major findings fully resolved. 5/5 Minor findings fully resolved. All Iteration 2 findings closed.

---

## New Findings (Iteration 3)

The revision successfully addressed all 7 Iteration 2 findings. The following new issues were identified through fresh application of the 10 adversarial strategies against Revision 3.

### Finding Summary

| # | ID | Strategy | Severity | Finding | Section |
|---|----|----------|----------|---------|---------|
| 1 | IT3-001 | S-010 Self-Refine | Minor | Header arithmetic: "13 Tier 1 + 4 Tier 2 + 1 workshop" = 18 peer-reviewed, but the revision log states Tier 2 is 5 sources (4 + 1 moved from Tier 1) — header omits the fifth Tier 2 source in the peer-reviewed count | Document Header |
| 2 | IT3-002 | S-011 Chain-of-Verification | Minor | Source 20 (Control Illusion / AAAI 2026) L2 note states "Some findings drawn from abstract; full quantitative failure rates not fully extracted" — this abstract-only reading caveat is not disclosed in L1 Quality Notes or the Methodology Quality table, creating inconsistent treatment compared to Source 29 | L2 Source 20, L1 Source 20 |
| 3 | IT3-003 | S-013 Inversion | Minor | The new "Model-Internal Approaches" section in L0 names CAST results for Qwen 1.5B specifically but the overall CAST section headline framing "harmful refusal from 45.78% to 90.67%" lacks model qualification in the subsection heading, creating an impression of universal applicability that the L2 constrains to specific model sizes | L0 "Model-Internal Approaches" |

---

## Detailed New Findings

### IT3-001: Header Arithmetic Inconsistency — Tier 2 Count

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | Document Header (line 4), Source Quality Assessment (lines 554-561) |
| **Strategy Step** | S-010 Self-Refine — Internal Consistency Check |

**Evidence:**

Document header (line 4): "13 Tier 1 peer-reviewed + **4 Tier 2 peer-reviewed** + 1 workshop/symposium peer-reviewed + 10 arXiv preprints + 1 rejected submission + 1 commercially-affiliated report"

Source Quality Assessment (lines 555-556): "Tier 2 (established venues, workshops with peer review): **5 sources** -- TMLR (1: Source 9), *SEM (1: Source 4), EACL (1: Source 26), Computational Linguistics/MIT Press (1: Source 30), LLM@IJCAI'23 symposium (1: Source 12)"

Revision Log (line 620) confirms: "Updated Tier 2 count from 4 to 5."

The header says "4 Tier 2 peer-reviewed + 1 workshop/symposium peer-reviewed" which separates the LLM@IJCAI'23 symposium (Source 12) from the other four Tier 2 sources. The body classifies all five as Tier 2. The total peer-reviewed count from the header is 13 + 4 + 1 = 18, while the body supports 13 + 5 = 18 — the arithmetic is correct, but the header's breakdown differs from the body's classification by splitting the workshop out of Tier 2 rather than listing it as one of 5 Tier 2 sources. This creates a labeling inconsistency rather than an arithmetic error.

**Analysis:**

The overall total (30 sources, 18 peer-reviewed) is arithmetically correct. However, the header's description "4 Tier 2 peer-reviewed + 1 workshop/symposium peer-reviewed" does not match the body's organization where Source 12 is explicitly listed under "Tier 2 (established venues, workshops with peer review)." The header is partially self-contradictory: it separates the workshop from Tier 2, while the body places it inside Tier 2. This is a minor inconsistency rather than a factual error — a reader comparing header to body will notice the categorization approach differs.

**Recommendation:**

Align header with body. The body's classification already handles the workshop appropriately within Tier 2. The header should read: "13 Tier 1 peer-reviewed + 5 Tier 2 peer-reviewed (including 1 workshop/symposium) + 10 arXiv preprints + 1 rejected submission + 1 commercially-affiliated report." Or alternatively: "13 Tier 1 peer-reviewed + 4 Tier 2 peer-reviewed + 1 workshop/symposium peer-reviewed (non-archival IJCAI) + 10 arXiv preprints + 1 rejected submission + 1 commercially-affiliated report" — but this second option requires the body to also adopt the split classification, which it currently does not.

---

### IT3-002: Source 20 Abstract-Only Reading Undisclosed in L1 Quality Notes

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | L2 Source 20 (lines 355-359), L1 Source 20 (line 99) |
| **Strategy Step** | S-011 Chain-of-Verification — Disclosure Consistency Check |

**Evidence:**

L2 Source 20 (line 359): "**Note: Some findings in this survey drawn from abstract-level review; full quantitative failure rates should be verified against the complete paper for specific numerical claims.**"

L1 Source 20 Quality Notes (line 99): "Tier 1 venue (AAAI). Peer-reviewed. **Note: Some findings drawn from abstract; full quantitative failure rates not fully extracted from paper body.**"

Source 29, by comparison, received: footnote [^1], an explicit "reviewed from abstract only" L2 flag, and inclusion in the Methodology Quality table with "Cannot assess -- abstract only."

Source 20 has a caveat in L1 and L2 that findings were drawn from the abstract, but it is NOT flagged in the Methodology Quality table (lines 563-576), which covers only Tier 3 preprints. Source 20 is Tier 1 and is therefore excluded from the per-source quality table — but the abstract-only reading caveat means its evidence quality is more limited than other Tier 1 sources. A reader scanning the Tier 1 list for quality notes would not see the Source 20 abstract-only flag.

**Analysis:**

The distinction between Source 29 (abstract-only, Tier 3, explicitly flagged everywhere) and Source 20 (partial abstract reading, Tier 1, flagged only in L1/L2 notes) is defensible — Source 20 received a fuller review than Source 29 based on the L2 description. However, the per-source methodology quality table is presented as covering "Tier 3 preprints" only, which means Tier 1 sources with partial reviews have no equivalent treatment. For a C4 deliverable, this creates a minor completeness gap in quality disclosure. The survey's per-source methodology section implicitly creates an expectation that all quality limitations are surface-level disclosed.

**Recommendation:**

Either (a) extend the methodology quality table to include all sources with reading limitations (not just Tier 3 preprints), noting Source 20 as "partial — abstract review supplemented by body sections; full quantitative extraction incomplete," or (b) add a brief consolidated note in the Coverage Assessment listing all sources where findings were partially drawn from abstract-level reading (Source 20, Source 29). Option (b) is lower-effort and consistent with the survey's existing disclosure approach.

---

### IT3-003: CAST L0 Model Specificity Gap in "Model-Internal Approaches" Subsection

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | L0 "Model-Internal Approaches to Negative Constraints" (lines 50-52) |
| **Strategy Step** | S-013 Inversion — Specificity Check |

**Evidence:**

L0 "Model-Internal Approaches" section (lines 50-52):
> "**Conditional Activation Steering (CAST):** Lee et al. (2024, ICLR 2025 Spotlight, Source 28) showed that CAST improves harmful refusal from 45.78% to 90.67% while harmless refusal stays at only 2.20% (i.e., 97.8% of harmless prompts are correctly accepted)."

L2 Source 28 (line 453):
> "Qwen 1.5 (1.8B): harmful refusal improved from 45.78% to 90.67%"

The L2 explicitly attributes the 45.78% to 90.67% improvement to Qwen 1.5 (1.8B) — a specific 1.8-billion parameter model. The L0 presents the same numbers without a model qualifier. L2 further notes: "Performance plateaus quickly with minimal additional data." The L0 subsection does not specify which model these figures apply to, potentially implying these results are uniform across the 10 LLMs tested (which range from 1.8B to 32B parameters).

**Analysis:**

This is a narrower version of the Iteration 1 McKenzie overgeneralization issue (CV-001). The numbers are correct and traceable to Source 28, but the absence of the model qualifier ("Qwen 1.5B") in L0 allows a reader to interpret the 90.67% refusal rate as a general CAST capability rather than a specific result for the smallest model tested. The L2 contains the qualifier; the L0 does not propagate it. Given that L2 is the authoritative source and L0 is a summary, this is a minor rather than major issue, but it is notable for a C4 deliverable where quantitative precision matters.

**Recommendation:**

Add the model qualifier in L0: "CAST improves harmful refusal from 45.78% to 90.67% (in Qwen 1.5 1.8B) while harmless refusal stays at only 2.20%." This makes the result specific without reducing the impact of the finding — CAST's conditional mechanism is the key insight, and the precise model tested is relevant context.

---

## S-014 Score Assessment (Iteration 3)

### Scoring Rationale by Dimension

Active leniency bias counteraction applied throughout. The threshold is 0.95 for C4. Scores are assigned based on the document's actual quality, with deliberate verification of all claimed changes before scoring.

**Steelman acknowledgment (H-16 compliance):** The Revision 3 deliverable has genuinely improved on all Iteration 2 blocking issues. The CAST relocation is structurally sound — the new "Model-Internal Approaches" subsection is clearly labeled with a disclaimer, and the "When Negative Prompting Works" section is now appropriately limited to prompt-level techniques that practitioners can actually use. The Phenomenon Taxonomy Coverage table is a substantive methodological addition that closes the taxonomy coverage gap cleanly. The 60% claim treatment is honest and P-022 compliant. These improvements are real and represent meaningful quality gains.

---

#### Dimension 1: Completeness (Weight: 0.20)

**Assessment:**

Revision 3 closes the two Major completeness gaps from Iteration 2:

1. CAST is now separately categorized in a "Model-Internal Approaches" subsection, distinguishing what prompt engineering can achieve from what mechanistic intervention can achieve. This is substantively complete — practitioners reading the L0 get accurate information about both levels.
2. The Phenomenon Taxonomy Coverage table accounts for all 30 sources explicitly, eliminating the taxonomy coverage gap (Source 2 now has explicit "Cross-modality context" categorization; Source 22 has "Verification alternative"; Source 6 has dual categorization documented).

The survey now covers:
- Four-phenomena taxonomy with source mapping
- Prompt-level vs. model-internal approaches, clearly distinguished
- Coverage Assessment with six identified gaps and source references
- "When Negative Prompting Works" section with practical guidance
- Verification-Based Alternatives section (CoVe)
- PROJ-014 Hypothesis Context with honest 60% origin assessment
- Per-source quality notes for Tier 3 preprints

**Remaining gaps:**
- Source 20's partial abstract reading is not disclosed in the methodology quality table (IT3-002). This is a minor completeness gap relative to the comprehensive disclosure given to Source 29.
- Source 29 (abstract-only) is included for "benchmark landscape awareness" — this is disclosed but remains a marginal inclusion that slightly dilutes the source count. The disclosure mitigates the risk, however.

**Score: 0.93**

Improved from 0.87. The CAST relocation and taxonomy coverage table are the two substantive completeness improvements. The survey now provides complete, accurate information about all major phenomena, sources, and practical implications. The minor Source 20 disclosure gap and the Source 29 inclusion rationale prevent a score above 0.93 at C4 rigor.

---

#### Dimension 2: Internal Consistency (Weight: 0.20)

**Assessment:**

Revision 3 eliminated all four major inconsistencies from Iteration 2:

1. CAST L0/L2 categorization conflict — RESOLVED. Both L0 and L2 now classify CAST as a model-internal mechanistic technique, not a prompting approach.
2. Tier 1 Source 12 double-count — RESOLVED. Tier 1 = 13, Tier 2 = 5, counts verified.
3. Header vs. body source classification — RESOLVED. Header and body now use compatible vocabulary.
4. CAST terminology (acceptance vs. refusal) — RESOLVED. Both L0 and L2 use the same framing.

**Remaining inconsistencies:**
- IT3-001: Header lists "4 Tier 2 peer-reviewed + 1 workshop/symposium peer-reviewed" but the body classifies all 5 as Tier 2. The arithmetic is consistent (18 total peer-reviewed) but the category labeling splits what the body treats as unified. This is a labeling inconsistency, not a factual error.
- IT3-003: L0 "Model-Internal Approaches" presents CAST numbers without the Qwen 1.5B model qualifier that appears in L2. Minor L0/L2 specificity gap.

**Score: 0.92**

Improved from 0.83. The four major inconsistencies are eliminated. The two remaining issues are both Minor-level labeling inconsistencies rather than substantive factual conflicts. At C4 rigor, these prevent a score above 0.92.

---

#### Dimension 3: Methodological Rigor (Weight: 0.20)

**Assessment:**

Revision 3 adds the Phenomenon Taxonomy Coverage table, which is a methodological improvement: every source is assigned to a category with explanation, making the taxonomy operationally testable rather than a declarative claim. The "additional quality improvements" in the Revision Log (lines 631-638) show:
- Parenthetical source references added to all quantitative L0 claims
- Research gap traceability added with source references
- Expanded practical implementation guidance in the "When It Works" section

**Remaining methodological limitations (disclosed):**
- Source 29 abstract-only inclusion.
- 40% zero-result search query rate (documented and explained).
- Source 20 partial reading caveat present in L1/L2 but not methodology table.
- No controlled experiments are directly provided — this is a survey, not original research, so the methodological ceiling is appropriate.

The inclusion/exclusion criteria are explicit and appropriate. The search strategy is documented with zero-result explanations. The coverage assessment is honest about selection bias. These are not new issues; they are appropriately acknowledged limitations.

**Score: 0.91**

Improved from 0.87. The taxonomy table and source reference additions are genuine methodological improvements. The abstract-only Source 20 disclosure gap (IT3-002) prevents 0.92+. The fundamental limitation of 40% zero-result queries and one abstract-only source remain, but are now fully disclosed.

---

#### Dimension 4: Evidence Quality (Weight: 0.15)

**Assessment:**

The CAST relocation from "When Negative Prompting Works" to "Model-Internal Approaches" eliminates the most significant evidence quality issue from Iteration 2 — the claim that prompt-level negative constraints can achieve ~90% refusal effectiveness. This was presenting mechanistic intervention evidence as prompting evidence, a material misrepresentation. It is now corrected.

The Tier 1/Tier 2 reclassification is evidence quality improvement: the peer-reviewed evidence base is now accurately represented as 13 Tier 1 + 5 Tier 2 + 10 Tier 3 + 1 rejected + 1 commercial. This is a more honest representation than the previous 15 + 4 + 10 + 1 + 1 count.

**Remaining evidence quality issues:**
- IT3-003: L0 presents CAST effectiveness numbers without the Qwen 1.5B model qualifier. This overgeneralizes a specific model result in the summary layer.
- Source 14 (Joyspace AI commercial) has the appropriate caveat but remains the only source directly comparing positive/neutral/negative framing — a structural dependency on a low-quality source for a key claim.
- Source 20 partial reading caveat (IT3-002) means one Tier 1 source's quantitative findings cannot be fully verified from the survey text.

**Score: 0.92**

Improved from 0.86. The CAST evidence quality fix is the primary driver of improvement. The remaining issues are Minor-level: model qualifier gap in L0 (IT3-003), one commercial source dependency, and one Tier 1 partial reading.

---

#### Dimension 5: Actionability (Weight: 0.15)

**Assessment:**

The CAST relocation substantially improves actionability. Practitioners reading the L0 now get clear separation:
- "When Negative Prompting Works" = two prompt-level techniques they can implement today (warning-based meta-prompting: specific example phrasing provided; DeCRIM atomic decomposition: specific decomposition example provided)
- "Model-Internal Approaches" = what requires model access (CAST) — explicitly labeled as NOT reproducible through prompt engineering

The Revision Log (lines 637-638) notes: "Expanded the two remaining prompt-level techniques with practical implementation guidance (warning-based: example phrasing; DeCRIM: example decomposition)." This is confirmed in L0 lines 43-45 where specific example phrasings are given.

The Research Gaps section with source references (lines 62-64) helps PROJ-014 Phase 2 understand specifically where to focus experimental design.

**Remaining actionability issues:**
- The "Model-Internal Approaches" section provides the CAST ceiling for comparison, which is useful context, but does not include a practical "therefore, if you want prompt-level improvements expect X% vs. Y% from mechanistic approaches" synthesis. This is minor — the distinction is clear and the numbers allow readers to compute this themselves.
- The 60% claim origin being unverifiable slightly limits actionability for PROJ-014 (cannot benchmark against a specific claim), but the honest treatment is the right call.

**Score: 0.94**

Improved from 0.87. The CAST relocation with explicit practical limitations and the expanded "When It Works" guidance with concrete example phrasings are genuine actionability improvements. This is the most improved dimension in Revision 3.

---

#### Dimension 6: Traceability (Weight: 0.10)

**Assessment:**

Revision 3 adds inline source references to all quantitative L0 claims (e.g., "Source 9", "Source 5", "Source 6" in parentheticals throughout the L0) and to the Research Gaps section. This is confirmed in the Revision Log (line 635-636): "Added parenthetical source references to all quantitative claims in L0."

Verifying against the document: L0 now includes references like "(McKenzie et al., 2023, Source 9)," "(Vrabcova et al., 2025, Source 5)," "(Harada et al., 2024, Source 16)," "(Geng et al., 2025, Source 20)," "(Bai et al., 2022, Source 10)" — all verified present in lines 29-64.

The Phenomenon Taxonomy Coverage table makes all 30 source assignments traceable in one place.

**Remaining traceability gaps:**
- IT3-001: Header arithmetic labeling inconsistency (Tier 2 count described differently in header vs. body) — minor traceability gap for the quality metadata section.
- IT3-003: L0 CAST numbers lack the Qwen 1.5B qualifier that appears in L2 — a minor traceability gap between L0 and L2.
- Source 20's partial reading limitation is not surface-level traced in the methodology quality table.

**Score: 0.94**

Improved from 0.90. The inline source references and taxonomy table are genuine traceability improvements. The three Minor remaining gaps prevent 0.95+.

---

### Weighted Composite Score

| Dimension | Weight | Iter 2 Score | Iter 3 Score | Weighted |
|-----------|--------|-------------|-------------|---------|
| Completeness | 0.20 | 0.87 | 0.93 | 0.186 |
| Internal Consistency | 0.20 | 0.83 | 0.92 | 0.184 |
| Methodological Rigor | 0.20 | 0.87 | 0.91 | 0.182 |
| Evidence Quality | 0.15 | 0.86 | 0.92 | 0.138 |
| Actionability | 0.15 | 0.87 | 0.94 | 0.141 |
| Traceability | 0.10 | 0.90 | 0.94 | 0.094 |
| **Weighted Composite** | **1.00** | **0.86** | | **0.925** |

**Calculation:**
(0.93 × 0.20) + (0.92 × 0.20) + (0.91 × 0.20) + (0.92 × 0.15) + (0.94 × 0.15) + (0.94 × 0.10)
= 0.186 + 0.184 + 0.182 + 0.138 + 0.141 + 0.094
= **0.925**

---

## Verdict: REVISE

**Score:** 0.925 (threshold: 0.95; delta: -0.025)

**Classification:** REVISE (0.85-0.91 band — wait, 0.925 is above 0.91, in a near-threshold zone. Actual classification: scoring is REVISE — above the 0.91 REVISE band upper bound but below the 0.95 C4 threshold. This is the highest score achieved so far and represents substantial convergence toward the threshold.)

**Score history:** 0.78 → 0.86 → 0.925 (+0.065 this iteration)

**Why REVISE, not PASS:**

The C4 threshold is 0.95, not 0.92. With a composite of 0.925, the deliverable is 0.025 below the C4 threshold. The three dimensions most constraining the score are:

1. **Methodological Rigor (0.91):** The Source 20 partial-reading disclosure gap (IT3-002) is the primary remaining methodological rigor issue. Source 20's L2 caveat ("Some findings drawn from abstract") is not reflected in the methodology quality table.

2. **Internal Consistency (0.92):** The header Tier 2 labeling inconsistency (IT3-001) leaves a minor but technically present inconsistency between "4 Tier 2 + 1 workshop" (header) and "5 Tier 2 including workshop" (body).

3. **Completeness (0.93):** The Source 29 marginal inclusion and Source 20 partial-reading gap are small but prevent a full 0.95.

**What justified REVISE over REJECTED:**

The three remaining findings are all Minor severity. There are no Critical or Major findings remaining. The deliverable has resolved every finding from Iterations 1 and 2. The composite score of 0.925 is well into the upper REVISE zone. The three Minor findings are targeted and can each be addressed in a single edit.

**What the revision did well (Iteration 3):**

- CAST relocation to "Model-Internal Approaches" with explicit practitioner disclaimer — structurally sound, clearly executed
- Source 12 reclassification from Tier 1 to Tier 2 with explanatory note — corrects the double-count and workshop/main-track distinction
- Header rewrite to accurate tier breakdown — matches body vocabulary
- Phenomenon Taxonomy Coverage table — complete source-to-category mapping for all 30 sources
- Inline source references in L0 — substantially improves traceability for every L0 quantitative claim
- Honest 60% claim treatment — P-022 compliant and methodologically sound

---

## Required Actions Before Iteration 4

**Priority 1 (Minor — targeted single-edit fixes to close the 0.025 gap):**

- [ ] **IT3-001:** Align header Tier 2 description with body. Change header from "4 Tier 2 peer-reviewed + 1 workshop/symposium peer-reviewed" to "5 Tier 2 peer-reviewed (including 1 non-archival IJCAI symposium)" or, alternatively, keep the split in the header but also split in the body's tier table. Current mismatch: header splits while body unifies. Choose one approach consistently.

- [ ] **IT3-002:** Add Source 20 to disclosure notes. Either: (a) extend the per-source methodology quality table to include Tier 1/Tier 2 sources with partial readings, adding a Source 20 row noting "partial — abstract-level review; full quantitative failure rates not verified from paper body," or (b) add a brief note in the Coverage Assessment: "Source 20 (Control Illusion): Full quantitative failure rates not fully extracted; see L2 Source 20 caveat." The footnote approach used for Source 29 would also work (e.g., [^2]: Source 20 findings partially drawn from abstract...).

- [ ] **IT3-003:** Add Qwen 1.5B model qualifier to L0 "Model-Internal Approaches" section. Change "CAST improves harmful refusal from 45.78% to 90.67%" to "CAST improves harmful refusal from 45.78% to 90.67% (Qwen 1.5B, 1.8 parameters) while harmless refusal stays at only 2.20%." This matches L2 Source 28 specificity and prevents overgeneralization.

**Score projection for Iteration 4:** If all three Minor findings are resolved, projected improvement is approximately +0.02 to +0.03 per dimension affected, yielding a composite near 0.94-0.96. The achievable score depends on whether any new issues emerge from the edits. All three fixes are non-structural (no taxonomy changes, no source reclassifications, no section reorganization required) — the risk of introducing new issues is low.

---

## Protocol Compliance

| Strategy | Executed | Findings Generated | Prefix Used |
|----------|----------|-------------------|-------------|
| S-010 Self-Refine | Yes | 1 Minor (IT3-001: header arithmetic) | SR- |
| S-003 Steelman | Yes | Applied in pre-assessment; confirmed CAST relocation is adequate; no new Steelman findings (all major improvements validated) | SM- |
| S-002 Devil's Advocate | Yes | IT3-002 identified (Source 20 undisclosed partial reading) | DA- |
| S-004 Pre-Mortem | Yes | No new pre-mortem findings; 60% claim treatment now adequate | PM- |
| S-001 Red Team | Yes | IT3-003 identified (CAST model specificity gap) | RT- |
| S-007 Constitutional AI | Yes | P-022 compliance confirmed on 60% claim; header now accurate | CC- |
| S-011 Chain-of-Verification | Yes | IT3-002 identified via L1/L2/methodology table cross-check for Source 20 | CV- |
| S-012 FMEA | Yes | No new high-RPN findings; all Iteration 2 blocking issues resolved | FM- |
| S-013 Inversion | Yes | IT3-003 identified (specificity inversion: L0 less specific than L2) | IN- |
| S-014 LLM-as-Judge | Yes | Scores in Score Assessment section | LJ- |

**H-16 Compliance:** S-003 (Steelman) executed at position 2 before S-002 (Devil's Advocate) at position 3. SATISFIED.

**H-15 Self-Review (performed before persistence):**
- All findings have specific evidence from the deliverable with line references. VERIFIED.
- Severity classifications justified (3 Minor findings, 0 Critical, 0 Major — consistent with a deliverable where all prior blocking issues are resolved). VERIFIED.
- Finding identifiers use IT3-{NNN} format consistent with iteration marker convention. VERIFIED.
- Summary table matches detailed finding count (3 new findings). VERIFIED.
- Resolution tracking covers all 7 Iteration 2 findings with explicit file content verification (not just researcher self-report). VERIFIED.
- Score assessment applied leniency bias counteraction: score of 0.925 reflects genuine residual gaps; not inflated to 0.95 despite major improvements. VERIFIED.
- Verdict (REVISE at 0.925) is consistent with the C4 threshold of 0.95 and the 0.025 remaining gap. VERIFIED.
- Steelman acknowledgment applied: the researcher's claimed changes were verified against actual file content before scoring, and genuine improvements were credited. VERIFIED.

---

*Generated by: adv-executor*
*Strategy Version: 1.0.0*
*Constitutional Compliance: P-002 (persisted), P-003 (no subagents), P-004 (provenance cited), P-011 (evidence-based), P-022 (not deceived on scores)*
*Date: 2026-02-27*
*Iteration: 3 of 5 | Prior Score: 0.86 | Current Score: 0.925 | Delta: +0.065*
