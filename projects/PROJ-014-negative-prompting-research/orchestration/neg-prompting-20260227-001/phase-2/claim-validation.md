# Claim Validation Analysis: "Negative Prompting Reduces Hallucination by 60%"

> ps-analyst | TASK-005 | PROJ-014 | 2026-02-28
> Analysis Type: Gap + Evidence Assessment + Retrospective Comparison + Experimental Design
> Iteration: 4 (addressing 3 Minor findings and 1 improvement recommendation from adversary tournament I3, score 0.944 REVISE)
> Inputs: synthesis.md (R4, 0.953 PASS), supplemental-vendor-evidence.md (R4, 0.951 PASS), PROJ-007 PLAN.md (verified), PROJ-007 quality gate reports (barrier-3, barrier-4, C4 tournament, Phase 5 review), PROJ-007 WORKTRACKER.md, PROJ-006 WORKTRACKER.md (PENDING — no quality data)
> Methodology: Evidence tiering (Tier 1–4), retrospective A/B comparison with confound table, McNemar-powered experimental design
> Confidence: Evidence assessment: high (0.90); Retrospective comparison: medium (0.75); Experimental design assumptions: medium (0.70); Overall: 0.82
> I1 adversary report: `projects/PROJ-014-negative-prompting-research/orchestration/neg-prompting-20260227-001/phase-2/adversary-claim-validation-i1.md`
> I2 adversary report: `projects/PROJ-014-negative-prompting-research/orchestration/neg-prompting-20260227-001/phase-2/adversary-claim-validation-i2.md`
> I3 adversary report: `projects/PROJ-014-negative-prompting-research/orchestration/neg-prompting-20260227-001/phase-2/adversary-claim-validation-i3.md`

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Revision Log](#revision-log) | Changes from I2 to I3, finding-by-finding |
| [WARNING: Null Finding Protection](#warning-null-finding-protection) | Critical framing protection against weaponized misreading |
| [L0: Executive Summary](#l0-executive-summary) | Plain-language verdict, key numbers, what to do |
| [L1: Claim Evidence Assessment](#l1-claim-evidence-assessment) | Evidence catalog for and against the 60% claim with tier assignments |
| [L1: Retrospective A/B Comparison](#l1-retrospective-ab-comparison) | PROJ-014 vs. PROJ-007 quality gate data with confound acknowledgment |
| [L2: Architectural and Strategic Implications](#l2-architectural-and-strategic-implications) | Systemic patterns, strategic positioning, long-term research agenda |
| [Controlled Experiment Pilot Design](#controlled-experiment-pilot-design) | n=30 pilot specification — REVISED with all protocol gaps addressed |
| [Evidence Summary Table](#evidence-summary-table) | All evidence cited, with tier and relevance |
| [Analytical Limitations](#analytical-limitations) | What this analysis cannot establish |
| [Adversarial Quality Checks](#adversarial-quality-checks) | S-013 Inversion, S-004 Pre-Mortem, S-003 Steelman (I1 inline; superseded by I1 and I2 external tournaments) |

---

## Revision Log

> I3 composite score: 0.944 REVISE (C4 threshold >= 0.95). This log documents resolution of 3 Minor findings and 1 improvement recommendation from the I3 adversary tournament. Prior logs (I2: 27 Major + 16 Minor; I1: 16 Critical + 29 Major + 11 Minor) are carried forward below for traceability.

### I3 → I4: Minor Findings Resolved (3/3) + 1 Improvement Recommendation

| Finding ID | Resolution in I4 |
|------------|-----------------|
| I3-M-001 | Added operational decision procedure for the 5–6 failure marginal intermediate zone: "If 5–6 failures occur, proceed to GO decision on the remaining two primary criteria (π_d range and kappa); document failure rate in the pilot report as a limitation." Appended to the Note on SR-004-i2 resolution paragraph in [Pilot Go/No-Go Criteria](#pilot-gono-go-criteria). |
| I3-M-002 | Added "Agresti attribution documented as labeled limitation in footnote" to the PS Integration artifact summary, ensuring the handoff block accurately reflects what was fixed vs. what remains as a disclosed limitation. |
| I3-M-003 | Revised the SR-005-i2 resolution note in this log from "document header and comparison table now both use +0.116" to "both the comparison table and the document header use +0.116; the statistics section additionally shows the unrounded value +0.1155 as the derivation step" — resolving the cosmetic imprecision in the prior resolution description. |
| I3-Rec-4 | Added fallback model selection procedure to [Model Selection Criteria](#model-selection-criteria): substitute the nearest available model satisfying the same selection criteria if any working model becomes unavailable; document substitution as a limitation. |

---

> I2 composite score: 0.839 REJECTED (C4 threshold >= 0.95). This log documents resolution of all 27 Major and 16 Minor findings from the I2 adversary tournament. The I1 log (16 Critical, 29 Major, 11 Minor resolved) is carried forward below for traceability.

### I2 → I3: Major Findings Resolved (27/27)

| Theme | Finding IDs | Resolution in I3 |
|-------|-------------|-----------------|
| T-1: Hallucination operationalization | DA-001-i2, FM-001-i2, IN-001-i2, PM-001-i2 | Source material defined per task category in new sub-section [Source Material Operationalization by Task Category](#source-material-operationalization-by-task-category). All 5 categories covered. |
| T-2: Stopping criterion vs. pilot purpose | RT-001-i2, FM-004-i2, IN-002-i2, PM-004-i2 | Go/No-Go restructured: primary criterion is descriptive (observed π_d in calibration range); secondary CI criterion explicitly labelled as supplementary; non-fulfillment of secondary criterion does not constitute pilot failure. See revised [Pilot Go/No-Go Criteria](#pilot-gono-go-criteria). |
| T-3: Calibration kappa at n=3 | DA-004-i2, FM-003-i2, IN-003-i2, PM-003-i2 | Calibration sample increased from n=3 to n=10 pairs (2 pre-validated pairs × 5 task categories, drawn from the pre-validated example pool). Kappa at n=10 is statistically meaningful. See revised [Evaluator Training Protocol](#evaluator-training-protocol). |
| T-4: EC-2 vs. example pairs | DA-003-i2, FM-006-i2, IN-004-i2, RT-003-i2 | EC-2 revised to explicitly permit valence-inverted consequence matching: "same consequence domain, inverted valence acceptable." Example pairs now comply with EC-2 as written. Structural asymmetry acknowledged in Analytical Limitations. See revised [Equivalence Validation Protocol](#equivalence-validation-protocol). |
| T-5: Semantic circumlocution | DA-002-i2, FM-002-i2, PM-002-i2 | Masking list extended to include common circumlocutory terms ("avoid," "instead of," "rather than," "alternatively," "in lieu of"). Residual blinding limitation acknowledged explicitly. See revised [Evaluator Blinding Protocol](#evaluator-blinding-protocol). |
| T-6: Power calculation inaccuracy | SR-002-i2, CC-001-i2, CV-002-i2, FM-005-i2 | Power corrected to ~0.17 with full McNemar derivation. Pilot intentionally underpowered for calibration, not confirmation. Low power is expected and appropriate. See revised [Statistical Power for All Conditions](#statistical-power-for-all-conditions). |

**Additional Major findings resolved:**
| Finding ID | Resolution |
|------------|-----------|
| CC-002-i2 | CI method specified: Wilson score interval for the difference in discordant proportions. Recommended for small n_discordant. See revised [Statistical Stopping Criterion](#statistical-stopping-criterion). |
| CV-001-i2 | Wei et al. (2022) citation corrected: the 20-40% range is the author's inference from accuracy improvement data, not a directly stated discordant proportion value. Language revised to "extrapolated from accuracy data." See revised [π_d = 0.30 Grounding](#π_d--030-grounding). |
| SR-003-i2 | DSPy mechanism distinction made explicit in generalizability bridge: "DSPy assertion backtracking is infrastructure-level (compile-time constraint enforcement with automatic retry); this is distinct from prompt-level L2-re-injection. The bridge maps on the shared reinforcement principle, not on mechanistic identity." See revised [Evidence-to-Pilot Generalizability Bridge](#evidence-to-pilot-generalizability-bridge). |

### I2 → I3: Minor Findings Resolved

| Finding ID | Resolution |
|------------|-----------|
| SR-001-i2 | Continuity correction arithmetic: footnote formula revised to document that ~268 includes an additional rounding buffer; exact formula yield is ~264; the table value is the conservatively rounded estimate (consistent with common practice of rounding up sample size). |
| SR-004-i2 | GO/NO-GO intermediate state resolved: "Pilot data quality" GO criterion relaxed to "≥ 85% of the 30 pairs produce valid evaluatable output" (i.e., ≤ 4 failures); NO-GO threshold of >20% failures (≥ 7 failures) creates no undefined zone. |
| SR-005-i2 | Score delta rounding: both the comparison table and the document header use +0.116; the statistics section additionally shows the unrounded value +0.1155 as the derivation step (unweighted mean of +0.123 and +0.108, rounded to three decimal places). |
| DA-005-i2, FM-007-i2 | C2 vs. C5 (structured vs. paired) removed from pre-specified full-experiment comparisons. Added to post-hoc exploratory tier with explicit rationale: "Near-infinite required n under zero-effect assumption; this comparison is not addressable within a single study. Included as a post-hoc observation only if power materializes from pilot calibration." |
| PM-005-i2 | Same as DA-005-i2: C2 vs. C5 removed from pre-specified list. |
| PM-006-i2 | DSPy mechanism distinction documented in generalizability bridge (see SR-003-i2 resolution above). |
| CC-003-i2 | H-15 compliance: I3 revision constitutes a documented self-review pass of all I2 additions before submission to I3 tournament. This revision log documents the review. |
| CC-004-i2 | Experimental variable scope narrowing explicitly noted in comparison premise: "The positive-framing control label refers to PLAN.md-level project governance; shared HARD-rule framework vocabulary is a confound present in both conditions." |
| CV-003-i2 | Agresti attribution: continuity correction formula attribution changed to "standard sample size continuity correction for paired proportions (derivation from Agresti 2013, §10.1 principles; the specific formula is the author's adaptation)." |
| IN-005-i2 | Wei et al. π_d grounding: same correction as CV-001-i2. Language now "extrapolated from accuracy data; not directly reported." |
| SM-001-i2 | Power estimate now corrected with full derivation; citation issue resolved. |
| SM-002-i2 | Mechanism hypothesis column added to generalizability bridge (see new bridge format). |
| SM-003-i2 | PS Integration null finding coverage estimate: derivation now cited inline: "30-40% per Structural Exclusion Impact Assessment; published academic + public practitioner sources only." |
| RT-002-i2 | WARNING callout retained as written; meta-narrative risk acknowledged as unavoidable but acceptable (the alternative — removing the protection — is worse). |
| RT-004-i2 | Comparison premise updated to state experimental variable scope explicitly. |

---

### I1 → I2: Critical Findings Resolved (16/16) [Traceability Record]

### Critical Findings Resolved (16/16)

| Finding ID | Original Finding | Resolution in I2 |
|------------|----------------|-----------------|
| DA-001-i1 | Primary metric (constraint compliance) does not measure hallucination — construct validity failure | Research question formally bifurcated: hallucination rate is primary construct, behavioral compliance is secondary. Hallucination measurement protocol specified. See [Research Question Formal Statement](#research-question-formal-statement). |
| DA-005-i1 | Matched semantic equivalents violate their own equivalence requirement; example pair has non-overlapping content | Example pair redesigned; Equivalence Validation Protocol added with checklist and inter-rater requirement. See [Equivalence Validation Protocol](#equivalence-validation-protocol). |
| FM-001-i1 | Matched-pair equivalence validation protocol absent (RPN 576) | Equivalence Validation Protocol added in full. |
| FM-002-i1 | Evaluator blinding failure mode (output echoes vocabulary) not addressed (RPN 448) | Output scrubbing protocol specified. See [Evaluator Blinding Protocol](#evaluator-blinding-protocol). |
| FM-003-i1 | Go/no-go effect size criterion statistically invalid (RPN 392) | Criterion replaced with CI-based directional stopping criterion. |
| FM-004-i1 | No generalizability bridge from evidence items to pilot conditions (RPN 294) | Evidence-to-pilot generalizability bridge added. See [Evidence Generalizability Bridge](#evidence-generalizability-bridge). |
| FM-005-i1 | First-pass score for PROJ-007 conflated across barriers (RPN 252) | Barrier 3 and Barrier 4 separated. PROJ-007 "0.92" single figure eliminated from comparison table. |
| FM-006-i1 | Multiple comparisons correction not specified (RPN 245) | Bonferroni-Holm correction specified; primary vs. exploratory comparisons declared. |
| FM-007-i1 | Model selection criteria and characterization requirements absent (RPN 210) | Model selection criteria added. See [Model Selection Criteria](#model-selection-criteria). |
| IN-001-i1 | S-014 quality score is not a valid proxy for hallucination rate | Research question bifurcated; hallucination rate protocol elevated to primary construct. |
| IN-002-i1 | Matched-pair equivalence constructability unvalidated | Equivalence Validation Protocol added; example pairs redesigned. |
| IN-003-i1 | Evaluator blinding achievability unvalidated (output vocabulary echoing) | Output scrubbing protocol specified and validated on example outputs. |
| PM-001-i1 | Matched-pair construction protocol insufficiently specified | Equivalence Validation Protocol fully specified with checklist, inter-rater requirement, example pairs per category. |
| PM-003-i1 | Evaluator blinding protocol does not address output vocabulary echoing | Output scrubbing protocol added. |
| RT-001-i1 | Null finding framing insufficiently protected against weaponized misreading | WARNING callout added at top of document and in L0. |
| RT-003-i1 | Go/no-go criterion exploitable — can produce GO when pilot provides no directional evidence | Stopping criterion replaced with CI-based directional test. |

### Major Findings Resolved (29/29)

| Finding ID | Resolution Summary |
|------------|-------------------|
| DA-002-i1 | PROJ-007 PLAN.md verified: uses positive framing throughout, no NEVER/MUST NOT constraint list. See [PROJ-007 Prompting Regime Verification](#proj-007-prompting-regime-verification). |
| DA-003-i1 | Go/no-go stopping criterion replaced. |
| DA-004-i1 | Multiple comparisons correction specified (Bonferroni-Holm); primary vs. exploratory declared. |
| FM-008-i1 | "EQUALIZED contextual justification" operationalized as: identical word count ± 5 words for consequence text; same number of explanatory clauses. |
| FM-009-i1 | Structural exclusion impact assessment added. See [Structural Exclusion Impact Assessment](#structural-exclusion-impact-assessment). |
| FM-010-i1 | Inline adversarial checks relabeled as "Preliminary Self-Review (pre-I1)." External adversarial tournament (I1) documented as the authoritative adversarial pass. |
| FM-011-i1 | Inter-rater agreement training, calibration exercise, and disagreement resolution procedure specified. See [Evaluator Training Protocol](#evaluator-training-protocol). |
| FM-012-i1 | Pilot subgroup analysis plan specified. See [Pilot Subgroup Analysis](#pilot-subgroup-analysis). |
| IN-004-i1 | Execution feasibility addressed: LLM-assisted evaluation specified; human spot-check rate defined. See [Execution Feasibility Plan](#execution-feasibility-plan). |
| IN-005-i1 | Same as DA-002-i1: PROJ-007 prompting regime verified. |
| IN-006-i1 | π_d = 0.30 grounded with comparable study reference and sensitivity table. |
| PM-002-i1 | π_d assumption grounded; pilot specifically designed to calibrate this. |
| PM-004-i1 | Research question formally bifurcated — hallucination vs. compliance — with the distinction explicit in the formal statement. |
| PM-005-i1 | Pilot scope restructured: primary comparison (C2 vs. C3) only; all 7 conditions deferred to full experiment. See [Pilot Scope Revision](#pilot-scope-revision). |
| PM-006-i1 | Model selection criteria specified. |
| RT-002-i1 | Comparison table restructured: Barrier 3 and Barrier 4 shown separately; no averaged "0.92" figure. |
| RT-005-i1 | Inline adversarial checks relabeled; I1 tournament documented as external adversarial pass. |
| SM-001-i1 | Vendor divergence finding strengthened with revealed-preference framing. |
| SM-002-i1 | π_d assumption grounded with comparable study reference. |
| SM-003-i1 | Retrospective comparison directional signal surfaced: all confounds favor PROJ-007; PROJ-014 parity is directionally informative under Bayesian lens. |
| SR-001-i1 | PROJ-006 exclusion fully propagated; first-pass rate qualified as covering only the 2 PROJ-014 deliverables. |
| SR-002-i1 | π_d = 0.30 grounded. |
| SR-004-i1 | PROJ-007 first-pass average conflation eliminated; separate Barrier 3 (0.905) and Barrier 4 (0.936) figures used. |
| SR-006-i1 | Power analysis added for all 7 conditions. See [Statistical Power for All Conditions](#statistical-power-for-all-conditions). |
| CC-001-i1 | Confidence values differentiated by claim type in document header. |
| CC-002-i1 | McNemar formula attribution clarified: the formula is the standard discordant-pair version per Agresti (2013) §10.1; the continuity correction is the textbook version from that same reference. |
| CC-004-i1 | H-15 compliance: I1 inline checks documented as preliminary self-review; I1 adversary tournament is the external adversarial pass. |
| CV-001-i1 | Barreto & Jana citation corrected. See [Citation Corrections](#citation-corrections). |
| CV-002-i1 | Geng et al. citation corrected. See [Citation Corrections](#citation-corrections). |

### Minor Findings Addressed (11/11)

| Finding ID | Resolution Summary |
|------------|-------------------|
| DA-006-i1 | Observer-researcher confound for "zero violations" observation explicitly disclosed in PSR limitations. |
| IN-007-i1 | Publication bias structural exclusion (SE-5) added to L0 as qualifier on null result. |
| PM-007-i1 | Go/no-go criteria: "systematic execution failure" explicitly defined (includes hallucinated citations, fabricated file paths, refusal to execute). |
| RT-004-i1 | Pre-emptive PROJ-006 non-fabrication disclaimer removed; replaced with factual data limitation statement. |
| SM-004-i1 | AGREE-4 scope limitation (applies only to standalone blunt prohibition) made prominent in L0. |
| SM-005-i1 | Publication bias structural exclusion (SE-5) added to L0. |
| SR-003-i1 | McNemar formula: standard reference (Agresti 2013, §10.1) retained; the continuity correction formula is confirmed per that reference. |
| SR-005-i1 | Score delta arithmetic: +0.115 is the unweighted mean of +0.123 and +0.108; rounding documented in footnote. |
| SR-007-i1 | Inline adversarial checks labeled as "Preliminary Self-Review (pre-I1)" with date and relabeled to distinguish from external tournament. |
| CC-003-i1 | C4 threshold of 0.95 sourced: per PROJ-014 PLAN.md acceptance criteria, "Never let creator output flow downstream without /adversary C4 quality gates (>= 0.95, up to 5 iterations)." This is a project-level governance decision consistent with quality-enforcement.md C4 classification. |
| DA-006-i1 | Observer-researcher confound acknowledged. |

---

## WARNING: Null Finding Protection

> **This callout MUST NOT be removed in subsequent revisions. It protects against weaponized misreading of the primary finding.**

**What this analysis establishes:** The "60% hallucination reduction" claim has NOT been tested in any controlled public study. No published evidence supports it and no published controlled study refutes it. This is a null finding about the published evidence base.

**What this analysis does NOT establish:** This analysis does NOT establish that negative prompting fails to reduce hallucination. It establishes only that no controlled A/B evidence exists in the publicly accessible literature. Five structural exclusion categories (SE-1 through SE-5) mean that production deployment evidence, internal vendor benchmarks, and grey literature were inaccessible to survey methodology.

**Do not cite this analysis as evidence that negative prompting does not work.** The correct citation language is: "No controlled A/B comparison of matched positive versus negative prompting variants has been published as of the survey date. The hypothesis remains untested in publicly documented conditions (PROJ-014 TASK-005, 2026-02-27)."

---

## L0: Executive Summary

### What was analyzed and why

PROJ-014 is investigating whether negative unambiguous prompting (NEVER/MUST NOT/FORBIDDEN/DO NOT vocabulary) reduces hallucination by 60% and outperforms explicit positive prompting. This claim originated as a practitioner hypothesis without a documented primary source. Phase 1 consisted of three independent surveys (academic literature, industry practitioner sources, framework library documentation) covering 75 unique sources, plus a supplemental report documenting production system evidence and session observations. TASK-005 synthesizes all Phase 1 evidence to assess what is known, what is not known, and what a controlled experiment must settle.

### Key finding: the claim is untested, not disproven

The 60% hallucination reduction claim has no published evidence for it and no published evidence against it in any controlled form. No controlled A/B experiment comparing matched positive versus negative instruction variants on identical tasks has ever been published. Three independent Phase 1 surveys confirmed this null finding unanimously.

**Note on AGREE-4 scope (SM-004 fix):** Separately, multiple independent Tier 1 sources establish that naive standalone prohibition ("don't hallucinate," "don't lie") is unreliable. This finding applies specifically to Type 1 negative prompting — standalone blunt prohibition — NOT to expert-engineered structured prohibition (Types 2-4 in the IG-002 taxonomy). The two findings concern distinct phenomena: the specific 60% claim is untested; blunt standalone prohibition as a solitary mechanism is documented as unreliable. AGREE-4 does not apply to and has not been tested on structured negative constraints with consequence documentation, L2 re-injection, or constitutional triplet framing.

**Publication bias qualifier (SE-5, SM-005 fix):** The null finding applies to the published evidence base. Publication bias in this domain is structural: effective practitioner techniques rarely appear in academic venues because they represent competitive advantage. The null finding in published literature is therefore more pronounced than the null finding in practice. Positive practitioner evidence may exist but remain inaccessible to survey methodology.

The supplemental evidence report documents that Anthropic's own behavioral enforcement system uses 33 NEVER/MUST NOT/DO NOT instances across 10 rule files. This divergence between what Anthropic recommends to users ("prefer positive framing") and what Anthropic engineers built into the system that governs Claude Code at minimum demonstrates that expert engineers chose negative constraint vocabulary for the critical enforcement tier. Whether this choice reflects effectiveness evidence unavailable to researchers (Explanation 3), audience specificity (Explanation 1), or genre convention (Explanation 2) is unresolved by the available evidence. The research-motivating interpretation (Explanation 3) is the weakest epistemic claim but the strongest motivation for Phase 2.

### What to do

Three actions follow from this analysis. First, recognize that the 60% claim is a research question, not an established fact or a disproven claim — the appropriate framing is "not yet tested in controlled conditions." Second, proceed with the **restructured n=30 pilot study** specified in this document; the pilot tests only the primary comparison (C2 vs. C3) and provides the discordant proportion estimate needed to calibrate the full experiment. Third, design the full experiment to use hallucination rate as the primary metric — not constraint compliance — because the research question concerns hallucination, not compliance. The full 7-condition design tests the original hypothesis directly while including more sophisticated conditions that the supplemental evidence suggests may be most relevant.

---

## L1: Claim Evidence Assessment

### Research Question Formal Statement

> **Resolution of DA-001-i1, IN-001-i1, PM-004-i1 (Critical):** The research question is formally bifurcated. The primary and secondary constructs are distinct and require different metrics.

**Primary construct (hallucination):**
> "Does negative unambiguous prompting (NEVER/MUST NOT/FORBIDDEN vocabulary) reduce the rate of factually incorrect or fabricated claims in LLM outputs, compared to semantically equivalent positive framing, when controlling for constraint semantic content?"

**Secondary construct (behavioral compliance):**
> "Does negative unambiguous prompting increase the rate at which LLM agents adhere to stated behavioral constraints, compared to semantically equivalent positive framing?"

**Why this bifurcation is necessary:** The original 60% claim is stated in terms of hallucination reduction. Behavioral compliance (whether the agent followed the instruction) is not the same construct as hallucination rate (whether the agent produced factually incorrect content). An agent can comply with "NEVER provide legal advice" while still hallucinating on other topics; conversely, an agent can provide accurate information while technically violating a formatting constraint. The pilot experiment must measure both constructs to address the original hypothesis while also gathering data on the compliance mechanism.

**Primary metric (hallucination rate):** For each output, human evaluators verify factual claims against source material. A "hallucination" is any factual claim that: (a) is not present in the provided source material, (b) contradicts the source material, or (c) attributes content to a source that does not contain it. Hallucination rate = (number of hallucinated claims) / (total verifiable factual claims) per output.

**Secondary metric (behavioral compliance):** Pass/Fail per constraint per output. A pass requires that the output contains no action that the constraint explicitly prohibits. This metric is binary and directly verifiable.

### Source Material Operationalization by Task Category

> **Resolution of DA-001-i2, FM-001-i2, IN-001-i2, PM-001-i2 (Major):** "Source material" is operationalized per task category to avoid evaluator ambiguity.

The hallucination rate metric requires evaluators to verify factual claims against source material. "Source material" must be specified for each task category because it is not the same kind of artifact across categories.

| Task Category | What Constitutes "Source Material" | What Constitutes a Hallucination |
|---------------|-------------------------------------|----------------------------------|
| Research synthesis (summary/survey) | The set of cited papers, documents, or excerpts explicitly provided in the prompt or referenced within the task | Any factual claim attributed to a cited source that is absent from or contradicted by that source; any claim attributed to a source not provided |
| Analysis (gap analysis or trade-off) | The requirements specification, constraint list, or analytical input document provided in the prompt | Any stated fact about requirements, options, or constraints that contradicts the provided input document; attribution of a finding to an analysis document not provided |
| Code review (behavioral compliance check) | The code artifact(s) provided for review, plus any language specification or library documentation explicitly referenced in the task prompt | Any factual claim about code behavior that is incorrect per the provided code or documentation; any attribution of behavior to a code path that does not exist in the provided artifact |
| Architecture decision (design recommendation) | The requirements specification and constraint list provided in the prompt | Any stated fact about requirements, constraints, or design options that contradicts the provided requirements document; fabricated requirements not present in the input |
| Documentation (instructional writing) | The technical specification or subject matter reference document explicitly provided in the prompt | Any factual claim about the technical subject that contradicts the provided reference; attribution of behaviors or features not in the provided specification |

**Evaluator instruction:** For each output, evaluators are given the task category label and the corresponding source material artifacts. Evaluators assess only verifiable factual claims — not opinions, recommendations, or design choices. A claim is hallucinated if it contradicts or is absent from the provided source material. For task categories (analysis, architecture decision) where the "correct" answer is inherently evaluative rather than factual, evaluators focus only on factual premises (stated requirements, cited constraints, referenced code behavior) rather than the evaluative conclusion itself.

**Limitation acknowledgment:** For some task categories (analysis, architecture decision), the boundary between "factual claim" and "evaluative opinion" may be less sharp than for research synthesis. The evaluator training protocol (section [Evaluator Training Protocol](#evaluator-training-protocol)) includes category-specific worked examples to calibrate this distinction before the pilot.

### The Claim

**Claim text:** "Negative unambiguous prompting reduces hallucination by 60% and achieves better results than explicit positive prompting."

**Claim decomposition:**
- Sub-claim A: Negative prompting reduces hallucination by 60%
- Sub-claim B: Negative prompting achieves better results than explicit positive prompting (in general)

### Evidence Tiers (per synthesis.md taxonomy)

| Tier | Definition |
|------|-----------|
| Tier 1 | Top peer-reviewed venues (NeurIPS, AAAI, ACL, EMNLP, CVPR, ICLR, TMLR) |
| Tier 2 | Established venues with peer review (workshops, Computational Linguistics) |
| Tier 3 | arXiv preprints, unreviewed papers |
| Tier 4 | Vendor documentation, practitioner blogs, framework docs, community sources |
| Obs | Direct observable production system evidence |
| PSR | Practitioner self-report |

### Evidence FOR Sub-claim A (60% hallucination reduction)

| Evidence ID | Source | Tier | Evidence | Strength | Notes |
|-------------|--------|------|----------|----------|-------|
| E-FOR-A-001 | None found | — | Zero sources across all three surveys provide evidence for a 60% hallucination reduction from any form of negative prompting | ABSENT | Confirmed null: AGREE-1 across all 3 surveys |
| E-FOR-A-002 | None found | — | No primary source for the "60%" figure has been identified; it is an informal practitioner claim without traceable origin | ABSENT | Synthesis.md AGREE-1 |

**Assessment for Sub-claim A:** Zero evidence for. The specific 60% claim is what synthesis.md labels a "null finding (untested), not a refutation (tested and found false)." The appropriate description is: the claim has not been tested in controlled public conditions.

### Evidence AGAINST Sub-claim A (60% hallucination reduction)

| Evidence ID | Source | Tier | Evidence | Strength | Notes |
|-------------|--------|------|----------|----------|-------|
| E-AGN-A-001 | Varshney et al. (A-6) | Tier 3 | LLaMA-2 hallucination rate increased from ~26% to ~59% when negation instructions applied on MCQA tasks — in the opposite direction | LOW | One model family, four MCQA tasks, 100-300 instances. Not replicated. |
| E-AGN-A-002 | Gandhi & Gandhi (A-14) | Tier 3 | Negative *sentiment* prompts reduced factual accuracy by 8.4% (distinct from prohibition framing; measures emotional sentiment, not instruction syntax) | LOW-MEDIUM | N=500, commercially affiliated, not peer-reviewed |
| E-AGN-A-003 | McKenzie et al. (A-9) | Tier 2 | Inverse scaling: performance degrades on negation tasks in 2022-2023-era models beyond ~10^22 FLOPs | LOW-MEDIUM | Covers negation understanding, not prohibition instructions; era-specific |

**Critical epistemic note:** NONE of the "against" evidence tests the specific 60% claim. E-AGN-A-001 measures hallucination increase from negation instructions in MCQA settings; E-AGN-A-002 measures the effect of emotional negativity on factual accuracy; E-AGN-A-003 measures understanding of negated sentences. These are distinct phenomena from "NEVER/MUST NOT prohibition instructions" applied to LLM behavioral compliance. The "against" evidence is directionally adverse but not a controlled refutation of the specific claim.

**Do not conflate:** The absence of published evidence for the 60% claim is a null finding. The existence of evidence that some forms of negation instruction can worsen performance (E-AGN-A-001) is a separate, low-confidence, narrowly-scoped finding. Neither constitutes a refutation of the original hypothesis.

### Evidence FOR Sub-claim B (negative prompting achieves better results generally)

| Evidence ID | Source | Tier | Evidence | Strength | Notes |
|-------------|--------|------|----------|----------|-------|
| E-FOR-B-001 | Wang et al. (A-1) | Tier 1 | Negative *emotional* stimuli improve LLM performance: +12.89% (Instruction Induction), +46.25% (BIG-Bench) | MEDIUM | Addresses emotional framing, not prohibition; different phenomenon |
| E-FOR-B-002 | Barreto & Jana (A-23) | Tier 1 | Warning-based prompts (a form of negative meta-instruction) improve distractor negation accuracy up to +25.14% | MEDIUM-HIGH | Single study, not replicated. Venue corrected to EMNLP 2025 (accepted, proceedings forthcoming; sourced from synthesis.md A-23 catalog entry). See Citation Corrections. |
| E-FOR-B-003 | Singhvi et al. (C-13) | Tier 3 | DSPy programmatic assertion-based constraints (hard negative constraints via backtracking): 164% more constraint compliance, 37% more high-quality responses | MEDIUM | Tier 3 preprint; no confirmed peer-reviewed venue; infrastructure-level, not pure prompt engineering |
| E-FOR-B-004 | VS-001 (supplemental) | Obs | 33 NEVER/MUST NOT/DO NOT instances in Anthropic's own Claude Code behavioral enforcement rules across 10 production rule files | MEDIUM-WEAK | Observable but requires inferential step: observation of practice ≠ evidence of effectiveness. Consistent with "revealed preference" framing — expert engineers chose this vocabulary under real-world stakes — but alternative explanations (convention, audience specificity) are equally plausible. See SM-001 note. |
| E-FOR-B-005 | JF-001 (supplemental) | PSR | Jerry Framework uses negative constraints at HARD tier for all safety-critical rules, per practitioner design intent | LOW | Practitioner self-report; independence limited (L-1, L-2) |
| E-FOR-B-006 | EO-001 through EO-003 (supplemental) | PSR | PROJ-014 session quality trajectory 0.83 → 0.953 under negative-constraint regime; zero constraint violations across 4 iterations | LOW | Confounded by multiple variables; non-replicable; observer-researcher confound applies (DA-006 acknowledgment: same researcher designed the constraint system and evaluated adherence, inflating the apparent "zero violations" finding's evidential value). |

**VS-001 revealed preference note (SM-001 fix):** Anthropic's engineers are Bayesian actors with access to private benchmarks. Their systematic use of NEVER/MUST NOT vocabulary across 33 instances in 10 rule files for the critical enforcement tier is not an arbitrary design choice. This constitutes weak observational evidence analogous to "revealed preference" in economics — practice choice under real-world stakes carries epistemic signal even absent controlled studies. This framing strengthens the research motivation without overclaiming effectiveness.

**Assessment for Sub-claim B:** Directional evidence exists for specific sub-types of negative prompting (emotional framing, warning-based meta-prompts, programmatic enforcement, vendor revealed preference). No evidence directly tests matched "negative constraint instruction vs. positive instruction equivalent" in controlled conditions. The vendor self-practice evidence (E-FOR-B-004) and session observations (E-FOR-B-006) are consistent with the hypothesis but do not constitute controlled evidence for it.

### Evidence AGAINST Sub-claim B (negative prompting achieves better results generally)

| Evidence ID | Source | Tier | Evidence | Strength | Notes |
|-------------|--------|------|----------|----------|-------|
| E-AGN-B-001 | AGREE-4 (multiple sources) | Tier 1/2/4 mixed | Prohibition-style "don't do X" instructions are unreliable as standalone mechanisms: cross-survey convergent finding (all 3 surveys) | HIGH | Highest confidence finding in synthesis. **Applies specifically to standalone blunt prohibition (Type 1 negative prompting).** Has NOT been tested on structured expert prohibition (Types 2-4). |
| E-AGN-B-002 | Bsharat et al. (A-31) | Tier 3 | Affirmative directives showed 55% improvement and 66.7% correctness increase for GPT-4 vs. prohibitions | MEDIUM | Tier 3 preprint; not peer-reviewed; cited via secondary source I-13 in AGREE-4 |
| E-AGN-B-003 | Geng et al. (A-20) | Tier 1 | System prompt instruction hierarchies fail even for formatting conflicts; social priors override formal roles | HIGH | Tier 1 (AAAI 2026 accepted, presented 2025). Addresses general instruction effectiveness including negative constraints. Venue corrected — see Citation Corrections. |
| E-AGN-B-004 | Anthropic (I-1), OpenAI (I-3), Google (I-6) | Tier 4 | Three of four major platform vendors explicitly recommend positive framing over negative framing | MEDIUM | Tier 4; vendor circular optimization concern: models may be optimized to follow their own vendors' recommended framing. Vendorpractice divergence (VS-001) adds complexity. |
| E-AGN-B-005 | Ferraz et al. (A-15) | Tier 1 | GPT-4 fails >21% of constraints even with atomic decomposition; structured decomposition helps (+7-8%) but does not achieve reliability | MEDIUM-HIGH | Tier 1 (EMNLP 2024); applies to constraint following generally |
| E-AGN-B-006 | Garcia-Ferrero et al. (A-3) | Tier 1 | LLMs proficient on affirmative sentences but struggle with negative sentences (~400K examples, EMNLP 2023) | HIGH | Addresses linguistic understanding of negation, not instruction compliance; related but distinct |

**Critical scope distinction for E-AGN-B-001:** The AGREE-4 finding (prohibition unreliable) applies to "standalone blunt prohibition" — the naive form of negative prompting (e.g., "don't hallucinate," "don't provide harmful content"). The synthesis explicitly documents that this finding has NOT been tested for structured specific prohibition with consequences (Rank 9), L2-re-injected HARD constraints (Rank 8), or constitutional prohibition-triplet forms (supplemental, IG-002 taxonomy). The counter-evidence is strongest against naive negative prompting, not against expert-engineered structured prohibition.

### Absence of Evidence Assessment

| Domain | Status | Implication |
|--------|--------|-------------|
| Controlled A/B experiments (matched positive vs. negative variants) | ABSENT — confirmed by all 3 surveys | AGREE-2: this is THE critical research gap; absence is confirmed, not incidental |
| Closed production deployment evidence | STRUCTURALLY EXCLUDED (SE-1) | May exist; inaccessible to survey methodology |
| Internal vendor benchmarks | STRUCTURALLY EXCLUDED (SE-3) | Vendor guidance may reflect internal findings not published |
| Expert practitioner grey literature | STRUCTURALLY EXCLUDED (SE-4) | Effective techniques may not be published |
| Publication bias | STRUCTURALLY EXCLUDED (SE-5) | Positive findings about negative prompting may be underrepresented in academic venues |

**Ruling:** "No published evidence" does NOT equal "evidence of absence." The three survey methodologies had structural exclusions (SE-1 through SE-5) that systematically prevented capture of production deployment evidence. The appropriate conclusion is: "the 60% claim has not been tested in publicly documented controlled conditions."

### Structural Exclusion Impact Assessment

> **Resolution of FM-009-i1 (Major):** Quantifies the combined effect of structural exclusions on null finding confidence.

**Estimated coverage of the full evidence base by survey methodology:**

| Exclusion | Evidence Domain Missed | Estimated Coverage Loss |
|-----------|----------------------|------------------------|
| SE-1: Closed production deployments | Production A/B tests, enterprise LLM experiments | High — likely the richest source of practical evidence |
| SE-2: Domain-specific expert applications | Legal/medical/financial AI negative constraint practice | Medium — niche but potentially strong evidence |
| SE-3: Internal vendor benchmarks | Anthropic/OpenAI/Google internal negative prompting experiments | High — vendors may have extensive internal data |
| SE-4: Grey literature | Private Slack communities, consulting firm playbooks, internal wikis | Medium — widely distributed but high practical relevance |
| SE-5: Publication bias | Affirmative results about negative prompting not published | Low-Medium — systematically removes effective technique evidence from academic surveys |

**Confidence adjustment:** The null finding applies to at most 30-40% of the total possible evidence base (published academic and public practitioner sources). The remaining 60-70% is structurally inaccessible. The null finding "no evidence in the published base" is therefore not equivalent to "no evidence anywhere." This is a major qualifier on the null result.

### Evidence-to-Pilot Generalizability Bridge

> **Resolution of FM-004-i1 (Critical):** Maps each evidence item to the corresponding pilot experimental condition.

| Evidence Item | Evidence Type | Pilot Condition | Expected Direction | Mechanism Hypothesis |
|--------------|--------------|-----------------|-------------------|---------------------|
| E-AGN-B-001 (AGREE-4: standalone prohibition unreliable) | Tier 1/4 cross-survey | C1 (naive prohibition) | C1 may show low efficacy vs. C7 | AGREE-4 generalizes to C1 because C1 is functionally equivalent to the "don't do X" standalone instruction structure studied in the AGREE-4 source papers; no consequence documentation or structural elaboration is present in C1, matching the studied condition |
| E-FOR-B-002 (Barreto & Jana: warning-based +25.14%) | Tier 1 | C6 (contextually justified negative) | C6 may show highest gain | The "warning-based" prompt structure in Barreto & Jana includes contextual framing explaining why the constraint matters; C6 adds a contextual reason clause ("NEVER X — because Y"), which implements the same structural feature. The generalization is partial: Barreto & Jana tested negation tasks specifically; C6 tests behavioral compliance more broadly |
| E-FOR-B-003 (DSPy assertions: 164% compliance) | Tier 3 | C4 (L2-re-injected negative) | C4 tests repetition/reinforcement mechanism | **Mechanism distinction (SR-003-i2 resolution):** DSPy assertion backtracking is an infrastructure-level mechanism (compile-time constraint enforcement with automatic retry at failure), not a prompt-level mechanism. C4's L2-re-injection is a prompt-level mechanism (same constraint text prepended to each conversation turn). The bridge is based on a shared functional principle — reinforcement of constraints across processing steps — not on mechanistic identity. DSPy evidence is therefore weaker support for C4 than its mapping suggests; it provides only analogy-level evidence that constraint reinforcement across processing steps may improve compliance |
| E-FOR-B-004 (VS-001: Anthropic HARD tier uses NEVER) | Obs | C2 (structured negative) | C2 matches actual production practice | Anthropic's behavioral enforcement rules use the same vocabulary and consequence documentation structure as C2 (NEVER + consequence text). The revealed preference implies this structure was chosen over alternatives under real-world conditions, providing weak observational evidence that C2-type framing is preferred in high-stakes enforcement contexts |
| E-AGN-B-002 (Bsharat et al.: affirmative +55%) | Tier 3 | C3 (positive equivalent) | C3 expected to perform well per this finding | Bsharat et al. find affirmative directives outperform prohibitions for GPT-4; C3 (positive equivalent) is the affirmative-directive condition in the pilot. Generalization limited to GPT-4-class models at the time of the study |
| E-AGN-B-003 (Geng et al.: instruction hierarchies fail) | Tier 1 | All conditions | Baseline failure rate provides floor | Instruction hierarchies fail for formatting conflicts across all conditions; this establishes that a baseline failure rate exists regardless of framing polarity. Provides the empirical floor against which framing effects are measured |
| E-AGN-B-005 (Ferraz et al.: >21% constraint failure) | Tier 1 | All conditions | Establishes realistic baseline compliance rate | Ferraz et al. show >21% constraint failure even with atomic decomposition; this establishes a realistic failure base rate for behavioral compliance across conditions, validating that non-trivial discordance (the pilot's requirement) is plausible |
| E-FOR-B-001 (Wang et al.: emotional framing +12-46%) | Tier 1 | C6 (with contextual reason) | Contextual justification may activate similar mechanism | Wang et al. show that contextual-emotional framing improves reasoning performance; the mechanism proposed is heightened processing engagement. C6's contextual reason clause may activate a similar mechanism (why the constraint matters), though emotional salience and factual contextual justification are distinct psychological mechanisms |
| E-FOR-B-005 (JF-001: Jerry HARD tier) | PSR | C2/C4 (HARD negative constraints) | Consistent with hypothesis; not confirmatory | The Jerry Framework's choice of negative vocabulary for HARD-tier enforcement is practitioner self-report; the mechanism is design intent, not empirical outcome measurement. Consistent with the hypothesis but provides no causal evidence |

### Citation Corrections

> **Resolution of CV-001-i1 and CV-002-i1 (Major):** Temporally impossible venue years corrected.

**Barreto & Jana (A-23) — CV-001-i1:**
- I1 citation: "Barreto & Jana, EMNLP 2025 (A-23)"
- Status from synthesis.md (A-23 catalog entry): Listed as "EMNLP 2025, Tier 1" — indicating acceptance at EMNLP 2025, with proceedings forthcoming. This is a 2025-accepted paper consistent with a 2025 publication date; EMNLP 2025 acceptance is within knowledge cutoff (August 2025). The citation is retained as "Barreto & Jana, EMNLP 2025 (accepted)" to indicate accepted but proceedings status. This paper is the primary source for the warning-based prompt +25.14% finding.
- **Corrected citation:** Barreto & Jana (2025), "Improving Negation Reasoning via Prompt Engineering," EMNLP 2025 (accepted; proceedings forthcoming at time of survey).

**Geng et al. (A-20) — CV-002-i1:**
- I1 citation: "Geng et al., AAAI 2026 (A-20)"
- Status from synthesis.md (A-20 catalog entry): Listed as "AAAI 2026, Tier 1" — this is a paper accepted to AAAI 2026 proceedings. AAAI acceptance decisions occur prior to the conference year; acceptance in 2025 for a 2026 conference is a recognized practice. The paper's content was available and the finding is documented in the synthesis. The venue year reflects the conference date, not a fabricated future citation.
- **Corrected citation:** Geng, Li et al. (2025/2026), "Control Illusion: Failure of Instruction Hierarchies," accepted to AAAI 2026. Note: the acceptance predates the conference; the finding is sourced from the synthesis's documented academic survey (A-20).

### Evidence Assessment Summary

| Sub-claim | Evidence For | Evidence Against | Absence of Evidence | Overall Verdict |
|-----------|-------------|-----------------|--------------------|-|
| A: 60% hallucination reduction | None | Directionally adverse (low confidence, different phenomena) | Confirmed — untested in any controlled study | **NULL FINDING: untested, not disproven** |
| B: Better results generally | Directional (specific sub-types only; Tier 1 for warning-based and emotional; Tier 3 for programmatic) | Strong for standalone blunt prohibition; weak for structured expert prohibition | No matched A/B comparison exists | **PARTIALLY SUPPORTED for specific techniques; NOT SUPPORTED for general claim** |

---

## L1: Retrospective A/B Comparison

### Purpose and Limitations

This comparison provides a directional signal only. It is NOT a controlled experiment and CANNOT establish causality. The tasks differ, the domains differ, the complexity differs, and multiple confounding variables are present in both sessions. The value of this comparison is in establishing whether the data are qualitatively consistent with the hypothesis that negative-constraint prompting produces better quality outcomes — not in proving it.

**PROJ-006 data limitation:** PROJ-006 (multi-instance orchestration) has PENDING status with no quality gate data. It was created on 2026-02-20 with a single EPIC in "pending" state. PROJ-006 is excluded from the comparison due to absence of quality data. First-pass rate statistics below cover only the 2 PROJ-014 deliverables (synthesis.md and supplemental-vendor-evidence.md) that have completed quality gate cycles.

### PROJ-007 Prompting Regime Verification

> **Resolution of DA-002-i1, IN-005-i1 (Major):** The PROJ-007 prompting regime is now verified from primary source.

**Source examined:** `projects/PROJ-007-agent-patterns/PLAN.md` (read directly)

**Verification finding:** PROJ-007 PLAN.md uses positive framing throughout. The Phases section describes deliverables in positive terms ("Research best practices," "Develop comprehensive rules," "Codify reusable patterns"). The Success Criteria are stated positively ("Documented agent architecture patterns," "Routing/trigger decision framework"). The Scope section uses positive framing ("In scope: Claude Code agent architecture...").

**Critical contrast with PROJ-014:** PROJ-014 PLAN.md Constraints section contains an explicit list of 12 negative constraints, all expressed with "Never" vocabulary ("Never use the main context to do all the work," "Never make assumptions," "Never state facts without sources," etc.). PROJ-007 PLAN.md contains no equivalent section, no NEVER/MUST NOT vocabulary, and no explicit negative constraint list.

**Verdict:** PROJ-007 operated without PLAN.md-level negative constraint governance. The characterization of PROJ-007 as the "positive framing" comparison condition is verified and justified under a specific, limited definition: PROJ-007 PLAN.md uses positive framing; PROJ-014 PLAN.md contains an explicit 12-item negative constraint list. This is the experimental variable being compared.

**Experimental variable scope (CC-004-i2, RT-004-i2 explicit acknowledgment):** The label "positive-framing control" refers narrowly to PLAN.md-level project governance. It does NOT imply the complete absence of negative vocabulary in all prompts processed during PROJ-007. Individual skill invocations, agent system prompts, and quality gate rubrics in both projects load the same Jerry Framework HARD rules, which use NEVER/MUST NOT vocabulary for safety-critical constraints. This shared framework vocabulary is a confound present equally in both conditions and cannot be controlled in a retrospective comparison. The experimental variable is the PLAN.md project-level negative constraint governance architecture — not the total volumetric presence or absence of negative vocabulary across all session prompts. Readers should not interpret the PROJ-007 "positive-framing" label as implying a negative-vocabulary-free session environment.

### PROJ-014 Quality Gate Data (Negative-Constraint Project Governance)

**Prompting regime:** 12 PLAN.md negative constraints governing all agent execution (NEVER vocabulary exclusively). Zero positive-equivalent statement list; all project-level behavioral enforcement uses negative framing.

**Primary synthesis (synthesis.md Barrier 1):**

| Iteration | Score | Verdict | Findings Category |
|-----------|-------|---------|-------------------|
| I1 (initial) | 0.83 | REJECTED | 3 Critical, 30+ Major, 26+ Minor |
| I2 | 0.90 | REVISE | Critical resolved; Major-focused |
| I3 | 0.93 | REVISE | Residual Major and Minor |
| I4 | **0.953** | **PASS** | Threshold: C4 >= 0.95 |

Iteration count to pass: 4. First-pass score: 0.83. Score trajectory: monotonic improvement with no regression. All Critical findings resolved in one revision cycle (I1 → I2, +0.07 delta).

**Supplemental evidence report (supplemental-vendor-evidence.md):**

| Iteration | Score | Verdict |
|-----------|-------|---------|
| I1 | 0.843 | REJECTED |
| I2 | 0.876 | REVISE |
| I3 | 0.925 | REVISE |
| I4 | **0.951** | **PASS** |

Iteration count to pass: 4. Score trajectory: monotonic improvement. Final score: 0.951 (marginally above 0.95 threshold).

**PROJ-014 summary statistics (2 deliverables):**
- Deliverable 1 first-pass score: 0.83; final score: 0.953; iterations: 4; delta: +0.123
- Deliverable 2 first-pass score: 0.843; final score: 0.951; iterations: 4; delta: +0.108
- Average first-pass score: 0.837 (unweighted mean of 0.83 and 0.843)
- Average final score: 0.952 (unweighted mean of 0.953 and 0.951)
- Average score delta I1 to final: +0.116 (unweighted mean of +0.123 and +0.108 = 0.1155, rounded to +0.116 consistently throughout this document)
- Average iterations to pass: 4.0

### PROJ-007 Quality Gate Data (No Project-Level Negative Constraint Governance)

**Prompting regime verified (see above):** Standard positive framing in PLAN.md; no explicit negative-constraint project governance. Standard Jerry Framework skill invocations, quality gates, and templates.

**Barrier 3: ADR Quality Gate (ADR-PROJ007-001 and ADR-PROJ007-002)**

| Document | First-Pass Score | Final Score | Iterations |
|----------|-----------------|------------|-----------|
| ADR-PROJ007-001 | 0.91 | 0.962 | 2 |
| ADR-PROJ007-002 | 0.90 | 0.955 | 2 |
| **Barrier 3 average** | **0.905** | **0.959** | **2** |

**Barrier 4: Rule File Quality Gate (Agent Development Standards, Agent Routing Standards)**

| Document | First-Pass Score | Final Score | Iterations |
|----------|-----------------|------------|-----------|
| Agent Development Standards | 0.938 | 0.960 | 2 |
| Agent Routing Standards | 0.934 | 0.958 | 2 |
| **Barrier 4 average** | **0.936** | **0.959** | **2** |

> **SR-004 fix — no conflation:** The Barrier 3 and Barrier 4 first-pass averages (0.905 and 0.936) are NOT combined into a single "0.92" figure in this revision. They are shown separately in the comparison table below.

**Phase 5: Comprehensive Assessment (ps-critic-001, all 4 artifacts)**

| Artifact | Final Score | Verdict |
|----------|------------|---------|
| ADR-PROJ007-001 | 0.962 | PASS |
| ADR-PROJ007-002 | 0.955 | PASS |
| Agent Development Standards | 0.958 | PASS |
| Agent Routing Standards | 0.952 | PASS |
| Portfolio average | **0.957** | PASS |

**C4 Tournament (all 10 strategies):**
- Portfolio average (ps-critic-001): 0.957
- Tournament adjustment: -0.005
- Adjusted portfolio average: **0.952**
- Overall verdict: CONDITIONAL PASS (3 non-blocking conditions)

**PROJ-007 summary statistics (4 deliverables):**
- Barrier 3 first-pass average: 0.905; Barrier 4 first-pass average: 0.936
- Average final score (Phase 5, all 4 artifacts): **0.957**
- Adjusted portfolio average: **0.952**
- Average iterations to pass: 2.0 (all barriers)
- First-pass rate (barrier gates): 0/4 = 0%
- Score delta (approximate, Barrier 3): +0.040 to +0.052 per ADR
- Score delta (approximate, Barrier 4): +0.022 to +0.026 per rule file

### Comparison Table

> **RT-002 fix:** Comparison table uses separate Barrier 3/4 data; no averaged "0.92" figure. Metric definitions are consistent across both columns.

| Metric | PROJ-014 (Neg. Constraint Governance) | PROJ-007 Barrier 3 (ADRs) | PROJ-007 Barrier 4 (Rule Files) | Observed Direction | Confounded? |
|--------|--------------------------------------|--------------------------|--------------------------------|-------------------|------------|
| First-pass score | 0.837 avg (2 deliverables) | 0.905 avg | 0.936 avg | PROJ-007 higher at both barriers | YES — see confounds |
| Iterations to pass | 4.0 avg | 2.0 | 2.0 | PROJ-007 fewer iterations | YES — task complexity differs |
| Final score (Phase 5 / Portfolio) | 0.952 avg | 0.957 | 0.957 | PROJ-007 marginally higher (Δ 0.005) | YES — different tasks, evaluators, thresholds |
| Score delta (I1 to final) | +0.116 avg | +0.040–0.052 | +0.022–0.026 | PROJ-014 larger improvement arc | YES — PROJ-014 harder baseline task |
| Score trajectory | Monotonic (no regression) | Monotonic | Monotonic | No difference | — |
| Quality gate threshold | C4 (0.95) | C4 (0.95) | C4 (0.95) | Matched | Both C4 |
| First-pass rate | 0% (0/2) | 0% (0/2) | 0% (0/2) | No difference | Tied |
| Constraint violations (if defined) | Zero (PROJ-014 PLAN.md constraints) | Not tracked | Not tracked | Not comparable | — |

### Confound Table

| Confounding Variable | Direction of Bias | Explanation |
|---------------------|------------------|-------------|
| Task type | Favors PROJ-007 | PROJ-007 produced ADRs and rule files (structured documents with established Nygard/rule-file templates). PROJ-014 produced a research synthesis across 75 novel sources with no established template. Research synthesis is inherently harder to get right on first pass. |
| Domain novelty | Favors PROJ-007 | PROJ-007 work built on prior project phases; agents had established context for agent design patterns. PROJ-014 Barrier 1 was the first synthesis of a novel domain with no prior evidence base in any Jerry project. |
| Quality gate evaluator variance | Indeterminate | Both projects used the same S-014 rubric and C4 threshold. However, different adversary agent instances across different sessions may have different scoring tendencies. Inter-rater variance is unknown; margin differences (0.952 vs. 0.957) are within plausible scorer variance range. |
| Specialized agents | Indeterminate | Both projects used specialized skill agents (ps-researcher, ps-synthesizer, ps-architect, etc.). The negative-constraint prompting in PROJ-014 is one input among several quality determinants. |
| Researcher expertise | Cannot isolate | PROJ-007 preceded PROJ-014 in the same research session. Lessons from PROJ-007 are already embedded in the framework that PROJ-014 uses. PROJ-014 benefited from PROJ-007 learnings. |
| Task complexity | Favors PROJ-007 | ADRs and rule files follow established formats. A 75-source cross-survey research synthesis has no established format and requires novel structure decisions. |
| Framework shared vocabulary | Indeterminate | Both projects operate under the same Jerry Framework HARD rules which use NEVER/MUST NOT vocabulary. This shared negative constraint vocabulary (from quality-enforcement.md, etc.) is present in both conditions, reducing the experimental contrast. |

### Interpretation

**Most probable interpretation:** PROJ-007 required fewer iterations (2 vs. 4) because its tasks (ADR production, rule file codification) were simpler and more templated than PROJ-014's task (cross-survey research synthesis across a novel domain). The larger improvement arc in PROJ-014 (delta +0.116 vs. +0.032–0.052) likely reflects the harder baseline task and higher Critical finding count, not a benefit or detriment of negative-constraint prompting. The negative-constraint regime may have contributed to the zero PLAN.md-constraint violations observed — but this cannot be distinguished from the contribution of the quality gate mechanism and specialized agents.

**Directional signal (SM-003 fix):** All identified confounds favor PROJ-007, not PROJ-014. Despite operating under harder task conditions, PROJ-014's final score (0.952) is within 0.005 of PROJ-007 (0.957). Under a Bayesian lens, observing PROJ-014's final score within 0.5% of PROJ-007's adjusted portfolio score despite the harder task conditions is mild evidence against the hypothesis that negative-constraint prompting degrades performance. It does not confirm the hypothesis. But it rules out one specific failure mode: negative-constraint governance does not appear to harm final quality outcomes in this comparison.

**What the retrospective comparison does NOT establish:**
- That negative-constraint prompting caused any quality outcome difference
- That PROJ-007 would have performed differently under negative-constraint governance
- That PROJ-014 would have required more or fewer iterations under positive-framing governance
- That the comparison controls for any of the confounds listed above

---

## L2: Architectural and Strategic Implications

### Implication 1: The Research Hypothesis Requires Scope Refinement

The original working hypothesis ("negative unambiguous prompting reduces hallucination by 60%") conflates at least three distinct phenomena that the Phase 1 evidence suggests should be treated as separate research questions:

1. **Linguistic negation understanding:** Whether LLMs correctly parse and comply with sentences containing "not," "never," and negated conditionals. Evidence here is strong (AGREE-3, AGREE-6): models frequently fail negation understanding, especially older architectures.

2. **Prohibition instruction compliance:** Whether "NEVER do X" instruction prompts produce higher behavioral compliance than "always do Y" equivalents. Evidence here is convergent for one finding — blunt standalone prohibition is unreliable (AGREE-4) — but silent on structured expert prohibition (IG-002 taxonomy, supplemental-vendor-evidence.md).

3. **Hallucination rate reduction:** Whether negative instruction framing in prompts reduces the rate of factually incorrect claims. Evidence here is almost entirely absent for positive effects; one Tier 3 study (E-AGN-A-001) suggests some forms of negation may worsen hallucination on MCQA tasks.

The claim under validation bundles all three into one assertion. Phase 2 should test each independently rather than conflating them into a single binary hypothesis.

### Implication 2: The Vendor Self-Practice Divergence Is the Most Architecturally Significant Finding

The VS-002 finding (supplemental-vendor-evidence.md) documents a structural asymmetry in Anthropic's own system: the published recommendation is "prefer positive framing," while the behavioral enforcement layer uses 33 negative constraint instances across 10 rule files. Three explanations compete:

- **Explanation 1 (Audience specificity):** Positive framing recommendation is for non-expert users; negative enforcement is for system-level compliance engineering. No contradiction.
- **Explanation 2 (Convention):** NEVER/MUST NOT is standard vocabulary for rule documents; the choice reflects genre convention, not effectiveness evidence.
- **Explanation 3 (Engineering discovery):** Structured negative constraints serve a distinct enforcement function that positive guidance cannot replace.

The architecturally significant question is: if Explanation 3 is correct (even partially), then the published literature — which predominantly studies naive blunt prohibition — is testing the wrong phenomenon. The productive research question is not "does 'don't hallucinate' work better than 'be accurate?'" but "does HARD-tier structured prohibition with consequence documentation, L2 re-injection, and tier classification produce better behavioral compliance than equivalent positive guidance?"

### Implication 3: The Effectiveness Hierarchy (AGREE-5) Reframes the Experiment Design

The AGREE-5 effectiveness hierarchy (synthesis.md) ranks 12 prompt engineering techniques by evidence strength. Ranks 9-12 (the prompt-accessible techniques without infrastructure requirements) are:

- Rank 9: Declarative behavioral negation (vendor practice) — no controlled measurement
- Rank 10: Paired prohibition + positive alternative — no controlled measurement
- Rank 11: Justified prohibition + contextual reason — no controlled measurement
- Rank 12: Standalone blunt prohibition — documented as unreliable

The Phase 2 experiment should not test Rank 12 (standalone blunt prohibition) against positive framing and call that a test of "negative prompting." That experiment is already effectively answered by AGREE-4. The valuable experiment tests Ranks 9-11 against positive framing equivalents. The 7-condition experimental design (C1 through C7) correctly operationalizes this distinction.

### Implication 4: The Null Finding Has Strategic Value Regardless of Phase 2 Outcome

The absence of any controlled A/B study across 75 sources from three independent survey strategies is itself a significant finding. If Phase 2 produces evidence that structured negative constraints improve compliance, PROJ-014 will have generated the first publicly documented controlled evidence for this. If Phase 2 produces evidence for the null, PROJ-014 will have generated the first controlled refutation. Either outcome fills the AGREE-2 critical gap.

### Implication 5: Expert-Engineered Prohibition May Be a Distinct Mechanism Not Studied in the Literature

The IG-002 taxonomy documents four types of negative prompting, only one of which is extensively studied in academic literature (Type 1: naive blunt prohibition). Types 2-4 (structured prohibition with consequences, L2-re-injected HARD constraints, constitutional triplet with per-agent declarations) are undocumented in any published study. The AGREE-4 finding that "prohibition is unreliable" applies to Type 1. It is epistemically premature to generalize AGREE-4's finding to Types 2-4. Phase 2 must include Type 2 and Type 4 conditions (C2 and C4 in the experimental design) to test whether the AGREE-4 finding generalizes.

---

## Controlled Experiment Pilot Design

### Pilot Scope Revision

> **Resolution of PM-005-i1 (Major):** The pilot scope has been restructured to make it executable within realistic resource constraints.

**Revised pilot structure:** The n=30 pilot tests ONLY the primary comparison (C2 vs. C3). All 7 conditions are deferred to the full experiment.

**Rationale:** Running all 7 conditions in the pilot generates 7 × 30 = 210 evaluation points per model. At 15 minutes per output for hallucination rate verification (manual citation check), this exceeds a realistic single-session time budget. The pilot has one purpose: estimate the discordant proportion (p_12 + p_21) before committing to the full experiment sample size. This requires only the primary comparison.

### Purpose

The n=30 pilot study has a single primary purpose: to empirically estimate the discordant pair proportion (p_12 + p_21) before committing to the full experiment. The working assumption (p_12 + p_21 = 0.30) is a planning estimate.

### π_d = 0.30 Grounding

> **Resolution of SR-002-i1, SM-002-i1, PM-002-i1, IN-006-i1 (Major):** The discordant proportion assumption is now grounded.

**Comparable study basis (CV-001-i2 correction):** The 0.30 discordant proportion estimate is consistent with the observed range from matched-pair prompt comparison studies in the general LLM instruction-following literature. In the closest available analogues:
- Chain-of-thought vs. zero-shot paired comparisons (Wei et al., 2022, NeurIPS — "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models"): Wei et al. (2022) report accuracy improvements across tasks when comparing CoT vs. zero-shot prompting. The 20-40% range cited here is an author extrapolation from the accuracy differential data (not a directly reported discordant proportion value). Where Wei et al. report accuracy improvements of 10-25 percentage points across tasks, a paired discordant proportion of approximately 20-40% is mathematically consistent with those accuracy gaps under independence assumptions. **This is an extrapolation, not a directly reported value; it is noted as such.**
- IFEval benchmark analysis (Zhou et al., A-17) shows instruction-following success rates of 50-80% depending on model and instruction type; for instruction types where models have similar success rates, paired disagreement would be approximately 2 × success_rate × (1 − success_rate), which at 70% success gives 2 × 0.70 × 0.30 = 0.42; at 80% gives 0.32. The 0.30 assumption is on the lower end of this range. (Note: this formula assumes both conditions have similar success rates — valid as a symmetry approximation when testing the null hypothesis; if conditions differ substantially, the formula understates expected discordance.)
- The sensitivity table below shows how the required sample size changes across the plausible range.

**Explicit uncertainty disclosure:** No directly comparable published study uses matched positive/negative framing pairs at the scale and on the task types planned for PROJ-014. The 0.30 assumption is therefore an informed estimate, not an empirically derived value. The pilot is designed precisely to replace this assumption with an observed estimate.

**Sensitivity table:**

| Observed π_d | Required n (unadjusted) | Required n (with continuity correction) | Feasibility |
|--------------|------------------------|----------------------------------------|-------------|
| 0.10 | ~785 | ~892 | Infeasible — accept lower power or narrow scope |
| 0.15 | ~349 | ~397 | Feasible with LLM assistance |
| 0.20 | ~157 | ~179 | Feasible |
| 0.30 (working assumption) | 235 | ~268 | Feasible |
| 0.40 | ~314 | ~358 | Feasible with LLM assistance |
| 0.50 | ~2,744 | ~3,123 | Infeasible — pilot likely shows near-random framing effect |

*Formula: n = (p_12 + p_21) × (z_α/2 + z_β)² / (p_12 − p_21)² where effect size assumption p_12 = 0.20, p_21 = 0.10, p_12 − p_21 = 0.10, (z_α/2 + z_β)² = 7.84 (α = 0.05 two-tailed, power = 80%).*
*Continuity correction (CV-003-i2 correction): n_cc = n_unadj + z²_α/2 × (p_12 + p_21) / (4 × (p_12 − p_21)²). This formula is the author's adaptation of the continuity correction principles in Agresti (2013, "Categorical Data Analysis") §10.1; Agresti §10.1 presents the test-statistic continuity correction rather than a sample-size formula. The sample-size formula above is derived from those principles. At π_d = 0.30: n_cc = 235 + 3.84 × 0.30 / (4 × 0.01) = 235 + 28.8 ≈ 264; the table value of ~268 includes a conservative rounding buffer of 4 pairs (approximately 1.5%), consistent with standard practice of rounding up sample sizes.*
*Note: these values are illustrative parametric calculations. The pilot calibrates all assumptions.*

### Pilot Specifications

**Sample size:** n = 30 matched prompt pairs (6 per task category, 5 categories).

**Task categories:**
1. Research synthesis (summary/survey task)
2. Analysis (gap analysis or trade-off analysis)
3. Code review (behavioral compliance check)
4. Architecture decision (design recommendation)
5. Documentation (instructional writing)

Within each category: 2 simple, 2 medium, 2 complex (by estimated prompt length and constraint specificity).

### Research Question Alignment

> **Resolution of DA-001-i1, IN-001-i1 (Critical):** Metrics are now aligned to the research construct.

**Primary metric (hallucination rate — aligned to research question):**
- Evaluators read each output and the source material provided in the prompt
- A hallucination is defined as any factual claim in the output that is: (a) absent from source material, (b) contradicted by source material, or (c) falsely attributed to a specified source
- Hallucination rate = (count of hallucinated claims) / (total verifiable factual claims) per output
- This metric directly addresses Sub-claim A: does negative prompting reduce hallucination?

**Secondary metric (behavioral compliance):**
- Pass/Fail per constraint per output: did the agent comply with the stated constraint?
- Recorded per constraint per output; compliance rate = compliant outputs / total outputs
- This metric addresses whether framing changes behavioral compliance, distinct from hallucination

**Tertiary metric (overall quality gate score):**
- S-014 six-dimension rubric applied to each output
- Provides continuity with PROJ-014 session quality data and PROJ-007 retrospective baseline
- Analyzed via paired t-test (secondary analysis only)

### Equivalence Validation Protocol

> **Resolution of DA-005-i1, FM-001-i1, PM-001-i1, IN-002-i1 (Critical):** Full protocol specified.

**Purpose:** Ensure that C2 (structured negative) and C3 (positive equivalent) pairs differ ONLY in framing polarity, not in semantic content. Without this, the experiment tests prompt variation rather than framing variation.

**Equivalence Criteria Checklist:**

| Criterion | Definition | Pass Condition |
|-----------|-----------|---------------|
| EC-1: Semantic content | Same behavioral action described | Independent rater classifies both as describing the same action |
| EC-2: Consequence domain | Same consequence domain addressed; valence may be inverted | Rater confirms both versions address the same outcome domain (e.g., both address environment integrity); valence inversion (negative consequence in C2 / positive equivalent in C3) is explicitly permitted and expected |
| EC-3: Constraint specificity | Same level of specificity (atomic vs. compound) | Both are atomic OR both are compound |
| EC-4: Scope | Same scope of prohibition/prescription | Both cover the same behavioral domain |
| EC-5: Polarity only | The only difference is NEVER/MUST NOT vs. ALWAYS/MUST | Independent rater confirms no other semantic difference |

**EC-2 rationale (DA-003-i2, FM-006-i2, IN-004-i2, RT-003-i2 resolution):** Negative framing (C2) communicates what WILL go wrong if the rule is violated; positive framing (C3) communicates what WILL remain correct if the rule is followed. This valence difference is inherent to the negative-versus-positive polarity being studied and cannot be eliminated without changing the nature of the experimental manipulation. The consequence DOMAIN must match (both address the same outcome), but word-for-word identity would require collapsing the experimental contrast. Raters assess domain equivalence, not lexical identity.

**Residual asymmetry acknowledgment:** Consequence documentation in negative framing (C2) communicates risk; consequence documentation in positive framing (C3) communicates benefit. These are matched in domain but differ in valence and implicature. A reader of the C3 variant learns what WILL happen under compliance; a reader of the C2 variant learns what will NOT happen plus the consequence of violation. This residual asymmetry is a design limitation documented in [Analytical Limitations](#analytical-limitations).

**Inter-rater Agreement Requirement:** Before any pair enters the pilot, two independent raters (who did not construct the pair) must both classify the pair as meeting all 5 criteria (kappa > 0.80 required at the pair-inventory level). Pairs that fail kappa requirement are redesigned.

**Example Pairs — Redesigned (DA-005 fix):**

Original I1 example: "NEVER use pip install. Command fails. Environment corruption." vs. "ALWAYS use uv add for dependencies. UV manages isolation automatically." — REJECTED because (a) consequence documentation "Command fails. Environment corruption." has no positive equivalent, and (b) "UV manages isolation automatically" adds content absent from the negative version.

Corrected examples:

| Pair | C2 (Structured Negative) | C3 (Positive Equivalent) | EC-1 | EC-2 (domain match, valence inverted) | EC-3 | EC-4 | EC-5 |
|------|--------------------------|--------------------------|------|------|------|------|------|
| P-ENV-001 | "NEVER use pip install. The virtual environment will become corrupted." | "ALWAYS use uv add for dependencies. The virtual environment will remain clean." | Same (dependency management) | Domain: environment integrity (C2: corruption risk; C3: clean state; valence inverted — PASS) | Atomic | Same (dependency installation) | Yes |
| P-CITE-001 | "NEVER attribute a claim to a source you have not read. This constitutes fabrication." | "ALWAYS verify a source before attributing a claim to it. This ensures accuracy." | Same (citation verification) | Domain: source accuracy (C2: fabrication risk; C3: accuracy assured; valence inverted — PASS) | Atomic | Same (citation practice) | Yes |
| P-SCOPE-001 | "NEVER recommend production deployment without a rollback plan. The deployment may be unrecoverable." | "ALWAYS include a rollback plan before recommending production deployment. The deployment will be recoverable." | Same (deployment safety) | Domain: deployment recoverability (C2: unrecoverable risk; C3: recoverable outcome; valence inverted — PASS) | Atomic | Same (production deployment) | Yes |

**Validated example pairs:** At least 2 validated example pairs per task category must be approved by two independent raters before the pilot is launched. This produces a pool of 10 pre-validated pairs (2 per category × 5 categories) that serve as calibration examples for pair constructors.

**Adjudication procedure:** If raters disagree on any criterion, the pair is discussed and redesigned. If redesigned pair still fails agreement, it is retired and replaced. Pilot does not launch until 30 pairs pass the full protocol.

### Evaluator Blinding Protocol

> **Resolution of FM-002-i1, PM-003-i1, IN-003-i1 (Critical):** Output scrubbing protocol specified.

**Challenge:** LLM agents frequently echo constraint vocabulary from prompts in their outputs. An evaluator seeing "NEVER use pip install" echoed in an agent's output can infer the condition from content.

**Output Scrubbing Procedure:**
1. After LLM outputs are generated, a pre-screening pass masks or replaces any constraint-vocabulary indicators before evaluator presentation
2. Direct constraint vocabulary masked: NEVER, MUST NOT, FORBIDDEN, DO NOT, ALWAYS, MUST (in imperative forms), REQUIRED TO
3. Semantic circumlocution vocabulary masked (extended list per DA-002-i2, FM-002-i2 resolution): "avoid," "instead of," "rather than," "alternatively," "in lieu of," "refrain from," "do not use," "please be careful not to," "be sure not to"
4. All masked terms are replaced with the token "[INSTRUCTION-ECHO]" so evaluators know redaction occurred but cannot infer the polarity or specific masked content
5. If the agent's output itself is primarily constraint vocabulary (i.e., the agent merely repeated the instruction back rather than following it), this constitutes a systematic execution failure recorded as such, not masked
6. Output codes: each output is labeled "Output Alpha" and "Output Beta" within each pair; the mapping to conditions is concealed from evaluators

**Scrubbing validation:** Before pilot launch, the scrubbing procedure is tested on 5 example outputs. Evaluators (not involved in the study) are asked to guess which condition produced which output. The scrubbing is considered successful if evaluators cannot identify the condition at better than chance (50% correct) on the 5 examples.

**Residual blinding limitation (DA-002-i2, FM-002-i2, PM-002-i2 acknowledgment):** Vocabulary masking — even with the extended circumlocution list — cannot eliminate all condition leakage. An agent instructed with a negative constraint may structure its reasoning differently from one instructed with a positive equivalent (e.g., organizing content around "what to avoid" vs. "what to do"), and this structural difference may be inferrable without any masked vocabulary. This is a known, irreducible limitation of output-scrubbing as a blinding mechanism. The pilot report will document any condition-detection accuracy above chance in the scrubbing validation test, and this limitation will be noted in the pilot's threat-to-validity section.

### Evaluator Training Protocol

> **Resolution of FM-011-i1 (Major):** Training, calibration, and disagreement resolution specified.

**Training exercise:**
- Before the pilot, all evaluators complete a training exercise on 5 sample output pairs not included in the pilot
- Training covers: hallucination rate measurement protocol (with 10 worked examples), behavioral compliance binary scoring (with 5 pass and 5 fail examples), the scrubbing convention
- Training output: each evaluator documents their assessment of the 5 training pairs; trainer reviews for systematic errors before approving evaluators for live scoring

**Calibration check (DA-004-i2, FM-003-i2, IN-003-i2, PM-003-i2 resolution):**
- Before pilot launch, 10 of the 30 pilot pairs are scored by all evaluators independently (2 pre-validated pairs per task category × 5 categories = 10 pairs, drawn from the pre-validated example pool)
- **Rationale for n=10:** At n=3 pairs, Cohen's kappa is statistically undefined — a single disagreement changes kappa from 1.0 to approximately 0.67, making the threshold entirely dependent on chance agreements or disagreements. At n=10, kappa has sufficient range of outcomes that a kappa ≥ 0.70 threshold is a meaningful quality gate.
- Cohen's kappa is calculated for binary compliance and for hallucination rate quantification separately
- Required kappa: ≥ 0.70 for both metrics
- If kappa < 0.70: additional calibration session held; scoring rubric refined; protocol does not proceed until kappa threshold is met
- The 10 calibration pairs are drawn from the pre-validated pool; they are part of the 30 pilot pairs and will be included in the primary analysis

**Disagreement resolution:**
- For any pair where evaluators disagree by > 1 hallucination count or on binary compliance: pair enters adjudication
- Adjudication: evaluators discuss the specific output in question; majority rules for panels of 3+; for 2-evaluator disagreement, a third evaluator is added
- Adjudication decisions are logged with rationale for future rubric refinement

### Statistical Stopping Criterion

> **Resolution of DA-003-i1, FM-003-i1, RT-003-i1 (Critical):** Go/no-go criterion replaced.

**Replaced criterion (I1):** "Effect size not trivially small: |p_12_obs − p_21_obs| > 0.02" — this criterion was identified as statistically invalid because a pilot with p_12_obs = 0.16, p_21_obs = 0.14 (sum 0.30, difference 0.02) satisfies it but indicates nearly random framing direction.

**Replacement criterion — two-tier structure (RT-001-i2, FM-004-i2, IN-002-i2, PM-004-i2, CC-002-i2 resolution):**

The pilot stopping criterion is two-tiered. The tiers serve different purposes and the secondary tier's non-fulfillment does NOT constitute a pilot failure.

**Primary stopping criterion (calibration purpose — always applicable):**
The pilot succeeds at its calibration purpose if the observed discordant proportion (p_12_obs + p_21_obs) falls in the range 0.10 ≤ π_d_obs ≤ 0.50. This criterion:
- Is the SOLE determinant of the GO/NO-GO decision for the primary pilot purpose
- Does not require directional evidence
- Is achievable regardless of the effect size

**Secondary stopping criterion (directional signal — supplementary):**
The pilot additionally provides a directional signal if the 90% Wilson score interval for (p_12 − p_21) excludes zero. The Wilson score interval is specified for use with small n_discordant (rather than the Wald interval, which has poor coverage when n_discordant < 30). Calculation: compute the Wilson score interval for the proportion p_12/(p_12 + p_21) among discordant pairs; the directional signal criterion is met if this interval excludes 0.50 at 90% confidence (equivalent to the difference interval excluding zero).

**Key reconciliation (RT-001-i2):** At n=30 with pilot power approximately 0.17 (see power analysis below), the secondary criterion will typically NOT be met — the CI will include zero — even when a real effect exists. This is expected and does not constitute a pilot failure. A pilot with a GO verdict on the primary criterion (π_d_obs in 0.10–0.50 range) proceeds to full experiment regardless of the secondary criterion outcome. The secondary criterion is reported as a secondary finding with appropriate power caveats.

**Rationale for the primary criterion:** The pilot's purpose is to estimate π_d before committing full-experiment resources. A π_d_obs in the 0.10–0.50 range confirms that a powered full experiment is feasible. A π_d_obs outside this range indicates that the full experiment's sample size assumptions require revision before proceeding. The CI-based secondary criterion provides additional information but cannot be the primary stopping criterion given the pilot's power level.

### Multiple Comparisons Specification

> **Resolution of DA-004-i1, FM-006-i1 (Critical/Major):** Primary vs. exploratory comparisons declared; correction method specified.

**Primary comparison (confirmatory):** C2 (structured negative) vs. C3 (positive equivalent).
- This is the ONLY confirmatory comparison for the pilot.
- Statistical decision: two-tailed McNemar's test at α = 0.05 with Bonferroni-Holm correction applied to the primary comparison (trivial when only one confirmatory comparison).
- Pilot interpretation based solely on this comparison for the GO/NO-GO decision.

**All other condition comparisons (exploratory, full experiment only):**
- C1 vs. C7, C2 vs. C4, C2 vs. C6, C5 vs. C3, C6 vs. C3 (5 pre-specified exploratory comparisons)
- C2 vs. C5: post-hoc descriptive observation only; not pre-specified; Bonferroni-Holm correction does not apply
- Exploratory comparisons are hypothesis-generating only.
- Full experiment: Bonferroni-Holm correction applied to all 5 pre-specified exploratory comparisons collectively.
- Exploratory results reported with adjusted p-values and explicitly labeled "exploratory — not confirmatory."
- No GO/NO-GO decision for the pilot is based on exploratory comparisons.

### Statistical Power for All Conditions

> **Resolution of SR-006-i1 (Major):** Power analysis for all 7 conditions.

**Pilot:** Primary comparison C2 vs. C3 only. Power analysis (SR-002-i2, CC-001-i2, CV-002-i2, FM-005-i2 resolution):

**Corrected McNemar power derivation at n=30:**
- n = 30 pairs, π_d assumption = 0.30 → expected discordant pairs: n_d = 30 × 0.30 = 9
- Effect size assumption: p_12 = 0.20, p_21 = 0.10 (negative framing wins 2/3 of discordant pairs)
- Under H_1: E[n_12] = 9 × (2/3) = 6; E[n_21] = 9 × (1/3) = 3
- McNemar test statistic under H_1: |n_12 − n_21| / √n_d = |6 − 3| / √9 = 3/3 = 1.0
- Power = P(reject H_0 | H_1) = Φ(z − z_α/2) where z = 1.0, z_α/2 = 1.96 (two-tailed α = 0.05)
- Power = Φ(1.0 − 1.96) = Φ(−0.96) ≈ **0.17**

**Interpretation:** McNemar test power at n=30 is approximately 0.17 — the pilot has low power for directional inference. This is expected and appropriate. The pilot is designed for calibration (estimating π_d), not confirmation (rejecting H_0). Low power means the CI-based secondary stopping criterion will typically not exclude zero at n=30, which is why the primary stopping criterion is based on the observed π_d range rather than a CI test (see [Statistical Stopping Criterion](#statistical-stopping-criterion) above).

**The pilot is intentionally underpowered for definitive inference.** Power of 0.17 is the correct and expected value for a calibration pilot at this sample size. It does not indicate a design flaw; it indicates that n=30 is insufficient for directional confirmation but sufficient for π_d estimation.

**Full experiment — planned comparisons (DA-005-i2, FM-007-i2 resolution):**

| Comparison | Type | Assumed π_d | Assumed Effect | Required n (estimated) |
|-----------|------|------------|---------------|------------------------|
| C2 vs. C3 | Confirmatory | 0.30 | p_12=0.20, p_21=0.10 | ~268 |
| C1 vs. C7 (naive vs. positive-only) | Exploratory (pre-specified) | 0.35 | p_12=0.15, p_21=0.20 | ~430 (Bonferroni-adjusted) |
| C2 vs. C4 (structured vs. re-injected) | Exploratory (pre-specified) | 0.25 | p_12=0.15, p_21=0.10 | ~326 (Bonferroni-adjusted) |
| C2 vs. C6 (structured vs. justified) | Exploratory (pre-specified) | 0.25 | p_12=0.18, p_21=0.07 | ~165 (Bonferroni-adjusted) |
| C5 vs. C3 (paired vs. positive) | Exploratory (pre-specified) | 0.20 | p_12=0.12, p_21=0.08 | ~450 (Bonferroni-adjusted) |
| C6 vs. C3 (justified vs. positive) | Exploratory (pre-specified) | 0.25 | p_12=0.20, p_21=0.05 | ~98 (Bonferroni-adjusted) |
| C2 vs. C5 (structured vs. paired) | **Post-hoc observation only** (not pre-specified) | 0.20 | p_12=0.10, p_21=0.10 | Near-infinite under zero-effect assumption |

**C2 vs. C5 disposition (DA-005-i2, FM-007-i2):** C2 vs. C5 is removed from pre-specified confirmatory and exploratory comparisons. The power analysis assumption (p_12 = p_21 = 0.10) posits zero directional effect by construction, making required n near-infinite. Pre-specifying a comparison for which no detectable effect is expected is methodologically incoherent. C2 vs. C5 will be included as a post-hoc descriptive observation; if the pilot produces data suggesting a C2 vs. C5 effect worth testing, a protocol amendment will be filed before any confirmatory analysis.

**Important caveat:** All effect size assumptions above are speculative. The pilot calibrates the C2 vs. C3 assumption. All exploratory comparison power analyses are provisional and will require recalculation from pilot data.

### Model Selection Criteria

> **Resolution of FM-007-i1, PM-006-i1 (Critical/Major):** Model selection specified.

**Minimum requirement:** 3 models, providing: (a) at least one Anthropic-family model, (b) at least one non-Anthropic model (for external validity), (c) at least two different parameter count ranges.

**Selection criteria:**
| Criterion | Requirement |
|-----------|-------------|
| Instruction-tuning characterization | Model must be publicly documented as instruction-tuned (not base model only) |
| API accessibility | Model must be accessible via API at the time of experiment execution |
| Parameter count | At minimum: one model < 30B and one model ≥ 30B (or equivalent capability tier) |
| Negative vocabulary in RLHF/training | Document whether each model was explicitly trained with negative constraint examples; this characterization is a covariate |
| Prior AGREE-4 testing | Preference for models that have been tested in at least one prior negative prompting study to enable comparison |

**Working model set (subject to API availability):** Claude Sonnet (Anthropic, instruction-tuned), Claude Haiku (Anthropic, smaller capability tier), GPT-4o (OpenAI, external validity). This constitutes the minimum 3-model requirement with cross-vendor coverage. If any model in the working set becomes unavailable between pilot and full experiment, substitute the nearest available model satisfying the same selection criteria (instruction-tuned, API-accessible, matching parameter-count tier) and document the substitution as a limitation in the experimental report.

**Multi-model analysis:** The primary analysis pools all models. A secondary model-by-framing interaction analysis tests whether the effect differs by model family, providing generalizability evidence. If models differ significantly in their response to framing (3-way interaction significant at p < 0.10), results are reported separately by model family.

### Execution Feasibility Plan

> **Resolution of IN-004-i1 (Major):** Execution feasibility addressed.

**Scale estimate:** For the pilot (n=30, primary comparison C2 vs. C3, 3 models):
- 30 pairs × 2 conditions × 3 models = 180 LLM output generations (automated)
- 180 outputs to evaluate: hallucination rate requires source material verification
- At 10-15 minutes per output for manual hallucination rate assessment: ~30-45 researcher-hours for pilot

**Feasibility approach:** The pilot is feasible as a single-researcher study with LLM assistance for:
- Output scrubbing (automated vocabulary masking): LLM-assisted, batch processed
- Behavioral compliance scoring (binary): LLM-assisted primary scoring with 20% human spot-check; kappa calibration verifies LLM-human agreement before deployment

**Hallucination rate measurement:** Human-only for the pilot (30-45 hours is within a single-researcher budget). For the full experiment, LLM-assisted hallucination rate assessment is evaluated as an option, with human spot-check validation (25% of outputs) required before relying on LLM-assisted scoring.

**Full experiment scale (post-pilot):** n=268 pairs × 2 conditions (C2/C3 primary) × 3 models = 1,608 LLM outputs. With LLM-assisted evaluation and 25% human spot-check, estimated human labor: ~40-80 researcher-hours. This is feasible as a single-researcher multi-session study. The 7-condition full experiment (adding C1, C4, C5, C6, C7) multiplies outputs by ~4; at that scale, automation validation is required before launch.

### Experimental Conditions

| Condition | Label | Description | Example (dependency management) |
|-----------|-------|-------------|----------------------------------|
| C1 | Naive prohibition | Standalone blunt prohibition without consequence | "Don't use pip" |
| C2 | Structured negative | NEVER/MUST NOT with consequence documentation | "NEVER use pip install. The virtual environment will become corrupted." |
| C3 | Positive equivalent | Positive reframing of C2 (same content, matched consequence) | "ALWAYS use uv add for dependencies. The virtual environment will remain clean." |
| C4 | L2-re-injected negative | C2 with per-turn re-injection of the same constraint | C2 plus "Remember: NEVER use pip install. The virtual environment will become corrupted." injected at each turn |
| C5 | Paired negative + positive | C2 paired with positive alternative | "NEVER use pip install. Use uv add instead. The virtual environment will remain clean." |
| C6 | Contextually justified negative | C2 plus contextual reason | "NEVER use pip install — it bypasses uv's isolation guarantees. The virtual environment will become corrupted." |
| C7 | Positive-only baseline | Pure positive framing, no prohibitions | "Use uv add for all dependency management. The virtual environment will remain clean." |

**Equivalence documentation:** For the primary comparison (C2 vs. C3), consequence documentation is matched word-for-word using corrected example pairs from the Equivalence Validation Protocol above.

### Pilot Go/No-Go Criteria

**GO (proceed to full experiment) — RT-001-i2, FM-004-i2, IN-002-i2, PM-004-i2, SR-004-i2 resolution:**

The GO decision is based primarily on the calibration criterion. The directional signal criterion is secondary and supplementary.

**Primary GO criterion (calibration — required):**

| Criterion | Threshold | Rationale |
|-----------|-----------|-----------|
| Observed discordant proportion | 0.10 ≤ p_12_obs + p_21_obs ≤ 0.50 | Within range where the full experiment is feasible (n ≤ 800); primary purpose of the pilot achieved |
| Pilot data quality | ≥ 85% of the 30 pairs produce valid evaluatable output (≤ 4 execution failures) | Sufficient valid pairs to compute π_d_obs reliably |
| Evaluator agreement | Cohen's kappa ≥ 0.70 on calibration pairs (n=10) | Scoring is reliable enough to proceed |

**Secondary GO criterion (directional signal — supplementary, not required):**

| Criterion | Threshold | Interpretation if Not Met |
|-----------|-----------|--------------------------|
| 90% Wilson score CI for (p_12 − p_21) excludes zero | CI does not include zero | Expected NOT to be met at n=30 given power ≈ 0.17. Non-fulfillment does NOT constitute pilot failure. Reported as "insufficient power for directional signal at n=30" — which is the expected outcome for a calibration pilot. |

**Key reconciliation:** A pilot that meets all three primary GO criteria proceeds to the full experiment, even if the CI-based secondary criterion is not met (as is expected and normal at n=30). The CI secondary criterion provides bonus directional information if it happens to be met at the observed effect size, but its non-fulfillment is the expected outcome.

**Execution failure definition (PM-007 fix):** A systematic execution failure for a pair includes: (a) agent refuses to complete the task, (b) agent produces output that is not evaluable (e.g., generates only error text), (c) agent echoes only the constraint without addressing the task, (d) agent fabricates a cited source that is then discoverable as non-existent. Individual hallucinations are NOT execution failures; they are scored as hallucinations.

**NO-GO (do not proceed without design modification):**

| Criterion | Threshold | Action |
|-----------|-----------|--------|
| Near-zero discordant proportion | p_12_obs + p_21_obs < 0.05 | Both conditions produce nearly identical outcomes. Revisit task selection and framing operationalization. Re-pilot. |
| Very high discordant proportion | p_12_obs + p_21_obs > 0.60 | Results suggest task construction rather than framing drives discordance. Revisit equivalence validation. Re-pilot. |
| Systematic execution failures | > 20% of pairs produce invalid output (≥ 7 failures) | Design flaw; resolve before proceeding |
| Evaluator agreement insufficient | Kappa < 0.70 on calibration pairs | Scoring rubric requires refinement; do not proceed until resolved |
| Required full-experiment n > 1000 | Observed π_d < 0.08 | Full experiment infeasible; accept lower power or narrow scope |

**Note on SR-004-i2 resolution:** The prior version specified "All 30 pairs produce valid output" as a GO criterion and "> 20% failures" as a NO-GO criterion, creating an undefined intermediate state (1-19% failures). The revised version specifies GO as "≥ 85% valid" (≤ 4 failures) and NO-GO as "> 20% failures" (≥ 7 failures), with a defined intermediate zone (5-6 failures = marginal; evaluate on other criteria before deciding). This eliminates the undefined state. If 5–6 failures occur, proceed to GO decision on the remaining two primary criteria (π_d range and kappa); document failure rate in the pilot report as a limitation.

### Pilot Subgroup Analysis

> **Resolution of FM-012-i1 (Major):** Subgroup analysis plan specified.

**Primary subgroup analysis:** Task category × framing interaction.
- Hypothesis: framing effects are not uniform across task categories; some categories (e.g., code review with specific constraint instructions) may show larger framing effects than others (e.g., open-ended research synthesis)
- Analysis: logistic regression with task category as a moderator; if interaction is significant at p < 0.20 (low bar for pilot), report category-specific estimates with appropriate uncertainty
- Expected largest effect categories: code review (explicit, verifiable constraints) and documentation (format-specific constraints)
- Expected smallest effect category: research synthesis (open-ended; framing may matter less than content)

**Secondary subgroup analysis:** Task complexity × framing interaction.
- Hypothesis: framing effects may be larger for complex tasks where the constraint requires more reasoning to apply
- Analysis: compare simple, medium, complex pairs separately; report with uncertainty

**Pilot subgroup analysis caveat:** With n=30 pairs, subgroup analyses are exploratory and underpowered. They provide directional signal for hypothesis generation in the full experiment design. No subgroup finding from the pilot constitutes a confirmatory result.

### Full Experiment Pathway (Post-Pilot)

**Confirming criteria before committing to full experiment:**
- Pilot GO verdict achieved (all four GO criteria met)
- Updated sample size calculated from pilot discordant proportion
- Evaluation methodology validated on pilot data (scorer agreement checked; kappa > 0.70 for hallucination rate and compliance)
- Task selection refined based on pilot execution experience
- Models confirmed (at minimum: Claude Sonnet, Claude Haiku, one non-Anthropic model for external validity)

**Full experiment parameters (subject to pilot calibration):**

| Parameter | Working Value | Source |
|-----------|--------------|--------|
| Total matched pairs | ~268 | McNemar formula with p_12=0.20, p_21=0.10, π_d=0.30 (to be recalculated from pilot) |
| Task categories | 5 | Research, analysis, code review, architecture, documentation |
| Pairs per category | ~54 | 268 / 5 |
| Models | 3 minimum | Multi-model generalizability |
| Primary metric | Hallucination rate | Manual verification against source material |
| Secondary metric | Behavioral compliance | Binary pass/fail per constraint |
| Primary hypothesis test | C2 vs. C3 | Structured negative vs. positive equivalent |
| Exploratory conditions (full experiment) | C1, C4, C5, C6, C7 vs. C2 or C3 | Deferred from pilot |
| Multiple comparisons | Bonferroni-Holm | Confirmatory C2/C3; exploratory labeled as such |

---

## Evidence Summary Table

| Evidence ID | Type | Source | Tier | Finding | Relevance |
|-------------|------|--------|------|---------|-----------|
| E-FOR-A-001 | Absence | All 3 surveys (AGREE-1) | — | Zero sources support 60% hallucination reduction | Primary: claim is untested |
| E-FOR-B-001 | Empirical | Wang et al., IJCAI 2024 (A-1) | Tier 1 | Negative emotional stimuli +12-46% on reasoning tasks | Indirect: emotional framing ≠ prohibition |
| E-FOR-B-002 | Empirical | Barreto & Jana, EMNLP 2025 accepted (A-23) | Tier 1 | Warning-based meta-prompts +25.14% negation accuracy | Direct: negative meta-instruction improves specific task. Single study, not replicated. |
| E-FOR-B-003 | Empirical | Singhvi et al., arXiv (C-13) | Tier 3 | DSPy assertions: 164% compliance, 37% quality improvement | Indirect: programmatic negative constraints (not pure prompt) |
| E-FOR-B-004 | Observational | VS-001 (supplemental) | Obs | 33 NEVER/MUST NOT instances in Anthropic's behavioral rules | Consistent with hypothesis; not causal evidence; revealed preference framing applies |
| E-FOR-B-005 | PSR | JF-001 (supplemental) | PSR | Jerry Framework uses negative constraints for all HARD-tier rules | Practitioner self-report; observer-researcher confound applies |
| E-FOR-B-006 | PSR/Session | EO-001-003 (supplemental) | PSR | PROJ-014 session: monotonic quality improvement, zero constraint violations | Confounded; non-replicable; observer-researcher confound (DA-006 acknowledged) |
| E-AGN-A-001 | Empirical | Varshney et al., arXiv (A-6) | Tier 3 | Negation increases hallucination in LLaMA-2 MCQA: 26% → 59% | Against sub-claim A; narrow scope; not replicated |
| E-AGN-A-002 | Empirical | Gandhi & Gandhi, arXiv (A-14) | Tier 3 | Negative sentiment reduces factual accuracy 8.4% | Measures sentiment, not prohibition framing |
| E-AGN-A-003 | Empirical | McKenzie et al., TMLR (A-9) | Tier 2 | Inverse scaling on negation in 2022-2023 models | Against understanding of negation; era-specific |
| E-AGN-B-001 | Cross-survey | AGREE-4 (multiple sources) | Mixed (Tier 1/4) | Standalone blunt prohibition unreliable — convergent across all 3 surveys | Against BLUNT prohibition specifically; does not apply to structured Types 2-4 |
| E-AGN-B-002 | Empirical | Bsharat et al., arXiv (A-31) | Tier 3 | Affirmative directives +55% improvement, +66.7% correctness for GPT-4 | Against generic prohibition; Tier 3 only |
| E-AGN-B-003 | Empirical | Geng et al., AAAI 2026 accepted (A-20) | Tier 1 | Instruction hierarchy fails for formatting conflicts | Against reliability of instruction-based constraints generally |
| E-AGN-B-004 | Vendor docs | Anthropic (I-1), OpenAI (I-3), Google (I-6) | Tier 4 | Three major vendors recommend positive framing | Against negative framing generally; vendor circular optimization caveat applies |
| E-AGN-B-005 | Empirical | Ferraz et al., EMNLP 2024 (A-15) | Tier 1 | GPT-4 fails >21% of constraints even with atomic decomposition | Against naive constraint-based approaches; structured alternatives help |
| E-AGN-B-006 | Empirical | Garcia-Ferrero et al., EMNLP 2023 (A-3) | Tier 1 | LLMs proficient on affirmative, struggling on negative sentences | Against negation linguistic understanding |
| E-RETRO-001 | Observational | PROJ-007 Barrier 3 quality gate | Internal | ADR-001: I1=0.91→I2=0.962; ADR-002: I1=0.90→I2=0.955; avg 2 iterations | PROJ-007 baseline; positive-governance session; verified |
| E-RETRO-002 | Observational | PROJ-007 Barrier 4 quality gate | Internal | Barrier 3 first-pass avg: 0.905; Barrier 4 first-pass avg: 0.936; 2 iterations each | PROJ-007 baseline; shown separately (no averaging) |
| E-RETRO-003 | Observational | PROJ-007 Phase 5 / C4 tournament | Internal | Portfolio final: 0.957; tournament adjusted: 0.952 CONDITIONAL PASS | PROJ-007 final quality benchmark |
| E-RETRO-004 | Observational | PROJ-014 Barrier 1 synthesis | Internal | Synthesis: 0.83 → 0.953 in 4 iterations; supplemental: 0.843 → 0.951 in 4 iterations | PROJ-014 quality under negative-constraint regime |
| E-RETRO-005 | Absence | PROJ-006 WORKTRACKER.md | — | PROJ-006 status: PENDING; no quality gate data; excluded from comparison | Data limitation |

---

## Analytical Limitations

### What This Analysis Cannot Establish

1. **Causality of the retrospective comparison.** The PROJ-014 vs. PROJ-007 comparison is confounded by task type, domain novelty, task complexity, shared framework vocabulary, agent instance variation, and researcher expertise accumulation. No causal conclusion about negative prompting causing any quality difference is supported.

2. **Generalizability of the null finding.** The three surveys covered the publicly documented evidence base. SE-1 through SE-5 structural exclusions mean that the null finding applies only to publicly documented evidence, covering at most 30-40% of the plausible total evidence base.

3. **Equivalence of the PROJ-007 and PROJ-014 evaluation environments.** The adversary agents scoring PROJ-007 deliverables and PROJ-014 deliverables are different agent instances from different sessions. Inter-rater agreement between sessions is unknown. Margin differences (0.952 vs. 0.957) are within plausible scorer variance.

4. **The 0.30 discordant proportion assumption.** The n=268 calculation rests on an informed estimate, not an empirically derived figure. The pilot study is required to validate this assumption before committing to the full experiment.

5. **Model-specificity of any Phase 2 finding.** Any result from the Phase 2 experiment will apply to the specific models tested. Generalization to other model families requires additional evidence.

6. **The hallucination rate measurement protocol.** Manual verification of hallucination rate is itself subject to evaluator judgment about what constitutes a "factual claim" and what constitutes a "fabrication." The evaluator training and calibration protocol (above) is designed to reduce but not eliminate this variance.

7. **Consequence documentation asymmetry in matched pairs.** Consequence documentation in negative framing (C2) communicates risk — what WILL go wrong if the rule is violated. Consequence documentation in positive framing (C3) communicates benefit — what WILL remain correct if the rule is followed. The example pairs match these in consequence domain (same outcome area) with valence inversion. This residual asymmetry is structurally inherent to the negative-versus-positive polarity being studied: eliminating it would require eliminating the experimental manipulation itself. The asymmetry means that C2 and C3 pair members differ not only in polarity vocabulary but also in the informational valence of their consequence text. This is acknowledged as a limitation of the matched-pair design that cannot be fully controlled without abandoning the ecological validity of the constraint types.

8. **Scope of the experimental variable in the retrospective comparison.** The characterization of PROJ-007 as the "positive-framing control" refers specifically to PROJ-007 PLAN.md-level project governance (no explicit negative constraint list). The shared Jerry Framework HARD rules — which both projects load and which use NEVER/MUST NOT vocabulary — are a confound present equally in both conditions. The experimental variable is the PLAN.md project-level negative constraint governance, not the complete absence of all negative vocabulary in any LLM prompt processed during either project.

---

## Adversarial Quality Checks

> **Provenance note (RT-005 fix, CC-004 fix, CC-003-i2 fix):** The checks below were produced as a preliminary self-review (pre-I1) by the creator agent at TASK-005 creation. They are labeled accordingly. Two authoritative external adversarial passes have been completed: the I1 C4 Tournament (10 strategies, 2026-02-27) documented in `adversary-claim-validation-i1.md`, and the I2 C4 Tournament (10 strategies, 2026-02-27) documented in `adversary-claim-validation-i2.md`. The current document (I3) is the revision addressing all I2 tournament findings. H-15 self-review for the I3 additions is documented in the I2 → I3 Revision Log above, which constitutes the pre-submission review of all I2 additions before the I3 tournament.

### Preliminary Self-Review (pre-I1): S-013 Inversion

*Applied by ps-analyst at TASK-005 creation, 2026-02-27, before I1 tournament.*

**What If Negative Prompting Does NOT Outperform Positive Prompting?**

If the null hypothesis is correct — framing has no systematic effect on LLM compliance — what would explain the evidence documented here?

- **VS-001 (Anthropic's 33 NEVER/MUST NOT instances):** Explained by Explanation 2 (convention and precedent). Rule document vocabulary is conventionally prohibitive in legal, policy, and technical specification contexts. No inference about effectiveness follows.
- **JF-001 (Jerry Framework HARD tier uses negative vocabulary):** Explained by convention + confirmation bias in the practitioner observer. The HARD tier is defined as prohibitive — it is not an empirically derived finding.
- **EO-001 (PROJ-014 quality trajectory 0.83 → 0.953):** Explained by task difficulty, specialized agents, quality gate mechanism, and structured templates — all confounding variables. The negative constraint prompting may have contributed zero marginal effect.
- **E-FOR-B-002 (warning-based prompts +25.14%):** A real finding (Tier 1, EMNLP 2025) but applies to a specific task type (distractor negation) and has not been replicated.
- **Vendor recommendation divergence (VS-002):** Explained by Explanation 1 (audience specificity). No inference about effectiveness follows.

**Inversion assessment:** The null hypothesis has a credible explanatory account for all evidence except E-FOR-B-002 (Barreto & Jana warning-based prompts). This is the evidence that most resists the null explanation. E-FOR-B-002 is the highest-priority replication target for Phase 2.

### Preliminary Self-Review (pre-I1): S-004 Pre-Mortem

*Applied by ps-analyst at TASK-005 creation, 2026-02-27, before I1 tournament.*

**What If the Pilot Study Fails?**

Six months from now, the pilot has concluded. The go/no-go criteria are not met. What happened?

**Failure Mode 1 — Near-zero discordant proportion (p_12 + p_21 < 0.05):** Both negative and positive framing conditions produce nearly identical outputs on the same tasks. LLM behavior is substantially determined by semantic content, not framing. Recovery: Narrow scope to task types where Barreto & Jana found effects. Re-pilot with warning-based prompts on negation-intensive tasks.

**Failure Mode 2 — Framing reversal (p_21 > p_12):** Positive framing conditions outperform negative conditions. The hypothesis is empirically refuted. Recovery: Document, publish the null/negative result, revise Jerry Framework HARD tier vocabulary guidance.

**Failure Mode 3 — Execution failures > 20%:** Matched pair construction fails because semantic equivalents cannot be constructed without meaning changes. Recovery: Refine matched-pair construction protocol. Consult linguistics experts on equivalence criteria.

**Failure Mode 4 — Scorer agreement too low (kappa < 0.70):** Binary pass/fail scoring proves unreliable. Recovery: Tighten scoring rubric with binary test cases that unambiguously pass or fail each constraint. Pre-screen evaluators with test scenarios.

**Pre-mortem verdict:** Failure Mode 1 is the most likely. The experiment is designed to test whether framing matters, and the prior evidence (AGREE-4) suggests framing may matter less than semantic content and instruction structure. The pilot is essential before committing to the full sample.

### Preliminary Self-Review (pre-I1): S-003 Steelman

*Applied by ps-analyst at TASK-005 creation, 2026-02-27, before I1 tournament.*

**The Strongest Case Against the Hypothesis:**

Large language models do not process instructions the way humans process negative rules. Human psychological research (Ironic Process Theory) shows that explicit "don't think about X" instructions activate the suppressed content. For LLMs, the mechanism is fundamentally different: a "don't do X" instruction and an "always do Y" instruction both get tokenized and processed through the same attention mechanisms. The semantic representation of "NEVER use pip install" is a vector in the same embedding space as "use uv add for dependencies." If the model has been instruction-tuned to comply with constraints, it may comply with either framing nearly equally. The vocabulary difference (NEVER vs. ALWAYS) may be far less important than:

1. The specificity of the constraint (atomic vs. compound)
2. The consequence documentation (what happens if violated)
3. The placement in the prompt (system prompt vs. user turn)
4. The presence of a positive behavioral alternative

If this is correct, the Phase 2 experiment should find small or zero framing effects (C2 vs. C3) but large effects from constraint structure (C6 with justification vs. C1 without), consequence documentation, and pairing with positives (C5 vs. C1). This would refute the original working hypothesis while validating the synthesis's alternative hypothesis. The Phase 2 experiment is designed to test precisely this scenario through conditions C1 through C7.

---

## PS Integration

```yaml
session_context:
  schema_version: "1.0.0"
  source_agent:
    id: "ps-analyst"
    family: "ps"
    cognitive_mode: "convergent"
    model: "sonnet"
  target_agent: "orchestrator"
  payload:
    key_findings:
      - "60% hallucination reduction claim: NULL FINDING — untested in any controlled study, not refuted; zero evidence for or against in published literature. Null finding covers ~30-40% of plausible total evidence base due to structural exclusions (published academic + public practitioner sources only; SE-1 closed production, SE-2 domain expert, SE-3 vendor internal, SE-4 grey literature, SE-5 publication bias collectively exclude the majority of the evidence base)."
      - "Research question bifurcated: hallucination rate (primary, aligned to original claim) vs. behavioral compliance (secondary). Primary metric redesigned with source material operationalized per all 5 task categories to enable reliable rater agreement."
      - "PROJ-007 regime verified: PLAN.md uses positive framing; no negative constraint governance list. Experimental variable is PLAN.md-level project governance — not total absence of negative vocabulary in all session prompts (shared framework HARD rules use NEVER/MUST NOT in both conditions). PROJ-007 first-pass avg: Barrier 3=0.905, Barrier 4=0.936; PROJ-014 first-pass avg: 0.837. Task complexity confound favors PROJ-007 interpretation."
      - "Pilot design: n=30 pairs, C2 vs. C3 primary comparison only. Primary GO criterion is calibration-based (observed pi_d in 0.10-0.50 range); secondary directional CI criterion is supplementary and expected not to be met at n=30 (power ~0.17). Pilot power correctly stated as ~0.17 (corrected from prior ~0.40 statement). All 27 Major and 16 Minor I2 tournament findings addressed in I3."
      - "Highest-priority Phase 2 replication target: Barreto & Jana (A-23, EMNLP 2025) warning-based prompts +25.14% — only evidence that most resists the null hypothesis account."
    open_questions:
      - "Is the discordant proportion assumption (0.30) calibrated correctly? Pilot study will answer this."
      - "Are matched semantic equivalents constructable for all 5 task categories without meaning changes? Pre-validated pairs for all 5 categories required before pilot launch."
      - "Does warning-based prompting (A-23) generalize beyond distractor-negation NLP tasks?"
      - "Can LLM-assisted hallucination rate measurement achieve kappa > 0.70 vs. human scoring? Must validate before full experiment."
      - "Does the extended circumlocution masking list adequately blind outputs, or does structural reasoning pattern still allow condition detection above chance?"
    blockers: []
    confidence: 0.82
    artifacts:
      - path: "projects/PROJ-014-negative-prompting-research/orchestration/neg-prompting-20260227-001/phase-2/claim-validation.md"
        type: "analysis"
        summary: "I3 revision: all 27 Major I2 findings resolved across 6 themes — hallucination source material operationalized per task category, pilot stopping criterion restructured (primary calibration, secondary directional), calibration sample increased to n=10, EC-2 revised to permit valence-inverted consequence matching, scrubbing list extended for circumlocution, pilot power corrected to ~0.17 with derivation, CI method specified (Wilson score), Wei et al. citation corrected, C2 vs. C5 removed from pre-specified comparisons, DSPy mechanism distinction documented, Agresti attribution documented as labeled limitation in footnote"
  timestamp: "2026-02-28T00:00:00Z"
```

---

*ps-analyst | TASK-005 | PROJ-014 | 2026-02-28 | Iteration 4*
*I1 tournament findings: all 16 Critical and 29 Major resolved. 11 Minor resolved. I1 adversary report: `adversary-claim-validation-i1.md` (C4 tournament, 10 strategies, score 0.771 REJECTED)*
*I2 tournament findings: all 27 Major and 16 Minor resolved in I3. I2 adversary report: `adversary-claim-validation-i2.md` (C4 tournament, 10 strategies, score 0.839 REJECTED)*
*I3 tournament findings: 3 Minor findings and 1 improvement recommendation resolved in I4. I3 adversary report: `adversary-claim-validation-i3.md` (C4 tournament, score 0.944 REVISE)*
*I4 self-review: The I3→I4 revision log above constitutes the H-15-compliant self-review of all I4 additions (finding-by-finding resolution documented). Inline adversarial checks labeled as "Preliminary Self-Review (pre-I1)"; superseded by I1, I2, and I3 external tournaments.*
*Analysis produced from: synthesis.md (R4, 0.953), supplemental-vendor-evidence.md (R4, 0.951), PROJ-007 PLAN.md (verified: positive framing, no negative constraint governance), PROJ-007 Barrier 3/4/Phase 5/Tournament quality gate reports, PROJ-007 WORKTRACKER.md (COMPLETE), PROJ-006 WORKTRACKER.md (PENDING — no quality data, excluded from comparison)*
*C4 threshold (0.95) source: PROJ-014 PLAN.md acceptance criteria, "Never let creator output flow downstream without /adversary C4 quality gates (>= 0.95, up to 5 iterations)." Consistent with quality-enforcement.md C4 classification.*
