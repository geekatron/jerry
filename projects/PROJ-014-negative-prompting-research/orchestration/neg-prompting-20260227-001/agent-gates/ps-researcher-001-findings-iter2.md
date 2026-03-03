# Adversarial Finding Report: ps-researcher-001 (Iteration 2)

> C4 Tournament | PROJ-014 | 2026-02-27
> Deliverable: research/academic-survey.md (Revision 2)
> Strategies executed: 10/10
> Prior score: 0.78 (REJECTED)

---

## Execution Context

- **Strategy Set:** S-010, S-003, S-002, S-004, S-001, S-007, S-011, S-012, S-013, S-014
- **Template Directory:** `.context/templates/adversarial/`
- **Deliverable Path:** `projects/PROJ-014-negative-prompting-research/research/academic-survey.md`
- **Criticality:** C4 (Critical)
- **Quality Threshold:** >= 0.95
- **Iteration:** 2 of 5
- **Executed:** 2026-02-27
- **Prior Iteration Findings:** `agent-gates/ps-researcher-001-findings-iter1.md`

---

## Iteration 1 Finding Resolution Tracking

The following table assesses whether each finding from Iteration 1 was adequately addressed in Revision 2. This is the primary gate check before evaluating new findings.

### Critical Findings (5 from Iteration 1)

| Finding ID | Original Issue | Resolution Status | Assessment |
|------------|----------------|-------------------|------------|
| SR-001/RT-001/FM-001/CC-001 | Source 19 anachronistic model citations (GPT-5, Claude-4-Sonnet) | RESOLVED | Model names verified via WebFetch. Corrected to "Claude Sonnet 4." Year corrected to 2026. Full 13-model list provided with verification note. Source 19 L2 now explicitly documents the verification. ADEQUATE. |
| RT-002 | Source 25 Nature venue unverified | RESOLVED | Nature DOI (10.1038/s41586-025-09937-5) confirmed and cited. Nature 649, 584-589 (2026) in L1. WebSearch confirmation noted. Tier 1 retained appropriately. ADEQUATE. |
| PM-001 | Source 14 commercial report without caveat | RESOLVED | Explicit "Commercially-affiliated arXiv report" paragraph added in L2. L1 Quality Notes updated. Retention justified as only positive/neutral/negative comparison study. ADEQUATE. |
| DA-001 | Core thesis conflates four phenomena | RESOLVED | Four-phenomena taxonomy (a-d) introduced in L0 with dedicated subsection. Each phenomenon has mechanism description, evidence base, and separate implication. ADEQUATE — though a new issue emerges from this fix (see SR-001-I2 below). |
| CV-001 | McKenzie et al. scope overgeneralization | RESOLVED | L0 now qualifies: "specific negation-related tasks in the Inverse Scaling Prize dataset," "2022-2023-era architectures," "competition-sourced dataset may have selection bias." Vrabcova counterevidence (r=0.867) prominently integrated. ADEQUATE. |

### Major Findings (15 from Iteration 1)

| Finding ID | Original Issue | Resolution Status | Assessment |
|------------|----------------|-------------------|------------|
| SR-002 / RT-004 | Hallucination rate claim overgeneralized | RESOLVED | L0 hallucination section now specifies: "LLaMA-2 (13B), hallucination rates on the Multiple-Choice QA task increased from approximately 26% (without negation) to 59.23% (with negation)." Task-specific ranges provided. ADEQUATE. |
| IN-001 | Missing "when negative prompting works" synthesis | RESOLVED | Dedicated "When Negative Prompting Works" section added to L0 with 3 specific conditions. PARTIALLY ADEQUATE — but the CAST inclusion introduces a new categorization error (see SR-002-I2 below). |
| DA-002 | NegativePrompt underweighted | RESOLVED | Constructive uses now covered in phenomenon (d) and "When Negative Prompting Works." ADEQUATE. |
| CV-002 | CoVe categorized as negative information | RESOLVED | CoVe moved to "Verification-Based Alternatives" subsection in L0 with explicit note it is NOT negative prompting. L2 Source 22 phenomenon category updated to "Verification-based mitigation strategy (NOT negative prompting)." ADEQUATE. |
| DA-003 | Selection bias toward negation comprehension | RESOLVED | Coverage Assessment now explicitly states: "majority of evidence in this survey (approximately 8 of 30 sources) addresses negation comprehension... rather than prohibition instruction-following." Selection bias acknowledged. ADEQUATE. |
| CV-003 | Source 16 published status not confirmed | RESOLVED | Confirmed REJECTED from ICLR 2025 via OpenReview. Both L1 and L2 now clearly state "Rejected from ICLR 2025." Caveated accordingly. ADEQUATE. |
| PM-003 | 60% claim origin undefined | PARTIALLY RESOLVED | "PROJ-014 Hypothesis Context" section added explaining the 60% figure is from "informal vendor and practitioner claims." However, no specific vendor document, blog post, or citation is provided. The claim remains attributed to unnamed sources. The section is more honest than the prior version but the specific origin remains undocumented. PARTIAL — warrants a minor finding. |
| PM-002 | Preprint quality heterogeneity understated | RESOLVED | Per-source methodology quality table added in Source Quality Assessment covering all 10 Tier 3 preprints. Abstract-only flags included. ADEQUATE. |
| RT-003 | Source 29 abstract-only reading not disclosed | RESOLVED | Footnote [^1] added. L1 Quality Notes updated. L2 Review Status explicitly states "reviewed from abstract only." ADEQUATE. |
| SM-001 | Vrabcova challenge understated | RESOLVED | Now "substantially challenges." Spearman r=0.867 explicitly quantified in L0 as "strong positive relationship." ADEQUATE. |
| SM-002 | Constructive uses needs L0 prominence | RESOLVED | L0 now leads with central tension framing. Four phenomena structured with explicit L0 presence. "When Negative Prompting Works" section prominent. ADEQUATE. |
| IN-002 | Inverse scaling potentially superseded | RESOLVED | McKenzie framed as "specific historical trend" in 2022-2023-era models. Architectural evolution acknowledged. ADEQUATE. |
| CC-002 | Inclusion/exclusion criteria not stated | RESOLVED | Inclusion and Exclusion criteria now explicitly stated in Research Methodology section. ADEQUATE. |
| CC-003 | Source 2 domain transfer speculative | RESOLVED | L1 Quality Notes now include explicit caveat about diffusion model vs. LLM domain transfer. L2 explicitly states "Transfer from diffusion model mechanisms to LLM mechanisms is theoretical and unvalidated." ADEQUATE. |
| FM-004 | Empty queries unexplained | RESOLVED | "Zero-Result Explanation" column added to search query table. Summary paragraph added explaining zero-result patterns. ADEQUATE. |

### Minor Findings (3 from Iteration 1)

| Finding ID | Original Issue | Resolution Status | Assessment |
|------------|----------------|-------------------|------------|
| SR-003 | Source 30 missing author names | RESOLVED | Authors identified: Renze Lou, Kai Zhang, Wenpeng Yin. Updated in L1 and L2. ADEQUATE. |
| IN-003 | "Pink elephant problem" label unsourced | RESOLVED | Term removed from L0 summary text. Only appears in reference to Source 5's actual title. ADEQUATE. |
| CC-003 | Source 2 domain transfer | RESOLVED | See above — covered under Major Findings. ADEQUATE. |

**Resolution Summary:** 4/5 Critical findings fully resolved. 1/5 Critical findings fully resolved (multiple finding compound). 14/15 Major findings resolved; 1 partially resolved (PM-003 60% claim origin). 3/3 Minor findings resolved. **All critical blocking issues cleared.**

---

## New Findings (Iteration 2)

The revision successfully addressed all blocking Critical findings from Iteration 1. However, the revision introduced several new issues and left minor residual problems. These are documented below.

### Finding Summary

| # | ID | Strategy | Severity | Finding | Section |
|---|----|----------|----------|---------|---------|
| 1 | SR-001-I2 | S-010 Self-Refine | Major | CAST (activation steering) included in "When Negative Prompting Works" section — activation steering is not a prompting technique; conflates model-internal intervention with prompt engineering | L0 "When Negative Prompting Works" |
| 2 | SR-002-I2 | S-010 Self-Refine | Major | Tier 1 source count error: Source 12 double-counted (listed under both "IJCAI" and "LLM@IJCAI"); actual unique Tier 1 count is 14, not 15 | Source Quality Assessment |
| 3 | SR-003-I2 | S-010 Self-Refine | Minor | Header claims "26 peer-reviewed or under review" — Source 16 (ICLR rejected) and Source 14 (commercial, not peer-reviewed) cannot be counted as peer-reviewed; actual peer-reviewed count is at most 19; "under review" label misrepresents preprints | Document Header |
| 4 | CV-001-I2 | S-011 Chain-of-Verification | Minor | L0 states CAST maintains "harmless acceptance at 97.8%" but L2 Source 28 says "harmless refusal stayed at 2.20%"; these are mathematically equivalent (complements) but terminology shift (refusal vs. acceptance) is inconsistent and could confuse readers | L0 "When Negative Prompting Works," L2 Source 28 |
| 5 | PM-001-I2 | S-004 Pre-Mortem | Minor | The 60% hallucination reduction claim's origin ("informal vendor and practitioner claims") remains without a single concrete example citation; the PROJ-014 Hypothesis Context section is better than Iteration 1 but still does not cite a specific source for the 60% figure | PROJ-014 Hypothesis Context |
| 6 | CC-001-I2 | S-007 Constitutional AI | Minor | Source 16 header count: The document header says "26 peer-reviewed or under review, 3 arXiv preprints, 1 commercially-affiliated arXiv report" — but Source 16 is described in L1 as "rejected" from ICLR, and Source 16 is counted among the 30 total. The math: 15+4=19 peer-reviewed + 10 arXiv preprints + 1 commercial = 30, but "26 peer-reviewed or under review" overcounts substantially | Document Header |
| 7 | IN-001-I2 | S-013 Inversion | Minor | The four-phenomena taxonomy creates a categorization edge case: Source 6 (Varshney hallucination) is labeled "a/b" spanning two categories, which is reasonable, but Source 2 (diffusion models) is labeled "Cross-modality mechanistic study" — a fifth category not in the taxonomy. The L0 taxonomy claims four phenomena but sources fall into five categories in practice | L2 Source 2, L0 taxonomy |

---

## Detailed New Findings

### SR-001-I2: CAST Included Under "When Negative Prompting Works" — Category Error

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | L0 "When Negative Prompting Works" |
| **Strategy Step** | S-010 Self-Refine — Completeness/Accuracy Check |

**Evidence:**
L0 "When Negative Prompting Works" includes:
> "Mechanistic activation steering: Lee et al. (2024, ICLR 2025 Spotlight) showed that Conditional Activation Steering (CAST) improves harmful refusal from 45.78% to 90.67% while maintaining harmless acceptance at 97.8%."

L2 Source 28 describes CAST's methodology as: "Used PCA on mean-centered examples for direction extraction" — this is a model-internal intervention that modifies residual stream activations. L2 explicitly states CAST is categorized as "(c) Training/alignment constraints (mechanistic intervention)," not as a prompting technique.

**Analysis:**
Conditional Activation Steering is not a prompting technique. It requires direct access to the model's internal activations, PCA decomposition, and injection of steering vectors into the residual stream at inference time. A practitioner cannot achieve these results by crafting better system prompts. Including CAST as evidence of "when negative prompting works" will cause readers to incorrectly conclude that negative prompting can achieve ~90% refusal rates via prompt engineering alone. This is a material misrepresentation of what CAST actually achieves. The section title "When Negative Prompting Works" should be limited to prompt-level interventions. CAST belongs in a separate section on "mechanistic approaches" or should be footnoted with a clear disclaimer that it is not a prompting technique.

**Recommendation:**
Either: (a) retitle the section to "When Negative Constraints Work" (broader framing that can legitimately include mechanistic approaches alongside prompting) and add a clear sub-heading distinguishing "prompt-level" from "mechanistic/model-level" approaches, or (b) remove CAST from the "When Negative Prompting Works" section and relocate it to a note following the section explaining that mechanistic approaches achieve much higher effectiveness than prompt-level approaches alone. A reader of PROJ-014 Phase 2 needs to know: "I cannot reproduce CAST results through prompt engineering."

---

### SR-002-I2: Tier 1 Source Count Error — Source 12 Double-Counted

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | Source Quality Assessment, "By venue tier" |
| **Strategy Step** | S-010 Self-Refine — Internal Consistency Check |

**Evidence:**
Source Quality Assessment states: "Tier 1 (top peer-reviewed venues): 15 sources -- Nature (1: Source 25), NeurIPS (1: Source 7), CVPR (1: Source 8), ICLR (3: Sources 13, 24, 28), ACL (2: Sources 22, 27), EMNLP (3: Sources 3, 15, 23), AAAI (1: Source 20), IJCAI (2: Sources 1, 12), LLM@IJCAI (1: Source 12)"

Source 12 is listed under both "IJCAI (2: Sources 1, 12)" and "LLM@IJCAI (1: Source 12)." Counting the enumerated entries: 1+1+1+3+2+3+1+2+1 = 15, but Source 12 appears in position 9 (IJCAI) and position 10 (LLM@IJCAI). The actual unique source count in Tier 1 is 14, not 15.

Additionally, "LLM@IJCAI'23" is an IJCAI-affiliated workshop, not the main IJCAI conference. Workshop papers typically receive different classification than main-track conference papers. Source 12 (Li et al., 2023) is a workshop paper at LLM@IJCAI, not a main-track IJCAI paper. Source 1 (Wang et al., 2024) is the main IJCAI 2024 paper. Conflating workshop and main-track inflates the apparent venue quality.

**Analysis:**
The error may seem minor but it matters for a C4 research deliverable that makes specific claims about source quality distribution. A reader using the Tier 1 count (15) to assess coverage breadth will be wrong by one, and the workshop/main-track conflation may lead to overestimating the quality-weighted evidence base.

**Recommendation:**
Correct the count to 14 unique Tier 1 sources (or keep at 15 if Source 12's workshop venue is considered Tier 1, but remove the double-counting). Clarify the IJCAI vs. LLM@IJCAI distinction. The L1 row for Source 12 says "LLM@IJCAI'23" — the Quality Assessment should use consistent labels and counts.

---

### SR-003-I2: Document Header Peer-Reviewed Count Overstated

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | Document Header (lines 4-5) |
| **Strategy Step** | S-010 Self-Refine — Accuracy Verification |

**Evidence:**
Document header states: "Sources: 30 unique sources (26 peer-reviewed or under review, 3 arXiv preprints, 1 commercially-affiliated arXiv report)"

Counting against the Source Quality Assessment tiers:
- Tier 1 (unique): ~14 sources (peer-reviewed)
- Tier 2: 4 sources (peer-reviewed — TMLR, *SEM, EACL, Computational Linguistics)
- Source 16 (rejected from ICLR): not peer-reviewed in any standard sense
- Total peer-reviewed: ~18 (not 26)
- Tier 3 arXiv preprints: 10 sources (Sources 2, 5, 6, 10, 11, 17, 18, 19, 21, 29)
- Source 16: rejected submission (1)
- Source 14: commercially-affiliated (1)

The breakdown 26 + 3 + 1 = 30 suggests that "26 peer-reviewed or under review" treats Tier 3 preprints as "under review" — but arXiv preprints are not submitted-and-under-review unless otherwise noted; they are self-published. The label "under review" implies formal peer review is in progress, which is not established for most of the Tier 3 sources.

**Analysis:**
The framing "26 peer-reviewed or under review" is more charitable to the survey's source quality than the evidence supports. This is not a critical integrity issue (the tier breakdown in the body is accurate and explicit), but the header-level summary is a mischaracterization that would mislead a casual reader.

**Recommendation:**
Update the header to: "Sources: 30 unique sources (18 peer-reviewed, 10 arXiv preprints [unreviewed], 1 ICLR-rejected submission, 1 commercially-affiliated arXiv report)" — or use the tier vocabulary already defined in the body: "15 Tier 1, 4 Tier 2, 10 Tier 3, 1 rejected, 1 commercial." Either is more accurate than "26 peer-reviewed or under review."

---

### CV-001-I2: CAST "Harmless Acceptance" vs. "Harmless Refusal" Terminology Inconsistency

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | L0 "When Negative Prompting Works" and L2 Source 28 |
| **Strategy Step** | S-011 Chain-of-Verification — Claim-Source Consistency Check |

**Evidence:**
L0 states: "Lee et al. (2024, ICLR 2025 Spotlight) showed that Conditional Activation Steering (CAST) improves harmful refusal from 45.78% to 90.67% **while maintaining harmless acceptance at 97.8%**."

L2 Source 28 states: "Qwen 1.5 (1.8B): harmful refusal improved from 45.78% to 90.67% while **harmless refusal stayed at 2.20%**" (parenthetical context: "vs. 96.40% with standard activation steering").

The values are mathematically consistent: 100% - 2.20% = 97.8%, so "harmless acceptance" and "harmless refusal" at those complementary rates refer to the same underlying measurement. However, the L0 switches from "refusal" to "acceptance" terminology within the same sentence, which is confusing. The L2 uses "harmless refusal stayed at 2.20%" meaning the model only incorrectly refused harmless prompts 2.20% of the time — a very low false-positive refusal rate. The L0 rephrases this as "harmless acceptance at 97.8%" — meaning the model correctly accepted 97.8% of harmless prompts. Both are correct but the terminology flip is unnecessary and potentially confusing.

**Analysis:**
This is a terminological inconsistency rather than a factual error, but for a C4 research deliverable, precision in quantitative terminology matters. A reader comparing L0 and L2 would need to recognize these are complements.

**Recommendation:**
Harmonize terminology: use "harmless refusal rate of 2.20% (i.e., only 2.20% of harmless prompts were incorrectly refused)" in L0, consistent with L2. This is clearer and self-explanatory without requiring the reader to compute the complement.

---

### PM-001-I2: 60% Hallucination Reduction Claim Origin Remains Uncited

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | PROJ-014 Hypothesis Context |
| **Strategy Step** | S-004 Pre-Mortem — Missing Citation Chain |

**Evidence:**
The PROJ-014 Hypothesis Context section states: "The specific '60% hallucination reduction' figure is PROJ-014's hypothesis target, derived from informal vendor and practitioner claims rather than from a single peer-reviewed source."

No specific vendor document, blog post, LLM vendor guidance page, or practitioner claim is cited. The section is honest about the figure's informal origin, but the "informal vendor and practitioner claims" attribution is itself uncited. A researcher reading this survey as a published artifact cannot trace what was actually claimed.

**Analysis:**
For an academic survey at C4 criticality, the origin of the central research hypothesis should be traceable. If the 60% figure comes from (for example) an OpenAI documentation page, a specific practitioner blog post, or a vendor-produced prompt engineering guide, that source should be cited or at minimum described with enough specificity to be identifiable. "Informal vendor and practitioner claims" is barely more informative than "it's commonly said." This does not undermine the survey's core findings (which correctly note the figure is unsupported), but it weakens the hypothesis contextualization.

**Recommendation:**
Either: (a) cite at least one concrete example of where this claim appears (a vendor documentation URL, a practitioner blog post, a conference talk) even if informal, or (b) acknowledge that the 60% figure may be an informal "rule of thumb" in the practitioner community with no traceable single origin, and frame it explicitly as such. Option (b) is honest but option (a) is more rigorous.

---

### CC-001-I2: Document Header Source Classification Inconsistency

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | Document Header |
| **Strategy Step** | S-007 Constitutional AI — P-022 (No Deception) Check |

**Evidence:**
This finding overlaps with SR-003-I2 but addresses the P-022 (No Deception) angle specifically. The header count "26 peer-reviewed or under review" uses the category "under review" to apparently absorb 8 arXiv preprints into a near-peer-reviewed category. The phrase "under review" has a specific meaning in academic publishing: it means a manuscript has been submitted to a venue and is awaiting editorial decision. Most arXiv preprints are NOT under review in this sense — they may have been submitted simultaneously, but arXiv is typically used for self-publication and the peer review status is independent.

The Source Quality Assessment body is transparent: it states "10 sources" in Tier 3 (arXiv). But the header converts these to "under review" language that overstates their formal review status.

**Analysis:**
This creates a potential P-022 concern: a reader encountering the header before the body would form an impression of source quality that the body partially contradicts. The header should match the body's honest Tier 3 disclosure.

**Recommendation:**
Align header language with the body's tier vocabulary. The current header is more favorable than the evidence supports. See SR-003-I2 recommendation for the specific corrected framing.

---

### IN-001-I2: Source 2 Creates Implicit Fifth Category Outside the Four-Phenomena Taxonomy

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | L2 Source 2, L0 Taxonomy |
| **Strategy Step** | S-013 Inversion — Taxonomy Completeness Check |

**Evidence:**
The L0 introduces a four-phenomena taxonomy: (a) negation comprehension, (b) prohibition instruction-following, (c) training/alignment constraints, (d) negative framing effects. The taxonomy claims to cover the literature's four distinct phenomena.

However, L2 Source 2 is categorized as "Cross-modality mechanistic study" — a label that does not correspond to any of the four phenomena. The L0 taxonomy does not include a category for "cross-modality mechanistic studies." Source 2's categorization is appropriate given its content (diffusion models), but it sits outside the taxonomy defined in L0, creating an internal inconsistency between the L0's claimed four-phenomena coverage and the L2's actual categorization scheme.

**Analysis:**
This is a minor structural inconsistency. The four-phenomena taxonomy describes phenomena in LLMs specifically; Source 2 is acknowledged as being about diffusion models (a different modality). The survey should either: (a) note that Source 2 is outside the four-phenomena taxonomy by design (it provides cross-modality context), or (b) include "cross-modality reference" as an explicit fifth category in the coverage assessment.

**Recommendation:**
Add a brief parenthetical in the L0 taxonomy or the Coverage Assessment noting that Source 2 provides cross-modality context and falls outside the four phenomena categories by design. This prevents a reader from noticing the apparent inconsistency between the claimed taxonomy and the L2 categorization labels.

---

## S-014 Score Assessment (Iteration 2)

### Scoring Rationale by Dimension

Active leniency bias counteraction applied throughout. The threshold is 0.95 for C4. Scores are assigned based on the revised document's actual quality, not relative improvement from Iteration 1.

---

#### Dimension 1: Completeness (Weight: 0.20)

**Assessment:**
The revision substantially improved completeness:
- Four-phenomena taxonomy now provides a comprehensive organizing framework.
- "When Negative Prompting Works" section fills the most significant gap from Iteration 1.
- Research gaps are explicitly documented with 6 identified gaps including direct A/B testing, CoT interaction, multilingual coverage.
- Coverage Assessment adds "Long-context negative instruction persistence" and "Production system telemetry" as gaps.
- Source 29 abstract-only reading is disclosed (the source still counts for benchmark landscape awareness).
- PROJ-014 Hypothesis Context section grounds the research question.

**Remaining gaps:**
- CAST (Source 28) is miscategorized as prompting in the "When Negative Prompting Works" section, which is a completeness distortion — readers will not understand that prompt-level and mechanistic interventions are distinct.
- The 60% claim origin remains without a concrete citation, which is an incompleteness in the hypothesis documentation.
- The taxonomy introduces a framework but Source 2 falls outside it without explanation.

**Score: 0.87**

The completeness has improved significantly from 0.82. The four-phenomena taxonomy and "When Negative Prompting Works" section are genuine improvements. Deducted for: CAST prompting conflation creates an incompleteness in the "when it works" synthesis (the practical answers are now partially wrong), and the 60% origin gap.

---

#### Dimension 2: Internal Consistency (Weight: 0.20)

**Assessment:**
The revision eliminated most of the major inconsistencies from Iteration 1:
- L0 hallucination claim now matches L2 Source 6 (MCQA, LLaMA-2 specific).
- CoVe now properly categorized as verification pipeline, not negative prompting.
- Source 14 caveat consistent between L1 and L2.
- Source 16 rejection noted consistently in L1 and L2.
- Source 19 verification note consistent in L1 and L2.
- Source 25 Nature DOI consistent in L1 and L2.

**Remaining inconsistencies:**
- L0 "harmless acceptance at 97.8%" vs. L2 Source 28 "harmless refusal stayed at 2.20%" — minor terminology inconsistency (mathematically equivalent, conceptually confusing).
- Source 12 double-counted in Tier 1 (listed under both IJCAI and LLM@IJCAI in Source Quality Assessment) — internal count inconsistency.
- Source 2 labeled "Cross-modality mechanistic study" in L2 but falls outside the four-phenomena taxonomy defined in L0 — category label inconsistency.
- Header "26 peer-reviewed or under review" inconsistent with body's Tier 3 disclosure of 10 arXiv preprints.
- CAST categorized as "(c) Training/alignment constraints (mechanistic intervention)" in L2 Source 28 but included under "When Negative Prompting Works" prompting section in L0 — category inconsistency.

**Score: 0.83**

Improved substantially from 0.74, but four material inconsistencies remain (CAST L0/L2 categorization conflict, Tier 1 double-count, Source 2 taxonomy gap, header vs. body source classification). At C4 threshold, these are notable deductions. The Critical-level consistency failures are eliminated; what remains are Major-to-Minor inconsistencies.

---

#### Dimension 3: Methodological Rigor (Weight: 0.20)

**Assessment:**
The revision improved methodological rigor substantially:
- Inclusion/exclusion criteria now explicitly stated.
- Per-source methodology quality notes added for all Tier 3 preprints.
- Zero-result query explanations added with a dedicated column in the search table.
- Verification notes (WebFetch, WebSearch) documented inline for contested sources.
- The Coverage Assessment is more explicit about what is well-covered vs. under-researched.

**Remaining gaps:**
- Source 29 remains abstract-only. While this is disclosed, the decision to include it (for "benchmark landscape awareness") is methodologically weak — a survey counting this as one of 30 sources while extracting no quantitative findings sets an inconsistent evidence standard.
- The search strategy shows 8 of 20 queries returning zero unique new sources (including queries 4, 5, 8, 9, 16, 19). The explanations are better but the high zero-result rate (40%) still suggests the search strategy has significant efficiency issues that future reproducers would encounter.
- The selection bias acknowledgment in Coverage Assessment is explicit and appropriate.

**Score: 0.87**

Improved from 0.78. The criteria, per-source quality notes, and verification documentation are genuine improvements. The abstract-only Source 29 and 40% zero-result rate are remaining limitations, but these are now disclosed rather than hidden.

---

#### Dimension 4: Evidence Quality (Weight: 0.15)

**Assessment:**
Evidence quality improvements are the most substantial change in Revision 2:
- Source 19 model names verified via WebFetch — this eliminates the most serious evidence quality concern.
- Source 25 Nature DOI confirmed — this eliminates the premature venue attribution concern.
- Source 14 explicit peer-review caveat added — this contextualizes the 8.4% accuracy degradation claim appropriately.
- Source 16 ICLR rejection confirmed — this contextualizes the exponential decay finding appropriately.
- Source 29 abstract-only disclosed — this limits readers from over-relying on that source.
- Per-source methodology quality table adds systematic evidence grading.

**Remaining evidence quality issues:**
- CAST (Source 28) presented in L0 as evidence that "negative prompting works" when CAST is a mechanistic intervention requiring model access — this is a material evidence quality problem because the L0 claim is not supported by CAST as evidence for prompting effectiveness.
- The Tier 1 double-count (Source 12) overstates the peer-reviewed evidence base by one source.
- Source 12 (LLM@IJCAI workshop) may not fully merit Tier 1 classification equivalent to main-track IJCAI.
- The 60% claim origin remains uncited.

**Score: 0.86**

Significantly improved from 0.69. The verification of Sources 19 and 25 — the most serious evidence quality failures — have been resolved. The CAST conflation (presenting mechanistic intervention as prompting evidence) is the primary remaining evidence quality issue. The Tier 1 counting error is secondary. Together, these prevent the score from reaching 0.92+.

---

#### Dimension 5: Actionability (Weight: 0.15)

**Assessment:**
Actionability has improved:
- "When Negative Prompting Works" section provides specific conditions with quantified improvements.
- Four-phenomena taxonomy helps practitioners understand which evidence applies to which context.
- Research gap section now explicitly names 6 gaps including "Direct A/B testing" as the highest-priority gap for PROJ-014 Phase 2.
- PROJ-014 Hypothesis Context section grounding is new and useful.
- Selection bias acknowledgment helps practitioners understand where to focus future research.

**Remaining actionability issues:**
- The CAST inclusion in "When Negative Prompting Works" is actively misleading for practitioners — it suggests prompt-level negative constraints can achieve ~90% effectiveness when this requires model-internal engineering. This reduces practical actionability by setting impossible expectations for prompt engineering.
- The 60% claim origin without citation makes it harder for PROJ-014 to benchmark against a specific claim.
- The "When Negative Prompting Works" section lists three conditions but does not prioritize them by accessibility or practical implementability (warning-based meta-prompting is readily implementable in prompts; CAST is not).

**Score: 0.87**

Improved from 0.84. The "When Negative Prompting Works" section is a genuine improvement. Deducted for CAST conflation actively misleading practitioners, and for the lack of practical prioritization within the "when it works" conditions.

---

#### Dimension 6: Traceability (Weight: 0.10)

**Assessment:**
Traceability is now strong:
- Source 30 authors added.
- Source 19 verification notes with specific WebFetch confirmation documented inline.
- Source 25 Nature DOI traceable.
- Source 14 commercially-affiliated attribution traceable.
- Revision Log documents all 22 finding resolutions systematically.
- Footnote [^1] for Source 29.
- L1 Quality Notes updated for Sources 2, 14, 16, 19, 20, 25, 29.

**Remaining traceability gaps:**
- "60% claim" has no traceable origin — it is attributed to "informal vendor and practitioner claims" without any identifiable source.
- CAST L0 claim ("harmless acceptance at 97.8%") cannot be directly traced to L2 Source 28 without reader computation — the complement relationship is not noted.
- Source 12 double-count obscures accurate traceability of the Tier 1 count.

**Score: 0.90**

Improved from 0.86. The revision log, verification notes, and author corrections are genuine improvements. The 60% claim origin and CAST terminology discrepancy are remaining gaps. Traceability is the strongest dimension in this revision.

---

### Weighted Composite Score

| Dimension | Weight | Score | Weighted |
|-----------|--------|-------|---------|
| Completeness | 0.20 | 0.87 | 0.174 |
| Internal Consistency | 0.20 | 0.83 | 0.166 |
| Methodological Rigor | 0.20 | 0.87 | 0.174 |
| Evidence Quality | 0.15 | 0.86 | 0.129 |
| Actionability | 0.15 | 0.87 | 0.1305 |
| Traceability | 0.10 | 0.90 | 0.090 |
| **Weighted Composite** | **1.00** | | **0.8635** |

**Calculation:**
(0.87 × 0.20) + (0.83 × 0.20) + (0.87 × 0.20) + (0.86 × 0.15) + (0.87 × 0.15) + (0.90 × 0.10)
= 0.174 + 0.166 + 0.174 + 0.129 + 0.1305 + 0.090
= **0.8635** (rounded to **0.86**)

---

## Verdict: REVISE

**Score:** 0.86 (threshold: 0.95; delta: -0.09)

**Classification:** REVISE (0.85-0.91 band — near threshold; targeted revision likely sufficient)

**Progress from Iteration 1:** 0.78 → 0.86 (+0.08). This is substantial improvement. All five Critical findings from Iteration 1 are resolved. The score moved from REJECTED into the REVISE band.

**Rationale for REVISE (not PASS):**

1. **CAST conflation is the primary remaining blocker.** The "When Negative Prompting Works" section includes Conditional Activation Steering as evidence that negative prompting works. CAST is a model-internal mechanistic intervention (activation steering via PCA on residual stream), not a prompt engineering technique. This conflation actively misleads practitioners about what prompting can achieve and creates an inconsistency with L2 Source 28's own categorization as "Training/alignment constraints." This is a Major finding that affects three dimensions simultaneously (Internal Consistency, Evidence Quality, Actionability) and prevents the score from reaching 0.90+ in those dimensions.

2. **Tier 1 source double-count.** Source 12 is enumerated under both "IJCAI (2: Sources 1, 12)" and "LLM@IJCAI (1: Source 12)" in the Source Quality Assessment, producing a count of 15 when the unique count is 14. This is a factual error in the quality metadata of a C4 deliverable.

3. **Header source classification overstates peer-review status.** "26 peer-reviewed or under review" is materially inconsistent with the body's own tier disclosure (10 Tier 3 arXiv preprints, 1 rejected submission, 1 commercial report). The gap between 26 (header) and actual peer-reviewed (~18-19) is too large for a C4 deliverable.

4. **Internal Consistency (0.83) is below the implicit per-dimension threshold for C4.** With four remaining inconsistencies (CAST categorization, Tier 1 count, header vs. body source classification, CAST terminology), Internal Consistency cannot reach 0.90+ without targeted fixes.

**What the revision did well (justifying REVISE not REJECTED):**
- All 5 Critical findings from Iteration 1 fully resolved
- Evidence Quality improved by +0.17 (most improved dimension)
- Methodological rigor substantially improved via criteria, per-source quality notes, zero-result explanations
- The four-phenomena taxonomy is a genuine structural improvement
- Revision Log is complete and systematically documented
- Traceability is now strong at 0.90

---

## Required Actions Before Iteration 3

**Priority 1 (Major — must resolve for PASS):**
- [ ] Fix CAST classification in "When Negative Prompting Works": either retitle section to "When Negative Constraints Work (Prompt-Level and Mechanistic)" with clear sub-headings distinguishing prompt-level approaches (Barreto/Jana, Ferraz/DeCRIM) from mechanistic approaches (CAST), OR remove CAST from this section and add a note that mechanistic approaches achieve higher effectiveness than prompt-level approaches.
- [ ] Fix Tier 1 source double-count: Source 12 appears in both "IJCAI (2: Sources 1, 12)" and "LLM@IJCAI (1: Source 12)"; correct to reflect one unique count. Clarify whether Source 12 (workshop paper) belongs to IJCAI Tier 1 or should be downgraded to Tier 2.

**Priority 2 (Minor — should resolve to clear threshold):**
- [ ] Update document header from "26 peer-reviewed or under review, 3 arXiv preprints, 1 commercially-affiliated arXiv report" to language consistent with the body's tier disclosure (e.g., "15 Tier 1 peer-reviewed, 4 Tier 2 peer-reviewed, 10 Tier 3 arXiv preprints, 1 rejected submission, 1 commercially-affiliated arXiv report").
- [ ] Harmonize CAST terminology: change L0 "harmless acceptance at 97.8%" to "harmless refusal rate of 2.20% (97.8% of harmless prompts correctly accepted)" to match L2 Source 28 framing.
- [ ] Clarify 60% claim origin in PROJ-014 Hypothesis Context: add at least one example of the type of vendor/practitioner source making this claim, or explicitly acknowledge the figure's origin is unverifiable.
- [ ] Add note that Source 2 falls outside the four-phenomena taxonomy by design (cross-modality reference context) to prevent apparent inconsistency with the L0 taxonomy.

---

## Protocol Compliance

| Strategy | Executed | Findings Generated | Prefix Used |
|----------|----------|-------------------|-------------|
| S-010 Self-Refine | Yes | 3 (2 Major, 1 Minor) | SR-{N}-I2 |
| S-003 Steelman | Yes | Findings surfaced in resolution tracking; no new Steelman findings (revision improved strongest claims) | SM- |
| S-002 Devil's Advocate | Yes | CAST conflation finding supported (DA-001-I2 = SR-001-I2) | DA- |
| S-004 Pre-Mortem | Yes | 1 Minor (PM-001-I2: 60% origin uncited) | PM- |
| S-001 Red Team | Yes | Tier 1 double-count confirmed, header accuracy issue | RT- |
| S-007 Constitutional AI | Yes | 1 Minor (CC-001-I2: P-022 header language) | CC- |
| S-011 Chain-of-Verification | Yes | 1 Minor (CV-001-I2: CAST terminology inconsistency) | CV- |
| S-012 FMEA | Yes | CAST conflation highest-RPN finding; Tier 1 count secondary | FM- |
| S-013 Inversion | Yes | 1 Minor (IN-001-I2: taxonomy fifth category) | IN- |
| S-014 LLM-as-Judge | Yes | Scores in Score Assessment section | LJ- |

**H-16 Compliance:** S-003 (Steelman) executed at position 2 before S-002 (Devil's Advocate) at position 3. SATISFIED.

**H-15 Self-Review (performed before persistence):**
- All findings have specific evidence from the deliverable. VERIFIED.
- Severity classifications justified against Critical/Major/Minor criteria. VERIFIED.
- Finding identifiers follow template prefix format with I2 iteration marker. VERIFIED.
- Summary table matches detailed finding count (7 new findings). VERIFIED.
- Resolution tracking covers all 22 Iteration 1 findings with explicit resolution status. VERIFIED.
- Score assessment applied leniency bias counteraction (no inflation to hide remaining issues). VERIFIED.
- Verdict (REVISE at 0.86) is consistent with dimension scores and REVISE band definition (0.85-0.91). VERIFIED.

---

*Generated by: adv-executor*
*Strategy Version: 1.0.0*
*Constitutional Compliance: P-002 (persisted), P-003 (no subagents), P-004 (provenance cited), P-011 (evidence-based), P-022 (not deceived on scores)*
*Date: 2026-02-27*
*Iteration: 2 of 5 | Prior Score: 0.78 | Current Score: 0.86 | Delta: +0.08*
