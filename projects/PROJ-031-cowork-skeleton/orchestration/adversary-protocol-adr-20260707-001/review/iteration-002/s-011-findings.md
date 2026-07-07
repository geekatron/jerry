# Chain-of-Verification Report: ADR-adversary-tournament-protocol-001 (iteration 2)

## Navigation

| Section | Purpose |
|---------|---------|
| [Execution Context](#execution-context) | Strategy, deliverable, scope |
| [Claim Inventory](#claim-inventory) | Extracted testable claims (CL-NNN) |
| [Verification Questions](#verification-questions) | Questions generated per claim (VQ-NNN) |
| [Independent Verification Results](#independent-verification-results) | Source-only answers |
| [Consistency Check / Findings Summary](#consistency-check--findings-summary) | CV-NNN findings table |
| [Detailed Findings](#detailed-findings) | Full evidence for each finding |
| [Recommendations](#recommendations) | Corrections grouped by severity |
| [Scoring Impact](#scoring-impact) | Mapping to S-014 dimensions |
| [Execution Statistics](#execution-statistics) | Counts |

---

## Execution Context

- **Strategy:** S-011 Chain-of-Verification
- **Deliverable:** `projects/PROJ-031-cowork-skeleton/decisions/ADR-adversary-tournament-protocol-001-verified-criticals-methodology.md`
- **Criticality:** C3 (per commission FU.12; AE-003 new-ADR auto-escalation; the ADR self-declares C3 minimum)
- **Date:** 2026-07-07
- **Reviewer:** adv-executor (S-011 Chain-of-Verification), blind pass
- **H-16 Compliance:** Indirect for CoVe. The deliverable's own Changelog records a prior S-014-scored iteration-1 remediation pass; this blind executor did not receive an S-003 Steelman output and proceeds per S-011's "indirect" ordering constraint (not a strict H-16 violation).
- **Claims Extracted:** 24 (5+ required; representative sample spanning quoted scores/counts, rule citations, cross-references, and behavioral/diagram claims)
- **Verified:** 20 | **Discrepancies (Critical):** 2 | **Discrepancies (Major):** 1 | **Unverifiable:** 0

---

## Claim Inventory

| ID | Claim (deliverable text) | Claimed Source | Type |
|----|---------------------------|-----------------|------|
| CL-01 | Iteration 5 (adr-convention): score 0.66 REVISE, 10 unresolved Criticals across 4 blind reviewers | `.../adr-convention.../iteration-005/s-014-quality-score.md` | Quoted value |
| CL-02 | Iteration 8 (adr-convention): 10/10 prior Criticals CLOSED (8 delete, 2 edit, 0 recurred); 7 brand-new Criticals | `.../adr-convention.../iteration-008/s-014-quality-score.md` | Quoted value |
| CL-03 | Iteration 6 (fu-log): score 0.46, declining, ESCALATE; composite drifted 0.468 -> 0.460 | `.../fu-log.../iteration-006/s-014-quality-score.md` | Quoted value |
| CL-04 | "reliably closes the specific instance of each finding … but has not yet closed the class of problem…" | `.../fu-log.../iteration-006/s-014-quality-score.md:56` | Direct quote |
| CL-05 | Score drifted downward across six rounds; ticked up ~0.01 in one round before declining across the rest | Implicit across fu-log iterations 1-6 | Behavioral/aggregate claim |
| CL-06 | Iteration 9 (adr-convention): verified 0.86 vs old-protocol 0.68; 10 claimed -> 5 VERIFIED / 5 REFUTED | `.../adr-convention.../iteration-009/s-014-quality-score.md` | Quoted value |
| CL-07 | "The ~0.18-point difference between the two protocols is the quantified value of the VERIFIED-CRITICALS refutation panel" | `.../iteration-009/s-014-quality-score.md:135` | Direct quote |
| CL-08 | Iteration 8 (fu-log): verified 0.72 vs old 0.51; panels CONFIRMED 6 real Criticals incl. DA-002-i8 (fix-introduced regression, dedup keyed on location only, 3-of-3 unanimous) | `.../fu-log.../iteration-008/s-014-quality-score.md` | Quoted value + behavioral claim |
| CL-09 | Same panel REFUTED PM-001-iter8 0-of-3 as a restatement of iteration-3's already-closed FM-006 | `.../fu-log.../iteration-008/s-014-quality-score.md` | Quoted value |
| CL-10 | Iteration 10 (adr-convention): verified 0.88, 0 VERIFIED Criticals; all 6 claimed REFUTED 2-of-3; reached RT-M-010 ceiling | `.../adr-convention.../iteration-010/s-014-quality-score.md` | Quoted value |
| CL-11 | Four independent strategies re-derived the same grandfather-exemption seam — recurrence the panels confirmed was factually real but immaterial | `.../iteration-010/s-014-quality-score.md:56` | Direct quote / behavioral claim |
| CL-12 | Fabricated-verification incident: "no PR template — Glob-verified" was false; PR template existed at lowercase path since 2026-02-18; reaffirmed iterations 6,7,8,9; **caught only by the iteration-10 refutation panel's factual lens** | `.../iteration-010/post-ceiling-fix-notes.md:55-65` | Behavioral/causal claim |
| CL-13 | Disclosed correction: "18 verification-panel files" corrected to 12 (3 lenses x 4 Critical-bearing reports) for fu-log iteration 8 | `.../fu-log.../iteration-008/verify/` | Quoted count |
| CL-14 | c-004: iter-9 = 15 files (3 lenses x 5 Criticals) | `.../adr-convention.../iteration-009/verify/` | Quoted count |
| CL-15 | Combined 18 tournament rounds across 2 packages (~250 agent invocations) | Aggregate across both orchestration dirs | Aggregate/quoted count |
| CL-16 | Current automatic-REVISE rule: "Any Critical finding from adv-executor reports → automatic REVISE regardless of score" | `skills/adversary/agents/adv-scorer.md:166-167` | Rule citation |
| CL-17 | H-16 constraint + Group F "ALWAYS LAST" ordering preserved | `skills/adversary/agents/adv-selector.md:112-128` | Rule citation |
| CL-18 | HARD-rule ceiling stays at 25/25; no HARD rule touched | `.context/rules/quality-enforcement.md` | Rule citation |
| CL-19 | Figure 1: Verify stage sits between finder Groups A-E and Group F, gated on criticality | ADR Fig. 1 (own diagram) | Behavioral/diagram claim |
| CL-20 | Figure 2: Verified Criticals unconditionally flow to AutoReviseGate -> Remediated | ADR Fig. 2 (own diagram) | Behavioral/diagram claim |
| CL-21 | Figure 3: stop-condition decision tree routes VERIFIED Criticals through a recurrence check (Q2) before remediation | ADR Fig. 3 (own diagram) | Behavioral/diagram claim |
| CL-22 | D-2: "Only panel-VERIFIED Criticals trigger automatic-REVISE" (unconditional on recurrence) | ADR Decision table, D-2 | Rule/decision claim |
| CL-23 | 5 of 6 surviving fu-log iteration-8 Criticals were materiality-refuted yet still passed 2-of-3 | `.../fu-log.../iteration-008/s-014-quality-score.md` | Quoted value |
| CL-24 | Old-protocol composite ~0.68 for both iteration 9 and iteration 10 (adr-convention) | Both iteration score reports | Quoted value |

---

## Verification Questions

- VQ-01..VQ-10: Do the cited score reports state the exact figures/verdicts claimed in CL-01, CL-02, CL-03, CL-06, CL-08, CL-09, CL-10, CL-23, CL-24? (Read each report directly.)
- VQ-11: Does `s-014-quality-score.md:56` (fu-log iter-6) contain the exact quoted sentence in CL-04?
- VQ-12: Across fu-log iterations 1-6, what is the actual per-iteration composite sequence, and does it match the "ticked up ~0.01 once, then declined" characterization (CL-05)?
- VQ-13: Does `s-014-quality-score.md:135` (adr-convention iter-9) contain the exact quoted sentence in CL-07?
- VQ-14: Does `s-014-quality-score.md:56` (adr-convention iter-10) support the claim that "every refutation panel confirmed the factual core is real" for all four convergent findings (CL-11)?
- VQ-15: Who/what actually caught the fabricated PR-template claim in iteration 10 — a refutation-panel lens, or a finder-strategy report (CL-12)?
- VQ-16: Does `adr-convention/.../iteration-009/verify/` contain exactly 15 files, and `fu-log/.../iteration-008/verify/` exactly 12 files (CL-13, CL-14)?
- VQ-17: How many `s-014-quality-score.md` files exist under each orchestration directory, and does the sum equal 18 (CL-15)?
- VQ-18: Does `adv-scorer.md` contain the exact quoted rule text at lines 166-167 (CL-16)?
- VQ-19: Does `adv-selector.md:112-128` contain the H-16 constraint and Group-F-last ordering (CL-17)?
- VQ-20: Does Figure 3's routing logic (CL-21) match D-2's unconditional gating rule (CL-22) and Figure 2's unconditional pathway (CL-20)?

---

## Independent Verification Results

All of CL-01, CL-02, CL-03, CL-06, CL-08, CL-09, CL-10, CL-13, CL-14, CL-16, CL-17, CL-18, CL-23, CL-24 were independently re-derived from the cited primary files (read in full) and matched the deliverable's characterization exactly (exact scores, exact verdicts, exact counts, exact file counts, exact rule text). No fabrication found in this set.

**VQ-11 (CL-04):** `fu-log/.../iteration-006/s-014-quality-score.md` ESCALATE Rationale paragraph reads verbatim: *"a wording-only remediation process reliably closes the specific instance of each finding (confirmed again this round — zero regressions across 6 rounds) but has not yet closed the class of problem that keeps producing fresh Critical-severity instances on each new blind pass."* Exact match. **VERIFIED.**

**VQ-12 (CL-05):** Direct reads of iterations 1-6 composites: iter-1 = 0.64, iter-2 = 0.65 (Delta +0.01), iter-3 = 0.59 (-0.06), iter-4 = 0.53 (-0.057), iter-5 = 0.468 (-0.063), iter-6 = 0.460 (-0.008). Sequence: 0.64 -> 0.65 -> 0.59 -> 0.53 -> 0.468 -> 0.460. This is exactly "ticked up ~0.01 once (iter1->iter2), then declined across the rest." **VERIFIED** — a precise, accurate characterization of a non-monotonic trend (this itself corrects an iteration-1 draft error per the deliverable's own changelog, and the correction holds up under re-verification).

**VQ-13 (CL-07):** `adr-convention/.../iteration-009/s-014-quality-score.md` "Why the gap matters" paragraph reads: *"The ~0.18-point difference between the two protocols is the quantified value of the VERIFIED-CRITICALS refutation panel for this package…"* Exact match at the cited location. **VERIFIED.**

**VQ-14 (CL-11):** `adr-convention/.../iteration-010/s-014-quality-score.md:56` states: *"four of the six claimed Criticals (002-001, 012-004, 013-001, CV-001-i010) independently converge… Every refutation panel confirmed the factual core is real (the textual tension exists)…"* However, the same report's own Verified-Criticals Disposition table (line ~53) shows **013-001's factual-accuracy lens vote as REFUTED**, not VERIFIED — i.e., NOT confirmed real by that item's own factual lens. Independent read of the underlying panel file (`iteration-010/verify/s-013 inversion technique-refutation-factual.md`) confirms this explicitly: its verdict is REFUTED, with the reasoning stating the apparent tension "does not hold up" and is "resolved in the same section" — i.e., that specific panel explicitly denies a genuine textual tension exists for 013-001, contradicting the score report's own summary sentence for that item. **DISCREPANCY (see CV-003).**

**VQ-15 (CL-12):** Cross-checked against `iteration-010/s-014-quality-score.md`'s own tables. The six claimed Criticals actually run through the 3-lens refutation panel in iteration 10 are: 002-001, 002-002, 004-001, 012-004, 013-001, CV-001-i010. The fabricated PR-template claim is tracked as **"RT-001-iter010"**, which the same report lists under **"Unrefuted Majors/Minors (Advisory)"** — explicitly a Major, not a Critical, and explicitly **not** one of the six panel-adjudicated Criticals. Per the report's own protocol statement ("no refutation panel runs against non-Critical findings under this protocol," consistent with the iteration-8 fu-log report's identical rule), RT-001-iter010 never passed through any refutation panel. It originates as an **S-001 Red Team** finder-strategy finding (an ordinary Group-C "Challenge" strategy that predates and is independent of the new Verify-stage mechanism this ADR proposes). `post-ceiling-fix-notes.md` Cluster 3 confirms the same attribution ("RT-001-iter010" as the finding ID) without crediting any panel. **DISCREPANCY (see CV-001).**

**VQ-16/17:** Confirmed by direct file enumeration: `iteration-009/verify/` = 15 files (3 lenses x 5 Criticals: S-001, S-002, S-004, S-011, S-012); `fu-log/iteration-008/verify/` = 12 files (3 lenses x 4 Criticals: S-001, S-002, S-004, S-012); `adr-convention` has 10 `s-014-quality-score.md` files (iterations 1-10); `fu-log` has 8 (iterations 1-8, excluding the non-scored `iteration-007-aborted-api-errors`). Sum = 18. **VERIFIED** for all three.

**VQ-18:** `skills/adversary/agents/adv-scorer.md` lines 165-167 read verbatim: *"Special cases: - Any Critical finding from adv-executor reports → automatic REVISE regardless of score"* **VERIFIED** exact match.

**VQ-19:** `skills/adversary/agents/adv-selector.md` lines 112-128 contain the H-16 constraint ("S-003 … MUST be ordered BEFORE S-002") and the Group A-F ordering table ending "Group F — Score: S-014 (LLM-as-Judge) — ALWAYS LAST." **VERIFIED** exact match.

**VQ-20 (CL-19..CL-22):** Figure 2's state diagram shows an unconditional path: `Verified --> AutoReviseGate: blocks PASS regardless of composite` then `AutoReviseGate --> Remediated: owner subtraction-first pass` — no conditional branch. D-2 (Decision table) states: *"Only panel-VERIFIED Criticals trigger automatic-REVISE"* — also unconditional on recurrence. Figure 3, however, routes any round with `Q1: Any VERIFIED Criticals this round? = Yes` into `Q2: Do findings RECUR across independent rounds?`. If `Q2 = No` (fresh stream) AND `Q3: Running verified protocol already? = Yes`, the flow goes directly to `Q4` (ceiling check) — **bypassing the `FIX` (remediation) node entirely.** This means a VERIFIED Critical that does not recur across rounds, while already on the verified protocol, has no path to remediation in Figure 3, contradicting both D-2's unconditional gating rule and Figure 2's own unconditional Verified -> Remediated pathway. **DISCREPANCY (see CV-002).**

---

## Consistency Check / Findings Summary

| ID | Claim | Source | Discrepancy | Severity | Affected Dimension |
|----|-------|--------|-------------|----------|---------------------|
| CV-001-20260707 | "caught only by the iteration-10 refutation panel's factual lens" (fabricated PR-template incident) | `.../iteration-010/post-ceiling-fix-notes.md:55-65`; `.../iteration-010/s-014-quality-score.md` | The catch is attributed to the NEW Refutation-Panel Verify stage, but the finding (RT-001-iter010) is an ordinary S-001 Red Team finder report, explicitly classified as an unrefuted Major that never entered any refutation panel (panels only adjudicate Criticals) | **Critical** | Evidence Quality / Internal Consistency |
| CV-002-20260707 | Figure 3 stop-condition decision tree | ADR Fig. 2 (own diagram); ADR Decision table D-2 | Fig. 3 permits a VERIFIED Critical (no cross-round recurrence, already on verified protocol) to bypass the FIX/remediation node entirely, contradicting D-2's unconditional gating rule and Fig. 2's unconditional Verified->Remediated pathway | **Critical** | Internal Consistency / Methodological Rigor |
| CV-003-20260707 | "Every refutation panel confirmed the factual core is real" (4-strategy grandfather-seam convergence) | `.../iteration-010/s-014-quality-score.md:56`; `.../iteration-010/verify/s-013 inversion technique-refutation-factual.md` | Overstated for 013-001: its own factual-accuracy lens voted REFUTED and its reasoning explicitly denies a genuine textual tension exists (calls the conclusion, not merely the severity, unsupported) | **Major** | Evidence Quality |

---

## Detailed Findings

### CV-001-20260707: Flagship "fabricated-verification" anecdote misattributes the catching mechanism [CRITICAL]

**Claim (from deliverable):** "The false negative came from an exact-uppercase-case search, was reaffirmed across iterations 6, 7, 8, and 9, and was **caught only by the iteration-10 refutation panel's factual lens** (`.../adversary/iteration-010/post-ceiling-fix-notes.md:55-65`). A self-attested 'verified' claim survived four blind rounds; only an *independent* factual lens exposed it." This attribution is repeated in the L1 Technical Implementation section ("Factual-accuracy lens … This is the lens that would have caught the fabricated PR-template claim") and in the Decision Rationale paragraph ("Adding an independent 3-lens refutation gate is the single intervention that demonstrably reversed this … correctly discarded restatements and one false claim").

**Source Document:** `projects/PROJ-031-cowork-skeleton/orchestration/adr-convention-20260702-001/adversary/iteration-010/s-014-quality-score.md` (Verified-Criticals Disposition table and Unrefuted Majors/Minors table); `.../iteration-010/post-ceiling-fix-notes.md`.

**Independent Verification:** Iteration 10's refutation panel adjudicated exactly six claimed Criticals: 002-001, 002-002, 004-001, 012-004, 013-001, CV-001-i010 — none of which is the PR-template claim. The PR-template finding is tracked as **RT-001-iter010**, sourced from **S-001 Red Team** (a Group-C "Challenge" finder strategy, not the new Verify-stage), and is explicitly listed in the score report's own "Unrefuted Majors/Minors (Advisory)" table as a **Major**, with the note that "no refutation panel runs against non-Critical findings under this protocol." `post-ceiling-fix-notes.md` Cluster 3 confirms the same finding ID and strategy attribution without crediting any panel mechanism.

**Discrepancy:** The deliverable's central evidentiary anecdote for why an *independent verification-panel stage* (D-1/D-6, the ADR's core proposed innovation) is necessary is, on independent verification, actually a story about an **ordinary blind finder-strategy rotation** (S-001 Red Team) catching a stale claim that a *different* finder (S-004/S-012, iteration 6) and a CoVe verification question (iteration 7, "VQ-019") had both missed or left unchallenged. This demonstrates that the existing tournament's blind, rotating multi-strategy design — with zero new machinery — already possesses the "independence" property the ADR credits exclusively to the proposed new adv-verifier panel. The misattribution is repeated at three separate locations in the document (Context section, L1 Item 2, Decision Rationale), compounding its weight as supporting evidence for D-1/D-6.

**Severity:** Critical — this is the deliverable's single most emphasized concrete evidentiary anecdote ("The strongest argument for *independent* verification is a concrete failure"). Because the actual record shows an existing mechanism (blind finder rotation) already caught this exact failure mode without the new machinery, the anecdote does not support the causal claim it is used to establish, undermining evidence-decision traceability for D-1/D-6.

**Dimension:** Evidence Quality (primary); Internal Consistency (the claim is inconsistent with the same iteration's own Critical-vs-Major classification tables).

**Correction:** Re-attribute the discovery to "an ordinary blind S-001 Red Team finder pass in iteration 10 (RT-001-iter010), independent of and prior to any refutation panel." If the ADR wishes to retain this incident as supporting evidence for the Verify stage, it should instead argue (with appropriate hedging) that the incident demonstrates the *general* value of continued blind multi-strategy re-examination — not that the specific new panel mechanism caught it — or find/cite a different incident where a refutation panel's factual lens was the actual catching mechanism (e.g., the fu-log iteration-8 DA-002-i8 catch is a stronger, verifiably panel-adjudicated example already cited elsewhere in the ADR and does not need this correction).

---

### CV-002-20260707: Figure 3 permits a VERIFIED Critical to bypass remediation, contradicting D-2 and Figure 2 [CRITICAL]

**Claim (from deliverable, Figure 3):** `Q1{"Any VERIFIED Criticals this round?"} -- "Yes" --> Q2{"Do findings RECUR across independent rounds?"}`; `Q2 -- "No: fresh stream every round (protocol artifact)" --> Q3{"Running verified protocol already?"}`; `Q3 -- "Yes" --> Q4{"RT-M-010 ceiling reached?"}` — with no edge from this path into the `FIX["Owner subtraction-first remediation pass"]` node.

**Source Document:** The deliverable itself — Figure 2 (`stateDiagram-v2`, Finding lifecycle) and the D-2 Decision-table row, both within `projects/PROJ-031-cowork-skeleton/decisions/ADR-adversary-tournament-protocol-001-verified-criticals-methodology.md`.

**Independent Verification:** Figure 2 states unconditionally: `Verified --> AutoReviseGate: blocks PASS regardless of composite` then `AutoReviseGate --> Remediated: owner subtraction-first pass` — no recurrence-conditional branch of any kind. D-2's Decision-table entry states: "Only panel-VERIFIED Criticals trigger automatic-REVISE… Refuted claims carry zero weight… Disclosed residuals are valid MEDIUM posture, not findings" — again, gating is unconditional once a Critical is VERIFIED; nothing in D-2's text conditions remediation on whether the VERIFIED Critical recurs across rounds.

**Discrepancy:** Figure 3, by contrast, inserts a "does this recur across rounds" gate (Q2) *after* confirming a VERIFIED Critical exists (Q1=Yes), and for the "fresh stream, already on verified protocol" branch (Q2=No, Q3=Yes) routes straight to the ceiling check (Q4) with **no path through FIX**. Taken literally, this specification would let a genuinely VERIFIED Critical (by definition already passed a 2-of-3 independent panel) go unremediated simply because it happened not to recur in a prior round — directly contradicting D-2's unconditional rule and Figure 2's own unconditional pathway. The Q2/Q3 recurrence heuristic described in the D-4 prose ("recurrence across rounds marks a real defect… a fresh non-overlapping crop marks a protocol artifact") is evidently intended to describe how to treat *claimed-but-not-yet-independently-verified* Criticals in the pre-panel era (i.e., a heuristic substitute for verification before the Verify stage exists) — not a second gate applied *after* a Critical has already cleared the panel. As drawn, Figure 3 conflates these two distinct scenarios into one flowchart, producing an implementable specification that a WI-4/WI-5 implementer could build exactly as diagrammed, silently reintroducing the "unresolved Critical claims counted as non-issues" failure mode the whole ADR exists to close.

**Severity:** Critical — this is one of the four "mmdc-validated" figures central to the Decision section, and the defect is a workflow-correctness gap directly affecting "implementable specification," one of the three fitness criteria this review was instructed to weight.

**Correction:** Either (a) remove the Q2/Q3 recurrence branch from the post-verification path entirely, so `Q1=Yes` routes unconditionally to `FIX` (matching D-2 and Figure 2), reserving the recurrence heuristic explicitly for a documented *pre-Verify-stage* fallback mode (e.g., C1/C2 rounds or a transition period before D-6 ships); or (b) if the recurrence check is intentionally meant to also apply post-verification for some other reason (e.g., prioritizing already-recurring VERIFIED Criticals over one-off ones), add an explicit edge from the "No: fresh stream" + "Yes: already verified protocol" branch into `FIX` as well, so no VERIFIED Critical is ever routed around remediation.

---

### CV-003-20260707: "Every refutation panel confirmed the factual core is real" overstates the iteration-10 grandfather-seam convergence [MAJOR]

**Claim (from deliverable):** "Notably, four independent strategies re-derived the *same* grandfather-exemption seam — recurrence that the panels confirmed was factually real but immaterial (`.../iteration-010/s-014-quality-score.md:56`)."

**Source Document:** `projects/PROJ-031-cowork-skeleton/orchestration/adr-convention-20260702-001/adversary/iteration-010/s-014-quality-score.md` line ~56 ("Every refutation panel confirmed the factual core is real (the textual tension exists)"); `.../iteration-010/verify/s-013 inversion technique-refutation-factual.md` (the underlying panel file for one of the four cited findings, 013-001).

**Independent Verification:** The cited score-report sentence is accurate as a *quote* (the ADR faithfully reproduces it), but it does not survive independent re-verification against its own supporting panel file. For `013-001` (one of the four convergent findings named: 002-001, 012-004, 013-001, CV-001-i010), the **factual-accuracy lens itself voted REFUTED**, and its written reasoning states that the cited text, while accurately quoted, "does not establish a 'genuine internal contradiction' under a fair reading of the section as a whole" and that the "apparent tension is resolved in the same section." This is a stronger disagreement than "factually real but immaterial" — this specific panel explicitly denies that a genuine textual tension exists at all for this item, rather than confirming the tension is real but merely low-materiality.

**Discrepancy:** The ADR's characterization applies a uniform "confirmed factually real" label to all four convergent findings, when one of the four (013-001) had its own factual lens dispute the underlying premise entirely (not merely its severity). This is an internal inconsistency inherited from the cited score report itself (whose own summary prose at line 56 does not match its own Verified-Criticals Disposition table, which lists 013-001's factual-accuracy verdict as REFUTED) — precisely the "verify before you count" failure class this ADR argues against, reproduced here without an independent check against the underlying panel file.

**Severity:** Major — the recurring-seam observation remains substantively true for the other three of four findings and the overall "recurrence, not raw count, is the signal" argument in the Context section is not invalidated; but the specific "every… confirmed" framing is inaccurate and should be corrected to avoid overstating panel unanimity.

**Correction:** Reword to "three of the four findings' factual-accuracy lenses confirmed the underlying textual tension is real (though immaterial); the fourth (013-001) was refuted even at the factual layer, its panel concluding the apparent tension is resolved by an adjacent paragraph the finder's own citation already includes" — or drop the "every… confirmed" framing and cite only the three items that actually support it.

---

## Recommendations

**Critical (MUST correct before acceptance):**
- CV-001-20260707: Correct the attribution of the fabricated PR-template catch at all three locations (Context section, L1 Item 2, Decision Rationale) to name the actual mechanism (S-001 Red Team finder, iteration 10), and either drop or substantially reframe the causal argument this anecdote is used to support for D-1/D-6.
- CV-002-20260707: Fix Figure 3's routing so no VERIFIED Critical can reach the ceiling-check (Q4) without first passing through the FIX/remediation node, consistent with D-2 and Figure 2.

**Major (SHOULD correct):**
- CV-003-20260707: Reword the "every refutation panel confirmed the factual core is real" sentence to accurately reflect that 013-001's own factual lens refuted the underlying premise, not merely its materiality.

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Neutral | Not affected by these findings |
| Internal Consistency | 0.20 | Negative | CV-002 (Fig. 3 vs. D-2/Fig. 2 contradiction); CV-003 (ADR's own source-summary sentence contradicts its own source table) |
| Methodological Rigor | 0.20 | Negative | CV-002 undermines the soundness of the D-4 stop-condition specification as drawn |
| Evidence Quality | 0.15 | Negative | CV-001 is the primary driver — the flagship anecdote for D-1/D-6 misattributes its own cited evidence |
| Actionability | 0.15 | Neutral | Both Critical findings have concrete, narrowly-scoped corrections requiring no new machinery |
| Traceability | 0.10 | Negative | CV-001 and CV-003 both stem from insufficiently independent re-verification of a cited source's own internal tables against its own prose summaries |

---

## Execution Statistics

- **Total Findings:** 3
- **Critical:** 2
- **Major:** 1
- **Minor:** 0
- **Claims Extracted:** 24 (20 independently verified clean, 0 fabrications among the purely-numeric/quoted-value claims; the 2 Critical + 1 Major findings are all behavioral/causal-attribution or diagram-consistency claims)
- **Protocol Steps Completed:** 5 of 5 (Extract Claims, Generate Verification Questions, Independent Verification, Consistency Check, Synthesize and Score Impact)

*No subagents spawned (P-003). No files edited outside this report's output path (P-020). All evidence cited by repo-relative file path; interpretive judgments (severity placement, dimension-impact assessment) are labeled as this executor's judgment, not independently-verified fact (P-022). Report persisted incrementally per P-002.*
