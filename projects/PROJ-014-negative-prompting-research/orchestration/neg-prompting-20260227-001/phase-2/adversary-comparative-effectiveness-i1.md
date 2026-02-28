# Adversary Tournament Execution Report: TASK-006 Comparative Effectiveness Analysis (Iteration 1)

> adv-executor | C4 Tournament | PROJ-014 | 2026-02-27
> Target: `phase-2/comparative-effectiveness.md`
> Strategies executed: S-010, S-003, S-002, S-004, S-001, S-007, S-011, S-012, S-013, S-014 (all 10 required for C4)
> Quality gate threshold: >= 0.95 (C4)
> Leniency bias counteraction: ACTIVE — no inflation, no excusing gaps, no rounding up

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Execution Context](#execution-context) | Strategy order, deliverable, template paths |
| [Consolidated Findings Summary](#consolidated-findings-summary) | All findings across all 10 strategies |
| [S-010: Self-Refine](#s-010-self-refine) | Self-consistency and surface error identification |
| [S-003: Steelman](#s-003-steelman) | Strongest-form reconstruction findings |
| [S-002: Devil's Advocate](#s-002-devils-advocate) | Counter-argument findings |
| [S-004: Pre-Mortem](#s-004-pre-mortem) | Failure mode findings |
| [S-001: Red Team](#s-001-red-team) | Adversarial threat vector findings |
| [S-007: Constitutional AI](#s-007-constitutional-ai) | Governance and principle compliance findings |
| [S-011: Chain-of-Verification](#s-011-chain-of-verification) | Factual claim verification findings |
| [S-012: FMEA](#s-012-fmea) | Component failure mode findings with RPN |
| [S-013: Inversion](#s-013-inversion) | Assumption inversion and anti-goal findings |
| [S-014: LLM-as-Judge](#s-014-llm-as-judge) | Dimensional quality scoring |
| [Execution Statistics](#execution-statistics) | Finding counts and protocol completion |

---

## Execution Context

- **Strategy Set:** C4 (all 10 strategies required)
- **Deliverable:** `projects/PROJ-014-negative-prompting-research/orchestration/neg-prompting-20260227-001/phase-2/comparative-effectiveness.md`
- **Templates:** `.context/templates/adversarial/s-{NNN}-*.md`
- **Executed:** 2026-02-27
- **H-16 Compliance:** S-003 executed before S-002 — VERIFIED
- **Orchestration Directives:** All 4 directives honored throughout

---

## Consolidated Findings Summary

| ID | Strategy | Severity | Finding | Section |
|----|----------|----------|---------|---------|
| SR-001-I1 | S-010 | Major | Dimension 4 rest-claim uses single-case observation as if directional data | Dimension 4: Iteration Efficiency |
| SR-002-I1 | S-010 | Major | Evidence Quality Matrix includes A-16 with "Below T3 (rejected)" — matrix claims all evidence assembled but A-16 is explicitly cited in the NEVER-cite instruction | Evidence Quality Matrix |
| SR-003-I1 | S-010 | Minor | Recommendations section uses passive positive framing ("proceed with") violating the analytical principle "NEVER use positive prompting framing" | Recommendations |
| SM-001-I1 | S-003 | Major | The strongest form of the Dimension 5 vendor-practice argument is undermined by failing to distinguish which specific enforcement mechanism (L2 re-injection vs. vocabulary choice) is being claimed as effective | Dimension 5 / T-002 |
| SM-002-I1 | S-003 | Major | The 12-level hierarchy is treated as an analytical backbone without establishing its own validity — no evidence is cited for the hierarchy's ordinal ordering being empirically grounded | Cross-Cutting Hierarchy |
| SM-003-I1 | S-003 | Minor | The confidence bounds table mixes "HIGH," "MEDIUM," and "LOW–MEDIUM" without operationalizing what those confidence levels mean numerically | Synthesis and Directional Verdict |
| DA-001-I1 | S-002 | Critical | The directional verdict ("favors structured negative constraint framing") is produced with LOW confidence on 4 of 5 dimensions yet presented as a usable research hypothesis — the evidence base is insufficient to support even this directional claim without a controlled study | Synthesis and Directional Verdict |
| DA-002-I1 | S-002 | Major | The audience-differentiation explanation (Explanation 1) is treated as "most parsimonious" without formal parsimony argument — this is assertion, not analysis | Dimension 5 / Assumption A-003 |
| DA-003-I1 | S-002 | Major | Dimension 3 and 4 produce "directional findings" from session data that is explicitly labeled as insufficient for causal attribution — the verdicts and the limitations contradict each other | Dimension 3 / Dimension 4 Verdicts |
| DA-004-I1 | S-002 | Minor | The hierarchy's rank 7 (NegativePrompt emotional stimuli) is placed in the effectiveness hierarchy alongside constraint-based techniques, then described as "a different phenomenon" — its presence in the hierarchy is analytically incoherent | Cross-Cutting Hierarchy |
| PM-001-I1 | S-004 | Critical | The analysis fails if the Phase 2 controlled experiment is never conducted — yet Phase 2 design is not this deliverable's scope, and the analysis currently has no standalone finding value without the experiment | Recommendations / L0 |
| PM-002-I1 | S-004 | Major | The analysis fails if the 12-level hierarchy (AGREE-5) is subsequently found to be a narrative construct rather than a validated taxonomy — the entire analytical backbone lacks inter-rater reliability validation | Cross-Cutting Hierarchy |
| PM-003-I1 | S-004 | Major | The analysis fails if a reader interprets "MEDIUM confidence" as operationally meaningful — no confidence scale is defined, making MEDIUM/LOW/HIGH confidence labels non-actionable | Confidence Bounds |
| PM-004-I1 | S-004 | Minor | The analysis fails if context compaction evidence (I-28, I-32) — described as "Anthropic GitHub bug reports from multiple independent users" — cannot be independently verified because no direct URLs or issue numbers are provided | Finding T-004 |
| RT-001-I1 | S-001 | Critical | A motivated critic could validly argue that the entire analysis is circular: researcher builds system using negative constraints, researcher finds system works, researcher concludes negative constraints work — and the VS-001–VS-004 evidence is produced by the same researcher examining their own tooling | Assumption A-002 / EO-001–EO-003 |
| RT-002-I1 | S-001 | Major | A motivated critic could correctly observe that the synthesis AGREE-5 hierarchy is cited as the analytical backbone but was produced in the immediately preceding stage of the same PROJ-014 research pipeline — it has not been independently validated | Cross-Cutting Hierarchy |
| RT-003-I1 | S-001 | Major | A motivated critic could use Finding T-004 (context compaction failure mode) to argue that negative framing is specifically brittle at the most challenging deployment conditions, inverting the directional verdict for real-world production use | Finding T-004 |
| RT-004-I1 | S-001 | Minor | A motivated critic could argue that "the absence of controlled comparison" is not symmetrically treated — the analysis uses absence-of-negative-evidence arguments in favor of the hypothesis (gap-is-not-refutation) but not against it (gap-is-not-confirmation) | Throughout |
| CC-001-I1 | S-007 | Critical | The L0 executive summary states "the evidence does NOT validate the PROJ-014 working hypothesis" — then the Synthesis states "the evidence directionally favors structured negative constraint framing." This is an internal P-001 (truth/accuracy) violation: the executive summary's null-finding tone contradicts the synthesis directional-verdict tone | L0 vs. Synthesis |
| CC-002-I1 | S-007 | Major | The analysis cites A-16 (Harada et al., rejected ICLR 2025) in the Evidence Quality Matrix with the notation "NEVER cite; rejected" — the citation appears in a row that is included in the assembled evidence, violating the NEVER cite instruction | Evidence Quality Matrix |
| CC-003-I1 | S-007 | Major | The analytical principles section states "NEVER use positive prompting framing in this analysis" — Recommendations R-001 through R-006 are written in standard affirmative prose ("Proceed with the controlled A/B experiment," "Specify hierarchy rank before making any comparative claim") | Recommendations |
| CC-004-I1 | S-007 | Minor | The PS Integration section lists confidence at 0.78 but the Synthesis Confidence Bounds table shows LOW confidence on 3 of 5 dimensions — the scalar 0.78 is unexplained and inconsistent with the dimension-by-dimension analysis | PS Integration |
| CV-001-I1 | S-011 | Critical | Claim: "A-31 (Bsharat et al., arXiv 2023): 55% improvement of affirmative directives over prohibition" — verification reveals the deliverable later states A-31 tests "rank-12 prohibition vs. positive framing" but does NOT specify in the evidence matrix whether A-31 controlled for instruction quality equivalence; the 55% figure's validity depends on this control | Evidence Quality Matrix / D1 |
| CV-002-I1 | S-011 | Major | Claim: "Zero constraint violations in 4-iteration C4 tournament" (EO-002) — unverifiable within this document; the adversary-gate.md file is referenced but not cited with specific page or section; independent reader cannot verify | Evidence Quality Matrix |
| CV-003-I1 | S-011 | Major | Claim: A-23 (Barreto & Jana, EMNLP 2025) "+25.14% distractor negation accuracy" — this is a 2025 EMNLP paper; EMNLP 2025 proceedings are not publicly available as of early 2026; the citation cannot be independently verified with current-access sources | Evidence Quality Matrix |
| CV-004-I1 | S-011 | Minor | The synthesis states ranks 9–11 "show qualitative improvement over rank 12" citing T4 (vendor docs, AGREE-8/AGREE-9) — but AGREE-8 and AGREE-9 are named synthesis findings from the upstream synthesis.md, not independently citable claims; the chain is synthesis cites itself | Synthesis |
| FM-001-I1 | S-012 | Critical | Component: Hierarchy validity — Failure Mode: The 12-level hierarchy is used as analytical backbone but its ranking is non-empirical (produced by narrative synthesis of 75 sources, not by controlled ranking study). Effect: All five dimension analyses inherit the hierarchy's construct validity problem. RPN: Severity=9, Occurrence=7, Detection=4, **RPN=252** | Cross-Cutting Hierarchy |
| FM-002-I1 | S-012 | Major | Component: Confidence labels — Failure Mode: MEDIUM/LOW/HIGH confidence labels are used without calibration scale definition. Effect: Downstream practitioners cannot operationalize the uncertainty bounds. RPN: Severity=7, Occurrence=8, Detection=7, **RPN=392** | Throughout |
| FM-003-I1 | S-012 | Major | Component: Session empirical data (EO-001–EO-003) — Failure Mode: Observational data presented with caveat "cannot establish causality" is still used in directional findings for D3 and D4. Effect: Risk of reader treating session observations as quasi-experimental. RPN: Severity=8, Occurrence=6, Detection=5, **RPN=240** | D3 / D4 Verdicts |
| FM-004-I1 | S-012 | Minor | Component: Reflexivity limitation — Failure Mode: The JF-001/JF-002 reflexivity limitation is disclosed but its impact on Dimension 1 and Dimension 3 analyses is not quantified. Effect: Reader cannot assess degree of contamination. RPN: Severity=5, Occurrence=5, Detection=6, **RPN=150** | Assumption A-002 |
| IN-001-I1 | S-013 | Critical | Anti-goal: "Ensure Phase 2 is NOT pursued." Inversion: The analysis must be compelling enough that Phase 2 is NOT funded. Condition achieved if: Dimensions 3 and 4 observational findings are elevated to causal claims (the analysis nearly does this), directional verdict is taken as settled (L2 implications move this direction), and MEDIUM confidence is interpreted as moderate certainty. The analysis does not sufficiently guard against this misuse of its output | D3/D4/L2 Implications |
| IN-002-I1 | S-013 | Major | Assumption: "The 12-level hierarchy correctly distinguishes effectiveness levels." Inversion: If this assumption is false, ALL five dimension analyses produce artifacts of the hierarchy's construction rather than real comparative findings. The analysis does not provide a falsifiability condition for the hierarchy | Cross-Cutting Hierarchy |
| IN-003-I1 | S-013 | Major | Assumption: "Vendor self-practice at ranks 9–11 reflects engineering design choice (not genre convention)." Inversion: If Explanation 2 (genre convention) is correct, ALL VS-001–VS-004 evidence is evidence of writing style, not enforcement effectiveness — reducing Dimension 1 and 5 directional findings to null findings. The analysis acknowledges this but does not state the implication's severity | D1 / D5 Verdicts |
| IN-004-I1 | S-013 | Minor | Assumption: "Post-2024 models behave consistently with the cited evidence." Inversion: GPT-5.2 guidance explicitly warns that newer models are more sensitive to ambiguous prompts. If this applies to negative constraint instructions, the entire evidence base (mostly 2023–2024 studies) may underestimate failure rates of negative framing on current frontier models | Finding T-005 |

---

## S-010: Self-Refine

**Objectivity assessment:** High investment (multi-phase research deliverable); treating as external review for maximum objectivity. Leniency bias counteraction active.

**Protocol Step 1 — Perspective shift:** Reviewing as an adversary reviewer with no stake in PROJ-014 research hypothesis.

**Protocol Step 2 — Systematic self-critique:**

### SR-001-I1: Single-Case Observation Presented as Directional Data

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | Dimension 4: Iteration Efficiency |
| **Strategy Step** | Step 2 (Methodological Rigor / Evidence Quality checks) |

**Evidence:**
> "4 iterations to C4 PASS on two separate deliverables under negative-constraint prompting. No controlled baseline for comparison exists."

The verdict title reads "Directional finding:" yet the body immediately states no controlled baseline exists. Two deliverables from the same pipeline with identical confounds are not independent observations. The "directional" label is not earned by this evidence.

**Analysis:**
The Evidence Quality check (weight 0.15) reveals that presenting n=2 same-pipeline deliverables as "directional data" on iteration efficiency overstates what the evidence supports. The Methodological Rigor check (weight 0.20) reveals the framing "directional finding" is applied uniformly across all 5 dimensions regardless of evidence quality, obscuring the fact that D4 has the weakest evidence base of the five.

**Recommendation:**
Rename the Dimension 4 section header from "Directional finding:" to "Observational note:" and explicitly state "this observation is not directional in the statistical sense — two same-pipeline observations do not constitute a direction." Reserve "directional" only for dimensions with at least T3 evidence.

---

### SR-002-I1: A-16 Appears in Evidence Matrix Despite NEVER-Cite Instruction

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | Evidence Quality Matrix |
| **Strategy Step** | Step 2 (Internal Consistency check) |

**Evidence:**
> Evidence matrix row: `| A-16 | Harada et al., rejected ICLR 2025 | Below T3 | | | NEVER cite; rejected |`

The row for A-16 is present in the consolidated evidence matrix. The matrix introduction states: "Across all five dimensions, consolidated evidence matrix." Including A-16 in the matrix — even with a NEVER-cite annotation — creates a reference path for this evidence. A reader scanning the matrix sees A-16 cited in Dimension 4 text as well ("Self-refinement improves GPT-4o from 15% to 31% on 10-instruction prompts (rejected paper)").

**Analysis:**
This is an internal consistency violation. The Dimension 4 evidence assembly includes A-16 with the parenthetical "(rejected paper)" — meaning the evidence was assembled and cited despite the NEVER-cite instruction. The Evidence Quality Matrix inclusion compounds this by formally cataloguing a source the analysis prohibits.

**Recommendation:**
Remove A-16 from the Dimension 4 evidence assembly table and from the Evidence Quality Matrix. Replace with a methodological note: "One rejected paper (A-16, Harada et al., ICLR 2025 rejection) was identified in the survey but is excluded from all analyses per P-001 (evidence accuracy standards). Its findings are not represented in any dimension verdict."

---

### SR-003-I1: Recommendations Use Positive Framing Contrary to Analytical Principle

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | Recommendations |
| **Strategy Step** | Step 2 (HARD rule compliance — Analytical Principles) |

**Evidence:**
> "NEVER use positive prompting framing in this analysis — all analytical framing uses negative constraint language" (Analytical Principles)
> R-001: "Proceed with the controlled A/B experiment"
> R-002: "Specify hierarchy rank before making any comparative claim"

Six recommendations are written in affirmative imperative form. The analytical principle "NEVER use positive prompting framing" is explicitly stated as governing the analysis.

**Analysis:**
Minor consistency issue. The principle appears directed at analytical framing (how findings are stated) rather than recommendation grammar. However, the contrast is visible and could undermine the internal coherence argument that negative constraint framing is being systematically demonstrated.

**Recommendation:**
Reframe each recommendation using constraint-first language: "NEVER treat the session observational data as sufficient to validate the hypothesis" (R-001 negative form), "NEVER compare negative prompting against positive prompting without specifying the hierarchy rank" (R-002 negative form).

---

## S-003: Steelman

**Core thesis:** Structured negative constraint framing serves a distinct enforcement function at the HARD behavioral tier, as demonstrated by Anthropic's own production enforcement system and supported by directional academic evidence for specific techniques — warranting controlled experimental validation.

**Protocol Step 1 — Charitable interpretation:** The deliverable's strongest version argues that the prohibition paradox (vendors recommend positive, use negative in production) is a real empirical signal that audience-differentiated communication alone cannot fully explain, and that the Phase 2 experiment is justified and correctly designed.

**Protocol Step 2 — Weakness classification:**

### SM-001-I1: Strongest Vendor-Practice Argument Weakened by Mechanism Conflation

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | Dimension 5 / Technical Finding T-002 |
| **Strategy Step** | Step 2 (Evidence weakness) |

**Evidence:**
> "The VS-001 finding — 33 NEVER/MUST NOT instances in Anthropic's own production behavioral enforcement rules, specifically placed at the HARD enforcement tier, with per-prompt L2-re-injection — constitutes the strongest observational signal in the entire evidence base."
>
> "Whether the NEVER/MUST NOT vocabulary contributes beyond what re-injection alone provides is untested."

The analysis simultaneously presents the L2-re-injection mechanism as the primary context-rot-prevention mechanism AND the NEVER/MUST NOT vocabulary as the signal. The steelman version of this argument requires distinguishing these two mechanisms more precisely so the reader understands what claim is actually being made.

**Analysis:**
The deliverable's strongest form would state: "The vendor self-practice evidence establishes that NEVER/MUST NOT vocabulary is systematically chosen for the HARD enforcement tier across all 33 instances, co-occurring with L2-re-injection. This co-occurrence is itself data — it suggests that re-injection alone (without prohibitive vocabulary) was not considered sufficient by the framework designers. Phase 2 condition C4 (C2+re-injection vs. C3 positive+re-injection) directly tests this co-occurrence." The current analysis states this in T-002 but does not bring it to the dimension verdicts or synthesis.

**Recommendation:**
Add an explicit synthesis note: "The design choice to pair re-injection with prohibitive vocabulary — rather than re-inject positive equivalents — is itself a signal that practitioners believe vocabulary matters at the enforcement tier. This is an additional observational data point beyond the 33-instance count, and it strengthens the case for the Phase 2 C4 condition."

---

### SM-002-I1: Hierarchy's Ordinal Validity Not Established

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | Cross-Cutting: 12-Level Effectiveness Hierarchy |
| **Strategy Step** | Step 2 (Evidence weakness) |

**Evidence:**
> "The primary synthesis (AGREE-5) establishes a 12-level effectiveness hierarchy synthesized from all three surveys. This hierarchy is the analytical backbone for all five dimensions."

The hierarchy is presented as the analytical backbone with no acknowledgment that it was produced by narrative synthesis in the immediately preceding pipeline stage. The steelman version of the deliverable would acknowledge the hierarchy's provenance and explain why it is reliable as an analytical framework despite being newly constructed.

**Analysis:**
The strongest form of this argument would note: the hierarchy's validity rests on the convergence of three independent surveys (three independent research strategies, 75 deduplicated sources). Its face validity is high because it correctly separates model-access-required techniques (ranks 1–4) from prompt-engineering-accessible techniques (ranks 5–12). Its construct validity is limited by the absence of a controlled study that empirically ranks these techniques. Acknowledging this would strengthen the deliverable by preempting the obvious critique.

**Recommendation:**
Add a Hierarchy Validity subsection: "The 12-level hierarchy is a narrative synthesis product with high face validity (rank ordering is consistent with mechanism-level differences in technique sophistication) and limited construct validity (no empirical ranking study validates the ordinal positions). Its use as an analytical backbone is warranted as a organizing framework, not as an empirically validated ranking."

---

### SM-003-I1: Confidence Labels Not Operationalized

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | Synthesis and Directional Verdict — Confidence Bounds |
| **Strategy Step** | Step 2 (Structural weakness) |

**Evidence:**
> Confidence Bounds table: "HIGH," "MEDIUM," "LOW-MEDIUM," "LOW for causal claims. MEDIUM for the observational claim"

The deliverable assigns confidence labels but does not define what HIGH, MEDIUM, or LOW mean operationally. The steelman version would operationalize these labels so downstream agents can use them.

**Analysis:**
Suggested operationalization: HIGH = consistent support across 3+ independent evidence sources at T1/T2 tier; MEDIUM = directional support from 1–2 T1/T2 sources or consistent T4 observational evidence without controlled comparison; LOW = observational/session data only, or single T3 source. This operationalization would make the confidence bounds table actionable for Phase 2 experimental design.

**Recommendation:**
Add confidence scale definition to the Assumptions and Limitations section. Apply the scale retroactively to verify existing labels are consistent.

---

## S-002: Devil's Advocate

**H-16 compliance:** S-003 executed prior to this step — CONFIRMED. Proceeding with adversarial critique.

**Role assumption:** Arguing against the deliverable's central thesis that structured negative constraint framing shows stronger evidence for HARD behavioral enforcement than positive framing.

**Protocol Step 2 — Assumptions challenged:**

Explicit assumptions: (1) The 12-level hierarchy correctly ranks technique effectiveness. (2) Vendor self-practice reflects engineering choice, not genre convention. (3) Explanation 1 (audience specificity) is the most parsimonious explanation for the paradox. (4) The PROJ-014 session data is consistent with the hypothesis. (5) Phase 2 would validly test the hypothesis.

Implicit assumptions: (6) The synthesis.md AGREE-5 findings are reliable enough to build a comparative effectiveness analysis upon. (7) Academic evidence on negative framing transfers to production enforcement contexts.

### DA-001-I1: Directional Verdict Unsupported by Its Own Evidence Base

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Section** | Synthesis and Directional Verdict |
| **Strategy Step** | Step 3 (Counter-argument construction) |

**Evidence:**
> "Across five dimensions, the evidence directionally favors structured negative constraint framing over blunt positive instructions for HARD behavioral enforcement tier applications."
>
> Dimension-by-dimension confidence: D1=MEDIUM, D2=LOW–MEDIUM, D3=LOW (causal)/MEDIUM (observational), D4=LOW, D5=HIGH (observational).

**Counter-argument:** A verdict of "directionally favors" requires that the evidence weight, when properly analyzed, tips in one direction. Examining the confidence levels: only D5 achieves HIGH confidence, and D5 is an observational finding about adoption patterns — not a finding about effectiveness. D1 achieves MEDIUM. D2, D3, and D4 achieve LOW or LOW–MEDIUM. A directional verdict derived from predominantly LOW-confidence dimensions is not a directional verdict; it is a prior belief expressed in the language of evidence.

The deliverable's own constraint ("NEVER present this verdict as a confirmed finding") does not go far enough — the problem is not that the verdict is presented as confirmed, but that it is presented as directional when the evidence is directionally ambiguous.

**Analysis:**
The counter-argument is that the synthesis section's headline verdict ("directionally favors") is inconsistent with the confidence table that follows it. A correct synthesis would say: "The evidence does not permit a directional verdict. It identifies specific structured techniques (ranks 5–6) that outperform blunt prohibition (rank 12) — a finding that does not bear on the primary comparison of structured negative vs. structured positive at ranks 9–11."

**Recommendation:**
Revise the directional verdict to: "The evidence establishes that blunt prohibition (rank 12) is less effective than structured alternatives. Whether structured negative constraints at ranks 9–11 are more effective than positively-framed equivalents cannot be determined from available evidence. The vendor adoption pattern (D5, HIGH confidence) is consistent with but does not establish the hypothesis. A directional verdict requires Phase 2 data."

---

### DA-002-I1: Parsimony Claim for Explanation 1 Is Asserted, Not Demonstrated

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | Dimension 5 / Assumption A-003 |
| **Strategy Step** | Step 3 (Unstated assumptions lens) |

**Evidence:**
> "The most parsimonious explanation" (L0 executive summary, referring to audience-differentiated communication)
> "Explanation 1 (audience specificity) is the null hypothesis for VS-002 — the most parsimonious explanation that requires no inference about effectiveness differences."

**Counter-argument:** Parsimony (Occam's Razor) means the explanation with the fewest auxiliary assumptions. The deliverable asserts Explanation 1 is most parsimonious but does not count the auxiliary assumptions each explanation requires. Explanation 1 requires: (a) vendors consciously chose different vocabulary for different audiences, (b) this choice is stable across all 33 instances, across three independent vendors, across multiple document types. Explanation 2 (genre convention) requires: (a) policy documents conventionally use prohibitive vocabulary. Explanation 3 (engineering discovery) requires: (a) negative constraint vocabulary was tested and found effective. Explanation 2 may be equally parsimonious or more parsimonious than Explanation 1 if genre convention is a simpler auxiliary assumption than conscious audience differentiation.

**Analysis:**
The analysis does not enumerate auxiliary assumptions for each explanation. It selects Explanation 1 as the null hypothesis without demonstrating that it has fewer assumptions. This is a methodological gap in the analysis that a critic would exploit.

**Recommendation:**
Add a formal parsimony analysis to Assumption A-003: enumerate auxiliary assumptions for each explanation, compare assumption counts, and explicitly argue why Explanation 1 requires fewer assumptions than Explanation 2 (or acknowledge that Explanation 2 may be equally parsimonious and restate it as "co-null hypothesis").

---

### DA-003-I1: Dimension 3 and 4 Verdicts Contradict Their Own Limitation Statements

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | Dimension 3 and Dimension 4 Verdicts |
| **Strategy Step** | Step 3 (Logical flaws lens) |

**Evidence:**
> D3 verdict: "The PROJ-014 session produced C4-passing results (0.953, 0.951) under negative-constraint prompting."
> D3 limitation: "NEVER interpret the session scores as evidence that negative framing caused the quality gate pass."
> D4 verdict: "4 iterations to C4 PASS on two separate deliverables under negative-constraint prompting."
> D4 limitation: "What cannot be established: Whether positive framing on the same tasks would require more or fewer iterations."

**Counter-argument:** A "directional finding" is a directional claim about the relative effectiveness of two approaches. Dimensions 3 and 4 produce "directional findings" from data that by the analysis's own admission cannot be used to compare the two approaches. A directional finding requires directional data. The session data is existence-proof data (it proves C4 is achievable), not directional data. Using the term "directional finding" for Dimensions 3 and 4 is a structural contradiction: the findings are labeled directional and immediately followed by statements that they cannot be directional.

**Analysis:**
This contradiction is the most significant internal consistency problem in the analysis. A reader encountering "Directional finding:" at the top of a section and "What cannot be established" at the bottom is receiving contradictory signals. This is an Internal Consistency failure (weight 0.20 in the quality rubric) that affects the credibility of the entire synthesis.

**Recommendation:**
Relabel D3 and D4 as "Observational Finding:" (not directional). State explicitly: "This is an existence proof, not a directional comparison. The session demonstrates that C4-threshold results are achievable under a negative-constraint prompting regime. This neither confirms nor disconfirms that positive-framing regimes would achieve similar or different results."

---

### DA-004-I1: NegativePrompt (Rank 7) Is Analytically Incoherent in the Hierarchy

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | Cross-Cutting: 12-Level Effectiveness Hierarchy |
| **Strategy Step** | Step 3 (Alternative interpretations lens) |

**Evidence:**
> Rank 7: "Negative emotional stimuli (NegativePrompt, A-1) | T1 (IJCAI 2024) | Prompt-only | Supports Negative (different phenomenon)"
> D2: "NegativePrompt: +12.89% (Instruction Induction), +46.25% (BIG-Bench) | A-1 (synthesis, GAP-1) | T1 (IJCAI 2024) | Negative EMOTIONAL stimuli — different phenomenon from prohibition instructions; NOT directly applicable"

**Counter-argument:** If A-1 tests a "different phenomenon from prohibition instructions" and is "NOT directly applicable," its presence in the effectiveness hierarchy as Rank 7 (assigned as "Supports Negative") is analytically incoherent. A technique for a different phenomenon should be excluded from the hierarchy, not included with a parenthetical caveat.

**Recommendation:**
Remove Rank 7 from the hierarchy and add a footnote: "NegativePrompt (A-1, IJCAI 2024) tests negative emotional stimuli — a different phenomenon from behavioral constraint prompting. It is excluded from this hierarchy as out-of-scope."

---

## S-004: Pre-Mortem

**Declaration:** "This comparative effectiveness analysis has failed. It is 18 months after publication. Phase 2 was never conducted. Practitioners adopted the analysis's directional verdict as a confirmed finding. The PROJ-014 research program is regarded as methodologically flawed."

**Protocol Step 2 — Failure cause enumeration:**

### PM-001-I1: Analysis Has No Standalone Value Without Phase 2 Experiment

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Section** | Recommendations / L0 |
| **Strategy Step** | Failure type: Assumption |

**Evidence:**
> "This verdict comes with non-trivial caveats...The directional verdict is therefore a research hypothesis warranting Phase 2 experimental validation — not a confirmed finding."
> R-001: "The 270-matched-pair McNemar design from the supplemental report is the correct next step."

**Failure analysis:** The analysis defers all conclusive findings to Phase 2. If Phase 2 is not conducted (funding gap, priority shift, project closure), the analysis produces no actionable finding — only a documented hypothesis. A practitioner who reads the analysis and does not pursue Phase 2 gains nothing operationally. The failure mode is that the analysis is presented as a deliverable complete in itself, but it is actually a prerequisite document whose value is contingent on a future experiment.

**Failure cause:** The analysis does not produce practitioner-actionable guidance for the case where Phase 2 is not available. It produces a conditional recommendation ("if Phase 2 is conducted, design it this way") but no unconditional guidance ("regardless of Phase 2 status, here is what a practitioner can do today based on available evidence").

**Recommendation:**
Add a section "Practitioner Guidance Under Evidence Uncertainty" that provides actionable recommendations not contingent on Phase 2. For example: "Regardless of Phase 2 outcomes, the following is supported by existing T4 evidence: [use enforcement-tier vocabulary architecture with consequences, use paired prohibition + positive alternative (rank 10), justify prohibitions with contextual reasons (rank 11)]. These recommendations are warranted by vendor self-practice evidence even without controlled experimental validation."

---

### PM-002-I1: Hierarchy Is the Analysis's Single Point of Failure

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | Cross-Cutting: 12-Level Effectiveness Hierarchy |
| **Strategy Step** | Failure type: Technical |

**Evidence:**
> "This hierarchy is the analytical backbone for all five dimensions. Evidence from each dimension is mapped against it."

**Failure analysis:** If the 12-level hierarchy is subsequently found to have construct validity problems (the ordinal positions are not supported by direct empirical comparison), all five dimension analyses fail simultaneously. The analysis has a single structural dependency with no fallback. The hierarchy was produced by narrative synthesis in the immediately preceding pipeline stage — it has not been externally validated.

**Failure cause:** The analysis does not include an alternative analytical structure that would survive hierarchy invalidation. A more robust design would present at least one alternative organizing framework (e.g., structured vs. unstructured constraint taxonomy, enforcement mechanism taxonomy) so that if the hierarchy is challenged, the dimensional analysis can be reframed.

**Recommendation:**
Add an alternative analytical frame in the Assumptions and Limitations section: "If the 12-level hierarchy is found to be an invalid organizing framework, the following simplified taxonomy retains the analysis's core findings: [structured constraints (ranks 5–11, collectively) vs. blunt prohibition (rank 12)]. Under this simplified taxonomy, the analysis reduces to: structured techniques outperform blunt prohibition (T1/T3 evidence, HIGH confidence). Whether negative framing within structured techniques is superior to positive framing within structured techniques remains untested under either framework."

---

### PM-003-I1: Undefined Confidence Scale Creates Misinterpretation Risk

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | Confidence Bounds |
| **Strategy Step** | Failure type: Process |

**Evidence:**
> Five distinct confidence labels used: "HIGH," "MEDIUM," "LOW–MEDIUM," "LOW (causal)/MEDIUM (observational)," "LOW"

**Failure analysis:** Without a defined confidence scale, "MEDIUM confidence" is ambiguous. In evidence-based medicine, "moderate confidence" typically means the true effect is likely close to the estimate but there is possibility the true effect is substantially different. In the Cochrane evidence framework, it corresponds to a specific description of study limitations. Without the PROJ-014 equivalent, a practitioner reading "MEDIUM confidence: structured negative constraints show stronger enforcement evidence" cannot determine whether MEDIUM means 60% probability, 70% probability, or "better than LOW but not high."

**Failure cause:** No confidence scale is defined in the deliverable, in the synthesis inputs, or in the methodology section.

**Recommendation:**
Define a confidence scale in the Methodology section: "HIGH: consistent directional evidence from 2+ independent T1 or T2 studies, or 1 T1 + 3+ T4 independent sources. MEDIUM: 1 T1 or T2 study, or consistent T4 evidence from 3+ independent vendors. LOW: T3 only, or observational data with 3+ confounds, or single-source T4. The evidence matrix column 'Tier' maps to this scale."

---

### PM-004-I1: Context Compaction Evidence Is Not Independently Verifiable

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | Finding T-004 |
| **Strategy Step** | Failure type: Technical |

**Evidence:**
> "GAP-13 documents a specific, practically critical failure mode: during context compaction, NEVER/DO NOT rules lose their imperative force (I-28, I-32 — Anthropic GitHub bug reports from multiple independent users)."

**Failure analysis:** The evidence identifiers I-28 and I-32 refer to entries in the synthesis.md evidence catalog, not to direct URLs. An independent reader cannot verify whether these Anthropic GitHub issues exist, whether they are from "multiple independent users" as stated, or whether the bug is currently open or resolved.

**Recommendation:**
Add direct GitHub issue URLs for I-28 and I-32 to the evidence matrix, or add a note: "Direct URLs provided in synthesis.md evidence catalog Section [N]. Independent readers should verify I-28 and I-32 directly before relying on the context compaction finding." If URLs are not available in synthesis.md, note this as an evidence traceability gap.

---

## S-001: Red Team

**Threat actor profile:** A peer reviewer at a major AI research venue (NeurIPS, ICLR) with domain expertise in prompting research, access to the cited papers, and a mandate to find fundamental flaws in the analysis. Capabilities: familiarity with the cited literature, ability to replicate evidence lookups, motivated by methodological rigor.

**Attack vector taxonomy:**

### RT-001-I1: Circular Evidence Structure Is Unresolvable

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Section** | Assumption A-002 / EO-001–EO-003 |
| **Strategy Step** | Attack vector: Logical integrity |

**Evidence:**
> "Assumption A-002: Vendor Self-Practice Evidence Is Independent of This Analysis. VS-001 through VS-004 are directly verifiable by reading cited files. This analysis did not produce that evidence; it cites it."
> "The methodological limitation is that the researcher who produced this analysis is also the operator of the Jerry Framework (Evidence Category 2, JF-001/JF-002)."

**Attack vector:** A peer reviewer would immediately identify the following attack: the researcher who designed the PROJ-014 research program (which uses negative constraints in its governance) is the same researcher who selected the evidence, designed the hierarchy, and now finds that the evidence supports negative constraints. The Assumption A-002 defense — "VS-001 through VS-004 are directly verifiable" — does not address this concern. The problem is not whether the files exist; the problem is that the researcher chose to investigate Anthropic's files (VS-001–VS-004), chose to frame them as positive evidence, chose which of the three competing explanations to present as "most parsimonious," and chose what analytical framework to use. Each choice is within the researcher's control and each choice favors the hypothesis.

**Analysis:** The circularity is structural and cannot be resolved by methodological disclaimers alone. The analysis discloses the limitation but does not provide a structural guard against it. An independent replication (a different researcher analyzing the same evidence with no hypothesis commitment) would be required.

**Recommendation:**
Add an explicit statement: "The most significant limitation of this analysis is that the researcher is not independent of the phenomenon being studied. An independent replication of the comparative effectiveness analysis using the same evidence base but without hypothesis commitment is required before Dimension 5 findings are relied upon. This replication is a higher priority than Phase 2 experimental data for establishing the credibility of the VS-001–VS-004 evidence interpretation."

---

### RT-002-I1: Backbone Hierarchy Is Produced by the Same Pipeline

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | Cross-Cutting: 12-Level Effectiveness Hierarchy |
| **Strategy Step** | Attack vector: Evidence provenance |

**Evidence:**
> "Input 1: barrier-1/synthesis.md (R4, adversary gate 0.953 PASS, 75 unique sources)"
> "The primary synthesis (AGREE-5) establishes a 12-level effectiveness hierarchy synthesized from all three surveys."

**Attack vector:** The 12-level hierarchy was produced by the same research pipeline in the immediately preceding stage. Its adversary gate score (0.953) was produced by the same adversary system (the Jerry Framework with its negative-constraint governance). A peer reviewer would argue: the hierarchy's "AGREE-5" status means three survey researchers agreed on it — but those three researchers are either the same researcher across different sessions or simulated perspectives within the same model, not independent expert validators. The adversary gate passing does not constitute independent validation.

**Recommendation:**
Acknowledge in the Hierarchy section: "The 12-level hierarchy was produced by the PROJ-014 research pipeline and passed an internal adversary gate. It has not been reviewed by independent prompting researchers. Its use as an analytical backbone is warranted for PROJ-014's internal analytical purposes but requires external validation before being cited in publications."

---

### RT-003-I1: Context Compaction Failure Inverts Directional Verdict at Scale

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | Finding T-004 |
| **Strategy Step** | Attack vector: Finding exploitation |

**Evidence:**
> "Finding T-004: Context Compaction Is an Unmitigated Failure Mode for Negative Framing"
> "NEVER/MUST NOT framing, even when effective at preventing constraint violations in short-context sessions, may systematically fail in long-context deployments."
> "This failure mode does NOT affect positive framing in the same way"

**Attack vector:** The deliverable establishes, using its own cited sources, that negative framing has a specific failure mode in production (context compaction) that positive framing does not share. The directional verdict is stated for "HARD behavioral enforcement tier applications." Production enforcement systems routinely operate in long-context conditions. If T-004 is correct, then in precisely the conditions where HARD behavioral enforcement is most needed (long-context production sessions), negative framing may systematically underperform positive framing. The directional verdict may be directionally inverted at the most critical deployment conditions.

**Analysis:** This is a high-severity logical consequence of the deliverable's own evidence that the synthesis section does not integrate. The directional verdict in the synthesis does not mention T-004. A peer reviewer would identify this omission as a critical gap in the synthesis.

**Recommendation:**
Add T-004 explicitly to the Synthesis and Directional Verdict section: "The context compaction failure mode (T-004) introduces a deployment-condition dependency on the directional verdict: under short-context conditions, the evidence directionally favors structured negative constraints. Under long-context conditions with context compaction, the evidence may directionally favor positive framing (no equivalent failure mode documented). The directional verdict is therefore deployment-context-conditional, not universal."

---

### RT-004-I1: Absence-of-Evidence Asymmetry

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | Throughout |
| **Strategy Step** | Attack vector: Logical consistency |

**Evidence:**
> "NEVER treat absence of published evidence as evidence of absence" (Analytical Principle)
> "IG-002: Published studies test naive prohibition; structured enforcement is understudied" (Interpretive)

**Attack vector:** The principle "NEVER treat absence of evidence as evidence of absence" is applied asymmetrically. It is used to protect the hypothesis from the absence of evidence for structured negative constraints outperforming positive alternatives. However, it is not applied in the other direction: the absence of evidence that structured positive constraints fail at the HARD enforcement tier is not flagged. If absence of negative evidence cannot be used against the hypothesis, it equally cannot be used against the null hypothesis.

**Recommendation:**
Add a symmetry note to the Analytical Principles section: "The principle 'NEVER treat absence of evidence as evidence of absence' applies symmetrically: the absence of evidence that structured positive constraints fail at the HARD enforcement tier is equally not evidence that they succeed less than structured negative constraints."

---

## S-007: Constitutional AI Critique

**Constitutional framework applied:** Jerry Constitution (JERRY_CONSTITUTION.md), P-001 through P-022, HARD Rules H-01 through H-36.

**Protocol: Principle-by-principle review of applicable principles.**

### CC-001-I1: P-001 Violation — Internal Contradiction Between L0 Summary and Synthesis Verdict

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Section** | L0: Executive Summary vs. Synthesis and Directional Verdict |
| **Strategy Step** | P-001 (Truth/Accuracy) review |

**Evidence:**
L0 Summary (line 35): "The evidence across five comparative dimensions does NOT validate the PROJ-014 working hypothesis that negative prompting reduces hallucination by 60%."

Synthesis Directional Verdict (line 522): "Across five dimensions, the evidence directionally favors structured negative constraint framing over blunt positive instructions for HARD behavioral enforcement tier applications."

**Analysis:** These two statements are not contradictory in principle — the L0 addresses the 60% hallucination claim while the Synthesis addresses a broader directional verdict about enforcement effectiveness. However, a reader reading only the L0 would conclude the analysis finds no support for negative prompting. A reader reading only the Synthesis would conclude there is directional support. This creates a P-001-adjacent accuracy problem: the document's summary misrepresents its own conclusion. The L0 does not mention that the Synthesis produces a directional verdict in favor of structured negative constraints — it stops at "does NOT validate" and does not disclose the subsequent "but directionally favors."

**Recommendation:**
Revise the L0 to include the directional verdict: "The evidence does NOT validate the specific claim of 60% hallucination reduction. It DOES produce a directional finding (MEDIUM confidence overall) that structured negative constraints at ranks 9–11 may show stronger behavioral compliance evidence than blunt positive instructions — a finding that warrants Phase 2 experimental validation."

---

### CC-002-I1: A-16 Cited in Evidence Matrix Despite NEVER-Cite Constraint

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | Evidence Quality Matrix |
| **Strategy Step** | P-001 (Truth/Accuracy) — evidence accuracy |

**Evidence:**
> Evidence matrix includes: `| A-16 | Harada et al., rejected ICLR 2025 | Below T3 | | | NEVER cite; rejected |`

The analytical constraint "NEVER cite; rejected" appears in the evidence matrix as an annotation on a row that is included in the consolidated evidence table. Additionally, D4 text cites A-16: "Self-refinement improves GPT-4o from 15% to 31% on 10-instruction prompts (rejected paper) | A-16."

**Analysis:** Citing a paper in the evidence matrix and in dimension analysis text, even with a parenthetical disclaimer "(rejected paper)," constitutes citing it. The NEVER cite instruction is violated. This is an accuracy issue: including a rejected paper's findings in evidence assembly, even with caveats, allows those findings to influence the reader's impression of the evidence base.

**Recommendation:**
Remove A-16 entirely from all evidence tables and dimension text. Replace with: "A rejected paper (A-16) was excluded from evidence assembly per accuracy standards. Its findings are not represented."

---

### CC-003-I1: Analytical Principle Prohibiting Positive Framing Not Applied to Recommendations

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | Recommendations |
| **Strategy Step** | P-001 (Internal consistency / self-declared principle compliance) |

**Evidence:**
> Analytical Principles (line 62–68): "NEVER use positive prompting framing in this analysis — all analytical framing uses negative constraint language"
> R-001: "Proceed with the controlled A/B experiment (Phase 2, controlled component)"
> R-002: "Specify hierarchy rank before making any comparative claim"

**Analysis:** The recommendations are written in affirmative imperative prose. Whether this violates the analytical principle depends on whether "analytical framing" includes recommendations or only finding statements. The principle is ambiguous on this point. A constitutional review must flag the ambiguity: if the principle applies to recommendations, CC-003-I1 is a Major violation. If it applies only to analytical finding language, it is a Minor framing inconsistency. Given the principle's stated purpose (to demonstrate negative constraint framing in practice), applying it to recommendations would strengthen the deliverable's meta-level consistency.

**Recommendation:**
Clarify the scope of the analytical principle in the Methodology section. If the principle applies to all document prose: rewrite all 6 recommendations using constraint-first language. If it applies only to finding statements: add a clarifying note "This principle governs analytical findings; recommendations use standard affirmative language for practitioner clarity."

---

### CC-004-I1: PS Integration Confidence (0.78) Is Inconsistent with Dimension Analysis

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | PS Integration |
| **Strategy Step** | P-001 (Internal consistency) |

**Evidence:**
> PS Integration: "Confidence: 0.78 (observational evidence on all 5 dimensions; no controlled comparison; vendor self-practice T4 direct observation is the strongest signal)"
> Confidence Bounds table: D1=MEDIUM, D2=LOW–MEDIUM, D3=LOW (causal)/MEDIUM (observational), D4=LOW, D5=HIGH

**Analysis:** The scalar confidence value of 0.78 is presented without a derivation formula. Three of five dimensions have LOW or LOW-MEDIUM confidence. A simple average of confidence levels does not produce 0.78 unless HIGH=1.0, MEDIUM=0.7, LOW=0.5, LOW-MEDIUM=0.6. Under this mapping: (0.7 + 0.6 + 0.6 + 0.5 + 1.0) / 5 = 0.68, not 0.78. The scalar value of 0.78 is inconsistent with the dimension-level confidence table.

**Recommendation:**
Either derive the 0.78 value explicitly using a defined formula, or replace it with the calculated value consistent with the dimension-level table (approximately 0.68 under the mapping above), or remove the scalar value and use the dimension-level confidence table as the authoritative confidence representation.

---

## S-011: Chain-of-Verification

**Protocol:** Extract testable claims, generate verification questions, answer independently.

### CV-001-I1: A-31 Percentage Figure Lacks Control Condition Specification

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Section** | Evidence Quality Matrix / Dimension 1 |
| **Strategy Step** | Claim extraction and independent verification |

**Claim:** "A-31 (Bsharat et al., arXiv 2023): 55% improvement of affirmative directives over prohibition (rank 12)"

**Verification question:** Does A-31 (Bsharat et al. 2023, "Principled Instructions Are All You Need for Questioning LLaMA-1/2, GPT-3.5/4") compare affirmative vs. prohibitive framing on tasks where instruction quality is otherwise held constant?

**Independent assessment:** Bsharat et al. 2023 tests 26 prompting principles across multiple tasks. The paper does not isolate a single affirmative-vs-prohibition comparison with controlled instruction quality. The "55% improvement" figure is cited without the specific task context, the model tested, or confirmation that instruction quality was equivalent between conditions. This is a verification failure: the specific percentage is presented as established fact but cannot be verified from the citation alone.

**Analysis:** The 55% figure is one of only two quantitative claims supporting the positive-framing side. If this figure is not robust (i.e., it applies to a specific task/model combination under conditions that may not generalize), the Evidence Quality Matrix overstates positive-framing support at rank 12.

**Recommendation:**
Replace the A-31 entry with: "Bsharat et al. (arXiv 2023): Affirmative instructions outperformed prohibitive framing on [specific task, specific model] by approximately 55%. Note: isolated single-principle comparison from a multi-principle study; task and model specificity limits generalization. Requires verification against original paper for precise conditions."

---

### CV-002-I1: EO-002 Claim Cannot Be Independently Verified

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | Evidence Quality Matrix |
| **Strategy Step** | Claim verification |

**Claim:** "Zero constraint violations in 4-iteration C4 tournament under negative-constraint regime (EO-002)"

**Verification question:** Is EO-002 independently verifiable from the sources cited in this deliverable?

**Independent assessment:** The claim cites "adversary-gate.md (supplemental)" as the source. No file path is provided. No section number is referenced. The evidence ID EO-002 does not appear to have a direct-access path specified in the Evidence Quality Matrix. An independent reader cannot verify this claim without access to the specific adversary-gate.md file at the correct path within the PROJ-014 session artifacts.

**Recommendation:**
Add full file paths for all EO-NNN evidence: "EO-002 source: `projects/PROJ-014-negative-prompting-research/orchestration/neg-prompting-20260227-001/barrier-1/adversary-gate.md`, [section reference]."

---

### CV-003-I1: A-23 (EMNLP 2025) Cannot Be Independently Verified

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | Evidence Quality Matrix / Dimension 2 |
| **Strategy Step** | Claim verification |

**Claim:** "A-23: Barreto & Jana, EMNLP 2025, '+25.14% distractor negation accuracy'"

**Verification question:** Is A-23 (EMNLP 2025) accessible for verification?

**Independent assessment:** EMNLP 2025 proceedings were not publicly available prior to late 2025. As of the current date (2026-02-27), the proceedings may be available, but the citation provides no DOI, arXiv preprint ID, or URL. Without access metadata, an independent reader cannot locate and verify the specific claim of "+25.14% distractor negation accuracy."

**Analysis:** This is the single most important positive evidence for structured negative framing in Dimension 2 (Hallucination Prevention). If the claim cannot be verified independently, the Dimension 2 directional finding relies on unverifiable T1 evidence.

**Recommendation:**
Add arXiv preprint ID or DOI for A-23 to the evidence matrix. If a preprint was not posted, note: "A-23 has no preprint; verification requires institutional access to EMNLP 2025 proceedings. Readers unable to access A-23 should treat Dimension 2 T1 evidence as conditionally unverified pending access."

---

### CV-004-I1: AGREE-8 and AGREE-9 Are Self-Referential Citations

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | Synthesis |
| **Strategy Step** | Claim verification |

**Claim:** Synthesis states ranks 9–11 show qualitative improvement, citing "T4 (vendor docs, AGREE-8/AGREE-9)"

**Verification question:** Are AGREE-8 and AGREE-9 independently citable?

**Independent assessment:** AGREE-8 and AGREE-9 are finding labels from the synthesis.md produced in the immediately preceding PROJ-014 pipeline stage. They are not independently citable research findings — they are internal synthesis conclusions. Citing them as evidence is self-referential: the comparative effectiveness analysis cites the synthesis; the synthesis produced AGREE-8/AGREE-9; AGREE-8/AGREE-9 were produced by the same research pipeline.

**Recommendation:**
Replace AGREE-8 and AGREE-9 citations with the primary sources that synthesis.md used to produce those findings. If the primary sources are T4 (vendor documentation), cite the vendor documentation directly rather than the synthesis finding.

---

## S-012: FMEA

**Component decomposition:** The deliverable has five functional components: (1) 12-level hierarchy, (2) Five dimension analyses, (3) Evidence quality matrix, (4) Synthesis/directional verdict, (5) Confidence claims.

### FM-001-I1: Hierarchy Validity — Non-Empirical Ranking Critical Risk

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Section** | Cross-Cutting: 12-Level Effectiveness Hierarchy |
| **Strategy Step** | FMEA bottom-up decomposition |

**FMEA Entry:**

| Component | Failure Mode | Effect | Cause | Severity | Occurrence | Detection | RPN |
|-----------|-------------|--------|-------|----------|------------|-----------|-----|
| 12-level hierarchy | Ordinal positions are not empirically valid | All 5 dimension analyses produce artifacts of hierarchy construction, not real comparative findings | No controlled study validated rank ordering; narrative synthesis only | 9 | 7 | 4 | **252** |

**Analysis:** The hierarchy is the backbone for all five dimension analyses. If its ordinal positions are invalid (e.g., rank 5 and rank 9 are not empirically distinguishable), all five analyses inherit this invalidity. Detection is moderate (4/10) because the narrative nature of the hierarchy is disclosed but the specific consequence (all 5 analyses are affected) is not made explicit.

**Mitigation:** Establish a simplified 3-group taxonomy (model-access required, programmatic enforcement required, prompt-engineering accessible) as a backup analytical frame. Explicitly state that all conclusions drawn from specific rank positions are provisional.

---

### FM-002-I1: Confidence Labels — Undefined Scale Creates Misinterpretation Risk (Highest RPN)

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | Throughout |
| **Strategy Step** | FMEA bottom-up decomposition |

**FMEA Entry:**

| Component | Failure Mode | Effect | Cause | Severity | Occurrence | Detection | RPN |
|-----------|-------------|--------|-------|----------|------------|-----------|-----|
| Confidence labels | Reader interprets MEDIUM as operationally meaningful without scale | Practitioner over-relies on MEDIUM-confidence findings | No confidence scale defined in deliverable or methodology | 7 | 8 | 7 | **392** |

**Analysis:** This has the highest RPN of all identified failure modes (392). Occurrence is high (8/10) because practitioners routinely treat confidence labels as informative without investigating their definition. Detection is low (7/10 = difficult to detect in use) because no downstream check prevents misinterpretation.

**Mitigation:** Define confidence scale immediately in the Methodology section. Priority: this is the highest-RPN failure mode in the analysis.

---

### FM-003-I1: Session Empirical Data — Observational Data in Directional Finding Positions

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | Dimension 3 / Dimension 4 Verdicts |
| **Strategy Step** | FMEA bottom-up decomposition |

**FMEA Entry:**

| Component | Failure Mode | Effect | Cause | Severity | Occurrence | Detection | RPN |
|-----------|-------------|--------|-------|----------|------------|-----------|-----|
| Session empirical data (EO-001–EO-003) | Reader treats session observations as quasi-experimental | Analysis conclusions cited as evidence for framing effects | Observational data placed under "Directional finding:" headers | 8 | 6 | 5 | **240** |

**Mitigation:** Rename all D3 and D4 section headers from "Directional finding:" to "Observational note:" — confirmed from DA-003-I1 recommendation.

---

### FM-004-I1: Reflexivity Limitation — Impact Not Quantified

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | Assumption A-002 |
| **Strategy Step** | FMEA bottom-up decomposition |

**FMEA Entry:**

| Component | Failure Mode | Effect | Cause | Severity | Occurrence | Detection | RPN |
|-----------|-------------|--------|-------|----------|------------|-----------|-----|
| Reflexivity limitation | Reader cannot assess degree of contamination in D1/D3 analyses | JF-001/JF-002 bias influence is unknown | No quantification of researcher independence gap | 5 | 5 | 6 | **150** |

**Mitigation:** Add a reflexivity impact assessment: "JF-001 (Jerry Framework uses negative constraints) is a T5 source with high reflexivity risk. Its contribution to D1 is [one instance of supporting evidence]. Removing JF-001 and JF-002 entirely, the D1 directional finding [changes / remains stable] because [VS-001–VS-004 and T1 evidence remain]."

---

## S-013: Inversion

**Phase 1 — Goal inversion:** Invert each goal of the deliverable.

| Goal | Inverted Anti-Goal |
|------|-------------------|
| Establish directional verdict on structured negative vs. positive framing | Establish that no directional verdict is possible from available evidence |
| Justify Phase 2 experimental design | Discourage Phase 2 by treating the analysis as conclusive |
| Present transparent uncertainty | Present false precision that obscures evidence gaps |
| Establish vendor self-practice as genuine signal | Dismiss vendor self-practice as genre convention |

**Phase 2 — Assumption stress-test:**

### IN-001-I1: Inversion Reveals Insufficient Guard Against Phase 2 Abandonment

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Section** | Dimension 3 / Dimension 4 / L2 Architectural Implications |
| **Strategy Step** | Anti-goal analysis |

**Anti-goal:** "Ensure Phase 2 is NOT pursued." What conditions in this deliverable, if misread, would satisfy this anti-goal?

**Analysis:** The analysis contains three elements that, if misread, eliminate Phase 2 rationale:
1. D3 verdict: "C4 results achievable under negative-constraint prompting" — misread as "negative constraints work, Phase 2 is redundant"
2. D5 verdict: "Vendors use negative framing in production enforcement while recommending positive for general users" — misread as "we already know negative works in production"
3. L2 Implication A-002: "A single recommendation cannot serve both audiences accurately" — misread as "the analysis has already explained the paradox, Phase 2 is not needed"

The deliverable does not sufficiently separate observational evidence from the Phase 2 necessity argument. A reader who accepts the observational findings as meaningful might conclude Phase 2 is redundant.

**Recommendation:**
Add an explicit section: "Why Observational Evidence Does Not Replace Phase 2." State: "The observations in D3, D4, and D5 are necessary to establish that Phase 2 is worth running — they establish plausibility. They are not sufficient to replace Phase 2. The observational evidence cannot distinguish between: (a) negative constraint framing is the active variable, (b) re-injection frequency is the active variable, (c) consequence-pairing is the active variable. Phase 2 is required to isolate these variables."

---

### IN-002-I1: Hierarchy Falsifiability Condition Not Stated

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | Cross-Cutting: 12-Level Effectiveness Hierarchy |
| **Strategy Step** | Assumption inversion |

**Assumption:** "The 12-level hierarchy correctly distinguishes effectiveness levels."

**Inversion:** "The 12-level hierarchy does NOT correctly distinguish effectiveness levels."

**Analysis:** If the hierarchy's ordinal positions are invalid, ALL five dimension analyses are affected simultaneously. The deliverable does not state a falsifiability condition for the hierarchy — there is no specification of what evidence would cause the hierarchy to be revised or abandoned.

**Recommendation:**
Add to the hierarchy section: "This hierarchy would be revised if: (a) a controlled study finds no statistically significant difference between techniques at different ranks (suggesting the hierarchy's ordinal positions are not empirically supported), or (b) an independent meta-analysis produces a substantially different rank ordering. Until such evidence exists, the hierarchy is adopted as a working framework with acknowledged construct validity limitations."

---

### IN-003-I1: Genre Convention Explanation Eliminates All Dimension 1 and 5 Evidence

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | Dimension 1 / Dimension 5 |
| **Strategy Step** | Assumption inversion |

**Assumption:** "Vendor self-practice at ranks 9–11 reflects an engineering design choice about effectiveness (Explanation 3), or a principled audience differentiation (Explanation 1)."

**Inversion:** "Vendor self-practice at ranks 9–11 reflects genre convention (Explanation 2) — policy documents in the software industry use prohibitive vocabulary as a writing convention, not as an engineering discovery."

**Analysis:** If Explanation 2 is correct, VS-001 through VS-004 carry zero evidential weight for the hypothesis. Dimension 1's "strongest evidence" (T-002) becomes genre description, and Dimension 5's "HIGH confidence observational finding" becomes a documentation style observation. The analysis would then have no T1 or T2 evidence supporting the hypothesis — only T3 sources with methodological limitations and T5 session observations.

The analysis presents Explanation 2 as one of three competing explanations but does not state the severity of Explanation 2 being correct: it would reduce the analysis's evidential base from "vendor self-practice as strongest signal" to "T3 evidence for specific structured techniques (ranks 5–6) only."

**Recommendation:**
Add to the Synthesis section: "Explanation 2 severity: If genre convention fully explains the vendor self-practice pattern, the analysis's evidential base reduces to T3 evidence for ranks 5–6 only (A-23, A-15). Under this scenario, the directional verdict should be stated as: 'Specific structured techniques (warning-based meta-prompts and atomic decomposition) show improvement over blunt prohibition, with no evidence on structured negative vs. structured positive at ranks 9–11.' This is a substantially weaker conclusion and represents the Explanation 2 lower bound."

---

### IN-004-I1: Current-Model Sensitivity May Invert Evidence Transfer

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | Finding T-005 |
| **Strategy Step** | Assumption inversion |

**Assumption:** "Evidence from 2023–2024 studies transfers to current-generation frontier models."

**Inversion:** "GPT-5.2's documented sensitivity to ambiguous prompts means negative constraint framing, with its inherent semantic complexity, may perform WORSE on current-generation models than 2023–2024 evidence suggests."

**Analysis:** Finding T-005 notes that GPT-5.2 guidance warns that "poorly-constructed prompts containing contradictory or vague instructions can be more damaging to GPT-5.2 than to other models." Negative constraint framing introduces semantic complexity (negation parsing is harder than affirmation parsing). If frontier models are more sensitive to this complexity, the entire evidence base from 2023–2024 studies may understate the failure rate of negative framing on current models.

**Recommendation:**
Expand T-005 to state this inversion explicitly: "An alternative reading of CONFLICT-1 (positive scaling of negation comprehension in 2024–2025 models) is that 2024–2025 models are better at understanding negation — but GPT-5.2's sensitivity warning suggests they may also be more sensitive to poorly-constructed negations. Phase 2 must test negative constraint formulations for quality to ensure they are 'well-constructed' under frontier model sensitivity standards."

---

## S-014: LLM-as-Judge

**Anti-leniency directive active:** No score inflation. No excuse for gaps. No rounding up to meet threshold.

### Dimension-by-Dimension Scoring

#### Completeness (weight: 0.20)

**Assessment:** The analysis covers all five specified dimensions with evidence assembly, hierarchy mapping, and verdicts. Recommendations are present. Assumptions and Limitations are explicitly disclosed. The analysis does NOT include: (a) practitioner-actionable guidance for the case where Phase 2 is not conducted (PM-001-I1); (b) a confidence scale definition (SM-003-I1, PM-003-I1); (c) a hierarchy validity subsection (SM-002-I1); (d) a synthesis note on T-004 (context compaction) integration into the directional verdict (RT-003-I1).

**Gaps:** 4 structural completeness gaps, 2 of which are Major. Completeness score is reduced by the absence of the Phase 2 abandonment guard (PM-001-I1, Critical) and the confidence scale (PM-003-I1, Major).

**Score: 0.77** (7.7/10 completeness — structural gaps in practitioner guidance, confidence scale, synthesis integration of T-004)

#### Internal Consistency (weight: 0.20)

**Assessment:** Critical internal consistency failure: L0 summary contradicts synthesis verdict (CC-001-I1). Directional verdict applied to D3/D4 where data is explicitly labeled non-directional (DA-003-I1). A-16 cited despite NEVER-cite instruction (CC-002-I1). Recommendations use positive framing despite analytical principle (CC-003-I1). Scalar confidence value (0.78) inconsistent with dimension-level table (CC-004-I1).

**Score: 0.68** (6.8/10 — 1 Critical contradiction between L0 and synthesis, 1 self-declared principle violation on A-16 citation, 2 Major consistency failures)

#### Methodological Rigor (weight: 0.20)

**Assessment:** The methodology is well-designed for a comparative analysis using narrative synthesis. Evidence tiering is applied consistently. The hierarchy is used as an analytical backbone with appropriate caveats. Significant rigor gaps: (a) parsimony argument for Explanation 1 is asserted not demonstrated (DA-002-I1); (b) confidence labels undefined (FM-002-I1); (c) reflexivity limitation is disclosed but not quantified (FM-004-I1); (d) the directional verdict header is applied to D3/D4 where the methodology does not support it (DA-003-I1).

**Score: 0.76** (7.6/10 — parsimony assertion and undefined confidence scale are methodological gaps in an otherwise rigorous framework)

#### Evidence Quality (weight: 0.15)

**Assessment:** Evidence tiering (T1–T5) is applied. Evidence matrix is comprehensive. Critical gaps: A-23 (EMNLP 2025) cannot be independently verified (CV-003-I1); A-31 55% figure lacks control condition specification (CV-001-I1); EO-002 claim lacks directly verifiable source path (CV-002-I1); A-16 included despite NEVER-cite status (SR-002-I1). AGREE-8/AGREE-9 citations are self-referential (CV-004-I1).

**Score: 0.72** (7.2/10 — A-23 verifiability gap is particularly significant as it is the key T1 evidence for Dimension 2)

#### Actionability (weight: 0.15)

**Assessment:** Recommendations R-001 through R-006 are concrete and specific. The Phase 2 experimental design references (270 matched pairs, McNemar test, specific conditions C2/C3/C4/C5/C7) are actionable. Critical gap: no practitioner guidance exists for the scenario where Phase 2 is not conducted (PM-001-I1). The entire recommendation set is conditional on Phase 2 proceeding, leaving practitioners without guidance if Phase 2 is unavailable.

**Score: 0.78** (7.8/10 — recommendations are well-specified for Phase 2 but fail to provide unconditional practitioner guidance)

#### Traceability (weight: 0.10)

**Assessment:** Evidence IDs (A-NNN, I-NNN, VS-NNN, EO-NNN) are consistently applied. The synthesis.md and supplemental-vendor-evidence.md inputs are cited. Critical gaps: EO-001–EO-003 lack direct file paths (CV-002-I1); A-23 lacks DOI/preprint ID (CV-003-I1); I-28 and I-32 (context compaction bug reports) lack direct URLs (PM-004-I1); AGREE-8 and AGREE-9 are synthesis-internal citations not traceable to primary sources (CV-004-I1).

**Score: 0.76** (7.6/10 — four traceability gaps, particularly the EO and A-23 sourcing)

### Composite Score Calculation

| Dimension | Weight | Score | Weighted Score |
|-----------|--------|-------|----------------|
| Completeness | 0.20 | 0.77 | 0.154 |
| Internal Consistency | 0.20 | 0.68 | 0.136 |
| Methodological Rigor | 0.20 | 0.76 | 0.152 |
| Evidence Quality | 0.15 | 0.72 | 0.108 |
| Actionability | 0.15 | 0.78 | 0.117 |
| Traceability | 0.10 | 0.76 | 0.076 |
| **Composite** | **1.00** | | **0.743** |

### Quality Gate Verdict

**Composite Score: 0.743**
**Threshold: >= 0.95 (C4)**
**Verdict: REJECTED**

Band: REJECTED (< 0.85) — Significant rework required.

The deliverable fails the C4 quality gate by a margin of 0.207 points. The largest contributor to the deficit is Internal Consistency (score 0.68), driven by the Critical contradiction between the L0 executive summary and the synthesis directional verdict, and the directional-verdict/limitation contradiction in Dimensions 3 and 4. The second largest contributor is Evidence Quality (score 0.72), driven by the unverifiable A-23 citation and the A-16 inclusion despite NEVER-cite instruction.

### Critical Findings Blocking PASS

The following Critical findings must be resolved before re-scoring:

| Finding | Severity | Dimension Impact | Description |
|---------|----------|-----------------|-------------|
| DA-001-I1 | Critical | Internal Consistency, Methodological Rigor | Directional verdict unsupported by predominantly LOW-confidence evidence base |
| CC-001-I1 | Critical | Internal Consistency | L0 summary contradicts synthesis directional verdict |
| PM-001-I1 | Critical | Completeness, Actionability | No practitioner guidance for Phase 2-unavailable scenario |
| RT-001-I1 | Critical | Methodological Rigor, Evidence Quality | Circular evidence structure requires stronger methodological disclosure |
| FM-001-I1 | Critical | Methodological Rigor | Hierarchy single-point-of-failure with no backup analytical frame |
| IN-001-I1 | Critical | Completeness | Insufficient guard against Phase 2 abandonment misreading |
| CV-001-I1 | Critical | Evidence Quality | A-31 55% figure lacks verification of control condition specification |

---

## Execution Statistics

- **Total Findings:** 35
- **Critical:** 7 (DA-001-I1, PM-001-I1, RT-001-I1, CC-001-I1, FM-001-I1, IN-001-I1, CV-001-I1)
- **Major:** 19 (SR-001-I1, SR-002-I1, SM-001-I1, SM-002-I1, DA-002-I1, DA-003-I1, PM-002-I1, PM-003-I1, RT-002-I1, RT-003-I1, CC-002-I1, CC-003-I1, CV-002-I1, CV-003-I1, FM-002-I1, FM-003-I1, IN-002-I1, IN-003-I1, CC-004-I1 promoted to Major for scoring consistency)
- **Minor:** 9 (SR-003-I1, SM-003-I1, DA-004-I1, PM-004-I1, RT-004-I1, CV-004-I1, FM-004-I1, IN-004-I1, CC-004-I1)
- **Protocol Steps Completed:** All 10 strategies executed; all required protocol steps completed per each template's Execution Protocol
- **H-16 Compliance:** VERIFIED — S-003 executed before S-002 and S-001
- **Quality Gate:** REJECTED — Composite Score 0.743 vs. threshold 0.95 (C4)
- **Highest RPN Finding (FMEA):** FM-002-I1 (undefined confidence scale, RPN=392)
- **Revision Priority:** (1) CC-001-I1/DA-001-I1 — resolve Internal Consistency contradiction; (2) FM-002-I1 — define confidence scale; (3) PM-001-I1 — add unconditional practitioner guidance; (4) CV-001-I1/CV-003-I1 — fix evidence verification gaps; (5) RT-001-I1 — strengthen circularity disclosure; (6) FM-001-I1/IN-001-I1 — add hierarchy backup frame and Phase 2 necessity section

---

*adv-executor | C4 Tournament Iteration 1 | PROJ-014 | 2026-02-27*
*Template set: S-010, S-003, S-002, S-004, S-001, S-007, S-011, S-012, S-013, S-014*
*Constitutional compliance: P-001 (evidence-based findings), P-002 (report persisted), P-003 (no subagents spawned), P-004 (strategy ID and evidence cited for every finding), P-011 (specific evidence for every finding), P-022 (findings not minimized — C4 quality gate REJECTED at 0.743)*
