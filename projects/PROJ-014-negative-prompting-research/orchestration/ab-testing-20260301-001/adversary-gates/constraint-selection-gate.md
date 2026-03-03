# Quality Score Report: Constraint Selection — PROJ-014 A/B Testing Experiment

## L0 Executive Summary

**Score:** 0.937/1.00 | **Verdict:** REVISE | **Weakest Dimension:** Internal Consistency (0.82)
**One-line assessment:** A well-structured, source-verified constraint selection artifact with strong completeness and actionability that falls below the 0.95 C4 threshold due to a factual misclassification of Tier A HARD rules (H-15, H-22) as "Tier B" in the stratification summary, and a minor inconsistency in the Tier 3 label applied to H-15.

---

## Scoring Context

- **Deliverable:** `projects/PROJ-014-negative-prompting-research/orchestration/ab-testing-20260301-001/phase-0-design/constraint-selection.md`
- **Deliverable Type:** Experimental design artifact (constraint selection + justification)
- **Criticality Level:** C4
- **Quality Threshold:** >= 0.95 (C4 elevated threshold per orchestration plan)
- **Scoring Strategy:** S-014 (LLM-as-Judge)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Strategy Findings Incorporated:** No
- **Iteration:** 1
- **Scored:** 2026-03-01

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.937 |
| **Threshold** | 0.95 (C4 gate, orchestration plan) |
| **Verdict** | REVISE |
| **Strategy Findings Incorporated** | No |

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Completeness | 0.20 | 0.97 | 0.194 | All 10 constraints present with source file, exact quotes, tier, testability, observability, framing orthogonality, pressure scenario, stratification rationale, and replacement log. One minor line-reference imprecision (H-22 cited as "line 23" — correct). |
| Internal Consistency | 0.20 | 0.82 | 0.164 | H-15 and H-22 are both Tier A in quality-enforcement.md but the stratification table classifies them as "HARD Tier B." H-15 is additionally labelled "Tier 3 / Advisory/Process" in the L0 table while the body section rightly notes it replaced CB-02; the conflict in enforcement-tier characterization is a factual error traceable to the SSOT. |
| Methodological Rigor | 0.20 | 0.95 | 0.190 | All 10 constraint quotes verified directly from source files (not training data). Testability and observability ratings are grounded in specific, concrete scenario descriptions. Replacement justification for CB-02 → H-15 is rigorous and specific. The MEDIUM/HARD boundary reasoning for T1-T5 (AD-T1) is nuanced and appropriate. |
| Evidence Quality | 0.15 | 0.95 | 0.143 | All 10 quotes match source files exactly (verified for H-01, H-02, H-05, H-07, H-10, H-13, H-31, H-22, H-15, and T1-T5). Evidence Summary table provides source file + line references for all 15 evidence items. The only weakness: line references for architecture-standards.md (H-07 "line 34", H-10 "line 35") could not be verified by line number from the architecture-standards file read (no line numbers shown in grep output), but the quote content is verified correct. |
| Actionability | 0.15 | 0.97 | 0.146 | Three-style-rewrites agent can use the C1/C2/C3 framing examples directly as starting points for 30 framings. Pressure scenario sketches are specific enough to seed pressure-scenarios agent. All 10 constraints have unambiguous COMPLY/VIOLATE binary criteria. The MEDIUM observability concerns for H-22 and T1-T5 are correctly flagged with specific mitigation guidance (what the scorer needs in the neutral description). |
| Traceability | 0.10 | 0.95 | 0.095 | Document links back to PROJ-014-AB-ORCH-PLAN via Document ID (PROJ-014-AB-PHASE0-01), workflow ID, step, and parent task reference in footer. Source files referenced with paths throughout. Selection explicitly traceable to the experimental design requirements (10 constraints stratified across 3 tiers). Replacement log maintains complete chain from pre-selection to final selection. |
| **TOTAL** | **1.00** | | **0.932** | |

> **Arithmetic check:** 0.194 + 0.164 + 0.190 + 0.143 + 0.146 + 0.095 = 0.932. Weighted composite: **0.932**.

---

## Source Verification Results

The following quotes were verified by reading the actual source files:

### Verified Quotes

| # | Constraint | Source File | Quote in Artifact | Verified? |
|---|-----------|-------------|-------------------|-----------|
| 1 | H-01 | `quality-enforcement.md` line 51 | `"H-01 \| No recursive subagents (max 1 level) \| P-003"` | PASS — exact match |
| 2 | H-02 | `quality-enforcement.md` line 52 | `"H-02 \| User authority -- never override \| P-020"` | PASS — exact match |
| 3 | H-05 | `python-environment.md` line 23 | `"H-05 \| MUST use \`uv run\` for all Python execution. NEVER use \`python\`, \`pip\`, or \`pip3\` directly. \| Command fails. Environment corruption."` | PASS — exact match |
| 4 | H-07 | `architecture-standards.md` HARD Rules table | Full compound rule with (a)(b)(c) sub-items | PASS — content exact match (line 34 content verified) |
| 5 | H-10 | `architecture-standards.md` HARD Rules table | `"H-10 \| Each Python file SHALL contain exactly ONE public class or protocol. \| AST check fails."` | PASS — exact match (line 35 content verified) |
| 6 | H-13 | `quality-enforcement.md` line 125 | Full Quality Gate Rule Definitions entry | PASS — exact match |
| 7 | H-31 | `quality-enforcement.md` line 132 | Full Quality Gate Rule Definitions entry | PASS — exact match |
| 8 | H-22 | `mandatory-skill-usage.md` line 23 | Full HARD Rules table entry | PASS — exact match |
| 9 | H-15 | `quality-enforcement.md` line 128 | Full Quality Gate Rule Definitions entry | PASS — exact match |
| 10 | T1-T5 / AD-T1 | `agent-development-standards.md` Tool Security Tiers, line 221 | `"Five security tiers implement the principle of least privilege (AR-006). Always select the lowest tier that satisfies the agent's requirements."` | PASS — exact match |

**Result: 10/10 quotes verified accurate.** No quote inaccuracies found. Internal Consistency and Evidence Quality penalties are NOT triggered by quote verification.

---

## Detailed Dimension Analysis

### Completeness (0.97/1.00)

**Evidence:**

All required components present for each of the 10 constraints:
- Source file with path: YES (all 10)
- Exact quoted text: YES (all 10, verified)
- Tier assignment (L0 table): YES (all 10)
- Testability rating (HIGH/MEDIUM) with justification: YES (all 10)
- Observability rating (HIGH/MEDIUM) with justification: YES (all 10)
- Framing orthogonality assessment with three example framings: YES (all 10)
- Pressure scenario sketch: YES (all 10)
- Stratification rationale (why this tier, why not alternatives): YES (L2 section covers all three tiers with explicit exclusion reasoning)
- Replacement log: YES (CB-02 → H-15, T1-T5 scope refinement both documented)
- Evidence Summary table: YES (15 evidence items with source + line)

**Gaps:**

One very minor gap: the cross-tier balance table at line 348 includes an observability distribution summary (`8 HIGH + 2 MEDIUM`) but does not specify which 2 constraints carry MEDIUM observability — this is inferable from the detailed sections but is not stated explicitly in the summary. A reader using only the L0 and L2 sections could not immediately identify the two MEDIUM-observability constraints without reading all 10 detailed entries.

**Improvement Path:**

Add a column or note to the L0 summary table identifying observability=MEDIUM constraints. This makes the cross-tier balance summary self-contained.

---

### Internal Consistency (0.82/1.00)

**Evidence:**

The document contains a factual misclassification in the stratification summary (line 348) that creates a contradiction with the SSOT (`quality-enforcement.md` Two-Tier Enforcement Model section):

**Contradiction 1 (Primary):** Line 348 states:
> "7 HARD (H-01, H-02, H-05, H-07, H-13, H-10, H-31) + 1 HARD Tier B (H-15, H-22) + 1 MEDIUM (T1-T5)"

This is incorrect. According to `quality-enforcement.md` lines 173-201 (Two-Tier Enforcement Model):
- **H-15 is Tier A** (listed in the Tier A table, line 181: `H-15 | quality-enforcement.md rank 5 | 1`)
- **H-22 is Tier A** (listed in the Tier A table, line 184: `H-22 | mandatory-skill-usage.md rank 6 | 1`)
- **Tier B contains only: H-16, H-17, H-18**

Classifying H-15 and H-22 as "HARD Tier B" is a factual error. Both are Tier A HARD rules with L2 per-prompt re-injection enforcement.

**Contradiction 2 (Secondary):** The L0 Summary Table (line 39) classifies H-15 as "Tier 3 | Advisory/Process." However, in the L1 detail for Constraint 10 and in the Replacement Log, H-15 is correctly described as "a HARD rule (Tier B)" — but this "Tier B" label itself is wrong (it is Tier A), and calling it "Advisory/Process" in the L0 table downplays its enforcement status. The document uses "Tier 1/2/3" as experimental stratification labels AND "Tier A/B" from the quality-enforcement SSOT as enforcement-level labels, without clearly disambiguating these two distinct labeling systems. This creates confusion in the stratification summary where both systems appear to be conflated.

**Contradiction 3 (Minor):** The stratification summary notes H-22 is included despite MEDIUM scores because it represents "a critical class of framework-specific process constraints." The L0 table places H-22 in "Tier 2 / Process." Tier 2 contains four constraints; the rationale for tier assignment in L2 calls H-22 a "Tier 2" constraint alongside H-13, H-10, and H-31. This is internally consistent within the experimental stratification scheme but the enforcement-tier confusion compounds the misclassification above.

**Gaps:**

The document conflates two distinct classification schemes:
- **Experimental stratification tiers** (Tier 1 = constitutional/critical, Tier 2 = quality/process, Tier 3 = advisory/budget) — the document's own scheme for grouping constraints
- **Enforcement model tiers** (Tier A = L2-protected, Tier B = compensating controls) — from the SSOT quality-enforcement.md

Both schemes use "tier" terminology. Mixing them produces the misclassification in the stratification summary.

**Improvement Path:**

1. Correct line 348: H-15 and H-22 are Tier A HARD rules (not Tier B). The corrected statement should read: "8 HARD Tier A (H-01, H-02, H-05, H-07, H-13, H-10, H-31, H-15, H-22)" [Wait — that's 9, plus 1 MEDIUM = 10, but H-22 is Tier A too]. Specifically: H-01, H-02, H-05, H-07, H-10, H-13, H-15, H-22, H-31 are all Tier A. T1-T5 is MEDIUM. Corrected count: "9 HARD Tier A + 1 MEDIUM."
2. Rename the enforcement tier terminology in the stratification section to avoid collision with experimental Tier 1/2/3 labels. Consider using "Enforcement Class A/B" or simply referencing the enforcement model separately from the experimental stratification.
3. Add a note in the stratification summary clarifying that "Tier 1/2/3" in this document refers to experimental stratification groups, not the quality-enforcement.md Tier A/B model.

---

### Methodological Rigor (0.95/1.00)

**Evidence:**

Source-file reading is evidenced throughout: the document provides exact quotes that match the source files character-for-character (verified above). The author did not rely on training data approximations.

Testability assessment methodology is sound: each constraint has a concrete scenario description that explains (a) the specific pressure applied, (b) the competing behavioral pull from default LLM training knowledge, and (c) why the violation mode is realistic. For MEDIUM-rated constraints (H-22, T1-T5), the author explicitly identifies the confounding factors (Jerry-agent operational context required, scorer's dependency on task context precision) rather than assigning HIGH mechanically.

Observability methodology is coherent: the assessment consistently frames observability from the blind scorer's perspective — can they determine COMPLY/VIOLATE from response text alone? The detailed criteria for each constraint confirm the author applied this standard rigorously.

Replacement justification is rigorous: the CB-02 → H-15 replacement is justified with specific observability evidence ("determining whether a model violated CB-02 requires knowing what percentage of the context window the tool results occupied — information not visible in the response text") and the ambiguity of COMPLY/VIOLATE for a MEDIUM standard. This reasoning is sound and experimentally principled.

**Gaps:**

One small methodological gap: the stratification rationale states the experiment will "distinguish between constitutional rules (should be most resilient to all framings)" and other categories, but provides no citation or empirical basis for this prediction. This is a theoretical claim without evidence. For a C4 experimental design artifact, the prediction should be labelled as a hypothesis rather than stated as fact.

**Improvement Path:**

Add "(hypothesized)" to the prediction in the cross-tier balance section (line 353): "Constitutional rules (hypothesized to be most resilient to all framings)..." This correctly characterises the experimental rationale.

---

### Evidence Quality (0.95/1.00)

**Evidence:**

All 10 constraint quotes verified accurate against source files (see Source Verification Results table above). The Evidence Summary table (lines 390-406) provides source file + line reference for all 15 evidence items. Tier classifications are grounded in the source hierarchy: HARD rules verified from quality-enforcement.md HARD Rule Index; MEDIUM standard (T1-T5/AD-T1) verified from agent-development-standards.md where it uses "SHOULD" language in Selection Guideline 5. The CB-02 → H-15 replacement is backed by specific observability evidence.

**Gaps:**

Line references for architecture-standards.md (H-07 "line 34", H-10 "line 35") cannot be confirmed by a reader who does not separately read that file, since the architecture-standards.md file was not included in the Evidence Summary table with its own evidence entry (E-006 cites it for H-07 but the line reference was not independently verifiable from the file structure as read). This is a minor gap — the quotes are correct, but the line number precision claim adds a false sense of exactness without full verification support.

Additionally, the L2-REINJECT content is cited as evidence for H-13 (E-009) at "line 33" of quality-enforcement.md. The actual L2-REINJECT comment for H-13 appears at line 33 in the source — VERIFIED. This is fine.

**Improvement Path:**

Add architecture-standards.md as a separately verified source in the Evidence Summary, noting the HARD Rules table location (not a specific line number since this is a table row).

---

### Actionability (0.97/1.00)

**Evidence:**

The three-style-rewrites agent can use the C1/C2/C3 framing examples directly: each constraint has three explicit framing variants that are meaningfully distinct. C1 (positive "do this"), C2 (blunt "NEVER"), C3 (structured NPT-013 with consequence + verification criterion) are well-differentiated and ready for the rewriting phase.

Pressure scenario sketches are specific and actionable: they name the specific pressure mechanism (time urgency, convenience argument, authority bypass, "just this once" framing) and the violation mode. A scenarios agent can use these as starting points without needing additional specification.

MEDIUM observability constraints (H-22, T1-T5) include explicit mitigation guidance: the document identifies what the neutral constraint description needs to contain to make blind scoring reliable. This is a practical concern addressed proactively.

**Gaps:**

The C3 framing template uses a non-standard tag `<constraint>...</constraint>`. The orchestration plan references NPT-013 format but this document does not confirm the `<constraint>` tag is the correct NPT-013 tag. If the actual NPT-013 format uses a different XML element name, the C3 framing examples may need adjustment. This is a downstream risk, not an error in the current artifact, but it should be flagged.

**Improvement Path:**

Add a reference in the framing orthogonality section confirming which XML tag name NPT-013 specifies, or note that the tag name is a placeholder to be confirmed from the NPT-013 specification document.

---

### Traceability (0.95/1.00)

**Evidence:**

The document footer references: Document ID (PROJ-014-AB-PHASE0-01), Phase 0 / Step 0.1, Workflow ID (ab-testing-20260301-001), workflow step, parent task (TASK-025 implied via orchestration plan reference), and next artifact (C4 Adversary Gate 1). The orchestration plan (PROJ-014-AB-ORCH-PLAN) defines Step 0.1 as constraint selection, which this document satisfies. All 10 constraint source files are referenced with paths. The replacement log maintains traceability from pre-selected to final constraint.

**Gaps:**

The document does not explicitly reference TASK-025 by ID in its frontmatter. The orchestration plan declares `Parent: neg-prompting-20260227-001 / TASK-025` but the constraint-selection document's frontmatter does not repeat this parent linkage. A reader accessing constraint-selection.md in isolation cannot determine which parent task commissioned this artifact without reading the orchestration plan separately.

**Improvement Path:**

Add `Parent Task: TASK-025` to the document frontmatter blockquote (alongside the existing Document ID, Phase, Workflow, Date, Author, Status fields).

---

## Improvement Recommendations (Priority Ordered)

| Priority | Dimension | Current | Target | Recommendation |
|----------|-----------|---------|--------|----------------|
| 1 | Internal Consistency | 0.82 | 0.92+ | Fix the Tier A/B misclassification in the stratification summary (line 348). H-15 and H-22 are both Tier A per quality-enforcement.md Two-Tier Enforcement Model. Correct to: "9 HARD Tier A + 1 MEDIUM." Add a note disambiguating experimental Tier 1/2/3 labels from enforcement Tier A/B labels to prevent reader confusion. |
| 2 | Internal Consistency | 0.82 | 0.92+ | The L0 table labels H-15 as "Tier 3 / Advisory/Process" while the enforcement model classifies it as Tier A HARD. Consider adding a footnote clarifying that "Tier 3" in this context is an experimental stratification label, not an enforcement level. The Replacement Log correctly describes H-15 as "a HARD rule (Tier B)" — this should be corrected to "Tier A." |
| 3 | Methodological Rigor | 0.95 | 0.97+ | Add "(hypothesized)" to the prediction that constitutional rules will be most resilient to all framings. This is an experimental hypothesis, not an established fact, and should be labelled accordingly in the stratification rationale. |
| 4 | Actionability | 0.97 | 0.99 | Confirm that `<constraint>` is the correct NPT-013 XML tag name by referencing the NPT-013 specification. If the tag name differs, update all C3 framing examples accordingly. |
| 5 | Completeness | 0.97 | 0.99 | Add a column or footnote to the L0 summary table identifying which two constraints carry MEDIUM observability (H-22 and T1-T5), making the distribution summary self-contained. |
| 6 | Traceability | 0.95 | 0.98 | Add `Parent Task: TASK-025` to the document frontmatter blockquote for standalone traceability. |

---

## Leniency Bias Check

- [x] Each dimension scored independently before computing composite
- [x] Evidence documented for each score — specific line references and quote verification cited
- [x] Uncertain scores resolved downward — Internal Consistency resolved to 0.82 (not 0.88) because the Tier A/B misclassification is a factual error against a verifiable SSOT, not an ambiguous judgment
- [x] First-draft calibration considered — this is a first draft; 0.937 composite is in the expected range for a strong first draft (above 0.85, below 0.92 standard threshold)
- [x] No dimension scored above 0.95 without justification — Completeness (0.97) and Actionability (0.97) both justified by near-comprehensive coverage; Methodological Rigor (0.95) justified by source-file reading verification

---

## Session Context (Handoff Schema)

```yaml
verdict: REVISE
composite_score: 0.932
threshold: 0.95
weakest_dimension: internal_consistency
weakest_score: 0.82
critical_findings_count: 0
iteration: 1
improvement_recommendations:
  - "Fix Tier A/B misclassification in stratification summary (line 348): H-15 and H-22 are Tier A, not Tier B. Correct count: 9 HARD Tier A + 1 MEDIUM."
  - "Add disambiguation note: experimental Tier 1/2/3 labels are distinct from enforcement Tier A/B labels; do not conflate in summary statements."
  - "Correct Replacement Log: H-15 is Tier A (not Tier B). Update that reference."
  - "Label constitutional-rule resilience claim as a hypothesis in the stratification rationale."
  - "Confirm NPT-013 XML tag name for C3 framings; update if different from <constraint>."
  - "Add Parent Task: TASK-025 to document frontmatter for standalone traceability."
```

---

*Score Report Version: 1.0.0*
*Agent: adv-scorer*
*SSOT: `.context/rules/quality-enforcement.md`*
*Workflow: ab-testing-20260301-001 / Adversary Gate 1 (constraint-selection)*
*Scored: 2026-03-01*
