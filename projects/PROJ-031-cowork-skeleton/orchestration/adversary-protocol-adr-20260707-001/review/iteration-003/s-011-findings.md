# Chain-of-Verification Report: ADR-adversary-tournament-protocol-001 (iteration 3)

## Navigation

| Section | Purpose |
|---------|---------|
| [Header](#header) | Execution metadata |
| [Summary](#summary) | Overall assessment |
| [Findings Table](#findings-table) | All CV-NNN findings |
| [Finding Details](#finding-details) | Expanded evidence per finding |
| [Recommendations](#recommendations) | Corrections by severity |
| [Scoring Impact](#scoring-impact) | Dimension-level impact |
| [Claims Independently Verified Clean](#claims-independently-verified-clean) | Spot-checked claims with no discrepancy |

---

## Header

**Strategy:** S-011 Chain-of-Verification
**Deliverable:** `projects/PROJ-031-cowork-skeleton/decisions/ADR-adversary-tournament-protocol-001-verified-criticals-methodology.md`
**Criticality:** C3 (per invoking task)
**Date:** 2026-07-07
**Reviewer:** adv-executor (S-011), blind execution (no access to iteration-003 sibling reports by design; iteration-001/002 review artifacts were incidentally surfaced by one directory-wide grep and are NOT relied upon as evidence for any finding below — every finding here is independently re-derived from primary tournament-corpus sources)
**H-16 Compliance:** Not independently confirmed in this blind execution (no S-003 output supplied); per S-011 template, this is an indirect/discouraged-but-not-blocking gap for CoVe.
**Claims Extracted:** 22 | **Verified:** 20 | **Discrepancies:** 2 (1 Critical, 1 Major)

---

## Summary

Independent Chain-of-Verification against the primary tournament corpus (`orchestration/adr-convention-20260702-001/` and `orchestration/fu-log-convention-20260705-001/`) confirms the overwhelming majority of the ADR's quantitative and quotational claims: composite scores, VERIFIED/REFUTED counts, panel-file counts, the disclosed "18→12" correction, the fabricated-PR-template incident's full evidentiary chain, and all four Mermaid diagrams (which match their persisted `.mmd` sources and the `## Design Diagrams` prose exactly). One **Critical** discrepancy was found: the ADR's evidence chain (L0 + Context) omits an entire scored tournament round (fu-log-convention iteration-007, VERIFIED-CRITICALS composite 0.83) that is neither narrated nor reconciled anywhere in the document, even though its own "0.86–0.88" claim and "four later rounds" count silently depend on it — and the omitted round documents an un-reconciled round-over-round **decline** (0.83 → 0.72) under the *same* protocol the ADR credits with eliminating exactly this kind of unexplained score movement. One **Major** discrepancy was found in the D-1 "Why C is chosen" rationale's specific verification-method claim. **Recommendation: REVISE** — correct both before acceptance; neither finding requires re-opening the six chosen decisions (D-1..D-6) themselves.

---

## Findings Table

| ID | Claim | Source | Discrepancy | Severity | Affected Dimension |
|----|-------|--------|-------------|----------|--------------------|
| CV-001-20260707iter3 | "moved scores from a misleading 0.68 up to an honest 0.86–0.88" / "proven across four later rounds" (ADR L0, line 72-76) | `fu-log-convention-20260705-001/adversary/iteration-007/s-014-quality-score.md` (full file) and `iteration-008/s-014-quality-score.md` (full file) | The Context section names exactly 3 verified-protocol rounds (ADR-conv iter-9: 0.86; ADR-conv iter-10: 0.88; FU-log iter-8: 0.72) — never iter-7. But FU-log iteration-007 also ran the VERIFIED-CRITICALS protocol (composite **0.83**, old-protocol 0.54) — the 4th round implied by "four later rounds." Its omission is not stylistic: (a) 0.83 falls outside the cited "0.86–0.88" range, and (b) the very next round (iter-8) **declined** to 0.72 under the identical protocol, a movement the ADR never discloses or reconciles — the opposite of the "converges" narrative the ADR builds its case on, and exactly the kind of un-reconciled inter-round score movement D-5 (mandatory delta-reconciliation) is designed to prevent going forward. iteration-008's own report compounds this: its own delta table reconciles against iteration-006 (0.46), silently skipping iteration-007 (0.83) entirely. | **Critical** | Evidence Quality / Internal Consistency |
| CV-002-20260707iter3 | "100% of the 18 cited tournament rounds ran at C4 -- there are zero C1, C2, or C3 rounds in the record (grep across every `Criticality Level` declaration in both packages confirms all-C4)" (ADR D-1 "Why C is chosen", line 307-309) | `fu-log-convention-20260705-001/adversary/iteration-{001..005}/s-014-quality-score.md` (`Criticality Level` field, each file) | A literal grep for `Criticality Level` across the FU-log package returns explicit **`C3`** labels in 5 of 8 rounds (iterations 1-5), each produced by the S-010 self-refine strategy report and each time flagged by the scorer as "a minor/recurring internal labeling inconsistency in the adversary run itself, not scored against the deliverable." The ADR's specific verification method ("grep... confirms all-C4") therefore does not hold as literally stated -- a grep surfaces contradicting hits. The ADR's *substantive* conclusion (every round's *operative, scored* criticality was C4) still stands, because the scorer consistently discounted the S-010 mislabeling as noise -- but the ADR states a stronger, mechanically-verifiable claim ("grep... confirms") than the evidence actually supports, in a document whose central thesis is about not trusting unverified "verified" claims. | **Major** | Methodological Rigor / Evidence Quality |

---

## Finding Details

### CV-001-20260707iter3: Evidence chain omits a scored round that contradicts the claimed convergence pattern [CRITICAL]

**Claim (from deliverable):** L0 Executive Summary: *"This single change moved scores from a misleading 0.68 up to an honest 0.86–0.88, correctly kept the genuinely broken items ... and correctly discarded restatements of already-known limitations."* Preceding sentence: *"The fix, discovered mid-engagement and proven across four later rounds..."* The Context section's "Evidence chain — the verified protocol converges" subsection narrates exactly three rounds in full: Iteration 9 (ADR-convention, verified 0.86 vs old 0.68), Iteration 8 (FU-log, verified 0.72 vs old 0.51), and Iteration 10 (ADR-convention, verified 0.88, 0 VERIFIED Criticals). No paragraph anywhere in the ADR mentions FU-log iteration 7.

**Source Document:** `projects/PROJ-031-cowork-skeleton/orchestration/fu-log-convention-20260705-001/adversary/iteration-007/s-014-quality-score.md`

**Independent Verification:** Iteration-007's own L0 states: *"Score: 0.83/1.00 (VERIFIED-CRITICALS protocol) | Verdict: REVISE"* with *"Composite (naive, old-protocol, all claims counted): 0.54."* This is the fourth VERIFIED-CRITICALS-scored round in the 18-round record (the other three being ADR-convention iter-9/10 and FU-log iter-8) -- confirming "four later rounds" is numerically correct, but only if iteration-007 is counted, which the ADR's own narrative never does. Critically, iteration-008's own score report -- read independently for this verification -- reconciles its delta explicitly against **iteration-006** ("Prior Iteration (iteration-006) Composite: 0.460 ... Delta vs. iteration-006: +0.260"), not against iteration-007, even though iteration-008 lists `adversary/iteration-007/restore-notes.md` as an input it read. Iteration-007's own composite (0.83) is never referenced by iteration-008's delta reconciliation, its dimension table, or its narrative -- an internal discontinuity in the corpus that the ADR's Context section silently inherits by omitting iteration-007 altogether rather than disclosing and explaining the 0.83 → 0.72 decline.

**Discrepancy:** The ADR's L0 states a specific numeric range ("0.86–0.88") as the outcome of the fix "proven across four later rounds," but two of those four rounds (FU-log iter-7 at 0.83 and FU-log iter-8 at 0.72) fall well outside that range, and the transition between them is a **decline under the identical VERIFIED-CRITICALS protocol** -- the same class of unexplained round-to-round score movement the ADR elsewhere criticizes in the *old* protocol (Context: "the composite drifted downward... even though no old problem ever came back") and that D-5 (mandatory delta-reconciliation) is expressly adopted to prevent. Because this decline is neither mentioned nor reconciled in the ADR, a reader is left with the impression that the new protocol produced a clean, monotonic improvement across "four later rounds," when the primary evidence shows one package's own two data points moving 0.83 → 0.72 -- non-monotonic, and undisclosed.

**Severity:** Critical -- this is a load-bearing empirical claim in the L0 Executive Summary (the section most likely to be read and relied upon by the human ratifying this ADR), it is directly checkable against primary sources, and independent verification shows the omitted data point both falls outside the cited range and undercuts the "converges" characterization central to the ADR's own rationale for adopting the methodology. It does not overturn the chosen decision (D-1..D-6) -- the VERIFIED-CRITICALS protocol still clearly outperforms naive counting in the omitted round too (0.83 vs. naive 0.54) -- but it is a genuine evidence-quality/traceability gap in the document that most needs to model rigorous verification.

**Dimension:** Evidence Quality (primary), Internal Consistency (secondary -- the omission conceals a real, unreconciled score discontinuity within the corpus itself)

**Correction:** Add FU-log iteration-007 to the "Evidence chain — the verified protocol converges" subsection (e.g., between the current Iteration-9 and Iteration-8-FU-log paragraphs, or reordered chronologically), citing `.../fu-log-convention-20260705-001/adversary/iteration-007/s-014-quality-score.md:20,65-66` (0.83 verified vs. 0.54 old-protocol). Either (a) explain the 0.83 → 0.72 decline explicitly (e.g., iteration-008 raised additional Critical claims that iteration-007's panel had not yet examined, and/or the FU.10 diagram addition introduced no regression but the panel found more VERIFIED Criticals: 6 vs. 4), or (b) soften "moved scores... up to an honest 0.86–0.88" to a range that honestly spans all four rounds (e.g., "0.72–0.88, non-monotonically, with the lowest and highest values both occurring after the fix was in place") and correct "proven across four later rounds" to explicitly name all four with their actual dispersion.

---

### CV-002-20260707iter3: "grep... confirms all-C4" is a stronger claim than a literal grep supports [MAJOR]

**Claim (from deliverable):** D-1 "Why C is chosen": *"100% of the 18 cited tournament rounds ran at C4 -- there are zero C1, C2, or C3 rounds in the record (grep across every `Criticality Level` declaration in both packages confirms all-C4)."*

**Source Document:** `projects/PROJ-031-cowork-skeleton/orchestration/fu-log-convention-20260705-001/adversary/iteration-001/s-014-quality-score.md:12`, `iteration-002/s-014-quality-score.md:12`, `iteration-003/s-014-quality-score.md:12`, `iteration-004/s-014-quality-score.md:26`, `iteration-005/s-014-quality-score.md:26`

**Independent Verification:** Each of the five cited lines reads a variant of: *"Criticality Level: C4 (... S-010 self-refine labels C3 -- a [minor/recurring] internal labeling inconsistency in the adversary run itself, not scored against the deliverable)."* A grep for `Criticality Level` across the FU-log package therefore returns the literal string `C3` five times, not zero.

**Discrepancy:** The ADR's claim is that a mechanical check ("grep... confirms") establishes the record is 100% C4 with zero exceptions. The actual mechanical check does not establish this cleanly -- it surfaces five `C3` hits that require a judgment call (the scorer's own explicit discounting of the S-010 self-refine mislabel as noise) to explain away. The *substance* the ADR wants to defend -- every round's operative, scored criticality was C4 -- is still true, because the scorer's discounting is itself documented and consistent across all five instances. But the specific evidentiary claim ("grep... confirms all-C4") overstates what a literal grep shows, in a document whose entire subject is the danger of unverified "verified" assertions (the fabricated-PR-template incident is the ADR's own centerpiece example of this exact failure mode).

**Severity:** Major -- does not change the C1-C2-exemption-is-a-cost-decision-not-a-finding conclusion (D-1 already frames the C1-C2 exemption as a reasoned default, not an empirical finding, so the underlying argument survives), but it is a checkable overclaim about the ADR's own verification method that a future reader re-running the cited grep will find does not "confirm all-C4" without qualification.

**Dimension:** Methodological Rigor (primary), Evidence Quality (secondary)

**Correction:** Reword to: *"100% of the 18 cited tournament rounds were **scored** at C4 -- there are zero C1, C2, or C3 rounds in the operative record. (A grep across every `Criticality Level` declaration in both packages returns five `C3` hits, all from S-010 self-refine's own report in FU-log iterations 1-5, each explicitly discounted by the scorer as an internal labeling inconsistency not scored against the deliverable -- the round's own composite and verdict treated the criticality as C4 in every case.)"*

---

## Recommendations

**Critical (MUST correct before acceptance):**
- CV-001-20260707iter3: Add FU-log iteration-007 (0.83 verified / 0.54 old) to the Context evidence chain; either explain the 0.83→0.72 decline or revise the "0.86–0.88... four later rounds" framing to honestly reflect the full four-round dispersion (0.72-0.88).

**Major (SHOULD correct):**
- CV-002-20260707iter3: Qualify the "grep... confirms all-C4" claim to acknowledge the five `C3` hits from S-010's own mislabeling in FU-log iterations 1-5, and state explicitly that the claim is about *operative/scored* criticality, not literal grep-string uniformity.

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Neutral | Not affected by either finding |
| Internal Consistency | 0.20 | Negative | CV-001: the corpus's own unreconciled 0.83→0.72 movement is silently inherited rather than disclosed |
| Methodological Rigor | 0.20 | Negative | CV-002: the cited "grep... confirms" verification method does not hold as literally stated |
| Evidence Quality | 0.15 | Negative | CV-001: a load-bearing L0 numeric claim ("0.86–0.88... four later rounds") omits and is contradicted by one of its own four underlying data points |
| Actionability | 0.15 | Neutral | Both findings have concrete, low-effort textual corrections (add one paragraph; reword one parenthetical) |
| Traceability | 0.10 | Negative | CV-001: "four later rounds" is not traceable to four narrated instances in the Context section as written |

---

## Claims Independently Verified Clean

The following load-bearing claims were independently re-checked against primary sources and found accurate (no discrepancy; listed for completeness per the S-011 template's evidence-requirements):

- `skills/adversary/agents/adv-scorer.md:166-167` -- verbatim quote of the current automatic-REVISE rule: confirmed exact.
- `skills/adversary/agents/adv-scorer.md:68-91` (leniency-bias-counteraction section) and `:79` (rule 3, "choose the LOWER one") -- confirmed exact, supports D-1/D-5 rationale citations.
- `skills/adversary/agents/adv-selector.md:109-131` -- Group A-F ordering, H-16 constraint, Group D "Verify" = S-007/S-011, Group F "ALWAYS LAST" -- confirmed exact match to ADR's characterization and naming-collision disclosure.
- Iteration-005 (ADR-convention) score 0.66 REVISE, 10 unresolved Criticals across 4 strategies (S-004: 2, S-001: 3, S-012: 4, S-013: 1) -- confirmed exact (`adversary/iteration-005/s-014-quality-score.md`).
- `subtraction-pass-notes.md:28` -- exact quote match: "each addition became new attack surface — the reviewers then attacked the additions."
- Iteration-008 (ADR-convention): "7 new Criticals," "10 of 10 prior Criticals verified closed (8 delete, 2 edit), 0 recurred" -- confirmed exact at lines 50 and 208 respectively.
- FU-log iteration-006: score 0.460 ESCALATE; non-monotonic trajectory 0.640→0.653→0.587→0.531→0.468→0.460 (i.e., one +0.01 tick at iteration 2, decline every round thereafter) -- independently recomputed from all six iteration score reports (iter-001 through iter-006) and confirmed to exactly match the ADR's L0 characterization ("it ticked up by about 0.01 in one round before declining across the rest").
- Iteration-009 (ADR-convention): 5 VERIFIED / 5 REFUTED of 10 claimed Criticals; "~0.18-point difference... is the quantified value of the VERIFIED-CRITICALS refutation panel" -- confirmed exact quote at line 135.
- FU-log iteration-008: verified 0.72 vs. old 0.51; DA-002-i8 VERIFIED 3-of-3 (dedup keyed on location only, silently dropping edited markers); PM-001-iter8 REFUTED 0-of-3 as a restatement of iteration-3's closed FM-006 -- all confirmed exact.
- The disclosed "18→12" correction: direct enumeration of `fu-log-convention-20260705-001/adversary/iteration-008/verify/` returns exactly 12 files (3 lenses × 4 Critical-bearing reports: S-001, S-002, S-004, S-012) -- confirmed via independent Glob; matches the ADR's corrected figure, not the source report's own self-contradictory "18... × 4" line.
- Iteration-010 (ADR-convention): verified 0.88 vs. old 0.68; 0 VERIFIED / 6 REFUTED; four strategies (002-001, 012-004, 013-001, CV-001-i010) converge on the same grandfather-exemption seam; 013-001 refuted even at the factual layer per its own refutation-factual.md ("the apparent tension is resolved in the same section") -- all confirmed exact, including the 15-file panel count (3 lenses × 5 reports).
- The fabricated-verification incident: `.github/pull_request_template.md` (lowercase) exists since 2026-02-18; the false "Glob-verified absent" claim was reaffirmed at iterations 6, 7, 8, 9 (exact phrasing confirmed present verbatim in the iteration-010 score report itself, not merely the ADR's paraphrase); exposed by RT-001-iter010, an unrefuted Major that never entered a panel -- all confirmed exact against `post-ceiling-fix-notes.md` and `iteration-010/s-014-quality-score.md`.
- All four Mermaid diagrams (`fig1-pipeline.mmd`, `fig2-lifecycle.mmd`, `fig3-stopcondition.mmd`, `fig4-iteration.mmd`) match the ADR's inline fences byte-for-byte, and all four corresponding `.svg` files exist in the `diagrams/` directory, corroborating the "4 mmdc-validated figures... rendered SVGs persisted" claim.
- The `adv-verifier` tool-tier is stated consistently as `T2, Read/Glob/Grep/Write` at every one of its ~10 occurrences in the current ADR body -- no stale "T1 read-only" references remain (the iteration-2 CC-001 correction is fully propagated).
- Current `skills/adversary/SKILL.md` confirms exactly 3 existing workers (adv-selector, adv-executor, adv-scorer), consistent with the ADR's "P-003 hierarchy shows 4 workers" claim once `adv-verifier` is added.

---

## Execution Statistics

- **Total Findings:** 2
- **Critical:** 1
- **Major:** 1
- **Minor:** 0
- **Protocol Steps Completed:** 5 of 5 (Extract Claims, Generate Verification Questions, Independent Verification, Consistency Check, Synthesize and Score Impact)

---

*Report persisted per P-002. Constitutional compliance: P-003 (no subagents invoked); P-020 (all output confined to `projects/PROJ-031-cowork-skeleton/`, deliverable not edited); P-022 (every finding cites file+line evidence from primary tournament-corpus sources; the incidental cross-directory grep hit into `review/iteration-001`/`review/iteration-002` is disclosed above in the Header and was not used as evidence for any finding -- both findings in this report are independently re-derived from primary source files read directly for this execution).*
