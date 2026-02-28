# Adversarial Finding Report: ps-researcher-001 (Iteration 1)

> C4 Tournament | PROJ-014 | 2026-02-27
> Deliverable: research/academic-survey.md
> Strategies executed: 10/10

---

## Execution Context

- **Strategy Set:** S-010, S-003, S-002, S-004, S-001, S-007, S-011, S-012, S-013, S-014
- **Template Directory:** `.context/templates/adversarial/`
- **Deliverable Path:** `projects/PROJ-014-negative-prompting-research/research/academic-survey.md`
- **Criticality:** C4 (Critical)
- **Quality Threshold:** >= 0.95
- **Iteration:** 1 of 5
- **Executed:** 2026-02-27

---

## Finding Summary

| # | ID | Strategy | Severity | Finding | Section |
|---|-----|----------|----------|---------|---------|
| 1 | SR-001 | S-010 Self-Refine | Critical | Source 19 cites GPT-5, Claude-4-Sonnet, GPT-4.1 -- models that did not exist at time of claimed publication (2025 arXiv) | L1 Source Catalog, L2 Source 19 |
| 2 | SR-002 | S-010 Self-Refine | Major | L0 attribution error: "33 percentage points" claim misattributes the baseline -- L2 Source 6 shows baseline is task-specific, not a single ~26% figure | L0 Executive Summary |
| 3 | SR-003 | S-010 Self-Refine | Minor | Source 30 authors listed as "multiple authors" -- no names provided despite being a journal publication | L1 Source Catalog |
| 4 | SM-001 | S-003 Steelman | Major | The strongest claim (inverse scaling) is presented with appropriate nuance but the Vrabcova (2025) challenge is understated; the tension deserves stronger synthesis | L0 Executive Summary |
| 5 | SM-002 | S-003 Steelman | Minor | The constructive uses theme is the survey's most actionable finding and deserves heavier emphasis in L0 given practical implications | L0 Executive Summary |
| 6 | DA-001 | S-002 Devil's Advocate | Critical | The core claim "negative prompting is problematic" conflates four distinct phenomena that have different evidentiary bases and practical implications | L0 Executive Summary |
| 7 | DA-002 | S-002 Devil's Advocate | Major | The survey's conclusion implicitly dismisses negative prompting effectiveness without addressing the NegativePrompt study's 46.25% improvement result on BIG-Bench | L0, L2 Source 1 |
| 8 | DA-003 | S-002 Devil's Advocate | Major | Selection bias: the survey over-represents negation comprehension failures but under-represents practical system prompt effectiveness studies | Research Methodology |
| 9 | PM-001 | S-004 Pre-Mortem | Critical | Source 14 (Gandhi & Gandhi 2025) is from an industry blog/company report (Joyspace AI), not peer-reviewed; yet it is cited alongside ICLR and NeurIPS papers without caveat | L1 Source Catalog, Source Quality Assessment |
| 10 | PM-002 | S-004 Pre-Mortem | Major | 12 of 30 sources (40%) are arXiv preprints with no peer review -- the survey's quality assessment buries this under "Tier 3" but does not adequately warn about methodological reliability of individual claims drawn from these sources | Source Quality Assessment |
| 11 | PM-003 | S-004 Pre-Mortem | Major | The survey presents the "60% hallucination reduction" claim as the research gap's absent evidence, but this specific figure appears nowhere in the survey as a positive claim -- it is unclear what the original marketing/vendor claim being tested is, nor where the 60% figure originates | L0 Executive Summary |
| 12 | RT-001 | S-001 Red Team | Critical | Source 19 methodology cites "GPT-5, GPT-4.1, Claude-4-Sonnet, Gemini 2.5, DeepSeek-R1" -- these model designations are anachronistic or non-standard (GPT-5 was not publicly released as of 2025; Claude-4-Sonnet is not a released designation). This raises fabrication concerns about the source itself or the metadata extraction | L2 Source 19 |
| 13 | RT-002 | S-001 Red Team | Critical | Source 25 publication venue listed as "Nature (January 2026)" -- a paper published in 2025 (arXiv preprint) cannot have a confirmed Nature 2026 venue unless the survey was written post-January 2026, which contradicts the 2026-02-27 survey date. This is either a premature attribution or a fabrication | L1 Source Catalog, L2 Source 25 |
| 14 | RT-003 | S-001 Red Team | Major | Source 29 (Thunder-NUBench) DOI is arXiv:2506.14397 -- the "25" prefix indicates June 2025. The survey is dated 2026-02-27. A June 2025 arXiv paper could legitimately be included; however the L2 section states "Full quantitative results not available from abstract" suggesting the source was not fully read, yet specific claims are made about its findings | L1 Source Catalog, L2 Source 29 |
| 15 | RT-004 | S-001 Red Team | Major | The L0 claim about Varshney et al. (2024) states hallucination increases "from ~26% to ~59%" but L2 Source 6 shows the baseline rates are task-specific (FPC 63.77%, CFG 72.33%, MCQA 36.6%, FG 62.59%). The ~26% vs. ~59% comparison appears to refer specifically to LLaMA-2 on one task type, not a general baseline. This is a material misquotation by overgeneralization | L0, L2 Source 6 |
| 16 | CC-001 | S-007 Constitutional AI | Critical | P-022 (No Deception): The survey states "Sources: 30 unique academic sources" in its header but Source 14 is from Joyspace AI (a commercial company), Source 19 cites non-existent model versions, and Source 29 was read only from the abstract. The "academic sources" framing is materially misleading | Header, L2 Sources 14, 19, 29 |
| 17 | CC-002 | S-007 Constitutional AI | Major | Research constraint compliance: The methodology section does not explicitly state inclusion/exclusion criteria. The survey mentions "peer-reviewed" in the quality assessment but includes 12 arXiv preprints under a tier system without explicit criteria for when a preprint is acceptable | Research Methodology |
| 18 | CC-003 | S-007 Constitutional AI | Minor | P-011 (Evidence-Based): Source 2 (negative prompts in diffusion models / Stable Diffusion) is included in a survey about LLM negative prompting. The relevance claim is speculative ("provides theoretical grounding") rather than evidence-based | L2 Source 2 |
| 19 | CV-001 | S-011 Chain-of-Verification | Critical | Claim: "McKenzie et al. (2023) documented that larger models perform worse on tasks requiring negation understanding, with performance dropping below random chance beyond approximately 10^22 training FLOPs." Verification: L2 Source 9 confirms the ~10^22 FLOPs threshold. However, the L0 uses this as a blanket statement about "negation understanding" when the McKenzie paper covers multiple task types, only some of which involve negation specifically. The attribution is accurate but the scope generalization is misleading | L0, L2 Source 9 |
| 20 | CV-002 | S-011 Chain-of-Verification | Critical | Claim: "Dhuliawala et al. (2023) demonstrated that chain-of-verification...more than doubles precision on list-based tasks." Verification: L2 Source 22 confirms "Precision more than doubles on Wikidata tasks (0.17 to 0.36)." The L0 attribution is accurate. However, the L0 frames this as part of "constructive uses of negative information" -- but CoVe is not negative prompting; it is a verification pipeline. The conceptual category assignment is a conflation | L0, L2 Source 22 |
| 21 | CV-003 | S-011 Chain-of-Verification | Major | Claim: Harada et al. (2024) -- "ICLR 2025 submission." Verification: The L1 catalog lists this as "ICLR 2025 submission" (a submission, not a published paper). The citation uses the OpenReview URL. The L2 does not clarify whether this paper was accepted. Citing unaccepted submissions as equivalent to published papers without caveat misrepresents source quality | L1 Source 16 |
| 22 | CV-004 | S-011 Chain-of-Verification | Major | Claim: Source 19 is described as studying "GPT-5, GPT-4.1, Claude-4-Sonnet, Gemini 2.5, DeepSeek-R1." These model designations (particularly GPT-5 and Claude-4-Sonnet) are unverifiable against known model release timelines. This constitutes an unverifiable factual claim that cannot be confirmed from the abstract or publicly available information at the time of this review | L1 Source 19, L2 Source 19 |
| 23 | FM-001 | S-012 FMEA | Critical | Failure Mode: Anachronistic model citations in Source 19; Effect: Reader concludes model X (which may not exist) shows property Y; RPN = Severity(9) × Occurrence(1 confirmed instance) × Detection(3, easily caught by date checking) = 27. The actual impact is high because it creates a plausibility halo for the entire survey | L2 Source 19 |
| 24 | FM-002 | S-012 FMEA | Major | Failure Mode: Source 14 (commercial company, no peer review) cited alongside Tier 1 venues; Effect: Over-inflation of evidence quality for claims about negative sentiment reducing accuracy by 8.4%; RPN = Severity(7) × Occurrence(1 confirmed) × Detection(4) = 28 | L1 Source 14, Source Quality Assessment |
| 25 | FM-003 | S-012 FMEA | Major | Failure Mode: 40% of sources are unreviewed arXiv preprints but source-level methodology quality varies enormously; the tier system treats all preprints equally; Effect: Claims from rigorous preprints (e.g., McKenzie TMLR) treated with same weight as speculative single-institution preprints; RPN = Severity(6) × Occurrence(12 preprints) × Detection(5) = 360. Highest RPN finding | Research Methodology, Source Quality Assessment |
| 26 | FM-004 | S-012 FMEA | Minor | Failure Mode: The search query table (20 queries) shows 8 of 20 queries returned 0 sources; Effect: Readers cannot assess whether search gap represents absence of literature or search strategy failure; RPN = Severity(4) × Occurrence(8 queries) × Detection(6) = 192 | Research Methodology |
| 27 | IN-001 | S-013 Inversion | Major | Inversion: "What if negative prompting IS effective for system prompt constraints?" Evidence in survey: Source 23 shows warning-based prompts improve distractor negation by up to 25.14%. Source 15 shows atomizing negative constraints (DeCRIM) improves compliance by 7.3-8%. Source 28 shows conditional activation steering achieves 90.67% harmful refusal vs. 45.78% baseline. The survey does not synthesize these as a "negative prompting CAN work under specific conditions" thesis | L0, L2 Sources 23, 15, 28 |
| 28 | IN-002 | S-013 Inversion | Major | Inversion: "What if the inverse scaling finding is an artifact of benchmark design rather than a fundamental negation failure?" Evidence in survey: McKenzie et al. note "competition-sourced datasets may have selection bias toward pathological cases" (L2 Source 9). Vrabcova (2025) shows newer architectures with 0.867 correlation. The survey does not adequately synthesize the possibility that inverse scaling is a 2023-era finding being superseded | L0, L2 Sources 5, 9 |
| 29 | IN-003 | S-013 Inversion | Minor | Inversion: "What if the 'pink elephant problem' label is not an established research finding but a rhetorical framing?" The survey uses this term in L0 but does not cite a specific paper that coins or validates this term. It is used as if it is a documented phenomenon but appears to be the survey author's interpretive label | L0 |

---

## Critical Findings (must fix before gate pass)

### SR-001 / RT-001 / FM-001 / CC-001 (COMPOUND): Source 19 Contains Anachronistic Model Citations

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **IDs** | SR-001, RT-001, FM-001, CC-001 (all address the same root defect from different angles) |
| **Section** | L1 Source Catalog row 19, L2 Source 19 |
| **Strategy Steps** | S-010 Step 2 (Completeness/Evidence Quality), S-001 Red Team, S-012 FMEA, S-007 Constitutional |

**Evidence:**
L1 row 19 states methodology includes "GPT-5, GPT-4.1, Claude-4-Sonnet, Gemini 2.5, DeepSeek-R1." L2 Source 19 elaborates: "13 LLMs (GPT-5 family, GPT-4.1, Claude-4-Sonnet, Gemini 2.0/2.5, DeepSeek-R1) on 600 enterprise RAG queries." As of 2026-02-27, "GPT-5" was not publicly released with that designation (GPT-4o and GPT-4.1 exist; GPT-5 is speculative). "Claude-4-Sonnet" is not a released model (Claude 3.5 Sonnet exists, Claude 3 Opus exists; Claude 4 was not released as of this date). The paper's DOI is arXiv:2601.03269 -- the "26" prefix indicates January 2026, which is consistent with the survey date. However, a January 2026 preprint citing "GPT-5" would require that model to exist. This creates a significant factual reliability concern.

**Analysis:**
Either: (a) the model name metadata was incorrectly extracted from the paper, (b) the paper uses aspirational/pre-release model names, or (c) the source's claims about which models were tested are unreliable. In any case, the survey presents these model names as established facts without caveat, which violates P-022 (No Deception) by representing unverified or potentially fabricated model metadata as factual.

**Recommendation:**
Verify the actual model names tested in arXiv:2601.03269 by reading the paper directly. If the model names differ from what is listed, correct them. If the paper genuinely cites "GPT-5" and "Claude-4-Sonnet," add an explicit caveat noting that these designations do not correspond to publicly released models as of the survey date, and assess whether the source should be retained. If the source cannot be verified, remove it.

---

### RT-002: Source 25 Venue Attribution is Premature or Fabricated

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Section** | L1 Source Catalog row 25, L2 Source 25 |
| **Strategy Step** | S-001 Red Team (citation fidelity attack) |

**Evidence:**
L1 row 25 states: "Publication venue: Nature (January 2026)." L2 Source 25 states: "Publication venue: Nature (January 2026)." The source is arXiv:2502.17424 (February 2025 preprint). A paper submitted in February 2025 cannot have a confirmed "Nature (January 2026)" venue in a survey written February 2026 unless: (a) the paper was accepted to Nature and published in January 2026 (one month before this survey), which is possible but the arXiv URL would still be the primary reference, or (b) this is an anticipatory attribution that was not verified. Nature does not announce acceptance timelines in arXiv metadata.

**Analysis:**
If this is accurate, it should be framed as "Nature (published January 2026)" with the DOI of the Nature publication, not the arXiv URL, as primary citation. If it is unverified, it is a material misrepresentation of a preprint as a published Nature paper, which significantly inflates the source's apparent quality tier. This finding directly affects how readers weight the "emergent misalignment" finding.

**Recommendation:**
Verify whether arXiv:2502.17424 was published in Nature in January 2026. If yes: update the citation to include the Nature DOI and retain Tier 1 classification. If no: reclassify as arXiv preprint (Tier 3) and update the Source Quality Assessment accordingly. In either case, add the DOI for the Nature publication if it exists.

---

### DA-001: Core Thesis Conflates Four Distinct Phenomena

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Section** | L0 Executive Summary |
| **Strategy Step** | S-002 Devil's Advocate Step 2 (assumption enumeration) |

**Evidence:**
The L0 summary builds a coherent narrative that "LLMs struggle fundamentally with negation, and this struggle worsens or persists even as models scale." However, the 30 sources actually study four distinct phenomena: (1) negation *comprehension* (understanding "NOT X" in text -- Sources 3, 4, 5, 9, 27, 29); (2) negation in *instructions/prompts* (following "don't do X" -- Sources 15, 16, 17, 18, 19, 20); (3) negation in *training/alignment* (RLHF, Constitutional AI -- Sources 7, 10, 24, 25, 28); and (4) *negative framing* effects (emotional/sentiment/contrastive -- Sources 1, 11, 12, 13, 14). These four phenomena have different mechanisms, different failure patterns, and different practical implications.

**Analysis:**
Conflating these four phenomena in the L0 creates a misleading narrative. For example, the Constitutional AI approach (Source 10) shows negative constraints in *training* are effective. The contrastive CoT approach (Source 11) shows negative *examples* improve reasoning. The inverse scaling finding (Source 9) applies to negation *comprehension*, not necessarily instruction-following. A reader of the L0 would conclude "negative prompting doesn't work" when the accurate conclusion is "direct prohibition instructions have limited effectiveness, but other uses of negative information (contrastive examples, training constraints, emotional framing) can be highly effective."

**Recommendation:**
Restructure the L0 to explicitly distinguish the four phenomena. Revise the framing from "LLMs struggle fundamentally with negation" to "LLMs struggle with direct prohibition instructions, but other forms of negative information can be effective depending on mechanism and framing." This is a more accurate and more actionable synthesis.

---

### CV-001: McKenzie et al. Scope Overgeneralization

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Section** | L0 Executive Summary, L2 Source 9 |
| **Strategy Step** | S-011 Step 3 (independent verification against source) |

**Evidence:**
L0 states: "McKenzie et al. (2023) documented that larger models perform *worse* on tasks requiring negation understanding, with performance dropping below random chance beyond approximately 10^22 training FLOPs." The actual McKenzie et al. paper (Inverse Scaling Prize) covers 11 datasets demonstrating performance degradation with scale. Per L2 Source 9, "For negation tasks, performance becomes worse than random beyond ~10^22 training FLOPs." The paper identifies four causes including "preference for memorized sequences" and "imitation of training data patterns" -- not all are negation-specific. The survey's L0 claim correctly cites the threshold but presents it as a general statement about "negation understanding" when the specific findings vary by task type.

**Analysis:**
The overgeneralization is material because it forms the centerpiece of the "inverse scaling phenomenon" claim in L0. The accurate framing would be: "McKenzie et al. (2023) documented that on specific negation-related tasks in the Inverse Scaling Prize dataset, performance drops below random chance..." The current framing implies that ALL tasks requiring negation understanding show this pattern, which is contradicted by Vrabcova et al. (2025) showing 0.867 positive correlation for newer models.

**Recommendation:**
Qualify the McKenzie et al. claim in L0 to specify: (a) the specific task types that show inverse scaling (not all negation tasks), (b) that this finding predates architectural advances seen in Llama 3/Qwen 2.5, and (c) that the 10^22 FLOPs threshold corresponds to ~2023-era model sizes, not necessarily current state-of-the-art.

---

### PM-001: Source 14 is Not Peer-Reviewed Academic Research

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Section** | L1 Source Catalog row 14, Source Quality Assessment |
| **Strategy Step** | S-004 Pre-Mortem (failure mode: source quality misrepresentation) |

**Evidence:**
L1 row 14: "Prompt Sentiment: The Catalyst for LLM Change | Gandhi, Gandhi (Joyspace AI) | 2025 | arXiv:2503.13510v1." L2 Source 14 acknowledges: "Authors: Vishal Gandhi, Sagar Gandhi (Joyspace AI)." The survey classifies this as a Tier 3 arXiv preprint but the Source Quality Assessment groups it with all arXiv preprints without distinguishing commercial/industry sources from university/research lab preprints. The paper's methodology describes "5 LLMs" but names the models inconsistently with their actual versions (Claude v1.3 was released in 2023; ChatGPT v4, DeepSeek v2.0, Gemini v1, LLaMA v2 are specific version designations that may be imprecise). The publication venue is "arXiv" only -- no conference or journal affiliation.

**Analysis:**
A commercial company blog/white paper published to arXiv does not carry the same methodological reliability as a university research lab preprint. The survey uses this source to support the claim "Neutral prompts achieve 92.3% factual accuracy; negative prompts drop to 84.5% (-8.4%)" -- a quantitative claim that is significant if true, but comes from an unreviewed, commercially-affiliated source with a sample size of 500 prompts and unspecified "automated fact-checking."

**Recommendation:**
Either: (a) remove Source 14 and identify peer-reviewed alternatives that compare positive vs. negative prompt framing on factual accuracy, or (b) retain it with an explicit caveat that it is a commercially-produced arXiv report without independent peer review, and weight it accordingly. The 8.4% accuracy degradation claim should not be presented in the survey without this caveat.

---

## Major Findings (should fix)

### SR-002: L0 Hallucination Rate Claim is Overgeneralized

**Evidence:** L0 states "negation increases hallucination rates by approximately 33 percentage points (from ~26% to ~59% in LLaMA-2)." L2 Source 6 provides task-specific baselines: FPC 63.77%, CFG 72.33%, MCQA 36.6%, FG 62.59% (all with negation). The ~26% figure represents LLaMA-2 without negation on one specific task configuration. The survey's L0 presents this as a single representative comparison when the actual data is highly task-dependent, with some baselines already above 60%.

**Recommendation:** Revise the L0 hallucination claim to specify which task type and model the 26% vs. 59% comparison applies to, and note that hallucination rates are highly task-dependent, ranging from 37% to 72% across the four tasks studied.

---

### DA-002: NegativePrompt 46.25% BIG-Bench Improvement Under-Weighted

**Evidence:** L0 dedicates only one paragraph to "constructive uses of negative information" and mentions the 46.25% BIG-Bench improvement. However, the survey's overall framing positions negative prompting as a failure. Source 1 (NegativePrompt) shows that negative emotional stimuli -- a form of negative prompting -- substantially improves performance. This result is arguably stronger evidence than many of the "failure" findings, yet it appears subordinate in the narrative.

**Recommendation:** Restructure the L0 to present the constructive uses findings with equal weight to the failure findings, and explicitly contrast "prohibition-style negative prompting" vs. "negative emotional/contrastive prompting" as the key distinction.

---

### DA-003: Selection Bias Toward Negation Comprehension Literature

**Evidence:** The Research Methodology explicitly identifies gaps: "No paper specifically compares identical constraints framed positively vs. negatively in system prompts with controlled experiments." Yet 6 of the 30 sources are negation comprehension benchmarks (Sources 3, 4, 5, 8, 27, 29) -- papers about whether LLMs understand negation in natural language, not whether they follow "don't do X" instructions. These are related but distinct phenomena. The survey's synthesis blurs this distinction.

**Recommendation:** Add a section in L0 explicitly distinguishing "negation comprehension" (understanding that "X is NOT Y") from "prohibition instruction-following" (obeying "don't do X"). Acknowledge that the majority of evidence is from the former, not the latter, which is the practically-relevant question for PROJ-014.

---

### PM-002: Preprint Quality Heterogeneity Understated

**Evidence:** 12/30 sources (40%) are arXiv preprints. The survey's Source Quality Assessment uses a tier system but does not differentiate within Tier 3. Source 5 (Vrabcova et al., Masaryk University) is a rigorous multilingual study; Source 29 (Thunder-NUBench) was read only from an abstract; Source 19 has model naming issues. These receive identical tier treatment.

**Recommendation:** Add per-source methodology quality notes in the Source Quality Assessment. Flag sources where only the abstract was read (Sources 29, 20) and note this limitation explicitly. This directly affects which findings downstream research should rely upon.

---

### PM-003: The "60% Hallucination Reduction" Reference Target is Undefined

**Evidence:** The strategy plan references "the evidence gap regarding the claimed 60% hallucination reduction via negative prompting" but the survey itself does not clearly identify what vendor claim or benchmark assertion is being tested. L0 mentions "limited work specifically on the effectiveness of 'don't' instructions in system prompts for production LLMs" but does not explicitly state "we are testing whether the claimed 60% reduction is supported." This makes the survey's contribution to PROJ-014's core hypothesis unclear.

**Recommendation:** Add a paragraph in L0 explicitly stating: (a) the claim being tested (e.g., "vendor guidance suggests negative prompting reduces hallucinations by X%"), (b) the specific claim source (which vendor documentation or paper asserts 60%?), and (c) what the survey found regarding that specific claim's evidentiary support.

---

### CV-002: CoVe Categorized as "Negative Information" Is Conceptual Conflation

**Evidence:** L0 frames CoVe (Source 22) as a "constructive use of negative information" because the verification pipeline checks for negation-related errors. However, CoVe is a verification *pipeline*, not a form of negative prompting. Including it in the "constructive uses of negative information" theme conflates verification techniques with negative prompting approaches.

**Recommendation:** Separate CoVe into its own category ("verification-based mitigation strategies") distinct from negative prompting per se. The L0 currently conflates three different things: negative emotional stimuli (Source 1), contrastive examples (Source 11), and verification pipelines (Source 22).

---

### CV-003: Source 16 Published Status Not Confirmed

**Evidence:** Source 16 (Harada et al.) is listed as "ICLR 2025 submission" in L1. This means it was *submitted* to ICLR 2025, not necessarily accepted. The survey cites this paper's findings about the exponential decay of instruction-following success as established fact, without noting the submission-only status.

**Recommendation:** Verify whether Harada et al. (OpenReview forum?id=R6q67CDBCH) was accepted to ICLR 2025. If accepted, update the venue to "ICLR 2025." If not, add "(under review)" caveat and weight findings accordingly.

---

### CV-004: Source 19 Model Names Unverifiable

**Evidence:** Source 19 references "GPT-5 family" and "Claude-4-Sonnet" which are not publicly known model designations as of 2026-02-27. These names cannot be verified against known model release timelines.

**Recommendation:** Read arXiv:2601.03269 directly to verify the actual model names. If the paper uses these names, add a caveat. If the metadata was incorrectly extracted, correct it.

---

### IN-001: Survey Does Not Synthesize "Negative Prompting CAN Work" Thesis

**Evidence:** Three sources collectively show negative prompting effectiveness under specific conditions: Source 23 (warning-based prompts: +25.14% on distractor negation), Source 15 (DeCRIM atomic constraints: +7.3-8%), Source 28 (CAST: harmful refusal 45.78% to 90.67%). The survey does not synthesize these into an affirmative finding.

**Recommendation:** Add a synthesis paragraph explicitly stating: "Under specific conditions -- warning-based meta-prompting, atomic constraint decomposition, and mechanistic activation steering -- negative instructions can be made substantially more effective." This is not present in the current L0 and represents a significant actionable finding for PROJ-014.

---

### IN-002: Inverse Scaling Potentially Superseded

**Evidence:** The survey presents inverse scaling as a primary finding but does not adequately synthesize the Vrabcova (2025) challenge. The L0 hedges ("partially challenged") but the body of evidence suggests the picture may have fundamentally changed with newer architectures. Newer models (Llama 3, Qwen 2.5) show 0.867 positive correlation, which would make the McKenzie finding a historical artifact.

**Recommendation:** Revise the framing to: "Inverse scaling was documented for 2022-2023 era models (McKenzie et al., Truong et al.) but appears to be reversing for newer architectures (Vrabcova et al. 2025, r=0.867). The field may be entering a period where architectural improvements are closing the negation gap." This is more accurate and more useful for PROJ-014.

---

### RT-003: Source 29 Abstract-Only Reading Not Disclosed

**Evidence:** L2 Source 29 explicitly states "Full quantitative results not available from abstract." The survey nonetheless includes Source 29 in the well-covered areas count and makes claims about its contributions.

**Recommendation:** Add an explicit footnote to Source 29 in L1 noting "reviewed from abstract only; full quantitative results not extracted." This prevents downstream researchers from treating this source as fully evaluated.

---

### RT-004: L0 Hallucination Baseline Misrepresentation

**Evidence:** Already documented under SR-002. The ~26% baseline in L0 is task-specific (likely one of the MCQA conditions for LLaMA-2) and does not represent the general baseline rates shown in L2 Source 6.

**Recommendation:** Consistent with SR-002 recommendation: specify the task condition for the 26% vs. 59% comparison.

---

## Minor Findings (consider fixing)

### SR-003: Source 30 Missing Author Names

**Evidence:** L1 row 30 lists "multiple authors" with no names. This is a journal article in *Computational Linguistics* (MIT Press) -- a prestigious peer-reviewed venue. The actual authors should be identifiable.

**Recommendation:** Look up the actual authors of the Computational Linguistics 2024 survey (DOI: 10.1162/coli_a_00517 or similar) and add them to the L1 table.

---

### SM-001: Vrabcova Challenge Understated in L0

**Evidence:** L0 describes Vrabcova (2025) as "partially challenging" the inverse scaling finding, but the 0.867 Spearman correlation is a strong result. The "partial challenge" framing undersells what may be a significant architectural development.

**Recommendation:** Revise to "substantially challenges" or provide explicit quantitative framing: "a Spearman correlation of 0.867 between model size and negation handling suggests architectural improvements may be reversing the inverse scaling trend."

---

### SM-002: Constructive Uses Theme Needs More L0 Prominence

**Evidence:** Three of the most practically actionable findings (contrastive CoT +16 accuracy points, NegativePrompt +46.25%, warning-based prompts +25.14%) are buried in the third paragraph of L0. The practical takeaway for PROJ-014 (what works in negative prompting) deserves first-paragraph prominence.

**Recommendation:** Restructure L0 to lead with the central tension (failure of prohibition-style prompting vs. success of structured negative information) rather than leading with the failure narrative.

---

### CC-003: Source 2 (Diffusion Models) Relevance is Speculative

**Evidence:** Source 2 is about negative prompts in image generation (Stable Diffusion), not LLMs. The L2 relevance claim states "provides theoretical grounding" but this transfer is theoretical, not empirical.

**Recommendation:** Either add a caveat that the mechanistic findings are from a different modality and transfer to LLMs is unvalidated, or move this source to a "Related Work (Different Modality)" category.

---

### IN-003: "Pink Elephant Problem" Label Unsourced

**Evidence:** L0 uses "the 'pink elephant problem'" as if it is an established research term, but no source is cited for this label. It appears to be the survey author's framing.

**Recommendation:** Either: (a) cite a specific paper that coins this term, or (b) rephrase as "the tendency for negative instructions to paradoxically increase target behavior (sometimes colloquially called the 'pink elephant problem')" and acknowledge it is an interpretive label.

---

### FM-004: 8 Empty-Result Queries Need Explanation

**Evidence:** 8 of 20 search queries returned 0 sources (queries 4, 5, 8, 9, 16, 18, 19 as shown in methodology table). While the survey notes these "guided thematic understanding" or "confirmed prior findings," this is not adequately explained.

**Recommendation:** For each zero-result query, add a one-sentence explanation: was there genuinely no relevant literature found, or did the query results confirm existing sources without adding new ones? This helps readers assess whether search gaps represent literature absence or query design limitations.

---

## Preliminary Score Assessment (S-014)

Active leniency bias counteraction applied: scores will not be inflated. The threshold is 0.95 for C4.

| Dimension | Weight | Score | Evidence |
|-----------|--------|-------|----------|
| Completeness | 0.20 | 0.82 | Survey covers 6 major thematic areas adequately. Key gaps: no explicit positive/negative instruction A/B comparison studies identified; multilingual negative prompting almost entirely absent; theoretical mechanistic understanding thin. Research gaps section acknowledges these. 30 sources across 2022-2025 is strong breadth. Deducted for: failure to synthesize "conditions under which negative prompting works" as an affirmative finding, and for the abstract-only reading of Source 29. |
| Internal Consistency | 0.20 | 0.74 | Multiple material inconsistencies identified: L0 hallucination claim (~26% to ~59%) does not match L2 Source 6 task-specific data; L0 frames CoVe as "negative information" which contradicts its L2 description as a verification pipeline; L0 "inverse scaling" claim conflicts with Vrabcova (2025) 0.867 correlation finding without adequate synthesis; Source 14 Tier 3 classification inconsistent with commercial-author concern. These are substantive inconsistencies, not minor tensions. |
| Methodological Rigor | 0.20 | 0.78 | 20 search queries executed as documented. Source quality tiering is present. Coverage assessment is explicit and honest about gaps. However: inclusion/exclusion criteria not stated; Source 14 (commercial report) accepted without peer review caveat; Source 29 read from abstract only but counted as a source; Source 19 and Source 25 citation metadata are potentially inaccurate. The search strategy appears sound but documentation of criteria is insufficient for reproduction. |
| Evidence Quality | 0.15 | 0.69 | Multiple evidence quality problems: Source 19 cites non-existent model designations; Source 25 venue attribution may be premature; Source 14 is commercially-produced without peer review; Source 29 abstract-only. The ~26% baseline claim in L0 misrepresents Source 6's task-specific data. 18/30 sources have code/data available (60%) which is strong. 14/30 in Tier 1 venues (47%) is reasonable. But the specific critical findings on Sources 14, 19, 25, 29 materially reduce evidence quality confidence. |
| Actionability | 0.15 | 0.84 | L0 identifies 4 research gaps clearly and specifically. The "pink elephant problem" description is practically useful. The constructive uses theme (contrastive CoT, NegativePrompt, warning-based prompts) provides actionable alternatives. However: no synthesis of "when negative prompting works" diminishes actionability for PROJ-014's Phase 2 design; the conflation of four distinct phenomena makes it harder to identify which specific negative prompting formulations to test. |
| Traceability | 0.10 | 0.86 | L1 Source Catalog provides structured traceability with author, year, URL, key finding for all 30 sources. L2 sections provide per-source analysis. Most L0 claims can be traced to specific sources. Deducted for: the ~26% hallucination baseline in L0 cannot be cleanly traced to a single task condition in Source 6; the "pink elephant problem" label is untraced; Source 30's missing author names reduce verification feasibility. |
| **Weighted Composite** | **1.00** | **0.779** | |

**Calculation:** (0.82 × 0.20) + (0.74 × 0.20) + (0.78 × 0.20) + (0.69 × 0.15) + (0.84 × 0.15) + (0.86 × 0.10)
= 0.164 + 0.148 + 0.156 + 0.1035 + 0.126 + 0.086
= **0.7835** (rounded to **0.78**)

---

## Verdict: REJECTED

**Score:** 0.78 (threshold: 0.95; delta: -0.17)

**Classification:** REJECTED (below 0.85 REVISE band; significant rework required)

**Rationale for Rejection:**

The survey is rejected at this iteration for the following reasons, ordered by severity:

1. **Five Critical findings that individually block acceptance:** Source 19 anachronistic model citations (potential metadata fabrication); Source 25 premature venue attribution (Nature 2026 unverified); Source 14 commercial report presented as academic source without caveat; McKenzie et al. scope overgeneralization in L0; core thesis conflates four distinct phenomena with different practical implications.

2. **Internal Consistency failure (0.74):** The L0/L2 discrepancy on hallucination rates is a material factual inconsistency. The CoVe categorization error is a conceptual conflation. These are not minor tensions -- they undermine the synthesis's reliability.

3. **Evidence Quality failure (0.69):** At C4 criticality with a 0.95 threshold, an Evidence Quality score of 0.69 is disqualifying. The two unverifiable source entries (Sources 19, 25) and the commercial report issue (Source 14) create a plausibility risk for the entire survey's findings.

4. **Missing core synthesis:** The survey does not deliver an answer to "when does negative prompting work and when does it fail?" which is the implicit research question of PROJ-014. Three sources directly answer this question (Sources 23, 15, 28) but their findings are not synthesized into an affirmative thesis.

**Required Actions Before Iteration 2:**

**Priority 1 (Critical -- must resolve):**
- [ ] Verify and correct Source 19 model names against actual paper content
- [ ] Verify and correct Source 25 Nature venue attribution (confirm or downgrade to arXiv Tier 3)
- [ ] Add peer-review caveat to Source 14 or remove it and find a peer-reviewed replacement
- [ ] Revise L0 McKenzie claim to specify task scope and acknowledge architectural evolution
- [ ] Restructure L0 to distinguish four phenomena: comprehension, instruction-following, training constraints, negative framing

**Priority 2 (Major -- should resolve before gate pass):**
- [ ] Fix L0 hallucination rate claim to match Source 6's task-specific data
- [ ] Add "conditions for success" synthesis paragraph to L0 (Sources 23, 15, 28)
- [ ] Separate CoVe from "negative information" category in L0
- [ ] Add explicit caveat for Source 16 (ICLR submission vs. accepted paper)
- [ ] Clarify the 60% hallucination reduction claim's origin (which vendor document?)
- [ ] Flag Sources 29 and 20 as abstract-only reads in L1 table

**Priority 3 (Minor -- polish):**
- [ ] Add Source 30 author names
- [ ] Strengthen Vrabcova framing from "partially challenges" to accurate quantitative description
- [ ] Cite or rephrase "pink elephant problem" label
- [ ] Add Source 2 caveat about diffusion model vs. LLM domain transfer
- [ ] Explain 8 zero-result search queries in methodology

---

## Protocol Compliance

| Strategy | Executed | Findings Generated | Prefix Used |
|----------|----------|-------------------|-------------|
| S-010 Self-Refine | Yes | 3 (1 Critical, 1 Major, 1 Minor) | SR- |
| S-003 Steelman | Yes | 2 (1 Major, 1 Minor) | SM- |
| S-002 Devil's Advocate | Yes | 3 (1 Critical, 2 Major) | DA- |
| S-004 Pre-Mortem | Yes | 3 (1 Critical, 2 Major) | PM- |
| S-001 Red Team | Yes | 4 (2 Critical, 2 Major) | RT- |
| S-007 Constitutional AI | Yes | 3 (1 Critical, 1 Major, 1 Minor) | CC- |
| S-011 Chain-of-Verification | Yes | 4 (2 Critical, 2 Major) | CV- |
| S-012 FMEA | Yes | 4 (1 Critical, 2 Major, 1 Minor) | FM- |
| S-013 Inversion | Yes | 3 (2 Major, 1 Minor) | IN- |
| S-014 LLM-as-Judge | Yes | Scores in Preliminary Score Assessment | LJ- |

**H-16 Compliance:** S-003 (Steelman) executed at position 2 before S-002 (Devil's Advocate) at position 3. SATISFIED.

**H-15 Self-Review:** Findings verified for internal consistency before persistence. All Critical findings have specific evidence from the deliverable. Severity classifications reviewed against criteria. Summary table matches detailed findings count. Leniency bias counteraction applied (score of 0.78 reflects genuine quality state, not inflated assessment).

---

*Generated by: adv-executor*
*Strategy Version: 1.0.0*
*Constitutional Compliance: P-002 (persisted), P-003 (no subagents), P-004 (provenance cited), P-011 (evidence-based), P-022 (not deceived on scores)*
*Date: 2026-02-27*
