# Quality Score Report: HARD Rule Budget Upper Boundary Derivation

## Scoring Context

- **Deliverable:** projects/PROJ-007-agent-patterns/orchestration/agent-patterns-20260221-001/adversary/hard-rule-budget/hard-rule-budget-upper-boundary-derivation.md
- **Deliverable Type:** Analysis
- **Criticality Level:** C4 (Critical) -- governance constraint affecting constitutional enforcement architecture
- **Scoring Strategy:** S-014 (LLM-as-Judge)
- **SSOT Reference:** .context/rules/quality-enforcement.md
- **Scored By:** adv-scorer (claude-opus-4-6)
- **Scored:** 2026-02-21
- **Iteration:** 1 (first score, initial draft)

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0 Executive Summary](#l0-executive-summary) | Score, verdict, and one-line assessment |
| [Score Summary](#score-summary) | Metric table |
| [Dimension Scores](#dimension-scores) | Weighted scoring matrix |
| [Detailed Dimension Analysis](#detailed-dimension-analysis) | Per-dimension evidence, gaps, improvement paths |
| [Improvement Recommendations](#improvement-recommendations-priority-ordered) | Priority-ordered actions |
| [Scoring Impact Analysis](#scoring-impact-analysis) | Gap-to-threshold breakdown |
| [Leniency Bias Check](#leniency-bias-check-h-15-self-review) | Anti-leniency verification |

---

## L0 Executive Summary

**Score:** 0.90/1.00 | **Verdict:** REVISE | **Weakest Dimension:** Methodological Rigor (0.85)

**One-line assessment:** Strong analytical work with well-sourced multi-constraint derivation, but methodological gaps in L2 marker analysis accuracy, absence of sensitivity analysis, and an underdeveloped implementation path prevent clearing the elevated 0.95 threshold. Targeted revisions in 3 dimensions should close the gap.

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.90 |
| **Threshold** | 0.95 (user-specified, above standard H-13 0.92) |
| **Verdict** | REVISE |
| **Strategy Findings Incorporated** | No (first scoring pass) |
| **Prior Score (if re-scoring)** | N/A |
| **Improvement Delta** | N/A |

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Severity | Evidence Summary |
|-----------|--------|-------|----------|----------|------------------|
| Completeness | 0.20 | 0.91 | 0.182 | Minor | Five constraints analyzed with synthesis; missing sensitivity analysis and L2 marker operational nuance |
| Internal Consistency | 0.20 | 0.93 | 0.186 | -- | Constraint analyses and synthesis table are internally coherent; minor tension in Implementation Path math |
| Methodological Rigor | 0.20 | 0.85 | 0.170 | Minor | Sound multi-constraint framework; L2 analysis conflates operational vs. documentation markers; no sensitivity analysis on key assumptions |
| Evidence Quality | 0.15 | 0.92 | 0.138 | -- | 12 evidence items with confidence ratings; academic citations are real and correctly attributed; one medium-confidence source treated as strongly corroborative |
| Actionability | 0.15 | 0.88 | 0.132 | Minor | Clear recommendation and consolidation table; implementation path has an unresolved arithmetic problem (29 > 25) acknowledged but not resolved |
| Traceability | 0.10 | 0.93 | 0.093 | -- | Evidence Index with 12 entries; each constraint traces to named sources; all claims link to evidence IDs |
| **TOTAL** | **1.00** | | **0.90** | | |

---

## Detailed Dimension Analysis

### Completeness (0.91/1.00) -- Minor

**Evidence:**

The deliverable covers five independent constraints (Token Budget, L2 Re-injection, Instruction-Following Research, Signal Quality, Rule Conflict Probability) and provides a synthesis section that identifies which constraint is binding. All twelve sections in the navigation table are present and populated. The Problem Statement clearly frames the "why" (retroactive ceiling with no derivation, impending exhaustion, prior silent breach). The Recommendation section includes a two-tier allocation model with specific counts. The Implementation Path provides a 7-step sequence.

Three evidence points justifying 0.91:
1. All 12 declared sections are present and substantive (no stubs).
2. Five independent constraint analyses span quantitative, empirical, and semi-quantitative methods -- a comprehensive approach.
3. The Problem Statement articulates 4 specific motivating concerns with supporting evidence (commit hash, rule counts, prior breach).

**Gaps:**

1. **No sensitivity analysis.** The derivation depends on several key assumptions (60% HARD-specific content ratio in Constraint 1, ~410 tokens/rule mean, 50 tokens per L2 marker in Constraint 2). No analysis of how the derived ceiling changes if these assumptions vary by +/-20%. For a C4 governance deliverable, this is a notable omission.

2. **L2 markers in non-quality-enforcement.md files not addressed.** The deliverable correctly identifies that the engine reads only `quality-enforcement.md`, but L2-REINJECT markers also exist in 8 other rule files (architecture-standards.md, coding-standards.md, testing-standards.md, mandatory-skill-usage.md, markdown-navigation-standards.md, mcp-tool-standards.md, python-environment.md, skill-standards.md). These markers are loaded into L1 context via auto-loaded rules and serve as structural emphasis even if not processed by the engine. The deliverable does not discuss whether these additional markers provide any enforcement value or whether the Tier A/B model should account for them.

3. **No discussion of L3-L5 enforcement contributions.** The enforcement architecture has 5 layers; the derivation focuses on L1 and L2 but does not analyze how L3 (deterministic gating), L4 (output inspection), or L5 (commit/CI verification) compensate for L1/L2 limitations. This is relevant because an L1-only rule with L3 or L5 coverage may be more effectively "HARD" than the derivation suggests.

**Improvement Path:**

Add a "Sensitivity Analysis" subsection to the Synthesis section showing how the derived ceiling shifts under different assumptions. Add a paragraph in Constraint 2 addressing L2-REINJECT markers in non-quality-enforcement.md files. Add a brief "L3-L5 Compensating Controls" discussion to the Synthesis section.

---

### Internal Consistency (0.93/1.00)

**Evidence:**

The five constraint analyses produce independent ceilings that converge, and the Synthesis table (lines 252-258) correctly identifies L2 Re-injection as binding for "truly HARD" rules and Instruction-Following as binding for total count. The "two ceilings emerge" conclusion (lines 260-264) logically follows from the constraint data. The recommendation's 25-rule total and 12/13 Tier A/B split are consistent with the Constraint 2 finding of "~14 rules with full L2 protection" and the Constraint 3/4 convergence on "20-25 total."

Three evidence points justifying 0.93:
1. Synthesis table binding constraint designations ("Yes"/"No"/"Corroborative") correctly match each constraint's derived ceiling relative to others.
2. The two-tier model in the Recommendation flows directly from the Constraint 2 finding of partial L2 coverage and the Constraint 3 finding of domain-partitioned rules.
3. Evidence confidence ratings (High/Medium/Emerging) are applied consistently and the Medium-rated E-008 is correctly labeled as "agent judgment" rather than empirical evidence.

**Gaps:**

1. **Implementation Path arithmetic inconsistency.** Steps 1-5 (lines 291-295) show consolidation to 25 then addition of 4 new rules reaching 29 -- which is "over the 25 ceiling by 4." The deliverable acknowledges this (line 295) and offers three resolution paths (lines 298-300). However, the Implementation Path table (lines 318-326) lists "Add PROJ-007 rules (H-32..H-35)" as Step 6 without resolving which resolution path to use. This is a minor tension: the Recommendation section identifies the problem but the Implementation Path does not resolve it, leaving the reader with an incomplete action plan. This is not a contradiction per se -- it is acknowledged as an open question -- but it weakens the internal coherence of the implementation plan.

**Improvement Path:**

Resolve the 29 > 25 gap in the Implementation Path by either (a) adding a Step 5.5 that consolidates H-32..H-35, or (b) explicitly selecting one of the three resolution options and updating the step table accordingly.

---

### Methodological Rigor (0.85/1.00) -- Minor

**Evidence:**

The five-constraint framework is a sound analytical approach. Using multiple independent constraints to triangulate an upper boundary is methodologically appropriate. The distinction between "binding" and "corroborative" constraints (Synthesis table) correctly applies the concept of a binding constraint from optimization theory. The separation of "quantitative" vs. "semi-quantitative" vs. "empirical" analysis types in the Methodology table (line 64) is methodologically transparent.

**Gaps:**

1. **L2 coverage claim requires qualification.** The deliverable states "only 32% of HARD rules (10/31) have L2 protection" (line 131) and "Engine reads from quality-enforcement.md only" (line 125). While confirmed correct by the engine source code, the L2-REINJECT markers in other rule files (8 additional files with markers covering H-07..H-12, H-20..H-21, H-22, H-23..H-24, H-25..H-30, and MCP rules) are loaded by Claude's L1 auto-loading mechanism and appear in context with the L2-REINJECT HTML comment structure. While the prompt reinforcement engine does not process them, their presence in auto-loaded context provides a form of emphasis that the derivation does not account for. This distinction between "engine-processed L2" and "structurally emphasized L1" should be addressed to avoid overstating the vulnerability of non-quality-enforcement.md rules.

2. **Absence of sensitivity analysis is a methodological gap.** The Constraint 1 analysis depends on a 60% HARD-specific content ratio (line 97: "Estimating HARD-rule-specific content at ~60% of file tokens"), which directly determines whether the token budget ceiling is 18 or 30+ rules. This is an assumption, not a measurement. Similarly, the Constraint 2 analysis uses "~50 tokens each" per additional L2 marker (line 137), which is stated without derivation. Without sensitivity analysis, the reader cannot assess the robustness of the 25-rule conclusion.

3. **Instruction-following research application.** The ManyIFEval and AGENTIF citations (Constraint 3) are real and correctly attributed, but the deliverable's distinction between "31 HARD rules in rule files" and "5-8 simultaneously active constraints per interaction" (lines 165-166) is introduced as an assertion without measurement. How many rules are actually "active" in a typical coding interaction vs. a governance interaction? The claimed 5-8 number is plausible but unverified.

4. **Combinatorial analysis (Constraint 5) is elementary.** N(N-1)/2 pairwise interactions is a standard combinatorial formula, but the analysis does not account for rule clustering (rules in the same domain file are more likely to interact than rules across domains) or the actual observed conflict rate. The three observed conflicts cited (lines 240-242) are anecdotal rather than systematic.

**Improvement Path:**

(1) Add sensitivity analysis for the 60% ratio and 50-token/marker assumptions. (2) Qualify the L2 coverage claim by distinguishing engine-processed L2 from structurally-emphasized L1. (3) Provide measurement or structured estimation of "simultaneously active" rule counts per interaction type. (4) Strengthen the conflict analysis with a systematic scan of rule interactions rather than anecdotal examples.

---

### Evidence Quality (0.92/1.00)

**Evidence:**

The Evidence Index (lines 332-345) contains 12 items, each with Source, Content, and Confidence rating. Academic citations are real and correctly attributed: ManyIFEval (arXiv:2509.21051), AGENTIF (arXiv:2505.16944, NeurIPS 2025), Control Illusion (arXiv:2502.15851), Lost in the Middle (TACL 2024). The deliverable correctly identifies these as "High (peer-reviewed)" or "High (NeurIPS Spotlight)."

Three evidence points justifying 0.92:
1. Engine source code claim (E-002) verified against `prompt_reinforcement_engine.py` -- the engine reads only quality-enforcement.md (line 243 of source). This is "High (source code)" confidence and correctly rated.
2. The L2-REINJECT marker inventory (E-003) was verified: quality-enforcement.md contains exactly 8 markers covering 10 H-rules (H-01..H-03, H-05, H-06, H-13..H-15, H-19, H-31). "High (file scan)" is correct.
3. Commit 936d61c (E-010) is cited as "Retroactive ceiling update from 25 to 35 with no justification" rated "High (git evidence)" -- verifiable and appropriate.

**Gaps:**

1. **E-008 confidence rating.** The nse-risk-001 "20-25 sweet spot" is rated "Medium (agent judgment)" which is honest. However, in Constraint 4 the derivation uses this as a key corroborative source alongside three other independent analyses. The text states "The convergence of three independent analyses on the 20-25 range is significant" (line 215), but the nse-risk-001 source is not truly independent -- it was produced within the same project, potentially by the same model, and may share epistemic biases with this derivation. This weakens the "independent corroboration" claim slightly.

2. **ADOR citation (E-011).** Rated "Emerging (formal literature)" with an OpenReview reference but no arXiv ID or full citation. This is the weakest evidence item and is used to support the "attention dilution" claim. While appropriate to flag as "Emerging," the citation format is less rigorous than the other academic sources.

**Improvement Path:**

(1) Qualify the "independence" of the nse-risk-001 corroboration. (2) Provide a full citation for ADOR including authors and year, or downgrade its influence on the conclusion.

---

### Actionability (0.88/1.00) -- Minor

**Evidence:**

The Recommendation section provides a concrete two-tier allocation model (Tier A: 12 constitutional rules with L2, Tier B: 13 operational rules L1-only, Total: 25). The consolidation table (lines 282-286) identifies specific rules to merge with before/after counts. The Implementation Path (lines 318-326) provides a 7-step sequence with criticality classifications per step.

**Gaps:**

1. **Unresolved arithmetic gap.** The "What This Means for PROJ-007's H-32..H-35" section (lines 289-300) identifies that adding 4 new rules after consolidation yields 29 rules -- 4 over the proposed 25 ceiling. Three resolution options are listed but none is selected. For a C4 deliverable that will drive governance changes, this open question is a significant actionability gap. The implementer must make this decision themselves.

2. **No Tier A/B classification of existing rules.** The recommendation proposes a two-tier model but does not classify the current 25 (post-consolidation) rules into Tier A vs. Tier B. This is listed as Implementation Step 3, but without even a draft classification, the recommendation is incomplete. The reader cannot validate whether 12 rules fit into Tier A or whether the split is workable.

3. **Consolidation feasibility unvalidated.** The claim that H-25..H-30 "could consolidate to 2 rules" and H-07..H-09 "could consolidate to 1 rule" is asserted but not validated. Are there any governance implications of compound rules? Does the compound-rule pattern preserve the specificity needed for L5 verification? These questions are not addressed.

4. **No timeline or sequencing constraints.** The 7-step Implementation Path has no timeline, dependency arrows, or sequencing constraints beyond the step numbers. Steps 4 and 5 (update quality-enforcement.md and update L2 markers) have a logical dependency that should be explicit.

**Improvement Path:**

(1) Select one of the three resolution options for the 29 > 25 gap and update the Implementation Path accordingly. (2) Provide a draft Tier A/B classification of the 25 post-consolidation rules. (3) Add a brief feasibility assessment of the compound-rule consolidation. (4) Add dependency arrows or sequencing notes to the Implementation Path.

---

### Traceability (0.93/1.00)

**Evidence:**

The Evidence Index (lines 332-345) provides 12 entries with ID, Source, Content, and Confidence columns. Each constraint section references its data sources by name (e.g., "From ADR-EPIC002-002 and current rule file measurements" for Constraint 1). The Problem Statement traces the retroactive ceiling to a specific commit hash (936d61c). The prior breach is traced to specific rule IDs (H-25..H-30). The Synthesis table traces each constraint's derived ceiling back to the corresponding constraint section.

Three evidence points justifying 0.93:
1. Each of the five constraint sections has an explicit Data subsection with tabulated parameters, values, and sources -- enabling the reader to verify claims against the cited sources.
2. The Evidence Index uses a consistent E-NNN ID scheme that could be cross-referenced (though the constraint sections use source names rather than E-IDs, requiring the reader to map between the two).
3. The Recommendation traces its 25-rule ceiling to "three independent evidence sources" and names them explicitly (lines 43).

**Gaps:**

1. **No E-ID cross-references in constraint sections.** The Evidence Index uses E-001..E-012, but the constraint sections reference sources by name (e.g., "ADR-EPIC002-002") rather than by E-ID. This requires the reader to manually map between the constraint text and the Evidence Index. Direct E-ID citations within the analysis text would strengthen traceability.

2. **No link to the actual ADR-EPIC002-002 file path.** The ADR is referenced by name throughout but its repository path is never provided, making it harder to locate for verification.

**Improvement Path:**

(1) Add E-ID references inline within the constraint analysis sections (e.g., "From ADR-EPIC002-002 [E-001]"). (2) Add file paths for key references in the Evidence Index.

---

## Improvement Recommendations (Priority Ordered)

| Priority | Dimension | Current | Target | Recommendation |
|----------|-----------|---------|--------|----------------|
| 1 | Methodological Rigor | 0.85 | 0.95 | Add sensitivity analysis for the 60% HARD-content ratio and 50-token/marker assumptions, showing ceiling range under +/-20% variation. Qualify L2 coverage by distinguishing engine-processed L2 from structurally-emphasized L1 markers. Provide structured estimation of simultaneously-active rule counts. |
| 2 | Actionability | 0.88 | 0.95 | Resolve the 29 > 25 gap by selecting a resolution option and updating the Implementation Path. Add a draft Tier A/B classification. Add consolidation feasibility assessment. |
| 3 | Completeness | 0.91 | 0.95 | Add sensitivity analysis subsection. Address L2 markers in non-quality-enforcement.md files. Add brief L3-L5 compensating controls discussion. |
| 4 | Evidence Quality | 0.92 | 0.95 | Qualify independence of nse-risk-001 corroboration. Provide full ADOR citation. |
| 5 | Internal Consistency | 0.93 | 0.95 | Resolve Implementation Path arithmetic by selecting a resolution option. |
| 6 | Traceability | 0.93 | 0.95 | Add E-ID cross-references inline within constraint sections. Add file paths for key references. |

**Implementation Guidance:**

The highest-impact revision is adding sensitivity analysis (addresses Priority 1 and 3 simultaneously). The second-highest impact is resolving the Implementation Path arithmetic gap (addresses Priority 2 and 5). These two changes alone would likely push the composite above 0.95. The remaining improvements (evidence qualification, traceability cross-referencing) are lower effort and can be addressed in parallel.

---

## Scoring Impact Analysis

### Dimension Impact on Composite

| Dimension | Weight | Score | Weighted Contribution | Gap to 0.95 Target | Weighted Gap |
|-----------|--------|-------|----------------------|-------------------|--------------|
| Completeness | 0.20 | 0.91 | 0.182 | 0.04 | 0.008 |
| Internal Consistency | 0.20 | 0.93 | 0.186 | 0.02 | 0.004 |
| Methodological Rigor | 0.20 | 0.85 | 0.170 | 0.10 | 0.020 |
| Evidence Quality | 0.15 | 0.92 | 0.138 | 0.03 | 0.005 |
| Actionability | 0.15 | 0.88 | 0.132 | 0.07 | 0.011 |
| Traceability | 0.10 | 0.93 | 0.093 | 0.02 | 0.002 |
| **TOTAL** | **1.00** | | **0.90** | | **0.050** |

**Interpretation:**

- **Current composite:** 0.90/1.00
- **Target composite:** 0.95/1.00 (user-specified threshold)
- **Total weighted gap:** 0.05
- **Largest improvement opportunity:** Methodological Rigor (0.020 weighted gap available -- 40% of the total gap)
- **Second-largest opportunity:** Actionability (0.011 weighted gap -- 22% of the total gap)
- **Combined top-2 opportunity:** 0.031 (62% of total gap). Addressing both could yield composite ~0.93-0.94; all 6 dimensions need some improvement to reach 0.95.

### Verdict Rationale

**Verdict:** REVISE

**Rationale:**

The weighted composite of 0.90 falls below the user-specified 0.95 threshold. Under the standard H-13 threshold of 0.92, this deliverable would also score REVISE (0.90 < 0.92). No individual dimension has a Critical finding (all >= 0.85). The deliverable is strong analytical work with a well-structured multi-constraint framework, appropriate evidence sourcing, and a clear recommendation. The gaps are addressable: sensitivity analysis (Methodological Rigor), resolution of the implementation arithmetic (Actionability/Internal Consistency), and nuanced treatment of L2 markers across the codebase (Completeness/Methodological Rigor). A single targeted revision pass should be sufficient to reach the 0.95 threshold.

---

## Leniency Bias Check (H-15 Self-Review)

- [x] Each dimension scored independently (no cross-dimension influence)
- [x] Evidence documented for each score (specific quotes/references with line numbers)
- [x] Uncertain scores resolved downward (Methodological Rigor: considered 0.87 but identified 4 distinct gaps -> 0.85; Actionability: considered 0.90 but unresolved arithmetic gap -> 0.88)
- [x] First-draft calibration considered (this is a first draft; 0.90 composite is within the typical 0.85-0.92 range for strong first drafts of complex analyses)
- [x] No dimension scored above 0.95 without exceptional evidence (highest scores: Internal Consistency 0.93, Traceability 0.93 -- both below 0.95)
- [x] High-scoring dimensions verified (> 0.90):
  - **Internal Consistency (0.93):** (1) Synthesis table correctly reflects constraint analysis findings. (2) Two-tier model flows logically from Constraint 2 partial coverage finding. (3) Evidence confidence ratings applied consistently.
  - **Evidence Quality (0.92):** (1) 12 evidence items with structured confidence ratings. (2) Academic citations verified as real and correctly attributed. (3) Source code verification (E-002) confirmed against actual engine code.
  - **Traceability (0.93):** (1) Evidence Index with 12 structured entries. (2) Each constraint section has explicit Data tables with sources. (3) Problem Statement traces to specific commit hash.
- [x] Low-scoring dimensions verified:
  - **Methodological Rigor (0.85):** 4 specific gaps documented (L2 conflation, no sensitivity analysis, unverified simultaneous-active claim, elementary combinatorial analysis)
  - **Actionability (0.88):** 4 specific gaps documented (unresolved 29>25, no Tier A/B draft, unvalidated consolidation, no timeline)
  - **Completeness (0.91):** 3 specific gaps documented (no sensitivity analysis, L2 non-QE markers, no L3-L5 discussion)
- [x] Weighted composite matches mathematical calculation: (0.91*0.20)+(0.93*0.20)+(0.85*0.20)+(0.92*0.15)+(0.88*0.15)+(0.93*0.10) = 0.182+0.186+0.170+0.138+0.132+0.093 = 0.901 -> rounded to 0.90
- [x] Verdict matches score range (0.90 < 0.95 threshold -> REVISE)
- [x] Improvement recommendations are specific and actionable (each tied to specific content additions with estimated impact)

**Leniency Bias Counteraction Notes:**

1. **Methodological Rigor downward adjustment.** Initially scored 0.87 based on the sound multi-constraint framework. Revised downward to 0.85 after identifying that the L2 analysis conflates engine-processed L2 markers with structurally-emphasized L1 markers (a methodological distinction the derivation should have made), and that the absence of sensitivity analysis is a meaningful gap for a C4 governance deliverable.

2. **Actionability downward adjustment.** Initially scored 0.90 based on the clear recommendation and consolidation tables. Revised downward to 0.88 after recognizing that the unresolved 29 > 25 arithmetic gap in the Implementation Path leaves the core governance question (how to fit PROJ-007 rules within the new ceiling) unanswered.

3. **Completeness considered at 0.93 initially.** Revised to 0.91 after identifying that a C4 deliverable should include sensitivity analysis and should address the L3-L5 enforcement layers that partially compensate for L1/L2 limitations.

4. **Evidence Quality held at 0.92 despite strong evidence index.** The nse-risk-001 independence concern and incomplete ADOR citation prevent scoring higher. Considered 0.93 but the epistemic bias concern with nse-risk-001 as "corroborative" evidence is a real quality gap.

---

*Score Report Version: 1.0.0*
*Template: S-014 (LLM-as-Judge)*
*SSOT: `.context/rules/quality-enforcement.md`*
