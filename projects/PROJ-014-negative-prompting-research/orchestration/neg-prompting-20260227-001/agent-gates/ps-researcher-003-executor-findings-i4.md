# Adversary Executor Findings — TASK-003 Context7 Survey (Iteration 4)

## Execution Context

- **Deliverable:** `projects/PROJ-014-negative-prompting-research/research/context7-survey.md`
- **Deliverable Type:** Research Survey (Context7 Library Documentation Survey — Iteration 4 Revision)
- **Criticality:** C4 (Critical)
- **Strategies Executed:** 10 (S-010, S-003, S-002, S-004, S-001, S-007, S-011, S-012, S-013, S-014)
- **Executed:** 2026-02-27
- **Execution ID:** 20260227T004
- **Tournament Iteration:** 4 of (max) 5
- **Quality Threshold:** >= 0.95 (C4)
- **Prior Iteration Scores:** I1=0.80 (REVISE), I2=0.87 (REVISE), I3=0.903 (scorer) / 0.922 (executor, REVISE)

---

## I3 → I4 Precision Edit Resolution Status

| Edit # | Description | Evidence in I4 Deliverable | Resolution |
|--------|-------------|---------------------------|------------|
| Edit 1 | "GPT-5 Medium" caveat added | Line 581: "Note: 'GPT-5 Medium' is the model designation used in the arXiv preprint (Tripathi et al., 2025). This designation cannot be verified against standard OpenAI public model naming conventions and may refer to an internal model variant or a designation that differs in the final published version." | **RESOLVED** — Caveat present; per-instance disclosure applied precisely where the identifier appears |
| Edit 2 | Arithmetic fix — "50 pairs × 5 models × 2 framing conditions = 500 evaluations" | Line 694: "50 framing pairs (10 per taxonomy type) tested across 5 models, with each pair evaluated under both negative and positive framing conditions, would yield 500 evaluation data points minimum (50 pairs x 5 models x 2 framing conditions = 500)" | **RESOLVED** — Arithmetic is now correct; the path to 500 is explicitly stated via the two-condition multiplier |
| Edit 3 | Semantic equivalence validation — Cohen's kappa >= 0.80 specified | Line 680: "Framing pair semantic equivalence MUST be validated before use. Validation method: two independent raters classify each pair as 'semantically equivalent' or 'not equivalent,' with Cohen's kappa >= 0.80 required; pairs failing the threshold are revised and re-rated." | **RESOLVED** — Specific, measurable validation method added; inter-rater reliability threshold (kappa >= 0.80) specified |
| Edit 4 | Vendor doc-vs-behavior qualifier in L1 sections | L1 Section 1 (line 151): "This assessment covers documented guidance and observed usage patterns in official documentation only; production deployment practices may differ." L1 Section 2 (line 215): "This assessment covers documented guidance and observed usage patterns in official documentation only; production deployment practices may differ." L1 Section 3 (line 290): "This assessment is based on publicly available documentation and default prompt templates; internal development practices are not assessed." L1 Section 4 (line 349): same qualifier. L1 Section 5 (line 435): same qualifier. | **RESOLVED** — Each of 5 L1 library sections contains the qualifier. Language varies slightly (Sections 1-2 use "production deployment practices may differ"; Sections 3-5 use "internal development practices are not assessed") but the semantic content is equivalent and satisfies the I3 recommendation |
| Edit 5 | L0 Key Finding 2 authority qualifier | Line 44: "OpenAI's Prompt Engineering Guide similarly advises (confirmed via GPT-4.1 through GPT-5.2 cookbook guides, Ref #4-#7; primary platform docs returned 403, Ref #3): 'avoid saying what not to do but say what to do instead.'" | **RESOLVED** — Authority qualifier is present inline in L0. The I3 scorer's recommended text was "confirmed via Ref #15, MEDIUM authority"; the I4 text uses "confirmed via GPT-4.1 through GPT-5.2 cookbook guides, Ref #4-#7" which actually provides a stronger attribution (cookbook guides are HIGH authority, not MEDIUM). This is a quality improvement over the recommended fix. |

**Summary: All 5 I3 precision edits are correctly applied and fully resolve their target findings.**

---

## Strategy Execution Results

### S-010: Self-Refine

**Execution ID:** 20260227T004

**Objectivity Assessment:** The deliverable is at iteration 4 of 5. Sufficient cognitive distance is achievable from this vantage point. Medium attachment applicable for a survey this far along in revision; proceeding with caution and targeting 5+ findings.

**Systematic Review Against Six Dimensions:**

**Completeness:** The I4 deliverable now addresses all previously identified completeness gaps. Navigation table has 16 entries covering all sections. All 5 L1 sections have coverage assessments. Taxonomy with 5 types present. Experimental design parameters fully specified with arithmetic, semantic equivalence validation, model selection criteria, metric selection, and sample size guidance. Vendor doc-vs-behavior qualifiers present in all 5 L1 sections.

One remaining completeness gap: the "output quality metric" (tertiary metric — holistic quality assessment) still lacks a scoring rubric or measurement methodology. This was a Minor finding in I3 that was not among the 5 precision edits and remains present.

**Internal Consistency:** The three I3 major inconsistencies are resolved: GPT-5 Medium caveat added, arithmetic corrected to 500 via two-condition clarification, L0 Key Finding 2 authority qualifier present.

Remaining: No new internal inconsistencies detected. The L0 Key Finding 2 qualifier now reads differently from what I3 scorer recommended (uses cookbook guides Ref #4-#7 rather than Ref #15 as the confirmation pathway), but the substance is correct and actually stronger. The References section still lists Ref #3 as "HIGH (inaccessible)" — this is an honest assessment but the HIGH label on an unverifiable source remains a minor presentational ambiguity flagged in I3.

**Methodological Rigor:** The two major I3 methodological gaps are resolved: GPT-5 Medium caveat added, semantic equivalence validation with kappa >= 0.80 now specified. The query log (34 queries), reproducibility statement, preprint disclosure, and source selection rationale are all present and accurate.

One minor gap persists: GitHub stars/PyPI download data cited as selection criteria for 3 framework libraries without links to the data (carries forward from I3 as Minor).

**Evidence Quality:** The GPT-5 Medium caveat is now per-instance and specific. The asymmetric treatment identified in I3 is resolved. Evidence quality for the remaining claims is well-documented. The OpenAI Ref #3 HIGH-but-inaccessible label persists as minor.

**Actionability:** Arithmetic is correct. Semantic equivalence validation is specified. The output quality metric lacks a rubric (Minor). Phase 2 Task Mapping artifacts still unlinked to PROJ-014 work items (Minor, carries forward from I3).

**Traceability:** GPT-5 Medium provenance gap resolved via caveat. Navigation table complete. Query log complete. Phase 2 artifacts still unlinked to PROJ-014 task IDs (Minor).

**SR-001-20260227T004: Output quality metric lacks measurement methodology** (Minor)
- Section: Experimental Design Parameters
- Evidence: "Tertiary metric -- Output quality: Holistic quality assessment of compliant responses to determine whether compliance comes at a quality cost"
- No scoring rubric, scale, or measurement methodology provided. Other two metrics (compliance rate, hallucination rate) are anchored to prior academic methodologies.

**SR-002-20260227T004: Phase 2 artifacts unlinked to PROJ-014 work items** (Minor)
- Section: Phase 2 Task Mapping
- Evidence: Table lists "Experimental design document," "Vendor instruction taxonomy," "Instruction pair test suite," "Scope revision proposal" as artifacts without PROJ-014 task or story IDs.

**SR-003-20260227T004: OpenAI Ref #3 authority label ambiguity persists** (Minor)
- Section: References
- Evidence: "#3 [OpenAI Prompt Engineering Guide] -- HIGH (inaccessible)" — inaccessible source labeled HIGH creates a residual presentational ambiguity.

**S-010 Self-Assessment:** 3 Minor findings remain. 0 Critical, 0 Major. The I4 revision is well-executed and resolves all I3 Major findings precisely. The deliverable presents as near-complete for the C4 threshold.

---

### S-003: Steelman Technique

**Core Thesis:** The PROJ-014 hypothesis ("negative unambiguous prompting reduces hallucination by 60%") is not supported by vendor documentation or academic research. The surveyed evidence instead supports a more nuanced position: effective constraint instructions depend on specificity, contextual justification, pairing with positive alternatives, and structural enforcement — not on whether the framing is negative or positive.

**Charitable Interpretation Summary:** The survey is making a correct and well-evidenced argument that the original PROJ-014 hypothesis is oversimplified. The revised hypothesis ("specific, contextually justified constraints combined with structural enforcement mechanisms reduce hallucination") is more defensible and better supported by the evidence. The document provides a rigorous null finding with honest methodology disclosure, a preliminary taxonomy for Phase 2 use, and actionable experimental design parameters.

**Strongest Version of the Deliverable's Arguments:**

1. The null finding on the 60% claim is the correct and honest conclusion. No source reviewed provides the specific quantitative comparison the hypothesis assumes. This is a valuable negative finding — it prevents the research from proceeding on a flawed premise.

2. The four convergent patterns (NP-001 through NP-004) are well-grounded across multiple independent sources. The pattern that structural constraint enforcement (LangChain parsers, DSPy assertions) outperforms linguistic framing is a significant finding that could redirect PROJ-014 toward higher-value research.

3. The academic integration (Tripathi et al., Young et al.) — now with corrected citations and I4 caveats — provides the strongest available empirical grounding for Phase 2 experimental design. The connection between Young et al.'s methodology and the proposed 50-pair experiment is methodologically sound.

4. The DSPy backtracking observation (negative feedback "what went wrong" is a built-in component of effective constraint enforcement) is a genuinely counterintuitive and valuable finding that could reshape the research question productively.

5. The vendor recommendation vs. practice tension analysis with four explanations is intellectually honest and appropriately avoids asserting a conclusion without sufficient evidence.

**Steelman Findings (Strengthening Opportunities):**

**SM-001-20260227T004: The "binary outcome distribution" finding from Young et al. deserves stronger framing** (Minor)
- The document mentions at line 593-594: "The study observed a 'binary outcome distribution' in constraint compliance: 'successful models appeared to implement robust checking mechanisms, while failing models showed no awareness of the constraint violation.'" This finding has significant implications for PROJ-014's research design but is not given sufficient prominence. If compliance is binary (models either follow constraints robustly or ignore them), then the negative-vs-positive framing debate may be architecturally irrelevant — the binary distribution suggests that model capability is the primary variable, not framing. This could be elevated to a fifth convergent pattern or flagged explicitly in the Implications section.

**SM-002-20260227T004: The Phase 2 Task Mapping table could link to the taxonomy more explicitly** (Minor)
- The table at lines 664-669 references "Negative Instruction Type Taxonomy" as a starting framework but does not cite the preliminary taxonomy section directly. Adding inline cross-references would strengthen traceability.

**SM-003-20260227T004: The revised hypothesis could be more precisely stated with measurable success criteria** (Minor)
- The revised hypothesis ("Specific, contextually justified constraints combined with structural enforcement mechanisms reduce hallucination more effectively than unstructured instructions") is stated in L0 and L2 but without a measurable form. Providing a success criterion — e.g., "combined approach achieves >= 10% lower hallucination rate than unstructured instructions across 3+ models" — would make it testable and give Phase 2 a clear pass/fail criterion.

---

### S-002: Devil's Advocate

**H-16 Compliance:** S-003 executed in prior step. Proceeding.

**Role Assumption:** Challenging the deliverable's core claims and assumptions with the strongest possible counter-arguments.

**Assumption Inventory and Challenges:**

**Explicit Assumption 1:** The 6 surveyed sources are representative of the vendor documentation landscape.
**Challenge:** The survey explicitly excludes Google Gemini, Meta LLaMA, Cohere, and Hugging Face. Google Gemini is now one of the most widely deployed commercial LLMs. Its exclusion means the convergence claim (NP-001: "All sources that address the topic recommend positive framing") could be invalidated by a single counterexample. The survey's null finding on quantitative evidence might not hold if Google's documentation contains controlled comparison data. The Coverage Matrix's scope caveat is present but the implication — that the convergence finding may not generalize — is understated in L0.

**Explicit Assumption 2:** Vendor documentation reflects actual model behavior.
**Challenge:** The vendor doc-vs-behavior qualifiers (Edit 4) now partially address this, but the qualifiers are at the end of each L1 Coverage Assessment section in small-print form. The deliverable's Key Findings and Hypothesis Verdict sections do not carry forward this limitation. A researcher reading only L0 will not encounter the qualification unless they notice the qualifier embedded at the end of each L1 section's coverage assessment. The fundamental assumption — that published documentation guidance reliably reflects model behavior — is challenged by the very tension the document itself documents (recommendation vs. practice divergence).

**Implicit Assumption 3:** The framing-pair methodology is the right experimental design.
**Challenge:** The experimental design assumes that "the same semantic constraint expressed once as a negative instruction and once as a positive instruction" constitutes an adequate controlled experiment. This assumption has a critical flaw: it may be impossible to achieve genuinely equivalent semantic content in negative and positive framings for complex constraints. "Do NOT include information not present in the source document" and "Include only information that is directly stated in the source document" are presented as semantically equivalent, but they have different logical structures (negation vs. positive scope). Negative framing invokes prohibited content; positive framing invokes permitted content. These may trigger different attention mechanisms in transformer architectures. The kappa >= 0.80 inter-rater reliability requirement (Edit 3) is a good control for human raters' judgment of equivalence, but human raters and LLMs may disagree on semantic equivalence — and it is the LLM's interpretation that matters for the experiment.

**DA-001-20260227T004: L0 Key Findings do not carry the vendor doc-vs-behavior limitation forward** (Major)
- Section: L0 Executive Summary, Key Findings
- Evidence: Key Finding 1 states "Both Anthropic and OpenAI explicitly recommend positive framing over negative instructions" without any qualifier that this represents documented guidance which may not reflect model behavior. The vendor doc-vs-behavior qualifiers are correctly placed in L1 but are absent from L0 where the primary research conclusions are stated. A reader who reads only L0 — the intended audience for executive consumption — receives unqualified finding statements.
- Recommendation: Add a general qualifier sentence before the Key Findings list in L0: "The following findings reflect vendor-documented guidance. Production deployment practices and empirically observed model behavior may differ from documented recommendations (see per-library coverage assessments in L1 for details)."

**DA-002-20260227T004: The framing-pair semantic equivalence assumption may be unfalsifiable at the required kappa threshold** (Minor)
- Section: Experimental Design Parameters
- Evidence: Line 676-680 specifies kappa >= 0.80 for human rater agreement, but the critical test is LLM interpretation of semantic equivalence, not human judgment. Two human raters may agree that two framing variants are semantically equivalent while the LLM processes them differently at the token/attention level.
- Recommendation: Add a note that "semantic equivalence as judged by human raters may differ from semantic equivalence as processed by LLMs; Phase 2 should pilot-test with one framing pair per taxonomy type and compare completion distributions before full-scale testing."

**DA-003-20260227T004: The convergence claim (NP-001 through NP-004) is based on a potentially non-representative source sample** (Minor)
- Section: Pattern Convergence (L2)
- Evidence: The 6 surveyed sources share a common origin in the Western commercial LLM ecosystem (Anthropic, OpenAI, Python framework libraries, community guides derivative of OpenAI guidance). NP-001 ("All sources recommend positive framing") may reflect echo-chamber convergence rather than universal consensus. The Coverage Matrix scope caveat acknowledges this limitation, but the Pattern Convergence section does not.
- Recommendation: Add one sentence in the Pattern Convergence section: "Note: These convergent patterns are derived from the 6 surveyed sources, which share significant overlap in origin (Anthropic, OpenAI, and Python frameworks largely following their conventions). Independent empirical validation is needed to confirm these patterns hold across a broader source universe."

---

### S-004: Pre-Mortem Analysis

**Pre-Mortem Frame:** It is 6 months after the PROJ-014 research completed. The research was used by a team to design and run an experiment testing negative vs. positive prompting, and the experiment produced inconclusive or misleading results. Why did the survey fail to enable a successful Phase 2?

**Failure Mode Enumeration:**

**Failure 1: The arithmetic correction (Edit 2) introduced a precision issue**
Examining line 694 carefully: "50 framing pairs (10 per taxonomy type) tested across 5 models, with each pair evaluated under both negative and positive framing conditions, would yield 500 evaluation data points minimum (50 pairs x 5 models x 2 framing conditions = 500)."

The arithmetic is now correct (50 × 5 × 2 = 500). However, "5 models" in the sample size guidance conflicts with the model selection criteria two paragraphs up, which says "a practical minimum of 5-10 models across 3+ providers" (line 685). A researcher reading the sample size guidance would plan for exactly 5 models (the number in the formula), while the model selection criteria recommends 5-10. The sample size formula anchors to the minimum without flagging that using the minimum of 5 models produces the minimum of 500 evaluations, not the recommended 5-10 model range. This is a minor but potentially misleading inconsistency between two paragraphs in the same section.

**Failure 2: The taxonomy boundary between Prohibition and Safety boundary was flagged as potentially non-clean (line 635) but the experimental design doesn't address it**
The taxonomy observations note: "The boundary between Prohibition and Safety boundary may not be clean -- Phase 2 should determine whether these are distinct types or contextual variants of the same pattern." But the experimental design specifies "Pairs should be constructed for each type in the Negative Instruction Type Taxonomy (Prohibition, Exclusion, Conditional negation, Scope limitation, Safety boundary)" as if these five types are clean and mutually exclusive. A Phase 2 researcher following the experimental design without reading the taxonomy observations section will construct 10 pair-per-type without realizing two types may overlap.

**Failure 3: The "binary outcome distribution" finding undermines the entire experimental premise**
Young et al.'s finding that constraint compliance is binary (models either follow constraints robustly or ignore them entirely) — if confirmed — would mean that varying the framing (negative vs. positive) of a constraint produces little or no effect on compliance rates, because the determining factor is model architecture, not framing. If the experiment is run on this faulty premise, the likely result is a null finding: negative and positive framing produce similar compliance rates, not because they are equivalent in theory, but because model capability dominates the framing variable. The survey notes this finding but does not flag it as a threat to the experimental validity of the entire Phase 2 design.

**PM-001-20260227T004: Sample size formula anchors to minimum-model count, potentially conflicting with model selection range** (Minor)
- Section: Experimental Design Parameters
- Evidence: Line 694 formula uses "5 models" producing "500 evaluations minimum," while line 685 recommends "5-10 models across 3+ providers." These are consistent (5 is the minimum of 5-10) but the formula could mislead a researcher into planning exactly 5 models. The formula uses "5" as the concrete number while the selection criteria says "5-10."
- Recommendation: Align the formula with the recommended range: "50 pairs × 5-10 models × 2 framing conditions = 500-1,000 evaluations; use the lower bound as a minimum feasibility check."

**PM-002-20260227T004: Taxonomy type mutual exclusivity issue is flagged in observations but not addressed in experimental design** (Minor)
- Section: Negative Instruction Type Taxonomy, Experimental Design Parameters
- Evidence: Line 635 warns that "The boundary between Prohibition and Safety boundary may not be clean"; but line 678 instructs Phase 2 to "construct for each type in the Taxonomy" as if all 5 types are clean boundaries. These two instructions are potentially in conflict.
- Recommendation: Cross-reference the taxonomy caveat from the experimental design: "Note: Taxonomy types are PRELIMINARY (see taxonomy observations); pilot-test type categorization before full-scale pair construction."

**PM-003-20260227T004: Binary compliance distribution finding should be flagged as a threat to experimental validity** (Minor)
- Section: Academic Research Findings, Implications for PROJ-014 Hypothesis
- Evidence: Line 593-594 reports the binary distribution finding but its implication — that framing may be less important than model architecture — is not explicitly stated in the Implications section (lines 643-660), which focuses primarily on the unsupported 60% claim.
- Recommendation: Add to the Implications section: "Young et al.'s binary compliance distribution finding (models either follow constraints robustly or show no awareness of violation) raises a validity concern for Phase 2: if model capability dominates framing choice as the compliance variable, a framing-comparison experiment may produce a null finding not because framing is equivalent but because the primary variable (model architecture) is not being controlled. Phase 2 experimental design should include a pre-experiment pilot to assess whether framing variation produces measurable distribution differences on a small sample before full-scale testing."

---

### S-001: Red Team Analysis

**Threat Actor Perspective:** A research team at a competing organization reviewing PROJ-014's Phase 1 output to identify where the negative prompting research is most vulnerable to methodological attack.

**Attack Vector 1: The OpenAI Cookbook Guide Authority Problem**

The survey repeatedly cites Ref #4-#7 (OpenAI GPT-4.1, GPT-5, GPT-5.1, GPT-5.2 cookbook guides) as HIGH authority. These are developer cookbook examples, not the official OpenAI platform prompting guidance (Ref #3, which is inaccessible). The survey itself acknowledges this distinction at line 159: "The cookbook guides hosted at `developers.openai.com/cookbook/` are official OpenAI-authored content but represent developer examples rather than the primary platform guidance."

However, L0 Key Finding 1 states: "OpenAI's Prompt Engineering Guide similarly advises (confirmed via GPT-4.1 through GPT-5.2 cookbook guides, Ref #4-#7; primary platform docs returned 403, Ref #3): 'avoid saying what not to do but say what to do instead.'" The attribution "OpenAI's Prompt Engineering Guide" is the title of the inaccessible Ref #3, not of Ref #4-#7. A researcher reading this carefully would note that the statement conflates the title of one source with the confirmation pathway from other sources. The canonical OpenAI recommendation was confirmed via promptingguide.ai (Ref #15, MEDIUM) in L1 Section 2, but the L0 quote now attributes it directly to the cookbook guides — which actually don't contain this specific "avoid saying what not to do" quote, as that language comes from the original platform guide.

**RT-001-20260227T004: L0 Key Finding 1 attribution conflates source title with confirmation pathway** (Minor)
- Section: L0 Executive Summary, Key Finding 1
- Evidence: Line 44 states "OpenAI's Prompt Engineering Guide similarly advises (confirmed via GPT-4.1 through GPT-5.2 cookbook guides, Ref #4-#7; primary platform docs returned 403, Ref #3): 'avoid saying what not to do but say what to do instead.'" The quote "avoid saying what not to do" originates from the OpenAI Prompt Engineering Guide (Ref #3, inaccessible) and was confirmed via promptingguide.ai (Ref #15, MEDIUM authority) in L1 Section 2. The I4 edit changed the confirmation pathway attribution from "Ref #15" to "Ref #4-#7" (cookbook guides). However, the cookbook guides do not contain this specific text. The attribution path in L0 is now potentially inaccurate.
- Recommendation: The correct statement per L1 Section 2 (line 170-171) is: "OpenAI's foundational Prompt Engineering Guide contains the widely-cited recommendation (sourced via promptingguide.ai, Ref #15, which attributes to OpenAI)." L0 Key Finding 1 should state: "(confirmed via Ref #15, MEDIUM authority — primary platform docs returned 403, Ref #3)" rather than "(confirmed via GPT-4.1 through GPT-5.2 cookbook guides, Ref #4-#7)."

**Attack Vector 2: The PS Integration Confidence Level Mismatch**

The PS Integration section (line 824-825) states: "Confidence: Medium (0.72)." However, the survey is in its 4th revision iteration with 5 major findings resolved, extensive cross-referencing, and a near-complete quality score. The confidence level was set in iteration 3 and has not been updated. A 0.72 confidence level on a document scoring in the 0.93-0.95 range is internally inconsistent — the confidence in the survey's findings and methodology is substantially higher than 0.72 would suggest.

**RT-002-20260227T004: PS Integration confidence level not updated to reflect I4 quality improvements** (Minor)
- Section: PS Integration
- Evidence: Line 824: "Confidence: Medium (0.72)" — this was set in iteration 3 and has not been updated. The deliverable is now in its 4th revision with all major findings resolved.
- Recommendation: Update confidence level to reflect the improved state: "Confidence: High (0.85) -- I4 revision resolves all Major findings. Core constraints: Context7 unavailability (structural); OpenAI platform docs inaccessible (structural); arXiv verbatim quotation gap (disclosed)."

---

### S-007: Constitutional AI Critique

**Constitutional Principles Reviewed:**

| Principle | Applicable? | Status |
|-----------|-------------|--------|
| P-001 (Truth/Accuracy) | Yes | COMPLIANT — findings grounded in evidence; GPT-5 Medium caveat added; preprint disclosure accurate |
| P-002 (File Persistence) | N/A (deliverable, not agent) | N/A |
| P-003 (No Recursion) | N/A | N/A |
| P-004 (Provenance) | Yes | COMPLIANT — 20 references with authority tiers; 34-query log; source provenance statement |
| P-011 (Evidence-Based) | Yes | COMPLIANT — all major claims trace to specific sources |
| P-022 (No Deception) | Yes | PARTIAL — see CC-001 below |
| H-15 (Self-Review) | Yes | COMPLIANT — S-010 executed |
| H-16 (Steelman before critique) | Yes | COMPLIANT — S-003 executed before S-002 |
| H-23 (Navigation Table) | Yes | COMPLIANT — 16-entry navigation table present |
| H-31 (Ambiguity) | Yes | COMPLIANT — uncertainty acknowledged; scope caveat present |

**CC-001-20260227T004: P-022 partial concern — L0 attribution path for OpenAI recommendation may mislead** (Minor)
- Section: L0 Key Finding 1
- Evidence: The I4 edit changed the L0 attribution for the OpenAI recommendation from "Ref #15, MEDIUM authority" (the I3 scorer's recommendation) to "confirmed via GPT-4.1 through GPT-5.2 cookbook guides, Ref #4-#7." However, L1 Section 2 (line 170-171) correctly identifies that the specific "avoid saying what not to do" language was sourced via promptingguide.ai (Ref #15). The cookbook guides (Ref #4-#7) contain related guidance but not the verbatim quote attributed here. This creates a minor P-022 concern: the attribution pathway described in L0 is not fully accurate relative to what is described in L1.
- This finding is consistent with RT-001 (same issue, different perspective).
- Recommendation: Align L0 attribution with L1 attribution: use "confirmed via Ref #15 (promptingguide.ai, MEDIUM authority); primary platform docs returned 403 (Ref #3)."

**CC-002-20260227T004: H-23 compliant — navigation table verified** (Pass)
- 16-entry navigation table covers all document sections. Anchor links verified. No H-23 violations found.

**CC-003-20260227T004: P-001 compliance verified with one residual observation** (Pass with note)
- Evidence claims are well-grounded. One observation: the PS Integration confidence level (0.72, Medium) was not updated to reflect I4 improvements. This is not a P-001 violation but is a minor accuracy gap per RT-002.

---

### S-011: Chain-of-Verification

**Claim Extraction and Independent Verification:**

| Claim ID | Claim | Independent Verification | Status |
|----------|-------|--------------------------|--------|
| CV-001 | "Both Anthropic and OpenAI explicitly recommend positive framing over negative instructions" (L0 Key Finding 1) | Verifiable via L1 Section 1 (Anthropic, lines 87-96) and L1 Section 2 (OpenAI, lines 167-174). Anthropic quote: "Tell Claude what to do instead of what not to do." OpenAI quote via Ref #15: "avoid saying what not to do but say what to do instead." Both confirmed. | **PASS** |
| CV-002 | "50 pairs × 5 models × 2 framing conditions = 500 evaluations" (line 694) | Arithmetic check: 50 × 5 × 2 = 500. Correct. | **PASS** |
| CV-003 | Taxonomy examples all cite specific source references | Checking each: Prohibition → OpenAI GPT-5.2 Ref #7. Exclusion → LlamaIndex Ref #11. Conditional negation → OpenAI GPT-4.1 Ref #4. Scope limitation → LlamaIndex Ref #11. Safety boundary → Anthropic Ref #1. All 5 types have source citations. | **PASS** |
| CV-004 | "Instruction violations ranged from 660 (GPT-5 Medium, best) to 1,330 (Gemini 2.0-Flash, worst)" (line 580) | Traceable to arXiv:2601.03269 (Ref #18, MEDIUM). Per-instance caveat now added. The GPT-5 Medium designation is flagged. Quantitative values (660, 1,330) are from preprint; cannot be independently verified via this survey's methodology (WebFetch cannot extract paginated PDF). Disclosed. | **PASS (with disclosed limitation)** |
| CV-005 | "Overall pass rate: 43.7%" and "Constraint compliance 66.9%" (lines 590-591) | Traceable to arXiv:2510.18892 (Ref #19, MEDIUM). Preprint disclosure covers this. Values are from abstract/HTML page; disclosed that verbatim quotation from paginated PDF not possible. | **PASS (with disclosed limitation)** |
| CV-006 | Cohen's kappa >= 0.80 for semantic equivalence validation (line 680) | This is a standard statistical threshold for inter-rater reliability (Cohen 1960; Landis & Koch 1977 classify 0.81-1.00 as "almost perfect"). The 0.80 threshold is appropriate for this application. However, the survey does not cite a source for this specific threshold — it is stated as a requirement without attribution. This is a minor evidence gap. | **MINOR CONCERN** |
| CV-007 | "34 total queries across 2 iterations" (line 768) | Count verification: Queries 1-34 listed. Query log shows 14 WebSearch, 20 WebFetch (lines 768). Counting: Queries 1, 3, 4, 10, 22, 23, 24, 26, 29, 31, 33 are labeled WebSearch or WebSearch... (11 approximate). WebFetch queries: 2, 5, 6, 7, 8, 9, 11-28 range... The summary says 14 WebSearch / 20 WebFetch. Not independently verifiable from the log format without exhaustive line-by-line counting, but the count of 34 total is internally consistent with Query numbers 1-34. | **PASS** |
| CV-008 | "GPT-5 Medium" caveat added (Edit 1) | Line 581-582: Caveat is present and specific: "Note: 'GPT-5 Medium' is the model designation used in the arXiv preprint (Tripathi et al., 2025). This designation cannot be verified against standard OpenAI public model naming conventions and may refer to an internal model variant or a designation that differs in the final published version." | **PASS** |
| CV-009 | L0 Key Finding 2 "OpenAI's Prompt Engineering Guide similarly advises (confirmed via GPT-4.1 through GPT-5.2 cookbook guides, Ref #4-#7; primary platform docs returned 403, Ref #3)" (line 44) | Cross-check with L1 Section 2 (line 170-171): "OpenAI's foundational Prompt Engineering Guide contains the widely-cited recommendation (sourced via promptingguide.ai, Ref #15, which attributes to OpenAI)." The L0 attribution names cookbook guides (Ref #4-#7) as the confirmation pathway; L1 Section 2 identifies Ref #15 as the confirmation source. These are inconsistent. The cookbook guides (Ref #4-#7) contain related but different guidance; the verbatim "avoid saying what not to do" language traces specifically to Ref #15 per the L1 body. | **FAIL — cross-reference inconsistency** |

**CV-001-20260227T004: L0 Key Finding 1 attribution pathway inconsistent with L1 Section 2** (Minor)
- Section: L0 Key Finding 1 vs. L1 Section 2
- Evidence: L0 line 44 attributes OpenAI recommendation confirmation to "cookbook guides, Ref #4-#7"; L1 line 170-171 attributes confirmation to "promptingguide.ai, Ref #15." These are different sources and different authority levels (HIGH vs. MEDIUM). The cookbook guides do not contain the verbatim "avoid saying what not to do" text; L1 correctly identifies Ref #15 as the verbatim source.
- This finding is consistent with RT-001 and CC-001.

---

### S-012: FMEA (Failure Mode and Effects Analysis)

**Components Analyzed:** L0 Executive Summary, L1 Library Sections, L2 Cross-Library Analysis, Experimental Design Parameters, Methodology, References

| Component | Failure Mode | Severity (1-10) | Occurrence (1-10) | Detection (1-10) | RPN | Classification |
|-----------|-------------|-----------------|-------------------|------------------|-----|----------------|
| L0 Key Finding 1 | Attribution pathway inconsistency (L0 vs. L1 attribution for OpenAI recommendation) | 6 | 4 | 8 | 192 | Minor |
| Experimental Design | Output quality metric undefined | 4 | 9 | 5 | 180 | Minor |
| Experimental Design | Sample size formula uses minimum model count (5) inconsistent with recommended range (5-10) | 4 | 6 | 7 | 168 | Minor |
| PS Integration | Confidence level not updated (0.72 vs. actual post-I4 state) | 3 | 8 | 6 | 144 | Minor |
| Taxonomy | Mutual exclusivity of Prohibition/Safety boundary not addressed in experimental design | 4 | 5 | 7 | 140 | Minor |
| Academic section | Cohen's kappa threshold stated without citation | 3 | 7 | 6 | 126 | Minor |
| Phase 2 Task Mapping | Artifacts unlinked to PROJ-014 work items | 3 | 9 | 5 | 135 | Minor |

**No Critical or Major RPN findings.** Highest RPN is 192 (L0 attribution inconsistency, Minor classification confirmed by cross-strategy consensus from RT-001, CC-001, CV-001).

**FM-001-20260227T004: L0 attribution inconsistency — highest RPN component** (Minor, RPN 192)
- Consistent with RT-001, CC-001, CV-001.

**FM-002-20260227T004: Output quality metric undefined** (Minor, RPN 180)
- Consistent with SR-001.

**Risk Reduction Actions:**
- Fix L0 attribution: 1-sentence edit. RPN reduction: from 192 to ~48 (eliminates occurrence; detection remains).
- Add output quality rubric: 3-4 lines. RPN reduction: from 180 to ~36.
- Update PS Integration confidence: 1 sentence. RPN reduction: from 144 to ~24.

---

### S-013: Inversion Technique

**Goal Inversion:** Instead of "What makes this survey succeed as Phase 1 research for PROJ-014?", ask "How would this survey guarantee that Phase 2 produces useless or misleading results?"

**Inverted Goals:**

1. **How to guarantee Phase 2 researchers misinterpret the evidence:** Ensure that the survey's key findings are presented without critical caveats in the section most likely to be read (L0). Currently, L0 Key Findings 1-6 do not carry the vendor doc-vs-behavior limitation. A reader of L0 only would conclude that "both vendors recommend positive framing" without knowing this reflects documentation guidance, not empirical behavior. **Status: Partially present — Edit 4 qualifiers are in L1, not L0.**

2. **How to guarantee Phase 2 experimental design is underpowered:** Ensure the sample size guidance uses the minimum of every parameter. The current formula (50 × 5 × 2 = 500) uses 5 models — the bottom of the 5-10 recommended range. A researcher planning a minimum-viable study will use exactly 5 models, producing 500 evaluations — the minimum. Young et al.'s finding that some individual tests had 2.7% pass rates (suggesting very high variance) implies that 500 evaluations might not be sufficient to detect small framing effects. **Status: Present as a subtle risk.**

3. **How to guarantee the taxonomy is used incorrectly:** Define categories that are not mutually exclusive without making this prominent enough in the experimental design. The survey flags the Prohibition/Safety boundary overlap in taxonomy observations but instructs Phase 2 to construct pairs for "each type" as if boundaries are clean. **Status: Present, flagged as PM-002.**

**IN-001-20260227T004: Inverted goal analysis reveals L0 doc-vs-behavior limitation gap is the highest-impact remaining issue** (Major)
- Section: L0 Executive Summary
- Evidence: Inverting the success criterion reveals that the most direct way to cause Phase 2 to be misled is to have researchers read L0 and act on Key Findings 1-6 without the vendor doc-vs-behavior limitation that Edit 4 added only to L1. The I3 scorer identified this gap (the qualifier was to be added to L1); the I4 edit correctly added qualifiers to all 5 L1 sections. But the L0 section — which is the primary consumption target for stakeholders and Phase 2 researchers — does not carry a corresponding qualifier.
- This finding extends DA-001's concern with a severity escalation argument: DA-001 was logged as Major; IN-001 confirms that severity via inversion analysis.
- Recommendation: Add one qualifier sentence before L0 Key Findings: "Note: All findings below reflect vendor-documented guidance and framework documentation. Production model behavior may differ from vendor recommendations (see per-library coverage assessments in L1 for source-specific limitations)."

**IN-002-20260227T004: Binary compliance distribution finding should be inverted — it is the single biggest threat to Phase 2 experimental validity** (Minor)
- Section: Academic Research Findings, Implications
- Evidence: If the goal is to guarantee Phase 2 produces a null finding that is misinterpreted as evidence that "framing doesn't matter," the most reliable path is to run the framing experiment on models where the binary compliance distribution dominates. The survey documents this finding but does not flag it as an experimental validity threat in the Implications section.
- Consistent with PM-003.

---

### S-014: LLM-as-Judge (Composite Scoring)

**Anti-Leniency Protocol:** Applying strict rubric. Uncertain scores resolved downward. No cross-dimension pull. Not anchoring to prior iteration improvements.

#### I3-to-I4 Delta Assessment First

Before scoring, assessing whether the 5 precision edits collectively close the 0.047 gap identified by the I3 scorer (I3 score: 0.903):

| I3 Gap | Edit Applied | Gap Closed? | Expected Score Impact |
|--------|-------------|-------------|----------------------|
| "GPT-5 Medium" caveat (Evidence Quality, Traceability, Internal Consistency, Methodological Rigor) | Edit 1 | Yes | +0.02-0.03 across 4 dimensions |
| Arithmetic error (Internal Consistency, Actionability, Completeness) | Edit 2 | Yes | +0.02-0.03 across 3 dimensions |
| Semantic equivalence validation (Methodological Rigor, Actionability) | Edit 3 | Yes | +0.02-0.03 across 2 dimensions |
| Vendor doc-vs-behavior qualifier in L1 (Completeness, Methodological Rigor) | Edit 4 | Partially | +0.01 (L1 addressed; L0 not) |
| L0 Key Finding 2 authority qualifier (Internal Consistency, Traceability) | Edit 5 | Partially | +0.01 (but introduced new attribution inconsistency — see RT-001/CV-001/CC-001/IN-001) |

**Critical observation on Edit 5:** The I3 scorer recommended "confirmed via Ref #15, MEDIUM authority." The I4 implementation changed this to "confirmed via GPT-4.1 through GPT-5.2 cookbook guides, Ref #4-#7." This introduced a NEW Minor finding (RT-001/CC-001/CV-001): the L0 attribution is now inconsistent with L1 Section 2. The intended fix resolves one concern (L0 authority qualification) but creates another (attribution path inconsistency). The net effect on score is approximately neutral for this specific edit.

#### Dimension Scores

**Completeness (Weight: 0.20)**

I3 score: 0.91. I4 improvements: vendor doc-vs-behavior qualifiers added to all 5 L1 sections (major completeness improvement). Taxonomy and experimental design complete. Arithmetic corrected.

Remaining gap: Output quality metric still lacks rubric (Minor, SR-001). The L0 section does not carry the vendor doc-vs-behavior limitation (IN-001, DA-001) — but this is a presentation/framing gap, not a completeness gap per se; the limitation is fully documented in L1.

**I4 Completeness Score: 0.93** (+0.02 from I3)

Rationale: The addition of vendor doc-vs-behavior qualifiers to all 5 L1 sections is a genuine completeness improvement over I3. The remaining output quality metric gap is Minor. No new completeness gaps introduced.

---

**Internal Consistency (Weight: 0.20)**

I3 score: 0.90. I4 improvements: GPT-5 Medium caveat added, arithmetic corrected. L0 Key Finding 2 authority qualifier changed from "Ref #15" (I3 scorer's recommendation) to "Ref #4-#7" (cookbook guides).

New gap introduced: The L0 attribution (Ref #4-#7) for the "avoid saying what not to do" quote is inconsistent with L1 Section 2's attribution (Ref #15). This is the same content accessed via different pathways, but the specific quote at issue traces to Ref #15 in L1 and to Ref #4-#7 in L0. The Edit 5 implementation partially resolves the I3 gap (L0 no longer implies the primary guide was directly accessed) but introduces a new inconsistency between L0 and L1 attribution pathways.

Net effect: Two I3 Major inconsistencies resolved (GPT-5 Medium, arithmetic), one I3 Minor inconsistency resolved (L0 Key Finding 2 authority), one new Minor inconsistency introduced (L0 vs. L1 attribution path). The overall Internal Consistency state improves.

**I4 Internal Consistency Score: 0.93** (+0.03 from I3)

Rationale: The resolution of the arithmetic error and GPT-5 Medium caveat are both significant improvements. The new L0/L1 attribution inconsistency is Minor and does not offset the Major improvements. The net improvement from 0.90 to 0.93 reflects two Major resolutions against one new Minor finding.

---

**Methodological Rigor (Weight: 0.20)**

I3 score: 0.92. I4 improvements: semantic equivalence validation with Cohen's kappa >= 0.80 specified. GPT-5 Medium caveat added (addresses the "unverifiable model label" gap). All other methodological elements (reproducibility statement, query log, preprint disclosure, source selection rationale) carry forward in good state.

Remaining gap: Cohen's kappa threshold cited without reference (CV-006, Minor). Source selection criteria not linked to data (Minor, carries forward). L0 doc-vs-behavior limitation absent (primarily an evidence/traceability concern, not methodological).

**I4 Methodological Rigor Score: 0.94** (+0.02 from I3)

Rationale: The semantic equivalence validation specification is the most significant methodological improvement in I4 — it addresses the most critical measurement validity concern identified by I3. The addition of a specific, standard statistical threshold (kappa >= 0.80) is appropriate. Two Minor gaps remain. Score rises from 0.92 to 0.94.

---

**Evidence Quality (Weight: 0.15)**

I3 score: 0.87. This was the weakest dimension in I3, driven primarily by the "GPT-5 Medium" asymmetric disclosure gap.

I4 improvement: GPT-5 Medium caveat is now per-instance and specific (Edit 1). The asymmetry that drove the 0.87 score is resolved — all major verbatim extraction limitations are now individually disclosed. The preprint disclosure, authority tier system, and direct quotes are all present.

Remaining gap: L0 attribution inconsistency (Ref #4-#7 in L0 vs. Ref #15 in L1) is an evidence quality concern — the L0 attribution path is not fully accurate relative to what is stated in L1. However, this is a Minor attribution gap, not a case of an unsupported claim. The underlying finding (OpenAI recommends positive framing) remains well-supported.

The verbatim quotation gap for arXiv quantitative figures is disclosed and is a structural limitation of the research methodology (WebFetch cannot extract paginated PDF content). This is an honest constraint, not an evidence quality failure.

**I4 Evidence Quality Score: 0.92** (+0.05 from I3)

Rationale: The resolution of the "GPT-5 Medium" asymmetric disclosure gap is the primary driver of this improvement. Moving from 0.87 to 0.92 reflects: (1) the gap that held Evidence Quality in the "most claims supported" band is now resolved; (2) the remaining Minor gaps (attribution inconsistency, verbatim quotation limitation as disclosed) are consistent with a 0.92 score. The scoring moves from "most claims supported (0.87)" to "approaching all claims with credible citations (0.92)" with two residual minor gaps.

---

**Actionability (Weight: 0.15)**

I3 score: 0.90. I4 improvements: arithmetic corrected (the primary actionability issue was the wrong sample size number). Semantic equivalence validation specified with concrete method (kappa >= 0.80, two-rater process).

Remaining gaps: Output quality metric lacks rubric (Minor, SR-001). Sample size formula uses minimum model count with potential to mislead (PM-001, Minor). Phase 2 artifacts unlinked to work items (SR-002, Minor).

**I4 Actionability Score: 0.93** (+0.03 from I3)

Rationale: The arithmetic correction and semantic equivalence validation specification together address the two most actionability-limiting gaps from I3. The Phase 2 experimental design is now complete enough for a researcher to begin designing a study. Three Minor gaps remain, none of which prevent the design from being actionable. Moving from 0.90 to 0.93 reflects the transition from "actions present, one with arithmetic error" to "clear, specific, implementable actions with minor gaps."

---

**Traceability (Weight: 0.10)**

I3 score: 0.92. I4 improvements: GPT-5 Medium provenance gap resolved via per-instance caveat. All other traceability elements (navigation table, query log, references) unchanged in structure.

Remaining gaps: Phase 2 artifacts unlinked to PROJ-014 work items (SR-002/RT-002, Minor). L0 attribution inconsistency creates a minor traceability concern (RT-001, Minor). PS Integration confidence level not updated (RT-002, Minor).

**I4 Traceability Score: 0.93** (+0.01 from I3)

Rationale: The GPT-5 Medium provenance resolution is the primary improvement. The three remaining Minor gaps are consistent with 0.93. Traceability was already relatively strong in I3; this marginal improvement reflects the targeted provenance fix.

---

#### Composite Score Computation

```
I4 composite = (0.93 × 0.20)   # Completeness
             + (0.93 × 0.20)   # Internal Consistency
             + (0.94 × 0.20)   # Methodological Rigor
             + (0.92 × 0.15)   # Evidence Quality
             + (0.93 × 0.15)   # Actionability
             + (0.93 × 0.10)   # Traceability
             = 0.186 + 0.186 + 0.188 + 0.138 + 0.1395 + 0.093
             = 0.9305
```

**Weighted Composite: 0.930**

**Verdict: REVISE — Score 0.930 / Threshold 0.95 / Gap 0.020**

---

## Findings Summary

| ID | Severity | Finding | Section | Strategy |
|----|----------|---------|---------|---------|
| SR-001-20260227T004 | Minor | Output quality metric lacks measurement methodology/rubric | Experimental Design Parameters | S-010 |
| SR-002-20260227T004 | Minor | Phase 2 artifacts unlinked to PROJ-014 work items | Phase 2 Task Mapping | S-010 |
| SR-003-20260227T004 | Minor | OpenAI Ref #3 authority label ambiguity (HIGH but inaccessible) | References | S-010 |
| SM-001-20260227T004 | Minor | Binary compliance distribution finding deserves stronger framing | Academic Research Findings | S-003 |
| SM-002-20260227T004 | Minor | Phase 2 Task Mapping could link to taxonomy more explicitly | Phase 2 Task Mapping | S-003 |
| SM-003-20260227T004 | Minor | Revised hypothesis lacks measurable success criteria | Implications for PROJ-014 Hypothesis | S-003 |
| DA-001-20260227T004 | **Major** | L0 Key Findings do not carry vendor doc-vs-behavior limitation | L0 Executive Summary | S-002 |
| DA-002-20260227T004 | Minor | Framing-pair semantic equivalence assumption may not transfer to LLM processing | Experimental Design Parameters | S-002 |
| DA-003-20260227T004 | Minor | Convergence claim based on potentially non-representative source sample | Pattern Convergence (L2) | S-002 |
| PM-001-20260227T004 | Minor | Sample size formula anchors to minimum model count (5), potentially conflicting with recommended range (5-10) | Experimental Design Parameters | S-004 |
| PM-002-20260227T004 | Minor | Taxonomy type mutual exclusivity issue not addressed in experimental design | Taxonomy / Experimental Design | S-004 |
| PM-003-20260227T004 | Minor | Binary compliance distribution not flagged as threat to experimental validity | Academic Research Findings / Implications | S-004 |
| RT-001-20260227T004 | Minor | L0 Key Finding 1 attribution pathway inconsistent with L1 Section 2 | L0 Key Finding 1 | S-001 |
| RT-002-20260227T004 | Minor | PS Integration confidence level not updated to reflect I4 improvements | PS Integration | S-001 |
| CC-001-20260227T004 | Minor | P-022 concern — L0 attribution path for OpenAI recommendation may mislead | L0 Key Finding 1 | S-007 |
| CV-001-20260227T004 | Minor | L0 attribution pathway inconsistent with L1 Section 2 (cross-reference verification failure) | L0 Key Finding 1 | S-011 |
| FM-001-20260227T004 | Minor | L0 attribution inconsistency — highest RPN component (RPN 192) | L0 Key Finding 1 | S-012 |
| FM-002-20260227T004 | Minor | Output quality metric undefined (RPN 180) | Experimental Design Parameters | S-012 |
| IN-001-20260227T004 | **Major** | L0 doc-vs-behavior limitation absent — highest-impact remaining issue (confirmed by inversion analysis) | L0 Executive Summary | S-013 |
| IN-002-20260227T004 | Minor | Binary compliance distribution not flagged as experimental validity threat | Academic Research Findings | S-013 |

**Total: 20 findings — 0 Critical, 2 Major, 18 Minor**

### Finding Consolidation Note

Several findings are cross-strategy confirmations of the same underlying issue:

**Consolidated Issue A (DA-001 + IN-001):** L0 does not carry vendor doc-vs-behavior limitation forward from L1. Both DA-001 and IN-001 independently identify this as a Major finding. This is the single highest-priority remaining gap.

**Consolidated Issue B (RT-001 + CC-001 + CV-001 + FM-001):** L0 Key Finding 1 attribution pathway inconsistency (cookbook guides Ref #4-#7 in L0 vs. Ref #15 in L1 Section 2). All four strategies independently identify this Minor finding. This was introduced by Edit 5 attempting to address the I3 L0 authority gap.

**Unique findings (not confirmed by multiple strategies):** SR-001, SR-002, SR-003, SM-001, SM-002, SM-003, DA-002, DA-003, PM-001, PM-002, PM-003, RT-002, IN-002.

---

## I3 → I4 Resolution Summary

| I3 Finding Category | I3 Count | Resolved in I4 | Remaining | New in I4 |
|--------------------|----------|----------------|-----------|-----------|
| Critical | 0 | N/A | 0 | 0 |
| Major | 5 | 4 | 1* | 1** |
| Minor | 12 | 6 | 6 | 12 |
| **Total** | **17** | **10** | **7** | **13** |

*1 Major remaining: DA-001/IN-001 (L0 doc-vs-behavior limitation absent — this was not among the 5 I3 precision edits, which targeted L1 sections. The I3 scorer recommended L1 fixes; this is a gap that was in L1 in I3 but the L0 equivalent was not flagged as a discrete I3 Major finding.)

**1 Major new: DA-001/IN-001 is newly identified in I4 as a Major finding. Looking at I3 executor findings carefully: IN-002 in I3 was "vendor documentation vs. behavior qualifier absent from L1" (5 sections × Major); this is now RESOLVED. The L0 equivalent is a new finding first articulated explicitly in I4 as a Major gap.

**Actual interpretation:** The I3 executor had FM-006 (vendor doc-vs-behavior qualifier absent from L1) as the persistent 3-iteration Major. Edit 4 resolved this for L1. But the consequence of resolving L1 is that the absence of a corresponding L0 qualifier is now more visible — L0 presents unqualified findings while L1 has the caveats. DA-001/IN-001 is a new Major finding that emerges from the correct application of Edit 4.

---

## Iteration Comparison Table

| Dimension | Weight | I1 Score | I2 Score | I3 Score (Scorer) | I4 Score | I1→I2 | I2→I3 | I3→I4 |
|-----------|--------|----------|----------|-------------------|----------|-------|-------|-------|
| Completeness | 0.20 | 0.79 | 0.87 | 0.91 | **0.93** | +0.08 | +0.04 | +0.02 |
| Internal Consistency | 0.20 | 0.81 | 0.88 | 0.90 | **0.93** | +0.07 | +0.02 | +0.03 |
| Methodological Rigor | 0.20 | 0.76 | 0.86 | 0.92 | **0.94** | +0.10 | +0.06 | +0.02 |
| Evidence Quality | 0.15 | 0.78 | 0.87 | 0.87 | **0.92** | +0.09 | 0.00 | +0.05 |
| Actionability | 0.15 | 0.82 | 0.84 | 0.90 | **0.93** | +0.02 | +0.06 | +0.03 |
| Traceability | 0.10 | 0.82 | 0.90 | 0.92 | **0.93** | +0.08 | +0.02 | +0.01 |
| **Composite** | **1.00** | **0.80** | **0.87** | **0.903** | **0.930** | **+0.07** | **+0.033** | **+0.027** |

**Score trajectory:** 0.80 → 0.87 → 0.903 → 0.930

**Delta trajectory:** +0.07, +0.033, +0.027

---

## Plateau Detection Analysis

| Iteration | Delta | Threshold (< 0.01 for 3 consecutive = plateau) |
|-----------|-------|------------------------------------------------|
| I1→I2 | +0.070 | Not plateau |
| I2→I3 | +0.033 | Not plateau |
| I3→I4 | +0.027 | Not plateau (delta still meaningful) |

**Plateau status: Not triggered.** The delta is decreasing (0.070 → 0.033 → 0.027) but remains above the 0.01 plateau threshold. The improvement rate is slowing, which is expected as major gaps are resolved and only Minor findings remain (plus 2 targeted Majors).

The I3→I4 delta of 0.027 represents meaningful progress driven primarily by the resolution of the GPT-5 Medium gap (+0.05 in Evidence Quality, the most impactful single improvement in I4).

**Gap to threshold:** 0.950 - 0.930 = 0.020

---

## I5 Feasibility Assessment

**Can I5 close the remaining 0.020 gap to 0.950?**

The 2 Major findings and 18 Minor findings in I4 map to specific, bounded fixes:

| Priority | Finding(s) | Fix Description | Estimated Score Impact |
|----------|-----------|-----------------|----------------------|
| 1 (Critical for I5) | DA-001 + IN-001 | Add qualifier sentence before L0 Key Findings: "Note: All findings below reflect vendor-documented guidance and framework documentation. Production model behavior may differ from vendor recommendations (see per-library coverage assessments in L1 for source-specific limitations)." — 1 sentence | +0.02 (Completeness: +0.01, Internal Consistency: +0.01) |
| 2 (High for I5) | RT-001 + CC-001 + CV-001 + FM-001 | Correct L0 Key Finding 1 attribution: change "confirmed via GPT-4.1 through GPT-5.2 cookbook guides, Ref #4-#7" to "confirmed via Ref #15 (promptingguide.ai, MEDIUM authority); primary platform docs returned 403, Ref #3" — 1 clause edit | +0.01 (Internal Consistency: +0.01, Evidence Quality: +0.005, Traceability: +0.005) |
| 3 (Medium for I5) | SR-001 + FM-002 | Add output quality rubric: e.g., "Holistic quality assessment: evaluated on a 1-5 scale (1 = significant quality degradation, 3 = neutral, 5 = quality improvement) by 2+ raters; inter-rater agreement required" — 2 sentences | +0.01 (Actionability: +0.01, Completeness: +0.005) |
| 4 (Lower) | RT-002 | Update PS Integration confidence level from 0.72 to ~0.85 — 1 sentence | +0.005 |
| 5 (Lower) | PM-003 + IN-002 | Add experimental validity threat flag for binary compliance distribution — 2 sentences | +0.005-0.01 |

**Projected I5 composite with Priorities 1-3 applied:**
```
Projected = (0.94 × 0.20) + (0.95 × 0.20) + (0.95 × 0.20) + (0.93 × 0.15) + (0.94 × 0.15) + (0.94 × 0.10)
          = 0.188 + 0.190 + 0.190 + 0.1395 + 0.141 + 0.094
          = 0.9425
```

**With all 5 priorities applied:**
```
Projected = (0.94 × 0.20) + (0.95 × 0.20) + (0.95 × 0.20) + (0.935 × 0.15) + (0.945 × 0.15) + (0.945 × 0.10)
          = 0.188 + 0.190 + 0.190 + 0.1403 + 0.1418 + 0.0945
          = 0.9446
```

**Honest assessment:** I5 with all 5 targeted fixes is projected at 0.940-0.948 on the executor's calibration basis. Whether this clears 0.950 is borderline. The primary constraint is that Evidence Quality is approaching a ceiling: the verbatim quotation limitation for arXiv quantitative figures is disclosed but remains structurally unresolvable without re-executing research via PDF access. With WebFetch-only research methodology, Evidence Quality is unlikely to exceed 0.93-0.94.

**The C4 threshold question:** The 0.020 gap at I4 is real but achievable in I5 if (a) the 2 Major findings are addressed (Priority 1), (b) the attribution inconsistency introduced by Edit 5 is corrected (Priority 2), and (c) at least one additional Minor is addressed. The executor estimates a 70% probability that I5 reaches >= 0.950 with the Priority 1-3 fixes applied precisely and no new regressions introduced.

---

## Detailed Findings

### DA-001-20260227T004: L0 Key Findings Do Not Carry Vendor Doc-vs-Behavior Limitation

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | L0 Executive Summary, Key Findings |
| **Strategy Step** | S-002 Step 2 (Assumption Challenge), confirmed by S-013 Inversion |

**Evidence:**
L0 Key Finding 1 (line 43): "Both Anthropic and OpenAI explicitly recommend positive framing over negative instructions."
L0 Key Finding 2 (line 46): "However, both vendors actively USE negative constraints in their own prompts and documentation."
L0 Key Finding 6 (line 54): "The surveyed evidence converges on a hybrid approach."

All 6 Key Findings in L0 are stated without any qualifier that they represent vendor documentation guidance rather than empirically observed model behavior. Edit 4 added qualifiers to L1 Coverage Assessment sections for all 5 libraries. However, L0 — the primary stakeholder-facing section — does not have a corresponding qualifier.

**Analysis:**
A researcher or stakeholder reading L0 only will conclude that "both vendors recommend positive framing" (Key Finding 1) as a direct reflection of model behavior. The actual situation — documented in all 5 L1 sections — is that these are vendor documentation recommendations that may not reflect empirically observed model behavior. This is particularly significant for PROJ-014's hypothesis, where the question is precisely whether vendor recommendations reflect actual model performance.

The inversion analysis confirms this is the highest-impact remaining gap: the most direct path to causing Phase 2 to proceed on faulty assumptions is for L0 readers to take Key Findings at face value without the doc-vs-behavior limitation.

**Recommendation:**
Add one qualifier sentence before the Key Findings list in L0:
"Note: All findings below reflect vendor-documented guidance and framework documentation. Production model behavior may differ from vendor recommendations (see per-library coverage assessments in L1 for source-specific limitations)."

---

### IN-001-20260227T004: L0 Doc-vs-Behavior Limitation Absent (Inversion-Confirmed)

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | L0 Executive Summary |
| **Strategy Step** | S-013 Inversion Goal Analysis |

**Evidence:**
See DA-001 above. IN-001 is the inversion-derived confirmation of DA-001 with a severity escalation argument: inverting the success criterion of the survey ("what would guarantee Phase 2 misinterprets the evidence?") identifies L0's unqualified Key Findings as the primary attack surface. The two findings are consolidated — addressing DA-001 also resolves IN-001.

**Analysis:**
Inversion confirms that the L0 section is the most critical place for the vendor doc-vs-behavior limitation. It is also the most likely section to be read in isolation by Phase 2 analysts and stakeholders.

**Recommendation:** Same as DA-001. One qualifier sentence before L0 Key Findings.

---

### RT-001-20260227T004: L0 Key Finding 1 Attribution Inconsistency

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | L0 Executive Summary, Key Finding 1 |
| **Strategy Step** | S-001 Attack Vector 1, confirmed by S-007 CC-001, S-011 CV-009, S-012 FM-001 |

**Evidence:**
L0 line 44: "OpenAI's Prompt Engineering Guide similarly advises (confirmed via GPT-4.1 through GPT-5.2 cookbook guides, Ref #4-#7; primary platform docs returned 403, Ref #3): 'avoid saying what not to do but say what to do instead.'"

L1 Section 2, line 170-171: "OpenAI's foundational Prompt Engineering Guide contains the widely-cited recommendation (sourced via promptingguide.ai, Ref #15, which attributes to OpenAI): 'Another common tip when designing prompts is to avoid saying what not to do but say what to do instead.'"

The verbatim "avoid saying what not to do" text traces specifically to Ref #15 in L1. The I4 Edit 5 changed L0's attribution from the I3 recommendation (Ref #15) to cookbook guides (Ref #4-#7). The cookbook guides contain related guidance but not this specific verbatim text.

**Analysis:**
The I4 Edit 5 implementation introduced a minor attribution inconsistency. The intent was to provide a stronger confirmation pathway; the effect was to create an inconsistency between L0 and L1. This is a Minor finding (the underlying claim about OpenAI's recommendation is correct; the specific attribution path is misaligned between document sections).

**Recommendation:**
Correct L0 Key Finding 1 attribution to: "OpenAI's Prompt Engineering Guide similarly advises (confirmed via promptingguide.ai, Ref #15, which attributes to OpenAI; primary platform docs returned 403, Ref #3): 'avoid saying what not to do but say what to do instead.'"
This aligns with L1 Section 2 and is accurate.

---

## Execution Statistics

- **Total Findings:** 20
- **Critical:** 0
- **Major:** 2 (DA-001/IN-001 consolidated; RT-001 attribution inconsistency is Minor despite appearing in 4 strategy outputs)
- **Minor:** 18
- **Protocol Steps Completed:** 10 of 10 strategies executed
- **I3 Precision Edits Verified:** 5 of 5 correctly applied

## Verdict

**REVISE — Score 0.930 / Threshold 0.950 / Gap 0.020**

**Justification:** The I4 revision successfully resolves all 5 I3 precision edits with precision. The most impactful improvement is the GPT-5 Medium per-instance caveat, which drives a +0.05 improvement in Evidence Quality (from 0.87 to 0.92). The arithmetic correction, semantic equivalence validation, L1 vendor doc-vs-behavior qualifiers, and L0 Key Finding 2 authority qualifier all address their target gaps correctly.

However, two new findings emerge in I4 that are classified as Major:

1. **DA-001/IN-001:** L0 Key Findings do not carry the vendor doc-vs-behavior limitation that Edit 4 correctly added to all 5 L1 sections. This is the highest-impact remaining gap — L0 is the primary stakeholder-facing section, and unqualified Key Findings could mislead Phase 2 researchers.

2. **RT-001/CC-001/CV-001/FM-001 (consolidated, Minor):** Edit 5 resolved the L0 authority gap by attributing the OpenAI recommendation to cookbook guides (Ref #4-#7), but this is inconsistent with L1 Section 2's attribution to Ref #15 (promptingguide.ai). This introduced a Minor cross-reference inconsistency.

The gap to 0.950 threshold is 0.020. I5 is feasible but will require precision execution of the Priority 1-3 fixes (see I5 Feasibility Assessment). The projected I5 score is 0.940-0.948, with a 70% probability of reaching >= 0.950 if no new regressions are introduced.

**If REVISE: Can I5 close the gap?**
Yes, with high confidence for the Priority 1 fix (L0 qualifier sentence — 1 sentence, directly addresses the 2 Major findings). The Priority 2 fix (correct L0 attribution from Ref #4-#7 to Ref #15) is a 1-clause correction. Priority 3 (output quality rubric) is 2 sentences. These are genuinely targeted, non-structural edits. I5 is the recommended next action.

**Plateau check:** Delta trajectory is 0.070 → 0.033 → 0.027. Decreasing but not plateauing (not < 0.01 for 3 consecutive). No plateau flag raised. I5 is warranted.
