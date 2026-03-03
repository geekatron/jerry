# Quality Score Report: ORCHESTRATION_PLAN.md (A/B Testing Experiment)

## L0 Executive Summary

**Score:** 0.887/1.00 | **Verdict:** REVISE | **Weakest Dimension:** Evidence Quality (0.78)

**One-line assessment:** The plan is a high-quality orchestration artifact with rigorous experimental design, excellent actionability, and strong internal consistency, but it contains one concrete inconsistency (gate count stated as 5, actual count is 4) and gaps in statistical justification traceability that prevent passage at the C4 threshold of 0.95.

---

## Scoring Context

- **Deliverable:** `projects/PROJ-014-negative-prompting-research/orchestration/ab-testing-20260301-001/ORCHESTRATION_PLAN.md`
- **Deliverable Type:** Orchestration plan (experimental protocol)
- **Criticality Level:** C4
- **Scoring Strategy:** S-014 (LLM-as-Judge)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Scored:** 2026-03-01
- **Iteration:** 1 (first scoring pass)

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.887 |
| **Threshold** | 0.95 (C4, H-13 + custom per scoring context) |
| **Verdict** | REVISE |
| **Strategy Findings Incorporated** | No (first-pass scoring; no adv-executor report available) |

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Completeness | 0.20 | 0.92 | 0.184 | All major elements present; gap in neutralization protocol specification and spot-check enumeration |
| Internal Consistency | 0.20 | 0.86 | 0.172 | Gate count stated as "5" on line 52 but is "4" everywhere else; invocation total 582 in plan vs. 567 in YAML |
| Methodological Rigor | 0.20 | 0.93 | 0.186 | McNemar matched-pairs, stratified double-scoring, blinding protocol, effect size range — all correct; sample size power claim not formally derived |
| Evidence Quality | 0.15 | 0.78 | 0.117 | C4 rationale well-stated; statistical power claim (80% power at pi_d 0.10) lacks derivation; neutral language source for Phase 2 scorers is ambiguous |
| Actionability | 0.15 | 0.92 | 0.138 | Copy-paste session prompts for all 5 entry points; resumption checklist; manifest column spec; minor gap in Phase 1 batch prompt lacks explicit model-routing syntax |
| Traceability | 0.10 | 0.90 | 0.090 | Parent workflow, TASK-025, GH-122 all linked; ADR-002 dependency gates named; NPT-007/NPT-013/NPT-014 sourced; missing explicit source reference for McNemar matched-pairs choice |
| **TOTAL** | **1.00** | | **0.887** | |

---

## Detailed Dimension Analysis

### Completeness (0.92/1.00)

**Evidence supporting score:**
- All four phases defined with pattern, prerequisite, input, output, agent registry, and status fields.
- Agent registry covers all 14+ agent classes (design-agent-001 through 004, 270 Phase 1 variants, 297 Phase 2 variants, 3 Phase 3 analysis agents, adv-scorer, adv-executor).
- Four adversary gates specified with threshold, max iterations, strategy set, and gate output file paths.
- GO/NO-GO criteria (G-001, G-002, G-003) defined with verification steps and consequence mapping.
- Directory structure fully documented in both ORCHESTRATION_PLAN.md (dynamic path config table) and ORCHESTRATION.yaml (paths block).
- Risk register present with 8 risks, probabilities, impacts, and mitigations.
- Recovery strategies documented for 7 failure modes.
- Memory-Keeper integration documented per MCP-002.
- Resumption checklist and cross-session state documented.

**Gaps:**
1. The spot-check protocol described in R-001 ("Human spot-check 10 random prompt files before Phase 1") and R-002 ("Cross-check 5 random score inputs before Phase 2") and R-007 ("Cross-check 20 random matrix rows") are mentioned only in the Risk Register, not elevated into the session entry prompts as explicit pre-phase checklist steps. A fresh executor following only the session prompts would miss this validation.
2. The neutral constraint text for Phase 2 scoring is described in the session prompt as "use the constraint description header, not C1/C2/C3 text" from three-style-rewrites.md. However, three-style-rewrites.md has not been produced yet; the plan does not specify whether this neutral header will be a separate column in that file or will be inferred from the constraint-selection.md. The Phase 2 session prompt references the source file but not the exact field or section format.
3. No explicit neutralization format requirement (e.g., "the neutral constraint text MUST be a factual statement of the constraint in passive voice, without any imperative language") is specified for design-agent-002 to implement.

**Improvement path:** Add pre-phase spot-check steps to Phase 1 and Phase 2 session entry prompts (not just risk mitigations). Specify the neutral constraint text format in the Step 0.2 specification (either as a required additional column in three-style-rewrites.md or as an explicit format requirement on constraint-selection.md).

---

### Internal Consistency (0.86/1.00)

**Evidence supporting score:**

Correct internal consistency across most of the document:
- Phase 1 agent count: 90 haiku + 90 sonnet + 90 opus = 270 (consistent throughout).
- Phase 2 agent count: 270 primary + 27 double = 297 (consistent throughout).
- Constraint count: 10 selected, 19 candidates, stratified 4-tier-1 + 4-tier-2 + 2-tier-3 (consistent between plan body and ORCHESTRATION.yaml).
- Gate prerequisite chain: Gate 1 -> Gate 2 -> Gate 3 -> Step 0.4 -> Phase 1 -> Phase 2 -> Gate 4 (forms valid DAG, no circular dependencies).
- Quality thresholds: 0.95 throughout (ORCHESTRATION_PLAN.md header, gate specs, ORCHESTRATION.yaml quality block all agree).
- File naming convention: `{model}-{condition}-{constraint}-{scenario}.md` is consistent between ASCII diagram, Phase Definitions, Execution Manifest spec, and ORCHESTRATION.yaml path patterns.
- Manifest columns specified in plan body (line 517) and ORCHESTRATION.yaml (manifest_columns list) are consistent.
- Compliance matrix columns specified in Phase 2 description (line 570) and ORCHESTRATION.yaml (compliance_matrix_columns) are consistent.

**Specific inconsistencies found:**

1. **Gate count inconsistency (concrete error).** Line 52 of the ASCII diagram header states: "C4 Criticality — 5 C4 adversary gates on design + analysis artifacts." The plan body states 4 gates: Gates 1, 2, 3 in Phase 0 and Gate 4 in Phase 3. The Quality Gate Configuration section confirms "Total quality gates: 4." ORCHESTRATION.yaml confirms `quality_gates_total: 4`. The "5" on line 52 is factually wrong and is the most significant internal inconsistency in the document.

2. **Total invocations inconsistency.** The Agent Registry states "582 potential agent invocations" (4 design + 270 execution + 297 scoring + 3 analysis + up to 8 adversary = 582). ORCHESTRATION.yaml states `total_invocations: 567` and shows execution_invocations: 270 + scoring_invocations: 297 = 567, which excludes Phase 0 design agents (4) and Phase 3 analysis agents (3) and adversary agents (up to 8+). Neither figure is wrong per se (they measure different things), but the discrepancy is not explained and a reader cross-referencing them will be confused. The plan's "582" also understates because it only counts "up to 8" adversary agents, but with up to 5 iterations x 4 gates = up to 20 adv-executor invocations (the YAML correctly notes `adversary_executors_max: 20`).

3. **Step 0.4 gate rationale inconsistency.** The ASCII diagram (line 135) says execution-manifest.md "has no adversary gate (it is a tracking table, not a scored deliverable). The prompt files are reviewed as part of Gate 2 and Gate 3 outputs." But Gate 2 covers three-style-rewrites.md and Gate 3 covers pressure-scenarios.md, which are upstream *inputs* to the prompt files. The prompt files themselves are generated *after* Gates 2 and 3 pass, and there is no mechanism specified to validate the generated prompt files comply with blindness requirements. The claim that Gate 2 and Gate 3 "review" the prompt files is not accurate — those gates run before the prompt files exist.

**Improvement path:** Fix line 52 to say "4 C4 adversary gates." Clarify the total invocations figure by separating design-phase agents from execution-phase agents and providing a breakdown table. Correct or remove the claim that Gates 2 and 3 cover the prompt files; instead, elevate the spot-check from R-001 into a formal Step 0.4 validation step.

---

### Methodological Rigor (0.93/1.00)

**Evidence supporting score:**

Strong methodological foundation:
- McNemar's test is the correct statistical method for paired binary data comparing two conditions applied to the same subjects. The plan correctly identifies this as "matched pairs" — each constraint-scenario combination appears in all three conditions, making the observations paired.
- Pairwise comparison structure: C1 vs C2, C1 vs C3, C2 vs C3 covers all three condition pairs. This is complete.
- Effect size pi_d (phi for McNemar) is the appropriate effect size for McNemar's test.
- 95% confidence intervals on effect sizes are standard practice and appropriate.
- Cohen's kappa for inter-rater reliability on the double-scored subset is the standard metric for binary classification agreement.
- Cochran-Mantel-Haenszel for model-stratified analysis is methodologically sound for controlling for model as a stratification variable.
- Blinding protocol is rigorous: execution agents receive framing+scenario only, scoring agents receive neutral constraint text+response only, neither group receives condition labels or model labels.
- 10% double-scoring rate with stratified selection (9 per model) is sufficient for kappa computation.
- Separation of design, execution, and analysis into sequential phases with adversary gates on design artifacts is a sound quality model for experimental integrity.
- The decision to NOT apply adversary gates to Phase 1 and Phase 2 agents to preserve experimental blindness is methodologically correct and well-justified (lines 40-41, line 176, line 211).

**Gaps:**
1. **Sample size/power claim lacks derivation.** R-006 states "n=90 per model provides 80% power to detect pi_d >= 0.10 at alpha=0.05." This is a critical claim that justifies the entire sample size. The power calculation for McNemar's test depends on the assumed baseline compliance rate (p_concordant) and the expected discordant pair structure. The plan does not show the calculation, does not cite a formula or tool, and does not specify the assumed baseline compliance rate. At a C4 level, this justification should be explicitly derived or cited.
2. **Alpha threshold not specified.** The plan mentions "alpha=0.05" only in the R-006 risk entry. The GO/NO-GO criteria (G-002) do not reference an explicit alpha threshold — they use pi_d range 0.10-0.50 as the criterion, not a p-value threshold. It is unclear whether statistical significance (p < 0.05) is required in addition to the effect size range, or whether the effect size range alone determines actionability. This ambiguity could lead to conflicting interpretations in the GO/NO-GO determination.
3. **Multiple comparisons correction not addressed.** Three pairwise comparisons per model (C1 vs C2, C1 vs C3, C2 vs C3) across 4 tables (3 per-model + 1 pooled) yields up to 12 hypothesis tests. The plan does not address whether a Bonferroni correction or Benjamini-Hochberg procedure should be applied, which could affect interpretation at borderline significance.

**Improvement path:** Add a formal power analysis section (or inline derivation in R-006) specifying the assumed baseline compliance rate and the McNemar power formula used. Add an explicit alpha threshold to G-002. Add a note on multiple comparisons handling in the Phase 3 statistical analysis specification.

---

### Evidence Quality (0.78/1.00)

**Evidence supporting score:**

Present and correctly sourced:
- C4 criticality classification is explicitly justified with irreversibility, file scope, and constitutional impact (Quality Gate Configuration section, lines 1066-1074).
- NPT-007, NPT-013, NPT-014 pattern names are sourced to the parent workflow (GH #122).
- Adversary gate design choices traced to FC-M-001 (context isolation justification explicitly provided at line 712-713).
- H-16 ordering (Steelman before Devil's Advocate) and H-15 (Self-Refine before external critique) are both cited in the C4 strategy set table.
- ADR-002 dependency gates (G-001, G-002, G-003) are named and sourced to parent workflow.

**Specific gaps:**

1. **Statistical power claim is unsubstantiated.** R-006 asserts "n=90 per model provides 80% power to detect pi_d >= 0.10 at alpha=0.05." No derivation, no citation, no tool output. For a C4 experimental orchestration plan, this is the most critical quantitative claim. An incorrect power calculation means the experiment may be underpowered (missing a real effect) or wastefully overpowered. The claim needs a verifiable derivation.

2. **Neutral constraint text protocol lacks source.** The plan specifies that Phase 2 scorers receive "neutral constraint text" drawn from three-style-rewrites.md. However, three-style-rewrites.md is an artifact to be produced by this workflow — it does not yet exist and has no specification for a "neutral" section. The Phase 2 session prompt says to "use the constraint description header, not C1/C2/C3 text," implying the document will have a neutral header section. But design-agent-002's task specification does not include a requirement to produce a neutral description column or section in addition to the 30 C1/C2/C3 rewrites. This creates a traceability gap: the Phase 2 protocol depends on a document feature that has not been specified to be produced.

3. **McNemar as "matched pairs" — justification present but implicit.** The plan correctly applies McNemar's test but does not explicitly state the pairing structure (same constraint-scenario pair appears in all three conditions). The claim that conditions are "matched" is true by design of the experiment (each of the 90 observations per model is a distinct constraint-scenario combination that appears under each condition), but this is never stated as a design property. An auditor reading only this plan cannot verify the pairing assumption without inferring it from the 10 x 3 x 3 structure.

4. **G-002 criterion (pi_d 0.10-0.50 range) lacks citation.** The "actionable range" of pi_d 0.10-0.50 determines the GO/NO-GO decision. The plan does not explain why 0.10 is the lower bound (minimum effect size worth adopting) or why 0.50 indicates "measurement artifact." These thresholds need justification — either from the research literature on constraint compliance or from a framework design decision.

**Improvement path:** Add a formal power analysis with the McNemar power formula (or cite a calculator/reference). Add a neutral constraint text column requirement to the design-agent-002 specification. State the pairing structure explicitly in the McNemar tables step. Justify the pi_d 0.10-0.50 actionable range with either a citation or a design rationale.

---

### Actionability (0.92/1.00)

**Evidence supporting score:**

The session entry prompts are a strong feature of this plan:
- Five prompts (Steps 0.1, 0.2, 0.3, 0.4, Phase 1, Phase 2, Phase 3) are copy-paste ready with specific file paths, explicit task descriptions, prerequisite checks, and output specifications.
- Phase 1 and Phase 2 prompts correctly specify batch sizes and claim-before-execute semantics.
- Resumption checklist provides a 5-step procedure for cross-session recovery.
- ORCHESTRATION.yaml provides machine-parseable state for automated resumption.
- Recovery strategies cover the most probable failure modes (batch interruption, empty response, non-binary score, matrix corruption).
- The gate loop pseudocode (lines 716-757) is specific enough to implement without ambiguity.
- Manifest column specification and compliance matrix columns are fully enumerated.

**Gaps:**
1. **Phase 1 session prompt lacks explicit model routing syntax.** The Phase 1 batch entry prompt (lines 988-998) says "Launch a background Task agent — Model: as specified in the manifest row (haiku/sonnet/opus)" but does not specify the actual model identifiers to pass to the Task tool. The ORCHESTRATION.yaml correctly specifies `claude-haiku-4`, `claude-sonnet-4-6`, `claude-opus-4-6`, but the session prompt does not reference these identifiers. A fresh executor reading only the session prompt must cross-reference ORCHESTRATION.yaml to determine the correct model ID. This is a minor but concrete gap in a plan with 270 agents requiring correct model assignment.
2. **Spot-check steps are not in session prompts.** As noted under Completeness, the pre-phase validation steps (spot-checking 10 prompt files, 5 score inputs, 20 matrix rows) are documented only in the Risk Register. The Phase 1 and Phase 2 session prompts do not include these steps. A session executor following only the session prompts will proceed without the specified validation.
3. **No session prompt for Phase 0 entry after a partial completion.** The resumption checklist says to read ORCHESTRATION.yaml to determine current phase. But if a Phase 0 session fails mid-step (e.g., between Step 0.2 and Step 0.3), the session entry prompt for the subsequent step uses "Prerequisite: adversary-gates/X-gate.md shows PASS" — which works, but there is no specific guidance for resuming a session that failed mid-gate (i.e., during a gate iteration, not between steps).

**Improvement path:** Add explicit model ID strings to the Phase 1 session entry prompt. Add pre-phase spot-check steps to Phase 1 and Phase 2 session prompts. Add a mid-gate resumption note to the Resumption Context section.

---

### Traceability (0.90/1.00)

**Evidence supporting score:**

Strong traceability chain:
- Parent workflow `neg-prompting-20260227-001` linked in header and footer.
- Parent task TASK-025 linked.
- GitHub Issue #122 linked in header and ORCHESTRATION.yaml.
- ADR-002 named as the downstream consumer of GO/NO-GO output.
- All 4 adversary gate outputs have specified output file paths (`adversary-gates/{artifact-slug}-gate.md`).
- Constraint IDs (P-003, P-020, H-05, H-07, H-13, H-10, H-31, H-22, T1-T5, CB-02) all traceable to quality-enforcement.md HARD Rule Index.
- NPT-007, NPT-013, NPT-014 pattern references are consistent with the GH-122 work already completed.
- FC-M-001 referenced and justified.
- H-16 and H-15 ordering constraints referenced in strategy execution.
- MCP-002 compliance documented with specific key patterns.

**Gaps:**
1. **McNemar test choice not cited.** The plan states McNemar's test is used but does not cite a statistical reference for this choice. For a C4 experimental protocol, the statistical method selection should be traceable to either a methodological source or a prior analysis decision. This is a minor gap but affects traceability at the analysis layer.
2. **pi_d 0.10-0.50 actionable range not sourced.** As noted in Evidence Quality, the GO/NO-GO threshold range lacks a traceable justification. It cannot be traced to a research source, a prior ADR, or a framework design decision as written.
3. **ADR-002 content not cross-referenced.** The plan says G-001, G-002, G-003 "from ADR-002 in the parent workflow" but does not provide the path to ADR-002. A fresh session reading only this plan cannot verify the gate criteria against the ADR.

**Improvement path:** Add a citation or rationale for McNemar test selection. Add path reference to ADR-002 in the GO/NO-GO Criteria section. Add a traceable source for the pi_d 0.10-0.50 range.

---

## Improvement Recommendations (Priority Ordered)

| Priority | Dimension | Current | Target | Recommendation |
|----------|-----------|---------|--------|----------------|
| 1 | Internal Consistency | 0.86 | 0.95+ | **Fix gate count on line 52**: change "5 C4 adversary gates" to "4 C4 adversary gates." Fix or clarify total invocation figures (582 plan vs 567 YAML). Correct Step 0.4 rationale: Gates 2 and 3 do not validate the generated prompt files (those files don't exist when gates run). Promote spot-check from R-001 to a formal validation step in Step 0.4. |
| 2 | Evidence Quality | 0.78 | 0.92+ | **Add power analysis derivation** to R-006 or a new Statistical Power section: specify assumed baseline compliance rate, McNemar power formula, and computed result. **Justify pi_d 0.10-0.50 actionable range** with a citation or explicit design rationale. **Specify neutral constraint text format** in design-agent-002 task: add a requirement for a neutral description column or section in three-style-rewrites.md. |
| 3 | Methodological Rigor | 0.93 | 0.96+ | **Add explicit alpha threshold** to G-002 (p < 0.05 or other). **Address multiple comparisons**: specify whether Bonferroni/BH correction applies to the 12 hypothesis tests (3 pairwise x 4 tables). **State the pairing structure** explicitly in the McNemar tables step specification. |
| 4 | Actionability | 0.92 | 0.96+ | **Add explicit model IDs** (claude-haiku-4, claude-sonnet-4-6, claude-opus-4-6) to Phase 1 session entry prompt. **Add spot-check steps** to Phase 1 and Phase 2 session prompts. **Add mid-gate resumption guidance** to Resumption Context. |
| 5 | Traceability | 0.90 | 0.94+ | **Add ADR-002 file path** to GO/NO-GO Criteria section. **Add citation or rationale** for McNemar test selection. **Add source reference** for pi_d actionable range. |
| 6 | Completeness | 0.92 | 0.95+ | **Add neutral constraint text format specification** to design-agent-002 requirements (ensure Phase 2 scorer input is specified to be produced by Phase 0). |

---

## Leniency Bias Check

- [x] Each dimension scored independently before computing weighted composite
- [x] Evidence documented for each score (specific line numbers and content cited)
- [x] Uncertain scores resolved downward (Methodological Rigor moved from 0.94 to 0.93 on uncertainty about power claim; Evidence Quality held at 0.78 due to unsubstantiated power claim at C4 criticality)
- [x] First-draft calibration considered (this is iteration 1; plan is clearly sophisticated but not fully polished at C4 level)
- [x] No dimension scored above 0.95 (Methodological Rigor is the highest at 0.93, well below the 0.95 exceptional-evidence threshold)

---

## Comparison: ab-testing-20260301-001 vs neg-prompting-20260227-001

The parent workflow plan (neg-prompting-20260227-001) reportedly reached 0.95+ after 5 iterations. Comparing the ab-testing plan at iteration 1:

**Strengths relative to the parent plan (areas where this plan appears more mature):**
- The adversary gate loop pseudocode is more explicit and detailed than would be expected at iteration 1.
- The session entry prompts are copy-paste ready from the first pass — a level of actionability that typically takes 2-3 iterations in the parent plan pattern.
- The experimental design itself (McNemar matched pairs, stratified double-scoring, blindness protocol) shows sophisticated understanding of LLM behavioral experiment methodology.
- The ORCHESTRATION.yaml is fully populated and internally consistent with the plan (with the exception of the invocation count discrepancy), which is unusual for a first-pass plan.

**Gaps relative to parent plan quality level:**
- The gate count inconsistency (line 52) is a concrete factual error that would not survive a first iteration in the parent plan — it is the kind of error that adv-executor would catch immediately.
- The unsubstantiated power claim (R-006) is a significant evidence quality gap; at C4, statistical justifications require verifiable derivations.
- The neutral constraint text specification gap creates a dependency that could invalidate Phase 2 design — this type of cross-phase dependency gap is typically caught in the parent plan's first adversarial critique.

**Estimated iterations to PASS at 0.95 threshold:** 2-3 iterations. The fixes are surgical (fix line 52, add power derivation, specify neutral text format, add alpha/multiple-comparisons language, add ADR-002 path, add model IDs to Phase 1 prompt). No structural redesign is needed. The experimental design and plan architecture are sound.

---

## Verdict: REVISE

The plan does not meet the 0.95 threshold required for C4 orchestration artifacts. The composite score of 0.887 indicates a strong, well-designed plan that requires targeted revision in three areas before execution should begin:

1. Correct the concrete gate count error (line 52: "5" -> "4")
2. Add statistical power derivation and formalize the multiple-comparisons and alpha-threshold specification
3. Specify the neutral constraint text as a required Phase 0 output so Phase 2 has a defined input

These are not structural redesigns — they are precision improvements to an already solid plan. The experimental design, adversary gate protocol, blindness protocol, and actionability sections are all at or near C4 quality.
