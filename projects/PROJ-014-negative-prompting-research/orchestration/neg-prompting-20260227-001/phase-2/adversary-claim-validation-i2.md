# C4 Adversary Tournament Execution Report: Iteration 2
## Claim Validation Analysis — "Negative Prompting Reduces Hallucination by 60%"

> adv-executor | C4 Tournament Iteration 2 | PROJ-014 | 2026-02-27
> Deliverable: phase-2/claim-validation.md (TASK-005, Revision 2)
> Strategies executed: 10 of 10 (S-010, S-003, S-002, S-004, S-001, S-007, S-011, S-012, S-013, S-014)
> Quality Gate: >= 0.95 (C4)
> Prior iteration: I1 score 0.771 REJECTED — 16 Critical, 29 Major, 11 Minor
> Leniency bias counteraction: Applied throughout. Scores not inflated.

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Execution Context](#execution-context) | Strategy order, H-16 compliance, I2 focus |
| [S-010: Self-Refine](#s-010-self-refine) | Self-review of I2 revision quality |
| [S-003: Steelman](#s-003-steelman) | Charitable reconstruction of the revised argument |
| [S-002: Devil's Advocate](#s-002-devils-advocate) | Counter-argument against the revised design |
| [S-004: Pre-Mortem](#s-004-pre-mortem) | Failure modes in the revised experimental design |
| [S-001: Red Team](#s-001-red-team) | Adversarial attack on the revision |
| [S-007: Constitutional AI](#s-007-constitutional-ai) | Constitutional compliance of the revision |
| [S-011: Chain-of-Verification](#s-011-chain-of-verification) | Factual claim verification in the revision |
| [S-012: FMEA](#s-012-fmea) | Component failure mode analysis of revised design |
| [S-013: Inversion](#s-013-inversion) | Assumption stress-test of the revision |
| [S-014: LLM-as-Judge](#s-014-llm-as-judge) | Final composite score |
| [Consolidated Findings](#consolidated-findings) | All I2 findings cross-referenced by severity |
| [Tournament Summary](#tournament-summary) | Verdict and disposition |

---

## Execution Context

- **Strategy:** C4 Tournament (all 10 selected strategies)
- **Deliverable:** `projects/PROJ-014-negative-prompting-research/orchestration/neg-prompting-20260227-001/phase-2/claim-validation.md`
- **Criticality:** C4 (Critical — research claim validation with experimental design implications)
- **Executed:** 2026-02-27
- **Quality Gate:** >= 0.95 weighted composite (C4)
- **H-16 Compliance:** S-010 (self-review, no H-16 prerequisite) → S-003 (Steelman) → critique strategies (S-002, S-004, S-001, S-007, S-011, S-012, S-013) → S-014 (scoring)
- **Leniency Bias Counteraction:** Applied throughout. No rounding toward threshold. No excusing gaps via "good faith effort."

**I2 Focus Areas:**
1. Verify all 16 I1 Critical findings genuinely resolved (not papered over)
2. Check for new issues introduced by the R2 revision
3. Verify internal consistency of the revised experimental design
4. Verify evidence tier assignments remain accurate after revision
5. Verify the construct validity fix (hallucination rate as primary metric) is methodologically sound

**Prior I1 score:** 0.771 REJECTED. Revision addressed: 16 Critical + 29 Major + 11 Minor = 56 findings total.

---

## S-010: Self-Refine

**Finding Prefix:** SR | **Execution ID:** i2-20260227

### Objectivity Assessment

External reviewer; no authorship investment in the revision. Proceeding with systematic critique across all 6 quality dimensions, with particular attention to whether I1 resolution claims are genuine or cosmetic.

### Critical Resolution Audit: 16 I1 Criticals

Before assessing dimensions, audit the 16 Critical findings to determine genuine vs. cosmetic resolution:

| I1 Finding | Claimed Resolution | Resolution Quality |
|------------|-------------------|--------------------|
| DA-001-i1 (primary metric not hallucination) | Research question bifurcated; hallucination rate elevated to primary | GENUINE — hallucination rate protocol fully specified with operational definition |
| DA-005-i1 (equivalents violate equivalence) | Example pair redesigned; Equivalence Validation Protocol added | GENUINE — 3 corrected example pairs with checklist; inter-rater requirement added |
| FM-001-i1 (equivalence protocol absent) | Equivalence Validation Protocol with 5-criterion checklist | GENUINE — complete protocol with adjudication procedure |
| FM-002-i1 (blinding failure: vocabulary echo) | Output scrubbing protocol with token masking | GENUINE — specific masking list, "[INSTRUCTION-ECHO]" token, 5-example validation test |
| FM-003-i1 (go/no-go criterion invalid) | Replaced with 90% CI excluding zero | GENUINE — correct directional stopping criterion |
| FM-004-i1 (no generalizability bridge) | Evidence-to-pilot generalizability bridge table added | GENUINE — 9 evidence items mapped to pilot conditions with expected direction |
| FM-005-i1 (PROJ-007 data conflated) | Barrier 3 and Barrier 4 shown separately | GENUINE — comparison table restructured; no averaged "0.92" figure |
| FM-006-i1 (multiple comparisons missing) | Bonferroni-Holm declared; primary vs. exploratory split | GENUINE — confirmatory vs. exploratory explicitly declared |
| FM-007-i1 (model selection absent) | Model selection criteria table added | GENUINE — instruction-tuning, API accessibility, parameter count, RLHF characterization |
| IN-001-i1 (S-014 not valid proxy for hallucination) | Hallucination rate elevated to primary metric | GENUINE — same resolution as DA-001 |
| IN-002-i1 (equivalence constructability unvalidated) | Protocol added; pairs redesigned and pre-validated | GENUINE — though constructability still requires empirical validation before pilot launch |
| IN-003-i1 (blinding achievability unvalidated) | Scrubbing protocol; 5-example validation test | GENUINE — residual blinding risk acknowledged as limitation |
| PM-001-i1 (matched-pair protocol insufficiently specified) | Full Equivalence Validation Protocol | GENUINE |
| PM-003-i1 (blinding doesn't address vocabulary echoing) | Output scrubbing protocol | GENUINE |
| RT-001-i1 (null finding not protected) | WARNING callout added at document top and in L0 | GENUINE — prominent callout with explicit counter-extraction language |
| RT-003-i1 (go/no-go exploitable) | CI-based directional stopping criterion | GENUINE |

**Critical resolution verdict: 16/16 genuinely resolved.** No cosmetic-only resolutions detected.

### Dimension Assessment

| ID | Finding | Severity | Evidence | Affected Dimension |
|----|---------|----------|----------|--------------------|
| SR-001-i2 | The sensitivity table for π_d has an arithmetic error at the π_d = 0.30 row: the table states "Required n (unadjusted) = 235" but the footnote formula yields n = 0.30 × 7.84 / (0.10)² = 0.30 × 784 = 235.2. This is consistent. However, the same table states "Required n (with continuity correction) = ~268" but the Pilot Specifications section directly says "Total matched pairs = ~268" with source "McNemar formula with p_12=0.20, p_21=0.10, π_d=0.30." The continuity correction adds n_cc_add = (1.96)² × 0.30 / (4 × 0.01) = 3.84 × 0.30 / 0.04 = 3.84 × 7.5 = 28.8, giving ~264, not 268. The discrepancy (268 vs. ~264) is minor but the rounding is undocumented. | Minor | "Required n (with continuity correction) = ~268" in sensitivity table vs. arithmetic from footnote formula | Internal Consistency |
| SR-002-i2 | The pilot power calculation states "McNemar test power at n=30: approximately 0.40 (low)" but provides no derivation or citation for this power estimate. For McNemar with n_discordant ≈ 9 (30 × 0.30), p_12 = 0.20, p_21 = 0.10, the power is approximately: z_obs = |n_12 − n_21| / sqrt(n_discordant) ≈ |6 − 3| / 3 = 1.0; Φ(1.0 − 1.96) = Φ(−0.96) ≈ 0.17. The stated 0.40 appears to overestimate power by roughly 2×. If the actual power is ~0.17, the pilot has even lower power than claimed, which is not inherently disqualifying (it is a calibration pilot), but the incorrect power statement could mislead readers about the pilot's inferential capacity. | Major | "McNemar test power at n=30: approximately 0.40" — no derivation provided; back-calculation suggests ~0.17 is more accurate | Methodological Rigor |
| SR-003-i2 | The evidence-to-pilot generalizability bridge maps E-FOR-B-003 (DSPy assertions: 164% compliance) to "C4 (L2-re-injected negative)" with the note "C4 tests repetition/reinforcement mechanism." This mapping conflates two distinct mechanisms: DSPy programmatic assertion backtracking is an infrastructure-level mechanism (compile-time constraint enforcement with automatic retry), not a prompt-level re-injection. L2-re-injection in the pilot is a prompt-level mechanism (same constraint text prepended to each turn). These are not the same mechanism; mapping them as equivalent in the generalizability bridge overstates the evidence for C4. | Major | "E-FOR-B-003 (DSPy assertions: 164% compliance) → C4 (L2-re-injected negative)" — DSPy assertion backtracking is infrastructure-level, not prompt-level re-injection | Evidence Quality |
| SR-004-i2 | The document states four GO criteria for the pilot but the "Pilot data quality" criterion — "All 30 pairs produce valid evaluatable output" — is defined as zero systematic execution failures. However, the definition of systematic execution failure was narrowed in the PM-007 fix: "agent echoes only the constraint without addressing the task." A pilot with 5 pairs failing (16.7%) due to constraint echoing would pass the NO-GO threshold (> 20%) but the GO criterion requires "all 30 pairs produce valid output." These two criteria are inconsistent: the GO criterion requires 100% validity, but the NO-GO threshold only triggers at > 20% failure rate. A pilot with 5–19% failures satisfies neither GO nor NO-GO on this criterion, creating an undefined intermediate state. | Minor | "GO: All 30 pairs produce valid evaluatable output" vs. "NO-GO: Systematic execution failures > 20%" — undefined state between 0% and 20% failure | Internal Consistency |
| SR-005-i2 | The document resolves SR-005-i1 (score delta arithmetic rounding) by noting "+0.116 avg" in the statistics section vs. the "exact" +0.1155. However, in the comparison table, the delta is listed as "+0.116 avg" while the statistics section says "Average score delta I1 to final: +0.1155 (unweighted mean of +0.123 and +0.108; rounded to +0.116 in comparison table)." The table uses +0.116 but the note says +0.115 in the header row. This is a minor inconsistency between the document's own rounding note. | Minor | Statistics: "rounded to +0.116 in comparison table" — but the revision log header says "score delta +0.115 average" | Internal Consistency |

### Scoring Impact (S-010)

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Positive | All 16 Critical gaps now filled; all major protocol sections present and detailed |
| Internal Consistency | 0.20 | Slightly Negative | SR-001 (continuity correction rounding), SR-004 (GO/NO-GO intermediate state), SR-005 (delta rounding inconsistency) — three minor internal consistency issues remain |
| Methodological Rigor | 0.20 | Slightly Negative | SR-002 (pilot power overstated); SR-003 (DSPy ≠ L2-re-injection conflated in generalizability bridge) |
| Evidence Quality | 0.15 | Positive | π_d now grounded with comparable studies; evidence tier assignments maintained |
| Actionability | 0.15 | Positive | Pilot design is now executable with the added protocols |
| Traceability | 0.10 | Positive | Citations corrected, adversarial checks relabeled, confidence differentiated |

**Decision:** Major finding SR-002 (pilot power overstatement), Major finding SR-003 (DSPy mechanism conflation) require attention. Minor findings SR-001, SR-004, SR-005 are addressable without structural changes. Deliverable proceeds to S-003 per tournament sequence.

---

## S-003: Steelman

**Finding Prefix:** SM | **Execution ID:** i2-20260227

**H-16 Compliance:** S-010 self-review executed immediately prior (confirmed above).

### Charitable Interpretation

The R2 revision is substantially stronger than R1. The document now correctly bifurcates the research question, operationalizes the primary metric, redesigns the equivalence validation protocol, addresses the blinding failure mode, replaces the invalid stopping criterion, and protects the null finding against weaponized misreading. The revision demonstrates that the analyst absorbed and genuinely addressed the I1 findings rather than superficially acknowledging them.

The core argument is sound: (1) the 60% claim is untested in controlled conditions; (2) evidence exists for specific sub-types of negative prompting but not for the specific claim; (3) a pilot study with a properly specified protocol can calibrate the full experiment; (4) the revised pilot is now executable by a single researcher with LLM assistance.

The strongest section of the revision is the Equivalence Validation Protocol — the EC-1 through EC-5 checklist with inter-rater requirement is methodologically rigorous. The example pair redesign (P-ENV-001, P-CITE-001, P-SCOPE-001) correctly matches consequence documentation and eliminates the semantic non-equivalence identified in I1.

### Steelman Reconstruction Improvements

| ID | Improvement | Severity | Original | Strengthened | Dimension |
|----|-------------|----------|----------|--------------|-----------|
| SM-001-i2 | The pilot power calculation (approximately 0.40) should either be corrected or acknowledged as an approximation from a specific power table reference. The document's value appears inconsistent with the McNemar power formula. Rather than silence, the revision should explicitly state this is a rough estimate from a nomogram or cite a specific power calculation source. | Minor | "McNemar test power at n=30: approximately 0.40" — bare assertion | State the source of the 0.40 estimate (e.g., nomogram, specific software, analytical approximation). Alternatively, revise to "approximately 0.15–0.40 depending on the true discordant proportion" to convey the range of uncertainty. | Methodological Rigor |
| SM-002-i2 | The Evidence-to-Pilot Generalizability Bridge is a genuine contribution but would benefit from an explicit "mechanism hypothesis" column explaining WHY each evidence item is expected to generalize to the mapped condition. The current table shows mapping but not the causal pathway. | Minor | Bridge table has "Evidence Item → Pilot Condition → Expected Direction" | Add a "Mechanism Hypothesis" column: e.g., for E-AGN-B-001 → C1: "The AGREE-4 finding generalizes to C1 because naive standalone prohibition (C1) is the functional equivalent of the 'don't do X' instructions studied in the AGREE-4 source papers." | Evidence Quality |
| SM-003-i2 | The WARNING callout box is well-placed and strongly worded, but the PS Integration key_findings still states the null finding covers "~30-40% of plausible total evidence base." This estimate (from the Structural Exclusion Impact Assessment) would be strengthened by citing the specific derivation: the 30-40% figure represents published academic + public practitioner sources vs. SE-1 through SE-5 excluded domains. Making the derivation visible in the PS Integration block would strengthen the handoff's epistemic transparency. | Minor | PS Integration: "Null finding covers ~30-40% of plausible total evidence base" — no derivation | Cite: "30-40% per Structural Exclusion Impact Assessment: published academic + public practitioner sources only; SE-1 (closed production), SE-2 (domain expert), SE-3 (vendor internal), SE-4 (grey literature), SE-5 (publication bias) collectively exclude the majority of the evidence base." | Traceability |

### Best Case Scenario

The deliverable succeeds completely when: (1) the pilot is launched using the Equivalence Validation Protocol as written; (2) the pilot produces a GO verdict; (3) the full experiment is designed using the pilot-calibrated π_d; (4) the hallucination rate measurement is validated against human scoring before relying on LLM-assisted assessment. Under these conditions, the document provides an honest, complete, and executable research planning instrument. The null finding protection (WARNING callout) is robust against misreading. The experimental design is methodologically defensible.

**Scoring Impact (S-003):**

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Positive | All major sections now complete; no structural gaps |
| Internal Consistency | 0.20 | Positive | Research question bifurcation resolves the primary internal consistency failure |
| Methodological Rigor | 0.20 | Mostly Positive | Protocol additions are genuine improvements; minor power estimate issue remains |
| Evidence Quality | 0.15 | Positive | π_d grounded; evidence bridge added; revealed preference framing maintained |
| Actionability | 0.15 | Positive | Pilot is now executable |
| Traceability | 0.10 | Positive | Citations corrected; confidence differentiated; adversarial provenance clarified |

---

## S-002: Devil's Advocate

**Finding Prefix:** DA | **Execution ID:** i2-20260227

**H-16 Compliance:** S-003 Steelman executed immediately prior (confirmed above).

### Role Assumption

Deliverable: claim-validation.md (TASK-005, I2 revision). Criticality: C4. Role: Argue against the central analytical conclusions and the revised experimental design's sufficiency. Focus on new issues introduced by the revision and whether claimed resolutions hold under scrutiny.

### Assumption Inventory (Post-Revision)

**Revised assumptions that require fresh challenge:**
1. The hallucination rate protocol (evaluator verifies factual claims against source material) is operationalizable for prompt engineering tasks where "source material" varies across task categories
2. The output scrubbing procedure (masking NEVER, MUST NOT, ALWAYS, MUST) achieves evaluator blinding
3. The Equivalence Validation Protocol's EC-1 through EC-5 criteria are independently verifiable by raters without implicit bias
4. The 90% CI stopping criterion is achievable at n=30 given realistic power (~0.17)
5. The DSPy C4 mapping is valid (asserted in generalizability bridge)

### Findings Table

| ID | Finding | Severity | Evidence | Affected Dimension |
|----|---------|----------|----------|--------------------|
| DA-001-i2 | The hallucination rate definition ("any factual claim absent from source material") presupposes that pilot tasks have clearly defined "source material" — but for 3 of the 5 task categories (code review, architecture decision, documentation), the "source material" is not well-defined. Code review tasks reference code repositories; architecture decisions reference requirements documents; documentation tasks reference technical specifications. None of these have "source material" in the same sense as a research synthesis where claims are verifiable against cited papers. The hallucination rate protocol will be operationally ambiguous for these categories. | Major | "A hallucination is any factual claim that: (a) is not present in the provided source material" — "provided source material" is task-category-specific and poorly defined for non-research categories | Methodological Rigor |
| DA-002-i2 | The output scrubbing procedure masks "NEVER, MUST NOT, FORBIDDEN, DO NOT, ALWAYS, MUST (in imperative forms), REQUIRED TO" — but this masking list is incomplete. An agent instructed with "NEVER use pip install" might respond "you should avoid pip and instead use the approved package manager." The word "avoid" is not in the masking list but signals the negative framing condition. Similarly, "instead" signals the alternative was provided. The masking list addresses only direct vocabulary echo, not semantic echo — the condition may still be inferable from circumlocutory output even after masking. | Major | "Masked terms: NEVER, MUST NOT, FORBIDDEN, DO NOT, ALWAYS, MUST (in imperative forms), REQUIRED TO" — does not address semantic circumlocution | Methodological Rigor |
| DA-003-i2 | The equivalence criterion EC-2 (Consequence documentation: "same consequence stated, or absent from both") has an asymmetry problem in practice: the negative framing condition (C2) is architecturally defined to include consequence documentation ("NEVER X. Consequence."), but the positive equivalent (C3) is not required to have consequence documentation by the original IG-002 taxonomy. The protocol resolves this by requiring "matched consequence" — but the three example pairs all use semantically inverted consequences ("corrupted"/"remain clean", "fabrication"/"ensures accuracy", "unrecoverable"/"recoverable"). These are not semantically equivalent — they differ in valence and in implication (active harm vs. affirmative assurance). A reader of the C3 variant learns what WILL happen; a reader of the C2 variant learns what will NOT happen plus what WILL happen if they violate the rule. The asymmetry is inherent to consequence matching for negative vs. positive frames and cannot be eliminated without changing what C3 is. | Major | "EC-2: Consequence documentation — Same consequence stated (or absent from both). Identical consequence text OR both omit consequence." — Example P-ENV-001: "corrupted" vs. "remain clean" — these are not identical consequence text | Methodological Rigor |
| DA-004-i2 | The pilot GO criterion requires kappa ≥ 0.70 on calibration pairs, but the calibration sample is n=3 pairs (three of the 30 pilot pairs). With n=3 pairs, Cohen's kappa has extremely wide confidence intervals and is essentially statistically undefined: a single disagreement on 3 pairs drops kappa from 1.0 to approximately 0.67, failing the threshold. A single chance agreement or disagreement determines pass/fail. The kappa ≥ 0.70 threshold at n=3 is operationally unreliable as a quality gate. | Major | "3 of the 30 pilot pairs are scored by all evaluators independently; Cohen's kappa is calculated; required kappa > 0.70" — kappa at n=3 is statistically unstable | Methodological Rigor |
| DA-005-i2 | The power analysis for exploratory condition C2 vs. C5 (structured vs. paired) states "Required n = Near-infinite — likely no effect" under the assumption p_12 = 0.10, p_21 = 0.10. This is the trivial case where the researcher assumes equal performance in both directions (discordant proportion with no directional bias). If p_12 = p_21 = 0.10, then p_12 − p_21 = 0, and the required n is genuinely infinite. However, it is methodologically unusual to pre-specify a comparison while simultaneously assuming no effect exists: this amounts to acknowledging a priori that this comparison cannot be powered. The correct action is to either drop C2 vs. C5 from the full experiment's pre-specified comparisons or provide a substantive justification for including it. As written, the power table for C2 vs. C5 is internally incoherent. | Minor | "C2 vs. C5 (structured vs. paired): Required n = Near-infinite — likely no effect" — if no effect is expected, why include as a pre-specified comparison? | Internal Consistency |

### Response Requirements

**P1 (Major — SHOULD resolve):**

- **DA-001-i2:** The hallucination rate protocol must be operationalized separately for each task category. At minimum, define what "source material" means for: research synthesis (cited papers), code review (the code itself + language documentation), architecture decision (requirements specification + known constraints), documentation (the technical subject matter + stated objectives). Without category-specific operationalization, rater agreement will fail on non-research tasks.

- **DA-002-i2:** Extend the output scrubbing procedure to address semantic circumlocution. Options: (a) add semantic circumlocution terms to the masking list ("avoid," "instead," "rather than," "alternatively"), OR (b) acknowledge that semantic echo is an uncontrolled residual blinding risk and add it explicitly to the "Residual blinding risk" section.

- **DA-003-i2:** Acknowledge the consequence asymmetry explicitly. The corrected example pairs are improvements but the asymmetry between "what will go wrong" (C2) and "what will go right" (C3) is structurally inherent, not fully resolvable by word matching. Add to the Analytical Limitations section: "Consequence documentation in negative framing (C2) communicates risk; consequence documentation in positive framing (C3) communicates benefit. These are matched in surface form but differ in valence and implicature. This residual asymmetry is a limitation of the matched-pair design."

- **DA-004-i2:** Increase the calibration sample from n=3 to at least n=10 pairs, or use an alternative calibration approach: score all 30 pairs with two raters on the first 5 and calculate kappa there, then proceed with single-rater scoring for the remainder with the pre-calibrated rater. At n=3, kappa is not a reliable quality gate.

**P2 (Minor — acknowledge):**

- **DA-005-i2:** Either remove C2 vs. C5 from the pre-specified full experiment comparisons or add a substantive rationale for including a comparison that the power analysis predicts requires infinite sample size.

### Scoring Impact (S-002)

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Neutral | DA findings are protocol-level gaps, not missing sections |
| Internal Consistency | 0.20 | Slightly Negative | DA-005: C2 vs. C5 comparison pre-specified while power assumes zero effect |
| Methodological Rigor | 0.20 | Negative | DA-001, DA-002, DA-003, DA-004: Four methodological gaps in the revised protocol |
| Evidence Quality | 0.15 | Neutral | No new evidence quality failures |
| Actionability | 0.15 | Mostly Positive | Pilot remains executable; gaps are correctable |
| Traceability | 0.10 | Neutral | No traceability failures |

---

## S-004: Pre-Mortem

**Finding Prefix:** PM | **Execution ID:** i2-20260227

**H-16 Compliance:** S-003 confirmed prior.

**Failure Scenario Declaration:** It is November 2026. The n=30 pilot was launched using the R2 claim-validation.md as the design document. The pilot produced ambiguous results — the GO criteria were not clearly met or not met. The research team is now analyzing why the pilot document was an insufficient operational guide. The I1 failures have been resolved, so we focus on what R2 introduced or left unresolved.

### Findings Table

| ID | Failure Cause | Category | Likelihood | Severity | Priority | Affected Dimension |
|----|---------------|----------|------------|----------|----------|--------------------|
| PM-001-i2 | Hallucination rate measurement failed for non-research task categories: evaluators could not agree on what constituted "source material" for code review tasks. One rater counted the language documentation as source material; another counted only the code provided. Kappa on hallucination rate for code review pairs: 0.48 — below the 0.70 threshold, blocking pilot proceed | Process | High | Major | P1 | Methodological Rigor |
| PM-002-i2 | Output scrubbing masked NEVER/ALWAYS vocabulary but agents produced semantically detectable outputs: "please be careful not to use the non-approved package manager" was not masked, allowing evaluators to detect the negative condition. Blinding failure rate: estimated 30-40% of outputs detectable through circumlocution | Process | Medium | Major | P1 | Methodological Rigor |
| PM-003-i2 | The calibration kappa (n=3 pairs, required ≥ 0.70) failed twice before the research team realized the sample was too small to produce reliable kappa estimates. Three additional calibration rounds were run, delaying pilot launch by 2 weeks. The document's n=3 calibration sample is operationally unworkable. | Process | High | Major | P1 | Methodological Rigor |
| PM-004-i2 | The pilot used the PI-based stopping criterion (90% CI for p_12 − p_21 excludes zero). At n=30 with power ~0.17, the CI did not exclude zero — but the research team disagreed on whether this meant NO-GO or merely "insufficient power." The pilot report says NO-GO; the principal investigator says the pilot was underpowered by design and GO should be based on the discordant proportion estimate, not the CI test. The criterion created a disputed verdict. | Assumption | High | Major | P1 | Internal Consistency |
| PM-005-i2 | The C2 vs. C5 comparison (structured vs. paired) was included in the full experiment's pre-specified comparisons despite the power table noting "near-infinite" required n. The IRB application listed 7 comparisons; reviewers questioned why the experiment was designed around a comparison where no effect was assumed. The response required a protocol amendment. | Process | Low-Medium | Minor | P2 | Internal Consistency |
| PM-006-i2 | The DSPy mechanism (C4 in generalizability bridge) was used to argue for C4's inclusion in the full experiment. When reviewers asked for the mechanism bridging DSPy assertion backtracking to prompt-level L2-re-injection, the document had no mechanism hypothesis. The rationale for C4 was not defensible from the written evidence bridge. | Technical | Medium | Minor | P2 | Evidence Quality |

### Scoring Impact (S-004)

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Neutral | No missing sections in R2 |
| Internal Consistency | 0.20 | Negative | PM-004: Stopping criterion creates disputed interpretation; PM-005: C2 vs. C5 pre-specified despite zero-effect assumption |
| Methodological Rigor | 0.20 | Negative | PM-001, PM-002, PM-003: Three medium-to-high likelihood process failures |
| Evidence Quality | 0.15 | Slightly Negative | PM-006: DSPy mechanism gap in generalizability bridge |
| Actionability | 0.15 | Slightly Negative | PM-004: Stopping criterion interpretation is ambiguous when CI doesn't exclude zero but pilot is intentionally underpowered |
| Traceability | 0.10 | Neutral | No traceability pre-mortem failures |

---

## S-001: Red Team

**Finding Prefix:** RT | **Execution ID:** i2-20260227

**H-16 Compliance:** S-003 confirmed prior.

**Threat Actor Profile (I2):**
- **Goal:** Exploit the R2 revision's new content to (a) launch a pilot that will produce uninterpretable results due to unresolved protocol gaps, or (b) use the WARNING callout against the document by claiming it pre-emptively disclaims its own null finding
- **Capability:** Full access to document; statistical methodology knowledge; awareness of I1 findings
- **Motivation:** Stop the research before it can produce a GO verdict by engineering a pilot design that fails on protocol grounds

### Attack Vectors

| ID | Attack Vector | Category | Exploitability | Severity | Priority | Defense | Affected Dimension |
|----|---------------|----------|----------------|----------|----------|---------|-------------------|
| RT-001-i2 | The pilot stopping criterion (90% CI for p_12 − p_21 excludes zero) is mathematically expected NOT to fire at n=30 given actual power ~0.17. A bad-faith actor can point to the NO-GO criterion being triggered (CI includes zero) and argue the pilot failed — when in fact the pilot was never designed to produce a definitive directional signal, only to estimate π_d. The document does not explicitly reconcile the GO criterion (CI excludes zero) with the stated purpose (calibration, not confirmation). | Ambiguity Exploit | High | Major | P1 | Missing | Internal Consistency |
| RT-002-i2 | The WARNING callout says "Do not cite this analysis as evidence that negative prompting does not work." A bad-faith actor can invert this: "The author felt it necessary to include a WARNING against misreading their own null finding — this itself suggests the evidence is weak enough to be weaponized." The WARNING, while protective, also signals that the null finding has been weaponized before and creates a meta-narrative about the document's credibility. | Rhetorical Attack | Low | Minor | P2 | N/A (unavoidable) | Evidence Quality |
| RT-003-i2 | The consequence matching in example pairs (P-ENV-001, P-CITE-001, P-SCOPE-001) uses valence-inverted consequences ("corrupted" → "remain clean"). A methodologist reviewing the protocol could argue that these are not matched consequences but inverted ones — violating EC-2 in spirit while satisfying it formally. If the equivalence validation raters accept valence-inverted consequences as "same consequence (or absent from both)," the protocol has a semantic gap that permits non-equivalent pairs to pass validation. | Boundary Exploit | Medium | Major | P1 | Partial (EC-2 criterion present but insufficient) | Methodological Rigor |
| RT-004-i2 | The PROJ-007 regime verification states the "characterization of PROJ-007 as the 'positive framing' comparison condition is verified and justified" because PROJ-007 PLAN.md uses positive framing. However, PROJ-007 was a multi-phase agent patterns research project that invoked `/adversary`, which executes strategies with HARD/MUST NOT vocabulary. A red team actor could argue that the `/adversary` invocations during PROJ-007 introduced substantial negative-constraint vocabulary that invalidates the positive-framing-control premise, since the framework's constitutional rules (loaded at every session) use NEVER/MUST NOT vocabulary that both projects share equally. The document's own caveat mentions "shared framework vocabulary" but then proceeds to treat PROJ-007 as the positive-framing baseline anyway. | Evidence Attack | Medium | Minor | P2 | Partial (acknowledged in document) | Evidence Quality |

### Defense Gap Assessment

**RT-001-i2 (Major — Missing defense):** The GO criterion and the stated pilot purpose are inconsistent. The document says the pilot purpose is "to estimate π_d before committing to the full experiment" — a calibration goal. But the GO criterion requires "90% CI for (p_12 − p_21) excludes zero" — an inferential goal that requires directional power the pilot lacks (~0.17). A calibration pilot can succeed at its purpose (estimating π_d) even if the CI includes zero. The document needs to resolve this: either (a) lower the GO CI criterion (e.g., "90% CI width < 0.40" as a precision criterion rather than a direction criterion), or (b) clarify that the CI criterion is supplementary to the discordant proportion criterion, and the pilot succeeds if π_d is in range even when CI includes zero.

**RT-003-i2 (Major — Partial defense):** EC-2 as written ("Identical consequence text OR both omit consequence") would formally reject P-ENV-001 ("corrupted" vs. "remain clean") since these are not identical text. Yet the document presents this pair as passing EC-2. The protocol appears to tacitly redefine EC-2 to mean "thematically matched consequence" rather than "identical consequence text." This needs to be made explicit or the example pairs redesigned to use identical consequence language.

### Scoring Impact (S-001)

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Neutral | No missing sections |
| Internal Consistency | 0.20 | Negative | RT-001: GO criterion inconsistent with pilot purpose; RT-003: EC-2 criterion inconsistently applied to example pairs |
| Methodological Rigor | 0.20 | Slightly Negative | RT-003: Equivalence criterion gap enables non-equivalent pairs to pass |
| Evidence Quality | 0.15 | Neutral | RT-002, RT-004 are low-severity acknowledged limitations |
| Actionability | 0.15 | Neutral | Red team countermeasures are implementable |
| Traceability | 0.10 | Neutral | No traceability attack surface |

---

## S-007: Constitutional AI

**Finding Prefix:** CC | **Execution ID:** i2-20260227

### Constitutional Context Loaded

Applicable rules for a research analysis document (I2 revision):
- H-03 (P-022): No deception about actions, capabilities, or confidence
- H-13: Quality threshold >= 0.95 for C4
- H-15: Self-review before presenting
- H-23: Navigation table required
- P-001 (Truth/Accuracy): Claims backed by evidence
- P-004 (Provenance): Source citations required
- P-011 (Evidence-Based): Every claim includes direct evidence

### Findings Table

| ID | Principle | Tier | Severity | Evidence | Affected Dimension |
|----|-----------|------|----------|----------|--------------------|
| CC-001-i2 | P-001 (Truth/Accuracy): The pilot power statement "approximately 0.40" is presented as a fact without derivation or source. If the actual power is ~0.17 (as back-calculation suggests), this represents a materially inaccurate claim about the pilot's inferential capacity. The document presents a quantitative value without verifying it. | HARD | Major | "McNemar test power at n=30: approximately 0.40 (low — appropriate for a pilot; sufficient to estimate π_d and detect large effects)" — arithmetic back-calculation contradicts this value | Methodological Rigor |
| CC-002-i2 | P-004 (Provenance): The CI-based stopping criterion — "compute the 90% CI for the difference in proportions" — does not specify which CI method (Wald, Wilson, Clopper-Pearson, etc.) should be used for the proportion difference at small n. With n_discordant potentially as low as 3–9 (30 × 0.10–0.30), the CI method choice substantially affects coverage. The stopping criterion is incomplete without specifying the CI method. | MEDIUM | Major | "Compute the 90% CI for the difference in proportions" — no CI method specified; at small n (< 30 discordant pairs), Wald CI for a proportion difference has poor coverage | Methodological Rigor |
| CC-003-i2 | H-15 (Self-review before presenting): The I2 revision claims all inline adversarial checks are labeled as "Preliminary Self-Review (pre-I1)." The Adversarial Quality Checks section correctly labels them accordingly. H-15 compliance requires self-review before presenting I2. The document's footer states "I2 preliminary self-review: S-013 (Inversion), S-004 (Pre-Mortem), S-003 (Steelman) applied pre-I1" — these are the I1 self-reviews, not I2. There is no H-15 compliant self-review documented for the I2 revision itself. The I2 revision introduces new content (all protocol additions) that has not been self-reviewed before the I2 tournament. | MEDIUM | Minor | Footer: self-review documented for "pre-I1" stage only. I2 additions (Equivalence Validation Protocol, Output Scrubbing, CI criterion, model selection, etc.) have no documented self-review pass before the I2 tournament. | Methodological Rigor |
| CC-004-i2 | P-001 (Truth/Accuracy): The PROJ-007 prompting regime verification states "PROJ-007 PLAN.md uses positive framing throughout." This is verified. However, the document also claims "the experimental variable is the PLAN.md project-level negative constraint governance, not the complete absence of all negative vocabulary in the session." This reframing narrows the experimental variable definition after the fact to preserve the validity of the retrospective comparison. The original "positive framing control" premise implied a broader absence of negative constraints than what was verified. The narrowing is epistemically reasonable but changes the nature of what is being compared — without explicitly noting this is a scope reduction from the original claim. | MEDIUM | Minor | "Experimental variable is the PLAN.md project-level negative constraint governance" — narrower than "PROJ-007 used standard positive framing without explicit negative enforcement constraints" stated in the comparison premise | Evidence Quality |

### Constitutional Compliance Score

Penalty calculation: 0 Critical (0.10 × 0) + 2 Major (0.05 × 2) + 2 Minor (0.02 × 2) = 0.14 penalty
Compliance score: 1.00 − 0.14 = **0.86 → above 0.85 minimum but below 0.92 standard**

### Scoring Impact (S-007)

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Neutral | No constitutional completeness gap |
| Internal Consistency | 0.20 | Slightly Negative | CC-004: experimental variable scope narrowed without explicit acknowledgment |
| Methodological Rigor | 0.20 | Negative | CC-001 (power misstatement), CC-002 (CI method unspecified), CC-003 (H-15 gap for I2 additions) |
| Evidence Quality | 0.15 | Neutral | CC-004 is acknowledged limitation, not a deception |
| Actionability | 0.15 | Neutral | Corrections are mechanical |
| Traceability | 0.10 | Neutral | Citations corrected from I1; no new traceability failures |

---

## S-011: Chain-of-Verification

**Finding Prefix:** CV | **Execution ID:** i2-20260227

### Claim Inventory (I2 New Content — Testable Factual Claims)

The I1 claim inventory is carried forward. Focus here on claims introduced in the I2 revision:

| CL-ID | Claim | Source Asserted | Type |
|-------|-------|-----------------|------|
| CL-009 | "Chain-of-thought vs. zero-shot paired comparisons (Wei et al., 2022, NeurIPS) observe disagreement rates of 20-40% across task types" | Wei et al., 2022 NeurIPS cited for π_d grounding | Empirical claim with specific value range |
| CL-010 | "IFEval benchmark analysis (Zhou et al., A-17) shows instruction-following success rates of 50-80% depending on model and instruction type; for instruction types where models have similar success rates, paired disagreement would be approximately 2 × success_rate × (1 − success_rate), which at 70% success gives 2 × 0.70 × 0.30 = 0.42; at 80% gives 0.32. The 0.30 assumption is on the lower end of this range." | Zhou et al. (A-17) + mathematical derivation | Mathematical derivation with specific values |
| CL-011 | "McNemar test power at n=30: approximately 0.40 (low)" | Bare assertion, no source | Power calculation |
| CL-012 | "(z_α/2 + z_β)² = 7.84 for α = 0.05 (two-tailed) and power = 80%" | Standard statistics | Parameter values |
| CL-013 | "DSPy programmatic assertion-based constraints... 164% more constraint compliance, 37% more high-quality responses" (from E-FOR-B-003, carried from I1) | Singhvi et al., arXiv (C-13) | Empirical values |
| CL-014 | Continuity correction: "n_cc = n_unadj + z²_α/2 × (p_12 + p_21) / (4 × (p_12 − p_21)²)" attributed to Agresti (2013) §10.1 | Agresti 2013 | Formula |

### Verification Questions and Results

**CL-009 (Wei et al., 2022 NeurIPS — 20-40% disagreement rates):** Wei et al. (2022) is the chain-of-thought prompting paper ("Chain-of-Thought Prompting Elicits Reasoning in Large Language Models"). The paper studies performance gains, not "disagreement rates" in paired comparisons. The specific claim that CoT vs. zero-shot "observe disagreement rates of 20-40%" is not a stated result in that paper — the paper reports accuracy improvements, not discordant proportion statistics from paired evaluation. The 20-40% range appears to be an inference or extrapolation by the document's author from accuracy data, not a directly reported value. **MATERIAL DISCREPANCY** — the cited paper does not directly report the claimed values; the citation is being used to support a value that is extrapolated rather than directly stated.

**CL-010 (IFEval derivation: 2 × p × (1-p)):** The formula 2 × p × (1-p) for expected disagreement between two independent classifiers is correct for the case where both classifiers have success probability p and are independent. For paired conditions where success rates differ, the expected discordant proportion is p_1 × (1-p_2) + p_2 × (1-p_1), not 2p(1-p). The document uses the symmetric formula as an approximation when success rates are similar. This is a reasonable approximation but the assumption of similar success rates across C2 and C3 is exactly the null hypothesis the experiment is designed to test. Using the approximation formula here has a mild circularity: it assumes p_1 ≈ p_2 to estimate π_d, which is valid only under the null. **MINOR DISCREPANCY** — the formula is technically correct only under the approximation that conditions perform similarly.

**CL-011 (Power ≈ 0.40 at n=30):** Back-calculation: expected discordant pairs = 30 × 0.30 = 9. For McNemar with n_d = 9, p_12 = 0.20/(0.20+0.10) ≈ 0.667 under H_1 (2/3 of discordant pairs favor negative): Test statistic under H_1: |n_12 - n_21| / sqrt(n_d) ≈ |6 - 3| / 3 = 1.0. Power = P(Z > 1.96 - 1.0) + P(Z < -1.96 - 1.0) ≈ Φ(-0.96) ≈ 0.17 (one-directional component). The 0.40 value is not reproduced. **MATERIAL DISCREPANCY** — the claimed power of ~0.40 appears to overestimate power at n=30 by approximately 2×.

**CL-012 ((z_α/2 + z_β)² = 7.84):** z_α/2 = 1.96, z_β = 0.842 (for 80% power), sum = 2.802, squared = 7.85. Rounding to 7.84 is within accepted precision. **VERIFIED** (within rounding).

**CL-013 (DSPy 164% compliance):** Carried from I1; cited as Tier 3 arXiv (Singhvi et al., C-13). **UNVERIFIABLE** from published sources; classification as Tier 3 is appropriate. No new discrepancy.

**CL-014 (Continuity correction formula):** The formula n_cc = n_unadj + z²_α/2 × (p_12 + p_21) / (4 × (p_12 − p_21)²) is being attributed to Agresti 2013 §10.1. Standard references (Agresti 2013, "Categorical Data Analysis") §10.1 covers McNemar's test but does not include this specific sample size continuity correction formula. The standard McNemar continuity correction is applied to the test statistic (|n_12 − n_21| − 1) rather than to the sample size. This appears to be a derived formula not directly from Agresti §10.1. **PARTIALLY UNVERIFIED** — the formula may be correct but the attribution to Agresti §10.1 appears imprecise (same issue as I1 CC-002 which was claimed as resolved).

### Findings Table

| ID | Claim | Source | Discrepancy | Severity | Affected Dimension |
|----|-------|--------|-------------|----------|--------------------|
| CV-001-i2 | "Wei et al., 2022, NeurIPS — disagreement rates of 20-40%" | Wei et al. 2022 CoT paper | Wei et al. (2022) reports accuracy improvements, not discordant proportion rates; the 20-40% range is the author's extrapolation, not a directly reported value | Major | Evidence Quality |
| CV-002-i2 | "McNemar test power at n=30: approximately 0.40" | Bare assertion | Back-calculation yields ~0.17, not 0.40; the claim overstates pilot power by approximately 2× | Major | Methodological Rigor |
| CV-003-i2 | McNemar continuity correction formula attributed to "Agresti 2013 §10.1" | Agresti (2013) | Agresti §10.1 presents a test statistic continuity correction, not a sample size continuity correction formula; attribution remains imprecise from I1 | Minor | Traceability |

### Scoring Impact (S-011)

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Neutral | Claim inventory comprehensive |
| Internal Consistency | 0.20 | Neutral | No new internal consistency discrepancies from I2 additions |
| Methodological Rigor | 0.20 | Negative | CV-002: Power calculation appears materially incorrect |
| Evidence Quality | 0.15 | Negative | CV-001: Citation used to support a value not directly in the cited source |
| Actionability | 0.15 | Slightly Positive | CV-001, CV-002 corrections are specific: revise power estimate and citation language |
| Traceability | 0.10 | Slightly Negative | CV-003: Continuity correction attribution remains imprecise (persisted from I1) |

---

## S-012: FMEA

**Finding Prefix:** FM | **Execution ID:** i2-20260227

**H-16 Compliance:** S-003 confirmed prior. S-004 Pre-Mortem completed immediately prior.

### Element Decomposition (Focused on I2 Additions)

| Element | Sub-elements |
|---------|-------------|
| E1: Hallucination Rate Protocol | E1a: Operational definition, E1b: Task-category-specific operationalization, E1c: LLM-assisted evaluation plan |
| E2: Equivalence Validation Protocol | E2a: EC-1 through EC-5 checklist, E2b: Inter-rater requirement, E2c: Example pairs, E2d: Adjudication |
| E3: Output Scrubbing Procedure | E3a: Masking list, E3b: Semantic circumlocution, E3c: Validation test |
| E4: Statistical Stopping Criterion | E4a: CI-based criterion, E4b: Pilot purpose consistency, E4c: CI method specification |
| E5: Calibration Protocol | E5a: Kappa requirement, E5b: Calibration sample size |
| E6: Power Analysis | E6a: Pilot power calculation, E6b: Full experiment power table |

### Failure Mode Table (RPN > 80)

| ID | Element | Failure Mode | S | O | D | RPN | Severity | Corrective Action | Affected Dimension |
|----|---------|-------------|---|---|---|-----|----------|-------------------|--------------------|
| FM-001-i2 | E1b: Hallucination rate protocol | Missing: task-category-specific operationalization of "source material" — protocol is only coherent for research synthesis tasks; ambiguous for code review, architecture, documentation | 8 | 7 | 7 | 392 | Major | Define what "source material" means for each of the 5 task categories before pilot launch | Methodological Rigor |
| FM-002-i2 | E3b: Output scrubbing | Missing: semantic circumlocution not addressed — masking vocabulary list is incomplete; agents can signal the framing condition through synonyms and paraphrases | 7 | 7 | 7 | 343 | Major | Extend masking list to include semantic circumlocution, OR explicitly document this as a residual uncontrolled blinding risk | Methodological Rigor |
| FM-003-i2 | E5b: Calibration protocol | Incorrect: kappa calculation at n=3 pairs is statistically unreliable — single disagreement changes pass/fail outcome | 7 | 8 | 6 | 336 | Major | Increase calibration sample to ≥ 10 pairs; revise protocol accordingly | Methodological Rigor |
| FM-004-i2 | E4b: Stopping criterion consistency | Inconsistent: GO criterion (CI excludes zero) requires directional power (~0.60+); pilot was designed for calibration (power ~0.17); the two purposes are in tension | 7 | 7 | 7 | 343 | Major | Add explicit reconciliation: the CI criterion is supplementary; pilot succeeds at its primary purpose (π_d estimation) regardless of CI outcome; add secondary GO criterion based on discordant proportion range alone | Internal Consistency |
| FM-005-i2 | E6a: Power calculation | Incorrect: stated power ~0.40 at n=30; back-calculation yields ~0.17; the error is material for readers deciding pilot sample size adequacy | 6 | 8 | 6 | 288 | Major | Correct the power estimate or provide a verified derivation/source for the 0.40 value | Methodological Rigor |
| FM-006-i2 | E2c: Example pairs | Ambiguous: EC-2 criterion ("identical consequence text OR both omit") conflicts with example pairs using valence-inverted consequences ("corrupted" / "remain clean"); the example pairs appear to fail EC-2 as written | 6 | 6 | 7 | 252 | Major | Revise EC-2 to explicitly permit valence-inverted consequence matching ("thematically matched consequence, same domain, inverted valence") OR redesign example pairs to use identical consequence language | Methodological Rigor |
| FM-007-i2 | E6b: Full experiment power table | Underspecified: C2 vs. C5 power listed as "near-infinite" under assumption of zero effect; this comparison should not be pre-specified if no detectable effect is expected | 4 | 5 | 6 | 120 | Minor | Remove C2 vs. C5 from pre-specified confirmatory comparisons OR add substantive rationale for testing a comparison expected to show no effect | Internal Consistency |
| FM-008-i2 | E4c: CI method | Missing: stopping criterion says "compute the 90% CI for the difference in proportions" without specifying which CI method; at small n_discordant, method choice affects coverage substantially | 5 | 6 | 6 | 180 | Major | Specify CI method: recommend Wilson or Clopper-Pearson for small n; Wald is not recommended at n_discordant < 30 | Methodological Rigor |

**Total RPN (I2 new findings):** 2254. Highest RPN element: E1b Hallucination Rate Protocol (392) and E4b Stopping Criterion (343).

### Comparison to I1

I1 total RPN (findings with RPN > 80): 3421. I2 total RPN (new findings): 2254. The revision substantially reduced risk, particularly in the highest-RPN categories (E4a matched-pair protocol was RPN 576 in I1, now resolved; E4d evaluator blinding was 448, now partially resolved). The remaining I2 issues are real but less severe than the I1 issues.

### Scoring Impact (S-012)

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Mostly Positive | Major protocol sections now complete; FM-007 is a minor gap |
| Internal Consistency | 0.20 | Negative | FM-004 (stopping criterion vs. pilot purpose), FM-006 (EC-2 vs. example pairs), FM-007 (C2/C5 pre-specified with zero effect) |
| Methodological Rigor | 0.20 | Negative | FM-001, FM-002, FM-003, FM-005, FM-008: Five methodological gaps in the revised protocol |
| Evidence Quality | 0.15 | Neutral | No new evidence quality failures at FMEA level |
| Actionability | 0.15 | Mostly Positive | Gaps are correctable; pilot is still fundamentally executable |
| Traceability | 0.10 | Neutral | No new FMEA-level traceability failures |

---

## S-013: Inversion

**Finding Prefix:** IN | **Execution ID:** i2-20260227

**H-16 Compliance:** S-003 confirmed prior. S-012 FMEA completed immediately prior.

### Goals (Post-Revision)

The I2 revision's stated goals are:
1. Correct the construct validity failure (hallucination rate as primary metric)
2. Make the pilot executable (equivalence protocol, blinding, stopping criterion)
3. Preserve the null finding's epistemic status (WARNING callout)
4. Provide a research planning document sufficient to launch Phase 2

### Revised Assumption Map

| ID | Assumption | Type | Confidence | Validation Status | Failure Consequence |
|----|------------|------|------------|-------------------|---------------------|
| A1 | Hallucination rate is measurable consistently across all 5 task categories with the protocol as written | Technical | Medium-Low | Not tested; category-specific operationalization absent | Rater disagreement collapses hallucination rate metric for non-research tasks |
| A2 | Output scrubbing (vocabulary masking) achieves evaluator blinding | Process | Medium | Tested on 5 examples (stated) before pilot; semantic circumlocution unaddressed | Blinding fails; systematic evaluator bias favoring expected winner |
| A3 | The pilot power (~0.40 as stated, ~0.17 per back-calculation) is sufficient for the pilot's calibration purpose | Assumption | Low | Power stated without derivation; back-calculation contradicts | Pilot produces no usable directional signal even for calibration |
| A4 | The 90% CI stopping criterion is achievable at n=30 | Technical | Low | Power analysis implies CI will include zero at realistic effect sizes with ~0.17 power | GO criterion not met; dispute about whether pilot succeeded |
| A5 | Calibration kappa at n=3 pairs is a reliable quality gate | Process | Very Low | Statistically undefined at n=3; single disagreement determines pass/fail | Kappa < 0.70 on chance; calibration loop blocks pilot launch |
| A6 | EC-2 (consequence matching) is operationally consistent with the example pairs | Technical | Low | Example pairs use valence-inverted consequences that appear to violate EC-2 as written | Raters reject the example pairs as non-equivalent; protocol inconsistency exposed |
| A7 | The Wei et al. (2022) citation supports the 20-40% discordant proportion range | Evidence | Low | Wei et al. (2022) reports accuracy, not discordant proportions; extrapolation not documented | π_d grounding appears weaker than claimed; confidence in 0.30 estimate reduced |

### Stress-Test Findings

| ID | Assumption | Inversion | Severity | Affected Dimension |
|----|------------|-----------|----------|--------------------|
| IN-001-i2 | A1: Hallucination rate measurable across task categories | If hallucination rate cannot be reliably measured for code review, architecture decision, or documentation tasks (the 3 non-research categories), the pilot's primary metric fails for 60% of the task category scope. The experiment effectively reduces to a research synthesis task only, which is one task category — insufficient for the 5-category design. | Major | Methodological Rigor |
| IN-002-i2 | A4: 90% CI criterion achievable at n=30 | If the 90% CI consistently includes zero at n=30 (the likely outcome given ~0.17 power), the GO criterion as written will not be met. The pilot will produce a technically NO-GO verdict even when it has successfully estimated π_d in the target range (0.10–0.50). This makes the stopping criterion systematically overly conservative relative to the pilot's stated purpose. | Major | Internal Consistency |
| IN-003-i2 | A5: Calibration kappa reliable at n=3 | If kappa at n=3 pairs is statistically unreliable (as it is, mathematically), then the kappa ≥ 0.70 calibration gate will sometimes fail due to sampling variance alone, not due to genuine rater disagreement. The protocol will produce false-negative calibration failures that delay pilot launch without meaningful quality signal. | Major | Methodological Rigor |
| IN-004-i2 | A6: EC-2 consistent with example pairs | If the example pairs are reviewed by raters who interpret EC-2 literally ("identical consequence text OR both omit"), the three provided example pairs will all fail EC-2 because "corrupted" ≠ "remain clean" (not identical text; neither is absent). The Equivalence Validation Protocol would then have example pairs that fail its own protocol — the same failure type as the I1 DA-005 finding, now in a different criterion. | Major | Methodological Rigor |
| IN-005-i2 | A7: Wei et al. citation supports 20-40% | If the Wei et al. (2022) citation is examined and found not to contain the claimed 20-40% discordant proportion range, the π_d grounding is reduced to a single approximation formula (the 2p(1-p) derivation from IFEval) plus a general statement of consistency. The grounding is weaker than presented but not absent. | Minor | Evidence Quality |

### Scoring Impact (S-013)

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Mostly Positive | No structural gaps; minor evidence weaknesses |
| Internal Consistency | 0.20 | Negative | IN-002 (GO criterion vs. pilot purpose), IN-004 (EC-2 vs. example pairs): two internal consistency failures in the revised design |
| Methodological Rigor | 0.20 | Negative | IN-001, IN-003, IN-004: Three methodological assumption failures in the revised protocol |
| Evidence Quality | 0.15 | Slightly Negative | IN-005: π_d grounding citation weaker than claimed |
| Actionability | 0.15 | Mostly Positive | Pilot remains executable; identified failures are correctable |
| Traceability | 0.10 | Neutral | Assumption map is internally traceable |

---

## S-014: LLM-as-Judge

**Finding Prefix:** LJ | **Execution ID:** i2-20260227

### Anti-Leniency Declaration

This scoring applies the rubric strictly. The C4 threshold is 0.95. The revision substantially improved the deliverable from I1 (0.771). The question is whether the improvements are sufficient to reach 0.95. Improvements are not scored leniently because they exist — they are scored on whether the current state meets the rubric criteria. Remaining gaps are not excused by noting that I1 gaps were worse.

### Dimension Scoring

**Completeness (weight: 0.20)**

Criteria evaluated:
- All required sections present: YES — L0, L1, L2, Experimental Design, Evidence Table, Limitations, Adversarial Checks, Revision Log
- Navigation table present: YES
- Revision log present: YES (comprehensive finding-by-finding resolution documentation)
- WARNING callout for null finding: YES (prominent; well-worded)
- Evidence catalog: YES (comprehensive, 21 entries)
- Research question bifurcation: YES — hallucination vs. compliance distinction formal and operational
- Hallucination rate protocol: PARTIAL — operational definition present; task-category-specific source material not defined (FM-001-i2)
- Equivalence Validation Protocol: YES — detailed; minor EC-2 inconsistency with example pairs
- Statistical power analysis for all 7 conditions: YES (resolved from I1)
- Execution feasibility plan: YES (resolved from I1)
- Structural exclusion impact assessment: YES (resolved from I1)
- Evidence-to-pilot generalizability bridge: YES (resolved from I1)
- CI method for stopping criterion: ABSENT (FM-008-i2)

Score assessment: The document is dramatically more complete than I1. The main completeness gap is the task-category-specific hallucination rate operationalization (a material gap for 3 of 5 task categories) and the CI method specification. **Score: 0.88**

**Internal Consistency (weight: 0.20)**

Criteria evaluated:
- Research question formal statement consistent with all experimental conditions: YES
- Primary metric (hallucination rate) consistent with stated claim: YES (resolved from I1)
- Confidence values differentiated: YES (resolved from I1)
- Comparison table uses separate Barrier 3/4 data: YES (resolved from I1)
- Score delta arithmetic consistent: MOSTLY (SR-001 minor discrepancy in continuity correction arithmetic; SR-005 rounding note inconsistency)
- GO criteria consistent with pilot purpose (calibration vs. confirmation): NO — GO criterion (CI excludes zero at 90%) requires directional power the pilot does not have; this is inconsistent with the stated pilot purpose of π_d calibration (RT-001-i2, FM-004-i2, IN-002-i2)
- EC-2 criterion consistent with example pairs: NO — "identical consequence text" in EC-2 vs. "corrupted"/"remain clean" in P-ENV-001 (RT-003-i2, FM-006-i2, IN-004-i2)
- C2 vs. C5 power analysis consistent with pre-specification: NO — "near-infinite required n" vs. pre-specified comparison (DA-005-i2, FM-007-i2)
- Calibration sample size (n=3) consistent with kappa reliability requirement: NO — kappa at n=3 is statistically unstable (DA-004-i2, FM-003-i2, IN-003-i2)

Score assessment: Three substantive internal consistency failures remain: GO criterion vs. pilot purpose, EC-2 vs. example pairs, calibration sample vs. kappa reliability. One additional minor issue (C2/C5 power). These are real failures in a document that is otherwise substantially improved. **Score: 0.78**

**Methodological Rigor (weight: 0.20)**

Criteria evaluated:
- Evidence tiering methodology applied systematically: YES
- Confound table for retrospective comparison: YES
- Matched-pair equivalence protocol: YES (but EC-2 criterion inconsistently applied to examples)
- Evaluator blinding: YES (scrubbing specified) — but semantic circumlocution not addressed (DA-002-i2, FM-002-i2)
- Statistical stopping criterion: PARTIALLY VALID — CI-based is correct but method not specified and inconsistent with pilot power
- Multiple comparisons: YES (Bonferroni-Holm declared; confirmatory vs. exploratory split)
- Power analysis: PARTIALLY VALID — stated power 0.40 appears incorrect (~0.17 per back-calculation); CV-002-i2, FM-005-i2, CC-001-i2
- Calibration protocol: PARTIALLY VALID — kappa threshold reasonable; calibration sample n=3 is too small (DA-004-i2, FM-003-i2)
- Hallucination rate protocol: PRESENT but task-category-specific operationalization absent (DA-001-i2, FM-001-i2)
- Model selection criteria: YES (resolved from I1)
- McNemar formula: CORRECT (arithmetic verified from I1)

Score assessment: Methodological rigor is substantially improved from I1 (score was 0.72 in I1). The equivalence protocol and blinding protocol are genuine improvements. However, four material methodological gaps remain: power calculation accuracy, calibration sample size, source material operationalization, and CI method specification. **Score: 0.81**

**Evidence Quality (weight: 0.15)**

Criteria evaluated:
- Evidence tiering applied consistently: YES
- Critical scope distinctions maintained: YES (AGREE-4 scope, Type 1 vs. Types 2-4 distinction)
- All claims backed by sources: MOSTLY — Wei et al. citation extrapolation issue (CV-001-i2)
- π_d assumption grounded: YES (improved from I1) — with caveat that Wei et al. citation may not directly support the claimed 20-40% range
- PROJ-007 prompting regime verified: YES (resolved from I1)
- Evidence generalizability bridge: YES — but DSPy mechanism conflation remains (SR-003-i2)
- Vendor evidence epistemic status: YES (revealed preference framing)
- Citation temporality: Corrected (CV-001-i1 and CV-002-i1 resolved) — CV-003-i2 (Agresti attribution) persists as a minor issue

Score assessment: Evidence quality is substantially improved from I1 (score was 0.80). One new citation issue (Wei et al. extrapolation), one persisting attribution issue (Agresti). DSPy mechanism conflation is a minor but real evidence quality gap. **Score: 0.87**

**Actionability (weight: 0.15)**

Criteria evaluated:
- Pilot study executable as specified: MOSTLY — Equivalence Validation Protocol is sufficient if EC-2 inconsistency is resolved; hallucination rate measurement needs task-category-specific operationalization before execution; calibration protocol needs sample size increase; CI method needs specification
- Go/no-go criteria operationally clear: PARTIALLY — CI criterion ambiguous when pilot power is ~0.17 (will almost certainly not exclude zero); intermediate state (0-20% failure) undefined for pilot data quality criterion
- Full experiment pathway actionable: YES
- Research question recommendations actionable: YES
- Execution feasibility: YES (resolved from I1)

Score assessment: The pilot is substantially more actionable than in I1. Key blockers are: task-category-specific hallucination operationalization, calibration sample increase, CI method specification, EC-2 revision. These are days of work, not weeks. **Score: 0.84**

**Traceability (weight: 0.10)**

Criteria evaluated:
- All evidence cited with source ID: YES
- Evidence summary table complete: YES (21 entries)
- Citation corrections from I1: YES (CV-001-i1, CV-002-i1 corrected)
- Power calculation source: ABSENT (no derivation or citation for 0.40 value)
- McNemar formula citation: PARTIALLY — Agresti §10.1 attribution imprecise (persists from I1)
- Adversarial check provenance: YES (relabeled as "Preliminary Self-Review (pre-I1)")
- Confidence differentiation: YES (resolved from I1)
- Revision log completeness: YES (comprehensive finding-by-finding resolution table)

Score assessment: Traceability substantially improved. Main gaps: power calculation without source, persisting Agresti attribution imprecision. **Score: 0.88**

### Composite Score Calculation

| Dimension | Weight | Score | Weighted |
|-----------|--------|-------|---------|
| Completeness | 0.20 | 0.88 | 0.176 |
| Internal Consistency | 0.20 | 0.78 | 0.156 |
| Methodological Rigor | 0.20 | 0.81 | 0.162 |
| Evidence Quality | 0.15 | 0.87 | 0.131 |
| Actionability | 0.15 | 0.84 | 0.126 |
| Traceability | 0.10 | 0.88 | 0.088 |
| **Composite** | **1.00** | | **0.839** |

**Threshold:** >= 0.95 (C4)
**Band:** REJECTED (< 0.85 — near boundary)
**Verdict:** REJECTED — targeted revision required (H-13)

**Score comparison:**
- I1 composite: 0.771 REJECTED
- I2 composite: 0.839 REJECTED (improvement: +0.068)
- Remaining gap to threshold: 0.111

---

## Consolidated Findings

### All I2 Findings by Severity

| ID | Strategy | Severity | Finding Summary | Dimension |
|----|---------|---------|----------------|-----------|
| SR-002-i2 | S-010 | **Major** | Pilot power stated as ~0.40 but back-calculation yields ~0.17 — materially overestimates pilot power | Methodological Rigor |
| SR-003-i2 | S-010 | **Major** | DSPy mechanism (assertion backtracking) conflated with prompt-level L2-re-injection in generalizability bridge | Evidence Quality |
| DA-001-i2 | S-002 | **Major** | Hallucination rate "source material" undefined for code review, architecture, documentation task categories (3 of 5) | Methodological Rigor |
| DA-002-i2 | S-002 | **Major** | Output scrubbing incomplete: semantic circumlocution ("avoid," "instead," "rather than") not in masking list | Methodological Rigor |
| DA-003-i2 | S-002 | **Major** | Consequence matching (EC-2): valence-inverted consequences ("corrupted"/"remain clean") appear to violate EC-2 literal criterion ("identical consequence text") — protocol inconsistency | Methodological Rigor |
| DA-004-i2 | S-002 | **Major** | Calibration kappa at n=3 pairs is statistically undefined — single disagreement determines pass/fail; gate is operationally unreliable | Methodological Rigor |
| PM-001-i2 | S-004 | **Major** | Hallucination rate kappa fails for non-research task categories due to ambiguous "source material" definition | Methodological Rigor |
| PM-002-i2 | S-004 | **Major** | Semantic circumlocution in LLM outputs degrades blinding despite vocabulary masking | Methodological Rigor |
| PM-003-i2 | S-004 | **Major** | Calibration kappa at n=3 operationally unworkable; delays pilot launch | Methodological Rigor |
| PM-004-i2 | S-004 | **Major** | CI-based stopping criterion creates disputed pilot verdict when power (~0.17) makes CI-exclusion unlikely | Internal Consistency |
| RT-001-i2 | S-001 | **Major** | GO criterion (CI excludes zero) inconsistent with pilot purpose (calibration); not meeting CI criterion ≠ pilot failure | Internal Consistency |
| RT-003-i2 | S-001 | **Major** | EC-2 criterion permits valence-inverted consequences in example pairs that appear to fail EC-2 as literally written | Methodological Rigor |
| CC-001-i2 | S-007 | **Major** | Power stated as ~0.40 without derivation or citation; apparent violation of P-001 accuracy requirement | Methodological Rigor |
| CC-002-i2 | S-007 | **Major** | CI method for stopping criterion not specified; at small n_discordant, method choice materially affects coverage | Methodological Rigor |
| CV-001-i2 | S-011 | **Major** | Wei et al. (2022) NeurIPS cited for 20-40% discordant proportion range; paper reports accuracy improvements, not discordant proportions | Evidence Quality |
| CV-002-i2 | S-011 | **Major** | Power ~0.40 at n=30 appears materially incorrect per back-calculation | Methodological Rigor |
| FM-001-i2 | S-012 | **Major** | Hallucination rate source material undefined for non-research task categories (RPN 392) | Methodological Rigor |
| FM-002-i2 | S-012 | **Major** | Semantic circumlocution not addressed in output scrubbing (RPN 343) | Methodological Rigor |
| FM-003-i2 | S-012 | **Major** | Calibration kappa at n=3 statistically unreliable (RPN 336) | Methodological Rigor |
| FM-004-i2 | S-012 | **Major** | GO criterion vs. pilot calibration purpose inconsistency (RPN 343) | Internal Consistency |
| FM-005-i2 | S-012 | **Major** | Power calculation incorrect (RPN 288) | Methodological Rigor |
| FM-006-i2 | S-012 | **Major** | EC-2 criterion inconsistent with example pairs (RPN 252) | Methodological Rigor |
| FM-008-i2 | S-012 | **Major** | CI method not specified for stopping criterion (RPN 180) | Methodological Rigor |
| IN-001-i2 | S-013 | **Major** | Hallucination rate fails for 3 of 5 task categories without category-specific source material definition | Methodological Rigor |
| IN-002-i2 | S-013 | **Major** | 90% CI stopping criterion systematically not achievable at n=30 with ~0.17 power | Internal Consistency |
| IN-003-i2 | S-013 | **Major** | Kappa at n=3 produces false-negative calibration failures due to sampling variance | Methodological Rigor |
| IN-004-i2 | S-013 | **Major** | Example pairs fail EC-2 as literally written — recurrence of I1 DA-005 pattern | Methodological Rigor |
| SR-001-i2 | S-010 | **Minor** | Continuity correction arithmetic in sensitivity table: documented as ~268; back-calculation yields ~264 | Internal Consistency |
| SR-004-i2 | S-010 | **Minor** | GO criterion (100% valid output) vs. NO-GO criterion (> 20% failure) creates undefined intermediate state | Internal Consistency |
| SR-005-i2 | S-010 | **Minor** | Score delta rounding inconsistency: revision log says +0.115, comparison table note says +0.116 | Internal Consistency |
| DA-005-i2 | S-002 | **Minor** | C2 vs. C5 pre-specified comparison assumes zero effect (near-infinite n required) — should be removed or justified | Internal Consistency |
| PM-005-i2 | S-004 | **Minor** | C2 vs. C5 pre-specification creates protocol amendment risk | Internal Consistency |
| PM-006-i2 | S-004 | **Minor** | DSPy mechanism gap in generalizability bridge not defensible under external review | Evidence Quality |
| RT-002-i2 | S-001 | **Minor** | WARNING callout creates meta-narrative risk (low-severity, unavoidable) | Evidence Quality |
| RT-004-i2 | S-001 | **Minor** | PROJ-007 "positive framing" scope narrowed from "no negative constraints" to "no PLAN.md negative constraints" without prominent acknowledgment | Evidence Quality |
| CC-003-i2 | S-007 | **Minor** | H-15 self-review documented for pre-I1 only; I2 additions not documented as having been self-reviewed | Methodological Rigor |
| CC-004-i2 | S-007 | **Minor** | Experimental variable scope narrowing (PLAN.md level vs. full session) acknowledged in body but not in comparison premise | Evidence Quality |
| CV-003-i2 | S-011 | **Minor** | Agresti §10.1 attribution for continuity correction formula imprecise (persisted from I1 CC-002) | Traceability |
| IN-005-i2 | S-013 | **Minor** | Wei et al. π_d grounding weaker than presented; reduces but does not eliminate confidence in 0.30 estimate | Evidence Quality |
| FM-007-i2 | S-012 | **Minor** | C2 vs. C5 pre-specified with "near-infinite" required n (RPN 120) | Internal Consistency |
| SM-001-i2 | S-003 | **Minor** | Pilot power source should be cited or range given | Methodological Rigor |
| SM-002-i2 | S-003 | **Minor** | Evidence bridge missing mechanism hypothesis column | Evidence Quality |
| SM-003-i2 | S-003 | **Minor** | PS Integration null finding coverage estimate lacks visible derivation | Traceability |

### Finding Count Summary

| Severity | Count |
|----------|-------|
| Critical | 0 |
| Major | 27 |
| Minor | 16 |
| **Total** | **43** |

### Thematic Clusters

The 27 Major findings cluster into 5 recurring themes:

| Theme | Major Findings | Dimension |
|-------|---------------|-----------|
| T-1: Hallucination rate operationalization (source material undefined for non-research tasks) | DA-001-i2, FM-001-i2, IN-001-i2, PM-001-i2, CV-002-i2 (power) | Methodological Rigor |
| T-2: Pilot stopping criterion vs. calibration purpose inconsistency | RT-001-i2, FM-004-i2, IN-002-i2, PM-004-i2 | Internal Consistency |
| T-3: Calibration kappa at n=3 operationally unreliable | DA-004-i2, FM-003-i2, IN-003-i2, PM-003-i2 | Methodological Rigor |
| T-4: EC-2 criterion vs. example pairs inconsistency | DA-003-i2, FM-006-i2, IN-004-i2, RT-003-i2 | Methodological Rigor |
| T-5: Output scrubbing incomplete (semantic circumlocution) | DA-002-i2, FM-002-i2, PM-002-i2 | Methodological Rigor |
| T-6: Power calculation inaccurate (~0.40 stated, ~0.17 per back-calculation) | SR-002-i2, CC-001-i2, CV-002-i2, FM-005-i2 | Methodological Rigor |

---

## Tournament Summary

### Verdict

**Score: 0.839 REJECTED** (C4 threshold: >= 0.95)
**Band:** Near REVISE/REJECTED boundary (REVISE band: 0.85–0.91)
**Score improvement from I1:** +0.068 (0.771 → 0.839)
**Remaining gap to threshold:** 0.111

### I1 Critical Finding Resolution Verification

All 16 I1 Critical findings are **GENUINELY RESOLVED** in R2. No cosmetic-only resolutions detected. The R2 revision demonstrates substantive engagement with the I1 findings.

### What Improved

The R2 revision represents substantial progress:
- Construct validity failure RESOLVED: hallucination rate now primary metric with full operational definition
- Equivalence validation protocol RESOLVED: 5-criterion checklist, inter-rater requirement, redesigned example pairs
- Output scrubbing protocol RESOLVED: vocabulary masking with "[INSTRUCTION-ECHO]" token (partially — semantic circumlocution gap remains)
- Stopping criterion RESOLVED: CI-based directional test replaces the invalid threshold (partially — CI method unspecified; GO purpose inconsistency remains)
- Multiple comparisons RESOLVED: Bonferroni-Holm declared; confirmatory/exploratory split explicit
- PROJ-007 prompting regime VERIFIED from primary source
- Power analysis for all 7 conditions RESOLVED
- π_d GROUNDED with comparable study references (with citation precision caveat)
- WARNING callout ADDED at document top

### What Remains Unresolved (Remediation Roadmap)

The 27 Major findings cluster into 6 themes, each with a specific remediation action:

**T-1: Hallucination rate source material (DA-001-i2, FM-001-i2, IN-001-i2, PM-001-i2):**
Remediation: Add a "Source Material Operationalization by Task Category" sub-section specifying what constitutes verifiable "source material" for each of the 5 task categories. For code review: the code itself plus language/library documentation explicitly provided in the prompt. For architecture decision: the requirements specification and constraint list provided. For documentation: the technical specification to be documented. This is a targeted addition of ~200 words.

**T-2: Stopping criterion vs. pilot purpose (RT-001-i2, FM-004-i2, IN-002-i2, PM-004-i2):**
Remediation: Add explicit reconciliation text: "The pilot has two GO criteria. Primary GO criterion (calibration purpose): observed π_d falls in the range 0.10 ≤ p_12 + p_21 ≤ 0.50. This criterion alone is sufficient for the pilot's calibration purpose. Secondary GO criterion (directional signal): 90% CI for (p_12 − p_21) excludes zero at 90% confidence. This secondary criterion may not be met at n=30 (power ~0.17), and its non-fulfillment does not constitute a pilot failure. A pilot may return GO on the primary criterion while failing the secondary criterion; the research team proceeds to full experiment with the calibrated π_d and acknowledges no directional signal from the pilot."

**T-3: Calibration kappa at n=3 (DA-004-i2, FM-003-i2, IN-003-i2, PM-003-i2):**
Remediation: Increase calibration sample from n=3 to n=10 pairs. The 10 pairs come from the pre-validated example pool (2 per task category × 5 categories = 10 pairs already specified). This requires no new pairs, only a restatement of the calibration protocol.

**T-4: EC-2 criterion vs. example pairs (DA-003-i2, FM-006-i2, IN-004-i2, RT-003-i2):**
Remediation: Revise EC-2 to explicitly permit valence-inverted consequence matching: "EC-2: Consequence domain — Same consequence domain; valence may be inverted (negative consequence in C2 / positive equivalent in C3 is acceptable). Rater confirms the consequence text addresses the same outcome domain." This makes the protocol consistent with the example pairs.

**T-5: Semantic circumlocution (DA-002-i2, FM-002-i2, PM-002-i2):**
Remediation: Either (a) extend the masking list to include common circumlocutory terms ("avoid," "instead of," "rather than," "alternatively," "in lieu of"), OR (b) add a "Residual Blinding Risk" acknowledgment that semantic echo through circumlocution is an uncontrolled limitation of the vocabulary masking approach.

**T-6: Power calculation (SR-002-i2, CC-001-i2, CV-002-i2, FM-005-i2):**
Remediation: Replace "approximately 0.40" with a verified estimate. Recommended: "McNemar pilot power at n=30, π_d = 0.30, p_12 = 0.20, p_21 = 0.10 is approximately 0.17 (expected discordant pairs n_d ≈ 9; test statistic under H_1: |6−3|/3 = 1.0; power = Φ(1.0 − 1.96) ≈ 0.17). The pilot is intentionally low-powered for calibration, not for confirmation."

**Additional specific fixes:**
- Add CI method specification (recommend Wilson or Agresti-Coull for small n_discordant)
- Remove C2 vs. C5 from pre-specified comparisons or add explicit rationale
- Correct Wei et al. citation: attribute the 20-40% range to the author's inference from Wei et al. data, not as a directly reported value

### Iteration Progression

| Iteration | Score | Band | Critical | Major | Minor |
|-----------|-------|------|----------|-------|-------|
| I1 | 0.771 | REJECTED | 16 | 29 | 11 |
| I2 | 0.839 | Near-REVISE | 0 | 27 | 16 |
| Gap to C4 threshold | 0.111 | — | — | — | — |

The I2 revision eliminated all Critical findings and reduced the score gap by +0.068. The remaining Major findings are concentrated in the experimental protocol specification (Themes T-1 through T-6) and are targeted rather than structural. A focused I3 revision addressing the 6 thematic clusters could close the remaining gap.

### Projected I3 Path

If Themes T-1 through T-6 are fully resolved in I3:
- Methodological Rigor score projects to ~0.91 (from 0.81, given 5 of 6 themes are methodological)
- Internal Consistency score projects to ~0.88 (from 0.78, given 2 themes are consistency failures)
- Completeness score remains ~0.91 (minor CI method addition)
- Evidence Quality projects to ~0.90 (citation precision improvement)
- Actionability projects to ~0.91 (pilot unblocked by T-1 through T-6 resolution)
- Traceability projects to ~0.91 (power calculation sourced)

Projected I3 composite: (0.91×0.20) + (0.88×0.20) + (0.91×0.20) + (0.90×0.15) + (0.91×0.15) + (0.91×0.10) = 0.182 + 0.176 + 0.182 + 0.135 + 0.137 + 0.091 = **0.903**

At 0.903, I3 would remain below the 0.95 C4 threshold, suggesting a fourth iteration may be required. The gap between projected 0.903 and 0.95 suggests that methodological rigor must reach ~0.96+ to achieve the composite threshold given the dimension weights. This requires not just resolving the 6 thematic clusters but achieving near-complete methodological rigor.

**Key insight:** The document is structurally sound but the experimental protocol specification has recurring precision gaps that accumulate across the 6 themes. The fundamental challenge is that the pilot design involves multiple interacting moving parts (hallucination rate measurement, equivalence validation, blinding, stopping criterion, calibration) where each part adds methodological rigor requirements. Reaching 0.95 requires each component to be fully specified and internally consistent.

---

## Execution Statistics

- **Total Findings:** 43
- **Critical:** 0
- **Major:** 27
- **Minor:** 16
- **Protocol Steps Completed:** 10 of 10
- **I1 Critical Findings Genuinely Resolved:** 16/16
- **New Issues Introduced by Revision:** 27 Major, 16 Minor (none Critical)
- **Composite Score:** 0.839 REJECTED (I1: 0.771; improvement: +0.068)
- **Iterations remaining before C4 ceiling (5 max per PROJ-014 PLAN.md):** 3
