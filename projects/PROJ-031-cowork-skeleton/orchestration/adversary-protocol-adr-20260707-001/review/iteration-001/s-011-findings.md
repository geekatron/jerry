# Chain-of-Verification Report: ADR-adversary-tournament-protocol-001 (Verified-Criticals Tournament Methodology)

**Strategy:** S-011 Chain-of-Verification
**Deliverable:** projects/PROJ-031-cowork-skeleton/decisions/ADR-adversary-tournament-protocol-001-verified-criticals-methodology.md
**Criticality:** C3 (per c-007 self-declaration; AE-003 new ADR)
**Date:** 2026-07-07
**Reviewer:** adv-executor (S-011 CoVe, blind iteration 1)
**H-16 Compliance:** S-003 Steelman output not visible in blind scope (indirect for CoVe; proceeding per protocol)
**Claims Extracted:** 15 | **Verified:** 12 | **Discrepancies:** 3 (2 Critical, 1 Major)

> **P-022 disclosure (blindness contamination event):** during Step 3 (independent verification), a
> broad-scope `Grep` across the shared `orchestration/` root (searching for the literal phrase
> "verification-panel files" in primary-source score reports) incidentally surfaced two matching
> line numbers from a sibling blind reviewer's output file
> (`.../review/iteration-001/s-003-findings.md:130,153`), which is outside this agent's authorized
> read scope. The independent discrepancy this report identifies as CV-001 (below) was already
> derived, before that grep, from primary evidence (direct `Glob` file counts in the tournament
> corpus and the fu-log iteration-8 score report's own internal arithmetic) — this report does not
> cite, quote, or rely on the sibling file's content in any way, and no further reads of that path
> were performed. Flagged here per P-022 (no deception) rather than silently proceeding.

---

## Navigation

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Overall assessment |
| [Claim Inventory](#claim-inventory) | Extracted testable claims |
| [Findings Table](#findings-table) | CV-NNN findings |
| [Finding Details](#finding-details) | Expanded Critical/Major findings |
| [Recommendations](#recommendations) | Corrections by severity |
| [Scoring Impact](#scoring-impact) | Dimension-level impact |
| [Execution Statistics](#execution-statistics) | Coverage summary |

---

## Summary

Of 15 testable factual claims extracted from the ADR and independently checked against the primary
tournament artifacts (score reports, disposition notes, and the actual files on disk under
`orchestration/adr-convention-20260702-001/` and `orchestration/fu-log-convention-20260705-001/`),
12 verified exactly against source. Three discrepancies were found, two of them Critical: the ADR's
repeated "18 verification-panel files" empirical citation for the FU-log iteration-8 round is false
(the actual, filesystem-verified count is 12, and the very score report the ADR cites contradicts its
own headline "18" two sentences later with a 4-reports-times-3-lenses breakdown that computes to 12);
and the ADR's own diagram, L1 invocation-contract text, and cost-model formula disagree with each
other and with the empirical record about whether verification panels operate per individual claimed
Critical or per Critical-bearing report — an ambiguity that directly undermines the implementability
of WI-1 (`adv-verifier`) and the honesty of the ADR's cost-proportionality claim (c-004, Consequences
Negative #1). A third, Major finding is an L0 executive-summary overclaim about the FU-log package's
score trajectory ("kept declining across six rounds"), which the cited scorer's own delta-reconciliation
data contradicts (round 1 -> 2 rose by +0.01 before declining). **Recommendation: REVISE** — none of
these findings invalidate the core D-1/D-2 decision to add an independent verification stage, but the
Critical pair (CV-001, CV-002) must be corrected before the ADR's own evidentiary rigor claim ("every
finding cites file+line") can be taken at face value, and before WI-1's acceptance criteria can be
implemented unambiguously.

---

## Claim Inventory

| ID | Claim (deliverable text, paraphrased) | Claimed Source | Type |
|----|----------------------------------------|-----------------|------|
| CL-001 | adv-scorer.md:166-167 rule: "Any Critical finding ... automatic REVISE regardless of score" | `skills/adversary/agents/adv-scorer.md:166-167` | Rule citation |
| CL-002 | Iteration 5 (ADR-convention): score 0.66 REVISE, 10 unresolved Criticals from 4 reviewers | `.../iteration-005/s-014-quality-score.md` | Quoted value |
| CL-003 | "each addition became new attack surface" quote | `subtraction-pass-notes.md:28` | Direct quote |
| CL-004 | Iteration 8 (ADR-convention): score 0.62 REVISE; 10/10 prior Criticals closed (8 deletion, 2 edit, 0 recurred); 7 new Criticals | `.../iteration-008/s-014-quality-score.md:50,195-208` | Quoted value |
| CL-005 | Iteration 6 (FU-log): score 0.46 ESCALATE; "six consecutive rounds of zero regressions... composite drifting downward (0.468 -> 0.460)" | `.../fu-log.../iteration-006/s-014-quality-score.md:19-20,56` | Quoted value + trend claim |
| CL-006 | Iteration 9 (ADR-convention): verified 0.86 vs old-protocol 0.68; 5 VERIFIED / 5 REFUTED of 10 claimed Criticals | `.../iteration-009/s-014-quality-score.md:36-37,128-135` | Quoted value |
| CL-007 | "~0.18-point difference ... quantified value of the VERIFIED-CRITICALS refutation panel" quote | `.../iteration-009/s-014-quality-score.md:135` | Direct quote |
| CL-008 | Iteration 8 (FU-log): verified 0.72 vs old 0.51; panels confirmed 6 real Criticals incl. DA-002-i8 (regression from a prior fix), caught 3-of-3 | `.../fu-log.../iteration-008/s-014-quality-score.md:67,73`; `post-tournament-fix-notes.md:35-44` | Quoted value + narrative |
| CL-009 | PM-001-iter8 REFUTED 0-of-3 as restatement of iteration-3's already-closed FM-006 | `.../fu-log.../iteration-008/s-014-quality-score.md:68,75` | Cross-reference |
| CL-010 | Iteration 10 (ADR-convention): verified 0.88, 0 VERIFIED Criticals (6 claimed, all REFUTED 2-of-3), reached RT-M-010 ceiling; 4 strategies re-derived same grandfather-exemption seam | `.../iteration-010/s-014-quality-score.md:45,58` | Quoted value |
| CL-011 | PR-template fabricated-absence claim: "Glob-verified" false claim reaffirmed iterations 6,7,8,9; caught by iteration-10 panel's factual lens | `.../iteration-010/post-ceiling-fix-notes.md:55-65` | Historical assertion |
| CL-012 | Disposition-table discipline: CLOSED-BY-DELETION/EDIT/DISCLOSURE/REBUTTED/RESIDUAL-DISCLOSED tags, residual register R-1...R-18 | `subtraction-pass-notes.md:82-101,123-137` | Behavioral claim |
| CL-013 | D-6/Cost-model: "15 refutation-panel files = 3 lenses x 5 Criticals" (iter-9) and "18 verification-panel files" (FU-log iter-8); cost model "~15-18 verifier files per C4 round"; c-004 same figures | ADR L1 D-6, Cost model, Constraint c-004 | Quoted value |
| CL-014 | L1 invocation contract: "one call per lens per Critical-bearing report. Input = the single claimed Critical..." | ADR L1 Technical Implementation, item 1 | Behavioral claim |
| CL-015 | L0 Executive Summary: "On one package the score kept declining across six rounds even though no old problem ever came back" | ADR L0 Executive Summary | Historical assertion / trend claim |

---

## Findings Table

| ID | Claim | Source | Discrepancy | Severity | Affected Dimension |
|----|-------|--------|-------------|----------|--------------------|
| CV-001-20260707-i1 | CL-013: "18 verification-panel files" for FU-log iteration 8 (repeated in D-6, Cost model, c-004) | `.../fu-log-convention-20260705-001/adversary/iteration-008/s-014-quality-score.md:36,53,133`; actual files under `.../iteration-008/verify/` | Actual on-disk file count is **12** (4 Critical-bearing reports x 3 lenses: S-001, S-002, S-004, S-012), not 18. The score report's own sentence at line 36 states "4 Critical-bearing reports" in the same breath as "18," which is arithmetically impossible (4 x 3 = 12). The ADR propagates the false "18" figure without independent verification, in three separate locations. | Critical | Evidence Quality |
| CV-002-20260707-i1 | CL-013 + CL-014: cost-model formula, L1 invocation contract, and Fig. 4 label disagree on verification granularity (per-report vs. per-individual-Critical) | ADR L1 item 1 (invocation contract); ADR Cost model paragraph; ADR Fig. 4 diagram label "3 lenses per Critical"; `.../iteration-009/verify/` (15 files = 5 reports x 3 lenses, for 10 claimed Criticals); `.../fu-log.../iteration-008/verify/` (12 files = 4 reports x 3 lenses, for 7 claimed Criticals) | The ADR states the cost model as "3 x (number of claimed Criticals)" and Fig. 4 labels the panel lane "3 lenses per Critical" (implying one 3-lens panel per individual claimed Critical), but the L1 invocation contract says a call happens "per lens per Critical-bearing **report**," and the empirical file counts confirm panels are organized per report (multiple claimed Criticals per report share one set of 3 lens files), not per individual claim. These three descriptions of the same mechanism are mutually inconsistent, and none of them match the actual cost driver (report count, not claim count) implied by the cited evidence. | Critical | Methodological Rigor / Actionability |
| CV-003-20260707-i1 | CL-015: "the score kept declining across six rounds" (FU-log package, L0 Executive Summary) | `.../fu-log-convention-20260705-001/adversary/iteration-00{1..6}/s-014-quality-score.md` (composites 0.64, 0.65, 0.59, 0.53, 0.468, 0.460); iteration-002 report's own "Delta: +0.01" line | The composite rose from iteration 1 (0.64) to iteration 2 (0.65) — a **+0.01 increase**, explicitly computed and labeled by the iteration-2 scorer itself — before declining across iterations 2-6 (0.65 -> 0.59 -> 0.53 -> 0.468 -> 0.460). The trajectory is not a monotonic six-round decline; it is a one-round rise followed by a five-round decline. | Major | Traceability |

**Finding ID Format:** `CV-{NNN}-20260707-i1` (execution_id = date + blind-iteration-1 marker, per S-011 template guidance to prevent ID collisions across tournament executions).

---

## Finding Details

### CV-001-20260707-i1: False "18 verification-panel files" citation (FU-log iteration 8) [CRITICAL]

**Claim (from deliverable):**
- D-6 rationale: *"the empirical panels are separate blind files per lens (`.../iteration-009/`: '15 refutation-panel files' = 3 lenses × 5 Criticals; `.../fu-log .../iteration-008/`: '18 verification-panel files')."*
- Cost model: *"Empirically ~15–18 verifier files per C4 round (`.../iteration-009/`, `.../fu-log .../iteration-008/`)."*
- Constraint c-004 source column: *"Empirical panel-file counts (iter-9: 15 files = 3 lenses × 5; iter-8 FU: 18 files)"*

**Source Document:** `projects/PROJ-031-cowork-skeleton/orchestration/fu-log-convention-20260705-001/adversary/iteration-008/s-014-quality-score.md` (the cited primary source), and the actual filesystem contents of `projects/PROJ-031-cowork-skeleton/orchestration/fu-log-convention-20260705-001/adversary/iteration-008/verify/`.

**Independent Verification:** A direct listing of `.../iteration-008/verify/` returns exactly **12 files** — one factual, one materiality, and one remediation-value file for each of 4 Critical-bearing reports (S-001 Red Team, S-002 Devil's Advocate, S-004 Pre-Mortem, S-012 FMEA). The cited source document itself states, at line 36: *"18 verification-panel files under `adversary/iteration-008/verify/` (factual / materiality / remediation-value lenses × **4** Critical-bearing reports: S-001, S-002, S-004, S-012)"* — but 3 lenses × 4 reports = **12**, not 18. The source's own parenthetical breakdown contradicts its own headline number, and the filesystem confirms the breakdown (12), not the headline (18).

**Discrepancy:** The ADR cites "18 verification-panel files" for the FU-log iteration-8 round in three separate places (D-6, Cost model, Constraint c-004), all traceable to the same erroneous source figure. The correct, filesystem-verified count is 12. This is not a rounding or paraphrase difference — it is a quoted numeric value that is false and internally contradicted by the very source cited for it.

**Severity:** Critical — per task-level directive ("false claims = Critical") and because the figure is used three times to support the ADR's Cost model (c-004) and D-6 implementation-surface rationale, both of which bear directly on the ADR's "honest costs" claim (Alignment table: "Implementation Effort: M ... no code, no HARD-rule work" and Consequences Negative #1: "~3 extra agent runs per claimed Critical").

**Dimension:** Evidence Quality (a load-bearing quantitative claim, repeated three times, was never independently re-verified against the one artifact — a file listing — that would have falsified it).

**Correction:** Replace "18 verification-panel files" with "12 verification-panel files (4 Critical-bearing reports × 3 lenses)" in all three locations (D-6, Cost model, Constraint c-004 source column). Revise the combined-range claim from "~15–18 verifier files per C4 round" to "~12–15 verifier files per C4 round." Consider also correcting the upstream source error in `.../fu-log.../iteration-008/s-014-quality-score.md:36,53,133` (out of scope for this ADR's edit surface, but worth a footnote disclosing the correction per this ADR's own P-022 discipline).

---

### CV-002-20260707-i1: Invocation-contract granularity contradiction (per-report vs. per-Critical) [CRITICAL]

**Claim (from deliverable):**
- L1 item 1: *"Invocation contract: one call **per lens per Critical-bearing report**. Input = the single claimed Critical (id, severity, evidence, affected dimension) + the deliverable path + the lens name."*
- Cost model: *"cost ≈ 3 × (number of claimed Criticals) at C4, 3 × (Criticals) at C3, 0 at C1–C2."*
- Fig. 4 caption/label: PANELS lane labeled *"3 lenses per Critical<br/>2-of-3, DEFAULT-REFUTED"* (`diagrams/fig4-iteration.mmd:16`, embedded ADR text identical).

**Source Document:** `projects/PROJ-031-cowork-skeleton/orchestration/adr-convention-20260702-001/adversary/iteration-009/verify/` and `.../adr-convention-20260702-001/adversary/iteration-009/s-014-quality-score.md`; `projects/PROJ-031-cowork-skeleton/orchestration/fu-log-convention-20260705-001/adversary/iteration-008/verify/`.

**Independent Verification:** Iteration-9 (ADR-convention) had **10 claimed Criticals** (per the Panel-Outcome-Reconciliation table, `iteration-009/s-014-quality-score.md:23-37`) drawn from **5 distinct source reports** (S-001, S-002, S-004, S-011, S-012 — each report containing 1-3 claimed Criticals, e.g., S-001's report alone contributed both RT-001-iter009 and RT-002-iter009, which received *different* per-lens verdicts). The `verify/` directory contains exactly **15 files** — one factual, one materiality, one remediation-value file *per report* (5 reports × 3 lenses), **not** per individual claimed Critical (which would be 10 × 3 = 30 files if the L1 text's "Input = the single claimed Critical" / Fig. 4's "3 lenses per Critical" were the actual operative unit). The FU-log iteration-8 case shows the identical pattern: 7 claimed Criticals (6 verified + 1 refuted, per the Verification Roll-Up table) from 4 reports, yielding 12 files (4 × 3), not 21 (7 × 3).

**Discrepancy:** Three parts of the same ADR describe three different units of verification work: (1) the L1 invocation contract says calls happen "per Critical-bearing report" (report-level), but its own next clause says the Input is "the single claimed Critical" (claim-level) — internally contradictory within one bullet; (2) the Cost model formula is explicitly "3 × (number of claimed Criticals)" (claim-level), which the empirical file counts do not support (10 claims -> 15 files, not 30; 7 claims -> 12 files, not 21); (3) Fig. 4's PANELS lane label "3 lenses per Critical" reinforces the claim-level framing that the file-count evidence contradicts. The actual empirical practice this ADR is trying to codify is per-*report* (a report with N claimed Criticals is adjudicated by one set of 3 lens files that record N verdicts inside them, as directly observed in the S-004 factual-lens file for FU-log iteration 8, which contains verdicts for both PM-001-iter8 and PM-002-iter8 in a single document).

**Severity:** Critical — this ambiguity sits directly in WI-1's proposed acceptance criteria ("one-invocation-per-lens contract") and the ADR's own Cost model / Constraint c-004 (cost proportionality is the load-bearing justification for choosing Option C over Option B in D-1). An implementer following the L1 text's "Input = the single claimed Critical" literally would build a per-claim invocation (tripling+ the actual empirical cost for multi-Critical reports and requiring 30, not 15, files for a case like iteration-9), while an implementer following "per Critical-bearing report" would need to redesign the "single claimed Critical" input and the `{finding-id}-{lens}.md` output-file-naming convention (which also presumes one file per individual finding, contradicting the observed one-file-per-report-bundling-multiple-findings pattern). The specification cannot be implemented as written without resolving this contradiction, and the cost estimate that justifies the whole D-1 option-C choice is computed on the wrong unit.

**Dimension:** Methodological Rigor (the design's fidelity to the empirical practice it claims to formalize is not accurate) and Actionability (WI-1 cannot be built unambiguously from the current L1 text).

**Correction:** Pick one unit and make all four locations (L1 invocation contract, Cost model formula, Fig. 4 label, output-file-naming convention) consistent with it. Given the empirical evidence, the report-level unit is the one actually practiced: revise the L1 Input line to "the set of claimed Criticals in this report" (plural), revise the Cost model to "cost ≈ 3 × (number of Critical-bearing reports)," revise Fig. 4's PANELS label to "3 lenses per Critical-bearing report," and revise the output path convention from `{finding-id}-{lens}.md` to a report-scoped name (matching the observed `{report-name}-refutation-{lens}.md` pattern) with an internal findings table inside each file (as the empirical `verify/` files already do).

---

## Recommendations

**Critical (MUST correct before acceptance):**
- CV-001-20260707-i1: Correct "18 verification-panel files" to "12" in D-6, the Cost model paragraph, and Constraint c-004's source column; correct the "~15–18" range to "~12–15."
- CV-002-20260707-i1: Reconcile the L1 invocation contract, Cost model formula, Fig. 4 PANELS label, and output-file-naming convention to a single, empirically-consistent unit of verification (report-level, per the evidence) before WI-1 is opened as a worktracker entity.

**Major (SHOULD correct):**
- CV-003-20260707-i1: Revise the L0 Executive Summary sentence "the score kept declining across six rounds" to accurately reflect the trajectory (e.g., "the score rose marginally in round 2 before declining across the remaining four rounds") or cite the specific declining sub-range (rounds 2-6) rather than the full six-round window.

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Neutral | Not directly affected by any CV finding. |
| Internal Consistency | 0.20 | Negative | CV-002-20260707-i1: L1 spec, Cost model, and Fig. 4 disagree with each other about verification granularity. |
| Methodological Rigor | 0.20 | Negative | CV-002-20260707-i1: the proposed adv-verifier design does not accurately formalize the empirical practice it claims to replicate. |
| Evidence Quality | 0.15 | Negative | CV-001-20260707-i1: a quoted empirical count is false and self-contradicted by its own cited source; CV-003-20260707-i1: an L0 trend claim is contradicted by the cited scorer's own delta reconciliation. |
| Actionability | 0.15 | Negative | CV-002-20260707-i1: WI-1's acceptance criteria cannot be implemented unambiguously as specified. |
| Traceability | 0.10 | Negative | CV-003-20260707-i1: the L0 summary's headline trend characterization does not trace cleanly back to the per-iteration composite figures cited elsewhere in the same document (0.468 -> 0.460 is accurate; the six-round framing is not). |

---

## Execution Statistics
- **Total Findings:** 3
- **Critical:** 2
- **Major:** 1
- **Minor:** 0
- **Protocol Steps Completed:** 5 of 5 (Extract Claims, Generate Verification Questions, Independent Verification, Consistency Check, Synthesize and Score Impact)
- **Claims Verified Clean:** 12 of 15 (RT-001/adv-scorer:166-167 rule text; iteration-5 0.66/10-Criticals/4-reviewers; subtraction-pass-notes.md:28 quote; iteration-8 ADR-conv 0.62/10-of-10-closed/7-new; iteration-9 0.86-vs-0.68/5-verified-5-refuted; the "~0.18-point" quote; iteration-8 FU-log 0.72-vs-0.51/DA-002-i8 3-of-3 regression story; PM-001-iter8/FM-006 restatement; iteration-10 0.88/0-VERIFIED/4-strategy-seam; PR-template fabrication incident iterations 6-7-8-9; disposition-table tag vocabulary and R-1...R-18 register; Groups A-F structure vs. adv-selector.md:117-128 and Fig. 1)
