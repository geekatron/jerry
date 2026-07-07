# Devil's Advocate Report: ADR-adversary-tournament-protocol-001 (Verified-Criticals Tournament Methodology)

## Document Sections

| Section | Purpose |
|---------|---------|
| [Header](#header) | Strategy metadata and H-16 compliance |
| [Summary](#summary) | Overall assessment |
| [Findings Table](#findings-table) | All DA-NNN findings at a glance |
| [Finding Details](#finding-details) | Expanded Critical/Major findings with evidence |
| [Recommendations](#recommendations) | P0/P1/P2 prioritized actions |
| [Scoring Impact](#scoring-impact) | Mapping to S-014 dimensions |

---

## Header

**Strategy:** S-002 Devil's Advocate
**Deliverable:** `projects/PROJ-031-cowork-skeleton/decisions/ADR-adversary-tournament-protocol-001-verified-criticals-methodology.md` (iteration 2 / v0.2)
**Criticality:** C3 (auto-escalated per c-007 / AE-003; the ADR itself is under a C3+ tournament)
**Date:** 2026-07-07
**Reviewer:** adv-executor (S-002 Devil's Advocate)
**H-16 Compliance:** This review is invoked as the "challenge" group of a six-group sequential tournament order (self-refine -> steelman -> challenge -> verify -> decompose -> score) per the orchestrating context; the S-003 Steelman group is specified to run before this "challenge" group. This executor is blind to the actual `iteration-002/review/` directory contents (including any S-003 output file) per its task constraints, so **direct confirmation of the S-003 artifact could not be performed** — this compliance statement is an **inference** from the stated orchestration order, not a verified read of an S-003 output file. Flagged for the scorer's attention, not treated as a blocking H-16 violation given the orchestration context explicitly assigns strategy order.

---

## Summary

Six counter-arguments identified (3 Critical, 2 Major, 1 Minor). The ADR is unusually self-aware about its own evidentiary limits (it already discloses the all-C4 evidence base, the n=2 external-validity risk, and the discard-biased nature of DEFAULT-REFUTED) — but that same self-awareness is inconsistently applied. Three passages **assert as settled fact** claims the ADR's own analysis elsewhere concedes are unproven: (1) the empirical arithmetic behind the "3 lens-invocations per claimed Critical" cost model does not reconcile with the claimed-Critical counts the ADR itself narrates for the same two rounds; (2) a Positive Consequence states the spiral "actually occurs" only at C3/C4, directly contradicting the ADR's own D-1 disclaimer that the C1-C2 exemption is a cost decision, not an evidentiary finding; (3) the work-item dependency graph does not actually gate "framework-general" adoption (WI-7) on the non-ADR-genre validation pass (WI-8) that RSK-7's mitigation explicitly promises. These three findings directly undermine the "evidence-decision traceability" and "honest costs/limits" fitness criteria this tournament is evaluating against. Recommend REVISE.

---

## Findings Table

| ID | Finding | Severity | Evidence | Affected Dimension |
|----|---------|----------|----------|--------------------|
| DA-001-i2 | Cost-model empirical basis does not reconcile: cited panel-file multipliers ("4", "5") are alternately labeled claimed-Criticals and Critical-bearing-reports for the same data, and neither reconciles with the round's own narrated claimed-Critical count | Critical | Lines 146-147, 154-161, 166, 217, 385-386, 659-660, 762 | Evidence Quality |
| DA-002-i2 | Positive Consequence #4 asserts as fact that the spiral "actually occurs" only at C3/C4, directly contradicting D-1's own disclaimer that the C1-C2 exemption is "not a finding that C1-C2 'did not spiral'" | Critical | Lines 226-228, 282-284, 705-706 | Internal Consistency |
| DA-003-i2 | RSK-7's textual promise ("before the protocol is treated as framework-general") is not enforced by the work-item dependency graph: WI-7 does not depend on WI-8 | Critical | Lines 747, 762-769 | Traceability |
| DA-004-i2 | The "structural closure" cited for two HIGH-impact risks (RSK-1, RSK-2) is an unscheduled, out-of-scope future phase with zero corresponding work item | Major | Lines 680-684, 741-742, 762-769 | Actionability |
| DA-005-i2 | RSK-4's stated mitigations do not bound the risk they name (a single Critical-heavy round/report) | Major | Line 744, Section "L1 Technical Implementation" (lines 598-661) | Actionability |
| DA-006-i2 | D-1's numeric score gap (C=9 vs B=6) implies a confidence differential the surrounding prose explicitly disclaims | Minor | Lines 257-259, 271-288 | Methodological Rigor |

**Finding ID Format:** `DA-{NNN}-i2` (execution_id `i2` = tournament iteration 2, per this review's context).

---

## Finding Details

### DA-001-i2: Cost-model empirical basis does not reconcile with the ADR's own narrated Critical counts [CRITICAL]

**Claim Challenged:** The ADR's central cost-honesty claim rests on c-004 ("panels ≈ 3 agent runs -- one per lens -- per claimed Critical") and its two empirical anchors: *"iter-9: 15 files = 3 lenses × 5 Criticals; iter-8 FU: 12 files = 3 lenses × 4 Criticals"* (line 217, repeated at lines 385-386). The L1 section states the invocation contract identically: *"the unit of verification work is one claimed Critical, adjudicated by one invocation per lens... a report with k claimed Criticals produces 3 × k verifier runs"* (lines 608-611), and WI-1's acceptance criteria requires *"one-invocation-per-lens-per-claimed-Critical contract"* (line 762) as the thing to be built.

**Counter-Argument:** The ADR's own Context section narrates claimed-Critical *counts* for these same two rounds that do not match the multipliers ("5" and "4") used in the cost-model arithmetic:
- **Iteration 9:** *"Of 10 claimed Criticals, 5 were VERIFIED and 5 REFUTED"* (paraphrased, lines 146-147, citing `.../iteration-009/s-014-quality-score.md:36-37, 128-135`). That is **10** claimed Criticals total. If the proposed "3 x every claimed Critical" model had actually produced the cited 15 files, the expected count is 3 x 10 = **30**, not 15. Fifteen is exactly half of that.
- **Iteration 8 (FU-log):** *"The panels CONFIRMED 6 real Criticals -- including `DA-002-i8`... The same panel REFUTED `PM-001-iter8`"* (lines 154-159). That is at minimum **6 VERIFIED + 1 named REFUTED = 7** claimed Criticals (very likely more, since only one REFUTED example is named). If "3 x every claimed Critical" produced the cited 12 files, expected is at least 3 x 7 = **21**, not 12.
- Compounding the ambiguity, the disclosed-correction footnote for this *exact same iter-8 FU datum* labels its multiplier differently from every other citation of it: *"12 files (= 3 lenses × 4 **Critical-bearing reports**)"* (line 166) -- "reports," not "Criticals" -- while lines 217 and 385-386 label the identical "4" as "**Criticals**." These are not interchangeable units unless every report happened to contain exactly one claimed Critical, which the round's own narrative (>=7 claimed Criticals) makes implausible for only 4 reports unless some reports carried multiple Criticals that were evidently *not* each given their own 3-lens pass.

**Evidence:** `projects/PROJ-031-cowork-skeleton/decisions/ADR-adversary-tournament-protocol-001-verified-criticals-methodology.md:146-147, 154-161, 166, 217, 385-386, 608-611, 659-660, 762`.

**Impact:** If the true empirical unit was "per Critical-bearing report" (as line 166 states) rather than "per claimed Critical" (as lines 217, 385-386, 608-611, and WI-1's acceptance criteria all specify going forward), the proposed protocol is **untested at the granularity it will actually operate at**, and the "Empirically ~12-15 verifier files per C4 round" claim (line 659-660) -- which the Alignment table's Implementation Effort rating and RSK-4's mitigation both lean on -- may **understate future per-round cost by roughly 2x** whenever a report contains more than one claimed Critical (the norm, per the round narratives cited above). This is precisely the "verify before you count" failure the ADR itself names and corrects elsewhere (the disclosed 18->12 correction, lines 163-170) -- but the correction fixed the *number* while leaving the *unit* (report vs. Critical) unreconciled.

**Dimension:** Evidence Quality (secondary: Internal Consistency)

**Response Required:** Reconcile, with a citation, whether the empirical "4" (iter-8 FU) and "5" (iter-9) multipliers denote claimed Criticals or Critical-bearing reports, and re-derive the per-round cost estimate under whichever unit the future protocol will actually use (per-claimed-Critical, per WI-1). If the empirical rounds in fact ran per-report (not per-Critical) panels, disclose that the going-forward per-Critical model is **untested** and provide a revised, not-yet-validated cost estimate rather than presenting "~12-15" as an empirically confirmed figure for the adopted model.

**Acceptance Criteria:** The Cost model subsection and c-004 state, with file+line citations to the raw panel-file listings (not the summary score reports), the exact number of claimed Criticals AND the exact number of Critical-bearing reports for both cited rounds, and explicitly reconcile any discrepancy between the "per Critical" and "per report" framing before either is used to justify the go-forward cost claim.

---

### DA-002-i2: Positive Consequence #4 asserts as fact what D-1 explicitly disclaims [CRITICAL]

**Claim Challenged:** *"4. **Cost proportionality.** C1-C2 work pays nothing; the panel budget concentrates on C3/C4 governance where **the spiral actually occurs**."* (lines 705-706, emphasis added).

**Counter-Argument:** This directly contradicts the ADR's own, more careful statement made earlier in the same document, in D-1's rationale for choosing Option C over Option B: *"the C1-C2 exemption is a cost-proportionality default... **not** a finding that C1-C2 'did not spiral.'"* (lines 282-284). One passage states as an empirical fact that the spiral is a C3/C4 phenomenon; the other explicitly disclaims that framing as unfounded. Compounding this, the ADR's own Forces section identifies the root cause as criticality-agnostic: *"Finder incentive vs. truth. Blind finders are rewarded for volume; without a counter-force they manufacture a steady stream of Critical claims **regardless of the document's real state**"* (lines 226-228) -- a mechanism description that says nothing about file count, reversibility window, or any other criticality-defining attribute. If the mechanism that causes the spiral is inherent to *any* blind, volume-rewarded tournament, the "spiral actually occurs [at C3/C4]" claim in the Positive Consequences is not merely optimistic framing -- it is the specific overclaim the ADR's own D-1 section was careful to avoid.

**Evidence:** `projects/PROJ-031-cowork-skeleton/decisions/ADR-adversary-tournament-protocol-001-verified-criticals-methodology.md:226-228, 282-284, 705-706`.

**Impact:** A reader who encounters the Consequences section (a natural place to summarize the ADR's net effect) without cross-referencing D-1's more careful language will conclude -- incorrectly, by the ADR's own admission elsewhere -- that C1-C2 work has been evidence-shown not to need verification. This misrepresents the actual, honestly narrower claim (a cost trade-off under an *untested* assumption) as an empirical result, which is a direct Internal Consistency defect and undermines the "evidence-led" self-description (c-005) the ADR claims for itself.

**Dimension:** Internal Consistency

**Response Required:** Rewrite the Positive Consequence #4 bullet to match D-1's honest framing, e.g.: "the panel budget concentrates on C3/C4 governance, where the record was actually observed; the C1-C2 exemption is a cost decision, not an evidence-based finding that C1-C2 tournaments do not exhibit the same spiral."

**Acceptance Criteria:** No passage outside D-1's own qualified discussion states or implies, without the same hedge, that the spiral is empirically confined to C3/C4.

---

### DA-003-i2: RSK-7's mitigation is not enforced by the work-item dependency graph [CRITICAL]

**Claim Challenged:** RSK-7 ("External-validity of the evidence base... n=2 governance/ADR-genre packages... generalize framework-wide to all C3/C4 deliverable genres") states its mitigation as: *"WI-8's validation pass is **required** to include at least one non-ADR-genre C3/C4 deliverable... before the protocol is treated as framework-general"* (line 747).

**Counter-Argument:** The Work-Item Decomposition table's "Depends on" column does not encode this gate. **WI-7** ("`quality-enforcement.md` Implementation-section pointer" -- the artifact that operationalizes framework-general adoption, since it is what points the SSOT at the new protocol) lists its dependencies as **"WI-2, WI-3"** only (line 768). **WI-8** ("Validation pass... including one non-ADR-genre case") lists its own dependencies as **"WI-1..WI-5"** (line 769) -- it does not appear as an upstream dependency *of* WI-7, and nothing in WI-7's row references WI-8. As specified, WI-7 can be completed -- and the `quality-enforcement.md` SSOT pointer added, which is the concrete act of "treating the protocol as framework-general" -- **before WI-8 ever runs**, silently defeating the exact safeguard RSK-7 names as its mitigation.

**Evidence:** `projects/PROJ-031-cowork-skeleton/decisions/ADR-adversary-tournament-protocol-001-verified-criticals-methodology.md:747 (RSK-7), 762-769 (Proposed backlog table, "Depends on" column)`.

**Impact:** This is not a cosmetic sequencing nit -- RSK-7 is explicitly rated Probability MED / Impact MED and is the ADR's only defense against the n=2, maximally-correlated evidence base the task's own attack vector calls out. A mitigation that is asserted in prose but absent from the actual implementable specification (the dependency table other work items *do* use to gate execution, e.g., WI-3 -> WI-1, WI-4 -> WI-2) is not a real bound on the overfitting risk; it is a bound in narrative only.

**Dimension:** Traceability

**Response Required:** Add WI-8 as an explicit dependency of WI-7 (or otherwise state in WI-7's acceptance criteria that the SSOT pointer MUST NOT land until WI-8's non-ADR-genre validation has run and its results are attached), so the "before the protocol is treated as framework-general" language in RSK-7 is actually enforced by the plan a team would execute.

**Acceptance Criteria:** WI-7's row (or its acceptance criteria text) names WI-8 as a precondition, and RSK-7's mitigation text and the dependency table are made to agree without requiring the reader to cross-reference two non-adjacent sections to notice the gap.

---

### DA-004-i2: The cited "structural closure" for two HIGH-impact risks is unscheduled and out of scope [MAJOR]

**Claim Challenged:** RSK-1 (verifier leniency false-negative, Impact HIGH) and RSK-2 (lens collusion/correlated error, Impact HIGH) both name the same mitigation as their most decisive backstop: *"the **deterministic pre-panel factual lens (L2 Phase 2)** is the structural closure"* (line 741-742, near-identical wording in both rows).

**Counter-Argument:** L2 Architectural Implications describes this exact mechanism as: *"Phase 2 (future, **out of scope**): a deterministic pre-panel factual lens... Phase 3 (future): if verified-criticals proves out framework-wide, consider whether the ps-critic embedded loop should adopt the same gate -- **a separate ADR when evidence warrants**"* (lines 680-684). Phase 3 at least states a trigger condition ("when evidence warrants"). Phase 2 has **no trigger, no timeline, and no corresponding entry in WI-1 through WI-8** (verified by scanning the full Work-Item Decomposition table, lines 758-769) -- it is simply declared out of scope for this ADR with no commitment to when or whether it will be picked up. Calling an unscheduled, unscoped idea "the structural closure" for two HIGH-impact risks overstates how bounded those risks actually are under the plan this ADR proposes to ratify now.

**Evidence:** `projects/PROJ-031-cowork-skeleton/decisions/ADR-adversary-tournament-protocol-001-verified-criticals-methodology.md:680-684 (Evolution path), 741-742 (RSK-1, RSK-2 mitigation cells), 758-769 (full backlog, no Phase-2 item present)`.

**Impact:** RSK-1 and RSK-2 read as adequately mitigated because of the "structural closure" phrase, but the only concrete, scheduled counterweights are the ones already listed alongside it (2-of-3 majority, evidence-anchored factual lens, convergence discriminator, anti-leniency mandate for RSK-1; blindness + distinct rubrics for RSK-2) -- all of which the ADR itself already concedes are "mitigated, not eliminated" / leave a "residual exposure." The unscheduled Phase 2 reference adds an impression of eventual closure without adding any actual near-term bound.

**Dimension:** Actionability

**Response Required:** Either (a) add Phase 2 (the deterministic pre-panel factual lens) as a WI-9 backlog item with an explicit trigger condition analogous to Phase 3's ("when evidence warrants" or a concrete threshold, e.g., "if RSK-1/RSK-2 residual exposure is observed in >= 1 of the first 3 post-ratification C3/C4 tournaments"), or (b) revise RSK-1/RSK-2 to drop the "structural closure" framing and state plainly that the residual exposure is accepted, unmitigated beyond the listed operative controls, pending a future decision.

**Acceptance Criteria:** RSK-1 and RSK-2's mitigation text either references a scheduled work item with a trigger condition, or explicitly states the residual risk is accepted without a committed closure date.

---

## Recommendations

**P0 (Critical -- MUST resolve before acceptance):**
- **DA-001-i2:** Reconcile the "per Critical" vs. "per report" cost-model units with citations to raw panel-file listings; correct or caveat the "~12-15 files per C4 round" claim accordingly.
- **DA-002-i2:** Align the Positive Consequences #4 bullet with D-1's honest "cost decision, not a finding" framing; remove the unqualified "the spiral actually occurs [at C3/C4]" claim.
- **DA-003-i2:** Add WI-8 as an explicit precondition of WI-7 (or equivalent acceptance-criteria language) so RSK-7's mitigation is enforced by the plan, not just asserted in prose.

**P1 (Major -- SHOULD resolve; require justification if not):**
- **DA-004-i2:** Schedule Phase 2 (deterministic pre-panel factual lens) as a triggered future work item, or drop the "structural closure" framing from RSK-1/RSK-2.
- **DA-005-i2:** Add an explicit per-round or per-report ceiling on verifier invocations (or an escalate-to-user rule) to RSK-4's mitigation, since none of its three listed mitigations bounds a single Critical-heavy round.

**P2 (Minor -- MAY resolve; acknowledgment sufficient):**
- **DA-006-i2:** Either narrow the D-1 score gap between Options B and C, or add a footnote clarifying the numeric scores are relative preference orderings under a stated cost assumption, not confidence levels derived from the (all-C4) evidence.

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Neutral | No coverage gap identified by this strategy; the ADR addresses its stated scope thoroughly. |
| Internal Consistency | 0.20 | Negative | DA-002-i2: a Positive Consequence contradicts D-1's own disclaimer on the same page-distance-2000-words topic. |
| Methodological Rigor | 0.20 | Negative | DA-006-i2: numeric scoring in D-1 overstates confidence relative to the ADR's own qualitative hedge. |
| Evidence Quality | 0.15 | Negative | DA-001-i2: the empirical basis for the headline cost-honesty claim (c-004) does not reconcile with the round narratives the ADR itself cites as its evidence. |
| Actionability | 0.15 | Negative | DA-004-i2, DA-005-i2: two risk mitigations (RSK-1/RSK-2's "structural closure," RSK-4's Critical-heavy-round bound) are not backed by scheduled, verifiable work. |
| Traceability | 0.10 | Negative | DA-003-i2: RSK-7's stated mitigation is not encoded in the work-item dependency graph that would actually execute it. |

**Overall assessment:** Targeted revision. The six-decision architecture (D-1 through D-6) and the underlying VERIFIED-CRITICALS mechanism are not in question -- the findings above attack specific passages where the ADR's own careful hedging is contradicted or left unenforced elsewhere in the same document, not the core methodology. All six findings are addressable without touching the chosen options (D-1C, D-2B, D-3B, D-4B, D-5B, D-6A) or any HARD rule.
